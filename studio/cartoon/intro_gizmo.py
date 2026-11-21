"""Gizmo Explains main intro (owner, Nov 21 2026 12:01 PM: "create an intro for the gizmo explain as well").

Built like The Animated Zoo's main intro (intro.py): the same four shots every time, about 15 s, one cut per bar line, the tune shots only give
the timing and the music is ONE score on recorded instruments (score_gzintro.py). Its own tune (C | F | G C: G E C E G C | A F C F A C |
B G D G D | C G E C), its own picture, Gizmo's blues (#1d3a8a, #3561d9) with the cyan accent.
  1. THE IDEA (bar 1). Blueprint space: a fine grid, big gears turning slowly, twinkling stars. Gizmo floats up, three question marks pop up
     around him, then his antenna lights up (the bell): the question marks burst into sparkles and light rings run out from the bulb.
  2. THE THINGS HE EXPLAINS (bar 2). Seven things pop up around him, one per half beat, each in a puff: a rocket, a rain cloud, a sprout, a
     magnet, a planet, a gear, a light bulb; they bob to the beat, Gizmo lifts both arms; a ring of light grows out of his bulb and fills the picture.
  3. THE LOGO (bars 3-4). Out of the flash: turning rays, GIZMO drops in letter by letter, EXPLAINS slams in, a cyan line draws on under it,
     confetti (behind everything), Gizmo flies in beside the name and waves, the seven things pop up along the bottom, the letters do a wave.
  4. THE NAME. Gizmo says "Gizmo Explains!" and each word of the logo lights up and jumps as he says it (no caption: the logo is the caption);
     on the last chord everything jumps, his arms go up and his bulb flashes.
STATUS: A PREVIEW until the owner has watched and HEARD it (CLAUDE.md: a new kind of sound is sent to him before it is used in a video). It is
in no episode yet. After his yes it goes, like the Zoo's, right after the hook and as the last four shots of every new long Gizmo cartoon:
    from intro_gizmo import GZ_INTRO_STAGES, gz_intro_shots
    STAGES = {..., **GZ_INTRO_STAGES}          # before Kit(STAGES)
    SHOTS = [<hook shots>, *gz_intro_shots(), <the rest>, *gz_intro_shots()]
Never in a Short, never on The Animated Zoo. Preview alone: `python3 toon.py gzintro`. Change the intro HERE only.
"""
import math
import art
import art_gizmo as G
from kit import S, prop
from intro import _star4, sparkles, puff, rings, confetti, _puff_fx, _twinkle, _confetti, _plus, B, BPM, TB, BAND

INK = G.NAVY; ACC = G.ACC; SUN = "#ffd23f"; LIGHT = "#dffbff"
GX, GY, GS = 960, 820, .70            # Gizmo in the idea space (antenna bulb at 960, 390)
LX, LY, LS = 1630, 800, .52           # Gizmo beside the logo
BULB = (GX, round(GY - 615 * GS))
LOGO = (860, 470)


# ---------------------------------------------------------------- drawings
def gear(r, teeth, fill, op=1.0, stroke=""):
    step = 2 * math.pi / teeth; pts = []
    for k in range(teeth):
        a = k * step
        for rr, da in ((r * .80, 0), (r, step * .14), (r, step * .36), (r * .80, step * .5)):
            pts.append(f"{rr * math.cos(a + da):.1f},{rr * math.sin(a + da):.1f}")
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" opacity="{op}" {stroke}/><circle r="{r * .46:.0f}" fill="{fill}" opacity="{op * .9:.2f}" {stroke}/>'
            f'<circle r="{r * .16:.0f}" fill="{INK}" opacity="{min(1.0, op * 2.2):.2f}"/>')


def bg_idea(p):
    """Blueprint space: Gizmo's blues, a fine grid, three big gears that turn slowly (behind everything)."""
    far = (f'<defs><radialGradient id="{p}_g" cx="50%" cy="46%" r="68%"><stop offset="0" stop-color="#5b8cf5"/><stop offset=".5" stop-color="{G.B2}"/>'
           f'<stop offset="1" stop-color="{G.B1}"/></radialGradient></defs><rect x="-600" y="-900" width="3120" height="2900" fill="url(#{p}_g)"/>'
           + "".join(f'<path d="M{x} -900 V2000" stroke="#fff" stroke-width="3" opacity=".07"/>' for x in range(-600, 2521, 120))
           + "".join(f'<path d="M-600 {y} H2520" stroke="#fff" stroke-width="3" opacity=".07"/>' for y in range(-900, 2001, 120))
           + f'<g transform="translate(130 960)"><g id="{p}_gearA">{gear(300, 14, "#ffffff", .10)}</g></g>'
           + f'<g transform="translate(1800 170)"><g id="{p}_gearB">{gear(230, 12, "#ffffff", .10)}</g></g>'
           + f'<g transform="translate(1560 1010)"><g id="{p}_gearC">{gear(150, 10, ACC, .14)}</g></g>')
    return far, "", ""


