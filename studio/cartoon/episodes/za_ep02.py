"""za_ep02 - Milo's Zoo Adventures: "Baby Elephant Tumble and the Big Muddy Puddle" (cartoon adventure, the 3D music-and-sync process: "beat").
Photo day at the zoo. Tumble wants to stay clean, but the sun is hot. A leaf hat, a fan and the shade each help for a moment.
At the mud hole he finds Mama, all muddy and cool, and chooses the mud himself. Nobody is hurt, lost, crying or trapped.

STATE (Nov 17 2026, 12:20 AM): FIRST DRAFT. The lines, the beats and the art exist; NO still of any shot has been looked at yet. Every position below is a first guess from the stage numbers. Before a render: plan check, one still of EVERY shot, fixes, stills again.

FACTS, read at the source on Nov 16 2026, 11:58 PM ET:
 [SDZ] San Diego Zoo Wildlife Alliance, animals.sandiegozoo.org/animals/elephant
   "Elephants often spray themselves with water or roll in the mud or dust for protection from the sun and biting insects."
   "An elephant's ears work like a radiator."   "This ear flapping behavior cools their large bodies on warm days."
   "Frequent bathing and showering, as well as powdering with dirt, is an important part of elephant skin care."
 Not animal facts, said as what happens in the story: a leaf is a small hat; shade moves when the sun moves and is smallest when the sun is overhead.
 "Mud is like a sun hat for the whole body" is Milo's comparison, not a quote.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
from kit import Kit, S, prop

EP = {"id": "za_ep02", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "tumble": {"voice": "am_puck", "speed": .85, "pitch": 5, "formant": 1.16, "gain": .66},
               "mango": {"voice": "af_bella", "speed": .95, "pitch": 2, "formant": 1.08, "gain": .95}, "mama": {"voice": "bf_emma", "speed": .8, "gain": .8}},
      "title": "Baby Elephant Tumble and the Big Muddy Puddle", "thumb_text": "SPLASH TIME!",
      "series": "Milo's Zoo Adventures",
      "description": ("It is photo day at the zoo, and baby elephant Tumble wants to stay clean. But the sun is so hot! A leaf hat, a fan and the shade each help for a moment. "
                      "Then Tumble finds a big muddy puddle, and Mama shows him what elephants do on a hot day. "
                      "A gentle animal adventure for ages 2-6 about trying, staying cool and having fun, with questions to answer and a song to sing along.\n"
                      "Kids see how an elephant flaps its big ears to cool down, and how mud protects an elephant's skin from the sun.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (elephant)."),
      "tags": ["baby elephant", "elephant story for kids", "animal stories for kids", "muddy puddle", "kids adventure cartoon", "why elephants roll in mud", "spider monkey",
               "hot day story for kids", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "zoo": [("mama", "elephant", 1480, 930, .92, True), ("tumble", "tumble", 560, 936, .6), ("milo", "milo", 260, 500, .78, False, True)],
    "savanna": [("tumble", "tumble", 620, 930, .62), ("milo", "milo", 430, 500, .8, False, True)],
    "jungle": [("tumble", "tumble", 860, 930, .62), ("milo", "milo", 400, 480, .78, False, True)],
    "canopy": [("mango", "monkey_hang", 780, 462, .6)],
    "bigtree": [("tumble", "tumble", 980, 930, .62), ("mango", "monkey", 520, 934, .58), ("milo", "milo", 280, 470, .75, False, True)],
    "mudhole": [("mama", "elephant_mud", 1440, 1000, .88, True), ("tumble", "tumble", 520, 874, .58), ("mango", "monkey", 190, 878, .52), ("milo", "milo", 860, 430, .7, False, True)],
    "zoo_eve": [("mango", "monkey", 300, 940, .55), ("tumble", "tumble_mud", 660, 940, .6), ("mama", "elephant_mud", 1540, 932, .9, True), ("milo", "milo", 330, 420, .68, False, True)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
EAR = "250 -590"; TP = "392 -430"       # the pivots of an elephant's ear and trunk
# stages used for a few shots
IN_MUD = [("mama", "elephant_mud", 1440, 1000, .88, True), ("tumble", "tumble_mud", 620, 1000, .6), ("mango", "monkey", 190, 878, .52), ("milo", "milo", 860, 520, .7, False, True)]
PHOTO = [("mama", "elephant_mud", 1340, 770, .66, True), ("tumble", "tumble_mud", 630, 774, .52), ("mango", "monkey", 440, 776, .46)]
MF = lambda: prop("mf", art3.mud_front, 960, 958, 1.0)                    # the mud in front of whoever stands in the pool
CAM_Z = lambda: prop("cam", art3.camera, 230, 952, .85)                     # Milo's camera at the zoo gate
CAM_E = lambda: prop("cam", art3.camera, 110, 962, .85)
SUN_S = lambda: prop("hs", art3.hot_sun, 1500, 220, .8)                     # over the savanna's own sun
SPIN = ("to", 0.05, "#{p}hs-rays", {"rotation": 60, "transformOrigin": "50% 50%", "duration": 6, "ease": "none"}, "")
FLAP = lambda at, who="tumble", n=7: ("to", at, "#{p}" + who + "-ear", {"rotation": 14, "svgOrigin": EAR, "duration": .18, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, f"{who} flaps its ears")
NOMUD = lambda who="tumble": ("to", 0, "#{p}" + who + " .mud", {"opacity": 0, "duration": .01}, "")
ARM_UP = ("to", 0, "#{p}mango-ar", {"rotation": -80, "svgOrigin": "58 -206", "duration": .01}, "")      # Mango holds the fan up: her right hand is then at (642, 795) on the "bigtree" stage
LEAF_ON = (908, 571)      # where the leaf hat lies on Tumble's head in the jungle (stem at the back of the head)

# Nov 17 2026 (owner: Milo's sung voice "sounds robotic"): nobody sings. The tune is played by the bells and the soft band; the rhyme is SAID by Milo and shown on screen.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}       # the show loop's key and the music bed's tempo
SING_GO = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~ ~", "notes": "C4:1 E4:1 G4:1 G4:.5 A4:.5,G4:.5 E4:.5 D4:2", "rest": 1},
                               {"text": "~ ~ ~ ~ ~ ~ ~", "notes": "A4:1 A4:1 G4:1 F4:.5 F4:.5 E4:1 C4:2", "rest": 1}])
SING_END_A = dict(REFRAIN, chords="C G", lines=[{"text": "~ ~ ~ ~ ~", "notes": "C4:1 E4:1 G4:1 G4:.5,A4:.5 G4:.5,E4:1.5", "rest": 2}])
SING_END_B = dict(REFRAIN, chords="F C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "A4:1 A4:.5 A4:.5,G4:.5 F4:.5,D4:.5 C4:2.5", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune

SHOTS = [
    # ------------------------------------------------------------ HOOK: the feeling and the problem in the first 5 seconds
    S("zoo", C("zoo", "tumble", "all", 1000, 20, -50), "It is photo day at the zoo! But the sun is so, so hot.", beat="hook", tag="hook: photo day, so hot", hide=["mama", "milo"],
      props=[prop("sw", art3.sweat, *P("zoo", "tumble", "top", 130, 20), .7, True)],
      words=[("w:photo", "PHOTO DAY!", .43, .13, .85, "sun"), ("w:hot.", "SO HOT!", .8, .16, .85, "")], fx=[("face", "w:But", "tumble", "sad"), ("show", "w:hot.", "sw")]),
    S("zoo", C("zoo", "milo", "body", 760), "I'm Milo! Can you help Tumble stay cool today?", tag="hook: Milo", hide=["mama", "tumble"], fx=[("hop", "w:help", "milo")]),
    S("zoo", WIDE, "This is Tumble, the baby elephant. And this is my camera!", tag="zoo wide", cam2=(980, 560, 1800), props=[CAM_Z()],
      words=[("w:Tumble,", "TUMBLE", .41, .4, .85, "pill"), ("w:camera!", "CLICK!", .2, .55, .7, "sun")], fx=[("snd", "w:camera!", "ding")]),
    S("zoo", C("zoo", "mama", "head", 900, 40, 40), "We take our photo when the sun is low, Tumble.", who="mama", tag="Mama: photo at sunset", hide=["tumble", "milo"],
      fx=[("nod", "w:photo", "mama")], words=[("w:sun", "AT SUNSET", .28, .2, .8, "pill")]),
    # ------------------------------------------------------------ GOAL
    S("zoo", C("zoo", "tumble", "head", 920, -60, 20), "I want to look my very best. All clean and shiny!", who="tumble", beat="goal", tag="goal: stay clean", hide=["mama", "milo"],
      fx=[("face", 0.1, "tumble", "happy"), ("hop", "w:All", "tumble")], words=[("w:clean", "ALL CLEAN!", .25, .19, .75, "sun")]),
    S("zoo", C("zoo", "milo", "body", 820, 30, 0), "But it is a hot, hot day. How will you stay cool, Tumble?", tag="Milo: how will you stay cool", hide=["mama", "tumble"],
      props=[prop("ht", art3.heat, 560, 470, .8, True)], fx=[("show", "w:hot,", "ht")], words=[("w:cool,", "STAY COOL?", .72, .22, .9, "pill")]),
    S("zoo", C("zoo", "tumble", "head", 800, -40, 10), "I will find a way. And I will not get dirty!", who="tumble", tag="I will find a way", hide=["mama", "milo"],
      fx=[("face", 0.02, "tumble", "wow"), ("trunk", "w:not", "tumble", -40, .3), ("trunk", "e:dirty!", "tumble", 0, .3)], words=[("w:not", "NO DIRT!", .28, .22, .9, "pill")]),
    S("zoo", C("zoo", "mama", "head", 900, 40, 40), "Have fun, Tumble. And stay out of the hot sun!", who="mama", tag="Mama: have fun", hide=["tumble", "milo"],
      fx=[("nod", "w:Have", "mama"), ("trunk", "w:stay", "mama", -30, .4), ("trunk", "e:sun!", "mama", 0, .4)]),
    S("zoo", (744, 600, 1400), "Off they go, to find a cool place.", tag="off they go", hide=["mama"], move={"milo": (260, 570, .78)},
      fx=[("walk", 0.1, "tumble", 260, 3.0), ("fly", 0.1, "milo", 480, 610, 3.0)]),
    S("savanna", WIDE, trans="iris", who="", sing=SING_GO, beat="song", tag="song: off we go", props=[SUN_S()],
      fx=[SPIN, ("walk", 0.2, "tumble", 360, 8.6), ("fly", 0.2, "milo", 400, 500, 8.6), ("trunk", TB(3), "tumble", -60, .4), ("trunk", TB(5), "tumble", 0, .4), ("trunk", TB(11), "tumble", -60, .4), ("trunk", TB(13), "tumble", 0, .4)],
      move={"tumble": (240, 930, .62), "milo": (150, 480, .8)}, words=[(TB(0), "FRIENDS HELP FRIENDS", .42, .15, .6, "pill"), (TB(8), "STEP BY STEP", .5, .32, .8, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: the sun on his head (a leaf hat is too small)
    S("savanna", (1150, 480, 1500), "The sun shines down on the wide savanna.", beat="obstacle1", tag="the hot sun", hide=["tumble", "milo"], cam2=(1250, 420, 1300), props=[SUN_S(), prop("ht", art3.heat, 1100, 520, 1.0, True)],
      fx=[SPIN, ("show", "w:down", "ht")], words=[("w:sun", "HOT SUN", .3, .2, 1.0, "sun")]),
    S("savanna", C("savanna", "tumble", "head", 820, -40, 10), "Oh my! My head is so hot.", who="tumble", beat="obstacle1", tag="my head is hot", hide=["milo"],
      props=[prop("sw", art3.sweat, *P("savanna", "tumble", "top", 130, 20), .7, True)], fx=[("face", 0.05, "tumble", "sad"), ("show", "w:head", "sw")]),
    S("savanna", C("savanna", "milo", "body", 820, 20, -70), "Hmm. What could keep the sun off Tumble's head? A hat, or a shoe?", q=True, beat="obstacle1", tag="question: hat or shoe", pause=3.2, hide=["tumble"],
      fx=[("signs", "w:hat,", ["HAT", "SHOE"], 0, "wait:2.0")]),
    S("jungle", WIDE, "In the green jungle, the leaves are big and round.", trans="iris", beat="obstacle1", tag="jungle wide", cam2=(1040, 560, 1720),
      move={"tumble": (700, 930, .62)}, fx=[("walk", 0.1, "tumble", 160, 3.0)], words=[("w:big", "BIG LEAVES", .7, .2, 1.0, "pill")]),
    S("jungle", C("jungle", "tumble", "all", 1000, 60, -20), "A leaf! I can make a sun hat.", who="tumble", beat="obstacle1", tag="a leaf", hide=["milo"],
      props=[prop("lf", art3.leaf, 1110, 900, .7)], fx=[("face", 0.02, "tumble", "wow"), ("trunk", "w:leaf!", "tumble", 14, .4), ("hop", "w:sun", "tumble")]),
    S("jungle", C("jungle", "tumble", "all", 1000, 60, -60), "Tumble puts the big leaf on his head. A leaf hat!", beat="obstacle1", tag="the leaf hat", hide=["milo"],
      props=[prop("lf", art3.leaf, 1110, 900, .7)],
      fx=[("trunk", 0.1, "tumble", -100, .7), ("to", 0.15, "#{p}lf_w", {"x": LEAF_ON[0], "y": LEAF_ON[1], "duration": .9, "ease": "power2.inOut"}, "the leaf goes on his head"), ("trunk", "w:on", "tumble", 0, .5)],
      words=[("w:hat!", "LEAF HAT!", .26, .2, 1.0, "sun")]),
    S("jungle", C("jungle", "tumble", "head", 820, -40, -10), "Oh, that is better. Now my head is cool!", who="tumble", beat="obstacle1", tag="my head is cool", hide=["milo"],
      props=[prop("lf", art3.leaf, LEAF_ON[0], LEAF_ON[1], .7)], fx=[("face", 0.02, "tumble", "happy"), ("blinkslow", "w:cool!", "tumble-eye", 1)]),
    S("jungle", (900, 660, 1500), "But look. The leaf is small. Tumble's big back is still in the sun.", beat="obstacle1", tag="the back is in the sun", hide=["milo"], cam2=(860, 660, 1400),
      props=[prop("lf", art3.leaf, LEAF_ON[0], LEAF_ON[1], .7), prop("ar", lambda p: art.arrow(p, 560, 440, 720, 630), 0, 0, 1, True), prop("ht", art3.heat, 740, 640, .8, True)],
      fx=[("show", "w:small.", "ar"), ("show", "w:back", "ht"), ("face", "w:still", "tumble", "sad")], words=[("w:still", "STILL HOT!", .26, .2, .9, "pill")]),
    S("jungle", C("jungle", "milo", "body", 820, 20, -70), "Is one leaf big enough for a whole elephant? Yes, or no?", q=True, beat="obstacle1", tag="question: yes or no", pause=3.0, hide=["tumble"],
      fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    S("jungle", C("jungle", "tumble", "all", 1000, 30, -40), "No. My back is hot, hot, hot.", who="tumble", beat="obstacle1", tag="the leaf slides off", hide=["milo"],
      props=[prop("lf", art3.leaf, LEAF_ON[0], LEAF_ON[1], .7)],
      fx=[("face", 0.02, "tumble", "sad"), ("to", "w:back", "#{p}lf_w", {"x": 1090, "y": 880, "rotation": 40, "transformOrigin": "50% 50%", "duration": .9, "ease": "power1.in"}, "the leaf slides off")]),
    # ------------------------------------------------------------ OBSTACLE 2: a fan (arms get tired) - and Tumble's own two fans
    S("canopy", C("canopy", "mango", "head", 900, 40, -110), "Hello down there! You look hot, Tumble.", who="mango", beat="obstacle2", tag="Mango appears",
      fx=[("arm", "w:You", "mango", "r", -50), ("fromto", 0, "#{p}mango_w", {"y": 60}, {"y": 462, "duration": .7, "ease": "back.out(1.4)"}, "Mango drops down on her tail")]),
    S("canopy", (860, 560, 1500), "It is Mango, the spider monkey! And Mango has an idea.", beat="obstacle2", tag="Mango has an idea", words=[("w:Mango,", "MANGO", .2, .3, 1.1, "pill"), ("w:idea.", "AN IDEA!", .8, .3, 1.0, "sun")]),
    S("bigtree", (760, 700, 1400), "I will fan you with a palm leaf. Flap, flap, flap!", who="mango", beat="obstacle2", tag="Mango fans", hide=["milo"],
      props=[prop("fan", art3.fan, 642, 795, .5), prop("wd", art3.wind, 720, 660, .7, True)],
      fx=[ARM_UP, ("to", "w:fan", "#{p}fan_w", {"rotation": 22, "transformOrigin": "50% 100%", "duration": .25, "yoyo": True, "repeat": 15, "ease": "sine.inOut"}, "Mango fans"), ("show", "w:Flap,", "wd"),
          ("to", "w:Flap,", "#{p}wd_w", {"x": 900, "duration": .9, "repeat": 2, "ease": "none"}, "the wind blows")], words=[("w:Flap,", "FLAP!", .5, .18, 1.1, "sun")]),
    S("bigtree", C("bigtree", "tumble", "head", 820, -60, 0), "Ooh, a little wind! That feels nice.", who="tumble", beat="obstacle2", tag="a little wind", hide=["milo", "mango"],
      props=[prop("wd", art3.wind, 760, 620, .7)], fx=[("face", 0.02, "tumble", "happy"), ("to", 0.1, "#{p}wd_w", {"x": 980, "duration": 1.0, "repeat": 3, "ease": "none"}, "the wind blows")]),
    S("bigtree", C("bigtree", "mango", "all", 760, 20, -20), "Oh dear. My arms are tired!", who="mango", beat="obstacle2", tag="tired arms", hide=["milo", "tumble"],
      props=[prop("fan", art3.fan, 642, 795, .5)], fx=[ARM_UP, ("face", 0.02, "mango", "sad"), ("to", "w:arms", "#{p}fan_w", {"x": 588, "y": 898, "rotation": 80, "transformOrigin": "50% 100%", "duration": .6, "ease": "power2.in"}, "the fan goes down"),
          ("to", "w:arms", "#{p}mango-ar", {"rotation": 0, "svgOrigin": "58 -206", "duration": .6, "ease": "power2.in"}, "")]),
    S("bigtree", (800, 660, 1500), "The fan stops. And Tumble is hot again.", beat="obstacle2", tag="hot again", hide=["milo"],
      props=[prop("fan", art3.fan, 588, 898, .5), prop("ht", art3.heat, 1000, 560, .9, True)], fx=[("to", 0, "#{p}fan_w", {"rotation": 80, "transformOrigin": "50% 100%", "duration": .01}, ""), ("show", "w:hot", "ht"), ("face", "w:hot", "tumble", "sad")], words=[("w:again.", "HOT AGAIN!", .3, .2, .9, "pill")]),
    S("bigtree", C("bigtree", "milo", "body", 780, 70, 0), "Wait! Tumble, you have two fans of your own. Your ears!", beat="obstacle2", tag="Milo: your ears", hide=["tumble", "mango"],
      fx=[("hop", "w:Wait!", "milo")], words=[("w:ears!", "YOUR EARS!", .74, .2, .8, "sun")]),
    S("bigtree", C("bigtree", "tumble", "head", 780, -40, 0), "My ears? Flap, flap, flap!", who="tumble", beat="obstacle2", tag="Tumble flaps his ears", hide=["milo", "mango"],
      fx=[("face", 0.02, "tumble", "wow"), FLAP("w:Flap,", n=9)], words=[("w:Flap,", "FLAP, FLAP!", .26, .2, 1.0, "sun")]),
    S("paper_blue", (960, 540, 1600), "An elephant flaps its big ears to cool its body on warm days.", beat="fact", tag="fact: ears cool the body",
      props=[prop("eb", art3.ear_board, 960, 600, .85), prop("wd", art3.wind, 600, 400, .8, True)],
      fx=[("to", "w:flaps", "#{p}ebe-ear", {"rotation": 14, "svgOrigin": EAR, "duration": .2, "yoyo": True, "repeat": 13, "ease": "sine.inOut"}, "the ear flaps"), ("show", "w:cool", "wd")],
      words=[("w:ears", "BIG EARS", .24, .16, 1.0, "sun"), ("w:cool", "= COOL!", .74, .16, 1.0, "")]),
    S("bigtree", C("bigtree", "milo", "body", 820, 20, 0), "Can you flap your arms like big ears? Flap, flap, flap!", q=True, beat="obstacle2", tag="question: flap your arms", hide=["tumble", "mango"],
      fx=[("hop", "w:Flap,", "milo", 2)], words=[("w:Flap,", "FLAP!", .8, .3, 1.4, "sun")]),
    S("bigtree", C("bigtree", "tumble", "all", 1000, 20, -30), "That helps a little. But the sun is still so hot.", who="tumble", beat="obstacle2", tag="helps a little", hide=["milo", "mango"],
      fx=[FLAP(0.1, n=5), ("face", "w:But", "tumble", "sad")]),
    # ------------------------------------------------------------ OBSTACLE 3: the shade moves
    S("bigtree", (900, 640, 1700), "Then Mango points. Look! Shade, under the tallest tree.", beat="obstacle3", tag="shade", hide=["milo"], cam2=(1040, 640, 1560),
      props=[prop("sh", art3.shade, 1480, 950, 1.0), prop("ar", lambda p: art.arrow(p, 1600, 500, 1580, 880), 0, 0, 1, True)], fx=[("arm", "w:points.", "mango", "r", -70), ("show", "w:Shade,", "ar")], words=[("w:Shade,", "SHADE", .8, .24, 1.0, "pill")]),
    S("bigtree", (1220, 660, 1400), "Tumble steps into the shade. Oh, so cool!", beat="obstacle3", tag="into the shade", hide=["milo", "mango"],
      props=[prop("sh", art3.shade, 1480, 950, 1.0)], fx=[("walk", 0.1, "tumble", 420, 2.6), ("face", "w:so", "tumble", "happy")], words=[("w:cool!", "COOL!", .22, .2, 1.1, "sun")]),
    S("bigtree", (1480, 660, 900), "This is the best spot. I will stay right here.", who="tumble", beat="obstacle3", tag="the best spot", hide=["milo", "mango"],
      move={"tumble": (1400, 930, .62)}, props=[prop("sh", art3.shade, 1480, 950, 1.0)], fx=[("face", 0.02, "tumble", "happy"), ("nod", "w:stay", "tumble")]),
    S("bigtree", (1300, 560, 1700), "But the sun moves across the sky. And the shade moves, too.", beat="obstacle3", tag="the shade moves", hide=["milo", "mango"],
      move={"tumble": (1400, 930, .62)}, props=[prop("sh", art3.shade, 1480, 950, 1.0), prop("hs", art3.hot_sun, 900, 270, .7)],
      fx=[("to", 0.2, "#{p}hs_w", {"x": 1350, "duration": 4.0, "ease": "none"}, "the sun moves"), ("to", "w:shade", "#{p}sh_w", {"x": 1800, "duration": 2.0, "ease": "power1.inOut"}, "the shade moves away")],
      words=[("w:moves,", "IT MOVES!", .3, .5, .9, "pill")]),
    S("bigtree", (1560, 700, 1300), "Step. Step. Step. Tumble follows the shade.", beat="obstacle3", tag="follows the shade", hide=["milo", "mango"],
      move={"tumble": (1400, 930, .62)}, props=[prop("sh", art3.shade, 1800, 950, 1.0)], fx=[("walk", 0.1, "tumble", 300, 3.4)], words=[("w:Step.", "STEP!", .2, .2, 1.0, "sun")]),
    S("bigtree", (1560, 660, 1500), "Now the sun is right over the tree. And the shade is tiny!", beat="obstacle3", tag="the shade is tiny", hide=["milo", "mango"],
      move={"tumble": (1700, 930, .62)}, props=[prop("sh", art3.shade, 1800, 950, 1.0), prop("hs", art3.hot_sun, 1400, 380, .55)],
      fx=[("to", "w:shade", "#{p}sh_w", {"scaleX": .22, "scaleY": .6, "transformOrigin": "50% 50%", "duration": 1.2, "ease": "power1.inOut"}, "the shade shrinks")], words=[("w:tiny!", "TINY SHADE!", .28, .42, .8, "pill")]),
    S("bigtree", (1700, 760, 1100), "Only my toes fit in the shade!", who="tumble", beat="obstacle3", tag="only my toes", hide=["milo", "mango"],
      move={"tumble": (1700, 930, .62)}, props=[prop("sh", art3.shade, 1800, 950, .24)], fx=[("face", 0.02, "tumble", "sad")], words=[("w:toes", "ONLY TOES!", .27, .2, .9, "sun")]),
    # ------------------------------------------------------------ LOW MOMENT: three tries, still hot - and the only cool thing is MUD (gentle: nobody cries)
    S("mudhole", WIDE, "Hot and tired, Tumble walks on.", trans="iris", beat="low", tag="walks on", hide=["mama", "mango", "milo"], cam2=(900, 560, 1760),
      move={"tumble": (200, 874, .58)}, fx=[("walk", 0.1, "tumble", 320, 3.0), ("face", 0.02, "tumble", "sad")]),
    S("mudhole", (1000, 900, 1300), "And there it is. A big, brown, muddy puddle.", beat="low", tag="the puddle", hide=["mama", "mango", "milo", "tumble"], cam2=(1000, 880, 1500),
      words=[("w:muddy", "MUDDY PUDDLE", .5, .2, 1.0, "pill")], fx=[("snd", "w:muddy", "pop")]),
    S("mudhole", C("mudhole", "tumble", "head", 800, -40, 10), "Oh no. Mud! I must stay clean for the photo.", who="tumble", beat="low", tag="I must stay clean", hide=["mama", "mango", "milo"],
      fx=[("face", 0.02, "tumble", "wow"), ("face", "w:I", "tumble", "sad")]),
    S("mudhole", C("mudhole", "tumble", "all", 1100, 160, -120), "I tried a hat. I tried a fan. I tried the shade.", who="tumble", beat="low", tag="three tries", hide=["mama", "mango", "milo"],
      props=[prop("t1", art3.leaf, 820, 420, .34, True), prop("t2", art3.fan, 1020, 500, .36, True), prop("t3", lambda p: art3.shade(p, 90, 26), 1160, 440, 1.0, True)],
      fx=[("show", "w:hat.", "t1"), ("show", "w:fan.", "t2"), ("show", "w:shade.", "t3"), ("face", 0.02, "tumble", "sad")]),
    S("mudhole", C("mudhole", "tumble", "head", 760, -40, 20), "And I am still so hot.", who="tumble", beat="low", tag="still so hot", hide=["mama", "mango", "milo"],
      props=[prop("sw", art3.sweat, *P("mudhole", "tumble", "top", 124, 20), .66, True)], fx=[("face", 0.02, "tumble", "sad"), ("show", "w:still", "sw")]),
    S("mudhole", (620, 640, 1500), "Tumble stops by the puddle. He feels hot and grumpy. His friends come close.", beat="low", tag="friends come close", hide=["mama"],
      move={"mango": (60, 878, .52), "milo": (860, 500, .7)},
      fx=[("face", 0.02, "tumble", "sad"), ("to", "w:He", "#{p}tumble-brow", {"rotation": -16, "y": -4, "transformOrigin": "50% 50%", "duration": .3}, "Tumble frowns"),
          ("to", "w:His", "#{p}mango_w", {"x": 190, "duration": 1.2, "ease": "power1.inOut"}, "Mango comes close"), ("fly", "w:His", "milo", 900, 520, 1.2)]),
    S("mudhole", C("mudhole", "milo", "body", 780, 70, 0), "Tumble is hot and grumpy. What could help him cool down?", q=True, beat="low", tag="question: what could help", hide=["mama", "tumble", "mango"], pause=2.4,
      fx=[("hop", "w:What", "milo")], words=[("w:cool", "COOL DOWN?", .74, .2, .8, "pill")]),
    S("mudhole", (400, 650, 1200), "It is okay, Tumble. We will think of something together.", who="mango", beat="low", tag="together", hide=["mama", "milo"],
      fx=[("face", 0.02, "tumble", "sad"), ("arm", "w:We", "mango", "r", -40)], words=[("w:together.", "TOGETHER", .72, .16, .9, "pill")]),
    # ------------------------------------------------------------ SOLUTION: Tumble sees what Mama does, asks, and chooses the mud himself
    S("mudhole", (1300, 700, 1500), "Splash! What is that sound?", beat="solution", tag="splosh", hide=["tumble", "mango", "milo"], props=[MF(), prop("sp", art3.splash, 1280, 985, .6, True)],
      fx=[("fromto", 0, "#{p}mama_w", {"x": 1900}, {"x": 1440, "duration": .5, "ease": "power1.out"}, "Mama steps into the mud"), ("show", 0.5, "sp", .9), ("snd", 0.5, "whoosh")],
      words=[("w:Splash!", "SPLASH!", .18, .25, .9, "sun")]),
    S("mudhole", WIDE, "Mama! You are all muddy!", who="tumble", beat="solution", tag="Mama is muddy", hide=["mango", "milo"], cam2=(1000, 560, 1800), props=[MF()],
      fx=[("face", 0.02, "tumble", "wow"), ("hop", "w:Mama!", "tumble")], words=[("w:muddy!", "ALL MUDDY!", .5, .16, 1.0, "sun")]),
    S("mudhole", C("mudhole", "mama", "head", 900, 40, 40), "Of course, little one. Mud keeps an elephant cool.", who="mama", beat="solution", tag="mud keeps cool", hide=["tumble", "mango", "milo"], props=[MF()],
      fx=[("nod", "w:Of", "mama")], words=[("w:cool.", "COOL!", .17, .2, 1.1, "sun")]),
    S("mudhole", (1250, 640, 1300), "And mud keeps the hot sun off our skin.", who="mama", beat="solution", tag="mud keeps the sun off", hide=["tumble", "mango", "milo"],
      props=[MF(), prop("hs", art3.hot_sun, 800, 470, .55, True)], fx=[("show", "w:hot", "hs"), ("blinkslow", "w:skin.", "mama-eye", 1)], words=[("w:sun", "SUN SHIELD", .74, .16, .8, "pill")]),
    S("paper_pink", (960, 540, 1600), "Elephants roll in mud. The mud protects their skin from the sun.", beat="fact", tag="fact: mud protects from the sun",
      actors=[("e", "elephant_mud", 1000, 960, .8)], props=[prop("hs", art3.hot_sun, 600, 350, .8), prop("ar", lambda p: art.arrow(p, 720, 470, 850, 570), 0, 0, 1, True), prop("x", art.cross, 900, 590, .8, True)],
      fx=[SPIN, ("show", "w:protects", "ar"), ("show", "w:sun.", "x")], words=[("w:mud.", "MUD", .72, .14, 1.2, "sun"), ("w:protects", "= SUN SHIELD", .74, .27, .7, "pill")]),
    S("mudhole", C("mudhole", "milo", "body", 760, 20, 0), "So mud is like a sun hat, for an elephant's whole body!", beat="solution", tag="Milo: a mud hat", hide=["mama", "tumble", "mango"],
      fx=[("hop", "w:sun", "milo")], words=[("w:whole", "A MUD HAT!", .74, .22, .9, "sun")]),
    S("mudhole", C("mudhole", "tumble", "head", 800, -40, 10), "But, Mama. What about my photo?", who="tumble", beat="solution", tag="what about my photo", hide=["mama", "mango", "milo"],
      fx=[("face", 0.02, "tumble", "sad"), ("lookat", 0.3, "tumble", -6)]),
    S("mudhole", C("mudhole", "mama", "head", 900, 40, 40), "A happy elephant makes the very best photo.", who="mama", beat="solution", tag="a happy elephant", hide=["tumble", "mango", "milo"], props=[MF()],
      fx=[("nod", "w:happy", "mama"), ("blinkslow", "w:best", "mama-eye", 1)], words=[("w:happy", "HAPPY!", .15, .2, 1.0, "sun")]),
    S("mudhole", (700, 760, 1200), "Then, one toe. One foot. And...", who="tumble", beat="solution", tag="one toe", hide=["mama", "mango", "milo"],
      fx=[("face", 0.02, "tumble", "wow"), ("to", "w:toe.", "#{p}tumble_w", {"x": 580, "y": 900, "duration": .4, "ease": "power1.out"}, "one toe"),
          ("to", "w:foot.", "#{p}tumble_w", {"x": 640, "y": 930, "duration": .4, "ease": "power1.out"}, "one foot")], words=[("w:toe.", "ONE TOE...", .7, .14, .9, "pill")]),
    S("mudhole", (700, 700, 1500), "Splash! Tumble jumps into the mud!", beat="solution", tag="splash", actors=IN_MUD, hide=["mama", "mango", "milo"], props=[MF(), prop("sp", art3.splash, 350, 975, .6, True), prop("sq", art3.splash, 1070, 975, .6, True)],
      move={"tumble": (600, 760, .6)},
      fx=[NOMUD(), ("to", 0.05, "#{p}tumble_w", {"x": 620, "y": 1000, "duration": .45, "ease": "power2.in"}, "Tumble jumps in"), ("show", 0.5, "sp", .9), ("show", 0.5, "sq", .9, False), ("snd", 0.5, "whoosh"),
          ("to", 0.55, "#{p}tumble .mud", {"opacity": 1, "duration": .3}, "Tumble is muddy"), ("face", 0.6, "tumble", "happy")], words=[("w:Splash!", "SPLASH!", .5, .16, 1.4, "sun")]),
    S("mudhole", (700, 760, 1000), "Oh! It is so cool. And so squishy!", who="tumble", beat="solution", tag="so cool", actors=IN_MUD, hide=["mama", "mango", "milo"], props=[MF()],
      fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:cool.", "tumble"), FLAP("w:squishy!", n=5)], words=[("w:cool.", "SO COOL!", .24, .2, 1.0, "sun")]),
    S("mudhole", C("mudhole", "mama", "head", 900, 40, 40), "That is my muddy little elephant!", who="mama", beat="solution", tag="my muddy little elephant", actors=IN_MUD, hide=["tumble", "mango", "milo"], props=[MF()],
      fx=[("nod", "w:muddy", "mama"), ("blinkslow", "w:little", "mama-eye", 1)]),
    S("mudhole", (690, 720, 1300), "He rolls to the left. He rolls to the right.", beat="solution", tag="rolls", actors=IN_MUD, hide=["mama", "mango", "milo"], props=[MF()],
      fx=[("to", "w:left.", "#{p}tumble", {"rotation": -14, "transformOrigin": "50% 100%", "duration": .5, "ease": "sine.inOut"}, "Tumble rolls left"),
          ("to", "w:right.", "#{p}tumble", {"rotation": 14, "transformOrigin": "50% 100%", "duration": .6, "ease": "sine.inOut"}, "Tumble rolls right"),
          ("to", "e:right.", "#{p}tumble", {"rotation": 0, "duration": .4}, "")], words=[("w:left.", "ROLL!", .24, .2, 1.1, "sun")]),
    S("mudhole", C("mudhole", "milo", "body", 820, 20, 0), "Can you roll your arms like Tumble? Roll, roll, roll!", q=True, beat="solution", tag="question: roll your arms", hide=["mama", "tumble", "mango"],
      fx=[("hop", "w:Roll,", "milo", 2)], words=[("w:Roll,", "ROLL!", .8, .3, 1.4, "sun")]),
    S("mudhole", (290, 720, 900), "That looks like fun! Plop. A drop of mud lands on Mango's nose.", beat="solution", tag="mud on Mango's nose", hide=["mama", "milo", "tumble"],
      props=[prop("ms", lambda p: art3.mud_spot(p, 9), 760, 500, 1.0, True)],
      fx=[("show", "w:Plop.", "ms"), ("to", "w:Plop.", "#{p}ms_w", {"x": P("mudhole", "mango", "head")[0], "y": P("mudhole", "mango", "head", 0, 14)[1], "duration": .5, "ease": "power1.in"}, "mud flies to Mango"),
          ("snd", "w:drop", "pop"), ("face", "w:lands", "mango", "wow")], words=[("w:Plop.", "PLOP!", .74, .2, 1.1, "sun")]),
    S("mudhole", WIDE, "Now everyone is cool. And everyone is laughing.", beat="solution", tag="everyone is cool", actors=IN_MUD, cam2=(980, 560, 1820), props=[MF()],
      fx=[("hop", "w:cool.", "milo"), ("hop", "w:laughing.", "tumble"), ("nod", "w:laughing.", "mama"), ("arm", "w:everyone", "mango", "l", 60)], words=[("w:laughing.", "MUD PARTY!", .5, .14, 1.0, "sun")]),
    # ------------------------------------------------------------ WARM ENDING: the photo
    S("zoo_eve", WIDE, "Back at the zoo, the sun is low. It is photo time!", trans="iris", beat="ending", tag="photo time", cam2=(940, 560, 1800), props=[CAM_E()],
      words=[("w:photo", "PHOTO TIME!", .5, .14, 1.0, "sun")]),
    S("zoo_eve", C("zoo_eve", "tumble", "head", 820, -40, 10), "I am not clean, Milo. But I am cool, and I am happy!", who="tumble", beat="ending", tag="cool and happy", hide=["mama", "mango", "milo"],
      fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:happy!", "tumble")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 760, 0, 0), "Then that is the photo I want! Everybody, say mud!", beat="ending", tag="say mud", hide=["mama", "mango", "tumble"],
      fx=[("hop", "w:Everybody,", "milo")], words=[("w:mud!", "SAY MUD!", .74, .22, .9, "sun")]),
    S("zoo_eve", (1000, 600, 1700), "Three, two, one. Click!", beat="ending", tag="click", hide=["milo"], props=[prop("fl", art3.flash, 960, 540, 1.0, True)],
      words=[("w:Three,", "3", .2, .18, 1.6, "sun"), ("w:two,", "2", .3, .18, 1.6, "sun"), ("w:one.", "1", .4, .18, 1.6, "sun")],
      fx=[("fromto", "w:Click!", "#{p}fl_w", {"opacity": .95}, {"opacity": 0, "duration": .5, "ease": "power1.out"}, "the camera flashes"), ("snd", "w:Click!", "ding"), ("hop", "w:Click!", "tumble")]),
    S("paper_blue", (960, 540, 1920), "And here is the photo. Muddy, cool, and smiling!", beat="ending", tag="the photo", actors=PHOTO,
      props=[prop("fr", lambda p: art3.frame(p, 1240, 560), 960, 510, 1.0)],
      words=[("w:Muddy,", "MUDDY", .27, .792, .6, "pill"), ("w:cool,", "COOL", .5, .792, .6, "pill"), ("w:smiling!", "SMILING!", .75, .792, .6, "pill")]),
    S("zoo_eve", C("zoo_eve", "mango", "all", 760, 0, -20), "That is the best photo ever!", who="mango", beat="ending", tag="best photo ever", hide=["milo", "tumble", "mama"],
      fx=[("hop", "w:best", "mango", 2), ("arm", "w:best", "mango", "l", 60), ("arm", "w:best", "mango", "r", -60)]),
    S("zoo_eve", (1200, 660, 1400), "Mama wraps her trunk around Tumble. A big, muddy trunk hug.", beat="ending", tag="trunk hug", hide=["milo", "mango"], move={"tumble": (900, 940, .6)},
      props=[prop("h1", lambda p: art2.heart(p), 1040, 560, 1.0, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 960, 590, .6, True)],
      fx=[("trunk", "w:wraps", "mama", 34, .8), ("lookat", "w:wraps", "mama", 8), ("show", "w:big,", "h1"), ("show", "w:hug.", "h2"),
          ("to", "w:big,", "#{p}h1_w,#{p}h2_w", {"y": "-=60", "duration": 1.6, "ease": "sine.out"}, "")], words=[("w:hug.", "TRUNK HUG", .21, .2, .7, "pill")]),
    S("zoo_eve", C("zoo_eve", "tumble", "head", 800, -20, 0), "I love mud days, Mama.", who="tumble", beat="ending", tag="I love mud days", hide=["milo", "mango", "mama"],
      fx=[("face", 0.02, "tumble", "happy"), ("blinkslow", "w:love", "tumble-eye", 1)]),
    S("zoo_eve", C("zoo_eve", "mama", "head", 900, 60, 50), "Me too, my little Tumble.", who="mama", beat="ending", tag="me too", hide=["milo", "mango", "tumble"], fx=[("nod", "w:too,", "mama")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 130, 0), "It is okay to get a little messy when you play.", beat="ending", tag="the lesson", hide=["mama", "tumble", "mango"],
      words=[("w:messy", "MESSY IS OKAY", .73, .22, .75, "pill")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 40, 0), "Do you remember? What keeps the sun off an elephant's skin? A fan, or mud?", q=True, beat="ending", tag="question: fan or mud", pause=3.2,
      hide=["mama", "tumble", "mango"], cam2=C("zoo_eve", "milo", "body", 830, 40, -60), fx=[("signs", "w:fan,", ["FAN", "MUD"], 1, "wait:2.0")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 40, 0), "And what does an elephant flap to cool down? Its ears, or its tail?", q=True, beat="ending", tag="question: ears or tail", pause=3.2,
      hide=["mama", "tumble", "mango"], cam2=C("zoo_eve", "milo", "body", 830, 40, -60), fx=[("signs", "w:ears,", ["EARS", "TAIL"], 0, "wait:2.0")]),
    S("zoo_eve", (980, 560, 1880), "Friends help friends. Hooray, hooray! What a muddy, happy day!", beat="ending", tag="the rhyme", cam2=(1000, 560, 1780),
      fx=[("hop", "w:Hooray,", "milo"), ("hop", "w:hooray!", "tumble"), ("hop", "w:muddy,", "mango")]),
    S("zoo_eve", WIDE, who="", sing=SING_END_A, beat="song", tag="song: hooray", cam2=(980, 560, 1880),
      fx=[("hop", 1.0, "tumble"), ("hop", 2.2, "mango"), ("nod", 3.2, "mama")], words=[(TB(3), "HOORAY!", .72, .2, 1.05, "sun")]),
    S("zoo_eve", (1145, 620, 1500), who="", sing=SING_END_B, beat="song", tag="song: muddy happy day", cam2=(1145, 620, 1420), hide=["milo", "mango"],
      props=[prop("h1", lambda p: art2.heart(p), 1020, 430, .9, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 940, 380, .6, True)],
      fx=[("hop", 0.6, "tumble"), ("nod", 1.6, "mama"), ("show", TB(1.5), "h1"), ("show", TB(3.5), "h2"), ("hop", 3.0, "tumble")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 0, 0), "See you on the next adventure, friends!", beat="ending", tag="goodbye", hide=["mama", "mango"], fx=[("hop", "w:next", "milo")],
      words=[("w:next", "SEE YOU SOON!", .74, .2, .9, "pill")]),
]

# thumbnail (thumb.py): the example in the picture (a muddy, grinning Tumble in the mud), 3 words at most, none of the title's words, no watermark
THUMBS = {
    "za_ep02": {"place": "mudhole", "cam": (960, 540, 1920),
                "actors": [("tumble_mud", 620, 1010, 1.05, False, 'gsap.set("#P-trunk",{rotation:-70,svgOrigin:"392 -430"});')],
                "props": [(art3.mud_front, 960, 960, 1.0), (art3.splash, 1590, 940, 1.0)],
                "words": [("SPLASH TIME!", 560, 125, 132, "sun")]},
}
