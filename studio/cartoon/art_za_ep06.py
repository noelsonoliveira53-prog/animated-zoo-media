"""Art for za_ep06 "The Rainy Day Umbrella" (Nov 19 2026): Puff the little white bat (a new rig, "bat", and "bat_hang" hanging upside down),
the giant leaf the friends carry as an umbrella, the small things that are too small (a flower hat, a mossy log and a moss hat), a leaf tent
with little bats inside, the rain with a dry place under the leaf, a rain cup for the fact board, a rainbow, and Mango's tree house.
Same hand as art.py / art2.py: flat fills, one warm dark outline, big brown eyes, pink cheeks. Nothing here changes an existing character, prop or place.
Read only: art3.leaf (the small leaf), art_za_ep03 rain / tint / cloud / drop (the rain props)."""
import art, art2, art3, kit
from art import INK, SUN, eye
import art_za_ep03 as A3

WATER, WATER_L, WATER_D = A3.WATER, A3.WATER_L, A3.WATER_D
BAT = {"fur": "#fbf8f2", "shade": "#e6dfd2", "line": "#6a5a4a", "wing": "#b9b1a6", "wing_d": "#8f877c", "ear": "#ffd36b", "nose": "#ffc94a"}
LEAF = ("#3fa85a", "#1f6a3a", "#7fd08a")        # the giant leaf: fill, line, light


# ------------------------------------------------------------------ Puff the little bat (front view, feet on y = 0)
def bat(pid, c=BAT, hang=False):
    """Puff: a round white fluffy bat, big ears, a little yellow nose, gray wings. Parts: -wl -wr (wings, flap round the shoulders),
    -eyeL -eyeR, -jaw, -smile / -frown. hang=True: upside down, her toes holding on at (0, 0), the body below."""
    ln = c["line"]
    fluff = "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((-62, -70, 30), (62, -70, 30), (-70, -120, 30), (70, -120, 30), (-52, -170, 30), (52, -170, 30), (0, -40, 34)))
    body_sh = '<ellipse cx="0" cy="-110" rx="78" ry="82"/>' + fluff
    head_sh = '<circle cx="0" cy="-206" r="64"/>'
    ears = "".join(f'<path d="M{s * 22} -250 L{s * 66} -330 L{s * 64} -222Z"/>' for s in (-1, 1))
    ears_in = "".join(f'<path d="M{s * 32} -250 L{s * 60} -306 L{s * 58} -232Z" fill="{c["ear"]}"/>' for s in (-1, 1))
    wing = lambda s: (f'<g id="{pid}-w{"lr"[s > 0]}"><path d="M{s * 60} -150 L{s * 190} -200 L{s * 176} -150 L{s * 210} -120 L{s * 170} -96 L{s * 190} -60 L{s * 66} -90Z" '
                      f'fill="{c["wing"]}" stroke="{ln}" stroke-width="8" stroke-linejoin="round"/>'
                      f'<path d="M{s * 70} -140 L{s * 176} -150 M{s * 70} -120 L{s * 170} -96 M{s * 72} -104 L{s * 190} -60" stroke="{c["wing_d"]}" stroke-width="6" fill="none" stroke-linecap="round"/></g>')
    feet = f'<path d="M-24 -30 v26 M24 -30 v26" stroke="{ln}" stroke-width="12" stroke-linecap="round"/>'
    face = (eye(f"{pid}-eyeL", -24, -214, 20, lid=c["fur"]) + eye(f"{pid}-eyeR", 24, -214, 20, lid=c["fur"])
            + f'<ellipse cx="-44" cy="-184" rx="12" ry="8" fill="#ff9ab8" opacity=".75"/><ellipse cx="44" cy="-184" rx="12" ry="8" fill="#ff9ab8" opacity=".75"/>'
            + f'<path d="M-14 -192 L14 -192 L0 -176Z" fill="{c["nose"]}" stroke="{ln}" stroke-width="5" stroke-linejoin="round"/>'
            + f'<g id="{pid}-jaw" opacity="0"><path d="M-12 -168 Q0 -146 12 -168Z" fill="#8a2f3f" stroke="{ln}" stroke-width="4"/></g>'
            + f'<g id="{pid}-smile"><path d="M-16 -168 Q0 -154 16 -168" stroke="{ln}" stroke-width="5" fill="none" stroke-linecap="round"/></g>'
            + f'<g id="{pid}-frown" opacity="0"><path d="M-14 -160 Q0 -172 14 -160" stroke="{ln}" stroke-width="5" fill="none" stroke-linecap="round"/></g>')
    inner = (wing(-1) + wing(1) + feet + art2._ol(body_sh + head_sh + ears, ln, 7)
             + f'<g fill="{c["fur"]}">{body_sh}{head_sh}{ears}</g>{ears_in}'
             + f'<ellipse cx="0" cy="-96" rx="44" ry="50" fill="{c["shade"]}" opacity=".6"/><ellipse cx="-22" cy="-240" rx="20" ry="9" fill="#fff" opacity=".8"/>' + face)
    if hang:
        return f'<g id="{pid}"><g id="{pid}-swing"><g id="{pid}-body" transform="rotate(180)">{inner}</g></g></g>'
    sh = '<ellipse cx="0" cy="4" rx="70" ry="10" fill="#000" opacity=".12"/>'
    return f'<g id="{pid}">{sh}<g id="{pid}-body">{inner}</g></g>'


