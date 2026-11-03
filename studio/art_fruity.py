"""Original art for Fruity Friends: smiling fruit and veggie friends plus healthy-habit scenes in a sunny kitchen.
Shared 1080x1100 frame, counter/floor at ~y1000."""
import math

def svg(body):
    return f'<svg viewBox="0 0 1080 1100" width="1080" height="1100">{body}</svg>'

def kitchen_env():
    tiles = "".join(f'<rect x="{x}" y="{y}" width="56" height="56" rx="6" fill="#fff" opacity=".35"/>' for x in range(-480, 1600, 64) for y in range(560, 980, 64) if (x // 64 + y // 64) % 2 == 0)
    return (f'{tiles}'
            '<g><rect x="-440" y="160" width="300" height="240" rx="20" fill="#bde9ff" stroke="#fff" stroke-width="16"/><path d="M-290 160 V400 M-440 280 H-140" stroke="#fff" stroke-width="12"/></g>'
            '<g><rect x="1220" y="160" width="300" height="240" rx="20" fill="#bde9ff" stroke="#fff" stroke-width="16"/><path d="M1370 160 V400 M1220 280 H1520" stroke="#fff" stroke-width="12"/></g>'
            '<g fill="#3aa856" opacity=".85"><ellipse cx="-330" cy="520" rx="60" ry="26"/><ellipse cx="1380" cy="520" rx="60" ry="26"/></g>'
            '<rect x="-500" y="975" width="2200" height="30" fill="#e8b07a"/><rect x="-500" y="1000" width="2200" height="110" fill="#f6c992"/>'
            + "".join(f'<rect x="{x}" y="1010" width="4" height="100" fill="#e8b07a"/>' for x in range(-480, 1600, 180)))

def face(cx, cy, s=1.0, mouth="#7a2b2b"):
    ex = int(46 * s)
    return (f'<circle cx="{cx-ex}" cy="{cy}" r="{int(28*s)}" fill="#fff"/><circle cx="{cx+ex}" cy="{cy}" r="{int(28*s)}" fill="#fff"/>'
            f'<circle cx="{cx-ex+4}" cy="{cy+4}" r="{int(15*s)}" fill="#1a1a2e"/><circle cx="{cx+ex+4}" cy="{cy+4}" r="{int(15*s)}" fill="#1a1a2e"/>'
            f'<circle cx="{cx-ex+10}" cy="{cy-3}" r="{max(4,int(6*s))}" fill="#fff"/><circle cx="{cx+ex+10}" cy="{cy-3}" r="{max(4,int(6*s))}" fill="#fff"/>'
            f'<path d="M{cx-30*s:.0f} {cy+46*s:.0f} q{30*s:.0f} {26*s:.0f} {60*s:.0f} 0" stroke="{mouth}" stroke-width="{max(5,int(8*s))}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{cx-ex-24*s:.0f}" cy="{cy+40*s:.0f}" rx="{20*s:.0f}" ry="{11*s:.0f}" fill="#ff8fab" opacity=".6"/>'
            f'<ellipse cx="{cx+ex+24*s:.0f}" cy="{cy+40*s:.0f}" rx="{20*s:.0f}" ry="{11*s:.0f}" fill="#ff8fab" opacity=".6"/>')

def scene(body, fx="", fx2=""):
    return svg(kitchen_env() + f'<g id="animal">{body}</g><g id="fx" opacity="0">{fx}</g><g id="fx2" opacity="0">{fx2}</g>')

def sparkles(pts, c="#fff59d"):
    return "".join(f'<path d="M{x} {y-34} L{x+9} {y-9} L{x+34} {y} L{x+9} {y+9} L{x} {y+34} L{x-9} {y+9} L{x-34} {y} L{x-9} {y-9}Z" fill="{c}"/>' for x, y in pts)

def bubbles(pts):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e3f2fd" stroke="#90caf9" stroke-width="5" opacity=".9"/><circle cx="{x-r//3}" cy="{y-r//3}" r="{max(4,r//5)}" fill="#fff"/>' for x, y, r in pts)

def leaf(cx, cy, rot, c="#3aa856", s=1.0):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{int(60*s)}" ry="{int(24*s)}" fill="{c}" transform="rotate({rot} {cx} {cy})"/>'

# ---------- fruits & veggies ----------
APPLE = scene('<path d="M540 470 C380 380 230 520 280 720 C320 900 450 990 540 930 C630 990 760 900 800 720 C850 520 700 380 540 470Z" fill="#ef4444" stroke="#b91c1c" stroke-width="10"/>'
              '<rect x="530" y="370" width="20" height="110" rx="8" fill="#795548"/>' + leaf(620, 400, -25) + '<ellipse cx="400" cy="560" rx="50" ry="26" fill="#fff" opacity=".4" transform="rotate(-35 400 560)"/>' + face(540, 680, 1.25),
              '<g transform="translate(860 300)"><circle r="110" fill="#fff7d6" stroke="#ef4444" stroke-width="16"/>' + "".join(f'<ellipse cx="{60*math.cos(math.radians(a)):.0f}" cy="{60*math.sin(math.radians(a)):.0f}" rx="12" ry="24" fill="#5d4037" transform="rotate({a+90} {60*math.cos(math.radians(a)):.0f} {60*math.sin(math.radians(a)):.0f})"/>' for a in range(-90, 270, 72)) + '</g>')
BANANA = scene('<path d="M260 520 Q300 920 760 900 Q900 890 880 840 Q500 880 400 520Z" fill="#ffd43b" stroke="#e8a400" stroke-width="10"/>'
               '<path d="M250 520 l-10 -60 40 0 z" fill="#8d6e63"/>' + face(620, 780, 1.0),
               "".join(f'<g transform="translate({x} {y}) rotate({r}) scale(.35)"><path d="M260 520 Q300 920 760 900 Q900 890 880 840 Q500 880 400 520Z" fill="#ffd43b" stroke="#e8a400" stroke-width="16"/></g>' for x, y, r in ((780, 160, 10), (830, 190, 0), (880, 220, -10), (930, 250, -20))))
ORANGE = scene('<circle cx="540" cy="690" r="290" fill="#fb923c" stroke="#ea580c" stroke-width="10"/>' + "".join(f'<circle cx="{540+220*math.cos(a):.0f}" cy="{690+220*math.sin(a):.0f}" r="6" fill="#ea580c" opacity=".5"/>' for a in [i*0.45 for i in range(14)])
               + '<rect x="530" y="380" width="20" height="40" fill="#795548"/>' + leaf(600, 390, -20) + face(540, 680, 1.25),
               '<g transform="translate(880 330)"><circle r="110" fill="#fdba74" stroke="#ea580c" stroke-width="14"/>' + "".join(f'<path d="M0 0 L{95*math.cos(math.radians(a)):.0f} {95*math.sin(math.radians(a)):.0f}" stroke="#fff7ed" stroke-width="8"/>' for a in range(0, 360, 45)) + '</g>')
WATERMELON = scene('<path d="M180 620 A360 360 0 0 0 900 620Z" fill="#22c55e" stroke="#15803d" stroke-width="10"/><path d="M220 620 A320 320 0 0 0 860 620Z" fill="#fef3c7"/><path d="M250 620 A290 290 0 0 0 830 620Z" fill="#fb7185"/>'
                   + "".join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="16" fill="#1a1a2e"/>' for x, y in ((350, 700), (460, 760), (620, 760), (730, 700), (540, 820), (400, 800), (680, 810))) + face(540, 670, .95),
                   "".join(f'<path d="M{x} {y} q12 30 0 50 q-12 -20 0 -50z" fill="#4dabf7"/>' for x, y in ((860, 260), (930, 320), (990, 250), (900, 400))))
BLUEBERRY = scene("".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#4f46e5" stroke="#312e81" stroke-width="8"/><path d="M{x-14} {y-r+10} l14 -14 14 14" stroke="#312e81" stroke-width="6" fill="none"/>' for x, y, r in ((360, 820, 120), (720, 820, 120)))
                  + '<circle cx="540" cy="660" r="230" fill="#6366f1" stroke="#312e81" stroke-width="10"/><path d="M510 440 l30 -30 30 30" stroke="#312e81" stroke-width="10" fill="none"/>' + face(540, 660, 1.15, "#fff"),
                  '<g transform="translate(900 340)"><ellipse rx="130" ry="90" fill="#3aa856"/>' + "".join(f'<circle cx="{dx}" cy="{dy}" r="22" fill="#4f46e5"/>' for dx, dy in ((-60, -10), (-20, 30), (30, -20), (70, 20), (0, -50))) + '</g>')
CARROT = scene('<path d="M380 450 Q540 400 700 450 L560 980 Q540 1000 520 980Z" fill="#fb923c" stroke="#ea580c" stroke-width="10"/>'
               + "".join(f'<path d="M{430+i*20} {560+i*90} q50 10 90 0" stroke="#ea580c" stroke-width="6" fill="none"/>' for i in range(4))
               + leaf(500, 380, -70, s=1.3) + leaf(580, 370, -100, s=1.3) + leaf(540, 360, -85, s=1.4) + face(545, 560, 1.0),
               '<path d="M-500 900 L1600 900 L1600 1000 L-500 1000Z" fill="#8d6e63" opacity=".55"/><path d="M450 900 L640 900" stroke="#fff59d" stroke-width="10" stroke-dasharray="20 12"/>',
               "".join(f'<path d="M{x-40} 300 Q{x} 290 {x+40} 300 L{x+6} 480 Q{x} 490 {x-6} 480Z" fill="{c}"/>' for x, c in ((820, "#7e22ce"), (900, "#facc15"), (980, "#f8fafc"))))
BROCCOLI = scene('<path d="M470 980 L490 700 L590 700 L610 980Z" fill="#86efac" stroke="#15803d" stroke-width="10"/>'
                 + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#22c55e" stroke="#15803d" stroke-width="8"/>' for x, y, r in ((380, 560, 130), (540, 480, 150), (700, 560, 130), (460, 660, 110), (630, 660, 110)))
                 + face(540, 600, 1.1),
                 '<g fill="none" stroke="#fff59d" stroke-width="10" stroke-dasharray="18 10">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r+20}"/>' for x, y, r in ((380, 560, 130), (540, 480, 150), (700, 560, 130))) + '</g>')
PEAS = scene('<path d="M140 700 Q540 420 940 700 Q540 940 140 700Z" fill="#4ade80" stroke="#15803d" stroke-width="10"/>'
             + "".join(f'<circle cx="{x}" cy="690" r="78" fill="#22c55e" stroke="#15803d" stroke-width="6"/><circle class="pupil" cx="{x-22}" cy="680" r="11" fill="#1a1a2e"/><circle class="pupil" cx="{x+22}" cy="680" r="11" fill="#1a1a2e"/><path d="M{x-20} 710 q20 14 40 0" stroke="#14532d" stroke-width="6" fill="none" stroke-linecap="round"/>' for x in (330, 480, 630, 770)),
             "".join(f'<text x="{x}" y="590" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="70" fill="#7a2b2b">{i+1}</text>' for i, x in enumerate((330, 480, 630, 770))))
CORN = scene('<ellipse cx="540" cy="660" rx="170" ry="320" fill="#fde047" stroke="#ca8a04" stroke-width="10"/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="22" fill="#facc15" stroke="#eab308" stroke-width="3"/>' for x in range(430, 660, 48) for y in range(400, 940, 50) if ((x-540)/170)**2 + ((y-660)/320)**2 < .8)
             + '<path d="M370 980 Q320 700 420 420 Q430 700 520 990Z" fill="#4ade80" stroke="#15803d" stroke-width="8"/><path d="M710 980 Q760 700 660 420 Q650 700 560 990Z" fill="#4ade80" stroke="#15803d" stroke-width="8"/>'
             + face(540, 600, 1.0),
             '<g stroke="#fef08a" stroke-width="6" fill="none">' + "".join(f'<path d="M{520+i*10} 340 Q{500+i*20} 260 {480+i*25} 220"/>' for i in range(5)) + '</g>')
