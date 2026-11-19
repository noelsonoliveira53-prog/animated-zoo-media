"""Test stills, one place at a time (the local software EEVEE stalls when the lab and 8 outdoor places are in one scene).
python3 stills_by_place.py <id> <tag> seg:line:frac ... -> out/<id>/test_<frame>.png and out/<id>/sheet_<tag>.png (Nov 19, Gizmo explainers)"""
import json, os, subprocess, sys, collections
Z = os.path.dirname(os.path.abspath(__file__))
sid, tag = sys.argv[1], sys.argv[2]; T = json.load(open(f"{Z}/jobs/{sid}_timing.json")); J = json.load(open(f"{Z}/jobs/{sid}.json"))
secs = {s["name"]: s for s in T["sections"]}
def lstart(lc):
    s = secs[lc["from"]]["start"]
    if lc.get("line"):
        ls = [l for l in T["lines"] if l["section"] == lc["from"]]; s = ls[lc["line"]]["start"]
    return s
starts = [lstart(lc) for lc in J["locations"]]
frames = collections.defaultdict(list); labels = []
for a in sys.argv[3:]:
    p = a.split(":"); ls = [l for l in T["lines"] if l["section"] == p[0]]; l = ls[int(p[1])]
    fr = float(p[2]) if len(p) > 2 else 0.6
    t = l["start"] + (fr if fr > 1 else fr * (l["end"] - l["start"]))
    li = max(i for i, s0 in enumerate(starts) if s0 <= t + 1e-6); f = int(t * 24)
    frames[li].append(f); labels.append((f, a))
out = f"{Z}/out/{sid}"; os.makedirs(out, exist_ok=True); subprocess.run(f"rm -f {out}/test_*.png", shell=True)
for li, fs in frames.items():
    j = dict(J); j["id"] = sid; j["locations"] = [dict(J["locations"][li], **{"from": J["locations"][0]["from"]})]; j["locations"][0].pop("line", None)
    jp = f"{Z}/jobs/_tmp_{sid}_{li}.json"; json.dump(j, open(jp, "w"))
    subprocess.run(["timeout", "900", "/root/bpyenv/bin/python", "bpyrun.py", "engine.py", "--", "--job", jp, "--test", "--engine", "EEVEE", "--res", "960x540",
                    "--samples", "6", "--frames", ",".join(map(str, fs))], cwd=Z, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(jp); print("place", li, J["locations"][li]["biome"], fs, flush=True)
# label each still with its spec ref, tile
lab = []
for f, a in sorted(labels):
    src = f"{out}/test_{f:05d}.png"
    if os.path.exists(src):
        dst = f"{out}/lab_{f:05d}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", f"drawtext=text='{a.replace(":", " ")} f{f}':x=10:y=h-40:fontsize=28:fontcolor=white:borderw=3:bordercolor=black", dst]); lab.append(dst)
n = len(lab); cols = 3
subprocess.run(f"ffmpeg -y -loglevel error -pattern_type glob -i '{out}/lab_*.png' -vf tile={cols}x{-(-n // cols)}:padding=4 {out}/sheet_{tag}.png", shell=True)
subprocess.run(f"rm -f {out}/lab_*.png", shell=True)
print("sheet", f"{out}/sheet_{tag}.png", n, "of", len(labels))
