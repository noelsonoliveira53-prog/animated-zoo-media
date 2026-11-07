// Blackwake check: region 15 map, Blackwake Moorings scenery + music, a Deckgunner shoots a soldier, an Ironkeel anchors.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'flotilla';
const server = await preview({ preview: { port: 4347, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 70; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4347/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 14 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 70 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(2, 'burrow');
  s.sim.build(5, 'glimmer');
  s.sim.status = 'running';
  for (let i = 0; i < 30; i++) s.sim.update(1 / 60);
  const sol = s.sim.soldiers[0];
  const g = s.sim.spawn('deckgunner', 0, 500);
  g.def = { ...g.def, speed: 0 };
  g.pos = { x: sol.pos.x - 100, y: sol.pos.y };
  const k = s.sim.spawn('ironkeel', 0, 1500);
  for (let i = 0; i < 60 * 6.2; i++) s.sim.update(1 / 60);
  return { music: window.__music.getTheme().id, soldierHp: Math.round(sol.hp), anchored: k.anchored };
});
for (let i = 0; i < 1; i++) await page.evaluate(() => window.__game.scene.getScene('Battle').sim.update(1 / 60));
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
