// Field Guide: jump to the last enemy page (the newest regions), screenshot it, then open the newest boss's detail page.
// then flips pages with the real "<" / ">" buttons and screenshots both.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
import { readFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'guide-lastpage';
const server = await preview({ preview: { port: 4385, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
// a save that has met every enemy so far, so the newest pages show their art and text
const ids = [...readFileSync('src/data/enemies.ts', 'utf8').matchAll(/^  (\w+): \{$/gm)].map((m) => m[1]);
await page.addInitScript((seen) => {
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, seenEnemies: seen }));
}, ids);
await page.goto('http://localhost:4385/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('FieldGuide'));
await page.waitForTimeout(800);
const info = await page.evaluate(() => {
  const g = window.__game.scene.getScene('FieldGuide');
  g.show('enemies');
  return { entries: g.entries().length, page: g.grid.list.find((o) => o.name === 'guidePage')?.text };
});
// click ">" until the last page
for (let k = 0; k < 20; k++) {
  const t = await page.evaluate(() => window.__game.scene.getScene('FieldGuide').grid.list.find((o) => o.name === 'guidePage')?.text);
  if (!t) break;
  const [a, b] = t.split('/').map(Number);
  if (a >= b) break;
  await page.mouse.click(670, 720 - 58);
  await page.waitForTimeout(250);
}
const last = await page.evaluate(() => window.__game.scene.getScene('FieldGuide').grid.list.find((o) => o.name === 'guidePage')?.text);
await page.screenshot({ path: `screenshots/${name}.png` });
await page.evaluate(() => { const g = window.__game.scene.getScene('FieldGuide'); g.showDetail(g.entries().find((e) => e.key === 'galestag' || e.key === 'enemy_galestag')); });
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}-boss.png` });
console.log(JSON.stringify({ ...info, last }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
