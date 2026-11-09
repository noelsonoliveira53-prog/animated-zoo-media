// Tower info card: builds a tower, taps it and screenshots the menu with its info card (stat bars with the
// next-level preview). `node scripts/towercard-check.mjs <name> [towerId] [slot] [tier]` (PHONE=1 for a phone)
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const [name = 'towercard', towerId = 'thornbow', slotArg = '3', tierArg = '0'] = process.argv.slice(2);
const server = await preview({ preview: { port: 4343, strictPort: true } });
const browser = await pw.chromium.launch();
const page = process.env.PHONE ? await (await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 })).newPage() : await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => { window.__noTouchTip = true; }); // the one-time touch tip card would cover the screen
await page.goto('http://localhost:4343/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const r = await page.evaluate(([id, slot, tier]) => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 5000;
  s.sim.build(slot, id);
  for (let i = 0; i < tier; i++) s.sim.upgrade(slot);
  s.openSlotMenu(slot);
  return { slots: s.level.slots.length };
}, [towerId, Number(slotArg), Number(tierArg)]);
const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 500, t0, { timeout: 20000, polling: 'raf' });
const card = await page.evaluate(() => { const c = window.__game.scene.getScene('Battle').menu?.getByName('towerCard'); if (!c) return null; const b = c.getBounds(); return { x: b.x, y: b.y, width: b.width, height: b.height, right: b.right, bottom: b.bottom }; });
await page.screenshot({ path: `screenshots/${name}.png` });
const inView = card && card.x >= 0 && card.y >= 0 && card.right <= 1280 && card.bottom <= 720;
console.log(JSON.stringify({ ...r, card: card && [Math.round(card.x), Math.round(card.y), Math.round(card.width), Math.round(card.height)], inView }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !inView ? 1 : 0);
