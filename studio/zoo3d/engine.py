"""ZooBlender 3D sing-along renderer.

blender -b -P engine.py -- --job jobs/<id>.json [--test] [--frames 100,900] [--res 960x540] [--engine CYCLES|EEVEE] [--samples N]

A job.json carries: channel, set, cast, the song timing (from sing.py), a direction list per song section,
and the song audio. Frames render one at a time (poses are set directly, no keyframes), so a stopped render
resumes where it left off. Output: out/<id>/frames/*.png then out/<id>/<id>_raw.mp4 (with the song audio).
"""
import bpy, sys, os, json, math, importlib, random, time, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib as L
importlib.reload(L)

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(name, default=None):
    if "--" + name in argv:
        i = argv.index("--" + name)
        return argv[i + 1] if i + 1 < len(argv) and not argv[i + 1].startswith("--") else True
    return default

JOB_PATH = os.path.abspath(opt("job"))
JOB_DIR = os.path.dirname(JOB_PATH)
job = json.load(open(JOB_PATH))
TEST = bool(opt("test", False))
ENGINE = str(opt("engine", job.get("engine", "EEVEE"))).upper()
W, H = map(int, str(opt("res", "960x540" if TEST else job.get("res", "1280x720"))).split("x"))   # default: 720p, upscaled to 1080p when assembling
SAMPLES = int(opt("samples", 16 if TEST else job.get("samples", 24 if str(opt("engine", job.get("engine", "EEVEE"))).upper() == "EEVEE" else 64)))
OUT = os.path.abspath(opt("out", os.path.join(os.path.dirname(JOB_DIR), "out", job["id"])))
timing = job.get("timing") or json.load(open(os.path.join(JOB_DIR, job["timing_file"])))
FPS = timing.get("fps", 24)
DUR = timing["duration"]
NF = int(math.ceil(DUR * FPS))

# setting values directly (no keyframes): characters call L.key(o, path, f, v)
L.key = lambda o, path, f, v: setattr(o, path, v)

bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene
S.render.fps = FPS
rng = random.Random(job.get("seed", 7))

# ---------------------------------------------------------------- set + cast
setmod = importlib.import_module("sets." + job["set"])
SET = setmod.build(L, rng, **job.get("set_opts", {}))
spots = SET["spots"]
cast = {}
for c in job["cast"]:
    mod = importlib.import_module("chars." + c["char"])
    sp = spots.get(c.get("spot", "center"), (0, 0, 0)) if isinstance(c.get("spot", "center"), str) else c["spot"]
    ch = mod.build(L, c["id"].capitalize(), tuple(sp), **c.get("opts", {}))
    ch.id = c["id"]; ch.base = tuple(sp); ch.scale = c.get("opts", {}).get("scale", 1.0)
    ch.root.rotation_euler = (0, 0, c.get("yaw", 0))
    cast[c["id"]] = ch
host_id = job["cast"][0]["id"]

# ---------------------------------------------------------------- props (pop-in teaching objects)
PROP_AT = SET.get("prop_spots", {"top": (0, 0.5, 3.6), "left": (-3, 0.5, 2.2), "right": (3, 0.5, 2.2), "front": (0, -1.5, 1.0)})
props = []   # (obj, t0, t1, base_scale, spin)
_fp = os.path.join(HERE, "fonts", "Poppins-Bold.ttf")
PROP_FONT = bpy.data.fonts.load(_fp) if os.path.exists(_fp) else None
for d in job["direct"]:
    sec = next((s for s in timing["sections"] if s["name"] == d["section"]), None)
    if not sec: continue
    for k, p in enumerate(d.get("props", [])):
        at = PROP_AT.get(p.get("at", "top"), (0, 0.5, 3.6)) if isinstance(p.get("at", "top"), str) else tuple(p["at"])
        if p["type"] == "text":
            m = L.mat("Prop" + p.get("color", "#ffcc00"), p.get("color", "#ffcc00"), 0.3, coat=0.6, emission=p.get("color", "#ffcc00"), emit=p.get("emit", 0.25))
            o = L.text3d("PropText", p["text"], p.get("size", 1.2), at, m, extrude=0.18, bevel=0.04)
            if PROP_FONT: o.data.font = PROP_FONT
        elif p["type"] == "set_prop" and hasattr(setmod, "prop"):
            o = setmod.prop(L, p["name"], at, **p.get("opts", {}))
        elif p["type"] == "shape":
            m = L.mat("Shape" + p.get("color", "#ff5252"), p.get("color", "#ff5252"), 0.25, coat=0.8)
            shp = p.get("shape", "sphere")
            o = (L.sphere if shp == "sphere" else L.cube)("PropShape", 0.6 if shp == "sphere" else 1.1, at, m=m)
        else:
            continue
        t0 = sec["start"] + p.get("delay", 0) + k * p.get("stagger", 0)
        if p.get("word"):   # pop in right as the word is sung (nth occurrence inside this section)
            _wn = "".join(ch for ch in p["word"].lower() if ch.isalnum())
            _ws = [w for w in timing["words"] if sec["start"] - 0.01 <= w["start"] < sec["end"] and "".join(ch for ch in w["w"].lower() if ch.isalnum()) == _wn]
            if len(_ws) > p.get("nth", 0): t0 = _ws[p.get("nth", 0)]["start"] - 0.12 + p.get("delay", 0)
        t1 = DUR if p.get("hold") else (min(sec["end"], t0 + p["dur"]) if p.get("dur") else sec["end"])
        props.append((o, t0, t1, tuple(o.scale), p.get("spin", 0.4)))
        o.scale = (0, 0, 0)

