"""za_ep15 - Milo's Zoo Adventures: "How Can Milo See Under the Deep Blue Sea?" (theme title "Milo and the Deep Blue Sea"; cartoon adventure, the 3D
music-and-sync process: "beat"). Ocean week, adventure 3.
Milo sits on his little rock in the sea. His friend Tula the sea turtle is going home, deep under the water, and Milo wants to see her home. But he
is a little bird: he needs air, he cannot go under the water (he is never under the water and never in it in this film). He tries three things from
the air: he looks down from his rock (the water is too deep, all he sees is the sun twinkling on the waves), he stands on a floating leaf (it goes
round and round, he gets dizzy and flies back to his rock), he calls (Tula is deep down and does not hear). Low moment: he sits on his rock, a
little sad, "maybe a little bird can never see under the sea" (nobody cries, nobody is lost, hurt or stuck). Then bubbles pop up beside the rock and
Tula comes up for air: sea turtles breathe air. Milo finds the idea himself: "I cannot go down, but you come up! Every time you come up for air, tell
me one thing you saw!" Tula dives to the coral garden, the seagrass meadow and her cozy bed by the big rocks, and each time she comes up for a
breath she tells Milo, who sees it in his head. Warm ending in the evening light, thank-yous, two recap questions, the rhyme and the tune.
The theme's premise had "a reed is too short" and "a jump is too splashy": both are things a child could copy in water (breathing through a reed,
jumping in), so they are not in the film; the leaf boat does not tip, it only turns.

FACTS, read at the source on Nov 27 2026, about 3:35 PM ET (each page fetched by the session's page reader, which quoted these sentences verbatim):
 [NOAA] NOAA Fisheries, "Green Turtle", fisheries.noaa.gov/species/green-turtle
   "Green turtles, like all sea turtles, are reptiles and must surface to breathe."
 [SI] Smithsonian Ocean, "Up for a Breath", ocean.si.edu/node/110298
   "Sea turtles, including this Kemp's ridley, must come to the surface to breathe air."
 [SI2] Smithsonian Ocean, "Sea Turtle Goes Up for Air", ocean.si.edu/node/110293
   "Even though they spend most of that time underwater, they still need to make trips to the surface to breathe."
 [ORP] Olive Ridley Project, "Can sea turtles breathe underwater?", oliveridleyproject.org/ufaqs/can-sea-turtles-breathe-underwater
   "Sea turtles cannot breathe underwater, however they can hold their breath for long periods of time."
 [ORP2] Olive Ridley Project, "How long can sea turtles hold their breath?", oliveridleyproject.org/ufaqs/how-long-can-sea-turtles-hold-their-breath
   "If they are sleeping, they can remain underwater for several hours."
 [SWOT] The State of the World's Sea Turtles, "How Long Can Sea Turtles Hold Their Breath?", seaturtlestatus.org/articles/2024/2/14/faq-how-long-can-sea-turtles-hold-their-breath
   "under most conditions, sea turtles will dive for 20 to 40 minutes while foraging and up to several hours when sleeping."
 Said as animal facts in the film (three fact shots, questions, recap): sea turtles breathe air and must come up to the surface to breathe [NOAA, SI];
 sea turtles cannot breathe under the water, but they can hold their breath for a long time [ORP]; a sleeping sea turtle can stay under the water for
 several hours [ORP2, SWOT].
 NOT said as facts: any number of minutes or hours, lungs or gills (no page sentence read today names them), how deep Tula's home is, what lives in a
 coral garden. That Milo, a bird, needs air and cannot go under the water is the story's own plain statement; Tula's "cozy bed" by the rocks is HER
 story (the pages say a sleeping sea turtle can stay under the water, not where). Zip and Pearl are the made-up little fish of za_ep12; they do not speak.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep12 as A
import art_za_ep13 as B
import art_za_ep15 as N
import kit
from kit import Kit, S, prop
from intro import INTRO_STAGES, intro_shots      # the main intro, right after the hook and as the last shots (owner, Nov 20 4:50 PM)

EP = {"id": "za_ep15", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "tula": {"voice": "bf_emma", "speed": .8, "gain": .8}},
      "title": "How Can Milo See Under the Deep Blue Sea?", "thumb_text": "DOWN THERE?",
      "series": "Milo's Zoo Adventures",
      "description": ("How can Milo see under the deep blue sea? His friend Tula the sea turtle lives down there, but Milo is a little bird: he needs air! "
                      "He looks from his rock, he tries a leaf boat, he calls as loud as he can... and then bubbles pop up, and Milo has a clever idea. "
                      "A gentle ocean adventure for ages 2-6 about finding another way when one way does not work, with questions to answer, a count-along and a little tune.\n"
                      "Kids see how sea turtles breathe air and must come up to the surface to breathe, how they can hold their breath for a long time, "
                      "and how a sleeping sea turtle can stay under the water for several hours.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNOAA Fisheries (green turtle); Smithsonian Ocean (sea turtles come up for a breath); "
                      "Olive Ridley Project (sea turtle questions and answers); The State of the World's Sea Turtles (how long sea turtles hold their breath)."),
      "tags": ["sea turtle for kids", "how do sea turtles breathe", "sea turtle", "ocean animals for kids", "under the sea", "ocean story for kids", "bluebird",
               "animal stories for kids", "friendship story for kids", "kids adventure cartoon", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

WL = N.WL
ROCK = B.ISLE_TOP                                  # (1560, 256): the top of Milo's little rock, in the air
MI = lambda x=ROCK[0], y=ROCK[1], s=.5: ("milo", "milo", x, y, s)
T = lambda x, y, s=.55, f=False: ("tula", "turtle", x, y, s, f)
TU = lambda x=1040, y=462, s=.58: ("tula", "turtle_up", x, y, s)      # Tula up for air: her head is out of the water beside the rock
Z = lambda x, y, s=.4, f=False: ("zip", "fish_zip", x, y, s, f)
PL = lambda x, y, s=.4, f=False: ("pearl", "fish_pearl", x, y, s, f)
LEAFX = 1040
ML = MI(LEAFX, WL - 8)                             # Milo on the leaf boat
STAGES = {
    "shore": [MI(), T(700, 700)],
    "deep": [T(820, 700, .6)],
    "reef": [T(860, 700, .58), Z(430, 520), PL(1500, 800, .4, True)],
    "meadow": [T(760, 730)],
    "rocks": [T(900, 800)],
    "shore_eve": [MI(), TU()],
    "paper_sea": [T(900, 800, .7)],
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
MCL = (ROCK[0], 170, 800)                          # Milo on his rock, close
MQ = (ROCK[0] - 60, 110, 920)                      # Milo low in the frame, under the answer signs
TOP2 = (1290, 330, 1100)                           # Milo on the rock and Tula's head out of the water
TUC = (1110, 290, 720)                             # Tula's head out of the water, close (the rock is out of the picture)
UPST = [MI(), TU()]
TCL = lambda place, w=1000, dx=0, dy=0, stage=None: C(place, "tula", "all", w, dx, dy, stage=stage)

SF = lambda: prop("sf", N.sea_front, 960, WL)
SFE = lambda: prop("sf", N.sea_front_eve, 960, WL)
LEAF = lambda x=LEAFX: prop("lf", N.leaf_boat, x, WL)
RIP = lambda hidden=False, x=1150: prop("rp", N.ripple, x, WL + 4, .9, hidden)
SWIM = lambda at, who, dx, d, ease="sine.inOut": ("to", at, "#{p}%s_w" % who, {"x": "+=%d" % dx, "duration": d, "ease": ease}, who + " swims")
FLAP = lambda at, n=7, d=.45: ("to", at, "#{p}tula-ff", {"rotation": 24, "svgOrigin": "95 -122", "duration": d, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "Tula paddles")
BOB = lambda at, who, n=5, dy=18: ("to", at, "#{p}%s" % who, {"y": "-=%d" % dy, "duration": .5, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "")
WIG = lambda at, who, n=9, d=.14: ("to", at, "#{p}%s" % who, {"rotation": 7, "transformOrigin": "50% 50%", "duration": d, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, who + " wiggles")
RISE = lambda at=0.1, y=462, d=1.3: ("to", at, "#{p}tula_w", {"y": y, "duration": d, "ease": "power2.out"}, "Tula comes up")
PUFFS = lambda at, name: ("fromto", at, "#{p}%s-0,#{p}%s-1,#{p}%s-2" % (name, name, name), {"opacity": 0}, {"opacity": 1, "duration": .3, "stagger": .25, "yoyo": True, "repeat": 3}, "a puff of breath")
PUFF = lambda hidden=True: prop("pf", A.puff, 1240, 215, .8, hidden)
TWINK = lambda at: ("to", at, "#{p}tw-0,#{p}tw-1,#{p}tw-2,#{p}tw-3,#{p}tw-4,#{p}tw-5", {"scale": .3, "opacity": .3, "transformOrigin": "50% 50%", "duration": .35, "stagger": {"each": .12, "yoyo": True, "repeat": 9}}, "the waves twinkle")
THINK = lambda fn, hidden=True: prop("th", fn, 1335, 85, .68, hidden)
ASLEEP = [("to", 0.0, "#{p}tula-eye-lid", {"opacity": 1, "duration": 0}), ("sleep", 0.3, "tula"), ("to", 0.32, "#{p}tula-neck", {"rotation": 5, "svgOrigin": "180 -170", "duration": 1.2})]
ZFLOAT = lambda at: ("to", at, "#{p}zz", {"y": -30, "opacity": .6, "duration": .9, "yoyo": True, "repeat": 11, "ease": "sine.inOut"}, "the Z's float")

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. The rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_DIVE = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "G4:1 E4:1 C4:2 D4:1 G4:1 B4:1", "rest": 1},      # down I dive in the deep blue sea (C bar falling, G bar)
                                 {"text": "~ ~ ~ ~ ~ ~", "notes": "F4:1 A4:1 C5:2 E5:1 D5:1 C5:1", "rest": 1}])     # up I come, take a breath with me (F bar rising, C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "D5:1 B4:1 G4:1 B4:1 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune
CNT3 = 0.52                                      # seconds from "One" to "three" (set from the timing file)

SHOTS = [
    # ------------------------------------------------------------ HOOK: Milo on his rock, Tula deep below (first 5 seconds)
    S("shore", (1100, 490, 1640), "How can Milo see under the deep blue sea? Look! His friend Tula lives down there!", beat="hook", tag="hook: Milo looks down at Tula",
      cam2=(1120, 510, 1540), props=[SF()],
      fx=[("face", 0.02, "milo", "wow"), FLAP(0.2, 15), BOB(0.2, "tula", 11), SWIM(0.2, "tula", 150, 6.5), ("hop", "w:Look!", "milo"), ("lookat", "w:Tula", "tula", -10)],
      words=[(0.4, "DOWN THERE?", .44, .4, 1.0, "sun"), ("w:Tula", "TULA'S HOME", .3, .7, .6, "pill")]),
    *intro_shots(),      # the main intro, right after the hook
    # ------------------------------------------------------------ GOAL: Milo wants to see Tula's home under the sea
    S("shore", WIDE, "Hello, I'm Milo! Today I am at the sea, on my little rock.", trans="iris", beat="goal", tag="Milo on his little rock",
      cam2=(1000, 520, 1800), props=[SF()], fx=[("hop", "w:Hello,", "milo"), FLAP(0.3, 11), SWIM(0.3, "tula", 160, 5.0), ("hop", "w:rock.", "milo")],
      words=[("w:sea,", "THE BLUE SEA", .42, .16, .75, "sun")]),
    S("shore", TCL("shore", 1000, 40, -20), "Hello, Milo! I am going home now. My home is deep under the water.", who="tula", beat="goal", tag="Tula: my home is under the water",
      props=[SF()], fx=[("face", 0.02, "tula", "happy"), ("nod", "w:Milo!", "tula"), FLAP("w:home", 9)], words=[("w:deep", "MY HOME", .5, .14, .85, "sun")]),
    S("shore", MCL, "Under the water? Oh, I want to see your home, Tula!", beat="goal", tag="Milo: I want to see your home",
      props=[SF()], fx=[("face", 0.02, "milo", "wow"), ("hop", "w:Oh,", "milo"), ("hop", "w:Tula!", "milo")], words=[("w:see", "I WANT TO SEE!", .5, .12, .8, "sun")]),
    S("shore", TCL("shore", 1040, 40, -30), "Then come along, Milo! Dive down with me!", who="tula", beat="goal", tag="Tula: dive down with me",
      props=[SF()], fx=[("face", 0.02, "tula", "happy"), FLAP("w:Dive", 5), BOB("w:Dive", "tula", 3)], words=[("w:Dive", "DIVE DOWN!", .5, .14, .85, "pill")]),
    S("shore", MCL, "Oh no. I am a little bird. I need air to breathe! I cannot go under the water.", beat="goal", tag="Milo: I need air",
      props=[SF()], fx=[("face", 0.02, "milo", "sad"), ("hop", "w:air", "milo"), ("face", "w:cannot", "milo", "sad")],
      words=[("w:air", "I NEED AIR!", .5, .12, .85, "sun")]),
    S("shore", MQ, "Can Milo go under the water? Yes, or no?", q=True, beat="goal", tag="question: under the water yes or no", pause=3.2, cam2=(ROCK[0] - 70, 120, 880),
      props=[SF()], fx=[("hop", "w:Milo", "milo"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    S("shore", WIDE, "So Tula dives down, down, into the deep blue sea. And Milo stays on his rock.", beat="goal", tag="Tula dives down",
      cam2=(900, 560, 1820), actors=[MI(), T(980, 600, .55, True)], props=[SF()],
      fx=[FLAP(0.1, 13), ("to", "w:dives", "#{p}tula_w", {"x": "-=1500", "y": "+=170", "duration": 4.6, "ease": "sine.in"}, "Tula dives away"), ("hop", "w:Milo", "milo")],
      words=[("w:deep", "DOWN SHE GOES", .4, .2, .7, "pill")]),
    S("shore", MCL, "I will find a way to see under the sea. I will try!", beat="goal", tag="Milo: I will try",
      hide=["tula"], props=[SF()], fx=[("face", 0.02, "milo", "happy"), ("hop", "w:way", "milo"), ("hop", "w:try!", "milo", 2)], words=[("w:try!", "I WILL TRY!", .5, .12, .85, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: looking from the rock (the water is too deep)
    S("shore", (1340, 350, 1300), "First, Milo looks down from his rock. He looks, and looks, and looks.", beat="obstacle1", tag="Milo looks down from his rock",
      cam2=(1300, 380, 1180), hide=["tula"], props=[SF()],
      fx=[("to", "w:looks", "#{p}milo", {"rotation": -14, "svgOrigin": "0 0", "duration": .5, "ease": "power2.out"}, "Milo leans over"), ("hop", "w:looks:3", "milo"), ("hop", "w:looks:4", "milo")],
      words=[("w:looks:2", "LOOK...", .3, .5, .7, "pill"), ("w:looks:4", "AND LOOK...", .36, .68, .7, "pill")]),
    S("shore", (1150, 380, 1300), "But the water is too deep. All he can see is the sun, twinkling on the waves.", beat="obstacle1", tag="only twinkles on the waves",
      cam2=(1120, 360, 1200), hide=["tula"], props=[SF(), prop("tw", N.twinkles, 1000, WL)],
      fx=[("face", 0.02, "milo", "sad"), TWINK(0.2), ("hop", "w:sun,", "milo")],
      words=[("w:deep.", "TOO DEEP!", .36, .66, .85, "sun"), ("w:twinkling", "TWINKLE, TWINKLE", .4, .16, .6, "pill")]),
    S("shore", MQ, "What can Milo see from his rock? Tula's home, or twinkles?", q=True, beat="obstacle1", tag="question: home or twinkles", pause=3.2, cam2=(ROCK[0] - 80, 120, 880),
      hide=["tula"], props=[SF(), prop("tw", N.twinkles, 1250, WL, .8)], fx=[TWINK(0.2), ("signs", "w:Tula's", ["HOME", "TWINKLES"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 2: the leaf boat (it goes round and round)
    S("shore", (1250, 360, 1300), "Next, Milo finds a big green leaf. It floats, like a little boat!", beat="obstacle2", tag="a big green leaf floats in",
      cam2=(1230, 340, 1220), hide=["tula"], props=[SF(), LEAF(680)],
      fx=[("to", 0.2, "#{p}lf_w", {"x": "+=%d" % (LEAFX - 680), "duration": 3.2, "ease": "sine.out"}, "the leaf floats in"), ("hop", "w:leaf.", "milo"), ("fly", "w:like", "milo", ML[2], ML[3], 1.1)],
      words=[("w:leaf.", "A BIG LEAF", .5, .14, .8, "sun")]),
    S("shore", (LEAFX, 200, 860), "A leaf boat! Now I can sail out, and peek down.", beat="obstacle2", tag="Milo on the leaf boat",
      hide=["tula"], actors=[ML], props=[SF(), LEAF()],
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:boat!", "milo"), ("to", 0.2, "#{p}lf,#{p}milo", {"rotation": 3, "svgOrigin": "0 0", "duration": .8, "yoyo": True, "repeat": 7, "ease": "sine.inOut"}, "")],
      words=[("w:boat!", "A LEAF BOAT!", .5, .1, .8, "sun")]),
    S("shore", (LEAFX, 250, 1100), "But the leaf goes round, and round, and round. Milo gets so dizzy!", beat="obstacle2", tag="the leaf goes round and round",
      cam2=(LEAFX, 240, 1020), hide=["tula"], actors=[ML], props=[SF(), LEAF(), prop("la", A.loop_arrow, 1330, 110, .8, True)],
      fx=[("face", 0.02, "milo", "wow"), ("to", 0.1, "#{p}lf,#{p}milo", {"rotation": 9, "svgOrigin": "0 0", "duration": .45, "yoyo": True, "repeat": 15, "ease": "sine.inOut"}, "the leaf rocks"),
          ("to", "w:round,", "#{p}lf_w,#{p}milo_w", {"x": "+=110", "duration": .9, "yoyo": True, "repeat": 5, "ease": "sine.inOut"}, "the leaf turns"), ("show", "w:round,", "la"),
          ("to", "w:round,", "#{p}la", {"rotation": 720, "transformOrigin": "50% 50%", "duration": 4.0, "ease": "none"}, "the arrow goes round")],
      words=[("w:round,", "ROUND AND ROUND", .28, .2, .6, "pill"), ("w:dizzy!", "SO DIZZY!", .28, .4, .85, "sun")]),
    S("shore", (1300, 300, 1300), "Flap, flap! Milo flies back to his rock. The leaf boat did not help.", beat="obstacle2", tag="Milo flies back to his rock",
      cam2=(1320, 290, 1220), hide=["tula"], actors=[ML], props=[SF(), LEAF()],
      fx=[("fly", "w:flies", "milo", ROCK[0], ROCK[1], 1.3), ("to", "w:leaf", "#{p}lf_w", {"x": "-=520", "duration": 3.0, "ease": "sine.in"}, "the leaf floats away"), ("face", "w:did", "milo", "sad")],
      words=[("w:Flap,", "FLAP, FLAP!", .5, .12, .8, "sun")]),
    S("shore", MQ, "Did the leaf boat help Milo? Yes, or no?", q=True, beat="obstacle2", tag="question: did the leaf boat help", pause=3.2, cam2=(ROCK[0] - 70, 120, 880),
      hide=["tula"], props=[SF()], fx=[("hop", "w:help", "milo"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 3: calling (Tula is deep down and does not hear)
    S("shore", MCL, "Then Milo calls, as loud as he can. Tula! Tula! Can you hear me?", beat="obstacle3", tag="Milo calls Tula",
      hide=["tula"], props=[SF()], fx=[("hop", "w:Tula!", "milo"), ("hop", "w:Tula!:2", "milo"), ("face", "w:Can", "milo", "wow")],
      words=[("w:Tula!", "TULA!", .3, .14, .9, "sun"), ("w:Tula!:2", "TULA!", .72, .22, .9, "sun")]),
    S("deep", WIDE, "But far below, in the deep blue water, Tula swims along. She does not hear Milo at all.", trans="iris", beat="obstacle3", tag="Tula deep down does not hear",
      cam2=(1000, 560, 1800), actors=[T(520, 700, .6)], props=[prop("bb", A.bubbles, 1300, 600, 1.0)],
      fx=[("face", 0.02, "tula", "happy"), FLAP(0.2, 17), SWIM(0.2, "tula", 420, 7.5, "none"), ("to", 0.2, "#{p}bb_w", {"y": "-=260", "duration": 7.0, "ease": "none"}, "bubbles float up")],
      words=[("w:deep", "DEEP DOWN", .5, .16, .8, "sun")]),
    S("deep", (860, 560, 1400), "Where is Tula now? Up at the top, or deep down?", q=True, beat="obstacle3", tag="question: at the top or deep down", pause=3.2, cam2=(880, 580, 1320),
      fx=[FLAP(0.2, 17), BOB(0.3, "tula", 13), ("signs", "w:Up", ["AT THE TOP", "DEEP DOWN"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ LOW MOMENT: Milo sits on his rock, a little sad (gentle: nobody cries)
    S("shore", (1400, 330, 1200), "Milo sits down on his rock. He tried, and tried, and he still cannot see Tula's home.", trans="iris", beat="low", tag="Milo sits on his rock",
      cam2=(1420, 310, 1100), hide=["tula"], props=[SF()],
      fx=[("face", 0.02, "milo", "sad"), ("to", 0.3, "#{p}milo-body", {"scaleY": .9, "svgOrigin": "0 0", "duration": .6}, "Milo sits down")],
      words=[("w:tried,", "HE TRIED...", .36, .2, .7, "pill"), ("w:still", "NOT YET", .36, .38, .8, "sun")]),
    S("shore", MCL, "Maybe a little bird can never see under the sea.", beat="low", tag="Milo: maybe never",
      hide=["tula"], props=[SF()], fx=[("face", 0.02, "milo", "sad"), ("to", 0.02, "#{p}milo-body", {"scaleY": .9, "svgOrigin": "0 0", "duration": .01}, "")]),
    S("shore", MQ, "How does Milo feel now? Happy, or sad?", q=True, beat="low", tag="question: happy or sad", pause=3.2, cam2=(ROCK[0] - 70, 120, 880),
      hide=["tula"], props=[SF()], fx=[("face", 0.02, "milo", "sad"), ("signs", "w:Happy,", ["HAPPY", "SAD"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: bubbles, Tula comes up for air, Milo's own idea
    S("shore", (1320, 360, 1100), "Then, look! Little bubbles pop up, right beside the rock.", beat="solution", tag="bubbles beside the rock",
      cam2=(1300, 370, 1020), hide=["tula"], props=[prop("b1", A.bubbles, 1200, 640, 1.2), prop("b2", A.bubbles, 1290, 760, 1.0), SF()],
      fx=[("face", "w:look!", "milo", "wow"), ("hop", "w:look!", "milo"), ("to", 0.2, "#{p}b1_w", {"y": "-=300", "duration": 4.4, "ease": "none"}, "bubbles float up"),
          ("to", 0.6, "#{p}b2_w", {"y": "-=400", "duration": 4.2, "ease": "none"}, "")],
      words=[("w:bubbles", "BUBBLES!", .3, .2, .9, "sun")]),
    S("shore", (1280, 350, 940), "Let's count the bubbles! One, two, three!", q=True, beat="solution", tag="count the bubbles", pause=1.0, cam2=(1270, 350, 900),
      hide=["tula"], props=[prop("b3", N.bub3, 1180, 400, 1.0), SF()],
      fx=[("fromto", 0.0, "#{p}b3-0,#{p}b3-1,#{p}b3-2", {"opacity": 0}, {"opacity": 0, "duration": .01}, ""),
          ("to", "w:One,", "#{p}b3-0", {"opacity": 1, "duration": .12}, "bubble one"), ("to", "w:two,", "#{p}b3-1", {"opacity": 1, "duration": .12}, "bubble two"),
          ("to", "w:three!", "#{p}b3-2", {"opacity": 1, "duration": .12}, "bubble three"), ("count", "w:One,", 3, CNT3, {"x": 560, "y": 210})]),
    S("shore", TOP2, "And up comes Tula! She takes a big, big breath of air.", beat="solution", tag="Tula comes up for air",
      cam2=(1280, 320, 1040), actors=[MI(), TU(1040, 760)], props=[SF(), RIP(True), PUFF()],
      fx=[RISE(0.1), ("show", 1.2, "rp", None, False), ("face", "w:Tula!", "milo", "wow"), ("hop", "w:Tula!", "milo"), ("show", "w:breath", "pf", None, False), PUFFS("w:breath", "pf")],
      words=[("w:up", "UP FOR AIR!", .3, .14, .85, "sun")]),
    S("shore", MCL, "Tula! You came back up! Why did you come up?", beat="solution", tag="Milo: why did you come up",
      hide=["tula"], props=[SF()], fx=[("face", 0.02, "milo", "wow"), ("hop", "w:Tula!", "milo"), ("hop", "w:Why", "milo")], words=[("w:Why", "WHY?", .5, .12, .95, "sun")]),
    S("shore", TUC, "I came up to breathe, Milo. I need air, just like you!", who="tula", beat="solution", tag="Tula: I need air too",
      hide=["milo"], actors=UPST, props=[SF(), RIP()], fx=[("face", 0.02, "tula", "happy"), ("nod", "w:Milo.", "tula"), BOB("w:air,", "tula", 3, 10)],
      words=[("w:air,", "I NEED AIR TOO!", .5, .12, .75, "sun")]),
    S("paper_sea", (960, 540, 1700), "Sea turtles breathe air. They must come up to the surface to breathe.", beat="fact", tag="fact: sea turtles breathe air",
      cam2=(960, 530, 1620), actors=[("tula", "turtle_up", 800, 830, .7)], props=[prop("ar", N.up_arrow, 1340, 600, 1.0, True), prop("pf", A.puff, 1060, 330, .9, True)],
      fx=[("to", "w:They", "#{p}tula_w", {"y": N.BWL + 203, "duration": 1.6, "ease": "power2.out"}, "the turtle comes up"), ("show", "w:come", "ar"),
          ("to", "w:come", "#{p}ar", {"y": "-=40", "duration": .4, "yoyo": True, "repeat": 7, "ease": "sine.inOut"}, ""), ("show", "w:surface", "pf", None, False), PUFFS("w:surface", "pf")],
      words=[("w:air.", "SEA TURTLES BREATHE AIR", .54, .07, .46, "sun"), ("w:surface", "UP TO THE TOP", .76, .3, .5, "pill")]),
    S("paper_sea", (960, 500, 1800), "What does a sea turtle breathe? Air, or water?", q=True, beat="fact", tag="question: air or water", pause=3.2, cam2=(960, 490, 1720),
      actors=[("tula", "turtle_up", 800, N.BWL + 203, .7)], fx=[BOB(0.3, "tula", 13, 10), ("signs", "w:Air,", ["AIR", "WATER"], 0, "wait:1.8")]),
    S("shore", TUC, "Can you take a big breath, like me? Breathe in, and blow it out!", q=True, who="tula", beat="solution", tag="copy me: a big breath",
      pause=3.0, hide=["milo"], actors=UPST, props=[SF(), RIP(), prop("pf", A.puff, 1240, 215, .8, True)], cam2=(1110, 290, 690),
      fx=[("face", 0.02, "tula", "happy"), ("to", "w:Breathe", "#{p}tula", {"y": "-=22", "duration": .7, "yoyo": True, "repeat": 1, "ease": "sine.inOut"}, "Tula breathes in"),
          ("show", "w:blow", "pf", None, False), PUFFS("w:blow", "pf"),
          ("to", "wait:0.3", "#{p}tula", {"y": "-=22", "duration": .8, "yoyo": True, "repeat": 1, "ease": "sine.inOut"}, "Tula breathes in again"), PUFFS("wait:1.6", "pf")],
      words=[("w:Breathe", "BREATHE IN...", .5, .12, .8, "sun"), ("w:blow", "AND OUT!", .5, .26, .7, "pill"), ("wait:0.3", "YOUR TURN!", .28, .5, .7, "pill")]),
    S("shore", MCL, "I have an idea! I cannot go down. But you come up!", beat="solution", tag="Milo: I have an idea",
      hide=["tula"], props=[SF()], fx=[("face", 0.02, "milo", "happy"), ("hop", "w:idea!", "milo", 2), ("hop", "w:up!", "milo")], words=[("w:idea!", "AN IDEA!", .5, .12, .9, "sun")]),
    S("shore", TOP2, "Every time you come up for air, tell me one thing you saw!", beat="solution", tag="Milo: tell me one thing you saw",
      cam2=(1280, 320, 1040), actors=UPST, props=[SF(), RIP()], fx=[("hop", "w:Every", "milo"), ("nod", "w:air,", "tula"), ("hop", "w:tell", "milo"), ("face", "w:saw!", "tula", "happy")],
      words=[("w:tell", "TELL ME!", .36, .14, .85, "sun")]),
    S("reef", WIDE, "So Tula dives down to the coral garden. It is pink, and orange, and purple!", trans="iris", beat="solution", tag="the coral garden",
      cam2=(1040, 550, 1800), actors=[T(420, 640, .58), Z(1280, 400), PL(1500, 800, .4, True)],
      fx=[("face", 0.02, "tula", "happy"), FLAP(0.1, 15), SWIM(0.1, "tula", 440, 6.5), BOB(0.2, "zip", 9), BOB(0.5, "pearl", 9), WIG("w:pink,", "zip", 7), WIG("w:purple!", "pearl", 7)],
      words=[("w:coral", "CORAL GARDEN", .5, .16, .75, "sun")]),
    S("shore", TUC, "Milo! I saw a coral garden. Pink, and orange, and purple!", who="tula", beat="solution", tag="Tula tells: a coral garden",
      hide=["milo"], actors=[MI(), TU(1040, 640)], props=[SF(), RIP(True)], fx=[RISE(0.0, 462, .8), ("show", 0.7, "rp", None, False), ("face", 0.02, "tula", "happy"), ("nod", "w:coral", "tula")],
      words=[("w:coral", "A CORAL GARDEN!", .5, .12, .7, "sun")]),
    S("shore", MCL, "Wow! I can see it in my head!", beat="solution", tag="Milo sees the coral in his head",
      hide=["tula"], props=[SF(), THINK(N.think_coral)], fx=[("face", 0.02, "milo", "wow"), ("show", "w:see", "th"), ("hop", "w:Wow!", "milo")]),
    S("paper_sea", (960, 560, 1700), "Sea turtles cannot breathe under the water. But they can hold their breath for a long time.", beat="fact", tag="fact: they hold their breath a long time",
      cam2=(980, 560, 1620), actors=[("tula", "turtle", 760, 800, .7)], props=[prop("ck", art.clock, 1380, 660, .8, True)],
      fx=[FLAP(0.2, 19), BOB(0.2, "tula", 15, 12), ("show", "w:hold", "ck"), ("to", "w:long", "#{p}ck-min", {"rotation": 720, "svgOrigin": "0 0", "duration": 3.0, "ease": "none"}, "the clock goes round")],
      words=[("w:hold", "HOLD THEIR BREATH", .5, .08, .55, "sun"), ("w:long", "A LONG TIME", .74, .4, .5, "pill")]),
    S("paper_sea", (960, 500, 1800), "Can a sea turtle hold her breath for a long time? Yes, or no?", q=True, beat="fact", tag="question: hold her breath yes or no", pause=3.2,
      cam2=(960, 490, 1720), actors=[("tula", "turtle", 760, 800, .7)], props=[prop("ck", art.clock, 1380, 660, .8)],
      fx=[FLAP(0.2, 19), ("to", 0.2, "#{p}ck-min", {"rotation": 720, "svgOrigin": "0 0", "duration": 7.5, "ease": "none"}, ""), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    S("meadow", WIDE, "Next, Tula dives down to the seagrass meadow. The tall green grass waves hello!", trans="iris", beat="solution", tag="the seagrass meadow",
      cam2=(1020, 560, 1800), actors=[T(360, 700)], fx=[("face", 0.02, "tula", "happy"), FLAP(0.1, 15), SWIM(0.1, "tula", 520, 6.5), ("nod", "w:hello!", "tula")],
      words=[("w:seagrass", "SEAGRASS MEADOW", .5, .16, .7, "sun")]),
    S("shore", TUC, "Milo! I saw a seagrass meadow. It waves like a big green field!", who="tula", beat="solution", tag="Tula tells: a seagrass meadow",
      hide=["milo"], actors=[MI(), TU(1040, 640)], props=[SF(), RIP(True)], fx=[RISE(0.0, 462, .8), ("show", 0.7, "rp", None, False), ("face", 0.02, "tula", "happy"), ("nod", "w:seagrass", "tula")],
      words=[("w:seagrass", "A SEAGRASS MEADOW!", .5, .12, .62, "sun")]),
    S("shore", MCL, "Green and wavy! Tell me more, Tula!", beat="solution", tag="Milo sees the seagrass in his head",
      hide=["tula"], props=[SF(), THINK(N.think_grass)], fx=[("face", 0.02, "milo", "happy"), ("show", 0.1, "th"), ("hop", "w:more,", "milo")]),
    S("rocks", WIDE, "Then Tula dives down to the big rocks. Here is her cozy bed!", trans="iris", beat="solution", tag="the big rocks: her cozy bed",
      cam2=(980, 600, 1700), actors=[T(380, 660)],
      fx=[("face", 0.02, "tula", "happy"), FLAP(0.1, 9), ("to", 0.1, "#{p}tula_w", {"x": 900, "y": 800, "duration": 4.2, "ease": "sine.inOut"}, "Tula swims to her bed")],
      words=[("w:cozy", "A COZY BED", .5, .16, .8, "sun")]),
    S("rocks", (960, 660, 1300), "A sleeping sea turtle can stay under the water for several hours.", beat="fact", tag="fact: a sleeping sea turtle stays under for hours",
      cam2=(980, 660, 1220), props=[prop("zz", N.zzz, 1120, 560, .8), prop("ck", art.clock, 520, 520, .6, True)],
      fx=[*ASLEEP, ZFLOAT(0.1), ("show", "w:several", "ck"), ("to", "w:several", "#{p}ck-min", {"rotation": 1080, "svgOrigin": "0 0", "duration": 3.0, "ease": "none"}, "the clock goes round and round")],
      words=[("w:sleeping", "FAST ASLEEP", .5, .12, .7, "sun"), ("w:several", "SEVERAL HOURS", .5, .26, .6, "pill")]),
    S("rocks", (940, 640, 1500), "Where is Tula's cozy bed? Under the water, or in a tree?", q=True, beat="fact", tag="question: under the water or in a tree", pause=3.2, cam2=(950, 660, 1420),
      props=[prop("zz", N.zzz, 1120, 560, .8)], fx=[*ASLEEP, ZFLOAT(0.1), ("signs", "w:Under", ["UNDER WATER", "IN A TREE"], 0, "wait:1.8")]),
    S("shore", TUC, "And I saw my cozy bed, by the big rocks!", who="tula", beat="solution", tag="Tula tells: my cozy bed",
      hide=["milo"], actors=[MI(), TU(1040, 640)], props=[SF(), RIP(True)], fx=[RISE(0.0, 462, .8), ("show", 0.7, "rp", None, False), ("face", 0.02, "tula", "happy"), ("nod", "w:bed,", "tula")],
      words=[("w:bed,", "MY COZY BED!", .5, .12, .75, "sun")]),
    S("shore", MCL, "Now I know your whole home, Tula! And I did not get wet at all!", beat="solution", tag="Milo: I know your whole home",
      hide=["tula"], props=[SF(), THINK(N.think_bed)], fx=[("face", 0.02, "milo", "happy"), ("show", 0.1, "th"), ("hop", "w:home,", "milo"), ("hop", "w:wet", "milo", 2)],
      words=[("w:wet", "NOT WET!", .82, .34, .55, "pill")]),
    # ------------------------------------------------------------ the song moment: Tula SAYS the rhyme, then the tune on instruments
    S("shore", TOP2, "Down I dive in the deep blue sea. Up I come, take a breath with me!", who="tula", beat="solution", tag="the diving rhyme", cam2=(1280, 320, 1040),
      actors=UPST, props=[SF(), RIP()],
      fx=[("face", 0.02, "tula", "happy"), ("to", "w:Down", "#{p}tula_w", {"y": "+=70", "duration": .9, "ease": "sine.inOut"}, "Tula dips down"),
          ("to", "w:Up", "#{p}tula_w", {"y": 462, "duration": .7, "ease": "sine.inOut"}, "Tula comes up"), ("hop", "w:breath", "milo")],
      words=[("w:Down", "DOWN I DIVE", .3, .13, .62, "sun"), ("w:Up", "UP I COME", .3, .25, .6, "pill")]),
    S("shore", (1200, 420, 1500), who="", sing=SING_DIVE, beat="song", tag="song: down and up", cam2=(1240, 400, 1380),
      actors=UPST, props=[prop("b1", A.bubbles, 760, 720, 1.0), SF(), RIP()],
      fx=[("to", TB(0), "#{p}tula_w", {"y": "+=230", "duration": 4 * 60 / 96, "ease": "sine.inOut"}, "Tula dives on the falling tune"),
          ("to", TB(4), "#{p}tula_w", {"y": 462, "duration": 3 * 60 / 96, "ease": "sine.inOut"}, "Tula comes up"),
          ("to", TB(8), "#{p}tula_w", {"y": "+=230", "duration": 2 * 60 / 96, "ease": "sine.inOut"}, "Tula dives again"),
          ("to", TB(10), "#{p}tula_w", {"y": 462, "duration": 3 * 60 / 96, "ease": "sine.inOut"}, "Tula comes up on the rising tune"),
          ("hop", TB(2), "milo"), ("hop", TB(6), "milo"), ("hop", TB(10), "milo"), ("hop", TB(13), "milo"),
          ("to", TB(0), "#{p}b1_w", {"y": "-=300", "duration": 9.6, "ease": "none"}, "bubbles float up"),
          ("word", TB(0), "DOWN I DIVE", {"x": 900, "y": 150, "size": 84, "cls": "sun", "hold": 4.6})],
      words=[(TB(8), "UP I COME", .36, .12, .62, "pill")]),
    S("shore", MQ, "Did Milo find a way to see Tula's home? Yes, or no?", q=True, beat="solution", tag="question: did Milo find a way", pause=3.2, cam2=(ROCK[0] - 70, 120, 880),
      hide=["tula"], props=[SF()], fx=[("face", 0.02, "milo", "happy"), ("hop", "w:way", "milo"), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ WARM ENDING: the evening, thank-yous, recap
    S("shore_eve", WIDE, "The sun goes down, and the sea turns gold. Milo and Tula rest, side by side.", trans="iris", beat="ending", tag="evening at the little rock",
      cam2=(1040, 500, 1760), props=[SFE(), RIP()], fx=[("face", 0.02, "tula", "happy"), ("hop", "w:sun", "milo"), BOB("w:Milo", "tula", 5, 10)],
      words=[("w:gold.", "GOLDEN SEA", .4, .62, .75, "sun")]),
    S("shore_eve", MCL, "Thank you, Tula! You showed me your home, one breath at a time.", beat="ending", tag="Milo: thank you",
      hide=["tula"], props=[SFE()], fx=[("face", 0.02, "milo", "happy"), ("hop", "w:Thank", "milo")], words=[("w:Thank", "THANK YOU!", .5, .12, .85, "sun")]),
    S("shore_eve", TUC, "And you had the good idea, Milo. Friends can share in many ways!", who="tula", beat="ending", tag="Tula: friends can share",
      hide=["milo"], props=[SFE(), RIP()], fx=[("face", 0.02, "tula", "happy"), ("nod", "w:Milo.", "tula"), BOB("w:Friends", "tula", 3, 10)],
      words=[("w:share", "FRIENDS SHARE", .5, .12, .75, "pill")]),
    S("shore_eve", (1480, 210, 1000), "When one way does not work, you can look for another way.", beat="ending", tag="the lesson",
      hide=["tula"], cam2=(1500, 200, 940), props=[SFE()], fx=[("hop", "w:work,", "milo"), ("hop", "w:another", "milo")], words=[("w:another", "ANOTHER WAY!", .42, .12, .85, "sun")]),
    S("shore_eve", (1180, 250, 1000), "Do you remember? What does a sea turtle breathe? Air, or sand?", q=True, beat="ending", tag="question: air or sand", pause=3.2,
      cam2=(1190, 250, 950), hide=["milo"], actors=[MI(), TU(1040, 480)], props=[SFE(), RIP()], fx=[BOB(0.3, "tula", 13, 10), ("signs", "w:Air,", ["AIR", "SAND"], 0, "wait:1.8")]),
    S("shore_eve", (1300, 190, 1160), "And where does a sea turtle go to breathe? Up to the top, or down to the sand?", q=True, beat="ending", tag="question: up or down", pause=3.2,
      cam2=(1310, 190, 1100), actors=[MI(), TU(1040, 480)], props=[SFE(), RIP()], fx=[("hop", "w:where", "milo"), BOB(0.3, "tula", 15, 10), ("signs", "w:Up", ["UP", "DOWN"], 0, "wait:1.8")]),
    S("shore_eve", WIDE, "Down she dives in the deep blue sea. Up she comes, for a breath with me!", beat="ending", tag="the closing rhyme", cam2=(1040, 520, 1780),
      props=[SFE(), RIP()], fx=[("to", "w:Down", "#{p}tula_w", {"y": "+=120", "duration": .9, "ease": "sine.inOut"}, "Tula dips down"),
                         ("to", "w:Up", "#{p}tula_w", {"y": 462, "duration": .7, "ease": "sine.inOut"}, "Tula comes up"), ("hop", "w:breath", "milo")],
      words=[("w:Down", "DOWN SHE DIVES", .4, .56, .6, "sun"), ("w:Up", "UP SHE COMES", .4, .68, .55, "pill")]),
    S("shore_eve", (1300, 340, 1200), who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(1320, 320, 1100),
      props=[SFE(), RIP()], fx=[("hop", 1.0, "milo"), ("nod", 1.6, "tula"), ("hop", 2.2, "milo"), BOB(0.2, "tula", 7, 10)],
      words=[(TB(3), "HOORAY!", .36, .18, .9, "sun")]),
    S("shore_eve", MCL, "See you on the next adventure, friends!", beat="ending", tag="goodbye",
      hide=["tula"], props=[SFE()], fx=[("hop", "w:See", "milo"), ("hop", "w:friends!", "milo")], words=[("w:See", "SEE YOU SOON!", .5, .12, .7, "sun")]),
    *intro_shots(),      # and again as the last shots: the video ends on the logo with the whole cast
]

# thumbnail (thumb.py): the promise of the first shot: Milo on his rock looks down at Tula under the water; 2 words, none of the title's words, no watermark
THUMBS = {
    "za_ep15": {"place": "shore", "cam": (1150, 400, 1400),
                "actors": [("turtle", 880, 730, .92, False, ''), ("milo", 1560, 256, .62, False, '')],
                "props": [(N.sea_front, 960, 300, 1.0)],
                "words": [("DOWN THERE?", 690, 250, 165, "sun", -5)]},
}
