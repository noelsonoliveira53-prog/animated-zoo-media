"""Pictures for za_ep09 "Sandy's First Night Away" (Nov 20 2026). New places and props only: no character, place or older prop is drawn differently.
Registers two places: "barn" (the cozy sleepover barn at the zoo, at night) and "zoo_night" (the zoo garden under the moon and stars).
Uses kit.PT["camel"] (registered by art_za_ep07) for Mama camel.

  card(p)        the sleepover invitation: a little card with a moon, a star and a heart. Anchored at its middle.
  cushion(p)     a big, fluffy pink bed, too soft for a camel. Anchored at its bottom middle. Parts: #<p>-top (squashes).
  straw(p)       the front of a straw bed: a low golden mound that hides a lying calf's legs (put it in front of her). Anchored at its bottom middle.
  blanket(p)     a lavender blanket with stars, in CALF units: put it at Sandy's feet point with her scale, it lies over her back.
  big_star(p)    a big shining star (for counting). Anchored at its middle.
  knee_pad(p)    the thick, tough knee pad of a grown camel, in CAMEL units: put it at Mama's feet point with her scale (front near knee).
  ring(p)        a bright ring that circles a part on a picture board. Anchored at its middle.
  notes3(p)      three music notes in a little curve (the hum). Anchored at the first note.
"""
import math, random
import art, kit, art_za_ep07      # art_za_ep07 registers kit.PT["camel"]

INK = art.INK


# ------------------------------------------------------------------ places
def bg_barn(p):
    """The sleepover barn at the zoo at night: warm wood, a round window with the moon, a lantern, hay bales, straw on the floor. Cozy and light enough to see every face."""
    planks = "".join(f'<rect x="{x}" y="-900" width="8" height="1800" fill="#9c6236" opacity=".55"/>' for x in range(-460, 2420, 150))
    knots = "".join(f'<ellipse cx="{x}" cy="{y}" rx="14" ry="9" fill="#8d5530" opacity=".6"/>' for x, y in ((120, 160), (560, 520), (900, 120), (1260, 600), (1720, 260), (2000, 640), (-200, 420)))
    r = random.Random(9)
    stars = "".join(f'<circle cx="{1500 + r.uniform(-120, 120):.0f}" cy="{330 + r.uniform(-120, 120):.0f}" r="{r.choice((4, 5, 6))}" fill="#fff8d6"/>' for _ in range(14))
    window = (f'<circle cx="1500" cy="330" r="196" fill="#7a4a24"/><circle cx="1500" cy="330" r="170" fill="#2b3c8c"/>{stars}'
              f'<circle cx="1556" cy="282" r="62" fill="#fff6c9"/><circle cx="1538" cy="270" r="12" fill="#f0e3a4"/><circle cx="1574" cy="300" r="9" fill="#f0e3a4"/>'
              f'<path d="M1500 160 V500 M1330 330 H1670" stroke="#7a4a24" stroke-width="18"/><circle cx="1500" cy="330" r="170" fill="none" stroke="#5e3a1c" stroke-width="10"/>')
    lamp = (f'<g id="{p}lamp"><path d="M380 -40 V170" stroke="#5e3a1c" stroke-width="8"/><circle cx="380" cy="250" r="220" fill="#ffd97a" opacity=".16"/><circle cx="380" cy="250" r="120" fill="#ffd97a" opacity=".22"/>'
            f'<rect x="346" y="196" width="68" height="100" rx="16" fill="#ffd97a"/><rect x="338" y="182" width="84" height="20" rx="8" fill="#7a4a24"/><rect x="338" y="290" width="84" height="16" rx="8" fill="#7a4a24"/>'
            f'<path d="M352 180 Q380 140 408 180" stroke="#7a4a24" stroke-width="8" fill="none"/></g>')
    far = (f'<rect x="-500" y="-900" width="2920" height="1800" fill="#c1814d"/>{planks}{knots}'
           f'<rect x="-500" y="-60" width="2920" height="70" fill="#8d5530"/><rect x="-500" y="0" width="2920" height="16" fill="#6e4224" opacity=".5"/>'
           f'<rect x="-500" y="700" width="2920" height="40" fill="#8d5530"/>{window}{lamp}')
    bale = lambda x, y, w, h: (f'<g transform="translate({x} {y})"><rect x="{-w / 2}" y="{-h}" width="{w}" height="{h}" rx="26" fill="#e8c25a" stroke="#b88a2a" stroke-width="9"/>'
                               + "".join(f'<path d="M{-w / 2 + 30 + k * (w - 60) / 5:.0f} {-h + 22} q10 {h / 2 - 22:.0f} 0 {h - 44}" stroke="#c99f3e" stroke-width="7" fill="none"/>' for k in range(6))
                               + f'<rect x="{-w / 2}" y="{-h * .62:.0f}" width="{w}" height="14" fill="#a5672f" opacity=".7"/></g>')
    mid = bale(30, 860, 330, 190) + bale(80, 680, 250, 160) + bale(1880, 860, 330, 200)
    straws = "".join(f'<path d="M{x} {y} l{d} -10" stroke="#e8c25a" stroke-width="7" stroke-linecap="round"/>' for x, y, d in
                     ((200, 930, 40), (420, 980, -36), (640, 920, 30), (860, 1010, 44), (1100, 940, -30), (1320, 990, 36), (1540, 930, -40), (1760, 1000, 30), (300, 1040, 34), (1200, 1050, -28)))
    near = f'<rect x="-500" y="860" width="2920" height="1200" fill="#cf9a5c"/><rect x="-500" y="860" width="2920" height="14" fill="#b07a42"/>{straws}'
    return far, mid, near


