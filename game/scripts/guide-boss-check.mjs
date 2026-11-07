// Field Guide boss page check: marks every enemy as seen, opens the guide, finds Zephyrax and screenshots its page.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'guide-boss';
const boss = process.argv[3] ?? 'zephyrax';
const server = await preview({ preview: { port: 4332, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4332/');
await page.waitForTimeout(1000);
await page.evaluate(() => {
  const raw = JSON.parse(localStorage.getItem('grovewatch.save.v1') ?? '{}');
  raw.seenEnemies = Object.keys(window.__game.textures.list).filter((k) => k.startsWith('enemy_')).map((k) => k.slice(6));
  localStorage.setItem('grovewatch.save.v1', JSON.stringify(raw));
  window.__game.scene.getScene('Menu').scene.start('FieldGuide');
});
await page.waitForTimeout(800);
const info = await page.evaluate((id) => {
  const g = window.__game.scene.getScene('FieldGuide');
  const all = g.entries();
  const i = all.findIndex((e) => e.key === id);
  g.show('enemies', Math.floor(i / 30));
  g.showDetail(all[i]);
  const phases = g.detail.list.find((o) => o.name === 'bossPhases');
  const right = Math.max(...g.detail.list.filter((o) => o.type === 'Text').map((o) => o.x + o.width));
  return { index: i, phases: phases?.text, bottom: phases ? phases.y + phases.height : null, right, fits: right <= 1236 };
}, boss);
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
