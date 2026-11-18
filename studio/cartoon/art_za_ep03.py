"""Art for za_ep03 "Tumble Shares the Last Drink" (Nov 17 2026): three little birds (Pip, Kiki, Bo), the dry water hole, the rocks with
the crack and its small pool, and the water props (a squirt, drops, rain, clouds, puddles, a smell trail).
Same hand as art.py / art2.py: flat fills, one warm dark outline, big brown eyes, pink cheeks. Nothing here changes an existing character, prop or place.

The birds are drawn from the SIDE (Milo is a round blue bird seen from the front, with a crest and a red scarf): a small body, a round head,
a pointed beak, a wing, a tail, two thin legs. Three colours and three shapes: Pip yellow and round, Kiki coral, slim, with a long tail and a
curl on her head, Bo green, chubby, with two short head feathers. Feet on y = 0, facing right.
Parts: -wing (flaps), -tail, -jaw (the lower beak opens), -eye (-lid), -brow, -smile / -frown (empty: a beak does not smile)."""
import art, art2
from art import INK, eye

PIP = {"fill": "#ffc93c", "shade": "#f0a51e", "belly": "#fff0b8", "line": "#8a5a10", "beak": "#ff7a3c", "beak_d": "#d9571e", "leg": "#d9571e"}
KIKI = {"fill": "#ff7f6e", "shade": "#e05a4e", "belly": "#ffd2c4", "line": "#8a2f2a", "beak": "#5b5560", "beak_d": "#3d3842", "leg": "#5b5560"}
BO = {"fill": "#6fcf97", "shade": "#3fa56e", "belly": "#d8f5c8", "line": "#1f6a45", "beak": "#ffd23f", "beak_d": "#e0a81e", "leg": "#e0a81e"}
WATER = "#58b9e8"; WATER_L = "#bfe6fb"; WATER_D = "#3f9fd0"
ROCK = ("#cdb79c", "#b39c80", "#e3d2ba", "#8f7a62")      # rock: fill, shade, light, line


