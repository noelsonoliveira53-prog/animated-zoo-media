"""Word-level sync for narrated lessons (Noelson, Nov 14 2026: "all words in sync").
Every spoken line is force-aligned against its own audio with an acoustic model (PocketSphinx, bundled US-English model,
no network needed), so each word's start/end comes from the sound itself, not from an estimate by word length.
teach.py uses these times for the karaoke captions, for every prop that appears "on a word" (counting 1-2-3, answer signs,
examples) and for the Shorts captions.

  align(audio_24k_float, text) -> ([(start, end) per whitespace token, seconds from the clip start], n_aligned)
A token the model cannot place keeps an interpolated time between its aligned neighbours and is reported as not aligned.
pip install pocketsphinx (setup.sh does it).
"""
import re, os
import numpy as np

_DEC = [None]
NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"}
# words the bundled dictionary does not know (names, animal sounds): ARPAbet
EXTRA = {"milo": "M AY L OW", "milo's": "M AY L OW Z", "joey": "JH OW IY", "clop": "K L AA P", "oink": "OY NG K", "brrr": "B ER", "rawr": "R AO R",
         "koala": "K OW AA L AH", "koala's": "K OW AA L AH Z", "koalas": "K OW AA L AH Z", "stripy": "S T R AY P IY", "squishy": "S K W IH SH IY",
         "spotty": "S P AA T IY", "bluebird": "B L UW B ER D", "zzz": "Z IY", "shh": "SH", "ahh": "AA", "moo": "M UW", "munches": "M AH N CH IH Z",
         "snooze": "S N UW Z", "sunscreen": "S AH N S K R IY N", "sunburn": "S AH N B ER N", "panda's": "P AE N D AH Z", "zebra's": "Z IY B R AH Z",
         "giraffe's": "JH ER AE F S", "tiger's": "T AY G ER Z", "hippo's": "HH IH P OW Z", "lion's": "L AY AH N Z", "elephant's": "EH L AH F AH N T S",
         "bear's": "B EH R Z", "cow's": "K AW Z", "pig's": "P IH G Z", "monkey's": "M AH NG K IY Z", "fox's": "F AA K S IH Z", "mama's": "M AA M AH Z"}
L2P = {"a": "AE", "b": "B", "c": "K", "d": "D", "e": "EH", "f": "F", "g": "G", "h": "HH", "i": "IH", "j": "JH", "k": "K", "l": "L", "m": "M", "n": "N",
       "o": "AA", "p": "P", "q": "K", "r": "R", "s": "S", "t": "T", "u": "AH", "v": "V", "w": "W", "x": "K S", "y": "IY", "z": "Z"}


def _dec():
    if _DEC[0] is None:
        from pocketsphinx import Decoder
        _DEC[0] = Decoder(samprate=16000, loglevel="FATAL", beam=1e-80, wbeam=1e-60, pbeam=1e-80)
    return _DEC[0]


# what the voice is asked to SAY for spellings it would read out letter by letter (checked Nov 14: Kokoro read "Shh." as
# "S H H" and "Brrr" as "B R R R"). The caption keeps the written form.
SAY = {"brrr": "burr", "shh": "shush", "rawr": "roar", "ahh": "ah", "zzz": "snore", "mmm": "yum", "hmm": "hum", "grr": "growl", "psst": "hey"}


def spoken(text):
    out = []
    for tok in text.split():
        core = re.sub(r"[^A-Za-z']", "", tok)
        rep_ = SAY.get(core.lower())
        if rep_: tok = tok.replace(core, rep_.capitalize() if core[:1].isupper() else rep_)
        out.append(tok)
    return " ".join(out)


def norm(tok):
    t = tok.lower().replace("’", "'")
    t = re.sub(r"[^a-z0-9']", "", t).strip("'")
    return NUM.get(t, t)


def _ensure(d, w):
    if d.lookup_word(w) is not None: return
    ph = EXTRA.get(w)
    if not ph:   # last resort: spell it out sound by sound
        ph = " ".join(L2P[c] for c in re.sub(r"(.)\1+", r"\1", w) if c in L2P) or "AH"
    d.add_word(w, ph, True)


