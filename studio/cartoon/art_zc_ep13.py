"""Pictures for zc_ep13 "How Do Polar Bears Stay Warm?" (Nov 21 2026). New props only: no character, place or older prop is drawn differently.
Poppy (art2 "bear"), the Arctic places (art2 "arctic", art_za_ep10 "snowbottom", art_za_ep11 "arctic_low") and the coat cut-away
(art_za_ep11.warm_layers: -fat, -skin, -under, -guard) are reused as they are.

Props (each anchored as written):
  thermometer(p)   a little thermometer, bulb at the bottom; -lvl is the blue level (scaleY from its bottom). Anchored at the middle of the bulb.
  fat_ruler(p)     a picture board: a slice of the bear's side, white fur on top, the skin, then the thick yellow fat, and a ruler beside the fat
                   with four inch marks -m1 .. -m4 (bottom to top) and the fat slab -fat. About 900 x 560, anchored at its middle.
  glow_ring(p)     a soft warm blanket of light round a body: a wide orange ring (-ring) with a dashed edge; anchored at its middle (1 = 520 x 340).
  water_front(p)   the icy sea in front of a swimmer: a blue band with a wavy top (-wv) and white glints; y = 0 is the water line, 2600 wide.
  drops(p)         four rain drops (-d0 .. -d3) side by side 120 apart, anchored at the middle drop pair.
  paw_sole(p)      the bottom of a polar bear foot, seen from below: black pads, soft white fur round them and between the toes (-fur, tufts);
                   about 620 x 700, anchored at its middle.
  den_cut(p)       a snow den cut open like a cake: a snow mound, inside a dark-blue room with a warm glow (-glow), a mama bear (-mama) and a cub
                   (-cub) curled up against her; cold wind lines outside (-wind). About 1500 x 760, anchored at the middle of its base.
  ice_floor(p)     a strip of slippery blue ice with shine lines; anchored at the middle of its top edge (1400 wide).
"""
import math, random
import art, art2

INK = art.INK


