"""Sunny kitchen counter with a garden window: Fruity Friends' home set (see API.md).

The cast stands on a big butcher-block counter (the friends are fruit-sized, the kitchen is giant). Behind them:
a candy-colored tiled backsplash, a big window onto a sunny veggie garden with sunflowers and hills, gingham curtains,
mint cabinets, jars, herbs on the sill, a fruit bowl (left) and a cutting board with veggies (right, no knife).
prop(name): water_drop, bubbles, plate, basket, number (opts text/color), bigfruit (opts kind), rainbow, floatbowl,
carrot_ground, banana_hand, tree, magnifier, heart, star, sun.
"""
import math
import bmesh


def _lin(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


# ------------------------------------------------------------------ procedural materials
def _tiles(L, name, colors, size=0.9, axis="XZ"):
    """Candy-colored square tiles with white grout: random color per tile (white noise on the floored position)."""
    m = L.mat(name, "#ffffff", 0.25, coat=0.6)
    if m.get("tiles"): return m
    m["tiles"] = 1
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); com = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    nt.links.new(sep.outputs[axis[0]], com.inputs["X"]); nt.links.new(sep.outputs[axis[1]], com.inputs["Y"])
    sc = nt.nodes.new("ShaderNodeVectorMath"); sc.operation = "SCALE"; sc.inputs["Scale"].default_value = 1 / size
    nt.links.new(com.outputs[0], sc.inputs[0])
    fl = nt.nodes.new("ShaderNodeVectorMath"); fl.operation = "FLOOR"; nt.links.new(sc.outputs[0], fl.inputs[0])
    wn = nt.nodes.new("ShaderNodeTexWhiteNoise"); wn.noise_dimensions = "3D"; nt.links.new(fl.outputs[0], wn.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.interpolation = "CONSTANT"
    els = cr.color_ramp.elements
    while len(els) < len(colors): els.new(0.5)
    for k, c in enumerate(colors):
        els[k].position = k / len(colors); els[k].color = (*_lin(c), 1)
    nt.links.new(wn.outputs["Value"], cr.inputs["Fac"])
    # grout lines: distance to the tile edge
    fr = nt.nodes.new("ShaderNodeVectorMath"); fr.operation = "FRACTION"; nt.links.new(sc.outputs[0], fr.inputs[0])
    s2 = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(fr.outputs[0], s2.inputs[0])
    def edge(out):
        a = nt.nodes.new("ShaderNodeMath"); a.operation = "PINGPONG"; a.inputs[1].default_value = 0.5
        nt.links.new(out, a.inputs[0]); return a
    ex, ey = edge(s2.outputs["X"]), edge(s2.outputs["Y"])
    mn = nt.nodes.new("ShaderNodeMath"); mn.operation = "MINIMUM"; nt.links.new(ex.outputs[0], mn.inputs[0]); nt.links.new(ey.outputs[0], mn.inputs[1])
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "LESS_THAN"; gt.inputs[1].default_value = 0.035
    nt.links.new(mn.outputs[0], gt.inputs[0])
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    nt.links.new(gt.outputs[0], mix.inputs["Factor"]); nt.links.new(cr.outputs["Color"], mix.inputs[6]); mix.inputs[7].default_value = (*_lin("#fdf8ef"), 1)
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.5; bp.inputs["Distance"].default_value = 0.02; bp.invert = True
    nt.links.new(gt.outputs[0], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def _wood(L, name, c1, c2, scale=1.4):
    m = L.mat(name, c1, 0.45, coat=0.35)
    if m.get("wood"): return m
    m["wood"] = 1
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "X"
    wv.inputs["Scale"].default_value = scale; wv.inputs["Distortion"].default_value = 7; wv.inputs["Detail"].default_value = 3
    cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (*_lin(c1), 1); cr.color_ramp.elements[1].color = (*_lin(c2), 1)
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"]); nt.links.new(wv.outputs["Fac"], cr.inputs["Fac"]); nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.08; nt.links.new(wv.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def _gingham(L, name, hexc):
    m = L.mat(name, hexc, 0.8, sheen=0.6)
    if m.get("ging"): return m
    m["ging"] = 1
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); ck = nt.nodes.new("ShaderNodeTexChecker"); ck.inputs["Scale"].default_value = 9
    ck.inputs["Color1"].default_value = (*_lin(hexc), 1); ck.inputs["Color2"].default_value = (*_lin("#fff5f7"), 1)
    nt.links.new(tc.outputs["Generated"], ck.inputs["Vector"]); nt.links.new(ck.outputs["Color"], b.inputs["Base Color"])
    return m


def _glass(L, name, hexc, alpha=0.25, film=False):
    m = L.mat(name, hexc, 0.03, coat=0.5)
    if m.get("glass"): return m
    m["glass"] = 1
    b = m.node_tree.nodes["Principled BSDF"]
    for k, v in (("Transmission Weight", 1.0), ("IOR", 1.33)):
        if k in b.inputs: b.inputs[k].default_value = v
    if film and "Thin Film Thickness" in b.inputs:
        b.inputs["Thin Film Thickness"].default_value = 420; b.inputs["Thin Film IOR"].default_value = 1.33
    return m


def _bowl_mesh(L, name, r, m, parent=None, loc=(0, 0, 0), scale=(1, 1, 1), cut=0.15):
    o = L.sphere(name, r, loc, scale, m, parent, 40)
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > r * cut], context="VERTS")
    bm.to_mesh(o.data); bm.free()
    sol = o.modifiers.new("Sol", "SOLIDIFY"); sol.thickness = r * 0.06
    return o


