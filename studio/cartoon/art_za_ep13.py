"""Pictures for za_ep13 "Can Little Crab Find a Shell That Fits?" (Nov 21 2026). New places, one new friend (Little Crab, a hermit crab) and props only:
no existing character, place or prop is drawn differently (Tula is art2.turtle as it is; the sea helpers of art_za_ep12 are used as they are).

Places:
  "shore"      split view of the shallow water: sand and pebbles under the water, a little rock on the right whose top (ISLE_TOP) is in the air for Milo.
  "shore_eve"  the same in the evening light.
  "shellbed"   a sandy place full of little shells.
  "rocks"      big grey rocks.
  "kelp"       the green kelp forest.
  "deep"       the deep blue water, where the empty shells lie.
Kinds (registered into art2.RIGS, kit.PT, kit.BOX): "hermit_small" (Little Crab in his old blue shell, much too small for him), "hermit_fit" (in the golden
  shell that fits), "hermit_blue" (a crab the blue shell fits: the tiny neighbour of the ending), "hermit_none" (the picture board only: the soft back part).
Props: shell_blue / shell_gold / shell_green / shell_pink / shell_purple / shell_white / shell_coral (empty snail shells, opening to the right, standing on y = 0), big_shell_peek (the
  huge shell with Little Crab's eyes looking out of it), snail_shell (a shell with a snail, -sn, that peeks out), arrow, sparkle, pull_lines, think_bulb.
"""
import math, random
import art, art2, kit
import art_za_ep12 as A12
from art import eye, INK
from art2 import _ol, _mouth

WL = A12.WL
ISLE_TOP = (1560, 256)        # where Milo stands on the little rock

CRAB = {"fill": "#ff7a4d", "shade": "#e2562c", "light": "#ffb08a", "line": "#7a2a12", "far": "#d9603a", "soft": "#ffc2b0"}
SHELLS = {"blue": ("#7fc4e8", "#4a93c4", "#2d5f8a"), "gold": ("#ffd166", "#f0a630", "#8a5a10"), "green": ("#9ad6a0", "#5fae6c", "#2f6a3c"),
          "pink": ("#ffb3c7", "#ee7fa0", "#8a3050"), "purple": ("#c9a8f0", "#9a6fd8", "#4a2f7a"), "white": ("#fff3dc", "#e8d2a8", "#7a6540"), "coral": ("#ff9a8a", "#e0685a", "#8a2f28")}


# ------------------------------------------------------------------ snail shells
def _shell(col, k=1.0, ox=0, oy=0, hole=True):
    """A spiral snail shell, its opening to the right. Unscaled it is about 330 wide and 290 tall and stands on y = 0."""
    fill, dark, ln = SHELLS[col]
    whorls = ((-60, -120, 112), (-138, -196, 70), (-186, -240, 42), (-216, -266, 22))
    sh = "".join('<circle cx="%d" cy="%d" r="%d"/>' % w for w in whorls)
    body = _ol(sh, ln) + '<g fill="%s">%s</g>' % (fill, sh)
    lines = ('<path d="M-150 -70 Q-178 -150 -100 -214" stroke="%s" stroke-width="12" fill="none" stroke-linecap="round"/>' % dark
             + '<path d="M-110 -30 Q-10 -20 30 -110" stroke="%s" stroke-width="12" fill="none" stroke-linecap="round" opacity=".7"/>' % dark
             + '<path d="M-186 -150 Q-200 -200 -150 -252" stroke="%s" stroke-width="10" fill="none" stroke-linecap="round"/>' % dark
             + '<path d="M-216 -214 Q-222 -244 -196 -272" stroke="%s" stroke-width="8" fill="none" stroke-linecap="round"/>' % dark
             + '<path d="M-110 -196 Q-60 -232 -6 -200" stroke="#fff" stroke-width="13" fill="none" stroke-linecap="round" opacity=".5"/>')
    mouth = '<ellipse cx="18" cy="-104" rx="50" ry="78" fill="%s" stroke="%s" stroke-width="9"/><ellipse cx="24" cy="-100" rx="30" ry="56" fill="#3a2418" opacity=".55"/>' % (dark, ln) if hole else ""
    return '<g transform="translate(%d %d) scale(%.3f)">%s%s%s</g>' % (ox, oy, k, body, lines, mouth)


def _shell_prop(col, k=1.0, hole=True):
    return lambda p: '<g id="%s">%s</g>' % (p, _shell(col, k, hole=hole))


