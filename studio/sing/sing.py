"""Sing-along song engine: turns lyrics + melody into a sung character vocal, a backing track and timing data.

python3 sing.py song.json outdir/
Writes outdir/song.wav (full mix), vocal.wav, backing.wav, timing.json (words, lines, beats, sections, mouth@24fps).

song.json:
{
  "bpm": 112, "voice": "af_heart", "formant": 1.12, "chords": "C G Am F", "style": "pop" | "lullaby" | "march",
  "intro_bars": 2, "outro_bars": 2,
  "parts": [
    {"section": "chorus", "who": "host", "group": true,              # group = kids-chorus doubling
     "lines": [ {"text": "Big red fire truck", "notes": "G4:1 G4:1 E4:.5,D4:.5 C4:1", "rest": 0} ]},
    {"section": "fact", "who": "host", "speak": "Fire trucks carry ladders and hoses.", "bars": 4}
  ]
}
notes: one token per word; "E4:.5,D4:.5" = melisma over one word; durations in beats. rest = beats of silence after line.
"""
import json, os, sys, re, hashlib
import numpy as np, soundfile as sf, pyworld as pw
from kokoro_onnx import Kokoro

SR = 24000
K = None
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")


def kokoro():
    global K
    if K is None:
        d = "/root/.cache/hyperframes/tts"
        K = Kokoro(f"{d}/models/kokoro-v1.0.onnx", f"{d}/voices/voices-v1.0.bin")
    return K


def say(text, voice, speed=1.0):
    os.makedirs(CACHE, exist_ok=True)
    h = hashlib.md5(f"{text}|{voice}|{speed}".encode()).hexdigest()[:16]
    p = f"{CACHE}/{h}.npy"
    if os.path.exists(p):
        return np.load(p)
    a, sr = kokoro().create(text, voice=voice, speed=speed, lang="en-gb" if voice.startswith("b") else "en-us")
    assert sr == SR
    a = trim(a.astype(np.float64))
    np.save(p, a)
    return a


def trim(a, th=0.01):
    idx = np.where(np.abs(a) > th)[0]
    if not len(idx):
        return a
    return a[max(0, idx[0] - 240): idx[-1] + 480]


NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def hz(n):
    m = re.match(r"([A-G])([#b]?)(\d)", n)
    s = NOTE[m.group(1)] + (1 if m.group(2) == "#" else -1 if m.group(2) == "b" else 0)
    midi = 12 * (int(m.group(3)) + 1) + s
    return 440 * 2 ** ((midi - 69) / 12), midi


def parse_notes(tok):
    out = []
    for n in tok.split(","):
        p, d = n.split(":")
        out.append((p, float(d)))
    return out


def sing_word(word, notes, beat, voice, formant, legato=0.92):
    """Speak the word, then stretch/pitch it onto its notes with the WORLD vocoder."""
    a = say(word, voice)
    f0, t = pw.harvest(a, SR, f0_floor=70, f0_ceil=700, frame_period=5.0)
    sp = pw.cheaptrick(a, f0, t, SR)
    ap = pw.d4c(a, f0, t, SR)
    n = len(f0)
    total = sum(d for _, d in notes) * beat
    tgt = max(4, int(total * legato / 0.005))
    voiced = np.where(f0 > 0)[0]
    if len(voiced) < 3:
        voiced = np.arange(n)
    v0, v1 = voiced[0], voiced[-1] + 1
    pre, post = v0, n - v1
    mid_t = tgt - pre - post
    if mid_t < (v1 - v0) * 0.5:  # too short: squeeze everything
        idx = np.linspace(0, n - 1, tgt)
    else:
        idx = np.concatenate([np.arange(pre), np.linspace(v0, v1 - 1, max(1, mid_t)), np.arange(v1, n)])
    ii = np.clip(np.round(idx).astype(int), 0, n - 1)
    sp2, ap2, vmask = sp[ii], ap[ii], f0[ii] > 0
    m = len(ii)
    # target pitch contour across the word's notes (voiced frames only)
    contour = np.zeros(m)
    edges = np.cumsum([0] + [d for _, d in notes]) / sum(d for _, d in notes) * m
    for k, (p, _) in enumerate(notes):
        contour[int(edges[k]):int(edges[k + 1])] = hz(p)[0]
    contour[int(edges[-2]):] = hz(notes[-1][0])[0]
    # portamento + vibrato
    lc = np.log(np.maximum(contour, 1))
    kern = np.hanning(9); kern /= kern.sum()
    lc = np.convolve(np.pad(lc, 4, mode="edge"), kern, mode="valid")
    tt = np.arange(m) * 0.005
    vib = 0.018 * np.sin(2 * np.pi * 5.6 * tt) * np.clip((tt - 0.22) / 0.2, 0, 1)
    f0n = np.exp(lc + vib) * vmask
    # cute-character formant shift: stretch the spectral envelope upward
    if formant != 1.0:
        fr = np.arange(sp2.shape[1])
        src = np.clip(fr / formant, 0, sp2.shape[1] - 1)
        sp2 = np.array([np.interp(src, fr, row) for row in sp2])
    y = pw.synthesize(f0n, np.ascontiguousarray(sp2), np.ascontiguousarray(ap2), SR, frame_period=5.0)
    fade = min(240, len(y) // 4)
    y[-fade:] *= np.linspace(1, 0, fade)
    return y


# ---------------------------------------------------------------- backing track
def osc(f, d, kind="tri", sr=SR):
    t = np.arange(int(d * sr)) / sr
    if kind == "sine":
        w = np.sin(2 * np.pi * f * t)
    elif kind == "square":
        w = np.sign(np.sin(2 * np.pi * f * t)) * 0.6
    elif kind == "saw":
        w = 2 * ((f * t) % 1) - 1
    else:
        w = 2 * np.abs(2 * ((f * t) % 1) - 1) - 1
    return w


def env(n, a=0.005, r=0.08, sr=SR):
    e = np.ones(n)
    na, nr = min(n, int(a * sr)), min(n, int(r * sr))
    e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


CHORD = {"": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11], "sus4": [0, 5, 7]}


