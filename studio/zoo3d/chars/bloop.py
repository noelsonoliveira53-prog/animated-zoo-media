"""Bloop, the wobbly jelly color blob who hosts Bloop's Color Lab (3D). See API.md.

opts:
  color           hex, Bloop's starting color (default house purple #9d6bff)
  color_schedule  [[t_seconds, "#hex"], ...] color changes over the song (blends in ~0.25 s with a jelly "pop")
  scale           handled by the engine (root scale is set here too)
"""
import math

HOME = "#9d6bff"
INK = "#3d2a7a"


# ------------------------------------------------------------------ shared helpers (shape.py uses these too)
def lin_mix(a, b, k):
    return tuple(x + (y - x) * k for x, y in zip(a, b))


def jelly_mat(L, name, hexcol, lite=0.0):
    """Glossy candy jelly: subsurface + clearcoat + a whisper of self-glow so it stays luminous in EEVEE."""
    m = L.mat(name, hexcol, 0.1, coat=1.0, sss=0.5)
    b = m.node_tree.nodes["Principled BSDF"]
    for k, v in (("Coat Roughness", 0.04), ("Subsurface Scale", 0.35), ("Specular IOR Level", 0.65), ("Emission Strength", 0.12)):
        if k in b.inputs: b.inputs[k].default_value = v
    if "Subsurface Radius" in b.inputs: b.inputs["Subsurface Radius"].default_value = (1.0, 0.7, 0.55)
    set_jelly_color(m, L.rgb(hexcol), lite)
    return m


def set_jelly_color(m, lin, lite=0.0):
    b = m.node_tree.nodes["Principled BSDF"]
    c = lin_mix(lin, (1, 1, 1), lite)
    b.inputs["Base Color"].default_value = (*c, 1)
    if "Emission Color" in b.inputs: b.inputs["Emission Color"].default_value = (*c, 1)


def _cut(L, o, keep):
    """Delete mesh vertices where keep(co) is False (object mode)."""
    import bmesh
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not keep(v.co)], context="VERTS")
    bm.to_mesh(o.data); bm.free()
    return o


def make_mouth(L, prefix, parent, loc, w=0.2, tilt=0.0, ink=INK):
    """Cartoon mouth: a soft smile curve plus a D-shaped open mouth (dark, with a pink tongue) that grows with talk.
    Returns the open-mouth object; scale z = 0.05 + talk."""
    dark = L.mat("BloopMouthIn", "#4a1638", 0.5, coat=0.4)
    tongue = L.mat("BloopTongue", "#ff7aa8", 0.45, coat=0.3, sss=0.2)
    inkm = L.mat("BloopInk", ink, 0.4, coat=0.5)
    piv = L.empty(prefix + "Mouth", loc, parent); piv.rotation_euler = (tilt, 0, 0)
    sm = L.torus(prefix + "Smile", w * 0.62, w * 0.11, (0, 0, w * 0.08), (1, 1, 0.9), inkm, piv, (math.pi / 2, 0, 0))
    _cut(L, sm, lambda c: c.y < 0.02)
    op = L.sphere(prefix + "MouthOpen", 1.0, (0, -0.005, w * 0.06), (w * 0.8, w * 0.35, 0.02), dark, piv, 32)
    _cut(L, op, lambda c: c.z <= 0.02)
    L.sphere(prefix + "Tongue", 0.6, (0, -0.25, -0.62), (0.7, 0.6, 0.45), tongue, op, 20)
    op["w"] = w
    return op


def mouth_talk(L, op, f, talk):
    w = op["w"]
    L.key(op, "scale", f, (w * 0.8 * (1 - talk * 0.15), w * 0.35, 0.02 + talk * w * 0.85))


def color_at(sched, t, base):
    """(current linear color, seconds since the last change) from a [[t, hex], ...] schedule."""
    if not sched: return base, 99.0
    idx = -1
    for k, (t0, _) in enumerate(sched):
        if t0 <= t: idx = k
        else: break
    if idx < 0: return base, 99.0
    t0, cur = sched[idx]
    prev = sched[idx - 1][1] if idx > 0 else base
    k = max(0.0, min(1.0, (t - t0) / 0.25)); k = k * k * (3 - 2 * k)
    return lin_mix(prev, cur, k), t - t0


def norm_sched(L, sched):
    return [(float(t0), L.rgb(h)) for t0, h in sorted(sched or [], key=lambda x: x[0])]


