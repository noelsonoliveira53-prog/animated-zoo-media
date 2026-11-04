"""Milo, The Animated Zoo's round blue bird. Reference character for the shared rig API (see API.md)."""
import math

def build(L, prefix="Milo", loc=(0, 0, 0), scale=1.0, **_):
    M = {
        "blue": L.mat("MiloBlue", "#0f5fd8", 0.62, coat=0.08, sheen=0.35, bump=0.18, bump_scale=22),
        "dark": L.mat("MiloDark", "#0a3fa0", 0.62, coat=0.05, sheen=0.3, bump=0.18, bump_scale=16),
        "belly": L.mat("MiloBelly", "#a9d2ff", 0.65, sheen=0.4, bump=0.15, bump_scale=18),
        "beak": L.mat("Beak", "#ffa21f", 0.28, coat=0.8, sss=0.1),
        "cheek": L.mat("Cheek", "#ff8fb0", 0.6),
    }
    root = L.empty(prefix, loc); root.scale = (scale,) * 3
    rig = L.empty(prefix + "Rig", (0, 0, 1.26), root)
    L.sphere(prefix + "Body", 1.0, (0, 0, 0), (1.02, 0.96, 0.98), M["blue"], rig, 64)
    L.sphere(prefix + "Belly", 0.8, (0, -0.42, -0.26), (0.95, 0.62, 0.9), M["belly"], rig, 48)
    eyes = L.eye_pair(prefix, rig, spacing=0.33, z=0.3, y=-0.74, r=0.3, iris_hex="#7a4a1c", lid_mat=M["blue"], toward=0.32)
    for sx in (-1, 1):
        L.sphere(f"{prefix}Cheek{sx}", 0.15, (0.6 * sx, -0.7, 0.0), (1, 0.3, 0.6), M["cheek"], rig, 16)
    beak = L.empty(prefix + "Beak", (0, -0.88, -0.1), rig)
    up = L.sphere(prefix + "BeakUp", 1.0, (0, -0.2, 0.02), (0.22, 0.36, 0.14), M["beak"], beak, 32)
    jaw = L.empty(prefix + "Jaw", (0, -0.02, 0), beak)
    L.sphere(prefix + "BeakLow", 1.0, (0, -0.16, -0.05), (0.2, 0.3, 0.12), M["beak"], jaw, 32)
    for x, lean, ln in ((-0.11, 0.35, 0.5), (0.02, 0.05, 0.62), (0.15, -0.3, 0.45)):
        L.cone(prefix + "Crest", 0.08, 0.01, ln, (x - lean * 0.3, 0.05, 0.9 + ln * 0.45), (1, 1, 1), M["blue"], rig, (0.3, -lean, 0))
    wings = []
    for sx in (-1, 1):
        piv = L.empty(f"{prefix}Wing{sx}", (0.9 * sx, -0.05, 0.12), rig)
        for k, (dz, s) in enumerate(((0, 1), (-0.12, 0.85), (-0.22, 0.7))):
            L.sphere(f"{prefix}Feather{sx}{k}", 0.5, ((0.1 + 0.04 * k) * sx, 0.04 * k, -0.32 + dz), (0.2, 0.5 * s, 0.78 * s), M["dark"] if k else M["blue"], piv, 32, (0, (0.28 + 0.08 * k) * sx, 0))
        wings.append((piv, sx))
    tail = L.empty(prefix + "Tail", (0, 0.9, -0.15), rig)
    for a in (-0.35, 0, 0.35):
        L.sphere(prefix + "TailF", 0.3, (math.sin(a) * 0.18, 0.18, 0), (0.42, 1, 0.18), M["dark"], tail, 24, (-0.5, 0, a))
    legs = []
    for sx in (-1, 1):
        lg = L.empty(f"{prefix}Leg{sx}", (0.3 * sx, -0.1, 0.42), root)
        L.cylinder(prefix + "Shin", 0.06, 0.4, (0, 0, -0.2), m=M["beak"], parent=lg, verts=16)
        for a in (-0.5, 0, 0.5):
            L.sphere(prefix + "Toe", 0.05, (math.sin(a) * 0.1, -0.08 - math.cos(a) * 0.06, -0.41), (0.8, 2.2, 0.5), M["beak"], lg, 12, (0, 0, a))
        legs.append(lg)
    return Char(L, root, rig, eyes, jaw, up, wings, tail, legs)


class Char:
    height = 2.6      # top of head above root (world units at scale 1)
    face_z = 1.5      # camera aim height for close-ups

    def __init__(self, L, root, rig, eyes, jaw, up, wings, tail, legs):
        self.L, self.root, self.rig, self.eyes, self.jaw, self.up = L, root, rig, eyes, jaw, up
        self.wings, self.tail, self.legs = wings, tail, legs

    def pose(self, f, t, s):
        L = self.L
        talk, e, beat, bar = s.get("talk", 0), s.get("energy", 0.3), s.get("beat", 0), s.get("bar", 0)
        bounce = abs(math.sin(math.pi * beat)) * 0.22 * e + s.get("jump", 0) * abs(math.sin(math.pi * beat)) * 0.5
        land = max(0.0, 1 - abs(math.sin(math.pi * beat)) * 4) * e
        sq = 1 - land * 0.1
        breathe = math.sin(t * 2.4) * 0.02
        L.key(self.rig, "location", f, (math.sin(bar * 2 * math.pi) * 0.12 * e, 0, 1.26 + breathe + bounce))
        L.key(self.rig, "scale", f, (1 / math.sqrt(sq), 1 / math.sqrt(sq), sq * (1 + breathe * 0.6)))
        L.key(self.rig, "rotation_euler", f, (talk * 0.05, math.sin(bar * 2 * math.pi) * 0.12 * e, s.get("look", 0)))
        for lg, k in zip(self.legs, (1, -1)):
            L.key(lg, "location", f, (lg.location.x, -0.1, 0.42 + bounce * 0.9))
        L.key(self.jaw, "rotation_euler", f, (talk * 0.55, 0, 0)); L.key(self.up, "rotation_euler", f, (-talk * 0.06, 0, 0))
        wave = s.get("wave", 0)
        for piv, sx in self.wings:
            flap = math.sin(t * 14) * 0.5 * wave + math.sin(beat * math.pi * 2) * 0.25 * e
            L.key(piv, "rotation_euler", f, (0, -sx * (0.38 + flap + wave * 0.9), 0))
        closed = s.get("blink", False)
        for sock, lid in self.eyes:
            L.key(lid, "rotation_euler", f, (math.radians(78 if closed else -110), 0, 0))
        L.key(self.tail, "rotation_euler", f, (math.sin(t * 3) * 0.08, 0, math.sin(beat * math.pi * 2) * 0.2 * e))
