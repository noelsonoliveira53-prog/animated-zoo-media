// Trains a hero from the menu, then starts a battle and checks the village bonus banner.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'perks';
const server = await preview({ preview: { port: 4326, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  if (localStorage.getItem('grovewatch.save.v1')) return;
  const now = Date.now();
  const b = (uid, type, level, col, row) => ({ uid, type, level, col, row, upgradeEnds: null, lastCollect: now });
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({
    stars: { l1: 3 }, hero: 'fen',
    village: { coins: 2000, glowsap: 1500, nextUid: 20, buildings: [b(1, 'townhall', 3, 10, 5), b(2, 'workshop', 2, 2, 2), b(3, 'barracks', 1, 15, 8), b(4, 'builderhut', 1, 2, 10), b(5, 'vault', 2, 6, 8)] },
  }));
});
await page.goto('http://localhost:4326/');
await page.waitForTimeout(1000);
await page.mouse.click(1040 + 95, 470 + 152); // Train
await page.waitForTimeout(300);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
const rank = await page.evaluate(() => JSON.parse(localStorage.getItem('grovewatch.save.v1')).heroRanks);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 1 }));
await page.waitForTimeout(900);
await page.screenshot({ path: `screenshots/${name}-battle.png` });
const st = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle').sim; return { coins: s.coins, heroLv: s.hero.level, dmg: s.towerDamageMult, rangers: s.rangerMult }; });
console.log('ranks', JSON.stringify(rank), 'battle', JSON.stringify(st));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
