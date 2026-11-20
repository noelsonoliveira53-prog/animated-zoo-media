"""The main intro's music: ONE continuous arrangement across the four intro shots, played on recorded instruments (studio/sing/sf2render.py),
in place of the four separate synthesized jingles (owner, Nov 20 2026 3:52 PM: "make the music better, now it sounds like artificial music").

Timed from the shots themselves (each section starts on its shot's first beat, v0), so it stays in sync wherever an episode places the intro.
96 bpm, C major. The tune is the same as before (C E G C | D B G B D | A C F C E D C D C), every note over a chord a chord tone or a whole
step from one. Every picture hit has its own instrument: the friends' pops = marimba, Milo's swoops = harp glissando, the letters = xylophone
run, ZOO = timpani + brass + cymbal, the ding = tubular bell, the confetti = celesta, the bear ears = wood blocks; no synthetic sound effects.
    toon.py: a shot with score="score_intro:score" and score_shots=4 calls score(shots) and mixes the result into the bed.
"""
import numpy as np

BPM = 96
B = 60 / BPM
C = {"C": [48, 52, 55], "G": [43, 47, 50], "F": [41, 45, 48]}       # chord roots in octave 3
DR = {"kick": 36, "snare": 38, "stick": 37, "hat": 42, "ohat": 46, "crash": 49, "ride": 51, "tamb": 54, "shaker": 70, "tri": 81,
      "tlo": 45, "tmid": 47, "thi": 50, "wbh": 76, "wbl": 77, "chimes": 84, "clap": 39, "kick2": 35}
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def m(n):
    """'C5' -> 60+12 ... (C4 = 60)."""
    return 12 * (int(n[-1]) + 1) + NOTE[n[0]]


class Score:
    def __init__(self, seed=11):
        self.n = []; self.r = np.random.default_rng(seed)

    def note(self, t, d, inst, key, vel, human=True):
        if human: t += float(self.r.normal(0, .004)); vel += float(self.r.normal(0, 5))
        self.n.append((round(max(0.0, t), 4), round(d, 4), inst, int(key), int(np.clip(vel, 8, 127))))

    def drum(self, t, name, vel, human=True):
        self.note(t, .25, "drums", DR[name], vel, human)

    def chord(self, t, d, inst, keys, vel, strum=0.0):
        for k, key in enumerate(keys): self.note(t + k * strum, d - k * strum, inst, key, vel - 4 * k)

    def gliss(self, t0, t1, inst, keys, vel0, vel1):
        for k, key in enumerate(keys):
            f = k / max(1, len(keys) - 1); self.note(t0 + f * (t1 - t0), .5, inst, key, vel0 + f * (vel1 - vel0), human=False)

    def melody(self, t, notes, vel=96):
        """notes 'C5:1 E5:.5 ...' -> glockenspiel + flute in unison (+ xylophone on short notes for sparkle)."""
        for tok in notes.split():
            n, d = tok.split(":"); d = float(d)
            self.note(t, d * B * .98, "flute", m(n), vel - 8); (self.note(t, d * B * .9, "glock", m(n), vel - 26) if m(n) >= 72 else None)      # the flute carries the tune, the bells (from C5 up)
            if d <= .5: self.note(t, d * B, "marimba", m(n), vel - 40)      # sparkle on top: louder bells' inharmonic partials read as clashes (round 6)
            t += d * B


def scale_keys(lo, hi, pcs=(0, 2, 4, 5, 7, 9, 11)):
    return [k for k in range(lo, hi + 1) if k % 12 in pcs]


def groove(s, t, chord, beats, vel=1.0, fill_last=False):
    """Light kids' pop band for `beats` beats from t: kick 1 & 3, snare 2 & 4 (soft), hats on 8ths, tambourine on 2 & 4, acoustic bass,
    nylon guitar strummed on the calypso pattern, pizzicato on the off-beats."""
    root = C[chord][0]; tri = C[chord]
    for b in range(beats):
        tb = t + b * B
        if fill_last and b == beats - 1:
            s.drum(tb, "shaker", 70 * vel)      # tambourine + shaker (toms rang out of the key in round 2, a kick read B3 in round 6)
            for k in range(1, 4): s.drum(tb + k * B / 4, "tamb", (48 + 12 * k) * vel)
        else:
            if b % 2 == 0: s.drum(tb, "kick", 92 * vel)
            else: s.drum(tb, "snare", 62 * vel); s.drum(tb, "tamb", 44 * vel)
            s.drum(tb, "hat", 46 * vel); s.drum(tb + B / 2, "hat", 32 * vel)
        if fill_last and b == beats - 1: continue      # the fill beat's bass is the walk-up the caller writes (two bass lines at once beat into a B3 / C#4, round 8)
        s.note(tb, B * .85, "bass", root - 12 + (7 if b % 4 == 2 else 0), 92 * vel)
        if b % 4 == 3: s.note(tb + B / 2, B * .4, "bass", root - 12 + 7, 70 * vel)
        gt = [tri[0] + 12, tri[1] + 12, tri[2] + 12, tri[0] + 24]
        for off, v in ((0, 66), (.5, 46)) if b % 2 == 0 else ((.5, 58),):
            s.chord(tb + off * B, B * .45, "nylon", gt if off == 0 else gt[::-1], v * vel, strum=.011)
        s.chord(tb + B / 2, B * .3, "pizz", [k + 12 for k in tri], 52 * vel)


