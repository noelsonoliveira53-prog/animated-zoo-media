"""Real instruments for the channel's music: plays a list of notes through a General MIDI SoundFont of RECORDED instruments
(GeneralUser GS v2, studio/sing/sf2/, licence: free for any music production, commercial included) instead of the raw sine / triangle / saw
oscillators of sing.backing(), then gives every group of instruments its own room, EQ and compression and masters the mix.

Owner, Nov 20 2026 3:52 PM, on the intro: "made the music better, now it sounds like artificial music".

    from sf2render import render
    audio = render(notes, seconds, sr=24000)      # mono float32
notes: (t_seconds, dur_seconds, inst, midi_key, velocity). inst is a name in INST (or "drums" with a GM drum key).
If the SoundFont is missing: python3 studio/sing/sf2render.py --fetch   (32 MB from github.com/mrbumpy409/GeneralUser-GS).
"""
import os, sys, hashlib, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SF2 = os.path.join(HERE, "sf2", "GeneralUser-GS.sf2")
URL = "https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2"
CACHE = os.path.join(HERE, "cache")
RATE = 48000

# name: (GM program 0-based, bus). Buses get their own processing in _bus().
INST = {
    "glock": (9, "lead"), "celesta": (8, "lead"), "flute": (73, "lead"), "tubular": (14, "lead"), "musicbox": (10, "lead"),
    "xylo": (13, "perc"), "marimba": (12, "perc"), "harp": (46, "perc"), "timpani": (47, "perc"), "brass": (61, "perc"),
    "piano": (0, "band"), "nylon": (24, "band"), "pizz": (45, "band"), "strings": (48, "pad"), "bass": (32, "bass"), "drums": (None, "drums"),
}


def fetch():
    import urllib.request
    os.makedirs(os.path.dirname(SF2), exist_ok=True); urllib.request.urlretrieve(URL, SF2); return SF2


def _play(notes, seconds, bus):
    import tinysoundfont as tsf
    syn = tsf.Synth(gain=-6, samplerate=RATE); sfid = syn.sfload(SF2, max_voices=256)
    chans = {}
    for name, (prog, b) in INST.items():
        if b != bus: continue
        ch = 9 if name == "drums" else len([c for c in chans.values() if c != 9])
        if ch == 9: syn.program_select(9, sfid, 128, 0, True)
        else: syn.program_select(ch, sfid, 0, prog)
        chans[name] = ch
    ev = []
    for t, d, inst, key, vel in notes:
        if INST[inst][1] != bus: continue
        ev.append((max(0.0, t), 1, chans[inst], int(key), int(np.clip(vel, 1, 127)))); ev.append((max(0.0, t) + max(0.02, d), 0, chans[inst], int(key), 0))
    ev.sort(key=lambda e: (e[0], e[1]))
    n = int(seconds * RATE); out = np.zeros((n, 2), np.float32); pos = 0
    for t, on, ch, key, vel in ev + [(seconds, 0, 0, 0, 0)]:
        i = min(n, int(t * RATE))
        if i > pos: out[pos:i] = np.frombuffer(syn.generate(i - pos), np.float32).reshape(-1, 2); pos = i
        if t >= seconds: break
        (syn.noteon(ch, key, vel) if on else syn.noteoff(ch, key))
    return out


def _bus(x, bus):
    from pedalboard import Pedalboard, Reverb, HighpassFilter, LowpassFilter, Compressor, LowShelfFilter, HighShelfFilter, PeakFilter
    room = lambda wet, size=.5: Reverb(room_size=size, damping=.45, wet_level=wet, dry_level=1 - wet * .5, width=.9)
    fx = {"lead": [HighpassFilter(250), PeakFilter(3200, 1.5, .8), room(.26, .55)],
          "perc": [HighpassFilter(90), room(.22, .55)],
          "band": [HighpassFilter(110), PeakFilter(300, -2.5, 1.0), Compressor(-20, 2.5, 8, 120), room(.16, .45)],
          "pad": [HighpassFilter(140), LowpassFilter(7000), room(.35, .7)],
          "bass": [HighpassFilter(38), LowpassFilter(2500), Compressor(-22, 3, 10, 150), room(.06, .3)],
          "drums": [HighpassFilter(45), PeakFilter(4000, -2, 1.0), Compressor(-18, 3, 5, 90), room(.14, .4)]}[bus]
    return Pedalboard(fx)(x.T.copy(), RATE).T


def render(notes, seconds, sr=24000, levels=None, master=True):
    """notes -> mono float32 at sr. levels: bus gains (dB). Cached by content."""
    lv = {"lead": 0, "perc": -1, "band": -3, "pad": -6, "bass": -3, "drums": -5}; lv.update(levels or {})
    h = hashlib.md5(json.dumps([notes, seconds, sr, lv, master, 4], sort_keys=True, default=float).encode()).hexdigest()[:16]
    f = os.path.join(CACHE, f"sf2_{h}.npy")
    if os.path.exists(f): return np.load(f)
    if not os.path.exists(SF2): fetch()
    mix = np.zeros((int(seconds * RATE), 2), np.float32)
    for bus in ("lead", "perc", "band", "pad", "bass", "drums"):
        if not any(INST[n[2]][1] == bus for n in notes): continue
        mix += _bus(_play(notes, seconds, bus), bus) * 10 ** (lv[bus] / 20)
    if master:
        from pedalboard import Pedalboard, Compressor, HighShelfFilter, LowShelfFilter, Limiter, HighpassFilter
        mix = Pedalboard([HighpassFilter(35), LowShelfFilter(120, -1.5), HighShelfFilter(9000, 1.5), Compressor(-16, 2.0, 15, 200), Limiter(-1.5, 120)])(mix.T.copy(), RATE).T
    from scipy.signal import resample_poly
    mono = resample_poly(mix.mean(axis=1), sr, RATE).astype(np.float32)
    os.makedirs(CACHE, exist_ok=True); np.save(f, mono); return mono


if __name__ == "__main__" and "--fetch" in sys.argv:
    print(fetch())
