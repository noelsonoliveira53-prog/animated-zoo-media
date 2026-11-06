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


def repair(tokens, aligned, tx):
    """tokens: lyric tokens in order. Returns [(start,end)] per token."""
    n = len(tokens)
    # 1) map aligned words onto tokens in order (tolerant)
    times = [None] * n; i = 0
    for k, t in enumerate(tokens):
        j = i
        while j < min(i + 4, len(aligned)) and norm(aligned[j]["w"]) != norm(t): j += 1
        if j >= len(aligned) or j >= i + 4: j = i
        if j < len(aligned):
            times[k] = [aligned[j]["start"], max(aligned[j]["end"], aligned[j]["start"] + 0.05)]; i = j + 1
    # 2) transcription matches
    txt = [None] * n
    if tx:
        a = [norm(t) for t in tokens]; b = [norm(w["w"]) for w in tx]
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for blk in sm.get_matching_blocks():
            for q in range(blk.size):
                w = tx[blk.b + q]; txt[blk.a + q] = [w["start"], max(w["end"], w["start"] + 0.05)]
    bad = [times[k] is None for k in range(n)]
    for k in range(n):   # suspicious forced times: stacked (3+ tokens within 0.15 s) or stretched (> 3 s)
        if bad[k]: continue
        if times[k][1] - times[k][0] > 3.0: bad[k] = True
        stack = [q for q in range(max(0, k - 3), min(n, k + 4)) if times[q] and abs(times[q][0] - times[k][0]) < 0.15]
        if len(stack) >= 3: bad[k] = True
    last = -1.0
    for k in range(n):   # non-monotonic
        if bad[k]: continue
        if times[k][0] < last - 0.05: bad[k] = True; continue
        last = times[k][0]
    for k in range(n):   # the transcription rescues suspicious words it heard (only if it keeps order)
        if bad[k] and txt[k]:
            prev = max([times[q][0] for q in range(k) if not bad[q]] or [-1])
            nxt = min([times[q][0] for q in range(k + 1, n) if not bad[q]] or [1e9])
            if prev - 0.05 <= txt[k][0] <= nxt + 0.05: times[k] = list(txt[k]); bad[k] = False
    # 3) re-spread bad runs between good neighbours
    k = 0
    while k < n:
        if not bad[k]: k += 1; continue
        e = k
        while e < n and bad[e]: e += 1
        t0 = times[k - 1][1] if k > 0 else 0.0
        t1 = times[e][0] if e < n else t0 + 0.45 * (e - k)
        span = max(0.12 * (e - k), min(t1 - t0, 0.5 * (e - k)))
        st = t0 + 0.05   # the singer usually carries straight on after the last good word
        step = span / (e - k)
        for q in range(k, e): times[q] = [st + (q - k) * step, st + (q - k + 1) * step]
        k = e
    for k in range(n):   # cap word length (sustained notes) so lyrics never sit on screen for 10+ s
        times[k][1] = min(times[k][1], times[k][0] + 2.5)
        if k + 1 < n: times[k][1] = min(times[k][1], max(times[k][0] + 0.08, times[k + 1][0]))
    return times, sum(bad)


def build(song, aligned, tx, spec, ffmpeg="ffmpeg", who="host", who_map=None):
    who_map = who_map or spec.get("who_map", {})
    secs = lyric_sections(spec["lyrics"])
    tokens = [t for s in secs for ln in s["lines"] for t in ln]
    times, nbad = repair(tokens, aligned, tx)
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
