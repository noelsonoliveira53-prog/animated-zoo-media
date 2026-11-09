// Mistwreath check: region 17 map, Lanternstep Rise scenery + music, a Mistfox phases and a Silkcrane dodges.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'mist';
const server = await preview({ preview: { port: 4368, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 80; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4368/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { region: 16 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 80 }));
await page.waitForTimeout(2500);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 3000;
  s.sim.build(1, 'thornbow');
  s.sim.build(2, 'glimmer');
  s.sim.build(6, 'burrow');
  s.sim.build(7, 'boulder');
  s.sim.status = 'running';
  const fox = s.sim.spawn('mistfox', 0, 520);
  const crane = s.sim.spawn('silkcrane', 0, 700);
  crane.def = { ...crane.def, speed: 0 };
  let dodged = 0, phased = 0;
  for (let i = 0; i < 60 * 5; i++) {
    s.sim.update(1 / 60);
    if (fox.phased) phased++;
  }
  return { music: window.__music.getTheme().id, foxPhasedFrames: phased, craneAlive: crane.alive };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
