"""Week-2 art for Tiny Truck Town: 25 new friendly vehicles and town places.
Same frame/style as art_truck.py: 1080x1100 viewBox, road at ~y1000, front of every vehicle faces right,
<g id="animal"> + <g id="fx" opacity="0"> + <g id="fx2" opacity="0">. All keys start with "tt2_"."""
import math
from art_truck import svg, town_env, wheel, face, cab, tracks

YEL = "#ffeb3b"  # highlight color used by the week-1 fx layers


def smallcar(x, y, color, s=1.0, rot=0):
    """Small friendly car, front to the right. (x, y) = top-left of its 380x235 box."""
    r = f' rotate({rot} 190 190)' if rot else ''
    return (f'<g transform="translate({x} {y}) scale({s}){r}">'
            f'<path d="M0 170 Q0 120 50 115 L90 115 L140 40 L280 40 L330 115 L360 120 Q380 125 380 170 L380 190 L0 190Z" fill="{color}"/>'
            '<path d="M150 55 L205 55 L205 115 L110 115Z" fill="#bde9ff"/><path d="M220 55 L272 55 L315 115 L220 115Z" fill="#bde9ff"/>'
            + face(262, 88, .5, False)
            + '<path d="M300 150 q18 12 36 0" stroke="#263238" stroke-width="6" fill="none" stroke-linecap="round"/>'
            '<ellipse cx="282" cy="140" rx="12" ry="7" fill="#ff8fab" opacity=".6"/>'
            '<circle cx="368" cy="148" r="11" fill="#fff59d"/>'
            + wheel(95, 195, 38) + wheel(290, 195, 38) + '</g>')


def box(x, y, w, h, c="#d7a86e"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}" stroke="#a1774a" stroke-width="4"/>'
            f'<rect x="{x+w//2-9}" y="{y}" width="18" height="{h}" fill="#f2d6a8"/>')


def note(x, y, c="#7e57c2", s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{c}"><ellipse cx="0" cy="40" rx="20" ry="15"/>'
            f'<rect x="14" y="-30" width="8" height="70"/><path d="M22 -30 q34 10 26 46 q-4 -22 -26 -24z"/></g>')


def env_snow():
    flakes = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".9"/>' for x, y, r in
                     ((80, 330, 9), (260, 420, 7), (420, 300, 10), (560, 460, 8), (700, 330, 9), (880, 420, 10), (1000, 300, 7),
                      (150, 560, 8), (980, 560, 9), (340, 600, 7), (620, 250, 7), (40, 760, 8), (1040, 720, 9)))
    banks = ('<path d="M-500 1000 Q-300 930 -100 975 Q60 925 200 980 Q260 1000 300 1000Z" fill="#fff"/>'
             '<path d="M1080 1000 Q1250 930 1400 970 Q1550 930 1700 1000Z" fill="#fff"/>')
    return town_env() + flakes + banks


def env_water():
    waves = "".join(f'<path d="M{x} 905 q40 -22 80 0 t80 0" stroke="#e1f5fe" stroke-width="8" fill="none" opacity=".8"/>' for x in range(-460, 1620, 240))
    return ('<circle cx="170" cy="150" r="85" fill="#ffe066"/>'
            '<g id="cloud1" opacity=".95"><ellipse cx="760" cy="140" rx="110" ry="42" fill="#fff"/><ellipse cx="700" cy="120" rx="60" ry="45" fill="#fff"/><ellipse cx="820" cy="118" rx="55" ry="40" fill="#fff"/></g>'
            '<path d="M-500 860 Q-300 760 -60 850 L-60 870 L-500 870Z" fill="#a5d6a7"/><path d="M1150 850 Q1400 740 1700 860 L1700 870 L1150 870Z" fill="#a5d6a7"/>'
            '<rect x="-500" y="860" width="2200" height="260" fill="#4fc3f7"/>' + waves)


def env_water_front():
    """Waves drawn over the bottom of the hull so the boat sits in the water."""
    return ('<path d="M-500 930 Q-420 905 -340 930 T-180 930 T-20 930 T140 930 T300 930 T460 930 T620 930 T780 930 T940 930 T1100 930 T1260 930 T1420 930 T1580 930 L1700 930 L1700 1120 L-500 1120Z" fill="#29b6f6"/>'
            + "".join(f'<path d="M{x} 990 q30 -16 60 0" stroke="#e1f5fe" stroke-width="7" fill="none" opacity=".8"/>' for x in range(-440, 1620, 200)))


def env_airport():
    return ('<circle cx="170" cy="150" r="85" fill="#ffe066"/>'
            '<g id="cloud1" opacity=".95"><ellipse cx="760" cy="140" rx="110" ry="42" fill="#fff"/><ellipse cx="700" cy="120" rx="60" ry="45" fill="#fff"/><ellipse cx="820" cy="118" rx="55" ry="40" fill="#fff"/></g>'
            '<rect x="-480" y="640" width="380" height="340" rx="12" fill="#9fa8da" opacity=".55"/><rect x="-440" y="560" width="70" height="90" rx="10" fill="#9fa8da" opacity=".55"/>'
            '<rect x="1300" y="700" width="400" height="280" rx="12" fill="#9fa8da" opacity=".55"/>'
            '<rect x="-500" y="975" width="2200" height="30" fill="#cfd8dc"/><rect x="-500" y="1000" width="2200" height="120" fill="#90a4ae"/>'
            '<g fill="#ffd54f">' + "".join(f'<rect x="{x}" y="1050" width="90" height="12" rx="6"/>' for x in range(-480, 1600, 150)) + '</g>')


