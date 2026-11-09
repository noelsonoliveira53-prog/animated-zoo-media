// Foes on their home map: `node scripts/foes-on-map.mjs <prefix> <levelIndex>:<enemy>[,<enemy>...] ...` (PHONE=1 for 740×360 touch)
// spawns each listed foe a little way along the road, pauses, and screenshots so their readability on the real ground can be judged.
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const [prefix = 'foes', ...specs] = process.argv.slice(2);
const server = await preview({ preview: { port: 4338, strictPort: true } });
const browser = await pw.chromium.launch();
const phone = !!process.env.PHONE;
const page = phone ? await (await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 })).newPage() : await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await page.addInitScript(() => { localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, seenStory: true })); window.__noTouchTip = true; });
await page.goto('http://localhost:4338/');
await page.waitForTimeout(1500);
for (const spec of specs) {
  const [idx, list] = spec.split(':');
  await page.evaluate((n) => { const g = window.__game; for (const s of g.scene.getScenes(true)) s.scene.stop(); g.scene.start('Battle', { levelIndex: +n }); }, idx);
  await page.waitForFunction(() => window.__game.scene.getScene('Battle')?.sys.isActive(), null, { timeout: 20000 });
  await page.waitForTimeout(1200);
  await page.evaluate((ids) => {
    const s = window.__game.scene.getScene('Battle');
    ids.forEach((id, k) => s.sim.spawn(id, 0, 480 + k * 110));
    s.sim.update(1 / 60);
    s.update(0, 16);
    s.children.getByName('banner')?.destroy();
    s.scene.pause();
  }, list.split(','));
  await page.waitForTimeout(300);
  await page.screenshot({ path: `screenshots/${prefix}-${idx}.png` });
}
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
