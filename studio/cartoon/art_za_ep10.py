"""Pictures for za_ep10 "Can Poppy Slide Down the Snowy Hill?" (Nov 20 2026). New places, props and slide poses only: no character, place or
older prop is drawn differently (the new poses wrap the existing rigs).

Places:
  "snowhill"   the big snowy hill, side view: a flat top on the left (y 440), a long slope down to the flat snow on the right (y 935).
               hill_y(x) gives the snow line, SLOPE the angle of the slope in degrees.
  "hilltop"    on the top of the hill: the flat top in front (y 900) ends at an edge on the right; far below, the snowy plain and the sea ice.
  "hillmid"    the little ledge in the middle of the hill: flat snow (y 920) on the left, the hill going on down to the right, the big top behind.
  "snowbottom" the bottom of the hill: flat snow (y 935) on the right, the hill rising up to the left.
  "arctic_eve" the Arctic shore in the evening: pink and gold sky, the same ice and water as art2's "arctic".
Kinds (registered into art2.RIGS, kit.PT, kit.BOX):
  "bear_slide"   Poppy on her tummy, legs stretched out, tilted to the slope (head down the hill).
  "tumble_slide" Tumble on his tummy, legs stretched out, tilted to the slope.
  "bear_belly"   Poppy on her tummy on flat snow (not tilted).
Props:
  paw_wide(p)  a big polar bear paw print, with arrows out to both sides (wide paws spread the weight). Anchored at its middle.
  paw_pad(p)   the underside of a paw: a big pad with many tiny bumps, fur round it; a magnifier ring. Anchored at its middle.
  spray(p)     a puff of snow behind a slider. Anchored at its middle.
  snowflake(p) a small snowflake. Anchored at its middle.
"""
import math, random, re
import art, art2, kit

INK = art.INK
TOP_Y, BOT_Y, X0, X1 = 440, 935, 600, 1720           # snowhill: the top edge at (X0, TOP_Y), the foot of the slope at (X1, BOT_Y)
SLOPE = math.degrees(math.atan2(BOT_Y - TOP_Y, X1 - X0))     # about 23.8 degrees


def hill_y(x):
    """The snow line of "snowhill" at x (where feet stand)."""
    if x <= X0: return TOP_Y
    if x >= X1: return BOT_Y
    return round(TOP_Y + (x - X0) * (BOT_Y - TOP_Y) / (X1 - X0))


SNOW, SNOW_SH, SNOW_LN = "#ffffff", "#dcecfb", "#b9d6ef"


def _snowsky(p, a="#a9dcff", b="#eef9ff"):
    return art._sky(p, a, b)


def _peaks(y, col="#dcefff", hi="#ffffff", r=7):
    rr = random.Random(r); x = -560; pts = []
    while x < 2480:
        pts.append((x, y - rr.uniform(120, 300))); x += rr.uniform(260, 420); pts.append((x, y - rr.uniform(10, 60))); x += rr.uniform(160, 260)
    d = f"M-560 {y} " + " ".join(f"L{px:.0f} {py:.0f}" for px, py in pts) + f" L2480 {y}Z"
    caps = "".join(f'<path d="M{px:.0f} {py:.0f} l60 46 l-40 10 l-30 -14 l-36 16 l-20 -10Z" fill="{hi}"/>' for px, py in pts[::2])
    return f'<path d="{d}" fill="{col}"/>{caps}'


def _sparkles(xs, col="#ffffff"):
    return "".join(f'<path d="M{x} {y} l6 -16 l6 16 l16 6 l-16 6 l-6 16 l-6 -16 l-16 -6Z" fill="{col}" opacity=".9"/>' for x, y in xs)


def _drift(x, y, w, h=40):
    return f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{h}" fill="{SNOW}"/><path d="M{x - w * .7:.0f} {y - h * .3:.0f} q{w * .7:.0f} {-h * .8:.0f} {w * 1.4:.0f} 0" stroke="{SNOW_SH}" stroke-width="8" fill="none" stroke-linecap="round"/>'


