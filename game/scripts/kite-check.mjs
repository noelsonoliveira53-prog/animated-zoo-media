// Kitewing check: opens level 32, places a Kitewing among walkers, fast-forwards to its gust, screenshots.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'kite-check';
const server = await preview({ preview: { port: 4331, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 31; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4331/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 6 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 31 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(2, 'thornbow');
  s.sim.build(6, 'glimmer');
  s.sim.status = 'running';
  const kite = s.sim.spawn('kitewing', 0, 700);
  const walkers = [660, 690, 720, 750].map((d) => s.sim.spawn(d % 60 ? 'galehound' : 'cloudram', 0, d));
  for (const e of [kite, ...walkers]) e.def = { ...e.def, speed: 0 };
  const before = walkers.map((w) => w.dist);
  kite.gustCd = 0.05;
  for (let i = 0; i < 6; i++) s.sim.update(1 / 60);
  return { moved: walkers.map((w, i) => Math.round(w.dist - before[i])) };
});
await page.waitForTimeout(150);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
