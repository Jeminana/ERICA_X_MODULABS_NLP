// Local browser QA using installed Chrome. No dependencies or runtime build step.
import {createServer} from 'node:http';
import {readFile,writeFile,mkdtemp} from 'node:fs/promises';
import {join,resolve,extname,sep} from 'node:path';
import {tmpdir} from 'node:os';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import assert from 'node:assert/strict';

const root=resolve(fileURLToPath(new URL('../portfolio/',import.meta.url)));
const exportCards=process.argv.includes('--export-cards');
const overview=process.argv.includes('--overview');
const submission=process.argv.includes('--submission');
const temp=await mkdtemp(join(tmpdir(),'najmi-portfolio-qa-'));
const server=createServer(async(req,res)=>{
  try{
    const name=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const path=resolve(root,'.'+(name.endsWith('/')?name+'index.html':name));
    if(!path.startsWith(root+sep)){res.writeHead(403).end();return;}
    const bytes=await readFile(path);
    const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.mp4':'video/mp4','.jpg':'image/jpeg','.png':'image/png'};
    // Chrome can seek in the demo recording during QA.
    const range=req.headers.range?.match(/^bytes=(\d+)-(\d*)$/);
    if(range){const start=Number(range[1]),end=range[2]?Number(range[2]):bytes.length-1;res.writeHead(206,{'Content-Type':types[extname(path)]||'application/octet-stream','Accept-Ranges':'bytes','Content-Range':`bytes ${start}-${end}/${bytes.length}`,'Content-Length':end-start+1});res.end(bytes.subarray(start,end+1));}
    else{res.writeHead(200,{'Content-Type':types[extname(path)]||'application/octet-stream','Accept-Ranges':'bytes'});res.end(bytes);}
  }catch{res.writeHead(404).end();}
});
await new Promise(done=>server.listen(0,'127.0.0.1',done));
const url=submission?pathToFileURL(join(root,'나즈미_인공지능학과_2024079443.html')).href:`http://127.0.0.1:${server.address().port}/${overview?'cardnews/overview.html':exportCards?'cardnews/':''}`;
const chrome=spawn('C:/Program Files/Google/Chrome/Application/chrome.exe',['--headless=new','--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--remote-debugging-port=0',`--user-data-dir=${join(temp,'chrome')}`,'about:blank'],{windowsHide:true,stdio:['ignore','ignore','pipe']});
let ws;
try{
  const endpoint=await Promise.race([new Promise((done,reject)=>{let log='';chrome.stderr.on('data',chunk=>{log+=chunk.toString();const match=log.match(/DevTools listening on (ws:\/\/\S+)/);if(match)done(match[1]);});chrome.on('error',reject);chrome.on('exit',code=>reject(new Error('Chrome exited '+code)));}),new Promise((_,reject)=>setTimeout(()=>reject(new Error('Chrome startup timeout')),15000))]);
  ws=new WebSocket(endpoint);await new Promise((done,reject)=>{ws.addEventListener('open',done);ws.addEventListener('error',reject);});
  let sequence=0;const pending=new Map();const errors=[];
  ws.addEventListener('message',event=>{const m=JSON.parse(event.data);if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);}}});
  function send(method,params={},sessionId){return new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params,...(sessionId?{sessionId}:{})}));});}
  const {targetId}=await send('Target.createTarget',{url:'about:blank'});
  const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});
  const command=(method,params={})=>send(method,params,sessionId);
  const evaluate=async(expression)=>{const r=await command('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  await command('Page.enable');await command('Runtime.enable');
  if(submission){await command('Network.enable');await command('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:-1,uploadThroughput:-1});}
  await command('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
  await command('Page.navigate',{url});
  for(let i=0;i<100;i++){if(await evaluate(`location.href===${JSON.stringify(url)} && document.readyState==='complete'`))break;await new Promise(done=>setTimeout(done,100));}
  await evaluate('document.fonts.ready.then(()=>true)');
  if(overview){
    assert.equal(await evaluate('document.querySelectorAll(".grid img").length'),5);
    await evaluate('Promise.all([...document.images].map(i=>i.decode()))');
    const layout=await evaluate(`(()=>{const cards=[...document.querySelectorAll('.grid figure')].map(e=>e.getBoundingClientRect());return {sameRow:cards.every(c=>Math.abs(c.top-cards[0].top)<1),allVisible:cards.every(c=>c.bottom<=innerHeight&&c.right<=innerWidth)}})()`);
    assert.ok(layout.sameRow&&layout.allVisible,JSON.stringify(layout));
    const screenshot=await command('Page.captureScreenshot',{format:'png'});
    await writeFile(join(temp,'cardnews-overview.png'),Buffer.from(screenshot.data,'base64'));
    for(const width of [768,390,320]){
      await command('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:width<700});
      assert.ok(await evaluate('document.documentElement.scrollWidth<=innerWidth'));
    }
    assert.deepEqual(errors,[]);
    console.log(JSON.stringify({layout,mobileOverflow:false,screenshot:join(temp,'cardnews-overview.png')}));
  }else if(exportCards){
    assert.equal(await evaluate('document.querySelectorAll(".news-card").length'),5);
    assert.ok(await evaluate('Promise.all([...document.images].map(i=>i.decode())).then(()=>true)'));
    await command('Emulation.setDeviceMetricsOverride',{width:1080,height:1350,deviceScaleFactor:1,mobile:false});
    await evaluate('document.body.classList.add("export-mode")');
    const exports=[];
    for(let number=1;number<=5;number++){
      const id=`card-${String(number).padStart(2,'0')}`;
      const info=await evaluate(`(()=>{document.querySelectorAll('.card-shell').forEach(s=>s.classList.remove('is-export'));const card=document.getElementById('${id}');card.parentElement.classList.add('is-export');window.scrollTo({top:0,behavior:'instant'});const r=card.getBoundingClientRect();const footer=card.querySelector('.card-bottom').getBoundingClientRect();const overlaps=[...card.querySelectorAll('h2,.support,.objects,.pipeline,.demo-panel,.signature,.featured,.name,.english-name,.school')].filter(e=>{const b=e.getBoundingClientRect();return b.bottom>footer.top+1||b.right>r.right+1||b.left<r.left-1}).map(e=>e.className||e.tagName);return {width:r.width,height:r.height,overlaps};})()`);
      assert.equal(info.width,1080);assert.equal(info.height,1350);assert.deepEqual(info.overlaps,[],id+' clipped or footer overlap');
      assert.ok(await evaluate(`(()=>{const c=document.getElementById('${id}');const s=c.querySelector('.support');const v=c.querySelector('.objects,.pipeline,.demo-panel,.signature,.personal-values,.personal-projects');return !s||!v||v.getBoundingClientRect().top>=s.getBoundingClientRect().bottom+16})()`),id+' text and visual overlap');
      assert.ok(await evaluate(`(()=>{const lines=[...document.querySelectorAll('#${id} .support>span')];return lines.length<=3&&lines.every(e=>e.getBoundingClientRect().height<=parseFloat(getComputedStyle(e).lineHeight)+1)})()`),id+' supporting text exceeds three lines');
      const shot=await command('Page.captureScreenshot',{format:'png',clip:{x:0,y:0,width:1080,height:1350,scale:1},captureBeyondViewport:true});
      await writeFile(join(root,'cardnews',id+'.png'),Buffer.from(shot.data,'base64'));
      exports.push({file:id+'.png',...info});
    }
    await evaluate('document.body.classList.remove("export-mode");document.querySelectorAll(".is-export").forEach(s=>s.classList.remove("is-export"))');
    for(const width of [1440,390,320]){
      await command('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:width<700});
      const mobile=await evaluate(`(()=>{window.dispatchEvent(new Event('resize'));return {width:innerWidth,scroll:document.documentElement.scrollWidth,cardWidth:document.querySelector('.news-card').getBoundingClientRect().width,shellWidth:document.querySelector('.card-shell').clientWidth};})()`);
      assert.ok(mobile.scroll<=mobile.width,JSON.stringify(mobile));assert.ok(Math.abs(mobile.cardWidth-mobile.shellWidth)<1);
    }
    assert.deepEqual(errors,[]);
    console.log(JSON.stringify({exports,previewWidths:[1440,390,320],scriptErrors:errors},null,2));
  }else{
  assert.equal(await evaluate('document.documentElement.lang'),'ko');
  assert.equal(await evaluate('document.querySelectorAll(".case-part h4").length'),5);
  assert.equal(await evaluate('document.querySelectorAll(".cards .card").length'),3);
  const checks=[];
  for(const width of [1440,768,390,320]){
    await command('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:width<700});
    for(const language of ['ko','en']){
      await evaluate(`document.querySelector('[data-language="${language}"]').click()`);
      const state=await evaluate(`(()=>({lang:document.documentElement.lang,width:innerWidth,scroll:document.documentElement.scrollWidth,overflow:[...document.querySelectorAll('main *, .topbar *')].filter(e=>{if(e.closest('.cardnews-item'))return false;const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+2||r.left< -2)}).slice(0,8).map(e=>({tag:e.tagName,class:e.className,text:e.innerText?.slice(0,45)})),name:JSON.parse(document.getElementById('person-data').textContent).name,title:document.title}))()`);
      assert.equal(state.lang,language);assert.ok(state.scroll<=state.width,'Horizontal page overflow');assert.equal(state.overflow.length,0,JSON.stringify(state));
      assert.equal(await evaluate(`getComputedStyle(document.querySelector('.headline [lang="${language==='ko'?'en':'ko'}"]')).display`),'none');
      checks.push({width,language,overflow:false});
      if((width===1440&&language==='ko')||(width===390&&language==='en')){
        await evaluate('window.scrollTo(0,0)');
        const {data}=await command('Page.captureScreenshot',{format:'png'});
        await writeFile(join(temp,`portfolio-${width}-${language}.png`),Buffer.from(data,'base64'));
      }
    }
  }
  const video=await evaluate(`(async()=>{const v=document.querySelector('video');await Promise.race([new Promise((ok,no)=>{if(v.readyState>=1)ok();else{v.addEventListener('loadedmetadata',ok,{once:true});v.addEventListener('error',()=>no(Error('Video decode error')),{once:true});}}),new Promise((_,no)=>setTimeout(()=>no(Error('Video metadata timeout')),10000))]);return {duration:v.duration,width:v.videoWidth,height:v.videoHeight,error:v.error?.message||null}})()`);
  assert.ok(video.duration>99&&video.duration<102);assert.equal(video.error,null);
  const playback=await evaluate(`(async()=>{const v=document.querySelector('video');v.muted=true;const start=v.currentTime;await v.play();await new Promise(ok=>setTimeout(ok,500));v.pause();return {advanced:v.currentTime>start,error:v.error?.message||null}})()`);
  assert.equal(playback.advanced,true);assert.equal(playback.error,null);
  const poster=await evaluate(`(async()=>{const v=document.querySelector('video');await Promise.race([new Promise(ok=>{v.addEventListener('seeked',ok,{once:true});v.currentTime=5;}),new Promise((_,no)=>setTimeout(()=>no(Error('Video seek timeout')),10000))]);const c=document.createElement('canvas');c.width=v.videoWidth;c.height=v.videoHeight;c.getContext('2d').drawImage(v,0,0);return c.toDataURL('image/jpeg',0.9).split(',')[1]})()`);
  if(!submission)await writeFile(join(root,'cakgo-demo-poster.jpg'),Buffer.from(poster,'base64'));
  const links=await evaluate(`(()=>{const ids=new Set([...document.querySelectorAll('[id]')].map(e=>e.id));return [...document.querySelectorAll('a')].map(a=>a.getAttribute('href')).filter(h=>!h||h==='#'||(h.startsWith('#')&&!ids.has(h.slice(1))));})()`);
  assert.deepEqual(links,[]);assert.deepEqual(errors,[]);
  assert.equal(await evaluate('document.querySelectorAll("#cardnews img").length'),5);
  assert.ok(await evaluate('Promise.race([Promise.all([...document.querySelectorAll("#cardnews img")].map(i=>{i.loading="eager";return i.decode()})).then(()=>true),new Promise((_,reject)=>setTimeout(()=>reject(Error("Gallery image decode timeout")),10000))])'));
  const source=await readFile(join(root,submission?'나즈미_인공지능학과_2024079443.html':'index.html'),'utf8');assert.ok(!source.includes('{{'));assert.ok(!source.includes('2024709443'));assert.ok(source.includes('href="https://github.com/Jeminana/SUARA-System"'));
  if(submission){
    assert.equal(await evaluate('location.protocol'),'file:');
    assert.ok(await evaluate(`(()=>{document.querySelector('[data-open-overview]').click();return document.getElementById('all-cards').open})()`));
    assert.equal(await evaluate('document.querySelectorAll(".embedded-grid img").length'),5);
    assert.ok(await evaluate('Promise.all([...document.querySelectorAll(".embedded-grid img")].map(i=>i.decode())).then(()=>true)'));
    assert.ok(await evaluate(`[...document.querySelectorAll('img,video source')].every(e=>e.src.startsWith('data:'))`));
    assert.ok(await evaluate(`[...document.querySelectorAll('[data-embedded-download],[data-embedded-video]')].every(e=>e.href.startsWith('data:'))`));
    assert.equal(await evaluate('document.querySelectorAll("link[rel=stylesheet]").length'),0);
    assert.ok(await evaluate('document.fonts.check(\'600 31px "Pretendard Variable"\')'));
    await command('Emulation.setDeviceMetricsOverride',{width:390,height:1000,deviceScaleFactor:1,mobile:true});
    assert.ok(await evaluate('document.documentElement.scrollWidth<=innerWidth'));
    console.log('Single HTML passed file:// tests with network disabled: font, cards, overview, downloads, language toggle, and video playback.');
  }
  await evaluate(`document.querySelector('[data-language="ko"]').click()`);
  await command('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
  await evaluate(`document.getElementById('case').scrollIntoView({behavior:'instant'})`);
  assert.ok(await evaluate(`document.getElementById('case-title').getBoundingClientRect().top<300`));
  const caseImage=await command('Page.captureScreenshot',{format:'png'});
  await writeFile(join(temp,'portfolio-case-ko.png'),Buffer.from(caseImage.data,'base64'));
  await evaluate(`document.getElementById('cardnews').scrollIntoView({behavior:'instant'})`);
  const galleryImage=await command('Page.captureScreenshot',{format:'png'});
  await writeFile(join(temp,'portfolio-cardnews-ko.png'),Buffer.from(galleryImage.data,'base64'));
  console.log(JSON.stringify({checks,video,playback,brokenLinks:links,scriptErrors:errors,screenshots:temp,poster:join(root,'cakgo-demo-poster.jpg')},null,2));
  }
}finally{ws?.close();chrome.kill();await new Promise(done=>server.close(done));}
