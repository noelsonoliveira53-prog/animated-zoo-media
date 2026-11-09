// Store hookup check: a save with store ranks starts a battle; the banner lists the bonuses and the sim applies them.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'store-perks';
const server = await preview({ preview: { port: 4401, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, store: { whetted: 5, warchest: 3, runes: 2, stew: 1 } }));
});
await page.goto('http://localhost:4401/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 1 }));
await page.waitForTimeout(1200);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  return { perks: s.perks, coins: s.sim.coins, startCoins: s.level.startCoins };
});
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
