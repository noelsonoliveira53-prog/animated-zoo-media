// Amberwood check: region 16 map, Amberwood Gate scenery + music, a Barkdrum hastens its pack, a Turnleaf turns its hide.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'amber';
const server = await preview({ preview: { port: 4348, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 75; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4348/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 15 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 75 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(1, 'thornbow');
  s.sim.build(2, 'glimmer');
  s.sim.build(6, 'burrow');
  s.sim.build(7, 'boulder');
  s.sim.status = 'running';
  const b = s.sim.spawn('barkdrum', 0, 520);
  const pack = [0, 1, 2, 3].map((k) => s.sim.spawn('mudling', 0, 480 + k * 26));
  const t = s.sim.spawn('turnleaf', 0, 700);
  for (let i = 0; i < 60 * 3; i++) s.sim.update(1 / 60);
  return { music: window.__music.getTheme().id, hasted: pack.filter((m) => m.hasteMult > 1).length, drumAlive: b.alive, turnArmor: +t.armor.toFixed(2), turnMr: +t.mr.toFixed(2) };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