def thermometer(p):
    tube = f'<rect x="-34" y="-420" width="68" height="420" rx="34" fill="#ffffff" stroke="{INK}" stroke-width="12"/>'
    lvl = f'<g id="{p}-lvl"><rect x="-16" y="-370" width="32" height="370" rx="16" fill="#e8402f"/></g>'
    bulb = f'<circle cx="0" cy="0" r="62" fill="#e8402f" stroke="{INK}" stroke-width="12"/><circle cx="-18" cy="-18" r="14" fill="#fff" opacity=".6"/>'
    ticks = "".join(f'<path d="M34 {-120 - k * 60} h26" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>' for k in range(5))
    flake = '<g transform="translate(110 -380)">' + "".join(f'<path d="M0 0 L0 -40" stroke="#7cc4ff" stroke-width="9" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 60)) + '</g>'
    return f'<g id="{p}">{tube}{lvl}{bulb}{ticks}{flake}</g>'


def fat_ruler(p):
    W, H = 900, 560
    x0, y0 = -W // 2, -H // 2
    r = random.Random(5)
    frame = f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" rx="36" fill="#eaf6ff" stroke="{INK}" stroke-width="14"/>'
    fur_y, skin_y, fat_y, fat_b = -230, -150, -126, 230            # tops of the fur, skin, fat; bottom of the fat
    fx0, fx1 = x0 + 30, 230                                         # the slab, left of the ruler
    fur = (f'<rect x="{fx0}" y="{fur_y}" width="{fx1 - fx0}" height="{skin_y - fur_y}" fill="#f6eedb"/>'
           + "".join(f'<path d="M{x} {skin_y} q{r.uniform(-12, 12):.0f} -40 {r.uniform(-8, 8):.0f} {fur_y - skin_y + 6}" stroke="#ffffff" stroke-width="14" fill="none" stroke-linecap="round"/>' for x in range(fx0 + 20, fx1 - 10, 24)))
    skin = f'<rect x="{fx0}" y="{skin_y}" width="{fx1 - fx0}" height="{fat_y - skin_y}" fill="#2f3640"/>'
    fat = (f'<g id="{p}-fat"><rect x="{fx0}" y="{fat_y}" width="{fx1 - fx0}" height="{fat_b - fat_y}" rx="18" fill="#ffd779" stroke="#d8a53a" stroke-width="8"/>'
           + "".join(f'<circle cx="{r.uniform(fx0 + 40, fx1 - 40):.0f}" cy="{r.uniform(fat_y + 30, fat_b - 30):.0f}" r="{r.uniform(12, 22):.0f}" fill="#ffe7a8"/>' for _ in range(18)) + '</g>')
    rx = 300                                                        # the ruler
    ruler = f'<rect x="{rx - 50}" y="{fat_y - 20}" width="100" height="{fat_b - fat_y + 40}" rx="16" fill="#ffb347" stroke="{INK}" stroke-width="10"/>'
    step = (fat_b - fat_y) / 4
    marks = ""
    for k in range(1, 5):
        y = fat_b - step * k
        marks += (f'<g id="{p}-m{k}"><path d="M{rx - 50} {y:.0f} h60" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
                  f'<circle cx="{rx + 26}" cy="{y + step / 2:.0f}" r="30" fill="#fff" stroke="{INK}" stroke-width="7"/>'
                  f'<text x="{rx + 26}" y="{y + step / 2 + 14:.0f}" font-family="Fredoka, Nunito, sans-serif" font-weight="700" font-size="42" text-anchor="middle" fill="{INK}">{k}</text></g>')
    base = f'<path d="M{rx - 50} {fat_b} h60" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
    return f'<g id="{p}">{frame}{fur}{skin}{fat}{ruler}{base}{marks}</g>'


def glow_ring(p):
    return (f'<g id="{p}"><g id="{p}-ring"><ellipse rx="520" ry="340" fill="none" stroke="#ffb347" stroke-width="70" opacity=".45"/>'
            f'<ellipse rx="520" ry="340" fill="none" stroke="#ff8c2a" stroke-width="12" stroke-dasharray="40 28" stroke-linecap="round"/></g></g>')


def water_front(p, w=2600):
    x0 = -w // 2
    wave = " ".join(f"q60 -34 120 0 q60 34 120 0" for _ in range(w // 240 + 2))
    band = (f'<g id="{p}-wv"><path d="M{x0 - 240} 0 {wave} L{x0 + w + 240} 700 L{x0 - 240} 700Z" fill="#5fb3e6"/>'
            f'<path d="M{x0 - 240} 0 {wave}" stroke="#ffffff" stroke-width="14" fill="none" stroke-linecap="round" opacity=".85"/></g>')
    glints = "".join(f'<path d="M{x} {y} h{l}" stroke="#ffffff" stroke-width="10" stroke-linecap="round" opacity=".6"/>' for x, y, l in ((x0 + 300, 90, 120), (-200, 150, 160), (500, 80, 110), (x0 + w - 400, 160, 140)))
    deep = f'<rect x="{x0 - 240}" y="230" width="{w + 480}" height="470" fill="#4aa0d8"/>'
    return f'<g id="{p}">{band}{deep}{glints}</g>'


def _drop(x, y, s=1.0):
    return (f'<path d="M{x} {y - 50 * s:.0f} C{x + 30 * s:.0f} {y - 10 * s:.0f} {x + 32 * s:.0f} {y + 22 * s:.0f} {x} {y + 30 * s:.0f} '
            f'C{x - 32 * s:.0f} {y + 22 * s:.0f} {x - 30 * s:.0f} {y - 10 * s:.0f} {x} {y - 50 * s:.0f}Z" fill="#7cc4ff" stroke="#2c7fc1" stroke-width="7"/>'
            f'<ellipse cx="{x - 10 * s:.0f}" cy="{y + 6 * s:.0f}" rx="7" ry="11" fill="#fff" opacity=".7"/>')


def drops(p):
    return f'<g id="{p}">' + "".join(f'<g id="{p}-d{k}">{_drop(-180 + k * 120, 0)}</g>' for k in range(4)) + '</g>'


def paw_sole(p):
    fur_c, ln = "#fdfaf2", "#6a5a4c"
    sole = f'<ellipse cx="0" cy="40" rx="290" ry="330" fill="{fur_c}" stroke="{ln}" stroke-width="14"/>'
    r = random.Random(9)
    tufts = "".join(f'<path d="M{x:.0f} {y:.0f} q{r.uniform(-10, 10):.0f} -30 {r.uniform(-14, 14):.0f} -54" stroke="#e3d8c2" stroke-width="12" fill="none" stroke-linecap="round"/>'
                    for x, y in ((r.uniform(-230, 230), r.uniform(-200, 330)) for _ in range(46)))
    pads = (f'<ellipse cx="0" cy="150" rx="150" ry="105" fill="#2a2320"/>'
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="52" ry="62" fill="#2a2320"/>' for x, y in ((-170, -100), (-70, -170), (60, -170), (160, -100), (220, 10))))
    fur_between = "".join(f'<path d="M{x} {y} q-12 -26 4 -50 M{x + 14} {y + 4} q10 -24 -2 -48" stroke="{fur_c}" stroke-width="13" fill="none" stroke-linecap="round"/>'
                          for x, y in ((-128, -110), (-4, -150), (118, -110), (200, -30), (-150, 20), (170, 60)))
    return f'<g id="{p}">{sole}<g id="{p}-fur">{tufts}</g>{pads}<g id="{p}-fur2">{fur_between}</g></g>'


def den_cut(p):
    ln = INK
    mound = f'<path d="M-760 0 C-700 -520 -300 -760 0 -760 C300 -760 700 -520 760 0Z" fill="#ffffff" stroke="#b9dcf5" stroke-width="16"/>'
    room = f'<path d="M-500 -20 C-470 -380 -240 -520 0 -520 C240 -520 470 -380 500 -20Z" fill="#3f5fa8"/>'
    glow = f'<g id="{p}-glow"><ellipse cx="0" cy="-200" rx="360" ry="250" fill="#ffd27a" opacity=".38"/><ellipse cx="0" cy="-180" rx="250" ry="170" fill="#ffd27a" opacity=".32"/></g>'
    door = f'<path d="M560 0 C560 -170 640 -230 720 -230 L760 -40 L760 0Z" fill="#2c4a8a"/>'
    floor = f'<rect x="-520" y="-30" width="1040" height="30" fill="#dcefff"/>'
    mama = f'<g id="{p}-mama"><g transform="translate(-60 -30) scale(.78)">{art2.bear(p + "-mb")}</g></g>'
    cub = f'<g id="{p}-cub"><g transform="translate(250 -30) scale(.4)">{art2.bear(p + "-cb")}</g></g>'
    wind = "".join(f'<path d="M{x} {y} q60 -26 120 0 q60 26 120 0" stroke="#9cc8ea" stroke-width="12" fill="none" stroke-linecap="round"/>' for x, y in ((830, -520), (880, -380), (820, -250)))
    return f'<g id="{p}">{mound}{room}{glow}{floor}{mama}{cub}{door}<g id="{p}-wind">{wind}</g></g>'


def ice_floor(p, w=1400):
    x0 = -w // 2
    return (f'<g id="{p}"><rect x="{x0}" y="0" width="{w}" height="120" rx="30" fill="#bfe6ff" stroke="#7cc4ff" stroke-width="10"/>'
            + "".join(f'<path d="M{x} 30 l70 -0 M{x + 30} 70 l90 0" stroke="#ffffff" stroke-width="10" stroke-linecap="round"/>' for x in range(x0 + 80, -x0 - 160, 260)) + '</g>')


def coat(p):
    """A cut through a polar bear's coat (clearer than art_za_ep11.warm_layers for a lesson about the layers): the thick yellow fat at the
    bottom (-fat), the skin (-skin), the soft, thick undercoat as a band of fluffy cream curls (-under), long guard hairs on top, white with a
    blue-grey line so they read against the sky (-guard). About 900 x 640, anchored at its middle."""
    W, H = 900, 640
    x0, y0 = -W // 2, -H // 2
    r = random.Random(13)
    frame = f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" rx="36" fill="#d9efff" stroke="{INK}" stroke-width="14"/>'
    fat_y, skin_y, under_y = 150, 124, 10
    fat = (f'<g id="{p}-fat"><rect x="{x0 + 22}" y="{fat_y}" width="{W - 44}" height="{H // 2 - fat_y - 22}" rx="18" fill="#ffd779" stroke="#d8a53a" stroke-width="8"/>'
           + "".join(f'<circle cx="{r.uniform(x0 + 60, -x0 - 60):.0f}" cy="{r.uniform(fat_y + 30, H // 2 - 50):.0f}" r="{r.uniform(10, 18):.0f}" fill="#ffe7a8"/>' for _ in range(16)) + '</g>')
    skin = f'<g id="{p}-skin"><rect x="{x0 + 22}" y="{skin_y}" width="{W - 44}" height="{fat_y - skin_y}" fill="#2f3640"/></g>'
    curls = "".join(f'<circle cx="{x + r.uniform(-8, 8):.0f}" cy="{y + r.uniform(-8, 8):.0f}" r="{r.uniform(24, 32):.0f}" fill="#fff6e0" stroke="#d6c08f" stroke-width="6"/>'
                    for y in (skin_y - 24, skin_y - 62, skin_y - 98) for x in range(x0 + 50, -x0 - 30, 46))
    under = f'<g id="{p}-under"><rect x="{x0 + 22}" y="{under_y}" width="{W - 44}" height="{skin_y - under_y}" fill="#f3e3bd"/>{curls}</g>'
    hairs = ""
    for x in range(x0 + 60, -x0 - 60, 56):
        d = f"M{x} {skin_y - 20} q{r.uniform(10, 30):.0f} -160 {r.uniform(50, 80):.0f} -{r.uniform(330, 370):.0f}"
        hairs += (f'<path d="{d}" stroke="#5b86ad" stroke-width="22" fill="none" stroke-linecap="round"/>'
                  f'<path d="{d}" stroke="#ffffff" stroke-width="11" fill="none" stroke-linecap="round"/>')
    guard = f'<g id="{p}-guard">{hairs}</g>'
    return f'<g id="{p}">{frame}<g>{fat}{skin}{guard}{under}</g></g>'


def splash(p):
    """A water splash: white drops flying up and out from 0 0 (the water line)."""
    r = random.Random(4)
    drops = "".join(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s:.0f}" ry="{s * 1.3:.0f}" fill="#ffffff" stroke="#7cc4ff" stroke-width="6"/>'
                    for x, y, s in ((r.uniform(-220, 220), r.uniform(-260, -40), r.uniform(14, 26)) for _ in range(16)))
    crown = '<path d="M-200 0 Q-160 -120 -110 -10 Q-60 -160 0 -10 Q60 -160 110 -10 Q160 -120 200 0Z" fill="#ffffff" stroke="#7cc4ff" stroke-width="8" stroke-linejoin="round"/>'
    return f'<g id="{p}">{crown}{drops}</g>'
