"""The Animated Zoo main intro (owner, Nov 20 2026 12:44 PM: "create a main intro for the animated zoo that will be repeated on every episode,
don't need to change anything on what we have, just for future ones"; 12:56 PM: "I want the intro to be more sophisticated with more details and effects").

The same four shots in every new long 2D episode (lesson, Guess With Milo, adventure), placed RIGHT AFTER the hook (the episode still opens on its
promise, viral packaging Nov 20). Not in the Shorts (the shots carry no `part`). About 15 s. One four-bar tune at 96 bpm on the bells with the light
"pop" band (instruments only, never a sung voice), one cut per bar line.
  1. SKY (bar 1). The camera starts in the morning sky (turning sun rays, twinkling stars, drifting clouds) and glides down toward the gate.
  2. THE GATE (bar 2). The friends pop up on the beat, each in a puff of stars (Tumble, Mango, Sandy, Tula); the bunting and balloons bounce in
     tempo; Milo swoops in from the sky with a sparkle trail and lands on the top of the arch.
  3. THE LOGO (bars 3-4). A turning sunburst; a badge with a spinning star; "THE" lands, then "ANIMATED" drops in letter by letter in rainbow colours,
     "ZOO" slams in with a ding, a confetti burst and two little bear ears popping onto the O's; a shine runs along the letters; Milo flies onto the
     badge and the friends pop up on both sides.
  4. THE NAME. Milo says "The Animated Zoo!", the friends cheer (they hop after the line, silently: no sound effect on a spoken word), confetti rains.
Use in an episode file:
    from intro import INTRO_STAGES, intro_shots
    STAGES = {..., **INTRO_STAGES}            # before Kit(STAGES)
    SHOTS = [<hook shots>, *intro_shots(), <the rest>]
Preview alone: `python3 toon.py zintro`. Change the intro HERE only, so every episode keeps the same one.
"""
import math, random
import art
from kit import S, prop

BPM = 96
B = 60 / BPM
TB = lambda b: round(0.12 + b * B, 3)          # seconds into a tune shot of beat b (the tune enters 0.12 s after the cut)
INK = "#2a1a4a"
FRIENDS = ["tumble", "mango", "sandy", "tula"]


# ---------------------------------------------------------------- places
def bg_intro(p):
    """The zoo gate in the morning, dressed for the show: the usual gate (art.bg_zoo) with bunting across the arch and balloons by the posts (both bounce)."""
    far, mid, near = art.bg_zoo(p)
    cols = ["#ff7aa2", art.SUN, "#5cc473", art.MILO_BLUE, "#b48cff"]
    flags = "".join(f'<path d="M{x:.0f} {y:.0f} l26 0 l-13 34Z" fill="{cols[k % 5]}"/>'
                    for k, (x, y) in enumerate((630 + 46 * k, 545 - 150 * (1 - ((k - 7.5) / 7.5) ** 2)) for k in range(16)))
    line = '<path d="M640 545 Q960 250 1300 545" stroke="#fff" stroke-width="5" fill="none"/>'
    balloons = "".join(f'<g transform="translate({x} {y})"><path d="M0 60 q-10 60 6 130" stroke="#fff" stroke-width="3" fill="none"/>'
                       f'<ellipse cx="0" cy="0" rx="46" ry="58" fill="{c}"/><ellipse cx="-14" cy="-20" rx="10" ry="16" fill="#fff" opacity=".5"/>'
                       f'<path d="M-6 56 l6 10 l6 -10Z" fill="{c}"/></g>'
                       for x, y, c in ((560, 300, "#ff7aa2"), (500, 380, art.SUN), (1360, 300, art.MILO_BLUE), (1430, 390, "#5cc473")))
    return far, mid, near + f'<g id="{p}_flags">{line}{flags}</g><g id="{p}_balloons">{balloons}</g>'


