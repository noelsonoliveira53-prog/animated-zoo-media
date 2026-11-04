"""Shape friends for Bloop's Color Lab: circle, square, triangle, star, heart with faces, arms and legs. See API.md.

opts: shape = circle | square | triangle | star | heart (default circle), color = hex.
"""
import math
from chars.bloop import jelly_mat, make_mouth, mouth_talk, INK

D = 0.5        # body thickness
LEGH = 0.55    # leg length (body bottom sits here)


def chaikin(pts, it=2):
    for _ in range(it):
        out = []
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            out += [(a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25), (a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75)]
        pts = out
    return pts


def outline(kind):
    """2D outline (x, z), counter-clockwise, about 1.5 units tall, z from 0 up. Returns (pts, face_z, half_width_at_face)."""
    if kind == "square":
        pts = []
        for i in range(56):
            a = i / 56 * math.tau; c, s = math.cos(a), math.sin(a)
            pts.append((0.72 * math.copysign(abs(c) ** 0.4, c), 0.72 + 0.72 * math.copysign(abs(s) ** 0.4, s)))
        return pts, 0.82, 0.72
    if kind == "triangle":
        base = [(-0.92, 0.0), (0.92, 0.0), (0.0, 1.62)]
        return chaikin(base, 4), 0.55, 0.6
    if kind == "star":
        pts = []
        for i in range(10):
            a = math.pi / 2 + i * math.pi / 5; r = 0.92 if i % 2 == 0 else 0.42
            pts.append((math.cos(a) * r, 0.75 + math.sin(a) * r))
        return chaikin(pts, 3), 0.75, 0.5
    if kind == "heart":
        pts = []
        for i in range(64):
            t = i / 64 * math.tau
            x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((x * 0.055, 0.95 + y * 0.055))
        pts.reverse()
        return pts, 0.85, 0.7
    return [(0.78 * math.cos(i / 56 * math.tau), 0.78 + 0.78 * math.sin(i / 56 * math.tau)) for i in range(56)], 0.8, 0.74


def extrude(L, name, pts, depth, m, parent):
    import bpy
    pts = [p for p in pts]
    xs = [p[0] for p in pts]; zs = [p[1] for p in pts]
    ccw = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts))) > 0
    if not ccw: pts = pts[::-1]
    n = len(pts)
    verts = [(x, -depth / 2, z) for x, z in pts] + [(x, depth / 2, z) for x, z in pts]
    faces = [list(range(n)), [n + i for i in range(n)][::-1]]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, n + i, n + j, j])
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    import bmesh
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); L.scene().collection.objects.link(o)
    o.data.materials.append(m); o.parent = parent
    bv = o.modifiers.new("Bevel", "BEVEL"); bv.width = 0.16; bv.segments = 5; bv.limit_method = "ANGLE"; bv.angle_limit = math.radians(50)
    try: bv.harden_normals = True
    except Exception: pass
    for p in me.polygons: p.use_smooth = True
    return o


