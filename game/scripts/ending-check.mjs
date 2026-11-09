// Opens the ending scene and screenshots it after the dawn animation.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const server = await preview({ preview: { port: 4329, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
await page.goto('http://localhost:4329/');
await page.waitForTimeout(900);
await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('Ending'));
// the body types itself out: wait until it shows the star count line (scene clock, headless frames are slow)
await page.waitForFunction(() => {
  const list = window.__game.scene.getScene('Ending').children.list;
  const typed = list.some((o) => typeof o.text === 'string' && o.alpha === 1 && /Stars earned: \d+ \/ \d+$/.test(o.text));
  return typed && list.some((o) => o.label?.text === 'Main Menu');
}, null, { timeout: 60000, polling: 500 });
await page.waitForTimeout(800);
await page.screenshot({ path: `screenshots/${process.argv[2] ?? 'ending'}.png` });
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length ? 1 : 0);
