"""Gizmo's space-station science lab: a bright, candy-coloured lab with a huge window onto planets and stars,
a spinning planet model (orrery), a workbench of bubbling beakers, gears, screens and blinking lights.

prop(L, name, at, size=1.0, face=True): sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, moon,
    raincloud, lightbulb, magnet, gear, rocket, star, beaker.
animate(): planets spin, gears turn, lights blink and screens pulse on the beat.
"""
import math
import bpy, bmesh

# ---------------------------------------------------------------- shader helpers
def _bsdf(m):
    return m.node_tree.nodes["Principled BSDF"]


def _glass(L, name, tint="#ffffff"):
    m = L.mat(name, tint, 0.03, coat=0.0)
    b = _bsdf(m)
    for k, v in (("Transmission Weight", 1.0), ("IOR", 1.3)):
        if k in b.inputs: b.inputs[k].default_value = v
    return m


def _banded(L, name, cols, scale=3.0, mode="bands", distort=2.0, emit=0.0):
    """Planet surface: wave bands (gas giants) or noise blotches (rocky / continents) between a few colours."""
    if name in L._mats: return L._mats[name]
    m = L.mat(name, cols[0], 0.55, coat=0.35)
    nt = m.node_tree; b = _bsdf(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    if mode == "bands":
        tex = nt.nodes.new("ShaderNodeTexWave"); tex.wave_type = "BANDS"; tex.bands_direction = "Z"
        tex.inputs["Scale"].default_value = scale; tex.inputs["Distortion"].default_value = distort
        tex.inputs["Detail"].default_value = 2.0
        out = tex.outputs["Fac"]
    else:
        tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = scale
        tex.inputs["Detail"].default_value = 3.0
        out = tex.outputs["Fac"]
    nt.links.new(tc.outputs["Object"], tex.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    if mode == "land":
        cr.interpolation = "CONSTANT"
    while len(cr.elements) < len(cols): cr.elements.new(0.5)
    for i, c in enumerate(cols):
        cr.elements[i].position = (i / (len(cols) - 1)) if mode != "land" else [0.0, 0.52, 0.62][i] if i < 3 else 0.7
        cr.elements[i].color = (*L.rgb(c), 1)
    nt.links.new(out, ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    if emit:
        nt.links.new(ramp.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = emit
    return m


def _space_mat(L):
    """Deep blue/purple nebula with procedural stars (emissive backdrop seen through the window)."""
    m = bpy.data.materials.new("SpaceBackdrop"); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
    tc = nt.nodes.new("ShaderNodeNewGeometry")   # world position: stars stay round on the stretched backdrop
    noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 0.035; noise.inputs["Detail"].default_value = 4
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    cr.elements.new(0.5)
    cr.elements[0].position = 0.3; cr.elements[0].color = (*L.rgb("#0b1a66"), 1)
    cr.elements[1].position = 0.52; cr.elements[1].color = (*L.rgb("#3a2399"), 1)
    cr.elements[2].position = 0.72; cr.elements[2].color = (*L.rgb("#c04fb8"), 1)
    nt.links.new(tc.outputs["Position"], noise.inputs["Vector"]); nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 0.7
    vor.feature = "F1"
    nt.links.new(tc.outputs["Position"], vor.inputs["Vector"])
    st = nt.nodes.new("ShaderNodeMapRange"); st.inputs["From Min"].default_value = 0.09; st.inputs["From Max"].default_value = 0.0
    st.inputs["To Min"].default_value = 0.0; st.inputs["To Max"].default_value = 6.0
    nt.links.new(vor.outputs["Distance"], st.inputs["Value"])
    add = nt.nodes.new("ShaderNodeMix"); add.data_type = "RGBA"; add.blend_type = "ADD"
    add.inputs["Factor"].default_value = 1.0
    nt.links.new(ramp.outputs["Color"], add.inputs[6]); nt.links.new(st.outputs["Result"], add.inputs[7])
    nt.links.new(add.outputs[2], em.inputs["Color"]); em.inputs["Strength"].default_value = 1.0
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return m


def _wave_screen(L, name, c1, c2):
    m = L.mat(name, c1, 0.2, emission=c1, emit=2.0)
    nt = m.node_tree; b = _bsdf(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    w = nt.nodes.new("ShaderNodeTexWave"); w.inputs["Scale"].default_value = 3.0; w.inputs["Distortion"].default_value = 4.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*L.rgb(c1), 1); ramp.color_ramp.elements[1].color = (*L.rgb(c2), 1)
    nt.links.new(tc.outputs["Generated"], w.inputs["Vector"]); nt.links.new(w.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Emission Color"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    return m


def gear_mesh(L, name, r, teeth, depth, m=None, loc=(0, 0, 0), rot=(math.pi / 2, 0, 0), parent=None, hole=0.3):
    """Single-object chunky toy gear (teeth around a ring with a hole), faces -Y by default."""
    bm = bmesh.new()
    n = teeth * 4; outer = []
    for k in range(n):
        a = k / n * math.tau
        rr = r * (1.0 if (k % 4) in (1, 2) else 0.8)
        outer.append(bm.verts.new((math.cos(a) * rr, math.sin(a) * rr, 0)))
    inner = [bm.verts.new((math.cos(k / n * math.tau) * r * hole, math.sin(k / n * math.tau) * r * hole, 0)) for k in range(n)]
    for k in range(n):
        bm.faces.new((outer[k], outer[(k + 1) % n], inner[(k + 1) % n], inner[k]))
    ext = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
    for v in ext["geom"]:
        if isinstance(v, bmesh.types.BMVert): v.co.z += depth
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    if m is not None: me.materials.append(m)
    bv = o.modifiers.new("Bevel", "BEVEL"); bv.width = depth * 0.2; bv.segments = 2; bv.use_clamp_overlap = True
    if parent is not None: o.parent = parent
    o.location = loc; o.rotation_euler = rot
    return o


# ---------------------------------------------------------------- set
def build(L, rng, **_):
    L.sky("#4a3fa8", 0.6, nishita=False)
    L.light("Sun", "SUN", 2.6, rot=(math.radians(52), 0, math.radians(-18)), color=(1, 0.95, 0.86), angle=math.radians(8))
    L.light("Key", "AREA", 650, (-4.5, -7.5, 6.5), (math.radians(50), 0, math.radians(-30)), (1, 0.95, 0.9), 6)
    L.light("Fill", "AREA", 380, (6, -6, 4), (math.radians(60), 0, math.radians(40)), (0.85, 0.9, 1), 7)
    L.light("Rim", "AREA", 420, (0, 4.5, 5.5), (math.radians(-55), 0, 0), (0.75, 0.95, 1), 6)
    L.light("WallWash", "AREA", 300, (0, -2, 9), (0, 0, 0), (1, 0.97, 0.95), 14)
    L.light("WinGlow", "AREA", 250, (0, 5.2, 3.0), (math.radians(-90), 0, 0), (0.75, 0.6, 1.0), 9)

    floor = L.mat("LabFloor", "#e8f1fb", 0.18, coat=0.6)
    fn = floor.node_tree; geo = fn.nodes.new("ShaderNodeNewGeometry"); chk = fn.nodes.new("ShaderNodeTexChecker")
    chk.inputs["Scale"].default_value = 0.5; chk.inputs["Color1"].default_value = (*L.rgb("#eef5ff"), 1)
    chk.inputs["Color2"].default_value = (*L.rgb("#c9dcff"), 1)
    fn.links.new(geo.outputs["Position"], chk.inputs["Vector"]); fn.links.new(chk.outputs["Color"], _bsdf(floor).inputs["Base Color"])
    wall = L.mat("LabWall", "#8fb8ff", 0.45, coat=0.2)
    wall2 = L.mat("LabWall2", "#b9a7ff", 0.45, coat=0.2)
    trim = L.mat("LabTrim", "#ffb703", 0.3, coat=0.8)
    teal = L.mat("LabTeal", "#19c3b3", 0.3, coat=0.8)
    pink = L.mat("LabPink", "#ff5fa2", 0.3, coat=0.8)
    white = L.mat("LabWhite", "#f6f8ff", 0.3, coat=0.6)
    steel = L.mat("LabSteel", "#a9b4c8", 0.25, coat=0.5, metal=0.6)
    cyan = L.mat("LabCyanGlow", "#5ff3ff", 0.2, emission="#5ff3ff", emit=3.0)

    # floor + rug + stage
    L.cube("Floor", 1, (0, 0, -0.5), (40, 30, 1), floor)
    L.cylinder("Rug1", 3.6, 0.02, (0, 0.3, 0.01), (1.35, 1, 1), L.mat("Rug1", "#ffd23f", 0.8, sheen=0.4), verts=48)
    L.cylinder("Rug2", 2.9, 0.022, (0, 0.3, 0.015), (1.35, 1, 1), L.mat("Rug2", "#ff7a45", 0.8, sheen=0.4), verts=48)
    L.cylinder("Stage", 2.2, 0.12, (0, 0.3, 0.06), (1.35, 1, 1), white, verts=48)
    L.torus("StageRim", 2.2, 0.05, (0, 0.3, 0.12), (1.35, 1, 1), cyan)

    # back wall with a huge window (built from frame pieces, so it is truly open)
    WY = 5.6
    L.cube("WallLow", 1, (0, WY, 0.55), (10.0, 0.4, 1.1), wall)
    L.cube("WallTop", 1, (0, WY, 8.5), (10.0, 0.4, 7.0), wall)
    L.cube("WallL", 1, (-9.5, WY, 6.0), (9.0, 0.4, 12), wall)
    L.cube("WallR", 1, (9.5, WY, 6.0), (9.0, 0.4, 12), wall)
    for nm, loc, sc in (("WinB", (0, WY - 0.25, 1.1), (10.2, 0.4, 0.3)), ("WinT", (0, WY - 0.25, 5.0), (10.2, 0.4, 0.3)),
                        ("WinLf", (-5.0, WY - 0.25, 3.05), (0.3, 0.4, 4.2)), ("WinRt", (5.0, WY - 0.25, 3.05), (0.3, 0.4, 4.2))):
        L.cube(nm, 1, loc, sc, trim, bevel=0.1, segs=3)
    L.cube("WinMull", 1, (0, WY - 0.2, 3.05), (0.12, 0.2, 3.8), steel, bevel=0.04)
    L.cube("WallStripe", 1, (0, WY - 0.22, 0.75), (28, 0.1, 0.16), teal, bevel=0.03)
    # angled side walls (purple) for depth
    for sx in (-1, 1):
        L.cube(f"SideWall{sx}", 1, (9.0 * sx, 2.2, 6.0), (0.4, 8, 12), wall2, rot=(0, 0, -0.45 * sx))
        L.cube(f"SideStripe{sx}", 1, (8.75 * sx, 2.1, 0.75), (0.1, 8, 0.16), teal, rot=(0, 0, -0.45 * sx))

    # beyond the window: space backdrop + big planets
    L.cube("Space", 1, (0, 40, 6), (120, 0.5, 60), _space_mat(L))
    big = {}
    big["ringed"] = L.sphere("WinSaturn", 2.6, (6.5, 22, 5.6), m=_banded(L, "WinSaturnMat", ("#f2d27a", "#e0a95c", "#fff0c2"), 2.5), segs=48)
    ring = L.torus("WinSaturnRing", 4.2, 0.9, (6.5, 22, 5.6), (1, 1, 0.04), L.mat("WinRing", "#ffe0a3", 0.4, emission="#ffd58a", emit=0.3), rot=(0.35, -0.3, 0))
    big["blue"] = L.sphere("WinPlanet2", 1.7, (-6.0, 20, 6.5), m=_banded(L, "WinBlueMat", ("#3d7bff", "#5fe0ff", "#2b44c9"), 2.0, "noise"), segs=40)
    big["moon"] = L.sphere("WinMoon", 0.7, (-2.2, 18, 4.2), m=L.mat("WinMoonMat", "#ffd6f2", 0.7, bump=0.4, bump_scale=6), segs=24)
    L.light("SpaceSun", "SUN", 1.5, rot=(math.radians(60), 0, math.radians(160)), color=(1, 0.9, 0.95))

    # light bulbs along the window frame (blink on the beat)
    bulbs = [L.mat(f"Bulb{i}", c, 0.2, emission=c, emit=3.0) for i, c in enumerate(("#ff4d6d", "#ffd23f", "#4dff9a", "#4dc3ff"))]
    for k in range(13):
        x = -4.8 + k * 0.8
        L.sphere("Bulb", 0.09, (x, WY - 0.5, 5.0), m=bulbs[k % 4], segs=12)

    # gears on the wall (turn in animate)
    gears = []
    for sx in (-1, 1):
        g1 = gear_mesh(L, "Gear", 0.95, 10, 0.18, trim if sx < 0 else pink, (6.6 * sx, WY - 0.3, 4.3))
        g2 = gear_mesh(L, "Gear", 0.6, 7, 0.18, teal if sx < 0 else trim, (6.6 * sx - 1.33 * sx, WY - 0.32, 5.0))
        gears += [(g1, 1.0 * sx), (g2, -1.0 * 0.95 / 0.6 * sx)]
    # screens on the wall
    screens = []
    for sx, c1, c2 in ((-1, "#1fd1ff", "#7a3cff"), (1, "#ff5fa2", "#ffd23f")):
        L.cube(f"ScreenBox{sx}", 1, (6.6 * sx, WY - 0.3, 2.3), (2.1, 0.2, 1.4), white, bevel=0.12, segs=3)
        sc = L.cube(f"Screen{sx}", 1, (6.6 * sx, WY - 0.42, 2.3), (1.8, 0.05, 1.1), _wave_screen(L, f"ScreenMat{sx}", c1, c2), bevel=0.05)
        screens.append(sc)

    # left: workbench with bubbling beakers
    bx, by = -4.7, 2.6
    L.cube("BenchTop", 1, (bx, by, 1.0), (3.0, 1.3, 0.14), white, bevel=0.05)
    L.cube("BenchBody", 1, (bx, by + 0.05, 0.48), (2.8, 1.1, 0.9), teal, bevel=0.08)
    for k, x in enumerate((-0.9, 0, 0.9)):
        L.sphere("Knob", 0.07, (bx + x, by - 0.58, 0.6), m=trim, segs=12)
    glass = _glass(L, "LabGlass")
    liquids = [L.mat(f"Liquid{i}", c, 0.2, coat=0.5, emission=c, emit=0.8) for i, c in enumerate(("#ff3d7f", "#3dff8b", "#3db8ff", "#ffcc33"))]
    bubbles = []
    for k, (x, h, r, kind) in enumerate(((-1.1, 0.5, 0.2, "tube"), (-0.45, 0.42, 0.26, "flask"), (0.3, 0.6, 0.18, "tube"), (1.0, 0.36, 0.3, "flask"))):
        px, pz = bx + x, 1.07
        if kind == "tube":
            L.cylinder("Beaker", r, h, (px, by, pz + h / 2), m=glass, verts=24)
            L.cylinder("Liquid", r * 0.86, h * 0.62, (px, by, pz + h * 0.31), m=liquids[k], verts=24)
        else:
            L.sphere("Flask", r, (px, by, pz + r), m=glass, segs=24)
            L.sphere("FlaskLiq", r * 0.86, (px, by, pz + r * 0.86), (1, 1, 0.8), liquids[k], segs=24)
            L.cylinder("FlaskNeck", r * 0.32, r * 1.1, (px, by, pz + r * 2.2), m=glass, verts=16)
        for j in range(2):
            bb = L.sphere("Bubble", 0.045, (px, by - 0.02, pz + 0.6), m=liquids[k], segs=10)
            bubbles.append((bb, px, by, pz + 0.3, 0.9 + j * 0.35, k * 0.37 + j * 0.5))

    # right: big planet model (orrery) with orbiting planets
    ox, oy = 4.8, 2.4
    L.cylinder("OrreryBase", 0.7, 0.25, (ox, oy, 0.13), m=pink, verts=32)
    L.cylinder("OrreryPole", 0.07, 1.6, (ox, oy, 1.0), m=steel, verts=16)
    sun = L.sphere("OrrerySun", 0.38, (ox, oy, 1.95), m=L.mat("OrrerySunMat", "#ffcc33", 0.4, emission="#ffb627", emit=4.0), segs=32)
    orrery = L.empty("Orrery", (ox, oy, 1.95))
    orb = []
    for k, (rad, r, c) in enumerate(((0.7, 0.09, "#c1440e"), (1.05, 0.13, "#2f6fd6"), (1.45, 0.2, "#e3a857"))):
        arm = L.empty(f"OrbArm{k}", (0, 0, 0), orrery)
        L.cylinder("OrbRod", 0.015, rad, (rad / 2, 0, 0), m=steel, parent=arm, rot=(0, math.pi / 2, 0), verts=8)
        L.sphere("OrbPlanet", r, (rad, 0, 0), m=L.mat(f"OrbP{k}", c, 0.35, coat=0.6), parent=arm, segs=20)
        L.torus("OrbTrack", rad, 0.008, (0, 0, 0), m=L.mat("Track", "#ffffff", 0.3, emission="#ffffff", emit=0.6), parent=orrery)
        orb.append((arm, 1.2 / (k + 1)))
    # tall glowing globe on the right floor
    globe = L.sphere("Globe", 0.55, (3.2, 3.9, 2.1), m=_banded(L, "GlobeMat", ("#2f6fd6", "#3fbf5f", "#ffffff"), 2.2, "land"), segs=40)
    L.cylinder("GlobeStand", 0.06, 1.5, (3.2, 3.9, 0.75), m=steel, verts=12)
    L.torus("GlobeArc", 0.66, 0.03, (3.2, 3.9, 2.1), m=trim, rot=(math.pi / 2, 0.4, 0))

    # floating mini planets (mobile) up high
    mobile = []
    for k, (x, z, r, c) in enumerate(((-3.0, 5.6, 0.32, "#ff7a45"), (-1.2, 6.0, 0.22, "#ffd23f"), (1.6, 5.8, 0.28, "#7ce0ff"), (3.4, 5.5, 0.2, "#c77dff"))):
        mobile.append((L.sphere("MobilePlanet", r, (x, 3.6, z), m=L.mat(f"Mob{k}", c, 0.3, coat=0.8), segs=20), z, k))

    # foreground: control console bottom-left, tall flask bottom-right (out of focus, adds depth)
    L.cube("Console", 1, (-3.6, -5.6, 0.55), (1.8, 1.0, 1.1), pink, bevel=0.12, segs=3, rot=(0, 0, 0.35))
    btns = []
    for k, (dx, c) in enumerate(((-0.5, "#ffd23f"), (0, "#4dff9a"), (0.5, "#4dc3ff"))):
        btns.append(L.sphere("Button", 0.13, (-3.6 + dx * 0.94, -5.6 + dx * 0.34, 1.13), (1, 1, 0.5), bulbs[(k + 1) % 4], segs=16))
    L.cylinder("Stool", 0.45, 0.9, (4.0, -5.0, 0.45), m=trim, verts=32)
    L.sphere("BigFlask", 0.5, (4.0, -5.0, 1.4), m=glass, segs=32)
    L.sphere("BigFlaskLiq", 0.43, (4.0, -5.0, 1.33), (1, 1, 0.8), liquids[2], segs=32)
    L.cylinder("BigFlaskNeck", 0.14, 0.5, (4.0, -5.0, 2.05), m=glass, verts=16)

    return {
        "spots": {"center": (0, 0, 0), "left": (-2.4, -0.4, 0), "right": (2.4, -0.4, 0), "back": (0, 2.0, 0)},
        "cams": {"wide": ((0.5, -9.4, 2.75), (0, 0.6, 1.75)), "center": (0, 0, 1.4), "orbit_r": 8.5,
                 "window": ((-1.8, -6.5, 1.6), (0.6, 4, 2.6)), "bench": ((-1.8, -3.4, 2.2), (-3.8, 2.2, 1.3)),
                 "orrery": ((2.0, -2.8, 2.3), (4.4, 2.4, 1.8))},
        "prop_spots": {"top": (0, 1.2, 3.45), "left": (-3.6, 0.8, 2.3), "right": (3.6, 0.8, 2.3), "front": (0, -2.0, 0.9)},
        "exposure": 0.0, "look": "AgX - Punchy",
        "_anim": dict(big=big, ring=ring, bulbs=bulbs, gears=gears, screens=screens, bubbles=bubbles, orrery=orrery,
                      orb=orb, sun=sun, globe=globe, mobile=mobile, btns=btns),
    }


def animate(L, SET, f, t, s):
    A = SET["_anim"]; beat = s.get("beat", 0); e = s.get("energy", 0.5)
    on = int(t * 112 / 60) % 2      # beat parity (song bpm; close enough for blinking)
    pulse = max(0.0, 1 - beat * 2.5)
    for i, m in enumerate(A["bulbs"]):
        _bsdf(m).inputs["Emission Strength"].default_value = (1.0 + 5.0 * pulse * e) if (i % 2) == on else 0.6
    for o, sp in A["gears"]:
        o.rotation_euler = (math.pi / 2, t * 0.6 * sp, 0)
    for k, (o, z) in enumerate(((A["big"]["ringed"], 0), (A["big"]["blue"], 0), (A["globe"], 0))):
        o.rotation_euler.z = t * (0.15 + 0.1 * k)
    A["orrery"].rotation_euler.z = t * 0.2
    for arm, sp in A["orb"]:
        arm.rotation_euler.z = t * sp
    A["sun"].scale = (1 + 0.06 * pulse,) * 3
    for o, z, k in A["mobile"]:
        o.location.z = z + math.sin(t * 1.3 + k) * 0.12
    for bb, px, py, z0, sp, ph in A["bubbles"]:
        u = (t * sp * 0.6 + ph) % 1.0
        bb.location = (px + math.sin(t * 5 + ph * 7) * 0.03, py - 0.02, z0 + u * 0.75)
        bb.scale = (min(1.0, (1 - u) * 3),) * 3
    for sc in A["screens"]:
        m = sc.data.materials[0]
        _bsdf(m).inputs["Emission Strength"].default_value = 1.6 + 1.2 * pulse * e


# ---------------------------------------------------------------- teaching props
PLANETS = {
    "mercury": (0.5, ("#8d8a86", "#b5b0aa", "#6e6b68"), "noise", 4.0),
    "venus":   (0.62, ("#e8c77a", "#f3dba0", "#d8a95a"), "bands", 2.0),
    "earth":   (0.65, ("#2f6fd6", "#3fbf5f", "#ffffff"), "land", 2.2),
    "mars":    (0.55, ("#c1440e", "#e2723a", "#9b3209"), "noise", 3.0),
    "jupiter": (1.0, ("#e6c39a", "#c98a4b", "#f6e6cf", "#b5703c"), "bands", 2.6),
    "saturn":  (0.85, ("#f2d27a", "#e0b25c", "#fff0c2"), "bands", 2.4),
    "uranus":  (0.72, ("#a8eef0", "#8fdde3", "#c5f6f6"), "bands", 1.2),
    "neptune": (0.7, ("#3f5fe0", "#2b44c9", "#6c8cff"), "bands", 1.6),
    "moon":    (0.45, ("#cfcfcf", "#e6e6e6", "#a8a8a8"), "noise", 4.0),
}


def _face(L, parent, r, y=-1.0):
    """Cute simple face on a prop: glossy oval eyes with catchlights, a smile, pink cheeks."""
    eye = L.mat("PropEye", "#1c1530", 0.25, coat=1.0)
    glint = L.mat("PropGlint", (1, 1, 1), 0.0, emission=(1, 1, 1), emit=3.0)
    cheek = L.mat("PropCheek", "#ff8fb0", 0.6)
    for sx in (-1, 1):
        L.sphere("PEye", r * 0.13, (r * 0.3 * sx, -r * 0.93, r * 0.14), (0.8, 0.5, 1.1), eye, parent, 16)
        L.sphere("PGlint", r * 0.045, (r * 0.3 * sx + r * 0.04, -r * 0.99, r * 0.2), (1, 0.5, 1), glint, parent, 8)
        L.sphere("PCheek", r * 0.09, (r * 0.52 * sx, -r * 0.82, -r * 0.08), (1, 0.4, 0.7), cheek, parent, 10)
    sm = L.torus("PSmile", r * 0.14, r * 0.03, (0, -r * 0.95, -r * 0.08), (1, 1, 1), eye, parent, (math.pi / 2 - 0.25, 0, 0))
    bm = bmesh.new(); bm.from_mesh(sm.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0.0], context="VERTS"); bm.to_mesh(sm.data); bm.free()


def prop(L, name, at, size=1.0, face=True, **_):
    name = name.lower()
    root = L.empty("Prop_" + name, at)
    root.scale = (size,) * 3
    if name in PLANETS:
        r, cols, mode, sc = PLANETS[name]
        L.sphere("PPlanet", r, (0, 0, 0), m=_banded(L, "PlanetMat_" + name, cols, sc, mode), parent=root, segs=48)
        if name == "jupiter":
            L.sphere("PSpot", r * 0.2, (-r * 0.5, -r * 0.7, -r * 0.5), (1.5, 0.3, 0.75), L.mat("RedSpot", "#b5462e", 0.5), root, 20)  # lower-left, away from the smile
        if name == "saturn":
            L.torus("PRing", r * 1.6, r * 0.35, (0, 0, 0), (1, 1, 0.05), L.mat("SatRing", "#f5deb0", 0.45, coat=0.4), root, (0.35, 0.15, 0))
        if name == "uranus":
            L.torus("PRingU", r * 1.4, r * 0.03, (0, 0, 0), (1, 1, 1), L.mat("URing", "#e0ffff", 0.4, emission="#e0ffff", emit=0.5), root, (0.2, 1.35, 0))
        if face and name != "moon":
            _face(L, root, r)
    elif name == "sun":
        r = 1.0
        L.sphere("PSun", r, m=_banded(L, "SunMat", ("#ffb627", "#ffd23f", "#ff8c1a"), 3.0, "noise", emit=3.5), parent=root, segs=48)
        rays = L.mat("SunRay", "#ffd23f", 0.4, emission="#ffcc33", emit=3.0)
        for k in range(10):
            a = k / 10 * math.tau
            L.cone("PRay", 0.16, 0.0, 0.42, (math.cos(a) * 1.22, 0.05, math.sin(a) * 1.22), m=rays, parent=root,
                   rot=(0, math.pi / 2 - a, 0), verts=12)
        if face: _face(L, root, r)
    elif name == "raincloud":
        cl = L.mat("Cloud", "#ffffff", 0.7, sheen=0.6)
        for x, z, r in ((-0.5, 0, 0.45), (0.05, 0.2, 0.6), (0.6, 0, 0.42), (0.1, -0.15, 0.5)):
            L.sphere("PCloud", r, (x, 0, z), (1, 0.8, 0.85), cl, root, 24)
        drop = L.mat("Drop", "#3db8ff", 0.1, coat=1.0)
        for k, x in enumerate((-0.45, 0.05, 0.5)):
            L.sphere("PDrop", 0.1, (x, 0, -0.75 - 0.15 * (k % 2)), (1, 1, 1.5), drop, root, 12)
        if face: _face(L, root, 0.6)
    elif name == "lightbulb":
        bulb = L.mat("BulbGlass", "#fff6a8", 0.15, emission="#fff09a", emit=4.0)
        L.sphere("PBulb", 0.55, (0, 0, 0.25), m=bulb, parent=root, segs=40)
        L.cone("PBulbNeck", 0.36, 0.24, 0.35, (0, 0, -0.3), m=bulb, parent=root, verts=32)
        base = L.mat("BulbBase", "#b9c2d0", 0.25, metal=0.8)
        for k in range(3):
            L.torus("PBulbScrew", 0.23, 0.04, (0, 0, -0.55 - k * 0.09), m=base, parent=root)
        L.sphere("PBulbTip", 0.1, (0, 0, -0.82), m=base, parent=root, segs=12)
    elif name == "magnet":
        red = L.mat("MagRed", "#e53935", 0.3, coat=0.8); sil = L.mat("MagTip", "#dfe6ee", 0.2, metal=0.8)
        arc = L.torus("PMagArc", 0.5, 0.18, (0, 0, 0.2), (1, 1, 1), red, root, (math.pi / 2, 0, 0))
        bm = bmesh.new(); bm.from_mesh(arc.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y < -0.01], context="VERTS"); bm.to_mesh(arc.data); bm.free()
        for sx in (-1, 1):
            L.cylinder("PMagLeg", 0.18, 0.5, (0.5 * sx, 0, -0.05), m=red, parent=root, verts=24)
            L.cylinder("PMagEnd", 0.185, 0.22, (0.5 * sx, 0, -0.4), m=sil, parent=root, verts=24)
    elif name == "gear":
        gear_mesh(L, "PGear", 0.8, 10, 0.25, L.mat("PGearMat", "#ffb703", 0.3, coat=0.8), (0, 0.12, 0), parent=root)
    elif name == "rocket":
        body = L.mat("RocketBody", "#f6f8ff", 0.25, coat=1.0); red = L.mat("RocketRed", "#ff4d6d", 0.3, coat=1.0)
        L.cylinder("PRocket", 0.32, 1.1, (0, 0, 0), m=body, parent=root, verts=32)
        L.cone("PNose", 0.32, 0.0, 0.55, (0, 0, 0.82), m=red, parent=root, verts=32)
        L.sphere("PPort", 0.14, (0, -0.28, 0.2), (1, 0.4, 1), L.mat("Port", "#5ff3ff", 0.1, emission="#5ff3ff", emit=1.5), root, 16)
        for k in range(3):
            a = k / 3 * math.tau + math.pi / 2
            L.cube("PFin", 1, (math.cos(a) * 0.36, math.sin(a) * 0.36, -0.42), (0.08, 0.3, 0.4), red, root, (0, 0, a), bevel=0.03)
        L.cone("PFlame", 0.2, 0.0, 0.5, (0, 0, -0.8), m=L.mat("RFlame", "#ffb627", 0.4, emission="#ff9a1c", emit=5.0), parent=root, rot=(math.pi, 0, 0), verts=16)
    elif name == "star":
        from chars.gizmo import star_mesh
        star_mesh("PStar", 0.8, 0.36, 0.25, L.mat("PStarMat", "#ffd23f", 0.3, emission="#ffcc33", emit=1.5), root, (0, 0.12, 0))
    elif name == "beaker":
        L.cylinder("PBeaker", 0.4, 0.9, (0, 0, 0), m=_glass(L, "LabGlass"), parent=root, verts=32)
        L.cylinder("PBeakLiq", 0.35, 0.55, (0, 0, -0.15), m=L.mat("PLiquid", "#3dff8b", 0.2, emission="#3dff8b", emit=0.8), parent=root, verts=32)
    else:
        L.sphere("PUnknown", 0.5, m=L.mat("PUnknown", "#ff5fa2", 0.3, coat=0.8), parent=root)
    return root
