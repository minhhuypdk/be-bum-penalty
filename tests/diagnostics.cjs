const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fixtureToken='eyJhbGciOiJIUzI1NiJ9.'+Buffer.from(JSON.stringify({role:'authenticated',exp:4102444800})).toString('base64url')+'.testSignature';
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
 try{
  for(const hasSession of [false,true]){
   const context=await browser.newContext();
   if(hasSession)await context.addInitScript(token=>localStorage.setItem('sb-zzphvbedtxbhajkpavqp-auth-token',JSON.stringify({access_token:token,refresh_token:'DO_NOT_PRINT_REFRESH'})),fixtureToken);
   const page=await context.newPage(),errors=[],methods=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.route('https://zzphvbedtxbhajkpavqp.supabase.co/**',async route=>{
    const req=route.request();methods.push(req.method());
    const stored=req.headers().authorization==='Bearer '+fixtureToken;
    return route.fulfill({status:stored?403:200,contentType:'application/json',body:JSON.stringify(stored?{code:'42501',message:'permission denied for table bebum_penalty_rooms',details:fixtureToken,hint:'Grant SELECT to authenticated'}:[{room_id:'ba-bum',state:{players:{ba:'DO_NOT_PRINT_PLAYER'}}}])});
   });
   await page.goto(new URL('diagnostics.html',process.env.GAME_URL||'http://127.0.0.1:4182/').href);
   await page.waitForSelector('#copy:not([disabled])');
   const text=await page.locator('#report').textContent(),report=JSON.parse(text);
   assert.equal(report.projectRef,'zzphvbedtxbhajkpavqp');
   assert.equal(report.keySha256,'48bf5efc37765edc42c34a4ebbe200510a4ea4e9ec8d7096aa6b232d15300ec5');
   assert.equal(report.hasStoredAccessToken,hasSession);assert.equal(report.requests[0].httpStatus,200);
   if(hasSession){assert.equal(report.requests[1].declaredJwtRole,'authenticated');assert.equal(report.requests[1].httpStatus,403);assert.equal(report.requests[1].error.code,'42501');assert.equal(report.requests[1].error.details,'[JWT redacted]');}
   assert(!text.includes(fixtureToken));assert(!text.includes('DO_NOT_PRINT'));assert(methods.every(m=>m==='GET'));assert.deepEqual(errors,[]);
   await context.close();
  }
  console.log('PASS: read-only diagnostics, deployed config fingerprint, fresh/cached credentials, detailed 42501 errors, JWT/refresh/player-data redaction; no database writes.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
