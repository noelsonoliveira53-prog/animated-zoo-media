"""Original SVG art for The Animated Zoo (Milo the bluebird + zoo animals). All shapes drawn here."""

MILO = """<svg id="milo" viewBox="0 0 220 200" width="260" height="236">
  <polygon points="40,118 0,96 6,150" fill="#1c5fc4"/>
  <polygon points="88,44 98,14 108,44" fill="#2f80ed"/>
  <polygon points="100,44 116,20 118,48" fill="#2f80ed"/>
  <circle cx="100" cy="110" r="70" fill="#2f80ed"/>
  <ellipse cx="114" cy="132" rx="46" ry="40" fill="#a7d3ff"/>
  <circle cx="128" cy="88" r="19" fill="#fff"/>
  <circle cx="133" cy="90" r="9" fill="#1a1a2e"/>
  <circle cx="136" cy="86" r="3" fill="#fff"/>
  <ellipse cx="148" cy="112" rx="10" ry="6" fill="#ff9ab0" opacity=".7"/>
  <polygon points="164,98 202,110 164,124" fill="#ff9f1c"/>
  <g id="wing"><ellipse cx="78" cy="122" rx="42" ry="26" fill="#1c5fc4" transform="rotate(-18 78 122)"/></g>
  <path d="M95 178 l-6 16 M112 178 l6 16" stroke="#ff9f1c" stroke-width="6" stroke-linecap="round"/>
</svg>"""

SKY_EXTRAS = """
  <circle cx="160" cy="150" r="90" fill="#ffe066"/>
  <g id="cloud1" opacity=".95"><ellipse cx="760" cy="140" rx="110" ry="42" fill="#fff"/><ellipse cx="700" cy="120" rx="60" ry="45" fill="#fff"/><ellipse cx="820" cy="118" rx="55" ry="40" fill="#fff"/></g>
"""

def ground(color="#7ccf5a", dark="#5fb043"):
    return f"""
  <rect x="-500" y="950" width="2200" height="200" fill="{color}"/><path d="M-500 960 Q-230 900 0 950 Q270 900 540 950 T1080 940 T1620 950 L1620 1100 L-500 1100 Z" fill="{color}"/>
  <path d="M-500 1020 Q-200 980 100 1020 Q300 980 600 1020 T1080 1010 T1620 1015 L1620 1100 L-500 1100 Z" fill="{dark}"/>
  <g stroke="#b07a3b" stroke-width="14" stroke-linecap="round">
    <line x1="-480" y1="1000" x2="1560" y2="1000"/><line x1="-480" y1="940" x2="1560" y2="940"/>
  </g>
  <g fill="#c98d4b">{''.join(f'<rect x="{x}" y="900" width="22" height="130" rx="8"/>' for x in range(-440,1560,120))}</g>"""

