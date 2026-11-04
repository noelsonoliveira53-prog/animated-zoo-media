"""The Animated Zoo: film-quality 3D Milo, built and rendered in Blender (4.2+ / 5.x).

Windows (RTX GPU):  blender.exe -b -P milo_blender.py -- --out C:\\path\\out --mouth mouth.json --audio voice.wav
Quick look:         ... -- --test   (renders 3 stills at low quality)
Options: --engine CYCLES|EEVEE  --samples 96  --res 1920x1080  --fps 24  --seconds 10.99  --start N --end N
Re-running continues where it stopped (existing frames are skipped), then encodes final.mp4 with the audio.
"""
import bpy, math, json, os, sys, random
def mem(tag): pass

# ---------------- args ----------------
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(name, default=None):
    if "--" + name in argv:
        i = argv.index("--" + name)
        return argv[i + 1] if i + 1 < len(argv) and not argv[i + 1].startswith("--") else True
    return default
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(opt("out", os.path.join(HERE, "out")))
TEST = bool(opt("test", False))
ENGINE = str(opt("engine", "CYCLES")).upper()
SAMPLES = int(opt("samples", 24 if TEST else 96))
W, H = map(int, str(opt("res", "960x540" if TEST else "1920x1080")).split("x"))
FPS = int(opt("fps", 24))
SECONDS = float(opt("seconds", 10.99))
MOUTH = opt("mouth", os.path.join(HERE, "mouth.json"))
AUDIO = opt("audio", os.path.join(HERE, "voice.wav"))
mouth = json.load(open(MOUTH)) if MOUTH and os.path.exists(MOUTH) else []
random.seed(7)

# ---------------- reset ----------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = int(opt("end", round(SECONDS * FPS)))
if opt("start"): scene.frame_start = int(opt("start"))

