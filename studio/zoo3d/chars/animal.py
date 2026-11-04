"""Savanna zoo friends for The Animated Zoo (3D). One module, five animals: opts kind in
{lion, elephant, giraffe, zebra, hippo}. Upright chibi style (big head, round body, stubby legs and arms)
so they sing face-to-camera and dance like Milo. Shared rig + per-kind signature parts. See API.md."""
import math
import bpy, bmesh

KINDS = {
    #            fur        belly/muzzle  dark/accent  inner-ear   iris
    "lion":     ("#f0ad3c", "#fde3a7", "#c2621b", "#ff9fb4", "#9a5a14"),
    "elephant": ("#98a9cc", "#c9d5ee", "#7486ad", "#ffb3c7", "#3d2a1c"),
    "giraffe":  ("#f8c64e", "#fff0c4", "#a8642a", "#ffb3c0", "#4a2c14"),
    "zebra":    ("#f7f4ee", "#d9d4cc", "#25232b", "#ffb0c0", "#3a2414"),
    "hippo":    ("#a493d6", "#f2b8d4", "#7f6cb8", "#ff9ec0", "#3a2414"),
}


# ---------------------------------------------------------------- materials
def _fur(L, kind, slot, hexc, sheen=0.55, rough=0.62):
    return L.mat(f"{kind}_{slot}", hexc, rough, coat=0.05, sheen=sheen, bump=0.12, bump_scale=30)


