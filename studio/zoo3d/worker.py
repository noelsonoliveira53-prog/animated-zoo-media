"""ZooBlender render worker (runs inside Blender's own Python, so nothing else needs installing).

Started by START_RENDER_WORKER.bat:  blender.exe -b --factory-startup --python zoo3d\\worker.py
Loop: for every jobs\\<id>.json without out\\<id>\\DONE ->
  1) render 3D frames (separate Blender process, EEVEE on the GPU; resumes if stopped)
  2) assemble out\\<id>\\<id>_raw.mp4 with ffmpeg + jobs\\<id>_song.wav
Writes worker.log (everything) and status.txt (one line: what it's doing now).
"""
import os, sys, time, glob, subprocess, datetime, traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOBS, OUT = os.path.join(ROOT, "jobs"), os.path.join(ROOT, "out")
os.makedirs(JOBS, exist_ok=True); os.makedirs(OUT, exist_ok=True)
BLENDER = sys.argv[0] if sys.argv[0].lower().endswith(".exe") else None
try:
    import bpy
    BLENDER = bpy.app.binary_path or BLENDER
except Exception:
    pass

def read(p):
    try: return open(p, encoding="utf-8", errors="ignore").read().strip().strip('"').strip()
    except Exception: return ""

def log(msg):
    line = f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line, flush=True)
    with open(os.path.join(ROOT, "worker.log"), "a", encoding="utf-8") as f: f.write(line + "\n")

def status(msg):
    with open(os.path.join(ROOT, "status.txt"), "w", encoding="utf-8") as f: f.write(f"{msg} {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n")

# ---------------------------------------------------------------- songs (ACE-Step 1.5, local GPU, MIT license)
import json, urllib.request
ACE = os.path.join(ROOT, "acestep")
SONGS = os.path.join(ROOT, "songs_out"); os.makedirs(SONGS, exist_ok=True)
API = "http://127.0.0.1:8001"
_ace_proc = None

def find_uv():
    la, up = os.environ.get("LOCALAPPDATA", ""), os.environ.get("USERPROFILE", "")
    for c in [read(os.path.join(ROOT, "uv_path.txt")), os.path.join(la, "Microsoft", "WinGet", "Links", "uv.exe"),
              os.path.join(up, ".local", "bin", "uv.exe"), os.path.join(up, ".cargo", "bin", "uv.exe"), "uv"]:
        if not c: continue
        try:
            if subprocess.run([c, "--version"], capture_output=True, timeout=20).returncode == 0: return c
        except Exception: continue
    return None

def http(path, body=None, timeout=60):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"}, method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r: return r.read()

def ace_up():
    global _ace_proc
    try: http("/health", timeout=5); return True
    except Exception: pass
    uv = find_uv()
    if not uv or not os.path.isdir(ACE): log("songs: ACE-Step not installed - run INSTALL_SONG_ENGINE.bat"); return False
    if _ace_proc is None or _ace_proc.poll() is not None:
        log("songs: starting ACE-Step API (first start downloads the model, can take 10+ min)")
        _ace_proc = subprocess.Popen([uv, "run", "acestep-api"], cwd=ACE, stdout=open(os.path.join(ROOT, "acestep.log"), "a"), stderr=subprocess.STDOUT)
    for _ in range(240):
        time.sleep(5)
        try: http("/health", timeout=5); log("songs: ACE-Step API ready"); return True
        except Exception: pass
    log("songs: ACE-Step API did not come up - see acestep.log"); return False

def dig(o, key):
    if isinstance(o, dict):
        if key in o: return o[key]
        for v in o.values():
            r = dig(v, key)
            if r is not None: return r
    if isinstance(o, list):
        for v in o:
            r = dig(v, key)
            if r is not None: return r
    return None

def make_song(sid, sp):
    out = os.path.join(SONGS, sid); os.makedirs(out, exist_ok=True)
    spec = json.load(open(sp, encoding="utf-8"))
    mp3 = os.path.join(out, "song.mp3")
    if not os.path.exists(mp3):
        if not ace_up(): return False
        status(f"SONG {sid}")
        body = {"prompt": spec["style"], "lyrics": spec["lyrics"], "audio_duration": spec.get("duration", 180), "bpm": spec.get("bpm"),
                "key_scale": spec.get("key", "C Major"), "time_signature": "4/4", "vocal_language": "en", "audio_format": "mp3",
                "inference_steps": spec.get("steps", 8), "seed": spec.get("seed", -1), "thinking": spec.get("thinking", True), "batch_size": 1}
        r = json.loads(http("/release_task", body))
        tid = dig(r, "task_id") or dig(r, "id")
        log(f"{sid}: song task {tid}")
        for _ in range(360):
            time.sleep(5)
            q = json.loads(http("/query_result", {"task_id_list": [tid]}))
            st = dig(q, "status")
            if st == 2: log(f"{sid}: song generation failed: {str(q)[:400]}"); return False
            if st == 1:
                res = dig(q, "result"); res = json.loads(res) if isinstance(res, str) else res
                f = dig(res, "file")
                open(mp3, "wb").write(http(f if f.startswith("/") else "/v1/audio?path=" + f, timeout=300))
                open(os.path.join(out, "meta.json"), "w").write(json.dumps(res))
                break
        else:
            log(f"{sid}: song timed out"); return False
    lyr = os.path.join(out, "lyrics.txt"); open(lyr, "w", encoding="utf-8").write(spec["lyrics"])
    status(f"ALIGNING {sid}")
    p = subprocess.run([find_uv(), "run", "--with", "stable-ts", "python", os.path.join(ROOT, "zoo3d", "align.py"), mp3, lyr, os.path.join(out, "words.json")],
                       cwd=ACE, capture_output=True, text=True)
    if p.returncode != 0: log(f"{sid}: align failed: {p.stderr[-600:]}"); return False
    open(os.path.join(out, "SONG_DONE"), "w").write(datetime.datetime.now().isoformat())
    log(f"{sid}: SONG DONE -> {mp3}")
    return True


