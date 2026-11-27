"""Pictures for zc_ep15 "Is a Polar Bear Really White?" (Nov 27 2026). New props only: no character, place or older prop is drawn differently.
Poppy (art2 "bear"), the Arctic places and the props of zc_ep13 (art_zc_ep13: coat, pointer, water_front, splash) are reused as they are.

Props (each anchored as written):
  lens_hair(p)     a big magnifying glass (handle down-right) with ONE polar bear hair across the glass: the hair is see-through (pale glassy
                   outline, the blue of the glass shows through it) with an empty middle (-hair). Glass radius 300, anchored at the glass middle.
  hair_tube(p)     one hair drawn big, standing up, cut open so the middle shows: a clear outer wall and an EMPTY middle full of air (-core: the air
                   column, light blue with little round air spaces). About 300 x 900, anchored at its middle.
  sun_bounce(p)    the same big hair with sunbeams: yellow beams come in from the top left (-in0..-in2, shown one by one), white sparkles bounce out
                   all round (-out: a ring of short white rays, shown last). About 900 x 900, anchored at the hair's middle.
  skin_board(p)    a picture board: clear hairs (glassy outlines) standing on a band of BLACK skin (-skin), a small sun in the top corner (-sun) and
                   three yellow beams that go through the clear hairs down to the skin (-rays), a warm orange glow along the skin (-warm, opacity 0).
                   About 900 x 600, anchored at its middle.
  fur_swatches(p)  two round fur patches side by side: bright white (-white, left) and soft yellow (-yellow, right, a little sun above it). About
                   900 x 420, anchored at its middle.
  finger_lens(p)   a hand-drawn circle of two fingers' size to show "make a magnifying glass with your fingers" (an orange ring with a shine),
                   radius 110, anchored at its middle.
"""
import random
import art

INK = art.INK
GLASS = "#bfe8ff"
HAIR_LINE = "#5f8fb8"


def _hair(x0, y0, x1, y1, w=46, core=True):
    """A see-through hair from (x0, y0) to (x1, y1): a pale glassy outline and, inside, a thinner empty middle (dashed)."""
    out = (f'<path d="M{x0} {y0} L{x1} {y1}" stroke="{HAIR_LINE}" stroke-width="{w}" stroke-linecap="round" opacity=".9"/>'
           f'<path d="M{x0} {y0} L{x1} {y1}" stroke="#eef9ff" stroke-width="{w - 14}" stroke-linecap="round" opacity=".55"/>')
    if core:
        out += f'<path d="M{x0} {y0} L{x1} {y1}" stroke="#ffffff" stroke-width="{max(6, w // 4)}" stroke-dasharray="26 18" stroke-linecap="round"/>'
    return out


def lens_hair(p):
    R = 300
    handle = (f'<path d="M210 210 L420 420" stroke="{INK}" stroke-width="86" stroke-linecap="round"/>'
              f'<path d="M210 210 L420 420" stroke="#ff9f43" stroke-width="56" stroke-linecap="round"/>')
    glass = f'<circle r="{R}" fill="{GLASS}" fill-opacity=".55"/>'
    hair = f'<g id="{p}-hair">{_hair(-240, 115, 240, -115, 104)}</g>'
    rim = (f'<circle r="{R}" fill="none" stroke="{INK}" stroke-width="40"/><circle r="{R}" fill="none" stroke="#d9dee8" stroke-width="22"/>'
           f'<path d="M-170 -170 Q-90 -240 20 -236" stroke="#ffffff" stroke-width="22" fill="none" stroke-linecap="round" opacity=".85"/>')
    return f'<g id="{p}">{handle}{glass}{hair}{rim}</g>'


