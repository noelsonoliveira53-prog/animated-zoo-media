"""Week-2 art for Bloop's Color Lab: numbers 6-10, color mixing, opposites, 3D shapes, patterns & sorting,
light/dark shades, white, rainbow order and a green color hunt.
Same 1080x1100 frame and lab background as art_bloop.py (floor at ~y1000). Every key starts with "bl2_".
Each scene: <g id="animal"> (the friend), <g id="fx" opacity="0"> (first reveal), <g id="fx2" opacity="0"> (second reveal)."""
import math
from art_bloop import svg, lab_env, face, ball, heart_path, star_path, RAINBOW

DARK = {"#ff5c5c": "#e03131", "#ffa94d": "#e8590c", "#ffd43b": "#f59f00", "#69db7c": "#2f9e44", "#4dabf7": "#1c7ed6", "#9775fa": "#6741d9",
        "#f783ac": "#d6336c"}
INK = "#3d2a7a"


def f(x):
    return f"{x:.0f}"


def frame(body, fx="", fx2="", defs=""):
    return svg((f'<defs>{defs}</defs>' if defs else '') + lab_env()
               + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')


# ---------- the jelly friend (same body as art_bloop.blob, but movable/scalable) ----------
BLOB_D = "M-280 0 Q-340 -290 -210 -430 Q-100 -560 20 -540 Q180 -520 250 -390 Q340 -230 280 0Z"


def jelly(cx, by, s, color, dark, mouth=INK):
    return (f'<g transform="translate({f(cx)} {f(by)}) scale({s})">'
            f'<path d="{BLOB_D}" fill="{color}" stroke="{dark}" stroke-width="{10 / s:.1f}"/>'
            f'<ellipse cx="-110" cy="-390" rx="60" ry="34" fill="#fff" opacity=".45" transform="rotate(-30 -110 -390)"/>'
            + face(5, -300, 1.25, mouth) + '</g>')


def tface(cx, cy, s=1.0, mouth=INK, eye="#1a1a2e"):
    e = 12 * s
    return (f'<circle cx="{f(cx - e)}" cy="{f(cy)}" r="{5 * s:.1f}" fill="{eye}"/><circle cx="{f(cx + e)}" cy="{f(cy)}" r="{5 * s:.1f}" fill="{eye}"/>'
            f'<path d="M{f(cx - 9 * s)} {f(cy + 10 * s)} q{f(9 * s)} {f(8 * s)} {f(18 * s)} 0" stroke="{mouth}" stroke-width="{3.5 * s:.1f}" fill="none" stroke-linecap="round"/>')


def star(cx, cy, r, c="#ffd43b", d="#f59f00", sw=5):
    return f'<path d="{star_path(cx, cy, r, r * .45)}" fill="{c}" stroke="{d}" stroke-width="{sw}" stroke-linejoin="round"/>'


def dashed(path, c="#ffd43b"):
    return f'<path d="{path}" fill="none" stroke="{c}" stroke-width="16" stroke-dasharray="34 18" stroke-linejoin="round" stroke-linecap="round"/>'


def puff(circles, c, d, sw=5):
    """cloud/wool made of circles with one clean outline"""
    return ("".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r + sw)}" fill="{d}"/>' for x, y, r in circles)
            + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{c}"/>' for x, y, r in circles))


# ---------- little things ----------
def apple_s(cx, cy, c="#ff5c5c", d="#e03131"):
    return (f'<rect x="{cx - 3}" y="{cy - 56}" width="7" height="24" rx="3" fill="#795548"/>'
            f'<ellipse cx="{cx + 17}" cy="{cy - 48}" rx="17" ry="8" fill="#69db7c" transform="rotate(-20 {cx + 17} {cy - 48})"/>'
            f'<path d="M{cx} {cy - 30} C{cx - 20} {cy - 46} {cx - 48} {cy - 36} {cx - 46} {cy - 2} C{cx - 44} {cy + 34} {cx - 18} {cy + 46} {cx} {cy + 38} '
            f'C{cx + 18} {cy + 46} {cx + 44} {cy + 34} {cx + 46} {cy - 2} C{cx + 48} {cy - 36} {cx + 20} {cy - 46} {cx} {cy - 30}Z" fill="{c}" stroke="{d}" stroke-width="4"/>'
            f'<ellipse cx="{cx - 26}" cy="{cy - 14}" rx="7" ry="12" fill="#fff" opacity=".5"/>' + tface(cx, cy + 4, .9))


def duck(cx, cy):
    return (f'<path d="M{cx - 46} {cy + 6} l-22 -20 l4 34z" fill="#ffd43b" stroke="#f59f00" stroke-width="4" stroke-linejoin="round"/>'
            f'<ellipse cx="{cx - 6}" cy="{cy + 14}" rx="48" ry="30" fill="#ffd43b" stroke="#f59f00" stroke-width="4"/>'
            f'<ellipse cx="{cx - 12}" cy="{cy + 12}" rx="22" ry="12" fill="#fcc419"/>'
            f'<circle cx="{cx + 22}" cy="{cy - 24}" r="26" fill="#ffd43b" stroke="#f59f00" stroke-width="4"/>'
            f'<path d="M{cx + 44} {cy - 26} q22 0 24 8 q-12 9 -26 3z" fill="#ff922b"/>'
            f'<circle cx="{cx + 28}" cy="{cy - 31}" r="5.5" fill="#1a1a2e"/><circle cx="{cx + 30}" cy="{cy - 33}" r="2" fill="#fff"/>'
            f'<ellipse cx="{cx + 16}" cy="{cy - 14}" rx="7" ry="4" fill="#ff8fab" opacity=".8"/>')


def fish(cx, cy, c="#4dabf7", d="#1c7ed6"):
    return (f'<path d="M{cx - 34} {cy} L{cx - 66} {cy - 26} L{cx - 62} {cy + 26}Z" fill="{c}" stroke="{d}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{cx - 6} {cy - 26} q12 -18 28 -2" fill="{c}" stroke="{d}" stroke-width="4"/>'
            f'<ellipse cx="{cx + 4}" cy="{cy}" rx="44" ry="30" fill="{c}" stroke="{d}" stroke-width="4"/>'
            f'<path d="M{cx - 12} {cy - 16} q-8 16 0 32" stroke="#fff" stroke-width="4" fill="none" opacity=".6"/>'
            f'<circle cx="{cx + 22}" cy="{cy - 6}" r="6" fill="#1a1a2e"/><circle cx="{cx + 24}" cy="{cy - 8}" r="2" fill="#fff"/>'
            f'<path d="M{cx + 18} {cy + 10} q8 6 16 0" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>')


def strawberry(cx, cy):
    seeds = "".join(f'<ellipse cx="{cx + dx}" cy="{cy + dy}" rx="3" ry="4.5" fill="#ffe066"/>'
                    for dx, dy in ((-30, -12), (30, -12), (-26, 20), (26, 20), (-10, 36), (10, 36)))
    return (f'<path d="M{cx - 42} {cy - 24} Q{cx - 46} {cy + 28} {cx} {cy + 50} Q{cx + 46} {cy + 28} {cx + 42} {cy - 24} Q{cx} {cy - 44} {cx - 42} {cy - 24}Z" fill="#ff5c5c" stroke="#e03131" stroke-width="4"/>'
            + seeds +
            f'<path d="M{cx - 32} {cy - 30} L{cx - 10} {cy - 36} L{cx} {cy - 54} L{cx + 10} {cy - 36} L{cx + 32} {cy - 30} L{cx + 8} {cy - 24} L{cx} {cy - 18} L{cx - 8} {cy - 24}Z" fill="#40c057" stroke="#2f9e44" stroke-width="3" stroke-linejoin="round"/>'
            + tface(cx, cy + 2, .85))


