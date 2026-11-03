"""Original art for WildKids Discovery: friendly backyard bugs and tiny critters, close-up, in the 1080x1100 frame."""
import math

def svg(body):
    return f'<svg viewBox="0 0 1080 1100" width="1080" height="1100">{body}</svg>'

def flower(x, y, c, s=1.0):
    pet = "".join(f'<circle cx="{x + 34*s*math.cos(a):.0f}" cy="{y + 34*s*math.sin(a):.0f}" r="{24*s:.0f}" fill="{c}"/>' for a in [i*1.2566 for i in range(5)])
    return f'<rect x="{x-5}" y="{y}" width="10" height="{int(950-y+60)}" fill="#558b2f"/>{pet}<circle cx="{x}" cy="{y}" r="{20*s:.0f}" fill="#ffd54f"/>'

def garden_env():
    blades = "".join(f'<path d="M{x} 1000 q{(-1)**i*18} -{90 + (i*37) % 80} {(-1)**i*8} -{150 + (i*53) % 110}" stroke="#66bb6a" stroke-width="14" fill="none" stroke-linecap="round"/>'
                     for i, x in enumerate(range(-480, 1600, 55)))
    return ("""
  <circle cx="170" cy="150" r="85" fill="#ffe066"/>
  <g id="cloud1" opacity=".95"><ellipse cx="760" cy="140" rx="110" ry="42" fill="#fff"/><ellipse cx="700" cy="120" rx="60" ry="45" fill="#fff"/><ellipse cx="820" cy="118" rx="55" ry="40" fill="#fff"/></g>
  <g fill="#a5d6a7" opacity=".8"><circle cx="-320" cy="760" r="200"/><circle cx="-120" cy="830" r="150"/><circle cx="1300" cy="760" r="200"/><circle cx="1480" cy="840" r="150"/></g>"""
            + flower(-250, 640, "#f48fb1") + flower(-40, 760, "#ce93d8", .8) + flower(1180, 660, "#90caf9") + flower(1400, 760, "#f48fb1", .8) + """
  <path d="M-500 940 Q-200 900 100 940 T700 935 T1300 940 T1700 930 L1700 1100 L-500 1100Z" fill="#7cb342"/>
  <path d="M-500 1010 Q-200 985 100 1010 T700 1005 T1300 1010 T1700 1005 L1700 1100 L-500 1100Z" fill="#558b2f"/>
  <g>""" + blades + "</g>")

def eye(cx, cy, r=30):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/><circle cx="{cx+5}" cy="{cy+3}" r="{int(r*.52)}" fill="#1a1a2e"/>'
            f'<circle cx="{cx+10}" cy="{cy-4}" r="5" fill="#fff"/>')

def smile(cx, cy, w=36, c="#3e2723"):
    return f'<path d="M{cx-w} {cy} q{w} {w*.8:.0f} {2*w} 0" stroke="{c}" stroke-width="9" fill="none" stroke-linecap="round"/>'

def blush(cx, cy):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="22" ry="12" fill="#ff8fab" opacity=".65"/>'

LEAF = '<path d="M90 960 Q300 700 640 760 Q900 800 1010 960 Q600 1040 90 960Z" fill="#43a047"/><path d="M140 955 Q560 850 980 955" stroke="#2e7d32" stroke-width="10" fill="none"/>'

