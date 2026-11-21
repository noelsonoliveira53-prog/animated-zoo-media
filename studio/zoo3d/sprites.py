"""Hybrid 2.5D asset renderer: one-time sprite library per character, background plates per set, prop sprites.

    blender -b -P sprites.py -- --job jobs/<id>.json                 # everything an episode needs (cast + set + props)
    blender -b -P sprites.py -- --char bloop [--opts '{"color":"#9d6bff"}'] [--light-set colorlab]
    blender -b -P sprites.py -- --set colorlab
    blender -b -P sprites.py -- --props jobs/<id>.json                # only the job's teaching props

Common options:
    --res 1920x1080      output video size the assets are made for (sprites/plates are sized from it)
    --engine EEVEE|CYCLES   --samples N
    --sprite-px N        sprite canvas (square); default 1.2 x output height
    --plate-os 1.3       plate overscan (plate pixels = res x os), --plate-pad 1.15 (extra field of view for pans)
    --loops idle,dance,wave  --angles front,q  --frames 24 (per bar)  --mouths 0,0.3,0.6,1.0
    --blink-loops idle,dance  --blink-mouths 0,0.6   (blink variants; "--blink-loops none" to skip)
    --mask-mats Jelly    materials whose region is written to a recolor mask (*_k.png); default per char (bloop)
    --bpm 116            only affects tiny time-based wobbles inside a loop
    --only chars|set|props   --force (re-render existing files)

Output: assets/<char key>/{front,q}/<loop>_m<i>_<ff>.png (+ _b blink, + _k mask) and manifest.json,
        assets/<set>/plates/<shot>.png + manifest.json, assets/<set>/props/<prop key>.png + manifest.json.
Frames already on disk are skipped, so an interrupted run resumes. A STOP file in assets/ stops it cleanly.
"""
import bpy, sys, os, json, math, importlib, random, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib as L
import hybrid_common as HC
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(name, default=None):
    if "--" + name in argv:
        i = argv.index("--" + name)
        return argv[i + 1] if i + 1 < len(argv) and not argv[i + 1].startswith("--") else True
    return default

def flist(s, cast=float):
    return [] if str(s).lower() in ("none", "") else [cast(x) for x in str(s).split(",")]

ENGINE = str(opt("engine", "EEVEE")).upper()
W, H = map(int, str(opt("res", "1920x1080")).split("x"))
SAMPLES = int(opt("samples", 24 if ENGINE == "EEVEE" else 64))
SPRITE_PX = int(opt("sprite-px", round(H * 1.2)))
PLATE_OS = float(opt("plate-os", 1.3))
PLATE_PAD = float(opt("plate-pad", 1.15))
NFR = int(opt("frames", 24))
MOUTHS = flist(opt("mouths", ",".join(str(m) for m in HC.MOUTHS)))
LOOP_NAMES = flist(opt("loops", "idle,dance,wave"), str)
ANGLE_NAMES = flist(opt("angles", "front,q"), str)
BLINK_LOOPS = flist(opt("blink-loops", "idle,dance"), str)
BLINK_MOUTHS = flist(opt("blink-mouths", "0,0.6"))
BPM = float(opt("bpm", 116))
FORCE = bool(opt("force", False))
ONLY = opt("only")
ASSETS = os.path.abspath(opt("assets", HC.ASSETS))
MASK_DEFAULT = {"bloop": ["Jelly"]}
CALIB = flist(opt("calib", "#ff3b3b,#ff8a1f,#ffd21f,#3ccf4e,#2f7bff,#3db8ff,#9d5cff,#ff6fb5,#9d6bff"), str)   # colors to calibrate the recolor

L.key = lambda o, path, f, v: setattr(o, path, v)     # poses are set directly, like engine.py


def stop_requested():
    return os.path.exists(os.path.join(ASSETS, "STOP"))


# ------------------------------------------------------------------ scene setup
def fresh():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    L._mats.clear()
    for m in list(sys.modules):
        if m.startswith("chars.") or m.startswith("sets."): del sys.modules[m]
    return bpy.context.scene


