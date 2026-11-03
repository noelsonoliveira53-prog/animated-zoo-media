"""Original art for Dino World Kids: friendly cartoon dinosaurs in the shared 1080x1100 frame (ground ~y1000)."""

def svg(body):
    return f'<svg viewBox="0 0 1080 1100" width="1080" height="1100">{body}</svg>'

def dino_env():
    return """
  <circle cx="170" cy="150" r="85" fill="#ffe082"/>
  <g id="cloud1" opacity=".9"><ellipse cx="760" cy="140" rx="110" ry="40" fill="#fff"/><ellipse cx="700" cy="120" rx="60" ry="44" fill="#fff"/><ellipse cx="820" cy="120" rx="55" ry="38" fill="#fff"/></g>
  <path d="M-500 760 L-260 520 L-140 600 L40 430 L250 700 L-500 900Z" fill="#b8a7d9" opacity=".7"/>
  <path d="M1000 720 L1180 460 L1250 500 L1300 430 L1400 520 L1700 760 L1700 900 L1000 900Z" fill="#b8a7d9" opacity=".7"/>
  <g fill="#fff" opacity=".75"><circle cx="1300" cy="390" r="30"/><circle cx="1330" cy="345" r="24"/><circle cx="1350" cy="300" r="18"/></g>
  <path d="M-500 900 Q-200 860 100 900 T700 895 T1300 900 T1700 890 L1700 1100 L-500 1100Z" fill="#9ccc65"/>
  <path d="M-500 990 Q-200 960 100 990 T700 985 T1300 990 T1700 985 L1700 1100 L-500 1100Z" fill="#7cb342"/>
  <g fill="#558b2f">
    <path d="M-330 905 q-60 -80 -130 -90 q80 0 130 60 q-10 -90 40 -140 q-20 80 0 140 q40 -60 110 -60 q-70 30 -150 90z"/>
    <path d="M1330 905 q-60 -80 -130 -90 q80 0 130 60 q-10 -90 40 -140 q-20 80 0 140 q40 -60 110 -60 q-70 30 -150 90z"/>
  </g>
  <g><rect x="-215" y="560" width="34" height="350" rx="12" fill="#8d6e63"/>
    <g fill="#689f38"><path d="M-198 560 q-120 -20 -190 60 q90 -40 190 -60z"/><path d="M-198 560 q120 -20 190 60 q-90 -40 -190 -60z"/>
    <path d="M-198 560 q-80 -90 -170 -80 q100 10 170 80z"/><path d="M-198 560 q80 -90 170 -80 q-100 10 -170 80z"/></g></g>
  <g><rect x="1225" y="600" width="30" height="310" rx="12" fill="#8d6e63"/>
    <g fill="#689f38"><path d="M1240 600 q-110 -20 -170 55 q80 -36 170 -55z"/><path d="M1240 600 q110 -20 170 55 q-80 -36 -170 -55z"/>
    <path d="M1240 600 q-70 -80 -150 -72 q90 10 150 72z"/><path d="M1240 600 q70 -80 150 -72 q-90 10 -150 72z"/></g></g>"""

def eye(cx, cy, r=30):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/><circle cx="{cx+6}" cy="{cy+3}" r="{int(r*.5)}" fill="#1a1a2e"/>'
            f'<circle cx="{cx+11}" cy="{cy-4}" r="5" fill="#fff"/>')

def blush(cx, cy):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="24" ry="13" fill="#ff8fab" opacity=".6"/>'

