// Hero skill preview: parks the hero by a crowd (three walkers and a flyer), hovers the skill button and screenshots
// the reach ring, marks and count; then checks the count matches the sim's hits and that it hides when the pointer
// leaves. `node scripts/skillaim-check.mjs <name> [heroId]`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const [name = 'skillaim', heroId = 'bramble'] = process.argv.slice(2);
const server = await preview({ preview: { port: 4353, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript((h) => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 3, l3: 3 }, hero: h })), heroId);
await page.goto('http://localhost:4353/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const es = [s.sim.spawn('shellback', 0, 600), s.sim.spawn('mudling', 0, 640), s.sim.spawn('skitter', 0, 570), s.sim.spawn('gloomwing', 0, 610)];
  s.sim.update(1 / 60);
  s.paused = true;
  const h = s.sim.hero;
  h.pos.x = es[0].pos.x + 40; h.pos.y = es[0].pos.y + 10; h.dest = null;
});
await page.mouse.move(58 + 104, 720 - 58); // the skill button
const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 300, t0, { timeout: 20000, polling: 'raf' });
const r = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { label: s.aimText.text, visible: s.aimText.visible, hits: s.sim.heroSkillHits().length, kind: s.sim.hero.def.active.kind }; });
await page.screenshot({ path: `screenshots/${name}.png` });
await page.mouse.move(640, 400);
await page.waitForTimeout(300);
const hidden = await page.evaluate(() => !window.__game.scene.getScene('Battle').aimText.visible);
const ok = r.visible && hidden && (r.kind === 'rally' ? /^Heals/.test(r.label) : r.label.includes(`${r.hits} foe`));
console.log(JSON.stringify({ ...r, hidden, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
