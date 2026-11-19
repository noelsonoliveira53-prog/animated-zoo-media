"""za_ep05 - Milo's Zoo Adventures: "Who Took Mango's Breakfast?" (cartoon adventure, the 3D music-and-sync process: "beat").
Mango's breakfast (three golden fruits and a banana on a big leaf) is gone from her branch. She is sure somebody took it. With Tumble and Milo
she follows three clues: a banana peel by the tree, a trail of sticky drips, and (when they stop guessing and listen) a happy little tune from a
bush. In the bush is Dot, a baby tapir: the fruit had rolled down the path to her, and she thought it was a present. Mango asks kindly, says it is
okay, and they share the rest. Nobody is hurt, lost, crying or trapped: Dot is near her mama, and nobody is in danger.

FACTS, read at the source on Nov 19 2026, 12:00-12:10 AM ET (each page fetched by the session's page reader, which quoted these sentences):
 [NGK] National Geographic Kids, kids.nationalgeographic.com/animals/mammals/facts/spider-monkey
   "During the day, the spider monkey searches for fruit, which makes up the main part of its diet."
 [LAZ] Los Angeles Zoo, lazoo.org/explore-your-zoo/our-animals/mammals/bairds-tapir/
   "a single calf is born with white stripes and spots"   "This camouflage allows the baby to blend in while hiding in dense bushes"
   "Tapirs are herbivores, eating fruits, leaves, grasses, and twigs."   "Baird's tapirs inhabit tropical rainforests ... of Central America."
 [DZ] Dublin Zoo, dublinzoo.ie/animal/tapir/
   "Tapir calves are born with "watermelon" spots and stripes to blend into dappled forest light and hide from predators."
   "This unique camouflage gradually fades into a solid dark brown adult coat after a few months."
   "Tapirs have a flexible snout (made of their upper lip and nose) that they use to detect smells, grasp food"   "They mostly eat leaves and fruits."
 Said as animal facts in the film (three fact shots and two closing questions), each from a quote above: in the daytime spider monkeys look for
 fruit, and fruit is their main food [NGK]; baby tapirs are born with white stripes and spots, like a little watermelon, that help them blend in
 among leaves and spots of sunlight, and the stripes and spots fade as they grow up [LAZ, DZ]; a tapir's snout is its nose and upper lip together,
 it bends, smells and grabs food [DZ]. Dot eating fruit fits "eating fruits" [LAZ, DZ].
 Read but NOT said: "hide from predators" (no danger in the film); how long the coat takes to change (the two pages say "six months" and "a few months").
 Not animal facts, said as what happens in THIS story: the breakfast on a leaf, the peel, the drips, the fruit rolling down the path, the bush, the tune.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep04 as A4          # the stream, the vine bridge deck, Mango gripping the rope with her tail (read only)
import art_za_ep05 as A
import kit
from kit import Kit, S, prop

EP = {"id": "za_ep05", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "tumble": {"voice": "am_puck", "speed": .85, "pitch": 5, "formant": 1.16, "gain": .66},
               "mango": {"voice": "af_bella", "speed": .95, "pitch": 2, "formant": 1.08, "gain": .95}, "mama": {"voice": "bf_emma", "speed": .8, "gain": .8},
               "dot": {"voice": "af_sky", "speed": .9, "pitch": 6, "formant": 1.25, "gain": .95}, "tmama": {"voice": "af_sarah", "speed": .82, "pitch": 3, "formant": 1.1, "gain": .88}},
      "title": "Who Took Mango's Breakfast?", "thumb_text": "A MYSTERY!",
      "series": "Milo's Zoo Adventures",
      "description": ("Mango the spider monkey wakes up hungry, but her breakfast is gone from her branch! Who took it? Mango, baby elephant Tumble and Milo the bluebird "
                      "follow the clues: a banana peel, a trail of sticky drips, and a happy little tune coming from a bush. Who is hiding in the leaves? "
                      "A gentle animal mystery for ages 2-6 about not guessing, asking kindly and sharing, with questions to answer, drips to count and a tune to clap along to.\n"
                      "Kids learn that fruit is a spider monkey's main food, that baby tapirs have stripes and spots like a little watermelon that help them blend in, "
                      "and that a tapir's bendy snout can smell and grab food.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNational Geographic Kids (spider monkey); Los Angeles Zoo (Baird's tapir); Dublin Zoo (tapir)."),
      "tags": ["spider monkey", "baby tapir", "monkey story for kids", "baby elephant", "animal stories for kids", "mystery story for kids", "sharing story for kids",
               "kids adventure cartoon", "tapir facts for kids", "counting for kids", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "canopy": [("mango", "monkey", 820, 422, .6), ("milo", "milo", 1460, 290, .7, False, True)],
    "bigtree": [("tumble", "tumble", 420, 930, .6), ("mango", "monkey_glass", 1120, 934, .55), ("milo", "milo", 230, 470, .72, False, True)],
    "jungle": [("tumble", "tumble", 360, 930, .6), ("mango", "monkey_glass", 1000, 934, .55), ("milo", "milo", 240, 460, .74, False, True)],
    "stream": [("tumble", "tumble", 120, 930, .6), ("mango", "monkey_glass", 560, 934, .55), ("milo", "milo", 420, 440, .7, False, True)],
    "hollow": [("tumble", "tumble", 340, 930, .55), ("mango", "monkey_glass", 760, 934, .55), ("milo", "milo", 560, 420, .7, False, True),
               ("dot", "tapir", 1500, 930, .5), ("tmama", "tapir_mama", 1560, 930, .6)],
    "zoo_eve": [("mango", "monkey", 300, 940, .55), ("tumble", "tumble", 660, 940, .6), ("mama", "elephant", 1540, 932, .9, True), ("milo", "milo", 330, 420, .68, False, True)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
SWIDE = (940, 680, 2000)
def only(place, *keep, stage=None): return [a[0] for a in (stage or STAGES[place]) if a[0] not in keep]

PLAIN = lambda x=1120, y=934: ("mango", "monkey", x, y, .55)            # Mango before she takes out her magnifying glass
BUSH = lambda x=1500, s=.85: prop("bu", A.bush, x, 960, s)               # the bush (drawn over the actors: Dot behind it is hidden)
BUSH_AWAY = lambda: prop("bu", A.bush, 2050, 960, .7)                    # after Dot comes out, the bush is at the right edge
DOT_OUT = ("dot", "tapir", 1000, 930, .5)                                 # Dot out of the bush, between Mango and the bush
LEAF = lambda n=0, nb=0, hidden=False: prop("lf", lambda p: A.breakfast(p, n, nb), 1150, 416, .8, hidden)
BUBBLE = lambda x, y, s=.62, side=-1: prop("tb", lambda p: art2.bubble_thought(p, f'<g transform="translate(0 40) scale(.72)">{A.breakfast(p + "i")}</g>', side), x, y, s, True)
PEEL = lambda x=860, y=980, s=.55, hidden=False: prop("pl", A.peel, x, y, s, hidden)
DRIPS = lambda name, pts, hidden=False: prop(name, lambda p: A.drips(p, pts), 0, 0, 1, hidden)
FR = lambda name, x, y, s=.36, hidden=False: prop(name, art2.fruit, x, y, s, hidden)
BR = lambda: prop("br", A4.bridge, 1080, 930, 1.0)
TAIL = lambda at, who="mango", n=5: ("to", at, "#{p}" + who + "-tail", {"rotation": 12, "svgOrigin": "40 -80", "duration": .25, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, f"{who} swishes her tail")
ARM = lambda at, side, deg, who="mango": ("arm", at, who, side, deg)
LOOK = lambda at, who="mango": ("arm", at, who, "r", -95)                 # Mango lifts her magnifying glass to her eye
RUSTLE = lambda at, n=5: ("to", at, "#{p}bu-leaves", {"rotation": 2, "svgOrigin": "0 0", "duration": .12, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "the bush rustles")
SNIFF = lambda at, who="dot", n=3: ("to", at, "#{p}" + who + "-trunk", {"rotation": -14, "svgOrigin": "296 -258", "duration": .16, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, f"{who}'s snout sniffs")
CROSS = [("tumble", "tumble", 360, 930, .6), ("mango", "monkey_grip", 760, 934, .55)]

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. Nobody sings or hums: the rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
# the detective tune (looking for clues): up and down, tiptoe steps (C bar, G bar / F bar, C bar)
SING_CLUE = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "C4:1 E4:1 G4:1 E4:1 D4:1 B3:1", "rest": 2},
                                 {"text": "~ ~ ~ ~ ~ ~", "notes": "A4:1 F4:1 A4:1 G4:1 E4:1 C4:1", "rest": 2}])
# Dot's happy little hum, played by the bells (C bar, G bar)
SING_HUM = dict(REFRAIN, chords="C G", lines=[{"text": "~ ~ ~ ~ ~", "notes": "G4:1 E4:1 G4:1 A4:.5,G4:.5 D4:1.5", "rest": 2.5}])
# the sharing tune (F bar, C bar, G bar, C bar)
SING_SHARE = dict(REFRAIN, chords="F C G C", lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "A4:1 C5:1 A4:1 F4:1 E4:1 G4:1", "rest": 2},
                                                    {"text": "~ ~ ~ ~ ~", "notes": "D4:1 G4:1 D4:1 G4:1 C4:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune

MCL = lambda place, dx=0, dy=-70, w=820: C(place, "milo", "body", w, dx, dy)          # Milo asks a question: low in the frame, under the signs

SHOTS = [
    # ------------------------------------------------------------ HOOK: the empty leaf in the first 5 seconds
    S("canopy", (980, 330, 1100), "Oh no! My breakfast is gone! Who took it?", who="mango", beat="hook", tag="hook: breakfast gone", hide=["milo"],
      props=[LEAF(), BUBBLE(1290, 160, .55, -1)], fx=[("face", 0.02, "mango", "wow"), ("show", "w:breakfast", "tb", 1.6), ARM("w:gone!", "r", -60), ("hop", "w:took", "mango")],
      words=[("w:gone!", "GONE!", .78, .62, 1.0, "sun")]),
    S("canopy", C("canopy", "milo", "body", 760, 0, -20), "I'm Milo! Mango can't find her breakfast. Can you help us look?", tag="hook: Milo", hide=["mango"], props=[LEAF()],
      fx=[("hop", "w:help", "milo")], words=[("w:breakfast.", "WHERE IS IT?", .76, .2, .7, "pill")]),
    S("canopy", (900, 470, 1500), "This is Mango, the spider monkey. This morning, her breakfast was right here, on a big leaf.", tag="canopy: the leaf was here", hide=["milo"],
      props=[LEAF(3, 1, True), prop("ar", lambda p: art.arrow(p, 1400, 200, 1240, 330), 0, 0, 1, True)],
      fx=[TAIL("w:Mango,"), ("show", "w:breakfast", "lf"), ("show", "w:here,", "ar")], words=[("w:Mango,", "MANGO", .3, .72, .85, "pill")]),
    S("canopy", (1150, 380, 900), "Three golden fruits, and one yellow banana. Yummy!", tag="the breakfast: count", hide=["milo", "mango"], props=[LEAF(3, 1)],
      fx=[("count", "w:Three", 3, .6, {"x": 1400, "y": 640}), ("to", "w:banana.", "#{p}lf-b0", {"rotation": -6, "svgOrigin": "0 0", "duration": .2, "yoyo": True, "repeat": 3}, "the banana wiggles")],
      words=[("w:banana.", "BANANA!", .5, .22, .9, "sun")]),
    # ------------------------------------------------------------ GOAL: find the breakfast; Tumble comes to help
    S("bigtree", WIDE, "Mango swings down, to find her friend Tumble, the baby elephant.", trans="iris", beat="goal", tag="Mango swings down", cam2=(980, 560, 1800),
      actors=[STAGES["bigtree"][0], ("mango", "monkey", 1120, 330, .55), STAGES["bigtree"][2]], hide=["milo"],
      fx=[("to", "w:swings", "#{p}mango_w", {"y": 934, "duration": 1.2, "ease": "power1.out"}, "Mango swings down"), ARM(0.05, "r", -160), ARM("w:find", "r", 0), ("hop", "w:Tumble,", "tumble")],
      words=[("w:Tumble,", "TUMBLE", .2, .38, .85, "pill")]),
    S("bigtree", C("bigtree", "mango", "head", 800, -60, 30, stage=[PLAIN()]), "Tumble! My breakfast is gone. Somebody took it, I'm sure!", who="mango", beat="goal", tag="Mango: somebody took it",
      actors=[PLAIN()], props=[BUBBLE(1330, 660, .5, -1)], fx=[("face", 0.02, "mango", "wow"), ("show", "w:breakfast", "tb"), ("hop", "w:sure!", "mango")],
      words=[("w:sure!", "SOMEBODY?", .78, .74, .7, "pill")]),
    S("bigtree", C("bigtree", "tumble", "head", 900, -60, 20), "Don't worry, Mango. Let's look for clues, and find it together!", who="tumble", beat="goal", tag="Tumble: let's find it", hide=["milo", "mango"],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:clues,", "tumble", -60, .4), ("hop", "w:together!", "tumble")], words=[("w:clues,", "CLUES!", .3, .18, .9, "sun")]),
    S("bigtree", MCL("bigtree", 30), "What does Mango eat for breakfast? Fruit, or fish?", q=True, beat="goal", tag="question: fruit or fish", pause=3.2, hide=["tumble", "mango"],
      fx=[("signs", "w:Fruit,", ["FRUIT", "FISH"], 0, "wait:1.8")]),
    S("paper_blue", (960, 560, 1700), "In the daytime, spider monkeys look for fruit. Fruit is their main food!", beat="fact", tag="fact: fruit is the main food",
      actors=[("m", "monkey", 620, 900, .9)], props=[FR("f1", 1100, 760, .7, True), FR("f2", 1300, 760, .7, True), FR("f3", 1200, 600, .7, True), prop("bn", A.banana, 1420, 880, .9, True)],
      fx=[("show", "w:fruit.", "f1"), ("show", "w:fruit.", "f2"), ("show", "w:Fruit:2", "f3"), ("show", "w:main", "bn"), ("hop", "w:food!", "m"), ARM("w:look", "r", -40, "m")],
      words=[("w:fruit.", "FRUIT!", .74, .16, .9, "sun"), ("w:main", "MAIN FOOD", .3, .16, .8, "pill")]),
    S("bigtree", C("bigtree", "mango", "all", 860, 60, -60), "I'll be a detective! I have my magnifying glass. Let's look for clues!", who="mango", beat="goal", tag="Mango: detective", hide=["tumble", "milo"],
      fx=[("face", 0.02, "mango", "happy"), LOOK("w:magnifying"), ARM("w:Let's", "r", 0), ("hop", "w:clues!", "mango")], words=[("w:detective!", "DETECTIVE!", .74, .2, .75, "sun")]),
    # ------------------------------------------------------------ CLUE 1 / OBSTACLE 1: the peel, and Mango guesses
    S("bigtree", (800, 760, 1300), "Mango looks down low. What is that, by the tree?", beat="obstacle1", tag="looking low", hide=["milo"], props=[PEEL()],
      fx=[LOOK("w:looks"), ("to", "w:looks", "#{p}mango-body", {"rotation": 6, "svgOrigin": "0 0", "duration": .4}, "Mango leans down"), ("show", "w:that,", "pl")]),
    S("bigtree", MCL("bigtree", 40), "Is it a banana peel, or a leaf?", q=True, beat="obstacle1", tag="question: peel or leaf", pause=3.2, hide=["tumble", "mango"], props=[PEEL()],
      fx=[("signs", "w:peel,", ["PEEL", "LEAF"], 0, "wait:1.8")]),
    S("bigtree", (920, 860, 860), "A banana peel! And it's empty. Somebody ate my banana!", who="mango", beat="obstacle1", tag="the peel close", hide=["tumble", "milo"], props=[PEEL(860, 980, .7)],
      actors=[("mango", "monkey_glass", 1080, 934, .55)], fx=[("to", "w:empty.", "#{p}pl_w", {"rotation": -8, "duration": .2, "yoyo": True, "repeat": 3}, "the peel wiggles")],
      words=[("w:peel!", "A PEEL!", .3, .26, 1.0, "sun")]),
    S("bigtree", C("bigtree", "mango", "head", 800, -40, 30), "Tumble! Did you eat my banana?", who="mango", beat="obstacle1", tag="Mango: did you?", hide=["tumble", "milo"],
      fx=[("face", 0.02, "mango", "wow"), ARM("w:Tumble!", "l", 60), ARM("w:banana?", "l", 0)]),
    S("bigtree", C("bigtree", "tumble", "head", 900, -60, 20), "Not me, Mango! I was with my mama all morning.", who="tumble", beat="obstacle1", tag="Tumble: not me", hide=["milo", "mango"],
      fx=[("face", 0.02, "tumble", "wow"), ("trunk", "w:me,", "tumble", 20, .3), ("trunk", "w:mama", "tumble", -40, .4)], words=[("w:me,", "NOT ME!", .3, .18, .9, "pill")]),
    S("bigtree", C("bigtree", "mango", "head", 800, -40, 30), "Sorry, Tumble. I should not guess like that.", who="mango", beat="obstacle1", tag="Mango: sorry, no guessing", hide=["tumble", "milo"],
      fx=[("face", 0.02, "mango", "sad"), ("face", "w:like", "mango", "happy")], words=[("w:guess", "NO GUESSING", .74, .13, .7, "pill")]),
    # ------------------------------------------------------------ CLUE 2: the trail of drips
    S("bigtree", (1060, 860, 1100), "Look! Sticky drips, on the ground. Drip, drip, drip!", beat="obstacle1", tag="the drips start", hide=["milo", "tumble"], props=[PEEL(),
      DRIPS("dr", [(1000, 1000, 1), (1150, 1020, .9), (1300, 1004, 1), (1450, 1022, .9)], True)],
      fx=[("show", "w:Sticky", "dr"), LOOK("w:Look!"), ("hop", "e:drip!:3", "mango")], words=[("w:Sticky", "DRIPS!", .74, .24, .9, "sun")]),
    S("bigtree", C("bigtree", "tumble", "head", 900, -60, 20), "Sticky drips, from a juicy fruit! They go this way.", who="tumble", beat="obstacle1", tag="Tumble: this way", hide=["milo", "mango"],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:way.", "tumble", -50, .4)], words=[("w:way.", "THIS WAY!", .3, .18, .85, "sun")]),
    S("jungle", (760, 680, 1500), "The friends follow the trail, through the green jungle.", trans="iris", tag="follow the trail", move={"tumble": (220, 930, .6), "mango": (640, 934, .55), "milo": (600, 640, .74)},
      props=[DRIPS("dr", [(700, 990, 1), (900, 1010, .9), (1100, 994, 1), (1300, 1012, .9), (1500, 996, 1)])],
      fx=[("walk", 0.1, "tumble", 360, 3.2), ("walk", 0.1, "mango", 420, 3.2), ("fly", 0.1, "milo", 1000, 640, 3.2)]),
    S("jungle", (980, 860, 1300), "How many drips can you see? Count with me! One, two, three, four, five!", q=True, tag="question: count the drips", hide=["milo", "tumble", "mango"],
      props=[DRIPS("dr", [(500, 990, 1), (700, 1010, .9), (900, 994, 1), (1100, 1012, .9), (1300, 996, 1)])],
      fx=[("count", "w:One,", 5, 1.25, {"x": 960, "y": 300})] + [("to", f"w:{w}", f"#{{p}}dr-d{k}", {"scale": 1.4, "transformOrigin": "50% 50%", "duration": .15, "yoyo": True, "repeat": 1}, "")
                                                              for k, w in enumerate(["One,", "two,", "three,", "four,", "five!"])]),
    S("jungle", C("jungle", "mango", "all", 860, 40, -60), "Look down low, and look up high. We will find it, you and I!", who="mango", tag="the clue rhyme", hide=["tumble", "milo"],
      fx=[LOOK("w:low,"), ARM("w:high.", "r", -170), ARM("w:find", "r", 0), ("hop", "w:I!", "mango")], words=[("w:low,", "LOOK LOW", .24, .7, .75, "pill"), ("w:high.", "LOOK HIGH", .74, .2, .75, "sun")]),
    S("jungle", (980, 600, 1700), who="", sing=SING_CLUE, beat="song", tag="song: the clue tune", move={"tumble": (220, 930, .6), "mango": (700, 934, .55), "milo": (680, 580, .74)},
      props=[DRIPS("dr", [(900, 990, 1), (1100, 1010, .9), (1300, 994, 1), (1500, 1012, .9)])],
      fx=[("walk", TB(0), "tumble", 420, 9.6), ("walk", TB(0), "mango", 420, 9.6), ("fly", TB(0), "milo", 1080, 560, 9.6), LOOK(TB(2)), ARM(TB(6), "r", -170), ARM(TB(9), "r", -95), ("hop", TB(12), "mango")],
      words=[(TB(0), "TIPTOE...", .8, .14, .8, "sun"), (TB(8), "CLUES!", .8, .14, .9, "pill")]),
    # ------------------------------------------------------------ OBSTACLE 2: the trail stops at the stream
    S("stream", SWIDE, "Oh no! The drips go to the stream. And there, the trail stops!", trans="iris", beat="obstacle2", tag="the trail stops", cam2=(920, 560, 1900),
      props=[BR(), DRIPS("dr", [(380, 1000, 1), (560, 1020, .9), (720, 1000, 1)])], fx=[("face", "w:stops!", "mango", "sad"), ("face", "w:stops!", "tumble", "sad")],
      words=[("w:stops!", "NO MORE DRIPS", .56, .28, .7, "pill")]),
    S("stream", C("stream", "tumble", "head", 860, -40, 20), "The trail is gone. Where did it go?", who="tumble", beat="obstacle2", tag="Tumble: where did it go", hide=["mango", "milo"],
      props=[BR()], fx=[("face", 0.02, "tumble", "sad"), ("trunk", "w:go?", "tumble", 20, .4)], words=[("w:go?", "WHERE?", .3, .18, .9, "pill")]),
    S("stream", (1200, 720, 1500), "Milo flies up high, over the water. Look, more drips, on the other side!", beat="obstacle2", tag="Milo sees more drips", hide=["mango", "tumble"],
      move={"milo": (640, 620, .7)}, props=[BR(), DRIPS("dr", [(1440, 955, 1), (1600, 975, .9), (1760, 955, 1)], True)],
      fx=[("fly", "w:flies", "milo", 1180, 660, 1.4), ("show", "w:drips,", "dr"), ("hop", "w:side!", "milo")], words=[("w:side!", "OVER HERE!", .74, .22, .85, "sun")]),
    S("stream", MCL("stream", 20), "How can Tumble and Mango get across? Jump, or the bridge?", q=True, beat="obstacle2", tag="question: jump or bridge", pause=3.2, hide=["tumble", "mango"], props=[BR()],
      fx=[("signs", "w:Jump,", ["JUMP", "BRIDGE"], 1, "wait:1.8")]),
    S("stream", C("stream", "mango", "all", 800, 40, -80), "The vine bridge! Remember, Tumble? Slow and steady, side by side.", who="mango", beat="obstacle2", tag="Mango: slow and steady", hide=["tumble", "milo"],
      props=[BR()], fx=[("face", 0.02, "mango", "happy"), ARM("w:bridge!", "l", 60), ARM("w:Slow", "l", 0), ("hop", "w:side.:2", "mango")], words=[("w:Slow", "SLOW AND STEADY", .5, .16, .62, "pill")]),
    S("stream", (1000, 640, 1700), "Mango holds the vine with her tail, and Tumble's trunk with her hand. Step, step, step.", beat="obstacle2", tag="crossing", actors=CROSS, props=[BR()],
      fx=[ARM(0.05, "l", 60), ("walk", 0.3, "tumble", 500, 4.4), ("walk", 0.3, "mango", 500, 4.4), TAIL("w:tail,")], words=[("w:Step,", "STEP, STEP!", .5, .16, .8, "sun")]),
    S("stream", (1450, 760, 1500), "And there are the drips again! The trail goes on, down the path.", beat="obstacle2", tag="drips again", hide=["milo"],
      actors=[("tumble", "tumble", 1000, 930, .6), ("mango", "monkey_glass", 1560, 934, .55)], props=[BR(), DRIPS("dr", [(1720, 1000, 1), (1850, 1020, .9), (1980, 1000, 1)])],
      fx=[LOOK("w:drips"), ("hop", "w:again!", "mango"), ("face", 0.02, "tumble", "happy")], words=[("w:again!", "DRIPS!", .76, .25, .9, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 3: the drips stop at a big bush in the hollow
    S("hollow", WIDE, "Down, down the path, to a sunny hollow. The drips stop, right by a big bush.", trans="iris", beat="obstacle3", tag="the hollow and the bush", cam2=(980, 560, 1800),
      hide=["tmama"], props=[BUSH(), DRIPS("dr", [(860, 1000, 1), (1000, 1018, .9), (1130, 1004, 1)])], fx=[("walk", 0.1, "tumble", 0, .1), RUSTLE("w:bush.", 1)],
      words=[("w:bush.", "A BIG BUSH", .73, .4, .75, "pill")]),
    S("hollow", C("hollow", "tumble", "head", 860, -40, 20), "I'll look inside with my trunk.", who="tumble", beat="obstacle3", tag="Tumble: I'll look", hide=["mango", "milo", "tmama"],
      props=[BUSH()], fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:trunk.", "tumble", -40, .4)]),
    S("hollow", (1100, 760, 1500), "Tumble pokes his trunk in the leaves. Only leaves, and more leaves!", beat="obstacle3", tag="only leaves", hide=["milo", "tmama"], move={"tumble": (940, 930, .55), "mango": (520, 934, .55)},
      props=[BUSH()], fx=[("trunk", "w:pokes", "tumble", -20, .4), RUSTLE("w:pokes", 7), ("trunk", "w:Only", "tumble", 0, .4), ("face", "w:Only", "tumble", "sad")],
      words=[("w:Only", "ONLY LEAVES", .3, .2, .75, "pill")]),
    S("hollow", C("hollow", "mango", "all", 860, 40, -60), "Hello? Who has my breakfast? Come out!", who="mango", beat="obstacle3", tag="Mango calls", hide=["tumble", "milo", "tmama"], props=[BUSH()],
      fx=[("face", 0.02, "mango", "wow"), ARM("w:Hello?", "l", 70), ("hop", "w:out!", "mango"), ARM("w:out!", "l", 0)], words=[("w:Hello?", "HELLO?", .74, .2, 1.0, "sun")]),
    S("hollow", (1400, 760, 1100), "But nobody comes out. The bush is very still.", beat="obstacle3", tag="nobody comes out", hide=["tumble", "mango", "milo", "tmama"], props=[BUSH()],
      fx=[("to", 0.4, "#{p}bu", {"scale": 1.0, "duration": .1}, "the bush is still")], words=[("w:still.", "SO STILL...", .5, .2, .8, "pill")]),
    # ------------------------------------------------------------ LOW MOMENT: the clues are all used up (gentle: nobody cries)
    S("hollow", (540, 800, 1200), "Mango sits down on the grass. Her tummy is empty, and the clues are all gone.", beat="low", tag="Mango sits down", hide=["milo", "tmama"],
      move={"tumble": (340, 948, .55), "mango": (760, 950, .55)}, props=[BUSH()], fx=[("to", "w:sits", "#{p}mango_w", {"y": 960, "duration": .5}, "Mango sits down"), ("face", "w:sits", "mango", "sad"), ("face", "w:empty,", "tumble", "sad")],
      words=[("w:empty,", "SO HUNGRY", .75, .2, .8, "pill")]),
    S("hollow", C("hollow", "mango", "head", 760, 0, 20), "My breakfast is gone. And I don't know who took it.", who="mango", beat="low", tag="Mango: I don't know", hide=["tumble", "milo", "tmama"],
      fx=[("face", 0.02, "mango", "sad"), ("blinkslow", "w:know", "mango-eyeL", 1), ("blinkslow", "w:know", "mango-eyeR", 1)]),
    S("hollow", (540, 800, 1200), "Tumble sits next to her, close and warm.", beat="low", tag="Tumble sits close", hide=["milo", "tmama"], move={"tumble": (340, 948, .55), "mango": (760, 950, .55)}, props=[BUSH()],
      fx=[("to", 0.05, "#{p}mango_w", {"y": 960, "duration": .01}, ""), ("face", 0.05, "mango", "sad"), ("to", "w:sits", "#{p}tumble", {"y": 20, "duration": .6}, "Tumble sits down"), ("trunk", "w:close", "tumble", -10, .6), ("face", "w:warm.", "mango", "happy")]),
    # ------------------------------------------------------------ SOLUTION: Mango stops guessing; they listen, find Dot, and ask kindly
    S("hollow", C("hollow", "mango", "all", 860, 40, -60), "Wait. We looked with our eyes. Now, let's be quiet, and listen with our ears!", who="mango", beat="solution", tag="Mango: let's listen",
      hide=["tumble", "milo", "tmama"], fx=[("face", 0.02, "mango", "wow"), ("hop", "w:Wait.", "mango"), ARM("w:ears!", "l", 120)], words=[("w:listen", "LISTEN!", .74, .2, 1.0, "sun")]),
    S("hollow", MCL("hollow", 20), "Can you be very quiet, and listen with us?", q=True, beat="solution", tag="question: be quiet", pause=3.2, hide=["tumble", "mango", "tmama"],
      fx=[("signs", "w:quiet,", ["LOUD", "QUIET"], 1, "wait:1.8")]),
    S("hollow", (1360, 700, 1300), "Listen! Somebody in the bush is humming a happy little tune.", beat="solution", tag="the hum is named", hide=["tumble", "milo", "tmama"],
      actors=[("mango", "monkey_glass", 900, 934, .55)], props=[BUSH()], fx=[LOOK("w:Listen!"), RUSTLE("w:humming", 3), ("face", "w:happy", "mango", "wow")],
      words=[("w:humming", "HUM, HUM!", .74, .2, .9, "sun")]),
    S("hollow", (1500, 620, 1300), who="", sing=SING_HUM, beat="song", tag="song: the happy hum", hide=["tumble", "milo", "mango", "tmama"],
      props=[BUSH(), prop("n1", A.note, 1380, 640, .8, True), prop("n2", lambda p: A.note(p, "#57c0e8"), 1600, 610, .7, True), prop("n3", lambda p: A.note(p, "#ffb347"), 1490, 570, .75, True)],
      fx=[("show", TB(0), "n1"), ("show", TB(1.5), "n2"), ("show", TB(3), "n3"), RUSTLE(TB(0), 3), RUSTLE(TB(3), 3),
          ("to", TB(0), "#{p}n1_w,#{p}n2_w,#{p}n3_w", {"y": "-=40", "duration": 4.0, "ease": "sine.out"}, "")]),
    S("hollow", MCL("hollow", 20), "Where is the tune coming from? The bush, or the sky?", q=True, beat="solution", tag="question: bush or sky", pause=3.2, hide=["tumble", "mango", "tmama"],
      fx=[("signs", "w:bush,", ["BUSH", "SKY"], 0, "wait:1.8")]),
    S("hollow", (1420, 760, 1000), "Mango looks closely, with her magnifying glass. Stripes, and spots!", beat="solution", tag="stripes and spots in the leaves", hide=["tumble", "milo", "tmama"],
      actors=[("mango", "monkey_glass", 1040, 934, .55)], props=[BUSH(), prop("pk", A.bush_peek, 1540, 800, .8, True)],
      fx=[LOOK("w:looks"), ("show", "w:Stripes,", "pk"), ("face", "w:spots!", "mango", "wow")], words=[("w:Stripes,", "STRIPES!", .7, .2, .85, "sun"), ("w:spots!", "SPOTS!", .3, .2, .85, "pill")]),
    S("hollow", C("hollow", "mango", "head", 760, 0, 20), "Hello in there. Please come out. I won't be cross.", who="mango", beat="solution", tag="Mango asks kindly", hide=["tumble", "milo", "tmama"],
      fx=[("face", 0.02, "mango", "happy"), ARM("w:Please", "l", 50), ARM("w:cross.", "l", 0)], words=[("w:Please", "PLEASE?", .74, .22, .9, "sun")]),
    S("hollow", (1100, 740, 1500), "Out steps a baby tapir! Her name is Dot.", beat="solution", tag="Dot steps out", hide=["milo", "tmama"],
      actors=[("mango", "monkey_glass", 760, 934, .55), ("dot", "tapir", 1500, 930, .5)], props=[BUSH()],
      fx=[RUSTLE("w:Out", 3), ("walk", "w:Out", "dot", -500, 1.6), ("face", "w:Dot.", "mango", "happy"), ("hop", "w:Dot.", "dot")], words=[("w:Dot.", "DOT!", .74, .2, 1.0, "sun")]),
    S("hollow", C("hollow", "dot", "head", 760, -40, 20, stage=[DOT_OUT]), "Hello! I'm Dot. Mmm, that was a yummy present!", who="dot", beat="solution", tag="Dot: hello", hide=["tumble", "milo", "mango", "tmama"],
      actors=[DOT_OUT], props=[BUSH_AWAY()], fx=[("face", 0.02, "dot", "happy"), SNIFF("w:yummy"), ("hop", "w:present!", "dot")], words=[("w:present!", "A PRESENT?", .28, .2, .8, "pill")]),
    S("paper_pink", (960, 560, 1700), "Baby tapirs have white stripes and spots, like a little watermelon. They help a baby blend in, with the leaves and the spots of sunlight.", beat="fact",
      tag="fact: stripes and spots", actors=[("d", "tapir", 760, 820, 1.1)],
      props=[prop("lv", lambda p: art3.leaf(p), 1440, 500, .8, True), prop("sp", lambda p: f'<g id="{p}">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .45:.0f}" fill="#fff3a0" opacity=".8"/>' for x, y, rx in ((-200, 0, 90), (120, 30, 70), (300, -20, 60))) + '</g>', 960, 880, 1.0, True)],
      fx=[("show", "w:stripes", "sp"), ("show", "w:leaves", "lv"), ("hop", "w:watermelon.", "d")],
      words=[("w:stripes", "STRIPES + SPOTS", .5, .2, .7, "sun"), ("w:blend", "BLEND IN", .82, .7, .8, "pill")]),
    S("hollow", C("hollow", "mango", "head", 760, 0, 20), "Dot, did you find three golden fruits, and a banana?", who="mango", beat="solution", tag="Mango asks Dot", hide=["tumble", "milo", "tmama"],
      fx=[("face", 0.02, "mango", "happy"), ARM("w:three", "l", 50), ARM("w:banana?", "l", 0)]),
    S("hollow", C("hollow", "dot", "head", 760, -40, 20, stage=[DOT_OUT]), "Yes! Sniff, sniff! My nose smelled them rolling down the path, right to me!", who="dot", beat="solution", tag="Dot: sniff sniff",
      actors=[DOT_OUT], props=[BUSH_AWAY()], fx=[("face", 0.02, "dot", "happy"), SNIFF("w:Sniff,", "dot", 5), ("hop", "w:me!", "dot")], words=[("w:Sniff,", "SNIFF, SNIFF!", .28, .2, .8, "sun")]),
    S("paper_blue", (960, 560, 1700), "A tapir's snout is its nose and upper lip, together. It bends, it smells, and it grabs food!", beat="fact", tag="fact: the bendy snout",
      actors=[("d", "tapir", 640, 860, 1.25)], props=[FR("f1", 1240, 660, .6), prop("ar", lambda p: art.arrow(p, 1380, 360, 1180, 520), 0, 0, 1, True)],
      fx=[("show", "w:snout", "ar"), SNIFF("w:smells,", "d", 3), ("to", "w:grabs", "#{p}d-trunk", {"rotation": 10, "svgOrigin": "296 -258", "duration": .3, "yoyo": True, "repeat": 1}, "the snout grabs")],
      words=[("w:bends,", "BENDY SNOUT", .78, .16, .8, "sun"), ("w:grabs", "GRAB!", .84, .62, .9, "pill")]),
    S("hollow", MCL("hollow", 20), "What did Dot use to find the fruit? Her nose, or her tail?", q=True, beat="solution", tag="question: nose or tail", pause=3.2, hide=["tumble", "mango", "dot", "tmama"],
      fx=[("signs", "w:nose,", ["NOSE", "TAIL"], 0, "wait:1.8")]),
    S("hollow", C("hollow", "dot", "head", 760, -40, 20, stage=[DOT_OUT]), "I ate the banana. Was it yours? I'm sorry, Mango.", who="dot", beat="solution", tag="Dot: sorry", hide=["tumble", "milo", "mango", "tmama"],
      actors=[DOT_OUT], props=[BUSH_AWAY()], fx=[("face", 0.02, "dot", "sad"), ("blinkslow", "w:sorry,", "dot-eye", 1)]),
    S("hollow", C("hollow", "mango", "all", 860, 40, -60), "That's okay, Dot. You didn't know! My fruit rolled off my branch, all the way to you.", who="mango", beat="solution", tag="Mango: that's okay",
      hide=["tumble", "milo", "tmama"], fx=[("face", 0.02, "mango", "happy"), ARM("w:okay,", "l", 60), ARM("w:rolled", "l", 0), TAIL("w:you.:2")], words=[("w:okay,", "IT'S OKAY!", .74, .2, .85, "sun")]),
    S("hollow", (1000, 740, 1700), "Nobody took it. It just rolled away! Mango laughs, and Dot laughs too.", beat="solution", tag="nobody took it", hide=["milo", "tmama"],
      actors=[("tumble", "tumble", 340, 930, .55), ("mango", "monkey_glass", 760, 934, .55), DOT_OUT], props=[BUSH_AWAY(), FR("f1", 1720, 960, .4, True)],
      fx=[("show", "w:rolled", "f1"), ("to", "w:rolled", "#{p}f1_w", {"x": 1300, "rotation": -360, "duration": 1.0, "ease": "power1.out"}, "a fruit rolls"), ("hop", "w:laughs,", "mango"), ("hop", "w:too.", "dot"),
          ("face", "w:Nobody", "tumble", "happy")], words=[("w:rolled", "IT ROLLED!", .5, .16, .85, "sun")]),
    # ------------------------------------------------------------ WARM ENDING: sharing, Dot's mama, home
    S("hollow", C("hollow", "mango", "all", 860, 40, -60), "There are still three fruits. I know! Let's share!", who="mango", beat="ending", tag="Mango: let's share", hide=["tumble", "milo", "tmama"],
      fx=[("face", 0.02, "mango", "happy"), ("hop", "w:know!", "mango"), ("hop", "w:share!", "mango")], words=[("w:share!", "LET'S SHARE!", .74, .2, .8, "sun")]),
    S("hollow", (900, 820, 1000), "One for Dot, one for Tumble, and one for Mango. Count with me! One, two, three!", q=True, beat="ending", tag="question: count the shared fruit", hide=["milo", "tmama", "tumble"],
      actors=[("mango", "monkey", 760, 934, .55), DOT_OUT], props=[FR("f1", 820, 990), FR("f2", 900, 1000), FR("f3", 980, 990)],
      fx=[("to", "w:Dot,", "#{p}f1_w", {"x": 1180, "duration": .5}, "a fruit for Dot"), ("to", "w:Tumble,", "#{p}f2_w", {"x": 470, "duration": .5}, "a fruit for Tumble"),
          ("to", "w:Mango.", "#{p}f3_w", {"x": 640, "duration": .5}, "a fruit for Mango"), ("count", "w:One,:4", 3, .6, {"x": 1560, "y": 260}), ("hop", "w:three!", "dot")]),
    S("hollow", (1240, 720, 1600), "Then, out from the pool, comes Dot's mama. She has no stripes or spots at all!", beat="ending", tag="Dot's mama", hide=["milo"],
      actors=[("mango", "monkey", 760, 934, .55), DOT_OUT, ("tmama", "tapir_mama", 2160, 930, .6)], props=[BUSH_AWAY()],
      fx=[("walk", "w:out", "tmama", -640, 2.2), ("hop", "w:mama.", "dot"), ("face", "w:stripes", "mango", "wow")], words=[("w:stripes", "NO STRIPES!", .5, .16, .8, "pill")]),
    S("paper_blue", (960, 560, 1700), "When a baby tapir grows up, her stripes and spots fade away. Then she looks just like her mama!", beat="fact", tag="fact: the coat fades",
      actors=[("d", "tapir", 520, 860, .9), ("mm", "tapir_mama", 1240, 860, 1.05)], props=[prop("ar", lambda p: art.arrow(p, 820, 520, 1000, 520), 0, 0, 1, True)],
      fx=[("show", "w:grows", "ar"), ("hop", "w:mama!", "d"), ("nod", "w:mama!", "mm")], words=[("w:fade", "FADE AWAY", .5, .16, .8, "sun")]),
    S("hollow", C("hollow", "tmama", "head", 820, -40, 40, stage=[("tmama", "tapir_mama", 1560, 930, .6)]), "Thank you for being so kind to Dot. Please come and play again!", who="tmama", beat="ending", tag="Dot's mama: thank you",
      actors=[("tmama", "tapir_mama", 1560, 930, .6)], fx=[("face", 0.02, "tmama", "happy"), ("nod", "w:kind", "tmama")]),
    S("hollow", C("hollow", "mango", "all", 860, 40, -60), "Share a little, share a lot. Friends are the best breakfast we've got!", who="mango", beat="ending", tag="the sharing rhyme",
      hide=["tumble", "milo", "tmama"], fx=[ARM("w:little,", "l", 50), ARM("w:lot.", "l", 100), ARM("w:Friends", "l", 0), ("hop", "e:got!", "mango")],
      words=[("w:Share", "SHARE!", .74, .2, 1.0, "sun")]),
    S("hollow", (950, 620, 1800), who="", sing=SING_SHARE, beat="song", tag="song: the sharing tune", cam2=(950, 620, 1880),
      actors=[("tumble", "tumble", 340, 930, .55), ("mango", "monkey", 760, 934, .55), DOT_OUT, ("tmama", "tapir_mama", 1540, 930, .56), ("milo", "milo", 1310, 470, .66, False, True)], props=[BUSH_AWAY()],
      fx=[("hop", TB(0), "mango"), ("hop", TB(2), "dot"), ("hop", TB(4), "tumble"), TAIL(TB(6)), ("nod", TB(8), "tmama"), ("hop", TB(10), "dot"), ("hop", TB(12), "mango")],
      words=[(TB(0), "SHARE A LITTLE", .5, .14, .66, "sun"), (TB(8), "SHARE A LOT!", .5, .14, .7, "pill")]),
    S("zoo_eve", WIDE, "In the evening, Tumble and Mango walk back to the zoo. And Mama is waiting.", trans="iris", beat="ending", tag="back at the zoo", cam2=(1000, 560, 1800),
      move={"tumble": (300, 940, .6), "mango": (-60, 940, .55)}, fx=[("walk", 0.1, "tumble", 360, 3.2), ("walk", 0.1, "mango", 360, 3.2)], words=[("w:Mama", "HOME!", .5, .16, 1.0, "sun")]),
    S("zoo_eve", C("zoo_eve", "tumble", "all", 1000, 40, -60), "Mama! We found Mango's breakfast. A baby tapir found it first!", who="tumble", beat="ending", tag="Tumble tells Mama", hide=["mama", "milo", "mango"],
      fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:found", "tumble"), ("trunk", "w:tapir", "tumble", -50, .4)], words=[("w:tapir", "BABY TAPIR", .5, .16, .72, "pill")]),
    S("zoo_eve", C("zoo_eve", "mango", "head", 760, 60, 30), "I didn't need to guess who took it. I just needed to listen, and ask.", who="mango", beat="ending", tag="Mango: listen and ask", hide=["milo", "tumble", "mama"],
      fx=[("face", 0.02, "mango", "happy"), ("nod", "w:listen,", "mango"), TAIL("w:ask.")], words=[("w:ask.", "ASK KINDLY", .74, .2, .75, "sun")]),
    S("zoo_eve", C("zoo_eve", "mama", "head", 900, 60, 50), "Well done, both of you. Kind friends share.", who="mama", beat="ending", tag="Mama: kind friends share", hide=["milo", "tumble", "mango"],
      fx=[("nod", "w:Well", "mama"), ("blinkslow", "w:share.", "mama-eye", 1)], words=[("w:share.", "SHARE!", .2, .2, .9, "sun")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 130, 0), "When something goes missing, don't guess. Look, listen, and ask kindly.", beat="ending", tag="the lesson", hide=["mama", "tumble", "mango"],
      fx=[("hop", "w:kindly.", "milo")], words=[("w:Look,", "LOOK", .73, .16, .75, "pill"), ("w:listen,", "LISTEN", .73, .3, .75, "sun"), ("w:ask", "ASK", .73, .44, .75, "pill")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 40, 0), "Do you remember? What does a baby tapir have on her coat? Stripes and spots, or feathers?", q=True, beat="ending", tag="question: spots or feathers", pause=3.2,
      hide=["mama", "tumble", "mango"], cam2=C("zoo_eve", "milo", "body", 830, 40, -60), fx=[("hop", "w:remember?", "milo"), ("signs", "w:Stripes", ["SPOTS", "FEATHERS"], 0, "wait:1.8")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 1080, -160, -40), "And what is a spider monkey's main food? Fruit, or rocks?", q=True, beat="ending", tag="question: fruit or rocks", pause=3.2,
      hide=["mama", "tumble", "mango"], cam2=C("zoo_eve", "milo", "body", 1000, -160, -80), fx=[("hop", "w:food?", "milo"), ("signs", "w:Fruit,", ["FRUIT", "ROCKS"], 0, "wait:1.8")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 150, 0), "Next time: the rainy day umbrella! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure", hide=["mama", "tumble", "mango"],
      fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .72, .17, .72, "sun"), ("w:See", "SEE YOU SOON!", .72, .32, .62, "pill")]),
]

# thumbnail (thumb.py): the example in the picture (Mango's magnifying glass over the banana peel), 3 words at most, none of the title's words, no watermark
THUMBS = {
    "za_ep05": {"place": "bigtree", "cam": (980, 760, 1100),
                "actors": [("monkey_glass", 1120, 934, .7, False, 'gsap.set("#P-ar",{rotation:-60,svgOrigin:"58 -206"});')],
                "props": [(A.peel, 860, 990, .8)],
                "words": [("A MYSTERY!", 760, 470, 190, "sun")]},
}
