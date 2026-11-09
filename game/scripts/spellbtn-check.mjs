// Spell button feedback: taps Starfall (press squash), casts it, then lets it come off cooldown and screenshots the
// ready ping (tweens paused). `node scripts/spellbtn-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'spellbtn';
const server = await preview({ preview: { port: 4341, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4341/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }));
await page.waitForTimeout(1500);
const pos = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return s.spellPos(0); });
await page.mouse.click(pos.x, pos.y); // real tap: squash + arm
await page.waitForTimeout(300);
const r = await page.evaluate(() => {
  const s = window.__game.scene.getScene('Battle');
  const armed = s.spellMode;
  s.armSpell(null);
  s.sim.castSpell('starfall', s.sim.paths[0].pointAt(300));
  s.sim.spellCd.starfall = 0.05;
  return { armed, cd: s.sim.spellCd.starfall };
});
await page.waitForFunction(() => { const s = window.__game.scene.getScene('Battle'); return s.spellWasReady.starfall === true; }, null, { timeout: 20000, polling: 'raf' });
await page.waitForTimeout(60);
await page.evaluate(() => window.__game.scene.getScene('Battle').tweens.pauseAll());
await page.screenshot({ path: `screenshots/${name}.png`, clip: { x: 940, y: 590, width: 340, height: 130 } });
console.log(JSON.stringify(r));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || r.armed !== 'starfall' ? 1 : 0);
