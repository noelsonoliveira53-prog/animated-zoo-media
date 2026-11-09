// Range preview + pad glow: builds two towers, opens one's menu (range field and dashed rim), leaves other pads empty
// with coins to spare (they should glow), then spends down so glows go off. `node scripts/range-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'range';
const server = await preview({ preview: { port: 4337, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4337/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1600);
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 800;
  s.sim.build(1, 'glimmer');
  s.sim.build(2, 'thornbow');
});
await page.waitForTimeout(800);
await page.evaluate(() => window.__game.scene.getScene('Battle').openSlotMenu(1));
await page.waitForTimeout(700);
const lit = await page.evaluate(() => window.__game.scene.getScene('Battle').padGlows.filter((g) => g.visible).length);
await page.screenshot({ path: `screenshots/${name}.png` });
const off = await page.evaluate(async () => { const s = window.__game.scene.getScene('Battle'); s.sim.coins = 0; await new Promise((r) => setTimeout(r, 600)); return s.padGlows.filter((g) => g.visible).length; });
console.log(JSON.stringify({ glowingWithCoins: lit, glowingBroke: off }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || lit === 0 || off !== 0 ? 1 : 0);