def tire(cx, cy, r, hub="#ffca28"):
    notches = "".join(f'<rect x="{cx-14}" y="{cy-r-8}" width="28" height="30" rx="6" fill="#263238" transform="rotate({a} {cx} {cy})"/>' for a in range(0, 360, 30))
    return (notches + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#263238"/><circle cx="{cx}" cy="{cy}" r="{int(r*.62)}" fill="#37474f"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{int(r*.42)}" fill="{hub}"/><circle cx="{cx}" cy="{cy}" r="{int(r*.15)}" fill="#f57f17"/>')


def arrow_up(x, y, c=YEL):
    return f'<path d="M{x} {y+90} L{x} {y}" stroke="{c}" stroke-width="14" stroke-linecap="round"/><path d="M{x-30} {y+30} L{x} {y} L{x+30} {y+30}" stroke="{c}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def arrow_right(x, y, c=YEL):
    return f'<path d="M{x} {y} L{x+110} {y}" stroke="{c}" stroke-width="14" stroke-linecap="round"/><path d="M{x+80} {y-30} L{x+112} {y} L{x+80} {y+30}" stroke="{c}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def sparkle(x, y, s=1.0, c="#fff59d"):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 -40 Q6 -6 40 0 Q6 6 0 40 Q-6 6 -40 0 Q-6 -6 0 -40Z" fill="{c}"/>'


def env():
    return town_env()


# ---------------------------------------------------------------- vehicles
TOWTRUCK = svg(env() + """
  <g id="animal">
    <rect x="150" y="740" width="580" height="150" rx="22" fill="#c62828"/>
    <rect x="180" y="770" width="160" height="70" rx="12" fill="#b71c1c"/>
    <path d="M330 750 L190 520" stroke="#455a64" stroke-width="30" stroke-linecap="round"/>
    <circle cx="330" cy="750" r="26" fill="#37474f"/>
    <line x1="190" y1="520" x2="190" y2="690" stroke="#37474f" stroke-width="7"/>
    <path d="M168 688 h44 v20 q-22 46 -44 0z" fill="#fdd835" stroke="#f9a825" stroke-width="5"/>
    """ + cab(700, 590, 250, 310, "#e53935") + """
    <rect x="780" y="566" width="90" height="26" rx="10" fill="#ffb300"/>
    """ + wheel(280) + wheel(520) + wheel(830) + """
  </g>
  <g id="fx" opacity="0">""" + smallcar(-10, 690, "#42a5f5", .55, -14) + """
    <circle cx="190" cy="700" r="70" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="18 10"/></g>
  <g id="fx2" opacity="0"><ellipse cx="825" cy="572" rx="80" ry="34" fill="#ffb300" opacity=".45"/><path d="M760 545 l-30 -40 M825 530 v-50 M890 545 l30 -40" stroke="#ffb300" stroke-width="12" stroke-linecap="round"/></g>""")

SWEEPER = svg(env() + """
  <g id="animal">
    <rect x="140" y="620" width="580" height="270" rx="34" fill="#26a69a"/>
    <rect x="170" y="650" width="210" height="160" rx="18" fill="#00897b"/>
    <rect x="400" y="650" width="290" height="70" rx="16" fill="#80cbc4"/>
    <circle cx="430" cy="685" r="14" fill="#4fc3f7"/><circle cx="470" cy="685" r="14" fill="#4fc3f7"/><circle cx="510" cy="685" r="14" fill="#4fc3f7"/>
    """ + cab(700, 600, 240, 300, "#4db6ac") + """
    <rect x="600" y="880" width="20" height="60" fill="#546e7a"/>
    <g id="brush"><circle cx="610" cy="950" r="50" fill="#ffca28"/>""" + "".join(
        f'<line x1="610" y1="950" x2="{610+48*math.cos(a):.0f}" y2="{950+48*math.sin(a):.0f}" stroke="#f57f17" stroke-width="6"/>' for a in [i * 0.5236 for i in range(12)]) + """
      <circle cx="610" cy="950" r="14" fill="#f57f17"/></g>
    """ + wheel(270) + wheel(830) + """
  </g>
  <g id="fx" opacity="0"><circle cx="610" cy="950" r="78" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="20 12"/>
    <path d="M520 860 A100 100 0 0 1 700 860" stroke="#ffeb3b" stroke-width="10" fill="none"/><path d="M700 860 l-8 -40 M700 860 l-40 -6" stroke="#ffeb3b" stroke-width="10" stroke-linecap="round"/></g>
  <g id="fx2" opacity="0"><g fill="#4fc3f7">""" + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
        ((560, 960, 10), (520, 940, 8), (680, 965, 9), (700, 935, 7), (540, 985, 7), (660, 990, 8), (590, 905, 7), (640, 910, 6))) + """</g>
    <path d="M150 600 Q140 560 170 540 M200 600 Q200 560 230 545" stroke="#b3e5fc" stroke-width="8" fill="none" stroke-linecap="round"/></g>""")

FORKLIFT = svg(env() + """
  <g id="animal">
    <rect x="190" y="690" width="140" height="220" rx="40" fill="#616161"/>
    <rect x="260" y="720" width="440" height="190" rx="30" fill="#ffa000"/>
    <rect x="300" y="430" width="16" height="300" fill="#424242"/><rect x="640" y="430" width="16" height="300" fill="#424242"/>
    <rect x="290" y="420" width="380" height="22" rx="10" fill="#424242"/>
    """ + cab(340, 500, 290, 280, "#ffb300") + """
    <rect x="705" y="400" width="26" height="580" rx="8" fill="#455a64"/><rect x="745" y="400" width="26" height="580" rx="8" fill="#546e7a"/>
    <rect x="770" y="800" width="30" height="160" rx="6" fill="#37474f"/>
    <rect x="770" y="940" width="260" height="20" rx="6" fill="#37474f"/>
    <rect x="800" y="905" width="220" height="34" rx="4" fill="#a1887f"/><rect x="820" y="912" width="30" height="20" fill="#795548"/><rect x="895" y="912" width="30" height="20" fill="#795548"/><rect x="970" y="912" width="30" height="20" fill="#795548"/>
    """ + box(805, 785, 100, 120) + box(910, 785, 105, 120, "#e0b07a") + box(855, 665, 110, 120, "#c99b62") + """
    """ + wheel(330, 940, 60) + wheel(610, 940, 60) + """
  </g>
  <g id="fx" opacity="0">""" + arrow_up(1050, 520) + arrow_up(640, 280) + """</g>
  <g id="fx2" opacity="0"><rect x="790" y="650" width="240" height="320" rx="14" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="22 12"/></g>""")

ROLLER = svg(env() + """
  <g id="animal">
    <rect x="300" y="430" width="330" height="30" rx="12" fill="#f57f17"/>
    <rect x="320" y="455" width="16" height="70" fill="#5d4037"/><rect x="594" y="455" width="16" height="70" fill="#5d4037"/>
    <rect x="190" y="740" width="540" height="140" rx="34" fill="#fdd835"/>
    """ + cab(330, 500, 270, 280, "#fbc02d") + """
    <rect x="660" y="750" width="160" height="56" rx="14" fill="#f9a825"/>
    <path d="M660 760 Q800 690 940 800 L900 820 Q800 750 680 800Z" fill="#f9a825"/>
    <circle cx="800" cy="880" r="120" fill="#90a4ae" stroke="#607d8b" stroke-width="8"/>
    <circle cx="800" cy="880" r="70" fill="#b0bec5"/><circle cx="800" cy="880" r="24" fill="#607d8b"/>
    """ + wheel(300, 920, 80) + """
  </g>
  <g id="fx" opacity="0"><rect x="-500" y="1000" width="1180" height="40" fill="#263238"/>""" + sparkle(140, 1018, .5, "#fff") + sparkle(420, 1018, .4, "#fff") + """</g>
  <g id="fx2" opacity="0"><circle cx="800" cy="880" r="150" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="22 12"/></g>""")

