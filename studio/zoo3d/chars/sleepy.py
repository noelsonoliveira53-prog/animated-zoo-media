"""Sleepy animal friends for Moonbeam Bedtime: bunny, teddy, lamb, owl (opts kind=...), in soft patterned pajamas.
Cuddly round bodies, half-lidded eyes, slow blinks, big sleepy yawns between lines, gentle sway (no bouncing)."""
import math
import mbkit as K

KINDS = {
    "bunny": dict(fur="#f6eee9", face="#fffaf6", inner="#ffc2d1", pj=("#f7a8c4", "#fff0f5", "stripes"), nose="#ff8fab", iris="#6b4630", height=2.55),
    "teddy": dict(fur="#c98d5a", face="#f1d2a8", inner="#e9b98a", pj=("#8fb8ff", "#ffffff", "dots"), nose="#4a2b1a", iris="#3b2414", height=2.15),
    "lamb":  dict(fur="#fff6ea", face="#fbe7d6", inner="#f7c6cf", pj=("#a9e4c4", "#effff5", "stripes"), nose="#e8a0a8", iris="#4a3328", height=2.1),
    "owl":   dict(fur="#e7dccb", face="#fff8ee", inner="#d9c8ae", pj=("#ffd98a", "#fff6dd", "dots"), nose="#ffb74d", iris="#b07a1e", height=2.1),
}


