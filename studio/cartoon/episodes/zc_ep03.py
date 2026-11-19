"""zc_ep03: "Why Do Elephants Have Such Big Ears?" - cartoon fact lesson with Milo, Tumble the baby elephant and his mama (3D music-and-sync process: "beat").
Three parts, each cut whole into one Short: 1. how big, what shape, 2. ears that cool, 3. more ways to keep cool (a drink and a swim).

FACTS, read at the source on Nov 17 2026, about 7:45 PM ET:
 [SDZ] San Diego Zoo Wildlife Alliance, animals.sandiegozoo.org/animals/elephant
   "African elephants (both species) have large ears shaped like the continent of Africa,"   "Asian elephants have smaller ears,"
   "An elephant's ears work like a radiator."   "As elephants flap their ears on a hot day, their blood flows through many blood vessels ... spread throughout their large ears and cools down."
   "This ear flapping behavior cools their large bodies on warm days."
   "the elephant sucks water only part way up the trunk, curls it toward its mouth, tilts its head up, and lets the water from the trunk pour in."
 [WWF] worldwildlife.org, "10 most-asked elephant questions - answered by an expert"
   "In the wild, they may swim across rivers, lakes, and even between islands to cool off or play."
 Not read today, so NOT said: smelling water far away, the trunk as a snorkel (shown only as a picture of Tumble swimming), stroking with the trunk.
 "Elephants cannot fly" and "a bird is much smaller than an elephant's ear" are plain observations, not quotes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
from kit import Kit, S, prop, W
from episodes.zc_ep02 import water, RV, drops, curl, tube, bubbles, crossx, DIP, UP, TP

EP = {"id": "zc_ep03", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "Why Do Elephants Have Such Big Ears?", "thumb_text": "LIKE A FAN?!", "series": "Animal Facts with Milo",
      "description": ("Why do elephants have such big ears? Are they for flying, or for keeping cool? Milo the bluebird visits baby elephant Tumble and his mama to find out! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn that African elephants have large ears shaped like Africa, that Asian elephants have smaller ears, "
                      "that flapping their ears cools an elephant's big body on warm days, and that elephants also drink and swim to cool off.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (elephant); WWF (10 most-asked elephant questions)."),
      "tags": ["elephant", "elephants for kids", "elephant ears", "baby elephant", "why do elephants have big ears", "savanna animals for kids", "animal facts for kids",
               "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "zoo": [("milo", "milo", 960, 940, 1.1, False, False)],
    "savanna": [("mama", "elephant", 1560, 930, .9, True), ("tumble", "tumble", 560, 936, .6), ("milo", "milo", 230, 490, .78, False, True)],
    "bigtree": [("mama", "elephant", 1450, 930, .85, True), ("tumble", "tumble", 560, 936, .6), ("milo", "milo", 300, 400, .75, False, True)],
    "jungle": [("tumble", "tumble", 900, 930, .66), ("milo", "milo", 380, 470, .78, False, True)],
    "river": [("mama", "elephant", 1500, 905, .8, True), ("tumble", "tumble", 560, 905, .55), ("milo", "milo", 300, 400, .7, False, True)],
    "zoo_eve": [("mama", "elephant", 1560, 932, .9, True), ("tumble", "tumble", 700, 940, .6), ("milo", "milo", 300, 420, .7, False, True)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
HUG = [("mama", "elephant", 1560, 944, .9, True), ("tumble", "tumble", 760, 940, .6)]
WIDE = (960, 540, 1920)
E = art2.ELE; INK = art.INK
EAR = "250 -590"
FLAP = lambda at, who="tumble", n=7, d=.18: ("to", at, "#{p}" + who + "-ear", {"rotation": 14, "svgOrigin": EAR, "duration": d, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, f"{who} flaps its ears")
SMALL_EAR = lambda who: ("to", 0, "#{p}" + who + "-ear", {"scale": .5, "svgOrigin": "256 -460", "duration": .01}, "")      # an Asian elephant: the same elephant with a smaller ear
SUN_S = lambda x=1500, y=220, s=.8: prop("hs", art3.hot_sun, x, y, s)
SPIN = ("to", 0.05, "#{p}hs-rays", {"rotation": 60, "transformOrigin": "50% 50%", "duration": 6, "ease": "none"}, "")


# ------------------------------------------------------------------ pictures for the boards
def africa(pid, col="#f2c45a"):
    """The continent of Africa, simply drawn (Madagascar beside it)."""
    pts = [(-150, -300), (-60, -312), (40, -302), (120, -292), (172, -272), (200, -180), (250, -110), (332, -92), (262, -20), (212, 60), (184, 150), (134, 230), (82, 292),
           (22, 312), (-30, 282), (-60, 182), (-52, 82), (-82, 2), (-132, -28), (-222, -48), (-282, -110), (-292, -182), (-242, -262)]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts) + "Z"
    return (f'<g id="{pid}"><path d="{d}" fill="{col}" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>'
            f'<ellipse cx="262" cy="182" rx="22" ry="56" transform="rotate(18 262 182)" fill="{col}" stroke="{INK}" stroke-width="9"/></g>')


def ear_shape(pid, col=None):
    """A big African elephant ear, drawn in the shape of Africa (grey edge, pink inside), for the boards and the thumbnail."""
    pts = [(-150, -300), (-60, -312), (40, -302), (120, -292), (172, -272), (200, -180), (250, -110), (332, -92), (262, -20), (212, 60), (184, 150), (134, 230), (82, 292),
           (22, 312), (-30, 282), (-60, 182), (-52, 82), (-82, 2), (-132, -28), (-222, -48), (-282, -110), (-292, -182), (-242, -262)]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts) + "Z"
    return (f'<g id="{pid}"><path d="{d}" fill="{col or E["fill"]}" stroke="{E["line"]}" stroke-width="16" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{E["ear"]}" transform="translate(4 8) scale(.72)"/></g>')


def waves(pid):
    return f'<g id="{pid}">' + "".join(f'<path d="M-120 {y} q30 -24 60 0 q30 24 60 0 q30 -24 60 0 q30 24 60 0" stroke="#2f8fd0" stroke-width="14" fill="none" stroke-linecap="round"/>' for y in (-30, 20)) + '</g>'


def breeze(pid):
    """Cool air leaving the ear: three soft blue curls."""
    return f'<g id="{pid}">' + "".join(f'<path d="M0 {y} q60 -26 120 0 q60 26 120 0" stroke="#7cc8f2" stroke-width="15" fill="none" stroke-linecap="round" opacity=".9"/>' for y in (-60, 0, 60)) + '</g>'


def wing(pid):
    """A bird's wing, for 'big ears are not wings'."""
    return (f'<g id="{pid}"><path d="M-160 20 C-80 -120 80 -150 170 -90 C110 -70 120 -30 60 -20 C100 0 80 30 20 30 C40 50 0 70 -40 60Z" fill="{art.MILO_BLUE}" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/></g>')


