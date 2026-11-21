"""studio_table_<date>.txt (rows read from YouTube Studio's Advanced mode) -> channel_<date>.json, with every video sorted into a kind."""
import re, json, sys
src = sys.argv[1]; TOTAL_V, TOTAL_L, TOTAL_S = 32766, 254, 75
CARTOON_EXPL = ("Amazing Animal Bodies", "Savanna Animals", "Treetop Animals", "Ocean & Ice", "Dinosaurs for Kids", "Desert Animals", "Baby Animals for Kids", "Backyard Bugs")
EXPL_3D = ("Who Am I?", "Yes or No?", "Forest Animals for Kids", "Animal Champions")
LEGACY = ("Ultimate Toddler", "Sing, Dance, Giggle", "Finny", "Zoo Animals for Kids! Meet 10")
def sec(t): m, s = t.split(":"); return int(m) * 60 + int(s)
def split(v, total):          # "4,91315.0%" -> 4913 (views and share are glued together in the table cell)
    if "—" in v: return None
    v = v.strip()
    for k in range(1, len(v)):
        a, b = v[:k], v[k:]
        if re.fullmatch(r"[\d,]+", a) and re.fullmatch(r"\d+\.\d%", b):
            n = int(a.replace(",", ""))
            if abs(n / total * 100 - float(b[:-1])) < 0.06: return n
    return None
def hours(v):
    m = re.match(r"(\d+\.\d)", v); return float(m.group(1)) if m else None
rows = []
for line in open(src):
    if line.startswith("#") or not line.strip(): continue
    c = [x.strip() for x in line.split(" | ")]
    d, title = c[0], c[1]; D = sec(d)
    kind = ("legacy" if title.startswith(LEGACY) or any(k in title for k in LEGACY) else "cartoon_explainer" if title.startswith(CARTOON_EXPL) else "explainer_3d" if title.startswith(EXPL_3D)
            else "song_3d" if D > 60 else "song_cut_short" if ("with Milo" in title or "Peekaboo" in title) else "cartoon_fact_short")
    rows.append({"title": title, "seconds": D, "kind": kind, "views": split(c[2], TOTAL_V), "watch_hours": hours(c[3]),
                 "impressions": int(c[4].replace(",", "")) if c[4] not in ("—", "") else None, "ctr": None if c[5] == "—" else float(c[5].rstrip("%")),
                 "avg_view_s": None if c[6] == "—" else sec(c[6]), "pct_viewed": None if c[7] == "—" else float(c[7].rstrip("%")),
                 "likes": split(c[8], TOTAL_L), "subs": split(c[9], TOTAL_S)})
bad = [r["title"] for r in rows if r["views"] is None]
agg = {}
for r in rows:
    a = agg.setdefault(r["kind"], {"videos": 0, "views": 0, "watch_hours": 0, "impressions": 0, "clicks": 0, "subs": 0, "likes": 0})
    a["videos"] += 1; a["views"] += r["views"] or 0; a["watch_hours"] += r["watch_hours"] or 0; a["impressions"] += r["impressions"] or 0
    a["clicks"] += (r["impressions"] or 0) * (r["ctr"] or 0) / 100; a["subs"] += r["subs"] or 0; a["likes"] += r["likes"] or 0
for k, a in agg.items():
    a["watch_hours"] = round(a["watch_hours"], 1); a["ctr"] = round(a["clicks"] / a["impressions"] * 100, 2) if a["impressions"] else None; a["clicks"] = round(a["clicks"])
    a["avg_view_s"] = round(a["watch_hours"] * 3600 / a["views"], 1) if a["views"] else None; a["views_per_video"] = round(a["views"] / a["videos"])
    vs = sorted(r["views"] or 0 for r in rows if r["kind"] == k); a["median_views"] = vs[len(vs) // 2]
json.dump({"read": "2026-11-16 12:15 PM ET, YouTube Studio Advanced mode, lifetime", "rows": rows, "by_kind": agg}, open(src.replace("studio_table_", "channel_").replace(".txt", ".json"), "w"), indent=1)
print("rows", len(rows), "unparsed views:", bad)
for k, a in sorted(agg.items(), key=lambda x: -x[1]["views"]): print(f"{k:20s}", a)
