// Touch previews (740×360 phone, real touch events over CDP):
//  1. arm Starfall, press on the map: the aim appears above the finger with a foe count and nothing is cast yet;
//     drag, lift: the star is cast where the aim was.
//  2. arm Thornsnare, press, drag onto the spell bar and lift: cancelled, the spell stays armed and ready.
//  3. hold the hero skill button: the reach preview shows and the skill is NOT used; lift on it: used.
// `node scripts/touchaim-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'touchaim';
const server = await preview({ preview: { port: 4354, strictPort: true } });
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const cdp = await ctx.newCDPSession(page);
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => { window.__noTouchTip = true; }); // the one-time touch tip card would cover the screen
await page.goto('http://localhost:4354/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const toPage = (p) => page.evaluate((q) => { const r = window.__game.canvas.getBoundingClientRect(); return { x: r.left + (q.x * r.width) / 1280, y: r.top + (q.y * r.height) / 720 }; }, p);
const touch = async (type, p) => { const q = p ? await toPage(p) : null; await cdp.send('Input.dispatchTouchEvent', { type, touchPoints: q ? [{ x: q.x, y: q.y }] : [] }); };
const frames = async (ms) => { const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now); await page.waitForFunction(([t, d]) => window.__game.scene.getScene('Battle').time.now > t + d, [t0, ms], { timeout: 20000, polling: 'raf' }); };
const crowd = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const es = [s.sim.spawn('shellback', 0, 600), s.sim.spawn('mudling', 0, 620), s.sim.spawn('skitter', 0, 585)];
  s.sim.update(1 / 60);
  s.paused = true;
  s.armSpell('starfall');
  return { x: es[0].pos.x, y: es[0].pos.y };
});
// 1. press 60 px below the crowd (the aim floats 60 px above the finger), drag a little, lift
await touch('touchStart', { x: crowd.x - 30, y: crowd.y + 60 });
await frames(150);
await touch('touchMove', { x: crowd.x, y: crowd.y + 60 });
await frames(300);
const during = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { hold: s.aimHold, label: s.aimText.text, visible: s.aimText.visible, strikes: s.sim.strikes.length, ready: s.sim.spellReady('starfall') }; });
await page.screenshot({ path: `screenshots/${name}.png` });
await touch('touchEnd');
await frames(150);
const cast = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { strikes: s.sim.strikes.length, ready: s.sim.spellReady('starfall'), at: s.sim.strikes[0] && [Math.round(s.sim.strikes[0].pos.x), Math.round(s.sim.strikes[0].pos.y)] }; });
// 2. snare, drag onto the spell bar, lift: cancelled
await page.evaluate(() => window.__game.scene.getScene('Battle').armSpell('thornsnare'));
await touch('touchStart', { x: crowd.x, y: crowd.y + 60 });
await frames(150);
await touch('touchMove', { x: 1100, y: 690 });
await frames(150);
await touch('touchEnd');
await frames(150);
const cancel = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { armed: s.spellMode, ready: s.sim.spellReady('thornsnare') }; });
await page.evaluate(() => window.__game.scene.getScene('Battle').armSpell(null));
// 3. hero skill hold
await page.evaluate((c) => { const s = window.__game.scene.getScene('Battle'); const h = s.sim.hero; h.pos.x = c.x + 40; h.pos.y = c.y + 10; h.dest = null; }, crowd);
await touch('touchStart', { x: 58 + 104, y: 720 - 58 });
await frames(300);
const hold = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { preview: s.skillPreview, label: s.aimText.text, cd: s.sim.hero.skillCd }; });
await page.screenshot({ path: `screenshots/${name}-skill.png` });
await touch('touchEnd');
await frames(150);
const used = await page.evaluate(() => window.__game.scene.getScene('Battle').sim.hero.skillCd > 0);
const ok = during.hold && during.visible && /foe/.test(during.label) && during.strikes === 0 && cast.strikes === 1 && !cast.ready && cancel.armed === 'thornsnare' && cancel.ready && hold.preview && hold.cd === 0 && used;
console.log(JSON.stringify({ during, cast, cancel, hold, used, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
