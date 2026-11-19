"""Art for za_ep04 "Mango and the Wobbly Vine Bridge" (Nov 18 2026): the little stream with its low vine bridge, the sunny picnic meadow,
the bridge itself (a prop, so it can wobble), the picnic basket and blanket, and Mango holding a vine with her tail (a new kind, "monkey_grip":
the same drawing as art2.monkey(), only the tail goes up and curls round the bridge's rope).
Same hand as art.py / art2.py: flat fills, one warm dark outline. Nothing here changes an existing character, prop or place.

Stage numbers: feet on y = 930 on both banks and on the bridge deck. The stream runs between x = 820 and x = 1340; the bridge is placed at
(1080, 930) and is 640 wide; its rope (drawn in the place, behind the actors) is at y = 760, the height of Mango's curled tail tip at scale .55."""
import art, art2, kit
from art import INK, SUN

MON = art2.MON
WATER = "#58b9e8"; WATER_L = "#bfe6fb"; WATER_D = "#3f9fd0"
WOOD = ("#b07a42", "#8a5a2c", "#d29a5c")
VINE = ("#4f9e4c", "#2f7a3a")
DECK_Y = 930; ROPE_Y = 760; BX0, BX1 = 760, 1400      # the bridge from post to post


def _limb(d, w=30, c=MON):
    return f'<path d="{d}" stroke="{c["line"]}" stroke-width="{w + 16}" fill="none" stroke-linecap="round"/><path d="{d}" stroke="{c["fur"]}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'


# ------------------------------------------------------------------ Mango holding the rope with her tail
GRIP_TAIL = "M40 -80 C150 -70 190 -170 160 -250 C146 -290 132 -322 154 -334 C180 -346 200 -312 180 -292 C164 -278 140 -286 142 -304"
GRIP_AT = (166, -310)      # the middle of the curl, in her own units: put the rope through here


def monkey_grip(pid):
    s = art2.monkey(pid)
    old = "M40 -80 C170 -60 226 -180 176 -262 C146 -310 92 -288 108 -244"
    assert old in s
    s = s.replace(old, GRIP_TAIL)
    # a short piece of rope over the back of the curl, so the tail is wrapped round it, not lying on it
    rope = (f'<path d="M150 -304 L184 -312" stroke="{VINE[1]}" stroke-width="24" stroke-linecap="round"/>'
            f'<path d="M150 -304 L184 -312" stroke="{VINE[0]}" stroke-width="12" stroke-linecap="round"/>')
    return s.replace(f'<g id="{pid}-body">', rope + f'<g id="{pid}-body">', 1)


art2.RIGS["monkey_grip"] = dict(art2.RIGS["monkey"], build=monkey_grip)
kit.PT["monkey_grip"] = dict(kit.PT["monkey"], grip=GRIP_AT)
kit.BOX["monkey_grip"] = (-170, 230, -430)


# ------------------------------------------------------------------ places
def _bank_edge(x0, sgn):
    """The earth edge of a bank where it drops to the water (sgn 1: the left bank, its edge on the right)."""
    return (f'<path d="M{x0} 900 C{x0 + 30 * sgn} 980 {x0 + 10 * sgn} 1080 {x0 - 40 * sgn} 1980" stroke="#8a6238" stroke-width="44" fill="none"/>'
            f'<path d="M{x0} 900 C{x0 + 30 * sgn} 980 {x0 + 10 * sgn} 1080 {x0 - 40 * sgn} 1980" stroke="#a8784a" stroke-width="18" fill="none"/>')


