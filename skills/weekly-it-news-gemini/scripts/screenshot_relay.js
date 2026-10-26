/**
 * Weekly IT News — Screenshot Relay (Apps Script V8).
 *
 * Gemini Tasks writes nine columns to Google Sheets `queue`:
 * asset_id, slide_id, url, status, file_name, drive_file_id,
 * drive_view_url, captured_at, notes.
 *
 * This relay CAPTURES image files. Only Gemini's inspection of the actual
 * pixels can APPROVE a screenshot for use in a finished presentation.
 *
 * Script Properties (optional; defaults preserve the existing installation):
 *   ITNEWS_ASSETS_FOLDER_ID, ITNEWS_QUEUE_SHEET_NAME,
 *   PSI_API_KEY, SCREENSHOT_API_TEMPLATE.
 *
 * Backoff/recovery metadata lives in the existing `notes` column; no new
 * Sheet columns or migration are required. API keys belong in Script Properties.
 */
const CONFIG = Object.freeze({
  DEFAULT_FOLDER_ID: '1gha0VJobU6ffTlMm5_ypVOck70cIH4pD',
  DEFAULT_SHEET_NAME: 'queue',
  STRATEGY: 'desktop',
  MAX_ROWS_PER_RUN: 8,
  MAX_RUNTIME_MS: 4 * 60 * 1000,
  STALE_PROCESSING_MS: 8 * 60 * 1000,
  MAX_ATTEMPTS: 3,
  BACKOFF_MS: [60 * 1000, 5 * 60 * 1000, 15 * 60 * 1000],
  PSI_COOLDOWN_MS: 10 * 60 * 1000,
  MIN_IMAGE_BYTES: 8 * 1024,
  MAX_IMAGE_BYTES: 15 * 1024 * 1024,
  MIN_IMAGE_WIDTH: 640,
  MIN_IMAGE_HEIGHT: 360,
  META_MARKER: '\n[ITNEWS_RELAY_META] ',
  RELAY_HANDLERS: ['processPendingScreenshots', 'onSheetChange'],
});

function relayProperties_() {
  return PropertiesService.getScriptProperties();
}

function relaySetting_(name, fallback) {
  return String(relayProperties_().getProperty(name) || fallback).trim();
}

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('📸 IT News スクショ取得')
    .addItem('▶ pending行を今すぐ一括撮影', 'processPendingScreenshots')
    .addItem('⏰ 1分おきの自動監視を設定', 'setupTimeTrigger')
    .addItem('🛑 スクショ自動監視を解除', 'removeTriggers')
    .addToUi();
}

/** Only the time-based poll is installed. Sheets API changes don't fire onChange. */
function setupTimeTrigger() {
  removeTriggers();
  ScriptApp.newTrigger('processPendingScreenshots').timeBased().everyMinutes(1).create();
  SpreadsheetApp.getActiveSpreadsheet().toast('1分周期の撮影キュー監視を設定しました。', '設定完了', 5);
}

/** Never delete unrelated triggers that happen to be in the same GAS project. */
function removeTriggers() {
  ScriptApp.getProjectTriggers().forEach(function(trigger) {
    if (CONFIG.RELAY_HANDLERS.indexOf(trigger.getHandlerFunction()) !== -1) {
      ScriptApp.deleteTrigger(trigger);
    }
  });
}

/** Legacy manually installed onChange handlers still work, but are no longer created. */
function onSheetChange(e) {
  processPendingScreenshots();
}

function parseNotes_(raw) {
  const text = String(raw || '');
  const pos = text.lastIndexOf(CONFIG.META_MARKER);
  if (pos < 0) return { userNotes: text, meta: {} };
  try {
    const data = JSON.parse(text.slice(pos + CONFIG.META_MARKER.length));
    if (!data || typeof data !== 'object' || Array.isArray(data)) throw new Error('Invalid metadata');
    return { userNotes: text.slice(0, pos), meta: data };
  } catch (err) {
    return { userNotes: text, meta: {} };
  }
}

