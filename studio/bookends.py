"""The main intro at the BEGINNING and at the END of every new long video of The Animated Zoo, 2D and 3D.

Owner, Nov 20 2026 4:50 PM: "awesome I like it, now let's include that at the end of every long version new video we upload in 2D and 3D as
well"; 4:51 PM: "Let's see how it works by including them at the beginning and at the end".

Where it goes
  2D (cartoon lesson, Guess With Milo, adventure): in the episode itself, `*intro_shots()` right after the hook (the episode still opens on
      its promise) and again as the LAST shots. toon.py's plan check fails an episode that has it in only one place.
  3D songs: finish.py lays it before the song (0:00) and after it, in the one encode it does anyway.
  Never: Shorts, the other channels (it says "The Animated Zoo"), a fix of a video that is already live.
  Gizmo Explains has its OWN main intro since Nov 21 2026 (owner, 12:18 PM: "amazing emplement on every new video and update the worflows"):
      `*gz_intro_shots()` (studio/cartoon/intro_gizmo.py) right after the hook and as the last four shots of every new long Gizmo cartoon;
      `check <video> --channel gizmo` compares with cartoon/gzintro.mp4, and review.py does that for Gizmo's plan.
The gate: review.py fails a new long video whose file does not carry it at both ends (`check` below).

  python3 studio/bookends.py check <video>                 is the intro in the first 75 s and at the very end?   exit 0 = both
  python3 studio/bookends.py add <video> <out> [--preview]  lay it on both ends of a FINISHED file (one more encode: for a sample, or for a
                                                            finished 3D song whose raw render is gone). --preview: 1080p, fast, to look at.
"""
import os, sys, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
INTRO = os.path.join(REPO, "cartoon", "zintro.mp4")
INTROS = {"zoo": INTRO, "gizmo": os.path.join(REPO, "cartoon", "gzintro.mp4")}      # Gizmo Explains has its own main intro (owner, Nov 21 2026 12:18 PM: "amazing emplement on every new video")
LONG_ZOO = ("3d_singalong", "cartoon_lesson", "cartoon_adventure")      # the formats that carry it
W, H = 160, 90
SAME = 14.0      # mean grey difference (0-255) under which two small frames show the same picture (the logo card against itself: 1-5; against another scene: 30+)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())


def _frames(path, t0, t1, fps):
    """Small grey frames of [t0, t1) at `fps` pictures a second."""
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{max(0, t0):.2f}", "-t", f"{max(.05, t1 - t0):.2f}", "-i", path, "-vf", f"fps={fps},scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (W * H)
    return np.frombuffer(raw[:n * W * H], np.uint8).reshape(n, H, W).astype(np.float32)


_REF = None
def use(channel):
    """Check against another channel's intro: use("gizmo") before check() for a Gizmo Explains video (studio/cartoon/intro_gizmo.py, cartoon/gzintro.mp4)."""
    global INTRO, _REF
    INTRO = INTROS[channel]; _REF = None


def _ref():
    """The settled logo card with the whole cast (the intro's last second and a half)."""
    global _REF
    if _REF is None: d = dur(INTRO); _REF = _frames(INTRO, d - 1.5, d - .1, 4)
    return _REF


def _best(fr):
    return min((float(np.mean(np.abs(a - b))) for a in fr for b in _ref()), default=999.0)


def check(path, verbose=False):
    """(intro near the beginning, intro at the very end). Beginning: the logo card shows up in the first 75 s (2D: after the hook; 3D: at 0:00)."""
    T = dur(path)
    b = _best(_frames(path, 8, min(75, T / 2), 2)); e = _best(_frames(path, T - 2.2, T - .1, 4))
    if verbose: print(f"  beginning: best match {b:.1f}  end: best match {e:.1f}  (same picture under {SAME:g})")
    return b < SAME, e < SAME


def concat_filter(i1, i2, vsong, asong, loud, vout="v", aout="a", w=3840, h=2160, fmt="yuv420p10le"):
    """filter_complex piece: [intro i1] + [the song's finished picture and sound] + [intro i2] -> [vout][aout].
    The intro is opened TWICE (two inputs): one input split in two would make ffmpeg hold the whole 4K intro in memory until the song is over."""
    v = lambda i, o: f"[{i}:v]fps=24,scale={w}:{h}:flags=lanczos,format={fmt},setsar=1[{o}];"
    a = lambda i, o: f"[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[{o}];"
    return (v(i1, "zi1") + v(i2, "zi2") + f"[{vsong}]fps=24,scale={w}:{h}:flags=lanczos,format={fmt},setsar=1[zsv];[zi1][zsv][zi2]concat=n=3:v=1:a=0[{vout}];"
            + a(i1, "za1") + a(i2, "za2") + f"[{asong}]{loud + ',' if loud else ''}aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[zsa];"
            + f"[za1][zsa][za2]concat=n=3:v=0:a=1[{aout}]")


def shift_hide(hide, total):
    """Watermark-hide windows of the song, moved to the finished file's clock, plus the two intros themselves (they carry their own mark, top left)."""
    d = dur(INTRO); out = [[0.0, round(d, 2)]] + [[round(a + d, 2), round(b + d, 2)] for a, b in (hide or [])] + [[round(total - d, 2), round(total, 2)]]
    return out


def add(src, dst, preview=False):
    """The intro on both ends of a finished file (one more encode of the whole video)."""
    T = dur(src) + 2 * dur(INTRO)
    if preview:
        fc = concat_filter(1, 2, "0:v", "0:a", "", w=1920, h=1080, fmt="yuv420p")
        enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p"]
    else:
        vb = int(((94 * 8 * 1e6) / T - 192e3) * 0.96)
        fc = concat_filter(1, 2, "0:v", "0:a", "")
        enc = ["-c:v", "libsvtav1", "-preset", "9", "-b:v", str(vb), "-svtav1-params", "tune=0", "-g", "240", "-pix_fmt", "yuv420p10le"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", INTRO, "-i", INTRO, "-filter_complex", fc, "-map", "[v]", "-map", "[a]"] + enc
                   + ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", dst], check=True)
    return dst


if __name__ == "__main__":
    if "--channel" in sys.argv: use(sys.argv[sys.argv.index("--channel") + 1]); del sys.argv[sys.argv.index("--channel"):sys.argv.index("--channel") + 2]
    if len(sys.argv) >= 3 and sys.argv[1] == "check":
        b, e = check(sys.argv[2], verbose=True)
        print(("BOOKENDS yes" if b and e else "BOOKENDS NO") + f" (beginning: {'yes' if b else 'NO'}, end: {'yes' if e else 'NO'})", sys.argv[2]); sys.exit(0 if b and e else 1)
    elif len(sys.argv) >= 4 and sys.argv[1] == "add":
        print("WROTE", add(sys.argv[2], sys.argv[3], "--preview" in sys.argv))
    else: print(__doc__)
