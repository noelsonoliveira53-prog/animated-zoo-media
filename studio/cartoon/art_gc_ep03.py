"""Art for gc_ep03 "Where Does Rain Come From?" (Gizmo Explains, Nov 27 2026): two new places (gpark: a sunny park path after the rain, with room
for a puddle; ghills: green hills under a big sky with a river that winds downhill into a lake and the sea) and the props of the water cycle
(a puddle that shrinks, water vapor drawn as little dots because it is invisible, a cloud that turns grey and rains or snows, a speck of dust a
tiny drop forms on, tiny drops that join into a big one, a winter window with drops on the inside of the glass, the water-cycle circle).
Registered from here the way art_gizmo.py does: nothing that exists changes. Props are drawn around (0, 0)."""
import math
import art, art2, kit
from art import INK, SUN
from art_gizmo import NAVY, SCREEN, CYAN, ACC, ORANGE, SILVER, STEEL, B1, B2, GREEN, _grad, _flower, warm_sun, drop

WATER = "#7fd0f5"; WLINE = "#2f80c0"; DEEP = "#3d8de0"; VAP = "#ffffff"; GREY = "#9aa6bd"; GREYD = "#7d8aa3"


def _cloud_shape(fill, o=1.0, extra=""):
    return (f'<g opacity="{o}" {extra}><ellipse cx="0" cy="20" rx="230" ry="70" fill="{fill}"/><ellipse cx="-100" cy="-30" rx="120" ry="90" fill="{fill}"/>'
            f'<ellipse cx="60" cy="-60" rx="140" ry="110" fill="{fill}"/><ellipse cx="170" cy="0" rx="90" ry="70" fill="{fill}"/><ellipse cx="-190" cy="20" rx="70" ry="55" fill="{fill}"/></g>')


# ================================================================== places
def bg_gpark(p):
    """A sunny park after the rain: blue sky, the sun high on the right, round trees, a bench, a wide grey path where the puddle (a prop) lies."""
    far = (_grad(f"{p}s", B2, "#bfe6ff") + f'<rect x="-600" y="-900" width="3120" height="1700" fill="url(#{p}s)"/>'
           + f'<ellipse cx="420" cy="150" rx="130" ry="40" fill="#fff"/><ellipse cx="500" cy="124" rx="80" ry="38" fill="#fff"/><ellipse cx="1150" cy="90" rx="100" ry="32" fill="#fff" opacity=".9"/>'
           + f'<path d="M-600 600 C-100 500 400 540 900 560 S1800 500 2520 560 V800 H-600Z" fill="#8fd08a"/>')
    tree = lambda x, y, s: (f'<g transform="translate({x} {y}) scale({s})"><rect x="-22" y="-160" width="44" height="170" rx="12" fill="#8a5a32"/>'
                            f'<circle cx="0" cy="-230" r="120" fill="#4fae4a"/><circle cx="-80" cy="-180" r="80" fill="#5fbf5a"/><circle cx="80" cy="-190" r="86" fill="#57b552"/></g>')
    mid = (f'<path d="M-600 680 C200 640 900 670 1500 650 S2200 660 2520 660 V900 H-600Z" fill="#6cc070"/>'
           + tree(-250, 700, 1.0) + tree(150, 690, .8) + tree(1900, 690, .95) + tree(2250, 700, .8)
           + f'<g transform="translate(1720 760)"><rect x="-130" y="-70" width="260" height="22" rx="8" fill="#c98a4a" stroke="#7a4d2b" stroke-width="5"/>'
           f'<rect x="-130" y="-40" width="260" height="22" rx="8" fill="#c98a4a" stroke="#7a4d2b" stroke-width="5"/><rect x="-110" y="-20" width="16" height="40" fill="#555"/><rect x="94" y="-20" width="16" height="40" fill="#555"/></g>')
    near = (f'<rect x="-600" y="780" width="3120" height="1300" fill="#5fb85f"/>'
            + f'<path d="M-600 840 C200 820 1200 830 2520 860 V1060 C1200 1040 200 1030 -600 1050Z" fill="#c9ced8"/>'
            + f'<path d="M-600 846 C200 826 1200 836 2520 866" stroke="#aab1bf" stroke-width="8" fill="none"/>'
            + "".join(_flower(x, y, .8, c) for x, y, c in ((-350, 1150, "#ff7aa2"), (60, 1170, SUN), (1600, 1160, ACC), (2100, 1150, "#fff")))
            + "".join(f'<path d="M{x} 1200 l-8 -34 M{x + 10} 1200 l2 -40 M{x + 20} 1200 l12 -30" stroke="#3f9e3c" stroke-width="7" stroke-linecap="round"/>' for x in range(-560, 2500, 110)))
    return far, mid, near


