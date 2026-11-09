// Village zoom/pan check: taps the real Zoom button, drags to pan, taps a building (panel must stay unzoomed), zooms out.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'village-zoom';
const server = await preview({ preview: { port: 4335, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4335/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Village'));
await page.waitForTimeout(1200);
const cam = () => page.evaluate(() => { const c = window.__game.scene.getScene('Village').cameras.main; return { zoom: c.zoom, x: Math.round(c.scrollX), y: Math.round(c.scrollY) }; });
await page.screenshot({ path: `screenshots/${name}-1.png` });
await page.mouse.click(1280 - 100, 720 - 112); // Zoom in
await page.waitForTimeout(300);
const zoomed = await cam();
await page.screenshot({ path: `screenshots/${name}-2.png` });
// Drag on empty ground near the bottom-left of the grid to pan.
await page.mouse.move(400, 560);
await page.mouse.down();
for (let i = 1; i <= 10; i++) await page.mouse.move(400 + i * 20, 560 - i * 10);
await page.mouse.up();
await page.waitForTimeout(200);
const panned = await cam();
const panelAfterDrag = await page.evaluate(() => !!window.__game.scene.getScene('Village').panel);
// Tap the Town Hall where it now appears on screen.
const th = await page.evaluate(() => {
  const v = window.__game.scene.getScene('Village');
  const b = v.v.buildings.find((x) => x.type === 'townhall');
  const view = v.views.get(b.uid).img;
  const c = v.cameras.main;
  const wx = view.x + view.displayWidth / 2, wy = view.y + view.displayHeight / 2;
  return { x: (wx - c.worldView.x) * c.zoom, y: (wy - c.worldView.y) * c.zoom };
});
await page.mouse.click(th.x, th.y);
await page.waitForTimeout(400);
const panel = await page.evaluate(() => { const v = window.__game.scene.getScene('Village'); return v.panel ? { depth: v.panel.depth, hiddenFromMain: (v.panel.cameraFilter & v.cameras.main.id) !== 0 } : null; });
await page.screenshot({ path: `screenshots/${name}-3.png` });
await page.evaluate(() => window.__game.scene.getScene('Village').closePanel());
await page.mouse.click(1280 - 100, 720 - 112); // Zoom out
await page.waitForTimeout(300);
const out = await cam();
console.log(JSON.stringify({ zoomed, panned, panelAfterDrag, townHallTap: th, panel, out }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
