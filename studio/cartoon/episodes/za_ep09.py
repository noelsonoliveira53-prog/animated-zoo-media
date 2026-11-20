"""za_ep09 - Milo's Zoo Adventures: "Sandy's First Night Away" (cartoon adventure, the 3D music-and-sync process: "beat").
Milo brings Sandy the baby camel a card: a sleepover at the zoo, her first night away from Mama. Mama walks her to the zoo and will be at the
gate in the morning. In the barn the fluffy bed is too soft (Sandy kneels down in the straw instead, the way camels kneel on the sand); the
night is too quiet (the friends look at the stars in the zoo garden; Sandy is still wide awake); she misses Mama's hum (at home Mama hums
to her every night). Low moment: "maybe I'm too little for a sleepover". Sandy works it out herself: she can teach her friends Mama's hum,
so it is here with them. She SAYS the rhyme, then the tune is played by the bells and the soft band while they snuggle and she falls asleep.
In the morning Mama is at the gate. Nobody is hurt, lost, crying or trapped: Mama knows where Sandy is and when she will fetch her, Mama is
shown calm under the same moon, Sandy is a little sad but never cries. Mama camel has no voice (no new voice in this film).

FACTS, read at the source on Nov 20 2026, about 9:10 AM ET (each page fetched by the session's page reader, which quoted these sentences):
 [SDZ] San Diego Zoo Wildlife Alliance, "Camel", animals.sandiegozoo.org/animals/camel (node/173)
   "Mothers and their newborns hum to each other."
   "After a gestation of 12 to 14 months, a newborn camel is able to walk beside the mother within half an hour."
 [PBS] PBS Nature, "Camel Fact Sheet", pbs.org/wnet/nature/blog/camel-fact-sheet
   "Mothers and their newborns hum to each other."  "The newborn is able to walk within half an hour after it is born."
 [OAK] Oakland Zoo, "Dromedary Camel", oaklandzoo.org/animals/dromedary-camel
   "Their knees, and usually chest, are calloused in a way to protect them from the hot sand when bending down."
   "A newborn camel is able to walk within half an hour after they are born"
 Said as animal facts in the film (three fact boards and questions), each from a quote above: camel mamas and their babies hum to each
 other [SDZ, PBS]; a baby camel can walk beside its mama when it is only half an hour old [SDZ, PBS, OAK]; camels have thick, tough skin on
 their knees, so they can kneel down on hot sand [OAK].
 Not animal facts, said as what happens in THIS story: Sandy kneeling down to sleep in the straw, Mama humming to Sandy every night, the tune.
 Nothing is said about how or how long camels sleep (no source read today says it).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep07 as A7
import art_za_ep09 as A
import art_zc_ep05 as A5
import art_zc_ep07 as AZ7
import kit
from kit import Kit, S, prop

EP = {"id": "za_ep09", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "sandy": {"voice": "af_sarah", "speed": .82, "pitch": 3, "formant": 1.1, "gain": .88},
               "tumble": {"voice": "am_puck", "speed": .85, "pitch": 5, "formant": 1.16, "gain": .66}},
      "title": "Sandy's First Night Away", "thumb_text": "SWEET DREAMS!",
      "series": "Milo's Zoo Adventures",
      "description": ("A sleepover at the zoo! Sandy the baby camel spends her very first night away from Mama, with Milo the bluebird and Tumble the baby elephant. "
                      "But the fluffy bed is too soft, the night is too quiet, and Sandy misses Mama's hum. How can her friends help her fall asleep? "
                      "A gentle bedtime adventure for ages 2-6 about friendship and feeling at home, with questions to answer, a star count and a soft lullaby tune.\n"
                      "Kids see how camel mamas and their babies hum to each other, how a baby camel can walk beside its mama when it is only half an hour old, "
                      "and how camels have thick, tough skin on their knees, so they can kneel down on hot sand.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (camel); PBS Nature (camel fact sheet); Oakland Zoo (dromedary camel)."),
      "tags": ["baby camel", "camel for kids", "sleepover story for kids", "bedtime story for kids", "first night away", "baby elephant", "animal stories for kids",
               "friendship story for kids", "kids adventure cartoon", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "dunes": [("mama", "camel", 1330, 905, .8, True), ("sandy", "calf", 640, 935, .54), ("milo", "milo", 820, 330, .72, False, True)],
    "zoo_eve": [("tumble", "tumble", 1440, 940, .6, True), ("sandy", "calf", 620, 940, .52), ("milo", "milo", 1020, 500, .68, False, True)],
    "barn": [("tumble", "tumble", 300, 935, .58), ("sandy", "calf", 980, 935, .52), ("milo", "milo", 1560, 930, .7)],
    "zoo_night": [("tumble", "tumble", 300, 940, .58), ("sandy", "calf", 900, 940, .52), ("milo", "milo", 1440, 600, .68, False, True)],
    "night": [("mama", "camel", 760, 905, .95)],
    "zoo": [("mama", "camel", 1400, 905, .8, True), ("sandy", "calf", 560, 935, .52), ("tumble", "tumble", 140, 935, .56), ("milo", "milo", 1000, 430, .68, False, True)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
MCL = lambda place, dx=0, dy=-70, w=820, stage=None: C(place, "milo", "body", w, dx, dy, stage=stage)     # Milo asks a question: low in the frame, under the signs

# Sandy lying in the straw: her feet point sinks 90 below the floor, the straw mound in front hides her legs, the blanket lies over her back
LY = 1025
LIE = [("tumble", "tumble", 300, 935, .58), ("sandy", "calf", 980, LY, .52), ("milo", "milo", 1560, 930, .7)]
STRAW = lambda hidden=False: prop("st", A.straw, 1020, 972, .82, hidden)
BLANKET = lambda hidden=False: prop("bk", A.blanket, 980, LY, .52, hidden)
SLEEPY = lambda at: ("face", at, "sandy", "sleepy")
NOTES = lambda x, y, s=1.0, hidden=True: prop("nt", A.notes3, x, y, s, hidden)
RISE = lambda at, d=3.0: ("to", at, "#{p}nt_w", {"y": "-=80", "duration": d, "ease": "sine.out"}, "the notes float up")
HEARTS = lambda x, y: [prop("h1", lambda p: art2.heart(p), x, y, .7, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), x + 80, y - 30, .5, True)]
UP = lambda at: ("to", at, "#{p}h1_w,#{p}h2_w", {"y": "-=60", "duration": 1.6, "ease": "sine.out"}, "")
CARD = lambda x, y, s=.6: prop("cd", A.card, x, y, s)
CUSH = lambda: prop("cu", A.cushion, 1000, 965, 1.0)

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. Nobody sings or hums with a voice: the rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_MOON = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "G4:2 E4:1 C4:1 D4:1 G4:1 B4:1", "rest": 1},     # moon is round (C bar), stars are bright (G bar)
                                 {"text": "~ ~ ~ ~ ~ ~", "notes": "A4:2 F4:1 C4:1 E4:1 G4:1 C4:1", "rest": 1}])    # close your eyes (F bar), and sleep tight (C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "D5:1 B4:1 G4:1 B4:1 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune

CNT_STAR = 1.35                                  # seconds from "One" to the last number, read from the timing file
MAMA_GATE = [("mama", "camel", 1400, 905, .8, True), ("sandy", "calf", 800, 935, .52)]

SHOTS = [
    # ------------------------------------------------------------ HOOK: a sleepover invitation, in the first 5 seconds
    S("dunes", C("dunes", "milo", "body", 1000, 60, 60), "A sleepover! Sandy, you are invited to a sleepover at the zoo!", beat="hook", tag="hook: the sleepover card",
      hide=["mama", "sandy"], props=[CARD(970, 340)], fx=[("face", 0.02, "milo", "wow"), ("hop", "w:sleepover!", "milo"), ("to", "w:invited", "#{p}cd_w", {"rotation": 8, "duration": .2, "yoyo": True, "repeat": 3}, "the card wiggles")],
      words=[("w:sleepover!", "SLEEPOVER!", .64, .2, 1.0, "sun")]),
    S("dunes", WIDE, "Hello, I'm Milo! This is Sandy the baby camel, and her Mama, in the sandy desert.", tag="dunes wide: Milo, Sandy, Mama", cam2=(980, 560, 1820),
      props=[CARD(970, 340)], fx=[("hop", "w:Hello,", "milo"), ("hop", "w:Sandy", "sandy"), ("nod", "w:Mama,", "mama")],
      words=[("w:Sandy", "SANDY", .33, .36, .7, "pill"), ("w:Mama,", "MAMA", .7, .3, .7, "pill")]),
    S("dunes", C("dunes", "sandy", "head", 820, -40, 30), "A sleepover? My very first night away from Mama!", who="sandy", beat="goal", tag="Sandy: my first night away", hide=["mama", "milo"],
      fx=[("face", 0.02, "sandy", "wow"), ("lookat", "w:Mama!", "sandy", -10)], words=[("w:first", "FIRST NIGHT!", .62, .2, .85, "sun")]),
    S("dunes", (1000, 640, 1500), "Mama camel nuzzles Sandy. Have fun, little one. I will be at the zoo gate in the morning.", beat="goal", tag="Mama: at the gate in the morning", hide=["milo"],
      actors=[("mama", "camel", 1270, 905, .8, True), ("sandy", "calf", 700, 935, .54)], props=HEARTS(980, 330),
      fx=[("lookat", "w:nuzzles", "mama", 18), ("show", "w:nuzzles", "h1"), ("show", "w:fun,", "h2"), UP("w:fun,"), ("lookat", "w:I", "mama", 0), ("nod", "w:morning.", "sandy")],
      words=[("w:morning.", "IN THE MORNING", .5, .16, .7, "pill")]),
    S("dunes", MCL("dunes", 0, -40, 800), "Where will Sandy sleep tonight? At the zoo, or at home?", q=True, beat="goal", tag="question: zoo or home", pause=3.2, hide=["mama", "sandy"],
      fx=[("signs", "w:zoo,", ["THE ZOO", "HOME"], 0, "wait:1.8")]),
    S("dunes", WIDE, "Sandy walks beside Mama, step, step, step, all the way to the zoo.", beat="goal", tag="walking beside Mama", cam2=(1000, 560, 1820),
      actors=[("sandy", "calf", 840, 935, .54), ("mama", "camel", 280, 905, .8)],
      fx=[("walk", 0.1, "sandy", 560, 5.0), ("walk", 0.1, "mama", 560, 5.0)], words=[("w:step,:1", "STEP, STEP!", .62, .2, .85, "sun")]),
    S("paper", (960, 560, 1500), "A baby camel can walk beside its mama, when it is only half an hour old!", beat="fact", tag="fact: walks at half an hour old",
      actors=[("mama", "camel", 640, 900, .66), ("sandy", "calf", 1000, 935, .5)], props=[prop("ck", art.clock, 1530, 300, .62)],
      fx=[("walk", "w:walk", "mama", 160, 3.2), ("walk", "w:walk", "sandy", 160, 3.2),
          ("fromto", "w:half", "#{p}ck-half", {"opacity": 0}, {"opacity": .85, "duration": .4}, "half the clock lights up"),
          ("fromto", "w:half", "#{p}ck-min", {"rotation": 0, "svgOrigin": "0 0"}, {"rotation": 180, "duration": 1.2, "ease": "power1.inOut"}, "the minute hand goes half way")],
      words=[("w:half", "HALF AN HOUR", .46, .18, .62, "sun")]),
    S("dunes", C("dunes", "sandy", "all", 960, 40, -60), "Can a baby camel walk, soon after it is born? Yes, or no?", q=True, beat="goal", tag="question: walk soon yes or no", pause=3.2,
      hide=["mama", "milo"], cam2=C("dunes", "sandy", "all", 900, 40, -80), fx=[("nod", "w:born?", "sandy"), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ at the zoo at sunset: Tumble, bye-bye Mama, play and supper
    S("zoo_eve", WIDE, "At the zoo, Tumble the baby elephant is waiting. Hooray, a sleepover!", trans="iris", beat="goal", tag="zoo at sunset: Tumble waits", cam2=(980, 560, 1820),
      actors=[("tumble", "tumble", 1440, 940, .6, True), ("sandy", "calf", 780, 940, .52), ("mama", "camel", 300, 905, .78), ("milo", "milo", 1020, 500, .68, False, True)],
      fx=[("trunk", "w:Tumble", "tumble", -90, .4), ("hop", "w:Hooray,", "sandy"), ("hop", "w:Hooray,", "milo")], words=[("w:Hooray,", "HOORAY!", .55, .2, .95, "sun")]),
    S("zoo_eve", C("zoo_eve", "tumble", "head", 860, -40, 40), "Hi, Sandy! We can play, and have supper, and sleep in the cozy barn!", who="tumble", beat="goal", tag="Tumble: play, supper, barn",
      hide=["sandy", "milo"], fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:play,", "tumble", -60, .4), ("trunk", "w:barn!", "tumble", 0, .4)],
      words=[("w:barn!", "COZY BARN!", .5, .1, .7, "pill")]),
    S("zoo_eve", (760, 620, 1500), "Bye-bye, Mama! See you in the morning!", who="sandy", beat="goal", tag="Sandy: bye-bye, Mama",
      actors=[("sandy", "calf", 960, 940, .52, True), ("mama", "camel", 380, 905, .78)], hide=["milo", "tumble"],
      fx=[("face", 0.02, "sandy", "happy"), ("nod", "w:Bye-bye,", "sandy"), ("nod", "w:See", "mama")], words=[("w:Bye-bye,", "BYE-BYE!", .62, .18, .9, "sun")]),
    S("zoo_eve", (1000, 620, 1600), "They play hide and seek, and eat a yummy supper. Munch, munch!", beat="goal", tag="play and supper",
      actors=[("tumble", "tumble", 1380, 940, .6, True), ("sandy", "calf", 600, 940, .52), ("milo", "milo", 940, 520, .66, False, True)],
      props=[prop("hy", A5.hay, 860, 945, .55), prop("hy2", A5.hay, 1120, 945, .45)],
      fx=[("hop", "w:hide", "milo"), ("trunk", "w:seek,", "tumble", -40, .4), ("chew", "w:Munch,", "sandy", 1.6), ("trunk", "w:Munch,", "tumble", -100, .5)],
      words=[("w:Munch,", "MUNCH, MUNCH!", .8, .2, .8, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: the fluffy bed is too soft
    S("barn", WIDE, "Bedtime! In the cozy barn, Tumble has a big, fluffy bed for Sandy.", trans="iris", beat="obstacle1", tag="the barn: the fluffy bed", cam2=(980, 560, 1820),
      actors=[("tumble", "tumble", 300, 935, .58), ("sandy", "calf", 1400, 935, .52, True), ("milo", "milo", 1720, 930, .7)], props=[CUSH()],
      fx=[("trunk", "w:fluffy", "tumble", -40, .4), ("to", "w:fluffy", "#{p}cu-top", {"scaleY": 1.06, "transformOrigin": "50% 100%", "duration": .25, "yoyo": True, "repeat": 1}, "the bed puffs")],
      words=[("w:Bedtime!", "BEDTIME!", .62, .18, .95, "sun")]),
    S("barn", (1060, 600, 1300), "Wobble, wobble! Oh, this bed is too soft! I sink down, down, down!", who="sandy", beat="obstacle1", tag="Sandy: too soft",
      actors=[("sandy", "calf", 960, 810, .52)], props=[CUSH()],
      fx=[("face", 0.02, "sandy", "wow"), ("to", "w:Wobble,", "#{p}sandy", {"rotation": 5, "svgOrigin": "0 0", "duration": .2, "yoyo": True, "repeat": 5}, "Sandy wobbles"),
          ("to", "w:sink", "#{p}sandy", {"y": 70, "duration": 1.6, "ease": "power1.in"}, "Sandy sinks"), ("to", "w:sink", "#{p}cu-top", {"scaleY": .8, "transformOrigin": "50% 100%", "duration": 1.6}, "the bed squashes")],
      words=[("w:soft!", "TOO SOFT!", .7, .2, .9, "pill")]),
    S("barn", MCL("barn", 0, -60, 760), "Is the fluffy bed too soft, or too hard?", q=True, beat="obstacle1", tag="question: soft or hard", pause=3.2, hide=["tumble", "sandy"],
      fx=[("signs", "w:soft,", ["TOO SOFT", "TOO HARD"], 0, "wait:1.8")]),
    S("barn", C("barn", "sandy", "head", 820, -60, 40), "At home, I kneel down on the warm sand, knees first.", who="sandy", beat="obstacle1", tag="Sandy: I kneel on the sand", hide=["tumble", "milo"],
      fx=[("face", 0.02, "sandy", "happy"), ("lookat", "w:kneel", "sandy", 14), ("lookat", "w:first.", "sandy", 0)], words=[("w:kneel", "KNEEL DOWN", .62, .2, .85, "sun")]),
    S("paper_pink", (960, 560, 1500), "Camels have thick, tough skin on their knees, so they can kneel down on hot sand.", beat="fact", tag="fact: tough knees",
      actors=[("mama", "camel", 760, 930, .9)], props=[prop("kp", A.knee_pad, 760, 930, .9), prop("rg", A.ring, 760 + round(166 * .9), 930 - round(130 * .9), .9, True)],
      fx=[("show", "w:knees,", "rg"), ("to", "w:tough", "#{p}kp_w", {"scale": 1.04, "duration": .2, "yoyo": True, "repeat": 1}, ""),
          ("to", "w:kneel", "#{p}rg_w", {"scale": 1.12, "duration": .25, "yoyo": True, "repeat": 3}, "the ring pulses")],
      words=[("w:knees,", "TOUGH KNEES", .74, .3, .8, "sun"), ("w:hot", "HOT SAND", .74, .5, .7, "pill")]),
    S("barn", C("barn", "tumble", "head", 860, 40, 40), "Where do camels have tough, thick skin? On their knees, or on their ears?", q=True, who="milo", beat="obstacle1", tag="question: knees or ears", pause=3.2,
      hide=["sandy", "milo"], fx=[("face", 0.02, "tumble", "happy"), ("signs", "w:knees,", ["KNEES", "EARS"], 0, "wait:1.8")]),
    S("barn", (1000, 640, 1400), "Tumble brings soft straw. Sandy kneels down, knees first. Ahh, just right!", beat="obstacle1", tag="Sandy kneels in the straw",
      actors=[("sandy", "calf", 980, 935, .52), ("milo", "milo", 1560, 930, .7)], props=[STRAW()],
      fx=[("to", "w:kneels", "#{p}sandy", {"y": LY - 935, "duration": 1.0, "ease": "power2.inOut"}, "Sandy kneels down"), ("face", "w:Ahh,", "sandy", "happy"), ("hop", "w:right!", "milo")],
      words=[("w:right!", "JUST RIGHT!", .5, .18, .9, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 2: the night is too quiet
    S("barn", C("barn", "sandy", "head", 820, -60, 40, stage=LIE), "But now it is so quiet. At home, the desert wind goes whoosh.", who="sandy", beat="obstacle2", tag="Sandy: so quiet",
      actors=LIE, hide=["tumble", "milo"], props=[STRAW(), BLANKET()], fx=[("face", 0.02, "sandy", "sad"), ("lookat", "w:whoosh.", "sandy", -10)],
      words=[("w:quiet.", "SO QUIET...", .62, .2, .85, "pill")]),
    S("barn", C("barn", "milo", "body", 760, 0, -20, stage=LIE), "I know! Let's tiptoe outside, and look at the stars!", beat="obstacle2", tag="Milo: look at the stars", actors=LIE, hide=["tumble", "sandy"],
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:know!", "milo"), ("hop", "w:stars!", "milo")], words=[("w:stars!", "STARS!", .68, .22, .95, "sun")]),
    S("zoo_night", WIDE, "In the zoo garden, the moon is round and bright, and the sky is full of stars.", trans="iris", beat="obstacle2", tag="the zoo garden at night", cam2=(1000, 500, 1760),
      fx=[("lookat", "w:moon", "sandy", -20), ("trunk", "w:sky", "tumble", -100, .6), ("to", "w:stars.", ".{p}star", {"opacity": 1, "duration": .3, "stagger": .01}, "the stars twinkle")],
      words=[("w:moon", "THE MOON", .66, .3, .8, "pill")]),
    S("zoo_night", (1000, 380, 1500), "How many big stars can you see? Count with me! One, two, three, four, five!", q=True, beat="obstacle2", tag="question: count the stars", pause=1.0,
      props=[prop("b%d" % k, A.big_star, x, y, .8, True) for k, (x, y) in enumerate(((480, 260), (720, 160), (960, 250), (1180, 140), (1340, 330)))],
      fx=[("count", "w:One,", 5, CNT_STAR, {"x": 640, "y": 470})] + [("show", w, "b%d" % k) for k, w in enumerate(("w:One,", "w:two,", "w:three,", "w:four,", "w:five!"))]),
    S("zoo_night", C("zoo_night", "tumble", "head", 860, 40, 40), "Hush, hush! Can you be very quiet, like the night?", q=True, who="tumble", beat="obstacle2", tag="be quiet along", pause=1.0, hide=["sandy", "milo"],
      cam2=C("zoo_night", "tumble", "head", 800, 40, 60), fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:Hush,", "tumble", -20, .4), ("trunk", "w:hush!:2", "tumble", 0, .4), ("trunk", "w:quiet,", "tumble", -20, .4)],
      words=[("w:Hush,", "HUSH, HUSH!", .6, .18, .8, "pill")]),
    S("zoo_night", C("zoo_night", "sandy", "head", 820, -40, 40), "The stars are so pretty. But I am still wide awake.", who="sandy", beat="obstacle2", tag="Sandy: still wide awake", hide=["tumble", "milo"],
      fx=[("lookat", 0.02, "sandy", -18), ("lookat", "w:But", "sandy", 0), ("face", "w:awake.", "sandy", "wow")], words=[("w:awake.", "WIDE AWAKE!", .5, .1, .8, "pill")]),
    S("zoo_night", (700, 640, 1400), "Is it day, or night?", q=True, beat="obstacle2", tag="question: day or night", pause=3.2, hide=["milo"], cam2=(760, 620, 1300),
      fx=[("trunk", "w:day,", "tumble", -60, .4), ("signs", "w:day,", ["DAY", "NIGHT"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 3: she misses Mama's hum
    S("barn", (1000, 620, 1500), "Back in the barn, Sandy lies in the straw. Her eyes stay open.", trans="iris", beat="obstacle3", tag="back in bed, eyes open",
      actors=LIE, props=[STRAW(), BLANKET()], fx=[("face", 0.02, "tumble", "sleepy"), ("face", "w:open.", "sandy", "sad")], words=[("w:open.", "EYES OPEN", .5, .16, .8, "pill")]),
    S("barn", C("barn", "sandy", "head", 760, -60, 40, stage=LIE), "At home, Mama hums to me every night. I miss Mama's hum.", who="sandy", beat="obstacle3", tag="Sandy: I miss Mama's hum",
      actors=LIE, hide=["tumble", "milo"], props=[STRAW(), BLANKET()], fx=[("face", 0.02, "sandy", "sad"), ("lookat", "w:miss", "sandy", 10)],
      words=[("w:hum.", "MAMA'S HUM", .42, .12, .8, "pill")]),
    S("night", (900, 560, 1500), "Far away in the desert, Mama camel looks up at the same big moon.", trans="iris", beat="obstacle3", tag="Mama under the moon", cam2=(880, 520, 1400),
      fx=[("lookat", "w:looks", "mama", -22)], words=[("w:same", "THE SAME MOON", .79, .44, .6, "sun")]),
    S("paper_blue", (960, 560, 1500), "Camel mamas and their babies hum to each other!", beat="fact", tag="fact: mamas and babies hum",
      actors=[("mama", "camel", 1290, 905, .72, True), ("sandy", "calf", 700, 935, .62)], props=[NOTES(880, 390, 1.0)],
      fx=[("lookat", 0.1, "mama", 14), ("lookat", 0.1, "sandy", -10), ("show", "w:hum", "nt"), ("to", "w:hum", "#{p}nt_w", {"y": "-=50", "duration": 2.4, "ease": "sine.out"}, "the notes float up")],
      words=[("w:hum", "HUM, HUM!", .8, .18, .8, "sun")]),
    S("night", C("night", "mama", "head", 800, 0, 60), "What do camel mamas and babies do? Hum, or roar?", q=True, beat="obstacle3", tag="question: hum or roar", pause=3.2,
      cam2=C("night", "mama", "head", 740, 0, 80), fx=[("signs", "w:Hum,", ["HUM", "ROAR"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ LOW MOMENT: maybe too little for a sleepover (gentle: nobody cries)
    S("barn", (960, 600, 1700), "The barn is quiet and dark, and Mama is far away. Sandy feels a little sad.", beat="low", tag="the quiet dark barn",
      actors=LIE, props=[STRAW(), BLANKET()], fx=[("face", 0.02, "sandy", "sad"), ("face", "w:sad.", "milo", "sad")], words=[("w:sad.", "A LITTLE SAD", .5, .16, .8, "pill")]),
    S("barn", C("barn", "sandy", "head", 700, -60, 40, stage=LIE), "Maybe I am too little for a sleepover.", who="sandy", beat="low", tag="Sandy: too little",
      actors=LIE, hide=["tumble", "milo"], props=[STRAW(), BLANKET()], fx=[("face", 0.02, "sandy", "sad"), ("lookat", "w:little", "sandy", 12)]),
    S("barn", C("barn", "tumble", "head", 860, 40, 40, stage=LIE), "Don't worry, Sandy. We are right here with you.", who="tumble", beat="low", tag="Tumble: we are right here",
      actors=LIE, hide=["sandy", "milo"], fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:here", "tumble", -40, .5)], words=[("w:here", "RIGHT HERE", .42, .1, .75, "sun")]),
    S("barn", C("barn", "milo", "body", 760, 0, -40, stage=LIE), "Can good friends help Sandy feel better? Yes, or no?", q=True, beat="low", tag="question: friends help yes or no", pause=3.2,
      actors=LIE, hide=["tumble", "sandy"], fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: Sandy works it out herself, teaches Mama's hum (the rhyme SAID, then the tune on instruments)
    S("barn", C("barn", "sandy", "all", 900, 0, -40, stage=LIE), "I know! I can teach you Mama's hum. Then a little bit of home is here with us!", who="sandy", beat="solution", tag="Sandy: I know!",
      actors=LIE, hide=["tumble", "milo"], props=[STRAW(), BLANKET()], fx=[("face", 0.02, "sandy", "happy"), ("lookat", "w:know!", "sandy", -12), ("lookat", "w:home", "sandy", 0)],
      words=[("w:know!", "I KNOW!", .44, .12, .85, "sun")]),
    S("barn", (1000, 640, 1500), "Yes! Teach us, Sandy! Tumble and Milo snuggle up close.", beat="solution", tag="the friends snuggle up",
      actors=[("tumble", "tumble", 480, 935, .58), ("sandy", "calf", 980, LY, .52), ("milo", "milo", 1560, 930, .7)], props=[STRAW(), BLANKET()],
      fx=[("hop", "w:Yes!", "milo"), ("walk", "w:Tumble", "tumble", 120, 1.2), ("fly", "w:Milo", "milo", 1340, 700, 1.0)], words=[("w:snuggle", "SNUGGLE UP", .5, .16, .85, "sun")]),
    S("barn", (980, 600, 1500), "Moon is round, stars are bright. Close your eyes, and sleep tight!", who="sandy", beat="solution", tag="the moon rhyme",
      actors=[("tumble", "tumble", 600, 935, .58), ("sandy", "calf", 980, LY, .52), ("milo", "milo", 1340, 700, .62, False, True)], props=[STRAW(), BLANKET()],
      fx=[("face", 0.02, "sandy", "happy"), ("lookat", "w:Moon", "sandy", -14), ("lookat", "w:Close", "sandy", 6), ("face", "w:Close", "tumble", "sleepy")],
      words=[("w:Moon", "MOON IS ROUND", .5, .1, .62, "sun"), ("w:Close", "SLEEP TIGHT!", .5, .21, .62, "pill")]),
    S("barn", (1000, 600, 1400), who="", sing=SING_MOON, beat="song", tag="song: moon is round", cam2=(1000, 640, 1200),
      actors=[("tumble", "tumble", 600, 935, .58), ("sandy", "calf", 980, LY, .52), ("milo", "milo", 1340, 700, .62, False, True)], props=[STRAW(), BLANKET(), NOTES(820, 440, 1.0)],
      fx=[("show", TB(0), "nt", None, False), RISE(TB(0), 4.4), ("face", TB(4), "milo", "sleepy"), SLEEPY(TB(6)), ("sleep", TB(12), "sandy"),
          ("word", TB(0), "MOON IS ROUND", {"x": 1000, "y": 340, "size": 70, "cls": "sun", "hold": 4.4})],
      words=[(TB(8), "SLEEP TIGHT", .5, .22, .65, "pill")]),
    S("barn", (1060, 600, 1200), "Her friends hum Mama's tune with her, soft and slow. And Sandy falls fast asleep. Sweet dreams!", beat="solution", tag="Sandy asleep: sweet dreams",
      actors=[("tumble", "tumble", 600, 935, .58), ("sandy", "calf", 980, LY, .52), ("milo", "milo", 1340, 700, .62, False, True)],
      props=[STRAW(), BLANKET(), prop("zz", AZ7.zzz, 1150, 540, .7, True)],
      fx=[("sleep", 0.6, "sandy"), ("face", 0.02, "tumble", "sleepy"), ("show", "w:asleep.", "zz"), ("to", "w:asleep.", "#{p}zz_w", {"y": "-=40", "duration": 2.4, "ease": "sine.out"}, "")],
      words=[("w:Sweet", "SWEET DREAMS!", .4, .14, .8, "sun")]),
    S("barn", MCL("barn", 0, -60, 760, stage=[("milo", "milo", 1560, 930, .7)]), "What helped Sandy fall asleep? Mama's tune, or a loud drum?", q=True, beat="solution", tag="question: tune or drum", pause=3.2,
      actors=[("milo", "milo", 1560, 930, .7)], fx=[("signs", "w:Mama's", ["MAMA'S TUNE", "A DRUM"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ WARM ENDING: morning, Mama at the gate
    S("zoo", WIDE, "Good morning! The sun is up. And look who is at the zoo gate!", trans="iris", beat="ending", tag="morning: Mama at the gate", cam2=(1000, 560, 1820),
      actors=[("mama", "camel", 1400, 905, .8, True), ("sandy", "calf", 520, 935, .52), ("tumble", "tumble", 190, 935, .56), ("milo", "milo", 860, 420, .68, False, True)],
      fx=[("walk", 0.1, "sandy", 280, 3.0), ("walk", 0.1, "tumble", 240, 3.0), ("nod", "w:gate!", "mama")], words=[("w:morning!", "GOOD MORNING!", .5, .16, .85, "sun")]),
    S("zoo", C("zoo", "sandy", "all", 900, 0, -60, stage=MAMA_GATE), "Mama! I slept all night! My friends hummed your tune with me.", who="sandy", beat="ending", tag="Sandy tells Mama",
      actors=MAMA_GATE, hide=["mama"], fx=[("face", 0.02, "sandy", "happy"), ("hop", "w:Mama!", "sandy"), ("nod", "w:tune", "sandy")], words=[("w:night!", "ALL NIGHT!", .5, .14, .8, "sun")]),
    S("zoo", (1120, 600, 1500), "Mama camel and Sandy hum hello, nose to nose.", beat="ending", tag="Mama and Sandy nose to nose",
      actors=[("mama", "camel", 1400, 905, .8, True), ("sandy", "calf", 900, 935, .52)], props=HEARTS(980, 450) + [NOTES(760, 580, .8)],
      fx=[("lookat", "w:Mama", "mama", 16), ("lookat", "w:Sandy", "sandy", -8), ("show", "w:hum", "nt", None, False), RISE("w:hum", 2.4), ("show", "w:nose", "h1"), ("show", "w:nose.:2", "h2"), UP("w:nose.:2")],
      words=[("w:hello,", "HELLO, MAMA!", .32, .14, .75, "sun")]),
    S("zoo", (760, 620, 1700), "Then Mama and Sandy walk home together, side by side.", beat="ending", tag="walking home side by side", cam2=(900, 600, 1600),
      actors=[("sandy", "calf", 760, 935, .52), ("mama", "camel", 220, 905, .8)], fx=[("walk", 0.1, "sandy", 520, 4.0), ("walk", 0.1, "mama", 520, 4.0)],
      words=[("w:together,", "TOGETHER", .5, .12, .8, "sun")]),
    S("zoo", (1250, 520, 1500), "Who was waiting at the gate? Mama, or Milo?", q=True, beat="ending", tag="question: Mama or Milo", pause=3.2,
      actors=[("mama", "camel", 1400, 905, .8, True)], fx=[("nod", "w:gate?", "mama"), ("signs", "w:Mama,", ["MAMA", "MILO"], 0, "wait:1.8")]),
    S("zoo", C("zoo", "milo", "body", 760, 0, -10), "Thank you for the sleepover, Sandy!", beat="ending", tag="Milo: thank you", hide=["tumble", "sandy", "mama"],
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:sleepover,", "milo")], words=[("w:Thank", "THANK YOU!", .64, .22, .85, "sun")]),
    S("zoo", C("zoo", "tumble", "head", 860, 40, 40), "Come again soon! Our barn is your barn too.", who="tumble", beat="ending", tag="Tumble: come again", hide=["sandy", "milo", "mama"],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:soon!", "tumble", -90, .5)], words=[("w:soon!", "COME AGAIN!", .42, .12, .8, "pill")]),
    S("zoo", C("zoo", "sandy", "head", 820, -40, 30), "Thank you, friends! You made my first night away so cozy.", who="sandy", beat="ending", tag="Sandy: thank you", hide=["tumble", "milo", "mama"],
      fx=[("face", 0.02, "sandy", "happy"), ("nod", "w:friends!", "sandy")], words=[("w:cozy.", "SO COZY!", .46, .14, .8, "sun")]),
    S("zoo", (960, 600, 1800), "When you miss someone, a song from home can come with you. And good friends help, too.", beat="ending", tag="the lesson", cam2=(1000, 600, 1700),
      fx=[("hop", "w:miss", "milo"), ("nod", "w:song", "sandy"), ("nod", "w:home", "mama"), ("trunk", "w:friends", "tumble", -80, .4), ("hop", "w:too.", "sandy")],
      words=[("w:song", "A SONG FROM HOME", .78, .1, .6, "sun")]),
    S("zoo", C("zoo", "milo", "body", 900, 40, 0), "Do you remember? When can a baby camel walk beside its mama? At half an hour old, or at one year old?", q=True, beat="ending", tag="question: half an hour or a year", pause=3.2,
      hide=["tumble", "sandy", "mama"], cam2=C("zoo", "milo", "body", 830, 40, -60), fx=[("hop", "w:remember?", "milo"), ("signs", "w:half", ["HALF AN HOUR", "ONE YEAR"], 0, "wait:1.8")]),
    S("zoo", C("zoo", "sandy", "all", 1000, 60, -40), "And what keeps a camel's knees safe on hot sand? Tough skin, or soft feathers?", q=True, beat="ending", tag="question: tough skin or feathers", pause=3.2,
      hide=["tumble", "milo", "mama"], cam2=C("zoo", "sandy", "all", 940, 60, -60), fx=[("nod", "w:knees", "sandy"), ("signs", "w:Tough", ["TOUGH SKIN", "FEATHERS"], 0, "wait:1.8")]),
    S("zoo", (960, 540, 1920), "Moon is round, stars are bright. Close your eyes, and sleep tight!", beat="ending", tag="the closing rhyme", cam2=(980, 560, 1880),
      fx=[("hop", "w:Moon", "milo"), ("nod", "w:bright.", "sandy"), ("trunk", "w:eyes,", "tumble", -80, .4), ("nod", "w:tight!", "mama")],
      words=[("w:Moon", "MOON IS ROUND", .78, .12, .65, "sun")]),
    S("zoo", WIDE, who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(980, 560, 1880),
      fx=[("hop", 1.0, "sandy"), ("trunk", 2.0, "tumble", -90, .4), ("hop", 2.2, "milo")], words=[(TB(3), "HOORAY!", .76, .16, 1.0, "sun")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, 0), "Next time: Poppy's first slide on the ice! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure", hide=["tumble", "sandy", "mama"],
      fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .8, .2, .66, "sun"), ("w:See", "SEE YOU SOON!", .8, .33, .56, "pill")]),
]

# thumbnail (thumb.py): the example in the picture (Sandy under a starry blanket in the straw, friends beside her, the moon in the window), 3 words at most, none of the title's words, no watermark
THUMBS = {
    "za_ep09": {"place": "barn", "cam": (1060, 590, 1340),
                "actors": [("calf", 980, LY, .56, False, ''), ("tumble", 600, 935, .6, False, ''), ("milo", 1400, 760, .62, False, '')],
                "props": [(A.straw, 1020, 975, .88), (A.blanket, 980, LY, .56)],
                "words": [("SWEET DREAMS!", 1000, 200, 140, "sun", -4)]},
}
