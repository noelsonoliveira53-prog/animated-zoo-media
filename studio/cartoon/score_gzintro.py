"""Gizmo Explains main intro: its music, ONE continuous arrangement across the four intro shots on recorded instruments (studio/sing/sf2render.py),
built with score_intro.py's tools (owner, Nov 21 2026 12:01 PM: "create an intro for the gizmo explain as well").

96 bpm, C major, C | F | G C. Gizmo's own tune (G E C E G C | A F C F A C | B G D G D | C G E C), every note a chord tone. Only instruments that
measured clean in the Zoo's score are used the same way (flute + bells for the tune, marimba pops, harp, celesta, xylophone run, strings, nylon
guitar, pizzicato, acoustic bass, light kit); no toms, timpani or snare roll, no crash and no brass on the last chord (score_intro.py's comments say why).
    toon.py: a shot with score="score_gzintro:score" and score_shots=4 calls score(shots) and mixes the result into the bed.
"""
from score_intro import Score, groove, m, scale_keys, B


def compose(idea_v0, things_v0, logo_v0, name_t0, name_voice_end, end):
    s = Score(seed=23)
    # ---- 1 THE IDEA (C): the tune alone on flute and bells over plucked strings; three marimba pops (the question marks); the bell = his bulb lights up
    t = idea_v0
    s.chord(t - B / 2, B * .5 + 4 * B, "harp", [48, 55, 60, 64, 67, 72], 58, strum=.045)
    s.melody(t, "G5:.5 E5:.5 C5:1 E5:.5 G5:.5 C6:1", 92)
    s.chord(t, 4.6 * B, "strings", [48, 55, 60, 64], 40)
    for b in range(4):
        s.chord(t + (b + .5) * B, B * .3, "pizz", [60, 64, 67], 50); s.drum(t + b * B, "shaker", 30 + 6 * b); s.drum(t + (b + .5) * B, "shaker", 24 + 6 * b)
    s.note(t, 2 * B, "bass", 36, 70); s.note(t + 2 * B, 2 * B, "bass", 43, 66)
    for k, n in enumerate(("G5", "C6", "E6")): s.note(t + (1 + .5 * k) * B, B * .4, "marimba", m(n), 72)
    s.note(t + 3 * B, 2 * B, "tubular", 84, 84); s.note(t + 3 * B, B, "glock", 84, 66); s.drum(t + 3 * B, "tri", 50)
    s.gliss(t + 3 * B, t + 3 * B + .3, "celesta", scale_keys(72, 96, (0, 7)), 46, 70)
    pre = things_v0 - B        # one beat before bar 2: a tambourine pickup and a harp sweep up into it (C and G only: both sit right over the F that follows)
    for k in range(4): s.drum(pre + k * B / 4, "tamb", 40 + 10 * k)
    s.gliss(pre, things_v0 - .02, "harp", scale_keys(55, 86, (0, 7)), 40, 76)
    # ---- 2 THE THINGS (F): the band comes in; each thing pops up on the marimba
    t = things_v0
    s.drum(t, "crash", 84)
    s.melody(t, "A5:.5 F5:.5 C5:1 F5:.5 A5:.5 C6:1", 98)
    groove(s, t, "F", 4)
    for k, n in enumerate(("F5", "A5", "C6", "F6", "C6", "A5", "F5")): s.note(t + k * B / 2, B * .4, "marimba", m(n), 70)
    s.chord(t, 4 * B, "strings", [41, 48, 53, 57], 40)
    pre = logo_v0 - B        # the extra beat before the logo: a cymbal roll that grows (the ring of light fills the picture)
    s.chord(pre, B, "strings", [41, 48, 53, 57], 48)
    for k in range(8): s.drum(pre + k * B / 8, "ride", 30 + 7 * k)
    s.note(pre, B, "bass", 41, 78)
    # ---- 3 THE LOGO (G then C): GIZMO drops in on the xylophone; EXPLAINS = kick, piano, brass, cymbal; the line = tubular bell
    t = logo_v0
    s.drum(t, "crash", 72); s.drum(t, "kick", 88)
    s.melody(t, "B5:.5 G5:.5 D5:1 G5:1 D6:1 C6:1 G5:.5 E5:.5 C6:1", 100)
    for k, n in enumerate(("G4", "B4", "D5", "G5", "B5")): s.note(t + (.5 + .5 * k) * B, B / 2, "xylo", m(n), 66 + 5 * k)      # G-I-Z-M-O land
    s.chord(t, 3 * B, "strings", [43, 50, 55, 59], 46)
    for b in range(3): s.drum(t + b * B, "hat", 40); s.drum(t + (b + .5) * B, "hat", 28); s.note(t + b * B, B * .9, "bass", 31 if b != 1 else 38, 84)
    for k in range(8): s.drum(t + 2 * B + k * B / 8, "ride", 30 + 9 * k)       # cymbal roll into EXPLAINS
    z = t + 3 * B            # EXPLAINS slams in
    s.drum(z, "crash", 108); s.drum(z, "kick", 110); s.drum(z, "kick2", 98); s.chord(z, B * .95, "piano", [43, 55], 100)
    s.chord(z, B * .55, "brass", [67, 71, 74], 98); s.note(z, B, "bass", 31, 102)
    d = z + B / 2            # the bell, the line, the confetti (G: over the G bar and over the C that follows)
    s.note(d, 2.5 * B, "tubular", 79, 90); s.note(d, B, "glock", 79, 76)
    s.gliss(d, d + .32, "celesta", scale_keys(74, 98, (7, 2)), 50, 74)
    s.drum(d, "wbh", 80); s.drum(d + .1, "wbl", 76)
    t2 = t + 4 * B           # the C bars: the full groove; Gizmo flies in = harp; the shine = celesta; the things pop up = marimba
    groove(s, t2, "C", 4, 1.0, fill_last=True)
    s.chord(t2, 4 * B, "strings", [48, 55, 60, 64], 44)
    s.gliss(t2, t2 + 1.6 * B, "harp", scale_keys(60, 88, (0, 4, 7))[::-1], 70, 46)
    s.gliss(t2 + .5 * B, t2 + .5 * B + .7, "celesta", [84, 88, 91, 96, 100, 103], 48, 70)
    for k, n in enumerate(("C6", "E6", "G6", "C7", "G6", "E6")): s.note(t2 + (.5 + .5 * k) * B, B * .4, "marimba", m(n), 68)
    s.note(t2 + 3 * B, B * .9, "bass", 43, 78)
    # ---- 4 THE NAME: a warm C chord under Gizmo's line (the mix lowers it under the voice); a bright final chord just after "Explains!"
    t = name_t0
    s.drum(t, "crash", 62); s.note(t, end - t, "bass", 36, 80)
    s.chord(t, end - t, "strings", [48, 55, 60, 64, 67], 46); s.chord(t, 3 * B, "piano", [48, 55, 60, 64], 52, strum=.02)
    s.note(t, B, "glock", 84, 50)
    f = t + round((name_voice_end + .03 - t) / (B / 2) + .499) * (B / 2)     # the final chord: the first half-beat after the line ends
    s.chord(f - .26, .3, "harp", [60, 64, 67, 72, 76, 79], 56, strum=.04)
    s.drum(f, "kick", 96); s.drum(f, "tamb", 70)
    s.chord(f, 1.2, "strings", [60, 64, 67, 72], 90)
    for k, n in enumerate(("G5", "C6", "E6", "G6")): s.note(f + k * B / 4, B, "marimba", m(n), 80 + 4 * k)      # his own run up on the last chord
    s.chord(f, end - f, "piano", [48, 55, 60, 64, 72], 96, strum=.008)
    s.note(f, 1.4, "celesta", 84, 72); s.note(f, 1.0, "celesta", 91, 66); s.note(f, .5, "glock", 84, 54)
    for k, n in enumerate(("E6", "C6", "G5")): s.note(f + (k + 1) * B, B, "celesta", m(n), 50 - 6 * k)
    return s.n


def score(shots):
    """shots: the four intro shots after toon.voice_lines (t0, v0, dur). Returns (audio at toon.SR, start seconds, end seconds)."""
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sing"))
    import sf2render
    idea, things, logo, name = shots[:4]
    start = max(0.0, idea["t0"] - .05); end = name["t0"] + name["dur"] + 1.6
    n = compose(idea["v0"] - start, things["v0"] - start, logo["v0"] - start, name["t0"] - start, name["v0"] + name["dur"] - start, end - start)
    a = sf2render.render(n, end - start + 1.5, 24000)
    return a, start, end
