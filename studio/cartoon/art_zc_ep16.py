"""Art for zc_ep16 "How Do Sea Turtles Breathe?" (Nov 27 2026): a new place at the top of the sea ("surface": sky above, water below, the water
line across the middle) with a see-through water layer drawn IN FRONT of the swimmer (so Tula's body is under the water and her head pops out
above it), a cut-away of a sea turtle with its two lungs under the shell (they fill and empty), air bubbles, a slow heart board, a clock, a
nostril breath puff. Tula is the existing rig ("turtle", art2.py). Same hand as art.py / art2.py. Nothing here changes an existing character,
prop or place."""
import math
import art, art2, kit
import art_za_ep12 as A12
from art import INK

WL = 470          # the water line of the "surface" place


def bg_surface(p):
    """The top of the sea: a sunny sky and clouds above, the water line across the middle (y = WL), blue water with light rays below."""
    far = (A12._airsky(p) + art._sun(p + "sun", 1560, 150, 70) + art._cloud(p + "c1", 420, 140, .8) + art._cloud(p + "c2", 980, 90, .55)
           + f'<rect x="-500" y="{WL}" width="2920" height="1700" fill="#4fb6e4"/>'
           + f'<rect x="-500" y="{WL + 260}" width="2920" height="1500" fill="#3a9fd4"/>'
           + "".join(f'<path d="M{x} {WL} L{x + 140} 1700 L{x + 300} 1700 L{x + 70} {WL}Z" fill="#fff" opacity=".08"/>' for x in (100, 700, 1300, 1800)))
    mid = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#fff" stroke-width="5" opacity=".55"/>' for x, y, r in ((300, 900, 14), (330, 830, 9), (1620, 980, 12), (1650, 900, 8)))
    near = ""
    return far, mid, near


art.BG["surface"] = bg_surface
art.PLACE["surface"] = "the top of the sea"


def water_over(pid, w=3000):
    """The water in FRONT of the swimmer: see-through blue from the water line down, with a white wavy edge, so what is under the line looks
    under the water and what is above it (Tula's head) is in the air. Anchored at the water line (y = 0 here)."""
    wave = " ".join(f"q30 -16 60 0 q30 16 60 0" for _ in range(int(w / 120)))
    return (f'<g id="{pid}"><rect x="{-w / 2}" y="0" width="{w}" height="1400" fill="#3aa6da" opacity=".42"/>'
            f'<path d="M{-w / 2} 0 {wave}" stroke="#ffffff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".95"/></g>')


def bubble_col(pid, n=6):
    """A little column of air bubbles (each its own -b<k>), bottom at 0 0."""
    out = ""
    for k in range(n):
        x = (-1) ** k * 18; y = -k * 70; r = 14 + (k % 3) * 6
        out += f'<g id="{pid}-b{k}"><circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" fill-opacity=".3" stroke="#ffffff" stroke-width="6"/><circle cx="{x - r * .35:.0f}" cy="{y - r * .35:.0f}" r="{r * .25:.0f}" fill="#fff"/></g>'
    return f'<g id="{pid}">{out}</g>'


