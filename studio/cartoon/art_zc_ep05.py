"""Pictures for zc_ep05 "What Is Inside a Camel's Hump?" (Nov 18 2026). New props only: no character, place or older prop is drawn differently.
Everything is anchored the way art.py does it: (0, 0) is the bottom middle unless the docstring says the middle."""
import art

INK = art.INK; SUN = art.SUN; C = art.CAMEL
HUMP_D = "M-260 0 C-230 -150 -110 -430 0 -430 C110 -430 230 -150 260 0Z"      # the outline of art.hump_cutaway


def hump_closed(pid):
    """The hump from outside (the same outline as art.hump_cutaway), before we look in."""
    return (f'<g id="{pid}"><path d="{HUMP_D}" fill="{C["fill"]}" stroke="{C["line"]}" stroke-width="16" stroke-linejoin="round"/>'
            f'<path d="M-120 -250 C-80 -330 -20 -372 40 -372" stroke="{C["light"]}" stroke-width="26" fill="none" stroke-linecap="round" opacity=".9"/>'
            f'<path d="M-214 -14 C-200 -80 -170 -150 -150 -190 C-90 -60 90 -40 214 -14Z" fill="{C["shade"]}" opacity=".45"/></g>')


def fat_blob(pid):
    """A lump of fat, drawn like the fat inside art.hump_cutaway. Anchored at its middle."""
    return (f'<g id="{pid}">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffe08a" stroke="#f2b84b" stroke-width="8"/>' for x, y, r in ((-52, 26, 60), (56, 30, 56), (0, -44, 62)))
            + '<ellipse cx="-22" cy="-66" rx="18" ry="12" fill="#fff" opacity=".7"/></g>')


def hay(pid):
    """Camel food: a bunch of grass and leaves. Anchored at the bottom middle."""
    blades = "".join(f'<path d="M{x0} 0 Q{(x0 + x1) / 2 + b} {-h * .6:.0f} {x1} {-h}" stroke="{col}" stroke-width="20" fill="none" stroke-linecap="round"/>'
                     for x0, x1, h, b, col in ((-60, -150, 190, -20, "#4fa35c"), (-36, -84, 250, -10, "#6cc070"), (-10, -12, 280, 0, "#4fa35c"), (20, 70, 250, 10, "#8fd07a"), (50, 150, 200, 20, "#4fa35c"), (0, 36, 170, 6, "#d9c45a"), (-20, -52, 150, -6, "#d9c45a")))
    leaves = "".join(f'<ellipse cx="{x}" cy="{y}" rx="34" ry="17" fill="#6cc070" stroke="#3a8a4c" stroke-width="6" transform="rotate({r} {x} {y})"/>' for x, y, r in ((-150, -196, -40), (150, -206, 40), (-12, -286, -80)))
    return f'<g id="{pid}">{blades}{leaves}<ellipse cx="0" cy="-6" rx="96" ry="22" fill="#3a8a4c"/></g>'


def backpack(pid):
    """A backpack full of snacks (Milo's comparison for the fat in a hump). #<pid>-snacks is what is inside. Anchored at the bottom middle."""
    snacks = (f'<g id="{pid}-snacks"><circle cx="-56" cy="-296" r="44" fill="#ff6b5e" stroke="{INK}" stroke-width="8"/><path d="M-56 -338 q6 -22 24 -26" stroke="#3a8a4c" stroke-width="9" fill="none" stroke-linecap="round"/>'
              f'<path d="M30 -270 L52 -392 L96 -290Z" fill="#ffb347" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
              f'<ellipse cx="-4" cy="-322" rx="26" ry="52" fill="#6cc070" stroke="{INK}" stroke-width="8" transform="rotate(12 -4 -322)"/></g>')
    return (f'<g id="{pid}">{snacks}<path d="M-96 -250 q96 -110 192 0" stroke="#1f7a70" stroke-width="20" fill="none" stroke-linecap="round"/>'
            f'<rect x="-140" y="-270" width="280" height="270" rx="56" fill="#3fb6a8" stroke="{INK}" stroke-width="10"/>'
            f'<path d="M-140 -214 q140 70 280 0 v-10 a56 56 0 0 0 -56 -46 h-168 a56 56 0 0 0 -56 46Z" fill="#62d0c2" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
            f'<rect x="-80" y="-130" width="160" height="100" rx="24" fill="#2a9488" stroke="{INK}" stroke-width="8"/><circle cx="0" cy="-196" r="16" fill="{SUN}" stroke="{INK}" stroke-width="7"/></g>')


