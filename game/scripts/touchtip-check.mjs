// Touch tip: on a phone (touch) the first battle shows the one-time gestures card and pauses; "Got it!" (a real tap)
// closes it, unpauses and remembers it, so the next battle starts without it. `node scripts/touchtip-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'touchtip';
const server = await preview({ preview: { port: 4360, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 })).newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4360/');
await page.waitForTimeout(900);
const start = () => page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await start();
await page.waitForTimeout(1800);
const first = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { card: !!s.children.getByName('touchTip'), paused: s.paused }; });
await page.screenshot({ path: `screenshots/${name}.png` });
// tap "Got it!" at its real screen position
const btn = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const c = s.children.getByName('touchTip');
  const b = c.list.find((o) => o.label?.text === 'Got it!');
  const m = b.getWorldTransformMatrix();
  const r = window.__game.canvas.getBoundingClientRect();
  return { x: r.left + (m.tx * r.width) / 1280, y: r.top + (m.ty * r.height) / 720 };
});
await page.touchscreen.tap(btn.x, btn.y);
await page.waitForTimeout(500);
const after = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { card: !!s.children.getByName('touchTip'), paused: s.paused, seen: JSON.parse(localStorage.getItem('grovewatch.save.v1')).settings.touchTipSeen }; });
await page.evaluate(() => window.__game.scene.getScene('Battle').scene.start('Menu'));
await page.waitForTimeout(800);
await start();
await page.waitForTimeout(1500);
const again = await page.evaluate(() => !!window.__game.scene.getScene('Battle').children.getByName('touchTip'));
const ok = first.card && first.paused && !after.card && !after.paused && after.seen === true && !again;
console.log(JSON.stringify({ first, after, again, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
