// Death-burst check: spawn one of each death style, kill them together and screenshot mid-burst.
// `node scripts/death-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'death';
const server = await preview({ preview: { port: 4324, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4324/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(2000);
const info = {};
const kinds = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  // pick enemies by trait from the live sim's spawn table
  const ids = ['mudling', 'gloomwing', 'shellback', 'bogmender', 'gnat', 'thornhog'];
  const out = [];
  ids.forEach((id, i) => {
    try {
      const e = s.sim.spawn(id, 0, 260 + i * 110);
      out.push(id);
    } catch (err) { out.push('x:' + id); }
  });
  s.sim.update(1 / 60);
  return out;
});
await page.waitForTimeout(300);
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  for (const e of s.sim.enemies) if (e.alive) s.sim.applyDamage(e, e.maxHp * 0.3);
  s.sim.update(1 / 60);
  for (const e of s.sim.enemies) if (e.alive) s.sim.applyDamage(e, 1e9, 'physical');
});
const mid = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { pieces: s.children.list.filter((o) => o.depth === 2390 || o.depth === 2400).length, low: s.sys.game && 0 }; });
console.log('mid', JSON.stringify(mid));
await page.waitForTimeout(220);
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.pauseAll());
await page.waitForTimeout(100);
await page.screenshot({ path: `screenshots/${name}.png` });
await page.screenshot({ path: `screenshots/${name}-zoom.png`, clip: { x: 120, y: 90, width: 220, height: 470 } });
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.resumeAll());
await page.waitForTimeout(2500);
const left = await page.evaluate(() => window.__game.scene.getScene('Battle').children.list.filter((o) => o.depth === 2390).length);
console.log(JSON.stringify({ info, kinds, leftoverPieces: left }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || left > 0 ? 1 : 0);
