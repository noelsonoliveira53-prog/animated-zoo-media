// Design sheet: lays out every generated texture whose key starts with <prefix> (hero_, enemy_, tower_, troop_,
// bld_, ...) in an enlarged grid on a plain backdrop, for before/after art comparisons.
// `node scripts/design-sheet.mjs <name> <prefix> [scale] [filter-regex]`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const [name = 'sheet', prefix = 'hero_', scaleArg = '2', filter = ''] = process.argv.slice(2);
const server = await preview({ preview: { port: 4367, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto('http://localhost:4367/');
await page.waitForTimeout(1200);
const n = await page.evaluate(([prefix, scale, filter]) => {
  const game = window.__game;
  const s = game.scene.getScene('Menu');
  s.children.list.slice().forEach((o) => o.setVisible?.(false));
  s.tweens.pauseAll();
  const keys = game.textures.getTextureKeys().filter((k) => k.startsWith(prefix) && (!filter || new RegExp(filter).test(k))).sort();
  const g = s.add.graphics().setDepth(9000);
  g.fillStyle(0x6a9a5a, 1); // a grass-ish backdrop like the battlefield
  g.fillRect(0, 0, 1280, 720);
  const cols = Math.max(1, Math.floor(1260 / (64 * scale + 12)));
  keys.forEach((k, i) => {
    const x = 20 + (i % cols) * (64 * scale + 12) + 32 * scale;
    const y = 30 + Math.floor(i / cols) * (74 * scale + 22) + 34 * scale;
    s.add.image(x, y, k).setScale(scale).setDepth(9001);
    s.add.text(x, y + 38 * scale, k.slice(prefix.length), { fontFamily: 'sans-serif', fontSize: '12px', color: '#10261b' }).setOrigin(0.5).setDepth(9001);
  });
  return keys.length;
}, [prefix, Number(scaleArg), filter]);
await page.waitForTimeout(400);
await page.screenshot({ path: `screenshots/${name}.png` });
console.log(JSON.stringify({ textures: n }));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no page errors');
await browser.close();
server.httpServer.close();
