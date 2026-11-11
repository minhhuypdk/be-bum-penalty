// Real CC-BY GLB integration: no fixtures, no live Supabase requests/writes.
const {chromium,webkit}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const engine=process.env.SHOWCASE_ENGINE||'chromium',out=process.env.ARTIFACT_DIR||'showcase/asset-review';fs.mkdirSync(out,{recursive:true});
const base=process.env.GAME_URL||'http://127.0.0.1:4180/';
async function render(page,name){const data=await page.evaluate(async()=>{const blob=await showcase.capture(false);return new Promise(r=>{const f=new FileReader();f.onload=()=>r(f.result.split(',')[1]);f.readAsDataURL(blob);});});fs.writeFileSync(path.join(out,name),Buffer.from(data,'base64'));}
(async()=>{
 const browser=engine==='webkit'?await webkit.launch({executablePath:process.env.WEBKIT_PATH,headless:true}):await chromium.launch({executablePath:require('./browser.cjs').executablePath,headless:true,args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const p=await browser.newPage({viewport:{width:1300,height:900}}),errors=[],requests=[];p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>requests.push(r.url()));
  await p.goto(new URL('graphics/showcase.html',base).href);await p.waitForSelector('body[data-ready=true]');await p.evaluate(()=>{showcase.setPaused(true);showcase.setAngle(.16);showcase.frame('face');});
  const before=await p.evaluate(()=>showcase.getView());await render(p,'baseline-face.png');
  await p.evaluate(()=>showcase.setVersion('snow','portrait'));await p.waitForTimeout(200);
  assert.equal((await p.evaluate(()=>showcase.getView())).angle,before.angle,'A/B preserves turntable angle');
  assert.equal(await p.locator('#review-version').inputValue(),'snow');assert((await p.locator('#character-name').innerText()).includes('SNOW'));
  assert.deepEqual((await p.evaluate(()=>showcase.getModelSummary())).available,['idle']);assert.equal(await p.locator('#pose option[value=kick]').isDisabled(),true);assert.equal(await p.locator('#pose option[value=save]').isDisabled(),true);
  assert((await p.evaluate(()=>showcase.getModelSummary())).geometryFinite);
  await render(p,'snow-portrait-face.png');await p.evaluate(()=>showcase.frame('body'));await p.waitForTimeout(100);await render(p,'snow-portrait-full.png');
  // Prove the actual skinned clip changes rendered pixels, rather than a label.
  await p.locator('#timeline').fill('0');await p.waitForTimeout(150);await render(p,'snow-idle-start.png');
  await p.locator('#timeline').fill('650');await p.waitForTimeout(150);await render(p,'snow-idle-motion.png');
  assert.notDeepEqual(fs.readFileSync(path.join(out,'snow-idle-start.png')),fs.readFileSync(path.join(out,'snow-idle-motion.png')),'real Idle skin animation must alter the render');
  const portrait=await p.evaluate(()=>showcase.getMetrics());
  await p.evaluate(()=>showcase.setVersion('snow','mobile'));await p.waitForTimeout(150);const mobile=await p.evaluate(()=>showcase.getMetrics());
  assert(mobile.triangles<portrait.triangles,'mobile must actually reduce geometry');
  await p.setViewportSize({width:390,height:844});await p.evaluate(()=>{showcase.frame('face');showcase.setAngle(0);});await p.waitForTimeout(200);assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await p.screenshot({path:path.join(out,'snow-mobile-ui.png'),fullPage:true});await render(p,'snow-mobile-face.png');
  await p.evaluate(()=>showcase.setVersion('baseline'));for(const id of ['ba-player','ba-keeper','bum-player','bum-keeper']){await p.evaluate(id=>showcase.selectCharacter(id),id);assert.equal((await p.evaluate(()=>showcase.getModelSummary())).source,'procedural');assert.equal((await p.evaluate(()=>showcase.getModelSummary())).available.length,5);}
  // Asset load races: selecting A while a B load is pending must leave A visible.
  await p.reload();await p.waitForSelector('body[data-ready=true]');await p.route('**/snow-review-portrait.glb',async route=>{await new Promise(r=>setTimeout(r,250));await route.continue();});
  await p.evaluate(async()=>{const loading=showcase.setVersion('snow');await showcase.setVersion('baseline');await loading;});assert.equal((await p.evaluate(()=>showcase.getView())).version,'baseline');
  // Failure must retain the prior active model, not relabel A as B.
  await p.unroute('**/snow-review-portrait.glb');await p.route('**/snow-review-portrait.glb',r=>r.fulfill({status:503,body:'test failure'}));
  const failed=await p.evaluate(async()=>{try{await showcase.setVersion('snow');return false}catch{return true}});assert(failed);assert.equal((await p.evaluate(()=>showcase.getView())).version,'baseline');assert.equal(await p.locator('#review-version').inputValue(),'baseline');
  assert(!requests.some(u=>u.includes('supabase')));assert.deepEqual(errors,[]);
  const report={engine,result:'PASS',portrait,mobile,noSupabaseRequests:true,realSkinClipVerified:true,preservedBaselineFour:true,raceAndFailureVerified:true,limitations:['Snow art-base candidate, not BA/BUM','Only minimal Idle head turn; no sports clips','Not physical iPhone performance evidence']};fs.writeFileSync(path.join(out,'asset-functional-'+engine+'.json'),JSON.stringify(report,null,2)+'\n');console.log(engine,'PASS: real licensed asset, A/B, both geometry LODs, actual skin animation, missing clips disabled, stale/failing load isolation, preserved four baselines, mobile UI, no Supabase.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
