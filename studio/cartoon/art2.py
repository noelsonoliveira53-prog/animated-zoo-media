"""The cast beyond Milo and the camels, and the places of the story world. Same hand as art.py:
flat fills, one warm dark outline round every moving part, a soft highlight, a shade crescent, big brown eyes, pink cheeks.

Every character is a rig: parts carry ids the engine moves (toon.py reads RIGS for the pivots), feet stand on y = 0, the animal faces right.
Registers itself into art.BG / art.PLACE.
"""
import math, random
import art
from art import eye, INK, SUN

ELE = {"fill": "#a9bdd0", "shade": "#8aa1b8", "light": "#cfdcea", "line": "#3d5068", "far": "#93a9bf", "ear": "#f4bfcd", "nail": "#eef3f8"}
MON = {"fur": "#9c6b45", "dark": "#7b4f30", "face": "#f7dcbc", "line": "#3d2415"}
BEAR = {"fill": "#fdfaf2", "shade": "#e4dccd", "light": "#ffffff", "line": "#6a5a4c", "far": "#ece4d6"}
LAMB = {"wool": "#fffaf0", "shade": "#eadfcd", "face": "#f6dcc6", "line": "#6a5140", "leg": "#c9a98c", "far": "#b5967a"}
HOG = {"spine": "#8a5e3c", "dark": "#6a4429", "face": "#f6dfc0", "line": "#3f2a1a"}
TUR = {"shell": "#4fae7a", "dark": "#2f8a5a", "skin": "#a8dc8c", "line": "#1f5a3c", "belly": "#f2e6a8"}


def _ol(shapes, ln, w=9): return f'<g fill="{ln}" stroke="{ln}" stroke-width="{w * 2}" stroke-linejoin="round" stroke-linecap="round">{shapes}</g>'


def _brow(pid, x, y, w, col, wd=9):
    return f'<path id="{pid}-brow" d="M{x - w / 2} {y} q{w / 2} {-w * .28:.0f} {w} 0" stroke="{col}" stroke-width="{wd}" fill="none" stroke-linecap="round"/>'


def _mouth(pid, x, y, w, ln, wd=7):
    """A smile and a little frown at the same spot: the engine shows one of them (faces: happy / sad)."""
    return (f'<path id="{pid}-smile" d="M{x - w / 2} {y} q{w / 2} {w * .42:.0f} {w} 0" stroke="{ln}" stroke-width="{wd}" fill="none" stroke-linecap="round"/>'
            f'<path id="{pid}-frown" opacity="0" d="M{x - w / 2} {y + w * .2:.0f} q{w / 2} {-w * .36:.0f} {w} 0" stroke="{ln}" stroke-width="{wd}" fill="none" stroke-linecap="round"/>')


# ================================================================== elephant
MUD = ("#8a5a2c", "#6f4520", "#b07a42")      # wet mud: fill, dark, shine


def elephant(pid, calf=False, c=ELE, hat=False, mud=False):
    """An elephant, side view. calf=True: Tumble (big head, short trunk, a tuft of hair, no tusks). Parts: -neck (the whole head), -trunk (lifts: a snorkel,
    a reach, a hug), -ear (flaps, droops), -jaw (talks), -eye, -brow, -smile / -frown, -tail, -fl -bl -fl2 -bl2 (legs)."""
    ln = c["line"]; L = .8 if calf else 1.0; HK = 1.2 if calf else 1.0

    def leg(x, far, name):
        col = c["far"] if far else c["fill"]; h = 250 * L
        sh = f'<rect x="{x - 52}" y="-250" width="104" height="{h:.0f}" rx="42"/>'
        nails = "" if far else "".join(f'<path d="M{x - 34 + k * 26} {h - 252:.0f} q11 -22 22 0Z" fill="{c["nail"]}"/>' for k in range(3))
        sock = "" if (not mud or far) else (f'<clipPath id="{pid}-{name}c"><rect x="{x - 60}" y="{h - 250 - 96:.0f}" width="120" height="110"/></clipPath>'
                                            f'<g class="mud"><rect x="{x - 52}" y="-250" width="104" height="{h:.0f}" rx="42" fill="{MUD[0]}" clip-path="url(#{pid}-{name}c)"/>'
                                            f'<circle cx="{x - 24}" cy="{h - 250 - 98:.0f}" r="20" fill="{MUD[0]}"/><circle cx="{x + 22}" cy="{h - 250 - 94:.0f}" r="26" fill="{MUD[0]}"/></g>')
        return f'<g id="{pid}-{name}">{_ol(sh, ln)}<rect x="{x - 52}" y="-250" width="104" height="{h:.0f}" rx="42" fill="{col}"/>{nails}{sock}</g>'
    lift = 250 * (1 - L)
    far_legs = leg(-196, True, "bl2") + leg(96, True, "fl2"); near_legs = leg(-140, False, "bl") + leg(150, False, "fl")
    body = _ol('<ellipse cx="-14" cy="-340" rx="262" ry="172"/>', ln) + f'<ellipse cx="-14" cy="-340" rx="262" ry="172" fill="{c["fill"]}"/>'
    shade = (f'<path d="M-262 -300 A262 172 0 0 0 232 -300 A330 230 0 0 1 -262 -300Z" fill="{c["shade"]}" opacity=".6"/>'
             f'<ellipse cx="-90" cy="-448" rx="110" ry="30" fill="{c["light"]}" opacity=".55"/>')
    tail = (f'<g id="{pid}-tail"><path d="M-268 -390 q-46 60 -30 150" stroke="{ln}" stroke-width="30" fill="none" stroke-linecap="round"/>'
            f'<path d="M-268 -390 q-46 60 -30 150" stroke="{c["fill"]}" stroke-width="14" fill="none" stroke-linecap="round"/><ellipse cx="-298" cy="-232" rx="15" ry="24" fill="{ln}"/></g>')
    tl = 0.72 if calf else 1.0                                 # the calf's trunk is short
    mud_t = "" if not mud else f'<g class="mud"><circle cx="452" cy="{-430 + 214 * tl:.0f}" r="24" fill="{MUD[0]}"/><circle cx="470" cy="{-430 + 150 * tl:.0f}" r="13" fill="{MUD[0]}"/></g>'
    mud_b = "" if not mud else (f'<clipPath id="{pid}-bc"><ellipse cx="-14" cy="-340" rx="262" ry="172"/></clipPath><g class="mud" clip-path="url(#{pid}-bc)">'
                                f'<path d="M-300 -262 q45 -44 96 -10 q50 34 104 -16 q54 -44 112 4 q48 34 96 -22 q44 -34 92 4 L300 -150 L-300 -150Z" fill="{MUD[0]}"/>'
                                f'<path d="M-300 -206 q60 -30 130 -6 q70 24 150 -8 q80 -30 220 6 L300 -150 L-300 -150Z" fill="{MUD[1]}" opacity=".55"/>'
                                f'<ellipse cx="-150" cy="-410" rx="62" ry="42" fill="{MUD[0]}"/><ellipse cx="-36" cy="-462" rx="40" ry="24" fill="{MUD[0]}"/><circle cx="-86" cy="-338" r="17" fill="{MUD[0]}"/>'
                                f'<circle cx="66" cy="-376" r="23" fill="{MUD[0]}"/><circle cx="118" cy="-330" r="11" fill="{MUD[0]}"/><ellipse cx="-164" cy="-424" rx="26" ry="11" fill="{MUD[2]}" opacity=".8"/></g>')
    mud_e = "" if not mud else f'<g class="mud"><ellipse cx="176" cy="-474" rx="46" ry="34" fill="{MUD[0]}"/><circle cx="214" cy="-400" r="15" fill="{MUD[0]}"/><ellipse cx="166" cy="-484" rx="18" ry="8" fill="{MUD[2]}" opacity=".8"/></g>'
    mud_h = "" if not mud else f'<g class="mud"><ellipse cx="318" cy="-590" rx="62" ry="26" fill="{MUD[0]}"/><circle cx="396" cy="-552" r="13" fill="{MUD[0]}"/><ellipse cx="300" cy="-384" rx="22" ry="15" fill="{MUD[0]}"/></g>'
    trunk_d = f"M392 -430 C{470} {-430 + 20 * tl:.0f} {486} {-430 + 150 * tl:.0f} {448} {-430 + 232 * tl:.0f} C{430} {-430 + 276 * tl:.0f} {456} {-430 + 302 * tl:.0f} {492} {-430 + 284 * tl:.0f}"
    wr = "".join(f'<path d="M{438 + dx} {-430 + dy * tl:.0f} q22 8 44 -2" stroke="{c["shade"]}" stroke-width="7" fill="none" stroke-linecap="round" opacity=".8"/>' for dx, dy in ((14, 70), (12, 120), (0, 170)))
    trunk = (f'<g id="{pid}-trunk"><path d="{trunk_d}" stroke="{ln}" stroke-width="86" fill="none" stroke-linecap="round"/>'
             f'<path d="{trunk_d}" stroke="{c["fill"]}" stroke-width="68" fill="none" stroke-linecap="round"/>{wr}{mud_t}</g>')
    ear_sh = '<path d="M250 -590 C120 -640 60 -540 84 -430 C100 -340 180 -290 262 -330 C300 -420 300 -520 250 -590Z"/>'
    ear = (f'<g id="{pid}-ear">{_ol(ear_sh, ln)}<g fill="{c["fill"]}">{ear_sh}</g>'
           f'<path d="M240 -560 C150 -590 108 -520 124 -436 C136 -372 190 -338 244 -360 C270 -430 270 -500 240 -560Z" fill="{c["ear"]}"/>{mud_e}</g>')
    tusk = "" if calf else f'<path d="M372 -372 q54 26 92 -22 q-8 66 -76 66 q-22 0 -32 -18Z" fill="#fffdf4" stroke="{ln}" stroke-width="7" stroke-linejoin="round"/>'
    tuft = "" if not calf else "".join(f'<path d="M{286 + k * 16} -596 q-6 -30 {10 + k * 6} -40" stroke="{ln}" stroke-width="8" fill="none" stroke-linecap="round"/>' for k in range(3))
    hat_s = "" if not hat else (f'<g id="{pid}-hat"><path d="M254 -604 L312 -760 L370 -596Z" fill="#ff7aa2" stroke="{ln}" stroke-width="8" stroke-linejoin="round"/><circle cx="312" cy="-766" r="20" fill="{SUN}" stroke="{ln}" stroke-width="7"/>'
                                '<path d="M276 -660 l68 14 M266 -628 l92 18" stroke="#fff" stroke-width="10" stroke-linecap="round"/></g>')
    head_sh = '<circle cx="300" cy="-470" r="140"/>'
    hs0, hs1 = (f'<g transform="translate(200 -420) scale({HK}) translate(-200 420)">', '</g>')
    neck = (f'<g id="{pid}-neck">' + hs0 + _ol(head_sh, ln) + f'<circle cx="300" cy="-470" r="140" fill="{c["fill"]}"/>'
            f'<ellipse cx="330" cy="-560" rx="70" ry="24" fill="{c["light"]}" opacity=".5"/>' + mud_h + trunk +
            f'<g id="{pid}-jaw" opacity="0"><path d="M316 -372 q36 34 76 2 q-4 46 -40 46 q-30 0 -36 -48Z" fill="#c9667d" stroke="{ln}" stroke-width="7" stroke-linejoin="round"/></g>'
            f'<path d="M300 -396 q60 44 110 2 l0 -46 l-110 0Z" fill="{c["fill"]}"/>' + _mouth(pid, 356, -384, 76, ln) + tusk + ear
            + eye(f"{pid}-eye", 352, -486, 34 if calf else 30, lashes=0 if calf else 1, lid=c["fill"]) + _brow(pid, 352, -536, 62, ln)
            + f'<ellipse cx="398" cy="-436" rx="20" ry="12" fill="#ff8fb1" opacity=".6"/>' + tuft + hat_s + hs1 + '</g>')
    sh = '<ellipse cx="0" cy="4" rx="280" ry="20" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-all" transform="translate(0 {lift:.0f})">{tail}<g>{far_legs}</g>{body}{shade}{mud_b}{near_legs}{neck}</g></g>'


