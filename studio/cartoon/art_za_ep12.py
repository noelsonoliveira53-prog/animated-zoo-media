"""Pictures for za_ep12 "Can Slow Tula Finish the Big Ocean Race?" (Nov 21 2026). New places, two new fish friends and props only: no existing
character, place or prop is drawn differently (Tula is art2.turtle as it is; this file only tells kit where her parts are).

Places (all under the sea; the two "split" ones show the sky above the water line WL too, so Milo can sit on a rock in the air):
  "sea_start"  split view: the START arch of coral on the left, a little rock island on the right whose top (1560, 256) is above the water.
  "meadow"     the seagrass meadow: tall green seagrass everywhere behind the swimmers.
  "fork"       a rock wall with two openings: a dark one on the left, a bright one on the right.
  "reef"       the coral garden: the right way to the Big Rock.
  "bigrock"    split view: the Big Rock rises from the sand through the water line; its top (1500, 236) is above the water; a gold star to touch at STAR.
  "bigrock_eve" the same in the evening light.
Kinds (registered into art2.RIGS, kit.PT, kit.BOX): "fish_zip" (Zip, yellow with a blue tail), "fish_pearl" (Pearl, pink with a purple tail).
  kit.PT / kit.BOX for "turtle" (art2.turtle had none).
Props: seagrass_front (seven blades b0..b6 that can be nibbled short), speed_lines, puff, bubbles, paddle, sea_map (a long trip across the sea, a
  little turtle that moves along it), loop_arrow, spark, start_flag.
"""
import math, random
import art, art2, kit
from art import eye, INK
from art2 import _ol, _mouth, _brow

WL = 300                      # the water line of the split views
STAR = (1318, 640)            # the gold star on the Big Rock
ROCK_TOP = (1500, 236)        # where Milo stands on the Big Rock
ISLE_TOP = (1560, 256)        # where Milo stands on the little rock at the start

ZIPC = {"fill": "#ffd23f", "shade": "#f2a81f", "fin": "#3fa7e0", "line": "#7a4a10", "belly": "#fff3b8"}
PEARLC = {"fill": "#ff9ec4", "shade": "#ee6fa6", "fin": "#b58af0", "line": "#7a2a55", "belly": "#ffe3ef"}


# ------------------------------------------------------------------ the fish
def fish(pid, c, spots=False):
    """A little round fish, side view, facing right. Parts: -tail (wags), -fin (side fin), -jaw, -eye, -brow, -smile / -frown. Its belly is at y = -20."""
    ln = c["line"]
    body_d = "M-150 -120 C-110 -236 90 -246 164 -130 C100 -6 -110 -6 -150 -120Z"
    tail_d = "M-136 -120 L-256 -206 Q-226 -120 -256 -34Z"
    dors_d = "M-70 -208 Q-20 -296 64 -212Z"
    fin_d = "M-6 -112 Q-78 -70 -40 -36 Q14 -52 12 -100Z"
    tail = '<g id="%s-tail">%s<path d="%s" fill="%s"/><path d="M-160 -120 L-232 -160 M-160 -120 L-232 -80" stroke="%s" stroke-width="6" stroke-linecap="round" opacity=".5"/></g>' % (
        pid, _ol('<path d="%s"/>' % tail_d, ln, 8), tail_d, c["fin"], ln)
    dors = _ol('<path d="%s"/>' % dors_d, ln, 8) + '<path d="%s" fill="%s"/>' % (dors_d, c["fin"])
    body = _ol('<path d="%s"/>' % body_d, ln) + '<path d="%s" fill="%s"/>' % (body_d, c["fill"])
    belly = '<path d="M-120 -84 C-60 -14 90 -14 140 -92 C80 -50 -50 -46 -120 -84Z" fill="%s"/>' % c["belly"]
    shine = '<path d="M-80 -196 Q0 -232 80 -196" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".45"/>'
    if spots: marks = "".join('<circle cx="%d" cy="%d" r="%d" fill="%s" opacity=".75"/>' % (x, y, r, c["shade"]) for x, y, r in ((-70, -150, 17), (-30, -110, 13), (-96, -104, 12)))
    else: marks = "".join('<path d="M%d -200 Q%d -120 %d -44" stroke="%s" stroke-width="16" fill="none" stroke-linecap="round" opacity=".8"/>' % (x, x - 22, x, c["shade"]) for x in (-84, -36))
    fin = '<g id="%s-fin">%s<path d="%s" fill="%s"/></g>' % (pid, _ol('<path d="%s"/>' % fin_d, ln, 7), fin_d, c["fin"])
    jaw = '<g id="%s-jaw" opacity="0"><path d="M98 -96 q20 18 42 2 q-6 22 -22 22 q-14 0 -20 -24Z" fill="#c9667d" stroke="%s" stroke-width="6" stroke-linejoin="round"/></g>' % (pid, ln)
    face = (jaw + _mouth(pid, 120, -98, 40, ln, 6) + eye(pid + "-eye", 76, -140, 32, lid=c["fill"]) + _brow(pid, 76, -182, 44, ln, 7)
            + '<ellipse cx="104" cy="-118" rx="14" ry="8" fill="#ff8fb1" opacity=".6"/>')
    return '<g id="%s">%s%s%s%s%s%s%s%s</g>' % (pid, tail, dors, body, belly, marks, shine, fin, face)


