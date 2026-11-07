// Visits the village: collects, opens a panel, upgrades, opens the shop, places a building.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try {
  pw = require('playwright');
} catch {
  pw = require(execSync('npm root -g').toString().trim() + '/playwright');
}
const name = process.argv[2] ?? 'village';
const server = await preview({ preview: { port: 4324, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4324/');
await page.waitForTimeout(1000);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
await page.mouse.click(460, 480); // Village
await page.waitForTimeout(800);
// Age the producers so there is something to collect.
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Village');
  for (const b of s.v.buildings) b.lastCollect -= 40 * 60 * 1000;
  s.v.coins = 1800;
  s.v.glowsap = 1800;
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}-home.png` });
const mine = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Village');
  const b = s.v.buildings.find((x) => x.type === 'coinmine');
  return { x: 128 + b.col * 46 + 46, y: 92 + b.row * 46 + 46 };
});
await page.mouse.click(mine.x, mine.y); // collect + panel
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}-panel.png` });
await page.mouse.click(640 - 60 + 320 - 150, 720 - 87 + 36); // Upgrade
await page.waitForTimeout(400);
await page.mouse.click(1280 - 100, 720 - 44); // Build
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}-shop.png` });
await page.mouse.click(640 - 550 + 30 + 73 + 4 * 152, 420); // Defense Workshop card
await page.waitForTimeout(300);
await page.mouse.move(1010, 330);
await page.waitForTimeout(150);
await page.mouse.click(1010, 330);
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}-placed.png` });
const st = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Village');
  return { coins: Math.floor(s.v.coins), sap: Math.floor(s.v.glowsap), buildings: s.v.buildings.map((b) => `${b.type}:${b.level}${b.upgradeEnds ? '*' : ''}`) };
});
console.log('village', JSON.stringify(st));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