# ================================================================== spider monkey
def monkey(pid, c=MON, hang=False):
    """Mango the spider monkey, front view: long thin arms and legs, a long tail that holds on like an extra hand (Nat Geo Kids: the tail "can grasp and
    can be used like a fifth limb"). hang=True: she hangs upside down from her tail (the branch is at y = 0, she hangs below it).
    Parts: -body (all but the tail when hanging), -al -ar (arms), -tail, -eyeL -eyeR, -browL -browR, -jaw, -smile / -frown."""
    ln = c["line"]

    def limb(d, w=30): return f'<path d="{d}" stroke="{ln}" stroke-width="{w + 16}" fill="none" stroke-linecap="round"/><path d="{d}" stroke="{c["fur"]}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'

    def hand(x, y): return f'<circle cx="{x}" cy="{y}" r="22" fill="{c["dark"]}" stroke="{ln}" stroke-width="7"/>'
    legs = limb("M-36 -86 C-70 -60 -74 -30 -58 -10") + limb("M36 -86 C70 -60 74 -30 58 -10") + \
        f'<ellipse cx="-66" cy="-6" rx="34" ry="16" fill="{c["dark"]}" stroke="{ln}" stroke-width="7"/><ellipse cx="66" cy="-6" rx="34" ry="16" fill="{c["dark"]}" stroke="{ln}" stroke-width="7"/>'
    al = f'<g id="{pid}-al">{limb("M-58 -206 C-124 -190 -140 -120 -118 -66", 28)}{hand(-118, -62)}</g>'
    ar = f'<g id="{pid}-ar">{limb("M58 -206 C124 -190 140 -120 118 -66", 28)}{hand(118, -62)}</g>'
    torso = _ol('<ellipse cx="0" cy="-150" rx="74" ry="94"/>', ln, 8) + f'<ellipse cx="0" cy="-150" rx="74" ry="94" fill="{c["fur"]}"/><ellipse cx="0" cy="-134" rx="46" ry="62" fill="{c["face"]}"/>'
    head_sh = '<circle cx="0" cy="-296" r="100"/><circle cx="-102" cy="-300" r="36"/><circle cx="102" cy="-300" r="36"/>'
    head = (_ol(head_sh, ln, 8) + f'<circle cx="-102" cy="-300" r="36" fill="{c["fur"]}"/><circle cx="102" cy="-300" r="36" fill="{c["fur"]}"/>'
            f'<circle cx="-102" cy="-300" r="20" fill="{c["face"]}"/><circle cx="102" cy="-300" r="20" fill="{c["face"]}"/><circle cx="0" cy="-296" r="100" fill="{c["fur"]}"/>'
            f'<path d="M-14 -392 q-10 -30 6 -40 M4 -394 q0 -34 18 -42 M20 -390 q10 -24 28 -26" stroke="{ln}" stroke-width="8" fill="none" stroke-linecap="round"/>'
            f'<circle cx="-38" cy="-312" r="48" fill="{c["face"]}"/><circle cx="38" cy="-312" r="48" fill="{c["face"]}"/><ellipse cx="0" cy="-256" rx="66" ry="48" fill="{c["face"]}"/>'
            f'<ellipse cx="-30" cy="-390" rx="34" ry="14" fill="#fff" opacity=".2" transform="rotate(-18 -30 -390)"/>'
            + eye(f"{pid}-eyeL", -38, -312, 31, lid=c["face"]) + eye(f"{pid}-eyeR", 38, -312, 31, lid=c["face"])
            + f'<path id="{pid}-browL" d="M-70 -362 q30 -18 58 -4" stroke="{c["dark"]}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            + f'<path id="{pid}-browR" d="M70 -362 q-30 -18 -58 -4" stroke="{c["dark"]}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            + f'<ellipse cx="-66" cy="-262" rx="15" ry="10" fill="#ff8fb1" opacity=".7"/><ellipse cx="66" cy="-262" rx="15" ry="10" fill="#ff8fb1" opacity=".7"/>'
            + f'<circle cx="-9" cy="-268" r="4.5" fill="{ln}"/><circle cx="9" cy="-268" r="4.5" fill="{ln}"/>'
            + f'<g id="{pid}-jaw" opacity="0"><path d="M-24 -244 Q0 -196 24 -244Z" fill="#8a2f3f" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
            + f'<path d="M-30 -250 h60 v8 h-60Z" fill="{c["face"]}"/>' + _mouth(pid, 0, -246, 56, ln, 6))
    if hang:      # upside down under a branch: (0, 0) is where the tail holds on; -swing turns round that point
        tail_d = "M0 222 C-34 150 30 84 0 12 C-10 -26 -52 -32 -56 -4 C-58 18 -28 28 -14 6"
        return (f'<g id="{pid}"><g id="{pid}-swing"><g id="{pid}-tail">{limb(tail_d, 22)}</g>'
                f'<g id="{pid}-body" transform="translate(0 150) rotate(180)">{legs}{torso}{al}{ar}{head}</g></g></g>')
    tail_d = "M40 -80 C170 -60 226 -180 176 -262 C146 -310 92 -288 108 -244"
    tail = f'<g id="{pid}-tail">{limb(tail_d, 22)}</g>'
    sh = '<ellipse cx="0" cy="4" rx="110" ry="14" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}{tail}<g id="{pid}-body">{legs}{torso}{al}{ar}{head}</g></g>'


