"""zc_ep13: "How Do Polar Bears Stay Warm?" - Arctic week, fact lesson 1 (2D, docs/CARTOON_RUN.md "A fact lesson and its three Shorts",
"VIRAL PACKAGING", "MAIN INTRO"), a cartoon fact lesson with the 3D music-and-sync process ("beat").
Cold open on Poppy the polar bear cub happy in the falling snow next to a little thermometer that drops: "How does a polar bear stay warm?".
Milo says his name after the hook; the main intro right after the hook and again as the last shots. Three parts ("Poppy's three warm secrets"),
each cut whole into one Short, each opening on its own question with answer signs and thinking time:
1. the thick layer of fat under the skin (up to four inches, keeps it warm in the icy water and helps it float),
2. the two layers of fur (a soft, thick undercoat and long guard hairs on top; the long hairs are like a raincoat, water rolls right off;
   fur covers almost all of its body),
3. furry feet and a cozy den (fur on the bottoms of the feet keeps them warm and stops slipping; a snow den can be much warmer inside;
   cubs stay warm with their mother; polar bears are so warm they can get too hot and cool off in the chilly water).
Quiz with the three secrets, recap, the closing names the next Arctic lesson ("Is a Polar Bear Really White?": clear hollow hairs and black skin
are left to that lesson, so they are NOT said here). zc_ep12 (live) already teaches the small ears and the short tail: not repeated.

FACTS, read at the source on Nov 21 2026, about 1:35-1:45 PM ET (pages read by the session's page reader, which quoted the sentences verbatim):
 [SDZ] San Diego Zoo Wildlife Alliance, Animals and Plants, Polar bear (animals.sandiegozoo.org/node/64 = /animals/polar-bear)
   "Their fat can be 2 to 4 inches (5 to 10 centimeters) thick."   "It may also help insulate their bodies, generate heat in the freezing
   temperatures, and keep them afloat in water."   "An outer coat of long guard hairs that stick together when wet protects a dense, thick
   undercoat of fur."   "On land, water rolls right off the guard hairs."   "Stiff fur on the sole of each foot keeps polar bears from slipping on
   the ice."   "Built to stay warm in their cold habitat, polar bears sometimes overheat and have to cool off in the chilly water."
   "The den is often no bigger than a telephone booth, but it can be about 40 degrees warmer in there."   "They depend on their mother to keep
   them warm and fed."   "When the weather is extremely cold, and hunting is impossible, bears may seek temporary shelter in snow dens"
 [SDZ-L] SDZWA Library, Polar bear, Physical Characteristics (ielc.libguides.com/sdzg/factsheets/polarbear/characteristics)
   "Large amounts of subcutaneous fat"  "5–10 cm thick in adults"  "Both fat and pelt provide insulation"  "Thick underfur"
   "Tufted intermediate guard hairs (15 cm long)"  "Few parts of a polar bear's body lack fur. Even their foot pads may be furred during winter."
 [NG] National Geographic Education, Animals 101: Polar Bears (education.nationalgeographic.org/resource/animals-101-polar-bears)
   "the bears have a two to four inch layer of fat that helps keep them buoyant and warm as they swim."
   "It consists of two layers of transparent hair, a soft, thick undercoat and a layer of hollow guard hairs."
 [SW] SeaWorld, Polar bear (seaworld.org/animals/facts/mammals/polar-bear): "a fat layer that can reach a thickness of up to 11 cm (4.3 in.)"
 [LPZ] Lincoln Park Zoo, Polar Bear Adaptations (lpzoo.org, PolarBearAdaptions_2025_English.pdf)
   "a thick, fuzzy, downy layer right next to their skin"  "a layer of guard hairs, or longer hairs, which acts like their raincoat."
   "They also have fur on their feet to help keep them warm"  "These layers help keep them warm even when it's minus 40 degrees Fahrenheit!"
 NOT read: Polar Bears International's adaptation page (the reader's permission request timed out today), so nothing is taken from it.
 Said as: under its skin a polar bear has a thick layer of fat [SDZ, SDZ-L, NG]; the fat helps keep it warm [NG, SDZ, SDZ-L]; it can be up to
 four inches thick [SDZ, NG; SW 4.3 in]; in the cold water the fat keeps it warm and helps it float [NG "buoyant and warm as they swim",
 SDZ "keep them afloat"]; a polar bear has two layers of fur [NG]: a soft, thick undercoat close to the skin [NG, LPZ, SDZ-L] and long guard
 hairs on top [SDZ, NG, LPZ]; the long hairs are like a raincoat [LPZ]; on land, water rolls right off [SDZ]; fur covers almost all of its body
 [SDZ-L]; fur and fat keep it warm even on the coldest days [LPZ, SDZ-L "Both fat and pelt provide insulation"]; it has fur on the bottoms of
 its feet [SDZ, SDZ-L, LPZ]; the fur keeps its feet warm [LPZ] and stops it slipping on the ice [SDZ]; a mama polar bear and her cubs stay in a
 cozy den in the snow, and inside the den it can be much warmer than outside [SDZ]; the cubs stay warm with their mama [SDZ]; polar bears are
 so warm they can even get too hot, then they cool off in the chilly water [SDZ].
 The fat "like a cozy blanket" and the fur "like a raincoat" are said as pictures to understand by (the raincoat one is LPZ's own).
 Nobody is hurt, lost, crying or trapped; the cold is a cozy "Brrr!", Poppy is happy and warm the whole time.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_za_ep10, art_za_ep11 as A11, art_zc_ep12 as A12
import art_zc_ep13 as A
from kit import Kit, S, prop, W
from intro import INTRO_STAGES, intro_shots

EP = {"id": "zc_ep13", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "How Do Polar Bears Stay Warm?", "thumb_text": "NOT COLD?!", "series": "Animal Facts with Milo",
      "description": ("How does a polar bear stay warm in the snow and the icy water? Find Poppy the polar bear cub's three warm secrets with Milo the bluebird! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count, moves to copy and a quiz at the end.\n"
                      "Kids learn that under its skin a polar bear has a thick layer of fat, up to four inches thick, that keeps it warm in the cold water and helps it float; "
                      "that it has two layers of fur, a soft, thick undercoat and long guard hairs on top that work like a raincoat; and that it has fur on the bottoms "
                      "of its feet, a cozy den in the snow for the cubs, and is so warm that it sometimes cools off in the chilly water.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (polar bear) and its Library fact sheet (polar bear); National Geographic Education "
                      "(Animals 101: Polar Bears); SeaWorld (polar bear); Lincoln Park Zoo (polar bear adaptations)."),
      "tags": ["how do polar bears stay warm", "polar bear facts for kids", "polar bear", "arctic animals for kids", "polar bear fur", "polar bear fat",
               "animal facts for kids", "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "arctic": [("bear", "bear", 1000, 930, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
    "arctic_low": [("bear", "bear", 1000, 930, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
    "arctic_eve": [("bear", "bear", 1000, 930, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
    "snowbottom": [("bear", "bear", 1000, 935, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
    "zoo": [("milo", "milo", 960, 940, 1.1)],
    "zoo_eve": [("milo", "milo", 960, 940, 1.0)],
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 1100, 0, -90))


def PULSE(at, sel, k=1.2, n=1, o="50% 50%"): return ("to", at, sel, {"scale": k, "transformOrigin": o, "duration": .2, "yoyo": True, "repeat": 2 * n - 1}, "a picture pulses")
def BOB(at, n=3, who="bear"): return ("to", at, f"#{{p}}{who}", {"y": "-=34", "duration": .42, "yoyo": True, "repeat": 2 * n - 1, "ease": "sine.inOut"}, f"{who} bobs in the water")
def BLINK(at, sel, n=3, desc=""): return ("to", at, sel, {"opacity": .35, "duration": .2, "yoyo": True, "repeat": 2 * n - 1}, desc)


# ------------------------------------------------------------------ cameras on Poppy (16:9, 9:16)
BB = C("arctic", "bear", "all", 1400, 20, -70); BBP = WV("arctic", ["bear"], floor=.72, top=.44, pad=.1)
BH = C("arctic", "bear", "head", 800, -60, -30); BHP = V("arctic", "bear", "head", 1200, -60, -40)
LB = C("arctic_low", "bear", "all", 1400, 20, -70); LBP = WV("arctic_low", ["bear"], floor=.72, top=.44, pad=.1)
EB = C("arctic_eve", "bear", "all", 1400, 20, -70); EBP = WV("arctic_eve", ["bear"], floor=.72, top=.44, pad=.1)
SB = C("snowbottom", "bear", "all", 1400, 20, -70); SBP = WV("snowbottom", ["bear"], floor=.72, top=.44, pad=.1)
SF = (1060, 700, 1100); SFP = V("snowbottom", "bear", "paw", 1300, -40, -260)
# swimming: Poppy lower, the sea in front of her (water line y 840)
SWIM = {"bear": (1000, 1080, 1.0)}
SWC = (1060, 760, 1300); SWCP = (1080, 700, 1500)
WATER = lambda: prop("wa", A.water_front, 1000, 840, 1.0, p=(1000, 840, 1.0))

# ------------------------------------------------------------------ props
SNOW = lambda: prop("snow", art.snow, 0, 0, 1.0)
def FALL(at=0, d=6.0): return ("fromto", at, ".{p}snow-f", {"y": -60}, {"y": 220, "duration": d, "ease": "none"}, "snow falls")
THERMO = lambda x=560, y=880, s=1.0, p=(330, 860, .8): prop("th", A.thermometer, x, y, s, p=p)
def DROP_T(at): return ("to", at, "#{p}th-lvl", {"scaleY": .35, "transformOrigin": "50% 100%", "duration": 1.0, "ease": "power2.inOut"}, "the thermometer drops: cold!")
COAT = lambda x=960, y=570, s=.9, p=(960, 660, .9): prop("co", A.coat, x, y, s, p=p)       # parts -fat -skin -under -guard
FATR = lambda x=960, y=580, s=1.15, p=(960, 640, .95): prop("fr", A.fat_ruler, x, y, s, p=p)          # parts -fat -m1..-m4
PAW = lambda x=960, y=560, s=1.05, p=(960, 720, .95): prop("pw", A.paw_sole, x, y, s, p=p)            # parts -fur -fur2
DEN = lambda x=960, y=900, s=.95, p=(960, 900, .62): prop("dn", A.den_cut, x, y, s, p=p)              # parts -glow -mama -cub -wind
HEAT = lambda name, x, y, s=1.0, p=None: prop(name, A12.heat_waves, x, y, s, True, p=p or (x, y, s))
DROPS = lambda x=1000, y=230, p=(1000, 300, 1.0): prop("dr", A.drops, x, y, 1.1, True, p=p)
def RAIN(at): return ("fromto", at, "#{p}dr-d0,#{p}dr-d1,#{p}dr-d2,#{p}dr-d3", {"y": -40}, {"y": 150, "duration": .7, "ease": "power1.in", "stagger": .18}, "rain drops fall on the long hairs")
def ROLL(at): return ("to", at, "#{p}dr-d0,#{p}dr-d1,#{p}dr-d2,#{p}dr-d3", {"x": "+=420", "y": "+=260", "opacity": 0, "duration": 1.1, "ease": "power1.in", "stagger": .15}, "the drops roll right off")

SHOTS = [
    # ---------------------------------------------------------------- HOOK (cold open on the promise: Poppy happy in the snow, the thermometer drops)
    S("arctic", (900, 620, 1500), "Brrr! The snow is so cold. How does a polar bear stay warm?", q=True, tag="hook: cold snow, warm bear", hide=["milo"],
      pcam=WV("arctic", ["bear"], floor=.74, top=.44, pad=.22), cam2=(900, 620, 1580), props=[SNOW(), THERMO()],
      fx=[FALL(0, 6.5), DROP_T("w:cold."), ("nod", "w:warm?", "bear")], words=[("w:warm?", "WARM?", .8, .2, 1.2, "sun", (.5, .32), 1.0)]),
    S("arctic", BB, "Look at Poppy! She is not cold at all!", q=True, tag="hook: not cold at all", hide=["milo"], pcam=BBP, cam2=W(BB, 1.05), props=[SNOW()],
      fx=[FALL(0, 4.0), ("hop", "w:Poppy!", "bear"), ("hop", "w:all!", "bear")], words=[("w:not", "NOT COLD!", .26, .32, 1.0, "sun", (.5, .32), .9)]),
    S("arctic", say="I'm Milo the bluebird. Let's find Poppy's warm secrets!", q=True, tag="hook: Milo", hide=["bear"], fx=[("hop", "w:secrets!", "milo")],
      words=[("w:secrets!", "SECRETS!", .8, .45, 1.0, "sun", (.5, .33), .9)], **dict(cam=C("arctic", "milo", "body", 900), pcam=V("arctic", "milo", "body", 1100, 0, -90))),
    *intro_shots(),
    S("arctic", (960, 600, 1700), "Poppy has three warm secrets. Let's find them, one by one!", q=True, tag="three secrets", trans="iris", hide=["milo"], pcam=BBP, cam2=(960, 600, 1780),
      fx=[("nod", "w:three", "bear")],
      words=[("w:three", "1", .22, .22, 1.1, "sun", (.3, .3), 1.0), ("w:secrets.", "2", .5, .22, 1.1, "sun", (.5, .3), 1.0), ("w:one:1", "3", .78, .22, 1.1, "sun", (.7, .3), 1.0)]),
    # ---------------------------------------------------------------- PART 1: thick fat
    S("arctic", BH, "Warm secret number one! What is under a polar bear's skin?", part=1, q=True, tag="secret 1", hide=["milo"], pcam=BHP, cam2=W(BH, 1.05),
      fx=[("lookat", "w:under", "bear", 8), ("lookat", "e:skin?", "bear", 0)], words=[("w:one!", "1", .78, .2, 1.4, "sun", (.3, .3), 1.2), ("w:skin?", "?", .2, .3, 2.0, "sun", (.7, .34), 1.3)]),
    S("arctic", (1000, 600, 1500), "Is it a layer of fat? Or a layer of ice?", part=1, q=True, tag="question 1a", pause=3.2, hide=["milo"], pcam=(1000, 520, 1800),
      fx=[("signs", "w:fat?", ["FAT", "ICE"], 0, "wait:2.0"), ("nod", "wait:1.2", "bear")]),
    S("paper", (960, 560, 1500), "It is fat! Under the skin, a polar bear has a thick layer of fat.", part=1, tag="board: thick fat", pcam=(960, 600, 1700), props=[COAT()],
      fx=[BLINK("w:skin,", "#{p}co-skin", 2, "the skin blinks"), PULSE("w:thick", "#{p}co-fat", 1.06, 2), BLINK("e:fat.:2", "#{p}co-fat", 2, "the fat layer blinks")],
      words=[("w:fat!:1", "FAT!", .84, .08, 1.2, "sun", (.5, .27), 1.0)]),
    S("paper", (1040, 600, 1420), "Can you point to the fat? It is the yellow layer, at the bottom!", part=1, q=True, tag="point to the fat", pause=2.4, pcam=(1000, 700, 1600),
      props=[COAT(), prop("pt", A.pointer, 1390, 772, .9, True, p=(1300, 860, .45))],
      fx=[("show", "w:point", "pt"), ("to", "w:yellow", "#{p}pt", {"x": 40, "duration": .25, "yoyo": True, "repeat": 5, "ease": "sine.inOut"}, "the arrow points at the fat"),
          PULSE("w:yellow", "#{p}co-fat", 1.06, 2), PULSE("e:bottom!", "#{p}co-fat", 1.08, 2), ("to", "wait:1.0", "#{p}pt", {"x": 40, "duration": .25, "yoyo": True, "repeat": 3}, "the arrow points again")],
      words=[("w:point", "POINT!", .86, .45, .9, "sun", (.5, .27), .9)]),
    S("paper_blue", (960, 560, 1500), "The fat works like a cozy blanket. It helps keep the bear warm!", part=1, tag="board: like a blanket", pcam=(960, 600, 1900),
      actors=[("bear", "bear", 980, 820, 1.0)], props=[prop("gl", A.glow_ring, 1030, 600, .9, p=(1030, 610, .9))],
      fx=[PULSE("w:blanket.", "#{p}gl-ring", 1.06, 2), ("nod", "w:warm!", "bear")], words=[("w:warm!", "WARM!", .2, .18, 1.1, "sun", (.5, .28), .9)]),
    S("paper", (960, 560, 1500), "How thick is it? Up to four inches! Count with me. One, two, three, four!", part=1, q=True, tag="board: count four inches", pcam=(960, 600, 1700), props=[FATR()],
      fx=[PULSE("w:thick", "#{p}fr-fat", 1.04), PULSE("w:One,", "#{p}fr-m1", 1.3), PULSE("w:two,", "#{p}fr-m2", 1.3), PULSE("w:three,", "#{p}fr-m3", 1.3), PULSE("w:four!:2", "#{p}fr-m4", 1.3)],
      words=[("w:four:1", "4 INCHES!", .5, .065, 1.0, "sun", (.5, .26), .8)]),
    S("zoo", say="Can you show me four fingers? One, two, three, four!", part=1, q=True, tag="four fingers", pause=2.0,
      fx=[("hop", "w:One,", "milo"), ("hop", "w:two,", "milo"), ("hop", "w:three,", "milo"), ("hop", "e:four!:2", "milo")],
      words=[("w:One,", "1", .12, .45, 1.0, "sun", (.15, .45), .9), ("w:two,", "2", .24, .45, 1.0, "sun", (.27, .45), .9), ("w:three,", "3", .76, .45, 1.0, "sun", (.73, .45), .9), ("e:four!:2", "4", .88, .45, 1.0, "sun", (.85, .45), .9)], **MILO("zoo", 940)),
    S("arctic", BB, "Wow! That is a lot of warm fat!", part=1, tag="a lot of fat", hide=["milo"], pcam=BBP, cam2=W(BB, 1.05),
      fx=[("hop", "w:Wow!", "bear")], words=[("w:Wow!", "WOW!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("arctic", BH, "What does the fat do, when Poppy swims in the icy water?", part=1, q=True, tag="what in the water", pause=3.0, hide=["milo"], pcam=BHP, cam2=W(BH, 1.06),
      fx=[("lookat", "w:swims", "bear", 6)], words=[("e:water?", "?", .2, .3, 2.0, "sun", (.5, .34), 1.3)]),
    S("arctic", SWC, "In the cold water, the fat keeps her warm. And it helps her float!", part=1, tag="fat in the water", hide=["milo"], pcam=SWCP, cam2=W(SWC, 1.05),
      move=SWIM, props=[WATER()], fx=[BOB("w:float!", 3), ("nod", "w:warm.", "bear")], words=[("w:float!", "FLOAT!", .24, .22, 1.1, "sun", (.5, .3), .9)]),
    S("zoo", say="Can you float like a polar bear? Bob up, and down. Bob, bob!", part=1, q=True, tag="float like a bear", pause=2.4,
      fx=[("hop", "w:up,", "milo"), ("hop", "w:Bob,:2", "milo"), ("hop", "e:bob!:3", "milo")], words=[("w:Bob:1", "BOB!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("arctic", BB, "Say it with me. Thick fat keeps a polar bear warm!", part=1, q=True, tag="say it: thick fat", hide=["milo"], pcam=BBP, cam2=W(BB),
      fx=[("nod", "w:Thick", "bear")], words=[("w:Say", "SAY IT!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("zoo", say="Now wrap your arms around you, like a cozy blanket. So warm!", part=1, q=True, tag="wrap your arms", pause=3.0, fx=[("hop", "w:warm!", "milo")],
      words=[("w:warm!", "SO WARM!", .76, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("paper", (960, 580, 1700), "Quick check! Is a polar bear's fat thin, or thick?", part=1, q=True, tag="question 1b", cam2=(960, 580, 1500), pause=3.2, pcam=(960, 700, 1700),
      props=[FATR(960, 700, .85, p=(960, 840, .72))], fx=[PULSE("w:fat", "#{p}fr-fat", 1.05), ("signs", "w:thin,", ["THIN", "THICK"], 1, "wait:2.0"),
          ("word", "e:thick?", "?", {"x": 1600, "y": 470, "size": 200, "cls": "sun", "p": {"x": 1250, "y": 520, "size": 170}})]),
    S("arctic", BB, "Thick! Thick and warm. Super job!", part=1, tag="super job 1", hide=["milo"], pcam=BBP, cam2=W(BB), fx=[("nod", "w:Super", "bear")],
      words=[("w:Thick!:1", "THICK!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- PART 2: two layers of fur
    S("arctic_low", LB, "Warm secret number two! Look at Poppy's fluffy fur. How many layers does it have?", part=2, q=True, tag="secret 2", trans="iris", hide=["milo"], pcam=LBP, pcam2=W(LBP, 1.04), cam2=W(LB, 1.05),
      fx=[("nod", "w:fluffy", "bear")], words=[("w:two!", "2", .26, .26, 1.4, "sun", (.3, .3), 1.2), ("w:have?", "?", .4, .3, 2.0, "sun", (.7, .34), 1.3)]),
    S("arctic_low", (1000, 600, 1500), "Is it one layer of fur? Or two layers?", part=2, q=True, tag="question 2a", pause=3.2, hide=["milo"], pcam=(1000, 520, 1800),
      fx=[("signs", "w:one", ["ONE", "TWO"], 1, "wait:2.0")]),
    S("paper", (960, 560, 1500), "Two layers! First, a soft, thick undercoat, close to the skin.", part=2, tag="board: undercoat", pcam=(960, 600, 1700), props=[COAT()],
      fx=[BLINK("w:soft,", "#{p}co-under", 3, "the soft undercoat blinks")], words=[("w:soft,", "SOFT!", .84, .08, 1.2, "sun", (.5, .27), 1.0)]),
    S("paper", (960, 560, 1500), "And on top, long guard hairs. They are much longer!", part=2, tag="board: guard hairs", pcam=(960, 600, 1700), props=[COAT()],
      fx=[BLINK("w:long", "#{p}co-guard", 3, "the long guard hairs blink")], words=[("w:long", "LONG!", .84, .08, 1.2, "sun", (.5, .27), 1.0)]),
    S("paper", (960, 580, 1500), "Count the layers with me. One, two!", part=2, q=True, tag="count the layers", pcam=(960, 640, 1700), cam2=(960, 580, 1440), props=[COAT()],
      fx=[PULSE("w:One,", "#{p}co-under", 1.08), PULSE("w:two!", "#{p}co-guard", 1.08)],
      words=[("w:One,", "1", .12, .55, 1.3, "sun", (.2, .3), 1.1), ("w:two!", "2", .88, .4, 1.3, "sun", (.8, .3), 1.1)]),
    S("zoo", say="Pat your arms softly, like a soft, fluffy undercoat. Pat, pat!", part=2, q=True, tag="pat softly", pause=2.4,
      fx=[("hop", "w:Pat:2", "milo"), ("hop", "e:pat!:3", "milo"), ("hop", "wait:1.2", "milo")], words=[("w:Pat:2", "PAT, PAT!", .76, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("paper_blue", (960, 560, 1500), "The long hairs work like a raincoat. Water rolls right off! Drip, drop!", part=2, tag="board: raincoat", pcam=(960, 600, 1700),
      props=[COAT(960, 600, 1.0, p=(960, 680, .9)), DROPS(1000, 230, p=(1000, 330, 1.0))],
      fx=[("show", "w:raincoat.", "dr"), RAIN("w:raincoat."), ROLL("w:rolls"), BLINK("w:long", "#{p}co-guard", 2, "the long hairs blink")],
      words=[("w:raincoat.", "RAINCOAT!", .82, .1, .85, "sun", (.5, .26), .85)]),
    S("zoo", say="Put on your raincoat, like a polar bear. Zip it up, all the way!", part=2, q=True, tag="zip your raincoat", pause=2.4, fx=[("hop", "w:Zip", "milo"), ("hop", "e:way!", "milo")],
      words=[("w:Zip", "ZIP!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("arctic_low", LB, "And look! Fur covers almost all of its body.", part=2, tag="fur all over", hide=["milo"], pcam=LBP, cam2=W(LB, 1.05),
      fx=[PULSE("w:all", "#{p}bear", 1.04, 1, "50% 100%")], words=[("w:Fur", "FUR!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("arctic_low", BH, "Does a polar bear stay warm, even on the very coldest days?", part=2, q=True, tag="even the coldest days", pause=3.0, hide=["milo"], pcam=BHP, pcam2=W(BHP, 1.08), cam2=W(BH, 1.06),
      props=[SNOW()], fx=[FALL(0, 6.0)], words=[("e:days?", "?", .2, .3, 2.0, "sun", (.5, .34), 1.3)]),
    S("arctic_low", LB, "Yes! Fur and fat keep it warm, even on the coldest, snowiest days!", part=2, tag="fur and fat", hide=["milo"], pcam=LBP, cam2=W(LB),
      props=[SNOW()], fx=[FALL(0, 5.0), ("hop", "w:Yes!", "bear")], words=[("w:Yes!", "YES!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("zoo", say="Fluff up your fur, like a fluffy polar bear. Puff!", part=2, q=True, tag="fluff up", pause=2.4,
      fx=[("to", "e:Puff!", "#{p}milo", {"scale": 1.12, "transformOrigin": "50% 100%", "duration": .25, "yoyo": True, "repeat": 3}, "Milo fluffs up")],
      words=[("e:Puff!", "PUFF!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("arctic_low", LB, "Say it with me. A polar bear has two layers of fur!", part=2, q=True, tag="say it: two layers", hide=["milo"], pcam=LBP, cam2=W(LB),
      fx=[("nod", "w:two", "bear")], words=[("w:Say", "SAY IT!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("paper_blue", (960, 580, 1700), "Quick check! What does water do on the long hairs? Roll off, or soak in?", part=2, q=True, tag="question 2b", cam2=(960, 580, 1500), pause=3.2, pcam=(960, 700, 1700),
      props=[COAT(960, 680, .8, p=(960, 860, .75))], fx=[BLINK("w:long", "#{p}co-guard", 2), ("signs", "w:Roll", ["ROLL OFF", "SOAK IN"], 0, "wait:2.0"),
          ("word", "e:in?", "?", {"x": 1600, "y": 470, "size": 200, "cls": "sun", "p": {"x": 1250, "y": 520, "size": 170}})]),
    S("arctic_low", LB, "It rolls right off! Great job!", part=2, tag="great job 2", hide=["milo"], pcam=LBP, cam2=W(LB), fx=[("nod", "w:Great", "bear")],
      words=[("w:off!", "GREAT!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- PART 3: furry feet and a cozy den
    S("snowbottom", SF, "Warm secret number three! The ice is so cold. How does Poppy keep her feet warm?", part=3, q=True, tag="secret 3", trans="iris", hide=["milo"], pcam=SBP, pcam2=W(SBP, 1.04), cam2=W(SF, 1.05),
      fx=[PULSE("w:feet", "#{p}bear-fl", 1.1, 2, "50% 100%")], words=[("w:three!", "3", .4, .15, 1.4, "sun", (.3, .3), 1.2), ("w:warm?:2", "?", .9, .25, 2.0, "sun", (.7, .34), 1.3)]),
    S("snowbottom", (1000, 600, 1500), "Is it fur on her feet? Or little socks?", part=3, q=True, tag="question 3a", pause=3.2, hide=["milo"], pcam=(1000, 520, 1800),
      fx=[("signs", "w:fur", ["FUR", "SOCKS"], 0, "wait:2.0")]),
    S("paper_pink", (960, 560, 1500), "Fur! A polar bear has fur, on the bottoms of its feet.", part=3, tag="board: furry soles", pcam=(960, 600, 1700), props=[PAW()],
      fx=[PULSE("w:fur,:2", "#{p}pw-fur", 1.04, 2), BLINK("w:bottoms", "#{p}pw-fur2", 3, "the fur between the pads blinks")], words=[("w:Fur!:1", "FUR!", .82, .14, 1.2, "sun", (.5, .26), 1.0)]),
    S("snowbottom", SB, "The fur keeps its feet warm. And it stops it slipping on the ice!", part=3, tag="warm feet, no slipping", hide=["milo"], pcam=SBP, cam2=W(SB, 1.05),
      fx=[("walk", "w:keeps", "bear", 80, 2.0)], words=[("w:slipping", "NO SLIP!", .26, .32, 1.1, "sun", (.5, .32), .9)]),
    S("zoo", say="Wiggle your toes, all warm and cozy. Wiggle, wiggle!", part=3, q=True, tag="wiggle your toes", pause=2.4, fx=[("hop", "w:Wiggle,:2", "milo"), ("hop", "e:wiggle!:3", "milo"), ("hop", "wait:1.2", "milo")],
      words=[("w:Wiggle,:2", "WIGGLE!", .76, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("arctic_eve", EB, "Where does a mama polar bear keep her cubs warm?", part=3, q=True, tag="where are cubs warm", pause=3.0, hide=["milo"], pcam=EBP, cam2=W(EB, 1.06),
      fx=[("lookat", "w:cubs", "bear", 6)], words=[("e:warm?", "?", .26, .34, 2.0, "sun", (.5, .34), 1.3)]),
    S("paper_blue", (960, 560, 1700), "In a cozy den, in the snow! Inside, it can be much warmer than outside.", part=3, tag="board: snow den", pcam=(960, 640, 1700), props=[DEN()],
      fx=[PULSE("w:den,", "#{p}dn-glow", 1.08, 2), PULSE("w:warmer", "#{p}dn-glow", 1.12, 2), BLINK("w:outside.", "#{p}dn-wind", 2, "the cold wind blows outside")],
      words=[("w:den,", "SNOW DEN!", .5, .1, 1.0, "sun", (.5, .27), .85), ("w:warmer", "WARM!", .5, .4, 1.0, "sun", (.5, .45), .9)]),
    S("paper_blue", (1080, 640, 1300), "The cubs snuggle up to their mama, to stay warm.", part=3, tag="board: cubs snuggle", pcam=(1100, 660, 1500), props=[DEN()],
      fx=[("to", "w:snuggle", "#{p}dn-cub", {"x": "-=30", "duration": .5, "ease": "sine.inOut"}, "the cub snuggles up to mama"), PULSE("w:warm.", "#{p}dn-glow", 1.1, 2)],
      words=[("w:snuggle", "SNUGGLE!", .5, .14, 1.0, "sun", (.5, .28), .85)]),
    S("zoo", say="Give yourself a cozy snuggle, like a polar bear cub. Snuggle!", part=3, q=True, tag="cozy snuggle", pause=3.0, fx=[("hop", "e:Snuggle!:2", "milo")],
      words=[("e:Snuggle!:2", "HUG!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("arctic_low", LB, "Polar bears are so warm, they can even get too hot!", part=3, tag="too hot", hide=["milo"], pcam=LBP, cam2=W(LB, 1.05),
      props=[HEAT("h1", 860, 590, 1.0, p=(880, 600, .9)), HEAT("h2", 1020, 580, .9, p=(1030, 590, .8))],
      fx=[("show", "w:warm,", "h1"), ("show", "w:hot!", "h2"), ("to", "w:hot!", "#{p}h1_w,#{p}h2_w", {"y": "-=50", "duration": 1.2, "ease": "sine.out"}, "the heat rises")],
      words=[("w:hot!", "TOO HOT!", .14, .32, .9, "sun", (.5, .32), .9)]),
    S("arctic", SWC, "Then they cool off, in the chilly water. Splash!", part=3, tag="cool off in water", hide=["milo"], pcam=SWCP, cam2=W(SWC, 1.04),
      move=SWIM, props=[WATER(), prop("sp", A.splash, 800, 845, 1.0, True, p=(820, 845, .9))],
      fx=[BOB("w:cool", 3), ("show", "e:Splash!", "sp"), PULSE("e:Splash!", "#{p}sp_w", 1.3)], words=[("e:Splash!", "SPLASH!", .24, .22, 1.1, "sun", (.5, .3), .9)]),
    S("zoo", say="Can you fan yourself, to cool off? Whoosh, whoosh!", part=3, q=True, tag="fan yourself", pause=2.4,
      fx=[("hop", "w:Whoosh,:1", "milo"), ("hop", "e:whoosh!:2", "milo"), ("hop", "wait:1.2", "milo")], words=[("w:Whoosh,:1", "WHOOSH!", .76, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("snowbottom", SB, "Say it with me. Furry feet keep a polar bear warm!", part=3, q=True, tag="say it: furry feet", hide=["milo"], pcam=SBP, cam2=W(SB),
      fx=[("nod", "w:Furry", "bear")], words=[("w:Say", "SAY IT!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("paper_blue", (960, 600, 1700), "Quick check! Where do polar bear cubs stay warm? In a den, or in a tree?", part=3, q=True, tag="question 3b", cam2=(960, 600, 1500), pause=3.2, pcam=(960, 760, 1700),
      props=[DEN(960, 960, .7, p=(960, 1020, .55))], fx=[PULSE("w:warm?", "#{p}dn-glow", 1.1), ("signs", "w:den,", ["DEN", "TREE"], 0, "wait:2.0"),
          ("word", "e:tree?", "?", {"x": 1600, "y": 470, "size": 200, "cls": "sun", "p": {"x": 1250, "y": 520, "size": 170}})]),
    S("arctic_eve", EB, "In a snow den! You remembered!", part=3, tag="you remembered", hide=["milo"], pcam=EBP, cam2=W(EB), fx=[("nod", "w:remembered!", "bear")],
      words=[("w:den!", "DEN!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- QUIZ
    S("zoo_eve", WIDE, "Three warm secrets! Now it is quiz time!", part=4, trans="iris", tag="quiz time", cam2=(960, 560, 1860), pcam=(960, 560, 1800),
      words=[("w:quiz", "QUIZ TIME!", .5, .3, 1.3, "sun", (.5, .33))], fx=[("hop", "w:quiz", "milo", 2)]),
    S("paper", (960, 600, 1600), "What is under a polar bear's skin? A thick layer of fat, or ice?", part=4, q=True, tag="quiz 1", pause=3.2, cam2=(960, 600, 1500), pcam=(960, 700, 1700),
      props=[COAT(960, 680, .8, p=(960, 860, .75))], fx=[BLINK("w:skin?", "#{p}co-skin", 2), ("signs", "w:fat,", ["FAT", "ICE"], 0, "wait:2.0")]),
    S("arctic", BB, "Thick fat! Like a cozy blanket.", part=4, tag="quiz 1: fat", hide=["milo"], pcam=BBP, cam2=W(BB), fx=[("nod", "w:fat!", "bear")],
      words=[("w:fat!", "FAT!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("arctic_low", (1000, 600, 1500), "How many layers of fur does a polar bear have? One, or two?", part=4, q=True, tag="quiz 2", pause=3.2, hide=["milo"], pcam=(1000, 520, 1800),
      fx=[("signs", "w:One,", ["ONE", "TWO"], 1, "wait:2.0")]),
    S("arctic_low", LB, "Two layers! Soft fur, and long hairs.", part=4, tag="quiz 2: two layers", hide=["milo"], pcam=LBP, cam2=W(LB), fx=[("hop", "w:Two", "bear")],
      words=[("w:Two", "TWO!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("paper_pink", (960, 600, 1600), "What is on the bottoms of a polar bear's feet? Fur, or feathers?", part=4, q=True, tag="quiz 3", pause=3.2, cam2=(960, 600, 1500), pcam=(960, 720, 1700),
      props=[PAW(960, 700, .8, p=(960, 860, .8))], fx=[PULSE("w:bottoms", "#{p}pw-fur", 1.04), ("signs", "w:Fur,", ["FUR", "FEATHERS"], 0, "wait:2.0")]),
    S("snowbottom", SB, "Fur! Warm, furry feet.", part=4, tag="quiz 3: fur", hide=["milo"], pcam=SBP, cam2=W(SB), fx=[("nod", "w:Fur!", "bear")],
      words=[("w:Fur!", "FUR!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- RECAP + GOODBYE (the closing picture names the next Arctic lesson)
    S("paper_blue", (960, 600, 1900), "Thick fat, two layers of fur, and furry feet. You found all of Poppy's warm secrets!", part=4, trans="iris", tag="recap: three secrets", pcam=(960, 640, 2500), cam2=(960, 600, 1960),
      props=[FATR(390, 560, .5, p=(540, 300, .55)), COAT(960, 560, .62, p=(540, 640, .55)), PAW(1530, 560, .6, p=(540, 1000, .55))],
      fx=[PULSE("w:fat,", "#{p}fr_w", 1.08), PULSE("w:fur,", "#{p}co_w", 1.08), PULSE("w:furry", "#{p}pw_w", 1.08)],
      words=[("w:found", "YOU DID IT!", .5, .14, 1.0, "sun", (.5, .1), .85)]),
    S("zoo_eve", say="Wrap up like a blanket, zip your raincoat, and wiggle your warm toes!", part=4, q=True, tag="all three moves", pause=1.6,
      fx=[("hop", "w:Wrap", "milo"), ("hop", "w:zip", "milo"), ("hop", "w:wiggle", "milo")],
      words=[("w:wiggle", "WIGGLE!", .76, .3, .9, "sun", (.5, .33), .8)], **MILO("zoo_eve", 940)),
    S("arctic_eve", (960, 600, 1700), "Next time: is a polar bear really white? Bye-bye, friends!", part=4, tag="next: really white", hide=["milo"], pcam=EBP, cam2=(960, 600, 1760),
      fx=[("nod", "w:white?", "bear")], words=[("w:white?", "WHITE?", .5, .12, 1.1, "sun", (.5, .28), .9), ("w:Bye-bye,", "BYE-BYE!", .2, .36, 1.0, "pill", (.5, .38), .8)]),
    *intro_shots(),      # the main intro again as the last shots (owner, Nov 20 4:50 PM)
]
for _s in SHOTS:        # a picture board never drifts closer: it only pulls out a little (16:9 and 9:16)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)

SHORTS = [
    {"id": "zc_ep13_short1", "title": "What Keeps a Polar Bear Warm Under Its Skin?", "band": ("UNDER ITS", "SKIN?"), "thumb_text": "BOB, BOB!", "part": 1,
     "extra_first": [S("arctic", BH, "Brrr! How does a polar bear stay warm in the icy cold?", part=1, q=True, tag="hook: warm in the cold", hide=["milo"], pcam=(BHP[0], BHP[1], 1050), pcam2=(BHP[0], BHP[1], 1130), cam2=W(BH, 1.05),
                       props=[SNOW()], fx=[FALL(0, 5.0), ("nod", "w:warm", "bear")], words=[("w:Brrr!", "?", .78, .3, 2.0, "sun", (.5, .34), 1.3)])]},
    {"id": "zc_ep13_short2", "title": "How Many Fur Coats Does a Polar Bear Have?", "band": ("HOW MANY", "COATS?"), "thumb_text": "DRIP DROP!", "part": 2,
     "extra_first": [S("arctic_low", LB, "Look at this fluffy fur! Is it one coat, or more?", part=2, q=True, tag="hook: fluffy fur", hide=["milo"], pcam=LBP, pcam2=W(LBP, 1.06), cam2=W(LB, 1.05),
                       fx=[("nod", "w:fluffy", "bear")], words=[("w:more?", "?", .26, .3, 2.0, "sun", (.5, .34), 1.3)])]},
    {"id": "zc_ep13_short3", "title": "Why Do Polar Bears Have Furry Feet?", "band": ("FURRY", "FEET?"), "thumb_text": "COZY TOES!", "part": 3,
     "extra_first": [S("snowbottom", SF, "Cold ice under your feet! How does a polar bear keep them warm?", part=3, q=True, tag="hook: cold ice", hide=["milo"], pcam=SBP, pcam2=W(SBP, 1.05), cam2=W(SF, 1.05),
                       fx=[PULSE("w:feet!", "#{p}bear-fl", 1.1, 2, "50% 100%")], words=[("w:warm?", "?", .9, .15, 2.0, "sun", (.5, .34), 1.3)])]},
]

# thumbnails (thumb.py): one big object, 1-2 words, none of the title's words, no watermark
THUMBS = {
    "zc_ep13": {"place": "arctic", "cam": (960, 600, 1500), "actors": [("bear", 1060, 1010, 1.25, False, "")],
                "props": [(A.thermometer, 380, 930, 1.25)], "words": [("NOT COLD?!", 960, 170, 190, "sun")]},
    "zc_ep13_short1": {"place": "arctic", "cam": (1120, 820, 950), "actors": [("bear", 1000, 1080, 1.0, False, "")],
                       "props": [(A.water_front, 1000, 840, 1.0)], "words": [("BOB, BOB!", 540, 1480, 190, "sun")]},
    "zc_ep13_short2": {"place": "paper_blue", "cam": (960, 640, 1900), "props": [(A.coat, 960, 560, 1.15), (A.drops, 1000, 110, 1.2)],
                       "words": [("DRIP", 540, 1380, 200, ""), ("DROP!", 540, 1600, 230, "sun")]},
    "zc_ep13_short3": {"place": "paper_pink", "cam": (960, 640, 1700), "props": [(A.paw_sole, 960, 460, 1.15)],
                       "words": [("COZY", 540, 1420, 200, ""), ("TOES!", 540, 1640, 230, "sun")]},
}
