// Phone-size (740×360 touch) check of the late meta screens: Field Guide page 3 (newest enemies),
// the Rustantler boss page, and the last achievements page. `node scripts/phone-guide-check.mjs <name>`.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'phone-guide';
const server = await preview({ preview: { port: 4361, strictPort: true } });
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 80; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars, stats: { boss_rustantler: 1 } }));
});
await page.goto('http://localhost:4361/');
await page.waitForTimeout(1200);
const shot = (suffix) => page.screenshot({ path: `screenshots/${name}${suffix}.png` });
const go = (scene, data) => page.evaluate(([sc, d]) => {
  window.__game.scene.getScenes(true).forEach((s) => s.scene.stop());
  window.__game.scene.start(sc, d);
}, [scene, data ?? {}]);
await page.evaluate(() => {
  const raw = JSON.parse(localStorage.getItem('grovewatch.save.v1') ?? '{}');
  raw.seenEnemies = Object.keys(window.__game.textures.list).filter((k) => k.startsWith('enemy_')).map((k) => k.slice(6));
  localStorage.setItem('grovewatch.save.v1', JSON.stringify(raw));
});
await go('FieldGuide', {});
await page.waitForTimeout(900);
const pages = await page.evaluate(() => { const g = window.__game.scene.getScene('FieldGuide'); g.show('enemies', 2); return g.entries().length; });
await page.waitForTimeout(400);
await shot('');
await page.evaluate(() => { const g = window.__game.scene.getScene('FieldGuide'); g.showDetail(g.entries().find((e) => e.key === 'rustantler')); });
await page.waitForTimeout(400);
await shot('-boss');
await go('Achievements', { page: 99 });
await page.waitForTimeout(900);
await shot('-ach');
console.log(JSON.stringify({ enemies: pages }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
