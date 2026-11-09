// Reduce motion check: toggle it in Settings with a real click, then start an Amberwood battle and confirm
// no drifting-leaf overlay is created and a leak does not shake the camera.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'motion';
const server = await preview({ preview: { port: 4367, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 80; i++) stars['l' + i] = 3;
  if (!localStorage.getItem('grovewatch.save.v1')) localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4367/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Settings'));
await page.waitForTimeout(700);
await page.mouse.click(640 + 125, 392); // Reduce motion toggle
await page.waitForTimeout(300);
await page.screenshot({ path: `screenshots/${name}.png` });
const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('grovewatch.save.v1')).settings.reduceMotion);
const count = async (reduced) => page.evaluate(async (reduced) => {
  const raw = JSON.parse(localStorage.getItem('grovewatch.save.v1'));
  raw.settings.reduceMotion = reduced;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify(raw));
  const active = window.__game.scene.getScenes(true)[0];
  active.scene.start('Battle', { levelIndex: 75 });
  let s;
  for (let k = 0; k < 40; k++) {
    await new Promise((r) => setTimeout(r, 200));
    s = window.__game.scene.getScene('Battle');
    if (s.sys.isActive() && s.cameras?.main && s.sim) break;
  }
  const leaves = s.children.list.filter((o) => o.type === 'Ellipse' && o.depth === 0.6).length;
  let shook = false;
  const orig = s.cameras.main.shake.bind(s.cameras.main);
  s.cameras.main.shake = (...a) => { shook = true; return orig(...a); };
  const e = s.sim.spawn('mudling', 0, s.sim.paths[0].length - 2);
  s.sim.status = 'running';
  for (let i = 0; i < 30; i++) s.sim.update(1 / 60);
  await new Promise((r) => setTimeout(r, 300));
  return { leaves, shook };
}, reduced);
const on = await count(true);
const off = await count(false);
console.log(JSON.stringify({ saved, reduced: on, normal: off }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
