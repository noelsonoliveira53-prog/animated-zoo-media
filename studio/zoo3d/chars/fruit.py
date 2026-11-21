"""Fruity Friends: singing fruit and veggie characters (see API.md).

opts: kind in {apple, banana, orange, strawberry, grape, carrot, broccoli, pipkiko}; optional color (body hex), scale.
pipkiko = the channel host: a big heart-shaped strawberry with seeds, a leafy crown and pink cheeks (art_fruity.py PIPKIKO).
Every body is a deformed UV sphere (one mesh), with the face placed on the real surface via a BVH ray cast.
"""
import math
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

LEG_H = 0.34


def _ss(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


# ------------------------------------------------------------------ body shapes (unit sphere -> body space)
def _apple(x, y, z):
    R = 0.92; rho2 = x * x + y * y; w = 1 + 0.1 * z
    Z = z * R * 0.9
    d = math.exp(-rho2 / 0.05)
    Z += -R * 0.24 * d if z > 0 else R * 0.1 * d
    return x * w * R, y * w * R * 0.92, Z


def _strawberry(R):
    def f(x, y, z):
        k = 0.5 + 0.5 * _ss((z + 1) / 1.3)
        Z = z * R * 1.08
        if z > 0.5: Z = R * 1.08 * (0.5 + (z - 0.5) * 0.5)
        return x * k * R * 1.04, y * k * R * 0.9, Z
    return f


def _banana(x, y, z):
    k = 1 - 0.12 * z * z
    return x * 0.5 * k + 0.34 * z ** 4, y * 0.44 * k, z * 0.98


def _orange(x, y, z):
    return x * 0.84, y * 0.8, z * 0.8


def _grape(x, y, z):
    k = 1 + 0.06 * z
    return x * 0.7 * k, y * 0.66 * k, z * 0.86


def _carrot(x, y, z):
    s = (z + 1) / 2
    k = 0.16 + 0.84 * s ** 0.85
    Z = z * 0.92
    if z > 0.55: Z = 0.92 * (0.55 + (z - 0.55) * 0.55)
    return x * 0.68 * k, y * 0.62 * k, Z


def _broccoli(x, y, z):
    k = 1 + 0.18 * max(0.0, z)
    return x * 0.5 * k, y * 0.46 * k, z * 0.66


#           shape fn, body hex, face fractions (eye, mouth), eye r, spacing, iris, limb, shoe
KINDS = {
    "pipkiko":    (_strawberry(0.98), "#e8202c", (0.62, 0.42), 0.25, 0.30, "#3a2414", "#2f8f3a", "#ffd23f"),
    "strawberry": (_strawberry(0.80), "#ff3a5c", (0.62, 0.42), 0.22, 0.25, "#2a5aa8", "#2f8f3a", "#7c4dff"),
    "apple":      (_apple, "#e3262b", (0.58, 0.38), 0.24, 0.28, "#2f7d32", "#5a3a22", "#42a5f5"),
    "banana":     (_banana, "#ffd83a", (0.66, 0.5), 0.2, 0.22, "#1e63c4", "#7a5a2e", "#ff5c8a"),
    "orange":     (_orange, "#ff9416", (0.6, 0.4), 0.23, 0.27, "#2f7d32", "#2f8f3a", "#ab47bc"),
    "grape":      (_grape, "#8e3fd0", (0.6, 0.4), 0.22, 0.25, "#3a2414", "#5a3a22", "#26c6da"),
    "carrot":     (_carrot, "#ff8418", (0.7, 0.52), 0.22, 0.25, "#4a2c18", "#3c9a3c", "#29b6f6"),
    "broccoli":   (_broccoli, "#9ed15f", (0.6, 0.36), 0.2, 0.22, "#4a2c18", "#6cae3a", "#ff7043"),
}


def _skin(L, kind, hexcol):
    if kind in ("pipkiko", "strawberry"):
        m = L.mat("FrSkin_" + kind + hexcol, hexcol, 0.3, coat=0.7, sss=0.12)
        _seeds(m, "#ffe27a")
        return m
    if kind == "apple": return L.mat("FrSkin_apple" + hexcol, hexcol, 0.22, coat=0.9, sss=0.1)
    if kind == "banana": return L.mat("FrSkin_banana" + hexcol, hexcol, 0.42, coat=0.35, sss=0.12)
    if kind == "orange": return L.mat("FrSkin_orange" + hexcol, hexcol, 0.38, coat=0.5, sss=0.1, bump=0.25, bump_scale=70)
    if kind == "grape": return L.mat("FrSkin_grape" + hexcol, hexcol, 0.18, coat=1.0, sss=0.3)
    if kind == "carrot":
        m = L.mat("FrSkin_carrot" + hexcol, hexcol, 0.42, coat=0.35, sss=0.1)
        _ridges(m)
        return m
    return L.mat("FrSkin_broc" + hexcol, hexcol, 0.48, coat=0.2, sss=0.15, sheen=0.2)


def _seeds(m, seed_hex):
    """Strawberry seeds: Voronoi dots in object space drive color + a little bump."""
    if m.get("seeded"): return
    m["seeded"] = 1
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    base = tuple(b.inputs["Base Color"].default_value)
    tc = nt.nodes.new("ShaderNodeTexCoord"); vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 4.2
    try: vo.inputs["Randomness"].default_value = 0.85
    except Exception: pass
    cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.interpolation = "CONSTANT"
    h = seed_hex.lstrip("#"); sc = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    sc = [((c + 0.055) / 1.055) ** 2.4 for c in sc]
    cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = (*sc, 1)
    cr.color_ramp.elements[1].position = 0.2; cr.color_ramp.elements[1].color = base
    nt.links.new(tc.outputs["Object"], vo.inputs["Vector"]); nt.links.new(vo.outputs["Distance"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35; bp.inputs["Distance"].default_value = 0.02
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 0.0; mr.inputs["From Max"].default_value = 0.2
    nt.links.new(vo.outputs["Distance"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])


def _ridges(m):
    """Carrot: soft horizontal growth rings as bump."""
    if m.get("ridged"): return
    m["ridged"] = 1
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); wv = nt.nodes.new("ShaderNodeTexWave")
    wv.wave_type = "BANDS"; wv.bands_direction = "Z"; wv.inputs["Scale"].default_value = 3.2; wv.inputs["Distortion"].default_value = 3.0
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.18; bp.inputs["Distance"].default_value = 0.02
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"]); nt.links.new(wv.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])


def _body(L, name, fn, m, parent):
    o = L.sphere(name, 1.0, (0, 0, 0), (1, 1, 1), m, parent, 48)
    pts = [fn(*v.co) for v in o.data.vertices]
    zmin = min(p[2] for p in pts)
    for v, p in zip(o.data.vertices, pts):
        v.co = (p[0], p[1], p[2] - zmin - 0.06)
    o.data.update()
    bvh = BVHTree.FromPolygons([tuple(v.co) for v in o.data.vertices], [tuple(p.vertices) for p in o.data.polygons])
    top = max(v.co.z for v in o.data.vertices)
    return o, bvh, top


def _front(bvh, x, z):
    hit = bvh.ray_cast(Vector((x, -10, z)), Vector((0, 1, 0)))
    return hit[0].y if hit[0] is not None else -0.5


def _side(bvh, z, sx):
    hit = bvh.ray_cast(Vector((10 * sx, 0, z)), Vector((-sx, 0, 0)))
    return abs(hit[0].x) if hit[0] is not None else 0.5


def _bowl(L, name, m, parent):
    """Lower half-sphere: the open-smile 'D' mouth (flat top, round bottom)."""
    o = L.sphere(name, 1.0, (0, 0, 0), (1, 1, 1), m, parent, 32)
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > 0.02], context="VERTS")
    bm.to_mesh(o.data); bm.free()
    return o