def build(L, prefix="Bunny", loc=(0, 0, 0), scale=1.0, **opts):
    kind = opts.get("kind", "bunny"); P = KINDS.get(kind, KINDS["bunny"])
    pj = opts.get("pj", P["pj"])
    M = {
        "fur": L.mat(f"SF_{kind}_fur", P["fur"], 0.75, sheen=1.0, sss=0.05, bump=0.12, bump_scale=55, emission=P["fur"], emit=0.04),
        "face": L.mat(f"SF_{kind}_face", P["face"], 0.7, sheen=0.9, sss=0.06, bump=0.06, bump_scale=55),
        "inner": L.mat(f"SF_{kind}_inner", P["inner"], 0.6, sheen=0.6, sss=0.2),
        "pj": K.pattern_mat(f"SF_{kind}_pj", pj[0], pj[1], pj[2], 7.0 if pj[2] == "stripes" else 9.0, 0.8, 1.0),
        "pjdark": L.mat(f"SF_{kind}_pjtrim", pj[1], 0.8, sheen=1.0),
        "nose": L.mat(f"SF_{kind}_nose", P["nose"], 0.3, coat=0.6),
        "mouth": L.mat("SF_mouth", "#5a2340", 0.6),
        "tongue": L.mat("SF_tongue", "#ff8aa0", 0.5, sss=0.2),
        "cheek": L.mat("SF_cheek", "#ff9ab0", 0.6, sss=0.2, emission="#ff9ab0", emit=0.12),
        "btn": L.mat("SF_button", "#fff3c4", 0.3, coat=0.6),
    }
    root = L.empty(prefix, loc); root.scale = (scale,) * 3
    rig = L.empty(prefix + "Rig", (0, 0, 0.42), root)        # hips pivot: sway + breathe from here
    # legs + slipper feet
    legs = []
    for sx in (-1, 1):
        lg = L.empty(f"{prefix}Leg{sx}", (0.2 * sx, 0, 0.36), root)
        L.sphere(f"{prefix}Thigh{sx}", 0.17, (0, 0, -0.14), (1, 1, 1.35), M["pj"], lg, 24)
        L.sphere(f"{prefix}Foot{sx}", 0.15, (0, -0.07, -0.3), (1, 1.35, 0.6), M["fur"] if kind != "owl" else M["nose"], lg, 24)
        legs.append(lg)
    # pajama body
    L.sphere(prefix + "Body", 0.48, (0, 0, 0.38), (1.0, 0.86, 1.1), M["pj"], rig, 40)
    L.torus(prefix + "Hem", 0.4, 0.06, (0, 0, -0.02), (1.08, 0.94, 1), M["pjdark"], rig)
    L.torus(prefix + "Collar", 0.24, 0.06, (0, -0.04, 0.86), (1, 0.9, 1), M["pjdark"], rig)
    for k in range(3):
        L.sphere(f"{prefix}Btn{k}", 0.035, (0, -0.42 + k * 0.01, 0.62 - k * 0.2), (1, 0.5, 1), M["btn"], rig, 12)
    # head
    head = L.empty(prefix + "Head", (0, 0, 1.16), rig)
    if kind == "owl":
        L.sphere(prefix + "Skull", 0.5, (0, 0, 0), (1.05, 0.95, 0.95), M["fur"], head, 40)
        for sx in (-1, 1):
            L.sphere(f"{prefix}Disc{sx}", 0.24, (0.17 * sx, -0.36, 0.03), (1, 0.45, 1), M["face"], head, 28)
            L.cone(f"{prefix}Tuft{sx}", 0.09, 0.01, 0.22, (0.32 * sx, -0.05, 0.48), (1, 0.6, 1), M["fur"], head, (0, 0.45 * sx, 0), 16)
        mz = L.empty(prefix + "Muzzle", (0, -0.47, -0.08), head)
        L.cone(prefix + "Beak", 0.07, 0.0, 0.14, (0, -0.02, 0.0), (1, 0.75, 1), M["nose"], mz, (math.pi, 0, 0), 16)
    else:
        L.sphere(prefix + "Skull", 0.5, (0, 0, 0), (1.06, 0.94, 0.94), M["fur"] if kind != "lamb" else M["face"], head, 40)
        mz = L.empty(prefix + "Muzzle", (0, -0.4, -0.13), head)
        L.sphere(prefix + "Snout", 0.2, (0, 0, 0), (1.15, 0.7, 0.8), M["face"], mz, 28)
        L.sphere(prefix + "Nose", 0.055, (0, -0.13, 0.07), (1.3, 0.8, 0.9), M["nose"], mz, 16)
    eyes = L.eye_pair(prefix, head, spacing=0.19, z=0.05, y=-0.39, r=0.135, iris_hex=P["iris"],
                      lid_mat=M["fur"] if kind != "lamb" else M["face"], toward=0.3)
    for sx in (-1, 1):
        L.sphere(f"{prefix}Cheek{sx}", 0.07, (0.31 * sx, -0.36, -0.11), (1, 0.4, 0.65), M["cheek"], head, 12)
    # mouth (a soft dark oval that opens for singing and big yawns)
    mouth = L.empty(prefix + "Mouth", (0, -0.42, -0.24 if kind != "owl" else -0.2), head)
    L.sphere(prefix + "MouthIn", 0.07, (0, 0, 0), (1, 0.5, 1), M["mouth"], mouth, 16)
    L.sphere(prefix + "Tongue", 0.045, (0, -0.01, -0.03), (1, 0.5, 0.6), M["tongue"], mouth, 12)
    mouth.scale = (1, 1, 0.15)
    # ears per kind
    ears = []
    if kind == "bunny":
        for sx in (-1, 1):
            e = L.empty(f"{prefix}Ear{sx}", (0.17 * sx, 0.02, 0.38), head); e.rotation_euler = (0, 0.18 * sx, 0)
            L.sphere(f"{prefix}EarO{sx}", 0.13, (0, 0, 0.36), (0.9, 0.5, 3.0), M["fur"], e, 24)
            L.sphere(f"{prefix}EarI{sx}", 0.09, (0, -0.045, 0.36), (0.8, 0.3, 2.6), M["inner"], e, 20)
            ears.append((e, sx, 0.18 * sx))
        L.sphere(prefix + "Tail", 0.13, (0, 0.42, 0.12), m=M["fur"], parent=rig, segs=16)
    elif kind == "teddy":
        for sx in (-1, 1):
            e = L.empty(f"{prefix}Ear{sx}", (0.36 * sx, 0.05, 0.34), head)
            L.sphere(f"{prefix}EarO{sx}", 0.15, (0, 0, 0), (1, 0.6, 1), M["fur"], e, 20)
            L.sphere(f"{prefix}EarI{sx}", 0.09, (0, -0.06, 0), (1, 0.4, 1), M["inner"], e, 16)
            ears.append((e, sx, 0.0))
        # striped nightcap with a pompom
        cap = L.empty(prefix + "Cap", (-0.05, 0.05, 0.36), head); cap.rotation_euler = (-0.1, -0.35, 0)
        cm = K.pattern_mat("SF_teddy_cap", "#5c6bc0", "#fff3c4", "stripes", 9.0, 0.8, 1.0)
        L.torus(prefix + "CapBrim", 0.33, 0.06, (0, 0, 0), (1, 1, 0.8), M["btn"], cap)
        L.cone(prefix + "CapCone", 0.33, 0.04, 0.6, (0, 0, 0.3), (1, 1, 1), cm, cap, (0, 0, 0), 28)
        L.sphere(prefix + "CapPom", 0.08, (0, 0, 0.62), m=M["btn"], parent=cap, segs=16)
    elif kind == "lamb":
        wool = L.mat("SF_lamb_wool", "#fffdf7", 0.85, sheen=1.0, bump=0.3, bump_scale=30)
        wl = [(0, -0.02, 0.5, 0.2)]
        for k in range(7):   # a big puffy wool cap ringing the top of the head
            a = math.pi * (-0.1 + 1.2 * k / 6)
            wl.append((math.cos(a) * 0.36, -0.12 + (1 - math.sin(a)) * 0.05 + 0.1 * math.sin(a), 0.33 + 0.08 * math.sin(a), 0.17))
        for k in range(5):
            a = math.tau * k / 5
            wl.append((math.cos(a) * 0.22, 0.05 + math.sin(a) * 0.18, 0.47, 0.16))
        for k, (x, y, z, r) in enumerate(wl):
            L.sphere(f"{prefix}Wool{k}", r, (x, y, z), m=wool, parent=head, segs=20)
        for k in range(6):   # woolly shoulders peeking out of the pajama collar
            a = math.pi * (0.15 + 0.7 * k / 5)
            L.sphere(f"{prefix}Fluff{k}", 0.1, (math.cos(a) * 0.3, math.sin(a) * 0.12 - 0.02, 0.9), m=wool, parent=rig, segs=16)
        for sx in (-1, 1):
            e = L.empty(f"{prefix}Ear{sx}", (0.42 * sx, 0.0, 0.1), head); e.rotation_euler = (0, 0, 0)
            L.sphere(f"{prefix}EarO{sx}", 0.12, (0.1 * sx, 0, 0), (1.6, 0.5, 0.7), M["face"], e, 20)
            L.sphere(f"{prefix}EarI{sx}", 0.08, (0.11 * sx, -0.04, 0), (1.5, 0.3, 0.55), M["inner"], e, 16)
            ears.append((e, sx, 0.0))
    # arms (sleeves + paws) on shoulder pivots; owl gets feathered wings
    arms = []
    for sx in (-1, 1):
        a = L.empty(f"{prefix}Arm{sx}", (0.42 * sx, 0, 0.72), rig)
        if kind == "owl":
            L.sphere(f"{prefix}Wing{sx}", 0.3, (0.05 * sx, 0, -0.26), (0.32, 0.6, 1.0), M["fur"], a, 28, (0, 0.2 * sx, 0))
        else:
            L.sphere(f"{prefix}Sleeve{sx}", 0.13, (0.03 * sx, 0, -0.2), (1, 1, 1.9), M["pj"], a, 24, (0, 0.15 * sx, 0))
            L.sphere(f"{prefix}Paw{sx}", 0.11, (0.08 * sx, -0.02, -0.46), (1, 0.95, 1), M["fur"] if kind != "lamb" else M["face"], a, 20)
        arms.append((a, sx))
    real = opts.get("true_scale", scale); root.scale = (real,) * 3
    ch = Char(L, root, rig, head, eyes, mouth, ears, arms, legs, P["height"] * real / max(0.05, scale), opts)
    ch.face_z = 1.62 * real / max(0.05, scale)    # see luna.py: true_scale gives tighter close-ups
    return ch


