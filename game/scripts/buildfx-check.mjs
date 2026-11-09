// Build/upgrade juice check: builds on one pad, upgrades a second, specializes a third, then screenshots mid-effect
// with tweens paused. `node scripts/buildfx-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'buildfx';
const server = await preview({ preview: { port: 4329, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4329/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
// pre-build the towers that will be upgraded, and let their pop-in finish
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 99999;
  s.sim.build(1, 'glimmer');
  s.sim.build(2, 'boulder');
  s.sim.upgrade(2);
  s.sim.upgrade(2);
});
await page.waitForTimeout(2500);
const r = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const built = !!s.sim.build(0, 'thornbow');
  const up = s.sim.upgrade(1);
  const spec = s.sim.specialize(2, 0);
  return { built, up, spec, t0: s.time.now };
});
// headless frames are slow and uneven: poll the scene clock and pause as soon as ~0.25 s of animation has played
await page.waitForFunction((t0) => window.__game.scene.getScene('Battle').time.now >= t0 + 250, r.t0, { timeout: 20000, polling: 'raf' });
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.pauseAll());
await page.waitForTimeout(40);
await page.screenshot({ path: `screenshots/${name}.png` });
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.resumeAll());
await page.waitForTimeout(3000);
r.leftoverText = await page.evaluate(() => window.__game.scene.getScene('Battle').children.list.filter((o) => o.depth === 3050).length);
console.log(JSON.stringify(r));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !r.built || !r.up || !r.spec ? 1 : 0);
