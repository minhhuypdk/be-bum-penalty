// Live integration test: creates a unique test room; retains it and releases owned roles.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { execFileSync } = require('node:child_process');
const base = process.env.GAME_URL || 'http://127.0.0.1:4173/';
const testRoom = `graphics-test-${Date.now()}`;
const realtimeOnly = process.env.REQUIRE_REALTIME === '1';
const errors = [];
const mock = process.env.MOCK_SUPABASE === '1';
let stored = null, created = false;
let browser, pages = [];
(async () => {
  browser = await chromium.launch({ executablePath: '/usr/bin/chromium', headless: true,
    args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
    proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY, bypass: '127.0.0.1,localhost' } : undefined });
  for (let i = 0; i < 2; i++) {
    const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
    if(realtimeOnly) await context.addInitScript(() => { const original = window.setInterval; window.setInterval = (fn, delay, ...args) => delay === 2500 ? 0 : original(fn, delay, ...args); });
    const page = await context.newPage(); pages.push(page);
    page.on('pageerror', e => errors.push(e.message));
    await page.route('**/supabase.min.js', r => r.fulfill({ contentType: 'text/javascript', body: fs.readFileSync('/tmp/bebum-supabase.min.js', 'utf8') + (mock ? `;const originalCreateClient=window.supabase.createClient;window.supabase.createClient=(...args)=>{const c=originalCreateClient(...args);c.channel=()=>{const channel={state:'mock',on:()=>channel,subscribe:()=>channel};return channel;};return c;};` : '') }));
    // Replace only the room constant in the fetched HTML, preserving all game code.
    await page.route(base, async r => {
      const response = await r.fetch();
      const html = await response.text();
      assert(html.includes("ROOM='ba-bum'"));
      await r.fulfill({ response, body: html.replace("ROOM='ba-bum'", `ROOM='${testRoom}'`) });
    });
    // curl uses the environment's trusted proxy for REST. Never permit another room.
    await page.route('**/rest/v1/bebum_penalty_rooms*', async r => {
      const req = r.request();
      const body = req.postData();
      assert(req.url().includes(encodeURIComponent(testRoom)) || body?.includes(testRoom), 'Refusing non-test room');
      if (mock) {
        let data;
        const method = req.method();
        if(method === 'POST') { stored = {...JSON.parse(body), version:0}; created = true; data = null; }
        else if(method === 'PATCH') {
          const expected = new globalThis.URL(req.url()).searchParams.get('version');
          if(stored && expected === `eq.${stored.version}`) { Object.assign(stored,JSON.parse(body)); data = [stored]; } else data = [];
        } else if(method === 'DELETE') { data = stored ? [{room_id:testRoom}] : []; stored = null; }
        else data = stored ? [stored] : [];
        if(req.headers().accept?.includes('vnd.pgrst.object')) data = Array.isArray(data) ? (data[0] || null) : data;
        return r.fulfill({status:200,contentType:'application/json',body:JSON.stringify(data)});
      }
      const args = ['-sS', '--max-time', '20', '-X', req.method(), req.url(), '-w', '\n%{http_code}'];
      for (const [k, v] of Object.entries(req.headers())) {
        if (['apikey', 'authorization', 'content-type', 'prefer', 'accept'].includes(k)) args.push('-H', `${k}: ${v}`);
      }
      if (body) args.push('--data-binary', body);
      const output = execFileSync('curl', args, { encoding: 'utf8' });
      const split = output.lastIndexOf('\n'); if (req.method() === 'POST' && Number(output.slice(split + 1)) < 300) created = true;
      await r.fulfill({ status: Number(output.slice(split + 1)), contentType: 'application/json', body: output.slice(0, split) });
    });
    await page.goto(base);
    await page.waitForFunction(() => typeof room !== 'undefined' && !!room, null, { timeout: 25000 });
  }
  const [ba, bum] = pages;
  if(realtimeOnly) for(const p of pages) await p.waitForFunction(() => channel?.state === 'joined');
  await ba.getByRole('button', { name: '👨 BA', exact: true }).click();
  await bum.getByRole('button', { name: '👦 BUM', exact: true }).click();
  for (const p of pages) {
    await p.waitForFunction(() => room?.state?.players.ba && room?.state?.players.bum);
    await p.waitForSelector('.goal[data-graphics="ready"]');
  }
  // Six turns: BA scores three, BUM is saved three times, exercising both roles.
  for (let turn = 0; turn < 6; turn++) {
    const shootPage = turn % 2 ? bum : ba, keepPage = turn % 2 ? ba : bum;
    await shootPage.locator('#directions button').nth(0).click();
    await keepPage.locator('#directions button').nth(turn % 2 ? 0 : 1).click();
    for (const p of pages) await p.waitForFunction(() => room?.state?.stage === 'result');
    const states = await Promise.all(pages.map(p => p.evaluate(() => room.state)));
    assert.deepEqual(states[0], states[1]);
    await ba.locator('#next').click();
    for (const p of pages) await p.waitForFunction(() => room?.state?.stage !== 'result');
  }
  for (const p of pages) assert.equal(await p.evaluate(() => room.state.winner), 'ba');
  assert.equal(await ba.evaluate(() => wallet), 130);
  await ba.reload();
  await ba.waitForSelector('#restart:not(.hide)');
  assert.equal(await ba.evaluate(() => wallet), 130, 'Reward must not repeat on reload');
  await ba.locator('#restart').click();
  for (const p of pages) await p.waitForFunction(() => room?.state?.stage === 'choose' && room.state.history.length === 0);
  await bum.getByRole('button', { name: '↩️ Đổi nhân vật' }).click();
  await ba.waitForFunction(() => !room.state.players.bum);
  const realtime = await Promise.all(pages.map(p => p.evaluate(() => channel?.state)));
  assert.deepEqual(errors, []);
  console.log(JSON.stringify({ result: 'PASS', base, testRoom, transport: mock ? 'mock REST with real Supabase SDK' : 'live Supabase', realtimeOnly, checks: ['two independent sessions', 'roles alternate', 'goal/save', 'scores synchronized', 'match winner', 'reward once after reload', 'restart', 'leave'], realtime, errors }));
})().catch(async e => { console.error(e, errors); if(pages[0]) console.error(await pages[0].locator('#status').textContent()); process.exitCode = 1; }).finally(async () => {
  if (pages[0] && created && mock) {
    try {
      const result = await pages[0].evaluate(async id => {
        const { error, data } = await client.from('bebum_penalty_rooms').delete().eq('room_id', id).select('room_id');
        return { error, deleted: data?.length };
      }, testRoom);
      console.log('Test room cleanup:', JSON.stringify(result));
    } catch (e) { console.error('Cleanup failed:', e.message); }
  }
  if(created && !mock) for(const p of pages) {
    try { await p.evaluate(async () => { const r=role; if(!r)return; role=null; await mutate(s=>{if(s.players[r]===token){s.players[r]=null;return true}return false}); }); } catch {}
  }
  if(created && !mock) console.log('Retained test row (no deletion):', testRoom);
  await browser?.close();
});
