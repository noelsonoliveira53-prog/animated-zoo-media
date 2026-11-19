"""Gizmo Explains channel watermark (CLAUDE.md: every video and Short carries the channel mark; GIZMO_RUN.md: Gizmo's channel picture
+ "Gizmo Explains", not Milo). Same size, place and opacity as The Animated Zoo's mark (studio/zoo3d/watermark.py), which is not changed.

  python3 gizmo/wm.py avatar                    -> brand/gizmo/avatar_flat.png (800x800): Gizmo (gizmo_flat.svg.part, the banner drawing) on the channel blue
  python3 gizmo/wm.py build                     -> brand/gizmo/watermark.png (16:9 at 3840x2160) and watermark_short.png (9:16 at 2160x3840)
  python3 gizmo/wm.py check <video> [tl|tr]     -> "MARK yes/no" (the letters white, their outline dark, the disc channel-blue)
  python3 gizmo/wm.py corner <video> <out.jpg>  -> the mark's corner every 5 s on one sheet: LOOK at it

The real channel picture uploaded to YouTube is not in the repo; the avatar here is drawn from the same flat Gizmo as the banner."""
import os, sys, io, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "studio", "zoo3d"))
import watermark as W

AV = os.path.join(REPO, "brand", "gizmo", "avatar_flat.png")
W.WM = os.path.join(REPO, "brand", "gizmo", "watermark.png"); W.WM_SHORT = os.path.join(REPO, "brand", "gizmo", "watermark_short.png"); W.NAME = "Gizmo Explains"


def avatar():
    svg = open(os.path.join(HERE, "gizmo_flat.svg.part")).read()
    html = ('<!doctype html><style>*{margin:0}body{width:800px;height:800px;overflow:hidden}</style><svg width="800" height="800" viewBox="0 0 800 800">'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d3a8a"/><stop offset="1" stop-color="#3561d9"/></linearGradient></defs>'
            '<rect width="800" height="800" fill="url(#g)"/><circle cx="400" cy="400" r="330" fill="#5ff3ff" opacity=".18"/>'
            f'<g transform="translate(400 470) scale(1.02)">{svg}</g></svg>')
    f = AV.replace(".png", ".html"); open(f, "w").write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 800, "height": 800}); pg.goto("file://" + f); pg.wait_for_timeout(200); pg.screenshot(path=AV); b.close()
    os.remove(f); print(AV)


def build():
    from PIL import Image
    real = Image.open; crop_src = AV
    def fake_open(path, *a, **k):
        if path.endswith(os.path.join("brand", "avatar.png")): return real(crop_src)
        return real(path, *a, **k)
    Image.open = fake_open
    try: W.build()
    finally: Image.open = real


def has_mark(video, pos="tl", verbose=False, hide=None):
    """As watermark.has_mark, with the disc's channel blue (#1d3a8a..#3561d9) in place of Milo's yellow."""
    from PIL import Image
    w, h, _, dur, _ = W.probe(video); k = W.kind_of(w, h); sc, x, y, mw, mh = W.place(k, w, pos)
    m = Image.open(W.wm_file(k)).convert("RGBA").resize((mw, mh), Image.LANCZOS); px = m.load()
    white = [(i, j) for j in range(0, mh, 2) for i in range(0, mw, 2) if px[i, j][3] > 250 and min(px[i, j][:3]) > 245 and i > mh]
    brown = [(i, j) for j in range(0, mh, 2) for i in range(0, mw, 2) if px[i, j][3] > 250 and max(px[i, j][:3]) < 80 and i > mh]
    blue = [(i, j) for j in range(0, mh, 2) for i in range(0, mh, 2) if px[i, j][3] > 250 and px[i, j][2] > 120 and px[i, j][0] < 80 and px[i, j][1] < 120]
    hits = 0; hide = W.parse_hide(hide)
    free = [t / 2 for t in range(4, int(dur * 2) - 4) if not any(a - 1 <= t / 2 <= b + 1 for a, b in hide)]
    for f in (0.12, 0.3, 0.5, 0.7, 0.88):
        tt = min(free, key=lambda t: abs(t - dur * f)) if free else dur * f
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{tt:.2f}", "-i", video, "-frames:v", "1", "-vf", f"crop={mw}:{mh}:{x}:{y}", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if not raw: continue
        fp = Image.open(io.BytesIO(raw)).convert("RGB").load(); lum = lambda c: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
        a = sum(lum(fp[i, j]) for i, j in white) / max(1, len(white)); b = sum(lum(fp[i, j]) for i, j in brown) / max(1, len(brown))
        bb = [fp[i, j] for i, j in blue]; c = sum(1 for q in bb if q[2] > 110 and q[2] > q[0] + 50) / max(1, len(bb))
        ok = a > 205 and b < 125 and c > 0.8; hits += ok
        if verbose: print(f"  {tt:6.1f} s: letters {a:.0f}, outline {b:.0f}, blue {c:.2f} ({len(bb)} px) -> {'mark' if ok else 'no mark'}")
    return hits >= 4


W.has_mark = has_mark       # corner() asks has_mark() whether to lay the mark on

if __name__ == "__main__":
    c = sys.argv[1]; a = sys.argv[2:]
    if c == "avatar": avatar()
    elif c == "build": build()
    elif c == "check": r = has_mark(a[0], *(a[1:2]), verbose=True); print("MARK", "yes" if r else "no", a[0]); sys.exit(0 if r else 1)
    elif c == "corner": W.corner(a[0], a[1], *(a[2:3]))
