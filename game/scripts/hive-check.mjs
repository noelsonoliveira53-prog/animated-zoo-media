// Raid check for the Hornet Hive: opens a Warren, walks brawlers and an owl up to the hive, knocks it down and checks the swarm stings them.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'hive';
const server = await preview({ preview: { port: 4375, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, army: { brawler: 12, slinger: 6, owl: 2 } }));
});
await page.goto('http://localhost:4375/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Raid', { tier: 1, seed: 3 }));
await page.waitForTimeout(1200);
await page.screenshot({ path: `screenshots/${name}-camp.png` });
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Raid');
  const hive = s.sim.camp.buildings.find((b) => b.type === 'hive');
  const img = s.buildingViews.get(hive.uid).img;
  const c = { x: img.x + img.displayWidth / 2, y: img.y + img.displayHeight / 2 };
  s.sim.army = { brawler: 3, owl: 1 };
  const edge = [];
  for (let x = 10; x < 1270 && edge.length < 1; x += 20) for (let y = 80; y < 700 && edge.length < 1; y += 20) if (s.sim.canDeployAt({ x, y })) edge.push({ x, y });
  const placed = ['brawler', 'brawler', 'brawler', 'owl'].map((id, k) => {
    const t = s.sim.deploy(id, edge[0]);
    if (t) t.pos = { x: c.x - 60 + k * 30, y: c.y + 50 };
    return t;
  });
  const before = placed.map((t) => t.hp);
  hive.hp = 1;
  s.sim.hurtBuilding(hive, 10, placed[0]);
  return { hive: !!hive, before, after: placed.map((t) => t.hp) };
});
await page.waitForTimeout(250);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
