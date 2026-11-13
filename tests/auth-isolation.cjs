const {chromium}=require('playwright');
const fs=require('node:fs');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:require('./browser.cjs').executablePath,headless:true,args:['--no-sandbox']});
 try{
  const context=await browser.newContext();
  const fixtureToken='eyJhbGciOiJIUzI1NiJ9.'+Buffer.from(JSON.stringify({role:'authenticated',exp:4102444800})).toString('base64url')+'.testSignature';
  const session=JSON.stringify({access_token:fixtureToken,refresh_token:'fixture-refresh',expires_at:4102444800,token_type:'bearer',user:{id:'00000000-0000-4000-8000-000000000001',aud:'authenticated',role:'authenticated'}});
  await context.addInitScript(session=>localStorage.setItem('sb-zzphvbedtxbhajkpavqp-auth-token',session),session);
  await context.routeWebSocket('**',socket=>socket.close());
  const page=await context.newPage(),requests=[],errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/supabase.min.js',r=>r.fulfill({contentType:'text/javascript',body:fs.readFileSync(process.env.SUPABASE_SDK||'/tmp/bebum-supabase.min.js','utf8')}));
  await page.route('**/graphics/scene.js',r=>r.fulfill({contentType:'text/javascript',body:''}));
  await page.route('https://zzphvbedtxbhajkpavqp.supabase.co/**',r=>{
   const req=r.request(),auth=req.headers().authorization;
   requests.push({method:req.method(),isPublishable:auth?.startsWith('Bearer sb_publishable_'),usesStored:auth==='Bearer '+fixtureToken,url:req.url()});
   return r.fulfill({status:auth==='Bearer '+fixtureToken?403:200,contentType:'application/json',body:JSON.stringify(auth==='Bearer '+fixtureToken?{code:'42501',message:'permission denied for table bebum_penalty_rooms'}:[{room_id:'ba-bum',version:0,state:{players:{ba:null,bum:null},stage:'choose',turn:0,score:{ba:0,bum:0},history:[]}}])});
  });
  await page.goto(process.env.GAME_URL||'http://127.0.0.1:4180/',{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>room?.state?.players);
  assert(requests.length>0&&requests.every(r=>r.method==='GET'&&r.isPublishable&&!r.usesStored));
  assert.equal(await page.evaluate(()=>localStorage.getItem('sb-zzphvbedtxbhajkpavqp-auth-token')),session);
  assert.equal(await page.evaluate(async()=>!!(await client.auth.getSession()).data.session),false);
  assert.deepEqual(errors,[]);
  console.log('PASS: account-free game ignores saved authenticated JWT, uses publishable credentials, does not refresh/sign out/delete the existing session.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