art2.RIGS["bat"] = dict(build=lambda p: bat(p), neck=None, tail=None, ear=None, legs=None, hip=0, jaw=("y", 6), eyes=["eyeL", "eyeR"], brows=[])
art2.RIGS["bat_hang"] = dict(build=lambda p: bat(p, hang=True), neck=None, tail=None, ear=None, legs=None, hip=0, jaw=("y", 6), eyes=["eyeL", "eyeR"], brows=[])
kit.PT["bat"] = {"head": (0, -206), "body": (0, -110), "top": (0, -330), "feet": (0, 0), "all": (0, -160)}
kit.PT["bat_hang"] = {"head": (0, 206), "body": (0, 110), "top": (0, 0), "feet": (0, 330), "all": (0, 160)}
kit.BOX["bat"] = (-215, 215, -335)
kit.BOX["bat_hang"] = (-215, 215, 0)


# ------------------------------------------------------------------ the rain
def rain_dry(pid, holes=(), w=3400, h=2200):
    """Rain over the whole picture except inside `holes` (polygons in the PICTURE's coordinates, given for a prop placed at (-500, -700)):
    the dry place under the giant leaf. The streaks move inside #<pid>-mv (move it 220 down and 60 left to loop); the holes stay put."""
    hole = "".join("M" + " L".join(f"{x + 500} {y + 700}" for x, y in poly) + "Z" for poly in holes)
    streaks = A3.rain(pid + "r", w, h + 300).replace(f'<g id="{pid}r">', f'<g id="{pid}-mv" transform="translate(0 -300)">', 1)
    # a mask, not a clip: #<pid>-hole can be moved (x) when the friends walk with the leaf
    return (f'<g id="{pid}"><mask id="{pid}-m" maskUnits="userSpaceOnUse" x="-200" y="-200" width="{w + 400}" height="{h + 400}">'
            f'<rect x="-200" y="-200" width="{w + 400}" height="{h + 400}" fill="#fff"/><g id="{pid}-hole"><path d="{hole or "M0 0Z"}" fill="#000"/></g></mask>'
            f'<g mask="url(#{pid}-m)">{streaks}</g></g>')


def drip(pid, s=.22):
    """One small drop (art_za_ep03.drop, smaller)."""
    return A3.drop(pid, s)


def shake(pid):
    """Little drops flying off a bird who shakes himself dry: eight drops in a ring."""
    import math
    out = ""
    for k in range(8):
        a = math.radians(k * 45 + 10); x, y = math.cos(a) * 170, math.sin(a) * 150
        out += f'<g transform="translate({x:.0f} {y:.0f}) rotate({k * 45 + 100})">{A3.drop(pid + str(k), .16)}</g>'
    return f'<g id="{pid}">{out}</g>'


