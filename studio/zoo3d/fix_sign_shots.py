"""Nov 15: a close-up while the answer signs are up cuts the signs at the picture's edge (zool_ep09, zool_ep10 frames).
Patch an existing lesson job without re-voicing it: every line that starts while a sign is visible gets the 'teach' shot.
python3 fix_sign_shots.py jobs/<job>.json [out.json]   (teach.py now does the same for new lessons)"""
import json, sys, os
jp = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else jp
job = json.load(open(jp))
tm = json.load(open(os.path.join(os.path.dirname(jp), job["timing_file"])))
secs = tm["sections"]; lines = tm["lines"]; n = 0
for i, d in enumerate(job["direct"]):
    sc = next(s for s in secs if s["name"] == d["section"]); s0 = sc["start"] if i else 0.0
    sl = [l for l in lines if sc["start"] - 0.01 <= l["start"] < sc["end"]]
    win = [(p["delay"], p["delay"] + p["dur"]) for p in d["props"] if p.get("type") == "teach" and p.get("name") == "sign"]
    for k, l in enumerate(sl):
        if k >= len(d["shots"]): break
        ls = l["start"] - s0
        if any(a - 0.01 <= ls < b for a, b in win) and d["shots"][k] not in (None, "teach"):
            print(f"{d['section']} line {k} '{l['text'][:40]}': {d['shots'][k]} -> teach"); d["shots"][k] = "teach"; n += 1
json.dump(job, open(out, "w"), indent=1)
print(n, "shots changed ->", out)