shell_blue, shell_gold, shell_green, shell_pink, shell_purple, shell_white, shell_coral = (_shell_prop(c) for c in ("blue", "gold", "green", "pink", "purple", "white", "coral"))
shell_gold_on = _shell_prop("gold", hole=False)      # the golden shell seen from outside (no opening): it slides over the soft back part on the picture board


# ------------------------------------------------------------------ Little Crab
def hermit(pid, shell="small", c=CRAB):
    """A hermit crab, side view, facing right, feet on y = 0. Parts: -shell, -neck (the two eyes on their stalks), -eye, -eye2, -jaw, -smile / -frown,
    -cl (the big near claw), -cr (the far claw), -fl -bl -fl2 -bl2 (walking legs), -soft (the soft back part: only without a shell)."""
    ln = c["line"]

    def leg(x, far, name):
        col = c["far"] if far else c["fill"]; d = "M%d -78 q34 16 26 74" % x
        return '<g id="%s-%s"><path d="%s" stroke="%s" stroke-width="30" fill="none" stroke-linecap="round"/><path d="%s" stroke="%s" stroke-width="15" fill="none" stroke-linecap="round"/></g>' % (pid, name, d, ln, d, col)

    def claw(x0, y0, x1, y1, r, name, col):
        arm = "M%d %d L%d %d" % (x0, y0, x1, y1)
        pin = '<ellipse cx="%d" cy="%d" rx="%d" ry="%d"/>' % (x1 + r * .7, y1, r, r * .74)
        gap = '<path d="M%d %d L%d %d L%d %d Z" fill="%s"/>' % (x1 + r * 1.74, y1 - r * .16, x1 + r * .56, y1 - r * .04, x1 + r * 1.6, y1 + r * .42, ln)
        return ('<g id="%s-%s"><path d="%s" stroke="%s" stroke-width="40" stroke-linecap="round"/><path d="%s" stroke="%s" stroke-width="22" stroke-linecap="round"/>' % (pid, name, arm, ln, arm, col)
                + _ol(pin, ln, 8) + '<g fill="%s">%s</g>%s<path d="M%d %d q%d %d %d 0" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" opacity=".5"/></g>'
                % (col, pin, gap, x1 + r * .2, y1 - r * .34, r * .5, -r * .3, r))

    if shell == "small": sh = '<g id="%s-shell">%s</g>' % (pid, _shell("blue", .56, 24, -52, hole=False))
    elif shell == "fit": sh = '<g id="%s-shell">%s</g>' % (pid, _shell("gold", 1.0, 30, -6, hole=False))
    elif shell == "blue": sh = '<g id="%s-shell">%s</g>' % (pid, _shell("blue", 1.0, 30, -6, hole=False))
    else:      # no shell: the soft back part, curled (the picture board)
        d = "M40 -150 C-60 -190 -170 -150 -170 -84 C-170 -30 -100 -16 -74 -54 C-58 -80 -96 -96 -104 -76"
        sh = ('<g id="%s-soft"><path d="%s" stroke="%s" stroke-width="96" fill="none" stroke-linecap="round"/><path d="%s" stroke="%s" stroke-width="78" fill="none" stroke-linecap="round"/>'
              '<path d="M-40 -196 Q-110 -196 -150 -150" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".55"/></g>' % (pid, d, ln, d, c["soft"]))
    body_sh = '<ellipse cx="96" cy="-108" rx="92" ry="72"/>'
    body = _ol(body_sh, ln) + '<g fill="%s">%s</g>' % (c["fill"], body_sh)
    shade = '<path d="M8 -92 A92 72 0 0 0 184 -92 A110 96 0 0 1 8 -92Z" fill="%s" opacity=".6"/><path d="M44 -156 Q96 -182 148 -156" stroke="%s" stroke-width="12" fill="none" stroke-linecap="round" opacity=".7"/>' % (c["shade"], c["light"])
    stalk = lambda x0, x1, y1: '<path d="M%d -166 L%d %d" stroke="%s" stroke-width="24" stroke-linecap="round"/><path d="M%d -166 L%d %d" stroke="%s" stroke-width="11" stroke-linecap="round"/>' % (x0, x1, y1, ln, x0, x1, y1, c["fill"])
    ring = lambda x, y, r: '<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (x, y, r + 7, ln)
    neck = ('<g id="%s-neck">' % pid + stalk(84, 74, -226) + stalk(138, 150, -224) + ring(74, -244, 27) + eye(pid + "-eye2", 74, -244, 27, lid=c["fill"])
            + ring(150, -242, 30) + eye(pid + "-eye", 150, -242, 30, lid=c["fill"]) + '</g>')
    jaw = '<g id="%s-jaw" opacity="0"><path d="M120 -120 q22 18 46 2 q-6 24 -24 24 q-16 0 -22 -26Z" fill="#a8323e" stroke="%s" stroke-width="6" stroke-linejoin="round"/></g>' % (pid, ln)
    face = jaw + _mouth(pid, 142, -122, 40, ln, 6) + '<ellipse cx="100" cy="-128" rx="15" ry="9" fill="#ffd0c0" opacity=".8"/>'
    feel = '<path d="M176 -150 q40 -30 62 -4" stroke="%s" stroke-width="7" fill="none" stroke-linecap="round"/>' % ln
    shadow = '<ellipse cx="40" cy="4" rx="210" ry="14" fill="#000" opacity=".12"/>'
    return ('<g id="%s">%s%s%s%s%s%s%s%s%s%s%s%s%s</g>' % (pid, shadow, claw(120, -128, 196, -160, 34, "cr", c["far"]), leg(44, True, "bl2"), leg(108, True, "fl2"), sh, body, shade,
                                                         leg(70, False, "bl"), leg(134, False, "fl"), feel, neck, face, claw(150, -74, 214, -58, 46, "cl", c["fill"])))


