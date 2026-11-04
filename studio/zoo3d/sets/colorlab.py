"""Bloop's Color Lab: a candy-bright color lab with a rainbow wall, jar shelves, giant crayons, bubbling beakers,
paint buckets and a polka-dot floor. See API.md."""
import math

RAINBOW = ["#ff4b4b", "#ff9a2e", "#ffd426", "#4cd964", "#3d8bff", "#9d5cff"]
CANDY = ["#ff5c8a", "#ff9a2e", "#ffd426", "#4cd964", "#3db8ff", "#9d6bff"]
COLOR_WORDS = {"red": "#ff3b3b", "orange": "#ff8a1f", "yellow": "#ffd21f", "green": "#3ccf4e", "blue": "#2f7bff",
               "purple": "#9d5cff", "pink": "#ff6fb5", "white": "#ffffff", "brown": "#8b5a2b", "black": "#2b2b38"}


def _hex(c):
    return COLOR_WORDS.get(c, c) if isinstance(c, str) else c


def _input(m, key, val):
    b = m.node_tree.nodes["Principled BSDF"]
    if key in b.inputs: b.inputs[key].default_value = val


def glass(L, name="LabGlass"):
    m = L.mat(name, "#eaf6ff", 0.04, coat=0.5)
    _input(m, "Transmission Weight", 1.0); _input(m, "IOR", 1.2)
    try: m.surface_render_method = "BLENDED"
    except Exception: pass
    return m


def candy(L, hexc, rough=0.25):
    return L.mat("Candy" + hexc, hexc, rough, coat=0.9, sss=0.05)


def polka_floor(L, sx=44, sy=34):
    import bpy
    m = bpy.data.materials.new("PolkaFloor"); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.32
    if "Coat Weight" in b.inputs: b.inputs["Coat Weight"].default_value = 0.6
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (sx * 0.95, sy * 0.95, 1)
    vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.voronoi_dimensions = "2D"; vo.inputs["Randomness"].default_value = 0.0; vo.inputs["Scale"].default_value = 1.0
    lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 0.24
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.interpolation = "CONSTANT"
    els = ramp.color_ramp.elements
    while len(els) < len(CANDY): els.new(0.5)
    for k, h in enumerate(CANDY):
        els[k].position = k / len(CANDY); els[k].color = (*L.rgb(h), 1)
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    mix.inputs[6].default_value = (*L.rgb("#fff3fa"), 1)
    L_ = nt.links
    L_.new(tc.outputs["Object"], mp.inputs["Vector"]); L_.new(mp.outputs["Vector"], vo.inputs["Vector"])
    L_.new(vo.outputs["Distance"], lt.inputs[0]); L_.new(vo.outputs["Color"], sep.inputs["Color"])
    L_.new(sep.outputs[0], ramp.inputs["Fac"])
    L_.new(lt.outputs[0], mix.inputs[0]); L_.new(ramp.outputs["Color"], mix.inputs[7])
    L_.new(mix.outputs[2], b.inputs["Base Color"])
    return m


def stripe_wall(L, name, a, b_, scale=1.6, axis=0):
    import bpy
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.6
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mm = nt.nodes.new("ShaderNodeMath"); mm.operation = "MULTIPLY"; mm.inputs[1].default_value = scale
    fr = nt.nodes.new("ShaderNodeMath"); fr.operation = "FRACT"
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.5
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    mix.inputs[6].default_value = (*L.rgb(a), 1); mix.inputs[7].default_value = (*L.rgb(b_), 1)
    l = nt.links
    l.new(tc.outputs["Object"], sep.inputs[0]); l.new(sep.outputs[axis], mm.inputs[0]); l.new(mm.outputs[0], fr.inputs[0])
    l.new(fr.outputs[0], gt.inputs[0]); l.new(gt.outputs[0], mix.inputs[0]); l.new(mix.outputs[2], b.inputs["Base Color"])
    return m


