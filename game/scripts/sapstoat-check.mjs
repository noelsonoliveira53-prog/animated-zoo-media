// Russet Hollow check: level 77 in the Amberwood, a Sapstoat brawls with Badger Wardens and heals off its bites.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'sapstoat';
const server = await preview({ preview: { port: 4349, strictPort: true } });
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
await page.goto('http://localhost:4349/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 76 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(4, 'burrow');
  s.sim.build(5, 'glimmer');
  s.sim.status = 'running';
  for (let i = 0; i < 40; i++) s.sim.update(1 / 60);
  const sol = s.sim.soldiers[0];
  const st = s.sim.spawn('sapstoat', 0, 900);
  st.pos = { x: sol.pos.x - 30, y: sol.pos.y };
  st.dist = s.sim.paths[0].length * 0.4;
  st.hp = st.maxHp * 0.5;
  let healed = 0;
  for (let i = 0; i < 60 * 3; i++) { s.sim.update(1 / 60); }
  return { music: window.__music.getTheme().id, stoatHpFrac: +(st.hp / st.maxHp).toFixed(2), blocked: st.blockedBy > 0, soldiers: s.sim.soldiers.length };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
