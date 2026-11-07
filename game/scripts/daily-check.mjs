// Starts the daily challenge from the menu, screenshots the banner, forces a win, checks the reward.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'daily';
const server = await preview({ preview: { port: 4335, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await page.addInitScript(() => {
  if (!localStorage.getItem('grovewatch.save.v1')) localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 2, l3: 2, l4: 1, l5: 1, l6: 1 } }));
});
await page.goto('http://localhost:4335/');
await page.waitForTimeout(900);
await page.screenshot({ path: `screenshots/${name}-menu.png` });
await page.mouse.click(460, 562); // Daily
await page.waitForTimeout(900);
await page.screenshot({ path: `screenshots/${name}-battle.png` });
const info = await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); return { level: s.level.id, mods: s.daily.modifiers, lives: s.sim.lives, coins: s.sim.coins, hero: !!s.sim.hero }; });
console.log('daily', JSON.stringify(info));
await page.evaluate(() => window.__game.scene.getScene('Battle').endBattle(true));
await page.waitForTimeout(800);
await page.screenshot({ path: `screenshots/${name}-win.png` });
const after = await page.evaluate(() => JSON.parse(localStorage.getItem('grovewatch.save.v1')).dailyDone);
console.log('dailyDone', after);
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