# ------------------------------------------------------------------ the things that are too small
def small_leaf(pid):
    """A small round leaf, like a little hat (art3.leaf)."""
    return art3.leaf(pid)


def flower_hat(pid):
    """A big pink flower turned upside down, like a hat: its stem points up. (0, 0) is the middle of its rim."""
    petals = "".join(f'<ellipse cx="{x}" cy="{y}" rx="62" ry="40" transform="rotate({r} {x} {y})" fill="{c}" stroke="#a83a6a" stroke-width="7"/>'
                     for x, y, r, c in ((-110, -10, 20, "#ff8fc0"), (110, -10, -20, "#ff8fc0"), (-56, -30, 10, "#ffb0d4"), (56, -30, -10, "#ffb0d4"), (0, -40, 0, "#ff8fc0")))
    cup = '<path d="M-90 -40 Q0 -170 90 -40Z" fill="#ff6fa8" stroke="#a83a6a" stroke-width="8" stroke-linejoin="round"/>'
    stem = '<path d="M0 -130 q10 -60 -6 -110" stroke="#3f9e5c" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M-4 -200 c40 -30 70 -10 70 10 c-30 6 -50 4 -70 -10Z" fill="#57c078" stroke="#2f7a3a" stroke-width="5"/>'
    return f'<g id="{pid}">{stem}{cup}{petals}</g>'


def flower_plant(pid):
    """A tall flower plant with three big pink flowers, standing in the meadow. (0, 0) is where it grows from the ground."""
    fl = lambda x, y, s: (f'<g transform="translate({x} {y}) scale({s})">' + "".join(f'<ellipse cx="{dx}" cy="{dy}" rx="52" ry="34" transform="rotate({r} {dx} {dy})" fill="#ff8fc0" stroke="#a83a6a" stroke-width="7"/>'
                                                                         for dx, dy, r in ((-56, 0, 0), (56, 0, 0), (0, -46, 90), (0, 46, 90), (-40, -34, 45), (40, 34, 45), (40, -34, -45), (-40, 34, -45)))
                          + '<circle r="30" fill="#ffd23f" stroke="#c98a10" stroke-width="7"/></g>')
    stems = "".join(f'<path d="M0 0 Q{dx * .3:.0f} {dy * .5:.0f} {dx} {dy}" stroke="#3f9e5c" stroke-width="14" fill="none" stroke-linecap="round"/>' for dx, dy in ((-120, -330), (20, -420), (140, -300)))
    leaves = art2._leaf(0, -120, .9, -150, "#3f9e5c") + art2._leaf(0, -160, .8, -30, "#57c078")
    return f'<g id="{pid}">{stems}{leaves}{fl(-120, -330, 1)}{fl(20, -420, 1.1)}{fl(140, -300, .9)}</g>'


def mossy_log(pid):
    """A fallen log by the stream with soft green moss on top. (0, 0) is the middle of its bottom; about 620 wide."""
    moss = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in ((-220, -150, 46, "#6cc463"), (-140, -170, 54, "#57b04f"), (-50, -176, 50, "#6cc463"), (40, -172, 56, "#57b04f"),
                                                                                      (130, -166, 48, "#6cc463"), (210, -150, 44, "#57b04f")))
    return (f'<g id="{pid}"><rect x="-300" y="-150" width="600" height="150" rx="70" fill="#9a6a3c" stroke="{INK}" stroke-width="9"/>'
            f'<ellipse cx="290" cy="-75" rx="44" ry="74" fill="#c99a62" stroke="{INK}" stroke-width="9"/><ellipse cx="290" cy="-75" rx="22" ry="40" fill="none" stroke="#9a6a3c" stroke-width="7"/>'
            f'<path d="M-240 -90 h160 M-60 -60 h200" stroke="#7a5030" stroke-width="8" stroke-linecap="round"/>{moss}</g>')


