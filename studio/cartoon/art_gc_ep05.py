"""Art for gc_ep05 "Why Do Things Fall Down?" (Gizmo Explains, catch-up run B, Nov 28 2026): props for gravity (no new place: the episode uses
glab, gbench, gpark, gmeadow, gsky, gspace and the board). An apple tree whose apple falls, balls (heavy and light), a feather, a rock, the Earth
with pull arrows and little people standing all around it, a small pull and a big pull, the Moon going around the Earth and the Earth going around
the Sun, a floor strip for the board. Props are drawn around (0, 0); nothing that exists changes."""
import math
import art, art2, kit
from art import INK, SUN
from art_gizmo import NAVY, SCREEN, CYAN, ACC, ORANGE, SILVER, STEEL, B1, B2, GREEN, _grad

RED = "#ff5d5d"; REDD = "#c23434"; LEAF = "#4fae4a"; BARK = "#8a5a32"; ROCK = "#9aa3b5"; ROCKD = "#6d7689"; SEA = "#3d8de0"; LAND = "#62b85a"


def _apple(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -26 C-30 -44 -56 -20 -50 10 C-44 40 -18 52 0 42 C18 52 44 40 50 10 C56 -20 30 -44 0 -26Z" '
            f'fill="{RED}" stroke="{REDD}" stroke-width="6"/><path d="M0 -26 Q4 -44 12 -52" stroke="{BARK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<path d="M8 -42 Q30 -60 44 -42 Q24 -30 8 -42Z" fill="{LEAF}"/><ellipse cx="-22" cy="-6" rx="9" ry="14" fill="#fff" opacity=".6"/></g>')


def apple_tree(pid):
    """An apple tree standing on the ground at (0, 0): trunk, round crown, five apples that stay, and -apple, the one that falls (it hangs at
    (150, -330); a tween of y = +300 lands it on the grass at (150, -30))."""
    crown = (f'<circle cx="0" cy="-470" r="230" fill="{LEAF}"/><circle cx="-170" cy="-380" r="150" fill="#5fbf5a"/><circle cx="170" cy="-390" r="160" fill="#57b552"/>'
             f'<circle cx="40" cy="-600" r="150" fill="#5fbf5a"/>')
    return (f'<g id="{pid}"><ellipse cx="0" cy="6" rx="260" ry="30" fill="#000" opacity=".14"/>'
            f'<path d="M-40 0 C-30 -120 -36 -220 -20 -320 H20 C36 -220 30 -120 40 0Z" fill="{BARK}" stroke="#6e4526" stroke-width="8"/>'
            + crown + _apple(-120, -420) + _apple(60, -520) + _apple(-30, -330) + _apple(190, -470) + _apple(-200, -300)
            + f'<g id="{pid}-apple">{_apple(150, -330, 1.1)}</g></g>')


def apple(pid):
    """One apple, its bottom at (0, 0)."""
    return f'<g id="{pid}">{_apple(0, -46, 1.1)}</g>'


def ball(pid, col=RED, r=70, line="#7a1f1f", label=""):
    """A ball resting on (0, 0): a coloured circle with a white band and a shine."""
    return (f'<g id="{pid}"><circle cx="0" cy="{-r}" r="{r}" fill="{col}" stroke="{line}" stroke-width="{max(5, r // 9)}"/>'
            f'<path d="M{-r * .95:.0f} {-r * 1.15:.0f} Q0 {-r * .55:.0f} {r * .95:.0f} {-r * 1.15:.0f}" stroke="#fff" stroke-width="{max(6, r // 6)}" fill="none" opacity=".9"/>'
            f'<ellipse cx="{-r * .38:.0f}" cy="{-r * 1.45:.0f}" rx="{r * .18:.0f}" ry="{r * .26:.0f}" fill="#fff" opacity=".65"/></g>')


def heavy_ball(pid): return ball(pid, "#3a4a8c", 90, NAVY)       # big and heavy (dark blue)
def light_ball(pid): return ball(pid, SUN, 60, "#b8860b")         # small and light (yellow)


def feather(pid):
    """A soft white feather, its middle at (0, -70); -f is the feather itself (the engine sways it)."""
    vane = "".join(f'<path d="M{x} {y} q{-50 + k * 3} {-14} {-80 + k * 4} {-6}" stroke="#d9e2f2" stroke-width="5" fill="none"/>' for k, (x, y) in enumerate((( -8 + i * 2, -10 - i * 15) for i in range(9))))
    return (f'<g id="{pid}"><g id="{pid}-f"><path d="M0 0 C-10 -40 -6 -100 20 -150 C70 -110 50 -40 0 0Z" fill="#fff" stroke="#9fb0cc" stroke-width="6"/>'
            f'<path d="M0 0 C-10 -40 -6 -100 20 -150 C-40 -110 -60 -40 0 0Z" fill="#f2f6ff" stroke="#9fb0cc" stroke-width="6"/>'
            f'<path d="M-4 20 C2 -40 8 -100 20 -150" stroke="#8b97b0" stroke-width="6" fill="none" stroke-linecap="round"/></g></g>')


