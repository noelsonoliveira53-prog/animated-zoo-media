// Thornsnare check: the spell bar shows three spells; arm Thornsnare with a real click on its button, tap a crowd of
// walkers, and confirm they're rooted (slowed) while a flyer is not.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'snare';
const server = await preview({ preview: { port: 4329, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4329/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 0 }));
await page.waitForTimeout(2500);
const crowd = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.status = 'running';
  const ids = [];
  for (let k = 0; k < 5; k++) ids.push(s.sim.spawn('mudling', 0, 560 + k * 14).uid);
  const fly = s.sim.spawn('gloomwing', 0, 580).uid;
  for (const e of s.sim.enemies) e.def = { ...e.def, speed: 0 };
  const e0 = s.sim.enemies.find((e) => e.uid === ids[2]);
  return { x: e0.pos.x, y: e0.pos.y, ids, fly, spellPos: s.spellPos(2) };
});
await page.mouse.click(crowd.spellPos.x, crowd.spellPos.y); // arm Thornsnare
await page.waitForTimeout(350);
await page.screenshot({ path: `screenshots/${name}-armed.png` });
const hint = await page.evaluate(() => !!window.__game.scene.getScene('Battle').children.getByName('spellHint'));
await page.mouse.click(crowd.x, crowd.y); // cast
await page.waitForTimeout(400);
const res = await page.evaluate(({ ids, fly }) => {
  const s = window.__game.scene.getScene('Battle');
  const walkers = s.sim.enemies.filter((e) => ids.includes(e.uid));
  const f = s.sim.enemies.find((e) => e.uid === fly);
  return { rooted: walkers.filter((e) => e.slowFactor < 0.5).length, flyerSlowed: f ? f.slowFactor < 1 : null, cd: Math.round(s.sim.spellCd.thornsnare) };
}, crowd);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify({ ...res, hint }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || res.rooted < 4 || res.flyerSlowed || res.cd <= 0 || !hint ? 1 : 0);