def moss_hat(pid):
    """A little hat of moss: a soft green bump. (0, 0) is the middle of its rim; about 230 wide."""
    return (f'<g id="{pid}"><path d="M-115 0 C-120 -90 -60 -130 0 -130 C60 -130 120 -90 115 0Z" fill="#57b04f" stroke="#2f7a3a" stroke-width="8" stroke-linejoin="round"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#6cc463"/>' for x, y, r in ((-60, -60, 26), (0, -90, 30), (60, -56, 24), (-20, -30, 20), (40, -24, 18)))
            + '</g>')


# ------------------------------------------------------------------ leaves that are big enough
def leaf_tent(pid, n=3):
    """A big leaf folded down like a tent (cut and folded by little bats), hanging under a branch, with n little white bats hanging inside.
    (0, 0) is where the leaf's stem meets the branch; the tent is about 520 wide and 300 tall."""
    # the bats hang inside, under the fold: drawn BEFORE the leaf, so only their heads peek out below its edge (they hang upside down)
    bats = "".join(f'<g transform="translate({x} {y}) scale(.32)">{bat(pid + "b" + str(k), hang=True)}</g>' for k, (x, y) in enumerate(((-84, 196), (0, 214), (84, 196))[:n]))
    leaf = (f'<path d="M0 0 C-80 10 -230 60 -260 250 C-150 220 -60 236 0 280 C60 236 150 220 260 250 C230 60 80 10 0 0Z" fill="{LEAF[0]}" stroke="{LEAF[1]}" stroke-width="9" stroke-linejoin="round"/>'
            f'<path d="M0 0 L0 270" stroke="{LEAF[1]}" stroke-width="8"/>'
            + "".join(f'<path d="M0 {y} q{s * 60} 20 {s * 150} {60 + y * .3:.0f}" stroke="{LEAF[1]}" stroke-width="5" fill="none" opacity=".7"/>' for y in (60, 120, 180) for s in (-1, 1))
            + f'<path d="M-30 30 C-100 60 -170 110 -200 190" stroke="{LEAF[2]}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".7"/>')
    # the inside under the tent is darker, so the bats show
    inside = '<path d="M-150 250 C-100 150 100 150 150 250 C80 236 -80 236 -150 250Z" fill="#1f5a32"/>'
    return f'<g id="{pid}"><path d="M0 0 v-30" stroke="{LEAF[1]}" stroke-width="12"/>{inside}{bats}{leaf}</g>'


def giant_leaf(pid, w=1150):
    """The giant leaf held up like an umbrella: a wide green dome, its stem hanging from the middle. (0, 0) is the bottom of the stem;
    the dome's rim is 260 above it and `w` wide. #<pid>-dome is the leaf itself (it can tilt)."""
    h = w / 2
    dome = (f'<path d="M{-h} -250 C{-h * .8} -470 {h * .8} -470 {h} -250 C{h * .5} -290 {h * .2} -270 0 -300 C{-h * .2} -270 {-h * .5} -290 {-h} -250Z" '
            f'fill="{LEAF[0]}" stroke="{LEAF[1]}" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M0 -300 L0 -420" stroke="{LEAF[1]}" stroke-width="10" stroke-linecap="round"/>'
            + "".join(f'<path d="M0 {-300 - k * 30} Q{s * h * .4:.0f} {-340 - k * 30} {s * h * (.95 - k * .12):.0f} {-280 - k * 6}" stroke="{LEAF[1]}" stroke-width="7" fill="none" opacity=".7"/>' for k in range(3) for s in (-1, 1))
            + f'<path d="M{-h * .7:.0f} -330 C{-h * .5:.0f} -410 {-h * .1:.0f} -430 {h * .1:.0f} -428" stroke="{LEAF[2]}" stroke-width="16" fill="none" stroke-linecap="round" opacity=".7"/>')
    stem = f'<path d="M0 0 L0 -300" stroke="{LEAF[1]}" stroke-width="26" stroke-linecap="round"/><path d="M0 0 L0 -300" stroke="#4fae5c" stroke-width="12" stroke-linecap="round"/>'
    return f'<g id="{pid}"><g id="{pid}-dome">{stem}{dome}</g></g>'


