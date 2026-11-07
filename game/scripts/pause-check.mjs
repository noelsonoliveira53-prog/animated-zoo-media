// Opens the pause menu, toggles sound, resumes; screenshots the menu.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'pause';
const server = await preview({ preview: { port: 4325, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4325/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(800);
await page.mouse.click(1280 - 400, 40); // pause button
await page.waitForTimeout(300);
await page.mouse.click(640, 360 + 80); // sound toggle (3rd item at -60+140=80)
await page.waitForTimeout(200);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
const muted = await page.evaluate(() => JSON.parse(localStorage.getItem('grovewatch.save.v1')).settings.muted);
await page.mouse.click(640, 300); // resume
await page.waitForTimeout(300);
const paused = await page.evaluate(() => window.__game.scene.getScene('Battle').paused);
console.log('muted after toggle:', muted, 'paused after resume:', paused);
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !muted || paused ? 1 : 0);