# ---------------------------------------------------------------- camera
cam = bpy.data.cameras.new("Cam"); cam.lens = 40; cam.clip_end = 400; cam.dof.use_dof = True; cam.dof.aperture_fstop = 4.0
co = bpy.data.objects.new("Cam", cam); S.collection.objects.link(co); S.camera = co
aim = L.empty("Aim", (0, 0, 1.4))
tr = co.constraints.new("TRACK_TO"); tr.target = aim; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"
cam.dof.focus_object = aim

def shot_pose(shot, u, t):
    """Camera (loc, aim, lens) for a shot name; u = 0..1 progress through the shot (slow push-in)."""
    if shot.startswith("close"):
        cid = shot.split(":")[1] if ":" in shot else host_id
        ch = cast.get(cid, cast[host_id]); bx, by, bz = ch.base; sc = ch.scale
        fz = bz + ch.face_z * sc
        dist = (getattr(ch, "close_dist", 6.4) - 0.6 * u) * sc
        side = 0.35 if zlib.crc32(cid.encode()) % 2 else -0.35
        return (bx + side * dist * 0.4, by - dist, fz + 0.35 * sc), (bx, by, fz - 0.1 * sc), 45
    if shot == "orbit":
        a = -0.6 + 1.2 * u
        c = SET["cams"].get("center", (0, 0, 1.4)); r = SET["cams"].get("orbit_r", 9)
        return (c[0] + math.sin(a) * r, c[1] - math.cos(a) * r, c[2] + 1.0), c, 35
    if shot == "low":
        c = SET["cams"].get("center", (0, 0, 1.4))
        return (c[0] + 1.2 - 2.4 * u, c[1] - 6.5, 0.45), (c[0], c[1], c[2] + 0.8), 28
    if shot == "top":
        c = SET["cams"].get("center", (0, 0, 1.4))
        return (c[0], c[1] - 5.5, c[2] + 6.5 - u), c, 32
    loc, tgt = SET["cams"].get(shot, SET["cams"]["wide"])
    push = 1 - 0.12 * u
    return (tgt[0] + (loc[0] - tgt[0]) * push, tgt[1] + (loc[1] - tgt[1]) * push, tgt[2] + (loc[2] - tgt[2]) * push), tgt, 35

# shot list over time: each section cycles its shots per line (cuts land on line starts)
# v2 (Nov 13, 2026), opt-in per job:
#   "cut_mode": "beat"     -> every cut snaps to the nearest beat (on the music, not between beats)
#   "cut_beats": {"chorus": 4, "bridge": 4, "verse": 8, ...} -> extra cuts every N beats inside long lines/sections
#   "follow_singer": true  -> when a line is sung by one animal, cut to a close-up of that animal (lip-sync on screen)
#   "punch": true          -> small camera punch-in on every downbeat in high-energy sections (energy >= 0.9)
_beats = timing.get("beats") or []
def _snap(t):
    if job.get("cut_mode") != "beat" or not _beats: return t
    b = min(_beats, key=lambda x: abs(x - t))
    return b if abs(b - t) <= 0.3 else t
