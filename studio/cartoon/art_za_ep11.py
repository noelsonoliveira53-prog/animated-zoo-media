"""Pictures for za_ep11 "How Can Milo Get Warm in the Snow?" (theme title "Too Cold for Milo!", Nov 21 2026). New place and props only: no character,
place or older prop is drawn differently. The Arctic places of za_ep10 (art_za_ep10) are reused as they are.

Place:
  "arctic_low"  the Arctic ice on a pale day: the same ice and water as art2's "arctic", the sun low on the horizon at the right, pale and soft.
Props (each anchored as written):
  leaf_wrap(p)   a big thin green leaf wrapped round Milo from his scarf down, like a blanket; anchored at Milo's feet (Milo units: draw at Milo's scale).
  shiver(p)      little zig-zag "shiver" lines on both sides of a small bird; anchored at Milo's body point (Milo units).
  warm_layers(p) a picture-board cut through a polar bear's coat: the fat at the bottom, the black skin, the soft thick underfur, the long
                 clear guard hairs on top; parts -fat, -skin, -under, -guard. Anchored at its middle (about 700 x 520).
  snow_nest(p)   the front of a round snow nest: six rounded snow blocks in a low ring, -b0 .. -b5 (left to right); anchored at the middle of
                 its bottom edge (about 520 wide, 150 high at scale 1).
  cloud(p)       a soft cloud (art._cloud), anchored at its middle.
  breath(p)      two small puffs of a cold breath; anchored at the left end.
  paw_print(p)   a polar bear paw print in the snow (pad and five toes), anchored at its middle.
  bird_print(p)  a tiny three-toed bird print in the snow, anchored at its middle.
"""
import math, random
import art, art2

INK = art.INK


def bg_arctic_low(p):
    far, mid, near = art2.bg_arctic(p)
    sky = art._sky(p, "#a9d4f0", "#ffe9c2")
    far = far.replace(art._sky(p, "#bfe6ff", "#f2fbff"), sky + art._sun(p + "lowsun", 1700, 560, 92, "#ffd27a"))
    far = far.replace(art._sun(p + "sun", 400, 240, 70, "#fff7c9"), "")
    return far, mid, near


art.BG["arctic_low"] = bg_arctic_low
art.PLACE["arctic_low"] = "the Arctic ice with the sun low on the horizon"


# ------------------------------------------------------------------ props
def leaf_wrap(p):
    """A big green leaf wrapped round Milo's body, its tip flapping in the wind (-tip). Thin: you can see a little through it."""
    body = "M-158 -80 C-164 -116 -100 -128 0 -124 C100 -128 164 -116 158 -80 C154 -30 100 -6 0 -4 C-100 -6 -154 -30 -158 -80Z"
    veins = "".join(f'<path d="M0 {y} q{d * 60} -24 {d * 120} -20" stroke="#3f8a3a" stroke-width="6" fill="none" stroke-linecap="round"/>'
                    for y in (-96, -60, -28) for d in (-1, 1))
    tip = (f'<g id="{p}-tip"><path d="M130 -100 C210 -150 290 -130 310 -80 C260 -70 200 -60 140 -40Z" fill="#7ccf6a" stroke="#3f8a3a" stroke-width="8" stroke-linejoin="round" opacity=".88"/>'
           f'<path d="M146 -66 Q220 -100 296 -84" stroke="#3f8a3a" stroke-width="6" fill="none" stroke-linecap="round"/></g>')
    return (f'<g id="{p}" opacity=".9"><path d="{body}" fill="#8ad978" stroke="#3f8a3a" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M0 -122 L0 -8" stroke="#3f8a3a" stroke-width="8" stroke-linecap="round"/>{veins}{tip}</g>')


def shiver(p):
    """Three little zig-zag lines at each side of Milo's body: he is shivering."""
    z = lambda x, y, d: f'<path d="M{x} {y} l{d * 22} 14 l{-d * 22} 14 l{d * 22} 14 l{-d * 22} 14" stroke="#4a90d9" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    left = "".join(z(-200 - k * 34, -120 + k * 30, 1) for k in range(3))
    right = "".join(z(200 + k * 34, -120 + k * 30, -1) for k in range(3))
    return f'<g id="{p}"><g id="{p}-l">{left}</g><g id="{p}-r">{right}</g></g>'


