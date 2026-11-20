"""The Animated Zoo main intro (owner, Nov 20 2026 12:44 PM: "create a main intro for the animated zoo that will be repeated on every episode,
don't need to change anything on what we have, just for future ones").

The same two shots in every new 2D episode (lesson, Guess With Milo, adventure), placed RIGHT AFTER the hook, so the episode still opens on its
promise (viral packaging, Nov 20) and the intro is the second thing the viewer sees. Not in the Shorts.
  1. The zoo gate at morning. On the beat, the friends pop up one by one (Tumble, Mango, Sandy, Tula) while the bells play the Animated Zoo
     jingle (instruments only, no sung voice); Milo flies in through the gate and lands on top of it; "THE ANIMATED ZOO" lands on the last beat.
  2. Close on the gate: Milo says "The Animated Zoo!" and every friend hops.
About 7 s. Same picture, same tune and same line every time (the line is cached, so it is the same sound too).

Use in an episode file:
    from intro import INTRO_STAGES, intro_shots
    STAGES = {..., **INTRO_STAGES}            # before Kit(STAGES)
    SHOTS = [<hook shots>, *intro_shots(), <the rest>]
Preview: `python3 toon.py zintro` renders the intro alone (episodes/zintro.py).
"""
import art, kit
from kit import S

BPM = 96
TB = lambda b: round(0.12 + b * 60 / BPM, 2)          # seconds into the tune shot of beat b (same rule as the other tune shots)

def bg_intro(p):
    """The zoo gate in the morning, dressed for the show: the usual gate (art.bg_zoo) with bunting across the arch and balloons by the posts."""
    far, mid, near = art.bg_zoo(p)
    cols = ["#ff7aa2", art.SUN, "#5cc473", art.MILO_BLUE, "#b48cff"]
    flags = "".join(f'<path d="M{x} {y} l26 0 l-13 34Z" fill="{cols[k % 5]}"/>' for k, (x, y) in enumerate((630 + 46 * k, 545 - 150 * (1 - ((k - 7.5) / 7.5) ** 2)) for k in range(16)))
    line = '<path d="M640 545 Q960 250 1300 545" stroke="#fff" stroke-width="5" fill="none"/>'
    balloons = "".join(f'<g transform="translate({x} {y})"><path d="M0 60 q-10 60 6 130" stroke="#fff" stroke-width="3" fill="none"/>'
                       f'<ellipse cx="0" cy="0" rx="46" ry="58" fill="{c}"/><ellipse cx="-14" cy="-20" rx="10" ry="16" fill="#fff" opacity=".5"/></g>'
                       for x, y, c in ((560, 300, "#ff7aa2"), (500, 380, art.SUN), (1360, 300, art.MILO_BLUE), (1430, 390, "#5cc473")))
    return far, mid, near + line + flags + balloons


art.BG["intro_gate"] = bg_intro
art.PLACE["intro_gate"] = "the zoo gate (main intro)"

INTRO_STAGES = {
    "intro_gate": [("mango", "monkey", 300, 880, .5), ("tumble", "tumble", 560, 875, .55), ("sandy", "calf", 1380, 878, .48),
                   ("tula", "turtle", 1640, 888, .5), ("milo", "milo", 960, 390, .62, False, True)],      # Milo sits on the top of the arch (its top edge is y 385 at the middle)
}
_POS = {a[0]: a[2:4] for a in INTRO_STAGES["intro_gate"]}

# the jingle: two bars in C at 96, chord tones only (C bar: C E G C; G bar: D B G B D), ends open on D so Milo's line answers it
JINGLE = {"bpm": BPM, "chords": "C G", "outro_bars": 0, "style": "lullaby",
          "lines": [{"text": "~ ~ ~ ~ ~ ~ ~ ~ ~", "notes": "C4:1 E4:1 G4:1 C5:1 D5:.5 B4:.5 G4:.5 B4:.5 D5:1", "rest": 1}]}


def _pop(at, who, d=.4):
    x, y = _POS[who]
    return ("fromto", at, f"#{{p}}{who}_w", {"x": x, "y": y + 420}, {"x": x, "y": y, "duration": d, "ease": "back.out(2)"}, f"{who} pops up")


def intro_shots():
    gx, gy = _POS["milo"]
    return [
        S("intro_gate", (960, 540, 1920), who="", sing=JINGLE, beat="song", tag="INTRO: the gate", trans="iris",
          fx=[_pop(TB(0), "tumble"), _pop(TB(1), "mango"), _pop(TB(2), "sandy"), _pop(TB(3), "tula"),
              ("fromto", TB(4), "#{p}milo_w", {"x": -180, "y": 160}, {"x": gx, "y": gy, "duration": TB(7) - TB(4), "ease": "power2.out"}, "Milo flies in and lands on the gate")],
          words=[(TB(5), "THE ANIMATED ZOO", .5, .905, 1.05, "sun")]),      # on the path under the friends' feet (stills Nov 20: higher, it covered feet and faces)
        S("intro_gate", (960, 560, 1760), "The Animated Zoo!", tag="INTRO: Milo says the name",      # wide enough to hold every friend (1300 cut Mango and Tula)
          fx=[("hop", "w:Animated", "tumble"), ("hop", "w:Animated", "mango"), ("hop", "w:Zoo!", "sandy"), ("hop", "w:Zoo!", "tula"), ("hop", "w:Zoo!", "milo")],
          words=[]),      # no big word here: the spoken line's caption already reads "The Animated Zoo!" at the bottom (stills Nov 20: the two sat on each other)
    ]
