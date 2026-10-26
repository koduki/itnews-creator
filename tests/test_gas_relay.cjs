'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const SCRIPT = fs.readFileSync(path.join(__dirname, '..', 'skills/weekly-it-news-gemini/scripts/screenshot_relay.js'), 'utf8');
const HEADERS = ['asset_id','slide_id','url','status','file_name','drive_file_id','drive_view_url','captured_at','notes'];

function png(width=1280, height=853, length=9000) {
  const b = Buffer.alloc(length, 0);
  Buffer.from([137,80,78,71,13,10,26,10]).copy(b);
  b.writeUInt32BE(13, 8); Buffer.from('IHDR').copy(b, 12);
  b.writeUInt32BE(width,16);b.writeUInt32BE(height,20);
  return b;
}
function blob(data, mime='image/png', name='test.png') {
  return {
    data:Buffer.from(data), mime, name,
    getBytes(){return Array.from(this.data.values());},
    getContentType(){return this.mime;},
    setName(next){this.name=next;return this;},
  };
}
function response(code, body, mime) {
  return {
    getResponseCode(){return code;},
    getContentText(){return typeof body==='string'?body:JSON.stringify(body);},
    getBlob(){return blob(body, mime || 'image/png');},
    getAllHeaders(){return {'content-type':mime || 'application/json'};},
  };
}
function harness({rows=[], fetch, props={}}={}) {
  props.ITNEWS_ASSETS_FOLDER_ID ??= 'test-folder';
  const values = [HEADERS, ...rows.map(x=>HEADERS.map(k=>x[k]??''))];
  const files=new Map(); const trashed=[];let seq=1;
  const folder = {getId(){return 'test-folder';}, createFile(image){
    const id='file-'+seq++;
    const file={ id, image, desc:'', getId(){return id;}, getUrl(){return 'https://drive.google.com/file/d/'+id;},
      setDescription(text){this.desc=text;}, setTrashed(v){if(v)trashed.push(id);},
      getParents(){let once=false;return {hasNext(){return !once;}, next(){once=true;return folder;}};},
    };
    files.set(id,file);return file;
  }};
  const sheet={
    getLastRow(){return values.length;},
    getRange(row,col,numRows=1,numCols=1){return {
      getValues(){return values.slice(row-1,row-1+numRows).map(r=>r.slice(col-1,col-1+numCols));},
      setValue(v){values[row-1][col-1]=v;},
    };},
  };
  const projectTriggers = [];
  const hooks = {
    props, values, files, trashed, projectTriggers,
    context: {
      Buffer, console:{warn(){},log(){}}, Date,
      PropertiesService:{getScriptProperties(){return {getProperty(key){return props[key]??null;},setProperty(key,val){props[key]=String(val);}};}},
      SpreadsheetApp:{getActiveSpreadsheet(){return {getSheetByName(name){return name==='queue'?sheet:null;},toast(){}};},flush(){},getUi(){return {createMenu(){return {addItem(){return this;},addToUi(){}};}};}},
      LockService:{getScriptLock(){return {tryLock(){return true;},releaseLock(){}};}},
      DriveApp:{getFolderById(){return folder;},getFileById(id){const f=files.get(id);if(!f)throw Error('Unknown file');return f;}},
      UrlFetchApp:{fetch(url, opts){return fetch(url, opts);}},
      Utilities:{base64Decode(s){return Array.from(Buffer.from(s,'base64'));},newBlob(bytes,mime,name){return blob(bytes,mime,name);}},
      ScriptApp:{getProjectTriggers(){return projectTriggers;},deleteTrigger(t){projectTriggers.splice(projectTriggers.indexOf(t),1);},newTrigger(name){return {timeBased(){return this;},everyMinutes(n){assert.equal(n,1);return this;},create(){projectTriggers.push({getHandlerFunction(){return name;}});}};}},
    }
  };
  vm.createContext(hooks.context);
  vm.runInContext(SCRIPT+'\nthis.api={validateCaptureUrl_,imageInfo_,fetchScreenshotBlob,processPendingScreenshots,setupTimeTrigger,removeTriggers,parseNotes_,formatNotes_};',hooks.context);
  hooks.api=hooks.context.api;
  return hooks;
}

const url='https://www.example-news.com/article';
function queue(status='pending', opts={}) {return {
  asset_id:'src1',slide_id:'s04',url,status,file_name:'src1.png',
  drive_file_id:'',drive_view_url:'',captured_at:'',notes:'human note', ...opts,
};}

test('reject internal/secret/invalid target URLs, accept public HTTPS',()=>{
  const h=harness();
  assert.equal(h.api.validateCaptureUrl_(url),url);
  for (const bad of ['http://www.example-news.com','https://localhost/test','https://10.1.2.3/','https://metadata.google.internal/',
    'https://user:pass@www.example-news.com','https://www.example-news.com/?access_token=secret','https://www.example-news.com:8080/']) {
    assert.throws(()=>h.api.validateCaptureUrl_(bad), undefined, bad);
  }
});