CHERRYPICKER = svg(env() + """
  <g id="animal">
    <rect x="80" y="200" width="22" height="800" rx="8" fill="#78909c"/>
    <path d="M91 210 Q91 150 170 150 L200 150" stroke="#78909c" stroke-width="20" fill="none" stroke-linecap="round"/>
    <path d="M180 140 h70 v30 q-35 26 -70 0z" fill="#607d8b"/><ellipse cx="215" cy="176" rx="26" ry="10" fill="#fff59d"/>
    <rect x="140" y="700" width="580" height="190" rx="24" fill="#ff7043"/>
    <g fill="#f4511e"><rect x="170" y="730" width="120" height="110" rx="10"/><rect x="310" y="730" width="120" height="110" rx="10"/></g>
    <path d="M520 710 L380 420" stroke="#eceff1" stroke-width="34" stroke-linecap="round"/>
    <path d="M380 420 L300 330" stroke="#cfd8dc" stroke-width="26" stroke-linecap="round"/>
    <circle cx="520" cy="710" r="30" fill="#90a4ae"/><circle cx="380" cy="420" r="22" fill="#90a4ae"/>
    <rect x="230" y="250" width="150" height="110" rx="22" fill="#ffca28" stroke="#f9a825" stroke-width="6"/>
    <rect x="230" y="270" width="150" height="14" fill="#f9a825"/>
    """ + cab(700, 600, 240, 300, "#ff8a65") + wheel(270) + wheel(520) + wheel(830) + """
  </g>
  <g id="fx" opacity="0"><circle cx="215" cy="180" r="60" fill="#fff59d" opacity=".7"/><circle cx="215" cy="180" r="110" fill="#fff59d" opacity=".3"/></g>
  <g id="fx2" opacity="0"><path d="M520 710 L380 420 L300 330" stroke="#ffeb3b" stroke-width="12" fill="none" stroke-dasharray="22 12"/></g>""")

MONSTER = svg(env() + """
  <g id="animal">
    <path d="M330 830 l-40 -40 l60 -30 l-60 -30 l60 -30 l-40 -30" stroke="#b0bec5" stroke-width="16" fill="none" stroke-linejoin="round"/>
    <path d="M790 830 l-40 -40 l60 -30 l-60 -30 l60 -30 l-40 -30" stroke="#b0bec5" stroke-width="16" fill="none" stroke-linejoin="round"/>
    """ + tire(300, 830, 160) + tire(790, 830, 160) + """
    <rect x="130" y="560" width="470" height="140" rx="34" fill="#8e24aa"/>
    <path d="M220 610 l14 -28 14 28 30 4 -22 20 6 30 -28 -14 -28 14 6 -30 -22 -20z" fill="#fdd835"/>
    <path d="M380 610 l14 -28 14 28 30 4 -22 20 6 30 -28 -14 -28 14 6 -30 -22 -20z" fill="#fdd835"/>
    """ + cab(570, 410, 310, 300, "#ab47bc") + """
  </g>
  <g id="fx" opacity="0"><circle cx="300" cy="830" r="200" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="24 14"/><circle cx="790" cy="830" r="200" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="24 14"/></g>
  <g id="fx2" opacity="0"><path d="M120 470 q40 -40 80 0 M880 400 q40 -40 80 0 M940 470 q30 -30 60 0" stroke="#ffeb3b" stroke-width="10" fill="none" stroke-linecap="round"/>
    """ + arrow_up(70, 380) + arrow_up(1010, 250) + """</g>""")

ICECREAM = svg(env() + """
  <g id="animal">
    <polygon points="350,470 450,470 400,575" fill="#ffcc80" stroke="#e0a050" stroke-width="5"/>
    <circle cx="372" cy="450" r="44" fill="#f48fb1"/><circle cx="428" cy="450" r="44" fill="#a5d6a7"/><circle cx="400" cy="400" r="44" fill="#fff59d"/>
    <circle cx="400" cy="352" r="12" fill="#e53935"/>
    <rect x="120" y="570" width="620" height="330" rx="40" fill="#f8bbd0"/>
    <rect x="120" y="800" width="620" height="30" fill="#f06292"/>
    <rect x="190" y="640" width="320" height="140" rx="16" fill="#fff3e0" stroke="#f06292" stroke-width="6"/>
    """ + "".join(f'<circle cx="{x}" cy="640" r="20" fill="{c}"/>' for x, c in zip(range(200, 520, 40), ["#f06292", "#fff", "#f06292", "#fff", "#f06292", "#fff", "#f06292", "#fff"])) + """
    <rect x="560" y="640" width="120" height="100" rx="14" fill="#bde9ff"/>
    """ + cab(720, 600, 230, 300, "#f48fb1") + wheel(260) + wheel(560) + wheel(830) + """
  </g>
  <g id="fx" opacity="0">""" + note(170, 470) + note(560, 400, "#42a5f5", .9) + note(960, 420, "#ef5350", .8) + note(690, 300, "#66bb6a", .7) + """</g>
  <g id="fx2" opacity="0">""" + "".join(f'<polygon points="{x-20},740 {x+20},740 {x},790" fill="#ffcc80"/><circle cx="{x}" cy="728" r="24" fill="{c}"/>' for x, c in ((260, "#f48fb1"), (350, "#a5d6a7"), (440, "#fff59d"))) + """</g>""")

MAIL = svg(env() + """
  <g id="animal">
    <rect x="160" y="560" width="560" height="340" rx="28" fill="#ffffff" stroke="#cfd8dc" stroke-width="6"/>
    <rect x="160" y="790" width="560" height="22" fill="#1e88e5"/><rect x="160" y="812" width="560" height="14" fill="#e53935"/>
    <rect x="300" y="620" width="200" height="130" rx="12" fill="#fff8e1" stroke="#90a4ae" stroke-width="6"/>
    <path d="M300 625 L400 700 L500 625" stroke="#90a4ae" stroke-width="6" fill="none" stroke-linejoin="round"/>
    <circle cx="400" cy="700" r="16" fill="#e53935"/>
    """ + cab(700, 600, 240, 300, "#fafafa") + """
    <rect x="700" y="800" width="240" height="22" fill="#1e88e5"/>
    """ + wheel(280) + wheel(830) + """
  </g>
  <g id="fx" opacity="0">""" + "".join(
        f'<g transform="translate({x} {y}) rotate({r})"><rect x="0" y="0" width="110" height="74" rx="8" fill="#fff8e1" stroke="#90a4ae" stroke-width="5"/><path d="M0 4 L55 44 L110 4" stroke="#90a4ae" stroke-width="5" fill="none"/></g>'
        for x, y, r in ((560, 380, -12), (760, 300, 8), (920, 430, -6))) + """</g>
  <g id="fx2" opacity="0"><rect x="980" y="830" width="22" height="170" fill="#8d6e63"/>
    <path d="M940 840 L940 780 Q940 740 990 740 Q1040 740 1040 780 L1040 840Z" fill="#1565c0"/><rect x="1030" y="760" width="10" height="60" fill="#e53935"/><rect x="1030" y="760" width="40" height="22" fill="#e53935"/></g>""")

