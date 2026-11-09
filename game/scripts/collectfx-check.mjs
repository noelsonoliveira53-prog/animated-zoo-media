// Collect feedback: in a busy village (an hour of production waiting), "Collect all" sends coin and glowsap icons
// arcing up to the HUD; screenshots them mid-flight (tweens paused) and checks they all land and are cleaned up.
// `node scripts/collectfx-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'collectfx';
const server = await preview({ preview: { port: 4366, strictPort: true } });
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
await page.addInitScript(() => { window.__noTouchTip = true; }); // the one-time touch tip card would cover the screen
await page.goto('http://localhost:4366/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Village'));
await page.waitForTimeout(1800);
const before = await page.evaluate(() => window.__game.scene.getScene('Village').v.coins);
await page.evaluate(() => window.__game.scene.getScene('Village').collectEverything());
const t0 = await page.evaluate(() => window.__game.scene.getScene('Village').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Village').time.now > t + 300, t0, { timeout: 20000, polling: 'raf' });
await page.evaluate(() => window.__game.scene.getScene('Village').tweens.pauseAll());
const flying = await page.evaluate(() => window.__game.scene.getScene('Village').children.list.filter((o) => o.type === 'Image' && (o.texture.key === 'icon_coin' || o.texture.key === 'icon_sap') && o.depth === 940).length);
await page.screenshot({ path: `screenshots/${name}.png` });
await page.evaluate(() => window.__game.scene.getScene('Village').tweens.resumeAll());
await page.waitForFunction(() => window.__game.scene.getScene('Village').children.list.filter((o) => o.depth === 940).length === 0, null, { timeout: 60000, polling: 'raf' });
const after = await page.evaluate(() => window.__game.scene.getScene('Village').v.coins);
const ok = flying > 0 && after > before;
console.log(JSON.stringify({ flying, coins: [before, after], ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
