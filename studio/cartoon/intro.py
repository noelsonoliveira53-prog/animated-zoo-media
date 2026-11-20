"""The Animated Zoo main intro (owner, Nov 20 2026 12:44 PM: "create a main intro for the animated zoo that will be repeated on every episode,
don't need to change anything on what we have, just for future ones"; 12:56 PM: "I want the intro to be more sophisticated with more details and effects").

The same four shots in every new long 2D episode (lesson, Guess With Milo, adventure), placed RIGHT AFTER the hook (the episode still opens on its
promise, viral packaging Nov 20). Not in the Shorts (the shots carry no `part`). About 15 s, one cut per bar line. The music is score_intro.py
(recorded instruments; approved by the owner Nov 20 4:20 PM: "the sound now is good"): the tune shots below only give the timing.
Round 3 (owner, Nov 20 4:20 PM: "improve on that animation, bring more items to make a viral entry"; and "3 dots behind the zoo name": the bear
ears behind ZOO read as stray dots and were taken out). The WHOLE cast is in it now: Milo, Tumble, Mango, Sandy, Tula, Poppy, Clover, Hazel.
  1. SKY (bar 1). A smiling sun that blinks, turning rays, drifting clouds, birds, a hot-air balloon; Milo flies across the sky with a sparkle
     trail and does a roll; the camera glides down toward the gate.
  2. THE GATE (bar 2). The seven friends pop up one per half beat, each in a puff of stars, and hop to the beat; Tumble lifts his trunk, Mango
     throws his arms up, Sandy nods; flowers pop up along the grass; bunting, balloons, bubbles, a butterfly; Milo swoops in from the lower left (under the sun) and lands on the
     arch; a star grows out of the gate and fills the picture (the wipe into the logo, on the cymbal roll).
  3. THE LOGO (bars 3-4). Out of the flash: turning sunburst, badge with a spinning star and light rings, THE, rainbow ANIMATED letter by letter,
     ZOO slams in (its O's bounce on the wood blocks), a rainbow draws on behind, fireworks, confetti (behind the friends), a shine along
     the letters, Milo flies in with a roll and lands on the badge, the friends pop up along the bottom and hop, the letters do a wave.
  4. THE NAME. Milo says "The Animated Zoo!" and each word of the logo lights up and jumps as he says it (so the shot has no caption: the logo is
     the caption); on the last chord everyone jumps, Tumble's trunk and Mango's arms go up, Milo flips, fireworks and confetti.
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
TB = lambda b: round(0.3125 + b * B, 3)        # seconds into a tune shot of beat b: the tune (and the score, score_intro.py) enters half a beat after the cut
INK = "#2a1a4a"
FRIENDS = ["tumble", "mango", "sandy", "tula", "poppy", "clover", "hazel"]      # the order they pop up at the gate, one per half beat


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
    far += (f'<g transform="translate(250 200)">{rays(p + "_rays")}</g>{clouds(p + "_cl")}<g transform="translate(1560 360) scale(.8)">{hotair(p + "_ha")}</g>'
            f'<g id="{p}_bdw" transform="translate(600 70)"><g transform="scale(1.9)">{birds(p + "_bd")}</g></g>')      # all behind the actors: Milo flies in front of the sun, the clouds and the far birds
    return far, mid, (near + f'<g id="{p}_flags">{line}{flags}</g><g id="{p}_balloons">{balloons}</g>'
                      + f'<g transform="translate(90 960)">{bubbles(p + "_ubl")}</g><g transform="translate(1835 960)">{bubbles(p + "_ubr")}</g>')      # bubbles rise behind the friends, never across a face


def bg_logo(p):
    """The logo card: a deep sky with a big sunburst that turns slowly behind everything, a soft glow in the middle, a grassy hill in front."""
    far = ('<defs><radialGradient id="%s_glow" cx="50%%" cy="45%%" r="60%%"><stop offset="0" stop-color="#bfeaff"/><stop offset=".55" stop-color="#4fb3ff"/>'
           '<stop offset="1" stop-color="#2a6fd6"/></radialGradient></defs><rect x="-500" y="-900" width="2920" height="2900" fill="url(#%s_glow)"/>' % (p, p))
    wedges = "".join(f'<path d="M0 0 L{2600 * math.cos(math.radians(a)):.0f} {2600 * math.sin(math.radians(a)):.0f} '
                     f'L{2600 * math.cos(math.radians(a + 9)):.0f} {2600 * math.sin(math.radians(a + 9)):.0f}Z" fill="#ffffff" opacity=".13"/>' for a in range(0, 360, 18))
    far += f'<g transform="translate(960 470)"><g id="{p}_burst">{wedges}</g></g>'
    far += f'<g transform="translate(960 960)">' + "".join(f'<path id="{p}_rb-a{k}" d="M{-r} 0 A{r} {r} 0 0 1 {r} 0" stroke="{c}" stroke-width="26" fill="none" opacity=".9" '
                                                        f'stroke-dasharray="{math.pi * r:.0f}" stroke-dashoffset="{math.pi * r:.0f}"/>' for k, (r, c) in enumerate(zip(RB_R, RB))) + '</g>'      # drawn on in the logo shot, behind the friends; its feet go behind the hill
    near = ('<path d="M-500 930 C200 860 700 900 1200 870 S2000 880 2420 920 L2420 2000 L-500 2000Z" fill="#7cc95e"/>'
            '<path d="M-500 960 C300 900 900 950 1400 915 S2100 930 2420 960 L2420 2000 L-500 2000Z" fill="#6bbd50"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/><circle cx="{x + 16}" cy="{y + 6}" r="7" fill="#fff"/>'
                      for x, y, c in ((140, 1010, "#ff7aa2"), (520, 1030, art.SUN), (1400, 1020, "#ff7aa2"), (1780, 1035, art.SUN))))
    # confetti, the confetti rain and the bubbles are drawn here, BEHIND the friends and the logo: nothing falls across a face or a letter (stills, Nov 20: a piece sat on Milo's eye)
    near += (f'<g id="{p}_cfw" transform="translate(960 640)" opacity="0">{confetti(p + "_cf")}</g>{rain(p + "_rn")}'
             f'<g transform="translate(85 960)">{bubbles(p + "_ubl")}</g><g transform="translate(1840 960)">{bubbles(p + "_ubr")}</g>')
    return far, "", near


art.BG["intro_gate"] = bg_intro; art.PLACE["intro_gate"] = "the zoo gate (main intro)"
art.BG["intro_logo"] = bg_logo; art.PLACE["intro_logo"] = "the logo (main intro)"

# (name, rig, x, y, size, mirrored[, flies]). Sizes and places from the rigs' measured outlines (Nov 20): no friend stands inside another, the
# left-hand friends face right and the right-hand friends face left (toward the middle).
INTRO_STAGES = {
    "intro_gate": [("mango", "monkey", 180, 880, .5), ("tumble", "tumble", 450, 875, .55), ("poppy", "bear", 880, 860, .40), ("clover", "lamb", 1165, 860, .40, True),
                   ("sandy", "calf", 1420, 878, .48), ("tula", "turtle", 1750, 888, .45, True), ("hazel", "hedgehog", 1000, 985, .40),
                   ("milo", "milo", 960, 390, .62, False, True)],      # Milo sits on the top of the arch (its top edge is y 385 at the middle)
    "intro_logo": [("mango", "monkey", 160, 1005, .40), ("tumble", "tumble", 380, 990, .44), ("poppy", "bear", 715, 1018, .32), ("hazel", "hedgehog", 945, 1030, .36),
                   ("clover", "lamb", 1170, 1018, .32, True), ("sandy", "calf", 1540, 995, .38, True), ("tula", "turtle", 1775, 1012, .38, True),
                   ("milo", "milo", 960, 236, .46, False, True)],      # Milo stands on the badge (its top is y 232)
}
_FLIP = {k: {a[0]: (len(a) > 5 and bool(a[5])) for a in v} for k, v in INTRO_STAGES.items()}
_POS = {k: {a[0]: a[2:4] for a in v} for k, v in INTRO_STAGES.items()}
_SC = {k: {a[0]: a[4] for a in v} for k, v in INTRO_STAGES.items()}


# ---------------------------------------------------------------- props (drawn at their own origin; fx reach their parts as "#{p}<prop>-<part>")
def _star4(r, c="#fff"):
    return f'<path d="M0 {-r} Q{r * .18:.1f} {-r * .18:.1f} {r} 0 Q{r * .18:.1f} {r * .18:.1f} 0 {r} Q{-r * .18:.1f} {r * .18:.1f} {-r} 0 Q{-r * .18:.1f} {-r * .18:.1f} 0 {-r}Z" fill="{c}"/>'


def _star5(r, c, k=.45):
    pts = " ".join(f"{(r if i % 2 == 0 else r * k) * math.sin(math.pi * i / 5):.1f},{-(r if i % 2 == 0 else r * k) * math.cos(math.pi * i / 5):.1f}" for i in range(10))
    return f'<polygon points="{pts}" fill="{c}"/>'


def rays(q):
    """Sun rays that turn, a fresh sun with a smiling face that can blink (eL, eR), a glow (sits exactly on the backdrop's sun; drawn in the backdrop, behind the actors)."""
    r = "".join(f'<path d="M0 0 L{300 * math.cos(math.radians(a)):.0f} {300 * math.sin(math.radians(a)):.0f} L{300 * math.cos(math.radians(a + 11)):.0f} '
                f'{300 * math.sin(math.radians(a + 11)):.0f}Z" fill="#fff6c4" opacity=".55"/>' for a in range(0, 360, 30))
    face = (f'<g id="{q}-eL"><ellipse cx="-30" cy="-8" rx="9" ry="13" fill="{INK}"/><circle cx="-27" cy="-13" r="3.5" fill="#fff"/></g>'
            f'<g id="{q}-eR"><ellipse cx="30" cy="-8" rx="9" ry="13" fill="{INK}"/><circle cx="33" cy="-13" r="3.5" fill="#fff"/></g>'
            f'<ellipse cx="-50" cy="16" rx="13" ry="8" fill="#ff9d6b" opacity=".75"/><ellipse cx="50" cy="16" rx="13" ry="8" fill="#ff9d6b" opacity=".75"/>'
            f'<path d="M-24 18 Q0 46 24 18" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    return (f'<g id="{q}-r">{r}</g><circle r="118" fill="#fff3a8" opacity=".55"/><circle r="88" fill="{art.SUN}"/><circle cx="-50" cy="-52" r="13" fill="#fff" opacity=".45"/>'
            f'<g id="{q}-face">{face}</g>')


SPARKLES = [(130, -280), (520, -150), (860, -330), (1180, -190), (1520, -300), (1780, -120), (330, 40), (1060, 30), (1660, 120), (720, 150)]
def sparkles(q):
    return "".join(f'<g transform="translate({x} {y})"><g id="{q}-s{k}">{_star4(26 if k % 3 else 38)}</g></g>' for k, (x, y) in enumerate(SPARKLES))


def puff(q):
    """A ring of little stars and dots that bursts out when a friend pops up."""
    cols = [art.SUN, "#ff7aa2", "#fff", "#5cc473", "#b48cff", art.MILO_BLUE]
    return "".join(f'<g id="{q}-d{k}">' + (_star5(18, cols[k % 6]) if k % 2 == 0 else f'<circle r="10" fill="{cols[k % 6]}"/>') + '</g>' for k in range(10))


TRAIL = [(-55, 547), (146, 494), (335, 444), (523, 395), (677, 354), (818, 317)]      # along Milo's swoop to the arch (from the lower left: from the upper left he crossed the sun's face, frames Nov 20)
def trail(q):
    return "".join(f'<g transform="translate({x} {y})"><g id="{q}-t{k}" opacity="0">{_star4(24 - k * 1.5, art.SUN if k % 2 else "#fff")}</g></g>' for k, (x, y) in enumerate(TRAIL))


_W = {"A": .64, "N": .66, "I": .31, "M": .86, "T": .58, "E": .56, "D": .66, "Z": .58, "O": .70, "H": .66}
RAINBOW = ["#ff4d6d", "#ff8a1f", "#ffd23f", "#4cc95a", "#2fb5ff", "#3a7bff", "#9b5cff", "#ff5fb8"]
def _word(q, name, text, size, y, cols, ls=.03):
    xs = []; w = sum(_W[c] for c in text) * size + ls * size * (len(text) - 1); x = -w / 2
    for c in text: xs.append(x + _W[c] * size / 2); x += _W[c] * size + ls * size
    out = ""; t = f'font-family="Baloo" font-weight="800" font-size="{size}" text-anchor="middle" stroke-linejoin="round" paint-order="stroke"'
    for k, (c, cx) in enumerate(zip(text, xs)):
        out += (f'<g id="{q}-{name}{k}" class="L{name}"><text x="{cx:.0f}" y="{y + size * .07:.0f}" {t} fill="{INK}" stroke="{INK}" stroke-width="{size * .16:.0f}" opacity=".35">{c}</text>'
                f'<text x="{cx:.0f}" y="{y:.0f}" {t} fill="{cols[k % len(cols)]}" stroke="{INK}" stroke-width="{size * .12:.0f}">{c}</text>'
                f'<text id="{q}-{name}{k}h" class="L{name}h" x="{cx:.0f}" y="{y:.0f}" {t} fill="#ffffff" opacity="0">{c}</text></g>')
    return out, xs


def logo(q):
    """THE / ANIMATED (rainbow) / ZOO (sunny), under a badge with a turning star. Origin: the middle of 'ANIMATED'. Nothing is drawn behind the
    letters (owner, Nov 20: the bear ears behind ZOO looked like three stray dots)."""
    badge = (f'<g transform="translate(0 -330)"><circle r="122" fill="#fff"/><circle r="104" fill="{art.MILO_BLUE}"/>'
             f'<circle id="{q}-dash" r="104" fill="none" stroke="#bfe0ff" stroke-width="8" stroke-dasharray="14 18"/><g id="{q}-star">{_star5(70, art.SUN)}</g></g>')
    the, _ = _word(q, "t", "THE", 78, -150, ["#ffffff"])
    ani, _ = _word(q, "a", "ANIMATED", 190, 60, RAINBOW)
    zoo, zx = _word(q, "z", "ZOO", 250, 300, [art.SUN])
    return f'<g id="{q}-badge">{badge}</g>{the}{ani}{zoo}'


def firework(q, c1="#ff7aa2", c2=None):
    """One burst: twelve streaks and dots flying out from a point (shown, grown and faded by _firework)."""
    c2 = c2 or art.SUN
    rs = "".join(f'<g transform="rotate({a})"><path d="M0 -46 L0 -118" stroke="{c1 if k % 2 else c2}" stroke-width="13" stroke-linecap="round"/>'
                 f'<circle cx="0" cy="-150" r="9" fill="{c2 if k % 2 else c1}"/></g>' for k, a in enumerate(range(0, 360, 30)))
    return f'<g id="{q}-g">{rs}<circle r="15" fill="#fff"/></g>'


def flash(q):
    return f'<rect id="{q}-r" x="-700" y="-700" width="3400" height="2600" fill="#fff6c4"/>'


def starwipe(q):
    return f'<g id="{q}-g">{_star5(100, "#fff6c4")}</g>'


FLOWERS = [(60, 1030, "#ff7aa2"), (300, 1046, "#ffffff"), (640, 1036, "#b48cff"), (1300, 1042, "#ff7aa2"), (1560, 1046, "#ffffff"), (1850, 1030, "#b48cff")]
def flowers(q):
    out = ""
    for k, (x, y, c) in enumerate(FLOWERS):
        petals = "".join(f'<circle cx="{17 * math.cos(math.radians(a)):.1f}" cy="{-66 + 17 * math.sin(math.radians(a)):.1f}" r="13" fill="{c}"/>' for a in range(0, 360, 72))
        out += (f'<g transform="translate({x} {y})"><g id="{q}-f{k}"><path d="M0 0 Q-6 -30 0 -62" stroke="#3f9a4c" stroke-width="7" fill="none" stroke-linecap="round"/>'
                f'<ellipse cx="-13" cy="-22" rx="13" ry="6" fill="#4fb565" transform="rotate(-28 -13 -22)"/><ellipse cx="13" cy="-34" rx="13" ry="6" fill="#4fb565" transform="rotate(28 13 -34)"/>'
                f'{petals}<circle cx="0" cy="-66" r="10" fill="{art.SUN}"/></g></g>')
    return out


SKYTRAIL = [(1420 - 1620 * f, 60 + 820 * f - 120, f) for f in (.18, .32, .46, .6, .74)]      # behind Milo as he crosses the sky
def skytrail(q):
    return "".join(f'<g transform="translate({x:.0f} {y:.0f})"><g id="{q}-t{k}" opacity="0">{_star4(30 - k * 2, art.SUN if k % 2 else "#fff")}</g></g>' for k, (x, y, _) in enumerate(SKYTRAIL))


_rnd = random.Random(7)
CONF = [(_rnd.uniform(-900, 900), _rnd.uniform(-560, -120), _rnd.choice(RAINBOW + [art.SUN, "#fff"]), _rnd.random() < .5, _rnd.uniform(-540, 540)) for _ in range(44)]
def confetti(q):
    return "".join((f'<rect id="{q}-c{k}" x="-9" y="-14" width="18" height="28" rx="4" fill="{c}"/>' if rect else f'<circle id="{q}-c{k}" r="11" fill="{c}"/>')
                   for k, (_, _, c, rect, _) in enumerate(CONF))


RAIN = [(_rnd.uniform(-60, 1980), _rnd.uniform(-700, -60), _rnd.choice(RAINBOW + [art.SUN, "#fff"]), _rnd.random() < .5) for _ in range(40)]
def rain(q):
    return "".join((f'<rect id="{q}-r{k}" x="{x - 8:.0f}" y="{y:.0f}" width="16" height="26" rx="4" fill="{c}"/>' if rect else f'<circle id="{q}-r{k}" cx="{x:.0f}" cy="{y:.0f}" r="10" fill="{c}"/>')
                   for k, (x, y, c, rect) in enumerate(RAIN))


CLOUDS = [(1250, 120, 1.0), (1650, 260, .7), (380, 330, .6)]
def clouds(q):
    one = lambda s: (f'<g transform="scale({s})"><ellipse cx="0" cy="0" rx="120" ry="48" fill="#fff"/><ellipse cx="-60" cy="-26" rx="62" ry="50" fill="#fff"/>'
                     f'<ellipse cx="40" cy="-40" rx="70" ry="58" fill="#fff"/><ellipse cx="0" cy="18" rx="130" ry="22" fill="#e3f2ff"/></g>')
    return "".join(f'<g transform="translate({x} {y})"><g id="{q}-c{k}" opacity=".95">{one(sc)}</g></g>' for k, (x, y, sc) in enumerate(CLOUDS))


def birds(q):
    """Three little birds far away, flapping (two curves each)."""
    out = ""
    for k, (x, y, s) in enumerate(((0, 0, 1), (70, 34, .8), (-56, 46, .7))):
        out += (f'<g transform="translate({x} {y}) scale({s})"><g id="{q}-b{k}"><path d="M-26 0 Q-13 -16 0 0 Q13 -16 26 0" stroke="{INK}" stroke-width="6" '
                f'fill="none" stroke-linecap="round" opacity=".7"/></g></g>')
    return out


def hotair(q):
    """A striped hot-air balloon far off (small, slow)."""
    cols = ["#ff7aa2", art.SUN, art.MILO_BLUE, "#5cc473", "#ff7aa2"]
    stripes = "".join(f'<path d="M{-60 + 24 * k} -40 Q{-62 + 24 * k + 12} 60 {-24 + 12 * k} 70 L{-12 + 12 * k} 70 Q{-40 + 24 * k + 12} 60 {-36 + 24 * k} -40Z" fill="{c}"/>' for k, c in enumerate(cols))
    return (f'<g id="{q}-g"><clipPath id="{q}-cl"><ellipse cx="0" cy="0" rx="62" ry="74"/></clipPath><ellipse cx="0" cy="0" rx="62" ry="74" fill="{art.SUN}"/>'
            f'<g clip-path="url(#{q}-cl)">{stripes}</g><ellipse cx="-20" cy="-30" rx="12" ry="20" fill="#fff" opacity=".45"/>'
            f'<path d="M-22 70 L-14 100 M22 70 L14 100" stroke="#8a5a2b" stroke-width="4"/><rect x="-18" y="100" width="36" height="26" rx="6" fill="#b5793f"/></g>')


BUB = [(-30, 0, 34), (40, -90, 24), (-50, -170, 20), (20, -230, 30), (55, -40, 17), (-40, -300, 22)]
def bubbles(q):
    return "".join(f'<g transform="translate({x} {y})"><g id="{q}-u{k}"><circle r="{r}" fill="#ffffff" opacity=".34" stroke="#ffffff" stroke-width="4" stroke-opacity=".95"/>'
                   f'<ellipse cx="{-r * .35:.0f}" cy="{-r * .38:.0f}" rx="{r * .28:.0f}" ry="{r * .18:.0f}" fill="#fff" opacity=".8"/></g></g>' for k, (x, y, r) in enumerate(BUB))


def butterfly(q, c1="#ff7aa2", c2=art.SUN):
    return (f'<g id="{q}-f"><g id="{q}-wl"><ellipse cx="-16" cy="-8" rx="17" ry="13" fill="{c1}"/><ellipse cx="-12" cy="10" rx="11" ry="9" fill="{c2}"/></g>'
            f'<g id="{q}-wr"><ellipse cx="16" cy="-8" rx="17" ry="13" fill="{c1}"/><ellipse cx="12" cy="10" rx="11" ry="9" fill="{c2}"/></g>'
            f'<rect x="-3" y="-14" width="6" height="30" rx="3" fill="{INK}"/></g>')


def rings(q):
    return "".join(f'<circle id="{q}-r{k}" r="112" fill="none" stroke="#ffffff" stroke-width="10" opacity="0"/>' for k in range(3))


RB = ["#ff4d6d", "#ff8a1f", "#ffd23f", "#4cc95a", "#2fb5ff", "#9b5cff"]
RB_R = [560 - 26 * k for k in range(6)]
def rainbow(q):
    arcs = "".join(f'<path id="{q}-a{k}" d="M{-r} 0 A{r} {r} 0 0 1 {r} 0" stroke="{c}" stroke-width="26" fill="none" opacity=".85" '
                   f'stroke-dasharray="{math.pi * r:.0f}" stroke-dashoffset="{math.pi * r:.0f}"/>' for k, (r, c) in enumerate(zip(RB_R, RB)))
    puffs = "".join(f'<g transform="translate({sx * 500} 6)"><ellipse cx="0" cy="0" rx="110" ry="46" fill="#fff"/><ellipse cx="-40" cy="-30" rx="56" ry="44" fill="#fff"/>'
                    f'<ellipse cx="38" cy="-34" rx="62" ry="50" fill="#fff"/></g>' for sx in (-1, 1))
    return f'{arcs}<g id="{q}-feet" opacity="0">{puffs}</g>'


RISE = [(150, 0, "#ff7aa2"), (1760, 60, art.SUN), (300, 120, art.MILO_BLUE), (1640, 180, "#5cc473")]
def rising(q):
    return "".join(f'<g transform="translate({x} {960 + y})"><g id="{q}-l{k}"><path d="M0 52 q-8 50 6 110" stroke="#fff" stroke-width="3" fill="none"/>'
                   f'<ellipse rx="40" ry="50" fill="{c}"/><ellipse cx="-12" cy="-18" rx="9" ry="14" fill="#fff" opacity=".5"/><path d="M-6 48 l6 9 l6 -9Z" fill="{c}"/></g></g>'
                   for k, (x, y, c) in enumerate(RISE))


def _float_bubbles(name, at, dur):
    return [("fromto", round(at + .13 * k, 3), f"#{{p}}{name}-u{k}", {"y": 120, "x": 0, "opacity": 0}, {"y": -420 - 40 * k, "opacity": 1, "duration": dur, "ease": "sine.out"}, "")
            for k in range(len(BUB))] + [("fromto", round(at + .13 * k, 3), f"#{{p}}{name}-u{k}", {"x": -14}, {"x": 14, "duration": .55, "yoyo": True, "repeat": 5, "ease": "sine.inOut"}, "")
            for k in range(len(BUB))]


def _flutter(name, at, dur, path):
    (x0, y0), (x1, y1) = path; reps = int(dur / .12)
    return [("fromto", at, f"#{{p}}{name}-wl", {"scaleX": 1, "transformOrigin": "100% 50%"}, {"scaleX": .25, "duration": .12, "yoyo": True, "repeat": reps, "ease": "sine.inOut"}, ""),
            ("fromto", at, f"#{{p}}{name}-wr", {"scaleX": 1, "transformOrigin": "0% 50%"}, {"scaleX": .25, "duration": .12, "yoyo": True, "repeat": reps, "ease": "sine.inOut"}, ""),
            ("fromto", at, f"#{{p}}{name}_w", {"x": x0, "y": y0}, {"x": x1, "y": y1, "duration": dur, "ease": "sine.inOut"}, ""),
            ("fromto", at, f"#{{p}}{name}-f", {"y": 0}, {"y": -26, "duration": .45, "yoyo": True, "repeat": int(dur / .45), "ease": "sine.inOut"}, "")]


def _rings(at, n, until):
    out = []
    for k in range(n):
        t = round(at + k * B * 2 / n, 3)
        out.append(("fromto", t, f"#{{p}}rg-r{k}", {"scale": 1, "opacity": .75, "transformOrigin": "50% 50%"},
                    {"scale": 2.1, "opacity": 0, "duration": B * 2, "repeat": max(0, int((until - t) / (B * 2)) - 1), "ease": "power1.out"}, ""))
    return out


# ---------------------------------------------------------------- the tune: four bars in C, chord tones or a whole step from them (CLAUDE.md)
BAND = {"bpm": BPM, "outro_bars": 0, "style": "pop", "band": .62, "mute": True}      # the tune gives the timing; the music is the score on recorded instruments (score_intro.py)
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


def _plus(at, d):
    """A moment d seconds after `at` (seconds into the shot, or "end" / "end+0.3")."""
    if isinstance(at, (int, float)): return round(at + d, 3)
    base, _, off = at.partition("+"); return f"{base}+{float(off or 0) + d:.3f}"


def _hop(who, at, amp=44):
    """A silent hop (the engine's "hop" plays a boing; here every sound is in the score)."""
    return ("to", at, f"#{{p}}{who}", {"y": f"-={amp}", "duration": .16, "yoyo": True, "repeat": 1, "ease": "power2.out"}, "")


def _firework(at, name):
    return [("fromto", at, f"#{{p}}{name}_w", {"opacity": 0}, {"opacity": 1, "duration": .01}, ""),
            ("fromto", at, f"#{{p}}{name}-g", {"scale": .1, "rotation": 0, "svgOrigin": "0 0"}, {"scale": 1, "rotation": 18, "duration": .75, "ease": "power2.out"}, "a firework"),
            ("to", _plus(at, .42), f"#{{p}}{name}_w", {"opacity": 0, "duration": .33, "ease": "power1.in"}, "")]


def _confetti(at, name):
    return ([("fromto", at, f"#{{p}}{name}w", {"opacity": 0}, {"opacity": 1, "duration": .01}, "")]      # the confetti is in the backdrop (bg_logo), behind the friends
            + [("fromto", at, f"#{{p}}{name}-c{k}", {"x": 0, "y": 0, "rotation": 0, "scale": .3, "opacity": 1},
                {"x": round(dx), "y": round(dy), "rotation": round(rot), "scale": 1, "duration": .9, "ease": "power3.out"}, "confetti" if k == 0 else "") for k, (dx, dy, _, _, rot) in enumerate(CONF)]
            + [("to", _plus(at, .9), f"#{{p}}{name}-c{k}", {"y": "+=640", "rotation": f"+={round(rot)}", "duration": 2.4, "ease": "power1.in"}, "") for k, (_, _, _, _, rot) in enumerate(CONF)])


def _blink(at, eyes=("eL", "eR")):
    return [("fromto", at, f"#{{p}}rays-{e}", {"scaleY": 1, "transformOrigin": "50% 50%"}, {"scaleY": .1, "duration": .08, "yoyo": True, "repeat": 1}, "") for e in eyes]


def _rainbow_fx(at, draw=True):
    out = []
    for k, r in enumerate(RB_R):
        L = round(math.pi * r)
        out.append(("fromto", round(at + .06 * k, 3) if draw else at, f"#{{p}}rb-a{k}", {"strokeDashoffset": L if draw else 0}, {"strokeDashoffset": 0, "duration": .7 if draw else .01, "ease": "power2.out"}, "the rainbow draws on" if k == 0 and draw else ""))
    return out


FW = [(300, 330, "#ff7aa2", None), (1620, 300, "#2fb5ff", "#ffffff"), (480, 170, "#4cc95a", None), (1450, 160, "#ff8a1f", "#ffffff"), (250, 520, "#9b5cff", None), (1680, 520, "#ff4d6d", None)]
def _fw_props(n=6): return [prop(f"fw{k}", (lambda q, c=c, d=d: firework(q, c, d)), x, y, hidden=True) for k, (x, y, c, d) in enumerate(FW[:n])]


def intro_shots():
    gx, gy = _POS["intro_gate"]["milo"]; lx, ly = _POS["intro_logo"]["milo"]
    # every picture hit lands on its note in the score (score_intro.py): a bounce reaches the ground ~0.18 s after it starts, a pop ~0.12 s
    LAND, POP = .18, .12
    # ---------------- 1. THE SKY
    sky = S("intro_gate", (660, 170, 1100), who="", sing=TUNE1, beat="song", tag="INTRO 1: the sky", trans="iris", cam2=(960, 470, 1760),
            hide=list(FRIENDS), props=[prop("spk", sparkles, 0, 0), prop("st", skytrail, 0, 0)],
            fx=[("fromto", 0, "#{p}rays-r", {"rotation": 0, "svgOrigin": "0 0"}, {"rotation": 28, "duration": 3.44, "ease": "none"}, "the sun's rays turn"),
                *_blink(TB(1)), *_blink(TB(3), ("eR",)),
                *_twinkle(0.05, len(SPARKLES), 2.5),
                *[("fromto", 0, f"#{{p}}cl-c{k}", {"x": 0}, {"x": 70 + 30 * k, "duration": 3.44, "ease": "none"}, "") for k in range(len(CLOUDS))],
                ("fromto", 0, "#{p}bdw", {"x": 600, "y": 70}, {"x": 1500, "y": 20, "duration": 3.44, "ease": "none"}, "birds fly across, far away (they start right of the sun: at 200 they crossed its face)"),
                *[("fromto", .07 * k, f"#{{p}}bd-b{k}", {"scaleY": 1, "transformOrigin": "50% 100%"}, {"scaleY": -.6, "duration": .16, "yoyo": True, "repeat": 19, "ease": "sine.inOut"}, "") for k in range(3)],
                ("fromto", 0, "#{p}ha-g", {"y": 30, "rotation": -3, "transformOrigin": "50% 0%"}, {"y": -30, "rotation": 3, "duration": 3.44, "ease": "sine.inOut"}, "a hot-air balloon rises far away"),
                ("fromto", .05, "#{p}milo_w", {"x": 1420, "y": 60}, {"x": -200, "y": 880, "duration": 2.4, "ease": "none"}, "Milo flies across the sky, under the sun"),
                ("fromto", .8, "#{p}milo", {"rotation": 0, "svgOrigin": "0 -170"}, {"rotation": -360, "duration": .55, "ease": "power1.inOut"}, "Milo does a roll"),
                *[("fromto", round(.05 + 2.4 * f + .16, 3), f"#{{p}}st-t{k}", {"opacity": 0, "scale": .2, "transformOrigin": "50% 50%"},
                   {"opacity": 1, "scale": 1, "rotation": 90, "duration": .24, "yoyo": True, "repeat": 1}, "") for k, (_, _, f) in enumerate(SKYTRAIL)]])
    sky["move"] = {"milo": (1420, 60, .62)}      # Milo starts outside the picture, on the right
    # ---------------- 2. THE GATE
    G = "intro_gate"; gate_fx = []
    for k, w in enumerate(FRIENDS):
        gate_fx += _pop(round(TB(k * .5) - POP, 3), G, w) + _puff_fx(TB(k * .5), f"pf{k}")
        gate_fx += [_hop(w, TB(b)) for b in (k * .5 + 1, k * .5 + 2) if b <= 3]      # each one hops on the beats after it lands
    gate_fx += [_hop(w, TB(3.5), 56) for w in FRIENDS]                               # everyone greets Milo
    gate_fx += [("fromto", TB(1), "#{p}milo_w", {"x": -220, "y": 700}, {"x": gx, "y": gy, "duration": round(TB(3.2) - TB(1), 3), "ease": "power2.out"}, "Milo swoops in and lands on the arch"),
                *[("fromto", round(TB(1) + .3 * (k + 1), 3), f"#{{p}}tr-t{k}", {"opacity": 0, "scale": .2, "transformOrigin": "50% 50%"},
                   {"opacity": 1, "scale": 1, "rotation": 90, "duration": .22, "yoyo": True, "repeat": 1}, "") for k in range(len(TRAIL))],
                *_puff_fx(TB(3.2), "pfm"),
                ("trunk", TB(2), "tumble", -75, .3), ("trunk", TB(3.25), "tumble", 0, .3),
                ("arm", TB(2.5), "mango", "r", -105), ("arm", TB(2.5), "mango", "l", 105),      # out and up: straight up (160) hides the arms behind his head (stills)
                ("nod", TB(2), "sandy"),
                _bounce("#{p}flags", 0, 4, 7), _bounce("#{p}balloons", B / 4, 3, -10),
                *_float_bubbles("ubl", .1, 2.8), *_float_bubbles("ubr", .4, 2.8),
                *_flutter("bf2", 0, 3.1, ((1840, 660), (1790, 290))),      # one butterfly, on the right: a second one on the left sat on Milo's chest at 4.62 s, then at the frame edge
                *[("fromto", TB(.25 + .5 * k), f"#{{p}}fl-f{k}", {"scale": 0, "transformOrigin": "50% 100%"}, {"scale": 1, "duration": .3, "ease": "back.out(2.4)"}, "a flower pops up" if k == 0 else "") for k in range(len(FLOWERS))],
                *[("to", round(TB(.25 + .5 * k) + .3, 3), f"#{{p}}fl-f{k}", {"rotation": 7 * (1 if k % 2 else -1), "transformOrigin": "50% 100%", "duration": B / 2, "yoyo": True, "repeat": 7, "ease": "sine.inOut"}, "") for k in range(len(FLOWERS))],
                ("fromto", 0, "#{p}rays-r", {"rotation": 28, "svgOrigin": "0 0"}, {"rotation": 54, "duration": 3.13, "ease": "none"}, ""), *_blink(TB(2)),
                *[("fromto", 0, f"#{{p}}cl-c{k}", {"x": 70 + 30 * k}, {"x": 134 + 57 * k, "duration": 3.13, "ease": "none"}, "") for k in range(len(CLOUDS))],
                ("fromto", 0, "#{p}ha-g", {"y": -30, "rotation": 3, "transformOrigin": "50% 0%"}, {"y": -80, "rotation": -3, "duration": 3.13, "ease": "sine.inOut"}, ""),
                ("fromto", 0, "#{p}bdw", {"x": 1500, "y": 20}, {"x": 2400, "y": -40, "duration": 3.13, "ease": "none"}, ""),
                *[("fromto", .07 * k, f"#{{p}}bd-b{k}", {"scaleY": 1, "transformOrigin": "50% 100%"}, {"scaleY": -.6, "duration": .16, "yoyo": True, "repeat": 19, "ease": "sine.inOut"}, "") for k in range(3)],
                ("fromto", TB(4), "#{p}sw_w", {"opacity": 0}, {"opacity": 1, "duration": .01}, ""),
                ("fromto", TB(4), "#{p}sw-g", {"scale": 0, "rotation": -40, "svgOrigin": "0 0"}, {"scale": 34, "rotation": 30, "duration": .31, "ease": "power2.in"}, "a star grows out of the gate and fills the picture")]
    gate = S(G, (960, 560, 1920), who="", sing=TUNE2, beat="song", tag="INTRO 2: the gate", cam2=(960, 540, 1840),
             props=[prop("fl", flowers, 0, 0), prop("bf2", lambda q: butterfly(q, art.MILO_BLUE, "#b48cff"), 0, 0)]
                   + [prop(f"pf{k}", puff, _POS[G][w][0], _POS[G][w][1] - 40, hidden=True) for k, w in enumerate(FRIENDS)]
                   + [prop("pfm", puff, gx, gy - 60, hidden=True), prop("tr", trail, 0, 0), prop("sw", starwipe, 960, 520, hidden=True)],
             fx=gate_fx)
    gate["move"] = {"milo": (-220, 700, .62)}      # Milo starts off-screen on the left, where he left the sky shot, and climbs to the arch under the sun
    # ---------------- 3. THE LOGO
    L = "intro_logo"; Z = TB(3)                # ZOO lands on the brass + low piano + cymbal; the bell, the confetti and the O's bounce half a beat later
    pops = [("tumble", 5), ("sandy", 5.5), ("mango", 6), ("poppy", 6), ("tula", 6.5), ("clover", 6.5), ("hazel", 7)]
    lfx = [("fromto", 0, "#{p}fx-r", {"opacity": 1}, {"opacity": 0, "duration": TB(0), "ease": "power2.in"}, "out of the flash"),
           ("fromto", 0, "#{p}burst", {"rotation": 0, "svgOrigin": "0 0"}, {"rotation": 22, "duration": 5.6, "ease": "none"}, "the sunburst turns"),
           ("fromto", round(TB(0) - POP, 3), "#{p}logo-badge", {"scale": 0, "transformOrigin": "50% 50%"}, {"scale": 1, "duration": .5, "ease": "back.out(2.2)"}, "the badge pops"),
           ("fromto", TB(0), "#{p}logo-star", {"rotation": -180, "svgOrigin": "0 0"}, {"rotation": 0, "duration": 1.2, "ease": "back.out(1.4)"}, ""),
           ("fromto", 0, "#{p}logo-dash", {"rotation": 0, "svgOrigin": "0 0"}, {"rotation": 90, "duration": 5.3, "ease": "none"}, ""),
           *_rings(TB(.5), 3, 5.6),
           *[("fromto", round(TB(.5) + k * B / 8 - .15, 3), f"#{{p}}logo-t{k}", {"y": -260, "opacity": 0}, {"y": 0, "opacity": 1, "duration": .35, "ease": "back.out(2)"}, "") for k in range(3)],
           *[("fromto", round(TB(1) + k * B / 4 - LAND, 3), f"#{{p}}logo-a{k}", {"y": -700, "rotation": -18 + 5 * k, "opacity": 0, "transformOrigin": "50% 100%"},
              {"y": 0, "rotation": 0, "opacity": 1, "duration": .5, "ease": "bounce.out"}, "a letter drops in") for k in range(8)],
           *[("fromto", round(TB(1) + k * B / 4, 3), f"#{{p}}logo-a{k}", {"scaleX": 1.2, "scaleY": .76}, {"scaleX": 1, "scaleY": 1, "duration": .32, "ease": "back.out(3)"}, "") for k in range(8)],
           *[("fromto", round(Z - .3, 3), f"#{{p}}logo-z{k}", {"scale": 2.6, "opacity": 0, "transformOrigin": "50% 50%"}, {"scale": 1, "opacity": 1, "duration": .3, "ease": "power3.in"}, "ZOO slams in") for k in range(3)],
           *[("fromto", Z, f"#{{p}}logo-z{k}", {"scaleX": 1.16, "scaleY": .8}, {"scaleX": 1, "scaleY": 1, "duration": .35, "ease": "elastic.out(1, .4)"}, "") for k in range(3)],
           *_rainbow_fx(Z), *_firework(Z, "fw0"), *_firework(round(Z + .16, 3), "fw1"),
           *[("to", round(TB(3.5) + .1 * j, 3), f"#{{p}}logo-z{j + 1}", {"y": -34, "duration": .12, "yoyo": True, "repeat": 1, "ease": "power2.out"}, "the O's bounce") for j in range(2)],
           *_puff_fx(TB(3.5), "pfe"), *_confetti(TB(3.5), "cf"),
           *_firework(TB(4.5), "fw2"), *_firework(TB(5.5), "fw3"), *_firework(TB(6.5), "fw4"), *_firework(TB(7.25), "fw5"),
           *[("fromto", round(TB(4.5) + .07 * k, 3), f"#{{p}}logo-a{k}h", {"opacity": 0}, {"opacity": .85, "duration": .12, "yoyo": True, "repeat": 1}, "") for k in range(8)],
           *[("fromto", round(TB(4.5) + .56 + .07 * k, 3), f"#{{p}}logo-z{k}h", {"opacity": 0}, {"opacity": .85, "duration": .12, "yoyo": True, "repeat": 1}, "") for k in range(3)],
           ("fromto", TB(4), "#{p}milo_w", {"x": 2140, "y": 160}, {"x": lx, "y": ly, "duration": round(TB(5.6) - TB(4), 3), "ease": "power2.out"}, "Milo flies onto the badge"),
           ("fromto", round(TB(4) + .12, 3), "#{p}milo", {"rotation": 0, "svgOrigin": "0 -170"}, {"rotation": -360, "duration": .5, "ease": "power1.inOut"}, "Milo does a roll"),
           *[f for w, b in pops for f in _pop(round(TB(b) - POP, 3), L, w)],
           *[_hop(w, TB(b2)) for w, b in pops for b2 in (b + 1, b + 2) if b2 <= 7.5],
           ("to", TB(7), "#{p}logo_w .La", {"y": -30, "duration": .1, "ease": "power2.out", "stagger": {"each": .045, "repeat": 1, "yoyo": True}}, "the letters do a wave"),
           ("to", round(TB(7) + .3, 3), "#{p}logo_w .Lz", {"y": -30, "duration": .1, "ease": "power2.out", "stagger": {"each": .045, "repeat": 1, "yoyo": True}}, ""),
           *[("fromto", round(.2 + .35 * k, 3), f"#{{p}}rs-l{k}", {"y": 0, "x": 0}, {"y": -1250, "x": 40 * (1 if k % 2 else -1), "duration": 4.8, "ease": "none"}, "") for k in range(len(RISE))],
           *_float_bubbles("ubl", 1.0, 3.2), *_float_bubbles("ubr", 1.6, 3.2),
           *_twinkle(TB(4), 6, 5.4)]
    logo_shot = S(L, (960, 540, 1920), who="", sing=TUNE3, beat="song", tag="INTRO 3: the logo", cam2=(960, 540, 1880),
                  props=[prop("rs", rising, 0, 0), prop("rg", rings, 960, 326), prop("spk", sparkles, 0, 120), *_fw_props(6), prop("logo", logo, 960, 590, .8),
                         prop("pfe", puff, 960, 700, hidden=True), prop("fx", flash, 0, 0)], fx=lfx)
    logo_shot["move"] = {"milo": (2140, 160, .46), **{w: (_POS[L][w][0], 1500, _SC[L][w], _FLIP[L][w]) for w in FRIENDS}}
    # ---------------- 4. THE NAME (the logo is the caption: each word lights up and jumps as Milo says it)
    lit = lambda cue, cls, v, st: [("to", cue, f"#{{p}}logo_w .L{cls}", {**v, "ease": "power2.out", "stagger": {"each": st, "repeat": 1, "yoyo": True}}, f"{cls.upper()} word lights up"),
                                    ("to", cue, f"#{{p}}logo_w .L{cls}h", {"opacity": .8, "duration": v["duration"], "stagger": {"each": st, "repeat": 1, "yoyo": True}}, "")]
    name_fx = [("fromto", 0, "#{p}burst", {"rotation": 22, "svgOrigin": "0 0"}, {"rotation": 30, "duration": 3.0, "ease": "none"}, ""),
               ("fromto", 0, "#{p}logo-dash", {"rotation": 90, "svgOrigin": "0 0"}, {"rotation": 140, "duration": 3.0, "ease": "none"}, ""),
               *_rainbow_fx(0, draw=False), *_rings(0, 3, 3.0),
               *_firework(0, "fw0"), *_firework(.14, "fw1"),
               *lit("w:The", "t", {"scale": 1.4, "transformOrigin": "50% 50%", "duration": .08}, .03),
               *lit("w:Animated", "a", {"y": -32, "duration": .11}, .075),
               *lit("w:Zoo!", "z", {"scale": 1.22, "transformOrigin": "50% 50%", "duration": .15}, .05),
               *[_hop(w, "end", 64) for w in FRIENDS], *[_hop(w, "end+0.45", 44) for w in FRIENDS],
               ("trunk", "end", "tumble", -80, .25), ("arm", "end", "mango", "r", -105), ("arm", "end", "mango", "l", 105),
               ("fromto", "end", "#{p}milo", {"rotation": 0, "svgOrigin": "0 -170"}, {"rotation": 360, "duration": .55, "ease": "power2.out"}, "Milo flips"),
               *_puff_fx("end", "pfb"), *_confetti("end", "cf"),
               *_firework("end", "fw2"), *_firework("end+0.12", "fw3"), *_firework("end+0.3", "fw4"), *_firework("end+0.42", "fw5"),
               ("to", "end+0.3", "#{p}logo_w .La", {"y": -30, "duration": .1, "ease": "power2.out", "stagger": {"each": .045, "repeat": 1, "yoyo": True}}, "the letters do a wave"),
               ("to", "end+0.66", "#{p}logo_w .Lz", {"y": -30, "duration": .1, "ease": "power2.out", "stagger": {"each": .045, "repeat": 1, "yoyo": True}}, ""),
               ("fromto", 0, "#{p}logo-star", {"rotation": 0, "svgOrigin": "0 0"}, {"rotation": 72, "duration": 1.2, "ease": "power2.inOut"}, ""),
               *_float_bubbles("ubl", .2, 2.8), *_float_bubbles("ubr", .5, 2.8),
               *[("fromto", 0, f"#{{p}}rn-r{k}", {"y": 0, "rotation": 0}, {"y": 1500, "rotation": 260 * (1 if k % 2 else -1), "duration": round(2.6 + (k % 5) * .25, 2), "ease": "none"}, "")
                 for k in range(len(RAIN))]]
    name = S(L, (960, 540, 1880), "The Animated Zoo!", tag="INTRO 4: Milo says the name", cam2=(960, 540, 1850),
             props=[prop("rg", rings, 960, 326), *_fw_props(6), prop("logo", logo, 960, 590, .8), prop("pfb", puff, 960, 326, hidden=True)], fx=name_fx)
    name["nocap"] = True      # the logo's own words light up in sync with the voice (toon.captions skips the shot)
    sky["score"] = "score_intro:score"; sky["score_shots"] = 4      # the intro's music: one score on recorded instruments across the four shots
    return [sky, gate, logo_shot, name]