def compose(sky_v0, gate_v0, logo_v0, name_t0, name_voice_end, end):
    s = Score()
    # ---- 1 SKY: the morning sky; the tune starts alone on the bells and the flute, the strings rise, the harp rolls, the celesta twinkles
    t = sky_v0
    s.chord(t - B / 2, B * .5 + 4 * B, "harp", [48, 52, 55, 60, 64, 67, 72, 76], 64, strum=.045)
    s.melody(t, "C5:1 E5:1 G5:1 C6:1", 92)
    for k, (b, n) in enumerate(((.5, "G6"), (1.5, "E6"), (2.5, "C7"), (3.5, "G6"))): s.note(t + b * B, B, "celesta", m(n), 58)
    s.chord(t, 4.6 * B, "strings", [48, 55, 60, 64], 44)
    for b in range(4): s.drum(t + b * B, "shaker", 30 + 6 * b); s.drum(t + (b + .5) * B, "shaker", 24 + 6 * b)
    s.note(t, 2 * B, "bass", 36, 70); s.note(t + 2 * B, 2 * B, "bass", 43, 66)
    s.drum(t + 3 * B, "tri", 52)
    pre = gate_v0 - B        # one beat before the gate: a tom pickup and a harp sweep up into it
    for k in range(4): s.drum(pre + k * B / 4, "tamb", 40 + 10 * k)
    s.gliss(pre, gate_v0 - .02, "harp", scale_keys(55, 86, (2, 7)), 40, 78)      # only G and D: the whole scale rubbed against the C still ringing (round 3)
    # ---- 2 GATE (G): the band comes in; the friends pop up on marimba; Milo's swoop is a harp glissando
    t = gate_v0
    s.drum(t, "crash", 86)
    s.melody(t, "D5:.5 B4:.5 G4:.5 B4:.5 D5:2", 98)
    groove(s, t, "G", 4)
    for k, n in enumerate(("G5", "B5", "D6", "G6")): s.note(t + k * B / 2, B * .4, "marimba", m(n), 74)
    s.gliss(t + B, t + 3.2 * B, "harp", scale_keys(55, 91, (2, 7)), 46, 70)
    s.chord(t, 4 * B, "strings", [43, 50, 55, 59], 40)
    pre = logo_v0 - B        # the extra beat before the logo: a snare roll that grows
    s.chord(pre, B, "strings", [43, 50, 55, 59], 50)
    for k in range(8): s.drum(pre + k * B / 8, "ride", 30 + 7 * k)      # a cymbal roll grows into the logo (a snare roll rang at G#3 in round 1, a timpani roll off the key in round 2)
    s.note(pre, B, "bass", 38, 80)
    # ---- 3 LOGO (F then C): badge pops; THE; the letters run up on the xylophone; ZOO = timpani, brass, cymbal; the ding = tubular bell
    t = logo_v0
    s.drum(t, "crash", 74); s.drum(t, "kick", 88); s.note(t, B, "piano", 29, 70); s.note(t, B, "piano", 41, 64)
    s.melody(t, "A4:1 C5:1 F5:1 C5:1 E5:.5 D5:.5 C5:.5 D5:.5 C5:1", 100)
    for k, n in enumerate(("F5", "A5", "C6")): s.note(t + B / 2 + k * B / 8, B / 4, "xylo", m(n), 70)       # T-H-E lands
    for k, n in enumerate(("F4", "A4", "C5", "F5", "A5", "C6", "F6", "A6")): s.note(t + B + k * B / 4, B / 2, "xylo", m(n), 66 + 4 * k)
    s.chord(t, 3 * B, "strings", [41, 48, 53, 57], 46)
    for b in range(3): s.drum(t + b * B, "hat", 40); s.drum(t + (b + .5) * B, "hat", 28); s.note(t + b * B, B * .9, "bass", 29 if b != 1 else 36, 84)
    for k in range(8): s.drum(t + 2 * B + k * B / 8, "ride", 30 + 9 * k)       # cymbal roll into ZOO
    z = t + 3 * B            # ZOO slams in
    s.drum(z, "crash", 112); s.drum(z, "kick", 112); s.drum(z, "kick2", 100); s.chord(z, B * .95, "piano", [29, 41, 53], 104)
    s.chord(z, B * .55, "brass", [65, 69, 72], 102); s.note(z, B, "bass", 29, 104)
    d = z + B / 2            # the ding, the confetti, the bear ears
    s.note(d, 2.5 * B, "tubular", 84, 92); s.note(d, B, "glock", 84, 80)
    s.gliss(d, d + .32, "celesta", scale_keys(72, 96, (0, 7, 9)), 50, 76)      # C, G, A: right over the F and over the C that follows (rounds 3-4)
    s.drum(d, "wbh", 84); s.drum(d + .1, "wbl", 80)
    t2 = t + 4 * B           # the C bars: the full groove; Milo's flight down = harp; the shine = celesta; the friends pop = marimba
    groove(s, t2, "C", 4, 1.0, fill_last=True)
    s.chord(t2, 4 * B, "strings", [48, 55, 60, 64], 44)
    s.gliss(t2, t2 + 1.6 * B, "harp", scale_keys(60, 88, (0, 4, 7))[::-1], 72, 46)
    s.gliss(t2 + .5 * B, t2 + .5 * B + .77, "celesta", [84, 88, 91, 96, 100, 103, 108], 50, 72)      # the shine runs along the 11 letters
    for k, n in enumerate(("C6", "E6", "G6", "C7")): s.note(t2 + B + k * B / 2, B * .4, "marimba", m(n), 70)
    s.note(t2 + 3 * B, B * .9, "bass", 43, 78)      # the fill beat: one G under it (a walk-up G2-A2 read B3 / C#4 in rounds 3-8)
    # ---- 4 NAME: a warm C chord under Milo's line (the mix lowers it under the voice); a cheerful final chord just after "Zoo!"
    t = name_t0
    s.drum(t, "crash", 64); s.note(t, end - t, "bass", 36, 80)
    s.chord(t, end - t, "strings", [48, 55, 60, 64, 67], 46); s.chord(t, 3 * B, "piano", [48, 55, 60, 64], 52, strum=.02)
    s.note(t, B, "glock", 84, 50)
    f = t + round((name_voice_end + .03 - t) / (B / 2) + .499) * (B / 2)     # the final chord: the first half-beat after the line ends
    s.chord(f - .26, .3, "harp", [60, 64, 67, 72, 76, 79], 56, strum=.04)
    s.drum(f, "kick", 96); s.drum(f, "tamb", 70)      # no crash on the last chord: it read G#6 (rounds 5-6)
    s.chord(f, 1.2, "strings", [60, 64, 67, 72], 92);
    for k, n in enumerate(("C6", "E6", "G6", "C7")): s.note(f + k * B / 4, B, "marimba", m(n), 80 + 4 * k)      # a bright four-note run on the last chord
    s.chord(f, end - f, "piano", [48, 55, 60, 64, 72], 98, strum=.008)      # no low C2 on the piano: its high partials read F#5 (round 5); the bass has the C
    # (the strings swell on the last chord replaced the brass there: it read G#6 / B5 against the piano, rounds 9-10)
    s.note(f, 1.4, "celesta", 84, 74); s.note(f, 1.0, "celesta", 96, 70); s.note(f, .5, "glock", 84, 56)
    for k, n in enumerate(("G6", "E6", "C6")): s.note(f + (k + 1) * B, B, "celesta", m(n), 50 - 6 * k)
    return s.n


def score(shots):
    """shots: the four intro shots after toon.voice_lines (t0, v0, dur). Returns (audio at toon.SR, start seconds, end seconds)."""
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sing"))
    import sf2render
    sky, gate, logo, name = shots[:4]
    start = max(0.0, sky["t0"] - .05); end = name["t0"] + name["dur"] + 1.6
    n = compose(sky["v0"] - start, gate["v0"] - start, logo["v0"] - start, name["t0"] - start, name["v0"] + name["dur"] - start, end - start)
    drop = os.environ.get("SCORE_DROP")      # testing only: leave one instrument out after a time ("piano@12.5")
    if drop: inst, at = drop.split("@"); n = [x for x in n if not (x[2] == inst and x[0] >= float(at) - start)]
    a = sf2render.render(n, end - start + 1.5, 24000)
    return a, start, end