def bg_logo(p):
    """The logo card: a blue glow with slow turning rays, a darker floor with circuit lines, the confetti drawn here (behind the logo and Gizmo)."""
    far = (f'<defs><radialGradient id="{p}_g" cx="45%" cy="42%" r="66%"><stop offset="0" stop-color="#78a8ff"/><stop offset=".5" stop-color="{G.B2}"/>'
           f'<stop offset="1" stop-color="{G.B1}"/></radialGradient></defs><rect x="-600" y="-900" width="3120" height="2900" fill="url(#{p}_g)"/>')
    wedges = "".join(f'<path d="M0 0 L{2600 * math.cos(math.radians(a)):.0f} {2600 * math.sin(math.radians(a)):.0f} '
                     f'L{2600 * math.cos(math.radians(a + 9)):.0f} {2600 * math.sin(math.radians(a + 9)):.0f}Z" fill="#ffffff" opacity=".10"/>' for a in range(0, 360, 18))
    far += f'<g transform="translate({LOGO[0]} {LOGO[1]})"><g id="{p}_burst">{wedges}</g></g>'
    near = ('<path d="M-600 880 C200 835 900 860 1400 842 S2200 850 2520 880 L2520 2000 L-600 2000Z" fill="#17307c"/>'
            + "".join(f'<path d="M{x} 1085 V{y} H{x + w}" stroke="{ACC}" stroke-width="6" fill="none" opacity=".35" stroke-linecap="round"/><circle cx="{x + w}" cy="{y}" r="10" fill="{ACC}" opacity=".5"/>'
                      for x, y, w in ((60, 1040, 70), (760, 1048, -60), (1010, 1052, 60), (1840, 1040, -70))))
    near += f'<g id="{p}_cfw" transform="translate({LOGO[0]} 600)" opacity="0">{confetti(p + "_cf")}</g>'
    return far, "", near


art.BG["gz_intro"] = bg_idea; art.PLACE["gz_intro"] = "the idea space (Gizmo's main intro)"
art.BG["gz_logo"] = bg_logo; art.PLACE["gz_logo"] = "the logo (Gizmo's main intro)"
GZ_INTRO_STAGES = {"gz_intro": [("gizmo", "gizmo", GX, GY, GS)], "gz_logo": [("gizmo", "gizmo", LX, LY, LS)]}

_SK = f'stroke="{INK}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"'


def _disc(): return '<circle r="96" fill="#ffffff" opacity=".16"/>'
def rocket(q):
    return (f'<g id="{q}-g">{_disc()}<g transform="rotate(35)"><path d="M-14 62 Q0 108 14 62Z" fill="{SUN}" {_SK}/><path d="M-30 30 L-58 66 L-22 58Z" fill="#ff8a4c" {_SK}/><path d="M30 30 L58 66 L22 58Z" fill="#ff8a4c" {_SK}/>'
            f'<path d="M0 -84 C40 -50 40 20 26 60 L-26 60 C-40 20 -40 -50 0 -84Z" fill="#ffffff" {_SK}/><path d="M0 -84 C20 -66 28 -50 31 -36 L-31 -36 C-28 -50 -20 -66 0 -84Z" fill="#ff5b6e" {_SK}/>'
            f'<circle cx="0" cy="-2" r="17" fill="{ACC}" {_SK}/></g></g>')
def cloud(q):
    return (f'<g id="{q}-g">{_disc()}<path d="M-58 4 a30 30 0 0 1 22 -50 a40 40 0 0 1 74 4 a28 28 0 0 1 18 50 a12 12 0 0 1 -8 4 h-98 a14 14 0 0 1 -8 -8z" fill="#ffffff" {_SK}/>'
            + "".join(f'<path d="M{x} {y} q-13 22 0 30 q13 -8 0 -30z" fill="#7fd0f5" {_SK}/>' for x, y in ((-34, 28), (2, 40), (38, 28))) + '</g>')
