// Phone-sized (740×360, touch) screenshots of the text-heavy screens, to check that the bumped phone fonts fit:
// Menu, Village (building panel, shop, raid/army), Achievements. `node scripts/phone-screens.mjs <name>`.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'phone';
const server = await preview({ preview: { port: 4326, strictPort: true } });
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 6; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars, stats: { kills: 820 }, achievements: ['first_win'] }));
});
await page.addInitScript(() => { window.__noTouchTip = true; }); // the one-time touch tip card would cover the screen
await page.goto('http://localhost:4326/');
await page.waitForTimeout(1200);
const shot = async (suffix) => page.screenshot({ path: `screenshots/${name}-${suffix}.png` });
await shot('menu');
const go = (scene, data) => page.evaluate(([sc, d]) => {
  window.__game.scene.getScenes(true).forEach((s) => s.scene.stop());
  window.__game.scene.start(sc, d);
}, [scene, data ?? {}]);
await go('Village');
await page.waitForTimeout(1200);
await page.evaluate(() => {
  const v = window.__game.scene.getScene('Village');
  const mine = v.v.buildings.find((b) => b.type === 'coinmine');
  v.openPanel(mine.uid, false);
});
await page.waitForTimeout(400);
await shot('village-panel');
await page.evaluate(() => { const v = window.__game.scene.getScene('Village'); v.closePanel(); v.openShop(); });
await page.waitForTimeout(500);
await shot('village-shop');
await page.evaluate(() => window.__game.scene.getScene('Village').scene.restart());
await page.waitForTimeout(1200);
await page.evaluate(() => window.__game.scene.getScene('Village').openRaid());
await page.waitForTimeout(500);
await shot('village-raid');
await go('Achievements');
await page.waitForTimeout(800);
await shot('achievements');
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
