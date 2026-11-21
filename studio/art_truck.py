"""Original art for Tiny Truck Town: friendly cartoon vehicles with headlight eyes, 1080x1100 frame, road at ~y1000."""

def svg(body):
    return f'<svg viewBox="0 0 1080 1100" width="1080" height="1100">{body}</svg>'

def town_env():
    blds = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{1000-y}" rx="10" fill="{c}" opacity=".55"/>'
                   + "".join(f'<rect x="{x+18+i*40}" y="{y+30+j*60}" width="22" height="30" rx="4" fill="#fff" opacity=".6"/>' for i in range(max(1, (w-30)//40)) for j in range(max(1, (1000-y-80)//60)))
                   for x, y, w, c in ((-470, 520, 180, "#9fa8da"), (-270, 600, 140, "#ffcc80"), (-110, 560, 120, "#a5d6a7"),
                                      (1110, 560, 150, "#ffab91"), (1280, 500, 190, "#9fa8da"), (1490, 620, 120, "#ffcc80")))
    return f"""
  <circle cx="170" cy="150" r="85" fill="#ffe066"/>
  <g id="cloud1" opacity=".95"><ellipse cx="760" cy="140" rx="110" ry="42" fill="#fff"/><ellipse cx="700" cy="120" rx="60" ry="45" fill="#fff"/><ellipse cx="820" cy="118" rx="55" ry="40" fill="#fff"/></g>
  <g>{blds}</g>
  <rect x="-500" y="975" width="2200" height="30" fill="#cfd8dc"/>
  <rect x="-500" y="1000" width="2200" height="120" fill="#78909c"/>
  <g fill="#ffe082">""" + "".join(f'<rect x="{x}" y="1046" width="70" height="12" rx="6"/>' for x in range(-480, 1600, 140)) + "</g>"

def wheel(x, y=940, r=62):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#263238"/><circle cx="{x}" cy="{y}" r="{int(r*.5)}" fill="#cfd8dc"/>'
            f'<circle cx="{x}" cy="{y}" r="{int(r*.18)}" fill="#607d8b"/>')

def face(cx, cy, s=1.0, smile=True):
    ex = int(42 * s)
    out = (f'<circle cx="{cx-ex}" cy="{cy}" r="{int(26*s)}" fill="#fff"/><circle cx="{cx+ex}" cy="{cy}" r="{int(26*s)}" fill="#fff"/>'
           f'<circle cx="{cx-ex+4}" cy="{cy+3}" r="{int(13*s)}" fill="#1a1a2e"/><circle cx="{cx+ex+4}" cy="{cy+3}" r="{int(13*s)}" fill="#1a1a2e"/>'
           f'<circle cx="{cx-ex+9}" cy="{cy-3}" r="5" fill="#fff"/><circle cx="{cx+ex+9}" cy="{cy-3}" r="5" fill="#fff"/>')
    if smile:
        out += f'<path d="M{cx-26*s:.0f} {cy+40*s:.0f} q{26*s:.0f} {22*s:.0f} {52*s:.0f} 0" stroke="#263238" stroke-width="7" fill="none" stroke-linecap="round"/>'
    return out

def cab(x, y, w, h, color, win="#bde9ff"):
    """Cab with a big windshield face, front facing right."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="{color}"/>'
            f'<rect x="{x+22}" y="{y+22}" width="{w-44}" height="{int(h*.45)}" rx="20" fill="{win}"/>'
            + face(x + w // 2, y + 22 + int(h * .22), 1.0, False)
            + f'<path d="M{x+w//2-30} {y+int(h*.72)} q30 22 60 0" stroke="#263238" stroke-width="8" fill="none" stroke-linecap="round"/>'
            + f'<ellipse cx="{x+w//2-62}" cy="{y+int(h*.66)}" rx="18" ry="10" fill="#ff8fab" opacity=".6"/>'
            + f'<ellipse cx="{x+w//2+62}" cy="{y+int(h*.66)}" rx="18" ry="10" fill="#ff8fab" opacity=".6"/>'
            + f'<circle cx="{x+w-12}" cy="{y+h-40}" r="16" fill="#fff59d" stroke="#f9a825" stroke-width="4"/>')

def tracks(x1, x2, y=900):
    return (f'<rect x="{x1}" y="{y}" width="{x2-x1}" height="90" rx="45" fill="#37474f"/>'
            + "".join(f'<circle cx="{cx}" cy="{y+45}" r="28" fill="#90a4ae"/>' for cx in range(x1 + 50, x2 - 30, 85)))

FIRETRUCK = svg(town_env() + """
  <g id="animal">
    <rect x="130" y="640" width="580" height="250" rx="24" fill="#e53935"/>
    <rect x="150" y="790" width="540" height="22" fill="#ffffff" opacity=".85"/>
    <g fill="#b71c1c"><rect x="180" y="680" width="90" height="80" rx="10"/><rect x="290" y="680" width="90" height="80" rx="10"/><rect x="400" y="680" width="90" height="80" rx="10"/></g>
    <circle cx="590" cy="720" r="52" fill="#fdd835" stroke="#f9a825" stroke-width="8"/><circle cx="590" cy="720" r="18" fill="#f9a825"/>
    <g id="ladder"><rect x="150" y="600" width="560" height="14" rx="7" fill="#b0bec5"/><rect x="150" y="625" width="560" height="14" rx="7" fill="#b0bec5"/>
      """ + "".join(f'<rect x="{x}" y="600" width="12" height="39" fill="#90a4ae"/>' for x in range(170, 700, 50)) + """</g>
    """ + cab(700, 600, 250, 300, "#e53935") + """
    <rect x="760" y="580" width="40" height="22" rx="8" fill="#ff5252"/><rect x="850" y="580" width="40" height="22" rx="8" fill="#448aff"/>
    """ + wheel(260) + wheel(470) + wheel(830) + """
  </g>
  <g id="fx" opacity="0"><path d="M610 700 Q760 380 1040 520" stroke="#4fc3f7" stroke-width="26" fill="none" stroke-linecap="round" stroke-dasharray="40 18"/></g>
  <g id="fx2" opacity="0"><rect x="140" y="590" width="580" height="60" rx="16" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="22 12"/></g>""")

EXCAVATOR = svg(town_env() + """
  <g id="animal">
    """ + tracks(220, 760) + """
    <rect x="330" y="840" width="380" height="60" rx="14" fill="#546e7a"/>
    <path d="M600 700 L800 430 L840 460 L660 730Z" fill="#fbc02d"/>
    <path d="M800 430 L960 560 L930 590 L790 480Z" fill="#f9a825"/>
    <path d="M930 560 L1010 640 Q960 720 880 660Z" fill="#78909c"/>
    """ + cab(360, 560, 280, 290, "#fbc02d") + """
    <rect x="250" y="700" width="110" height="140" rx="20" fill="#f9a825"/>
  </g>
  <g id="fx" opacity="0"><path d="M300 520 A250 70 0 1 0 700 520" stroke="#ffeb3b" stroke-width="12" fill="none" stroke-dasharray="26 14"/><path d="M690 500 l40 24 -46 16z" fill="#ffeb3b"/></g>
  <g id="fx2" opacity="0"><path d="M820 1000 Q900 880 1000 1000Z" fill="#8d6e63"/><path d="M860 990 Q920 920 980 990Z" fill="#a1887f"/></g>""")

BULLDOZER = svg(town_env() + """
  <g id="animal">
    """ + tracks(200, 740) + """
    <rect x="240" y="720" width="300" height="180" rx="20" fill="#fbc02d"/>
    <rect x="270" y="690" width="40" height="40" rx="8" fill="#455a64"/>
    """ + cab(480, 560, 260, 340, "#fbc02d") + """
    <path d="M760 820 L860 760 L870 790 L780 850Z" fill="#78909c"/>
    <path d="M860 640 Q900 820 870 990 L930 990 Q960 820 920 640Z" fill="#90a4ae" stroke="#607d8b" stroke-width="6"/>
  </g>
  <g id="fx" opacity="0"><path d="M940 1000 Q1010 880 1080 1000Z" fill="#8d6e63"/><path d="M960 990 Q1010 920 1060 990Z" fill="#a1887f"/></g>
  <g id="fx2" opacity="0"><rect x="850" y="630" width="90" height="370" rx="20" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="20 12"/></g>""")

DUMPTRUCK = svg(town_env() + """
  <g id="animal">
    <rect x="140" y="830" width="600" height="50" rx="12" fill="#546e7a"/>
    <g id="bed"><path d="M120 600 L700 600 L680 830 L160 830Z" fill="#fb8c00"/><path d="M150 620 L680 620" stroke="#ef6c00" stroke-width="10"/>
      <g fill="#8d6e63"><circle cx="260" cy="590" r="40"/><circle cx="340" cy="575" r="48"/><circle cx="430" cy="590" r="40"/><circle cx="520" cy="580" r="44"/><circle cx="600" cy="595" r="34"/></g></g>
    """ + cab(700, 590, 240, 310, "#fb8c00") + wheel(250) + wheel(400) + wheel(830) + """
  </g>
  <g id="fx" opacity="0"><path d="M140 540 Q400 450 690 540" stroke="#ffeb3b" stroke-width="10" fill="none" stroke-dasharray="20 12"/></g>
  <g id="fx2" opacity="0"><path d="M100 640 L140 600 L60 560" stroke="#ffeb3b" stroke-width="12" fill="none" stroke-linecap="round"/></g>""")

MIXER = svg(town_env() + """
  <defs><clipPath id="drumc"><ellipse cx="420" cy="700" rx="270" ry="150" transform="rotate(-12 420 700)"/></clipPath></defs>
  <g id="animal">
    <rect x="140" y="830" width="600" height="50" rx="12" fill="#546e7a"/>
    <ellipse cx="420" cy="700" rx="270" ry="150" transform="rotate(-12 420 700)" fill="#eceff1" stroke="#90a4ae" stroke-width="8"/>
    <g clip-path="url(#drumc)" stroke="#ef5350" stroke-width="34" fill="none"><path d="M220 500 L330 900"/><path d="M380 480 L490 880"/><path d="M540 470 L650 860"/></g>
    <rect x="600" y="780" width="110" height="60" rx="12" fill="#78909c"/>
    """ + cab(700, 590, 240, 310, "#42a5f5") + wheel(250) + wheel(420) + wheel(830) + """
  </g>
  <g id="fx" opacity="0" fill="none" stroke="#ffeb3b" stroke-width="12" stroke-linecap="round"><path d="M140 560 A300 170 0 0 1 560 470"/><path d="M560 470 l-40 -30 M560 470 l-44 22"/>
    <path d="M700 820 A300 170 0 0 1 280 900"/><path d="M280 900 l40 30 M280 900 l44 -22"/></g>
  <g id="fx2" opacity="0"><rect x="40" y="975" width="260" height="30" rx="6" fill="#bdbdbd"/></g>""")

CRANE = svg(town_env() + """
  <g id="animal">
    <rect x="160" y="800" width="560" height="90" rx="16" fill="#fbc02d"/>
    <rect x="380" y="690" width="220" height="120" rx="16" fill="#f9a825"/>
    <g id="boom"><path d="M450 720 L930 170 L965 200 L500 760Z" fill="#fdd835" stroke="#f9a825" stroke-width="6"/>
      <line x1="950" y1="190" x2="950" y2="520" stroke="#455a64" stroke-width="6"/>
      <path d="M935 520 h30 v20 q-15 30 -30 0z" fill="#607d8b"/></g>
    """ + cab(720, 600, 230, 300, "#fbc02d") + wheel(260) + wheel(420) + wheel(580) + wheel(840) + """
  </g>
  <g id="fx" opacity="0"><rect x="850" y="545" width="200" height="40" rx="6" fill="#ff7043"/><rect x="870" y="550" width="160" height="10" fill="#ffab91"/></g>
  <g id="fx2" opacity="0"><path d="M450 720 L930 170" stroke="#ffeb3b" stroke-width="12" stroke-dasharray="22 12" fill="none"/></g>""")

AMBULANCE = svg(town_env() + """
  <g id="animal">
    <rect x="130" y="580" width="600" height="320" rx="30" fill="#ffffff" stroke="#cfd8dc" stroke-width="6"/>
    <rect x="130" y="760" width="600" height="40" fill="#e53935"/>
    <path d="M430 650 c-30 -40 -90 -10 -60 40 l60 50 60 -50 c30 -50 -30 -80 -60 -40z" fill="#e53935"/>
    <rect x="170" y="620" width="120" height="90" rx="14" fill="#bde9ff"/>
    """ + cab(720, 620, 230, 280, "#ffffff") + """
    <rect x="780" y="596" width="40" height="26" rx="8" fill="#ff5252"/><rect x="860" y="596" width="40" height="26" rx="8" fill="#448aff"/>
    """ + wheel(270) + wheel(560) + wheel(830) + """
  </g>
  <g id="fx" opacity="0"><rect x="880" y="840" width="190" height="56" rx="10" fill="#fff" stroke="#e53935" stroke-width="5"/>
    <text x="975" y="882" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="36" fill="#e53935" transform="translate(1950 0) scale(-1 1)">AMBULANCE</text></g>
  <g id="fx2" opacity="0"><g fill="#fff59d" opacity=".9"><circle cx="800" cy="560" r="50"/><circle cx="880" cy="560" r="50" fill="#bbdefb"/></g></g>""")

POLICECAR = svg(town_env() + """
  <g id="animal">
    <path d="M150 900 L150 760 Q160 700 260 690 L360 690 L440 590 L700 590 L800 690 L900 700 Q950 710 950 780 L950 900Z" fill="#1e3a8a"/>
    <path d="M150 790 L950 790 L950 850 L150 850Z" fill="#ffffff"/>
    <path d="M470 610 L560 610 L560 690 L400 690Z" fill="#bde9ff"/>
    <path d="M590 610 L690 610 L780 690 L590 690Z" fill="#bde9ff"/>
    """ + face(685, 650, .75, False) + """
    <path d="M880 770 q22 14 44 0" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/>
    <circle cx="930" cy="740" r="16" fill="#fff59d"/>
    <rect x="510" y="560" width="70" height="30" rx="10" fill="#ff5252"/><rect x="590" y="560" width="70" height="30" rx="10" fill="#448aff"/>
    <path d="M400 820 l14 -28 14 28 30 4 -22 20 6 30 -28 -14 -28 14 6 -30 -22 -20z" fill="#fdd835"/>
    """ + wheel(300, 900, 66) + wheel(800, 900, 66) + """
  </g>
  <g id="fx" opacity="0"><circle cx="545" cy="560" r="70" fill="#ff5252" opacity=".35"/><circle cx="625" cy="560" r="70" fill="#448aff" opacity=".35"/></g>
  <g id="fx2" opacity="0"><circle cx="430" cy="830" r="70" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="18 10"/></g>""")

GARBAGE = svg(town_env() + """
  <g id="animal">
    <rect x="120" y="580" width="590" height="320" rx="26" fill="#43a047"/>
    <rect x="140" y="610" width="550" height="40" rx="10" fill="#2e7d32"/>
    <g id="arm"><rect x="560" y="680" width="30" height="170" rx="10" fill="#78909c"/>
      <rect x="520" y="830" width="110" height="70" rx="10" fill="#1e88e5"/><rect x="510" y="822" width="130" height="16" rx="6" fill="#1565c0"/></g>
    """ + cab(700, 600, 240, 300, "#66bb6a") + wheel(250) + wheel(430) + wheel(830) + """
  </g>
  <g id="fx" opacity="0"><g transform="translate(0 -250)"><rect x="520" y="830" width="110" height="70" rx="10" fill="#1e88e5"/><rect x="510" y="822" width="130" height="16" rx="6" fill="#1565c0"/></g>
    <path d="M575 560 L575 500" stroke="#ffeb3b" stroke-width="12" stroke-linecap="round"/><path d="M550 520 l25 -30 25 30" stroke="#ffeb3b" stroke-width="12" fill="none"/></g>
  <g id="fx2" opacity="0"><path d="M200 700 L330 700 M230 740 L300 740 M200 780 L330 780" stroke="#ffeb3b" stroke-width="10" stroke-linecap="round"/></g>""")

SCHOOLBUS = svg(town_env() + """
  <g id="animal">
    <rect x="80" y="580" width="860" height="320" rx="34" fill="#fbc02d"/>
    <rect x="80" y="790" width="860" height="22" fill="#263238"/>
    <g fill="#bde9ff">""" + "".join(f'<rect x="{x}" y="620" width="96" height="100" rx="12"/>' for x in (110, 226, 342, 458, 574)) + """</g>
    <rect x="700" y="610" width="220" height="130" rx="18" fill="#bde9ff"/>
    """ + face(810, 668, 1.0, False) + """
    <path d="M780 760 q30 22 60 0" stroke="#263238" stroke-width="8" fill="none" stroke-linecap="round"/>
    <circle cx="925" cy="850" r="16" fill="#fff59d"/>
    <g id="stoparm"><rect x="640" y="690" width="40" height="30" rx="6" fill="#263238"/></g>
    """ + wheel(240) + wheel(780) + """
  </g>
  <g id="fx" opacity="0"><rect x="600" y="690" width="60" height="16" fill="#263238"/>
    <polygon points="520,640 560,620 600,640 600,700 560,720 520,700" fill="#e53935" stroke="#fff" stroke-width="6"/>
    <text x="560" y="676" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="22" fill="#fff">STOP</text></g>
  <g id="fx2" opacity="0"><rect x="70" y="570" width="880" height="340" rx="40" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="24 14"/></g>""")

TRAIN = svg(town_env() + """
  <rect x="-500" y="990" width="2200" height="14" fill="#5d4037"/>
  <g fill="#8d6e63">""" + "".join(f'<rect x="{x}" y="985" width="16" height="30"/>' for x in range(-480, 1600, 60)) + """</g>
  <g id="animal">
    <rect x="200" y="600" width="250" height="300" rx="20" fill="#1e88e5"/>
    <rect x="230" y="630" width="190" height="120" rx="16" fill="#bde9ff"/>
    <rect x="180" y="580" width="290" height="40" rx="14" fill="#1565c0"/>
    <rect x="440" y="700" width="420" height="200" rx="100" fill="#e53935"/>
    <rect x="700" y="560" width="60" height="150" rx="12" fill="#37474f"/><rect x="680" y="540" width="100" height="30" rx="12" fill="#263238"/>
    <circle cx="860" cy="800" r="70" fill="#e53935"/>
    """ + face(790, 770, .9, False) + """
    <path d="M770 830 q24 18 48 0" stroke="#263238" stroke-width="7" fill="none" stroke-linecap="round"/>
    <path d="M900 900 L980 900 L920 840Z" fill="#78909c"/>
    """ + wheel(290, 930, 58) + wheel(520, 930, 58) + wheel(700, 930, 58) + """
    <g id="smoke" fill="#eceff1"><circle cx="730" cy="490" r="34"/><circle cx="780" cy="430" r="44"/><circle cx="850" cy="370" r="52"/></g>
  </g>
  <g id="fx" opacity="0"><rect x="-480" y="680" width="640" height="220" rx="20" fill="#fdd835"/><rect x="-170" y="680" width="20" height="220" fill="#f9a825"/>
    """ + wheel(-380, 930, 50) + wheel(-250, 930, 50) + wheel(-60, 930, 50) + wheel(70, 930, 50) + """</g>
  <g id="fx2" opacity="0"><circle cx="730" cy="480" r="120" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="18 10"/></g>""")

TRACTOR = svg(town_env() + """
  <g id="animal">
    <rect x="300" y="700" width="560" height="160" rx="30" fill="#43a047"/>
    <rect x="720" y="640" width="40" height="80" rx="10" fill="#37474f"/>
    """ + cab(300, 480, 280, 300, "#66bb6a") + """
    <circle cx="390" cy="880" r="150" fill="#263238"/><circle cx="390" cy="880" r="90" fill="#fdd835"/><circle cx="390" cy="880" r="30" fill="#f9a825"/>
    <g stroke="#37474f" stroke-width="16">""" + "".join(f'<line x1="{390+130*__import__("math").cos(a):.0f}" y1="{880+130*__import__("math").sin(a):.0f}" x2="{390+150*__import__("math").cos(a):.0f}" y2="{880+150*__import__("math").sin(a):.0f}"/>' for a in [i*0.5236 for i in range(12)]) + """</g>
    """ + wheel(800, 930, 70) + """
  </g>
  <g id="fx" opacity="0"><circle cx="390" cy="880" r="185" fill="none" stroke="#ffeb3b" stroke-width="12" stroke-dasharray="26 14"/></g>
  <g id="fx2" opacity="0"><g fill="#8d6e63"><ellipse cx="120" cy="985" rx="90" ry="20"/><ellipse cx="190" cy="1010" rx="60" ry="14"/></g>
    <path d="M60 940 l40 -20 M90 960 l50 -10" stroke="#8d6e63" stroke-width="10" stroke-linecap="round"/></g>""")

TRUCK_TITLE = svg(town_env() + """
  <g transform="translate(-130 -40)">
    <rect x="160" y="230" width="760" height="150" rx="40" fill="#e8402f" stroke="#b71c1c" stroke-width="10"/>
    <text x="540" y="332" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="86" fill="#fff">TINY TRUCK TOWN</text>
    <rect x="300" y="380" width="24" height="160" fill="#607d8b"/><rect x="756" y="380" width="24" height="160" fill="#607d8b"/>
    <g transform="translate(470 780)"><path d="M0 220 L60 0 L120 220Z" fill="#ff7043"/><rect x="18" y="120" width="84" height="30" fill="#fff"/><rect x="-20" y="210" width="160" height="30" rx="8" fill="#ff7043"/></g>
  </g>""")

SCENES6 = {"firetruck": FIRETRUCK, "excavator": EXCAVATOR, "bulldozer": BULLDOZER, "dumptruck": DUMPTRUCK, "mixer": MIXER,
           "crane": CRANE, "ambulance": AMBULANCE, "policecar": POLICECAR, "garbage": GARBAGE, "schoolbus": SCHOOLBUS,
           "train": TRAIN, "tractor": TRACTOR}
NAMES6 = {"firetruck": "FIRE TRUCK", "dumptruck": "DUMP TRUCK", "mixer": "CEMENT MIXER", "policecar": "POLICE CAR",
          "garbage": "GARBAGE TRUCK", "schoolbus": "SCHOOL BUS"}

BOLT = """<svg id="milo" viewBox="0 0 220 200" width="260" height="236">
  <g id="wing"><path d="M58 96 L22 58" stroke="#455a64" stroke-width="10" stroke-linecap="round"/><path d="M22 58 L22 118" stroke="#455a64" stroke-width="4"/>
    <path d="M14 118 h16 v8 q-8 18 -16 0z" fill="#fdd835" stroke="#f9a825" stroke-width="3"/></g>
  <rect x="40" y="110" width="150" height="50" rx="14" fill="#c62828"/>
  <rect x="70" y="40" width="120" height="110" rx="26" fill="#e53935"/>
  <rect x="84" y="54" width="92" height="56" rx="16" fill="#bde9ff"/>
  <circle cx="111" cy="80" r="14" fill="#fff"/><circle cx="149" cy="80" r="14" fill="#fff"/>
  <ellipse class="mpupil" cx="113" cy="82" rx="7" ry="9" fill="#1a1a2e"/><ellipse class="mpupil" cx="151" cy="82" rx="7" ry="9" fill="#1a1a2e"/>
  <circle class="glint" cx="116" cy="77" r="3.5" fill="#fff"/><circle class="glint" cx="154" cy="77" r="3.5" fill="#fff"/>
  <path d="M118 104 q12 8 24 0" stroke="#7a1414" stroke-width="5" fill="none" stroke-linecap="round"/>
  <ellipse id="beaklow" cx="130" cy="117" rx="9" ry="2.4" fill="#7a1414"/>
  <circle cx="100" cy="124" r="7" fill="#ff9ab0" opacity=".7"/><circle cx="162" cy="124" r="7" fill="#ff9ab0" opacity=".7"/>
  <circle cx="182" cy="138" r="8" fill="#fff59d"/>
  <circle cx="72" cy="168" r="22" fill="#263238"/><circle cx="72" cy="168" r="9" fill="#cfd8dc"/>
  <circle cx="160" cy="168" r="22" fill="#263238"/><circle cx="160" cy="168" r="9" fill="#cfd8dc"/>
</svg>"""