def _pattern(L, kind, name, base_hex, mark_hex, mode, scale, cut):
    """Fur with a procedural pattern. mode: stripes_x / stripes_z (zebra bands), spots (giraffe patches)."""
    key = f"{kind}_{name}"
    m = bpy.data.materials.get(key)
    if m is not None:
        return m
    m = bpy.data.materials.new(key); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.62
    for k, v in (("Sheen Weight", 0.55), ("Coat Weight", 0.05)):
        if k in b.inputs: b.inputs[k].default_value = v
    tc = nt.nodes.new("ShaderNodeTexCoord")
    if mode.startswith("stripes"):
        # wobble the coordinates with noise so stripes look hand-drawn, not ruler straight
        noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 2.2
        mix = nt.nodes.new("ShaderNodeVectorMath"); mix.operation = "MULTIPLY_ADD"
        mix.inputs[1].default_value = (0.09, 0.09, 0.09)
        nt.links.new(noise.outputs["Color"], mix.inputs[0]); nt.links.new(tc.outputs["Object"], mix.inputs[2])
        nt.links.new(tc.outputs["Object"], noise.inputs["Vector"])
        tex = nt.nodes.new("ShaderNodeTexWave"); tex.wave_type = "BANDS"
        tex.bands_direction = "X" if mode == "stripes_x" else "Z"
        tex.inputs["Scale"].default_value = scale
        tex.inputs["Distortion"].default_value = 1.5
        tex.inputs["Detail"].default_value = 0.5
        nt.links.new(mix.outputs["Vector"], tex.inputs["Vector"]); fac = tex.outputs["Fac"]
    else:
        tex = nt.nodes.new("ShaderNodeTexVoronoi"); tex.inputs["Scale"].default_value = scale
        if "Randomness" in tex.inputs: tex.inputs["Randomness"].default_value = 0.85
        nt.links.new(tc.outputs["Object"], tex.inputs["Vector"]); fac = tex.outputs["Distance"]
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp; cr.interpolation = "CONSTANT"
    a, c = (mark_hex, base_hex) if mode == "spots" else (base_hex, mark_hex)
    cr.elements[0].position = 0.0; cr.elements[0].color = (*L.rgb(a), 1)
    cr.elements[1].position = cut; cr.elements[1].color = (*L.rgb(c), 1)
    nt.links.new(fac, ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    # soft fur bump
    vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 30
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.12; bp.inputs["Distance"].default_value = 0.02
    nt.links.new(tc.outputs["Object"], vor.inputs["Vector"]); nt.links.new(vor.outputs["Distance"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


# ---------------------------------------------------------------- build
def build(L, prefix="Animal", loc=(0, 0, 0), scale=1.0, kind="lion", **opts):
    kind = kind if kind in KINDS else "lion"
    fur_h, belly_h, dark_h, ear_h, iris_h = KINDS[kind]
    fur_h = opts.get("color", fur_h)
    P = prefix
    M = {
        "fur": _fur(L, kind, "fur", fur_h),
        "belly": _fur(L, kind, "belly", belly_h, 0.45, 0.66),
        "dark": _fur(L, kind, "dark", dark_h, 0.5, 0.68),
        "ear": L.mat(f"{kind}_ear", ear_h, 0.55, sss=0.15),
        "cheek": L.mat("AnimalCheek", "#ff86a8", 0.6),
        "mouth": L.mat("AnimalMouth", "#5a1724", 0.5, coat=0.4),
        "tongue": L.mat("AnimalTongue", "#ff6f8e", 0.4, coat=0.5, sss=0.1),
        "nose": L.mat(f"{kind}_nose", {"lion": "#7a3b2a", "elephant": "#5d6b8f", "giraffe": "#5b3a1e",
                                        "zebra": "#2a2830", "hippo": "#6e5aa8"}[kind], 0.3, coat=0.8),
        "hoof": L.mat(f"{kind}_hoof", {"lion": "#fde3a7", "elephant": "#f3ead8", "giraffe": "#5b3a1e",
                                        "zebra": "#26242b", "hippo": "#f3e3ee"}[kind], 0.35, coat=0.6),
        "brow": L.mat(f"{kind}_brow", {"lion": "#9a4a14", "elephant": "#55638a", "giraffe": "#8a5222",
                                        "zebra": "#25232b", "hippo": "#5e4c99"}[kind], 0.6),
        "tooth": L.mat("AnimalTooth", "#ffffff", 0.25, coat=0.8),
    }
    body_m = M["fur"]; head_m = M["fur"]; limb_m = M["fur"]
    if kind == "zebra":
        body_m = _pattern(L, kind, "stripesX", "#f7f4ee", "#25232b", "stripes_x", 1.45, 0.5)
        limb_m = _pattern(L, kind, "stripesZ", "#f7f4ee", "#25232b", "stripes_z", 1.8, 0.5)
        head_m = _pattern(L, kind, "stripesH", "#f7f4ee", "#25232b", "stripes_z", 1.55, 0.5)
    if kind == "giraffe":
        body_m = head_m = limb_m = _pattern(L, kind, "spots", "#f8c64e", "#b8692c", "spots", 3.2, 0.36)

    root = L.empty(P, loc); root.scale = (scale,) * 3
    hip = 0.95
    rig = L.empty(P + "Rig", (0, 0, hip), root)
    wide = 1.12 if kind in ("hippo", "elephant") else 1.0
    L.sphere(P + "Body", 0.58, (0, 0, 0), (1.0 * wide, 0.9 * wide, 1.05), body_m, rig, 40)
    if kind != "zebra":
        L.sphere(P + "Belly", 0.46, (0, -0.24, -0.08), (0.92 * wide, 0.62, 0.95), M["belly"], rig, 32)

    # ---- head (giraffe: on a long neck)
    neck = None
    if kind == "giraffe":
        neck = L.empty(P + "Neck", (0, 0.02, 0.38), rig)
        L.cylinder(P + "NeckTube", 0.2, 1.4, (0, 0, 0.68), (1, 0.9, 1), body_m, neck, verts=24)
        for k in range(8):
            L.sphere(P + "Mane", 0.075, (0, 0.17, 0.12 + k * 0.17), (0.7, 1, 1.3), M["dark"], neck, 12)
        head = L.empty(P + "Head", (0, -0.04, 1.55), neck)
        hr = 0.47
    else:
        head = L.empty(P + "Head", (0, 0, 1.05), rig)
        hr = {"lion": 0.56, "elephant": 0.63, "zebra": 0.52, "hippo": 0.6}[kind]
    hs = {"hippo": (1.12, 0.98, 0.94), "elephant": (1.04, 0.98, 1.0), "giraffe": (0.95, 1.0, 1.06)}.get(kind, (1, 0.97, 1))
    L.sphere(P + "Skull", hr, (0, 0, 0), hs, head_m, head, 48)

    # eyes, brows, cheeks
    ez = {"lion": 0.1, "elephant": 0.12, "giraffe": 0.1, "zebra": 0.12, "hippo": 0.16}[kind]
    er = {"lion": 0.2, "elephant": 0.2, "giraffe": 0.19, "zebra": 0.19, "hippo": 0.19}[kind]
    esp = hr * 0.42 * (1.08 if kind == "hippo" else 1.0)
    ey = -math.sqrt(max(0.01, (hr * hs[1]) ** 2 - ez ** 2 - esp ** 2)) + 0.07
    eyes = L.eye_pair(P, head, spacing=esp, z=ez, y=ey, r=er, iris_hex=iris_h, lid_mat=head_m if kind != "zebra" else M["fur"], toward=0.3)
    brows = []
    for sx in (-1, 1):
        b = L.sphere(f"{P}Brow{sx}", 0.1, (esp * sx * 1.05, ey - 0.02, ez + er + 0.06), (0.9, 0.3, 0.28), M["brow"], head, 16, (0, sx * 0.25, 0))
        brows.append((b, b.location.z, sx))
        L.sphere(f"{P}Cheek{sx}", 0.09, (hr * 0.62 * sx, ey + 0.08, ez - 0.25), (1, 0.35, 0.65), M["cheek"], head, 16)

    # ---- muzzle + mouth: a smile arc when closed; a dark mouth with a tongue opens below it with talk
    #      (mouth sits on the face surface: center, half-width)
    mouth_at = {"lion": ((0, -0.462, -0.27), 0.1), "elephant": ((0, -0.5, -0.37), 0.1),
                "giraffe": ((0, -0.735, -0.27), 0.1), "zebra": ((0, -0.73, -0.28), 0.11),
                "hippo": ((0, -0.885, -0.2), 0.27)}[kind]
    (mx, my, mz), mw = mouth_at
    jaw = L.empty(P + "Jaw", (0, -0.25, -0.26), head)
    if kind == "lion":
        for sx in (-1, 1):
            L.sphere(f"{P}Pad{sx}", 0.15, (0.12 * sx, -0.4, -0.15), (1, 0.8, 0.85), M["belly"], head, 24)
        L.sphere(P + "Snout", 0.16, (0, -0.37, -0.27), (1.1, 0.8, 0.7), M["belly"], head, 24)
        L.sphere(P + "Nose", 0.1, (0, -0.53, -0.05), (1.15, 0.65, 0.7), M["nose"], head, 20)
        my, mz = -0.49, -0.27
    elif kind in ("giraffe", "zebra"):
        mzc = (0, -0.42, -0.17) if kind == "giraffe" else (0, -0.44, -0.17)
        ms = (0.29, 0.34, 0.24) if kind == "giraffe" else (0.29, 0.34, 0.24)
        L.sphere(P + "Muzzle", 1.0, mzc, ms, M["belly"] if kind == "giraffe" else L.mat("zebra_muzzle", "#55505e", 0.55, sheen=0.4), head, 32)
        for sx in (-1, 1):
            L.sphere(f"{P}Nostril{sx}", 0.035, (0.1 * sx, mzc[1] - ms[1] + 0.06, mzc[2] + 0.08), (1, 0.6, 1.2), M["mouth"], head, 10)
    elif kind == "hippo":
        L.sphere(P + "Muzzle", 1.0, (0, -0.5, -0.1), (0.52, 0.42, 0.27), M["belly"], head, 40)
        for sx in (-1, 1):
            L.sphere(f"{P}Nostril{sx}", 0.06, (0.17 * sx, -0.78, 0.08), (1, 0.8, 0.6), M["dark"], head, 12)
        L.sphere(P + "Chin", 1.0, (0, -0.24, -0.02), (0.46, 0.36, 0.16), M["belly"], jaw, 40)
        for sx in (-1, 1):
            L.cone(f"{P}Tooth{sx}", 0.05, 0.02, 0.12, (0.24 * sx, -0.52, 0.12), (1, 1, 1), M["tooth"], jaw, verts=12)
    mouth_m = L.mat("AnimalMouthDark", "#3a0912", 0.8)
    smile = L.torus(P + "Smile", mw * 0.9, 0.02 if kind != "hippo" else 0.03, (mx, my - 0.005, mz + mw * 0.45), (1, 0.35 if kind == "hippo" else 0.6, 0.75),
                    mouth_m, head, (math.pi / 2, 0, 0))
    bm = bmesh.new(); bm.from_mesh(smile.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0.004], context="VERTS"); bm.to_mesh(smile.data); bm.free()
    cav = L.sphere(P + "Mouth", 1.0, (mx, my, mz), (mw, 0.05 if kind != "hippo" else 0.08, 0.01), mouth_m, head, 24)
    tongue = L.sphere(P + "Tongue", 1.0, (mx, my - 0.012, mz), (mw * 0.6, 0.04, 0.01), M["tongue"], head, 16)
    cav_s = (mw, mz, kind)

    # ---- ears and signature features
    flaps = []      # (pivot, base_rot, axis_index, amp, phase)
    if kind == "lion":
        for k in range(14):
            a = k / 14 * math.tau
            L.sphere(P + "Mane", 0.25 if k % 2 else 0.22, (math.cos(a) * 0.58, 0.14, math.sin(a) * 0.6 + 0.02), (1, 0.75, 1),
                     M["dark"] if k % 2 else L.mat("lion_mane2", "#d97a22", 0.66, sheen=0.6, bump=0.15, bump_scale=30), head, 20)
        for x, z, s in ((-0.13, 0.5, 0.15), (0.05, 0.56, 0.17), (0.2, 0.48, 0.13)):
            L.sphere(P + "Tuft", s, (x, -0.12, z), (1, 0.8, 1), M["dark"], head, 16)
        for sx in (-1, 1):
            e = L.empty(f"{P}Ear{sx}", (0.38 * sx, 0.0, 0.4), head)
            L.sphere(P + "EarO", 0.14, (0, 0, 0), (1, 0.55, 1), M["fur"], e, 20)
            L.sphere(P + "EarI", 0.09, (0, -0.06, -0.01), (1, 0.4, 1), M["ear"], e, 16)
            flaps.append((e, (0, 0, 0), 1, 0.15 * sx, 0))
    elif kind == "elephant":
        for sx in (-1, 1):
            e = L.empty(f"{P}Ear{sx}", (0.5 * sx, 0.08, 0.06), head); e.rotation_euler = (0, 0, -0.35 * sx)
            L.sphere(P + "EarO", 1.0, (0.36 * sx, 0, -0.04), (0.44, 0.08, 0.52), M["fur"], e, 32)
            L.sphere(P + "EarI", 1.0, (0.36 * sx, -0.05, -0.06), (0.34, 0.05, 0.41), M["ear"], e, 28)
            flaps.append((e, (0, 0, -0.35 * sx), 2, 0.35 * sx, 0))
    elif kind == "giraffe":
        for sx in (-1, 1):
            L.cylinder(f"{P}Ossi{sx}", 0.05, 0.28, (0.15 * sx, 0.05, hr + 0.1), m=M["fur"], parent=head, rot=(0, 0.15 * sx, 0), verts=12)
            L.sphere(f"{P}OssiTip{sx}", 0.075, (0.17 * sx, 0.05, hr + 0.25), m=M["dark"], parent=head, segs=16)
            e = L.empty(f"{P}Ear{sx}", (0.38 * sx, 0.06, 0.24), head); e.rotation_euler = (0, 0.5 * sx, 0)
            L.sphere(P + "EarO", 1.0, (0.12 * sx, 0, 0), (0.17, 0.06, 0.08), M["fur"], e, 20)
            L.sphere(P + "EarI", 1.0, (0.12 * sx, -0.03, 0), (0.12, 0.04, 0.05), M["ear"], e, 16)
            flaps.append((e, (0, 0.5 * sx, 0), 1, 0.25 * sx, 0))
    elif kind == "zebra":
        for k in range(7):
            a = -0.2 + k * 0.33
            z, y = math.cos(a) * (hr + 0.03), math.sin(a) * (hr + 0.03)
            L.sphere(P + "Mane", 0.1, (0, y, z), (0.55, 1.1, 1.2), M["dark"] if k % 2 == 0 else M["fur"], head, 14, (a, 0, 0))
        for sx in (-1, 1):
            e = L.empty(f"{P}Ear{sx}", (0.26 * sx, 0.04, 0.42), head); e.rotation_euler = (0, 0.35 * sx, 0)
            L.cone(P + "EarO", 0.1, 0.02, 0.32, (0, 0, 0.12), (1, 0.55, 1), M["fur"], e, verts=16)
            L.cone(P + "EarI", 0.06, 0.01, 0.22, (0, -0.04, 0.1), (1, 0.4, 1), M["ear"], e, verts=12)
            flaps.append((e, (0, 0.35 * sx, 0), 1, 0.2 * sx, 0))
    elif kind == "hippo":
        for sx in (-1, 1):
            e = L.empty(f"{P}Ear{sx}", (0.42 * sx, 0.12, 0.44), head)
            L.sphere(P + "EarO", 0.11, (0, 0, 0), (1, 0.6, 1.1), M["fur"], e, 16)
            L.sphere(P + "EarI", 0.07, (0, -0.05, 0), (1, 0.4, 1), M["ear"], e, 12)
            flaps.append((e, (0, 0, 0), 1, 0.3 * sx, 0))

    trunk = []
    if kind == "elephant":
        par = L.empty(P + "Trunk", (0, ey - 0.06, -0.1), head)
        base = (-0.35, 0.05, 0.12, -0.35, -0.75)
        r0 = 0.15
        for k, b in enumerate(base):
            j = L.empty(f"{P}TrunkJ{k}", (0, 0, 0) if k == 0 else (0, 0, -0.17), par); j.rotation_euler = (b, 0, 0)
            r = r0 * (1 - 0.13 * k)
            L.sphere(f"{P}TrunkS{k}", r, (0, 0, -0.09), (1, 1, 1.25), M["fur"], j, 24)
            trunk.append((j, b)); par = j
        L.torus(P + "TrunkTip", 0.07, 0.035, (0, 0, -0.19), (1, 1, 1), M["dark"], par)
        for sx in (-1, 1):
            L.cone(f"{P}Tusk{sx}", 0.04, 0.012, 0.16, (0.17 * sx, ey + 0.02, -0.3), (1, 1, 1), M["tooth"], head, (-1.9, 0, 0), verts=12)

    # ---- arms
    arms = []
    for sx in (-1, 1):
        piv = L.empty(f"{P}Arm{sx}", (0.5 * wide * sx, -0.02, 0.22), rig)
        L.sphere(f"{P}ArmS{sx}", 0.13, (0.04 * sx, 0, -0.2), (1, 1, 1.9), limb_m, piv, 24, (0, 0.2 * sx, 0))
        L.sphere(f"{P}Paw{sx}", 0.13, (0.1 * sx, -0.02, -0.44), (1, 1, 0.9), M["hoof"] if kind in ("zebra", "giraffe") else limb_m, piv, 20)
        arms.append((piv, sx))

    # ---- legs + feet
    legs = []
    for sx in (-1, 1):
        lg = L.empty(f"{P}Leg{sx}", (0.25 * wide * sx, -0.02, 0.46), root)
        L.cylinder(f"{P}Thigh{sx}", 0.15, 0.42, (0, 0, -0.17), m=limb_m, parent=lg, verts=24)
        if kind in ("zebra", "giraffe"):
            L.cylinder(f"{P}Hoof{sx}", 0.16, 0.12, (0, -0.02, -0.4), m=M["hoof"], parent=lg, verts=24)
        else:
            L.sphere(f"{P}Foot{sx}", 0.19, (0, -0.06, -0.38), (1, 1.25, 0.55), limb_m, lg, 24)
            if kind in ("elephant", "hippo"):
                for k in (-1, 0, 1):
                    L.sphere(f"{P}Nail{sx}{k}", 0.05, (0.09 * k, -0.27, -0.4), (1, 0.6, 0.8), M["hoof"], lg, 10)
        legs.append((lg, sx))

    # ---- tail
    tail = L.empty(P + "Tail", (0, 0.5 * wide, -0.25), rig)
    tl = {"lion": 0.5, "elephant": 0.3, "giraffe": 0.45, "zebra": 0.45, "hippo": 0.15}[kind]
    L.cylinder(P + "TailS", 0.035 if kind != "hippo" else 0.06, tl, (0, tl * 0.35, -tl * 0.35), m=M["fur"] if kind != "zebra" else M["dark"], parent=tail, rot=(-0.8, 0, 0), verts=10)
    if kind in ("lion", "giraffe", "zebra", "elephant"):
        L.sphere(P + "TailTuft", 0.09 if kind == "lion" else 0.07, (0, tl * 0.7, -tl * 0.7), (1, 1, 1.4), M["dark"], tail, 14)

    ch = Char(L, kind, root, rig, head, neck, eyes, brows, jaw, cav, cav_s, tongue, flaps, trunk, arms, legs, tail)
    return ch


class Char:
    height = 2.65
    face_z = 1.98

    def __init__(self, L, kind, root, rig, head, neck, eyes, brows, jaw, cav, cav_s, tongue, flaps, trunk, arms, legs, tail):
        self.L, self.kind, self.root, self.rig, self.head, self.neck = L, kind, root, rig, head, neck
        self.eyes, self.brows, self.jaw, self.cav, self.cav_s, self.tongue = eyes, brows, jaw, cav, cav_s, tongue
        self.flaps, self.trunk, self.arms, self.legs, self.tail = flaps, trunk, arms, legs, tail
        if kind == "giraffe":
            self.height, self.face_z = 3.8, 2.9
        elif kind == "lion":
            self.height = 2.7
        self.phase = {"lion": 0.0, "elephant": 0.6, "giraffe": 1.3, "zebra": 2.1, "hippo": 2.8}[kind]

    def pose(self, f, t, s):
        L = self.L
        talk, e, beat, bar = s.get("talk", 0), s.get("energy", 0.3), s.get("beat", 0), s.get("bar", 0)
        jump, wave = s.get("jump", 0), s.get("wave", 0)
        hop = abs(math.sin(math.pi * beat))
        bounce = hop * 0.16 * e + jump * hop * 0.45
        land = max(0.0, 1 - hop * 4) * e
        sq = 1 - land * 0.09
        breathe = math.sin(t * 2.2 + self.phase) * 0.02
        sway = math.sin(bar * 2 * math.pi + self.phase * 0.3)
        heavy = 0.7 if self.kind in ("elephant", "hippo") else 1.0
        L.key(self.rig, "location", f, (sway * 0.1 * e, 0, 0.95 + breathe + bounce * heavy))
        L.key(self.rig, "scale", f, (1 / math.sqrt(sq), 1 / math.sqrt(sq), sq * (1 + breathe * 0.6)))
        L.key(self.rig, "rotation_euler", f, (talk * 0.04, sway * 0.1 * e, s.get("look", 0)))  # +look turns toward the singer
        # head bob and tilt (sings with its whole head)
        nod = math.sin(beat * 2 * math.pi) * 0.07 * e
        tilt = math.sin(bar * 2 * math.pi + 1.0 + self.phase) * 0.13 * e
        if self.neck is not None:
            L.key(self.neck, "rotation_euler", f, (nod * 0.6, tilt * 0.8, 0))
            L.key(self.head, "rotation_euler", f, (-nod * 0.5 - talk * 0.08, -tilt * 0.5, 0))
        else:
            L.key(self.head, "rotation_euler", f, (nod - talk * 0.08, tilt, 0))
        # mouth: opens downward from the smile line; the hippo opens extra wide (its big jaw drops too)
        open_ = min(1.0, talk ** 0.8)
        mw, mz, kind = self.cav_s
        big = 1.9 if kind == "hippo" else 1.0
        h = 0.012 + open_ * 0.1 * big
        L.key(self.cav, "scale", f, (mw * (0.8 + 0.3 * open_), self.cav.scale.y, h))
        L.key(self.cav, "location", f, (0, self.cav.location.y, mz - h * 0.45))
        L.key(self.tongue, "scale", f, (mw * 0.55, self.tongue.scale.y, 0.004 + open_ * 0.045 * big))
        L.key(self.tongue, "location", f, (0, self.tongue.location.y, mz - h * 0.95 + 0.02 * open_))
        L.key(self.jaw, "rotation_euler", f, (open_ * 0.5 if kind == "hippo" else 0, 0, 0))
        for b, z0, sx in self.brows:
            L.key(b, "location", f, (b.location.x, b.location.y, z0 + open_ * 0.04 + wave * 0.03))
        # ears, trunk, tail
        for piv, base, ax, amp, ph in self.flaps:
            r = list(base); r[ax] += amp * (math.sin(beat * 2 * math.pi) * 0.6 * e + math.sin(t * 2.5) * 0.15)
            L.key(piv, "rotation_euler", f, tuple(r))
        for k, (j, b) in enumerate(self.trunk):
            curl = -talk * 0.22 * k - wave * 0.15 * k
            L.key(j, "rotation_euler", f, (b + curl + math.sin(t * 3.0 - k * 0.7) * 0.08 * (0.5 + e),
                                          0, math.sin(beat * 2 * math.pi - k * 0.5) * 0.12 * e))
        L.key(self.tail, "rotation_euler", f, (math.sin(t * 3) * 0.08, 0, math.sin(beat * 2 * math.pi) * 0.45 * e + math.sin(t * 4) * 0.1))
        # arms: swing on the beat, both up and waving when celebrating
        for piv, sx in self.arms:
            swing = math.sin(beat * 2 * math.pi + (0 if sx > 0 else math.pi))
            up = 0.25 + 0.3 * e * (0.5 + 0.5 * swing) + wave * (1.7 + 0.35 * math.sin(t * 13))
            L.key(piv, "rotation_euler", f, (swing * 0.35 * e * (1 - wave), -sx * up, 0))
        # legs: step on alternate beats
        idx = int(bar * 4) % 2
        for k, (lg, sx) in enumerate(self.legs):
            lift = math.sin(math.pi * beat) * 0.12 * e if (k == idx) else 0.0
            L.key(lg, "location", f, (lg.location.x, -0.02, 0.46 + bounce * heavy * 0.9 + lift))
        closed = s.get("blink", False)
        for sock, lid in self.eyes:
            L.key(lid, "rotation_euler", f, (math.radians(78 if closed else -110), 0, 0))
