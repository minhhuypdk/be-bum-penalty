const{chromium,webkit}=require('playwright');
const engine=process.env.SHOWCASE_ENGINE||'chromium';
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const base=process.env.GAME_URL||'http://127.0.0.1:4180/';
const out=process.env.ARTIFACT_DIR||'showcase/renders';fs.mkdirSync(out,{recursive:true});
function fixtureGLB(external=false){
 const bin=Buffer.alloc(68);new Float32Array(bin.buffer,bin.byteOffset,17).set([-.5,0,0,.5,0,0,0,1,0,0,1,0,0,0,0,.1,0]);
 const animation=name=>({name,samplers:[{input:1,output:2}],channels:[{sampler:0,target:{node:0,path:'translation'}}]});
 const json={asset:{version:'2.0'},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0,name:'test-fixture'}],meshes:[{primitives:[{attributes:{POSITION:0}}]}],buffers:[{byteLength:68}],bufferViews:[{buffer:0,byteOffset:0,byteLength:36},{buffer:0,byteOffset:36,byteLength:8},{buffer:0,byteOffset:44,byteLength:24}],accessors:[{bufferView:0,componentType:5126,count:3,type:'VEC3',min:[-.5,0,0],max:[.5,1,0]},{bufferView:1,componentType:5126,count:2,type:'SCALAR',min:[0],max:[1]},{bufferView:2,componentType:5126,count:2,type:'VEC3'}],animations:['Idle','Run','Kick','Dive','Celebrate'].map(animation)};
 if(external)json.images=[{uri:'https://example.com/not-allowed.png'}];
 let text=JSON.stringify(json);while(Buffer.byteLength(text)%4)text+=' ';const data=Buffer.from(text),buffer=Buffer.alloc(12+8+data.length+8+bin.length);
 buffer.writeUInt32LE(0x46546c67,0);buffer.writeUInt32LE(2,4);buffer.writeUInt32LE(buffer.length,8);buffer.writeUInt32LE(data.length,12);buffer.writeUInt32LE(0x4e4f534a,16);data.copy(buffer,20);const offset=20+data.length;buffer.writeUInt32LE(bin.length,offset);buffer.writeUInt32LE(0x004e4942,offset+4);bin.copy(buffer,offset+8);return buffer;
}
async function exportCanvas(page,file){const encoded=await page.evaluate(async()=>{const blob=await window.showcase.capture(false);return await new Promise(resolve=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result.split(',')[1]);reader.readAsDataURL(blob)})});fs.writeFileSync(file,Buffer.from(encoded,'base64'));}
(async()=>{
 const browser=engine==='webkit'?await webkit.launch({executablePath:process.env.WEBKIT_PATH,headless:true}):await chromium.launch({executablePath:require('./browser.cjs').executablePath,headless:true,args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const p=await browser.newPage({viewport:{width:1300,height:900}}),errors=[],requests=[];p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>requests.push(r.url()));
  await p.goto(new URL('graphics/showcase.html',base).href);await p.waitForSelector('body[data-ready=true]',{timeout:60000});await p.evaluate(()=>showcase.setPaused(true));
  const results=[];
  for(const id of ['ba-player','ba-keeper','bum-player','bum-keeper']){
   await p.locator(`[data-character="${id}"]`).click();await p.evaluate(()=>{showcase.setAngle(0);showcase.frame('body')});
   for(const action of ['idle','run','kick','save','celebrate']){
    await p.selectOption('#pose',action);await p.locator('#timeline').fill(action==='save'?'410':'400');await p.waitForTimeout(110);
    const summary=await p.evaluate(()=>showcase.getModelSummary());assert(summary.geometryFinite);assert(summary.position.every(Number.isFinite));assert(summary.rotation.every(Number.isFinite));assert.equal(summary.available.length,5);results.push({id,action,summary});
   }
   await p.selectOption('#pose','idle');await p.locator('#timeline').fill('250');await p.waitForTimeout(120);await exportCanvas(p,path.join(out,`${id}-full.png`));
   await p.locator('#face').click();await p.waitForTimeout(120);await exportCanvas(p,path.join(out,`${id}-face.png`));
   if(process.env.GENERATE_SHOWCASE_THUMBS==='1'){fs.mkdirSync('graphics/showcase-assets',{recursive:true});await exportCanvas(p,`graphics/showcase-assets/${id}.png`);}
  }
  await p.locator('#full-body').click();const before=await p.evaluate(()=>showcase.getMetrics());await p.locator('#zoom-in').click();await p.locator('#zoom-out').click();
  await p.locator('#rotate').click();assert.equal(await p.locator('#rotate').getAttribute('aria-pressed'),'true');await p.locator('#rotate').click();
  await p.locator('#asset-open').click();await p.locator('#asset-file').setInputFiles({name:'animation-fixture.glb',mimeType:'model/gltf-binary',buffer:fixtureGLB()});
  await p.waitForFunction(()=>showcase.getModelSummary().source==='glb');assert.equal((await p.evaluate(()=>showcase.getModelSummary())).available.length,5);
  await p.locator('#asset-file').setInputFiles({name:'external-not-allowed.glb',mimeType:'model/gltf-binary',buffer:fixtureGLB(true)});await p.waitForFunction(()=>document.querySelector('#asset-status').textContent.includes('không cho phép URL'));
  await p.locator('#asset-reset').click();await p.locator('[data-close="asset-dialog"]').click();assert.equal((await p.evaluate(()=>showcase.getModelSummary())).source,'procedural');
  await p.reload({waitUntil:'domcontentloaded'});await p.waitForSelector('body[data-ready=true]');await p.evaluate(()=>showcase.setPaused(true));
  await p.waitForFunction(()=>document.querySelectorAll('.portrait img').length===4);
  await p.setViewportSize({width:390,height:844});await p.waitForTimeout(250);assert(await p.locator('#face').isVisible());assert(await p.locator('#pose').isVisible());
  assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await p.screenshot({path:path.join(out,'showcase-mobile.png'),fullPage:true});
  await p.setViewportSize({width:1300,height:900});await p.evaluate(()=>{showcase.selectCharacter('ba-player');showcase.frame('body');showcase.setPaused(true)});await p.waitForTimeout(200);await p.screenshot({path:path.join(out,'showcase-desktop.png')});
  assert(!requests.some(u=>u.includes('supabase')),'Showcase must not access Supabase');assert.deepEqual(errors,[]);
  fs.writeFileSync(path.join(out,'showcase-functional-report.json'),JSON.stringify({result:'PASS',cases:results,metrics:before,noSupabaseRequests:true},null,2));
  console.log(engine,'PASS: four characters × five motions, 360 controls, face/body zoom, timeline, GLB clips/import isolation, mobile layout, PNG render export; no Supabase requests or page errors.');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
