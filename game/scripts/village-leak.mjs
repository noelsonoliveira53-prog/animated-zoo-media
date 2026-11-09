// Village leak check: counts live objects and tweens after 2 s and 22 s idle (chimney smoke, tree sway).
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const server = await preview({ preview: { port: 4372, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const now = Date.now();
  const b = (uid, type, level, col, row) => ({ uid, type, level, col, row, upgradeEnds: null, lastCollect: now });
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ village: { coins: 100, glowsap: 100, nextUid: 9, buildings: [b(1, 'townhall', 3, 10, 5), b(2, 'coinmine', 2, 3, 2), b(3, 'barracks', 1, 15, 7), b(4, 'workshop', 1, 5, 8), b(5, 'builderhut', 1, 2, 10)] } }));
});
await page.goto('http://localhost:4372/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Village'));
const count = () => page.evaluate(() => { const s = window.__game.scene.getScene('Village'); return { objects: s.children.list.length, tweens: s.tweens.getTweens().length, frame: window.__game.loop.frame }; });
await page.waitForTimeout(2000);
const early = await count();
await page.waitForTimeout(20000);
const later = await count();
console.log(JSON.stringify({ early, later }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no page errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || later.objects > early.objects + 40 ? 1 : 0);
