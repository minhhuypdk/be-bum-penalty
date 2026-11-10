const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const b=await chromium.launch({executablePath:require('./browser.cjs').executablePath,args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const p=await b.newPage({viewport:{width:390,height:844}}),errors=[];
  p.on('pageerror',e=>errors.push(e.message));
  await p.addInitScript(()=>{const Native=window.AudioContext;window.audioMetrics={contexts:0,tones:0};window.AudioContext=function(...args){audioMetrics.contexts++;const c=new Native(...args);audioMetrics.context=c;const make=c.createOscillator.bind(c);c.createOscillator=()=>{audioMetrics.tones++;return make()};return c};window.AudioContext.prototype=Native.prototype;});
  await p.route('**/supabase.min.js',r=>r.fulfill({body:'window.supabase=undefined;',contentType:'text/javascript'}));
  await p.goto(process.env.GAME_URL||'http://127.0.0.1:4180/');
  await p.evaluate(()=>document.querySelector('#game').classList.remove('hide'));
  assert.equal(await p.evaluate(()=>audioMetrics.contexts),0);
  await p.locator('#sound').click();
  await p.waitForFunction(()=>document.querySelector('#sound').dataset.audioState==='on'&&audioMetrics.context.state==='running');
  await p.evaluate(()=>window.dispatchEvent(new CustomEvent('penalty:state',{detail:{matchId:'audio-test',turn:0,stage:'result',shot:0,dive:1}})));
  await p.waitForTimeout(500);
  assert((await p.evaluate(()=>audioMetrics.tones))>=3);
  await p.locator('#sound-volume').fill('0');
  await p.locator('#sound').click();
  await p.waitForFunction(()=>audioMetrics.context.state==='suspended');
  const count=await p.evaluate(()=>audioMetrics.tones);await p.waitForTimeout(500);assert.equal(await p.evaluate(()=>audioMetrics.tones),count);
  assert.deepEqual(errors,[]);console.log('PASS: no autoplay/context before gesture, playback unlocks, goal effects, volume, mute suspends and stops music timer.');
 }finally{await b.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
