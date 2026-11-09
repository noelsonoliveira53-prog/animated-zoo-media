// Boss intro: spawns a boss and screenshots the nameplate once it has slid in (tweens paused).
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'bossintro';
const server = await preview({ preview: { port: 4339, strictPort: true } });
const browser = await pw.chromium.launch();
// PHONE=1: a 740×360 touch phone instead of desktop
const page = process.env.PHONE ? await (await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 })).newPage() : await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4339/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 64 }));
await page.waitForTimeout(1500);
const t0 = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.sim.spawn('zephyrax', 0, 200); return s.time.now; });
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 700, t0, { timeout: 20000, polling: 'raf' });
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.pauseAll());
await page.screenshot({ path: `screenshots/${name}.png` });
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.resumeAll());
await page.waitForTimeout(4000);
const left = await page.evaluate(() => window.__game.scene.getScene('Battle').children.list.filter((o) => o.depth === 4000 || o.depth === 3990).length);
console.log(JSON.stringify({ leftover: left }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
