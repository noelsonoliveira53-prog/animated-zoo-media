"""Original space art for Space Kids Academy: cartoon planets with faces, in the shared 1080x1100 frame."""
import math

def _rnd(n, s):
    x = math.sin(n * 12.9898 + s * 78.233) * 43758.5453
    return x - math.floor(x)

def svg(body):
    return f'<svg viewBox="0 0 1080 1100" width="1080" height="1100">{body}</svg>'

def space_env():
    stars = "".join(f'<circle cx="{-480 + 2040*_rnd(i,1):.0f}" cy="{1100*_rnd(i,2):.0f}" r="{1.2 + 3*_rnd(i,3):.1f}" fill="#fff" opacity="{.35 + .65*_rnd(i,4):.2f}"/>' for i in range(110))
    return f"""<defs><radialGradient id="spbg" cx="50%" cy="40%" r="80%"><stop offset="0" stop-color="#28328a"/><stop offset="1" stop-color="#090d2b"/></radialGradient></defs>
  <g>{stars}</g>
  <ellipse cx="1330" cy="200" rx="90" ry="22" fill="none" stroke="#c39bff" stroke-width="8" opacity=".7"/><circle cx="1330" cy="200" r="42" fill="#9c7bff" opacity=".85"/>
  <circle cx="-260" cy="860" r="70" fill="#8fa3c8" opacity=".55"/><circle cx="-280" cy="840" r="12" fill="#6f84ad" opacity=".55"/>"""

def face(cx, cy, s=1.0, smile="#5b3a1a"):
    ex = 62 * s
    return (f'<circle cx="{cx-ex:.0f}" cy="{cy:.0f}" r="{24*s:.0f}" fill="#fff"/><circle cx="{cx+ex:.0f}" cy="{cy:.0f}" r="{24*s:.0f}" fill="#fff"/>'
            f'<circle cx="{cx-ex+3:.0f}" cy="{cy+2:.0f}" r="{12*s:.0f}" fill="#1a1a2e"/><circle cx="{cx+ex+3:.0f}" cy="{cy+2:.0f}" r="{12*s:.0f}" fill="#1a1a2e"/>'
            f'<circle cx="{cx-ex+7*s:.0f}" cy="{cy-4*s:.0f}" r="{max(3,4*s):.0f}" fill="#fff"/><circle cx="{cx+ex+7*s:.0f}" cy="{cy-4*s:.0f}" r="{max(3,4*s):.0f}" fill="#fff"/>'
            f'<path d="M{cx-34*s:.0f} {cy+46*s:.0f} q{34*s:.0f} {30*s:.0f} {68*s:.0f} 0" stroke="{smile}" stroke-width="{8*s:.0f}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{cx-ex-30*s:.0f}" cy="{cy+40*s:.0f}" rx="{20*s:.0f}" ry="{11*s:.0f}" fill="#ff8fab" opacity=".6"/>'
            f'<ellipse cx="{cx+ex+30*s:.0f}" cy="{cy+40*s:.0f}" rx="{20*s:.0f}" ry="{11*s:.0f}" fill="#ff8fab" opacity=".6"/>')

def grad(id_, a, b):
    return f'<defs><radialGradient id="{id_}" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></radialGradient></defs>'

EARTH_MINI = ('<circle cx="0" cy="0" r="34" fill="#3d8bfd"/><path d="M-20 -10 q10 -14 22 -4 q8 10 -4 16 q-14 4 -18 -12z" fill="#4caf50"/>'
              '<path d="M8 12 q10 -2 14 6 q-6 10 -16 4z" fill="#4caf50"/>')

VENUS = svg(space_env() + grad("vg", "#ffe3a3", "#e39a37") + """
  <defs><clipPath id="vclip"><circle cx="540" cy="540" r="300"/></clipPath></defs>
  <g id="animal">
    <circle cx="540" cy="540" r="300" fill="url(#vg)"/>
    <g clip-path="url(#vclip)" stroke="#fff1c9" stroke-width="30" fill="none" opacity=".45" stroke-linecap="round">
      <path d="M200 380 q160 -40 340 0 t360 0"/><path d="M200 470 q180 40 360 0 t340 0"/><path d="M200 650 q160 -40 340 0 t360 0"/><path d="M200 740 q180 40 360 0 t340 0"/></g>
    """ + face(540, 520, 1.55) + """
  </g>
  <g id="fx" opacity="0"><path d="M820 290 A 390 390 0 0 0 260 290" stroke="#7ef9ff" stroke-width="16" fill="none" stroke-dasharray="34 22" stroke-linecap="round"/>
    <path d="M262 250 l-52 52 l72 14 z" fill="#7ef9ff"/></g>""")

