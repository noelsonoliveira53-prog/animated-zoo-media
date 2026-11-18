"""zc_ep06: "What Does a Monkey Eat All Day?" - cartoon fact lesson with Milo and Mango the spider monkey (3D music-and-sync process: "beat").
Milo follows Mango from breakfast to dinner. Three parts, each cut whole into one Short:
1. breakfast: fruit comes first (and how she picks the best one), 2. lunch: the other foods, and eating in a small group, 3. dinner: the seeds travel.
The lesson is about FOOD; the tail lesson is zc_ep04 and is not repeated here (Mango sits and walks on her branch).

FACTS, read at the source on Nov 18 2026 (each page fetched and its sentences quoted by the session's page reader; nothing is stated as an animal fact without a quote):
 [NGK] National Geographic Kids, kids.nationalgeographic.com/animals/mammals/spider-monkey ("Spider Monkey")
   "During the day, the spider monkey searches for fruit, which makes up the main part of its diet."
   "They will also eat flowers, seeds, bark, leaves, and small insects during the dry season when fruit isn't available."
   "They spend most of the daylight hours climbing and swinging through the high canopy of trees."
   "They split into smaller groups for feeding."   "Spider monkeys usually live in groups of 20 to 30"
 [LAZ] Los Angeles Zoo, lazoo.org/explore-your-zoo/our-animals/mammals/geoffroys-black-handed-spider-monkey
   "Their diet is 80 percent fruit with some young leaves and flowers."   "Their keen color vision allows them to select the best fruit."
   "These monkeys break into smaller groups to forage during the day and return to the group (which numbers between 20 and 30 individuals) at night."
 [NG] National Geographic, nationalgeographic.com/animals/mammals/facts/spider-monkeys
   "Spider monkeys are important seed dispersers for their rainforest homes."
   "When animals eat fruit and nuts from trees and then go on their merry way, they eventually defecate the seeds"
 [IFAW] ifaw.org/international/animals/spider-monkeys
   "As they move about the canopy, dispersing seeds through their droppings, they actively assist in the regeneration and health of their habitats."
 Plain observations, not animal facts: a fruit can be green or golden; bark is the outside of a tree; a seed in the ground can grow into a plant.
 Read but NOT said: eggs, honey, arachnids, nuts (not on every page), the tail as a fifth limb (that is zc_ep04's lesson).
 "Eight bites out of ten" is the Los Angeles Zoo's "80 percent fruit" shown as ten plates.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_zc_ep06 as A
from kit import Kit, S, prop, W
from episodes.zc_ep02 import crossx

for _k in A.FUR: kit.PT[_k] = kit.PT["monkey"]; kit.BOX[_k] = kit.BOX["monkey"]

EP = {"id": "zc_ep06", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "What Does a Monkey Eat All Day?", "thumb_text": "YUM, FRUIT!", "series": "Animal Facts with Milo",
      "description": ("What does a monkey eat all day? Fruit, leaves, or little bugs? Milo the bluebird follows Mango the spider monkey from breakfast to dinner to find out! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn that fruit is the main food of a spider monkey, that spider monkeys see colors well and pick the best fruit, that they also eat "
                      "flowers, leaves, seeds, bark and small insects, that the big group splits into smaller groups to find food, and that spider monkeys spread seeds around the rainforest.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNational Geographic Kids (spider monkey); Los Angeles Zoo (Geoffroy's black-handed spider monkey); "
                      "National Geographic (spider monkeys); IFAW (spider monkeys)."),
      "tags": ["monkey", "monkeys for kids", "spider monkey", "what do monkeys eat", "rainforest animals for kids", "animal facts for kids", "learning videos for toddlers", "preschool",
               "Milo the bluebird", "The Animated Zoo"]}

MX = 1100; MY = 432; MS = .62          # Mango on the treetop branch
TREE = [("mango", "monkey", MX, MY, MS), ("milo", "milo", 420, 300, .62, False, True)]
STAGES = {"zoo": [("milo", "milo", 960, 940, 1.1, False, False)], "canopy": TREE, "figtree": TREE, "blossom": TREE, "canopy_eve": TREE,
          "jungle": [("milo", "milo", 420, 470, .78, False, True)],
          "bigtree": [("mango", "monkey", 900, -536, .7)]}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920); INK = art.INK
MW = (960, 380, 1800)                       # the treetop, wide
MC = (MX, 290, 1000)                        # Mango, whole
MH = (MX, 262, 720)                         # Mango, close
QC = (MX, 170, 1300)                        # Mango low in the picture: room for the two answer signs above her
MP = WV("canopy", ["mango"], floor=.68, top=.42)                # 9:16: Mango whole, under the title and the signs
MPW = WV("canopy", ["mango"], hmin=1040, floor=.68, top=.42)    # 9:16: a little wider
MPQ = WV("canopy", ["mango"], floor=.70, top=.46)   # 9:16: a question with two answer signs: Mango lower, the signs clear of her hair
MPH = (MX, 270, 900)                        # 9:16: Mango close
WALKP = (950, 198, 1300)                     # 9:16: holds Mango while she walks from x = 700 to 1100
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 900))
HAND = {"r": (MX + 130, 283), "l": (MX - 130, 283)}      # where Mango's hand is when the arm is up


def ARM(side="r", at=0, deg=80):
    return ("to", at, "#{p}mango-a" + side, {"rotation": -deg if side == "r" else deg, "svgOrigin": ("58" if side == "r" else "-58") + " -206", "duration": .01 if at == 0 else .35}, "" if at == 0 else "Mango lifts her arm")


def HOLD(name="fr", fn=art2.fruit, side="r", s=.34, hidden=False): return prop(name, fn, *HAND[side], s, hidden)


def EAT(at, name="fr"): return ("to", at, "#{p}" + name + "_w", {"x": MX, "y": 286, "scale": .3, "opacity": 0, "transformOrigin": "50% 50%", "duration": .45, "ease": "power2.in"}, "Mango puts it in her mouth")


def MUNCH(at, who="mango", n=11): return ("to", at, "#{p}" + who + "-jaw", {"opacity": 1, "y": 12, "duration": .16, "yoyo": True, "repeat": n}, "Mango munches")


def hang(fn):
    """A fruit or a flower hanging on its twig from the leaves above."""
    return lambda p: f'<g id="{p}"><path d="M3 -100 C-8 -220 10 -330 0 -470" stroke="#6a4a26" stroke-width="13" fill="none" stroke-linecap="round"/>{fn(p + "h")}</g>'


GREEN = lambda hidden=False: prop("gf", hang(A.green_fruit), MX - 200, 262, .34, hidden)
GOLD = lambda hidden=False: prop("yf", hang(art2.fruit), MX + 200, 262, .34, hidden)
BOB = lambda at, name: ("to", at, "#{p}" + name + "_w", {"rotation": 9, "transformOrigin": "50% 0%", "duration": .25, "yoyo": True, "repeat": 5}, "the fruit swings")

# ------------------------------------------------------------------ the ten-bites board and the six-foods board
DX = [480, 720, 960, 1200, 1440]; DY = [400, 660]; DPX = [630, 795, 960, 1125, 1290]; DPY = [470, 660]
DCAM = (960, 520, 1560); DPCAM = (960, 480, 1700)


def dishes(shown, new=(), empty=True):
    """Ten plates, one for each bite: 0-7 are fruit, 8 and 9 are leaves and a flower. `shown` are there from the start, `new` pop in."""
    out = []
    for k in range(10):
        x, y = DX[k % 5], DY[k // 5]; p = (DPX[k % 5], DPY[k // 5], .78)
        if empty: out.append(prop(f"e{k}", A.empty_dish, x, y, 1.0, p=p))
        if k in shown or k in new: out.append(prop(f"d{k}", lambda q, k=k: A.dish(q, "fruit" if k < 8 else "leaves"), x, y, 1.0, k in new, p=p))
    return out


FOODS = ["FRUIT", "LEAVES", "FLOWERS", "SEEDS", "BARK", "BUGS"]
JX = [360, 600, 840, 1080, 1320, 1560]; JP = [(690, 520), (960, 520), (1230, 520), (690, 765), (960, 765), (1230, 765)]
JCAM = (960, 520, 1560); JPCAM = (960, 480, 1700)


def foods(shown, new=()): return [prop(f"j{k}", A.food(k), JX[k], 560, 1.0, k in new, p=(*JP[k], 1.0)) for k in range(6) if k in shown or k in new]


# ------------------------------------------------------------------ Mango's group
GS = .42
GX0 = [485, 675, 865, 1055, 1245, 1435]; GKIND = ["monkey_b", "monkey_c", "monkey_d", "monkey", "monkey_c", "monkey_b"]; GID = ["f1", "f2", "f3", "mango", "f4", "f5"]
GX1 = [285, 475, 665, 1255, 1445, 1635]


def group(xs=GX0, only=None): return [(GID[k], GKIND[k], xs[k], MY, GS) for k in range(6) if only is None or k in only]


GP = (1445, 248, 1150)       # 9:16: Mango's three after the big group splits
GPL = (475, 248, 1150)       # 9:16: the other three
P6 = (972, 96, 2100)       # 9:16: all six on the branch (the three treetop places of this episode have sky up to y = -1900)
G3 = (1445, 300, 900); G3P = GP
GALL = (960, 330, 1600); GALL2 = (960, 330, 1690)      # the group shots only pull out: with the default slow push-in the outer monkeys were cut by the frame in the first render

SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("figtree", MC, "What does a monkey eat all day?", q=True, tag="hook: what does she eat", hide=["milo"], pcam=MP, props=[HOLD()],
      fx=[ARM(), ("face", 0.05, "mango", "wow")], words=[("w:eat", "?", .82, .3, 3.0, "sun", (.8, .36), 1.5)]),
    S("paper_pink", (960, 540, 1500), "Fruit? Leaves? Or little bugs?", tag="hook: guesses", pcam=(960, 480, 1700),
      props=[prop("a", A.food(0), 600, 560, 1.3, True, p=(690, 640, 1.1)), prop("b", A.food(1), 960, 560, 1.3, True, p=(960, 640, 1.1)), prop("c", A.food(5), 1320, 560, 1.3, True, p=(1230, 640, 1.1))],
      fx=[("show", "w:Fruit?", "a"), ("show", "w:Leaves?", "b"), ("show", "w:bugs?", "c")], words=[("e:bugs?", "?", .5, .14, 1.8, "sun", (.5, .33), 1.5)]),
    S("figtree", say="I'm Milo. Let's find out together!", tag="hook: Milo", hide=["mango"], fx=[("hop", "w:find", "milo")], **MILO("canopy")),
    # ---------------------------------------------------------------- INTRO
    S("zoo", WIDE, "Welcome to The Animated Zoo, friends!", trans="iris", tag="gate wide", words=[("w:Animated", "HELLO!", .74, .6, 1.2, "pill")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, -40), "Today we fly up to the rainforest treetops.", tag="Milo close", words=[("w:treetops.", "THE TREETOPS", .5, .16, 1.1, "sun")]),
    S("canopy", MW, "Here we are! Look who is waking up.", trans="iris", tag="treetops wide", cam2=(980, 370, 1700), pcam=MPW, pcam2=MPW,
      fx=[("fromto", 0, "#{p}milo_w", {"x": -300, "y": 520}, {"x": 420, "y": 300, "duration": 1.3, "ease": "power2.out"}, "Milo flies in")]),
    S("canopy", MC, "This is Mango. Mango is a spider monkey.", tag="this is Mango", hide=["milo"], pcam=MP, words=[("w:Mango.", "MANGO", .2, .3, 1.1, "pill", (.5, .33))],
      fx=[("hop", "w:Mango.", "mango"), ("arm", "w:spider", "mango", "r", -60)]),
    # ---------------------------------------------------------------- PART 1: breakfast - fruit comes first
    S("canopy", MH, "Good morning, Mango! Her tummy goes rumble, rumble.", part=1, tag="rumble", hide=["milo"], pcam=MP,
      fx=[("to", "w:rumble,", "#{p}mango-body", {"scaleX": 1.05, "svgOrigin": "0 -150", "duration": .12, "yoyo": True, "repeat": 9}, "Mango's tummy rumbles")],
      words=[("w:rumble,", "RUMBLE!", .82, .34, 1.0, "sun", (.5, .33), .9)]),
    S("canopy", say="It is breakfast time! What do you eat for breakfast?", part=1, q=True, tag="your breakfast", hide=["mango"], pause=.8, fx=[("hop", "w:What", "milo")],
      words=[("w:breakfast", "BREAKFAST!", .74, .2, .9, "sun", (.5, .33), .85)], **MILO("canopy")),
    S("figtree", MW, "Mango walks along the branch, to a tree full of fruit.", part=1, trans="iris", tag="to the fruit tree", cam2=(980, 370, 1700), pcam=WALKP, pcam2=WALKP,
      hide=["milo"], move={"mango": (700, MY, MS)}, fx=[("walk", 0.1, "mango", 400, 3.0)], words=[("w:fruit.", "FRUIT!", .8, .56, 1.3, "sun", (.5, .33))]),
    S("paper", (960, 520, 1500), "A spider monkey looks for fruit during the day.", part=1, tag="board: in the day", pcam=(900, 480, 1700),
      actors=[("mango", "monkey", 720, 790, .85)], props=[prop("fr", art2.fruit, 720 + 178, 790 - 204, .46), prop("sun", A.sun_small, 1240, 380, 1.0, True)],
      fx=[ARM(), ("show", "w:during", "sun"), ("to", "w:during", "#{p}sun-rays", {"rotation": 90, "transformOrigin": "50% 50%", "duration": 3, "ease": "none"}, "")],
      words=[("w:day.", "IN THE DAY", .7, .66, .9, "pill", (.5, .33), .85)]),
    S("paper", (960, 540, 1300), "Fruit is the main part of what it eats.", part=1, tag="board: main food", pcam=(960, 440, 1500), props=[prop("fr", art2.fruit, 960, 640, 2.0)],
      fx=[("to", "w:main", "#{p}fr_w", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .3, "yoyo": True, "repeat": 5}, "the fruit pulses")],
      words=[("w:main", "NUMBER 1", .5, .17, 1.2, "sun", (.5, .33), 1.0)]),
    S("figtree", MC, "Look! This fruit is green. And this fruit is golden.", part=1, tag="green and golden", hide=["milo"], pcam=MPW, pcam2=MPW, props=[GREEN(), GOLD()],
      fx=[BOB("w:green.", "gf"), BOB("w:golden.", "yf")],
      words=[("w:green.", "GREEN", .2, .34, 1.0, "", (.24, .34), .6), ("w:golden.", "GOLDEN", .8, .34, 1.0, "sun", (.76, .34), .6)]),
    S("figtree", MH, "Mango looks, and looks, with her big brown eyes.", part=1, tag="she looks", hide=["milo"], pcam=MPW, pcam2=MPW, props=[GREEN(), GOLD()],
      fx=[("face", "w:looks,", "mango", "wow"), ("face", "w:big", "mango", "wow")], words=[("w:looks,", "LOOK!", .82, .3, 1.0, "sun", (.5, .33), .8)]),
    S("paper_blue", (960, 520, 1500), "Spider monkeys see colors very well.", part=1, tag="board: colors", pcam=(960, 480, 1700),
      props=[prop("c0", lambda p: A.swatch(p, "#e63946"), 600, 600, 1.2, True, p=(660, 620, 1.0)), prop("c1", lambda p: A.swatch(p, "#ffd23f"), 840, 600, 1.2, True, p=(860, 620, 1.0)),
             prop("c2", lambda p: A.swatch(p, "#4fb56c"), 1080, 600, 1.2, True, p=(1060, 620, 1.0)), prop("c3", lambda p: A.swatch(p, "#2f80ed"), 1320, 600, 1.2, True, p=(1260, 620, 1.0))],
      fx=[("show", "w:Spider", "c0"), ("show", "w:see", "c1"), ("show", "w:colors", "c2"), ("show", "w:well.", "c3")], words=[("w:colors", "COLORS", .5, .2, 1.3, "sun", (.5, .33))]),
    S("paper_blue", (960, 520, 1500), "That helps them pick the best fruit.", part=1, tag="board: the best fruit", pcam=(960, 480, 1700),
      props=[prop("g", A.green_fruit, 720, 660, 1.5, p=(760, 680, 1.3)), prop("y", art2.fruit, 1200, 660, 1.5, p=(1160, 680, 1.3)), prop("ok", art.tick, 1340, 500, 1.0, True, p=(1290, 530, .9))],
      fx=[("show", "w:best", "ok")], words=[("w:best", "THE BEST!", .5, .17, 1.2, "sun", (.5, .33), .95)]),
    S("figtree", say="What color is your favorite fruit?", part=1, q=True, tag="your fruit", hide=["mango"], pause=1.0, fx=[("hop", "w:favorite", "milo")],
      words=[("w:color", "WHAT COLOR?", .74, .2, .85, "sun", (.5, .33), .8)], **MILO("canopy")),
    S("figtree", QC, "Which fruit will Mango pick? The green one, or the golden one?", part=1, q=True, tag="question 1", pause=3.2, hide=["milo"], pcam=MPQ, pcam2=MPQ, props=[GREEN(), GOLD()],
      fx=[("signs", "w:green", ["GREEN", "GOLDEN"], 1, "wait:2.0"), ("to", "wait:2.05", "#{p}mango-ar", {"rotation": -88, "svgOrigin": "58 -206", "duration": .35}, "Mango reaches for the golden fruit")]),
    S("figtree", MC, "The golden one! Good choice, Mango.", part=1, tag="the golden one", hide=["milo"], pcam=MPW, pcam2=MPW, props=[GREEN(), HOLD()],
      fx=[ARM(), ("hop", "w:Good", "mango"), ("face", 0.05, "mango", "happy")], words=[("w:golden", "GOLDEN!", .8, .34, 1.1, "sun", (.5, .33), .9)]),
    S("figtree", (MX - 100, 262, 760), "The green fruit can wait for another day.", part=1, tag="not yet", hide=["milo"], pcam=MPW, pcam2=MPW, props=[GREEN(), HOLD()],
      fx=[ARM(), BOB("w:green", "gf")], words=[("w:wait", "NOT YET", .2, .3, 1.0, "pill", (.3, .33), .7)]),
    S("figtree", MH, "Munch, munch, munch! Can you munch like Mango?", part=1, q=True, tag="munch", hide=["milo"], pcam=MPH, props=[HOLD()],
      fx=[ARM(), EAT(0.15), ("arm", 0.7, "mango", "r", 0), MUNCH("w:Munch,", n=15)], words=[("w:Munch,", "MUNCH!", .82, .3, 1.0, "sun", (.5, .33), .8)]),
    S("paper_pink", DCAM, "Imagine Mango takes ten bites.", part=1, tag="board: ten bites", pcam=DPCAM, props=dishes(()),
      words=[("w:ten", "10 BITES", .5, .12, 1.1, "sun", (.5, .33), .95)]),
    S("paper_pink", DCAM, "How many bites are fruit? Let's count!", part=1, q=True, tag="board: how many", pcam=DPCAM, props=dishes(()),
      words=[("w:How", "HOW MANY?", .5, .12, 1.1, "", (.5, .33), .95)]),
    S("paper_pink", DCAM, "One, two, three, four,", part=1, tag="board: count 1-4", pcam=DPCAM, props=dishes((), (0, 1, 2, 3)),
      fx=[("show", "w:One,", "d0"), ("show", "w:two,", "d1"), ("show", "w:three,", "d2"), ("show", "w:four,", "d3")]),
    S("paper_pink", DCAM, "five, six, seven, eight!", part=1, tag="board: count 5-8", pcam=DPCAM, props=dishes((0, 1, 2, 3), (4, 5, 6, 7)),
      fx=[("show", "w:five,", "d4"), ("show", "w:six,", "d5"), ("show", "w:seven,", "d6"), ("show", "w:eight!", "d7")], words=[("e:eight!", "8", .5, .13, 1.3, "sun", (.5, .33), 1.3)]),
    S("paper_pink", DCAM, "About eight bites out of ten are fruit!", part=1, tag="board: eight of ten", pcam=DPCAM, props=dishes(range(8)),
      words=[("w:eight", "8 OUT OF 10", .5, .12, 1.1, "sun", (.5, .33), .95)]),
    S("paper_pink", DCAM, "And the last two? Some young leaves and flowers.", part=1, tag="board: the last two", pcam=DPCAM, props=dishes(range(8), (8, 9)),
      fx=[("show", "w:young", "d8"), ("show", "w:flowers.", "d9")], words=[("w:two?", "+ 2", .5, .13, 1.3, "", (.5, .33), 1.1)]),
    S("paper_pink", DCAM, "Fruit, fruit, fruit, and more fruit!", part=1, tag="board: so much fruit", pcam=DPCAM, props=dishes(range(10)),
      fx=[("to", "w:Fruit,", "#{p}d0_w,#{p}d1_w,#{p}d2_w,#{p}d3_w", {"y": "-=22", "duration": .2, "yoyo": True, "repeat": 3}, "the fruit plates bob"),
          ("to", "w:more", "#{p}d4_w,#{p}d5_w,#{p}d6_w,#{p}d7_w", {"y": "-=22", "duration": .2, "yoyo": True, "repeat": 3}, "more fruit plates bob")],
      words=[("w:more", "SO MUCH FRUIT!", .5, .12, 1.0, "sun", (.5, .33), .8)]),
    S("figtree", MC, "So for a spider monkey, fruit comes first.", part=1, tag="fruit first", hide=["milo"], pcam=MP, props=[HOLD()],
      fx=[ARM(), ("hop", "w:fruit", "mango"), ("face", 0.05, "mango", "happy")], words=[("w:fruit", "FRUIT FIRST!", .25, .28, .78, "pill", (.5, .33), .8)]),
    S("figtree", say="Do you like fruit, too? Rub your tummy!", part=1, q=True, tag="rub your tummy", hide=["mango"], fx=[("hop", "w:Rub", "milo", 2)],
      words=[("w:Rub", "YUM!", .76, .22, 1.2, "sun", (.5, .33))], **MILO("canopy")),
    S("paper_pink", JCAM, "That is food number one. Fruit!", part=1, tag="board: food 1", pcam=JPCAM, props=foods((), (0,)), fx=[("show", "w:one.", "j0")],
      words=[("w:one.", "1", .115, .22, 1.5, "sun", (.22, .4), 1.1)]),
    # ---------------------------------------------------------------- PART 2: lunch - the other foods, and a small group
    S("blossom", MW, "Lunchtime! But look. This tree has no fruit at all.", part=2, trans="iris", tag="the flower tree", cam2=(980, 370, 1700), pcam=WALKP, pcam2=WALKP,
      hide=["milo"], move={"mango": (700, MY, MS)}, fx=[("walk", 0.1, "mango", 400, 2.6)], words=[("w:no", "NO FRUIT!", .8, .56, 1.1, "", (.5, .33), .9)]),
    S("blossom", MH, "Hmm. What can Mango eat now?", part=2, q=True, tag="what now", hide=["milo"], pcam=MPH, pause=1.3, fx=[("face", 0.05, "mango", "wow")],
      words=[("w:What", "?", .82, .3, 2.6, "sun", (.8, .36), 1.3)]),
    S("paper", (960, 520, 1500), "When there is no fruit, spider monkeys eat other things.", part=2, tag="board: other things", pcam=(960, 480, 1700),
      props=[prop("fr", art2.fruit, 700, 660, 1.4, p=(740, 680, 1.2)), prop("x", crossx, 700, 640, 1.1, True, p=(740, 660, 1.0)), prop("fl", A.flower, 1090, 500, 1.1, True, p=(1090, 520, 1.0)),
             prop("lv", A.leaves, 1340, 730, 1.2, True, p=(1290, 780, 1.1))],
      fx=[("show", "w:no", "x"), ("show", "w:other", "fl"), ("show", "w:things.", "lv")], words=[("w:other", "OTHER FOOD", .5, .14, 1.1, "sun", (.5, .33), .9)]),
    S("blossom", MC, "Look, flowers! Mango picks a pink flower.", part=2, tag="a flower", hide=["milo"], pcam=MPW, pcam2=MPW, props=[prop("fl", hang(A.flower), MX + 170, 268, .3)],
      fx=[BOB("w:flowers!", "fl"), ARM("r", "w:picks", 86)], words=[("w:flowers!", "FLOWERS", .22, .32, .85, "sun", (.5, .33), .85)]),
    S("blossom", MH, "Nibble, nibble, nibble. Flowers are food, too!", part=2, tag="nibble", hide=["milo"], pcam=MPH, props=[HOLD("fl", A.flower, "r", .3)],
      fx=[ARM(), EAT(0.15, "fl"), ("arm", 0.7, "mango", "r", 0), MUNCH("w:Nibble,", n=13), ("face", "w:Flowers", "mango", "happy")], words=[("w:Nibble,", "NIBBLE!", .82, .3, 1.0, "sun", (.5, .33), .8)]),
    S("blossom", QC, "Does a spider monkey eat leaves, too? Yes, or no?", part=2, q=True, tag="question 2", pause=3.2, hide=["milo"], pcam=MPQ, pcam2=MPQ, props=[HOLD("lf", A.leaf1, "l", .5)],
      fx=[ARM("l"), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0"), ("hop", "wait:2.05", "mango")]),
    S("blossom", MH, "Yes! Mango munches a soft, young leaf.", part=2, tag="a leaf", hide=["milo"], pcam=MPH, props=[HOLD("lf", A.leaf1, "l", .5)],
      fx=[ARM("l"), EAT("w:munches", "lf"), ("arm", "w:soft,", "mango", "l", 0), MUNCH("w:soft,", n=9)], words=[("w:Yes!", "YES!", .82, .3, 1.2, "sun", (.5, .33), .9)]),
    S("paper", (960, 540, 1300), "Young leaves are the new, soft ones.", part=2, tag="board: young leaves", pcam=(960, 440, 1500), props=[prop("lv", A.leaves, 960, 660, 2.2, p=(960, 680, 2.2))],
      fx=[("to", "w:new,", "#{p}lv_w", {"rotation": 6, "transformOrigin": "50% 100%", "duration": .3, "yoyo": True, "repeat": 5}, "the leaves sway")],
      words=[("w:new,", "NEW", .22, .36, 1.2, "sun", (.27, .33), .9), ("w:soft", "SOFT", .78, .36, 1.2, "", (.73, .33), .9)]),
    S("blossom", say="Chomp, chomp! Can you chomp like Mango?", part=2, q=True, tag="chomp", hide=["mango"], fx=[("hop", "w:Chomp,", "milo", 2)],
      words=[("w:Chomp,", "CHOMP!", .76, .22, 1.0, "sun", (.5, .33))], **MILO("canopy")),
    S("paper", (960, 520, 1500), "Spider monkeys eat seeds, too. And even bark!", part=2, tag="board: seeds and bark", pcam=(960, 480, 1700),
      props=[prop("s0", art2.seed, 620, 480, 1.5, True, p=(680, 540, 1.3)), prop("s1", art2.seed, 760, 580, 1.5, True, p=(800, 640, 1.3)), prop("s2", art2.seed, 640, 690, 1.5, True, p=(700, 750, 1.3)),
             prop("tr", A.trunk_piece, 1240, 600, .72, True, p=(1200, 660, .72))],
      fx=[("show", "w:seeds,", "s0"), ("show", "w:seeds,", "s1", None, False), ("show", "w:seeds,", "s2", None, False), ("show", "w:bark!", "tr")],
      words=[("w:seeds,", "SEEDS", .3, .16, 1.1, "sun", (.3, .33), .7), ("w:bark!", "BARK", .69, .16, 1.0, "", (.75, .33), .8)]),
    S("paper", (1100, 580, 1100), "Bark is the skin of a tree.", part=2, tag="board: bark", pcam=(1090, 480, 1500),
      props=[prop("tr", A.trunk_piece, 1240, 600, .72, p=(1200, 660, .72)), prop("bk", A.bark, 1240, 600, .8, p=(1200, 660, .8)), prop("ar", lambda p: art.arrow(p, 860, 480, 980, 560), 0, 0, 1, True, p=(-40, 60, 1))],
      fx=[("to", "w:skin", "#{p}bk_w", {"x": "-=250", "rotation": -14, "duration": .7, "ease": "power2.out"}, "a piece of bark comes off"), ("show", "w:skin", "ar")],
      words=[("w:skin", "TREE SKIN", .3, .2, 1.0, "pill", (.5, .33), .85)]),
    S("blossom", (1240, 330, 760), "And what is that, on the branch? A tiny bug!", part=2, q=True, tag="a bug", hide=["milo"], pcam=(1215, 270, 900),
      props=[prop("bug", lambda p: f'<g transform="scale(-1 1)">{A.bug(p)}</g>', 1500, 416, .3), prop("ar", lambda p: art.arrow(p, 1400, 250, 1340, 380), 0, 0, 1, True)],
      fx=[("to", 0.1, "#{p}bug_w", {"x": 1330, "duration": 2.4, "ease": "none"}, "a bug walks along the branch"), ("show", "w:tiny", "ar"), ("face", "w:tiny", "mango", "wow")],
      words=[("w:bug!", "A BUG!", .78, .2, 1.0, "sun", (.66, .34), .8)]),
    S("paper_blue", (960, 540, 1300), "Spider monkeys eat small insects, too.", part=2, tag="board: insects", pcam=(960, 440, 1500), props=[prop("bug", A.bug, 960, 640, 3.0, p=(960, 660, 2.6))],
      fx=[("to", 0.1, "#{p}bug_w", {"rotation": 5, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 15}, "the bug wiggles")],
      words=[("w:insects,", "INSECTS", .5, .17, 1.2, "sun", (.5, .33), 1.0)]),
    S("blossom", say="Would you eat a bug? Mango would!", part=2, q=True, tag="would you", hide=["mango"], fx=[("hop", "w:Mango", "milo")],
      words=[("w:bug?", "A BUG?!", .76, .22, 1.1, "sun", (.5, .33))], **MILO("canopy")),
    S("paper_pink", JCAM, "Let's fill Mango's menu. Fruit, leaves, flowers,", part=2, tag="board: menu 1", pcam=JPCAM, props=foods((0,), (1, 2)),
      fx=[("show", "w:leaves,", "j1"), ("show", "w:flowers,", "j2")], words=[("w:menu.", "MENU", .5, .14, 1.2, "pill", (.5, .33), 1.0)]),
    S("paper_pink", JCAM, "seeds, bark, and bugs. Six foods!", part=2, tag="board: menu 2", pcam=JPCAM, props=foods((0, 1, 2), (3, 4, 5)),
      fx=[("show", "w:seeds,", "j3"), ("show", "w:bark,", "j4"), ("show", "w:bugs.", "j5")], words=[("w:Six", "6 FOODS", .5, .14, 1.3, "sun", (.5, .33), 1.0)]),
    S("blossom", MC, "What a big menu for one little monkey!", part=2, tag="big menu", hide=["milo"], pcam=MP, fx=[("hop", "w:big", "mango"), ("face", 0.05, "mango", "happy"), ("arm", "w:one", "mango", "r", -60)],
      words=[("w:big", "BIG MENU!", .2, .3, 1.0, "sun", (.5, .33), .9)]),
    S("blossom", GALL, "And Mango does not look for food alone.", part=2, tag="not alone", cam2=GALL2, hide=["milo"], actors=group(), pcam=P6, pcam2=P6,
      fx=[("hop", "w:alone.", "f4"), ("hop", "w:alone.", "f5")], words=[("w:alone.", "FRIENDS!", .5, .13, 1.1, "sun", (.5, .33), .9)]),
    S("blossom", GALL, "Spider monkeys live in a big group.", part=2, tag="a big group", cam2=GALL2, actors=group(), pcam=P6, pcam2=P6,
      fx=[("hop", "w:big", "f1"), ("hop", "w:big", "f3"), ("hop", "w:big", "mango")], words=[("w:big", "BIG GROUP", .5, .13, 1.1, "pill", (.5, .33), .9)]),
    S("blossom", GALL, "To find food, the big group splits into smaller groups.", part=2, tag="smaller groups", cam2=GALL2, actors=group(), pcam=P6, pcam2=GP,
      fx=[("walk", "w:splits", k, -200 if n < 3 else 200, 1.8) for n, k in enumerate(GID)], words=[("w:smaller", "SMALLER GROUPS", .5, .13, .9, "sun", (.9, .487), .38)]),
    S("blossom", GALL, "Three here, and three over there.", part=2, tag="three and three", cam2=GALL2, actors=group(GX1), pcam=GPL, pcam2=GP,
      fx=[("hop", "w:here,", "f1"), ("hop", "w:here,", "f2"), ("hop", "w:here,", "f3"), ("hop", "w:there.", "mango"), ("hop", "w:there.", "f4"), ("hop", "w:there.", "f5")],
      words=[("w:here,", "3", .197, .14, 1.6, "sun", (.5, .33), 1.2), ("w:there.", "3", .803, .14, 1.6, "sun", (2.0, .33), 1.2)]),
    S("blossom", G3, "Count Mango's little group with me. One, two, three!", part=2, q=True, tag="count the group", actors=group(GX1, (3, 4, 5)), pcam=G3P, pcam2=G3P,
      fx=[("hop", "w:One,", "mango"), ("hop", "w:two,", "f4"), ("hop", "w:three!", "f5")],
      words=[("w:One,", "1", .289, .14, 1.6, "sun", (.21, .36), 1.1), ("w:two,", "2", .5, .14, 1.6, "sun", (.5, .36), 1.1), ("w:three!", "3", .711, .14, 1.6, "sun", (.79, .36), 1.1)]),
    S("blossom", say="Who do you eat lunch with?", part=2, q=True, tag="your lunch", hide=["mango"], pause=1.5, fx=[("hop", "w:Who", "milo")],
      words=[("w:lunch", "WHO?", .76, .22, 1.2, "sun", (.5, .33))], **MILO("canopy")),
    # ---------------------------------------------------------------- PART 3: dinner - the seeds travel
    S("figtree", GALL, "In the afternoon, Mango's little group finds one more fruit tree.", part=3, trans="iris", tag="afternoon", cam2=GALL2, actors=group(GX1, (3, 4, 5)), pcam=G3P, pcam2=G3P,
      move={"mango": (GX1[3] - 300, MY, GS), "f4": (GX1[4] - 300, MY, GS), "f5": (GX1[5] - 300, MY, GS)},
      fx=[("walk", 0.1, k, 300, 2.6) for k in ("mango", "f4", "f5")], words=[("w:fruit", "MORE FRUIT!", .32, .2, 1.0, "sun", (.5, .33), .9)]),
    S("bigtree", (960, -60, 2860), "Spider monkeys spend most of the day high up in the treetops.", part=3, trans="iris", tag="high up", cam2=(980, -200, 2500), pcam=(950, -690, 2000), pcam2=(950, -700, 1800),
      props=[prop("ar", lambda p: art.arrow(p, 620, 500, 620, -400), 0, 0, 1, True)], fx=[("show", "w:high", "ar"), ("hop", "w:treetops.", "mango")],
      words=[("w:high", "UP HIGH", .24, .5, .8, "sun", (.5, .33), .9)]),
    S("figtree", MC, "They climb, and they look for food.", part=3, tag="looking for food", hide=["milo"], pcam=MPW, pcam2=MPW, move={"mango": (MX - 160, MY, MS)},
      fx=[("walk", 0.1, "mango", 160, 1.6), ("face", "w:look", "mango", "wow")], words=[("w:look", "LOOK!", .82, .3, 1.0, "sun", (.5, .33), .9)]),
    S("figtree", say="Can you reach up high, like Mango? Stretch!", part=3, q=True, tag="stretch", hide=["mango"],
      fx=[("to", "w:Stretch!", "#{p}milo-body", {"scaleY": 1.14, "scaleX": .95, "svgOrigin": "0 0", "duration": .4, "yoyo": True, "repeat": 3}, "Milo stretches up")],
      words=[("w:Stretch!", "STRETCH!", .76, .22, 1.0, "sun", (.5, .33))], **MILO("canopy")),
    S("figtree", MC, "Dinner time! Mango picks one more golden fruit.", part=3, tag="dinner", hide=["milo"], pcam=MPW, pcam2=MPW, props=[GOLD()],
      fx=[BOB("w:Mango", "yf"), ARM("r", "w:picks", 88)], words=[("w:Dinner", "DINNER!", .2, .3, 1.0, "sun", (.5, .33), .9)]),
    S("figtree", MH, "Gulp! She swallows the fruit,", part=3, tag="gulp", hide=["milo"], pcam=MPH, props=[HOLD()],
      fx=[ARM(), EAT("w:Gulp!"), ("arm", "w:She", "mango", "r", 0), MUNCH("w:She", n=7)], words=[("w:Gulp!", "GULP!", .82, .3, 1.1, "sun", (.5, .33), .8)]),
    S("paper", (960, 540, 1300), "and the little seeds inside it, too.", part=3, tag="board: seeds inside", pcam=(960, 440, 1500), props=[prop("fo", A.fruit_open, 960, 640, 2.3, p=(960, 660, 2.1))],
      fx=[("to", "w:seeds", "#{p}fo-s0,#{p}fo-s1,#{p}fo-s2", {"scale": .68, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 5}, "the seeds light up")],
      words=[("w:seeds", "SEEDS", .5, .17, 1.2, "sun", (.5, .33), 1.0)]),
    S("figtree", say="Have you seen the seeds inside a fruit?", part=3, q=True, tag="your seeds", hide=["mango"], pause=.8, fx=[("hop", "w:seeds", "milo")],
      words=[("w:seeds", "SEEDS?", .76, .22, 1.1, "sun", (.5, .33))], **MILO("canopy")),
    S("figtree", (1300, 380, 1500), "Then off she goes. Far, far away!", part=3, tag="off she goes", hide=["milo"], pcam=(1150, 200, 1100), pcam2=(1650, 200, 1100),
      fx=[("walk", 0.1, "mango", 700, 3.4)], words=[("w:Far,", "FAR AWAY!", .3, .3, 1.1, "sun", (.5, .33), .9)]),
    S("canopy", (900, 380, 1700), "She walks from tree, to tree, to tree.", part=3, tag="tree to tree", hide=["milo"], move={"mango": (300, MY, MS)}, pcam=(500, 200, 1100), pcam2=(1250, 200, 1100),
      fx=[("walk", 0.1, "mango", 1100, 3.8), ("word", "w:tree,", "TREE", {"x": 390, "y": 533, "size": 104, "cls": "", "landscape_only": True}),
          ("word", "w:tree,:2", "TO TREE", {"x": 900, "y": 533, "size": 104, "cls": "", "landscape_only": True})], words=[("w:tree.", "TO TREE!", .8, .66, .9, "sun", (1.71, .33), .8)]),
    S("blossom", QC, "Where will the seeds land? Near the fruit tree, or far away?", part=3, q=True, tag="question 3", pause=3.2, hide=["milo"], pcam=MPQ, pcam2=MPQ,
      fx=[("signs", "w:Near", ["NEAR", "FAR"], 1, "wait:2.0"), ("hop", "wait:2.05", "mango")]),
    S("jungle", (960, 760, 1300), "Far away! Later, the seeds drop to the ground. Plop, plop, plop!", part=3, trans="iris", tag="plop", hide=["milo"], pcam=(960, 680, 1300),
      props=[prop("s0", art2.seed, 800, -200, .8), prop("s1", art2.seed, 960, -200, .8), prop("s2", art2.seed, 1120, -200, .8)],
      fx=[("to", "w:Plop,", "#{p}s0_w", {"y": 905, "duration": .5, "ease": "bounce.out"}, "a seed lands"), ("to", "w:plop,", "#{p}s1_w", {"y": 915, "duration": .5, "ease": "bounce.out"}, "a seed lands"),
          ("to", "w:plop!", "#{p}s2_w", {"y": 905, "duration": .5, "ease": "bounce.out"}, "a seed lands"), ("snd", "w:Plop,", "pop"), ("snd", "w:plop,", "pop"), ("snd", "w:plop!", "pop")],
      words=[("w:Far", "FAR!", .5, .2, 1.3, "sun", (.5, .33)), ("w:Plop,", "PLOP!", .8, .45, 1.1, "", (.5, .44), .9)]),
    S("paper_pink", (960, 560, 1560), "Spider monkeys spread seeds all around the rainforest.", part=3, tag="board: spread", pcam=(960, 480, 1700),
      props=[prop("fr", art2.fruit, 620, 580, 1.3, p=(680, 660, 1.1)), prop("a0", lambda p: art.arrow(p, 760, 500, 960, 400), 0, 0, 1, True, p=(20, 80, 1)), prop("a1", lambda p: art.arrow(p, 780, 580, 1040, 580), 0, 0, 1, True, p=(20, 80, 1)),
             prop("a2", lambda p: art.arrow(p, 760, 660, 960, 760), 0, 0, 1, True, p=(20, 80, 1)), prop("s0", art2.seed, 1060, 360, 1.3, True, p=(1070, 440, 1.2)), prop("s1", art2.seed, 1160, 580, 1.3, True, p=(1160, 660, 1.2)),
             prop("s2", art2.seed, 1060, 790, 1.3, True, p=(1070, 870, 1.2))],
      fx=[("show", "w:spread", "a0"), ("show", "w:spread", "s0", None, False), ("show", "w:all", "a1"), ("show", "w:all", "s1", None, False), ("show", "w:rainforest.", "a2"), ("show", "w:rainforest.", "s2", None, False)],
      words=[("w:spread", "SPREAD!", .5, .14, 1.2, "sun", (.5, .33), .95)]),
    S("paper_pink", (960, 560, 1560), "A seed here. A seed there. Seeds everywhere!", part=3, tag="board: everywhere", pcam=(960, 480, 1700),
      props=[prop("s0", art2.seed, 1060, 360, 1.3, p=(1070, 440, 1.2)), prop("s1", art2.seed, 1160, 580, 1.3, p=(1160, 660, 1.2)), prop("s2", art2.seed, 1060, 790, 1.3, p=(1070, 870, 1.2)),
             prop("s3", art2.seed, 640, 400, 1.3, True, p=(700, 480, 1.2)), prop("s4", art2.seed, 560, 640, 1.3, True, p=(640, 720, 1.2)), prop("s5", art2.seed, 760, 780, 1.3, True, p=(780, 880, 1.2)), prop("s6", art2.seed, 1380, 440, 1.3, True, p=(1320, 520, 1.2)),
             prop("s7", art2.seed, 1400, 730, 1.3, True, p=(1330, 800, 1.2)), prop("s8", art2.seed, 880, 560, 1.3, True, p=(900, 640, 1.2))],
      fx=[("to", "w:here.", "#{p}s0_w", {"y": "-=30", "duration": .2, "yoyo": True, "repeat": 1}, "a seed hops"), ("to", "w:there.", "#{p}s2_w", {"y": "-=30", "duration": .2, "yoyo": True, "repeat": 1}, "a seed hops"),
          ("show", "w:Seeds", "s3"), ("show", "w:Seeds", "s4", None, False), ("show", "w:Seeds", "s5", None, False), ("show", "w:everywhere!", "s6"), ("show", "w:everywhere!", "s7", None, False), ("show", "w:everywhere!", "s8", None, False)],
      words=[("w:everywhere!", "EVERYWHERE!", .5, .14, 1.1, "sun", (.5, .33), .85)]),
    S("jungle", (960, 800, 1100), "And in the ground, a seed can grow. Look, a baby tree!", part=3, tag="a baby tree", hide=["milo"], pcam=(960, 680, 1300),
      props=[prop("s1", art2.seed, 960, 915, .8), prop("sp", art2.sprout, 960, 925, 1.5, True)],
      fx=[("to", "w:Look,", "#{p}s1_w", {"opacity": 0, "duration": .2}, ""), ("show", "w:Look,", "sp")], words=[("w:baby", "A BABY TREE!", .5, .2, 1.0, "sun", (.5, .33), .9)]),
    S("jungle", (960, 760, 1300), "So Mango helps the rainforest grow.", part=3, tag="the forest grows", hide=["milo"], pcam=(960, 680, 1300),
      props=[prop("p0", art2.sprout, 700, 915, 1.2, True, p=(740, 915, .9)), prop("sp", art2.sprout, 960, 925, 1.5), prop("p2", art2.sprout, 1220, 915, 1.2, True, p=(1180, 915, .9)), prop("h", art2.heart, 960, 660, 1.3, True)],
      fx=[("show", "w:helps", "p0"), ("show", "w:rainforest", "p2"), ("show", "w:grow.", "h")], words=[("w:helps", "THANK YOU, MANGO!", .5, .12, .85, "pill", (.5, .33), .62)]),
    S("jungle", say="Can you grow like a little tree? Up, up, up!", part=3, q=True, tag="grow", fx=[("to", "w:Up,", "#{p}milo-body", {"scaleY": 1.16, "scaleX": .95, "svgOrigin": "0 0", "duration": .35, "yoyo": True, "repeat": 5}, "Milo grows tall")],
      words=[("w:Up,", "UP, UP, UP!", .76, .22, .9, "sun", (.5, .33), .85)], **MILO("jungle")),
    S("canopy_eve", GALL, "The sun goes down. The little groups come back.", part=3, trans="iris", tag="sunset", cam2=GALL2, actors=group(GX1), pcam=P6, pcam2=P6,
      fx=[("walk", 0.1, k, 200 if n < 3 else -200, 2.4) for n, k in enumerate(GID)], words=[("w:sun", "SUNSET", .5, .13, 1.1, "sun", (.5, .33), .9)]),
    S("canopy_eve", GALL, "At night, the big group is together again.", part=3, tag="together", cam2=GALL2, actors=group(), pcam=P6, pcam2=P6,
      props=[prop("h1", art2.heart, 770, 150, 1.0, True), prop("h2", art2.heart, 1150, 110, 1.3, True)],
      fx=[("show", "w:together", "h1"), ("show", "w:again.", "h2")], words=[("w:together", "TOGETHER", .5, .7, 1.1, "pill", (.5, .33), .9)]),
    S("canopy_eve", MH, "Mango's tummy is full. No more rumble!", part=3, tag="full", hide=["milo"], pcam=MPH, fx=[("face", 0.05, "mango", "happy"), ("arm", "w:full.", "mango", "l", 34)],
      words=[("w:full.", "FULL!", .82, .3, 1.2, "sun", (.5, .33), .9)]),
    S("canopy_eve", MC, "What a busy day of eating, Mango!", part=3, tag="busy day", hide=["milo"], pcam=MP, fx=[("face", 0.05, "mango", "sleepy"), ("hop", "w:Mango!", "mango")],
      words=[("w:busy", "BUSY DAY!", .23, .3, .85, "sun", (.5, .33), .9)]),
    S("canopy_eve", say="Fruit all day, and seeds on the way. Wow!", part=3, tag="wow", hide=["mango"], fx=[("hop", "w:Wow!", "milo", 2)], words=[("w:Wow!", "WOW!", .76, .22, 1.3, "sun", (.5, .33))], **MILO("canopy")),
    # ---------------------------------------------------------------- QUIZ + RECAP
    S("canopy_eve", MW, "Time to remember what we learned!", part=4, tag="quiz time", cam2=(980, 370, 1700), pcam=MPW, words=[("w:remember", "QUIZ TIME!", .5, .62, 1.3, "sun", (.5, .33))]),
    S("canopy_eve", QC, "What does a spider monkey eat most? Fruit, or bark?", part=4, q=True, tag="quiz 1", pause=3.2, hide=["milo"], pcam=MP, fx=[("signs", "w:Fruit,", ["FRUIT", "BARK"], 0, "wait:2.0")]),
    S("paper_pink", DCAM, "Fruit! About eight bites out of ten.", part=4, tag="board: eight again", pcam=DPCAM, props=dishes(range(10), empty=False),
      words=[("w:Fruit!", "FRUIT!", .5, .12, 1.2, "sun", (.5, .33), .95)]),
    S("canopy_eve", QC, "Do spider monkeys eat flowers? Yes, or no?", part=4, q=True, tag="quiz 2", pause=3.2, hide=["milo"], pcam=MP, fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("paper_pink", JCAM, "Yes! And leaves, seeds, bark and bugs, too.", part=4, tag="board: menu again", pcam=JPCAM, props=foods((0, 1, 2, 3, 4, 5)),
      words=[("w:Yes!", "YES!", .5, .14, 1.3, "sun", (.5, .33), 1.0)]),
    S("paper", (960, 540, 1300), "What is hiding inside the fruit?", part=4, q=True, tag="quiz 3", pause=1.6, pcam=(960, 440, 1500), props=[prop("fr", art2.fruit, 960, 640, 2.0)],
      words=[("end+0.3", "?", .78, .3, 2.4, "sun", (.5, .33), 1.5)]),
    S("paper", (960, 540, 1300), "Seeds! Mango spreads them far away.", part=4, tag="board: seeds again", pcam=(960, 440, 1500), props=[prop("fo", A.fruit_open, 960, 640, 2.3, p=(960, 660, 2.1))],
      words=[("w:Seeds!", "SEEDS!", .5, .17, 1.2, "sun", (.5, .33), 1.0)]),
    S("canopy_eve", GALL, "Good night, Mango. Good night, friends.", part=4, tag="good night", cam2=GALL2, actors=group(), pcam=GP, props=[prop("h1", art2.heart, 960, 130, 1.2, True)],
      fx=[("show", "w:friends.", "h1")] + [("face", 0.05, k, "sleepy") for k in GID]),
    S("canopy_eve", MW, "Thank you for learning with me, friends. See you at the zoo!", part=4, tag="goodbye", cam2=(960, 380, 1900), pcam=MPW,
      words=[("w:See", "SEE YOU AT THE ZOO!", .5, .62, .95, "pill", (.5, .33), .62)], fx=[("hop", "w:zoo!", "milo", 2), ("arm", "w:See", "mango", "r", -70)]),
]
for _s in SHOTS:        # a picture board never drifts closer in 9:16 (a plate or a seed slid out of the frame in the first stills): it only pulls out a little
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)

SHORTS = [
    {"id": "zc_ep06_short1", "title": "How Does a Spider Monkey Pick the Best Fruit?", "band": ("WHICH FRUIT", "IS BEST?"), "thumb_text": "GREEN OR GOLDEN?", "part": 1,
     "extra_first": [S("figtree", MC, "Which fruit is the best one for Mango?", part=1, q=True, tag="hook: which fruit", hide=["milo"], pcam=MPW, pcam2=MPW, props=[GREEN(), GOLD()],
                       fx=[BOB(0.2, "gf"), BOB("w:best", "yf"), ("face", 0.05, "mango", "wow")], words=[("w:best", "?", .5, .1, 2.2, "sun", (.5, .33), 1.3)])]},
    {"id": "zc_ep06_short2", "title": "Do Spider Monkeys Eat Flowers and Bugs?", "band": ("DO MONKEYS", "EAT BUGS?"), "thumb_text": "LUNCH TIME!", "part": 2,
     "extra_first": [S("blossom", MC, "Do monkeys eat flowers? And bugs?", part=2, q=True, tag="hook: flowers and bugs", hide=["milo"], pcam=MP, props=[HOLD("fl", A.flower, "r", .3)],
                       fx=[ARM(), ("face", 0.05, "mango", "wow")], words=[("w:bugs?", "?", .2, .3, 2.6, "sun", (.22, .36), 1.4)])]},
    {"id": "zc_ep06_short3", "title": "How Do Spider Monkeys Help the Rainforest Grow?", "band": ("WHERE DO THE", "SEEDS GO?"), "thumb_text": "PLOP, PLOP!", "part": 3,
     "extra_first": [S("paper", (960, 540, 1300), "Where do the seeds in a fruit go?", part=3, q=True, tag="hook: where do seeds go", pcam=(960, 440, 1500), props=[prop("fo", A.fruit_open, 960, 640, 2.3, p=(960, 660, 2.1))],
                       fx=[("to", "w:seeds", "#{p}fo-s0,#{p}fo-s1,#{p}fo-s2", {"scale": .68, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 5}, "the seeds light up")],
                       words=[("w:go?", "?", .8, .3, 2.6, "sun", (.5, .33), 1.5)])]},
]

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
_UP = 'gsap.set("#P-ar",{rotation:-80,svgOrigin:"58 -206"});'
_UPL = 'gsap.set("#P-al",{rotation:80,svgOrigin:"-58 -206"});'
THUMBS = {
    "zc_ep06": {"place": "figtree", "cam": (960, 330, 1150), "actors": [("monkey", 760, 520, 1.15, False, _UP)],
                "props": [(art2.fruit, 760 + 242, 520 - 276, .64), (A.leaf1, 1450, 330, .9), (A.flower, 1300, 250, .5)],
                "words": [("YUM,", 1420, 640, 190, ""), ("FRUIT!", 1420, 840, 230, "sun")]},
    "zc_ep06_short1": {"place": "figtree", "cam": (MX, 200, 900), "actors": [("monkey", MX, MY, MS, False, "")],
                       "props": [(hang(A.green_fruit), MX - 200, 262, .34), (hang(art2.fruit), MX + 200, 262, .34)],
                       "words": [("GREEN", 540, 300, 180, ""), ("OR", 540, 455, 120, ""), ("GOLDEN?", 540, 610, 180, "sun")]},
    "zc_ep06_short2": {"place": "blossom", "cam": (MX, 230, 800), "actors": [("monkey", MX, MY, MS, False, _UP)],
                       "props": [(A.flower, MX + 130, 283, .3)],
                       "words": [("LUNCH", 540, 420, 190, ""), ("TIME!", 540, 610, 210, "sun")]},
    "zc_ep06_short3": {"place": "jungle", "cam": (960, 560, 1300), "actors": [],
                       "props": [(art2.seed, 800, 905, .8), (art2.sprout, 960, 925, 1.5), (art2.seed, 1120, 600, .8), (art2.seed, 1150, 905, .8)],
                       "words": [("PLOP,", 540, 440, 190, ""), ("PLOP!", 540, 640, 210, "sun")]},
}
