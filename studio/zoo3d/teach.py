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
import wordsync as WS

SR, FPS, BPM = LS.SR, LS.FPS, LS.BPM
GAP, SEG_GAP, LEAD = 0.75, 1.3, 0.5
THINK, DO, CHOOSE = 2.0, 2.6, 3.2
POS = {"ex": (2.55, -0.5, 0.0), "ex_front": (2.2, -1.5, 0.0), "ex_hi": (2.6, -1.1, 3.2), "sign_a": (1.95, -1.3, 3.7), "sign_b": (1.95, -1.3, 2.55),
       "dots": (1.95, -1.3, 1.7), "mid_hi": (-0.55, -0.9, 3.75), "mid": (0.1, -0.3, 0.0), "host_hi": (-3.05, -1.0, 3.3), "top": (-0.7, -0.6, 4.35)}   # top: x=-0.7 since Nov 15 (at x=0 a wide top sign covered the end of the word)
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
    SYNC = {"aligned": 0, "words": 0, "onset_err": [], "unaligned_lines": []}
    for seg in spec["segments"]:
        sec = {"name": seg["name"], "start": t if sections else 0.0, "who": "host"}
        seg["_lt"] = []; seg["_words"] = []
        for ln in seg["lines"]:
            if isinstance(ln, str): ln = {"t": ln}
            elif isinstance(ln, list): ln = {"t": ln[0], "shot": ln[1] if len(ln) > 1 else None}
            text = ln["t"]
            said = WS.spoken(text)                       # the voice gets a sayable spelling ("Brrr" -> "Burr"); the caption keeps the text
            a = sing.say(said, voice, speed); d = len(a) / SR
            clips.append((t, a)); lines.append({"text": text, "start": round(t, 3), "end": round(t + d, 3), "who": "host", "kind": "say", "section": seg["name"]})
            # every word is placed from the sound itself (forced alignment), not estimated: captions, counting props and
            # answer signs all hang on these times ("all words in sync", Noelson Nov 14)
            toks = text.split(); al, got, nw = WS.align(a, said); lw = []
            SYNC["aligned"] += got; SYNC["words"] += nw; SYNC["onset_err"] += WS.onset_errors(a, al)
            if got < nw: SYNC["unaligned_lines"].append(text)
            for w_, (ws_, we_) in zip(toks, al):         # a word that takes far too long was probably mispronounced by the voice
                if we_ - ws_ > max(0.95, 0.2 * len(_norm(w_))): SYNC.setdefault("suspect", []).append(f"{w_} ({we_ - ws_:.1f} s) in: {text}")
            for w, (ws, we) in zip(toks, al):
                words.append({"w": w, "start": round(t + ws, 3), "end": round(t + we, 3), "who": "host"}); lw.append((_norm(w), t + ws))
            seg["_lt"].append((t, t + d, ln)); seg["_words"].append(lw)
            pause = ln.get("pause")
            if pause is None: pause = DO if text.lower().startswith("can you") else (THINK if text.rstrip().endswith("?") else 0)
            t += d + GAP + pause
        t += SEG_GAP - GAP; sec["end"] = round(t, 3); sections.append(sec)
    dur = round(t + 1.2, 2); sections[-1]["end"] = dur
    wc = sum(len(l["text"].split()) for l in lines)
    V3 = spec.get("version", 2) >= 3     # Noelson, Nov 14 5:12 PM: lessons at least 5 minutes, Shorts a minute and a half
    LMIN, LMAX = (300, 390) if V3 else (270, 390)
    PROBLEMS = []
    if not LMIN <= dur <= LMAX: PROBLEMS.append(f"lesson is {dur:.1f} s; it must be {LMIN}-{LMAX} s")
    print("   parts: " + ", ".join(f"{sc_['name']} {sc_['end'] - (sc_['start'] if k_ else 0.0):.1f}" for k_, sc_ in enumerate(sections)))
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
        if kind != "teach":   # group scenes: a line that brings in an example is shown wide, so the example is in the picture
            # ... and so is every later line while it stays up (Nov 15: the "vista" line after the 1-2-3 count cut Milo at the bottom of
            # the picture in every hello; zool_ep09 0:16, zool_ep12 0:17)
            for e_ in seg.get("exhibits", []):
                k_ = e_["on"][0] if isinstance(e_["on"], list) else int(e_["on"])
                f_ = e_.get("off"); k1_ = nl - 1 if f_ is None else (f_[0] if isinstance(f_, list) else int(f_))
                for q_ in range(k_, min(k1_, nl - 1) + 1):
                    if not seg["_lt"][q_][2].get("shot"): shots[q_] = "wide"
        d = {"section": seg["name"], "shots": shots, "energy": seg.get("energy", 0.3 if kind == "teach" else 0.6), "wave": 0 if kind == "teach" else 1,
             "jump": seg.get("jump", 0.0 if kind == "teach" else 0.2), "group": False, "props": []}
        if seg.get("jumpers"): d["jumpers"] = seg["jumpers"]
        P = d["props"]

        def add(prop, at, on, off=None, opts=None, lead=0.0):
            at = POS[at] if isinstance(at, str) else tuple(at)
            t_on = max(0.0, on - lead); t_off = seg_len - 0.3 if off is None else off
            P.append({"type": "teach", "name": prop, "at": list(at), "delay": round(t_on, 3), "dur": round(max(0.6, t_off - t_on), 3), "spin": 0, "opts": opts or {}})
            if prop == "sign" and kind == "teach":      # Shorts-safe check: the Short shows the centre 90% of the picture's width (still review Nov 14: x=3.94 touched the edge)
                tx = (opts or {}).get("text", "?"); ts_ = 0.5 * (8.0 / len(tx) if len(tx) > 8 else 1.0); w_ = min(2.8, max(1.5, len(tx) * ts_ * 0.66 + 0.6))
                if at[0] + w_ / 2 + 0.24 > 3.7 or at[0] - w_ / 2 < -4.0: PROBLEMS.append(f"sign '{tx}' in {seg['name']} reaches x={at[0] + w_ / 2 + 0.24:.2f}: outside the Shorts-safe area (3.7)")

        if seg.get("word"):
            pr = {"type": "text", "text": seg["word"], "color": LS.COLORS[i % len(LS.COLORS)], "at": list(POS["top"]) if kind == "teach" else "top",
                  "size": seg.get("word_size", 0.62 if kind == "teach" else 0.7), "delay": 1.0}
            if seg.get("word_on"): pr["delay"] = ref(seg, seg["word_on"], s0)
            if seg.get("word_off"): pr["dur"] = max(1.0, ref(seg, seg["word_off"], s0) - pr["delay"])
            P.append(pr)
        rounds = ([seg["choices"]] if seg.get("choices") else []) + list(seg.get("checks", []))
        # "checks": more question rounds in the same part (a second yes/no, the quick check at the end). The board is cleared
        # for each of them: an example on the right that has no "off" of its own leaves just before the signs come in.
        clear_at = sorted(ref(seg, c_["ask"], s0) - 0.25 for c_ in seg.get("checks", []))
        for ch in rounds:   # two answer signs, a thinking timer, then the right one is marked and the wrong one leaves
            t_ask = ref(seg, ch["ask"], s0); t_ans = ref(seg, ch["answer"], s0)
            q_end = seg["_lt"][ch["ask"][0]][1] - s0
            for key in ("a", "b"):
                right = ch["right"] == key
                o = {"text": ch[key], "color": ch.get("colors", SIGN_COL).get(key, SIGN_COL[key]) if isinstance(ch.get("colors"), dict) else SIGN_COL[key]}
                if right: o["win"] = round(t_ans - (t_ask + (0.0 if key == "a" else 0.45)), 3)
                add("sign", "sign_" + key, t_ask + (0.0 if key == "a" else 0.45), t_ans + (ch.get("hold", 3.0) if right else 0.0), o)
            add("dots", "dots", q_end + 0.2, t_ans, {})
            # Nov 15 frame check (zool_ep09 "It is the giraffe!", zool_ep10 "It is the cow!"): a close-up while the answer signs
            # are still up cuts the signs at the edge of the picture. Every line that starts while the signs are visible is
            # shown on the teaching shot, so the signs, the confetti on the right one and both faces stay in the picture.
            t_end = t_ans + ch.get("hold", 3.0)
            for k_ in range(nl):
                ls_ = seg["_lt"][k_][0] - s0
                if t_ask - 0.01 <= ls_ < t_end and shots[k_] not in (None, "teach"):
                    print(f"  note: {seg['name']} line {k_} shot {shots[k_]} -> teach (answer signs are on screen)")
                    shots[k_] = "teach"
        for ex in seg.get("exhibits", []):
            on = ref(seg, ex["on"], s0); off = ref(seg, ex["off"], s0) if ex.get("off") else None
            at_ = POS[ex.get("at", "ex")] if isinstance(ex.get("at", "ex"), str) else ex["at"]
            if off is None and kind == "teach" and at_[0] >= 0.8 and not ex.get("keep"):
                nxt = [c_ for c_ in clear_at if c_ > on + 0.5]
                if nxt: off = nxt[0]
            o = dict(ex.get("opts", {}))
            if ex.get("times"): o["times"] = [round(ref(seg, r, s0) - on, 3) for r in ex["times"]]
            if ex.get("leave"): o["leave"] = round(ref(seg, ex["leave"], s0) - on, 3)
            add(ex["prop"], ex.get("at", "ex"), on, off, o)
        if kind != "teach":   # group scenes: in the wide shot the 1-2-3 count stands on the 3D word (zool_ep12 still): the word leaves first
            cn_ = [p_["delay"] for p_ in P if p_.get("type") == "teach" and p_["name"] == "count"]
            for p_ in P:
                if cn_ and p_.get("type") == "text" and "dur" not in p_: p_["dur"] = round(max(1.0, min(cn_) - p_.get("delay", 0) - 0.15), 3)
        if kind == "teach":
            # Nov 15 frame check (sun at 2:32 of zool_ep09b, 2:23 of zool_ep08): a close-up while a high example (z >= 3.0: sun,
            # count badges) is up cuts it at the top of the picture. Close-up lines that overlap one use the teaching shot.
            hi_ = [(p_["delay"], p_["delay"] + p_["dur"], p_["name"]) for p_ in P if p_.get("type") == "teach" and p_["name"] not in ("sign", "dots") and p_["at"][2] >= 3.0]
            for k_ in range(nl):
                a_, b_ = seg["_lt"][k_][0] - s0, seg["_lt"][k_][1] - s0
                hit_ = [h_ for h_ in hi_ if h_[0] < b_ and a_ < h_[1]]
                if hit_ and str(shots[k_]).startswith("close"):
                    print(f"  note: {seg['name']} line {k_} shot {shots[k_]} -> teach ({hit_[0][2]} is up high)"); shots[k_] = "teach"
        if kind == "quiz" and seg.get("quiz"):
            q0 = seg["_q0"]
            for k, (q, a, who) in enumerate(seg["quiz"]):
                tq = seg["_lt"][q0 + 2 * k][0] - s0; ta = seg["_lt"][q0 + 2 * k + 1][0] - s0; te = seg["_lt"][q0 + 2 * k + 1][1] - s0
                add("badge", (0.0, -1.2, 3.55), tq, ta, {"text": "?", "color": "#8e5bd8", "s": 1.25})
                if who in mains:
                    # Nov 15 frames (lion 5:16 of zool_ep09b, koala 5:12 of zool_ep08): 0.9 in front of the animal the check
                    # covered its face in the answer close-up. It stands beside the head on the outer side (1.75: clear of the
                    # elephant's ears and the lion's mane in the stills), smaller, and is gone before the next question's wide shot.
                    x, y = ARC[mains.index(who) % len(ARC)]
                    nq_ = seg["_lt"][q0 + 2 * k + 2][0] - s0 - 0.05 if q0 + 2 * k + 2 < nl else te + 0.9
                    sl_ = mains.index(who) % len(ARC)     # back-left place: its outer side is hidden behind the front-left animal -> inner side
                    zc_ = TALL.get(who, 2.65) - 0.45       # inner side: 1.5 from the head and 0.3 higher, or Milo's head hides its lower edge
                    if sl_ == 0 and zc_ < 3.0: zc_ += 0.3
                    add("check", (x + ((1.5 if sl_ == 0 else 1.75) if (x >= 0 or sl_ == 0) else -1.75), y, zc_), ta + 0.25, min(te + 0.9, nq_), {"s": 0.6})
                    if len(mains) > 3: PROBLEMS.append("quiz with more than 3 animals: the check places are only checked for 3; look at a still of every quiz answer")
            # the "?" badge covered the middle of the QUIZ TIME! word: the word leaves just before the first badge
            tq0_ = seg["_lt"][q0][0] - s0
            for p_ in P:
                if p_.get("type") == "text" and "dur" not in p_: p_["dur"] = round(max(1.0, tq0_ - p_.get("delay", 0) - 0.15), 3)
        direct.append(d)
        if seg.get("short"):
            sh = seg["short"]   # "from"/"to": line numbers, so the Short is the question, the answer and the example (20-60 s)
            a0 = seg["_lt"][sh["from"]][0] - 0.35 if sh.get("from") else (seg["_lt"][0][0] - 0.4 if V3 else s0)
            b0 = seg["_lt"][sh["to"]][0] - 0.25 if sh.get("to") else (seg["_lt"][-1][1] + 0.9 if V3 else sc["end"])
            shorts.append(dict(sh, seg=seg["name"], start=round(max(0.0, a0), 3), end=round(b0, 3), seconds=round(b0 - a0, 1)))
            if V3 and not 85 <= b0 - a0 <= 95: PROBLEMS.append(f"Short {sh['id']} ({seg['name']}) is {b0 - a0:.1f} s; it must be 85-95 s (a minute and a half)")

    thumb = spec.get("thumb_frame", 72)
    if spec.get("thumb_at"):   # ["segment", line, 0..1]: the thumbnail shows a teaching moment (animal + example), not the hello
        sg = next(g for g in spec["segments"] if g["name"] == spec["thumb_at"][0]); a0, b0, _ = sg["_lt"][spec["thumb_at"][1]]
        thumb = int((a0 + (b0 - a0) * spec["thumb_at"][2]) * FPS)
    job = {"id": sid, "title": spec.get("card", spec["title"]), "channel": "zoo", "set": "zooworld", "set_opts": {}, "seed": spec.get("seed", 5),
           "new_song": True, "kind": "lesson", "cast": cast, "locations": locs, "intro_shot": "reveal", "intro": {"energy": 0.6, "wave": 1},
           "thumb_frame": thumb, "direct": direct, "song": sid, "res": spec.get("res", "3840x2160"),
           "samples": spec.get("samples", 16), "step": 1, "hold_shots": True, "cut_mode": "beat", "follow_singer": False, "punch": False,
           "timing_file": f"{sid}_timing.json", "audio": f"{sid}_song.wav"}
    json.dump(job, open(os.path.join(HERE, "jobs", f"{sid}.json"), "w"), indent=1)
    song = {"kind": "lesson", "format": "3d_lesson", "lesson_version": 3 if V3 else 2, "desc_header": "IN THIS LESSON", "lyrics": "\n".join(spec.get("facts", [])),
            "script": "\n".join(l["text"] for l in lines), "duration": dur, "bpm": BPM,
            "sync": {"method": "forced alignment of every line (PocketSphinx)", "aligned": SYNC["aligned"], "words": SYNC["words"],
                     "pause_onsets_checked": len(SYNC["onset_err"]), "onset_err_mean_ms": round(1000 * float(np.mean(SYNC["onset_err"] or [0])), 1),
                     "onset_err_max_ms": round(1000 * float(max(SYNC["onset_err"] or [0])), 1), "unaligned_lines": SYNC["unaligned_lines"],
                     "suspect_words": SYNC.get("suspect", [])},
            "meta": {"title": spec["title"], "card": spec.get("card", spec["title"]), "thumb_text": spec.get("thumb_text", ""),
                     "description": spec["description"].rstrip() + "\n\n" + LS.BOILER, "tags": spec.get("tags", [])}, "shorts": shorts, "job": job}
    json.dump(song, open(os.path.join(HERE, "songs", f"{sid}.json"), "w"), indent=1)
    print(f"OK {sid}: {dur:.0f} s ({int(dur // 60)}:{int(dur % 60):02d}), {wc} words, {len(lines)} lines, {len(locs)} visits, "
          f"{sum(len(x['props']) for x in direct)} teaching props, {len(shorts)} shorts")
    print(f"   sync: {SYNC['aligned']}/{SYNC['words']} words aligned from the audio; at {len(SYNC['onset_err'])} pauses the next word starts "
          f"{1000 * float(np.mean(SYNC['onset_err'] or [0])):.0f} ms (mean) / {1000 * float(max(SYNC['onset_err'] or [0])):.0f} ms (max) from the measured sound onset"
          + (f"; NOT aligned: {SYNC['unaligned_lines']}" if SYNC['unaligned_lines'] else "")
          + (f"; CHECK PRONUNCIATION: {SYNC['suspect']}" if SYNC.get('suspect') else ""))
    json.dump(PROBLEMS, open(os.path.join(HERE, "jobs", f"{sid}_problems.json"), "w"))
    for p_ in PROBLEMS: print("   FAIL:", p_)
    if SYNC["aligned"] < SYNC["words"] or SYNC.get("suspect"): print("   FAIL: word sync is not 100% clean")
    return job


if __name__ == "__main__":
    build(json.load(open(sys.argv[1])))
