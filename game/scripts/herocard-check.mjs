// Hero info card: taps the hero portrait (a real tap) and screenshots the card; then a fallen hero's card.
// `node scripts/herocard-check.mjs <name> [heroId]` (PHONE=1 for a 740×360 phone)
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const [name = 'herocard', heroId = 'fen'] = process.argv.slice(2);
const server = await preview({ preview: { port: 4345, strictPort: true } });
const browser = await pw.chromium.launch();
const phone = !!process.env.PHONE;
const page = phone ? await (await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 })).newPage() : await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript((h) => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 3, l3: 3 }, hero: h })), heroId);
await page.addInitScript(() => { window.__noTouchTip = true; }); // the one-time touch tip card would cover the screen
await page.goto('http://localhost:4345/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
await page.evaluate(() => { const h = window.__game.scene.getScene('Battle').sim.hero; h.xp = 70; h.level = 2; });
// tap the portrait (bottom-left), mapped from game to page coordinates
const tap = await page.evaluate(() => { const r = window.__game.canvas.getBoundingClientRect(); return { x: r.left + (58 * r.width) / 1280, y: r.top + ((720 - 52) * r.height) / 720 }; });
if (phone) await page.touchscreen.tap(tap.x, tap.y); else await page.mouse.click(tap.x, tap.y);
let t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 400, t0, { timeout: 20000, polling: 'raf' });
const r = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const c = s.heroCard;
  if (!c) return { open: false };
  const b = c.getBounds();
  return { open: true, hero: s.sim.hero.def.id, x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), inView: b.x >= 0 && b.y >= 64 && b.right <= 1280 && b.bottom <= 720 - 100 };
});
await page.screenshot({ path: `screenshots/${name}.png` });
// fallen hero: the card shows the respawn countdown and closes on its own
const dead = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.toggleHeroCard(false); const h = s.sim.hero; h.alive = false; h.hp = 0; h.respawnTimer = 12; s.toggleHeroCard(true); return s.heroCard.list.some((o) => o.type === 'Text' && /back in/.test(o.text)); });
t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 12000, t0, { timeout: 90000, polling: 'raf' });
const closed = await page.evaluate(() => window.__game.scene.getScene('Battle').heroCard === null);
console.log(JSON.stringify({ ...r, dead, closed }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !r.open || !r.inView || !dead || !closed ? 1 : 0);
