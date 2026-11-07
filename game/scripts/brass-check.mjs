// Brasswork check: world-map style, battle music + scenery, Cogjammer slows nearby towers, Steamrunner bolts when hit.
// and an enraged Rootrager. Screenshots each step.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'dusk';
const server = await preview({ preview: { port: 4337, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
// Unlock through level 40 so region 9 is open.
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 40; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4337/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 8 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 40 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  const t = s.sim.build(2, 'thornbow');
  s.sim.build(6, 'glimmer');
  s.sim.status = 'running';
  const jam = s.sim.spawn('cogjammer', 0, 600);
  const run = s.sim.spawn('steamrunner', 1, 300);
  for (const e of [jam]) e.def = { ...e.def, speed: 0 };
  const jammed = s.sim.towerJam(t);
  s.sim.applyDamage(run, 1);
  return { music: window.__music.getTheme().id, towerAt: t.pos, jamAt: jam.pos, jammed, bolting: s.sim.chargeMult(run) };
});
const after = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  for (let i = 0; i < 30; i++) s.sim.update(1 / 60);
  return { alive: s.sim.enemies.filter((e) => e.alive).map((e) => e.def.id) };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify({ ...info, after }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
