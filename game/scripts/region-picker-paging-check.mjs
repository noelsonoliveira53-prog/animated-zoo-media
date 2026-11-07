// Region picker paging: with a smaller page size (9), the picker opens on the current region's page and the real "<" / ">" buttons flip pages.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'picker-paging';
const server = await preview({ preview: { port: 4373, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 89; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4373/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 16 }));
await page.waitForTimeout(1200);
const first = await page.evaluate(() => {
  const m = window.__game.scene.getScene('WorldMap');
  m.constructor.PICKER_PER_PAGE = 9;
  m.openRegionPicker();
  return m.panel.getByName('pickerPage')?.text ?? null;
});
await page.waitForTimeout(300);
await page.screenshot({ path: `screenshots/${name}.png` });
// tap ">" (second button left of the title)
const pos = await page.evaluate(() => { const m = window.__game.scene.getScene('WorldMap'); const p = m.panel; const lbl = p.getByName('pickerPage'); return { x: p.x + lbl.x - 44, y: p.y + lbl.y }; });
await page.mouse.click(pos.x, pos.y);
await page.waitForTimeout(300);
const second = await page.evaluate(() => window.__game.scene.getScene('WorldMap').panel.getByName('pickerPage')?.text ?? null);
await page.screenshot({ path: `screenshots/${name}-p2.png` });
console.log(JSON.stringify({ first, second }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