VAN = svg(env() + """
  <g id="animal">
    <rect x="130" y="580" width="620" height="320" rx="44" fill="#7cb342"/>
    <rect x="130" y="580" width="620" height="40" rx="20" fill="#9ccc65"/>
    <rect x="430" y="630" width="170" height="240" rx="14" fill="none" stroke="#558b2f" stroke-width="8"/>
    <rect x="450" y="740" width="40" height="14" rx="7" fill="#558b2f"/>
    """ + box(200, 680, 160, 120) + """
    """ + cab(700, 600, 240, 300, "#9ccc65") + wheel(270) + wheel(830) + """
  </g>
  <g id="fx" opacity="0">""" + box(10, 900, 110, 100) + box(20, 800, 95, 100, "#e0b07a") + box(560, 420, 120, 100, "#c99b62") + arrow_right(700, 470) + """</g>
  <g id="fx2" opacity="0"><rect x="415" y="615" width="200" height="270" rx="20" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="22 12"/></g>""")

TANKER = svg(env() + """
  <defs><clipPath id="tt2tank"><rect x="110" y="600" width="600" height="240" rx="120"/></clipPath></defs>
  <g id="animal">
    <rect x="130" y="830" width="600" height="50" rx="12" fill="#546e7a"/>
    <rect x="110" y="600" width="600" height="240" rx="120" fill="#e0e0e0" stroke="#90a4ae" stroke-width="8"/>
    <rect x="130" y="630" width="560" height="26" rx="13" fill="#ffffff" opacity=".7"/>
    <g stroke="#b0bec5" stroke-width="8"><line x1="300" y1="604" x2="300" y2="836"/><line x1="520" y1="604" x2="520" y2="836"/></g>
    <rect x="360" y="575" width="100" height="30" rx="8" fill="#90a4ae"/>
    <path d="M410 680 Q440 730 440 755 A30 30 0 0 1 380 755 Q380 730 410 680Z" fill="#42a5f5"/>
    """ + cab(700, 590, 240, 310, "#5c6bc0") + wheel(230) + wheel(380) + wheel(830) + """
  </g>
  <g id="fx" opacity="0"><path d="M120 760 Q60 800 70 900" stroke="#455a64" stroke-width="18" fill="none" stroke-linecap="round"/>
    <path d="M70 920 Q84 950 84 962 A14 14 0 0 1 56 962 Q56 950 70 920Z" fill="#42a5f5"/><path d="M110 950 Q122 975 122 985 A12 12 0 0 1 98 985 Q98 975 110 950Z" fill="#42a5f5"/></g>
  <g id="fx2" opacity="0"><g clip-path="url(#tt2tank)"><path d="M110 720 Q190 690 270 720 T430 720 T590 720 T750 720 L750 860 L110 860Z" fill="#81d4fa" opacity=".9"/></g>
    <rect x="110" y="600" width="600" height="240" rx="120" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="22 12"/></g>""")

CARCARRIER = svg(env() + """
  <g id="animal">
    <rect x="40" y="836" width="720" height="44" rx="10" fill="#546e7a"/>
    <rect x="40" y="820" width="720" height="22" rx="8" fill="#78909c"/>
    <rect x="40" y="598" width="720" height="22" rx="8" fill="#78909c"/>
    <g fill="#90a4ae"><rect x="50" y="610" width="18" height="216"/><rect x="390" y="610" width="18" height="216"/><rect x="730" y="610" width="18" height="216"/></g>
    """ + smallcar(70, 494, "#ef5350", .45) + smallcar(250, 494, "#fdd835", .45) + smallcar(430, 494, "#ab47bc", .45) + smallcar(570, 494, "#42a5f5", .45)
    + smallcar(80, 716, "#66bb6a", .45) + smallcar(260, 716, "#ff7043", .45) + smallcar(440, 716, "#26c6da", .45) + """
    """ + cab(760, 600, 210, 300, "#3949ab") + wheel(130, 950, 50) + wheel(250, 950, 50) + wheel(640, 950, 50) + wheel(865) + """
  </g>
  <g id="fx" opacity="0"><rect x="60" y="480" width="690" height="125" rx="20" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="22 12"/>
    <rect x="60" y="702" width="530" height="125" rx="20" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="22 12"/></g>
  <g id="fx2" opacity="0"><path d="M40 830 L-160 1000 L-120 1000 L60 846Z" fill="#b0bec5"/>""" + arrow_up(30, 380) + """</g>""")

SNOWPLOW = svg(env_snow() + """
  <g id="animal">
    <rect x="80" y="760" width="90" height="100" rx="14" fill="#607d8b"/>
    <rect x="140" y="620" width="510" height="270" rx="24" fill="#f57c00"/>
    <path d="M160 650 L620 650" stroke="#ef6c00" stroke-width="12"/>
    <path d="M170 620 Q300 580 420 610 Q520 580 630 620Z" fill="#fff"/>
    """ + cab(640, 590, 240, 310, "#ff8f00") + """
    <rect x="720" y="566" width="80" height="26" rx="10" fill="#ffb300"/>
    <rect x="875" y="850" width="80" height="40" rx="8" fill="#455a64"/>
    <path d="M945 740 Q1010 870 965 1000 L1050 1000 Q1085 870 1015 740Z" fill="#fdd835" stroke="#f9a825" stroke-width="6"/>
    """ + wheel(250) + wheel(450) + wheel(770) + """
  </g>
  <g id="fx" opacity="0"><path d="M1000 1000 Q1020 900 1080 880 Q1150 870 1180 1000Z" fill="#fff"/><path d="M1040 1000 Q1070 940 1120 940 Q1150 960 1150 1000Z" fill="#e3f2fd"/></g>
  <g id="fx2" opacity="0"><g fill="#fff">""" + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((60, 880, 7), (40, 920, 6), (90, 940, 8), (30, 970, 6), (110, 900, 5), (70, 990, 7), (120, 970, 6))) + """</g>
    <g fill="#b3e5fc">""" + "".join(f'<circle cx="{x}" cy="{y}" r="5"/>' for x, y in ((50, 900), (80, 960), (100, 925), (20, 945))) + """</g></g>""")

LOADER = svg(env() + """
  <g id="animal">
    <path d="M320 730 L190 520" stroke="#f9a825" stroke-width="36" stroke-linecap="round"/>
    <path d="M190 520 L110 700" stroke="#fbc02d" stroke-width="30" stroke-linecap="round"/>
    <path d="M80 690 L150 700 L140 780 Q90 790 70 740Z" fill="#78909c"/>
    <circle cx="190" cy="520" r="20" fill="#455a64"/>
    <rect x="290" y="700" width="440" height="170" rx="26" fill="#fbc02d"/>
    """ + cab(370, 470, 270, 260, "#fdd835") + """
    <path d="M650 760 L880 830" stroke="#f9a825" stroke-width="30" stroke-linecap="round"/>
    <path d="M870 760 L1010 760 L1020 900 L860 900 Q840 830 870 760Z" fill="#f9a825" stroke="#f57f17" stroke-width="6"/>
    """ + wheel(390, 918, 82) + wheel(690, 940, 60) + """
  </g>
  <g id="fx" opacity="0"><rect x="830" y="730" width="220" height="200" rx="20" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="22 12"/></g>
  <g id="fx2" opacity="0"><path d="M320 730 L190 520 L110 700" stroke="#ffeb3b" stroke-width="12" fill="none" stroke-dasharray="22 12"/><circle cx="110" cy="740" r="70" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="18 10"/></g>""")

