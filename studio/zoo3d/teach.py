"""Interactive teaching lessons, v2 (Noelson, Nov 14 2026 noon): "lessons should be interactive, not just the cartoon
moving his body; in-depth, with examples and images matching the items discussed. Music videos keep their own dynamic."

A v2 lesson is built from teaching scenes. In each scene Milo stands on the left, the animal in the middle, and the right
third of the picture is a teaching board: answer signs the child chooses between, a thinking timer, then the example that
shows the fact (teachprops.py), counted or compared with something the child knows. The cast stays calm (no dancing).

  python3 teach.py lessons/<id>.json
     -> jobs/<id>_song.wav, jobs/<id>_timing.json, jobs/<id>.json (zooworld, native 4K, 16 samples: measured Nov 14 on the PC, 1.35 s/frame vs 1.97 at 32, no visible difference), songs/<id>.json (meta + "shorts")

Spec (see make_lessons_p2.py): {"id", "title" (<=60), "card", "thumb_text", "description", "tags", "facts": [...],
  "cast": [main animal kinds], "extras": [{"id", "kind", "scale"}] (live examples: a baby, a friend, a look-alike),
  "segments": [{"name", "kind": "intro" | "teach" | "quiz" | "outro", "biome", "tod", "show": [cast ids], "word": "3D WORD",
     "lines": ["text" | ["text", "shot"] | {"t": "text", "shot": "...", "pause": seconds}],
     "visits": [{"line": n, "show": [...], "biome", "tod", "formation", "place": {"id": [x, y, z]}}],
     "choices": {"a": "YES", "b": "NO", "right": "b", "ask": REF, "answer": REF},
     "exhibits": [{"prop": "<teachprops name>", "at": "ex" | [x, y, z], "on": REF, "off": REF, "opts": {...}, "times": [REF, ...]}],
     "quiz": [["question?", "answer!", "<cast id>"], ...]  (kind quiz), "short": {"id", "title", "l1", "l2"}}]}
REF = [line] (start of that line) | [line, "word"] | [line, "word", nth] | [line, "word", nth, seconds to add].
"""
import json, os, sys, re
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "sing"))
import sing
import lesson as LS

SR, FPS, BPM = LS.SR, LS.FPS, LS.BPM
GAP, SEG_GAP, LEAD = 0.75, 1.3, 0.5
THINK, DO, CHOOSE = 2.0, 2.6, 3.2
POS = {"ex": (2.55, -0.5, 0.0), "ex_front": (2.2, -1.5, 0.0), "ex_hi": (2.6, -1.1, 3.2), "sign_a": (2.6, -1.3, 3.7), "sign_b": (2.6, -1.3, 2.55),
       "dots": (2.6, -1.3, 1.7), "mid_hi": (-0.55, -0.9, 3.75), "mid": (-0.55, -0.3, 0.0), "host_hi": (-3.05, -1.0, 3.3), "top": (0, -0.6, 4.35)}
SIGN_COL = {"a": "#1479d6", "b": "#e85d00"}
ARC = [(-2.3, 1.2), (2.3, 1.2), (-4.1, 0.1), (4.1, 0.1), (-0.9, 2.9), (1.2, 3.0)]     # engine "arc" slots (quiz)
TALL = {"giraffe": 3.8}


def _norm(w): return re.sub(r"\W", "", w.lower())


