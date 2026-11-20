"""Pictures for za_ep08 "The Long Walk to the Oasis" (Nov 19 2026). New props only: no character, place or older prop is drawn differently.
Uses kit.PT["camel"] (registered by art_za_ep07) for Mama camel.

  tree(p)         the zoo garden's little tree on a mound of earth. Two crowns in one prop: #<p>-sad (droopy, pale leaves hanging down)
                  and #<p>-glad (round, bright green, pink flowers; starts hidden). Anchored at the mound's foot, middle.
  can(p)          a watering can (spout to the right). #<p>-pour: three drops under the spout (start hidden). Anchored at its foot.
  pack(p)         two little water jugs on a saddle pad, for Sandy's back (side view: the near jug hangs in front, the far jug peeks out
                  behind it). Anchored at the middle of the pad's underside: put it on Sandy's "back" point.
  big_pack(p)     a grown camel's big load (two bundles and a rolled blanket on a saddle pad) for the fact board. Anchored like pack.
  jug_grid(p)     thirty small jugs in three rows of ten, each row a group #<p>-r0 .. -r2 (they pop in row by row). Anchored at the middle.
  pond_fill(p)    water drops going into a jug (the jugs are filled at the oasis). Anchored at the jug's mouth.
"""
import art, kit, art_za_ep07     # art_za_ep07 registers kit.PT["camel"]

LEAF_SAD, LEAF_SAD_D = "#b9c46a", "#7f8a3a"
LEAF, LEAF_D, LEAF_L = "#4fb565", "#2f8a4c", "#78d68e"
TRUNK, TRUNK_D = "#9a6a3a", "#5a3a1a"


def tree(p):
    mound = f'<ellipse cx="0" cy="-6" rx="150" ry="40" fill="#8a5a2c" stroke="#5a3a1a" stroke-width="8"/><ellipse cx="-40" cy="-20" rx="40" ry="10" fill="#a8713f"/>'
    trunk = f'<path d="M-16 -20 C-14 -110 -20 -170 -10 -230 L12 -230 C18 -170 14 -110 16 -20Z" fill="{TRUNK}" stroke="{TRUNK_D}" stroke-width="8" stroke-linejoin="round"/>'
    hang = lambda x, y, r: (f'<g transform="translate({x} {y}) rotate({r})"><path d="M0 0 C-22 30 -18 80 0 100 C18 80 22 30 0 0Z" fill="{LEAF_SAD}" stroke="{LEAF_SAD_D}" stroke-width="7" stroke-linejoin="round"/></g>')
    sad = (f'<g id="{p}-sad"><path d="M0 -226 C-60 -250 -110 -230 -130 -170 M0 -226 C60 -250 110 -230 130 -170 M0 -228 C-20 -270 10 -290 30 -250" stroke="{TRUNK_D}" stroke-width="12" fill="none" stroke-linecap="round"/>'
           + "".join(hang(x, y, r) for x, y, r in ((-130, -172, 12), (-80, -232, 6), (-30, -240, -4), (30, -250, 4), (80, -234, -6), (130, -172, -12), (30, -252, 8)))
           + '</g>')
    flower = lambda x, y: f'<g transform="translate({x} {y})">' + "".join(f'<circle cx="{dx}" cy="{dy}" r="13" fill="#ff8fb1"/>' for dx, dy in ((0, -14), (14, 0), (0, 14), (-14, 0))) + '<circle r="9" fill="#ffd23f"/></g>'
    glad = (f'<g id="{p}-glad" opacity="0"><circle cx="0" cy="-320" r="120" fill="{LEAF_D}"/><circle cx="-90" cy="-270" r="86" fill="{LEAF_D}"/><circle cx="92" cy="-272" r="88" fill="{LEAF_D}"/>'
            f'<circle cx="0" cy="-326" r="110" fill="{LEAF}"/><circle cx="-86" cy="-276" r="76" fill="{LEAF}"/><circle cx="88" cy="-278" r="78" fill="{LEAF}"/>'
            f'<circle cx="-40" cy="-370" r="40" fill="{LEAF_L}" opacity=".8"/>' + flower(-70, -300) + flower(40, -380) + flower(90, -260) + flower(-10, -250) + '</g>')
    return f'<g id="{p}">{mound}{trunk}{sad}{glad}</g>'


