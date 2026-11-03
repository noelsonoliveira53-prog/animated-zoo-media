"""More original zoo animals. Same local frame as art.py: 1080x1100, ground line ~y1000, animal centred ~x540."""
from art import SKY_EXTRAS, ground

def svg(body):
    return f'<svg viewBox="0 0 1080 1100" width="1080" height="1100">{body}</svg>'

def sea_env():
    return """
  <defs><linearGradient id="seag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4fc3f7"/><stop offset="1" stop-color="#0277bd"/></linearGradient></defs>
  <rect x="-500" y="-10" width="2200" height="1200" fill="url(#seag)"/>
  <g fill="#ffffff" opacity=".18"><polygon points="-200,0 0,0 200,700 60,700"/><polygon points="500,0 640,0 780,650 620,650"/><polygon points="1200,0 1350,0 1450,700 1300,700"/></g>
  <path d="M-500 960 Q-200 920 100 960 T700 955 T1300 960 T1700 955 L1700 1100 L-500 1100 Z" fill="#f2d49b"/>
  <g fill="#2e7d32"><path d="M-150 960 q-30 -120 10 -220 q30 100 -10 220"/><path d="M1240 960 q-40 -160 10 -280 q40 130 -10 280"/><path d="M1290 960 q-20 -100 20 -180 q20 90 -20 180"/></g>
  <g fill="#ff8a80"><circle cx="-60" cy="950" r="26"/><circle cx="1180" cy="955" r="22"/></g>
  <g id="bubbles" fill="none" stroke="#e1f5fe" stroke-width="5"><circle cx="160" cy="700" r="16"/><circle cx="190" cy="600" r="10"/><circle cx="930" cy="760" r="14"/><circle cx="960" cy="650" r="9"/><circle cx="1350" cy="500" r="18"/></g>"""

def snow_env():
    return SKY_EXTRAS + """
  <rect x="-500" y="930" width="2200" height="200" fill="#ffffff"/>
  <path d="M-500 940 Q-200 900 100 940 T700 935 T1300 940 T1700 930 L1700 1100 L-500 1100 Z" fill="#eef7ff"/>
  <polygon points="-380,940 -260,760 -140,940" fill="#e3f2fd"/><polygon points="1260,940 1380,720 1520,940" fill="#e3f2fd"/>
  <g fill="#ffffff" opacity=".9"><circle cx="80" cy="300" r="7"/><circle cx="330" cy="420" r="6"/><circle cx="880" cy="360" r="7"/><circle cx="1260" cy="260" r="8"/><circle cx="-250" cy="380" r="6"/></g>"""

def forest_env():
    return SKY_EXTRAS + ground() + """
  <g fill="#81c784" opacity=".8"><circle cx="-300" cy="520" r="170"/><circle cx="-160" cy="600" r="130"/><circle cx="1300" cy="520" r="170"/><circle cx="1440" cy="600" r="140"/></g>
  <g fill="#8d5a2b"><rect x="-320" y="600" width="40" height="350"/><rect x="1290" y="600" width="40" height="350"/></g>"""

def pond_env():
    return SKY_EXTRAS + ground() + '<ellipse cx="540" cy="985" rx="640" ry="95" fill="#4fc3f7"/><ellipse cx="540" cy="975" rx="560" ry="60" fill="#81d4fa"/>'

def sand_env():
    return SKY_EXTRAS + ground("#e9c46a", "#d4a94f") + """
  <g><rect x="-250" y="560" width="26" height="390" fill="#8d5a2b"/><ellipse cx="-237" cy="560" rx="200" ry="55" fill="#7cb342"/></g>"""

LION = svg(sand_env() + """
  <g id="animal">
    <path d="M300 760 Q230 760 225 690" stroke="#d69a3a" stroke-width="16" fill="none" stroke-linecap="round"/>
    <circle cx="225" cy="680" r="24" fill="#8a4b16"/>
    <g fill="#e0a640">""" + ''.join(f'<rect x="{x}" y="780" width="58" height="215" rx="22"/>' for x in (340,410,600,670)) + """</g>
    <g fill="#c98b30">""" + ''.join(f'<ellipse cx="{x+29}" cy="992" rx="38" ry="16"/>' for x in (340,410,600,670)) + """</g>
    <ellipse cx="500" cy="740" rx="215" ry="115" fill="#e8b04a"/>
    <g fill="#b5651d">""" + ''.join(f'<circle cx="{700+150*__import__("math").cos(a/8*6.283):.0f}" cy="{560+150*__import__("math").sin(a/8*6.283):.0f}" r="58"/>' for a in range(8)) + """</g>
    <circle cx="700" cy="560" r="152" fill="#b5651d"/>
    <circle cx="628" cy="478" r="30" fill="#e8b04a"/><circle cx="772" cy="478" r="30" fill="#e8b04a"/>
    <circle cx="700" cy="572" r="102" fill="#f2c35e"/>
    <ellipse cx="682" cy="622" rx="26" ry="19" fill="#fbe3b0"/><ellipse cx="718" cy="622" rx="26" ry="19" fill="#fbe3b0"/>
    <polygon points="684,592 716,592 700,612" fill="#6d3b1f"/>
    <circle cx="664" cy="550" r="12" fill="#1a1a2e"/><circle cx="736" cy="550" r="12" fill="#1a1a2e"/>
    <circle cx="668" cy="545" r="4" fill="#fff"/><circle cx="740" cy="545" r="4" fill="#fff"/>
    <ellipse cx="640" cy="590" rx="16" ry="9" fill="#ff9ab0" opacity=".6"/><ellipse cx="760" cy="590" rx="16" ry="9" fill="#ff9ab0" opacity=".6"/>
  </g>
  <g id="fx" opacity="0" stroke="#ff7043" stroke-width="12" fill="none" stroke-linecap="round">
    <path d="M860 520 q30 40 0 80"/><path d="M900 490 q50 70 0 140"/><path d="M940 460 q70 100 0 200"/>
  </g>""")