def bird(pid, c=PIP, shape="round"):
    bw, bh, hr, tail_len = {"round": (92, 84, 70, 86), "slim": (78, 76, 62, 150), "chubby": (104, 92, 76, 56)}[shape]
    hx, hy = (66, -122 - bh - hr * .36); ln = c["line"]
    legs = "".join(f'<path d="M{x} {-bh * .52:.0f} L{x} -6 M{x} -6 l-16 6 M{x} -6 l4 8 M{x} -6 l18 5" stroke="{c["leg"]}" stroke-width="9" fill="none" stroke-linecap="round"/>' for x in (-22, 26))
    ty = -122 - bh * .1
    if shape == "slim": tail_sh = f'<path d="M{-bw + 14} {ty:.0f} L{-bw - tail_len} {ty - 66:.0f} L{-bw - tail_len + 6} {ty - 26:.0f} L{-bw - tail_len - 22} {ty + 4:.0f} L{-bw + 10} {ty + 30:.0f}Z"/>'
    else: tail_sh = f'<path d="M{-bw + 14} {ty:.0f} L{-bw - tail_len} {ty - 50:.0f} L{-bw - tail_len + 4} {ty + 10:.0f} L{-bw + 10} {ty + 34:.0f}Z"/>'
    tail = f'<g id="{pid}-tail">{art2._ol(tail_sh, ln, 7)}<g fill="{c["shade"]}">{tail_sh}</g></g>'
    if shape == "slim": top = f'<path d="M{hx - 6} {hy - hr + 6:.0f} q-6 -44 22 -52 q24 -4 20 18" stroke="{ln}" stroke-width="9" fill="none" stroke-linecap="round"/>'
    elif shape == "chubby": top = f'<path d="M{hx - 14} {hy - hr + 8:.0f} l-12 -40 M{hx + 8} {hy - hr + 4:.0f} l4 -44" stroke="{ln}" stroke-width="11" fill="none" stroke-linecap="round"/>'
    else: top = f'<path d="M{hx - 4} {hy - hr + 6:.0f} q2 -30 -16 -36" stroke="{ln}" stroke-width="9" fill="none" stroke-linecap="round"/>'
    sil = f'<ellipse cx="0" cy="-122" rx="{bw}" ry="{bh}"/><circle cx="{hx}" cy="{hy:.0f}" r="{hr}"/>'
    bx = hx + hr - 10; by = hy + 8                      # where the beak joins the head
    body = (art2._ol(sil, ln, 7) + f'<ellipse cx="0" cy="-122" rx="{bw}" ry="{bh}" fill="{c["fill"]}"/><circle cx="{hx}" cy="{hy:.0f}" r="{hr}" fill="{c["fill"]}"/>'
            f'<ellipse cx="18" cy="-96" rx="{bw * .62:.0f}" ry="{bh * .6:.0f}" fill="{c["belly"]}"/>'
            f'<ellipse cx="{hx - 26}" cy="{hy - hr * .52:.0f}" rx="22" ry="11" fill="#fff" opacity=".3" transform="rotate(-24 {hx - 26} {hy - hr * .52:.0f})"/>')
    wing = (f'<g id="{pid}-wing"><ellipse cx="-22" cy="-126" rx="{bw * .56:.0f}" ry="{bh * .4:.0f}" fill="{c["shade"]}" stroke="{ln}" stroke-width="7" transform="rotate(18 -22 -126)"/>'
            f'<path d="M-58 -104 q10 14 26 12 M-34 -98 q10 12 24 8" stroke="{c["fill"]}" stroke-width="6" fill="none" stroke-linecap="round"/></g>')
    face = (eye(f"{pid}-eye", hx + 18, round(hy - 8), round(hr * .38), lid=c["fill"])
            + f'<path id="{pid}-brow" d="M{hx - 6} {hy - hr * .56:.0f} q22 -14 44 -2" stroke="{ln}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            + f'<ellipse cx="{hx + 30}" cy="{hy + hr * .42:.0f}" rx="13" ry="8" fill="#ff8fb1" opacity=".8"/>'
            + f'<g id="{pid}-jaw"><path d="M{bx} {by + 4:.0f} L{bx + 46} {by + 6:.0f} L{bx + 2} {by + 22:.0f}Z" fill="{c["beak_d"]}" stroke="{ln}" stroke-width="5" stroke-linejoin="round"/></g>'
            + f'<path d="M{bx} {by - 18:.0f} L{bx + 62} {by + 4:.0f} L{bx} {by + 10:.0f}Z" fill="{c["beak"]}" stroke="{ln}" stroke-width="5" stroke-linejoin="round"/>'
            + f'<g id="{pid}-smile"></g><g id="{pid}-frown" opacity="0"></g>')
    sh = '<ellipse cx="0" cy="3" rx="78" ry="11" fill="#000" opacity=".13"/>'
    return f'<g id="{pid}">{sh}{legs}{tail}{top}{body}{wing}{face}</g>'


def _rig(c, shape):
    bw, bh, hr, _ = {"round": (92, 84, 70, 86), "slim": (78, 76, 62, 150), "chubby": (104, 92, 76, 56)}[shape]; hy = -122 - bh - hr * .36
    return dict(build=lambda p: bird(p, c, shape), neck=None, tail=f"{-bw + 12} {-122 - bh * .1:.0f}", ear=None, legs=None, hip=0, jaw=("rot", 20, f"{66 + hr - 10} {hy + 10:.0f}"), eyes=["eye"], brows=["brow"])


art2.RIGS.update({"bird_pip": _rig(PIP, "round"), "bird_kiki": _rig(KIKI, "slim"), "bird_bo": _rig(BO, "chubby")})
# where the parts are, for kit.PT / kit.BOX (the episode file adds them)
BIRD_PT = {"bird_pip": {"head": (66, -231), "body": (0, -122), "top": (66, -310), "beak": (188, -219), "feet": (0, 0), "all": (10, -150)},
           "bird_kiki": {"head": (66, -220), "body": (0, -122), "top": (66, -340), "beak": (180, -208), "feet": (0, 0), "all": (0, -150)},
           "bird_bo": {"head": (66, -241), "body": (0, -122), "top": (66, -365), "beak": (194, -229), "feet": (0, 0), "all": (10, -160)}}
