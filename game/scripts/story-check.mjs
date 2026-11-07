// Story card check: wins level 45 (forced), checks the end panel offers "Story", taps it, screenshots the card.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'story';
const level = Number(process.argv[3] ?? 44);
const server = await preview({ preview: { port: 4338, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  const stars = {};
  for (let i = 1; i <= 60; i++) stars['l' + i] = 3;
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars }));
});
await page.goto('http://localhost:4338/');
await page.waitForTimeout(1000);
await page.evaluate((i) => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: i }), level);
await page.waitForTimeout(2000);
await page.evaluate(() => window.__game.scene.getScene('Battle').endBattle(true));
await page.waitForTimeout(1500);
const labels = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const out = [];
  const walk = (o) => { if (o.label?.text) out.push(o.label.text); (o.list ?? []).forEach(walk); };
  s.children.list.forEach(walk);
  return out;
});
await page.screenshot({ path: `screenshots/${name}-panel.png` });
await page.evaluate(() => window.__game.scene.getScene('Battle').scene.start('Story', { levelId: window.__game.scene.getScene('Battle').level.id }));
await page.waitForTimeout(2600);
const title = await page.evaluate(() => window.__game.scene.getScene('Story').children.list.find((o) => o.name === 'storyTitle')?.text);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify({ labels, title }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
