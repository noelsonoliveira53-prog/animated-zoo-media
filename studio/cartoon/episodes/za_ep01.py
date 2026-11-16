"""za_ep01 - TEST adventure episode (cartoon style, not for upload until Noelson approves the format).
Milo's Zoo Adventures: "A Birthday Surprise for Mama". A baby and his mama (Where Is My Mama?), a goal, three obstacles,
a low moment, a solution the characters find themselves, a warm ending. No one is in danger, lost or crying.

FACTS in the plot, read at the source on Nov 16 2026:
 [WWF] wwf.org.uk, "Unforgettable elephant facts": the trunk "can be used as a snorkel when an elephant wades in deep water."
 [NGK] National Geographic Kids, spider monkey: "has a prehensile tail, which means it can grasp and can be used like a fifth limb";
       "they hang upside down from their tails"; "searches for fruit, which makes up the main part of its diet."
 [SDZ] San Diego Zoo, camel: "Their large, broad feet ... expand when stepped on and contract when lifted to simplify walking in sand or snow."
 Shown, not stated as a fact card - [SDZ] elephant: "Elephants eat all types of vegetation, from grass and fruit to leaves";
       a trunk "is also used in caressing"; "so agile that it can pick up a single piece of straw"; "Elephants often spray themselves with water".
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2
from toon import shot

EP = {"id": "za_ep01", "kind": "story", "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "tumble": {"voice": "am_puck", "speed": .85, "pitch": 5, "formant": 1.16, "gain": .66},
               "mango": {"voice": "af_bella", "speed": .95, "pitch": 2, "formant": 1.08, "gain": .95}, "sandy": {"voice": "af_sarah", "speed": .82, "pitch": 3, "formant": 1.1, "gain": .88},
               "mama": {"voice": "bf_emma", "speed": .8, "gain": .8}},      # gain: each voice measured against Milo's lines (RMS) on Nov 16
      "title": "Baby Elephant's Birthday Surprise for Mama", "thumb_text": "BEST GIFT EVER!",
      "series": "Milo's Zoo Adventures",
      "description": ("It is Mama Elephant's birthday, and little Tumble has no present! Tumble and Milo the bluebird set off to find the golden fruit at the top of the "
                      "tallest tree. A wide river, a tall tree and a big sandy hill are in the way, and new friends Mango the spider monkey and Sandy the baby camel help. "
                      "A gentle animal adventure for ages 2-6 about kindness, courage and friendship, with a song to sing along.\n"
                      "Kids see how an elephant can use its trunk like a snorkel, how a spider monkey holds on with its tail, and why a camel's wide feet do not sink in sand.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nWWF (elephants); National Geographic Kids (spider monkey); San Diego Zoo Wildlife Alliance (camel, elephant)."),
      "tags": ["baby elephant", "elephant story for kids", "animal stories for kids", "bedtime story animals", "kids adventure cartoon", "spider monkey", "baby camel",
               "friendship story for kids", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "zoo": [("mama", "elephant_hat", 1400, 930, .92), ("tumble", "tumble", 640, 936, .6), ("milo", "milo", 250, 500, .78, False, True)],
    "savanna": [("tumble", "tumble", 980, 930, .62), ("milo", "milo", 470, 500, .8, False, True)],
    "river": [("tumble", "tumble", 760, 800, .5), ("milo", "milo", 360, 430, .7, False, True)],
    "jungle": [("tumble", "tumble", 860, 930, .62), ("milo", "milo", 400, 480, .78, False, True)],
    "bigtree": [("tumble", "tumble", 940, 930, .62), ("milo", "milo", 500, 440, .75, False, True)],
    "canopy": [("mango", "monkey_hang", 780, 462, .6)],
    "dune_eve": [("mango", "monkey", 300, 934, .58), ("tumble", "tumble", 700, 930, .62), ("sandy", "calf", 1480, 935, .56, True), ("milo", "milo", 200, 400, .7, False, True)],
    "zoo_eve": [("mango", "monkey", 230, 940, .55), ("sandy", "calf", 560, 940, .5), ("tumble", "tumble", 860, 940, .6), ("mama", "elephant_hat", 1600, 932, .9, True),
                ("milo", "milo", 720, 400, .68, False, True)],
}
PT = {"milo": {"head": (0, -185), "body": (0, -150), "top": (0, -360), "feet": (0, 0)},
      "tumble": {"head": (320, -430), "eye": (382, -449), "body": (-14, -290), "top": (320, -620), "trunk": (500, -250), "feet": (0, 0), "all": (90, -330)},
      "elephant": {"head": (300, -470), "eye": (352, -486), "body": (-14, -340), "top": (300, -640), "trunk": (470, -250), "feet": (0, 0), "all": (80, -360)},
      "monkey": {"head": (0, -296), "body": (0, -150), "top": (0, -410), "feet": (0, 0), "all": (0, -200)},
      "monkey_hang": {"head": (0, 446), "body": (0, 300), "top": (0, 0), "feet": (0, 560), "all": (0, 290)},
      "calf": {"head": (379, -690), "body": (0, -353), "top": (379, -760), "feet": (0, 0), "all": (90, -400), "back": (0, -470)}}
PT["elephant_hat"] = PT["elephant"]


def P(place, who, part="head", dx=0, dy=0, stage=None):
    a = next(a for a in (stage or STAGES[place]) if a[0] == who); kind, x, y, s = a[1], a[2], a[3], a[4]; flip = len(a) > 5 and a[5]; lx, ly = PT[kind][part]
    return round(x + (-lx if flip else lx) * s + dx), round(y + ly * s + dy)


def C(place, who, part, w, dx=0, dy=0, stage=None): return (*P(place, who, part, dx, dy, stage), w)


WIDE = (960, 540, 1920)


def S(place, cam, say="", who="milo", words=(), fx=(), **kw):
    out = list(fx)
    for w in words:
        at, text, fx_, fy_ = w[:4]; k = w[4] if len(w) > 4 else 1.0; cls = w[5] if len(w) > 5 else ""
        cx, cy, cw = cam; out.append(("word", at, text, {"x": round(cx + (fx_ - .5) * cw), "y": round(cy + (fy_ - .5) * cw * 9 / 16), "size": round(cw * .068 * k), "cls": cls}))
    return shot(place, cam, say, fx=out, who=who, **kw)


def prop(name, fn, x, y, s=1.0, hidden=False): return (name, fn, x, y, s, "hidden" if hidden else "", None)


REFRAIN = {"bpm": 108, "chords": "C G F C", "outro_bars": 0}
SING_GO = dict(REFRAIN, lines=[{"text": "Friends help friends, come along with me!", "notes": "C4:1 E4:1 G4:1 G4:.5 A4:.5,G4:.5 E4:.5 D4:2", "rest": 1},
                               {"text": "Step by step, what will we see?", "notes": "F4:1 F4:1 E4:1 D4:.5 D4:.5 E4:1 C4:2", "rest": 1}])
SING_HOME = dict(REFRAIN, lines=[{"text": "Friends help friends, come along with me!", "notes": "C4:1 E4:1 G4:1 G4:.5 A4:.5,G4:.5 E4:.5 D4:2", "rest": 1},
                                 {"text": "Home we go, as happy as can be!", "notes": "F4:1 F4:1 E4:1 D4:.5 D4:.5 E4:.5 E4:.5 C4:2", "rest": 1}])
# the ending song line, in two shots (one long wide shot was 8.8 s without a visual change in the finished file: over the 8 s gate)
SING_END_A = dict(REFRAIN, chords="C G", lines=[{"text": "Friends help friends, hooray, hooray!", "notes": "C4:1 E4:1 G4:1 G4:.5,A4:.5 G4:.5,E4:1.5", "rest": 2}])
SING_END_B = dict(REFRAIN, chords="F C", lines=[{"text": "What a big adventure day!", "notes": "F4:1 F4:.5 F4:.5 E4:.5,D4:.5,E4:.5 C4:2.5", "rest": 2}])

# stages used for one or two shots
IN_WATER = [("tumble", "tumble", 620, 1012, .62), ("milo", "milo", 1480, 660, .7, True, True)]
TREE_MANGO = [("tumble", "tumble", 940, 930, .62), ("mango", "monkey_hang", 760, -470, .5), ("milo", "milo", 500, 440, .75, False, True)]
TREE_GIFT = [("tumble", "tumble", 1000, 930, .62), ("mango", "monkey", 560, 934, .6), ("milo", "milo", 300, 520, .72, False, True)]
HILL_TOP = [("mango", "monkey", 300, 934, .58), ("tumble", "tumble", 700, 930, .62), ("sandy", "calf", 1300, 935, .56), ("milo", "milo", 200, 500, .7, False, True)]
SAD = [("mango", "monkey", 600, 934, .58), ("tumble", "tumble", 1000, 930, .62), ("sandy", "calf", 1780, 935, .56, True), ("milo", "milo", 780, 480, .66, False, True)]
FRUIT_T = lambda x, y: prop("fruit", art2.fruit, x, y, .62)          # the fruit, about as big as Tumble's head

SHOTS = [
    # ------------------------------------------------------------ HOOK: the feeling and the problem in the first 5 seconds
    S("zoo", C("zoo", "tumble", "all", 900, 20, -10), "Today is Mama's birthday. And Tumble has no present!", beat="hook", tag="hook: no present", hide=["mama", "milo"],
      words=[("w:no", "NO PRESENT?", .3, .28, .85, "")], fx=[("face", "w:And", "tumble", "sad")]),
    S("zoo", C("zoo", "milo", "body", 760), "I'm Milo! Come on a big adventure with us!", tag="hook: Milo", hide=["mama", "tumble"], fx=[("hop", "w:big", "milo")]),
    S("zoo", WIDE, "This is Tumble, the baby elephant, and this is his mama.", tag="zoo wide", cam2=(1000, 560, 1760),
      props=[prop("b1", lambda p: art2.balloon(p), 960, 640, 1.0), prop("b2", lambda p: art2.balloon(p, "#ffd23f"), 1050, 600, 1.0)],
      words=[("w:Tumble,", "TUMBLE", .35, .4, .9, "pill"), ("w:mama.", "MAMA", .72, .2, .9, "pill")]),
    S("zoo", C("zoo", "mama", "head", 900, -40, 40), "Mama Elephant is one year older today. Happy birthday, Mama!", tag="Mama close", hide=["tumble", "milo"],
      fx=[("nod", "w:Happy", "mama")], words=[("w:Happy", "HAPPY BIRTHDAY!", .27, .2, .78, "sun")]),
    S("zoo", (1270, 560, 1580), "Mama is big, and gentle, and kind.", tag="Mama is kind", hide=["milo"], move={"tumble": (780, 936, .6)},
      fx=[("trunk", "w:gentle,", "mama", 20, .6), ("face", "w:kind.", "tumble", "happy")], words=[("w:big,", "BIG", .3, .16, 1.0, "sun"), ("w:kind.", "KIND", .5, .16, 1.0, "")]),
    # ------------------------------------------------------------ GOAL
    S("zoo", C("zoo", "tumble", "head", 860, -60, 20), "Mama loves sweet, golden fruit. I want to find her the biggest one!", who="tumble", beat="goal", tag="goal: the fruit", hide=["mama", "milo"],
      props=[prop("th", lambda p: art2.bubble_thought(p, art2.fruit(p + "f"), tail=1), 520, 600, .6, True)], fx=[("show", "w:golden", "th"), ("face", 0.1, "tumble", "happy")]),
    S("zoo", C("zoo", "milo", "body", 820, 30, 0), "The best golden fruit grows far away, at the top of the tallest tree.", tag="Milo knows", hide=["mama", "tumble"],
      words=[("w:far", "FAR AWAY", .74, .24, 1.0, "pill")]),
    S("zoo", C("zoo", "tumble", "head", 800, -40, 10), "So far? How will we get there, Milo?", who="tumble", tag="how", hide=["mama", "milo"], fx=[("face", 0.02, "tumble", "wow"), ("lookat", 0.2, "tumble", -6)]),
    S("zoo", C("zoo", "milo", "body", 700, 0, 0), "I know the way. Look at my map!", tag="the map", hide=["mama", "tumble"], fx=[("hop", "w:Look", "milo")]),
    S("paper", (960, 540, 1700), "We must cross a river, climb a tree, and walk over a hill.", tag="board: the way", props=[prop("map", art2.map_board, 960, 520, 1.15)],
      fx=[("fromto", 0, "#{p}map-b,#{p}map-c,#{p}map-d", {"opacity": 0}, {"opacity": 0, "duration": .01}, ""), ("to", "w:river,", "#{p}map-b", {"opacity": 1, "duration": .25}, "the river on the map"),
          ("to", "w:tree,", "#{p}map-c", {"opacity": 1, "duration": .25}, "the tree on the map"), ("to", "w:hill.", "#{p}map-d", {"opacity": 1, "duration": .25}, "the hill on the map")],
      words=[("w:river,", "RIVER", .365, .7, .8, "pill"), ("w:tree,", "TREE", .635, .7, .8, "pill"), ("w:hill.", "HILL", .905, .7, .8, "pill")]),
    S("zoo", C("zoo", "tumble", "all", 1100, -120, -30), "Let's go, Tumble! We must be back before the sun goes down.", tag="let's go", hide=["mama"],
      fx=[("hop", "w:go,", "tumble"), ("fly", 0.1, "milo", 300, 770, .8)], q=False),
    S("savanna", WIDE, trans="iris", who="milo", sing=SING_GO, beat="song", tag="song: off we go", cam2=(1100, 560, 1700),
      fx=[("walk", 0.2, "tumble", 420, 7.6), ("fly", 0.2, "milo", 640, 600, 7.6), ("trunk", "w:come", "tumble", -60, .4), ("trunk", "w:me!", "tumble", 0, .4), ("trunk", "w:what", "tumble", -60, .4), ("trunk", "w:see?", "tumble", 0, .4)],
      move={"tumble": (520, 930, .62), "milo": (240, 520, .8)}, words=[("w:Friends", "FRIENDS HELP FRIENDS", .64, .15, .8, "pill"), ("w:Step", "STEP BY STEP", .64, .3, .9, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: the wide river (the trunk is a snorkel)
    S("river", WIDE, "They walk and walk. Then, oh! A wide river is in the way.", trans="iris", beat="obstacle1", tag="river wide", cam2=(960, 600, 1700),
      words=[("w:river", "RIVER", .72, .8, 1.0, "pill")]),
    S("river", C("river", "tumble", "all", 760, 30, -10), "It is too deep! I can not jump across.", who="tumble", beat="obstacle1", tag="too deep", hide=["milo"],
      fx=[("face", 0.1, "tumble", "sad"), ("lookat", 0.3, "tumble", 8)]),
    S("river", C("river", "milo", "body", 700, 20, 0), "Hmm. What can Tumble do? Jump over, or use his trunk?", q=True, beat="obstacle1", tag="question: jump or trunk", pause=3.2, hide=["tumble"],
      fx=[("signs", "w:Jump", ["JUMP", "TRUNK"], 1, "wait:2.8")]),
    S("river", C("river", "tumble", "head", 640, 30, -20), "I know! My trunk!", who="tumble", beat="obstacle1", tag="I know", hide=["milo"],
      fx=[("face", 0.05, "tumble", "wow"), ("trunk", "w:My", "tumble", -150, .5), ("hop", "w:trunk!", "tumble")]),
    S("river", (900, 800, 1700), "Tumble walks into the water, and lifts his trunk up high.", beat="obstacle1", tag="into the water", actors=IN_WATER, cam2=(1040, 780, 1560),
      props=[prop("wf", art2.water_front, 960, 940, 1.0)],
      fx=[("walk", 0.1, "tumble", 380, 4.2), ("trunk", "w:lifts", "tumble", -160, .7), ("to", "w:lifts", "#{p}tumble-trunk", {"scaleY": 1.35, "duration": .7}, ""),
          ("to", "w:water,", "#{p}wf_w", {"y": 850, "duration": 1.6, "ease": "sine.inOut"}, "the water gets deeper")]),
    S("river", (1030, 760, 1100), "He breathes through his trunk, just like a snorkel!", beat="obstacle1", tag="snorkel", actors=[("tumble", "tumble", 900, 1012, .62)],
      props=[prop("wf", art2.water_front, 960, 800, 1.0)], words=[("w:snorkel!", "SNORKEL!", .26, .2, 1.3, "sun")],
      fx=[("to", 0, "#{p}tumble-trunk", {"rotation": -160, "scaleY": 1.35, "svgOrigin": "392 -430", "duration": .01}, ""), ("walk", 0.1, "tumble", 160, 3.6),
          ("to", "w:breathes", "#{p}wf_w", {"y": 770, "duration": 1.2, "ease": "sine.inOut"}, "only the trunk is above the water")]),
    S("paper_blue", (960, 540, 1600), "An elephant can use its trunk like a snorkel in deep water.", beat="fact", tag="fact: the snorkel trunk",
      props=[prop("sb", art2.snorkel_board, 960, 400, 1.0)], words=[("w:trunk", "TRUNK", .36, .13, 1.0, "sun"), ("w:snorkel", "= SNORKEL", .68, .13, 1.0, "")],
      fx=[("to", 0, "#{p}sbe-trunk", {"rotation": -160, "scaleY": 1.35, "svgOrigin": "392 -430", "duration": .01}, "")]),
    S("savanna", C("savanna", "milo", "body", 820, 20, 0), "Can you lift your arm up high, like a trunk? Up, up, up!", q=True, beat="obstacle1", tag="question: arm up", hide=["tumble"],
      props=[prop("ar", lambda p: art.arrow(p, 770, 560, 770, 250), 0, 0, 1, True)], fx=[("show", "w:Up,", "ar"), ("hop", "w:Up,", "milo", 2)], words=[("w:Up,", "UP!", .84, .3, 1.5, "sun")]),
    S("savanna", C("savanna", "tumble", "all", 1000, 0, -30), "Trunks up! I did it!", who="tumble", beat="obstacle1", tag="across", hide=["milo"],
      fx=[("trunk", 0.05, "tumble", -150, .3), ("hop", "w:I", "tumble", 2), ("face", 0.02, "tumble", "happy")], words=[("w:Trunks", "TRUNKS UP!", .3, .26, .9, "sun")]),
    S("savanna", C("savanna", "milo", "body", 760, 10, 0), "Hooray, Tumble! You are so brave.", tag="hooray", hide=["tumble"], fx=[("hop", "w:Hooray,", "milo")]),
    # ------------------------------------------------------------ OBSTACLE 2: the tallest tree (the tail is an extra hand)
    S("jungle", WIDE, "Into the green jungle they go.", trans="iris", beat="obstacle2", tag="jungle wide", cam2=(1040, 560, 1720), fx=[("walk", 0.1, "tumble", 160, 3.0)], move={"tumble": (700, 930, .62)}),
    S("jungle", (900, 620, 1640), "The trees are so tall. The leaves are so big!", beat="obstacle2", tag="jungle look", hide=["milo"], cam2=(900, 600, 1500), move={"tumble": (860, 930, .62)},
      words=[("w:tall.", "TALL", .76, .24, 1.1, "sun"), ("w:big!", "BIG", .24, .3, 1.1, "")], fx=[("lookat", 0.2, "tumble", -12)]),
    S("bigtree", (1060, 560, 1700), "There it is! The tallest tree. And the golden fruit, at the very top.", beat="obstacle2", tag="the tree, tilt up", cam2=(1120, -330, 1500),
      props=[FRUIT_T(1150, -388)]),
    S("bigtree", (950, 330, 2900), "I will reach it with my trunk. Stretch!", who="tumble", beat="obstacle2", tag="stretch", props=[FRUIT_T(1150, -388)], hide=["milo"],
      fx=[("trunk", "w:Stretch!", "tumble", -165, .6), ("to", "w:Stretch!", "#{p}tumble-trunk", {"scaleY": 1.3, "duration": .6}, "")]),
    S("bigtree", (950, 330, 2900), "But the fruit is much too high.", beat="obstacle2", tag="too high", hide=["milo"],
      props=[FRUIT_T(1150, -388), prop("ar", lambda p: art.arrow(p, 1260, 420, 1260, -260), 0, 0, 1, True)], words=[("w:too", "TOO HIGH!", .72, .5, .8, "pill")],
      fx=[("to", 0, "#{p}tumble-trunk", {"rotation": -165, "scaleY": 1.3, "svgOrigin": "392 -430", "duration": .01}, ""), ("show", "w:much", "ar"), ("face", "w:too", "tumble", "sad"), ("trunk", "e:high.", "tumble", 0, .6)]),
    S("bigtree", (1100, -380, 1000), "I can fly up here. But the fruit is too heavy for a little bird!", beat="obstacle2", tag="Milo tries", hide=["tumble"], props=[FRUIT_T(1150, -388)],
      move={"milo": (900, -300, .7)}, fx=[("to", "w:heavy", "#{p}milo", {"x": "+=40", "duration": .18, "yoyo": True, "repeat": 5}, "Milo pulls and pulls"), ("face", "w:too", "milo", "sad")]),
    S("canopy", C("canopy", "mango", "head", 900, 40, -110), "Hello down there! Do you need a hand? Or a tail?", who="mango", beat="obstacle2", tag="Mango appears",
      fx=[("arm", "w:hand?", "mango", "r", -50), ("fromto", 0, "#{p}mango_w", {"y": 60}, {"y": 462, "duration": .7, "ease": "back.out(1.4)"}, "Mango drops down on her tail")]),
    S("canopy", (860, 560, 1500), "It is Mango, the spider monkey! She hangs upside down by her tail.", beat="obstacle2", tag="Mango hangs", words=[("w:Mango,", "MANGO", .2, .3, 1.1, "pill")],
      props=[prop("ar", lambda p: art.arrow(p, 1100, 600, 830, 500), 0, 0, 1, True)], fx=[("show", "w:tail.", "ar")]),
    S("canopy", C("canopy", "mango", "head", 760, 0, -60), "I know all about fruit. Fruit is what I eat the most!", who="mango", beat="obstacle2", tag="Mango loves fruit",
      props=[prop("fr", art2.fruit, 1060, 640, .7, True)], fx=[("show", "w:Fruit", "fr"), ("arm", "w:eat", "mango", "l", 40)]),
    S("paper_pink", (960, 540, 1600), "A spider monkey's tail can hold on, just like an extra hand.", beat="fact", tag="fact: the tail",
      actors=[("m", "monkey_hang", 960, 232, 1.0)], props=[prop("br", lambda p: f'<rect x="-700" y="-40" width="1400" height="56" rx="26" fill="#8a6238" stroke="{art.INK}" stroke-width="8"/>', 960, 232, 1.0),
                                                          prop("ar", lambda p: art.arrow(p, 610, 420, 900, 330), 0, 0, 1, True)],
      words=[("w:tail", "TAIL", .2, .44, 1.2, "sun"), ("w:extra", "EXTRA HAND!", .82, .62, .85, "pill")], fx=[("show", "w:tail", "ar")]),
    S("canopy", (960, 560, 1500), "Swing-a-ding! Here I go!", who="mango", beat="obstacle2", tag="Mango swings", props=[prop("fruit", art2.fruit, 1230, 602, 1.0)], speak="Swing a ding! Here I go!",
      fx=[("to", "w:Here", "#{p}mango_w", {"x": 1040, "duration": 1.0, "ease": "power1.inOut"}, "Mango swings along the branch"),
          ("to", "w:Here", "#{p}mango-swing", {"rotation": -16, "svgOrigin": "0 0", "duration": .5, "yoyo": True, "repeat": 1}, "")]),
    S("canopy", (1120, 600, 1100), "Mango holds the branch with her tail, and picks the fruit with both hands.", beat="obstacle2", tag="picks the fruit",
      props=[prop("fruit", art2.fruit, 1230, 602, 1.0)], move={"mango": (1040, 462, .6)},
      fx=[("arm", "w:picks", "mango", "l", 42), ("arm", "w:picks", "mango", "r", -8), ("to", "w:both", "#{p}fruit_w", {"y": 640, "duration": .3, "ease": "back.out(2)"}, "the fruit comes off the branch")]),
    S("canopy", (1100, 600, 1300), "How many hands does Mango use? One, two. And one tail!", q=True, beat="obstacle2", tag="count the hands", props=[prop("fruit", art2.fruit, 1230, 640, 1.0)],
      move={"mango": (1040, 462, .6)}, fx=[("to", 0, "#{p}mango-al", {"rotation": 42, "svgOrigin": "-58 -206", "duration": .01}, "")],
      words=[("w:One,", "1", .2, .5, 2.0, "sun"), ("w:two.", "2", .32, .5, 2.0, "sun"), ("w:tail!", "+ 1 TAIL", .28, .72, 1.0, "pill")]),
    S("bigtree", (800, 640, 1500), "Here you go, Tumble. One golden fruit for your mama!", who="mango", beat="obstacle2", tag="the gift", actors=TREE_GIFT, props=[FRUIT_T(840, 800)],
      fx=[("arm", 0.05, "mango", "r", -70), ("to", "w:One", "#{p}fruit_w", {"x": 1385, "y": 815, "duration": .7, "ease": "power2.inOut"}, "the fruit goes to Tumble"), ("trunk", "w:One", "tumble", -40, .5)]),
    S("bigtree", C("bigtree", "tumble", "all", 1000, 30, -20, TREE_GIFT), "Thank you, Mango! Will you come to the party?", who="tumble", beat="obstacle2", tag="thank you", actors=TREE_GIFT, hide=["milo", "mango"],
      props=[FRUIT_T(1385, 815)], fx=[("to", 0, "#{p}tumble-trunk", {"rotation": -40, "svgOrigin": "392 -430", "duration": .01}, ""), ("hop", "w:Thank", "tumble"), ("face", 0.02, "tumble", "happy")]),
    S("bigtree", C("bigtree", "mango", "all", 760, 0, -20, TREE_GIFT), "Yes, please! I love a party.", who="mango", beat="obstacle2", tag="yes please", actors=TREE_GIFT, hide=["milo", "tumble"],
      fx=[("hop", "w:Yes,", "mango", 2), ("arm", "w:love", "mango", "l", 60), ("arm", "w:love", "mango", "r", -60)]),
    # ------------------------------------------------------------ OBSTACLE 3: the big sandy hill (wide feet do not sink)
    S("dune_eve", WIDE, "The way home goes over a big, sandy hill.", trans="iris", beat="obstacle3", tag="hill wide", hide=["sandy"], cam2=(900, 560, 1760), props=[FRUIT_T(1085, 815)],
      fx=[("to", 0, "#{p}tumble-trunk", {"rotation": -40, "svgOrigin": "392 -430", "duration": .01}, "")]),
    S("dune_eve", (730, 890, 640), "Step, sink. Step, sink. Tumble's heavy feet sink into the soft sand.", beat="obstacle3", tag="feet sink", hide=["sandy", "milo", "mango"],
      fx=[("to", "w:sink.", "#{p}tumble", {"y": "+=22", "duration": .3, "yoyo": True, "repeat": 1}, "Tumble sinks"), ("to", "w:sink.:2", "#{p}tumble", {"y": "+=22", "duration": .3, "yoyo": True, "repeat": 1}, "Tumble sinks"),
          ("to", "w:soft", "#{p}tumble", {"y": "+=26", "duration": .5}, "his feet are in the sand")], words=[("w:sink.", "SINK!", .8, .24, 1.2, "sun")]),
    S("dune_eve", C("dune_eve", "tumble", "head", 760, -40, 10), "Puff, puff. The fruit is so heavy, and the hill is so high.", who="tumble", beat="obstacle3", tag="so heavy", hide=["sandy", "milo", "mango"],
      props=[FRUIT_T(1085, 815)], fx=[("to", 0, "#{p}tumble-trunk", {"rotation": -40, "svgOrigin": "392 -430", "duration": .01}, ""), ("face", 0.05, "tumble", "sad")]),
    S("dune_eve", (1500, 420, 1100), "And look! The sun is going down.", beat="obstacle3", tag="the sun goes down", hide=["tumble", "mango", "milo", "sandy"],
      fx=[("to", 0.2, "#{p}sun", {"y": 90, "duration": 3.0, "ease": "none"}, "the sun sinks"), ], words=[("w:sun", "HURRY!", .26, .3, 1.1, "pill")]),
    S("dune_eve", C("dune_eve", "sandy", "all", 900, -40, -20), "Hello, friends! I am Sandy. Sand is easy for me!", who="sandy", beat="obstacle3", tag="Sandy comes", hide=["tumble", "mango", "milo"],
      fx=[("fromto", 0, "#{p}sandy_w", {"x": 2100}, {"x": 1480, "duration": 1.4, "ease": "power1.out"}, "Sandy walks in"), ("nod", "w:Sand", "sandy")], words=[("w:Sandy.", "SANDY", .74, .2, 1.0, "pill")]),
    S("paper_blue", (960, 540, 1500), "A camel's wide feet spread out, so they do not sink in the sand.", beat="fact", tag="fact: wide feet",
      props=[prop("foot", lambda p: art.footprint(p), 960, 620, 3.0)], words=[("w:wide", "WIDE FEET", .5, .16, 1.2, "sun"), ("w:not", "NO SINKING!", .84, .36, .8, "pill")],
      fx=[("to", "w:spread", "#{p}foot_w", {"scaleX": 1.18, "transformOrigin": "50% 50%", "duration": .5, "yoyo": True, "repeat": 3}, "the foot spreads out")]),
    S("dune_eve", (1160, 620, 1560), "Put the fruit on my back, Tumble. Step, step, step!", who="sandy", beat="obstacle3", tag="fruit on Sandy", hide=["mango", "milo"], props=[FRUIT_T(1085, 815)],
      move={"sandy": (1420, 935, .56)},
      fx=[("to", 0, "#{p}tumble-trunk", {"rotation": -40, "svgOrigin": "392 -430", "duration": .01}, ""), ("to", "w:Put", "#{p}fruit_w", {"x": 1420, "y": 664, "duration": .8, "ease": "power2.inOut"}, "the fruit goes on Sandy's back"),
          ("trunk", "e:back,", "tumble", 0, .5)]),
    S("dune_eve", C("dune_eve", "tumble", "head", 780, -20, 10), "Thank you, Sandy! You are a good friend.", who="tumble", beat="obstacle3", tag="thank you Sandy", hide=["mango", "milo", "sandy"],
      fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:Thank", "tumble")]),
    S("dune_eve", WIDE, "Up the hill they go, all together.", beat="obstacle3", tag="up the hill", actors=HILL_TOP, props=[FRUIT_T(1300, 664)], cam2=(1060, 540, 1800),
      fx=[("walk", 0.1, "sandy", 260, 3.2), ("to", 0.1, "#{p}fruit_w", {"x": "+=260", "duration": 3.2, "ease": "none"}, ""), ("walk", 0.1, "tumble", 240, 3.2), ("walk", 0.1, "mango", 220, 3.2), ("fly", 0.1, "milo", 460, 520, 3.2)]),
    # ------------------------------------------------------------ LOW MOMENT: the fruit rolls away (gentle: nobody is hurt, nobody cries)
    S("dune_eve", C("dune_eve", "sandy", "all", 1000, -80, -40, HILL_TOP), "But at the top of the hill, bump!", beat="low", tag="bump", actors=HILL_TOP, hide=["mango", "milo", "tumble"], props=[FRUIT_T(1300, 664)],
      fx=[("to", "w:bump!", "#{p}sandy", {"y": "-=30", "duration": .14, "yoyo": True, "repeat": 1}, "a bump"), ("to", "w:bump!", "#{p}fruit_w", {"y": 600, "x": 1240, "duration": .3, "ease": "power2.out"}, "the fruit jumps off"),
          ("snd", "w:bump!", "boing")], words=[("w:bump!", "BUMP!", .24, .2, 1.3, "sun")]),
    S("dune_eve", (1000, 640, 1700), "The golden fruit rolls away. Down, down, down the hill.", beat="low", tag="the fruit rolls", actors=HILL_TOP, hide=["milo"], props=[FRUIT_T(1240, 760)], cam2=(760, 700, 1500),
      fx=[("to", 0.1, "#{p}fruit_w", {"x": 120, "y": 1000, "rotation": -900, "transformOrigin": "50% 50%", "duration": 3.6, "ease": "power1.in"}, "the fruit rolls down the hill")]),
    S("dune_eve", (330, 900, 900), "Splat. The fruit is squashed.", beat="low", tag="splat", actors=[], props=[prop("sp", art2.fruit_splat, 330, 985, 1.0)],
      fx=[("fromto", 0, "#{p}sp_w", {"scaleY": .2, "transformOrigin": "50% 100%"}, {"scaleY": 1, "duration": .3, "ease": "back.out(2)"}, "splat"), ("snd", 0.05, "pop")], words=[("w:Splat.", "SPLAT!", .7, .2, 1.3, "sun")]),
    S("dune_eve", C("dune_eve", "tumble", "head", 760, -40, 20, SAD), "Oh no. Now I have no present for Mama.", who="tumble", beat="low", tag="Tumble is sad", actors=SAD, hide=["mango", "sandy", "milo"],
      fx=[("face", 0.02, "tumble", "sad")]),
    S("dune_eve", WIDE, "Tumble feels very sad. His friends come close.", beat="low", tag="friends come close", actors=SAD, cam2=(940, 600, 1700), props=[prop("sp", art2.fruit_splat, 330, 985, .7)],
      fx=[("to", 0, "#{p}tumble-brow", {"rotation": -16, "y": -4, "transformOrigin": "50% 50%", "duration": .01}, ""), ("face", 0.02, "tumble", "sad"),
          ("to", "w:His", "#{p}mango_w", {"x": 680, "duration": 1.2, "ease": "power1.inOut"}, "Mango comes close"), ("to", "w:His", "#{p}sandy_w", {"x": 1620, "duration": 1.2, "ease": "power1.inOut"}, "Sandy comes close")]),
    S("dune_eve", C("dune_eve", "milo", "body", 700, 20, 0, SAD), "Tumble is sad. What could help him feel better?", q=True, beat="low", tag="question: what could help", actors=SAD, hide=["tumble", "mango", "sandy"], pause=2.2),
    S("dune_eve", (900, 610, 1400), "It is okay to feel sad, Tumble. We are here with you.", beat="low", tag="we are here", actors=SAD, hide=["sandy"], move={"mango": (680, 934, .58)},
      fx=[("to", 0, "#{p}tumble-brow", {"rotation": -16, "y": -4, "transformOrigin": "50% 50%", "duration": .01}, ""), ("face", 0.02, "tumble", "sad"), ("arm", "w:We", "mango", "r", -40)], words=[("w:here", "WE ARE HERE", .8, .2, .85, "pill")]),
    # ------------------------------------------------------------ SOLUTION: found by the friends themselves
    S("dune_eve", (330, 950, 760), "Look, Tumble! There is something inside the fruit.", who="mango", beat="solution", tag="something inside", actors=[], props=[prop("sp", art2.fruit_splat, 330, 985, 1.0)],
      fx=[("to", "w:something", "#{p}sp-seed", {"scale": 1.5, "transformOrigin": "50% 50%", "duration": .3, "yoyo": True, "repeat": 3}, "the seed shines"), ("snd", "w:something", "ding")]),
    S("dune_eve", C("dune_eve", "sandy", "head", 820, -60, 40, SAD), "It is a seed! A seed can grow into a new tree.", who="sandy", beat="solution", tag="a seed", actors=SAD, hide=["tumble", "mango", "milo"],
      props=[prop("seed", art2.seed, 1370, 610, 1.6, True)], fx=[("show", "w:seed!", "seed"), ("nod", "w:grow", "sandy")], words=[("w:seed!", "A SEED!", .26, .2, 1.1, "sun")]),
    S("dune_eve", C("dune_eve", "tumble", "head", 820, -30, 10, SAD), "A tree with golden fruit, for Mama, every single year!", who="tumble", beat="solution", tag="Tumble's idea", actors=SAD, hide=["mango", "sandy", "milo"],
      props=[prop("th", lambda p: art2.bubble_thought(p, f'<g transform="translate(0 70) scale(1.1)">{art2.sprout(p + "s")}</g>', tail=1), 910, 610, .6, True)],
      fx=[("face", 0.02, "tumble", "wow"), ("show", "w:tree", "th"), ("hop", "w:every", "tumble"), ("face", "w:golden", "tumble", "happy")]),
    S("dune_eve", C("dune_eve", "milo", "body", 760, 20, 0, SAD), "What a wonderful idea, Tumble!", beat="solution", tag="wonderful idea", actors=SAD, hide=["tumble", "mango", "sandy"], fx=[("hop", "w:wonderful", "milo")]),
    S("dune_eve", (1150, 880, 900), "Tumble picks up the tiny seed with the tip of his trunk. So gently!", beat="solution", tag="picks up the seed", actors=[("tumble", "tumble", 800, 930, .62)],
      props=[prop("seed", art2.seed, 1180, 930, .8)], fx=[("lookat", 0.1, "tumble", 10), ("to", "w:tip", "#{p}seed_w", {"y": 850, "x": 1140, "duration": .6, "ease": "power2.out"}, "the seed is lifted"),
                                                              ("trunk", "w:tip", "tumble", -18, .6)], words=[("w:gently!", "GENTLY", .74, .2, 1.0, "pill")]),
    S("dune_eve", WIDE, who="milo", sing=SING_HOME, beat="song", tag="song: home we go", actors=HILL_TOP, cam2=(1080, 560, 1760),
      fx=[("walk", 0.2, "sandy", 300, 7.6), ("walk", 0.2, "tumble", 300, 7.6), ("walk", 0.2, "mango", 300, 7.6), ("fly", 0.2, "milo", 700, 540, 7.6), ("trunk", "w:come", "tumble", -60, .4), ("trunk", "w:me!", "tumble", 0, .4),
          ("arm", "w:Home", "mango", "l", 60), ("arm", "w:happy", "mango", "r", -60)], words=[("w:Friends", "FRIENDS HELP FRIENDS", .64, .15, .8, "pill"), ("w:Home", "HOME WE GO!", .64, .3, .9, "sun")]),
    # ------------------------------------------------------------ WARM ENDING: back at the zoo
    S("zoo_eve", WIDE, "Back at the zoo, the sun is low and golden.", trans="iris", beat="ending", tag="zoo at sunset", hide=["mama"], cam2=(900, 560, 1760)),
    S("zoo_eve", (1150, 900, 800), "Tumble digs a little hole.", beat="ending", tag="digs a hole", hide=["mama", "milo", "sandy", "mango"],
      props=[prop("hole", lambda p: f'<ellipse cx="0" cy="0" rx="80" ry="22" fill="#7a5632" stroke="{art.INK}" stroke-width="7"/>', 1250, 950, 1.0, True)],
      fx=[("trunk", 0.2, "tumble", -30, .3), ("trunk", 0.8, "tumble", 0, .3), ("show", 0.9, "hole"), ("snd", 0.9, "pop")]),
    S("zoo_eve", (1220, 810, 1140), "Mango drops in the seed. Sandy pats the sand.", beat="ending", tag="the seed goes in", hide=["mama", "milo", "tumble"],
      move={"mango": (1000, 940, .55), "sandy": (1540, 940, .5, True)},
      props=[prop("hole", lambda p: f'<ellipse cx="0" cy="0" rx="80" ry="22" fill="#7a5632" stroke="{art.INK}" stroke-width="7"/>', 1250, 950, 1.0), prop("seed", art2.seed, 1150, 800, .7)],
      fx=[("arm", 0.1, "mango", "r", -60), ("to", "w:drops", "#{p}seed_w", {"x": 1250, "y": 944, "duration": .5, "ease": "power2.in"}, "the seed drops into the hole"),
          ("nod", "w:pats", "sandy")]),
    S("zoo_eve", (1130, 760, 1300), "And Tumble sprays it with water. Whoosh!", beat="ending", tag="sprays water", hide=["mama", "milo", "sandy", "mango"],
      props=[prop("hole", lambda p: f'<ellipse cx="0" cy="0" rx="90" ry="24" fill="#9a6a3a" stroke="{art.INK}" stroke-width="7"/>', 1420, 950, 1.0), prop("spray", art2.spray, 1200, 740, 1.0, True)],
      fx=[("trunk", 0.1, "tumble", -60, .4), ("show", "w:sprays", "spray"), ("snd", "w:Whoosh!", "whoosh")], words=[("w:Whoosh!", "WHOOSH!", .3, .2, 1.2, "sun")]),
    S("zoo_eve", C("zoo_eve", "mama", "head", 1000, 80, 60), "Tumble! What are you making?", who="mama", beat="ending", tag="Mama comes", hide=["milo", "sandy", "mango", "tumble"],
      fx=[("fromto", 0, "#{p}mama_w", {"x": 2200}, {"x": 1600, "duration": 1.2, "ease": "power1.out"}, "Mama walks in")]),
    S("zoo_eve", (1260, 700, 1400), "Happy birthday, Mama! It is a fruit tree. It will grow and grow, just for you.", who="tumble", beat="ending", tag="happy birthday", hide=["milo", "sandy", "mango"],
      props=[prop("spr", art2.sprout, 1112, 950, .9, True)], move={"tumble": (800, 940, .6)}, fx=[("show", "w:fruit", "spr"), ("hop", "w:Happy", "tumble"), ("to", "w:grow", "#{p}spr_w", {"scale": 1.25, "transformOrigin": "50% 100%", "duration": .8}, "the little tree grows")]),
    S("zoo_eve", (520, 720, 1100), "Happy birthday, Mama Elephant!", who="mango", beat="ending", tag="friends cheer", hide=["milo", "mama", "tumble"],
      fx=[("hop", "w:Happy", "mango", 2), ("arm", "w:Happy", "mango", "l", 60), ("arm", "w:Happy", "mango", "r", -60), ("hop", "w:Mama", "sandy")]),
    S("zoo_eve", C("zoo_eve", "mama", "head", 900, 60, 50), "Oh, Tumble. This is the best present of all.", who="mama", beat="ending", tag="the best present", hide=["milo", "sandy", "mango", "tumble"],
      fx=[("blinkslow", "w:best", "mama-eye", 1), ("nod", "w:This", "mama")]),
    S("zoo_eve", (1260, 660, 1300), "Mama wraps her trunk around Tumble. A big, warm trunk hug.", beat="ending", tag="trunk hug", hide=["milo", "sandy", "mango"], move={"tumble": (1010, 940, .6)},
      props=[prop("spr", art2.sprout, 760, 950, 1.0), prop("h1", lambda p: art2.heart(p), 1240, 380, 1.0, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 1380, 300, .7, True)],
      fx=[("trunk", "w:wraps", "mama", 34, .8), ("lookat", "w:wraps", "mama", 8), ("show", "w:big,", "h1"), ("show", "w:hug.", "h2"),
          ("to", "w:big,", "#{p}h1_w,#{p}h2_w", {"y": "-=60", "duration": 1.6, "ease": "sine.out"}, "")], words=[("w:hug.", "TRUNK HUG", .24, .2, 1.0, "pill")]),
    S("zoo_eve", C("zoo_eve", "tumble", "head", 800, -20, 0), "I love you, Mama.", who="tumble", beat="ending", tag="I love you", hide=["milo", "sandy", "mango", "mama"], fx=[("face", 0.02, "tumble", "happy"), ("blinkslow", "w:love", "tumble-eye", 1)]),
    S("zoo_eve", C("zoo_eve", "mama", "head", 900, 60, 50), "I love you too, my little Tumble.", who="mama", beat="ending", tag="I love you too", hide=["milo", "sandy", "mango", "tumble"], fx=[("nod", "w:too,", "mama")]),
    S("zoo_eve", (1000, 760, 1300), "One day, this little tree will be as tall as Mama.", beat="ending", tag="the little tree", hide=["milo", "sandy", "mango", "mama", "tumble"],
      props=[prop("spr", art2.sprout, 1000, 950, 1.3)], fx=[("to", "w:tall", "#{p}spr_w", {"scale": 1.7, "transformOrigin": "50% 100%", "duration": 1.2, "ease": "power1.inOut"}, "the little tree grows tall")],
      words=[("w:tall", "ONE DAY...", .26, .2, 1.0, "pill")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 760, 0, 0), "A present made with friends is the best present of all.", beat="ending", tag="the lesson", hide=["mama", "tumble", "sandy", "mango"],
      words=[("w:friends", "WITH FRIENDS", .74, .26, .85, "pill")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 40, 0), "Do you remember? Who used a trunk like a snorkel? Tumble, or Mango?", q=True, beat="ending", tag="question: who", pause=3.2, hide=["mama", "tumble", "sandy", "mango"], cam2=C("zoo_eve", "milo", "body", 830, 40, -60),
      fx=[("signs", "w:Tumble,", ["TUMBLE", "MANGO"], 0, "wait:2.8")]),
    S("zoo_eve", WIDE, who="milo", sing=SING_END_A, beat="song", tag="song: hooray", cam2=(980, 560, 1880), props=[prop("spr", art2.sprout, 1114, 950, .8)],
      fx=[("hop", 1.0, "tumble"), ("hop", 2.2, "mango"), ("hop", 3.2, "sandy")], words=[("w:hooray,", "HOORAY!", .18, .3, 1.05, "sun")]),
    S("zoo_eve", (1240, 640, 1280), who="milo", sing=SING_END_B, beat="song", tag="song: adventure day", cam2=(1240, 620, 1200), hide=["milo", "sandy", "mango"],
      props=[prop("spr", art2.sprout, 1114, 950, .8), prop("h1", lambda p: art2.heart(p), 1150, 440, .9, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 1050, 390, .6, True)],
      fx=[("hop", 0.6, "tumble"), ("nod", 1.6, "mama"), ("show", "w:big", "h1"), ("show", "w:day!", "h2"), ("hop", 3.0, "tumble")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 0, 0), "See you on the next adventure, friends!", beat="ending", tag="goodbye", hide=["mama", "sandy"], fx=[("hop", "w:next", "milo")],
      words=[("w:next", "SEE YOU SOON!", .74, .2, .9, "pill")]),
]

# thumbnail (thumb.py): the gift in the picture, 3 words at most, none of the title's words, no watermark
THUMBS = {
    "za_ep01": {"place": "zoo", "cam": (960, 540, 1920),
                "actors": [("elephant_hat", 1420, 1010, 1.0, True, ""), ("tumble", 500, 1010, .78, False, 'gsap.set("#P-trunk",{rotation:-40,svgOrigin:"392 -430"});')],
                "props": [(art2.fruit, 975, 850, .8), (lambda p: art2.heart(p), 960, 470, 1.5)],
                "words": [("BEST GIFT EVER!", 610, 125, 132, "sun")]},
}
EP["thumb_text"] = "BEST GIFT EVER!"