TREX = svg(dino_env() + """
  <g id="animal">
    <path d="M330 690 Q160 720 60 860 Q200 800 360 790Z" fill="#e07b39"/>
    <rect x="390" y="780" width="90" height="210" rx="36" fill="#c9652a"/>
    <rect x="520" y="780" width="90" height="210" rx="36" fill="#d06d30"/>
    <ellipse cx="430" cy="992" rx="62" ry="18" fill="#a9521f"/><ellipse cx="570" cy="992" rx="62" ry="18" fill="#a9521f"/>
    <ellipse cx="480" cy="700" rx="200" ry="150" fill="#e07b39"/>
    <ellipse cx="540" cy="740" rx="120" ry="90" fill="#ffd59a"/>
    <g fill="#b5541f" opacity=".5"><circle cx="400" cy="620" r="18"/><circle cx="450" cy="590" r="12"/><circle cx="350" cy="680" r="14"/></g>
    <path d="M560 560 Q600 480 650 470 L700 600 Q620 640 560 620Z" fill="#e07b39"/>
    <ellipse cx="720" cy="460" rx="180" ry="118" fill="#e98a45"/>
    <path d="M590 520 Q720 590 880 500" stroke="#8a3a12" stroke-width="10" fill="none" stroke-linecap="round"/>
    <g fill="#fff"><path d="M640 540 l12 22 12 -20z"/><path d="M760 548 l12 22 12 -22z"/><path d="M830 528 l10 20 10 -22z"/></g>
    <circle cx="860" cy="420" r="8" fill="#8a3a12"/>
    """ + eye(705, 415, 34) + blush(640, 490) + """
    <g id="arms" fill="#d06d30"><path d="M640 640 q40 0 50 30 q-10 10 -22 0 q-6 -12 -28 -8z"/><path d="M610 670 q38 4 44 34 q-12 8 -22 -2 q-6 -12 -24 -10z"/></g>
  </g>
  <g id="fx" opacity="0"><circle cx="652" cy="672" r="70" fill="none" stroke="#ffeb3b" stroke-width="12" stroke-dasharray="26 16"/></g>
  <g id="fx2" opacity="0"><path d="M900 400 q40 -20 70 0" stroke="#4fc3f7" stroke-width="10" fill="none" stroke-linecap="round"/>
    <path d="M910 360 q50 -30 90 0" stroke="#4fc3f7" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M920 320 q60 -40 110 0" stroke="#4fc3f7" stroke-width="10" fill="none" stroke-linecap="round"/></g>""")

TRICERATOPS = svg(dino_env() + """
  <g id="animal">
    <path d="M260 720 Q140 760 80 860 Q190 820 280 800Z" fill="#4fa3a5"/>
    <g fill="#3f8d8f">""" + "".join(f'<rect x="{x}" y="790" width="80" height="200" rx="32"/>' for x in (270, 360, 540, 630)) + """</g>
    <g fill="#2f7072">""" + "".join(f'<ellipse cx="{x+40}" cy="992" rx="54" ry="16"/>' for x in (270, 360, 540, 630)) + """</g>
    <ellipse cx="460" cy="730" rx="240" ry="150" fill="#4fa3a5"/>
    <ellipse cx="470" cy="790" rx="160" ry="70" fill="#9fd8d0"/>
    <g fill="#3a8587" opacity=".6"><circle cx="380" cy="640" r="20"/><circle cx="450" cy="610" r="14"/><circle cx="330" cy="700" r="12"/></g>
    <circle cx="720" cy="560" r="170" fill="#f4a261"/>
    <g fill="#e76f51">""" + "".join(f'<circle cx="{720 + 150*__import__("math").cos(a):.0f}" cy="{560 + 150*__import__("math").sin(a):.0f}" r="22"/>' for a in [i*0.523 for i in range(12)]) + """</g>
    <g id="horns" fill="#fff6e0" stroke="#d9c49a" stroke-width="5">
      <path d="M735 520 Q780 380 850 340 Q820 430 785 535Z"/><path d="M845 540 Q900 400 975 370 Q935 460 885 560Z"/>
      <path d="M940 640 Q980 580 1010 575 Q995 620 965 665Z"/></g>
    <ellipse cx="830" cy="650" rx="140" ry="100" fill="#4fa3a5"/>
    <path d="M930 620 Q1000 650 960 700 L900 700Z" fill="#3f8d8f"/>
    <path d="M800 700 q50 30 100 0" stroke="#1d4f50" stroke-width="9" fill="none" stroke-linecap="round"/>
    """ + eye(800, 620, 30) + blush(760, 680) + """
  </g>
  <g id="fx" opacity="0" fill="none" stroke="#ffeb3b" stroke-width="12" stroke-linecap="round" stroke-dasharray="22 14">
    <circle cx="800" cy="420" r="80"/><circle cx="915" cy="450" r="80"/><circle cx="975" cy="620" r="55"/></g>
  <g id="fx2" opacity="0"><g fill="#66bb6a"><ellipse cx="1000" cy="880" rx="60" ry="26"/><ellipse cx="960" cy="860" rx="40" ry="20"/><ellipse cx="1040" cy="858" rx="40" ry="20"/></g></g>""")