ZEBRA = svg(SKY_EXTRAS + ground() + """
  <defs><clipPath id="zbody"><ellipse cx="480" cy="720" rx="200" ry="100"/></clipPath>
  <clipPath id="zneck"><polygon points="590,700 670,700 735,480 660,455"/></clipPath></defs>
  <g id="animal">
    <path d="M285 700 Q250 760 262 830" stroke="#222" stroke-width="10" fill="none"/>
    <g fill="#fff" stroke="#222" stroke-width="5">""" + ''.join(f'<rect x="{x}" y="780" width="42" height="215" rx="14"/>' for x in (340,400,540,600)) + """</g>
    <g stroke="#222" stroke-width="12">""" + ''.join(f'<line x1="{x}" y1="{y}" x2="{x+42}" y2="{y}"/>' for x in (340,400,540,600) for y in (830,875,920)) + """</g>
    <g fill="#333">""" + ''.join(f'<rect x="{x}" y="975" width="42" height="22" rx="6"/>' for x in (340,400,540,600)) + """</g>
    <ellipse cx="480" cy="720" rx="200" ry="100" fill="#fff" stroke="#222" stroke-width="6"/>
    <g clip-path="url(#zbody)" stroke="#222" stroke-width="18" fill="none">""" + ''.join(f'<path d="M{x} 610 q22 110 0 220"/>' for x in range(320, 680, 46)) + """</g>
    <polygon points="590,700 670,700 735,480 660,455" fill="#fff" stroke="#222" stroke-width="5"/>
    <g clip-path="url(#zneck)" stroke="#222" stroke-width="16">""" + ''.join(f'<line x1="560" y1="{y}" x2="760" y2="{y-30}"/>' for y in range(500, 720, 42)) + """</g>
    <path d="M655 455 l-20 40 l25 5 l-20 45 l25 5 l-20 45 l25 5 l-20 45" stroke="#222" stroke-width="14" fill="none"/>
    <ellipse cx="735" cy="470" rx="95" ry="52" fill="#fff" stroke="#222" stroke-width="5" transform="rotate(22 735 470)"/>
    <ellipse cx="800" cy="510" rx="40" ry="34" fill="#333"/>
    <circle cx="790" cy="500" r="6" fill="#777"/>
    <ellipse cx="680" cy="410" rx="16" ry="36" fill="#fff" stroke="#222" stroke-width="5" transform="rotate(-20 680 410)"/>
    <circle cx="725" cy="455" r="11" fill="#1a1a2e"/><circle cx="729" cy="450" r="4" fill="#fff"/>
  </g>
  <g id="fx" opacity="0"><circle cx="470" cy="720" r="95" fill="none" stroke="#ffca28" stroke-width="16"/>
    <line x1="400" y1="790" x2="330" y2="870" stroke="#ffca28" stroke-width="22" stroke-linecap="round"/></g>""")

HIPPO = svg(pond_env() + """
  <g id="animal">
    <g fill="#8f7d9a">""" + ''.join(f'<rect x="{x}" y="850" width="74" height="140" rx="24"/>' for x in (350,440,600,690)) + """</g>
    <ellipse cx="520" cy="770" rx="270" ry="155" fill="#9c8aa5"/>
    <path d="M262 760 q-30 10 -36 40" stroke="#8f7d9a" stroke-width="14" fill="none" stroke-linecap="round"/>
    <ellipse cx="760" cy="700" rx="145" ry="112" fill="#9c8aa5"/>
    <ellipse cx="835" cy="770" rx="125" ry="88" fill="#b9a7c2"/>
    <circle cx="860" cy="735" r="11" fill="#5d4e66"/><circle cx="905" cy="742" r="11" fill="#5d4e66"/>
    <circle cx="718" cy="610" r="30" fill="#9c8aa5"/><circle cx="782" cy="604" r="30" fill="#9c8aa5"/>
    <circle cx="720" cy="608" r="12" fill="#1a1a2e"/><circle cx="784" cy="602" r="12" fill="#1a1a2e"/>
    <circle cx="724" cy="603" r="4" fill="#fff"/><circle cx="788" cy="597" r="4" fill="#fff"/>
    <ellipse cx="680" cy="585" rx="14" ry="20" fill="#8f7d9a"/>
    <path d="M760 805 q70 30 140 0" stroke="#5d4e66" stroke-width="7" fill="none" stroke-linecap="round"/>
    <ellipse cx="750" cy="745" rx="20" ry="11" fill="#ff9ab0" opacity=".6"/>
  </g>
  <g id="fx" opacity="0"><ellipse cx="560" cy="740" rx="300" ry="175" fill="#ff8a50" opacity=".33"/>
    <g fill="#ff7043">""" + ''.join(f'<circle cx="{x}" cy="{y}" r="9"/>' for x, y in ((420,700),(520,660),(610,720),(470,800),(700,660),(800,700))) + """</g></g>
  <g id="fx2" opacity="0"><rect x="-500" y="760" width="2200" height="400" fill="#29b6f6" opacity=".78"/>
    <path d="M-500 770 q60 -24 120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0" stroke="#e1f5fe" stroke-width="10" fill="none"/></g>""")

MONKEY = svg(forest_env() + """
  <rect x="-500" y="400" width="2200" height="40" rx="20" fill="#8d5a2b"/>
  <g fill="#43a047"><ellipse cx="160" cy="400" rx="60" ry="26"/><ellipse cx="900" cy="400" rx="70" ry="28"/><ellipse cx="1200" cy="410" rx="60" ry="24"/></g>
  <g id="animal">
    <path id="fx" d="M570 640 C 720 640, 740 420, 650 412 C 600 410, 600 445, 640 446" stroke="#6d4c2f" stroke-width="20" fill="none" stroke-linecap="round"/>
    <path d="M495 600 Q420 520 455 425" stroke="#6d4c2f" stroke-width="24" fill="none" stroke-linecap="round"/>
    <path d="M585 600 Q640 700 620 800" stroke="#6d4c2f" stroke-width="24" fill="none" stroke-linecap="round"/>
    <path d="M510 740 Q480 830 500 900" stroke="#6d4c2f" stroke-width="24" fill="none" stroke-linecap="round"/>
    <path d="M570 740 Q610 830 590 900" stroke="#6d4c2f" stroke-width="24" fill="none" stroke-linecap="round"/>
    <ellipse cx="540" cy="660" rx="75" ry="105" fill="#6d4c2f"/>
    <ellipse cx="540" cy="680" rx="45" ry="65" fill="#a1887f"/>
    <circle cx="465" cy="520" r="26" fill="#d7a86e"/><circle cx="615" cy="520" r="26" fill="#d7a86e"/>
    <circle cx="540" cy="515" r="78" fill="#6d4c2f"/>
    <ellipse cx="540" cy="535" rx="56" ry="50" fill="#d7a86e"/>
    <circle cx="518" cy="520" r="10" fill="#1a1a2e"/><circle cx="562" cy="520" r="10" fill="#1a1a2e"/>
    <circle cx="521" cy="516" r="3" fill="#fff"/><circle cx="565" cy="516" r="3" fill="#fff"/>
    <path d="M520 560 q20 16 40 0" stroke="#5d3a1a" stroke-width="6" fill="none" stroke-linecap="round"/>
    <circle cx="455" cy="425" r="16" fill="#6d4c2f"/>
  </g>""")

