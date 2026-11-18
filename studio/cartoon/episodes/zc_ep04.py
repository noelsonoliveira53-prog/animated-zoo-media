"""zc_ep04: "Why Do Monkeys Have Long Tails?" - cartoon fact lesson with Milo and Mango the spider monkey (3D music-and-sync process: "beat").
Milo's question: is a long tail a toy, a scarf, or a hand? Three parts, each cut whole into one Short:
1. a long tail that grabs (longer than her body; it holds on like an extra hand: two hands, two feet and a tail), 2. hanging upside down
(the tail holds her whole body, her hands are free to pick fruit; why she is called a SPIDER monkey), 3. the tip of the tail (little lines
like a fingertip, each monkey's own, they help it grip), four long fingers that hook, and a baby that holds on to its mama's tail.
The food lesson is zc_ep06 and is not repeated here (only "her hands are free to pick fruit").

FACTS, read at the source on Nov 18 2026 (each page fetched by the session's page reader, which quoted these sentences; nothing is said as an animal fact without one):
 [NGK] National Geographic Kids, kids.nationalgeographic.com/animals/mammals/facts/spider-monkey
   "has a prehensile tail, which means it can grasp" ... "can be used like a fifth limb to grab trees."
   "They were named spider monkeys because they look like spiders as they hang upside down from their tails" "with their arms and legs dangling."
   "Spider monkeys have long, thin arms with hooklike hands that allow them to swing through the trees."
   "They spend most of the daylight hours climbing and swinging through the high canopy of trees."
 [NG] National Geographic, nationalgeographic.com/animals/mammals/facts/spider-monkeys
   (the tail) "It is generally longer than the animal's body and acts as a fifth limb"   "The spider monkey's tail is prehensile, which means 'capable of grasping.'"
   "It can support a spider monkey's full body weight" "and allows them to hang onto branches, freeing their hands so they can climb, forage, and eat."
   "Spider monkeys can let go with their arms and hang by their tail as they play"
   "Baby spider monkeys also wrap their tiny tail around their mother's tail for security"
   "The set of lines on the end of a spider monkey's prehensile tail is unique to each monkey, like human fingerprints."
   "Four long fingers on each hand help them grasp branches, too."
   "which get their name from the way their long limbs and tails resemble spider legs as they dangle from branches"
 [WNPRC] Wisconsin National Primate Research Center, Primate Info Net, primate.wisc.edu/primate-info-net/pin-factsheets/black-spider-monkey
   "On the underside of the very tip of the tail there is a patch of skin with distinct pattern of lines like a fingerprint"
   "it helps the tail grip onto surfaces, much like fingers on a hand"   "taking advantage of their tails to free both hands for collecting fruit"
 [SDZ] San Diego Zoo, animals.sandiegozoo.org/animals/monkey
   "Tails that can grab and hold are called prehensile."   "Prehensile tails come in handy for holding on to tree branches while a monkey collects food"
 Not fetched: Los Angeles Zoo (the page did not load today): nothing from it is used.
 Read but NOT said: thumbs (Nat Geo Kids "do not have opposable thumbs", Nat Geo "thumbs but those are extremely short": the two pages word it differently, so
 the lesson only says "four long fingers"), sizes in inches, "every monkey has a tail like this" (San Diego Zoo: Old World monkeys do not).
 "Two hands, two feet and a tail: five" is Nat Geo's "fifth limb" counted for small children. A spider in this film is a friendly cartoon, only to show the name.
 "To feel safe" is Nat Geo's "for security".
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_zc_ep06 as A6          # the treetop places and Mango's friends (read only)
import art_zc_ep04 as A
from kit import Kit, S, prop, W

for _k in A6.FUR: kit.PT[_k] = kit.PT["monkey"]; kit.BOX[_k] = kit.BOX["monkey"]

EP = {"id": "zc_ep04", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "Why Do Monkeys Have Long Tails?", "thumb_text": "EXTRA HAND?!", "series": "Animal Facts with Milo",
      "description": ("Why do monkeys have long tails? Is a tail a toy, a scarf, or a hand? Milo the bluebird visits Mango the spider monkey in the rainforest treetops to find out! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn that a spider monkey's tail is longer than its body, that it can grab and hold on like an extra hand, that it can hold up the "
                      "monkey's whole body so both hands are free to pick fruit, why it is called a spider monkey, that the tip of the tail has little lines like a fingertip, "
                      "different for every monkey, and that a baby spider monkey wraps its tiny tail around its mother's tail.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNational Geographic Kids (spider monkey); National Geographic (spider monkeys); "
                      "Wisconsin National Primate Research Center, Primate Info Net (black spider monkey); San Diego Zoo (monkeys)."),
      "tags": ["monkey", "monkeys for kids", "spider monkey", "monkey tail", "why do monkeys have tails", "rainforest animals for kids", "animal facts for kids",
               "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

MX = 1100; MY = 432; MS = .62          # Mango sitting on the treetop branch
TREE = [("mango", "monkey", MX, MY, MS), ("milo", "milo", 420, 300, .62, False, True)]
STAGES = {"zoo": [("milo", "milo", 960, 940, 1.1, False, False)], "canopy": TREE, "figtree": TREE, "blossom": TREE, "canopy_eve": TREE,
          "bigtree": [("mango", "monkey", 900, -536, .7)]}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920); INK = art.INK
MW = (960, 380, 1800)                       # the treetop, wide
MC = (MX, 290, 1000)                        # Mango, whole
MH = (MX, 262, 720)                         # Mango, close
MP = WV("canopy", ["mango"], floor=.68, top=.42)
MPW = WV("canopy", ["mango"], hmin=1040, floor=.68, top=.42)
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 900))

# Mango hanging by her tail under the branch: (HX, HY) is where the tail holds on
HX = 1000; HY = 462; HS = .62
HANG = lambda kind="monkey_hang", x=HX: [("mango", kind, x, HY, HS)]
HC = (HX, 610, 1000)                 # hanging, whole: the branch near the top of the picture
HH = (HX, 700, 680)                  # her face, close (upside down)
HT = (HX, 470, 560)                  # the tail round the branch, close
HQ = (HX, 540, 1400)                 # a question: room above the branch for the two answer signs
HP = (HX, 560, 1100)                 # 9:16: hanging, whole, under the title
HPQ = (HX, 520, 1250)                # 9:16: a question (signs at 30-38 % of the height: above the branch)
HPH = (HX, 640, 820)                 # 9:16: close
HPT = (HX, 520, 700)                 # 9:16: the tail, close


def DANGLE(at, who="mango", deg=160):
    """Hanging, her arms let go and dangle down (inside the upside-down body an arm turned by 160 degrees points at the ground)."""
    return [("to", at, "#{p}" + who + "-ar", {"rotation": -deg, "svgOrigin": "58 -206", "duration": .5, "ease": "power2.out"}, "her arms dangle"),
            ("to", at, "#{p}" + who + "-al", {"rotation": deg, "svgOrigin": "-58 -206", "duration": .5, "ease": "power2.out"}, "")]


def DROP(at=0):
    return ("fromto", at, "#{p}mango_w", {"y": HY - 400}, {"y": HY, "duration": .7, "ease": "back.out(1.4)"}, "Mango swings down on her tail")


def MUNCH(at, who="mango", n=11): return ("to", at, "#{p}" + who + "-jaw", {"opacity": 1, "y": 12, "duration": .16, "yoyo": True, "repeat": n}, "Mango munches")


SQUEEZE = lambda at: ("to", at, "#{p}mango-tail", {"scale": 1.06, "transformOrigin": "50% 0%", "duration": .2, "yoyo": True, "repeat": 5}, "the tail squeezes the branch")

# ------------------------------------------------------------------ boards
BRD = (960, 540, 1500); BRDP = (960, 480, 1700)
# the tail against her body: Mango standing on the board, her own tail hidden, the measured tail from her hip
TM = (760, 860, 1.0)
def MEASURE(tail_hidden=False, lb_hidden=False, lt_hidden=False):
    return [prop("tl", A.tail_up, TM[0] + 40, TM[1] - 80, 1.0, tail_hidden, p=(TM[0] + 40, TM[1] - 80, 1.0)),
            prop("lb", lambda p: A.level(p, 560, "#2f80ed"), 820, TM[1] - 420, 1.0, lb_hidden, p=(820, TM[1] - 420, 1.0)),
            prop("lt", lambda p: A.level(p, 560), 960, TM[1] - 640, 1.0, lt_hidden, p=(960, TM[1] - 640, 1.0))]
MEASURE_ACT = [("m", "monkey", *TM)]
HIDE_TAIL = ("to", 0, "#{p}m-tail", {"opacity": 0, "duration": .01}, "")
MCAM = (980, 560, 1500); MPC = (980, 520, 1700)

# two hands, two feet and a tail: Mango big on the board, a number at each
CM = (960, 820, 1.25)
BX = [(690, 690), (1230, 690), (790, 900), (1130, 900), (1360, 430)]      # left hand, right hand, left foot, right foot, tail
BXP = [(640, 690), (1280, 690), (760, 900), (1160, 900), (1260, 380)]
CCAM = (980, 600, 1560); CPC = (980, 600, 1800)
def BADGES(shown, new=()): return [prop(f"b{k}", A.badge(k + 1), *BX[k], 1.0, k in new, p=(*BXP[k], 1.0)) for k in range(5) if k in shown or k in new]

# the tail tips
TIPS = [(520, 560), (960, 560), (1400, 560)]
TIPSP = [(960, 380), (960, 720), (960, 1060)]

SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("canopy", HC, "Why does a monkey have such a long tail?", q=True, tag="hook: why a long tail", actors=HANG(), pcam=HP,
      fx=[DROP(0.05), ("face", 0.3, "mango", "happy")], words=[("w:tail?", "?", .82, .3, 3.0, "sun", (.8, .36), 1.5)]),
    S("paper_pink", BRD, "Is it a toy? A scarf? Or a hand?", tag="hook: guesses", pcam=BRDP,
      props=[prop("a", A.ball, 560, 560, 1.1, True, p=(700, 600, .9)), prop("b", A.scarf, 960, 560, 1.2, True, p=(1220, 760, .9)), prop("c", A.hand_big, 1360, 580, .8, True, p=(800, 980, .7))],
      fx=[("show", "w:toy?", "a"), ("show", "w:scarf?", "b"), ("show", "w:hand?", "c")], words=[("e:hand?", "?", .5, .14, 1.8, "sun", (.5, .33), 1.5)]),
    S("canopy", say="I'm Milo. Let's find out together!", tag="hook: Milo", hide=["mango"], fx=[("hop", "w:find", "milo")], **MILO("canopy")),
    # ---------------------------------------------------------------- INTRO
    S("zoo", WIDE, "Welcome to The Animated Zoo, friends!", trans="iris", tag="gate wide", words=[("w:Animated", "HELLO!", .74, .6, 1.2, "pill")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, -40), "Today we fly up to the rainforest treetops.", tag="Milo close", words=[("w:treetops.", "THE TREETOPS", .5, .16, 1.1, "sun")]),
    S("canopy", MW, "Here we are! Look who is sitting on the branch.", trans="iris", tag="treetops wide", cam2=(980, 370, 1700), pcam=MPW, pcam2=MPW,
      fx=[("fromto", 0, "#{p}milo_w", {"x": -300, "y": 520}, {"x": 420, "y": 300, "duration": 1.3, "ease": "power2.out"}, "Milo flies in")]),
    S("canopy", MC, "This is Mango. Mango is a spider monkey.", tag="this is Mango", hide=["milo"], pcam=MP, words=[("w:Mango.", "MANGO", .2, .3, 1.1, "pill", (.5, .33))],
      fx=[("hop", "w:Mango.", "mango"), ("arm", "w:spider", "mango", "r", -60)]),
    # ---------------------------------------------------------------- PART 1: a long tail that grabs
    S("canopy", (MX + 60, 262, 800), "Hello, Mango! Look behind her. What a long tail!", part=1, tag="a long tail", hide=["milo"], pcam=MPW, pcam2=MPW,
      props=[prop("ar", lambda p: art.arrow(p, MX + 330, 90, MX + 190, 200), 0, 0, 1, True)],
      fx=[("show", "w:long", "ar"), ("to", "w:long", "#{p}mango-tail", {"rotation": 14, "svgOrigin": "40 -80", "duration": .25, "yoyo": True, "repeat": 5}, "Mango wiggles her tail")],
      words=[("w:long", "LONG TAIL!", .22, .3, 1.0, "sun", (.5, .33), .9)]),
    S("canopy", MC, "It curls, and wiggles, and swishes!", part=1, tag="curls and wiggles", hide=["milo"], pcam=MPW, pcam2=MPW,
      fx=[("to", "w:curls,", "#{p}mango-tail", {"rotation": -16, "svgOrigin": "40 -80", "duration": .3, "yoyo": True, "repeat": 1}, "the tail curls"),
          ("to", "w:wiggles,", "#{p}mango-tail", {"rotation": 14, "svgOrigin": "40 -80", "duration": .15, "yoyo": True, "repeat": 3}, "the tail wiggles"),
          ("to", "w:swishes!", "#{p}mango-tail", {"rotation": 22, "svgOrigin": "40 -80", "duration": .4, "yoyo": True, "repeat": 1}, "the tail swishes")],
      words=[("w:swishes!", "SWISH!", .22, .3, 1.1, "sun", (.5, .33), .9)]),
    S("canopy", say="Do you have a tail? Wiggle, wiggle!", part=1, q=True, tag="your tail", hide=["mango"], pause=.6,
      fx=[("to", "w:Wiggle,", "#{p}milo", {"rotation": 6, "svgOrigin": "0 0", "duration": .2, "yoyo": True, "repeat": 5}, "Milo wiggles")],
      words=[("w:Wiggle,", "WIGGLE!", .76, .22, 1.1, "sun", (.5, .33))], **MILO("canopy")),
    S("paper", MCAM, "Let's measure. Mango stands up tall. This is her body.", part=1, tag="board: her body", pcam=MPC, actors=MEASURE_ACT,
      props=MEASURE(True, True, True), fx=[HIDE_TAIL, ("show", "w:body.", "lb"), ("hop", "w:tall.", "m")], words=[("w:body.", "BODY", .14, .3, 1.0, "pill", (.3, .33), .8)]),
    S("paper", MCAM, "And this is her tail, stretched out next to her.", part=1, tag="board: her tail", pcam=MPC, actors=MEASURE_ACT,
      props=MEASURE(True, False, True), fx=[HIDE_TAIL, ("show", "w:tail,", "tl"), ("show", "w:stretched", "lt")],
      words=[("w:tail,", "TAIL", .86, .2, 1.0, "sun", (.7, .33), .8)]),
    S("paper", MCAM, "Which one is longer? Her body, or her tail?", part=1, q=True, tag="question 1", pause=3.2, pcam=MPC, actors=MEASURE_ACT,
      props=MEASURE(), fx=[HIDE_TAIL, ("signs", "w:body,", ["BODY", "TAIL"], 1, "wait:2.0")]),
    S("paper", MCAM, "Her tail! A spider monkey's tail is longer than its body.", part=1, tag="board: longer", pcam=MPC, actors=MEASURE_ACT,
      props=MEASURE(), fx=[HIDE_TAIL, ("to", "w:longer", "#{p}tl_w", {"scale": 1.06, "transformOrigin": "0% 100%", "duration": .25, "yoyo": True, "repeat": 5}, "the tail pulses")],
      words=[("w:longer", "LONGER!", .8, .2, 1.1, "sun", (.5, .33), .95)]),
    S("canopy", say="Wow! Can you stretch out long, like a tail? Stretch!", part=1, q=True, tag="stretch", hide=["mango"],
      fx=[("to", "w:Stretch!", "#{p}milo-body", {"scaleY": 1.14, "scaleX": .95, "svgOrigin": "0 0", "duration": .4, "yoyo": True, "repeat": 3}, "Milo stretches up")],
      words=[("w:Stretch!", "STRETCH!", .76, .22, 1.0, "sun", (.5, .33))], **MILO("canopy")),
    S("canopy", MC, "But what does Mango do with her long tail? Watch!", part=1, q=True, tag="watch", hide=["milo"], pcam=MP, pause=.4,
      fx=[("face", "w:Watch!", "mango", "wow")], words=[("w:Watch!", "WATCH!", .2, .3, 1.0, "sun", (.5, .33), .9)]),
    S("canopy", HC, "She wraps it around the branch, and down she goes!", part=1, tag="she swings down", actors=HANG(), pcam=HP,
      fx=[DROP("w:down"), ("face", "w:goes!", "mango", "happy")], words=[("w:goes!", "WHEE!", .2, .3, 1.1, "sun", (.5, .33), .9)]),
    S("canopy", HT, "Her tail holds on tight. Squeeze!", part=1, tag="squeeze", actors=HANG(), pcam=HPT,
      props=[prop("ar", lambda p: art.arrow(p, HX - 260, 320, HX - 80, 430), 0, 0, 1, True, p=(-60, 0, 1))], fx=[("show", "w:tail", "ar"), SQUEEZE("w:Squeeze!")],
      words=[("w:Squeeze!", "SQUEEZE!", .75, .22, 1.0, "sun", (.5, .33), .85)]),
    S("paper_blue", BRD, "A spider monkey's tail can grab, and hold on.", part=1, tag="board: grab", pcam=BRDP,
      actors=[("m", "monkey_hang", 960, 300, .95)], props=[prop("br", A.branch, 960, 300, 1.0, p=(960, 300, 1.0)),
                                                        prop("ar", lambda p: art.arrow(p, 620, 470, 880, 330), 0, 0, 1, True, p=(120, 60, 1))],
      fx=[("show", "w:grab,", "ar")], words=[("w:grab,", "GRAB!", .2, .62, 1.2, "sun", (.5, .33), 1.0), ("w:hold", "HOLD ON!", .8, .62, 1.0, "pill", (.5, .42), .9)]),
    S("canopy", HT, "Round and round the branch it goes.", part=1, tag="round and round", actors=HANG(), pcam=HPT, fx=[SQUEEZE("w:Round")],
      words=[("w:round", "ROUND AND ROUND", .5, .2, .8, "sun", (.5, .33), .7)]),
    S("paper_blue", BRD, "It holds on, just like an extra hand!", part=1, tag="board: extra hand", pcam=BRDP,
      actors=[("m", "monkey_hang", 960, 300, .95)], props=[prop("br", A.branch, 960, 300, 1.0, p=(960, 300, 1.0)), prop("hd", A.hand_big, 1420, 640, .62, True, p=(960, 1040, .5))],
      fx=[("show", "w:extra", "hd")], words=[("w:extra", "EXTRA HAND!", .22, .62, 1.0, "sun", (.5, .33), .9)]),
    S("canopy", say="Can you grab with your hand? Squeeze, squeeze!", part=1, q=True, tag="your hand", hide=["mango"], fx=[("hop", "w:Squeeze,", "milo", 2)],
      words=[("w:Squeeze,", "SQUEEZE!", .76, .22, 1.0, "sun", (.5, .33))], **MILO("canopy")),
    S("paper_pink", CCAM, "Let's count what Mango can hold on with.", part=1, q=True, tag="board: let's count", pcam=CPC, actors=[("m", "monkey", *CM)],
      words=[("w:count", "LET'S COUNT!", .5, .12, 1.0, "sun", (.5, .2), .9)]),
    S("paper_pink", CCAM, "One hand, two hands,", part=1, tag="board: hands", pcam=CPC, actors=[("m", "monkey", *CM)], props=BADGES((), (0, 1)),
      fx=[("show", "w:One", "b0"), ("show", "w:two", "b1"), ("arm", "w:One", "m", "l", 20), ("arm", "w:two", "m", "r", -20)]),
    S("paper_pink", CCAM, "one foot, two feet,", part=1, tag="board: feet", pcam=CPC, actors=[("m", "monkey", *CM)], props=BADGES((0, 1), (2, 3)),
      fx=[("show", "w:one", "b2"), ("show", "w:two", "b3"), ("hop", "w:feet,", "m")]),
    S("paper_pink", CCAM, "and her long tail. Five!", part=1, tag="board: five", pcam=CPC, actors=[("m", "monkey", *CM)], props=BADGES((0, 1, 2, 3), (4,)),
      fx=[("show", "w:tail.", "b4"), ("to", "w:tail.", "#{p}m-tail", {"rotation": 12, "svgOrigin": "40 -80", "duration": .25, "yoyo": True, "repeat": 3}, "")],
      words=[("w:Five!", "5!", .5, .12, 1.4, "sun", (.5, .2), 1.3)]),
    S("canopy", HQ, "How many can Mango hold on with? Four, or five?", part=1, q=True, tag="question 2", pause=3.2, actors=HANG(), pcam=HPQ,
      fx=[("signs", "w:Four,", ["4", "5"], 1, "wait:2.0"), SQUEEZE("wait:2.05")]),
    S("paper_pink", CCAM, "Five! Two hands, two feet, and one tail.", part=1, tag="board: five again", pcam=CPC, actors=[("m", "monkey", *CM)], props=BADGES(range(5)),
      fx=[("hop", "w:Five!", "m")], words=[("w:Five!", "FIVE!", .5, .12, 1.2, "sun", (.5, .2), 1.0)]),
    S("canopy", HC, "Mango has five ways to hold on!", part=1, tag="five ways", actors=HANG(), pcam=HP, fx=[SQUEEZE("w:five"), ("face", "w:hold", "mango", "happy")],
      words=[("w:five", "5 WAYS!", .22, .3, 1.1, "sun", (.5, .33), .9)]),
    S("canopy", say="How many hands do you have? Show me!", part=1, q=True, tag="your hands", hide=["mango"], pause=1.0, fx=[("hop", "w:Show", "milo")],
      words=[("w:hands", "SHOW ME!", .76, .22, 1.0, "sun", (.5, .33))], **MILO("canopy")),
    # ---------------------------------------------------------------- PART 2: hanging upside down, hands free
    S("figtree", MW, "Look! A tree full of golden fruit.", part=2, trans="iris", tag="the fruit tree", cam2=(980, 370, 1700), pcam=MPW, pcam2=MPW, hide=["milo"],
      words=[("w:fruit.", "FRUIT!", .8, .56, 1.2, "sun", (.5, .33))]),
    S("figtree", HC, "Mango hangs upside down, just by her tail!", part=2, tag="upside down", actors=HANG(), pcam=HP,
      fx=[DROP(0.05), ("face", "w:upside", "mango", "happy")], words=[("w:upside", "UPSIDE DOWN!", .22, .3, .85, "sun", (.5, .33), .8)]),
    S("bigtree", (960, -60, 2860), "Spider monkeys spend most of the day high up in the treetops.", part=2, trans="iris", tag="high up", cam2=(980, -200, 2500), pcam=(950, -690, 2000), pcam2=(950, -700, 1800),
      actors=[("mango", "monkey_hang", 900, -515, .7)], props=[prop("ar", lambda p: art.arrow(p, 620, 500, 620, -400), 0, 0, 1, True)], fx=[("show", "w:high", "ar")],
      words=[("w:high", "UP HIGH", .24, .5, .8, "sun", (.5, .33), .9)]),
    S("canopy", (960, 560, 1500), "They climb, and swing, from branch to branch.", part=2, trans="iris", tag="swing along", actors=HANG(x=600), pcam=(1000, 520, 1300), pcam2=(1250, 520, 1300),
      fx=[("to", "w:swing,", "#{p}mango_w", {"x": 1350, "duration": 2.4, "ease": "power1.inOut"}, "Mango swings along the branch"),
          ("to", "w:swing,", "#{p}mango-swing", {"rotation": -16, "svgOrigin": "0 0", "duration": .6, "yoyo": True, "repeat": 3}, "")],
      words=[("w:swing,", "SWING!", .8, .3, 1.1, "sun", (.5, .33), .9)]),
    S("canopy", HC, "Sometimes spider monkeys hang by their tails just to play!", part=2, tag="hang to play", actors=HANG(), pcam=HP,
      fx=[("to", "w:play!", "#{p}mango-swing", {"rotation": 18, "svgOrigin": "0 0", "duration": .45, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "Mango swings to play"), ("face", "w:play!", "mango", "happy")],
      words=[("w:play!", "PLAY TIME!", .22, .3, 1.0, "sun", (.5, .33), .9)]),
    S("canopy", say="What do you like to play?", part=2, q=True, tag="your play", hide=["mango"], pause=1.2, fx=[("hop", "w:play?", "milo")],
      words=[("w:play?", "PLAY!", .76, .22, 1.2, "sun", (.5, .33))], **MILO("canopy")),
    S("paper_blue", BRD, "A spider monkey's tail can hold up its whole body.", part=2, tag="board: whole body", pcam=BRDP,
      actors=[("m", "monkey_hang", 960, 300, .95)], props=[prop("br", A.branch, 960, 300, 1.0, p=(960, 300, 1.0)),
                                                        prop("ar", lambda p: art.arrow(p, 620, 470, 880, 330), 0, 0, 1, True, p=(120, 60, 1))],
      fx=[("show", "w:tail", "ar"), ("to", "w:whole", "#{p}m", {"scale": 1.05, "svgOrigin": "0 300", "duration": .25, "yoyo": True, "repeat": 3}, "")],
      words=[("w:whole", "WHOLE BODY!", .76, .62, 1.0, "sun", (.5, .33), .9)]),
    S("canopy", say="Can you tilt your head, like Mango? Tilt!", part=2, q=True, tag="tilt", hide=["mango"],
      fx=[("to", "w:Tilt!", "#{p}milo", {"rotation": -20, "svgOrigin": "0 -150", "duration": .35, "yoyo": True, "repeat": 3}, "Milo tilts his head")],
      words=[("w:Tilt!", "TILT!", .76, .22, 1.1, "sun", (.5, .33))], **MILO("canopy")),
    S("figtree", HH, "Now both of her hands are free. What will she do?", part=2, q=True, tag="hands free", trans="iris", actors=HANG(), pcam=HPH, pause=.8,
      fx=[("face", "w:free.", "mango", "wow")], words=[("w:free.", "HANDS FREE!", .5, .14, .9, "sun", (.5, .33), .8)]),
    S("figtree", HQ, "Can Mango pick fruit while she hangs? Yes, or no?", part=2, q=True, tag="question 3", pause=3.2, actors=HANG(), pcam=HPQ,
      props=[prop("f1", art2.fruit, HX - 230, 610, .4), prop("f2", art2.fruit, HX + 230, 610, .4)],
      fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0"), SQUEEZE("wait:2.05")]),
    S("figtree", HC, "Yes! One fruit, two fruits. Both hands are busy!", part=2, tag="two fruits", actors=HANG("monkey_hangfruit"), pcam=HP,
      fx=[("face", 0.05, "mango", "happy")], words=[("w:One", "1", .3, .3, 1.4, "sun", (.3, .36), 1.1), ("w:two", "2", .7, .3, 1.4, "sun", (.7, .36), 1.1)]),
    S("figtree", say="Count the fruits with me. One, two!", part=2, q=True, tag="count the fruits", hide=["mango"], fx=[("hop", "w:One,", "milo"), ("hop", "w:two!", "milo")],
      words=[("w:One,", "1", .66, .22, 1.3, "sun", (.38, .33)), ("w:two!", "2", .86, .22, 1.3, "sun", (.62, .33))], **MILO("canopy")),
    S("paper", BRD, "Her tail holds on, so her hands can pick, and eat.", part=2, tag="board: tail holds, hands eat", pcam=BRDP,
      actors=[("m", "monkey_hangfruit", 960, 300, .95)], props=[prop("br", A.branch, 960, 300, 1.0, p=(960, 300, 1.0))],
      fx=[SQUEEZE("w:holds")], words=[("w:tail", "TAIL: HOLD", .2, .7, .8, "pill", (.5, .25), .7), ("w:hands", "HANDS: EAT", .8, .7, .8, "sun", (.5, .9), .7)]),
    S("figtree", HC, "Two hands for fruit, and one tail to hold on.", part=2, tag="two hands one tail", actors=HANG("monkey_hangfruit"), pcam=HP, fx=[SQUEEZE("w:tail")],
      words=[("w:Two", "2 HANDS", .25, .3, .9, "sun", (.5, .33), .8), ("w:tail", "1 TAIL", .75, .3, .9, "pill", (.5, .42), .8)]),
    S("figtree", HH, "Munch, munch! A snack, upside down!", part=2, tag="munch", actors=HANG("monkey_hangfruit"), pcam=HPH,
      fx=[MUNCH("w:Munch,", n=13), ("face", "w:snack,", "mango", "happy")], words=[("w:Munch,", "MUNCH!", .5, .14, 1.0, "sun", (.5, .33), .8)]),
    S("figtree", say="Pretend to munch a fruit with me. Yum!", part=2, q=True, tag="pretend to munch", hide=["mango"], fx=[("hop", "w:Yum!", "milo", 2)],
      words=[("w:Yum!", "YUM!", .76, .22, 1.2, "sun", (.5, .33))], **MILO("canopy")),
    S("paper", BRD, "Do you know why she is called a spider monkey?", part=2, q=True, tag="board: why spider", pcam=BRDP, pause=.8,
      props=[prop("q", lambda p: f'<g id="{p}"><text x="0" y="60" text-anchor="middle" font-family="Baloo, sans-serif" font-weight="800" font-size="300" fill="{art.SUN}" stroke="{INK}" stroke-width="14" paint-order="stroke fill">?</text></g>', 960, 560, 1.0, p=(960, 600, 1.0))],
      words=[("w:spider", "SPIDER?", .5, .16, 1.2, "sun", (.5, .25), 1.0)]),
    S("figtree", HC, "When she hangs, her long arms and legs dangle down.", part=2, tag="dangle", actors=HANG(), pcam=HP,
      fx=DANGLE("w:dangle"), words=[("w:dangle", "DANGLE!", .22, .3, 1.0, "sun", (.5, .33), .9)]),
    S("figtree", HH, "Hello, upside-down Mango!", part=2, tag="hello upside down", actors=HANG(), pcam=HPH, fx=DANGLE(0.01) + [("face", "w:Hello,", "mango", "happy")],
      words=[("w:Hello,", "HELLO!", .5, .14, 1.1, "sun", (.5, .33), .9)]),
    S("paper_blue", BRD, "Long arms, long legs, a little bit like a spider!", part=2, tag="board: like a spider", pcam=BRDP,
      actors=[("m", "monkey_hang", 600, 280, .85)], props=[prop("br", lambda p: A.branch(p, 800), 600, 280, 1.0, p=(960, 260, 1.0)), prop("sp", A.spider, 1300, 600, 1.4, True, p=(960, 980, 1.1))],
      fx=DANGLE(0.05, "m") + [("show", "w:spider!", "sp")], words=[("w:spider!", "LIKE A SPIDER!", .5, .14, .9, "sun", (.5, .2), .8)]),
    S("paper_blue", BRD, "That is how the spider monkey got its name!", part=2, tag="board: the name", pcam=BRDP,
      actors=[("m", "monkey_hang", 600, 280, .85)], props=[prop("br", lambda p: A.branch(p, 800), 600, 280, 1.0, p=(960, 260, 1.0)), prop("sp", A.spider, 1300, 600, 1.4, p=(960, 980, 1.1))],
      fx=DANGLE(0.01, "m"), words=[("w:name!", "SPIDER MONKEY!", .5, .14, .9, "sun", (.5, .2), .8)]),
    S("figtree", say="Can you wiggle your arms like a spider monkey?", part=2, q=True, tag="wiggle your arms", hide=["mango"], pause=.6,
      fx=[("to", "w:wiggle", "#{p}milo-wl,#{p}milo-wr", {"rotation": 30, "duration": .18, "yoyo": True, "repeat": 7}, "Milo flaps his wings")],
      words=[("w:wiggle", "WIGGLE!", .76, .22, 1.1, "sun", (.5, .33))], **MILO("canopy")),
    # ---------------------------------------------------------------- PART 3: the tip of the tail, four long fingers, a baby's tail
    S("blossom", MW, "Mango swings over to a tree full of flowers.", part=3, trans="iris", tag="the flower tree", cam2=(980, 370, 1700), pcam=HP, pcam2=HP,
      actors=HANG(x=HX - 500), fx=[("to", 0.1, "#{p}mango_w", {"x": HX, "duration": 2.6, "ease": "power1.inOut"}, "Mango swings along the branch")],
      words=[("w:flowers.", "FLOWERS!", .8, .62, 1.1, "sun", (.5, .33))]),
    S("blossom", HT, "Look closely at the very tip of her tail.", part=3, q=True, tag="the tip", actors=HANG(), pcam=HPT,
      props=[prop("ar", lambda p: art.arrow(p, HX - 260, 320, HX - 80, 430), 0, 0, 1, True, p=(-60, 0, 1))], fx=[("show", "w:tip", "ar")],
      words=[("w:tip", "THE TIP!", .75, .22, 1.0, "sun", (.5, .33), .85)]),
    S("paper", BRD, "Under the tip, there are little lines.", part=3, tag="board: little lines", pcam=BRDP, props=[prop("tt", A.tail_tip(0), 900, 560, 1.3, p=(900, 600, 1.2))],
      fx=[("to", "w:lines.", "#{p}tt-pad", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 5}, "the little lines glow")],
      words=[("w:lines.", "LITTLE LINES", .5, .14, 1.0, "sun", (.5, .25), .85)]),
    S("paper_pink", BRD, "Now look at your fingertip. You have little lines, too!", part=3, q=True, tag="board: your fingertip", pcam=BRDP, pause=.6,
      props=[prop("fg", A.fingertip, 960, 600, 1.0, p=(960, 640, 1.0))], words=[("w:fingertip.", "YOUR FINGER!", .5, .14, 1.0, "sun", (.5, .25), .85)]),
    S("blossom", say="Your little lines are only yours!", part=3, tag="only yours", hide=["mango"], fx=[("hop", "w:only", "milo")],
      words=[("w:yours!", "ONLY YOURS!", .76, .22, .9, "sun", (.5, .33), .85)], **MILO("canopy")),
    S("paper", (960, 560, 1700), "Here are three spider monkey tails. One, two, three.", part=3, tag="board: three tails", pcam=(960, 560, 1700),
      props=[prop(f"t{k}", A.tail_tip(k), *TIPS[k], .7, True, p=(*TIPSP[k], .6)) for k in range(3)],
      fx=[("show", "w:One,", "t0"), ("show", "w:two,", "t1"), ("show", "w:three.", "t2")], words=[("w:three", "3 TAILS", .5, .12, 1.0, "sun", (.5, .18), .9)]),
    S("paper", BRD, "Every spider monkey has its own lines. Look, all different!", part=3, tag="board: all different", pcam=(960, 560, 1700),
      props=[prop(f"t{k}", A.tail_tip(k), *TIPS[k], .7, p=(*TIPSP[k], .6)) for k in range(3)],
      fx=[("to", "w:own", "#{p}t0-pad,#{p}t1-pad,#{p}t2-pad", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 3}, "the three sets of lines glow")], words=[("w:different!", "ALL DIFFERENT!", .5, .12, .9, "sun", (.5, .18), .8)]),
    S("paper", (960, 560, 1700), "Are Mango's lines the same as her friend's? Yes, or no?", part=3, q=True, tag="question 4", pause=3.2, pcam=(960, 560, 1700),
      props=[prop("t0", A.tail_tip(0), 640, 640, .8, p=(960, 720, .6)), prop("t1", A.tail_tip(1), 1280, 640, .8, p=(960, 1060, .6))],
      fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("blossom", HC, "No! Mango's lines are only Mango's.", part=3, tag="only Mango's", actors=HANG(), pcam=HP,
      fx=[("face", 0.05, "mango", "happy"), SQUEEZE("w:only")], words=[("w:only", "ONLY MANGO'S!", .5, .14, .85, "sun", (.5, .33), .75)]),
    S("paper", BRD, "And the little lines help her tail hold on tight.", part=3, tag="board: lines grip", pcam=BRDP,
      props=[prop("br", lambda p: A.branch(p, 900), 960, 300, 1.0, p=(960, 300, 1.0)), prop("tt", A.tail_tip(0), 900, 560, 1.0, p=(900, 600, 1.0))],
      fx=[("to", "w:tight.", "#{p}tt_w", {"y": "-=60", "duration": .4, "yoyo": True, "repeat": 1}, "the tail tip presses up on the branch")],
      words=[("w:tight.", "HOLD TIGHT!", .5, .8, 1.0, "sun", (.5, .9), .85)]),
    S("blossom", HT, "Her tail holds the branch, tight, tight, tight!", part=3, tag="tight tight", actors=HANG(), pcam=HPT, fx=[SQUEEZE("w:tight,")],
      words=[("w:tight,", "TIGHT!", .75, .22, 1.1, "sun", (.5, .33), .9)]),
    S("paper_blue", BRD, "Her hands are good at holding, too. Four long fingers!", part=3, tag="board: four fingers", pcam=BRDP,
      props=[prop("hd", A.hand_big, 960, 640, 1.2, p=(960, 700, 1.1))] + [prop(f"n{k}", A.badge(k + 1), 960 + (-66 + 44 * k) * 1.2 + 24, 640 - 330, .55, True, p=(960 + (-66 + 44 * k) * 1.1 + 22, 700 - 305, .5)) for k in range(4)],
      fx=[("show", "w:Four", "n0"), ("show", "w:Four", "n1", None, False), ("show", "w:long", "n2"), ("show", "w:fingers!", "n3")],
      words=[("w:Four", "4 FINGERS", .2, .3, 1.0, "sun", (.5, .2), .8)]),
    S("paper_blue", BRD, "They hook onto a branch. Hook!", part=3, tag="board: hook", pcam=BRDP,
      props=[prop("br", lambda p: A.branch(p, 900), 960, 360, 1.0, p=(960, 380, 1.0)), prop("hd", A.hand_big, 960, 640, 1.2, p=(960, 700, 1.1))],
      fx=[("to", "w:hook", "#{p}hd-f", {"scaleY": .55, "svgOrigin": "0 -60", "duration": .4, "ease": "back.out(1.6)"}, "the fingers hook")],
      words=[("w:Hook!", "HOOK!", .8, .3, 1.2, "sun", (.5, .2), 1.0)]),
    S("blossom", say="Can you make a hook with your fingers? Hook!", part=3, q=True, tag="make a hook", hide=["mango"], pause=.6, fx=[("hop", "w:Hook!", "milo")],
      words=[("w:Hook!", "HOOK!", .76, .22, 1.2, "sun", (.5, .33))], **MILO("canopy")),
    S("blossom", HC, "Hands that hook, and a tail that grabs. Just right for the treetops!", part=3, tag="just right", actors=HANG("monkey_hangfruit"), pcam=HP,
      fx=[SQUEEZE("w:grabs."), ("face", "w:right", "mango", "happy")], words=[("w:right", "JUST RIGHT!", .5, .14, .9, "sun", (.5, .33), .8)]),
    S("canopy_eve", MW, "Look who is here! Mango's friend Coco, and her baby.", part=3, trans="iris", tag="Coco and baby", hide=["milo"], pcam=(1000, 300, 1150),
      actors=[("mango", "monkey", 700, MY, MS), ("coco", "monkey_c", 1150, MY, MS), ("baby", "monkey_b", 1330, MY, .3)],
      fx=[("hop", "w:Coco,", "coco"), ("hop", "w:baby.", "baby")], words=[("w:baby.", "A BABY!", .8, .56, 1.1, "sun", (.5, .33))]),
    S("paper_pink", BRD, "The baby wraps its tiny tail around its mama's tail.", part=3, tag="board: tails hold", pcam=BRDP,
      props=[prop("th", A.tails_hug, 960, 560, 1.0, p=(960, 620, .8))],
      fx=[("fromto", "w:wraps", "#{p}th-baby", {"opacity": 0}, {"opacity": 1, "duration": .5}, "the tiny tail wraps around")],
      words=[("w:tiny", "TINY TAIL", .3, .78, 1.0, "sun", (.5, .25), .8), ("w:mama's", "MAMA", .82, .3, 1.0, "pill", (.5, .85), .8)]),
    S("canopy_eve", (1240, 300, 760), "That helps the baby feel safe and snug.", part=3, tag="safe and snug", hide=["milo"], pcam=(1240, 280, 900),
      actors=[("mango", "monkey", 700, MY, MS), ("coco", "monkey_c", 1150, MY, MS), ("baby", "monkey_b", 1330, MY, .3)],
      props=[prop("h1", art2.heart, 1240, 110, 1.0, True)], fx=[("show", "w:safe", "h1"), ("face", 0.05, "baby", "happy"), ("face", 0.05, "coco", "happy")],
      words=[("w:snug.", "SAFE AND SNUG", .5, .86, .8, "pill", (.5, .25), .7)]),
    S("canopy_eve", say="Hold on tight, little baby!", part=3, tag="hold on baby", hide=["mango"], fx=[("hop", "w:baby!", "milo")],
      words=[("w:tight,", "HOLD ON!", .76, .22, 1.0, "sun", (.5, .33))], **MILO("canopy")),
    S("canopy_eve", say="Who do you hold hands with?", part=3, q=True, tag="hold hands", hide=["mango"], pause=1.2, fx=[("hop", "w:hold", "milo")],
      words=[("w:hands", "WHO?", .76, .22, 1.2, "sun", (.5, .33))], **MILO("canopy")),
    # ---------------------------------------------------------------- QUIZ + RECAP
    S("canopy_eve", say="Can you give yourself a big hug? Squeeze!", part=3, q=True, tag="a big hug", hide=["mango"], pause=.4,
      fx=[("to", "w:Squeeze!", "#{p}milo-body", {"scaleX": .9, "svgOrigin": "0 0", "duration": .3, "yoyo": True, "repeat": 3}, "Milo hugs himself")],
      words=[("w:hug?", "HUG!", .76, .22, 1.2, "sun", (.5, .33))], **MILO("canopy")),
    S("canopy_eve", HC, "What a wonderful tail, Mango!", part=3, tag="wonderful tail", actors=HANG(), pcam=HP,
      fx=[("face", 0.05, "mango", "happy"), ("to", "w:wonderful", "#{p}mango-swing", {"rotation": 12, "svgOrigin": "0 0", "duration": .4, "yoyo": True, "repeat": 3}, "Mango swings happily")],
      words=[("w:wonderful", "WONDERFUL!", .5, .14, .95, "sun", (.5, .33), .85)]),
    S("canopy_eve", MW, "Time to remember what we learned!", part=4, tag="quiz time", cam2=(980, 370, 1700), pcam=MPW, words=[("w:remember", "QUIZ TIME!", .5, .62, 1.3, "sun", (.5, .33))]),
    S("paper", MCAM, "Which is longer? Mango's body, or her tail?", part=4, q=True, tag="quiz 1", pause=3.2, pcam=MPC, actors=MEASURE_ACT,
      props=MEASURE(), fx=[HIDE_TAIL, ("signs", "w:body,", ["BODY", "TAIL"], 1, "wait:2.0")]),
    S("canopy_eve", HQ, "What can her tail do? Hold on, or sing?", part=4, q=True, tag="quiz 2", pause=3.2, actors=HANG(), pcam=HPQ,
      fx=[("signs", "w:Hold", ["HOLD ON", "SING"], 0, "wait:2.0"), SQUEEZE("wait:2.05")]),
    S("paper_blue", BRD, "Hold on! Just like an extra hand.", part=4, tag="board: extra hand again", pcam=BRDP,
      actors=[("m", "monkey_hangfruit", 960, 300, .95)], props=[prop("br", A.branch, 960, 300, 1.0, p=(960, 300, 1.0))],
      words=[("w:Hold", "HOLD ON!", .22, .62, 1.0, "sun", (.5, .33), .9)]),
    S("paper", BRD, "What is under the tip of her tail?", part=4, q=True, tag="quiz 3", pause=1.6, pcam=BRDP,
      props=[prop("tt", A.tail_tip(0), 900, 560, 1.3, p=(900, 600, 1.2))], words=[("end+0.3", "?", .82, .3, 2.4, "sun", (.5, .25), 1.5)]),
    S("paper_pink", BRD, "Little lines, just like your fingertip!", part=4, tag="board: lines again", pcam=BRDP,
      props=[prop("tt", A.tail_tip(0), 640, 560, .9, p=(960, 560, .7)), prop("fg", A.fingertip, 1320, 600, .8, p=(960, 1080, .6))],
      words=[("w:Little", "LITTLE LINES!", .5, .12, 1.0, "sun", (.5, .2), .85)]),
    S("canopy_eve", HC, "Good night, Mango. Hold on tight!", part=4, tag="good night", actors=HANG(), pcam=HP, props=[prop("h1", art2.heart, HX + 200, 560, 1.0, True)],
      fx=[("show", "w:tight!", "h1"), ("face", 0.05, "mango", "sleepy")]),
    S("canopy_eve", MW, "Thank you for learning with me, friends. See you at the zoo!", part=4, tag="goodbye", cam2=(960, 380, 1900), pcam=MPW,
      words=[("w:See", "SEE YOU AT THE ZOO!", .5, .62, .95, "pill", (.5, .33), .62)], fx=[("hop", "w:zoo!", "milo", 2), ("arm", "w:See", "mango", "r", -70)]),
]
for _s in SHOTS:        # a picture board never drifts closer in 9:16: it only pulls out a little (zc_ep06)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)

SHORTS = [
    {"id": "zc_ep04_short1", "title": "Why Is a Spider Monkey's Tail So Long?", "band": ("A TAIL THAT", "CAN GRAB?"), "thumb_text": "EXTRA HAND!", "part": 1,
     "extra_first": [S("canopy", HC, "What can a long monkey tail do?", part=1, q=True, tag="hook: what can it do", actors=HANG(), pcam=HP,
                       fx=[DROP(0.05), ("face", 0.3, "mango", "wow")], words=[("w:do?", "?", .78, .3, 2.6, "sun", (.8, .36), 1.4)])]},
    {"id": "zc_ep04_short2", "title": "Why Does This Monkey Hang Upside Down?", "band": ("UPSIDE", "DOWN?!"), "thumb_text": "SNACK TIME!", "part": 2,
     "extra_first": [S("figtree", HH, "Why is Mango upside down?", part=2, q=True, tag="hook: upside down", actors=HANG("monkey_hangfruit"), pcam=HPH,
                       fx=[("face", 0.05, "mango", "happy")], words=[("w:down?", "?", .2, .3, 2.6, "sun", (.22, .36), 1.4)])]},
    {"id": "zc_ep04_short3", "title": "What Is Under a Monkey's Tail Tip?", "band": ("LITTLE", "LINES?"), "thumb_text": "LIKE YOURS!", "part": 3,
     "extra_first": [S("paper", BRD, "What is hiding under a monkey's tail?", part=3, q=True, tag="hook: hiding under", pcam=BRDP,
                       props=[prop("tt", A.tail_tip(0), 900, 560, 1.3, p=(900, 600, 1.2))], words=[("w:tail?", "?", .82, .3, 2.6, "sun", (.5, .25), 1.5)])]},
]

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
THUMBS = {
    "zc_ep04": {"place": "canopy", "cam": (HX, 560, 1150), "actors": [("monkey_hangfruit", HX - 200, HY, .8, False, "")],
                "props": [],
                "words": [("EXTRA", 1420, 520, 200, ""), ("HAND?!", 1420, 740, 230, "sun")]},
    "zc_ep04_short1": {"place": "canopy", "cam": (HX, 560, 900), "actors": [("monkey_hang", HX, HY, HS, False, "")],
                       "props": [],
                       "words": [("EXTRA", 540, 300, 190, ""), ("HAND!", 540, 480, 210, "sun")]},
    "zc_ep04_short2": {"place": "figtree", "cam": (HX, 600, 800), "actors": [("monkey_hangfruit", HX, HY, HS, False, "")],
                       "props": [],
                       "words": [("SNACK", 540, 300, 190, ""), ("TIME!", 540, 480, 210, "sun")]},
    "zc_ep04_short3": {"place": "paper", "cam": (960, 600, 1300), "actors": [],
                       "props": [(A.tail_tip(0), 900, 640, 1.2)],
                       "words": [("LIKE", 540, 300, 190, ""), ("YOURS!", 540, 480, 210, "sun")]},
}
