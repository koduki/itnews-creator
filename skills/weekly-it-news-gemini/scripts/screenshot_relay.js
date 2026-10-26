/**
 * Weekly IT News — Screenshot Capture Relay Bot (Google Apps Script)
 *
 * 監視対象シート: itnews-screenshot-queue (Sheet ID: 1G3qzrzC4P_y-Kh8YeiJGKiBBC_-gaEDgXbbBD81hZK8)
 * 保存先Driveフォルダ: itnews-assets (Folder ID: 1gha0VJobU6ffTlMm5_ypVOck70cIH4pD)
 *
 * 【機能】
 * 1. シート「queue」の status 列が "pending" の行を検出
 * 2. 第1経路: Google PageSpeed Insights API (v5, desktop) を呼び出し、
 *    lighthouseResult.audits['final-screenshot'] または full-page-screenshot から Base64 PNG を抽出
 * 3. 第2経路 (フォールバック): PageSpeed API がブロック/タイムアウトした場合は、
 *    無料の認証不要スクリーンショットAPI (WordPress mshots / Thum.io) または
 *    スクリプトプロパティ設定済みの ScreenshotOne / Urlbox API で PNG を取得
 * 4. Google Drive の `itnews-assets` フォルダに `<asset_id>.png` として保存し、
 *    シートの status を "captured"、drive_file_id / drive_view_url / captured_at を自動記録
 */

const CONFIG = {
  FOLDER_ID: '1gha0VJobU6ffTlMm5_ypVOck70cIH4pD', // Google Drive `itnews-assets` フォルダID
  SHEET_NAME: 'queue',
  STRATEGY: 'desktop', // 'desktop' (16:9向きの横長画面) または 'mobile'
};

/**
 * スプレッドシートを開いたときにカスタムメニューを追加
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('📸 IT News スクショ取得')
    .addItem('▶ pending行を今すぐ一括撮影', 'processPendingScreenshots')
    .addItem('⏰ 1分おきの自動監視トリガーを設定', 'setupTimeTrigger')
    .addItem('🛑 自動監視トリガーを解除', 'removeTriggers')
    .addToUi();
}

/**
 * 1分おきの時間主導型トリガーと編集時トリガーを登録（初回1回だけ実行）
 */
function setupTimeTrigger() {
  removeTriggers();
  ScriptApp.newTrigger('processPendingScreenshots')
    .timeBased()
    .everyMinutes(1)
    .create();
  ScriptApp.newTrigger('onSheetChange')
    .forSpreadsheet(SpreadsheetApp.getActiveSpreadsheet())
    .onChange()
    .create();
  SpreadsheetApp.getActiveSpreadsheet().toast(
    '自動監視トリガー（1分周期＆シート変更時）を設定しました。',
    '設定完了',
    5
  );
}

/**
 * 既存トリガーの削除
 */
function removeTriggers() {
  const triggers = ScriptApp.getProjectTriggers();
  for (const t of triggers) {
    ScriptApp.deleteTrigger(t);
  }
}

/**
 * シート変更時トリガー（Geminiのsheets_agentが行を追加した際に発火）
 */
function onSheetChange(e) {
  processPendingScreenshots();
}

/**
 * メイン処理: status が 'pending' の行を順番に撮影して Google Drive へ保存
 */
function processPendingScreenshots() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) {
    console.log('別プロセスが実行中のためスキップします。');
    return;
  }

  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(CONFIG.SHEET_NAME) || ss.getSheets()[0];
    const lastRow = sheet.getLastRow();
    if (lastRow < 2) return;

    const range = sheet.getRange(1, 1, lastRow, 9);
    const values = range.getValues();
    const headers = values[0].map(h => String(h).trim().toLowerCase());

    const idx = {
      assetId: headers.indexOf('asset_id'),
      slideId: headers.indexOf('slide_id'),
      url: headers.indexOf('url'),
      status: headers.indexOf('status'),
      fileName: headers.indexOf('file_name'),
      driveFileId: headers.indexOf('drive_file_id'),
      driveViewUrl: headers.indexOf('drive_view_url'),
      capturedAt: headers.indexOf('captured_at'),
      notes: headers.indexOf('notes'),
    };

    const missing = Object.entries(idx).filter(([_, value]) => value < 0).map(([name]) => name);
    if (missing.length) {
      throw new Error('Missing required queue columns: ' + missing.join(', '));
    }

    const folder = DriveApp.getFolderById(CONFIG.FOLDER_ID);

    for (let r = 1; r < values.length; r++) {
      const row = values[r];
      const status = String(row[idx.status] || '').trim().toLowerCase();
      const targetUrl = String(row[idx.url] || '').trim();
      const assetId = String(row[idx.assetId] || `asset_${r}`).trim();

      // Only public HTTPS article URLs. Never relay secrets or internal pages to screenshot providers.
      if (status !== 'pending' || !/^https:\/\/[^\s/?#]+/i.test(targetUrl)) {
        continue;
      }

      const rowNum = r + 1;
      const outFileName = String(row[idx.fileName] || `${assetId}.png`).trim();

      // 処理中ステータスに更新
      sheet.getRange(rowNum, idx.status + 1).setValue('processing');
      SpreadsheetApp.flush();

      try {
        const result = fetchScreenshotBlob(targetUrl, outFileName);

        // 同名ファイルが既にフォルダ内にあれば上書き用にゴミ箱へ移動
        const existing = folder.getFilesByName(outFileName);
        while (existing.hasNext()) {
          existing.next().setTrashed(true);
        }

        const file = folder.createFile(result.blob);
        file.setDescription(`Source URL: ${targetUrl} | Captured via ${result.method}`);

        const nowIso = new Date().toISOString();
        sheet.getRange(rowNum, idx.status + 1).setValue('captured');
        sheet.getRange(rowNum, idx.fileName + 1).setValue(outFileName);
        sheet.getRange(rowNum, idx.driveFileId + 1).setValue(file.getId());
        sheet.getRange(rowNum, idx.driveViewUrl + 1).setValue(file.getUrl());
        sheet.getRange(rowNum, idx.capturedAt + 1).setValue(nowIso);

        const prevNotes = String(row[idx.notes] || '').trim();
        sheet.getRange(rowNum, idx.notes + 1).setValue(
          prevNotes ? `${prevNotes} [Method: ${result.method}]` : `[Method: ${result.method}]`
        );
        SpreadsheetApp.flush();
      } catch (err) {
        console.error(`Row ${rowNum} (${targetUrl}) failed:`, err);
        sheet.getRange(rowNum, idx.status + 1).setValue('error');
        const prevNotes = String(row[idx.notes] || '').trim();
        sheet.getRange(rowNum, idx.notes + 1).setValue(
          `${prevNotes} [ERROR: ${err.message}]`
        );
      }
    }
  } finally {
    lock.releaseLock();
  }
}

