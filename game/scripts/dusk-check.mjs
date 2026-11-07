// Region 4 check: the Duskcap world map, then level 16 with Veilstalkers (veiled until near a tower)
// and an enraged Rootrager. Screenshots each step.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'dusk';
const server = await preview({ preview: { port: 4322, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
// Unlock through level 15 so region 4 is open.
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 25; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4322/');
await page.waitForTimeout(1000);
await page.evaluate((r) => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: r }), Number(process.env.REGION ?? 3));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 15 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(4, 'glimmer');
  s.sim.status = 'running';
  const far = s.sim.spawn('veilstalker', 0, 60); // far from any tower: veiled
  const near = s.sim.spawn('veilstalker', 0, 1085); // near the tower at slot 4
  const r = s.sim.spawn('rootrager', 1, 380);
  r.hp = r.maxHp * 0.45; // will enrage on the next tick
  for (const e of [far, near, r]) e.def = { ...e.def, speed: 0 };
  return { music: window.__music.getTheme().id, theme: s.level.theme.shrooms };
});
await page.waitForTimeout(500);
const after = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  for (let i = 0; i < 180; i++) s.sim.update(1 / 60); // headless renders slowly; fast-forward the sim
  const vs = s.sim.enemies.filter((e) => e.def.id === 'veilstalker');
  const r = s.sim.enemies.find((e) => e.def.id === 'rootrager');
  return { farHp: vs[0] && vs[0].hp === vs[0].maxHp, nearHurt: vs[1] && vs[1].hp < vs[1].maxHp, enraged: r?.enraged };
});
await page.screenshot({ path: `screenshots/${name}-l16.png` });
// Level 17: pop a Puffcap next to a crowd and check the spore haste.
await page.evaluate(() => window.__game.scene.getScene('Battle').scene.start('Battle', { levelIndex: 16 }));
await page.waitForTimeout(2500);
const spores = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.status = 'running';
  s.sim.coins = 2000;
  s.sim.build(1, 'thornbow');
  s.sim.build(3, 'glimmer');
  const p = s.sim.spawn('puffcap', 0, 700);
  const crowd = [0, 1, 2, 3].map((k) => s.sim.spawn('thornhog', 0, 640 + k * 30));
  s.sim.applyDamage(p, 99999);
  return crowd.filter((e) => e.hasteMult > 1).length;
});
await page.waitForTimeout(250);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify({ ...info, ...after, hastedByPuffcap: spores }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !after.enraged || !after.farHp || !after.nearHurt || info.music !== 'dusk' || spores < 3 ? 1 : 0);
