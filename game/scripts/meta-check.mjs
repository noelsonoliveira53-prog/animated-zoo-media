// Field Guide (enemies + towers tabs) and Settings (slider, mute, reset confirm) with real clicks.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'meta';
const server = await preview({ preview: { port: 4332, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await page.addInitScript(() => {
  if (!localStorage.getItem('grovewatch.save.v1'))
    localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, seenEnemies: ['mudling', 'skitter', 'shellback', 'gloomwing', 'bogmender', 'murkmaw', 'rimewraith'] }));
});
await page.goto('http://localhost:4332/');
await page.waitForTimeout(900);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
await page.mouse.click(240, 662); // Field Guide
await page.waitForTimeout(600);
await page.mouse.click(90 + 98 * 5 + 49, 130 + 49 - 10); // 6th entry (murkmaw? order of ENEMIES)
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}-guide.png` });
await page.mouse.click(1280 - 420 + 140, 44); // Towers tab
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}-towers.png` });
await page.mouse.click(90, 44); // Back
await page.waitForTimeout(500);
await page.mouse.click(680, 662); // Settings
await page.waitForTimeout(500);
await page.mouse.click(640 - 220 + 440 * 0.3, 220); // volume 30%
await page.mouse.click(640 - 125, 320); // mute
await page.mouse.click(640, 470); // reset (arm)
await page.waitForTimeout(300);
await page.screenshot({ path: `screenshots/${name}-settings.png` });
const s = await page.evaluate(() => JSON.parse(localStorage.getItem('grovewatch.save.v1')).settings);
console.log('settings', JSON.stringify(s));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
