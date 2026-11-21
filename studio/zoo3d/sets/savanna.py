"""Sunny golden African savanna: The Animated Zoo's 3D savanna set (see API.md).
Golden grass (one merged blade mesh, no particles), acacia trees, a watering hole, rolling hills,
a Kilimanjaro silhouette, puffy clouds and a big friendly sun. Everything stays inside the camera's
100 m clip range."""
import math, os
import bpy, bmesh

FONT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts", "Poppins-Bold.ttf")


def _font(o):
    """Chunky rounded kids font on a text3d object (falls back to Blender's default font)."""
    try:
        f = bpy.data.fonts.get("PropFont") or bpy.data.fonts.load(FONT)
        f.name = "PropFont"; o.data.font = f
    except Exception:
        pass
    return o


def _world(L):
    """Big warm sky: golden haze at the horizon fading to a clear blue at the top."""
    w = bpy.data.worlds.new("SavannaSky"); L.scene().world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    cr.elements[0].position = 0.0; cr.elements[0].color = (*L.rgb("#ffc978"), 1)
    cr.elements[1].position = 0.42; cr.elements[1].color = (*L.rgb("#1f7fe0"), 1)
    e = cr.elements.new(0.04); e.color = (*L.rgb("#ffe2a6"), 1)
    e = cr.elements.new(0.12); e.color = (*L.rgb("#7cc3f5"), 1)
    e = cr.elements.new(0.24); e.color = (*L.rgb("#43a0ee"), 1)
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.0
    return w


