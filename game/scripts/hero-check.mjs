// Plays the hero controls with real clicks: select hero, move, use skill. Screenshots each step.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try {
  pw = require('playwright');
} catch {
  pw = require(execSync('npm root -g').toString().trim() + '/playwright');
}
const name = process.argv[2] ?? 'hero';
const heroId = process.argv[3] ?? 'bramble';
const server = await preview({ preview: { port: 4319, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript((h) => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ hero: h })), heroId);
await page.goto('http://localhost:4319/');
await page.waitForTimeout(1000);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 0 }));
await page.waitForTimeout(3500);
const heroPos = await page.evaluate(() => window.__game.scene.getScene('Battle').sim.hero.pos);
await page.mouse.click(heroPos.x, heroPos.y - 20); // select
await page.waitForTimeout(200);
await page.mouse.click(640, 430); // move to road near the middle
await page.waitForTimeout(300);
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 600;
  s.sim.build(3, 'thornbow');
  s.sim.build(4, 'glimmer');
  s.sim.callNextWave();
  s.sim.callNextWave();
});
await page.waitForTimeout(9000);
await page.screenshot({ path: `screenshots/${name}-fight.png` });
await page.mouse.click(58 + 104, 720 - 58); // skill button
await page.waitForTimeout(150);
await page.screenshot({ path: `screenshots/${name}-skill.png` });
const st = await page.evaluate(() => {
  const h = window.__game.scene.getScene('Battle').sim.hero;
  return { pos: h.pos, level: h.level, xp: Math.round(h.xp), skillCd: h.skillCd, alive: h.alive };
});
console.log('hero', JSON.stringify(st));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
