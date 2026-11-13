// Real GLB rendering in isolated checkout. No game/DB integration.
const {chromium,webkit}=require('playwright'),fs=require('fs'),path=require('path'),assert=require('node:assert/strict'),crypto=require('crypto'),http=require('http');
const root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]),engine=process.argv[4]||'chromium';fs.mkdirSync(out,{recursive:true});
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const server=http.createServer((req,res)=>{let f;try{f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));}catch{res.writeHead(400).end();return;}if(!f.startsWith(root+path.sep)){res.writeHead(403).end();return;}fs.readFile(f,(e,b)=>{if(e){res.writeHead(404).end();return;}res.writeHead(200,{'content-type':({'.js':'text/javascript','.html':'text/html','.css':'text/css','.glb':'model/gltf-binary','.png':'image/png'}[path.extname(f)]||'application/octet-stream')});res.end(b);});});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;try{
browser=await ({chromium,webkit}[engine]).launch({headless:true,...(engine==='chromium'?{...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{}),args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']}:(process.env.WEBKIT_PATH?{executablePath:process.env.WEBKIT_PATH}:{}))});
const p=await browser.newPage({viewport:{width:1500,height:1100},deviceScaleFactor:1}),errors=[],requests=[],shots=[],views={};p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>requests.push(r.url()));
await p.goto('http://127.0.0.1:'+server.address().port+'/graphics/showcase.html');await p.waitForSelector('body[data-ready=true]',{timeout:90000});await p.evaluate(()=>{showcase.setPaused(true);showcase.selectCharacter('bum-player');});
const inputs=['graphics/models/bum07/bum07-study-portrait.glb','graphics/models/p2-original.glb','graphics/models/bum07-p31/bum07-p31-experimental.glb'];const hashes=Object.fromEntries(inputs.map(f=>[f,hash(path.join(root,f))]));
async function capture(file){const data=await p.evaluate(async()=>{const b=await showcase.capture(false);return new Promise(r=>{const f=new FileReader();f.onload=()=>r(f.result.split(',')[1]);f.readAsDataURL(b);});});fs.writeFileSync(path.join(out,file),Buffer.from(data,'base64'));return hash(path.join(out,file));}
for(const [idx,variant]of ['C','P2','P3.1'].entries()){
console.log(engine,'rendering',variant);
if(idx===0)await p.evaluate(()=>showcase.setVersion('bum07','portrait'));else await p.evaluate(async url=>{const r=await fetch(url);if(!r.ok)throw Error(url);await showcase.importGLB(new File([await r.blob()],url.split('/').pop()));},'./models/'+(idx===1?'p2-original.glb':'bum07-p31/bum07-p31-experimental.glb'));
await p.evaluate(()=>{showcase.setPaused(true);showcase.setAction('idle');});
for(const s of [{id:'front',angle:0},{id:'45',angle:45},{id:'profile',angle:90},{id:'close',angle:0,close:true}]){
await p.evaluate(s=>{showcase.frame('face');showcase.setReviewAngle(s.angle*Math.PI/180);},s);if(s.close)await p.locator('#zoom-in').click();
if(idx===0)views[s.id]=await p.evaluate(()=>showcase.getView());else await p.evaluate(v=>showcase.setMatchedView(v),views[s.id]);await p.waitForTimeout(180);
const v=await p.evaluate(()=>showcase.getView());for(const k of ['camera','target'])assert(v[k].every((x,i)=>Math.abs(x-views[s.id][k][i])<1e-6),'matched camera drift');
const file=variant.toLowerCase().replace('.','')+'-'+s.id+'.png';shots.push({variant,...s,file,sha256:await capture(file),view:v,metrics:await p.evaluate(()=>showcase.getMetrics())});}
}
const targets=await p.evaluate(()=>showcase.getStudyTargets());assert(targets.length>=5);assert(targets.every(x=>x.finite));
for(const mode of ['Blink','Smile'])for(const v of [0,.5,1]){await p.evaluate(({mode,v})=>showcase.setStudyExpression(mode,v),{mode,v});await p.waitForTimeout(100);await capture('p31-'+mode.toLowerCase()+'-'+v+'.png');}
await p.evaluate(()=>showcase.setStudyExpression('none'));
const motion=[];
for(const action of ['idle','run','kick','celebrate']){await p.evaluate(a=>showcase.setAction(a),action);await p.locator('#timeline').fill('500');await p.evaluate(()=>{showcase.frame('body');showcase.setReviewAngle(Math.PI/4);});await p.waitForTimeout(100);motion.push({action,file:'p31-motion-'+action+'.png',sha256:await capture('p31-motion-'+action+'.png'),metrics:await p.evaluate(()=>showcase.getMetrics())});}
await p.setViewportSize({width:390,height:844});await p.evaluate(()=>{showcase.setAction('idle');showcase.frame('face');});await p.waitForTimeout(200);await p.screenshot({path:path.join(out,'p31-mobile-layout.png'),fullPage:true});
assert.deepEqual(errors,[]);assert(!requests.some(u=>/supabase/i.test(u)));for(const[f,h]of Object.entries(hashes))assert.equal(hash(path.join(root,f)),h);
const report={result:'PASS',engine,physicalIPhone:false,artApproved:false,quality9Verified:false,scope:'Actual GLB import/render; matched camera and studio; morph and existing action playback. Does not certify collision-free anatomy or iPhone performance.',sourceHashes:hashes,shots,motion,targets,errors,noSupabaseRequests:true};fs.writeFileSync(path.join(out,'browser-report.json'),JSON.stringify(report,null,2));console.log(engine,'PASS real C/P2/P3.1 GLB views + expressions + original action playback; no art approval');
}finally{if(browser)await browser.close();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
