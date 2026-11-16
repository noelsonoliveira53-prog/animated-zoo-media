"""Tile the newest `toon.py --stills` frames into one sheet to look at: python3 sheet.py <proj dir> <out.jpg> [cols] [width]"""
import sys, glob, os, subprocess, re
proj, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3; w = int(sys.argv[4]) if len(sys.argv) > 4 else 960
d = max(glob.glob(os.path.join(proj, ".hyperframes/artifacts/snapshots/*/")), key=lambda x: max(os.path.getmtime(f) for f in glob.glob(x + "*")))
fr = sorted(glob.glob(d + "frame-*.png"))
keep = [f for f in fr if not re.search(r"at-\d+\.\d{3}s", f)] or fr
ins = []; fc = ""
for k, f in enumerate(keep):
    t = re.search(r"at-([\d.]+)s", f).group(1); ins += ["-i", f]
    fc += f"[{k}:v]scale={w}:-2,drawtext=text='{t} s':x=10:y=h-44:fontsize=30:fontcolor=white:box=1:boxcolor=black@0.6[s{k}];"
import PIL.Image as I
iw, ih = I.open(keep[0]).size; h = round(w * ih / iw / 2) * 2
lay = "|".join(f"{(k % cols) * w}_{(k // cols) * h}" for k in range(len(keep)))
fc += "".join(f"[s{k}]" for k in range(len(keep))) + f"xstack=inputs={len(keep)}:layout={lay}:fill=white[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", fc, "-map", "[v]", "-frames:v", "1", "-q:v", "3", out], check=True); print(out, len(keep))
