// Raid check for the Sludge Pit: opens a Warren, shows the pit's muddy zone, deploys brawlers into it and checks they slow.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'sludge';
const server = await preview({ preview: { port: 4362, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, army: { brawler: 12, slinger: 6, owl: 2 } }));
});
await page.goto('http://localhost:4362/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Raid', { tier: 1, seed: 3 }));
await page.waitForTimeout(1200);
const info = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Raid');
  const pit = s.sim.camp.buildings.find((b) => b.type === 'sludge');
  const c = { x: 0, y: 0 };
  const img = s.buildingViews.get(pit.uid).img;
  c.x = img.x + img.displayWidth / 2; c.y = img.y + img.displayHeight / 2;
  s.sim.army = { brawler: 4, owl: 1 };
  // deploy at the camp's edge, then carry the troops to the pit's rim
  const edge = [];
  for (let x = 10; x < 1270 && edge.length < 5; x += 20) for (let y = 80; y < 700 && edge.length < 5; y += 20) if (s.sim.canDeployAt({ x, y })) edge.push({ x, y });
  const placed = ['brawler', 'brawler', 'brawler', 'owl'].map((id, k) => {
    const t = s.sim.deploy(id, edge[0]);
    if (t) t.pos = { x: c.x - 90 + k * 8, y: c.y - 20 + k * 14 };
    return t;
  });
  const troop = placed[0];
  return { pit: !!pit, zones: s.mireZones.size, factor: troop ? s.sim.mireFactor(troop) : null, owlFactor: placed[3] ? s.sim.mireFactor(placed[3]) : null };
});
await page.waitForTimeout(1500);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify(info));
// knock the pit out, end the raid, and check the Mudlark stat was banked
const banked = await page.evaluate(async () => {
  const s = window.__game.scene.getScene('Raid');
  for (const b of s.sim.camp.buildings) if (b.type === 'sludge') b.hp = 0;
  s.sim.finish();
  await new Promise((r) => setTimeout(r, 800));
  return JSON.parse(localStorage.getItem('grovewatch.save.v1')).stats?.sludgeDestroyed ?? 0;
});
console.log('sludgeDestroyed', banked);
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