def warm_layers(p):
    """A cut through a polar bear's coat, like a slice of cake: long clear hairs on top, soft thick fur under them, black skin, thick fat."""
    W, H = 700, 520
    x0, y0 = -W // 2, -H // 2
    r = random.Random(11)
    fat_y, skin_y, under_y = 120, 92, -10          # top of the fat, top of the skin, top of the underfur
    frame = f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" rx="36" fill="#eaf6ff" stroke="{INK}" stroke-width="14"/>'
    fat = (f'<g id="{p}-fat"><rect x="{x0 + 20}" y="{fat_y}" width="{W - 40}" height="{H // 2 - fat_y - 20}" rx="20" fill="#ffd779" stroke="#d8a53a" stroke-width="8"/>'
           + "".join(f'<circle cx="{r.uniform(x0 + 60, -x0 - 60):.0f}" cy="{r.uniform(fat_y + 30, H // 2 - 50):.0f}" r="{r.uniform(10, 18):.0f}" fill="#ffe7a8"/>' for _ in range(14)) + '</g>')
    skin = f'<g id="{p}-skin"><rect x="{x0 + 20}" y="{skin_y}" width="{W - 40}" height="{fat_y - skin_y}" fill="#2f3640"/></g>'
    under = "".join(f'<path d="M{x} {skin_y} q{r.uniform(-14, 14):.0f} -50 {r.uniform(-8, 8):.0f} {under_y - skin_y + r.uniform(-8, 8):.0f}" stroke="#f6eedb" stroke-width="16" fill="none" stroke-linecap="round"/>'
                    for x in range(x0 + 34, -x0 - 30, 18))
    under = f'<g id="{p}-under"><rect x="{x0 + 20}" y="{under_y}" width="{W - 40}" height="{skin_y - under_y}" fill="#efe4c8"/>{under}</g>'
    guard = "".join(f'<path d="M{x} {skin_y - 10} q{r.uniform(10, 30):.0f} -120 {r.uniform(40, 70):.0f} -{r.uniform(220, 250):.0f}" stroke="#9cc8ea" stroke-width="14" fill="none" stroke-linecap="round"/>'
                    f'<path d="M{x} {skin_y - 10} q{r.uniform(10, 30):.0f} -120 {r.uniform(40, 70):.0f} -{r.uniform(220, 250):.0f}" stroke="#ffffff" stroke-width="6" fill="none" stroke-linecap="round"/>'
                    for x in range(x0 + 50, -x0 - 70, 46))
    guard = f'<g id="{p}-guard">{guard}</g>'
    return f'<g id="{p}">{frame}<g>{fat}{skin}{under}{guard}</g></g>'


def snow_nest(p):
    """The front of a round snow nest: six rounded snow blocks in a low ring, the middle ones lower (we look into the nest)."""
    blocks = ((-230, -70, 96, 76), (-140, -44, 100, 70), (-46, -30, 100, 64), (52, -30, 100, 64), (146, -44, 100, 70), (236, -70, 96, 76))
    out = ""
    for k, (x, y, w, h) in enumerate(blocks):
        out += (f'<g id="{p}-b{k}"><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h + 40}" rx="30" fill="#dcecfb"/>'
                f'<rect x="{x - w / 2:.0f}" y="{y - h / 2 - 6:.0f}" width="{w}" height="{h + 34}" rx="30" fill="#ffffff" stroke="#b9d6ef" stroke-width="7"/>'
                f'<path d="M{x - w / 2 + 20:.0f} {y - h / 2 + 10:.0f} q{w / 2 - 20:.0f} -12 {w - 40:.0f} 0" stroke="#e8f3fd" stroke-width="8" fill="none" stroke-linecap="round"/></g>')
    return f'<g id="{p}"><g transform="translate(0 -40)">{out}</g></g>'


def cloud(p):
    return art._cloud(p, 0, 0, 1.0, "#ffffff", .97)


def breath(p):
    return (f'<g id="{p}" opacity=".85"><circle cx="20" cy="0" r="16" fill="#ffffff" stroke="#c9def0" stroke-width="5"/>'
            f'<circle cx="54" cy="-12" r="22" fill="#ffffff" stroke="#c9def0" stroke-width="5"/><circle cx="96" cy="-24" r="26" fill="#ffffff" stroke="#c9def0" stroke-width="5"/></g>')


def paw_print(p):
    toes = "".join(f'<ellipse cx="{x}" cy="{y}" rx="18" ry="22" fill="#9fb8d2"/>' for x, y in ((-62, -50), (-32, -72), (0, -78), (32, -72), (62, -50)))
    return f'<g id="{p}"><ellipse cx="0" cy="0" rx="78" ry="54" fill="#9fb8d2"/>{toes}</g>'


def bird_print(p):
    return (f'<g id="{p}" stroke="#7f9fbf" stroke-width="9" stroke-linecap="round" fill="none">'
            f'<path d="M0 20 L0 -24 M0 20 L-24 -16 M0 20 L24 -16 M0 20 L0 40"/></g>')
