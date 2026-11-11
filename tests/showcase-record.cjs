// Capture the actual running browser, not a generated movie or an FPS claim.
const {webkit}=require('playwright'),fs=require('node:fs'),path=require('node:path');
(async()=>{
 const bum=process.env.SHOWCASE_ASSET==='bum07',out=path.resolve(bum?'showcase/bum07-review':'showcase/asset-review');fs.mkdirSync(out,{recursive:true});
 const browser=await webkit.launch({executablePath:process.env.WEBKIT_PATH,headless:true});
 try{
  const context=await browser.newContext({viewport:{width:1100,height:820},recordVideo:{dir:path.join(out,'recording'),size:{width:1100,height:820}}}),p=await context.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto((process.env.GAME_URL||'http://127.0.0.1:4180/')+'graphics/showcase.html');await p.waitForSelector('body[data-ready=true]');await p.evaluate(bum=>showcase.setVersion(bum?'bum07':'snow','mobile'),bum);await p.evaluate(()=>{showcase.setPaused(false);showcase.frame('face');});
  const start=new Date().toISOString();if(bum){await p.evaluate(()=>showcase.frame('body'));for(const action of ['idle','run','kick','celebrate']){await p.evaluate(action=>showcase.setAction(action),action);await p.waitForTimeout(3300);}}else{await p.waitForTimeout(8500);await p.evaluate(()=>{showcase.frame('body');});await p.waitForTimeout(4000);}
  const metrics=await p.evaluate(()=>showcase.getMetrics());const video=p.video();await context.close();await video.saveAs(path.join(out,bum?'bum07-motion-studies.webm':'snow-idle-runtime.webm'));await video.delete();
  fs.writeFileSync(path.join(out,'motion-recording.json'),JSON.stringify({capturedAt:start,engine:'Playwright WebKit on Linux',actualRunningBrowser:true,notPhysicalIPhone:true,content:bum?'Four actual FK studies of original BUM07 GLB; NOT final sports animation':'Mobile LOD standing / slight head-turn Idle; face and body camera views; no sports clips',metrics,errors,note:'Video includes startup and camera changes. Its playback frame rate is not game render FPS; use the separate measured FPS report.'},null,2)+'\n');if(errors.length)throw new Error(errors.join('\n'));console.log('Saved actual WebKit runtime video; not physical iPhone evidence.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
