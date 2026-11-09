// Sorrel check: hero picker shows the hare medic; in battle Second Wind heals nearby soldiers. Screenshots both.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'sorrel';
const server = await preview({ preview: { port: 4343, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 3, l3: 3 }, hero: 'sorrel' }));
});
await page.goto('http://localhost:4343/');
await page.waitForTimeout(1500);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  const slot = s.level.slots.findIndex(() => true);
  s.sim.build(slot, 'burrow');
  s.sim.status = 'running';
  for (let i = 0; i < 60; i++) s.sim.update(1 / 60);
  const sol = s.sim.soldiers[0];
  s.sim.hero.pos = { x: sol.pos.x + 20, y: sol.pos.y };
  s.sim.hero.dest = null;
  for (const so of s.sim.soldiers) so.hp = 5;
  const ok = s.sim.useHeroSkill();
  return { hero: s.sim.hero.def.name, ok, soldierHp: s.sim.soldiers.map((so) => Math.round(so.hp)) };
});
await page.waitForTimeout(250);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