# ================================================================== polar bear cub
def bear(pid, c=BEAR):
    """Poppy the polar bear cub, side view: round and soft, small round ears, a black nose. Parts: -neck, -ear, -jaw, -eye, -brow, -tail, legs."""
    ln = c["line"]

    def leg(x, far, name):
        col = c["far"] if far else c["fill"]; sh = f'<rect x="{x - 46}" y="-150" width="92" height="150" rx="40"/>'
        pad = "" if far else f'<path d="M{x - 22} -4 q8 -14 16 0 M{x + 2} -4 q8 -14 16 0" stroke="{c["shade"]}" stroke-width="6" fill="none" stroke-linecap="round"/>'
        return f'<g id="{pid}-{name}">{_ol(sh, ln)}<rect x="{x - 46}" y="-150" width="92" height="150" rx="40" fill="{col}"/>{pad}</g>'
    body = _ol('<ellipse cx="-10" cy="-212" rx="212" ry="132"/>', ln) + f'<ellipse cx="-10" cy="-212" rx="212" ry="132" fill="{c["fill"]}"/>'
    shade = f'<path d="M-214 -180 A212 132 0 0 0 190 -180 A270 180 0 0 1 -214 -180Z" fill="{c["shade"]}" opacity=".7"/>'
    tail_sh = '<circle cx="-214" cy="-250" r="30"/>'
    tail = f'<g id="{pid}-tail">{_ol(tail_sh, ln, 7)}<circle cx="-214" cy="-250" r="30" fill="{c["fill"]}"/></g>'
    head_sh = '<circle cx="214" cy="-306" r="118"/><ellipse cx="300" cy="-272" rx="70" ry="54"/>'
    ear_sh = '<circle cx="150" cy="-402" r="38"/>'
    neck = (f'<g id="{pid}-neck"><g id="{pid}-ear">{_ol(ear_sh, ln)}<circle cx="150" cy="-402" r="38" fill="{c["fill"]}"/><circle cx="152" cy="-398" r="20" fill="#f6c9d3"/></g>'
            + _ol(head_sh, ln) + f'<circle cx="214" cy="-306" r="118" fill="{c["fill"]}"/><circle cx="266" cy="-408" r="34" fill="{c["fill"]}" stroke="{ln}" stroke-width="9"/><circle cx="266" cy="-404" r="18" fill="#f6c9d3"/>'
            f'<g id="{pid}-jaw" opacity="0"><path d="M270 -246 q34 30 70 4 q-6 36 -36 36 q-26 0 -34 -40Z" fill="#c9667d" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
            f'<ellipse cx="300" cy="-272" rx="70" ry="54" fill="{c["light"]}"/><ellipse cx="300" cy="-262" rx="70" ry="44" fill="{c["shade"]}" opacity=".35"/>'
            f'<ellipse cx="346" cy="-296" rx="24" ry="17" fill="#2a2320"/><ellipse cx="340" cy="-302" rx="8" ry="4" fill="#fff" opacity=".6"/>'
            + _mouth(pid, 318, -246, 54, ln, 6) + eye(f"{pid}-eye", 246, -330, 28, lid=c["fill"]) + _brow(pid, 246, -374, 52, ln, 8)
            + f'<ellipse cx="266" cy="-284" rx="17" ry="10" fill="#ff8fb1" opacity=".6"/></g>')
    sh = '<ellipse cx="0" cy="4" rx="230" ry="18" fill="#000" opacity=".12"/>'
    return f'<g id="{pid}">{sh}{tail}<g>{leg(-150, True, "bl2")}{leg(96, True, "fl2")}</g>{body}{shade}{leg(-106, False, "bl")}{leg(140, False, "fl")}{neck}</g>'