def giant_leaf_flat(pid, w=1150):
    """The same giant leaf lying flat on the ground, where it fell: a long green leaf with its stem. (0, 0) is its middle on the ground."""
    h = w / 2
    return (f'<g id="{pid}"><path d="M{-h} 0 C{-h * .6} -110 {h * .6} -110 {h} 0 C{h * .6} 50 {-h * .6} 50 {-h} 0Z" fill="{LEAF[0]}" stroke="{LEAF[1]}" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M{-h + 20} 0 L{h - 20} -6" stroke="{LEAF[1]}" stroke-width="9"/><path d="M{-h} 0 l-160 30" stroke="{LEAF[1]}" stroke-width="22" stroke-linecap="round"/>'
            + "".join(f'<path d="M{x} -2 q50 -40 110 -50 M{x} -2 q50 26 110 30" stroke="{LEAF[1]}" stroke-width="6" fill="none" opacity=".7"/>' for x in range(int(-h * .7), int(h * .6), 140))
            + f'<path d="M{-h * .6:.0f} -50 C{-h * .3:.0f} -86 {h * .3:.0f} -86 {h * .5:.0f} -60" stroke="{LEAF[2]}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".7"/></g>')


# ------------------------------------------------------------------ fact board pictures
def rain_cup(pid):
    """A clear cup that catches rain, with a mark at one inch: #<pid>-lv is the water (scaleY from 0 to 1, from the bottom)."""
    return (f'<g id="{pid}"><rect x="-130" y="-300" width="260" height="300" rx="18" fill="#eaf7ff" stroke="{INK}" stroke-width="10"/>'
            f'<clipPath id="{pid}-c"><rect x="-122" y="-292" width="244" height="284" rx="12"/></clipPath>'
            f'<g clip-path="url(#{pid}-c)"><g id="{pid}-lv"><rect x="-130" y="-120" width="260" height="130" fill="{WATER}"/><path d="M-130 -120 h260" stroke="{WATER_L}" stroke-width="10"/></g></g>'
            f'<path d="M130 -120 h60" stroke="#e63946" stroke-width="10" stroke-linecap="round"/><path d="M-160 -300 h320" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M-90 -270 v220" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity=".7"/></g>')


def tent_board(pid):
    """For the fact board: one leaf, first flat, then cut and folded into a tent (an arrow between)."""
    flat = f'<g transform="translate(-420 0) rotate(-90) scale(.55)">{giant_leaf_flat(pid + "f", 700)}</g>'
    return f'<g id="{pid}">{flat}{art.arrow(pid + "a", -260, 0, -80, 0)}</g>'


def scissors_snips(pid):
    """Little snip marks along a leaf (where the bats bite small cuts)."""
    return f'<g id="{pid}">' + "".join(f'<path d="M{x} {y} l18 -18 M{x} {y - 18} l18 18" stroke="#e63946" stroke-width="7" stroke-linecap="round"/>' for x, y in ((-60, -40), (-20, -50), (20, -50), (60, -40))) + '</g>'


def rainbow(pid):
    """A rainbow arc, about 1600 wide, its feet at y = 0."""
    cols = ("#ff6f6f", "#ffb347", "#ffe066", "#7ed37e", "#6fb8ff", "#a98bff")
    return f'<g id="{pid}" opacity=".85">' + "".join(f'<path d="M{-800 + k * 34} 0 A{800 - k * 34} {640 - k * 30} 0 0 1 {800 - k * 34} 0" stroke="{c}" stroke-width="34" fill="none"/>' for k, c in enumerate(cols)) + '</g>'


