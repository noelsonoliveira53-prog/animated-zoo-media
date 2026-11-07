// Close-up of enemy sprites at 2.2×: `node scripts/enemy-sprites.mjs <out.png> [id,id,...]`.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { preview } from 'vite';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const server = await preview({ preview: { port: 4324, strictPort: true } });
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
await page.goto('http://localhost:4324/');
await page.waitForTimeout(1200);
const ids = (process.argv[3] ?? 'morrowcap,puffcap,veilstalker,rootrager,vulkhar').split(',');
await page.evaluate((ids) => {
  const s = window.__game.scene.getScene('Menu');
  const bg = s.add.rectangle(640, 360, 1280, 720, 0x4a5a78).setDepth(9000);
  ids.forEach((id, i) => s.add.image(180 + i * 230, 360, `enemy_${id}`).setScale(2.2).setDepth(9001));
}, ids);
await page.waitForTimeout(300);
await page.screenshot({ path: process.argv[2] });
await browser.close();
server.httpServer.close();
