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
  <g id="fx" opacity="0" fill="#66bb6a">""" + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((430,480,16),(500,520,12),(560,470,18),(620,515,14),(680,490,11),(470,540,10),(590,540,12),(735,500,9))) + """</g>""")

TITLE = svg(SKY_EXTRAS + ground() + """
  <g fill="#c98d4b"><rect x="230" y="420" width="90" height="560" rx="18"/><rect x="760" y="420" width="90" height="560" rx="18"/></g>
  <rect x="190" y="300" width="700" height="150" rx="40" fill="#2f80ed"/>
  <text x="540" y="400" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="84" fill="#fff">THE ANIMATED ZOO</text>
  <g fill="#ff5c8a"><circle cx="160" cy="300" r="40"/><circle cx="920" cy="300" r="40"/></g><g fill="#ffca28"><circle cx="110" cy="360" r="34"/><circle cx="970" cy="360" r="34"/></g>
  <g stroke="#999" stroke-width="3"><line x1="160" y1="340" x2="270" y2="430"/><line x1="920" y1="340" x2="810" y2="430"/><line x1="110" y1="394" x2="270" y2="440"/><line x1="970" y1="394" x2="810" y2="440"/></g>""")

SCENES2 = {"lion": LION, "zebra": ZEBRA, "hippo": HIPPO, "monkey": MONKEY, "flamingo": FLAMINGO,
           "kangaroo": KANGAROO, "octopus": OCTOPUS, "turtle": TURTLE, "polarbear": POLARBEAR,
           "owl": OWL, "panda": PANDA, "koala": KOALA, "sloth": SLOTH, "title": TITLE}
