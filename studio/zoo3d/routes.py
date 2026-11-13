"""Fine scene routes (Nov 13 night: "more change on the scenes"). Turns a job's coarse list of places into a visit
plan where every chorus, each half of every verse and the bridge is its own scene, with its own place, formation and
the animals that part of the song is about.

  from routes import refine;  job["locations"] = refine(job, timing)      (job["locations"] gives the pool of places)
  python3 routes.py jobs/<id>.json      -> rewrites the job in place (needs its timing file) and prints the plan
"""
import json, os, sys, re

def refine(job, timing, verses=None):
    pool = []
    for l in job["locations"]:
        p = (l["biome"], l.get("tod", "golden"))
        if p not in pool: pool.append(p)
    ids = [c["id"] for c in job["cast"][1:]]
    host = job["cast"][0]["id"]
    def mentioned(lines):
        txt = " ".join(l["text"].lower() for l in lines)
        return [i for i in ids if re.search(r"\b" + i.replace("_", " ").lower() + r"s?\b", txt)]
    out = []; k = [0]; forms = ["line", "arc", "v"]; nch = 0; last = None; vi = 0
    def nxt():
        k[0] += 1; p = pool[k[0] % len(pool)]
        if last and (p[0], p[1]) == last and len(pool) > 1: k[0] += 1; p = pool[k[0] % len(pool)]
        return p
    secs = timing["sections"]
    for n, sec in enumerate(secs):
        name = sec["name"]; kind = "".join(ch for ch in name if ch.isalpha())
        end = sec.get("end") or (secs[n + 1]["start"] if n + 1 < len(secs) else timing["duration"])
        lines = [l for l in timing["lines"] if sec["start"] - 0.01 <= l["start"] < end]
        if n == 0:
            p = pool[0]; out.append({"from": name, "biome": p[0], "tod": p[1], "formation": "line"}); nch += kind == "chorus"
        elif kind == "chorus" or kind.endswith("chorus") and kind != "prechorus":
            final = not any("chorus" in s2["name"] and "pre" not in s2["name"] for s2 in secs[n + 1:])
            if final:
                b = pool[0][0]; tod = "golden" if pool[0][1] in ("sunset", "night") else "sunset"
                if job["locations"][0].get("tod") == "night" or b == "night_meadow": tod = pool[0][1]
                p = (b, tod)
            else: p = nxt()
            out.append({"from": name, "biome": p[0], "tod": p[1], "formation": forms[nch % 3], "shot": "reveal" if final else "vista"}); nch += 1
        elif kind == "verse":
            half = max(1, len(lines) // 2)
            who = verses[vi] if verses and vi < len(verses) else None; vi += 1
            a = [who[0]] if who else mentioned(lines[:half]); b = (who[1:] if who else mentioned(lines[half:]))
            a = [x for x in a if x != host]; b = [x for x in b if x != host and x not in a] or [x for x in b if x != host]
            p = nxt(); e = {"from": name, "biome": p[0], "tod": p[1], "formation": "host_left" if a else "duo", "shot": "dolly"}
            if a: e["show"] = a[:2]
            out.append(e)
            if len(lines) >= 4:
                last = p; p = nxt(); e = {"from": name, "line": half, "biome": p[0], "tod": p[1], "formation": "host_right" if b else "duo", "shot": "side"}
                if b: e["show"] = b[:2]
                out.append(e)
        elif kind == "prechorus":
            out.append({"from": name, "biome": last[0], "tod": last[1], "formation": "v", "shot": "low"}); continue
        elif kind == "bridge":
            p = nxt(); out.append({"from": name, "biome": p[0], "tod": p[1], "formation": "arc", "shot": "high"})
        else:   # outro and anything else: stay, everyone together
            out.append({"from": name, "biome": last[0], "tod": last[1], "formation": "line"}); continue
        last = (out[-1]["biome"], out[-1]["tod"])
    return out

if __name__ == "__main__":
    jp = sys.argv[1]; job = json.load(open(jp))
    timing = json.load(open(os.path.join(os.path.dirname(jp), job["timing_file"])))
    job["locations"] = refine(job, timing, job.get("verses")); json.dump(job, open(jp, "w"), indent=1)
    for l in job["locations"]: print(l)