def _star_mesh(L, name, r, m, parent=None, loc=(0, 0, 0), depth=0.25):
    import bpy
    me = bpy.data.meshes.new(name)
    vs = [(0, 0, 0)]
    for k in range(10):
        a = k / 10 * math.tau + math.pi / 2; rr = r if k % 2 == 0 else r * 0.45
        vs.append((math.cos(a) * rr, 0, math.sin(a) * rr))
    fs = [(0, 1 + k, 1 + (k + 1) % 10) for k in range(10)]
    me.from_pydata(vs, [], fs); me.update()
    o = bpy.data.objects.new(name, me); L.scene().collection.objects.link(o)
    o.data.materials.append(m); o.location = loc
    if parent is not None: o.parent = parent
    so = o.modifiers.new("Sol", "SOLIDIFY"); so.thickness = depth; so.offset = 0
    bv = o.modifiers.new("Bev", "BEVEL"); bv.width = depth * 0.3; bv.segments = 3
    L.smooth(o)
    return o


def _shift(bpy, before, dz):
    for o in bpy.data.objects:
        if o not in before and o.parent is None:
            o.location.z += dz


# ------------------------------------------------------------------ set
def build(L, rng, **_):
    import bpy
    w = L.sky(nishita=True, sun_elev=42)
    try: w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.11
    except Exception: pass
    L.light("Sun", "SUN", 4.2, rot=(math.radians(52), 0, math.radians(-50)), color=(1, 0.94, 0.84), angle=math.radians(5))
    L.light("Fill", "AREA", 300, (-3, -11, 6), (math.radians(62), 0, math.radians(-12)), (1, 0.93, 0.86), 10)
    L.light("Rim", "AREA", 380, (2, 4.5, 6.5), (math.radians(-55), 0, math.radians(175)), (1, 0.96, 0.85), 6)
    L.light("Bounce", "AREA", 160, (0, -4, 0.3), (math.radians(-80), 0, 0), (1, 0.85, 0.65), 8)

    A = {}
    noshadow = []
    # counter (butcher block) + front lip
    wood = _wood(L, "CounterWood", "#e9ae6e", "#c98546", 0.9)
    L.cube("Counter", 1, (0, -4, -0.5), (30, 22, 1), wood, bevel=0.05)
    L.cylinder("Placemat", 1.0, 0.03, (0, 0.6, 0.015), (6.2, 2.6, 1), _gingham(L, "GinghamMat", "#5cc8f0"), verts=48)
    # back wall: tiled backsplash with a window opening
    tiles = _tiles(L, "Tiles", ("#ff4f8b", "#22c995", "#2fa3ff", "#ffc61a", "#ff7a1f", "#9a5cff"), 0.85, "XZ")
    tiles_side = _tiles(L, "TilesSide", ("#ff4f8b", "#22c995", "#2fa3ff", "#ffc61a", "#ff7a1f", "#9a5cff"), 0.85, "YZ")
    paint = L.mat("WallPaint", "#ffe08a", 0.75, sheen=0.2)
    L.cube("Backsplash", 1, (0, 6.2, 1.1), (30, 0.4, 2.2), tiles)
    before = set(bpy.data.objects)
    for nm, (x0, x1, z0, z1) in {"WallL": (-15, -3.8, 2.8, 12), "WallR": (3.8, 15, 2.8, 12), "WallT": (-3.8, 3.8, 7.6, 12)}.items():
        noshadow.append(L.cube(nm, 1, ((x0 + x1) / 2, 6.2, (z0 + z1) / 2), (x1 - x0, 0.4, z1 - z0), paint))
    for sx in (-1, 1):
        L.cube("SideSplash", 1, (15 * sx, 0, 1.4), (0.4, 14, 2.8), tiles_side)
        noshadow.append(L.cube("SideWall", 1, (15 * sx, 0, 7.4), (0.4, 14, 9.2), paint))
    # window frame, sill and mullions
    white = L.mat("FrameWhite", "#ffffff", 0.3, coat=0.5)
    sunny = L.mat("FrameYellow", "#ffcf3a", 0.3, coat=0.6)
    L.cube("Sill", 1, (0, 5.75, 2.82), (8.6, 0.9, 0.2), white, bevel=0.06)
    for nm, loc, sc in (("FrL", (-3.75, 6.0, 5.2), (0.32, 0.5, 4.9)), ("FrR", (3.75, 6.0, 5.2), (0.32, 0.5, 4.9)),
                        ("FrT", (0, 6.0, 7.65), (7.8, 0.5, 0.32)), ("MulV", (0, 6.15, 5.2), (0.16, 0.16, 4.8)), ("MulH", (0, 6.15, 5.3), (7.4, 0.16, 0.16))):
        L.cube(nm, 1, loc, sc, sunny if nm.startswith("Fr") else white, bevel=0.05)
    # gingham curtains + rod
    ging = _gingham(L, "Gingham", "#ff6f91")
    L.cylinder("Rod", 0.06, 9.4, (0, 5.6, 8.1), m=sunny, rot=(0, math.pi / 2, 0), verts=12)
    for sx in (-1, 1):
        c = L.cube("Curtain", 1, (4.35 * sx, 5.55, 5.9), (1.3, 0.12, 4.4), ging, bevel=0.05)
        sim = c.modifiers.new("Wave", "WAVE"); sim.use_normal = False; sim.height = 0.08; sim.width = 0.35; sim.speed = 0
        L.torus("Tie", 0.5, 0.06, (4.35 * sx, 5.55, 4.6), (1.1, 0.4, 0.3), sunny)
    # upper cabinets (mint) with gold knobs, open shelf with jars
    mint = L.mat("Cabinet", "#74d8bf", 0.35, coat=0.5)
    mintdk = L.mat("CabinetDoor", "#5cc9ad", 0.35, coat=0.5)
    gold = L.mat("Knob", "#ffc93c", 0.2, metal=0.6, coat=0.6)
    for sx in (-1, 1):
        cx = 9.0 * sx
        L.cube("Cab", 1, (cx, 5.7, 7.6), (9.6, 1.0, 3.0), mint, bevel=0.08)
        for k in range(3):
            dx = cx + (k - 1) * 3.05
            L.cube("Door", 1, (dx, 5.17, 7.6), (2.7, 0.08, 2.6), mintdk, bevel=0.06)
            L.sphere("KnobS", 0.12, (dx + 1.0 * (1 if k % 2 else -1), 5.08, 6.8), m=gold, segs=16)
        L.cube("Shelf", 1, (cx, 5.6, 4.6), (9.6, 0.9, 0.16), white, bevel=0.04)
    jarc = ("#ff7aa2", "#ffd23f", "#7ad3ff", "#b388ff", "#ff9e4a", "#7ee08a")
    for k, x in enumerate((-12.5, -11.3, -10.2, -8.9, -7.7, -6.3, 6.4, 7.8, 9.0, 10.3, 11.6, 12.8)):
        h = 0.6 + 0.35 * ((k * 7) % 3)
        jm = L.mat(f"Jar{k % 6}", jarc[k % 6], 0.25, coat=0.8, sss=0.1)
        L.cylinder("Jar", 0.36, h, (x, 5.55, 4.68 + h / 2), m=jm, verts=24)
        L.cylinder("JarLid", 0.39, 0.12, (x, 5.55, 4.68 + h + 0.06), m=white, verts=24)
    # herbs in terracotta pots on the sill
    terra = L.mat("Terracotta", "#e07a4f", 0.6, sss=0.05)
    herb = L.mat("Herb", "#43b649", 0.5, sss=0.2, bump=0.3, bump_scale=8)
    for k, x in enumerate((-3.0, 3.0)):
        L.cone("Pot", 0.3, 0.4, 0.5, (x, 5.6, 3.17), m=terra, verts=24)
        for j, (dx, dz, r) in enumerate(((0, 0.62, 0.3), (-0.2, 0.52, 0.23), (0.22, 0.54, 0.24), (0.04, 0.85, 0.22))):
            L.sphere("Basil", r, (x + dx, 5.6, 3.17 + dz - 0.2), m=herb, segs=20)
    _shift(bpy, before, -0.6)
    before = set(bpy.data.objects)

    # ---------------------------------------------------------------- garden outside the window
    grass = L.mat("Grass", "#6cc24a", 0.8, sheen=0.5, bump=0.3, bump_scale=30)
    L.cube("Garden", 1, (0, 40, 0.5), (120, 66, 3), grass)        # top at z=2.0
    hill = L.mat("Hill", "#8ad35a", 0.8, sheen=0.4)
    hill2 = L.mat("Hill2", "#5fb848", 0.8, sheen=0.4)
    for k, (x, y, r) in enumerate(((-14, 60, 11), (6, 66, 13), (22, 58, 10), (-30, 66, 14))):
        L.sphere("HillS", r, (x, y, -r * 0.55), (1.4, 1, 1), hill if k % 2 else hill2, segs=32)
    bark = L.mat("Bark", "#8a5a3a", 0.85)
    leafm = [L.mat("TreeLeaf0", "#4fbf4f", 0.6, sss=0.1, bump=0.2, bump_scale=4), L.mat("TreeLeaf1", "#3faa48", 0.6, sss=0.1, bump=0.2, bump_scale=4)]
    for k, (x, y, s) in enumerate(((-9, 30, 2.2), (7, 34, 2.6), (-1.5, 44, 3.0), (15, 28, 2.0))):
        L.cylinder("Trunk", 0.3 * s, 2.4 * s, (x, y, 2 + 1.2 * s), m=bark, verts=12)
        for dx, dz, r in ((0, 3.0, 1.4), (0.9, 2.6, 0.95), (-0.9, 2.7, 1.0)):
            L.sphere("Crown", r * s, (x + dx * s, y, 2 + dz * s), m=leafm[k % 2], segs=20)
        if k % 2 == 0:
            red = L.mat("ApplesOnTree", "#ff3b3b", 0.3, coat=0.6)
            for dx, dz in ((0.6, 3.2), (-0.7, 2.8), (0.1, 2.4), (1.1, 2.7)):
                L.sphere("TreeApple", 0.2 * s, (x + dx * s, y - 1.3 * s, 2 + dz * s), m=red, segs=12)
    # picket fence: one picket + array modifier
    fence = L.mat("Fence", "#ffffff", 0.5)
    pk = L.cube("Picket", 1, (-14, 16, 2.9), (0.35, 0.12, 1.8), fence, bevel=0.04)
    ar = pk.modifiers.new("Arr", "ARRAY"); ar.count = 40; ar.relative_offset_displace = (2.0, 0, 0)
    for z in (2.5, 3.3):
        L.cube("Rail", 1, (0, 16.1, z), (30, 0.1, 0.18), fence)
    # sunflowers + raised veggie bed
    stemm = L.mat("FlowerStem", "#3d9a3d", 0.6)
    pet = L.mat("SunPetal", "#ffd21f", 0.45, sss=0.2)
    ctr = L.mat("SunCenter", "#7a4a1e", 0.8, bump=0.4, bump_scale=40)
    A["flowers"] = []
    for k, (x, y, h) in enumerate(((-6.2, 11, 3.6), (-4.6, 12.5, 4.2), (5.0, 11.5, 3.9), (6.6, 13, 3.3), (1.8, 13.5, 3.0))):
        piv = L.empty("SunflowerPiv", (x, y, 2.0))
        L.cylinder("SFStem", 0.08, h, (0, 0, h / 2), m=stemm, parent=piv, verts=10)
        head = L.empty("SFHead", (0, -0.1, h), piv); head.rotation_euler = (math.radians(70), 0, 0)
        L.cylinder("SFPetals", 0.85, 0.06, (0, 0, 0), m=pet, parent=head, verts=14)
        L.sphere("SFCenter", 0.48, (0, 0, 0.05), (1, 1, 0.35), ctr, head, 20)
        A["flowers"].append((piv, k))
    bedw = _wood(L, "BedWood", "#c98b58", "#a86d42", 2.0)
    L.cube("Bed", 1, (0, 9.5, 2.3), (9, 2.2, 0.7), bedw, bevel=0.06)
    soil = L.mat("Soil", "#6b4428", 0.95, bump=0.5, bump_scale=20)
    L.cube("BedSoil", 1, (0, 9.5, 2.62), (8.6, 1.9, 0.1), soil)
    lettuce = L.mat("Lettuce", "#9be15d", 0.5, sss=0.25, bump=0.4, bump_scale=6)
    tomato = L.mat("Tomato", "#ff3d2e", 0.25, coat=0.8)
    for k in range(7):
        x = -3.6 + k * 1.2
        if k % 2:
            L.sphere("LettuceS", 0.5, (x, 9.3, 2.85), (1, 1, 0.7), lettuce, segs=20)
        else:
            L.cylinder("TomStake", 0.04, 1.6, (x, 9.7, 3.4), m=stemm, verts=8)
            L.sphere("TomBush", 0.45, (x, 9.7, 3.3), m=leafm[0], segs=16)
            for dz in (0.1, 0.55):
                L.sphere("TomatoS", 0.17, (x + 0.2, 9.3, 3.1 + dz), m=tomato, segs=14)
    # window box with flowers just outside the sill
    L.cube("WinBox", 1, (0, 6.75, 2.95), (6.4, 0.6, 0.5), sunny, bevel=0.05)
    fl = [L.mat(f"WBFlower{k}", c, 0.4, sss=0.2) for k, c in enumerate(("#ff5c8a", "#ffffff", "#ff9f43", "#b57cff"))]
    for k in range(9):
        L.sphere("WBF", 0.22, (-2.8 + k * 0.7, 6.75, 3.35 + 0.08 * (k % 2)), m=fl[k % 4], segs=12)
        L.sphere("WBLeaf", 0.24, (-2.45 + k * 0.7, 6.8, 3.2), m=leafm[1], segs=12)
    # clouds
    cloud = L.mat("Cloud", "#ffffff", 0.9, sss=0.3, emission="#ffffff", emit=0.2)
    A["clouds"] = []
    for k, (x, y, z) in enumerate(((-8, 50, 16), (9, 56, 18), (-1, 62, 21))):
        c = L.empty("CloudE", (x, y, z))
        for dx, dz, r in ((0, 0, 2.2), (2.2, -0.4, 1.6), (-2.1, -0.5, 1.5), (0.9, 1.0, 1.4)):
            L.sphere("CloudS", r, (dx, 0, dz), (1, 0.7, 0.8), cloud, c, 20)
        A["clouds"].append((c, x))
    # butterflies in the garden
    wingm = [L.mat("Wing0", "#ff7ac0", 0.4, sss=0.3), L.mat("Wing1", "#5cc8ff", 0.4, sss=0.3)]
    A["bflies"] = []
    for k in range(2):
        bf = L.empty("Butterfly", (0, 9, 4))
        ws = []
        for sx in (-1, 1):
            w = L.empty("BWing", (0, 0, 0), bf)
            L.sphere("BWingS", 0.32, (0.3 * sx, 0, 0.05), (1, 0.15, 0.8), wingm[k], w, 16)
            ws.append((w, sx))
        A["bflies"].append((bf, ws, k))

    _shift(bpy, before, -0.7)
    # ---------------------------------------------------------------- counter dressing
    # fruit bowl, back left
    ceramic = L.mat("BowlCeramic", "#5bc6e8", 0.2, coat=0.9)
    _bowl_mesh(L, "FruitBowl", 1.0, ceramic, loc=(-6.0, 3.4, 0.62), scale=(1.5, 1.3, 0.62))
    L.cylinder("BowlFoot", 0.5, 0.12, (-6.0, 3.4, 0.06), m=ceramic, verts=24)
    red = L.mat("BowlApple", "#ef2b2b", 0.22, coat=0.9, sss=0.1)
    org = L.mat("BowlOrange", "#ff9416", 0.38, coat=0.5, bump=0.25, bump_scale=70)
    grp = L.mat("BowlGrape", "#8e3fd0", 0.18, coat=1.0, sss=0.3)
    yel = L.mat("BowlBanana", "#ffd83a", 0.42, coat=0.35)
    for x, y, z, m_ in ((-6.6, 3.3, 1.05, red), (-5.4, 3.5, 1.1, org), (-6.0, 3.9, 1.35, red), (-5.0, 3.0, 0.95, red)):
        L.sphere("BowlFruit", 0.5 if m_ is org else 0.46, (x, y, z), m=m_, segs=24)
    import importlib
    fr = importlib.import_module("chars.fruit")
    ban = L.sphere("BowlBanana", 1.0, (-6.1, 2.95, 1.2), (0.6, 0.6, 0.6), yel, None, 32, (math.radians(-10), math.radians(80), math.radians(15)))
    for v in ban.data.vertices: v.co = fr._banana(*v.co)
    for k in range(7):
        a = k * 2.4
        L.sphere("BowlGrape", 0.17, (-6.9 + math.cos(a) * 0.2, 3.8 + math.sin(a) * 0.2, 1.2 + 0.08 * k), m=grp, segs=12)
    # cutting board with veggies (no knife), back right
    board = _wood(L, "BoardWood", "#e9b77c", "#cf9358", 3.0)
    L.cube("Board", 1, (5.8, 3.3, 0.09), (3.4, 2.0, 0.18), board, bevel=0.08)
    L.cylinder("BoardHandle", 0.28, 0.18, (7.65, 3.3, 0.09), m=board, verts=20)
    orng = L.mat("CarrotSlice", "#ff8418", 0.4, sss=0.2)
    cuc = L.mat("Cucumber", "#7ed957", 0.35, sss=0.2)
    for k in range(4):
        L.cylinder("Slice", 0.24, 0.1, (5.0 + k * 0.42, 2.9, 0.23), m=orng, verts=20)
        L.cylinder("Cuc", 0.27, 0.1, (5.2 + k * 0.42, 3.6, 0.23), m=cuc, verts=20)
    L.sphere("CherryTom", 0.26, (6.9, 3.0, 0.42), m=tomato, segs=20)
    L.sphere("CherryTom", 0.24, (6.6, 3.7, 0.40), m=tomato, segs=20)
    # canisters + teapot at the far ends
    pink = L.mat("CanPink", "#ff8fb1", 0.25, coat=0.8)
    for k, (x, h) in enumerate(((-11.6, 2.2), (-10.2, 1.7))):
        L.cylinder("Canister", 0.62, h, (x, 4.6, h / 2), m=pink if k == 0 else ceramic, verts=28)
        L.sphere("CanLid", 0.62, (x, 4.6, h), (1, 1, 0.35), white, segs=24)
    tea = L.mat("Teapot", "#ffd23f", 0.2, coat=0.9)
    L.sphere("Teapot", 1.0, (10.6, 4.2, 1.0), (1.1, 1.0, 0.95), tea, segs=32)
    L.cone("Spout", 0.22, 0.1, 1.1, (9.3, 4.2, 1.2), m=tea, rot=(0, math.radians(-55), 0), verts=16)
    L.torus("Handle", 0.5, 0.1, (11.75, 4.2, 1.1), m=tea, rot=(math.pi / 2, 0, 0))
    L.sphere("TeaLid", 0.3, (10.6, 4.2, 1.95), (1, 1, 0.6), white, segs=16)
    # midground sprinkles for depth: blueberries, cherries, a gingham napkin
    blue = L.mat("Blueberry", "#3f51b5", 0.3, coat=0.7, sheen=0.4)
    for k, (x, y) in enumerate(((-1.9, -2.6), (-2.3, -2.3), (-1.6, -2.15), (-2.0, -1.9), (-2.5, -2.75))):
        L.sphere("Blueb", 0.2, (x, y, 0.19), (1, 1, 0.9), blue, segs=16)
    L.cube("Napkin", 1, (1.9, -2.5, 0.02), (1.8, 1.8, 0.04), _gingham(L, "GinghamB", "#4fc3f7"), rot=(0, 0, 0.3))
    cher = L.mat("Cherry", "#d81b3a", 0.15, coat=1.0, sss=0.1)
    for dx in (-0.25, 0.25):
        L.sphere("CherryS", 0.26, (1.9 + dx, -2.5, 0.3), m=cher, segs=20)
        L.cylinder("CherryStem", 0.025, 0.6, (1.9 + dx * 0.5, -2.5, 0.75), m=stemm, rot=(0, -dx * 1.2, 0), verts=8)

    for o in noshadow:
        try: o.visible_shadow = False
        except Exception: pass
    return {
        "spots": {"center": (0, 0, 0), "left": (-2.5, 0.5, 0), "right": (2.5, 0.5, 0),
                  "farleft": (-4.5, 1.5, 0), "farright": (4.5, 1.5, 0), "back": (0, 2.2, 0)},
        "cams": {"wide": ((0.5, -10.4, 2.9), (0, 0.8, 1.55)), "center": (0, 0.5, 1.3), "orbit_r": 9.5,
                 "bowl": ((-3.6, -3.0, 2.2), (-6.0, 3.4, 1.0)), "garden": ((0.4, -3.0, 3.8), (0, 9, 4.0)),
                 "board": ((3.8, -1.6, 2.4), (5.8, 3.3, 0.4))},
        "prop_spots": {"top": (0, 0.8, 3.75), "left": (-3.9, 0.3, 3.0), "right": (3.9, 0.3, 3.0), "front": (0, -2.4, 0.9)},
        "exposure": -0.45, "look": "AgX - Punchy", "_anim": A,
    }


