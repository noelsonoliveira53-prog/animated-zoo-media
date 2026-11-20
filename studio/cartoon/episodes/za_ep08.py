"""za_ep08 - Milo's Zoo Adventures: "The Long Walk to the Oasis" (cartoon adventure, the 3D music-and-sync process: "beat").
In the zoo garden the little tree is droopy and thirsty, and the watering can is empty. Milo, Sandy the baby camel and Tumble the baby elephant
walk to the oasis to bring water back in two little jugs. On the way Milo's wings get tired (he rests on Sandy's back), Tumble gets hot (they
rest in the shade of a big rock), and on the way back the sand is soft and the full jugs are heavy: Tumble's trunk wobbles, Milo cannot lift one.
Sitting on the sandy hill with the zoo far away, they think the tree may not get a drink today. Sandy works it out herself: camels are made
for carrying loads and walking far, and she had a big drink at the oasis, so she carries both jugs home, step by step. The tree drinks and
its leaves stand up. Nobody is hurt, lost, crying or trapped: Mama camel knows where they are going and when they will be back, the sun only
makes Tumble warm, and resting in the shade fixes it. Mama camel has no voice (no new voice in this film).

FACTS, read at the source on Nov 19 2026, about 7:50 PM ET (each page fetched by the session's page reader, which quoted these sentences):
 [NG]  National Geographic, "Arabian camel", nationalgeographic.com/animals/mammals/facts/arabian-camel
   "A very thirsty animal can drink 30 gallons of water in only 13 minutes."
   "They can carry large loads for up to 25 miles a day."
 [SDZ] San Diego Zoo Wildlife Alliance, "Camel", animals.sandiegozoo.org/node/173
   "A camel can go a week or more without water, and it can last for several months without food."
   "They can easily carry an extra 200 pounds (90 kilograms) while walking 20 miles (32 kilometers) a day in the harsh desert."
 [WWF] World Wildlife Fund, "What do camels store in their humps and other camel superpowers", worldwildlife.org
   "Camels can survive a week without water..."
 Said as animal facts in the film (three fact boards and questions), each from a quote above: a very thirsty camel can drink thirty gallons
 of water in only thirteen minutes [NG]; grown-up camels can carry big, heavy loads and walk a long way every day [NG, SDZ]; a camel can go
 a week or more without water [SDZ, WWF].
 Not animal facts, said as what happens in THIS story: Sandy (a calf) carrying two little jugs, Tumble flapping his ears in the heat,
 the tree, the oasis being far. Nothing is said about how much a baby camel can carry.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep07 as A7
import art_za_ep08 as A
import kit
from kit import Kit, S, prop

EP = {"id": "za_ep08", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "sandy": {"voice": "af_sarah", "speed": .82, "pitch": 3, "formant": 1.1, "gain": .88},
               "tumble": {"voice": "am_puck", "speed": .85, "pitch": 5, "formant": 1.16, "gain": .66}},
      "title": "The Long Walk to the Oasis", "thumb_text": "STEP BY STEP",
      "series": "Milo's Zoo Adventures",
      "description": ("Oh no! The little tree in the zoo garden is droopy and thirsty, and the watering can is empty. Milo the bluebird, Sandy the baby camel "
                      "and Tumble the baby elephant set off across the desert to bring back water. Tired wings, a hot sun, soft sand and heavy jugs! "
                      "Who can carry the water all the way home? A gentle animal adventure for ages 2-6 about helping friends, with questions to answer, "
                      "a count-along and a tune to clap along to.\n"
                      "Kids see how a very thirsty camel can drink 30 gallons of water in only 13 minutes, how grown-up camels can carry big, heavy loads "
                      "and walk a long way, and how a camel can go a week or more without water.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNational Geographic (Arabian camel); San Diego Zoo Wildlife Alliance (camel); World Wildlife Fund (camels)."),
      "tags": ["baby camel", "camel for kids", "desert animals for kids", "how much water does a camel drink", "oasis", "baby elephant", "animal stories for kids",
               "friendship story for kids", "kids adventure cartoon", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "zoo": [("tumble", "tumble", 360, 936, .6), ("sandy", "calf", 900, 935, .52), ("milo", "milo", 1290, 540, .72, False, True)],
    "dunes": [("tumble", "tumble", 300, 936, .6), ("sandy", "calf", 960, 935, .54), ("milo", "milo", 1420, 520, .72, False, True)],
    "trail": [("tumble", "tumble", 360, 932, .58), ("sandy", "calf", 1000, 932, .52)],
    "oasis": [("tumble", "tumble", 360, 936, .58), ("sandy", "calf", 1560, 935, .54, True), ("milo", "milo", 960, 420, .7, False, True)],
    "dune_eve": [("tumble", "tumble", 330, 935, .6), ("sandy", "calf", 1000, 935, .54)],
    "zoo_eve": [("tumble", "tumble", 330, 940, .6), ("sandy", "calf", 860, 940, .52), ("milo", "milo", 1390, 560, .68, False, True)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)

# Milo on Sandy's back (on top of the pack when she carries one) and the pack of two jugs: both stand on the calf's "back" point
def BACK(sx, sy=935, s=.54, pk=True): return ("milo", "milo", round(sx - 30 * s), round(sy - 470 * s - (26 if pk else 0)), .4)
def RIDE(sx, sy=935, s=.54, pk=True): return [("sandy", "calf", sx, sy, s), BACK(sx, sy, s, pk)]
def PACK(sx, sy=935, s=.54, hidden=False, name="pk"): return prop(name, A.pack, sx, round(sy - 470 * s + 6), round(s * .9, 3), hidden)
def CARRY(at, dx, d, extra=("pk",)):      # whatever rides on Sandy's back goes along with her walk
    return ("to", at, ",".join("#{p}%s_w" % n for n in extra), {"x": "+=%d" % dx, "duration": d, "ease": "none"}, "")
TREE = lambda x=1560, y=905, s=.9, glad=False: prop("tr", A.tree, x, y, s)
GLAD = lambda at: [("to", at, "#{p}tr-sad", {"opacity": 0, "duration": .6}, "the droopy leaves go"), ("to", at, "#{p}tr-glad", {"opacity": 1, "duration": .8}, "the tree is green and happy")]
GLAD_NOW = [("fromto", 0, "#{p}tr-sad", {"opacity": 0}, {"opacity": 0, "duration": .01}, ""), ("fromto", 0, "#{p}tr-glad", {"opacity": 1}, {"opacity": 1, "duration": .01}, "")]
DROOP = lambda at: ("to", at, "#{p}tr-sad", {"rotation": 3, "transformOrigin": "50% 100%", "duration": .5, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "the leaves droop")
EARS = lambda at, who="tumble", n=7: ("to", at, "#{p}%s-ear" % who, {"rotation": -16, "svgOrigin": "250 -590", "duration": .2, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "Tumble flaps his ears")
HOT = lambda x, y, s=.7: prop("sun", art3.hot_sun, x, y, s)
SPIN = ("to", 0.05, "#{p}sun-rays", {"rotation": 30, "transformOrigin": "50% 50%", "duration": 4, "ease": "none"}, "")
MCL = lambda place, dx=0, dy=-70, w=820, stage=None: C(place, "milo", "body", w, dx, dy, stage=stage)     # Milo asks a question: low in the frame, under the signs

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. Nobody sings: the rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_STEP = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~ ~", "notes": "C4:1 E4:1 G4:1 E4:1 D4:1 G4:1 B4:1", "rest": 1},     # step by step (C bar), slow and steady (G bar)
                                 {"text": "~ ~ ~ ~ ~ ~ ~", "notes": "A4:1 F4:1 C5:1 A4:1 G4:1 E4:1 C4:1", "rest": 1}])    # here comes water (F bar), tree, get ready (C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "G4:1 B4:1 D5:1 B4:1 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune

CNT_JUG = .32                                    # seconds from "One" to the last number, read from the timing file
ZOO_RIDE = RIDE(900, 935, .52, False)
DUNE_RIDE = RIDE(960, 935, .54, False)
EVE_RIDE = RIDE(1000)
ROCK_X = 1640
SHADE = [("tumble", "tumble", 430, 932, .58), ("sandy", "calf", 1200, 932, .52)]

SHOTS = [
    # ------------------------------------------------------------ HOOK: the little tree is thirsty, in the first 5 seconds
    S("zoo", (1400, 640, 1100), "Oh no! Our little tree is droopy. It is so thirsty!", beat="hook", tag="hook: the droopy tree", hide=["tumble", "sandy"], move={"milo": (1180, 760, .72)},
      props=[TREE()], fx=[("face", 0.02, "milo", "wow"), DROOP("w:droopy."), ("face", "w:thirsty!", "milo", "sad")],
      words=[("w:thirsty!", "THIRSTY!", .72, .2, 1.0, "sun")]),
    S("zoo", WIDE, "Hello, I'm Milo! This is our zoo garden, with Sandy the baby camel, and Tumble the baby elephant.", tag="zoo wide: Milo, Sandy, Tumble", cam2=(980, 560, 1820),
      props=[TREE()], fx=[("hop", "w:Hello,", "milo"), ("hop", "w:Sandy", "sandy"), ("nod", "w:Tumble", "tumble")],
      words=[("w:Sandy", "SANDY", .47, .3, .7, "pill"), ("w:Tumble", "TUMBLE", .2, .3, .7, "pill")]),
    S("zoo", C("zoo", "tumble", "head", 900, 40, 40), "I'll water it! Oh. The watering can is empty.", who="tumble", tag="Tumble: the can is empty", hide=["sandy", "milo"],
      props=[prop("cn", A.can, *P("zoo", "tumble", "tip", 60, 70), .5)],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:water", "tumble", -40, .4), ("to", "w:Oh.", "#{p}cn", {"rotation": 20, "svgOrigin": "0 0", "duration": .4}, "the can tips: nothing"),
          ("face", "w:empty.", "tumble", "sad")], words=[("w:empty.", "EMPTY!", .7, .2, 1.0, "pill")]),
    # ------------------------------------------------------------ GOAL
    S("zoo", C("zoo", "sandy", "head", 820, -40, 30), "Our tree needs water every day, and we have none left.", who="sandy", tag="Sandy: none left", hide=["tumble", "milo"],
      fx=[("face", 0.02, "sandy", "sad"), ("lookat", "w:tree", "sandy", 10), ("lookat", "w:none", "sandy", 0)], words=[("w:none", "NO WATER", .26, .2, .8, "pill")]),
    S("zoo", C("zoo", "sandy", "all", 900, 40, -60), "The oasis has lots of water. Let's walk there, and bring some back for the tree!", who="sandy", beat="goal", tag="goal: to the oasis", hide=["tumble", "milo"],
      fx=[("face", 0.02, "sandy", "happy"), ("hop", "w:walk", "sandy"), ("nod", "w:tree!", "sandy")], words=[("w:oasis", "TO THE OASIS!", .3, .2, .75, "sun")]),
    S("zoo", (1000, 640, 1500), "Mama camel puts two little jugs on Sandy's back. Stay together, and be home by supper.", beat="goal", tag="Mama gives the jugs",
      actors=[("mama", "camel", 1420, 905, .8, True), ("sandy", "calf", 760, 935, .52)], props=[PACK(760, 935, .52, True)],
      fx=[("lookat", "w:puts", "mama", 18), ("show", "w:jugs", "pk"), ("lookat", "w:Stay", "mama", 0), ("nod", "w:together,", "mama"), ("nod", "w:supper.", "sandy")],
      words=[("w:together,", "STAY TOGETHER", .3, .2, .7, "pill")]),
    S("zoo", MCL("zoo", 40), "Is the little tree happy, or thirsty?", q=True, beat="goal", tag="question: happy or thirsty", pause=3.2, hide=["tumble", "sandy"],
      fx=[("signs", "w:happy,", ["HAPPY", "THIRSTY"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ off over the dunes
    S("zoo", C("zoo", "tumble", "all", 1000, 40, -60), "Bye, Mama camel! We'll be back by supper!", who="tumble", beat="goal", tag="Tumble: bye, Mama", hide=["sandy", "milo"],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:Bye,", "tumble", -90, .4), ("trunk", "w:back", "tumble", 0, .4)], words=[("w:Bye,", "BYE-BYE!", .74, .2, .9, "sun")]),
    S("dunes", WIDE, "Off they go, over the dunes. The oasis is far, far away.", trans="iris", beat="goal", tag="over the dunes", cam2=(980, 560, 1820),
      move={"tumble": (-460, 936, .6), "sandy": (380, 935, .54), "milo": (-200, 440, .72)}, props=[PACK(380, 935, .54)],
      fx=[("walk", 0.1, "tumble", 760, 4.0), ("walk", 0.1, "sandy", 580, 4.0), CARRY(0.1, 580, 4.0), ("fly", 0.1, "milo", 1420, 520, 4.0)],
      words=[("w:go,", "OFF WE GO!", .3, .2, .85, "sun"), ("w:far,", "SO FAR!", .55, .32, .85, "pill")]),
    S("dunes", (920, 640, 1300), "How many jugs does Sandy carry? Count with me! One. Two!", q=True, beat="goal", tag="question: count the jugs", pause=1.0,
      actors=[("sandy", "calf", 1060, 935, .6), ("milo", "milo", 640, 600, .72, False, True)], props=[PACK(1060, 935, .6)],
      fx=[("count", "w:One.", 2, CNT_JUG, {"x": 1000, "y": 330}), ("to", "w:One.", "#{p}pk_w", {"y": "-=12", "duration": .15, "yoyo": True, "repeat": 1}, ""),
          ("to", "w:Two!", "#{p}pk_w", {"y": "-=12", "duration": .15, "yoyo": True, "repeat": 1}, "")]),
    # ------------------------------------------------------------ OBSTACLE 1: Milo's wings get tired
    S("dunes", C("dunes", "milo", "body", 820, 40, -20), "Flap, flap, flap. Phew! My wings are tired.", beat="obstacle1", tag="Milo: tired wings", hide=["tumble", "sandy"],
      fx=[("face", 0.02, "milo", "happy"), ("fly", "w:Phew!", "milo", 1400, 600, 1.2), ("face", "w:tired.", "milo", "sleepy")],
      words=[("w:Flap,", "FLAP, FLAP!", .26, .2, .85, "sun"), ("w:tired.", "TIRED!", .74, .22, .9, "pill")]),
    S("dunes", C("dunes", "sandy", "all", 980, 60, -60), "Rest on my back, Milo! I can carry a little bird.", who="sandy", beat="obstacle1", tag="Sandy: rest on my back", hide=["tumble", "milo"],
      props=[PACK(960, 935, .54)], fx=[("face", 0.02, "sandy", "happy"), ("nod", "w:back,", "sandy")], words=[("w:back,", "HOP ON!", .3, .2, .9, "sun")]),
    S("dunes", (960, 640, 1500), "Milo lands softly on Sandy's back. Ahh, that's better!", beat="obstacle1", tag="Milo lands on Sandy", hide=["tumble"],
      props=[PACK(960, 935, .54)], fx=[("to", "w:lands", "#{p}milo_w", {"x": BACK(960)[2], "y": BACK(960)[3], "duration": .9, "ease": "power2.inOut"}, "Milo lands on her back"),
                                     ("to", "w:lands", "#{p}milo", {"scale": .4 / .72, "svgOrigin": "0 0", "duration": .9}, ""), ("face", "w:Ahh,", "milo", "happy")],
      words=[("w:better!", "AHH!", .7, .2, .9, "sun")]),
    S("dunes", MCL("dunes", 0, -40, 760, stage=RIDE(960)), "Who is carrying Milo now? Sandy, or Tumble?", q=True, beat="obstacle1", tag="question: Sandy or Tumble", pause=3.2,
      actors=RIDE(960), props=[PACK(960, 935, .54)], fx=[("signs", "w:Sandy,", ["SANDY", "TUMBLE"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 2: Tumble gets hot (they rest in the shade of a big rock)
    S("trail", WIDE, "On the rocky trail, the sun is hot, hot, hot.", trans="iris", beat="obstacle2", tag="the hot rocky trail", cam2=(980, 560, 1820),
      actors=[("tumble", "tumble", 60, 932, .58)] + RIDE(700, 932, .52),
      props=[HOT(1520, 220), prop("rk", A7.rock, ROCK_X, 935, .9), prop("ht", art3.heat, 800, 560, .9, True), PACK(700, 932, .52)],
      fx=[SPIN, ("walk", 0.1, "tumble", 300, 3.0), ("walk", 0.1, "sandy", 300, 3.0), CARRY(0.1, 300, 3.0, ("pk", "milo")), ("show", "w:hot,", "ht")],
      words=[("w:hot,", "HOT!", .5, .2, 1.0, "sun")]),
    S("trail", C("trail", "tumble", "head", 860, 40, 30), "Phew! I'm so hot. My big ears go flap, flap, like fans!", who="tumble", beat="obstacle2", tag="Tumble: so hot", hide=["sandy"],
      props=[prop("sw", art3.sweat, *P("trail", "tumble", "top", -60, 40), .5, True)],
      fx=[("face", 0.02, "tumble", "sad"), ("show", "w:hot.", "sw"), EARS("w:flap,")], words=[("w:hot.", "SO HOT!", .74, .2, .9, "pill")]),
    S("trail", C("trail", "sandy", "all", 900, 40, -60, stage=RIDE(1000, 932, .52)), "Let's rest in the shade of the big rock.", who="milo", beat="obstacle2", tag="Milo: rest in the shade",
      actors=RIDE(1000, 932, .52), props=[PACK(1000, 932, .52)], fx=[("hop", "w:rest", "milo"), ("lookat", "w:rock.", "sandy", -6)],
      words=[("w:shade", "SHADE!", .16, .3, .9, "sun")]),
    S("trail", (1060, 700, 1600), "They sit down in the cool shade. Tumble flaps his ears, and soon he feels better.", beat="obstacle2", tag="resting in the shade",
      actors=SHADE + [("milo", "milo", 965, 930, .7)], fly=[],
      props=[prop("sh", art3.shade, 990, 950, 1.3), prop("rk", A7.rock, ROCK_X, 935, .9), prop("sw", art3.sweat, 560, 600, .45)],
      fx=[("face", 0.02, "tumble", "sleepy"), EARS("w:flaps"), ("hide", "w:better.", "sw"), ("face", "w:better.", "tumble", "happy"), ("hop", "w:better.", "milo")],
      words=[("w:cool", "COOL SHADE", .3, .2, .75, "pill")]),
    S("trail", C("trail", "tumble", "head", 860, 40, 30, stage=SHADE), "Can you flap your ears like Tumble? Flap, flap, flap!", q=True, beat="obstacle2", tag="flap along", actors=SHADE, hide=["sandy"],
      fx=[("face", 0.02, "tumble", "happy"), EARS("w:Flap,", n=11)], words=[("w:Flap,", "FLAP, FLAP!", .74, .2, .85, "sun")]),
    S("trail", MCL("trail", 0, -60, 760, stage=SHADE + [("milo", "milo", 965, 930, .7)]), "Where is it cool? In the sun, or in the shade?", q=True, beat="obstacle2", tag="question: sun or shade", pause=3.2,
      actors=SHADE + [("milo", "milo", 965, 930, .7)], fly=[], hide=["tumble", "sandy"], props=[prop("sh", art3.shade, 990, 950, 1.3)],
      fx=[("signs", "w:sun,", ["SUN", "SHADE"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ the oasis: a big drink (fact 1), the jugs are filled
    S("oasis", WIDE, "At last, the oasis! Cool blue water, and tall palm trees.", trans="iris", beat="goal", tag="the oasis wide", cam2=(980, 560, 1820),
      props=[PACK(1560, 935, .54)], fx=[("hop", "w:last,", "milo"), ("hop", "w:water,", "tumble"), ("nod", "w:trees.", "sandy")],
      words=[("w:oasis!", "THE OASIS!", .5, .2, .95, "sun")]),
    S("oasis", (980, 620, 1660), "Tumble drinks with his trunk. Slurp! And Sandy drinks, and drinks, and drinks.", beat="goal", tag="they drink", hide=["milo"],
      props=[PACK(1560, 935, .54)], fx=[("trunk", "w:drinks", "tumble", 50, .5), ("trunk", "w:Slurp!", "tumble", -60, .3), ("trunk", "w:And", "tumble", 0, .4),
                                        ("drink", "w:Sandy", "sandy", 3.0, 58)],
      words=[("w:Slurp!", "SLURP!", .3, .2, .9, "sun"), ("w:drinks.:4", "GULP, GULP!", .75, .2, .8, "pill")]),
    S("oasis", C("oasis", "milo", "body", 760, 0, -10, stage=[("milo", "milo", 460, 985, .7)]), "Milo has a tiny sip. A little bird needs only a little drink.", tag="Milo sips",
      actors=[("milo", "milo", 460, 985, .7)], fly=[], fx=[("to", "w:sip.", "#{p}milo", {"rotation": 18, "svgOrigin": "0 0", "duration": .3, "yoyo": True, "repeat": 1}, "Milo sips"), ("hop", "w:little", "milo")],
      words=[("w:sip.", "SIP!", .74, .22, 1.0, "sun")]),
    S("paper_blue", (960, 540, 1500), "A very thirsty camel can drink thirty gallons of water, in only thirteen minutes!", beat="fact", tag="fact: thirty gallons in thirteen minutes",
      props=[prop("jg", A.jug_grid, 960, 600, .9), prop("ck", art.clock, 1590, 230, .5, True)],
      fx=[("fromto", 0, "#{p}jg-r1,#{p}jg-r2", {"opacity": 0}, {"opacity": 0, "duration": .01}, ""),
          ("to", "w:thirty", "#{p}jg-r0", {"scale": 1.04, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 1}, "ten jugs"), ("to", "w:gallons", "#{p}jg-r1", {"opacity": 1, "duration": .25}, "ten more"),
          ("to", "w:water,", "#{p}jg-r2", {"opacity": 1, "duration": .25}, "thirty jugs"), ("show", "w:thirteen", "ck"),
          ("fromto", "w:thirteen", "#{p}ck-min", {"rotation": 0, "svgOrigin": "0 0"}, {"rotation": 78, "duration": 1.4, "ease": "power1.inOut"}, "the clock turns")],
      words=[("w:thirty", "30 GALLONS", .26, .14, .8, "sun"), ("w:thirteen", "13 MINUTES", .64, .14, .7, "pill")]),
    S("oasis", MCL("oasis", 0, -40, 800), "Which is more water? One jug, or thirty jugs?", q=True, beat="goal", tag="question: one or thirty jugs", pause=3.2, hide=["tumble", "sandy"],
      fx=[("signs", "w:One", ["1 JUG", "30 JUGS"], 1, "wait:1.8")]),
    S("oasis", C("oasis", "sandy", "all", 900, -60, -60), "Glug, glug! Milo helps fill the two little jugs, all the way to the top.", beat="goal", tag="filling the jugs", hide=["tumble"],
      actors=[("tumble", "tumble", 250, 936, .58), ("sandy", "calf", 1560, 935, .54, True), ("milo", "milo", 1770, 730, .6, False, True)],
      props=[PACK(1560, 935, .54), prop("fl", A.pond_fill, 1560, 722, .5, True)],
      fx=[("show", "w:Glug,", "fl"), ("fromto", "w:Glug,", "#{p}fl", {"y": -20}, {"y": 30, "duration": .5, "repeat": 5, "ease": "none"}, "water pours in"), ("hide", "w:top.", "fl"), ("hop", "w:top.", "milo")],
      words=[("w:Glug,", "GLUG, GLUG!", .26, .2, .85, "sun"), ("w:top.", "FULL!", .15, .55, .9, "pill")]),
    # ------------------------------------------------------------ OBSTACLE 3: the way back - soft sand, heavy jugs
    S("dune_eve", WIDE, "On the way back, the sand is soft and deep. And the jugs are heavy now.", trans="iris", beat="obstacle3", tag="the way back: soft sand", cam2=(1000, 560, 1820),
      actors=[("tumble", "tumble", 330, 935, .6), ("sandy", "calf", 1000, 935, .54), ("milo", "milo", 1560, 600, .7, False, True)],
      move={"tumble": (-420, 935, .6), "sandy": (400, 935, .54)}, props=[PACK(400, 935, .54)],
      fx=[("walk", 0.1, "tumble", 620, 4.0), ("walk", 0.1, "sandy", 400, 4.0), CARRY(0.1, 400, 4.0), ("to", "w:heavy", "#{p}pk", {"y": 8, "duration": .3, "yoyo": True, "repeat": 3}, "the jugs sway")],
      words=[("w:soft", "SOFT SAND", .3, .2, .8, "pill"), ("w:heavy", "HEAVY!", .64, .2, .9, "sun")]),
    S("dune_eve", C("dune_eve", "tumble", "head", 900, 60, 60), "I'll carry a jug with my trunk! Oh, oh! It wobbles. Splish!", who="tumble", beat="obstacle3", tag="Tumble: the jug wobbles", hide=["sandy"],
      props=[prop("j1", art.jug, *P("dune_eve", "tumble", "tip", 10, 110), .9), prop("sp", lambda p: art3.splash(p, ("#7fd3f7", "#2b7fb0", "#ffffff")), *P("dune_eve", "tumble", "tip", 60, 40), .5, True)],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:trunk!", "tumble", -30, .4), ("to", "w:wobbles.", "#{p}j1", {"rotation": 14, "svgOrigin": "0 -120", "duration": .15, "yoyo": True, "repeat": 7}, "the jug wobbles"),
          ("show", "w:Splish!", "sp"), ("face", "w:Splish!", "tumble", "wow")], words=[("w:Splish!", "SPLISH!", .74, .2, 1.0, "sun")]),
    S("dune_eve", (1300, 760, 1100), "I'll carry one! Ooh, it's too heavy for a little bird.", beat="obstacle3", tag="Milo: too heavy",
      actors=[("milo", "milo", 1260, 935, .72)], fly=[], props=[prop("j1", art.jug, 1420, 935, 1.1)],
      fx=[("face", 0.02, "milo", "happy"), ("to", "w:Ooh,", "#{p}milo", {"rotation": 8, "svgOrigin": "0 0", "duration": .15, "yoyo": True, "repeat": 5}, "Milo pulls"),
          ("face", "w:heavy", "milo", "wow")], words=[("w:heavy", "TOO HEAVY!", .3, .2, .85, "pill")]),
    S("dune_eve", MCL("dune_eve", 0, -60, 800, stage=[("milo", "milo", 1260, 935, .72)]), "Is a full jug heavy, or light?", q=True, beat="obstacle3", tag="question: heavy or light", pause=3.2,
      actors=[("milo", "milo", 1260, 935, .72)], fly=[], props=[prop("j1", art.jug, 1420, 935, 1.1)], fx=[("signs", "w:heavy,", ["HEAVY", "LIGHT"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ LOW MOMENT: on the sandy hill, the zoo far away (gentle: nobody cries)
    S("dune_eve", (960, 620, 1600), "They sit down on the sandy hill. The sun is low, and the zoo is still far away.", beat="low", tag="sitting on the hill",
      actors=[("tumble", "tumble", 400, 935, .6), ("sandy", "calf", 1290, 935, .54), ("milo", "milo", 945, 935, .7)], fly=[], props=[PACK(1290, 935, .54)],
      fx=[("face", "w:sit", "milo", "sad"), ("face", "w:sit", "tumble", "sad"), ("to", "w:sit", "#{p}sandy", {"y": 10, "duration": .5}, "Sandy settles")],
      words=[("w:far", "SO FAR...", .5, .2, .85, "pill")]),
    S("dune_eve", C("dune_eve", "milo", "body", 700, 0, -20, stage=[("milo", "milo", 945, 935, .7)]), "Tumble is hot, my wings are tired, and the jugs are so heavy.", beat="low", tag="Milo: so heavy",
      actors=[("milo", "milo", 945, 935, .7)], fly=[], fx=[("face", 0.02, "milo", "sad")], words=[("w:heavy.", "SO HEAVY", .74, .22, .75, "pill")]),
    S("dune_eve", C("dune_eve", "tumble", "head", 860, 40, 40, stage=[("tumble", "tumble", 400, 935, .6)]), "Maybe our little tree can't have a drink today.", who="tumble", beat="low", tag="Tumble: maybe not today",
      actors=[("tumble", "tumble", 400, 935, .6)], fx=[("face", 0.02, "tumble", "sad"), ("trunk", "w:drink", "tumble", 30, .6)]),
    S("dune_eve", C("dune_eve", "sandy", "head", 800, -40, 40, stage=[("sandy", "calf", 1290, 935, .54)]), "Don't worry, friends. We are together. Let me think.", who="sandy", beat="low", tag="Sandy: let me think",
      actors=[("sandy", "calf", 1290, 935, .54)], props=[PACK(1290, 935, .54)], fx=[("face", 0.02, "sandy", "sad"), ("lookat", "w:think.", "sandy", -12)],
      words=[("w:think.", "HMM...", .26, .2, 1.0, "pill")]),
    S("dune_eve", MCL("dune_eve", 0, -60, 760, stage=[("milo", "milo", 945, 935, .7)]), "Who can carry the heavy jugs? Milo, or Sandy?", q=True, beat="low", tag="question: Milo or Sandy", pause=3.2,
      actors=[("milo", "milo", 945, 935, .7)], fly=[], fx=[("signs", "w:Milo,", ["MILO", "SANDY"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: Sandy works it out herself (fact 2), and carries the jugs home
    S("dune_eve", C("dune_eve", "sandy", "all", 900, 40, -60, stage=[("sandy", "calf", 1290, 935, .54)]), "I know! Camels are made for carrying, and for walking far. I can carry the jugs, step by step!", who="sandy",
      beat="solution", tag="Sandy: I know!", actors=[("sandy", "calf", 1290, 935, .54)], props=[PACK(1290, 935, .54)],
      fx=[("face", 0.02, "sandy", "happy"), ("hop", "w:know!", "sandy"), ("nod", "w:step,", "sandy")], words=[("w:know!", "I KNOW!", .3, .2, .9, "sun")]),
    S("paper", (960, 560, 1500), "Grown-up camels can carry big, heavy loads, and walk a long way every day.", beat="fact", tag="fact: camels carry heavy loads",
      actors=[("mama", "camel", 760, 900, .72)], props=[prop("bp", A.big_pack, 760, 900 - 440 * .72 + 8, .72), prop("f1", lambda p: art.footprint(p), 1180, 860, .6, True),
                                                     prop("f2", lambda p: art.footprint(p), 1360, 800, .6, True), prop("f3", lambda p: art.footprint(p), 1540, 740, .6, True)],
      fx=[("to", "w:heavy", "#{p}bp", {"y": -10, "duration": .25, "yoyo": True, "repeat": 3}, "the big load"),
          ("show", "w:walk", "f1"), ("show", "w:long", "f2"), ("show", "w:way", "f3"), ("nod", "w:day.", "mama")],
      words=[("w:heavy", "HEAVY LOADS", .26, .14, .8, "sun"), ("w:long", "A LONG WAY", .76, .3, .7, "pill")]),
    S("dune_eve", (1000, 640, 1700), "Milo hops on top. Tumble walks beside her. Step, step, step, slow and steady.", beat="solution", tag="step step step",
      actors=[("tumble", "tumble", 420, 935, .6)] + EVE_RIDE, props=[PACK(1000)],
      fx=[("walk", "w:Tumble", "tumble", 420, 4.0), ("walk", "w:Tumble", "sandy", 420, 4.0), CARRY("w:Tumble", 420, 4.0, ("pk", "milo")), ("hop", "w:hops", "milo")],
      words=[("w:Step,", "STEP, STEP!", .26, .2, .85, "sun"), ("w:steady.", "SLOW AND STEADY", .62, .12, .6, "pill")]),
    S("dune_eve", C("dune_eve", "tumble", "head", 860, 40, 40), "Sandy, aren't you thirsty?", who="tumble", beat="solution", tag="Tumble: aren't you thirsty?", hide=["sandy"],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:thirsty?", "tumble", -40, .4)]),
    S("dune_eve", C("dune_eve", "sandy", "head", 820, -40, 30, stage=EVE_RIDE), "Not yet! I had a big drink at the oasis.", who="sandy", beat="solution", tag="Sandy: not yet",
      actors=EVE_RIDE, props=[PACK(1000)], fx=[("face", 0.02, "sandy", "happy"), ("nod", "w:yet!", "sandy")], words=[("w:big", "BIG DRINK!", .26, .2, .85, "sun")]),
    S("paper_pink", (960, 540, 1500), "A camel can go a week or more without water!", beat="fact", tag="fact: a week without water",
      props=[prop("wk", art.week, 960, 600, 1.15), prop("dr", lambda p: art.water_drop(p), 960, 330, .9)],
      fx=[("fromto", "w:week", ".{p}wk-d", {"opacity": .25}, {"opacity": 1, "duration": .2, "stagger": .22}, "seven days, one by one"),
          ("to", "w:more", "#{p}dr_w", {"scale": 1.1, "duration": .2, "yoyo": True, "repeat": 3}, "")],
      words=[("w:week", "1 WEEK", .2, .16, 1.0, "sun"), ("w:more", "OR MORE!", .8, .16, .8, "pill")]),
    S("dune_eve", C("dune_eve", "milo", "body", 640, 0, -10, stage=EVE_RIDE), "Wow! A whole week!", tag="Milo: a whole week", actors=EVE_RIDE, props=[PACK(1000)],
      fx=[("face", 0.02, "milo", "wow"), ("hop", "w:week!", "milo")], words=[("w:week!", "WOW!", .74, .2, 1.0, "sun")]),
    S("dune_eve", MCL("dune_eve", 0, -40, 760, stage=EVE_RIDE), "Can a camel go a week without water? Yes, or no?", q=True, beat="solution", tag="question: a week yes or no", pause=3.2,
      actors=EVE_RIDE, props=[PACK(1000)], fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ SONG MOMENT: the rhyme SAID by Sandy, then the tune on instruments while they walk home
    S("dune_eve", (1000, 640, 1700), "Can you walk slow and steady, like Sandy? Step, step, step!", q=True, beat="solution", tag="walk along",
      actors=[("tumble", "tumble", 420, 935, .6)] + EVE_RIDE, props=[PACK(1000)],
      fx=[("walk", "w:Step,", "tumble", 240, 2.4), ("walk", "w:Step,", "sandy", 240, 2.4), CARRY("w:Step,", 240, 2.4, ("pk", "milo"))], words=[("w:Step,", "STEP, STEP!", .26, .2, .85, "sun")]),
    S("dune_eve", C("dune_eve", "sandy", "all", 1100, 0, -80, stage=EVE_RIDE), "Step by step, slow and steady. Here comes water! Tree, get ready!", who="sandy", beat="solution", tag="the step rhyme",
      actors=EVE_RIDE, props=[PACK(1000)], fx=[("face", 0.02, "sandy", "happy"), ("nod", "w:Step", "sandy"), ("hop", "w:water!", "milo"), ("nod", "w:ready!", "sandy")],
      words=[("w:Step", "STEP BY STEP", .26, .2, .7, "sun"), ("w:Here", "HERE COMES WATER!", .7, .2, .6, "pill")]),
    S("dune_eve", (760, 620, 1500), who="", sing=SING_STEP, beat="song", tag="song: step by step", actors=[("tumble", "tumble", 220, 935, .6)] + RIDE(760), cam2=(1240, 620, 1500),
      props=[PACK(760)],
      fx=[("walk", TB(0), "tumble", 760, 9.6), ("walk", TB(0), "sandy", 760, 9.6), CARRY(TB(0), 760, 9.6, ("pk", "milo")), ("hop", TB(4), "milo"), ("hop", TB(12), "milo"),
          ("word", TB(0), "STEP BY STEP!", {"x": 760, "y": 300, "size": 80, "cls": "sun", "hold": 4.4})],
      words=[(TB(8), "SLOW AND STEADY!", .8, .14, .7, "pill")]),
    # ------------------------------------------------------------ WARM ENDING: home at the zoo, the tree drinks
    S("zoo_eve", WIDE, "Back at the zoo, the little tree is waiting.", trans="iris", beat="ending", tag="back at the zoo", cam2=(980, 560, 1820),
      actors=[("tumble", "tumble", -420, 940, .6)] + RIDE(300, 940, .52), props=[PACK(300, 940, .52), TREE(1620, 920)],
      fx=[("walk", 0.1, "tumble", 720, 3.0), ("walk", 0.1, "sandy", 560, 3.0), CARRY(0.1, 560, 3.0, ("pk", "milo")), DROOP("w:waiting.")],
      words=[("w:zoo,", "HOME!", .3, .2, 1.0, "sun")]),
    S("zoo_eve", (1340, 700, 1300), "Tumble pours the water. Glug, glug, glug! The little tree drinks.", beat="ending", tag="Tumble waters the tree",
      actors=[("tumble", "tumble", 950, 940, .6)], props=[TREE(1620, 920), prop("cn", A.can, 1350, 860, .6)],
      fx=[("trunk", "w:pours", "tumble", -30, .4), ("to", "w:pours", "#{p}cn", {"rotation": 26, "svgOrigin": "0 0", "duration": .4}, "the can tips"),
          ("to", "w:Glug,", "#{p}cn-pour", {"opacity": 1, "duration": .2}, "water pours"), ("fromto", "w:Glug,", "#{p}cn-pour", {"y": -10}, {"y": 20, "duration": .4, "repeat": 5, "ease": "none"}, ""),
          ("hide", "w:drinks.", "cn")], words=[("w:Glug,", "GLUG, GLUG!", .26, .2, .85, "sun")]),
    S("zoo_eve", (1620, 640, 1000), "Look! Its leaves stand up, green and happy!", beat="ending", tag="the tree is happy", hide=["tumble", "sandy", "milo"],
      props=[TREE(1620, 920)], fx=GLAD("w:leaves") + [("to", "w:happy!", "#{p}tr_w", {"scale": .95, "duration": .2, "yoyo": True, "repeat": 1}, "")],
      words=[("w:happy!", "HAPPY TREE!", .26, .2, .85, "sun")]),
    S("zoo_eve", MCL("zoo_eve", 0, -40, 800), "How does the little tree look now? Droopy, or happy?", q=True, beat="ending", tag="question: droopy or happy", pause=3.2, hide=["tumble", "sandy"],
      fx=[("signs", "w:Droopy,", ["DROOPY", "HAPPY"], 1, "wait:1.8")]),
    S("zoo_eve", (980, 600, 1500), "Mama camel nuzzles Sandy. She is so proud of her.", beat="ending", tag="Mama nuzzles Sandy",
      actors=[("mama", "camel", 1260, 905, .82, True), ("sandy", "calf", 660, 940, .52)],
      props=[prop("h1", lambda p: art2.heart(p), 980, 330, .7, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 1060, 300, .5, True)],
      fx=[("lookat", "w:nuzzles", "mama", 20), ("lookat", "w:nuzzles", "sandy", -8), ("show", "w:nuzzles", "h1"), ("show", "w:proud", "h2"),
          ("to", "w:proud", "#{p}h1_w,#{p}h2_w", {"y": "-=60", "duration": 1.6, "ease": "sine.out"}, "")],
      words=[("w:proud", "SO PROUD!", .26, .2, .8, "sun")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 760, 0, -10), "Thank you, Sandy. You carried the water all the way!", beat="ending", tag="Milo: thank you", hide=["tumble", "sandy"],
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:way!", "milo")], words=[("w:way!", "ALL THE WAY!", .74, .22, .75, "sun")]),
    S("zoo_eve", C("zoo_eve", "tumble", "head", 860, 40, 40), "And we all helped, together!", who="tumble", beat="ending", tag="Tumble: together", hide=["sandy", "milo"],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:together!", "tumble", -90, .5)]),
    S("zoo_eve", C("zoo_eve", "sandy", "head", 820, -40, 30), "Thank you for walking with me, Tumble and Milo!", who="sandy", beat="ending", tag="Sandy: thank you", hide=["tumble", "milo"],
      fx=[("face", 0.02, "sandy", "happy"), ("nod", "w:Tumble", "sandy")], words=[("w:Thank", "THANK YOU!", .26, .2, .85, "sun")]),
    S("zoo_eve", (1000, 600, 1760), "Little steps can go a long, long way, when friends help each other.", beat="ending", tag="the lesson", cam2=(1040, 600, 1700),
      props=[TREE(1620, 920)], fx=GLAD_NOW + [("hop", "w:Little", "milo"), ("nod", "w:steps", "sandy"), ("trunk", "w:long,", "tumble", -80, .4), ("hop", "w:friends", "sandy"), ("hop", "w:other.", "milo")],
      words=[("w:friends", "FRIENDS HELP", .5, .16, .6, "sun")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 40, 0), "Do you remember? How long can a camel go without water? A week, or a year?", q=True, beat="ending", tag="question: week or year", pause=3.2,
      hide=["tumble", "sandy"], cam2=C("zoo_eve", "milo", "body", 830, 40, -60), fx=[("hop", "w:remember?", "milo"), ("signs", "w:week,", ["A WEEK", "A YEAR"], 0, "wait:1.8")]),
    S("zoo_eve", C("zoo_eve", "sandy", "all", 1000, 60, -40), "Who carried the jugs home? Sandy, or Milo?", q=True, beat="ending", tag="question: who carried", pause=3.2,
      hide=["tumble", "milo"], cam2=C("zoo_eve", "sandy", "all", 940, 60, -60), fx=[("nod", "w:home?", "sandy"), ("signs", "w:Sandy,", ["SANDY", "MILO"], 0, "wait:1.8")]),
    S("zoo_eve", (960, 540, 1920), "Step by step, slow and steady. Here comes water! Tree, get ready!", beat="ending", tag="the closing rhyme", cam2=(980, 560, 1880),
      props=[TREE(1620, 920)], fx=GLAD_NOW + [("hop", "w:Step", "milo"), ("nod", "w:steady.", "sandy"), ("trunk", "w:water!", "tumble", -80, .4), ("hop", "w:ready!", "sandy")],
      words=[("w:Step", "STEP BY STEP", .5, .15, .7, "sun")]),
    S("zoo_eve", WIDE, who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(980, 560, 1880), props=[TREE(1620, 920)],
      fx=GLAD_NOW + [("hop", 1.0, "sandy"), ("trunk", 2.0, "tumble", -90, .4), ("hop", 2.2, "milo")], words=[(TB(3), "HOORAY!", .5, .2, 1.05, "sun")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 0, 0), "Next time: Sandy's first night away! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure", hide=["tumble", "sandy"],
      fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .24, .2, .72, "sun"), ("w:See", "SEE YOU SOON!", .24, .33, .62, "pill")]),
]

# thumbnail (thumb.py): the example in the picture (Sandy carrying the two jugs over a dune, Milo on top), 3 words at most, none of the title's words, no watermark
THUMBS = {
    "za_ep08": {"place": "dune_eve", "cam": (1080, 600, 1300),
                "actors": [("calf", 1000, 935, .62, False, ''), ("milo", 1000 - round(30 * .62), 935 - round(470 * .62) - 30, .44, False, '')],
                "props": [(A.pack, 1000, 935 - round(470 * .62) + 6, .56)],
                "words": [("STEP BY STEP", 1420, 160, 150, "sun", -4)]},
}
