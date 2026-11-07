// Field Guide paging check: inflates the enemy list to 40 entries (in-browser only) so a second page exists,
// then flips pages with the real "<" / ">" buttons and screenshots both.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const name = process.argv[2] ?? 'guide-paging';
const server = await preview({ preview: { port: 4328, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4328/');
await page.waitForTimeout(1000);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('FieldGuide'));
await page.waitForTimeout(800);
await page.evaluate(() => {
  const g = window.__game.scene.getScene('FieldGuide');
  const orig = g.entries.bind(g);
  g.entries = () => {
    const base = orig();
    return g.tab === 'enemies' ? [...base, ...base.slice(0, 40 - base.length)] : base;
  };
  g.show('enemies');
});
await page.waitForTimeout(400);
const label = () => page.evaluate(() => window.__game.scene.getScene('FieldGuide').grid.list.find((o) => o.name === 'guidePage')?.text);
const p1 = await label();
await page.screenshot({ path: `screenshots/${name}-1.png` });
await page.mouse.click(670, 720 - 58);
await page.waitForTimeout(400);
const p2 = await label();
await page.screenshot({ path: `screenshots/${name}-2.png` });
console.log('pages', p1, p2);
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || p1 !== '1/2' || p2 !== '2/2' ? 1 : 0);
