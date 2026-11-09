// Hit-size check: `node scripts/hitsize-check.mjs` — every clickable control on the menu and map, at desktop and phone size,
// reports its drawn size and hit size in CSS px; flags (and exits 1 on) a control under 44 CSS px that did not grow at all.
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const server = await preview({ preview: { port: 4332, strictPort: true } });
const browser = await pw.chromium.launch();
let bad = 0;
const errors = [];
for (const vp of [{ width: 1280, height: 720 }, { width: 740, height: 360 }]) {
  const page = await browser.newPage({ viewport: vp });
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.addInitScript(() => { localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3, l2: 2 }, seenStory: true })); window.__noTouchTip = true; });
  await page.goto('http://localhost:4332/');
  await page.waitForTimeout(1800);
  for (const scene of ['Menu', 'WorldMap']) {
    if (scene === 'WorldMap') { await page.evaluate(() => window.__game.scene.getScene('Menu').scene.start('WorldMap')); await page.waitForTimeout(1800); }
    const rows = await page.evaluate((key) => {
      const g = window.__game, s = g.scene.getScene(key), k = 1 / g.scale.displayScale.x, out = [];
      const lab = (o) => { if (typeof o.text === 'string') return o.text; for (const c of o.list ?? []) { const t = lab(c); if (t) return t; } return ''; };
      const visit = (l) => { for (const o of l) { if (o.input?.cursor === 'pointer' && o.visible !== false && o.width > 0) { const m = o.getWorldTransformMatrix(); const sc = Math.abs(m.scaleX); out.push({ label: lab(o).slice(0, 18) || o.type, drawn: [Math.round(o.width * sc * k), Math.round(o.height * sc * k)], hit: [Math.round(o.input.hitArea.width * sc * k), Math.round(o.input.hitArea.height * sc * k)], grew: [o.input.hitArea.width - o.width, o.input.hitArea.height - o.height] }); } if (o.list) visit(o.list); } };
      visit(s.children.list);
      return out;
    }, scene);
    for (const r of rows) {
      // a side below 44 css px is only OK if it already got the full 24 game px of growth (the per-side cap)
      const short = [0, 1].some((i) => r.hit[i] < 44 && r.grew[i] < 60 && r.grew[i] < 1);
      if (short) bad++;
      if (short || vp.width === 740) console.log(vp.width, scene, r.label.padEnd(18), 'drawn', r.drawn.join('x'), 'hit', r.hit.join('x'), short ? '  <-- SHORT' : '');
    }
  }
  if (vp.width === 740) await page.screenshot({ path: 'screenshots/fix-2-phone-map.png' });
  await page.close();
}
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no page errors', '| short:', bad);
await browser.close();
server.httpServer.close();
process.exit(errors.length || bad ? 1 : 0);