def bg_zoo_night(p):
    """The zoo garden at night: a deep-blue sky full of stars, a round moon, soft hills, the zoo trees, a little lamp. Calm, never dark enough to hide a face."""
    r = random.Random(13)
    stars = "".join(f'<circle class="{p}star" cx="{r.uniform(-400, 2300):.0f}" cy="{r.uniform(-800, 520):.0f}" r="{r.choice((3, 4, 5, 6))}" fill="#fff8d6" opacity="{r.uniform(.5, 1):.2f}"/>' for _ in range(110))
    far = (art._sky(p, "#1c2a6e", "#4a5cb0") + stars
           + f'<circle cx="1540" cy="190" r="160" fill="#fff6c9" opacity=".18"/><circle cx="1540" cy="190" r="108" fill="#fff6c9"/><circle cx="1510" cy="166" r="18" fill="#f0e3a4"/><circle cx="1572" cy="222" r="13" fill="#f0e3a4"/>'
           + '<path d="M-500 700 C0 560 400 640 800 600 S1600 560 2420 680 L2420 800 L-500 800Z" fill="#2f5a78"/>')
    tree = lambda x, y, s: (f'<g transform="translate({x} {y}) scale({s})"><rect x="-14" y="-90" width="28" height="90" fill="#4a3a52"/><circle cx="0" cy="-150" r="80" fill="#2e6a62"/>'
                            f'<circle cx="-46" cy="-110" r="52" fill="#285d57"/><circle cx="48" cy="-114" r="56" fill="#336f66"/></g>')
    mid = '<path d="M-500 780 C200 700 700 760 1200 720 S2000 720 2420 760 L2420 900 L-500 900Z" fill="#336b5e"/>' + tree(150, 790, 1.2) + tree(560, 760, .9) + tree(1820, 780, 1.1)
    lamp = (f'<g transform="translate(1180 860)"><rect x="-8" y="-300" width="16" height="300" fill="#5a4a5e"/><circle cx="0" cy="-318" r="150" fill="#ffd97a" opacity=".18"/>'
            f'<circle cx="0" cy="-318" r="34" fill="#ffd97a"/><rect x="-26" y="-290" width="52" height="12" rx="6" fill="#5a4a5e"/></g>')
    near = (f'<rect x="-500" y="860" width="2920" height="1200" fill="#3f7d62"/><path d="M640 1980 L840 860 L1000 860 L1200 1980Z" fill="#8a8ab0" opacity=".55"/>{lamp}'
            + "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="{c}"/>' for x, y, c in ((300, 960, "#ffd0e0"), (480, 1010, "#fff3b0"), (1500, 970, "#ffd0e0"), (1720, 1020, "#fff3b0"), (1380, 1050, "#ffffff"))))
    return far, mid, near


art.BG.update({"barn": bg_barn, "zoo_night": bg_zoo_night})
art.PLACE.update({"barn": "the sleepover barn at night", "zoo_night": "the zoo garden at night"})


# ------------------------------------------------------------------ props
def card(p):
    return (f'<g id="{p}"><rect x="-150" y="-104" width="300" height="208" rx="24" fill="#ffffff" stroke="{art.MILO_BLUE}" stroke-width="12"/>'
            f'<rect x="-128" y="-82" width="256" height="164" rx="16" fill="#2b3c8c"/>'
            f'<circle cx="-50" cy="-10" r="46" fill="#fff6c9"/><circle cx="-30" cy="-22" r="40" fill="#2b3c8c"/>'
            f'<path d="M60 -40 l10 22 l24 2 l-18 16 l6 24 l-22 -12 l-22 12 l6 -24 l-18 -16 l24 -2Z" fill="{art.SUN}"/>'
            f'<path d="M40 52 C22 34 0 46 12 64 L40 84 L68 64 C80 46 58 34 40 52Z" fill="#ff7aa2"/></g>')


def cushion(p):
    bumps = "".join(f'<circle cx="{x}" cy="{y}" r="{rr}"/>' for x, y, rr in ((-210, -120, 70), (-110, -160, 84), (10, -172, 90), (130, -160, 84), (230, -118, 70)))
    body = f'<rect x="-290" y="-150" width="580" height="150" rx="74"/>{bumps}'
    return (f'<g id="{p}"><ellipse cx="0" cy="6" rx="300" ry="20" fill="#000" opacity=".14"/>'
            f'<g id="{p}-top"><g fill="#c2457a" stroke="#c2457a" stroke-width="18" stroke-linejoin="round">{body}</g><g fill="#ff9ec4">{body}</g>'
            f'<path d="M-200 -150 Q-100 -200 0 -196 Q100 -200 200 -150" stroke="#ffd0e3" stroke-width="22" fill="none" stroke-linecap="round"/>'
            + "".join(f'<circle cx="{x}" cy="-80" r="9" fill="#e86fa0"/>' for x in (-160, -60, 40, 140)) + '</g></g>')


def straw(p):
    """Front of the straw bed: 760 wide, about 190 tall, golden, with loose straws on top."""
    mound = "M-380 0 C-380 -120 -260 -190 -120 -186 C-40 -200 60 -204 140 -188 C280 -190 380 -120 380 0Z"
    r = random.Random(4)
    st = "".join(f'<path d="M{x:.0f} {y:.0f} l{r.uniform(-40, 40):.0f} {r.uniform(-30, -10):.0f}" stroke="{c}" stroke-width="8" stroke-linecap="round"/>'
                 for x, y, c in [(r.uniform(-340, 340), r.uniform(-190, -20), r.choice(("#f6dc84", "#c99f3e", "#e8c25a"))) for _ in range(46)])
    return (f'<g id="{p}"><path d="{mound}" fill="#b88a2a" stroke="#b88a2a" stroke-width="18" stroke-linejoin="round"/><path d="{mound}" fill="#e8c25a"/>'
            f'<path d="M-300 -130 C-180 -176 0 -186 200 -170" stroke="#f6dc84" stroke-width="20" fill="none" stroke-linecap="round" opacity=".9"/>{st}</g>')


def blanket(p):
    """Over a calf's back and sides (calf units: back at y -470, body -480..-260, x -250..250)."""
    sh = "M-270 -300 C-280 -420 -190 -500 -40 -500 C120 -506 240 -450 262 -320 L250 -230 C120 -206 -120 -206 -262 -230Z"
    st = "".join(f'<path d="M{x} {y} l7 15 l17 2 l-13 11 l4 17 l-15 -9 l-15 9 l4 -17 l-13 -11 l17 -2Z" fill="#fff3b0"/>' for x, y in ((-170, -420), (-40, -460), (100, -430), (-110, -330), (60, -320), (190, -340)))
    return (f'<g id="{p}"><path d="{sh}" fill="#6a4fb3" stroke="#6a4fb3" stroke-width="18" stroke-linejoin="round"/><path d="{sh}" fill="#a58bf0"/>'
            f'<path d="M-262 -240 C-120 -218 120 -218 250 -240" stroke="#ffffff" stroke-width="14" fill="none" stroke-linecap="round" opacity=".7"/>{st}</g>')


def big_star(p, col="#ffe066"):
    pts = " ".join(f"{(70 if k % 2 == 0 else 30) * math.sin(math.pi * k / 5):.0f},{-(70 if k % 2 == 0 else 30) * math.cos(math.pi * k / 5):.0f}" for k in range(10))
    return f'<g id="{p}"><circle r="90" fill="{col}" opacity=".22"/><polygon points="{pts}" fill="{col}" stroke="#fff8d6" stroke-width="8" stroke-linejoin="round"/></g>'


def knee_pad(p):
    """Mama camel's front near knee (art.camel: leg x 160, knee bulge at y -130)."""
    return (f'<g id="{p}"><ellipse cx="166" cy="-130" rx="31" ry="25" fill="#8f5a2b" stroke="#5e3a1c" stroke-width="6"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#6e4526"/>' for x, y in ((154, -138), (170, -124), (180, -140), (160, -118), (174, -146))) + '</g>')


def ring(p, r=84, col="#ffe066"):
    return (f'<g id="{p}"><circle r="{r}" fill="none" stroke="{INK}" stroke-width="22"/><circle r="{r}" fill="none" stroke="{col}" stroke-width="12"/></g>')


def notes3(p):
    return (f'<g id="{p}"><g id="{p}-a">{art.note(p + "a", "#ffd97a")}</g>'
            f'<g id="{p}-b" transform="translate(110 -60)">{art.note(p + "b", "#ff9ab8")}</g>'
            f'<g id="{p}-c" transform="translate(220 -10)">{art.note(p + "c", "#bfe3ff")}</g></g>')