def sun_peek(pid):
    """The sun coming out: a sun with rays (#<pid>-r turns)."""
    rays = "".join(f'<path d="M0 -150 v-60" stroke="{SUN}" stroke-width="22" stroke-linecap="round" transform="rotate({k * 30})"/>' for k in range(12))
    return f'<g id="{pid}"><g id="{pid}-r">{rays}</g><circle r="120" fill="#ffe066" stroke="#e8b400" stroke-width="10"/></g>'


# ------------------------------------------------------------------ places
def bg_treehouse(p):
    """Mango's tree house: the green jungle, one big tree on the right with a little wooden house on a platform (floor at y = 330),
    a rope ladder hanging down, the ground below where the friends stand (feet at y = 930). No rain is drawn in the place."""
    far, mid, near = art2.bg_jungle(p)
    trunk = ('<path d="M1420 900 C1400 500 1410 -200 1390 -900 L1640 -900 C1620 -200 1640 500 1680 900Z" fill="#8a6238"/>'
             '<path d="M1580 900 C1550 500 1560 -200 1550 -900 L1640 -900 C1620 -200 1640 500 1680 900Z" fill="#735029" opacity=".7"/>'
             + "".join(f'<path d="M{1450 + (k % 2) * 70} {820 - k * 160} q20 -30 6 -70" stroke="#6a4a26" stroke-width="9" fill="none" stroke-linecap="round"/>' for k in range(6)))
    house = ('<rect x="1060" y="320" width="760" height="40" rx="10" fill="#b07a42" stroke="#402010" stroke-width="9"/>'
             + "".join(f'<path d="M{x} 360 L{x + 30} 430" stroke="#8a5a2c" stroke-width="16" stroke-linecap="round"/>' for x in (1100, 1760))
             + '<rect x="1180" y="120" width="420" height="200" rx="8" fill="#d29a5c" stroke="#402010" stroke-width="9"/>'
             + "".join(f'<path d="M1180 {y} H1600" stroke="#b07a42" stroke-width="7"/>' for y in (170, 220, 270))
             + '<path d="M1140 130 L1390 -30 L1640 130Z" fill="#3fa85a" stroke="#1f6a3a" stroke-width="10" stroke-linejoin="round"/>'
             + '<path d="M1200 120 L1390 0 L1580 120" stroke="#7fd08a" stroke-width="10" fill="none" opacity=".7"/>'
             + '<rect x="1250" y="180" width="110" height="140" rx="50" fill="#7a4a24" stroke="#402010" stroke-width="8"/>'
             + '<rect x="1440" y="170" width="100" height="80" rx="10" fill="#bfe6fb" stroke="#402010" stroke-width="8"/><path d="M1490 170 v80 M1440 210 h100" stroke="#402010" stroke-width="6"/>'
             + '<path d="M1310 -10 q-10 -40 10 -60" stroke="#ff6f91" stroke-width="10" fill="none"/>')
    ladder = ('<path d="M1110 360 C1100 560 1120 700 1110 880 M1190 360 C1180 560 1200 700 1190 880" stroke="#c9a14a" stroke-width="10" fill="none"/>'
              + "".join(f'<path d="M1106 {y} H1194" stroke="#a8743a" stroke-width="12" stroke-linecap="round"/>' for y in range(420, 880, 70)))
    return far, mid + trunk + house + ladder, near


art.BG.update({"treehouse": bg_treehouse})
art.PLACE.update({"treehouse": "Mango's tree house"})


def bg_mossy(p):
    """The little stream again (art_za_ep04.bg_stream: the banks, the water, the vine bridge's posts and rope), with an old log covered in soft
    green moss lying on the left bank, drawn in the near layer so the friends stand in front of it (the log at x 380 to 790, feet line y = 930)."""
    import art_za_ep04 as A4
    far, mid, near = A4.bg_stream(p)
    log = f'<g transform="translate(560 930) scale(.62)">{mossy_log(p + "log")}</g>'
    return far, mid, near + log


art.BG.update({"mossy": bg_mossy})
art.PLACE.update({"mossy": "the mossy log by the stream"})