FLAMINGO = svg(pond_env() + """
  <g id="animal">
    <line x1="520" y1="620" x2="520" y2="965" stroke="#ff6f91" stroke-width="13" stroke-linecap="round"/>
    <path d="M545 620 L585 735 L530 760" stroke="#ff6f91" stroke-width="13" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M520 965 l-40 12 M520 965 l40 12" stroke="#ff6f91" stroke-width="10" stroke-linecap="round"/>
    <path d="M330 560 l-60 -30 l20 50 z" fill="#e85d84"/>
    <ellipse cx="510" cy="560" rx="150" ry="85" fill="#ff8fb1"/>
    <ellipse cx="480" cy="555" rx="95" ry="52" fill="#f06292"/>
    <path d="M620 540 Q720 420 655 330 Q600 255 665 225" stroke="#ff8fb1" stroke-width="36" fill="none" stroke-linecap="round"/>
    <circle cx="672" cy="222" r="42" fill="#ff8fb1"/>
    <path d="M700 215 Q760 220 755 270 L735 262 Q735 240 702 238 Z" fill="#fff"/>
    <path d="M745 245 Q760 262 750 278 L735 262 Z" fill="#1a1a2e"/>
    <circle cx="676" cy="212" r="9" fill="#1a1a2e"/><circle cx="679" cy="208" r="3" fill="#fff"/>
  </g>
  <g id="fx" opacity="0">
    <line x1="230" y1="850" x2="230" y2="965" stroke="#bdbdbd" stroke-width="8"/>
    <ellipse cx="230" cy="840" rx="62" ry="40" fill="#cfcfcf"/>
    <path d="M275 830 Q310 770 290 745" stroke="#cfcfcf" stroke-width="18" fill="none" stroke-linecap="round"/>
    <circle cx="292" cy="738" r="22" fill="#cfcfcf"/><circle cx="296" cy="734" r="5" fill="#1a1a2e"/>
    <path d="M310 735 l18 10 l-18 6 z" fill="#555"/>
  </g>
  <g id="fx2" opacity="0" fill="#ff7043">""" + ''.join(f'<path d="M{x} {y} q18 -14 36 0 q-6 14 -18 16 q-14 -2 -18 -16 z"/>' for x, y in ((250,960),(330,975),(780,968),(860,958),(920,975))) + """</g>""")

KANGAROO = svg(sand_env() + """
  <g id="animal">
    <path d="M430 850 Q330 960 220 990" stroke="#b5733a" stroke-width="48" fill="none" stroke-linecap="round"/>
    <ellipse cx="470" cy="990" rx="95" ry="22" fill="#a8652f"/><ellipse cx="600" cy="992" rx="95" ry="22" fill="#a8652f"/>
    <ellipse cx="500" cy="900" rx="80" ry="95" fill="#c68642"/><ellipse cx="590" cy="905" rx="75" ry="90" fill="#c68642"/>
    <ellipse cx="530" cy="700" rx="140" ry="200" fill="#c68642" transform="rotate(-12 530 700)"/>
    <ellipse cx="560" cy="740" rx="85" ry="140" fill="#e0b080" transform="rotate(-12 560 740)"/>
    <g id="fx" opacity="0"><circle cx="575" cy="742" r="34" fill="#d9a066"/>
      <ellipse cx="555" cy="708" rx="9" ry="20" fill="#d9a066"/><ellipse cx="592" cy="706" rx="9" ry="20" fill="#d9a066"/>
      <circle cx="565" cy="740" r="5" fill="#1a1a2e"/><circle cx="586" cy="740" r="5" fill="#1a1a2e"/></g>
    <path d="M490 790 Q575 820 650 770" stroke="#b5733a" stroke-width="10" fill="#e0b080"/>
    <path d="M640 620 Q690 660 700 700" stroke="#c68642" stroke-width="22" fill="none" stroke-linecap="round"/>
    <ellipse cx="575" cy="390" rx="20" ry="58" fill="#c68642" transform="rotate(-12 575 390)"/>
    <ellipse cx="625" cy="388" rx="20" ry="58" fill="#c68642" transform="rotate(12 625 388)"/>
    <ellipse cx="575" cy="392" rx="9" ry="38" fill="#f3b6c4" transform="rotate(-12 575 392)"/>
    <ellipse cx="625" cy="390" rx="9" ry="38" fill="#f3b6c4" transform="rotate(12 625 390)"/>
    <ellipse cx="605" cy="475" rx="62" ry="70" fill="#c68642"/>
    <ellipse cx="655" cy="500" rx="48" ry="34" fill="#e0b080"/>
    <ellipse cx="690" cy="490" rx="12" ry="9" fill="#3e2723"/>
    <circle cx="600" cy="460" r="11" fill="#1a1a2e"/><circle cx="604" cy="455" r="4" fill="#fff"/>
    <ellipse cx="620" cy="500" rx="14" ry="8" fill="#ff9ab0" opacity=".6"/>
  </g>""")

OCTOPUS = svg(sea_env() + """
  <g id="animal">
    <g class="ocs" stroke="#ff7043" stroke-width="46" fill="none" stroke-linecap="round">
      <path d="M430 640 Q330 760 260 760 Q200 760 220 820"/><path d="M460 670 Q400 820 350 880"/>
      <path d="M500 690 Q480 840 440 920"/><path d="M530 700 Q540 850 520 930"/>
      <path d="M560 700 Q600 850 620 920"/><path d="M590 690 Q680 820 720 880"/>
      <path d="M620 670 Q720 760 800 770 Q850 770 840 830"/><path d="M640 640 Q760 680 860 640"/>
    </g>
    <g fill="#ffccbc">""" + ''.join(f'<circle cx="{x}" cy="{y}" r="9"/>' for x, y in ((300,762),(370,850),(458,880),(523,900),(607,890),(690,850),(780,770),(820,655))) + """</g>
    <ellipse class="ocf" cx="540" cy="500" rx="175" ry="200" fill="#ff7043"/>
    <ellipse class="ocf2" cx="500" cy="420" rx="50" ry="70" fill="#ff8a65"/>
    <circle cx="480" cy="560" r="36" fill="#fff"/><circle cx="600" cy="560" r="36" fill="#fff"/>
    <circle cx="488" cy="565" r="17" fill="#1a1a2e"/><circle cx="592" cy="565" r="17" fill="#1a1a2e"/>
    <circle cx="494" cy="558" r="6" fill="#fff"/><circle cx="598" cy="558" r="6" fill="#fff"/>
    <path d="M515 625 q25 18 50 0" stroke="#bf360c" stroke-width="7" fill="none" stroke-linecap="round"/>
    <ellipse cx="440" cy="610" rx="18" ry="10" fill="#ff9ab0" opacity=".7"/><ellipse cx="640" cy="610" rx="18" ry="10" fill="#ff9ab0" opacity=".7"/>
  </g>""")

TURTLE = svg(sea_env() + """
  <g id="animal">
    <ellipse cx="690" cy="430" rx="110" ry="40" fill="#8bc34a" transform="rotate(-30 690 430)"/>
    <ellipse cx="690" cy="690" rx="110" ry="40" fill="#8bc34a" transform="rotate(30 690 690)"/>
    <ellipse cx="370" cy="460" rx="70" ry="30" fill="#8bc34a" transform="rotate(30 370 460)"/>
    <ellipse cx="370" cy="660" rx="70" ry="30" fill="#8bc34a" transform="rotate(-30 370 660)"/>
    <ellipse cx="810" cy="555" rx="78" ry="58" fill="#8bc34a"/>
    <circle cx="830" cy="535" r="12" fill="#1a1a2e"/><circle cx="834" cy="530" r="4" fill="#fff"/>
    <path d="M840 580 q25 10 45 -6" stroke="#33691e" stroke-width="6" fill="none" stroke-linecap="round"/>
    <ellipse cx="540" cy="560" rx="230" ry="150" fill="#2e7d32"/>
    <g fill="#66bb6a">""" + ''.join(f'<polygon points="{x-40},{y} {x-20},{y-35} {x+20},{y-35} {x+40},{y} {x+20},{y+35} {x-20},{y+35}"/>' for x, y in ((540,560),(450,510),(630,510),(450,610),(630,610),(360,560),(720,560))) + """</g>
  </g>
  <g id="fx" opacity="0">""" + ''.join(f'<g transform="translate({x} {y}) scale(.22)"><ellipse cx="0" cy="0" rx="230" ry="150" fill="#2e7d32"/><ellipse cx="270" cy="-5" rx="78" ry="58" fill="#8bc34a"/><ellipse cx="150" cy="-130" rx="110" ry="40" fill="#8bc34a"/><ellipse cx="150" cy="130" rx="110" ry="40" fill="#8bc34a"/></g>' for x, y in ((180,930),(330,945),(880,935))) + """</g>""")