_RIG = dict(neck="112 -160", tail=None, ear=None, legs={"fl": 134, "bl": 70, "fl2": 108, "bl2": 44}, hip=-78, jaw=("y", 8), eyes=["eye", "eye2"], brows=[])
for _k, _s in (("hermit_small", "small"), ("hermit_fit", "fit"), ("hermit_blue", "blue"), ("hermit_none", "none")):
    art2.RIGS[_k] = dict(_RIG, build=(lambda s_: (lambda p: hermit(p, s_)))(_s))
    kit.PT[_k] = {"head": (120, -200), "eye": (150, -242), "body": (60, -120), "top": (40, -290), "feet": (0, 0), "all": (40, -140), "claw": (250, -58)}
    kit.BOX[_k] = (-260, 310, -300)
kit.BOX["hermit_small"] = (-120, 310, -300)


# ------------------------------------------------------------------ places
def _pebbles(pts): return "".join('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" stroke="#00000022" stroke-width="4"/>' % (x, y, w, w * .55, c) for x, y, w, c in pts)


def _mini(x, y, col, k=.16, flip=False):
    return '<g transform="translate(%d %d) scale(%s 1)">%s</g>' % (x, y, -1 if flip else 1, _shell(col, k))


def _shore(p, eve=False):
    if eve:
        far = (A12._airsky(p, "#ffb38a", "#ffe6b0") + '<circle cx="420" cy="%d" r="92" fill="#ffd27a"/><circle cx="420" cy="%d" r="140" fill="#ffd27a" opacity=".3"/>' % (WL - 30, WL - 30)
               + art._cloud(p + "c1", 1000, 110, .7, "#ffe1ea") + A12._under(p, "#cdeaf2", "#3f86c2", WL))
        waves = A12._waves("#fff3e0", "#ffd9c0")
    else:
        far = A12._airsky(p) + art._sun(p + "sun", 360, 120, 60) + art._cloud(p + "c1", 820, 110, .7) + art._cloud(p + "c2", 1240, 70, .5) + A12._under(p, "#a6ecff", "#3aa6da", WL)
        waves = A12._waves()
    far += "".join(A12._stone(x, 860, w, h, "#58b4e0" if not eve else "#6f9fd0", "#79c8ec") for x, w, h in ((140, 230, 170), (980, 280, 120)))
    sm, sn = A12._sand()
    mid = waves + sm + A12._coral(170, 866, .7, "#ffb347", "#e08a1f")
    near = (sn + A12._tall_rock(1380, 1760, ISLE_TOP[1], 1480, 1640) + _pebbles(((260, 1000, 46, "#c9c2b0"), (1180, 1030, 38, "#b9b2a4"), (760, 1040, 30, "#d8d0bc")))
            + A12._star(1010, 1010, 30, "#ff8a5c") + _mini(420, 1050, "pink") + _mini(1320, 1010, "white", .14, True))
    return far, mid, near