def sprout(q):
    return (f'<g id="{q}-g">{_disc()}<path d="M-56 56 Q0 22 56 56 Q0 78 -56 56Z" fill="#8a5a32" {_SK}/><path d="M0 46 V-28" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>'
            f'<path d="M0 46 V-28" stroke="#57c078" stroke-width="9" stroke-linecap="round"/><path d="M0 -24 C-18 -70 -62 -66 -70 -58 C-58 -24 -24 -14 0 -24Z" fill="#57c078" {_SK}/>'
            f'<path d="M0 -24 C18 -70 62 -66 70 -58 C58 -24 24 -14 0 -24Z" fill="#9be08a" {_SK}/></g>')
def magnet(q):
    return (f'<g id="{q}-g">{_disc()}<g transform="rotate(-20)"><path d="M-56 62 V-6 a56 56 0 0 1 112 0 V62 H22 V-6 a22 22 0 0 0 -44 0 V62Z" fill="#ff5b6e" {_SK}/>'
            f'<path d="M-56 62 V34 H-22 V62Z" fill="#e3e9f4" {_SK}/><path d="M22 62 V34 H56 V62Z" fill="#e3e9f4" {_SK}/></g></g>')
def planet(q):
    return (f'<g id="{q}-g">{_disc()}<g transform="rotate(-18)"><path d="M-92 0 a92 24 0 0 1 184 0" stroke="{INK}" stroke-width="20" fill="none"/><path d="M-92 0 a92 24 0 0 1 184 0" stroke="{SUN}" stroke-width="9" fill="none"/>'
            f'<circle r="52" fill="#ff9d4c" {_SK}/><path d="M-44 -18 q44 -22 88 0" stroke="#ffc48a" stroke-width="10" fill="none" stroke-linecap="round"/>'
            f'<path d="M-92 0 a92 24 0 0 0 184 0" stroke="{INK}" stroke-width="20" fill="none"/><path d="M-92 0 a92 24 0 0 0 184 0" stroke="{SUN}" stroke-width="9" fill="none"/></g></g>')
def gearicon(q): return f'<g id="{q}-g">{_disc()}{gear(70, 8, ACC, 1.0, _SK)}</g>'
def bulb(q):
    return (f'<g id="{q}-g">{_disc()}<path d="M0 -76 a50 50 0 0 1 30 90 v16 h-60 v-16 a50 50 0 0 1 30 -90z" fill="{SUN}" {_SK}/><rect x="-26" y="30" width="52" height="34" rx="8" fill="#c9d3e6" {_SK}/>'
            f'<path d="M-12 -4 l12 -22 l12 22" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="-18" cy="-44" r="9" fill="#fff" opacity=".8"/></g>')
ICONS = [rocket, cloud, sprout, magnet, planet, gearicon, bulb]
POS2 = [(300, 800), (330, 470), (590, 230), (960, 150), (1330, 230), (1590, 470), (1620, 800)]      # around Gizmo, clear of the watermark's corner (top left)
POS3 = [(170 + 215 * k, 950) for k in range(7)]                                                      # along the floor of the logo card


def qmark(q):
    t = 'font-family="Baloo" font-weight="800" font-size="170" text-anchor="middle" stroke-linejoin="round" paint-order="stroke"'
    return f'<g id="{q}-g"><text x="0" y="60" {t} fill="{SUN}" stroke="{INK}" stroke-width="22">?</text></g>'
QPOS = [(600, 470), (1320, 440), (690, 250)]


_W = {"G": .68, "I": .31, "Z": .58, "M": .86, "O": .70, "E": .56, "X": .62, "P": .60, "L": .50, "A": .64, "N": .66, "S": .56}
GCOL = [ACC, SUN, "#ff9d4c", "#7cf29a", "#ff8fc0"]
def _word(q, name, text, size, y, cols, ls=.03):
    w = sum(_W[c] for c in text) * size + ls * size * (len(text) - 1); x = -w / 2; out = ""
    t = f'font-family="Baloo" font-weight="800" font-size="{size}" text-anchor="middle" stroke-linejoin="round" paint-order="stroke"'
    for k, c in enumerate(text):
        cx = x + _W[c] * size / 2; x += _W[c] * size + ls * size
        out += (f'<g id="{q}-{name}{k}" class="L{name}"><text x="{cx:.0f}" y="{y + size * .07:.0f}" {t} fill="{INK}" stroke="{INK}" stroke-width="{size * .16:.0f}" opacity=".35">{c}</text>'
                f'<text x="{cx:.0f}" y="{y:.0f}" {t} fill="{cols[k % len(cols)]}" stroke="{INK}" stroke-width="{size * .12:.0f}">{c}</text>'
                f'<text id="{q}-{name}{k}h" class="L{name}h" x="{cx:.0f}" y="{y:.0f}" {t} fill="#ffffff" opacity="0">{c}</text></g>')
    return out, w


