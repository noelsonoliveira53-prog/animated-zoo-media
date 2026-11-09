// Honeycomb Hills check: region 19 map, Hivegate Meadow scenery + music, a Waxback's coat melts under magic and a Hexguard parries shots.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'comb';
const server = await preview({ preview: { port: 4376, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 90; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4376/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 18 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 90 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(1, 'thornbow');
  s.sim.build(2, 'glimmer');
  s.sim.build(6, 'burrow');
  s.sim.build(7, 'boulder');
  s.sim.status = 'running';
  const w = s.sim.spawn('waxback', 0, 520);
  const a0 = w.armor;
  s.sim.applyDamage(w, w.maxHp * 0.25, 'magic');
  const g = s.sim.spawn('hexguard', 1, 200);
  let parries = 0;
  for (let i = 0; i < 240; i++) { s.sim.update(1 / 60); parries += s.sim.events.filter((e) => e.type === 'parry').length; }
  for (let k = 0; k < 4; k++) s.sim.spawn(k % 2 ? 'hexguard' : 'waxback', k % 2, 300 + k * 60);
  return { music: window.__music.getTheme().id, waxArmor: [+a0.toFixed(2), +w.armor.toFixed(2)], hexCharges: g.parryCharges, parries };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