def chord_notes(name):
    m = re.match(r"([A-G][#b]?)(.*)", name)
    _, root = hz(m.group(1) + "3")
    return root, [root + i for i in CHORD.get(m.group(2), CHORD[""])]


def mf(midi):
    return 440 * 2 ** ((midi - 69) / 12)


def add(buf, x, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    n = min(len(x), len(buf) - i)
    buf[i:i + n] += x[:n]


def backing(total_s, bpm, chords, style, melody_events, seed=1):
    rng = np.random.default_rng(seed)
    beat = 60 / bpm
    B = np.zeros(int((total_s + 2) * SR))
    ch = chords.split()
    nbeats = int(total_s / beat) + 1
    kick = osc(1, 0.25, "sine") * 0
    t = np.arange(int(0.25 * SR)) / SR
    kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 14)
    snare = (rng.standard_normal(int(0.18 * SR)) * np.exp(-np.arange(int(0.18 * SR)) / SR * 22)) * 0.5
    hat = rng.standard_normal(int(0.04 * SR)) * np.exp(-np.arange(int(0.04 * SR)) / SR * 90) * 0.18
    soft = style == "lullaby"
    for b in range(nbeats):
        at = b * beat
        bar, pos = divmod(b, 4)
        root, notes = chord_notes(ch[bar % len(ch)])
        if not soft:
            if pos in (0, 2):
                add(B, kick * 0.9, at)
            if pos in (1, 3):
                add(B, snare * (0.55 if style == "pop" else 0.4), at)
            add(B, hat, at); add(B, hat * 0.6, at + beat / 2)
            # bass: root on beats, octave bounce on offbeats
            bl = osc(mf(root - 12), beat * 0.45, "tri") * env(int(beat * 0.45 * SR), r=0.05) * 0.5
            add(B, bl, at)
            if pos in (1, 3):
                add(B, osc(mf(root), beat * 0.25, "tri") * env(int(beat * 0.25 * SR)) * 0.25, at + beat / 2)
            # bright plucked chord stabs on the offbeat
            for nn in notes:
                x = osc(mf(nn + 12), beat * 0.3, "saw") * env(int(beat * 0.3 * SR), r=0.12) * 0.045
                add(B, x, at + beat / 2)
        else:
            # lullaby: soft arpeggio (music box) + warm pad
            arp = [notes[0], notes[2], notes[1], notes[2]]
            for k in range(2):
                nn = arp[(pos * 2 + k) % 4]; d = beat / 2
                x = osc(mf(nn + 24), d * 3, "sine") * np.exp(-np.arange(int(d * 3 * SR)) / SR * 4) * 0.12
                add(B, x, at + k * d)
            if pos == 0:
                for nn in notes:
                    x = osc(mf(nn), beat * 4, "sine") * env(int(beat * 4 * SR), a=0.6, r=1.0) * 0.06
                    add(B, x, at)
    # melody doubled by a friendly bell/whistle lead so kids hear the tune
    for (at, d, f) in melody_events:
        n = int(d * 0.9 * SR)
        tt = np.arange(n) / SR
        x = (np.sin(2 * np.pi * f * 2 * tt) + 0.3 * np.sin(2 * np.pi * f * 4 * tt)) * np.exp(-tt * 3.5) * 0.07
        add(B, x, at)
    return B


