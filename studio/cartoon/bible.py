#!/usr/bin/env python3
"""Style-bible sheets, drawn by the same art.py the films use (so the bible can never drift from the films).

    python3 bible.py <out_dir>

Writes milo_sheet.png, camel_sheet.png, places.png: every pose is the film's own rig with the film's own moves
(the same part ids, the same pivots as toon.py), held still.
"""
import os, sys, json
import art

HERE = os.path.dirname(os.path.abspath(__file__))
GSAP = os.path.join(HERE, "out", "zc_ep01", "proj_l", "assets", "gsap.min.js")
FONT = os.path.join(HERE, "out", "zc_ep01", "proj_l", "assets", "baloo.woff2")

# (label, pose js for pid "P") - the moves are the ones toon.py plays
MILO = [
    ("Rest", ""),
    ("Talking", 'gsap.set("#P-beak",{y:24});'),
    ("Asking", 'gsap.set("#P-beak",{y:16});gsap.set("#P-browL,#P-browR",{y:-12});'),
    ("Blink", 'gsap.set("#P-eyeL-lid,#P-eyeR-lid",{opacity:1});'),
    ("Flying, wings up", 'gsap.set("#P-shadow",{opacity:0});gsap.set("#P-legs",{y:-14});gsap.set("#P-wl",{rotation:46,svgOrigin:"-96 -182"});gsap.set("#P-wr",{rotation:-46,svgOrigin:"96 -182"});'),
    ("Flying, wings down", 'gsap.set("#P-shadow",{opacity:0});gsap.set("#P-legs",{y:-14});gsap.set("#P-wl",{rotation:-8,svgOrigin:"-96 -182"});gsap.set("#P-wr",{rotation:8,svgOrigin:"96 -182"});'),
    ("Squash (hop lands)", 'gsap.set("#P-body",{scaleY:.9,scaleX:1.08,svgOrigin:"0 0"});'),
    ("Stretch (hop rises)", 'gsap.set("#P-body",{scaleY:1.08,scaleX:.94,svgOrigin:"0 0"});gsap.set("#P",{y:-40});'),
]
CAMELS = [
    ("Mama: rest", dict(humps=1), ""),
    ("Mama: looks up", dict(humps=1), 'gsap.set("#P-neck",{rotation:-14,svgOrigin:"190 -330"});'),
    ("Mama: bends to drink", dict(humps=1), 'gsap.set("#P-neck",{rotation:62,svgOrigin:"190 -330"});'),
    ("Mama: chews", dict(humps=1), 'gsap.set("#P-jaw",{rotation:9,x:6,svgOrigin:"372 -560"});'),
    ("Mama: slow blink", dict(humps=1), 'gsap.set("#P-eye-lid",{opacity:1});'),
    ("Mama: hump used up", dict(humps=1), 'gsap.set("#P-hump",{rotation:28,scaleY:.72,scaleX:.94,svgOrigin:"0 -372"});'),
    ("Sandy the calf: rest", dict(humps=0, calf=True), ""),
    ("Sandy: looks up", dict(humps=0, calf=True), 'gsap.set("#P-neck",{rotation:-16,svgOrigin:"190 -330"});'),
    ("Sandy: walks", dict(humps=0, calf=True), 'gsap.set("#P-fl",{rotation:-13,svgOrigin:"160 -262"});gsap.set("#P-bl",{rotation:13,svgOrigin:"-138 -262"});gsap.set("#P-fl2",{rotation:13,svgOrigin:"118 -262"});gsap.set("#P-bl2",{rotation:-13,svgOrigin:"-178 -262"});'),
    ("Sandy, older: the hump has grown", dict(humps=1, calf=True), 'gsap.set("#P-hump",{scaleY:.7,scaleX:.8,svgOrigin:"0 -372"});'),
    ("Bactrian cousin: two humps", dict(humps=2, c=art.CAMEL_B, wool=True), ""),
    ("Bactrian: nods", dict(humps=2, c=art.CAMEL_B, wool=True), 'gsap.set("#P-neck",{rotation:14,svgOrigin:"190 -330"});'),
]
CSS = """@font-face{font-family:Baloo;src:url(file://%s)}*{box-sizing:border-box}body{margin:0;background:#fff6e0;font-family:Baloo,sans-serif;color:#402010}
.grid{display:grid;gap:18px;padding:24px}.cell{background:#fffdf6;border:3px solid #f0e2c0;border-radius:22px;padding:10px 10px 6px;text-align:center}
.cell svg{display:block;width:100%%;height:auto}.cell b{display:block;font-size:26px;line-height:1.5}""" % FONT


def page(cells, cols, w):
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS}.grid{{grid-template-columns:repeat({cols},1fr);width:{w}px}}</style><script src="file://{GSAP}"></script>'
            f'<div class="grid" id="g">{"".join(cells)}</div>')


def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    jobs = []
    cells, js = [], []
    for k, (label, pose) in enumerate(MILO):
        pid = f"m{k}"; cells.append(f'<div class="cell"><svg viewBox="-230 -450 460 490">{art.milo(pid)}</svg><b>{label}</b></div>'); js.append(pose.replace("#P", "#" + pid))
    jobs.append(("milo_sheet.png", page(cells, 4, 1600), "".join(js)))
    cells, js = [], []
    for k, (label, kw, pose) in enumerate(CAMELS):
        pid = f"c{k}"; calf = kw.get("calf"); vb = "-330 -800 1010 860"
        cells.append(f'<div class="cell"><svg viewBox="{vb}">{art.camel(pid, **kw)}</svg><b>{label}</b></div>'); js.append(pose.replace("#P", "#" + pid))
    jobs.append(("camel_sheet.png", page(cells, 3, 1800), "".join(js)))
    cells = []
    for k, name in enumerate(["dunes", "trail", "oasis", "wind", "gobi", "night", "zoo", "paper", "paper_blue", "paper_pink"]):
        far, mid, near = art.BG[name](f"b{k}")
        cells.append(f'<div class="cell"><svg viewBox="0 0 1920 1080">{far}{mid}{near}</svg><b>{art.PLACE.get(name, name.replace("_", " ") + " picture board")}</b></div>')
    jobs.append(("places.png", page(cells, 5, 2400), ""))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(device_scale_factor=1.5)
        for name, html, js in jobs:
            f = os.path.join(out, name.replace(".png", ".html")); open(f, "w").write(html)
            pg.goto("file://" + f); pg.wait_for_timeout(400)
            if js: pg.evaluate(js)
            pg.wait_for_timeout(200); pg.locator("#g").screenshot(path=os.path.join(out, name)); os.remove(f); print(os.path.join(out, name))
        b.close()


if __name__ == "__main__": main()
