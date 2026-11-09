// Tower build menu: with 100 coins (some towers affordable, some not) opens the build ring on an empty pad and
// screenshots a close-up once the buttons have popped in. `node scripts/towermenu-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'towermenu';
const server = await preview({ preview: { port: 4342, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4342/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const pos = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.sim.coins = 100; return s.level.slots[3]; });
await page.mouse.click(pos.x, pos.y); // a real tap opens the build ring
const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 600, t0, { timeout: 20000, polling: 'raf' });
const r = await page.evaluate(() => ({ open: !!window.__game.scene.getScene('Battle').menu }));
await page.screenshot({ path: `screenshots/${name}.png`, clip: { x: pos.x - 130, y: pos.y - 130, width: 260, height: 260 } });
console.log(JSON.stringify(r));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !r.open ? 1 : 0);