LADYBUG = svg(garden_env() + LEAF + """
  <g id="animal">
    <g stroke="#263238" stroke-width="16" stroke-linecap="round"><line x1="370" y1="760" x2="270" y2="900"/><line x1="360" y1="680" x2="230" y2="760"/><line x1="710" y1="760" x2="810" y2="900"/><line x1="720" y1="680" x2="850" y2="760"/></g>
    <ellipse cx="540" cy="720" rx="250" ry="210" fill="#e53935"/>
    <path d="M540 520 L540 930" stroke="#263238" stroke-width="10"/>
    <g fill="#263238"><circle cx="430" cy="640" r="44"/><circle cx="650" cy="640" r="44"/><circle cx="400" cy="790" r="38"/><circle cx="680" cy="790" r="38"/><circle cx="500" cy="880" r="26"/><circle cx="580" cy="880" r="26"/></g>
    <ellipse cx="460" cy="590" rx="60" ry="26" fill="#fff" opacity=".35" transform="rotate(-25 460 590)"/>
    <path d="M420 430 Q380 340 330 320" stroke="#263238" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="328" cy="318" r="16" fill="#263238"/>
    <path d="M660 430 Q700 340 750 320" stroke="#263238" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="752" cy="318" r="16" fill="#263238"/>
    <ellipse cx="540" cy="500" rx="150" ry="110" fill="#37474f"/>
    """ + eye(490, 480, 34) + eye(590, 480, 34) + smile(540, 540, 30, "#fff") + blush(440, 535) + blush(640, 535) + """
  </g>
  <g id="fx" opacity="0" fill="none" stroke="#ffeb3b" stroke-width="12" stroke-dasharray="26 16"><ellipse cx="540" cy="690" rx="320" ry="300"/><ellipse cx="540" cy="690" rx="380" ry="360" opacity=".6"/></g>
  <g id="fx2" opacity="0"><g transform="translate(860 300)"><path d="M0 40 q30 -40 60 0 q30 -40 60 0" stroke="#37474f" stroke-width="10" fill="none" stroke-linecap="round"/></g></g>""")

BEE = svg(garden_env() + flower(540, 900, "#f48fb1", 1.6) + """
  <defs><clipPath id="beeclip"><ellipse cx="500" cy="600" rx="230" ry="160"/></clipPath></defs>
  <g id="animal">
    <g id="bwings" fill="#e3f2fd" stroke="#90caf9" stroke-width="6" opacity=".9"><ellipse cx="420" cy="390" rx="120" ry="170" transform="rotate(-25 420 390)"/><ellipse cx="560" cy="380" rx="100" ry="150" transform="rotate(20 560 380)"/></g>
    <path d="M280 610 l-60 -10 60 -20z" fill="#5d4037"/>
    <ellipse cx="500" cy="600" rx="230" ry="160" fill="#ffca28"/>
    <g clip-path="url(#beeclip)" fill="#3e2723"><rect x="330" y="400" width="60" height="400"/><rect x="450" y="400" width="60" height="400"/><rect x="570" y="400" width="50" height="400"/></g>
    <g stroke="#3e2723" stroke-width="12" stroke-linecap="round"><line x1="430" y1="740" x2="410" y2="820"/><line x1="520" y1="750" x2="520" y2="830"/><line x1="610" y1="740" x2="630" y2="815"/></g>
    <circle cx="760" cy="560" r="130" fill="#ffd54f"/>
    <path d="M730 440 Q700 340 650 310" stroke="#3e2723" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="648" cy="306" r="15" fill="#3e2723"/>
    <path d="M800 440 Q840 340 900 320" stroke="#3e2723" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="902" cy="318" r="15" fill="#3e2723"/>
    <g id="smalleyes" fill="#5d4037"><circle cx="735" cy="458" r="9"/><circle cx="765" cy="448" r="9"/><circle cx="795" cy="458" r="9"/></g>
    """ + eye(720, 545, 36) + eye(815, 545, 36) + smile(768, 610, 30) + blush(700, 615) + blush(840, 615) + """
  </g>
  <g id="fx" opacity="0" fill="none" stroke="#ffeb3b" stroke-width="12" stroke-linecap="round" stroke-dasharray="24 14">
    <path d="M200 260 C320 120 420 400 540 260 C660 120 760 400 880 260 C760 120 660 400 540 260 C420 120 320 400 200 260Z"/></g>
  <g id="fx2" opacity="0"><circle cx="765" cy="452" r="62" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="18 10"/></g>""")

