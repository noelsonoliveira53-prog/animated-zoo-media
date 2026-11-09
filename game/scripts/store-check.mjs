// Store scene check: opens the Store from the menu with a funded village, buys a Whetted Tips rank with the real
// Buy button, checks the purse and rank changed, then screenshots the shop.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'store';
const server = await preview({ preview: { port: 4402, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const now = Date.now();
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({
    stars: { l1: 3 },
    store: { whetted: 2, warchest: 2 },
    village: { coins: 5000, glowsap: 5000, nextUid: 5, buildings: [{ uid: 1, type: 'townhall', level: 5, col: 10, row: 5, upgradeEnds: null, lastCollect: now }, { uid: 2, type: 'vault', level: 3, col: 2, row: 2, upgradeEnds: null, lastCollect: now }] },
  }));
});
await page.goto('http://localhost:4402/');
await page.waitForTimeout(1000);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
await page.mouse.click(140, 435);
await page.waitForTimeout(800);
const before = await page.evaluate(() => { const s = JSON.parse(localStorage.getItem('grovewatch.save.v1')); return { coins: s.village.coins, rank: s.store.whetted }; });
await page.evaluate(() => {
  const st = window.__game.scene.getScene('Store');
  const find = (list) => { for (const o of list) { if (o.name === 'buy_whetted') return o; if (o.list) { const f = find(o.list); if (f) return f; } } return null; };
  find(st.children.list).emit('pointerdown', null, 0, 0, { stopPropagation() {} });
});
await page.waitForTimeout(450);
await page.screenshot({ path: `screenshots/${name}-buy.png` });
await page.waitForTimeout(900);
const after = await page.evaluate(() => { const s = JSON.parse(localStorage.getItem('grovewatch.save.v1')); return { coins: s.village.coins, rank: s.store.whetted }; });
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify({ scene: await page.evaluate(() => window.__game.scene.isActive('Store')), before, after }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
