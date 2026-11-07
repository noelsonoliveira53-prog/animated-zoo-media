// Bramble's Shield Toss: with Bramble near a hovering flyer, fast-forward a moment and confirm the flyer took a hit;
// screenshot mid-throw.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'toss';
const server = await preview({ preview: { port: 4330, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ hero: 'bramble' })));
await page.goto('http://localhost:4330/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 0 }));
await page.waitForTimeout(2500);
const res = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.status = 'running';
  const h = s.sim.hero;
  h.pos = { x: 300, y: 380 };
  h.dest = null;
  const f = s.sim.spawn('gloomwing', 0, 560);
  f.def = { ...f.def, speed: 0 };
  for (let i = 0; i < 20; i++) s.sim.update(1 / 60);
  return { flyerHp: f.hp, max: f.maxHp, tossCd: +h.tossCd.toFixed(2), shots: s.sim.projectiles.filter((p) => p.kind === 'hero_toss').length };
});
await page.waitForTimeout(150);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(res));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !(res.tossCd > 0) ? 1 : 0);
