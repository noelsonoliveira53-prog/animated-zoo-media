"""Art for zc_ep06 "What Does a Monkey Eat All Day?" (Nov 18 2026): three treetop places made from the canopy (a tree full of fruit,
a tree in flower, the treetops at sunset), Mango's friends (the same spider monkey drawing in three other fur colours), and the foods:
a green fruit, a fruit cut open with its seeds, young leaves, a flower, a piece of bark, a small insect, the six round food pictures.
Same hand as art.py / art2.py: flat fills, one warm dark outline. Nothing here changes an existing character, prop or place."""
import art, art2
from art import INK

# ------------------------------------------------------------------ Mango's friends: art2.monkey with other fur (Mango herself is unchanged)
FUR = {"monkey_b": {"fur": "#5d4a40", "dark": "#40312a", "face": "#f2d3b4", "line": "#2a1c14"},
       "monkey_c": {"fur": "#c08a4e", "dark": "#96683a", "face": "#fbe6c8", "line": "#4a2c14"},
       "monkey_d": {"fur": "#7d5a4a", "dark": "#5c3f33", "face": "#f6dcc0", "line": "#33201a"}}
for _k, _c in FUR.items():
    art2.RIGS[_k] = dict(build=(lambda c: lambda p: art2.monkey(p, c=c))(_c), neck=None, tail="40 -80", ear=None, legs=None, hip=0, jaw=("y", 12), eyes=["eyeL", "eyeR"], brows=["browL", "browR"])


# ------------------------------------------------------------------ places
def _small_fruit(pid, x, y, s=.3, green=False):
    return f'<path d="M{x} {y - 150 * s:.0f} V{y - 80 * s:.0f}" stroke="#6a4a26" stroke-width="6" stroke-linecap="round"/><g transform="translate({x} {y}) scale({s})">{(green_fruit if green else art2.fruit)(pid)}</g>'


def _up(col): return f'<rect x="-500" y="-1900" width="2920" height="1010" fill="{col}"/>'      # more sky above the canopy's own (it ends at y = -900): for the tall 9:16 views of the whole group


def bg_figtree(p):
    """A tree full of fruit, high in the treetops: the canopy's branch (y = 430), more leaves above it and golden fruit hanging under them."""
    far, mid, near = art2.bg_canopy(p)
    leaves = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/>' for x, y, rx, ry, c in
                     ((420, -40, 460, 170, "#3f9e5c"), (1500, -20, 520, 180, "#4fb56c"), (960, -130, 620, 150, "#3f9e5c"), (-260, 60, 300, 160, "#4fb56c"), (2200, 40, 320, 170, "#3f9e5c")))
    spots = ((150, 196), (330, 150), (560, 176), (760, 120), (1640, 186), (1820, 150), (1480, 130), (2050, 230), (-120, 250), (-330, 230), (2260, 250))
    fruit = "".join(_small_fruit(f"{p}bf{k}", x, y, .3, k in (3, 6)) for k, (x, y) in enumerate(spots))
    return _up("#9fe0ff") + far, mid + leaves + fruit, near


def _bloom(x, y, s=1.0, col="#ff8fb8", mid="#ffd23f"):
    pet = "".join(f'<ellipse cx="0" cy="-17" rx="11" ry="16" fill="{col}" transform="rotate({a})"/>' for a in range(0, 360, 72))
    return f'<g transform="translate({x} {y}) scale({s})">{pet}<circle r="9" fill="{mid}"/></g>'


def bg_blossom(p):
    """A tree in flower, high in the treetops: the canopy's branch, leaves and pink and white flowers, no fruit."""
    far, mid, near = art2.bg_canopy(p)
    leaves = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/>' for x, y, rx, ry, c in
                     ((380, -30, 480, 170, "#57c078"), (1540, -10, 520, 180, "#4fb56c"), (960, -140, 620, 150, "#57c078"), (-280, 50, 300, 160, "#4fb56c"), (2220, 30, 320, 170, "#57c078")))
    spots = ((90, 60, 1.5), (260, 110, 1.2), (470, 40, 1.6), (650, 96, 1.2), (820, 10, 1.4), (1330, 60, 1.3), (1500, 100, 1.6), (1700, 40, 1.3), (1860, 110, 1.5), (120, 180, 1.1), (1640, 180, 1.1),
             (-200, 130, 1.4), (-380, 80, 1.2), (2100, 120, 1.4), (2300, 90, 1.2), (560, -90, 1.3), (1200, -80, 1.4), (900, -150, 1.2), (1900, -60, 1.3), (200, -100, 1.3))
    blooms = "".join(_bloom(x, y, s, "#ff8fb8" if k % 3 else "#fff3f7") for k, (x, y, s) in enumerate(spots))
    return _up("#9fe0ff") + far, mid + leaves + blooms, near


