"""Tiny Truck Town 3D cast: friendly cartoon trucks with windshield eyes and a smiling bumper mouth (BOLT's look).

build(L, prefix, loc, scale, variant="fire"|"police"|"dump"|"garbage"|"school_bus", color="#hex", name=None)
The truck faces -Y. Wheels roll with the rocking dance, the body squashes on its suspension, the mouth opens with
`talk`, and each variant has a "wave" part: fire = ladder lifts, police = light bar flashes faster, dump = bed tips,
garbage = side arm lifts a recycling bin, school_bus = STOP arm swings out.
"""
import math
import bmesh

VARIANTS = {
    #            paint      trim       lamp colors                 accent
    "fire":       ("#e3221c", "#fff3c4", ("#ff2a2a", "#ff2a2a"), "#ffd54a"),
    "police":     ("#2a62e8", "#ffffff", ("#ff2a3a", "#2a6bff"), "#ffd54a"),
    "dump":       ("#ffc21a", "#ff8a1a", ("#ffae00", "#ffae00"), "#3a3f4a"),
    "garbage":    ("#3dae4a", "#c8f07a", ("#ffae00", "#ffae00"), "#2a8bff"),
    "school_bus": ("#ffc21a", "#2b2f3a", ("#ff8a00", "#ff2a2a"), "#e8302a"),
}

RZ = 0.62   # body rig height above the ground (suspension pivot)


def _box(L, name, dims, loc, m, parent, bevel=0.08, segs=3, soft=True, rot=(0, 0, 0)):
    """Rounded box with true dimensions (scale stays 1, so bevels stay round). soft=True adds a subsurf for a toy look."""
    o = L.cube(name, 1, loc, (1, 1, 1), m, parent, rot)
    for v in o.data.vertices:
        v.co.x *= dims[0]; v.co.y *= dims[1]; v.co.z *= dims[2]
    if bevel:
        b = o.modifiers.new("Bevel", "BEVEL"); b.width = bevel; b.segments = segs; b.use_clamp_overlap = True
        if soft:
            L.subsurf(o, 1)
        L.smooth(o)
    return o


def _half(o, keep="lower"):
    bm = bmesh.new(); bm.from_mesh(o.data)
    kill = [v for v in bm.verts if (v.co.z > 1e-4 if keep == "lower" else v.co.z < -1e-4)]
    bmesh.ops.delete(bm, geom=kill, context="VERTS")
    bm.to_mesh(o.data); bm.free()
    return o