def hair_tube(p, H=900, W=260):
    r = random.Random(3)
    wall = (f'<rect x="{-W // 2}" y="{-H // 2}" width="{W}" height="{H}" rx="{W // 2}" fill="#f4fbff" fill-opacity=".55" stroke="{HAIR_LINE}" stroke-width="18"/>'
            f'<path d="M{-W // 2 + 30} {-H // 2 + 120} V{H // 2 - 120}" stroke="#ffffff" stroke-width="16" stroke-linecap="round" opacity=".9"/>')
    cw = W // 2
    bubbles = "".join(f'<circle cx="{r.uniform(-cw / 2 + 18, cw / 2 - 18):.0f}" cy="{y:.0f}" r="{r.uniform(14, 24):.0f}" fill="#ffffff" stroke="#a9d6f5" stroke-width="5"/>'
                      for y in range(-H // 2 + 110, H // 2 - 90, 62))
    core = f'<g id="{p}-core"><rect x="{-cw // 2}" y="{-H // 2 + 60}" width="{cw}" height="{H - 120}" rx="{cw // 2}" fill="#dff3ff" stroke="#a9d6f5" stroke-width="8"/>{bubbles}</g>'
    return f'<g id="{p}">{wall}{core}</g>'


def sun_bounce(p):
    tube = hair_tube(p + "-t", 760, 220)
    beams = ""
    for k, (x, y) in enumerate(((-420, -360), (-460, -170), (-400, 20))):
        beams += (f'<g id="{p}-in{k}"><path d="M{x} {y} L{-70} {y + 300}" stroke="#ffb627" stroke-width="30" stroke-linecap="round"/>'
                  f'<path d="M{-70} {y + 300} l-64 -10 l34 -50Z" fill="#ffb627"/></g>')
    rays = "".join(f'<path d="M0 -150 V-280" stroke="#ffb627" stroke-width="40" stroke-linecap="round" transform="rotate({a})"/>'
                   f'<path d="M0 -150 V-280" stroke="#fff6c8" stroke-width="18" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 30))
    out = f'<g id="{p}-out" transform="translate(0 0)">{rays}<circle r="60" fill="#ffffff" opacity=".7"/></g>'
    sun = (f'<g transform="translate(-380 -400)"><circle r="70" fill="#ffd23f" stroke="#e8a317" stroke-width="10"/>'
           + "".join(f'<path d="M0 -84 V-118" stroke="#ffd23f" stroke-width="14" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 45)) + '</g>')
    return f'<g id="{p}">{tube}{beams}{out}{sun}</g>'


def skin_board(p):
    W, H = 900, 600
    x0, y0 = -W // 2, -H // 2
    frame = f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" rx="36" fill="#d9efff" stroke="{INK}" stroke-width="14"/>'
    sky_y = 150
    skin = f'<g id="{p}-skin"><rect x="{x0 + 22}" y="{sky_y}" width="{W - 44}" height="{H // 2 - sky_y - 22}" rx="14" fill="#23282f"/></g>'
    warm = f'<g id="{p}-warm" opacity="0"><rect x="{x0 + 22}" y="{sky_y - 10}" width="{W - 44}" height="70" rx="30" fill="#ff8c2a" opacity=".55"/></g>'
    r = random.Random(8)
    hairs = "".join(_hair(x, sky_y + 6, x + r.uniform(20, 50), sky_y - r.uniform(250, 300), 34) for x in range(x0 + 80, -x0 - 60, 70))
    sun = (f'<g id="{p}-sun" transform="translate({x0 + 110} {y0 + 100})"><circle r="56" fill="#ffd23f" stroke="#e8a317" stroke-width="9"/>'
           + "".join(f'<path d="M0 -68 V-96" stroke="#ffd23f" stroke-width="12" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 45)) + '</g>')
    rays = '<g id="' + p + '-rays">' + "".join(
        f'<path d="M{x0 + 170 + k * 40} {y0 + 150 + k * 10} L{x} {sky_y + 30}" stroke="#ffb627" stroke-width="20" stroke-linecap="round" stroke-dasharray="40 24"/>'
        for k, x in enumerate((-160, 40, 240))) + '</g>'
    return f'<g id="{p}">{frame}{skin}{warm}<g>{hairs}</g>{rays}{sun}</g>'


def _fur_patch(cx, col, edge, seed):
    r = random.Random(seed)
    tufts = "".join(f'<path d="M{cx + r.uniform(-120, 120):.0f} {r.uniform(-90, 110):.0f} q{r.uniform(-20, 20):.0f} -50 {r.uniform(-14, 14):.0f} -86" stroke="{edge}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".7"/>' for _ in range(14))
    return f'<circle cx="{cx}" cy="0" r="170" fill="{col}" stroke="{INK}" stroke-width="12"/>{tufts}'


def fur_swatches(p):
    white = f'<g id="{p}-white">{_fur_patch(-230, "#ffffff", "#c9d6e2", 1)}</g>'
    sun = (f'<g transform="translate(360 -190)"><circle r="44" fill="#ffd23f" stroke="#e8a317" stroke-width="8"/>'
           + "".join(f'<path d="M0 -54 V-76" stroke="#ffd23f" stroke-width="10" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 45)) + '</g>')
    yellow = f'<g id="{p}-yellow">{_fur_patch(230, "#fbe7a6", "#d9b864", 2)}{sun}</g>'
    return f'<g id="{p}">{white}{yellow}</g>'


def finger_lens(p):
    return (f'<g id="{p}"><circle r="110" fill="none" stroke="#ff9f43" stroke-width="34"/><circle r="110" fill="none" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M-60 -60 Q-20 -90 30 -86" stroke="#ffffff" stroke-width="12" fill="none" stroke-linecap="round"/></g>')
