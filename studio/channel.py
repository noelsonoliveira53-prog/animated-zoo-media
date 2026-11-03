"""Per-channel settings for the shared video engine. Pick with env CHANNEL=zoo|space."""
import os

NOVA = """<svg id="milo" viewBox="0 0 220 200" width="260" height="236">
  <line x1="110" y1="42" x2="110" y2="18" stroke="#9aa7c7" stroke-width="6" stroke-linecap="round"/>
  <circle cx="110" cy="14" r="11" fill="#ffd23f"/><circle cx="106" cy="10" r="3.5" fill="#fff8d6"/>
  <g id="wing"><path d="M86 166 q9 30 18 0 z" fill="#ff9f1c"/><path d="M116 166 q9 30 18 0 z" fill="#ff9f1c"/>
    <path d="M90 166 q5 16 10 0 z" fill="#ffe066"/><path d="M120 166 q5 16 10 0 z" fill="#ffe066"/></g>
  <rect x="78" y="148" width="64" height="22" rx="10" fill="#c5cee6"/>
  <rect x="16" y="90" width="36" height="18" rx="9" fill="#e3e9f7" stroke="#9aa7c7" stroke-width="4"/>
  <rect x="168" y="90" width="36" height="18" rx="9" fill="#e3e9f7" stroke="#9aa7c7" stroke-width="4"/>
  <rect x="40" y="36" width="140" height="122" rx="52" fill="#f3f6ff" stroke="#9aa7c7" stroke-width="5"/>
  <rect x="58" y="58" width="104" height="72" rx="30" fill="#1b2a5e"/>
  <ellipse class="mpupil" cx="88" cy="89" rx="11" ry="14" fill="#7ef9ff"/>
  <ellipse class="mpupil" cx="132" cy="89" rx="11" ry="14" fill="#7ef9ff"/>
  <circle class="glint" cx="92" cy="84" r="3.5" fill="#fff"/><circle class="glint" cx="136" cy="84" r="3.5" fill="#fff"/>
  <path d="M97 110 q13 9 26 0" stroke="#7ef9ff" stroke-width="5" fill="none" stroke-linecap="round"/>
  <ellipse id="beaklow" cx="110" cy="117" rx="8" ry="2.2" fill="#7ef9ff"/>
  <circle cx="64" cy="140" r="7" fill="#ff9ab0" opacity=".7"/><circle cx="156" cy="140" r="7" fill="#ff9ab0" opacity=".7"/>
  <path d="M110 140 l4 8 9 1 -7 6 2 9 -8 -5 -8 5 2 -9 -7 -6 9 -1z" fill="#ffd23f" transform="translate(0 -6) scale(.8) translate(28 40)"/>
</svg>"""

SHOOTING_STAR = ('<svg id="birds" width="220" height="80" viewBox="0 0 220 80" style="position:absolute;left:-260px;top:110px">'
                 '<defs><linearGradient id="trail" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient></defs>'
                 '<path d="M0 60 L180 22" stroke="url(#trail)" stroke-width="6" stroke-linecap="round"/>'
                 '<path d="M190 20 l5 -11 5 11 11 5 -11 5 -5 11 -5 -11 -11 -5z" fill="#fff59d"/></svg>')

DASH = """<svg id="milo" viewBox="0 0 220 200" width="260" height="236">
  <g id="wing"><path d="M70 160 Q30 160 8 120 Q40 140 78 140Z" fill="#5fb848"/></g>
  <ellipse cx="88" cy="190" rx="18" ry="8" fill="#4a9a37"/><ellipse cx="132" cy="190" rx="18" ry="8" fill="#4a9a37"/>
  <ellipse cx="110" cy="158" rx="50" ry="36" fill="#7ccf5b"/><ellipse cx="110" cy="166" rx="30" ry="22" fill="#d9f7b0"/>
  <g fill="#ffb74d"><path d="M84 36 l10 -22 10 22z"/><path d="M104 30 l10 -24 10 24z"/><path d="M124 36 l10 -22 10 22z"/></g>
  <circle cx="110" cy="88" r="58" fill="#7ccf5b"/>
  <circle cx="88" cy="80" r="17" fill="#fff"/><circle cx="132" cy="80" r="17" fill="#fff"/>
  <ellipse class="mpupil" cx="91" cy="82" rx="8" ry="10" fill="#1a1a2e"/><ellipse class="mpupil" cx="135" cy="82" rx="8" ry="10" fill="#1a1a2e"/>
  <circle class="glint" cx="94" cy="77" r="3.5" fill="#fff"/><circle class="glint" cx="138" cy="77" r="3.5" fill="#fff"/>
  <path d="M96 106 q14 10 28 0" stroke="#2e6b20" stroke-width="5" fill="none" stroke-linecap="round"/>
  <ellipse id="beaklow" cx="110" cy="117" rx="8" ry="2.2" fill="#7a2e2e"/>
  <circle cx="70" cy="104" r="8" fill="#ff9ab0" opacity=".7"/><circle cx="150" cy="104" r="8" fill="#ff9ab0" opacity=".7"/>
</svg>"""