BOAT = svg(env_water() + """
  <g id="animal">
    <rect x="600" y="470" width="14" height="80" fill="#90a4ae"/><circle cx="607" cy="462" r="16" fill="#ffb300"/>
    """ + cab(450, 540, 330, 260, "#fafafa") + """
    <path d="M110 780 L990 780 Q960 900 840 930 L230 930 Q150 880 110 780Z" fill="#ff7043"/>
    <path d="M128 820 L975 820" stroke="#ffffff" stroke-width="18"/>
    <path d="M120 780 L990 780" stroke="#e64a19" stroke-width="10"/>
    <circle cx="300" cy="700" r="48" fill="none" stroke="#ffffff" stroke-width="24"/>
    <circle cx="300" cy="700" r="48" fill="none" stroke="#ef5350" stroke-width="24" stroke-dasharray="37.7 37.7"/>
    <g stroke="#cfd8dc" stroke-width="8"><line x1="150" y1="780" x2="150" y2="640"/><line x1="150" y1="650" x2="430" y2="650"/></g>
  </g>
  """ + env_water_front() + """
  <g id="fx" opacity="0" stroke="#ffffff" stroke-width="12" fill="none" stroke-linecap="round"><path d="M100 910 Q40 880 -20 900"/><path d="M90 950 Q20 930 -40 960"/><path d="M60 990 Q0 975 -40 1000"/></g>
  <g id="fx2" opacity="0"><circle cx="300" cy="700" r="85" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="18 10"/></g>""")

TUG = svg(env_airport() + """
  <g id="animal">
    <path d="M520 690 Q520 560 700 540 L1700 540 L1700 830 L700 830 Q540 820 520 690Z" fill="#fafafa" stroke="#cfd8dc" stroke-width="6"/>
    <rect x="560" y="740" width="1140" height="22" fill="#1e88e5"/>
    <path d="M572 640 Q590 600 650 592 L740 592 L740 660 L585 660Z" fill="#4fc3f7"/>
    """ + face(668, 625, .6, False) + """
    <path d="M610 700 q24 16 48 0" stroke="#263238" stroke-width="7" fill="none" stroke-linecap="round"/>
    <g fill="#bde9ff">""" + "".join(f'<circle cx="{x}" cy="640" r="18"/>' for x in range(820, 1700, 70)) + """</g>
    <path d="M900 780 L1100 780 L1260 920 L1160 920Z" fill="#e0e0e0" stroke="#b0bec5" stroke-width="5"/>
    <ellipse cx="1030" cy="860" rx="80" ry="42" fill="#b0bec5"/><ellipse cx="960" cy="860" rx="16" ry="34" fill="#78909c"/>
    <rect x="612" y="820" width="20" height="120" fill="#78909c"/>
    """ + wheel(622, 962, 38) + """
    <rect x="420" y="930" width="200" height="16" rx="8" fill="#455a64"/>
    <rect x="70" y="850" width="380" height="110" rx="34" fill="#fdd835"/>
    """ + cab(150, 690, 230, 210, "#ffca28") + """
    <rect x="70" y="900" width="380" height="18" fill="#263238" opacity=".8"/>
    """ + wheel(150, 960, 40) + wheel(370, 960, 40) + """
  </g>
  <g id="fx" opacity="0">""" + arrow_right(780, 470) + arrow_right(960, 470) + """</g>
  <g id="fx2" opacity="0"><rect x="405" y="905" width="240" height="66" rx="20" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="18 10"/></g>""")

RACECAR = svg(env() + """
  <g id="animal">
    <rect x="140" y="660" width="20" height="90" fill="#455a64"/><rect x="100" y="650" width="170" height="30" rx="10" fill="#1565c0"/>
    <path d="M120 890 L150 780 L470 770 L560 690 L720 690 L780 780 L990 830 Q1020 850 1010 900 L120 900Z" fill="#1e88e5"/>
    <path d="M580 705 L700 705 L740 775 L560 775Z" fill="#bde9ff"/>
    """ + face(650, 740, .55, False) + """
    <path d="M840 860 q24 16 48 0" stroke="#263238" stroke-width="7" fill="none" stroke-linecap="round"/>
    <path d="M150 840 L1000 840" stroke="#fff" stroke-width="14"/>
    <circle cx="420" cy="830" r="42" fill="#fff"/><path d="M420 800 l10 20 22 3 -16 15 4 22 -20 -10 -20 10 4 -22 -16 -15 22 -3z" fill="#e53935"/>
    <rect x="930" y="890" width="130" height="18" rx="8" fill="#1565c0"/>
    <circle cx="1000" cy="870" r="12" fill="#fff59d"/>
    """ + wheel(260, 920, 80) + wheel(830, 920, 80) + """
  </g>
  <g id="fx" opacity="0" stroke="#ffffff" stroke-width="12" stroke-linecap="round"><line x1="-40" y1="740" x2="80" y2="740"/><line x1="-80" y1="800" x2="90" y2="800"/><line x1="-30" y1="860" x2="70" y2="860"/><line x1="-60" y1="920" x2="60" y2="920"/></g>
  <g id="fx2" opacity="0"><rect x="985" y="190" width="14" height="330" fill="#455a64"/>""" + "".join(
        f'<rect x="{825+i*40}" y="{200+j*40}" width="40" height="40" fill="{"#263238" if (i+j)%2 else "#ffffff"}"/>' for i in range(4) for j in range(3)) + """</g>""")

CAMPER = svg(env() + """
  <g id="animal">
    <rect x="130" y="570" width="780" height="330" rx="70" fill="#80cbc4"/>
    <path d="M130 700 L130 640 Q130 570 200 570 L840 570 Q910 570 910 640 L910 700Z" fill="#fff8e1"/>
    <g fill="#bde9ff"><rect x="190" y="600" width="130" height="80" rx="16"/><rect x="345" y="600" width="130" height="80" rx="16"/><rect x="500" y="600" width="130" height="80" rx="16"/></g>
    <g fill="#ffab91"><rect x="190" y="600" width="30" height="80" rx="8"/><rect x="290" y="600" width="30" height="80" rx="8"/></g>
    <rect x="360" y="720" width="120" height="150" rx="12" fill="none" stroke="#4db6ac" stroke-width="8"/>
    <rect x="160" y="540" width="600" height="20" rx="10" fill="#8d6e63"/>
    <rect x="690" y="600" width="190" height="110" rx="22" fill="#bde9ff"/>
    """ + face(785, 650, .9, False) + """
    <path d="M755 760 q30 22 60 0" stroke="#263238" stroke-width="8" fill="none" stroke-linecap="round"/>
    <ellipse cx="720" cy="750" rx="18" ry="10" fill="#ff8fab" opacity=".6"/><ellipse cx="850" cy="750" rx="18" ry="10" fill="#ff8fab" opacity=".6"/>
    <circle cx="895" cy="830" r="18" fill="#fff59d" stroke="#f9a825" stroke-width="4"/>
    """ + wheel(290) + wheel(760) + """
  </g>
  <g id="fx" opacity="0"><path d="M200 545 L270 420 L760 420 L820 545Z" fill="#ffb74d" stroke="#fb8c00" stroke-width="6"/><rect x="380" y="455" width="160" height="60" rx="12" fill="#fff3e0"/></g>
  <g id="fx2" opacity="0"><circle cx="980" cy="160" r="60" fill="#fff59d"/><circle cx="1005" cy="140" r="52" fill="#7fd3ff"/>""" + sparkle(120, 330, .5) + sparkle(560, 260, .4) + sparkle(900, 360, .45) + """
    <g fill="#ffe082" opacity=".75"><rect x="190" y="600" width="130" height="80" rx="16"/><rect x="345" y="600" width="130" height="80" rx="16"/><rect x="500" y="600" width="130" height="80" rx="16"/></g></g>""")


