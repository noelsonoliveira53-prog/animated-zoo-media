// Sunscour check: region 13 map, Mirage Flats scenery + music, a Shimmerjack sheds decoys, a Sandpicker steals coins.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'dunes';
const server = await preview({ preview: { port: 4344, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 60; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4344/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 12 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 60 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(0, 'thornbow');
  s.sim.build(3, 'glimmer');
  s.sim.status = 'running';
  const sj = s.sim.spawn('shimmerjack', 0, 520);
  sj.def = { ...sj.def, speed: 0 };
  s.sim.applyDamage(sj, 5);
  const sp = s.sim.spawn('sandpicker', 1, s.sim.paths[1].length - 5);
  const c0 = s.sim.coins;
  for (let i = 0; i < 30; i++) s.sim.update(1 / 60);
  return { music: window.__music.getTheme().id, decoys: s.sim.enemies.filter((e) => e.alive && e.def.id === 'mirageling').length, stolen: c0 - s.sim.coins };
});
for (let i = 0; i < 1; i++) await page.evaluate(() => window.__game.scene.getScene('Battle').sim.update(1 / 60));
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
