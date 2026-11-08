// Field Guide raids tab: opens the Standing Stone entry and screenshots it, to check camp-building facts are listed.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
import { readFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'guide-lastpage';
const server = await preview({ preview: { port: 4397, strictPort: true } });
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
await page.goto('http://localhost:4397/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('FieldGuide'));
await page.waitForTimeout(800);
const info = await page.evaluate(() => {
  const g = window.__game.scene.getScene('FieldGuide');
  g.show('raids');
  const e = g.entries().find((x) => x.key === 'camp_menhir');
  g.showDetail(e);
  return { lines: e.lines };
});
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