def lungs_cut(pid):
    """A sea turtle seen from the side with a window in its shell: two pink lungs right under the shell (Olive Ridley Project: "The lungs are
    located right under the carapace"). Parts: -lungs (they fill: scale them up from their top), -air (light blue air flowing in at the nose,
    hidden), -shell. Centred at 0 0, about 900 wide."""
    shell_d = "M-360 40 C-300 -300 260 -330 380 40Z"
    body = (f'<path d="M-380 40 Q0 150 400 40 Q0 90 -380 40Z" fill="#f2e6a8" stroke="#1f5a3c" stroke-width="12"/>'
            f'<path d="M330 10 C380 -70 560 -80 590 0 C600 50 520 80 430 70 C380 66 340 50 330 10Z" fill="#a8dc8c" stroke="#1f5a3c" stroke-width="12"/>'
            f'<circle cx="500" cy="-14" r="20" fill="#fff" stroke="#1f5a3c" stroke-width="5"/><circle cx="506" cy="-12" r="11" fill="#1a1a2e"/>'
            f'<circle cx="578" cy="-6" r="6" fill="#1f5a3c"/>'
            f'<path d="M150 60 C230 100 200 220 110 250 C100 180 110 120 130 70Z" fill="#a8dc8c" stroke="#1f5a3c" stroke-width="10"/>'
            f'<path d="M-280 60 C-360 80 -380 150 -350 180 C-310 160 -290 110 -260 70Z" fill="#a8dc8c" stroke="#1f5a3c" stroke-width="10"/>')
    shell = (f'<g id="{pid}-shell"><path d="{shell_d}" fill="#4fae7a" stroke="#1f5a3c" stroke-width="14"/>'
             f'<path d="M-250 -60 C-150 -230 150 -240 270 -60 C150 -10 -150 -10 -250 -60Z" fill="#cfeee0" stroke="#2f8a5a" stroke-width="10" stroke-dasharray="26 16"/></g>')
    lung = lambda x: f'<path d="M{x - 110} -70 C{x - 120} -170 {x - 30} -190 {x} -150 C{x + 30} -190 {x + 120} -170 {x + 110} -70 C{x + 60} -40 {x - 60} -40 {x - 110} -70Z" fill="#ff8fab" stroke="#b8324f" stroke-width="9"/>'
    lungs = f'<g id="{pid}-lungs">{lung(-110)}{lung(130)}<path d="M20 -150 L20 -120 M20 -120 Q300 -120 420 -40" stroke="#b8324f" stroke-width="10" fill="none" stroke-linecap="round"/></g>'
    air = f'<g id="{pid}-air" opacity="0">' + "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="#bfe8ff" stroke="#5fb8ea" stroke-width="5"/>' for x, y in ((640, -10), (700, -40), (760, -20))) + '</g>'
    return f'<g id="{pid}">{body}{shell}{lungs}{air}</g>'


def slow_heart(pid):
    """A big heart and a heartbeat line under it with long flat stretches between the beats (the heart beats very slowly). Parts: -h (the heart,
    it pulses), -line, -dot (a dot that travels along the line). Centred at 0 0."""
    line = "M-600 260 L-380 260 L-350 190 L-320 330 L-290 260 L300 260 L330 190 L360 330 L390 260 L600 260"
    return (f'<g id="{pid}"><g id="{pid}-h" transform="translate(0 -60) scale(3.4)">{art2.heart(pid + "-hh")}</g>'
            f'<path id="{pid}-line" d="{line}" stroke="#e63946" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<circle id="{pid}-dot" cx="-600" cy="260" r="22" fill="#ffd23f" stroke="{INK}" stroke-width="6"/></g>')


def big_clock(pid):
    """A round clock (art.clock) whose minute hand -min can turn round and round (hours passing)."""
    return art.clock(pid)


def nose_puff(pid):
    """A little puff of breath out of the nose (three soft circles), anchored at the nose."""
    return f'<g id="{pid}">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" stroke="#9fd4f0" stroke-width="5" opacity=".95"/>' for x, y, r in ((30, -10, 16), (70, -36, 22), (120, -70, 28))) + '</g>'


def rest_ledge(pid, w=900):
    """A rocky ledge drawn IN FRONT of a resting turtle's back half (a cozy spot under a rock), base at y = 0."""
    return (f'<g id="{pid}"><path d="M{-w / 2} 0 C{-w / 2} -260 {-w * .1:.0f} -380 {w * .05:.0f} -360 C{w * .2:.0f} -340 {w * .22:.0f} -240 {w * .1:.0f} -200 '
            f'C{w * .02:.0f} -170 {-w * .05:.0f} -60 {w * .08:.0f} 0Z" fill="#8a95ad" stroke="#5a6480" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M{-w * .35:.0f} -200 q60 -40 120 -10" stroke="#a9b3c8" stroke-width="12" fill="none" stroke-linecap="round"/></g>')
