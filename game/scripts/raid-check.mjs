// Opens the raid panel, trains troops with real clicks, attacks the easy camp, deploys, and plays it out.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'raid';
const server = await preview({ preview: { port: 4330, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
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
await page.goto('http://localhost:4330/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Village'));
await page.waitForTimeout(800);
await page.mouse.click(100, 720 - 44); // Raid
await page.waitForTimeout(400);
// Train: brawler x6, slinger x4, sapper x3 (+1 buttons at x+92,y+34 for each card)
// Cards share the 1060px row evenly (5 troop types → 212px steps); the +1 button sits near each card's right edge.
const step = (1120 - 60) / 5;
const card = (i) => ({ x: 640 - 560 + 30 + step / 2 + i * step + (step - 8) / 2 - 38, y: 380 - 260 + 160 + 74 });
for (let k = 0; k < 6; k++) await page.mouse.click(card(0).x, card(0).y);
for (let k = 0; k < 4; k++) await page.mouse.click(card(1).x, card(1).y);
for (let k = 0; k < 3; k++) await page.mouse.click(card(2).x, card(2).y);
await page.waitForTimeout(700);
await page.screenshot({ path: `screenshots/${name}-prep.png` });
// Training takes real time now: fast-forward the queue so the raid can start.
await page.evaluate(() => {
  const s = JSON.parse(localStorage.getItem('grovewatch.save.v1'));
  for (const q of s.trainQueue) q.endsAt = 0;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify(s));
});
await page.mouse.click(100, 720 - 44); // reopen Raid panel so it reloads the save
await page.waitForTimeout(700);
const army = await page.evaluate(() => JSON.parse(localStorage.getItem('grovewatch.save.v1')).army);
console.log('army', JSON.stringify(army));
await page.mouse.click(640 - 560 + 30 + 175 + 360 + 90, 380 + 150 + 44); // Attack medium camp
await page.waitForTimeout(900);
// Deploy from the left edge, then right edge.
for (let k = 0; k < 8; k++) await page.mouse.click(70, 160 + k * 55);
await page.mouse.click(640 - 110 * 1.5 + 65 + 110 * 2 - 110, 720 - 50); // pick 3rd troop button approx
for (let k = 0; k < 6; k++) await page.mouse.click(1220, 180 + k * 70);
// Headless rendering is slow, so fast-forward the sim 15s before the mid-raid screenshot.
await page.evaluate(() => { const s = window.__game.scene.getScene('Raid'); for (let i = 0; i < 450 && !s.sim.ended; i++) s.sim.update(1 / 30); });
await page.waitForTimeout(800);
await page.screenshot({ path: `screenshots/${name}-battle.png` });
await page.evaluate(() => { const s = window.__game.scene.getScene('Raid'); for (let i = 0; i < 2400 && !s.sim.ended; i++) s.sim.update(1 / 30); });
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-result.png` });
const after = await page.evaluate(() => { const s = JSON.parse(localStorage.getItem('grovewatch.save.v1')); return { army: s.army, coins: Math.floor(s.village.coins), sap: Math.floor(s.village.glowsap), seed: s.raidSeed }; });
console.log('after', JSON.stringify(after));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