def rock(pid):
    """A grey rock resting on (0, 0)."""
    return (f'<g id="{pid}"><path d="M-70 0 C-80 -40 -50 -80 -10 -84 C40 -90 80 -60 76 -20 C74 0 40 4 0 4 C-30 4 -60 4 -70 0Z" fill="{ROCK}" stroke="{ROCKD}" stroke-width="8"/>'
            f'<circle cx="-20" cy="-50" r="9" fill="{ROCKD}" opacity=".6"/><circle cx="30" cy="-30" r="6" fill="{ROCKD}" opacity=".6"/></g>')


def floor(pid, w=1000):
    """A wooden floor strip on the board (top at y 0)."""
    return (f'<g id="{pid}"><rect x="{-w // 2}" y="0" width="{w}" height="60" rx="14" fill="#c98a4a" stroke="{NAVY}" stroke-width="8"/>'
            + "".join(f'<path d="M{x} 6 V54" stroke="#8a5a2a" stroke-width="5"/>' for x in range(-w // 2 + 120, w // 2, 160)) + '</g>')


def _arrow(x1, y1, x2, y2, col, w=22):
    ang = math.atan2(y2 - y1, x2 - x1); hx, hy = x2 - 40 * math.cos(ang), y2 - 40 * math.sin(ang)
    px, py = -math.sin(ang) * 34, math.cos(ang) * 34
    return (f'<path d="M{x1:.0f} {y1:.0f} L{hx:.0f} {hy:.0f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{hx + px:.0f} {hy + py:.0f} L{x2:.0f} {y2:.0f} L{hx - px:.0f} {hy - py:.0f}Z" fill="{col}"/>')


def down_arrow(pid, col=ACC):
    """One big arrow pointing down (-a, opacity 0), from (0, -160) to (0, 160)."""
    return f'<g id="{pid}"><g id="{pid}-a" opacity="0">{_arrow(0, -160, 0, 160, col, 40)}</g></g>'


def _person(col):
    """A tiny person standing on (0, 0), head up (the caller rotates it)."""
    return (f'<rect x="-14" y="-60" width="28" height="44" rx="10" fill="{col}" stroke="{NAVY}" stroke-width="5"/>'
            f'<path d="M-8 -16 V0 M8 -16 V0" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/>'
            f'<circle cx="0" cy="-78" r="20" fill="#ffd2a8" stroke="{NAVY}" stroke-width="5"/>')


def earth(pid, r=230):
    """The Earth, centre at (0, 0): ocean, land, -arr (four pull arrows from outside pointing at the centre, opacity 0), -ppl (four tiny people
    standing on the top, right, bottom and left, feet on the ground, heads away from the centre; opacity 0), -dot (the centre, opacity 0)."""
    land = (f'<path d="M{-r * .7:.0f} {-r * .4:.0f} C{-r * .4:.0f} {-r * .8:.0f} {-r * .05:.0f} {-r * .6:.0f} {-r * .1:.0f} {-r * .25:.0f} C{-r * .2:.0f} 0 {-r * .6:.0f} {r * .1:.0f} {-r * .7:.0f} {-r * .4:.0f}Z" fill="{LAND}"/>'
            f'<path d="M{r * .2:.0f} {r * .1:.0f} C{r * .5:.0f} {-r * .1:.0f} {r * .8:.0f} {r * .2:.0f} {r * .6:.0f} {r * .5:.0f} C{r * .4:.0f} {r * .75:.0f} {r * .1:.0f} {r * .5:.0f} {r * .2:.0f} {r * .1:.0f}Z" fill="{LAND}"/>'
            f'<path d="M{-r * .45:.0f} {r * .45:.0f} C{-r * .3:.0f} {r * .3:.0f} {-r * .1:.0f} {r * .5:.0f} {-r * .2:.0f} {r * .7:.0f} C{-r * .35:.0f} {r * .75:.0f} {-r * .5:.0f} {r * .6:.0f} {-r * .45:.0f} {r * .45:.0f}Z" fill="{LAND}"/>')
    arr = "".join(_arrow(math.cos(a) * (r + 230), math.sin(a) * (r + 230), math.cos(a) * (r * .35), math.sin(a) * (r * .35), SUN, 26)
                  for a in (math.radians(d) for d in (-135, -45, 45, 135)))
    ppl = "".join(f'<g transform="rotate({d}) translate(0 {-r})">{_person(c)}</g>' for d, c in ((0, ORANGE), (90, ACC), (180, "#ff7aa2"), (270, SUN)))
    return (f'<g id="{pid}"><circle r="{r}" fill="{SEA}" stroke="#9fd8ff" stroke-width="14"/>{land}'
            f'<g id="{pid}-ppl" opacity="0">{ppl}</g><g id="{pid}-arr" opacity="0">{arr}</g>'
            f'<g id="{pid}-dot" opacity="0"><circle r="20" fill="{SUN}" stroke="{NAVY}" stroke-width="6"/></g></g>')


def pulls(pid):
    """A small pull and a big pull side by side: a little ball at (-330, 0) with two short arrows (-a), the big Earth at (250, 0) with long
    arrows (-b); both arrow sets opacity 0."""
    small = ball(f"{pid}-sb", RED, 50) .replace(f'id="{pid}-sb"', f'id="{pid}-sb" transform="translate(-330 50)"')
    big = earth(f"{pid}-e", 200).replace(f'id="{pid}-e"', f'id="{pid}-e" transform="translate(250 0)"')
    a = "".join(_arrow(x1, 0, x2, 0, SUN, 12) for x1, x2 in ((-450, -400), (-210, -260)))
    b = "".join(_arrow(250 + math.cos(t) * 400, math.sin(t) * 330, 250 + math.cos(t) * 230, math.sin(t) * 200, SUN, 30) for t in (math.radians(d) for d in (180, -120, -60, 0, 60, 120)))
    return f'<g id="{pid}">{small}{big}<g id="{pid}-a" opacity="0">{a}</g><g id="{pid}-b" opacity="0">{b}</g></g>'


def _sun(r=130):
    rays = "".join(f'<path d="M0 {-r - 20} L0 {-r - 60}" stroke="#ffb020" stroke-width="16" stroke-linecap="round" transform="rotate({k * 30})"/>' for k in range(12))
    return (f'{rays}<circle r="{r}" fill="{SUN}" stroke="#ffb020" stroke-width="12"/><circle cx="-38" cy="-16" r="11" fill="{INK}"/><circle cx="38" cy="-16" r="11" fill="{INK}"/>'
            f'<path d="M-40 30 Q0 62 40 30" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/>')


def _globe(r):
    return (f'<circle r="{r}" fill="{SEA}" stroke="#9fd8ff" stroke-width="{max(6, r // 12)}"/>'
            f'<path d="M{-r * .6:.0f} {-r * .3:.0f} C{-r * .3:.0f} {-r * .7:.0f} 0 {-r * .5:.0f} {-r * .05:.0f} {-r * .1:.0f} C{-r * .3:.0f} {r * .1:.0f} {-r * .6:.0f} 0 {-r * .6:.0f} {-r * .3:.0f}Z" fill="{LAND}"/>'
            f'<path d="M{r * .2:.0f} {r * .2:.0f} C{r * .5:.0f} 0 {r * .7:.0f} {r * .3:.0f} {r * .5:.0f} {r * .55:.0f} C{r * .3:.0f} {r * .7:.0f} {r * .1:.0f} {r * .5:.0f} {r * .2:.0f} {r * .2:.0f}Z" fill="{LAND}"/>')


def _moon(r):
    return (f'<circle r="{r}" fill="#e8ecf4" stroke="#b6bfd2" stroke-width="{max(5, r // 10)}"/><circle cx="{-r * .3:.0f}" cy="{-r * .2:.0f}" r="{r * .22:.0f}" fill="#cfd6e4"/>'
            f'<circle cx="{r * .35:.0f}" cy="{r * .3:.0f}" r="{r * .16:.0f}" fill="#cfd6e4"/>')


def orbit_moon(pid, R=360):
    """The Earth at (0, 0) with the Moon's path (a dashed ring of radius R) and -spin, the group that carries the Moon (at (R, 0)); the engine
    turns -spin around (0, 0) (svgOrigin "0 0"). -pull: a short arrow from the Moon toward the Earth inside -spin (opacity 0)."""
    return (f'<g id="{pid}"><circle r="{R}" fill="none" stroke="#fff" stroke-width="6" stroke-dasharray="22 22" opacity=".55"/>{_globe(130)}'
            f'<g id="{pid}-spin"><g transform="translate({R} 0)">{_moon(60)}</g><g id="{pid}-pull" opacity="0">{_arrow(R - 80, 0, R - 200, 0, SUN, 18)}</g></g></g>')


def orbit_sun(pid, R=400):
    """The Sun at (0, 0) with the Earth's path (radius R) and -spin carrying the Earth (at (R, 0)); the engine turns -spin around (0, 0)."""
    return (f'<g id="{pid}"><circle r="{R}" fill="none" stroke="#fff" stroke-width="6" stroke-dasharray="22 22" opacity=".55"/>{_sun(120)}'
            f'<g id="{pid}-spin"><g transform="translate({R} 0)">{_globe(60)}</g></g></g>')