PUMPKIN = scene("".join(f'<ellipse cx="{x}" cy="720" rx="{rx}" ry="260" fill="#f97316" stroke="#c2410c" stroke-width="10"/>' for x, rx in ((390, 170), (690, 170), (540, 200)))
                + '<path d="M520 470 Q510 400 560 380" stroke="#4d7c0f" stroke-width="30" fill="none" stroke-linecap="round"/>' + face(540, 700, 1.15),
                '<path d="M560 400 Q760 300 900 420 Q1000 520 1060 460" stroke="#4d7c0f" stroke-width="16" fill="none"/>' + leaf(820, 340, 20, s=1.2) + leaf(980, 470, -30))

# ---------- healthy habits ----------
def kid(cx, cy, c="#ffd6a5", hair="#5d4037", shirt="#60a5fa"):
    return (f'<rect x="{cx-90}" y="{cy+90}" width="180" height="200" rx="70" fill="{shirt}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="120" fill="{c}"/><path d="M{cx-120} {cy-20} Q{cx-100} {cy-150} {cx} {cy-130} Q{cx+110} {cy-150} {cx+120} {cy-20} Q{cx+60} {cy-90} {cx-120} {cy-20}Z" fill="{hair}"/>'
            + face(cx, cy + 10, .8))
HANDWASH = scene('<rect x="250" y="760" width="580" height="220" rx="30" fill="#e0f2fe" stroke="#7dd3fc" stroke-width="10"/><ellipse cx="540" cy="770" rx="250" ry="40" fill="#bae6fd"/>'
                 '<path d="M700 560 L700 640 Q700 670 670 670 L620 670" stroke="#94a3b8" stroke-width="30" fill="none" stroke-linecap="round"/><rect x="680" y="530" width="60" height="40" rx="10" fill="#94a3b8"/>'
                 '<rect x="300" y="610" width="80" height="140" rx="20" fill="#f9a8d4"/><rect x="320" y="580" width="40" height="40" rx="8" fill="#f472b6"/>'
                 '<ellipse cx="500" cy="720" rx="70" ry="40" fill="#ffd6a5" stroke="#e8a77a" stroke-width="6"/><ellipse cx="580" cy="720" rx="70" ry="40" fill="#ffd6a5" stroke="#e8a77a" stroke-width="6"/>'
                 + face(540, 880, .9),
                 bubbles([(430, 650, 40), (520, 610, 30), (600, 640, 46), (680, 600, 26), (470, 560, 22), (640, 540, 34)]),
                 '<g transform="translate(860 300)"><circle r="100" fill="#fff" stroke="#7a2b2b" stroke-width="10"/><text y="35" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="100" fill="#3aa856">20</text></g>')
