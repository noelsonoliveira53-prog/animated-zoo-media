// One card at a time: open the hero card, then tap a tower — the hero card closes and the tower card opens
// (and the hero is no longer waiting for a move order). `node scripts/cards-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'cards';
const server = await preview({ preview: { port: 4347, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4347/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const slot = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.sim.coins = 500; s.sim.build(1, 'thornbow'); return s.level.slots[1]; });
await page.mouse.click(58, 668); // portrait
await page.waitForTimeout(400);
const before = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { heroCard: !!s.heroCard, selected: s.heroSelected }; });
await page.mouse.click(slot.x, slot.y); // the tower
const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 500, t0, { timeout: 20000, polling: 'raf' });
const after = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { heroCard: !!s.heroCard, selected: s.heroSelected, towerCard: !!s.menu?.getByName('towerCard') }; });
await page.screenshot({ path: `screenshots/${name}.png` });
const ok = before.heroCard && before.selected && !after.heroCard && !after.selected && after.towerCard;
console.log(JSON.stringify({ before, after, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