LINE_W = 640
def logo(q):
    """GIZMO (five colours) over EXPLAINS (white), a cyan line under it that draws on. Origin: the middle, between the two words."""
    giz, _ = _word(q, "g", "GIZMO", 270, -20, GCOL)
    exp, _ = _word(q, "e", "EXPLAINS", 150, 165, ["#ffffff"])
    shadow = f'<g id="{q}-under" opacity="0"><path d="M{-LINE_W / 2:.0f} 222 H{LINE_W / 2:.0f}" stroke="{INK}" stroke-width="30" stroke-linecap="round" opacity=".35"/></g>'
    line = f'<path id="{q}-line" d="M{-LINE_W / 2:.0f} 214 H{LINE_W / 2:.0f}" stroke="{ACC}" stroke-width="18" stroke-linecap="round" stroke-dasharray="{LINE_W}" stroke-dashoffset="{LINE_W}"/>'
    return f'{shadow}{line}{giz}{exp}'


def flash(q): return f'<rect id="{q}-r" x="-700" y="-700" width="3400" height="2600" fill="{LIGHT}"/>'
def ringwipe(q): return f'<g id="{q}-g"><circle r="100" fill="{LIGHT}"/></g>'


# ---------------------------------------------------------------- the tune: four bars in C, every note a chord tone (CLAUDE.md)
TUNE1 = dict(BAND, chords="C", lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "G5:.5 E5:.5 C5:1 E5:.5 G5:.5 C6:1", "rest": 0}])
TUNE2 = dict(BAND, chords="F", lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "A5:.5 F5:.5 C5:1 F5:.5 A5:.5 C6:1", "rest": 0}])
TUNE3 = dict(BAND, chords="G C", lines=[{"text": "~ ~ ~ ~ ~ ~ ~ ~ ~", "notes": "B5:.5 G5:.5 D5:1 G5:1 D6:1 C6:1 G5:.5 E5:.5 C6:1", "rest": 1}])


# ---------------------------------------------------------------- effects
def _bob(sel, at, amp=26):
    return ("to", at, sel, {"y": f"-={amp}", "duration": .16, "yoyo": True, "repeat": 1, "ease": "power2.out"}, "")


def _glow(at, hold=None):
    k = [{"opacity": 1, "duration": .12}] + [{"opacity": o, "duration": .18} for o in (.55, 1, .55, 1)]
    return ("to", at, "#{p}gizmo-glow", {"keyframes": k}, "the antenna lights up")


def _lit(at=0): return ("fromto", at, "#{p}gizmo-glow", {"opacity": 1}, {"opacity": 1, "duration": .01}, "")


def _arms(at, l, r, hold, what=""):
    kl = [{"rotation": l, "svgOrigin": "-120 120", "duration": .25}, {"rotation": l, "svgOrigin": "-120 120", "duration": hold}, {"rotation": 0, "svgOrigin": "-120 120", "duration": .3}]
    kr = [{"rotation": r, "svgOrigin": "120 120", "duration": .25}, {"rotation": r, "svgOrigin": "120 120", "duration": hold}, {"rotation": 0, "svgOrigin": "120 120", "duration": .3}]
    return [("to", at, "#{p}gizmo-al", {"keyframes": kl}, what), ("to", at, "#{p}gizmo-ar", {"keyframes": kr}, "")]


def _wave(at, n=3):      # a hand raised higher than about -85 degrees disappears behind his head (gc_ep01 stills)
    k = [{"rotation": -70, "svgOrigin": "120 120", "duration": .2}] + [{"rotation": r, "svgOrigin": "120 120", "duration": .16} for _ in range(n) for r in (-50, -84)] + [{"rotation": 0, "svgOrigin": "120 120", "duration": .25}]
    return ("to", at, "#{p}gizmo-ar", {"keyframes": k}, "Gizmo waves")