TOOTH = scene('<path d="M330 480 Q330 380 450 390 Q540 420 630 390 Q750 380 750 480 Q760 640 700 760 Q680 960 620 960 Q590 960 580 860 Q560 800 540 800 Q520 800 500 860 Q490 960 460 960 Q400 960 380 760 Q320 640 330 480Z" fill="#fff" stroke="#93c5fd" stroke-width="12"/>'
              + face(540, 600, 1.05),
              '<g transform="rotate(-30 860 420)"><rect x="700" y="400" width="340" height="40" rx="20" fill="#3aa856"/><rect x="700" y="350" width="90" height="56" rx="12" fill="#fff" stroke="#93c5fd" stroke-width="6"/><path d="M710 350 v-30 M730 350 v-30 M750 350 v-30 M770 350 v-30" stroke="#60a5fa" stroke-width="8"/></g>' + sparkles([(300, 380), (790, 330), (820, 620)]),
              '<g transform="translate(150 330)"><circle r="90" fill="#fff" stroke="#7a2b2b" stroke-width="10"/><text y="30" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="62" fill="#3aa856">2:00</text></g>')
WATER = scene('<path d="M360 440 L720 440 L680 980 L400 980Z" fill="#e0f2fe" stroke="#7dd3fc" stroke-width="12" opacity=".95"/><path d="M372 560 L708 560 L680 970 L400 970Z" fill="#38bdf8"/>'
              '<path d="M600 460 L700 300" stroke="#f472b6" stroke-width="22" stroke-linecap="round"/>' + face(540, 720, 1.0, "#0c4a6e"),
              "".join(f'<path d="M{x} {y} q18 40 0 70 q-18 -30 0 -70z" fill="#38bdf8"/>' for x, y in ((180, 340), (900, 300), (960, 460), (120, 520))))
