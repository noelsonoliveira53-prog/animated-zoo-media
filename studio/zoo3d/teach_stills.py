"""Test stills for a v2 lesson: python3 teach_stills.py <id> "seg:line[:frac]" ...  (frac 0..1 through the line, or >1 = seconds after it starts)
Renders them with the local bpy (EEVEE, 960x540) and tiles them into out/<id>/sheet.png."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sid = sys.argv[1]; T = json.load(open(f"{HERE}/jobs/{sid}_timing.json"))
frames = []
for a in sys.argv[2:]:
    p = a.split(":"); ls = [l for l in T["lines"] if l["section"] == p[0]]; l = ls[int(p[1])]
    fr = float(p[2]) if len(p) > 2 else 0.6
    t = l["start"] + (fr if fr > 1 else fr * (l["end"] - l["start"]))
    frames.append(int(t * 24))
out = f"{HERE}/out/{sid}"; subprocess.run(f"rm -f {out}/test_*.png", shell=True)
subprocess.run(["/root/bpyenv/bin/python", "bpyrun.py", "engine.py", "--", "--job", f"jobs/{sid}.json", "--test", "--engine", "EEVEE", "--res", "960x540",
                "--samples", "6", "--frames", ",".join(map(str, frames))], cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
n = len(frames); cols = 3 if n > 4 else 2
subprocess.run(f"ffmpeg -y -loglevel error -pattern_type glob -i '{out}/test_*.png' -vf tile={cols}x{-(-n // cols)}:padding=4 {out}/sheet.png", shell=True)
print("sheet", f"{out}/sheet.png", sorted(frames))
