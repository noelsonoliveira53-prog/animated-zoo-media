// Opens a maxed tower's menu, buys a specialization with two taps, then shows it fighting.
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
const name = process.argv[2] ?? 'spec';
const server = await preview({ preview: { port: 4323, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4323/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 0 }));
await page.waitForTimeout(800);
const slot = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  for (const [i, id] of [[3, 'glimmer'], [1, 'thornbow'], [4, 'boulder'], [6, 'burrow']]) {
    s.sim.build(i, id);
    s.sim.upgrade(i);
    s.sim.upgrade(i);
  }
  s.sim.specialize(1, 1);
  s.sim.specialize(4, 1);
  s.sim.specialize(6, 0);
  return s.sim.level.slots[3];
});
await page.waitForTimeout(400);
await page.mouse.click(slot.x, slot.y);
await page.waitForTimeout(300);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
await page.mouse.click(slot.x - 56, slot.y - 82); // first tap: preview Stormcall
await page.waitForTimeout(200);
await page.screenshot({ path: `screenshots/${name}-preview.png` });
await page.mouse.click(slot.x - 56, slot.y - 82); // second tap: buy
await page.waitForTimeout(300);
await page.mouse.click(640, 690); // close menu
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  for (let i = 0; i < 14; i++) s.sim.spawn(i % 3 ? 'mudling' : 'shellback', 0, 820 + i * 22);
  s.sim.status = 'running';
});
await page.waitForTimeout(2500);
await page.screenshot({ path: `screenshots/${name}-fight.png` });
const st = await page.evaluate(() => window.__game.scene.getScene('Battle').sim.towers.filter(Boolean).map((t) => t.def.id + ':' + t.spec));
console.log('towers', JSON.stringify(st));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
