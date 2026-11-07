// Village "Collect all": a village with full mines and taps; one real tap on the button banks everything.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'collect-all';
const server = await preview({ preview: { port: 4369, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const then = Date.now() - 2 * 3600 * 1000;
  const b = (uid, type, level, col, row) => ({ uid, type, level, col, row, upgradeEnds: null, lastCollect: then });
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({
    stars: { l1: 3 },
    village: { coins: 100, glowsap: 100, nextUid: 20, buildings: [b(1, 'townhall', 3, 10, 5), b(2, 'coinmine', 2, 3, 2), b(3, 'coinmine', 2, 6, 2), b(4, 'sapwell', 2, 15, 2), b(5, 'sapwell', 1, 18, 2), b(6, 'builderhut', 1, 2, 9)] },
  }));
});
await page.goto('http://localhost:4369/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Village'));
await page.waitForTimeout(1000);
const before = await page.evaluate(() => { const v = window.__game.scene.getScene('Village').v; return { coins: v.coins, glowsap: v.glowsap }; });
await page.mouse.click(100, 720 - 112);
await page.waitForTimeout(250);
await page.screenshot({ path: `screenshots/${name}.png` });
const after = await page.evaluate(() => { const v = window.__game.scene.getScene('Village').v; return { coins: v.coins, glowsap: v.glowsap }; });
console.log(JSON.stringify({ before, after }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