def bg_stream(p):
    """The little stream in the jungle: two grassy banks, clear water between them, and the low vine bridge's two posts and rope.
    The deck of the bridge is a prop (bridge()), so it can wobble; the posts and the rope stay still."""
    far, mid, _ = art2.bg_jungle(p)
    water = (f'<path d="M820 900 C850 1000 830 1100 780 1980 L1380 1980 C1330 1100 1310 1000 1340 900Z" fill="{WATER}"/>'
             f'<path d="M860 960 C910 1100 890 1300 850 1980 L960 1980 C960 1300 960 1100 910 960Z" fill="{WATER_D}" opacity=".35"/>'
             + "".join(f'<path id="{p}w{k}" d="M{x} {y} q24 -12 48 0 q24 12 48 0" stroke="{WATER_L}" stroke-width="8" fill="none" stroke-linecap="round"/>'
                       for k, (x, y) in enumerate(((920, 990), (1160, 1030), (1020, 1110), (1200, 1180), (880, 1250), (1100, 1300)))))
    stones = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .55:.0f}" fill="#9aa3a8" stroke="#6d777c" stroke-width="6"/>' for x, y, r in ((860, 1180, 30), (1300, 1120, 28), (1280, 1330, 36)))
    post = lambda x: (f'<rect x="{x - 22}" y="{ROPE_Y - 40}" width="44" height="{DECK_Y - ROPE_Y + 70}" rx="14" fill="{WOOD[0]}" stroke="{INK}" stroke-width="8"/>'
                      f'<circle cx="{x}" cy="{ROPE_Y - 40}" r="26" fill="{WOOD[2]}" stroke="{INK}" stroke-width="8"/>')
    rope = (f'<path d="M{BX0} {ROPE_Y} Q1080 {ROPE_Y + 14} {BX1} {ROPE_Y}" stroke="{VINE[1]}" stroke-width="24" fill="none" stroke-linecap="round"/>'
            f'<path d="M{BX0} {ROPE_Y} Q1080 {ROPE_Y + 14} {BX1} {ROPE_Y}" stroke="{VINE[0]}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            + "".join(f'<path d="M{x} {ROPE_Y + 6} q-10 30 4 56" stroke="{VINE[0]}" stroke-width="7" fill="none" stroke-linecap="round"/>'
                      f'<path d="M{x + 4} {ROPE_Y + 60} c-24 -8 -30 14 -10 20 c16 4 22 -12 10 -20Z" fill="#57c078"/>' for x in (840, 1000, 1180, 1330)))
    # the picnic spot on the far bank: a little blanket and a flag
    spot = ('<path d="M1500 960 L1760 950 L1800 1010 L1480 1022Z" fill="#ff6f6f" stroke="#a83a3a" stroke-width="7" stroke-linejoin="round"/>'
            + "".join(f'<path d="M{1500 + k * 60} 958 L{1485 + k * 76} 1020" stroke="#fff" stroke-width="10" opacity=".8"/>' for k in range(1, 5))
            + f'<rect x="1706" y="820" width="10" height="150" fill="{WOOD[1]}"/><path d="M1716 824 L1790 846 L1716 870Z" fill="{SUN}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    near = ('<rect x="-500" y="850" width="2920" height="1200" fill="#4aa85a"/><path d="M-500 870 C300 836 900 860 1400 846 S2100 850 2420 862 L2420 900 L-500 900Z" fill="#4aa85a"/>'
            + water + stones + _bank_edge(820, 1) + _bank_edge(1340, -1)
            + art2._leaf(-40, 900, 1.5, -40, "#2f8a4c") + art2._leaf(60, 930, 1.3, -80, "#3f9e5c") + art2._leaf(2020, 930, 1.5, -130, "#2f8a4c")
            + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="{c}"/><circle cx="{x}" cy="{y}" r="5" fill="#fff6c0"/>' for x, y, c in ((260, 1000, "#ff7aa2"), (420, 1080, "#ffb347"), (1520, 1060, "#ff7aa2"), (1720, 1100, "#fff")))
            + post(BX0) + post(BX1) + rope + spot)
    return far, mid, near