def mjelly(cx, cy, c, d):
    return jelly(cx, cy + 46, .17, c, d)


def orange_fruit(cx, cy, r=52):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffa94d" stroke="#e8590c" stroke-width="5"/>'
            + "".join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="2.5" fill="#e8590c" opacity=".5"/>' for dx, dy in ((-20, 18), (14, 26), (26, -4), (-28, -10)))
            + f'<ellipse cx="{cx - 18}" cy="{cy - 20}" rx="10" ry="16" fill="#fff" opacity=".45"/>'
            f'<ellipse cx="{cx + 14}" cy="{cy - r - 6}" rx="18" ry="9" fill="#69db7c" transform="rotate(-25 {cx + 14} {cy - r - 6})"/>'
            f'<rect x="{cx - 3}" y="{cy - r - 12}" width="6" height="16" rx="3" fill="#795548"/>')


def carrot(cx, cy):
    return (f'<ellipse cx="{cx - 14}" cy="{cy - 60}" rx="9" ry="26" fill="#51cf66" transform="rotate(-20 {cx - 14} {cy - 60})"/>'
            f'<ellipse cx="{cx}" cy="{cy - 66}" rx="9" ry="28" fill="#40c057"/>'
            f'<ellipse cx="{cx + 14}" cy="{cy - 60}" rx="9" ry="26" fill="#51cf66" transform="rotate(20 {cx + 14} {cy - 60})"/>'
            f'<path d="M{cx - 36} {cy - 42} Q{cx} {cy - 58} {cx + 36} {cy - 42} L{cx + 5} {cy + 72} Q{cx} {cy + 80} {cx - 5} {cy + 72}Z" fill="#ff922b" stroke="#e8590c" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M{cx - 22} {cy - 10} h14 M{cx + 6} {cy + 20} h12 M{cx - 14} {cy + 44} h10" stroke="#e8590c" stroke-width="4" stroke-linecap="round"/>')


def pumpkin(cx, cy):
    return (f'<rect x="{cx - 6}" y="{cy - 66}" width="14" height="26" rx="5" fill="#5c940d"/>'
            f'<ellipse cx="{cx - 30}" cy="{cy}" rx="36" ry="46" fill="#ffa94d" stroke="#e8590c" stroke-width="5"/>'
            f'<ellipse cx="{cx + 30}" cy="{cy}" rx="36" ry="46" fill="#ffa94d" stroke="#e8590c" stroke-width="5"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="32" ry="50" fill="#ffa94d" stroke="#e8590c" stroke-width="5"/>'
            + tface(cx, cy + 2, .9))


def leaf(cx, cy, c="#69db7c", d="#2f9e44", rot=0):
    return (f'<g transform="rotate({rot} {cx} {cy})"><path d="M{cx - 62} {cy + 40} Q{cx - 50} {cy - 52} {cx + 54} {cy - 52} Q{cx + 54} {cy + 40} {cx - 62} {cy + 40}Z" fill="{c}" stroke="{d}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M{cx - 62} {cy + 40} Q{cx - 4} {cy - 4} {cx + 40} {cy - 38}" stroke="{d}" stroke-width="5" fill="none" stroke-linecap="round"/></g>')


def frog(cx, cy):
    return (f'<circle cx="{cx - 30}" cy="{cy - 34}" r="24" fill="#69db7c" stroke="#2f9e44" stroke-width="5"/><circle cx="{cx + 30}" cy="{cy - 34}" r="24" fill="#69db7c" stroke="#2f9e44" stroke-width="5"/>'
            f'<ellipse cx="{cx}" cy="{cy + 6}" rx="64" ry="44" fill="#69db7c" stroke="#2f9e44" stroke-width="5"/>'
            f'<circle cx="{cx - 30}" cy="{cy - 36}" r="14" fill="#fff"/><circle cx="{cx + 30}" cy="{cy - 36}" r="14" fill="#fff"/>'
            f'<circle cx="{cx - 28}" cy="{cy - 34}" r="7" fill="#1a1a2e"/><circle cx="{cx + 32}" cy="{cy - 34}" r="7" fill="#1a1a2e"/>'
            f'<path d="M{cx - 34} {cy + 8} q34 26 68 0" stroke="#2b8a3e" stroke-width="6" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{cx - 44}" cy="{cy + 6}" rx="10" ry="6" fill="#ff8fab" opacity=".7"/><ellipse cx="{cx + 44}" cy="{cy + 6}" rx="10" ry="6" fill="#ff8fab" opacity=".7"/>')


