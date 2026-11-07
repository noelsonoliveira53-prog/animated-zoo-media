// Endless mode check: open level 1's map card with a real click, press Endless, play a few generated waves (fast-forward),
// end the run and check the result panel + saved best.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'endless';
const server = await preview({ preview: { port: 4327, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 } })));
await page.goto('http://localhost:4327/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 0 }));
await page.waitForTimeout(1200);
const node = await page.evaluate(() => window.__game.registry ? null : null);
// Level 1 node position comes from the level data (mapPos); click it, then the Endless button.
const pos = await page.evaluate(() => {
  const m = window.__game.scene.getScene('WorldMap');
  m.openPanel(0);
  return true;
});
await page.waitForTimeout(500);
await page.screenshot({ path: `screenshots/${name}-card.png` });
// Panel centre (640, 380); Endless button at (-30, H/2 - 44) with H = 330.
await page.mouse.click(640 - 30, 380 + 165 - 44);
await page.waitForTimeout(2500);
const started = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  return { active: window.__game.scene.isActive('Battle'), endless: s.endless, waves: s.sim.totalWaves, hud: s.waveText.text };
});
// Defend a little and fast-forward several waves.
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 4000;
  const kinds = ['thornbow', 'glimmer', 'boulder', 'burrow'];
  s.level.slots.forEach((_, i) => s.sim.build(i, kinds[i % 4]));
  s.sim.callNextWave();
  for (let i = 0; i < 60 * 120; i++) s.sim.update(1 / 60);
});
await page.waitForTimeout(800);
await page.screenshot({ path: `screenshots/${name}-run.png` });
const ran = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const w = s.sim.waveIndex;
  s.endBattle(false);
  return { waveIndex: w, hud: s.waveText.text };
});
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}.png` });
const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('grovewatch.save.v1')));
const out = { started, ran, best: saved.endlessBest?.l1, stars: saved.stars };
console.log(JSON.stringify(out));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
const ok = started.endless && started.hud.includes('∞') && out.best === ran.waveIndex && !Object.keys(out.stars).some((k) => k.includes('endless'));
process.exit(errors.length || !ok ? 1 : 0);
