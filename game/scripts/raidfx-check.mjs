// Raid defense effects: opens a raid (dev army), sends brawlers at the camp, and screenshots mid-volley once a dart or
// stone is in the air (tweens paused). `node scripts/raidfx-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'raidfx';
const server = await preview({ preview: { port: 4333, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ settings: { dev: true }, army: { brawler: 12 } })));
await page.goto('http://localhost:4333/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Raid', { tier: 1, seed: 3 }));
await page.waitForTimeout(1500);
const n = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Raid');
  let k = 0;
  for (let i = 0; i < 8; i++) if (s.sim.deploy('brawler', { x: 200, y: 200 + i * 40 })) k++;
  return k;
});
// wait until a shot is flying (a dart rectangle or a stone circle at the projectile depth)
await page.waitForFunction(() => window.__game.scene.getScene('Raid').children.list.some((o) => o.depth === 5550), null, { timeout: 30000, polling: 'raf' });
await page.evaluate(() => window.__game.scene.getScene('Raid').tweens.pauseAll());
await page.waitForTimeout(60);
await page.screenshot({ path: `screenshots/${name}.png` });
await page.evaluate(() => window.__game.scene.getScene('Raid').tweens.resumeAll());
await page.waitForTimeout(3000);
const left = await page.evaluate(() => window.__game.scene.getScene('Raid').children.list.filter((o) => o.depth === 5550).length);
console.log(JSON.stringify({ deployed: n, inFlightAfter: left }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