def bg_logo(p):
    """The logo card: a deep sky with a big sunburst that turns slowly behind everything, a soft glow in the middle, a grassy hill in front."""
    far = ('<defs><radialGradient id="%s_glow" cx="50%%" cy="45%%" r="60%%"><stop offset="0" stop-color="#bfeaff"/><stop offset=".55" stop-color="#4fb3ff"/>'
           '<stop offset="1" stop-color="#2a6fd6"/></radialGradient></defs><rect x="-500" y="-900" width="2920" height="2900" fill="url(#%s_glow)"/>' % (p, p))
    wedges = "".join(f'<path d="M0 0 L{2600 * math.cos(math.radians(a)):.0f} {2600 * math.sin(math.radians(a)):.0f} '
                     f'L{2600 * math.cos(math.radians(a + 9)):.0f} {2600 * math.sin(math.radians(a + 9)):.0f}Z" fill="#ffffff" opacity=".13"/>' for a in range(0, 360, 18))
    far += f'<g transform="translate(960 470)"><g id="{p}_burst">{wedges}</g></g>'
    near = ('<path d="M-500 930 C200 860 700 900 1200 870 S2000 880 2420 920 L2420 2000 L-500 2000Z" fill="#7cc95e"/>'
            '<path d="M-500 960 C300 900 900 950 1400 915 S2100 930 2420 960 L2420 2000 L-500 2000Z" fill="#6bbd50"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/><circle cx="{x + 16}" cy="{y + 6}" r="7" fill="#fff"/>'
                      for x, y, c in ((140, 1010, "#ff7aa2"), (520, 1030, art.SUN), (1400, 1020, "#ff7aa2"), (1780, 1035, art.SUN))))
    return far, "", near


art.BG["intro_gate"] = bg_intro; art.PLACE["intro_gate"] = "the zoo gate (main intro)"
art.BG["intro_logo"] = bg_logo; art.PLACE["intro_logo"] = "the logo (main intro)"

INTRO_STAGES = {
    "intro_gate": [("mango", "monkey", 300, 880, .5), ("tumble", "tumble", 560, 875, .55), ("sandy", "calf", 1380, 878, .48),
                   ("tula", "turtle", 1640, 888, .5), ("milo", "milo", 960, 390, .62, False, True)],      # Milo sits on the top of the arch (its top edge is y 385 at the middle)
    "intro_logo": [("mango", "monkey", 230, 1000, .42), ("tumble", "tumble", 440, 995, .46), ("sandy", "calf", 1480, 998, .42),
                   ("tula", "turtle", 1690, 1004, .42), ("milo", "milo", 960, 236, .46, False, True)],      # Milo stands on the badge (its top is y 232)
}
_POS = {k: {a[0]: a[2:4] for a in v} for k, v in INTRO_STAGES.items()}
_SC = {k: {a[0]: a[4] for a in v} for k, v in INTRO_STAGES.items()}


# ---------------------------------------------------------------- props (drawn at their own origin; fx reach their parts as "#{p}<prop>-<part>")
def _star4(r, c="#fff"):
    return f'<path d="M0 {-r} Q{r * .18:.1f} {-r * .18:.1f} {r} 0 Q{r * .18:.1f} {r * .18:.1f} 0 {r} Q{-r * .18:.1f} {r * .18:.1f} {-r} 0 Q{-r * .18:.1f} {-r * .18:.1f} 0 {-r}Z" fill="{c}"/>'


def _star5(r, c, k=.45):
    pts = " ".join(f"{(r if i % 2 == 0 else r * k) * math.sin(math.pi * i / 5):.1f},{-(r if i % 2 == 0 else r * k) * math.cos(math.pi * i / 5):.1f}" for i in range(10))
    return f'<polygon points="{pts}" fill="{c}"/>'


def rays(q):
    """Sun rays that turn, with a fresh sun and a glow on top (sits exactly on the backdrop's sun)."""
    r = "".join(f'<path d="M0 0 L{300 * math.cos(math.radians(a)):.0f} {300 * math.sin(math.radians(a)):.0f} L{300 * math.cos(math.radians(a + 11)):.0f} '
                f'{300 * math.sin(math.radians(a + 11)):.0f}Z" fill="#fff6c4" opacity=".55"/>' for a in range(0, 360, 30))
    return f'<g id="{q}-r">{r}</g><circle r="118" fill="#fff3a8" opacity=".55"/><circle r="88" fill="{art.SUN}"/><circle cx="-24" cy="-26" r="20" fill="#fff" opacity=".45"/>'


