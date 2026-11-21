"""Art for zc_ep12 "Whose Ears Are These? Guess With Milo" (Nov 21 2026): a rhino and a fennec fox (new rigs, registered here the way
art_zc_ep11.py registers its giraffe and zebra), the clue props the animals hide behind so only their ears show (tall grass, a sand dune,
a snow bank), sound rings, heat waves, a fennec fox face (front view) for the fact boards, a cut through the sand with food hiding under it,
the two ears side by side (big fox ear lets heat out, small round polar bear ear keeps it in), forward / back arrows.
The polar bear is the existing Poppy rig ("bear", art2.py). Same hand as art.py / art2.py: flat fills, one warm dark outline round every
moving part. Nothing here changes an existing character, prop or place."""
import art, art2, kit
from art import eye, INK

RHI = {"fill": "#a7a3a0", "shade": "#8d8986", "light": "#c9c6c3", "line": "#4a4542", "far": "#959290", "horn": "#d9cdb8", "ear": "#f2b8c2", "nail": "#e8e2d8"}
FOX = {"fill": "#f2cb8c", "shade": "#ddb070", "light": "#fff3dc", "line": "#7a4a1e", "far": "#e2b878", "ear": "#f6bcc6", "tip": "#5a3418", "fur": "#fffaf0"}


def _ol(shapes, ln, w=9): return f'<g fill="{ln}" stroke="{ln}" stroke-width="{w * 2}" stroke-linejoin="round" stroke-linecap="round">{shapes}</g>'


# ================================================================== rhino
RHI_EAR = "M-30 0 C-46 -68 -27 -130 0 -140 C27 -130 46 -68 30 0Z"          # one ear, base at 0 0, pointing up


def _rhi_ear(pid, name, x, y, c, far=False, rot=-8):
    col = c["far"] if far else c["fill"]
    return (f'<g id="{pid}-{name}"><g transform="translate({x} {y}) rotate({rot})">{_ol(f"<path d=\"{RHI_EAR}\"/>", c["line"], 8)}<path d="{RHI_EAR}" fill="{col}"/>'
            f'<path d="M-15 -10 C-24 -60 -14 -105 0 -113 C14 -105 24 -60 15 -10Z" fill="{c["ear"]}"/>'
            f'<path d="M-8 -136 l-8 -16 M2 -140 l2 -18 M12 -134 l10 -14" stroke="{c["line"]}" stroke-width="6" stroke-linecap="round"/></g></g>')


