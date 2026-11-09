// Pause menu: opens the pause panel mid-battle and screenshots it once the buttons have popped in.
// `node scripts/pause-check.mjs <name>` (PHONE=1 for a 740×360 touch phone)
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'pause';
const server = await preview({ preview: { port: 4340, strictPort: true } });
const browser = await pw.chromium.launch();
const page = process.env.PHONE ? await (await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 })).newPage() : await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => { window.__noTouchTip = true; }); // the one-time touch tip card would cover the screen
await page.goto('http://localhost:4340/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 3 }));
await page.waitForTimeout(1500);
const t0 = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.togglePause(); return s.time.now; });
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 600, t0, { timeout: 20000, polling: 'raf' });
await page.screenshot({ path: `screenshots/${name}.png` });
// closing it again should leave nothing behind
const left = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.togglePause(); return s.children.list.filter((o) => o.name === 'pauseMenu').length; });
console.log(JSON.stringify({ leftover: left }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