_cutb = job.get("cut_beats", {})
_bl = 60 / timing["bpm"]
cuts = []   # (t_start, shot, section_directive)
dmap = {d["section"]: d for d in job["direct"]}
prev = None
for sec in timing["sections"]:
    d = dmap.get(sec["name"], {})
    shots = d.get("shots", ["wide"])
    sec_end = sec.get("end") or next((s2["start"] for s2 in timing["sections"] if s2["start"] > sec["start"]), DUR)
    lns = [l for l in timing["lines"] if sec["start"] - 0.01 <= l["start"] < sec_end]
    ls = [l["start"] for l in lns]
    starts = [sec["start"]] + [x for x in ls if x - sec["start"] > 0.8]
    kind = "".join(ch for ch in sec["name"] if ch.isalpha())
    nb = d.get("cut_beats", _cutb.get(kind))
    if nb:   # add cuts every nb beats where the gap to the next cut is long
        ext = []
        bnd = starts + [sec_end]
        for a, b in zip(bnd, bnd[1:]):
            x = a + nb * _bl
            while x < b - nb * _bl * 0.5:
                ext.append(x); x += nb * _bl
        starts = sorted(starts + ext)
    for k, st in enumerate(starts):
        shot = shots[k % len(shots)]
        if job.get("follow_singer"):
            ln = next((l for l in lns if abs(l["start"] - st) < 0.05), None)
            if ln and ln.get("who") not in (None, "host", "all", host_id) and ln.get("who") in cast and k % 2 == 1:
                shot = "close:" + ln["who"]
        if shot == prev and len(shots) > 1: shot = shots[(k + 1) % len(shots)]
        prev = shot
        cuts.append((_snap(st), shot, d))
if not cuts or cuts[0][0] > 0:
    cuts.insert(0, (0.0, job.get("intro_shot", "orbit"), job.get("intro", {"energy": 0.6})))
cuts.sort(key=lambda c: c[0])
_dd = []
for c in cuts:   # drop cuts closer than 1 beat to the previous one (snapping can stack them)
    if _dd and c[0] - _dd[-1][0] < _bl * 0.9: _dd[-1] = c if c[0] == _dd[-1][0] else _dd[-1]; continue
    _dd.append(c)
cuts = _dd

def cut_at(t):
    i = max(k for k, c in enumerate(cuts) if c[0] <= t)
    t0 = cuts[i][0]; t1 = cuts[i + 1][0] if i + 1 < len(cuts) else DUR
    return cuts[i][1], (t - t0) / max(0.01, t1 - t0), cuts[i][2]

def who_sings(t):
    for l in timing["lines"]:
        if l["start"] - 0.05 <= t <= l["end"] + 0.05:
            return l.get("who", host_id), l.get("kind", "sing")
    return None, None

beats = timing["beats"]; beat_len = 60 / timing["bpm"]
mouth = timing["mouth"]

def state_for(ch, f, t):
    shot, u, d = cut_at(t)
    who, kind = who_sings(t)
    m = mouth[f] if f < len(mouth) else 0
    singing = who in (ch.id, "all") or (who == "host" and ch.id == host_id) or (d.get("group") and kind == "sing")
    bpos = (t / beat_len) % 1.0; barpos = (t / (beat_len * 4)) % 1.0
    e = d.get("energy", 0.5) * (1.0 if ch.id == host_id or singing else 0.7)
    if t < 1.5: e *= L.smoothstep(t / 1.5)
    rr = random.Random(zlib.crc32(f"{ch.id}{int(t / 3.3)}".encode()))
    blink = (t + rr.random() * 3) % 3.3 > 3.15
    look = 0.0
    if not singing and who and who in cast:   # turn toward whoever is singing
        sx = cast[who].base[0] - ch.base[0]
        look = max(-0.6, min(0.6, sx * 0.15))
    return {"talk": m if singing else 0.0, "energy": e, "beat": bpos, "bar": barpos, "look": look,
            "wave": d.get("wave", 0) * (1 if (t % (beat_len * 8)) < beat_len * 2 else 0), "jump": d.get("jump", 0),
            "blink": blink, "singing": singing, "t_section": t, "bpm": timing["bpm"]}

def apply(f):
    t = f / FPS
    for ch in cast.values():
        ch.pose(f, t, state_for(ch, f, t))
    for o, t0, t1, bs, spin in props:
        if t < t0 or t > t1 + 0.4: s = 0.0
        elif t < t0 + 0.45: x = (t - t0) / 0.45; s = 1 + math.sin(x * math.pi) * 0.25 if x > 0.6 else L.smoothstep(x / 0.6) * 1.1
        elif t > t1: s = 1 - L.smoothstep((t - t1) / 0.4)
        else: s = 1 + math.sin((t / beat_len) * math.pi * 2) * 0.04
        o.scale = (bs[0] * s, bs[1] * s, bs[2] * s)
        o.hide_render = (s == 0)
        o.rotation_euler.z = math.sin(t * 1.3) * spin
    shot, u, d = cut_at(t)
    loc, tgt, lens = shot_pose(shot, L.smoothstep(u), t)
    sway = 0.05 * math.sin(t * 0.9)
    if job.get("punch") and d.get("energy", 0.5) >= 0.9:   # punch-in on each downbeat, eases out over the beat
        bp = (t / beat_len) % 4.0
        lens = lens * (1 + 0.035 * math.exp(-bp * 5) if bp < 1 else 1)
    co.location = (loc[0] + sway, loc[1], loc[2] + 0.03 * math.sin(t * 1.3)); aim.location = tgt; cam.lens = lens
    if hasattr(setmod, "animate"): setmod.animate(L, SET, f, t, {"beat": (t / beat_len) % 1.0, "bar": (t / (beat_len * 4)) % 1.0, "energy": d.get("energy", 0.5), "bpm": timing["bpm"], "talk": mouth[f] if f < len(mouth) else 0})

