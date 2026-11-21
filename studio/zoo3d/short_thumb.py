"""Custom thumbnail for a Short that is already cut (Noelson, Nov 14 2026: every video gets its own thumbnail when it is posted).
  python3 short_thumb.py <short.mp4 path inside the repo> [--t seconds] [--text "3 WORDS MAX"]
Takes the frame at --t (default 62% through: the answer is on screen), boosts it a little, optionally adds big words
(yt-package: 3 words max, never the title's words) and writes brand/zoo/shorts/thumb_<name>.png (1080x1920).
With --plan it also stores "thumb" (and "thumb_text") in studio/upload_plan_shorts_zoo.json for that file."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FONT = os.path.join(HERE, "fonts", "Baloo2-ExtraBold.ttf")
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d

def make(rel, t=None, text=""):
    src = os.path.join(REPO, rel)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
    t = float(t) if t is not None else dur * 0.62
    out = os.path.join(REPO, "brand", "zoo", "shorts", "thumb_" + os.path.splitext(os.path.basename(rel))[0] + ".png"); os.makedirs(os.path.dirname(out), exist_ok=True)
    vf = "scale=1080:1920:flags=lanczos,eq=saturation=1.15:contrast=1.05"
    if text:
        tt = text.replace("'", "’").replace(":", "\\:"); fs = min(150, int(940 / max(1, len(tt) * 0.62)))
        vf += f",drawtext=fontfile={FONT}:text='{tt}':fontsize={fs}:fontcolor=0xFFD23F:borderw=12:bordercolor=0x402010:x=(w-tw)/2:y=640"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-vf", vf, "-frames:v", "1", out], check=True)
    return os.path.relpath(out, REPO)

if __name__ == "__main__":
    rel = sys.argv[1]; th = make(rel, arg("--t"), arg("--text", ""))
    print("thumb", th)
    if "--plan" in sys.argv:
        p = os.path.join(REPO, "studio", "upload_plan_shorts_zoo.json"); d = json.load(open(p)); L = d if isinstance(d, list) else next(v for v in d.values() if isinstance(v, list))
        for e in L:
            if e.get("file") == rel:
                e["thumb"] = th
                if arg("--text"): e["thumb_text"] = arg("--text")
        json.dump(d, open(p, "w"), indent=1)