def rhino(pid, c=RHI):
    """A rhino, side view facing right, feet at y = 0 (about 560 tall). Parts: -neck (head: nods, looks), -ear (near ear) and -ear2 (far ear):
    each turns on its own round its base (SDZWA: "Their ears can move independently of each other"), -jaw, -eye, -brow, -smile / -frown, -tail,
    -fl -bl -fl2 -bl2 (legs). Ear bases: near 262 -436, far 214 -446 (the rig's "ear" / "ear2")."""
    ln = c["line"]

    def leg(x, far, name):
        col = c["far"] if far else c["fill"]
        sh = f'<rect x="{x - 48}" y="-240" width="96" height="240" rx="34"/>'
        nails = "" if far else "".join(f'<path d="M{x - 30 + k * 24} -2 q10 -20 20 0Z" fill="{c["nail"]}"/>' for k in range(3))
        return f'<g id="{pid}-{name}">{_ol(sh, ln)}<rect x="{x - 48}" y="-240" width="96" height="240" rx="34" fill="{col}"/>{nails}</g>'
    far_legs = leg(-196, True, "bl2") + leg(96, True, "fl2"); near_legs = leg(-140, False, "bl") + leg(150, False, "fl")
    body_sh = '<ellipse cx="-20" cy="-300" rx="270" ry="160"/>'
    body = _ol(body_sh, ln) + f'<ellipse cx="-20" cy="-300" rx="270" ry="160" fill="{c["fill"]}"/>'
    shade = (f'<path d="M-288 -260 A270 160 0 0 0 246 -260 A330 220 0 0 1 -288 -260Z" fill="{c["shade"]}" opacity=".6"/>'
             f'<ellipse cx="-100" cy="-410" rx="120" ry="30" fill="{c["light"]}" opacity=".5"/>'
             f'<path d="M-150 -420 q20 60 0 120 M40 -440 q16 60 0 130" stroke="{c["shade"]}" stroke-width="8" fill="none" stroke-linecap="round" opacity=".7"/>')
    tail = (f'<g id="{pid}-tail"><path d="M-286 -340 q-30 50 -20 120" stroke="{ln}" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<path d="M-286 -340 q-30 50 -20 120" stroke="{c["fill"]}" stroke-width="10" fill="none" stroke-linecap="round"/>'
            f'<path d="M-306 -226 l-10 30 M-304 -224 l2 32 M-300 -226 l12 28" stroke="{ln}" stroke-width="7" stroke-linecap="round"/></g>')
    head_d = "M170 -430 C250 -470 350 -400 430 -300 C470 -250 470 -190 420 -178 C340 -166 250 -196 180 -250 C150 -300 140 -390 170 -430Z"
    horn1 = "M396 -282 C404 -340 418 -400 440 -440 C452 -390 458 -330 460 -272Z"
    horn2 = "M334 -352 C340 -380 350 -404 362 -416 C370 -392 374 -366 376 -340Z"
    neck = (f'<g id="{pid}-neck">' + _rhi_ear(pid, "ear2", 214, -446, c, True, -14)
            + _ol(f'<path d="{head_d}"/><path d="{horn1}"/><path d="{horn2}"/>', ln)
            + f'<path d="{head_d}" fill="{c["fill"]}"/><path d="M200 -260 C260 -210 340 -186 420 -180 C440 -186 452 -198 456 -214 C380 -200 280 -220 200 -260Z" fill="{c["shade"]}" opacity=".6"/>'
            f'<path d="{horn1}" fill="{c["horn"]}"/><path d="{horn2}" fill="{c["horn"]}"/><path d="M412 -300 q10 -50 26 -110" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".6"/>'
            f'<g id="{pid}-jaw" opacity="0"><path d="M372 -192 q30 22 60 4 q-4 30 -30 32 q-24 0 -30 -36Z" fill="#c9667d" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
            + art2._mouth(pid, 400, -196, 50, ln, 6)
            + f'<ellipse cx="446" cy="-232" rx="9" ry="6" fill="{ln}" transform="rotate(30 446 -232)"/>'
            + eye(f"{pid}-eye", 316, -330, 24, lashes=1, lid=c["fill"]) + art2._brow(pid, 316, -366, 40, ln, 7)
            + f'<ellipse cx="346" cy="-282" rx="16" ry="9" fill="#ff8fb1" opacity=".55"/>'
            + _rhi_ear(pid, "ear", 262, -436, c, False, 6) + '</g>')
    sh = '<ellipse cx="0" cy="4" rx="290" ry="20" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-all">{tail}<g>{far_legs}</g>{body}{shade}{near_legs}{neck}</g></g>'


# ================================================================== fennec fox
FOX_EAR = "M-46 0 C-60 -70 -40 -150 -4 -190 C28 -150 46 -70 38 0Z"       # one tall ear, base at 0 0, pointing up


def _fox_ear(pid, name, x, y, c, far=False, rot=-10):
    col = c["far"] if far else c["fill"]
    return (f'<g id="{pid}-{name}"><g transform="translate({x} {y}) rotate({rot})">{_ol(f"<path d=\"{FOX_EAR}\"/>", c["line"], 8)}<path d="{FOX_EAR}" fill="{col}"/>'
            f'<path d="M-28 -10 C-38 -66 -24 -126 -4 -160 C16 -126 28 -66 22 -10Z" fill="{c["ear"]}"/>'
            f'<path d="M-18 -30 q6 -26 4 -52 M10 -30 q-2 -26 -6 -60 M-4 -24 q2 -34 0 -70" stroke="{c["fur"]}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".9"/></g></g>')