def _bulb_rings(at, n=3):
    # "to" with keyframes, not "fromto": a fromTo shows its start state from the first frame of the shot, and a small ring sat on the bulb before the idea (stills, Nov 21)
    return [("to", _plus(at, .16 * k), f"#{{p}}rg-r{k}", {"keyframes": [{"scale": .3, "opacity": .9, "transformOrigin": "50% 50%", "duration": .01},
                                                                       {"scale": 3.2, "opacity": 0, "duration": .9, "ease": "power1.out"}]},
             "light rings run out from the bulb" if k == 0 else "") for k in range(n)]


def _gears(a0, a1, d):
    return [("fromto", 0, "#{p}gearA", {"rotation": a0, "svgOrigin": "0 0"}, {"rotation": a1, "duration": d, "ease": "none"}, "the gears turn"),
            ("fromto", 0, "#{p}gearB", {"rotation": -a0 * 1.3, "svgOrigin": "0 0"}, {"rotation": -a1 * 1.3, "duration": d, "ease": "none"}, ""),
            ("fromto", 0, "#{p}gearC", {"rotation": -a0 * 2, "svgOrigin": "0 0"}, {"rotation": -a1 * 2, "duration": d, "ease": "none"}, "")]


def _icon_props(pos, s=1.0): return [prop(f"ic{k}", fn, x, y, s) for k, (fn, (x, y)) in enumerate(zip(ICONS, pos))]


