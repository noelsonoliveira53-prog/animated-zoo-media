// Leak check (`node scripts/leak-check.mjs <levelIdx> [idle]`): plays a busy level and compares live tweens, timers and display objects early vs later.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const idx = Number(process.argv[2] ?? 95);
const server = await preview({ preview: { port: 4403, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: {}, settings: { volume: 0, muted: true, music: false, dev: true } })));
await page.goto('http://localhost:4403/');
await page.waitForTimeout(1000);
await page.evaluate((i) => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: i }), idx);
await page.waitForTimeout(1500);
if (process.argv[3] === 'idle') await page.evaluate(() => { window.__idleOnly = true; });
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.level.slots.forEach((_, k) => { s.sim.build(k, ['thornbow', 'glimmer', 'boulder', 'burrow'][k % 4]); s.sim.upgrade(k); s.sim.upgrade(k); });
  if (window.__idleOnly) return; // idle mode: towers only, no waves (isolates ambient and idle effects)
  s.sim.callNextWave();
  s.speed = 3;
  window.__callAll = setInterval(() => s.sim.callNextWave(), 4000);
});
const snap = () => page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { tweens: s.tweens.getTweens().length, timers: (s.time._active ?? []).length, objects: s.children.list.length, wave: s.sim.waveIndex }; });
await page.waitForTimeout(3000);
const a = await snap();
await page.waitForTimeout(20000);
const b = await snap();
// LONG=1 adds a third sample 20 s later, to tell a plateau from steady growth
const c = process.env.LONG ? (await page.waitForTimeout(20000), await snap()) : undefined;
console.log(JSON.stringify({ early: a, later: b, ...(c ? { latest: c } : {}) }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no page errors');
await browser.close();
server.httpServer.close();