BUTTERFLY = svg(garden_env() + """
  <defs><radialGradient id="bfw" cx="50%" cy="50%" r="70%"><stop offset="0" stop-color="#ffb74d"/><stop offset="1" stop-color="#ef6c00"/></radialGradient>
  <radialGradient id="bfw2" cx="50%" cy="50%" r="70%"><stop offset="0" stop-color="#ce93d8"/><stop offset="1" stop-color="#8e24aa"/></radialGradient></defs>
  <g id="animal">
    <g id="lwing"><path d="M520 560 Q300 200 140 330 Q60 460 240 600 Q380 650 520 600Z" fill="url(#bfw)" stroke="#4e342e" stroke-width="10"/>
      <path d="M520 640 Q300 650 230 780 Q240 900 380 860 Q500 800 520 680Z" fill="url(#bfw2)" stroke="#4e342e" stroke-width="10"/>
      <g fill="#fff"><circle cx="230" cy="420" r="28"/><circle cx="330" cy="370" r="20"/><circle cx="330" cy="790" r="22"/></g></g>
    <g id="rwing"><path d="M560 560 Q780 200 940 330 Q1020 460 840 600 Q700 650 560 600Z" fill="url(#bfw)" stroke="#4e342e" stroke-width="10"/>
      <path d="M560 640 Q780 650 850 780 Q840 900 700 860 Q580 800 560 680Z" fill="url(#bfw2)" stroke="#4e342e" stroke-width="10"/>
      <g fill="#fff"><circle cx="850" cy="420" r="28"/><circle cx="750" cy="370" r="20"/><circle cx="750" cy="790" r="22"/></g></g>
    <rect x="510" y="470" width="60" height="400" rx="30" fill="#4e342e"/>
    <g stroke="#4e342e" stroke-width="10" stroke-linecap="round"><line x1="520" y1="860" x2="490" y2="940"/><line x1="560" y1="860" x2="590" y2="940"/></g>
    <path d="M520 400 Q480 300 430 270" stroke="#4e342e" stroke-width="9" fill="none" stroke-linecap="round"/><circle cx="428" cy="266" r="14" fill="#4e342e"/>
    <path d="M560 400 Q600 300 650 270" stroke="#4e342e" stroke-width="9" fill="none" stroke-linecap="round"/><circle cx="652" cy="266" r="14" fill="#4e342e"/>
    <circle cx="540" cy="440" r="80" fill="#6d4c41"/>
    """ + eye(510, 430, 24) + eye(572, 430, 24) + smile(540, 470, 22, "#fff") + blush(485, 470) + blush(598, 470) + """
  </g>
  <g id="fx" opacity="0"><g fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="16 10"><circle cx="490" cy="945" r="40"/><circle cx="590" cy="945" r="40"/></g></g>
  <g id="fx2" opacity="0"><g transform="translate(140 930)"><circle cx="0" cy="0" r="30" fill="#8bc34a"/><circle cx="50" cy="-6" r="30" fill="#9ccc65"/><circle cx="100" cy="0" r="30" fill="#8bc34a"/><circle cx="150" cy="-6" r="34" fill="#9ccc65"/>
    <circle cx="160" cy="-14" r="6" fill="#1b1b1b"/><path d="M146 6 q12 8 24 0" stroke="#33691e" stroke-width="5" fill="none"/></g></g>""")

