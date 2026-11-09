// World map progress ribbon: with a few stars saved, checks the region bar text and the "Next:" pill, taps the pill
// (a real tap) and checks it opens that level's card; screenshots the ribbon. `node scripts/mapprogress-check.mjs <name>`
// (PHONE=1 for a 740×360 touch phone)
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'mapprogress';
const server = await preview({ preview: { port: 4365, strictPort: true } });
const browser = await pw.chromium.launch();
const phone = !!process.env.PHONE;
const page = phone ? await (await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 })).newPage() : await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 2 }, settings: { volume: 0.6, muted: true, music: false } })));
await page.goto('http://localhost:4365/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 0 }));
await page.waitForTimeout(1600);
const info = await page.evaluate(() => { const s = window.__game.scene.getScene('WorldMap'); const p = s.children.getByName('nextPill'); return { stars: s.children.getByName('regionStars')?.text, next: p?.list.find((o) => o.type === 'Text')?.text, pill: p ? { x: p.x, y: p.y } : null }; });
await page.screenshot({ path: `screenshots/${name}.png` });
const q = await page.evaluate((p) => { const r = window.__game.canvas.getBoundingClientRect(); return { x: r.left + (p.x * r.width) / 1280, y: r.top + (p.y * r.height) / 720 }; }, info.pill);
if (phone) await page.touchscreen.tap(q.x, q.y); else await page.mouse.click(q.x, q.y);
await page.waitForTimeout(600);
const opened = await page.evaluate(() => { const s = window.__game.scene.getScene('WorldMap'); return s.children.list.some((o) => o.list?.some?.((c) => c.type === 'Text' && c.text?.startsWith('3. '))); });
const ok = info.stars === '5/15 here' && /^Next: 3\. /.test(info.next ?? '') && opened;
console.log(JSON.stringify({ ...info, opened, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