GIRAFFE = f"""<svg viewBox="0 0 1080 1100" width="1080" height="1100">
  {SKY_EXTRAS}{ground()}
  <rect x="945" y="380" width="50" height="620" rx="20" fill="#8d5a2b"/>
  <g id="leaves"><circle cx="975" cy="300" r="120" fill="#43a047"/><circle cx="895" cy="345" r="78" fill="#4caf50"/><circle cx="1060" cy="355" r="80" fill="#4caf50"/></g>
  <g id="animal">
    <path d="M245 735 Q215 800 222 860" stroke="#d9a23f" stroke-width="10" fill="none"/>
    <ellipse cx="222" cy="868" rx="12" ry="20" fill="#8a5222"/>
    <g fill="#e8b247">{''.join(f'<rect x="{x}" y="800" width="38" height="200" rx="14"/>' for x in (290,350,480,540))}</g>
    <g fill="#5d3a1a">{''.join(f'<rect x="{x}" y="975" width="38" height="28" rx="6"/>' for x in (290,350,480,540))}</g>
    <ellipse cx="430" cy="760" rx="195" ry="100" fill="#f6c453"/>
    <polygon points="465,710 565,705 650,300 595,280" fill="#f6c453"/>
    <g fill="#b8732e">
      <circle cx="380" cy="740" r="24"/><circle cx="465" cy="785" r="19"/><circle cx="525" cy="735" r="21"/>
      <circle cx="325" cy="790" r="16"/><circle cx="560" cy="625" r="15"/><circle cx="590" cy="505" r="14"/>
      <circle cx="616" cy="395" r="12"/><circle cx="505" cy="700" r="15"/><circle cx="440" cy="715" r="13"/>
    </g>
    <g id="tongue"><rect x="740" y="268" width="140" height="26" rx="13" fill="#6a3d9a"/></g>
    <line x1="622" y1="210" x2="612" y2="160" stroke="#c98a3b" stroke-width="12" stroke-linecap="round"/>
    <line x1="662" y1="205" x2="668" y2="155" stroke="#c98a3b" stroke-width="12" stroke-linecap="round"/>
    <circle cx="612" cy="156" r="13" fill="#7a4a1f"/><circle cx="668" cy="151" r="13" fill="#7a4a1f"/>
    <ellipse cx="588" cy="228" rx="34" ry="16" fill="#e8b247" transform="rotate(-25 588 228)"/>
    <ellipse cx="650" cy="250" rx="88" ry="52" fill="#f6c453" transform="rotate(-12 650 250)"/>
    <ellipse cx="718" cy="272" rx="46" ry="36" fill="#f9dc8c"/>
    <circle cx="735" cy="262" r="5" fill="#7a4a1f"/>
    <circle cx="648" cy="236" r="12" fill="#1a1a2e"/><circle cx="652" cy="231" r="4" fill="#fff"/>
    <ellipse cx="690" cy="262" rx="12" ry="7" fill="#ff9ab0" opacity=".6"/>
  </g>
  <g id="sunshield" opacity="0"><circle cx="160" cy="150" r="130" fill="#ffe066" opacity=".35"/></g>
</svg>"""

PENGUIN = f"""<svg viewBox="0 0 1080 1100" width="1080" height="1100">
  {SKY_EXTRAS}
  <path d="M-500 930 L1620 930 L1620 1100 L-500 1100 Z" fill="#4fc3f7"/>
  <path d="M120 940 L960 940 L1010 1100 L70 1100 Z" fill="#f4fbff"/>
  <path d="M120 940 L960 940 L975 980 L105 980 Z" fill="#d7eefa"/>
  <polygon points="40,930 120,840 190,930" fill="#e8f6ff"/><polygon points="880,930 960,820 1050,930" fill="#e8f6ff"/>
  <g id="animal">
    <ellipse cx="470" cy="985" rx="62" ry="22" fill="#ff9f1c"/><ellipse cx="610" cy="985" rx="62" ry="22" fill="#ff9f1c"/>
    <ellipse cx="350" cy="720" rx="42" ry="140" fill="#263238" transform="rotate(18 350 720)"/>
    <ellipse cx="730" cy="720" rx="42" ry="140" fill="#263238" transform="rotate(-18 730 720)"/>
    <ellipse cx="540" cy="700" rx="200" ry="285" fill="#263238"/>
    <ellipse cx="540" cy="745" rx="142" ry="222" fill="#fdfdfd"/>
    <circle cx="482" cy="520" r="20" fill="#fff"/><circle cx="598" cy="520" r="20" fill="#fff"/>
    <circle cx="486" cy="522" r="10" fill="#1a1a2e"/><circle cx="594" cy="522" r="10" fill="#1a1a2e"/>
    <circle cx="489" cy="518" r="3" fill="#fff"/><circle cx="597" cy="518" r="3" fill="#fff"/>
    <polygon points="512,560 568,560 540,604" fill="#ff9f1c"/>
    <ellipse cx="455" cy="590" rx="18" ry="10" fill="#ff9ab0" opacity=".7"/><ellipse cx="625" cy="590" rx="18" ry="10" fill="#ff9ab0" opacity=".7"/>
    <g id="coat" opacity="0" stroke="#90caf9" stroke-width="6" stroke-linecap="round" fill="none">
      <path d="M440 760 q15 -14 30 0 q15 14 30 0"/><path d="M560 800 q15 -14 30 0 q15 14 30 0"/>
      <path d="M470 880 q15 -14 30 0 q15 14 30 0"/><path d="M580 690 q15 -14 30 0 q15 14 30 0"/>
    </g>
  </g>
  <g id="xray" opacity="0">
    <rect x="370" y="760" width="340" height="235" rx="40" fill="#0d47a1" opacity=".72"/>
    <g stroke="#ffffff" stroke-width="20" stroke-linecap="round" fill="none">
      <path d="M485 785 L450 880 L478 970"/><path d="M595 785 L630 880 L602 970"/>
    </g>
    <circle cx="450" cy="880" r="19" fill="#ffeb3b"/><circle cx="630" cy="880" r="19" fill="#ffeb3b"/>
    <text x="540" y="835" text-anchor="middle" font-family="Baloo 2, Arial Rounded MT Bold, sans-serif" font-weight="800" font-size="46" fill="#ffeb3b">KNEES!</text>
  </g>
</svg>"""

