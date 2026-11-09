// Thunderhead check: region 12 map, Rainmarch Downs scenery + music, a Stormcaller bolt and a Thunderhoof herd.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'storm';
const server = await preview({ preview: { port: 4342, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 55; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4342/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 11 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 55 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(1, 'thornbow');
  s.sim.build(5, 'glimmer');
  s.sim.status = 'running';
  const sc = s.sim.spawn('stormcaller', 0, 420);
  sc.def = { ...sc.def, speed: 0 };
  const herd = [0, 1, 2, 3, 4].map((k) => s.sim.spawn('thunderhoof', 0, 900 + k * 20));
  for (let i = 0; i < 60 * 4; i++) s.sim.update(1 / 60);
  return { music: window.__music.getTheme().id, frozen: s.sim.towers.filter((t) => t && t.frozen > 0).length, herdSpeed: s.sim.herdMult(herd[2]) };
});
for (let i = 0; i < 1; i++) await page.evaluate(() => window.__game.scene.getScene('Battle').sim.update(1 / 60));
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
