// Hazel check: the menu hero card, then a battle where her lullaby slows a mudling and Dream Darts hit several foes.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'hazel';
const server = await preview({ preview: { port: 4370, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 3, l3: 3 }, hero: 'hazel' }));
});
await page.goto('http://localhost:4370/');
await page.waitForTimeout(1500);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.status = 'running';
  const h = s.sim.hero;
  const m = s.sim.spawn('mudling', 0, 300);
  h.pos = { x: m.pos.x + 30, y: m.pos.y - 40 };
  h.dest = null;
  const slowed = s.sim.drowseMult(m);
  for (let k = 0; k < 4; k++) s.sim.spawn('mudling', 0, 260 + k * 30);
  const ok = s.sim.useHeroSkill();
  return { hero: h.def.name, ok, slowed };
});
await page.waitForTimeout(250);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