# ------------------------------------------------------------------ Bloop
R = 1.08          # body radius
LIFT = 0.80       # body center height above the ground


def _shape(x, y, z):
    """Unit-sphere point -> gumdrop jelly body (wide soft bottom, rounded top), centered at rig origin + LIFT."""
    k = 1 + 0.17 * (1 - z) * 0.5
    zz = z * 1.06 if z > 0 else z
    if zz < -0.58: zz = -0.58 + (zz + 0.58) * 0.32
    return x * k * R, y * k * R * 0.9, zz * R + LIFT


def surf_y(zn, xn=0.0):
    """Front surface y of the body at unit height zn (and unit x offset xn)."""
    k = 1 + 0.17 * (1 - zn) * 0.5
    yy = math.sqrt(max(0.0, 1 - zn * zn - xn * xn))
    return -yy * k * R * 0.9


def build(L, prefix="Bloop", loc=(0, 0, 0), scale=1.0, **opts):
    base_hex = opts.get("color", HOME)
    jelly = jelly_mat(L, prefix + "Jelly", base_hex)
    lite = jelly_mat(L, prefix + "JellyLite", base_hex, 0.45)
    M = {
        "ink": L.mat("BloopInk", INK, 0.4, coat=0.5),
        "lens": L.mat("GoggleLens", "#bde9ff", 0.05, coat=1.0, emission="#bde9ff", emit=0.25),
        "rim": L.mat("GoggleRim", "#ffffff", 0.25, coat=0.8),
        "cheek": L.mat("BloopCheek", "#ff8fb0", 0.55, sss=0.2),
    }
    root = L.empty(prefix, loc); root.scale = (scale,) * 3
    rig = L.empty(prefix + "Rig", (0, 0, 0), root)

    body = L.sphere(prefix + "Body", 1.0, (0, 0, 0), (1, 1, 1), jelly, rig, 48)
    for v in body.data.vertices:
        v.co = _shape(*v.co)
    # soft little drop-tip on top, like a jelly swirl
    tip = L.sphere(prefix + "Tip", 0.2, (0.05, 0.02, LIFT + R * 1.06 + 0.06), (1, 0.9, 1.25), jelly, rig, 24, (0, 0.35, 0))
    # glossy highlight streak (the bright jelly "shine" of the 2D art)
    hz = 0.5; hx = -0.42
    L.sphere(prefix + "Shine", 0.14, (hx * R * 1.05, surf_y(hz, hx) + 0.03, LIFT + hz * R * 1.06), (1.6, 0.25, 0.7), lite, rig, 16, (0.5, 0, 0.7))

    # face
    ez = 0.18
    eyes = L.eye_pair(prefix, rig, spacing=0.36, z=LIFT + ez * R, y=surf_y(ez, 0.33) + 0.12, r=0.3, iris_hex="#2a1a55", lid_mat=jelly, toward=0.3)
    mz = -0.2
    mouth = make_mouth(L, prefix, rig, (0, surf_y(mz) + 0.01, LIFT + mz * R), w=0.34, tilt=-0.22)
    for sx in (-1, 1):
        L.sphere(f"{prefix}Cheek{sx}", 0.13, (0.6 * sx, surf_y(-0.1, 0.56) + 0.03, LIFT - 0.1 * R), (1, 0.35, 0.62), M["cheek"], rig, 16, (0, 0, 0.5 * sx))

    # tiny lab goggles pushed up on the forehead
    gz = 0.62
    rad = math.sqrt(1 - gz * gz) * (1 + 0.17 * (1 - gz) * 0.5) * R
    L.torus(prefix + "Strap", rad + 0.015, 0.045, (0, 0, LIFT + gz * R * 1.06), (1, 0.9, 0.55), M["ink"], rig, (0.0, 0, 0))
    tilt = math.pi / 2 - math.asin(gz)
    for sx in (-1, 1):
        gx = 0.24 * sx
        gy = surf_y(gz, gx / R) - 0.04
        g = L.empty(f"{prefix}Goggle{sx}", (gx, gy, LIFT + gz * R * 1.06), rig); g.rotation_euler = (tilt, 0, -0.35 * sx)
        L.torus(f"{prefix}GRim{sx}", 0.15, 0.045, (0, 0, 0), (1, 1, 1), M["rim"], g)
        L.cylinder(f"{prefix}GLens{sx}", 0.14, 0.04, (0, 0, 0.01), (1, 1, 1), M["lens"], g, verts=32)
    L.cylinder(prefix + "GBridge", 0.03, 0.12, (0, surf_y(gz) - 0.05, LIFT + gz * R * 1.06), (1, 1, 1), M["rim"], rig, (0, math.pi / 2, 0), 12)

    # little jelly arms
    arms = []
    for sx in (-1, 1):
        az = -0.12
        piv = L.empty(f"{prefix}Arm{sx}", (sx * 1.0 * R, -0.05, LIFT + az * R), rig)
        L.sphere(f"{prefix}ArmS{sx}", 0.15, (sx * 0.16, 0, -0.18), (1, 1, 2.0), jelly, piv, 20, (0, -0.5 * sx, 0))
        L.sphere(f"{prefix}Hand{sx}", 0.16, (sx * 0.3, -0.02, -0.4), (1, 0.9, 1), jelly, piv, 20)
        arms.append((piv, sx))

    # two floating bubbles above the head (from the 2D logo)
    bubbles = [L.sphere(f"{prefix}Bub{k}", r, p, (1, 1, 1), lite, root, 20)
               for k, (r, p) in enumerate(((0.12, (0.62, 0.1, 2.35)), (0.075, (0.86, 0.1, 2.6))))]
    return Char(L, root, rig, eyes, mouth, arms, bubbles, jelly, lite, L.rgb(base_hex), norm_sched(L, opts.get("color_schedule") or [[0.0, base_hex]]))


