"""Gizmo, the friendly robot host of Gizmo Explains (3D). Matches the 2D GIZMO look: a rounded silver TV-head body,
a dark navy screen with glowing cyan eyes and a cyan D-shaped smile, a cyan antenna ball, side arms, pink cheeks, a cyan chest
star and a hover base with little thruster flames. Faces -Y, about 2.4 units tall.

opts: color (accent plastic, default orange), variant ("mini" = sidekick: twin antennas, round eyes), scale.
"""
import math
import bpy, bmesh


def _cut(o, keep):
    """Delete the vertices of a mesh object where keep(co) is False."""
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not keep(v.co)], context="VERTS")
    bm.to_mesh(o.data); bm.free()
    return o


def star_mesh(name, r_out, r_in, depth, m=None, parent=None, loc=(0, 0, 0), rot=(math.pi / 2, 0, 0), points=5):
    """Chunky 5-point star, built in XY then rotated to face -Y."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = []
    for k in range(points * 2):
        a = math.pi / 2 + k * math.pi / points
        rr = r_out if k % 2 == 0 else r_in
        vs.append(bm.verts.new((math.cos(a) * rr, math.sin(a) * rr, 0)))
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in ext["geom"]:
        if isinstance(v, bmesh.types.BMVert): v.co.z += depth
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    if m is not None: me.materials.append(m)
    b = o.modifiers.new("Bevel", "BEVEL"); b.width = depth * 0.35; b.segments = 3; b.use_clamp_overlap = True
    if parent is not None: o.parent = parent
    o.location = loc; o.rotation_euler = rot
    return o


def build(L, prefix="Gizmo", loc=(0, 0, 0), scale=1.0, color="#ff8a1f", variant="", **_):
    mini = variant == "mini"
    P = prefix
    M = {
        "metal": L.mat(P + "Metal", "#eef2f8", 0.2, coat=1.0, metal=0.18),
        "steel": L.mat(P + "Steel", "#9aa6bd", 0.3, coat=0.6, metal=0.6),
        "accent": L.mat(P + "Accent" + color, color, 0.28, coat=1.0),
        "screen": L.mat(P + "Screen", "#14214d", 0.08, coat=1.0),
        "glow": L.mat("GizmoGlow", "#7ef9ff", 0.2, emission="#7ef9ff", emit=4.0),
        "glint": L.mat("GizmoGlint", (1, 1, 1), 0.0, emission=(1, 1, 1), emit=6.0),
        "cheek": L.mat("GizmoCheek", "#ff8fb0", 0.45, coat=0.5, emission="#ff8fb0", emit=0.4),
        "flame": L.mat("GizmoFlame", "#ffb627", 0.4, emission="#ff9a1c", emit=6.0),
        "flame2": L.mat("GizmoFlameCore", "#fff3b0", 0.4, emission="#fff1a8", emit=8.0),
        "ant": L.mat("GizmoAntBall", "#5ff3ff", 0.15, coat=1.0, emission="#5ff3ff", emit=3.0),
    }
    root = L.empty(P, loc); root.scale = (scale,) * 3
    rig = L.empty(P + "Rig", (0, 0, 1.45), root)          # body centre; everything above the hover pod hangs here
    # ---- body: big soft rounded box (the 2D head/body)
    L.cube(P + "Body", 1, (0, 0, 0), (1.56, 1.22, 1.24), M["metal"], rig, bevel=0.42, segs=6)
    # accent top cap and side bands (coloured plastic panels)
    L.cube(P + "Cap", 1, (0, 0.02, 0.6), (1.0, 0.8, 0.14), M["accent"], rig, bevel=0.06, segs=3)
    # ---- face screen (dark glossy visor)
    L.cube(P + "Visor", 1, (0, -0.56, 0.06), (1.18, 0.14, 0.8), M["screen"], rig, bevel=0.06 if mini else 0.065, segs=4)
    L.cube(P + "VisorRim", 1, (0, -0.545, 0.06), (1.26, 0.12, 0.88), M["steel"], rig, bevel=0.07, segs=4)
    face = L.empty(P + "Face", (0, -0.64, 0.06), rig)
    eyes = []
    for sx in (-1, 1):
        sock = L.empty(f"{P}Eye{sx}", (0.25 * sx, 0, 0.08), face)
        if mini:
            L.sphere(f"{P}EyeGlow{sx}", 0.13, (0, 0, 0), (1, 0.32, 1), M["glow"], sock, 32)
        else:
            L.sphere(f"{P}EyeGlow{sx}", 0.13, (0, 0, 0), (0.9, 0.32, 1.25), M["glow"], sock, 32)
        L.sphere(f"{P}EyeGlint{sx}", 0.04, (0.045, -0.04, 0.06), (1, 0.5, 1), M["glint"], sock, 12)
        L.sphere(f"{P}EyeGlint2{sx}", 0.018, (-0.04, -0.04, -0.06), (1, 0.5, 1), M["glint"], sock, 10)
        eyes.append(sock)
    # mouth: a glowing D-shaped light (flat top, round bottom). Closed it reads as a smile, `talk` opens it downward.
    mouth = L.empty(P + "Mouth", (0, 0, -0.14), face)
    jaw = L.sphere(P + "MouthD", 0.15, (0, 0, 0), (1, 0.18, 1), M["glow"], mouth, 32)
    _cut(jaw, lambda co: co.z < 0.001)
    sm = None
    for sx in (-1, 1):
        L.sphere(f"{P}Cheek{sx}", 0.09, (0.46 * sx, -0.02, -0.17), (1, 0.25, 0.65), M["cheek"], face, 16)
    # chest star on an accent plate
    L.cube(P + "Plate", 1, (0, -0.57, -0.47), (0.62, 0.1, 0.22), M["accent"], rig, bevel=0.05, segs=3)
    star_mesh(P + "Star", 0.1, 0.045, 0.04, M["glow"], rig, (0, -0.62, -0.47))
    # ear pods with glowing rings (where the 2D ears/side rects are)
    for sx in (-1, 1):
        L.cylinder(f"{P}Ear{sx}", 0.2, 0.16, (0.8 * sx, 0, 0.12), m=M["accent"], parent=rig, rot=(0, math.pi / 2, 0), verts=32)
        L.torus(f"{P}EarRing{sx}", 0.13, 0.025, (0.885 * sx, 0, 0.12), m=M["glow"], parent=rig, rot=(0, math.pi / 2, 0))
    # bolts
    for sx in (-1, 1):
        for sz in (-1, 1):
            L.sphere(P + "Bolt", 0.035, (0.66 * sx, -0.6, 0.06 + 0.5 * sz), m=M["steel"], parent=rig, segs=12)
    # ---- antenna (bobs with lag)
    ants = []
    spots = ((-0.22, 0.25), (0.22, -0.25)) if mini else ((0.0, 0.0),)
    for k, (ax, lean) in enumerate(spots):
        a = L.empty(f"{P}Ant{k}", (ax, 0.05, 0.64), rig)
        L.cylinder(P + "AntBase", 0.08, 0.08, (0, 0, 0.06), m=M["steel"], parent=a, verts=20)
        L.cylinder(P + "AntStalk", 0.028, 0.34, (0, 0, 0.25), m=M["steel"], parent=a, verts=12)
        L.sphere(P + "AntBall", 0.105, (0, 0, 0.46), m=M["ant"], parent=a, segs=24)
        L.sphere(P + "AntGlint", 0.03, (-0.035, -0.07, 0.5), m=M["glint"], parent=a, segs=10)
        ants.append((a, lean))
    # ---- arms (shoulder -> forearm -> mitten hand)
    arms = []
    for sx in (-1, 1):
        sh = L.empty(f"{P}Arm{sx}", (0.78 * sx, -0.02, -0.24), rig)
        L.sphere(P + "Shoulder", 0.15, (0, 0, 0), m=M["steel"], parent=sh, segs=24)
        L.cylinder(P + "Upper", 0.085, 0.36, (0.2 * sx, 0, 0), m=M["metal"], parent=sh, rot=(0, math.pi / 2, 0), verts=20)
        el = L.empty(f"{P}Elbow{sx}", (0.4 * sx, 0, 0), sh)
        L.sphere(P + "ElbowBall", 0.1, (0, 0, 0), m=M["steel"], parent=el, segs=20)
        L.cylinder(P + "Fore", 0.08, 0.32, (0.18 * sx, 0, 0), m=M["metal"], parent=el, rot=(0, math.pi / 2, 0), verts=20)
        L.torus(P + "Cuff", 0.09, 0.03, (0.34 * sx, 0, 0), m=M["accent"], parent=el, rot=(0, math.pi / 2, 0))
        L.sphere(P + "Hand", 0.15, (0.47 * sx, 0, 0), (0.95, 0.8, 1.05), M["accent"], el, 24)
        L.sphere(P + "Thumb", 0.065, (0.42 * sx, -0.11, 0.09), m=M["accent"], parent=el, segs=16)
        arms.append((sh, el, sx))
    # ---- hover pod + thruster flames (rides under the body, lags a touch)
    pod = L.empty(P + "Pod", (0, 0, 0.55), root)
    L.sphere(P + "PodShell", 0.5, (0, 0, 0.02), (1.1, 0.95, 0.5), M["steel"], pod, 40)
    L.torus(P + "PodBand", 0.5, 0.06, (0, 0, 0.06), (1.1, 0.95, 1), M["accent"], pod)
    L.cylinder(P + "Neck", 0.3, 0.3, (0, 0, 0.28), m=M["steel"], parent=pod, verts=28)
    flames = []
    for sx in ((0,) if mini else (-0.22, 0.22)):
        L.cylinder(P + "Nozzle", 0.1, 0.12, (sx, 0, -0.22), m=M["metal"], parent=pod, verts=20)
        fl = L.empty(P + "Flame", (sx, 0, -0.28), pod)
        L.cone(P + "FlameOut", 0.09, 0.0, 0.34, (0, 0, -0.17), m=M["flame"], parent=fl, rot=(math.pi, 0, 0), verts=20)
        L.cone(P + "FlameIn", 0.05, 0.0, 0.2, (0, -0.01, -0.1), m=M["flame2"], parent=fl, rot=(math.pi, 0, 0), verts=16)
        flames.append(fl)
    glow_ring = L.torus(P + "HoverRing", 0.42, 0.03, (0, 0, 0.015), (1.2, 1.0, 0.2), M["glow"], root)
    ch = Char(L, root, rig, eyes, jaw, sm, mouth, ants, arms, pod, flames, glow_ring)
    if mini:
        ch.height = 2.5; ch.face_z = 1.5
    return ch


class Char:
    height = 2.4      # top of antenna above root (world units at scale 1)
    face_z = 1.5      # camera aim height for close-ups (the screen face)

    def __init__(self, L, root, rig, eyes, jaw, smile, mouth, ants, arms, pod, flames, ring):
        self.L, self.root, self.rig, self.eyes, self.jaw, self.smile, self.mouth = L, root, rig, eyes, jaw, smile, mouth
        self.ants, self.arms, self.pod, self.flames, self.ring = ants, arms, pod, flames, ring

    def pose(self, f, t, s):
        L = self.L
        talk, e, beat, bar = s.get("talk", 0), s.get("energy", 0.3), s.get("beat", 0), s.get("bar", 0)
        jump = s.get("jump", 0); wave = s.get("wave", 0)
        hop = abs(math.sin(math.pi * beat))
        bounce = hop * 0.16 * e + jump * hop * 0.42
        land = max(0.0, 1 - hop * 4) * e
        sq = 1 - land * 0.08 + hop * 0.02 * e
        hover = math.sin(t * 2.2) * 0.05
        sway = math.sin(bar * 2 * math.pi)
        z = 1.45 + hover + bounce
        L.key(self.rig, "location", f, (sway * 0.1 * e, 0, z))
        L.key(self.rig, "scale", f, (1 / math.sqrt(sq), 1 / math.sqrt(sq), sq))
        tilt = sway * 0.1 * e
        L.key(self.rig, "rotation_euler", f, (talk * 0.06 - 0.03, tilt, -s.get("look", 0) + math.sin(t * 0.7) * 0.04))
        # pod follows with a little lag; flames flicker and stretch on jumps
        lag = math.sin(math.pi * ((beat - 0.12) % 1.0))
        pz = 0.55 + hover * 0.8 + (lag * 0.16 * e + jump * lag * 0.42) * 0.9
        L.key(self.pod, "location", f, (sway * 0.08 * e, 0, pz))
        L.key(self.pod, "rotation_euler", f, (0, tilt * 0.6, 0))
        for k, fl in enumerate(self.flames):
            fk = 0.85 + 0.18 * math.sin(t * 37 + k * 1.7) + 0.1 * math.sin(t * 23 + k) + jump * (1 - hop) * 0.5 + bounce * 0.8
            L.key(fl, "scale", f, (1 - 0.08 * math.sin(t * 31 + k), 1, fk))
        rs = 1.0 - (bounce + hover) * 0.6
        L.key(self.ring, "scale", f, (1.2 * rs, 1.0 * rs, 0.2))
        # mouth: open glow grows with talk, smile widens
        L.key(self.jaw, "scale", f, (1 + talk * 0.08, 0.18, 0.36 + talk * 0.7))
        # eyes: blink by squashing, happy squint on the beat when singing, glance with look
        closed = s.get("blink", False)
        sy = 0.08 if closed else (1 - 0.12 * talk)
        for sock in self.eyes:
            L.key(sock, "scale", f, (1 + (0.1 if closed else 0), 1, sy))
        # antenna: springy lag behind the bounce
        for a, lean in self.ants:
            wob = math.cos(math.pi * beat) * 0.22 * e + jump * math.cos(math.pi * beat) * 0.25
            L.key(a, "rotation_euler", f, (wob * 0.6 + math.sin(t * 3.1) * 0.05, lean + math.sin(t * 2.3 + lean) * 0.08 + tilt * -1.5, 0))
        # arms: dance pumps on the beat; wave = right arm high and waving, left arm cheers
        b2 = math.sin(beat * math.pi * 2)
        for sh, el, sx in self.arms:
            side = 1 if sx > 0 else -1
            pump = b2 * (1 if sx > 0 else -1)
            down = 0.95 - e * 0.35
            if wave:
                if sx > 0:
                    lift = -1.5 + math.sin(t * 9) * 0.12
                    bend = 0.9 + math.sin(t * 12) * 0.45
                else:
                    lift = -0.9 + pump * 0.25
                    bend = 0.5
            else:
                lift = down - pump * 0.45 * e - jump * hop * 0.5
                bend = 0.25 + 0.35 * e + max(0.0, pump) * 0.4 * e
            # rotation about Y: positive lowers the right arm; mirror for the left
            L.key(sh, "rotation_euler", f, (0, side * lift, -side * 0.15))
            L.key(el, "rotation_euler", f, (0, -side * bend, 0))
