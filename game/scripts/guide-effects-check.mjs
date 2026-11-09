// Field Guide Effects tab: opens it, steps through all six effects (checks each detail page fits the parchment),
// and screenshots one live preview. `node scripts/guide-effects-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'guide-effects';
const server = await preview({ preview: { port: 4336, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4336/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('FieldGuide', { tab: 'effects' }));
await page.waitForTimeout(1500);
const pages = await page.evaluate(() => {
  const s = window.__game.scene.getScene('FieldGuide');
  const out = [];
  for (const e of s.entries()) {
    s.showDetail(e);
    let bottom = 0;
    for (const o of s.detail.list) if (o.getBounds) bottom = Math.max(bottom, o.getBounds().bottom);
    out.push({ key: e.key, bottom: Math.round(bottom) });
  }
  s.showDetail(s.entries().find((e) => e.key === 'stun'));
  return out;
});
await page.waitForTimeout(900);
await page.screenshot({ path: `screenshots/${name}.png` });
const fits = pages.every((p) => p.bottom <= 690);
console.log(JSON.stringify({ pages, fits }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !fits ? 1 : 0);
