"""Build Command Center db writes from the upload plans + rendered MP4s + render queue.
Usage: python3 hq_sync.py <versions.json>   -> writes hq/batch_N.json (ArtifactData batch entries) and hq/ops.json"""
import json, glob, os, sys, re, datetime
Z = "/root/zoo"; R = "/home/claude/animated-zoo-media"
CH = {"truck": "tiny-truck-town", "bloop": "bloops-color-lab", "fruity": "fruity-friends", "moon": "moonbeam-bedtime", "gizmo": "gizmo-explains"}
ver = json.load(open(sys.argv[1]))  # {doc_id: {"version": n, "status": s}}
shorts = set()
for f in glob.glob(f"{Z}/shorts_*.json"):
    shorts |= {s["id"] for s in json.load(open(f))}
writes = []
for f in sorted(glob.glob(f"{Z}/upload_plan_*.json")):
    if f.endswith("/upload_plan.json"): continue
    for it in json.load(open(f)):
        sub, fn = it["file"].split("/"); vid = fn[:-4]
        if sub not in CH: continue
        doc = vid.replace("_", "-")
        m = re.match(r"tt_ep(\d\d)_", vid)
        if m and f"tt-ep{m.group(1)}" in ver: doc = f"tt-ep{m.group(1)}"
        rendered = os.path.exists(f"{R}/{sub}/{fn}")
        cur = ver.get(doc, {})
        status = cur.get("status") if cur.get("status") in ("scheduled", "public") else ("scheduled" if it.get("status") == "scheduled" else ("ready" if rendered else "rendering"))
        data = {"channel": CH[sub], "date": it["date"], "time": it["time"], "title": it["title"], "kind": "short" if vid in shorts else "episode", "status": status}
        if doc in ver:
            writes.append({"op": "update", "collection": "videos", "doc_id": doc, "data": data, "if_version": ver[doc]["version"]})
        else:
            data.update({"url": "", "notes": ""}); writes.append({"op": "set", "collection": "videos", "doc_id": doc, "data": data})
os.makedirs(f"{Z}/hq", exist_ok=True)
for i in range(0, len(writes), 50):
    json.dump(writes[i:i+50], open(f"{Z}/hq/batch_{i//50}.json", "w"))
q = [l.split() for l in open(f"{Z}/queue.txt") if l.strip()]
log = open(f"{Z}/night_q.log").read().splitlines() if os.path.exists(f"{Z}/night_q.log") else []
cur = next((l for l in reversed(log) if l.startswith("CHUNK_START")), "")
done = next((l for l in reversed(log) if l.startswith("CHUNK_DONE")), "")
last = next((l for l in reversed(log) if l.startswith("PUSHED")), "")
running = cur and (not done or log.index(cur) > log.index(done))
now = datetime.datetime.now()
ops = {"uploads": {"count": 0, "cap": 15, "note": "YouTube's account-wide daily limit was reached Nov 3 at about 1:20 PM ET. The 5:47 AM run on Nov 4 posts the Nov 4 videos first."},
       "queue": {"current": (" ".join(cur.split()[1:-1]) if running else "Idle"), "chunksLeft": len(q), "itemsLeft": sum(len(x) - 2 for x in q), "last": " ".join(last.split()[1:]) if last else "—"},
       "alerts": [{"level": "critical", "title": "Uploads paused until tomorrow", "body": "YouTube's daily upload limit for the account was reached. Nothing more can be scheduled until the 24-hour window rolls over (around 6 AM ET)."},
                  {"level": "warn", "title": "Verify channels to lift the cap", "body": "Phone-verify channels at youtube.com/verify (2 channels per phone number per year). Verified channels can upload more and use custom thumbnails."}],
       "updatedLabel": now.strftime("%b %-d, %-I:%M %p ET")}
json.dump(ops, open(f"{Z}/hq/ops.json", "w"))
from collections import Counter
print(len(writes), "writes;", Counter(w["data"]["status"] for w in writes), "| queue:", ops["queue"])
