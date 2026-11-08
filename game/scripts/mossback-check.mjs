// Pebblebrook finale check: level 120 with Ironhorn on the field and its first phase.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'mossback';
const server = await preview({ preview: { port: 4392, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 119; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4392/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 23 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 119 }));
let ready = false;
for (let t = 0; t < 30 && !ready; t++) {
  await page.waitForTimeout(300);
  ready = await page.evaluate(() => !!window.__game.scene.getScene('Battle')?.sim);
}
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 4000;
  s.sim.build(1, 'thornbow');
  s.sim.build(4, 'glimmer');
  s.sim.build(6, 'burrow');
  s.sim.build(7, 'boulder');
  s.sim.status = 'running';
  for (let i = 0; i < 60; i++) s.sim.update(1 / 60);
  const soldiers0 = s.sim.soldiers.filter((x) => x.alive).length;
  const sold = s.sim.soldiers.find((x) => x.alive);
  const b = s.sim.spawn('mossback', 1, 300);
  if (sold) { b.pos.x = sold.pos.x + 40; b.pos.y = sold.pos.y; }
  for (let i = 0; i < 5; i++) s.sim.update(1 / 60);
  const soldiers1 = s.sim.soldiers.filter((x) => x.alive).length;
  s.sim.applyDamage(b, b.maxHp * 0.3);
  for (let i = 0; i < 30; i++) s.sim.update(1 / 60);
  return { soldiers: [soldiers0, soldiers1], bossAlive: b.alive, pikes: s.sim.enemies.filter((e) => e.alive && e.def.id === 'pike').length };
});
await page.waitForTimeout(800);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
