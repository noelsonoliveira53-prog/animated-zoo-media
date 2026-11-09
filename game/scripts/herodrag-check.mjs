// Touch hero move (740×360 phone, real touch events over CDP): drag from the hero to a spot (screenshot mid-drag with
// the dashed trail and ring), lift: the hero is ordered there. A short tap on the hero still selects it.
// `node scripts/herodrag-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'herodrag';
const server = await preview({ preview: { port: 4358, strictPort: true } });
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const cdp = await ctx.newCDPSession(page);
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4358/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const toPage = (p) => page.evaluate((q) => { const r = window.__game.canvas.getBoundingClientRect(); return { x: r.left + (q.x * r.width) / 1280, y: r.top + (q.y * r.height) / 720 }; }, p);
const touch = async (type, p) => { const q = p ? await toPage(p) : null; await cdp.send('Input.dispatchTouchEvent', { type, touchPoints: q ? [{ x: q.x, y: q.y }] : [] }); };
const frames = async (ms) => { const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now); await page.waitForFunction(([t, d]) => window.__game.scene.getScene('Battle').time.now > t + d, [t0, ms], { timeout: 20000, polling: 'raf' }); };
const hero = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.paused = true; return { ...s.sim.hero.pos }; });
const grab = { x: hero.x, y: hero.y - 22 }; // the sprite stands above its feet
const target = { x: hero.x - 260, y: hero.y + 90 };
await touch('touchStart', grab);
await frames(120);
await touch('touchMove', { x: (grab.x + target.x) / 2, y: (grab.y + target.y) / 2 });
await frames(120);
await touch('touchMove', target);
await frames(300);
const mid = await page.evaluate(() => !!window.__game.scene.getScene('Battle').heroDrag);
await page.screenshot({ path: `screenshots/${name}.png` });
await touch('touchEnd');
await frames(150);
const ordered = await page.evaluate(() => { const h = window.__game.scene.getScene('Battle').sim.hero; return h.dest ? [Math.round(h.dest.x), Math.round(h.dest.y)] : null; });
// tap: selects
await touch('touchStart', grab);
await frames(80);
await touch('touchEnd');
await frames(150);
const selected = await page.evaluate(() => window.__game.scene.getScene('Battle').heroSelected);
const ok = mid && !!ordered && Math.abs(ordered[0] - target.x) < 3 && Math.abs(ordered[1] - target.y) < 3 && selected;
console.log(JSON.stringify({ mid, ordered, target: [Math.round(target.x), Math.round(target.y)], selected, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
