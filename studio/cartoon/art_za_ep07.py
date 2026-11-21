"""Pictures for za_ep07 "Sandy and the Flying Scarf" (Nov 19 2026). New props only: no character, place or older prop is drawn differently.
Registers kit.PT["camel"] (where the parts of a grown camel are, the same numbers zc_ep01 carries as CAMEL_PT), so K.P / K.C work on Mama camel.

  scarf(p)        Milo's red scarf on its own (it flies away in the wind): a band with a knot, two ends and fringes. Anchored at its middle.
                  Parts: #<p>-band (flutters), #<p>-endL / -endR (wave).
  bush_scarf(p)   a thorny bush (art._thorn) with the red scarf caught on its top. Anchored at the bush's foot.
  rock(p)         a big round desert rock to rest beside (out of the wind). Anchored at its foot, middle.
  shut_eyes(p)    two closed eyes drawn over Milo's own eyes, in Milo's units: put it at Milo's feet with Milo's scale (he keeps his eyes shut
                  while the sand blows; the film's idle blink would open them again, so the lids are a prop on top). Anchored like Milo.
  wind_lines(p)   a few long white wind curls for the sky. Anchored at the middle.
"""
import art, kit

SC, SC_D, SC_L = art.SCARF, art.SCARF_D, "#ff6b78"
kit.PT.setdefault("camel", {"head": (345, -600), "eye": (352, -612), "nose": (452, -594), "mouth": (440, -548), "top": (345, -690), "back": (0, -440),
                            "body": (0, -322), "feet": (0, 0), "all": (80, -360), "legs": (10, -130)})
kit.BOX.setdefault("camel", (-340, 490, -700))


def scarf(p):
    fr = "".join(f'<path d="M{x} 0 l{d} 26" stroke="{SC_D}" stroke-width="7" stroke-linecap="round"/>' for x, d in ((-8, -4), (6, 0), (20, 4)))
    endL = (f'<g id="{p}-endL"><path d="M-40 -6 C-90 -10 -130 10 -170 0 L-176 30 C-136 40 -96 22 -44 26Z" fill="{SC}" stroke="{SC_D}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M-90 -2 L-94 30 M-128 4 L-132 34" stroke="{SC_L}" stroke-width="8" stroke-linecap="round"/>'
            f'<g transform="translate(-186 2) rotate(10)">{fr}</g></g>')
    endR = (f'<g id="{p}-endR"><path d="M40 -6 C80 -2 112 26 150 30 L144 60 C104 54 74 26 38 26Z" fill="{SC}" stroke="{SC_D}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M82 6 L74 36 M116 22 L108 50" stroke="{SC_L}" stroke-width="8" stroke-linecap="round"/>'
            f'<g transform="translate(140 46) rotate(-20)">{fr}</g></g>')
    band = (f'<g id="{p}-band"><path d="M-60 -24 Q0 -8 60 -24 L56 20 Q0 34 -56 20Z" fill="{SC}" stroke="{SC_D}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M-30 -16 L-28 24 M2 -12 L2 28 M32 -16 L30 24" stroke="{SC_L}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="0" cy="4" r="20" fill="{SC_D}"/><circle cx="-5" cy="-1" r="7" fill="{SC_L}"/></g>')
    return f'<g id="{p}">{endL}{endR}{band}</g>'


def bush_scarf(p):
    """The bush is 1.4 times art._thorn; the scarf hangs over its top branches (about y = -230)."""
    return (f'<g id="{p}">{art._thorn(p + "-b", 0, 0, 1.4)}'
            f'<g transform="translate(10 -236) rotate(-8) scale(.62)">{scarf(p + "-s")}</g></g>')


def rock(p):
    return (f'<g id="{p}"><ellipse cx="0" cy="4" rx="230" ry="22" fill="#000" opacity=".12"/>'
            f'<path d="M-220 0 C-240 -120 -160 -230 -40 -250 C80 -270 200 -190 224 -80 C236 -30 220 0 210 0Z" fill="#c98f5f" stroke="#7d4a22" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M-150 -160 C-100 -210 -30 -228 30 -224" stroke="#e2b07e" stroke-width="22" fill="none" stroke-linecap="round" opacity=".8"/>'
            f'<path d="M60 -120 l40 -20 M-60 -70 l30 18" stroke="#9a6a3e" stroke-width="10" stroke-linecap="round"/></g>')


def shut_eyes(p):
    lid = lambda x: (f'<ellipse cx="{x}" cy="-184" rx="47" ry="49" fill="{art.MILO_BLUE}"/>'
                     f'<path d="M{x - 34} -176 Q{x} -150 {x + 34} -176" stroke="{art.INK}" stroke-width="8" fill="none" stroke-linecap="round"/>'
                     f'<path d="M{x - 34} -176 l-12 8 M{x + 34} -176 l12 8" stroke="{art.INK}" stroke-width="6" stroke-linecap="round"/>')
    return f'<g id="{p}">{lid(-46)}{lid(46)}</g>'


def wind_lines(p):
    return (f'<g id="{p}" fill="none" stroke="#ffffff" stroke-linecap="round" opacity=".85">'
            f'<path d="M-420 -60 q140 -40 280 0 t280 0 q60 -60 0 -90 q-50 -10 -40 40" stroke-width="12"/>'
            f'<path d="M-200 60 q120 -30 240 0 t240 0" stroke-width="9"/>'
            f'<path d="M80 -150 q100 -26 200 0 t200 0 q50 -50 0 -76 q-40 -8 -34 32" stroke-width="10"/></g>')
