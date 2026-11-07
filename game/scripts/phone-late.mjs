// Phone-size (740×360, touch) screenshots of the late-game screens: region 8 map, a Ruins battle with a build menu, Field Guide spells + a boss page.
// Menu, Village (building panel, shop, raid/army), Achievements. `node scripts/phone-screens.mjs <name>`.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'phone';
const server = await preview({ preview: { port: 4334, strictPort: true } });
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 36; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4334/');
await page.waitForTimeout(1200);
const shot = async (suffix) => page.screenshot({ path: `screenshots/${name}-${suffix}.png` });
const go = (scene, data) => page.evaluate(([sc, d]) => {
  window.__game.scene.getScenes(true).forEach((s) => s.scene.stop());
  window.__game.scene.start(sc, d);
}, [scene, data ?? {}]);
await go('WorldMap', { region: 7 });
await page.waitForTimeout(1200);
await shot('map');
await go('Battle', { levelIndex: 36 });
await page.waitForTimeout(2500);
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const slot = s.level.slots[3];
  s.input.emit('pointerdown', { x: slot.x, y: slot.y, worldX: slot.x, worldY: slot.y, downX: slot.x, downY: slot.y, event: {} }, []);
  if (typeof s.openBuildMenu === 'function') s.openBuildMenu(3);
});
await page.waitForTimeout(500);
await shot('battle');
await go('FieldGuide', { tab: 'spells' });
await page.waitForTimeout(900);
await shot('guide-spells');
await page.evaluate(() => {
  const raw = JSON.parse(localStorage.getItem('grovewatch.save.v1') ?? '{}');
  raw.seenEnemies = Object.keys(window.__game.textures.list).filter((k) => k.startsWith('enemy_')).map((k) => k.slice(6));
  localStorage.setItem('grovewatch.save.v1', JSON.stringify(raw));
  const g = window.__game.scene.getScene('FieldGuide');
  g.show('enemies');
  const all = g.entries();
  g.showDetail(all.find((e) => e.key === 'zephyrax'));
});
await page.waitForTimeout(500);
await shot('guide-boss');
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