def bwheel(cx, cy=860, r=140):
    spokes = "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx+r*math.cos(a):.0f}" y2="{cy+r*math.sin(a):.0f}" stroke="#b0bec5" stroke-width="5"/>' for a in [i * 0.3927 for i in range(16)])
    return spokes + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#263238" stroke-width="24"/><circle cx="{cx}" cy="{cy}" r="20" fill="#607d8b"/>'


BIKE = svg(env() + """
  <g id="animal">
    """ + bwheel(290) + bwheel(790) + """
    <path d="M290 860 L480 860 L780 860" stroke="none"/>
    <path d="M300 860 L480 860" stroke="#90a4ae" stroke-width="10"/>
    <g stroke="#e53935" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" fill="none">
      <path d="M290 860 L480 860 L420 640"/><path d="M290 860 L420 640 L700 650 L480 860"/><path d="M700 650 L790 860"/><path d="M700 650 L680 560"/></g>
    <path d="M640 560 L720 560" stroke="#455a64" stroke-width="18" stroke-linecap="round"/>
    <circle cx="640" cy="548" r="16" fill="#fdd835" stroke="#f9a825" stroke-width="4"/>
    <ellipse cx="410" cy="618" rx="70" ry="22" fill="#37474f"/>
    <circle cx="480" cy="860" r="34" fill="#546e7a"/><rect x="490" y="876" width="60" height="18" rx="6" fill="#263238"/>
    <rect x="730" y="560" width="190" height="130" rx="24" fill="#ffca28" stroke="#f9a825" stroke-width="6"/>
    <path d="M745 620 L905 620 M745 655 L905 655" stroke="#f9a825" stroke-width="5"/>
    """ + face(825, 605, .7, True) + """
  </g>
  <g id="fx" opacity="0"><path d="M400 860 A80 80 0 1 1 480 940" stroke="#ffeb3b" stroke-width="12" fill="none" stroke-dasharray="20 12"/><path d="M470 920 l20 22 -28 10" stroke="#ffeb3b" stroke-width="12" fill="none" stroke-linecap="round"/></g>
  <g id="fx2" opacity="0" stroke="#ffeb3b" stroke-width="10" fill="none" stroke-linecap="round"><path d="M600 520 q-20 -20 0 -50"/><path d="M570 540 q-36 -36 0 -90"/><path d="M680 520 q20 -20 0 -50"/><path d="M710 540 q36 -36 0 -90"/></g>""")

HELI = svg(env() + """
  <g id="animal">
    <path d="M400 680 L130 650 L130 700 L400 760Z" fill="#ffa000"/>
    <path d="M110 580 L170 580 L180 700 L130 700Z" fill="#ff8f00"/>
    <circle cx="140" cy="630" r="54" fill="none" stroke="#455a64" stroke-width="10"/><circle cx="140" cy="630" r="10" fill="#455a64"/>
    <g stroke="#546e7a" stroke-width="14" stroke-linecap="round"><line x1="430" y1="880" x2="400" y2="950"/><line x1="770" y1="880" x2="800" y2="950"/><line x1="340" y1="955" x2="860" y2="955"/></g>
    <ellipse cx="600" cy="720" rx="280" ry="180" fill="#ffb300"/>
    <path d="M640 570 Q860 570 880 720 L640 720Z" fill="#bde9ff"/>
    """ + face(760, 650, .8, False) + """
    <path d="M730 770 q30 22 60 0" stroke="#263238" stroke-width="8" fill="none" stroke-linecap="round"/>
    <ellipse cx="690" cy="760" rx="18" ry="10" fill="#ff8fab" opacity=".6"/><ellipse cx="830" cy="760" rx="18" ry="10" fill="#ff8fab" opacity=".6"/>
    <rect x="585" y="500" width="30" height="50" fill="#455a64"/>
    <rect x="200" y="488" width="800" height="22" rx="11" fill="#455a64"/><circle cx="600" cy="499" r="20" fill="#37474f"/>
    <circle cx="860" cy="800" r="14" fill="#fff59d"/>
  </g>
  <g id="fx" opacity="0"><ellipse cx="600" cy="499" rx="460" ry="40" fill="#ffffff" opacity=".55"/><path d="M200 450 Q600 380 1000 450" stroke="#ffeb3b" stroke-width="10" fill="none" stroke-dasharray="22 12"/></g>
  <g id="fx2" opacity="0"><circle cx="140" cy="630" r="80" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="18 10"/>""" + arrow_up(960, 600) + """</g>""")

ROCKET = svg(env() + """
  <g id="animal">
    <rect x="40" y="760" width="720" height="40" rx="10" fill="#546e7a"/>
    <rect x="40" y="800" width="720" height="60" rx="10" fill="#455a64"/>
    <g fill="#78909c"><rect x="200" y="740" width="30" height="30"/><rect x="460" y="740" width="30" height="30"/></g>
    <path d="M60 680 Q90 610 190 610 L620 610 L620 750 L190 750 Q90 750 60 680Z" fill="#fafafa" stroke="#cfd8dc" stroke-width="6"/>
    <rect x="300" y="612" width="30" height="136" fill="#e53935"/><rect x="520" y="612" width="30" height="136" fill="#e53935"/>
    <circle cx="210" cy="680" r="34" fill="#4fc3f7" stroke="#90a4ae" stroke-width="8"/>
    <path d="M580 610 L680 560 L680 610Z" fill="#e53935"/><path d="M580 750 L680 800 L680 750Z" fill="#e53935"/>
    <path d="M620 630 L680 610 L680 750 L620 730Z" fill="#90a4ae"/>
    """ + cab(730, 590, 230, 310, "#1e88e5") + wheel(130, 920, 70) + wheel(290, 920, 70) + wheel(560, 920, 70) + wheel(840) + """
  </g>
  <g id="fx" opacity="0"><g transform="translate(985 950) scale(.6)"><ellipse cx="0" cy="60" rx="70" ry="40" fill="#66bb6a"/><path d="M-60 60 Q0 -10 60 60Z" fill="#43a047"/>
    <circle cx="80" cy="60" r="22" fill="#81c784"/><circle cx="88" cy="54" r="5" fill="#1a1a2e"/><rect x="-50" y="85" width="20" height="18" rx="8" fill="#81c784"/><rect x="30" y="85" width="20" height="18" rx="8" fill="#81c784"/></g></g>
  <g id="fx2" opacity="0"><path d="M60 680 Q90 610 190 610 L620 610 L620 750 L190 750 Q90 750 60 680Z" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="22 12"/>""" + sparkle(120, 540, .5) + sparkle(420, 520, .6) + sparkle(640, 470, .45) + """</g>""")

