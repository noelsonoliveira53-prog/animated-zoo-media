// Trading Post: shows it in the village, opens the 10-card build shop and its trade panel,
// then clicks the coins-to-glowsap trade and checks both purses.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'market';
const server = await preview({ preview: { port: 4388, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const now = Date.now();
  const b = (uid, type, level, col, row) => ({ uid, type, level, col, row, upgradeEnds: null, lastCollect: now });
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({
    stars: { l1: 3, l2: 3 }, hero: 'fen',
    village: { coins: 3000, glowsap: 1000, nextUid: 20, buildings: [b(1, 'townhall', 3, 10, 5), b(2, 'workshop', 1, 2, 2), b(3, 'market', 1, 15, 8), b(4, 'builderhut', 1, 2, 10), b(5, 'builderhut', 1, 6, 10), b(6, 'market', 3, 0, 0)].slice(0, 5) },
  }));
});
await page.goto('http://localhost:4388/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Village'));
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Village').openPanel(3, false));
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}-panel.png` });
await page.evaluate(() => { const s = window.__game.scene.getScene('Village'); s.closePanel?.(); s.openShop(); });
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}.png` });
const before = await page.evaluate(() => { const v = window.__game.scene.getScene('Village').v; return [v.coins, v.glowsap]; });
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Village');
  s.openPanel(3, false);
  const btn = s.panel.list.find((o) => o.name === 'trade_coins');
  btn.emit('pointerdown', null, 0, 0, { stopPropagation() {} });
});
await page.waitForTimeout(300);
const after = await page.evaluate(() => { const v = window.__game.scene.getScene('Village').v; return [v.coins, v.glowsap]; });
console.log('trade', JSON.stringify({ before, after }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(0);