def _ice_block(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-60 0 L-50 -90 L40 -100 L64 0Z" fill="#cfeaff" stroke="#9cc8ea" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M-36 -70 L10 -78" stroke="#fff" stroke-width="9" stroke-linecap="round"/></g>')


# ------------------------------------------------------------------ places
def bg_snowhill(p):
    far = _snowsky(p) + art._sun(p + "sun", 1560, 200, 70, "#fff7c9") + art._cloud(p + "c1", 900, 150, .8) + _peaks(640) + \
        '<rect x="-500" y="630" width="2920" height="120" fill="#cfe7fb"/>'
    mid = _peaks(760, "#e6f3ff", "#ffffff", 11)
    hill = f"M-500 {TOP_Y} L{X0 - 60} {TOP_Y} Q{X0} {TOP_Y} {X0 + 50} {hill_y(X0 + 50)} L{X1 - 60} {hill_y(X1 - 60)} Q{X1} {BOT_Y} {X1 + 80} {BOT_Y} L2420 {BOT_Y} L2420 1980 L-500 1980Z"
    lines = "".join(f'<path d="M{x} {hill_y(x) + 60} l200 {round(200 * math.tan(math.radians(SLOPE)))}" stroke="{SNOW_SH}" stroke-width="10" stroke-linecap="round" opacity=".8"/>' for x in (520, 900, 1260))
    near = (f'<path d="{hill}" fill="{SNOW_LN}" transform="translate(0 -10)"/><path d="{hill}" fill="{SNOW}"/>{lines}'
            f'<path d="M-500 {TOP_Y + 30} L{X0 - 40} {TOP_Y + 30}" stroke="{SNOW_SH}" stroke-width="12" stroke-linecap="round"/>'
            + _drift(1820, BOT_Y + 40, 120, 30) + _drift(160, TOP_Y + 120, 90, 26) + _ice_block(1900, BOT_Y + 10, .9)
            + _sparkles(((260, TOP_Y + 200), (700, 760), (1100, 900), (1500, 1000), (1760, 1040), (400, 980))))
    return far, mid, near


def bg_hilltop(p):
    far = _snowsky(p, "#9fd6ff", "#f0faff") + art._sun(p + "sun", 360, 190, 64, "#fff7c9") + art._cloud(p + "c1", 1300, 130, .9) + \
        '<rect x="-500" y="560" width="2920" height="400" fill="#dcefff"/><path d="M-500 560 L2420 560" stroke="#bfe0f8" stroke-width="10"/>' + \
        '<rect x="-500" y="600" width="2920" height="40" fill="#8ccff0" opacity=".7"/>' + \
        "".join(f'<path d="M{x} {y} q30 -14 64 -4 q34 -12 66 4 l-8 20 l-116 0Z" fill="#fff"/>' for x, y in ((200, 620), (980, 612), (1640, 624)))
    mid = ('<path d="M1180 900 Q1300 900 1360 940 L2420 1500 L2420 700 L1500 700Z" fill="#eaf5ff"/>'
           + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="10" fill="#cfe5f8"/>' for x, y, w in ((1500, 760, 70), (1800, 800, 90), (1640, 690, 50))))
    near = (f'<path d="M-500 880 L1180 880 Q1290 880 1330 930 L1420 1980 L-500 1980Z" fill="{SNOW_LN}" transform="translate(0 -10)"/>'
            f'<path d="M-500 880 L1180 880 Q1290 880 1330 930 L1420 1980 L-500 1980Z" fill="{SNOW}"/>'
            + _drift(120, 960, 140, 30) + _drift(820, 1020, 110, 24) + _sparkles(((400, 1000), (1000, 960), (1240, 1040), (600, 1050))))
    return far, mid, near


def bg_hillmid(p):
    far = _snowsky(p) + art._cloud(p + "c1", 1500, 170, .9) + _peaks(700, "#e3f1ff", "#fff", 5)
    big = f'<path d="M-500 260 L-200 230 Q-100 228 0 280 L1100 900 L-500 900Z" fill="{SNOW_SH}"/><path d="M-500 290 L-210 262 Q-110 260 -10 310 L1060 900 L-500 900Z" fill="#eef7ff"/>'
    mid = big + '<path d="M140 470 l180 100 M420 640 l160 90" stroke="#d6e8f8" stroke-width="10" stroke-linecap="round"/>'
    g = "M-500 920 L1180 920 Q1280 920 1340 960 L2420 1600 L2420 1980 L-500 1980Z"
    near = (f'<path d="{g}" fill="{SNOW_LN}" transform="translate(0 -10)"/><path d="{g}" fill="{SNOW}"/>'
            + _drift(260, 1000, 120, 26) + _drift(1500, 1180, 90, 22) + _sparkles(((500, 1010), (900, 1060), (1600, 1250), (180, 1080))))
    return far, mid, near


def bg_snowbottom(p):
    far = _snowsky(p, "#b2e0ff", "#f4fbff") + art._sun(p + "sun", 1640, 220, 70, "#fff7c9") + art._cloud(p + "c1", 1180, 140, .8) + _peaks(700, "#e3f1ff", "#fff", 3)
    rise = f'<path d="M-500 160 L-300 150 Q-200 152 -120 200 L1000 935 L-500 935Z" fill="{SNOW_SH}"/><path d="M-500 190 L-310 180 Q-210 182 -130 230 L960 935 L-500 935Z" fill="#f4faff"/>'
    mid = rise + '<path d="M100 420 l200 130 M380 640 l180 118" stroke="#d6e8f8" stroke-width="10" stroke-linecap="round"/>'
    near = (f'<path d="M-500 935 L2420 935 L2420 1980 L-500 1980Z" fill="{SNOW_LN}" transform="translate(0 -10)"/><path d="M-500 935 L2420 935 L2420 1980 L-500 1980Z" fill="{SNOW}"/>'
            + _drift(1840, 990, 140, 32) + _ice_block(1960, 960, 1.0) + _drift(200, 1040, 120, 26) + _sparkles(((700, 1020), (1200, 1060), (1600, 1010), (420, 1080))))
    return far, mid, near


def bg_arctic_eve(p):
    far, mid, near = art2.bg_arctic(p)
    far = far.replace(art._sky(p, "#bfe6ff", "#f2fbff"), art._sky(p, "#f7a8c4", "#ffe2b0"))
    far = far.replace('fill="#dcefff"', 'fill="#f2d6e8"')
    return far, mid, near


art.BG.update({"snowhill": bg_snowhill, "hilltop": bg_hilltop, "hillmid": bg_hillmid, "snowbottom": bg_snowbottom, "arctic_eve": bg_arctic_eve})
art.PLACE.update({"snowhill": "the big snowy hill", "hilltop": "the top of the snowy hill", "hillmid": "the little ledge in the middle of the hill",
                  "snowbottom": "the bottom of the snowy hill", "arctic_eve": "the Arctic shore in the evening"})


# ------------------------------------------------------------------ slide poses (wrap the existing rigs: the drawing is the same, the legs stretch out)
def _stretch(svg, pid, legs, ang):
    for name, (ox, oy) in legs.items():
        a = -ang if name.startswith("f") else ang
        svg = svg.replace(f'<g id="{pid}-{name}">', f'<g id="{pid}-{name}" transform="rotate({a} {ox} {oy})">', 1)
    return svg


def bear_belly(pid, tilt=0.0):
    legs = {"fl": (140, -150), "fl2": (96, -150), "bl": (-106, -150), "bl2": (-150, -150)}
    return f'<g transform="rotate({tilt:.1f}) translate(0 78)">' + _stretch(art2.bear(pid), pid, legs, 72) + '</g>'


def tumble_belly(pid, tilt=0.0):
    legs = {"fl": (150, -250), "fl2": (96, -250), "bl": (-140, -250), "bl2": (-196, -250)}
    return f'<g transform="rotate({tilt:.1f}) translate(0 120)">' + _stretch(art2.elephant(pid, calf=True), pid, legs, 72) + '</g>'


art2.RIGS["bear_slide"] = dict(art2.RIGS["bear"], build=lambda p: bear_belly(p, SLOPE), legs=None)
art2.RIGS["bear_belly"] = dict(art2.RIGS["bear"], build=lambda p: bear_belly(p, 0), legs=None)
art2.RIGS["tumble_slide"] = dict(art2.RIGS["tumble"], build=lambda p: tumble_belly(p, SLOPE), legs=None)

# where the parts of a polar bear cub are (art2.bear: head circle at (214, -306), muzzle to x 370, ear tops at y -440)
kit.PT["bear"] = {"head": (240, -300), "eye": (246, -330), "body": (-10, -212), "top": (214, -440), "paw": (140, -20), "feet": (0, 0), "all": (60, -230)}
kit.BOX["bear"] = (-250, 380, -450)
_c, _s = math.cos(math.radians(SLOPE)), math.sin(math.radians(SLOPE))
_rot = lambda x, y: (round(x * _c - (y + 78) * _s), round(x * _s + (y + 78) * _c))
kit.PT["bear_slide"] = {k: _rot(*v) for k, v in kit.PT["bear"].items()}
kit.PT["bear_belly"] = {k: (v[0], v[1] + 78) for k, v in kit.PT["bear"].items()}
kit.BOX["bear_slide"] = (-280, 420, -330); kit.BOX["bear_belly"] = (-260, 420, -380)
_rt = lambda x, y: (round(x * _c - (y + 120) * _s), round(x * _s + (y + 120) * _c))
kit.PT["tumble_slide"] = {k: _rt(*v) for k, v in kit.PT["tumble"].items()}
kit.BOX["tumble_slide"] = (-360, 640, -560)


# ------------------------------------------------------------------ props
def paw_wide(p):
    """A big polar bear paw print (a wide pad and five toes), with an arrow out to each side."""
    toes = "".join(f'<ellipse cx="{x}" cy="{y}" rx="40" ry="48" fill="#5a6f8a"/>' for x, y in ((-150, -120), (-78, -170), (0, -186), (78, -170), (150, -120)))
    pad = '<path d="M-190 -40 C-200 -110 -100 -120 0 -116 C100 -120 200 -110 190 -40 C180 40 100 90 0 90 C-100 90 -180 40 -190 -40Z" fill="#5a6f8a"/>'
    arr = lambda d: (f'<path d="M{d * 240} -20 L{d * 380} -20" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M{d * 240} -20 L{d * 380} -20" stroke="#ff8a3d" stroke-width="16" stroke-linecap="round"/>'
                     f'<path d="M{d * 350} -60 L{d * 410} -20 L{d * 350} 20Z" fill="#ff8a3d" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    return f'<g id="{p}"><ellipse cx="0" cy="-30" rx="250" ry="200" fill="#ffffff" opacity=".7"/>{pad}{toes}<g id="{p}-arr">{arr(1)}{arr(-1)}</g></g>'


def paw_pad(p):
    """The underside of a paw seen close: a big dark pad covered in tiny bumps, white fur all round, inside a magnifier."""
    r = random.Random(21)
    bumps = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(7, 11):.0f}" fill="#6f7f96"/><circle cx="{x - 3:.0f}" cy="{y - 3:.0f}" r="3" fill="#a9b6c8"/>'
                    for x, y in [(r.uniform(-120, 120), r.uniform(-70, 80)) for _ in range(120)] if (x / 135) ** 2 + (y / 95) ** 2 < 1)
    fur = "".join(f'<path d="M{170 * math.cos(a):.0f} {130 * math.sin(a):.0f} l{40 * math.cos(a):.0f} {40 * math.sin(a):.0f}" stroke="#ffffff" stroke-width="16" stroke-linecap="round"/>'
                  for a in [k * math.pi / 14 for k in range(28)])
    return (f'<g id="{p}"><circle r="250" fill="#eaf6ff"/>{fur}<ellipse rx="160" ry="118" fill="#fdfaf2" stroke="#d8cfc0" stroke-width="10"/>'
            f'<ellipse rx="140" ry="100" fill="#3f4c5f"/><g id="{p}-bumps">{bumps}</g>'
            f'<circle r="250" fill="none" stroke="{INK}" stroke-width="34"/><circle r="250" fill="none" stroke="#9fd0ff" stroke-width="18"/>'
            f'<path d="M176 176 L300 300" stroke="{INK}" stroke-width="64" stroke-linecap="round"/><path d="M176 176 L300 300" stroke="#c98a4a" stroke-width="40" stroke-linecap="round"/></g>')


def spray(p):
    return f'<g id="{p}">' + "".join(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="#ffffff" stroke="{SNOW_LN}" stroke-width="6"/>' for x, y, rr in ((0, 0, 40), (-50, -30, 30), (-90, 10, 24), (-30, -70, 20), (40, -40, 22))) + '</g>'


def snowflake(p, col="#ffffff"):
    arms = "".join(f'<path d="M0 0 L{40 * math.cos(k * math.pi / 3):.0f} {40 * math.sin(k * math.pi / 3):.0f}" stroke="{col}" stroke-width="9" stroke-linecap="round"/>' for k in range(6))
    return f'<g id="{p}">{arms}<circle r="9" fill="{col}"/></g>'
