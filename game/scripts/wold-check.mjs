// Patchwork Wolds check: region 22 map, Hedgerow Lane scenery + music, a Tithe Weasel skims bounty and a Plough Ox tramples through soldiers.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'wold';
const server = await preview({ preview: { port: 4386, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 105; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4386/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 21 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 105 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(1, 'thornbow');
  s.sim.build(2, 'glimmer');
  s.sim.build(6, 'burrow');
  s.sim.build(7, 'boulder');
  s.sim.status = 'running';
  const w = s.sim.spawn('titheweasel', 0, 200);
  const cut = s.sim.titheCut();
  const ox = s.sim.spawn('ploughox', 0, 380);
  ox.hp = ox.maxHp = 99999;
  for (let i = 0; i < 300; i++) s.sim.update(1 / 60);
  for (let k = 0; k < 4; k++) s.sim.spawn(k % 2 ? 'ploughox' : 'titheweasel', k % 2, 300 + k * 60);
  return { music: window.__music.getTheme().id, titheCut: cut, oxTrampled: ox.trampled.length, oxHeld: ox.blockedBy !== 0 };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
