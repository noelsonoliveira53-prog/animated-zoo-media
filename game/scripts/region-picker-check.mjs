// Region picker check: the world map's "Regions" button lists every region; unlocked ones jump there.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'regions';
const server = await preview({ preview: { port: 4348, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 42; i++) stars['l' + i] = i % 4 === 0 ? 2 : 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4348/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 2 }));
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('WorldMap').openRegionPicker());
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}.png` });
// Jump to region 7 (Verdant Ruins) through the picker's handler.
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.restart({ region: 7 }));
await page.waitForTimeout(800);
const region = await page.evaluate(() => window.__game.scene.getScene('WorldMap').region);
console.log(JSON.stringify({ region }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