def grapes(cx, cy, c="#9775fa", d="#6741d9"):
    pts = ((-30, -26), (0, -26), (30, -26), (-15, 2), (15, 2), (0, 30))
    return (f'<path d="M{cx} {cy - 56} q6 -18 20 -24" stroke="#795548" stroke-width="6" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{cx + 26}" cy="{cy - 68}" rx="18" ry="9" fill="#69db7c"/>'
            + "".join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="20" fill="{c}" stroke="{d}" stroke-width="4"/><circle cx="{cx + dx - 6}" cy="{cy + dy - 6}" r="5" fill="#fff" opacity=".5"/>' for dx, dy in pts))


def eggplant(cx, cy):
    return (f'<path d="M{cx - 10} {cy - 40} C{cx - 60} {cy - 20} {cx - 60} {cy + 70} {cx} {cy + 70} C{cx + 60} {cy + 70} {cx + 50} {cy - 10} {cx + 14} {cy - 40}Z" fill="#9775fa" stroke="#6741d9" stroke-width="5"/>'
            f'<path d="M{cx - 26} {cy - 36} Q{cx} {cy - 56} {cx + 28} {cy - 36} Q{cx} {cy - 24} {cx - 26} {cy - 36}Z" fill="#51cf66" stroke="#2f9e44" stroke-width="4"/>'
            f'<rect x="{cx - 4}" y="{cy - 70}" width="9" height="24" rx="4" fill="#2f9e44"/>'
            + tface(cx, cy + 22, .9))


def flower(cx, cy, pc="#9775fa", pd="#6741d9", cc="#ffd43b"):
    return ("".join(f'<circle cx="{f(cx + 34 * math.cos(a))}" cy="{f(cy + 34 * math.sin(a))}" r="27" fill="{pc}" stroke="{pd}" stroke-width="4"/>'
                    for a in [math.radians(-90 + i * 72) for i in range(5)])
            + f'<circle cx="{cx}" cy="{cy}" r="24" fill="{cc}" stroke="#f59f00" stroke-width="4"/>' + tface(cx, cy - 2, .7))


def pig(cx, cy):
    return (f'<path d="M{cx - 44} {cy - 30} L{cx - 50} {cy - 66} L{cx - 16} {cy - 46}Z" fill="#f783ac" stroke="#d6336c" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{cx + 44} {cy - 30} L{cx + 50} {cy - 66} L{cx + 16} {cy - 46}Z" fill="#f783ac" stroke="#d6336c" stroke-width="4" stroke-linejoin="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="52" fill="#fcc2d7" stroke="#d6336c" stroke-width="5"/>'
            f'<ellipse cx="{cx}" cy="{cy + 14}" rx="22" ry="15" fill="#f783ac" stroke="#d6336c" stroke-width="3"/>'
            f'<circle cx="{cx - 7}" cy="{cy + 14}" r="4" fill="#a61e4d"/><circle cx="{cx + 7}" cy="{cy + 14}" r="4" fill="#a61e4d"/>'
            f'<circle cx="{cx - 20}" cy="{cy - 14}" r="6" fill="#1a1a2e"/><circle cx="{cx + 20}" cy="{cy - 14}" r="6" fill="#1a1a2e"/>'
            f'<path d="M{cx - 10} {cy + 34} q10 7 20 0" stroke="#a61e4d" stroke-width="4" fill="none" stroke-linecap="round"/>')


def heart(cx, cy, s=.6, c="#f783ac", d="#d6336c"):
    return f'<path d="{heart_path(cx, cy, s)}" fill="{c}" stroke="{d}" stroke-width="5" stroke-linejoin="round"/>'


def cloud(cx, cy, c="#ffffff", d="#ced4da", s=1.0, with_face=False):
    out = puff([(cx - 42 * s, cy + 10 * s, 34 * s), (cx, cy - 12 * s, 46 * s), (cx + 44 * s, cy + 10 * s, 34 * s), (cx - 20 * s, cy + 22 * s, 30 * s), (cx + 20 * s, cy + 22 * s, 30 * s)], c, d)
    return out + (tface(cx, cy + 6 * s, s * .9) if with_face else "")


def elephant(cx, cy):
    return (f'<circle cx="{cx - 50}" cy="{cy - 4}" r="38" fill="#adb5bd" stroke="#868e96" stroke-width="5"/><circle cx="{cx + 50}" cy="{cy - 4}" r="38" fill="#adb5bd" stroke="#868e96" stroke-width="5"/>'
            f'<circle cx="{cx - 50}" cy="{cy - 4}" r="22" fill="#ffc9de" opacity=".7"/><circle cx="{cx + 50}" cy="{cy - 4}" r="22" fill="#ffc9de" opacity=".7"/>'
            f'<circle cx="{cx}" cy="{cy}" r="44" fill="#adb5bd" stroke="#868e96" stroke-width="5"/>'
            f'<path d="M{cx} {cy + 20} Q{cx + 4} {cy + 64} {cx + 30} {cy + 70}" stroke="#868e96" stroke-width="26" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx} {cy + 20} Q{cx + 4} {cy + 64} {cx + 30} {cy + 70}" stroke="#adb5bd" stroke-width="16" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{cx - 16}" cy="{cy - 8}" r="6" fill="#1a1a2e"/><circle cx="{cx + 16}" cy="{cy - 8}" r="6" fill="#1a1a2e"/>')


def stone(cx, cy):
    return (f'<path d="M{cx - 66} {cy + 30} Q{cx - 70} {cy - 30} {cx - 10} {cy - 40} Q{cx + 60} {cy - 44} {cx + 68} {cy + 18} Q{cx + 66} {cy + 44} {cx} {cy + 44} Q{cx - 60} {cy + 46} {cx - 66} {cy + 30}Z" fill="#868e96" stroke="#495057" stroke-width="5"/>'
            f'<ellipse cx="{cx - 24}" cy="{cy - 16}" rx="16" ry="8" fill="#fff" opacity=".35"/>' + tface(cx + 6, cy + 4, .9))


def snowflake(cx, cy, r=58):
    arms = ""
    for i in range(6):
        a = math.radians(i * 60 - 90); ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
        mx, my = cx + r * .6 * math.cos(a), cy + r * .6 * math.sin(a)
        b1, b2 = a + math.radians(40), a - math.radians(40)
        arms += f'M{f(cx)} {f(cy)} L{f(ex)} {f(ey)} M{f(mx)} {f(my)} L{f(mx + 18 * math.cos(b1))} {f(my + 18 * math.sin(b1))} M{f(mx)} {f(my)} L{f(mx + 18 * math.cos(b2))} {f(my + 18 * math.sin(b2))} '
    return (f'<path d="{arms}" stroke="#a5d8ff" stroke-width="16" stroke-linecap="round" fill="none"/>'
            f'<path d="{arms}" stroke="#fff" stroke-width="8" stroke-linecap="round" fill="none"/>')


def milk(cx, cy):
    return (f'<path d="M{cx - 40} {cy - 60} L{cx + 40} {cy - 60} L{cx + 32} {cy + 60} L{cx - 32} {cy + 60}Z" fill="#e7f5ff" stroke="#74c0fc" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M{cx - 37} {cy - 30} L{cx + 37} {cy - 30} L{cx + 32} {cy + 56} L{cx - 32} {cy + 56}Z" fill="#fff"/>'
            f'<path d="M{cx - 37} {cy - 30} L{cx + 37} {cy - 30}" stroke="#dee2e6" stroke-width="4"/>')


def sheep(cx, cy):
    return (f'<rect x="{cx - 40}" y="{cy + 30}" width="14" height="40" rx="6" fill="#495057"/><rect x="{cx + 20}" y="{cy + 30}" width="14" height="40" rx="6" fill="#495057"/>'
            + puff([(cx - 40, cy, 30), (cx - 10, cy - 20, 32), (cx + 22, cy - 14, 30), (cx + 10, cy + 18, 30), (cx - 26, cy + 20, 28)], "#ffffff", "#ced4da")
            + f'<ellipse cx="{cx + 56}" cy="{cy - 8}" rx="26" ry="32" fill="#495057"/>'
            f'<ellipse cx="{cx + 34}" cy="{cy - 26}" rx="14" ry="7" fill="#495057" transform="rotate(-30 {cx + 34} {cy - 26})"/>'
            f'<circle cx="{cx + 48}" cy="{cy - 12}" r="5" fill="#fff"/><circle cx="{cx + 66}" cy="{cy - 12}" r="5" fill="#fff"/>'
            f'<circle cx="{cx + 49}" cy="{cy - 11}" r="2.5" fill="#1a1a2e"/><circle cx="{cx + 67}" cy="{cy - 11}" r="2.5" fill="#1a1a2e"/>')


def egg(cx, cy):
    return (f'<path d="M{cx} {cy - 58} C{cx + 34} {cy - 58} {cx + 46} {cy + 6} {cx + 44} {cy + 20} C{cx + 42} {cy + 50} {cx + 20} {cy + 58} {cx} {cy + 58} '
            f'C{cx - 20} {cy + 58} {cx - 42} {cy + 50} {cx - 44} {cy + 20} C{cx - 46} {cy + 6} {cx - 34} {cy - 58} {cx} {cy - 58}Z" fill="#fff" stroke="#ced4da" stroke-width="5"/>'
            + tface(cx, cy + 10, .9))


def caterpillar(cx, cy):
    segs = "".join(f'<circle cx="{cx - 90 + i * 34}" cy="{cy + (6 if i % 2 else 0)}" r="24" fill="{"#69db7c" if i % 2 else "#8ce99a"}" stroke="#2f9e44" stroke-width="4"/>' for i in range(4))
    return (segs + f'<circle cx="{cx + 52}" cy="{cy - 10}" r="30" fill="#69db7c" stroke="#2f9e44" stroke-width="4"/>'
            f'<path d="M{cx + 42} {cy - 38} l-8 -24 M{cx + 62} {cy - 38} l8 -24" stroke="#2f9e44" stroke-width="4" stroke-linecap="round"/>'
            f'<circle cx="{cx + 34}" cy="{cy - 62}" r="6" fill="#ffd43b"/><circle cx="{cx + 70}" cy="{cy - 62}" r="6" fill="#ffd43b"/>' + tface(cx + 52, cy - 12, .85))


def gift(cx, cy):
    return (f'<rect x="{cx - 62}" y="{cy - 40}" width="124" height="104" rx="10" fill="#f783ac" stroke="#d6336c" stroke-width="5"/>'
            f'<rect x="{cx - 70}" y="{cy - 62}" width="140" height="32" rx="8" fill="#faa2c1" stroke="#d6336c" stroke-width="5"/>'
            f'<rect x="{cx - 12}" y="{cy - 62}" width="24" height="126" fill="#ffd43b"/>'
            f'<ellipse cx="{cx - 22}" cy="{cy - 74}" rx="22" ry="14" fill="none" stroke="#ffd43b" stroke-width="9"/><ellipse cx="{cx + 22}" cy="{cy - 74}" rx="22" ry="14" fill="none" stroke="#ffd43b" stroke-width="9"/>')


def block(cx, cy, s=1.0, c=("#ffe066", "#fcc419", "#f59f00")):
    a = 50 * s; o = 28 * s
    return (f'<path d="M{f(cx - a)} {f(cy - a)} L{f(cx - a + o)} {f(cy - a - o)} L{f(cx + a + o)} {f(cy - a - o)} L{f(cx + a)} {f(cy - a)}Z" fill="{c[0]}" stroke="{c[2]}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{f(cx + a)} {f(cy - a)} L{f(cx + a + o)} {f(cy - a - o)} L{f(cx + a + o)} {f(cy + a - o)} L{f(cx + a)} {f(cy + a)}Z" fill="{c[2]}" stroke="{c[2]}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="{f(cx - a)}" y="{f(cy - a)}" width="{f(2 * a)}" height="{f(2 * a)}" fill="{c[1]}" stroke="{c[2]}" stroke-width="4"/>'
            + star(cx, cy, 26 * s, "#fff", "#fff", 1))


def beachball(cx, cy, r=62):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>'
            f'<path d="M{cx} {cy - r} Q{cx - r} {cy} {cx} {cy + r} Q{cx - r * 1.9:.0f} {cy} {cx} {cy - r}Z" fill="#ff5c5c"/>'
            f'<path d="M{cx} {cy - r} Q{cx + r} {cy} {cx} {cy + r} Q{cx + r * 1.9:.0f} {cy} {cx} {cy - r}Z" fill="#4dabf7"/>'
            f'<path d="M{cx} {cy - r} Q{cx - r * .35:.0f} {cy} {cx} {cy + r} Q{cx + r * .35:.0f} {cy} {cx} {cy - r}Z" fill="#ffd43b"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#495057" stroke-width="5"/>'
            f'<ellipse cx="{cx - r * .4:.0f}" cy="{cy - r * .45:.0f}" rx="10" ry="16" fill="#fff" opacity=".6" transform="rotate(30 {cx - r * .4:.0f} {cy - r * .45:.0f})"/>')


