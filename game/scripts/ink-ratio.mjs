// Ink-ratio scan: `node scripts/ink-ratio.mjs [prefix] [top]` — renders every texture with the prefix (default enemy_)
// and lists the ones where near-ink pixels make up the largest share of the sprite: slim parts drowned by outlines.
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const [prefix = 'enemy_', topArg = '15'] = process.argv.slice(2);
const server = await preview({ preview: { port: 4339, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
await page.goto('http://localhost:4339/');
await page.waitForTimeout(2500);
const rows = await page.evaluate((prefix) => {
  const tm = window.__game.textures;
  const out = [];
  for (const key of tm.getTextureKeys().filter((k) => k.startsWith(prefix))) {
    const src = tm.get(key).getSourceImage();
    const c = document.createElement('canvas');
    c.width = src.width; c.height = src.height;
    const ctx = c.getContext('2d');
    ctx.drawImage(src, 0, 0);
    const d = ctx.getImageData(0, 0, c.width, c.height).data;
    let solid = 0, ink = 0;
    for (let i = 0; i < d.length; i += 4) {
      if (d[i + 3] < 200) continue; // skip shadows and soft glows
      solid++;
      if (d[i] < 60 && d[i + 1] < 70 && d[i + 2] < 60) ink++;
    }
    if (solid > 30) out.push({ key, ink: Math.round((ink / solid) * 100) });
  }
  return out.sort((a, b) => b.ink - a.ink);
}, prefix);
const top = +topArg;
console.log(rows.slice(0, top).map((r) => `${r.ink}%  ${r.key}`).join('\n'));
const avg = rows.reduce((s, r) => s + r.ink, 0) / rows.length;
console.log(`median ${rows[Math.floor(rows.length / 2)].ink}%  mean ${avg.toFixed(1)}%  (${rows.length} sprites)`);
await browser.close();
server.httpServer.close();