SPARKLES = [(130, -280), (520, -150), (860, -330), (1180, -190), (1520, -300), (1780, -120), (330, 40), (1060, 30), (1660, 120), (720, 150)]
def sparkles(q):
    return "".join(f'<g transform="translate({x} {y})"><g id="{q}-s{k}">{_star4(26 if k % 3 else 38)}</g></g>' for k, (x, y) in enumerate(SPARKLES))


def puff(q):
    """A ring of little stars and dots that bursts out when a friend pops up."""
    cols = [art.SUN, "#ff7aa2", "#fff", "#5cc473", "#b48cff", art.MILO_BLUE]
    return "".join(f'<g id="{q}-d{k}">' + (_star5(18, cols[k % 6]) if k % 2 == 0 else f'<circle r="10" fill="{cols[k % 6]}"/>') + '</g>' for k in range(10))


TRAIL = [(-60, 200), (140, 236), (340, 280), (520, 316), (680, 344), (820, 366)]      # along Milo's swoop to the arch
def trail(q):
    return "".join(f'<g transform="translate({x} {y})"><g id="{q}-t{k}" opacity="0">{_star4(24 - k * 1.5, art.SUN if k % 2 else "#fff")}</g></g>' for k, (x, y) in enumerate(TRAIL))


_W = {"A": .64, "N": .66, "I": .31, "M": .86, "T": .58, "E": .56, "D": .66, "Z": .58, "O": .70, "H": .66}
RAINBOW = ["#ff4d6d", "#ff8a1f", "#ffd23f", "#4cc95a", "#2fb5ff", "#3a7bff", "#9b5cff", "#ff5fb8"]
def _word(q, name, text, size, y, cols, ls=.03):
    xs = []; w = sum(_W[c] for c in text) * size + ls * size * (len(text) - 1); x = -w / 2
    for c in text: xs.append(x + _W[c] * size / 2); x += _W[c] * size + ls * size
    out = ""; t = f'font-family="Baloo" font-weight="800" font-size="{size}" text-anchor="middle" stroke-linejoin="round" paint-order="stroke"'
    for k, (c, cx) in enumerate(zip(text, xs)):
        out += (f'<g id="{q}-{name}{k}"><text x="{cx:.0f}" y="{y + size * .07:.0f}" {t} fill="{INK}" stroke="{INK}" stroke-width="{size * .16:.0f}" opacity=".35">{c}</text>'
                f'<text x="{cx:.0f}" y="{y:.0f}" {t} fill="{cols[k % len(cols)]}" stroke="{INK}" stroke-width="{size * .12:.0f}">{c}</text>'
                f'<text id="{q}-{name}{k}h" x="{cx:.0f}" y="{y:.0f}" {t} fill="#ffffff" opacity="0">{c}</text></g>')
    return out, xs


def logo(q):
    """THE / ANIMATED (rainbow) / ZOO (sunny, with bear ears on the O's), under a badge with a turning star. Origin: the middle of 'ANIMATED'."""
    badge = (f'<g transform="translate(0 -330)"><circle r="122" fill="#fff"/><circle r="104" fill="{art.MILO_BLUE}"/>'
             f'<circle r="104" fill="none" stroke="#bfe0ff" stroke-width="8" stroke-dasharray="14 18"/><g id="{q}-star">{_star5(70, art.SUN)}</g></g>')
    the, _ = _word(q, "t", "THE", 78, -150, ["#ffffff"])
    ani, _ = _word(q, "a", "ANIMATED", 190, 60, RAINBOW)
    zoo, zx = _word(q, "z", "ZOO", 250, 300, [art.SUN])
    ears = "".join(f'<g id="{q}-ear{j}" opacity="0"><circle cx="{zx[k] - 52:.0f}" cy="150" r="30" fill="{art.SUN}" stroke="{INK}" stroke-width="16" paint-order="stroke"/>'
                   f'<circle cx="{zx[k] + 52:.0f}" cy="150" r="30" fill="{art.SUN}" stroke="{INK}" stroke-width="16" paint-order="stroke"/></g>' for j, k in enumerate((1, 2)))
    return f'<g id="{q}-badge">{badge}</g>{the}{ani}{ears}{zoo}'


