const {chromium}=require('playwright');
const fs=require('node:fs');
const {execFileSync}=require('node:child_process');
const assert=require('node:assert/strict');
exports.openHarness=async function(base){
 const id=`session-test-${Date.now()}`,pages=[],contexts=[],errors=[];
 let failWrite=false,created=false;
 const browser=await chromium.launch({executablePath:require('./browser.cjs').executablePath,headless:true,args:['--no-sandbox'],proxy:process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY,bypass:'127.0.0.1,localhost'}:undefined});
 async function open(storageState){
  const context=await browser.newContext({viewport:{width:390,height:844},storageState});contexts.push(context);
  await context.addInitScript(()=>{const real=window.setInterval;window.setInterval=(fn,ms,...rest)=>ms===2500?0:real(fn,ms,...rest)});
  const p=await context.newPage();pages.push(p);p.on('pageerror',e=>errors.push(e.message));p.on('dialog',d=>d.dismiss());
  await p.route('**/supabase.min.js',r=>r.fulfill({contentType:'text/javascript',body:fs.readFileSync(process.env.SUPABASE_SDK||'/tmp/bebum-supabase.min.js','utf8')}));
  await p.route('**/graphics/scene.js',r=>r.fulfill({contentType:'text/javascript',body:''}));
  await p.route(base,async r=>{const response=await r.fetch(),html=await response.text();assert(html.includes("ROOM='ba-bum'"));await r.fulfill({response,body:html.replace("ROOM='ba-bum'",`ROOM='${id}'`)});});
  await p.route('**/rest/v1/bebum_penalty_rooms*',async r=>{
   const req=r.request(),body=req.postData();
   const filter=new URL(req.url()).searchParams.get('room_id');
   assert(filter===`eq.${id}`||(req.method()==='POST'&&JSON.parse(body).room_id===id),'Refusing access outside isolated test room');
   assert.notEqual(req.method(),'DELETE','No live deletion');
   if(req.method()==='PATCH'&&failWrite){failWrite=false;return r.abort('internetdisconnected')}
   const args=['-sS','--max-time','20','-X',req.method(),req.url(),'-w','\n%{http_code}'];
   for(const[k,v]of Object.entries(req.headers()))if(['apikey','authorization','content-type','prefer','accept'].includes(k))args.push('-H',`${k}: ${v}`);
   if(body)args.push('--data-binary',body);
   const out=execFileSync('curl',args,{encoding:'utf8'}),split=out.lastIndexOf('\n'),code=Number(out.slice(split+1));
   if(req.method()==='POST'&&code<300)created=true;
   await r.fulfill({status:code,contentType:'application/json',body:out.slice(0,split)});
  });
  await p.goto(base,{waitUntil:'domcontentloaded',timeout:60000});
  await p.waitForFunction(()=>typeof room!=='undefined'&&!!room&&channel?.state==='joined');
  return p;
 }
 return {id,pages,errors,open,failNextWrite(){failWrite=true},async close(){
  for(const p of pages)if(!p.isClosed())try{await p.evaluate(async()=>{const r=role;if(!r)return;await mutate(s=>{if(s.players[r]!==token)return false;s.players[r]=null;return true});});}catch{}
  await browser.close();if(created)console.log('Retained isolated room:',id);
 }};
};
