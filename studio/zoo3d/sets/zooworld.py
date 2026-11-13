"""Zoo World: one parametric 3D set with many biomes and times of day, so no two Animated Zoo episodes look alike
(Noelson, Nov 13, 2026: "each episode should have different images and theme").

job["set"] = "zooworld", job["set_opts"] = {"biome": "jungle", "tod": "morning", "seed": 4}
or, for scene changes inside one episode (the Google Vids principle: every part of the song gets a fresh place),
job["locations"] = [{"from": "chorus1", "biome": "jungle", "tod": "morning"}, {"from": "verse2", "biome": "river", ...}]
(see engine.py "locations").

Biomes: savanna, jungle, arctic, beach, farm, desert, autumn_forest, spring_meadow, river, mountain, bamboo, night_meadow
Times of day: morning, noon, golden, sunset, night
Spots (same layout in every biome, so casts work everywhere): center, lion, zebra, elephant, hippo, giraffe, left, right, back
plus s1..s6 aliases (s1 = left front ... s6 = back right).
"""
import math, os
import bpy, bmesh

FONT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts", "Poppins-Bold.ttf")

# --------------------------------------------------------------------------- palettes
BIOMES = {
    "savanna":       dict(ground=("#d9962a", "#f5c445"), stage="#eab066", grass=("#a8902a", "#ffe08a"), cover="grass",
                          trees=("acacia",), hills=("#d1a24a", "#c9a24f", "#c79a6a"), far="kili", flowers=("#ff7043", "#fff176", "#ffffff"),
                          water=False, fx=None),
    "jungle":        dict(ground=("#2f7d22", "#5ea82e"), stage="#c9a36a", grass=("#2a7a22", "#8fd14a"), cover="grass",
                          trees=("palm", "bigleaf", "round_jungle"), hills=("#2f8a4a", "#3c9a5a", "#4fa86c"), far="waterfall",
                          flowers=("#ff4f8b", "#ffcc00", "#ff7a1a"), water=False, fx="butterflies"),
    "arctic":        dict(ground=("#dfeaf6", "#ffffff"), stage="#eef6ff", grass=None, cover="snow",
                          trees=("snowpine",), hills=("#d8e6f5", "#c9dcf2", "#b9cfee"), far="icebergs", flowers=None,
                          water="ice", fx="snow"),
    "beach":         dict(ground=("#f0d49a", "#ffe9b8"), stage="#f7e0a8", grass=None, cover="shells",
                          trees=("palm",), hills=None, far="ocean", flowers=None, water="ocean", fx="bubbles"),
    "farm":          dict(ground=("#5aa83a", "#8fcf4f"), stage="#d9b27a", grass=("#4f9a30", "#a6dd5a"), cover="grass",
                          trees=("round_apple",), hills=("#7cc35a", "#6db54e", "#94c96a"), far="barn",
                          flowers=("#ffffff", "#ffe14f", "#ff8fb0"), water=False, fx="butterflies"),
    "desert":        dict(ground=("#e8a85a", "#f8cf7c"), stage="#f2c07a", grass=None, cover="pebbles",
                          trees=("cactus",), hills=("#eab06a", "#e39c5a", "#d98f6a"), far="mesa", flowers=("#ff6fa6", "#ffd23f"),
                          water=False, fx=None),
    "autumn_forest": dict(ground=("#8a6a3a", "#c49a52"), stage="#d6a86a", grass=("#9a7a30", "#e0b050"), cover="leaves",
                          trees=("round_autumn", "pine"), hills=("#c7783a", "#b8663a", "#a9884a"), far="hills",
                          flowers=("#ff8a3d", "#ffd23f", "#d9442b"), water=False, fx="leaves"),
    "spring_meadow": dict(ground=("#6cc04a", "#a8e06a"), stage="#e9d8a0", grass=("#5ab83c", "#b8ef6a"), cover="grass",
                          trees=("round_blossom",), hills=("#8fd06a", "#7cc35a", "#a9da7a"), far="rainbow",
                          flowers=("#ff6f9c", "#ffd23f", "#ffffff", "#b57cff", "#ff9f43"), water=False, fx="butterflies"),
    "river":         dict(ground=("#4f9a3a", "#86c44f"), stage="#d8c08a", grass=("#3f8a2a", "#9ad45a"), cover="grass",
                          trees=("round", "reeds"), hills=("#5aa24a", "#6aae5a", "#8ab98a"), far="hills", flowers=("#ffffff", "#ffd23f"),
                          water="river", fx="dragonflies"),
    "mountain":      dict(ground=("#6a9a4a", "#9cc46a"), stage="#cbb48a", grass=("#5a8a3a", "#a6c85a"), cover="rocks",
                          trees=("pine",), hills=("#7aa0c8", "#8aaed2", "#a9c2e2"), far="peaks", flowers=("#b57cff", "#ffffff", "#ffd23f"),
                          water=False, fx=None),
    "bamboo":        dict(ground=("#5a9a3a", "#8cc45a"), stage="#d2c28a", grass=("#4a8a2a", "#9ad45a"), cover="grass",
                          trees=("bamboo",), hills=("#6aa88a", "#7cb89a", "#9ac8b0"), far="hills", flowers=("#ff8fb0", "#ffffff"),
                          water=False, fx="petals"),
    "night_meadow":  dict(ground=("#3f7a4a", "#6aa860"), stage="#c8b890", grass=("#3a7040", "#7ab070"), cover="grass",
                          trees=("round",), hills=("#3a5a7a", "#33507a", "#2c4670"), far="hills", flowers=("#ffffff", "#ffe48a"),
                          water=False, fx="fireflies", force_tod="night"),
}

TOD = {   # sky bottom -> top, sun (energy, elevation deg, azimuth deg, color), fill color, exposure
    "morning": dict(sky=("#ffd6b0", "#ffe9cf", "#a9d8ff", "#5fb2f2"), sun=(4.0, 22, -60, (1.0, 0.86, 0.72)), fill=(1.0, 0.88, 0.85), exp=-0.25, sun_disc="#ffe0a0"),
    "noon":    dict(sky=("#dff2ff", "#bfe6ff", "#7cc3f5", "#2f8fe6"), sun=(4.6, 58, -25, (1.0, 0.96, 0.9)), fill=(0.95, 0.95, 1.0), exp=-0.35, sun_disc="#fff4b0"),
    "golden":  dict(sky=("#ffc978", "#ffe2a6", "#7cc3f5", "#1f7fe0"), sun=(4.6, 30, -28, (1.0, 0.86, 0.66)), fill=(1.0, 0.9, 0.8), exp=-0.3, sun_disc="#ffd84a"),
    "sunset":  dict(sky=("#ff8a5c", "#ffb37a", "#c99ad8", "#5a6ad0"), sun=(3.6, 10, 20, (1.0, 0.68, 0.48)), fill=(1.0, 0.78, 0.8), exp=-0.15, sun_disc="#ff9a5a"),
    "night":   dict(sky=("#3a4a8a", "#2a3a7a", "#1c2a62", "#121c4a"), sun=(1.6, 40, 30, (0.62, 0.72, 1.0)), fill=(0.7, 0.78, 1.0), exp=0.25, sun_disc=None),
}


