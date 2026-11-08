// Spray Otter check: level 117, an otter's mist soaks a group and a Starfall lands on it for reduced damage.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'otter';
const server = await preview({ preview: { port: 4391, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 116; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4391/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 23 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 116 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(1, 'thornbow');
  s.sim.build(2, 'glimmer');
  s.sim.build(6, 'burrow');
  s.sim.build(7, 'boulder');
  s.sim.status = 'running';
  const o = s.sim.spawn('sprayotter', 0, 420);
  const m1 = s.sim.spawn('mudling', 0, 460);
  const m2 = s.sim.spawn('mudling', 1, 200);
  const hp0 = [m1.hp, m2.hp];
  s.sim.castSpell('starfall', m1.pos);
  s.sim.spellCd.starfall = 0;
  s.sim.castSpell('starfall', m2.pos);
  for (let i = 0; i < 70; i++) s.sim.update(1 / 60);
  const lost = [Math.round(hp0[0] - m1.hp), Math.round(hp0[1] - m2.hp)];
  return { spells: Object.keys(s.sim.spellCd), soakedLost: lost[0], dryLost: lost[1] };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