POLARBEAR = svg(snow_env() + """
  <g id="animal">
    <g fill="#f5f5f5" stroke="#cfd8dc" stroke-width="6">""" + ''.join(f'<rect x="{x}" y="770" width="80" height="210" rx="30"/>' for x in (320,420,580,680)) + """</g>
    <g fill="#e0e0e0">""" + ''.join(f'<ellipse cx="{x+40}" cy="980" rx="55" ry="18"/>' for x in (320,420,580,680)) + """</g>
    <ellipse cx="510" cy="720" rx="250" ry="150" fill="#fafafa" stroke="#cfd8dc" stroke-width="6"/>
    <circle cx="705" cy="565" r="28" fill="#fafafa" stroke="#cfd8dc" stroke-width="6"/><circle cx="810" cy="560" r="28" fill="#fafafa" stroke="#cfd8dc" stroke-width="6"/>
    <circle cx="760" cy="640" r="100" fill="#fafafa" stroke="#cfd8dc" stroke-width="6"/>
    <ellipse cx="835" cy="675" rx="55" ry="40" fill="#ffffff" stroke="#cfd8dc" stroke-width="5"/>
    <ellipse cx="878" cy="662" rx="17" ry="13" fill="#1a1a2e"/>
    <circle cx="770" cy="615" r="11" fill="#1a1a2e"/><circle cx="774" cy="610" r="4" fill="#fff"/>
    <ellipse cx="770" cy="660" rx="16" ry="9" fill="#ff9ab0" opacity=".6"/>
  </g>
  <g id="fx" opacity="0"><circle cx="470" cy="720" r="95" fill="#263238"/>
    <g stroke="#ffffff" stroke-width="5" opacity=".85">""" + ''.join(f'<line x1="{x}" y1="660" x2="{x+8}" y2="770"/>' for x in range(400, 540, 20)) + """</g>
    <circle cx="470" cy="720" r="95" fill="none" stroke="#ffca28" stroke-width="16"/>
    <line x1="400" y1="790" x2="330" y2="870" stroke="#ffca28" stroke-width="22" stroke-linecap="round"/></g>""")

OWL = svg(forest_env() + """
  <rect x="-500" y="790" width="2200" height="40" rx="20" fill="#8d5a2b"/>
  <g id="animal">
    <ellipse cx="400" cy="620" rx="50" ry="130" fill="#6d4c41" transform="rotate(12 400 620)"/>
    <ellipse cx="680" cy="620" rx="50" ry="130" fill="#6d4c41" transform="rotate(-12 680 620)"/>
    <ellipse cx="540" cy="610" rx="150" ry="190" fill="#8d6e63"/>
    <ellipse cx="540" cy="660" rx="100" ry="125" fill="#d7ccc8"/>
    <g stroke="#8d6e63" stroke-width="6" fill="none">""" + ''.join(f'<path d="M{x-14} {y} l14 12 l14 -12"/>' for x, y in ((510,620),(570,620),(540,660),(500,700),(580,700),(540,740))) + """</g>
    <g fill="#ffb300"><path d="M480 795 l-14 22 M495 798 l0 24 M510 795 l14 22" stroke="#ffb300" stroke-width="8" stroke-linecap="round"/><path d="M570 795 l-14 22 M585 798 l0 24 M600 795 l14 22" stroke="#ffb300" stroke-width="8" stroke-linecap="round"/></g>
    <g id="head">
      <polygon points="430,410 450,340 485,400" fill="#6d4c41"/><polygon points="650,410 630,340 595,400" fill="#6d4c41"/>
      <circle cx="540" cy="470" r="125" fill="#8d6e63"/>
      <circle cx="485" cy="475" r="68" fill="#efebe9"/><circle cx="595" cy="475" r="68" fill="#efebe9"/>
      <circle cx="485" cy="475" r="40" fill="#ffca28"/><circle cx="595" cy="475" r="40" fill="#ffca28"/>
      <circle cx="485" cy="478" r="20" fill="#1a1a2e"/><circle cx="595" cy="478" r="20" fill="#1a1a2e"/>
      <circle cx="492" cy="470" r="7" fill="#fff"/><circle cx="602" cy="470" r="7" fill="#fff"/>
      <polygon points="525,520 555,520 540,555" fill="#ffa000"/>
    </g>
  </g>""")

PANDA = svg(forest_env() + """
  <g fill="#7cb342">""" + ''.join(f'<rect x="{x}" y="250" width="34" height="700" rx="10"/>' for x in (-260,-180,120,1000,1120,1280)) + """</g>
  <g stroke="#558b2f" stroke-width="6">""" + ''.join(f'<line x1="{x}" y1="{y}" x2="{x+34}" y2="{y}"/>' for x in (-260,-180,120,1000,1120,1280) for y in (400,560,720,880)) + """</g>
  <g id="animal">
    <ellipse cx="420" cy="930" rx="85" ry="60" fill="#212121"/><ellipse cx="660" cy="930" rx="85" ry="60" fill="#212121"/>
    <ellipse cx="540" cy="770" rx="190" ry="175" fill="#fafafa"/>
    <path d="M360 720 Q540 650 720 720 L720 780 Q540 720 360 780 Z" fill="#212121"/>
    <rect x="610" y="520" width="26" height="330" rx="10" fill="#7cb342" transform="rotate(18 623 685)"/>
    <ellipse cx="400" cy="760" rx="55" ry="95" fill="#212121" transform="rotate(25 400 760)"/>
    <ellipse cx="660" cy="720" rx="55" ry="90" fill="#212121" transform="rotate(-35 660 720)"/>
    <circle cx="440" cy="415" r="48" fill="#212121"/><circle cx="640" cy="415" r="48" fill="#212121"/>
    <circle cx="540" cy="520" r="135" fill="#fafafa"/>
    <ellipse cx="488" cy="515" rx="42" ry="30" fill="#212121" transform="rotate(-30 488 515)"/>
    <ellipse cx="592" cy="515" rx="42" ry="30" fill="#212121" transform="rotate(30 592 515)"/>
    <circle cx="495" cy="512" r="11" fill="#fff"/><circle cx="585" cy="512" r="11" fill="#fff"/>
    <circle cx="497" cy="514" r="5" fill="#1a1a2e"/><circle cx="583" cy="514" r="5" fill="#1a1a2e"/>
    <ellipse cx="540" cy="572" rx="22" ry="15" fill="#212121"/>
    <path d="M520 600 q20 16 40 0" stroke="#212121" stroke-width="6" fill="none" stroke-linecap="round"/>
    <ellipse cx="455" cy="580" rx="18" ry="10" fill="#ff9ab0" opacity=".6"/><ellipse cx="625" cy="580" rx="18" ry="10" fill="#ff9ab0" opacity=".6"/>
  </g>
  <g id="fx" opacity="0"><circle cx="700" cy="680" r="50" fill="none" stroke="#ffca28" stroke-width="12"/></g>
  <g id="fx2" opacity="0"><ellipse cx="250" cy="930" rx="70" ry="40" fill="#f8bbd0"/><circle cx="195" cy="905" r="30" fill="#f8bbd0"/>
    <path d="M185 905 q8 6 16 0" stroke="#c2185b" stroke-width="4" fill="none"/></g>""")