RECYCLE = svg(env() + """
  <g id="animal">
    <rect x="120" y="580" width="590" height="320" rx="26" fill="#1e88e5"/>
    <rect x="150" y="620" width="160" height="170" rx="16" fill="#90caf9"/>
    <rect x="335" y="620" width="160" height="170" rx="16" fill="#cfd8dc"/>
    <rect x="520" y="620" width="160" height="170" rx="16" fill="#a5d6a7"/>
    <g><rect x="190" y="660" width="80" height="96" rx="6" fill="#fff"/><path d="M202 680 h56 M202 700 h56 M202 720 h40" stroke="#90a4ae" stroke-width="6"/></g>
    <g><rect x="380" y="660" width="70" height="100" rx="12" fill="#90a4ae"/><rect x="380" y="672" width="70" height="14" fill="#b0bec5"/><rect x="380" y="734" width="70" height="14" fill="#b0bec5"/></g>
    <g><path d="M585 650 h30 v24 q20 14 20 40 v50 q0 10 -10 10 h-50 q-10 0 -10 -10 v-50 q0 -26 20 -40z" fill="#66bb6a"/></g>
    <g stroke="#43a047" stroke-width="12" fill="none" stroke-linecap="round"><path d="M260 850 A40 40 0 0 1 330 830"/><path d="M340 870 A40 40 0 0 1 280 890"/></g>
    """ + cab(700, 600, 240, 300, "#42a5f5") + wheel(250) + wheel(430) + wheel(830) + """
  </g>
  <g id="fx" opacity="0">
    <g transform="translate(220 420) rotate(-15)"><rect x="0" y="0" width="60" height="72" rx="6" fill="#fff" stroke="#90a4ae" stroke-width="4"/></g>
    <g transform="translate(400 380) rotate(10)"><rect x="0" y="0" width="50" height="76" rx="10" fill="#90a4ae"/></g>
    <g transform="translate(580 420) rotate(-8)"><path d="M10 0 h24 v18 q16 12 16 32 v40 h-56 v-40 q0 -20 16 -32z" fill="#66bb6a"/></g>
    <path d="M250 510 L260 570 M430 480 L420 570 M610 520 L600 570" stroke="#ffeb3b" stroke-width="10" stroke-linecap="round" stroke-dasharray="14 10"/></g>
  <g id="fx2" opacity="0"><circle cx="415" cy="420" r="110" fill="none" stroke="#43a047" stroke-width="16" stroke-dasharray="150 80"/>
    <path d="M520 360 l12 34 -36 0z M330 340 l36 -6 -14 30z M380 530 l-30 -20 32 -12z" fill="#43a047"/></g>""")

# ---------------------------------------------------------------- places
CARWASH = svg(env() + """
  <g id="animal">
    <rect x="60" y="360" width="960" height="640" rx="20" fill="#b2ebf2"/>
    <rect x="60" y="360" width="90" height="640" rx="16" fill="#00acc1"/><rect x="930" y="360" width="90" height="640" rx="16" fill="#00acc1"/>
    <rect x="40" y="340" width="1000" height="100" rx="30" fill="#00acc1"/>
    <path d="M540 350 Q575 395 575 412 A35 35 0 0 1 505 412 Q505 395 540 350Z" fill="#fff"/>
    <g><rect x="170" y="470" width="90" height="480" rx="45" fill="#f06292"/>""" + "".join(f'<path d="M175 {y} L255 {y+30}" stroke="#ec407a" stroke-width="10"/>' for y in range(490, 930, 50)) + """</g>
    <g><rect x="820" y="470" width="90" height="480" rx="45" fill="#f06292"/>""" + "".join(f'<path d="M825 {y} L905 {y+30}" stroke="#ec407a" stroke-width="10"/>' for y in range(490, 930, 50)) + """</g>
    <rect x="270" y="460" width="540" height="70" rx="35" fill="#ba68c8"/>""" + "".join(f'<path d="M{x} 465 L{x+30} 525" stroke="#ab47bc" stroke-width="10"/>' for x in range(290, 790, 50)) + """
    """ + smallcar(300, 707, "#ffb300", 1.25) + """
    <g fill="#fff" stroke="#81d4fa" stroke-width="4"><circle cx="330" cy="700" r="22"/><circle cx="760" cy="690" r="18"/></g>
  </g>
  <g id="fx" opacity="0"><g fill="#ffffff" stroke="#81d4fa" stroke-width="5" opacity=".95">""" + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
        ((360, 640, 30), (420, 600, 22), (500, 620, 34), (580, 590, 26), (650, 630, 30), (720, 610, 22), (460, 680, 18), (690, 690, 20),
         (300, 760, 24), (780, 760, 26), (540, 560, 18))) + """</g></g>
  <g id="fx2" opacity="0" stroke="#4fc3f7" stroke-width="10" stroke-linecap="round" stroke-dasharray="20 18">""" + "".join(
        f'<line x1="{x}" y1="540" x2="{x}" y2="720"/>' for x in range(320, 800, 60)) + """</g>""")

GASSTATION = svg(env() + """
  <g id="animal">
    <rect x="100" y="360" width="40" height="640" fill="#b0bec5"/><rect x="960" y="360" width="40" height="640" fill="#b0bec5"/>
    <rect x="60" y="300" width="980" height="80" rx="22" fill="#e53935"/><rect x="60" y="350" width="980" height="16" fill="#fff"/>
    <rect x="160" y="960" width="240" height="40" rx="8" fill="#cfd8dc"/>
    <rect x="180" y="600" width="200" height="370" rx="30" fill="#43a047"/>
    <rect x="205" y="635" width="150" height="110" rx="18" fill="#bde9ff"/>
    """ + face(280, 685, .65, False) + """
    <path d="M255 790 q25 18 50 0" stroke="#263238" stroke-width="7" fill="none" stroke-linecap="round"/>
    <ellipse cx="220" cy="790" rx="14" ry="8" fill="#ff8fab" opacity=".6"/><ellipse cx="340" cy="790" rx="14" ry="8" fill="#ff8fab" opacity=".6"/>
    <rect x="370" y="760" width="30" height="70" rx="8" fill="#2e7d32"/>
    """ + smallcar(440, 732, "#7e57c2", 1.15) + """
    <path d="M395 800 Q430 930 490 880" stroke="#263238" stroke-width="14" fill="none" stroke-linecap="round"/>
    <rect x="478" y="860" width="34" height="24" rx="6" fill="#37474f"/>
  </g>
  <g id="fx" opacity="0"><g fill="#ffca28">""" + "".join(f'<path d="M{x} {y} q12 20 12 28 a12 12 0 0 1 -24 0 q0 -8 12 -28z"/>' for x, y in ((420, 850), (450, 900), (480, 830))) + """</g>""" + sparkle(560, 820, .5) + """</g>
  <g id="fx2" opacity="0"><rect x="895" y="760" width="60" height="240" rx="14" fill="#29b6f6"/><path d="M930 800 l-18 34 h16 l-12 30 30 -40 h-16 l12 -24z" fill="#fff59d"/>
    <circle cx="925" cy="830" r="70" fill="#4fc3f7" opacity=".3"/></g>""")