def build(L, rng, **_):
    L.sky(color_hex="#ffe6f5", strength=0.45, nishita=False)
    L.light("Sun", "SUN", 2.6, rot=(math.radians(52), 0, math.radians(-25)), color=(1, 0.95, 0.88), angle=math.radians(10))
    L.light("Key", "AREA", 650, (-4, -9, 7), (math.radians(55), 0, math.radians(-22)), (1, 0.95, 0.9), 9)
    L.light("Fill", "AREA", 300, (6, -7, 3), (math.radians(70), 0, math.radians(40)), (0.92, 0.95, 1), 7)
    L.light("Rim", "AREA", 700, (0, 5, 6), (math.radians(-55), 0, 0), (1, 0.85, 0.95), 8)
    pink = L.light("GlowPink", "POINT", 220, (-6, 5.5, 3.5), color=(1, 0.45, 0.75), size=1.0)
    cyan = L.light("GlowCyan", "POINT", 220, (6, 5.5, 3.5), color=(0.4, 0.8, 1), size=1.0)

    # room
    L.cube("Floor", 1, (0, 4, -0.5), (44, 34, 1), polka_floor(L))
    L.cube("BackWall", 1, (0, 9.2, 6), (34, 0.4, 12), stripe_wall(L, "WallStripes", "#ffd3ea", "#fff0f8", 34 / 1.3))
    side = stripe_wall(L, "SideStripes", "#d9d0ff", "#efeaff", 14 / 1.3, 1)
    for sx in (-1, 1):
        L.cube("SideWall", 1, (sx * 10.5, 2.5, 6), (0.4, 14, 12), side, rot=(0, 0, sx * 0.32))
    L.cube("Baseboard", 1, (0, 8.95, 0.25), (34, 0.2, 0.5), L.mat("Baseboard", "#b9f2e6", 0.4, coat=0.5), bevel=0.05)

    # rainbow arch with clouds
    for k, h in enumerate(RAINBOW):
        L.torus(f"Rainbow{k}", 5.0 - k * 0.42, 0.21, (0, 8.75, 0.2), (1, 0.6, 1), L.mat(f"Rain{h}", h, 0.3, coat=0.8, emission=h, emit=0.15), rot=(math.pi / 2, 0, 0))
    cloud = L.mat("Cloud", "#ffffff", 0.6, sheen=0.6, sss=0.1)
    for sx in (-1, 1):
        for dx, dz, r in ((0, 0.55, 0.75), (0.65, 0.4, 0.55), (-0.65, 0.35, 0.55), (0.2, 1.05, 0.5)):
            L.sphere("Cloud", r, (sx * 3.95 + dx, 8.3, dz), (1, 0.7, 0.85), cloud, segs=24)
    L.text3d("Sign", "BLOOP'S COLOR LAB", 0.72, (0, 8.85, 6.1), L.mat("SignInk", "#9d6bff", 0.3, coat=0.8, emission="#9d6bff", emit=0.2), extrude=0.1)

    # jar shelves on the back wall
    board = L.mat("Shelf", "#ffffff", 0.35, coat=0.6)
    lid = L.mat("JarLid", "#ffffff", 0.3, coat=0.8)
    for sx in (-1, 1):
        for row, z in enumerate((1.6, 3.0, 4.4)):
            L.cube("ShelfBoard", 1, (sx * 7.6, 8.55, z), (3.4, 0.9, 0.12), board, bevel=0.04)
            for j in range(3):
                h = CANDY[(j + row * 2 + (sx > 0) * 3) % 6]
                x = sx * 7.6 + (j - 1) * 1.05
                hh = 0.75 + 0.15 * ((j + row) % 2)
                L.cylinder("Jar", 0.33, hh, (x, 8.5, z + 0.06 + hh / 2), (1, 1, 1), L.mat(f"Jar{h}", h, 0.15, coat=1.0, sss=0.4, emission=h, emit=0.2), verts=24)
                L.cylinder("JarLid", 0.36, 0.14, (x, 8.5, z + 0.12 + hh), (1, 1, 1), lid, verts=24)

    # lab table with bubbling beakers (left midground)
    tbl = L.mat("Table", "#7fd8ff", 0.35, coat=0.6)
    L.cube("TableTop", 1, (-5.4, 4.4, 1.25), (3.4, 1.5, 0.16), L.mat("TableTop", "#ffffff", 0.3, coat=0.7), bevel=0.06)
    for dx in (-1.5, 1.5):
        L.cube("TableLeg", 1, (-5.4 + dx, 4.4, 0.6), (0.18, 1.2, 1.2), tbl, bevel=0.05)
    gl = glass(L)
    bubbles = []
    for k, (dx, h) in enumerate(((-1.0, "#ff5c8a"), (0.0, "#4cd964"), (1.0, "#3db8ff"))):
        x = -5.4 + dx
        liq = L.mat(f"Liquid{h}", h, 0.1, coat=1, sss=0.3, emission=h, emit=0.6)
        if k == 1:
            L.sphere("Flask", 0.5, (x, 4.4, 1.8), (1, 1, 1), gl, segs=32)
            L.cylinder("FlaskNeck", 0.15, 0.6, (x, 4.4, 2.5), (1, 1, 1), gl, verts=20)
            L.sphere("FlaskLiq", 0.44, (x, 4.4, 1.76), (1, 1, 0.8), liq, segs=32)
        else:
            L.cylinder("Beaker", 0.36, 1.0, (x, 4.4, 1.83), (1, 1, 1), gl, verts=32)
            L.cylinder("BeakerLiq", 0.32, 0.62, (x, 4.4, 1.66), (1, 1, 1), liq, verts=32)
        bm = L.mat(f"Bubble{h}", h, 0.05, coat=1, emission=h, emit=1.0)
        for j in range(3):
            b = L.sphere("Bub", 0.07 + 0.03 * j, (x, 4.4, 2.3), m=bm, segs=12)
            bubbles.append((b, x, 2.1 + (0.4 if k == 1 else 0), j / 3 + k * 0.17))

    # giant crayons in a cup (right midground)
    cup = L.mat("CrayonCup", "#ff9ecb", 0.3, coat=0.8)
    L.cylinder("Cup", 0.85, 1.4, (5.6, 4.6, 0.7), (1, 1, 1), cup, verts=40)
    L.torus("CupRim", 0.85, 0.08, (5.6, 4.6, 1.4), m=cup)
    for k, h in enumerate(RAINBOW[:5]):
        a = (k - 2) * 0.22
        cm = L.mat(f"Crayon{h}", h, 0.45, sheen=0.3)
        piv = L.empty("CrayonPiv", (5.6 + (k - 2) * 0.28, 4.6 + (k % 2) * 0.2, 0.6))
        piv.rotation_euler = (0.06 * (k % 2 - 0.5), a, 0)
        L.cylinder("Crayon", 0.2, 2.6 + 0.2 * (k % 2), (0, 0, 1.3), (1, 1, 1), cm, piv, verts=16)
        L.cone("CrayonTip", 0.2, 0.05, 0.45, (0, 0, 2.85 + 0.1 * (k % 2)), (1, 1, 1), cm, piv, verts=16)
        L.cylinder("CrayonBand", 0.215, 0.12, (0, 0, 2.2), (1, 1, 1), L.mat("CrayonBand", "#2b2b38", 0.5), piv, verts=16)

    # paint buckets + spills (foreground corners)
    for k, (x, y, h, tip) in enumerate(((-7.2, -0.8, "#ff4b4b", 0), (-6.2, -1.9, "#ffd426", 0), (7.0, -1.0, "#3d8bff", 0), (6.0, 1.6, "#4cd964", 1))):
        bucket(L, f"Bucket{k}", (x, y, 0), h, tipped=bool(tip))
    for x, y, h, s in ((5.2, 1.0, "#4cd964", 1.0), (-4.2, 1.8, "#ff9a2e", 0.7), (3.4, 6.2, "#9d5cff", 0.8)):
        splash(L, "Spill", (x, y, 0.0), h, s, flat=True)

    # floating soap bubbles for sparkle
    sb = L.mat("SoapBubble", "#f2f8ff", 0.02, coat=1.0, emission="#ffffff", emit=0.05, alpha=0.35)
    floaters = []
    for k in range(9):
        x = rng.uniform(-8, 8); y = rng.uniform(1.5, 7); z = rng.uniform(2.6, 5.5)
        floaters.append((L.sphere("Floater", rng.uniform(0.12, 0.28), (x, y, z), m=sb, segs=20), (x, y, z), rng.random() * 6))

    return {
        "spots": {"center": (0, 0, 0), "left": (-2.7, 0.8, 0), "right": (2.7, 0.8, 0), "back": (0, 2.4, 0),
                  "backleft": (-1.5, 2.2, 0), "backright": (1.5, 2.2, 0), "farleft": (-4.7, 1.9, 0), "farright": (4.7, 1.9, 0)},
        "cams": {"wide": ((0.6, -10.2, 2.9), (0, 1.4, 2.0)), "mid": ((0.4, -7.2, 2.3), (0, 0.5, 1.6)), "center": (0, 0.4, 1.3), "orbit_r": 9.5,
                 "lab": ((-6.0, -3.0, 2.6), (-3.0, 3.0, 1.6)), "high": ((0, -8.5, 6.5), (0, 1.5, 1.0))},
        "prop_spots": {"top": (0, 0.6, 3.5), "left": (-3.9, 0.2, 2.5), "right": (3.9, 0.2, 2.5), "front": (0, -2.4, 0.7),
                       "frontleft": (-1.8, -2.2, 0.7), "frontright": (1.8, -2.2, 0.7)},
        "exposure": -0.45, "look": "AgX - Punchy",
        "anim": {"bubbles": bubbles, "floaters": floaters, "glow": (pink, cyan)},
    }


