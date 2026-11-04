"""Moonbeam Bedtime home set: a cozy moonlit kids' bedroom. Big window onto a starry sky with a crescent moon,
a bed with a patchwork quilt, a moon night-light, a slowly spinning star mobile, fairy lights, soft rug and toys.
Lighting is purple/blue moonlight plus warm gold practicals, with soft front fills so faces always read."""
import math
from mathutils import Vector
import mbkit as K

_twinkle = []   # (obj, base_scale, phase, speed) for stars created by prop() too


def _aim(o, target):
    d = Vector(target) - Vector(o.location)
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return o


def build(L, rng, **opts):
    _twinkle.clear()
    # ---- world: deep starry blue (also a soft blue ambient bounce in the room)
    w = L.sky("#202a72", 0.55, nishita=False)
    # ---- lights
    key = _aim(L.light("MB_Key", "AREA", 520, (-4.5, -7.5, 6.0), color=(1.0, 0.84, 0.8), size=6), (0, 0.5, 1.4))
    fill = _aim(L.light("MB_Fill", "AREA", 260, (5.5, -6.5, 3.2), color=(0.78, 0.8, 1.0), size=7), (0, 0.5, 1.3))
    face = _aim(L.light("MB_FaceFill", "AREA", 140, (0.5, -5.0, 1.8), color=(1.0, 0.9, 0.85), size=3), (0, 0.5, 1.5))
    rim = _aim(L.light("MB_MoonRim", "AREA", 700, (0.5, 5.5, 5.4), color=(0.62, 0.72, 1.0), size=5), (0, 0, 1.0))
    top = _aim(L.light("MB_Ceiling", "AREA", 90, (0, 0.5, 6.2), color=(0.85, 0.78, 1.0), size=8), (0, 0.5, 0))
    lamp = L.light("MB_NightLight", "POINT", 90, (-4.4, 3.4, 1.75), color=(1.0, 0.78, 0.45)); lamp.data.shadow_soft_size = 0.5
    bedl = L.light("MB_BedGlow", "POINT", 45, (4.2, 1.2, 2.6), color=(1.0, 0.82, 0.55)); bedl.data.shadow_soft_size = 0.8

    # ---- room shell
    wood = K.pattern_mat("MB_Floor", "#b57b52", "#a46d47", "stripes", 1.3, 0.55, 0.2, axis="X")
    L.cube("MB_FloorSlab", 1, (0, -2, -0.05), (18, 20, 0.1), wood)
    wall_up = K.pattern_mat("MB_WallUp", "#5a60b8", "#757bd0", "dots", 1.6, 0.85, 0.3)
    wall_lo = L.mat("MB_WallLow", "#a497e0", 0.8, sheen=0.3)
    trim = L.mat("MB_Trim", "#fff3dc", 0.45, coat=0.3)
    by = 4.6
    # back wall with a big window hole: x -2.6..2.6, z 1.5..5.6
    for nm, cx, sx_, cz, sz in (("L", -5.6, 6.0, 3.6, 7.2), ("R", 5.6, 6.0, 3.6, 7.2), ("T", 0, 5.2, 6.6, 2.0), ("B", 0, 5.2, 0.75, 1.5)):
        L.cube("MB_Wall" + nm, 1, (cx, by + 0.15, cz), (sx_, 0.3, sz), wall_up)
    L.cube("MB_WainL", 1, (-5.6, by - 0.02, 0.7), (6.0, 0.06, 1.4), wall_lo)
    L.cube("MB_WainR", 1, (5.6, by - 0.02, 0.7), (6.0, 0.06, 1.4), wall_lo)
    L.cube("MB_WainB", 1, (0, by - 0.02, 0.7), (5.2, 0.06, 1.4), wall_lo)
    L.cube("MB_Rail", 1, (0, by - 0.07, 1.42), (17, 0.1, 0.08), trim, bevel=0.03)
    L.cube("MB_Skirt", 1, (0, by - 0.07, 0.08), (17, 0.1, 0.16), trim, bevel=0.03)
    for sx in (-1, 1):   # side walls angled open a little so the wide shot feels like a cozy nook
        sw = L.cube(f"MB_Side{sx}", 1, (8.4 * sx, -1.0, 3.6), (0.3, 12, 7.2), wall_up, rot=(0, 0, -0.18 * sx))
    L.cube("MB_Ceiling", 1, (0, -1, 7.25), (18, 14, 0.2), L.mat("MB_CeilingM", "#3e4597", 0.9))
    # window frame + sill + mullions
    fr = L.mat("MB_Frame", "#fff6e6", 0.4, coat=0.4)
    L.cube("MB_FrL", 1, (-2.65, by - 0.05, 3.55), (0.22, 0.4, 4.3), fr, bevel=0.06)
    L.cube("MB_FrR", 1, (2.65, by - 0.05, 3.55), (0.22, 0.4, 4.3), fr, bevel=0.06)
    L.cube("MB_FrT", 1, (0, by - 0.05, 5.65), (5.5, 0.4, 0.22), fr, bevel=0.06)
    L.cube("MB_Sill", 1, (0, by - 0.25, 1.45), (6.0, 0.8, 0.18), fr, bevel=0.06)
    L.cube("MB_MulV", 1, (0, by + 0.05, 3.55), (0.09, 0.08, 4.1), fr, bevel=0.03)
    L.cube("MB_MulH", 1, (0, by + 0.0, 3.9), (5.2, 0.07, 0.09), fr, bevel=0.03)
    # curtains (soft folds) with tie-backs
    cur = L.mat("MB_Curtain", "#b48be0", 0.85, sheen=1.0, sss=0.05)
    tie = L.mat("MB_Tie", "#ffd36b", 0.4, coat=0.3)
    for sx in (-1, 1):
        for k in range(4):
            x = sx * (2.75 + k * 0.28)
            L.sphere(f"MB_Cur{sx}{k}", 0.24, (x, by - 0.35 - (k % 2) * 0.06, 3.5), (0.7, 0.5, 8.2), cur, segs=20)
        L.torus(f"MB_TieB{sx}", 0.42, 0.05, (sx * 3.15, by - 0.4, 2.6), (1, 0.6, 0.25), tie)
    L.cylinder("MB_Rod", 0.05, 8.4, (0, by - 0.4, 5.95), m=tie, rot=(0, math.pi / 2, 0), verts=16)

    # ---- outside: night sky, hills, crescent moon, stars, soft clouds
    sky_m = L.mat("MB_SkyBack", "#1a2366", 1.0, emission="#2b3a9a", emit=0.9)
    L.cube("MB_SkyCard", 1, (0, 18, 6), (40, 0.2, 24), sky_m)
    glow_m = L.mat("MB_Horizon", "#5a4fb0", 1.0, emission="#7a62c8", emit=0.9)
    L.sphere("MB_HorizonGlow", 1, (0, 17.6, 0.5), (22, 0.3, 3.2), glow_m, segs=24)
    hill = L.mat("MB_Hill", "#22306e", 0.9, emission="#2a3a80", emit=0.25)
    for k, (x, z, r) in enumerate(((-4.5, -2.2, 4.6), (2.0, -3.0, 5.4), (7.5, -2.6, 4.8))):
        L.sphere(f"MB_Hill{k}", r, (x, 13.5, z), (1.4, 0.4, 1), hill, segs=32)
    moon_m = L.mat("MB_Moon", "#fff3c4", 0.4, emission="#ffeeb0", emit=4.0)
    moon = K.curve_shape(L, "MB_BigMoon", K.crescent_pts(1.25, 0.8, 0.42), 0.25, 0.12, moon_m, None, (2.3, 14.5, 6.1), (math.pi / 2, 0, 0.35))
    halo = L.mat("MB_MoonHalo", "#a99cf0", 1.0, emission="#c8bcff", emit=0.6, alpha=0.25)
    L.sphere("MB_MoonHaloS", 2.0, (2.0, 14.9, 6.1), (1, 0.05, 1), halo, segs=32)
    star_m = L.mat("MB_Star", "#fff6c8", 0.4, emission="#ffe9a0", emit=5.0)
    stars = []
    for i in range(22):
        x = -6 + rng.random() * 11; z = 2.0 + rng.random() * 8.5
        if (x - 2.3) ** 2 + (z - 6.1) ** 2 < 4.0: continue
        r = 0.09 + rng.random() * 0.16
        o = K.curve_shape(L, "MB_SkyStar", K.star_pts(r, 0.45), 0.03, 0.02, star_m, None, (x, 15.5, z), (math.pi / 2, 0, rng.random()))
        stars.append((o, tuple(o.scale), rng.random() * 6.28, 1.2 + rng.random() * 1.6))
    cloud_m = L.mat("MB_Cloud", "#8c7fd6", 0.9, emission="#9d90e6", emit=0.5)
    for k, (x, z) in enumerate(((-3.5, 3.6), (-2.8, 3.8), (-4.2, 3.5), (5.0, 3.0), (5.7, 3.2))):
        L.sphere(f"MB_Cloud{k}", 0.7, (x, 14.0, z), (1.5, 0.4, 0.8), cloud_m, segs=20)

    # ---- glow-in-the-dark star stickers on the wall + fairy lights
    sticker = L.mat("MB_Sticker", "#fff2b3", 0.5, emission="#ffe48a", emit=1.2)
    for k, (x, z, r) in enumerate(((-4.2, 5.4, 0.22), (-6.1, 4.3, 0.16), (-3.6, 3.8, 0.13), (4.0, 5.7, 0.2), (6.3, 4.8, 0.15), (3.6, 4.2, 0.12), (-7.0, 6.2, 0.18))):
        o = K.curve_shape(L, "MB_Sticker", K.star_pts(r, 0.47), 0.01, 0.012, sticker, None, (x, by - 0.03, z), (math.pi / 2, 0, k * 0.4))
        stars.append((o, tuple(o.scale), k * 1.3, 0.7))
    K.curve_shape(L, "MB_WallMoon", K.crescent_pts(0.3), 0.01, 0.015, sticker, None, (-5.2, by - 0.03, 4.9), (math.pi / 2, 0, 0.4))
    bulbs = [L.mat("MB_BulbG", "#ffd27a", 0.3, emission="#ffcf6e", emit=6.0), L.mat("MB_BulbP", "#ffb3d1", 0.3, emission="#ffa8cc", emit=5.0),
             L.mat("MB_BulbB", "#b9c8ff", 0.3, emission="#a9bcff", emit=5.0)]
    wire = L.mat("MB_Wire", "#3a3f7a", 0.6)
    for seg in range(2):
        x0 = -7.6 if seg == 0 else 0.4
        for k in range(10):
            u = k / 9; x = x0 + u * 7.2; z = 6.55 - math.sin(u * math.pi) * 0.55
            L.sphere("MB_Bulb", 0.07, (x, by - 0.12, z), (1, 1, 1.3), bulbs[(k + seg) % 3], segs=12)

    # ---- rug
    L.cylinder("MB_Rug", 3.5, 0.04, (0, 0.5, 0.02), (1.25, 0.9, 1), L.mat("MB_RugM", "#c486c9", 0.95, sheen=1.0, bump=0.2, bump_scale=80), verts=48)
    L.torus("MB_RugRim", 3.5, 0.07, (0, 0.5, 0.04), (1.25, 0.9, 0.4), L.mat("MB_RugRimM", "#fff1d6", 0.95, sheen=1.0))

    # ---- bed (right, against the back wall) with patchwork quilt + pillows
    bw = L.mat("MB_BedWood", "#f2e2cf", 0.45, coat=0.3)
    bx, byy = 5.6, 2.6
    L.cube("MB_BedBase", 1, (bx, byy, 0.42), (2.6, 3.6, 0.5), bw, bevel=0.1)
    L.cube("MB_Headboard", 1, (bx, byy + 1.85, 1.2), (2.8, 0.22, 2.0), bw, bevel=0.12)
    L.cylinder("MB_HeadArch", 1.4, 0.22, (bx, byy + 1.85, 2.2), (1, 1, 0.45), m=bw, rot=(math.pi / 2, 0, 0), verts=40)
    K.curve_shape(L, "MB_HeadStar", K.star_pts(0.35, 0.48), 0.04, 0.03, L.mat("MB_HeadStarM", "#ffd36b", 0.35, coat=0.5, emission="#ffc94d", emit=0.6), None, (bx, byy + 1.72, 2.25), (math.pi / 2, 0, 0))
    L.cube("MB_Mattress", 1, (bx, byy, 0.82), (2.45, 3.4, 0.36), L.mat("MB_Sheet", "#fdf6ff", 0.8, sheen=0.8), bevel=0.15)
    quilt = K.pattern_mat("MB_Quilt", "#9fb6ff", "#ffc0dc", "checker", 2.2, 0.85, 1.0)
    L.cube("MB_Quilt", 1, (bx, byy - 0.45, 1.03), (2.65, 2.5, 0.16), quilt, bevel=0.07)
    L.cube("MB_QuiltFold", 1, (bx, byy + 0.75, 1.08), (2.6, 0.4, 0.2), L.mat("MB_QuiltFoldM", "#fff3d6", 0.85, sheen=1.0), bevel=0.09)
    pil = L.mat("MB_Pillow", "#ffffff", 0.75, sheen=1.0)
    for k, x in enumerate((-0.6, 0.6)):
        L.sphere(f"MB_Pillow{k}", 0.5, (bx + x, byy + 1.35, 1.18), (1.1, 0.5, 0.35), pil, segs=24)

    # ---- mobile above the bed (spins slowly in animate)
    mob = L.empty("MB_Mobile", (bx - 0.4, byy - 0.2, 5.3))
    L.cylinder("MB_MobString", 0.012, 1.9, (bx - 0.4, byy - 0.2, 6.25), m=wire, verts=6)
    L.torus("MB_MobRing", 0.75, 0.035, (0, 0, 0), m=tie, parent=mob)
    hang_m = [L.mat("MB_MobStar", "#ffd36b", 0.35, coat=0.5, emission="#ffc94d", emit=0.8), L.mat("MB_MobMoon", "#fff3c4", 0.35, emission="#ffeeb0", emit=0.9),
              L.mat("MB_MobCloud", "#c9b8ff", 0.6, sheen=0.8), L.mat("MB_MobPink", "#ffb3d1", 0.5, sheen=0.8)]
    hangers = []
    for k in range(5):
        a = k / 5 * math.tau; hx, hy = math.cos(a) * 0.75, math.sin(a) * 0.75; drop = 0.45 + (k % 2) * 0.3
        L.cylinder("MB_MobLine", 0.008, drop, (hx, hy, -drop / 2), m=wire, parent=mob, verts=6)
        h = L.empty("MB_MobH", (hx, hy, -drop - 0.15), mob)
        if k % 4 == 0 or k == 3:
            K.curve_shape(L, "MB_MobItem", K.star_pts(0.2, 0.5), 0.05, 0.03, hang_m[0], h, (0, 0, 0), (math.pi / 2, 0, 0))
        elif k == 1:
            K.curve_shape(L, "MB_MobItem", K.crescent_pts(0.2), 0.05, 0.03, hang_m[1], h, (0, 0, 0), (math.pi / 2, 0, 0))
        else:
            for dx, r in ((-0.1, 0.11), (0.05, 0.14), (0.17, 0.1)):
                L.sphere("MB_MobPuff", r, (dx, 0, 0), m=hang_m[2] if k == 2 else hang_m[3], parent=h, segs=14)
        hangers.append((h, k))

    # ---- nightstand + moon night-light (left)
    L.cube("MB_Stand", 1, (-4.4, 3.6, 0.55), (1.2, 0.9, 1.1), bw, bevel=0.08)
    L.cube("MB_Drawer", 1, (-4.4, 3.13, 0.6), (0.9, 0.04, 0.4), L.mat("MB_DrawerM", "#c7b5ff", 0.5, coat=0.3), bevel=0.02)
    L.sphere("MB_Knob", 0.05, (-4.4, 3.09, 0.6), m=tie, segs=12)
    nl_m = L.mat("MB_NightLightM", "#ffe6a8", 0.3, emission="#ffd27a", emit=6.0)
    nl = L.sphere("MB_NightLightBall", 0.3, (-4.4, 3.55, 1.42), m=nl_m, segs=32)
    L.cylinder("MB_NLBase", 0.22, 0.12, (-4.4, 3.55, 1.16), m=L.mat("MB_NLBaseM", "#8f7fe0", 0.4, coat=0.4), verts=24)
    K.curve_shape(L, "MB_NLMoon", K.crescent_pts(0.18), 0.03, 0.02, sticker, None, (-4.4, 3.22, 1.45), (math.pi / 2, 0, 0.3))

    # ---- toys + books (foreground/midground depth)
    blocks = [L.mat("MB_Blk0", "#ff9fb8", 0.4, coat=0.5), L.mat("MB_Blk1", "#9fd3ff", 0.4, coat=0.5), L.mat("MB_Blk2", "#ffe08a", 0.4, coat=0.5)]
    for k, (x, y, z, rz) in enumerate(((-6.1, 0.2, 0.25, 0.2), (-5.5, 0.4, 0.25, -0.3), (-5.8, 0.3, 0.75, 0.5))):
        L.cube("MB_Block", 0.5, (x, y, z), m=blocks[k], rot=(0, 0, rz), bevel=0.06)
    L.sphere("MB_Ball", 0.35, (6.2, -0.9, 0.35), m=K.pattern_mat("MB_BallM", "#ffb3d1", "#fff3c4", "stripes", 3.0, 0.4, 0.2), segs=32, rot=(0.3, 0.2, 0))
    bk = [L.mat("MB_Bk0", "#7fb2ff", 0.6), L.mat("MB_Bk1", "#ffb07a", 0.6), L.mat("MB_Bk2", "#9be3b4", 0.6)]
    for k in range(3):
        L.cube("MB_Book", 1, (-6.6, 2.8 + k * 0.02, 0.1 + k * 0.17), (0.9 - k * 0.1, 0.65, 0.15), bk[k], rot=(0, 0, 0.2 * k - 0.2), bevel=0.02)
    # a small plush star pillow on the rug, front right (foreground depth)
    K.curve_shape(L, "MB_FloorStar", K.star_pts(0.42, 0.5), 0.16, 0.12, L.mat("MB_PlushStar", "#ffd36b", 0.8, sheen=1.0), None, (4.6, -2.2, 0.2), (0.25, 0, 0.3))

    return {
        "spots": {"center": (0, 0, 0), "left": (-2.5, 0.8, 0), "right": (2.5, 0.8, 0), "farleft": (-3.8, 1.9, 0),
                  "farright": (3.9, 0.2, 0), "back": (0, 2.0, 0)},
        "cams": {"wide": ((0.6, -10.5, 2.7), (0, 0.6, 1.5)), "center": (0, 0.4, 1.3), "orbit_r": 8.5,
                 "cozy": ((-0.6, -7.2, 2.0), (0, 0.5, 1.45)),
                 "window": ((-2.6, -2.0, 2.2), (0.6, 8.0, 4.6)),
                 "bed": ((1.6, -3.4, 2.4), (5.2, 2.4, 1.3)),
                 "mobile": ((2.4, -2.0, 1.6), (bx - 0.4, byy - 0.2, 4.6))},
        "prop_spots": {"top": (0, 1.6, 3.15), "left": (-3.0, 1.2, 3.0), "right": (3.0, 1.2, 3.0), "front": (0, -2.2, 0.9)},
        "exposure": -0.15, "look": "AgX - Punchy",
        "_stars": stars, "_mobile": mob, "_hangers": hangers, "_lamp": lamp, "_nl": nl,
    }