def traffic_cone(cx, cy):
    return (f'<rect x="{cx - 66}" y="{cy + 56}" width="132" height="22" rx="8" fill="#e8590c"/>'
            f'<path d="M{cx - 14} {cy - 90} L{cx + 14} {cy - 90} L{cx + 50} {cy + 58} L{cx - 50} {cy + 58}Z" fill="#ff922b" stroke="#e8590c" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M{cx - 26} {cy - 30} L{cx + 26} {cy - 30} L{cx + 32} {cy - 4} L{cx - 32} {cy - 4}Z M{cx - 38} {cy + 18} L{cx + 38} {cy + 18} L{cx + 43} {cy + 38} L{cx - 43} {cy + 38}Z" fill="#fff"/>')


def icecream(cx, cy):
    return (f'<path d="M{cx - 48} {cy - 10} L{cx + 48} {cy - 10} L{cx} {cy + 110}Z" fill="#f4c27a" stroke="#c88a3a" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M{cx - 30} {cy + 10} L{cx + 14} {cy + 70} M{cx} {cy - 8} L{cx + 30} {cy + 30} M{cx + 30} {cy + 10} L{cx - 14} {cy + 70} M{cx} {cy - 8} L{cx - 30} {cy + 30}" stroke="#c88a3a" stroke-width="4"/>'
            f'<circle cx="{cx}" cy="{cy - 34}" r="44" fill="#f783ac" stroke="#d6336c" stroke-width="5"/>'
            f'<circle cx="{cx - 14}" cy="{cy - 50}" r="8" fill="#fff" opacity=".5"/>' + tface(cx, cy - 30, .9))


def drum(cx, cy):
    zig = " ".join(f'L{cx - 60 + i * 20} {cy - 14 + (40 if i % 2 else 0)}' for i in range(1, 7))
    return (f'<path d="M{cx - 60} {cy - 24} L{cx - 60} {cy + 50} A60 18 0 0 0 {cx + 60} {cy + 50} L{cx + 60} {cy - 24}Z" fill="#ff5c5c" stroke="#c92a2a" stroke-width="5"/>'
            f'<path d="M{cx - 60} {cy - 14} {zig}" stroke="#ffd43b" stroke-width="6" fill="none" stroke-linejoin="round"/>'
            f'<ellipse cx="{cx}" cy="{cy - 24}" rx="60" ry="18" fill="#fff4e6" stroke="#c92a2a" stroke-width="5"/>'
            f'<path d="M{cx - 70} {cy - 90} L{cx - 20} {cy - 34} M{cx + 70} {cy - 90} L{cx + 20} {cy - 34}" stroke="#a9744f" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="{cx - 70}" cy="{cy - 90}" r="10" fill="#ffd43b"/><circle cx="{cx + 70}" cy="{cy - 90}" r="10" fill="#ffd43b"/>')


def cup(cx, cy):
    return (f'<path d="M{cx + 40} {cy - 20} q44 0 44 34 q0 34 -44 34" stroke="#1c7ed6" stroke-width="12" fill="none"/>'
            f'<path d="M{cx - 44} {cy - 50} L{cx - 44} {cy + 60} A44 14 0 0 0 {cx + 44} {cy + 60} L{cx + 44} {cy - 50}Z" fill="#4dabf7" stroke="#1c7ed6" stroke-width="5"/>'
            f'<ellipse cx="{cx}" cy="{cy - 50}" rx="44" ry="14" fill="#d0ebff" stroke="#1c7ed6" stroke-width="5"/>' + tface(cx, cy + 14, .9))


def tent(cx, cy):
    return (f'<path d="M{cx} {cy - 90} L{cx + 90} {cy + 70} L{cx - 90} {cy + 70}Z" fill="#ffa94d" stroke="#e8590c" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M{cx} {cy - 10} L{cx + 32} {cy + 70} L{cx - 32} {cy + 70}Z" fill="#d9480f"/>'
            f'<path d="M{cx} {cy - 90} L{cx} {cy - 116}" stroke="#795548" stroke-width="6" stroke-linecap="round"/><path d="M{cx} {cy - 116} l26 8 -26 8z" fill="#ff5c5c"/>')


