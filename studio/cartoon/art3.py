"""Art for the adventures after za_ep01 (Nov 17 2026): the mud hole, and the props of "Tumble and the Big Muddy Puddle".
Same style as art.py: flat fills, a thick coloured outline, nothing traced. Props are drawn around (0, 0)."""
import art, art2
from art import INK, SUN

MUD = art2.MUD
LEAF = ("#4fae4a", "#2f8a3a", "#8fd46a")       # leaf: fill, dark, light


# ------------------------------------------------------------------ place
def bg_mudhole(p):
    """The mud hole on the savanna: a wide, shiny brown pool with green reeds around it."""
    far, mid, _ = art2.bg_savanna(p)
    reeds = lambda x, y, s: f'<g transform="translate({x} {y}) scale({s})">' + "".join(
        f'<path d="M{k * 16} 0 q{-8 + k * 5} -70 {-18 + k * 12} -128" stroke="#5f9a3c" stroke-width="9" fill="none" stroke-linecap="round"/>' for k in range(-2, 3)) + \
        '<ellipse cx="-30" cy="-128" rx="9" ry="26" fill="#7a5632"/><ellipse cx="24" cy="-140" rx="9" ry="26" fill="#7a5632"/></g>'
    near = ('<rect x="-500" y="840" width="2920" height="1200" fill="#cdb85a"/>'
            + art2._hill("M-500 860 C300 820 900 850 1400 832 S2100 840 2420 850 L2420 900 L-500 900Z", "#cdb85a")
            + f'<ellipse cx="960" cy="1000" rx="900" ry="150" fill="{MUD[1]}"/><ellipse cx="960" cy="992" rx="872" ry="134" fill="{MUD[0]}"/>'
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w * .16:.0f}" fill="{MUD[2]}" opacity=".7"/>' for x, y, w in ((520, 950, 120), (1320, 940, 150), (900, 1050, 100), (1560, 1040, 90), (300, 1010, 70)))
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{MUD[2]}" stroke-width="5" opacity=".8"/>' for x, y, r in ((700, 1010, 16), (1180, 1060, 12), (1440, 980, 14)))
            + reeds(80, 900, 1.1) + reeds(1860, 906, 1.2) + reeds(1700, 1130, 1.0) + reeds(220, 1140, .9)
            + art2._grass(1240, 1150, 1.0, "#7fae4c") + art2._grass(640, 1160, 1.1, "#7fae4c"))
    return far, mid, near


art.BG.update({"mudhole": bg_mudhole})
art.PLACE.update({"mudhole": "the mud hole"})


def mud_front(pid, w=2920):
    """Mud in front of an animal that stands in the pool (it covers the feet)."""
    top = "M-1460 0 " + " ".join("q60 -16 120 0 q60 16 120 0" for _ in range(13))
    return f'<g id="{pid}"><path d="{top} L1660 400 L-1460 400Z" fill="{MUD[0]}"/><path d="{top}" stroke="{MUD[2]}" stroke-width="9" fill="none" opacity=".8"/></g>'


# ------------------------------------------------------------------ props
def camera(pid):
    """Milo's photo camera on three legs. The feet stand on y = 0."""
    legs = "".join(f'<path d="M0 -210 L{x} 0" stroke="{INK}" stroke-width="20" stroke-linecap="round"/><path d="M0 -210 L{x} 0" stroke="#c9a06a" stroke-width="9" stroke-linecap="round"/>' for x in (-86, 0, 86))
    return (f'<g id="{pid}">{legs}<rect x="-96" y="-330" width="192" height="126" rx="22" fill="#5b7fd6" stroke="{INK}" stroke-width="9"/>'
            f'<rect x="-66" y="-356" width="70" height="34" rx="10" fill="#3f5fb0" stroke="{INK}" stroke-width="8"/><circle cx="60" cy="-298" r="11" fill="{SUN}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="0" cy="-262" r="44" fill="#22335c" stroke="{INK}" stroke-width="9"/><circle cx="0" cy="-262" r="24" fill="#6fc3ff"/><circle cx="-10" cy="-272" r="8" fill="#fff"/></g>')


def flash(pid):
    """The camera's flash: a white sheet over the whole picture (shown for a moment)."""
    return f'<g id="{pid}"><rect x="-3000" y="-3000" width="6000" height="6000" fill="#fff"/></g>'


def leaf(pid, col=LEAF):
    """One big round jungle leaf, lying flat: a sun hat for a small head. The stem is at (0, 0), the leaf points right."""
    return (f'<g id="{pid}"><path d="M0 0 C60 -130 300 -150 430 -30 C300 70 80 90 0 0Z" fill="{col[0]}" stroke="{col[1]}" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M10 -4 Q200 -50 410 -30" stroke="{col[1]}" stroke-width="8" fill="none" stroke-linecap="round"/>'
            + "".join(f'<path d="M{x} {-18 - k * 4} q30 -40 70 -52" stroke="{col[1]}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".8"/>' for k, x in enumerate((90, 170, 250)))
            + f'<path d="M70 -70 Q200 -110 330 -70" stroke="{col[2]}" stroke-width="9" fill="none" stroke-linecap="round" opacity=".7"/></g>')


def fan(pid):
    """A palm-leaf fan on a stick. The hand holds it at (0, 0); it stands up."""
    blades = "".join(f'<path d="M0 -150 Q{dx * .5:.0f} -300 {dx} -{420 - abs(dx) * .35:.0f} Q{dx * .2:.0f} -260 0 -150Z" fill="{LEAF[0]}" stroke="{LEAF[1]}" stroke-width="8" stroke-linejoin="round"/>' for dx in (-190, -100, 0, 100, 190))
    return f'<g id="{pid}">{blades}<path d="M0 0 L0 -160" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M0 0 L0 -160" stroke="#9a6a3a" stroke-width="11" stroke-linecap="round"/></g>'


