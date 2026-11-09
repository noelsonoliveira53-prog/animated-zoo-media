// Spell effects check: casts Starfall, Grove Call and Thornsnare on a road and screenshots each one mid-effect.
// `node scripts/spellfx-check.mjs <name>` writes screenshots/<name>.png (all three) plus <name>-star.png
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'spellfx';
const server = await preview({ preview: { port: 4325, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4325/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(2000);
// points on the first road, spread apart
const pts = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const at = (d) => { const e = s.sim.spawn('mudling', 0, d); const p = { ...e.pos }; e.alive = false; return p; };
  return [at(300), at(700), at(1100)];
});
const casts = await page.evaluate((pts) => {
  const s = window.__game.scene.getScene('Battle');
  for (const id of ['mudling', 'mudling', 'mudling']) pts.forEach((p, i) => s.sim.spawn('mudling', 0, [300, 700, 1100][i]));
  s.sim.callNextWave();
  return [s.sim.castSpell('starfall', pts[0]), s.sim.castSpell('grovecall', pts[1]), s.sim.castSpell('thornsnare', pts[2])];
}, pts);
// headless frames can run slow, so follow the sim's own strike timer instead of wall-clock waits
await page.waitForFunction(() => { const st = window.__game.scene.getScene('Battle').sim.strikes[0]; return !st || st.timer < 0.35; }, null, { timeout: 15000 });
await page.screenshot({ path: `screenshots/${name}-star.png` }); // star mid-fall
await page.waitForFunction(() => window.__game.scene.getScene('Battle').sim.strikes.length === 0, null, { timeout: 15000 });
await page.waitForTimeout(120);
await page.screenshot({ path: `screenshots/${name}.png` }); // star impact
await page.waitForTimeout(6000);
const left = await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.getTweens().length);
console.log(JSON.stringify({ pts, casts, tweensAfter: left }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || casts.includes(false) ? 1 : 0);