# ================================================================== lamb
def lamb(pid, c=LAMB):
    """Clover the lamb, side view: a woolly cloud on four thin legs. Parts: -neck, -ear, -jaw, -eye, -brow, -tail, legs."""
    ln = c["line"]

    def leg(x, far, name):
        col = c["far"] if far else c["leg"]; sh = f'<rect x="{x - 17}" y="-170" width="34" height="164" rx="15"/><ellipse cx="{x + 2}" cy="-8" rx="24" ry="13"/>'
        return f'<g id="{pid}-{name}">{_ol(sh, ln, 7)}<rect x="{x - 17}" y="-170" width="34" height="164" rx="15" fill="{col}"/><ellipse cx="{x + 2}" cy="-8" rx="24" ry="13" fill="{ln}"/></g>'
    puffs = [(-150, -250, 78), (-70, -310, 86), (30, -316, 88), (120, -270, 78), (-160, -180, 70), (-60, -160, 84), (50, -160, 84), (140, -190, 70), (-10, -236, 110)]
    wool_sh = "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in puffs)
    body = _ol(wool_sh, ln) + f'<g fill="{c["wool"]}">{wool_sh}</g>' + "".join(f'<path d="M{x - 26} {y + 6} q26 -30 52 0" stroke="{c["shade"]}" stroke-width="8" fill="none" stroke-linecap="round"/>' for x, y in ((-90, -250), (20, -270), (90, -200), (-40, -180), (-130, -190)))
    tail_sh = '<circle cx="-214" cy="-262" r="34"/>'
    tail = f'<g id="{pid}-tail">{_ol(tail_sh, ln, 7)}<circle cx="-214" cy="-262" r="34" fill="{c["wool"]}"/></g>'
    head_sh = '<ellipse cx="222" cy="-330" rx="84" ry="74"/><circle cx="170" cy="-398" r="40"/><circle cx="222" cy="-416" r="44"/><circle cx="272" cy="-396" r="36"/>'
    ear_sh = '<ellipse cx="150" cy="-338" rx="42" ry="20" transform="rotate(28 150 -338)"/>'
    neck = (f'<g id="{pid}-neck">' + _ol(head_sh, ln) + f'<ellipse cx="222" cy="-330" rx="84" ry="74" fill="{c["face"]}"/>'
            f'<g fill="{c["wool"]}"><circle cx="170" cy="-398" r="40"/><circle cx="222" cy="-416" r="44"/><circle cx="272" cy="-396" r="36"/></g>'
            f'<g id="{pid}-ear">{_ol(ear_sh, ln, 7)}<ellipse cx="150" cy="-338" rx="42" ry="20" fill="{c["face"]}" transform="rotate(28 150 -338)"/><ellipse cx="148" cy="-336" rx="26" ry="10" fill="#f6b8c6" transform="rotate(28 148 -336)"/></g>'
            f'<g id="{pid}-jaw" opacity="0"><path d="M258 -292 q22 22 46 2 q-4 28 -24 28 q-18 0 -22 -30Z" fill="#c9667d" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
            f'<ellipse cx="282" cy="-306" rx="34" ry="26" fill="{c["face"]}"/><path d="M286 -322 l14 0 l-7 10Z" fill="#e88aa0" stroke="{ln}" stroke-width="5" stroke-linejoin="round"/>'
            + _mouth(pid, 286, -294, 36, ln, 6) + eye(f"{pid}-eye", 232, -346, 27, lid=c["face"]) + _brow(pid, 232, -386, 46, ln, 7)
            + f'<ellipse cx="250" cy="-304" rx="14" ry="9" fill="#ff8fb1" opacity=".6"/></g>')
    sh = '<ellipse cx="0" cy="4" rx="220" ry="16" fill="#000" opacity=".12"/>'
    return f'<g id="{pid}">{sh}{tail}<g>{leg(-120, True, "bl2")}{leg(70, True, "fl2")}</g>{body}{leg(-80, False, "bl")}{leg(110, False, "fl")}{neck}</g>'


# ================================================================== hedgehog
def hedgehog(pid, c=HOG):
    """Hazel the hedgehog, side view: a dome of soft spines, a cream face, a pointed snout. Parts: -neck (the face), -jaw, -eye, -brow, -spines, legs."""
    ln = c["line"]; r = random.Random(4); pts = []
    for k in range(15):                                   # the spiny back: a zigzag along a dome
        a = math.pi * (1.0 - k / 14 * 0.86); R = 190 if k % 2 == 0 else 236
        pts.append((-20 + R * 1.08 * math.cos(a), -70 - R * .86 * math.sin(a) + r.uniform(-6, 6)))
    d = "M-226 -66 " + " ".join(f"L{x:.0f} {y:.0f}" for x, y in pts) + " L150 -40 Q-40 -10 -226 -66Z"
    spines = f'<g id="{pid}-spines">{_ol(f"<path d=\"{d}\"/>", ln, 8)}<path d="{d}" fill="{c["spine"]}"/>' + \
        "".join(f'<path d="M{-150 + k * 52} {-130 - 46 * math.sin(k * .55):.0f} l-16 -44" stroke="{c["dark"]}" stroke-width="9" stroke-linecap="round"/>' for k in range(6)) + '</g>'

    def leg(x, name): return f'<g id="{pid}-{name}"><ellipse cx="{x}" cy="-10" rx="34" ry="18" fill="{c["face"]}" stroke="{ln}" stroke-width="8"/></g>'
    face_sh = '<path d="M70 -210 C150 -230 230 -160 290 -86 C300 -70 290 -54 270 -52 C200 -40 120 -40 70 -52Z"/><circle cx="96" cy="-214" r="30"/>'
    neck = (f'<g id="{pid}-neck"><g id="{pid}-ear"><circle cx="96" cy="-214" r="30" fill="{c["face"]}" stroke="{ln}" stroke-width="9"/><circle cx="98" cy="-210" r="15" fill="#f6b8c6"/></g>'
            + _ol('<path d="M70 -210 C150 -230 230 -160 290 -86 C300 -70 290 -54 270 -52 C200 -40 120 -40 70 -52Z"/>', ln, 8)
            + f'<path d="M70 -210 C150 -230 230 -160 290 -86 C300 -70 290 -54 270 -52 C200 -40 120 -40 70 -52Z" fill="{c["face"]}"/>'
            f'<g id="{pid}-jaw" opacity="0"><path d="M214 -62 q22 20 46 4 q-6 24 -24 24 q-16 0 -22 -28Z" fill="#c9667d" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
            f'<path d="M200 -70 q40 22 78 6 l6 -20 l-84 0Z" fill="{c["face"]}"/><circle cx="288" cy="-80" r="19" fill="#2a2320"/><circle cx="283" cy="-86" r="5" fill="#fff" opacity=".7"/>'
            + _mouth(pid, 236, -66, 44, ln, 6) + eye(f"{pid}-eye", 170, -140, 27, lid=c["face"]) + _brow(pid, 170, -182, 46, ln, 7)
            + f'<ellipse cx="196" cy="-98" rx="15" ry="9" fill="#ff8fb1" opacity=".6"/></g>')
    belly = f'<path d="M-200 -60 Q-20 -16 160 -44 L160 -26 Q-20 0 -200 -40Z" fill="{c["face"]}" stroke="{ln}" stroke-width="8" stroke-linejoin="round"/>'
    sh = '<ellipse cx="10" cy="4" rx="240" ry="15" fill="#000" opacity=".12"/>'
    return f'<g id="{pid}">{sh}{leg(-150, "bl2")}{leg(60, "fl2")}{spines}{belly}{neck}{leg(-100, "bl")}{leg(120, "fl")}</g>'