def build(L, prefix="Fruit", loc=(0, 0, 0), scale=1.0, kind="pipkiko", color=None, **_):
    kind = kind if kind in KINDS else "pipkiko"
    fn, hexcol, (fe, fm), er, esp, iris, limb_hex, shoe_hex = KINDS[kind]
    hexcol = color or hexcol
    skin = _skin(L, kind, hexcol)
    M = {
        "mouth": L.mat("FrMouth", "#5a0f22", 0.45, coat=0.3),
        "tongue": L.mat("FrTongue", "#ff6f8f", 0.4, sss=0.2),
        "teeth": L.mat("FrTeeth", "#fffdf6", 0.25, coat=0.6),
        "cheek": L.mat("FrCheek", "#ff86a8", 0.6, sss=0.2),
        "brow": L.mat("FrBrow", "#3b1f12", 0.5),
        "leaf": L.mat("FrLeaf", "#34b548", 0.38, coat=0.4, sss=0.15),
        "leafdk": L.mat("FrLeafDk", "#23913a", 0.42, coat=0.3, sss=0.12),
        "stem": L.mat("FrStem", "#7a4a26", 0.6),
        "limb": L.mat("FrLimb" + limb_hex, limb_hex, 0.4, coat=0.4),
        "glove": L.mat("FrGlove", "#ffffff", 0.35, coat=0.5, sheen=0.3),
        "shoe": L.mat("FrShoe" + shoe_hex, shoe_hex, 0.3, coat=0.8),
        "sole": L.mat("FrSole", "#fff7e6", 0.5),
    }
    root = L.empty(prefix, loc); root.scale = (scale,) * 3
    bod = L.empty(prefix + "Bod", (0, 0, LEG_H), root)
    body, bvh, top = _body(L, prefix + "Body", fn, skin, bod)

    ez, mz = top * fe, top * fm
    if kind == "broccoli": ez, mz = top * 0.62, top * 0.38
    # ------------------------------------------------ face
    ey = min(_front(bvh, esp + dx * er, ez + dz * er) for dx in (-0.5, 0, 0.5) for dz in (-0.6, 0, 0.5, 0.9))
    eyes = L.eye_pair(prefix, bod, spacing=esp, z=ez, y=ey + er * 0.28, r=er, iris_hex=iris, lid_mat=skin, toward=0.22)
    lidm = L.mat("FrLid" + hexcol, hexcol, 0.35, coat=0.5, sss=0.1)
    for sock, lid in eyes:
        lid.scale = (1.03, 0.8, 1.03)
        lid.data.materials[0] = lidm
    for sx in (-1, 1):   # little friendly eyebrows
        bx = esp * sx * 1.08; bz = ez + er * 1.28
        L.sphere(f"{prefix}Brow{sx}", 1.0, (bx, _front(bvh, bx, bz) - 0.01, bz), (er * 0.42, 0.03, er * 0.1), M["brow"], bod, 16, (0, -sx * 0.12, 0))
        cx = (esp + er * 0.95) * sx; cz = ez - er * 1.05
        L.sphere(f"{prefix}Cheek{sx}", 1.0, (cx, _front(bvh, cx, cz) + 0.01, cz), (er * 0.55, 0.05, er * 0.36), M["cheek"], bod, 20, (0, 0, sx * 0.35))
    mw, mh = er * (1.1 if kind == "pipkiko" else 0.95), er * (0.95 if kind == "pipkiko" else 0.85)
    my = min(_front(bvh, dx * mw, mz + dz * mh) for dx in (-0.8, 0, 0.8) for dz in (-0.8, 0))
    mouth = L.empty(prefix + "Mouth", (0, my + 0.03, mz), bod)
    _bowl(L, prefix + "MouthIn", M["mouth"], mouth).scale = (mw, 0.07, mh)
    L.sphere(prefix + "Tongue", 1.0, (0, -0.03, -mh * 0.62), (mw * 0.62, 0.05, mh * 0.32), M["tongue"], mouth, 20)
    L.sphere(prefix + "Teeth", 1.0, (0, -0.035, -mh * 0.06), (mw * 0.62, 0.035, mh * 0.13), M["teeth"], mouth, 16)

    # ------------------------------------------------ crown / leaves / stem (wiggle pivots)
    leaves = []
    def leafpiv(name, at):
        p = L.empty(prefix + name, at, bod); leaves.append(p); return p
    if kind in ("pipkiko", "strawberry"):
        s = 1.0 if kind == "pipkiko" else 0.82
        p = leafpiv("Crown", (0, 0.02, top - 0.04))
        for k in range(7):
            a = k / 7 * math.tau + 0.2
            L.sphere(f"{prefix}Sepal{k}", 1.0, (math.sin(a) * 0.26 * s, math.cos(a) * 0.22 * s, 0.03), (0.11 * s, 0.34 * s, 0.035), M["leaf"] if k % 2 else M["leafdk"], p, 20, (0.3, 0, -a))
        L.cylinder(prefix + "Stem", 0.045 * s, 0.26 * s, (0.02, 0, 0.13 * s), m=M["leafdk"], parent=p, rot=(0, 0.25, 0), verts=12)
        L.sphere(prefix + "StemTip", 0.05 * s, (0.05, 0, 0.26 * s), m=M["leafdk"], parent=p, segs=12)
    elif kind in ("apple", "orange"):
        dz = -0.18 if kind == "apple" else -0.02
        p = leafpiv("Stem", (0, 0, top + dz))
        L.cylinder(prefix + "StemC", 0.045, 0.36, (0.03, 0, 0.16), m=M["stem"], parent=p, rot=(0, 0.22, 0), verts=12)
        L.sphere(prefix + "Leaf", 1.0, (0.24, -0.02, 0.24), (0.26, 0.12, 0.05), M["leaf"], p, 24, (0.2, -0.5, 0.2))
    elif kind == "grape":
        p = leafpiv("Stem", (0, 0, top - 0.03))
        L.cylinder(prefix + "StemC", 0.04, 0.3, (0, 0, 0.13), m=M["stem"], parent=p, rot=(0, -0.15, 0), verts=12)
        L.torus(prefix + "Curl", 0.09, 0.022, (0.12, 0, 0.26), m=M["leafdk"], parent=p, rot=(math.pi / 2, 0, 0))
        L.sphere(prefix + "Leaf", 1.0, (-0.22, 0.02, 0.22), (0.28, 0.14, 0.05), M["leaf"], p, 24, (0.2, 0.5, -0.2))
    elif kind == "banana":
        p = leafpiv("Stem", (0.33, 0, top - 0.05))
        L.cylinder(prefix + "StemC", 0.07, 0.26, (0.04, 0, 0.1), m=L.mat("FrBanStem", "#8a7a2a", 0.55), parent=p, rot=(0, 0.45, 0), verts=12)
        L.sphere(prefix + "StemTip", 0.07, (0.1, 0, 0.21), (1, 1, 0.5), M["stem"], p, 12)
        L.sphere(prefix + "Tip", 0.07, (0.3, 0, 0.0), (1, 1, 0.7), M["stem"], bod, 12)
    elif kind == "carrot":
        p = leafpiv("Tops", (0, 0, top - 0.06))
        for k, (a, ln) in enumerate(((-0.55, 0.5), (-0.2, 0.62), (0.2, 0.58), (0.55, 0.48), (0, 0.42))):
            L.sphere(f"{prefix}Top{k}", 1.0, (math.sin(a) * ln * 0.5, 0.06 * (k == 4), math.cos(a) * ln * 0.5), (0.1, 0.07, ln * 0.55), M["leaf"] if k % 2 else M["leafdk"], p, 20, (0, a, 0))
    elif kind == "broccoli":
        flo = L.mat("FrFloret", "#2e9440", 0.6, sheen=0.4, sss=0.08, bump=0.7, bump_scale=26)
        flo2 = L.mat("FrFloret2", "#3aa84c", 0.6, sheen=0.4, sss=0.08, bump=0.7, bump_scale=30)
        p = leafpiv("Crown", (0, 0.05, top - 0.12))
        L.sphere(prefix + "Flo", 0.56, (0, 0.05, 0.42), (1, 0.92, 0.9), flo, p, 32)
        for k in range(7):
            a = k / 7 * math.tau + 0.4
            L.sphere(f"{prefix}Flo{k}", 0.38 + 0.05 * (k % 2), (math.sin(a) * 0.52, math.cos(a) * 0.4 + 0.08, 0.22 + 0.06 * (k % 3)), (1, 0.9, 0.85), flo2 if k % 2 else flo, p, 24)
        for k, (x, y) in enumerate(((-0.25, -0.05), (0.25, 0.0), (0.0, 0.3))):
            L.sphere(f"{prefix}FloT{k}", 0.34, (x, y, 0.72), (1, 0.9, 0.8), flo2, p, 24)

    # ------------------------------------------------ arms (shoulder pivots) and legs
    az = top * (0.36 if kind not in ("carrot",) else 0.55)
    if kind in ("pipkiko", "strawberry"): az = top * 0.45
    if kind == "broccoli": az = top * 0.4
    arms = []
    for sx in (-1, 1):
        ax = _side(bvh, az, sx) - 0.04
        piv = L.empty(f"{prefix}Arm{sx}", (ax * sx, 0, az), bod)
        L.cylinder(f"{prefix}ArmC{sx}", 0.05, 0.42, (0, 0, -0.21), m=M["limb"], parent=piv, verts=12)
        L.sphere(f"{prefix}Hand{sx}", 0.1, (0, -0.01, -0.44), (1, 0.85, 1), M["glove"], piv, 20)
        L.sphere(f"{prefix}Thumb{sx}", 0.045, (0.05 * -sx, -0.07, -0.4), m=M["glove"], parent=piv, segs=12)
        arms.append((piv, sx))
    legs = []
    lx = 0.17 if kind not in ("carrot", "pipkiko", "strawberry") else 0.13
    for sx in (-1, 1):
        lg = L.empty(f"{prefix}Leg{sx}", (lx * sx, 0, LEG_H), root)
        L.cylinder(f"{prefix}LegC{sx}", 0.055, LEG_H, (0, 0, -LEG_H / 2), m=M["limb"], parent=lg, verts=12)
        L.sphere(f"{prefix}Shoe{sx}", 1.0, (0.02 * sx, -0.07, -LEG_H + 0.07), (0.14, 0.21, 0.1), M["shoe"], lg, 24)
        L.sphere(f"{prefix}Sole{sx}", 1.0, (0.02 * sx, -0.07, -LEG_H + 0.025), (0.145, 0.215, 0.035), M["sole"], lg, 16)
        legs.append((lg, sx))

    ch = Char(L, root, bod, eyes, mouth, leaves, arms, legs, kind)
    ch.height = LEG_H + top + (0.4 if kind == "carrot" else 0.1)
    ch.face_z = LEG_H + (ez + mz) / 2 + 0.1
    return ch