ANT = svg(garden_env() + """
  <g id="fx" opacity="0"><path d="M220 470 Q420 300 700 420 Q560 520 220 470Z" fill="#66bb6a" stroke="#2e7d32" stroke-width="8"/><path d="M240 466 Q460 400 690 420" stroke="#2e7d32" stroke-width="6" fill="none"/></g>
  <g id="animal">
    <g stroke="#5d2e1a" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path d="M560 690 L470 780 L430 990"/><path d="M600 700 L600 820 L560 995"/><path d="M640 690 L720 790 L760 990"/>
      <path d="M570 640 L470 560 L420 480"/></g>
    <ellipse cx="350" cy="680" rx="190" ry="140" fill="#a0522d"/>
    <ellipse cx="300" cy="640" rx="60" ry="26" fill="#fff" opacity=".25" transform="rotate(-20 300 640)"/>
    <ellipse cx="600" cy="660" rx="100" ry="72" fill="#b5653a"/>
    <path d="M820 480 Q800 360 740 320" stroke="#5d2e1a" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="738" cy="316" r="16" fill="#5d2e1a"/>
    <path d="M880 490 Q910 370 980 340" stroke="#5d2e1a" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="982" cy="338" r="16" fill="#5d2e1a"/>
    <circle cx="830" cy="600" r="125" fill="#bf6a3d"/>
    """ + eye(795, 575, 34) + eye(885, 575, 30) + smile(840, 640, 30) + blush(770, 650) + blush(910, 650) + """
  </g>
  <g id="fx2" opacity="0" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-linecap="round" stroke-dasharray="14 10"><circle cx="738" cy="316" r="40"/><circle cx="982" cy="338" r="40"/></g>""")

SNAIL = svg(garden_env() + """
  <g id="fx" opacity="0"><path d="M-480 990 Q-100 960 260 985" stroke="#e1f5fe" stroke-width="30" fill="none" stroke-linecap="round" opacity=".85"/>
    <path d="M-400 985 Q-80 965 240 982" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round"/></g>
  <g id="animal">
    <path d="M200 990 Q240 900 420 900 L760 900 Q860 900 880 760 L960 760 Q980 990 820 990Z" fill="#ffcc80"/>
    <path d="M880 780 L840 560" stroke="#ffcc80" stroke-width="30" stroke-linecap="round"/>
    <path d="M930 780 L960 540" stroke="#ffcc80" stroke-width="30" stroke-linecap="round"/>
    <circle cx="840" cy="545" r="38" fill="#ffcc80"/><circle cx="960" cy="525" r="38" fill="#ffcc80"/>
    """ + eye(840, 545, 28) + eye(960, 525, 28) + """
    <circle cx="500" cy="700" r="240" fill="#8d6e63"/>
    <path d="M500 700 m-180 0 a180 180 0 1 1 360 0 a140 140 0 1 1 -280 0 a100 100 0 1 1 200 0 a60 60 0 1 1 -120 0" stroke="#5d4037" stroke-width="22" fill="none" stroke-linecap="round"/>
    <ellipse cx="420" cy="560" rx="70" ry="30" fill="#fff" opacity=".22" transform="rotate(-30 420 560)"/>
    """ + smile(920, 870, 28) + blush(980, 850) + """
  </g>
  <g id="fx2" opacity="0" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="16 10"><circle cx="840" cy="545" r="64"/><circle cx="960" cy="525" r="64"/></g>""")

WILD_TITLE = svg(garden_env() + """
  <g transform="translate(-130 -40)">
    <rect x="130" y="230" width="820" height="150" rx="40" fill="#2e7d32" stroke="#1b5e20" stroke-width="10"/>
    <text x="540" y="332" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="78" fill="#fff">WILDKIDS DISCOVERY</text>
    <circle cx="500" cy="680" r="170" fill="#e1f5fe" stroke="#8d6e63" stroke-width="30"/>
    <path d="M620 800 L780 960" stroke="#8d6e63" stroke-width="44" stroke-linecap="round"/>
    <g transform="translate(500 690) scale(.55) translate(-540 -720)"><ellipse cx="540" cy="720" rx="250" ry="210" fill="#e53935"/>
      <path d="M540 520 L540 930" stroke="#263238" stroke-width="10"/><g fill="#263238"><circle cx="430" cy="640" r="44"/><circle cx="650" cy="640" r="44"/><circle cx="400" cy="790" r="38"/><circle cx="680" cy="790" r="38"/></g>
      <ellipse cx="540" cy="500" rx="150" ry="110" fill="#37474f"/></g>
  </g>""")

SCENES5 = {"ladybug": LADYBUG, "bee": BEE, "butterfly": BUTTERFLY, "ant": ANT, "snail": SNAIL}
NAMES5 = {"bee": "HONEYBEE"}