# ---------------------------------------------------------------- main
def build(spec, outdir):
    os.makedirs(outdir, exist_ok=True)
    bpm = spec["bpm"]; beat = 60 / bpm
    voice = spec.get("voice", "af_heart"); formant = spec.get("formant", 1.1)
    t = spec.get("intro_bars", 2) * 4 * beat
    V = np.zeros(int(60 * 30 * SR)); G = np.zeros_like(V)
    words, lines, sections, mel = [], [], [], []
    for part in spec["parts"]:
        s0 = t
        who = part.get("who", "host")
        if "speak" in part:
            a = say(part["speak"], part.get("voice", spec.get("speak_voice", voice)), part.get("speed", spec.get("speak_speed", 0.95)))
            bars = part.get("bars") or int(np.ceil((len(a) / SR + 0.6) / (4 * beat)))
            add(V, a * 0.9, t + 0.15)
            lines.append({"text": part["speak"], "start": t + 0.15, "end": t + 0.15 + len(a) / SR, "who": who, "kind": "speak", "section": part["section"]})
            t += bars * 4 * beat
        else:
            for ln in part["lines"]:
                toks = ln["text"].split()
                nts = ln["notes"].split()
                assert len(toks) == len(nts), f"word/note count mismatch: {ln['text']} ({len(toks)} vs {len(nts)})"
                l0 = t
                for w, nt in zip(toks, nts):
                    notes = parse_notes(nt)
                    dur = sum(d for _, d in notes) * beat
                    clean = re.sub(r"[^A-Za-z']", "", w)
                    if clean and not nt.startswith("R"):
                        y = sing_word(clean, notes, beat, part.get("voice", voice), part.get("formant", formant))
                        add(V, y * 0.85, t)
                        if part.get("group"):
                            for k, (dt, st) in enumerate([(0.012, 1.004), (0.021, 0.996)]):
                                g = np.interp(np.arange(0, len(y), st), np.arange(len(y)), y)
                                add(G, g * 0.35, t + dt)
                        a2 = t
                        for p, d in notes:
                            mel.append((a2, d * beat, hz(p)[0])); a2 += d * beat
                        words.append({"w": w, "start": t, "end": t + dur * 0.92, "who": who})
                    t += dur
                t += ln.get("rest", 0) * beat
                lines.append({"text": ln["text"], "start": l0, "end": t, "who": who, "kind": "sing", "section": part["section"]})
            # snap section end to the bar
            bars_used = (t - s0) / (4 * beat)
            t = s0 + np.ceil(bars_used - 1e-6) * 4 * beat
        sections.append({"name": part["section"], "start": s0, "end": t, "who": who})
    t += spec.get("outro_bars", 2) * 4 * beat
    total = t
    vocal = (V + G)[: int(total * SR)]
    bk = backing(total, bpm, spec.get("chords", "C G Am F"), spec.get("style", "pop"), mel)[: int(total * SR)]
    # gentle compression-ish limiter on vocal, mix
    vocal = np.tanh(vocal * 1.6) / 1.6
    mix = vocal * 1.0 + bk * (0.55 if spec.get("style") == "lullaby" else 0.75)
    mix /= max(1e-6, np.abs(mix).max()) / 0.89
    sf.write(f"{outdir}/song.wav", mix, SR)
    sf.write(f"{outdir}/vocal.wav", vocal / max(1e-6, np.abs(vocal).max()) * 0.9, SR)
    sf.write(f"{outdir}/backing.wav", bk / max(1e-6, np.abs(bk).max()) * 0.9, SR)
    # mouth openness at 24 fps from the lead vocal envelope
    fps = 24; hop = SR // fps
    v = V[: int(total * SR)]
    mouth = [float(min(1, np.sqrt(np.mean(v[i:i + hop] ** 2)) * 9)) for i in range(0, len(v), hop)]
    beats = [round(i * beat, 4) for i in range(int(total / beat) + 1)]
    json.dump({"duration": total, "bpm": bpm, "beats": beats, "sections": sections, "lines": lines, "words": words, "mouth": mouth, "fps": fps},
              open(f"{outdir}/timing.json", "w"))
    print(f"song {total:.1f}s  {len(words)} sung words  {len(lines)} lines -> {outdir}")
    return total


if __name__ == "__main__":
    build(json.load(open(sys.argv[1])), sys.argv[2])
