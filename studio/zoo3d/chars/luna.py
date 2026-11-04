"""Luna, Moonbeam Bedtime's host: a sleepy lavender owl in a blue nightcap with a glowing crescent-moon pompom.
Matches the channel's 2D Luna (art_moon.py LUNA svg): lavender body, pale belly with feather chevrons, darker wings
and ear tufts, cream eyes, orange beak, rosy cheeks, curling nightcap. Calm rig: floats, sways, slow heavy blinks."""
import math
import bpy
import mbkit as K


def build(L, prefix="Luna", loc=(0, 0, 0), scale=1.0, **opts):
    glow = opts.get("glow", 0.12)
    M = {
        "body": L.mat("LunaBody", opts.get("color", "#9682de"), 0.55, sheen=0.6, sss=0.06, bump=0.08, bump_scale=30, emission="#b3a4ff", emit=glow),
        "wing": L.mat("LunaWing", "#7e6bb8", 0.55, sheen=0.55, sss=0.04, bump=0.08, bump_scale=24, emission="#9a86e0", emit=glow * 0.8),
        "belly": L.mat("LunaBelly", "#e2d8ff", 0.6, sheen=0.7, sss=0.08, emission="#f3eeff", emit=glow * 0.4),
        "chev": L.mat("LunaChevron", "#b9acec", 0.6, sheen=0.5),
        "mask": L.mat("LunaMask", "#c4b8f0", 0.6, sheen=0.6, sss=0.05, emission="#d8ceff", emit=glow),
        "beak": L.mat("LunaBeak", "#ffb74d", 0.3, coat=0.7, sss=0.15),
        "beak2": L.mat("LunaBeakLow", "#e8962e", 0.35, coat=0.5, sss=0.1),
        "mouth": L.mat("LunaMouth", "#5a2340", 0.6),
        "cheek": L.mat("LunaCheek", "#ff9ab0", 0.6, sss=0.2, emission="#ff9ab0", emit=0.15),
        "cap": L.mat("LunaCap", "#5c6bc0", 0.75, sheen=0.8, bump=0.1, bump_scale=60),
        "brim": L.mat("LunaBrim", "#fff3c4", 0.8, sheen=0.9, bump=0.25, bump_scale=70),
        "moon": L.mat("LunaMoonGlow", "#fff3c4", 0.35, emission="#ffe9a3", emit=2.2),
        "feet": L.mat("LunaFeet", "#ffb74d", 0.4, coat=0.4),
    }
    root = L.empty(prefix, loc); root.scale = (scale,) * 3
    rig = L.empty(prefix + "Rig", (0, 0, 1.0), root)
    L.sphere(prefix + "Body", 0.74, (0, 0, 0), (1.0, 0.9, 1.06), M["body"], rig, 48)
    L.sphere(prefix + "Belly", 0.56, (0, -0.32, -0.2), (0.95, 0.62, 0.92), M["belly"], rig, 40)
    for k, (x, z) in enumerate(((-0.16, -0.08), (0.16, -0.08), (0.0, -0.28), (-0.2, -0.46), (0.2, -0.46))):
        L.torus(f"{prefix}Chev{k}", 0.075, 0.016, (x, -0.66 + abs(z + 0.2) * 0.25, z), (1, 1, 0.7), M["chev"], rig, (math.radians(80), 0, 0))
    # owl face mask (soft heart-shaped disc behind the eyes)
    for sx in (-1, 1):
        L.sphere(f"{prefix}Mask{sx}", 0.33, (0.25 * sx, -0.52, 0.28), (1, 0.42, 0.95), M["mask"], rig, 32)
    eyes = L.eye_pair(prefix, rig, spacing=0.26, z=0.29, y=-0.62, r=0.24, iris_hex="#3b2c73", lid_mat=M["wing"], toward=0.28)
    # big extra catchlight for that sleepy-sparkly Pixar look
    for sock, lid in eyes:
        L.sphere(sock.name + "Glint2", 0.024, (-0.05, -0.235, -0.07), (1, 0.5, 1), L.mat("Glint", (1, 1, 1)), sock, 10)
    for sx in (-1, 1):
        L.sphere(f"{prefix}Cheek{sx}", 0.1, (0.43 * sx, -0.6, 0.06), (1, 0.35, 0.65), M["cheek"], rig, 16)
    # beak: upper triangle-ish beak + lower beak on a jaw pivot, with a dark mouth inside
    beak = L.empty(prefix + "Beak", (0, -0.7, 0.1), rig)
    up = L.cone(prefix + "BeakUp", 0.1, 0.0, 0.2, (0, -0.03, -0.03), (1, 0.75, 1), M["beak"], beak, (math.pi, 0, 0), 24)
    L.sphere(prefix + "BeakTop", 0.1, (0, -0.03, 0.07), (1, 0.75, 0.45), M["beak"], beak, 20)
    jaw = L.empty(prefix + "Jaw", (0, 0.0, -0.02), beak)
    L.sphere(prefix + "MouthIn", 0.085, (0, -0.0, -0.07), (0.9, 0.6, 0.7), M["mouth"], jaw, 20)
    L.sphere(prefix + "BeakLow", 0.075, (0, -0.04, -0.09), (1, 0.8, 0.5), M["beak2"], jaw, 20)
    # ear tufts
    for sx in (-1, 1):
        L.cone(f"{prefix}Tuft{sx}", 0.12, 0.015, 0.34, (0.42 * sx, -0.05, 0.68), (1, 0.6, 1), M["wing"], rig, (0.1, 0.42 * sx, 0), 20)
    # wings on shoulder pivots
    wings = []
    for sx in (-1, 1):
        piv = L.empty(f"{prefix}Wing{sx}", (0.66 * sx, 0.0, 0.12), rig)
        L.sphere(f"{prefix}WingA{sx}", 0.36, (0.07 * sx, 0, -0.3), (0.32, 0.6, 1.0), M["wing"], piv, 32, (0, 0.22 * sx, 0))
        L.sphere(f"{prefix}WingB{sx}", 0.26, (0.1 * sx, 0.06, -0.52), (0.3, 0.5, 0.75), M["wing"], piv, 24, (0, 0.32 * sx, 0))
        wings.append((piv, sx))
    # feet dangle under the floating body
    feet = []
    for sx in (-1, 1):
        ft = L.empty(f"{prefix}Foot{sx}", (0.22 * sx, -0.25, -0.74), rig)
        for a in (-0.4, 0, 0.4):
            L.sphere(f"{prefix}Toe{sx}", 0.055, (math.sin(a) * 0.07, -math.cos(a) * 0.06, 0), (0.85, 1.8, 0.7), M["feet"], ft, 12, (0, 0, a))
        feet.append(ft)
    # nightcap: fluffy brim + one smooth tapering, drooping tube + glowing moon-ball pompom (secondary motion)
    cap = L.empty(prefix + "Cap", (0.0, 0.05, 0.6), rig); cap.rotation_euler = (-0.12, 0.18, 0)
    L.torus(prefix + "Brim", 0.47, 0.1, (0, 0, 0.02), (1, 0.96, 0.8), M["brim"], cap)
    path = ((0, 0, -0.02, 0.47), (0.0, 0, 0.18, 0.43), (0.06, 0, 0.42, 0.31), (0.22, 0, 0.6, 0.2), (0.44, 0, 0.62, 0.12), (0.6, 0, 0.5, 0.07), (0.66, 0, 0.36, 0.045))
    cu = bpy.data.curves.new(prefix + "CapCurve", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 1.0; cu.bevel_resolution = 8
    cu.use_fill_caps = True; cu.resolution_u = 18
    sp = cu.splines.new("NURBS"); sp.points.add(len(path) - 1); sp.order_u = 3; sp.use_endpoint_u = True
    for pt, (x, y, z, rr) in zip(sp.points, path):
        pt.co = (x, y, z, 1); pt.radius = rr
    co = bpy.data.objects.new(prefix + "CapTube", cu); L.scene().collection.objects.link(co); co.parent = cap
    cu.materials.append(M["cap"])
    pom = L.empty(prefix + "Pom", (0.67, 0, 0.3), cap)
    L.sphere(prefix + "PomBall", 0.12, (0, 0, 0), m=M["moon"], parent=pom, segs=24)
    # a tiny warm glow from the moon pompom lights her face softly
    gl = L.light(prefix + "PomLight", "POINT", 5, (0, -0.25, 0), color=(1.0, 0.88, 0.6)); gl.parent = pom
    gl.data.shadow_soft_size = 0.3
    real = opts.get("true_scale", scale); root.scale = (real,) * 3
    ch = Char(L, root, rig, eyes, jaw, wings, feet, cap, pom, None, opts)
    # close-up framing: the engine frames close shots by the declared cast scale; a smaller declared scale with a
    # true_scale opt gives a tighter, face-filling close-up, so keep the aim on the real face height.
    ch.face_z = 1.4 * real / max(0.05, scale); ch.height = 2.15 * real / max(0.05, scale)
    return ch


class Char:
    height = 2.15
    face_z = 1.4

    def __init__(self, L, root, rig, eyes, jaw, wings, feet, cap, c2, c3, opts):
        self.L, self.root, self.rig, self.eyes, self.jaw = L, root, rig, eyes, jaw
        self.wings, self.feet, self.cap, self.c2, self.c3 = wings, feet, cap, c2, c3
        self.sleepy = opts.get("sleepy", 0.35)        # 0 wide awake .. 1 nearly asleep
        self.seed = (hash(root.name) % 100) / 37.0

    def pose(self, f, t, s):
        L = self.L
        talk, e, bar = s.get("talk", 0), min(0.6, s.get("energy", 0.3)), s.get("bar", 0)
        # floating + slow sway (no bouncing): one sway per bar, a slow float bob over ~6 s
        sw = math.sin(bar * 2 * math.pi)
        floatz = 0.16 + math.sin(t * 1.05 + self.seed) * 0.06
        breathe = math.sin(t * 1.6 + self.seed) * 0.015
        L.key(self.rig, "location", f, (sw * 0.06 * (0.4 + e), 0, 1.0 + floatz))
        L.key(self.rig, "scale", f, (1 - breathe * 0.5, 1 - breathe * 0.5, 1 + breathe))
        L.key(self.rig, "rotation_euler", f, (talk * 0.04 - 0.03, sw * (0.05 + 0.1 * e), -s.get("look", 0) + math.sin(t * 0.5) * 0.05))
        # beak opens with the vocal
        L.key(self.jaw, "rotation_euler", f, (-talk * 0.5, 0, 0))
        # wings: soft drift, a slow paddle that keeps her afloat, or a gentle goodnight wave
        wave = s.get("wave", 0)
        for piv, sx in self.wings:
            drift = math.sin(t * 2.1 + (0.6 if sx > 0 else 0)) * 0.1 + sw * 0.08 * e
            if wave and sx > 0:
                L.key(piv, "rotation_euler", f, (0.2, -sx * 2.3, math.sin(t * 3.2) * 0.35))
            else:
                L.key(piv, "rotation_euler", f, (0, -sx * (0.12 + drift), 0))
        for ft, k in zip(self.feet, (0, 1.3)):
            L.key(ft, "rotation_euler", f, (math.sin(t * 1.4 + k) * 0.25, 0, 0))
        # nightcap lags behind the sway (secondary motion)
        lag = math.sin(bar * 2 * math.pi - 0.9)
        L.key(self.cap, "rotation_euler", f, (-0.12 + math.sin(t * 1.3) * 0.03, 0.18 - lag * 0.07, 0))
        L.key(self.c2, "location", f, (0.67, 0, 0.3 + math.sin(t * 2.0) * 0.015))
        # slow, heavy sleepy blinks: half-lidded base, a long soft blink every ~4.5 s
        heavy = K.pulse(t, 4.6, 0.75, self.seed)
        if s.get("blink"): heavy = max(heavy, 0.7)
        base = -55 + 45 * self.sleepy - talk * 12     # degrees; -110 = wide open, 78 = closed
        ang = K.lerp(base, 78, heavy)
        for sock, lid in self.eyes:
            L.key(lid, "rotation_euler", f, (math.radians(ang), 0, 0))
