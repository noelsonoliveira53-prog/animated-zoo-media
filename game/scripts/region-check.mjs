// World map regions: locked arrow toast, then region 2 with progress; and a snowy battlefield.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'region';
const server = await preview({ preview: { port: 4327, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 3, l3: 2, l4: 2, l5: 1, l6: 2, l7: 2, l8: 1, l9: 2, l10: 1 }, hero: 'ember' })));
await page.goto('http://localhost:4327/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 0 }));
await page.waitForTimeout(700);
await page.screenshot({ path: `screenshots/${name}-r1.png` });
await page.evaluate(() => window.__game.scene.getScenes(true)[0].scene.start('WorldMap', { region: 2 }));
await page.waitForTimeout(800);
await page.screenshot({ path: `screenshots/${name}-r2.png` });
for (const i of [10, 11]) {
  await page.evaluate((idx) => window.__game.scene.getScenes(true)[0].scene.start('Battle', { levelIndex: idx }), i);
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `screenshots/${name}-level${i + 1}.png` });
}
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
