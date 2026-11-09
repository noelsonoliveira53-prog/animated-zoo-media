// Wave call button: screenshots the start glow, then mid-countdown after wave 1 (strip + "Call now: +N" chip),
// and checks a real tap pays exactly the bonus the chip showed. `node scripts/wavecall-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'wavecall';
const server = await preview({ preview: { port: 4352, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 })).newPage();
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4352/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
await page.screenshot({ path: `screenshots/${name}-start.png`, clip: { x: 860, y: 0, width: 420, height: 130 } });
const startChip = await page.evaluate(() => window.__game.scene.getScene('Battle').callChip.visible);
// call wave 1, let a few seconds of the next countdown run, then freeze
await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.sim.callNextWave(); for (let i = 0; i < 300; i++) s.sim.update(1 / 60); s.paused = true; });
const t0 = await page.evaluate(() => window.__game.scene.getScene('Battle').time.now);
await page.waitForFunction((t) => window.__game.scene.getScene('Battle').time.now > t + 300, t0, { timeout: 20000, polling: 'raf' });
const mid = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { chip: s.callChip.text, visible: s.callChip.visible, bonus: s.sim.callBonus(), full: +s.callFull.toFixed(1), left: +s.sim.waveCountdown.toFixed(1) }; });
await page.screenshot({ path: `screenshots/${name}.png`, clip: { x: 860, y: 0, width: 420, height: 130 } });
// tap the button: the coins should rise by the shown bonus plus the wave's income
const paid = await page.evaluate(() => new Promise((res) => { const s = window.__game.scene.getScene('Battle'); s.sim.drainEvents(); s.paused = false; s.callWave(); const ev = s.sim.drainEvents().find((e) => e.type === 'waveStart'); res(ev ? ev.bonus : -1); }));
const ok = !startChip && mid.visible && mid.chip === `Call now: +${mid.bonus} coins` && paid === mid.bonus;
console.log(JSON.stringify({ startChip, mid, paid, ok }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