# ================================================================== sea turtle
def turtle(pid, c=TUR):
    """Tula the green sea turtle, side view, swimming: a domed shell, long front flippers. Parts: -neck (head), -jaw, -eye, -brow, -ff (front flipper), -bf."""
    ln = c["line"]
    shell_d = "M-196 -150 C-150 -330 130 -350 204 -150Z"
    plates = "".join(f'<path d="{p}" stroke="{c["dark"]}" stroke-width="9" fill="none" stroke-linecap="round"/>' for p in
                     ("M-120 -190 Q-60 -290 0 -300 Q60 -296 130 -200", "M-70 -160 L-40 -240 L40 -246 L80 -160", "M-40 -240 L-70 -296 M40 -246 L74 -300 M-150 -160 L-120 -190 M160 -160 L130 -200"))
    shell = f'<g id="{pid}-shell">{_ol(f"<path d=\"{shell_d}\"/>", ln)}<path d="{shell_d}" fill="{c["shell"]}"/>{plates}<path d="M-120 -260 Q-40 -320 60 -318" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".35"/></g>'
    under_d = "M-210 -150 Q0 -84 214 -150 Q0 -128 -210 -150Z"
    under = _ol('<path d="M-206 -150 Q0 -70 210 -150Z"/>', ln, 8) + f'<path d="M-206 -150 Q0 -70 210 -150Z" fill="{c["belly"]}"/>'
    ff_d = "M110 -124 C190 -90 150 30 60 60 C50 -10 60 -70 80 -120Z"; bf_d = "M-150 -124 C-230 -110 -250 -50 -226 -20 C-190 -40 -160 -80 -128 -116Z"
    ff = f'<g id="{pid}-ff">{_ol(f"<path d=\"{ff_d}\"/>", ln, 8)}<path d="{ff_d}" fill="{c["skin"]}"/><circle cx="96" cy="-30" r="9" fill="{c["dark"]}" opacity=".5"/><circle cx="112" cy="-66" r="7" fill="{c["dark"]}" opacity=".5"/></g>'
    bf = f'<g id="{pid}-bf">{_ol(f"<path d=\"{bf_d}\"/>", ln, 8)}<path d="{bf_d}" fill="{c["skin"]}"/></g>'
    head_sh = '<path d="M170 -170 C210 -250 330 -250 346 -180 C352 -130 300 -110 230 -120 C200 -124 176 -140 170 -170Z"/>'
    neck = (f'<g id="{pid}-neck">' + _ol(head_sh, ln) + f'<g fill="{c["skin"]}">{head_sh}</g>'
            f'<g id="{pid}-jaw" opacity="0"><path d="M286 -134 q22 18 44 2 q-6 22 -22 22 q-16 0 -22 -24Z" fill="#c9667d" stroke="{ln}" stroke-width="6" stroke-linejoin="round"/></g>'
            f'<path d="M270 -140 q36 20 70 2 l4 -22 l-74 0Z" fill="{c["skin"]}"/>' + _mouth(pid, 306, -136, 44, ln, 6)
            + eye(f"{pid}-eye", 272, -186, 28, lid=c["skin"]) + _brow(pid, 272, -228, 46, ln, 7) + f'<ellipse cx="296" cy="-150" rx="14" ry="8" fill="#ff8fb1" opacity=".6"/>'
            f'<circle cx="222" cy="-214" r="8" fill="{c["dark"]}" opacity=".45"/><circle cx="204" cy="-186" r="6" fill="{c["dark"]}" opacity=".45"/></g>')
    return f'<g id="{pid}">{bf}{neck}{under}{shell}{ff}</g>'


# ================================================================== the rigs: what the engine may move, and round which point
def _quad(neck, tail, ear, legs, hip, jaw):
    return {"neck": neck, "tail": tail, "ear": ear, "legs": legs, "hip": hip, "jaw": jaw}


RIGS = {
    "elephant": dict(build=lambda p: elephant(p), **_quad("200 -420", "-268 -390", "250 -590", {"fl": 150, "bl": -140, "fl2": 96, "bl2": -196}, -250, ("y", 16)), eyes=["eye"], brows=["brow"], trunk="392 -430"),
    "elephant_hat": dict(build=lambda p: elephant(p, hat=True), **_quad("200 -420", "-268 -390", "250 -590", {"fl": 150, "bl": -140, "fl2": 96, "bl2": -196}, -250, ("y", 16)), eyes=["eye"], brows=["brow"], trunk="392 -430"),
    "tumble": dict(build=lambda p: elephant(p, calf=True), **_quad("200 -420", "-268 -390", "250 -590", {"fl": 150, "bl": -140, "fl2": 96, "bl2": -196}, -250, ("y", 16)), eyes=["eye"], brows=["brow"], trunk="392 -430"),
    "elephant_mud": dict(build=lambda p: elephant(p, mud=True), **_quad("200 -420", "-268 -390", "250 -590", {"fl": 150, "bl": -140, "fl2": 96, "bl2": -196}, -250, ("y", 16)), eyes=["eye"], brows=["brow"], trunk="392 -430"),
    "tumble_mud": dict(build=lambda p: elephant(p, calf=True, mud=True), **_quad("200 -420", "-268 -390", "250 -590", {"fl": 150, "bl": -140, "fl2": 96, "bl2": -196}, -250, ("y", 16)), eyes=["eye"], brows=["brow"], trunk="392 -430"),
    "monkey": dict(build=lambda p: monkey(p), neck=None, tail="40 -80", ear=None, legs=None, hip=0, jaw=("y", 12), eyes=["eyeL", "eyeR"], brows=["browL", "browR"]),
    "monkey_hang": dict(build=lambda p: monkey(p, hang=True), neck=None, tail=None, ear=None, legs=None, hip=0, jaw=("y", 12), eyes=["eyeL", "eyeR"], brows=["browL", "browR"]),
    "bear": dict(build=lambda p: bear(p), **_quad("120 -250", "-214 -250", "150 -402", {"fl": 140, "bl": -106, "fl2": 96, "bl2": -150}, -150, ("y", 12)), eyes=["eye"], brows=["brow"]),
    "lamb": dict(build=lambda p: lamb(p), **_quad("150 -290", "-214 -262", "170 -350", {"fl": 110, "bl": -80, "fl2": 70, "bl2": -120}, -170, ("y", 10)), eyes=["eye"], brows=["brow"]),
    "hedgehog": dict(build=lambda p: hedgehog(p), **_quad("90 -110", None, "96 -214", None, 0, ("y", 9)), eyes=["eye"], brows=["brow"]),
    "turtle": dict(build=lambda p: turtle(p), **_quad("180 -170", None, None, None, 0, ("y", 9)), eyes=["eye"], brows=["brow"]),
}


# ================================================================== places
def _hill(d, col): return f'<path d="{d}" fill="{col}"/>'


def _acacia(x, y, s=1.0, col="#6f9a4a", dark="#57803a"):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-10 0 Q-18 -120 -4 -200 L-70 -260 L-56 -268 L4 -222 L60 -276 L74 -266 L14 -196 Q4 -110 14 0Z" fill="#8a6238"/>'
            f'<ellipse cx="0" cy="-292" rx="190" ry="46" fill="{col}"/><ellipse cx="-70" cy="-312" rx="110" ry="34" fill="{dark}" opacity=".6"/><ellipse cx="60" cy="-316" rx="96" ry="30" fill="{col}"/></g>')


def _grass(x, y, s=1.0, col="#c9a84a"):
    return f'<g transform="translate({x} {y}) scale({s})">' + "".join(f'<path d="M{k * 12} 0 q{-6 + k * 4} -46 {-16 + k * 9} -78" stroke="{col}" stroke-width="7" fill="none" stroke-linecap="round"/>' for k in range(-2, 3)) + '</g>'


