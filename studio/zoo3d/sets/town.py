"""Tiny Truck Town: a candy-colored toy-town street. Road with lane lines and a crosswalk, sidewalks, a fire station
behind the host, candy shops, lollipop trees, bunting, a traffic light that changes on the beat, hills and clouds.

prop(L, name, at, **opts): ladder, hose, cone, hydrant, helmet, siren, water, bell, number (n=, color=), sign (text=, color=)
animate(L, SET, f, t, s): traffic light steps on each bar, bunting sways, clouds drift.
"""
import math
import bpy


def _prism(L, name, w, d, h, loc, m, parent=None):
    """Gable roof: triangle facing -Y (front), ridge along Y. Base centered at loc."""
    v = [(-w / 2, -d / 2, 0), (w / 2, -d / 2, 0), (0, -d / 2, h), (-w / 2, d / 2, 0), (w / 2, d / 2, 0), (0, d / 2, h)]
    fc = [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (0, 2, 5, 3)]
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], fc); me.update()
    o = bpy.data.objects.new(name, me); L.scene().collection.objects.link(o)
    o.data.materials.append(m); o.location = loc
    if parent is not None: o.parent = parent
    b = o.modifiers.new("Bevel", "BEVEL"); b.width = 0.08; b.segments = 2
    return o


def _box(L, name, dims, loc, m, parent=None, bevel=0.06, segs=2):
    o = L.cube(name, 1, loc, (1, 1, 1), m, parent)
    for vv in o.data.vertices:
        vv.co.x *= dims[0]; vv.co.y *= dims[1]; vv.co.z *= dims[2]
    if bevel:
        b = o.modifiers.new("Bevel", "BEVEL"); b.width = bevel; b.segments = segs; b.use_clamp_overlap = True
        L.smooth(o)
    return o


def _window(L, x, y, z, w, h, M, tag):
    _box(L, f"WinFrame{tag}", (w + 0.16, 0.1, h + 0.16), (x, y - 0.03, z), M["white"], bevel=0.04)
    _box(L, f"WinGlass{tag}", (w, 0.1, h), (x, y - 0.07, z), M["glass"], bevel=0.03)


def _shop(L, k, x, y, w, h, body_hex, roof_hex, M, awning=None, roof="gable", sign=None):
    bm = L.mat(f"TownWall{body_hex}", body_hex, 0.55, coat=0.25)
    rm = L.mat(f"TownRoof{roof_hex}", roof_hex, 0.45, coat=0.4)
    _box(L, f"Shop{k}", (w, 3.0, h), (x, y + 1.5, h / 2), bm, bevel=0.12)
    if roof == "gable":
        _prism(L, f"ShopRoof{k}", w + 0.5, 3.4, 1.3, (x, y + 1.5, h - 0.02), rm)
    else:
        _box(L, f"ShopCornice{k}", (w + 0.3, 3.3, 0.35), (x, y + 1.5, h + 0.1), rm, bevel=0.1)
    # door + windows
    _box(L, f"ShopDoor{k}", (0.85, 0.12, 1.5), (x, y - 0.03, 0.75), M["door"], bevel=0.08)
    L.sphere(f"ShopKnob{k}", 0.05, (x + 0.27, y - 0.12, 0.75), m=M["gold"], segs=10)
    for sx in (-1, 1):
        _window(L, x + sx * w * 0.3, y, 1.25, w * 0.24, 0.9, M, f"{k}{sx}")
    if h > 3.6:
        _window(L, x, y, h - 1.1, w * 0.45, 0.75, M, f"{k}up")
    if awning:
        stripes = 6
        for i in range(stripes):
            am = M["white"] if i % 2 else L.mat(f"Awn{awning}", awning, 0.5, sheen=0.4)
            sw = (w * 0.9) / stripes
            _box(L, f"Awn{k}_{i}", (sw, 0.9, 0.08), (x - w * 0.45 + sw * (i + 0.5), y - 0.42, 2.25), am, bevel=0.03, segs=1).rotation_euler = (-0.35, 0, 0)
    if sign:
        txt, col = sign
        L.text3d(f"ShopSign{k}", txt, 0.42, (x, y - 0.12, 2.75 if not awning else 2.75), L.mat(f"SignTxt{col}", col, 0.3, coat=0.6), extrude=0.06, bevel=0.015)