STEGOSAURUS = svg(dino_env() + """
  <g id="animal">
    <g id="plates" fill="#ff8a65" stroke="#e86a45" stroke-width="5">
      <path d="M300 620 l40 -110 40 110z"/><path d="M370 580 l50 -140 50 140z"/><path d="M460 560 l55 -160 55 160z"/>
      <path d="M560 565 l50 -140 50 140z"/><path d="M650 600 l40 -110 40 110z"/></g>
    <path d="M300 700 Q180 690 100 600" stroke="#7cb342" stroke-width="70" fill="none" stroke-linecap="round"/>
    <g id="spikes" fill="#fff6e0" stroke="#d9c49a" stroke-width="4"><path d="M110 610 l-60 -70 70 40z"/><path d="M130 630 l-30 -100 45 85z"/><path d="M100 600 l-90 -10 85 30z"/><path d="M120 640 l-70 20 80 -5z"/></g>
    <g fill="#689f38">""" + "".join(f'<rect x="{x}" y="770" width="78" height="220" rx="30"/>' for x in (320, 410, 580, 670)) + """</g>
    <g fill="#4e7d2a">""" + "".join(f'<ellipse cx="{x+39}" cy="992" rx="52" ry="16"/>' for x in (320, 410, 580, 670)) + """</g>
    <path d="M260 760 Q300 560 500 560 Q720 560 780 760 Q520 830 260 760Z" fill="#8bc34a"/>
    <path d="M330 770 Q520 830 720 770 Q520 790 330 770Z" fill="#c5e1a5"/>
    <g fill="#689f38" opacity=".6"><circle cx="420" cy="660" r="18"/><circle cx="520" cy="630" r="14"/><circle cx="620" cy="670" r="16"/></g>
    <path d="M760 700 Q840 690 880 740" stroke="#8bc34a" stroke-width="70" fill="none" stroke-linecap="round"/>
    <ellipse cx="910" cy="760" rx="95" ry="68" fill="#8bc34a"/>
    <path d="M900 800 q40 20 80 -5" stroke="#33691e" stroke-width="8" fill="none" stroke-linecap="round"/>
    """ + eye(905, 735, 26) + blush(870, 790) + """
  </g>
  <g id="fx" opacity="0"><circle cx="105" cy="610" r="110" fill="none" stroke="#ffeb3b" stroke-width="12" stroke-dasharray="24 14"/></g>
  <g id="fx2" opacity="0" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="20 12"><path d="M280 640 Q500 340 720 640"/></g>""")

BRACHIOSAURUS = svg(dino_env() + """
  <g><rect x="975" y="300" width="44" height="610" rx="14" fill="#8d6e63"/>
    <g fill="#7cb342"><circle cx="1000" cy="250" r="110"/><circle cx="910" cy="300" r="70"/><circle cx="1090" cy="300" r="76"/></g></g>
  <g id="animal">
    <path d="M250 760 Q120 800 40 900 Q160 860 270 840Z" fill="#9575cd"/>
    <rect x="270" y="800" width="80" height="190" rx="32" fill="#7e57c2"/><rect x="360" y="800" width="80" height="190" rx="32" fill="#7e57c2"/>
    <rect x="500" y="740" width="86" height="250" rx="34" fill="#8661c9"/><rect x="600" y="740" width="86" height="250" rx="34" fill="#8661c9"/>
    <g fill="#5e3fa0"><ellipse cx="310" cy="992" rx="52" ry="16"/><ellipse cx="400" cy="992" rx="52" ry="16"/><ellipse cx="543" cy="992" rx="56" ry="16"/><ellipse cx="643" cy="992" rx="56" ry="16"/></g>
    <ellipse cx="450" cy="760" rx="240" ry="130" fill="#9575cd"/>
    <ellipse cx="470" cy="810" rx="150" ry="55" fill="#d1c4e9"/>
    <path d="M560 720 Q600 420 760 210" stroke="#9575cd" stroke-width="110" fill="none" stroke-linecap="round"/>
    <g fill="#7e57c2" opacity=".55"><circle cx="400" cy="700" r="18"/><circle cx="470" cy="680" r="12"/><circle cx="640" cy="500" r="14"/><circle cx="700" cy="380" r="11"/></g>
    <ellipse cx="800" cy="185" rx="100" ry="62" fill="#9f84d6"/>
    <path d="M800 220 q40 22 85 -2" stroke="#4a2f85" stroke-width="8" fill="none" stroke-linecap="round"/>
    <circle cx="880" cy="160" r="7" fill="#4a2f85"/>
    """ + eye(790, 165, 26) + blush(760, 215) + """
  </g>
  <g id="fx" opacity="0"><line x1="140" y1="990" x2="140" y2="150" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="26 14"/>
    <path d="M110 180 l30 -40 30 40" stroke="#ffeb3b" stroke-width="10" fill="none"/>
    <g transform="translate(60 840)"><rect x="0" y="50" width="160" height="100" fill="#fff3e0" stroke="#8d6e63" stroke-width="6"/><path d="M-12 56 L80 -10 L172 56Z" fill="#e57373"/><rect x="62" y="90" width="36" height="60" fill="#8d6e63"/></g></g>
  <g id="fx2" opacity="0"><circle cx="910" cy="230" r="90" fill="none" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="20 12"/></g>""")

