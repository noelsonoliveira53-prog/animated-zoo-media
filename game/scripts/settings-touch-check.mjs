// Settings → touch options: clicks "Touch aim" (to Tap to cast) and "Show touch tips" (real clicks), checks the save,
// screenshots the screen; then on a phone with Tap to cast, a single tap on the map casts the armed spell at once.
// `node scripts/settings-touch-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'settings-touch';
const server = await preview({ preview: { port: 4362, strictPort: true } });
const browser = await pw.chromium.launch();
const errors = [];
const watch = (p) => { p.on('console', (m) => m.type() === 'error' && errors.push(m.text())); p.on('pageerror', (e) => errors.push(String(e))); };
// 1. desktop settings screen
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
watch(page);
await page.addInitScript(() => { if (!localStorage.getItem('grovewatch.save.v1')) localStorage.setItem('grovewatch.save.v1', JSON.stringify({ settings: { volume: 0.6, muted: true, music: false, touchTipSeen: true } })); });
await page.goto('http://localhost:4362/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Settings'));
await page.waitForTimeout(1200);
const pos = await page.evaluate(() => { const s = window.__game.scene.getScene('Settings'); const a = s.children.getByName('touchAimBtn'); const t = s.children.getByName('touchTipsBtn'); return { a: { x: a.x, y: a.y }, t: { x: t.x, y: t.y } }; });
await page.mouse.click(pos.a.x, pos.a.y);
await page.waitForTimeout(200);
await page.mouse.click(pos.t.x, pos.t.y);
await page.waitForTimeout(300);
const saved = await page.evaluate(() => { const s = JSON.parse(localStorage.getItem('grovewatch.save.v1')).settings; return { touchAim: s.touchAim, touchTipSeen: s.touchTipSeen }; });
const labels = await page.evaluate(() => { const s = window.__game.scene.getScene('Settings'); return [s.children.getByName('touchAimBtn').label.text, s.children.getByName('touchTipsBtn').label.text]; });
await page.screenshot({ path: `screenshots/${name}.png` });
await page.close();
// 2. phone battle with Tap to cast
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
const phone = await ctx.newPage();
watch(phone);
await phone.addInitScript(() => { window.__noTouchTip = true; localStorage.setItem('grovewatch.save.v1', JSON.stringify({ settings: { volume: 0.6, muted: true, music: false, touchAim: 'tap' } })); });
await phone.goto('http://localhost:4362/');
await phone.waitForTimeout(900);
await phone.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await phone.waitForTimeout(1500);
const at = await phone.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.paused = true; s.armSpell('starfall'); const r = window.__game.canvas.getBoundingClientRect(); return { x: r.left + (640 * r.width) / 1280, y: r.top + (380 * r.height) / 720, tap: s.touchAimTap }; });
await phone.touchscreen.tap(at.x, at.y);
await phone.waitForTimeout(400);
const cast = await phone.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { strikes: s.sim.strikes.length, held: s.aimHold }; });
const ok = saved.touchAim === 'tap' && saved.touchTipSeen === false && at.tap && cast.strikes === 1 && !cast.held;
console.log(JSON.stringify({ saved, labels, tapMode: at.tap, cast, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
