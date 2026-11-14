"""Teaching lessons for The Animated Zoo (Noelson, Nov 14, 2026: "not only music but teaching lessons as well").
A lesson is a narrated 4:30-6:30 episode (rulebook KID-04): Milo talks to the viewer, each animal gets its own scene
in its own place, one true fact at a time, with a question, an action to copy and a recap quiz at the end.

  python3 lesson.py lessons/<id>.json
     -> jobs/<id>_song.wav (Milo's voice over soft music), jobs/<id>_timing.json, jobs/<id>.json (zooworld scenes),
        songs/<id>.json (meta for finish.py). Then: variety check + record, 2 test stills, copy the 3 job files to the PC.

Spec: {"id", "title" (<=60), "card", "thumb_text", "description", "tags", "voice": "af_heart", "speed": 0.9,
       "cast": [animal kinds], "segments": [{"name": "panda", "biome", "tod", "show": [ids] (omit = everyone),
       "formation", "energy", "word": "BAMBOO!" (3D word that pops in), "lines": ["sentence", ...]}], "facts": [...]}
Voice: Kokoro (same engine as the old narrated videos), slowed for little listeners. Music: gentle, ducked under the voice.
"""
import json, os, sys, re
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "sing"))
import sing

SR, FPS, BPM = sing.SR, 24, 96
GAP, SEG_GAP, LEAD = 0.8, 1.4, 0.5
THINK, DO = 2.0, 2.6     # quiet time after a question / after "Can you ...?" so little viewers can answer and copy
BOILER = ("The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
          "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.")
SPOTS = [("s1", 0.22), ("s2", -0.22), ("s3", 0.38), ("s4", -0.38), ("s5", -0.1), ("s6", 0.1)]
COLORS = ["#ffb627", "#3db8ff", "#ff7a00", "#8e5bd8", "#3cc45a", "#ff6fb5"]


def pluck(f, d, amp=0.16):
    t = np.arange(int(SR * d)) / SR
    return (amp * np.exp(-t * 3.2) * (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t))).astype(np.float64)


