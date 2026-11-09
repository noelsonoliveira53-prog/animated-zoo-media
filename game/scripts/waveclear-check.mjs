// Wave cleared: calls wave 1 and kills each foe as it spawns until the sim's waveCleared fires; checks the
// "✓ Wave 1 cleared" pill (with "Flawless" since nothing leaked) and screenshots it once popped in (tweens paused).
// `node scripts/waveclear-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'waveclear';
const server = await preview({ preview: { port: 4364, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 })).newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4364/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
// play the wave out in fast sim steps, striking down each foe the moment it appears
await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  s.sim.callNextWave();
  s.paused = true; // the scene keeps handling events; we drive the sim here
  s.sim.dmgSrc = 'spell';
  for (let i = 0; i < 60 * 90 && s.sim.status === 'running'; i++) {
    s.sim.update(1 / 30);
    for (const e of s.sim.enemies) if (e.alive) s.sim.applyDamage(e, e.maxHp * 3 + e.shield, 'true');
  }
});
await page.waitForFunction(() => !!window.__game.scene.getScene('Battle').children.getByName('waveClear'), null, { timeout: 20000, polling: 'raf' });
const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 300, t0, { timeout: 20000, polling: 'raf' });
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.pauseAll());
const texts = await page.evaluate(() => window.__game.scene.getScene('Battle').children.getByName('waveClear').list.filter((o) => o.type === 'Text').map((o) => o.text));
await page.screenshot({ path: `screenshots/${name}.png`, clip: { x: 390, y: 60, width: 500, height: 260 } });
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.resumeAll());
await page.waitForFunction(() => !window.__game.scene.getScene('Battle').children.getByName('waveClear'), null, { timeout: 60000, polling: 'raf' });
const ok = texts[0] === '✓ Wave 1 cleared' && texts.includes('Flawless') && texts.includes('11 waves to go');
console.log(JSON.stringify({ texts, gone: true, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
