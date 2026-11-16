#!/usr/bin/env python3
"""Style-bible sheets, drawn by the same art.py the films use (so the bible can never drift from the films).

    python3 bible.py <out_dir>

Writes milo_sheet.png, camel_sheet.png, places.png: every pose is the film's own rig with the film's own moves
(the same part ids, the same pivots as toon.py), held still.
"""
import os, sys, json
import art, art2

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
            f'<div class="grid" id="GRID">{"".join(cells)}</div>')


SAD1 = 'gsap.set("#P-brow",{rotation:-16,y:-4,transformOrigin:"50% 50%"});gsap.set("#P-smile",{opacity:0});gsap.set("#P-frown",{opacity:1});'
WOW1 = 'gsap.set("#P-brow",{y:-14,transformOrigin:"50% 50%"});gsap.set("#P-jaw",{opacity:1,y:12});'
TALK = 'gsap.set("#P-jaw",{opacity:1,y:12});'
ELE_VB = "-380 -820 1040 880"
TUMBLE = [
    ("Rest", ""), ("Talking", TALK), ("Worried", SAD1 + 'gsap.set("#P-ear",{rotation:12,svgOrigin:"250 -590"});gsap.set("#P-neck",{rotation:9,svgOrigin:"200 -420"});'),
    ("Surprised", WOW1 + 'gsap.set("#P-ear",{rotation:-10,svgOrigin:"250 -590"});'), ("Blink", 'gsap.set("#P-eye-lid",{opacity:1});'),
    ("Trunks up!", 'gsap.set("#P-trunk",{rotation:-150,svgOrigin:"392 -430"});'), ("Trunk as a snorkel", 'gsap.set("#P-trunk",{rotation:-160,scaleY:1.35,svgOrigin:"392 -430"});'),
    ("Walks", 'gsap.set("#P-fl",{rotation:-13,svgOrigin:"150 -250"});gsap.set("#P-bl",{rotation:13,svgOrigin:"-140 -250"});gsap.set("#P-fl2",{rotation:13,svgOrigin:"96 -250"});gsap.set("#P-bl2",{rotation:-13,svgOrigin:"-196 -250"});'),
]
MAMA_E = [("Mama Elephant: rest", dict(), ""), ("Mama: talking", dict(), TALK), ("Mama: trunk hug", dict(), 'gsap.set("#P-trunk",{rotation:34,svgOrigin:"392 -430"});gsap.set("#P-neck",{rotation:8,svgOrigin:"200 -420"});'),
          ("Mama: birthday hat", dict(hat=True), 'gsap.set("#P-eye-lid",{opacity:1});')]
SAD2 = 'gsap.set("#P-browL",{rotation:-16,y:-4,transformOrigin:"50% 50%"});gsap.set("#P-browR",{rotation:16,y:-4,transformOrigin:"50% 50%"});gsap.set("#P-smile",{opacity:0});gsap.set("#P-frown",{opacity:1});'
MANGO = [("Rest", False, ""), ("Talking", False, TALK), ("Worried", False, SAD2), ("Hooray", False, 'gsap.set("#P-al",{rotation:60,svgOrigin:"-58 -206"});gsap.set("#P-ar",{rotation:-60,svgOrigin:"58 -206"});'),
         ("Blink", False, 'gsap.set("#P-eyeL-lid,#P-eyeR-lid",{opacity:1});'), ("Hangs by her tail", True, ""), ("Hangs and reaches", True, 'gsap.set("#P-al",{rotation:42,svgOrigin:"-58 -206"});'),
         ("Hangs and talks", True, TALK)]
FRIENDS = [("Poppy the polar bear cub", art2.bear, "-320 -500 760 540", ""), ("Poppy: worried", art2.bear, "-320 -500 760 540", SAD1), ("Clover the lamb", art2.lamb, "-320 -520 760 560", ""), ("Clover: talking", art2.lamb, "-320 -520 760 560", TALK),
           ("Hazel the hedgehog", art2.hedgehog, "-320 -400 720 440", ""), ("Hazel: surprised", art2.hedgehog, "-320 -400 720 440", WOW1), ("Tula the sea turtle", art2.turtle, "-320 -400 760 520", ""), ("Tula: worried", art2.turtle, "-320 -400 760 520", SAD1)]
PLACES = ["zoo", "zoo_eve", "savanna", "river", "jungle", "bigtree", "canopy", "dunes", "dune_eve", "oasis", "trail", "wind", "night", "gobi", "ocean", "arctic", "farm", "nightforest", "paper", "paper_blue", "paper_pink"]


def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    jobs = []

    def sheet(name, items, cols, w):
        cells, js = [], []
        for k, (label, svg_fn, vb, pose) in enumerate(items):
            pid = f"x{k}"; cells.append(f'<div class="cell"><svg viewBox="{vb}">{svg_fn(pid)}</svg><b>{label}</b></div>'); js.append(pose.replace("#P", "#" + pid))
        jobs.append((name, page(cells, cols, w), "".join(js)))
    sheet("milo_sheet.png", [(l, art.milo, "-230 -450 460 490", p) for l, p in MILO], 4, 1600)
    sheet("camel_sheet.png", [(l, (lambda kw: (lambda pid: art.camel(pid, **kw)))(kw), "-330 -800 1010 860", p) for l, kw, p in CAMELS], 4, 2200)
    sheet("tumble_sheet.png", [(l, lambda pid: art2.elephant(pid, calf=True), "-380 -760 1000 820", p) for l, p in TUMBLE], 4, 2200)
    sheet("mama_elephant_sheet.png", [(l, (lambda kw: (lambda pid: art2.elephant(pid, **kw)))(kw), "-380 -900 1040 960", p) for l, kw, p in MAMA_E], 4, 2200)
    sheet("mango_sheet.png", [(l, (lambda h: (lambda pid: art2.monkey(pid, hang=h)))(h), "-300 -80 600 680" if h else "-300 -470 620 510", p) for l, h, p in MANGO], 4, 1800)
    sheet("friends_sheet.png", FRIENDS, 4, 2200)
    cells = []
    for k, name in enumerate(PLACES):
        far, mid, near = art.BG[name](f"b{k}"); vb = "0 0 1920 1080"
        cells.append(f'<div class="cell"><svg viewBox="{vb}">{far}{mid}{near}</svg><b>{art.PLACE.get(name, name)}</b></div>')
    jobs.append(("places.png", page(cells, 4, 2400), ""))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(device_scale_factor=1)
        for name, html, js in jobs:
            f = os.path.join(out, name.replace(".png", ".html")); open(f, "w").write(html)
            pg.goto("file://" + f); pg.wait_for_timeout(400)
            if js: pg.evaluate(js)
            pg.wait_for_timeout(200); pg.locator("#GRID").screenshot(path=os.path.join(out, name)); os.remove(f); print(os.path.join(out, name))
        b.close()


if __name__ == "__main__": main()
