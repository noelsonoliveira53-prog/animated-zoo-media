"""Song + word alignment -> engine timing.json.  Shared by build_timing.py (container) and align.py (PC).

build(song, aligned_words, tx_words, spec, ffmpeg="ffmpeg", who_map=None) -> timing dict

aligned_words: forced alignment to the lyrics (one entry per lyric token, but it can collapse in long
               instrumental breaks: many words stacked on one timestamp, or a line stretched over 20 s).
tx_words:      free transcription with word times (may mishear words, but its timing is honest).
Repair: every lyric token that the transcription also heard (difflib match) takes the transcription's time
when the two disagree by more than 0.8 s, and stacked/stretched words are re-spread between good neighbours.
"""
import re, subprocess, difflib
import numpy as np

norm = lambda s: re.sub(r"[^a-z']", "", s.lower()).replace("'s", "").replace("'", "")


def lyric_sections(lyrics):
    secs, counts = [], {}
    for raw in lyrics.splitlines():
        l = raw.strip()
        if not l: continue
        m = re.match(r"^\[(.+?)\]$", l)
        if m:
            base = re.sub(r"[^a-z]", "", m.group(1).lower().split()[0]) or "part"
            base = {"finalchorus": "chorus", "final": "chorus", "break": "action"}.get(base, base)
            counts[base] = counts.get(base, 0) + 1
            secs.append({"name": f"{base}{counts[base]}", "lines": []}); continue
        if not secs: secs.append({"name": "verse1", "lines": []}); counts["verse"] = 1
        toks = [t for t in l.split() if norm(t)]
        if toks: secs[-1]["lines"].append(toks)
    return secs


def _merge_tx(tx):
    out = []
    for w in tx or []:
        if out and w["w"].startswith("-"):
            out[-1] = {"w": out[-1]["w"] + w["w"], "start": out[-1]["start"], "end": w["end"]}
        else:
            out.append(dict(w))
    return out


def repair(line_toks, aligned, tx):
    """line_toks: list of lines (lists of lyric tokens). Returns (times per token, n repaired, extra tx words after the lyrics)."""
    tokens = [t for l in line_toks for t in l]; n = len(tokens)
    tx = _merge_tx(tx)
    # 1) forced alignment mapped onto tokens in order (tolerant)
    times = [None] * n; i = 0
    for k, t in enumerate(tokens):
        j = i
        while j < min(i + 4, len(aligned)) and norm(aligned[j]["w"]) != norm(t): j += 1
        if j >= len(aligned) or j >= i + 4: j = i
        if j < len(aligned):
            times[k] = [aligned[j]["start"], max(aligned[j]["end"], aligned[j]["start"] + 0.05)]; i = j + 1
    bad = [times[k] is None for k in range(n)]
    def suspicious(a, b):   # forced times inside one line look broken?
        ts = [times[k] for k in range(a, b)]
        if any(t is None for t in ts): return True
        if any(t[1] - t[0] > 3.0 for t in ts): return True
        if any(ts[q + 1][0] - ts[q][1] > 2.5 for q in range(len(ts) - 1)): return True
        if any(ts[q + 1][0] < ts[q][0] - 0.05 for q in range(len(ts) - 1)): return True
        st = sorted(t[0] for t in ts)
        return any(st[q + 2] - st[q] < 0.15 for q in range(len(st) - 2))
    # 2) line-by-line anchoring on the transcription (greedy, in order)
    bn = [norm(w["w"]) for w in tx]
    pos, prev_end, k0 = 0, 0.0, 0
    for toks in line_toks:
        a, b = k0, k0 + len(toks); k0 = b
        if not tx: continue
        an = [norm(t) for t in toks]
        best = None
        for s0 in range(pos, len(tx)):
            if tx[s0]["start"] < prev_end - 1.0: continue
            if tx[s0]["start"] > prev_end + 45: break
            win = bn[s0:s0 + len(toks) + 4]
            sm = difflib.SequenceMatcher(None, an, win, autojunk=False)
            lim = tx[s0]["start"] + max(6.0, 0.9 * len(toks))   # the matched words must sit close together in time
            pairs = [(blk.a + q, s0 + blk.b + q) for blk in sm.get_matching_blocks() for q in range(blk.size)]
            pairs = [pq for pq in pairs if tx[pq[1]]["start"] <= lim]
            if not pairs: continue
            sc = len(pairs) / max(1, len(toks))
            if pairs and pairs[0][0] == 0: sc += 0.05   # prefer windows that start on the line's first word
            if best is None or sc > best[0] + 1e-9: best = (sc, pairs)
        if best and best[0] >= 0.5:
            pairs = best[1]
            fk, ftx = pairs[0]
            off = abs(times[a + fk][0] - tx[ftx]["start"]) if times[a + fk] else 99
            gap = (times[a][0] - prev_end) if times[a] else 0
            if suspicious(a, b) or (gap > 8 and off > 3.0 and best[0] >= 0.7):
                matched = {a + x: tx[y] for x, y in pairs}
                for k in range(a, b):
                    if k in matched: times[k] = [matched[k]["start"], max(matched[k]["end"], matched[k]["start"] + 0.05)]; bad[k] = False
                    else: bad[k] = True
            pos = pairs[-1][1] + 1
        else:
            if suspicious(a, b):
                for k in range(a, b): bad[k] = True
        good = [times[k][1] for k in range(a, b) if not bad[k] and times[k]]
        if good: prev_end = max(good)
    # 3) word-level clean-up: stacked / stretched / non-monotonic / big gap inside the line
    k0 = 0
    for toks in line_toks:
        a, b = k0, k0 + len(toks); k0 = b
        for k in range(a, b):
            if bad[k]: continue
            if times[k][1] - times[k][0] > 3.0: bad[k] = True
            if k > a and not bad[k - 1] and times[k][0] - times[k - 1][1] > 2.5: bad[k] = True
    last = -1.0
    for k in range(n):
        if bad[k]: continue
        if times[k][0] < last - 0.05: bad[k] = True; continue
        last = times[k][0]
    # 4) re-spread bad runs right after the last good word
    k = 0
    while k < n:
        if not bad[k]: k += 1; continue
        e = k
        while e < n and bad[e]: e += 1
        t0 = times[k - 1][1] if k > 0 else 0.0
        t1 = times[e][0] if e < n else t0 + 0.45 * (e - k)
        span = max(0.12 * (e - k), min(t1 - t0, 0.5 * (e - k)))
        st = t0 + 0.05
        step = span / (e - k)
        for q in range(k, e): times[q] = [st + (q - k) * step, st + (q - k + 1) * step]
        k = e
    for k in range(n):   # cap word length so lyrics never sit on screen for 10+ s
        times[k][1] = min(times[k][1], times[k][0] + 2.5)
        if k + 1 < n: times[k][1] = min(times[k][1], max(times[k][0] + 0.08, times[k + 1][0]))
    end = times[-1][1] if n else 0
    extra = [w for w in tx if w["start"] > end + 0.5]
    return times, sum(bad), extra


