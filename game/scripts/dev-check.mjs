// Dev mode check: toggles the menu's DEV switch on a fresh save, opens the newest level (locked normally),
// checks endless coins/lives/spells in battle, the village top-up and a raid with a full army, then turns it off.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'dev';
const server = await preview({ preview: { port: 4398, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4398/');
await page.waitForTimeout(1200);
// click the DEV toggle on the menu
await page.evaluate(() => {
  const m = window.__game.scene.getScene('Menu');
  m.children.list.find((o) => o.name === 'devToggle').emit('pointerdown', null, 0, 0, { stopPropagation() {} });
});
await page.waitForTimeout(800);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
const devAfterClick = await page.evaluate(() => JSON.parse(localStorage.getItem('grovewatch.save.v1')).settings.dev);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap', { focus: 124 }));
await page.waitForTimeout(1000);
await page.screenshot({ path: `screenshots/${name}-map.png` });
await page.evaluate(() => window.__game.scene.getScene('WorldMap').scene.start('Battle', { levelIndex: 124 }));
await page.waitForTimeout(1500);
const battle = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.build(1, 'thornbow');
  s.sim.build(2, 'glimmer');
  s.sim.castSpell('starfall', { x: 400, y: 300 });
  s.sim.status = 'running';
  return { coinsAfterBuild: s.sim.coins };
});
await page.waitForTimeout(800);
const battle2 = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { coins: s.sim.coins, lives: s.sim.lives, starfallCd: s.sim.spellCd.starfall }; });
await page.screenshot({ path: `screenshots/${name}.png` });
await page.evaluate(() => window.__game.scene.getScene('Battle').scene.start('Village'));
await page.waitForTimeout(1200);
const village = await page.evaluate(() => { const v = window.__game.scene.getScene('Village').v; return { coins: v.coins, glowsap: v.glowsap }; });
await page.evaluate(() => window.__game.scene.getScene('Village').scene.start('Raid', { tier: 2, seed: 1 }));
await page.waitForTimeout(1200);
const raid = await page.evaluate(() => window.__game.scene.getScene('Raid').sim.army);
await page.screenshot({ path: `screenshots/${name}-raid.png` });
console.log(JSON.stringify({ devAfterClick, battle, battle2, village, raid }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
