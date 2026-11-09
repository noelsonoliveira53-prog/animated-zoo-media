// Status icons: `node scripts/status-icons-check.mjs` — spawns foes with slow / haste / rage / anchor and a poisoned, stunned soldier,
// pauses, and screenshots a close-up so the icons can be checked beside (and without) the health bars.
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const server = await preview({ preview: { port: 4335, strictPort: true } });
const browser = await pw.chromium.launch();
const phone = !!process.env.PHONE; // PHONE=1: a 740×360 touch screen (icons draw bigger there)
const page = phone ? await (await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 })).newPage() : await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await page.addInitScript(() => { localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, seenStory: true })); window.__noTouchTip = true; });
await page.goto('http://localhost:4335/');
await page.waitForTimeout(1500);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 0 }));
await page.waitForFunction(() => window.__game.scene.getScene('Battle')?.sys.isActive(), null, { timeout: 20000 });
await page.waitForTimeout(800);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const a = s.sim.spawn('mudling', 0, 300);
  const b = s.sim.spawn('shellback', 0, 360);
  const c = s.sim.spawn('bogbrute', 0, 420);
  s.sim.slow(a, 0.5, 60);
  b.hasteTime = 60; b.hasteMult = 1.4; b.hp = b.maxHp * 0.6;
  s.sim.slow(b, 0.6, 60);
  c.speedMult = 1.5; c.anchored = true; c.hp = c.maxHp * 0.5;
  s.sim.update(1 / 60);
  s.update(0, 16);
  s.scene.pause();
  return [a, b, c].map((e) => ({ x: Math.round(e.pos.x), y: Math.round(e.pos.y) }));
});
await page.waitForTimeout(300);
const xs = info.map((p) => p.x), ys = info.map((p) => p.y);
const r = await page.evaluate(() => { const b = window.__game.canvas.getBoundingClientRect(); return { l: b.left, t: b.top, k: b.width / 1280 }; });
const sx = (v) => r.l + v * r.k, sy = (v) => r.t + v * r.k;
const clip = { x: sx(Math.min(...xs) - 90), y: sy(Math.max(0, Math.min(...ys) - 90)), width: 0, height: 0 };
clip.width = sx(Math.max(...xs) + 90) - clip.x;
clip.height = sy(Math.max(...ys) + 60) - clip.y;
await page.screenshot({ path: phone ? 'screenshots/fix-15-icons-phone.png' : 'screenshots/fix-13-icons.png', clip });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
