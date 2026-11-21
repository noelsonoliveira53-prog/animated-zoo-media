"""zc_ep05: "What Is Inside a Camel's Hump?" - cartoon fact lesson with Milo, Sandy the baby camel and her Mama (3D music-and-sync process: "beat").
Three parts, each cut whole into one Short: 1. what is inside (fat, not water), 2. why a hump is tall or floppy, 3. why baby Sandy has no hump.

FACTS, read at the source on Nov 18 2026 (this run):
 [SDZ] San Diego Zoo Wildlife Alliance, animals.sandiegozoo.org/animals/camel
   "They store fat, not water."   "The fat becomes an energy source for the camel."
   "The size of the hump can change, depending on the amount of food the camel eats."
   "When food is scarce, the camel's body uses the fat stored in the hump, causing the hump to lean over and droop."
   "The dromedary camel has one hump and the Bactrian camel has two."
   "The calf has no humps but small peaks of hide, each topped with a tassel of curly hair to indicate where the humps will form."
   "a newborn camel is able to walk beside the mother within half an hour."   "Mothers and their newborns hum to each other."
   "Camel calves nurse for 10 to 18 months"
   "A camel can go a week or more without water, and it can last for several months without food."
   "drink up to 32 gallons (145 liters) of water in one drinking session!"
   "These tough but flexible lips can break off and eat vegetation such as thorns or salty plants"
 [EB] Encyclopaedia Britannica, britannica.com/story/do-camels-store-water-in-their-humps
   "camels' humps actually store fatty tissue, not water, which is used as a source of nourishment when food is scarce."
   "The humps can deflate and droop if the camel has gone a particularly long time without food"   "they will sit upright again once the camel is able to refuel."
 [PBS] PBS Nature, pbs.org/wnet/nature/blog/camel-fact-sheet
   "They store fat in these humps, which later can be used as an energy source."   "The hump changes size depending on the amount of food that the animal eats."
   "The newborn is able to walk within half an hour after it is born."
 Not read today, so NOT said: how many pounds of fat a hump holds, how fast a camel drinks, where in the body the water goes, at what age a calf's hump forms.
 Milo's comparisons, not quotes: "like a backpack full of snacks", "like a little hat". "Food saved for later" says [EB]'s "a source of nourishment when food is scarce" in a child's words.
 The hums: SDZ says mothers and newborns hum; the tunes are made up, played by instruments in their own shots (no voice on notes).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_zc_ep05 as A5
from kit import Kit, S, prop, W

# the grown camel's points for kit.py (the calf's are there): the numbers of zc_ep01, which were checked in its stills
kit.PT.setdefault("camel", {"head": (345, -601), "eye": (352, -613), "nose": (452, -595), "mouth": (440, -549), "hump": (0, -501), "humptop": (0, -601), "back": (0, -441),
                            "body": (0, -323), "feet": (0, 0), "legs": (10, -131), "all": (60, -330), "top": (345, -700)})

EP = {"id": "zc_ep05", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "What Is Inside a Camel's Hump?", "thumb_text": "WATER OR FAT?", "series": "Animal Facts with Milo",
      "description": ("What is inside a camel's hump? Is it water, or is it fat? And why does baby camel Sandy have no hump at all? Milo the bluebird visits Sandy and her mama in the desert to find out! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn that a camel's hump stores fat, not water, that the fat is food saved for later, that a hump stands tall when a camel eats a lot "
                      "and leans over when food is hard to find, and that a baby camel is born with no hump, just a little tuft of curly hair.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (camel); Encyclopaedia Britannica (Do Camels Store Water in Their Humps?); PBS Nature (Camel Fact Sheet)."),
      "tags": ["camel", "camels for kids", "camel hump", "baby camel", "what is inside a camel's hump", "desert animals for kids", "animal facts for kids", "learning videos for toddlers",
               "preschool", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {      # the stages of zc_ep01 (looked at in its stills)
    "zoo": [("milo", "milo", 960, 940, 1.1, False, False)],
    "dunes": [("mama", "camel", 1390, 905, 1.0), ("calf", "calf", 700, 935, .56), ("milo", "milo", 330, 560, .8, False, True)],
    "trail": [("mama", "camel", 1180, 900, .95), ("calf", "calf", 590, 930, .54), ("milo", "milo", 300, 500, .75, False, True)],
    "oasis": [("mama", "camel", 1000, 880, .9), ("calf", "calf", 400, 915, .52), ("milo", "milo", 1640, 520, .72, True, True)],
    "wind": [("mama", "camel", 1370, 905, 1.0), ("calf", "calf", 690, 935, .56), ("milo", "milo", 320, 540, .78, False, True)],
    "night": [("mama", "camel", 1260, 905, .95), ("calf", "calf", 680, 935, .54), ("milo", "milo", 290, 892, .8, False, False)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920); PAPER = (960, 540, 1920)
TWO = (1223, 560, 1640); TWOP = (1235, 480, 2600)             # Mama and Sandy on the dunes, 16:9 and 9:16
DRK = (1180, 500, 1700)                                       # 9:16 at the oasis: Mama drinking, sky above for the count and the jug
HP = "0 -372"                                                 # the pivot of a camel's hump
FLOPPY = {"rotation": 30, "scaleY": .72, "scaleX": .94, "svgOrigin": HP, "duration": .01}
BUSH = lambda: prop("bush", lambda p: art._thorn(p, 0, 0), 1700, 905, 1.5)
CAM = [("cam", "camel", 880, 930, 1.05)]                      # one camel on a board
CAMP = (1000, 600, 2000)
BCAM = (960, 585, 1640); CL = (930, 430, 1060)                 # 16:9 on a board: the whole camel with its feet above the caption; a closer view of hump and head                                      # its 9:16 view
CARD = lambda: prop("card", lambda p: A5.qcard(p, 400, 250), 885, 419, 1.0)      # hides the hump until the answer
QCAM = (960, 470, 2300); QPCAM = (959, 306, 2310)             # the question views: the camel under the answer signs, feet above the caption
SP = (765, 635, 1200)                                        # 9:16 on Sandy alone, whole, feet above the caption
CP2 = (1080, 600, 2150)                                      # 9:16: the board camel with something beside it
TRP = (1150, 300, 2700)                                      # 9:16 on the trail: Sandy, Mama and the bush whole
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 900))
# The camels' hums: tunes for instruments only (bells and the soft band), in C at 96. Mama low (sol do mi), Sandy high (do' sol mi). Nobody's voice is on the notes.
HUM = {"bpm": 96, "chords": "C C", "style": "lullaby", "outro_bars": 0, "group": False, "level": 0.3}
HUM_MAMA = dict(HUM, lines=[{"text": "~ ~ ~", "notes": "G3:1 C4:1 E4:2"}])
HUM_SANDY = dict(HUM, level=0.27, lines=[{"text": "~ ~ ~", "notes": "C5:1 G4:1 E4:2"}])
HUM_ALL = dict(HUM, lines=[{"text": "~ ~ ~", "notes": "C5:1 G4:1 E4:2"}])
SCL = C("dunes", "calf", "head", 600, -150, -65); SCLP = (725, 636, 1300)      # Sandy's close-up while her tune plays: Mama's tail stays outside
STARS = ("to", 0, ".{p}star", {"opacity": .2, "duration": .5, "yoyo": True, "repeat": 9, "stagger": {"each": .05, "from": "random"}}, "the stars twinkle")

SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("dunes", C("dunes", "mama", "hump", 1000, 60, 10), "What is inside a camel's hump?", q=True, tag="hook: the hump", pcam=V("dunes", "mama", "hump", 1400, 120),
      words=[("w:inside", "?", .2, .3, 3.2, "sun", (.22, .42))], fx=[("hop", "w:hump?", "mama")], cam2=C("dunes", "mama", "hump", 860, 40, 0)),
    S("dunes", C("dunes", "calf", "back", 720, 30, -20), "And why does baby Sandy have no hump at all?", q=True, tag="hook: no hump", hide=["milo", "mama"], pcam=SP,
      words=[("w:no", "NO HUMP?", .27, .2, 1.2, "", (.5, .31), 1.0)], fx=[("lookat", "w:no", "calf", -12)]),
    S("dunes", say="I'm Milo. Let's find out together!", tag="hook: Milo", hide=["mama", "calf"], fx=[("hop", "w:find", "milo")], **MILO("dunes")),
    # ---------------------------------------------------------------- INTRO
    S("zoo", WIDE, "Welcome to The Animated Zoo, friends!", trans="iris", tag="gate wide", words=[("w:Animated", "HELLO!", .74, .6, 1.2, "pill")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, -40), "Today we fly to the hot, sandy desert.", tag="Milo close", words=[("w:desert.", "THE DESERT", .5, .16, 1.1, "sun")]),
    S("dunes", WIDE, "Here we are! Look who is waiting for us.", trans="iris", tag="dunes wide", cam2=(1000, 560, 1780),
      fx=[("fromto", 0, "#{p}milo_w", {"x": -300, "y": 200}, {"x": 330, "y": 560, "duration": 1.3, "ease": "power2.out"}, "Milo flies in")]),
    S("dunes", TWO, "This is Sandy, the baby camel. And this is her mama.", tag="two camels", hide=["milo"],
      words=[("w:Sandy,", "SANDY", .2, .26, 1.0, "pill"), ("w:mama.", "MAMA", .46, .12, 1.0, "pill")], fx=[("hop", "w:Sandy,", "calf"), ("nod", "w:mama.", "mama")]),
    # ---------------------------------------------------------------- PART 1: what is inside the hump? Fat, not water
    S("dunes", C("dunes", "mama", "hump", 1000, 60, 20), "Look at the big hump on Mama's back.", part=1, tag="the hump", hide=["calf"], pcam=V("dunes", "mama", "hump", 1500, 110),
      words=[("w:hump", "HUMP", .2, .2, 1.6, "sun", (.3, .33))], props=[prop("ar", lambda p: art.arrow(p, 1310, 170, 1380, 285), 0, 0, 1, True)], fx=[("show", "w:big", "ar")]),
    S("dunes", (1390, 480, 1700), "It is tall and round, like a little hill of sand.", part=1, tag="like a hill", hide=["calf", "milo"], pcam=WV("dunes", ["mama"]),
      words=[("w:hill", "LIKE A HILL", .32, .2, .9, "pill", (.5, .31), .8)], fx=[("nod", "w:tall", "mama")]),
    S("dunes", C("dunes", "mama", "body", 1500, 40, -80), "How many humps does Mama have? One!", part=1, q=True, tag="one hump", hide=["calf", "milo"], pcam=WV("dunes", ["mama"]),
      words=[("w:One!", "1", .2, .3, 2.6, "sun", (.2, .36), 1.6)], fx=[("hop", "w:One!", "mama")]),
    S("paper_blue", PAPER, "Some camels have one hump. Some camels have two.", part=1, tag="board: one or two", actors=[("a", "camel", 520, 900, .78), ("b", "bactrian", 1320, 900, .78)],
      pcam=(640, 583, 1300), pcam2=(1440, 583, 1300), words=[("w:one", "1 HUMP", .25, .2, 1.3, "sun", (.36, .3), 1.0), ("w:two.", "2 HUMPS", .7, .2, 1.3, "", (1.45, .3), 1.0)]),
    S("dunes", say="Can you make a hump with your arms? Up, and over!", part=1, q=True, tag="make a hump", hide=["mama", "calf"], fx=[("hop", "w:Up,", "milo", 2)],
      words=[("w:Up,", "UP AND OVER!", .76, .22, .8, "sun", (.5, .31), .8)], **MILO("dunes")),
    S("dunes", C("dunes", "calf", "head", 900, 60, -40), "Sandy looks up at the hump. What is in there?", part=1, q=True, hide=["milo"], tag="Sandy wonders", pcam=TWOP, pcam2=W(TWOP),
      words=[("w:What", "?", .7, .2, 2.4, "sun", (.3, .44), 1.6)], fx=[("lookat", 0.2, "calf", -16)]),
    S("paper_blue", (960, 520, 1500), "Is it full of water, like a big water bottle?", part=1, tag="board: water?", pcam=(960, 560, 1900),
      props=[prop("hc", A5.hump_closed, 700, 860, 1.2, p=(960, 1130, 1.0)), prop("jug", art.jug, 1340, 760, 2.6, True, p=(960, 640, 2.0))],
      words=[("w:water,", "WATER?", .7, .17, 1.2, "", (.5, .31))], fx=[("show", "w:water,", "jug")]),
    S("paper_blue", (960, 520, 1500), "Or is it full of fat?", part=1, tag="board: fat?", pcam=(960, 560, 1900),
      props=[prop("hc", A5.hump_closed, 700, 860, 1.2, p=(960, 1130, 1.0)), prop("jug", art.jug, 1130, 760, 2.0, p=(780, 640, 1.8)), prop("fb", A5.fat_blob, 1420, 640, 1.2, True, p=(1140, 540, 1.1))],
      words=[("w:fat?", "FAT?", .76, .15, 1.3, "sun", (.5, .33))], fx=[("show", "w:fat?", "fb")]),
    S("dunes", (1000, 520, 1920), "What do you think? Is it water, or is it fat?", part=1, q=True, tag="question 1", pause=4.4, hide=["milo"], pcam=TWOP, pcam2=W(TWOP), cam2=(1000, 520, 1920),
      fx=[("signs", "w:water,", ["WATER", "FAT"], 1, "wait:3.0"), ("hop", "wait:3.05", "calf")]),
    S("paper", (960, 520, 1500), "It is fat! A camel's hump is full of fat.", part=1, tag="board: inside the hump", pcam=(960, 430, 1700),
      props=[prop("cut", art.hump_cutaway, 960, 880, 1.45)], words=[("w:fat!", "FAT!", .2, .24, 1.9, "sun", (.5, .33), 1.3)],
      fx=[("fromto", 0, "#{p}cut_w", {"scale": .5, "transformOrigin": "50% 100%"}, {"scale": 1, "duration": .6, "ease": "back.out(1.6)"}, "the hump opens"),
          ("to", "w:full", ".{p}cut-fat", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .3, "yoyo": True, "repeat": 5, "stagger": .05}, "the fat wobbles")]),
    S("paper", (1000, 520, 1640), "Not water. Fat!", part=1, tag="board: not water", pcam=(1090, 560, 1700),
      props=[prop("cut", art.hump_cutaway, 760, 880, 1.2, p=(900, 1010, .7)), prop("drop", art.water_drop, 1420, 520, 1.7, True, p=(1300, 520, 1.3)), prop("x", art.cross, 1420, 540, 1.5, True, p=(1300, 535, 1.2))],
      words=[("w:Fat!", "NOT WATER!", .72, .78, 1.1, "pill", (.5, .33), .9)], fx=[("show", 0.1, "drop"), ("show", "w:water.", "x")]),
    S("dunes", say="Say it with me. Fat, not water!", part=1, q=True, tag="say it", hide=["mama", "calf"], fx=[("hop", "w:Fat,", "milo")],
      words=[("w:Fat,", "FAT, NOT WATER!", .74, .22, .72, "sun", (.5, .31), .72)], **MILO("dunes")),
    S("paper_pink", (960, 520, 1500), "The fat is food, saved for later.", part=1, tag="board: saved for later", pcam=(960, 560, 1900),
      props=[prop("hay", A5.hay, 520, 800, 1.3, p=(650, 780, 1.0)), prop("ar", lambda p: art.arrow(p, -130, 0, 130, 0), 880, 640, 1.0, True, p=(940, 640, .7)),
             prop("cut", art.hump_cutaway, 1300, 860, 1.1, p=(1260, 780, .6))],
      words=[("w:saved", "FOR LATER", .5, .15, 1.1, "sun", (.5, .31), 1.0)], fx=[("show", "w:food,", "ar")]),
    S("paper_pink", (960, 520, 1100), "It is like a backpack full of snacks.", part=1, tag="board: backpack", pcam=(960, 560, 1150),
      props=[prop("bp", A5.backpack, 900, 790, 1.1, True, p=(960, 860, 1.25))], fx=[("show", "w:backpack", "bp")], words=[("w:snacks.", "SNACKS!", .76, .32, 1.0, "sun", (.5, .33))]),
    S("paper", BCAM, "When a camel cannot find food, the fat feeds her.", part=1, tag="board: the fat feeds her", actors=CAM, pcam=CP2,
      props=[prop("bp", A5.backpack, 1410, 800, .8)], words=[("w:fat", "FOOD INSIDE", .24, .2, .8, "pill", (.3, .29), .7)],
      fx=[("to", "w:cannot", "#{p}bp_w", {"rotation": 8, "transformOrigin": "50% 100%", "duration": .2, "yoyo": True, "repeat": 5}, "the backpack wiggles"),
          ("to", "w:fat", "#{p}cam-hump", {"scaleY": 1.08, "svgOrigin": HP, "duration": .3, "yoyo": True, "repeat": 3}, "the hump bounces")]),
    S("paper", BCAM, "The fat gives the camel energy.", part=1, tag="board: energy", actors=CAM, pcam=CAMP,
      props=[prop("b1", art.bolt, 420, 640, 1.3, True, p=(1450, 520, .7)), prop("b2", art.bolt, 1480, 420, 1.3, True, p=(1450, 760, .7))],
      fx=[("show", "w:energy.", "b1"), ("show", "e:energy.", "b2"), ("hop", "w:energy.", "cam")], words=[("w:energy.", "ENERGY!", .2, .2, 1.0, "pill", (.36, .3), .8)]),
    S("trail", WIDE, "Energy to walk, and walk, and walk!", part=1, trans="iris", tag="trail walk", hide=["milo"], cam2=(1060, 560, 1740), pcam=TRP, pcam2=TRP,
      move={"mama": (880, 900, .95), "calf": (330, 930, .54)}, fx=[("walk", 0, "mama", 300, 3.4), ("walk", 0, "calf", 260, 3.4)], words=[("w:walk,", "WALK!", .5, .2, 1.3, "sun")]),
    S("oasis", (1130, 640, 1100), "And water? A camel drinks it. Slurp!", part=1, trans="iris", tag="Mama drinks", hide=["milo", "calf"], pcam=DRK, pcam2=W(DRK),
      words=[("w:Slurp!", "SLURP!", .78, .2, 1.3, "sun")], fx=[("drink", "w:camel", "mama", 3.0, 100)]),
    S("oasis", (1150, 640, 1000), "A thirsty camel can drink up to thirty-two gallons at one time!", part=1, tag="32 gallons", hide=["milo", "calf"], pcam=DRK, pcam2=W(DRK),
      props=[prop("jug", art.jug, 1575, 524, 1.3, True, p=(1500, 470, 2.0))],
      fx=[("to", 0, "#{p}mama-neck", {"rotation": 100, "svgOrigin": "190 -330", "duration": .01}), ("show", "w:thirty-two", "jug"), ("count", "w:thirty-two", 32, 1.5, {"x": 1300, "y": 112})],
      words=[("e:gallons", "GALLONS", .72, .4, 1.0, "pill", (.5, .31), .8)]),
    S("oasis", say="Glug, glug, glug! Can you drink like a camel?", part=1, q=True, tag="drink along", hide=["mama", "calf"], fx=[("hop", "w:Glug,", "milo", 2)],
      words=[("w:Glug,", "GLUG!", .26, .22, 1.2, "sun", (.5, .34))], **MILO("oasis")),
    S("paper_blue", PAPER, "Then a camel can go a week or more without water.", part=1, tag="board: a week", pcam=(960, 440, 2700), props=[prop("wk", art.week, 960, 640, 1.5, p=(960, 640, 1.3))],
      fx=[("fromto", "w:week", ".{p}wk-d", {"opacity": .25}, {"opacity": 1, "duration": .2, "stagger": .22}, "seven days light up"), ("count", "w:week", 7, 1.4, {"x": 960, "y": 300})],
      words=[("e:week", "DAYS", .5, .8, 1.2, "pill", (.5, .68))]),
    S("oasis", (640, 700, 1000), "Sandy has a drink, too. Let's count her sips. One, two, three!", part=1, q=True, hide=["mama", "milo"], tag="count the sips", pcam=(500, 742, 1100),
      fx=[("to", 0, "#{p}calf-neck", {"rotation": 96, "svgOrigin": "190 -330", "duration": .01}), ("to", "w:One,", "#{p}calf", {"y": "+=8", "duration": .15, "yoyo": True, "repeat": 1}, "sip"),
          ("to", "w:two,", "#{p}calf", {"y": "+=8", "duration": .15, "yoyo": True, "repeat": 1}, "sip"), ("to", "w:three!", "#{p}calf", {"y": "+=8", "duration": .15, "yoyo": True, "repeat": 1}, "sip")],
      words=[("w:One,", "1", .2, .22, 2.0, "sun", (.28, .34), 1.5), ("w:two,", "2", .36, .22, 2.0, "sun", (.5, .34), 1.5), ("w:three!", "3", .52, .22, 2.0, "sun", (.72, .34), 1.5)]),
    S("oasis", C("oasis", "mama", "hump", 1000, 60, 20), "So the water is for drinking. And the hump is full of fat!", part=1, tag="so: fat", hide=["calf", "milo"], pcam=V("oasis", "mama", "hump", 1400, 110),
      words=[("w:fat!", "FAT!", .2, .24, 1.7, "sun", (.3, .33))], fx=[("hop", "w:fat!", "mama")]),
    # ---------------------------------------------------------------- PART 2: tall or floppy? The hump changes with the food
    S("trail", WIDE, "Mama and Sandy walk down the rocky trail.", part=2, trans="iris", tag="trail wide", hide=["milo"], cam2=(1060, 560, 1740), pcam=TRP, pcam2=TRP,
      props=[BUSH()], move={"mama": (880, 900, .95), "calf": (330, 930, .54)}, fx=[("walk", 0, "mama", 300, 3.2), ("walk", 0, "calf", 260, 3.2)]),
    S("trail", (1000, 600, 1640), "Sandy is hungry. Mama is hungry, too.", part=2, tag="hungry", hide=["milo"], pcam=TRP, pcam2=TRP, props=[BUSH()],
      words=[("w:hungry.", "HUNGRY!", .5, .14, 1.1, "sun", (.5, .31))], fx=[("hop", "w:Sandy", "calf"), ("nod", "w:Mama", "mama")]),
    S("trail", (1730, 760, 680), "Look! A thorny bush. Those thorns are sharp.", part=2, tag="the bush", hide=["milo", "mama", "calf"], cam2=(1730, 760, 680), pcam=(1640, 600, 1150), props=[BUSH()],
      words=[("w:thorny", "THORNS", .26, .2, 1.3, "sun", (.5, .31))], fx=[("to", "w:sharp.", "#{p}bush_w", {"rotation": 4, "transformOrigin": "50% 100%", "duration": .15, "yoyo": True, "repeat": 5}, "the bush shakes")]),
    S("trail", (1300, 600, 1500), "But camels have tough lips. Mama can eat thorny plants!", part=2, tag="Mama eats", hide=["milo", "calf"], pcam=(1300, 500, 2000), pcam2=(1300, 500, 2000), props=[BUSH()],
      words=[("w:tough", "TOUGH LIPS", .27, .14, 1.0, "pill", (.5, .31), .9)], fx=[("drink", "w:Mama", "mama", 2.4, 58), ("chew", "w:eat", "mama", 2.0)]),
    S("trail", (1600, 640, 900), "Munch, munch, munch! Can you munch like Mama?", part=2, q=True, tag="munch", hide=["milo", "calf"], pcam=(1300, 500, 2000), pcam2=(1300, 500, 2000), props=[BUSH()],
      words=[("w:Munch,", "MUNCH!", .24, .2, 1.3, "sun", (.5, .31))], fx=[("to", 0, "#{p}mama-neck", {"rotation": 58, "svgOrigin": "190 -330", "duration": .01}), ("chew", 0.1, "mama", 4.2)]),
    S("paper", BCAM, "A camel's hump can change its size.", part=2, tag="board: it changes", actors=CAM, pcam=CAMP,
      words=[("w:change", "IT CHANGES!", .22, .2, .9, "pill", (.37, .285), .6)],
      fx=[("to", "w:change", "#{p}cam-hump", {"scaleY": .7, "scaleX": .92, "svgOrigin": HP, "duration": .45, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "the hump gets smaller and bigger")]),
    S("paper", BCAM, "When a camel eats a lot, the hump is big and tall.", part=2, tag="board: tall hump", actors=CAM, pcam=CAMP,
      words=[("w:tall.", "TALL", .2, .26, 1.4, "sun", (.3, .297), 1.0)], props=[prop("ar", lambda p: art.arrow(p, 620, 560, 620, 330), 0, 0, 1, True), prop("hay", A5.hay, 1470, 900, .8, p=(1400, 930, .6))],
      fx=[("fromto", "w:eats", "#{p}cam-hump", {"scaleY": .7, "scaleX": .94, "rotation": 22, "svgOrigin": HP}, {"scaleY": 1, "scaleX": 1, "rotation": 0, "duration": 1.6, "ease": "back.out(2)"}, "the hump stands up"),
          ("to", 0, "#{p}cam-hump", {"scaleY": .7, "scaleX": .94, "rotation": 22, "svgOrigin": HP, "duration": .01}), ("show", "w:tall.", "ar")]),
    S("paper_pink", (960, 520, 1500), "It is full of fat. A full backpack!", part=2, tag="board: full backpack", pcam=(960, 560, 1900),
      props=[prop("cut", art.hump_cutaway, 620, 880, 1.2, p=(960, 660, .7)), prop("bp", A5.backpack, 1320, 880, 1.5, True, p=(960, 1000, .6))],
      words=[("w:full", "FULL", .5, .15, 1.4, "sun", (.5, .33), 1.2)], fx=[("show", "w:backpack!", "bp")]),
    S("wind", WIDE, "But sometimes, there is not much food in the desert.", part=2, trans="iris", tag="windy wide", hide=["milo"], cam2=(980, 540, 1920), pcam=(1205, 380, 2400), pcam2=W((1205, 380, 2400)),
      props=[prop("puff", art.sand_puffs, 960, 520, 1.0)], words=[("w:not", "NO FOOD", .5, .2, 1.2, "", (.5, .31))],
      fx=[("fromto", 0, "#{p}gust", {"x": -260}, {"x": 320, "duration": 4.0, "ease": "none"}, ""), ("fromto", 0, "#{p}puff_w", {"x": 700}, {"x": 1300, "duration": 4.0, "ease": "none"}, ""), ("snd", 0.1, "whoosh")]),
    S("paper", BCAM, "Then the camel's body uses the fat in the hump.", part=2, tag="board: using the fat", actors=CAM, pcam=CP2,
      props=[prop("bp", A5.backpack, 1410, 800, .8)], words=[("w:uses", "FAT USED", .22, .2, .9, "pill", (.3, .285), .7)],
      fx=[("to", "w:uses", "#{p}bp-snacks", {"scale": .2, "y": 60, "opacity": 0, "transformOrigin": "50% 100%", "duration": 1.4}, "the backpack empties"), ("droop", "w:uses", "cam", 10)]),
    S("paper", BCAM, "The hump gets smaller, and smaller.", part=2, tag="board: smaller", actors=CAM, pcam=CAMP,
      words=[("w:smaller,", "SMALLER", .26, .2, 1.0, "", (.3, .297), .9)],
      fx=[("to", 0, "#{p}cam-hump", {"rotation": 10, "scaleY": .9, "scaleX": .97, "svgOrigin": HP, "duration": .01}),
          ("to", "w:smaller,", "#{p}cam-hump", {"rotation": 16, "scaleY": .8, "scaleX": .95, "duration": .7}, "the hump gets smaller"), ("to", "w:smaller.", "#{p}cam-hump", {"rotation": 20, "scaleY": .74, "scaleX": .94, "duration": .7}, "and smaller")]),
    S("paper", CL, "And it leans over. Flop!", part=2, tag="board: flop", actors=CAM, pcam=CAMP,
      words=[("w:Flop!", "FLOP!", .17, .2, 1.3, "sun", (.3, .31), 1.0)],
      fx=[("to", 0, "#{p}cam-hump", {"rotation": 20, "scaleY": .74, "scaleX": .94, "svgOrigin": HP, "duration": .01}), ("droop", "w:leans", "cam", 30), ("snd", "w:Flop!", "boing")]),
    S("wind", say="Can you flop over like a hump? Flop!", part=2, q=True, tag="flop along", hide=["mama", "calf"],
      fx=[("to", "w:Flop!", "#{p}milo", {"rotation": 35, "svgOrigin": "0 0", "duration": .35, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "Milo flops over")],
      words=[("w:Flop!", "FLOP!", .76, .22, 1.2, "sun", (.5, .31))], **MILO("wind")),
    S("paper_blue", PAPER, "A tall hump is full of fat. A floppy hump has used it up.", part=2, tag="board: full or used", actors=[("a", "camel", 520, 900, .78), ("b", "camel", 1300, 900, .78)],
      pcam=(640, 583, 1300), pcam2=(1390, 583, 1300),
      words=[("w:full", "FULL", .25, .2, 1.3, "sun", (.36, .3), 1.1), ("w:used", "USED UP", .68, .2, 1.2, "", (1.46, .3), 1.0)], fx=[("to", 0, "#{p}b-hump", FLOPPY)]),
    S("paper", QCAM, "This camel found no food for a long time. Is her hump tall, or floppy?", part=2, q=True, tag="question 2", pause=4.4, actors=CAM, pcam=QPCAM, pcam2=QPCAM, cam2=QCAM,
      props=[CARD()], fx=[("to", 0, "#{p}cam-hump", FLOPPY), ("signs", "w:tall,", ["TALL", "FLOPPY"], 1, "wait:3.0"), ("hide", "wait:3.0", "card"),
                          ("to", "w:no", "#{p}card_w", {"rotation": 5, "transformOrigin": "50% 50%", "duration": .3, "yoyo": True, "repeat": 3}, "the card wiggles")]),
    S("paper", CL, "Floppy! She used the fat in her hump.", part=2, tag="floppy!", actors=CAM, pcam=CAMP,
      words=[("w:Floppy!", "FLOPPY!", .2, .2, 1.0, "sun", (.42, .3), .72)], fx=[("to", 0, "#{p}cam-hump", FLOPPY), ("nod", "w:used", "cam")]),
    S("paper", BCAM, "What will make her hump stand up again?", part=2, q=True, tag="what next", pause=1.0, actors=CAM, pcam=CAMP,
      words=[("w:What", "?", .22, .22, 2.4, "sun", (.3, .31), 1.4)], fx=[("to", 0, "#{p}cam-hump", FLOPPY), ("to", "w:stand", "#{p}cam-hump", {"rotation": 24, "duration": .3, "yoyo": True, "repeat": 3}, "the hump wobbles")]),
    S("paper", (1040, 600, 1640), "Food! The camel eats, and eats, and eats.", part=2, tag="board: she eats", actors=CAM, pcam=CP2,
      props=[prop("hay", A5.hay, 1420, 930, .9)], words=[("w:Food!", "FOOD!", .24, .2, 1.4, "sun", (.34, .3), .9)],
      fx=[("to", 0, "#{p}cam-hump", FLOPPY), ("drink", "w:camel", "cam", 3.2, 52), ("chew", "w:eats,", "cam", 2.6)]),
    S("paper", CL, "And the hump sits up tall again. Pop!", part=2, tag="board: pop", actors=CAM, pcam=CAMP,
      words=[("w:Pop!", "TALL AGAIN!", .26, .22, .8, "sun", (.34, .3), .8)], fx=[("to", 0, "#{p}cam-hump", FLOPPY), ("perk", "w:sits", "cam"), ("snd", "w:Pop!", "boing")]),
    S("trail", C("trail", "mama", "hump", 1000, 60, 20), "Mama had a big lunch today. Is her hump tall? Yes, it is!", part=2, q=True, tag="Mama's hump", trans="iris", hide=["milo", "calf"], pcam=(1340, 470, 1560), pcam2=W((1340, 470, 1560)),
      words=[("w:Yes,", "TALL!", .2, .26, 1.6, "sun", (.3, .33), 1.2)], fx=[("hop", "w:Yes,", "mama")]),
    S("paper_blue", (960, 540, 1600), "With a full hump, a camel can last for several months without food!", part=2, tag="board: months", pcam=(960, 560, 1900),
      props=[prop("cut", art.hump_cutaway, 520, 800, .8, p=(960, 640, .6)), prop("mo", A5.months, 1220, 600, .72, p=(960, 860, .6))],
      fx=[("fromto", "w:several", ".{p}mo-m", {"opacity": .2}, {"opacity": 1, "duration": .25, "stagger": .35}, "the months light up")],
      words=[("w:months", "MONTHS!", .66, .2, 1.1, "sun", (.5, .3))]),
    S("trail", say="Months and months! Thank you, hump!", part=2, tag="thank you, hump", hide=["mama", "calf"], fx=[("hop", "w:Thank", "milo", 2)],
      words=[("w:Thank", "THANK YOU!", .82, .2, .8, "sun", (.5, .31), .9)], **MILO("trail")),
    # ---------------------------------------------------------------- PART 3: why does baby Sandy have no hump?
    S("dunes", TWO, "Now look at baby Sandy. Where is her hump?", part=3, q=True, trans="iris", tag="where is it", hide=["milo"], pcam=TWOP, pcam2=W(TWOP),
      words=[("w:Where", "?", .2, .24, 2.6, "sun", (.3, .44), 1.6)], fx=[("hop", "w:Sandy.", "calf")]),
    S("dunes", C("dunes", "calf", "back", 720, 30, -20), "No hump! Just a little bump.", part=3, tag="no hump", hide=["milo", "mama"], pcam=SP,
      words=[("w:No", "NO HUMP!", .27, .2, 1.2, "", (.5, .31), 1.0)], fx=[("lookat", "w:Just", "calf", -10)]),
    S("dunes", C("dunes", "calf", "back", 700, 20, -30), "And on top, a tuft of curly hair.", part=3, tag="the tuft", hide=["milo", "mama"], pcam=SP,
      words=[("w:tuft", "CURLY TUFT", .3, .76, 1.0, "pill", (.5, .31))], props=[prop("ar", lambda p: art.arrow(p, 620, 520, 760, 640), 0, 0, 1, True)], fx=[("show", "w:top,", "ar")]),
    S("paper_pink", (960, 520, 1400), "Curly, curly, curly! Like a little hat.", part=3, tag="board: curly", pcam=(960, 440, 1900), props=[prop("tb", A5.tuft_big, 960, 830, 1.0, p=(960, 900, .9))],
      words=[("w:Curly,", "CURLY!", .76, .2, 1.2, "sun", (.5, .33))],
      fx=[("to", "w:Curly,", ".{p}tb-c", {"rotation": 14, "transformOrigin": "50% 100%", "duration": .22, "yoyo": True, "repeat": 9, "stagger": .08, "ease": "sine.inOut"}, "the curls wiggle")]),
    S("dunes", say="Can you draw a curl in the air? Round and round!", part=3, q=True, tag="draw a curl", hide=["mama", "calf"], fx=[("hop", "w:Round", "milo", 2)],
      words=[("w:Round", "ROUND!", .76, .22, 1.1, "sun", (.5, .31))], **MILO("dunes")),
    S("dunes", TWO, "Mama has a big hump. Sandy has a little tuft.", part=3, tag="hump and tuft", hide=["milo"], pcam=TWOP, pcam2=W(TWOP),
      words=[("w:big", "BIG HUMP", .42, .14, 1.0, "", (.7, .3), .8), ("w:little", "LITTLE TUFT", .16, .4, .8, "sun", (.32, .46), .8)]),
    S("paper_blue", PAPER, "A baby camel is born with no hump.", part=3, tag="board: newborn", actors=[("calf", "calf", 760, 900, .8)], pcam=(860, 560, 1500),
      words=[("w:no", "NO HUMP", .72, .2, 1.2, "sun", (.5, .3), 1.0)],
      fx=[("fromto", 0, "#{p}calf", {"y": 60, "scaleY": .8, "svgOrigin": "0 0"}, {"y": 0, "scaleY": 1, "duration": 1.0, "ease": "back.out(2)"}, "the newborn stands up")]),
    S("paper_blue", (1180, 480, 1400), "In just half an hour, Sandy could walk beside her mama!", part=3, tag="board: the clock", actors=[("calf", "calf", 720, 860, .8)], pcam=(940, 500, 2000), pcam2=(940, 500, 2000),
      props=[prop("clock", art.clock, 1420, 400, 1.05, p=(1270, 600, .6))], words=[("w:half", "30 MINUTES", .7, .79, .95, "pill", (.5, .31))],
      fx=[("to", "w:half", "#{p}clock-min", {"rotation": 180, "svgOrigin": "0 0", "duration": 1.6, "ease": "power1.inOut"}, "the clock hand goes round half way")]),
    S("dunes", WIDE, "Step, step, step! Off they go.", part=3, tag="they walk", hide=["milo"], pcam=(1290, 480, 2700), pcam2=(1290, 480, 2700), cam2=(1080, 560, 1840),
      fx=[("walk", 0.1, "mama", 110, 3.0), ("walk", 0.1, "calf", 110, 3.0)], words=[("w:Step,", "STEP!", .5, .2, 1.2, "sun", (.5, .31))]),
    S("dunes", TWO, "Sandy stays close to her mama.", part=3, tag="close to Mama", hide=["milo"], pcam=TWOP, pcam2=W(TWOP), fx=[("hop", "w:close", "calf")],
      words=[("w:close", "CLOSE!", .42, .15, 1.0, "sun", (.5, .33))]),
    S("paper_pink", (960, 520, 1500), "A baby camel drinks her mama's milk.", part=3, tag="board: milk", actors=[("calf", "calf", 640, 920, .8)], pcam=(880, 480, 1800),
      props=[prop("mk", A5.milk_drop, 1400, 600, 1.5, True, p=(1220, 560, 1.0))], words=[("w:milk.", "MILK", .8, .17, 1.3, "", (.5, .31))],
      fx=[("show", "w:milk.", "mk"), ("chew", "w:drinks", "calf", 1.6)]),
    S("paper_pink", (940, 540, 1400), "Sip, sip, sip! Can you sip like Sandy?", part=3, q=True, tag="sip along", actors=[("calf", "calf", 640, 920, .8)], pcam=(880, 480, 1800),
      props=[prop("mk", A5.milk_drop, 1400, 600, 1.5, p=(1220, 560, 1.0))], words=[("w:Sip,", "SIP!", .2, .2, 1.3, "sun", (.5, .31))], fx=[("chew", "w:Sip,", "calf", 2.4)]),
    S("dunes", TWO, "Mama and Sandy hum to each other. Listen!", part=3, tag="they hum", hide=["milo"], pcam=TWOP, pcam2=W(TWOP),
      fx=[("lookat", "w:hum", "mama", 14), ("lookat", "w:hum", "calf", -14)], words=[("w:Listen!", "LISTEN!", .42, .2, 1.0, "pill", (.5, .33))]),
    S("dunes", C("dunes", "mama", "head", 900, -70, 10), part=3, tag="Mama's tune", who="", sing=HUM_MAMA, pcam=V("dunes", "mama", "head", 1100, -60, 40),
      props=[prop("n1", lambda p: art.note(p), 1900, 300, 1.1, True, p=(1790, 180, 1.0)), prop("n2", lambda p: art.note(p, "#58b9e8"), 1990, 330, .9, True, p=(1890, 250, .9))],
      fx=[("lookat", 0, "mama", 14), ("show", 0.15, "n1", None, False), ("show", 1.4, "n2", None, False), ("to", 0.15, "#{p}n1_w", {"y": "-=60", "x": "+=30", "rotation": 10, "duration": 2.3, "ease": "sine.out"}),
          ("to", 1.4, "#{p}n2_w", {"y": "-=50", "x": "+=20", "rotation": -12, "duration": 1.2, "ease": "sine.out"})]),
    S("dunes", SCL, part=3, tag="Sandy's tune", who="", sing=HUM_SANDY, hide=["milo"], cam2=SCL, pcam=SCLP, pcam2=SCLP,
      props=[prop("n1", lambda p: art.note(p, "#58b9e8"), 770, 450, .7, True), prop("n2", lambda p: art.note(p, "#ff9ab8"), 945, 430, .55, True)],
      fx=[("lookat", 0, "calf", -14), ("show", 0.15, "n1", None, False), ("show", 1.4, "n2", None, False), ("to", 0.15, "#{p}n1_w", {"y": "-=25", "x": "-=10", "rotation": -10, "duration": 2.3, "ease": "sine.out"}),
          ("to", 1.4, "#{p}n2_w", {"y": "-=20", "x": "+=8", "rotation": 10, "duration": 1.2, "ease": "sine.out"})]),
    S("dunes", C("dunes", "milo", "body", 820, 60, -20), "Can you hum like a camel? Your turn!", part=3, q=True, hide=["mama", "calf"], tag="hum along", pcam=V("dunes", "milo", "body", 860, -60, 70), fx=[("hop", "w:Your", "milo")]),
    S("dunes", TWO, part=3, tag="everybody's tune", who="", sing=HUM_ALL, pause=0.3, hide=["milo"], pcam=TWOP, pcam2=W(TWOP), words=[(0.1, "YOUR TURN!", .36, .2, .8, "pill", (.4, .3))],
      props=[prop("n1", lambda p: art.note(p), 1620, 340, 1.3, True, p=(1640, 250, 2.0)), prop("n2", lambda p: art.note(p, "#58b9e8"), 1030, 480, 1.0, True, p=(1040, 420, 1.7)),
             prop("n3", lambda p: art.note(p, "#59c36a"), 1180, 420, .9, True, p=(1230, 250, 1.6))],
      fx=[("lookat", 0, "mama", 14), ("lookat", 0, "calf", -14), ("show", 0.15, "n1", None, False), ("show", 0.75, "n2", None, False), ("show", 1.4, "n3", None, False),
          ("to", 0.15, "#{p}n1_w,#{p}n2_w,#{p}n3_w", {"y": "-=50", "duration": 2.4, "ease": "sine.out"})]),
    S("dunes", say="Well done! You hum like a camel.", part=3, tag="well done", hide=["mama", "calf"], fx=[("hop", "w:Well", "milo", 2)],
      words=[("w:Well", "WELL DONE!", .76, .22, .9, "sun", (.5, .33), .9)], **MILO("dunes")),
    S("dunes", (1000, 520, 1920), "Was Sandy born with a hump? Yes, or no?", part=3, q=True, tag="question 3", pause=4.4, hide=["milo"], pcam=TWOP, pcam2=W(TWOP), cam2=(1000, 520, 1920),
      fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:3.0"), ("hop", "wait:3.05", "calf")]),
    S("dunes", C("dunes", "calf", "back", 700, 20, -30), "No! Just a little tuft of curly hair.", part=3, tag="no!", hide=["milo", "mama"], pcam=SP,
      words=[("w:No!", "NO!", .26, .22, 1.6, "sun", (.5, .32), 1.3)], props=[prop("ar", lambda p: art.arrow(p, 620, 520, 760, 640), 0, 0, 1, True)], fx=[("show", "w:tuft", "ar")]),
    S("paper", (900, 520, 1400), "The tuft shows where her hump will grow.", part=3, tag="board: right here", actors=[("calf", "calf", 800, 930, .85)], pcam=(900, 500, 1800),
      props=[prop("gh", A5.ghost_hump, 800, 904, .85, True)], words=[("w:where", "RIGHT HERE!", .28, .2, .8, "pill", (.5, .3), .9)], fx=[("show", "w:where", "gh")]),
    S("paper_pink", BCAM, "As Sandy grows up, her hump will grow, too.", part=3, tag="board: the hump grows", actors=[("c", "camel", 900, 930, 1.0)], pcam=(1020, 520, 1700),
      fx=[("grow", 0.2, "c", .8)], words=[("w:grow,", "GROW!", .24, .2, 1.3, "sun", (.36, .3), 1.0)]),
    S("paper_pink", (950, 430, 1060), "Bigger, and bigger, and bigger!", part=3, tag="board: bigger", actors=[("c", "camel", 900, 930, 1.0)], pcam=(1020, 520, 1700),
      words=[("w:bigger!", "BIGGER!", .24, .26, 1.3, "sun", (.36, .31), 1.0)],
      fx=[("to", 0, "#{p}c-hump", {"scaleY": .8, "scaleX": .8, "svgOrigin": HP, "duration": .01}), ("to", "w:Bigger,", "#{p}c-hump", {"scaleY": 1, "scaleX": 1, "duration": 2.4, "ease": "power1.inOut"}, "the hump grows tall")]),
    S("dunes", C("dunes", "calf", "head", 860, 0, 20), "One day, Sandy will have a hump just like Mama's.", part=3, tag="one day", hide=["milo", "mama"], pcam=SP, fx=[("hop", "w:hump", "calf", 2)],
      words=[("w:just", "ONE DAY!", .24, .2, 1.0, "pill", (.5, .31))]),
    S("dunes", TWO, "And it will be full of fat!", part=3, tag="full of fat", hide=["milo"], pcam=TWOP, pcam2=W(TWOP), words=[("w:fat!", "FAT!", .42, .2, 1.4, "sun", (.5, .33))],
      fx=[("hop", "w:fat!", "calf"), ("nod", "w:fat!", "mama")]),
    # ---------------------------------------------------------------- QUIZ + GOODBYE
    S("night", WIDE, "The sun goes down. Time to remember what we learned!", part=4, trans="iris", tag="night wide", cam2=(1000, 560, 1760), fx=[STARS], words=[("w:remember", "QUIZ TIME!", .5, .2, 1.3, "sun")]),
    S("night", (960, 480, 2100), "What is inside a camel's hump? Water, or fat?", part=4, q=True, tag="quiz 1", pause=4.2, cam2=(960, 480, 2100), fx=[("signs", "w:Water,", ["WATER", "FAT"], 1, "wait:2.8")]),
    S("paper", (960, 520, 1500), "Fat! It is food, saved for later.", part=4, tag="board: fat again", props=[prop("cut", art.hump_cutaway, 700, 880, 1.25), prop("bp", A5.backpack, 1400, 860, 1.4, True)],
      words=[("w:Fat!", "FAT!", .5, .12, 1.6, "sun")], fx=[("show", "w:food,", "bp")]),
    S("paper", QCAM, "When a camel finds no food, does her hump stand tall, or flop over?", part=4, q=True, tag="quiz 2", pause=4.2, actors=CAM, cam2=QCAM,
      props=[CARD()], fx=[("to", 0, "#{p}cam-hump", FLOPPY), ("signs", "w:tall,", ["TALL", "FLOP"], 1, "wait:2.8"), ("hide", "wait:2.8", "card"),
                          ("to", "w:no", "#{p}card_w", {"rotation": 5, "transformOrigin": "50% 50%", "duration": .3, "yoyo": True, "repeat": 3}, "the card wiggles")]),
    S("paper", CL, "It flops over. Flop!", part=4, tag="board: flop again", actors=CAM, words=[("w:Flop!", "FLOP!", .17, .2, 1.3, "sun")],
      fx=[("to", 0, "#{p}cam-hump", {"rotation": 10, "scaleY": .9, "svgOrigin": HP, "duration": .01}), ("droop", "w:flops", "cam", 30), ("snd", "w:Flop!", "boing")]),
    S("night", (960, 480, 2100), "Was baby Sandy born with a hump? Yes, or no?", part=4, q=True, tag="quiz 3", pause=4.2, cam2=(960, 480, 2100), fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.8")]),
    S("night", C("night", "calf", "back", 760, 30, -30), "No! Just a little curly tuft.", part=4, tag="the tuft again", hide=["milo", "mama"], words=[("w:No!", "NO!", .22, .22, 1.6, "sun")],
      props=[prop("ar", lambda p: art.arrow(p, 540, 520, 660, 630), 0, 0, 1, True)], fx=[("show", "w:curly", "ar")]),
    S("night", C("night", "milo", "body", 820, 20, -20), "Good night, Sandy. Good night, Mama.", part=4, tag="good night", hide=["mama", "calf"], fx=[("hop", "w:Mama.", "milo")]),
    S("night", WIDE, "Thank you for learning with me, friends. See you at the zoo!", part=4, tag="goodbye", cam2=(960, 520, 2050), words=[("w:See", "SEE YOU AT THE ZOO!", .5, .2, 1.05, "pill")],
      fx=[STARS, ("hop", "w:zoo!", "milo", 2)]),
]


def T(src, **kw):
    """A copy of a shot of the lesson (by its tag), with changes, for a Short's first shot."""
    d = dict(next(x for x in SHOTS if x["tag"] == src)); d.update(kw); return d