# ------------------------------------------------------------------ teaching props
def _root(L, name, at):
    return L.empty("MBP_" + name, at)


def prop(L, name, at, **opts):
    r = _root(L, name, at)
    gold = L.mat("MBP_Gold", "#ffd36b", 0.3, coat=0.6, emission="#ffc94d", emit=1.2)
    if name in ("star", "numstar"):
        s = opts.get("size", 0.5)
        st = K.curve_shape(L, "MBP_Star", K.star_pts(s, 0.5), 0.14, 0.1, gold, r, (0, 0, 0))
        _twinkle.append((st, tuple(st.scale), hash(name) % 7 * 0.9, 1.6))
        if name == "numstar" or "n" in opts:
            num = L.text3d("MBP_Num", str(opts.get("n", 1)), s * 0.95, (0, -0.2, -0.05), L.mat("MBP_NumM", "#5c4bb5", 0.35, coat=0.5), r, 0.06, 0.02)
    elif name == "moon":
        K.curve_shape(L, "MBP_Moon", K.crescent_pts(opts.get("size", 0.5)), 0.14, 0.1, L.mat("MBP_MoonM", "#ffe9a8", 0.35, coat=0.4, emission="#ffe08a", emit=0.5), r, (0, 0, 0), (math.pi / 2, 0, 0.35))
    elif name == "heart":
        K.curve_shape(L, "MBP_Heart", K.heart_pts(opts.get("size", 0.6)), 0.16, 0.12, L.mat("MBP_HeartM", "#ff8fb8", 0.35, coat=0.6, emission="#ff8fb8", emit=0.4), r)
    elif name == "toothbrush":
        r.rotation_euler = (0, 0.5, 0)
        h = L.mat("MBP_Brush", "#5ad1c8", 0.25, coat=0.8)
        L.cube("MBP_Handle", 1, (0, 0, 0), (1.5, 0.18, 0.2), h, r, bevel=0.08)
        L.cube("MBP_Neck", 1, (0.85, 0, 0.02), (0.3, 0.12, 0.13), h, r, bevel=0.05)
        L.cube("MBP_Bristles", 1, (1.05, 0, 0.17), (0.42, 0.18, 0.22), L.mat("MBP_Bristle", "#ffffff", 0.6, sheen=0.5), r, bevel=0.04)
        for k in range(3):
            L.sphere("MBP_Paste", 0.09 - k * 0.015, (1.0 + k * 0.05, 0, 0.33 + k * 0.08), m=L.mat("MBP_PasteM", "#b8f2e6", 0.3, coat=0.5), parent=r, segs=14)
        L.sphere("MBP_Grip", 0.1, (-0.4, -0.07, 0), (2.5, 0.6, 1), L.mat("MBP_GripM", "#ffd36b", 0.4), r, 16)
    elif name in ("pajamas", "pajama"):
        pm = K.pattern_mat("MBP_PJ", "#8fb8ff", "#ffffff", "stripes", 6.0, 0.8, 1.0)
        L.cube("MBP_Torso", 1, (0, 0, 0), (0.9, 0.3, 1.0), pm, r, bevel=0.15)
        for sx in (-1, 1):
            L.cylinder(f"MBP_Sleeve{sx}", 0.17, 0.6, (0.62 * sx, 0, 0.2), m=pm, parent=r, rot=(0, 0.9 * sx, 0), verts=20)
        L.torus("MBP_Collar", 0.2, 0.05, (0, -0.1, 0.45), (1, 0.6, 1), L.mat("MBP_Collar", "#ffffff", 0.7), r, (math.radians(70), 0, 0))
        for k in range(3):
            L.sphere("MBP_Btn", 0.05, (0, -0.16, 0.25 - k * 0.25), (1, 0.5, 1), gold, r, 12)
    elif name == "book":
        cv = L.mat("MBP_Cover", "#ff8fb8", 0.45, coat=0.4)
        pg = L.mat("MBP_Page", "#fffaf0", 0.8)
        for sx in (-1, 1):
            L.cube(f"MBP_Cov{sx}", 1, (0.42 * sx, 0, 0), (0.85, 0.06, 1.1), cv, r, rot=(0, 0, -0.25 * sx), bevel=0.03)
            L.cube(f"MBP_Pg{sx}", 1, (0.4 * sx, -0.06, 0), (0.78, 0.06, 1.02), pg, r, rot=(0, 0, -0.25 * sx), bevel=0.02)
        K.curve_shape(L, "MBP_BookStar", K.star_pts(0.18, 0.5), 0.02, 0.01, gold, r, (0.4, -0.2, 0.15), (math.pi / 2, 0, 0))
        K.curve_shape(L, "MBP_BookMoon", K.crescent_pts(0.17), 0.02, 0.01, gold, r, (-0.4, -0.2, 0.15), (math.pi / 2, 0, 0))
    elif name == "duck":
        y = L.mat("MBP_Duck", "#ffd23f", 0.25, coat=0.9)
        L.sphere("MBP_DuckBody", 0.45, (0, 0, 0), (1.25, 0.9, 0.8), y, r, 32)
        L.sphere("MBP_DuckHead", 0.28, (-0.25, 0, 0.45), m=y, parent=r, segs=28)
        L.sphere("MBP_DuckBeak", 0.12, (-0.5, -0.02, 0.4), (1.3, 0.8, 0.5), L.mat("MBP_DuckBeakM", "#ff9a3c", 0.3, coat=0.6), r, 16)
        L.sphere("MBP_DuckEye", 0.045, (-0.33, -0.22, 0.55), m=L.mat("Pupil", "#050303"), parent=r, segs=10)
    elif name == "bubbles":
        bm = L.mat("MBP_Bubble", "#cfe8ff", 0.05, coat=1.0, emission="#bfe0ff", emit=0.3, alpha=0.45)
        for k, (x, z, s) in enumerate(((0, 0, 0.35), (0.5, 0.35, 0.22), (-0.45, 0.3, 0.26), (0.2, 0.7, 0.16), (-0.15, -0.4, 0.18))):
            L.sphere("MBP_Bub", s, (x, 0, z), m=bm, parent=r, segs=24)
    elif name == "zzz":
        zm = L.mat("MBP_Z", "#c8bcff", 0.4, coat=0.4, emission="#c8bcff", emit=0.6)
        for k in range(3):
            L.text3d("MBP_Zt", "Z", 0.45 + k * 0.2, (k * 0.4, 0, k * 0.4), zm, r, 0.08, 0.02)
    else:   # fallback: a twinkly gold star
        st = K.curve_shape(L, "MBP_Star", K.star_pts(0.6, 0.5), 0.14, 0.1, gold, r)
        _twinkle.append((st, tuple(st.scale), 0.0, 1.6))
    return r


# ------------------------------------------------------------------ animation
def animate(L, SET, f, t, s):
    for o, bs, ph, sp in SET.get("_stars", []):
        k = 0.78 + 0.22 * math.sin(t * sp + ph)
        o.scale = (bs[0] * k, bs[1] * k, bs[2] * k)
    for o, bs, ph, sp in _twinkle:
        k = 1.0 + 0.06 * math.sin(t * sp * 2 + ph)
        o.scale = (bs[0] * k, bs[1] * k, bs[2] * k)
        o.rotation_euler.y = math.sin(t * 0.8 + ph) * 0.12
    mob = SET.get("_mobile")
    if mob is not None:
        mob.rotation_euler = (math.sin(t * 0.4) * 0.03, math.sin(t * 0.33) * 0.03, t * 0.35)
        for h, k in SET.get("_hangers", []):
            h.rotation_euler = (0, 0, math.sin(t * 0.9 + k) * 0.4 - t * 0.35)   # items keep facing the room
    lamp = SET.get("_lamp")
    if lamp is not None:
        lamp.data.energy = 90 * (0.92 + 0.08 * math.sin(t * 0.8))