BIRD_BOX = {"bird_pip": (-190, 200, -330), "bird_kiki": (-240, 190, -350), "bird_bo": (-170, 205, -370)}


# ------------------------------------------------------------------ places
def bg_dryhole(p):
    """The water hole after many days without rain: a wide basin of dry, cracked mud on the savanna."""
    far, mid, _ = art2.bg_savanna(p)
    cr = lambda x, y, s, r=0: (f'<g transform="translate({x} {y}) rotate({r}) scale({s})"><path d="M-90 0 L-30 -14 L10 10 L70 -6 M-30 -14 L-44 -44 M10 10 L24 44 M70 -6 L104 -30 M-90 0 L-120 24" '
                              f'stroke="#8a6a40" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    reed = lambda x, y, s: f'<g transform="translate({x} {y}) scale({s})">' + "".join(
        f'<path d="M{k * 16} 0 q{-8 + k * 5} -60 {-18 + k * 14} -112" stroke="#b89a4a" stroke-width="9" fill="none" stroke-linecap="round"/>' for k in range(-2, 3)) + '</g>'
    near = ('<rect x="-500" y="840" width="2920" height="1200" fill="#e0bf5c"/>' + art2._hill("M-500 860 C300 820 900 850 1400 832 S2100 840 2420 850 L2420 900 L-500 900Z", "#e0bf5c")
            + '<ellipse cx="1180" cy="990" rx="800" ry="140" fill="#a88455"/><ellipse cx="1180" cy="984" rx="772" ry="124" fill="#c9a673"/><ellipse cx="1180" cy="1000" rx="560" ry="84" fill="#d6b684"/>'
            + cr(760, 960, 1.0) + cr(1040, 1010, 1.2, 12) + cr(1330, 950, 1.1, -8) + cr(1600, 1000, 1.0, 20) + cr(1180, 930, .8, 4) + cr(900, 1060, .9, -14) + cr(1460, 1060, .9, 6) + cr(1780, 950, .7, -20)
            + reed(330, 900, 1.1) + reed(1960, 930, 1.2) + reed(420, 1090, .9)
            + art2._grass(160, 960, 1.0) + art2._grass(640, 1130, 1.1))
    return far, mid, near


def bg_rocks(p):
    """A pile of big round rocks on the savanna. In the flat rock at the front there is a deep crack (the pool inside it is a prop: pool())."""
    far, _, _ = art2.bg_savanna(p)
    b = lambda x, y, rx, ry, col, hl=True: (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{col}"/>'
                                            + (f'<ellipse cx="{x - rx * .3:.0f}" cy="{y - ry * .55:.0f}" rx="{rx * .34:.0f}" ry="{ry * .16:.0f}" fill="{ROCK[2]}" opacity=".7" transform="rotate(-14 {x - rx * .3:.0f} {y - ry * .55:.0f})"/>' if hl else ""))
    mid = (art2._hill("M-500 720 C200 660 700 700 1200 680 S2000 670 2420 710 L2420 900 L-500 900Z", "#e6cd72")
           + b(1500, 860, 420, 300, "#a8937a") + b(1060, 880, 300, 210, "#b7a288") + b(1840, 880, 300, 250, "#b7a288") + b(60, 880, 330, 190, "#a8937a") + art2._acacia(420, 740, .8))
    near = (f'<rect x="-500" y="850" width="2920" height="1200" fill="{ROCK[0]}"/>'
            + art2._hill("M-500 866 C300 836 900 858 1400 842 S2100 850 2420 858 L2420 910 L-500 910Z", ROCK[0])
            + b(1790, 900, 250, 150, ROCK[1]) + b(1560, 930, 150, 84, ROCK[0]) + b(-60, 930, 260, 130, ROCK[1])
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w * .2:.0f}" fill="{ROCK[1]}" opacity=".55"/>' for x, y, w in ((380, 1030, 120), (1280, 1050, 150), (1680, 1060, 100), (620, 1100, 90)))
            + "".join(f'<path d="M{x} {y} l{dx} 16 l{dx * .7:.0f} -8" stroke="{ROCK[3]}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".55"/>' for x, y, dx in ((1120, 1010, 50), (330, 950, 44), (1440, 990, -46)))
            # the crack: a deep wedge in the rock, dark inside, with a lighter rim
            + '<path d="M768 900 L962 900 L900 1056 L832 1056Z" fill="#4a3a2e"/><path d="M768 900 L832 1056" stroke="#3a2c22" stroke-width="10" stroke-linecap="round"/>'
            + f'<path d="M740 900 L768 900 M962 900 L996 900" stroke="{ROCK[3]}" stroke-width="9" stroke-linecap="round" opacity=".7"/><path d="M962 900 L900 1056" stroke="#6a5644" stroke-width="8" stroke-linecap="round"/>')
    return far, mid, near