def build(spec):
    sid = spec["id"]; voice = spec.get("voice", "af_heart"); speed = spec.get("speed", 0.84)
    assert len(spec["title"]) <= 60, "title over 60 characters"
    mains = list(spec["cast"]); extras = spec.get("extras", [])
    # ---- expand quiz segments into lines
    for seg in spec["segments"]:
        if seg.get("kind") == "quiz" and seg.get("quiz"):
            ls = list(seg.get("lines", []))
            seg["_q0"] = len(ls)
            for q, a, who in seg["quiz"]:
                ls += [{"t": q, "shot": "wide", "pause": 2.4}, {"t": a, "shot": "close:" + who}]
            seg["lines"] = ls
    # ---- voice + timing
    t = LEAD; sections, lines, words, clips = [], [], [], []
    for seg in spec["segments"]:
        sec = {"name": seg["name"], "start": t if sections else 0.0, "who": "host"}
        seg["_lt"] = []; seg["_words"] = []
        for ln in seg["lines"]:
            if isinstance(ln, str): ln = {"t": ln}
            elif isinstance(ln, list): ln = {"t": ln[0], "shot": ln[1] if len(ln) > 1 else None}
            text = ln["t"]
            a = sing.say(text, voice, speed); d = len(a) / SR
            clips.append((t, a)); lines.append({"text": text, "start": round(t, 3), "end": round(t + d, 3), "who": "host", "kind": "say", "section": seg["name"]})
            toks = text.split(); tot = sum(len(_norm(w)) + 1.5 for w in toks); c = t; lw = []
            for w in toks:
                wd = d * (len(_norm(w)) + 1.5) / tot
                words.append({"w": w, "start": round(c, 3), "end": round(c + wd, 3), "who": "host"}); lw.append((_norm(w), c)); c += wd
            seg["_lt"].append((t, t + d, ln)); seg["_words"].append(lw)
            pause = ln.get("pause")
            if pause is None: pause = DO if text.lower().startswith("can you") else (THINK if text.rstrip().endswith("?") else 0)
            t += d + GAP + pause
        t += SEG_GAP - GAP; sec["end"] = round(t, 3); sections.append(sec)
    dur = round(t + 1.2, 2); sections[-1]["end"] = dur
    wc = sum(len(l["text"].split()) for l in lines)
    if not 270 <= dur <= 390: print(f"WARNING: lesson is {dur:.0f} s; rulebook KID-04 wants 4:30-6:30 (270-390 s)")
    n = int(SR * dur); vox = np.zeros(n)
    for st, a in clips:
        s0 = int(st * SR); vox[s0:s0 + len(a)] += a[:n - s0]
    env = np.zeros(n)
    for st, a in clips: env[int(st * SR):int(st * SR) + len(a)] = 1.0
    k = int(SR * 0.25); env = np.convolve(env, np.ones(k) / k, "same")
    mus = LS.music(dur) * (0.42 - 0.3 * env)        # quieter bed than the first lessons: the voice is the lesson
    fade = np.minimum(1, np.minimum(np.arange(n) / (SR * 0.5), (n - np.arange(n)) / (SR * 1.5)))
    mix = (vox * 0.95 + mus) * fade; mix = mix / max(1e-6, np.abs(mix).max()) * 0.89
    sf.write(os.path.join(HERE, "jobs", f"{sid}_song.wav"), mix.astype(np.float32), SR)
    hop = SR // FPS; nf = int(np.ceil(dur * FPS)); mouth = []
    for f in range(nf):
        x = vox[f * hop:(f + 1) * hop]; mouth.append(float(np.sqrt(np.mean(x ** 2))) if len(x) else 0.0)
    mx = max(mouth) or 1.0; mouth = [round(min(1.0, (m / mx) * 2.2) ** 0.7, 3) for m in mouth]
    bl = 60 / BPM
    timing = {"duration": dur, "bpm": BPM, "beats": [round(i * bl, 4) for i in range(int(dur / bl) + 1)], "sections": sections,
              "lines": lines, "words": words, "mouth": mouth, "fps": FPS, "repaired_words": 0, "kind": "lesson"}
    json.dump(timing, open(os.path.join(HERE, "jobs", f"{sid}_timing.json"), "w"))

    # ---- cast
    cast = [{"id": "host", "char": "milo", "spot": "center"}]
    for i, kind in enumerate(mains):
        cast.append({"id": kind, "char": "animal", "spot": LS.SPOTS[i % 6][0], "opts": {"kind": kind}, "yaw": LS.SPOTS[i % 6][1]})
    for e in extras:
        cast.append({"id": e["id"], "char": "animal", "spot": "back", "opts": {"kind": e["kind"], "scale": e.get("scale", 1.0)}})

    def ref(seg, r, sec_start):
        """REF -> seconds from the section start."""
        if isinstance(r, (int, float)): r = [int(r)]
        li = r[0]; t0 = seg["_lt"][li][0]
        if len(r) > 1 and r[1]:
            if r[1] == "end": t0 = seg["_lt"][li][1]
            else:
                hits = [c for w, c in seg["_words"][li] if w == _norm(r[1])]
                nth = r[2] if len(r) > 2 else 0
                if len(hits) > nth: t0 = hits[nth] - 0.1
                else: print(f"  note: word {r[1]!r} not found in line {li} of {seg['name']}")
        return round(t0 - sec_start + (r[3] if len(r) > 3 else 0.0), 3)

    locs, direct, shorts = [], [], []
    for i, seg in enumerate(spec["segments"]):
        kind = seg.get("kind", "teach"); sc = sections[i]; s0 = sc["start"] if i else 0.0; nl = len(seg["lines"]); seg_len = sc["end"] - s0
        visits = seg.get("visits") or [{}]
        shots = [None] * nl
        for vi, v in enumerate(visits):
            show = v.get("show", seg.get("show"))
            if show is None and kind != "teach": show = mains            # never show the helpers (babies, look-alikes) in group scenes
            form = v.get("formation", seg.get("formation"))
            if not form:
                form = {"intro": "line", "quiz": "arc", "outro": "v"}.get(kind, "teach")
            lc = {"from": seg["name"], "biome": v.get("biome", seg["biome"]), "tod": v.get("tod", seg.get("tod", "noon")), "formation": form,
                  "shot": v.get("shot", seg.get("shot", "teach" if kind == "teach" else ("reveal", "vista", "dolly")[i % 3]))}
            if kind == "teach": lc["zoom"] = 1.0
            if v.get("line"): lc["line"] = v["line"]
            if show: lc["show"] = show
            if v.get("place") or seg.get("place"): lc["place"] = dict(seg.get("place", {}), **v.get("place", {}))
            locs.append(lc)
            a = v.get("line", 0); b = visits[vi + 1].get("line", nl) if vi + 1 < len(visits) else nl
            for k in range(a, b):
                given = seg["_lt"][k][2].get("shot")
                if given: shots[k] = given
                elif kind == "teach": shots[k] = "teach"
                else: shots[k] = ("wide", "close:host", "orbit", "low", "vista", "close:host", "high", "dolly")[(k - a) % 8]
        d = {"section": seg["name"], "shots": shots, "energy": seg.get("energy", 0.3 if kind == "teach" else 0.6), "wave": 0 if kind == "teach" else 1,
             "jump": seg.get("jump", 0.0 if kind == "teach" else 0.2), "group": False, "props": []}
        if seg.get("jumpers"): d["jumpers"] = seg["jumpers"]
        P = d["props"]

        def add(prop, at, on, off=None, opts=None, lead=0.0):
            at = POS[at] if isinstance(at, str) else tuple(at)
            t_on = max(0.0, on - lead); t_off = seg_len - 0.3 if off is None else off
            P.append({"type": "teach", "name": prop, "at": list(at), "delay": round(t_on, 3), "dur": round(max(0.6, t_off - t_on), 3), "spin": 0, "opts": opts or {}})

        if seg.get("word"):
            pr = {"type": "text", "text": seg["word"], "color": LS.COLORS[i % len(LS.COLORS)], "at": list(POS["top"]) if kind == "teach" else "top",
                  "size": seg.get("word_size", 0.62 if kind == "teach" else 0.7), "delay": 1.0}
            if seg.get("word_on"): pr["delay"] = ref(seg, seg["word_on"], s0)
            if seg.get("word_off"): pr["dur"] = max(1.0, ref(seg, seg["word_off"], s0) - pr["delay"])
            P.append(pr)
        ch = seg.get("choices")
        if ch:   # two answer signs, a thinking timer, then the right one is marked and the wrong one leaves
            t_ask = ref(seg, ch["ask"], s0); t_ans = ref(seg, ch["answer"], s0)
            q_end = seg["_lt"][ch["ask"][0]][1] - s0
            for key in ("a", "b"):
                right = ch["right"] == key
                o = {"text": ch[key], "color": ch.get("colors", SIGN_COL).get(key, SIGN_COL[key]) if isinstance(ch.get("colors"), dict) else SIGN_COL[key]}
                if right: o["win"] = round(t_ans - (t_ask + (0.0 if key == "a" else 0.45)), 3)
                add("sign", "sign_" + key, t_ask + (0.0 if key == "a" else 0.45), t_ans + (ch.get("hold", 3.0) if right else 0.0), o)
            add("dots", "dots", q_end + 0.2, t_ans, {})
        for ex in seg.get("exhibits", []):
            on = ref(seg, ex["on"], s0); off = ref(seg, ex["off"], s0) if ex.get("off") else None
            o = dict(ex.get("opts", {}))
            if ex.get("times"): o["times"] = [round(ref(seg, r, s0) - on, 3) for r in ex["times"]]
            if ex.get("leave"): o["leave"] = round(ref(seg, ex["leave"], s0) - on, 3)
            add(ex["prop"], ex.get("at", "ex"), on, off, o)
        if kind == "quiz" and seg.get("quiz"):
            q0 = seg["_q0"]
            for k, (q, a, who) in enumerate(seg["quiz"]):
                tq = seg["_lt"][q0 + 2 * k][0] - s0; ta = seg["_lt"][q0 + 2 * k + 1][0] - s0; te = seg["_lt"][q0 + 2 * k + 1][1] - s0
                add("badge", (0.0, -1.2, 3.55), tq, ta, {"text": "?", "color": "#8e5bd8", "s": 1.25})
                if who in mains:
                    x, y = ARC[mains.index(who) % len(ARC)]
                    add("check", (x + 0.75, y - 0.9, TALL.get(who, 2.65) + 0.25), ta + 0.25, te + 0.9, {"s": 0.8})
        direct.append(d)
        if seg.get("short"):
            sh = seg["short"]   # "from"/"to": line numbers, so the Short is the question, the answer and the example (20-60 s)
            a0 = seg["_lt"][sh["from"]][0] - 0.35 if sh.get("from") else s0
            b0 = seg["_lt"][sh["to"]][0] - 0.25 if sh.get("to") else sc["end"]
            shorts.append(dict(sh, seg=seg["name"], start=round(max(0.0, a0), 3), end=round(b0, 3), seconds=round(b0 - a0, 1)))

    job = {"id": sid, "title": spec.get("card", spec["title"]), "channel": "zoo", "set": "zooworld", "set_opts": {}, "seed": spec.get("seed", 5),
           "new_song": True, "kind": "lesson", "cast": cast, "locations": locs, "intro_shot": "reveal", "intro": {"energy": 0.6, "wave": 1},
           "thumb_frame": spec.get("thumb_frame", 72), "direct": direct, "song": sid, "res": spec.get("res", "3840x2160"),
           "samples": spec.get("samples", 16), "step": 1, "hold_shots": True, "cut_mode": "beat", "follow_singer": False, "punch": False,
           "timing_file": f"{sid}_timing.json", "audio": f"{sid}_song.wav"}
    json.dump(job, open(os.path.join(HERE, "jobs", f"{sid}.json"), "w"), indent=1)
    song = {"kind": "lesson", "format": "3d_lesson", "lesson_version": 2, "desc_header": "IN THIS LESSON", "lyrics": "\n".join(spec.get("facts", [])),
            "script": "\n".join(l["text"] for l in lines), "duration": dur, "bpm": BPM,
            "meta": {"title": spec["title"], "card": spec.get("card", spec["title"]), "thumb_text": spec.get("thumb_text", ""),
                     "description": spec["description"].rstrip() + "\n\n" + LS.BOILER, "tags": spec.get("tags", [])}, "shorts": shorts, "job": job}
    json.dump(song, open(os.path.join(HERE, "songs", f"{sid}.json"), "w"), indent=1)
    print(f"OK {sid}: {dur:.0f} s ({int(dur // 60)}:{int(dur % 60):02d}), {wc} words, {len(lines)} lines, {len(locs)} visits, "
          f"{sum(len(x['props']) for x in direct)} teaching props, {len(shorts)} shorts")
    return job


if __name__ == "__main__":
    build(json.load(open(sys.argv[1])))