def build(L, prefix="Truck", loc=(0, 0, 0), scale=1.0, variant="fire", color=None, name=None, **_):
    variant = variant if variant in VARIANTS else "fire"
    paint_hex, trim_hex, lamp_hex, accent_hex = VARIANTS[variant]
    paint_hex = color or paint_hex
    P = prefix
    M = {
        "paint": L.mat(f"TT_Paint{paint_hex}", paint_hex, 0.32, coat=1.0, sheen=0.05),
        "trim": L.mat(f"TT_Trim{trim_hex}", trim_hex, 0.35, coat=0.8),
        "accent": L.mat(f"TT_Acc{accent_hex}", accent_hex, 0.3, coat=0.8),
        "glass": L.mat("TT_Glass", "#86d0f7", 0.08, coat=1.0),
        "rubber": L.mat("TT_Rubber", "#2a2e38", 0.62, sheen=0.25),
        "chrome": L.mat("TT_Chrome", "#e3e9ee", 0.18, metal=0.75, coat=0.5),
        "dark": L.mat("TT_Dark", "#3a3f4a", 0.5, coat=0.2),
        "mouth": L.mat("TT_Mouth", "#5a1018", 0.45, coat=0.3),
        "tongue": L.mat("TT_Tongue", "#ff6f86", 0.4, sss=0.2, coat=0.3),
        "cheek": L.mat("TT_Cheek", "#ff8fae", 0.55, sss=0.1),
        "brow": L.mat("TT_Brow", "#3b2318", 0.5),
        "head": L.mat("TT_Headlight", "#fff6c8", 0.1, coat=1.0, emission="#fff1b0", emit=1.2),
        "tail": L.mat("TT_Taillight", "#ff3b3b", 0.2, coat=1.0, emission="#ff2a2a", emit=1.0),
    }
    lamps = [L.mat(f"TT_Lamp{P}{k}", h, 0.15, coat=1.0, emission=h, emit=2.0) for k, h in enumerate(lamp_hex)]

    root = L.empty(P, loc); root.scale = (scale,) * 3
    hop = L.empty(P + "Hop", (0, 0, 0), root)
    rig = L.empty(P + "Rig", (0, 0, RZ), hop)
    z = lambda wz: wz - RZ   # world height -> rig local

    # ---------------------------------------------------------------- wheels
    wheels = []
    for wy in (-0.85, 1.35):
        for sx in (-1, 1):
            piv = L.empty(f"{P}Wheel{sx}{wy}", (0.9 * sx, wy, 0.44), hop)
            L.torus(f"{P}Tire{sx}{wy}", 0.29, 0.15, (0, 0, 0), (1, 1, 1), M["rubber"], piv, (0, math.pi / 2, 0))
            L.cylinder(f"{P}Hub{sx}{wy}", 0.2, 0.2, (0.02 * sx, 0, 0), m=M["chrome"], parent=piv, rot=(0, math.pi / 2, 0), verts=32)
            L.cylinder(f"{P}Cap{sx}{wy}", 0.11, 0.06, (0.12 * sx, 0, 0), m=M["paint"], parent=piv, rot=(0, math.pi / 2, 0), verts=24)
            for k in range(3):   # bolts make the roll readable
                a = k * math.tau / 3
                L.sphere(f"{P}Bolt{sx}{wy}{k}", 0.035, (0.13 * sx, math.cos(a) * 0.16, math.sin(a) * 0.16), m=M["dark"], parent=piv, segs=10)
            wheels.append(piv)

    # ---------------------------------------------------------------- chassis, cab
    _box(L, P + "Chassis", (1.5, 3.2, 0.3), (0, 0.25, z(0.55)), M["dark"], rig, 0.08, 2, soft=False)
    _box(L, P + "Lower", (1.78, 3.3, 0.55), (0, 0.25, z(0.95)), M["paint"], rig, 0.16, 3)
    _box(L, P + "Cab", (1.74, 1.45, 1.3), (0, -0.68, z(1.62)), M["paint"], rig, 0.3, 3)
    _box(L, P + "Shield", (1.46, 0.12, 0.76), (0, -1.39, z(1.79)), M["glass"], rig, 0.05, 2)
    for sx in (-1, 1):
        _box(L, f"{P}SideWin{sx}", (0.1, 0.78, 0.56), (0.84 * sx, -0.66, z(1.84)), M["glass"], rig, 0.03, 2, soft=False)
        # mirrors = little ears
        mir = L.empty(f"{P}Mirror{sx}", (0.9 * sx, -1.2, z(1.72)), rig)
        L.cylinder(f"{P}MirArm{sx}", 0.03, 0.22, (0.1 * sx, 0, 0), m=M["dark"], parent=mir, rot=(0, math.pi / 2, 0), verts=10)
        _box(L, f"{P}MirHead{sx}", (0.1, 0.12, 0.28), (0.22 * sx, 0, 0.06), M["paint"], mir, 0.04, 2, soft=False)
    # bumper + headlights + tail lights
    _box(L, P + "Bumper", (1.92, 0.3, 0.24), (0, -1.44, z(0.7)), M["chrome"], rig, 0.1, 3)
    for sx in (-1, 1):
        L.cylinder(f"{P}Head{sx}", 0.13, 0.08, (0.66 * sx, -1.42, z(1.0)), m=M["head"], parent=rig, rot=(math.pi / 2, 0, 0), verts=24)
        L.torus(f"{P}HeadRim{sx}", 0.13, 0.03, (0.66 * sx, -1.45, z(1.0)), m=M["chrome"], parent=rig, rot=(math.pi / 2, 0, 0))
        _box(L, f"{P}Tail{sx}", (0.22, 0.06, 0.14), (0.72 * sx, 1.91, z(1.05)), M["tail"], rig, 0.03, 2, soft=False)

    # ---------------------------------------------------------------- face
    eyes = L.eye_pair(P, rig, spacing=0.35, z=z(1.79), y=-1.43, r=0.3, iris_hex="#4a2a12", lid_mat=M["paint"], toward=0.1)
    brows = []
    for sx in (-1, 1):
        b = L.sphere(f"{P}Brow{sx}", 1.0, (0.36 * sx, -1.48, z(2.13)), (0.19, 0.05, 0.05), M["brow"], rig, 16, (0, -0.12 * sx, 0))
        brows.append((b, sx))
        L.sphere(f"{P}Cheek{sx}", 0.13, (0.6 * sx, -1.42, z(1.24)), (1, 0.25, 0.7), M["cheek"], rig, 16)
    mouth = L.empty(P + "Mouth", (0, -1.42, z(1.22)), rig)
    _half(L.sphere(P + "MouthIn", 0.3, (0, 0, 0), (1, 0.25, 1), M["mouth"], mouth, 32))
    L.sphere(P + "Tongue", 0.17, (0, -0.03, -0.7 * 0.3), (1, 0.3, 0.5), M["tongue"], mouth, 16)
    # smile corners (little dimples)
    for sx in (-1, 1):
        L.sphere(f"{P}Dimple{sx}", 0.035, (0.31 * sx, -1.43, z(1.235)), (1, 0.4, 1), M["mouth"], rig, 10)

    # ---------------------------------------------------------------- roof lamps
    lamp_objs = []
    if variant in ("fire", "police"):
        _box(L, P + "LampBar", (1.3, 0.32, 0.1), (0, -1.0, z(2.3)), M["dark"], rig, 0.04, 2, soft=False)
        xs = (-0.42, 0.42) if variant == "fire" else (-0.36, 0.36)
        for k, x in enumerate(xs):
            if variant == "police":
                lamp_objs.append(_box(L, f"{P}Lamp{k}", (0.56, 0.28, 0.16), (x, -1.0, z(2.4)), lamps[k], rig, 0.07, 2))
            else:
                lamp_objs.append(L.sphere(f"{P}Lamp{k}", 0.15, (x, -1.0, z(2.36)), (1, 1, 0.85), lamps[k], rig, 24))
    else:
        for k, x in enumerate((-0.55, 0.55)):
            L.cylinder(f"{P}LampBase{k}", 0.1, 0.06, (x, -0.95, z(2.3)), m=M["dark"], parent=rig, verts=16)
            lamp_objs.append(L.sphere(f"{P}Lamp{k}", 0.11, (x, -0.95, z(2.36)), (1, 1, 1.1), lamps[k % len(lamps)], rig, 20))

    # ---------------------------------------------------------------- variant body + wave part
    wave_part, wave_axis, wave_amt = None, "x", 0.0
    if variant == "fire":
        _box(L, P + "Body", (1.78, 1.86, 0.82), (0, 0.98, z(1.62)), M["paint"], rig, 0.18, 3)
        for sx in (-1, 1):
            _box(L, f"{P}Stripe{sx}", (0.04, 2.9, 0.1), (0.9 * sx, 0.45, z(1.08)), M["trim"], rig, 0.02, 1, soft=False)
            for k, yy in enumerate((0.55, 1.42)):
                _box(L, f"{P}Door{sx}{k}", (0.05, 0.72, 0.55), (0.89 * sx, yy, z(1.64)), M["chrome"], rig, 0.05, 2, soft=False)
            em = L.cylinder(f"{P}Badge{sx}", 0.17, 0.04, (0.88 * sx, -0.62, z(1.28)), m=M["accent"], parent=rig, rot=(0, math.pi / 2, 0), verts=24)
            L.text3d(f"{P}BadgeTxt{sx}", "1", 0.22, (0.91 * sx, -0.62, z(1.27)), M["paint"], rig, 0.02, 0.005, (math.pi / 2, 0, math.pi / 2 * sx))
        L.cylinder(P + "Turn", 0.28, 0.1, (0, 1.55, z(2.08)), m=M["chrome"], parent=rig, verts=24)
        lad = L.empty(P + "Ladder", (0, 1.55, z(2.16)), rig)
        ln = 2.8
        for sx in (-1, 1):
            _box(L, f"{P}Rail{sx}", (0.08, ln, 0.1), (0.3 * sx, -ln / 2 + 0.15, 0.05), M["chrome"], lad, 0.03, 2, soft=False)
        for k in range(8):
            L.cylinder(f"{P}Rung{k}", 0.032, 0.6, (0, 0.05 - k * 0.36, 0.05), m=M["chrome"], parent=lad, rot=(0, math.pi / 2, 0), verts=10)
        lad.rotation_euler = (-0.07, 0, 0)
        wave_part, wave_axis, wave_amt = lad, "x", -0.6
        # hose reel on the back
        L.torus(P + "Reel", 0.22, 0.07, (0, 1.95, z(1.62)), m=M["accent"], parent=rig, rot=(math.pi / 2, 0, 0))
    elif variant == "police":
        _box(L, P + "Body", (1.78, 1.86, 0.62), (0, 0.98, z(1.5)), M["paint"], rig, 0.22, 3)
        for sx in (-1, 1):
            _box(L, f"{P}WhiteDoor{sx}", (0.05, 1.3, 0.62), (0.885 * sx, -0.25, z(1.28)), M["trim"], rig, 0.08, 2, soft=False)
            L.text3d(f"{P}Word{sx}", "POLICE", 0.26, (0.92 * sx, 1.0, z(1.45)), M["trim"], rig, 0.02, 0.005, (math.pi / 2, 0, math.pi / 2 * sx))
            star = L.cylinder(f"{P}Star{sx}", 0.16, 0.04, (0.92 * sx, -0.3, z(1.3)), m=M["accent"], parent=rig, rot=(0, math.pi / 2, 0), verts=5)
        wave_part, wave_axis, wave_amt = None, "x", 0.0
    elif variant == "dump":
        hinge = L.empty(P + "Bed", (0, 1.85, z(1.3)), rig)
        bm = L.mat(f"TT_Bed{trim_hex}", trim_hex, 0.35, coat=0.7)
        _box(L, P + "BedFloor", (1.78, 1.8, 0.1), (0, -0.9, 0.0), bm, hinge, 0.04, 2, soft=False)
        for sx in (-1, 1):
            _box(L, f"{P}BedSide{sx}", (0.1, 1.8, 0.62), (0.84 * sx, -0.9, 0.3), bm, hinge, 0.04, 2, soft=False)
        _box(L, P + "BedFront", (1.78, 0.12, 0.85), (0, -1.78, 0.42), bm, hinge, 0.04, 2, soft=False)
        _box(L, P + "BedBack", (1.78, 0.1, 0.55), (0, -0.02, 0.27), bm, hinge, 0.04, 2, soft=False)
        dirt = L.mat("TT_Dirt", "#8a5a34", 0.95, bump=0.4, bump_scale=10)
        L.sphere(P + "Dirt", 1.0, (0, -0.9, 0.5), (0.72, 0.8, 0.32), dirt, hinge, 24)
        for k, (x, y) in enumerate(((-0.35, -0.6), (0.3, -1.1), (0.05, -0.85))):
            L.sphere(f"{P}Rock{k}", 0.13, (x, y, 0.75), (1, 0.9, 0.8), M["dark"], hinge, 10)
        wave_part, wave_axis, wave_amt = hinge, "x", -0.5
        for sx in (-1, 1):
            _box(L, f"{P}Stripe{sx}", (0.04, 1.4, 0.1), (0.9 * sx, -0.55, z(1.08)), M["dark"], rig, 0.02, 1, soft=False)
    elif variant == "garbage":
        _box(L, P + "Body", (1.8, 1.9, 1.2), (0, 0.98, z(1.8)), M["paint"], rig, 0.3, 3)
        _box(L, P + "Band", (1.84, 1.6, 0.22), (0, 0.98, z(1.62)), M["trim"], rig, 0.06, 2, soft=False)
        _box(L, P + "Hopper", (1.6, 0.4, 0.9), (0, 1.98, z(1.5)), M["dark"], rig, 0.12, 2)
        arm = L.empty(P + "Arm", (-0.92, 0.9, z(1.15)), rig)
        _box(L, P + "ArmBar", (0.1, 0.12, 0.7), (-0.06, 0, 0.3), M["chrome"], arm, 0.03, 2, soft=False)
        bin_m = L.mat("TT_Bin", accent_hex, 0.35, coat=0.6)
        _box(L, P + "Bin", (0.4, 0.42, 0.52), (-0.32, 0, 0.55), bin_m, arm, 0.06, 2)
        _box(L, P + "BinLid", (0.44, 0.46, 0.06), (-0.32, 0, 0.83), bin_m, arm, 0.03, 1, soft=False)
        wave_part, wave_axis, wave_amt = arm, "y", -0.8
    else:   # school bus
        _box(L, P + "Body", (1.78, 2.0, 1.28), (0, 0.9, z(1.62)), M["paint"], rig, 0.28, 3)
        for sx in (-1, 1):
            for k, yy in enumerate((0.35, 0.95, 1.55)):
                _box(L, f"{P}Win{sx}{k}", (0.08, 0.48, 0.42), (0.88 * sx, yy, z(1.9)), M["glass"], rig, 0.04, 2, soft=False)
            for k, wz in enumerate((1.35, 1.12)):
                _box(L, f"{P}Line{sx}{k}", (0.04, 3.0, 0.05), (0.9 * sx, 0.4, z(wz)), M["trim"], rig, 0.01, 1, soft=False)
        stop = L.empty(P + "StopArm", (-0.92, -0.25, z(1.55)), rig)
        L.cylinder(P + "Stop", 0.24, 0.04, (-0.3, 0, 0), m=M["accent"], parent=stop, rot=(math.pi / 2, math.pi / 8, 0), verts=8)
        L.text3d(P + "StopTxt", "STOP", 0.12, (-0.3, -0.04, 0), L.mat("TT_White", "#ffffff", 0.3), stop, 0.01, 0.004)
        stop.rotation_euler = (0, 0, -1.45)
        wave_part, wave_axis, wave_amt = stop, "z", 1.45
    return Char(L, root, hop, rig, wheels, eyes, brows, mouth, lamp_objs, lamps, wave_part, wave_axis, wave_amt, variant)


