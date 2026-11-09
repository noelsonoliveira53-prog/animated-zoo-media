// Phone consistency tour: `node scripts/phone-tour.mjs <prefix>` → menu, world map, battle (levels 1 and 34), settings at 740×360 touch.
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const prefix = process.argv[2] ?? 'phone';
const server = await preview({ preview: { port: 4334, strictPort: true } });
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await page.addInitScript(() => { localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 2 }, seenStory: true })); window.__noTouchTip = true; });
await page.goto('http://localhost:4334/');
await page.waitForTimeout(1800);
const go = async (key, data) => {
  await page.evaluate(([k, d]) => {
    const g = window.__game;
    const cur = g.scene.getScene(k);
    if (cur?.sys.isActive()) { cur.scene.restart(d); return; } // same scene again: restart it with the new data
    for (const s of g.scene.getScenes(true)) s.scene.stop();
    g.scene.start(k, d);
  }, [key, data]);
  await page.waitForFunction((k) => window.__game.scene.getScene(k)?.sys.isActive(), key, { timeout: 20000 });
  await page.waitForTimeout(2200);
};
await page.screenshot({ path: `screenshots/${prefix}-menu.png` });
await go('WorldMap', {}); await page.screenshot({ path: `screenshots/${prefix}-map.png` });
await go('Battle', { levelIndex: 0 }); await page.screenshot({ path: `screenshots/${prefix}-battle1.png` });
await go('Battle', { levelIndex: 33 }); await page.screenshot({ path: `screenshots/${prefix}-battle34.png` });
await go('Settings', {}); await page.screenshot({ path: `screenshots/${prefix}-settings.png` });
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
