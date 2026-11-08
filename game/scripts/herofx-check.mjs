// Hero skill effects: for each hero, starts a battle, fires the active skill next to a few enemies and
// screenshots it mid-burst (tweens paused). `node scripts/herofx-check.mjs <name>` writes <name>-<hero>.png
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'herofx';
const heroes = ['bramble', 'fen', 'ember', 'wren', 'sorrel', 'hazel'];
const server = await preview({ preview: { port: 4326, strictPort: true } });
const browser = await pw.chromium.launch();
const errors = [];
const out = {};
for (const hero of heroes) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  page.on('console', (m) => m.type() === 'error' && errors.push(hero + ': ' + m.text()));
  page.on('pageerror', (e) => errors.push(hero + ': ' + String(e)));
  await page.addInitScript((h) => {
    const unlocked = ['bramble', 'fen', 'ember', 'wren', 'sorrel', 'hazel'];
    localStorage.setItem('grovewatch.save.v1', JSON.stringify({ hero: h, heroesUnlocked: unlocked, stars: { l1: 3 } }));
  }, hero);
  await page.goto('http://localhost:4326/');
  await page.waitForTimeout(900);
  await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
  await page.waitForTimeout(1500);
  const r = await page.evaluate(() => {
    const s = window.__game.scene.getScene('Battle');
    const h = s.sim.hero;
    const e = s.sim.spawn('mudling', 0, 520);
    h.pos = { x: e.pos.x + 30, y: e.pos.y + 10 };
    h.dest = null;
    for (let i = 0; i < 3; i++) s.sim.spawn('mudling', 0, 500 + i * 25);
    s.sim.update(1 / 60);
    h.skillCd = 0;
    return { id: h.def.id, used: s.sim.useHeroSkill() };
  });
  await page.waitForTimeout(260);
  await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.pauseAll());
  await page.waitForTimeout(80);
  await page.screenshot({ path: `screenshots/${name}-${hero}.png`, clip: { x: 0, y: 0, width: 1280, height: 720 } });
  await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.resumeAll());
  await page.waitForTimeout(2200);
  r.leftover = await page.evaluate(() => window.__game.scene.getScene('Battle').children.list.filter((o) => o.depth >= 2400 && o.depth < 2410).length);
  out[hero] = r;
  await page.close();
}
console.log(JSON.stringify(out));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || Object.values(out).some((r) => !r.used) ? 1 : 0);
