"""Turn an ACE-Step song + aligned words into the engine's timing.json (same format sing.py writes).

python3 build_timing.py <song.mp3> <words.json> <song.json(spec with lyrics,bpm)> <out_timing.json> [--who host]
Sections come from the [Tag] headers in the lyrics, renamed uniquely: chorus1, verse1, chorus2, bridge1, outro1 ...
Mouth = song loudness inside each sung word (fast open, softer close, 1-frame lead), 0 between words.
"""
import json, re, sys, subprocess
import numpy as np

song, wordsp, specp, outp = sys.argv[1:5]
who = sys.argv[sys.argv.index("--who") + 1] if "--who" in sys.argv else "host"
spec = json.load(open(specp)); aw = json.load(open(wordsp))
words_al = aw["words"]
norm = lambda s: re.sub(r"[^a-z']", "", s.lower())

# lyrics -> sections of lines of tokens
secs, counts = [], {}
for raw in spec["lyrics"].splitlines():
    l = raw.strip()
    if not l: continue
    m = re.match(r"^\[(.+?)\]$", l)
    if m:
        base = re.sub(r"[^a-z]", "", m.group(1).lower().split()[0]) or "part"
        base = {"finalchorus": "chorus", "final": "chorus", "break": "action", "prechorus": "prechorus"}.get(base, base)
        counts[base] = counts.get(base, 0) + 1
        secs.append({"name": f"{base}{counts[base]}", "lines": []}); continue
    if not secs: secs.append({"name": "verse1", "lines": []}); counts["verse"] = 1
    secs[-1]["lines"].append([t for t in l.split() if norm(t)])

# walk aligned words in order, matching lyric tokens (tolerant of small alignment differences)
i = 0; words, lines, sections = [], [], []
for s in secs:
    s0 = None
    for toks in s["lines"]:
        lw = []
        for t in toks:
            j = i
            while j < min(i + 4, len(words_al)) and norm(words_al[j]["w"]) != norm(t): j += 1
            if j >= len(words_al) or j >= i + 4: j = i
            if j < len(words_al):
                a = words_al[j]; lw.append({"w": t, "start": a["start"], "end": max(a["end"], a["start"] + 0.08), "who": who}); i = j + 1
        if not lw: continue
        words += lw
        lines.append({"text": " ".join(toks), "start": lw[0]["start"], "end": lw[-1]["end"], "who": who, "kind": "sing", "section": s["name"]})
        s0 = lw[0]["start"] if s0 is None else s0
    if s0 is not None: sections.append({"name": s["name"], "start": s0, "who": who})

# audio -> loudness per frame
fps = 24
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", song, "-ac", "1", "-ar", "24000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(pcm, dtype=np.float32); sr = 24000; dur = len(a) / sr
hop = sr // fps
rms = np.array([np.sqrt(np.mean(a[k:k + hop] ** 2)) for k in range(0, len(a), hop)])
ref = np.percentile(rms[rms > 1e-4], 95) if (rms > 1e-4).any() else 1
gate = np.zeros_like(rms)
for w in words:
    gate[int(max(0, w["start"] - 0.03) * fps): int(w["end"] * fps) + 1] = 1
m = np.clip(rms / ref, 0, 1) * gate
out, cur = np.zeros_like(m), 0.0
for k, x in enumerate(m):
    cur = x if x > cur else cur * 0.55 + x * 0.45; out[k] = cur
mouth = [round(float(x), 3) for x in np.concatenate([out[1:], [0.0]])]

# section boundaries: start a beat early, end where the next starts
bpm = spec.get("bpm", 116); beat = 60 / bpm
for k, s in enumerate(sections):
    s["start"] = max(0.0, s["start"] - beat * 0.5) if k else 0.0
    s["end"] = sections[k + 1]["start"] - beat * 0.5 if k + 1 < len(sections) else dur
    s["end"] = max(s["end"], s["start"] + 0.5)
sections[-1]["end"] = dur
json.dump({"duration": dur, "bpm": bpm, "beats": [round(k * beat, 4) for k in range(int(dur / beat) + 1)], "sections": sections,
           "lines": lines, "words": words, "mouth": mouth, "fps": fps}, open(outp, "w"))
print(f"timing: {dur:.1f}s, {len(sections)} sections, {len(lines)} lines, {len(words)}/{len(words_al)} words matched")