def bg_canopy_eve(p):
    """The treetops when the sun goes down: the same branch in warm evening light."""
    far, mid, near = art2.bg_canopy(p)
    far = far.replace("#9fe0ff", "#ff9f6e").replace("#e4fbe6", "#ffe3a8").replace("#8fd09a", "#9bbf86").replace('cx="1640" cy="190"', 'cx="1560" cy="640"').replace("#ffe066", "#fff0a0")
    sw = {"#3f9e5c": "#3a8a55", "#4fb56c": "#4a9f62", "#2f8a4c": "#2b7845", "#57c078": "#52a86c", "#8a6238": "#84583a", "#735029": "#6c4729"}
    for a, b in sw.items(): mid = mid.replace(a, b); near = near.replace(a, b)
    return _up("#ff9f6e") + far, mid, near


art.BG.update({"figtree": bg_figtree, "blossom": bg_blossom, "canopy_eve": bg_canopy_eve})
art.PLACE.update({"figtree": "the fruit tree", "blossom": "the flower tree", "canopy_eve": "the treetops at sunset"})


# ------------------------------------------------------------------ foods
def green_fruit(pid):
    """The same fruit before it is ready: green."""
    s = art2.fruit(pid)
    for a, b in (("#ffb81f", "#9ccc5a"), ("#a8640a", "#4f7a2a"), ("#ffe08a", "#d9f2a6"), ("#f08a00", "#6fa83a")): s = s.replace(a, b)
    return s


def fruit_open(pid):
    """A fruit cut open: the soft inside and the little seeds."""
    seeds = "".join(f'<g id="{pid}-s{k}" transform="translate({x} {y}) rotate({r}) scale(.5)"><ellipse rx="26" ry="38" fill="#8a5a2c" stroke="#4a2c10" stroke-width="10"/><ellipse cx="-8" cy="-8" rx="7" ry="14" fill="#c08a52"/></g>'
                    for k, (x, y, r) in enumerate(((-32, -22, -20), (30, -30, 24), (0, 22, 4))))
    return (f'<g id="{pid}"><ellipse cx="0" cy="-10" rx="100" ry="108" fill="#ffb81f" stroke="#a8640a" stroke-width="10"/><ellipse cx="0" cy="-10" rx="80" ry="88" fill="#ffe9a8"/>'
            f'<ellipse cx="0" cy="-10" rx="56" ry="64" fill="#ffd66a"/>{seeds}</g>')


def leaves(pid):
    """Young leaves on a twig: soft and light green."""
    lf = lambda x, y, r, c: f'<path d="M0 0 C22 -44 78 -52 112 -14 C78 14 30 18 0 0Z" fill="{c}" stroke="#2f8a4c" stroke-width="7" stroke-linejoin="round" transform="translate({x} {y}) rotate({r})"/><path d="M0 0 L84 -12" stroke="#2f8a4c" stroke-width="5" stroke-linecap="round" transform="translate({x} {y}) rotate({r})"/>'
    return (f'<g id="{pid}"><path d="M-6 70 C-10 20 6 -30 0 -70" stroke="#6a4a26" stroke-width="10" fill="none" stroke-linecap="round"/>'
            + lf(0, 40, -24, "#8fd46a") + lf(-2, 14, -150, "#a6e07a") + lf(2, -26, -30, "#a6e07a") + lf(0, -64, -100, "#b8ea8c") + '</g>')


def leaf1(pid):
    """One young leaf (for Mango's hand)."""
    return f'<g id="{pid}"><path d="M-60 6 C-34 -44 34 -52 66 -8 C30 22 -26 26 -60 6Z" fill="#a6e07a" stroke="#2f8a4c" stroke-width="8" stroke-linejoin="round"/><path d="M-56 6 L44 -8" stroke="#2f8a4c" stroke-width="6" stroke-linecap="round"/></g>'


def flower(pid, col="#ff8fb8"):
    pet = "".join(f'<ellipse cx="0" cy="-46" rx="30" ry="44" fill="{col}" stroke="#c94a7c" stroke-width="7" transform="rotate({a})"/>' for a in range(0, 360, 72))
    return f'<g id="{pid}">{pet}<circle r="26" fill="#ffd23f" stroke="#c98a0a" stroke-width="7"/></g>'


