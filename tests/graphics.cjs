const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const base = process.env.GAME_URL || 'http://127.0.0.1:4173/';
(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/chromium', headless: true, args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  // Deterministic room transport: never mutate the family's live Supabase room.
  await page.route('**/*supabase*', route => {
    if (route.request().url().includes('supabase.min.js')) return route.fulfill({ contentType: 'text/javascript', body: 'window.supabase = undefined;' });
    return route.abort();
  });
  await page.goto(base);
  await page.evaluate(() => document.querySelector('#game').classList.remove('hide'));
  await page.waitForSelector('.goal[data-graphics="ready"]');
  const presets = await page.evaluate(async base => {
    const { createCharacter, CHARACTER_PRESETS } = await import(new URL('graphics/characters.js', base).href);
    return Object.keys(CHARACTER_PRESETS).map(id => {
      const c = createCharacter(id);
      return { id, joints: Object.keys(c.userData.joints).length, children: c.children.length };
    });
  }, base);
  assert.equal(presets.length, 4);
  assert(presets.every(c => c.joints === 4 && c.children > 5));
  for (const turn of [0, 1]) for (let shot = 0; shot < 5; shot++) {
    await page.evaluate(({ turn, shot }) => window.dispatchEvent(new CustomEvent('penalty:state', { detail: { matchId: 1, turn: turn * 5 + shot, stage: 'result', shot, dive: shot } })), { turn, shot });
    await page.waitForTimeout(80);
  }
  await page.evaluate(() => window.dispatchEvent(new CustomEvent('penalty:state', { detail: { turn: 0, stage: 'choose' } })));
  await page.screenshot({ path: 'tests/graphics-mobile.png', fullPage: true });
  assert.equal(await page.locator('.goal canvas').count(), 1);
  assert.deepEqual(errors, []);
  console.log('PASS: four articulated characters, both roles, five directions, mobile WebGL; no page errors. Supabase writes blocked.');
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
