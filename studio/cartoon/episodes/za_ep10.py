"""za_ep10 - Milo's Zoo Adventures: "Can Poppy Slide Down the Snowy Hill?" (cartoon adventure, the 3D music-and-sync process: "beat"). Arctic week, adventure 1.
Milo and Tumble visit Poppy the polar bear cub in the snowy Arctic. Everybody slides down Poppy's big snowy hill, but Poppy stays at the top: she
is shy. She sits at the edge (the hill looks so long), she holds Milo's wing (Milo is too little and floats up), she watches Tumble zoom (too fast
for her, she likes slow) and stops each time. Low moment: "maybe sliding is not for me" (a little sad, never crying; her friends stay with her).
Poppy finds the way herself: she looks at her paws (wide, with tiny grippy bumps), walks down slow and steady to the little ledge in the middle and
slides from there, her friends sliding slowly beside her. At the bottom: "I did it!", the rhyme said, the tune on instruments, "Can we go again?
From the top this time!", and she slides from the very top. Nobody is hurt, lost, crying or trapped; nobody slips or falls; sliding is slow and
gentle play on snow, sitting or on the tummy.

FACTS, read at the source on Nov 20 2026, about 2:45 PM ET (each page fetched by the session's page reader, which quoted these sentences):
 [PBS] PBS Nature, "Bears of the Last Frontier: Polar Bear Fact Sheet", pbs.org/wnet/nature/bears-of-the-last-frontier-polar-bear-fact-sheet/7053
   "The paws are broad to distribute their weight as their walk across ice and snow,"
   "The bottoms of their paws are also covered with small bumps called papillae."
   "Polar bears also have fur on the bottoms of their paws, providing extra warmth and creating traction on the ice."
 [SDZ] San Diego Zoo Wildlife Alliance Library, "Polar Bear Fact Sheet: Physical Characteristics", ielc.libguides.com/sdzg/factsheets/polarbear/characteristics
   "Wide feet"  "Large, paddle-like"  "Soles of feet have small dermal bumps or papillae"  "May help with traction on ice"  "Even foot pads are furred in winter"
 [SNE] Science News Explores, "Tiny bumps on polar bear paws help them get traction on snow", snexplores.org (2022 study, Orndorf, Dhinojwala et al.)
   "Super-small structures on the bears' paw pads offer extra friction."  "That extra grip could keep polar bears from slipping on snow, says Ali Dhinojwala."
 Said as animal facts in the film (two fact boards, questions, recap): polar bears have big, wide paws that spread out their weight when they walk on
 snow and ice [PBS, SDZ]; tiny bumps on their paw pads help them grip the snow [PBS, SDZ, SNE]; fur on the bottoms of their paws keeps them warm [PBS, SDZ].
 Not animal facts, said as what happens in THIS story: Poppy sliding, the little ledge, the rhyme and the tune. Nothing is said about polar bears
 sliding in the wild (no page read today says it).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep09 as A9
import art_za_ep10 as A
import kit
from kit import Kit, S, prop
from intro import INTRO_STAGES, intro_shots      # the main intro, right after the hook and as the last shots (owner, Nov 20 4:50 PM)

EP = {"id": "za_ep10", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "poppy": {"voice": "af_jessica", "speed": .88, "pitch": 4, "formant": 1.2, "gain": .9},
               "tumble": {"voice": "am_puck", "speed": .85, "pitch": 5, "formant": 1.16, "gain": .66}},
      "title": "Can Poppy Slide Down the Snowy Hill?", "thumb_text": "WHEE!",
      "series": "Milo's Zoo Adventures",
      "description": ("Can Poppy slide down the big snowy hill? Everybody is sliding, but Poppy the polar bear cub stays at the top: she feels shy. "
                      "Milo the bluebird and Tumble the baby elephant wait with her, until Poppy finds her very own way down. "
                      "A gentle Arctic adventure for ages 2-6 about trying something new a little bit at a time, with questions to answer, a count-along and a snowy tune.\n"
                      "Kids see how polar bears have big, wide paws that spread out their weight on snow and ice, how tiny bumps on their paw pads help them grip the snow, "
                      "and how fur on the bottoms of their paws keeps them warm.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nPBS Nature (polar bear fact sheet); San Diego Zoo Wildlife Alliance Library (polar bear fact sheet); Science News Explores (polar bear paws)."),
      "tags": ["polar bear for kids", "polar bear cub", "polar bear paws", "arctic animals for kids", "snow day", "sliding", "baby elephant", "animal stories for kids",
               "friendship story for kids", "kids adventure cartoon", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

HY = A.hill_y
STAGES = {
    "arctic": [("tumble", "tumble", 330, 900, .55), ("poppy", "bear", 1180, 900, .6, True), ("milo", "milo", 770, 560, .62, False, True)],
    "snowhill": [("poppy", "bear", 440, A.TOP_Y, .5), ("tumble", "tumble", 1760, 935, .5, True), ("milo", "milo", 1260, 560, .6, False, True)],
    "hilltop": [("tumble", "tumble", 280, 880, .55), ("poppy", "bear", 800, 880, .62), ("milo", "milo", 1180, 620, .6, False, True)],
    "hillmid": [("tumble", "tumble", 300, 920, .55), ("poppy", "bear", 800, 920, .6), ("milo", "milo", 1180, 640, .6, False, True)],
    "snowbottom": [("poppy", "bear", 1180, 935, .6, True), ("tumble", "tumble", 1780, 935, .55, True), ("milo", "milo", 960, 600, .62, False, True)],
    "arctic_eve": [("tumble", "tumble", 330, 900, .55), ("poppy", "bear", 1120, 900, .6, True), ("milo", "milo", 730, 560, .62, False, True)],
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
MCL = lambda place, dx=0, dy=-70, w=820, stage=None: C(place, "milo", "body", w, dx, dy, stage=stage)     # Milo asks a question: low in the frame, under the signs

SL = lambda who, kind, x, s: (who, kind, x, HY(x), s)                                       # a slider standing on the snowhill slope at x
SLIDE = lambda at, who, x0, x1, d, ease="sine.inOut": ("to", at, "#{p}%s_w" % who, {"x": "+=%d" % (x1 - x0), "y": "+=%d" % (HY(x1) - HY(x0)), "duration": d, "ease": ease}, who + " slides down")
SPRAY = lambda name, x, y, s=.6: prop(name, A.spray, x, y, s, True)
FLAKES = lambda xs: [prop("f%d" % k, A.snowflake, x, y, .5) for k, (x, y) in enumerate(xs)]

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. The rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_PAWS = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "E4:1 G4:1 C5:2 B4:1 G4:1 D5:1", "rest": 1},      # wide paws, hold on tight (C bar, G bar)
                                 {"text": "~ ~ ~ ~ ~ ~", "notes": "A4:1 C5:1 F4:2 E4:1 G4:1 C4:1", "rest": 1}])     # down we slide, snowy white (F bar, C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "B4:1 D5:1 G4:1 D5:1 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune
CNT3 = 0.95                                      # seconds from "One" to "three", read from the timing file

TOPST = [("tumble", "tumble", 280, 880, .55), ("poppy", "bear", 800, 880, .62), ("milo", "milo", 1180, 620, .6, False, True)]

SHOTS = [
    # ------------------------------------------------------------ HOOK: the big hill, everybody slides, Poppy at the top (first 5 seconds)
    S("snowhill", (1000, 580, 1720), "Can Poppy slide down the big, snowy hill? Whee! Here goes Tumble!", beat="hook", tag="hook: Poppy at the top, Tumble slides",
      actors=[("poppy", "bear", 440, A.TOP_Y, .5), SL("tumble", "tumble_slide", 820, .45), ("milo", "milo", 1250, 340, .55, False, True)],
      fx=[("face", 0.02, "poppy", "wow"), SLIDE("w:Whee!", "tumble", 820, 1500, 2.6), ("fly", "w:Whee!", "milo", 1600, 560, 2.6), ("lookat", "w:Tumble!", "poppy", 12)],
      words=[("w:Whee!", "WHEE!", .66, .2, 1.0, "sun")]),
    *intro_shots(),      # the main intro, right after the hook
    # ------------------------------------------------------------ GOAL: visiting Poppy in the Arctic
    S("arctic", WIDE, "Hello, I'm Milo! Tumble and I are visiting Poppy the polar bear cub, in the snowy Arctic.", trans="iris", beat="goal", tag="arctic wide: Milo, Tumble, Poppy",
      cam2=(980, 560, 1820), fx=[("hop", "w:Hello,", "milo"), ("trunk", "w:Tumble", "tumble", -60, .4), ("nod", "w:Poppy", "poppy")],
      words=[("w:Poppy", "POPPY", .6, .3, .7, "pill"), ("w:Arctic.", "THE ARCTIC", .5, .14, .7, "sun")]),
    S("arctic", C("arctic", "poppy", "head", 820, -60, 40), "Hi, Milo! Hi, Tumble! Come and see my big snowy hill. Everybody slides on it!", who="poppy", beat="goal", tag="Poppy: my snowy hill",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:Hi,:2", "poppy"), ("lookat", "w:hill.", "poppy", -8), ("lookat", "w:Everybody", "poppy", 0)],
      words=[("w:hill.", "SNOWY HILL", .72, .14, .8, "sun")]),
    S("arctic", C("arctic", "tumble", "head", 860, 40, 40), "A sliding hill? Hooray! I love sliding!", who="tumble", beat="goal", tag="Tumble: hooray, sliding",
      hide=["poppy", "milo"], fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:Hooray!", "tumble", -100, .4), ("hop", "w:love", "tumble")],
      words=[("w:Hooray!", "HOORAY!", .6, .1, .9, "sun")]),
    S("arctic", C("arctic", "poppy", "all", 1000, -40, -40), "I have big paws! Can you make big paws too? Spread your hands out wide!", q=True, who="poppy", beat="goal", tag="copy me: big paws",
      pause=3.0, hide=["tumble", "milo"], cam2=C("arctic", "poppy", "all", 940, -40, -60),
      fx=[("face", 0.02, "poppy", "happy"), ("hop", "w:big", "poppy"), ("nod", "w:Spread", "poppy"), ("hop", "w:wide!", "poppy")],
      words=[("w:big", "BIG PAWS!", .72, .14, .85, "sun"), ("w:Spread", "SPREAD WIDE!", .72, .26, .7, "pill")]),
    S("arctic", MCL("arctic", 0, -40, 800), "What color is Poppy's fluffy fur? White, or green?", q=True, beat="goal", tag="question: white or green", pause=3.2, hide=["tumble", "poppy"],
      fx=[("signs", "w:White,", ["WHITE", "GREEN"], 0, "wait:1.8")]),
    S("arctic", WIDE, "Poppy walks over the snow, on her big, wide paws. Step, step, step!", beat="goal", tag="Poppy walks on the snow", cam2=(1000, 560, 1820),
      actors=[("tumble", "tumble", 200, 900, .55), ("poppy", "bear", 760, 900, .6), ("milo", "milo", 500, 560, .62, False, True)],
      fx=[("walk", 0.1, "poppy", 520, 4.6), ("walk", 0.4, "tumble", 380, 4.2), ("fly", 0.6, "milo", 900, 520, 4.0)], words=[("w:Step,", "STEP, STEP!", .7, .2, .85, "sun")]),
    S("paper", (960, 560, 1500), "Polar bears have big, wide paws. Wide paws spread out their weight, when they walk on snow and ice.", beat="fact", tag="fact: wide paws spread the weight",
      actors=[("poppy", "bear", 620, 900, .7)], props=[prop("pw", A.paw_wide, 1300, 520, .8)],
      fx=[("walk", 0.2, "poppy", 120, 2.4), ("to", "w:wide,:1", "#{p}pw_w", {"scale": 1.08, "duration": .25, "yoyo": True, "repeat": 1}, "the paw print pulses"),
          ("fromto", "w:spread", "#{p}pw-arr", {"opacity": 0}, {"opacity": 1, "duration": .4}, "the arrows show the weight spreading out"),
          ("to", "w:snow", "#{p}pw-arr", {"scale": 1.1, "transformOrigin": "50% 50%", "duration": .3, "yoyo": True, "repeat": 3}, "")],
      words=[("w:wide,:1", "WIDE PAWS", .7, .2, .7, "sun"), ("w:snow", "SNOW AND ICE", .7, .8, .6, "pill")]),
    S("arctic", C("arctic", "poppy", "all", 960, 40, -40), "Are a polar bear's paws big and wide, or tiny?", q=True, beat="goal", tag="question: wide or tiny", pause=3.2,
      hide=["tumble", "milo"], cam2=C("arctic", "poppy", "all", 900, 40, -60), fx=[("nod", "w:paws", "poppy"), ("signs", "w:big", ["BIG AND WIDE", "TINY"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ the hill: everybody slides, Poppy stays at the top
    S("snowhill", WIDE, "Here is the snowy hill! It is so big, and so white.", trans="iris", beat="goal", tag="the snowy hill wide", cam2=(980, 560, 1820),
      actors=[("poppy", "bear", 560, A.TOP_Y, .5), ("tumble", "tumble", 190, A.TOP_Y, .36), ("milo", "milo", 900, 300, .55, False, True)],
      fx=[("lookat", "w:hill!", "poppy", 10), ("hop", "w:big,", "tumble"), ("fly", "w:white.", "milo", 980, 330, 1.2)], words=[("w:big,", "SO BIG!", .7, .2, .9, "sun")]),
    S("snowhill", (980, 600, 1700), "Tumble lies down on his tummy, and slides. Whee! Milo zooms down beside him.", beat="goal", tag="Tumble slides, Milo zooms beside",
      actors=[("poppy", "bear", 440, A.TOP_Y, .5), SL("tumble", "tumble_slide", 820, .45), ("milo", "milo", 1100, 370, .55, False, True)],
      props=[SPRAY("sp", 1240, 860)],
      fx=[SLIDE("w:slides.", "tumble", 820, 1520, 3.0), ("fly", "w:Milo", "milo", 1560, 640, 2.0), ("show", "w:beside", "sp"), ("face", "w:Whee!", "tumble", "happy")],
      words=[("w:Whee!", "WHEE!", .7, .2, 1.0, "sun")]),
    S("hilltop", C("hilltop", "poppy", "all", 1100, 60, -40), "Poppy watches from the top. She wants to slide too. But she feels shy.", beat="obstacle1", tag="Poppy watches, shy",
      hide=["tumble", "milo"], fx=[("lookat", 0.02, "poppy", 14), ("face", "w:wants", "poppy", "happy"), ("face", "w:shy.", "poppy", "sad"), ("lookat", "w:shy.", "poppy", 8)],
      words=[("w:shy.", "SHY", .66, .2, .9, "pill")]),
    # ------------------------------------------------------------ OBSTACLE 1: sitting at the edge, the hill looks so long
    S("hilltop", C("hilltop", "poppy", "head", 800, -60, 40), "Maybe I can sit down first, right here at the top.", who="poppy", beat="obstacle1", tag="Poppy: sit down first",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "happy"), ("lookat", "w:sit", "poppy", 10), ("lookat", "w:top.", "poppy", 0)], words=[("w:sit", "SIT DOWN", .84, .3, .7, "sun")]),
    S("hilltop", (1100, 620, 1500), "Poppy sits at the edge, and looks down. The hill looks so long! She stops.", beat="obstacle1", tag="at the edge: so long",
      actors=[("poppy", "bear_belly", 1000, 880, .62)], hide=["tumble", "milo"],
      fx=[("to", 0.2, "#{p}poppy_w", {"x": "+=120", "duration": 1.4, "ease": "sine.inOut"}, "Poppy creeps to the edge"), ("lookat", "w:down.", "poppy", 18),
          ("face", "w:long!", "poppy", "wow"), ("to", "w:stops.", "#{p}poppy_w", {"x": "-=80", "duration": .8, "ease": "sine.out"}, "Poppy scoots back")],
      words=[("w:long!", "SO LONG!", .56, .12, .9, "sun")]),
    S("hilltop", MCL("hilltop", 0, -60, 760), "Is the big hill long, or short?", q=True, beat="obstacle1", tag="question: long or short", pause=3.2, hide=["tumble", "poppy"],
      fx=[("signs", "w:long,", ["LONG", "SHORT"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 2: holding Milo's wing (Milo is too little)
    S("snowbottom", C("snowbottom", "tumble", "head", 900, -20, 40), "Come on down, Poppy! It is so much fun!", who="tumble", beat="obstacle2", tag="Tumble calls from the bottom",
      hide=["poppy", "milo"], fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:Come", "tumble", -100, .4), ("trunk", "w:fun!", "tumble", -40, .4)],
      words=[("w:fun!", "SO MUCH FUN!", .64, .14, .7, "pill")]),
    S("hilltop", C("hilltop", "milo", "body", 820, 0, -20), "I know! Hold my wing, Poppy. We can go down together!", beat="obstacle2", tag="Milo: hold my wing",
      hide=["tumble", "poppy"], fx=[("face", 0.02, "milo", "happy"), ("hop", "w:know!", "milo"), ("hop", "w:together!", "milo")], words=[("w:wing,", "HOLD MY WING", .66, .2, .7, "sun")]),
    S("hilltop", (1000, 560, 1500), "Poppy holds Milo's wing. But Milo is little, and Poppy is big! Milo flutters up into the sky!", beat="obstacle2", tag="Milo flutters up",
      actors=[("poppy", "bear", 860, 880, .62), ("milo", "milo", 1190, 640, .6, False, True)],
      fx=[("nod", "w:holds", "poppy"), ("fly", "w:flutters", "milo", 1260, 330, 2.0), ("lookat", "w:up", "poppy", -14), ("face", "w:sky!", "poppy", "happy")],
      words=[("w:little,", "LITTLE", .78, .55, .7, "pill"), ("w:big!", "BIG", .42, .42, .8, "pill"), ("w:up", "UP!", .5, .1, .9, "sun")]),
    S("hilltop", C("hilltop", "poppy", "head", 820, -40, 40), "Oh, Milo! You are too little to hold me. Hee hee!", who="poppy", beat="obstacle2", tag="Poppy giggles: too little",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "happy"), ("lookat", 0.02, "poppy", -16), ("nod", "w:Hee", "poppy")], words=[("w:little", "TOO LITTLE!", .8, .12, .8, "sun")]),
    S("hilltop", (1020, 600, 1400), "Who is bigger? Poppy, or Milo?", q=True, beat="obstacle2", tag="question: Poppy or Milo", pause=3.2,
      actors=[("poppy", "bear", 860, 880, .62), ("milo", "milo", 1240, 640, .6, False, True)], cam2=(1020, 640, 1280),
      fx=[("nod", "w:Poppy,", "poppy"), ("signs", "w:Poppy,", ["POPPY", "MILO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 3: Tumble zooms so fast, Poppy likes slow
    S("snowhill", (1060, 600, 1700), "Tumble climbs up and slides again. Whoosh! He goes so fast!", beat="obstacle3", tag="Tumble zooms again",
      actors=[("poppy", "bear", 440, A.TOP_Y, .5), SL("tumble", "tumble_slide", 820, .45)], hide=["milo"], props=[SPRAY("sp", 1400, 900)],
      fx=[SLIDE("w:Whoosh!", "tumble", 820, 1560, 1.6, "power1.in"), ("show", "w:fast!", "sp"), ("lookat", "w:Whoosh!", "poppy", 12)],
      words=[("w:Whoosh!", "WHOOSH!", .7, .2, .95, "sun")]),
    S("hilltop", C("hilltop", "poppy", "head", 820, -40, 40), "That is too fast for me. I like slow.", who="poppy", beat="obstacle3", tag="Poppy: I like slow",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "wow"), ("nod", "w:slow.", "poppy"), ("face", "w:slow.", "poppy", "happy")], words=[("w:slow.", "I LIKE SLOW", .78, .12, .8, "pill")]),
    S("hilltop", C("hilltop", "poppy", "all", 1000, 60, -40), "Does Poppy like fast, or slow?", q=True, beat="obstacle3", tag="question: fast or slow", pause=3.2,
      hide=["tumble", "milo"], cam2=C("hilltop", "poppy", "all", 940, 60, -60), fx=[("signs", "w:fast,", ["FAST", "SLOW"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ LOW MOMENT: maybe sliding is not for me (gentle: nobody cries)
    S("hilltop", (900, 620, 1600), "Poppy sits down in the snow, and looks at her paws. She feels a little sad.", beat="low", tag="Poppy sits, a little sad",
      actors=[("poppy", "bear_belly", 820, 880, .62)], hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "sad"), ("lookat", "w:paws.", "poppy", 16)],
      words=[("w:sad.", "A LITTLE SAD", .6, .16, .8, "pill")]),
    S("hilltop", C("hilltop", "poppy", "head", 760, -40, 60, stage=[("poppy", "bear_belly", 820, 880, .62)]), "Maybe sliding is not for me.", who="poppy", beat="low", tag="Poppy: not for me",
      actors=[("poppy", "bear_belly", 820, 880, .62)], fx=[("face", 0.02, "poppy", "sad"), ("lookat", "w:not", "poppy", 12)]),
    S("hilltop", (900, 600, 1700), "Milo flies up, and Tumble walks up too. It's okay, Poppy. We will stay right here with you.", beat="low", tag="friends come and stay",
      actors=[("tumble", "tumble", 230, 880, .55), ("poppy", "bear_belly", 820, 880, .62), ("milo", "milo", 1500, 400, .6, False, True)],
      fx=[("fly", "w:Milo", "milo", 1160, 640, 1.4), ("walk", "w:Tumble", "tumble", 80, 1.4), ("face", "w:okay,", "poppy", "happy"), ("trunk", "w:stay", "tumble", -40, .4)],
      words=[("w:stay", "RIGHT HERE", .5, .14, .8, "sun")]),
    S("hilltop", C("hilltop", "milo", "body", 760, 0, -40, stage=[("milo", "milo", 1160, 640, .6, False, True)]), "Can good friends help Poppy feel better? Yes, or no?", q=True, beat="low",
      tag="question: friends help yes or no", pause=3.2, actors=[("milo", "milo", 1160, 640, .6, False, True)], fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: Poppy finds the way herself (her grippy paws, walk down, slide from the middle)
    S("hilltop", C("hilltop", "poppy", "all", 900, 40, -20, stage=[("poppy", "bear_belly", 820, 880, .62)]), "Wait! Look at my paws. Tiny bumps, and soft fur. They hold on to the snow!", who="poppy", beat="solution",
      tag="Poppy looks at her paws", actors=[("poppy", "bear_belly", 820, 880, .62)], fx=[("face", 0.02, "poppy", "wow"), ("lookat", "w:paws.", "poppy", 18), ("lookat", "w:hold", "poppy", 0), ("face", "w:hold", "poppy", "happy")],
      words=[("w:bumps,", "TINY BUMPS", .56, .1, .8, "sun")]),
    S("paper_blue", (960, 560, 1500), "Polar bears have tiny bumps on the pads of their paws. The bumps help them grip the snow. And fur on their paws keeps them warm.", beat="fact",
      tag="fact: tiny bumps grip, fur keeps warm", actors=[("poppy", "bear_belly", 560, 900, .66)], props=[prop("pp", A.paw_pad, 1260, 500, .9), prop("rg", A9.ring, 1260, 500, 2.0, True)],
      fx=[("to", "w:bumps", "#{p}pp-bumps", {"scale": 1.06, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 3}, "the bumps pulse"),
          ("show", "w:grip", "rg"), ("to", "w:fur", "#{p}pp_w", {"scale": 1.05, "duration": .3, "yoyo": True, "repeat": 1}, ""), ("hide", "w:fur", "rg")],
      words=[("w:bumps", "TINY BUMPS", .78, .14, .7, "sun"), ("w:grip", "GRIP!", .46, .2, .8, "pill"), ("w:warm.", "WARM FUR", .25, .4, .7, "sun")]),
    S("hilltop", C("hilltop", "tumble", "head", 860, 40, 40), "What helps a polar bear grip the snow? Tiny bumps, or wheels?", q=True, who="milo", beat="solution", tag="question: bumps or wheels", pause=3.2,
      hide=["poppy", "milo"], fx=[("face", 0.02, "tumble", "happy"), ("signs", "w:Tiny", ["TINY BUMPS", "WHEELS"], 0, "wait:1.8")]),
    S("hilltop", (1000, 600, 1400), "Can you walk slow and steady, like Poppy? Step, step, step!", q=True, beat="solution", tag="copy me: slow and steady", pause=3.0,
      actors=[("poppy", "bear", 760, 880, .62), ("milo", "milo", 1240, 640, .6, False, True)], cam2=(1000, 640, 1300),
      fx=[("walk", "w:walk", "poppy", 160, 4.0), ("hop", "w:Step,", "milo")], words=[("w:slow", "SLOW AND STEADY", .5, .14, .7, "sun")]),
    S("hilltop", C("hilltop", "poppy", "head", 860, -40, 40), "I know! I can walk down a little bit first, slow and steady. Then I can slide from the middle, where the hill is small!", who="poppy",
      beat="solution", tag="Poppy: I know!", hide=["tumble", "milo"],
      fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:know!", "poppy"), ("lookat", "w:walk", "poppy", 12), ("lookat", "w:slide", "poppy", 0), ("nod", "w:small!", "poppy")],
      words=[("w:know!", "I KNOW!", .8, .1, .8, "sun"), ("w:middle,", "THE MIDDLE", .8, .22, .7, "pill")]),
    S("snowhill", (900, 560, 1500), "Poppy walks down the hill, step by step, on her grippy paws. Slow and steady!", beat="solution", tag="Poppy walks down slowly",
      actors=[("poppy", "bear", 440, A.TOP_Y, .5), ("milo", "milo", 800, 400, .55, False, True)],
      fx=[("walk", 0.3, "poppy", 520, 5.4), ("to", 0.3 + 5.4 * (A.X0 - 440) / 520, "#{p}poppy_w", {"y": "+=%d" % (HY(960) - A.TOP_Y), "duration": 5.4 * (960 - A.X0) / 520, "ease": "none"}, "she walks down the slope"),
          ("fly", 1.0, "milo", 1340, 440, 4.0)],
      words=[("w:step", "STEP BY STEP", .5, .12, .8, "sun")]),
    S("hillmid", WIDE, "Here, in the middle, the hill is small. Tumble and Milo come too.", trans="iris", beat="solution", tag="the little ledge in the middle", cam2=(980, 560, 1820),
      actors=[("tumble", "tumble", 190, 920, .55), ("poppy", "bear", 800, 920, .6), ("milo", "milo", 420, 360, .6, False, True)],
      fx=[("nod", "w:small.", "poppy"), ("walk", "w:Tumble", "tumble", 110, 1.4), ("fly", "w:Milo", "milo", 1180, 640, 1.6)], words=[("w:small.", "SMALL HILL", .7, .2, .85, "sun")]),
    S("hillmid", C("hillmid", "tumble", "head", 860, 40, 40), "We can slide beside you, nice and slow!", who="tumble", beat="solution", tag="Tumble: beside you, slow",
      hide=["poppy", "milo"], fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:beside", "tumble", -40, .4), ("trunk", "w:slow!", "tumble", -90, .4)],
      words=[("w:slow!", "NICE AND SLOW", .62, .09, .7, "pill")]),
    S("hillmid", (800, 560, 1600), "Ready? Count with me! One, two, three!", q=True, beat="solution", tag="count to three", pause=1.0,
      actors=[("tumble", "tumble", 300, 920, .55), ("poppy", "bear_belly", 820, 920, .6), ("milo", "milo", 1180, 640, .6, False, True)],
      fx=[("face", 0.02, "poppy", "happy"), ("count", "w:One,", 3, CNT3, {"x": 820, "y": 380}), ("hop", "w:three!", "milo")]),
    S("snowhill", (1100, 640, 1500), "Poppy slides on her tummy, slow and gentle. Whee! Her friends slide right beside her.", beat="solution", tag="Poppy slides from the middle",
      actors=[SL("tumble", "tumble_slide", 680, .4), SL("poppy", "bear_slide", 1100, .5), ("milo", "milo", 1250, 400, .5, False, True)], props=[SPRAY("sp", 1560, 900, .5)],
      fx=[SLIDE(0.3, "poppy", 1100, 1520, 4.6), SLIDE(0.3, "tumble", 680, 1100, 4.6), ("fly", 0.3, "milo", 1640, 600, 4.6), ("face", "w:Whee!", "poppy", "happy"), ("show", "w:beside", "sp")],
      words=[("w:Whee!", "WHEE!", .5, .16, 1.0, "sun")]),
    S("snowbottom", C("snowbottom", "poppy", "all", 1000, -40, -40), "I did it! I slid down the hill!", who="poppy", beat="solution", tag="Poppy: I did it!",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "happy"), ("hop", "w:did", "poppy"), ("hop", "w:hill!", "poppy")], words=[("w:did", "I DID IT!", .72, .16, .9, "sun")]),
    S("snowbottom", C("snowbottom", "tumble", "head", 900, -20, 40), "Hooray, Poppy! You slid all the way down!", who="tumble", beat="solution", tag="Tumble: hooray, Poppy",
      hide=["poppy", "milo"], fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:Hooray,", "tumble", -100, .4), ("trunk", "w:down!", "tumble", -40, .4)],
      words=[("w:way", "ALL THE WAY!", .64, .14, .75, "sun")]),
    S("snowbottom", (1300, 600, 1500), "Where did Poppy slide from? The middle, or the very top?", q=True, beat="solution", tag="question: middle or top", pause=3.2, cam2=(1320, 620, 1400),
      hide=["milo"], fx=[("trunk", "w:middle,", "tumble", -60, .4), ("signs", "w:middle,", ["THE MIDDLE", "THE TOP"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ the song moment: Poppy SAYS the rhyme, then the tune on instruments
    S("snowbottom", (1280, 620, 1500), "Wide paws, hold on tight. Down we slide, snowy white!", who="poppy", beat="solution", tag="the paws rhyme",
      fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:Wide", "poppy"), ("trunk", "w:Down", "tumble", -90, .4), ("nod", "w:white!", "poppy")],
      words=[("w:Wide", "WIDE PAWS", .6, .1, .62, "sun"), ("w:Down", "DOWN WE SLIDE", .6, .2, .62, "pill")]),
    S("snowbottom", (1240, 600, 1600), who="", sing=SING_PAWS, beat="song", tag="song: wide paws", cam2=(1260, 620, 1500), props=FLAKES(((900, 300), (1300, 260), (1560, 360))),
      fx=[("hop", TB(0), "poppy"), ("trunk", TB(2), "tumble", -100, .4), ("hop", TB(4), "milo"), ("hop", TB(8), "poppy"), ("trunk", TB(10), "tumble", -40, .4), ("hop", TB(12), "milo"),
          ("to", TB(0), "#{p}f0_w,#{p}f1_w,#{p}f2_w", {"y": "+=120", "rotation": 60, "duration": 6, "ease": "none"}, "snowflakes drift down"),
          ("word", TB(0), "WIDE PAWS", {"x": 1240, "y": 330, "size": 80, "cls": "sun", "hold": 4.4})],
      words=[(TB(8), "SNOWY WHITE", .5, .2, .7, "pill")]),
    S("snowbottom", C("snowbottom", "poppy", "head", 820, -40, 40), "Can we go again? From the very top this time!", who="poppy", beat="solution", tag="Poppy: again, from the top",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "happy"), ("lookat", "w:top", "poppy", -16), ("hop", "w:time!", "poppy")], words=[("w:again?", "AGAIN!", .72, .14, .9, "sun")]),
    # ------------------------------------------------------------ WARM ENDING: the very top, evening, thank-yous, next time
    S("snowhill", WIDE, "So Poppy walks up on her grippy paws, and slides from the very top!", beat="ending", tag="Poppy slides from the top", cam2=(980, 560, 1820),
      actors=[SL("poppy", "bear_slide", 640, .5), ("tumble", "tumble", 1700, 935, .5, True), ("milo", "milo", 1500, 520, .55, False, True)], props=[SPRAY("sp", 1500, 880, .5)],
      fx=[SLIDE("w:slides", "poppy", 640, 1500, 3.4), ("show", "w:very", "sp"), ("trunk", "w:top!", "tumble", -100, .4), ("hop", "w:top!", "milo")],
      words=[("w:very", "THE VERY TOP!", .5, .14, .8, "sun")]),
    S("snowbottom", (1060, 620, 1600), "Tumble slides down after her. Whoosh! And everybody laughs in the soft, white snow.", beat="ending", tag="everybody laughs in the snow",
      actors=[("tumble", "tumble", 520, 935, .55), ("poppy", "bear_belly", 1300, 935, .6, True), ("milo", "milo", 1150, 600, .62, False, True)], props=[SPRAY("sp", 960, 900, .7)],
      fx=[("walk", 0.2, "tumble", 180, 1.4), ("show", "w:Whoosh!", "sp"), ("face", "w:laughs", "poppy", "happy"), ("hop", "w:laughs", "milo"), ("hop", "w:snow.", "tumble")],
      words=[("w:Whoosh!", "WHOOSH!", .6, .12, .9, "sun")]),
    S("arctic_eve", WIDE, "The sun is low, and the sky is pink. What a happy snowy day!", trans="iris", beat="ending", tag="evening on the ice", cam2=(980, 560, 1820),
      fx=[("hop", "w:happy", "poppy"), ("trunk", "w:happy", "tumble", -90, .4), ("hop", "w:day!", "milo")], words=[("w:happy", "HAPPY DAY!", .5, .14, .9, "sun")]),
    S("arctic_eve", C("arctic_eve", "poppy", "head", 820, -60, 40), "Thank you, friends! You waited for me, and slid right beside me.", who="poppy", beat="ending", tag="Poppy: thank you",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:friends!", "poppy"), ("nod", "w:beside", "poppy")], words=[("w:Thank", "THANK YOU!", .72, .14, .85, "sun")]),
    S("arctic_eve", C("arctic_eve", "tumble", "head", 860, 40, 40), "And you found your very own way down, Poppy!", who="tumble", beat="ending", tag="Tumble: your own way",
      hide=["poppy", "milo"], fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:found", "tumble", -90, .5)], words=[("w:own", "YOUR OWN WAY", .62, .1, .7, "pill")]),
    S("arctic_eve", (960, 600, 1800), "When something feels big, you can try it a little bit at a time. And good friends wait for you.", beat="ending", tag="the lesson", cam2=(1000, 600, 1700),
      fx=[("hop", "w:big,", "milo"), ("nod", "w:little", "poppy"), ("trunk", "w:friends", "tumble", -80, .4), ("hop", "w:you.", "poppy")],
      words=[("w:little", "A LITTLE BIT AT A TIME", .6, .1, .55, "sun")]),
    S("arctic_eve", C("arctic_eve", "milo", "body", 900, 40, 0), "Do you remember? What do the tiny bumps on a polar bear's paws do? Grip the snow, or make music?", q=True, beat="ending",
      tag="question: grip or music", pause=3.2, hide=["tumble", "poppy"], cam2=C("arctic_eve", "milo", "body", 830, 40, -60),
      fx=[("hop", "w:remember?", "milo"), ("signs", "w:Grip", ["GRIP THE SNOW", "MAKE MUSIC"], 0, "wait:1.8")]),
    S("arctic_eve", C("arctic_eve", "poppy", "all", 1000, 60, -40), "And what do big, wide paws do on the snow? Spread out the weight, or tickle?", q=True, beat="ending", tag="question: spread or tickle", pause=3.2,
      hide=["tumble", "milo"], cam2=C("arctic_eve", "poppy", "all", 940, 60, -60), fx=[("nod", "w:paws", "poppy"), ("signs", "w:Spread", ["SPREAD THE WEIGHT", "TICKLE"], 0, "wait:1.8")]),
    S("arctic_eve", (960, 540, 1920), "Wide paws, hold on tight. Down we slide, snowy white!", beat="ending", tag="the closing rhyme", cam2=(980, 560, 1880),
      fx=[("hop", "w:Wide", "milo"), ("nod", "w:tight.", "poppy"), ("trunk", "w:Down", "tumble", -80, .4), ("hop", "w:white!", "poppy")],
      words=[("w:Wide", "WIDE PAWS", .7, .14, .65, "sun")]),
    S("arctic_eve", WIDE, who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(980, 560, 1880),
      fx=[("hop", 1.0, "poppy"), ("trunk", 2.0, "tumble", -90, .4), ("hop", 2.2, "milo")], words=[(TB(3), "HOORAY!", .7, .16, 1.0, "sun")]),
    S("arctic_eve", C("arctic_eve", "milo", "body", 900, 0, 0), "Next time: Too Cold for Milo! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure", hide=["tumble", "poppy"],
      fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .8, .2, .66, "sun"), ("w:See", "SEE YOU SOON!", .8, .33, .56, "pill")]),
    *intro_shots(),      # and again as the last shots: the video ends on the logo with the whole cast
]

# thumbnail (thumb.py): the promise of the first shot: Poppy sliding down the big snowy hill, friends cheering below; 1 word, none of the title's words, no watermark
THUMBS = {
    "za_ep10": {"place": "snowhill", "cam": (1080, 640, 1300),
                "actors": [("bear_slide", 1000, HY(1000), .78, False, ''), ("tumble", 1620, 935, .5, True, ''), ("milo", 1450, 560, .55, False, '')],
                "props": [(A.spray, 760, HY(760) - 20, .8)],
                "words": [("WHEE!", 760, 260, 190, "sun", -6)]},
}
