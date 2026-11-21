"""zc_ep10: "One Hump or Two? Meet the Camels" - cartoon fact lesson with Milo, Sandy the baby camel, her Mama (one hump) and Sandy's two-humped
camel cousin in the Gobi (3D music-and-sync process: "beat"). Milo visits Sandy's cousin in the snow. Three parts, each cut whole into one Short:
1. one hump or two (a dromedary has one hump, a Bactrian camel two, like the letter B; dromedaries are taller with longer legs, Bactrians shorter and heavier),
2. where they live (dromedaries: hot, dry deserts; Bactrian camels: the rocky Gobi Desert in Asia, very cold in winter with snow, hot in summer),
3. coats (a dromedary's coat is short and light; a Bactrian camel grows a thick, shaggy coat for winter that keeps it warm, and sheds it in big patches in spring).
Not what is inside the hump, eyelashes, nose, feet, drinking, food or chewing: those are in the live zc_ep01 and zc_ep09 and their Shorts.

FACTS, read at the source on Nov 20 2026, about 2:10-2:30 AM ET (each page fetched by the session's page reader, which quotes the sentences it finds;
three pages could not be read this session and nothing is taken from them: animals.sandiegozoo.org camel page, SeaWorld dromedary, National Geographic Arabian camel URL):
 [NGK] National Geographic Kids, "Bactrian camel", kids.nationalgeographic.com/animals/mammals/facts/bactrian-camel
   "Bactrian camels have two humps on their backs where they store fat."   "Arabian camels, called dromedaries, have only one hump"
   "Bactrian camels live in Central and East Asia's rocky deserts where it gets very cold in the winter and hot in the summer."
   "In the Gobi, Bactrian camels gather together around mountain areas where snow and springs provide water in the winter."
 [NG] National Geographic, "Bactrian camel", nationalgeographic.com/animals/mammals/facts/bactrian-camel
   "Bactrian camels have two humps rather than the single hump of their Arabian relatives."   "...live not in shifting Sahara sands but in Central and East Asia's rocky deserts."
   "Yet they can also drop to -20F in winter."   "One is a thick, shaggy coat that protects them in winter and falls away as seasons change and temperatures rise."
   "These herds survive in the Gobi Desert of Mongolia and China."
 [LPZ] Lincoln Park Zoo, "Bactrian camel", go.lpzoo.org/animals/bactrian-camel
   "Bactrian camels are large, desert-dwelling animals with two dorsal humps."   "... the Gobi Desert in Central Asia with thick, shaggy coats that shed in patches in the spring."
 [DZ] Denver Zoo, "Bactrian camel", denverzoo.org/animals/bactrian-camel
   "Bactrian camels have two humps - like the letter "B"."   "Bactrian camels are shorter and heavier than the one-humped dromedary camels found in Africa and the Middle East."
   "They have thick, wooly coats that provide warmth during the cold months"   "they shed this for the summer months."   "Their fur color varies from beige to dark brown."
 [BZ] Brookfield Zoo, "Bactrian camel", brookfieldzoo.org/bactriancamel
   "Bactrian camels are large, two-humped camels."   "They grow a dense winter coat and shed it in large raggedy patches during the spring and summer months."
   "Geographic Distribution: Western China, Gobi Desert, and Mongolia"
 [SDZG] San Diego Zoo Wildlife Alliance Library fact sheet "Camels: Summary", ielc.libguides.com/sdzg/factsheets/extantcamels/summary
   "Dromedary Camels have one hump, a more smaller frame, and longer, more slender legs than Bactrian Camels."   "Dromedary: hot, arid desert regions of Africa, the Middle East, and Australia"
   "Dromedary: short, light-colored coat"   "Their hair is also lighter and shorter."   shoulder height: Bactrian 160-180 cm, Dromedary 180-200 cm.
 [OZ] Oakland Zoo, "Dromedary camel", oaklandzoo.org/animals/dromedary-camel   "The Arabian camel, or dromedary, has one back hump,"   "...protect them from the hot sand when bending down."
 [PBS] PBS Nature, "Camel Fact Sheet"   "While the dromedary camel has one hump, the Bactrian camel has two humps."   "Camels typically live in deserts, where it is hot and dry."
 [SYD] Sydney Zoo, "Dromedary camel"   "...easily identified by its single distinctive hump, in contrast to its Bactrian cousin which has two."
 Said as: a camel with one hump is a dromedary [NGK, OZ, PBS]; a camel with two humps is a Bactrian camel [NGK, NG, PBS]; two humps like the letter B [DZ];
 the two-humped camel is the dromedary's camel cousin [SYD]; dromedaries are taller, with longer legs [SDZG]; Bactrian camels are shorter and heavier [DZ];
 dromedaries live in hot, dry deserts [SDZG, PBS]; the sand is hot [OZ]; Bactrian camels live in the Gobi Desert, far away in Asia [NG, BZ]; it is a rocky desert [NGK, NG];
 in winter it gets very, very cold [NGK, NG]; in winter there is snow [NGK]; in summer it gets hot [NGK, NG]; a dromedary's coat is short and light [SDZG];
 Bactrian camels grow a thick, shaggy coat for winter [NG, LPZ, BZ]; it keeps them warm [DZ]; in spring the coat falls off in big, shaggy patches [LPZ, BZ, NG];
 that is called shedding [LPZ, BZ, DZ]; then the coat is thinner for summer [DZ]; a new thick coat grows for the next winter [BZ "They grow a dense winter coat"].
 Read but NOT said: fat in the humps (zc_ep01's topic), weights and heights in numbers, -20F, wild camels and how few are left, Australia, Mongolia and China by name,
 water, eyelashes, feet. "Cousin" is said as a camel cousin, the word Sydney Zoo uses; Sandy and the cousin are the frame, not facts.
 The frame: Milo flies to visit Sandy's cousin; nobody is hurt, lost, crying or trapped; the cold is a cosy "Brrr!", the cousin is warm in her coat.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_zc_ep10 as A
from kit import Kit, S, prop, W

EP = {"id": "zc_ep10", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "One Hump or Two? Meet the Camels", "thumb_text": "COUSINS?!", "series": "Animal Facts with Milo",
      "description": ("One hump or two? Milo the bluebird flies far away to the snowy Gobi Desert to meet Sandy the baby camel's two-humped camel cousin! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn that a camel with one hump is a dromedary and a camel with two humps is a Bactrian camel (two humps, like the letter B), "
                      "that dromedaries are taller and live in hot, dry deserts, that Bactrian camels live in the rocky Gobi Desert, where winters are very cold and snowy, "
                      "and that Bactrian camels grow a thick, shaggy coat for winter and shed it in big patches in spring.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNational Geographic Kids (Bactrian camel); National Geographic (Bactrian camel); San Diego Zoo Wildlife Alliance Library (camels fact sheet); "
                      "Lincoln Park Zoo, Denver Zoo and Brookfield Zoo (Bactrian camel); Oakland Zoo and Sydney Zoo (dromedary camel); PBS Nature (camel fact sheet)."),
      "tags": ["one hump or two", "bactrian camel", "dromedary", "camels for kids", "two humps", "baby camel", "Gobi desert", "desert animals for kids",
               "animal facts for kids", "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "zoo": [("milo", "milo", 960, 940, 1.1)],
    "dunes": [("mama", "camel", 1330, 905, .95), ("sandy", "calf", 620, 935, .56), ("milo", "milo", 300, 520, .75, False, True)],
    "trail": [("mama", "camel", 1330, 900, .95), ("sandy", "calf", 590, 930, .54), ("milo", "milo", 300, 500, .75, False, True)],
    "gobi": [("bac", "bac_winter", 1150, 920, .95), ("milo", "milo", 380, 560, .78, False, True)],
    "gobi_spring": [("bac", "bac_winter", 1150, 920, .95), ("milo", "milo", 380, 560, .78, False, True)],
    "oasis": [("mama", "camel", 1150, 880, .9), ("sandy", "calf", 400, 915, .52), ("milo", "milo", 1640, 520, .72, True, True)],
    "night": [("mama", "camel", 1260, 905, .95), ("sandy", "calf", 680, 935, .54), ("milo", "milo", 290, 892, .8, False, False)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 1100, 0, -90))
BOARD = (960, 540, 1500); BOARDP = (960, 440, 1700)
SNOW = lambda: prop("snow", art.snow, 0, 0, 1.0)
def FALL(at, d=6.0): return ("fromto", 0 if at is None else at, ".{p}snow-f", {"y": -60}, {"y": 220, "duration": d, "ease": "none"}, "snow falls")

# the cousin in the Gobi
GB = C("gobi", "bac", "body", 1300, 40, -120); GBP = WV("gobi", ["bac"], floor=.72, top=.42, pad=.1)
GH = C("gobi", "bac", "hump", 1000, 0, 20); GHP = WV("gobi", ["bac"], floor=.68, top=.40, pad=.04)
GQ = (1060, 480, 1920); GQP = WV("gobi", ["bac"], floor=.74, top=.46, pad=.1)
GC = C("gobi", "bac", "body", 1150, 60, -90); GCP = WV("gobi", ["bac"], floor=.7, top=.38, pad=.03)          # close on the shaggy coat
SPB = C("gobi_spring", "bac", "body", 1300, 40, -120); SPBP = WV("gobi_spring", ["bac"], floor=.72, top=.42, pad=.1)
SPC = C("gobi_spring", "bac", "body", 1400, 60, -60); SPCP = WV("gobi_spring", ["bac"], floor=.7, top=.38, pad=.12)
SPQ = (1060, 480, 1920); SPQP = WV("gobi_spring", ["bac"], floor=.74, top=.46, pad=.1)
SPW = (1100, 640, 1700); SPWP = (1100, 600, 1900)      # the camel and the patches on the ground
# Mama and Sandy on the dunes
MH = C("dunes", "mama", "hump", 1000, 60, 10); MHP = V("dunes", "mama", "hump", 1400, 120)
DQ = (1000, 520, 1920); DQP = WV("dunes", ["sandy", "mama"], floor=.72, top=.46)
DMS = WV("dunes", ["sandy", "mama"], floor=.72, top=.42)
TR = (1000, 560, 1800); TRP = WV("trail", ["sandy", "mama"], floor=.72, top=.42)
OSM = C("oasis", "mama", "body", 1150, 60, -60); OSMP = WV("oasis", ["mama"], floor=.72, top=.42, pad=.1)

# the cousin's coat: patches fall to the ground, one by one (patch k lands at y = -its y in the camel's units)
def _land(k): return {"x": A.LAND[k] - A.PATCHES[k][0], "y": -A.PATCHES[k][1] - 12, "rotation": 14 if k % 2 else -12}
def SHED(at, k, d=0.9): return ("to", at, f"#{{p}}bac-sh{k}", dict(_land(k), duration=d, ease="power2.in"), "a patch of the coat falls off")
def SHED_DONE(ks): return [("to", 0, f"#{{p}}bac-sh{k}", dict(_land(k), duration=.01), "") for k in ks]

# pictures on the boards
DROM = lambda name, x, y, s, hidden=False, p=None: prop(name, lambda q: art.camel(q, 1), x, y, s, hidden, p)
BAC = lambda name, x, y, s, hidden=False, p=None: prop(name, A.bactrian_winter, x, y, s, hidden, p)
BACS = lambda name, x, y, s, hidden=False, p=None: prop(name, A.bactrian_summer, x, y, s, hidden, p)
PAIR = lambda hid=(), tall=True: [DROM("d1", 620, 900, .62, "d1" in hid), prop("b2", A.bactrian_short, 1300, 900, .62, "b2" in hid)]      # 9:16: the same, side by side, with PAIRP
PAIRP = (1020, 660, 2300)      # 9:16: the two side by side, to compare how tall they are
def PULSE(at, sel, k=1.2, n=1, o="50% 50%"): return ("to", at, sel, {"scale": k, "transformOrigin": o, "duration": .2, "yoyo": True, "repeat": 2 * n - 1}, "")
def HUMP(at, who, n=1): return ("to", at, f"#{{p}}{who}-hump", {"scaleY": 1.12, "svgOrigin": "0 -372", "duration": .2, "yoyo": True, "repeat": 2 * n - 1}, "the hump bounces")
ICONS = lambda new=(): [prop("ic0", A.snowflake, 700, 560, 1.0, "ic0" in new, p=(960, 180, .8)), prop("ic1", A.sun_disc, 1220, 560, 1.0, "ic1" in new, p=(960, 620, .8))]

SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("gobi", GH, "Look at this camel! One hump, two humps!", q=True, tag="hook: two humps", pcam=GHP, props=[SNOW()], fx=[FALL(0), HUMP("w:One", "bac"), HUMP("w:two", "bac")],
      words=[("w:One", "1", .3, .3, 1.6, "sun", (.3, .38), 1.2), ("w:two", "2", .7, .3, 1.6, "sun", (.7, .38), 1.2)]),
    S("paper_pink", BOARD, "Why do some camels have one hump, and some have two?", q=True, tag="hook: one or two", pcam=PAIRP, props=PAIR(("b2",)),
      fx=[HUMP("w:one", "d1"), ("show", "w:two?", "b2")], words=[("w:Why", "?", .5, .16, 1.6, "sun", (.5, .3), 1.2)]),
    S("gobi", say="I'm Milo. Let's meet the camels!", tag="hook: Milo", hide=["bac"], props=[SNOW()], fx=[FALL(0, 4), ("hop", "w:meet", "milo")], **MILO("gobi")),
    # ---------------------------------------------------------------- INTRO
    S("zoo", WIDE, "Welcome to The Animated Zoo, friends!", trans="iris", tag="gate wide", words=[("w:Animated", "HELLO!", .74, .6, 1.2, "pill")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, -40), "Today we meet two kinds of camels!", tag="Milo close", words=[("w:two", "2 KINDS", .5, .16, 1.1, "sun")]),
    S("dunes", WIDE, "First, the hot, sandy desert. Hello, Sandy! Hello, Mama!", trans="iris", tag="dunes wide", cam2=(1000, 560, 1780), pcam=DMS, pcam2=W(DMS),
      fx=[("fromto", 0, "#{p}milo_w", {"x": -200, "y": 300}, {"x": 300, "y": 520, "duration": 1.6, "ease": "power2.out"}, "Milo flies in"), ("hop", "w:Sandy!:2", "sandy"), ("nod", "w:Mama!", "mama")],
      words=[("w:hot,", "HOT!", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    # ---------------------------------------------------------------- PART 1: one hump or two
    S("dunes", MH, "Look at Mama's back. Let's count her humps.", part=1, q=True, tag="Mama's back", hide=["sandy", "milo"], pcam=MHP, cam2=C("dunes", "mama", "hump", 900, 40, 0),
      words=[("w:count", "COUNT!", .2, .3, 1.2, "sun", (.5, .3), 1.0)]),
    S("dunes", C("dunes", "mama", "hump", 1100, 60, 20), "One! Mama has one hump.", part=1, tag="one hump", hide=["sandy", "milo"], pcam=MHP, fx=[HUMP("w:One!:1", "mama"), HUMP("w:one:2", "mama")],
      words=[("w:One!:1", "1", .2, .28, 2.2, "sun", (.22, .4), 1.4)]),
    S("paper", BOARD, "A camel with one hump is called a dromedary.", part=1, tag="board: dromedary", pcam=BOARDP, props=[DROM("d1", 900, 900, .9, p=(960, 820, .62))],
      fx=[HUMP("w:one", "d1")], words=[("w:dromedary.", "DROMEDARY", .5, .14, 1.0, "sun", (.5, .3), .8), ("w:one", "1", .28, .36, 1.3, "", (.3, .4), 1.0)]),
    S("paper", (960, 520, 1400), "Say it with me. Dromedary!", part=1, q=True, tag="board: say dromedary", pcam=BOARDP, props=[DROM("d1", 900, 900, .9, p=(960, 820, .62))],
      fx=[("nod", "w:Dromedary!", "d1")], words=[("w:Say", "SAY IT!", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    S("dunes", DQ, "Does Sandy's mama have one hump, or two humps?", part=1, q=True, tag="question 1a", pause=3.2, hide=["milo"], pcam=DQP,
      fx=[("signs", "w:one", ["ONE", "TWO"], 0, "wait:2.0"), HUMP("wait:2.05", "mama", 2)]),
    S("dunes", MH, "One! Mama is a dromedary.", part=1, tag="Mama is a dromedary", hide=["sandy", "milo"], pcam=MHP, fx=[HUMP("w:One!", "mama", 2)],
      words=[("w:dromedary.", "DROMEDARY!", .33, .26, 1.0, "sun", (.5, .34), .8)]),
    S("dunes", say="Now let's fly far away, to Sandy's camel cousin!", part=1, tag="fly away", hide=["mama", "sandy"], fx=[("fly", "w:fly", "milo", 250, 505, 1.6)],
      words=[("w:cousin!", "COUSIN!", .77, .2, .9, "sun", (.5, .33), .85)], **MILO("dunes")),
    S("gobi", WIDE, "Oh! It is so cold here. This is the Gobi Desert.", part=1, trans="iris", tag="Gobi wide", cam2=(1000, 560, 1800), pcam=GBP, pcam2=W(GBP), props=[SNOW()],
      fx=[FALL(0), ("fromto", 0, "#{p}milo_w", {"x": -200, "y": 260}, {"x": 380, "y": 560, "duration": 1.6, "ease": "power2.out"}, "Milo flies in")],
      words=[("w:cold", "BRRR!", .5, .14, 1.3, "", (.5, .3), 1.0), ("w:Gobi", "THE GOBI", .5, .26, .9, "sun", (.5, .4), .8)]),
    S("gobi", GB, "And here is Sandy's cousin. Look at her back!", part=1, tag="the cousin", hide=["milo"], pcam=GBP, props=[SNOW()], fx=[FALL(0), ("nod", "w:cousin.", "bac")]),
    S("gobi", GQ, "How many humps does she have? One, or two?", part=1, q=True, tag="question 1", pause=3.2, hide=["milo"], pcam=GQP, props=[SNOW()],
      fx=[FALL(0, 8), ("signs", "w:One,", ["ONE", "TWO"], 1, "wait:2.0"), HUMP("wait:2.05", "bac", 2)]),
    S("gobi", GH, "Two! One hump, two humps.", part=1, q=True, tag="count two", pcam=GHP, props=[SNOW()], fx=[FALL(0, 4), HUMP("w:One", "bac"), HUMP("w:two:2", "bac")],
      words=[("w:One", "1", .3, .3, 1.6, "sun", (.3, .38), 1.2), ("w:two:2", "2", .7, .3, 1.6, "sun", (.7, .38), 1.2)]),
    S("paper_blue", BOARD, "A camel with two humps is called a Bactrian camel.", part=1, tag="board: Bactrian", pcam=BOARDP, props=[BAC("b2", 900, 900, .9, p=(960, 820, .62))],
      fx=[HUMP("w:two", "b2")], words=[("w:Bactrian", "BACTRIAN", .5, .14, 1.0, "sun", (.5, .3), .8)]),
    S("paper_blue", (960, 520, 1400), "Say it with me. Bactrian!", part=1, q=True, tag="board: say Bactrian", pcam=BOARDP, props=[BAC("b2", 900, 900, .9, p=(960, 820, .62))],
      fx=[("nod", "w:Bactrian!", "b2")], words=[("w:Say", "SAY IT!", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    S("paper_blue", BOARD, "Look at the letter B. It has two bumps!", part=1, tag="board: letter B", pcam=BOARDP,
      props=[prop("lb", A.letter_b, 960, 560, 1.0, p=(960, 520, .9))],
      fx=[PULSE("w:B.", "#{p}lb_w"), ("to", "w:bumps!", "#{p}lb_w", {"rotation": -90, "transformOrigin": "50% 50%", "duration": .7, "ease": "back.out(1.6)"}, "the B turns: two bumps up")]),
    S("paper_blue", BOARD, "B for Bactrian. Two humps, like a B!", part=1, tag="board: B for Bactrian", pcam=BOARDP,
      props=[prop("lb", A.letter_b, 520, 520, .7, p=(960, 260, .6)), BAC("b2", 1220, 900, .72, p=(960, 950, .5))],
      fx=[("to", 0, "#{p}lb_w", {"rotation": -90, "transformOrigin": "50% 50%", "duration": .01}, ""), PULSE("w:B:1", "#{p}lb_w"), HUMP("w:humps,", "b2", 2)]),
    S("gobi", say="Make two humps with your hands. Bump, bump!", part=1, q=True, tag="bump bump", hide=["bac"], props=[SNOW()], fx=[FALL(0, 5), ("hop", "w:Bump,:1", "milo", 2)],
      words=[("w:Bump,:1", "BUMP, BUMP!", .77, .1, .8, "sun", (.5, .33), .85)], **MILO("gobi", 820)),
    S("paper", BOARD, "One hump, a dromedary. Two humps, a Bactrian!", part=1, tag="board: one and two", pcam=PAIRP, props=PAIR(("b2",)),
      fx=[HUMP("w:One", "d1"), ("show", "w:Two", "b2")], words=[("w:One", "1", .27, .16, 1.3, "sun", (.23, .36), 1.0), ("w:Two", "2", .73, .16, 1.3, "sun", (.76, .36), 1.0)]),
    S("paper", BOARD, "Which camel has two humps? The dromedary, or the Bactrian?", part=1, q=True, tag="question 1b", pause=3.2, pcam=PAIRP, props=PAIR(),
      fx=[("signs", "w:dromedary,", ["DROMEDARY", "BACTRIAN"], 1, "wait:2.0"), HUMP("wait:2.05", "b2", 2)]),
    S("paper", BOARD, "The Bactrian! Look, the dromedary is taller.", part=1, tag="board: taller", props=PAIR(tall=True) + [prop("hl", lambda q: A.height_line(q, 1260), 1090, 466, 1.0, True)], pcam=PAIRP, pcam2=W(PAIRP),
      fx=[("show", "w:taller.", "hl")], words=[("w:taller.", "TALLER!", .33, .26, 1.1, "sun", (.5, .32), .9)]),
    S("paper", (960, 620, 1350), "Dromedaries have longer legs.", part=1, tag="board: longer legs", pcam=PAIRP, pcam2=W(PAIRP), props=PAIR(tall=True),
      fx=[PULSE("w:longer", "#{p}d1-fl", 1.1, 1, "50% 0%"), PULSE("w:legs.", "#{p}d1-bl", 1.1, 1, "50% 0%")], words=[("w:longer", "LONG LEGS", .33, .26, 1.0, "sun", (.5, .32), .8)]),
    S("paper", (1400, 680, 880), "Bactrian camels are shorter, and heavier.", part=1, tag="board: heavier", pcam=(1360, 640, 1400), pcam2=(1360, 640, 1460), props=PAIR(tall=True),
      fx=[PULSE("w:heavier.", "#{p}b2_w", 1.08)], words=[("w:heavier.", "HEAVY!", .28, .22, 1.1, "sun", (.5, .3), .9)]),
    S("dunes", say="Stand up tall, like a dromedary. Tall, tall!", part=1, q=True, tag="stand tall", hide=["mama", "sandy"], fx=[("hop", "w:Tall,:1", "milo", 2)],
      words=[("w:Tall,:1", "TALL, TALL!", .77, .1, .8, "sun", (.5, .33), .85)], **MILO("dunes", 820)),
    S("paper_pink", BOARD, "One hump, or two? Now you know!", part=1, tag="board: now you know", pcam=PAIRP, props=PAIR(),
      fx=[HUMP("w:One", "d1"), HUMP("w:two?", "b2", 2)], words=[("w:know!", "YOU KNOW!", .5, .14, 1.0, "sun", (.5, .32), .85)]),
    # ---------------------------------------------------------------- PART 2: where they live
    S("dunes", WIDE, "Mama and Sandy live in a hot, dry desert.", part=2, trans="iris", tag="hot desert wide", cam2=(1000, 560, 1780), pcam=DMS, pcam2=W(DMS), hide=["milo"],
      words=[("w:hot,", "HOT AND DRY", .5, .14, 1.0, "sun", (.5, .3), .8)]),
    S("trail", TR, "The sun is hot. The sand is hot, too!", part=2, tag="hot sand", hide=["milo"], pcam=TRP, pcam2=W(TRP),
      fx=[("fromto", 0, "#{p}sun", {"scale": 1.0}, {"scale": 1.15, "transformOrigin": "50% 50%", "duration": .6, "yoyo": True, "repeat": 3}, "the sun glows"), ("walk", "w:sand", "sandy", 120, 1.6)],
      words=[("w:sun", "HOT SUN", .33, .26, 1.0, "sun", (.5, .3), .8), ("w:sand", "HOT SAND", .7, .14, 1.0, "sun", (.5, .4), .8)]),
    S("trail", say="Fan yourself, like it is hot. Phew!", part=2, q=True, tag="fan yourself", hide=["mama", "sandy"], fx=[("hop", "w:Phew!", "milo")],
      words=[("w:Phew!", "PHEW!", .77, .1, 1.0, "sun", (.5, .33), .9)], **MILO("trail", 820)),
    S("dunes", DQ, "Is Sandy's desert hot, or cold?", part=2, q=True, tag="question 2a", pause=3.2, hide=["milo"], pcam=DQP,
      fx=[("signs", "w:hot,", ["HOT", "COLD"], 0, "wait:2.0"), ("hop", "wait:2.05", "sandy")]),
    S("paper", BOARD, "Hot! Dromedaries live in hot, dry deserts.", part=2, tag="board: hot deserts", pcam=BOARDP,
      props=[DROM("d1", 760, 900, .8, p=(960, 900, .55)), prop("ic1", A.sun_disc, 1360, 420, 1.0, p=(960, 300, .8))],
      fx=[PULSE("w:hot,:2", "#{p}ic1_w")], words=[("w:Hot!:1", "HOT!", .78, .72, 1.2, "sun", (.5, .31), .9)]),
    S("gobi", WIDE, "But Sandy's cousin lives far away, in the Gobi Desert.", part=2, trans="iris", tag="Gobi again", cam2=(1000, 560, 1800), pcam=GBP, pcam2=W(GBP), hide=["milo"], props=[SNOW()],
      fx=[FALL(0, 7)], words=[("w:Gobi", "THE GOBI", .5, .14, 1.0, "sun", (.5, .3), .85)]),
    S("gobi", (700, 760, 1100), "It is a rocky desert, in Asia.", part=2, tag="rocky", hide=["milo", "bac"], pcam=(600, 640, 1300), props=[prop("rk", A.rocks, 520, 930, 1.0), prop("rk2", A.rocks, 960, 990, .7), SNOW()], fx=[FALL(0, 5)],
      words=[("w:rocky", "ROCKY!", .5, .14, 1.2, "sun", (.5, .3), .9)]),
    S("gobi", (1000, 400, 1500), "There are big mountains, with snow on top.", part=2, tag="snowy mountains", hide=["milo", "bac"], pcam=(760, 380, 1500), props=[SNOW()], fx=[FALL(0, 5)],
      words=[("w:mountains,", "MOUNTAINS", .5, .74, 1.0, "sun", (.5, .62), .8)]),
    S("gobi", say="Say it with me. Gobi!", part=2, q=True, tag="say Gobi", hide=["bac"], props=[SNOW()], fx=[FALL(0, 4), ("hop", "w:Gobi!", "milo")],
      words=[("w:Gobi!", "GOBI!", .77, .1, 1.0, "sun", (.5, .33), .9)], **MILO("gobi")),
    S("paper_blue", BOARD, "In winter, it gets very, very cold.", part=2, tag="board: very cold", pcam=BOARDP, props=[prop("ic0", A.snowflake, 960, 560, 1.4, p=(960, 520, 1.1))],
      fx=[PULSE("w:winter,", "#{p}ic0_w"), ("to", "w:cold.", "#{p}ic0_w", {"rotation": 60, "transformOrigin": "50% 50%", "duration": .8}, "the snowflake turns")],
      words=[("w:cold.", "COLD!", .5, .14, 1.2, "", (.5, .3), 1.0)]),
    S("paper_blue", BOARD, "Count the snowflakes with me. One, two, three!", part=2, q=True, tag="board: count snowflakes", pcam=BOARDP,
      props=[prop("s1", A.snowflake, 560, 560, .9, p=(1000, 120, .7)), prop("s2", A.snowflake, 960, 560, .9, p=(1000, 400, .7)), prop("s3", A.snowflake, 1360, 560, .9, p=(1000, 680, .7))],
      fx=[PULSE("w:One,", "#{p}s1_w", 1.3), PULSE("w:two,", "#{p}s2_w", 1.3), PULSE("w:three!", "#{p}s3_w", 1.3)],
      words=[("w:One,", "1", .25, .16, 1.2, "sun", (.27, .31), 1.0), ("w:two,", "2", .5, .16, 1.2, "sun", (.27, .475), 1.0), ("w:three!", "3", .75, .16, 1.2, "sun", (.27, .64), 1.0)]),
    S("gobi", GB, "Look! In winter, there is snow!", part=2, tag="snow", hide=["milo"], pcam=GBP, props=[SNOW()], fx=[FALL(0, 4), ("lookat", "w:snow!", "bac", -14)],
      words=[("w:snow!", "SNOW!", .33, .26, 1.2, "", (.5, .3), 1.0)]),
    S("gobi", say="Can you shiver like Milo? Shiver, shiver!", part=2, q=True, tag="shiver", hide=["bac"], props=[SNOW()],
      fx=[FALL(0, 4), ("to", "w:shiver:1", "#{p}milo", {"x": 8, "duration": .05, "yoyo": True, "repeat": 21}, "Milo shivers")],
      words=[("w:Shiver,:2", "BRRR!", .77, .1, 1.0, "", (.5, .33), .9)], **MILO("gobi", 820)),
    S("gobi", GQ, "Is the Gobi cold in winter? Yes, or no?", part=2, q=True, tag="question 2", pause=3.2, hide=["milo"], pcam=GQP, props=[SNOW()],
      fx=[FALL(0, 8), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0"), ("nod", "wait:2.05", "bac")]),
    S("gobi", GC, "Yes! Very cold, and snowy.", part=2, tag="cold and snowy", hide=["milo"], pcam=GCP, props=[SNOW()], fx=[FALL(0, 4)],
      words=[("w:snowy.", "SNOWY!", .33, .26, 1.2, "", (.5, .3), 1.0)]),
    S("paper_pink", BOARD, "But in summer, the Gobi gets hot!", part=2, tag="board: hot summer", pcam=BOARDP, props=[prop("ic1", A.sun_disc, 960, 560, 1.4, p=(960, 520, 1.1))],
      fx=[PULSE("w:summer,", "#{p}ic1_w"), PULSE("w:hot!", "#{p}ic1_w")], words=[("w:hot!", "HOT!", .5, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper_pink", BOARD, "Cold in winter. Hot in summer!", part=2, tag="board: cold and hot", pcam=BOARDP, props=ICONS(("ic0", "ic1")),
      fx=[("show", "w:Cold", "ic0"), ("show", "w:Hot", "ic1")], words=[("w:winter.", "WINTER", .33, .8, .9, "", (.5, .49), .8), ("w:summer!", "SUMMER", .67, .8, .9, "sun", (.5, .74), .8)]),
    S("paper", BOARD, "Who lives where it snows? The dromedary, or the Bactrian?", part=2, q=True, tag="question 2b", pause=3.2, pcam=PAIRP, props=PAIR(),
      fx=[("signs", "w:dromedary,", ["DROMEDARY", "BACTRIAN"], 1, "wait:2.0"), HUMP("wait:2.05", "b2", 2)]),
    S("gobi", GH, "The Bactrian! Sandy's cousin, in the snowy Gobi.", part=2, tag="the Bactrian", pcam=GHP, props=[SNOW()], fx=[FALL(0, 5), HUMP("w:Bactrian!", "bac")],
      words=[("w:Bactrian!", "BACTRIAN!", .5, .14, 1.0, "sun", (.5, .3), .8)]),
    S("paper_blue", BOARD, "Point to the snowflake! Where is the snowflake?", part=2, q=True, tag="board: point to snowflake", pause=1.4, pcam=BOARDP, props=ICONS(),
      fx=[("to", "e:snowflake?:2", "#{p}ic0_w", {"scale": 1.25, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 3}, "the snowflake picture")],
      words=[("e:snowflake?:2", "THERE!", .33, .16, 1.1, "", (.78, .27), .75)]),
    S("paper_blue", BOARD, "Hot deserts for dromedaries. Snowy winters for Bactrians!", part=2, tag="board: who lives where", pcam=BOARDP,
      props=[DROM("d1", 560, 900, .55, p=(860, 420, .4)), prop("ic1", A.sun_disc, 560, 320, .7, p=(1230, 250, .5)), BAC("b2", 1300, 900, .55, p=(860, 800, .4)), prop("ic0", A.snowflake, 1300, 320, .7, p=(1230, 640, .5))],
      fx=[PULSE("w:Hot", "#{p}ic1_w"), PULSE("w:Snowy", "#{p}ic0_w")]),
    # ---------------------------------------------------------------- PART 3: coats
    S("gobi", GC, "Look at the cousin's coat. It is thick, and shaggy!", part=3, trans="iris", tag="shaggy coat", hide=["milo"], pcam=GCP, props=[SNOW()],
      fx=[FALL(0, 5), ("to", "w:shaggy!", "#{p}bac-sh0,#{p}bac-sh1,#{p}bac-sh3", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 3, "stagger": .05}, "the shaggy patches")],
      words=[("w:shaggy!", "SHAGGY!", .33, .26, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper_blue", BOARD, "Bactrian camels grow a thick coat for winter.", part=3, tag="board: winter coat", pcam=BOARDP,
      props=[BAC("b2", 760, 900, .8, p=(960, 900, .55)), prop("ic0", A.snowflake, 1380, 420, 1.0, p=(960, 300, .8))],
      fx=[("to", "w:thick", ".{p}b2-shag", {"scale": 1.15, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 3, "stagger": .03}, "the thick coat")],
      words=[("w:thick", "THICK COAT", .5, .14, 1.0, "sun", (.5, .29), .8)]),
    S("gobi", GB, "The thick coat keeps her warm in the snow.", part=3, tag="warm in the snow", hide=["milo"], pcam=GBP, props=[SNOW()], fx=[FALL(0, 5), ("nod", "w:warm", "bac")],
      words=[("w:warm", "WARM!", .33, .26, 1.2, "sun", (.5, .3), 1.0)]),
    S("gobi", say="Put on a warm, fuzzy coat. Zip it up!", part=3, q=True, tag="zip", hide=["bac"], props=[SNOW()], fx=[FALL(0, 4), ("hop", "w:Zip", "milo")],
      words=[("w:Zip", "ZIP!", .77, .1, 1.0, "sun", (.5, .33), .9)], **MILO("gobi", 820)),
    S("oasis", OSM, "Mama's coat is not shaggy. It is short, and light.", part=3, trans="iris", tag="Mama's short coat", hide=["milo", "sandy"], pcam=OSMP,
      words=[("w:short,", "SHORT!", .33, .26, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper", BOARD, "Which coat is warmer in the snow? Short, or thick?", part=3, q=True, tag="question 3a", pause=3.2, pcam=PAIRP, props=PAIR(),
      fx=[("signs", "w:Short,", ["SHORT", "THICK"], 1, "wait:2.0"), ("to", "wait:2.05", ".{p}b2-shag", {"scale": 1.15, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 3, "stagger": .03}, "")]),
    S("paper", (1400, 680, 880), "Thick! A thick coat is warm and cozy.", part=3, tag="thick!", pcam=(1360, 640, 1400), pcam2=(1360, 640, 1460), props=PAIR(tall=True),
      fx=[("to", "w:cozy.", ".{p}b2-shag", {"scale": 1.15, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 3, "stagger": .03}, "")],
      words=[("w:Thick!:1", "THICK!", .5, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("gobi_spring", WIDE, "Then spring comes. The snow is gone. It is warm!", part=3, trans="iris", tag="spring wide", cam2=(1000, 560, 1800), pcam=SPBP, pcam2=W(SPBP), hide=["milo"],
      words=[("w:spring", "SPRING!", .5, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("gobi_spring", SPQ, "Is it winter, or spring? Look at the grass!", part=3, q=True, tag="question 3b", pause=3.2, hide=["milo"], pcam=SPQP,
      fx=[("signs", "w:winter,", ["WINTER", "SPRING"], 1, "wait:2.0"), ("nod", "wait:2.05", "bac")]),
    S("gobi_spring", SPC, "Look! Her shaggy coat falls off, in big patches!", part=3, tag="patches fall", hide=["milo"], pcam=SPCP, fx=[SHED("w:falls", 3), SHED("w:off,", 0), SHED("w:patches!", 6)],
      words=[("w:patches!", "PATCHES!", .33, .26, 1.1, "sun", (.5, .35), .9)]),
    S("gobi_spring", SPW, "Now the patches lie on the ground. Count them. One, two, three!", part=3, q=True, tag="count patches", hide=["milo"], pcam=SPWP,
      fx=SHED_DONE((3, 0, 6)) + [PULSE("w:One,", "#{p}bac-sh0", 1.25), PULSE("w:two,", "#{p}bac-sh3", 1.25), PULSE("w:three!", "#{p}bac-sh6", 1.25)],
      words=[("w:One,", "1", .3, .6, 1.0, "sun", (.17, .58), .9), ("w:two,", "2", .51, .6, 1.0, "sun", (.51, .58), .9), ("w:three!", "3", .67, .6, 1.0, "sun", (.77, .58), .9)]),
    S("gobi_spring", SPC, "Plop! Plop! More patches fall off.", part=3, tag="plop plop", hide=["milo"], pcam=SPCP, fx=SHED_DONE((3, 0, 6)) + [SHED("w:Plop!:1", 1), SHED("w:Plop!:2", 2), SHED("w:More", 4)],
      words=[("w:Plop!:1", "PLOP!", .2, .28, 1.2, "sun", (.25, .34), 1.0), ("w:Plop!:2", "PLOP!", .2, .44, 1.2, "sun", (.3, .44), 1.0)]),
    S("gobi_spring", SPQ, "Does the thick coat fall off in spring, or stay on?", part=3, q=True, tag="question 3", pause=3.2, hide=["milo"], pcam=SPQP,
      fx=SHED_DONE((3, 0, 6, 1, 2, 4)) + [("signs", "w:fall", ["FALLS OFF", "STAYS ON"], 0, "wait:2.0"), SHED("wait:2.05", 5)]),
    S("paper_pink", BOARD, "It falls off! This is called shedding.", part=3, tag="board: shedding", pcam=BOARDP,
      props=[prop("hc", A.hair_clump, 720, 700, 1.4, p=(960, 520, 1.0)), prop("hc2", A.hair_clump, 1220, 720, 1.2, True, p=(960, 860, .9))],
      fx=[("show", "w:shedding.", "hc2")], words=[("w:shedding.", "SHEDDING", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    S("gobi_spring", say="Shake, shake! Shake off your winter coat!", part=3, q=True, tag="shake", hide=["bac"],
      fx=[("to", "w:Shake,:1", "#{p}milo", {"rotation": 8, "svgOrigin": "0 0", "duration": .1, "yoyo": True, "repeat": 13}, "Milo shakes")],
      words=[("w:Shake,:1", "SHAKE, SHAKE!", .77, .1, .75, "sun", (.5, .33), .8)], **MILO("gobi_spring", 820)),
    S("gobi_spring", (1150, 600, 1500), "Now her coat is not so thick. Just right for summer!", part=3, tag="summer coat", hide=["milo"], pcam=SPBP, actors=[("bac", "bac_summer", 1150, 920, .95)],
      props=[prop("hc", A.hair_clump, 760, 930, .9), prop("hc2", A.hair_clump, 1620, 950, .8)], fx=[("nod", "w:summer!", "bac")],
      words=[("w:summer!", "SUMMER!", .33, .26, 1.2, "sun", (.5, .37), 1.0)]),
    S("paper_blue", BOARD, "A thick coat in winter. It falls off in spring.", part=3, tag="board: winter spring", pcam=BOARDP,
      props=[BAC("b2", 620, 900, .62, p=(960, 470, .46)), BACS("b3", 1300, 900, .62, True, p=(960, 900, .46)), prop("ic0", A.snowflake, 620, 260, .6, p=(1260, 140, .45)),
             prop("ic2", A.flower_disc, 1300, 260, .6, True, p=(1260, 600, .45))],
      fx=[("show", "w:spring.", "b3"), ("show", "w:spring.", "ic2")]),
    S("paper_blue", BOARD, "And next winter, a new thick coat grows!", part=3, tag="board: grows again", pcam=BOARDP,
      props=[BAC("b4", 960, 900, .85, p=(960, 820, .6))],
      fx=[("fromto", "w:new", ".{p}b4-shag", {"scale": 0, "transformOrigin": "50% 50%"}, {"scale": 1, "duration": .8, "stagger": .08, "ease": "back.out(2)"}, "the new coat grows")],
      words=[("w:grows!", "IT GROWS!", .5, .14, 1.0, "sun", (.5, .3), .85)]),
    S("oasis", say="Do you wear a coat in winter?", part=3, q=True, tag="your coat", hide=["mama", "sandy"], pause=1.2, fx=[("hop", "w:coat", "milo")],
      words=[("w:coat", "YOUR COAT?", .77, .16, .8, "sun", (.5, .33), .85)], **MILO("oasis")),
    S("paper_pink", BOARD, "One hump, or two? Short coat, or shaggy coat!", part=3, tag="board: recap", pcam=PAIRP, props=PAIR(),
      fx=[HUMP("w:One", "d1"), HUMP("w:two?", "b2", 2), ("to", "w:shaggy", ".{p}b2-shag", {"scale": 1.15, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 3, "stagger": .03}, "")]),
    # ---------------------------------------------------------------- QUIZ + GOODBYE
    S("night", WIDE, "Time to remember what we learned!", part=4, trans="iris", tag="quiz time", cam2=(1000, 560, 1800), pcam=(900, 520, 1800),
      words=[("w:remember", "QUIZ TIME!", .5, .14, 1.3, "sun", (.5, .33))]),
    S("night", (960, 560, 1920), "How many humps does a Bactrian camel have? One, or two?", part=4, q=True, tag="quiz 1", pause=3.2, hide=["milo"], pcam=(980, 470, 2000),
      fx=[("signs", "w:One,", ["ONE", "TWO"], 1, "wait:2.0")]),
    S("paper_blue", BOARD, "Two! Like the letter B.", part=4, tag="board: B again", pcam=BOARDP,
      props=[prop("lb", A.letter_b, 520, 520, .7, p=(960, 260, .6)), BAC("b2", 1220, 900, .72, p=(960, 950, .5))],
      fx=[("to", 0, "#{p}lb_w", {"rotation": -90, "transformOrigin": "50% 50%", "duration": .01}, ""), HUMP("w:Two!", "b2", 2), PULSE("w:B.", "#{p}lb_w")],
      words=[("w:Two!", "TWO!", .5, .14, 1.2, "sun", (.75, .56), 1.0)]),
    S("night", (1000, 430, 2100), "Which camel lives where it snows? One hump, or two humps?", part=4, q=True, tag="quiz 2", pause=3.2, hide=["milo"], pcam=(1000, 500, 1900),
      fx=[("signs", "w:One", ["ONE HUMP", "TWO HUMPS"], 1, "wait:2.0")]),
    S("gobi", GB, "Two humps! The Bactrian camel, in the snowy Gobi.", part=4, tag="Gobi again", hide=["milo"], pcam=GBP, props=[SNOW()], fx=[FALL(0, 5), HUMP("w:Two", "bac", 2)],
      words=[("w:Two", "TWO HUMPS!", .33, .26, 1.0, "sun", (.5, .3), .85)]),
    S("night", (1000, 430, 2100), "When does the shaggy coat fall off? In winter, or in spring?", part=4, q=True, tag="quiz 3", pause=3.2, hide=["milo"], pcam=(960, 480, 1950),
      fx=[("signs", "w:winter,", ["WINTER", "SPRING"], 1, "wait:2.0")]),
    S("gobi_spring", SPC, "In spring! Plop, plop, plop!", part=4, tag="spring again", hide=["milo"], pcam=SPCP, fx=[SHED("w:Plop,:1", 3), SHED("w:plop,:2", 0), SHED("w:plop!:3", 6)],
      words=[("w:spring!", "SPRING!", .33, .26, 1.2, "sun", (.5, .3), 1.0)]),
    S("night", WIDE, "Thank you for learning with me, friends. See you at the zoo!", part=4, tag="goodbye", cam2=(960, 560, 1860), pcam=(900, 520, 1800),
      words=[("w:See", "SEE YOU AT THE ZOO!", .45, .12, .82, "pill", (.5, .33), .62)], fx=[("hop", "w:zoo!", "milo", 2), ("hop", "w:See", "sandy")]),
]
for _s in SHOTS:        # a picture board never drifts closer: it only pulls out a little (16:9 and 9:16)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)

SHORTS = [
    {"id": "zc_ep10_short1", "title": "Which Camel Has Two Humps?", "band": ("ONE HUMP", "OR TWO?"), "thumb_text": "LIKE A B!", "part": 1,
     "extra_first": [S("gobi", GH, "Does a camel have one hump, or two humps?", part=1, q=True, tag="hook: one or two", pcam=GHP, props=[SNOW()], fx=[FALL(0, 5), HUMP("w:one", "bac"), HUMP("w:two", "bac")],
                       words=[("w:Does", "?", .5, .16, 2.0, "sun", (.5, .3), 1.3)])]},
    {"id": "zc_ep10_short2", "title": "Where Do Camels Live in the Snow?", "band": ("SNOWY", "CAMELS?"), "thumb_text": "BRRR, COLD!", "part": 2,
     "extra_first": [S("gobi", GB, "A camel in the snow? Where does this camel live?", part=2, q=True, tag="hook: camel in snow", hide=["milo"], pcam=GBP, props=[SNOW()], fx=[FALL(0, 5)],
                       words=[("w:snow?", "?", .33, .26, 2.0, "sun", (.5, .3), 1.3)])]},
    {"id": "zc_ep10_short3", "title": "Why Does a Camel's Coat Fall Off?", "band": ("SHAGGY", "COAT?"), "thumb_text": "PLOP, PLOP!", "part": 3,
     "extra_first": [S("gobi", GC, "Why is this camel so shaggy? And where does her coat go?", part=3, q=True, tag="hook: shaggy", hide=["milo"], pcam=GCP, props=[SNOW()], fx=[FALL(0, 5)],
                       words=[("w:Why", "?", .33, .26, 2.0, "sun", (.5, .3), 1.3)])]},
]

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
THUMBS = {
    "zc_ep10": {"place": "paper_blue", "cam": (960, 600, 1700), "actors": [("camel", 560, 960, .78, False, ""), ("bac_winter", 1360, 960, .78, True, "")],
                "words": [("COUSINS?!", 960, 220, 190, "sun")]},
    "zc_ep10_short1": {"place": "paper_blue", "cam": (960, 560, 1500), "actors": [("bac_winter", 900, 1230, .85, False, "")],
                       "props": [(lambda p: f'<g transform="rotate(-90)">{A.letter_b(p)}</g>', 960, 130, .75)],
                       "words": [("LIKE A", 540, 690, 170, ""), ("B!", 540, 900, 230, "sun")]},
    "zc_ep10_short2": {"place": "gobi", "cam": (1215, 420, 1520), "actors": [("bac_winter", 1150, 920, .95, False, "")], "props": [(art.snow, 0, 0, 1.0)],
                       "words": [("BRRR,", 540, 300, 190, ""), ("COLD!", 540, 520, 210, "sun")]},
    "zc_ep10_short3": {"place": "gobi_spring", "cam": (1215, 420, 1520), "actors": [("bac_winter", 1150, 920, .95, False, "")],
                       "props": [(A.hair_clump, 860, 935, .8), (A.hair_clump, 1560, 950, .7)],
                       "words": [("PLOP,", 540, 300, 190, ""), ("PLOP!", 540, 520, 210, "sun")]},
}