# ---------------- materials ----------------
def principled(name, color, rough=0.5, coat=0.0, sheen=0.0, sss=0.0, bump=0.0, bump_scale=8.0, emission=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    for key, val in (("Coat Weight", coat), ("Sheen Weight", sheen), ("Subsurface Weight", sss)):
        if key in b.inputs: b.inputs[key].default_value = val
    if "Sheen Tint" in b.inputs and sheen: b.inputs["Sheen Tint"].default_value = (0.8, 0.9, 1.0, 1)
    if "Subsurface Radius" in b.inputs and sss: b.inputs["Subsurface Radius"].default_value = (0.4, 0.3, 0.25)
    if emission and "Emission Color" in b.inputs:
        b.inputs["Emission Color"].default_value = (*emission, 1); b.inputs["Emission Strength"].default_value = 1.0
    if bump:
        tc = nt.nodes.new("ShaderNodeTexCoord"); vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = bump_scale
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; bp.inputs["Distance"].default_value = 0.02
        nt.links.new(tc.outputs["Object"], vor.inputs["Vector"]); nt.links.new(vor.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m

def rgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)  # sRGB -> linear

MAT = {
    "blue": principled("MiloBlue", rgb("#0f5fd8"), 0.62, coat=0.08, sheen=0.35, bump=0.18, bump_scale=22),
    "dark": principled("MiloDark", rgb("#0a3fa0"), 0.62, coat=0.05, sheen=0.3, bump=0.18, bump_scale=16),
    "belly": principled("MiloBelly", rgb("#a9d2ff"), 0.65, sheen=0.4, bump=0.15, bump_scale=18),
    "beak": principled("Beak", rgb("#ffa21f"), 0.28, coat=0.8, sss=0.1),
    "white": principled("EyeWhite", rgb("#fbfdff"), 0.12, coat=1.0, sss=0.05),
    "pupil": principled("Pupil", rgb("#050303"), 0.45, coat=0.15),
    "cheek": principled("Cheek", rgb("#ff8fb0"), 0.6),
    "glint": principled("Glint", (1, 1, 1), 0.0, emission=(1, 1, 1)),
}
# iris: spherical gradient from the iris center -> brown rings
iris = bpy.data.materials.new("Iris"); iris.use_nodes = True
nt = iris.node_tree; b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.55
if "Coat Weight" in b.inputs: b.inputs["Coat Weight"].default_value = 0.0
tc = nt.nodes.new("ShaderNodeTexCoord"); gr = nt.nodes.new("ShaderNodeTexGradient"); gr.gradient_type = "SPHERICAL"
ramp = nt.nodes.new("ShaderNodeValToRGB"); el = ramp.color_ramp.elements
el[0].position, el[0].color = 0.0, (*rgb("#3a230d"), 1); el[1].position, el[1].color = 0.55, (*rgb("#b8742e"), 1)
mid = el.new(0.85); mid.color = (*rgb("#6b3f17"), 1)
nt.links.new(tc.outputs["Object"], gr.inputs["Vector"]); nt.links.new(gr.outputs["Color"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
MAT["iris"] = iris

# ---------------- helpers ----------------
def smooth(o):
    for p in o.data.polygons: p.use_smooth = True
    return o
def sphere(name, r, loc, scale=(1, 1, 1), mat=None, parent=None, segs=64, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segs, ring_count=segs // 2, radius=r, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = scale; smooth(o)
    if mat: o.data.materials.append(mat)
    if parent: o.parent = parent
    return o
def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); scene.collection.objects.link(o); o.location = loc
    if parent: o.parent = parent
    return o
def subsurf(o, lv=2):
    m = o.modifiers.new("Subsurf", "SUBSURF"); m.levels = lv; m.render_levels = lv
    return o

# ---------------- Milo (Blender axes: X right, Y back, Z up; Milo faces -Y) ----------------
root = empty("Milo", (-5, 0, 0))
rig = empty("MiloRig", (0, 0, 1.26), root)
body = sphere("Body", 1.0, (0, 0, 0), (1.02, 0.96, 0.98), MAT["blue"], rig, 96)
sphere("Belly", 0.8, (0, -0.42, -0.26), (0.95, 0.62, 0.9), MAT["belly"], rig, 72)
eyes, lids = [], []
for sx in (-1, 1):
    sock = empty(f"EyeSocket{sx}", (0.33 * sx, -0.74, 0.3), rig); sock.rotation_euler = (0, 0, -0.32 * sx)
    sphere(f"EyeWhite{sx}", 0.3, (0, 0, 0), (1, 0.72, 1), MAT["white"], sock, 64)
    ir = sphere(f"Iris{sx}", 0.2, (0, -0.17, 0), (1, 0.35, 1), MAT["iris"], sock, 48)
    sphere(f"Pupil{sx}", 0.115, (0, -0.24, 0), (1, 0.3, 1), MAT["pupil"], sock, 32)
    sphere(f"Glint{sx}", 0.04, (0.06 * sx + 0.03, -0.27, 0.07), (1, 0.5, 1), MAT["glint"], sock, 16)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.315)
    lid = bpy.context.object; lid.name = f"Lid{sx}"; smooth(lid); lid.data.materials.append(MAT["blue"]); lid.parent = sock
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="DESELECT"); bpy.ops.object.mode_set(mode="OBJECT")
    for v in lid.data.vertices: v.select = v.co.z < -0.01
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.delete(type="VERT"); bpy.ops.object.mode_set(mode="OBJECT")
    lid.scale = (1, 0.76, 1); lid.rotation_euler = (math.radians(-110), 0, 0)
    lids.append(lid)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.24, location=(0, -0.12, 0.36), rotation=(0, math.pi / 2, 0.12 * sx))
    brow = bpy.context.object; brow.name = f"Brow{sx}"; brow.data.materials.append(MAT["dark"]); brow.parent = sock; smooth(brow)
    sphere(f"Cheek{sx}", 0.15, (0.6 * sx, -0.7, 0.0), (1, 0.3, 0.6), MAT["cheek"], rig, 24)
