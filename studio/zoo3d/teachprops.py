"""Teaching props for LESSONS (Noelson, Nov 14 2026: "lessons should be interactive, not just the cartoon moving his body;
in-depth, with examples and images matching the items discussed"). Music videos do not use these.

  root = build(L, name, at, **opts)      # an empty at `at` with the prop built under it (faces -Y, ground at z = 0 of the root)
  animate(root, tr, dur, st)             # every frame while the prop is on screen; tr = seconds since it appeared

Job prop: {"type": "teach", "name": "<prop>", "at": [x, y, z], "delay": s, "dur": s, "spin": 0, "opts": {...}}
Interactive pieces: sign (answer choice; "win": seconds after which it is marked right and bounces), dots (thinking timer),
qbox (mystery box), badge (clue number), count (things that appear one by one on "times"), check / cross.
Examples: flies, mud, sun, snowflake, leaves, plate, pool, house2, ruler, cars, rings, town, swatch, fingerprint, magnifier,
butter, sock, ball, zzz, bones, thermo, bamboo, den, notree, heart, arrow.
"""
import math, os
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
_FONT = [None]
ANIM = {}     # root.name -> (prop name, opts, parts)


def _font():
    if _FONT[0] is None:
        for fn in ("Baloo2-ExtraBold.ttf", "Poppins-Bold.ttf"):
            p = os.path.join(HERE, "fonts", fn)
            if os.path.exists(p):
                try: _FONT[0] = bpy.data.fonts.load(p); break
                except Exception: pass
        if _FONT[0] is None: _FONT[0] = False
    return _FONT[0]


def _txt(L, body, size, loc, color, parent, extrude=0.06, emit=0.35):
    m = L.mat("TPtxt" + color, color, 0.35, coat=0.5, emission=color, emit=emit)
    o = L.text3d("TPText", body, size, loc, m, parent, extrude=extrude, bevel=0.012)
    if _font(): o.data.font = _font()
    return o


def _m(L, color, rough=0.4, coat=0.5, emit=0.0, alpha=1.0):
    return L.mat(f"TP{color}{rough}{coat}{emit}{alpha}", color, rough, coat=coat, emission=color if emit else None, emit=emit, alpha=alpha)


def _check(L, parent, loc, s=1.0, color="#18a03a"):
    r = L.empty("TPCheck", loc, parent); m = _m(L, color, 0.6, 0.1, 0.6)
    L.cube("ck1", 1, (-0.16 * s, 0, -0.10 * s), (0.30 * s, 0.12 * s, 0.11 * s), m, r, rot=(0, math.radians(45), 0), bevel=0.02)
    L.cube("ck2", 1, (0.12 * s, 0, 0.04 * s), (0.62 * s, 0.12 * s, 0.11 * s), m, r, rot=(0, math.radians(-50), 0), bevel=0.02)
    return r


def _cross(L, parent, loc, s=1.0, color="#f0443a"):
    r = L.empty("TPCross", loc, parent); m = _m(L, color, 0.3, 0.7, 0.5)
    for a in (45, -45):
        L.cube("cx", 1, (0, 0, 0), (0.78 * s, 0.12 * s, 0.13 * s), m, r, rot=(0, math.radians(a), 0), bevel=0.02)
    return r


def _bone(L, parent, loc, w, m):
    r = L.empty("TPBone", loc, parent)
    L.cylinder("shaft", 0.085, w, (0, 0, 0), m=m, parent=r, rot=(0, math.pi / 2, 0), verts=20)
    for sx in (-1, 1):
        for sz in (-0.07, 0.07):
            L.sphere("knob", 0.11, (sx * w / 2, 0, sz), m=m, parent=r, segs=16)
    return r


def _house(L, parent, loc, w, h, wall, roof):
    r = L.empty("TPHouse", loc, parent)
    L.cube("wall", 1, (0, 0, h / 2), (w, w * 0.8, h), _m(L, wall, 0.7, 0.1), r, bevel=0.04)
    L.cone("roof", w * 0.85, 0.0, w * 0.6, (0, 0, h + w * 0.3), m=_m(L, roof, 0.6, 0.2), parent=r, rot=(0, 0, math.pi / 4), verts=4)
    return r