def fennec(pid, c=FOX):
    """A fennec fox, side view facing right, feet at y = 0 (about 470 tall with its ears). Huge ears (SDZWA: "Fennec foxes' ears can be half as long
    as their body"): -ear (near) and -ear2 (far) turn on their own round their bases (near 150 -244, far 196 -250). Parts: -neck (head), -jaw, -eye,
    -brow, -smile / -frown, -tail, -fl -bl -fl2 -bl2. Furry feet (SDZWA: "fur on their feet")."""
    ln = c["line"]

    def leg(x, far, name):
        col = c["far"] if far else c["fill"]
        sh = f'<rect x="{x - 15}" y="-120" width="30" height="118" rx="13"/><ellipse cx="{x + 6}" cy="-6" rx="24" ry="12"/>'
        return (f'<g id="{pid}-{name}">{_ol(sh, ln, 6)}<rect x="{x - 15}" y="-120" width="30" height="118" rx="13" fill="{col}"/>'
                f'<ellipse cx="{x + 6}" cy="-6" rx="24" ry="12" fill="{c["fur"] if not far else c["far"]}"/></g>')
    far_legs = leg(-100, True, "bl2") + leg(60, True, "fl2"); near_legs = leg(-74, False, "bl") + leg(86, False, "fl")
    body_sh = '<ellipse cx="-10" cy="-150" rx="120" ry="64"/>'
    body = _ol(body_sh, ln, 8) + f'<ellipse cx="-10" cy="-150" rx="120" ry="64" fill="{c["fill"]}"/><path d="M-120 -120 C-60 -90 40 -88 110 -116 C60 -96 -60 -96 -120 -120Z" fill="{c["light"]}"/>'
    tail_d = "M-116 -168 C-200 -200 -270 -170 -284 -110 C-292 -70 -262 -54 -240 -70 C-226 -116 -190 -140 -116 -128Z"
    tail = (f'<g id="{pid}-tail">{_ol(f"<path d=\"{tail_d}\"/>", ln, 7)}<path d="{tail_d}" fill="{c["fill"]}"/>'
            f'<path d="M-282 -100 C-292 -66 -264 -50 -242 -66 C-252 -82 -262 -96 -282 -100Z" fill="{c["tip"]}"/></g>')
    head_sh = ('<circle cx="160" cy="-214" r="62"/><path d="M190 -244 C240 -230 270 -206 276 -190 C270 -176 236 -170 196 -176Z"/>'
               '<path d="M110 -190 C100 -170 120 -150 150 -156Z"/>')
    neck = (f'<g id="{pid}-neck">' + _fox_ear(pid, "ear2", 176, -262, c, True, 18) + _fox_ear(pid, "ear", 128, -256, c, False, -20)
            + _ol(head_sh, ln, 8) + f'<circle cx="160" cy="-214" r="62" fill="{c["fill"]}"/>'
            f'<path d="M190 -244 C240 -230 270 -206 276 -190 C270 -176 236 -170 196 -176Z" fill="{c["fill"]}"/>'
            f'<path d="M150 -180 C190 -168 236 -168 272 -184 C262 -168 220 -162 186 -164 C166 -166 154 -172 150 -180Z" fill="{c["fur"]}"/>'
            f'<path d="M110 -190 C100 -170 120 -150 150 -156Z" fill="{c["fur"]}"/>'
            f'<ellipse cx="274" cy="-196" rx="12" ry="9" fill="{c["tip"]}"/>'
            f'<g id="{pid}-jaw" opacity="0"><path d="M224 -174 q20 14 40 2 q-4 20 -20 20 q-16 0 -20 -22Z" fill="#c9667d" stroke="{ln}" stroke-width="5" stroke-linejoin="round"/></g>'
            + art2._mouth(pid, 240, -176, 34, ln, 5) + eye(f"{pid}-eye", 190, -224, 20, lashes=1, lid=c["fill"]) + art2._brow(pid, 190, -254, 32, ln, 6)
            + f'<ellipse cx="206" cy="-196" rx="11" ry="7" fill="#ff8fb1" opacity=".6"/>'
            + '</g>')
    sh = '<ellipse cx="0" cy="4" rx="170" ry="14" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-all">{tail}<g>{far_legs}</g>{body}{near_legs}{neck}</g></g>'


art2.RIGS["rhino"] = dict(build=lambda p: rhino(p), neck="180 -380", tail="-286 -340", ear="262 -436",
                          legs={"fl": 150, "bl": -140, "fl2": 96, "bl2": -196}, hip=-240, jaw=("y", 10), eyes=["eye"], brows=["brow"])
art2.RIGS["fennec"] = dict(build=lambda p: fennec(p), neck="120 -190", tail="-140 -150", ear="128 -256",
                           legs={"fl": 86, "bl": -74, "fl2": 60, "bl2": -100}, hip=-120, jaw=("y", 6), eyes=["eye"], brows=["brow"])
