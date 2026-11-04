// Render a Three.js scene frame-by-frame in headless Chromium and encode to MP4.
// node render3d.js --out out.mp4 [--dur 8] [--fps 24] [--w 1280] [--h 720] [--audio voice.wav] [--mouth mouth.json]
const { chromium } = require("playwright");
const http = require("http"), fs = require("fs"), path = require("path"), { spawn } = require("child_process");
const arg = (k, d) => { const i = process.argv.indexOf("--" + k); return i > 0 ? process.argv[i + 1] : d; };
const out = arg("out", "milo3d.mp4"), dur = +arg("dur", 8), fps = +arg("fps", 24), w = +arg("w", 1280), h = +arg("h", 720);
const audio = arg("audio"), mouth = arg("mouth") ? JSON.parse(fs.readFileSync(arg("mouth"))) : null;
const ROOT = __dirname, TYPES = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json" };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split("?")[0]));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(p)] || "application/octet-stream" }); fs.createReadStream(p).pipe(res);
});
(async () => {
  await new Promise(r => server.listen(0, "127.0.0.1", r));
  const port = server.address().port;
  const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  page.on("pageerror", e => console.error("PAGE ERROR", e.message));
  await page.goto(`http://127.0.0.1:${port}/scene.html`);
  await page.waitForFunction(() => window.ready === true, null, { timeout: 30000 });
  await page.evaluate(c => window.setup(c), { w, h, fps, dur, mouth });
  const ffArgs = ["-y", "-f", "image2pipe", "-vcodec", "mjpeg", "-framerate", String(fps), "-i", "-"];
  if (audio) ffArgs.push("-i", audio);
  ffArgs.push("-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p");
  if (audio) ffArgs.push("-c:a", "aac", "-b:a", "160k", "-shortest");
  ffArgs.push(out);
  const ff = spawn("ffmpeg", ffArgs, { stdio: ["pipe", "ignore", "inherit"] });
  const total = Math.round(dur * fps), t0 = Date.now();
  for (let f = 0; f < total; f++) {
    const url = await page.evaluate(t => window.renderAt(t), f / fps);
    const buf = Buffer.from(url.split(",")[1], "base64");
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
    if (f % 24 === 0) process.stdout.write(`frame ${f}/${total} ${((Date.now() - t0) / 1000).toFixed(0)}s\n`);
  }
  ff.stdin.end(); await new Promise(r => ff.on("close", r));
  await browser.close(); server.close();
  console.log("DONE", out, ((Date.now() - t0) / 1000).toFixed(0) + "s");
})().catch(e => { console.error(e); process.exit(1); });