def bg_savanna(p):
    """The wide, sunny savanna: golden grass and flat-topped trees."""
    far = art._sky(p, "#8fd6ff", "#fff2c9") + art._sun(p + "sun", 1500, 220, 84) + art._cloud(p + "c1", 380, 180) + art._cloud(p + "c2", 1120, 120, .7) + \
        _hill("M-500 640 C100 540 500 600 900 570 S1700 540 2420 620 L2420 760 L-500 760Z", "#d9c877")
    mid = _hill("M-500 720 C200 660 700 700 1200 680 S2000 670 2420 710 L2420 900 L-500 900Z", "#e6cd72") + _acacia(260, 740, 1.15) + _acacia(1650, 730, .9) + _acacia(1050, 716, .55, "#7da755")
    near = ('<rect x="-500" y="840" width="2920" height="1200" fill="#e0bf5c"/>' + _hill("M-500 860 C300 820 900 850 1400 832 S2100 840 2420 850 L2420 900 L-500 900Z", "#e0bf5c")
            + "".join(_grass(x, y, s) for x, y, s in ((120, 900, 1.0), (520, 960, 1.2), (980, 1000, 1.0), (1420, 950, 1.1), (1800, 1010, 1.2), (760, 1050, .9)))
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="6" fill="#cba94a" opacity=".6"/>' for x, y, w in ((320, 1010, 90), (1180, 1040, 110), (1640, 900, 70))))
    return far, mid, near


def bg_river(p):
    """The savanna river: wide, blue and slow."""
    far, mid, _ = bg_savanna(p)
    near = ('<rect x="-500" y="820" width="2920" height="1200" fill="#e0bf5c"/>'
            f'<path d="M-500 800 C200 770 800 800 1300 784 S2100 790 2420 800 L2420 1100 L-500 1100Z" fill="#5fb8ea"/>'
            '<path d="M-500 1060 C300 1030 900 1060 1400 1044 S2100 1050 2420 1060 L2420 1980 L-500 1980Z" fill="#d6b352"/>'
            + "".join(f'<path id="{p}w{k}" d="M{x} {y} q30 -14 60 0 q30 14 60 0" stroke="#bfe6fb" stroke-width="8" fill="none" stroke-linecap="round" opacity=".9"/>' for k, (x, y) in enumerate(((200, 870), (700, 930), (1150, 880), (1560, 960), (420, 1000), (1840, 890))))
            + _grass(140, 1090, 1.1, "#7fae4c") + _grass(1700, 1084, 1.2, "#7fae4c") + _grass(960, 1100, .9, "#7fae4c"))
    return far, mid, near


def _leaf(x, y, s, rot, col):
    return f'<path d="M0 0 C40 -70 130 -80 190 -20 C130 20 50 30 0 0Z" fill="{col}" transform="translate({x} {y}) rotate({rot}) scale({s})"/>'


def _jtree(x, w, col="#7a5632", h=1400): return f'<rect x="{x - w / 2}" y="{-h + 900}" width="{w}" height="{h}" fill="{col}"/>'


def bg_jungle(p):
    """The green jungle: tall trunks, big leaves, hanging vines."""
    far = art._sky(p, "#bff0d4", "#e9fbd9", y1=1100) + "".join(_jtree(x, w, "#6f9a72", 1700) for x, w in ((120, 70), (520, 50), (900, 80), (1340, 56), (1760, 76))) + \
        "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#8fc98f"/>' for x, y, rx, ry in ((200, 120, 330, 170), (820, 60, 380, 190), (1500, 130, 400, 180), (2100, 80, 300, 170)))
    mid = ("".join(_jtree(x, w) for x, w in ((330, 96), (1560, 110))) + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/>' for x, y, rx, ry, c in
           ((330, 160, 300, 150, "#3f9e5c"), (1560, 120, 340, 170, "#3f9e5c"), (960, 40, 360, 120, "#4fb56c"), (-100, 220, 240, 130, "#4fb56c"), (2050, 250, 260, 130, "#4fb56c")))
           + "".join(f'<path d="M{x} {y0} q{dx} {(y1 - y0) / 2:.0f} 0 {y1 - y0}" stroke="#2f8a4c" stroke-width="10" fill="none" stroke-linecap="round"/>' for x, y0, y1, dx in ((700, 60, 430, 40), (1180, 80, 380, -36), (1840, 200, 520, 30)))
           + '<path d="M-500 760 C200 700 800 740 1300 720 S2100 720 2420 750 L2420 900 L-500 900Z" fill="#5cb86a"/>')
    near = ('<rect x="-500" y="850" width="2920" height="1200" fill="#4aa85a"/><path d="M-500 870 C300 836 900 860 1400 846 S2100 850 2420 862 L2420 900 L-500 900Z" fill="#4aa85a"/>'
            + _leaf(-40, 900, 1.5, -40, "#2f8a4c") + _leaf(60, 930, 1.3, -80, "#3f9e5c") + _leaf(1900, 930, 1.5, -130, "#2f8a4c") + _leaf(1800, 950, 1.2, -95, "#3f9e5c")
            + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="{c}"/><circle cx="{x}" cy="{y}" r="5" fill="#fff6c0"/>' for x, y, c in ((420, 980, "#ff7aa2"), (1240, 1010, "#ffb347"), (860, 1040, "#ff7aa2"), (1640, 1000, "#fff")))
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="6" fill="#3c9550" opacity=".7"/>' for x, y, w in ((300, 1030, 100), (1100, 960, 120), (1560, 1050, 80))))
    return far, mid, near


def bg_bigtree(p):
    """The tallest tree in the jungle: the ground at the bottom, one great trunk, a branch far above (y = -520) where the golden fruit hangs."""
    far, mid, near = bg_jungle(p)
    trunk = (f'<path d="M1330 900 C1310 500 1320 -300 1300 -1100 L1560 -1100 C1540 -300 1560 500 1600 900Z" fill="#8a6238"/>'
             f'<path d="M1500 900 C1470 500 1480 -300 1470 -1100 L1560 -1100 C1540 -300 1560 500 1600 900Z" fill="#735029" opacity=".7"/>'
             + "".join(f'<path d="M{1370 + (k % 2) * 60} {700 - k * 210} q20 -30 6 -70" stroke="#6a4a26" stroke-width="9" fill="none" stroke-linecap="round"/>' for k in range(8))
             + '<path d="M1340 -470 C1100 -500 900 -520 640 -500 L640 -548 C900 -570 1100 -556 1330 -560Z" fill="#8a6238"/>'
             + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/>' for x, y, rx, ry, c in
                       ((1440, -900, 520, 240, "#3f9e5c"), (900, -760, 380, 170, "#4fb56c"), (1900, -720, 360, 180, "#4fb56c"), (560, -610, 200, 90, "#3f9e5c"), (1440, -690, 300, 120, "#57c078"))))
    sky_up = f'<rect x="-500" y="-1700" width="2920" height="900" fill="#bff0d4"/>'
    return sky_up + far, mid + trunk, near


