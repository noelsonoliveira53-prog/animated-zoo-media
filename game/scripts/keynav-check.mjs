// Keyboard-only play check: `node scripts/keynav-check.mjs` — from the main menu, reach a battle using only Tab / arrows / Enter.
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const server = await preview({ preview: { port: 4331, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));
await page.addInitScript(() => {
  localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 2 }, seenStory: true }));
  window.__noTouchTip = true;
});
await page.goto('http://localhost:4331/');
await page.waitForTimeout(2000);
const state = () => page.evaluate(() => {
  const g = window.__game;
  const top = g.scene.getScenes(true, true).find((s) => s.keyNav && s.keyNav.targets().length) ?? g.scene.getScenes(true, true)[0];
  return { scene: top.sys.settings.key, focus: top.keyNav?.focusedLabel() ?? '', targets: top.keyNav?.targets().map((t) => lab(t.obj) || '?') ?? [] };
  function lab(o) { if (typeof o.text === 'string') return o.text; for (const c of o.list ?? []) { const s = lab(c); if (s) return s; } return ''; }
});
const key = async (k, n = 1) => { for (let i = 0; i < n; i++) { await page.keyboard.press(k); await page.waitForTimeout(120); } };
const log = [];
await page.mouse.move(5, 5);
let s = await state(); log.push(['menu', s.scene, s.targets.join(' | ')]);
await key('Tab');
s = await state(); log.push(['tab', s.focus]);
await page.waitForTimeout(300);
await page.screenshot({ path: 'screenshots/fix-1-menu.png' });
await key('ArrowDown');
s = await state(); log.push(['down', s.focus]);
for (let i = 0; i < 15 && s.focus !== 'Campaign'; i++) { await key('Tab'); s = await state(); }
log.push(['campaign?', s.focus]);
await key('Enter');
await page.waitForTimeout(2500);
s = await state(); log.push(['after enter', s.scene, s.targets.join(' | ')]);
// on the map: Tab until a level node with label containing "1" or the first node is focused, then Enter
for (let i = 0; i < 40 && s.scene === 'WorldMap'; i++) {
  await key('Tab');
  s = await state();
  if (/^1$|^1\b/.test(s.focus)) break;
}
log.push(['map focus', s.focus]);
await page.waitForTimeout(300);
await page.screenshot({ path: 'screenshots/fix-1-map.png' });
await key('Enter');
await page.waitForTimeout(1200);
s = await state(); log.push(['card', s.scene, s.targets.join(' | ')]);
log.push(['card focus', s.focus]);
await page.screenshot({ path: 'screenshots/fix-1-card.png' });
await key('Enter');
await page.waitForTimeout(3000);
s = await state(); log.push(['battle', s.scene, s.targets.join(' | ')]);
await key('Tab');
await page.waitForTimeout(300);
s = await state(); log.push(['battle focus', s.focus]);
await page.screenshot({ path: 'screenshots/fix-1-battle.png' });
const ok = s.scene === 'Battle';
console.log(JSON.stringify(log, null, 1));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || !ok ? 1 : 0);