function formatNotes_(userNotes, meta) {
  return userNotes + CONFIG.META_MARKER + JSON.stringify(meta);
}

function writeNotes_(sheet, rowNum, col, original, meta) {
  const parsed = parseNotes_(original);
  sheet.getRange(rowNum, col + 1).setValue(formatNotes_(parsed.userNotes, meta));
}

/** Allow only public, ordinary HTTPS domains. Never send private/signed URLs to third parties. */
function validateCaptureUrl_(input) {
  const url = String(input || '').trim();
  if (url.length > 2048 || /[\s\\<>]/.test(url) || !/^https:\/\//i.test(url)) {
    throw new Error('URL must be a public HTTPS URL');
  }
  const match = /^https:\/\/([^/?#]+)/i.exec(url);
  if (!match) throw new Error('Invalid HTTPS URL');
  const authority = match[1];
  if (authority.indexOf('@') !== -1 || authority.indexOf('%') !== -1 || authority.indexOf('[') !== -1) {
    throw new Error('Credentials, encoded hostnames and IPv6 URL literals are not supported');
  }
  const hostAndPort = authority.toLowerCase().split(':');
  if (hostAndPort.length > 2 || (hostAndPort.length === 2 && hostAndPort[1] !== '443')) {
    throw new Error('Only public HTTPS on port 443 is supported');
  }
  const hostname = hostAndPort[0].replace(/\.$/, '');
  const labels = hostname.split('.');
  if (labels.length < 2 || labels.some(function(x) { return !/^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/.test(x); })) {
    throw new Error('Invalid public hostname');
  }
  const tld = labels[labels.length - 1];
  if (!/^(?:[a-z]{2,}|xn--[a-z0-9-]{2,})$/.test(tld)) {
    throw new Error('IP addresses and non-public hostnames are not supported');
  }
  if (['localhost', 'local', 'internal', 'test', 'invalid', 'example', 'corp', 'lan'].indexOf(tld) !== -1 ||
      /^(localhost|metadata|instance-data)(\.|$)/.test(hostname)) {
    throw new Error('Private hostnames are not supported');
  }
  if (/[?&](?:access_token|id_token|auth|authorization|api_key|apikey|token|password|secret|signature|session|code)=/i.test(url)) {
    throw new Error('URLs containing authentication query parameters cannot be sent to screenshot providers');
  }
  return url.split('#')[0]; // Browser fragments are not needed for article screenshots.
}

function safeFileName_(requested, assetId) {
  const defaultStem = String(assetId || 'asset').replace(/[^a-zA-Z0-9_.-]/g, '_').slice(0, 96);
  const name = String(requested || (defaultStem + '.png')).trim();
  if (!name || name.length > 160 || !/^[\w.-]+\.(png|jpe?g)$/i.test(name) ||
      name === '..' || name.indexOf('..') !== -1) {
    return defaultStem + '.png';
  }
  return name;
}

function imageInfo_(blob, declaredType) {
  const bytes = blob.getBytes();
  if (!bytes || bytes.length < CONFIG.MIN_IMAGE_BYTES || bytes.length > CONFIG.MAX_IMAGE_BYTES) {
    throw new Error('Image byte length is outside acceptable bounds');
  }
  const u8 = function(i) { return bytes[i] & 255; };
  const be16 = function(i) { return (u8(i) << 8) | u8(i + 1); };
  const be32 = function(i) { return u8(i) * 16777216 + (u8(i + 1) << 16) + (u8(i + 2) << 8) + u8(i + 3); };
  let width, height, mime, ext;
  if ([137,80,78,71,13,10,26,10].every(function(v, i) { return u8(i) === v; })) {
    mime = 'image/png'; ext = '.png'; width = be32(16); height = be32(20);
  } else if (u8(0) === 255 && u8(1) === 216 && u8(2) === 255) {
    mime = 'image/jpeg'; ext = '.jpg';
    let i = 2;
    while (i + 9 < bytes.length) {
      if (u8(i) !== 255) { i++; continue; }
      while (u8(i) === 255) i++;
      const marker = u8(i++);
      if (marker === 0xD9 || marker === 0xDA) break;
      if (marker === 0xD8 || marker === 0x01 || (marker >= 0xD0 && marker <= 0xD7)) continue;
      if (i + 2 > bytes.length) break;
      const len = be16(i);
      if (len < 2 || i + len > bytes.length) break;
      if ([0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF].indexOf(marker) !== -1) {
        height = be16(i + 3); width = be16(i + 5); break;
      }
      i += len;
    }
  } else {
    throw new Error('HTTP response is not a PNG or JPEG screenshot');
  }
  if (!width || !height || width < CONFIG.MIN_IMAGE_WIDTH || height < CONFIG.MIN_IMAGE_HEIGHT ||
      width > 20000 || height > 20000) {
    throw new Error('Screenshot dimensions are unavailable or too small');
  }
  const claimed = String(declaredType || '').toLowerCase().split(';')[0].trim();
  if (claimed && claimed !== 'application/octet-stream' && claimed !== mime &&
      !(claimed === 'image/jpg' && mime === 'image/jpeg')) {
    throw new Error('Image file signature disagrees with declared MIME type');
  }
  return { mime: mime, ext: ext, width: width, height: height, bytes: bytes.length };
}

function normalizedBlob_(blob, filename, contentType) {
  const info = imageInfo_(blob, contentType);
  const realName = filename.replace(/\.(png|jpe?g)$/i, info.ext);
  const result = Utilities.newBlob(blob.getBytes(), info.mime, realName);
  return { blob: result, fileName: realName, mime: info.mime, width: info.width, height: info.height };
}

function responseHeader_(response, key) {
  const headers = response.getAllHeaders ? response.getAllHeaders() : response.getHeaders();
  const found = Object.keys(headers || {}).find(function(k) { return k.toLowerCase() === key.toLowerCase(); });
  return found ? String(headers[found]) : '';
}

function providerResponse_(url, name, method) {
  const resp = UrlFetchApp.fetch(url, { muteHttpExceptions: true, followRedirects: true });
  const status = resp.getResponseCode();
  if (status !== 200) throw new Error(method + ' HTTP ' + status);
  const result = normalizedBlob_(resp.getBlob(), name, responseHeader_(resp, 'Content-Type'));
  result.method = method;
  return result;
}

function fetchScreenshotBlob(targetUrl, filename) {
  const props = relayProperties_();
  const failures = [];
  const now = Date.now();
  const cooldown = Number(props.getProperty('ITNEWS_PSI_COOLDOWN_UNTIL') || 0);
  if (now >= cooldown) {
    try {
      const key = props.getProperty('PSI_API_KEY');
      let url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=' +
        encodeURIComponent(targetUrl) + '&strategy=' + CONFIG.STRATEGY + '&category=performance';
      if (key) url += '&key=' + encodeURIComponent(key);
      const resp = UrlFetchApp.fetch(url, { muteHttpExceptions: true, followRedirects: true });
      const code = resp.getResponseCode();
      if (code === 429 || code === 503) {
        props.setProperty('ITNEWS_PSI_COOLDOWN_UNTIL', String(now + CONFIG.PSI_COOLDOWN_MS));
        failures.push('PageSpeed HTTP ' + code + ' (cooldown applied)');
      } else if (code !== 200) {
        failures.push('PageSpeed HTTP ' + code);
      } else {
        const data = JSON.parse(resp.getContentText());
        const audits = (data.lighthouseResult && data.lighthouseResult.audits) || {};
        const full = audits['full-page-screenshot'];
        const final = audits['final-screenshot'];
        const uri = (full && full.details && full.details.screenshot && full.details.screenshot.data) ||
          (final && final.details && final.details.data) || '';
        if (!/^data:image\/(?:png|jpeg|jpg);base64,/i.test(uri)) {
          failures.push('PageSpeed has no supported screenshot');
        } else {
          const b64 = uri.slice(uri.indexOf(',') + 1);
          if (b64.length > CONFIG.MAX_IMAGE_BYTES * 1.5) throw new Error('PageSpeed screenshot too large');
          const mime = /^data:([^;]+)/i.exec(uri)[1].toLowerCase().replace('image/jpg','image/jpeg');
          const raw = Utilities.newBlob(Utilities.base64Decode(b64), mime, filename);
          const result = normalizedBlob_(raw, filename, mime);
          result.method = 'PageSpeedInsights_v5';
          return result;
        }
      }
    } catch (err) {
      failures.push('PageSpeed failed: ' + String(err.message).slice(0, 100));
    }
  } else {
    failures.push('PageSpeed temporarily cooling down');
  }

  // Optional paid provider configured via Script Properties, not in source code.
  const custom = props.getProperty('SCREENSHOT_API_TEMPLATE');
  if (custom) {
    try {
      if (!/^https:\/\//i.test(custom) || custom.indexOf('{URL}') < 0) {
        throw new Error('Invalid SCREENSHOT_API_TEMPLATE configuration');
      }
      const result = providerResponse_(custom.replace('{URL}', encodeURIComponent(targetUrl)), filename, 'CustomScreenshotAPI');
      return result;
    } catch (err) {
      // Do not print the custom provider URL or embedded API key.
      failures.push('Custom screenshot API failed: ' + String(err.message).slice(0, 100));
    }
  }

  try {
    // Preserve the URL form verified in the Gemini+GAS production PoC.
    return providerResponse_('https://image.thum.io/get/width/1280/crop/853/noanimate/' + targetUrl,
      filename, 'ThumIO_Fallback');
  } catch (err) {
    failures.push('ThumIO failed: ' + String(err.message).slice(0, 100));
  }
  throw new Error('All screenshot providers failed: ' + failures.join(' | '));
}

function markError_(sheet, rowNum, idx, initialNotes, meta, message, retry) {
  meta.processingStartedAt = null;
  meta.lastError = String(message).slice(0, 350);
  if (retry && meta.attempt < CONFIG.MAX_ATTEMPTS) {
    const delay = CONFIG.BACKOFF_MS[Math.min(meta.attempt - 1, CONFIG.BACKOFF_MS.length - 1)];
    meta.nextRetryAt = new Date(Date.now() + delay).toISOString();
    sheet.getRange(rowNum, idx.status + 1).setValue('pending');
  } else {
    meta.nextRetryAt = null;
    sheet.getRange(rowNum, idx.status + 1).setValue('error');
  }
  writeNotes_(sheet, rowNum, idx.notes, initialNotes, meta);
}

function trashOldFile_(previousId, newId, folderId) {
  if (!previousId || String(previousId) === String(newId)) return;
  try {
    const previous = DriveApp.getFileById(String(previousId));
    const parents = previous.getParents();
    while (parents.hasNext()) {
      if (parents.next().getId() === folderId) {
        previous.setTrashed(true);
        return;
      }
    }
  } catch (err) {
    console.warn('Unable to retire previous screenshot file; the new reference is safe.');
  }
}

function processPendingScreenshots() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return { skipped: 'locked' };
  const summary = { captured: 0, failed: 0, deferred: 0, recovered: 0 };
  const started = Date.now();
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(relaySetting_('ITNEWS_QUEUE_SHEET_NAME', CONFIG.DEFAULT_SHEET_NAME));
    if (!sheet) throw new Error('Screenshot queue sheet not found');
    const lastRow = sheet.getLastRow();
    if (lastRow < 2) return summary;
    const data = sheet.getRange(1, 1, lastRow, 9).getValues();
    const headers = data[0].map(function(h) { return String(h).trim().toLowerCase(); });
    const columns = ['asset_id','slide_id','url','status','file_name','drive_file_id','drive_view_url','captured_at','notes'];
    const idx = {};
    columns.forEach(function(name) { idx[name] = headers.indexOf(name); });
    const missing = columns.filter(function(name) { return idx[name] < 0; });
    if (missing.length) throw new Error('Missing queue headers: ' + missing.join(', '));
    const folderId = relaySetting_('ITNEWS_ASSETS_FOLDER_ID', CONFIG.DEFAULT_FOLDER_ID);
    const folder = DriveApp.getFolderById(folderId);
    let handled = 0;
    for (let i = 1; i < data.length; i++) {
      if (handled >= CONFIG.MAX_ROWS_PER_RUN || Date.now() - started > CONFIG.MAX_RUNTIME_MS) break;
      const row = data[i];
      const rowNum = i + 1;
      let status = String(row[idx.status] || '').trim().toLowerCase();
      const note = String(row[idx.notes] || '');
      const parsed = parseNotes_(note);
      const meta = parsed.meta;
      if (status === 'processing') {
        const elapsed = Date.now() - Date.parse(meta.processingStartedAt || '');
        if (!Number.isFinite(elapsed) || elapsed >= CONFIG.STALE_PROCESSING_MS) {
          summary.recovered++;
          meta.attempt = Math.max(1, Number(meta.attempt) || 1);
          markError_(sheet, rowNum, idx, note, meta, 'Recovered stale processing job', true);
          // Re-attempt on the next poll, respecting the backoff.
        }
        continue;
      }
      if (status !== 'pending') continue;
      if (meta.nextRetryAt && Date.parse(meta.nextRetryAt) > Date.now()) {
        summary.deferred++;
        continue;
      }
      handled++;
      let target;
      try {
        target = validateCaptureUrl_(row[idx.url]);
      } catch (err) {
        markError_(sheet, rowNum, idx, note, meta, err.message, false);
        summary.failed++;
        continue;
      }
      const assetId = String(row[idx.asset_id] || 'asset_' + rowNum).trim();
      const requestedName = safeFileName_(row[idx.file_name], assetId);
      const oldId = String(row[idx.drive_file_id] || '').trim();
      // A manually re-queued row after exhausting retries starts a new attempt cycle.
      if (Number(meta.attempt) >= CONFIG.MAX_ATTEMPTS) meta.attempt = 0;
      meta.attempt = Math.max(0, Number(meta.attempt) || 0) + 1;
      meta.processingStartedAt = new Date().toISOString();
      meta.nextRetryAt = null;
      sheet.getRange(rowNum, idx.status + 1).setValue('processing');
      writeNotes_(sheet, rowNum, idx.notes, note, meta);
      SpreadsheetApp.flush();
      try {
        const image = fetchScreenshotBlob(target, requestedName);
        // Save and verify the new file before changing any previous file.
        const newFile = folder.createFile(image.blob);
        newFile.setDescription('Weekly IT News source: ' + target + ' | via ' + image.method);
        sheet.getRange(rowNum, idx.file_name + 1).setValue(image.fileName);
        sheet.getRange(rowNum, idx.drive_file_id + 1).setValue(newFile.getId());
        sheet.getRange(rowNum, idx.drive_view_url + 1).setValue(newFile.getUrl());
        sheet.getRange(rowNum, idx.captured_at + 1).setValue(new Date().toISOString());
        meta.processingStartedAt = null;
        meta.lastError = null;
        meta.attempt = 0; // Future manual recaptures start with a clean budget.
        meta.lastMethod = image.method;
        meta.dimensions = image.width + 'x' + image.height;
        writeNotes_(sheet, rowNum, idx.notes, note, meta);
        sheet.getRange(rowNum, idx.status + 1).setValue('captured');
        SpreadsheetApp.flush();
        summary.captured++;
        // Never trash unrelated same-named files; only the prior file of this row.
        trashOldFile_(oldId, newFile.getId(), folderId);
      } catch (err) {
        const msg = String(err.message || err).slice(0, 350);
        markError_(sheet, rowNum, idx, note, meta, msg, true);
        summary.failed++;
        console.warn('Screenshot capture failed at row ' + rowNum + ' (attempt ' + meta.attempt + ')');
      }
    }
    return summary;
  } finally {
    lock.releaseLock();
  }
}