def bg_ghills(p):
    """Green hills under a big sky: a tall hill on the left, a blue river that winds down from it to a lake and the sea on the right."""
    far = (_grad(f"{p}s", "#5f8fe0", "#cfe9ff") + f'<rect x="-600" y="-900" width="3120" height="1800" fill="url(#{p}s)"/>'
           + f'<path d="M-600 560 L-100 120 L250 420 L520 200 L900 560Z" fill="#7fb6d9" opacity=".7"/>'
           + f'<path d="M-100 120 L-30 180 L-100 210 L-170 180Z M520 200 L580 250 L520 270 L460 250Z" fill="#fff" opacity=".9"/>')
    mid = (f'<path d="M-600 700 C-300 420 100 300 500 460 C800 580 1100 600 1500 620 S2200 640 2520 640 V900 H-600Z" fill="#74c06f"/>'
           + f'<path d="M1500 650 C1800 640 2200 640 2520 650 V760 H1400Z" fill="{DEEP}"/>'            # the sea, far right
           + f'<path d="M1500 652 C1800 642 2200 642 2520 652" stroke="#bfe6ff" stroke-width="6" fill="none"/>')
    river = "M200 430 C320 520 260 600 420 660 C600 730 760 700 900 770 C1050 840 1250 820 1420 760 C1500 730 1560 700 1620 680"
    near = (f'<path d="M-600 760 C200 720 900 760 1500 740 S2200 760 2520 750 V2100 H-600Z" fill="#62b85a"/>'
            + f'<path d="{river}" stroke="{WLINE}" stroke-width="64" fill="none" stroke-linecap="round"/><path d="{river}" stroke="{WATER}" stroke-width="44" fill="none" stroke-linecap="round"/>'
            + f'<ellipse cx="1660" cy="700" rx="150" ry="40" fill="{WATER}" stroke="{WLINE}" stroke-width="10"/>'
            + "".join(_flower(x, y, .8, c) for x, y, c in ((-300, 980, "#ff7aa2"), (300, 1010, SUN), (1300, 1000, ACC), (2000, 980, "#fff")))
            + "".join(f'<path d="M{x} 1060 l-8 -34 M{x + 10} 1060 l2 -40 M{x + 20} 1060 l12 -30" stroke="#3f9e3c" stroke-width="7" stroke-linecap="round"/>' for x in range(-560, 2500, 110)))
    return far, mid, near


art.BG.update({"gpark": bg_gpark, "ghills": bg_ghills})
art.PLACE.update({"gpark": "the sunny park after the rain", "ghills": "the hills with a river"})


# ================================================================== props
def puddle(pid):
    """A puddle on the path (it shrinks with a scale tween around its middle): -sky is the bit of sky it reflects."""
    return (f'<g id="{pid}"><ellipse cx="0" cy="0" rx="300" ry="70" fill="{WATER}" stroke="{WLINE}" stroke-width="10"/>'
            f'<g id="{pid}-sky"><ellipse cx="-80" cy="-12" rx="110" ry="20" fill="#fff" opacity=".7"/><ellipse cx="120" cy="16" rx="60" ry="12" fill="#fff" opacity=".5"/></g></g>')


def vapor(pid, n=5, h=360):
    """Water vapor, drawn as little dots (it is invisible: the episode says so): n wavy columns of small white dots rising from y = 0 to y = -h.
    The engine fades -v in and moves it up (the columns rise)."""
    cols = ""
    for c in range(n):
        x0 = (c - (n - 1) / 2) * 90
        cols += "".join(f'<circle cx="{x0 + 22 * math.sin(k * 1.1 + c):.0f}" cy="{-k * h / 9:.0f}" r="{12 - k * .7:.1f}" fill="{VAP}" stroke="{WLINE}" stroke-width="3" opacity="{1 - k * .07:.2f}"/>' for k in range(9))
    return f'<g id="{pid}"><g id="{pid}-v" opacity="0">{cols}</g></g>'


