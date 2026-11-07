// Verifies the procedural music starts after a user gesture and switches moods with scenes.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'music';
const server = await preview({ preview: { port: 4336, strictPort: true } });
const browser = await pw.chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await page.goto('http://localhost:4336/');
await page.waitForTimeout(900);
await page.mouse.click(1040 + 140, 470 - 36); // hero arrow (a gesture that unlocks audio)
await page.waitForTimeout(1200);
const a = await page.evaluate(() => ({ mood: window.__music.getMood(), step: window.__music.step }));
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 1 }));
await page.waitForTimeout(800);
await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.sim.spawn('murkmaw', 0, 100); });
await page.waitForTimeout(800);
const b = await page.evaluate(() => ({ mood: window.__music.getMood(), step: window.__music.step, theme: window.__music.getTheme().id }));
console.log('menu', JSON.stringify(a), 'battle+boss', JSON.stringify(b));
// Frost region battle picks the frost theme; losing plays the defeat stinger and rests the loop.
await page.evaluate(() => window.__game.scene.getScene('Battle').scene.start('Battle', { levelIndex: 6 }));
await page.waitForTimeout(800);
const c = await page.evaluate(() => {
  const m = window.__music;
  const theme = m.getTheme().id;
  const before = m.nextTime - m.ctx.currentTime;
  window.__game.scene.getScene('Battle').endBattle(false);
  return { theme, restBefore: +before.toFixed(2), restAfter: +(m.nextTime - m.ctx.currentTime).toFixed(2), mood: m.getMood() };
});
console.log('frost battle + defeat', JSON.stringify(c));
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}-defeat.png` });
const stingerOk = c.theme === 'frost' && c.restAfter > 3 && b.theme === 'grove';
await page.mouse.click(1280 - 400, 40); // pause
await page.waitForTimeout(200);
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || a.step <= 0 || b.mood !== 'boss' || !stingerOk ? 1 : 0);
