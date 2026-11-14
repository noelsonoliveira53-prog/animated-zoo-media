"""Review gate (Noelson, Nov 14, 2026: "activate YouTube skills on the workflow to revise and create a better version
every time"). Every episode is checked against the youtube-network-channels rulebook BEFORE it is uploaded, and every
review ends with one concrete improvement that the next episode must apply.

  python3 review.py <plan file name, e.g. zoo3d_ep14.mp4> [--job jobs/<id>.json] [--note "next time: ..."]
      -> prints PASS / FAIL with reasons, writes a 12-frame contact sheet to finished/review_<id>.png (LOOK at it:
         characters on-model, nothing scary, text readable, scenes really change), and appends a row to docs/REVIEW_LOG.md.
  python3 review.py --improve "what to do better" [--why "number or observation"]   -> adds a note to docs/IMPROVE.md
  python3 review.py --brief        -> the latest improvement notes (read these before writing any new song or lesson)

Upload only on PASS. A FAIL is fixed (re-title, re-cut, re-render) or the episode is held; never upload around it.
"""
import json, os, re, subprocess, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
BANNED = ["cocomelon", "bluey", "peppa", "paw patrol", "disney", "pixar", "pokemon", "minecraft", "spiderman", "spider-man", "elsa", "mickey",
          "sesame", "blippi", "ms rachel", "baby shark", "pinkfong", "you won't believe", "gone wrong", "scary", "died", "blood", "kill"]
DISTRESS = ["lost", "cry", "cries", "crying", "scared", "afraid", "hurt", "trapped", "stuck", "danger", "dangerous", "alone", "help me",
            "bite", "bites", "attack", "hunt", "hunts", "dead", "die", "sad", "tears", "monster", "fight"]
CTA = ["subscribe", "like this video", "hit the bell", "smash", "comment below", "click"]
RANGE = {"3d_singalong": (120, 200), "3d_singalong_vids_hook": (120, 200), "vids_full": (120, 200), "3d_lesson": (270, 390), "3d_short_cut": (15, 60)}
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d

def note(text, why=""):
    p = os.path.join(REPO, "docs", "IMPROVE.md")
    if not os.path.exists(p):
        open(p, "w").write("# Improvement notes (newest last)\nEvery review and every views check adds one concrete thing to do better. "
                           "Before writing a new song or lesson, read the last 8 notes (`python3 studio/zoo3d/review.py --brief`) and apply them; "
                           "say in the spec's `improves` field which ones were applied.\n\n")
    open(p, "a").write(f"- {datetime.date.today()}: {text}" + (f" (why: {why})" if why else "") + "\n")

def brief(n=8):
    p = os.path.join(REPO, "docs", "IMPROVE.md")
    ls = [l for l in open(p).read().split("\n") if l.startswith("- ")] if os.path.exists(p) else []
    print("\n".join(ls[-n:]) or "no notes yet")

def probe(path):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", path], capture_output=True, text=True).stdout
    j = json.loads(o); return j["streams"][0]["width"], j["streams"][0]["height"], float(j["format"]["duration"])

