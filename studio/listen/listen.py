#!/usr/bin/env python3
"""Machine listening for a finished sound or video file: what an ear would notice first, measured, plus a picture to LOOK at.

    python3 studio/listen/listen.py <file.wav|mp3|mp4> [--from 49 --to 60] [--key C] [--bpm 96] [--out dir] [--name label] [--music-only]
                                                                                   --music-only: the file has no speaking voice (a song's backing, a music track): judge everything
    python3 studio/listen/listen.py --episode <cartoon id> [--from .. --to ..]     the episode's MUSIC without the speaking voice (music bed, effects, hums and songs),
                                                                                   rebuilt from the engine: the exact way to check notes, clashes and the beat of our own videos

A speaking voice also holds tones (every long vowel) and is not in any key. In a finished mix the tool leaves out held tones that have two or more overtones
(voice-like) and anything shorter than 0.6 s, and judges only long, loud, pure tones (a beep, a held note); clashes are judged only with --episode. For our own cartoon videos --episode listens to the music alone
and every finding counts. Tested Nov 16: on two finished Shorts the first version called 13 spoken p/t/k sounds "clicks" and vowels "LOUD tones outside the key";
both were the voice. The click check now wants one single jump with a calm wave around it.

It writes <out>/<label>_listen.json and <out>/<label>_listen.png and prints the findings. It does not judge taste: whether a tune is
pretty or a voice is warm stays with a person. What it does find:
  notes       every held tone (a quarter second or longer): when, which note, how many cents off, how loud; overtones of a louder tone are left out
  key         the key the tones fit best, and every held tone that is NOT in the expected key (--key), with its time
  clashes     two held tones a semitone apart sounding together
  beat        the tempo the sound has, and how much of its attacks fall on the grid of the expected tempo (--bpm)
  clicks      jumps in the wave that a speaker plays as a click (hard cuts)
  silence     stretches with no sound at all
  level       programme loudness (LUFS), loudness range, true peak, clipped samples, the quietest and loudest second
  balance     how much of the sound a phone speaker plays (above 300 Hz), and how much is low rumble
The picture has the spectrogram (time left to right, pitch bottom to top, C notes marked, held tones outside the key boxed in red),
the twelve pitch classes over time, and the loudness curve with clicks and silences marked. Open it and look."""
import sys, os, json, re, subprocess
import numpy as np