def blockstack(cx, cy):
    cols = ["#ff5c5c", "#4dabf7", "#69db7c", "#ffd43b", "#9775fa", "#ffa94d"]
    out, k = "", 0
    for row, n in enumerate((3, 2, 1)):
        for j in range(n):
            x = cx - (n - 1) * 30 + j * 60 - 28; y = cy + 50 - row * 58
            out += f'<rect x="{x}" y="{y}" width="56" height="56" rx="8" fill="{cols[k]}" stroke="{INK}" stroke-width="4"/>'; k += 1
    return out


def plus(cx, cy):
    return f'<rect x="{cx - 30}" y="{cy - 8}" width="60" height="16" rx="8" fill="#9d6bff"/><rect x="{cx - 8}" y="{cy - 30}" width="16" height="60" rx="8" fill="#9d6bff"/>'


def equals(cx, cy):
    return f'<rect x="{cx - 30}" y="{cy - 20}" width="60" height="14" rx="7" fill="#9d6bff"/><rect x="{cx - 30}" y="{cy + 6}" width="60" height="14" rx="7" fill="#9d6bff"/>'


def drop(cx, cy, c, d, s=1.0, light_face=False):
    p = (f'M{f(cx)} {f(cy - 62 * s)} C{f(cx + 30 * s)} {f(cy - 25 * s)} {f(cx + 50 * s)} {f(cy)} {f(cx + 50 * s)} {f(cy + 20 * s)} '
         f'A{f(50 * s)} {f(50 * s)} 0 0 1 {f(cx - 50 * s)} {f(cy + 20 * s)} C{f(cx - 50 * s)} {f(cy)} {f(cx - 30 * s)} {f(cy - 25 * s)} {f(cx)} {f(cy - 62 * s)}Z')
    fc = ("#fff", "#fff") if light_face else (INK, "#1a1a2e")
    return (f'<path d="{p}" fill="{c}" stroke="{d}" stroke-width="5" stroke-linejoin="round"/>'
            f'<ellipse cx="{f(cx - 24 * s)}" cy="{f(cy + 4 * s)}" rx="{f(8 * s)}" ry="{f(14 * s)}" fill="#fff" opacity=".5"/>'
            + tface(cx + 4 * s, cy + 26 * s, s, fc[0], fc[1]))


# ================= scenes =================
S = {}

# ---- numbers 6..10: big numeral, n friends to count (fx: count badges), ten-frame (fx2) ----
NUMCOL = {6: "#ff5c5c", 7: "#ffd43b", 8: "#4dabf7", 9: "#f783ac", 10: "#9775fa"}


def num_item(n, i, x, y):
    if n == 6: return apple_s(x, y)
    if n == 7: return duck(x, y)
    if n == 8: return fish(x, y)
    if n == 9: return strawberry(x, y)
    c = RAINBOW[i % 6]; return mjelly(x, y, c, DARK[c])


def num_scene(n):
    top = (n + 1) // 2
    pos = []
    for k, y in zip((top, n - top), (800, 930)):
        pos += [(round(540 + (j - (k - 1) / 2) * 180), y) for j in range(k)]
    items = "".join(num_item(n, i, x, y) for i, (x, y) in enumerate(pos))
    big = (f'<text x="540" y="665" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="430" fill="{NUMCOL[n]}" '
           f'stroke="{INK}" stroke-width="14" paint-order="stroke">{n}</text>')
    marks = "".join(f'<circle cx="{x + 46}" cy="{y - 48}" r="24" fill="#fff" stroke="#9d6bff" stroke-width="5"/>'
                    f'<text x="{x + 46}" y="{y - 37}" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="32" fill="{INK}">{i + 1}</text>'
                    for i, (x, y) in enumerate(pos))
    x0, y0, cs = 365, 120, 70
    tf = f'<rect x="{x0 - 12}" y="{y0 - 12}" width="{5 * cs + 24}" height="{2 * cs + 24}" rx="20" fill="#fff" stroke="#9d6bff" stroke-width="6"/>'
    for idx in range(10):
        r, c = divmod(idx, 5); cx, cy = x0 + c * cs + cs // 2, y0 + r * cs + cs // 2
        tf += f'<rect x="{x0 + c * cs}" y="{y0 + r * cs}" width="{cs}" height="{cs}" fill="none" stroke="#d0bfff" stroke-width="4"/>'
        if idx < n:
            tf += f'<circle cx="{cx}" cy="{cy}" r="24" fill="{NUMCOL[n]}" stroke="{DARK[NUMCOL[n]]}" stroke-width="4"/>'
    return frame(big + items, marks, tf)


for n in range(6, 11):
    S[f"bl2_n{n}"] = num_scene(n)

# ---- color mixing: equation drops (fx), things of the new color (fx2) ----
RED, YEL, BLU = ("#ff5c5c", "#e03131"), ("#ffd43b", "#f59f00"), ("#4dabf7", "#1c7ed6")
WHT, BLK = ("#ffffff", "#ced4da"), ("#343a40", "#212529")


def mix_scene(res, rd, a, b, things):
    fx = (drop(290, 250, *a, light_face=(a == BLK)) + plus(415, 270) + drop(540, 250, *b, light_face=(b == BLK))
          + equals(665, 270) + drop(790, 250, res, rd))
    return frame(jelly(540, 990, 1.0, res, rd), fx, things)


S["bl2_mix_orange"] = mix_scene("#ffa94d", "#e8590c", RED, YEL, orange_fruit(140, 580) + carrot(950, 560) + pumpkin(140, 850))
S["bl2_mix_green"] = mix_scene("#69db7c", "#2f9e44", BLU, YEL, leaf(140, 580, rot=-10) + frog(950, 580) + apple_s(140, 860, "#8ce99a", "#2f9e44"))
S["bl2_mix_purple"] = mix_scene("#9775fa", "#6741d9", RED, BLU, grapes(140, 600) + eggplant(950, 570) + flower(140, 860))
S["bl2_mix_pink"] = mix_scene("#f783ac", "#d6336c", RED, WHT, flower(140, 580, "#f783ac", "#d6336c") + pig(950, 590) + heart(140, 860, .55))
S["bl2_mix_gray"] = mix_scene("#adb5bd", "#868e96", BLK, WHT, cloud(140, 580, "#ced4da", "#868e96") + elephant(950, 580) + stone(140, 880))

# ---- opposites ----
S["bl2_bigsmall"] = frame(jelly(400, 990, 1.0, "#9775fa", "#6741d9") + jelly(870, 990, .32, "#ffd43b", "#f59f00"),
                          star(420, 320, 100), star(876, 755, 36))

