"""Variety guard for The Animated Zoo (Noelson, Nov 13, 2026): "ensure no videos are the same, even if that is what
YouTube Studio is suggesting, otherwise the channel will be just a repetition of the same images".

Every Zoo episode must look different from the recent ones:
  - its own route of places: job["locations"] (zooworld biomes + time of day), 3-5 places per song, a new place at
    least every ~35 s (the Google Vids principle: each part of the song is a fresh scene);
  - its first place (the thumbnail / first 10 s and the Vids hook) differs from the last 4 episodes' first places;
  - at most half of its places repeat the previous episode's places;
  - its cast: new songs (written from now on) must change at least 2 animals vs the previous episode
    (chars/animal.py ALL_KINDS has 17 animals); songs already written keep their lyric cast.

  python3 variety.py check jobs/<id>.json      -> OK or the reasons it repeats (exit 1)
  python3 variety.py record jobs/<id>.json     -> add it to variety_ledger.json (do this when the spec is final)
  python3 variety.py suggest                    -> least-used biomes, times of day and animals for the next song
"""
import json, os, sys, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "variety_ledger.json")
BIOMES = ["savanna", "jungle", "arctic", "beach", "farm", "desert", "autumn_forest", "spring_meadow", "river", "mountain", "bamboo", "night_meadow"]
TODS = ["morning", "noon", "golden", "sunset", "night"]
KINDS = ["lion", "elephant", "giraffe", "zebra", "hippo", "tiger", "bear", "polar_bear", "panda", "monkey", "fox",
         "arctic_fox", "koala", "horse", "pig", "cow", "rhino"]
# animals that fit each biome (used by suggest; any cast may visit any place in a song, but these read best)
FITS = {"savanna": ["lion", "elephant", "giraffe", "zebra", "hippo", "rhino"], "jungle": ["tiger", "monkey", "elephant", "hippo"],
        "arctic": ["polar_bear", "arctic_fox"], "beach": ["monkey", "hippo", "polar_bear"], "farm": ["pig", "cow", "horse"],
        "desert": ["fox", "lion", "rhino"], "autumn_forest": ["bear", "fox"], "spring_meadow": ["horse", "cow", "pig", "fox"],
        "river": ["hippo", "elephant", "bear"], "mountain": ["bear", "fox", "horse"], "bamboo": ["panda", "tiger", "monkey"],
        "night_meadow": ["fox", "bear", "koala"]}


def load():
    try: return json.load(open(LEDGER))
    except Exception: return []


def signature(job):
    locs = job.get("locations") or ([dict(job.get("set_opts", {}), biome=job.get("set"))] if job.get("set") else [])
    places = [(l.get("biome", job.get("set")), l.get("tod", "golden")) for l in locs]
    cast = sorted({(c.get("opts") or {}).get("kind", c.get("char")) for c in job.get("cast", []) if c.get("char") != "milo"})
    return {"id": job["id"], "places": places, "cast": cast, "new_song": bool(job.get("new_song", False))}


def check(job, ledger=None):
    ledger = [e for e in (ledger if ledger is not None else load()) if e["id"] != job["id"]]
    sig = signature(job); why = []
    if len(sig["places"]) < 3: why.append(f"only {len(sig['places'])} place(s); use 3-5 locations per song")
    first = sig["places"][0] if sig["places"] else None
    for e in ledger[-4:]:
        if e["places"] and first and tuple(e["places"][0]) == tuple(first):
            why.append(f"first place {first} repeats {e['id']}")
        if e["places"] and first and e["places"][0][0] == first[0] and e is ledger[-1]:
            why.append(f"first biome {first[0]} same as the previous episode {e['id']}")
    if ledger:
        prev = {tuple(p) for p in ledger[-1]["places"]}
        rep = sum(1 for p in sig["places"] if tuple(p) in prev)
        if sig["places"] and rep > len(sig["places"]) / 2:
            why.append(f"{rep}/{len(sig['places'])} places repeat {ledger[-1]['id']}")
        if sig["new_song"]:
            changed = len(set(sig["cast"]) ^ set(ledger[-1]["cast"])) // 2
            if changed < 2: why.append(f"cast changes only {changed} animal(s) vs {ledger[-1]['id']} (new songs need 2+)")
    return why


def record(job):
    led = [e for e in load() if e["id"] != job["id"]]
    led.append(signature(job)); json.dump(led, open(LEDGER, "w"), indent=1)


def suggest():
    led = load()
    used_b = {b: 0 for b in BIOMES}; used_k = {k: 0 for k in KINDS}
    for age, e in enumerate(reversed(led[-12:])):
        w = 12 - age
        for b, _ in e["places"]: used_b[b] = used_b.get(b, 0) + w
        for k in e["cast"]: used_k[k] = used_k.get(k, 0) + w
    b = sorted(BIOMES, key=lambda x: used_b[x])
    print("least used biomes:", ", ".join(b[:6]))
    main = b[0]
    print(f"suggested route: {main} -> {b[1]} -> {b[2]} -> {main} (times of day: mix of {', '.join(TODS[:4])})")
    print("animals that fit", main, ":", ", ".join(sorted(FITS[main], key=lambda k: used_k.get(k, 0))))
    print("least used animals:", ", ".join(sorted(KINDS, key=lambda k: used_k[k])[:8]))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "suggest"
    if cmd == "suggest": suggest(); sys.exit(0)
    job = json.load(open(sys.argv[2]))
    if cmd == "check":
        w = check(job)
        print("OK: looks new" if not w else "REPEATS:\n  - " + "\n  - ".join(w)); sys.exit(1 if w else 0)
    if cmd == "record":
        w = check(job)
        if w and "--force" not in sys.argv: print("not recorded, fix first:\n  - " + "\n  - ".join(w)); sys.exit(1)
        record(job); print("recorded", job["id"])
