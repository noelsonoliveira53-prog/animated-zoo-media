// Thistledown check: region 21 map, Windfluff Rise scenery + music, a Tumblehog gathers momentum and a Bloomdoe heals on death.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'thistle';
const server = await preview({ preview: { port: 4383, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 100; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4383/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 20 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 100 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(1, 'thornbow');
  s.sim.build(2, 'glimmer');
  s.sim.build(6, 'burrow');
  s.sim.build(7, 'boulder');
  s.sim.status = 'running';
  const t = s.sim.spawn('tumblehog', 0, 200);
  for (let i = 0; i < 240; i++) s.sim.update(1 / 60);
  const roll = s.sim.momentumMult(t);
  const d = s.sim.spawn('bloomdoe', 1, 150);
  const pal = s.sim.spawn('mudling', 1, 170);
  pal.hp = 1;
  s.sim.applyDamage(d, 99999);
  for (let k = 0; k < 4; k++) s.sim.spawn(k % 2 ? 'bloomdoe' : 'tumblehog', k % 2, 300 + k * 60);
  return { music: window.__music.getTheme().id, roll: +roll.toFixed(2), healed: pal.hp > 1 };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