def gz_intro_shots():
    LAND, POP = .18, .12      # a bounce reaches the ground ~0.18 s after it starts, a pop ~0.12 s: every picture hit lands on its note in the score
    # ---------------- 1. THE IDEA
    idea_fx = [*_gears(0, 14, 3.44), *_twinkle(0.05, 10, 2.6),
               ("fromto", .05, "#{p}gizmo_w", {"x": GX, "y": 1560}, {"x": GX, "y": GY, "duration": .95, "ease": "back.out(1.3)"}, "Gizmo floats up"),
               *[f for k in range(3) for f in (("fromto", round(TB(1 + .5 * k) - POP, 3), f"#{{p}}q{k}-g", {"scale": 0, "rotation": -30, "transformOrigin": "50% 50%"},
                                                {"scale": 1, "rotation": (10, -12, 8)[k], "duration": .3, "ease": "back.out(2.4)"}, "a question mark pops up"),
                                               ("to", round(TB(3) - .02, 3), f"#{{p}}q{k}-g", {"scale": 1.7, "opacity": 0, "duration": .3, "ease": "power2.out"}, ""))],
               _glow(TB(3)), *_arms(TB(3), 0, -82, 1.0, "Gizmo has an idea"), *_bulb_rings(TB(3)), *_puff_fx(TB(3), "pfb")]
    idea = S("gz_intro", (960, 560, 1300), who="", sing=TUNE1, beat="song", tag="INTRO 1: the idea", trans="iris", cam2=(960, 540, 1800),
             props=[prop("spk", sparkles, 0, 330), prop("rg", rings, *BULB), *[prop(f"q{k}", qmark, x, y) for k, (x, y) in enumerate(QPOS)], prop("pfb", puff, BULB[0], BULB[1], hidden=True)],
             fx=idea_fx)
    idea["move"] = {"gizmo": (GX, 1560, GS)}      # Gizmo starts under the picture
    # ---------------- 2. THE THINGS HE EXPLAINS
    th_fx = [*_gears(14, 27, 3.13), _lit(), *_twinkle(0.05, 10, 2.6)]
    for k in range(7):
        th_fx += [("fromto", round(TB(k * .5) - POP, 3), f"#{{p}}ic{k}-g", {"scale": 0, "rotation": -40, "transformOrigin": "50% 50%"}, {"scale": 1, "rotation": 0, "duration": .32, "ease": "back.out(2.2)"},
                   "a thing he explains pops up" if k == 0 else ""), *_puff_fx(TB(k * .5), f"pf{k}")]
        th_fx += [_bob(f"#{{p}}ic{k}-g", TB(b)) for b in (k * .5 + 1, k * .5 + 2) if b <= 3]
    th_fx += [_bob(f"#{{p}}ic{k}-g", TB(3.5), 40) for k in range(7)]
    th_fx += [*_arms(TB(2.5), 80, -80, .9, "Gizmo lifts both arms"), *_bulb_rings(TB(3.5), 2),
              ("fromto", TB(4), "#{p}sw_w", {"opacity": 0}, {"opacity": 1, "duration": .01}, ""),
              ("fromto", TB(4), "#{p}sw-g", {"scale": 0, "transformOrigin": "50% 50%"}, {"scale": 34, "duration": .31, "ease": "power2.in"}, "a ring of light grows out of his bulb and fills the picture")]
    things = S("gz_intro", (960, 540, 1920), who="", sing=TUNE2, beat="song", tag="INTRO 2: the things he explains", cam2=(960, 540, 1840),
               props=[prop("spk", sparkles, 0, 330), prop("rg", rings, *BULB), *_icon_props(POS2),
                      *[prop(f"pf{k}", puff, x, y, hidden=True) for k, (x, y) in enumerate(POS2)], prop("sw", ringwipe, *BULB, hidden=True)],
               fx=th_fx)
    # ---------------- 3. THE LOGO
    L = "gz_logo"; Z = TB(3)                 # EXPLAINS lands on the brass + piano + cymbal; the bell, the line and the confetti half a beat later
    lfx = [("fromto", 0, "#{p}fx-r", {"opacity": 1}, {"opacity": 0, "duration": TB(0), "ease": "power2.in"}, "out of the flash"),
           ("fromto", 0, "#{p}burst", {"rotation": 0, "svgOrigin": "0 0"}, {"rotation": 22, "duration": 5.6, "ease": "none"}, "the rays turn"),
           *[("fromto", round(TB(.5 + .5 * k) - LAND, 3), f"#{{p}}logo-g{k}", {"y": -760, "rotation": -18 + 9 * k, "opacity": 0, "transformOrigin": "50% 100%"},
              {"y": 0, "rotation": 0, "opacity": 1, "duration": .5, "ease": "bounce.out"}, "a letter drops in") for k in range(5)],
           *[("fromto", round(TB(.5 + .5 * k), 3), f"#{{p}}logo-g{k}", {"scaleX": 1.2, "scaleY": .76}, {"scaleX": 1, "scaleY": 1, "duration": .32, "ease": "back.out(3)"}, "") for k in range(5)],
           *[("fromto", round(Z - .3 + .012 * k, 3), f"#{{p}}logo-e{k}", {"scale": 2.6, "opacity": 0, "transformOrigin": "50% 50%"}, {"scale": 1, "opacity": 1, "duration": .3, "ease": "power3.in"},
              "EXPLAINS slams in" if k == 0 else "") for k in range(8)],
           *[("fromto", round(Z + .012 * k, 3), f"#{{p}}logo-e{k}", {"scaleX": 1.16, "scaleY": .8}, {"scaleX": 1, "scaleY": 1, "duration": .35, "ease": "elastic.out(1, .4)"}, "") for k in range(8)],
           ("to", TB(3.5), "#{p}logo-under", {"opacity": 1, "duration": .05}, ""),
           ("to", TB(3.5), "#{p}logo-line", {"strokeDashoffset": 0, "duration": .45, "ease": "power2.out"}, "the line draws on"),
           *_puff_fx(TB(3.5), "pfe"), *_confetti(TB(3.5), "cf"),
           ("fromto", TB(4), "#{p}gizmo_w", {"x": 2250, "y": 520}, {"x": LX, "y": LY, "duration": round(TB(5.6) - TB(4), 3), "ease": "power2.out"}, "Gizmo flies in beside the name"),
           _glow(TB(5.6)), _wave(TB(5.8), 2),
           *[("fromto", round(TB(4.5 + .5 * k) - POP, 3), f"#{{p}}ic{k}-g", {"scale": 0, "rotation": -40, "transformOrigin": "50% 50%"}, {"scale": 1, "rotation": 0, "duration": .32, "ease": "back.out(2.2)"},
              "the things pop up along the floor" if k == 0 else "") for k in range(7)],
           *[_bob(f"#{{p}}ic{k}-g", TB(b)) for k in range(7) for b in (5.5 + .5 * k,) if b <= 7.5],
           *[("fromto", round(TB(4.5) + .06 * k, 3), f"#{{p}}logo-g{k}h", {"opacity": 0}, {"opacity": .85, "duration": .12, "yoyo": True, "repeat": 1}, "a shine runs along the letters" if k == 0 else "") for k in range(5)],
           *[("fromto", round(TB(4.5) + .3 + .06 * k, 3), f"#{{p}}logo-e{k}h", {"opacity": 0}, {"opacity": .85, "duration": .12, "yoyo": True, "repeat": 1}, "") for k in range(8)],
           ("to", TB(7), "#{p}logo_w .Lg", {"y": -30, "duration": .1, "ease": "power2.out", "stagger": {"each": .05, "repeat": 1, "yoyo": True}}, "the letters do a wave"),
           ("to", round(TB(7) + .3, 3), "#{p}logo_w .Le", {"y": -24, "duration": .1, "ease": "power2.out", "stagger": {"each": .04, "repeat": 1, "yoyo": True}}, ""),
           *_twinkle(TB(4), 6, 5.4)]
    logo_shot = S(L, (960, 540, 1920), who="", sing=TUNE3, beat="song", tag="INTRO 3: the logo", cam2=(960, 540, 1880),
                  props=[prop("spk", sparkles, 0, 300), prop("logo", logo, *LOGO), *_icon_props(POS3, .86), prop("pfe", puff, LOGO[0], LOGO[1] + 170, hidden=True), prop("fx", flash, 0, 0)], fx=lfx)
    logo_shot["move"] = {"gizmo": (2250, 520, LS)}      # Gizmo starts outside the picture, on the right
    # ---------------- 4. THE NAME (the logo is the caption: each word lights up and jumps as Gizmo says it)
    lit = lambda cue, cls, v, st, what: [("to", cue, f"#{{p}}logo_w .L{cls}", {**v, "ease": "power2.out", "stagger": {"each": st, "repeat": 1, "yoyo": True}}, what),
                                         ("to", cue, f"#{{p}}logo_w .L{cls}h", {"opacity": .8, "duration": v["duration"], "stagger": {"each": st, "repeat": 1, "yoyo": True}}, "")]
    name_fx = [("fromto", 0, "#{p}burst", {"rotation": 22, "svgOrigin": "0 0"}, {"rotation": 30, "duration": 3.0, "ease": "none"}, ""),
               ("fromto", 0, "#{p}logo-under", {"opacity": 1}, {"opacity": 1, "duration": .01}, ""),
               ("fromto", 0, "#{p}logo-line", {"strokeDashoffset": 0}, {"strokeDashoffset": 0, "duration": .01}, ""), _lit(),
               *lit("w:Gizmo", "g", {"y": -34, "duration": .11}, .07, "GIZMO lights up"),
               *lit("w:Explains!", "e", {"scale": 1.2, "transformOrigin": "50% 50%", "duration": .1}, .045, "EXPLAINS lights up"),
               *[_bob(f"#{{p}}ic{k}-g", "end", 44) for k in range(7)], *[_bob(f"#{{p}}ic{k}-g", "end+0.45", 30) for k in range(7)],
               *_arms("end", 80, -80, .7, "Gizmo lifts both arms"), _glow("end"),
               *_puff_fx("end", "pfb"), *_confetti("end", "cf"),
               ("to", "end+0.3", "#{p}logo_w .Lg", {"y": -30, "duration": .1, "ease": "power2.out", "stagger": {"each": .05, "repeat": 1, "yoyo": True}}, "the letters do a wave"),
               ("to", "end+0.6", "#{p}logo_w .Le", {"y": -24, "duration": .1, "ease": "power2.out", "stagger": {"each": .04, "repeat": 1, "yoyo": True}}, ""),
               *_twinkle(0.05, 6, 2.8)]
    # pause=1.0: the finish (the jump, the bulb, the last chord) plays out before the episode's next shot
    name = S(L, (960, 540, 1880), "Gizmo Explains!", who="gizmo", tag="INTRO 4: Gizmo says the name", cam2=(960, 540, 1850), pause=1.0,
             props=[prop("spk", sparkles, 0, 300), prop("logo", logo, *LOGO), *_icon_props(POS3, .86), prop("pfb", puff, LX, round(LY - 615 * LS), hidden=True)], fx=name_fx)
    name["nocap"] = True      # the logo's own words light up in sync with the voice
    idea["score"] = "score_gzintro:score"; idea["score_shots"] = 4      # the intro's music: one score on recorded instruments across the four shots
    return [idea, things, logo_shot, name]