test('PNG is validated by signature, bytes and dimensions; HTML and tiny screenshots rejected',()=>{
  const h=harness();
  const pic= h.api.imageInfo_(blob(png()),'image/png');
  assert.equal(pic.width,1280);assert.equal(pic.height,853);
  assert.throws(()=>h.api.imageInfo_(blob(Buffer.alloc(9000,60)),'image/png'),/not a PNG or JPEG/);
  assert.throws(()=>h.api.imageInfo_(blob(png(200,100)),'image/png'),/too small/);
  assert.throws(()=>h.api.imageInfo_(blob(png()),'text/html'),/MIME type/);
});

test('PageSpeed 429 triggers cooldown and valid ThumIO PNG fallback',()=>{
  const called=[];
  const h=harness({fetch(uri){called.push(uri);return uri.includes('googleapis.com')?response(429,'fail','text/plain'):response(200,png(),'image/png');}});
  const first=h.api.fetchScreenshotBlob(url,'src1.png');
  assert.equal(first.method,'ThumIO_Fallback');
  assert.equal(first.fileName,'src1.png');
  assert.ok(Number(h.props.ITNEWS_PSI_COOLDOWN_UNTIL)>Date.now());
  const second=h.api.fetchScreenshotBlob(url,'src1.png');
  assert.equal(second.method,'ThumIO_Fallback');
  assert.equal(called.filter(x=>x.includes('googleapis.com')).length,1);
});

test('a valid PageSpeed data URL is accepted without falling back',()=>{
  const uri='data:image/png;base64,'+png().toString('base64');
  const h=harness({fetch(u){assert.match(u,/pagespeedonline/);return response(200,{lighthouseResult:{audits:{'final-screenshot':{details:{data:uri}}}}},'application/json');}});
  const img=h.api.fetchScreenshotBlob(url,'src1.png');
  assert.equal(img.method,'PageSpeedInsights_v5');
  assert.equal(img.width,1280);
});

test('success writes nine-column sheet, preserves human notes, and trashes only row previous file',()=>{
  const h=harness({rows:[queue()],fetch(u){return u.includes('googleapis.com')?response(503,'overload','text/plain'):response(200,png(),'image/png');}});
  const old=h.context.DriveApp.getFolderById('test-folder').createFile(blob(png()));
  h.values[1][5]=old.getId();
  const result=h.api.processPendingScreenshots();
  assert.equal(result.captured,1);assert.equal(h.values[1][3],'captured');
  assert.equal(h.values[1][4],'src1.png');
  assert.equal(h.trashed.join(),old.getId());
  assert.notEqual(h.values[1][5],old.getId());
  assert.match(h.values[1][8],/human note/);
  assert.match(h.values[1][8],/ThumIO_Fallback/);
});

test('failed capture does not delete previous image and schedules retry',()=>{
  const h=harness({rows:[queue()],fetch(){return response(500,'error','text/html');}});
  const old=h.context.DriveApp.getFolderById('test-folder').createFile(blob(png()));
  h.values[1][5]=old.getId();
  const result=h.api.processPendingScreenshots();
  assert.equal(result.failed,1);assert.equal(h.values[1][3],'pending');
  assert.equal(h.values[1][5],old.getId());assert.equal(h.trashed.length,0);
  const parsed=h.api.parseNotes_(h.values[1][8]);
  assert.equal(parsed.meta.attempt,1);
  assert.ok(Date.parse(parsed.meta.nextRetryAt)>Date.now());
  assert.match(parsed.meta.lastError,/All screenshot providers failed/);
  // Subsequent poll must honor backoff and not call a provider.
  assert.equal(h.api.processPendingScreenshots().deferred,1);
});

test('stale processing is recovered and eventually transitions to error',()=>{
  const m={attempt:1,processingStartedAt:new Date(Date.now()-9*60*1000).toISOString()};
  const h=harness({rows:[queue('processing',{notes:'note\n[ITNEWS_RELAY_META] '+JSON.stringify(m)})],fetch(){throw Error('unexpected');}});
  const out=h.api.processPendingScreenshots();
  assert.equal(out.recovered,1);assert.equal(h.values[1][3],'pending');
  const recovered=h.api.parseNotes_(h.values[1][8]).meta;
  assert.equal(recovered.processingStartedAt,null);
  assert.ok(Date.parse(recovered.nextRetryAt)>Date.now());
  h.values[1][3]='processing';
  h.values[1][8]='note\n[ITNEWS_RELAY_META] '+JSON.stringify({attempt:3,processingStartedAt:new Date(Date.now()-9*60*1000).toISOString()});
  h.api.processPendingScreenshots();
  assert.equal(h.values[1][3],'error');
});

test('invalid pending URL fails visibly; unrelated triggers are preserved',()=>{
  const h=harness({rows:[queue('pending',{url:'https://localhost/private'})],fetch(){throw Error('unexpected');}});
  assert.equal(h.api.processPendingScreenshots().failed,1);
  assert.equal(h.values[1][3],'error');
  h.projectTriggers.push({getHandlerFunction(){return 'unrelatedImportantTrigger';}});
  h.api.setupTimeTrigger();
  assert.deepEqual(h.projectTriggers.map(t=>t.getHandlerFunction()),['unrelatedImportantTrigger','processPendingScreenshots']);
  h.api.removeTriggers();
  assert.deepEqual(h.projectTriggers.map(t=>t.getHandlerFunction()),['unrelatedImportantTrigger']);
});