SLEEP = scene('<rect x="160" y="700" width="760" height="200" rx="30" fill="#c4b5fd"/><rect x="140" y="560" width="60" height="420" rx="20" fill="#a78bfa"/><rect x="880" y="620" width="60" height="360" rx="20" fill="#a78bfa"/>'
              '<ellipse cx="320" cy="660" rx="120" ry="60" fill="#fff"/><path d="M220 720 L900 720 L900 880 L220 880Z" fill="#f9a8d4"/>'
              '<circle cx="330" cy="610" r="90" fill="#ffd6a5"/><path d="M290 610 q20 14 40 0 M350 610 q20 14 40 0" stroke="#1a1a2e" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M315 655 q15 10 30 0" stroke="#7a2b2b" stroke-width="6" fill="none"/>'
              '<path d="M240 560 Q260 480 330 500 Q400 480 420 560 Q360 520 240 560Z" fill="#5d4037"/>',
              '<path d="M820 200 A110 110 0 1 0 900 380 A90 90 0 1 1 820 200Z" fill="#fde047"/>' + sparkles([(640, 260), (720, 380), (580, 400)], "#fef9c3"),
              '<text x="560" y="520" font-family="Baloo, sans-serif" font-weight="800" font-size="80" fill="#7c3aed">Z z z</text>')
