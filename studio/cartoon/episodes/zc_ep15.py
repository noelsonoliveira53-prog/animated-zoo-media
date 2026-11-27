"""zc_ep15: "Is a Polar Bear Really White?" - Arctic week, fact lesson 2 (2D, docs/CARTOON_RUN.md "A fact lesson and its three Shorts",
"VIRAL PACKAGING", "MAIN INTRO"), a cartoon fact lesson with the 3D music-and-sync process ("beat"). Follows zc_ep13 ("How Do Polar Bears Stay
Warm?", which named this lesson as the next one and left the clear hairs and the black skin to it).
Cold open on Poppy the polar bear cub in the snow, her fur looking white: "Is a polar bear really white?". Milo says his name after the hook;
the main intro right after the hook and again as the last shots. Three parts ("three surprises about polar bear fur"), each cut whole into one
Short, each opening on its own question with answer signs and thinking time:
1. the hairs are clear: see-through, no colour of their own; both layers (the soft undercoat and the long guard hairs) are clear,
2. why the fur looks white: the long guard hairs are hollow, full of air; sunlight bounces around in the hairs, and that makes the fur look white,
3. under the fur the skin is black (the nose too); sunlight goes through the clear fur to the black skin, which soaks up the sun's warmth and
   warms the bear; in summer the fur can look a little yellow.
Quiz with the three surprises, recap, goodbye.

FACTS, read at the source on Nov 27 2026, about 3:25-3:35 PM ET (pages read by the session's page reader, which quoted the sentences verbatim):
 [NG] National Geographic Education, Animals 101: Polar Bears (education.nationalgeographic.org/resource/animals-101-polar-bears/)
   "The fur is actually transparent."   "It consists of two layers of transparent hair, a soft, thick undercoat and a layer of hollow guard hairs."
   "The layers only appear white because the air spaces in each hair scatter all visible wavelengths of light."
   "Underneath this fur, polar bears have black skin."   "Sunlight can penetrate the bear's transparent fur and reach its black skin, which
   absorbs the sun's heat and warms the bear's body."
 [SDZ-L] San Diego Zoo Wildlife Alliance Library, Polar bear, Physical Characteristics (ielc.libguides.com/sdzg/factsheets/polarbear/characteristics)
   "Translucent; no pigments"   "Color varies somewhat with season"   "Yellowish in summer due to oxidation by sun or oils from prey"
   "Black nose, skin, and claws"
 [PBI] Polar Bears International, What Does Polar Bear Fur Feel Like? (polarbearsinternational.org/news-media/articles/what-does-polar-bear-fur-feel-like)
   "Both types of hair are pigment-free and transparent with a mostly hollow, air-filled core."   "This makes the light scatter as each hair
   strand reflects the visible light"   "thus making the polar bear appear white to you and me."   "the guard hairs are longer and actually cover
   the undercoat."
 [OC] Ocean Conservancy, Why Do Polar Bears Have White Fur? (oceanconservancy.org/blog/2020/02/20/polar-bears-white-fur/)
   "polar bear fur is actually transparent"   "Polar bear hair shafts are actually hollow, which allows the fur to reflect back the light of the sun."
   "Much like ice, this reflection is what allows these bears to appear white or even yellow at times."
 NOT read today: the San Diego Zoo animal page, SeaWorld and National Geographic's polar bear page (the reader's permission requests timed out),
 so nothing is taken from them.
 Said as: a polar bear's hair is clear, see-through [NG, PBI, OC, SDZ-L "Translucent"], it has no colour of its own [SDZ-L "no pigments", PBI
 "pigment-free"]; both layers, the soft undercoat and the long guard hairs, are clear [NG, PBI]; the long guard hairs are hollow, full of air
 [NG "hollow guard hairs", PBI "air-filled core", OC]; the light bounces around in the hairs [NG "scatter", PBI "light scatter ... reflects"] and
 that makes the fur look white [NG, PBI, OC]; like sparkly ice [OC "Much like ice"]; under the fur a polar bear has black skin [NG, SDZ-L] and a
 black nose [SDZ-L]; sunlight shines through the clear fur to the black skin [NG], which soaks up the sun's warmth and warms the bear [NG
 "absorbs the sun's heat and warms the bear's body"]; the colour changes a little with the seasons and in summer the fur can look a little
 yellow [SDZ-L, OC "or even yellow at times"].
 "Hollow, like a straw" is said as a picture to understand by. Nobody is hurt, lost, crying or trapped; Poppy is happy the whole time.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_za_ep10, art_za_ep11 as A11, art_zc_ep12 as A12
import art_zc_ep13 as A13
import art_zc_ep15 as A
from kit import Kit, S, prop, W
from intro import INTRO_STAGES, intro_shots

EP = {"id": "zc_ep15", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "Is a Polar Bear Really White?", "thumb_text": "SEE-THROUGH?!", "series": "Animal Facts with Milo",
      "description": ("Is a polar bear really white? Look very closely at one hair with Milo the bluebird and Poppy the polar bear cub, and find three surprises! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count, moves to copy and a quiz at the end.\n"
                      "Kids learn that a polar bear's hairs are clear and see-through, with no color of their own; that the long guard hairs are hollow and full of air, "
                      "and the sunlight bouncing around in the hairs makes the fur look white; and that under the fur a polar bear has black skin and a black nose, "
                      "and the black skin soaks up the sun's warmth. In summer the fur can even look a little yellow.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNational Geographic Education (Animals 101: Polar Bears); San Diego Zoo Wildlife Alliance Library fact sheet (polar bear); "
                      "Polar Bears International (What Does Polar Bear Fur Feel Like?); Ocean Conservancy (Why Do Polar Bears Have White Fur?)."),
      "tags": ["is a polar bear really white", "polar bear facts for kids", "polar bear fur", "polar bear black skin", "polar bear", "arctic animals for kids",
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
def BLINK(at, sel, n=3, desc=""): return ("to", at, sel, {"opacity": .35, "duration": .2, "yoyo": True, "repeat": 2 * n - 1}, desc)
def SHOW(at, sel, desc): return ("to", at, sel, {"opacity": 1, "duration": .35}, desc)


# ------------------------------------------------------------------ cameras on Poppy (16:9, 9:16)
BB = C("arctic", "bear", "all", 1400, 20, -70); BBP = WV("arctic", ["bear"], floor=.72, top=.44, pad=.1)
BH = C("arctic", "bear", "head", 800, -60, -30); BHP = V("arctic", "bear", "head", 1200, -60, -40)
LB = C("arctic_low", "bear", "all", 1400, 20, -70); LBP = WV("arctic_low", ["bear"], floor=.72, top=.44, pad=.1)
LH = C("arctic_low", "bear", "head", 800, -60, -30); LHP = V("arctic_low", "bear", "head", 1200, -60, -40)
EB = C("arctic_eve", "bear", "all", 1400, 20, -70); EBP = WV("arctic_eve", ["bear"], floor=.72, top=.44, pad=.1)
EH = C("arctic_eve", "bear", "head", 800, -60, -30); EHP = V("arctic_eve", "bear", "head", 1200, -60, -40)
SB = C("snowbottom", "bear", "all", 1400, 20, -70); SBP = WV("snowbottom", ["bear"], floor=.72, top=.44, pad=.1)

# ------------------------------------------------------------------ props
SNOW = lambda: prop("snow", art.snow, 0, 0, 1.0)
def FALL(at=0, d=6.0): return ("fromto", at, ".{p}snow-f", {"y": -60}, {"y": 220, "duration": d, "ease": "none"}, "snow falls")
LENS = lambda x=960, y=500, s=.85, p=(960, 720, .85): prop("ln", A.lens_hair, x, y, s, p=p)                 # part -hair
TUBE = lambda x=960, y=560, s=.85, p=(960, 780, .85): prop("tb", A.hair_tube, x, y, s, p=p)                 # part -core
BOUNCE = lambda x=1000, y=580, s=.85, p=(1000, 760, .8): prop("bo", A.sun_bounce, x, y, s, p=p)           # parts -in0..-in2, -out
SKIN = lambda x=960, y=560, s=1.05, p=(960, 660, .95): prop("sk", A.skin_board, x, y, s, p=p)              # parts -skin -sun -rays -warm
SWATCH = lambda x=960, y=600, s=1.0, p=(960, 680, .9): prop("sw", A.fur_swatches, x, y, s, p=p)            # parts -white -yellow
COAT = lambda x=960, y=570, s=.9, p=(960, 660, .9): prop("co", A13.coat, x, y, s, p=p)                     # parts -fat -skin -under -guard
POINT = lambda x, y, p: prop("pt", A13.pointer, x, y, .9, True, p=p)


SHOTS = [
    # ---------------------------------------------------------------- HOOK (cold open on the promise: Poppy's fur looks white... or does it?)
    S("arctic", (900, 620, 1500), "Poppy's fur looks so white, like the snow. But is a polar bear really white?", q=True, tag="hook: really white?", hide=["milo"],
      pcam=WV("arctic", ["bear"], floor=.74, top=.44, pad=.22), cam2=(900, 620, 1580), props=[SNOW()],
      fx=[FALL(0, 6.5), ("nod", "w:white?", "bear")], words=[("w:white?", "WHITE?", .8, .2, 1.2, "sun", (.5, .32), 1.0)]),
    S("arctic", BH, "Let's look very closely, at just one hair!", q=True, tag="hook: one hair", hide=["milo"], pcam=BHP, cam2=W(BH, 1.05),
      fx=[("lookat", "w:closely,", "bear", 6), ("nod", "w:hair!", "bear")], words=[("w:one", "1 HAIR!", .78, .3, 1.0, "sun", (.5, .32), .9)]),
    S("arctic", say="I'm Milo the bluebird. Let's find out together!", q=True, tag="hook: Milo", hide=["bear"], fx=[("hop", "w:together!", "milo")],
      words=[("w:find", "LET'S SEE!", .8, .45, 1.0, "sun", (.5, .33), .9)], **dict(cam=C("arctic", "milo", "body", 900), pcam=V("arctic", "milo", "body", 1100, 0, -90))),
    *intro_shots(),
    S("arctic", (960, 600, 1700), "Polar bear fur has three big surprises. Let's find them, one by one!", q=True, tag="three surprises", trans="iris", hide=["milo"], pcam=BBP, cam2=(960, 600, 1780),
      fx=[("nod", "w:three", "bear")],
      words=[("w:three", "1", .22, .22, 1.1, "sun", (.3, .3), 1.0), ("w:surprises.", "2", .5, .22, 1.1, "sun", (.5, .3), 1.0), ("w:one:1", "3", .78, .22, 1.1, "sun", (.7, .3), 1.0)]),
    # ---------------------------------------------------------------- PART 1: the hairs are clear
    S("arctic", BH, "Surprise number one! What color is one polar bear hair?", part=1, q=True, tag="surprise 1", hide=["milo"], pcam=BHP, cam2=W(BH, 1.05),
      fx=[("lookat", "w:color", "bear", 8)], words=[("w:one!", "1", .78, .2, 1.4, "sun", (.3, .3), 1.2), ("w:hair?", "?", .2, .3, 2.0, "sun", (.7, .34), 1.3)]),
    S("arctic", (1000, 600, 1500), "Is it white, like snow? Or clear, like water?", part=1, q=True, tag="question 1a", pause=3.2, hide=["milo"], pcam=(1000, 520, 1800),
      fx=[("signs", "w:white,", ["WHITE", "CLEAR"], 1, "wait:2.0"), ("nod", "wait:1.2", "bear")]),
    S("paper_blue", (960, 560, 1500), "It is clear! Each hair is see-through. It has no color of its own.", part=1, tag="board: clear hair", pcam=(960, 620, 1700), props=[LENS()],
      fx=[BLINK("w:clear!", "#{p}ln-hair", 2, "the hair blinks"), PULSE("w:see-through.", "#{p}ln-hair", 1.06, 2)],
      words=[("w:clear!", "CLEAR!", .84, .1, 1.2, "sun", (.5, .31), 1.0)]),
    S("paper_blue", (1000, 600, 1420), "Look through the hair. You can see the blue, right through it!", part=1, q=True, tag="see through it", pause=2.2, pcam=(1000, 660, 1600),
      props=[LENS(960, 590, .85), POINT(1290, 490, (1240, 450, .45))],
      fx=[("show", "w:Look", "pt"), ("to", "w:blue,", "#{p}pt", {"x": 40, "duration": .25, "yoyo": True, "repeat": 5, "ease": "sine.inOut"}, "the arrow points at the hair"),
          PULSE("w:through:2", "#{p}ln-hair", 1.06, 2)],
      words=[("w:blue,", "SEE-THROUGH!", .5, .08, .9, "sun", (.5, .31), .8)]),
    S("zoo", say="Make a magnifying glass with your fingers. Now look, look!", part=1, q=True, tag="finger magnifier", pause=2.4,
      fx=[("hop", "w:look,", "milo"), ("hop", "e:look!", "milo")],
      words=[("w:look,", "LOOK!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("paper", (960, 560, 1500), "Both layers of fur are clear. The soft undercoat, and the long guard hairs!", part=1, tag="board: both layers clear", pcam=(960, 600, 1700), props=[COAT()],
      fx=[BLINK("w:soft", "#{p}co-under", 2, "the soft undercoat blinks"), BLINK("w:long", "#{p}co-guard", 2, "the long guard hairs blink")],
      words=[("w:Both", "BOTH CLEAR!", .5, .08, 1.0, "sun", (.5, .31), .85)]),
    S("paper", (960, 580, 1500), "Count the layers with me. One, two!", part=1, q=True, tag="count the layers", pcam=(960, 640, 1700), cam2=(960, 580, 1440), props=[COAT()],
      fx=[PULSE("w:One,", "#{p}co-under", 1.08), PULSE("w:two!", "#{p}co-guard", 1.08)],
      words=[("w:One,", "1", .12, .55, 1.3, "sun", (.2, .3), 1.1), ("w:two!", "2", .88, .4, 1.3, "sun", (.8, .3), 1.1)]),
    S("arctic", BB, "Wow! Poppy's hairs are not white at all. They are clear!", part=1, tag="not white at all", hide=["milo"], pcam=BBP, cam2=W(BB, 1.05),
      fx=[("hop", "w:Wow!", "bear"), ("nod", "w:clear!", "bear")], words=[("w:Wow!", "WOW!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("arctic", BB, "Poppy has lots and lots of hairs. And every one of them is clear!", part=1, tag="lots of clear hairs", hide=["milo"], pcam=BBP, cam2=W(BB, 1.05),
      props=[SNOW()], fx=[FALL(0, 5.0), ("nod", "w:clear!", "bear")], words=[("w:lots:2", "LOTS!", .26, .34, 1.2, "sun", (.5, .34), 1.0)]),
    S("paper_blue", (960, 580, 1600), "Does a polar bear hair have a color of its own? Yes, or no?", part=1, q=True, tag="question 1c", pause=3.2, cam2=(960, 580, 1500), pcam=(960, 700, 1700),
      props=[LENS(960, 640, .6, p=(960, 840, .62))], fx=[PULSE("w:color", "#{p}ln-hair", 1.05), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("arctic", BH, "No! No color at all. It is see-through.", part=1, tag="no color", hide=["milo"], pcam=BHP, cam2=W(BH, 1.05),
      fx=[("nod", "w:No!", "bear")], words=[("w:No!", "NO COLOR!", .78, .3, 1.0, "sun", (.5, .32), .9)]),
    S("zoo", say="Hold your hands up to your eyes, and peek through. Peekaboo!", part=1, q=True, tag="peek through", pause=2.4,
      fx=[("hop", "w:peek", "milo"), ("hop", "e:Peekaboo!", "milo"), ("hop", "wait:1.2", "milo")],
      words=[("e:Peekaboo!", "PEEKABOO!", .76, .3, .85, "sun", (.5, .33), .8)], **MILO("zoo", 940)),
    S("zoo", say="Blink your eyes, like you are looking very closely. Blink, blink!", part=1, q=True, tag="blink closely", pause=2.4,
      fx=[("hop", "w:Blink,:2", "milo"), ("hop", "e:blink!:3", "milo"), ("hop", "wait:1.2", "milo")],
      words=[("w:Blink,:2", "BLINK!", .76, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("arctic", BB, "Say it with me. Polar bear hair is clear!", part=1, q=True, tag="say it: clear", hide=["milo"], pcam=BBP, cam2=W(BB),
      fx=[("nod", "w:clear!", "bear")], words=[("w:Say", "SAY IT!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("paper_blue", (960, 580, 1700), "Quick check! Is one polar bear hair white, or clear?", part=1, q=True, tag="question 1b", cam2=(960, 580, 1500), pause=3.2, pcam=(960, 700, 1700),
      props=[LENS(960, 640, .6, p=(960, 840, .62))], fx=[PULSE("w:hair", "#{p}ln-hair", 1.05), ("signs", "w:white,", ["WHITE", "CLEAR"], 1, "wait:2.0"),
          ("word", "e:clear?", "?", {"x": 1600, "y": 470, "size": 200, "cls": "sun", "p": {"x": 1250, "y": 520, "size": 170}})]),
    S("arctic", BB, "Clear! See-through. Super job!", part=1, tag="super job 1", hide=["milo"], pcam=BBP, cam2=W(BB), fx=[("nod", "w:Super", "bear")],
      words=[("w:Clear!", "CLEAR!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- PART 2: hollow hairs, bouncing light
    S("arctic_low", LH, "Surprise number two! If the hairs are clear, why does Poppy look white?", part=2, q=True, tag="surprise 2", trans="iris", hide=["milo"], pcam=LHP, pcam2=W(LHP, 1.04), cam2=W(LH, 1.05),
      fx=[("lookat", "w:white?", "bear", 6)], words=[("w:two!", "2", .78, .2, 1.4, "sun", (.3, .3), 1.2), ("w:white?", "?", .2, .3, 2.0, "sun", (.7, .34), 1.3)]),
    S("arctic_low", (1000, 600, 1500), "Is she painted white? Or is it the light?", part=2, q=True, tag="question 2a", pause=3.2, hide=["milo"], pcam=(1000, 520, 1800),
      fx=[("signs", "w:painted", ["PAINT", "LIGHT"], 1, "wait:2.0")]),
    S("paper_blue", (960, 560, 1500), "It is the light! First, look inside a long hair. The middle is hollow. It is full of air!", part=2, tag="board: hollow hair", pcam=(960, 620, 1700), props=[TUBE()],
      fx=[BLINK("w:hollow.", "#{p}tb-core", 3, "the hollow middle blinks"), PULSE("w:air!", "#{p}tb-core", 1.05, 2)],
      words=[("w:hollow.", "HOLLOW!", .84, .12, 1.2, "sun", (.5, .31), 1.0), ("w:air!", "AIR!", .16, .5, 1.1, "sun", (.2, .55), .8)]),
    S("zoo", say="Hollow, like a straw! Pretend to sip with a straw. Sip, sip!", part=2, q=True, tag="sip a straw", pause=2.4,
      fx=[("hop", "w:Sip,", "milo"), ("hop", "e:sip!", "milo"), ("hop", "wait:1.2", "milo")],
      words=[("w:Sip,", "SIP, SIP!", .76, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("paper", (1000, 560, 1600), "When sunlight shines in, the light bounces all around. Count the sunbeams. One, two, three!", part=2, q=True, tag="board: sunbeams", pcam=(1000, 640, 1800),
      props=[BOUNCE()],
      fx=[("to", 0, "#{p}bo-in0,#{p}bo-in1,#{p}bo-in2,#{p}bo-out", {"opacity": 0, "duration": 0}, "the beams wait"),
          SHOW("w:sunlight", "#{p}bo-in0", "beam one comes in"), SHOW("w:shines", "#{p}bo-in1", "beam two comes in"), SHOW("w:bounces", "#{p}bo-in2", "beam three comes in"),
          BLINK("w:around.", "#{p}bo-t-core", 2, "the hollow middle blinks"),
          PULSE("w:One,", "#{p}bo-in0", 1.15, 1, "100% 100%"), PULSE("w:two,", "#{p}bo-in1", 1.15, 1, "100% 100%"), PULSE("w:three!", "#{p}bo-in2", 1.15, 1, "100% 100%")],
      words=[("w:One,", "1", .14, .2, 1.1, "sun", (.2, .31), 1.0), ("w:two,", "2", .14, .45, 1.1, "sun", (.5, .31), 1.0), ("w:three!", "3", .14, .7, 1.1, "sun", (.8, .31), 1.0)]),
    S("paper", (1000, 560, 1600), "All that bouncing light makes the fur look white. Like sparkly ice!", part=2, tag="board: looks white", pcam=(1000, 640, 1800), props=[BOUNCE()],
      fx=[PULSE("w:All", "#{p}bo-t", 1.05), SHOW("w:bouncing", "#{p}bo-out", "the light bounces out all round"), PULSE("w:white.", "#{p}bo-out", 1.12, 2), PULSE("w:sparkly", "#{p}bo-out", 1.12, 2)],
      words=[("w:white.", "WHITE!", .84, .12, 1.2, "sun", (.5, .31), 1.0)]),
    S("zoo", say="Wiggle your fingers, like bouncing sunlight. Bounce, bounce!", part=2, q=True, tag="bouncing fingers", pause=2.4,
      fx=[("hop", "w:Bounce,", "milo"), ("hop", "e:bounce!", "milo"), ("hop", "wait:1.2", "milo")],
      words=[("w:Bounce,", "BOUNCE!", .76, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("arctic_low", LB, "Clear hairs, full of air, look white in the sun!", part=2, tag="clear hairs look white", hide=["milo"], pcam=LBP, cam2=W(LB, 1.05),
      fx=[("nod", "w:white", "bear")], words=[("w:sun!", "SO WHITE!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("paper_blue", (960, 580, 1600), "Is the middle of a long hair full, or hollow?", part=2, q=True, tag="question 2c", pause=3.2, cam2=(960, 580, 1500), pcam=(960, 700, 1700),
      props=[TUBE(960, 700, .5, p=(960, 860, .55))], fx=[BLINK("w:middle", "#{p}tb-core", 2), ("signs", "w:full,", ["FULL", "HOLLOW"], 1, "wait:2.0")]),
    S("arctic_low", LB, "Hollow! The middle is full of air.", part=2, tag="hollow answer", hide=["milo"], pcam=LBP, cam2=W(LB, 1.05),
      fx=[("nod", "w:Hollow!", "bear")], words=[("w:Hollow!", "HOLLOW!", .26, .34, 1.2, "sun", (.5, .34), 1.0)]),
    S("zoo", say="Puff your cheeks, full of air, like a hollow hair. Puff!", part=2, q=True, tag="puff your cheeks", pause=2.4,
      fx=[("to", "e:Puff!", "#{p}milo", {"scale": 1.12, "transformOrigin": "50% 100%", "duration": .25, "yoyo": True, "repeat": 3}, "Milo puffs up"), ("hop", "wait:1.2", "milo")],
      words=[("e:Puff!", "PUFF!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("arctic", BB, "In the sunshine, look how white Poppy looks!", part=2, tag="sun on Poppy", hide=["milo"], pcam=BBP, cam2=W(BB, 1.05),
      fx=[("hop", "w:sunshine,", "bear"), ("nod", "w:looks!", "bear")], words=[("w:sunshine,", "SUNNY!", .26, .34, 1.2, "sun", (.5, .34), 1.0)]),
    S("arctic_low", LB, "Clear hairs, but bright white fur. What a surprise!", part=2, tag="what a surprise 2", hide=["milo"], pcam=LBP, cam2=W(LB, 1.05),
      fx=[("hop", "w:surprise!", "bear")], words=[("w:surprise!", "SURPRISE!", .26, .34, 1.0, "sun", (.5, .34), .9)]),
    S("arctic_low", LB, "Say it with me. The light makes polar bear fur look white!", part=2, q=True, tag="say it: the light", hide=["milo"], pcam=LBP, cam2=W(LB),
      fx=[("nod", "w:light", "bear")], words=[("w:Say", "SAY IT!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("paper_blue", (960, 580, 1700), "Quick check! What is inside a long polar bear hair? Air, or water?", part=2, q=True, tag="question 2b", cam2=(960, 580, 1500), pause=3.2, pcam=(960, 700, 1700),
      props=[TUBE(960, 700, .5, p=(960, 860, .55))], fx=[BLINK("w:inside", "#{p}tb-core", 2), ("signs", "w:Air,", ["AIR", "WATER"], 0, "wait:2.0"),
          ("word", "e:water?", "?", {"x": 1600, "y": 470, "size": 200, "cls": "sun", "p": {"x": 1250, "y": 520, "size": 170}})]),
    S("arctic_low", LB, "Air! Great job!", part=2, tag="great job 2", hide=["milo"], pcam=LBP, cam2=W(LB), fx=[("nod", "w:Great", "bear")],
      words=[("w:Air!", "AIR!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- PART 3: black skin
    S("arctic_eve", EH, "Surprise number three! What color is the skin, under Poppy's fur?", part=3, q=True, tag="surprise 3", trans="iris", hide=["milo"], pcam=EHP, pcam2=W(EHP, 1.04), cam2=W(EH, 1.05),
      fx=[("lookat", "w:skin,", "bear", 8)], words=[("w:three!", "3", .78, .2, 1.4, "sun", (.3, .3), 1.2), ("w:fur?", "?", .2, .3, 2.0, "sun", (.7, .34), 1.3)]),
    S("arctic_eve", (1000, 600, 1500), "Is it pink? Or black?", part=3, q=True, tag="question 3a", pause=3.2, hide=["milo"], pcam=(1000, 520, 1800),
      fx=[("signs", "w:pink?", ["PINK", "BLACK"], 1, "wait:2.0")]),
    S("paper_pink", (960, 560, 1500), "Black! Under the clear fur, a polar bear has black skin.", part=3, tag="board: black skin", pcam=(960, 620, 1700), props=[SKIN()],
      fx=[("to", 0, "#{p}sk-rays", {"opacity": 0, "duration": 0}, "the beams wait"), BLINK("w:black:2", "#{p}sk-skin", 3, "the black skin blinks")],
      words=[("w:Black!", "BLACK!", .84, .1, 1.2, "sun", (.5, .31), 1.0)]),
    S("arctic", BH, "And look at Poppy's nose. It is black too!", part=3, tag="black nose", hide=["milo"], pcam=BHP, cam2=W(BH, 1.06),
      fx=[("nod", "w:nose.", "bear"), ("nod", "w:too!", "bear")], words=[("w:black", "BLACK NOSE!", .26, .3, 1.0, "sun", (.5, .32), .85)]),
    S("zoo", say="Can you touch your nose? Boop!", part=3, q=True, tag="boop your nose", pause=2.4,
      fx=[("hop", "e:Boop!", "milo"), ("hop", "wait:1.2", "milo")], words=[("e:Boop!", "BOOP!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("paper_pink", (960, 560, 1500), "Sunlight shines through the clear fur, all the way down to the black skin.", part=3, tag="board: light to the skin", pcam=(960, 620, 1700), props=[SKIN()],
      fx=[("to", 0, "#{p}sk-rays", {"opacity": 0, "duration": 0}, "the beams wait"), PULSE("w:Sunlight", "#{p}sk-sun", 1.15, 2), SHOW("w:shines", "#{p}sk-rays", "the sunbeams go through the clear fur"),
          BLINK("w:black", "#{p}sk-skin", 2, "the black skin blinks")],
      words=[("w:through", "THROUGH!", .84, .1, 1.1, "sun", (.5, .31), .9)]),
    S("paper_pink", (960, 560, 1500), "The black skin soaks up the sun's warmth, and warms the bear!", part=3, tag="board: skin warms", pcam=(960, 620, 1700), props=[SKIN()],
      fx=[SHOW("w:soaks", "#{p}sk-warm", "a warm glow along the skin"), PULSE("w:warms", "#{p}sk-warm", 1.04, 2)],
      words=[("w:warms", "WARM!", .84, .1, 1.2, "sun", (.5, .31), 1.0)]),
    S("paper_pink", (960, 600, 1600), "Can the sunlight get through the clear fur, to the skin? Yes, or no?", part=3, q=True, tag="question 3c", pause=3.2, cam2=(960, 600, 1500), pcam=(960, 720, 1700),
      props=[SKIN(960, 700, .7, p=(960, 860, .7))], fx=[PULSE("w:sunlight", "#{p}sk-sun", 1.15), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("arctic_eve", EB, "Yes! Right through the clear fur.", part=3, tag="yes through", hide=["milo"], pcam=EBP, cam2=W(EB, 1.05),
      fx=[("nod", "w:Yes!", "bear")], words=[("w:Yes!", "YES!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("zoo", say="Stretch up high, to the warm sun. Stretch!", part=3, q=True, tag="stretch to the sun", pause=2.4,
      fx=[("hop", "e:Stretch!:2", "milo"), ("hop", "wait:1.2", "milo")], words=[("e:Stretch!:2", "STRETCH!", .76, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("arctic", BB, "Clear fur and black skin. Poppy is cozy in the sun!", part=3, tag="cozy in the sun", hide=["milo"], pcam=BBP, cam2=W(BB, 1.05),
      fx=[("nod", "w:cozy", "bear")], words=[("w:cozy", "COZY!", .26, .34, 1.2, "sun", (.5, .34), 1.0)]),
    S("arctic_eve", EB, "Black skin, under clear fur. What a surprise!", part=3, tag="what a surprise 3", hide=["milo"], pcam=EBP, cam2=W(EB, 1.05),
      fx=[("hop", "w:surprise!", "bear")], words=[("w:surprise!", "SURPRISE!", .26, .34, 1.0, "sun", (.5, .34), .9)]),
    S("zoo", say="Rub your hands together, in the warm sun. Warm, warm!", part=3, q=True, tag="rub your hands", pause=2.4,
      fx=[("hop", "w:Warm,", "milo"), ("hop", "e:warm!:2", "milo"), ("hop", "wait:1.2", "milo")],
      words=[("w:Warm,", "WARM!", .76, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("paper", (960, 600, 1500), "Sometimes the fur looks bright white. And in summer, it can look a little yellow!", part=3, tag="board: white and yellow", pcam=(960, 660, 1800), props=[SWATCH()],
      fx=[PULSE("w:white.", "#{p}sw-white", 1.06, 2), PULSE("w:yellow!", "#{p}sw-yellow", 1.06, 2)],
      words=[("w:yellow!", "YELLOW!", .74, .1, 1.0, "sun", (.5, .31), .9)]),
    S("arctic_eve", EB, "Say it with me. Under the fur, a polar bear has black skin!", part=3, q=True, tag="say it: black skin", hide=["milo"], pcam=EBP, cam2=W(EB),
      fx=[("nod", "w:black", "bear")], words=[("w:Say", "SAY IT!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("arctic", (1000, 600, 1500), "Quick check! What color is a polar bear's nose? Black, or orange?", part=3, q=True, tag="question 3b", pause=3.2, hide=["milo"], pcam=(1000, 520, 1800),
      fx=[("nod", "w:nose?", "bear"), ("signs", "w:Black,", ["BLACK", "ORANGE"], 0, "wait:2.0")]),
    S("arctic", BB, "Black! You remembered!", part=3, tag="you remembered", hide=["milo"], pcam=BBP, cam2=W(BB), fx=[("nod", "w:remembered!", "bear")],
      words=[("w:Black!", "BLACK!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- QUIZ
    S("zoo_eve", WIDE, "Three surprises! Now it is quiz time!", part=4, trans="iris", tag="quiz time", cam2=(960, 560, 1860), pcam=(960, 560, 1800),
      words=[("w:quiz", "QUIZ TIME!", .5, .3, 1.3, "sun", (.5, .33))], fx=[("hop", "w:quiz", "milo", 2)]),
    S("paper_blue", (960, 600, 1600), "Is one polar bear hair white, or clear?", part=4, q=True, tag="quiz 1", pause=3.2, cam2=(960, 600, 1500), pcam=(960, 700, 1700),
      props=[LENS(960, 640, .6, p=(960, 840, .62))], fx=[PULSE("w:hair", "#{p}ln-hair", 1.05), ("signs", "w:white,", ["WHITE", "CLEAR"], 1, "wait:2.0")]),
    S("arctic", BB, "Clear! See-through hairs.", part=4, tag="quiz 1: clear", hide=["milo"], pcam=BBP, cam2=W(BB), fx=[("nod", "w:Clear!", "bear")],
      words=[("w:Clear!", "CLEAR!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("arctic_low", (1000, 600, 1500), "What makes the fur look white? The light, or paint?", part=4, q=True, tag="quiz 2", pause=3.2, hide=["milo"], pcam=(1000, 520, 1800),
      fx=[("signs", "w:light,", ["LIGHT", "PAINT"], 0, "wait:2.0")]),
    S("arctic_low", LB, "The light! Bouncing all around.", part=4, tag="quiz 2: light", hide=["milo"], pcam=LBP, cam2=W(LB), fx=[("hop", "w:light!", "bear")],
      words=[("w:light!", "LIGHT!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("paper_pink", (960, 600, 1600), "What color is the skin, under the fur? Black, or pink?", part=4, q=True, tag="quiz 3", pause=3.2, cam2=(960, 600, 1500), pcam=(960, 720, 1700),
      props=[SKIN(960, 700, .7, p=(960, 860, .7))], fx=[BLINK("w:skin,", "#{p}sk-skin", 2), ("signs", "w:Black,", ["BLACK", "PINK"], 0, "wait:2.0")]),
    S("arctic_eve", EB, "Black skin! Warm in the sun.", part=4, tag="quiz 3: black", hide=["milo"], pcam=EBP, cam2=W(EB), fx=[("nod", "w:Black", "bear")],
      words=[("w:Black", "BLACK!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- RECAP + GOODBYE
    S("paper_blue", (960, 600, 1900), "Clear hairs, bouncing light, and black skin. You found all three surprises!", part=4, trans="iris", tag="recap: three surprises", pcam=(960, 640, 2500), cam2=(960, 600, 1960),
      props=[LENS(400, 560, .5, p=(540, 300, .5)), BOUNCE(980, 560, .5, p=(540, 650, .5)), SKIN(1540, 560, .5, p=(540, 1000, .55))],
      fx=[PULSE("w:Clear", "#{p}ln_w", 1.08), PULSE("w:bouncing", "#{p}bo_w", 1.08), PULSE("w:black", "#{p}sk_w", 1.08)],
      words=[("w:found", "YOU DID IT!", .5, .14, 1.0, "sun", (.5, .1), .85)]),
    S("zoo_eve", say="Make your magnifying glass, sip your straw, and boop your nose!", part=4, q=True, tag="all three moves", pause=1.6,
      fx=[("hop", "w:Make", "milo"), ("hop", "w:sip", "milo"), ("hop", "w:boop", "milo")],
      words=[("w:boop", "BOOP!", .76, .3, .9, "sun", (.5, .33), .8)], **MILO("zoo_eve", 940)),
    S("arctic_eve", (960, 600, 1700), "Clear fur, black skin, and a big warm smile. Bye-bye, friends!", part=4, tag="goodbye", hide=["milo"], pcam=EBP, cam2=(960, 600, 1760),
      fx=[("nod", "w:smile.", "bear")], words=[("w:Bye-bye,", "BYE-BYE!", .2, .36, 1.0, "pill", (.5, .38), .8)]),
    *intro_shots(),      # the main intro again as the last shots (owner, Nov 20 4:50 PM)
]
for _s in SHOTS:        # a picture board never drifts closer: it only pulls out a little (16:9 and 9:16)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)

SHORTS = [
    {"id": "zc_ep15_short1", "title": "What Color Is One Polar Bear Hair?", "band": ("ONE BEAR", "HAIR?"), "thumb_text": "LOOK!", "part": 1,
     "extra_first": [S("arctic", BH, "Look very closely! What color is one polar bear hair?", part=1, q=True, tag="hook: one hair", hide=["milo"], pcam=(BHP[0], BHP[1], 1050), pcam2=(BHP[0], BHP[1], 1130), cam2=W(BH, 1.05),
                       props=[SNOW()], fx=[FALL(0, 5.0), ("lookat", "w:closely!", "bear", 6)], words=[("w:hair?", "?", .78, .3, 2.0, "sun", (.5, .34), 1.3)])]},
    {"id": "zc_ep15_short2", "title": "Why Does a Polar Bear Look White?", "band": ("WHY SO", "BRIGHT?"), "thumb_text": "SIP, SIP!", "part": 2,
     "extra_first": [S("arctic_low", LB, "The hairs are clear. So why does a polar bear look white?", part=2, q=True, tag="hook: why white", hide=["milo"], pcam=LBP, pcam2=W(LBP, 1.06), cam2=W(LB, 1.05),
                       fx=[("nod", "w:clear.", "bear")], words=[("w:white?", "?", .26, .3, 2.0, "sun", (.5, .34), 1.3)])]},
    {"id": "zc_ep15_short3", "title": "What Color Is a Polar Bear's Skin?", "band": ("UNDER THE", "FUR?"), "thumb_text": "BOOP!", "part": 3,
     "extra_first": [S("arctic_eve", EH, "Under all that fluffy fur, what color is a polar bear's skin?", part=3, q=True, tag="hook: skin color", hide=["milo"], pcam=EHP, pcam2=W(EHP, 1.05), cam2=W(EH, 1.05),
                       fx=[("lookat", "w:fur,", "bear", 6)], words=[("w:skin?", "?", .2, .3, 2.0, "sun", (.5, .34), 1.3)])]},
]

# thumbnails (thumb.py): one big object, 1-2 words, none of the title's words, no watermark
THUMBS = {
    "zc_ep15": {"place": "paper_blue", "cam": (960, 600, 1500), "props": [(A.lens_hair, 860, 600, .8)], "words": [("SEE-THROUGH?!", 960, 140, 160, "sun")]},
    "zc_ep15_short1": {"place": "paper_blue", "cam": (960, 640, 1700), "props": [(A.lens_hair, 960, 520, 1.1)], "words": [("LOOK!", 540, 1560, 240, "sun")]},
    "zc_ep15_short2": {"place": "paper_blue", "cam": (960, 600, 1900), "props": [(A.hair_tube, 960, 520, 1.0)], "words": [("SIP,", 540, 1400, 210, ""), ("SIP!", 540, 1630, 240, "sun")]},
    "zc_ep15_short3": {"place": "arctic", "cam": (1080, 720, 1350), "actors": [("bear", 1000, 930, 1.0, False, "")], "words": [("BOOP!", 540, 1600, 240, "sun")]},
}
