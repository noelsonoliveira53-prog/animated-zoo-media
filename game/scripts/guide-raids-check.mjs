// Field Guide "Raids" tab: 6 troops + 7 camp buildings, detail pages for the Otter and the Sludge Pit, desktop and phone.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'guide-raids';
const server = await preview({ preview: { port: 4366, strictPort: true } });
const browser = await pw.chromium.launch();
const errors = [];
for (const [suffix, opts] of [['', { viewport: { width: 1280, height: 720 } }], ['-phone', { viewport: { width: 740, height: 360 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }]]) {
  const ctx = await browser.newContext(opts);
  const page = await ctx.newPage();
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto('http://localhost:4366/');
  await page.waitForTimeout(1000);
  await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('FieldGuide', { tab: 'raids' }));
  await page.waitForTimeout(900);
  const n = await page.evaluate(() => {
    const g = window.__game.scene.getScene('FieldGuide');
    const all = g.entries();
    g.showDetail(all.find((e) => e.key === (location.hash === '#b' ? 'camp_sludge' : 'troop_otter')));
    return all.length;
  });
  await page.waitForTimeout(400);
  await page.screenshot({ path: `screenshots/${name}${suffix}.png` });
  await page.evaluate(() => { const g = window.__game.scene.getScene('FieldGuide'); g.showDetail(g.entries().find((e) => e.key === 'camp_sludge')); });
  await page.waitForTimeout(300);
  await page.screenshot({ path: `screenshots/${name}${suffix}-camp.png` });
  console.log(suffix || 'desktop', 'entries', n);
  await ctx.close();
}
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