class Char:
    height = 2.2
    face_z = 1.3

    def __init__(self, L, root, bod, eyes, mouth, leaves, arms, legs, kind):
        self.L, self.root, self.bod, self.eyes, self.mouth = L, root, bod, eyes, mouth
        self.leaves, self.arms, self.legs, self.kind = leaves, arms, legs, kind
        self.ph = (sum(map(ord, kind)) % 17) / 17.0
        self.pupils = [c for sock, lid in eyes for c in sock.children if any(k in c.name for k in ("Iris", "Pupil", "Glint"))]   # small phase offset so friends don't move like clones

    def pose(self, f, t, s):
        L = self.L
        talk, e, beat, bar = s.get("talk", 0), s.get("energy", 0.3), s.get("beat", 0), s.get("bar", 0)
        jump, wave, singing = s.get("jump", 0), s.get("wave", 0), s.get("singing", False)
        hop = abs(math.sin(math.pi * beat))
        bounce = hop * 0.14 * e + jump * hop * 0.42
        land = max(0.0, 1 - hop * 3.5) * (e + jump * 0.5)
        sq = 1 - land * 0.13 + hop * e * 0.05 + talk * 0.02
        breathe = math.sin(t * 2.3 + self.ph * 6) * 0.015
        sway = math.sin((bar + self.ph * 0.25) * 2 * math.pi)
        xy = 1 / math.sqrt(max(0.5, sq))
        L.key(self.bod, "location", f, (sway * 0.09 * e, 0, LEG_H + bounce))
        L.key(self.bod, "scale", f, (xy, xy, sq + breathe))
        L.key(self.bod, "rotation_euler", f, (-talk * 0.05, sway * 0.11 * e, -s.get("look", 0)))
        step = math.sin(bar * 4 * math.pi)
        for lg, sx in self.legs:
            lift = max(0.0, step * sx) * 0.1 * e
            L.key(lg, "location", f, (lg.location.x, 0, LEG_H + bounce + lift))
            L.key(lg, "rotation_euler", f, (-lift * 1.5, 0, 0))
        L.key(self.mouth, "scale", f, (1 + talk * 0.12, 1, 0.42 + talk * 0.95))
        pump = math.sin(beat * 2 * math.pi)
        for piv, sx in self.arms:
            a = 0.42 + (0.35 if singing else 0.0) + pump * sx * 0.3 * e
            fwd = -0.25 - (0.25 if singing else 0) * (0.5 + 0.5 * pump)
            if wave:
                a = (2.5 if sx > 0 else 2.1) + math.sin(t * 13 + sx) * 0.3
                fwd = -0.1
            L.key(piv, "rotation_euler", f, (fwd, -sx * a, 0))
        for k, p in enumerate(self.leaves):
            L.key(p, "rotation_euler", f, (math.sin(t * 3.1 + k) * 0.05 + land * 0.12, math.sin(beat * 2 * math.pi) * 0.1 * e, 0))
        closed = s.get("blink", False)
        for sock, lid in self.eyes:
            L.key(lid, "rotation_euler", f, (math.radians(80 if closed else -100), 0, 0))
        for o in self.pupils:   # hidden while the lid is shut, so nothing pokes through
            o.hide_render = bool(closed)
