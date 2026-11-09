// Coralreach check: region 14 map, Coral Shallows scenery + music, a Shellsnap molts, a Tidecaller washes slows.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'reef';
const server = await preview({ preview: { port: 4345, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 65; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4345/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 13 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 65 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(0, 'thornbow');
  s.sim.build(4, 'glimmer');
  s.sim.status = 'running';
  const crab = s.sim.spawn('shellsnap', 0, 700);
  crab.def = { ...crab.def, speed: 0 };
  s.sim.applyDamage(crab, crab.maxHp * 0.6);
  const otter = s.sim.spawn('tidecaller', 1, 300);
  otter.def = { ...otter.def, speed: 0 };
  const mud = s.sim.spawn('mudling', 1, 330);
  mud.def = { ...mud.def, speed: 0 };
  mud.slowFactor = 0.4; mud.slowTime = 60;
  for (let i = 0; i < 60 * 4; i++) s.sim.update(1 / 60);
  return { music: window.__music.getTheme().id, molted: crab.molted, mudSlow: mud.slowFactor };
});
for (let i = 0; i < 1; i++) await page.evaluate(() => window.__game.scene.getScene('Battle').sim.update(1 / 60));
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
