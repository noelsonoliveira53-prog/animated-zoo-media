// Enemy info card: spawns a foe, taps it (a real tap), screenshots the card following it, then checks it updates,
// that tapping empty ground closes it, and that a flyer can be tapped on its lifted body.
// `node scripts/enemycard-check.mjs <name> [enemyId] [flyerId]` (PHONE=1 for a 740×360 phone)
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const [name = 'enemycard', enemyId = 'shellback', flyerId = 'gloomwing'] = process.argv.slice(2);
const server = await preview({ preview: { port: 4349, strictPort: true } });
const browser = await pw.chromium.launch();
const phone = !!process.env.PHONE;
const page = phone ? await (await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 })).newPage() : await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => { window.__noTouchTip = true; }); // the one-time touch tip card would cover the screen
await page.goto('http://localhost:4349/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
// game → page coordinates from the canvas's real box
const toPage = (p) => page.evaluate((q) => { const r = window.__game.canvas.getBoundingClientRect(); return { x: r.left + (q.x * r.width) / 1280, y: r.top + (q.y * r.height) / 720 }; }, p);
const tap = async (p) => { const q = await toPage(p); if (phone) await page.touchscreen.tap(q.x, q.y); else await page.mouse.click(q.x, q.y); };
const pos = await page.evaluate(([id, fid]) => {
  const s = window.__game.scene.getScene('Battle');
  const e = s.sim.spawn(id, 0, 520);
  const f = s.sim.spawn(fid, 0, 760);
  s.sim.update(1 / 60);
  s.paused = true; // hold them still so the taps land
  e.hp = e.maxHp * 0.6;
  window.__eu = [e.uid, f.uid];
  return { e: { x: e.pos.x, y: e.pos.y }, f: { x: f.pos.x, y: f.pos.y - 34 } };
}, [enemyId, flyerId]);
let t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 300, t0, { timeout: 20000, polling: 'raf' });
await tap(pos.e);
t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 400, t0, { timeout: 20000, polling: 'raf' });
const first = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); const c = s.enemyCard; if (!c) return null; const b = c.getBounds(); return { uid: s.enemyCardUid === window.__eu[0], hp: c.getData('hp').text, inView: b.x >= 0 && b.y >= 60 && b.right <= 1280 && b.bottom <= 720 }; });
await page.screenshot({ path: `screenshots/${name}.png` });
// live: damage it and the hp text follows
const live = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); const e = s.sim.enemies.find((x) => x.uid === window.__eu[0]); e.hp = e.maxHp * 0.3; s.updateEnemyCard(0.016); return s.enemyCard.getData('hp').text; });
// flyer: tap its lifted body
await tap(pos.f);
await page.waitForTimeout(300);
const flyerInfo = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { uid: s.enemyCardUid, want: window.__eu[1], menu: !!s.menu, f: s.sim.enemies.find((x) => x.uid === window.__eu[1])?.pos }; });
const flyer = flyerInfo.uid === flyerInfo.want;
// empty ground closes it, and so does opening a tower menu (one card at a time)
await tap({ x: 1000, y: 240 });
await page.waitForTimeout(300);
const closed = await page.evaluate(() => window.__game.scene.getScene('Battle').enemyCard === null);
await tap(pos.e);
await page.waitForTimeout(300);
const reopened = await page.evaluate(() => !!window.__game.scene.getScene('Battle').enemyCard);
await page.evaluate(() => window.__game.scene.getScene('Battle').openSlotMenu(0));
const slotCloses = await page.evaluate(() => window.__game.scene.getScene('Battle').enemyCard === null);
const ok = reopened && slotCloses && !!first?.uid && first.inView && live !== first.hp && flyer && closed;
console.log(JSON.stringify({ first, live, flyer, closed, reopened, slotCloses, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