UP_ARROW = '<path d="M800 170 L875 265 L832 265 L832 420 L768 420 L768 265 L725 265Z" fill="#69db7c" stroke="#2f9e44" stroke-width="7" stroke-linejoin="round"/>'
DOWN_ARROW = '<path d="M900 830 L970 740 L930 740 L930 590 L870 590 L870 740 L830 740Z" fill="#ffa94d" stroke="#e8590c" stroke-width="7" stroke-linejoin="round"/>'
BALLOON = ('<path d="M540 338 q-18 40 6 80 q22 40 0 80 q-14 30 6 66" stroke="#868e96" stroke-width="4" fill="none"/>'
           '<path d="M528 344 L552 344 L540 326Z" fill="#e03131"/>'
           '<ellipse cx="540" cy="245" rx="72" ry="88" fill="#ff5c5c" stroke="#e03131" stroke-width="6"/>'
           '<ellipse cx="512" cy="210" rx="14" ry="24" fill="#fff" opacity=".5" transform="rotate(20 512 210)"/>')
S["bl2_updown"] = frame(jelly(540, 990, .8, "#4dabf7", "#1c7ed6"), BALLOON + UP_ARROW, DOWN_ARROW + ball(900, 935, "#ffa94d", 60))

BOX_IN = ('<path d="M330 600 L400 540 L820 540 L750 600Z" fill="#d9480f" stroke="#e8590c" stroke-width="10" stroke-linejoin="round"/>'
          '<path d="M750 600 L820 540 L820 900 L750 960Z" fill="#fd7e14" stroke="#e8590c" stroke-width="10" stroke-linejoin="round"/>'
          '<rect x="330" y="600" width="420" height="360" rx="8" fill="#ffa94d" stroke="#e8590c" stroke-width="10"/>'
          '<ellipse cx="400" cy="680" rx="34" ry="18" fill="#fff" opacity=".35"/>' + face(540, 770, 1.0))
S["bl2_inout"] = frame(BOX_IN, f'<g clip-path="url(#inclip)">{ball(575, 572, "#4dabf7", 64)}</g>', ball(930, 935, "#4dabf7", 64),
                       defs='<clipPath id="inclip"><rect x="0" y="0" width="1080" height="598"/></clipPath>')

GIFTBOX = ('<rect x="300" y="620" width="480" height="340" rx="16" fill="#f783ac" stroke="#d6336c" stroke-width="10"/>'
           '<rect x="306" y="626" width="468" height="26" fill="#d6336c" opacity=".5"/>'
           '<rect x="300" y="900" width="480" height="34" fill="#ffd43b"/>' + face(540, 780, 1.0))
LID = ('<rect x="280" y="566" width="520" height="70" rx="14" fill="#faa2c1" stroke="#d6336c" stroke-width="10"/>'
       '<rect x="515" y="566" width="50" height="70" fill="#ffd43b"/>'
       '<ellipse cx="505" cy="540" rx="40" ry="24" fill="none" stroke="#ffd43b" stroke-width="16"/><ellipse cx="575" cy="540" rx="40" ry="24" fill="none" stroke="#ffd43b" stroke-width="16"/>'
       '<circle cx="540" cy="552" r="16" fill="#fcc419"/>')
S["bl2_openclosed"] = frame(GIFTBOX, LID,
                            f'<g transform="rotate(-38 290 630)">{LID}</g>' + star(470, 470, 40) + star(620, 400, 52, "#a5d8ff", "#4dabf7") + star(720, 510, 34, "#ffc9de", "#f783ac") + star(560, 260, 30))


def jar(x, full):
    w, top, bot = 300, 470, 960
    out = (f'<rect x="{x}" y="{top + 40}" width="{w}" height="{bot - top - 40}" rx="44" fill="#e7f5ff" fill-opacity=".8" stroke="#74c0fc" stroke-width="8"/>')
    if full:
        k = 0
        for row in range(6):
            for j in range(4):
                c = RAINBOW[k % 6]; k += 1
                out += f'<circle cx="{x + 52 + j * 65 + (16 if row % 2 else 0) - (8 if j == 3 and row % 2 else 0)}" cy="{915 - row * 62}" r="30" fill="{c}" stroke="{DARK[c]}" stroke-width="3"/>'
    out += (f'<rect x="{x + 30}" y="{top}" width="{w - 60}" height="54" rx="14" fill="#9d6bff" stroke="#6741d9" stroke-width="6"/>'
            f'<rect x="{x + 26}" y="{top + 80}" width="16" height="110" rx="8" fill="#fff" opacity=".7"/>')
    return out + face(x + w // 2, 650, .8)


def jar_ring(x):
    return (f'<rect x="{x - 26}" y="440" width="352" height="546" rx="60" fill="none" stroke="#ffd43b" stroke-width="14" stroke-dasharray="30 16"/>'
            + star(x - 10, 430, 30) + star(x + 310, 470, 24))


S["bl2_fullempty"] = frame(jar(170, True) + jar(610, False), jar_ring(170), jar_ring(610))

# ---- 3D shapes ----
CUBE_FRONT = "M340 560 L740 560 L740 960 L340 960Z"
S["bl2_cube"] = frame('<path d="M340 560 L480 440 L880 440 L740 560Z" fill="#ff8787" stroke="#c92a2a" stroke-width="10" stroke-linejoin="round"/>'
                      '<path d="M740 560 L880 440 L880 840 L740 960Z" fill="#e03131" stroke="#c92a2a" stroke-width="10" stroke-linejoin="round"/>'
                      f'<path d="{CUBE_FRONT}" fill="#ff5c5c" stroke="#c92a2a" stroke-width="10" stroke-linejoin="round"/>'
                      '<ellipse cx="410" cy="620" rx="34" ry="16" fill="#fff" opacity=".35"/>' + face(540, 750, 1.05),
                      dashed(CUBE_FRONT), gift(140, 430) + block(950, 300))

S["bl2_sphere"] = frame('<circle cx="540" cy="680" r="300" fill="url(#sph)" stroke="#1864ab" stroke-width="10"/>'
                        '<ellipse cx="430" cy="520" rx="60" ry="34" fill="#fff" opacity=".45" transform="rotate(-35 430 520)"/>' + face(540, 700, 1.2),
                        dashed("M240 680 A300 300 0 1 1 840 680 A300 300 0 1 1 240 680Z") + '<ellipse cx="540" cy="680" rx="300" ry="80" fill="none" stroke="#ffd43b" stroke-width="10" stroke-dasharray="24 16"/>',
                        beachball(140, 380) + orange_fruit(950, 390, 58),
                        defs='<radialGradient id="sph" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#d0ebff"/><stop offset=".45" stop-color="#4dabf7"/><stop offset="1" stop-color="#1971c2"/></radialGradient>')

S["bl2_cone"] = frame('<path d="M540 320 L810 920 A270 70 0 0 1 270 920Z" fill="url(#cng)" stroke="#e67700" stroke-width="10" stroke-linejoin="round"/>' + face(540, 770, .9),
                      '<ellipse cx="540" cy="920" rx="270" ry="70" fill="none" stroke="#9d6bff" stroke-width="14" stroke-dasharray="30 16"/>'
                      '<circle cx="540" cy="320" r="26" fill="#ff5c5c" stroke="#fff" stroke-width="6"/>',
                      traffic_cone(140, 870) + icecream(950, 400),
                      defs='<linearGradient id="cng" x1="0" x2="1"><stop offset="0" stop-color="#fff3bf"/><stop offset=".45" stop-color="#ffd43b"/><stop offset="1" stop-color="#f59f00"/></linearGradient>')

S["bl2_cylinder"] = frame('<path d="M330 420 L330 920 A210 60 0 0 0 750 920 L750 420Z" fill="url(#cyg)" stroke="#2b8a3e" stroke-width="10" stroke-linejoin="round"/>'
                          '<ellipse cx="540" cy="420" rx="210" ry="60" fill="#b2f2bb" stroke="#2b8a3e" stroke-width="10"/>' + face(540, 690, 1.1),
                          '<ellipse cx="540" cy="420" rx="210" ry="60" fill="none" stroke="#ffd43b" stroke-width="14" stroke-dasharray="30 16"/>'
                          '<ellipse cx="540" cy="920" rx="210" ry="60" fill="none" stroke="#ffd43b" stroke-width="14" stroke-dasharray="30 16"/>',
                          drum(140, 470) + cup(950, 400),
                          defs='<linearGradient id="cyg" x1="0" x2="1"><stop offset="0" stop-color="#51cf66"/><stop offset=".35" stop-color="#8ce99a"/><stop offset="1" stop-color="#2b8a3e"/></linearGradient>')

PYR_FRONT = "M560 330 L260 960 L760 960Z"
S["bl2_pyramid"] = frame('<path d="M560 330 L760 960 L900 880Z" fill="#6741d9" stroke="#5f3dc4" stroke-width="10" stroke-linejoin="round"/>'
                         f'<path d="{PYR_FRONT}" fill="#9775fa" stroke="#5f3dc4" stroke-width="10" stroke-linejoin="round"/>' + face(525, 800, .85),
                         dashed(PYR_FRONT) + dashed("M560 330 L900 880 L760 960"), tent(150, 860) + blockstack(955, 390))

# ---- patterns & sorting ----
def bead(cx, cy, c, r=55):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" stroke="{DARK[c]}" stroke-width="5"/>'
            f'<ellipse cx="{f(cx - r * .38)}" cy="{f(cy - r * .4)}" rx="{f(r * .16)}" ry="{f(r * .26)}" fill="#fff" opacity=".5" transform="rotate(30 {f(cx - r * .38)} {f(cy - r * .4)})"/>'
            + tface(cx, cy + 4, r / 55))


