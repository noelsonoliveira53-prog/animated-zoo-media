// Touch rally drag (740×360 phone, real touch events over CDP): builds a Burrow Den, enters rally mode, drags the
// ghost flag onto the road inside the circle (screenshot mid-drag) and lifts: the flag is planted on the road.
// Then a drag out of reach keeps rally mode so the player can try again. `node scripts/rallydrag-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'rallydrag';
const server = await preview({ preview: { port: 4355, strictPort: true } });
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const cdp = await ctx.newCDPSession(page);
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4355/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const toPage = (p) => page.evaluate((q) => { const r = window.__game.canvas.getBoundingClientRect(); return { x: r.left + (q.x * r.width) / 1280, y: r.top + (q.y * r.height) / 720 }; }, p);
const touch = async (type, p) => { const q = p ? await toPage(p) : null; await cdp.send('Input.dispatchTouchEvent', { type, touchPoints: q ? [{ x: q.x, y: q.y }] : [] }); };
const frames = async (ms) => { const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now); await page.waitForFunction(([t, d]) => window.__game.scene.getScene('Battle').time.now > t + d, [t0, ms], { timeout: 20000, polling: 'raf' }); };
// a Burrow Den, and a road spot inside its reach (plus one far outside it)
const setup = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 20000;
  for (let slot = 0; slot < s.level.slots.length; slot++) {
    const t = s.sim.build(slot, 'burrow');
    if (!t) continue;
    const range = s.sim.stats(t).range;
    let good = null, far = null;
    for (const path of s.sim.paths) for (let d = 0; d < path.length; d += 10) {
      const q = path.pointAt(d);
      const r = Math.hypot(q.x - t.pos.x, q.y - t.pos.y);
      if (!good && r < range * 0.8 && Math.hypot(q.x - t.rally.x, q.y - t.rally.y) > 40 && q.y > 140 && q.y < 560) good = q;
      if (!far && r > range * 1.5 && r < range * 3 && q.y > 140 && q.y < 560) far = q;
    }
    if (good && far) {
      s.rallyMode = slot;
      s.drawRange(t.pos, range, t.def.color);
      return { slot, good, far, before: { ...t.rally } };
    }
    s.sim.sell(slot);
  }
  return null;
});
if (!setup) throw new Error('no slot with a road spot in reach');
await page.evaluate((k) => { window.__slot = k; }, setup.slot);
// press a little off the road, below the spot (the flag floats 60 px above the finger), drag onto it
await touch('touchStart', { x: setup.good.x + 30, y: setup.good.y + 60 + 20 });
await frames(150);
await touch('touchMove', { x: setup.good.x + 8, y: setup.good.y + 60 + 10 });
await frames(300);
const mid = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { ghost: !!s.rallyGhost?.visible, drag: s.rallyDrag }; });
await page.screenshot({ path: `screenshots/${name}.png` });
await touch('touchEnd');
await frames(200);
const planted = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); const t = s.sim.towers[window.__slot]; const onRoad = s.sim.paths.some((p) => p.distanceTo(t.rally) < 1); return { rally: [Math.round(t.rally.x), Math.round(t.rally.y)], onRoad, mode: s.rallyMode }; });
// out of reach: rally mode stays on
await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); const t = s.sim.towers[window.__slot]; s.rallyMode = window.__slot; s.drawRange(t.pos, s.sim.stats(t).range, t.def.color); });
await touch('touchStart', { x: setup.far.x, y: setup.far.y + 60 });
await frames(150);
await touch('touchEnd');
await frames(200);
const missed = await page.evaluate(() => window.__game.scene.getScene('Battle').rallyMode === window.__slot);
const ok = mid.ghost && mid.drag && planted.onRoad && planted.mode === null && missed && (planted.rally[0] !== Math.round(setup.before.x) || planted.rally[1] !== Math.round(setup.before.y));
console.log(JSON.stringify({ mid, planted, missed, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
