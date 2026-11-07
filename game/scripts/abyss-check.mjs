// Starwell check: world-map style, battle music + scenery, Dimlantern shrinks tower range, Echo Wisp re-forms once.
// and an enraged Rootrager. Screenshots each step.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'dusk';
const server = await preview({ preview: { port: 4339, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
// Unlock through level 45 so region 10 is open.
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 45; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4339/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 9 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 45 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  const t = s.sim.build(4, 'thornbow');
  s.sim.build(6, 'glimmer');
  s.sim.status = 'running';
  const dim = s.sim.spawn('dimlantern', 0, 1180);
  const wisp = s.sim.spawn('echowisp', 1, 400);
  dim.def = { ...dim.def, speed: 0 };
  const dimmed = s.sim.towerDim(t);
  s.sim.applyDamage(wisp, 9999);
  const echoes = s.sim.enemies.filter((e) => e.alive && e.def.id === 'echowisp').length;
  return { music: window.__music.getTheme().id, towerAt: t.pos, dimAt: dim.pos, dimmed, echoes };
});
const after = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  for (let i = 0; i < 20; i++) s.sim.update(1 / 60);
  return { alive: s.sim.enemies.filter((e) => e.alive).map((e) => e.def.id) };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify({ ...info, after }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