JUPITER = svg(space_env() + grad("jg", "#f6dcb8", "#c98b55") + """
  <defs><clipPath id="jclip"><circle cx="540" cy="540" r="330"/></clipPath></defs>
  <g id="animal">
    <circle cx="540" cy="540" r="330" fill="url(#jg)"/>
    <g clip-path="url(#jclip)">
      <rect x="200" y="300" width="700" height="44" fill="#b8703f" opacity=".7"/><rect x="200" y="370" width="700" height="26" fill="#e9c69c"/>
      <rect x="200" y="660" width="700" height="54" fill="#b8703f" opacity=".75"/><rect x="200" y="740" width="700" height="30" fill="#d79a62"/>
      <rect x="200" y="800" width="700" height="40" fill="#a65f33" opacity=".7"/>
      <ellipse cx="700" cy="690" rx="92" ry="52" fill="#d0553f"/><ellipse cx="700" cy="690" rx="58" ry="30" fill="#e2775f"/></g>
    """ + face(480, 500, 1.45) + """
  </g>
  <g id="fx" opacity="0"><ellipse cx="700" cy="690" rx="120" ry="78" fill="none" stroke="#ffeb3b" stroke-width="12" stroke-dasharray="26 16"/></g>
  <g id="fx2" opacity="0"><g transform="translate(700 690)">""" + EARTH_MINI + """</g></g>""")

SATURN = svg(space_env() + grad("sg", "#fbe9b7", "#d8b56a") + """
  <defs><clipPath id="stop"><rect x="-500" y="-10" width="2200" height="560"/></clipPath><clipPath id="sbot"><rect x="-500" y="550" width="2200" height="700"/></clipPath>
  <clipPath id="sclip"><circle cx="540" cy="540" r="235"/></clipPath></defs>
  <g id="fx" opacity="0">
    <rect x="110" y="700" width="860" height="270" rx="70" fill="#ffffff" stroke="#b0bec5" stroke-width="10"/>
    <rect x="140" y="760" width="800" height="180" rx="50" fill="#4fc3f7"/>
    <g fill="none" stroke="#e1f5fe" stroke-width="6"><circle cx="230" cy="740" r="18"/><circle cx="270" cy="700" r="11"/><circle cx="860" cy="730" r="15"/></g>
    <rect x="170" y="960" width="30" height="50" rx="10" fill="#b0bec5"/><rect x="880" y="960" width="30" height="50" rx="10" fill="#b0bec5"/>
  </g>
  <g id="animal">
    <g clip-path="url(#stop)" fill="none"><ellipse cx="540" cy="550" rx="450" ry="112" stroke="#eadbb0" stroke-width="40"/><ellipse cx="540" cy="550" rx="370" ry="90" stroke="#c7ae74" stroke-width="18"/></g>
    <circle cx="540" cy="540" r="235" fill="url(#sg)"/>
    <g clip-path="url(#sclip)"><rect x="300" y="390" width="480" height="34" fill="#e8cc8a" opacity=".8"/><rect x="300" y="650" width="480" height="40" fill="#c9a35c" opacity=".7"/></g>
    """ + face(540, 505, 1.2) + """
    <g clip-path="url(#sbot)" fill="none"><ellipse cx="540" cy="550" rx="450" ry="112" stroke="#eadbb0" stroke-width="40"/><ellipse cx="540" cy="550" rx="370" ry="90" stroke="#c7ae74" stroke-width="18"/></g>
  </g>
  <g id="fx2" opacity="0"><rect x="140" y="760" width="800" height="70" rx="30" fill="#4fc3f7" opacity=".55"/></g>""")

MOON = svg(space_env() + grad("mg", "#eef2f5", "#9aa9b5") + """
  <g id="animal">
    <circle cx="540" cy="540" r="300" fill="url(#mg)"/>
    <g fill="#8796a3" opacity=".55"><circle cx="380" cy="380" r="46"/><circle cx="700" cy="350" r="30"/><circle cx="740" cy="700" r="56"/><circle cx="360" cy="720" r="34"/><circle cx="560" cy="300" r="20"/></g>
    """ + face(540, 520, 1.5, "#5d6b78") + """
  </g>
  <g id="fx" opacity="0" fill="#5d6b78">""" + "".join(
      f'<ellipse cx="{300 + i*70}" cy="{790 + (i % 2)*26}" rx="14" ry="24" transform="rotate(-20 {300 + i*70} {790 + (i % 2)*26})"/>' for i in range(7)) + """</g>""")

