"""Pictures for za_ep15 "How Can Milo See Under the Deep Blue Sea?" (Nov 27 2026). One new picture board, one new kind and props only: no existing
character, place or prop is drawn differently (Tula is art2.turtle as it is; the sea places of art_za_ep12 and art_za_ep13 are used as they are).

Place:
  "paper_sea"  a picture board: a framed picture, air above a water line (BWL), water below, the words AIR and WATER on it.
Kind (registered into art2.RIGS, kit.PT, kit.BOX):
  "turtle_up"  Tula as she is, tilted nose-up by 40 degrees: she comes up for air and her head is out of the water when the water line is at y = -290
               of her own units. The parts keep their names (-neck, -ff, -eye ...), so the engine moves them as it moves "turtle".
Props: sea_front (a thin sheet of water in FRONT of the swimmers of a split view: what is under the water line looks under the water),
  leaf_boat (a big floating leaf; y = 0 is where Milo's feet stand), twinkles (six sparkles along the water line, -0..-5), ripple (rings on the
  water round a head), bub3 (three big bubbles to count, -0..-2), up_arrow, think (a thought bubble with a little picture in it).
"""
import math
import art, art2, kit
import art_za_ep12 as A12
import art_za_ep13 as A13
from art import INK

WL = A12.WL                 # the water line of the split views (300)
BWL = 470                   # the water line on the picture board
UP_DEG = -40
_PIV = (40, -170)


def _rot(x, y, deg=UP_DEG, piv=_PIV):
    a = math.radians(deg); dx, dy = x - piv[0], y - piv[1]
    return round(piv[0] + dx * math.cos(a) - dy * math.sin(a)), round(piv[1] + dx * math.sin(a) + dy * math.cos(a))


def turtle_up(pid):
    inner = art2.turtle(pid).replace('<g id="%s">' % pid, '<g id="%s-tilt" transform="rotate(%d %d %d)">' % (pid, UP_DEG, _PIV[0], _PIV[1]), 1)
    return '<g id="%s">%s</g>' % (pid, inner)


art2.RIGS["turtle_up"] = dict(art2.RIGS["turtle"], build=lambda p: turtle_up(p))
kit.PT["turtle_up"] = {"head": _rot(258, -182), "eye": _rot(272, -186), "body": _rot(0, -200), "top": (150, -400), "feet": (0, 0), "all": (40, -200)}
kit.BOX["turtle_up"] = (-300, 330, -400)


# ------------------------------------------------------------------ the picture board
def bg_paper_sea(p):
    far, mid, near = art.BG["paper_blue"](p)
    x0, y0, x1, y1 = 250, 150, 1670, 900
    wave = "M%d %d " % (x0, BWL) + " ".join("q35 -14 71 0 q35 14 71 0" for _ in range(10))
    pic = ('<clipPath id="%sclip"><rect x="%d" y="%d" width="%d" height="%d" rx="40"/></clipPath>' % (p, x0, y0, x1 - x0, y1 - y0)
           + '<g clip-path="url(#%sclip)"><rect x="%d" y="%d" width="%d" height="%d" fill="#eaf8ff"/>' % (p, x0, y0, x1 - x0, BWL - y0)
           + '<rect x="%d" y="%d" width="%d" height="%d" fill="#4fb4ea"/>' % (x0, BWL, x1 - x0, y1 - BWL)
           + '<path d="%s L%d %d L%d %d Z" fill="#8fd4f4" opacity=".7"/>' % (wave, x1, BWL + 40, x0, BWL + 40)
           + '<path d="%s" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/>' % wave
           + '<path d="M%d %d C600 %d 1300 %d %d %d L%d %d L%d %d Z" fill="#f2dfa6"/></g>' % (x0, y1 - 60, y1 - 110, y1 - 30, x1, y1 - 80, x1, y1, x0, y1)
           + '<rect x="%d" y="%d" width="%d" height="%d" rx="40" fill="none" stroke="%s" stroke-width="12"/>' % (x0, y0, x1 - x0, y1 - y0, INK)
           + '<text x="%d" y="%d" font-family="Baloo, sans-serif" font-weight="800" font-size="92" fill="#2f80ed">AIR</text>' % (x0 + 60, BWL - 50)
           + '<text x="%d" y="%d" font-family="Baloo, sans-serif" font-weight="800" font-size="92" fill="#fff">WATER</text>' % (x0 + 60, BWL + 160))
    return far + pic, mid, near


art.BG["paper_sea"] = bg_paper_sea
art.PLACE["paper_sea"] = "the picture board (air and water)"


# ------------------------------------------------------------------ props
def sea_front(p, col="#4fb4ea", line="#ffffff"):
    """A thin sheet of water in front of the swimmers, anchored at the water line (y = 0): what is below it looks under the water."""
    top = "M-1700 0 " + " ".join("q40 -16 80 0 q40 16 80 0" for _ in range(22))
    return ('<g id="%s"><path d="%s L1820 900 L-1700 900Z" fill="%s" opacity=".42"/><path d="%s" stroke="%s" stroke-width="9" fill="none" stroke-linecap="round" opacity=".95"/></g>' % (p, top, col, top, line))


def sea_front_eve(p): return sea_front(p, "#5a8fc8", "#fff3e0")


