// Endless "home turf" check: an endless run on Hollow Oak Crossing (Amberwood) brings Amberwood enemies after wave 5
// and Rustantler as the wave-10 boss. Calls waves early, fast-forwards, and screenshots a home-turf wave.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'endless-home';
const server = await preview({ preview: { port: 4363, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 80; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4363/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 77, endless: true }));
await page.waitForTimeout(2000);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const sim = s.sim;
  const home = ['sapstoat', 'barkdrum', 'turnleaf'];
  const firstHome = sim.level.waves.findIndex((w) => w.groups.some((g) => home.includes(g.enemy))) + 1;
  const boss10 = sim.level.waves[9].groups.find((g) => g.enemy === 'rustantler')?.enemy ?? null;
  // play up to the first home-turf wave so it is on screen
  sim.coins = 6000;
  sim.level.slots.forEach((_, i) => sim.build(i, ['thornbow', 'glimmer', 'boulder', 'burrow'][i % 4]));
  for (let w = 0; w < firstHome; w++) sim.callNextWave();
  for (let i = 0; i < 60 * 6; i++) sim.update(1 / 60);
  return { firstHome, boss10, onField: [...new Set(sim.enemies.filter((e) => e.alive).map((e) => e.def.id))] };
});
await page.waitForTimeout(800);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
