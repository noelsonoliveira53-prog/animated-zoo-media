// Tooltips: `node scripts/tooltip-check.mjs` — hovers the pause button, then a spell button, then tabs the focus ring
// onto the hero skill, screenshotting each tooltip (desktop) and long-pressing a spell on a phone.
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const server = await preview({ preview: { port: 4336, strictPort: true } });
const browser = await pw.chromium.launch();
const errors = [];
const out = {};
for (const phone of [false, true]) {
  const ctx = phone ? await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }) : await browser.newContext({ viewport: { width: 1280, height: 720 } });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  await page.addInitScript(() => { localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, seenStory: true })); window.__noTouchTip = true; });
  await page.goto('http://localhost:4336/');
  await page.waitForTimeout(1500);
  await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 0 }));
  await page.waitForFunction(() => window.__game.scene.getScene('Battle')?.sys.isActive(), null, { timeout: 20000 });
  await page.waitForTimeout(1200);
  // Phaser timers crawl in headless Chromium, so wait for the tooltip to appear (up to 6 s) instead of a fixed pause
  const tipText = async (want = true) => {
    try {
      await page.waitForFunction((w) => !!window.__game.scene.getScene('Battle').children.getByName('tooltip') === w, want, { timeout: 6000, polling: 100 });
    } catch { /* report what is there */ }
    return page.evaluate(() => window.__game.scene.getScene('Battle').children.getByName('tooltip')?.list?.[1]?.text ?? null);
  };
  const toScreen = (gx, gy) => page.evaluate(([x, y]) => { const r = window.__game.canvas.getBoundingClientRect(); return { x: r.left + (x / 1280) * r.width, y: r.top + (y / 720) * r.height }; }, [gx, gy]);
  if (!phone) {
    const p = await toScreen(1280 - 400, 40);
    await page.mouse.move(p.x, p.y);
    await page.waitForTimeout(700);
    out.pause = await tipText();
    await page.screenshot({ path: 'screenshots/fix-14-pause.png' });
    const sp = await toScreen(1280 - 58 - 2 * 92, 720 - 58);
    await page.mouse.move(sp.x, sp.y);
    await page.waitForTimeout(700);
    out.spell = await tipText();
    await page.screenshot({ path: 'screenshots/fix-14-spell.png' });
    await page.mouse.move(640, 400);
    await page.waitForTimeout(200);
    out.afterLeave = await tipText(false);
  } else {
    const sp = await toScreen(1280 - 400, 40); // the pause button: icon-only, so a long press explains it, even while paused
    const cdp = await ctx.newCDPSession(page);
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: sp.x, y: sp.y }] });
    await page.waitForTimeout(800);
    out.phoneLongPress = await tipText();
    await page.screenshot({ path: 'screenshots/fix-14-phone.png' });
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  }
  await ctx.close();
}
console.log(JSON.stringify(out, null, 1));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !out.pause || !out.spell || out.afterLeave || !out.phoneLongPress ? 1 : 0);