beak = empty("Beak", (0, -0.88, -0.1), rig)
up = sphere("BeakUpper", 1.0, (0, -0.2, 0.02), (0.22, 0.36, 0.14), MAT["beak"], beak, 48)
jaw = empty("Jaw", (0, -0.02, 0), beak)
sphere("BeakLower", 1.0, (0, -0.16, -0.05), (0.2, 0.3, 0.12), MAT["beak"], jaw, 48)
for x, lean, ln in ((-0.11, 0.35, 0.5), (0.02, 0.05, 0.62), (0.15, -0.3, 0.45)):   # crest feathers (tapered curves)
    cu = bpy.data.curves.new("Crest", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.07; cu.bevel_resolution = 6
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(2)
    pts = [(x, -0.05, 0.9), (x - lean * 0.3, 0.0, 0.9 + ln * 0.55), (x - lean * 0.7, 0.18, 0.9 + ln)]
    for bp_, p, rad in zip(sp.bezier_points, pts, (1.0, 0.7, 0.15)):
        bp_.co = p; bp_.handle_left_type = bp_.handle_right_type = "AUTO"; bp_.radius = rad
    o = bpy.data.objects.new("Crest", cu); scene.collection.objects.link(o); o.parent = rig; cu.materials.append(MAT["blue"])
wings = []
for sx in (-1, 1):
    piv = empty(f"Wing{sx}", (0.9 * sx, -0.05, 0.12), rig)
    for k, (dz, s) in enumerate(((0, 1), (-0.12, 0.85), (-0.22, 0.7))):
        w = sphere(f"Feather{sx}{k}", 0.5, ((0.1 + 0.04 * k) * sx, 0.04 * k, -0.32 + dz), (0.2, 0.5 * s, 0.78 * s), MAT["dark"] if k else MAT["blue"], piv, 48)
        w.rotation_euler = (0, (0.28 + 0.08 * k) * sx, 0)
    wings.append((piv, sx))
tail = empty("Tail", (0, 0.9, -0.15), rig)
for a in (-0.35, 0, 0.35):
    f = sphere("TailFeather", 0.3, (math.sin(a) * 0.18, 0.18, 0), (0.42, 1, 0.18), MAT["dark"], tail, 32); f.rotation_euler = (-0.5, 0, a)
legs = []
for sx in (-1, 1):
    lg = empty(f"Leg{sx}", (0.3 * sx, -0.1, 0.42), root)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.4, location=(0, 0, -0.2)); sh = bpy.context.object; sh.parent = lg; sh.data.materials.append(MAT["beak"]); smooth(sh)
    for a in (-0.5, 0, 0.5):
        t = sphere("Toe", 0.05, (math.sin(a) * 0.1, -0.08 - math.cos(a) * 0.06, -0.41), (0.8, 2.2, 0.5), MAT["beak"], lg, 16); t.rotation_euler = (0, 0, a)
    legs.append(lg)

mem('milo')
# ---------------- world ----------------
world = bpy.data.worlds.new("Sky"); scene.world = world; world.use_nodes = True
wn = world.node_tree; bg = wn.nodes["Background"]
try:
    if opt('nosky'): raise Exception('nosky')
    sky = wn.nodes.new("ShaderNodeTexSky")
    for t in ("MULTIPLE_SCATTERING", "NISHITA", "HOSEK_WILKIE"):
        try: sky.sky_type = t; break
        except Exception: pass
    for a, v in (("sun_elevation", math.radians(38)), ("sun_rotation", math.radians(200)), ("altitude", 300)):
        if hasattr(sky, a): setattr(sky, a, v)
    wn.links.new(sky.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 0.18
except Exception:
    bg.inputs["Color"].default_value = (*rgb("#9fd4ff"), 1)

sun = bpy.data.lights.new("Sun", "SUN"); sun.energy = 2.6; sun.angle = math.radians(6); sun.color = (1, 0.95, 0.86)
so = bpy.data.objects.new("Sun", sun); scene.collection.objects.link(so); so.rotation_euler = (math.radians(52), 0, math.radians(200))
fill = bpy.data.lights.new("Fill", "AREA"); fill.energy = 120; fill.size = 6; fill.color = (1, 0.9, 0.8)
fo = bpy.data.objects.new("Fill", fill); scene.collection.objects.link(fo); fo.location = (-4, -6, 4); fo.rotation_euler = (math.radians(60), 0, math.radians(-35))
rim = bpy.data.lights.new("Rim", "AREA"); rim.energy = 160; rim.size = 4; rim.color = (0.75, 0.88, 1)
ro = bpy.data.objects.new("Rim", rim); scene.collection.objects.link(ro); ro.location = (4, 6, 3.5); ro.rotation_euler = (math.radians(-60), 0, math.radians(150))

mem('world')
# ---------------- ground + grass ----------------
bpy.ops.mesh.primitive_plane_add(size=60); ground = bpy.context.object; ground.name = "Ground"
gm = principled("Soil", rgb("#6fb04e"), 0.95); ground.data.materials.append(gm)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=140, y_subdivisions=140, size=26, location=(0, 4, 0.001)); lawn = bpy.context.object; lawn.name = "Lawn"
vg = lawn.vertex_groups.new(name="Dens")
for v in lawn.data.vertices:
    wx, wy = v.co.x + lawn.location.x, v.co.y + lawn.location.y
    d = math.hypot(wx / 1.35, wy)
    vg.add([v.index], max(0.0, min(1.0, (d - 1.7) / 0.8)), "REPLACE")
