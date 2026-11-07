// Verdant Ruins check: world-map style, battle music + scenery, Shiftscale swaps resists, Idol Keeper raises the fallen.
// and an enraged Rootrager. Screenshots each step.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'dusk';
const server = await preview({ preview: { port: 4333, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
// Unlock through level 35 so region 8 is open.
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 35; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4333/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 7 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 35 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(2, 'glimmer');
  s.sim.build(6, 'thornbow');
  s.sim.status = 'running';
  const lizard = s.sim.spawn('shiftscale', 0, 700);
  const keeper = s.sim.spawn('idolkeeper', 0, 560);
  const mud = s.sim.spawn('mudling', 0, 600);
  for (const e of [lizard, keeper, mud]) e.def = { ...e.def, speed: 0 };
  s.sim.applyDamage(mud, 9999);
  const before = { ...s.sim.res(lizard) };
  return { music: window.__music.getTheme().id, before };
});
const after = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  for (let i = 0; i < 380; i++) s.sim.update(1 / 60);
  const lizard = s.sim.enemies.find((e) => e.def.id === 'shiftscale');
  const risen = s.sim.enemies.filter((e) => e.alive && e.revived).map((e) => e.def.id);
  return { lizardShifted: lizard?.shifted, res: lizard && s.sim.res(lizard), risen };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify({ ...info, after }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
