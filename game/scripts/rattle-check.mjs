// Raid check for the Rattle Trap: opens a Stronghold, drops brawlers and an owl beside the trap and checks the ground troops get poisoned.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'rattle';
const server = await preview({ preview: { port: 4389, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, army: { brawler: 12, slinger: 6, owl: 2 } }));
});
await page.goto('http://localhost:4389/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Raid', { tier: 2, seed: 3 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-camp.png` });
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Raid');
  const trap = s.sim.camp.buildings.find((b) => b.type === 'rattle');
  const img = s.buildingViews.get(trap.uid).img;
  const c = { x: img.x, y: img.y };
  s.sim.army = { brawler: 3, owl: 1 };
  const edge = [];
  for (let x = 10; x < 1270 && edge.length < 1; x += 20) for (let y = 80; y < 700 && edge.length < 1; y += 20) if (s.sim.canDeployAt({ x, y })) edge.push({ x, y });
  const placed = ['brawler', 'brawler', 'brawler', 'owl'].map((id, k) => {
    const t = s.sim.deploy(id, edge[0]);
    if (t) t.pos = { x: c.x - 50 + k * 30, y: c.y + 45 };
    return t;
  });
  for (let i = 0; i < 20; i++) s.sim.update(1 / 30);
  return { trap: !!trap, poisoned: placed.map((t) => +(t.poisonT ?? 0).toFixed(2)), hp: placed.map((t) => Math.round(t.hp)) };
});
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