def render_setup(S, SET, w, h, transparent):
    r = S.render; r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, 100
    r.image_settings.file_format = "PNG"; r.image_settings.color_mode = "RGBA" if transparent else "RGB"
    r.film_transparent = transparent
    vt = [i.identifier for i in type(S.view_settings).bl_rna.properties["view_transform"].enum_items]
    S.view_settings.view_transform = "AgX" if "AgX" in vt else "Filmic"
    S.view_settings.exposure = SET.get("exposure", -0.3)
    try: S.view_settings.look = SET.get("look", "AgX - Punchy")
    except Exception: pass
    if ENGINE == "EEVEE":
        for e in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
            try: r.engine = e; break
            except Exception: pass
        ee = S.eevee
        for a, v in (("taa_render_samples", SAMPLES), ("use_raytracing", True), ("use_shadows", True), ("use_gtao", True),
                     ("use_bloom", True), ("shadow_ray_count", 1), ("shadow_step_count", 4), ("use_fast_gi", True), ("fast_gi_resolution", "4")):
            try: setattr(ee, a, v)
            except Exception: pass
    else:
        r.engine = "CYCLES"; cy = S.cycles; cy.samples = SAMPLES; cy.use_denoising = True; cy.use_adaptive_sampling = True; cy.max_bounces = 4
        try:
            prefs = bpy.context.preferences.addons["cycles"].preferences
            for dev in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
                try:
                    prefs.compute_device_type = dev; prefs.get_devices()
                    if any(d.type == dev for d in prefs.devices):
                        for d in prefs.devices: d.use = d.type == dev
                        cy.device = "GPU"; print("Cycles GPU:", dev); break
                except Exception: continue
        except Exception as ex: print("GPU setup skipped:", ex)
    return r


def make_cam(S, loc, aim, lens, fstop=None):
    cam = bpy.data.cameras.new("SprCam"); cam.lens = lens; cam.clip_end = 400; cam.sensor_width = HC.SENSOR
    co = bpy.data.objects.new("SprCam", cam); S.collection.objects.link(co); S.camera = co
    place_cam(co, loc, aim, lens, fstop)
    return co


def place_cam(co, loc, aim, lens, fstop=None):
    co.location = loc
    co.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    co.data.lens = lens
    if fstop:
        co.data.dof.use_dof = True; co.data.dof.aperture_fstop = fstop
        co.data.dof.focus_distance = (Vector(aim) - Vector(loc)).length
    else:
        co.data.dof.use_dof = False


def build_set(name):
    setmod = importlib.import_module("sets." + name)
    SET = setmod.build(L, random.Random(7))
    return setmod, SET


def hide_from_camera(objs):
    for o in objs:
        if o.type == "LIGHT": continue
        try: o.visible_camera = False
        except Exception: pass


def render_to(S, path):
    S.render.filepath = path
    bpy.ops.render.render(write_still=True)


def bbox_world(objs):
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    for o in objs:
        if o.type not in ("MESH", "FONT", "CURVE"): continue
        oe = o.evaluated_get(dg)
        for c in oe.bound_box:
            p = oe.matrix_world @ Vector(c)
            lo = Vector(map(min, lo, p)); hi = Vector(map(max, hi, p))
    return lo, hi


def descendants(o):
    out = [o]
    for c in o.children: out += descendants(c)
    return out


def cam_dict(co, w, h):
    from mathutils import Vector as V
    fwd = co.matrix_world.to_quaternion() @ V((0, 0, -1))
    return {"loc": list(co.location), "aim": list(co.location + fwd * 10), "lens": co.data.lens, "res": [w, h]}