def bg_shellbed(p):
    """A sandy place full of little shells."""
    r = random.Random(5)
    far = A12._under(p, "#a6ecff", "#38a8de") + "".join(A12._stone(x, 860, w, h, "#58b4e0", "#79c8ec") for x, w, h in ((320, 300, 150), (1500, 340, 190)))
    sm, sn = A12._sand()
    mid = sm + "".join(_mini(x, 850 + r.randint(-14, 10), r.choice(("pink", "white", "green", "purple")), r.choice((.2, .24, .28)), r.random() < .5) for x in range(-260, 2300, 190))
    near = sn + "".join(_mini(x, 1000 + r.randint(0, 50), r.choice(("pink", "white", "purple")), r.choice((.16, .2)), r.random() < .5) for x in range(-200, 2300, 260)) + A12._star(1480, 990, 30, "#ffb347")
    return far, mid, near


def bg_rocks(p):
    """Big grey rocks."""
    far = A12._under(p, "#9be6ff", "#3aa6da") + "".join(A12._stone(x, 860, w, h, "#58b4e0", "#79c8ec") for x, w, h in ((60, 280, 300), (700, 240, 180), (1900, 300, 340)))
    sm, sn = A12._sand()
    mid = (sm + A12._stone(200, 880, 250, 300, "#8d93ad", "#b3b9d0") + A12._stone(1680, 880, 280, 380, "#7f86a6", "#a4abc6") + A12._stone(1320, 880, 150, 170, "#9aa0b8", "#bcc2d8")
           + A12._stone(520, 880, 120, 110, "#9aa0b8", "#bcc2d8"))
    near = sn + _pebbles(((300, 1000, 50, "#9aa0b8"), (1500, 1030, 60, "#8d93ad"), (900, 1050, 40, "#b3b9d0"), (1840, 990, 44, "#9aa0b8")))
    return far, mid, near