kit.PT["rhino"] = {"head": (330, -320), "eye": (316, -330), "ears": (240, -520), "body": (-20, -300), "top": (250, -560), "horn": (430, -400), "tail": (-300, -280),
                   "legs": (0, -120), "feet": (0, 0), "all": (80, -290)}
kit.BOX["rhino"] = (-330, 480, -600)
kit.PT["fennec"] = {"head": (180, -214), "eye": (190, -224), "ears": (170, -380), "body": (-14, -150), "top": (170, -470), "tail": (-240, -100),
                    "legs": (0, -60), "feet": (0, 0), "all": (0, -220)}
kit.BOX["fennec"] = (-310, 290, -480)
kit.PT.setdefault("bear", {"head": (240, -300), "eye": (246, -330), "body": (-10, -212), "top": (214, -440), "paw": (140, -20), "feet": (0, 0), "all": (60, -230)})
kit.PT["bear"] = dict(kit.PT["bear"], ears=(200, -400), tail=(-214, -250))
kit.BOX.setdefault("bear", (-260, 380, -450))


# ================================================================== the hiding places (props are drawn IN FRONT of actors)
def grass_tall(pid, w=900, h=330, seed=1):
    """A thick band of tall savanna grass, base at y = 0, w wide: solid up to about 0.8 h, blade tips to 0.9 h. An animal behind it shows only
    what pokes out above."""
    import random
    r = random.Random(seed); blades = []
    for k in range(int(w / 22)):
        x = -w / 2 + k * 22 + r.uniform(-6, 6); hh = h * r.uniform(.8, .9); bend = r.uniform(-30, 30); col = r.choice(("#c9a84a", "#d8b85a", "#b8973c", "#e2c46a"))
        blades.append(f'<path d="M{x - 14:.0f} 0 Q{x + bend * .3:.0f} {-hh * .5:.0f} {x + bend:.0f} {-hh:.0f} Q{x + bend * .3 + 8:.0f} {-hh * .5:.0f} {x + 16:.0f} 0Z" fill="{col}"/>')
    wav = " ".join(f"Q{-w / 2 + (k + .5) * w / 8:.0f} {-h * .86:.0f} {-w / 2 + (k + 1) * w / 8:.0f} {-h * .8:.0f}" for k in range(8))
    base = f'<path d="M{-w / 2 - 10} 120 L{-w / 2 - 10} {-h * .78:.0f} Q{-w / 2} {-h * .82:.0f} {-w / 2} {-h * .8:.0f} {wav} L{w / 2 + 10} 120Z" fill="#c9a447"/>'
    return f'<g id="{pid}">{base}{"".join(blades)}</g>'


def dune_mound(pid, w=1000, h=300):
    """A round sand dune, base at y = 0: the fox behind it shows only its ears."""
    return (f'<g id="{pid}"><path d="M{-w / 2} 60 C{-w * .3:.0f} {-h:.0f} {w * .3:.0f} {-h:.0f} {w / 2} 60Z" fill="#f0c878"/><path d="M{-w / 2 + 6} 50 C{-w * .3:.0f} {-h:.0f} {w * .3:.0f} {-h:.0f} {w / 2 - 6} 50" fill="none" stroke="#d9a854" stroke-width="10"/>'
            f'<path d="M{-w * .3:.0f} {-h * .45:.0f} C{-w * .1:.0f} {-h * .7:.0f} {w * .15:.0f} {-h * .72:.0f} {w * .3:.0f} {-h * .5:.0f}" stroke="#fbe3a8" stroke-width="16" fill="none" stroke-linecap="round" opacity=".8"/>'
            '</g>')


def snow_bank(pid, w=900, h=280):
    """A soft snow bank, base at y = 0: the polar bear behind it shows only its small round ears."""
    return (f'<g id="{pid}"><path d="M{-w / 2} 60 C{-w * .4:.0f} {-h:.0f} {-w * .05:.0f} {-h * 1.05:.0f} {w * .1:.0f} {-h * .8:.0f} C{w * .3:.0f} {-h * 1.1:.0f} {w * .45:.0f} {-h * .6:.0f} {w / 2} 60Z" '
            f'fill="#ffffff" stroke="#b9d3ea" stroke-width="10"/><path d="M{-w * .3:.0f} {-h * .5:.0f} q{w * .12:.0f} -{h * .2:.0f} {w * .25:.0f} -{h * .05:.0f}" stroke="#dbeaf7" stroke-width="18" fill="none" stroke-linecap="round"/>'
            '</g>')