PIP = """<svg id="milo" viewBox="0 0 220 200" width="260" height="236">
  <circle cx="58" cy="44" r="34" fill="#b08968"/><circle cx="58" cy="44" r="20" fill="#f4c7c3"/>
  <circle cx="162" cy="44" r="34" fill="#b08968"/><circle cx="162" cy="44" r="20" fill="#f4c7c3"/>
  <ellipse cx="110" cy="168" rx="46" ry="30" fill="#c49a6c"/>
  <circle cx="110" cy="96" r="62" fill="#c49a6c"/><ellipse cx="110" cy="112" rx="34" ry="24" fill="#f1dcc2"/>
  <path d="M70 44 Q110 0 150 44Z" fill="#7cb342"/><rect x="62" y="40" width="96" height="10" rx="5" fill="#558b2f"/>
  <circle cx="88" cy="88" r="15" fill="#fff"/><circle cx="132" cy="88" r="15" fill="#fff"/>
  <ellipse class="mpupil" cx="90" cy="90" rx="7.5" ry="9.5" fill="#1a1a2e"/><ellipse class="mpupil" cx="134" cy="90" rx="7.5" ry="9.5" fill="#1a1a2e"/>
  <circle class="glint" cx="93" cy="85" r="3.5" fill="#fff"/><circle class="glint" cx="137" cy="85" r="3.5" fill="#fff"/>
  <ellipse cx="110" cy="104" rx="8" ry="6" fill="#e57373"/>
  <g stroke="#8d6e63" stroke-width="3" stroke-linecap="round"><line x1="70" y1="106" x2="40" y2="100"/><line x1="70" y1="114" x2="40" y2="118"/><line x1="150" y1="106" x2="180" y2="100"/><line x1="150" y1="114" x2="180" y2="118"/></g>
  <ellipse id="beaklow" cx="110" cy="117" rx="7" ry="2.2" fill="#6d2e2e"/>
  <g id="wing"><line x1="168" y1="178" x2="196" y2="150" stroke="#8d6e63" stroke-width="8" stroke-linecap="round"/>
    <circle cx="204" cy="140" r="16" fill="#e1f5fe" stroke="#8d6e63" stroke-width="6"/></g>
</svg>"""

GIZMO = (NOVA.replace('fill="#f3f6ff" stroke="#9aa7c7"', 'fill="#d9dee8" stroke="#8792a8"')
         .replace('<circle cx="110" cy="14" r="11" fill="#ffd23f"/><circle cx="106" cy="10" r="3.5" fill="#fff8d6"/>',
                  '<circle cx="110" cy="14" r="11" fill="#5ff3ff"/><circle cx="106" cy="10" r="3.5" fill="#e6ffff"/>')
         .replace('fill="#ffd23f" transform=', 'fill="#5ff3ff" transform='))

def _tail(total, even=False):
    r = int(total / .3)
    if even: r = r // 2 * 2 - 1
    return f'tl.to("#wing",{{rotation:-14,svgOrigin:"74 150",duration:.3,yoyo:true,repeat:{r},ease:"sine.inOut"}},0);'

def _glass(total, even=False):
    r = int(total / .45)
    if even: r = r // 2 * 2 - 1
    return f'tl.to("#wing",{{rotation:-16,svgOrigin:"168 178",duration:.45,yoyo:true,repeat:{r},ease:"sine.inOut"}},0);'

def _milo_wing(total, even=False):
    r = int(total / .18)
    if even: r = r // 2 * 2 - 1
    return f'tl.to("#wing",{{rotation:-28,svgOrigin:"78 122",duration:.18,yoyo:true,repeat:{r},ease:"sine.inOut"}},0);'

def _flame(total, even=False):
    r = int(total / .12)
    if even: r = r // 2 * 2 - 1
    return f'tl.to("#wing",{{scaleY:.55,svgOrigin:"110 166",duration:.12,yoyo:true,repeat:{r},ease:"sine.inOut"}},0);'

CONFIGS = {
    "zoo": dict(brand="THE ANIMATED ZOO", host=None, voice="af_heart", talk="rot",
                kind="💙 Be kind!", bye="See you at the zoo! 💙", wing=_milo_wing, birds_html=None,
                root_bg="linear-gradient(180deg,#8fd3ff,#e3f5ff)", brand_color="#1c5fc4", repo_prefix=""),
    "space": dict(brand="SPACE KIDS ACADEMY", host=NOVA, voice="af_nova", talk="scale",
                  kind="🚀 Great job!", bye="See you in space! 🚀", wing=_flame, birds_html=SHOOTING_STAR,
                  root_bg="radial-gradient(ellipse at 50% 42%,#28328a 0%,#141a4f 45%,#090d2b 100%)", brand_color="#a9b8ff", repo_prefix="space/"),
    "gizmo": dict(brand="GIZMO EXPLAINS", host=GIZMO, voice="am_michael", talk="scale",
                  kind="🤖 Great job!", bye="See you next time! 🤖", wing=_flame, birds_html=SHOOTING_STAR,
                  root_bg="radial-gradient(ellipse at 50% 42%,#3561d9 0%,#1d3a8a 50%,#0d1b4a 100%)", brand_color="#5ff3ff", repo_prefix="gizmo/"),
    "dino": dict(brand="DINO WORLD KIDS", host=DASH, voice="af_sky", talk="scale",
                 kind="🦕 Be gentle!", bye="See you in Dino World! 🦕", wing=_tail, birds_html=None,
                 root_bg="linear-gradient(180deg,#ffcc9a 0%,#ffe9c7 55%,#fff4dc 100%)", brand_color="#8d4a1a", repo_prefix="dino/"),
    "wild": dict(brand="WILDKIDS DISCOVERY", host=PIP, voice="bf_emma", talk="scale",
                 kind="🐞 Be gentle!", bye="See you outside, explorers! 🌼", wing=_glass, birds_html=None,
                 root_bg="linear-gradient(180deg,#9fe3ff 0%,#e3f7ff 70%)", brand_color="#2e7d32", repo_prefix="wild/"),
}
NAME = os.environ.get("CHANNEL", "zoo")
C = CONFIGS[NAME]