SR = 24000; N = 4096; HOP = 1024
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MAJOR = [0, 2, 4, 5, 7, 9, 11]; MINOR = [0, 2, 3, 5, 7, 8, 10]
KS_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]); KS_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def arg(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


def load(path, a=None, b=None):
    cmd = ["ffmpeg", "-loglevel", "error"] + (["-ss", str(a)] if a is not None else []) + (["-to", str(b)] if b is not None else []) + ["-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).astype(np.float64)


def stft(x):
    w = np.hanning(N); n = 1 + max(0, (len(x) - N) // HOP); idx = np.arange(N)[None, :] + HOP * np.arange(n)[:, None]
    return np.abs(np.fft.rfft(x[idx] * w, axis=1)), np.fft.rfftfreq(N, 1 / SR)


def midi(f): return 69 + 12 * np.log2(np.maximum(f, 1e-9) / 440.0)


def note_name(m): m = int(round(m)); return f"{NAMES[m % 12]}{m // 12 - 1}"


def held_tones(S, fr, lo=70, hi=2100, min_s=0.25):
    """Peaks of the spectrum that stay on the same pitch for a quarter second or longer."""
    T, F = S.shape; b0, b1 = np.searchsorted(fr, lo), np.searchsorted(fr, hi); ref = np.percentile(S[:, b0:b1].max(1), 95) + 1e-12
    live = {}; out = []
    for t in range(T):
        row = S[t]; pk = [k for k in range(max(b0, 2), b1) if row[k] > row[k - 1] and row[k] >= row[k + 1] and row[k] > ref * 10 ** (-38 / 20) and row[k] > 0.12 * row[b0:b1].max()]
        nxt = {}
        for k in pk:
            y0, y1, y2 = np.log(row[k - 1] + 1e-12), np.log(row[k] + 1e-12), np.log(row[k + 1] + 1e-12); d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12); f = (k + d) * SR / N
            prev = next((live[j] for j in (k, k - 1, k + 1) if j in live and abs(1200 * np.log2(f / live[j]["f"][-1])) < 45), None)
            if prev is None: prev = {"t0": t, "f": [], "a": []}
            prev["f"].append(f); prev["a"].append(row[k]); nxt[k] = prev
        for j, tr in live.items():
            if not any(tr is v for v in nxt.values()): out.append(tr)
        live = nxt
    out += list({id(v): v for v in live.values()}.values()); tones = []
    for tr in out:
        d = len(tr["f"]) * HOP / SR
        if d < min_s: continue
        f = float(np.median(tr["f"])); m = midi(f); spread = float(np.percentile(1200 * np.log2(np.array(tr["f"]) / f), 90) - np.percentile(1200 * np.log2(np.array(tr["f"]) / f), 10))
        if spread > 60: continue        # a glide (speech), not a held tone
        tones.append({"start": round(tr["t0"] * HOP / SR, 2), "seconds": round(d, 2), "hz": round(f, 1), "note": note_name(m), "pc": int(round(m)) % 12, "cents": int(round(100 * (m - round(m)))),
                      "db": round(20 * np.log10(float(np.median(tr["a"])) / ref), 1)})
    tones.sort(key=lambda z: z["start"])
    for a in tones:                      # an overtone of a louder tone that sounds at the same time is not a note of its own
        a["overtone_of"] = None
        for b in tones:
            if b is a or b["hz"] >= a["hz"] * 0.97: continue
            ov = min(a["start"] + a["seconds"], b["start"] + b["seconds"]) - max(a["start"], b["start"])
            if ov < 0.6 * a["seconds"]: continue
            k = a["hz"] / b["hz"]
            if 1.9 < k < 12.5 and abs(1200 * np.log2(k / round(k))) < 28 and b["db"] > a["db"] - 4: a["overtone_of"] = b["note"]; b["overtones"] = b.get("overtones", 0) + 1; break
    return tones


def best_key(tones):
    ch = np.zeros(12)
    for z in tones:
        if not z["overtone_of"]: ch[z["pc"]] += z["seconds"] * 10 ** (z["db"] / 20)
    if ch.sum() == 0: return None, ch
    best = max(((np.corrcoef(np.roll(p, k), ch)[0, 1], f"{NAMES[k]} {nm}") for k in range(12) for p, nm in ((KS_MAJ, "major"), (KS_MIN, "minor"))), key=lambda z: z[0])
    return {"key": best[1], "fit": round(float(best[0]), 2)}, ch


def scale_of(key):
    m = re.match(r"([A-G]#?)(m|\s*minor)?", key.strip()); root = NAMES.index(m.group(1)); return {(root + i) % 12 for i in (MINOR if m.group(2) else MAJOR)}


def tempo(S, bpm=None):
    flux = np.maximum(0, np.diff(np.log1p(30 * S), axis=0)).sum(1); flux = flux - np.convolve(flux, np.ones(43) / 43, "same"); flux = np.maximum(0, flux); fps = SR / HOP
    if flux.sum() == 0: return {"heard_bpm": None}
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]; lags = np.arange(len(ac)); ok = (lags > fps * 60 / 200) & (lags < fps * 60 / 55); out = {}
    if ok.any():
        l = lags[ok][np.argmax(ac[ok])]; y0, y1, y2 = ac[l - 1], ac[l], ac[l + 1]; l = l + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12); out["heard_bpm"] = round(60 * fps / l, 1)
    if bpm:
        g = 60 / bpm / 2 * fps; best = 0     # the half-beat grid: which phase catches the most attacks, and how much of all attacks that is (within 45 ms)
        tol = 0.045 * fps; idx = np.arange(len(flux))
        for ph in np.linspace(0, g, 24, endpoint=False):
            dist = np.abs((idx - ph + g / 2) % g - g / 2); best = max(best, float(flux[dist <= tol].sum() / flux.sum()))
        out.update(expected_bpm=bpm, attacks_on_the_half_beat_grid=round(best, 2), by_chance=round(2 * tol / g, 2))
        if out.get("heard_bpm"): r = out["heard_bpm"] / bpm; out["heard_against_expected"] = round(min((r / k for k in (0.5, 1, 2, 1.5, 0.75)), key=lambda q: abs(q - 1)), 3)
    return out