# ================================================================== little signs and effects
def sound_rings(pid, col="#3aa0ff", flip=False):
    """Three sound rings (a sound coming in), parts -a0 -a1 -a2 (small to big), drawn to the right of 0 0; flip=True: to the left."""
    k = -1 if flip else 1
    return (f'<g id="{pid}">' + "".join(f'<g id="{pid}-a{i}"><path d="M{k * (40 + i * 46)} {-(36 + i * 34)} Q{k * (70 + i * 60)} 0 {k * (40 + i * 46)} {36 + i * 34}" stroke="{INK}" stroke-width="{24}" fill="none" stroke-linecap="round"/>'
                                     f'<path d="M{k * (40 + i * 46)} {-(36 + i * 34)} Q{k * (70 + i * 60)} 0 {k * (40 + i * 46)} {36 + i * 34}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round"/></g>' for i in range(3)) + '</g>')


def heat_waves(pid, col="#ff7a3a"):
    """Three wavy lines rising from 0 0 (heat going out), parts -h0 -h1 -h2."""
    return (f'<g id="{pid}">' + "".join(f'<g id="{pid}-h{i}"><path d="M{(i - 1) * 50} 0 q-20 -30 0 -60 q20 -30 0 -60 q-20 -30 0 -60" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round"/>'
                                     f'<path d="M{(i - 1) * 50} 0 q-20 -30 0 -60 q20 -30 0 -60 q-20 -30 0 -60" stroke="{col}" stroke-width="11" fill="none" stroke-linecap="round"/></g>' for i in range(3)) + '</g>')


def warm_glow(pid):
    """A warm cosy glow (warmth staying in): a soft orange disc with a small heart."""
    return (f'<g id="{pid}"><circle r="120" fill="#ffb347" opacity=".35"/><circle r="80" fill="#ffb347" opacity=".45"/>'
            f'<path d="M0 30 C-60 -14 -42 -66 0 -36 C42 -66 60 -14 0 30Z" fill="#ff6f91" stroke="#b8324f" stroke-width="7" stroke-linejoin="round"/></g>')


def turn_arrow(pid, col="#ff5a5f", back=False):
    """A curved arrow: forward (to the right) or back (to the left)."""
    t = ' transform="scale(-1 1)"' if back else ""
    return (f'<g id="{pid}"><g{t}><path d="M-70 20 Q0 -60 70 0" stroke="{INK}" stroke-width="26" fill="none" stroke-linecap="round"/>'
            f'<path d="M-70 20 Q0 -60 70 0" stroke="{col}" stroke-width="14" fill="none" stroke-linecap="round"/>'
            f'<path d="M50 -34 L96 8 L40 26Z" fill="{col}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/></g></g>')


# ================================================================== fact boards
def fox_face(pid, c=FOX):
    """A fennec fox's face, front view, about 760 tall with the ears, centred on its nose line. Parts: -eL, -eR (the ears, turn round their bases)."""
    ln = c["line"]
    def ear(name, x, rot):
        return (f'<g id="{pid}-{name}"><g transform="translate({x} -120) rotate({rot}) scale(1.9)">{_ol(f"<path d=\"{FOX_EAR}\"/>", ln, 5)}<path d="{FOX_EAR}" fill="{c["fill"]}"/>'
                f'<path d="M-20 -10 C-32 -76 -24 -150 -6 -190 C12 -150 22 -76 16 -10Z" fill="{c["ear"]}"/>'
                f'<path d="M-16 -30 q6 -30 4 -60 M8 -30 q-2 -30 -6 -70" stroke="{c["fur"]}" stroke-width="4" fill="none" stroke-linecap="round"/></g></g>')
    face = ('<ellipse cx="0" cy="0" rx="170" ry="150"/>')
    return (f'<g id="{pid}">' + ear("eL", -110, -24) + ear("eR", 110, 24) + _ol(face, ln, 9)
            + f'<ellipse cx="0" cy="0" rx="170" ry="150" fill="{c["fill"]}"/>'
            f'<path d="M-150 40 C-90 150 90 150 150 40 C90 90 -90 90 -150 40Z" fill="{c["fur"]}"/>'
            f'<ellipse cx="0" cy="40" rx="70" ry="56" fill="{c["fur"]}"/><ellipse cx="0" cy="22" rx="26" ry="18" fill="{c["tip"]}"/>'
            f'<path d="M0 40 v22 M-22 70 q22 18 44 0" stroke="{ln}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            + eye(f"{pid}-eyeL", -70, -36, 30, lashes=1, lid=c["fill"]) + eye(f"{pid}-eyeR", 70, -36, 30, lashes=1, lid=c["fill"])
            + '<ellipse cx="-104" cy="20" rx="20" ry="11" fill="#ff8fb1" opacity=".6"/><ellipse cx="104" cy="20" rx="20" ry="11" fill="#ff8fb1" opacity=".6"/></g>')