def sq(cx, cy, c, h=50):
    return (f'<rect x="{cx - h}" y="{cy - h}" width="{2 * h}" height="{2 * h}" rx="12" fill="{c}" stroke="{DARK[c]}" stroke-width="5"/>'
            + tface(cx, cy + 4, h / 55))


def pattern_scene(seq, last, row2):
    line = '<path d="M60 420 H1020" stroke="#c5b3ff" stroke-width="8" stroke-linecap="round"/>'
    items = "".join(fn(140 + i * 160, 420) for i, fn in enumerate(seq))
    slot = '<circle cx="940" cy="420" r="60" fill="#fff" fill-opacity=".7" stroke="#9d6bff" stroke-width="7" stroke-dasharray="20 12"/>'
    host = jelly(540, 990, .72, "#d0bfff", "#9d6bff")
    r2 = "".join(fn(140 + i * 160, 220) for i, fn in enumerate(row2))
    return frame(line + items + slot + host, last(940, 420), r2)


R_, B_, Y_, G_ = "#ff5c5c", "#4dabf7", "#ffd43b", "#69db7c"
S["bl2_pattern_ab"] = pattern_scene([lambda x, y, c=c: bead(x, y, c) for c in (R_, B_, R_, B_, R_)], lambda x, y: bead(x, y, B_),
                                    [lambda x, y, c=c: bead(x, y, c, 38) for c in (Y_, G_, Y_, G_, Y_, G_)])
S["bl2_pattern_shapes"] = pattern_scene([lambda x, y: bead(x, y, R_), lambda x, y: sq(x, y, B_)] * 2 + [lambda x, y: bead(x, y, R_)], lambda x, y: sq(x, y, B_),
                                        [lambda x, y, i=i: star(x, y, 46) if i % 2 == 0 else heart(x, y + 6, .42) for i in range(6)])


def bin_(x0, c, d, icon=""):
    x1 = x0 + 360; cx = x0 + 180
    return (f'<path d="M{x0} 700 L{x1} 700 L{x1 - 26} 960 L{x0 + 26} 960Z" fill="{c}" stroke="{d}" stroke-width="10" stroke-linejoin="round"/>'
            + icon + face(cx, 845 if icon else 815, .8))


def rim(x0, d):
    return f'<rect x="{x0 - 12}" y="688" width="384" height="28" rx="14" fill="{d}"/>'


def sort_scene(left, right, fx_items, fx2_items):
    body = bin_(120, *left) + rim(120, left[1]) + bin_(600, *right) + rim(600, right[1])
    return frame(body, fx_items + rim(120, left[1]), fx2_items + rim(600, right[1]))


S["bl2_sort_color"] = sort_scene(("#ffc9c9", "#e03131"), ("#d0ebff", "#1c7ed6"),
                                 apple_s(205, 650) + heart(300, 640, .45, "#ff5c5c", "#e03131") + ball(400, 655, "#ff5c5c", 46),
                                 ball(690, 655, "#4dabf7", 46) + star(785, 640, 52, "#4dabf7", "#1c7ed6") + fish(890, 655))
S["bl2_sort_shape"] = sort_scene(("#fff3bf", "#f59f00", '<circle cx="300" cy="752" r="26" fill="none" stroke="#f59f00" stroke-width="9"/>'),
                                 ("#d3f9d8", "#2f9e44", '<rect x="756" y="728" width="48" height="48" rx="6" fill="none" stroke="#2f9e44" stroke-width="9"/>'),
                                 bead(210, 650, R_, 44) + bead(300, 635, B_, 48) + bead(392, 650, "#9775fa", 44),
                                 sq(692, 652, Y_, 38) + sq(782, 636, "#ffa94d", 42) + sq(872, 652, G_, 38))


def party_hat(cx, base_y, s, c, d):
    w, h = 150 * s, 190 * s
    return (f'<path d="M{f(cx - w / 2)} {f(base_y)} L{f(cx)} {f(base_y - h)} L{f(cx + w / 2)} {f(base_y)}Z" fill="{c}" stroke="{d}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M{f(cx - w * .32)} {f(base_y - h * .35)} L{f(cx + w * .32)} {f(base_y - h * .35)}" stroke="#fff" stroke-width="{f(10 * s + 3)}" stroke-linecap="round"/>'
            f'<circle cx="{f(cx)}" cy="{f(base_y - h)}" r="{f(18 * s + 4)}" fill="#fff" stroke="{d}" stroke-width="4"/>')


SIZES = [(140, .3), (420, .55), (800, .78)]
S["bl2_sizes"] = frame("".join(jelly(cx, 990, s, "#f783ac", "#d6336c") for cx, s in reversed(SIZES)),
                       "".join(star(cx + 20 * s, 990 - 540 * s - 50 - 60 * s, 30 + 70 * (s - .3) / .48) for cx, s in SIZES),
                       "".join(party_hat(cx + 20 * s, 990 - 528 * s, s * 1.4, hc, hd) for (cx, s), (hc, hd) in zip(SIZES, (("#4dabf7", "#1c7ed6"), ("#ffd43b", "#f59f00"), ("#69db7c", "#2f9e44")))))

