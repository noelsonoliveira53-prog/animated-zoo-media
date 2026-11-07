// Visual check: spawns every enemy type on level 2 and screenshots them mid-walk.
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
const name = process.argv[2] ?? 'enemies';
const server = await preview({ preview: { port: 4318, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4318/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.start('Battle', { levelIndex: 1 }));
await page.waitForTimeout(800);
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const ids = ['mudling', 'skitter', 'shellback', 'gloomwing', 'gnat', 'bogmender', 'reedguard', 'splotch', 'thornhog', 'wispling', 'bogbrute', 'murkmaw'];
  ids.forEach((id, i) => s.sim.spawn(id, i % 2, 200 + i * 75));
  s.sim.status = 'running';
  s.sim.coins = 2000;
  s.sim.build(4, 'glimmer');
  s.sim.build(5, 'burrow');
  s.sim.build(1, 'boulder');
});
await page.waitForTimeout(2500);
await page.screenshot({ path: `screenshots/${name}.png` });
// Damage the boss through its phases.
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const boss = s.sim.enemies.find((e) => e.def.id === 'murkmaw');
  s.sim.applyDamage(boss, boss.maxHp * 0.65);
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}-boss.png` });
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
