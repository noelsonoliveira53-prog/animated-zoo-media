// Raid panel at phone size (740x360 touch): checks the five troop cards stay readable.
// Opens the raid panel, trains troops with real clicks, attacks the easy camp, deploys, and plays it out.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'raid';
const server = await preview({ preview: { port: 4346, strictPort: true } });
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await page.addInitScript(() => {
  if (localStorage.getItem('grovewatch.save.v1')) return;
  const now = Date.now();
  const b = (uid, type, level, col, row) => ({ uid, type, level, col, row, upgradeEnds: null, lastCollect: now });
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({
    stars: { l1: 3, l2: 2 }, hero: 'fen',
    village: { coins: 1000, glowsap: 3000, nextUid: 20, buildings: [b(1, 'townhall', 2, 10, 5), b(2, 'barracks', 2, 2, 2), b(3, 'builderhut', 1, 2, 10), b(4, 'vault', 2, 6, 8)] },
  }));
});
await page.goto('http://localhost:4346/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Village'));
await page.waitForTimeout(800);
await page.evaluate(() => window.__game.scene.getScene('Village').openRaid());
await page.waitForTimeout(700);
await page.screenshot({ path: `screenshots/${name}-prep.png` });
await browser.close();
server.httpServer.close();
process.exit(0);