/**
 * URLからスクリーンショットのPNG Blobを取得する（複数経路フォールバック付き）
 */
function fetchScreenshotBlob(targetUrl, fileName) {
  const props = PropertiesService.getScriptProperties();

  // 経路1: Google PageSpeed Insights API (v5)
  // ※スクリプトプロパティ `PSI_API_KEY` があれば付与（なくても無料クォータで動作）
  try {
    const psiKey = props.getProperty('PSI_API_KEY');
    let apiUrl =
      'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=' +
      encodeURIComponent(targetUrl) +
      '&strategy=' +
      CONFIG.STRATEGY +
      '&category=performance';
    if (psiKey) {
      apiUrl += '&key=' + encodeURIComponent(psiKey);
    }

    const res = UrlFetchApp.fetch(apiUrl, {
      muteHttpExceptions: true,
      followRedirects: true,
    });

    if (res.getResponseCode() === 200) {
      const data = JSON.parse(res.getContentText());
      const audits = (data.lighthouseResult && data.lighthouseResult.audits) || {};

      // 高解像度の full-page-screenshot または final-screenshot を取得
      let dataUri = null;
      if (
        audits['full-page-screenshot'] &&
        audits['full-page-screenshot'].details &&
        audits['full-page-screenshot'].details.screenshot &&
        audits['full-page-screenshot'].details.screenshot.data
      ) {
        dataUri = audits['full-page-screenshot'].details.screenshot.data;
      } else if (
        audits['final-screenshot'] &&
        audits['final-screenshot'].details &&
        audits['final-screenshot'].details.data
      ) {
        dataUri = audits['final-screenshot'].details.data;
      }

      if (dataUri && dataUri.indexOf('base64,') !== -1) {
        const parts = dataUri.split('base64,');
        const mimeMatch = parts[0].match(/data:([^;]+);/);
        const mimeType = mimeMatch ? mimeMatch[1] : 'image/png';
        const bytes = Utilities.base64Decode(parts[1]);
        const blob = Utilities.newBlob(bytes, mimeType, fileName);
        return { blob: blob, method: 'PageSpeedInsights_v5' };
      }
    }
  } catch (psiErr) {
    console.warn('PageSpeed Insights API fallback triggered:', psiErr);
  }

  // 経路2: カスタムScreenshot API（ScreenshotOne / Urlbox 等をスクリプトプロパティに設定している場合）
  const customApiTemplate = props.getProperty('SCREENSHOT_API_TEMPLATE');
  // 例: https://api.screenshotone.com/take?access_key=YOUR_KEY&url={URL}&viewport_width=1440&viewport_height=900&format=png
  if (customApiTemplate) {
    const customUrl = customApiTemplate.replace('{URL}', encodeURIComponent(targetUrl));
    const res2 = UrlFetchApp.fetch(customUrl, { muteHttpExceptions: true });
    if (res2.getResponseCode() === 200) {
      const blob = res2.getBlob().setName(fileName);
      return { blob: blob, method: 'CustomScreenshotAPI' };
    }
  }

  // 経路3: 認証不要の公開スクリーンショット中継 (thum.io 1280x853 PNG)
  const thumUrl = `https://image.thum.io/get/width/1280/crop/853/noanimate/${targetUrl}`;
  const res3 = UrlFetchApp.fetch(thumUrl, {
    muteHttpExceptions: true,
    followRedirects: true,
  });
  if (
    res3.getResponseCode() === 200 &&
    res3.getHeaders()['Content-Type'] &&
    String(res3.getHeaders()['Content-Type']).indexOf('image/') !== -1
  ) {
    const blob = res3.getBlob().setName(fileName);
    return { blob: blob, method: 'ThumIO_Fallback' };
  }

  throw new Error('All screenshot capture methods failed for URL: ' + targetUrl);
}