def _tree(L, k, x, y, s, M):
    L.cylinder(f"TreeTrunk{k}", 0.13 * s, 1.4 * s, (x, y, 0.7 * s), m=M["bark"], verts=12)
    leaf = M["leaf"][k % len(M["leaf"])]
    L.sphere(f"TreeTop{k}", 0.85 * s, (x, y, 1.75 * s), (1, 1, 1.05), leaf, segs=24)
    L.sphere(f"TreeTop2{k}", 0.55 * s, (x + 0.35 * s, y - 0.2 * s, 1.55 * s), m=leaf, segs=18)


def build(L, rng, **_):
    L.sky("#74c4ff", 0.85, nishita=False)
    L.light("Sun", "SUN", 3.6, rot=(math.radians(50), 0, math.radians(-32)), color=(1, 0.94, 0.84), angle=math.radians(5))
    L.light("Fill", "AREA", 420, (-6, -9, 6), (math.radians(58), 0, math.radians(-35)), (1, 0.93, 0.86), 9)
    L.light("Rim", "AREA", 300, (6, 7, 5), (math.radians(-58), 0, math.radians(150)), (0.78, 0.88, 1), 6)
    M = {
        "grass": L.mat("TownGrass", "#6cc24a", 0.85, sheen=0.4, bump=0.25, bump_scale=40),
        "road": L.mat("TownRoad", "#4d5566", 0.8, bump=0.08, bump_scale=60),
        "walk": L.mat("TownWalk", "#f4e3c4", 0.75),
        "curb": L.mat("TownCurb", "#e6d3b0", 0.7),
        "lineW": L.mat("TownLineW", "#ffffff", 0.5),
        "lineY": L.mat("TownLineY", "#ffd23f", 0.45),
        "white": L.mat("TownWhite", "#fffaf2", 0.5, coat=0.2),
        "glass": L.mat("TownGlass", "#9adcff", 0.1, coat=1.0),
        "door": L.mat("TownDoor", "#8d5a3b", 0.5, coat=0.3),
        "gold": L.mat("TownGold", "#ffcf3a", 0.25, metal=0.6, coat=0.5),
        "bark": L.mat("TownBark", "#8a5a3a", 0.85),
        "leaf": [L.mat(f"TownLeaf{i}", c, 0.7, sss=0.06, sheen=0.3) for i, c in enumerate(("#4cbb4a", "#7ed957", "#3fae5a"))],
        "pole": L.mat("TownPole", "#4a5060", 0.4, coat=0.3),
        "cloud": L.mat("TownCloud", "#ffffff", 0.9, sss=0.15, emission="#ffffff", emit=0.15),
    }
    # ground, road, sidewalks
    L.cube("Ground", 1, (0, 20, -0.06), (120, 90, 0.1), M["grass"])
    L.cube("Road", 1, (0, 0.2, -0.05), (120, 6.8, 0.1), M["road"])
    for y0, y1, tag in ((3.6, 6.2, "B"), (-5.2, -3.2, "F")):
        L.cube(f"Walk{tag}", 1, (0, (y0 + y1) / 2, 0.06), (120, y1 - y0, 0.12), M["walk"])
        cy = y0 if tag == "B" else y1
        L.cube(f"Curb{tag}", 1, (0, cy, 0.08), (120, 0.22, 0.16), M["curb"])
    for i in range(-14, 15):   # dashed yellow center line (behind the cast)
        L.cube("Dash", 1, (i * 2.2, 2.55, 0.003), (1.2, 0.16, 0.01), M["lineY"])
    for y in (-2.95, 3.35):
        L.cube("EdgeLine", 1, (0, y, 0.003), (120, 0.12, 0.01), M["lineW"])
    for i in range(7):         # crosswalk
        L.cube("Zebra", 1, (8.2, -2.6 + i * 0.85, 0.004), (2.4, 0.45, 0.01), M["lineW"])

    # fire station behind the host
    red = L.mat("StationRed", "#e8402f", 0.5, coat=0.35)
    _box(L, "Station", (7.0, 3.6, 4.6), (0, 9.2, 2.3), red, bevel=0.14)
    _box(L, "StationTrim", (7.3, 3.8, 0.4), (0, 9.2, 4.7), M["white"], bevel=0.1)
    _prism(L, "StationRoof", 4.0, 3.2, 1.3, (0, 9.2, 4.88), L.mat("StationRoofM", "#b8322a", 0.45, coat=0.4))
    for sx in (-1, 1):
        _box(L, f"StationDoorFrame{sx}", (2.6, 0.12, 3.0), (sx * 1.7, 7.36, 1.5), M["white"], bevel=0.08)
        _box(L, f"StationDoor{sx}", (2.3, 0.14, 2.75), (sx * 1.7, 7.32, 1.4), L.mat("StationDoorM", "#fff1d6", 0.5, coat=0.3), bevel=0.06)
        for r in range(2):
            for c in range(3):
                _box(L, "StationDoorWin", (0.55, 0.06, 0.35), (sx * 1.7 + (c - 1) * 0.68, 7.24, 2.2 - r * 0.5), M["glass"], bevel=0.03, segs=1)
    sign = _box(L, "StationSign", (3.4, 0.16, 0.8), (0, 7.3, 3.75), M["white"], bevel=0.1)
    L.text3d("StationText", "FIRE STATION", 0.5, (0, 7.17, 3.72), L.mat("StationTxt", "#d32f2f", 0.35, coat=0.6), extrude=0.05, bevel=0.012)
    L.sphere("StationBell", 0.38, (0, 7.6, 5.35), (1, 1, 1.1), M["gold"], segs=24)

    # candy shops
    shops = [(-6.4, 7.3, 3.2, 4.2, "#ff8fbf", "#e85d9b", "#ff5d9e", "gable", ("CAKES", "#ffffff")),
             (-10.2, 7.6, 3.6, 3.4, "#6fe0c8", "#2fb59a", None, "flat", ("TOYS", "#ff5d5d")),
             (-14.2, 7.8, 3.6, 4.6, "#b79cff", "#7e5be0", "#ffd23f", "gable", None),
             (6.4, 7.3, 3.2, 3.8, "#ffd23f", "#ff9f1a", "#ff7a45", "flat", ("ICE CREAM", "#e8402f")),
             (10.2, 7.6, 3.6, 4.4, "#7cc6ff", "#3b8be0", None, "gable", ("BOOKS", "#ffffff")),
             (14.2, 7.8, 3.6, 3.6, "#ffab73", "#ff7043", "#6fe0c8", "flat", None)]
    for k, (x, y, w, h, bc, rc, aw, rf, sg) in enumerate(shops):
        _shop(L, k, x, y, w, h, bc, rc, M, aw, rf, sg)

    # trees, hills, clouds
    for k, (x, y, s) in enumerate(((-4.3, 5.3, 1.1), (4.3, 5.3, 1.05), (-8.3, 5.4, 1.0), (8.4, 5.4, 1.1), (-12.3, 5.5, 1.05),
                                    (12.3, 5.5, 0.95), (-17, 9, 1.4), (17, 9, 1.3), (-3.5, 14, 1.6), (4.5, 14.5, 1.7),
                                    (-9, -6.5, 1.2), (9.5, -6.3, 1.15))):
        _tree(L, k, x, y, s, M)
    hill = [L.mat(f"Hill{i}", c, 0.85, sheen=0.4) for i, c in enumerate(("#7fd65a", "#5ec26a", "#9be070"))]
    for k, (x, y, r, sz) in enumerate(((-22, 34, 12, 0.45), (0, 40, 16, 0.4), (24, 34, 13, 0.45), (-8, 30, 8, 0.5), (12, 28, 7, 0.55))):
        L.sphere("Hill", r, (x, y, -r * sz * 0.35), (1.6, 1, sz), hill[k % 3], segs=32)
    clouds = []
    for k, (x, y, z, s) in enumerate(((-14, 45, 15, 2.4), (6, 50, 17, 3.0), (20, 44, 13, 2.2), (-3, 42, 12, 1.6))):
        c = L.empty(f"Cloud{k}", (x, y, z))
        for dx, dz, r in ((0, 0, 1.0), (1.0, -0.2, 0.75), (-1.0, -0.25, 0.7), (0.45, 0.45, 0.7)):
            L.sphere(f"CloudPuff{k}", r * s, (dx * s, 0, dz * s), (1, 0.7, 0.85), M["cloud"], c, 20)
        clouds.append((c, x))

    # bunting across the street front of the shops
    flag_cols = ("#ff5d5d", "#ffd23f", "#4fc3f7", "#7ed957", "#ff8fbf", "#b79cff")
    bunting = L.empty("Bunting", (0, 5.9, 0))
    for i in range(26):
        x = -13 + i * 1.04
        zc = 4.4 - 0.5 * math.cos(math.pi * ((x + 13) % 6.5) / 6.5 * 2) * 0.5
        fm = L.mat(f"Flag{i % 6}", flag_cols[i % 6], 0.55, sheen=0.4)
        L.cone("Flag", 0.26, 0.0, 0.5, (x, 0, zc - 0.3), (1, 0.12, 1), fm, bunting, (math.pi, 0, 0), verts=3)
    for sx in (-1, 1):
        L.cylinder("BuntPole", 0.06, 4.6, (sx * 13.3, 5.9, 2.3), m=M["pole"], verts=12)

    # traffic light (back sidewalk, right of the host)
    tl = {}
    L.cylinder("TLPole", 0.08, 3.4, (5.2, 4.3, 1.7), m=M["pole"], verts=16)
    _box(L, "TLBox", (0.62, 0.42, 1.6), (5.2, 4.2, 3.7), L.mat("TLYellow", "#ffcc2a", 0.4, coat=0.6), bevel=0.15, segs=3)
    for k, (nm, col, zz) in enumerate((("red", "#ff3030", 4.2), ("yellow", "#ffb300", 3.7), ("green", "#2fe060", 3.2))):
        m = L.mat(f"TL_{nm}", col, 0.2, coat=1.0, emission=col, emit=0.1)
        L.sphere(f"TLLamp{nm}", 0.19, (5.2, 3.98, zz), (1, 0.5, 1), m, segs=20)
        _box(L, f"TLVisor{nm}", (0.46, 0.18, 0.05), (5.2, 3.9, zz + 0.2), M["pole"], bevel=0.02, segs=1)
        tl[nm] = m
    # fire hydrant + planters (story details)
    hyd = L.mat("Hydrant", "#ff3b30", 0.35, coat=0.8)
    L.cylinder("HydBody", 0.2, 0.6, (-5.3, 4.2, 0.42), m=hyd, verts=24)
    L.sphere("HydCap", 0.21, (-5.3, 4.2, 0.72), (1, 1, 0.7), L.mat("HydCap", "#ffd23f", 0.35, coat=0.8), segs=20)
    for sx in (-1, 1):
        L.cylinder("HydNub", 0.08, 0.5, (-5.3, 4.2, 0.48), m=hyd, rot=(0, math.pi / 2, 0), verts=16)
    pm = L.mat("Planter", "#ff8a65", 0.5, coat=0.4)
    pet = [L.mat(f"Petal{i}", c, 0.5, sss=0.2) for i, c in enumerate(("#ff6f9c", "#ffd23f", "#ffffff", "#b57cff", "#ff9f43"))]
    for k, x in enumerate((-6.8, 6.8, -11.5, 11.5)):
        _box(L, f"Planter{k}", (1.4, 0.6, 0.5), (x, -4.2, 0.37), pm, bevel=0.1)
        L.sphere(f"Bush{k}", 0.55, (x, -4.2, 0.72), (1.25, 0.55, 0.6), M["leaf"][k % 3], segs=18)
        for j in range(5):
            L.sphere("Flower", 0.09, (x - 0.5 + j * 0.25, -4.42, 0.95 + 0.06 * (j % 2)), (1, 1, 0.7), pet[(j + k) % 5], segs=10)
    for i in range(40):   # flowers in the front grass and along the back lawn
        x = -16 + rng.random() * 32
        y = -6.0 - rng.random() * 3 if i % 2 else 6.5 + rng.random() * 0.4
        if abs(x) < 3.8 and y > 0: continue
        L.sphere("Flower", 0.08, (x, y, 0.08 if y < 0 else 0.13), (1, 1, 0.6), pet[i % 5], segs=10)

    return {
        "spots": {"center": (0, 0, 0), "left": (-3.6, 0.9, 0), "right": (3.6, 0.9, 0),
                  "far_left": (-6.6, 2.2, 0), "far_right": (6.6, 2.4, 0), "back": (0, 3.0, 0)},
        "cams": {"wide": ((1.0, -11.5, 2.5), (0.8, 1.4, 1.6)), "center": (0, 0.6, 1.3), "orbit_r": 10,
                 "street": ((-7.5, -8.5, 1.6), (0.5, 1.0, 1.4)), "station": ((2.5, -9.0, 5.2), (0, 3.0, 2.2))},
        "prop_spots": {"top": (0, 2.0, 3.85), "left": (-1.75, -0.8, 3.1), "right": (1.75, -0.8, 3.1), "front": (0, -2.6, 0.9),
                       "far_left": (-5.4, -0.6, 2.9), "far_right": (5.4, -0.6, 2.9)},
        "exposure": -0.3, "look": "AgX - Punchy",
        "_tl": tl, "_clouds": clouds, "_bunting": bunting,
    }


