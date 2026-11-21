#!/usr/bin/env python3
"""Thumbnails for the cartoon videos, drawn with the films' own rigs (so the thumbnail shows the same characters as the video).

    python3 thumb.py <episode id>          writes out/<id>/<id>_thumb.jpg (1920x1080) and one <short id>_thumb.jpg (1080x1920) per Short

The episode file holds THUMBS = {"<id>": {...}}: place, cam (cx, cy, w for 16:9; cx, cy, h for 9:16), actors [(kind, x, y, scale, flip, pose js with #P)],
props [(fn, x, y, scale)], words [(text, x, y, size, "sun" | "")] in picture pixels.
Rules checked here: 3 words at most, none of the title's words, no watermark."""
import os, sys, re, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import art, art2
GSAP = os.path.join(os.path.dirname(HERE), "vendor/package/dist/gsap.min.js"); FONT = os.path.join(os.path.dirname(HERE), "vendor/f/package/files/baloo-2-latin-800-normal.woff2")
KINDS = {"milo": lambda p: art.milo(p), "calf": lambda p: art.camel(p, 0, calf=True), "camel": lambda p: art.camel(p, 1), "bactrian": lambda p: art.camel(p, 2, c=art.CAMEL_B, wool=True)}


def words_ok(text, title):
    w = re.findall(r"[a-z']+", text.lower()); t = set(re.findall(r"[a-z']+", title.lower().replace("'s", "")))
    bad = [x for x in w if x in t]
    assert len(w) <= 3, f"thumbnail has {len(w)} words (3 at most): {text}"
    assert not bad, f"thumbnail repeats the title's words {bad}: '{text}' / '{title}'"


def build(tid, t, title, out, tall):
    words_ok(" ".join(w[0] for w in t["words"]), title)
    W, Hh = (1080, 1920) if tall else (1920, 1080); cx, cy, z = t["cam"]; s = (Hh / z) if tall else (W / z)
    far, mid, near = art.BG[t["place"]]("t"); js = []; body = ""
    for k, a in enumerate(t.get("actors", [])):
        kind, x, y, sc = a[:4]; flip = len(a) > 4 and a[4]; pose = a[5] if len(a) > 5 else ""; pid = f"a{k}"
        inner = KINDS[kind](pid) if kind in KINDS else art2.RIGS[kind]["build"](pid)
        body += f'<g transform="translate({x} {y}) scale({-sc if flip else sc} {sc})">{inner}</g>'; js.append(pose.replace("#P", "#" + pid))
    for k, pr in enumerate(t.get("props", [])):
        fn, x, y, sc = pr[:4]; body += f'<g transform="translate({x} {y}) scale({sc})">{fn(f"p{k}")}</g>'
    wd = "".join(f'<div class="w {w[4] if len(w) > 4 else ""}" style="left:{w[1]}px;top:{w[2]}px;font-size:{w[3]}px;transform:translate(-50%,-50%) rotate({w[5] if len(w) > 5 else -4}deg)">{w[0]}</div>' for w in t["words"])
    html = (f'<!doctype html><meta charset="utf-8"><style>@font-face{{font-family:Baloo;src:url(file://{FONT})}}*{{margin:0;padding:0}}body{{width:{W}px;height:{Hh}px;overflow:hidden}}'
            f'#root{{position:relative;width:{W}px;height:{Hh}px;overflow:hidden;font-family:Baloo,sans-serif}}svg{{position:absolute;left:0;top:0;overflow:visible;transform-origin:0 0;'
            f'transform:translate({W / 2 - cx * s:.1f}px,{Hh / 2 - cy * s:.1f}px) scale({s:.4f})}}'
            f'.w{{position:absolute;white-space:nowrap;color:#fff;-webkit-text-stroke:26px #402010;paint-order:stroke fill;line-height:1;letter-spacing:.01em;filter:drop-shadow(0 14px 0 rgba(64,32,16,.28))}}.w.sun{{color:#ffd23f}}</style>'
            f'<script src="file://{GSAP}"></script><div id="root"><svg width="1920" height="1080" viewBox="0 0 1920 1080">{far}{mid}{near}{body}</svg>{wd}</div>')
    f = out.replace(".jpg", ".html"); open(f, "w").write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": Hh}); pg.goto("file://" + f); pg.wait_for_timeout(500)
        if "".join(js): pg.evaluate("".join(js))
        pg.wait_for_timeout(200); pg.screenshot(path=out, type="jpeg", quality=92); b.close()
    os.remove(f); print(out, os.path.getsize(out) // 1024, "KB")


def main():
    mod = importlib.import_module("episodes." + sys.argv[1]); ep = mod.EP; out = os.path.join(HERE, "out", ep["id"]); os.makedirs(out, exist_ok=True)
    for tid, t in mod.THUMBS.items():
        title = ep["title"] if tid == ep["id"] else next(s["title"] for s in mod.SHORTS if s["id"] == tid)
        build(tid, t, title, os.path.join(out, tid + "_thumb.jpg"), tall=tid != ep["id"])


if __name__ == "__main__": main()
