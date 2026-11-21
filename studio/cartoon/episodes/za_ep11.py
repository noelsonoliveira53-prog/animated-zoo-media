"""za_ep11 - Milo's Zoo Adventures: "How Can Milo Get Warm in the Snow?" (theme title "Too Cold for Milo!"; cartoon adventure, the 3D music-and-sync
process: "beat"). Arctic week, adventure 2.
Milo visits Poppy the polar bear cub in the snowy Arctic and cannot stop shivering. Poppy wants to play in the snow; Milo wants to get warm first.
A leaf blanket from home is too thin (the wind blows through it), hopping warms him only until he is too tired, and the sun is too low and pale
(a cloud floats over it). Low moment: "maybe the Arctic is too cold for a little bird like me" (a little sad, never crying; Poppy sits beside him).
Poppy shows how SHE stays warm (two layers of fur, a thick layer of fat) and Milo finds the answer for a bird himself: a cozy nest out of the wind,
right next to his fluffy friend. They build a snow nest together, Milo snuggles in, Poppy curls up beside it. The rhyme is said, the tune is played
on instruments, they play in the snow, and the day ends with the two of them in the nest under a pink sky. Nobody is hurt, lost, crying or trapped;
nobody is in danger: being chilly is a small, funny problem that friends solve.

FACTS, read at the source on Nov 21 2026, about 9:00 AM ET (each page fetched by the session's page reader, which quoted these sentences verbatim):
 [PBI] Polar Bears International, "Adaptation", polarbearsinternational.org/polar-bears/adaptation
   "In addition to 2 layers of fur, a thick layer of fat helps keep the bears warm."   "Polar bears have 2 layers of fur that prevent almost all heat loss."
   "In the water, polar bears rely more on their fat than their fur to keep out the cold; wet fur is a poor insulator."
 [PBS] PBS Nature, "Bears of the Last Frontier: Polar Bear Fact Sheet", pbs.org/wnet/nature/bears-of-the-last-frontier-polar-bear-fact-sheet/7053
   "It's composed of two layers."   "The layer closer to the body, the undercoat, consists of thick, plush hair that retains heat."
   "The outer layer provides extra insulation and repels cold water and ice."   "...below the skin is a thick, 4-inch layer of blubber."
   "This blubber layer is particularly beneficial while polar bears swim, keeping them warm in the cold water"
 [WWF] World Wildlife Fund, "Why do polar bears have white fur? And 10 other polar bear facts", worldwildlife.org
   "They have a thick layer of body fat, which keeps them warm while swimming," "and a double-layered coat that insulates them from the cold Arctic air."
 Said as animal facts in the film (two fact boards, questions, recap): polar bears have two layers of fur, a soft thick layer close to the skin and
 long hairs on top [PBS, PBI, WWF]; under the skin a thick layer of fat keeps them warm, even when they swim in cold water [PBI, PBS, WWF].
 Not animal facts, said as what happens in THIS story: Milo being chilly, the leaf, the hopping, the low sun, the snow nest, the rhyme and the tune.
 Nothing is said about how birds keep warm (no page about birds was read today).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep07 as A7
import art_za_ep10 as A10
import art_za_ep11 as A
import kit
from kit import Kit, S, prop
from intro import INTRO_STAGES, intro_shots      # the main intro, right after the hook and as the last shots (owner, Nov 20 4:50 PM)

EP = {"id": "za_ep11", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "poppy": {"voice": "af_jessica", "speed": .88, "pitch": 4, "formant": 1.2, "gain": .9}},
      "title": "How Can Milo Get Warm in the Snow?", "thumb_text": "BRRR!",
      "series": "Milo's Zoo Adventures",
      "description": ("How can Milo get warm in the snow? Milo the bluebird visits Poppy the polar bear cub in the snowy Arctic, and he cannot stop shivering. "
                      "A leaf blanket, a hopping game and the low sun do not help for long, until Milo and Poppy find a cozy idea together. "
                      "A gentle Arctic adventure for ages 2-6 about friends helping each other, with questions to answer, a count-along and a snowy tune.\n"
                      "Kids see how polar bears have two layers of fur, a soft thick layer close to the skin and long hairs on top, "
                      "and how a thick layer of fat under the skin keeps them warm, even when they swim in cold water.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nPolar Bears International (polar bear adaptations); PBS Nature (polar bear fact sheet); World Wildlife Fund (polar bear facts)."),
      "tags": ["polar bear for kids", "polar bear cub", "how do polar bears stay warm", "arctic animals for kids", "snow day", "cold weather for kids", "bluebird",
               "animal stories for kids", "friendship story for kids", "kids adventure cartoon", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "arctic": [("milo", "milo", 720, 905, .62), ("poppy", "bear", 1200, 900, .6, True)],
    "arctic_low": [("poppy", "bear", 330, 900, .6), ("milo", "milo", 860, 905, .6)],
    "snowbottom": [("milo", "milo", 1150, 940, .6), ("poppy", "bear", 1620, 935, .6, True)],
    "hillmid": [("poppy", "bear", 260, 920, .6), ("milo", "milo", 780, 920, .62)],
    "hilltop": [("milo", "milo", 920, 885, .62), ("poppy", "bear", 300, 880, .6)],
    "arctic_eve": [("milo", "milo", 820, 905, .6), ("poppy", "bear_belly", 1260, 900, .6, True)],
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
MCL = lambda place, dx=0, dy=-70, w=820, stage=None: C(place, "milo", "body", w, dx, dy, stage=stage)     # Milo close: low in the frame, under the signs
PCL = lambda place, w=820, dx=-60, dy=40, stage=None: C(place, "poppy", "head", w, dx, dy, stage=stage)  # Poppy close

SHAKE = lambda at, who="milo", n=13: ("to", at, "#{p}%s_w" % who, {"x": "+=7", "duration": .06, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, who + " shivers")
SHIV = lambda name, place, s=.6, stage=None: prop(name, A.shiver, *P(place, "milo", "body", stage=stage), s, True)
SHIVF = lambda at, name: ("to", at, "#{p}%s-l,#{p}%s-r" % (name, name), {"opacity": .25, "duration": .12, "yoyo": True, "repeat": 9}, "the shiver lines flicker")
NEST = lambda name, x, y, s=.8, hidden=False: prop(name, A.snow_nest, x, y, s, hidden)
FLAKES = lambda xs: [prop("f%d" % k, A10.snowflake, x, y, .5) for k, (x, y) in enumerate(xs)]

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. The rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_NEST = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "G4:1 E4:1 C5:2 D5:1 B4:1 G4:1", "rest": 1},      # fluffy fur and a cozy nest (C bar, G bar)
                                 {"text": "~ ~ ~ ~ ~ ~", "notes": "C5:1 A4:1 F4:2 G4:1 E4:1 C5:1", "rest": 1}])     # warm with friends, that's the best (F bar, C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "D5:1 B4:1 G4:1 B4:1 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune
CNT3 = 0.52                                      # seconds from "One" to "three", read from the timing file

NX, NY = 1150, 978                               # the snow nest at the bottom of the hill (front of the ring, in front of Milo's feet)
EX, EY = 820, 944                                # the snow nest on the evening shore

SHOTS = [
    # ------------------------------------------------------------ HOOK: Milo shivering beside a cozy Poppy (first 5 seconds)
    S("arctic", (960, 640, 1500), "How can Milo get warm in the snow? He is so cold, he cannot stop shivering!", beat="hook", tag="hook: Milo shivers, Poppy cozy",
      cam2=(900, 660, 1400), props=[SHIV("sh", "arctic"), prop("br", A.breath, 790, 700, .9, True)],
      fx=[("face", 0.02, "milo", "wow"), ("show", 0.1, "sh"), SHAKE(0.3), SHIVF(0.3, "sh"), ("face", 0.02, "poppy", "happy"), ("show", "w:cold,", "br"),
          SHAKE("w:shivering!"), ("nod", "w:snow?", "poppy")],
      words=[(0.4, "BRRR!", .5, .14, 1.0, "sun")]),
    *intro_shots(),      # the main intro, right after the hook
    # ------------------------------------------------------------ GOAL: visiting Poppy, getting warm to play
    S("arctic", WIDE, "Hello, I'm Milo! I came to visit my friend Poppy the polar bear cub, in the snowy Arctic.", trans="iris", beat="goal", tag="arctic wide: Milo and Poppy",
      cam2=(980, 580, 1780), fx=[("hop", "w:Hello,", "milo"), ("nod", "w:Poppy", "poppy"), ("lookat", "w:Arctic.", "poppy", -6)],
      words=[("w:Poppy", "POPPY", .66, .3, .7, "pill"), ("w:Arctic.", "THE ARCTIC", .5, .14, .7, "sun")]),
    S("arctic", PCL("arctic"), "Hi, Milo! Welcome to the Arctic! Do you want to play in the snow with me?", who="poppy", beat="goal", tag="Poppy: play in the snow",
      hide=["milo"], fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:Hi,", "poppy"), ("lookat", "w:play", "poppy", -6), ("nod", "w:snow", "poppy")],
      words=[("w:play", "LET'S PLAY!", .62, .12, .8, "sun")]),
    S("arctic", MCL("arctic", 0, -70, 780), "Yes, please! But I am so cold. My little scarf is too tiny!", beat="goal", tag="Milo: so cold, tiny scarf",
      hide=["poppy"], props=[SHIV("sh", "arctic")], fx=[("hop", "w:Yes,", "milo"), ("face", "w:cold.", "milo", "wow"), ("show", "w:cold.", "sh"), SHAKE("w:cold."), SHIVF("w:cold.", "sh")],
      words=[("w:tiny!", "TOO TINY!", .5, .12, .85, "pill")]),
    S("arctic", (960, 620, 1500), "Who is cold? Milo, or Poppy?", q=True, beat="goal", tag="question: who is cold", pause=3.2, cam2=(960, 640, 1400),
      props=[SHIV("sh", "arctic")], fx=[("show", 0.1, "sh"), SHAKE(0.2), ("signs", "w:Milo,", ["MILO", "POPPY"], 0, "wait:1.8")]),
    S("arctic", PCL("arctic", 860), "I am not cold at all! I feel cozy and warm.", who="poppy", beat="goal", tag="Poppy: cozy and warm",
      hide=["milo"], fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:cold", "poppy"), ("hop", "w:cozy", "poppy")], words=[("w:cozy", "COZY!", .6, .12, .9, "sun")]),
    S("arctic", MCL("arctic", 0, -60, 800), "I want to get warm, so I can play in the snow with Poppy!", beat="goal", tag="Milo: I want to get warm",
      hide=["poppy"], fx=[("face", 0.02, "milo", "happy"), ("hop", "w:warm,", "milo"), ("hop", "w:Poppy!", "milo")], words=[("w:warm,", "GET WARM", .5, .12, .85, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: a leaf blanket from home, too thin
    S("snowbottom", (1300, 700, 1400), "Milo has a big leaf from home. He wraps it around him, like a blanket.", beat="obstacle1", tag="the leaf blanket",
      cam2=(1280, 720, 1260), props=[prop("lf", A.leaf_wrap, *P("snowbottom", "milo", "feet"), .6, True)],
      fx=[("face", 0.02, "milo", "happy"), ("show", "w:leaf", "lf"), ("hop", "w:wraps", "milo"), ("nod", "w:blanket.", "poppy")],
      words=[("w:blanket.", "LEAF BLANKET", .62, .14, .75, "sun")]),
    S("snowbottom", (1200, 740, 1300), "But the leaf is too thin! The cold wind blows right through it.", beat="obstacle1", tag="leaf too thin, wind",
      hide=["poppy"], props=[prop("lf", A.leaf_wrap, *P("snowbottom", "milo", "feet"), .6), prop("wl", A7.wind_lines, 1100, 905, .5, True),
                             SHIV("sh", "snowbottom")],
      fx=[("to", "w:thin!", "#{p}lf-tip", {"rotation": -12, "svgOrigin": "140 -70", "duration": .12, "yoyo": True, "repeat": 15}, "the leaf flaps in the wind"),
          ("show", "w:wind", "wl"), ("to", "w:wind", "#{p}wl_w", {"x": "+=140", "duration": 2.0, "ease": "none"}, "the wind blows across"),
          ("face", "w:thin!", "milo", "wow"), ("show", "w:through", "sh"), SHAKE("w:through"), SHIVF("w:through", "sh")],
      words=[("w:thin!", "TOO THIN!", .56, .12, .9, "pill")]),
    S("snowbottom", C("snowbottom", "poppy", "head", 820, -60, 40), "That leaf is so thin, Milo. I can almost see you through it! Hee hee!", who="poppy", beat="obstacle1",
      tag="Poppy giggles: so thin", hide=["milo"], fx=[("face", 0.02, "poppy", "happy"), ("lookat", 0.02, "poppy", 6), ("nod", "w:see", "poppy"), ("nod", "w:Hee", "poppy")],
      words=[("w:see", "SEE-THROUGH!", .4, .12, .75, "sun")]),
    S("snowbottom", MCL("snowbottom", 0, -60, 800), "Is a thin leaf a warm blanket? Yes, or no?", q=True, beat="obstacle1", tag="question: leaf warm yes or no", pause=3.2, hide=["poppy"],
      props=[prop("lf", A.leaf_wrap, *P("snowbottom", "milo", "feet"), .6)], cam2=MCL("snowbottom", 0, -70, 740),
      fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 2: hopping to warm up, too tiring
    S("hillmid", MCL("hillmid", 0, -70, 820), "I know! I can hop to warm up. Can you hop with me? One hop, two hops, three hops!", q=True, beat="obstacle2", tag="copy me: hop with Milo",
      pause=3.0, hide=["poppy"], cam2=MCL("hillmid", 0, -80, 760),
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:One", "milo"), ("hop", "w:two", "milo"), ("hop", "w:three", "milo"), ("hop", "w:hops!", "milo")],
      words=[("w:hop:1", "HOP!", .5, .12, .9, "sun")]),
    S("hillmid", WIDE, "Milo hops and hops, all over the snow. Then he stops. He is so tired! He needs a rest.", trans="iris", beat="obstacle2", tag="Milo hops, then tired",
      cam2=(940, 580, 1760),
      fx=[("hop", "w:hops", "milo"), ("to", "w:hops", "#{p}milo_w", {"x": "+=220", "duration": 1.6, "ease": "sine.inOut"}, "Milo hops across"),
          ("hop", "w:all", "milo"), ("hop", "w:over", "milo"), ("lookat", "w:hops", "poppy", 6), ("face", "w:tired!", "milo", "sleepy"), ("face", "w:tired!", "poppy", "wow")],
      words=[("w:tired!", "SO TIRED!", .62, .14, .9, "pill")]),
    S("hillmid", (980, 640, 1300), "Can Milo hop all day long? Yes, or no?", q=True, beat="obstacle2", tag="question: hop all day yes or no", pause=3.2, cam2=(1000, 660, 1220), hide=["poppy"],
      actors=[("poppy", "bear", 260, 920, .6), ("milo", "milo", 1000, 920, .62)], props=[SHIV("sh", "hillmid", stage=[("milo", "milo", 1000, 920, .62)])],
      fx=[("face", 0.02, "milo", "sleepy"), ("show", "w:day", "sh"), SHAKE("w:day"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 3: the sun is too low
    S("arctic_low", WIDE, "Maybe the sunshine can warm me up! Milo flies to a sunny spot on the ice.", trans="iris", beat="obstacle3", tag="Milo flies to the sun",
      cam2=(1000, 600, 1780), fx=[("face", 0.02, "milo", "happy"), ("fly", "w:flies", "milo", 1150, 905, 2.2), ("lookat", "w:flies", "poppy", -6)],
      words=[("w:sunshine", "SUNSHINE?", .5, .14, .85, "sun")]),
    S("arctic_low", (1340, 640, 1240), "But the sun sits very low in the sky. It looks pale, not hot. Then a cloud floats right in front of it.", beat="obstacle3", tag="the low pale sun, a cloud",
      actors=[("milo", "milo", 1150, 905, .6)], props=[prop("cl", A.cloud, 1380, 500, 1.2), SHIV("sh", "arctic_low", stage=[("milo", "milo", 1150, 905, .6)])],
      fx=[("lookat", 0.02, "milo", -10), ("to", "w:cloud", "#{p}cl_w", {"x": "+=320", "y": "+=40", "duration": 2.4, "ease": "sine.inOut"}, "the cloud floats over the sun"),
          ("face", "w:cloud", "milo", "wow"), ("show", "w:front", "sh"), SHAKE("w:front")],
      words=[("w:low", "LOW SUN", .3, .3, .8, "sun")]),
    S("arctic_low", C("arctic_low", "milo", "body", 780, 0, -60, stage=[("milo", "milo", 1150, 905, .6)]), "Come back, sunshine! Oh, I am still so cold.", beat="obstacle3",
      tag="Milo: come back, sunshine", actors=[("milo", "milo", 1150, 905, .6)], props=[SHIV("sh", "arctic_low", stage=[("milo", "milo", 1150, 905, .6)])],
      fx=[("lookat", 0.02, "milo", -12), ("hop", "w:Come", "milo"), ("face", "w:still", "milo", "wow"), ("show", "w:cold.", "sh"), SHAKE("w:cold.")],
      words=[("w:back,", "COME BACK!", .5, .12, .85, "sun")]),
    S("arctic_low", (1300, 600, 1500), "Is the sun high in the sky today, or low?", q=True, beat="obstacle3", tag="question: sun high or low", pause=3.2, cam2=(1320, 620, 1420),
      actors=[("milo", "milo", 1150, 905, .6)], fx=[("lookat", 0.02, "milo", -10), ("signs", "w:high", ["HIGH", "LOW"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ LOW MOMENT: maybe the Arctic is too cold for me (gentle: nobody cries)
    S("hilltop", (960, 640, 1500), "Milo sits down in the snow, and looks at the far, white ice. He feels a little sad.", beat="low", tag="Milo sits, a little sad",
      hide=["poppy"], cam2=(940, 650, 1400), fx=[("face", 0.02, "milo", "sad"), ("lookat", "w:ice.", "milo", 8)],
      words=[("w:sad.", "A LITTLE SAD", .5, .16, .8, "pill")]),
    S("hilltop", MCL("hilltop", 0, -60, 760), "Maybe the Arctic is too cold, for a little bird like me.", beat="low", tag="Milo: too cold for me",
      hide=["poppy"], fx=[("face", 0.02, "milo", "sad")]),
    S("hilltop", (820, 620, 1600), "Poppy walks over, and sits right beside him. Don't worry, Milo. I will help you.", beat="low", tag="Poppy comes and stays",
      actors=[("poppy", "bear", 220, 880, .6), ("milo", "milo", 920, 885, .62)],
      fx=[("walk", "w:walks", "poppy", 240, 1.6), ("lookat", "w:beside", "milo", 0), ("face", "w:worry,", "milo", "happy"), ("nod", "w:help", "poppy")],
      words=[("w:help", "I WILL HELP", .55, .14, .8, "sun")]),
    S("hilltop", C("hilltop", "milo", "body", 1100, -240, -40, stage=[("milo", "milo", 920, 885, .62)]), "Can a good friend help Milo feel better? Yes, or no?", q=True, beat="low",
      tag="question: friend helps yes or no", pause=3.2, actors=[("poppy", "bear", 460, 880, .6), ("milo", "milo", 920, 885, .62)],
      cam2=C("hilltop", "milo", "body", 1040, -240, -60, stage=[("milo", "milo", 920, 885, .62)]), fx=[("nod", "w:friend", "poppy"), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: how Poppy stays warm, Milo's own idea, the snow nest
    S("hilltop", MCL("hilltop", 0, -60, 780), "Poppy, how do you stay so warm?", beat="solution", tag="Milo asks Poppy", hide=["poppy"],
      fx=[("face", 0.02, "milo", "wow"), ("hop", "w:warm?", "milo")], words=[("w:warm?", "HOW?", .5, .12, .9, "sun")]),
    S("hilltop", C("hilltop", "poppy", "head", 820, 60, 40, stage=[("poppy", "bear", 420, 880, .6)]), "Let me show you what is under my fluffy coat!", who="poppy", beat="solution",
      tag="Poppy: under my coat", actors=[("poppy", "bear", 420, 880, .6)], fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:show", "poppy"), ("lookat", "w:coat!", "poppy", 12)],
      words=[("w:fluffy", "FLUFFY COAT", .52, .12, .8, "pill")]),
    S("paper", (960, 560, 1500), "Polar bears have two layers of fur. A soft, thick layer close to the skin, and long hairs on top.", beat="fact", tag="fact: two layers of fur",
      actors=[("poppy", "bear", 520, 900, .66)], props=[prop("wl", A.warm_layers, 1300, 520, .9)],
      fx=[("nod", "w:two", "poppy"), ("to", "w:soft,", "#{p}wl-under", {"opacity": .45, "duration": .2, "yoyo": True, "repeat": 3}, "the soft underfur blinks"),
          ("to", "w:long", "#{p}wl-guard", {"opacity": .35, "duration": .2, "yoyo": True, "repeat": 3}, "the long hairs blink")],
      words=[("w:two", "TWO LAYERS", .78, .12, .7, "sun"), ("w:soft,", "SOFT FUR", .45, .5, .55, "pill"), ("w:long", "LONG HAIRS", .45, .34, .55, "pill")]),
    S("paper", (1100, 560, 1400), "How many layers of fur does a polar bear have? Two, or ten?", q=True, beat="fact", tag="question: two or ten", pause=3.2, cam2=(1140, 580, 1300), hide=["poppy"],
      actors=[("poppy", "bear", 520, 900, .66)], props=[prop("wl", A.warm_layers, 1300, 520, .9)],
      fx=[("signs", "w:Two,", ["TWO", "TEN"], 0, "wait:1.8")]),
    S("paper_blue", (960, 560, 1500), "And under the skin, a thick layer of fat keeps polar bears warm, even when they swim in cold water.", beat="fact", tag="fact: thick fat keeps them warm",
      actors=[("poppy", "bear", 520, 900, .66)], props=[prop("wl", A.warm_layers, 1300, 520, .9)],
      fx=[("to", "w:skin,", "#{p}wl-skin", {"opacity": .4, "duration": .2, "yoyo": True, "repeat": 3}, "the skin blinks"),
          ("to", "w:fat", "#{p}wl-fat", {"scale": 1.05, "transformOrigin": "50% 50%", "duration": .3, "yoyo": True, "repeat": 3}, "the fat pulses"), ("hop", "w:swim", "poppy")],
      words=[("w:fat", "THICK FAT", .78, .82, .7, "sun"), ("w:swim", "WARM IN WATER", .3, .3, .55, "pill")]),
    S("paper_blue", (1100, 560, 1400), "What keeps a polar bear warm? A thick layer of fat, or ice cream?", q=True, beat="fact", tag="question: fat or ice cream", pause=3.2, cam2=(1140, 580, 1300), hide=["poppy"],
      actors=[("poppy", "bear", 520, 900, .66)], props=[prop("wl", A.warm_layers, 1300, 520, .9)],
      fx=[("signs", "w:thick", ["THICK FAT", "ICE CREAM"], 0, "wait:1.8")]),
    S("hilltop", C("hilltop", "poppy", "all", 1000, 60, -40, stage=[("poppy", "bear", 420, 880, .6)]), "Can you give yourself a big, warm hug, like a cozy fur coat? Hug, hug!", q=True, who="poppy",
      beat="solution", tag="copy me: a warm hug", pause=3.0, actors=[("poppy", "bear", 420, 880, .6)], cam2=C("hilltop", "poppy", "all", 940, 60, -60, stage=[("poppy", "bear", 420, 880, .6)]),
      fx=[("face", 0.02, "poppy", "happy"), ("hop", "w:hug,", "poppy"), ("nod", "w:Hug,", "poppy"), ("hop", "w:hug!", "poppy")],
      words=[("w:hug,", "BIG HUG!", .5, .12, .9, "sun")]),
    S("hilltop", MCL("hilltop", 0, -60, 780), "I am a little bird. I do not have a fur coat like you.", beat="solution", tag="Milo: no fur coat", hide=["poppy"],
      fx=[("face", 0.02, "milo", "sad"), ("face", "w:coat", "milo", "wow")]),
    S("hilltop", MCL("hilltop", 0, -60, 840), "But I have an idea! A cozy nest, out of the wind, right next to my fluffy friend!", beat="solution", tag="Milo: I have an idea",
      hide=["poppy"], cam2=MCL("hilltop", 0, -70, 780), fx=[("face", 0.02, "milo", "happy"), ("hop", "w:idea!", "milo"), ("hop", "w:friend!", "milo")],
      words=[("w:idea!", "AN IDEA!", .5, .12, .9, "sun"), ("w:nest,", "COZY NEST", .78, .4, .7, "pill")]),
    S("hilltop", C("hilltop", "poppy", "head", 820, 60, 40, stage=[("poppy", "bear", 420, 880, .6)]), "A snow nest! Let's build it together!", who="poppy", beat="solution",
      tag="Poppy: let's build it", actors=[("poppy", "bear", 420, 880, .6)], fx=[("face", 0.02, "poppy", "happy"), ("hop", "w:nest!", "poppy"), ("nod", "w:together!", "poppy")],
      words=[("w:together!", "TOGETHER!", .52, .12, .85, "sun")]),
    S("snowbottom", (1300, 700, 1500), "Poppy pushes the soft snow into a round wall, with her big paws. Milo pats it smooth with his wings.", trans="iris", beat="solution", tag="building the snow nest",
      cam2=(1280, 720, 1400), actors=[("milo", "milo", 1150, 700, .6, False, True), ("poppy", "bear", 1560, 935, .6, True)],
      props=[NEST("ns", NX, NY, .8)],
      fx=[("fromto", "w:pushes", "#{p}ns-b5,#{p}ns-b4", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0, "duration": .4, "stagger": .3}, "snow blocks rise"),
          ("fromto", "w:round", "#{p}ns-b3,#{p}ns-b2", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0, "duration": .4, "stagger": .3}, "snow blocks rise"),
          ("fromto", "w:paws.", "#{p}ns-b1,#{p}ns-b0", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0, "duration": .4, "stagger": .3}, "snow blocks rise"),
          ("nod", "w:pushes", "poppy"), ("nod", "w:paws.", "poppy"), ("fly", "w:Milo", "milo", 1060, 760, 1.2), ("hop", "w:pats", "milo"), ("hop", "w:smooth", "milo")],
      words=[("w:wall,", "ROUND WALL", .5, .12, .8, "sun")]),
    S("snowbottom", (1260, 700, 1400), "Let's count the snow blocks! One, two, three!", q=True, beat="solution", tag="count the snow blocks", pause=1.0,
      actors=[("milo", "milo", 1060, 760, .6, False, True), ("poppy", "bear", 1560, 935, .6, True)], props=[NEST("ns", NX, NY, .8)], cam2=(1260, 720, 1320),
      fx=[("count", "w:One,", 3, CNT3, {"x": 920, "y": 190}), ("to", "w:One,", "#{p}ns-b1", {"y": -16, "duration": .15, "yoyo": True, "repeat": 1}, ""),
          ("to", "w:two,", "#{p}ns-b2", {"y": -16, "duration": .15, "yoyo": True, "repeat": 1}, ""), ("to", "w:three!", "#{p}ns-b3", {"y": -16, "duration": .15, "yoyo": True, "repeat": 1}, "")]),
    S("snowbottom", (1320, 660, 1400), "Milo snuggles into the nest. The snow wall stops the wind. And Poppy curls up, right beside him.", beat="solution", tag="Milo snuggles in, Poppy curls up",
      cam2=(1300, 680, 1300), actors=[("milo", "milo", 1060, 760, .6, False, True), ("poppy", "bear", 1560, 935, .6, True)], props=[NEST("ns", NX, NY, .8)],
      fx=[("fly", 0.1, "milo", NX, 940, 1.6), ("face", "w:wind.", "milo", "happy"), ("walk", "w:Poppy", "poppy", -60, 1.4), ("face", "w:curls", "poppy", "happy")],
      words=[("w:snuggles", "SNUGGLE!", .66, .14, .85, "sun")]),
    S("snowbottom", C("snowbottom", "milo", "body", 760, 0, -60), "Oh! Now I feel warm and cozy!", beat="solution", tag="Milo: warm and cozy",
      hide=["poppy"], props=[NEST("ns", NX, NY, .8)], fx=[("face", 0.02, "milo", "happy"), ("hop", "w:warm", "milo")],
      words=[("w:warm", "WARM!", .5, .12, .95, "sun")]),
    S("snowbottom", (1300, 640, 1300), "Is Milo cold now, or warm?", q=True, beat="solution", tag="question: cold or warm", pause=3.2, cam2=(1300, 660, 1220),
      actors=[("milo", "milo", NX, 940, .6), ("poppy", "bear", 1560, 935, .6, True)], props=[NEST("ns", NX, NY, .8)],
      fx=[("face", 0.02, "milo", "happy"), ("face", 0.02, "poppy", "happy"), ("signs", "w:cold", ["COLD", "WARM"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ the song moment: Milo SAYS the rhyme, then the tune on instruments
    S("snowbottom", (1300, 660, 1400), "Fluffy fur and a cozy nest. Warm with friends, that's the best!", beat="solution", tag="the nest rhyme",
      actors=[("milo", "milo", NX, 940, .6), ("poppy", "bear", 1560, 935, .6, True)], props=[NEST("ns", NX, NY, .8)],
      fx=[("face", 0.02, "milo", "happy"), ("nod", "w:Fluffy", "poppy"), ("hop", "w:Warm", "milo"), ("nod", "w:best!", "poppy")],
      words=[("w:Fluffy", "COZY NEST", .5, .1, .62, "sun"), ("w:Warm", "WARM WITH FRIENDS", .5, .2, .55, "pill")]),
    S("snowbottom", (1280, 620, 1640), who="", sing=SING_NEST, beat="song", tag="song: cozy nest", cam2=(1300, 640, 1500),
      actors=[("milo", "milo", NX, 940, .6), ("poppy", "bear", 1560, 935, .6, True)], props=[NEST("ns", NX, NY, .8)] + FLAKES(((900, 320), (1300, 260), (1640, 360))),
      fx=[("hop", TB(0), "milo"), ("nod", TB(2), "poppy"), ("hop", TB(4), "milo"), ("hop", TB(8), "poppy"), ("hop", TB(10), "milo"), ("nod", TB(12), "poppy"),
          ("to", TB(0), "#{p}f0_w,#{p}f1_w,#{p}f2_w", {"y": "+=120", "rotation": 60, "duration": 6, "ease": "none"}, "snowflakes drift down"),
          ("word", TB(0), "COZY NEST", {"x": 1280, "y": 330, "size": 80, "cls": "sun", "hold": 4.4})],
      words=[(TB(8), "WARM WITH FRIENDS", .5, .2, .6, "pill")]),
    S("snowbottom", C("snowbottom", "poppy", "head", 820, -60, 40, stage=[("poppy", "bear", 1560, 935, .6, True)]), "Now we can play in the snow together!", who="poppy", beat="solution",
      tag="Poppy: now we can play", actors=[("poppy", "bear", 1560, 935, .6, True)], fx=[("face", 0.02, "poppy", "happy"), ("hop", "w:play", "poppy")],
      words=[("w:play", "PLAY TIME!", .4, .12, .85, "sun")]),
    # ------------------------------------------------------------ WARM ENDING: play, evening in the nest, thank-yous, next time
    S("hillmid", WIDE, "Poppy makes big paw prints in the snow, and Milo makes tiny bird prints, right beside them.", trans="iris", beat="ending", tag="paw prints and bird prints",
      cam2=(960, 580, 1780), props=[prop("p%d" % k, A.paw_print, 330 + k * 130, 958 + (k % 2) * 18, .55, True) for k in range(3)] + [prop("b%d" % k, A.bird_print, 840 + k * 70, 950 + (k % 2) * 12, .5, True) for k in range(3)],
      fx=[("walk", "w:Poppy", "poppy", 260, 2.6), ("show", "w:paw", "p0"), ("show", "w:prints", "p1"), ("show", "w:snow,", "p2"),
          ("hop", "w:Milo", "milo"), ("show", "w:tiny", "b0"), ("show", "w:bird", "b1"), ("show", "w:beside", "b2"), ("to", "w:tiny", "#{p}milo_w", {"x": "+=220", "duration": 1.4, "ease": "sine.inOut"}, "Milo hops along"), ("hop", "w:bird", "milo"), ("hop", "w:beside", "milo")],
      words=[("w:tiny", "TINY PRINTS", .66, .14, .8, "sun")]),
    S("hillmid", C("hillmid", "milo", "body", 820, -120, 20, stage=[("milo", "milo", 940, 920, .62)]), "Look, Poppy! Big prints and tiny prints, side by side. Just like us!", beat="ending",
      tag="Milo: prints side by side", actors=[("milo", "milo", 940, 920, .62)], props=[prop("p%d" % k, A.paw_print, 560 + k * 110, 958 + (k % 2) * 18, .55) for k in range(2)] + [prop("b%d" % k, A.bird_print, 840 + k * 70, 950 + (k % 2) * 12, .5) for k in range(2)],
      fx=[("face", 0.02, "milo", "happy"), ("lookat", "w:Big", "milo", 10), ("hop", "w:side", "milo"), ("hop", "w:us!", "milo")],
      words=[("w:side", "SIDE BY SIDE", .5, .12, .8, "pill")]),
    S("arctic_eve", WIDE, "The sun goes down, and the sky turns pink. Milo and Poppy snuggle up in the cozy nest.", trans="iris", beat="ending", tag="evening in the nest",
      cam2=(940, 600, 1700), props=[NEST("ne", EX, EY, .8)], fx=[("face", 0.02, "milo", "happy"), ("face", 0.02, "poppy", "happy"), ("hop", "w:snuggle", "milo"), ("nod", "w:nest.", "poppy")],
      words=[("w:pink.", "PINK SKY", .5, .2, .85, "sun")]),
    S("arctic_eve", C("arctic_eve", "milo", "body", 760, 0, -60), "Thank you, Poppy! You helped me get warm.", beat="ending", tag="Milo: thank you",
      hide=["poppy"], props=[NEST("ne", EX, EY, .8)], fx=[("face", 0.02, "milo", "happy"), ("hop", "w:Thank", "milo")], words=[("w:Thank", "THANK YOU!", .5, .12, .85, "sun")]),
    S("arctic_eve", C("arctic_eve", "poppy", "head", 820, -40, 20), "And you found a cozy idea, Milo! Good friends help each other.", who="poppy", beat="ending", tag="Poppy: friends help",
      hide=["milo"], fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:idea,", "poppy"), ("nod", "w:help", "poppy")], words=[("w:help", "HELP EACH OTHER", .62, .16, .62, "pill")]),
    S("arctic_eve", (1000, 640, 1500), "When you feel cold, find a cozy spot, and snuggle up close with someone who loves you.", beat="ending", tag="the lesson", cam2=(1020, 660, 1400),
      props=[NEST("ne", EX, EY, .8)], fx=[("hop", "w:cold,", "milo"), ("nod", "w:cozy", "poppy"), ("hop", "w:snuggle", "milo"), ("nod", "w:loves", "poppy")],
      words=[("w:snuggle", "SNUGGLE UP", .5, .14, .8, "sun")]),
    S("arctic_eve", C("arctic_eve", "milo", "body", 900, 40, -20), "Do you remember? How many layers of fur does a polar bear have? Two, or one?", q=True, beat="ending",
      tag="question: two or one", pause=3.2, hide=["poppy"], props=[NEST("ne", EX, EY, .8)], cam2=C("arctic_eve", "milo", "body", 830, 40, -60),
      fx=[("hop", "w:remember?", "milo"), ("signs", "w:Two,", ["TWO", "ONE"], 0, "wait:1.8")]),
    S("arctic_eve", C("arctic_eve", "poppy", "all", 1000, -60, -40), "And what is under a polar bear's skin? A thick layer of fat, or feathers?", q=True, beat="ending", tag="question: fat or feathers", pause=3.2,
      hide=["milo"], cam2=C("arctic_eve", "poppy", "all", 940, -60, -60), fx=[("nod", "w:skin?", "poppy"), ("signs", "w:thick", ["THICK FAT", "FEATHERS"], 0, "wait:1.8")]),
    S("arctic_eve", (960, 540, 1920), "Fluffy fur and a cozy nest. Warm with friends, that's the best!", beat="ending", tag="the closing rhyme", cam2=(980, 560, 1860),
      props=[NEST("ne", EX, EY, .8)], fx=[("hop", "w:Fluffy", "milo"), ("nod", "w:nest.", "poppy"), ("hop", "w:Warm", "milo"), ("nod", "w:best!", "poppy")],
      words=[("w:Fluffy", "COZY NEST", .6, .14, .65, "sun"), ("w:Warm", "WARM WITH FRIENDS", .6, .25, .55, "pill")]),
    S("arctic_eve", (1040, 700, 1100), who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(1040, 680, 1040), props=[NEST("ne", EX, EY, .8)] + FLAKES(((760, 460), (1040, 420), (1320, 470))),
      fx=[("hop", 1.0, "milo"), ("nod", 2.0, "poppy"), ("hop", 2.2, "milo"),
          ("to", 0.1, "#{p}f0_w,#{p}f1_w,#{p}f2_w", {"y": "+=110", "rotation": 60, "duration": 4.6, "ease": "none"}, "snowflakes drift down")],
      words=[(TB(3), "HOORAY!", .5, .12, .9, "sun")]),
    S("arctic_eve", C("arctic_eve", "milo", "body", 900, 0, -20), "Next time: Poppy and the Dancing Sky! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure",
      hide=["poppy"], props=[NEST("ne", EX, EY, .8)], fx=[("hop", "w:next", "milo")],
      words=[("w:Next", "NEXT TIME!", .8, .2, .62, "sun"), ("w:See", "SEE YOU SOON!", .8, .33, .5, "pill")]),
    *intro_shots(),      # and again as the last shots: the video ends on the logo with the whole cast
]

# thumbnail (thumb.py): the promise of the first shot: Milo shivering beside a cozy Poppy; 1 word, none of the title's words, no watermark
THUMBS = {
    "za_ep11": {"place": "arctic", "cam": (1000, 640, 1100),
                "actors": [("milo", 760, 935, .95, False, ''), ("bear", 1400, 930, .64, True, '')],
                "props": [(A.shiver, 760, 935 - 143, .72)],
                "words": [("BRRR!", 1080, 230, 200, "sun", -6)]},
}