class Char:
    height = 2.5
    face_z = 1.72

    def __init__(self, L, root, hop, rig, wheels, eyes, brows, mouth, lamp_objs, lamps, wave_part, wave_axis, wave_amt, variant):
        self.L, self.root, self.hop, self.rig, self.wheels, self.eyes, self.brows, self.mouth = L, root, hop, rig, wheels, eyes, brows, mouth
        self.lamp_objs, self.lamps, self.variant = lamp_objs, lamps, variant
        self.wave_part, self.wave_axis, self.wave_amt = wave_part, wave_axis, wave_amt
        self.wave_base = tuple(wave_part.rotation_euler) if wave_part is not None else None
        self.mirrors = [o for o in rig.children if "Mirror" in o.name]
        self._wv, self._lf = 0.0, None

    def pose(self, f, t, s):
        L = self.L
        talk, e, beat, bar = s.get("talk", 0), s.get("energy", 0.3), s.get("beat", 0), s.get("bar", 0)
        jump = s.get("jump", 0)
        hb = abs(math.sin(math.pi * beat))
        # smoothed wave (engine sends a 0/1 gate); snap when frames are not consecutive (test stills)
        tgt = float(s.get("wave", 0))
        if self._lf is None or abs(f - self._lf) > 2: self._wv = tgt
        else: self._wv += (tgt - self._wv) * 0.22
        self._lf = f
        wv = self._wv
        # hop + rock forward/back (wheels roll with it)
        dy = math.sin(bar * 2 * math.pi) * 0.16 * e
        hopz = jump * hb * 0.42
        L.key(self.hop, "location", f, (0, dy, hopz))
        L.key(self.hop, "rotation_euler", f, (0, 0, -s.get("look", 0) * 0.7 + math.sin(bar * 2 * math.pi + 1.2) * 0.07 * e))
        for w in self.wheels:
            L.key(w, "rotation_euler", f, (-dy / 0.44, 0, 0))
        # body: suspension bob, squash on the downbeat, roll with the bar
        land = max(0.0, 1 - hb * 3.5) * e
        sq = 1 - land * 0.07 + hb * 0.03 * e
        breathe = math.sin(t * 2.4) * 0.012
        L.key(self.rig, "location", f, (0, 0, RZ + hb * 0.07 * e + breathe))
        L.key(self.rig, "scale", f, (1 / math.sqrt(sq), 1 / math.sqrt(sq), sq))
        L.key(self.rig, "rotation_euler", f, (-talk * 0.03 + math.sin(beat * 2 * math.pi) * 0.02 * e, math.sin(bar * 2 * math.pi) * 0.06 * e, 0))
        # mouth + brows
        L.key(self.mouth, "scale", f, (1 + talk * 0.08, 1, 0.32 + talk * 0.78))
        for b, sx in self.brows:
            b.location.z = (2.13 - RZ) + talk * 0.04 + e * 0.03 + wv * 0.05
            b.rotation_euler.y = -0.12 * sx - wv * 0.1 * sx
        for m in self.mirrors:
            sx = 1 if m.location.x > 0 else -1
            m.rotation_euler = (0, sx * math.sin(beat * 2 * math.pi) * 0.25 * e, 0)
        closed = s.get("blink", False)
        for sock, lid in self.eyes:
            L.key(lid, "rotation_euler", f, (math.radians(70 if closed else -110), 0, 0))
        # lamps: alternate flash on the beat, faster when waving
        rate = 2 if (wv > 0.5 or e > 0.85) else 1
        ph = bar * 4 * rate          # beats within the bar (keeps the flash on the beat at any bpm)
        for k, m in enumerate(self.lamps):
            on = 0.5 + 0.5 * math.cos(math.pi * (ph + k))
            m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.6 + on * (2.5 + 4 * e)
        for k, o in enumerate(self.lamp_objs):
            on = 0.5 + 0.5 * math.cos(math.pi * (ph + k))
            o.scale = (1 + on * 0.12,) * 3
        # variant wave part
        if self.wave_part is not None:
            bx, by, bz = self.wave_base
            amt = self.wave_amt * wv + (self.wave_amt * 0.12 * hb * e if self.variant != "school_bus" else 0)
            r = {"x": (bx + amt, by, bz), "y": (bx, by + amt, bz), "z": (bx, by, bz + amt)}[self.wave_axis]
            L.key(self.wave_part, "rotation_euler", f, r)