_rnd = random.Random(7)
CONF = [(_rnd.uniform(-900, 900), _rnd.uniform(-560, -120), _rnd.choice(RAINBOW + [art.SUN, "#fff"]), _rnd.random() < .5, _rnd.uniform(-540, 540)) for _ in range(44)]
def confetti(q):
    return "".join((f'<rect id="{q}-c{k}" x="-9" y="-14" width="18" height="28" rx="4" fill="{c}"/>' if rect else f'<circle id="{q}-c{k}" r="11" fill="{c}"/>')
                   for k, (_, _, c, rect, _) in enumerate(CONF))


RAIN = [(_rnd.uniform(-60, 1980), _rnd.uniform(-700, -60), _rnd.choice(RAINBOW + [art.SUN, "#fff"]), _rnd.random() < .5) for _ in range(40)]
def rain(q):
    return "".join((f'<rect id="{q}-r{k}" x="{x - 8:.0f}" y="{y:.0f}" width="16" height="26" rx="4" fill="{c}"/>' if rect else f'<circle id="{q}-r{k}" cx="{x:.0f}" cy="{y:.0f}" r="10" fill="{c}"/>')
                   for k, (x, y, c, rect) in enumerate(RAIN))


# ---------------------------------------------------------------- the tune: four bars in C, chord tones or a whole step from them (CLAUDE.md)
BAND = {"bpm": BPM, "outro_bars": 0, "style": "pop", "band": .62}
TUNE1 = dict(BAND, chords="C", lines=[{"text": "~ ~ ~ ~", "notes": "C4:1 E4:1 G4:1 C5:1", "rest": 0}])
TUNE2 = dict(BAND, chords="G", lines=[{"text": "~ ~ ~ ~ ~", "notes": "D5:.5 B4:.5 G4:.5 B4:.5 D5:2", "rest": 0}])
TUNE3 = dict(BAND, chords="F C", lines=[{"text": "~ ~ ~ ~ ~ ~ ~ ~ ~", "notes": "A4:1 C5:1 F5:1 C5:1 E5:.5 D5:.5 C5:.5 D5:.5 C5:1", "rest": 1}])


# ---------------------------------------------------------------- effects
def _pop(at, place, who, d=.45):
    x, y = _POS[place][who]
    return [("fromto", at, f"#{{p}}{who}_w", {"x": x, "y": y + 420}, {"x": x, "y": y, "duration": d, "ease": "back.out(1.8)"}, f"{who} pops up")]


def _puff_fx(at, name):
    out = [("fromto", at, f"#{{p}}{name}_w", {"opacity": 0}, {"opacity": 1, "duration": .01}, "")]
    for k in range(10):
        a = 2 * math.pi * k / 10; r = 120 + 40 * (k % 2)
        out.append(("fromto", at, f"#{{p}}{name}-d{k}", {"x": 0, "y": 0, "scale": .2, "opacity": 1, "transformOrigin": "50% 50%"},
                    {"x": round(r * math.cos(a)), "y": round(r * math.sin(a) * .6 - 40), "scale": 1.1, "opacity": 0, "rotation": 120, "duration": .6, "ease": "power2.out"}, ""))
    return out


def _twinkle(at0, n, until):
    out = []
    for k in range(n):
        t = round(at0 + (k * .37) % 1.2, 3); reps = max(1, int((until - t) / .5) - 1) | 1
        out.append(("fromto", t, f"#{{p}}spk-s{k}", {"scale": .1, "rotation": 0, "transformOrigin": "50% 50%"},
                    {"scale": 1, "rotation": 90, "duration": .25, "yoyo": True, "repeat": reps, "ease": "sine.inOut"}, ""))
    return out


def _bounce(sel, at, beats, amp):
    return ("fromto", round(at, 3), sel, {"y": 0}, {"y": amp, "duration": B / 2, "yoyo": True, "repeat": 2 * beats - 1, "ease": "sine.inOut"}, "")