def find_ffmpeg():
    cands = [read(os.path.join(ROOT, "ffmpeg_path.txt"))]
    la = os.environ.get("LOCALAPPDATA", "")
    cands.append(os.path.join(la, "Microsoft", "WinGet", "Links", "ffmpeg.exe"))
    cands += glob.glob(os.path.join(la, "Microsoft", "WinGet", "Packages", "Gyan.FFmpeg*", "ffmpeg-*", "bin", "ffmpeg.exe"))
    cands += [r"C:\ffmpeg\bin\ffmpeg.exe", "ffmpeg"]
    for c in cands:
        if not c: continue
        try:
            if subprocess.run([c, "-version"], capture_output=True, timeout=20).returncode == 0: return c
        except Exception: continue
    return None

def render_frames(jid, jp):
    status(f"RENDERING {jid}")
    log(f"{jid}: rendering 3D frames")
    eng = os.path.join(ROOT, "zoo3d", "engine.py")
    with open(os.path.join(OUT, jid + ".log"), "a", encoding="utf-8", errors="ignore") as lf:
        lf.write(f"\n===== {datetime.datetime.now()} start =====\n"); lf.flush()
        p = subprocess.run([BLENDER, "-b", "--factory-startup", "-P", eng, "--", "--job", jp, "--engine", "EEVEE"], stdout=lf, stderr=subprocess.STDOUT)
    log(f"{jid}: blender exit code {p.returncode}")
    return os.path.exists(os.path.join(OUT, jid, "FRAMES_DONE"))

def assemble(jid, ff):
    status(f"ASSEMBLING {jid}")
    fr = os.path.join(OUT, jid, "frames", "%05d.png")
    song = os.path.join(JOBS, jid + "_song.wav")
    mp4 = os.path.join(OUT, jid, jid + "_raw.mp4")
    try: job = json.load(open(os.path.join(JOBS, jid + ".json")))
    except Exception: job = {}
    step = int(job.get("step", 1))
    cmd = [ff, "-y", "-loglevel", "error", "-framerate", str(24 / step), "-i", fr]
    if os.path.exists(song): cmd += ["-i", song]
    vf = ["fps=24"]                                   # on-twos frames are held for 2 frames each
    if str(job.get("res", "1920x1080")) != "1920x1080": vf.append("scale=1920:1080:flags=lanczos")   # upscale 720p renders
    cmd += ["-vf", ",".join(vf), "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p"]
    if os.path.exists(song): cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-movflags", "+faststart", mp4]
    log(f"{jid}: assembling MP4 with ffmpeg")
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0 or not os.path.exists(mp4):
        log(f"{jid}: ffmpeg failed: {p.stderr[-800:]}"); return False
    open(os.path.join(OUT, jid, "DONE"), "w").write(datetime.datetime.now().isoformat())
    log(f"{jid}: DONE -> {mp4} ({os.path.getsize(mp4) // 1048576} MB)")
    return True

def main():
    log(f"worker started. Blender: {BLENDER}")
    ff = find_ffmpeg()
    log(f"ffmpeg: {ff}")
    if ff: open(os.path.join(ROOT, "ffmpeg_path.txt"), "w").write(ff)
    fails = {}
    while True:
        busy = False
        for sp in sorted(glob.glob(os.path.join(JOBS, "*.song.json"))):
            sid = os.path.basename(sp)[:-len(".song.json")]
            if os.path.exists(os.path.join(SONGS, sid, "SONG_DONE")) or fails.get("song:" + sid, 0) >= 3: continue
            busy = True
            try:
                if not make_song(sid, sp): fails["song:" + sid] = fails.get("song:" + sid, 0) + 1
            except Exception:
                fails["song:" + sid] = fails.get("song:" + sid, 0) + 1; log(f"{sid}: song crashed: {traceback.format_exc()[-1200:]}")
        for jp in sorted(glob.glob(os.path.join(JOBS, "*.json"))):
            jid = os.path.splitext(os.path.basename(jp))[0]
            if jid.endswith("_timing") or jid.endswith(".song") or os.path.exists(os.path.join(OUT, jid, "DONE")): continue
            if fails.get(jid, 0) >= 3: continue
            busy = True
            try:
                ok = os.path.exists(os.path.join(OUT, jid, "FRAMES_DONE")) or render_frames(jid, jp)
                if ok and ff: ok = assemble(jid, ff)
                elif ok and not ff:
                    log(f"{jid}: frames done but ffmpeg is missing"); ok = False
                if not ok:
                    fails[jid] = fails.get(jid, 0) + 1
                    log(f"{jid}: problem (attempt {fails[jid]}/3) - see out\\{jid}.log")
            except Exception:
                fails[jid] = fails.get(jid, 0) + 1
                log(f"{jid}: crashed: {traceback.format_exc()[-1500:]}")
        if not busy:
            status("IDLE")
            time.sleep(60)
            fails = {k: v for k, v in fails.items() if v < 3}

main()
