// Field Guide spells tab check: opens the guide, taps the real "Spells" tab, taps Thornsnare, screenshots.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'guide-spells';
const server = await preview({ preview: { port: 4329, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4329/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('FieldGuide'));
await page.waitForTimeout(800);
await page.mouse.click(1280 - 568 + 3 * 124, 44); // Spells tab (5 tabs since the Raids tab was added)
await page.waitForTimeout(400);
const tab = await page.evaluate(() => window.__game.scene.getScene('FieldGuide').tab);
await page.screenshot({ path: `screenshots/${name}-1.png` });
await page.mouse.click(90 + 2 * 98 + 49, 130 + 49 - 10);
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}-2.png` });
console.log('tab', tab);
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
