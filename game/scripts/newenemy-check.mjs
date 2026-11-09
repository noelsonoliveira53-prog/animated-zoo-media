// "New!" tags in the next-wave strip: a save that has met only Mudlings opens a level whose first wave brings others.
// Checks the tags and the one-line tip appear, then that a seen-everything save shows none. `node scripts/newenemy-check.mjs <name>`
import { createRequire } from 'node:module';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
const pw = require('playwright');
const name = process.argv[2] ?? 'newenemy';
const server = await preview({ preview: { port: 4338, strictPort: true } });
const browser = await pw.chromium.launch();
const errors = [];
const out = {};
for (const mode of ['fresh', 'veteran']) {
  // PHONE=1: a 740×360 touch phone instead of desktop
const page = process.env.PHONE ? await (await browser.newContext({ viewport: { width: 740, height: 360 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 })).newPage() : await browser.newPage({ viewport: { width: 1280, height: 720 } });
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.addInitScript((m) => {
    const all = m === 'veteran';
    localStorage.setItem('grovewatch.save.v1', JSON.stringify({ stars: { l1: 3 }, seenEnemies: all ? ['__all__'] : ['mudling'] }));
  }, mode);
  await page.goto('http://localhost:4338/');
  await page.waitForTimeout(900);
  await page.evaluate((m) => {
    if (m === 'veteran') {
      // mark every enemy seen through the game's own data
      const ids = window.__game.textures.getTextureKeys().filter((k) => k.startsWith('enemy_')).map((k) => k.slice(6));
      const s = JSON.parse(localStorage.getItem('grovewatch.save.v1'));
      s.seenEnemies = ids;
      localStorage.setItem('grovewatch.save.v1', JSON.stringify(s));
    }
    window.__game.scene.getScene('Menu').scene.start('Battle', { levelIndex: 2 }); // its first wave mixes Mudlings with something new
  }, mode);
  await page.waitForTimeout(1800);
  out[mode] = await page.evaluate(() => {
    const s = window.__game.scene.getScene('Battle');
    const strip = s.children.getByName('wavePreview');
    const tags = strip ? strip.list.filter((o) => o.type === 'Container').length : -1;
    const tip = s.children.getByName('newEnemyTip');
    return { tags, tip: tip ? tip.list.find((o) => o.type === 'Text').text : null };
  });
  if (mode === 'fresh') await page.screenshot({ path: `screenshots/${name}.png`, ...(process.env.PHONE ? {} : { clip: { x: 300, y: 0, width: 760, height: 120 } }) });
  await page.close();
}
console.log(JSON.stringify(out));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no console errors');
await browser.close();
server.httpServer.close();
process.exit(errors.length || out.fresh.tags < 1 || !out.fresh.tip || out.veteran.tags !== 0 || out.veteran.tip ? 1 : 0);