def animate(L, SET, f, t, s):
    A = SET.get("anim", {})
    for b, x, z0, ph in A.get("bubbles", []):
        u = (t * 0.7 + ph) % 1.0
        b.location = (x + math.sin(t * 5 + ph * 9) * 0.06, 4.4, z0 + u * 1.1)
        k = 1 - abs(u * 2 - 1) ** 3
        b.scale = (k, k, k)
    for o, (x, y, z), ph in A.get("floaters", []):
        o.location = (x + math.sin(t * 0.5 + ph) * 0.4, y, z + math.sin(t * 0.8 + ph) * 0.35)
    beat = s.get("beat", 0); e = s.get("energy", 0.5)
    pulse = 1 + 0.35 * e * max(0.0, 1 - beat * 3)
    for lt in A.get("glow", ()):
        lt.data.energy = 220 * pulse


# ------------------------------------------------------------------ teaching props
def bucket(L, name, at, color="#ff4b4b", tipped=False, parent=None):
    color = _hex(color)
    root = L.empty(name, at, parent)
    metal = L.mat("BucketWhite", "#f7f7fb", 0.25, coat=0.8)
    paint = L.mat("Paint" + color, color, 0.12, coat=1.0, sss=0.1)
    if tipped: root.rotation_euler = (math.radians(-80), 0, 0.4)
    z0 = 0.55 if tipped else 0.0
    L.cone(name + "Pail", 0.48, 0.6, 1.0, (0, 0, 0.5 + z0), (1, 1, 1), metal, root, verts=32)
    L.cylinder(name + "Band", 0.56, 0.3, (0, 0, 0.6 + z0), (1, 1, 1), paint, root, verts=32)
    L.cylinder(name + "Paint", 0.56, 0.05, (0, 0, 0.98 + z0), (1, 1, 1), paint, root, verts=32)
    L.sphere(name + "Drip", 0.13, (0.3, -0.45, 0.88 + z0), (0.6, 0.6, 1.4), paint, root, 12)
    L.torus(name + "Handle", 0.58, 0.03, (0, 0, 1.0 + z0), (1, 1, 1), L.mat("BucketHandle", "#9aa3b5", 0.3, metal=0.8), root, (0.0, math.radians(70), 0))
    return root


