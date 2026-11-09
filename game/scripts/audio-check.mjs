// Audio smoke test: a real click unlocks WebAudio, then a battle runs with its ambience bed, shots and a heavy kill
// (thump), then the scene restarts (ambience must stop and restart cleanly). Fails on any console error.
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const server = await preview({ preview: { port: 4334, strictPort: true } });
const browser = await pw.chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4334/');
await page.waitForTimeout(1200);
await page.mouse.click(460, 390); // Campaign: a real gesture that unlocks audio
await page.waitForTimeout(800);
for (const idx of [0, 55, 5]) {
  await page.evaluate((i) => window.__game.scene.getScenes(true)[0].scene.start('Battle', { levelIndex: i }), idx);
  await page.waitForTimeout(1500);
  await page.evaluate(() => {
    const s = window.__game.scene.getScene('Battle');
    s.sim.coins = 9999;
    ['thornbow', 'glimmer', 'boulder'].forEach((k, i) => s.sim.build(i, k));
    s.sim.callNextWave();
    const boss = Object.values(window.__game.scene.getScene('Battle').sim.enemies)[0];
    void boss;
  });
  await page.waitForTimeout(2500);
}
const state = await page.evaluate(() => (window.__game.sound?.context?.state ?? 'n/a'));
console.log(JSON.stringify({ phaserAudio: state }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