def _hexmix(a, b, u, L):
    ca, cb = L.rgb(a), L.rgb(b)
    return tuple(ca[i] + (cb[i] - ca[i]) * u for i in range(3))


# --------------------------------------------------------------------------- sky + ground
def _world(L, name, stops):
    w = bpy.data.worlds.new(name); L.scene().world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    pos = (0.0, 0.05, 0.14, 0.42)
    cr.elements[0].position = pos[0]; cr.elements[0].color = (*L.rgb(stops[0]), 1)
    cr.elements[1].position = pos[3]; cr.elements[1].color = (*L.rgb(stops[3]), 1)
    for p, c in zip(pos[1:3], stops[1:3]):
        e = cr.elements.new(p); e.color = (*L.rgb(c), 1)
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 1.0
    return w


def _ramp_mat(L, name, c0, c1, scale=0.08, rough=0.9):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = rough
    tc = nt.nodes.new("ShaderNodeTexCoord"); n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale * 10
    nt.links.new(tc.outputs["Object"], n.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    cr.elements[0].position = 0.35; cr.elements[0].color = (*L.rgb(c0), 1)
    cr.elements[1].position = 0.65; cr.elements[1].color = (*L.rgb(c1), 1)
    nt.links.new(n.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.2
    nt.links.new(n.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def _grass(L, rng, mat, clear, n=560, keep_out=()):
    me = bpy.data.meshes.new("ZWGrass"); bm = bmesh.new()
    def tuft(x, y, h, k):
        for _ in range(k):
            ret = bmesh.ops.create_cone(bm, cap_ends=False, segments=4, radius1=0.035 + rng.random() * 0.02, radius2=0.0, depth=h * (0.6 + rng.random() * 0.6))
            d = h * 0.5; ax, ay = (rng.random() - 0.5) * 0.7, (rng.random() - 0.5) * 0.7
            for v in ret["verts"]:
                z = v.co.z + d
                v.co.x += x + (rng.random() - 0.5) * 0.25 + ax * z; v.co.y += y + (rng.random() - 0.5) * 0.25 + ay * z; v.co.z = z
    for _ in range(n):
        x = (rng.random() - 0.5) * 36; y = -7 + rng.random() ** 1.15 * 36
        if y < -2.2 and abs(x) < 4.5: continue
        cx, cy, rx, ry = clear
        if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1.0: continue
        if any(((x - a) / ra) ** 2 + ((y - b) / rb) ** 2 < 1.0 for a, b, ra, rb in keep_out): continue
        far = max(0.0, (y - 4) / 30)
        tuft(x, y, (0.4 + rng.random() * 0.4) * (1 + far * 0.8), 5 + int(rng.random() * 5))
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("ZWGrass", me); L.scene().collection.objects.link(o); o.data.materials.append(mat)
    return o


# --------------------------------------------------------------------------- trees and props
def _tree(L, rng, kind, x, y, s, k):
    bark = L.mat("ZWBark", "#6b4426", 0.9, bump=0.3, bump_scale=6)
    if kind == "acacia":
        leafs = [L.mat(f"ZWAcacia{i}", c, 0.75, sheen=0.3) for i, c in enumerate(("#6f9a2c", "#82ab36", "#5f8a26"))]
        L.cylinder("Trunk", 0.18 * s, 2.6 * s, (x, y, 1.3 * s), m=bark, verts=12)
        for j, (dx, dy, dz, r) in enumerate(((0, 0, 3.5, 1.6), (-1.3, 0.2, 3.3, 1.1), (1.35, -0.1, 3.35, 1.2))):
            L.sphere("Canopy", r * s, (x + dx * s, y + dy * s, dz * s), (1.35, 1.1, 0.33), leafs[(j + k) % 3], segs=20)
    elif kind == "palm":
        lean = (rng.random() - 0.5) * 0.4
        segs = 7
        for j in range(segs):
            u = j / segs
            L.cylinder("PalmSeg", (0.2 - 0.06 * u) * s, 0.62 * s, (x + math.sin(lean) * u * 3.6 * s, y, (0.3 + u * 3.9) * s),
                       m=L.mat("ZWPalmBark", "#a87a4a", 0.85, bump=0.4, bump_scale=10), rot=(0, lean * 0.8, 0), verts=10)
        tx, tz = x + math.sin(lean) * 3.6 * s, 4.3 * s
        leaf = L.mat(f"ZWPalmLeaf{k % 2}", ("#3fa83a", "#58c046")[k % 2], 0.6, sheen=0.3, sss=0.05)
        for j in range(8):
            a = j / 8 * math.tau
            L.sphere("Frond", 1.0, (tx + math.cos(a) * 1.0 * s, y + math.sin(a) * 1.0 * s, tz - 0.25 * s), (1.5 * s, 0.32 * s, 0.09 * s), leaf, segs=16, rot=(0.0, 0.35, a))
        for j in range(3):
            L.sphere("Coconut", 0.17 * s, (tx + (j - 1) * 0.2 * s, y - 0.15 * s, tz - 0.35 * s), m=L.mat("ZWCoco", "#7a5230", 0.6), segs=14)
    elif kind in ("pine", "snowpine"):
        green = L.mat("ZWPine", "#2f7a4a", 0.8, sheen=0.2)
        L.cylinder("Trunk", 0.15 * s, 1.0 * s, (x, y, 0.5 * s), m=bark, verts=10)
        for j, (z, r) in enumerate(((1.3, 1.3), (2.2, 1.0), (3.0, 0.7))):
            L.cone("PineTier", r * s, 0.05 * s, 1.3 * s, (x, y, z * s), m=green, verts=16)
            if kind == "snowpine":
                L.cone("Snow", r * 0.62 * s, 0.04 * s, 0.55 * s, (x, y, (z + 0.42) * s), m=L.mat("ZWSnow", "#ffffff", 0.7, sheen=0.3), verts=16)
    elif kind in ("round", "round_apple", "round_autumn", "round_blossom", "round_jungle"):
        cols = {"round": ("#4caf50", "#5cb85c", "#43a047"), "round_apple": ("#4caf50", "#5cb85c", "#43a047"),
                "round_autumn": ("#e8742a", "#f2b23a", "#d9442b"), "round_blossom": ("#ffb3cf", "#ffd1e3", "#ff9cc0"),
                "round_jungle": ("#2f9a3a", "#3fb04a", "#228a32")}[kind]
        leaf = L.mat(f"ZW{kind}{k % 3}", cols[k % 3], 0.7, sss=0.08, bump=0.2, bump_scale=3)
        L.cylinder("Trunk", 0.22 * s, 1.8 * s, (x, y, 0.9 * s), m=bark, verts=14)
        for dx, z, dy, r in ((0, 2.3, 0, 1.15), (0.6, 2.0, 0.2, 0.75), (-0.55, 2.1, -0.1, 0.8), (0.1, 2.95, 0.05, 0.8)):
            L.sphere("Leaf", r * s, (x + dx * s, y + dy * s, z * s), m=leaf, segs=22)
        if kind == "round_apple":
            for j in range(6):
                a = j / 6 * math.tau
                L.sphere("Apple", 0.12 * s, (x + math.cos(a) * 0.95 * s, y - 0.5 * s, (2.2 + 0.4 * math.sin(a * 2)) * s), m=L.mat("ZWApple", "#e8302a", 0.35, coat=0.6), segs=12)
    elif kind == "bigleaf":
        leaf = L.mat("ZWBigLeaf", "#2f9a3a", 0.6, sheen=0.3, sss=0.06)
        for j in range(5):
            a = j / 5 * math.tau + k
            L.sphere("BigLeaf", 1.0, (x + math.cos(a) * 0.7 * s, y + math.sin(a) * 0.7 * s, 0.7 * s), (0.9 * s, 0.35 * s, 0.06 * s), leaf, segs=16, rot=(0, -0.6, a))
    elif kind == "cactus":
        cm = L.mat("ZWCactus", "#4f9a4a", 0.6, sheen=0.3)
        L.cylinder("Cactus", 0.35 * s, 2.4 * s, (x, y, 1.2 * s), m=cm, verts=16)
        L.sphere("CactusTop", 0.35 * s, (x, y, 2.4 * s), m=cm, segs=16)
        for sx in (-1, 1):
            L.cylinder("CArm", 0.2 * s, 0.7 * s, (x + 0.55 * sx * s, y, 1.3 * s), m=cm, rot=(0, math.pi / 2, 0), verts=12)
            L.cylinder("CArmUp", 0.2 * s, 0.8 * s, (x + 0.85 * sx * s, y, 1.7 * s), m=cm, verts=12)
            L.sphere("CArmTop", 0.2 * s, (x + 0.85 * sx * s, y, 2.1 * s), m=cm, segs=12)
        L.sphere("CFlower", 0.14 * s, (x, y, 2.75 * s), m=L.mat("ZWCFlower", "#ff5fa2", 0.4, emission="#ff5fa2", emit=0.2), segs=12)
    elif kind == "bamboo":
        bm_ = L.mat("ZWBamboo", "#8cc04a", 0.5, coat=0.4)
        for j in range(4):
            bx, by, h = x + (j - 1.5) * 0.45 * s, y + (j % 2) * 0.3 * s, (4.2 + (j * 7 % 3) * 0.8) * s
            L.cylinder("Bamboo", 0.09 * s, h, (bx, by, h / 2), m=bm_, verts=10)
            for z in range(1, int(h / s)):
                L.torus("Node", 0.095 * s, 0.022 * s, (bx, by, z * s), m=L.mat("ZWBambooNode", "#6aa03a", 0.5))
            L.sphere("BLeaf", 1.0, (bx + 0.35 * s, by, h * 0.92), (0.55 * s, 0.12 * s, 0.05 * s), L.mat("ZWBambooLeaf", "#4caf50", 0.6), segs=12, rot=(0, -0.4, j))
    elif kind == "reeds":
        reed = L.mat("ZWReed", "#5d9a32", 0.7, sheen=0.3)
        for j in range(7):
            L.cone("Reed", 0.06 * s, 0.0, (0.9 + rng.random() * 0.6) * s, (x + (rng.random() - 0.5) * 1.2 * s, y + (rng.random() - 0.5) * 0.6 * s, 0.5 * s), m=reed, verts=6)
            L.cylinder("Cattail", 0.05 * s, 0.25 * s, (x + (j - 3) * 0.15 * s, y, 1.25 * s), m=L.mat("ZWCattail", "#7a4a26", 0.8), verts=8)


def _far(L, rng, kind, B):
    if B.get("hills"):
        for k, (x, y, sx, sz) in enumerate(((-30, 50, 26, 6), (8, 55, 30, 5), (38, 52, 24, 7))):
            L.sphere("Hill", 1.0, (x, y, 0), (sx, 10, sz), L.mat(f"ZWHill{B['hills'][k]}", B["hills"][k], 1.0), segs=32)
    if kind == "kili":
        L.cone("Kili", 30, 8, 14, (-17, 82, 3.0), (1, 0.4, 1), L.mat("ZWKili", "#7d78b8", 1.0), verts=40)
        L.cone("KiliSnow", 11.6, 8.0, 2.4, (-17, 81.5, 9.0), (1, 0.4, 1), L.mat("ZWSnowCap", "#ffffff", 0.8, emission="#f4f2ff", emit=0.3), verts=40)
    elif kind == "peaks":
        for k, (x, h, r) in enumerate(((-28, 26, 18), (-6, 34, 22), (20, 28, 18), (42, 22, 16))):
            L.cone("Peak", r, 0.5, h, (x, 85, h / 2 - 2), (1, 0.45, 1), L.mat("ZWPeak", "#7e8fb8", 1.0), verts=6, rot=(0, 0, k))
            L.cone("PeakSnow", r * 0.36, 0.3, h * 0.34, (x, 84.6, h - h * 0.17 - 2), (1, 0.45, 1), L.mat("ZWSnowCap", "#ffffff", 0.8, emission="#f4f2ff", emit=0.3), verts=6, rot=(0, 0, k))
    elif kind == "icebergs":
        ice = L.mat("ZWIceberg", "#cfe8ff", 0.25, coat=0.8, sss=0.2)
        for k, (x, y, s) in enumerate(((-26, 60, 7), (-6, 70, 9), (18, 62, 6), (36, 72, 8))):
            L.cone("Iceberg", s, s * 0.3, s * 1.1, (x, y, s * 0.4), (1.3, 0.8, 1), ice, verts=7, rot=(0, 0, k))
        L.cube("Sea", 1, (0, 75, -0.45), (240, 40, 1), L.mat("ZWSea", "#4aa8e0", 0.45, emission="#4aa8e0", emit=0.15))
    elif kind == "ocean":
        L.cube("Sea", 1, (0, 50, -0.42), (260, 70, 1), L.mat("ZWOcean", "#2fb4e0", 0.45, sheen=0.2, emission="#2fb4e0", emit=0.15))
        for k in range(5):
            L.torus("Wave", 6 + k * 3, 0.06, (-10 + k * 6, 14 + k * 4, -0.36), (1, 0.12, 1), L.mat("ZWFoam", "#ffffff", 0.3, emission="#ffffff", emit=0.3))
        for k, (x, y) in enumerate(((-40, 70), (35, 80))):
            L.sphere("Island", 1.0, (x, y, 0), (9, 5, 3), L.mat("ZWIsland", "#58b04a", 0.9), segs=24)
    elif kind == "barn":
        red = L.mat("ZWBarn", "#d23a2a", 0.6); white = L.mat("ZWBarnTrim", "#ffffff", 0.5)
        L.cube("Barn", 1, (-11, 22, 2.2), (5.5, 4.5, 4.4), red)
        L.cone("BarnRoof", 4.3, 0.0, 2.6, (-11, 22, 5.7), (1, 0.82, 1), L.mat("ZWBarnRoof", "#7a3a2a", 0.6), verts=4, rot=(0, 0, math.pi / 4))
        L.cube("BarnDoor", 1, (-11, 19.7, 1.4), (2.2, 0.1, 2.8), white)
        L.cylinder("Silo", 1.3, 6.0, (-6.5, 23, 3.0), m=L.mat("ZWSilo", "#c9d2dc", 0.4, metal=0.3), verts=24)
        L.sphere("SiloTop", 1.3, (-6.5, 23, 6.0), (1, 1, 0.6), L.mat("ZWBarnRoof", "#7a3a2a", 0.6), segs=20)
        wood = L.mat("ZWFence", "#f2e6d0", 0.7)
        for k in range(14):
            fx = -16 + k * 2.4
            L.cube("Post", 1, (fx, 11, 0.55), (0.14, 0.14, 1.1), wood)
        for z in (0.45, 0.85):
            L.cube("Rail", 1, (-0.4, 11, z), (31.2, 0.08, 0.12), wood)
    elif kind == "mesa":
        for k, (x, y, w, h) in enumerate(((-30, 70, 16, 10), (4, 80, 22, 13), (34, 72, 14, 9))):
            L.cube("Mesa", 1, (x, y, h / 2 - 1), (w, 8, h), L.mat(f"ZWMesa{k}", ("#c8683a", "#d9784a", "#b8583a")[k], 0.95))
    elif kind == "waterfall":
        rock = L.mat("ZWCliff", "#6a8a6a", 0.95, bump=0.4, bump_scale=2)
        L.cube("Cliff", 1, (6, 40, 6), (30, 8, 14), rock)
        fall = L.cube("Waterfall", 1, (6, 35.9, 5.5), (4.5, 0.3, 13), L.mat("ZWFall", "#bfe9ff", 0.1, emission="#dff6ff", emit=0.6))
        L.cylinder("Pool", 1.0, 0.06, (6, 33, 0.03), (6, 2.5, 1), L.mat("ZWPool", "#2fa8e0", 0.05, coat=1.0), verts=40)
        return {"_fall": fall}
    elif kind == "rainbow":
        cols = ("#ff4f4f", "#ff9f43", "#ffe14f", "#5ad06a", "#4fa8ff", "#a87cff")
        for k, c in enumerate(cols):
            L.torus("Rainbow", 34 - k * 1.6, 0.8, (0, 80, -4), (1, 1, 1), L.mat(f"ZWRain{k}", c, 0.5, emission=c, emit=0.8, alpha=0.75), rot=(math.pi / 2, 0, 0))
    return {}


def _water(L, rng, kind, clear):
    if kind == "river":
        w = L.mat("ZWRiver", "#3fb0e8", 0.05, coat=1.0)
        me = bpy.data.meshes.new("River"); bm = bmesh.new()
        pts = [(-40 + i * 4, 9 + 2.2 * math.sin(i * 0.5)) for i in range(21)]
        vs = []
        for x, y in pts:
            vs.append((bm.verts.new((x, y - 1.6, 0.03)), bm.verts.new((x, y + 1.6, 0.03))))
        for a, b in zip(vs, vs[1:]): bm.faces.new((a[0], b[0], b[1], a[1]))
        bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("River", me); L.scene().collection.objects.link(o); o.data.materials.append(w)
        for k in range(8):
            L.sphere("Stone", 0.35 + rng.random() * 0.3, (-14 + k * 4, 7.2 + rng.random() * 0.4, 0.1), (1.3, 1, 0.6), L.mat("ZWStone", "#9a948a", 0.8), segs=12)
        for k in range(6):
            L.cylinder("LilyPad", 0.4, 0.02, (-10 + k * 4.5, 9.5 + (k % 2) * 0.8, 0.06), m=L.mat("ZWLily", "#4caf50", 0.6), verts=20)
        return ((0, 9, 40, 2.2),)
    if kind == "ice":
        L.cylinder("IcePond", 1.0, 0.04, (7.5, 6, 0.03), (3.6, 2.1, 1), L.mat("ZWIce", "#bfe3ff", 0.15, coat=1.0), verts=40)
        return ((7.5, 6, 3.8, 2.3),)
    return ()


def _cover(L, rng, kind, clear):
    if kind == "snow":
        m = L.mat("ZWSnowMound", "#ffffff", 0.75, sheen=0.4)
        for k in range(26):
            x, y = (rng.random() - 0.5) * 34, 1 + rng.random() * 26
            if abs(x) < 6 and y < 5: continue
            r = 0.6 + rng.random() * 1.2
            L.sphere("Mound", r, (x, y, 0), (1.6, 1.2, 0.45), m, segs=16)
        ice = L.mat("ZWIceBlock", "#d8efff", 0.15, coat=0.9, sss=0.2)
        for k, (x, y) in enumerate(((-8, 3), (9, 4), (-5, 9), (6, 10))):
            L.cube("IceBlock", 1, (x, y, 0.4), (1.0, 0.9, 0.8), ice, rot=(0, 0, k * 0.5), bevel=0.08)
    elif kind == "shells":
        cols = ("#ff9fb0", "#fff1d6", "#ffc58a", "#c9a7ff")
        for k in range(30):
            x, y = (rng.random() - 0.5) * 22, -2 + rng.random() * 12
            if abs(x) < 5 and y < 4: continue
            L.sphere("Shell", 0.12 + rng.random() * 0.08, (x, y, 0.04), (1, 1.2, 0.45), L.mat(f"ZWShell{k % 4}", cols[k % 4], 0.4, coat=0.6), segs=10)
        L.cylinder("Bucket", 0.35, 0.6, (-5.5, -1.2, 0.3), m=L.mat("ZWBucket", "#ff5a5a", 0.4, coat=0.5), verts=20)
        L.sphere("Ball", 0.45, (5.8, -0.6, 0.45), m=L.mat("ZWBall", "#ffd23f", 0.35, coat=0.6), segs=20)
    elif kind == "pebbles":
        for k in range(36):
            x, y = (rng.random() - 0.5) * 30, rng.random() * 20
            if abs(x) < 6 and y < 4: continue
            L.sphere("Pebble", 0.1 + rng.random() * 0.35, (x, y, 0.05), (1.4, 1, 0.6), L.mat(f"ZWPeb{k % 3}", ("#c98a5a", "#e0a870", "#a8704a")[k % 3], 0.85), segs=10)
    elif kind == "leaves":
        cols = ("#e8742a", "#f2b23a", "#d9442b", "#b8663a")
        for k in range(70):
            x, y = (rng.random() - 0.5) * 26, -3 + rng.random() * 18
            if abs(x) < 3.5 and y < 3: continue
            L.sphere("Leaf", 0.16, (x, y, 0.02), (1, 0.6, 0.12), L.mat(f"ZWFall{k % 4}", cols[k % 4], 0.6), segs=8, rot=(0, 0, rng.random() * 3))
        for k, (x, y) in enumerate(((-6, 4), (7, 5))):
            L.cylinder("MushStem", 0.12, 0.35, (x, y, 0.18), m=L.mat("ZWStem", "#fff3dc", 0.6), verts=12)
            L.sphere("MushCap", 0.32, (x, y, 0.38), (1, 1, 0.55), L.mat("ZWCap", "#e8302a", 0.4, coat=0.4), segs=16)
    elif kind == "rocks":
        rock = L.mat("ZWRock", "#9a9aa8", 0.85, bump=0.4, bump_scale=3)
        for k in range(14):
            x, y = (rng.random() - 0.5) * 30, 2 + rng.random() * 16
            if abs(x) < 6 and y < 5: continue
            r = 0.3 + rng.random() * 0.8
            L.sphere("Rock", r, (x, y, r * 0.3), (1.3, 1, 0.8), rock, segs=14)


def _fx(L, rng, kind):
    """Small moving things that make a place feel alive (animated in animate())."""
    out = []
    if not kind: return out
    spec = {"butterflies": (14, ("#ff6fa6", "#ffd23f", "#6fc8ff"), 0.12, 2.0),
            "dragonflies": (8, ("#4fd8ff", "#7affc0"), 0.1, 1.5), "snow": (90, ("#ffffff",), 0.05, 6.0),
            "leaves": (40, ("#e8742a", "#f2b23a", "#d9442b"), 0.1, 5.0), "petals": (40, ("#ffb3cf", "#ffffff"), 0.07, 5.0),
            "fireflies": (50, ("#fff27a",), 0.06, 2.5), "bubbles": (18, ("#dff6ff",), 0.18, 3.0)}[kind]
    n, cols, r, h = spec
    for k in range(n):
        c = cols[k % len(cols)]
        emit = 4.0 if kind == "fireflies" else (0.4 if kind in ("snow", "bubbles") else 0.15)
        m = L.mat(f"ZWFx{kind}{k % len(cols)}", c, 0.4, emission=c, emit=emit, alpha=0.6 if kind == "bubbles" else 1.0)
        x, y, z = (rng.random() - 0.5) * 24, -2 + rng.random() * 16, 0.4 + rng.random() * h
        if kind in ("butterflies", "dragonflies"):
            o = L.empty("Flyer", (x, y, z))
            for sx in (-1, 1):
                L.sphere("Wing", r, (sx * r * 0.9, 0, 0), (1, 0.15, 0.8), m, o, 10)
        else:
            o = L.sphere("Fx", r, (x, y, z), (1, 1, 0.3) if kind in ("leaves", "petals") else (1, 1, 1), m, segs=8)
        out.append((o, (x, y, z), rng.random() * 6.28))
    return out


# --------------------------------------------------------------------------- landmarks (each place gets its own big shapes)
def _landmark(L, rng, biome, v):
    """Mid-distance landmark(s) that give a place its identity. v (0..3) picks the side and the variant."""
    sx = -1 if v % 2 else 1; X = lambda x: x * sx
    wood = L.mat("ZWWood", "#a8743e", 0.8, bump=0.3, bump_scale=8); white = L.mat("ZWWhite", "#ffffff", 0.6)
    red = L.mat("ZWRed", "#e2463a", 0.5, coat=0.3); yellow = L.mat("ZWYellow", "#ffd23f", 0.5); stone = L.mat("ZWStoneLm", "#a9a59c", 0.85, bump=0.3, bump_scale=4)
    out = {}
    if biome == "farm":
        bx, by = X(9.5), 15
        L.cone("MillBody", 1.5, 0.9, 5.0, (bx, by, 2.5), m=white, verts=8)
        L.cone("MillRoof", 1.2, 0.0, 1.3, (bx, by, 5.6), m=red, verts=8)
        hub = L.empty("MillHub", (bx, by - 1.2, 4.5))
        for k in range(4):
            bp = L.empty(f"BladeP{k}", (0, 0, 0), hub); bp.rotation_euler = (0, k * math.pi / 2, 0)
            L.cube("Blade", 1, (0, 0, 1.5), (0.5, 0.06, 3.0), wood, parent=bp)
        out["_spin"] = hub
        hay = L.mat("ZWHay", "#f0c95a", 0.9, bump=0.4, bump_scale=14)
        for k, (x, y) in enumerate(((-7.5, 5.5), (-8.6, 6.3), (-8.0, 5.9))):
            L.cylinder("Hay", 0.7, 1.0, (X(x), y, 0.7 + (0.95 if k == 2 else 0)), m=hay, rot=(math.pi / 2, 0, 0.4), verts=20)
    elif biome == "arctic":
        ix, iy = X(-8.5), 9
        L.sphere("Igloo", 2.4, (ix, iy, 0), (1, 1, 0.85), L.mat("ZWIgloo", "#eef7ff", 0.5, sheen=0.4, bump=0.25, bump_scale=3), segs=24)
        L.cylinder("IglooDoor", 0.9, 1.4, (ix, iy - 2.3, 0.5), m=L.mat("ZWIglooDoor", "#5a7fb0", 0.7), rot=(math.pi / 2, 0, 0), verts=16)
        mx, my = X(8.0), 6.5
        for z, r in ((0.7, 0.8), (1.75, 0.58), (2.55, 0.42)): L.sphere("Snowman", r, (mx, my, z), m=white, segs=20)
        L.cone("Carrot", 0.08, 0.0, 0.4, (mx, my - 0.5, 2.55), m=L.mat("ZWCarrot", "#ff8a1f", 0.5), rot=(math.pi / 2, 0, 0), verts=10)
        L.cylinder("Hat", 0.3, 0.4, (mx, my, 3.05), m=red, verts=16)
    elif biome == "beach":
        ux, uy = X(-7.0), 4.5
        L.cylinder("Pole", 0.06, 3.0, (ux, uy, 1.5), m=white, verts=10)
        for k in range(8):
            L.cone(f"Umb{k}", 2.0, 0.0, 0.8, (ux, uy, 3.1), m=(red if k % 2 else white), verts=3, rot=(0, 0, k * math.pi / 4))
        cx, cy = X(7.5), 5
        sand = L.mat("ZWCastle", "#f2d28a", 0.95, bump=0.3, bump_scale=20)
        L.cube("Castle", 1, (cx, cy, 0.5), (2.2, 1.6, 1.0), sand)
        for dx in (-1.1, 1.1):
            L.cylinder("Tower", 0.45, 1.8, (cx + dx, cy, 0.9), m=sand, verts=14); L.cone("TowerTop", 0.5, 0.0, 0.6, (cx + dx, cy, 2.1), m=red, verts=14)
        bx = X(14)
        out["_boat"] = L.cube("Boat", 1, (bx, 30, 0.3), (4, 1.4, 0.9), red); L.cone("Sail", 1.8, 0.0, 3.6, (bx, 30, 2.8), (0.15, 1, 1), white, verts=3)
    elif biome == "jungle":
        ax, ay = X(-8.0), 8
        vine = L.mat("ZWVine", "#3b8a3a", 0.7, sheen=0.3)
        L.torus("VineArch", 3.2, 0.3, (ax, ay, 0), (1, 1, 1.25), vine, rot=(math.pi / 2, 0, 0.3))
        for k in range(9):
            a = k / 8 * math.pi
            L.sphere("ArchFlower", 0.28, (ax + math.cos(a) * 3.2 * math.cos(0.3), ay - 0.25 + math.cos(a) * 3.2 * math.sin(0.3) * 0, math.sin(a) * 4.0), m=L.mat(f"ZWArchF{k % 3}", ("#ff4f8b", "#ffcc00", "#ff7a1a")[k % 3], 0.4, emission=("#ff4f8b", "#ffcc00", "#ff7a1a")[k % 3], emit=0.15), segs=12)
        for k, (x, y, sc) in enumerate(((8.5, 6, 1.0), (10, 9, 1.3), (7.2, 10, 0.8))):
            L.cylinder("BigStem", 0.1 * sc, 1.6 * sc, (X(x), y, 0.8 * sc), m=vine, verts=8)
            for j in range(6):
                a = j / 6 * math.tau
                L.sphere("BigPetal", 0.42 * sc, (X(x) + math.cos(a) * 0.5 * sc, y, 1.7 * sc + math.sin(a) * 0.5 * sc), (1, 0.4, 1), L.mat(f"ZWBigPetal{k}", ("#ff5fa2", "#ff9f1c", "#b57cff")[k], 0.5, sss=0.2), segs=14)
            L.sphere("BigCore", 0.3 * sc, (X(x), y - 0.12, 1.7 * sc), m=yellow, segs=12)
    elif biome == "desert":
        ax, ay = X(-9), 12
        rock = L.mat("ZWArchRock", "#d0703c", 0.95, bump=0.4, bump_scale=3)
        L.torus("RockArch", 4.0, 1.1, (ax, ay, 0), (1, 1, 1.15), rock, rot=(math.pi / 2, 0, -0.25))
        ox_, oy = X(8.5), 8
        L.cylinder("Oasis", 1.0, 0.05, (ox_, oy, 0.03), (2.6, 1.6, 1), L.mat("ZWOasis", "#39b6e6", 0.4, emission="#39b6e6", emit=0.15), verts=32)
        _tree(L, rng, "palm", ox_ + 2.4, oy + 1.2, 0.9, 1); _tree(L, rng, "palm", ox_ - 2.6, oy + 1.6, 0.75, 2)
    elif biome in ("autumn_forest", "mountain"):
        cx, cy = X(9.5), 13
        L.cube("Cabin", 1, (cx, cy, 1.3), (4.2, 3.4, 2.6), wood)
        L.cone("CabinRoof", 3.6, 0.0, 2.0, (cx, cy, 3.6), (1, 0.85, 1), L.mat("ZWCabinRoof", "#7a3a2a" if biome == "autumn_forest" else "#4a6a8a", 0.7), verts=4, rot=(0, 0, math.pi / 4))
        L.cube("CabinDoor", 1, (cx, cy - 1.72, 0.9), (0.9, 0.08, 1.8), L.mat("ZWDoor", "#5a3a22", 0.7))
        L.cube("CabinWin", 1, (cx + 1.3, cy - 1.72, 1.6), (0.8, 0.08, 0.8), L.mat("ZWWin", "#ffe9a0", 0.3, emission="#ffe9a0", emit=1.5))
        if biome == "autumn_forest":
            pk = L.mat("ZWPumpkin", "#f28a1f", 0.5, coat=0.3, bump=0.2, bump_scale=6)
            for k, (x, y, r) in enumerate(((-7.2, 4.5, 0.5), (-8.3, 5.2, 0.38), (-6.6, 5.6, 0.3), (-8.9, 4.2, 0.28))):
                L.sphere("Pumpkin", r, (X(x), y, r * 0.75), (1.15, 1.15, 0.85), pk, segs=16); L.cylinder("PStem", r * 0.12, r * 0.4, (X(x), y, r * 1.5), m=L.mat("ZWVine", "#3b8a3a", 0.7), verts=8)
        else:
            L.cylinder("Lake", 1.0, 0.05, (X(-9), 11, 0.03), (5.5, 2.6, 1), L.mat("ZWLake", "#4fb4e8", 0.4, emission="#4fb4e8", emit=0.15), verts=40)
    elif biome == "river":
        bx = X(-6.5)
        L.torus("Bridge", 2.6, 0.22, (bx, 9, -0.7), (1, 1, 1), wood, rot=(0, math.pi / 2, 0))
        L.cube("BridgeDeck", 1, (bx, 9, 1.55), (1.6, 3.0, 0.14), wood)
        for sy in (-1, 1):
            for k in (-1, 1): L.cylinder("BPost", 0.08, 0.9, (bx + 0.75 * k, 9 + sy * 1.3, 2.0), m=wood, verts=8)
        boat = L.cube("RowBoat", 1, (X(6), 9, 0.25), (2.2, 0.9, 0.5), red, bevel=0.1)
        out["_boat"] = boat
    elif biome == "bamboo":
        for k, (x, y) in enumerate(((-7.5, 4.5), (7.8, 5.2))):
            L.cylinder("LanternBase", 0.3, 1.2, (X(x), y, 0.6), m=stone, verts=8)
            L.cube("LanternBox", 1, (X(x), y, 1.5), (0.7, 0.7, 0.6), L.mat("ZWLantern", "#ffe9a0", 0.3, emission="#ffd070", emit=2.5))
            L.cone("LanternTop", 0.7, 0.0, 0.5, (X(x), y, 2.05), m=stone, verts=4, rot=(0, 0, math.pi / 4))
        L.torus("RedBridge", 3.0, 0.25, (X(9), 13, -1.2), (1, 1, 1), red, rot=(math.pi / 2, 0, 0))
    elif biome == "spring_meadow":
        L.cube("Blanket", 1, (X(-7.5), 4.5, 0.03), (2.6, 2.0, 0.04), L.mat("ZWBlanket", "#ff6f7a", 0.9), rot=(0, 0, 0.3))
        L.cube("Basket", 1, (X(-7.2), 4.8, 0.3), (0.7, 0.5, 0.5), wood, bevel=0.08)
        kite = L.empty("Kite", (X(9), 14, 9))
        L.cone("KiteBody", 0.9, 0.0, 0.12, (0, 0, 0), (1, 1, 1), L.mat("ZWKite", "#ff4f8b", 0.4, emission="#ff4f8b", emit=0.3), kite, verts=4, rot=(math.pi / 2, 0, 0))
        for k in range(4): L.sphere("KiteTail", 0.14, (0.15 * k, 0, -0.7 - 0.5 * k), m=(yellow if k % 2 else red), parent=kite, segs=8)
        out["_kite"] = kite
        L.cylinder("Pond", 1.0, 0.05, (X(8), 7, 0.03), (3.0, 1.8, 1), L.mat("ZWPondSm", "#4fb4e8", 0.4, emission="#4fb4e8", emit=0.15), verts=32)
    elif biome == "night_meadow":
        tx, ty = X(-8), 7
        L.cone("Tent", 2.4, 0.0, 2.6, (tx, ty, 1.3), m=L.mat("ZWTent", "#ff8a3d", 0.7), verts=4, rot=(0, 0, math.pi / 4))
        L.sphere("TentGlow", 0.4, (tx, ty - 1.9, 0.6), m=L.mat("ZWTentGlow", "#ffe9a0", 0.3, emission="#ffd070", emit=6.0), segs=12)
        gl = []
        for k in range(9):
            u = k / 8
            gl.append(L.sphere("StringLight", 0.16, (X(3 + u * 8), 6 + u * 2, 3.4 - math.sin(u * math.pi) * 0.8),
                               m=L.mat(f"ZWStr{k % 3}", ("#ffd070", "#ff8fb0", "#8fd0ff")[k % 3], 0.3, emission=("#ffd070", "#ff8fb0", "#8fd0ff")[k % 3], emit=5.0), segs=10))
        for x in (3, 11): L.cylinder("LightPole", 0.07, 3.5, (X(x), 6 if x == 3 else 8, 1.75), m=wood, verts=8)
    elif biome == "savanna":
        for k, (x, y, h) in enumerate(((-8.0, 6.5, 2.2), (-9.2, 7.6, 1.4))):
            L.cone("Termite", 0.9, 0.2, h, (X(x), y, h / 2), m=L.mat("ZWTermite", "#b8743a", 0.95, bump=0.4, bump_scale=6), verts=10)
        L.cylinder("Hole", 1.0, 0.05, (X(8), 6.5, 0.03), (3.4, 2.0, 1), L.mat("ZWHole", "#39a8e0", 0.4, emission="#39a8e0", emit=0.15), verts=40)
    # birds far in the sky (every daytime place)
    birds = []
    bm_ = L.mat("ZWBird", "#3a3a4a", 0.8)
    for k in range(5):
        b = L.empty("SkyBird", (-20 + k * 9 + (v * 5), 60, 16 + (k % 3) * 2))
        for s_ in (-1, 1): L.sphere("BW", 0.5, (0.45 * s_, 0, 0), (1, 0.25, 0.12), bm_, b, 8, (0, 0.4 * s_, 0))
        birds.append(b)
    out["_birds"] = birds
    return out



# --------------------------------------------------------------------------- build
def build(L, rng, biome="savanna", tod="golden", seed=None, **_):
    if seed is not None:
        import random as _r; rng = _r.Random(seed)
    B = BIOMES.get(biome, BIOMES["savanna"]); tod = B.get("force_tod", tod); T = TOD.get(tod, TOD["golden"])
    stops = list(T["sky"])
    if biome == "arctic" and tod != "night": stops = ["#e8f4ff", "#d6ecff", "#9ccaf5", "#5a9ae6"]
    _world(L, f"ZW_{biome}_{tod}", stops)
    e, el, az, col = T["sun"]
    L.light("Sun", "SUN", e, rot=(math.radians(90 - el), 0, math.radians(az)), color=col, angle=math.radians(4))
    L.light("Fill", "AREA", 300 if tod != "night" else 380, (-4, -10, 6), (math.radians(58), 0, math.radians(-20)), T["fill"], 10)
    L.light("Rim", "AREA", 550, (3, 9, 5), (math.radians(-62), 0, math.radians(165)), (1, 0.85, 0.65) if tod != "night" else (0.6, 0.7, 1.0), 9)

    L.cube("Ground", 1, (0, 35, -0.5), (200, 110, 1), _ramp_mat(L, f"ZWGround_{biome}", *B["ground"]))
    clear = (0, 0.9, 6.8, 2.9)
    L.cylinder("Stage", 1.0, 0.02, (0, 0.9, 0.006), (clear[2] * 0.95, clear[3] * 0.95, 1),
               L.mat(f"ZWStage_{biome}", B["stage"], 1.0, sheen=0.2, bump=0.25, bump_scale=10), verts=48)
    keep = _water(L, rng, B["water"], clear) if B["water"] in ("river", "ice") else ()
    if B["grass"]:
        gm = _ramp_mat(L, f"ZWGrass_{biome}", *B["grass"], scale=0.3, rough=0.7)
        _grass(L, rng, gm, clear, keep_out=keep)
    _cover(L, rng, B["cover"], clear)
    if B.get("flowers"):
        fl = [L.mat(f"ZWFlower{c}", c, 0.5, sss=0.2) for c in B["flowers"]]
        for i in range(44):
            a = rng.random() * math.tau; rr = 1.0 + rng.random() * 0.3
            L.sphere("Flower", 0.08, (math.cos(a) * clear[2] * rr, clear[1] + math.sin(a) * clear[3] * rr, 0.1), (1, 1, 0.6), fl[i % len(fl)], segs=10)

    # trees: framing pair, midground, background (deterministic per seed, different per biome)
    spots_t = [(-10.5, 4.5, 1.3), (11.0, 6.5, 1.15), (-6.5, 15, 1.0), (4.0, 20, 0.95), (-16, 22, 1.0), (17, 24, 1.0), (-1, 34, 0.9), (24, 38, 1.0), (-26, 36, 1.0), (-13, 9, 0.8), (13, 13, 0.85)]
    kinds = B["trees"]
    for k, (x, y, s) in enumerate(spots_t):
        if B["water"] == "river" and abs(y - 9) < 3: y += 5
        _tree(L, rng, kinds[(k + (seed or 0)) % len(kinds)], x + (rng.random() - 0.5) * 2, y, s * (0.85 + rng.random() * 0.3), k)
    extra = _far(L, rng, B["far"], B)
    extra.update(_landmark(L, rng, biome, (seed or 0) % 4))
    if B["water"] == "ocean": _far(L, rng, "ocean", B)

    # sky: sun or moon + stars, clouds
    out = {}
    if T["sun_disc"]:
        sz = 4.2 if tod != "sunset" else 6.0; zz = 24 if tod not in ("sunset", "morning") else 9
        sun = L.sphere("SkySun", sz, (22 if tod != "morning" else -26, 80, zz), m=L.mat(f"ZWSun{tod}", T["sun_disc"], 0.5, emission=T["sun_disc"], emit=6.0), segs=32)
        out["_sun"] = sun
    else:
        moon = L.sphere("Moon", 3.6, (18, 80, 22), m=L.mat("ZWMoon", "#fff6d0", 0.5, emission="#fff2c0", emit=4.0), segs=32)
        out["_sun"] = moon
        sm = L.mat("ZWStar", "#ffffff", 0.5, emission="#fff8e0", emit=8.0)
        stars = []
        for k in range(80):
            a = rng.random(); b = rng.random()
            stars.append(L.sphere("Star", 0.18 + rng.random() * 0.2, (-60 + a * 120, 88, 8 + b * 40), m=sm, segs=6))
        out["_stars"] = stars
    cloud_m = L.mat(f"ZWCloud{tod}", "#ffffff" if tod not in ("sunset", "night") else ("#ffd0e0" if tod == "sunset" else "#8a9ad0"),
                    0.9, sheen=0.4, emission="#fff6ea" if tod != "night" else "#5a6aa0", emit=0.5 if tod != "night" else 0.2)
    clouds = []
    for k, (x, y, z, s) in enumerate(((-26, 70, 19, 2.6), (-4, 76, 23, 3.0), (34, 68, 17, 2.4), (10, 72, 15, 1.8))):
        c = L.empty("Cloud", (x, y, z))
        for dx, dz, r in ((0, 0, 1.0), (1.1, -0.25, 0.75), (-1.1, -0.3, 0.7), (0.5, 0.45, 0.7)):
            L.sphere("Puff", r * s, (dx * s, 0, dz * s), (1, 0.6, 0.85), cloud_m, c, 18)
        clouds.append((c, x))
    out.update(extra)
    out["_clouds"] = clouds
    out["_fx"] = _fx(L, rng, B["fx"]); out["_fxkind"] = B["fx"]
    cams = {"wide": ((0, -13.4, 4.4), (0, 1.0, 1.75)), "center": (0, 0.6, 1.7), "orbit_r": 10.5,
            "pond": ((-1.5, -6.5, 2.6), (5.5, 4.5, 1.1)), "hero": ((-1.2, -8.0, 1.0), (0, 0.5, 2.2)),
            "vista": ((0, -10.0, 5.2), (0, 6, 2.6)), "giraffe": ((2.3, -0.8, 3.6), (1.1, 3.3, 3.05)),
            "side": ((-9.0, -6.0, 2.4), (0, 1.0, 1.5)), "high": ((0, -6.0, 9.0), (0, 1.5, 0.8))}
    spots = {"center": (0, -0.6, 0), "lion": (-2.35, 0.1, 0), "zebra": (2.6, 0.2, 0), "elephant": (-4.6, 1.3, 0),
             "hippo": (4.9, 1.4, 0), "giraffe": (1.1, 3.3, 0), "left": (-2.35, 0.1, 0), "right": (2.35, 0.1, 0), "back": (0, 2.4, 0)}
    spots.update({"s1": spots["lion"], "s2": spots["zebra"], "s3": spots["elephant"], "s4": spots["hippo"], "s5": spots["giraffe"], "s6": (-1.6, 3.2, 0)})
    out.update({"spots": spots, "cams": cams,
                "prop_spots": {"top": (0, 0.0, 4.15), "left": (-3.6, -1.4, 3.3), "right": (3.6, -1.4, 3.3), "front": (0, -2.6, 0.9)},
                "exposure": T["exp"], "look": "AgX - Punchy", "biome": biome, "tod": tod})
    return out


# --------------------------------------------------------------------------- props (same API as savanna.prop)
def prop(L, name, at, **o):
    try:
        from sets import savanna
        return savanna.prop(L, name, at, **o)
    except Exception:
        return L.sphere("Prop", 0.4, at, m=L.mat("ZWProp", "#ffcc00", 0.4))


def animate(L, SET, f, t, s):
    for c, x0 in SET.get("_clouds", []):
        c.location.x = x0 + math.sin(t * 0.05 + x0) * 2.0 + t * 0.03
    sun = SET.get("_sun")
    if sun:
        p = 1 + 0.04 * math.sin(s.get("beat", 0) * math.tau) * s.get("energy", 0.5)
        sun.scale = (p, p, p)
    for k, st in enumerate(SET.get("_stars", [])):
        tw = 0.7 + 0.3 * math.sin(t * 2.0 + k * 1.7)
        st.scale = (tw, tw, tw)
    kind = SET.get("_fxkind")
    for o, (x, y, z), ph in SET.get("_fx", []):
        if kind in ("snow", "leaves", "petals"):
            fall = 0.6 if kind == "snow" else 0.45
            zz = (z - t * fall) % 6.5
            o.location = (x + math.sin(t * 0.8 + ph) * 0.4, y, zz)
            if kind != "snow": o.rotation_euler = (t * 1.5 + ph, t + ph, 0)
        elif kind in ("butterflies", "dragonflies"):
            o.location = (x + math.sin(t * 0.6 + ph) * 1.5, y + math.cos(t * 0.5 + ph) * 0.8, z + math.sin(t * 2 + ph) * 0.3)
            flap = math.sin(t * (24 if kind == "butterflies" else 40) + ph)
            for w in o.children: w.rotation_euler = (0, flap * 0.6 * (1 if w.location.x > 0 else -1), 0)
        elif kind == "fireflies":
            o.location = (x + math.sin(t * 0.4 + ph) * 0.8, y + math.cos(t * 0.3 + ph) * 0.5, z + math.sin(t * 0.7 + ph) * 0.3)
            g = max(0.0, math.sin(t * 1.6 + ph * 3)); o.scale = (0.4 + g, 0.4 + g, 0.4 + g)
        elif kind == "bubbles":
            zz = (z + t * 0.5) % 4.0
            o.location = (x + math.sin(t + ph) * 0.3, y, zz)
    sp = SET.get("_spin")
    if sp: sp.rotation_euler = (0, t * 0.9, 0)
    bo = SET.get("_boat")
    if bo: bo.rotation_euler = (math.sin(t * 1.2) * 0.05, 0, 0); bo.location.z = 0.28 + math.sin(t * 1.5) * 0.05
    ki = SET.get("_kite")
    if ki: ki.rotation_euler = (0, math.sin(t * 1.1) * 0.25, math.sin(t * 0.7) * 0.2)
    for k, b in enumerate(SET.get("_birds", [])):
        fl = math.sin(t * 7 + k)
        for w in b.children: w.rotation_euler = (0, (0.4 + fl * 0.5) * (1 if w.location.x > 0 else -1), 0)
    fall = SET.get("_fall")
    if fall: fall.scale.z = 13 * (1 + 0.01 * math.sin(t * 6))
