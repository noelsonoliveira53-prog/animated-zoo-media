// Rotbloom check: world-map style, battle music + scenery, Barkwarden armors allies, Rotseeds sprout.
// and an enraged Rootrager. Screenshots each step.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'dusk';
const server = await preview({ preview: { port: 4340, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
// Unlock through level 50 so region 11 is open.
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 50; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4340/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 10 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 50 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(2, 'thornbow');
  s.sim.build(6, 'glimmer');
  s.sim.status = 'running';
  const bw = s.sim.spawn('barkwarden', 0, 700);
  const mud = s.sim.spawn('mudling', 0, 740);
  const sc = s.sim.spawn('seedcaster', 1, 300);
  for (const e of [bw, mud, sc]) e.def = { ...e.def, speed: 0 };
  return { music: window.__music.getTheme().id, mudArmor: s.sim.res(mud).armor, baseArmor: mud.def.armor };
});
const after = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  for (let i = 0; i < 60 * 11; i++) s.sim.update(1 / 60);
  return { alive: s.sim.enemies.filter((e) => e.alive).map((e) => e.def.id) };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify({ ...info, after }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