def leaf_boat(p):
    """A big green leaf that floats like a little boat. y = 0 is the top of the leaf, where Milo's feet stand."""
    d = "M-210 -6 C-150 70 150 70 230 -10 C150 10 -120 14 -210 -6Z"
    return ('<g id="%s"><path d="%s" fill="%s" stroke="%s" stroke-width="18" stroke-linejoin="round"/><path d="%s" fill="#5cc46a"/>' % (p, d, "#1f6f3c", "#1f6f3c", d)
            + '<path d="M-180 2 C-80 30 120 28 214 -4" stroke="#2f8f4a" stroke-width="9" fill="none" stroke-linecap="round"/>'
            + "".join('<path d="M%d %d l%d 24" stroke="#2f8f4a" stroke-width="7" stroke-linecap="round"/>' % (x, y, dx) for x, y, dx in ((-110, 18, -22), (-30, 24, -18), (60, 22, 18), (140, 12, 22)))
            + '<path d="M226 -10 q44 -30 70 -64" stroke="#1f6f3c" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M226 -10 q44 -30 70 -64" stroke="#5cc46a" stroke-width="7" fill="none" stroke-linecap="round"/></g>')


def _spark(x, y, r, col="#fffbe0"):
    return '<path d="M%d %d L%d %d L%d %d L%d %d L%d %d L%d %d L%d %d L%d %dZ" fill="%s" stroke="#ffd23f" stroke-width="5" stroke-linejoin="round"/>' % (
        x, y - r, x + r * .22, y - r * .22, x + r, y, x + r * .22, y + r * .22, x, y + r, x - r * .22, y + r * .22, x - r, y, x - r * .22, y - r * .22, col)


def twinkles(p):
    """Six sparkles of sunlight along the water line (y = 0), each its own part."""
    pts = ((-420, -6, 34), (-270, 8, 24), (-120, -10, 40), (40, 6, 26), (190, -8, 36), (330, 8, 24))
    return '<g id="%s">' % p + "".join('<g id="%s-%d">%s</g>' % (p, k, _spark(x, y, r)) for k, (x, y, r) in enumerate(pts)) + '</g>'


def ripple(p):
    """Rings on the water round a head that has just come up (y = 0 is the water line)."""
    return ('<g id="%s">' % p + "".join('<ellipse cx="0" cy="0" rx="%d" ry="%d" fill="none" stroke="#fff" stroke-width="%d" opacity="%.2f"/>' % (rx, ry, w, o) for rx, ry, w, o in ((120, 20, 9, .95), (190, 30, 7, .7), (260, 40, 5, .45))) + '</g>')


def bub3(p):
    """Three big bubbles to count, side by side, each its own part."""
    return '<g id="%s">' % p + "".join(
        '<g id="%s-%d"><circle cx="%d" cy="%d" r="%d" fill="#fff" fill-opacity=".35" stroke="#fff" stroke-width="8"/><path d="M%d %d q10 -18 28 -22" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/></g>'
        % (p, k, x, y, r, x - r * .5, y - r * .2) for k, (x, y, r) in enumerate(((-110, 0, 40), (0, -30, 46), (110, 0, 40)))) + '</g>'


def up_arrow(p):
    d = "M0 150 L0 -40 M-70 30 L0 -60 L70 30"
    return ('<g id="%s"><path d="%s" stroke="%s" stroke-width="56" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="%s" stroke="#ffd23f" stroke-width="34" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>' % (p, d, INK, d))


def _think(inner):
    return lambda p: art2.bubble_thought(p, inner, tail=1)


_mini_coral = ('<g transform="translate(-20 60) scale(.42)">' + A12._coral(-110, 0, 1.0) + A12._fan(40, 0, .8) + A12._coral(190, 0, .8, "#ffb347", "#e08a1f") + '</g>')
_mini_grass = '<g transform="translate(0 70)">' + "".join(A12._blade(x, 0, h, d, c, 14) for x, h, d, c in ((-90, 130, 16, "#3fae7a"), (-45, 160, -14, "#49ba84"), (0, 140, 16, "#35a06e"), (45, 165, -14, "#3fae7a"), (90, 125, 14, "#49ba84"))) + '</g>'
_mini_bed = ('<g transform="translate(0 20)">' + A12._stone(30, 60, 110, 90) + '<g transform="translate(-50 62) scale(.22)">' + art2.turtle("thinkbedt") + '</g></g>')
think_coral, think_grass, think_bed = _think(_mini_coral), _think(_mini_grass), _think(_mini_bed)


def zzz(p):
    """Three Z's that float up from a sleeper."""
    z = lambda x, y, s, o: ('<g transform="translate(%d %d) scale(%.2f)" opacity="%.2f"><path d="M-30 -30 L30 -30 L-30 30 L30 30" stroke="%s" stroke-width="22" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
                            '<path d="M-30 -30 L30 -30 L-30 30 L30 30" stroke="#ffffff" stroke-width="11" fill="none" stroke-linejoin="round" stroke-linecap="round"/></g>' % (x, y, s, o, INK))
    return '<g id="%s">%s%s%s</g>' % (p, z(0, 0, 1.0, 1), z(70, -90, .8, .9), z(120, -170, .6, .8))