def build(L, prefix="Shape", loc=(0, 0, 0), scale=1.0, **opts):
    kind = opts.get("shape", "circle"); hexc = opts.get("color", "#ff5252")
    body_m = jelly_mat(L, prefix + "Body", hexc)
    body_m.node_tree.nodes["Principled BSDF"].inputs["Subsurface Weight"].default_value = 0.25
    limb = L.mat("ShapeLimb", INK, 0.45, coat=0.5)
    white = L.mat("ShapeGlove", "#ffffff", 0.35, coat=0.6, sheen=0.3)
    shoe = L.mat("ShapeShoe" + hexc, hexc, 0.3, coat=0.9)
    pts, fz, hw = outline(kind)
    root = L.empty(prefix, loc); root.scale = (scale,) * 3
    rig = L.empty(prefix + "Rig", (0, 0, LEGH), root)
    extrude(L, prefix + "Body", pts, D, body_m, rig)
    fy = -D / 2
    er = 0.22 if kind != "star" else 0.19
    eyes = L.eye_pair(prefix, rig, spacing=er * 1.25, z=fz + 0.1, y=fy + er * 0.25, r=er, iris_hex="#2a1a55", lid_mat=body_m, toward=0.12)
    mouth = make_mouth(L, prefix, rig, (0, fy - 0.03, fz - 0.24), w=0.2, tilt=0.0)
    cheek = L.mat("BloopCheek", "#ff8fb0", 0.55, sss=0.2)
    for sx in (-1, 1):
        L.sphere(f"{prefix}Cheek{sx}", 0.08, (sx * er * 2.0, fy - 0.01, fz - 0.14), (1, 0.3, 0.62), cheek, rig, 12)
    arms, legs = [], []
    for sx in (-1, 1):
        piv = L.empty(f"{prefix}Arm{sx}", (sx * (hw - 0.05), 0, fz - 0.15), rig)
        L.cylinder(f"{prefix}ArmS{sx}", 0.055, 0.5, (sx * 0.25, 0, 0), (1, 1, 1), limb, piv, (0, math.pi / 2, 0), 12)
        L.sphere(f"{prefix}Glove{sx}", 0.12, (sx * 0.52, -0.02, 0), (1, 0.85, 1), white, piv, 16)
        arms.append((piv, sx))
        lg = L.empty(f"{prefix}Leg{sx}", (sx * 0.28, 0, LEGH + 0.06), root)
        L.cylinder(f"{prefix}Shin{sx}", 0.06, LEGH, (0, 0, -LEGH / 2), (1, 1, 1), limb, lg, verts=12)
        L.sphere(f"{prefix}Shoe{sx}", 0.17, (0, -0.08, -LEGH + 0.02), (0.85, 1.25, 0.55), shoe, lg, 20)
        legs.append((lg, sx))
    ch = Char(L, root, rig, eyes, mouth, arms, legs)
    ch.height = LEGH + max(p[1] for p in pts)
    ch.face_z = LEGH + fz
    return ch


class Char:
    height = 2.1
    face_z = 1.35

    def __init__(self, L, root, rig, eyes, mouth, arms, legs):
        self.L, self.root, self.rig, self.eyes, self.mouth, self.arms, self.legs = L, root, rig, eyes, mouth, arms, legs
        self.ph = (hash(root.name) % 100) / 100.0

    def pose(self, f, t, s):
        L = self.L
        talk, e, beat, bar = s.get("talk", 0), s.get("energy", 0.3), s.get("beat", 0), s.get("bar", 0)
        jump = s.get("jump", 0); wave = s.get("wave", 0)
        hop = abs(math.sin(math.pi * beat))
        lift = hop * (0.1 * e + jump * 0.5)
        land = max(0.0, 1 - hop * 3.5) * (0.5 * e + jump)
        sq = 1 - land * 0.12 + hop * 0.05 * (e + jump) + math.sin(t * 2.3 + self.ph * 6) * 0.012
        sway = math.sin(bar * 2 * math.pi + self.ph)
        L.key(self.rig, "location", f, (sway * 0.08 * e, 0, LEGH + lift))
        L.key(self.rig, "scale", f, (1 / math.sqrt(sq), 1, sq))
        L.key(self.rig, "rotation_euler", f, (talk * 0.05, sway * 0.12 * e, -s.get("look", 0)))
        mouth_talk(L, self.mouth, f, talk)
        for piv, sx in self.arms:
            sw = math.sin(beat * math.pi * 2 + (0 if sx > 0 else math.pi)) * 0.45 * e
            up = wave * (2.1 + math.sin(t * 12 + sx) * 0.4)
            L.key(piv, "rotation_euler", f, (0, -sx * (-0.95 + sw + up + jump * hop * 0.9), 0))
        for lg, sx in self.legs:
            step = max(0.0, math.sin(beat * math.pi * 2 + (0 if sx > 0 else math.pi))) * 0.12 * e
            L.key(lg, "location", f, (lg.location.x, 0, LEGH + 0.06 + lift + step))
        closed = s.get("blink", False)
        for sock, lid in self.eyes:
            L.key(lid, "rotation_euler", f, (math.radians(78 if closed else -110), 0, 0))