def clicks(x):
    """A click is ONE jump in the wave with a calm wave right before and after it (a hard cut). A spoken p, t or k is a burst of many jumps: not a click."""
    d = np.abs(np.diff(x)); cand = np.where(d > 0.1)[0]; out = []
    for i in cand:
        near = np.concatenate([d[max(0, i - 72):max(0, i - 1)], d[i + 2:i + 73]])
        if len(near) and (near > 0.35 * d[i]).sum() <= 1 and d[i] > 12 * (np.median(near) + 1e-4) and (not out or i - out[-1] > SR * 0.05): out.append(int(i))
    return [round(i / SR, 3) for i in out]


def silences(x, min_s=1.5):
    w = int(SR * 0.05); r = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, "same")); q = r < 10 ** (-60 / 20); out = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) / SR >= min_s: out.append([round(i / SR, 2), round(j / SR, 2)])
            i = j
        else: i += 1
    return out


def loudness(path, a, b):
    cmd = ["ffmpeg", "-hide_banner", "-nostats"] + (["-ss", str(a)] if a is not None else []) + (["-to", str(b)] if b is not None else []) + ["-i", path, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]
    e = subprocess.run(cmd, capture_output=True, text=True).stderr; g = lambda p: (float(re.findall(p, e)[-1]) if re.findall(p, e) else None)
    return {"lufs": g(r"I:\s+(-?[\d.]+) LUFS"), "range_lu": g(r"LRA:\s+(-?[\d.]+) LU"), "true_peak_db": g(r"Peak:\s+(-?[\d.]+) dBFS")}


def picture(x, S, fr, tones, bad, clk, sil, out, title, scale):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    T = S.shape[0]; dur = len(x) / SR; fig, ax = plt.subplots(3, 1, figsize=(18, 11), gridspec_kw={"height_ratios": [5, 2, 1.6]}); fig.suptitle(title, fontsize=13)
    b0, b1 = np.searchsorted(fr, 60), np.searchsorted(fr, 8000); D = 20 * np.log10(S[:, b0:b1].T + 1e-9); D -= D.max()
    ax[0].pcolormesh(np.arange(T) * HOP / SR, fr[b0:b1], D, vmin=-70, vmax=0, cmap="magma", shading="auto"); ax[0].set_yscale("log"); ax[0].set_ylabel("pitch (C notes marked)")
    cs = [(f"C{o}", 440 * 2 ** ((12 * (o + 1) - 69) / 12)) for o in range(2, 9)]; ax[0].set_yticks([f for _, f in cs]); ax[0].set_yticklabels([n for n, _ in cs]); ax[0].set_ylim(60, 8000)
    for z in tones:
        if z["overtone_of"]: continue
        red = z in bad; ax[0].plot([z["start"], z["start"] + z["seconds"]], [z["hz"], z["hz"]], color="red" if red else "#7CFC9A", lw=2.2 if red else 1.2)
        if red: ax[0].text(z["start"], z["hz"] * 1.08, z["note"], color="red", fontsize=10, weight="bold")
    ch = np.zeros((12, T)); pcs = np.round(midi(fr[b0:np.searchsorted(fr, 2100)])).astype(int) % 12
    for p in range(12): ch[p] = (S[:, b0:np.searchsorted(fr, 2100)][:, pcs == p] ** 2).sum(1)
    ch /= ch.max(0, keepdims=True) + 1e-12
    ax[1].imshow(ch, aspect="auto", origin="lower", cmap="viridis", extent=[0, dur, -0.5, 11.5], interpolation="nearest"); ax[1].set_yticks(range(12))
    ax[1].set_yticklabels([n + ("" if (scale is None or k in scale) else "  (not in key)") for k, n in enumerate(NAMES)], fontsize=8); ax[1].set_ylabel("pitch classes")
    w = int(SR * 0.4); r = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(w) / w, "same")) + 1e-9); ax[2].plot(np.arange(len(x)) / SR, r, color="#2a6", lw=0.8); ax[2].set_ylim(-70, 0); ax[2].set_ylabel("level dBFS")
    for c in clk: ax[2].axvline(c, color="red", lw=1)
    for a, b in sil: ax[2].axvspan(a, b, color="orange", alpha=0.4)
    for q in ax: q.set_xlim(0, dur)
    ax[2].set_xlabel("seconds   (red line: click, orange: silence)"); fig.tight_layout(); fig.savefig(out, dpi=100); plt.close(fig)


