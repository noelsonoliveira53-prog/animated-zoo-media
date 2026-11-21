"""Upload guard (owner, Nov 17 2026: "create a process to check if the video is already uploaded and not upload twice").

One LIVE video per file, per title and per slot. Run it before every upload, and the whole-plan audit at the start of every run.

  python3 studio/upload_guard.py <plan file name>                  may this file be uploaded now?   exit 0 = yes
  python3 studio/upload_guard.py <plan file name> --replace <id>   a FIX of a video that is already up (the owner said it is wrong, or a defect was found):
                                                                   allowed only when <id> is the entry's own live id. After the upload: old one Private,
                                                                   renamed "OLD (replaced): <title>", id moved to "replaced_video_ids", new id recorded.
  python3 studio/upload_guard.py --audit                           every plan entry: two live ids on one title, one slot or one file; entries that say
                                                                   to_upload but already carry an id; long videos on one topic
  python3 studio/upload_guard.py --next lesson|adventure           the next cartoon to build: first title of docs/cartoon/build_plan.py THEMES that has no
                                                                   plan entry, the next free id, and the first free slots (video and, for a lesson, 3 Shorts)

What it cannot see: Studio itself. So the second half of the check is in the browser, on the content list, before a file is armed:
`zlive("<title>")` from studio/studio-upload2.js must give live = [] (or [the id being replaced]); rows_read = 0 means the list was not read.
After the upload it must give exactly one live id for the title.

"Live" = a plan entry with a video_id whose status is scheduled or published. Private, rejected, dropped and paused entries are not live.

2D ONLY (owner, Nov 20 2026 11:13 PM: "Let's keep just 2d cartons on the channel suspend all 3d uploads of songs and fill the spaces with the same carton
model we have"): on The Animated Zoo no 3D file is uploaded any more, song, lesson or Short (every upload and every --replace of one is REFUSED), and the
3:30 PM slot that was the song's is an adventure slot. 3D videos that were scheduled and not public yet carry "hold_2d_only" (Private in Studio, not deleted).
Gizmo Explains (--channel gizmo) is another channel and is not touched by this."""
import json, os, re, sys, ast, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
PLANS = ["upload_plan_3d.json", "upload_plan_shorts_zoo.json"]
if "--channel" in sys.argv and sys.argv[sys.argv.index("--channel") + 1] == "gizmo":      # Gizmo Explains (owner, Nov 19 2026): its own plan; every check is per channel
    PLANS = ["upload_plan_gizmo_v3.json"]; sys.argv[sys.argv.index("--channel"):sys.argv.index("--channel") + 2] = []
LIVE = ("scheduled", "published", "public")
NEVER = ("hold_review", "hold_fix", "hold_fact_check", "hold_3d_cap", "hold_2d_only", "in_production", "paused_channel", "rendering_variety", "rejected", "dropped", "private", "spare_song_cut")
ZOO_3D = ("3d_singalong", "3d_singalong_vids_hook", "vids_full", "3d_lesson", "3d_lesson_v3", "3d_short_cut", "3d_short_test", "lesson_fact_short_90", "lesson_fact_short_4k")      # The Animated Zoo is 2D only since Nov 20 2026 11:13 PM
GIZMO = PLANS == ["upload_plan_gizmo_v3.json"]
STOP = set("a an the and or of to in on at for with by from is are do does did can what why how who whose where when which this that it its his her "
           "kids kid milo song songs story stories fun facts fact video learn animal animals baby little big all day".split())
SLOTS = {"adventure": ["5:30 AM", "1:30 PM", "3:30 PM"], "lesson": ["9:30 AM", "5:30 PM"], "short": ["7:30 AM", "11:30 AM", "7:30 PM"]}      # 3:30 PM was the 3D song's slot until Nov 20 2026; three adventure builds a day fill the three adventure slots


def load():
    out = []
    for p in PLANS:
        for e in json.load(open(os.path.join(HERE, p))): e["_plan"] = p; out.append(e)
    return out


def norm(t): return re.sub(r"\s+", " ", re.sub(r"^old \(replaced\): ", "", (t or "").strip().lower()))
def live(e): return bool(e.get("video_id")) and e.get("status") in LIVE
def is_short(e): return "short" in e["_plan"] or "short" in (e.get("format") or "")
def is_talk(e): return (e.get("format") or "") in ("3d_lesson", "3d_lesson_v3", "cartoon_lesson", "cartoon_adventure", "gizmo_explainer")      # lessons, stories and Gizmo explainers: a topic is told once (a song on the same animal is not a repeat)
def today(): return datetime.datetime.now(__import__("zoneinfo").ZoneInfo("America/New_York")).date()