# ---------------------------------------------------------------- render settings
r = S.render; r.resolution_x, r.resolution_y, r.resolution_percentage = W, H, 100
r.image_settings.file_format = "PNG"
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
    for a, v in (("taa_render_samples", SAMPLES), ("use_raytracing", True), ("use_shadows", True), ("use_gtao", True), ("use_bloom", True), ("shadow_ray_count", 1), ("shadow_step_count", 4), ("use_fast_gi", True), ("fast_gi_resolution", "4")):
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

FR = os.path.join(OUT, "frames"); os.makedirs(FR, exist_ok=True)
if TEST:
    fl = [int(x) for x in str(opt("frames", f"{FPS*2},{NF//3},{NF//2},{NF*3//4}")).split(",")]
    for f in fl:
        f = min(f, NF - 1); apply(f); S.frame_set(f)
        r.filepath = os.path.join(OUT, f"test_{f:05d}.png"); bpy.ops.render.render(write_still=True); print("TEST", r.filepath, flush=True)
    sys.exit(0)

thumb = job.get("thumb_frame")
t_start = time.time(); done = 0
STEP = int(opt("step", job.get("step", 2)))   # default: on twos (12 fps animation)
RANGE = job.get("frame_range") or [0, NF]          # re-render just a slice (frames named from 0 inside the slice)
for f in range(int(RANGE[0]), min(int(RANGE[1]), NF), STEP):
    fp = os.path.join(FR, f"{(f - int(RANGE[0])) // STEP:05d}.png")
    if os.path.exists(fp) and os.path.getsize(fp) > 1000: continue
    def _stop(pth):   # a STOP file pauses rendering unless its text starts with RESUME
        try: return os.path.exists(pth) and not open(pth, encoding="utf-8", errors="ignore").read().strip().upper().startswith("RESUME")
        except Exception: return True
    if _stop(os.path.join(os.path.dirname(OUT), "STOP")) or _stop(os.path.join(OUT, "STOP")):
        print("STOP file found - stopping (frames so far are kept)", flush=True); sys.exit(3)
    apply(f); S.frame_set(f)
    r.filepath = fp; bpy.ops.render.render(write_still=True); done += 1
    if done % 48 == 0:
        el = time.time() - t_start
        print(f"frame {f}/{NF}  {el / done:.2f}s/frame  ~{(NF - f) * el / done / 60:.0f} min left", flush=True)
print("FRAMES DONE", flush=True)

# ---------------------------------------------------------------- encode
# Frames are done. The worker assembles them with ffmpeg + the song (works on every Blender version).
# If ffmpeg isn't available, fall back to Blender's own encoder.
open(os.path.join(OUT, "FRAMES_DONE"), "w").write(time.strftime("%Y-%m-%d %H:%M:%S"))
if not opt("blender-encode"):
    sys.exit(0)
audio = os.path.join(JOB_DIR, job["audio"]) if job.get("audio") else None
enc = bpy.data.scenes.new("Encode")
enc.render.fps = FPS; enc.render.resolution_x, enc.render.resolution_y = W, H; enc.frame_start = 1; enc.frame_end = NF
seq = enc.sequence_editor_create()
frames = sorted(x for x in os.listdir(FR) if x.endswith(".png"))
strips = seq.strips if hasattr(seq, "strips") else seq.sequences
img = strips.new_image("Frames", os.path.join(FR, frames[0]), 1, 1)
for fn in frames[1:]: img.elements.append(fn)
if audio and os.path.exists(audio): strips.new_sound("Song", audio, 2, 1)
ims = enc.render.image_settings
if hasattr(ims, "media_type"):
    try: ims.media_type = "VIDEO"
    except Exception as ex: print("media_type:", ex)
ims.file_format = "FFMPEG"; enc.render.ffmpeg.format = "MPEG4"; enc.render.ffmpeg.codec = "H264"
enc.render.ffmpeg.constant_rate_factor = "HIGH"; enc.render.ffmpeg.audio_codec = "AAC"; enc.render.ffmpeg.audio_bitrate = 192
enc.render.filepath = os.path.join(OUT, job["id"] + "_raw.mp4")
bpy.ops.render.render(animation=True, scene=enc.name)
open(os.path.join(OUT, "DONE"), "w").write(time.strftime("%Y-%m-%d %H:%M:%S"))
print("DONE", enc.render.filepath, flush=True)
