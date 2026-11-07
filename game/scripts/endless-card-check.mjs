// Level card check: on a beaten level, the Endless line shows the best run, today's mutator and the wave-10 home boss.
// Desktop and phone (740×360 touch) screenshots. `node scripts/endless-card-check.mjs <name>`.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'endless-card';
const server = await preview({ preview: { port: 4364, strictPort: true } });
const browser = await pw.chromium.launch();
const errors = [];
for (const [suffix, opts] of [['', { viewport: { width: 1280, height: 720 } }], ['-phone', { viewport: { width: 740, height: 360 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }]]) {
  const ctx = await browser.newContext(opts);
  const page = await ctx.newPage();
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.addInitScript(() => {
    const stars = {};
    for (let i = 1; i <= 80; i++) stars['l' + i] = 3;
    localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars, endlessBest: { l78: 17 } }));
  });
  await page.goto('http://localhost:4364/');
  await page.waitForTimeout(1000);
  await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 15 }));
  await page.waitForTimeout(1200);
  const info = await page.evaluate(() => {
    const m = window.__game.scene.getScene('WorldMap');
    m.openPanel(77);
    return m.panel.getByName('endlessInfo')?.text ?? null;
  });
  await page.waitForTimeout(500);
  await page.screenshot({ path: `screenshots/${name}${suffix}.png` });
  console.log(suffix || 'desktop', JSON.stringify(info));
  await ctx.close();
}
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
