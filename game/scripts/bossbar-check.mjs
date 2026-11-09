// Boss bar: spawns a boss with phases, knocks it just past its first phase (a real phase event), screenshots the
// bar mid-flash with the gold notch and the damage trail, then checks the trail drains and the flash ends.
// `node scripts/bossbar-check.mjs <name> [bossId] [levelIndex]`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const [name = 'bossbar', bossId = 'zephyrax', lvl = '64'] = process.argv.slice(2);
const server = await preview({ preview: { port: 4359, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 })).newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4359/');
await page.waitForTimeout(900);
await page.evaluate((i) => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: i }), Number(lvl));
await page.waitForTimeout(1500);
const frames = async (ms) => { const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now); await page.waitForFunction(([t, d]) => window.__game.scene.getScene('Battle').time.now > t + d, [t0, ms], { timeout: 60000, polling: 'raf' }); };
const info = await page.evaluate((id) => {
  const s = window.__game.scene.getScene('Battle');
  const b = s.sim.spawn(id, 0, 200);
  s.sim.update(1 / 60);
  window.__b = b.uid;
  return { phases: (b.def.phases ?? []).map((p) => p.at) };
}, bossId);
await frames(2500); // let the boss intro settle
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const b = s.sim.enemies.find((e) => e.uid === window.__b);
  const at = (b.def.phases ?? [{ at: 0.5 }])[0].at;
  s.sim.dmgSrc = 'spell';
  s.sim.applyDamage(b, b.hp - b.maxHp * (at - 0.04) + (b.shield ?? 0), 'true'); // drop just past the first phase
  s.sim.update(1 / 60); // the phase fires on the sim's next step
  s.paused = true;
});
// headless frames are slow (a frame can outlast the 450 ms flash), so catch the flash as soon as it is set
await page.waitForFunction(() => window.__game.scene.getScene('Battle').bossFlashUntil > 0, null, { timeout: 20000, polling: 'raf' });
const mid = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { flashing: s.bossFlashUntil > 0, trail: +s.bossTrail.trail.toFixed(2) }; });
await page.screenshot({ path: `screenshots/${name}.png`, clip: { x: 360, y: 60, width: 560, height: 90 } });
await frames(9000);
const later = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); const b = s.sim.enemies.find((e) => e.uid === window.__b); return { flashing: s.bossFlashUntil > s.time.now, trail: +s.bossTrail.trail.toFixed(2), frac: +(b.hp / b.maxHp).toFixed(2) }; });
const ok = info.phases.length > 0 && mid.flashing && !later.flashing && Math.abs(later.trail - later.frac) < 0.02 && mid.trail > later.frac;
console.log(JSON.stringify({ ...info, mid, later, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