_FISH_RIG = dict(neck=None, tail="-140 -120", ear=None, legs=None, hip=0, jaw=("y", 8), eyes=["eye"], brows=["brow"])
art2.RIGS["fish_zip"] = dict(_FISH_RIG, build=lambda p: fish(p, ZIPC))
art2.RIGS["fish_pearl"] = dict(_FISH_RIG, build=lambda p: fish(p, PEARLC, spots=True))
for _k in ("fish_zip", "fish_pearl"):
    kit.PT[_k] = {"head": (70, -130), "eye": (76, -150), "body": (0, -124), "top": (0, -250), "feet": (0, 0), "all": (-40, -124)}
    kit.BOX[_k] = (-260, 170, -300)
# where the parts of Tula are (art2.turtle: shell dome from y -350 to -150, head at (258, -180), belly at y -84, front flipper down to y 60)
kit.PT["turtle"] = {"head": (258, -182), "eye": (272, -186), "body": (0, -200), "top": (0, -350), "flipper": (100, -30), "feet": (0, 0), "all": (60, -170)}
kit.BOX["turtle"] = (-260, 350, -360)


# ------------------------------------------------------------------ the sea
def _under(p, top="#8fe0ff", bot="#2f9fd6", y0=-900, rays=True, k="u"):
    g = ('<defs><linearGradient id="%s%s" gradientUnits="userSpaceOnUse" x1="0" y1="%d" x2="0" y2="1000"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
         '<rect x="-500" y="%d" width="2920" height="%d" fill="url(#%s%s)"/>' % (k, p, max(y0, -60), top, bot, y0, 2000 - y0, k, p))
    if rays: g += "".join('<path d="M%d %d L%d 900 L%d 900 L%d %d Z" fill="#fff" opacity=".08"/>' % (x, max(y0, -100), x + 130, x + 280, x + 70, max(y0, -100)) for x in (60, 660, 1260, 1800))
    return g


def _airsky(p, top="#8fd8ff", bot="#eaf8ff"):
    return ('<defs><linearGradient id="a%s" gradientUnits="userSpaceOnUse" x1="0" y1="-200" x2="0" y2="%d"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
            '<rect x="-500" y="-900" width="2920" height="%d" fill="url(#a%s)"/>' % (p, WL, top, bot, 900 + WL, p))


def _waves(col="#ffffff", band="#bfeeff"):
    d = "M-500 %d " % WL + " ".join("q40 -16 80 0 q40 16 80 0" for _ in range(19))
    return '<path d="%s L2540 %d L-500 %d Z" fill="%s" opacity=".55"/><path d="%s" stroke="%s" stroke-width="9" fill="none" stroke-linecap="round" opacity=".95"/>' % (d, WL + 46, WL + 46, band, d, col)


def _sand(y=880, a="#f2dfa6", b="#ecd592"):
    mid = '<path d="M-500 %d C200 %d 700 %d 1200 %d S2000 %d 2420 %d L2420 %d L-500 %d Z" fill="%s"/>' % (y - 60, y - 120, y - 80, y - 100, y - 100, y - 70, y + 20, y + 20, a)
    near = '<rect x="-500" y="%d" width="2920" height="1200" fill="%s"/>' % (y - 10, b)
    return mid, near