def review(fname):
    plans = [("studio/upload_plan_3d.json", "ep"), ("studio/upload_plan_shorts_zoo.json", "short")]
    entry = allp = None
    for pp, _ in plans:
        d = json.load(open(os.path.join(REPO, pp))); L = d if isinstance(d, list) else next(v for v in d.values() if isinstance(v, list))
        for e in L:
            if e.get("file") == fname: entry, allp = e, L
    if not entry: sys.exit(f"{fname} is not in an upload plan")
    fails, warns = [], []
    title, desc, fmt = entry["title"], entry.get("description", ""), entry.get("format", "3d_singalong")
    low = (title + " " + desc).lower()
    # META-01/02/03
    if len(title) > 60: fails.append(f"title is {len(title)} characters (max 60)")
    caps = [w for w in re.findall(r"[A-Za-z']+", title) if w.isupper() and len(w) > 3]
    if len(caps) > 1: fails.append(f"more than one ALL-CAPS word in the title: {caps}")
    for b in BANNED:
        if re.search(r"\b" + re.escape(b) + r"\b", low): fails.append(f"banned word in title/description: {b}")
    # WORD SYNC (Noelson Nov 14: "all words in sync"): v2 lessons carry the forced-alignment result
    if os.path.exists(os.path.join(HERE, "songs", os.path.splitext(os.path.basename(fname))[0] + ".json")):
        _sy = json.load(open(os.path.join(HERE, "songs", os.path.splitext(os.path.basename(fname))[0] + ".json")))
        if _sy.get("lesson_version") == 2:
            sy = _sy.get("sync") or {}
            if not sy: fails.append("lesson has no word-sync record: rebuild it with teach.py (wordsync)")
            elif sy.get("aligned", 0) < sy.get("words", 1): fails.append(f"word sync: only {sy.get('aligned')}/{sy.get('words')} words were placed from the audio")
            if sy.get("suspect_words"): fails.append(f"the voice may have mispronounced: {sy['suspect_words'][:3]}")
    # PACKAGING (yt-package; Noelson Nov 14: "personalized thumbnails are being applied to all videos upon posting")
    th = entry.get("thumb"); tpath = os.path.join(REPO, th) if th else None
    if not tpath or not os.path.exists(tpath): fails.append("no custom thumbnail file for this video (plan 'thumb'): make one before uploading (finish.py / lesson_shorts.py / short_thumb.py)")
    else:
        if os.path.getsize(tpath) > 2e6: fails.append("thumbnail is over 2 MB (YouTube's limit)")
        if any(e is not entry and e.get("thumb") == th and e.get("status") != "dropped" for e in allp): fails.append("this thumbnail file is used by another video: every video gets its own")
    _sj = os.path.join(HERE, "songs", os.path.splitext(os.path.basename(fname))[0] + ".json")
    tt = entry.get("thumb_text") or (json.load(open(_sj)).get("meta", {}).get("thumb_text", "") if os.path.exists(_sj) else "")
    if tt:
        tw = re.findall(r"[A-Za-z0-9']+", tt.lower()); stop = {"the", "a", "an", "is", "or", "and", "to", "of", "in", "it", "so", "no", "too", "can"}
        if len(tw) > 3: fails.append(f"thumbnail text has {len(tw)} words (max 3): '{tt}'")
        rep = [w for w in tw if w not in stop and w in re.findall(r"[a-z0-9']+", title.lower())]
        if rep: warns.append(f"thumbnail text repeats the title's words {rep}: the thumbnail should add a hook, not say the title again")
    same = [e for e in allp if e is not entry and e["title"].strip().lower() == title.strip().lower() and e.get("status") != "dropped"]
    if same: fails.append("title repeats another video on this channel (META-02)")
    if "AI tools" not in desc or "reviewed for kid safety" not in desc: fails.append("description is missing the AI-disclosure boilerplate (META-03)")
    first2 = desc.split("\n")[:2]
    if len(" ".join(first2)) < 80: warns.append("first 2 description lines are short; make them searchable")
    # KID-01
    if entry.get("made_for_kids") is not True and "short" not in fmt: fails.append("made_for_kids is not true (KID-01)")
    # file checks
    path = os.path.join(REPO, fname)
    if not os.path.exists(path): fails.append("video file is missing")
    else:
        w, h, dur = probe(path); lo, hi = RANGE.get(fmt, (15, 400))
        if "short" not in fmt and (w, h) != (3840, 2160): fails.append(f"video is {w}x{h}, expected 3840x2160")
        if os.path.getsize(path) >= 100e6: fails.append("file is over 100 MB")
        au = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_name", "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
        if not au: fails.append("video has NO SOUND (no audio stream)")
        else:
            vol = subprocess.run(["ffmpeg", "-v", "info", "-t", "60", "-i", path, "-vn", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
            m = re.search(r"mean_volume: (-?[0-9.]+)", vol)
            if m and float(m.group(1)) < -45: fails.append(f"audio is almost silent (mean {m.group(1)} dB)")
        if not lo <= dur <= hi: fails.append(f"length {dur:.0f} s is outside {lo}-{hi} s for {fmt} (KID-04)")
        os.makedirs(os.path.join(HERE, "finished"), exist_ok=True)
        sheet = os.path.join(HERE, "finished", "review_" + os.path.splitext(os.path.basename(fname))[0] + ".png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-vf", f"fps=12/{dur:.2f},scale=480:-1,tile=4x3", "-frames:v", "1", sheet])
        print("contact sheet:", sheet, "(look at it before uploading, next to docs/quality_baseline/*.png: it must be at least that good)")
    # script / lyrics: KID-02, KID-03, no calls to action aimed at kids
    sid = os.path.splitext(os.path.basename(fname))[0].rstrip("h") if fname.endswith("h.mp4") else os.path.splitext(os.path.basename(fname))[0]
    sp = os.path.join(HERE, "songs", sid + ".json"); text = ""
    if os.path.exists(sp):
        s = json.load(open(sp)); text = (s.get("lyrics", "") + "\n" + s.get("script", "")).lower()
        for wd in DISTRESS:
            if re.search(r"\b" + re.escape(wd) + r"\b", text): warns.append(f"word to check for distress/danger (KID-03): '{wd}'")
        for wd in CTA:
            if wd in text or wd in desc.lower().split("lyrics")[0]: fails.append(f"call to action aimed at kids: '{wd}'")
    elif "short" not in fmt: warns.append("no song/lesson spec found to check the words")
    # variety + scene plan
    jp = arg("--job")
    if jp:
        import variety
        job = json.load(open(jp)); n = len(job.get("locations", []))
        if n < 8: (warns if job.get("pre_scene_plan") else fails).append(f"only {n} scenes in the scene plan (need 8+; run routes.py)")
        led = variety.load()
        _ids = {job["id"], job.get("song", job["id"])}   # re-renders (w/x/a4k ids) share the original episode's ledger entry
        if not any(e["id"] in _ids for e in led): fails.append("episode is not recorded in the variety ledger")
    elif "short" not in fmt and "vids" not in fmt: warns.append("no --job given: scene plan and variety were not checked")
    ok = not fails
    print(("PASS" if ok else "FAIL"), fname)
    for f in fails: print("  FAIL:", f)
    for w_ in warns: print("  check:", w_)
    lp = os.path.join(REPO, "docs", "REVIEW_LOG.md")
    if not os.path.exists(lp): open(lp, "w").write("# Review log (rulebook gate before every upload)\n\n| Date | File | Format | Result | Fails | To check | Improvement for next time |\n|---|---|---|---|---|---|---|\n")
    nt = arg("--note", "")
    open(lp, "a").write(f"| {datetime.date.today()} | {fname} | {fmt} | {'PASS' if ok else 'FAIL'} | {'; '.join(fails) or '-'} | {'; '.join(warns) or '-'} | {nt or '-'} |\n")
    if nt: note(nt, f"review of {fname}")
    return ok

if __name__ == "__main__":
    if "--brief" in sys.argv: brief(); sys.exit(0)
    if "--improve" in sys.argv: note(arg("--improve"), arg("--why", "")); print("noted"); sys.exit(0)
    sys.exit(0 if review(sys.argv[1]) else 1)
