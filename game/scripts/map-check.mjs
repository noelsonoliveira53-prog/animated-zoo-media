// Screenshots the menu, world map (with some progress), a level card, and each later level's battlefield.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try {
  pw = require('playwright');
} catch {
  pw = require(execSync('npm root -g').toString().trim() + '/playwright');
}
const name = process.argv[2] ?? 'map';
const server = await preview({ preview: { port: 4322, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 2 }, hero: 'ember' })));
await page.goto('http://localhost:4322/');
await page.waitForTimeout(1000);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
await page.mouse.click(460, 420); // Campaign
await page.waitForTimeout(700);
await page.screenshot({ path: `screenshots/${name}-world.png` });
await page.mouse.click(600, 330); // level 3 node
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}-card.png` });
await page.mouse.click(640 + 260 - 110, 360 + 20 + 165 - 44); // Play
await page.waitForTimeout(1200);
const scene = await page.evaluate(() => window.__game.scene.getScenes(true).map((s) => s.scene.key));
console.log('active scenes after Play:', scene.join(','));
for (const i of [2, 3, 4]) {
  await page.evaluate((idx) => {
    const active = window.__game.scene.getScenes(true)[0];
    active.scene.start('Battle', { levelIndex: idx });
  }, i);
  await page.waitForTimeout(1200);
  await page.screenshot({ path: `screenshots/${name}-level${i + 1}.png` });
}
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