def words(t):
    w = [re.sub(r"'s$", "", x) for x in re.findall(r"[a-z']+", norm(t))]
    return {re.sub(r"s$", "", x) for x in w if x not in STOP and len(x) > 2}


def same_topic(a, b):
    """Two long videos on one topic: most of the shorter title's own words are in the other one (camel hump inside / camel hump inside)."""
    x, y = words(a), words(b)
    if len(x) < 2 or len(y) < 2: return False
    return len(x & y) / min(len(x), len(y)) >= 0.75 and len(x & y) >= 2


def uploads_24h():
    try:
        log = subprocess.run(["git", "-C", REPO, "log", "--since=24 hours ago", "--format=%s"], capture_output=True, text=True).stdout
        by_msg = sum(len(set(re.findall(r"\(([\w-]{11})[),;]", ln))) for ln in log.splitlines() if re.search(r"scheduled|uploads|re-uploaded", ln, re.I) and not ln.startswith("Merge"))
        # Nov 18: a commit whose message does not say "scheduled" can still record uploads (the Nov 17 morning five sat in a
        # "Four new lessons" commit). Also count the video ids ADDED to the plans in the last 24 hours; take the larger number.
        cut = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24); base = ""
        for ln in subprocess.run(["git", "-C", REPO, "log", "--first-parent", "-400", "--format=%H %aI"], capture_output=True, text=True).stdout.splitlines():
            h, d = ln.split(" ", 1)
            if datetime.datetime.fromisoformat(d) < cut: base = h; break
        ids = lambda txt: set(re.findall(r'"video_id": "([\w-]{11})"', txt))
        added = set(); removed = set()
        for f in ("studio/upload_plan_3d.json", "studio/upload_plan_shorts_zoo.json"):
            old_t = subprocess.run(["git", "-C", REPO, "show", f"{base}:{f}"], capture_output=True, text=True).stdout if base else ""
            if not base: continue
            diff = subprocess.run(["git", "-C", REPO, "log", "-p", "--format=", f"{base}..HEAD", "--", f], capture_output=True, text=True).stdout
            added |= set(re.findall(r'^\+\s*"video_id": "([\w-]{11})"', diff, re.M)) - ids(old_t)   # every id written since, also ids later replaced and deleted
        if not base: print("   NOTE: no commit older than 24 hours in this clone (shallow): run git fetch --deepen=60, the count below is the commit-message count only", file=sys.stderr)
        return max(by_msg, len(added))
    except Exception: return None


def check(name, replace=None, same_topic_ok=None):
    es = load(); mine = [e for e in es if e["file"] == name or os.path.basename(e["file"]) == os.path.basename(name)]
    fails, notes = [], []
    if not mine: return [f"{name}: no plan entry (a video is uploaded only from its plan entry)"], notes
    if len(mine) > 1: fails.append(f"{name}: {len(mine)} plan entries for one file")
    e = mine[0]; st = e.get("status"); vid = e.get("video_id"); title = e.get("title") or ""
    if not title: fails.append("the entry has no title")
    if st in NEVER: fails.append(f'status "{st}" is never uploaded')
    if not GIZMO and (e.get("format") or "") in ZOO_3D: fails.append(f'2D ONLY (owner, Nov 20 2026 11:13 PM): "{e.get("format")}" is a 3D format; no 3D video is uploaded to The Animated Zoo, not as a fix either')
    if replace:
        if vid != replace: fails.append(f"--replace {replace}: the entry's live id is {vid}; a replacement names the id it replaces")
        if not os.path.exists(os.path.join(REPO, e["file"])): fails.append(f'{e["file"]} is not in the repo')
        notes.append(f'REPLACEMENT of {replace} on its slot {e.get("date")} {e.get("time")}: upload, then set {replace} Private and rename it "OLD (replaced): {title}", '
                     f'move the id to "replaced_video_ids", record the new id; the content list must then show ONE live row for this title')
    else:
        if vid and st in LIVE: fails.append(f"ALREADY UPLOADED: {vid} ({st} {e.get('date')} {e.get('time')}). A second upload of this file is only a fix: --replace {vid}")
        elif vid: fails.append(f'the entry carries video_id {vid} with status "{st}": find out what that upload is before uploading again')
        if st != "to_upload" and st not in LIVE and st not in NEVER: fails.append(f'status "{st}": only "to_upload" entries are uploaded')
    for o in es:
        if o is e or not live(o): continue
        if norm(o.get("title")) == norm(title) and title: fails.append(f'SAME TITLE is live: {o["file"]} {o["video_id"]} ({o.get("date")} {o.get("time")})')
        elif o.get("date") and o.get("date") == e.get("date") and o.get("time") == e.get("time") and is_short(o) == is_short(e):
            fails.append(f'SLOT {e.get("date")} {e.get("time")} already holds a live video: {o["file"]} {o["video_id"]}')
        elif is_talk(e) and is_talk(o) and same_topic(title, o.get("title")):
            m = f'SAME TOPIC as a live video: "{o.get("title")}" ({o["file"]} {o["video_id"]})'
            (notes if same_topic_ok else fails).append(m + (f"; allowed: {same_topic_ok}" if same_topic_ok else '; a different video on the topic needs --same-topic-ok "<why it is not a repeat>"'))
    m = re.match(r"(.*/)?((?:zc|za)_ep\d+)_short\d+\.mp4$", e["file"])      # a Short of a lesson that repeats a live lesson's topic repeats it too
    if m:
        par = [o for o in es if os.path.basename(o["file"]) == m.group(2) + ".mp4"]
        for o in es:
            if par and o is not par[0] and live(o) and is_talk(o) and same_topic(par[0].get("title"), o.get("title")) and not par[0].get("same_topic_ok"):
                fails.append(f'its lesson {par[0]["file"]} ("{par[0].get("title")}") is on the SAME TOPIC as the live "{o.get("title")}" ({o["video_id"]}): the Shorts are held with it')
    n = uploads_24h()
    if n is not None: notes.append(f"uploads in the last 24 hours by the commit log: {n} of 20" + (" (count again in Studio if this is 20 or more)" if n >= 20 else ""))
    notes.append(f'In Studio, on the content list, before arming the file: zlive({json.dumps(title)}) must give live = {json.dumps([replace] if replace else [])}')
    return fails, notes