SHORTS = [
    {"id": "zc_ep05_short1", "title": "Is a Camel's Hump Full of Water?", "band": ("IS IT FULL", "OF WATER?"), "thumb_text": "ALL FAT!", "part": 1,
     "extra_first": [T("hook: the hump", part=1)]},
    {"id": "zc_ep05_short2", "title": "Why Does a Camel's Hump Flop Over?", "band": ("WHY DOES IT", "FLOP?"), "thumb_text": "TALL OR FLOPPY?", "part": 2,
     "extra_first": [S("paper", CL, "Why does a camel's hump flop over?", part=2, q=True, tag="hook: the flop", actors=CAM, pcam=CAMP,
                       words=[("w:Why", "?", .17, .22, 2.2, "sun", (.3, .31), 1.5)], fx=[("droop", "w:flop", "cam", 30), ("snd", "w:flop", "boing")])]},
    {"id": "zc_ep05_short3", "title": "Was a Baby Camel Born with a Hump?", "band": ("BORN WITH", "A HUMP?"), "thumb_text": "CURLY TUFT!", "part": 3,
     "extra_first": [T("hook: no hump", part=3, say="Why does baby Sandy have no hump at all?")]},
]

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
_FLOP = 'gsap.set("#P-hump",{rotation:30,scaleY:.72,scaleX:.94,svgOrigin:"0 -372"});'
THUMBS = {
    "zc_ep05": {"place": "dunes", "cam": (960, 540, 1920),
                "actors": [("camel", 1240, 1060, 1.15)],
                "props": [(lambda p: A5.qcard(p, 250, 170), 1250, 470, 1.0), (lambda p: art.water_drop(p), 250, 640, 1.5), (A5.fat_blob, 640, 650, 1.5)],
                "words": [("WATER OR FAT?", 560, 190, 150, "sun")]},
    "zc_ep05_short1": {"place": "paper", "cam": (960, 500, 1500),
                       "props": [(art.hump_cutaway, 960, 900, 1.5)],
                       "words": [("ALL FAT!", 540, 440, 215, "sun")]},
    "zc_ep05_short2": {"place": "paper_blue", "cam": (960, 480, 1900),
                       "actors": [("camel", 880, 930, 1.05, False, _FLOP)],
                       "words": [("TALL OR", 540, 440, 170, ""), ("FLOPPY?", 540, 620, 200, "sun")]},
    "zc_ep05_short3": {"place": "dunes", "cam": (760, 560, 1300),
                       "actors": [("calf", 700, 935, .8, False, 'gsap.set("#P-neck",{rotation:-10,svgOrigin:"190 -330"});')],
                       "props": [(lambda p: art.arrow(p, 560, 300, 680, 470), 0, 0, 1)],
                       "words": [("CURLY", 470, 290, 190, ""), ("TUFT!", 470, 460, 220, "sun")]},
}