def _resample(a, sr=24000, to=16000):
    n = int(len(a) * to / sr); x = np.linspace(0, len(a) - 1, n)
    return np.interp(x, np.arange(len(a)), a)


def align(audio, text, sr=24000):
    toks = text.split(); words = [norm(t) for t in toks]
    idx = [i for i, w in enumerate(words) if w]            # tokens that are spoken words
    dur = len(audio) / sr; out = [None] * len(toks); got = 0
    try:
        d = _dec()
        for i in idx: _ensure(d, words[i])
        PAD = 0.12   # a little silence before the clip; the tail is tried with several paddings because a short last word
        # ("it", "up") is sometimes swallowed as silence with one padding and found with another
        body = (np.clip(_resample(np.asarray(audio, dtype=np.float64), sr) * 0.9, -1, 1) * 32767).astype(np.int16).tobytes()
        best = []
        for tail in (0.0, 0.25, 1.0, 0.1, 0.5):
            d.set_align_text(" ".join(words[i] for i in idx))
            d.start_utt(); d.process_raw(b"\0" * int(16000 * PAD) * 2 + body + b"\0" * int(16000 * tail) * 2, full_utt=True); d.end_utt()
            segs = [s for s in d.seg() if s.word not in ("<sil>", "(NULL)", "<s>", "</s>") and not s.word.startswith("+")]
            segs = [(s.start_frame / 100.0 - PAD, (s.end_frame + 1) / 100.0 - PAD) for s in segs]
            if len(segs) > len(best): best = segs
            if len(segs) == len(idx): break
        if len(best) == len(idx) - 1 and best:   # only the last word is missing: it is whatever sound is left
            best = best + [(best[-1][1], dur)]; got = -1
        if len(best) == len(idx):
            got = got + len(idx)
            for i, (s0, s1) in zip(idx, best):
                out[i] = (max(0.0, s0), min(dur, max(s0 + 0.02, s1)))
    except Exception as e:
        pass
    # fill anything missing by interpolation over character length between known anchors
    if got < len(toks):
        known = [(-1, 0.0)] + [(i, out[i][0]) for i in range(len(toks)) if out[i]] + [(len(toks), dur)]
        for (a, ta), (b, tb) in zip(known, known[1:]):
            miss = [i for i in range(a + 1, b) if not out[i]]
            if not miss: continue
            t0 = out[a][1] if a >= 0 and out[a] else ta
            tot = sum(len(toks[i]) + 1.5 for i in miss); c = t0
            for i in miss:
                w = (tb - t0) * (len(toks[i]) + 1.5) / tot; out[i] = (c, c + w); c += w
    return out, got, len(idx)


def onset_errors(audio, al, sr=24000):
    """Independent check of the alignment: wherever the speaker pauses (>= 0.15 s between two aligned words) the next word's
    start must sit on the place where the sound really comes back. Returns |aligned start - measured onset| in seconds."""
    a = np.asarray(audio, dtype=np.float64); hop = sr // 100
    env = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
    thr = max(0.012, 0.08 * np.percentile(env, 95)); errs = []
    for i in range(1, len(al)):
        gap0, st = al[i - 1][1], al[i][0]
        if st - gap0 < 0.15: continue
        lo = int(max(0, gap0 - 0.05) * 100); hi = int(min(len(env) - 1, (st + 0.35) * 100))
        k = lo; on = None
        while k < hi - 3:                               # a real pause (>= 80 ms quiet) followed by >= 30 ms of sound
            if all(env[j] < thr for j in range(k, min(hi, k + 8))):
                j = k + 8
                while j < hi and env[j] < thr: j += 1
                if j + 3 <= len(env) and all(env[x] >= thr for x in range(j, min(len(env), j + 3))): on = j; break
                k = j + 1
            else: k += 1
        if on is not None: errs.append(abs(on / 100.0 - st))
    return errs


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sing"))
    import sing
    text = sys.argv[1] if len(sys.argv) > 1 else "Let's count them. One, two, three, four, five, six, seven!"
    a = sing.say(text, "af_heart", 0.84); r, got, n = align(a, text)
    print(f"{got}/{n} words aligned, clip {len(a) / 24000:.2f} s")
    for t, (s, e) in zip(text.split(), r): print(f"  {s:5.2f}-{e:5.2f}  {t}")
