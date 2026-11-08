// Pebblebrook check: region 24 map, Stepping Stones scenery + music, a Bubbler Newt bubbles its friends and a Torrent Pike surges them down the stream.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'brook';
const server = await preview({ preview: { port: 4390, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 115; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4390/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 23 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 115 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(1, 'thornbow');
  s.sim.build(2, 'glimmer');
  s.sim.build(6, 'burrow');
  s.sim.build(7, 'boulder');
  s.sim.status = 'running';
  const n = s.sim.spawn('bubbler', 0, 380);
  const p = s.sim.spawn('pike', 0, 330);
  for (let k = 0; k < 3; k++) s.sim.spawn('mudling', 0, 340 + k * 25);
  n.bubbleCd = 0.01;
  p.surgeCd = 0.01;
  const d0 = p.dist;
  for (let i = 0; i < 20; i++) s.sim.update(1 / 60);
  const bubbled = s.sim.enemies.filter((e) => e.bubbled).length;
  const surged = Math.round(p.dist - d0);
  return { music: window.__music.getTheme().id, bubbled, surged };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