ELEPHANT = f"""<svg viewBox="0 0 1080 1100" width="1080" height="1100">
  {SKY_EXTRAS}{ground("#e9c46a", "#d4a94f")}
  <g id="animal">
    <path d="M262 640 Q225 700 238 770" stroke="#8c8c8c" stroke-width="12" fill="none"/>
    <g fill="#9e9e9e">{''.join(f'<rect x="{x}" y="700" width="78" height="300" rx="26"/>' for x in (330,430,580,680))}</g>
    <g fill="#f1e3c8">{''.join(f'<ellipse cx="{x+39+d}" cy="992" rx="11" ry="8"/>' for x in (330,430,580,680) for d in (-20,0,20))}</g>
    <ellipse cx="520" cy="640" rx="270" ry="175" fill="#a8a8a8"/>
    <g id="legsglow" opacity="0" stroke="#ffeb3b" stroke-width="10" stroke-dasharray="22 16" stroke-linecap="round">
      {''.join(f'<line x1="{x+39}" y1="720" x2="{x+39}" y2="990"/>' for x in (330,430,580,680))}
    </g>
    <circle cx="770" cy="520" r="128" fill="#b0b0b0"/>
    <ellipse cx="690" cy="525" rx="112" ry="145" fill="#999"/>
    <ellipse cx="695" cy="530" rx="72" ry="98" fill="#f3b6c4"/>
    <g id="trunk">
      <path d="M850 570 Q905 690 870 820 Q862 850 900 846" stroke="#b0b0b0" stroke-width="52" stroke-linecap="round" fill="none"/>
    </g>
    <path d="M820 610 q30 30 62 18" stroke="#fffaf0" stroke-width="16" stroke-linecap="round" fill="none"/>
    <circle cx="800" cy="482" r="12" fill="#1a1a2e"/><circle cx="804" cy="477" r="4" fill="#fff"/>
    <ellipse cx="835" cy="525" rx="18" ry="10" fill="#ff9ab0" opacity=".6"/>
  </g>
  <g id="water" opacity="0">
    <rect x="0" y="780" width="1080" height="320" fill="#29b6f6" opacity=".82"/>
    <path d="M0 790 q45 -26 90 0 t90 0 t90 0 t90 0 t90 0 t90 0 t90 0 t90 0 t90 0 t90 0 t90 0 t90 0" stroke="#e1f5fe" stroke-width="10" fill="none"/>
  </g>
  <g id="heart" opacity="0">
    <path d="M930 420 C860 370 860 300 905 300 C925 300 930 318 930 318 C930 318 935 300 955 300 C1000 300 1000 370 930 420 Z" fill="#ff5c8a"/>
  </g>
</svg>"""

SCENES = {"giraffe": GIRAFFE, "penguin": PENGUIN, "elephant": ELEPHANT}
