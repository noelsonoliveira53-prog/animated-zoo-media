// Tower effects check: builds a tower kind at several tiers on level 5, sends a stream of enemies and screenshots
// mid-volley (trails, launch flashes, impacts, tier auras). `node scripts/towerfx-check.mjs <name> <towerId>`
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'towerfx';
const tower = process.argv[3] ?? 'thornbow';
const waitMs = Number(process.argv[4] ?? 1600);
const server = await preview({ preview: { port: 4399, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 10; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4399/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 4 }));
let ready = false;
for (let t = 0; t < 30 && !ready; t++) {
  await page.waitForTimeout(300);
  ready = await page.evaluate(() => !!window.__game.scene.getScene('Battle')?.sim);
}
const info = await page.evaluate((id) => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 99999;
  const slots = [0, 1, 2, 3, 4, 5];
  slots.forEach((slot, k) => {
    s.sim.build(slot, id);
    for (let u = 0; u < Math.min(k, 2); u++) s.sim.upgrade(slot);
    if (k >= 4) s.sim.specialize(slot, k - 4);
  });
  s.sim.status = 'running';
  for (let k = 0; k < 14; k++) s.sim.spawn('mudling', 0, 80 + k * 45);
  return { towers: s.sim.towers.filter(Boolean).map((t) => `${t.def.id}:${t.tier}${t.spec ? ':' + t.spec : ''}`) };
}, tower);
await page.waitForTimeout(waitMs);
await page.screenshot({ path: `screenshots/${name}.png` });
for (let k = 0; k < 3; k++) {
  await page.waitForTimeout(130);
  await page.screenshot({ path: `screenshots/${name}-zoom${k}.png`, clip: { x: 180, y: 90, width: 640, height: 360 } });
}
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
