// Battle-map screenshots: `node scripts/maps-shot.mjs <prefix> <levelIndex...>` → screenshots/<prefix>-<index>.png (map at rest, HUD included).
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const [prefix = 'map', ...idx] = process.argv.slice(2);
const server = await preview({ preview: { port: 4333, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await page.addInitScript(() => { localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, seenStory: true })); window.__noTouchTip = true; });
await page.goto('http://localhost:4333/');
await page.waitForTimeout(1500);
for (const i of idx.length ? idx : ['0']) {
  await page.evaluate((n) => { const g = window.__game; for (const s of g.scene.getScenes(true)) if (s.sys.settings.key !== 'Battle') s.scene.stop(); g.scene.start('Battle', { levelIndex: +n }); }, i);
  await page.waitForFunction(() => window.__game.scene.getScene('Battle')?.sys.isActive(), null, { timeout: 20000 });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `screenshots/${prefix}-${i}.png` });
}
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
