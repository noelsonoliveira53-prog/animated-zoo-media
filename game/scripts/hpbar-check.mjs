// Enemy health bars: damages four foes (plain, armored, magic-resistant, both) and screenshots the bars while the
// damage trail is still held, then checks the trail drains down to the fill. `node scripts/hpbar-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'hpbar';
const server = await preview({ preview: { port: 4341, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 })).newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4341/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const p = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const kinds = [['mudling', 0.75], ['shellback', 0.5], ['wispling', 0.3], ['mirrorback', 0.12]];
  const es = kinds.map(([k], i) => s.sim.spawn(k, 0, 480 + i * 70));
  s.sim.update(1 / 60);
  s.paused = true;
  window.__hpEs = es.map((e) => e.uid);
  // set health directly so armor doesn't change the numbers; first a light hit, then the big one
  es.forEach((e, i) => { e.hp = e.maxHp * 0.95; });
  return { pos: es[1].pos, fr: kinds.map(([, f]) => f) };
});
// let the first light hit settle into the bar, then land the big drop and catch the held trail
let t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 3000, t0, { timeout: 20000, polling: 'raf' });
t0 = await page.evaluate((fr) => { const s = window.__game.scene.getScene('Battle'); s.sim.enemies.filter((e) => window.__hpEs.includes(e.uid)).forEach((e) => { e.hp = e.maxHp * fr[window.__hpEs.indexOf(e.uid)]; }); return s.time.now; }, p.fr);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 120, t0, { timeout: 20000, polling: 'raf' });
await page.screenshot({ path: `screenshots/${name}.png`, clip: { x: Math.max(0, p.pos.x - 200), y: Math.max(0, p.pos.y - 120), width: 400, height: 200 } });
const held = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return window.__hpEs.map((u) => +s.enemyViews.get(u).trail.trail.toFixed(2)); });
t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 9000, t0, { timeout: 60000, polling: 'raf' });
const later = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return window.__hpEs.map((u) => +s.enemyViews.get(u).trail.trail.toFixed(2)); });
console.log(JSON.stringify({ held, later, fill: p.fr }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