def bg_canopy(p):
    """High in the treetops: sky, leaves and one strong branch (y = 430)."""
    far = art._sky(p, "#9fe0ff", "#e4fbe6", y1=1300) + art._sun(p + "sun", 1640, 190, 76) + art._cloud(p + "c1", 420, 200, .9) + \
        "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#8fd09a"/>' for x, y, rx, ry in ((200, 1000, 420, 200), (980, 1060, 460, 210), (1760, 1010, 420, 200)))
    mid = ("".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/>' for x, y, rx, ry, c in ((60, 150, 380, 190, "#3f9e5c"), (1900, 380, 300, 200, "#3f9e5c"), (760, 60, 420, 130, "#4fb56c")))
           + '<path d="M-500 400 C200 380 900 430 1500 410 S2200 420 2420 400 L2420 470 C1800 480 1200 486 600 470 S-200 450 -500 462Z" fill="#8a6238"/>'
           '<path d="M-500 440 C200 430 900 466 1500 452 S2200 456 2420 444 L2420 470 C1800 480 1200 486 600 470 S-200 450 -500 462Z" fill="#735029" opacity=".7"/>')
    near = (_leaf(-60, 420, 1.6, -30, "#2f8a4c") + _leaf(1700, 430, 1.6, -150, "#2f8a4c") + _leaf(300, 400, 1.0, -70, "#57c078") + _leaf(1400, 410, 1.1, -110, "#57c078")
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/>' for x, y, rx, ry, c in ((-200, 980, 420, 200, "#3f9e5c"), (2120, 1000, 420, 220, "#3f9e5c"))))
    return far, mid, near


def bg_zoo_eve(p):
    """The zoo gate when the sun is low: the same place, in warm evening light."""
    far, mid, near = art.bg_zoo(p)
    far = far.replace("#8fd8ff", "#ffb07a").replace("#eaf8ff", "#ffe9bf").replace("#a8e08a", "#b9c979")
    far = far.replace(f'cx="250" cy="200"', 'cx="1560" cy="470"')
    mid = mid.replace("#8fd470", "#a3c063").replace("#4fb565", "#5fa055").replace("#43a559", "#528f4b").replace("#5cc473", "#74b060")
    near = near.replace("#7cc95e", "#93b955")
    return far, mid, near


def bg_dune_eve(p):
    """The big sandy hill late in the day."""
    far, mid, near = art.bg_dunes(p)
    far = far.replace("#7fd0ff", "#ffb98a").replace("#ffe9c4", "#ffe4b0").replace('cx="1560" cy="210"', 'cx="1560" cy="430"')
    return far, mid, near


def bg_ocean(p):
    """Under the blue sea: light from above, sand and seagrass below."""
    far = art._sky(p, "#8fe0ff", "#2f9fd6", y1=1100) + '<rect x="-500" y="1100" width="2920" height="900" fill="#2f9fd6"/>' + \
        "".join(f'<path d="M{x} -100 L{x + 120} 900 L{x + 260} 900 L{x + 60} -100Z" fill="#fff" opacity=".08"/>' for x in (100, 700, 1300))
    mid = ('<path d="M-500 820 C200 760 700 800 1200 780 S2000 780 2420 810 L2420 900 L-500 900Z" fill="#f2dfa6"/>'
           + "".join(f'<path d="M{x} 830 q{d} -90 0 -180 q{-d} -90 0 -170" stroke="#3fae7a" stroke-width="16" fill="none" stroke-linecap="round"/>' for x, d in ((220, 40), (300, -30), (1620, 36), (1720, -40)))
           + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#fff" stroke-width="5" opacity=".6"/>' for x, y, r in ((520, 420, 16), (560, 330, 10), (1380, 520, 14), (1420, 440, 9))))
    near = '<rect x="-500" y="870" width="2920" height="1200" fill="#ecd592"/>' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w * .5:.0f}" fill="{c}"/>' for x, y, w, c in ((420, 960, 60, "#ff9ab8"), (1500, 990, 70, "#ffb347"), (980, 1040, 50, "#c9a8f0")))
    return far, mid, near


def bg_arctic(p):
    """The snowy Arctic: white ice, blue water, a pale sky."""
    far = art._sky(p, "#bfe6ff", "#f2fbff") + art._sun(p + "sun", 400, 240, 70, "#fff7c9") + \
        '<path d="M-500 660 L-100 420 L260 640 L620 380 L1000 660 L1400 440 L1800 650 L2140 470 L2420 640 L2420 760 L-500 760Z" fill="#dcefff"/>' \
        '<path d="M-100 420 L20 494 L-60 520Z M620 380 L740 470 L640 500Z M1400 440 L1520 520 L1420 546Z" fill="#fff"/>'
    mid = '<rect x="-500" y="720" width="2920" height="240" fill="#6fbfe8"/>' + "".join(f'<path d="M{x} {y} q40 -22 90 -8 q50 -20 100 6 l-10 30 l-170 0Z" fill="#fff"/>' for x, y in ((120, 770), (1500, 790), (900, 750)))
    near = '<path d="M-500 860 C200 820 800 850 1300 836 S2100 840 2420 850 L2420 1980 L-500 1980Z" fill="#ffffff"/>' + \
        "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="8" fill="#dcefff"/>' for x, y, w in ((300, 960, 120), (1100, 1010, 140), (1700, 950, 90)))
    return far, mid, near


def bg_farm(p):
    """The farm: a red barn, a fence, soft green fields."""
    far = art._sky(p, "#8fd8ff", "#eaf8ff") + art._sun(p + "sun", 300, 200, 84) + art._cloud(p + "c1", 1000, 160) + \
        '<path d="M-500 700 C0 580 500 640 900 610 S1700 580 2420 680 L2420 800 L-500 800Z" fill="#a8e08a"/>'
    barn = ('<g transform="translate(1500 800)"><path d="M-190 0 V-210 L0 -340 L190 -210 V0Z" fill="#e2574c"/><path d="M-210 -200 L0 -350 L210 -200 L190 -186 L0 -322 L-190 -186Z" fill="#fff"/>'
            '<rect x="-60" y="-150" width="120" height="150" fill="#b83b34"/><path d="M-60 -150 L60 0 M60 -150 L-60 0" stroke="#fff" stroke-width="10"/><rect x="-36" y="-262" width="72" height="56" rx="8" fill="#fff"/></g>')
    mid = '<path d="M-500 780 C200 720 700 760 1200 740 S2000 730 2420 770 L2420 900 L-500 900Z" fill="#8fd470"/>' + barn + \
        "".join(f'<rect x="{x}" y="716" width="18" height="96" rx="6" fill="#f2e6c8"/>' for x in range(-40, 1100, 130)) + '<rect x="-60" y="736" width="1160" height="16" rx="6" fill="#f2e6c8"/><rect x="-60" y="776" width="1160" height="16" rx="6" fill="#f2e6c8"/>'
    near = '<rect x="-500" y="860" width="2920" height="1200" fill="#7cc95e"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/>' for x, y, c in ((300, 960, "#fff"), (520, 1010, SUN), (1300, 980, "#fff"), (1760, 1020, "#ff7aa2")))
    return far, mid, near


def bg_nightforest(p):
    """The night forest: a cosy, moonlit wood with fireflies. Soft and bright enough to see every face."""
    far = art._sky(p, "#2b3f8f", "#5a6fc0", y1=1100) + f'<circle cx="1520" cy="230" r="150" fill="#fff6c9" opacity=".18"/><circle cx="1520" cy="230" r="92" fill="#fff6c9"/>' + \
        "".join(f'<circle class="{p}star" cx="{x}" cy="{y}" r="{r}" fill="#fff"/>' for x, y, r in ((200, 120, 5), (520, 220, 4), (860, 90, 5), (1160, 260, 4), (1840, 140, 5), (360, 330, 3), (1000, 380, 3))) + \
        "".join(f'<path d="M{x} 760 L{x + 90} {440 - h} L{x + 180} 760Z" fill="#33508f"/>' for x, h in ((-80, 0), (260, 80), (640, 20), (1120, 90), (1700, 40), (2040, 70)))
    mid = "".join(f'<g transform="translate({x} 860)"><rect x="-18" y="-120" width="36" height="120" fill="#4a3a5a"/><path d="M-130 -100 L0 -420 L130 -100Z" fill="#2f6a6a"/><path d="M-100 -240 L0 -500 L100 -240Z" fill="#3a7f7a"/></g>' for x in (140, 1780)) + \
        '<path d="M-500 780 C200 720 700 760 1200 740 S2000 730 2420 770 L2420 900 L-500 900Z" fill="#3f6f86"/>'
    near = '<rect x="-500" y="860" width="2920" height="1200" fill="#4d7f8f"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="#ffe98a" opacity=".25"/><circle cx="{x}" cy="{y}" r="6" fill="#ffe98a"/>' for x, y in ((420, 620), (760, 520), (1180, 640), (1460, 560), (980, 720)))
    return far, mid, near


art.BG.update({"savanna": bg_savanna, "river": bg_river, "jungle": bg_jungle, "bigtree": bg_bigtree, "canopy": bg_canopy, "zoo_eve": bg_zoo_eve, "dune_eve": bg_dune_eve,
               "ocean": bg_ocean, "arctic": bg_arctic, "farm": bg_farm, "nightforest": bg_nightforest})
art.PLACE.update({"savanna": "the sunny savanna", "river": "the wide river", "jungle": "the green jungle", "bigtree": "the tallest tree", "canopy": "the treetops",
                  "zoo_eve": "the zoo at sunset", "dune_eve": "the big sandy hill", "ocean": "the blue ocean", "arctic": "the snowy Arctic", "farm": "the farm", "nightforest": "the night forest"})


