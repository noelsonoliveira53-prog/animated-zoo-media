// Swiftbloom check: a forced 3-star win grants a token (shown on the victory panel); in the Village, a building under
// construction is opened with a real click and the Swiftbloom button finishes it.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'swift';
const server = await preview({ preview: { port: 4325, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4325/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 0 }));
await page.waitForTimeout(2000);
await page.evaluate(() => window.__game.scene.getScene('Battle').endBattle(true));
await page.waitForTimeout(1900);
const panel = await page.evaluate(() => {
  const t = window.__game.scene.getScene('Battle').children.list.flatMap((o) => (o.list ? o.list : [o])).find((o) => o.name === 'bloomText');
  return { shown: !!t, blooms: JSON.parse(localStorage.getItem('grovewatch.save.v1')).village.swiftblooms };
});
await page.screenshot({ path: `screenshots/${name}-victory.png` });
// Start a Grove Hall upgrade, then open the village and rush it.
await page.evaluate(() => {
  const s = JSON.parse(localStorage.getItem('grovewatch.save.v1'));
  const hall = s.village.buildings.find((b) => b.type === 'townhall');
  hall.upgradeEnds = Date.now() + 50 * 60 * 1000; // 50 minutes left
  localStorage.setItem('grovewatch.save.v1', JSON.stringify(s));
  window.__game.scene.getScene('Battle').scene.start('Village');
});
await page.waitForTimeout(1500);
const hallXY = await page.evaluate(() => {
  const v = window.__game.scene.getScene('Village');
  const hall = v.v.buildings.find((b) => b.type === 'townhall');
  const p = v.cellToXY(hall.col, hall.row);
  return { x: p.x + 46, y: p.y + 46 };
});
await page.mouse.click(hallXY.x, hallXY.y);
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}.png` });
// Rush button: panel container at (GAME_W/2 - 60, GAME_H - 87); button at (W/2 - 150, 40) inside it.
await page.mouse.click(1280 / 2 - 60 + 320 - 150, 720 - 87 + 40);
await page.waitForTimeout(800);
const after = await page.evaluate(() => {
  const v = window.__game.scene.getScene('Village');
  const hall = v.v.buildings.find((b) => b.type === 'townhall');
  return { level: hall.level, building: hall.upgradeEnds !== null, blooms: v.v.swiftblooms };
});
await page.screenshot({ path: `screenshots/${name}-after.png` });
console.log(JSON.stringify({ panel, after }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !panel.shown || panel.blooms !== 1 || after.level !== 2 || after.blooms !== 0 ? 1 : 0);
