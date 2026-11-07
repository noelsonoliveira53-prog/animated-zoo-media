// Screenshot any campaign level mid-battle: `node scripts/level-shot.mjs <name> <levelIndex> [bossId]`.
// With a bossId, the boss is spawned and hurt to 45% so its phases (summons, shield) trigger.
// Builds a mixed defence on every pad, calls a few waves and fast-forwards the sim so the map looks lived-in.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'level';
const levelIndex = Number(process.argv[3] ?? 0);
const bossId = process.argv[4] ?? null;
const server = await preview({ preview: { port: 4323, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 80; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4323/');
await page.waitForTimeout(1000);
await page.evaluate((i) => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: i }), levelIndex);
await page.waitForTimeout(2500);
const info = await page.evaluate((bossId) => {
  const s = window.__game.scene.getScene('Battle');
  const kinds = ['thornbow', 'glimmer', 'boulder', 'burrow'];
  s.sim.coins = 99999;
  s.sim.level.slots.forEach((_, i) => s.sim.build(i, kinds[i % kinds.length]));
  s.sim.callNextWave();
  s.sim.callNextWave();
  s.sim.callNextWave();
  for (let i = 0; i < 60 * 14; i++) s.sim.update(1 / 60);
  let boss = null;
  if (bossId) {
    const b = s.sim.spawn(bossId, 0, 900);
    s.sim.applyDamage(b, b.maxHp * 0.3);
    s.sim.update(1 / 60);
    s.sim.applyDamage(b, b.maxHp * 0.25);
    for (let i = 0; i < 60 * 2; i++) s.sim.update(1 / 60);
    boss = { phase: b.phase, shield: Math.round(b.shield), alive: b.alive, minions: s.sim.enemies.filter((e) => e.alive && !e.def.boss).length };
  }
  return { level: s.level.name, enemies: s.sim.enemies.filter((e) => e.alive).length, lives: s.sim.lives, boss };
}, bossId);
await page.waitForTimeout(700);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || (bossId && !(info.boss && info.boss.phase >= 2)) ? 1 : 0);