art.BG.update({"dryhole": bg_dryhole, "rocks": bg_rocks})
art.PLACE.update({"dryhole": "the dry water hole", "rocks": "the rocks"})


# ------------------------------------------------------------------ props
def pool(pid, level=58):
    """The water inside the crack of bg_rocks. Placed at (866, 1056), the bottom of the crack. #<pid>-lv moves down (y +) as the water goes:
    y = 0 full to the top, 58 the small pool, 170 empty."""
    return (f'<g id="{pid}"><clipPath id="{pid}-c"><path d="M-98 -156 L96 -156 L34 0 L-34 0Z"/></clipPath><g clip-path="url(#{pid}-c)">'
            f'<g id="{pid}-lv" transform="translate(0 {level})"><rect x="-140" y="-146" width="280" height="400" fill="{WATER}"/><path d="M-140 -146 h280" stroke="{WATER_L}" stroke-width="12"/>'
            f'<ellipse cx="-24" cy="-126" rx="26" ry="5" fill="#fff" opacity=".6"/></g></g></g>')


def squirt(pid, dx=200, dy=60, h=120):
    """One squirt of water from the tip of a trunk at (0, 0) to (dx, dy), in an arc."""
    d = f"M0 0 Q{dx * .5:.0f} {-h} {dx} {dy}"
    return (f'<g id="{pid}"><path d="{d}" stroke="{WATER_D}" stroke-width="26" fill="none" stroke-linecap="round"/><path class="{pid}-s" d="{d}" stroke="{WATER}" stroke-width="16" fill="none" stroke-linecap="round"/>'
            f'<path class="{pid}-s" d="{d}" stroke="{WATER_L}" stroke-width="6" fill="none" stroke-linecap="round" stroke-dasharray="30 26"/>'
            + "".join(f'<circle cx="{dx + ox}" cy="{dy + oy}" r="{r}" fill="{WATER}" stroke="{WATER_D}" stroke-width="4"/>' for ox, oy, r in ((-20, -26, 9), (16, -30, 7), (26, -4, 8))) + '</g>')


def drop(pid, s=.3):
    """One drop of water with an outline (art.water_drop has none: it is lost on a pale background)."""
    return (f'<g id="{pid}" transform="scale({s})"><path d="M0 -120 C60 -40 80 0 80 40 A80 80 0 0 1 -80 40 C-80 0 -60 -40 0 -120Z" fill="{WATER}" stroke="{WATER_D}" stroke-width="16" stroke-linejoin="round"/>'
            f'<ellipse cx="-30" cy="30" rx="16" ry="26" fill="#fff" opacity=".7"/></g>')


def drops3(pid, gap=64, s=.26):
    """Three drops side by side: #<pid>-0, -1, -2."""
    return f'<g id="{pid}">' + "".join(f'<g id="{pid}-{k}" transform="translate({(k - 1) * gap} 0)">{drop(pid + "d" + str(k), s)}</g>' for k in range(3)) + '</g>'