PTERANODON = svg(dino_env() + """
  <g id="animal">
    <path d="M540 520 L80 380 Q200 520 300 600 L540 600Z" fill="#4fc3f7"/>
    <path d="M540 520 L1000 380 Q880 520 780 600 L540 600Z" fill="#4fc3f7"/>
    <path d="M540 540 L170 410 Q250 520 330 585 L540 590Z" fill="#81d4fa"/>
    <path d="M540 540 L910 410 Q830 520 750 585 L540 590Z" fill="#81d4fa"/>
    <ellipse cx="540" cy="580" rx="80" ry="120" fill="#29b6f6"/>
    <ellipse cx="540" cy="610" rx="48" ry="80" fill="#e1f5fe"/>
    <path d="M510 690 l-20 50 M570 690 l20 50" stroke="#0288d1" stroke-width="14" stroke-linecap="round"/>
    <path d="M520 440 L360 360 Q470 400 545 420Z" fill="#ff8a65"/>
    <circle cx="560" cy="440" r="70" fill="#29b6f6"/>
    <path d="M600 440 L820 470 L600 480Z" fill="#ffb74d" stroke="#f57c00" stroke-width="5" stroke-linejoin="round"/>
    """ + eye(560, 425, 26) + blush(540, 475) + """
  </g>
  <g id="fx" opacity="0"><g transform="translate(830 230)"><path d="M0 40 q30 -40 60 0 q30 -40 60 0" stroke="#37474f" stroke-width="10" fill="none" stroke-linecap="round"/></g></g>
  <g id="fx2" opacity="0"><path d="M-500 1000 Q-200 960 100 1000 T700 995 T1300 1000 T1700 995 L1700 1100 L-500 1100Z" fill="#4fc3f7"/><path d="M-500 1030 Q-200 1010 100 1030 T700 1025 T1300 1030 T1700 1025" stroke="#e1f5fe" stroke-width="10" fill="none"/></g>""")

DINO_TITLE = svg(dino_env() + """
  <g transform="translate(-130 -40)">
    <rect x="160" y="230" width="760" height="150" rx="40" fill="#8d5a2b" stroke="#5d3a1a" stroke-width="10"/>
    <text x="540" y="332" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="84" fill="#fff6e0">DINO WORLD KIDS</text>
    <rect x="300" y="380" width="26" height="140" fill="#5d3a1a"/><rect x="754" y="380" width="26" height="140" fill="#5d3a1a"/>
    <ellipse cx="540" cy="760" rx="150" ry="190" fill="#fff6e0" stroke="#d9c49a" stroke-width="8"/>
    <g fill="#9ccc65"><circle cx="480" cy="690" r="28"/><circle cx="600" cy="740" r="34"/><circle cx="520" cy="840" r="24"/><circle cx="610" cy="860" r="18"/></g>
    <path d="M400 700 l40 -40 40 40 40 -40 40 40 40 -40 40 40 40 -40" stroke="#d9c49a" stroke-width="8" fill="none"/>
  </g>""")

SCENES4 = {"trex": TREX, "triceratops": TRICERATOPS, "stegosaurus": STEGOSAURUS,
           "brachiosaurus": BRACHIOSAURUS, "pteranodon": PTERANODON}
NAMES4 = {"trex": "T. REX", "brachiosaurus": "BRACHIOSAURUS"}
