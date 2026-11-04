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
    cmd = [ff, "-y", "-loglevel", "error", "-framerate", "24", "-i", fr]
    if os.path.exists(song): cmd += ["-i", song]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p"]
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
        for jp in sorted(glob.glob(os.path.join(JOBS, "*.json"))):
            jid = os.path.splitext(os.path.basename(jp))[0]
            if jid.endswith("_timing") or os.path.exists(os.path.join(OUT, jid, "DONE")): continue
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
