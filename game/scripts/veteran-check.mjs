// Veteran towers: gives a Thornbow 74 kills, lets it land the 75th (a real sim kill credited to it), checks the gold
// badge pops once, then opens its menu and screenshots the card's "★ 75 kills" record. Selling removes the badge.
// `node scripts/veteran-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'veteran';
const server = await preview({ preview: { port: 4357, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4357/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const r = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.coins = 2000;
  const t = s.sim.build(3, 'thornbow');
  s.sim.upgrade(3);
  const key = `tower:${t.uid}`;
  s.sim.killsBy[key] = 74;
  s.sim.dmgBy[key] = 3480;
  const e = s.sim.spawn('mudling', 0, 300);
  s.sim.update(1 / 60);
  s.sim.dmgSrc = key; // the 50th kill lands from this tower
  s.sim.applyDamage(e, 9999, 'physical');
  window.__uid = t.uid;
  return { uid: t.uid };
});
const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 500, t0, { timeout: 20000, polling: 'raf' });
const badge = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { badge: s.veteranBadges.has(window.__uid), kills: s.sim.killsBy[`tower:${window.__uid}`] }; });
const tp = await page.evaluate(() => window.__game.scene.getScene('Battle').sim.towers[3].pos);
await page.screenshot({ path: `screenshots/${name}-badge.png`, clip: { x: tp.x - 80, y: tp.y - 90, width: 160, height: 130 } });
await page.evaluate(() => window.__game.scene.getScene('Battle').openSlotMenu(3));
await page.waitForTimeout(400);
const rec = await page.evaluate(() => window.__game.scene.getScene('Battle').menu.getByName('towerCard').getByName('towerRecord').text);
await page.screenshot({ path: `screenshots/${name}.png` });
const sold = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.sim.sell(3); for (const ev of s.sim.drainEvents()) s.handleEvent(ev); return !s.veteranBadges.has(window.__uid); });
const ok = badge.badge && badge.kills === 75 && /★ 75 kills/.test(rec) && sold;
console.log(JSON.stringify({ ...badge, rec, sold, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
