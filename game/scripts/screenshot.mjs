// Headless smoke test: serves dist/, plays a battle, captures screenshots and console errors.
// Usage: node scripts/screenshot.mjs <name>
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

// Use the preinstalled global Playwright (do not install another copy).
const require = createRequire(import.meta.url);
let pw;
try {
  pw = require('playwright');
} catch {
  pw = require(execSync('npm root -g').toString().trim() + '/playwright');
}
const { chromium } = pw;

const name = process.argv[2] ?? 'shot';
const server = await preview({ preview: { port: 4317, strictPort: true } });
const url = 'http://localhost:4317/';
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));

await page.goto(url);
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-menu.png` });

// Enter battle 1 and set up a defense through the exposed game object.
await page.evaluate(() => window.__game.scene.start('Battle', { levelIndex: 0 }));
await page.waitForTimeout(800);
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 1000;
  s.sim.build(1, 'thornbow');
  s.sim.build(3, 'boulder');
  s.sim.build(4, 'burrow');
  s.sim.upgrade(4);
  s.sim.build(6, 'glimmer');
  s.sim.build(0, 'burrow');
  s.sim.callNextWave();
  s.sim.callNextWave();
  s.sim.callNextWave();
});
await page.waitForTimeout(7000);
await page.screenshot({ path: `screenshots/${name}-battle.png` });
// Open a tower menu by clicking a slot.
await page.mouse.click(Number(process.env.CLICK_X ?? 1080), Number(process.env.CLICK_Y ?? 460));
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}-menu-open.png` });

const state = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  return { status: s.sim.status, lives: s.sim.lives, wave: s.sim.waveIndex, enemies: s.sim.enemies.length };
});
console.log('state', JSON.stringify(state));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
