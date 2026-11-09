// Boss defeat: spawns a boss, kills it (a real sim kill), and checks the "<Boss> defeated!" ribbon and the slow-motion
// beat (the sim's time scale dips, then returns to 1); screenshots the ribbon once it has popped in (tweens paused).
// `node scripts/bossdown-check.mjs <name> [bossId] [levelIndex]`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const [name = 'bossdown', bossId = 'zephyrax', lvl = '64'] = process.argv.slice(2);
const server = await preview({ preview: { port: 4361, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4361/');
await page.waitForTimeout(900);
await page.evaluate((i) => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: i }), Number(lvl));
await page.waitForTimeout(1500);
const frames = async (ms) => { const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now); await page.waitForFunction(([t, d]) => window.__game.scene.getScene('Battle').time.now > t + d, [t0, ms], { timeout: 60000, polling: 'raf' }); };
await page.evaluate((id) => { const s = window.__game.scene.getScene('Battle'); const b = s.sim.spawn(id, 0, 300); s.sim.update(1 / 60); window.__b = b.uid; }, bossId);
await frames(2500); // the boss intro plays out
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const b = s.sim.enemies.find((e) => e.uid === window.__b);
  s.sim.dmgSrc = 'spell';
  // phases and shields can soak a single blow: keep hitting until it falls
  for (let k = 0; k < 20 && b.alive; k++) { b.shield = 0; s.sim.applyDamage(b, b.maxHp * 2, 'true'); }
});
await page.waitForFunction(() => !!window.__game.scene.getScene('Battle').children.getByName('bossDefeated'), null, { timeout: 20000, polling: 'raf' });
const slowing = await page.evaluate(() => window.__game.scene.getScene('Battle').slowMoStart > 0);
await frames(350);
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.pauseAll());
const text = await page.evaluate(() => window.__game.scene.getScene('Battle').children.getByName('bossDefeated').list.filter((o) => o.type === 'Text').map((o) => o.text));
await page.screenshot({ path: `screenshots/${name}.png` });
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.resumeAll());
await frames(4000);
const after = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { slow: s.slowMoStart, banner: !!s.children.getByName('bossDefeated') }; });
const ok = slowing && /defeated!/.test(text[0] ?? '') && after.slow === 0 && !after.banner;
console.log(JSON.stringify({ slowing, text, after, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