SHARE = scene(kid(340, 560, shirt="#60a5fa") + kid(740, 560, c="#c68642", hair="#1a1a2e", shirt="#f472b6")
              + '<circle cx="540" cy="760" r="80" fill="#facc15" stroke="#ca8a04" stroke-width="8"/><path d="M460 760 q80 -50 160 0" stroke="#ef4444" stroke-width="10" fill="none"/>',
              "".join(f'<path d="M{x} {y+40} C{x-70} {y} {x-40} {y-50} {x} {y-20} C{x+40} {y-50} {x+70} {y} {x} {y+40}Z" fill="#fb7185"/>' for x, y in ((540, 380), (420, 330), (660, 330))),
              '<path d="M440 860 Q540 920 640 860" stroke="#3aa856" stroke-width="14" fill="none" stroke-dasharray="20 12"/><path d="M630 845 l20 18 -26 8z" fill="#3aa856"/>')
VEGGIEPLATE = scene('<ellipse cx="540" cy="820" rx="400" ry="150" fill="#fff" stroke="#e2e8f0" stroke-width="12"/><ellipse cx="540" cy="810" rx="320" ry="110" fill="#f8fafc"/>'
                    '<circle cx="420" cy="790" r="60" fill="#22c55e"/><circle cx="470" cy="760" r="50" fill="#22c55e"/><rect x="560" y="770" width="140" height="30" rx="15" fill="#fb923c" transform="rotate(-15 630 785)"/>'
                    '<circle cx="660" cy="830" r="30" fill="#ef4444"/><circle cx="610" cy="840" r="26" fill="#4f46e5"/>' + face(540, 560, 1.1),
                    "".join(f'<rect x="{150 + i*170}" y="300" width="120" height="120" rx="24" fill="{c}"/>' for i, c in enumerate(("#ef4444", "#fb923c", "#facc15", "#22c55e", "#6366f1"))))