def smell(pid, n=3):
    """A smell on the air: wavy blue lines with a tiny drop at the head of each (the smell of water)."""
    out = ""
    for k in range(n):
        y = (k - (n - 1) / 2) * 62
        out += (f'<path d="M0 {y} q40 -28 80 0 q40 28 80 0 q40 -28 80 0" stroke="{WATER}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".9"/>'
                f'<g transform="translate(-26 {y + 6}) scale(.16)">{art.water_drop(pid + "w" + str(k))}</g>')
    return f'<g id="{pid}">{out}</g>'


def cloud(pid, col="#9fb0c4", shade="#8497ae"):
    """A gray rain cloud, about 520 wide, its middle at (0, 0)."""
    return (f'<g id="{pid}"><ellipse cx="0" cy="34" rx="250" ry="62" fill="{shade}"/><circle cx="-130" cy="0" r="86" fill="{col}"/><circle cx="-10" cy="-50" r="118" fill="{col}"/>'
            f'<circle cx="130" cy="-6" r="92" fill="{col}"/><ellipse cx="0" cy="24" rx="240" ry="58" fill="{col}"/><ellipse cx="-40" cy="-110" rx="50" ry="18" fill="#fff" opacity=".35"/></g>')


def rain(pid, w=3400, h=2200):
    """Rain over the whole picture: streaks on a 220 px grid, so a move of 220 px down (and 60 px left) loops without a jump. Its top left is at (0, 0)."""
    out = ""
    for j in range(int(h / 220) + 2):
        for i in range(int(w / 190) + 1):
            x = i * 190 + (95 if j % 2 else 0) + ((i * 37 + j * 53) % 40); y = j * 220 + ((i * 71) % 90)
            out += f'<path d="M{x} {y} l-16 58" stroke="{WATER_L}" stroke-width="9" stroke-linecap="round" opacity=".9"/><path d="M{x} {y} l-16 58" stroke="{WATER}" stroke-width="5" stroke-linecap="round"/>'
    return f'<g id="{pid}">{out}</g>'


def tint(pid, col="#4a6a8a", op=.2):
    """A soft gray-blue light over the picture while it rains."""
    return f'<g id="{pid}"><rect x="-3000" y="-3000" width="6000" height="6000" fill="{col}" opacity="{op}"/></g>'


def puddle(pid, rx=150):
    """A rain puddle on the ground."""
    return (f'<g id="{pid}"><ellipse cx="0" cy="0" rx="{rx}" ry="{rx * .2:.0f}" fill="{WATER_D}"/><ellipse cx="0" cy="-4" rx="{rx * .94:.0f}" ry="{rx * .17:.0f}" fill="{WATER}"/>'
            f'<ellipse cx="{-rx * .3:.0f}" cy="-8" rx="{rx * .3:.0f}" ry="{rx * .04:.0f}" fill="#fff" opacity=".6"/></g>')


def ripple(pid):
    """Small splash rings where a drop lands."""
    return f'<g id="{pid}"><ellipse cx="0" cy="0" rx="46" ry="12" fill="none" stroke="{WATER_L}" stroke-width="7"/><path d="M-30 -14 l-12 -26 M0 -18 l0 -32 M30 -14 l12 -26" stroke="{WATER}" stroke-width="8" stroke-linecap="round"/></g>'


def pond(pid):
    """A small round pond for the fact board."""
    return (f'<g id="{pid}"><ellipse cx="0" cy="0" rx="230" ry="56" fill="{WATER_D}"/><ellipse cx="0" cy="-6" rx="218" ry="48" fill="{WATER}"/>'
            f'<ellipse cx="-70" cy="-16" rx="60" ry="9" fill="#fff" opacity=".6"/></g>')


def num(pid, n, col="#2f80ed"):
    """A number in a round badge (step 1, step 2 on a fact board)."""
    return (f'<g id="{pid}"><circle cx="0" cy="0" r="62" fill="{col}" stroke="#fff" stroke-width="10"/>'
            f'<text x="0" y="30" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="88" fill="#fff">{n}</text></g>')