# ---- light & dark shades, white, rainbow ----
def ld_scene(light, dark, strip, ex_l, ex_r):
    body = jelly(300, 990, .62, *light) + jelly(780, 990, .62, *dark, mouth="#fff")
    x0 = 540 - (5 * 110 + 4 * 14) // 2
    fx = "".join(f'<rect x="{x0 + i * 124}" y="170" width="110" height="110" rx="24" fill="{c}" stroke="{INK}" stroke-width="5"/>' for i, c in enumerate(strip))
    fx += '<path d="M250 320 H830" stroke="#9d6bff" stroke-width="10" stroke-linecap="round"/><path d="M830 320 l-26 -18 v36z" fill="#9d6bff"/>'
    return frame(body, fx, ex_l + ex_r)


def day_sky(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="80" fill="#a5d8ff" stroke="#74c0fc" stroke-width="6"/>'
            f'<circle cx="{cx - 22}" cy="{cy - 20}" r="24" fill="#ffd43b"/>' + cloud(cx + 18, cy + 22, s=.55))


def night_sky(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="80" fill="#1c3d7a" stroke="#102a5c" stroke-width="6"/>'
            f'<path d="M{cx + 8} {cy - 44} A44 44 0 1 0 {cx + 8} {cy + 44} A34 34 0 1 1 {cx + 8} {cy - 44}Z" fill="#ffe066"/>'
            + star(cx + 36, cy - 30, 14, "#fff", "#fff", 1) + star(cx + 44, cy + 26, 10, "#fff", "#fff", 1))


def pine(cx, cy):
    return (f'<rect x="{cx - 10}" y="{cy + 56}" width="20" height="28" fill="#795548"/>'
            + "".join(f'<path d="M{cx} {cy - 80 + k * 40} L{cx + 50 + k * 10} {cy - 10 + k * 40} L{cx - 50 - k * 10} {cy - 10 + k * 40}Z" fill="#2b8a3e" stroke="#1b5e2a" stroke-width="5" stroke-linejoin="round"/>' for k in range(3)))


def lavender(cx, cy):
    buds = "".join(f'<ellipse cx="{cx + (8 if k % 2 else -8)}" cy="{cy - 70 + k * 16}" rx="11" ry="9" fill="#d0bfff" stroke="#b197fc" stroke-width="3"/>' for k in range(6))
    return (f'<path d="M{cx} {cy + 80} L{cx} {cy - 40}" stroke="#69db7c" stroke-width="7" stroke-linecap="round"/>'
            f'<ellipse cx="{cx - 20}" cy="{cy + 40}" rx="20" ry="7" fill="#69db7c" transform="rotate(-30 {cx - 20} {cy + 40})"/>' + buds
            + f'<path d="M{cx + 50} {cy + 80} L{cx + 50} {cy - 10}" stroke="#69db7c" stroke-width="7" stroke-linecap="round"/>'
            + "".join(f'<ellipse cx="{cx + 50 + (7 if k % 2 else -7)}" cy="{cy - 40 + k * 15}" rx="10" ry="8" fill="#e5dbff" stroke="#b197fc" stroke-width="3"/>' for k in range(5)))


S["bl2_ld_blue"] = ld_scene(("#a5d8ff", "#4dabf7"), ("#1864ab", "#0b3d75"), ["#d0ebff", "#74c0fc", "#339af0", "#1c7ed6", "#1864ab"], day_sky(300, 470), night_sky(780, 470))
S["bl2_ld_green"] = ld_scene(("#b2f2bb", "#51cf66"), ("#2b8a3e", "#1b5e2a"), ["#d3f9d8", "#8ce99a", "#51cf66", "#2f9e44", "#2b6a35"], leaf(300, 480, "#b2f2bb", "#51cf66"), pine(780, 470))
S["bl2_ld_purple"] = ld_scene(("#e5dbff", "#b197fc"), ("#5f3dc4", "#3b2785"), ["#e5dbff", "#b197fc", "#845ef7", "#6741d9", "#4527a0"], lavender(280, 470), grapes(780, 490, "#5f3dc4", "#3b2785"))

S["bl2_white"] = frame(jelly(540, 990, 1.0, "#ffffff", "#ced4da"), cloud(150, 400) + snowflake(940, 380) + milk(950, 650), sheep(130, 720) + egg(960, 870))

ARCS = "".join(f'<path d="M{540 - (430 - i * 42)} 905 A{430 - i * 42} {430 - i * 42} 0 0 1 {540 + 430 - i * 42} 905" stroke="{c}" stroke-width="44" fill="none"/>' for i, c in enumerate(RAINBOW))
S["bl2_rainbow"] = frame(ARCS + cloud(215, 925, s=1.7) + cloud(865, 925, s=1.7) + jelly(540, 990, .32, "#d0bfff", "#9d6bff"),
                         "".join(drop(540 + (i - 2.5) * 150, 200, c, DARK[c], .75) for i, c in enumerate(RAINBOW)),
                         star(110, 380, 34) + star(970, 400, 40, "#ffc9de", "#f783ac") + star(540, 380, 28, "#a5d8ff", "#4dabf7") + star(980, 230, 24) + star(110, 200, 26, "#d3f9d8", "#69db7c"))

S["bl2_hunt_green"] = frame(jelly(540, 990, 1.0, "#69db7c", "#2f9e44")
                            + '<path d="M842 692 L922 772" stroke="#9d6bff" stroke-width="26" stroke-linecap="round"/>'
                            '<circle cx="790" cy="640" r="72" fill="#e7f5ff" fill-opacity=".55" stroke="#495057" stroke-width="14"/>'
                            '<path d="M752 612 q14 -22 38 -26" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round"/>',
                            frog(150, 430) + leaf(940, 330, rot=10), apple_s(140, 820, "#8ce99a", "#2f9e44") + caterpillar(960, 930))

SCENES_BLOOP2 = S
NAMES_BLOOP2 = {
    "bl2_n6": "SIX", "bl2_n7": "SEVEN", "bl2_n8": "EIGHT", "bl2_n9": "NINE", "bl2_n10": "TEN",
    "bl2_mix_orange": "ORANGE", "bl2_mix_green": "GREEN", "bl2_mix_purple": "PURPLE", "bl2_mix_pink": "PINK", "bl2_mix_gray": "GRAY",
    "bl2_bigsmall": "BIG & SMALL", "bl2_updown": "UP & DOWN", "bl2_inout": "IN & OUT", "bl2_openclosed": "OPEN & CLOSED", "bl2_fullempty": "FULL & EMPTY",
    "bl2_cube": "CUBE", "bl2_sphere": "SPHERE", "bl2_cone": "CONE", "bl2_cylinder": "CYLINDER", "bl2_pyramid": "PYRAMID",
    "bl2_pattern_ab": "COLOR PATTERN", "bl2_pattern_shapes": "SHAPE PATTERN", "bl2_sort_color": "SORT BY COLOR", "bl2_sort_shape": "SORT BY SHAPE",
    "bl2_sizes": "SMALL TO BIG",
    "bl2_white": "WHITE", "bl2_ld_blue": "BLUE SHADES", "bl2_ld_green": "GREEN SHADES", "bl2_ld_purple": "PURPLE SHADES",
    "bl2_rainbow": "RAINBOW", "bl2_hunt_green": "GREEN HUNT",
}
assert set(NAMES_BLOOP2) == set(SCENES_BLOOP2) and all(k.startswith("bl2_") for k in SCENES_BLOOP2)