def music(total):
    """Soft ukulele-like arpeggio, C - G - Am - F, at BPM (half-beat steps)."""
    chords = [[261.6, 329.6, 392.0, 523.3], [196.0, 293.7, 392.0, 493.9], [220.0, 261.6, 329.6, 440.0], [174.6, 261.6, 349.2, 440.0]]
    step = 60 / BPM / 2; out = np.zeros(int(SR * (total + 2))); i, t = 0, 0.0
    while t < total:
        ch = chords[(i // 8) % 4]; n = pluck(ch[[0, 2, 1, 3, 2, 1, 3, 2][i % 8]], 0.9)
        s = int(t * SR); out[s:s + len(n)] += n[:len(out) - s]
        if i % 8 == 0:
            b = pluck(ch[0] / 2, 1.6, 0.2); out[s:s + len(b)] += b[:len(out) - s]
        i += 1; t += step
    return out[:int(SR * total)]


def build(spec):
    sid = spec["id"]; voice = spec.get("voice", "af_heart"); speed = spec.get("speed", 0.82)
    assert len(spec["title"]) <= 60, "title over 60 characters"
    t = LEAD; sections, lines, words, clips = [], [], [], []
    for seg in spec["segments"]:
        sec = {"name": seg["name"], "start": t if sections else 0.0, "who": "host"}
        for text in seg["lines"]:
            a = sing.say(text, voice, speed); d = len(a) / SR
            clips.append((t, a)); lines.append({"text": text, "start": round(t, 3), "end": round(t + d, 3), "who": "host", "kind": "say", "section": seg["name"]})
            toks = text.split(); tot = sum(len(re.sub(r"\W", "", w)) + 1.5 for w in toks); c = t
            for w in toks:
                wd = d * (len(re.sub(r"\W", "", w)) + 1.5) / tot
                words.append({"w": w, "start": round(c, 3), "end": round(c + wd, 3), "who": "host"}); c += wd
            t += d + GAP + (DO if text.lower().startswith("can you") else (THINK if text.rstrip().endswith("?") else 0))
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
    mus = music(dur) * (0.55 - 0.38 * env)          # duck the music under the voice
    fade = np.minimum(1, np.minimum(np.arange(n) / (SR * 0.5), (n - np.arange(n)) / (SR * 1.5)))
    mix = (vox * 0.95 + mus) * fade; mix = mix / max(1e-6, np.abs(mix).max()) * 0.89
    sf.write(os.path.join(HERE, "jobs", f"{sid}_song.wav"), mix.astype(np.float32), SR)
    # mouth: voice loudness per video frame, 0..1
    hop = SR // FPS; nf = int(np.ceil(dur * FPS)); mouth = []
    for f in range(nf):
        x = vox[f * hop:(f + 1) * hop]; mouth.append(float(np.sqrt(np.mean(x ** 2))) if len(x) else 0.0)
    mx = max(mouth) or 1.0; mouth = [round(min(1.0, (m / mx) * 2.2) ** 0.7, 3) for m in mouth]
    bl = 60 / BPM
    timing = {"duration": dur, "bpm": BPM, "beats": [round(i * bl, 4) for i in range(int(dur / bl) + 1)], "sections": sections,
              "lines": lines, "words": words, "mouth": mouth, "fps": FPS, "repaired_words": 0, "kind": "lesson"}
    json.dump(timing, open(os.path.join(HERE, "jobs", f"{sid}_timing.json"), "w"))

    cast = [{"id": "host", "char": "milo", "spot": "center"}]
    for i, kind in enumerate(spec["cast"]):
        cast.append({"id": kind, "char": "animal", "spot": SPOTS[i][0], "opts": {"kind": kind}, "yaw": SPOTS[i][1]})
    locs, direct = [], []
    for i, seg in enumerate(spec["segments"]):
        show = seg.get("show")
        lc = {"from": seg["name"], "biome": seg["biome"], "tod": seg.get("tod", "noon"),
              "formation": seg.get("formation", ("host_left", "host_right")[i % 2] if show else ("line", "arc", "v")[i % 3]),
              "shot": seg.get("shot", ("dolly", "side", "reveal", "vista")[i % 4])}
        if show: lc["show"] = show
        locs.append(lc)
        if show:
            shots = []
            for k in range(len(seg["lines"])):
                shots.append(("close:" + show[k % len(show)], "wide", "close:host", "dolly", "close:" + show[0], "side", "low", "orbit")[k % 8])
        else:
            shots = ["wide", "close:host", "orbit", "low", "vista", "close:host", "high", "dolly"]
        d = {"section": seg["name"], "shots": shots, "energy": seg.get("energy", 0.5 if show else 0.75), "wave": 0 if show else 1,
             "jump": 0.1 if show else 0.25, "group": False, "props": []}
        if seg.get("word"):
            d["props"].append({"type": "text", "text": seg["word"], "color": COLORS[i % len(COLORS)], "at": "top", "size": 0.7, "delay": 1.0})
        direct.append(d)
    job = {"id": sid, "title": spec.get("card", spec["title"]), "channel": "zoo", "set": "zooworld", "set_opts": {}, "seed": spec.get("seed", 5),
           "new_song": True, "kind": "lesson", "cast": cast, "locations": locs, "intro_shot": "reveal", "intro": {"energy": 0.6, "wave": 1},
           "thumb_frame": spec.get("thumb_frame", 72), "direct": direct, "song": sid, "res": "1920x1080", "step": 1,
           "cut_mode": "beat", "follow_singer": False, "punch": False,
           "timing_file": f"{sid}_timing.json", "audio": f"{sid}_song.wav"}
    json.dump(job, open(os.path.join(HERE, "jobs", f"{sid}.json"), "w"), indent=1)
    song = {"kind": "lesson", "format": "3d_lesson", "desc_header": "IN THIS LESSON", "lyrics": "\n".join(spec.get("facts", [])),
            "script": "\n".join(l["text"] for l in lines), "duration": dur, "bpm": BPM,
            "meta": {"title": spec["title"], "card": spec.get("card", spec["title"]), "thumb_text": spec.get("thumb_text", ""),
                     "description": spec["description"].rstrip() + "\n\n" + BOILER, "tags": spec.get("tags", [])}, "job": job}
    json.dump(song, open(os.path.join(HERE, "songs", f"{sid}.json"), "w"), indent=1)
    print(f"OK {sid}: {dur:.0f} s ({int(dur // 60)}:{int(dur % 60):02d}), {wc} words, {len(lines)} lines, {len(locs)} scenes")
    return job


if __name__ == "__main__":
    build(json.load(open(sys.argv[1])))
