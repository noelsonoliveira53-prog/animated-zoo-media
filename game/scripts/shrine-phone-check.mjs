// Phone-size (740×360 touch) version of shrine-check: the 8-card build shop must stay readable with enlarged phone text.
// then starts a battle and checks the faster spell cooldowns and the bonus banner.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'shrine';
const server = await preview({ preview: { port: 4328, strictPort: true } });
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 740, height: 360 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
const page = await ctx.newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const now = Date.now();
  const b = (uid, type, level, col, row) => ({ uid, type, level, col, row, upgradeEnds: null, lastCollect: now });
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({
    stars: { l1: 3, l2: 3 }, hero: 'fen',
    village: { coins: 9000, glowsap: 9000, nextUid: 20, buildings: [b(1, 'townhall', 3, 10, 5), b(2, 'workshop', 1, 2, 2), b(3, 'shrine', 2, 15, 8), b(4, 'builderhut', 1, 2, 10), b(5, 'builderhut', 1, 6, 10), b(6, 'shrine', 3, 0, 0)].slice(0, 5) },
  }));
});
await page.addInitScript(() => { window.__noTouchTip = true; }); // the one-time touch tip card would cover the screen
await page.goto('http://localhost:4328/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Village'));
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Village').openPanel(3, false));
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}-panel.png` });
await page.evaluate(() => { const s = window.__game.scene.getScene('Village'); s.closePanel?.(); s.openShop(); });
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}.png` });
await page.evaluate(() => window.__game.scene.getScene('Village').scene.start('Battle', { levelIndex: 1 }));
await page.waitForTimeout(900);
await page.screenshot({ path: `screenshots/${name}-battle.png` });
const st = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle').sim; s.castSpell('starfall', { x: 600, y: 400 }); return { mult: s.spellCdMult, cd: s.spellCd.starfall }; });
console.log('battle', JSON.stringify(st));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
