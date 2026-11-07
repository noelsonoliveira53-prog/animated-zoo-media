// Phone-sized touch check: taps just outside a button's drawn edge and just outside a build pad,
// and confirms both still register thanks to padded hit areas. Screenshots the result.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'mobile';
const server = await preview({ preview: { port: 4321, strictPort: true } });
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4321/');
await page.waitForTimeout(1200);
// Convert game coords to page coords via the canvas rect.
const toPage = (gx, gy) => page.evaluate(([x, y]) => {
  const r = document.querySelector('canvas').getBoundingClientRect();
  return { x: r.left + (x / 1280) * r.width, y: r.top + (y / 720) * r.height };
}, [gx, gy]);
const results = {};
// Settings button: 190×52 at (680,662). Tap 8 game px below its drawn bottom edge.
let p = await toPage(680, 662 + 26 + 8);
await page.touchscreen.tap(p.x, p.y);
await page.waitForTimeout(500);
results.settingsTapOutsideEdge = await page.evaluate(() => window.__game.scene.isActive('Settings'));
await page.screenshot({ path: `screenshots/${name}-settings.png` });
// Battle: tap 10 px above a build pad's top edge (pad texture 64×48).
await page.evaluate(() => {
  window.__game.scene.getScenes(true).forEach((s) => s.scene.stop());
  window.__game.scene.start('Battle', { levelIndex: 0 });
});
await page.waitForTimeout(2500);
const slot = await page.evaluate(() => window.__game.scene.getScene('Battle').level.slots[0]);
p = await toPage(slot.x, slot.y - 24 - 8);
await page.touchscreen.tap(p.x, p.y);
await page.waitForTimeout(400);
results.slotTapOutsideEdge = await page.evaluate(() => !!window.__game.scene.getScene('Battle').menu);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(results));
console.log(errors.length ? 'ERRORS: ' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(results.settingsTapOutsideEdge && results.slotTapOutsideEdge && !errors.length ? 0 : 1);
