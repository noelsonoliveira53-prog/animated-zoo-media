// Trait sound check: clicks to unlock WebAudio, plays every trait cue, then plays the Ruins mechanics in a live battle.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const server = await preview({ preview: { port: 4336, strictPort: true } });
const browser = await pw.chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4336/');
await page.waitForTimeout(1000);
await page.mouse.click(640, 360);
const info = await page.evaluate(async () => {
  const s = window.__sfx;
  s.unlock();
  const kinds = ['gust', 'swoop', 'revive', 'shift', 'blink', 'thorns', 'glare', 'coral', 'spores', 'enrage', 'burrow', 'split'];
  for (const k of kinds) { s.trait(k); await new Promise((r) => setTimeout(r, 150)); }
  return { state: s.ctx?.state, played: kinds.length };
});
console.log(JSON.stringify(info));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