def intro_shots():
    gx, gy = _POS["intro_gate"]["milo"]; lx, ly = _POS["intro_logo"]["milo"]
    sky = S("intro_gate", (700, 170, 1100), who="", sing=TUNE1, beat="song", tag="INTRO 1: the sky", trans="iris", cam2=(960, 470, 1760),
            hide=["milo", *FRIENDS], props=[prop("rays", rays, 250, 200), prop("spk", sparkles, 0, 0)],
            fx=[("fromto", 0, "#{p}rays-r", {"rotation": 0, "svgOrigin": "0 0"}, {"rotation": 28, "duration": 2.6, "ease": "none"}, "the sun's rays turn"),
                *_twinkle(0.05, len(SPARKLES), 2.5)])
    gate_fx = []
    for k, w in enumerate(FRIENDS):
        gate_fx += _pop(TB(k * .5), "intro_gate", w) + _puff_fx(round(TB(k * .5) + .25, 3), f"pf{k}")
    gate_fx += [("fromto", TB(1), "#{p}milo_w", {"x": -220, "y": 140}, {"x": gx, "y": gy, "duration": round(TB(3.2) - TB(1), 3), "ease": "power2.out"}, "Milo swoops in and lands on the arch"),
                ("snd", TB(1), "whoosh"),
                *[("fromto", round(TB(1) + .3 * (k + 1), 3), f"#{{p}}tr-t{k}", {"opacity": 0, "scale": .2, "transformOrigin": "50% 50%"},
                   {"opacity": 1, "scale": 1, "rotation": 90, "duration": .22, "yoyo": True, "repeat": 1}, "") for k in range(len(TRAIL))],
                _bounce("#{p}flags", 0, 4, 7), _bounce("#{p}balloons", B / 4, 3, -10)]
    gate = S("intro_gate", (960, 560, 1920), who="", sing=TUNE2, beat="song", tag="INTRO 2: the gate", cam2=(960, 540, 1840),
             props=[prop(f"pf{k}", puff, _POS["intro_gate"][w][0], _POS["intro_gate"][w][1] - 40, hidden=True) for k, w in enumerate(FRIENDS)] + [prop("tr", trail, 0, 0)],
             fx=gate_fx)
    gate["move"] = {"milo": (-220, 140, .62)}      # Milo starts off-screen up left (he swoops in)
    lfx = [("fromto", 0, "#{p}burst", {"rotation": 0, "svgOrigin": "0 0"}, {"rotation": 22, "duration": 5.6, "ease": "none"}, "the sunburst turns"),
           ("fromto", TB(0), "#{p}logo-badge", {"scale": 0, "transformOrigin": "50% 50%"}, {"scale": 1, "duration": .5, "ease": "back.out(2.2)"}, "the badge pops"),
           ("fromto", TB(0), "#{p}logo-star", {"rotation": -180, "svgOrigin": "0 0"}, {"rotation": 0, "duration": 1.2, "ease": "back.out(1.4)"}, ""),
           *[("fromto", round(TB(.5) + .08 * k, 3), f"#{{p}}logo-t{k}", {"y": -260, "opacity": 0}, {"y": 0, "opacity": 1, "duration": .35, "ease": "back.out(2)"}, "") for k in range(3)],
           *[("fromto", round(TB(1) + k * B / 4, 3), f"#{{p}}logo-a{k}", {"y": -700, "rotation": -18 + 5 * k, "opacity": 0, "transformOrigin": "50% 100%"},
              {"y": 0, "rotation": 0, "opacity": 1, "duration": .5, "ease": "bounce.out"}, "a letter drops in") for k in range(8)],
           *[("fromto", TB(3), f"#{{p}}logo-z{k}", {"scale": 2.6, "opacity": 0, "transformOrigin": "50% 50%"}, {"scale": 1, "opacity": 1, "duration": .3, "ease": "power3.in"}, "ZOO slams in") for k in range(3)],
           ("snd", round(TB(3) + .3, 3), "ding"),
           *[("fromto", round(TB(3.5) + .1 * j, 3), f"#{{p}}logo-ear{j}", {"opacity": 0, "y": 40}, {"opacity": 1, "y": 0, "duration": .3, "ease": "back.out(3)"}, "bear ears pop onto the O's") for j in range(2)],
           *[("fromto", round(TB(3) + .3, 3), f"#{{p}}cf-c{k}", {"x": 0, "y": 0, "rotation": 0, "scale": .3, "opacity": 1},
              {"x": round(dx), "y": round(dy), "rotation": round(rot), "scale": 1, "duration": .9, "ease": "power3.out"}, "") for k, (dx, dy, _, _, rot) in enumerate(CONF)],
           *[("to", round(TB(3) + 1.2, 3), f"#{{p}}cf-c{k}", {"y": "+=640", "rotation": f"+={round(rot)}", "duration": 2.4, "ease": "power1.in"}, "") for k, (_, _, _, _, rot) in enumerate(CONF)],
           *[("fromto", round(TB(4.5) + .07 * k, 3), f"#{{p}}logo-a{k}h", {"opacity": 0}, {"opacity": .85, "duration": .12, "yoyo": True, "repeat": 1}, "") for k in range(8)],
           *[("fromto", round(TB(4.5) + .56 + .07 * k, 3), f"#{{p}}logo-z{k}h", {"opacity": 0}, {"opacity": .85, "duration": .12, "yoyo": True, "repeat": 1}, "") for k in range(3)],
           ("fromto", TB(4), "#{p}milo_w", {"x": 2140, "y": 160}, {"x": lx, "y": ly, "duration": round(TB(5.6) - TB(4), 3), "ease": "power2.out"}, "Milo flies onto the badge"),
           ("snd", TB(4), "whoosh"),
           *[f for k, w in enumerate(["tumble", "sandy", "mango", "tula"]) for f in _pop(round(TB(5) + k * B / 2, 3), "intro_logo", w)],
           *_twinkle(TB(4), 6, 5.4)]
    logo_shot = S("intro_logo", (960, 540, 1920), who="", sing=TUNE3, beat="song", tag="INTRO 3: the logo", cam2=(960, 540, 1880),
                  props=[prop("spk", sparkles, 0, 120), prop("logo", logo, 960, 590, .8), prop("cf", confetti, 960, 640)], fx=lfx)
    logo_shot["move"] = {"milo": (2140, 160, .46), **{w: (_POS["intro_logo"][w][0], 1500, _SC["intro_logo"][w]) for w in FRIENDS}}
    name_fx = [("fromto", 0, "#{p}burst", {"rotation": 22, "svgOrigin": "0 0"}, {"rotation": 30, "duration": 2.4, "ease": "none"}, ""),
               *[("to", "end", f"#{{p}}{w}", {"y": "-=60", "duration": .2, "yoyo": True, "repeat": 1, "ease": "power2.out"}, "") for w in FRIENDS],
               ("to", "end", "#{p}milo", {"y": "-=40", "duration": .2, "yoyo": True, "repeat": 1}, ""),
               *[("fromto", 0, f"#{{p}}logo-ear{j}", {"opacity": 1}, {"opacity": 1, "duration": .01}, "") for j in range(2)],
               ("fromto", 0, "#{p}logo-star", {"rotation": 0, "svgOrigin": "0 0"}, {"rotation": 72, "duration": 1.2, "ease": "power2.inOut"}, ""),
               *[("fromto", 0, f"#{{p}}rn-r{k}", {"y": 0, "rotation": 0}, {"y": 1500, "rotation": 260 * (1 if k % 2 else -1), "duration": round(2.6 + (k % 5) * .25, 2), "ease": "none"}, "")
                 for k in range(len(RAIN))]]
    name = S("intro_logo", (960, 540, 1880), "The Animated Zoo!", tag="INTRO 4: Milo says the name", cam2=(960, 540, 1840),
             props=[prop("logo", logo, 960, 590, .8), prop("rn", rain, 0, 0)], fx=name_fx)
    return [sky, gate, logo_shot, name]