FRUITY_TITLE = svg(kitchen_env() + """
  <g transform="translate(-130 -40)">
    <rect x="200" y="230" width="680" height="150" rx="44" fill="#3aa856" stroke="#15803d" stroke-width="10"/>
    <text x="540" y="333" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="74" fill="#fff">FRUITY FRIENDS</text>
    <path d="M360 760 Q420 980 540 980 Q660 980 720 760Z" fill="#fde68a" stroke="#d97706" stroke-width="10"/>
    <circle cx="460" cy="740" r="70" fill="#ef4444"/><circle cx="560" cy="720" r="74" fill="#fb923c"/><path d="M600 760 Q700 640 690 760Z" fill="#ffd43b"/><circle cx="640" cy="760" r="50" fill="#22c55e"/>
  </g>""")

SCENES8 = {"apple": APPLE, "banana": BANANA, "orangefruit": ORANGE, "watermelon": WATERMELON, "blueberry": BLUEBERRY,
           "carrot": CARROT, "broccoli": BROCCOLI, "peas": PEAS, "corn": CORN, "pumpkin": PUMPKIN,
           "handwash": HANDWASH, "toothbrush": TOOTH, "water": WATER, "sleep": SLEEP, "share": SHARE, "plate": VEGGIEPLATE}
NAMES8 = {"orangefruit": "ORANGE", "handwash": "WASH HANDS", "toothbrush": "BRUSH TEETH", "water": "DRINK WATER", "sleep": "BEDTIME", "share": "SHARING",
          "plate": "RAINBOW PLATE", "blueberry": "BLUEBERRIES", "peas": "PEAS"}

PIPKIKO = """<svg id="milo" viewBox="0 0 220 200" width="260" height="236">
  <g id="wing"><rect x="168" y="150" width="22" height="40" rx="8" fill="#86efac" stroke="#15803d" stroke-width="3"/>
    <circle cx="166" cy="140" r="18" fill="#22c55e"/><circle cx="192" cy="136" r="20" fill="#22c55e"/><circle cx="180" cy="120" r="18" fill="#22c55e"/>
    <circle cx="174" cy="140" r="3.5" fill="#1a1a2e"/><circle cx="188" cy="140" r="3.5" fill="#1a1a2e"/><path d="M174 150 q7 5 14 0" stroke="#14532d" stroke-width="2.5" fill="none"/></g>
  <path d="M110 192 C40 150 30 80 60 54 C80 38 140 38 160 54 C190 80 180 150 110 192Z" fill="#ef4444" stroke="#b91c1c" stroke-width="5"/>
  """ + "".join(f'<ellipse cx="{x}" cy="{y}" rx="3" ry="5" fill="#fde68a"/>' for x, y in ((70, 80), (150, 80), (80, 140), (140, 140), (110, 165), (60, 110), (160, 110))) + """
  <path d="M70 52 Q90 20 110 46 Q130 20 150 52 Q110 60 70 52Z" fill="#22c55e"/>
  <circle cx="90" cy="92" r="15" fill="#fff"/><circle cx="130" cy="92" r="15" fill="#fff"/>
  <ellipse class="mpupil" cx="92" cy="94" rx="7.5" ry="9.5" fill="#1a1a2e"/><ellipse class="mpupil" cx="132" cy="94" rx="7.5" ry="9.5" fill="#1a1a2e"/>
  <circle class="glint" cx="95" cy="89" r="3.5" fill="#fff"/><circle class="glint" cx="135" cy="89" r="3.5" fill="#fff"/>
  <path d="M97 108 q13 9 26 0" stroke="#7a1414" stroke-width="5" fill="none" stroke-linecap="round"/>
  <ellipse id="beaklow" cx="110" cy="117" rx="8" ry="2.2" fill="#7a1414"/>
  <circle cx="72" cy="114" r="7" fill="#ff9ab0" opacity=".8"/><circle cx="148" cy="114" r="7" fill="#ff9ab0" opacity=".8"/>
</svg>"""