def listen(path, a=None, b=None, key=None, bpm=None, out=None, name=None, music_only=False):
    """music_only: the file has no speaking voice (an episode's music stem): every held tone is judged.
    Otherwise a held tone with two or more overtones is taken as a VOICE (a long vowel has many overtones; the plucked and bell notes of the music have one)
    and is counted, not judged: a speaking voice is not in any key."""
    x = load(path, a, b); S, fr = stft(x); tones = held_tones(S, fr); every = [z for z in tones if not z["overtone_of"]]; heard, _ = best_key([z for z in tones if music_only or z.get("overtones", 0) < 2])
    # with a speaking voice in the file only a LONG, LOUD, PURE tone is judged (a beep or a held instrument note): vowels are shorter and rich in overtones.
    # Tested Nov 16 on two narrated Shorts: judging every held tone gave dozens of false "wrong notes" and "clashes", all of them the voice.
    own = [z for z in every if music_only or (z["seconds"] >= 0.6 and z.get("overtones", 0) <= 1)]; voice_like = len(every) - len(own)
    scale = scale_of(key) if key else (scale_of(heard["key"].replace(" major", "").replace(" minor", "m")) if heard else None)
    loud = max([z["db"] for z in own] or [0]); bad = [z for z in own if scale is not None and z["pc"] not in scale and abs(z["cents"]) <= 35 and z["db"] > loud - 26]
    if not music_only: bad = [z for z in bad if z["db"] > -12]
    sour = [z for z in own if abs(z["cents"]) > 35 and z["db"] > loud - 20]; cl = []
    for i, p in enumerate(own if music_only else []):
        for q in own[i + 1:]:
            ov = min(p["start"] + p["seconds"], q["start"] + q["seconds"]) - max(p["start"], q["start"])
            if ov >= 0.2 and (p["pc"] - q["pc"]) % 12 in (1, 11) and abs(p["db"] - q["db"]) < 15 and max(p["db"], q["db"]) > loud - 24:
                cl.append({"at": round(max(p["start"], q["start"]), 2), "seconds": round(ov, 2), "notes": f'{p["note"]} + {q["note"]}'})
    clk = clicks(x) if music_only else []; sil = silences(x)      # a spoken s, t or k makes the same single jumps as a click at this sample rate (tested Nov 16): clicks are judged only without a speaking voice; lv = loudness(path, a, b); P = np.abs(np.fft.rfft(x)) ** 2; ff = np.fft.rfftfreq(len(x), 1 / SR); tot = P[ff > 30].sum() + 1e-12
    lv = loudness(path, a, b); P = np.abs(np.fft.rfft(x)) ** 2; ff = np.fft.rfftfreq(len(x), 1 / SR); tot = P[ff > 30].sum() + 1e-12
    w = SR; sec = [20 * np.log10(np.sqrt(np.mean(x[i:i + w] ** 2)) + 1e-9) for i in range(0, max(1, len(x) - w + 1), w)]
    rep = {"file": path, "from": a, "to": b, "seconds": round(len(x) / SR, 2), "expected_key": key, "key_heard": heard,
           "held_tones": len(own), "voice_like_tones_not_judged": voice_like, "tones_outside_the_key": [{k: z[k] for k in ("start", "seconds", "note", "hz", "db")} for z in bad],
           "tones_between_two_notes": [{k: z[k] for k in ("start", "seconds", "note", "cents", "db")} for z in sour], "clashes_a_semitone_apart": cl,
           "beat": tempo(S, bpm), "clicks_at": clk, "silences": sil,
           "judged": "everything (no speaking voice in the file)" if music_only else "level, silences, tempo, balance, and long loud pure tones only; NOT judged because a voice is speaking: short tones, clashes, clicks (use --episode, or --music-only for a file without speech)",
           "level": dict(lv, clipped_samples=int((np.abs(x) >= 0.999).sum()), quietest_second_db=round(min(sec), 1), loudest_second_db=round(max(sec), 1)),
           "balance": {"share_a_phone_speaker_plays_above_300hz": round(float(P[ff > 300].sum() / tot), 2), "share_below_120hz": round(float(P[(ff > 30) & (ff < 120)].sum() / tot), 2), "share_above_4khz": round(float(P[ff > 4000].sum() / tot), 2)},
           "tones": [{k: z[k] for k in ("start", "seconds", "note", "cents", "db")} for z in own][:400],
           "not_judged": "whether it sounds pleasant, whether a voice is warm or a word is said right: a person listens for that"}
    name = name or os.path.splitext(os.path.basename(path))[0] + (f"_{a}-{b}" if a is not None else ""); out = out or os.path.dirname(os.path.abspath(path)); os.makedirs(out, exist_ok=True)
    rep["picture"] = os.path.join(out, name + "_listen.png"); json.dump(rep, open(os.path.join(out, name + "_listen.json"), "w"), indent=1)
    picture(x, S, fr, tones, bad, clk, sil, rep["picture"], f"{os.path.basename(path)}  {a if a is not None else 0}-{b if b is not None else round(len(x) / SR, 1)} s   key heard: {heard and heard['key']}   expected: {key}", scale)
    return rep