def tuft_big(pid):
    """Close up: a small peak of hide with a tassel of curly hair on top (San Diego Zoo). The curls are .<pid>-c. Anchored at the bottom middle."""
    curls = "".join(f'<path class="{pid}-c" d="M{x} {y} q-64 -136 40 -184 q104 -32 72 80 q-32 72 -88 32" stroke="{C["hair"]}" stroke-width="40" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                    for x, y in ((-170, -150), (-30, -214), (112, -158)))
    return (f'<g id="{pid}"><path d="M-520 0 Q-380 -30 -300 -90 Q0 -330 300 -90 Q380 -30 520 0Z" fill="{C["fill"]}" stroke="{C["line"]}" stroke-width="18" stroke-linejoin="round"/>'
            f'<path d="M-250 -96 Q-60 -250 120 -208" stroke="{C["light"]}" stroke-width="30" fill="none" stroke-linecap="round" opacity=".8"/>{curls}</g>')


def milk_drop(pid):
    """A drop of milk. Anchored at its middle."""
    return (f'<g id="{pid}"><path d="M0 -120 C60 -40 80 0 80 40 A80 80 0 0 1 -80 40 C-80 0 -60 -40 0 -120Z" fill="#fff" stroke="#8fc1ee" stroke-width="12" stroke-linejoin="round"/>'
            f'<ellipse cx="-30" cy="30" rx="16" ry="26" fill="#dcecfb"/></g>')


def qcard(pid, w=300, h=220):
    """A card with a question mark, to hide the answer until the reveal. Anchored at its middle."""
    return (f'<g id="{pid}"><rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="40" fill="#2f80ed" stroke="#fff" stroke-width="14"/>'
            f'<text x="0" y="{h * .32:.0f}" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="{h * .9:.0f}" fill="{SUN}" stroke="{INK}" stroke-width="10" paint-order="stroke fill">?</text></g>')


def ghost_hump(pid):
    """Where a hump will form: the outline of a camel's hump in dashes. Drawn in the camel's own units (the hump's base is at y = -372)."""
    d = "M-170 -372 C-150 -470 -70 -590 10 -590 C90 -590 150 -470 176 -372"
    return (f'<g id="{pid}"><path d="{d}Z" fill="{SUN}" opacity=".3"/><path d="{d}" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round" stroke-dasharray="6 34"/>'
            f'<path d="{d}" stroke="{SUN}" stroke-width="9" fill="none" stroke-linecap="round" stroke-dasharray="6 34"/></g>')


def months(pid, n=3):
    """Calendar pages: one page is one month. The pages are .<pid>-m. Anchored at the middle."""
    out = ""
    for k in range(n):
        x = (k - (n - 1) / 2) * 300
        out += (f'<g class="{pid}-m"><rect x="{x - 125:.0f}" y="-140" width="250" height="280" rx="30" fill="#fff" stroke="{art.MILO_BLUE}" stroke-width="12"/>'
                f'<path d="M{x - 125:.0f} -80 v-30 a30 30 0 0 1 30 -30 h190 a30 30 0 0 1 30 30 v30Z" fill="#e63946"/>'
                + "".join(f'<circle cx="{x - 72 + c * 48:.0f}" cy="{-30 + r * 48}" r="13" fill="{SUN}"/>' for r in range(3) for c in range(4)) + '</g>')
    return f'<g id="{pid}">{out}</g>'
