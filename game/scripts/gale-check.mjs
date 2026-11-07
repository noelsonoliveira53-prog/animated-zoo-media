// Galecrest Aeries check: world-map style, battle music + scenery, Galehound ignores slows, Cloudram regrows.
// and an enraged Rootrager. Screenshots each step.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'dusk';
const server = await preview({ preview: { port: 4330, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
// Unlock through level 30 so region 7 is open.
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 30; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4330/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 6 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 30 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(4, 'glimmer');
  s.sim.build(8, 'boulder');
  s.sim.status = 'running';
  const hound = s.sim.spawn('galehound', 0, 420);
  const mud = s.sim.spawn('mudling', 0, 440);
  const ram = s.sim.spawn('cloudram', 1, 120);
  ram.hp = ram.maxHp * 0.5;
  for (const e of [hound, mud, ram]) e.def = { ...e.def, speed: 0 };
  s.sim.castSpell('thornsnare', { ...hound.pos });
  return { music: window.__music.getTheme().id, houndSlow: hound.slowFactor, mudSlow: mud.slowFactor, ramHp: ram.hp };
});
const after = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  for (let i = 0; i < 240; i++) s.sim.update(1 / 60);
  const ram = s.sim.enemies.find((e) => e.def.id === 'cloudram');
  return { ramHp: ram?.hp, ramMax: ram?.maxHp };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify({ ...info, after }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