# ------------------------------------------------------------------ characters
def render_char(char, opts, light_set, key=None):
    key = key or HC.char_key(char, opts)
    out = os.path.join(ASSETS, key); os.makedirs(out, exist_ok=True)
    S = fresh()
    setmod, SET = build_set(light_set)
    set_objs = list(S.objects)
    hide_from_camera(set_objs)
    for o in set_objs:   # loose decorations floating in the air would read as specks in reflections only; keep them
        pass
    mod = importlib.import_module("chars." + char)
    bopts = {k: v for k, v in opts.items() if k not in HC.STRIP}
    ch = mod.build(L, "Spr", (0, 0, 0), **bopts)
    char_objs = descendants(ch.root)
    h = float(getattr(ch, "height", 2.2)); fz = float(getattr(ch, "face_z", h * 0.6))
    E = max(1.8 * h, 3.4)                       # vertical extent of the canvas in world units
    cz = 0.52 * h
    lens = 60.0
    D = (E / 2) / (HC.SENSOR / 2 / lens)
    elev = math.radians(5)
    cam_loc = (0, -D, cz + D * math.tan(elev)); cam_aim = (0, 0, cz)
    co = make_cam(S, cam_loc, cam_aim, lens)
    r = render_setup(S, SET, SPRITE_PX, SPRITE_PX, True)
    camd = {"loc": list(cam_loc), "aim": list(cam_aim), "lens": lens, "res": [SPRITE_PX, SPRITE_PX]}
    ax, ay, _ = HC.project((0, 0, 0), camd)
    _, hy, _ = HC.project((0, 0, h), camd)
    ppu = (ay - hy) / h

    mask_names = flist(opt("mask-mats", ",".join(MASK_DEFAULT.get(char, []))), str)
    mask_objs = []
    if mask_names:
        allm = {m.name for o in char_objs if o.type == "MESH" for m in o.data.materials if m}
        for m in bpy.data.materials:
            hit = any(n in m.name for n in mask_names)
            m.diffuse_color = (1, 1, 1, 1) if hit else (0, 0, 0, 1)
            m.roughness = 1.0; m.metallic = 0.0
        mask_objs = char_objs
        print("mask materials:", sorted(n for n in allm if any(k in n for k in mask_names)))

    def mask_pass(path):
        eng = S.render.engine; vt = S.view_settings.view_transform; look = S.view_settings.look; ex = S.view_settings.exposure
        for o in set_objs: o.hide_render = True
        S.render.engine = "BLENDER_WORKBENCH"
        sh = S.display.shading; sh.light = "FLAT"; sh.color_type = "MATERIAL"
        for a, v in (("show_object_outline", False), ("show_specular_highlight", False), ("show_shadows", False), ("show_cavity", False)):
            try: setattr(sh, a, v)
            except Exception: pass
        try: S.display.render_aa = "8"
        except Exception: pass
        S.view_settings.view_transform = "Standard"; S.view_settings.exposure = 0
        try: S.view_settings.look = "None"
        except Exception: pass
        render_to(S, path)
        S.render.engine = eng; S.view_settings.view_transform = vt; S.view_settings.exposure = ex
        try: S.view_settings.look = look
        except Exception: pass
        for o in set_objs: o.hide_render = False

    barlen = 4 * 60.0 / BPM
    jobs = []   # (path, angle, loop, mouth, fi, blink)
    for ang in ANGLE_NAMES:
        for lp in LOOP_NAMES:
            for mi, m in enumerate(MOUTHS):
                for fi in range(NFR):
                    jobs.append((os.path.join(out, ang, f"{lp}_m{mi}_{fi:02d}.png"), ang, lp, m, fi, False))
            if lp in BLINK_LOOPS:
                for m in BLINK_MOUTHS:
                    mi = min(range(len(MOUTHS)), key=lambda k: abs(MOUTHS[k] - m))
                    for fi in range(NFR):
                        jobs.append((os.path.join(out, ang, f"{lp}_b_m{mi}_{fi:02d}.png"), ang, lp, m, fi, True))
    t0 = time.time(); done = 0
    for path, ang, lp, m, fi, blink in jobs:
        if stop_requested(): print("STOP file found"); sys.exit(3)
        need_main = FORCE or not (os.path.exists(path) and os.path.getsize(path) > 200)
        mpath = path[:-4] + "_k.png"
        need_mask = bool(mask_objs) and (FORCE or not os.path.exists(mpath))
        if not (need_main or need_mask): continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        bar = fi / NFR; t = bar * barlen
        st = dict(HC.LOOPS[lp]); st.update({"talk": m, "beat": (bar * 4) % 1.0, "bar": bar, "look": 0.0, "blink": blink,
                                            "singing": m > 0, "t_section": t, "bpm": BPM})
        ch.root.rotation_euler = (0, 0, HC.ANGLES.get(ang, 0.0))
        ch.pose(fi, t, st)
        S.frame_set(fi)
        if need_main: render_to(S, path)
        if need_mask: mask_pass(mpath)
        done += 1
        if done % 12 == 0:
            el = time.time() - t0
            print(f"[{key}] {done}/{len(jobs)}  {el / done:.2f}s/frame", flush=True)
    calib_cols = [c for c in CALIB if c] if mask_objs else []
    if calib_cols:
        # one reference frame per schedule color (front, dance, mouth 0, frame 0): compose.py measures the real
        # rendered hue/saturation/value from these, so the masked hue shift lands on the true AgX-rendered color
        bar = 0.0; st = dict(HC.LOOPS["dance"]); st.update({"talk": 0.0, "beat": 0.0, "bar": 0.0, "look": 0.0, "blink": False,
                                                            "singing": False, "t_section": 0.0, "bpm": BPM})
        ch.root.rotation_euler = (0, 0, 0); ch.pose(0, 0.0, st); S.frame_set(0)
        mats = [m for m in bpy.data.materials if any(n in m.name for n in mask_names) and m.node_tree]
        saved = {m.name: [tuple(m.node_tree.nodes["Principled BSDF"].inputs[k].default_value) for k in ("Base Color", "Emission Color")
                          if k in m.node_tree.nodes["Principled BSDF"].inputs] for m in mats}
        for hx in calib_cols:
            fp = os.path.join(out, "calib", hx.lstrip("#").lower() + ".png")
            if os.path.exists(fp) and not FORCE: continue
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            lin = L.rgb(hx)
            for m in mats:
                lite = 0.45 if "Lite" in m.name else 0.0      # bloop.jelly_mat convention: the shine material is the color mixed with white
                c = tuple(x + (1 - x) * lite for x in lin)
                b_ = m.node_tree.nodes["Principled BSDF"]
                for k in ("Base Color", "Emission Color"):
                    if k in b_.inputs: b_.inputs[k].default_value = (*c, 1)
            render_to(S, fp)
        for m in mats:
            b_ = m.node_tree.nodes["Principled BSDF"]
            for k, v in zip(("Base Color", "Emission Color"), saved[m.name]):
                if k in b_.inputs: b_.inputs[k].default_value = v
        if bopts.get("color"):
            fp = os.path.join(out, "calib", bopts["color"].lstrip("#").lower() + ".png")
            if not os.path.exists(fp): render_to(S, fp)

    avail = {}
    for ang in ANGLE_NAMES:
        for lp in LOOP_NAMES:
            avail.setdefault(ang, {})[lp] = {"n": NFR, "mouths": MOUTHS,
                "blink": sorted({min(range(len(MOUTHS)), key=lambda k: abs(MOUTHS[k] - m)) for m in BLINK_MOUTHS}) if lp in BLINK_LOOPS else []}
    old = HC.load_json(os.path.join(out, "manifest.json"), {}) or {}
    for ang, lps in (old.get("available") or {}).items():
        for lp, v in lps.items():
            avail.setdefault(ang, {}).setdefault(lp, v)
    man = {"key": key, "char": char, "opts": bopts, "light_set": light_set, "engine": ENGINE, "samples": SAMPLES,
           "sprite_px": SPRITE_PX, "made_for_res": [W, H], "bpm": BPM, "frames_per_bar": NFR, "mouths": MOUTHS,
           "loops": {k: HC.LOOPS[k] for k in LOOP_NAMES}, "angles": {k: HC.ANGLES[k] for k in ANGLE_NAMES},
           "blink": {"loops": BLINK_LOOPS, "mouths": BLINK_MOUTHS}, "mask": bool(mask_objs), "mask_mats": mask_names,
           "calib": sorted(fn[:-4] for fn in os.listdir(os.path.join(out, "calib"))) if os.path.isdir(os.path.join(out, "calib")) else [],
           "home_color": bopts.get("color"), "anchor": [ax, ay], "ppu": ppu, "height": h, "face_z": fz, "close_dist": float(getattr(ch, "close_dist", 6.4)),
           "camera": camd, "available": avail,
           "frame_count": sum(1 for a in os.listdir(out) if os.path.isdir(os.path.join(out, a))
                              for fn in os.listdir(os.path.join(out, a)) if fn.endswith(".png") and not fn.endswith("_k.png")),
           "mask_frames": sum(1 for a in os.listdir(out) if os.path.isdir(os.path.join(out, a))
                              for fn in os.listdir(os.path.join(out, a)) if fn.endswith("_k.png")),
           "render_seconds": round(time.time() - t0, 1) + float(old.get("render_seconds", 0) if old.get("camera") == camd else 0)}
    json.dump(man, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print("CHAR DONE", key, len(jobs), "frames", flush=True)
    return man


# ------------------------------------------------------------------ set plates
CLOSE_FACE, CLOSE_DIST = 1.4, 7.4   # generic close plate: wide enough that the biggest host still fits (2D zoom-in for smaller casts)


def plate_shots(SET, cast_h=1.0):
    """(name, loc, aim, lens, fstop) for every shot engine.py can cut to, posed at the middle of the shot."""
    cams = SET["cams"]; c = cams.get("center", (0, 0, 1.4)); r = cams.get("orbit_r", 9)
    shots = []
    for name, v in cams.items():
        if isinstance(v, (list, tuple)) and len(v) == 2 and isinstance(v[0], (list, tuple)):
            loc, tgt = v
            push = 1 - 0.12 * 0.0       # plate at the start of the push; the push-in is a 2D zoom
            shots.append((name, tuple(loc), tuple(tgt), 35, 4.0))
    shots.append(("orbit", (c[0], c[1] - r, c[2] + 1.0), tuple(c), 35, 4.0))
    shots.append(("low", (c[0], c[1] - 6.5, 0.45), (c[0], c[1], c[2] + 0.8), 28, 4.0))
    shots.append(("top", (c[0], c[1] - 5.5, c[2] + 6.0), tuple(c), 32, 4.0))
    for sp, (bx, by, bz) in SET["spots"].items():   # generic close-up plates; compose.py zooms per character
        fz = bz + CLOSE_FACE; dist = CLOSE_DIST
        for side, tag in ((-0.35, "L"), (0.35, "R")):
            shots.append((f"close_{sp}_{tag}", (bx + side * dist * 0.4, by - dist, fz + 0.35), (bx, by, fz - 0.1), 45, 4.0))
    return shots


def render_set(name, shots_only=None):
    out = os.path.join(ASSETS, name, "plates"); os.makedirs(out, exist_ok=True)
    S = fresh()
    setmod, SET = build_set(name)
    if hasattr(setmod, "animate"):
        try: setmod.animate(L, SET, 0, 0.0, {"beat": 0.5, "bar": 0, "energy": 0.5, "bpm": BPM, "talk": 0})
        except Exception as ex: print("animate skipped:", ex)
    pw, ph = round(W * PLATE_OS), round(H * PLATE_OS)
    co = None; man = {"set": name, "engine": ENGINE, "samples": SAMPLES, "made_for_res": [W, H], "overscan": PLATE_OS, "pad": PLATE_PAD,
                      "spots": {k: list(v) for k, v in SET["spots"].items()}, "cams": {}, "prop_spots": {k: list(v) for k, v in SET.get("prop_spots", {}).items()},
                      "plates": {}}
    for k, v in SET["cams"].items():
        man["cams"][k] = v if not isinstance(v, tuple) else [list(x) if isinstance(x, tuple) else x for x in v]
    t0 = time.time(); n = 0
    render_setup(S, SET, pw, ph, False)
    for shot, loc, aim, lens, fstop in plate_shots(SET):
        if shots_only and shot not in shots_only and shot.split("_")[0] not in shots_only: continue
        if stop_requested(): sys.exit(3)
        eff = lens / PLATE_PAD
        if co is None: co = make_cam(S, loc, aim, eff, fstop)
        else: place_cam(co, loc, aim, eff, fstop)
        fp = os.path.join(out, shot + ".png")
        if FORCE or not os.path.exists(fp):
            render_to(S, fp); n += 1
        man["plates"][shot] = {"file": f"plates/{shot}.png", "loc": list(loc), "aim": list(aim), "lens": eff, "base_lens": lens,
                               "res": [pw, ph], "fstop": fstop}
        if shot.startswith("close_"): man["plates"][shot].update({"dist": CLOSE_DIST, "face": CLOSE_FACE})
    man["render_seconds"] = round(time.time() - t0, 1)
    old = HC.load_json(os.path.join(ASSETS, name, "manifest.json"), {}) or {}
    if old.get("plates"):
        old["plates"].update(man["plates"]); man["plates"] = old["plates"]
        man["render_seconds"] += float(old.get("render_seconds", 0))
    man["frame_count"] = len(man["plates"])
    json.dump(man, open(os.path.join(ASSETS, name, "manifest.json"), "w"), indent=1)
    print("SET DONE", name, n, "plates rendered", flush=True)
    return man


# ------------------------------------------------------------------ props
def collect_props(job):
    seen = {}
    for d in job.get("direct", []):
        for p in d.get("props", []):
            if p.get("type") in ("text", "set_prop", "shape"):
                seen[HC.prop_key(p)] = HC.prop_spec(p)
    return seen


def render_props(set_name, specs):
    out = os.path.join(ASSETS, set_name, "props"); os.makedirs(out, exist_ok=True)
    manp = os.path.join(out, "manifest.json"); man = HC.load_json(manp, {}) or {}
    todo = {k: v for k, v in specs.items() if FORCE or k not in man or not os.path.exists(os.path.join(out, k + ".png"))}
    if not todo:
        print("PROPS up to date", flush=True); return man
    S = fresh()
    setmod, SET = build_set(set_name)
    set_objs = list(S.objects); hide_from_camera(set_objs)
    fp = os.path.join(HERE, "fonts", "Poppins-Bold.ttf")
    font = bpy.data.fonts.load(fp) if os.path.exists(fp) else None
    at = (0, 0.5, 2.6)
    co = None
    for key, p in todo.items():
        if stop_requested(): sys.exit(3)
        before = set(bpy.data.objects)
        if p["type"] == "text":
            m = L.mat("Prop" + p.get("color", "#ffcc00"), p.get("color", "#ffcc00"), 0.3, coat=0.6, emission=p.get("color", "#ffcc00"), emit=p.get("emit", 0.25))
            o = L.text3d("PropText", p["text"], p.get("size", 1.2), at, m, extrude=0.18, bevel=0.04)
            if font: o.data.font = font
        elif p["type"] == "set_prop" and hasattr(setmod, "prop"):
            o = setmod.prop(L, p["name"], at, **p.get("opts", {}))
        elif p["type"] == "shape":
            m = L.mat("Shape" + p.get("color", "#ff5252"), p.get("color", "#ff5252"), 0.25, coat=0.8)
            shp = p.get("shape", "sphere")
            o = (L.sphere if shp == "sphere" else L.cube)("PropShape", 0.6 if shp == "sphere" else 1.1, at, m=m)
        else:
            continue
        objs = [x for x in bpy.data.objects if x not in before]
        lo, hi = bbox_world(objs)
        ext = max(hi.x - lo.x, hi.z - lo.z) * 1.15 + 0.2
        cx, cz = (lo.x + hi.x) / 2, (lo.z + hi.z) / 2
        lens = 60.0; D = (ext / 2) / (HC.SENSOR / 2 / lens)
        loc = (cx, at[1] - D, cz + D * math.tan(math.radians(4))); aim = (cx, at[1], cz)
        px = max(64, int(min(SPRITE_PX, H * 0.9) * min(1.0, ext / 4.0) + 0.5))
        if co is None: co = make_cam(S, loc, aim, lens)
        else: place_cam(co, loc, aim, lens)
        render_setup(S, SET, px, px, True)
        render_to(S, os.path.join(out, key + ".png"))
        camd = {"loc": list(loc), "aim": list(aim), "lens": lens, "res": [px, px]}
        ax, ay, _ = HC.project(at, camd); _, ty, _ = HC.project((at[0], at[1], at[2] + 1), camd)
        man[key] = {"file": key + ".png", "spec": p, "anchor": [ax, ay], "ppu": ay - ty, "px": px}
        for x in objs: x.hide_render = True
        json.dump(man, open(manp, "w"), indent=1)
        print("PROP", key, flush=True)
    return man


# ------------------------------------------------------------------ main
def main():
    os.makedirs(ASSETS, exist_ok=True)
    if opt("job"):
        jp = os.path.abspath(opt("job")); job = json.load(open(jp))
        tp = os.path.join(os.path.dirname(jp), job["timing_file"])
        global BPM
        if os.path.exists(tp) and not opt("bpm"): BPM = float(json.load(open(tp)).get("bpm", BPM))
        if ONLY in (None, "set"): render_set(job["set"])
        if ONLY in (None, "props"): render_props(job["set"], collect_props(job))
        if ONLY in (None, "chars"):
            done = set()
            for c in job["cast"]:
                k = HC.char_key(c["char"], c.get("opts", {}))
                if k in done: continue
                done.add(k)
                sched = c.get("opts", {}).get("color_schedule")
                if sched and not opt("calib"):
                    global CALIB
                    CALIB = sorted({h.lower() for _, h in sched})
                render_char(c["char"], c.get("opts", {}), opt("light-set", job["set"]), k)
        return
    if opt("char"):
        render_char(opt("char"), json.loads(opt("opts", "{}")), opt("light-set", "colorlab"))
    if opt("set"):
        render_set(opt("set"), flist(opt("shots"), str) if opt("shots") else None)
    if opt("props"):
        job = json.load(open(os.path.abspath(opt("props"))))
        render_props(job["set"], collect_props(job))


if __name__ == "__main__":
    main()
