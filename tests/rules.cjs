const { chromium } = require('playwright');
const assert = require('node:assert/strict');
(async () => {
  const browser = await chromium.launch({ executablePath:'/usr/bin/chromium', headless:true, args:['--no-sandbox'] });
  try {
    const page = await browser.newPage();
    await page.route('**/supabase.min.js', r => r.fulfill({body:'window.supabase=undefined;',contentType:'text/javascript'}));
    await page.route('**/graphics/scene.js', r => r.fulfill({body:'',contentType:'text/javascript'}));
    await page.goto('http://127.0.0.1:4173/');
    const result = await page.evaluate(async () => {
      const make = (a,b,score) => ({ history:[...Array.from({length:a},()=>({by:'ba'})),...Array.from({length:b},()=>({by:'bum'}))],score });
      const winners = [
        getWinner(make(3,3,{ba:3,bum:0})),
        getWinner(make(5,5,{ba:3,bum:3})),
        getWinner(make(6,5,{ba:4,bum:3})),
        getWinner(make(6,6,{ba:4,bum:3})),
        getWinner(make(6,6,{ba:4,bum:4})),
        getWinner(make(7,7,{ba:4,bum:5})),
      ];
      room={version:20,state:initial()};
      const staleAccepted = acceptRoom({version:19,state:{...initial(),turn:9}});
      const version = room.version;
      const originalMutate = mutate;
      role='ba';
      const state = initial(); state.players={ba:token,bum:'other'};
      mutate=async fn=>fn(state);
      const rejected = [];
      for(const n of [-1,5,1.5,'0',null]) { await choose(n); rejected.push(state.shot===null); }
      state.players.ba='different-session'; await choose(0); rejected.push(state.shot===null);
      state.players.ba=token; await choose(0); const validShot=state.shot;
      await choose(1); const repeatedShot=state.shot;
      mutate=originalMutate;
      return {winners,staleAccepted,version,rejected,validShot,repeatedShot};
    });
    assert.deepEqual(result.winners,['ba',null,null,'ba',null,'bum']);
    assert.equal(result.staleAccepted,false); assert.equal(result.version,20);
    assert(result.rejected.every(Boolean)); assert.equal(result.validShot,0); assert.equal(result.repeatedShot,0);
    console.log('PASS: regulation/sudden-death fairness, stale room rejection, invalid/duplicate choices and session ownership.');
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