def cloud(pid):
    """A big white cloud; -grey turns it into a heavy grey rain cloud (opacity), -rain is a field of falling drops under it, -snow a field of
    snowflakes (both opacity 0; the engine moves them down)."""
    rain = "".join(f'<path d="M{x} {y} c10 16 14 24 14 32 a14 14 0 0 1 -28 0 c0 -8 4 -16 14 -32z" fill="{WATER}" stroke="{WLINE}" stroke-width="4"/>'
                   for x, y in ((-180, 120), (-100, 180), (-20, 130), (60, 200), (140, 140), (200, 220), (-140, 260), (0, 280), (100, 300), (-60, 340), (180, 360), (-200, 380)))
    snow = "".join(f'<g transform="translate({x} {y})">' + "".join(f'<path d="M0 0 L0 -20" stroke="#fff" stroke-width="7" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 60)) + '</g>'
                   for x, y in ((-170, 130), (-80, 200), (10, 140), (90, 230), (170, 150), (-130, 300), (40, 320), (150, 330), (-30, 380)))
    return (f'<g id="{pid}"><g id="{pid}-rain" opacity="0">{rain}</g><g id="{pid}-snow" opacity="0">{snow}</g>'
            + _cloud_shape("#ffffff") + f'<g id="{pid}-grey" opacity="0">{_cloud_shape(GREY)}<ellipse cx="0" cy="40" rx="210" ry="40" fill="{GREYD}"/></g></g>')


def speck(pid):
    """A tiny speck of dust (brown, rough) seen big; -drop is the tiny drop of water that forms around it (opacity 0)."""
    return (f'<g id="{pid}"><g id="{pid}-drop" opacity="0"><circle r="120" fill="{WATER}" stroke="{WLINE}" stroke-width="10" opacity=".85"/>'
            f'<ellipse cx="-42" cy="-48" rx="22" ry="34" fill="#fff" opacity=".8" transform="rotate(30 -42 -48)"/></g>'
            f'<path d="M-40 -10 L-20 -38 L14 -34 L40 -8 L34 26 L4 40 L-30 30Z" fill="#a0784a" stroke="#5e4226" stroke-width="8" stroke-linejoin="round"/>'
            f'<circle cx="-6" cy="-10" r="7" fill="#5e4226"/><circle cx="16" cy="12" r="5" fill="#5e4226"/></g>')


def dots_cloud(pid):
    """Lots of tiny drops (-dots, blue dots filling the cloud's shape) and the cloud they make (-cl, opacity 0)."""
    blobs = ((0, 20, 230, 70), (-100, -30, 120, 90), (60, -60, 140, 110), (170, 0, 90, 70), (-190, 20, 70, 55))
    pts = []
    for k in range(400):
        x, y = ((k * 137) % 500) - 250, ((k * 89) % 300) - 170
        if any(((x - bx) / rx) ** 2 + ((y - by) / ry) ** 2 < .8 for bx, by, rx, ry in blobs) and all((x - a) ** 2 + (y - b) ** 2 > 900 for a, b in pts): pts.append((x, y))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="{WATER}" stroke="{WLINE}" stroke-width="3"/>' for x, y in pts)
    return f'<g id="{pid}"><g id="{pid}-cl" opacity="0">{_cloud_shape("#ffffff")}</g><g id="{pid}-dots">{dots}</g></g>'


def join(pid):
    """Tiny drops that join into one big drop: -a and -b (small drops left and right) move together, -big (opacity 0) is the bigger drop."""
    sm = lambda x, i: f'<g id="{pid}-{i}"><g transform="translate({x} 0) scale(.8)">{drop(pid + "x" + i)}</g></g>'
    return (f'<g id="{pid}">{sm(-170, "a")}{sm(170, "b")}<g id="{pid}-c"><g transform="translate(0 -150) scale(.7)">{drop(pid + "xc")}</g></g>'
            f'<g id="{pid}-big" opacity="0"><g transform="scale(1.7)">{drop(pid + "xbig")}</g></g></g>')


def winter_window(pid):
    """The lab window on a cold winter day (covers the window of gwindow, centre (960, 350)): grey sky, snow on the ground outside, snowflakes;
    -drops are drops of water on the INSIDE of the glass (opacity 0)."""
    flakes = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" opacity=".9"/>' for x, y in ((-460, -300), (-300, -180), (-120, -320), (60, -220), (220, -330), (400, -200), (-380, 60), (-200, -40), (300, 20), (480, -60), (120, 80), (-40, 140)))
    drops = "".join(f'<path d="M{x} {y} c8 13 11 19 11 25 a11 11 0 0 1 -22 0 c0 -6 3 -12 11 -25z" fill="#dff4ff" stroke="#8fb8d8" stroke-width="3" opacity=".95"/>'
                    for x, y in ((-500, 200), (-440, 260), (-470, 330), (-360, 300), (-260, 340), (-150, 310), (-40, 350), (80, 320), (190, 345), (300, 300), (420, 335), (500, 280), (-400, 160), (460, 180), (-200, 250), (240, 240)))
    return (f'<g id="{pid}"><rect x="-580" y="-410" width="1160" height="780" fill="#c3cfdf"/><rect x="-580" y="-410" width="1160" height="400" fill="#aebbd0"/>'
            f'<path d="M-580 200 C-300 150 0 170 300 150 S520 160 580 170 V370 H-580Z" fill="#f4f8ff"/>{flakes}'
            f'<rect x="-600" y="-430" width="1200" height="820" fill="none" stroke="{SILVER}" stroke-width="40"/><path d="M0 -430 V390 M-600 -20 H600" stroke="{SILVER}" stroke-width="24"/>'
            f'<g id="{pid}-drops" opacity="0">{drops}</g></g>')


def snowflake(pid):
    """One big snowflake."""
    arm = '<path d="M0 0 V-120 M0 -70 l-30 -30 M0 -70 l30 -30 M0 -40 l-22 -22 M0 -40 l22 -22" stroke="#fff" stroke-width="16" stroke-linecap="round" fill="none"/>'
    return f'<g id="{pid}">' + "".join(f'<g transform="rotate({a})"><g stroke="{WLINE}">{arm.replace("#fff", WLINE).replace("16", "26")}</g>{arm}</g>' for a in range(0, 360, 60)) + '</g>'


def flow(pid, pts, col=ACC):
    """Little arrows along a path (the way the water goes): -a0, -a1, ... shown one after another."""
    out = ""
    for k, (x1, y1, x2, y2) in enumerate(pts): out += f'<g id="{pid}-a{k}" opacity="0">{art.arrow(pid + f"x{k}", x1, y1, x2, y2, col)}</g>'
    return f'<g id="{pid}">{out}</g>'


def wcycle(pid):
    """The water cycle as a circle of four pictures with arrows between (clockwise on screen): -k0 the sun warms the water (bottom), -k1 the vapor
    rises (left), -k2 the cloud (top), -k3 the rain falls (right)."""
    pos = ((0, 300), (-330, 0), (0, -300), (330, 0))
    ring = "".join(f'<path d="M{a[0] * .7 + b[0] * .3:.0f} {a[1] * .7 + b[1] * .3:.0f} Q{(a[0] + b[0]) * .62:.0f} {(a[1] + b[1]) * .62:.0f} {a[0] * .3 + b[0] * .7:.0f} {a[1] * .3 + b[1] * .7:.0f}" stroke="{ACC}" stroke-width="16" fill="none" stroke-linecap="round"/>'
                   for a, b in zip(pos, pos[1:] + pos[:1]))
    heads = "".join(f'<circle cx="{a[0] * .3 + b[0] * .7:.0f}" cy="{a[1] * .3 + b[1] * .7:.0f}" r="18" fill="{ACC}"/>' for a, b in zip(pos, pos[1:] + pos[:1]))
    wave = f'<path d="M-90 40 q22 -18 45 0 t45 0 t45 0 t45 0 V80 H-90Z" fill="{WATER}" stroke="{WLINE}" stroke-width="6"/>'
    pics = [f'<g transform="translate(-30 -40) scale(.32)">{warm_sun(pid + "s")}</g>{wave}',
            f'<g transform="translate(0 70)">{vapor(pid + "v", 3, 160).replace(" opacity=\"0\"", "")}</g>',
            f'<g transform="scale(.42)">{_cloud_shape("#ffffff", 1, "stroke=\"" + WLINE + "\" stroke-width=\"8\"")}</g>',
            f'<g transform="translate(0 -40) scale(.35)">{_cloud_shape(GREY)}</g>' + "".join(f'<path d="M{x} {y} c6 10 8 14 8 19 a8 8 0 0 1 -16 0 c0 -5 2 -9 8 -19z" fill="{WATER}" stroke="{WLINE}" stroke-width="3"/>' for x, y in ((-40, 10), (0, 30), (40, 10), (-20, 60), (24, 66)))]
    body = "".join(f'<g id="{pid}-k{k}" transform="translate({x} {y})"><circle r="128" fill="#fff" stroke="{NAVY}" stroke-width="10"/>{pics[k]}</g>' for k, (x, y) in enumerate(pos))
    return f'<g id="{pid}">{ring}{heads}{body}</g>'


def sea(pid):
    """A strip of sea with little waves (for the board: water that the sun warms)."""
    return (f'<g id="{pid}"><path d="M-420 0 q35 -26 70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 V160 H-420Z" fill="{WATER}" stroke="{WLINE}" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M-300 70 h120 M60 100 h140" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".8"/></g>')


def heat(pid):
    """Three soft warm wavy lines (the sun's heat), opacity 0 (-h)."""
    return f'<g id="{pid}"><g id="{pid}-h" opacity="0">' + "".join(f'<path d="M{x} 0 q-20 -40 0 -80 t0 -80" stroke="#ffb020" stroke-width="16" fill="none" stroke-linecap="round"/>' for x in (-90, 0, 90)) + '</g></g>'