grassmat = principled("Grass", rgb("#5fae3c"), 0.6, sss=0.15)
lawn.data.materials.append(grassmat)
if int(opt('grass', 1)) > 0:
    ps = lawn.modifiers.new("Grass", "PARTICLE_SYSTEM").particle_system.settings
    ps.type = "HAIR"; ps.count = int(opt("grass", 6000 if TEST else 20000)); ps.hair_length = 0.28; ps.use_advanced_hair = True
    ps.child_type = "INTERPOLATED"; ps.rendered_child_count = 6 if TEST else 14; ps.child_length = 0.9; ps.child_length_threshold = 0.4
    ps.roughness_2 = 0.08; ps.roughness_endpoint = 0.05; ps.root_radius = 0.6; ps.tip_radius = 0.0; ps.radius_scale = 0.012
    ps.material = 1
    lawn.particle_systems[0].vertex_group_density = "Dens"
path = principled("Path", rgb("#e7cc96"), 1.0)
bpy.ops.mesh.primitive_circle_add(vertices=96, radius=1.9, fill_type="NGON", location=(0, 0, 0.004)); pad = bpy.context.object; pad.name = "Clearing"; pad.data.materials.append(path); pad.scale = (1.4, 1, 1)

_blobmats = {}
def blob(name, r, loc, color, scale=(1, 1, 1), strength=0.35, size=0.9):
    key = tuple(round(c, 3) for c in color)
    if key not in _blobmats: _blobmats[key] = principled(name + "Mat", color, 0.7, sss=0.08, bump=0.15, bump_scale=3)
    o = sphere(name, r, loc, scale, _blobmats[key], None, 48)
    for k in range(3):   # a few smaller lumps on the surface make it read as foliage
        a, b = random.random() * math.tau, random.uniform(-0.3, 0.9)
        dx, dy, dz = math.cos(a) * math.cos(b), math.sin(a) * math.cos(b), math.sin(b)
        sphere(name + "Lump", r * random.uniform(0.45, 0.6), (loc[0] + dx * r * 0.75 * scale[0], loc[1] + dy * r * 0.75 * scale[1], loc[2] + dz * r * 0.75 * scale[2]), scale, _blobmats[key], None, 32)
    return o
for i, (x, y, s) in enumerate(((-6.5, 6.5, 1.35), (6.8, 7.5, 1.55), (-10, 3, 1.2), (10, 3.5, 1.3), (-3.2, 11, 1.7), (3.6, 12, 1.5), (-14, 8, 1.8), (14, 9, 1.7))):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22 * s, depth=1.8 * s, location=(x, y, 0.9 * s)); tr = bpy.context.object; tr.data.materials.append(principled("Bark", rgb("#7a4b2e"), 0.9, bump=0.3, bump_scale=6))
    g = rgb(random.choice(("#4caf50", "#5cb85c", "#43a047")))
    for dx, z, dy, r in ((0, 2.3, 0, 1.15), (0.6, 2.0, 0.2, 0.75), (-0.55, 2.1, -0.1, 0.8), (0.1, 2.95, 0.05, 0.8)):
        blob(f"Leaves{i}", r * s, (x + dx * s, y + dy * s, z * s), g)
for x, y, s in ((-3.6, 3.2, 1), (3.9, 3.5, 1.2), (-5.4, -1.4, 0.8), (5.4, -0.9, 0.9)):
    blob("Bush", 0.7 * s, (x, y, 0.4 * s), rgb("#4caf50"), (1, 1, 0.72))
wood = principled("FenceWood", rgb("#fff8ee"), 0.55)
for i in range(11):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-10 + i * 2, 4.8, 0.45)); p = bpy.context.object; p.scale = (0.16, 0.16, 0.9); p.data.materials.append(wood)
for z in (0.35, 0.72):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 4.8, z)); r = bpy.context.object; r.scale = (20.4, 0.07, 0.1); r.data.materials.append(wood)
petals = [principled(f"Petal{i}", rgb(c), 0.5, sss=0.2) for i, c in enumerate(("#ff6f9c", "#ffd23f", "#ffffff", "#b57cff", "#ff9f43"))]
for i in range(120):
    a, rr = random.random() * math.tau, 2.3 + random.random() * 9
    f = sphere("Flower", 0.055, (math.cos(a) * rr, math.sin(a) * rr * 0.7 + 1.5, 0.24), (1, 1, 0.55), petals[i % 5], None, 12)
