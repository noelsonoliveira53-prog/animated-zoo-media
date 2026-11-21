"""Validate a channel's week-2 files and append render chunks. Usage: CHANNEL=<ch> python3 queue_w2.py <ch> <subdir> <shorts.json> <plan.json> <ep_glob...>"""
import json, sys, glob, build, long
ch, sub, shf, planf = sys.argv[1:5]
s = json.load(open(shf)); ids = {x["id"] for x in s}
bad = [x["id"] for x in s if x["animal"] not in build.SCENES]
for f in sys.argv[5:]:
    for p in glob.glob(f):
        e = json.load(open(p)); bad += [p + ":" + a["key"] for a in e["animals"] if a["key"] not in long.ALL]
assert not bad, bad
p = json.load(open(planf))
order = [x["file"].split("/")[1][:-4] for x in sorted(p, key=lambda x: (x["date"], x["time"]))]
sh = [i for i in order if i in ids]; ep = [i for i in order if i not in ids]
lines = [f"{ch} {sub} {' '.join(sh[i:i+8])}" for i in range(0, len(sh), 8)] + [f"{ch} {sub} {' '.join(ep[i:i+2])}" for i in range(0, len(ep), 2)]
open("queue.txt", "a").write("\n".join(lines) + "\n"); print(len(s), "shorts,", len(ep), "eps queued")