KOALA = svg(forest_env() + """
  <rect x="380" y="150" width="110" height="850" rx="40" fill="#a1887f"/>
  <g fill="#7cb342">""" + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="55" ry="20" transform="rotate({r} {x} {y})"/>' for x, y, r in ((330,260,-30),(560,230,25),(300,420,-20),(580,380,30),(320,640,-25))) + """</g>
  <g id="animal">
    <ellipse cx="560" cy="660" rx="120" ry="150" fill="#9e9e9e"/>
    <ellipse cx="575" cy="690" rx="70" ry="100" fill="#e0e0e0"/>
    <path d="M480 600 Q420 610 450 660" stroke="#9e9e9e" stroke-width="40" fill="none" stroke-linecap="round"/>
    <path d="M500 780 Q430 790 455 840" stroke="#9e9e9e" stroke-width="40" fill="none" stroke-linecap="round"/>
    <circle cx="460" cy="400" r="58" fill="#9e9e9e"/><circle cx="660" cy="400" r="58" fill="#9e9e9e"/>
    <circle cx="460" cy="400" r="34" fill="#f5f5f5"/><circle cx="660" cy="400" r="34" fill="#f5f5f5"/>
    <circle cx="560" cy="470" r="100" fill="#9e9e9e"/>
    <ellipse cx="565" cy="495" rx="30" ry="40" fill="#424242"/>
    <circle cx="520" cy="455" r="10" fill="#1a1a2e"/><circle cx="610" cy="455" r="10" fill="#1a1a2e"/>
    <circle cx="523" cy="451" r="3" fill="#fff"/><circle cx="613" cy="451" r="3" fill="#fff"/>
    <ellipse cx="505" cy="500" rx="15" ry="9" fill="#ff9ab0" opacity=".6"/><ellipse cx="625" cy="500" rx="15" ry="9" fill="#ff9ab0" opacity=".6"/>
  </g>""")

SLOTH = svg(forest_env() + """
  <rect x="-500" y="330" width="2200" height="40" rx="20" fill="#8d5a2b"/>
  <g fill="#43a047"><ellipse cx="120" cy="330" rx="70" ry="26"/><ellipse cx="880" cy="330" rx="80" ry="28"/></g>
  <g id="animal">
    <g stroke="#a1887f" stroke-width="34" stroke-linecap="round" fill="none">
      <path d="M400 470 L380 355"/><path d="M470 480 L470 355"/><path d="M620 480 L620 355"/><path d="M690 470 L720 355"/>
    </g>
    <g stroke="#5d4037" stroke-width="7" stroke-linecap="round">""" + ''.join(f'<path d="M{x-10} 352 q10 -22 20 0"/>' for x in (380,470,620,720)) + """</g>
    <ellipse cx="545" cy="500" rx="190" ry="85" fill="#a1887f"/>
    <circle cx="760" cy="540" r="66" fill="#a1887f"/>
    <ellipse cx="770" cy="550" rx="50" ry="40" fill="#efebe9"/>
    <path d="M735 535 q12 -10 28 2" stroke="#4e342e" stroke-width="13" stroke-linecap="round" fill="none"/>
    <path d="M790 537 q12 -10 26 0" stroke="#4e342e" stroke-width="13" stroke-linecap="round" fill="none"/>
    <circle cx="750" cy="537" r="6" fill="#1a1a2e"/><circle cx="802" cy="537" r="6" fill="#1a1a2e"/>
    <ellipse cx="775" cy="560" rx="10" ry="7" fill="#4e342e"/>
    <path d="M758 575 q17 12 34 0" stroke="#4e342e" stroke-width="5" fill="none" stroke-linecap="round"/>
  </g>
  <g id="fx" opacity="0" fill="#66bb6a">""" + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((430,480,16),(500,520,12),(560,470,18),(620,515,14),(680,490,11),(470,540,10),(590,540,12),(735,500,9))) + """</g>
  <g id="fx2" opacity="0">
    <g stroke="#bcaaa4" stroke-width="16" stroke-linecap="round" fill="none"><path d="M520 610 L500 570"/><path d="M600 612 L615 572"/></g>
    <ellipse cx="560" cy="618" rx="72" ry="36" fill="#bcaaa4" stroke="#2b2540" stroke-width="4"/>
    <circle cx="645" cy="625" r="32" fill="#bcaaa4" stroke="#2b2540" stroke-width="4"/>
    <ellipse cx="650" cy="630" rx="24" ry="19" fill="#efebe9"/>
    <path d="M633 624 q7 -6 15 1 M656 624 q7 -6 14 0" stroke="#4e342e" stroke-width="7" stroke-linecap="round" fill="none"/>
    <circle cx="641" cy="625" r="4" fill="#1a1a2e"/><circle cx="663" cy="625" r="4" fill="#1a1a2e"/>
    <path d="M643 641 q8 6 16 0" stroke="#4e342e" stroke-width="3" fill="none" stroke-linecap="round"/>
  </g>""")

def surface_env():
    return SKY_EXTRAS + """
  <rect x="-500" y="640" width="2200" height="500" fill="#29b6f6"/>
  <rect x="-500" y="820" width="2200" height="320" fill="#0288d1" opacity=".55"/>
  <path d="M-500 650 q60 -22 120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0" stroke="#e1f5fe" stroke-width="10" fill="none"/>
  <g fill="#2e7d32" opacity=".8"><path d="M-120 1100 q-30 -200 20 -360 q30 180 -20 360"/><path d="M1180 1100 q-40 -230 10 -400 q40 200 -10 400"/></g>
  <g fill="#ffffff" opacity=".35"><ellipse cx="120" cy="760" rx="60" ry="8"/><ellipse cx="960" cy="800" rx="80" ry="9"/><ellipse cx="300" cy="900" rx="70" ry="8"/></g>"""

def _rings(cx, cy, rx, ry, rot):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#e07b39" transform="rotate({rot} {cx} {cy})"/>'

REDPANDA = svg(forest_env() + """
  <g id="animal">
    <path d="M640 900 C 820 900, 900 800, 870 640 C 860 590, 830 560, 800 560" stroke="#c1440e" stroke-width="110" fill="none" stroke-linecap="round"/>
    <g stroke="#7a2a08" stroke-width="22" fill="none" opacity=".75">
      <path d="M760 855 q30 50 0 95"/><path d="M845 790 q55 20 80 -20"/><path d="M880 700 q55 -5 60 -55"/><path d="M845 610 q40 -35 20 -85"/>
    </g>
    <ellipse cx="420" cy="965" rx="70" ry="38" fill="#3b1a0b"/><ellipse cx="660" cy="965" rx="70" ry="38" fill="#3b1a0b"/>
    <ellipse cx="540" cy="780" rx="190" ry="185" fill="#c1440e"/>
    <ellipse cx="540" cy="820" rx="120" ry="140" fill="#4a2511"/>
    <path d="M420 690 Q380 800 450 900" stroke="#3b1a0b" stroke-width="62" fill="none" stroke-linecap="round"/>
    <path d="M660 690 Q700 800 630 900" stroke="#3b1a0b" stroke-width="62" fill="none" stroke-linecap="round"/>
    <polygon points="400,430 420,320 495,390" fill="#c1440e"/><polygon points="680,430 660,320 585,390" fill="#c1440e"/>
    <polygon points="418,410 428,348 475,392" fill="#fff4e6"/><polygon points="662,410 652,348 605,392" fill="#fff4e6"/>
    <ellipse cx="540" cy="500" rx="165" ry="140" fill="#c1440e"/>
    <ellipse cx="540" cy="565" rx="80" ry="58" fill="#fff4e6"/>
    <ellipse cx="470" cy="455" rx="30" ry="20" fill="#fff4e6"/><ellipse cx="610" cy="455" rx="30" ry="20" fill="#fff4e6"/>
    <path d="M478 500 Q470 560 500 610" stroke="#7a2a08" stroke-width="20" fill="none" stroke-linecap="round"/>
    <path d="M602 500 Q610 560 580 610" stroke="#7a2a08" stroke-width="20" fill="none" stroke-linecap="round"/>
    <circle cx="482" cy="500" r="14" fill="#1a1a2e"/><circle cx="598" cy="500" r="14" fill="#1a1a2e"/>
    <circle cx="487" cy="494" r="5" fill="#fff"/><circle cx="603" cy="494" r="5" fill="#fff"/>
    <ellipse cx="540" cy="545" rx="20" ry="14" fill="#2b1408"/>
    <path d="M522 575 q18 14 36 0" stroke="#2b1408" stroke-width="6" fill="none" stroke-linecap="round"/>
    <ellipse cx="445" cy="560" rx="18" ry="10" fill="#ff9ab0" opacity=".6"/><ellipse cx="635" cy="560" rx="18" ry="10" fill="#ff9ab0" opacity=".6"/>
  </g>
  <g id="fx" opacity="0"><path d="M640 900 C 820 900, 900 800, 870 640 C 860 590, 830 560, 800 560" stroke="#ffca28" stroke-width="20" fill="none" stroke-linecap="round" stroke-dasharray="30 26"/></g>""")

MEERKAT = svg(sand_env() + """
  <ellipse cx="830" cy="985" rx="190" ry="40" fill="#c9a24a"/><ellipse cx="830" cy="975" rx="70" ry="22" fill="#6d4c2f"/>
  <g id="animal">
    <path d="M500 960 Q380 990 300 980" stroke="#b08850" stroke-width="30" fill="none" stroke-linecap="round"/>
    <path d="M300 980 l-30 2" stroke="#3e2723" stroke-width="26" stroke-linecap="round"/>
    <ellipse cx="490" cy="985" rx="60" ry="20" fill="#9c7743"/><ellipse cx="600" cy="985" rx="60" ry="20" fill="#9c7743"/>
    <ellipse cx="510" cy="930" rx="55" ry="70" fill="#c9a26a"/><ellipse cx="580" cy="930" rx="55" ry="70" fill="#c9a26a"/>
    <ellipse cx="545" cy="740" rx="105" ry="230" fill="#d4b07a"/>
    <ellipse cx="555" cy="770" rx="62" ry="170" fill="#f1dcb0"/>
    <g stroke="#a98450" stroke-width="10" fill="none" opacity=".6"><path d="M460 640 q15 10 30 0"/><path d="M455 700 q15 10 30 0"/><path d="M455 760 q15 10 30 0"/></g>
    <path d="M480 610 Q470 680 520 690" stroke="#c9a26a" stroke-width="30" fill="none" stroke-linecap="round"/>
    <path d="M615 610 Q630 680 580 690" stroke="#c9a26a" stroke-width="30" fill="none" stroke-linecap="round"/>
    <circle cx="470" cy="420" r="22" fill="#3e2723"/><circle cx="630" cy="420" r="22" fill="#3e2723"/>
    <ellipse cx="550" cy="470" rx="95" ry="85" fill="#d4b07a"/>
    <ellipse cx="555" cy="520" rx="52" ry="48" fill="#f1dcb0"/>
    <ellipse cx="505" cy="455" rx="30" ry="26" fill="#3e2723" transform="rotate(-15 505 455)"/>
    <ellipse cx="600" cy="455" rx="30" ry="26" fill="#3e2723" transform="rotate(15 600 455)"/>
    <circle cx="507" cy="455" r="14" fill="#f6e6c4"/><circle cx="598" cy="455" r="14" fill="#f6e6c4"/>
    <circle cx="509" cy="457" r="8" fill="#1a1a2e"/><circle cx="596" cy="457" r="8" fill="#1a1a2e"/>
    <circle cx="512" cy="453" r="3" fill="#fff"/><circle cx="599" cy="453" r="3" fill="#fff"/>
    <ellipse cx="555" cy="512" rx="17" ry="12" fill="#2b1d16"/>
    <path d="M540 538 q15 12 30 0" stroke="#2b1d16" stroke-width="5" fill="none" stroke-linecap="round"/>
    <ellipse cx="490" cy="505" rx="14" ry="8" fill="#ff9ab0" opacity=".55"/><ellipse cx="620" cy="505" rx="14" ry="8" fill="#ff9ab0" opacity=".55"/>
  </g>
  <g id="fx" opacity="0" stroke="#ffca28" stroke-width="12" fill="none">
    <ellipse cx="505" cy="455" rx="44" ry="40"/><ellipse cx="600" cy="455" rx="44" ry="40"/>
  </g>""")

def _otter(x, y, s=1.0, flip=False):
    tr = f'translate({x} {y}) scale({-s if flip else s} {s})'
    return f"""<g transform="{tr}">
      <path d="M-230 -10 Q-300 -40 -320 -90" stroke="#5d3a1a" stroke-width="44" fill="none" stroke-linecap="round"/>
      <ellipse cx="-250" cy="-60" rx="34" ry="22" fill="#4e2f14" transform="rotate(-40 -250 -60)"/>
      <ellipse cx="-200" cy="-75" rx="34" ry="22" fill="#4e2f14" transform="rotate(-20 -200 -75)"/>
      <ellipse cx="-20" cy="0" rx="250" ry="95" fill="#6d4524"/>
      <ellipse cx="-10" cy="-30" rx="190" ry="55" fill="#8b5e34"/>
      <ellipse cx="250" cy="-40" rx="95" ry="88" fill="#d9c3a5"/>
      <circle cx="225" cy="-122" r="22" fill="#6d4524"/>
      <ellipse cx="300" cy="-20" rx="42" ry="32" fill="#efe3cf"/>
      <ellipse cx="318" cy="-38" rx="15" ry="11" fill="#2b1d16"/>
      <path d="M296 -2 q16 10 30 -4" stroke="#2b1d16" stroke-width="5" fill="none" stroke-linecap="round"/>
      <circle cx="245" cy="-62" r="11" fill="#1a1a2e"/><circle cx="295" cy="-75" r="11" fill="#1a1a2e"/>
      <circle cx="249" cy="-66" r="4" fill="#fff"/><circle cx="299" cy="-79" r="4" fill="#fff"/>
      <ellipse cx="235" cy="-20" rx="16" ry="9" fill="#ff9ab0" opacity=".6"/>
      <path d="M120 -40 Q90 -110 40 -100" stroke="#5d3a1a" stroke-width="34" fill="none" stroke-linecap="round"/>
      <path d="M140 -20 Q130 -90 80 -95" stroke="#5d3a1a" stroke-width="34" fill="none" stroke-linecap="round"/>
    </g>"""

SEAOTTER = svg(surface_env() + """
  <g id="animal">""" + _otter(370, 660, 1.0) + """
  </g>
  <rect x="-500" y="676" width="2200" height="30" fill="#29b6f6" opacity=".55"/>
  <g id="fx" opacity="0">""" + _otter(965, 680, .5, flip=True) + """
    <path d="M790 600 C 760 570, 740 540, 765 525 C 780 517, 790 530, 790 538 C 790 530, 800 517, 815 525 C 840 540, 820 570, 790 600Z" fill="#ff5c8a"/></g>""")

TITLE = svg(SKY_EXTRAS + ground() + """
  <g fill="#c98d4b"><rect x="230" y="420" width="90" height="560" rx="18"/><rect x="760" y="420" width="90" height="560" rx="18"/></g>
  <rect x="190" y="300" width="700" height="150" rx="40" fill="#2f80ed"/>
  <text x="540" y="400" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="84" fill="#fff">THE ANIMATED ZOO</text>
  <g fill="#ff5c8a"><circle cx="160" cy="300" r="40"/><circle cx="920" cy="300" r="40"/></g><g fill="#ffca28"><circle cx="110" cy="360" r="34"/><circle cx="970" cy="360" r="34"/></g>
  <g stroke="#999" stroke-width="3"><line x1="160" y1="340" x2="270" y2="430"/><line x1="920" y1="340" x2="810" y2="430"/><line x1="110" y1="394" x2="270" y2="440"/><line x1="970" y1="394" x2="810" y2="440"/></g>""")

# --- Nov 2026: gorilla, rhino, harbor seal (ep05 Baby Animals) ---
def _gorilla(x, y, s=1.0):
    """Gorilla in local units, feet at (0,0) before translate. Used big for mom, small for the baby."""
    return f"""<g transform="translate({x} {y}) scale({s})">
      <ellipse cx="-120" cy="-30" rx="80" ry="40" fill="#2b2b33"/><ellipse cx="120" cy="-30" rx="80" ry="40" fill="#2b2b33"/>
      <ellipse cx="0" cy="-260" rx="230" ry="230" fill="#3a3a44"/>
      <ellipse cx="0" cy="-220" rx="140" ry="150" fill="#55555f"/>
      <path d="M-200 -380 Q-300 -220 -250 -40" stroke="#1f1f26" stroke-width="122" fill="none" stroke-linecap="round"/>
      <path d="M200 -380 Q300 -220 250 -40" stroke="#1f1f26" stroke-width="122" fill="none" stroke-linecap="round"/>
      <path d="M-200 -380 Q-300 -220 -250 -40" stroke="#44444f" stroke-width="104" fill="none" stroke-linecap="round"/>
      <path d="M200 -380 Q300 -220 250 -40" stroke="#44444f" stroke-width="104" fill="none" stroke-linecap="round"/>
      <ellipse cx="-250" cy="-25" rx="70" ry="36" fill="#2b2b33"/><ellipse cx="250" cy="-25" rx="70" ry="36" fill="#2b2b33"/>
      <circle cx="-120" cy="-590" r="42" fill="#3a3a44"/><circle cx="120" cy="-590" r="42" fill="#3a3a44"/>
      <circle cx="-120" cy="-590" r="22" fill="#6b5a55"/><circle cx="120" cy="-590" r="22" fill="#6b5a55"/>
      <ellipse cx="0" cy="-610" rx="140" ry="150" fill="#3a3a44"/>
      <ellipse cx="0" cy="-700" rx="95" ry="60" fill="#3a3a44"/>
      <path d="M-100 -620 Q-60 -560 0 -570 Q60 -560 100 -620 Q120 -500 70 -470 Q0 -440 -70 -470 Q-120 -500 -100 -620Z" fill="#8a7468"/>
      <ellipse cx="0" cy="-660" rx="105" ry="38" fill="#8a7468"/>
      <path d="M-95 -690 Q0 -720 95 -690" stroke="#2b2b33" stroke-width="16" fill="none" stroke-linecap="round"/>
      <circle cx="-48" cy="-655" r="17" fill="#1a1a2e"/><circle cx="48" cy="-655" r="17" fill="#1a1a2e"/>
      <circle cx="-42" cy="-661" r="6" fill="#fff"/><circle cx="54" cy="-661" r="6" fill="#fff"/>
      <ellipse cx="-22" cy="-575" rx="14" ry="10" fill="#4a3b35"/><ellipse cx="22" cy="-575" rx="14" ry="10" fill="#4a3b35"/>
      <path d="M-40 -515 q40 28 80 0" stroke="#4a3b35" stroke-width="8" fill="none" stroke-linecap="round"/>
      <ellipse cx="-92" cy="-560" rx="20" ry="11" fill="#ff9ab0" opacity=".55"/><ellipse cx="92" cy="-560" rx="20" ry="11" fill="#ff9ab0" opacity=".55"/>
    </g>"""

GORILLA = svg(forest_env() + """
  <g fill="#66bb6a"><ellipse cx="900" cy="960" rx="150" ry="50"/><ellipse cx="180" cy="965" rx="120" ry="40"/></g>
  <g id="animal">""" + _gorilla(540, 1000, 1.0) + """
  </g>
  <g id="fx" opacity="0">""" + _gorilla(770, 640, .32) + """
    <path d="M700 520 q-40 40 -20 90" stroke="#3a3a44" stroke-width="28" fill="none" stroke-linecap="round"/>
  </g>""")

RHINO = svg(sand_env() + """
  <g id="animal">
    <path d="M250 700 Q215 740 225 800" stroke="#8e9499" stroke-width="12" fill="none" stroke-linecap="round"/>
    <ellipse cx="225" cy="808" rx="10" ry="18" fill="#5f666b"/>
    <g fill="#8e9499">""" + ''.join(f'<rect x="{x}" y="790" width="82" height="205" rx="30"/>' for x in (300,390,580,670)) + """</g>
    <g fill="#6f777c">""" + ''.join(f'<ellipse cx="{x+41}" cy="990" rx="48" ry="16"/>' for x in (300,390,580,670)) + """</g>
    <ellipse cx="500" cy="720" rx="270" ry="160" fill="#a3a9ad"/>
    <path d="M330 640 q40 -30 80 0 M560 610 q40 -30 80 0" stroke="#8e9499" stroke-width="10" fill="none" stroke-linecap="round"/>
    <ellipse cx="760" cy="690" rx="150" ry="115" fill="#a3a9ad"/>
    <ellipse cx="880" cy="740" rx="110" ry="80" fill="#b5bbbe"/>
    <path id="horn" d="M900 680 Q950 560 925 470 Q895 560 850 670Z" fill="#e8dcc4"/>
    <path d="M820 640 Q845 590 835 550 Q815 590 795 640Z" fill="#e8dcc4"/>
    <polygon points="680,600 700,520 735,590" fill="#a3a9ad"/><polygon points="760,585 790,510 810,585" fill="#a3a9ad"/>
    <polygon points="692,592 703,548 722,588" fill="#e3a3a8"/><polygon points="772,580 789,538 800,580" fill="#e3a3a8"/>
    <circle cx="760" cy="660" r="13" fill="#1a1a2e"/><circle cx="765" cy="655" r="5" fill="#fff"/>
    <ellipse cx="935" cy="745" rx="9" ry="13" fill="#5f666b"/>
    <path d="M860 790 q45 22 90 0" stroke="#5f666b" stroke-width="7" fill="none" stroke-linecap="round"/>
    <ellipse cx="790" cy="720" rx="20" ry="11" fill="#ff9ab0" opacity=".55"/>
  </g>
  <g id="fx" opacity="0">
    <path d="M900 680 Q950 560 925 470 Q895 560 850 670Z" fill="none" stroke="#ffca28" stroke-width="14" stroke-linejoin="round"/>
    <g fill="#ffca28"><circle cx="985" cy="500" r="12"/><circle cx="870" cy="470" r="9"/><circle cx="990" cy="600" r="8"/></g>
  </g>
  <g id="fx2" opacity="0">
    <g transform="translate(-110 582) scale(.42)">
      <g fill="#a9b0b4">""" + ''.join(f'<rect x="{x}" y="790" width="82" height="205" rx="30"/>' for x in (300,390,580,670)) + """</g>
      <ellipse cx="500" cy="720" rx="270" ry="160" fill="#b9bfc2"/><ellipse cx="760" cy="690" rx="150" ry="115" fill="#b9bfc2"/>
      <ellipse cx="880" cy="740" rx="110" ry="80" fill="#c8cdd0"/>
      <path d="M890 680 Q910 640 900 610 Q880 640 860 675Z" fill="#efe6d4"/>
      <polygon points="680,600 700,520 735,590" fill="#b9bfc2"/><polygon points="760,585 790,510 810,585" fill="#b9bfc2"/>
      <circle cx="760" cy="660" r="16" fill="#1a1a2e"/><circle cx="766" cy="654" r="6" fill="#fff"/>
      <path d="M860 790 q45 22 90 0" stroke="#5f666b" stroke-width="8" fill="none" stroke-linecap="round"/>
    </g>
  </g>""")

def shore_env():
    return SKY_EXTRAS + """
  <rect x="-500" y="700" width="2200" height="450" fill="#29b6f6"/>
  <rect x="-500" y="860" width="2200" height="300" fill="#0288d1" opacity=".5"/>
  <path d="M-500 710 q60 -22 120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0" stroke="#e1f5fe" stroke-width="10" fill="none"/>
  <path d="M120 1000 Q160 820 330 800 Q520 770 700 800 Q880 820 960 1000 Z" fill="#8d8a86"/>
  <path d="M170 980 Q210 850 340 830 Q520 805 690 830 Q850 850 910 980 Z" fill="#a8a5a0"/>
  <rect x="-500" y="990" width="2200" height="120" fill="#0288d1"/>
  <g fill="#ffffff" opacity=".35"><ellipse cx="-200" cy="780" rx="60" ry="8"/><ellipse cx="1150" cy="820" rx="80" ry="9"/></g>"""

def _seal(x, y, s=1.0, body="#9aa7b0", belly="#c7d0d6", spots="#6f7d87"):
    return f"""<g transform="translate({x} {y}) scale({s})">
      <path d="M-300 -20 Q-380 -30 -420 -90 M-300 -20 Q-390 10 -440 -10" stroke="{spots}" stroke-width="40" fill="none" stroke-linecap="round"/>
      <ellipse cx="-60" cy="-70" rx="270" ry="85" fill="{body}"/>
      <ellipse cx="-40" cy="-40" rx="220" ry="45" fill="{belly}"/>
      <g fill="{spots}" opacity=".7"><circle cx="-180" cy="-110" r="12"/><circle cx="-110" cy="-125" r="9"/><circle cx="-40" cy="-115" r="11"/><circle cx="-230" cy="-80" r="8"/><circle cx="40" cy="-120" r="8"/></g>
      <ellipse cx="200" cy="-150" rx="115" ry="105" fill="{body}"/>
      <ellipse cx="270" cy="-120" rx="60" ry="45" fill="{belly}"/>
      <ellipse cx="300" cy="-140" rx="15" ry="11" fill="#2b2b33"/>
      <g stroke="#ffffff" stroke-width="4" opacity=".9"><line x1="280" y1="-112" x2="340" y2="-125"/><line x1="280" y1="-104" x2="342" y2="-100"/><line x1="240" y1="-112" x2="188" y2="-125"/><line x1="240" y1="-104" x2="186" y2="-98"/></g>
      <path d="M265 -98 q18 12 36 0" stroke="#2b2b33" stroke-width="5" fill="none" stroke-linecap="round"/>
      <circle cx="185" cy="-180" r="18" fill="#1a1a2e"/><circle cx="265" cy="-185" r="18" fill="#1a1a2e"/>
      <circle cx="191" cy="-187" r="6" fill="#fff"/><circle cx="271" cy="-192" r="6" fill="#fff"/>
      <ellipse cx="160" cy="-130" rx="18" ry="10" fill="#ff9ab0" opacity=".55"/>
      <path d="M60 -40 Q110 0 70 30" stroke="{spots}" stroke-width="34" fill="none" stroke-linecap="round"/>
    </g>"""

SEAL = svg(shore_env() + """
  <g id="animal">""" + _seal(560, 860, 1.0) + """
  </g>
  <g id="fx" opacity="0">""" + _seal(1050, 930, .42, body="#d9dfe3", belly="#f1f4f6", spots="#aab5bc") + """
    <g fill="none" stroke="#e1f5fe" stroke-width="5"><circle cx="1190" cy="830" r="12"/><circle cx="1215" cy="790" r="8"/></g>
  </g>""")

SCENES2 = {"lion": LION, "zebra": ZEBRA, "hippo": HIPPO, "monkey": MONKEY, "flamingo": FLAMINGO,
           "kangaroo": KANGAROO, "octopus": OCTOPUS, "turtle": TURTLE, "polarbear": POLARBEAR,
           "owl": OWL, "panda": PANDA, "koala": KOALA, "sloth": SLOTH, "title": TITLE,
           "redpanda": REDPANDA, "meerkat": MEERKAT, "seaotter": SEAOTTER,
           "gorilla": GORILLA, "rhino": RHINO, "seal": SEAL}