def episode_stem(eid, out):
    """The music of a cartoon episode without the speaking voice: toon.py's own bed (music + effects) plus the sung and hummed shots."""
    import importlib, soundfile as sf
    here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(here), "cartoon")); import toon
    mod = importlib.import_module("episodes." + eid); ep = dict(mod.EP, beat=True) if os.environ.get("TOON_BEAT") else mod.EP; shots = [dict(s) for s in mod.SHOTS]
    total, _, _ = toon.voice_lines(ep, shots); total += ep.get("tail", 0.6); shots[0]["t0"] = 0.0
    film = toon.Film(ep, mod.STAGES, shots, False); film.build_html(total, None); voice, bed = toon.mix_parts(film, total, ep); stem = bed.copy()
    for s in shots:
        if s.get("sung"): a0 = int(s["v0"] * toon.SR); stem[a0:a0 + len(s["audio"])] += s["audio"][:len(stem) - a0] * 0.95
    os.makedirs(out, exist_ok=True); p = os.path.join(out, eid + "_music_stem.wav"); sf.write(p, stem, toon.SR)
    return p, [(round(s["v0"], 2), round(s["v0"] + s["dur"], 2), s["tag"]) for s in shots if s.get("sung")], toon.BPM


def main():
    f = lambda v: float(v) if v is not None else None; sung = []
    if "--episode" in sys.argv:
        out = arg("--out") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); path, sung, bpm = episode_stem(arg("--episode"), out)
        r = listen(path, f(arg("--from")), f(arg("--to")), arg("--key", "C"), f(arg("--bpm", bpm)), out, arg("--name"), music_only=True)
        for a, b, tag in sung: print(f'  sung or hummed: {tag}  {a}-{b} s: ' + " ".join(z["note"] + (f'({z["cents"]:+d}c)' if abs(z["cents"]) > 12 else "") for z in r["tones"] if a - 0.1 <= z["start"] + (r["from"] or 0) < b and z["db"] > -14))
    else: r = listen(sys.argv[1], f(arg("--from")), f(arg("--to")), arg("--key"), f(arg("--bpm")), arg("--out"), arg("--name"), music_only="--music-only" in sys.argv)
    print("  judged:", r["judged"])
    print(f'{r["seconds"]} s   key heard: {r["key_heard"]}   expected: {r["expected_key"]}   held tones judged: {r["held_tones"]}   voice-like tones left out: {r["voice_like_tones_not_judged"]}')
    for z in r["tones_outside_the_key"]: print(f'  OUTSIDE THE KEY  {z["start"]:7.2f} s  {z["note"]:4s} for {z["seconds"]} s  ({z["db"]} dB, {"LOUD" if z["db"] > -12 else "faint"})')
    for z in r["clashes_a_semitone_apart"]: print(f'  CLASH            {z["at"]:7.2f} s  {z["notes"]} together for {z["seconds"]} s')
    for z in r["tones_between_two_notes"][:12]: print(f'  BETWEEN NOTES    {z["start"]:7.2f} s  {z["note"]} {z["cents"]:+d} cents for {z["seconds"]} s')
    print("  beat:", r["beat"]); print("  clicks at:", r["clicks_at"][:20], " silences:", r["silences"][:10]); print("  level:", r["level"]); print("  balance:", r["balance"]); print("  picture:", r["picture"])


if __name__ == "__main__":
    main()
