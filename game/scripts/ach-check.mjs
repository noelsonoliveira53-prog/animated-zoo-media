// Wins a battle (forced) to trigger achievement toasts, then opens the Achievements screen.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'ach';
const server = await preview({ preview: { port: 4334, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await page.goto('http://localhost:4334/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 0 }));
await page.waitForTimeout(800);
await page.evaluate(() => { const s = window.__game.scene.getScene('Battle'); s.tally.kills = 520; s.endBattle(true); });
await page.waitForTimeout(900);
await page.screenshot({ path: `screenshots/${name}-toast.png` });
const saved = await page.evaluate(() => { const s = JSON.parse(localStorage.getItem('grovewatch.save.v1')); return { ach: s.achievements, stats: s.stats, coins: Math.floor(s.village?.coins ?? 0) }; });
console.log('saved', JSON.stringify(saved));
await page.evaluate(() => window.__game.scene.getScene('Battle').scene.start('Achievements'));
await page.waitForTimeout(600);
await page.screenshot({ path: `screenshots/${name}-list.png` });
// Page 2 via the ">" button (real click), then back to page 1 with "<".
await page.mouse.click(1280 - 70, 44);
await page.waitForTimeout(500);
const page2 = await page.evaluate(() => window.__game.scene.getScene('Achievements').children.getByName('pageLabel')?.text);
await page.screenshot({ path: `screenshots/${name}-page2.png` });
await page.mouse.click(1280 - 210, 44);
await page.waitForTimeout(500);
const page1 = await page.evaluate(() => window.__game.scene.getScene('Achievements').children.getByName('pageLabel')?.text);
console.log('pages', page2, page1);
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || page2 !== '2/2' || page1 !== '1/2' ? 1 : 0);