def bark(pid):
    """A piece of bark: the skin of a tree."""
    return (f'<g id="{pid}"><path d="M-84 -56 L70 -70 L92 50 L-66 66Z" fill="#8a6238" stroke="#4a2c10" stroke-width="9" stroke-linejoin="round"/>'
            f'<path d="M-50 -34 q20 30 0 70 M-6 -48 q22 40 -2 86 M40 -46 q18 36 4 76" stroke="#5a3a1a" stroke-width="8" fill="none" stroke-linecap="round"/></g>')


def bug(pid):
    """A small insect: a little green beetle (no face: it is food, not a friend)."""
    legs = "".join(f'<path d="M{x} 0 l{dx} {dy}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>' for x, dx, dy in ((-28, -22, 34), (0, 0, 40), (28, 22, 34), (-28, -22, -34), (0, 0, -40), (28, 22, -34)))
    return (f'<g id="{pid}">{legs}<path d="M52 -10 q30 -22 44 -6 M52 10 q30 22 44 6" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            f'<circle cx="52" cy="0" r="24" fill="#3d5a2a" stroke="{INK}" stroke-width="7"/><ellipse cx="0" cy="0" rx="56" ry="40" fill="#6fbf4a" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M-52 0 H52" stroke="{INK}" stroke-width="6"/><ellipse cx="-14" cy="-18" rx="20" ry="8" fill="#c4f09a" opacity=".8"/></g>')


def trunk_piece(pid):
    """A piece of a tree trunk on the board, to show where bark is."""
    return (f'<g id="{pid}"><rect x="-120" y="-330" width="240" height="660" rx="26" fill="#8a6238" stroke="#4a2c10" stroke-width="11"/>'
            + "".join(f'<path d="M{x} {y} q22 36 0 84" stroke="#5a3a1a" stroke-width="9" fill="none" stroke-linecap="round"/>' for x, y in ((-70, -270), (20, -230), (-30, -90), (60, -40), (-76, 60), (10, 130), (64, 210), (-40, 230)))
            + '</g>')


def swatch(pid, col):
    """A blob of colour."""
    return f'<g id="{pid}"><path d="M-70 -10 C-76 -66 -10 -84 30 -66 C84 -60 96 0 60 40 C30 80 -50 70 -70 -10Z" fill="{col}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/><ellipse cx="-20" cy="-34" rx="24" ry="12" fill="#fff" opacity=".45" transform="rotate(-20 -20 -34)"/></g>'


def sun_small(pid):
    rays = "".join(f'<path d="M0 -96 V-130" stroke="#f5a623" stroke-width="14" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 45))
    return f'<g id="{pid}"><g id="{pid}-rays">{rays}</g><circle r="74" fill="#ffd23f" stroke="#c98a0a" stroke-width="9"/></g>'


def food(k):
    """One of the six foods as a round picture: fruit, leaves, flowers, seeds, bark, bugs."""
    def f(pid):
        ic = [f'<g transform="translate(0 26) scale(.78)">{art2.fruit(pid + "i")}</g>', f'<g transform="translate(-6 6) scale(.92)">{leaves(pid + "i")}</g>',
              f'<g transform="scale(.9)">{flower(pid + "i")}</g>',
              "".join(f'<g transform="translate({x} {y}) scale(.9)">{art2.seed(pid + "i" + str(n))}</g>' for n, (x, y) in enumerate(((-40, -20), (36, -34), (4, 40)))),
              f'<g transform="scale(.92)">{bark(pid + "i")}</g>', f'<g transform="translate(-10 0) scale(.9)">{bug(pid + "i")}</g>'][k]
        return f'<g id="{pid}"><circle r="108" fill="#fff" stroke="{INK}" stroke-width="10"/>{ic}</g>'
    return f


def dish(pid, what="fruit"):
    """One bite on the ten-bites board: a round plate with a fruit, or with leaves and a flower."""
    ic = f'<g transform="translate(0 22) scale(.66)">{art2.fruit(pid + "i")}</g>' if what == "fruit" else (f'<g transform="translate(-22 4) scale(.66)">{leaves(pid + "i")}</g><g transform="translate(38 20) scale(.42)">{flower(pid + "j")}</g>')
    return f'<g id="{pid}"><circle r="96" fill="#fff" stroke="{INK}" stroke-width="9"/><circle r="74" fill="none" stroke="#e8dcc0" stroke-width="6"/>{ic}</g>'


def empty_dish(pid): return f'<g id="{pid}"><circle r="96" fill="#fff" stroke="{INK}" stroke-width="9" stroke-dasharray="20 16" opacity=".55"/></g>'