def animate(L, SET, f, t, s):
    A = SET.get("_anim", {})
    e = s.get("energy", 0.5); beat = s.get("beat", 0)
    for piv, k in A.get("flowers", []):
        piv.rotation_euler = (math.sin(t * 1.3 + k) * 0.04, math.sin(t * 1.7 + k * 1.3) * 0.05 + math.sin(beat * math.tau) * 0.03 * e, 0)
    for c, x in A.get("clouds", []):
        c.location.x = x + math.sin(t * 0.05) * 3 + t * 0.03
    for bf, ws, k in A.get("bflies", []):
        a = t * (0.5 + 0.15 * k) + k * 3
        bf.location = (math.sin(a) * 3.2 + (1.5 if k else -1.5), 8.8 + math.cos(a * 0.7), 3.9 + math.sin(a * 2.3) * 0.5 + k * 0.6)
        bf.rotation_euler = (0, 0, math.cos(a) * 0.8)
        for w, sx in ws:
            w.rotation_euler = (0, sx * math.sin(t * 22 + k) * 0.8, 0)


# ------------------------------------------------------------------ teaching props
def prop(L, name, at, **opts):
    import importlib
    root = L.empty("Prop_" + name, at)
    white = L.mat("PropWhite", "#ffffff", 0.25, coat=0.6)
    if name == "water_drop":
        root.scale = (0.72,) * 3
        m = _glass(L, "WaterDrop", "#3db7ff")
        o = L.sphere("Drop", 0.55, (0, 0, 0), m=m, parent=root, segs=40)
        for v in o.data.vertices:
            z = v.co.z / 0.55
            if z > 0:
                k = max(0.0, 1 - z) ** 1.6
                v.co.x *= k; v.co.y *= k; v.co.z *= 1.9
        L.sphere("DropCore", 0.4, (0, 0.05, -0.05), m=L.mat("DropBlue", "#2aa8ff", 0.1, coat=1.0, sss=0.4), parent=root, segs=24)
        L.sphere("DropShine", 0.09, (-0.2, -0.45, 0.2), (1, 0.5, 1.6), L.mat("Shine", "#ffffff", 0.0, emission="#ffffff", emit=3), root, 12)
    elif name == "bubbles":
        m = _glass(L, "Bubble", "#e8f7ff", film=True)
        for k, (x, y, z, r) in enumerate(((0, 0, 0, 0.55), (0.8, 0.2, 0.5, 0.35), (-0.75, 0.1, 0.4, 0.4), (0.3, -0.1, 0.95, 0.25),
                                           (-0.35, 0.2, -0.6, 0.3), (1.1, 0.0, -0.35, 0.22), (-1.1, 0.3, 1.0, 0.2))):
            L.sphere("Bub", r, (x, y, z), m=m, parent=root, segs=24)
            L.sphere("BubShine", r * 0.18, (x - r * 0.4, y - r * 0.85, z + r * 0.4), m=L.mat("Shine", "#ffffff", 0.0, emission="#ffffff", emit=3), parent=root, segs=8)
    elif name == "plate":
        tilt = L.empty("PlateTilt", (0, 0, 0), root); tilt.rotation_euler = (math.radians(62), 0, 0)
        L.cylinder("Plate", 1.0, 0.08, (0, 0, 0), m=white, parent=tilt, verts=40)
        L.torus("PlateRim", 0.95, 0.07, (0, 0, 0.05), m=white, parent=tilt)
        foods = (("#ff3d2e", 0.22, (-0.45, 0.25)), ("#ff8418", 0.18, (0.0, 0.5)), ("#ffd21f", 0.2, (0.45, 0.25)),
                 ("#3aa84c", 0.24, (0.4, -0.3)), ("#3f51b5", 0.15, (-0.05, -0.45)), ("#8e3fd0", 0.17, (-0.45, -0.25)))
        for k, (c, r, (x, y)) in enumerate(foods):
            m = L.mat(f"PlateFood{k}", c, 0.3, coat=0.7, sss=0.1, bump=0.5 if k == 3 else 0, bump_scale=25)
            for j in range(2):
                L.sphere("Food", r, (x + j * r * 0.9, y + j * r * 0.4, 0.1 + r * 0.6), m=m, parent=tilt, segs=16)
    elif name == "basket":
        weave = L.mat("Weave", "#c98a4b", 0.75, bump=0.8, bump_scale=14)
        L.cylinder("Basket", 0.8, 0.8, (0, 0, -0.2), (1, 0.75, 1), weave, root, verts=32)
        L.torus("BasketRim", 0.8, 0.09, (0, 0, 0.2), (1, 0.75, 1), weave, root)
        L.torus("BasketHandle", 0.75, 0.06, (0, 0, 0.2), m=weave, parent=root, rot=(math.pi / 2, 0, 0))
        for k, (x, y, z, c) in enumerate(((-0.35, -0.1, 0.3, "#ef2b2b"), (0.3, -0.15, 0.32, "#ff9416"), (0, 0.15, 0.42, "#ffd83a"), (0.45, 0.15, 0.25, "#3aa84c"), (-0.4, 0.2, 0.28, "#8e3fd0"))):
            L.sphere("BasketFruit", 0.27, (x, y, z), m=L.mat(f"BF{k}", c, 0.25, coat=0.8, sss=0.1), parent=root, segs=20)
    elif name == "number":
        col = opts.get("color", "#ff5c8a")
        disc = L.empty("Sign", (0, 0, 0), root); disc.rotation_euler = (math.pi / 2, 0, 0)
        L.cylinder("SignDisc", 0.75, 0.16, (0, 0, 0), m=white, parent=disc, verts=40)
        L.torus("SignRing", 0.75, 0.1, (0, 0, 0), m=L.mat("Ring" + col, col, 0.25, coat=0.8), parent=disc)
        L.text3d("SignNum", str(opts.get("text", "1")), opts.get("size", 0.85 if len(str(opts.get("text", "1"))) < 3 else 0.55), (0, -0.14, 0),
                 L.mat("Num" + col, col, 0.25, coat=0.7, emission=col, emit=0.2), root, extrude=0.1, bevel=0.025)
    elif name == "bigfruit":
        fr = importlib.import_module("chars.fruit")
        kind = opts.get("kind", "apple")
        fn, hexcol = fr.KINDS.get(kind, fr.KINDS["apple"])[:2]
        skin = fr._skin(L, kind, hexcol)
        body, bvh, top = fr._body(L, "BigFruit", fn, skin, root)
        body.location = (0, 0, -top / 2)
        leaf = L.mat("FrLeaf", "#34b548", 0.38, coat=0.4, sss=0.15)
        if kind == "carrot":
            for k, a in enumerate((-0.4, 0, 0.4)):
                L.sphere("BFTop", 1.0, (math.sin(a) * 0.25, 0, top / 2 + 0.25), (0.09, 0.07, 0.35), leaf, root, 16, (0, a, 0))
        elif kind == "broccoli":
            flo = L.mat("FrFloret", "#2e9440", 0.6, sheen=0.4, sss=0.08, bump=0.7, bump_scale=26)
            for x, z, r in ((0, 0.55, 0.55), (-0.45, 0.35, 0.4), (0.45, 0.35, 0.4)):
                L.sphere("BFFlo", r, (x, 0, top / 2 + z - 0.2), m=flo, parent=root, segs=24)
        else:
            L.cylinder("BFStem", 0.05, 0.35, (0.03, 0, top / 2 + 0.05), m=L.mat("FrStem", "#7a4a26", 0.6), parent=root, rot=(0, 0.2, 0), verts=10)
            L.sphere("BFLeaf", 1.0, (0.24, 0, top / 2 + 0.12), (0.26, 0.12, 0.05), leaf, root, 20, (0.2, -0.5, 0.2))
        L.sphere("BFShine", 0.1, (-0.3, -0.75, 0.25), (1, 0.4, 1.4), L.mat("Shine", "#ffffff", 0.0, emission="#ffffff", emit=3), root, 10)
    elif name == "rainbow":
        for k, c in enumerate(("#ff3d3d", "#ff9416", "#ffd21f", "#3cc45a", "#3f8cff", "#8e3fd0")):
            arc = L.torus("Arc", 1.5 - k * 0.17, 0.09, (0, 0, -0.6), m=L.mat(f"Rb{k}", c, 0.3, coat=0.6, emission=c, emit=0.15), parent=root, rot=(math.pi / 2, 0, 0))
            bm = bmesh.new(); bm.from_mesh(arc.data)
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y < -0.02], context="VERTS")
            bm.to_mesh(arc.data); bm.free()
        cl = L.mat("Cloud", "#ffffff", 0.9, sss=0.3, emission="#ffffff", emit=0.2)
        for sx in (-1, 1):
            for dx, dz, r in ((0, 0, 0.38), (0.32 * sx, -0.08, 0.28), (-0.3 * sx, -0.1, 0.26)):
                L.sphere("RbCloud", r, (1.32 * sx + dx, -0.05, -0.6 + dz), m=cl, parent=root, segs=16)
    elif name == "floatbowl":
        root.scale = (0.62,) * 3
        g = _glass(L, "BowlGlass", "#e6f6ff")
        _bowl_mesh(L, "GlassBowl", 0.9, g, root, (0, 0, 0), (1.2, 1.0, 0.75), cut=0.35)
        L.cylinder("Water", 0.98, 0.5, (0, 0, -0.2), (1.2, 1.0, 1), L.mat("WaterBlue", "#59c3ff", 0.05, coat=1.0, sss=0.3, alpha=0.75), root, verts=36)
        L.sphere("FloatApple", 0.38, (0, -0.1, 0.12), (1, 1, 0.9), L.mat("FrSkin_apple#e3262b", "#e3262b", 0.22, coat=0.9, sss=0.1), root, 24)
        L.cylinder("FloatStem", 0.03, 0.2, (0.02, -0.1, 0.5), m=L.mat("FrStem", "#7a4a26", 0.6), parent=root, verts=8)
    elif name == "carrot_ground":
        soil = L.mat("Soil", "#6b4428", 0.95, bump=0.5, bump_scale=20)
        L.sphere("Mound", 0.9, (0, 0, -0.55), (1.3, 1.0, 0.6), soil, root, 32)
        L.cone("CarrotTop", 0.22, 0.26, 0.2, (0, -0.05, -0.08), m=L.mat("FrSkin_carrot#ff8418", "#ff8418", 0.42, coat=0.35, sss=0.1), parent=root, verts=20)
        leaf = L.mat("FrLeaf", "#34b548", 0.38, coat=0.4, sss=0.15)
        for k, a in enumerate((-0.5, -0.15, 0.2, 0.55)):
            L.sphere("CGTop", 1.0, (math.sin(a) * 0.22, -0.05, 0.3), (0.08, 0.06, 0.38), leaf, root, 16, (0, a, 0))
        arrow = L.mat("Arrow", "#ffd21f", 0.3, coat=0.6, emission="#ffd21f", emit=0.2)
        L.cube("CGArrow", 1, (1.0, -0.1, 0.75), (0.12, 0.08, 0.5), arrow, root, bevel=0.03)
        L.cone("CGArrowHead", 0.22, 0.0, 0.3, (1.0, -0.1, 0.35), m=arrow, parent=root, rot=(math.pi, 0, 0), verts=16)
    elif name == "banana_hand":
        fr = importlib.import_module("chars.fruit")
        yel = L.mat("FrSkin_banana#ffd83a", "#ffd83a", 0.42, coat=0.35, sss=0.12)
        st = L.mat("FrStem", "#7a4a26", 0.6)
        L.cylinder("HandStem", 0.1, 0.45, (0, 0.05, 0.75), m=L.mat("FrBanStem", "#8a7a2a", 0.55), parent=root, verts=12)
        for k in range(5):
            a = (k - 2) * 0.38
            arm = L.empty("Finger", (0, 0.04 * abs(k - 2), 0.55), root); arm.rotation_euler = (0, a, 0)
            b = L.sphere("Banana", 1.0, (0, 0, -0.5), (0.5, 0.5, 0.5), yel, arm, 32, (0, 0, math.pi))
            for v in b.data.vertices: v.co = fr._banana(*v.co)
            L.sphere("BTip", 0.05, (0.0, 0, -0.98), m=st, parent=arm, segs=8)
    elif name == "tree":
        bark = L.mat("Bark", "#8a5a3a", 0.85)
        L.cylinder("PTrunk", 0.16, 1.0, (0, 0, -0.4), m=bark, parent=root, verts=12)
        lf = L.mat("TreeLeaf0", "#4fbf4f", 0.6, sss=0.1, bump=0.2, bump_scale=4)
        for dx, dz, r in ((0, 0.45, 0.62), (0.5, 0.2, 0.45), (-0.5, 0.22, 0.47), (0, 0.9, 0.42)):
            L.sphere("PCrown", r, (dx, 0, dz), m=lf, parent=root, segs=20)
    elif name == "magnifier":
        rim = L.mat("MagRim", "#ff5c8a", 0.25, coat=0.8)
        L.torus("MagRing", 0.6, 0.08, (0, 0, 0), m=rim, parent=root, rot=(math.pi / 2, 0, 0))
        L.cylinder("MagGlass", 0.6, 0.04, (0, 0, 0), m=_glass(L, "MagGlassM", "#eefaff"), parent=root, rot=(math.pi / 2, 0, 0), verts=32)
        L.cylinder("MagHandle", 0.09, 0.8, (0.62, 0, -0.62), m=rim, parent=root, rot=(0, math.radians(-45), 0), verts=16)
        L.sphere("MagSeed", 1.0, (0, 0.15, 0), (0.18, 0.05, 0.26), L.mat("SeedBig", "#ffe27a", 0.3, coat=0.6), root, 16)
    elif name == "heart":
        m = L.mat("Heart", "#ff3d6e", 0.2, coat=0.9, sss=0.15, emission="#ff3d6e", emit=0.15)
        for sx in (-1, 1):
            L.sphere("HeartLobe", 0.42, (0.3 * sx, 0, 0.15), (1, 0.6, 1), m, root, 32)
        L.cone("HeartTip", 0.62, 0.02, 0.85, (0, 0, -0.38), (1, 0.6, 1), m, root, (math.pi, 0, 0), verts=32)
    elif name == "star":
        _star_mesh(L, "Star", 0.7, L.mat("StarGold", "#ffd21f", 0.2, coat=0.8, emission="#ffd21f", emit=0.4), root)
    elif name == "sun":
        m = L.mat("SunProp", "#ffd21f", 0.3, coat=0.5, emission="#ffb300", emit=0.8)
        L.sphere("SunBall", 0.55, (0, 0, 0), (1, 0.6, 1), m, root, 32)
        for k in range(10):
            a = k / 10 * math.tau
            L.cone("Ray", 0.12, 0.0, 0.35, (math.cos(a) * 0.8, 0, math.sin(a) * 0.8), m=m, parent=root, rot=(0, -a + math.pi / 2, 0), verts=12)
    else:
        L.text3d("PropName", name.upper(), 0.6, (0, 0, 0), L.mat("PropDefault", "#ff5c8a", 0.3, coat=0.6), root)
    return root