cloudm = principled("Cloud", (1, 1, 1), 1.0, sss=0.3, emission=(0.25, 0.25, 0.25))
for x, z, y, s in ((-10, 8, 26, 1.8), (7, 9.5, 30, 2.4), (18, 7.5, 24, 1.5), (-22, 9, 32, 2.2)):
    for k in range(6):
        sphere("Cloud", (0.7 + random.random() * 0.5) * s, (x + (k - 2.5) * 0.7 * s, y, z + random.random() * 0.5 * s), (1, 1, 1), cloudm, None, 32)

mem('scenery')
# ---------------- camera ----------------
cam = bpy.data.cameras.new("Cam"); cam.lens = 50; cam.dof.use_dof = True; cam.dof.aperture_fstop = 2.8
co = bpy.data.objects.new("Cam", cam); scene.collection.objects.link(co); scene.camera = co
focus = empty("Focus", (0, 0, 1.25), root); cam.dof.focus_object = focus
track = co.constraints.new("TRACK_TO"); aim = empty("Aim", (0, 0, 1.25)); track.target = aim; track.track_axis = "TRACK_NEGATIVE_Z"; track.up_axis = "UP_Y"

mem('anim_start')
# ---------------- animation ----------------
def smoothstep(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def key(o, path, frame, value):
    setattr(o, path, value); o.keyframe_insert(path, frame=frame)
end = round(SECONDS * FPS)
for f in range(1, end + 1):
    t = (f - 1) / FPS
    talk = mouth[f - 1] if f - 1 < len(mouth) else 0
    inP = smoothstep(t / 1.8); hop = 1.0 if t < 1.8 else (0.6 if t > SECONDS - 1.6 else 0.0)
    ph = math.sin(t * 7); hopZ = abs(ph) * 0.42 * hop
    land = max(0.0, 1 - abs(ph) * 5) * hop; sq = 1 - land * 0.12; breathe = math.sin(t * 2.4) * 0.022
    key(root, "location", f, (-5 * (1 - inP), 0, 0))
    look = 0.9 * (1 - inP) if t < 1.8 else math.sin(t * 0.7) * 0.22 + (math.sin(t * 2) * 0.35 if t > SECONDS - 1.6 else 0)
    key(rig, "location", f, (0, 0, 1.26 + breathe + hopZ))
    key(rig, "scale", f, (1 / math.sqrt(sq), 1 / math.sqrt(sq), sq * (1 + breathe * 0.6)))
    key(rig, "rotation_euler", f, (math.sin(t * 1.1) * 0.03 + talk * 0.04, math.sin(t * 1.3) * 0.035 + talk * 0.04, -look))
    for lg, s in zip(legs, (1, -1)):
        key(lg, "location", f, (lg.location.x, -0.1, 0.42 + hopZ * 0.92)); key(lg, "rotation_euler", f, (s * ph * 0.45 * (hop > 0), 0, 0))
    key(jaw, "rotation_euler", f, (-talk * 0.5, 0, 0)); key(up, "rotation_euler", f, (talk * 0.06, 0, 0))
    flap = 1.0 if 1.9 < t < 2.9 else 0.0
    fl = math.sin(t * (15 if flap else 2.6)) * (0.1 + flap * 0.85)
    for piv, sx in wings: key(piv, "rotation_euler", f, (0, -sx * (0.38 + fl + flap * 0.55), 0))
    blink = (t % 3.1) > 2.96
    for lid in lids: key(lid, "rotation_euler", f, (math.radians(78 if blink else -110), 0, 0))
    key(tail, "rotation_euler", f, (math.sin(t * 3) * 0.08, 0, math.sin(t * 2.2) * 0.15))
    push = smoothstep((t - 2) / (SECONDS - 2)); ang = 0.22 - t * 0.025; dist = 10 - push * 2.6
    key(co, "location", f, (math.sin(ang) * dist, -math.cos(ang) * dist, 2.2 - push * 0.45))
    key(aim, "location", f, (root.location.x * 0.6, 0, 1.25))
for o in bpy.data.objects:
    if o.animation_data and o.animation_data.action:
        try:
            for fc in o.animation_data.action.fcurves:
                for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
        except Exception: pass

mem('anim_done')
# ---------------- render settings ----------------
r = scene.render; r.resolution_x, r.resolution_y, r.resolution_percentage = W, H, 100
r.use_overwrite = False; r.use_placeholder = True
r.image_settings.file_format = "PNG"
os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
r.filepath = os.path.join(OUT, "frames", "f_")
scene.view_settings.view_transform = "AgX" if "AgX" in [i.identifier for i in type(scene.view_settings).bl_rna.properties["view_transform"].enum_items] else "Filmic"
scene.view_settings.exposure = -0.55
try: scene.view_settings.look = "AgX - Punchy"
except Exception: pass
try:
    scene.view_settings.use_curve_mapping = False
    scene.render.film_transparent = False
except Exception: pass
if ENGINE == "EEVEE":
    for e in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try: r.engine = e; break
        except Exception: pass
    try: scene.eevee.taa_render_samples = SAMPLES; scene.eevee.use_raytracing = True; scene.eevee.use_shadows = True
    except Exception: pass
else:
    r.engine = "CYCLES"; cy = scene.cycles; cy.samples = SAMPLES; cy.use_denoising = True; cy.use_adaptive_sampling = True
    cy.max_bounces = 6; cy.caustics_reflective = cy.caustics_refractive = False
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for dev in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
            try:
                prefs.compute_device_type = dev; prefs.get_devices()
                if any(d.type == dev for d in prefs.devices):
                    for d in prefs.devices: d.use = d.type == dev
                    cy.device = "GPU"; print("Cycles GPU:", dev); break
            except Exception: continue
    except Exception as e: print("GPU setup skipped:", e)

if opt('stats'):
    import resource as R
    last = R.getrusage(R.RUSAGE_SELF).ru_maxrss
    for o in list(scene.objects):
        o.hide_viewport = True
    dg = bpy.context.evaluated_depsgraph_get(); dg.update(); print('MEM base', R.getrusage(R.RUSAGE_SELF).ru_maxrss//1024)
    seen = set()
    for o in list(scene.objects):
        k = o.name.rstrip('0123456789.-')
        print('EVAL', o.name, o.type, flush=True); o.hide_viewport = False; dg.update()
        now = R.getrusage(R.RUSAGE_SELF).ru_maxrss
        if now - last > 50000: print('JUMP', o.name, o.type, (now - last)//1024, 'MB')
        last = now
    tot = {}
    for o in scene.objects:
        if o.type in ('MESH','CURVE'):
            e = o.evaluated_get(dg)
            try: n = len(e.to_mesh().polygons); e.to_mesh_clear()
            except Exception: n = -1
            k = o.name.rstrip('0123456789.-'); tot[k] = tot.get(k, 0) + n
    print('STATS', sorted(tot.items(), key=lambda x: -x[1])[:12]); mem('evaluated'); sys.exit(0)
if opt('drop'):
    pats = str(opt('drop')).split(',')
    for o in list(scene.objects):
        if any(o.name.startswith(p) for p in pats): bpy.data.objects.remove(o, do_unlink=True)
if TEST:
    for f in [int(x) for x in str(opt('frames', '24,72,200')).split(',')]:
        scene.frame_set(min(f, end)); r.filepath = os.path.join(OUT, f"test_{f:03d}.png"); bpy.ops.render.render(write_still=True); print("TEST", r.filepath)
    sys.exit(0)

bpy.ops.render.render(animation=True)
print("FRAMES DONE")

# ---------------- encode final.mp4 with audio (Blender's own FFmpeg) ----------------
enc = bpy.data.scenes.new("Encode"); bpy.context.window_scene = enc if bpy.context.window else enc
enc.render.fps = FPS; enc.render.resolution_x, enc.render.resolution_y = W, H; enc.frame_start = 1; enc.frame_end = end
seq = enc.sequence_editor_create()
frames = sorted(os.listdir(os.path.join(OUT, "frames")))
strips = seq.strips if hasattr(seq, "strips") else seq.sequences
img = strips.new_image("Frames", os.path.join(OUT, "frames", frames[0]), 1, 1)
for fn in frames[1:]: img.elements.append(fn)
if AUDIO and os.path.exists(AUDIO): strips.new_sound("Voice", AUDIO, 2, 1)
enc.render.image_settings.file_format = "FFMPEG"; enc.render.ffmpeg.format = "MPEG4"; enc.render.ffmpeg.codec = "H264"
enc.render.ffmpeg.constant_rate_factor = "HIGH"; enc.render.ffmpeg.audio_codec = "AAC"; enc.render.ffmpeg.audio_bitrate = 192
enc.render.filepath = os.path.join(OUT, "final.mp4")
bpy.ops.render.render(animation=True, scene=enc.name)
print("DONE", enc.render.filepath)