def wind(pid):
    """Three little puffs of moving air."""
    return f'<g id="{pid}">' + "".join(f'<path d="M0 {y} q50 -26 100 0 q50 26 100 0 q30 -16 50 -6" stroke="#fff" stroke-width="11" fill="none" stroke-linecap="round" opacity=".9"/>' for y in (-60, 0, 60)) + '</g>'


def hot_sun(pid):
    """A big hot sun with rays."""
    rays = "".join(f'<path d="M0 -150 L0 -214" stroke="#ffb020" stroke-width="20" stroke-linecap="round" transform="rotate({k * 30})"/>' for k in range(12))
    return f'<g id="{pid}"><g id="{pid}-rays">{rays}</g><circle cx="0" cy="0" r="118" fill="#ffd23f" stroke="#ffb020" stroke-width="12"/><circle cx="-34" cy="-38" r="26" fill="#fff6c8" opacity=".8"/></g>'


def heat(pid):
    """Wavy lines of heat rising."""
    return f'<g id="{pid}">' + "".join(f'<path d="M{x} 0 q-20 -30 0 -60 q20 -30 0 -60 q-20 -30 0 -60" stroke="#ff8a3c" stroke-width="12" fill="none" stroke-linecap="round" opacity=".85"/>' for x in (-70, 0, 70)) + '</g>'


def sweat(pid):
    """Two drops of sweat."""
    d = lambda x, y, s: f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -60 C30 -20 40 0 40 20 A40 40 0 0 1 -40 20 C-40 0 -30 -20 0 -60Z" fill="#7fd0f5" stroke="#3f9fd0" stroke-width="7"/><ellipse cx="-14" cy="16" rx="8" ry="13" fill="#fff" opacity=".7"/></g>'
    return f'<g id="{pid}">{d(0, 0, 1)}{d(70, 50, .7)}</g>'


def shade(pid, rx=330, ry=58):
    """A patch of shade on the ground."""
    return f'<g id="{pid}"><ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="#1d3a2a" opacity=".34"/></g>'


def splash(pid, col=MUD):
    """A splash of mud: drops flying up and out from (0, 0)."""
    drops = "".join(f'<g transform="rotate({a}) translate(0 -{r})"><path d="M0 -44 C22 -14 30 0 30 16 A30 30 0 0 1 -30 16 C-30 0 -22 -14 0 -44Z" fill="{col[0]}" stroke="{col[1]}" stroke-width="6"/></g>'
                    for a, r in ((-70, 190), (-42, 260), (-16, 300), (12, 280), (38, 250), (66, 200), (-56, 110), (50, 120), (0, 170)))
    return f'<g id="{pid}">{drops}<ellipse cx="0" cy="0" rx="210" ry="40" fill="{col[0]}" stroke="{col[1]}" stroke-width="7"/><ellipse cx="-60" cy="-8" rx="50" ry="10" fill="{col[2]}" opacity=".7"/></g>'


def mud_spot(pid, r=30):
    """One splat of mud (on a nose, on a tummy)."""
    return (f'<g id="{pid}"><circle cx="0" cy="0" r="{r}" fill="{MUD[0]}" stroke="{MUD[1]}" stroke-width="5"/><circle cx="{r * .9:.0f}" cy="{-r * .5:.0f}" r="{r * .36:.0f}" fill="{MUD[0]}" stroke="{MUD[1]}" stroke-width="4"/>'
            f'<circle cx="{-r * .8:.0f}" cy="{r * .7:.0f}" r="{r * .3:.0f}" fill="{MUD[0]}" stroke="{MUD[1]}" stroke-width="4"/><ellipse cx="{-r * .3:.0f}" cy="{-r * .3:.0f}" rx="{r * .3:.0f}" ry="{r * .16:.0f}" fill="{MUD[2]}" opacity=".8"/></g>')


def frame(pid, w=1500, h=900):
    """A photo frame: a white border around the picture, with a little shadow and two strips of tape."""
    b = 60
    return (f'<g id="{pid}"><path fill-rule="evenodd" d="M{-w / 2 - 2000} {-h / 2 - 2000} h{w + 4000} v{h + 4000} h{-w - 4000}Z M{-w / 2} {-h / 2} h{w} v{h} h{-w}Z" fill="#fbe9c6"/>'
            f'<path fill-rule="evenodd" d="M{-w / 2 - b} {-h / 2 - b} h{w + 2 * b} v{h + 2 * b + 70} h{-w - 2 * b}Z M{-w / 2} {-h / 2} h{w} v{h} h{-w}Z" fill="#fff" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>'
            f'<rect x="{-w / 2 - b - 30}" y="{-h / 2 - b - 24}" width="150" height="50" fill="#ff9ab8" opacity=".85" transform="rotate(-24 {-w / 2 - b + 40} {-h / 2 - b})"/>'
            f'<rect x="{w / 2 + b - 120}" y="{-h / 2 - b - 24}" width="150" height="50" fill="#8fd6ff" opacity=".85" transform="rotate(24 {w / 2 + b - 40} {-h / 2 - b})"/></g>')


def ear_board(pid):
    """An elephant's head with its big ear, for the fact board (the ear is the part that moves: #<pid>e-ear)."""
    return f'<g id="{pid}"><g transform="translate(-150 330) scale(1.0)">{art2.elephant(pid + "e")}</g></g>'
