// Raid check for the Mole Tunneler: opens a Warren, sends moles and brawlers in, and screenshots the moles digging under the walls.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'mole';
const server = await preview({ preview: { port: 4381, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, army: { brawler: 6, slinger: 4, mole: 3 } }));
});
await page.goto('http://localhost:4381/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Raid', { tier: 1, seed: 3 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-camp.png` });
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Raid');
  const edge = [];
  for (let x = 10; x < 1270 && edge.length < 3; x += 20) for (let y = 300; y < 500 && edge.length < 3; y += 20) if (s.sim.canDeployAt({ x, y })) edge.push({ x, y });
  const moles = [0, 1, 2].map((k) => s.sim.deploy('mole', edge[k % edge.length]));
  for (let k = 0; k < 4; k++) s.sim.deploy('brawler', edge[0]);
  for (let i = 0; i < 90; i++) s.sim.update(1 / 30);
  return { moles: moles.filter(Boolean).length, tunneling: moles.filter((m) => m && m.tunneling).length, hp: moles.map((m) => m && m.hp) };
});
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}.png` });
const later = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Raid');
  for (let i = 0; i < 30 * 25; i++) s.sim.update(1 / 30);
  const totem = s.sim.camp.buildings.find((b) => b.type === 'totem');
  return { totemHp: Math.round(totem.hp), totemMax: totem.maxHp };
});
console.log(JSON.stringify(later));
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