# ================================================================== story props
def fruit(pid, s=1.0):
    """The golden fruit."""
    return (f'<g id="{pid}"><path d="M0 -92 q-6 -26 14 -40" stroke="#6a4a26" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M12 -128 q40 -26 62 6 q-40 18 -62 -6Z" fill="#4fb56c" stroke="#2f8a4c" stroke-width="6" stroke-linejoin="round"/>'
            f'<ellipse cx="0" cy="-10" rx="78" ry="86" fill="#ffb81f" stroke="#a8640a" stroke-width="9"/><ellipse cx="-26" cy="-40" rx="26" ry="34" fill="#ffe08a" opacity=".8"/>'
            f'<path d="M-66 20 A78 86 0 0 0 66 20 A100 110 0 0 1 -66 20Z" fill="#f08a00" opacity=".55"/></g>')


def fruit_splat(pid):
    return (f'<g id="{pid}"><path d="M-150 0 q20 -50 70 -40 q20 -40 70 -30 q40 -30 80 6 q50 -4 60 40 q-40 30 -100 26 q-60 14 -120 0 q-50 6 -60 -2Z" fill="#ffb81f" stroke="#a8640a" stroke-width="9" stroke-linejoin="round"/>'
            f'<ellipse cx="-30" cy="-16" rx="50" ry="18" fill="#ffe08a" opacity=".8"/><circle cx="140" cy="10" r="14" fill="#ffb81f" stroke="#a8640a" stroke-width="7"/><circle cx="-176" cy="14" r="11" fill="#ffb81f" stroke="#a8640a" stroke-width="7"/>'
            f'<g id="{pid}-seed"><ellipse cx="30" cy="-22" rx="26" ry="38" fill="#8a5a2c" stroke="#4a2c10" stroke-width="8" transform="rotate(24 30 -22)"/><ellipse cx="22" cy="-30" rx="7" ry="14" fill="#c08a52" transform="rotate(24 22 -30)"/></g></g>')


def seed(pid): return f'<g id="{pid}"><ellipse cx="0" cy="0" rx="26" ry="38" fill="#8a5a2c" stroke="#4a2c10" stroke-width="8" transform="rotate(24)"/><ellipse cx="-8" cy="-8" rx="7" ry="14" fill="#c08a52" transform="rotate(24 -8 -8)"/></g>'


def sprout(pid):
    return (f'<g id="{pid}"><ellipse cx="0" cy="0" rx="90" ry="26" fill="#9a6a3a" stroke="#5a3a1a" stroke-width="8"/><path d="M0 -4 q-6 -50 4 -96" stroke="#3f9e5c" stroke-width="12" fill="none" stroke-linecap="round"/>'
            f'<path d="M4 -96 q-60 -40 -84 10 q50 24 84 -10Z" fill="#57c078" stroke="#2f8a4c" stroke-width="7" stroke-linejoin="round"/><path d="M4 -96 q50 -50 86 -6 q-44 30 -86 6Z" fill="#6fd08a" stroke="#2f8a4c" stroke-width="7" stroke-linejoin="round"/></g>')


def heart(pid, col="#ff6f91"): return f'<g id="{pid}"><path d="M0 30 C-70 -20 -50 -80 0 -44 C50 -80 70 -20 0 30Z" fill="{col}" stroke="#b8324f" stroke-width="7" stroke-linejoin="round"/><ellipse cx="-20" cy="-36" rx="10" ry="7" fill="#fff" opacity=".6"/></g>'


def balloon(pid, col="#ff7aa2"):
    return f'<g id="{pid}"><path d="M0 0 q-16 60 6 150" stroke="#8a7a6a" stroke-width="5" fill="none"/><ellipse cx="0" cy="-70" rx="56" ry="70" fill="{col}" stroke="{INK}" stroke-width="7"/><ellipse cx="-18" cy="-96" rx="12" ry="20" fill="#fff" opacity=".5"/><path d="M-10 -2 l20 0 l-10 -12Z" fill="{col}" stroke="{INK}" stroke-width="5"/></g>'


def water_front(pid, w=2920, col="#5fb8ea"):
    """A sheet of water in front of an animal that wades (the river covers its legs)."""
    top = "M-1460 0 " + " ".join(f"q60 -22 120 0 q60 22 120 0" for _ in range(13))
    return f'<g id="{pid}"><path d="{top} L1660 400 L-1460 400Z" fill="{col}" opacity=".93"/><path d="{top}" stroke="#bfe6fb" stroke-width="10" fill="none" opacity=".9"/></g>'


def spray(pid):
    return f'<g id="{pid}">' + "".join(f'<path d="M0 0 Q{60 + k * 26} {-150 - k * 6} {150 + k * 46} {-20 + k * 30}" stroke="#7fd0f5" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="26 22"/>' for k in range(4)) + '</g>'


def bubble_thought(pid, inner="", tail=-1):
    """A thought bubble; tail = -1: the little circles lead down to the left, 1: down to the right (towards the one who thinks)."""
    return (f'<g id="{pid}"><circle cx="{150 * tail}" cy="150" r="16" fill="#fff" stroke="{INK}" stroke-width="7"/><circle cx="{110 * tail}" cy="110" r="26" fill="#fff" stroke="{INK}" stroke-width="7"/>'
            f'<ellipse cx="0" cy="0" rx="170" ry="130" fill="#fff" stroke="{INK}" stroke-width="8"/>{inner}</g>')


def map_board(pid):
    """The trip on one picture: zoo gate, river, jungle tree, sandy hill."""
    stop = lambda x, y, col, ic: f'<g transform="translate({x} {y})"><circle r="92" fill="{col}" stroke="{INK}" stroke-width="9"/>{ic}</g>'
    gate = f'<path d="M-44 40 V-20 Q0 -66 44 -20 V40" stroke="{art.MILO_BLUE}" stroke-width="18" fill="none" stroke-linecap="round"/>'
    riv = '<path d="M-56 -10 q28 -22 56 0 q28 22 56 0 M-56 26 q28 -22 56 0 q28 22 56 0" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round"/>'
    tree = '<rect x="-10" y="-6" width="20" height="56" fill="#8a6238"/><circle cx="0" cy="-24" r="42" fill="#3f9e5c"/><circle cx="14" cy="-30" r="12" fill="#ffb81f"/>'
    hill = '<path d="M-66 40 Q-10 -60 66 40Z" fill="#eaae62" stroke="#a8743a" stroke-width="8" stroke-linejoin="round"/>'
    path = '<path d="M-600 0 H600" stroke="#c9a05a" stroke-width="16" stroke-dasharray="6 34" stroke-linecap="round" fill="none"/>'
    return f'<g id="{pid}">{path}<g id="{pid}-a">{stop(-600, 0, "#bfe6ff", gate)}</g><g id="{pid}-b">{stop(-200, 0, "#5fb8ea", riv)}</g><g id="{pid}-c">{stop(200, 0, "#bff0d4", tree)}</g><g id="{pid}-d">{stop(600, 0, "#ffe2a8", hill)}</g></g>'


def snorkel_board(pid):
    """An elephant in deep water, seen from the side: only the tip of the trunk is above the water (WWF: the trunk "can be used as a snorkel when an elephant wades in deep water")."""
    wave = "M-700 0 " + " ".join("q50 -24 100 0 q50 24 100 0" for _ in range(7))
    return (f'<g id="{pid}"><rect x="-700" y="0" width="1400" height="470" rx="30" fill="#bfe6fb"/>'
            f'<g transform="translate(-80 440) scale(.6)" id="{pid}-ele">{elephant(pid + "e", calf=True)}</g>'
            f'<path d="{wave} L700 440 Q700 470 670 470 L-670 470 Q-700 470 -700 440Z" fill="#3fa3e0" opacity=".5"/><path d="{wave}" stroke="#2f8fd0" stroke-width="12" fill="none" stroke-linecap="round"/></g>')
