// Screenshot a busy village (every building type, a wall run, one upgrade in progress): `node scripts/village-shot.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'village';
const server = await preview({ preview: { port: 4371, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const now = Date.now();
  let uid = 1;
  const b = (type, level, col, row, extra = {}) => ({ uid: uid++, type, level, col, row, upgradeEnds: null, lastCollect: now - 3600 * 1000, ...extra });
  const blds = [
    b('townhall', 4, 10, 4), b('coinmine', 3, 2, 1), b('coinmine', 2, 5, 1), b('sapwell', 3, 16, 1), b('sapwell', 2, 19, 1),
    b('vault', 2, 2, 5), b('builderhut', 1, 2, 9), b('barracks', 2, 14, 7), b('workshop', 2, 6, 7),
    b('shrine', 1, 18, 5), b('apiary', 1, 5, 4), b('weir', 1, 19, 9), b('market', 1, 15, 4, { upgradeEnds: now + 600 * 1000 }),
  ];
  for (let c = 9; c <= 13; c++) blds.push(b('wall', 1, c, 3));
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 3, l3: 3 }, village: { coins: 5000, glowsap: 3000, nextUid: uid, buildings: blds } }));
});
await page.goto('http://localhost:4371/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Village'));
await page.waitForTimeout(1800);
await page.screenshot({ path: `screenshots/${name}.png` });
const n = await page.evaluate(() => window.__game.scene.getScene('Village').v.buildings.length);
console.log(JSON.stringify({ buildings: n }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