MERCURY = svg(space_env() + grad("hg", "#d9c3a8", "#8d7259") + """
  <defs><radialGradient id="sun" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff59d"/><stop offset=".6" stop-color="#ffb300"/><stop offset="1" stop-color="#ff7043" stop-opacity="0"/></radialGradient></defs>
  <circle cx="-180" cy="560" r="460" fill="url(#sun)"/>
  <g id="fx" opacity="0"><ellipse cx="-180" cy="560" rx="720" ry="300" fill="none" stroke="#ffe082" stroke-width="8" stroke-dasharray="24 18"/></g>
  <g id="animal">
    <circle cx="540" cy="560" r="200" fill="url(#hg)"/>
    <g fill="#7a5f47" opacity=".55"><circle cx="440" cy="460" r="30"/><circle cx="640" cy="470" r="20"/><circle cx="620" cy="680" r="34"/><circle cx="450" cy="680" r="18"/></g>
    """ + face(540, 550, 1.0, "#4a3626") + """
  </g>""")

MARS = svg(space_env() + grad("rg", "#ff9a6b", "#b7432b") + """
  <defs><clipPath id="rclip"><circle cx="540" cy="540" r="290"/></clipPath></defs>
  <g id="animal">
    <circle cx="540" cy="540" r="290" fill="url(#rg)"/>
    <g clip-path="url(#rclip)"><ellipse cx="540" cy="262" rx="150" ry="40" fill="#fff4ef"/><ellipse cx="540" cy="820" rx="120" ry="30" fill="#ffe5dc"/>
      <path d="M300 640 q80 -40 150 10 t140 0" fill="#a33a24" opacity=".5"/><circle cx="740" cy="430" r="46" fill="#a33a24" opacity=".45"/></g>
    """ + face(540, 520, 1.45, "#6b1f10") + """
  </g>
  <g id="fx" opacity="0" fill="#ffcc80">""" + "".join(
      f'<path d="M{360 + 360*_rnd(i,7):.0f} {360 + 360*_rnd(i,8):.0f} l6 -16 6 16 16 6 -16 6 -6 16 -6 -16 -16 -6z"/>' for i in range(9)) + """</g>""")

SUN = svg(space_env() + """
  <defs><radialGradient id="sung" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#fff59d"/><stop offset=".7" stop-color="#ffb300"/><stop offset="1" stop-color="#ff8f00"/></radialGradient></defs>
  <g id="animal">
    <g fill="#ffcc4d">""" + "".join(
      f'<polygon points="{540 + 360*math.cos(a):.0f},{540 + 360*math.sin(a):.0f} {540 + 300*math.cos(a+.12):.0f},{540 + 300*math.sin(a+.12):.0f} {540 + 300*math.cos(a-.12):.0f},{540 + 300*math.sin(a-.12):.0f}"/>'
      for a in [i * math.pi / 8 for i in range(16)]) + """</g>
    <circle cx="540" cy="540" r="300" fill="url(#sung)"/>
    """ + face(540, 520, 1.5, "#8a4b00") + """
  </g>
  <g id="fx" opacity="0"><g transform="translate(930 860) scale(.35)">""" + EARTH_MINI + """</g>
    <path d="M900 830 L870 800" stroke="#fff" stroke-width="5"/></g>""")

SPACE_TITLE = svg(space_env() + """
  <g transform="translate(-130 -40)">
    <rect x="160" y="230" width="760" height="150" rx="44" fill="#6c4cd6"/>
    <text x="540" y="330" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="74" fill="#fff">SPACE KIDS ACADEMY</text>
    <path d="M540 470 q70 80 70 260 l-140 0 q0 -180 70 -260z" fill="#f3f6ff" stroke="#9aa7c7" stroke-width="6"/>
    <path d="M540 470 q40 46 56 110 l-112 0 q16 -64 56 -110z" fill="#e23d4b"/>
    <circle cx="540" cy="640" r="30" fill="#7ef9ff" stroke="#9aa7c7" stroke-width="8"/>
    <path d="M470 700 l-50 70 l50 0z" fill="#e23d4b"/><path d="M610 700 l50 70 l-50 0z" fill="#e23d4b"/>
    <path d="M495 740 q45 120 90 0z" fill="#ff9f1c"/><path d="M515 740 q25 70 50 0z" fill="#ffe066"/>
    <rect x="300" y="900" width="480" height="30" rx="12" fill="#3a4170"/>
  </g>""")

SCENES3 = {"venus": VENUS, "jupiter": JUPITER, "saturn": SATURN, "moon": MOON, "mercury": MERCURY,
           "mars": MARS, "sun": SUN}
PLANETS = set(SCENES3)
