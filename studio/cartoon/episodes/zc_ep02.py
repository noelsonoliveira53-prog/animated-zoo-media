"""zc_ep02: "What Can an Elephant's Trunk Do?" - cartoon fact lesson with Milo, Tumble the baby elephant and his mama.
Three parts of 85-95 s, each cut whole into one Short: 1. a nose and a hand, 2. a drink and a shower, 3. a snorkel and a hug.

FACTS, read at the source on Nov 16 2026:
 [WWF] wwf.org.uk, "Unforgettable elephant facts"
   "An elephant's trunk is its nose and an upper lip."   "They use their long trunks to smell their food and lift it up into their mouths"
   "They also use their trunks to smell water up to 5km away."   "They suck water up their trunks then blow it into their mouths."
   "As well as smelling and grabbing things it can be used as a snorkel when an elephant wades in deep water."
   "they keep cool by squirting a trunkful of cool water over their bodies"
 [SDZ] San Diego Zoo, animals.sandiegozoo.org/animals/elephant
   "An elephant's trunk serves as both an upper lip and a nose."   "There are no bones or cartilage in this unique appendage."
   "so strong it can pick up large tree trunks and so agile that it can pick up a single piece of straw."
   "Elephants also use their trunk like we use our hands: to grab, hold, pick up, reach, touch, pull, push, and throw."
   "has two nostrils at the end that suck air up the long nasal passages and into the lungs."
   "the water doesn't go all the way up the nose like a straw; instead, the elephant sucks water only part way up the trunk, curls it toward its mouth"
   "Calves are clumsy at first with their trunk, but they learn to use it as they grow older."
   "The little one uses its mouth to drink its mother's milk, so it doesn't need a long trunk yet to feed."
   a trunk "is also used in caressing" (read for za_ep01 the same day).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2
from kit import Kit, S, prop, W

EP = {"id": "zc_ep02", "nest": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "What Can an Elephant's Trunk Do?", "thumb_text": "ONE NOSE?!", "series": "Animal Facts with Milo",
      "description": ("What can an elephant's trunk do? Is it a nose, a hand or a shower? Milo the bluebird visits baby elephant Tumble and his mama to find out! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn that a trunk is a nose and an upper lip, that it can smell, grab, drink, spray and work like a snorkel, "
                      "that the water does not go all the way up like a straw, and that there are no bones inside.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nWWF (Unforgettable elephant facts); San Diego Zoo Wildlife Alliance (elephant)."),
      "tags": ["elephant", "elephants for kids", "elephant trunk", "baby elephant", "savanna animals for kids", "animal facts for kids", "learning videos for toddlers", "preschool",
               "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "zoo": [("milo", "milo", 960, 940, 1.1, False, False)],
    "savanna": [("mama", "elephant", 1560, 930, .9, True), ("tumble", "tumble", 560, 936, .6), ("milo", "milo", 230, 490, .78, False, True)],
    "jungle": [("tumble", "tumble", 900, 930, .66), ("milo", "milo", 380, 470, .78, False, True)],
    "bigtree": [("mama", "elephant", 1250, 930, .85, True), ("milo", "milo", 330, 400, .75, False, True)],
    "river": [("mama", "elephant", 1500, 905, .8, True), ("tumble", "tumble", 560, 905, .55), ("milo", "milo", 300, 400, .7, False, True)],
    "zoo_eve": [("mama", "elephant", 1560, 932, .9, True), ("tumble", "tumble", 700, 940, .6), ("milo", "milo", 300, 420, .7, False, True)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
HUG = [("mama", "elephant", 1560, 944, .9, True), ("tumble", "tumble", 760, 940, .6)]      # her trunk rests on the top of his head (-68): lower (-60) it covered his eye in the first render      # Mama a little nearer the camera: her trunk is drawn over Tumble, not behind him
WIDE = (960, 540, 1920)
E = art2.ELE; INK = art.INK; SUN = art.SUN
TP = "392 -430"       # the trunk's pivot

# ------------------------------------------------------------------ pictures for the boards
def tip(pid):
    """The tip of a trunk, seen from the front: two nostrils."""
    return (f'<g id="{pid}"><path d="M-170 -430 C-190 -200 -205 -40 -155 62 C-100 158 100 158 155 62 C205 -40 190 -200 170 -430Z" fill="{E["fill"]}" stroke="{E["line"]}" stroke-width="13" stroke-linejoin="round"/>'
            + "".join(f'<path d="M-150 {y} q150 34 300 0" stroke="{E["shade"]}" stroke-width="9" fill="none" stroke-linecap="round"/>' for y in (-330, -230, -130))
            + f'<ellipse cx="0" cy="40" rx="150" ry="84" fill="{E["ear"]}" stroke="{E["line"]}" stroke-width="10"/>'
            f'<ellipse id="{pid}-n0" cx="-58" cy="40" rx="36" ry="46" fill="#5b3a4c"/><ellipse id="{pid}-n1" cx="58" cy="40" rx="36" ry="46" fill="#5b3a4c"/></g>')


def scent(pid):
    return f'<g id="{pid}">' + "".join(f'<path d="M{x} 0 q-22 -32 0 -64 q22 -32 0 -64 q-22 -32 0 -64" stroke="#7ccf6a" stroke-width="13" fill="none" stroke-linecap="round"/>' for x in (-50, 0, 50)) + '</g>'


def pond(pid):
    return (f'<g id="{pid}"><ellipse cx="0" cy="0" rx="210" ry="70" fill="#5fb8ea" stroke="#2f8fd0" stroke-width="9"/><path d="M-110 -6 q30 -16 60 0 M20 14 q30 -16 60 0" stroke="#dff3ff" stroke-width="8" fill="none" stroke-linecap="round"/>'
            + "".join(f'<path d="M{x} -40 q-10 -60 {d} -110" stroke="#4fa35c" stroke-width="10" fill="none" stroke-linecap="round"/>' for x, d in ((-190, -18), (-170, 14), (180, 18), (200, -10))) + '</g>')


def tube(pid):
    """A trunk you can see into: the water only rises part of the way."""
    return (f'<g id="{pid}"><rect x="-74" y="-520" width="148" height="520" rx="60" fill="{E["light"]}" stroke="{E["line"]}" stroke-width="13"/>'
            f'<rect id="{pid}-w" x="-52" y="-498" width="104" height="476" rx="44" fill="#58b9e8"/>'
            f'<path d="M-120 -260 H120" stroke="{INK}" stroke-width="8" stroke-dasharray="18 14" stroke-linecap="round"/></g>')


def log(pid):
    return (f'<g id="{pid}"><rect x="-170" y="-52" width="340" height="104" rx="46" fill="#9a6a3a" stroke="#5a3a1a" stroke-width="10"/><path d="M-110 -18 h90 M-60 18 h120" stroke="#7a4f26" stroke-width="8" stroke-linecap="round"/>'
            f'<ellipse cx="138" cy="0" rx="30" ry="46" fill="#dcae72" stroke="#5a3a1a" stroke-width="9"/><ellipse cx="138" cy="0" rx="13" ry="22" fill="none" stroke="#a8743a" stroke-width="6"/></g>')


def straw(pid): return f'<g id="{pid}"><path d="M-70 12 L70 -12" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-70 12 L70 -12" stroke="#f2cf5a" stroke-width="11" stroke-linecap="round"/></g>'


def bone(pid):
    b = '<circle cx="-110" cy="-26" r="34"/><circle cx="-110" cy="26" r="34"/><circle cx="110" cy="-26" r="34"/><circle cx="110" cy="26" r="34"/><rect x="-110" y="-28" width="220" height="56" rx="10"/>'
    return f'<g id="{pid}"><g fill="{INK}" stroke="{INK}" stroke-width="18" stroke-linejoin="round">{b}</g><g fill="#fff">{b}</g></g>'


def crossx(pid): return f'<g id="{pid}"><path d="M-120 -120 L120 120 M120 -120 L-120 120" stroke="{INK}" stroke-width="46" stroke-linecap="round"/><path d="M-120 -120 L120 120 M120 -120 L-120 120" stroke="#e63946" stroke-width="26" stroke-linecap="round"/></g>'


def cup(pid):
    return (f'<g id="{pid}"><path d="M-70 -150 L-52 0 H52 L70 -150Z" fill="#dff3ff" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/><path d="M-62 -90 L-52 0 H52 L62 -90Z" fill="#58b9e8"/>'
            f'<path d="M10 -40 L60 -250 L110 -262" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 -40 L60 -250 L110 -262" stroke="#ff7aa2" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')


def curl(pid, flip=False):
    """The trunk curled to the mouth, drawn in the elephant's own units (it sits on the elephant while the rig's straight trunk is hidden)."""
    d = "M392 -430 C486 -412 528 -330 478 -286 C436 -250 372 -286 368 -350"
    return (f'<g id="{pid}" transform="scale({-1 if flip else 1} 1)"><path d="{d}" stroke="{E["line"]}" stroke-width="86" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{E["fill"]}" stroke-width="68" fill="none" stroke-linecap="round"/></g>')


def drops(pid, n=3):
    return f'<g id="{pid}">' + "".join(f'<g class="{pid}-d" transform="translate({k * 46 - 46 * (n - 1) / 2:.0f} {(k % 2) * 26}) scale(.24)">{art.water_drop(pid + str(k))}</g>' for k in range(n)) + '</g>'


def bubbles(pid): return f'<g id="{pid}">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#dff3ff" opacity=".85" stroke="#fff" stroke-width="5"/>' for x, y, r in ((0, 0, 20), (46, -40, 14), (-30, -70, 17), (20, -120, 11), (-60, -10, 10))) + '</g>'


def vine(pid): return f'<g id="{pid}"><path d="M0 0 C-14 -200 14 -400 0 -760" stroke="#2f7d45" stroke-width="16" fill="none" stroke-linecap="round"/></g>'


def sprayB(pid): return f'<g transform="scale(-1 1)">{art2.spray(pid)}</g>'


def air(pid): return f'<g id="{pid}">' + "".join(f'<path d="M{x} -150 V-20 M{x - 26} -52 L{x} -16 L{x + 26} -52" stroke="#2f80ed" stroke-width="15" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' for x in (-34, 34)) + '</g>'


def job(k):
    """One of the six trunk jobs as a round picture: smell, grab, drink, spray, snorkel, hug."""
    def f(pid):
        ic = [f'<g transform="translate(0 78) scale(.82)">{scent(pid + "i")}</g>', f'<g transform="translate(0 30) scale(.78)">{art2.fruit(pid + "i")}</g>',
              f'<g transform="translate(0 16) scale(.62)">{art.water_drop(pid + "i")}</g>', f'<g transform="translate(-74 44) scale(.5)">{art2.spray(pid + "i")}</g>',
              (f'<path d="M-84 30 q21 -18 42 0 q21 18 42 0 q21 -18 42 0 q21 18 42 0" stroke="#2f8fd0" stroke-width="13" fill="none" stroke-linecap="round"/>'
               f'<path d="M0 34 V-62" stroke="{E["line"]}" stroke-width="46" stroke-linecap="round"/><path d="M0 34 V-62" stroke="{E["fill"]}" stroke-width="30" stroke-linecap="round"/>'),
              f'<g transform="translate(0 22) scale(1.5)">{art2.heart(pid + "i")}</g>'][k]
        return f'<g id="{pid}"><circle r="108" fill="#fff" stroke="{INK}" stroke-width="10"/>{ic}</g>'
    return f


JOBS = ["SMELL", "GRAB", "DRINK", "SPRAY", "SNORKEL", "HUG"]
JX = [360, 600, 840, 1080, 1320, 1560]; JP = [(690, 340), (960, 340), (1230, 340), (690, 780), (960, 780), (1230, 780)]     # the six in a row (16:9) and in two rows (9:16)
JCAM = (960, 520, 1560); JPCAM = (960, 480, 1700)


def jobs(shown, new=()):
    """The six-jobs board: the ones in `shown` are there from the start, the ones in `new` are hidden and pop in."""
    return [prop(f"j{k}", job(k), JX[k], 560, 1.0, k in new, p=(*JP[k], 1.05)) for k in range(6) if k in shown or k in new]


def water(pid): return art2.water_front(pid).replace("L1660 400 L-1460 400Z", "L1660 1700 L-1460 1700Z")      # deep enough for the tall 9:16 views (400 left a strip of ground under the river)


def RV(y=850): return [prop("wf", water, 960, y, 1.0)]      # the river in front of the elephants' legs


UP = {"rotation": -160, "scaleY": 1.35, "svgOrigin": TP, "duration": .01}       # the trunk straight up: a snorkel
DIP = {"scaleY": 1.38, "svgOrigin": TP, "duration": .6}                           # the trunk reaches down into the water
TUP = (700, 626, 1200); MAP = WV("savanna", ["mama"]); JUP = (1050, 549, 1410); BTP = (1040, 417, 1900)
RTP = WV("river", ["tumble"]); RMP = WV("river", ["mama"]); ZTP = WV("zoo_eve", ["tumble"]); ZMP = WV("zoo_eve", ["mama"]); HUGP = (1208, 400, 2600)       # Tumble and Mama whole in 9:16 (the evening sky ends at y = -900)
BRD = dict(actors=[("t", "tumble", 760, 960, 1.0)], pcam=(895, 480, 1850))      # the board with Tumble on it
TC = C("savanna", "tumble", "head", 880, 50, 20); TV = V("savanna", "tumble", "head", 1000, 50, 40)
RTC = C("river", "tumble", "head", 880, 60, 30); RTV = V("river", "tumble", "head", 1000, 60, 40)
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 900))

SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("savanna", C("savanna", "tumble", "trunk", 900, -40, -60), "What can an elephant's trunk do?", q=True, tag="hook: the trunk", hide=["milo", "mama"], pcam=TV,
      words=[("w:trunk", "?", .8, .3, 3.0, "sun", (.8, .37), 1.6)], fx=[("trunk", "w:What", "tumble", -70, .5), ("trunk", "w:trunk", "tumble", 10, .5), ("trunk", "e:do?", "tumble", -40, .4)]),
    S("savanna", C("savanna", "tumble", "trunk", 900, -40, -60), "Is it a nose? A hand? A shower?", tag="hook: guesses", hide=["milo", "mama"], pcam=TV,
      words=[("w:nose?", "NOSE?", .76, .22, 1.0, "", (.28, .29), .8), ("w:hand?", "HAND?", .8, .42, 1.0, "sun", (.72, .29), .8), ("w:shower?", "SHOWER?", .76, .62, 1.0, "", (.5, .36), .8)],
      fx=[("to", 0, "#{p}tumble-trunk", {"rotation": -40, "svgOrigin": TP, "duration": .01}), ("trunk", "w:hand?", "tumble", 10, .4), ("trunk", "w:shower?", "tumble", -100, .4)]),
    S("savanna", say="I'm Milo. Let's find out together!", tag="hook: Milo", hide=["tumble", "mama"], fx=[("hop", "w:find", "milo")], **MILO("savanna")),
    # ---------------------------------------------------------------- INTRO
    S("zoo", WIDE, "Welcome to The Animated Zoo, friends!", trans="iris", tag="gate wide", words=[("w:Animated", "HELLO!", .74, .6, 1.2, "pill")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, -40), "Today we fly to the sunny savanna.", tag="Milo close", words=[("w:savanna.", "THE SAVANNA", .5, .16, 1.1, "sun")]),
    S("savanna", WIDE, "Here we are! Look who is waiting for us.", trans="iris", tag="savanna wide", cam2=(960, 560, 1840), pcam=TUP, pcam2=MAP,
      fx=[("fromto", 0, "#{p}milo_w", {"x": -300, "y": 200}, {"x": 230, "y": 490, "duration": 1.3, "ease": "power2.out"}, "Milo flies in")]),
    S("savanna", (1110, 560, 1640), "This is Tumble. Tumble is a baby elephant.", tag="this is Tumble", hide=["milo"], pcam=TUP, words=[("w:Tumble.", "TUMBLE", .3, .26, 1.0, "pill", (.5, .31))], fx=[("hop", "w:Tumble.", "tumble")]),
    S("savanna", C("savanna", "mama", "head", 960, 100, 70), "And this is Tumble's mama. Hello, Mama!", tag="Mama close", hide=["milo"], pcam=MAP, fx=[("nod", "w:Hello,", "mama")],
      words=[("w:Hello,", "MAMA", .8, .16, 1.0, "pill", (.5, .31))]),
    # ---------------------------------------------------------------- PART 1: a nose and a hand
    S("savanna", C("savanna", "tumble", "trunk", 760, -20, -40), "Look at Tumble's long, bendy trunk.", part=1, tag="the trunk", hide=["milo", "mama"], pcam=TV,
      words=[("w:trunk.", "TRUNK", .78, .22, 1.2, "sun", (.5, .31))], fx=[("trunk", "w:long,", "tumble", -50, .6), ("trunk", "w:trunk.", "tumble", 15, .6)]),
    S("paper", (960, 520, 1500), "A trunk is a nose.", part=1, tag="board: a nose", **BRD, props=[prop("ar", lambda p: art.arrow(p, 1330, 500, 1290, 650), 0, 0, 1, True)],
      words=[("w:nose.", "NOSE", .78, .26, 1.6, "sun", (.5, .31), 1.2)], fx=[("show", "w:nose.", "ar"), ("trunk", "w:nose.", "t", -20, .4)]),
    S("paper", (960, 520, 1500), "And it is an upper lip, too. All in one!", part=1, tag="board: a lip", **BRD,
      words=[("w:lip,", "+ LIP", .78, .26, 1.6, "", (.5, .31), 1.2), ("w:All", "2 IN 1", .26, .27, 1.2, "pill", (.5, .385), .9)], fx=[("trunk", "w:All", "t", -30, .4), ("trunk", "e:one!", "t", 0, .4)]),
    S("savanna", say="Where is your nose? Can you touch your nose?", part=1, q=True, tag="touch your nose", hide=["tumble", "mama"], pause=1.0, fx=[("hop", "w:touch", "milo")],
      words=[("w:touch", "TOUCH!", .76, .24, 1.0, "sun", (.5, .31))], **MILO("savanna")),
    S("paper_blue", (960, 540, 1400), "At the tip of the trunk are two little holes.", part=1, tag="board: the tip", props=[prop("tip", tip, 960, 760, 1.0, p=(960, 620, .85))], pcam=(960, 480, 1500),
      words=[("w:two", "2 HOLES", .78, .2, 1.1, "pill", (.5, .31), .9)],
      fx=[("to", "w:two", "#{p}tip-n0,#{p}tip-n1", {"scale": 1.3, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 5}, "the two nostrils light up")]),
    S("paper_blue", (960, 600, 1200), "An elephant breathes through them. Sniff, sniff!", part=1, tag="board: sniff", pcam=(960, 480, 1500),
      props=[prop("tip", tip, 960, 760, 1.0, p=(960, 620, .85)), prop("sc", scent, 960, 1130, 1.0, True, p=(960, 900, .8))], words=[("w:Sniff,", "SNIFF!", .2, .2, 1.3, "sun", (.5, .31))],
      fx=[("fromto", "w:Sniff,", "#{p}sc_w", {"y": "+=0", "opacity": 1}, {"y": "-=140", "opacity": 0, "duration": .5, "repeat": 3}, "air goes into the nostrils")]),
    S("savanna", TC, "Sniff, sniff! Tumble smells something yummy.", part=1, tag="Tumble sniffs", hide=["milo", "mama"], pcam=TV, props=[prop("sc", scent, 1010, 640, .7, True)],
      fx=[("trunk", "w:Sniff,", "tumble", -80, .5), ("show", "w:smells", "sc"), ("face", "w:yummy.", "tumble", "happy")], words=[("w:Sniff,", "SNIFF!", .55, .16, 1.1, "sun", (.3, .31), .9)]),
    S("savanna", (760, 660, 1100), "An elephant uses its trunk to smell its food.", part=1, tag="smell the food", hide=["milo", "mama"], pcam=TUP, props=[prop("fr", art2.fruit, 1010, 905, .6, p=(950, 905, .55))],
      words=[("w:smell", "SMELL", .5, .14, 1.3, "sun")], fx=[("trunk", 0.1, "tumble", -25, .5), ("nod", "w:food.", "tumble")]),
    S("paper_pink", (960, 520, 1600), "It can even smell water from far, far away!", part=1, tag="board: far away", actors=[("t", "tumble", 330, 900, .62)], pcam=(1380, 520, 1250), pcam2=(490, 520, 1300),
      props=[prop("pond", pond, 1480, 840, 1.0), prop("s1", scent, 1300, 700, .6, True), prop("s2", scent, 1040, 640, .6, True), prop("s3", scent, 800, 640, .6, True)],
      words=[("w:far,", "FAR AWAY", .62, .16, 1.2, "sun", (.5, .31))], fx=[("trunk", 0.1, "t", -75, .5), ("show", "w:water", "s1"), ("show", "w:far,", "s2"), ("show", "w:away!", "s3")]),
    S("savanna", (1110, 520, 1700), "So, is a trunk a nose, or a tail?", part=1, q=True, tag="question 1", pause=3.4, hide=["milo"], pcam=TUP,
      fx=[("signs", "w:nose,", ["NOSE", "TAIL"], 0, "wait:3.0"), ("trunk", "wait:3.05", "tumble", -60, .3)]),
    S("savanna", TC, "A nose! A very, very long nose.", part=1, tag="a nose!", hide=["milo", "mama"], pcam=TV, words=[("w:nose!", "NOSE!", .8, .16, 1.4, "sun", (.5, .31))],
      fx=[("hop", "w:nose!", "tumble"), ("trunk", "w:long", "tumble", -30, .6)]),
    S("jungle", WIDE, "Now Tumble is hungry. Look, a fruit!", part=1, trans="iris", tag="jungle wide", cam2=(1040, 560, 1760), pcam=JUP, pcam2=W(JUP),
      props=[prop("vine", vine, 1363, 600, 1.0), prop("fr", art2.fruit, 1363, 640, .55)], words=[("w:fruit!", "FRUIT!", .84, .3, 1.2, "sun", (.5, .31))],
      fx=[("to", "w:Look,", "#{p}fr_w", {"rotation": 8, "transformOrigin": "50% 0%", "duration": .3, "yoyo": True, "repeat": 5}, "the fruit swings")]),
    S("jungle", (1231, 626, 1000), "A trunk is like a hand, too.", part=1, tag="like a hand", hide=["milo"], pcam=JUP, props=[prop("vine", vine, 1363, 600, 1.0), prop("fr", art2.fruit, 1363, 640, .55)],
      words=[("w:hand,", "HAND", .55, .18, 1.4, "sun", (.3, .31))], fx=[("trunk", "w:trunk", "tumble", -70, .7)]),
    S("jungle", (1231, 626, 1000), "It can grab, hold, pick up and reach.", part=1, tag="grab", hide=["milo"], pcam=JUP, props=[prop("vine", vine, 1363, 600, 1.0), prop("fr", art2.fruit, 1363, 640, .55)],
      words=[("w:grab,", "GRAB!", .55, .16, 1.3, "sun", (.3, .31))],
      fx=[("to", 0, "#{p}tumble-trunk", {"rotation": -70, "svgOrigin": TP, "duration": .01}), ("to", "w:grab,", "#{p}tumble-trunk", {"rotation": -10, "duration": .8}, "Tumble picks the fruit"),
          ("to", "w:grab,", "#{p}fr_w", {"x": 1290, "y": 836, "duration": .8}, ""), ("to", "w:pick", "#{p}tumble-trunk", {"rotation": 35, "scaleY": .8, "duration": .6}, "the trunk brings it to his mouth"),
          ("to", "w:pick", "#{p}fr_w", {"x": 1176, "y": 806, "duration": .6}, "")]),
    S("jungle", C("jungle", "tumble", "head", 860, 40, 10), "Yum, yum, yum! Can you munch like Tumble?", part=1, q=True, tag="munch", hide=["milo"], pcam=V("jungle", "tumble", "head", 1000, 40, 40),
      fx=[("to", 0.1, "#{p}tumble-jaw", {"opacity": 1, "y": 14, "duration": .16, "yoyo": True, "repeat": 13}, "Tumble munches"), ("face", 0.05, "tumble", "happy")],
      words=[("w:Yum,", "YUM!", .8, .18, 1.3, "sun", (.5, .31))]),
    S("bigtree", WIDE, "Here comes Mama. Her trunk is very, very strong.", part=1, trans="iris", tag="bigtree wide", cam2=(1000, 560, 1780), pcam=BTP, pcam2=W(BTP), props=[prop("log", log, 800, 890, 1.0)],
      move={"mama": (1700, 930, .85, True)}, fx=[("walk", 0, "mama", -450, 2.6)], words=[("w:strong.", "STRONG", .5, .2, 1.3, "sun", (.5, .31))]),
    S("bigtree", (1010, 640, 1150), "It can lift a big, heavy log. Up it goes!", part=1, tag="the log", hide=["milo"], pcam=BTP, pcam2=W(BTP), props=[prop("log", log, 832, 866, 1.0)],
      words=[("w:Up", "UP!", .5, .16, 1.4, "sun", (.3, .31))],
      fx=[("to", "w:Up", "#{p}mama-trunk", {"rotation": -55, "svgOrigin": TP, "duration": .9, "ease": "power2.inOut"}, "Mama lifts the log"),
          ("to", "w:Up", "#{p}log_w", {"x": 670, "y": 640, "rotation": -18, "duration": .9, "ease": "power2.inOut"}, "")]),
    S("paper", (900, 560, 1300), "And a trunk is very gentle, too.", part=1, tag="board: gentle", actors=[("m", "elephant", 1150, 960, .95, True)], pcam=(960, 470, 1800), pcam2=W((960, 470, 1800)), props=[prop("st", straw, 683, 905, 1.0)],
      words=[("w:gentle,", "GENTLE", .22, .2, 1.2, "", (.5, .31))], fx=[("lookat", "w:gentle,", "m", 5)]),
    S("paper", (860, 600, 1100), "It can pick up one tiny piece of straw.", part=1, tag="board: one straw", actors=[("m", "elephant", 1150, 960, .95, True)], pcam=(960, 470, 1800), pcam2=W((960, 470, 1800)), props=[prop("st", straw, 683, 905, 1.0)],
      words=[("w:one", "1 STRAW", .22, .22, 1.1, "sun", (.5, .31))],
      fx=[("to", 0.1, "#{p}m-trunk", {"scaleY": 1.26, "svgOrigin": TP, "duration": .5}, "Mama's trunk reaches down"),
          ("to", "w:one", "#{p}m-trunk", {"rotation": -30, "scaleY": 1.0, "duration": .7}, "she picks up one straw"), ("to", "w:one", "#{p}st_w", {"x": 560, "y": 742, "duration": .7}, "")]),
    S("bigtree", C("bigtree", "mama", "head", 900, -60, 40), "So strong, and so gentle. What a nose!", part=1, tag="strong and gentle", hide=["milo"], pcam=V("bigtree", "mama", "head", 1150, -60, 60),
      words=[("w:strong,", "STRONG", .8, .16, 1.0, "sun", (.5, .3), .8), ("w:gentle.", "GENTLE", .8, .32, 1.0, "", (.5, .365), .8)], fx=[("nod", "w:What", "mama")]),
    S("paper_blue", (960, 520, 1500), "There are no bones inside a trunk.", part=1, tag="board: no bones", pcam=(960, 480, 1900),
      props=[prop("tip", tip, 720, 820, .9, p=(960, 850, .78)), prop("bone", bone, 1240, 560, 1.3, p=(960, 380, 1.1)), prop("x", crossx, 1240, 560, 1.1, True, p=(960, 380, .9))],
      fx=[("show", "w:no", "x")], words=[("w:no", "NO BONES", .68, .16, 1.2, "sun", (.5, .29), .9)]),
    S("jungle", C("jungle", "tumble", "head", 1000, 100, 0), "So it can bend this way, and that way!", part=1, tag="bendy", hide=["milo"], pcam=(1050, 549, 1410),
      fx=[("trunk", "w:this", "tumble", -80, .5), ("trunk", "w:that", "tumble", 30, .5), ("trunk", "e:way!", "tumble", -20, .4)],
      words=[("w:this", "THIS WAY", .8, .12, .9, "sun", (.5, .3), .75), ("w:that", "THAT WAY", .8, .26, .9, "", (.5, .365), .75)]),
    S("jungle", say="Can you wiggle your arm like a trunk? Wiggle, wiggle!", part=1, q=True, tag="wiggle", hide=["tumble"], fx=[("hop", "w:Wiggle,", "milo", 2)],
      words=[("w:Wiggle,", "WIGGLE!", .76, .22, 1.0, "sun", (.5, .31))], **MILO("jungle")),
    S("paper_pink", JCAM, "That is two trunk jobs. One, smell. Two, grab.", part=1, tag="board: jobs 1 2", pcam=JPCAM, props=jobs((), (0, 1)),
      fx=[("show", "w:One,", "j0"), ("show", "w:Two,", "j1")], words=[("w:One,", "1", .115, .22, 1.5, "sun", (.22, .305), 1.1), ("w:Two,", "2", .27, .22, 1.5, "sun", (.5, .305), 1.1)]),
    # ---------------------------------------------------------------- PART 2: a drink and a shower
    S("river", WIDE, "Phew, it is hot! Tumble and Mama walk into the river.", part=2, trans="iris", tag="river wide", cam2=(1000, 560, 1780), pcam=RTP, pcam2=RMP, props=RV(),
      move={"tumble": (260, 905, .55), "mama": (1800, 905, .8, True)}, fx=[("walk", 0, "tumble", 300, 3.0), ("walk", 0, "mama", -300, 3.0)], words=[("w:hot!", "HOT!", .5, .16, 1.3, "sun")]),
    S("river", (1360, 639, 960), "Time for a drink. Watch Mama's trunk!", part=2, tag="watch Mama", hide=["milo"], pcam=RMP, props=RV(),
      fx=[("trunk", "w:Watch", "mama", -30, .4), ("trunk", "e:trunk!", "mama", 0, .4)], words=[("w:Watch", "WATCH!", .8, .16, 1.0, "sun", (.5, .31))]),
    S("river", (1180, 660, 1000), "She sucks the water up into her trunk. Slurp!", part=2, tag="slurp", hide=["milo", "tumble"], pcam=RMP, props=RV(),
      fx=[("to", 0.1, "#{p}mama-trunk", DIP, "Mama's trunk dips into the water"), ("lookat", 0.1, "mama", 6), ("snd", "w:Slurp!", "whoosh")], words=[("w:Slurp!", "SLURP!", .22, .27, 1.3, "sun", (.5, .31))]),
    S("river", (1070, 540, 1560), "Does the water go all the way up her nose? Yes, or no?", part=2, q=True, tag="question 2", pause=3.4, hide=["milo"], pcam=RMP, props=RV(),
      fx=[("to", 0, "#{p}mama-trunk", dict(DIP, duration=.01)), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:3.0")]),
    S("paper_blue", (960, 520, 1400), "No! The water only goes part of the way up.", part=2, tag="board: part way", props=[prop("tube", tube, 960, 930, 1.3, p=(960, 1000, 1.3))], pcam=(960, 480, 1700),
      fx=[("fromto", "w:water", "#{p}tube-w", {"scaleY": .02, "transformOrigin": "50% 100%"}, {"scaleY": .5, "duration": 1.4, "ease": "power1.out"}, "the water rises half way up")],
      words=[("w:No!", "NO!", .26, .2, 1.5, "sun", (.5, .29), 1.2), ("w:part", "PART WAY", .76, .52, 1.0, "pill", (.5, .37), .8)]),
    S("river", (1180, 660, 1000), "Then she curls her trunk to her mouth,", part=2, tag="curl", hide=["milo", "tumble"], pcam=RMP, props=RV() + [prop("curl", lambda p: curl(p, True), 1500, 905, .8, True)],
      fx=[("to", "w:curls", "#{p}mama-trunk", {"opacity": 0, "duration": .15}, "Mama curls her trunk to her mouth"), ("to", "w:curls", "#{p}curl_w", {"opacity": 1, "duration": .15}, "")]),
    S("river", C("river", "mama", "head", 760, -40, 40), "and blows the water in! Glug, glug, glug.", part=2, tag="glug", hide=["milo", "tumble"], pcam=V("river", "mama", "head", 1100, -40, 60),
      props=RV() + [prop("curl", lambda p: curl(p, True), 1500, 905, .8), prop("dr", drops, 1206, 640, 1.0, True)], words=[("w:Glug,", "GLUG!", .8, .2, 1.2, "sun", (.5, .31))],
      fx=[("to", 0, "#{p}mama-trunk", {"opacity": 0, "duration": .01}), ("fromto", "w:Glug,", "#{p}dr_w", {"opacity": 1, "y": 650}, {"y": 610, "opacity": 0, "duration": .4, "repeat": 3}, "the water goes into her mouth")]),
    S("paper", (960, 520, 1500), "So a trunk is not like a straw. It carries the water to the mouth.", part=2, tag="board: not a straw", pcam=(960, 480, 1700),
      props=[prop("cup", cup, 960, 800, 1.7, p=(960, 900, 1.8)), prop("x", crossx, 960, 600, 1.3, True, p=(960, 700, 1.3))], fx=[("show", "w:not", "x")],
      words=[("w:not", "NOT A STRAW", .5, .14, 1.2, "sun", (.5, .31), .95)]),
    S("river", RTC, "Now it is Tumble's turn. His trunk is still short.", part=2, tag="Tumble's turn", hide=["milo", "mama"], pcam=RTV, props=RV(),
      words=[("w:short.", "SHORT", .82, .2, 1.1, "", (.5, .31))], fx=[("trunk", "w:trunk", "tumble", -40, .4), ("trunk", "e:short.", "tumble", 0, .4)]),
    S("river", RTC, "Baby elephants are clumsy with their trunks at first.", part=2, tag="clumsy", hide=["milo", "mama"], pcam=RTV, props=RV(),
      words=[("w:clumsy", "WOBBLE!", .82, .2, 1.0, "sun", (.5, .31))],
      fx=[("to", "w:clumsy", "#{p}tumble-trunk", {"rotation": -35, "svgOrigin": TP, "duration": .22, "yoyo": True, "repeat": 9}, "Tumble's trunk wobbles")]),
    S("river", (800, 640, 1200), "Oops! Splash! The water goes everywhere.", part=2, tag="splash", hide=["milo", "mama"], pcam=RTV, props=RV() + [prop("sp", art2.spray, 880, 790, 1.0, True)],
      fx=[("show", "w:Splash!", "sp"), ("face", "w:Splash!", "tumble", "wow"), ("snd", "w:Splash!", "whoosh"), ("trunk", "w:Oops!", "tumble", -50, .3)], words=[("w:Splash!", "SPLASH!", .78, .2, 1.2, "sun", (.5, .31))]),
    S("river", RTC, "But Tumble keeps trying. Little by little, he learns.", part=2, tag="he learns", hide=["milo", "mama"], pcam=RTV, props=RV(),
      fx=[("face", 0.05, "tumble", "happy"), ("trunk", "w:Little", "tumble", -30, .5), ("trunk", "w:learns.", "tumble", -90, .5), ("hop", "w:learns.", "tumble")],
      words=[("w:Little", "LITTLE BY LITTLE", .76, .16, .8, "pill", (.5, .31), .7)]),
    S("river", say="Can you slurp like an elephant? Slurp, slurp!", part=2, q=True, tag="slurp along", hide=["tumble", "mama"], props=RV(), fx=[("hop", "w:Slurp,", "milo", 2)],
      words=[("w:Slurp,", "SLURP!", .76, .22, 1.0, "sun", (.5, .31))], **MILO("river")),
    S("paper_pink", (960, 520, 1500), "A baby elephant drinks his mama's milk with his mouth.", part=2, tag="board: milk", **BRD, props=[prop("ar", lambda p: art.arrow(p, 1340, 470, 1215, 595), 0, 0, 1, True)],
      words=[("w:mouth.", "MOUTH", .8, .2, 1.2, "sun", (.5, .31))], fx=[("show", "w:mouth.", "ar"), ("to", "w:drinks", "#{p}t-jaw", {"opacity": 1, "y": 12, "duration": .2, "yoyo": True, "repeat": 9}, "he drinks with his mouth")]),
    S("paper_pink", (960, 520, 1500), "So he does not need a long trunk yet.", part=2, tag="board: not yet", **BRD, words=[("w:long", "NOT YET", .28, .24, 1.1, "pill", (.5, .31))],
      fx=[("trunk", "w:long", "t", -25, .5), ("trunk", "e:yet.", "t", 0, .5)]),
    S("river", (1070, 560, 1500), "Now Mama fills her trunk again. What will she do?", part=2, q=True, tag="what next", hide=["milo"], pcam=RMP, props=RV(),
      fx=[("to", 0.1, "#{p}mama-trunk", DIP, "Mama fills her trunk"), ("to", "w:What", "#{p}mama-trunk", {"scaleY": 1, "duration": .5}, "")], words=[("w:What", "?", .5, .2, 2.4, "sun", (.5, .32), 1.5)]),
    S("river", (1250, 500, 1350), "Whoosh! A shower! She sprays water all over her back.", part=2, tag="shower", hide=["milo", "tumble"], move={"mama": (1350, 905, .8, True)}, pcam=(1330, 500, 1700), pcam2=(1330, 500, 1700),
      props=RV() + [prop("sp", art2.spray, 992, 330, 1.3, True)], words=[("w:shower!", "A SHOWER!", .73, .36, 1.0, "sun", (.74, .29), .62)],
      fx=[("trunk", 0.05, "mama", -150, .4), ("show", "w:Whoosh!", "sp"), ("snd", "w:Whoosh!", "whoosh"), ("to", "w:sprays", "#{p}sp_w", {"rotation": 6, "duration": .25, "yoyo": True, "repeat": 7}, "the water sprays")]),
    S("river", (1250, 500, 1350), "Elephants squirt cool water over their bodies to keep cool.", part=2, tag="keep cool", hide=["milo", "tumble"], move={"mama": (1350, 905, .8, True)}, pcam=(1330, 500, 1700), pcam2=(1330, 500, 1700),
      props=RV() + [prop("sp", art2.spray, 992, 330, 1.3)], words=[("w:cool", "COOL!", .2, .3, 1.3, "", (.76, .31), .8)],
      fx=[("to", 0, "#{p}mama-trunk", {"rotation": -150, "svgOrigin": TP, "duration": .01}), ("to", 0.1, "#{p}sp_w", {"rotation": 6, "duration": .25, "yoyo": True, "repeat": 13}, ""), ("face", "w:cool", "mama", "happy")]),
    S("river", (760, 600, 1150), "Tumble wants a shower too. Ready, steady, spray!", part=2, tag="Tumble sprays", hide=["milo", "mama"], pcam=WV("river", ["tumble"], hmin=1400), props=RV() + [prop("sp", sprayB, 833, 549, .9, True)],
      fx=[("trunk", "w:Ready,", "tumble", -140, .5), ("show", "w:spray!", "sp"), ("snd", "w:spray!", "whoosh"), ("face", "w:spray!", "tumble", "happy")], words=[("w:spray!", "SPRAY!", .8, .22, 1.2, "sun", (.5, .29))]),
    S("river", say="Can you spray like an elephant? Whoosh, whoosh!", part=2, q=True, tag="spray along", hide=["tumble", "mama"], props=RV(), fx=[("hop", "w:Whoosh,", "milo", 2)],
      words=[("w:Whoosh,", "WHOOSH!", .76, .22, 1.0, "sun", (.5, .31))], **MILO("river")),
    S("paper_pink", JCAM, "Now we have four trunk jobs. Three, drink. Four, spray.", part=2, tag="board: jobs 3 4", pcam=JPCAM, props=jobs((0, 1), (2, 3)),
      fx=[("show", "w:Three,", "j2"), ("show", "w:Four,", "j3")], words=[("w:Three,", "3", .423, .22, 1.5, "sun", (.78, .305), 1.1), ("w:Four,", "4", .577, .22, 1.5, "sun", (.22, .565), 1.1)]),
    # ---------------------------------------------------------------- PART 3: a snorkel and a hug
    S("river", (1000, 600, 1700), "Now Tumble wades into the deep, deep water.", part=3, trans="iris", tag="wading", hide=["milo", "mama"], pcam=(760, 520, 1500), pcam2=(860, 560, 1500), props=RV(),
      fx=[("walk", 0.1, "tumble", 300, 3.6), ("to", 0.1, "#{p}tumble_w", {"y": "+=90", "duration": 3.6, "ease": "none"}, "")], words=[("w:deep,", "DEEP", .7, .2, 1.2, "", (.5, .31))]),
    S("river", (1100, 720, 1300), "Deeper, and deeper, and deeper.", part=3, tag="deeper", actors=[("tumble", "tumble", 900, 1000, .62)], pcam=(1100, 640, 1500), props=RV(),
      fx=[("to", 0.1, "#{p}tumble_w", {"y": 1263, "duration": 3.0, "ease": "none"}, "Tumble goes deeper"), ("trunk", 0.3, "tumble", -160, 1.2), ("to", 0.3, "#{p}tumble-trunk", {"scaleY": 1.35, "duration": 1.2}, "")],
      words=[("w:deeper:2", "DEEPER", .76, .16, 1.0, "", (.5, .3), .8), ("w:deeper:3", "DEEPER!", .76, .3, 1.2, "sun", (.5, .37), .9)]),
    S("river", (1150, 700, 1200), "Where did Tumble go? Can you see him?", part=3, q=True, tag="where is Tumble", pause=1.2, actors=[("tumble", "tumble", 900, 1263, .62)], pcam=(1167, 640, 1400), props=RV(),
      fx=[("to", 0, "#{p}tumble-trunk", UP), ("to", 0.2, "#{p}tumble_w", {"y": "-=14", "duration": .6, "yoyo": True, "repeat": 9}, "the tip of a trunk bobs on the water")],
      words=[("w:Where", "?", .26, .3, 2.6, "sun", (.5, .34), 1.6)]),
    S("river", (1167, 720, 860), "Peekaboo! There is the tip of his trunk.", part=3, tag="peekaboo", actors=[("tumble", "tumble", 900, 1263, .62)], pcam=(1167, 640, 1200),
      props=RV() + [prop("ar", lambda p: art.arrow(p, 1330, 620, 1215, 770), 0, 0, 1, True)],
      fx=[("to", 0, "#{p}tumble-trunk", UP), ("show", "w:tip", "ar"), ("to", "w:Peekaboo!", "#{p}tumble_w", {"y": "-=30", "duration": .25, "yoyo": True, "repeat": 3}, "the trunk waves")],
      words=[("w:Peekaboo!", "PEEKABOO!", .5, .2, 1.1, "sun", (.5, .31), .9)]),
    S("paper_blue", (960, 540, 1600), "An elephant can use its trunk like a snorkel.", part=3, tag="board: snorkel", pcam=(960, 480, 1800), props=[prop("sb", art2.snorkel_board, 960, 400, 1.0, p=(960, 430, .7))],
      words=[("w:trunk", "TRUNK", .36, .13, 1.0, "sun", (.24, .31), .68), ("w:snorkel.", "= SNORKEL", .68, .13, 1.0, "", (.67, .31), .68)], fx=[("to", 0, "#{p}sbe-trunk", UP)]),
    S("paper_blue", (960, 500, 1300), "The tip stays up in the air, so he can breathe.", part=3, tag="board: air", pcam=(960, 480, 1800),
      props=[prop("sb", art2.snorkel_board, 960, 400, 1.0, p=(960, 430, .7)), prop("air", air, 1040, 330, 1.0, True, p=(1016, 372, .8))],
      words=[("w:air,", "AIR", .78, .2, 1.3, "", (.5, .31))], fx=[("to", 0, "#{p}sbe-trunk", UP), ("show", "w:air,", "air"), ("to", "w:breathe.", "#{p}air_w", {"y": "+=26", "duration": .4, "yoyo": True, "repeat": 3}, "air goes down the trunk")]),
    S("paper_blue", (1138, 440, 820), "Only the tip of the trunk is above the water.", part=3, tag="board: only the tip", pcam=(1040, 520, 1300),
      props=[prop("sb", art2.snorkel_board, 960, 400, 1.0, p=(960, 430, .7)), prop("ar", lambda p: art.arrow(p, 170, -150, 45, -30), 1138, 400, 1.0, True, p=(1085, 430, .8))],
      words=[("w:tip", "ONLY THE TIP", .26, .2, .9, "pill", (.5, .31), .8)], fx=[("to", 0, "#{p}sbe-trunk", UP), ("show", "w:tip", "ar")]),
    S("river", say="Breathe in through your nose. And out. Can you do it?", part=3, q=True, tag="breathe", hide=["tumble", "mama"], props=RV(),
      fx=[("to", "w:in", "#{p}milo-body", {"scaleX": 1.1, "scaleY": 1.08, "svgOrigin": "0 0", "duration": .8}, "Milo breathes in"), ("to", "w:out.", "#{p}milo-body", {"scaleX": 1, "scaleY": 1, "duration": .8}, "and out")],
      words=[("w:in", "IN", .76, .2, 1.3, "sun", (.3, .31)), ("w:out.", "OUT", .76, .36, 1.3, "", (.7, .31))], **MILO("river")),
    S("river", (1000, 720, 1300), "Tumble walks along under the water. Bubble, bubble!", part=3, tag="bubbles", actors=[("tumble", "tumble", 660, 1263, .62)], pcam=(1090, 640, 1500),
      props=RV() + [prop("bu", bubbles, 1100, 830, 1.0, True)], words=[("w:Bubble,", "BUBBLE!", .5, .18, 1.1, "sun", (.5, .31))],
      fx=[("to", 0, "#{p}tumble-trunk", UP), ("to", 0.1, "#{p}tumble_w", {"x": 960, "duration": 3.4, "ease": "none"}, "the trunk tip moves along"), ("show", "w:Bubble,", "bu"),
          ("to", "w:Bubble,", "#{p}bu_w", {"y": "-=40", "duration": .5, "yoyo": True, "repeat": 3}, "")]),
    S("river", (1090, 700, 1000), "Let's count his bubbles. One, two, three!", part=3, q=True, tag="count the bubbles", actors=[("tumble", "tumble", 960, 1263, .62)], pcam=(1150, 640, 1300),
      props=RV() + [prop("b1", bubbles, 1000, 800, .9, True), prop("b2", bubbles, 1180, 760, .9, True), prop("b3", bubbles, 1360, 800, .9, True)],
      fx=[("to", 0, "#{p}tumble-trunk", UP), ("show", "w:One,", "b1"), ("show", "w:two,", "b2"), ("show", "w:three!", "b3")],
      words=[("w:One,", "1", .42, .16, 1.8, "sun", (.3, .33), 1.3), ("w:two,", "2", .59, .12, 1.8, "sun", (.52, .31), 1.3), ("w:three!", "3", .77, .16, 1.8, "sun", (.74, .33), 1.3)]),
    S("river", (1000, 640, 1500), "And out he comes. Drip, drip, drip!", part=3, tag="out he comes", actors=[("tumble", "tumble", 900, 1263, .62)], pcam=(1010, 560, 1500), props=RV() + [prop("dr", drops, 850, 620, 1.6, True)],
      fx=[("to", 0, "#{p}tumble-trunk", UP), ("to", 0.1, "#{p}tumble_w", {"y": 930, "duration": 1.5, "ease": "power1.out"}, "Tumble comes out of the water"),
          ("to", 0.1, "#{p}tumble-trunk", {"rotation": 0, "scaleY": 1, "duration": 1.5}, ""), ("show", "w:Drip,", "dr"), ("to", "w:Drip,", "#{p}dr_w", {"y": "+=60", "duration": .35, "yoyo": True, "repeat": 5}, "")],
      words=[("w:Drip,", "DRIP!", .2, .2, 1.2, "", (.5, .31))]),
    S("river", RTC, "Tumble flaps his big ears. Flap, flap, flap!", part=3, tag="ears", hide=["milo", "mama"], pcam=RTV, props=RV(),
      fx=[("to", "w:Flap,", "#{p}tumble-ear", {"rotation": -16, "svgOrigin": "250 -590", "duration": .13, "yoyo": True, "repeat": 13}, "Tumble flaps his ears"), ("face", 0.05, "tumble", "happy")],
      words=[("w:Flap,", "FLAP!", .82, .2, 1.2, "sun", (.5, .31))]),
    S("river", (800, 560, 1300), "What did Tumble breathe with? His trunk, or his tail?", part=3, q=True, tag="question 3", pause=3.4, hide=["milo", "mama"], pcam=WV("river", ["tumble"], pad=.16), props=RV(),
      fx=[("signs", "w:trunk,", ["TRUNK", "TAIL"], 0, "wait:3.0"), ("trunk", "wait:3.05", "tumble", -100, .3)]),
    S("river", RTC, "His trunk! Just like a snorkel.", part=3, tag="his trunk!", hide=["milo", "mama"], pcam=RTV, props=RV(), words=[("w:trunk!", "TRUNK!", .74, .2, 1.3, "sun", (.5, .31))],
      fx=[("to", 0, "#{p}tumble-trunk", {"rotation": -100, "svgOrigin": TP, "duration": .01}), ("hop", "w:trunk!", "tumble")]),
    S("zoo_eve", WIDE, "The sun goes down. Tumble walks home with Mama.", part=3, trans="iris", tag="evening wide", cam2=(1000, 560, 1780), pcam=ZTP, pcam2=WV("zoo_eve", ["tumble", "mama"], floor=.7),
      move={"tumble": (380, 940, .6)}, fx=[("walk", 0, "tumble", 320, 3.0)], words=[("w:home", "HOME", .5, .16, 1.2, "sun")]),
    S("zoo_eve", (1150, 620, 1100), "Tumble is tired. He comes close to Mama.", part=3, tag="tired", actors=HUG, pcam=HUGP, pcam2=HUGP, fx=[("face", 0.05, "tumble", "sleepy"), ("lookat", "w:close", "mama", 6)],
      words=[("w:tired.", "YAWN", .2, .2, 1.0, "", (.3, .31))]),
    S("zoo_eve", (1150, 620, 1100), "Mama reaches out her trunk, and strokes him gently.", part=3, tag="strokes", actors=HUG, pcam=HUGP, pcam2=HUGP,
      fx=[("trunk", "w:reaches", "mama", -74, .7), ("to", "w:strokes", "#{p}mama-trunk", {"rotation": -65, "duration": .4, "yoyo": True, "repeat": 5}, "Mama strokes Tumble"), ("face", "w:gently.", "tumble", "happy")],
      words=[("w:gently.", "GENTLY", .2, .2, 1.0, "pill", (.3, .31))]),
    S("paper_pink", (960, 520, 1500), "Elephants stroke each other with their trunks.", part=3, tag="board: stroke", actors=[("a", "elephant", 1330, 950, .75, True), ("b", "tumble", 600, 950, .62)], pcam=(960, 480, 2400),
      props=[prop("h1", art2.heart, 960, 380, 1.3, True)], fx=[("trunk", 0.2, "a", -35, .6), ("trunk", 0.2, "b", -40, .6), ("show", "w:trunks.", "h1")],
      words=[("w:stroke", "STROKE", .5, .12, 1.1, "", (.5, .31))]),
    S("zoo_eve", (1150, 620, 1100), "It is like a hug. A trunk hug!", part=3, tag="trunk hug", actors=HUG, pcam=HUGP, pcam2=HUGP, props=[prop("h1", art2.heart, 1010, 430, 1.2, True), prop("h2", art2.heart, 1140, 370, .8, True)],
      fx=[("to", 0, "#{p}mama-trunk", {"rotation": -68, "svgOrigin": TP, "duration": .01}), ("show", "w:hug.", "h1"), ("show", "w:trunk", "h2"), ("face", 0.02, "tumble", "happy")],
      words=[("w:trunk", "TRUNK HUG!", .32, .2, .9, "sun", (.5, .29), .9)]),
    S("zoo_eve", say="Can you give yourself a big hug? Squeeze!", part=3, q=True, tag="hug along", hide=["tumble", "mama"],
      fx=[("to", "w:Squeeze!", "#{p}milo-body", {"scaleX": .9, "scaleY": 1.06, "svgOrigin": "0 0", "duration": .3, "yoyo": True, "repeat": 3}, "Milo hugs himself")],
      words=[("w:Squeeze!", "SQUEEZE!", .76, .22, 1.0, "sun", (.5, .31))], **MILO("zoo_eve")),
    S("zoo_eve", C("zoo_eve", "tumble", "head", 900, 60, 20, HUG), "Tumble feels warm and happy.", part=3, tag="happy", actors=HUG, pcam=V("zoo_eve", "tumble", "head", 1100, 60, 40, HUG),
      props=[prop("h1", art2.heart, 880, 500, .8, True)], fx=[("to", 0, "#{p}mama-trunk", {"rotation": -68, "svgOrigin": TP, "duration": .01}), ("face", 0.02, "tumble", "happy"), ("show", "w:happy.", "h1")]),
    S("paper_pink", JCAM, "Five, snorkel. Six, hug. Six trunk jobs!", part=3, tag="board: jobs 5 6", pcam=JPCAM, props=jobs((0, 1, 2, 3), (4, 5)),
      fx=[("show", "w:Five,", "j4"), ("show", "w:Six,", "j5")], words=[("w:Five,", "5", .73, .22, 1.5, "sun", (.5, .565), 1.1), ("w:Six,", "6", .885, .22, 1.5, "sun", (.78, .565), 1.1)]),
    S("zoo_eve", say="One nose, six jobs. Wow!", part=3, tag="wow", hide=["tumble", "mama"], fx=[("hop", "w:Wow!", "milo", 2)], words=[("w:Wow!", "WOW!", .76, .22, 1.3, "sun", (.5, .31))], **MILO("zoo_eve")),
    # ---------------------------------------------------------------- QUIZ + RECAP
    S("zoo_eve", WIDE, "Time to remember what we learned!", part=4, tag="quiz time", cam2=(1000, 560, 1760), actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      words=[("w:remember", "QUIZ TIME!", .62, .14, 1.3, "sun", (.5, .31))]),
    S("zoo_eve", (960, 520, 1920), "Is a trunk a nose? Yes, or no?", part=4, q=True, tag="quiz 1", pause=3.2, actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.8")]),
    S("paper", (960, 520, 1500), "Yes! A nose and an upper lip, all in one.", part=4, tag="board: nose again", **BRD, props=[prop("ar", lambda p: art.arrow(p, 1330, 500, 1290, 650), 0, 0, 1)],
      words=[("w:Yes!", "YES!", .2, .2, 1.5, "sun", (.5, .31))], fx=[("trunk", "w:nose", "t", -25, .4), ("trunk", "w:all", "t", 0, .4)]),
    S("zoo_eve", (960, 520, 1920), "Are there bones inside a trunk? Yes, or no?", part=4, q=True, tag="quiz 2", pause=3.2, actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.8")]),
    S("paper_blue", (960, 520, 1500), "No bones! It bends this way and that way.", part=4, tag="board: no bones again", actors=[("t", "tumble", 760, 960, 1.0)], pcam=(895, 480, 1850),
      words=[("w:No", "NO BONES!", .3, .22, 1.0, "sun", (.5, .31))], fx=[("trunk", "w:this", "t", -70, .5), ("trunk", "w:that", "t", 30, .5)]),
    S("paper_blue", (960, 540, 1600), "What does Tumble use as a snorkel?", part=4, q=True, tag="quiz 3", pause=1.6, pcam=(960, 480, 1800), props=[prop("sb", art2.snorkel_board, 960, 400, 1.0, p=(960, 430, .7))],
      words=[("end+0.3", "?", .5, .13, 2.2, "sun", (.5, .31), 1.5)], fx=[("to", 0, "#{p}sbe-trunk", UP)]),
    S("paper_blue", (960, 500, 1300), "His trunk!", part=4, tag="board: his trunk", pcam=(960, 480, 1800), props=[prop("sb", art2.snorkel_board, 960, 400, 1.0, p=(960, 430, .7))],
      words=[("w:trunk!", "HIS TRUNK!", .5, .1, 1.2, "sun", (.5, .31), .95)], fx=[("to", 0, "#{p}sbe-trunk", UP)]),
    S("paper_pink", JCAM, "One nose, six jobs. Let's count them!", part=4, tag="board: six jobs", pcam=JPCAM, props=jobs((0, 1, 2, 3, 4, 5), ()), words=[("w:six", "6 JOBS", .5, .2, 1.4, "sun", (.5, .31))]),
    S("paper_pink", JCAM, "Smell, grab, drink,", part=4, tag="board: count 1", pcam=JPCAM, props=jobs((), (0, 1, 2)), fx=[("show", "w:Smell,", "j0"), ("show", "w:grab,", "j1"), ("show", "w:drink,", "j2")]),
    S("paper_pink", JCAM, "spray, snorkel, hug!", part=4, tag="board: count 2", pcam=JPCAM, props=jobs((0, 1, 2), (3, 4, 5)), fx=[("show", "w:spray,", "j3"), ("show", "w:snorkel,", "j4"), ("show", "w:hug!", "j5")]),
    S("zoo_eve", (1150, 620, 1200), "Good night, Tumble. Good night, Mama.", part=4, tag="good night", actors=HUG, pcam=HUGP, pcam2=HUGP, props=[prop("h1", art2.heart, 1010, 440, 1.0, True)],
      fx=[("to", 0, "#{p}mama-trunk", {"rotation": -68, "svgOrigin": TP, "duration": .01}), ("face", 0.02, "tumble", "sleepy"), ("show", "w:Mama.", "h1")]),
    S("zoo_eve", WIDE, "Thank you for learning with me, friends. See you at the zoo!", part=4, tag="goodbye", cam2=(960, 520, 2050), actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      words=[("w:See", "SEE YOU AT THE ZOO!", .6, .17, .95, "pill", (.5, .31), .62)], fx=[("to", 0, "#{p}mama-trunk", {"rotation": -68, "svgOrigin": TP, "duration": .01}), ("hop", "w:zoo!", "milo", 2)]),
]


def T(src, **kw):
    d = dict(next(x for x in SHOTS if x["tag"] == src)); d.update(kw); return d


SHORTS = [
    {"id": "zc_ep02_short1", "title": "Is an Elephant's Trunk a Nose or a Hand?", "band": ("IS A TRUNK", "A NOSE?"), "thumb_text": "SO LONG!", "part": 1,
     "extra_first": [T("hook: the trunk", part=1)]},
    {"id": "zc_ep02_short2", "title": "How Does an Elephant Drink Water?", "band": ("HOW DOES IT", "DRINK?"), "thumb_text": "NOT A STRAW!", "part": 2,
     "extra_first": [S("river", (1180, 660, 1000), "How does an elephant drink water?", part=2, q=True, tag="hook: how to drink", hide=["milo", "tumble"], pcam=RMP, props=RV(),
                       fx=[("to", 0.1, "#{p}mama-trunk", DIP, "Mama's trunk dips into the water")], words=[("w:drink", "?", .2, .2, 2.6, "sun", (.5, .33), 1.6)])]},
    {"id": "zc_ep02_short3", "title": "Can an Elephant Breathe Under Water?", "band": ("WHERE DID", "TUMBLE GO?"), "thumb_text": "PEEKABOO!", "part": 3,
     "extra_first": [S("river", (1167, 720, 1000), "Can an elephant breathe under the water?", part=3, q=True, tag="hook: under the water", actors=[("tumble", "tumble", 900, 1263, .62)], pcam=(1167, 640, 1300), props=RV(),
                       fx=[("to", 0, "#{p}tumble-trunk", UP), ("to", 0.2, "#{p}tumble_w", {"y": "-=14", "duration": .6, "yoyo": True, "repeat": 5}, "the tip of a trunk bobs on the water")],
                       words=[(0.0, "?", .26, .26, 2.6, "sun", (.5, .34), 1.6)])]},
]

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
_UPJS = 'gsap.set("#P-trunk",{rotation:-160,scaleY:1.35,svgOrigin:"392 -430"});'
THUMBS = {
    "zc_ep02": {"place": "savanna", "cam": (960, 540, 1920),
                "actors": [("tumble", 420, 1040, 1.25, False, 'gsap.set("#P-trunk",{rotation:-70,svgOrigin:"392 -430"});')],
                "props": [(art2.fruit, 1335, 470, .95), (lambda p: art.water_drop(p, .8), 1610, 640, 1.0), (art2.heart, 1420, 850, 2.2)],
                "words": [("ONE NOSE?!", 1300, 170, 200, "sun")]},
    "zc_ep02_short1": {"place": "savanna", "cam": (835, 640, 840),
                       "actors": [("tumble", 560, 936, .6, False, 'gsap.set("#P-trunk",{rotation:-62,scaleY:1.25,svgOrigin:"392 -430"});')],
                       "props": [(lambda p: art.arrow(p, 800, 830, 1015, 800), 0, 0, 1)],
                       "words": [("SO LONG!", 540, 440, 210, "sun")]},
    "zc_ep02_short2": {"place": "river", "cam": (1230, 480, 1700),
                       "actors": [("elephant", 1500, 905, .8, True, 'gsap.set("#P-trunk",{scaleY:1.38,svgOrigin:"392 -430"});')],
                       "props": [(water, 960, 850, 1.0), (cup, 905, 720, 1.3), (crossx, 905, 600, 1.1)],
                       "words": [("NOT A", 540, 340, 170, ""), ("STRAW!", 540, 520, 200, "sun")]},
    "zc_ep02_short3": {"place": "river", "cam": (1167, 640, 1300),
                       "actors": [("tumble", 900, 1263, .62, False, _UPJS)],
                       "props": [(water, 960, 850, 1.0), (lambda p: art.arrow(p, 1330, 600, 1215, 770), 0, 0, 1)],
                       "words": [("PEEKABOO!", 540, 520, 170, "sun")]},
}