class Char:
    height = 2.3
    face_z = 1.25

    def __init__(self, L, root, rig, eyes, mouth, arms, bubbles, jelly, lite, base, sched):
        self.L, self.root, self.rig, self.eyes, self.mouth, self.arms = L, root, rig, eyes, mouth, arms
        self.bubbles, self.jelly, self.lite, self.base, self.sched = bubbles, jelly, lite, base, sched
        self.bub0 = [tuple(b.location) for b in bubbles]

    def pose(self, f, t, s):
        L = self.L
        talk, e, beat, bar = s.get("talk", 0), s.get("energy", 0.3), s.get("beat", 0), s.get("bar", 0)
        jump = s.get("jump", 0)
        # color
        col, dt = color_at(self.sched, s.get("t_section", t), self.base)
        set_jelly_color(self.jelly, col); set_jelly_color(self.lite, col, 0.45)
        pop = math.exp(-dt * 5.0) * math.sin(dt * 26) * 0.14 if dt < 1.2 else 0.0
        # bounce + jelly squash/stretch
        hop = abs(math.sin(math.pi * beat))
        lift = hop * (0.1 * e + jump * 0.3)
        land = max(0.0, 1 - hop * 3.5) * (0.6 * e + jump)
        wob = math.sin(beat * 2 * math.pi * 2) * 0.035 * e + math.sin(t * 7.3) * 0.012
        sq = 1 - land * 0.16 + hop * 0.06 * (e + jump) + wob + pop
        breathe = math.sin(t * 2.2) * 0.015
        sway = math.sin(bar * 2 * math.pi)
        L.key(self.rig, "location", f, (sway * 0.1 * e, 0, lift))
        L.key(self.rig, "scale", f, (1 / math.sqrt(sq), 1 / math.sqrt(sq), sq * (1 + breathe)))
        L.key(self.rig, "rotation_euler", f, (talk * 0.06 - 0.03, sway * 0.1 * e, -s.get("look", 0)))
        # mouth
        mouth_talk(L, self.mouth, f, talk)
        # arms: swing on the beat, wave / celebrate
        wave = s.get("wave", 0)
        for piv, sx in self.arms:
            sw = math.sin(beat * math.pi * 2 + (0 if sx > 0 else math.pi)) * 0.35 * e
            up = wave * (1.9 + math.sin(t * 13 + sx) * 0.35) if sx > 0 else wave * 1.2
            L.key(piv, "rotation_euler", f, (0, -sx * (0.25 + sw + up + jump * hop * 0.6), 0))
        closed = s.get("blink", False)
        for sock, lid in self.eyes:
            L.key(lid, "rotation_euler", f, (math.radians(78 if closed else -110), 0, 0))
        for k, (b, p0) in enumerate(zip(self.bubbles, self.bub0)):
            L.key(b, "location", f, (p0[0] + math.sin(t * 1.3 + k) * 0.06, p0[1], p0[2] + lift + math.sin(t * 2.1 + k * 2) * 0.08))