def build(L, name, at, **o):
    root = L.empty("TP_" + name, tuple(at)); P = {}
    s = o.get("s", 1.0)

    if name == "sign":            # answer choice board: text, color; "win" marks it right
        text = o.get("text", "?"); ts = o.get("size", 0.5) * s
        if len(text) > 8: ts *= 8.0 / len(text)
        w = max(1.5, len(text) * ts * 0.66 + 0.6); h = max(0.95, ts * 1.9)
        L.cube("back", 1, (0, 0.05, 0), (w + 0.18, 0.12, h + 0.18), _m(L, "#ffffff", 0.8, 0.0), root, bevel=0.06)
        L.cube("board", 1, (0, 0, 0), (w, 0.14, h), _m(L, o.get("color", "#1479d6"), 0.85, 0.0, 0.35), root, bevel=0.06)
        _txt(L, text, ts, (0, -0.1, -ts * 0.04), o.get("tcolor", "#ffffff"), root, extrude=0.05, emit=1.1)
        P["wh"] = (w, h)
        P["check"] = L.empty("ckroot", (w / 2 - 0.12, -0.22, h / 2 - 0.12), root)
        L.cylinder("ckdisc", 0.36, 0.06, (0, 0.04, 0), m=_m(L, "#ffffff", 0.8, 0.0), parent=P["check"], rot=(math.pi / 2, 0, 0), verts=32)
        _check(L, P["check"], (0.02, -0.02, 0.02), 0.72, "#18a03a"); P["check"].scale = (0, 0, 0)
    elif name == "badge":         # round clue badge with a number or short word
        L.cylinder("disc", 0.42 * s, 0.12, (0, 0, 0), m=_m(L, o.get("color", "#ffb627"), 0.3, 0.7), parent=root, rot=(math.pi / 2, 0, 0))
        L.torus("rim", 0.42 * s, 0.045, (0, 0, 0), m=_m(L, "#ffffff", 0.3, 0.6), parent=root, rot=(math.pi / 2, 0, 0))
        _txt(L, str(o.get("text", "1")), 0.5 * s, (0, -0.09, -0.02), "#ffffff", root)
    elif name == "qbox":          # mystery box: who is hiding?
        L.cube("box", 1, (0, 0, 1.0), (1.9, 1.5, 2.0), _m(L, o.get("color", "#8e5bd8"), 0.4, 0.6), root, bevel=0.14)
        L.cube("lid", 1, (0, 0, 2.08), (2.06, 1.66, 0.22), _m(L, "#ffd23f", 0.35, 0.6), root, bevel=0.07)
        P["q"] = _txt(L, "?", 1.25, (0, -0.8, 1.0), "#ffffff", root, extrude=0.08)
    elif name == "dots":          # thinking timer: three dots fill in while the child thinks
        P["dots"] = [L.sphere("dot", 0.15 * s, ((k - 1) * 0.46 * s, 0, 0), m=_m(L, "#ffd23f", 0.3, 0.6, 0.8), parent=root, segs=20) for k in range(3)]
    elif name == "check":
        _check(L, root, (0, 0, 0), 1.5 * s)
    elif name == "cross":
        _cross(L, root, (0, 0, 0), 1.3 * s)
    elif name == "arrow":         # points down at something
        m = _m(L, o.get("color", "#ff6fb5"), 0.3, 0.6, 0.4)
        if o.get("up"):
            L.cylinder("stem", 0.1 * s, 0.6 * s, (0, 0, 0.3 * s), m=m, parent=root, verts=16)
            L.cone("head", 0.26 * s, 0, 0.4 * s, (0, 0, 0.8 * s), m=m, parent=root, verts=24)
        else:
            L.cylinder("stem", 0.1 * s, 0.6 * s, (0, 0, 0.5 * s), m=m, parent=root, verts=16)
            L.cone("head", 0.26 * s, 0, 0.4 * s, (0, 0, 0.05 * s), m=m, parent=root, rot=(math.pi, 0, 0), verts=24)
    elif name == "count":         # numbers that pop in one by one (opts: n, times, dx, dz, start)
        n = o.get("n", 3); P["items"] = []
        cols = ["#ff7a00", "#3db8ff", "#3cc45a", "#8e5bd8", "#ff6fb5", "#ffb627", "#f0443a"]
        for k in range(n):
            e = L.empty("num", (k * o.get("dx", 0.7), 0, k * o.get("dz", 0.0)), root)
            L.sphere("b", 0.3 * s, (0, 0.05, 0), (1, 0.4, 1), _m(L, cols[k % len(cols)], 0.3, 0.7), e, 24)
            _txt(L, str(o.get("start", 1) + k), 0.4 * s, (0, -0.1, -0.02), "#ffffff", e)
            P["items"].append(e)
    elif name == "flies":         # buzzing flies; "leave": seconds after which they fly away
        P["flies"] = []
        for k in range(o.get("n", 4)):
            f = L.empty("fly", (0, 0, 0), root)
            L.sphere("body", 0.15, (0, 0, 0), (1.3, 1, 1), _m(L, "#2b2b33", 0.3, 0.6), f, 14)
            for sx in (-1, 1):
                L.sphere("wing", 0.15, (0, sx * 0.12, 0.12), (1.2, 0.5, 0.12), _m(L, "#dff4ff", 0.2, 0.8, 0.5), f, 10)
            L.sphere("eye", 0.06, (0.15, -0.05, 0.03), m=_m(L, "#f0443a", 0.3, 0.6, 0.6), parent=f, segs=8)
            P["flies"].append(f)
    elif name == "mud":           # cool mud puddle
        m = _m(L, "#7a4a2a", 0.18, 0.9)
        L.sphere("pud", 1.0, (0, 0, 0.02), (1.35, 0.95, 0.07), m, root, 32)
        for dx, dy, r in ((-1.0, 0.5, 0.3), (1.1, -0.35, 0.36), (0.3, 0.75, 0.24)):
            L.sphere("blob", r, (dx, dy, 0.02), (1, 0.9, 0.12), m, root, 20)
        P["drops"] = [L.sphere("drop", 0.07, (dx, -0.2, 0.3), m=m, parent=root, segs=10) for dx in (-0.5, 0.1, 0.6)]
    elif name == "sun":
        m = _m(L, "#ffcf33", 0.3, 0.5, 1.6)
        L.sphere("core", 0.42 * s, (0, 0, 0), m=m, parent=root, segs=32)
        P["rays"] = L.empty("rays", (0, 0, 0), root)
        for k in range(10):
            a = k * math.tau / 10
            L.cone("ray", 0.085 * s, 0, 0.3 * s, (math.cos(a) * 0.66 * s, 0, math.sin(a) * 0.66 * s), m=m, parent=P["rays"], rot=(0, math.pi / 2 - a, 0), verts=12)
    elif name == "snowflake":
        m = _m(L, "#e9f6ff", 0.2, 0.8, 0.9)
        for k in range(3):
            L.cube("arm", 1, (0, 0, 0), (0.95 * s, 0.07, 0.085 * s), m, root, rot=(0, k * math.pi / 3, 0), bevel=0.02)
        for k in range(6):
            a = k * math.pi / 3
            L.sphere("tip", 0.075 * s, (math.cos(a) * 0.47 * s, 0, math.sin(a) * 0.47 * s), m=m, parent=root, segs=12)
    elif name == "leaves":        # leafy branch (koala food)
        L.cylinder("branch", 0.07, 2.0, (0, 0, 1.25), m=_m(L, "#8a5a36", 0.7, 0.1), parent=root, rot=(0, math.radians(18), 0), verts=14)
        g = _m(L, "#57b86a", 0.45, 0.4); g2 = _m(L, "#7fd08a", 0.45, 0.4)
        for k, (dx, dz) in enumerate(((-0.55, 0.7), (0.25, 0.95), (-0.25, 1.35), (0.55, 1.6), (0.05, 1.95), (0.75, 2.2), (0.35, 2.45))):
            L.sphere("leaf", 0.3, (dx, -0.05, dz), (1.25, 0.3, 0.55), g if k % 2 else g2, root, 16, rot=(0, math.radians(-35 + 70 * (k % 2)), 0))
    elif name == "plate":         # dinner plate, standing up so the camera sees it
        r = o.get("r", 0.62)
        L.cylinder("plate", r, 0.06, (0, 0, r + 0.1), m=_m(L, "#ffffff", 0.15, 0.9), parent=root, rot=(math.radians(78), 0, 0))
        L.torus("rim", r * 0.72, 0.03, (0, -0.04, r + 0.1), m=_m(L, "#8fd3ff", 0.2, 0.8), parent=root, rot=(math.radians(78), 0, 0))
    elif name == "pool":          # little pool of water
        L.cylinder("water", 1.25 * s, 0.06, (0, 0, 0.04), m=_m(L, "#39a7ee", 0.05, 1.0, 0.15), parent=root, verts=48)
        L.torus("edge", 1.25 * s, 0.1, (0, 0, 0.05), m=_m(L, "#f2e2b8", 0.6, 0.2), parent=root)
        P["rip"] = [L.torus("rip", 0.4, 0.025, (0, 0, 0.085), m=_m(L, "#c9ecff", 0.1, 0.8, 0.5), parent=root) for _ in range(2)]
    elif name == "house2":        # two-floor house with an upstairs window (giraffe peeks in)
        h = o.get("h", 3.3); w = 2.1
        _house(L, root, (0, 0, 0), w, h, o.get("wall", "#ffe2b8"), o.get("roof", "#e8554a"))
        L.cube("door", 1, (-0.45, -w * 0.4 - 0.02, 0.6), (0.56, 0.06, 1.2), _m(L, "#8a5a36", 0.5, 0.3), root, bevel=0.03)
        for (dx, dz) in ((0.45, 0.85), (-0.45, h - 0.75), (0.45, h - 0.75)):
            L.cube("frame", 1, (dx, -w * 0.4 - 0.02, dz), (0.62, 0.06, 0.62), _m(L, "#ffffff", 0.4, 0.4), root, bevel=0.03)
            L.cube("glass", 1, (dx, -w * 0.4 - 0.05, dz), (0.48, 0.04, 0.48), _m(L, "#7fd3ff", 0.05, 1.0, 0.25), root)
    elif name == "ruler":         # height chart
        h = o.get("h", 4.2)
        L.cube("stick", 1, (0, 0, h / 2), (0.5, 0.1, h), _m(L, "#ffd23f", 0.4, 0.5), root, bevel=0.04)
        for k in range(1, int(h * 2)):
            L.cube("tick", 1, (0.09 if k % 2 else 0, -0.06, k * 0.5), (0.3 if k % 2 else 0.46, 0.04, 0.045), _m(L, "#402010", 0.5, 0.2), root)
        P["top"] = L.empty("top", (0, 0, o.get("mark", 3.8)), root)
        L.cone("ptr", 0.22, 0, 0.42, (-0.52, 0, 0), m=_m(L, "#f0443a", 0.3, 0.6, 0.5), parent=P["top"], rot=(0, math.pi / 2, 0), verts=20)
    elif name == "cars":          # n cars that appear one by one (count along)
        n = o.get("n", 4); P["items"] = []
        cols = ["#f0443a", "#3db8ff", "#3cc45a", "#ffb627", "#8e5bd8"]
        for k in range(n):
            c = L.empty("car", ((k % 2) * 1.45 - 0.72, 0, (k // 2) * 1.0), root)
            L.cube("body", 1, (0, 0, 0.36), (1.25, 0.62, 0.38), _m(L, cols[k % 5], 0.3, 0.8), c, bevel=0.1)
            L.cube("cab", 1, (-0.05, 0, 0.68), (0.7, 0.56, 0.32), _m(L, "#bfe8ff", 0.1, 0.9), c, bevel=0.1)
            for wx in (-0.38, 0.38):
                L.cylinder("wheel", 0.17, 0.66, (wx, 0, 0.17), m=_m(L, "#2b2b33", 0.6, 0.2), parent=c, rot=(math.pi / 2, 0, 0), verts=20)
            _txt(L, str(k + 1), 0.3, (0, -0.34, 0.37), "#ffffff", c)
            P["items"].append(c)
    elif name == "rings":         # sound waves leaving the lion's mouth
        P["rings"] = [L.torus("ring", 0.5, 0.045, (0, 0, 0), m=_m(L, "#ffd23f", 0.3, 0.5, 1.2), parent=root, rot=(0, math.pi / 2, 0)) for _ in range(4)]
    elif name == "town":          # tiny far-away town (the roar reaches it)
        for k, (dx, hh, col) in enumerate(((-0.8, 0.8, "#ffe2b8"), (0.0, 1.1, "#cfe8ff"), (0.8, 0.7, "#ffd1e0"))):
            _house(L, root, (dx, 0, 0), 0.62, hh, col, ("#e8554a", "#4a8fe8", "#8e5bd8")[k])
        _txt(L, o.get("text", "5 MILES"), 0.34, (0, -0.4, 1.75), "#ffffff", root)
    elif name == "swatch":        # a board showing a pattern: kind = stripes | spots
        w, h = 1.5 * s, 1.5 * s
        L.cube("frame", 1, (0, 0.04, 0), (w + 0.18, 0.12, h + 0.18), _m(L, "#ffffff", 0.4, 0.4), root, bevel=0.06)
        L.cube("bg", 1, (0, 0, 0), (w, 0.14, h), _m(L, o.get("base", "#f7f4ee"), 0.6, 0.2), root, bevel=0.03)
        dm = _m(L, o.get("mark", "#25232b"), 0.6, 0.2)
        if o.get("kind", "stripes") == "stripes":
            for k in range(4):
                L.cube("bar", 1, ((-0.375 + k * 0.25) * w + 0.0, -0.075, 0), (0.115 * w, 0.03, h * 0.96), dm, root)
        else:
            for dx, dz, r in ((-0.28, 0.26, 0.17), (0.22, 0.3, 0.13), (0.3, -0.12, 0.18), (-0.1, -0.05, 0.12), (-0.3, -0.3, 0.14), (0.05, -0.34, 0.1)):
                L.cylinder("dot", r * w, 0.03, (dx * w, -0.075, dz * h), m=dm, parent=root, rot=(math.pi / 2, 0, 0), verts=24)
        if o.get("label"): _txt(L, o["label"], 0.3 * s, (0, -0.05, -h / 2 - 0.3 * s), "#ffffff", root)
    elif name == "fingerprint":   # "like your fingerprint"
        L.cube("card", 1, (0, 0, 0), (1.2 * s, 0.1, 1.5 * s), _m(L, "#fff3d6", 0.5, 0.3), root, bevel=0.06)
        for k in range(4):
            L.torus("loop", (0.12 + k * 0.1) * s, 0.022, (0, -0.07, 0.05 * s), (1, 1, 1.25), _m(L, "#ff7a00", 0.4, 0.4), root, rot=(math.pi / 2, 0, 0))
    elif name == "magnifier":     # look closer: shows what is under the fur (opts fill, hairs, label)
        L.torus("ring", 0.72 * s, 0.085, (0, 0, 0), m=_m(L, "#ffb627", 0.3, 0.7), parent=root, rot=(math.pi / 2, 0, 0))
        L.cylinder("lens", 0.7 * s, 0.05, (0, 0.03, 0), m=_m(L, o.get("fill", "#1c1c22"), 0.55, 0.3), parent=root, rot=(math.pi / 2, 0, 0), verts=40)
        L.cylinder("handle", 0.085, 0.85 * s, (0.72 * s, 0, -0.78 * s), m=_m(L, "#8a5a36", 0.5, 0.4), parent=root, rot=(0, math.radians(-42), 0), verts=16)
        if o.get("hairs", 0):
            hm = _m(L, o.get("hair", "#eef6ff"), 0.15, 0.9, 0.25, o.get("hair_alpha", 1.0))
            for k in range(o["hairs"]):
                x = (-0.42 + 0.84 * k / max(1, o["hairs"] - 1)) * s
                L.cylinder("hair", 0.03, 0.62 * s, (x, -0.06, 0.12 * s), m=hm, parent=root, rot=(0, math.radians(-12 + 6 * (k % 3)), 0), verts=10)
        if o.get("stripes"):
            sm = _m(L, o.get("stripe", "#f28a2e"), 0.55, 0.3)
            for k in range(3):
                L.cube("st", 1, ((-0.36 + k * 0.36) * s, -0.04, 0), (0.17 * s, 0.03, 1.1 * s), sm, root)
        if o.get("label"):
            lw = len(o["label"]) * 0.2 * s + 0.35
            L.cube("plate", 1, (0, 0.0, -0.72 * s - 0.36 * s), (lw, 0.1, 0.46 * s), _m(L, "#2459b8", 0.85, 0.0, 0.2), root, bevel=0.05)
            _txt(L, o["label"], 0.3 * s, (0, -0.09, -0.72 * s - 0.37 * s), "#ffffff", root, emit=0.9)
    elif name == "table":         # little display table, so small examples are easy to see
        w = o.get("w", 2.4); h = o.get("h", 0.9)
        L.cylinder("leg", 0.16, h, (0, 0, h / 2), m=_m(L, "#8a5a36", 0.7, 0.1), parent=root, verts=16)
        L.cube("top", 1, (0, 0, h), (w, 1.0, 0.12), _m(L, o.get("color", "#ffd98a"), 0.6, 0.2), root, bevel=0.05)
        L.cylinder("foot", 0.5, 0.08, (0, 0, 0.04), m=_m(L, "#8a5a36", 0.7, 0.1), parent=root, verts=24)
    elif name == "butter":        # a stick of butter on a little dish (how small a newborn panda is)
        L.cylinder("dish", 0.55, 0.05, (0, 0, 0.03), m=_m(L, "#ffffff", 0.15, 0.9), parent=root, verts=32)
        L.cube("butter", 1, (0, 0, 0.19), (0.72, 0.3, 0.26), _m(L, "#ffe066", 0.35, 0.6), root, bevel=0.03)
    elif name == "sock":          # stripy sock (stripes at home)
        m = _m(L, "#ffffff", 0.7, 0.1); sm = _m(L, o.get("color", "#f0443a"), 0.7, 0.1)
        L.cube("leg", 1, (0, 0, 0.42), (0.5, 0.3, 0.9), m, root, bevel=0.12)
        L.cube("foot", 1, (-0.28, 0, 0.02), (1.0, 0.3, 0.46), m, root, bevel=0.14)
        for z in (0.3, 0.55, 0.8):
            L.cube("stripe", 1, (0, 0, z), (0.52, 0.32, 0.09), sm, root)
    elif name == "ball":          # spotty ball (spots at home)
        L.sphere("ball", 0.5 * s, (0, 0, 0.5 * s), m=_m(L, o.get("color", "#ffd23f"), 0.3, 0.7), parent=root, segs=32)
        dm = _m(L, o.get("mark", "#f0443a"), 0.3, 0.7)
        for a, b in ((0.2, 0.5), (1.3, 0.1), (2.4, 0.6), (3.5, -0.2), (4.6, 0.4), (5.6, -0.3), (0.9, -0.5), (3.0, 1.0)):
            x, y, z = math.cos(a) * math.cos(b), math.sin(a) * math.cos(b), math.sin(b)
            L.sphere("spot", 0.13 * s, (x * 0.46 * s, y * 0.46 * s, (0.5 + z * 0.46) * s), m=dm, parent=root, segs=12)
    elif name == "zzz":           # sleeping
        P["z"] = [_txt(L, "Z", (0.34 + 0.12 * k) * s, (k * 0.3 * s, 0, k * 0.42 * s), o.get("color", "#8fd3ff"), root) for k in range(3)]
    elif name == "bones":         # n neck bones stacked up, counted one by one
        n = o.get("n", 7); P["items"] = []; P["bones"] = []; bm = _m(L, "#fff8e8", 0.6, 0.2)
        L.cube("frame", 1, (0, 0.16, n * 0.21 + 0.1), (2.08, 0.1, n * 0.42 + 0.63), _m(L, "#ffffff", 0.8, 0.0), root, bevel=0.07)
        L.cube("board", 1, (0, 0.12, n * 0.21 + 0.1), (1.9, 0.1, n * 0.42 + 0.45), _m(L, "#2459b8", 0.85, 0.0, 0.2), root, bevel=0.07)
        for k in range(n):
            b = L.empty("bone", (0.24, 0, 0.3 + k * 0.42), root); _bone(L, b, (0, 0, 0), 0.72, bm); P["bones"].append(b)
            e = L.empty("num", (-0.6, -0.02, 0.28 + k * 0.42), root)
            _txt(L, str(k + 1), 0.32, (0, 0, 0), "#ffd23f", e, emit=0.9)
            P["items"].append(e)
    elif name == "thermo":        # thermometer: level 0..1, hot (red) or cold (blue)
        hot = o.get("hot", True); lv = o.get("level", 0.9 if hot else 0.2); h = 2.0
        col = "#f0443a" if hot else "#3db8ff"
        L.cylinder("tube", 0.16, h, (0, 0, 0.5 + h / 2), m=_m(L, "#ffffff", 0.15, 0.9), parent=root, verts=24)
        L.sphere("bulb", 0.3, (0, 0, 0.42), m=_m(L, col, 0.2, 0.8, 0.5), parent=root, segs=24)
        L.cylinder("fill", 0.1, h * lv, (0, -0.09, 0.5 + h * lv / 2), m=_m(L, col, 0.2, 0.8, 0.5), parent=root, verts=16)
        L.cube("tag", 1, (0, 0.0, h + 0.95), (1.5 if hot else 1.8, 0.1, 0.62), _m(L, "#ffffff", 0.8, 0.0), root, bevel=0.06)
        _txt(L, "HOT" if hot else "COLD", 0.44, (0, -0.08, h + 0.93), "#d42a20" if hot else "#1479d6", root, emit=0.5)
    elif name == "bamboo":
        g = _m(L, "#6cc04a", 0.4, 0.5); g2 = _m(L, "#3f9a3a", 0.5, 0.3)
        for k, (dx, hh) in enumerate(((-0.7, 3.0), (-0.25, 3.6), (0.25, 2.7), (0.7, 3.3))):
            for j in range(int(hh / 0.6)):
                L.cylinder("seg", 0.11, 0.56, (dx, 0.1 * (k % 2), 0.3 + j * 0.6), m=g, parent=root, verts=14)
                L.torus("joint", 0.115, 0.025, (dx, 0.1 * (k % 2), 0.6 + j * 0.6), m=g2, parent=root)
            L.sphere("leaf", 0.32, (dx + 0.3, 0, hh - 0.2), (1.2, 0.25, 0.4), g2, root, 12, rot=(0, math.radians(-30), 0))
            L.sphere("leaf", 0.3, (dx - 0.28, 0, hh - 0.6), (1.2, 0.25, 0.4), g, root, 12, rot=(0, math.radians(30), 0))
    elif name == "den":           # cozy bear den
        L.sphere("hill", 1.5, (0, 0.4, 0), (1.15, 0.9, 0.95), _m(L, "#8d7a66", 0.85, 0.05), root, 32)
        L.sphere("hole", 0.85, (0, -0.55, 0.0), (0.95, 0.5, 1.0), _m(L, "#2a211c", 0.9, 0.0), root, 28)
        for dx in (-1.1, 1.15):
            L.sphere("bush", 0.42, (dx, -0.5, 0.25), (1, 0.8, 0.8), _m(L, "#57b86a", 0.6, 0.2), root, 16)
        L.sphere("snowcap", 1.2, (0, 0.4, 0.75), (1.0, 0.8, 0.5), _m(L, "#ffffff", 0.5, 0.3), root, 28)
    elif name == "notree":        # jungle tree with a "not here" cross
        L.cylinder("trunk", 0.2, 2.0, (0, 0, 1.0), m=_m(L, "#8a5a36", 0.7, 0.1), parent=root, verts=14)
        for k in range(6):
            a = k * math.tau / 6
            L.sphere("frond", 0.6, (math.cos(a) * 0.55, math.sin(a) * 0.3, 2.1), (1.3, 0.4, 0.3), _m(L, "#2f9e55", 0.5, 0.3), root, 14, rot=(0, math.radians(20) * math.cos(a), a))
        if not o.get("nocross"): P["cross"] = _cross(L, root, (0, -0.6, 1.5), 1.6)
    elif name == "heart":
        m = _m(L, "#ff4f7a", 0.25, 0.8, 0.5)
        for sx in (-1, 1):
            L.sphere("lobe", 0.3 * s, (sx * 0.22 * s, 0, 0.14 * s), m=m, parent=root, segs=24)
        L.cone("tip", 0.44 * s, 0, 0.62 * s, (0, 0, -0.22 * s), (1, 0.62, 1), m, root, rot=(math.pi, 0, 0), verts=32)
    else:
        L.sphere("unknown", 0.4, (0, 0, 0.4), m=_m(L, "#ff00ff"), parent=root)
    try: _detail(L, name, root, P, o)      # second pass: the small things that make a prop read as a real object
    except Exception as e: print("teachprops detail skipped for", name, e)
    ANIM[root.name] = (name, dict(o), P)
    return root


def _sparkle(L, parent, loc, r=0.1, color="#fff3a0"):
    e = L.empty("spark", loc, parent); m = _m(L, color, 0.3, 0.5, 1.4)
    L.cone("s1", r * 0.45, 0, r * 2.2, (0, 0, r * 1.1), m=m, parent=e, verts=4)
    L.cone("s2", r * 0.45, 0, r * 2.2, (0, 0, -r * 1.1), m=m, parent=e, rot=(math.pi, 0, 0), verts=4)
    L.cone("s3", r * 0.45, 0, r * 1.6, (r * 0.8, 0, 0), m=m, parent=e, rot=(0, math.pi / 2, 0), verts=4)
    L.cone("s4", r * 0.45, 0, r * 1.6, (-r * 0.8, 0, 0), m=m, parent=e, rot=(0, -math.pi / 2, 0), verts=4)
    return e


def _tuft(L, parent, loc, s=1.0, color="#4fb35a"):
    for k, (dx, a) in enumerate(((-0.1, -0.35), (0, 0.0), (0.1, 0.35))):
        L.cone("blade", 0.05 * s, 0, 0.42 * s, (loc[0] + dx * s, loc[1], loc[2] + 0.2 * s), m=_m(L, color, 0.6, 0.2), parent=parent, rot=(0, a, 0), verts=6)


def _window(L, parent, x, y, z, w=0.62, shutter="#3d8fd9"):
    L.cube("frame", 1, (x, y, z), (w, 0.06, w), _m(L, "#ffffff", 0.5, 0.2), parent, bevel=0.03)
    L.cube("glass", 1, (x, y - 0.03, z), (w * 0.78, 0.04, w * 0.78), _m(L, "#7fd3ff", 0.05, 1.0, 0.3), parent)
    L.cube("barv", 1, (x, y - 0.05, z), (0.045, 0.03, w * 0.78), _m(L, "#ffffff", 0.5, 0.2), parent)
    L.cube("barh", 1, (x, y - 0.05, z), (w * 0.78, 0.03, 0.045), _m(L, "#ffffff", 0.5, 0.2), parent)
    for sx in (-1, 1):
        L.cube("shutter", 1, (x + sx * (w * 0.5 + 0.11), y, z), (0.18, 0.05, w), _m(L, shutter, 0.6, 0.2), parent, bevel=0.02)
    L.cube("sill", 1, (x, y - 0.06, z - w * 0.5 - 0.04), (w + 0.2, 0.14, 0.07), _m(L, "#ffffff", 0.5, 0.2), parent, bevel=0.02)


def _detail(L, name, root, P, o):
    s = o.get("s", 1.0); cols = ["#f0443a", "#ffb627", "#3cc45a", "#3db8ff", "#8e5bd8", "#ff6fb5"]
    if name == "sign":
        w, h = P["wh"][0] + 0.18, P["wh"][1] + 0.18
        for sx in (-1, 1):
            for sz in (-1, 1):
                L.sphere("stud", 0.055, (sx * (w / 2 - 0.1), -0.09, sz * (h / 2 - 0.1)), m=_m(L, "#ffd23f", 0.3, 0.6, 0.6), parent=root, segs=12)
        L.cube("shine", 1, (0, -0.075, h * 0.3), (w * 0.8, 0.01, 0.045), _m(L, "#ffffff", 0.2, 0.6, 0.5, 0.55), root)
        P["confetti"] = []
        for k in range(20):                      # bursts when this answer is marked right
            c = L.cube("conf", 1, (0, -0.25, 0), (0.1, 0.02, 0.07), _m(L, cols[k % 6], 0.4, 0.4, 0.7), root, rot=(0.4 * k, 0.9 * k, 0.3 * k))
            c.scale = (0, 0, 0); P["confetti"].append(c)
    elif name == "badge":
        for k in range(12):
            a = k * math.tau / 12
            L.cone("ray", 0.09 * s, 0, 0.2 * s, (math.cos(a) * 0.5 * s, 0.04, math.sin(a) * 0.5 * s), m=_m(L, "#ffffff", 0.4, 0.4), parent=root, rot=(0, math.pi / 2 - a, 0), verts=4)
    elif name == "qbox":
        rb = _m(L, "#ff5fa2", 0.35, 0.6)
        L.cube("ribv", 1, (0, 0, 1.0), (0.3, 1.54, 2.04), rb, root, bevel=0.03)
        L.cube("ribh", 1, (0, 0, 2.08), (2.1, 0.3, 0.26), rb, root, bevel=0.03)
        for sx in (-1, 1):
            L.sphere("bow", 0.3, (sx * 0.3, 0, 2.42), (1.2, 0.55, 0.75), rb, root, 18, rot=(0, sx * 0.5, 0))
        L.sphere("knot", 0.14, (0, 0, 2.34), m=rb, parent=root, segs=14)
        for sx in (-0.62, 0.62):
            _txt(L, "?", 0.42, (sx, -0.79, 1.55 if sx < 0 else 0.5), "#ffd23f", root, extrude=0.04)
        P["sparks"] = [_sparkle(L, root, (0, 0, 0), 0.11, ("#fff3a0", "#ffd0e6", "#c9ecff")[k % 3]) for k in range(6)]
    elif name == "dots":
        L.cube("pill", 1, (0, 0.08, 0), (1.5 * s, 0.08, 0.5 * s), _m(L, "#ffffff", 0.8, 0.0, 0.0, 0.9), root, bevel=0.2 * s)
    elif name == "check":
        sc = 1.5 * s
        L.cylinder("disc", 0.52 * sc, 0.06, (0.0, 0.08, 0.0), m=_m(L, "#ffffff", 0.8, 0.0), parent=root, rot=(math.pi / 2, 0, 0), verts=40)
        L.torus("ring", 0.52 * sc, 0.05 * sc, (0, 0.06, 0), m=_m(L, "#18a03a", 0.5, 0.2, 0.5), parent=root, rot=(math.pi / 2, 0, 0))
        P["sparks"] = [_sparkle(L, root, (0, 0, 0), 0.09 * sc) for _ in range(5)]
    elif name == "cross":
        sc = 1.3 * s
        L.cylinder("disc", 0.56 * sc, 0.06, (0.0, 0.08, 0.0), m=_m(L, "#ffffff", 0.8, 0.0), parent=root, rot=(math.pi / 2, 0, 0), verts=40)
        L.torus("ring", 0.56 * sc, 0.05 * sc, (0, 0.06, 0), m=_m(L, "#f0443a", 0.5, 0.2, 0.5), parent=root, rot=(math.pi / 2, 0, 0))
    elif name == "count":
        for e in P["items"]:
            L.torus("ring", 0.3 * s, 0.035 * s, (0, 0.0, 0), m=_m(L, "#ffffff", 0.4, 0.4), parent=e, rot=(math.pi / 2, 0, 0))
            L.sphere("hl", 0.06 * s, (-0.12 * s, -0.11, 0.14 * s), m=_m(L, "#ffffff", 0.2, 0.6, 0.8), parent=e, segs=10)
    elif name == "mud":
        L.torus("rim", 1.05, 0.12, (0, 0, 0.02), (1.32, 0.93, 0.5), _m(L, "#5c3620", 0.5, 0.3), root)
        P["bubbles"] = [L.sphere("bub", 0.09, (dx, dy, 0.1), m=_m(L, "#9a6a45", 0.15, 0.9), parent=root, segs=12) for dx, dy in ((-0.45, 0.1), (0.3, -0.25), (0.6, 0.3), (-0.1, -0.4))]
        for dx, dy in ((-1.45, -0.3), (1.5, 0.35), (-0.9, 0.85), (1.0, -0.8)): _tuft(L, root, (dx, dy, 0), 1.0)
    elif name == "sun":
        fm = _m(L, "#7a4a1e", 0.5, 0.2)
        for sx in (-1, 1):
            L.sphere("eye", 0.055 * s, (sx * 0.15 * s, -0.39 * s, 0.08 * s), m=fm, parent=root, segs=12)
            L.sphere("cheek", 0.07 * s, (sx * 0.25 * s, -0.36 * s, -0.06 * s), (1, 0.4, 0.7), _m(L, "#ff9d6b", 0.5, 0.2), root, 12)
        L.torus("smile", 0.13 * s, 0.022 * s, (0, -0.4 * s, -0.04 * s), (1, 1, 0.55), fm, root, rot=(math.pi / 2, 0, 0))
        L.sphere("smilecover", 0.16 * s, (0, -0.37 * s, 0.045 * s), (1.1, 0.5, 0.6), _m(L, "#ffcf33", 0.3, 0.5, 1.6), root, 16)
    elif name == "snowflake":
        m = _m(L, "#e9f6ff", 0.2, 0.8, 0.9)
        for k in range(6):
            a = k * math.pi / 3; cx, cz = math.cos(a) * 0.3 * s, math.sin(a) * 0.3 * s
            for da in (0.9, -0.9):
                L.cube("twig", 1, (cx + math.cos(a + da) * 0.08 * s, 0, cz + math.sin(a + da) * 0.08 * s), (0.2 * s, 0.06, 0.05 * s), m, root, rot=(0, -(a + da), 0))
        L.sphere("gem", 0.1 * s, (0, -0.02, 0), m=_m(L, "#bfe8ff", 0.1, 0.9, 1.0), parent=root, segs=12)
    elif name == "leaves":
        for dx, dz in ((-0.2, 0.55), (0.45, 1.25), (0.2, 2.2)):
            L.sphere("nut", 0.09, (dx, -0.12, dz), m=_m(L, "#b98a5a", 0.6, 0.2), parent=root, segs=10)
        L.sphere("mound", 0.5, (0.1, 0, 0), (1.3, 1, 0.3), _m(L, "#6a4a2e", 0.9, 0.0), root, 16)
    elif name == "plate":
        r = o.get("r", 0.62); mm = _m(L, "#d9dde3", 0.2, 0.8)
        L.cube("forkh", 1, (-r - 0.3, 0, r * 0.75), (0.07, 0.04, r * 1.2), mm, root, bevel=0.02)
        for k in (-1, 0, 1):
            L.cube("tine", 1, (-r - 0.3 + k * 0.07, 0, r * 1.5), (0.035, 0.04, 0.3), mm, root, bevel=0.01)
        L.cube("spoonh", 1, (r + 0.3, 0, r * 0.75), (0.07, 0.04, r * 1.2), mm, root, bevel=0.02)
        L.sphere("spoon", 0.15, (r + 0.3, 0, r * 1.5), (0.85, 0.3, 1.25), mm, root, 14)
        L.sphere("stand", 0.3, (0, 0.1, 0.02), (1.6, 0.8, 0.2), _m(L, "#f2e2b8", 0.7, 0.1), root, 14)
    elif name == "pool":
        st = _m(L, "#b9b3a6", 0.8, 0.1)
        for k in range(9):
            a = k * math.tau / 9 + 0.3
            L.sphere("stone", 0.2 * s, (math.cos(a) * 1.32 * s, math.sin(a) * 1.32 * s, 0.06), (1.2, 1, 0.6), st, root, 12, rot=(0, 0, a))
        for dx, dy in ((-0.45, 0.4), (0.5, 0.1)):
            L.cylinder("pad", 0.2 * s, 0.03, (dx * s, dy * s, 0.09), m=_m(L, "#4fb35a", 0.5, 0.3), parent=root, verts=16)
        L.sphere("lily", 0.08 * s, (-0.45 * s, 0.4 * s, 0.15), m=_m(L, "#ffb3d1", 0.4, 0.4, 0.4), parent=root, segs=10)
        for dx in (-1.1, -0.95):
            L.cylinder("reed", 0.025, 0.9, (dx * s, 0.85 * s, 0.45), m=_m(L, "#3f9a3a", 0.6, 0.2), parent=root, verts=8)
            L.sphere("cattail", 0.06, (dx * s, 0.85 * s, 0.85), (1, 1, 2.2), _m(L, "#7a4a2a", 0.7, 0.1), root, 10)
    elif name == "house2":
        h = o.get("h", 3.3); w = 2.1; fy = -w * 0.4 - 0.02
        for c in [c for c in root.children if c.name.startswith(("frame", "glass"))]: c.scale = (0, 0, 0)   # plain windows -> detailed ones
        _window(L, root, 0.47, fy, 0.95, 0.56); _window(L, root, -0.47, fy, h - 0.8, 0.56); _window(L, root, 0.47, fy, h - 0.8, 0.56)
        L.cube("doorframe", 1, (-0.45, fy + 0.01, 0.63), (0.7, 0.05, 1.32), _m(L, "#ffffff", 0.5, 0.2), root, bevel=0.03)
        L.sphere("knob", 0.05, (-0.27, fy - 0.07, 0.6), m=_m(L, "#ffd23f", 0.2, 0.8, 0.4), parent=root, segs=10)
        L.cube("step", 1, (-0.45, fy - 0.2, 0.05), (0.9, 0.4, 0.1), _m(L, "#c9c2b4", 0.8, 0.1), root, bevel=0.03)
        L.cube("chimney", 1, (0.62, 0.2, h + 0.75), (0.36, 0.36, 0.9), _m(L, "#b5533c", 0.8, 0.1), root, bevel=0.03)
        P["smoke"] = [L.sphere("puff", 0.2, (0.62, 0.2, h + 1.3), m=_m(L, "#ffffff", 0.9, 0.0, 0.0, 0.85), parent=root, segs=12) for _ in range(3)]
        L.cube("box", 1, (0.47, fy - 0.12, 0.6), (0.7, 0.2, 0.14), _m(L, "#8a5a36", 0.7, 0.1), root, bevel=0.03)
        for k in range(4):
            L.sphere("flower", 0.08, (0.22 + k * 0.17, fy - 0.14, 0.73), m=_m(L, cols[(k * 2) % 6], 0.4, 0.4, 0.4), parent=root, segs=10)
        for dx in (-1.25, 1.3):
            L.sphere("bush", 0.36, (dx, fy + 0.1, 0.26), (1, 0.8, 0.85), _m(L, "#57b86a", 0.7, 0.1), root, 14)
        for k in range(3):
            L.cylinder("path", 0.2, 0.04, (-0.45 + 0.05 * k, fy - 0.75 - k * 0.45, 0.02), (1.2, 0.8, 1), _m(L, "#d9d2c4", 0.8, 0.1), root, verts=12)
    elif name == "ruler":
        h = o.get("h", 4.2)
        for k in range(1, int(h) + 1):
            _txt(L, str(k), 0.2, (-0.12, -0.07, k * 1.0 - 0.33), "#402010", root, extrude=0.02, emit=0.0)
        L.cube("foot", 1, (0, 0, 0.06), (0.9, 0.5, 0.12), _m(L, "#e0a81e", 0.5, 0.4), root, bevel=0.04)
    elif name == "cars":
        for c in P["items"]:
            for sy in (-1, 1):
                L.sphere("lamp", 0.07, (0.62, sy * 0.2, 0.4), m=_m(L, "#fff3a0", 0.2, 0.6, 1.2), parent=c, segs=10)
            L.cube("bumper", 1, (0.63, 0, 0.24), (0.06, 0.6, 0.09), _m(L, "#d9dde3", 0.2, 0.8), c, bevel=0.02)
            L.cube("pillar", 1, (-0.05, -0.29, 0.68), (0.06, 0.03, 0.3), _m(L, "#ffffff", 0.4, 0.4), c)
            for wx in (-0.38, 0.38):
                L.cylinder("hub", 0.08, 0.68, (wx, 0, 0.17), m=_m(L, "#d9dde3", 0.3, 0.7), parent=c, rot=(math.pi / 2, 0, 0), verts=12)
    elif name == "town":
        for dx, hh in ((-0.8, 0.8), (0.0, 1.1), (0.8, 0.7)):
            L.cube("door", 1, (dx, -0.26, 0.17), (0.16, 0.03, 0.34), _m(L, "#8a5a36", 0.6, 0.2), root)
            L.cube("win", 1, (dx, -0.26, hh * 0.68), (0.2, 0.03, 0.2), _m(L, "#7fd3ff", 0.1, 0.9, 0.5), root)
        for dx in (-1.35, 1.35, 0.42):
            L.cylinder("trunk", 0.04, 0.3, (dx, 0.1, 0.15), m=_m(L, "#8a5a36", 0.7, 0.1), parent=root, verts=8)
            L.sphere("crown", 0.2, (dx, 0.1, 0.45), m=_m(L, "#57b86a", 0.7, 0.1), parent=root, segs=12)
        L.cube("road", 1, (0, -0.55, 0.012), (3.1, 0.36, 0.02), _m(L, "#8d8f96", 0.9, 0.0), root)
        for k in range(5):
            L.cube("dash", 1, (-1.2 + k * 0.6, -0.55, 0.026), (0.26, 0.04, 0.01), _m(L, "#ffffff", 0.6, 0.1), root)
        L.cube("plate", 1, (0, 0.02, 1.75), (1.75, 0.06, 0.52), _m(L, "#2459b8", 0.85, 0.0, 0.2), root, bevel=0.05)
        L.cylinder("post", 0.035, 0.5, (0, 0.03, 1.3), m=_m(L, "#8a5a36", 0.7, 0.1), parent=root, verts=8)
    elif name == "swatch":
        for sx in (-1, 1):
            L.cylinder("leg", 0.045, 1.3 * s, (sx * 0.45 * s, 0.12, -1.1 * s), m=_m(L, "#8a5a36", 0.7, 0.1), parent=root, rot=(0, sx * 0.14, 0), verts=10)
    elif name == "fingerprint":
        L.cube("title", 1, (0, -0.01, 0.6 * s), (1.2 * s, 0.11, 0.26 * s), _m(L, "#ff7a00", 0.6, 0.2), root, bevel=0.04)
        L.sphere("thumb", 0.34 * s, (0, -0.03, 0.02 * s), (1, 0.12, 1.3), _m(L, "#ffd9b8", 0.6, 0.2), root, 20)
    elif name == "magnifier":
        L.torus("shine", 0.5 * s, 0.03, (-0.08 * s, -0.045, 0.08 * s), (0.7, 1, 0.7), _m(L, "#ffffff", 0.1, 0.9, 0.9, 0.7), root, rot=(math.pi / 2, 0, 0.6))
        for k in range(3):
            L.torus("grip", 0.092, 0.018, ((0.92 + k * 0.1) * s, 0, (-1.0 - k * 0.11) * s), m=_m(L, "#5e3a20", 0.6, 0.2), parent=root, rot=(0, math.radians(48), 0))
    elif name == "table":
        w = o.get("w", 2.4); h = o.get("h", 0.9)
        L.cube("cloth", 1, (0, 0, h + 0.05), (w * 0.62, 1.04, 0.04), _m(L, "#ffffff", 0.9, 0.0), root, bevel=0.02)
        for k in range(int(w * 0.62 / 0.24)):
            L.sphere("scallop", 0.12, (-w * 0.31 + 0.12 + k * 0.24, -0.52, h + 0.0), (1, 0.25, 1), _m(L, cols[k % 6], 0.7, 0.1), root, 12)
    elif name == "butter":
        L.cube("wrap", 1, (-0.2, 0, 0.2), (0.36, 0.34, 0.3), _m(L, "#f5f1e6", 0.8, 0.0), root, bevel=0.02)
        L.cube("stripe", 1, (-0.2, -0.171, 0.2), (0.3, 0.01, 0.08), _m(L, "#3d8fd9", 0.7, 0.1), root)
    elif name == "ball":
        L.sphere("hl", 0.09 * s, (-0.17 * s, -0.4 * s, 0.72 * s), m=_m(L, "#ffffff", 0.1, 0.8, 0.9), parent=root, segs=10)
    elif name == "sock":
        L.cube("cuff", 1, (0, 0, 0.92), (0.56, 0.36, 0.14), _m(L, o.get("color", "#f0443a"), 0.8, 0.0), root, bevel=0.05)
        L.sphere("heel", 0.2, (0.2, 0, 0.1), (1, 0.8, 1), _m(L, o.get("color", "#f0443a"), 0.8, 0.0), root, 12)
        L.sphere("toe", 0.22, (-0.72, 0, 0.03), (1, 0.72, 1), _m(L, o.get("color", "#f0443a"), 0.8, 0.0), root, 12)
    elif name == "bones":
        n = o.get("n", 7)
        L.cube("title", 1, (0, 0.1, n * 0.42 + 0.62), (1.9, 0.12, 0.42), _m(L, "#ffd23f", 0.7, 0.1), root, bevel=0.06)
        _txt(L, o.get("title", "NECK BONES"), 0.2, (0, 0.03, n * 0.42 + 0.6), "#402010", root, extrude=0.02, emit=0.0)
        for sx in (-1, 1):
            L.cylinder("leg", 0.05, 0.3, (sx * 0.7, 0.14, 0.0), m=_m(L, "#8a5a36", 0.7, 0.1), parent=root, verts=10)
    elif name == "thermo":
        for k in range(1, 8):
            L.cube("tick", 1, (0.2, -0.02, 0.5 + k * 0.25), (0.12 if k % 2 else 0.2, 0.03, 0.03), _m(L, "#402010", 0.6, 0.1), root)
        L.sphere("hl", 0.07, (-0.1, -0.24, 0.52), m=_m(L, "#ffffff", 0.1, 0.8, 0.9), parent=root, segs=10)
        L.cylinder("base", 0.42, 0.06, (0, 0, 0.03), m=_m(L, "#d9d2c4", 0.8, 0.1), parent=root, verts=20)
    elif name == "bamboo":
        L.sphere("mound", 1.0, (0, 0.05, 0), (1.2, 0.6, 0.16), _m(L, "#5a8a3a", 0.9, 0.0), root, 16)
        g2 = _m(L, "#3f9a3a", 0.5, 0.3)
        for k, (dx, dz) in enumerate(((-0.95, 1.4), (0.95, 1.9), (-0.5, 2.3), (0.5, 1.0), (0.0, 2.9), (-0.9, 0.6))):
            L.sphere("leaf", 0.26, (dx, -0.05, dz), (1.25, 0.22, 0.38), g2, root, 10, rot=(0, math.radians(35 if k % 2 else -35), 0))
        for dx in (-0.45, 0.45): _tuft(L, root, (dx, -0.4, 0), 0.9, "#6cc04a")
    elif name == "den":
        st = _m(L, "#a39683", 0.85, 0.05)
        for k in range(7):
            a = math.pi * k / 6
            L.sphere("stone", 0.2, (math.cos(a) * 0.92, -0.72, math.sin(a) * 0.95), (1.1, 0.8, 0.9), st, root, 12)
        for dx in (-1.6, 1.65, -0.2): _tuft(L, root, (dx, -0.9, 0), 1.0)
        for dx, col in ((-1.35, "#ffb3d1"), (1.4, "#ffd23f")):
            L.sphere("flower", 0.08, (dx, -0.95, 0.2), m=_m(L, col, 0.4, 0.4, 0.4), parent=root, segs=10)
        L.sphere("bed", 0.6, (0, -0.6, 0.03), (1.2, 0.5, 0.12), _m(L, "#c9a56a", 0.9, 0.0), root, 14)
    elif name == "notree":
        for k in range(3):
            L.torus("ringt", 0.205, 0.02, (0, 0, 0.5 + k * 0.5), m=_m(L, "#6f4526", 0.7, 0.1), parent=root)
        for dx, dy in ((0.16, -0.12), (-0.14, -0.1), (0.02, 0.15)):
            L.sphere("coconut", 0.12, (dx, dy, 1.9), m=_m(L, "#6f4526", 0.7, 0.1), parent=root, segs=10)
        _tuft(L, root, (-0.5, -0.2, 0), 1.0); _tuft(L, root, (0.55, 0.1, 0), 0.9)
    elif name == "heart":
        m = _m(L, "#ff8fb0", 0.25, 0.8, 0.5); P["minis"] = []
        for dx, dz in ((-0.55, 0.4), (0.6, 0.55)):
            e = L.empty("mini", (dx * s, 0, dz * s), root)
            for sx in (-1, 1):
                L.sphere("lobe", 0.1 * s, (sx * 0.075 * s, 0, 0.05 * s), m=m, parent=e, segs=12)
            L.cone("tip", 0.15 * s, 0, 0.21 * s, (0, 0, -0.075 * s), (1, 0.62, 1), m, e, rot=(math.pi, 0, 0), verts=16)
            P["minis"].append(e)
    elif name == "arrow":
        P["bob"] = [(c, c.location.z) for c in root.children]
    elif name == "flies":
        for f in P["flies"]:
            for sx in (-1, 1):
                L.cylinder("ant", 0.008, 0.12, (0.2, sx * 0.04, 0.08), m=_m(L, "#2b2b33", 0.5, 0.2), parent=f, rot=(0, 0.9, sx * 0.4), verts=6)


def _pop(x):
    """0..1 -> scale with a little overshoot."""
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    return 1.12 * math.sin(x * math.pi / 2) if x < 0.8 else 1.12 - 0.12 * (x - 0.8) / 0.2


def animate(root, tr, dur, st):
    rec = ANIM.get(root.name)
    if not rec: return
    name, o, P = rec
    if "sparks" in P:                        # sparkles circle the prop
        R = 1.5 if name == "qbox" else 0.75 * 1.5 * o.get("s", 1.0)
        for k, e in enumerate(P["sparks"]):
            a_ = tr * 1.6 + k * math.tau / len(P["sparks"]); tw = 0.6 + 0.4 * math.sin(tr * 5 + k * 1.7)
            e.location = (math.cos(a_) * R, -0.3 if name == "qbox" else -0.1, (1.15 if name == "qbox" else 0.0) + math.sin(a_) * R * (0.85 if name == "qbox" else 1.0))
            e.scale = (tw, tw, tw); e.rotation_euler.y = tr * 2 + k
    if "confetti" in P:
        win = o.get("win")
        for k, c in enumerate(P["confetti"]):
            if win is None or tr < win or tr > win + 1.7: c.scale = (0, 0, 0); continue
            x = tr - win; a_ = k * 2.399; v = 1.6 + 0.9 * ((k * 37) % 10) / 10
            c.location = (math.cos(a_) * v * x, -0.25 - 0.1 * x, math.sin(a_) * v * x + 1.2 * x - 1.9 * x * x)
            c.rotation_euler = (x * 7 + k, x * 5 + 2 * k, x * 3); sc = 1.0 if x < 1.2 else max(0.0, 1 - (x - 1.2) / 0.5); c.scale = (0.1 * sc, 0.02 * sc, 0.07 * sc)
    if "bubbles" in P:
        for k, b in enumerate(P["bubbles"]):
            ph = (tr * 0.6 + k * 0.27) % 1.0; sc = 0.3 + ph * 1.2 if ph < 0.85 else 0.0; b.scale = (sc, sc, sc * 0.8)
    if "smoke" in P:
        h_ = o.get("h", 3.3)
        for k, p in enumerate(P["smoke"]):
            ph = (tr * 0.35 + k / 3.0) % 1.0; p.location = (0.62 + 0.35 * ph * math.sin(tr + k), 0.2, h_ + 1.3 + ph * 1.1); sc = 0.5 + ph * 0.9 if ph < 0.9 else 0.0; p.scale = (sc, sc, sc)
    if "minis" in P:
        for k, e in enumerate(P["minis"]):
            b_ = 1 + 0.25 * math.sin(tr * 4 + k * 2); e.scale = (b_, b_, b_); e.location.z += 0.0
    if "bob" in P:
        for c, z0 in P["bob"]: c.location.z = z0 + 0.12 * math.sin(tr * 5.0)
    if name == "sign":
        win = o.get("win")
        if win is not None and tr >= win:
            x = tr - win; b = 1 + 0.16 * math.exp(-x * 2.2) * math.cos(x * 9)
            root.scale = tuple(v * b for v in root.scale)
            c = _pop(x / 0.35); P["check"].scale = (c, c, c)
        else:
            P["check"].scale = (0, 0, 0)
    elif name == "qbox":
        P["q"].rotation_euler.z = 0.25 * math.sin(tr * 3.0); root.rotation_euler.z = 0.05 * math.sin(tr * 2.2)
    elif name == "dots":
        for k, d in enumerate(P["dots"]):
            c = _pop((tr - k * dur / 3.4) / 0.25) * (1 + 0.12 * math.sin(tr * 6 + k)); d.scale = (c, c, c)
    elif name in ("count", "cars", "bones"):
        times = o.get("times") or [k * o.get("gap", 0.7) for k in range(len(P["items"]))]
        for k, e in enumerate(P["items"]):
            t0 = times[k] if k < len(times) else times[-1] + 0.6 * (k - len(times) + 1)
            c = _pop((tr - t0) / 0.3); e.scale = (c, c, c)
            if name == "bones":   # the bone being counted bounces
                x = tr - t0; b = 1 + (0.35 * math.exp(-x * 5) if x >= 0 else 0.0); P["bones"][k].scale = (b, b, b)
    elif name == "flies":
        leave = o.get("leave"); R = o.get("r", 0.9)
        for k, f in enumerate(P["flies"]):
            a = tr * (3.4 + 0.5 * k) + k * 1.9
            x, y, z = math.cos(a) * R * (0.7 + 0.2 * math.sin(tr * 1.7 + k)), math.sin(a) * R * 0.45, 0.25 * math.sin(a * 2.3 + k) + 0.12 * k
            sc = 1.0
            if leave is not None and tr > leave:
                u = min(1.0, (tr - leave) / 1.6); x += u * u * (4.5 + k); z += u * u * (2.5 + 0.5 * k); sc = 1 - 0.85 * u
            f.location = (x, y, z); f.rotation_euler.z = a + math.pi / 2; f.scale = (sc, sc, sc)
    elif name == "mud":
        for k, d in enumerate(P["drops"]):
            ph = (tr * 1.4 + k * 0.33) % 1.0; d.location.z = 0.1 + 0.7 * math.sin(ph * math.pi); d.scale = (1, 1, 1) if ph < 0.95 else (0, 0, 0)
    elif name == "sun":
        P["rays"].rotation_euler.y = tr * 0.6
    elif name == "snowflake":
        root.rotation_euler.y = tr * 0.8
    elif name == "pool":
        for k, r in enumerate(P["rip"]):
            ph = (tr * 0.5 + k * 0.5) % 1.0; s = 0.4 + 2.4 * ph; r.scale = (s, s, 1 - 0.6 * ph)
    elif name == "ruler":
        P["top"].location.x = 0.06 * math.sin(tr * 5)
    elif name == "rings":
        for k, r in enumerate(P["rings"]):
            ph = (tr * 0.75 + k * 0.25) % 1.0; s = 0.5 + 1.9 * ph
            r.location = (ph * o.get("reach", 5.0), 0, 0); r.scale = (s, s, max(0.05, 1 - ph))
    elif name == "zzz":
        for k, z in enumerate(P["z"]):
            ph = (tr * 0.45 + k * 0.33) % 1.0; z.location.z = (k * 0.42 + ph * 0.5) * o.get("s", 1.0); z.rotation_euler.y = 0.2 * math.sin(tr * 2 + k)
    elif name == "heart":
        b = 1 + 0.12 * abs(math.sin(tr * 3.2)); root.scale = tuple(v * b for v in root.scale)
    elif name == "notree":
        if "cross" in P: c = _pop((tr - o.get("cross_at", 0.8)) / 0.3); P["cross"].scale = (c, c, c)
    elif name == "arrow":
        root.location.z += 0.0   # bobbing is done through the engine's own wobble
