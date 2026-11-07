// Highcanopy check: region 18 map, Ropebridge Reach scenery + music, a Howler riles under slows and a Mourner's fall toughens a mudling.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'canopy';
const server = await preview({ preview: { port: 4372, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 85; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4372/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 17 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 85 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(1, 'thornbow');
  s.sim.build(2, 'glimmer');
  s.sim.build(6, 'burrow');
  s.sim.build(7, 'boulder');
  s.sim.status = 'running';
  const h = s.sim.spawn('howler', 0, 520);
  for (let k = 0; k < 3; k++) { s.sim.slow(h, 0.6, 1); for (let i = 0; i < 40; i++) s.sim.update(1 / 60); }
  const m = s.sim.spawn('mourner', 0, 700);
  const pal = s.sim.spawn('mudling', 0, 720);
  const a0 = pal.armor;
  s.sim.applyDamage(m, 99999);
  for (let i = 0; i < 10; i++) s.sim.update(1 / 60);
  return { music: window.__music.getTheme().id, howlerSpeed: +h.speedMult.toFixed(2), mournerDead: !m.alive, palArmor: [a0, +pal.armor.toFixed(2)] };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
