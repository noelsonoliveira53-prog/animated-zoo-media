// Tower idle life: builds one of each tower, waits for a burrow critter to peek, pauses and screenshots a close-up.
// `node scripts/idle-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'idle';
const server = await preview({ preview: { port: 4332, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4332/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const pads = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 9999;
  ['thornbow', 'glimmer', 'boulder', 'burrow'].forEach((k, i) => s.sim.build(i, k));
  return s.sim.level.slots.slice(0, 4).map((p) => ({ x: p.x, y: p.y }));
});
// wait for a peek in progress (critter container scaled up)
await page.waitForFunction(() => window.__game.scene.getScene('Battle').children.list.some((o) => o.type === 'Container' && o.list?.length === 5 && o.scaleY > 0.8), null, { timeout: 30000, polling: 'raf' });
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.pauseAll());
await page.waitForTimeout(60);
const xs = pads.map((p) => p.x), ys = pads.map((p) => p.y);
const clip = { x: Math.max(0, Math.min(...xs) - 70), y: Math.max(0, Math.min(...ys) - 110), width: 0, height: 0 };
clip.width = Math.min(1280 - clip.x, Math.max(...xs) - clip.x + 70);
clip.height = Math.min(720 - clip.y, Math.max(...ys) - clip.y + 50);
await page.screenshot({ path: `screenshots/${name}.png`, clip });
const flips = await page.evaluate(() => window.__game.scene.getScene('Battle').towerViews.filter(Boolean).map((v) => v.flipX));
console.log(JSON.stringify({ pads, clip, flips }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