GARAGE = svg(env() + """
  <g id="animal">
    <rect x="40" y="380" width="1000" height="620" fill="#ffcc80"/>
    <rect x="20" y="330" width="1040" height="80" rx="18" fill="#8d6e63"/>
    <rect x="140" y="460" width="800" height="540" fill="#fff3e0"/>
    <rect x="140" y="460" width="800" height="56" fill="#bcaaa4"/><path d="M140 478 H940 M140 498 H940" stroke="#a1887f" stroke-width="5"/>
    <g fill="#90a4ae"><rect x="170" y="545" width="16" height="70" rx="6"/><circle cx="178" cy="545" r="18" fill="none" stroke="#90a4ae" stroke-width="10"/>
      <rect x="215" y="550" width="16" height="70" rx="6"/><rect x="200" y="545" width="46" height="22" rx="6" fill="#8d6e63"/></g>
    <rect x="230" y="520" width="40" height="480" rx="10" fill="#ef5350"/><rect x="850" y="520" width="40" height="480" rx="10" fill="#ef5350"/>
    <rect x="230" y="815" width="660" height="22" rx="8" fill="#c62828"/>
    """ + smallcar(310, 572, "#26a69a", 1.3) + """
    <rect x="150" y="890" width="70" height="110" rx="8" fill="#e53935"/><path d="M150 930 h70 M150 965 h70" stroke="#b71c1c" stroke-width="5"/>
  </g>
  <g id="fx" opacity="0">""" + sparkle(330, 600, .7) + sparkle(800, 560, .6) + sparkle(560, 520, .5) + """
    <g transform="translate(980 600) rotate(30)"><rect x="-10" y="0" width="20" height="120" rx="8" fill="#ffeb3b"/><circle cx="0" cy="0" r="26" fill="none" stroke="#ffeb3b" stroke-width="14"/></g></g>
  <g id="fx2" opacity="0">""" + arrow_up(190, 700) + arrow_up(930, 700) + """</g>""")

TRAFFICLIGHT = svg(env() + """
  <g id="animal">
    <rect x="515" y="740" width="50" height="260" fill="#546e7a"/>
    <rect x="400" y="110" width="280" height="660" rx="60" fill="#37474f"/>
    """ + face(540, 190, .75, False) + """
    <g fill="#263238"><path d="M460 290 h160 l-20 -30 h-120z"/><path d="M460 440 h160 l-20 -30 h-120z"/><path d="M460 590 h160 l-20 -30 h-120z"/></g>
    <circle cx="540" cy="340" r="58" fill="#a33b3b"/><circle cx="540" cy="490" r="58" fill="#b8962e"/><circle cx="540" cy="640" r="58" fill="#3b8a4b"/>
    <path d="M510 715 q30 22 60 0" stroke="#fff59d" stroke-width="8" fill="none" stroke-linecap="round"/>
    <ellipse cx="460" cy="230" rx="16" ry="9" fill="#ff8fab" opacity=".6"/><ellipse cx="620" cy="230" rx="16" ry="9" fill="#ff8fab" opacity=".6"/>
  </g>
  <g id="fx" opacity="0"><circle cx="540" cy="340" r="110" fill="#ff5252" opacity=".3"/><circle cx="540" cy="340" r="58" fill="#ff1744"/><circle cx="522" cy="322" r="16" fill="#fff" opacity=".6"/></g>
  <g id="fx2" opacity="0"><circle cx="540" cy="640" r="110" fill="#69f0ae" opacity=".3"/><circle cx="540" cy="640" r="58" fill="#00e676"/><circle cx="522" cy="622" r="16" fill="#fff" opacity=".6"/></g>""")

SCENES_TRUCK2 = {
    "tt2_towtruck": TOWTRUCK, "tt2_sweeper": SWEEPER, "tt2_forklift": FORKLIFT, "tt2_roller": ROLLER,
    "tt2_cherrypicker": CHERRYPICKER, "tt2_monster": MONSTER, "tt2_icecream": ICECREAM, "tt2_mail": MAIL,
    "tt2_van": VAN, "tt2_tanker": TANKER, "tt2_carcarrier": CARCARRIER, "tt2_snowplow": SNOWPLOW,
    "tt2_loader": LOADER, "tt2_boat": BOAT, "tt2_tug": TUG, "tt2_racecar": RACECAR, "tt2_camper": CAMPER,
    "tt2_bike": BIKE, "tt2_heli": HELI, "tt2_rocket": ROCKET, "tt2_recycle": RECYCLE,
    "tt2_carwash": CARWASH, "tt2_gasstation": GASSTATION, "tt2_garage": GARAGE, "tt2_trafficlight": TRAFFICLIGHT,
}
NAMES_TRUCK2 = {
    "tt2_towtruck": "TOW TRUCK", "tt2_sweeper": "STREET SWEEPER", "tt2_forklift": "FORKLIFT", "tt2_roller": "ROAD ROLLER",
    "tt2_cherrypicker": "CHERRY PICKER", "tt2_monster": "MONSTER TRUCK", "tt2_icecream": "ICE CREAM TRUCK", "tt2_mail": "MAIL TRUCK",
    "tt2_van": "DELIVERY VAN", "tt2_tanker": "TANKER TRUCK", "tt2_carcarrier": "CAR CARRIER", "tt2_snowplow": "SNOWPLOW",
    "tt2_loader": "BACKHOE LOADER", "tt2_boat": "RESCUE BOAT", "tt2_tug": "AIRPLANE TUG", "tt2_racecar": "RACE CAR",
    "tt2_camper": "CAMPER VAN", "tt2_bike": "BICYCLE", "tt2_heli": "HELICOPTER", "tt2_rocket": "ROCKET MOVER",
    "tt2_recycle": "RECYCLING TRUCK", "tt2_carwash": "CAR WASH", "tt2_gasstation": "GAS STATION", "tt2_garage": "GARAGE",
    "tt2_trafficlight": "TRAFFIC LIGHT",
}