class Char:
    face_z = 1.62

    def __init__(self, L, root, rig, head, eyes, mouth, ears, arms, legs, height, opts):
        self.L, self.root, self.rig, self.head, self.eyes, self.mouth = L, root, rig, head, eyes, mouth
        self.ears, self.arms, self.legs, self.height = ears, arms, legs, height
        self.sleepy = opts.get("sleepy", 0.45)
        self.seed = (hash(root.name) % 97) / 13.0

    def pose(self, f, t, s):
        L = self.L
        talk, e, bar = s.get("talk", 0), min(0.6, s.get("energy", 0.3)), s.get("bar", 0)
        sw = math.sin(bar * 2 * math.pi + self.seed * 0.3)
        breathe = math.sin(t * 1.5 + self.seed) * 0.02
        # a big slow yawn every ~12 s when not singing
        yawn = 0.0 if s.get("singing") else K.pulse(t, 12.0, 2.6, self.seed)
        open_ = max(talk * 0.85, yawn)
        L.key(self.rig, "location", f, (0, 0, 0.42))
        L.key(self.rig, "rotation_euler", f, (0, sw * (0.04 + 0.1 * e), -s.get("look", 0)))
        L.key(self.rig, "scale", f, (1 - breathe * 0.4, 1 - breathe * 0.4, 1 + breathe))
        L.key(self.head, "rotation_euler", f, (-yawn * 0.3 + talk * 0.04, sw * 0.06 * (0.5 + e), math.sin(t * 0.6 + self.seed) * 0.08))
        L.key(self.mouth, "scale", f, (1 + open_ * 0.15, 1, 0.15 + open_ * 1.35))
        wave = s.get("wave", 0)
        for a, sx in self.arms:
            if wave and sx > 0:
                L.key(a, "rotation_euler", f, (0.1, -sx * 2.5, math.sin(t * 3.2 + self.seed) * 0.4))
            elif yawn > 0.05:
                L.key(a, "rotation_euler", f, (0, -sx * (0.25 + yawn * 2.3), 0))   # big stretch up
            else:
                L.key(a, "rotation_euler", f, (math.sin(t * 1.2 + sx) * 0.05, -sx * (0.12 + sw * sx * 0.08 * (0.4 + e)), 0))
        for e_, sx, base in self.ears:
            L.key(e_, "rotation_euler", f, (math.sin(t * 1.1 + sx) * 0.06 - 0.05, base + sw * 0.05, 0))
        heavy = max(K.pulse(t, 5.2, 0.8, self.seed * 1.7), yawn * 1.0)
        if s.get("blink"): heavy = max(heavy, 0.7)
        base = -55 + 50 * self.sleepy - talk * 10
        ang = K.lerp(base, 78, min(1.0, heavy))
        for sock, lid in self.eyes:
            L.key(lid, "rotation_euler", f, (math.radians(ang), 0, 0))
