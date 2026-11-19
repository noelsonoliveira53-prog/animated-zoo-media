"""za_ep06 - Milo's Zoo Adventures: "The Rainy Day Umbrella" (cartoon adventure, the 3D music-and-sync process: "beat").
Rain starts on the way to Mango's tree house, and Milo's feathers get soggy. The friends look for an umbrella: a small leaf, a flower hat and
a moss hat are each too small (or too drippy). Resting under the big tree, they see little white bats dry inside a leaf they folded into a
tent. Mango works it out herself: a leaf, but a giant one. A giant leaf has fallen on the ground; it is too heavy for one, so they lift it
together, and Milo, Mango, Tumble and Puff the little bat all fit under it. They walk to the tree house, the rain stops, a rainbow, fruit.
Nobody is hurt, lost, crying or trapped: the rain is a soft warm jungle rain, Tumble likes it, Milo is only soggy and shakes himself dry.

FACTS, read at the source on Nov 19 2026, about 12:00 AM ET (each page fetched by the session's page reader, which quoted these sentences):
 [NGK] National Geographic Kids, "Rainforest Habitat", kids.nationalgeographic.com/nature/habitats/article/rain-forest
   "In some rainforests it rains more than an inch every day!"
   "Most animals in the rainforest live in the canopy."
   "In the next layer, the canopy, the leaves and branches of the trees all touch one another or are connected by vines."
 [SI] Smithsonian, "Researchers Observe Novel Bat Behavior in Panama", si.edu/es/node/538210
   "Tent-making bats snip and fold huge leaves of tropical plants to create tents."
 [CO] COTERC (Canadian Organization for Tropical Education and Rainforest Conservation), "Tent-making Bats", coterc.org/tent-making-bats
   tents are used for "protection from rain and predators"; the bats "chew the leaves of plants in a way that creates 'tents'".
 [NG] National Geographic, "These bats make intricate tents out of leaves", nationalgeographic.com/animals/article/tent-building-bats-central-south-america
   "Some tent-making bats sport stripes or mottled markings, while others are pale all over"; one is described as looking "like a pig or a cotton ball".
 Said as animal facts in the film (three fact shots and one closing question), each from a quote above: in some rainforests it rains more than
 an inch every day [NGK]; some little bats snip and fold a big leaf to make a tent, and it keeps the rain off [SI, CO]; most animals in the
 rainforest live in the canopy, high up in the treetops [NGK].
 Read but NOT said: predators (CO) - not for ages 2-6; how many bats share a tent (no page gives a number); what the bats eat (not read).
 Not animal facts, said as what happens in THIS story: Tumble likes the rain, the flower and moss hats, the fallen giant leaf, Puff joining
 the walk, the tree house. Puff is a story bat, white and fluffy ("pale all over", NG); nothing else is claimed about her kind.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep03 as A3          # rain, tint, clouds, drops (read only)
import art_za_ep04 as A4          # the stream place, fruit (read only)
import art_za_ep06 as A
import kit
from kit import Kit, S, prop

EP = {"id": "za_ep06", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "tumble": {"voice": "am_puck", "speed": .85, "pitch": 5, "formant": 1.16, "gain": .66},
               "mango": {"voice": "af_bella", "speed": .95, "pitch": 2, "formant": 1.08, "gain": .95}, "mama": {"voice": "bf_emma", "speed": .8, "gain": .8}},
      "title": "The Rainy Day Umbrella", "thumb_text": "ROOM FOR ALL!",
      "series": "Milo's Zoo Adventures",
      "description": ("Drip, drop! Rain starts on the way to Mango's tree house, and Milo's feathers get soggy. A little leaf, a pink flower and a hat of moss: "
                      "each one is too small. Then the friends see little bats, dry inside a leaf tent. What can Mango, Tumble and Milo find that is big enough for everyone? "
                      "A gentle animal adventure for ages 2-6 about working together and making room for a new friend, with questions to answer, friends to count and a tune to clap along to.\n"
                      "Kids see how much it can rain in a rainforest, how some little bats snip and fold a big leaf into a tent that keeps the rain off, "
                      "and where most rainforest animals live.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNational Geographic Kids (rainforest habitat); Smithsonian Institution and COTERC (tent-making bats)."),
      "tags": ["rain story for kids", "rainy day cartoon", "spider monkey", "baby elephant", "tent-making bat", "animal stories for kids", "rainforest for kids",
               "friendship story for kids", "kids adventure cartoon", "counting friends", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "jungle": [("tumble", "tumble", 380, 930, .6), ("mango", "monkey", 1220, 934, .56), ("milo", "milo", 860, 500, .72, False, True)],
    "meadow": [("tumble", "tumble", 240, 880, .6), ("mango", "monkey", 900, 884, .56), ("milo", "milo", 640, 430, .7, False, True)],
    "mossy": [("tumble", "tumble", 230, 930, .6), ("mango", "monkey", 760, 934, .55), ("milo", "milo", 1040, 520, .7, False, True)],
    "bigtree": [("tumble", "tumble", 260, 930, .6), ("mango", "monkey", 820, 934, .55), ("milo", "milo", 560, 520, .7, False, True)],
    "treehouse": [("tumble", "tumble", 300, 930, .6), ("mango", "monkey", 820, 934, .55), ("milo", "milo", 900, 420, .7, False, True), ("puff", "bat", 700, 600, .34)],
    "canopy": [("mango", "monkey_hang", 900, 446, .6), ("milo", "milo", 1460, 290, .7, False, True)],
    "zoo_eve": [("mango", "monkey", 300, 940, .55), ("tumble", "tumble", 660, 940, .6), ("mama", "elephant", 1540, 932, .9, True), ("milo", "milo", 330, 420, .68, False, True)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
def only(place, *keep, stage=None): return [a[0] for a in (stage or STAGES[place]) if a[0] not in keep]

# ------------------------------------------------------------------ the rain: a gray-blue light and streaks over everything, a dry hole under the giant leaf
RAINFX = ("to", 0, "#{p}rn-mv", {"x": "-=60", "y": "+=220", "duration": .3, "repeat": 40, "ease": "none"}, "")
def RAIN(holes=()): return [prop("rn", lambda p: A.rain_dry(p, holes), -500, -700, 1.0)]
TINT = lambda: prop("tn", A3.tint, 0, 0, 1.0)
def RS(place, cam, say="", rain=True, holes=(), props=(), fx=(), **kw):
    """A rainy shot: the rain under every other prop, the gray light over all of them."""
    if not rain: return S(place, cam, say, props=list(props), fx=list(fx), **kw)
    return S(place, cam, say, props=RAIN(holes) + list(props) + [TINT()], fx=[RAINFX] + list(fx), **kw)
CLOUDS = lambda: [prop("c1", A3.cloud, 1560, 170, 1.1), prop("c2", A3.cloud, 260, 100, 1.0)]

# ------------------------------------------------------------------ the giant leaf: carried over the four friends
TU_L = (360, 930, .6)                                # Tumble under the leaf
def TIP(tx, ty=930, s=.6): return (round(tx + 653 * s), round(ty - 636 * s))      # the tip of his trunk turned straight up (-100): the stem's foot
LEAF_W = 1150
def GL(tx, ty=930, hidden=False): x, y = TIP(tx, ty); return prop("gl", lambda p: A.giant_leaf(p, LEAF_W), x, y + 10, 1.0, hidden)
def HOLE(tx, ty=930):
    x, y = TIP(tx, ty); rim = y + 10 - 250; return [(x - LEAF_W / 2 + 40, rim + 10), (x + LEAF_W / 2 - 40, rim + 10), (x + LEAF_W / 2 - 40, 1200), (x - LEAF_W / 2 + 40, 1200)]
TRUNK_UP = lambda at=0.02, d=.01: ("trunk", at, "tumble", -100, d)
UNDER = lambda tx=360: [("tumble", "tumble", tx, 930, .6), ("mango", "monkey", tx + 720, 934, .55), ("milo", "milo", tx + 590, 620, .62, False, True),
                        ("puff", "bat_hang", tx + 830, TIP(tx)[1] + 10 - 250, .32)]

# ------------------------------------------------------------------ hats on heads (the wearer stands still: no hop, no flying bob)
def HAT(name, fn, place, who, s, dy=0, hidden=True, stage=None):
    x, y = P(place, who, "top", 0, dy, stage=stage); return prop(name, fn, x, y, s, hidden)
MILO_GND = {"milo": (620, 930, .72)}        # Milo standing on the ground in the jungle hat shots
GND_J = [("tumble", "tumble", 380, 930, .6), ("mango", "monkey", 1220, 934, .56), ("milo", "milo", 620, 930, .72)]

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. Nobody sings: the rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}       # the show loop's key and the music bed's tempo
SING_DRIP = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~ ~", "notes": "E4:1 G4:1 E4:1 G4:1 G4:1 D4:1 G4:1", "rest": 1},      # drip, drop, drip, drop (C bar), hear the rain (G bar)
                                 {"text": "~ ~ ~ ~ ~ ~ ~", "notes": "A4:1 F4:1 A4:1 C5:1 G4:1 E4:1 C4:1", "rest": 1}])     # under our leaf (F bar), dry again (C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "D4:1 G4:1 B4:1 A4:.5,B4:.5 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune

CNT_DROPS, CNT_LIFT, CNT_FOUR = .64, .64, 1.2     # seconds from "One" to the last number, read from the timing file
MCL = lambda place, dx=0, dy=-70, w=820: C(place, "milo", "body", w, dx, dy)          # Milo asks a question: low in the frame, under the signs
SHAKE = lambda at, who="milo": ("to", at, "#{p}" + who, {"rotation": 8, "svgOrigin": "0 -150", "duration": .09, "yoyo": True, "repeat": 7, "ease": "sine.inOut"}, f"{who} shakes himself")
FLAP = lambda at, n=9: ("to", at, "#{p}puff-wl,#{p}puff-wr", {"scaleY": .55, "transformOrigin": "50% 50%", "duration": .12, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "Puff flaps her wings")
def DRIPS(name, x, y, at, n=3, dy=120, gap=.35, s=.22):
    """n drops that fall one after another from (x, y)."""
    ps = [prop(f"{name}{k}", lambda p, s=s: A.drip(p, s), x + (k - 1) * 22, y, 1.0, True) for k in range(n)]
    fx = []
    for k in range(n):
        t = at if isinstance(at, (int, float)) else at
        fx.append(("fromto", at, f"#{{p}}{name}{k}_w", {"opacity": 1, "y": y}, {"opacity": 0, "y": y + dy, "duration": .6, "delay": k * gap, "ease": "power1.in", "repeat": 2, "repeatDelay": .5, "immediateRender": False}, "a drop falls" if k == 0 else ""))
    return ps, fx

d1p, d1f = DRIPS("dm", *P("jungle", "milo", "body", 150, 0), 0.1, 3, 110)                 # drops falling off soggy Milo in the hook
d2p, d2f = DRIPS("dk", *P("meadow", "mango", "head", 120, -20), "w:Drip!", 3, 110)          # drops through the flower hat onto Mango's nose
TENT_X, TENT_Y = 1060, 300                                                              # the leaf tent hangs under a low branch of the big tree
TENT = lambda hidden=False: prop("lt", A.leaf_tent, TENT_X, TENT_Y, .9, hidden)
BRANCH = lambda: prop("br", lambda p: f'<g id="{p}"><path d="M0 0 C120 -10 220 -6 300 -20" stroke="#8a6238" stroke-width="44" stroke-linecap="round"/><path d="M10 10 C120 4 220 8 300 -6" stroke="#735029" stroke-width="16" stroke-linecap="round" opacity=".7"/></g>', TENT_X - 20, TENT_Y - 26, 1.0)
FLAT = lambda hidden=False: prop("lf", lambda p: A.giant_leaf_flat(p, 1000), 760, 960, 1.0, hidden)

SHOTS = [
    # ------------------------------------------------------------ HOOK: the rain and soggy Milo in the first 5 seconds
    RS("jungle", C("jungle", "milo", "body", 760, 0, -10), "Drip, drop! Oh, it's raining! And my feathers are all soggy!", beat="hook", tag="hook: rain, soggy Milo", hide=["tumble", "mango"],
       props=d1p, fx=d1f + [("face", "w:Oh,", "milo", "wow"), SHAKE("w:soggy!")], words=[("w:Drip,", "DRIP, DROP!", .27, .2, .85, "sun")]),
    RS("jungle", WIDE, "Hello, I'm Milo! We are on the way to Mango's tree house. This is Mango, the spider monkey.", tag="jungle wide: Milo, Mango", cam2=(980, 560, 1800),
       fx=[("hop", "w:Hello,", "milo"), ("to", "w:Mango,", "#{p}mango-tail", {"rotation": 12, "svgOrigin": "40 -80", "duration": .25, "yoyo": True, "repeat": 5}, "Mango swishes her tail")],
       words=[("w:Mango,", "MANGO", .64, .4, .85, "pill")]),
    RS("jungle", C("jungle", "tumble", "all", 1000, 60, -40), "And this is Tumble, the baby elephant.", tag="Tumble", hide=["mango", "milo"],
       fx=[("hop", "w:Tumble,", "tumble")], words=[("w:Tumble,", "TUMBLE", .72, .22, .85, "pill")]),
    RS("jungle", C("jungle", "tumble", "head", 860, -40, 20), "I like the rain! Splish, splash!", who="tumble", tag="Tumble: I like the rain", hide=["mango", "milo"],
       fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:Splish,", "tumble", -90, .3), ("trunk", "w:splash!", "tumble", -20, .3)], words=[("w:Splish,", "SPLISH SPLASH!", .7, .2, .7, "sun")]),
    RS("jungle", C("jungle", "milo", "body", 760, 0, -10), "Not me! Soggy feathers are no fun.", tag="Milo: soggy feathers", hide=["tumble", "mango"],
       props=[prop("sk", A.shake, *P("jungle", "milo", "body"), 1.0, True)], fx=[SHAKE("w:Soggy"), ("show", "w:Soggy", "sk", 1.0), ("face", "w:fun.", "milo", "sad")],
       words=[("w:Soggy", "SOGGY!", .26, .22, .9, "pill")]),
    # ------------------------------------------------------------ GOAL
    RS("jungle", C("jungle", "mango", "head", 800, -40, 30), "Come on, friends! My tree house is this way.", who="mango", beat="goal", tag="Mango: this way", hide=["tumble", "milo"],
       fx=[("face", 0.02, "mango", "happy"), ("arm", "w:way.", "mango", "r", -100)], words=[("w:tree", "TREE HOUSE", .26, .2, .8, "pill")]),
    RS("jungle", C("jungle", "mango", "all", 860, -60, -60), "Let's find an umbrella! Then we can all stay dry on the way to my tree house.", who="mango", beat="goal", tag="goal: an umbrella",
       hide=["tumble", "milo"], fx=[("hop", "w:umbrella!", "mango"), ("arm", "w:tree", "mango", "r", -150)], words=[("w:umbrella!", "AN UMBRELLA!", .28, .2, .8, "sun")]),
    RS("jungle", MCL("jungle", 30), "What keeps you dry in the rain? An umbrella, or a spoon?", q=True, beat="goal", tag="question: umbrella or spoon", pause=3.2, hide=["tumble", "mango"],
       fx=[("signs", "w:umbrella,", ["UMBRELLA", "SPOON"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ the rainforest: lots of rain (fact 1)
    RS("jungle", (900, 560, 1700), "The jungle is a rainforest. And a rainforest gets lots and lots of rain.", tag="a rainforest", cam2=(920, 540, 1560),
       fx=[("face", "w:rain.", "milo", "happy"), ("hop", "w:lots", "tumble")], words=[("w:rainforest.", "RAINFOREST", .5, .17, .8, "pill")]),
    S("paper_blue", (960, 540, 1700), "In some rainforests, it rains more than an inch every day!", beat="fact", tag="fact: more than an inch a day",
      props=[prop("cup", A.rain_cup, 960, 860, 1.4), prop("cl", A3.cloud, 960, 230, .9), prop("rd", lambda p: A3.drops3(p, 70, .3), 960, 400, 1.0, True)],
      fx=[("fromto", 0.05, "#{p}cup-lv", {"scaleY": 0, "svgOrigin": "0 10"}, {"scaleY": 0, "duration": .01}, ""), ("show", "w:rains", "rd"),
          ("fromto", "w:rains", "#{p}rd_w", {"y": 380}, {"y": 640, "duration": .6, "repeat": 3, "ease": "power1.in"}, "rain falls into the cup"),
          ("to", "w:inch", "#{p}cup-lv", {"scaleY": 1.15, "svgOrigin": "0 10", "duration": 1.4, "ease": "power1.inOut"}, "the cup fills past the line")],
      words=[("w:inch", "MORE THAN 1 INCH", .76, .52, .55, "pill"), ("w:every", "EVERY DAY!", .22, .45, .85, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: a small leaf is only big enough for Milo
    RS("jungle", C("jungle", "mango", "all", 860, -60, -60), "Here's a leaf! You try it first, Milo.", who="mango", beat="obstacle1", tag="Mango: a leaf", hide=["tumble", "milo"],
       props=[prop("sl", A.small_leaf, *P("jungle", "mango", "head", 120, 60), .45, True)], fx=[("show", "w:leaf!", "sl"), ("arm", "w:leaf!", "mango", "r", -60)],
       words=[("w:leaf!", "A LEAF!", .26, .2, .9, "sun")]),
    RS("jungle", C("jungle", "milo", "body", 760, 0, -10, stage=GND_J), "Ooh, nice and dry! Now you, Tumble.", tag="Milo under the leaf", actors=GND_J, fly=[], hide=["tumble", "mango"],
       props=[prop("sl", A.small_leaf, P("jungle", "milo", "top", -105, 40, stage=GND_J)[0], P("jungle", "milo", "top", -105, 40, stage=GND_J)[1], .5)], fx=[("face", 0.02, "milo", "happy")], words=[("w:dry!", "DRY!", .74, .24, 1.0, "sun")]),
    RS("jungle", C("jungle", "tumble", "head", 860, -40, 20), "Hmm. The leaf is too small for my big head!", who="tumble", beat="obstacle1", tag="Tumble: too small", hide=["mango", "milo"],
       props=[HAT("sl", A.small_leaf, "jungle", "tumble", .42, 30, False)], fx=[("face", 0.02, "tumble", "wow"), ("face", "w:small", "tumble", "sad")],
       words=[("w:small", "TOO SMALL!", .74, .2, .85, "pill")]),
    RS("jungle", MCL("jungle", 30), "Is the leaf big, or small?", q=True, beat="obstacle1", tag="question: big or small", pause=3.2, hide=["tumble", "mango"],
       fx=[("signs", "w:big,", ["BIG", "SMALL"], 1, "wait:1.8")]),
    RS("jungle", (744, 600, 1400), "On they go, through the rainy jungle. Squish, squash, go Tumble's feet.", tag="on they go", move={"tumble": (320, 930, .6), "mango": (840, 934, .56), "milo": (500, 515, .72)},
       fx=[("walk", 0.1, "tumble", 300, 3.4), ("walk", 0.1, "mango", 320, 3.4), ("fly", 0.1, "milo", 760, 480, 3.4)], words=[("w:Squish,", "SQUISH!", .18, .25, .9, "sun"), ("w:squash,", "SQUASH!", .82, .25, .9, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 2: a flower hat lets the rain through
    RS("meadow", (960, 560, 1800), "In the meadow, big pink flowers grow.", trans="iris", beat="obstacle2", tag="the meadow", cam2=(980, 560, 1720),
       props=CLOUDS() + [prop("fp", A.flower_plant, 1420, 900, 1.0)], fx=[("hop", "w:flowers", "mango")], words=[("w:flowers", "PINK FLOWERS", .74, .18, .8, "pill")]),
    RS("meadow", C("meadow", "mango", "head", 820, 0, 40), "A flower hat! Pretty, and dry!", who="mango", beat="obstacle2", tag="Mango: a flower hat", hide=["tumble", "milo"],
       props=CLOUDS() + [HAT("fh", A.flower_hat, "meadow", "mango", .55, 34)], fx=[("show", "w:flower", "fh"), ("face", "w:Pretty,", "mango", "happy")],
       words=[("w:flower", "FLOWER HAT", .74, .24, .8, "sun")]),
    RS("meadow", C("meadow", "mango", "head", 700, 0, 40), "Drip! Drip! The rain runs right through the petals.", beat="obstacle2", tag="drips through the flower", hide=["tumble", "milo"],
       props=CLOUDS() + [HAT("fh", A.flower_hat, "meadow", "mango", .55, 34, False)] + d2p, fx=d2f + [("face", "w:Drip!", "mango", "wow"), ("face", "w:petals.", "mango", "sad")],
       words=[("w:Drip!", "DRIP!", .78, .3, 1.0, "sun")]),
    RS("meadow", C("meadow", "tumble", "head", 860, -40, 20), "And a flower is much too small for an elephant!", who="tumble", beat="obstacle2", tag="Tumble: too small for me", hide=["mango", "milo"],
       props=CLOUDS(), fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:elephant!", "tumble", -40, .4)], words=[("w:small", "MUCH TOO SMALL", .74, .2, .65, "pill")]),
    RS("meadow", MCL("meadow", 20), "Can an elephant fit under a flower? Yes, or no?", q=True, beat="obstacle2", tag="question: elephant under a flower", pause=3.2, hide=["tumble", "mango"],
       fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 3: a moss hat is soggy and drippy
    RS("mossy", (900, 600, 1800), "By the little stream, there is an old log, with soft green moss.", trans="iris", beat="obstacle3", tag="the mossy log", cam2=(900, 600, 1700),
       fx=[("hop", "w:moss.", "mango")], words=[("w:moss.", "SOFT MOSS", .4, .2, .85, "pill")]),
    RS("mossy", C("mossy", "mango", "all", 800, 40, -60), "Moss is soft, like a hat. I'll make one for Milo!", who="mango", beat="obstacle3", tag="Mango: a moss hat", hide=["tumble", "milo"],
       props=[prop("mh", A.moss_hat, *P("mossy", "mango", "head", 150, 70), .4, True)], fx=[("arm", "w:soft,", "mango", "r", -50), ("show", "w:hat.", "mh"), ("hop", "w:Milo!", "mango")],
       words=[("w:hat.", "MOSS HAT", .74, .2, .85, "sun")]),
    RS("mossy", C("mossy", "milo", "body", 700, 0, -20, stage=[("milo", "milo", 600, 930, .72)]), "Milo puts on the moss hat. Squish! Water drips out.", beat="obstacle3", tag="moss hat squish",
       actors=[("milo", "milo", 600, 930, .72)], fly=[],
       props=[HAT("mh", A.moss_hat, "mossy", "milo", .48, 30, False, stage=[("milo", "milo", 600, 930, .72)])] + DRIPS("dh", 700, 700, "w:Squish!", 3, 140)[0],
       fx=DRIPS("dh", 700, 700, "w:Squish!", 3, 140)[1] + [("face", "w:Squish!", "milo", "wow"), ("to", "w:Squish!", "#{p}mh_w", {"scaleY": .8, "duration": .15, "yoyo": True, "repeat": 1}, "the moss squishes")],
       words=[("w:Squish!", "SQUISH!", .76, .22, 1.0, "sun")]),
    RS("mossy", C("mossy", "milo", "body", 760, 0, -20, stage=[("milo", "milo", 600, 930, .72)]), "Oh! It's soggy and drippy, just like me!", tag="Milo: soggy like me", actors=[("milo", "milo", 600, 930, .72)], fly=[],
       props=[HAT("mh", A.moss_hat, "mossy", "milo", .48, 30, False, stage=[("milo", "milo", 600, 930, .72)])], fx=[("face", 0.02, "milo", "happy")], words=[("w:soggy", "SOGGY HAT", .26, .22, .8, "pill")]),
    RS("mossy", (640, 700, 900), "How many drops fall from the hat? Count with me! One. Two. Three!", q=True, beat="obstacle3", tag="question: count the drops", actors=[("milo", "milo", 600, 930, .72)], fly=[],
       props=[HAT("mh", A.moss_hat, "mossy", "milo", .48, 30, False, stage=[("milo", "milo", 600, 930, .72)])] + [prop(f"cd{k}", lambda p: A.drip(p, .3), 690 + k * 36, 690, 1.0, True) for k in range(3)],
       fx=[("count", "w:One.", 3, CNT_DROPS, {"x": 1420, "y": 400})] + [("fromto", f"w:{w}", f"#{{p}}cd{k}_w", {"opacity": 1, "y": 690}, {"y": 930, "opacity": 0, "duration": .7, "ease": "power1.in", "immediateRender": False}, "a drop falls")
                                                                     for k, w in enumerate(("One.", "Two.", "Three!"))]),
    # ------------------------------------------------------------ LOW MOMENT: everything is too small (gentle: nobody cries)
    RS("bigtree", WIDE, "The friends rest under the big tree. Still wet, and the tree house is far away.", trans="iris", beat="low", tag="under the big tree", cam2=(1000, 560, 1800),
       props=[BRANCH(), TENT()], fx=[("to", "w:rest", "#{p}tumble", {"y": 30, "duration": .6}, "Tumble sits down"), ("face", "w:wet,", "tumble", "sad"), ("face", "w:wet,", "mango", "sad")],
       words=[("w:far", "SO FAR...", .3, .2, .9, "pill")]),
    RS("bigtree", C("bigtree", "mango", "head", 760, 0, 20), "A leaf, a flower, a moss hat. Everything is too small.", who="mango", beat="low", tag="Mango: everything too small", hide=["tumble", "milo"],
       fx=[("face", 0.02, "mango", "sad"), ("arm", "w:leaf,", "mango", "r", -40), ("arm", "w:Everything", "mango", "r", 0)], words=[("w:small.", "TOO SMALL", .74, .22, .85, "pill")]),
    RS("bigtree", C("bigtree", "milo", "body", 760, 0, -10), "Maybe we can't stay dry today.", beat="low", tag="Milo: maybe not", hide=["tumble", "mango"],
       fx=[("face", 0.02, "milo", "sad")]),
    RS("bigtree", C("bigtree", "tumble", "head", 860, -40, 50), "We are wet, but we are together. That's okay.", who="tumble", beat="low", tag="Tumble: together is okay", hide=["mango", "milo"],
       fx=[("to", 0.02, "#{p}tumble", {"y": 30, "duration": .01}, ""), ("face", 0.02, "tumble", "sad"), ("face", "w:together.", "tumble", "happy")]),
    RS("bigtree", MCL("bigtree", 20), "What do we need now? Something small, or something big?", q=True, beat="low", tag="question: small or big", pause=3.2, hide=["tumble", "mango"],
       fx=[("signs", "w:small,", ["SMALL", "BIG"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: the leaf tent gives Mango the idea, and they lift a giant leaf together
    RS("bigtree", (960, 580, 1400), "Look! Little white bats, under that leaf!", who="mango", beat="solution", tag="Mango: little bats", hide=["tumble", "milo"],
       props=[BRANCH(), TENT()], fx=[("face", 0.02, "mango", "wow"), ("arm", "w:Look!", "mango", "r", -140)], words=[("w:bats,", "LITTLE BATS!", .72, .7, .8, "sun")]),
    RS("bigtree", (TENT_X, TENT_Y + 140, 900), "The bats fold the leaf down, like a tent. Inside, they stay nice and dry.", beat="solution", tag="the leaf tent close", hide=only("bigtree"),
       props=[BRANCH(), TENT()], fx=[("to", "w:fold", "#{p}lt_w", {"rotation": 3, "duration": .5, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "the tent sways")],
       words=[("w:tent.", "A TENT!", .2, .2, .9, "sun"), ("w:dry.", "DRY!", .8, .75, .9, "pill")]),
    S("paper_pink", (960, 540, 1700), "Some little bats snip and fold a big leaf to make a tent. It keeps the rain off!", beat="fact", tag="fact: bats make leaf tents",
      props=[prop("fl", lambda p: A.giant_leaf_flat(p, 640), 560, 560, 1.0), prop("sn", A.scissors_snips, 560, 500, 1.4, True), prop("ar", lambda p: art.arrow(p, 920, 560, 1120, 560), 0, 0, 1, True),
             prop("lt", A.leaf_tent, 1420, 360, 1.0, True), prop("cl", A3.cloud, 1420, 170, .6, True), prop("rd", lambda p: A3.drops3(p, 120, .26), 1420, 300, 1.0, True)],
      fx=[("show", "w:snip", "sn"), ("show", "w:tent.", "ar"), ("show", "w:tent.", "lt"), ("show", "w:rain", "cl"), ("show", "w:rain", "rd"),
          ("fromto", "w:rain", "#{p}rd_w", {"x": 1200}, {"x": 1200, "duration": .01}, "")],
      words=[("w:snip", "SNIP, FOLD!", .29, .2, .8, "sun"), ("w:off!", "NO RAIN INSIDE", .74, .8, .62, "pill")]),
    RS("bigtree", C("bigtree", "mango", "all", 860, 60, -70), "A leaf tent! That's it! We need a leaf. A giant one!", who="mango", beat="solution", tag="Mango: a giant leaf", hide=["tumble", "milo"],
       fx=[("face", 0.02, "mango", "happy"), ("hop", "w:it!", "mango"), ("arm", "w:giant", "mango", "r", -160), ("arm", "w:giant", "mango", "l", 160)], words=[("w:giant", "A GIANT LEAF!", .26, .2, .8, "sun")]),
    RS("bigtree", (TENT_X + 60, TENT_Y + 150, 1000), "A little bat named Puff peeks out, and smiles.", beat="solution", tag="Puff peeks out", hide=only("bigtree"),
       actors=[("puff", "bat_hang", TENT_X + 270, TENT_Y - 36, .42)], props=[BRANCH(), TENT()],
       fx=[("fromto", 0.02, "#{p}puff_w", {"x": TENT_X + 60, "opacity": 0}, {"x": TENT_X + 60, "opacity": 0, "duration": .01}, ""),
           ("to", "w:peeks", "#{p}puff_w", {"x": TENT_X + 270, "opacity": 1, "duration": .7, "ease": "power1.out"}, "Puff peeks out"), ("face", "w:smiles.", "puff", "happy")],
       words=[("w:Puff", "PUFF", .2, .3, 1.0, "pill")]),
    RS("bigtree", (900, 720, 1500), "And there, on the ground! A giant leaf has fallen down.", beat="solution", tag="the fallen giant leaf", hide=["milo", "tumble"], move={"mango": (1360, 934, .55)},
       props=[FLAT(True)], fx=[("show", "w:giant", "lf"), ("hop", "w:ground!", "mango")], words=[("w:giant", "SO BIG!", .5, .2, 1.0, "sun")]),
    RS("bigtree", (980, 760, 1300), "Mango pulls and pulls. But it is too heavy for one little monkey.", beat="solution", tag="too heavy for one", hide=["milo", "tumble"], move={"mango": (1360, 934, .55)},
       props=[FLAT()], fx=[("arm", "w:pulls", "mango", "l", 70), ("to", "w:pulls", "#{p}mango_w", {"x": 1330, "duration": .3, "yoyo": True, "repeat": 5}, "Mango pulls"),
                           ("to", "w:pulls", "#{p}lf_w", {"rotation": -1.5, "duration": .3, "yoyo": True, "repeat": 5}, ""), ("face", "w:heavy", "mango", "sad")],
       words=[("w:heavy", "TOO HEAVY!", .74, .2, .85, "pill")]),
    RS("bigtree", C("bigtree", "tumble", "head", 860, -40, 20), "Let's lift it together! I can hold the stem with my trunk.", who="tumble", beat="solution", tag="Tumble: together", hide=["mango", "milo"],
       fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:trunk.", "tumble", -60, .4)], words=[("w:together!", "TOGETHER!", .74, .2, .85, "sun")]),
    RS("bigtree", MCL("bigtree", 20), "What can good friends do? Work alone, or work together?", q=True, beat="solution", tag="question: alone or together", pause=3.2, hide=["tumble", "mango"],
       fx=[("signs", "w:alone,", ["ALONE", "TOGETHER"], 1, "wait:1.8")]),
    RS("bigtree", (900, 500, 1700), "Count with me! One. Two. Three. Lift! Up goes the giant leaf.", q=True, beat="solution", tag="question: count, lift", actors=UNDER(360)[:3],
       props=[FLAT(), GL(360, hidden=True)],
       fx=[("count", "w:One.", 3, CNT_LIFT, {"x": 1560, "y": 300}), ("hide", "w:Lift!", "lf"), ("show", "w:Lift!", "gl"), ("trunk", "w:Lift!", "tumble", -100, .4),
           ("arm", "w:Lift!", "mango", "r", -160), ("hop", "w:Up", "milo")], words=[("w:Lift!", "LIFT!", .84, .55, 1.0, "sun")]),
    RS("bigtree", (900, 500, 1700), "It's a big green umbrella! Mango, Tumble and Milo all fit underneath.", beat="solution", tag="under the umbrella", actors=UNDER(360)[:3], holes=[HOLE(360)],
       props=[GL(360)], fx=[TRUNK_UP(), ("arm", 0.02, "mango", "r", -160), ("face", "w:umbrella!", "mango", "happy"), ("face", "w:umbrella!", "tumble", "happy"), ("face", "w:Milo", "milo", "happy")],
       words=[("w:umbrella!", "UMBRELLA!", .84, .5, .8, "sun")]),
    RS("bigtree", (920, 480, 1600), "Puff flies over. Is there room for one more?", beat="solution", tag="Puff: room for one more?", actors=UNDER(360)[:3] + [("puff", "bat", 1500, 600, .34)], holes=[HOLE(360)],
       props=[GL(360)], fx=[TRUNK_UP(), ("arm", 0.02, "mango", "r", -160), FLAP("w:Puff", 15), ("to", "w:flies", "#{p}puff_w", {"x": 1190, "y": 440, "duration": 1.4, "ease": "power1.inOut"}, "Puff flies under the leaf")],
       words=[("w:more?", "ONE MORE?", .8, .2, .85, "pill")]),
    RS("bigtree", C("bigtree", "mango", "head", 760, 0, 20, stage=UNDER(360)), "Of course, Puff! There is room for all!", who="mango", beat="solution", tag="Mango: room for all", actors=UNDER(360)[1:2], holes=[HOLE(360)],
       props=[GL(360)], fx=[("arm", 0.02, "mango", "r", -160), ("face", 0.02, "mango", "happy"), ("arm", "w:room", "mango", "l", 120)], words=[("w:all!", "ROOM FOR ALL!", .28, .22, .75, "sun")]),
    RS("bigtree", (920, 500, 1600), "How many friends are under the leaf? Count with me! One. Two. Three. Four!", q=True, beat="solution", tag="question: count four friends", actors=UNDER(360), holes=[HOLE(360)],
       props=[GL(360)], fx=[TRUNK_UP(), ("arm", 0.02, "mango", "r", -160), ("count", "w:One.", 4, CNT_FOUR, {"x": 1560, "y": 300}),
                           ("hop", "w:One.", "milo"), ("nod", "w:Two.", "tumble"), ("to", "w:Three.", "#{p}mango-tail", {"rotation": 12, "svgOrigin": "40 -80", "duration": .25, "yoyo": True, "repeat": 3}, "Mango swishes her tail"), FLAP("w:Four!", 5)]),
    # ------------------------------------------------------------ SONG MOMENT: the rhyme SAID, then the tune on instruments while they walk under the leaf
    RS("bigtree", (900, 500, 1600), "Drip, drop, drip, drop, hear the rain. Under our leaf, we're dry again!", who="mango", beat="solution", tag="the rain rhyme", actors=UNDER(360), holes=[HOLE(360)],
       props=[GL(360)], fx=[TRUNK_UP(), ("arm", 0.02, "mango", "r", -160), ("face", 0.02, "mango", "happy"), ("arm", "w:dry", "mango", "l", 120)],
       words=[("w:Drip,", "DRIP, DROP!", .78, .4, .75, "sun"), ("w:dry", "DRY AGAIN!", .8, .56, .7, "pill")]),
    RS("jungle", (760, 500, 1600), who="", sing=SING_DRIP, beat="song", tag="song: under our leaf", actors=UNDER(240), holes=[HOLE(240)], trans="iris", cam2=(1240, 500, 1600),
       props=[GL(240)], fx=[TRUNK_UP(), ("arm", 0.02, "mango", "r", -160), ("walk", TB(0), "tumble", 480, 9.6), ("walk", TB(0), "mango", 480, 9.6), ("to", TB(0), "#{p}milo_w", {"x": "+=480", "duration": 9.6, "ease": "none"}, ""),
                            ("to", TB(0), "#{p}puff_w,#{p}gl_w,#{p}rn-hole", {"x": "+=480", "duration": 9.6, "ease": "none"}, "they walk under the leaf"),
                            ("word", TB(0), "DRIP, DROP!", {"x": 760, "y": 196, "size": 87, "cls": "sun", "hold": 4.6})],
       words=[(TB(8), "DRY AGAIN!", .8, .14, .8, "pill")]),
    # ------------------------------------------------------------ WARM ENDING: the tree house, the rain stops, a rainbow, fruit, thank-yous, home to Mama
    S("treehouse", (960, 560, 1800), "Here is Mango's tree house! And look, the rain has stopped.", trans="iris", beat="ending", tag="the tree house, the rain stops", cam2=(980, 560, 1720),
      props=[prop("sun", A.sun_peek, 1760, 120, .6, True), prop("rb", A.rainbow, 300, 460, .5, True)],
      fx=[("show", "w:look,", "sun"), ("show", "w:stopped.", "rb"), ("to", "w:look,", "#{p}sun-r", {"rotation": 60, "svgOrigin": "0 0", "duration": 3, "ease": "none"}, ""), ("hop", "w:tree", "mango"), FLAP("w:stopped.", 5)],
      words=[("w:stopped.", "NO MORE RAIN!", .76, .17, .75, "sun")]),
    S("treehouse", C("treehouse", "milo", "body", 760, 0, -10), "A rainbow! And my feathers are drying in the sun.", tag="Milo: a rainbow", hide=["tumble", "mango", "puff"],
      props=[prop("rb", A.rainbow, P("treehouse", "milo", "body", -320)[0], P("treehouse", "milo", "body", 0, 130)[1], .22)], fx=[("face", 0.02, "milo", "happy"), SHAKE("w:feathers"), ("hop", "e:sun.", "milo")], words=[("w:rainbow!", "RAINBOW!", .26, .2, .9, "sun")]),
    S("treehouse", (1250, 560, 1500), "Up, up goes Mango, all the way to the top of the trees.", tag="Mango climbs", cam2=(1300, 440, 1500), hide=["milo", "puff", "tumble"], move={"mango": (1150, 934, .55)},
      fx=[("to", "w:Up,", "#{p}mango_w", {"y": 330, "duration": 1.6, "ease": "power1.in"}, "Mango climbs up the ladder"), ("arm", "w:Up,", "mango", "r", -160)], words=[("w:top", "UP, UP!", .2, .2, .9, "sun")]),
    S("canopy", (900, 600, 1300), "Way up high is the canopy. Most animals in the rainforest live up here, in the canopy!", trans="iris", beat="fact", tag="fact: most animals live in the canopy", hide=["milo"],
      props=[prop("ar", lambda p: art.arrow(p, 620, 330, 800, 410), 0, 0, 1, True)],
      fx=[("show", "w:canopy.", "ar"), ("to", "w:animals", "#{p}mango-swing", {"rotation": 10, "svgOrigin": "0 0", "duration": .5, "yoyo": True, "repeat": 3}, "Mango swings")],
      words=[("w:canopy.", "THE CANOPY", .26, .2, .8, "pill"), ("w:Most", "MOST ANIMALS", .78, .8, .75, "sun")]),
    S("treehouse", (700, 640, 1500), "Mango brings fruit for everyone. A tree house party!", beat="ending", tag="fruit party", hide=["puff", "milo"],
      props=[prop("f1", A4.fruit, 560, 900, .36, True), prop("f2", A4.fruit, 660, 920, .36, True), prop("f3", A4.fruit, 760, 900, .36, True)],
      fx=[("show", "w:fruit", "f1"), ("show", "w:fruit", "f2"), ("show", "w:fruit", "f3"), ("hop", "w:party!", "mango"), ("hop", "w:party!", "tumble")], words=[("w:party!", "PARTY!", .72, .2, 1.0, "sun")]),
    S("treehouse", C("treehouse", "tumble", "head", 860, -40, 20), "Thank you for the umbrella idea, Mango.", who="tumble", beat="ending", tag="Tumble: thank you", hide=["mango", "milo", "puff"],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:umbrella", "tumble", -50, .4), ("trunk", "e:Mango.", "tumble", 0, .4)]),
    S("treehouse", C("treehouse", "mango", "head", 800, 0, 30), "We did it together. And Puff showed us the way!", who="mango", beat="ending", tag="Mango: together, and Puff", hide=["tumble", "milo", "puff"],
      props=[prop("h1", lambda p: art2.heart(p), *P("treehouse", "mango", "top", 170, 30), .6, True)], fx=[("face", 0.02, "mango", "happy"), ("show", "w:together.", "h1")]),
    S("treehouse", C("treehouse", "puff", "all", 760, 0, 0), "Thank you, Puff! See you soon!", tag="Milo: thank you Puff", hide=["tumble", "mango", "milo"],
      fx=[FLAP(0.2, 15), ("face", 0.02, "puff", "happy")], words=[("w:Puff!", "BYE, PUFF!", .74, .22, .85, "sun")]),
    S("zoo_eve", WIDE, "Back at the zoo, the sky is pink. And Mama is waiting.", trans="iris", beat="ending", tag="back at the zoo", cam2=(1000, 560, 1800),
      move={"tumble": (300, 940, .6), "mango": (-60, 940, .55)}, fx=[("walk", 0.1, "tumble", 360, 3.2), ("walk", 0.1, "mango", 360, 3.2)], words=[("w:Mama", "HOME!", .5, .16, 1.0, "sun")]),
    S("zoo_eve", C("zoo_eve", "tumble", "all", 1000, 40, -60), "Mama! We made an umbrella, from a giant leaf!", who="tumble", beat="ending", tag="Tumble tells Mama", hide=["mama", "milo", "mango"],
      fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:umbrella,", "tumble"), ("trunk", "w:giant", "tumble", -90, .4)], words=[("w:giant", "A GIANT LEAF", .5, .16, .7, "pill")]),
    S("zoo_eve", C("zoo_eve", "mama", "head", 900, 60, 50), "What a clever idea. You all worked together. I am so proud of you.", who="mama", beat="ending", tag="Mama: so proud", hide=["milo", "tumble", "mango"],
      fx=[("nod", "w:clever", "mama"), ("nod", "w:together.", "mama"), ("blinkslow", "w:proud", "mama-eye", 1)], words=[("w:proud", "SO PROUD!", .2, .2, .8, "sun")]),
    S("zoo_eve", (1200, 660, 1400), "Mama wraps her trunk around Tumble. A big, warm trunk hug.", beat="ending", tag="trunk hug", hide=["milo", "mango"], move={"tumble": (900, 940, .6)},
      props=[prop("h1", lambda p: art2.heart(p), 1030, 470, .7, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 1105, 440, .5, True)],
      fx=[("trunk", "w:wraps", "mama", 34, .8), ("lookat", "w:wraps", "mama", 8), ("show", "w:big,", "h1"), ("show", "w:hug.", "h2"),
          ("to", "w:big,", "#{p}h1_w,#{p}h2_w", {"y": "-=60", "duration": 1.6, "ease": "sine.out"}, "")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 130, 0), "When a job is too big for one, we can do it together. And there is always room for one more friend.", beat="ending", tag="the lesson",
      hide=["mama", "tumble", "mango"], fx=[("hop", "w:together.", "milo"), ("hop", "w:friend.", "milo")],
      words=[("w:together.", "TOGETHER", .73, .16, .75, "sun"), ("w:room", "ROOM FOR ONE MORE", .73, .3, .55, "pill")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 40, 0), "Do you remember? What did the little bats make from a leaf? A tent, or a boat?", q=True, beat="ending", tag="question: tent or boat", pause=3.2,
      hide=["mama", "tumble", "mango"], cam2=C("zoo_eve", "milo", "body", 830, 40, -60), fx=[("hop", "w:remember?", "milo"), ("signs", "w:tent,", ["TENT", "BOAT"], 0, "wait:1.8")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 960, 120, -40), "Where do most rainforest animals live? In the treetops, or in the mud?", q=True, beat="ending", tag="question: treetops or mud", pause=3.2,
      hide=["mama", "tumble", "mango"], cam2=C("zoo_eve", "milo", "body", 900, 120, -80), fx=[("hop", "w:live?", "milo"), ("signs", "w:treetops,", ["TREETOPS", "MUD"], 0, "wait:1.8")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 1080, -160, -40), "And how many friends fit under the giant leaf? Two, or four?", q=True, beat="ending", tag="question: two or four", pause=3.2,
      hide=["mama", "tumble", "mango"], cam2=C("zoo_eve", "milo", "body", 1000, -160, -80), fx=[("hop", "w:leaf?", "milo"), ("signs", "w:Two,", ["TWO", "FOUR"], 1, "wait:1.8")]),
    S("zoo_eve", (980, 560, 1880), "Drip, drop, drip, drop, hear the rain. Under our leaf, we're dry again!", beat="ending", tag="the closing rhyme", cam2=(1000, 560, 1780),
      fx=[("hop", "w:Drip,", "milo"), ("hop", "w:hear", "tumble"), ("hop", "w:leaf,", "mango"), ("nod", "w:again!", "mama")], words=[("w:Drip,", "DRIP, DROP!", .5, .15, .7, "sun")]),
    S("zoo_eve", WIDE, who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(980, 560, 1880),
      fx=[("hop", 1.0, "tumble"), ("hop", 1.0, "mango"), ("nod", 3.2, "mama"), ("hop", 2.2, "milo")], words=[(TB(3), "HOORAY!", .5, .2, 1.05, "sun")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 0, 0), "Next time: Sandy and the flying scarf! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure", hide=["mama", "tumble", "mango"],
      fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .78, .17, .8, "sun"), ("w:See", "SEE YOU SOON!", .78, .32, .72, "pill")]),
]

# thumbnail (thumb.py): the example in the picture (four friends under one giant leaf in the rain), 3 words at most, none of the title's words, no watermark
THUMBS = {
    "za_ep06": {"place": "bigtree", "cam": (920, 600, 1500),
                "actors": [("tumble", 360, 930, .6, False, 'gsap.set("#P-trunk",{rotation:-100,svgOrigin:"392 -430"});'),
                           ("monkey", 1080, 934, .55, False, 'gsap.set("#P-ar",{rotation:-160,svgOrigin:"58 -206"});'),
                           ("milo", 950, 620, .62, False, ''),
                           ("bat_hang", 1190, TIP(360)[1] + 10 - 250, .32, False, '')],
                "props": [(lambda p: A.rain_dry(p, [HOLE(360)]), -500, -700, 1.0), (lambda p: A.giant_leaf(p, LEAF_W), TIP(360)[0], TIP(360)[1] + 10, 1.0), (A3.tint, 0, 0, 1.0)],
                "words": [("ROOM FOR ALL!", 1400, 230, 170, "sun")]},
}
