// Raid bars: deploys troops, wounds two troops and two camp buildings, screenshots while the damage trails are
// held, then checks they drain to the fill. `node scripts/raidbar-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'raidbar';
const server = await preview({ preview: { port: 4348, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 })).newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ settings: { dev: true }, army: { brawler: 12 } })));
await page.goto('http://localhost:4348/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Raid', { tier: 1, seed: 3 }));
await page.waitForTimeout(1500);
await page.evaluate(() => { const s = window.__game.scene.getScene('Raid'); for (let i = 0; i < 3; i++) s.sim.deploy('brawler', { x: 200, y: 260 + i * 40 }); });
let t0 = await page.evaluate(() => window.__game.scene.getScene('Raid').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Raid').time.now > t + 1500, t0, { timeout: 20000, polling: 'raf' });
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Raid');
  s.done = true; // freeze the sim (the views keep animating) so nothing dies mid-check
  const troops = s.sim.troops.filter((t) => t.alive).slice(0, 2);
  troops.forEach((t, i) => { t.hp = t.maxHp * (i ? 0.25 : 0.6); });
  const blds = s.sim.camp.buildings.filter((b) => b.hp > 0).slice(0, 2);
  blds.forEach((b, i) => { b.hp = b.maxHp * (i ? 0.2 : 0.55); });
  window.__ids = { troops: troops.map((t) => t.uid), blds: blds.map((b) => b.uid) };
  return { tx: troops[0].pos.x, ty: troops[0].pos.y, n: troops.length + blds.length };
});
t0 = await page.evaluate(() => window.__game.scene.getScene('Raid').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Raid').time.now > t + 120, t0, { timeout: 20000, polling: 'raf' });
await page.screenshot({ path: `screenshots/${name}.png` });
const read = () => page.evaluate(() => { const s = window.__game.scene.getScene('Raid'); return [...window.__ids.troops.map((u) => s.troopViews.get(u).trail.trail), ...window.__ids.blds.map((u) => s.buildingViews.get(u).trail.trail)].map((v) => +v.toFixed(2)); });
const held = await read();
t0 = await page.evaluate(() => window.__game.scene.getScene('Raid').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Raid').time.now > t + 9000, t0, { timeout: 60000, polling: 'raf' });
const later = await read();
console.log(JSON.stringify({ wounded: info.n, held, later }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
