// Settings check: the Effects High/Low toggle saves, and a battle with Effects: Low runs clean.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'settings-fx';
const server = await preview({ preview: { port: 4400, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4400/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Settings'));
await page.waitForTimeout(700);
await page.mouse.click(515, 464);
await page.waitForTimeout(300);
await page.screenshot({ path: `screenshots/${name}.png` });
const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('grovewatch.save.v1')).settings.fxLow);
await page.evaluate(() => window.__game.scene.getScene('Settings').scene.start('Battle', { levelIndex: 0 }));
await page.waitForTimeout(1200);
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 9999;
  s.sim.build(0, 'thornbow'); s.sim.upgrade(0); s.sim.upgrade(0);
  s.sim.build(1, 'boulder');
  s.sim.status = 'running';
  for (let k = 0; k < 8; k++) s.sim.spawn('mudling', 0, 60 + k * 40);
});
await page.waitForTimeout(1500);
console.log(JSON.stringify({ saved }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