def _ground_mat(L):
    m = bpy.data.materials.new("SavGround"); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.9
    if "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = 0.5
    tc = nt.nodes.new("ShaderNodeTexCoord")
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 0.12; n.inputs["Detail"].default_value = 4
    nt.links.new(tc.outputs["Object"], n.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    cr.elements[0].position = 0.35; cr.elements[0].color = (*L.rgb("#d9962a"), 1)
    cr.elements[1].position = 0.65; cr.elements[1].color = (*L.rgb("#f5c445"), 1)
    e = cr.elements.new(0.5); e.color = (*L.rgb("#c8a83a"), 1)
    nt.links.new(n.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    vor = nt.nodes.new("ShaderNodeTexNoise"); vor.inputs["Scale"].default_value = 60
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35
    nt.links.new(tc.outputs["Object"], vor.inputs["Vector"]); nt.links.new(vor.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def _grass_mat(L):
    m = bpy.data.materials.new("SavGrass"); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.75
    for k, v in (("Sheen Weight", 0.6), ("Subsurface Weight", 0.08)):
        if k in b.inputs: b.inputs[k].default_value = v
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 0.25
    nt.links.new(tc.outputs["Object"], n.inputs["Vector"])
    mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "MULTIPLY_ADD"
    mx.inputs[1].default_value = 1.4
    nt.links.new(sep.outputs["Z"], mx.inputs[0]); nt.links.new(n.outputs["Fac"], mx.inputs[2])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    cr.elements[0].position = 0.3; cr.elements[0].color = (*L.rgb("#a8902a"), 1)
    cr.elements[1].position = 1.2 / 1.6; cr.elements[1].color = (*L.rgb("#ffe08a"), 1)
    e = cr.elements.new(0.5); e.color = (*L.rgb("#e2b04a"), 1)
    nt.links.new(mx.outputs["Value"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    return m


def _grass(L, rng, mat, clear):
    """All grass blades in one mesh: tufts of thin cones, shorter near the stage."""
    me = bpy.data.meshes.new("SavGrass"); bm = bmesh.new()
    def tuft(x, y, h, n):
        for _ in range(n):
            ret = bmesh.ops.create_cone(bm, cap_ends=False, segments=4, radius1=0.035 + rng.random() * 0.02, radius2=0.0, depth=h * (0.6 + rng.random() * 0.6))
            vs = ret["verts"]; d = h * 0.5
            ax, ay = (rng.random() - 0.5) * 0.7, (rng.random() - 0.5) * 0.7
            for v in vs:
                z = v.co.z + d
                v.co.x += x + (rng.random() - 0.5) * 0.25 + ax * z; v.co.y += y + (rng.random() - 0.5) * 0.25 + ay * z; v.co.z = z
    for i in range(620):
        x = (rng.random() - 0.5) * 36; y = -7 + rng.random() ** 1.15 * 36
        if y < -2.2 and abs(x) < 4.5:     # keep the view of the cast's feet clear
            continue
        far = max(0.0, (y - 4) / 30)
        cx, cy, rx, ry = clear
        if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1.0:
            continue
        if ((x - 7.5) / 3.6) ** 2 + ((y - 6) / 2.2) ** 2 < 1.0:   # watering hole
            continue
        tuft(x, y, (0.45 + rng.random() * 0.4) * (1 + far * 0.8), 6 + int(rng.random() * 5))
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("SavGrass", me); L.scene().collection.objects.link(o); o.data.materials.append(mat)
    return o


def _acacia(L, rng, x, y, s, k):
    bark = L.mat("AcaciaBark", "#6b4426", 0.9, bump=0.3, bump_scale=6)
    leafs = [L.mat(f"Acacia{i}", c, 0.75, sheen=0.3, sss=0.05, bump=0.25, bump_scale=4)
             for i, c in enumerate(("#6f9a2c", "#82ab36", "#5f8a26"))]
    lean = (rng.random() - 0.5) * 0.25
    L.cylinder("AcTrunk", 0.18 * s, 2.6 * s, (x, y, 1.3 * s), m=bark, rot=(0, lean, 0), verts=12)
    top = (x + math.sin(lean) * 2.6 * s, y, 2.55 * s)
    for sx in (-1, 1):
        L.cylinder("AcBranch", 0.1 * s, 1.5 * s, (top[0] + 0.45 * s * sx, y, top[2] + 0.45 * s), m=bark, rot=(0, 0.75 * sx, 0), verts=10)
    for j, (dx, dy, dz, r) in enumerate(((0, 0, 0.95, 1.6), (-1.3, 0.2, 0.75, 1.1), (1.35, -0.1, 0.8, 1.2), (0.3, 0.6, 1.15, 1.0), (-0.5, -0.5, 1.1, 0.9))):
        L.sphere("AcCanopy", r * s, (top[0] + dx * s, top[1] + dy * s, top[2] + dz * s), (1.35, 1.1, 0.33), leafs[(j + k) % 3], segs=20)


def build(L, rng, **_):
    _world(L)
    L.light("Sun", "SUN", 4.6, rot=(math.radians(52), 0, math.radians(-28)), color=(1, 0.9, 0.74), angle=math.radians(4))
    L.light("Fill", "AREA", 260, (-4, -10, 6), (math.radians(58), 0, math.radians(-20)), (1, 0.9, 0.8), 10)
    L.light("Rim", "AREA", 650, (3, 9, 5), (math.radians(-62), 0, math.radians(165)), (1, 0.82, 0.55), 9)

    L.cube("Ground", 1, (0, 35, -0.5), (200, 110, 1), _ground_mat(L))
    clear = (0, 0.9, 6.8, 2.9)
    L.cylinder("Stage", 1.0, 0.02, (clear[0], clear[1], 0.006), (clear[2] * 0.95, clear[3] * 0.95, 1),
               L.mat("Dirt", "#eab066", 1.0, sheen=0.2, bump=0.25, bump_scale=10), verts=48)
    _grass(L, rng, _grass_mat(L), clear)
    fl = [L.mat(f"SavFlower{i}", c, 0.5, sss=0.2) for i, c in enumerate(("#ff7043", "#fff176", "#ffffff", "#f06292"))]
    for i in range(40):
        a = rng.random() * math.tau; rr = 1.0 + rng.random() * 0.25
        x, y = clear[0] + math.cos(a) * clear[2] * rr, clear[1] + math.sin(a) * clear[3] * rr
        L.sphere("Flower", 0.08, (x, y, 0.1), (1, 1, 0.6), fl[i % 4], segs=10)

    # watering hole (right side, behind the hippo)
    L.cylinder("PondRim", 1.0, 0.06, (7.5, 6, 0.02), (3.9, 2.4, 1), L.mat("Mud", "#9a6a3c", 0.8, bump=0.3, bump_scale=8), verts=48)
    water = L.mat("Water", "#2fa8e0", 0.05, coat=1.0)
    pond = L.cylinder("Pond", 1.0, 0.06, (7.5, 6, 0.05), (3.5, 2.05, 1), water, verts=48)
    ripple = L.torus("Ripple", 1.0, 0.025, (7.0, 5.8, 0.09), (1, 0.6, 0.3), L.mat("RippleW", "#d8f3ff", 0.1, emission="#d8f3ff", emit=0.4))
    reed = L.mat("Reed", "#5d9a32", 0.7, sheen=0.3)
    for k in range(9):
        a = 0.2 + k * 0.33
        L.cone("Reed", 0.06, 0.0, 0.8 + rng.random() * 0.6, (7.5 + math.cos(a) * 3.7, 6 + math.sin(a) * 2.3, 0.45), m=reed, rot=((rng.random() - .5) * .3, (rng.random() - .5) * .3, 0), verts=6)
    rock = L.mat("Rock", "#a08c7a", 0.85, bump=0.4, bump_scale=3)
    for (x, y, r) in ((4.3, 5.2, 0.5), (4.9, 7.4, 0.35), (10.6, 5.0, 0.6), (-7.5, 2.0, 0.7), (-6.6, 2.6, 0.4), (-10.5, 9, 1.0), (11.5, 11, 0.8)):
        L.sphere("Rock", r, (x, y, r * 0.3), (1.3, 1, 0.75), rock, segs=16)

    # acacia trees: one big framing tree, midground and background ones
    for k, (x, y, s) in enumerate(((-10.5, 4.5, 1.35), (11.5, 13, 1.1), (-6.5, 15, 1.0), (3.5, 22, 0.9), (-17, 24, 1.0), (18, 26, 1.0), (-1, 40, 0.9), (26, 45, 1.1), (-30, 42, 1.1))):
        _acacia(L, rng, x, y, s, k)
    bush = [L.mat(f"Bush{i}", c, 0.7, sheen=0.3, bump=0.3, bump_scale=5) for i, c in enumerate(("#7a9c34", "#90ae3e"))]
    for k, (x, y, r) in enumerate(((-8.2, 7, 0.8), (-12, 10, 1.0), (9.5, 9, 0.7), (13, 6, 0.9), (-4, 11, 0.6), (6, 15, 0.8), (-14, 17, 1.2), (15, 19, 1.0))):
        L.sphere("Bush", r, (x, y, r * 0.45), (1.3, 1, 0.8), bush[k % 2], segs=16)
        L.sphere("Bush", r * 0.7, (x + r * 0.7, y + 0.2, r * 0.35), (1.2, 1, 0.8), bush[(k + 1) % 2], segs=16)

    # rolling hills (atmospheric: lighter and bluer with distance)
    for k, (x, y, sx, sz, c) in enumerate(((-30, 50, 26, 6, "#d1a24a"), (8, 55, 30, 5, "#c9a24f"), (38, 52, 24, 7, "#c49650"),
                                            (-12, 66, 40, 4.5, "#c79a6a"), (30, 68, 36, 4.5, "#b39ab0"))):
        L.sphere("Hill", 1.0, (x, y, 0), (sx, 10, sz), L.mat(f"Hill{k}", c, 1.0), segs=32)
    # Kilimanjaro silhouette with a snowy top
    KX = -17
    L.cone("Kili", 30, 8, 14, (KX, 82, 3.0), (1, 0.4, 1), L.mat("KiliM", "#7d78b8", 1.0), verts=40)
    L.cone("KiliSnow", 11.6, 8.0, 2.4, (KX, 81.5, 9.0), (1, 0.4, 1), L.mat("Snow", "#ffffff", 0.8, emission="#f4f2ff", emit=0.35), verts=40)
    for k, (dx, z, r) in enumerate(((-4.5, 9.9, 2.2), (0.5, 10.4, 2.5), (5, 9.7, 2.0), (-8.5, 8.1, 1.4), (9, 7.9, 1.3))):
        L.sphere("SnowPuff", r, (KX + dx, 80.5, z), (1, 0.5, 0.45), L.mat("Snow", "#ffffff", 0.8), segs=20)

    # big friendly sun + puffy clouds
    sun = L.sphere("SkySun", 4.2, (22, 80, 24), m=L.mat("SunDisc", "#ffe27a", 0.5, emission="#ffd84a", emit=6.0), segs=32)
    glow = L.sphere("SunGlow", 6.5, (22, 80.5, 24), (1, 0.2, 1), L.mat("SunHalo", "#fff1b8", 0.5, emission="#ffe9a0", emit=1.2, alpha=0.35), segs=32)
    cloud_m = L.mat("Cloud", "#ffffff", 0.9, sheen=0.4, emission="#fff6ea", emit=0.5)
    clouds = []
    for k, (x, y, z, s) in enumerate(((-26, 70, 19, 2.6), (-4, 76, 23, 3.0), (34, 68, 17, 2.4), (10, 72, 15, 1.8), (-40, 62, 13, 2.0))):
        c = L.empty("Cloud", (x, y, z))
        for dx, dz, r in ((0, 0, 1.0), (1.1, -0.25, 0.75), (-1.1, -0.3, 0.7), (0.5, 0.45, 0.7), (-0.4, 0.4, 0.65)):
            L.sphere("Puff", r * s, (dx * s, 0, dz * s), (1, 0.6, 0.85), cloud_m, c, 20)
        clouds.append((c, x))

    return {
        "spots": {"center": (0, -0.6, 0), "lion": (-2.35, 0.1, 0), "zebra": (2.6, 0.2, 0),
                  "elephant": (-4.6, 1.3, 0), "hippo": (4.9, 1.4, 0), "giraffe": (1.1, 3.3, 0),
                  "left": (-2.35, 0.1, 0), "right": (2.35, 0.1, 0), "back": (0, 2.4, 0)},
        "cams": {"wide": ((0, -13.4, 4.4), (0, 1.0, 1.75)), "center": (0, 0.6, 1.7), "orbit_r": 10.5,
                 "pond": ((-1.5, -6.5, 2.6), (5.5, 4.5, 1.1)), "hero": ((-1.2, -8.0, 1.0), (0, 0.5, 2.2)),
                 "vista": ((0, -10.0, 5.2), (0, 6, 2.6)),
                 "giraffe": ((2.3, -0.8, 3.6), (1.1, 3.3, 3.05))},   # giraffe close-up from the side, clear of Milo's crest
        "prop_spots": {"top": (0, 0.0, 4.15), "left": (-3.6, -1.4, 3.3), "right": (3.6, -1.4, 3.3), "front": (0, -2.6, 0.9)},
        "exposure": -0.3, "look": "AgX - Punchy",
        "_clouds": clouds, "_sun": (sun, glow), "_ripple": ripple,
    }


# ---------------------------------------------------------------- teaching props
SIGN_COLORS = {"LION": "#ff9f1c", "ELEPHANT": "#5c7cfa", "GIRAFFE": "#f7b500", "ZEBRA": "#3d3d4e", "HIPPO": "#b06ad9"}


def prop(L, name, at, **o):
    root = L.empty("Prop_" + name, at)
    if name == "sign":   # animal name sign: rounded wooden plank with chunky letters
        txt = o.get("text", "LION").upper()
        w = 0.42 * len(txt) + 0.5
        L.cube("SignBoard", 1, (0, 0.05, 0), (w, 0.12, 0.72), L.mat("SignWood", "#f5d9a8", 0.55, coat=0.3, bump=0.15, bump_scale=6), root, bevel=0.06)
        L.cube("SignEdge", 1, (0, 0.1, 0), (w + 0.16, 0.1, 0.88), L.mat("SignEdgeW", "#9b5e2e", 0.6, coat=0.2), root, bevel=0.06)
        c = o.get("color", SIGN_COLORS.get(txt, "#ff6f00"))
        _font(L.text3d("SignText", txt, 0.62, (0, -0.06, -0.02), L.mat("SignInk" + c, c, 0.3, coat=0.7, emission=c, emit=0.15), root, extrude=0.06, bevel=0.015))
    elif name == "num":  # number badge (counting the zoo friends)
        n = str(o.get("n", 1)); c = o.get("color", "#ff4f7b")
        L.cylinder("NumDisc", 0.5, 0.14, (0, 0.05, 0), m=L.mat("NumDisc" + c, c, 0.3, coat=0.8), parent=root, rot=(math.pi / 2, 0, 0), verts=40)
        L.torus("NumRing", 0.5, 0.06, (0, 0.05, 0), m=L.mat("NumRing", "#ffffff", 0.3, coat=0.8), parent=root, rot=(math.pi / 2, 0, 0))
        _font(L.text3d("NumText", n, 0.8, (0, -0.06, -0.02), L.mat("NumInk", "#ffffff", 0.3, coat=0.6, emission="#ffffff", emit=0.2), root, extrude=0.06, bevel=0.015))
    elif name == "leaves":  # a leafy acacia branch (giraffe snack)
        L.cylinder("Twig", 0.04, 1.4, (0, 0, 0), m=L.mat("AcaciaBark", "#6b4426", 0.9), parent=root, rot=(0, math.pi / 2.3, 0), verts=8)
        lm = L.mat("PropLeaf", "#6fc23a", 0.5, coat=0.4, sss=0.1)
        for k in range(7):
            x = -0.6 + k * 0.2
            L.sphere("Leaf", 0.15, (x, -0.02, 0.12 * (1 if k % 2 else -1) + x * 0.4), (1.3, 0.35, 0.7), lm, root, 12, (0, 0.5 * (1 if k % 2 else -1), 0))
    elif name == "splash":  # water splash crown + droplets
        wm = L.mat("SplashW", "#5cc8ff", 0.05, coat=1.0, emission="#9fe0ff", emit=0.3)
        L.torus("SplashRing", 0.45, 0.07, (0, 0, -0.35), (1, 1, 0.5), wm, root)
        for k in range(8):
            a = k / 8 * math.tau
            L.sphere("Drop", 0.11, (math.cos(a) * 0.45, math.sin(a) * 0.25, 0.1 + 0.25 * (k % 2)), (0.8, 0.8, 1.3), wm, root, 12)
        L.sphere("DropTop", 0.16, (0, 0, 0.55), (0.8, 0.8, 1.3), wm, root, 16)
    elif name == "sun":  # smiling sun (hot day)
        sm = L.mat("PropSun", "#ffcc33", 0.3, coat=0.6, emission="#ffb300", emit=0.6)
        L.sphere("SunBall", 0.5, (0, 0, 0), (1, 0.6, 1), sm, root, 32)
        for k in range(10):
            a = k / 10 * math.tau
            L.cone("Ray", 0.1, 0.0, 0.3, (math.cos(a) * 0.7, 0, math.sin(a) * 0.7), m=sm, parent=root, rot=(0, -a + math.pi / 2, 0), verts=8)
        L.sphere("SunEyeL", 0.06, (-0.16, -0.3, 0.08), m=L.mat("Pupil", "#050303", 0.4), parent=root, segs=12)
        L.sphere("SunEyeR", 0.06, (0.16, -0.3, 0.08), m=L.mat("Pupil", "#050303", 0.4), parent=root, segs=12)
        sm_ = L.torus("SunSmile", 0.15, 0.03, (0, -0.3, -0.02), (1, 0.7, 0.6), L.mat("Pupil", "#050303", 0.4), root, (math.pi / 2, 0, 0))
        bm = bmesh.new(); bm.from_mesh(sm_.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0.004], context="VERTS"); bm.to_mesh(sm_.data); bm.free()
    elif name == "heart":  # family love (lion pride)
        hm = L.mat("PropHeart", "#ff4f7b", 0.3, coat=0.8, emission="#ff4f7b", emit=0.2)
        for sx in (-1, 1):
            L.sphere("HeartLobe", 0.3, (0.2 * sx, 0, 0.12), (1, 0.6, 1), hm, root, 24)
        L.cone("HeartTip", 0.44, 0.0, 0.6, (0, 0, -0.25), (1, 0.55, 1), hm, root, (math.pi, 0, 0), verts=24)
    else:  # fallback: text
        c = o.get("color", "#ffcc00")
        L.text3d("PropText", o.get("text", name.upper()), o.get("size", 0.9), (0, 0, 0), L.mat("Prop" + c, c, 0.3, coat=0.6, emission=c, emit=0.25), root)
    if name != "text" and "size" in o:
        root.scale = (o["size"],) * 3
    return root


def animate(L, SET, f, t, s):
    for c, x0 in SET.get("_clouds", []):
        c.location.x = x0 + math.sin(t * 0.05 + x0) * 2.0 + t * 0.03
    sun, glow = SET["_sun"]
    p = 1 + 0.04 * math.sin(s.get("beat", 0) * math.tau) * s.get("energy", 0.5)
    sun.scale = (p, p, p); glow.scale = (p * 1.05, 0.2, p * 1.05)
    r = SET["_ripple"]; u = (t * 0.5) % 1.0
    r.scale = (0.4 + 1.6 * u, (0.4 + 1.6 * u) * 0.6, 0.3)
