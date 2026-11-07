// Clicks both spell buttons and targets the road; screenshots the meteor in flight and the rangers.
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
const name = process.argv[2] ?? 'spells';
const server = await preview({ preview: { port: 4321, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4321/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 0 }));
await page.waitForTimeout(800);
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  for (let i = 0; i < 8; i++) s.sim.spawn(i % 2 ? 'shellback' : 'mudling', 0, 300 + i * 25);
  s.sim.status = 'running';
});
// Grove Call (right button) onto the road ahead of the enemies.
await page.mouse.click(1280 - 58, 720 - 58);
await page.waitForTimeout(150);
await page.mouse.click(300, 420);
// Starfall (left button) onto the clump.
await page.mouse.click(1280 - 58 - 92, 720 - 58);
await page.waitForTimeout(150);
const target = await page.evaluate(() => window.__game.scene.getScene('Battle').sim.enemies[3].pos);
await page.mouse.click(target.x, target.y);
await page.waitForTimeout(450);
await page.screenshot({ path: `screenshots/${name}-meteor.png` });
await page.waitForTimeout(4000);
await page.screenshot({ path: `screenshots/${name}-after.png` });
const st = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle').sim;
  return { cd: s.spellCd, summons: s.soldiers.filter((x) => x.summoned).length, alive: s.enemies.length };
});
console.log('state', JSON.stringify(st));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