def bg_meadow(p):
    """The sunny picnic meadow on the far side of the stream: soft grass, flowers, the jungle behind, the stream glinting at the back."""
    far = art._sky(p, "#9fe0ff", "#eafbe0", y1=1100) + art._sun(p + "sun", 1560, 170, 80) + art._cloud(p + "c1", 420, 170, .9) + art._cloud(p + "c2", 1000, 110, .6) + \
        "".join(art2._jtree(x, w, "#6f9a72", 1700) for x, w in ((80, 70), (430, 50), (1780, 76))) + \
        "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#8fc98f"/>' for x, y, rx, ry in ((120, 260, 330, 170), (520, 300, 280, 150), (1840, 280, 360, 180)))
    mid = ('<path d="M-500 700 C200 660 800 690 1300 672 S2100 676 2420 700 L2420 900 L-500 900Z" fill="#7ccf6e"/>'
           f'<path d="M-500 760 C200 744 700 770 1200 750 S2000 752 2420 770 L2420 800 C1900 790 1300 800 800 796 S-100 786 -500 800Z" fill="{WATER}"/>'
           f'<path d="M100 772 q30 -10 60 0 M700 778 q30 -10 60 0 M1500 770 q30 -10 60 0" stroke="{WATER_L}" stroke-width="7" fill="none" stroke-linecap="round"/>'
           + art2._leaf(1760, 760, .9, -120, "#3f9e5c") + art2._leaf(300, 740, .8, -60, "#3f9e5c"))
    near = ('<rect x="-500" y="840" width="2920" height="1200" fill="#6cc463"/><path d="M-500 860 C300 826 900 850 1400 836 S2100 840 2420 852 L2420 900 L-500 900Z" fill="#6cc463"/>'
            + "".join(f'<g transform="translate({x} {y})"><path d="M0 0 v-30" stroke="#3f9e5c" stroke-width="6"/>' + "".join(f'<circle cx="{12 * dx}" cy="{-30 + 12 * dy}" r="10" fill="{c}"/>' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) + f'<circle cx="0" cy="-30" r="8" fill="#fff6c0"/></g>'
                      for x, y, c in ((120, 990, "#ff7aa2"), (380, 1100, "#fff"), (1700, 1000, "#ffb347"), (1880, 1110, "#ff7aa2"), (1460, 1130, "#fff"), (240, 1180, "#ffb347")))
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="7" fill="#58b052" opacity=".7"/>' for x, y, w in ((300, 1030, 100), (1300, 980, 120), (1600, 1060, 80))))
    return far, mid, near


art.BG.update({"stream": bg_stream, "meadow": bg_meadow})
art.PLACE.update({"stream": "the stream with the vine bridge", "meadow": "the picnic meadow"})


# ------------------------------------------------------------------ props
def bridge(pid):
    """The deck of the low vine bridge, placed at (1080, 930): wooden planks tied with vines, its top edge at y = 0 (the actors' feet).
    -deck is the planks: a little rotation and y on it make the wobble."""
    w = (BX1 - BX0) / 2; planks = []
    x = -w + 10
    while x < w - 30:
        planks.append(f'<rect x="{x:.0f}" y="0" width="44" height="30" rx="6" fill="{WOOD[0] if len(planks) % 2 else WOOD[2]}" stroke="{INK}" stroke-width="6"/>'); x += 52
    ties = (f'<path d="M{-w} 6 L{w} 6" stroke="{VINE[1]}" stroke-width="14" stroke-linecap="round"/><path d="M{-w} 24 L{w} 24" stroke="{VINE[1]}" stroke-width="10" stroke-linecap="round"/>')
    hang = "".join(f'<path d="M{x} 30 q8 30 -4 52" stroke="{VINE[0]}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M{x - 4} 80 c-22 -6 -26 14 -8 18 c14 4 20 -10 8 -18Z" fill="#57c078"/>' for x in (-240, -90, 60, 220))
    return f'<g id="{pid}"><g id="{pid}-deck">{ties}{"".join(planks)}{hang}</g></g>'


def basket(pid, n=3, tip=False):
    """The picnic basket: wicker, a handle, n golden fruits on top (art2.fruit). (0, 0) is the middle of its bottom."""
    fr = "".join(f'<g transform="translate({x} {-130}) scale(.5)">{art2.fruit(f"{pid}-f{k}")}</g>' for k, x in enumerate((-60, 0, 60)[:n]))
    weave = "".join(f'<path d="M{-110 + k * 10} {-110 + k * 26} H{110 - k * 10}" stroke="#a8743a" stroke-width="8"/>' for k in range(4))
    body = (f'<path d="M-130 -120 L130 -120 L104 0 L-104 0Z" fill="#d9a35c" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>{weave}'
            f'<path d="M-140 -126 H140" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-140 -126 H140" stroke="#e8b874" stroke-width="10" stroke-linecap="round"/>')
    handle = f'<path d="M-96 -126 C-96 -260 96 -260 96 -126" stroke="{INK}" stroke-width="22" fill="none"/><path d="M-96 -126 C-96 -260 96 -260 96 -126" stroke="#c48a46" stroke-width="10" fill="none"/>'
    return f'<g id="{pid}">{handle}{fr}{body}</g>'


def fruit(pid, s=1.0): return art2.fruit(pid, s)


def blanket(pid):
    """A red-and-white picnic blanket seen from the front, lying on the grass. (0, 0) is its middle."""
    q = "M-420 -70 L400 -80 L470 90 L-470 100Z"
    lines = "".join(f'<path d="M{-420 + k * 164} {-70 - k * 2} L{-470 + k * 188} {100 - k * 2}" stroke="#fff" stroke-width="22" opacity=".85"/>' for k in range(1, 5))
    lines += '<path d="M-444 -4 L436 -10" stroke="#fff" stroke-width="22" opacity=".85"/>'
    return f'<g id="{pid}"><path d="{q}" fill="#ff6f6f" stroke="#a83a3a" stroke-width="9" stroke-linejoin="round"/>{lines}</g>'


def wobble_lines(pid):
    """Little curved lines that say: it wobbles."""
    return (f'<g id="{pid}">' + "".join(f'<path d="M{x} -40 q-16 40 0 80" stroke="{INK}" stroke-width="9" fill="none" stroke-linecap="round" opacity=".7"/>' for x in (-40, 40)) + '</g>')


def bridge_pic(pid):
    """The vine bridge, small, inside a thought bubble."""
    return (f'<g id="{pid}"><path d="M-130 70 C-110 110 -100 120 -90 130 L90 130 C100 120 110 110 130 70Z" fill="{WATER}"/>'
            f'<rect x="-150" y="30" width="300" height="20" rx="6" fill="{WOOD[0]}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-156" y="-30" width="14" height="80" fill="{WOOD[1]}"/><rect x="142" y="-30" width="14" height="80" fill="{WOOD[1]}"/>'
            f'<path d="M-150 -24 Q0 -10 150 -24" stroke="{VINE[0]}" stroke-width="9" fill="none"/>'
            f'<path d="M60 -70 L150 -74 L160 -40 L50 -36Z" fill="#ff6f6f" stroke="#a83a3a" stroke-width="5"/></g>')


def stepnum(n, col=SUN):
    """A step number (a round badge)."""
    def f(pid):
        return (f'<g id="{pid}"><circle r="50" fill="{col}" stroke="{INK}" stroke-width="9"/>'
                f'<text x="0" y="24" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="70" fill="{INK}">{n}</text></g>')
    return f
