// Gorgegrub check: level 52 opens, a grub eats nearby fallen mudlings and swells. Screenshot.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'grub';
const server = await preview({ preview: { port: 4341, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 51; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4341/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 10 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 51 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(2, 'thornbow');
  s.sim.build(3, 'glimmer');
  s.sim.status = 'running';
  const g = s.sim.spawn('gorgegrub', 0, 760);
  g.def = { ...g.def, speed: 0 };
  const max0 = g.maxHp;
  for (let i = 0; i < 3; i++) {
    const m = s.sim.spawn('mudling', 0, 740 + i * 20);
    s.sim.applyDamage(m, 99999);
  }
  return { name: s.level?.name ?? s.sim.level?.name, fed: g.fed, max0, max1: g.maxHp };
});
for (let i = 0; i < 20; i++) await page.evaluate(() => window.__game.scene.getScene('Battle').sim.update(1 / 60));
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