def animate(L, SET, f, t, s):
    beat = 60 / s.get("bpm", 116)   # engine passes only "beat"; see report for the bpm patch
    step = int(t / (beat * 4)) % 3    # one light per bar: green -> yellow -> red
    on = {0: "green", 1: "yellow", 2: "red"}[step]
    pulse = 0.85 + 0.15 * math.cos(math.pi * 2 * s.get("beat", 0))
    for nm, m in SET["_tl"].items():
        m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = (5.0 * pulse) if nm == on else 0.05
    for c, x0 in SET["_clouds"]:
        c.location.x = x0 + math.sin(t * 0.05 + x0) * 2.0
    SET["_bunting"].rotation_euler.x = math.sin(t * 1.6) * 0.03


def prop(L, name, at, **o):
    """Teaching props, centered on `at` (they pop in mid-air next to the cast)."""
    root = L.empty("TTProp_" + name, at)
    red = L.mat("PropRed", "#e8302a", 0.3, coat=1.0)
    chrome = L.mat("PropChrome", "#e3e9ee", 0.2, metal=0.7, coat=0.5)
    gold = L.mat("PropGold", "#ffcf3a", 0.25, metal=0.5, coat=0.7)
    if name == "ladder":
        for sx in (-1, 1):
            _box(L, "PLRail", (0.12, 0.12, 1.9), (sx * 0.38, 0, 0), chrome, root, 0.04)
        for k in range(5):
            L.cylinder("PLRung", 0.05, 0.76, (0, 0, -0.8 + k * 0.4), m=red, parent=root, rot=(0, math.pi / 2, 0), verts=12)
        root.rotation_euler = (0, 0.15, 0)
    elif name == "hose":
        hm = L.mat("PropHose", "#ffd23f", 0.4, coat=0.6)
        for k in range(3):
            L.torus("PHCoil", 0.55, 0.11, (0, 0, -0.25 + k * 0.22), (1, 1, 1), hm, root, (math.pi / 2 * 0, 0, 0))
        root.rotation_euler = (math.radians(70), 0, 0)
        L.cylinder("PHNozzle", 0.1, 0.5, (0.75, 0, 0.3), m=gold, parent=root, rot=(0, math.pi / 2, 0), verts=16)
    elif name == "cone":
        cm = L.mat("PropCone", "#ff7a1a", 0.35, coat=0.6)
        L.cone("PCone", 0.5, 0.08, 1.3, (0, 0, 0.05), m=cm, parent=root)
        for zz, rr in ((0.15, 0.36), (-0.2, 0.44)):
            L.cylinder("PConeBand", rr, 0.14, (0, 0, zz), m=L.mat("PropWhite", "#ffffff", 0.4), parent=root, verts=40)
        _box(L, "PConeBase", (1.1, 1.1, 0.12), (0, 0, -0.66), cm, root, 0.05)
    elif name == "hydrant":
        L.cylinder("PHyd", 0.32, 0.95, (0, 0, 0), m=red, parent=root, verts=32)
        L.sphere("PHydTop", 0.34, (0, 0, 0.47), (1, 1, 0.7), gold, root, 24)
        L.cylinder("PHydArm", 0.13, 0.9, (0, 0, 0.1), m=red, parent=root, rot=(0, math.pi / 2, 0), verts=16)
        L.cylinder("PHydFace", 0.15, 0.2, (0, -0.32, 0.1), m=gold, parent=root, rot=(math.pi / 2, 0, 0), verts=16)
    elif name == "helmet":
        L.sphere("PHelm", 0.62, (0, 0, 0), (1, 1.08, 0.85), red, root, 32)
        L.cylinder("PHelmBrim", 0.82, 0.08, (0, 0.1, -0.3), (1, 1.2, 1), red, root, verts=40)
        L.cylinder("PHelmShield", 0.26, 0.06, (0, -0.62, 0.05), m=gold, parent=root, rot=(math.pi / 2 - 0.3, 0, 0), verts=24)
        L.text3d("PHelmNum", "1", 0.3, (0, -0.67, 0.04), red, root, 0.03, 0.006, (math.pi / 2 - 0.3, 0, 0))
    elif name == "siren":
        L.sphere("PSiren", 0.55, (0, 0, 0.1), (1, 1, 0.9), L.mat("PropLamp", "#ff2a2a", 0.15, coat=1.0, emission="#ff2a2a", emit=3.0), root, 32)
        L.cylinder("PSirenBase", 0.62, 0.25, (0, 0, -0.35), m=chrome, parent=root, verts=32)
    elif name == "water":
        wm = L.mat("PropWater", "#39a8ff", 0.05, coat=1.0, sss=0.1)
        L.sphere("PDrop", 0.55, (0, 0, -0.1), m=wm, parent=root, segs=32)
        L.cone("PDropTip", 0.47, 0.0, 0.8, (0, 0, 0.45), m=wm, parent=root)
        L.sphere("PDropGlint", 0.1, (-0.2, -0.45, 0.05), (1, 0.4, 1.4), L.mat("PropGlint", "#ffffff", 0.0, emission="#ffffff", emit=2), root, 12)
    elif name == "bell":
        L.cone("PBell", 0.6, 0.25, 0.9, (0, 0, 0), m=gold, parent=root)
        L.sphere("PBellTop", 0.27, (0, 0, 0.45), m=gold, parent=root, segs=20)
        L.sphere("PBellBall", 0.13, (0, 0, -0.5), m=chrome, parent=root, segs=16)
    elif name == "number":
        col = o.get("color", "#ffd23f")
        disc = L.mat(f"PropNum{col}", col, 0.3, coat=0.9)
        L.cylinder("PNumDisc", 0.62, 0.16, (0, 0, 0), m=disc, parent=root, rot=(math.pi / 2, 0, 0), verts=40)
        L.torus("PNumRim", 0.62, 0.06, (0, 0, 0), m=L.mat("PropWhite", "#ffffff", 0.4), parent=root, rot=(math.pi / 2, 0, 0))
        L.text3d("PNumTxt", str(o.get("n", 1)), 0.85, (0, -0.1, -0.02), L.mat("PropNumTxt", "#ffffff", 0.3, coat=0.5), root, 0.08, 0.02)
    else:   # sign
        col = o.get("color", "#e8302a")
        txt = o.get("text", name.upper())
        w = max(1.6, 0.42 * len(txt) + 0.5)
        _box(L, "PSignBoard", (w, 0.16, 0.9), (0, 0, 0), L.mat(f"PropSign{col}", col, 0.3, coat=0.9), root, 0.12)
        L.text3d("PSignTxt", txt, 0.5, (0, -0.12, -0.02), L.mat("PropNumTxt", "#ffffff", 0.3, coat=0.5), root, 0.05, 0.015)
    return root