def way(k):
    """One of the three ways to keep cool as a round picture: flap the ears, drink, swim."""
    def f(pid):
        ic = [f'<g transform="translate(-26 4) scale(.24)">{ear_shape(pid + "i")}</g><g transform="translate(18 -40) scale(.28)">{breeze(pid + "b")}</g>',
              f'<g transform="translate(0 16) scale(.62)">{art.water_drop(pid + "i")}</g>',
              f'<g transform="translate(0 10) scale(.75)">{waves(pid + "i")}</g>'][k]
        return f'<g id="{pid}"><circle r="108" fill="#fff" stroke="{INK}" stroke-width="10"/>{ic}</g>'
    return f


WX = [600, 960, 1320]; WP = [(960, 520), (960, 760), (960, 1000)]
WCAM = (960, 520, 1500); WPCAM = (960, 640, 1700)


def ways(shown, new=()):
    return [prop(f"w{k}", way(k), WX[k], 560, 1.15, k in new, p=(*WP[k], 1.0)) for k in range(3) if k in shown or k in new]


TUP = (700, 626, 1200); MAP = WV("savanna", ["mama"]); BTP = WV("bigtree", ["tumble", "mama"], pad=.03)
RTP = WV("river", ["tumble"]); RMP = WV("river", ["mama"]); ZTP = WV("zoo_eve", ["tumble"]); HUGP = (1208, 400, 2600)
TC = C("savanna", "tumble", "head", 880, 0, 20); TV = V("savanna", "tumble", "head", 1000, -30, 40)
MC = C("savanna", "mama", "head", 960, 100, 70); MV = V("savanna", "mama", "head", 1150, 80, 60)
RTC = C("river", "tumble", "head", 880, 60, 30); RTV = V("river", "tumble", "head", 1000, 60, 40)
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 900))
EB = dict(props=[prop("eb", art3.ear_board, 960, 640, .9, p=(960, 700, .8))], pcam=(960, 480, 1700))        # the ear board (#{p}ebe-ear moves)
SHAPE = (960, 520, 1700); SHAPEP = (960, 560, 1900)
TWO = [("af", "elephant", 620, 900, .7), ("as", "elephant", 1360, 900, .7)]       # an African and an Asian elephant side by side

SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("savanna", TC, "Why does Tumble have such big ears?", q=True, tag="hook: big ears", hide=["milo", "mama"], pcam=TV,
      words=[("w:ears?", "?", .2, .3, 3.0, "sun", (.75, .36), 1.6)], fx=[FLAP("w:big", n=5)]),
    S("savanna", TC, "Are they for flying? Or for keeping cool?", tag="hook: guesses", hide=["milo", "mama"], pcam=TV,
      words=[("w:flying?", "FLYING?", .22, .22, 1.0, "", (.3, .29), .8), ("w:cool?", "COOL?", .22, .45, 1.0, "sun", (.7, .29), .8)], fx=[FLAP("w:flying?", n=3), ("face", "w:cool?", "tumble", "wow")]),
    S("savanna", say="I'm Milo. Let's find out together!", tag="hook: Milo", hide=["tumble", "mama"], fx=[("hop", "w:find", "milo")], **MILO("savanna")),
    # ---------------------------------------------------------------- INTRO
    S("zoo", WIDE, "Welcome to The Animated Zoo, friends!", trans="iris", tag="gate wide", words=[("w:Animated", "HELLO!", .74, .6, 1.2, "pill")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, -40), "Today we fly to the sunny savanna.", tag="Milo close", words=[("w:savanna.", "THE SAVANNA", .5, .16, 1.1, "sun")]),
    S("savanna", WIDE, "Here we are! Look who is waiting for us.", trans="iris", tag="savanna wide", cam2=(960, 560, 1840), pcam=TUP, pcam2=MAP,
      fx=[("fromto", 0, "#{p}milo_w", {"x": -300, "y": 200}, {"x": 230, "y": 490, "duration": 1.3, "ease": "power2.out"}, "Milo flies in")]),
    S("savanna", (1110, 560, 1640), "This is Tumble. Tumble is a baby elephant.", tag="this is Tumble", hide=["milo"], pcam=TUP, words=[("w:Tumble.", "TUMBLE", .3, .26, 1.0, "pill", (.5, .31))], fx=[("hop", "w:Tumble.", "tumble")]),
    S("savanna", MC, "And this is Tumble's mama. Hello, Mama!", tag="Mama close", hide=["milo"], pcam=MAP, fx=[("nod", "w:Hello,", "mama")],
      words=[("w:Hello,", "MAMA", .8, .16, 1.0, "pill", (.5, .31))]),
    # ---------------------------------------------------------------- PART 1: how big, what shape
    S("savanna", MC, "Look at Mama's ears. They are so, so big!", part=1, tag="Mama's big ears", hide=["milo", "tumble"], pcam=MV,
      words=[("w:big!", "BIG EARS!", .8, .16, 1.1, "sun", (.5, .31))], fx=[FLAP("w:ears.", "mama", n=5, d=.22)]),
    S("paper", (960, 540, 1600), "African elephants have very large ears.", part=1, tag="board: large ears", **EB,
      words=[("w:large", "LARGE!", .78, .2, 1.4, "sun", (.5, .37), 1.1)], fx=[FLAP("w:large", "ebe", n=5, d=.22)]),
    S("savanna", say="Where are your ears? Can you touch your ears?", part=1, q=True, tag="touch your ears", hide=["tumble", "mama"], pause=1.0, fx=[("hop", "w:touch", "milo")],
      words=[("w:touch", "TOUCH!", .76, .24, 1.0, "sun", (.5, .31))], **MILO("savanna")),
    S("paper_blue", (960, 540, 1600), "Mama's ear is much bigger than me!", part=1, tag="board: ear and Milo",
      props=[prop("es", ear_shape, 720, 560, .85, p=(960, 520, .75))], actors=[("m", "milo", 1350, 760, .55, False, True)], pcam=(1060, 560, 1750),
      words=[("w:bigger", "BIGGER!", .78, .2, 1.2, "sun", (.5, .37), 1.0)], fx=[("hop", "w:me!", "m")]),
    S("paper_blue", (960, 540, 1600), "Let's count birds up the ear. One, two, three! Still more ear!", part=1, q=True, tag="board: count up the ear",
      props=[prop("es", ear_shape, 720, 560, .85, p=(900, 560, .75)), prop("b1", lambda p: art.milo(p), 1270, 850, .32, True, p=(1200, 820, .3)), prop("b2", lambda p: art.milo(p), 1270, 690, .32, True, p=(1200, 660, .3)),
             prop("b3", lambda p: art.milo(p), 1270, 530, .32, True, p=(1200, 500, .3))], pcam=(1000, 560, 1750),
      fx=[("show", "w:One,", "b1"), ("show", "w:two,", "b2"), ("show", "w:three!", "b3")],
      words=[("w:One,", "1", .78, .7, 1.2, "sun", (.82, .62), .9), ("w:two,", "2", .78, .5, 1.2, "sun", (.82, .48), .9), ("w:three!", "3", .78, .3, 1.2, "sun", (.82, .34), .9)]),
    S("paper_blue", SHAPE, "And look at the shape. Can you see it?", part=1, q=True, tag="board: the shape", pause=1.0, props=[prop("es", ear_shape, 960, 540, .85, p=(960, 600, .9))], pcam=SHAPEP,
      fx=[("to", "w:shape.", "#{p}es_w", {"scale": 1.08, "transformOrigin": "50% 50%", "duration": .3, "yoyo": True, "repeat": 3}, "the ear pulses")], words=[("w:shape.", "SHAPE?", .8, .2, 1.2, "", (.5, .37))]),
    S("paper_blue", SHAPE, "It looks like a map of Africa!", part=1, tag="board: like Africa",
      props=[prop("es", ear_shape, 600, 560, .75, p=(960, 380, .6)), prop("af", africa, 1360, 560, .72, True, p=(960, 830, .6))], pcam=SHAPEP,
      fx=[("show", "w:Africa!", "af")], words=[("w:map", "AFRICA", .76, .16, 1.2, "sun", (.5, .62), 1.0)]),
    S("paper_blue", SHAPE, "African elephants have ears shaped like Africa.", part=1, tag="board: shaped like Africa",
      props=[prop("es", ear_shape, 600, 560, .75, p=(960, 380, .6)), prop("af", africa, 1360, 560, .72, p=(960, 830, .6))], pcam=SHAPEP,
      fx=[("to", "w:shaped", "#{p}es_w,#{p}af_w", {"y": "-=24", "duration": .3, "yoyo": True, "repeat": 3}, "both bob")], words=[("w:shaped", "SAME SHAPE!", .5, .14, 1.0, "pill", (.5, .62), .8)]),
    S("paper_pink", (960, 520, 1800), "Asian elephants live far away. They have smaller ears.", part=1, tag="board: smaller ears", actors=TWO, pcam=(990, 520, 2700),
      fx=[SMALL_EAR("as"), FLAP("w:smaller", "as", n=3), FLAP("w:smaller", "af", n=3)],
      words=[("w:Asian", "ASIAN", .7, .18, 1.0, "", (.68, .31), .7), ("w:smaller", "SMALLER", .7, .3, 1.0, "sun", (.68, .37), .7)]),
    S("paper_pink", (960, 520, 1800), "Which one has bigger ears? This one, or that one?", part=1, q=True, tag="question 1", pause=3.2, actors=TWO, pcam=(990, 520, 2700),
      fx=[SMALL_EAR("as"), ("signs", "w:This", ["THIS", "THAT"], 0, "wait:2.0")]),
    S("paper_pink", (960, 520, 1800), "This one! The African elephant, like Mama and Tumble.", part=1, tag="answer 1", actors=TWO, pcam=(990, 520, 2700),
      fx=[SMALL_EAR("as"), FLAP("w:This", "af", n=5)], words=[("w:African", "AFRICAN", .3, .18, 1.0, "sun", (.32, .31), .7)]),
    S("savanna", TC, "Tumble's ears are big, and they can move. Flap, flap!", part=1, tag="Tumble flaps", hide=["milo", "mama"], pcam=TV,
      fx=[("face", 0.05, "tumble", "happy"), FLAP("w:Flap,", n=7)], words=[("w:Flap,", "FLAP!", .82, .2, 1.2, "sun", (.5, .31))]),
    S("savanna", (1110, 560, 1640), "Tumble's ears are big. But Mama's ears are even bigger!", part=1, tag="Tumble and Mama", hide=["milo"], pcam=TUP, pcam2=MAP,
      fx=[FLAP("w:Tumble's", n=3), FLAP("w:Mama's", "mama", n=3, d=.24)], words=[("w:bigger!", "BIGGER!", .7, .2, 1.1, "sun", (.5, .31))]),
    S("savanna", (1110, 520, 1700), "Who has bigger ears, Tumble or Mama?", part=1, q=True, tag="question 1b", pause=3.2, hide=["milo"], pcam=TUP,
      fx=[("signs", "w:Tumble", ["TUMBLE", "MAMA"], 1, "wait:2.0")]),
    S("savanna", MC, "Mama! She is big, and her ears are big too.", part=1, tag="answer 1b", hide=["milo", "tumble"], pcam=MV,
      fx=[("nod", "w:Mama!", "mama"), FLAP("w:ears", "mama", n=3, d=.24)], words=[("w:Mama!", "MAMA!", .8, .16, 1.2, "sun", (.5, .31))]),
    S("savanna", (760, 600, 1200), "Can Tumble fly with his big ears? He tries. Flap, flap, jump!", part=1, q=True, tag="Tumble tries to fly", hide=["milo", "mama"], pcam=TUP,
      fx=[FLAP("w:tries.", n=9, d=.12), ("hop", "w:jump!", "tumble")], words=[("w:fly", "FLY?", .8, .2, 1.3, "", (.5, .31))]),
    S("savanna", TC, "Bump! No. Elephants cannot fly.", part=1, tag="cannot fly", hide=["milo", "mama"], pcam=TV,
      fx=[("face", "w:No.", "tumble", "wow"), ("face", "w:Elephants", "tumble", "happy")], words=[("w:cannot", "NO FLYING!", .82, .2, 1.0, "pill", (.5, .31))]),
    S("paper", (960, 540, 1500), "Big ears are not wings.", part=1, tag="board: not wings",
      props=[prop("wg", wing, 960, 560, 1.4, p=(960, 600, 1.3)), prop("x", crossx, 960, 560, 1.1, True, p=(960, 600, 1.0))], pcam=(960, 480, 1700),
      fx=[("show", "w:not", "x")], words=[("w:wings.", "NOT WINGS", .5, .14, 1.2, "sun", (.5, .37), .9)]),
    S("savanna", say="Can you flap your hands like big ears? Flap, flap, flap!", part=1, q=True, tag="flap along", hide=["tumble", "mama"], fx=[("hop", "w:Flap,", "milo", 2)],
      words=[("w:Flap,", "FLAP!", .76, .22, 1.0, "sun", (.5, .31))], **MILO("savanna")),
    S("savanna", (1110, 520, 1700), "So what are big ears for? Let's find out!", part=1, q=True, tag="what for", hide=["milo"], pcam=TUP,
      fx=[FLAP("w:ears", "tumble", n=3), FLAP("w:ears", "mama", n=3)], words=[("w:for?", "?", .5, .2, 2.4, "sun", (.5, .32), 1.5)]),
    # ---------------------------------------------------------------- PART 2: ears that cool
    S("savanna", WIDE, "Phew! The sun is hot on the savanna.", part=2, trans="iris", tag="hot savanna", cam2=(960, 560, 1840), pcam=TUP, pcam2=MAP, hide=["milo"],
      props=[SUN_S(), prop("ht", art3.heat, 1000, 600, 1.0, True)], fx=[SPIN, ("show", "w:hot", "ht")], words=[("w:hot", "HOT!", .5, .16, 1.3, "sun", (.5, .31))]),
    S("savanna", TC, "Tumble feels hot, hot, hot.", part=2, tag="Tumble is hot", hide=["milo", "mama"], pcam=TV,
      props=[prop("sw", art3.sweat, *P("savanna", "tumble", "top", 130, 20), .7, True)], fx=[("face", 0.05, "tumble", "sad"), ("show", "w:hot,", "sw")]),
    S("savanna", MC, "Watch Mama. She flaps her big ears. Flap, flap, flap!", part=2, tag="Mama flaps", hide=["milo", "tumble"], pcam=MV,
      fx=[FLAP("w:flaps", "mama", n=13, d=.22)], words=[("w:Flap,", "FLAP!", .8, .16, 1.2, "sun", (.5, .31))]),
    S("savanna", TC, "Tumble flaps his ears, too. Ahh, that feels nice.", part=2, tag="Tumble copies", hide=["milo", "mama"], pcam=TV,
      fx=[FLAP("w:flaps", n=11), ("face", "w:Ahh,", "tumble", "happy")], words=[("w:nice.", "AHH!", .82, .2, 1.2, "", (.5, .31))]),
    S("jungle", WIDE, "Tumble walks into the green jungle. It is still so hot!", part=2, trans="iris", tag="jungle wide", cam2=(1040, 560, 1760), pcam=WV("jungle", ["tumble"]), pcam2=W(WV("jungle", ["tumble"])), hide=["milo"],
      move={"tumble": (640, 930, .66)}, fx=[("walk", 0.1, "tumble", 260, 3.0), ("face", "w:hot!", "tumble", "sad")], words=[("w:hot!", "STILL HOT!", .5, .16, 1.0, "pill", (.5, .31))]),
    S("jungle", C("jungle", "tumble", "head", 900, -40, 20), "Flap, flap, flap! His ears make a little wind.", part=2, tag="a little wind", hide=["milo"], pcam=V("jungle", "tumble", "head", 1050, -40, 40),
      props=[prop("wd", art3.wind, 760, 600, .7, True)], fx=[FLAP("w:Flap,", n=11), ("show", "w:wind.", "wd"), ("to", "w:wind.", "#{p}wd_w", {"x": "-=160", "duration": .9, "repeat": 1, "ease": "none"}, "the wind blows")],
      words=[("w:wind.", "WIND!", .2, .2, 1.2, "sun", (.5, .31))]),
    S("jungle", C("jungle", "tumble", "all", 1000, 30, -40), "How many ears does Tumble have? One, or two?", part=2, q=True, tag="question 2a", pause=3.2, hide=["milo"], pcam=V("jungle", "tumble", "all", 1300, 30, 0),
      fx=[("signs", "w:One,", ["ONE", "TWO"], 1, "wait:2.0")]),
    S("jungle", C("jungle", "tumble", "head", 900, -40, 20), "Two! Two big ears to flap.", part=2, tag="answer 2a", hide=["milo"], pcam=V("jungle", "tumble", "head", 1050, -40, 40),
      fx=[FLAP("w:Two!", n=5), ("face", 0.05, "tumble", "happy")], words=[("w:Two!", "2 EARS!", .2, .2, 1.2, "sun", (.5, .31))]),
    S("jungle", say="Big ears flap like a fan on a hot day. Whoosh, whoosh!", part=2, tag="like a fan", hide=["tumble"], fx=[("hop", "w:Whoosh,", "milo", 2)],
      words=[("w:fan", "LIKE A FAN", .76, .22, .9, "pill", (.5, .31), .8)], **MILO("jungle")),
    S("paper_blue", (960, 540, 1600), "An elephant's ears help it stay cool.", part=2, tag="board: ears cool", **EB,
      fx=[FLAP("w:ears", "ebe", n=7, d=.2)], words=[("w:cool.", "COOL!", .78, .2, 1.4, "sun", (.5, .37), 1.1)]),
    S("paper_blue", (960, 540, 1600), "When an elephant flaps its ears, the ears cool down.", part=2, tag="board: the ears cool down",
      props=[prop("eb", art3.ear_board, 960, 640, .9, p=(960, 700, .8)), prop("bz", breeze, 640, 420, 1.0, True, p=(700, 470, .8))], pcam=(960, 480, 1700),
      fx=[FLAP("w:flaps", "ebe", n=9, d=.2), ("show", "w:cool", "bz"), ("to", "w:cool", "#{p}bz_w", {"x": "-=80", "duration": .8, "repeat": 2, "ease": "none"}, "the cool air")],
      words=[("w:down.", "COOL EARS", .78, .2, 1.1, "pill", (.5, .37), .9)]),
    S("paper_blue", (960, 540, 1600), "And that cools the whole big body.", part=2, tag="board: the whole body",
      props=[prop("eb", art3.ear_board, 960, 640, .9, p=(960, 700, .8)), prop("ar", lambda p: art.arrow(p, 960, 520, 700, 720), 0, 0, 1, True)], pcam=(960, 480, 1700),
      fx=[FLAP(0.1, "ebe", n=7, d=.2), ("show", "w:cools", "ar")], words=[("w:whole", "WHOLE BODY!", .78, .2, 1.0, "sun", (.5, .37), .85)]),
    S("savanna", (1110, 520, 1700), "Do big ears help an elephant keep warm, or keep cool?", part=2, q=True, tag="question 2", pause=3.2, hide=["milo"], pcam=TUP,
      fx=[("signs", "w:warm,", ["WARM", "COOL"], 1, "wait:2.0"), FLAP("wait:2.05", "mama", n=5)]),
    S("savanna", TC, "Keep cool! Flap, flap, cool.", part=2, tag="answer 2", hide=["milo", "mama"], pcam=TV,
      fx=[FLAP("w:Flap,", n=7), ("hop", "w:cool.", "tumble"), ("face", 0.05, "tumble", "happy")], words=[("w:cool!", "COOL!", .82, .2, 1.3, "sun", (.5, .31))]),
    S("savanna", say="Can you fan your face with your hands? Ahh, nice and cool!", part=2, q=True, tag="fan along", hide=["tumble", "mama"],
      fx=[("hop", "w:fan", "milo", 2)], words=[("w:Ahh,", "AHH!", .76, .22, 1.2, "sun", (.5, .31))], **MILO("savanna")),
    S("bigtree", WIDE, "On warm days, elephants flap their ears a lot.", part=2, trans="iris", tag="bigtree wide", cam2=(1000, 560, 1780), pcam=BTP, pcam2=W(BTP), hide=["milo"],
      fx=[FLAP(0.2, "tumble", n=13), FLAP(0.4, "mama", n=11, d=.24)], words=[("w:lot.", "A LOT!", .5, .16, 1.2, "sun", (.5, .31))]),
    S("bigtree", (760, 640, 1100), "Let's count Tumble's flaps. One, two, three!", part=2, q=True, tag="count the flaps", hide=["milo", "mama"], pcam=WV("bigtree", ["tumble"]),
      fx=[FLAP("w:One,", n=1, d=.25), FLAP("w:two,", n=1, d=.25), FLAP("w:three!", n=1, d=.25)],
      words=[("w:One,", "1", .3, .3, 1.6, "sun", (.3, .31), 1.2), ("w:two,", "2", .5, .26, 1.6, "sun", (.5, .37), 1.2), ("w:three!", "3", .7, .3, 1.6, "sun", (.7, .31), 1.2)]),
    S("bigtree", C("bigtree", "mama", "head", 900, 100, 60), "Mama flaps her ears slowly. Flap... flap... flap.", part=2, tag="Mama slowly", hide=["milo", "tumble"], pcam=V("bigtree", "mama", "head", 1150, 80, 60),
      fx=[FLAP("w:flaps", "mama", n=5, d=.6), ("blinkslow", "w:slowly.", "mama-eye", 1)], words=[("w:slowly.", "SLOWLY", .8, .16, 1.1, "pill", (.5, .31))]),
    S("bigtree", (1000, 640, 1500), "Tumble and Mama rest in the shade of the big tree.", part=2, tag="rest in the shade", hide=["milo"], pcam=BTP,
      fx=[("face", 0.05, "tumble", "sleepy"), FLAP("w:shade", "mama", n=3, d=.5), FLAP("w:tree.", "tumble", n=3, d=.4)], words=[("w:shade", "SHADE", .5, .16, 1.2, "pill", (.5, .31))]),
    S("bigtree", (1000, 600, 1500), "Now they feel cool. Big ears, big job!", part=2, tag="big job", hide=["milo"], pcam=BTP,
      fx=[("face", 0.05, "tumble", "happy"), ("hop", "w:job!", "tumble"), ("nod", "w:job!", "mama")], words=[("w:job!", "BIG JOB!", .5, .16, 1.2, "sun", (.5, .31))]),
    S("paper_pink", WCAM, "That is one way to keep cool. One, flap your ears.", part=2, tag="board: way 1", pcam=WPCAM, props=ways((), (0,)),
      fx=[("show", "w:One,", "w0")], words=[("w:One,", "1", .2, .25, 1.6, "sun", (.24, .43), 1.1)]),
    # ---------------------------------------------------------------- PART 3: a drink and a swim
    S("river", WIDE, "Tumble and Mama walk to the cool river.", part=3, trans="iris", tag="river wide", cam2=(1000, 560, 1780), pcam=RTP, pcam2=RMP, props=RV(), hide=["milo"],
      move={"tumble": (260, 905, .55), "mama": (1800, 905, .8, True)}, fx=[("walk", 0, "tumble", 300, 3.0), ("walk", 0, "mama", -300, 3.0)], words=[("w:river.", "RIVER", .5, .16, 1.3, "sun")]),
    S("river", (1360, 639, 960), "Time for a cool drink. Watch Mama's trunk!", part=3, tag="watch Mama", hide=["milo"], pcam=RMP, props=RV(),
      fx=[("trunk", "w:Watch", "mama", -30, .4), ("trunk", "e:trunk!", "mama", 0, .4)], words=[("w:Watch", "WATCH!", .8, .16, 1.0, "sun", (.5, .31))]),
    S("river", (1180, 660, 1000), "She sucks the water part way up her trunk. Slurp!", part=3, tag="slurp", hide=["milo", "tumble"], pcam=RMP, props=RV(),
      fx=[("to", 0.1, "#{p}mama-trunk", DIP, "Mama's trunk dips into the water"), ("lookat", 0.1, "mama", 6)], words=[("w:Slurp!", "SLURP!", .22, .27, 1.3, "sun", (.5, .31))]),
    S("paper_blue", (960, 520, 1400), "Only part of the way up. Not all the way!", part=3, tag="board: part way", props=[prop("tube", tube, 960, 930, 1.3, p=(960, 1000, 1.3))], pcam=(960, 480, 1700),
      fx=[("fromto", "w:part", "#{p}tube-w", {"scaleY": .02, "transformOrigin": "50% 100%"}, {"scaleY": .5, "duration": 1.4, "ease": "power1.out"}, "the water rises half way up")],
      words=[("w:part", "PART WAY", .76, .52, 1.0, "pill", (.5, .37), .8)]),
    S("river", (1180, 660, 1000), "Then she curls her trunk to her mouth,", part=3, tag="curl", hide=["milo", "tumble"], pcam=RMP, props=RV() + [prop("curl", lambda p: curl(p, True), 1500, 905, .8, True)],
      fx=[("to", "w:curls", "#{p}mama-trunk", {"opacity": 0, "duration": .15}, "Mama curls her trunk to her mouth"), ("to", "w:curls", "#{p}curl_w", {"opacity": 1, "duration": .15}, "")]),
    S("river", C("river", "mama", "head", 760, -40, 40), "and the water pours in. Glug, glug, glug.", part=3, tag="glug", hide=["milo", "tumble"], pcam=V("river", "mama", "head", 1100, -40, 60),
      props=RV() + [prop("curl", lambda p: curl(p, True), 1500, 905, .8), prop("dr", drops, 1206, 640, 1.0, True)], words=[("w:Glug,", "GLUG!", .8, .2, 1.2, "sun", (.5, .31))],
      fx=[("to", 0, "#{p}mama-trunk", {"opacity": 0, "duration": .01}), ("fromto", "w:Glug,", "#{p}dr_w", {"opacity": 1, "y": 650}, {"y": 610, "opacity": 0, "duration": .4, "repeat": 3}, "the water goes into her mouth")]),
    S("river", (1070, 540, 1560), "Does Mama drink with her trunk, or with her tail?", part=3, q=True, tag="question 3", pause=3.2, hide=["milo"], pcam=RMP, props=RV(),
      fx=[("signs", "w:trunk,", ["TRUNK", "TAIL"], 0, "wait:2.0")]),
    S("river", C("river", "mama", "head", 900, -40, 40), "With her trunk! Ahh, a cool drink.", part=3, tag="answer 3", hide=["milo", "tumble"], pcam=V("river", "mama", "head", 1100, -40, 60), props=RV(),
      fx=[("nod", "w:trunk!", "mama"), ("face", "w:Ahh,", "mama", "happy")], words=[("w:trunk!", "TRUNK!", .8, .2, 1.3, "sun", (.5, .31))]),
    S("river", RTC, "Tumble has a cool drink, too. Slurp, slurp!", part=3, tag="Tumble drinks", hide=["milo", "mama"], pcam=RTV, props=RV(),
      fx=[("to", 0.1, "#{p}tumble-trunk", DIP, "Tumble's trunk dips into the water"), ("face", "w:Slurp,", "tumble", "happy")], words=[("w:Slurp,", "SLURP!", .82, .2, 1.2, "sun", (.5, .31))]),
    S("paper_pink", WCAM, "Two, have a drink.", part=3, tag="board: way 2", pcam=WPCAM, props=ways((0,), (1,)),
      fx=[("show", "w:Two,", "w1")], words=[("w:Two,", "2", .5, .25, 1.6, "sun", (.24, .57), 1.1)]),
    S("river", (1000, 600, 1700), "And now? Tumble walks into the deep water.", part=3, q=True, tag="wading", hide=["milo", "mama"], pcam=(760, 520, 1500), pcam2=(860, 560, 1500), props=RV(),
      fx=[("walk", 0.1, "tumble", 300, 3.6), ("to", 0.1, "#{p}tumble_w", {"y": "+=90", "duration": 3.6, "ease": "none"}, "")], words=[("w:deep", "DEEP", .7, .2, 1.2, "", (.5, .31))]),
    S("river", (1000, 640, 1500), "Can elephants swim? Yes, or no?", part=3, q=True, tag="question 3b", pause=3.2, actors=[("tumble", "tumble", 860, 995, .55)], pcam=(900, 560, 1500), props=RV(),
      fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("paper_blue", (960, 540, 1500), "Elephants can swim! They swim to cool off, and to play.", part=3, tag="board: swim",
      actors=[("t", "tumble", 900, 1010, .9)], props=[prop("wf", water, 960, 860, 1.0), prop("wv", waves, 1350, 600, 1.0, True, p=(960, 440, .8))], pcam=(960, 560, 1500),
      fx=[("to", 0, "#{p}t-trunk", UP), ("show", "w:swim!", "wv"), ("to", 0.2, "#{p}t_w", {"y": "-=16", "duration": .6, "yoyo": True, "repeat": 7}, "Tumble bobs in the water")],
      words=[("w:swim!", "SWIM!", .22, .2, 1.4, "sun", (.5, .37), 1.1), ("w:play.", "AND PLAY!", .76, .2, 1.0, "pill", (.5, .45), .8)]),
    S("river", (1000, 720, 1300), "Splash, splash! Tumble swims along. Bubble, bubble!", part=3, tag="bubbles", actors=[("tumble", "tumble", 660, 1060, .62)], pcam=(1050, 640, 1500),
      props=RV() + [prop("bu", bubbles, 640, 850, 1.0, True)], words=[("w:Splash,", "SPLASH!", .5, .18, 1.1, "sun", (.5, .31))],
      fx=[("to", 0, "#{p}tumble-trunk", UP), ("to", 0.1, "#{p}tumble_w", {"x": 960, "duration": 3.4, "ease": "none"}, "Tumble swims along"), ("show", "w:Bubble,", "bu"),
          ("to", "w:Bubble,", "#{p}bu_w", {"y": "-=40", "duration": .5, "yoyo": True, "repeat": 3}, "")]),
    S("river", say="Can you swim with your arms? Splash, splash, splash!", part=3, q=True, tag="swim along", hide=["tumble", "mama"], props=RV(), fx=[("hop", "w:Splash,", "milo", 2)],
      words=[("w:Splash,", "SPLASH!", .76, .22, 1.0, "sun", (.5, .31))], **MILO("river")),
    S("river", (1000, 640, 1500), "Out he comes, all wet and cool. Drip, drip!", part=3, tag="out he comes", actors=[("tumble", "tumble", 900, 1060, .62)], pcam=(1010, 560, 1500), props=RV() + [prop("dr", drops, 850, 620, 1.6, True)],
      fx=[("to", 0, "#{p}tumble-trunk", UP), ("to", 0.1, "#{p}tumble_w", {"y": 905, "duration": 1.5, "ease": "power1.out"}, "Tumble comes out of the water"),
          ("to", 0.1, "#{p}tumble-trunk", {"rotation": 0, "scaleY": 1, "duration": 1.5}, ""), ("show", "w:Drip,", "dr"), ("to", "w:Drip,", "#{p}dr_w", {"y": "+=60", "duration": .35, "yoyo": True, "repeat": 3}, "")],
      words=[("w:Drip,", "DRIP!", .2, .2, 1.2, "", (.5, .31))]),
    S("river", RTC, "Flap, flap, flap! Tumble feels nice and cool.", part=3, tag="flap after the swim", hide=["milo", "mama"], pcam=RTV, props=RV(),
      fx=[FLAP("w:Flap,", n=9), ("face", 0.05, "tumble", "happy")], words=[("w:cool.", "COOL!", .82, .2, 1.2, "sun", (.5, .31))]),
    S("paper_pink", WCAM, "Three, go for a swim!", part=3, tag="board: way 3", pcam=WPCAM, props=ways((0, 1), (2,)),
      fx=[("show", "w:Three,", "w2")], words=[("w:Three,", "3", .8, .25, 1.6, "sun", (.24, .71), 1.1)]),
    S("river", say="Which way do you like best? Flap, drink, or swim?", part=3, q=True, tag="which way", pause=1.6, hide=["tumble", "mama"], props=RV(), fx=[("hop", "w:best?", "milo")],
      words=[("w:best?", "YOU?", .76, .22, 1.2, "sun", (.5, .31))], **MILO("river")),
    S("zoo_eve", WIDE, "The sun goes down. Tumble walks home with Mama.", part=3, trans="iris", tag="evening wide", cam2=(1000, 560, 1780), pcam=ZTP, pcam2=WV("zoo_eve", ["tumble", "mama"], floor=.7), hide=["milo"],
      move={"tumble": (380, 940, .6)}, fx=[("walk", 0, "tumble", 320, 3.0)], words=[("w:home", "HOME", .5, .16, 1.2, "sun")]),
    S("zoo_eve", (1150, 620, 1100), "Tumble flaps his ears one more time. Cool and happy!", part=3, tag="cool and happy", actors=HUG, pcam=HUGP, pcam2=HUGP,
      fx=[FLAP("w:flaps", n=5), ("face", "w:Cool", "tumble", "happy"), FLAP("w:happy!", "mama", n=3, d=.3)], words=[("w:happy!", "HAPPY!", .2, .2, 1.0, "sun", (.3, .31))]),
    S("zoo_eve", say="Big ears, big job. Wow!", part=3, tag="wow", hide=["tumble", "mama"], fx=[("hop", "w:Wow!", "milo", 2)], words=[("w:Wow!", "WOW!", .76, .22, 1.3, "sun", (.5, .31))], **MILO("zoo_eve")),
    # ---------------------------------------------------------------- QUIZ + RECAP
    S("zoo_eve", WIDE, "Time to remember what we learned!", part=4, tag="quiz time", cam2=(1000, 560, 1760), actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      words=[("w:remember", "QUIZ TIME!", .62, .14, 1.3, "sun", (.5, .31))]),
    S("zoo_eve", (960, 520, 1920), "Can an elephant fly with its ears? Yes, or no?", part=4, q=True, tag="quiz 1", pause=3.2, actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("paper", (960, 540, 1500), "No! Big ears are not wings.", part=4, tag="board: not wings again",
      props=[prop("wg", wing, 960, 560, 1.4, p=(960, 600, 1.3)), prop("x", crossx, 960, 560, 1.1, p=(960, 600, 1.0))], pcam=(960, 480, 1700), words=[("w:No!", "NO!", .2, .2, 1.5, "sun", (.5, .37), 1.2)]),
    S("zoo_eve", (960, 520, 1920), "What do big ears help an elephant do? Keep cool, or keep warm?", part=4, q=True, tag="quiz 2", pause=3.2, actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      fx=[("signs", "w:cool,", ["COOL", "WARM"], 0, "wait:2.0")]),
    S("paper_blue", (960, 540, 1600), "Keep cool! Flap, flap, cool.", part=4, tag="board: cool again", **EB,
      fx=[FLAP("w:Flap,", "ebe", n=7, d=.2)], words=[("w:cool!", "COOL!", .78, .2, 1.4, "sun", (.5, .37), 1.1)]),
    S("paper_blue", SHAPE, "And what shape is an African elephant's ear?", part=4, q=True, tag="quiz 3", pause=1.6, props=[prop("es", ear_shape, 960, 540, .85, p=(960, 600, .9))], pcam=SHAPEP,
      words=[("end+0.3", "?", .8, .2, 2.2, "sun", (.5, .37), 1.5)]),
    S("paper_blue", SHAPE, "Like Africa!", part=4, tag="board: Africa again",
      props=[prop("es", ear_shape, 600, 560, .75, p=(960, 380, .6)), prop("af", africa, 1360, 560, .72, p=(960, 830, .6))], pcam=SHAPEP, words=[("w:Africa!", "AFRICA!", .5, .14, 1.2, "sun", (.5, .62), 1.0)]),
    S("paper_pink", WCAM, "Three ways to keep cool. Let's say them!", part=4, tag="board: three ways", pcam=WPCAM, props=ways((0, 1, 2)), words=[("w:Three", "3 WAYS", .5, .16, 1.4, "sun", (.5, .28), .9)]),
    S("paper_pink", WCAM, "Flap, drink, swim!", part=4, tag="board: say them", pcam=WPCAM, props=ways((), (0, 1, 2)), fx=[("show", "w:Flap,", "w0"), ("show", "w:drink,", "w1"), ("show", "w:swim!", "w2")]),
    S("zoo_eve", (1150, 620, 1200), "Good night, Tumble. Good night, Mama.", part=4, tag="good night", actors=HUG, pcam=HUGP, pcam2=HUGP, props=[prop("h1", art2.heart, 1010, 440, 1.0, True)],
      fx=[("face", 0.02, "tumble", "sleepy"), ("show", "w:Mama.", "h1")]),
    S("zoo_eve", WIDE, "Thank you for learning with me, friends. See you at the zoo!", part=4, tag="goodbye", cam2=(960, 520, 2050), actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      words=[("w:See", "SEE YOU AT THE ZOO!", .6, .17, .95, "pill", (.5, .31), .62)], fx=[("hop", "w:zoo!", "milo", 2)]),
]


def T(src, **kw):
    d = dict(next(x for x in SHOTS if x["tag"] == src)); d.update(kw); return d


SHORTS = [
    {"id": "zc_ep03_short1", "title": "How Big Are an Elephant's Ears?", "band": ("HOW BIG ARE", "THE EARS?"), "thumb_text": "AFRICA?!", "part": 1,
     "extra_first": [T("hook: big ears", part=1)]},
    {"id": "zc_ep03_short2", "title": "Why Do Elephants Flap Their Ears?", "band": ("WHY DO THEY", "FLAP?"), "thumb_text": "SO COOL!", "part": 2,
     "extra_first": [S("savanna", MC, "Why do elephants flap their ears?", part=2, q=True, tag="hook: why flap", hide=["milo", "tumble"], pcam=MV,
                       fx=[FLAP("w:flap", "mama", n=5, d=.22)], words=[("w:ears?", "?", .2, .2, 2.6, "sun", (.5, .33), 1.6)])]},
    {"id": "zc_ep03_short3", "title": "Can a Baby Elephant Swim?", "band": ("CAN TUMBLE", "SWIM?"), "thumb_text": "SPLASH!", "part": 3,
     "extra_first": [S("river", (1000, 720, 1300), "Can a baby elephant swim?", part=3, q=True, tag="hook: can he swim", actors=[("tumble", "tumble", 800, 1060, .62)], pcam=(1050, 640, 1500), props=RV(),
                       fx=[("to", 0, "#{p}tumble-trunk", UP), ("to", 0.2, "#{p}tumble_w", {"y": "-=14", "duration": .6, "yoyo": True, "repeat": 3}, "Tumble bobs in the water")],
                       words=[(0.0, "?", .26, .26, 2.6, "sun", (.5, .34), 1.6)])]},
]

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
THUMBS = {
    "zc_ep03": {"place": "savanna", "cam": (960, 540, 1920),
                "actors": [("elephant", 420, 1340, 1.75, False, 'gsap.set("#P-ear",{rotation:10,svgOrigin:"250 -590"});'), ("milo", 1640, 900, .85, False, "")],
                "props": [(breeze, 470, 130, 1.0)],
                "words": [("LIKE A FAN?!", 1380, 170, 170, "sun")]},
    "zc_ep03_short1": {"place": "paper_blue", "cam": (960, 560, 1900),
                       "actors": [],
                       "props": [(ear_shape, 960, 420, 1.0), (africa, 960, 1100, 1.0)],
                       "words": [("AFRICA?!", 540, 330, 190, "sun")]},
    "zc_ep03_short2": {"place": "savanna", "cam": MV,
                       "actors": [("elephant", 1560, 930, .9, True, 'gsap.set("#P-ear",{rotation:14,svgOrigin:"250 -590"});')],
                       "props": [(breeze, 1160, 360, 1.0)],
                       "words": [("SO COOL!", 540, 420, 200, "sun")]},
    "zc_ep03_short3": {"place": "river", "cam": (1050, 640, 1500),
                       "actors": [("tumble", 900, 1060, .62, False, 'gsap.set("#P-trunk",{rotation:-160,scaleY:1.35,svgOrigin:"392 -430"});')],
                       "props": [(water, 960, 850, 1.0), (bubbles, 700, 850, 1.0)],
                       "words": [("SPLASH!", 540, 520, 190, "sun")]},
}