def audit():
    es = load(); fails = []; lv = [e for e in es if live(e)]
    for i, a in enumerate(lv):
        for b in lv[i + 1:]:
            if norm(a.get("title")) == norm(b.get("title")): fails.append(f'two live videos with one title: {a["file"]} {a["video_id"]} / {b["file"]} {b["video_id"]}')
            elif a.get("date") and a.get("date") == b.get("date") and a.get("time") == b.get("time") and is_short(a) == is_short(b):
                fails.append(f'two live videos on one slot {a["date"]} {a["time"]}: {a["file"]} {a["video_id"]} / {b["file"]} {b["video_id"]}')
            elif a["video_id"] == b["video_id"]: fails.append(f'one video id on two entries: {a["video_id"]} {a["file"]} / {b["file"]}')
    seen = {}
    for e in es:
        if e["file"] in seen: fails.append(f'two plan entries for {e["file"]}')
        seen[e["file"]] = 1
        if e.get("video_id") and e.get("status") == "to_upload": fails.append(f'{e["file"]} says to_upload but carries {e["video_id"]}')
        if not GIZMO and (e.get("format") or "") in ZOO_3D and e.get("status") in ("to_upload", "in_production"): fails.append(f'{e["file"]} is 3D ({e.get("format")}) and "{e.get("status")}": The Animated Zoo is 2D only, set it "hold_2d_only"')
    lg = [e for e in es if is_talk(e) and e.get("status") in LIVE + ("to_upload", "in_production") and e.get("title")]
    topics = [f'{a["file"]} ({a.get("status")}) / {b["file"]} ({b.get("status")}): "{a["title"]}" / "{b["title"]}"' for i, a in enumerate(lg) for b in lg[i + 1:]
              if norm(a["title"]) != norm(b["title"]) and same_topic(a["title"], b["title"]) and not (a.get("same_topic_ok") or b.get("same_topic_ok"))]
    return fails, topics, len(lv)


def themes():
    src = open(os.path.join(REPO, "docs/cartoon/build_plan.py")).read(); tree = ast.parse(src)
    node = [n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "THEMES"][0]
    ns = {}; exec(compile(ast.Module([node], []), "themes", "exec"), ns); return ns["THEMES"]


ANIMALS = set("lion elephant giraffe zebra hippo tiger bear panda monkey fox koala horse pig cow rhino camel octopus penguin flamingo meerkat snail ant "
              "owl frog tapir bat crab anteater macaw eagle dinosaur rex shark whale dolphin turtle sloth kangaroo seal duck chicken sheep goat rabbit".split())
NAMES = {"mango": "monkey", "tumble": "elephant", "sandy": "camel", "jungle": "rainforest", "rainforest": "rainforest", "dino": "dinosaur"}


def animals(t):
    """The animals (and the rainforest topic) a title is about: Mango in the title = monkey, Tumble = elephant (owner's rule: never two uploads on one animal or topic in a day)."""
    w = {re.sub(r"'s$", "", x) for x in re.findall(r"[a-z']+", norm(t))}; w |= {re.sub(r"s$", "", x) for x in w}
    a = {NAMES.get(x, x) for x in w if x in ANIMALS or x in NAMES}
    try: fr = {norm(i[0]): th["friend"] for th in themes() for k in ("adv", "les") for i in th.get(k, [])}
    except Exception: fr = {}
    if norm(t) in fr and fr[norm(t)] != t: a |= animals(fr[norm(t)])     # a THEMES title counts its friend (za_ep08 "The Long Walk to the Oasis" = Sandy = camel, Nov 20)
    return a


