// Result screen check: wins a level (3 stars) and loses another, screenshotting each panel after the stars land.
// `node scripts/result-check.mjs <name>` writes <name>.png (victory) and <name>-defeat.png
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'result';
const server = await preview({ preview: { port: 4330, strictPort: true } });
const browser = await pw.chromium.launch();
const errors = [];
const out = {};
for (const won of [true, false]) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.addInitScript(() => localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 3 } })));
  await page.goto('http://localhost:4330/');
  await page.waitForTimeout(900);
  await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
  await page.waitForTimeout(1500);
  const t0 = await page.evaluate((won) => {
    const s = window.__game.scene.getScene('Battle');
    // a believable run for the wave chart: a couple of slips and one rough wave (the defeat ends at wave 7)
    s.sim.leaksByWave = won ? [0, 0, 1, 0, 0, 2, 0, 0, 4, 0, 1, 0] : [0, 1, 0, 3, 2, 6, 8];
    if (!won) { s.sim.lives = 0; s.sim.waveIndex = 6; }
    // and believable run stats for the summary line: two towers, the hero and a few spells
    s.sim.coins = 5000;
    const a = s.sim.build(0, 'boulder'); s.sim.upgrade(0); s.sim.upgrade(0);
    const b = s.sim.build(1, 'thornbow');
    s.sim.dmgBy = { [`tower:${a.uid}`]: 14230, [`tower:${b.uid}`]: 3810, hero: 820, spell: 600 };
    s.sim.killsBy = { [`tower:${a.uid}`]: 41, [`tower:${b.uid}`]: 17, hero: 6 };
    s.sim.spellsCast = 3;
    s.endBattle(won);
    return s.time.now;
  }, won);
  // follow the scene clock (headless frames are slow): stars land by ~1.4 s, the reward has rolled by ~2.4 s,
  // the wave chart's bars have all grown by ~3.3 s
  await page.waitForFunction((t0) => window.__game.scene.getScene('Battle').time.now >= t0 + 3600, t0, { timeout: 30000, polling: 'raf' });
  out[won ? 'victory' : 'defeat'] = await page.evaluate(() => {
    const s = window.__game.scene.getScene('Battle');
    const find = (list, n) => { for (const o of list) { if (o.name === n) return o; if (o.list) { const f = find(o.list, n); if (f) return f; } } return null; };
    return { reward: find(s.children.list, 'rewardText')?.text ?? null, summary: find(s.children.list, 'runSummary')?.text ?? null };
  });
  await page.screenshot({ path: `screenshots/${name}${won ? '' : '-defeat'}.png` });
  await page.close();
}
console.log(JSON.stringify(out));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