def splash(L, name, at, color="#ff4b4b", s=1.0, flat=False, parent=None):
    color = _hex(color)
    root = L.empty(name, at, parent)
    paint = L.mat("Paint" + color, color, 0.12, coat=1.0, sss=0.1)
    if flat:
        L.sphere(name + "Pool", 1.0 * s, (0, 0, 0.0), (1.1, 0.8, 0.05), paint, root, 32)
        for k in range(5):
            a = k * 1.3
            L.sphere(name + "Dot", 0.18 * s, (math.cos(a) * 1.35 * s, math.sin(a) * 1.05 * s, 0), (1, 1, 0.25), paint, root, 12)
        return root
    L.sphere(name + "Core", 0.55 * s, (0, 0, 0), (1, 0.35, 1), paint, root, 32)
    for k in range(8):
        a = k * math.tau / 8 + 0.2
        r = (0.75 + 0.25 * (k % 2)) * s
        L.sphere(name + "Blob", (0.2 + 0.06 * (k % 3)) * s, (math.cos(a) * r, 0, math.sin(a) * r), (1, 0.4, 1), paint, root, 16)
    return root


def prop(L, name, at, **o):
    """Teaching props. name: bucket, splash, swatch, block, crayon, beaker, apple, banana, carrot, leaf, grapes,
    drop, sun, flower, balloon, heart, star, rainbow. opts: color (hex or color word), n (number for block), text."""
    col = _hex(o.get("color", "#ff4b4b"))
    root = L.empty("Prop_" + name, at)
    if name == "bucket":
        bucket(L, "PBucket", (0, 0, -0.5), col, parent=root)
    elif name == "splash":
        splash(L, "PSplash", (0, 0, 0), col, o.get("size", 1.0), parent=root)
    elif name == "swatch":
        L.cube("Swatch", 1, (0, 0.02, 0), (1.2, 0.12, 1.5), L.mat("SwatchCard", "#ffffff", 0.3, coat=0.8), root, bevel=0.08)
        L.cube("SwatchCol", 1, (0, -0.06, 0.12), (1.0, 0.06, 1.05), candy(L, col), root, bevel=0.06)
        if o.get("text"):
            L.text3d("SwatchTxt", o["text"], 0.22, (0, -0.1, -0.55), L.mat("SwatchInk", "#3d2a7a", 0.4), root, extrude=0.03, bevel=0.01)
    elif name == "block":
        L.cube("Block", 1.1, (0, 0, 0), (1, 1, 1), candy(L, col), root, bevel=0.15)
        L.text3d("BlockNum", str(o.get("n", o.get("text", "1"))), 0.8, (0, -0.58, 0), L.mat("BlockInk", "#ffffff", 0.3, coat=0.6), root, extrude=0.06)
    elif name == "crayon":
        cm = L.mat(f"Crayon{col}", col, 0.45, sheen=0.3)
        piv = L.empty("PCrayon", (0, 0, 0), root); piv.rotation_euler = (0, math.radians(-60), 0)
        L.cylinder("PCrayonBody", 0.22, 2.0, (0, 0, 0), (1, 1, 1), cm, piv, verts=20)
        L.cone("PCrayonTip", 0.22, 0.05, 0.5, (0, 0, 1.25), (1, 1, 1), cm, piv, verts=20)
        for z in (-0.6, 0.6):
            L.cylinder("PCrayonBand", 0.235, 0.1, (0, 0, z), (1, 1, 1), L.mat("CrayonBand", "#2b2b38", 0.5), piv, verts=20)
    elif name == "beaker":
        L.cylinder("PBeaker", 0.45, 1.2, (0, 0, 0), (1, 1, 1), glass(L), root, verts=32)
        L.cylinder("PBeakerLiq", 0.4, 0.8, (0, 0, -0.18), (1, 1, 1), L.mat(f"Liquid{col}", col, 0.1, coat=1, sss=0.3, emission=col, emit=0.6), root, verts=32)
    elif name == "apple":
        L.sphere("Apple", 0.6, (0, 0, 0), (1, 0.95, 0.9), candy(L, col if o.get("color") else "#ff3b3b"), root, 32)
        L.cylinder("AppleStem", 0.04, 0.3, (0.02, 0, 0.6), (1, 1, 1), L.mat("Stem", "#7a4b2e", 0.6), root, (0, 0.2, 0), 8)
        L.sphere("AppleLeaf", 0.2, (0.2, 0, 0.66), (1, 0.25, 0.5), candy(L, "#4cd964"), root, 16, (0, -0.5, 0))
    elif name == "banana":
        ban = L.torus("Banana", 0.6, 0.17, (0, 0, 0.5), (1, 1, 1), candy(L, "#ffd21f", 0.35), root, (math.pi / 2, 0, 0))
        import bmesh
        bm = bmesh.new(); bm.from_mesh(ban.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > -0.2], context="VERTS"); bm.to_mesh(ban.data); bm.free()
        for sx in (-1, 1):
            L.sphere("BananaTip", 0.06, (sx * 0.43, 0, 0.05), (1, 1, 1), L.mat("Stem", "#7a4b2e", 0.6), root, 10)
    elif name == "carrot":
        L.cone("Carrot", 0.32, 0.04, 1.3, (0, 0, 0), (1, 1, 1), candy(L, "#ff8a1f", 0.4), root, (math.pi, 0, 0), 24)
        for a in (-0.4, 0, 0.4):
            L.cone("CarrotTop", 0.08, 0.01, 0.5, (math.sin(a) * 0.12, 0, 0.85), (1, 1, 1), candy(L, "#4cd964"), root, (0, a, 0), 10)
    elif name == "leaf":
        L.sphere("Leaf", 0.7, (0, 0, 0), (0.55, 0.12, 1), candy(L, col if o.get("color") else "#3ccf4e", 0.35), root, 32, (0, 0.5, 0))
        L.cylinder("LeafVein", 0.025, 1.3, (0, -0.07, 0), (1, 1, 1), candy(L, "#2e9e3e"), root, (0, 0.5, 0), 8)
    elif name == "grapes":
        gm = candy(L, col if o.get("color") else "#9d5cff", 0.2)
        k = 0
        for row, n in enumerate((4, 3, 2, 1)):
            for j in range(n):
                L.sphere("Grape", 0.2, ((j - (n - 1) / 2) * 0.36, (k % 2) * 0.05, 0.5 - row * 0.32), (1, 1, 1), gm, root, 16); k += 1
        L.cylinder("GrapeStem", 0.04, 0.3, (0, 0, 0.8), (1, 1, 1), L.mat("Stem", "#7a4b2e", 0.6), root, verts=8)
    elif name == "drop":
        dm = candy(L, col if o.get("color") else "#2f7bff", 0.1)
        L.sphere("Drop", 0.5, (0, 0, 0), (1, 0.85, 1), dm, root, 32)
        L.cone("DropTip", 0.43, 0.0, 0.7, (0, 0, 0.55), (1, 0.85, 1), dm, root, verts=32)
    elif name == "sun":
        sm = L.mat("SunProp", "#ffd21f", 0.3, coat=0.8, emission="#ffd21f", emit=0.6)
        L.sphere("SunBall", 0.55, (0, 0, 0), (1, 0.6, 1), sm, root, 32)
        for k in range(8):
            a = k * math.tau / 8
            L.cone("SunRay", 0.13, 0.0, 0.35, (math.cos(a) * 0.8, 0, math.sin(a) * 0.8), (1, 0.6, 1), sm, root, (0, math.pi / 2 - a, 0), 12)
    elif name == "flower":
        pm = candy(L, col if o.get("color") else "#9d5cff")
        for k in range(6):
            a = k * math.tau / 6
            L.sphere("Petal", 0.28, (math.cos(a) * 0.36, 0, math.sin(a) * 0.36), (1, 0.4, 1), pm, root, 16)
        L.sphere("FlowerMid", 0.22, (0, -0.06, 0), (1, 0.6, 1), candy(L, "#ffd21f"), root, 16)
        L.cylinder("FlowerStem", 0.04, 1.0, (0, 0.02, -0.75), (1, 1, 1), candy(L, "#3ccf4e"), root, verts=8)
    elif name == "balloon":
        bm = candy(L, col, 0.15)
        L.sphere("Balloon", 0.55, (0, 0, 0.2), (1, 1, 1.18), bm, root, 32)
        L.cone("BalloonKnot", 0.04, 0.09, 0.12, (0, 0, -0.5), (1, 1, 1), bm, root, verts=10)
        L.cylinder("BalloonString", 0.01, 1.0, (0, 0, -1.05), (1, 1, 1), L.mat("String", "#ffffff", 0.6), root, verts=6)
    elif name in ("heart", "star", "circle", "square", "triangle"):
        from chars.shape import outline, extrude
        pts, _, _ = outline(name)
        ob = extrude(L, "PShape", [(x, z - 0.8) for x, z in pts], 0.35, candy(L, col), root)
        ob.scale = (0.8, 0.8, 0.8)
    elif name == "rainbow":
        for k, h in enumerate(RAINBOW):
            tr = L.torus("PRain", 1.1 - k * 0.14, 0.07, (0, 0, -0.4), (1, 0.6, 1), L.mat(f"Rain{h}", h, 0.3, coat=0.8, emission=h, emit=0.15), root, (math.pi / 2, 0, 0))
            import bmesh
            bm = bmesh.new(); bm.from_mesh(tr.data)
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y < -0.02], context="VERTS"); bm.to_mesh(tr.data); bm.free()
    else:
        L.sphere("PBall", 0.5, (0, 0, 0), (1, 1, 1), candy(L, col), root, 32)
    return root