def free_slots(es, kind, n, start, title=None, avoid_days=()):
    """Free slots of a kind from start on. With a title: skip days that already carry an upload on the same animal/topic, and give each slot its own day
    (three Shorts of one lesson never share a day, and never the lesson's own day: avoid_days)."""
    taken = {(e.get("date"), e.get("time")) for e in es if e.get("date") and is_short(e) == (kind == "short") and e.get("status") in LIVE + ("to_upload", "in_production")}
    mine = animals(title) if title else set()
    busy = {e.get("date") for e in es if mine and e.get("date") and e.get("status") in LIVE + ("to_upload", "in_production") and animals(e.get("title")) & mine}
    out = []; d = start
    while len(out) < n:
        day = d.isoformat()
        if not (title and (day in busy or day in avoid_days)):
            for t in SLOTS[kind]:
                if (day, t) not in taken and len(out) < n and not (title and any(o["date"] == day for o in out)): out.append({"date": day, "time": t})
        d += datetime.timedelta(days=1)
    return out


def nxt(kind):
    es = load(); have = [x for e in es if e.get("status") not in ("dropped", "rejected") for x in (e.get("title") or "", e.get("theme_title") or "") if x]   # theme_title: the THEMES title a build renamed (viral packaging, za_ep10)
    key = "les" if kind == "lesson" else "adv"; pick = None
    for t in themes():
        for item in t[key]:
            if not any(norm(h) == norm(item[0]) or norm(h).startswith(norm(item[0])) or same_topic(h, item[0]) for h in have): pick = (t, item); break
        if pick: break
    pre = "zc_ep" if kind == "lesson" else "za_ep"
    nums = [int(m.group(1)) for e in es for m in [re.search(pre + r"(\d+)", e["file"])] if m] + [int(m.group(1)) for f in os.listdir(os.path.join(HERE, "cartoon/episodes")) for m in [re.match(pre + r"(\d+)\.py", f)] if m]
    start = today() + datetime.timedelta(days=2)
    ttl = pick[1][0] if pick else None
    out = {"kind": kind, "id": f"{pre}{max(nums + [0]) + 1:02d}", "slot": free_slots(es, kind, 1, start, ttl)[0]}
    if kind == "lesson": out["short_slots"] = free_slots(es, "short", 3, start + datetime.timedelta(days=1), ttl or "", (out["slot"]["date"],))
    if ttl: out["same_day_rule"] = f"slots skip days that already carry {sorted(animals(ttl)) or 'nothing named in the title'}; each Short on its own day, not the lesson's day"
    fmt = "cartoon_lesson" if kind == "lesson" else "cartoon_adventure"; lv = [o for o in es if live(o) and is_talk(o)]
    out["unfinished_first"] = [{"file": e["file"], "title": e.get("title"), "slot": f'{e.get("date")} {e.get("time")}'} for e in es if e.get("format") == fmt and e.get("status") == "in_production"
                               and not any(same_topic(e.get("title"), o.get("title")) for o in lv)]      # finish these before starting a new title (docs/cartoon/runs/<id>.md says where each stopped); a repeat of a live topic is not finished, it is held
    if pick: t, item = pick; out.update(theme=t["name"], friend=t["friend"], place=t["place"], title=item[0], premise=item[1], facts_to_read_today=item[2], thumbnail=item[3])
    else: out["title"] = None; out["note"] = "every THEMES title of this kind has a plan entry: write five new themes into docs/cartoon/build_plan.py first"
    return out


if __name__ == "__main__":
    a = sys.argv[1:]; opt = lambda k: a[a.index(k) + 1] if k in a else None
    if "--audit" in a:
        f, topics, n = audit()
        for x in f: print("FAIL", x)
        for x in topics: print("SAME TOPIC (look, then drop one or mark the entry \"same_topic_ok\": \"why\")", x)
        print(f"audit: {n} live videos in the plans, {len(f)} failures, {len(topics)} topic pairs"); sys.exit(1 if f else 0)
    if "--next" in a: print(json.dumps(nxt(opt("--next")), indent=1, ensure_ascii=False)); sys.exit(0)
    if not a: sys.exit(__doc__)
    f, notes = check(a[0], opt("--replace"), opt("--same-topic-ok"))
    for x in f: print("REFUSED", x)
    for x in notes: print("  ", x)
    print(("DO NOT UPLOAD " if f else "OK TO UPLOAD ") + a[0]); sys.exit(1 if f else 0)
