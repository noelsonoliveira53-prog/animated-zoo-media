"""za_ep12 - Milo's Zoo Adventures: "Can Slow Tula Finish the Big Ocean Race?" (theme title "Tula and the Slow, Slow Race"; cartoon adventure, the 3D
music-and-sync process: "beat"). Ocean week, adventure 1.
Race day in the blue ocean: swim to the Big Rock and touch the gold star. Milo is the helper on the rock (a bird stays in the air: he is never under
the water). Zip and Pearl, two little fish, are very fast; Tula the green sea turtle is slow. The fish zoom away and Tula is left at the back, but
she keeps paddling ("slow, but steady"). The fish cannot zoom in the thick seagrass (it tickles, they have to wiggle slowly), then they rush into
the dark one of two ways without thinking: it only goes round and comes out at the seagrass again. Low moment: the two fish rest on the sand, very
tired, "maybe we cannot finish the race" (a little sad, nobody cries, nobody is lost or stuck). Tula arrives at her own pace, nibbles the seagrass
(a path opens), stops and thinks at the two ways and knows the bright one. The fish find the idea themselves: no zooming, slow and steady right
behind Tula. They swim through the coral garden side by side and touch the gold star all together. Nobody is hurt, lost, crying or trapped.

FACTS, read at the source on Nov 21 2026, about 1:00 PM ET (each page fetched by the session's page reader, which quoted these sentences verbatim):
 [NWF] National Wildlife Federation, "Green Sea Turtle", nwf.org/Educational-Resources/Wildlife-Guide/Reptiles/Sea-Turtles/Green-Sea-Turtle
   "Green sea turtles have paddle-like limbs called flippers that allow the turtle to move quickly and easily through the water."
   "Adult green sea turtles are herbivores."   "They will travel long distances, even across oceans, to return to their preferred breeding site."
 [NOAA] NOAA Fisheries, "Green Turtle", fisheries.noaa.gov/species/green-turtle
   "They are unique among sea turtles in that they are herbivores, eating mostly seaweed, seagrasses, and algae."
 [NMSF] National Marine Sanctuary Foundation, "Sea Wonder: Green Sea Turtle", marinesanctuary.org/blog/sea-wonder-green-sea-turtle
   "Green sea turtles mostly munch on algae and sea grasses in adulthood, making them the only herbivorous species of sea turtles."
   "Green sea turtles have four paddle-shaped flippers that allow them to move quickly and effortlessly through the ocean."
 [BOEM] Bureau of Ocean Energy Management, "Green Sea Turtles", boem.gov/newsroom/ocean-science-news/green-sea-turtles
   "Primarily herbivorous as adults, feeding mainly on seagrasses and algae."
   "Like most sea turtles, green turtles are known for their long migrations between feeding grounds and nesting sites"
 Said as animal facts in the film (three fact shots, questions, recap): green sea turtles have flippers shaped like paddles, and flippers help them
 move easily through the water [NWF, NMSF]; grown-up green sea turtles eat plants, like seagrass [NOAA, NWF, NMSF, BOEM]; green sea turtles travel
 long distances, even across oceans [NWF, BOEM].
 NOT said as facts: how fast or slow a sea turtle swims (BOEM's "up to 35 mph" was not used; that Tula is slower than the two fish is THIS story),
 "steady pace" (the theme's note; no page read today says it), that a turtle knows a way because she travels far (Tula says she has been this way
 before: her story), that seagrass gives her strength. Zip and Pearl are made-up little fish of no named kind; nothing is said about fish as a fact.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep12 as A
import kit
from kit import Kit, S, prop
from intro import INTRO_STAGES, intro_shots      # the main intro, right after the hook and as the last shots (owner, Nov 20 4:50 PM)

EP = {"id": "za_ep12", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "tula": {"voice": "bf_emma", "speed": .8, "gain": .8},
               "zip": {"voice": "af_nova", "speed": .95, "pitch": 5, "formant": 1.22, "gain": 1.1}, "pearl": {"voice": "af_sky", "speed": .9, "pitch": 6, "formant": 1.25, "gain": .95}},
      "title": "Can Slow Tula Finish the Big Ocean Race?", "thumb_text": "LAST PLACE?",
      "series": "Milo's Zoo Adventures",
      "description": ("Can slow Tula finish the big ocean race? Zip and Pearl, two speedy little fish, zoom away to the Big Rock, and Tula the sea turtle is left at the back. "
                      "But thick seagrass and a wrong turn slow the fast swimmers down, while Tula keeps paddling, slow and steady. "
                      "A gentle ocean adventure for ages 2-6 about going at your own pace and finishing together, with questions to answer, a count-along and a paddling tune.\n"
                      "Kids see how green sea turtles have flippers shaped like paddles, how grown-up green sea turtles eat plants like seagrass, "
                      "and how green sea turtles travel long distances, even across oceans.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNational Wildlife Federation (green sea turtle); NOAA Fisheries (green turtle); "
                      "National Marine Sanctuary Foundation (green sea turtle); Bureau of Ocean Energy Management (green sea turtles)."),
      "tags": ["sea turtle for kids", "green sea turtle", "what do sea turtles eat", "ocean animals for kids", "under the sea", "slow and steady", "turtle race story",
               "animal stories for kids", "friendship story for kids", "kids adventure cartoon", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

MILO_S = ("milo", "milo", A.ISLE_TOP[0], A.ISLE_TOP[1], .5)
MILO_R = ("milo", "milo", A.ROCK_TOP[0], A.ROCK_TOP[1], .5)
T = lambda x, y, s=.55, f=False: ("tula", "turtle", x, y, s, f)
Z = lambda x, y, s=.42, f=False: ("zip", "fish_zip", x, y, s, f)
PL = lambda x, y, s=.42, f=False: ("pearl", "fish_pearl", x, y, s, f)
STAGES = {
    "ocean": [T(760, 740, .6), Z(1280, 540), PL(1420, 760)],
    "sea_start": [MILO_S, T(860, 790), Z(1000, 570), PL(1180, 700)],
    "meadow": [Z(900, 600), PL(1120, 770), T(420, 740)],
    "fork": [T(760, 740), Z(360, 590), PL(320, 830)],
    "reef": [T(980, 740, .58), Z(520, 560), PL(470, 820)],
    "bigrock": [MILO_R, T(1070, 740), Z(1191, 560), PL(1130, 880)],
    "bigrock_eve": [MILO_R, T(800, 740), Z(430, 580), PL(400, 830)],
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
TCL = lambda place, w=1000, dx=0, dy=0, stage=None: C(place, "tula", "all", w, dx, dy, stage=stage)          # Tula whole, close
FCL = lambda place, who, w=700, dx=20, dy=-10, stage=None: C(place, who, "body", w, dx, dy, stage=stage)   # a fish close
MCLS = (A.ISLE_TOP[0], 170, 800); MCLR = (A.ROCK_TOP[0] - 40, 150, 800); MQR = (A.ROCK_TOP[0] - 60, 110, 920)      # Milo on his rock: low in the frame, under the signs

SWIM = lambda at, who, dx, d, ease="sine.inOut": ("to", at, "#{p}%s_w" % who, {"x": "+=%d" % dx, "duration": d, "ease": ease}, who + " swims")
FLAP = lambda at, n=7, d=.45: ("to", at, "#{p}tula-ff", {"rotation": 24, "svgOrigin": "95 -122", "duration": d, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "Tula paddles")
WIG = lambda at, who, n=9, d=.14: ("to", at, "#{p}%s" % who, {"rotation": 7, "transformOrigin": "50% 50%", "duration": d, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, who + " wiggles")
BOB = lambda at, who, n=5: ("to", at, "#{p}%s" % who, {"y": "-=18", "duration": .5, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "")
PUFFS = lambda at, name: ("fromto", at, "#{p}%s-0,#{p}%s-1,#{p}%s-2" % (name, name, name), {"opacity": 0}, {"opacity": 1, "duration": .3, "stagger": .25, "yoyo": True, "repeat": 5}, "little puffs")
GRASS = lambda x=1330, y=905, hidden=False: prop("sg", A.seagrass_front, x, y, 1.0, hidden)
NIB = lambda at, k: ("to", at, "#{p}sg-b%d" % k, {"scaleY": .16, "transformOrigin": "50% 100%", "duration": .35, "ease": "power2.in"}, "a blade is nibbled short")
SHORT = lambda ks=(0, 1, 2, 3, 4, 5): ("to", 0.01, ",".join("#{p}sg-b%d" % k for k in ks), {"scaleY": .16, "transformOrigin": "50% 100%", "duration": .01}, "")

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. The rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_PADDLE = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "E4:1 G4:1 C5:2 B4:1 D5:1 G4:1", "rest": 1},      # slow and steady, here we go (C bar, G bar)
                                   {"text": "~ ~ ~ ~ ~ ~", "notes": "A4:1 C5:1 F4:2 E4:1 G4:1 C5:1", "rest": 1}])     # paddle, paddle, nice and slow (F bar, C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "G4:1 B4:1 D5:1 B4:1 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune
CNT3 = 0.56                                      # seconds from "One" to "three" (set from the timing file)

HOOK_ST = [T(900, 740, .6), Z(430, 500), PL(350, 800)]
START_GO = [MILO_S, T(860, 790), Z(1000, 570), PL(1180, 700)]
BACK_ST = [T(520, 740, .6), Z(1560, 470, .26), PL(1640, 600, .26)]
PAPER_T = [T(640, 800, .9)]
REST_ST = [Z(860, 890), PL(1130, 905)]
ARRIVE_ST = [Z(860, 890), PL(1130, 905), T(-160, 740)]
MEET_ST = [Z(860, 890), PL(1130, 905), T(400, 740)]
EAT_ST = [T(900, 760), Z(380, 600), PL(330, 820)]
ROCK_IN = [MILO_R, T(560, 740), Z(260, 520), PL(180, 840)]

SHOTS = [
    # ------------------------------------------------------------ HOOK: slow Tula, the fast fish zoom past (first 5 seconds)
    S("ocean", (960, 600, 1700), "Can slow Tula finish the big ocean race? Look! The fast fish zoom right past her!", beat="hook", tag="hook: the fish zoom past Tula",
      cam2=(1000, 610, 1600), actors=HOOK_ST, props=[prop("sl", A.speed_lines, 420, 640, 1.0, True)],
      fx=[("face", 0.02, "tula", "wow"), FLAP(0.2, 13), BOB(0.2, "tula", 9), WIG(0.3, "zip", 13), WIG(0.5, "pearl", 13), SWIM("w:Look!", "zip", 1900, 1.9, "power1.in"), SWIM("w:fast", "pearl", 2000, 1.9, "power1.in"),
          ("show", "w:zoom", "sl"), ("lookat", "w:past", "tula", -6), ("hide", "e:past", "sl")],
      words=[(0.4, "RACE DAY!", .5, .13, 1.0, "sun"), ("w:zoom", "ZOOM!", .78, .3, .9, "pill")]),
    *intro_shots(),      # the main intro, right after the hook
    # ------------------------------------------------------------ GOAL: swim to the Big Rock and touch the gold star
    S("sea_start", WIDE, "Hello, I'm Milo! Today is the big ocean race, and I am the helper on the rock.", trans="iris", beat="goal", tag="start wide: Milo on his rock",
      cam2=(1000, 520, 1800), fx=[("hop", "w:Hello,", "milo"), BOB(0.3, "zip"), BOB(0.6, "pearl"), FLAP(0.3, 11), ("hop", "w:helper", "milo")],
      words=[("w:race,", "THE OCEAN RACE", .36, .2, .7, "sun")]),
    S("sea_start", (1180, 660, 1100), "Here are the swimmers. Zip the yellow fish, Pearl the pink fish, and my friend Tula the sea turtle.", beat="goal", tag="the three swimmers",
      cam2=(1180, 665, 1050), fx=[("hop", "w:Zip", "zip"), ("hop", "w:Pearl", "pearl"), ("nod", "w:Tula", "tula"), FLAP("w:Tula", 5)],
      words=[("w:Zip", "ZIP", .34, .1, .6, "pill"), ("w:Pearl", "PEARL", .74, .47, .6, "pill"), ("w:Tula", "TULA", .13, .34, .6, "pill")]),
    S("sea_start", MCLS, "Swim all the way to the Big Rock, and touch the gold star!", beat="goal", tag="Milo: touch the gold star",
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:Big", "milo"), ("hop", "w:star!", "milo")], words=[("w:gold", "GOLD STAR!", .5, .12, .85, "sun")]),
    S("sea_start", FCL("sea_start", "zip"), "I am Zip, and I am super fast! I will be there first!", who="zip", beat="goal", tag="Zip: super fast",
      hide=["pearl", "tula"], fx=[("face", 0.02, "zip", "happy"), ("hop", "w:Zip,", "zip"), WIG("w:super", "zip"), ("hop", "w:first!", "zip")],
      words=[("w:fast!", "SUPER FAST!", .5, .13, .85, "sun")]),
    S("sea_start", FCL("sea_start", "pearl", 720, 0), "I am fast too! Tula, you are so slow. Hee hee!", who="pearl", beat="goal", tag="Pearl: you are so slow",
      hide=["zip", "tula"], fx=[("face", 0.02, "pearl", "happy"), ("hop", "w:fast", "pearl"), WIG("w:Hee", "pearl", 7)],
      words=[("w:slow.", "SO SLOW!", .5, .13, .85, "pill")]),
    S("sea_start", TCL("sea_start", 860, 170, -20), "I am slow. But I want to try. I want to touch the gold star too!", who="tula", beat="goal", tag="Tula: I want to try",
      hide=["zip", "pearl"], fx=[("face", 0.02, "tula", "sad"), ("face", "w:But", "tula", "happy"), ("nod", "w:try.", "tula"), FLAP("w:touch", 5)],
      words=[("w:try.", "I WANT TO TRY!", .56, .13, .8, "sun")]),
    S("sea_start", (1200, 600, 1140), "Who is the slow swimmer? Zip, or Tula?", q=True, beat="goal", tag="question: who is slow", pause=3.2, cam2=(1200, 610, 1090),
      fx=[BOB(0.2, "zip", 9), FLAP(0.2, 13), ("signs", "w:Zip,", ["ZIP", "TULA"], 1, "wait:1.8")]),
    S("sea_start", WIDE, "Ready, steady, go! Zip and Pearl zoom away. And Tula paddles, nice and slow.", beat="goal", tag="ready steady go",
      cam2=(1040, 540, 1840), actors=START_GO, props=[prop("sl", A.speed_lines, 1000, 600, 1.0, True)],
      fx=[("hop", "w:Ready,", "milo"), ("hop", "w:steady,", "milo"), ("hop", "w:go!", "milo", 2), SWIM("e:go!", "zip", 1400, 1.5, "power2.in"), SWIM("w:Zip", "pearl", 1300, 1.5, "power2.in"),
          ("show", "w:zoom", "sl"), FLAP("w:Tula", 7), SWIM("w:Tula", "tula", 150, 3.0)],
      words=[("w:go!", "GO!", .4, .42, 1.2, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: Tula is left far behind (she keeps paddling)
    S("ocean", WIDE, "The fish are so fast! Soon they are far, far away. And Tula is all the way at the back.", trans="iris", beat="obstacle1", tag="the fish far away, Tula at the back",
      cam2=(900, 560, 1800), actors=BACK_ST,
      fx=[SWIM(0.1, "zip", 420, 5.5, "none"), SWIM(0.1, "pearl", 380, 5.5, "none"), FLAP(0.2, 15), SWIM(0.2, "tula", 120, 6.0), ("face", "w:back.", "tula", "sad")],
      words=[("w:far,", "FAR AWAY", .78, .2, .7, "sun"), ("w:back.", "AT THE BACK", .3, .3, .65, "pill")]),
    S("ocean", TCL("ocean", 1000, 0, -20, stage=BACK_ST), "Wait for me, friends! Oh. They are gone already.", who="tula", beat="obstacle1", tag="Tula: wait for me",
      actors=[BACK_ST[0]], fx=[("face", 0.02, "tula", "wow"), FLAP(0.1, 5), ("face", "w:Oh.", "tula", "sad"), ("lookat", "w:gone", "tula", 6)],
      words=[("w:Wait", "WAIT FOR ME!", .5, .13, .8, "sun")]),
    S("ocean", (700, 640, 1500), "Who is at the back of the race? Tula, or Pearl?", q=True, beat="obstacle1", tag="question: who is at the back", pause=3.2, cam2=(720, 660, 1420),
      actors=[BACK_ST[0]], fx=[FLAP(0.2, 15), ("signs", "w:Tula,", ["TULA", "PEARL"], 0, "wait:1.8")]),
    S("ocean", TCL("ocean", 1100, 40, -20, stage=BACK_ST), "I am slow, but I am steady. Paddle, paddle. I will not stop!", who="tula", beat="obstacle1", tag="Tula: slow but steady",
      actors=[BACK_ST[0]], cam2=TCL("ocean", 1040, 120, -20, stage=BACK_ST),
      fx=[("face", 0.02, "tula", "happy"), FLAP("w:Paddle,", 9), SWIM("w:Paddle,", "tula", 130, 3.0), ("nod", "w:stop!", "tula")],
      words=[("w:steady.", "SLOW AND STEADY", .5, .13, .75, "sun")]),
    S("paper", (960, 560, 1500), "Green sea turtles have flippers, shaped like paddles. Flippers help them move easily through the water.", beat="fact", tag="fact: flippers like paddles",
      actors=PAPER_T, props=[prop("pd", A.paddle, 1400, 540, .8, True)],
      fx=[("to", "w:flippers,", "#{p}tula-ff,#{p}tula-bf", {"opacity": .35, "duration": .2, "yoyo": True, "repeat": 5}, "the flippers blink"), ("show", "w:paddles.", "pd"),
          FLAP("w:Flippers", 9), SWIM("w:move", "tula", 110, 2.4)],
      words=[("w:flippers,", "FLIPPERS", .32, .13, .75, "sun"), ("w:paddles.", "LIKE PADDLES", .5, .28, .6, "pill")]),
    S("paper", (1000, 560, 1500), "What are Tula's flippers shaped like? Paddles, or wheels?", q=True, beat="fact", tag="question: paddles or wheels", pause=3.2, cam2=(1010, 580, 1420),
      actors=PAPER_T, props=[prop("pd", A.paddle, 1400, 560, .8)], fx=[FLAP(0.2, 15), ("signs", "w:Paddles,", ["PADDLES", "WHEELS"], 0, "wait:1.8")]),
    S("ocean", TCL("ocean", 1100, 20, -40, stage=BACK_ST), "Can you paddle with your arms, like me? Paddle, paddle, paddle!", q=True, who="tula", beat="obstacle1", tag="copy me: paddle your arms",
      pause=3.0, actors=[BACK_ST[0]], cam2=TCL("ocean", 1040, 20, -50, stage=BACK_ST),
      fx=[("face", 0.02, "tula", "happy"), FLAP("w:Paddle,", 7, .4), BOB("w:Paddle,", "tula", 9), FLAP("wait:0.2", 7, .4), ("nod", "wait:1.6", "tula")],
      words=[("w:Paddle,", "PADDLE!", .5, .13, .9, "sun"), ("wait:0.3", "YOUR TURN!", .5, .27, .7, "pill")]),
    # ------------------------------------------------------------ OBSTACLE 2: the thick seagrass (the fast fish cannot zoom)
    S("meadow", WIDE, "Far ahead, Zip and Pearl zoom into the seagrass meadow. But the grass is tall and thick!", trans="iris", beat="obstacle2", tag="the fish zoom into the seagrass",
      cam2=(1000, 560, 1820), actors=[Z(100, 600), PL(-40, 770)], props=[GRASS()],
      fx=[SWIM(0.1, "zip", 800, 1.6, "power2.out"), SWIM(0.3, "pearl", 1160, 1.8, "power2.out"), ("face", "w:But", "zip", "wow"), ("face", "w:But", "pearl", "wow"),
          WIG("w:tall", "zip", 7), WIG("w:thick!", "pearl", 7)],
      words=[("w:seagrass", "SEAGRASS", .3, .2, .8, "sun"), ("w:thick!", "TALL AND THICK", .5, .36, .6, "pill")]),
    S("meadow", FCL("meadow", "zip", 760), "Oh no! I cannot zoom in here. The grass tickles my tummy!", who="zip", beat="obstacle2", tag="Zip: it tickles",
      hide=["pearl", "tula"], props=[GRASS(1190, 905)], fx=[("face", 0.02, "zip", "wow"), WIG("w:cannot", "zip", 7), WIG("w:tickles", "zip", 13, .1)],
      words=[("w:tickles", "IT TICKLES!", .42, .13, .8, "sun")]),
    S("meadow", (1100, 660, 1300), "We have to wiggle, slowly, slowly. This takes so long!", who="pearl", beat="obstacle2", tag="Pearl: wiggle slowly",
      hide=["tula"], cam2=(1160, 660, 1260), props=[GRASS()],
      fx=[("face", 0.02, "pearl", "sad"), WIG("w:wiggle,", "pearl", 15, .18), WIG("w:wiggle,", "zip", 15, .2), SWIM("w:wiggle,", "pearl", 90, 3.4, "none"), SWIM("w:slowly,", "zip", 80, 3.0, "none")],
      words=[("w:long!", "SO LONG!", .3, .14, .8, "pill")]),
    S("meadow", (1060, 640, 1500), "Can the fish swim fast in the tall grass? Yes, or no?", q=True, beat="obstacle2", tag="question: fast in the grass yes or no", pause=3.2, cam2=(1080, 660, 1420),
      hide=["tula"], props=[GRASS()], fx=[WIG(0.3, "zip", 21, .2), WIG(0.5, "pearl", 21, .2), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 3: two ways, and no time to think
    S("fork", WIDE, "Next, the fish come to two ways. One is dark, and one is bright. Which one goes to the Big Rock?", trans="iris", beat="obstacle3", tag="the two ways",
      cam2=(960, 560, 1840), hide=["tula"], actors=[Z(-60, 600), PL(-160, 820)],
      fx=[SWIM(0.1, "zip", 300, 1.6, "power2.out"), SWIM(0.2, "pearl", 360, 1.8, "power2.out"), ("face", "w:Which", "zip", "wow")],
      words=[("w:dark,", "DARK", .29, .3, .7, "pill"), ("w:bright.", "BRIGHT", .71, .3, .7, "sun"), ("w:Which", "?", .5, .5, 1.3, "sun")]),
    S("fork", (420, 660, 1100), "No time to think! This way, quick!", who="zip", beat="obstacle3", tag="Zip: this way, quick",
      actors=[Z(240, 600), PL(200, 820)], props=[prop("sl", A.speed_lines, 330, 640, .9, True)],
      fx=[("face", 0.02, "zip", "happy"), ("hop", "w:No", "zip"), ("show", "w:This", "sl"), SWIM("w:This", "zip", 330, 1.0, "power2.in"), SWIM("w:quick!", "pearl", 370, 1.0, "power2.in"),
          ("to", "w:quick!", "#{p}zip_w", {"opacity": 0, "duration": .35}, "Zip goes into the dark way"), ("to", "e:quick!", "#{p}pearl_w", {"opacity": 0, "duration": .35}, "Pearl follows")],
      words=[("w:quick!", "QUICK!", .72, .16, .85, "sun")]),
    S("fork", (600, 600, 1300), "Zip and Pearl zoom into the dark way. But it only goes round, and round, and round.", beat="obstacle3", tag="the dark way goes round",
      cam2=(620, 600, 1220), actors=[], props=[prop("la", A.loop_arrow, 560, 430, 1.0, True), prop("bb", A.bubbles, 470, 800, 1.0)],
      fx=[("to", 0.2, "#{p}bb_w", {"y": "-=160", "opacity": 0, "duration": 2.4, "ease": "none"}, "bubbles float up"), ("show", "w:only", "la"),
          ("to", "w:round,", "#{p}la", {"rotation": 720, "transformOrigin": "50% 50%", "duration": 3.2, "ease": "none"}, "the arrow goes round")],
      words=[("w:round,", "ROUND AND ROUND", .76, .5, .55, "pill")]),
    S("meadow", WIDE, "And look where they come out. Back at the seagrass meadow! That was the wrong way.", trans="iris", beat="obstacle3", tag="back at the seagrass",
      cam2=(940, 560, 1820), actors=[Z(-220, 610), PL(-380, 790)], props=[GRASS()],
      fx=[SWIM("w:look", "zip", 900, 1.8, "power2.out"), SWIM("w:they", "pearl", 960, 1.9, "power2.out"), ("face", "w:Back", "zip", "wow"), ("face", "w:Back", "pearl", "wow"),
          ("face", "w:wrong", "zip", "sad"), ("face", "w:wrong", "pearl", "sad")],
      words=[("w:Back", "BACK AGAIN!", .5, .2, .8, "sun"), ("w:wrong", "WRONG WAY", .5, .38, .65, "pill")]),
    S("meadow", (700, 660, 1400), "Was the dark way the right way? Yes, or no?", q=True, beat="obstacle3", tag="question: right way yes or no", pause=3.2, cam2=(720, 680, 1320),
      actors=[Z(680, 610), PL(580, 790)], fx=[("face", 0.02, "zip", "sad"), ("face", 0.02, "pearl", "sad"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ LOW MOMENT: the fast fish are too tired (gentle: nobody cries)
    S("meadow", (1000, 700, 1500), "Zip and Pearl sink down to the soft sand. They swam so fast, and now they are very tired.", beat="low", tag="the fish rest on the sand",
      cam2=(1000, 720, 1400), actors=[Z(860, 700), PL(1130, 740)], props=[prop("pf", A.puff, 960, 800, .9, True), prop("pg", A.puff, 1230, 815, .9, True)],
      fx=[("face", 0.02, "zip", "sleepy"), ("face", 0.02, "pearl", "sleepy"), ("to", 0.2, "#{p}zip_w", {"y": 890, "duration": 1.6, "ease": "sine.inOut"}, "Zip sinks down"),
          ("to", 0.5, "#{p}pearl_w", {"y": 905, "duration": 1.6, "ease": "sine.inOut"}, "Pearl sinks down"), ("show", "w:swam", "pf", None, False), PUFFS("w:swam", "pf"),
          ("show", "w:now", "pg", None, False), PUFFS("w:now", "pg")],
      words=[("w:tired.", "SO TIRED", .5, .14, .85, "pill")]),
    S("meadow", FCL("meadow", "zip", 740, 20, -30, stage=REST_ST), "My tail is too tired to wag. Maybe we cannot finish the race.", who="zip", beat="low", tag="Zip: maybe we cannot finish",
      actors=[REST_ST[0]], fx=[("face", 0.02, "zip", "sad")]),
    S("meadow", FCL("meadow", "pearl", 740, 0, -30, stage=REST_ST), "We went so fast. And we are still not there.", who="pearl", beat="low", tag="Pearl: still not there",
      actors=[REST_ST[1]], fx=[("face", 0.02, "pearl", "sad")], words=[("w:still", "NOT THERE YET", .5, .13, .7, "pill")]),
    S("meadow", (1000, 720, 1300), "How do the fish feel now? Tired, or fast?", q=True, beat="low", tag="question: tired or fast", pause=3.2, cam2=(1000, 740, 1220),
      actors=REST_ST, fx=[("face", 0.02, "zip", "sleepy"), ("face", 0.02, "pearl", "sleepy"), ("signs", "w:Tired,", ["TIRED", "FAST"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: Tula arrives at her own pace; the path, the right way, the fish's own idea
    S("meadow", WIDE, "Then, paddle, paddle, here comes Tula! Slow and steady, she never stopped.", beat="solution", tag="here comes Tula",
      cam2=(900, 560, 1840), actors=ARRIVE_ST,
      fx=[("face", 0.02, "tula", "happy"), ("face", 0.02, "zip", "sleepy"), ("face", 0.02, "pearl", "sleepy"), FLAP(0.1, 13), SWIM(0.1, "tula", 560, 4.6), ("face", "w:Tula!", "zip", "wow"), ("face", "w:Tula!", "pearl", "wow")],
      words=[("w:Tula!", "HERE COMES TULA!", .5, .16, .75, "sun")]),
    S("meadow", FCL("meadow", "zip", 760, 0, -30, stage=REST_ST), "Tula! You are still swimming? How do you keep going?", who="zip", beat="solution", tag="Zip: how do you keep going",
      actors=[Z(860, 890, .42, True)], fx=[("face", 0.02, "zip", "wow"), ("hop", "w:Tula!", "zip")], words=[("w:How", "HOW?", .5, .13, .9, "sun")]),
    S("meadow", TCL("meadow", 1000, 0, -20, stage=MEET_ST), "I do not hurry. I paddle, and paddle, and I take my time.", who="tula", beat="solution", tag="Tula: I take my time",
      actors=[MEET_ST[2]], fx=[("face", 0.02, "tula", "happy"), FLAP("w:paddle,", 7), ("nod", "w:time.", "tula")], words=[("w:time.", "TAKE YOUR TIME", .5, .13, .75, "sun")]),
    S("meadow", (1120, 660, 1300), "And look! Tula nibbles the seagrass. Grown-up green sea turtles eat plants, like seagrass.", beat="fact", tag="fact: sea turtles eat seagrass",
      cam2=(1140, 670, 1240), actors=[T(780, 760)], props=[GRASS()],
      fx=[("lookat", 0.02, "tula", 4), NIB("w:nibbles", 0), NIB("w:seagrass.", 1), NIB("w:Grown-up", 2), NIB("w:green", 3), NIB("w:turtles", 4), NIB("w:plants,", 5),
          ("to", "w:nibbles", "#{p}tula-jaw", {"opacity": 1, "y": 7, "duration": .16, "yoyo": True, "repeat": 21}, "Tula chews"), SWIM("w:Grown-up", "tula", 150, 3.0)],
      words=[("w:seagrass.", "SEAGRASS", .32, .14, .8, "sun"), ("w:plants,", "PLANT EATER", .3, .3, .6, "pill")]),
    S("meadow", (1100, 660, 1400), "What does a grown-up green sea turtle eat? Seagrass, or pizza?", q=True, beat="fact", tag="question: seagrass or pizza", pause=3.2, cam2=(1110, 680, 1320),
      actors=[T(1050, 760)], props=[GRASS()], fx=[SHORT(), ("signs", "w:Seagrass,", ["SEAGRASS", "PIZZA"], 0, "wait:1.8")]),
    S("meadow", (1000, 680, 1500), "Tula made a path in the grass! Now we can all swim through.", who="pearl", beat="solution", tag="Pearl: a path in the grass",
      cam2=(1040, 680, 1440), actors=[T(1150, 760), Z(560, 620), PL(740, 800)], props=[GRASS()],
      fx=[SHORT(), ("face", 0.02, "pearl", "happy"), ("face", 0.02, "zip", "happy"), ("hop", "w:path", "pearl"), SWIM("w:Now", "tula", 130, 2.4), SWIM("w:Now", "zip", 200, 2.4), SWIM("w:Now", "pearl", 200, 2.4), FLAP("w:Now", 5)],
      words=[("w:path", "A PATH!", .36, .14, .85, "sun")]),
    S("fork", WIDE, "Soon they are back at the two ways. This time, nobody rushes. Tula stops, and thinks.", trans="iris", beat="solution", tag="back at the two ways: stop and think",
      cam2=(960, 560, 1840), fx=[FLAP(0.2, 5), ("lookat", "w:Tula", "tula", -8), ("face", "w:nobody", "zip", "happy"), BOB(0.3, "zip", 9), BOB(0.5, "pearl", 9)],
      words=[("w:stops,", "STOP AND THINK", .5, .5, .7, "sun")]),
    S("paper_blue", (960, 540, 1700), "Green sea turtles travel long distances, even across oceans.", beat="fact", tag="fact: long trips across the sea",
      cam2=(980, 540, 1600), actors=[], props=[prop("mp", A.sea_map, 960, 450, .8)],
      fx=[("to", 0.3, "#{p}mp-t", {"x": 440, "y": 60, "duration": 4.6, "ease": "sine.inOut"}, "the little turtle swims across the map"),
          ("to", "w:long", "#{p}mp-way", {"opacity": .4, "duration": .25, "yoyo": True, "repeat": 5}, "the way blinks")],
      words=[("w:long", "LONG TRIPS", .5, .11, .7, "sun"), ("w:oceans.", "ACROSS OCEANS", .5, .71, .55, "pill")]),
    S("fork", TCL("fork", 1000, 60, -20), "I have been this way before. The bright way goes to the Big Rock!", who="tula", beat="solution", tag="Tula: the bright way",
      hide=["zip", "pearl"], fx=[("face", 0.02, "tula", "happy"), ("nod", "w:before.", "tula"), ("lookat", "w:bright", "tula", -6), FLAP("w:Big", 5)],
      words=[("w:bright", "THE BRIGHT WAY!", .5, .13, .75, "sun")]),
    S("fork", (960, 600, 1840), "Which way goes to the Big Rock? The dark way, or the bright way?", q=True, beat="solution", tag="question: dark or bright", pause=3.2, cam2=(980, 610, 1760),
      fx=[FLAP(0.3, 15), ("signs", "w:dark", ["DARK", "BRIGHT"], 1, "wait:1.8")]),
    S("fork", FCL("fork", "zip", 720), "I have an idea! Let's not zoom. Let's swim slow and steady, right behind Tula!", who="zip", beat="solution", tag="Zip: I have an idea",
      hide=["tula", "pearl"], fx=[("face", 0.02, "zip", "happy"), ("hop", "w:idea!", "zip"), WIG("w:slow", "zip", 9, .2), ("hop", "w:Tula!", "zip")],
      words=[("w:idea!", "AN IDEA!", .5, .13, .9, "sun")]),
    S("fork", FCL("fork", "pearl", 720, 0), "Yes! All together!", who="pearl", beat="solution", tag="Pearl: all together",
      hide=["tula", "zip"], fx=[("face", 0.02, "pearl", "happy"), ("hop", "w:Yes!", "pearl"), ("hop", "w:together!", "pearl")], words=[("w:together!", "TOGETHER!", .5, .13, .9, "sun")]),
    S("reef", WIDE, "So the three friends swim through the coral garden, side by side. Nobody zooms, and nobody gets tired.", trans="iris", beat="solution", tag="the coral garden, side by side",
      cam2=(1040, 550, 1820), actors=[T(700, 740, .58), Z(240, 560), PL(190, 820)],
      fx=[("face", 0.02, "zip", "happy"), ("face", 0.02, "pearl", "happy"), FLAP(0.1, 17), SWIM(0.1, "tula", 280, 7.0, "none"), SWIM(0.1, "zip", 280, 7.0, "none"), SWIM(0.1, "pearl", 280, 7.0, "none"),
          BOB("w:coral", "zip", 7), BOB("w:side", "pearl", 7)],
      words=[("w:coral", "CORAL GARDEN", .5, .16, .75, "sun"), ("w:side", "SIDE BY SIDE", .5, .32, .6, "pill")]),
    S("reef", TCL("reef", 1200, 60, -40), "Let's count Tula's paddles! One, two, three!", q=True, beat="solution", tag="count the paddles", pause=1.0, cam2=TCL("reef", 1140, 60, -50), hide=["zip", "pearl"],
      fx=[("count", "w:One,", 3, CNT3, {"x": 520, "y": 250}),
          ("to", "w:One,", "#{p}tula-ff", {"rotation": 30, "svgOrigin": "95 -122", "duration": .14, "yoyo": True, "repeat": 1}, "paddle one"),
          ("to", "w:two,", "#{p}tula-ff", {"rotation": 30, "svgOrigin": "95 -122", "duration": .14, "yoyo": True, "repeat": 1}, "paddle two"),
          ("to", "w:three!", "#{p}tula-ff", {"rotation": 30, "svgOrigin": "95 -122", "duration": .14, "yoyo": True, "repeat": 1}, "paddle three")]),
    # ------------------------------------------------------------ the song moment: Tula SAYS the rhyme, then the tune on instruments
    S("reef", (900, 660, 1500), "Slow and steady, here we go. Paddle, paddle, nice and slow!", who="tula", beat="solution", tag="the paddle rhyme", cam2=(940, 660, 1440),
      fx=[("face", 0.02, "tula", "happy"), FLAP("w:Slow", 11), BOB("w:here", "zip", 5), BOB("w:Paddle,", "pearl", 5), ("nod", "w:slow!", "tula")],
      words=[("w:Slow", "SLOW AND STEADY", .5, .12, .62, "sun"), ("w:Paddle,", "PADDLE, PADDLE", .5, .25, .55, "pill")]),
    S("reef", (1000, 600, 1760), who="", sing=SING_PADDLE, beat="song", tag="song: slow and steady", cam2=(1100, 600, 1640),
      props=[prop("b1", A.bubbles, 250, 620, 1.0), prop("b2", A.bubbles, 1640, 640, 1.0)],
      fx=[("to", TB(0), "#{p}tula-ff", {"rotation": 24, "svgOrigin": "95 -122", "duration": 60 / 96, "yoyo": True, "repeat": 15, "ease": "sine.inOut"}, "Tula paddles to the beat"),
          SWIM(TB(0), "tula", 240, 9.6, "none"), SWIM(TB(0), "zip", 240, 9.6, "none"), SWIM(TB(0), "pearl", 240, 9.6, "none"),
          ("hop", TB(2), "zip"), ("hop", TB(4), "pearl"), ("nod", TB(6), "tula"), ("hop", TB(8), "zip"), ("hop", TB(10), "pearl"), ("nod", TB(12), "tula"),
          ("to", TB(0), "#{p}b1_w,#{p}b2_w", {"y": "-=260", "duration": 9.6, "ease": "none"}, "bubbles float up"),
          ("word", TB(0), "SLOW AND STEADY", {"x": 1000, "y": 250, "size": 84, "cls": "sun", "hold": 4.4})],
      words=[(TB(8), "PADDLE, PADDLE", .5, .16, .62, "pill")]),
    S("bigrock", WIDE, "And there it is. The Big Rock! Milo waves from the top.", trans="iris", beat="solution", tag="the Big Rock",
      cam2=(1000, 530, 1840), actors=ROCK_IN,
      fx=[FLAP(0.1, 9), SWIM(0.1, "tula", 300, 4.0), SWIM(0.1, "zip", 520, 4.0), SWIM(0.1, "pearl", 480, 4.0), ("hop", "w:Milo", "milo", 2)],
      words=[("w:Big", "THE BIG ROCK!", .3, .2, .8, "sun")]),
    S("bigrock", (1220, 660, 1200), "Tula, Zip and Pearl touch the gold star, all at the same time!", beat="solution", tag="they touch the gold star together",
      cam2=(1240, 650, 1120), hide=["milo"], actors=[MILO_R, T(940, 740), Z(1061, 560), PL(1010, 880)], props=[prop("sp", A.spark, A.STAR[0], A.STAR[1], .8, True)],
      fx=[SWIM(0.1, "tula", 130, 1.8), SWIM(0.1, "zip", 130, 1.8), SWIM(0.1, "pearl", 120, 1.8), ("show", "w:gold", "sp"),
          ("to", "w:gold", "#{p}sp", {"rotation": 90, "transformOrigin": "50% 50%", "duration": 2.6, "ease": "none"}, "the star shines"), ("hop", "w:same", "zip"), ("hop", "w:time!", "pearl")],
      words=[("w:all", "ALL TOGETHER!", .3, .12, .75, "sun")]),
    S("bigrock", MCLR, "Hooray! Everybody finished the race! A gold star for all three of you!", beat="solution", tag="Milo: everybody finished",
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:Hooray!", "milo", 2), ("hop", "w:race!", "milo"), ("hop", "w:three", "milo")],
      words=[("w:Hooray!", "HOORAY!", .5, .12, .9, "sun")]),
    S("bigrock", (1100, 640, 1340), "Did slow Tula finish the big race? Yes, or no?", q=True, beat="solution", tag="question: did Tula finish yes or no", pause=3.2, cam2=(1110, 650, 1280), hide=["milo"],
      fx=[FLAP(0.3, 15), ("face", 0.02, "tula", "happy"), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ WARM ENDING: evening at the Big Rock, thank-yous, next time
    S("bigrock_eve", WIDE, "The sun goes down, and the sea turns gold. The three friends rest beside the Big Rock.", trans="iris", beat="ending", tag="evening at the Big Rock",
      cam2=(940, 550, 1820), fx=[("face", 0.02, "tula", "happy"), ("face", 0.02, "zip", "happy"), ("face", 0.02, "pearl", "happy"), BOB(0.2, "zip", 9), BOB(0.5, "pearl", 9), FLAP("w:three", 5), ("hop", "w:sun", "milo")],
      words=[("w:gold.", "GOLDEN SEA", .42, .17, .75, "sun")]),
    S("bigrock_eve", FCL("bigrock_eve", "zip", 720), "Thank you, Tula! You showed us the way.", who="zip", beat="ending", tag="Zip: thank you",
      hide=["tula", "pearl"], fx=[("face", 0.02, "zip", "happy"), ("hop", "w:Thank", "zip")], words=[("w:Thank", "THANK YOU!", .5, .13, .85, "sun")]),
    S("bigrock_eve", TCL("bigrock_eve", 1000, 0, -20), "And you swam with me. A race is more fun with friends!", who="tula", beat="ending", tag="Tula: more fun with friends",
      hide=["zip", "pearl"], fx=[("face", 0.02, "tula", "happy"), ("nod", "w:me.", "tula"), FLAP("w:fun", 5)], words=[("w:fun", "MORE FUN WITH FRIENDS", .5, .13, .6, "pill")]),
    S("bigrock_eve", MCLR, "You do not have to be the fastest. Keep going, a little bit at a time, and you will get there.", beat="ending", tag="the lesson",
      fx=[("hop", "w:fastest.", "milo"), ("hop", "w:Keep", "milo"), ("hop", "w:there.", "milo")], words=[("w:Keep", "KEEP GOING!", .5, .12, .85, "sun")]),
    S("bigrock_eve", TCL("bigrock_eve", 1100, 0, -60), "Do you remember? What are a sea turtle's flippers shaped like? Paddles, or spoons?", q=True, beat="ending",
      tag="question: paddles or spoons", pause=3.2, hide=["zip", "pearl"], cam2=TCL("bigrock_eve", 1040, 0, -70),
      fx=[FLAP("w:flippers", 15), ("signs", "w:Paddles,", ["PADDLES", "SPOONS"], 0, "wait:1.8")]),
    S("bigrock_eve", (700, 640, 1500), "And what do grown-up green sea turtles eat? Seagrass, or sand?", q=True, beat="ending", tag="question: seagrass or sand", pause=3.2,
      cam2=(710, 660, 1420), fx=[("nod", "w:eat?", "tula"), BOB(0.3, "zip", 13), ("signs", "w:Seagrass,", ["SEAGRASS", "SAND"], 0, "wait:1.8")]),
    S("bigrock_eve", WIDE, "Slow and steady, here we go. Paddle, paddle, nice and slow!", beat="ending", tag="the closing rhyme", cam2=(980, 560, 1860),
      fx=[("hop", "w:Slow", "milo"), FLAP("w:here", 9), ("hop", "w:Paddle,", "milo"), BOB("w:nice", "zip", 3), BOB("w:nice", "pearl", 3)],
      words=[("w:Slow", "SLOW AND STEADY", .4, .13, .6, "sun"), ("w:Paddle,", "PADDLE, PADDLE", .4, .24, .5, "pill")]),
    S("bigrock_eve", (760, 680, 1300), who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(740, 680, 1220),
      props=[prop("b1", A.bubbles, 300, 620, 1.0), prop("b2", A.bubbles, 1120, 560, 1.0)],
      fx=[("hop", 1.0, "zip"), ("nod", 1.6, "tula"), ("hop", 2.2, "pearl"), FLAP(0.2, 9),
          ("to", 0.1, "#{p}b1_w,#{p}b2_w", {"y": "-=200", "duration": 4.6, "ease": "none"}, "bubbles float up")],
      words=[(TB(3), "HOORAY!", .5, .13, .9, "sun")]),
    S("bigrock_eve", MCLR, "Next time: A New House for Little Crab! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure",
      fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .5, .1, .62, "sun"), ("w:See", "SEE YOU SOON!", .5, .22, .5, "pill")]),
    *intro_shots(),      # and again as the last shots: the video ends on the logo with the whole cast
]

# thumbnail (thumb.py): the promise of the first shot: Tula, big, paddling at the back while the two fish zoom ahead; 2 words, none of the title's words, no watermark
THUMBS = {
    "za_ep12": {"place": "ocean", "cam": (960, 560, 1500),
                "actors": [("turtle", 760, 800, 1.15, False, ''), ("fish_zip", 1480, 330, .36, False, ''), ("fish_pearl", 1560, 520, .36, False, '')],
                "props": [(A.speed_lines, 1380, 280, .8), (A.speed_lines, 1450, 470, .8)],
                "words": [("LAST PLACE?", 700, 250, 180, "sun", -5)]},
}
