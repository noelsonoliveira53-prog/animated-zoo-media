// Hero and soldier bars: wounds the hero and two Wardens (one poisoned), screenshots them while the damage
// trail is held, then checks the trails drain to the fill. `node scripts/allybar-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'allybar';
const server = await preview({ preview: { port: 4344, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 })).newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4344/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const p = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 5000;
  s.sim.build(3, 'burrow');
  s.sim.update(1 / 60);
  s.sim.update(1);
  const sol = s.sim.soldiers.filter((x) => x.alive);
  const h = s.sim.hero;
  // park the hero beside the Wardens for one close-up
  h.pos.x = sol[0].pos.x + 50; h.pos.y = sol[0].pos.y; if (h.target) { h.target.x = h.pos.x; h.target.y = h.pos.y; }
  s.paused = true;
  return { x: sol[0].pos.x, y: sol[0].pos.y, n: sol.length };
});
let t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 400, t0, { timeout: 20000, polling: 'raf' });
t0 = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const sol = s.sim.soldiers.filter((x) => x.alive);
  sol[0].hp = sol[0].maxHp * 0.55;
  if (sol[1]) { sol[1].hp = sol[1].maxHp * 0.25; sol[1].poisonT = 5; }
  if (sol[2]) sol[2].hp = sol[2].maxHp * 0.8;
  s.sim.hero.hp = s.sim.hero.maxHp * 0.4;
  return s.time.now;
});
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 120, t0, { timeout: 20000, polling: 'raf' });
await page.screenshot({ path: `screenshots/${name}.png`, clip: { x: Math.max(0, p.x - 140), y: Math.max(0, p.y - 110), width: 280, height: 160 } });
const held = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return [+s.heroTrail.trail.toFixed(2), ...[...s.soldierViews.values()].map((v) => +v.trail.trail.toFixed(2))]; });
t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 9000, t0, { timeout: 60000, polling: 'raf' });
const later = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return [+s.heroTrail.trail.toFixed(2), ...[...s.soldierViews.values()].map((v) => +v.trail.trail.toFixed(2))]; });
console.log(JSON.stringify({ soldiers: p.n, held, later }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