def beetle(pid):
    """A small round beetle (a fennec's food: SDZWA "They enjoy insects ...")."""
    return (f'<g id="{pid}"><path d="M-30 10 l-24 16 M-10 16 l-10 26 M10 16 l10 26 M30 10 l24 16" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
            f'<ellipse cx="0" cy="0" rx="44" ry="30" fill="#3f7a4a" stroke="{INK}" stroke-width="8"/><path d="M0 -30 v60" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="46" cy="-4" r="16" fill="#2f5a36" stroke="{INK}" stroke-width="7"/><circle cx="50" cy="-8" r="4" fill="#fff"/></g>')


def sand_cut(pid):
    """A cut through the sand (about 1300 x 640, top edge at y = -200): the desert floor on top, under it a little burrow with a beetle (parts -bug,
    -rings: sound rings rising from the beetle to the surface)."""
    return (f'<g id="{pid}"><rect x="-650" y="-200" width="1300" height="640" rx="40" fill="#e9b96a" stroke="{INK}" stroke-width="10"/>'
            f'<path d="M-640 -40 C-300 -10 300 -60 640 -20 L640 120 C300 90 -300 140 -640 110Z" fill="#dda552" opacity=".7"/>'
            f'<path d="M-640 260 C-300 230 300 290 640 250 L640 400 C300 380 -300 420 -640 400Z" fill="#cf9440" opacity=".7"/>'
            f'<path d="M-640 -200 L640 -200" stroke="#fbe3a8" stroke-width="18"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="#c8893a" opacity=".6"/>' for x, y, rr in ((-500, 60, 10), (-380, 320, 8), (420, 40, 12), (520, 300, 9), (-200, 380, 7), (300, 360, 8)))
            + f'<ellipse cx="80" cy="230" rx="170" ry="92" fill="#8a5a2c" stroke="{INK}" stroke-width="8"/>'
            f'<g transform="translate(80 250)">{beetle(pid + "-bug")}</g>'
            f'<g id="{pid}-rings" transform="translate(80 110) rotate(-90)">{sound_rings(pid + "-r", "#ffffff")}</g></g>')


def ear_pair(pid):
    """The two ears side by side on a board (about 1200 wide): left the fennec's big ear with heat waves going out, right the polar bear's small round
    ear with a warm glow staying in. Parts: -fox, -bear, -heat, -glow."""
    fc, bc = FOX, art2.BEAR
    fox_ear = (f'<g id="{pid}-fox" transform="translate(-300 200)"><g transform="scale(2.3)">{_ol(f"<path d=\"{FOX_EAR}\"/>", fc["line"], 4)}<path d="{FOX_EAR}" fill="{fc["fill"]}"/>'
               f'<path d="M-20 -10 C-32 -76 -24 -150 -6 -190 C12 -150 22 -76 16 -10Z" fill="{fc["ear"]}"/></g></g>')
    bear_ear = (f'<g id="{pid}-bear" transform="translate(330 120)"><circle r="96" fill="{bc["fill"]}" stroke="{bc["line"]}" stroke-width="12"/><circle r="52" fill="#f6c9d3"/></g>')
    return (f'<g id="{pid}">{fox_ear}<g id="{pid}-heat" transform="translate(-290 -240)">{heat_waves(pid + "-hw")}</g>'
            f'<g id="{pid}-glow" transform="translate(330 120)"><circle r="190" fill="#ffb347" opacity=".3"/><circle r="140" fill="#ffb347" opacity=".35"/></g>{bear_ear}</g>')