def can(p):
    drop = lambda x, y: f'<path d="M{x} {y - 26} C{x + 14} {y - 8} {x + 18} {y} {x + 18} {y + 8} A18 18 0 0 1 {x - 18} {y + 8} C{x - 18} {y} {x - 14} {y - 8} {x} {y - 26}Z" fill="#7fd3f7" stroke="#2b7fb0" stroke-width="5"/>'
    return (f'<g id="{p}"><path d="M60 -120 L190 -200 L204 -186 L84 -86Z" fill="#5fb0e0" stroke="#24628c" stroke-width="8" stroke-linejoin="round"/>'
            f'<ellipse cx="204" cy="-196" rx="22" ry="12" fill="#3f8fc4" stroke="#24628c" stroke-width="6" transform="rotate(-34 204 -196)"/>'
            f'<path d="M-90 0 L-80 -150 L80 -150 L90 0Z" fill="#6fc0ef" stroke="#24628c" stroke-width="9" stroke-linejoin="round"/>'
            f'<path d="M-60 -150 C-60 -230 60 -230 60 -150" fill="none" stroke="#24628c" stroke-width="16" stroke-linecap="round"/>'
            f'<rect x="-60" y="-110" width="120" height="22" rx="10" fill="#fff" opacity=".45"/>'
            f'<g id="{p}-pour" opacity="0">{drop(222, -150)}{drop(240, -90)}{drop(226, -36)}</g></g>')


def _jug(x, y, s=1.0, rot=0):
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">' + art.jug("j").replace('id="j"', "") + '</g>'


def pack(p):
    pad = (f'<path d="M-150 0 C-150 -50 150 -50 150 0 L136 30 C60 44 -60 44 -136 30Z" fill="#e85d5d" stroke="#8c2a2a" stroke-width="8" stroke-linejoin="round"/>'
           f'<path d="M-130 18 C-60 30 60 30 130 18" stroke="#ffd23f" stroke-width="10" fill="none" stroke-dasharray="20 14"/>')
    far = _jug(70, 10, .95)
    near = (f'<path d="M-44 6 L-44 120 M44 6 L44 120" stroke="#8c5a2c" stroke-width="10" stroke-linecap="round"/>' + _jug(0, 240, 1.25))
    return f'<g id="{p}"><g opacity=".85">{far}</g>{pad}{near}</g>'


def big_pack(p):
    bundle = lambda x, c, d: f'<rect x="{x - 90}" y="-150" width="180" height="150" rx="34" fill="{c}" stroke="{d}" stroke-width="9"/><path d="M{x - 90} -80 H{x + 90}" stroke="{d}" stroke-width="10"/>'
    return (f'<g id="{p}"><path d="M-260 0 C-260 -60 260 -60 260 0 L240 40 C100 56 -100 56 -240 40Z" fill="#e85d5d" stroke="#8c2a2a" stroke-width="9"/>'
            + bundle(-120, "#f2c14e", "#9a6a1a") + bundle(120, "#7fc6a4", "#2f7a5a")
            + f'<rect x="-150" y="-230" width="300" height="86" rx="43" fill="#9fb8ff" stroke="#3d5aa8" stroke-width="9"/><path d="M-90 -230 V-144 M90 -230 V-144" stroke="#3d5aa8" stroke-width="9"/></g>')


def jug_grid(p):
    rows = []
    for r in range(3):
        rows.append(f'<g id="{p}-r{r}">' + "".join(_jug(-585 + k * 130, -110 + r * 170, .9) for k in range(10)) + '</g>')
    return f'<g id="{p}">{"".join(rows)}</g>'


def pond_fill(p):
    return f'<g id="{p}">' + "".join(f'<g transform="translate({x} {y}) scale(.5)">{art.water_drop(f"{p}-d{k}")}</g>' for k, (x, y) in enumerate(((0, -120), (-14, -70), (8, -30)))) + '</g>'