def bg_kelp(p):
    """The green kelp forest: tall kelp behind the friends."""
    r = random.Random(31)
    def kelp(x, h, col, w):
        leaves = "".join('<ellipse cx="%d" cy="%d" rx="34" ry="13" fill="%s" transform="rotate(%d %d %d)"/>' % (x + (28 if k % 2 else -28), 860 - 90 - k * 110, col, (-28 if k % 2 else 28), x, 860 - 90 - k * 110) for k in range(h // 110))
        return A12._blade(x, 870, h, 30, col, w) + leaves
    far = A12._under(p, "#9be6c8", "#2f9fb6") + "".join(kelp(x, r.randint(600, 820), "#58b889", 13) for x in range(-300, 2300, 170))
    sm, sn = A12._sand()
    mid = sm + "".join(kelp(x + r.randint(-20, 20), r.randint(480, 700), r.choice(("#2f8f5e", "#3a9f6a")), 20) for x in range(-200, 2300, 330))
    near = sn + _pebbles(((500, 1010, 44, "#c9c2b0"), (1560, 1030, 50, "#b9b2a4"))) + _mini(1000, 1050, "white", .15)
    return far, mid, near


def bg_deep(p):
    """The deep blue water: darker, with many empty shells on the bottom."""
    r = random.Random(9)
    far = (A12._under(p, "#4f9fe0", "#173f86") + "".join(A12._stone(x, 860, w, h, "#2f6fb8", "#4a8ad0") for x, w, h in ((180, 300, 240), (1000, 360, 160), (1800, 280, 300)))
           + "".join('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#fff" stroke-width="5" opacity=".45"/>' % (x, y, rr) for x, y, rr in ((300, 300, 14), (340, 220, 9), (1500, 380, 16), (1540, 290, 10), (900, 180, 12))))
    mid = ('<path d="M-500 820 C200 760 700 800 1200 780 S2000 780 2420 810 L2420 900 L-500 900Z" fill="#8fa8c8"/>'
           + "".join(_mini(x, 846 + r.randint(-10, 12), r.choice(("pink", "white", "green", "purple", "gold")), r.choice((.24, .3, .34)), r.random() < .5) for x in range(-240, 2300, 150)))
    near = '<rect x="-500" y="870" width="2920" height="1200" fill="#7f9ac0"/>' + "".join(_mini(x, 1010 + r.randint(0, 40), r.choice(("pink", "white", "purple")), .2, r.random() < .5) for x in range(-200, 2300, 300))
    return far, mid, near


art.BG.update({"shore": lambda p: _shore(p), "shore_eve": lambda p: _shore(p, True), "shellbed": bg_shellbed, "rocks": bg_rocks, "kelp": bg_kelp, "deep": bg_deep})
art.PLACE.update({"shore": "the shallow water", "shore_eve": "the shallow water in the evening", "shellbed": "the shell bed", "rocks": "the big rocks", "kelp": "the kelp forest", "deep": "the deep blue water"})


# ------------------------------------------------------------------ props
def big_shell_peek(p):
    """The huge green shell with Little Crab inside: only his two eyes look out of the opening (-eyes)."""
    c = CRAB; ln = c["line"]
    eyes = ('<g id="%s-eyes">' % p + '<circle cx="-2" cy="-112" r="19" fill="%s"/>' % ln + eye(p + "-e2", -2, -112, 14, lid=c["fill"])
            + '<circle cx="36" cy="-108" r="21" fill="%s"/>' % ln + eye(p + "-e1", 36, -108, 16, lid=c["fill"]) + '</g>')
    return '<g id="%s">%s%s</g>' % (p, _shell("green", 1.0), eyes)


def snail_shell(p):
    """A pink shell that looks just right, but a snail lives in it: -sn (the snail's head and two eyes) comes out of the opening."""
    ln = "#6a4a2a"; sk = "#f2d6a0"
    sn = ('<g id="%s-sn" opacity="0"><path d="M10 -40 C60 -60 150 -50 170 -20 C176 -4 150 0 20 0Z" fill="%s" stroke="%s" stroke-width="9" stroke-linejoin="round"/>'
          '<path d="M120 -44 L112 -118 M150 -40 L160 -112" stroke="%s" stroke-width="20" stroke-linecap="round"/><path d="M120 -44 L112 -118 M150 -40 L160 -112" stroke="%s" stroke-width="9" stroke-linecap="round"/>'
          % (p, sk, ln, ln, sk) + '<circle cx="112" cy="-128" r="22" fill="%s"/>' % ln + eye(p + "-e2", 112, -128, 16, lid=sk) + '<circle cx="160" cy="-122" r="24" fill="%s"/>' % ln + eye(p + "-e1", 160, -122, 18, lid=sk)
          + '<path d="M132 -22 q14 12 28 0" stroke="%s" stroke-width="6" fill="none" stroke-linecap="round"/></g>' % ln)
    return '<g id="%s">%s%s</g>' % (p, sn, _shell("pink", 1.0))


def arrow(p):
    """A fat arrow to the right, anchored at its middle."""
    return '<g id="%s"><path d="M-110 -26 L30 -26 L30 -70 L120 0 L30 70 L30 26 L-110 26Z" fill="#ff8a3d" stroke="%s" stroke-width="10" stroke-linejoin="round"/></g>' % (p, INK)


def sparkle(p):
    star = lambda x, y, r: '<path d="M%d %d L%d %d L%d %d L%d %d L%d %d L%d %d L%d %d L%d %dZ" fill="#fff" stroke="#ffd23f" stroke-width="5" stroke-linejoin="round"/>' % (
        x, y - r, x + r * .25, y - r * .25, x + r, y, x + r * .25, y + r * .25, x, y + r, x - r * .25, y + r * .25, x - r, y, x - r * .25, y - r * .25)
    return '<g id="%s">%s%s%s</g>' % (p, star(0, 0, 44), star(90, -70, 26), star(-80, 50, 22))


def pull_lines(p):
    """Three little effort lines beside someone who pulls hard."""
    return '<g id="%s">' % p + "".join('<path d="M%d %d l%d %d" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".9"/>' % (x, y, dx, dy) for x, y, dx, dy in ((0, 0, 50, -30), (10, 40, 60, 0), (0, 80, 50, 30))) + '</g>'


def think_bulb(p):
    """A light bulb: an idea."""
    return ('<g id="%s"><circle cx="0" cy="-20" r="96" fill="#fff6c9" opacity=".6"/><path d="M-52 -30 C-52 -100 52 -100 52 -30 C52 6 26 14 24 44 L-24 44 C-26 14 -52 6 -52 -30Z" fill="#ffd23f" stroke="%s" stroke-width="10" stroke-linejoin="round"/>'
            '<rect x="-24" y="46" width="48" height="30" rx="8" fill="#b0b6c8" stroke="%s" stroke-width="9"/><path d="M-20 -44 q20 -30 40 0" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" opacity=".8"/></g>' % (p, INK, INK))