def _blade(x, y, h, d, col, w=16):
    return '<path d="M%d %d q%d %d 0 %d q%d %d 0 %d" stroke="%s" stroke-width="%d" fill="none" stroke-linecap="round"/>' % (x, y, d, -h // 4, -h // 2, -d, -h // 4, -h // 2, col, w)


def _coral(x, y, s=1.0, col="#ff8fa8", dark="#e0607f"):
    arms = "".join('<path d="M0 0 Q%d %d %d %d" stroke="%s" stroke-width="30" fill="none" stroke-linecap="round"/><circle cx="%d" cy="%d" r="19" fill="%s"/>' % (dx // 3, dy // 2, dx, dy, col, dx, dy, col)
                   for dx, dy in ((-90, -120), (-30, -190), (40, -170), (100, -110)))
    return '<g transform="translate(%d %d) scale(%.2f)"><ellipse cx="0" cy="0" rx="70" ry="22" fill="%s"/>%s</g>' % (x, y, s, dark, arms)


def _fan(x, y, s=1.0, col="#c9a8f0"):
    return ('<g transform="translate(%d %d) scale(%.2f)"><path d="M0 0 C-150 -80 -130 -250 0 -280 C130 -250 150 -80 0 0Z" fill="%s"/>' % (x, y, s, col)
            + "".join('<path d="M0 0 L%d %d" stroke="#fff" stroke-width="7" opacity=".5" stroke-linecap="round"/>' % (dx, dy) for dx, dy in ((-80, -180), (-30, -240), (30, -240), (80, -180))) + '</g>')


def _stone(x, y, w, h, col="#8d93ad", hi="#aab0c8"):
    return ('<path d="M%d %d C%d %d %d %d %d %d Z" fill="%s"/><path d="M%d %d q%d %d %d 0" stroke="%s" stroke-width="12" fill="none" stroke-linecap="round" opacity=".8"/>'
            % (x - w, y, x - w, y - h * 1.3, x + w, y - h * 1.3, x + w, y, col, x - w * .5, y - h * .8, w * .5, -h * .25, w, hi))


def _shells(pts):
    return "".join('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s"/>' % (x, y, w, w * .5, c) for x, y, w, c in pts)


def _tall_rock(x0, x1, top_y, tx0, tx1, col="#8d93ad", hi="#b3b9d0", dark="#73799a"):
    """A rock from the sand (y 900) up through the water: its foot spans x0..x1, its flat top tx0..tx1 at top_y."""
    d = "M%d 900 C%d 640 %d %d %d %d Q%d %d %d %d C%d %d %d 640 %d 900Z" % (x0, x0 + 30, tx0 - 70, top_y + 110, tx0, top_y + 14, (tx0 + tx1) // 2, top_y - 26, tx1, top_y + 14, tx1 + 70, top_y + 110, x1 - 30, x1)
    return ('<path d="%s" fill="%s" stroke="#565b78" stroke-width="10" stroke-linejoin="round"/>' % (d, col)
            + '<path d="M%d %d Q%d %d %d %d" stroke="%s" stroke-width="16" fill="none" stroke-linecap="round" opacity=".9"/>' % (tx0 + 10, top_y + 30, (tx0 + tx1) // 2, top_y - 4, tx1 - 10, top_y + 30, hi)
            + '<path d="M%d 760 q60 -40 130 -10 M%d 560 q50 -30 110 -6" stroke="%s" stroke-width="12" fill="none" stroke-linecap="round" opacity=".6"/>' % (x0 + 90, (x0 + tx0) // 2 + 60, dark)
            + '<path d="M%d %d q24 -30 50 -4 q26 -30 54 0 q20 -22 44 2 l0 14 l-148 0Z" fill="#6fcf7a"/>' % (tx0 + 6, top_y + 8))


def _star(x, y, r=64, col="#ffd23f"):
    pts = " ".join("%.0f,%.0f" % (x + (r if k % 2 == 0 else r * .45) * math.sin(k * math.pi / 5), y - (r if k % 2 == 0 else r * .45) * math.cos(k * math.pi / 5)) for k in range(10))
    return '<polygon points="%s" fill="%s" stroke="#402010" stroke-width="9" stroke-linejoin="round"/>' % (pts, col)


def bg_sea_start(p):
    """The start of the race: a coral arch with a START banner under the water, a little rock island in the air for Milo."""
    far = (_airsky(p) + art._sun(p + "sun", 300, 120, 60) + art._cloud(p + "c1", 900, 110, .7) + art._cloud(p + "c2", 1300, 60, .5)
           + _under(p, "#9be6ff", "#2f9fd6", WL) + "".join(_stone(x, 860, w, h, "#58b4e0", "#79c8ec") for x, w, h in ((80, 220, 200), (1050, 260, 150), (1900, 200, 230))))
    sm, sn = _sand()
    arch = ('<path d="M250 880 C240 640 300 470 470 470 C640 470 700 640 690 880 L610 880 C616 690 580 560 470 560 C360 560 324 690 330 880Z" fill="#ff9a8a" stroke="#c2574e" stroke-width="10" stroke-linejoin="round"/>'
            + "".join('<circle cx="%d" cy="%d" r="%d" fill="#ffc2b6"/>' % (x, y, r) for x, y, r in ((290, 760, 14), (300, 620, 11), (380, 510, 13), (560, 512, 12), (646, 640, 12), (652, 780, 14)))
            + '<rect x="330" y="366" width="280" height="96" rx="24" fill="#2f80ed" stroke="#fff" stroke-width="10"/>'
            '<text x="470" y="436" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="74" fill="#fff">START</text>')
    mid = _waves() + sm + "".join(_blade(x, 850, 190, d, "#3fae7a") for x, d in ((90, 30), (150, -26), (1130, 28), (1200, -30)))
    near = sn + _tall_rock(1380, 1760, ISLE_TOP[1], 1480, 1640) + arch + _coral(1010, 930, .8, "#ffb347", "#e08a1f") + _shells(((820, 990, 44, "#ff9ab8"), (1240, 1030, 50, "#c9a8f0"), (120, 1010, 40, "#fff3b8")))
    return far, mid, near


def bg_meadow(p):
    """The seagrass meadow: tall green seagrass all across, behind the swimmers."""
    r = random.Random(12)
    far = _under(p, "#9be6ff", "#2f9fd6") + "".join(_blade(x, 860, r.randint(330, 520), r.choice((-34, 30, 38, -28)), "#5cc99a", 13) for x in range(-300, 2300, 74))
    sm, sn = _sand()
    mid = sm + "".join(_blade(x + r.randint(-14, 14), 880, r.randint(260, 470), r.choice((-40, 36, 44, -32)), r.choice(("#3fae7a", "#35a06e", "#49ba84")), 18) for x in range(-260, 2300, 96))
    near = sn + "".join(_blade(x, 960 + (k % 3) * 22, 150, (-22, 24)[k % 2], "#2f946a", 15) for k, x in enumerate(range(-200, 2200, 210))) + _shells(((640, 1010, 40, "#ff9ab8"), (1500, 1030, 46, "#fff3b8")))
    return far, mid, near


def bg_fork(p):
    """Two ways through a rock wall: a dark opening on the left, a bright one on the right."""
    far = _under(p, "#9be6ff", "#3aa6da") + '<rect x="1090" y="440" width="560" height="470" fill="#b9f0ff" opacity=".55"/>' + _coral(1380, 850, .7, "#ff8fa8", "#e0607f") + _fan(1260, 860, .6)
    hole = lambda x: "M%d 890 L%d 640 C%d 430 %d 430 %d 640 L%d 890Z" % (x - 190, x - 190, x - 190, x + 190, x + 190, x + 190)
    wall = ('<path fill-rule="evenodd" d="M-500 230 C100 150 500 250 960 190 S1900 150 2420 240 L2420 900 L-500 900Z %s %s" fill="#7f86a6" stroke="#565b78" stroke-width="10" stroke-linejoin="round"/>' % (hole(560), hole(1360))
            + '<path d="M370 890 L370 640 C370 430 750 430 750 640 L750 890Z" fill="#123f66" opacity=".78"/>'
            + "".join('<path d="M%d %d q70 -34 150 -6" stroke="#9aa1c0" stroke-width="14" fill="none" stroke-linecap="round" opacity=".8"/>' % (x, y) for x, y in ((-80, 420), (840, 380), (900, 640), (1640, 420), (1700, 700), (60, 700))))
    sm, sn = _sand()
    mid = wall + sm
    near = sn + _stone(960, 960, 90, 60) + _shells(((300, 1010, 40, "#ffb347"), (1700, 1020, 44, "#ff9ab8")))
    return far, mid, near


def bg_reef(p):
    """The coral garden: the bright way to the Big Rock."""
    far = _under(p, "#a6ecff", "#38a8de") + "".join(_stone(x, 860, w, h, "#58b4e0", "#79c8ec") for x, w, h in ((200, 260, 190), (1000, 320, 140), (1760, 240, 220)))
    sm, sn = _sand()
    mid = (sm + _coral(170, 860, 1.2) + _fan(420, 870, 1.0) + _coral(760, 850, .9, "#ffb347", "#e08a1f") + _fan(1120, 860, .8, "#8fe0c0") + _coral(1450, 856, 1.1, "#ff8fd0", "#d860a8") + _fan(1760, 872, 1.0, "#ffd27a")
           + "".join('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#fff" stroke-width="5" opacity=".6"/>' % (x, y, r) for x, y, r in ((560, 380, 16), (600, 300, 10), (1380, 420, 14), (1420, 340, 9), (980, 250, 12))))
    near = sn + _shells(((420, 1000, 50, "#ff9ab8"), (1500, 1020, 60, "#ffb347"), (980, 1050, 44, "#c9a8f0"))) + _star(760, 1000, 34, "#ff8a5c")
    return far, mid, near


def _bigrock(p, eve=False):
    if eve:
        far = (_airsky(p, "#ffb38a", "#ffe6b0") + '<circle cx="520" cy="%d" r="92" fill="#ffd27a"/><circle cx="520" cy="%d" r="140" fill="#ffd27a" opacity=".3"/>' % (WL - 30, WL - 30) + art._cloud(p + "c1", 1000, 110, .7, "#ffe1ea")
               + _under(p, "#cdeaf2", "#3f86c2", WL))
        waves = _waves("#fff3e0", "#ffd9c0")
    else:
        far = _airsky(p) + art._sun(p + "sun", 420, 110, 60) + art._cloud(p + "c1", 900, 120, .7) + art._cloud(p + "c2", 200, 70, .5) + _under(p, "#9be6ff", "#2f9fd6", WL)
        waves = _waves()
    far += "".join(_stone(x, 860, w, h, "#58b4e0" if not eve else "#6f9fd0", "#79c8ec") for x, w, h in ((120, 240, 200), (760, 220, 130)))
    sm, sn = _sand()
    mid = waves + sm + _coral(260, 860, .9) + _fan(560, 868, .7)
    rock = _tall_rock(1130, 1900, ROCK_TOP[1], 1390, 1620) + _star(*STAR) + '<path d="M1634 250 L1634 120" stroke="#6a4a26" stroke-width="12" stroke-linecap="round"/><path d="M1634 124 L1740 156 L1634 190Z" fill="#ff5a5a" stroke="#402010" stroke-width="7" stroke-linejoin="round"/>'
    near = sn + rock + _shells(((300, 1010, 50, "#ff9ab8"), (820, 1030, 46, "#fff3b8")))
    return far, mid, near


art.BG.update({"sea_start": bg_sea_start, "meadow": bg_meadow, "fork": bg_fork, "reef": bg_reef, "bigrock": lambda p: _bigrock(p), "bigrock_eve": lambda p: _bigrock(p, True)})
art.PLACE.update({"sea_start": "the start of the race", "meadow": "the seagrass meadow", "fork": "the two ways", "reef": "the coral garden", "bigrock": "the Big Rock", "bigrock_eve": "the Big Rock in the evening"})


# ------------------------------------------------------------------ props
def seagrass_front(p, n=7, h=430):
    """Seven thick seagrass blades in FRONT of the swimmers, anchored at the sand (y = 0). Each blade is its own part (b0..b6) so it can be nibbled short."""
    out = ""
    for k in range(n):
        x = (k - (n - 1) / 2) * 96; hh = h - (k % 3) * 46; d = (36, -30, 42)[k % 3]
        out += '<g id="%s-b%d">%s%s</g>' % (p, k, _blade(int(x), 0, hh, d, "#1f6f4c", 34), _blade(int(x), 0, hh, d, ("#3fae7a", "#49ba84")[k % 2], 22))
    return '<g id="%s">%s</g>' % (p, out)


def speed_lines(p):
    return '<g id="%s">' % p + "".join('<path d="M%d %d h%d" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".85"/>' % (x, y, w) for x, y, w in ((-150, -50, 130), (-190, 0, 170), (-140, 50, 120))) + '</g>'


def puff(p):
    """Little puffs of breath in front of a tired swimmer."""
    return '<g id="%s">' % p + "".join('<g id="%s-%d"><circle cx="%d" cy="%d" r="%d" fill="#fff" stroke="#7fbfe0" stroke-width="6" opacity=".95"/></g>' % (p, k, x, y, r) for k, (x, y, r) in enumerate(((0, 0, 20), (38, -34, 15), (70, -72, 11)))) + '</g>'


def bubbles(p):
    return '<g id="%s">' % p + "".join('<circle cx="%d" cy="%d" r="%d" fill="#fff" fill-opacity=".25" stroke="#fff" stroke-width="5" opacity=".9"/>' % (x, y, r) for x, y, r in ((0, 0, 18), (30, -50, 12), (-14, -96, 9), (22, -140, 7))) + '</g>'


def paddle(p):
    """A canoe paddle, standing upright (blade down), anchored at its middle."""
    return ('<g id="%s"><path d="M0 -330 L0 60" stroke="%s" stroke-width="40" stroke-linecap="round"/><path d="M0 -330 L0 60" stroke="#c98a4a" stroke-width="24" stroke-linecap="round"/>'
            '<path d="M-74 60 C-90 200 -60 330 0 350 C60 330 90 200 74 60Z" fill="#e0a45e" stroke="%s" stroke-width="10" stroke-linejoin="round"/><path d="M-30 110 Q-40 220 -8 300" stroke="#f6cf96" stroke-width="12" fill="none" stroke-linecap="round"/>'
            '<rect x="-50" y="-360" width="100" height="44" rx="20" fill="#c98a4a" stroke="%s" stroke-width="9"/></g>' % (p, INK, INK, INK))


def sea_map(p):
    """A long trip across the sea on one picture: a seagrass bay on the left, a sandy beach on the right, a dotted way between, a little turtle (-t) that swims along it."""
    wave = lambda y: "".join('<path d="M%d %d q24 -14 48 0 q24 14 48 0" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".7"/>' % (x, y) for x in (-420, -160, 110, 360))
    return ('<g id="%s"><rect x="-700" y="-280" width="1400" height="560" rx="40" fill="#4fb4ea" stroke="%s" stroke-width="12"/>%s%s'
            '<path d="M-700 60 C-640 -40 -520 -20 -500 80 C-480 180 -560 240 -660 280 L-700 240Z" fill="#f2dfa6" stroke="%s" stroke-width="9" stroke-linejoin="round"/>'
            '%s<path d="M700 -40 C620 -120 520 -80 510 20 C500 140 600 220 700 240Z" fill="#f6e3ad" stroke="%s" stroke-width="9" stroke-linejoin="round"/>'
            '<path d="M610 40 q20 -50 0 -90 M610 -50 q-40 -30 -70 -4 M610 -50 q40 -30 70 -4 M610 -50 q-10 -40 -50 -44 M610 -50 q10 -40 50 -44" stroke="#3f9e5c" stroke-width="12" fill="none" stroke-linecap="round"/>'
            '<path id="%s-way" d="M-470 90 C-250 -160 200 200 480 30" stroke="#fff" stroke-width="14" stroke-dasharray="8 30" stroke-linecap="round" fill="none"/>'
            '<g id="%s-t" transform="translate(-470 120)"><g transform="scale(.27)">%s</g></g></g>'
            % (p, INK, wave(-190), wave(190), INK, "".join(_blade(x, 150, 110, d, "#2f946a", 13) for x, d in ((-640, 16), (-600, -14), (-560, 16))), INK, p, p, art2.turtle(p + "tt")))


def loop_arrow(p):
    """A round arrow: this way only goes round and comes back."""
    return ('<g id="%s"><path d="M120 0 A120 120 0 1 1 60 -104" stroke="%s" stroke-width="44" fill="none" stroke-linecap="round"/><path d="M120 0 A120 120 0 1 1 60 -104" stroke="#ff8a3d" stroke-width="26" fill="none" stroke-linecap="round"/>'
            '<path d="M36 -160 L128 -118 L52 -52Z" fill="#ff8a3d" stroke="%s" stroke-width="9" stroke-linejoin="round"/></g>' % (p, INK, INK))


def spark(p):
    """A burst of light round something that was just touched."""
    return '<g id="%s">' % p + "".join('<path d="M%.0f %.0f L%.0f %.0f" stroke="#fff6c9" stroke-width="16" stroke-linecap="round"/>' % (90 * math.cos(a), 90 * math.sin(a), 150 * math.cos(a), 150 * math.sin(a)) for a in [k * math.pi / 4 for k in range(8)]) + '</g>'
