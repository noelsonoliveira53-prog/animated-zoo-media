"""Original art for Bloop's Color Lab: friendly color blobs, shape friends and counting scenes in a candy-colored lab.
Shared 1080x1100 frame, floor at ~y1000."""
import math

def svg(body):
    return f'<svg viewBox="0 0 1080 1100" width="1080" height="1100">{body}</svg>'

RAINBOW = ["#ff5c5c", "#ffa94d", "#ffd43b", "#69db7c", "#4dabf7", "#9775fa"]

def lab_env():
    shelves = ""
    for k, (x0, x1) in enumerate(((-480, -40), (1120, 1560))):
        for row, y in enumerate((300, 520, 740)):
            shelves += f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="16" rx="8" fill="#e0d4ff"/>'
            for j in range(5):
                c = RAINBOW[(j + row + k) % 6]; cx = x0 + 50 + j * ((x1 - x0 - 80) // 5)
                shelves += (f'<rect x="{cx}" y="{y-90}" width="56" height="90" rx="14" fill="{c}" opacity=".85"/>'
                            f'<rect x="{cx+8}" y="{y-104}" width="40" height="18" rx="6" fill="#fff"/>')
    tiles = "".join(f'<rect x="{x}" y="1000" width="118" height="100" fill="{"#f3edff" if (x//120)%2 else "#ffffff"}"/>' for x in range(-480, 1600, 120))
    return (f'<rect x="-500" y="-10" width="2200" height="1010" fill="#fff6fb" opacity=".0"/>{shelves}'
            f'<g opacity=".9">' + "".join(f'<path d="M{-300+i*30} 120 q600 -110 1680 0" stroke="{c}" stroke-width="22" fill="none" opacity=".25"/>' for i, c in enumerate(RAINBOW)) + '</g>'
            f'{tiles}<rect x="-500" y="994" width="2200" height="10" fill="#d9ccff"/>')

def face(cx, cy, s=1.0, mouth="#3d2a7a"):
    ex = int(48 * s)
    return (f'<circle cx="{cx-ex}" cy="{cy}" r="{int(30*s)}" fill="#fff"/><circle cx="{cx+ex}" cy="{cy}" r="{int(30*s)}" fill="#fff"/>'
            f'<circle cx="{cx-ex+4}" cy="{cy+4}" r="{int(16*s)}" fill="#1a1a2e"/><circle cx="{cx+ex+4}" cy="{cy+4}" r="{int(16*s)}" fill="#1a1a2e"/>'
            f'<circle cx="{cx-ex+10}" cy="{cy-3}" r="6" fill="#fff"/><circle cx="{cx+ex+10}" cy="{cy-3}" r="6" fill="#fff"/>'
            f'<path d="M{cx-30*s:.0f} {cy+48*s:.0f} q{30*s:.0f} {26*s:.0f} {60*s:.0f} 0" stroke="{mouth}" stroke-width="{max(6,int(8*s))}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{cx-ex-24*s:.0f}" cy="{cy+42*s:.0f}" rx="{20*s:.0f}" ry="{11*s:.0f}" fill="#ff8fab" opacity=".6"/>'
            f'<ellipse cx="{cx+ex+24*s:.0f}" cy="{cy+42*s:.0f}" rx="{20*s:.0f}" ry="{11*s:.0f}" fill="#ff8fab" opacity=".6"/>')

# ---- color friends: a jelly blob of the color + three things of that color (fx) ----
def heart_path(cx, cy, s):
    return f'M{cx} {cy+60*s:.0f} C{cx-110*s:.0f} {cy-10*s:.0f} {cx-50*s:.0f} {cy-90*s:.0f} {cx} {cy-35*s:.0f} C{cx+50*s:.0f} {cy-90*s:.0f} {cx+110*s:.0f} {cy-10*s:.0f} {cx} {cy+60*s:.0f}Z'

def blob(color, dark, things, mouth="#3d2a7a"):
    body = (f'<path d="M260 990 Q200 700 330 560 Q440 430 560 450 Q720 470 790 600 Q880 760 820 990Z" fill="{color}" stroke="{dark}" stroke-width="10"/>'
            f'<ellipse cx="430" cy="600" rx="60" ry="34" fill="#fff" opacity=".45" transform="rotate(-30 430 600)"/>'
            + face(545, 690, 1.25, mouth))
    return svg(lab_env() + f'<g id="animal">{body}</g><g id="fx" opacity="0">{things}</g>')

def apple(cx, cy, c="#ff5c5c"):
    return f'<circle cx="{cx-28}" cy="{cy}" r="52" fill="{c}"/><circle cx="{cx+28}" cy="{cy}" r="52" fill="{c}"/><rect x="{cx-4}" y="{cy-80}" width="8" height="34" fill="#795548"/><ellipse cx="{cx+22}" cy="{cy-70}" rx="22" ry="11" fill="#69db7c"/>'

def ball(cx, cy, c, r=55):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/><path d="M{cx-r} {cy} q{r} {-r*.6:.0f} {2*r} 0" stroke="#fff" stroke-width="8" fill="none" opacity=".7"/>'

def star_path(cx, cy, r, ri, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        a = math.radians(rot + i * 180 / n); rr = r if i % 2 == 0 else ri
        pts.append(f"{cx + rr*math.cos(a):.0f},{cy + rr*math.sin(a):.0f}")
    return "M" + " L".join(pts) + "Z"

THINGS = {
    "red": apple(900, 360) + ball(150, 380, "#ff5c5c") + f'<path d="{heart_path(940, 640, .9)}" fill="#ff5c5c"/>',
    "blue": ball(900, 380, "#4dabf7") + '<path d="M150 300 Q100 380 150 420 Q200 380 150 300Z" fill="#4dabf7" transform="scale(1.6) translate(-56 -150)"/>' + '<rect x="860" y="560" width="120" height="90" rx="16" fill="#4dabf7"/><circle cx="890" cy="660" r="16" fill="#1c7ed6"/><circle cx="950" cy="660" r="16" fill="#1c7ed6"/>',
    "yellow": '<circle cx="920" cy="360" r="70" fill="#ffd43b"/>' + "".join(f'<line x1="{920+85*math.cos(a):.0f}" y1="{360+85*math.sin(a):.0f}" x2="{920+115*math.cos(a):.0f}" y2="{360+115*math.sin(a):.0f}" stroke="#ffd43b" stroke-width="12" stroke-linecap="round"/>' for a in [i*0.785 for i in range(8)])
              + '<path d="M90 420 Q160 300 240 360 Q190 400 150 460Z" fill="#ffd43b"/>' + '<ellipse cx="920" cy="640" rx="80" ry="55" fill="#ffd43b"/><circle cx="975" cy="590" r="38" fill="#ffd43b"/><path d="M1005 595 l30 6 -30 10z" fill="#ffa94d"/>',
    "green": '<path d="M860 420 Q920 280 1010 300 Q990 420 860 420Z" fill="#69db7c"/><path d="M860 420 L1000 305" stroke="#2b8a3e" stroke-width="6"/>' + '<ellipse cx="160" cy="400" rx="80" ry="60" fill="#69db7c"/><circle cx="125" cy="345" r="26" fill="#69db7c"/><circle cx="195" cy="345" r="26" fill="#69db7c"/><circle cx="125" cy="345" r="10" fill="#1a1a2e"/><circle cx="195" cy="345" r="10" fill="#1a1a2e"/>' + '<path d="M900 700 L940 560 L980 700Z" fill="#69db7c"/><rect x="930" y="700" width="20" height="30" fill="#795548"/>',
    "orange": ball(910, 380, "#ffa94d") + '<path d="M120 300 L200 300 L160 460Z" fill="#ffa94d"/><path d="M130 300 q30 -40 60 0" fill="#69db7c"/>' + '<rect x="880" y="580" width="110" height="80" rx="14" fill="#ffa94d"/><path d="M880 600 h110" stroke="#fff" stroke-width="8"/>',
    "purple": "".join(f'<circle cx="{900+dx}" cy="{340+dy}" r="30" fill="#9775fa"/>' for dx, dy in ((0,0),(-40,40),(40,40),(-20,80),(20,80),(0,120))) + '<path d="M120 460 Q160 330 200 460Z" fill="#9775fa"/><circle cx="160" cy="380" r="34" fill="#9775fa"/>' + ball(930, 640, "#9775fa"),
    "pink": '<circle cx="920" cy="370" r="36" fill="#ffd43b"/>' + "".join(f'<circle cx="{920+60*math.cos(a):.0f}" cy="{370+60*math.sin(a):.0f}" r="36" fill="#f783ac"/>' for a in [i*1.2566 for i in range(5)]) + '<path d="M90 430 Q160 300 230 430Z" fill="#f783ac"/><circle cx="160" cy="330" r="20" fill="#fff"/>' + ball(930, 650, "#f783ac"),
    "brown": '<rect x="860" y="300" width="140" height="120" rx="18" fill="#a9744f"/><rect x="900" y="340" width="60" height="80" rx="6" fill="#7b4f32"/>' + '<circle cx="150" cy="380" r="70" fill="#a9744f"/><circle cx="100" cy="320" r="26" fill="#a9744f"/><circle cx="200" cy="320" r="26" fill="#a9744f"/>' + '<rect x="900" y="580" width="40" height="120" fill="#a9744f"/><circle cx="920" cy="560" r="60" fill="#69db7c"/>',
    "gray": '<ellipse cx="920" cy="380" rx="110" ry="60" fill="#adb5bd"/><ellipse cx="860" cy="350" rx="60" ry="50" fill="#adb5bd"/>' + '<ellipse cx="160" cy="400" rx="90" ry="60" fill="#adb5bd"/><circle cx="230" cy="350" r="30" fill="#adb5bd"/><circle cx="240" cy="345" r="8" fill="#1a1a2e"/>' + '<ellipse cx="930" cy="640" rx="90" ry="50" fill="#868e96"/>',
    "black": '<circle cx="920" cy="380" r="80" fill="#343a40"/><circle cx="920" cy="380" r="38" fill="#868e96"/>' + '<path d="M80 440 Q160 300 240 440Z" fill="#343a40"/><path d="M160 300 L160 470" stroke="#343a40" stroke-width="8"/>' + '<rect x="860" y="580" width="150" height="90" rx="10" fill="#fff" stroke="#343a40" stroke-width="5"/>' + "".join(f'<rect x="{878+i*32}" y="580" width="18" height="55" fill="#343a40"/>' for i in range(4)),
}
COLORS = {"red": ("#ff5c5c", "#e03131"), "blue": ("#4dabf7", "#1c7ed6"), "yellow": ("#ffd43b", "#f59f00"), "green": ("#69db7c", "#2f9e44"),
          "orange": ("#ffa94d", "#e8590c"), "purple": ("#9775fa", "#6741d9"), "pink": ("#f783ac", "#d6336c"), "brown": ("#a9744f", "#7b4f32"),
          "gray": ("#adb5bd", "#868e96"), "black": ("#343a40", "#212529")}
SCENES7 = {k: blob(c, d, THINGS[k], "#fff" if k == "black" else "#3d2a7a") for k, (c, d) in COLORS.items()}

# ---- shape friends: the shape with a face; fx traces the sides/corners; fx2 shows a real-life example ----
def shape_scene(path, color, dark, fx, fx2, fcx=540, fcy=640, s=1.2):
    body = f'<path d="{path}" fill="{color}" stroke="{dark}" stroke-width="12" stroke-linejoin="round"/>' + face(fcx, fcy, s)
    return svg(lab_env() + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')

def dots(pts, c="#ffd43b"):
    return "".join(f'<circle cx="{x}" cy="{y}" r="26" fill="{c}" stroke="#fff" stroke-width="6"/>' for x, y in pts)

def outline(path):
    return f'<path d="{path}" fill="none" stroke="#ffd43b" stroke-width="16" stroke-dasharray="34 18" stroke-linejoin="round"/>'

CIRCLE_P = "M540 360 A300 300 0 1 1 539.9 360Z"
SQUARE_P = "M270 420 L810 420 L810 960 L270 960Z"
TRI_P = "M540 330 L860 960 L220 960Z"
STAR_P = star_path(540, 650, 350, 150)
HEART_P = heart_path(540, 600, 3.6)
RECT_P = "M160 520 L920 520 L920 960 L160 960Z"
OVAL_P = "M540 320 A230 320 0 1 1 539.9 320Z"
DIAMOND_P = "M540 320 L840 650 L540 980 L240 650Z"
MOON_P = "M620 340 A320 320 0 1 0 620 960 A260 260 0 1 1 620 340Z"
HEX_P = "M" + " L".join(f"{540+330*math.cos(math.radians(a)):.0f},{650+330*math.sin(math.radians(a)):.0f}" for a in range(0, 360, 60)) + "Z"

SHAPES = {
    "circle": shape_scene(CIRCLE_P, "#4dabf7", "#1c7ed6", outline(CIRCLE_P), ball(950, 350, "#ff5c5c", 70) + '<circle cx="130" cy="380" r="80" fill="#fff" stroke="#495057" stroke-width="10"/><path d="M130 380 L130 320 M130 380 L170 400" stroke="#495057" stroke-width="10" stroke-linecap="round"/>'),
    "square": shape_scene(SQUARE_P, "#ff5c5c", "#e03131", dots([(270, 420), (810, 420), (810, 960), (270, 960)]), '<rect x="860" y="280" width="160" height="160" rx="10" fill="#ffd43b"/><text x="940" y="385" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="90" fill="#fff">A</text>'),
    "triangle": shape_scene(TRI_P, "#ffd43b", "#f59f00", dots([(540, 330), (860, 960), (220, 960)]), '<path d="M880 440 L1020 440 L950 300Z" fill="#ffa94d"/><circle cx="910" cy="420" r="10" fill="#e03131"/><circle cx="960" cy="400" r="10" fill="#e03131"/>', fcy=760, s=1.0),
    "star": shape_scene(STAR_P, "#ffd43b", "#f59f00", dots([(540 + round(350*math.cos(math.radians(-90 + i*72))), 650 + round(350*math.sin(math.radians(-90 + i*72)))) for i in range(5)], "#ff5c5c"), "".join(f'<path d="{star_path(x, y, 40, 17)}" fill="#fff59d"/>' for x, y in ((130, 300), (950, 280), (1000, 450), (100, 480))), fcy=670, s=1.0),
    "heart": shape_scene(HEART_P, "#f783ac", "#d6336c", outline(HEART_P), "".join(f'<path d="{heart_path(x, y, .5)}" fill="#ff5c5c"/>' for x, y in ((130, 330), (960, 320), (990, 520))), fcy=620, s=1.1),
    "rectangle": shape_scene(RECT_P, "#69db7c", "#2f9e44", '<path d="M160 520 L920 520" stroke="#ffd43b" stroke-width="18"/><path d="M160 960 L920 960" stroke="#ffd43b" stroke-width="18"/><path d="M160 520 L160 960" stroke="#ff5c5c" stroke-width="18"/><path d="M920 520 L920 960" stroke="#ff5c5c" stroke-width="18"/>', '<rect x="880" y="220" width="130" height="200" rx="10" fill="#a9744f"/><circle cx="985" cy="330" r="10" fill="#ffd43b"/>', fcy=720),
    "oval": shape_scene(OVAL_P, "#9775fa", "#6741d9", outline(OVAL_P), '<ellipse cx="950" cy="360" rx="60" ry="80" fill="#fff" stroke="#dee2e6" stroke-width="6"/>'),
    "diamond": shape_scene(DIAMOND_P, "#4dabf7", "#1c7ed6", dots([(540, 320), (840, 650), (540, 980), (240, 650)]), '<path d="M950 260 L1030 360 L950 460 L870 360Z" fill="#ff5c5c"/><path d="M950 460 Q920 520 960 560" stroke="#495057" stroke-width="5" fill="none"/>'),
    "crescent": shape_scene(MOON_P, "#ffd43b", "#f59f00", outline(MOON_P), "".join(f'<path d="{star_path(x, y, 34, 14)}" fill="#fff59d"/>' for x, y in ((850, 300), (960, 420), (900, 560))), fcx=330, fcy=650, s=.7),
    "hexagon": shape_scene(HEX_P, "#ffa94d", "#e8590c", dots([(round(540+330*math.cos(math.radians(a))), round(650+330*math.sin(math.radians(a)))) for a in range(0, 360, 60)]), "".join(f'<path d="M{x+40} {y} L{x+20} {y+35} L{x-20} {y+35} L{x-40} {y} L{x-20} {y-35} L{x+20} {y-35}Z" fill="#ffd43b" stroke="#f59f00" stroke-width="4"/>' for x, y in ((920, 320), (1000, 360), (920, 390), (1000, 430)))),
}

# ---- counting 1..5: big number + that many smiling fruit ----
FRUIT = {1: "#ff5c5c", 2: "#ffd43b", 3: "#69db7c", 4: "#4dabf7", 5: "#9775fa"}
def mini(cx, cy, c):
    return (f'<circle cx="{cx}" cy="{cy}" r="58" fill="{c}" stroke="#3d2a7a" stroke-width="5"/>'
            f'<circle class="pupil" cx="{cx-18}" cy="{cy-6}" r="8" fill="#1a1a2e"/><circle class="pupil" cx="{cx+18}" cy="{cy-6}" r="8" fill="#1a1a2e"/>'
            f'<path d="M{cx-16} {cy+16} q16 12 32 0" stroke="#3d2a7a" stroke-width="5" fill="none" stroke-linecap="round"/>')
def number_scene(n):
    xs = {1: [540], 2: [420, 660], 3: [330, 540, 750], 4: [240, 420, 600, 780], 5: [180, 360, 540, 720, 900]}[n]
    items = "".join(mini(x, 920, FRUIT[n]) for x in xs)
    marks = "".join(f'<text x="{x}" y="830" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="70" fill="#3d2a7a">{i+1}</text>' for i, x in enumerate(xs))
    body = (f'<text x="540" y="720" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="560" fill="{FRUIT[n]}" stroke="#3d2a7a" stroke-width="14" paint-order="stroke">{n}</text>' + items)
    return svg(lab_env() + f'<g id="animal">{body}</g><g id="fx" opacity="0">{marks}</g>')
NUMBERS = {f"n{n}": number_scene(n) for n in range(1, 6)}

BLOOP_TITLE = svg(lab_env() + """
  <g transform="translate(-130 -40)">
    <rect x="150" y="230" width="780" height="150" rx="44" fill="#9d6bff" stroke="#6741d9" stroke-width="10"/>
    <text x="540" y="333" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="84" fill="#fff">BLOOP'S COLOR LAB</text>
    """ + "".join(f'<rect x="{300+i*85}" y="760" width="64" height="200" rx="18" fill="{c}"/><rect x="{310+i*85}" y="740" width="44" height="26" rx="8" fill="#fff"/>' for i, c in enumerate(RAINBOW)) + """
  </g>""")

SCENES7.update(SHAPES); SCENES7.update(NUMBERS)
NAMES7 = {f"n{n}": w for n, w in zip(range(1, 6), ["ONE", "TWO", "THREE", "FOUR", "FIVE"])}
NAMES7.update({k: k.upper() for k in list(COLORS) + list(SHAPES)})

BLOOP = """<svg id="milo" viewBox="0 0 220 200" width="260" height="236">
  <g id="wing"><circle cx="150" cy="22" r="10" fill="#c7b3ff"/><circle cx="168" cy="10" r="6" fill="#c7b3ff"/></g>
  <path d="M30 190 Q18 120 60 70 Q100 30 150 46 Q200 66 196 130 Q194 170 186 190Z" fill="#9d6bff" stroke="#6741d9" stroke-width="5"/>
  <ellipse cx="80" cy="80" rx="18" ry="10" fill="#fff" opacity=".5" transform="rotate(-35 80 80)"/>
  <rect x="62" y="52" width="100" height="14" rx="7" fill="#3d2a7a"/>
  <circle cx="88" cy="58" r="16" fill="#bde9ff" stroke="#3d2a7a" stroke-width="5"/><circle cx="136" cy="58" r="16" fill="#bde9ff" stroke="#3d2a7a" stroke-width="5"/>
  <circle cx="90" cy="96" r="16" fill="#fff"/><circle cx="134" cy="96" r="16" fill="#fff"/>
  <ellipse class="mpupil" cx="92" cy="98" rx="8" ry="10" fill="#1a1a2e"/><ellipse class="mpupil" cx="136" cy="98" rx="8" ry="10" fill="#1a1a2e"/>
  <circle class="glint" cx="95" cy="93" r="3.5" fill="#fff"/><circle class="glint" cx="139" cy="93" r="3.5" fill="#fff"/>
  <path d="M98 112 q14 10 28 0" stroke="#3d2a7a" stroke-width="5" fill="none" stroke-linecap="round"/>
  <ellipse id="beaklow" cx="112" cy="117" rx="8" ry="2.2" fill="#3d2a7a"/>
  <circle cx="68" cy="116" r="8" fill="#ff9ab0" opacity=".7"/><circle cx="158" cy="116" r="8" fill="#ff9ab0" opacity=".7"/>
</svg>"""