def build(song, aligned, tx, spec, ffmpeg="ffmpeg", who="host", who_map=None):
    who_map = who_map or spec.get("who_map", {})
    secs = lyric_sections(spec["lyrics"])
    line_toks = [ln for s in secs for ln in s["lines"]]
    times, nbad, extra = repair(line_toks, aligned, tx)
    words, lines, sections = [], [], []; k = 0
    for s in secs:
        s_who = who_map.get(s["name"], who); s0 = None
        for toks in s["lines"]:
            lw = []
            for t in toks:
                st, en = times[k]; k += 1
                lw.append({"w": t, "start": round(st, 3), "end": round(max(en, st + 0.08), 3), "who": s_who})
            words += lw
            lines.append({"text": " ".join(toks), "start": lw[0]["start"], "end": lw[-1]["end"], "who": s_who, "kind": "sing", "section": s["name"]})
            s0 = lw[0]["start"] if s0 is None else s0
        if s0 is not None: sections.append({"name": s["name"], "start": s0, "who": s_who})
    # the singer often repeats the chorus after the written lyrics end: caption it from the transcription
    if extra and lines:
        grp = []
        for w in extra + [None]:
            if w is None or (grp and (w["start"] - grp[-1]["end"] > 0.8 or len(grp) >= 8 or (len(grp) >= 3 and w["w"].strip()[:1].isupper()))):
                if grp:
                    lw = [{"w": x["w"].strip(), "start": round(x["start"], 3), "end": round(min(max(x["end"], x["start"] + 0.08), x["start"] + 2.5), 3), "who": lines[-1]["who"]} for x in grp]
                    words += lw
                    lines.append({"text": " ".join(x["w"] for x in lw), "start": lw[0]["start"], "end": lw[-1]["end"], "who": lw[0]["who"], "kind": "sing", "section": sections[-1]["name"], "extra": True})
                grp = []
            if w is not None: grp.append(w)
    fps = 24
    pcm = subprocess.run([ffmpeg, "-v", "error", "-i", song, "-ac", "1", "-ar", "24000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, dtype=np.float32); sr = 24000; dur = len(a) / sr
    hop = sr // fps
    rms = np.array([np.sqrt(np.mean(a[q:q + hop] ** 2)) for q in range(0, len(a), hop)])
    ref = np.percentile(rms[rms > 1e-4], 95) if (rms > 1e-4).any() else 1
    gate = np.zeros_like(rms)
    for w in words:
        gate[int(max(0, w["start"] - 0.03) * fps): int(w["end"] * fps) + 1] = 1
    m = np.clip(rms / ref * 1.15, 0, 1) * gate
    out, cur = np.zeros_like(m), 0.0
    for q, x in enumerate(m):
        cur = x if x > cur else cur * 0.55 + x * 0.45; out[q] = cur
    mouth = [round(float(x), 3) for x in np.concatenate([out[1:], [0.0]])]
    bpm = spec.get("bpm", 116); beat = 60 / bpm
    # a long instrumental gap inside a section becomes its own "break" section (dance shots, no lyrics)
    fixed = []
    for q, s in enumerate(sections):
        fixed.append(s)
        nxt = sections[q + 1]["start"] if q + 1 < len(sections) else None
        sl = [l for l in lines if l["section"] == s["name"]]
        if sl and nxt is not None and nxt - sl[-1]["end"] > 8:
            fixed.append({"name": f"break_{s['name']}", "start": sl[-1]["end"] + 0.6, "who": s["who"]})
    sections = fixed
    for q, s in enumerate(sections):
        s["start"] = max(0.0, s["start"] - beat * 0.5) if q else 0.0
        s["end"] = sections[q + 1]["start"] - beat * 0.5 if q + 1 < len(sections) else dur
        s["end"] = max(s["end"], s["start"] + 0.5)
    sections[-1]["end"] = dur
    return {"duration": dur, "bpm": bpm, "beats": [round(q * beat, 4) for q in range(int(dur / beat) + 1)], "sections": sections,
            "lines": lines, "words": words, "mouth": mouth, "fps": fps, "repaired_words": nbad}
