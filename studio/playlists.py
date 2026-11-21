#!/usr/bin/env python3
"""Which playlists does a video of The Animated Zoo belong in? (owner, Nov 20 2026: "Start to create playlist on YouTube and organizing the channel better")

    python3 studio/playlists.py <plan file name, e.g. cartoon/za_ep09.mp4>   the playlists this video goes into (titles, as Studio's dialog lists them)
    python3 studio/playlists.py --todo                                       videos that are on YouTube (video_id) and have no "playlists" recorded yet
    python3 studio/playlists.py --done <plan file name>                      record it in the plan AFTER Studio said "Playlists edited"
    python3 studio/playlists.py --audit                                      how many recorded videos each playlist holds (compare with Studio's playlist list)

The rules are in studio/playlists.json: a format decides the series playlists, the TITLE decides the topic playlists (`match`), `also` lists the exceptions.
Only The Animated Zoo: Gizmo Explains and the other channels have no playlists here. How to add in Studio, and the duplicate trap: docs/PLAYLISTS.md."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = json.load(open(os.path.join(HERE, "playlists.json")))
PLANS = ["upload_plan_3d.json", "upload_plan_shorts_zoo.json"]
ZOO_FORMATS = set(CONF["long_formats"]) | set(CONF["short_formats"])


def is_zoo(e, plan_name=""):
    """upload_plan_shorts_zoo.json is The Animated Zoo's alone. In upload_plan_3d.json its files sit in the repo root or in cartoon/; every other channel has its own folder."""
    f = e.get("file", "")
    if e.get("format") not in ZOO_FORMATS or e.get("channel", "animated-zoo") != "animated-zoo": return False
    return plan_name == "upload_plan_shorts_zoo.json" or "/" not in f or f.startswith("cartoon/")


def playlists_for(e):
    """The keys of the playlists this plan entry belongs in."""
    fmt = e.get("format"); title = e.get("title", ""); long_ = fmt in CONF["long_formats"]; out = []
    for p in CONF["playlists"]:
        if fmt in p.get("formats", []): out.append(p["key"]); continue
        if p.get("long_only") and not long_: continue
        if (p.get("match") and re.search(p["match"], title, re.I)) or e.get("file") in p.get("also", []): out.append(p["key"])
    return out


def entries():
    for name in PLANS:
        path = os.path.join(HERE, name); raw = open(path).read(); plan = json.loads(raw)
        for e in plan:
            if is_zoo(e, name): yield name, path, raw, plan, e


def title_of(key):
    return next(p["title"] for p in CONF["playlists"] if p["key"] == key)


def save(path, raw, plan):
    out = json.dumps(plan, indent=1, ensure_ascii="\\u" in raw)
    open(path, "w").write(out + ("\n" if raw.endswith("\n") else ""))


def live(e):
    return bool(e.get("video_id")) and e.get("status") in ("scheduled", "published", "public")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(0)
    if a[0] == "--todo":
        n = 0
        for name, path, raw, plan, e in entries():
            if live(e) and e.get("playlists") != playlists_for(e):
                n += 1; print(f"{e['file']}  {e['video_id']}  {e['title'][:50]}\n    add to: " + " | ".join(title_of(k) for k in playlists_for(e) if k not in (e.get("playlists") or [])))
        print(f"{n} video(s) to add to playlists" if n else "every live video has its playlists recorded"); sys.exit(1 if n else 0)
    if a[0] == "--audit":
        cnt = {p["key"]: 0 for p in CONF["playlists"]}; seen = set()
        for name, path, raw, plan, e in entries():
            if live(e) and e["video_id"] not in seen:
                seen.add(e["video_id"])
                for k in e.get("playlists") or []: cnt[k] += 1
        for p in CONF["playlists"]: print(f"{cnt[p['key']]:4d}  {p['title']}  ({p['id']})")
        print("recorded in the plans only: videos uploaded before the plans existed are on YouTube and not counted here"); sys.exit(0)
    done = a[0] == "--done"; want = a[1] if done else a[0]; hit = None
    for name, path, raw, plan, e in entries():
        if e.get("file") == want or os.path.basename(e.get("file", "")) == want:
            hit = e; keys = playlists_for(e)
            if done: e["playlists"] = keys; save(path, raw, plan)
            break
    if not hit: print(want, "is not a video of The Animated Zoo in an upload plan"); sys.exit(1)
    print(f"{hit['file']}  \"{hit['title']}\"" + ("  recorded" if done else ""))
    for k in keys: print("   ", title_of(k))
