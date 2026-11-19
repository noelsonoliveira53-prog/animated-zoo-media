"""zc_ep09: "What Do Camels Eat in the Desert?" - cartoon fact lesson with Milo, Sandy the baby camel and her Mama (3D music-and-sync process: "beat").
Milo and Sandy look for lunch in the desert, where so little grows. Three parts, each cut whole into one Short:
1. what camels eat (grass, leaves and twigs of desert plants; a few leaves from each plant, then on to the next; eating all day),
2. how they eat thorny plants (big, tough lips; the top lip split in two, each half moving on its own; hard little bumps inside the mouth that push the food down),
3. salty plants, chewing the food again, and hay at the zoo.
Not the eyelashes, nose, feet, hump or drinking: those are in the live hump lesson zc_ep01 and its Shorts.

FACTS, read at the source on Nov 19 2026, about 1:40 PM ET (each page fetched by the session's page reader, which quotes the sentences it finds):
 [SDZ] San Diego Zoo Wildlife Alliance, "Camel", animals.sandiegozoo.org/node/173
   "Camels are diurnal and spend their days eating."   "They are very clever at finding food in their harsh desert environment."
   "Each half of the split upper lip moves independently, so camels can get near the ground for eating short grass."
   "These tough but flexible lips can break off and eat vegetation such as thorns or salty plants; they even eat fish."
   "Camels are ruminants, like cows, and they regurgitate the food back up from their stomach to chew it again."
   "At the San Diego Zoo and San Diego Zoo Safari Park, the camels eat Bermuda and Sudan hay and herbivore pellets."
 [SDZG] San Diego Zoo Global Library fact sheet, "Camels: Diet", ielc.libguides.com/sdzg/factsheets/extantcamels/diet
   "Mainly grasses, leaves and twigs of shrubs and trees - all plants of the desert."   "Camels graze (like sheep) and browse (like antelopes)."
   "Camels have tough mouths and can eat sharp, thorny plants that other animals can't eat."   "Can eat sharp, thorny plants other animals can't eat (e.g., saltbush)."
   "Salt is very important for the camel."
 [NG] National Geographic, "How camels eat cactus" (nationalgeographic.com/animals/article/camels-cactus-mouth-papillae-animals)
   "The animals' tough, flexible lips move over the food,"   "each half of their split upper lips wiggle independently to get close to the vegetation."
   "the inside of a camel's mouth is lined with raised, cone-shaped structures called papillae."   "they manipulate food to flow in one direction, generally toward the stomach."
   "Papillae in camels partially consist of keratin, the same hard material that your fingernails are made of."
 [NGA] National Geographic, "Arabian camel" facts (nationalgeographic.com/animals/mammals/facts/arabian-camel)
   "Large, tough lips enable them to pick at dry and thorny desert vegetation."
 [SW] SeaWorld, "Dromedary Camel" (seaworld.org/animals/facts/mammals/dromedary-camel)
   "Dromedary Camels may browse for 6 to 8 hours every day."   "This species only selects a few leaves from each plant."
   "These camels are also capable of eating parts of the plant that other species avoid, such as the thorns of the acacia tree."
 Said as: camels eat plants that grow in the desert: grass, leaves and twigs [SDZG]; a camel takes just a few leaves from each plant, then walks on to the next [SW];
 camels spend their days eating [SDZ, SW]; many animals cannot eat thorny plants, camels can [SDZG, SW]; camels have big, tough lips [NGA]; the top lip is split in two
 and each half moves on its own [SDZ, NG]; the lips are tough but bendy (flexible) [SDZ, NG]; inside the mouth there are lots of little bumps [NG]; they are hard, like
 your fingernails [NG]; they help push the food down, toward the tummy [NG]; camels can eat salty plants, like saltbush [SDZ, SDZG]; salt is very important for camels [SDZG];
 camels bring their food back up and chew it again [SDZ]; at the zoo, camels eat hay [SDZ].
 Read but NOT said: cactus and its needles (NG says eating them "can hurt"), fish, cows and sheep (no cow is drawn), how much salt, how many hours, poisonous plants,
 drinking, water in plants (drinking is zc_ep01's topic), smelly breath.
 Sandy's lunch walk is the lesson's frame, not a fact: Sandy is never hungry for long, nobody is hurt, lost, crying or trapped; Mama is with her.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_zc_ep09 as A
import art_zc_ep05 as A5
from kit import Kit, S, prop, W

# the grown camel's points for kit.py (the calf's are there): the numbers of zc_ep01 / zc_ep05, checked in their stills
kit.PT.setdefault("camel", {"head": (345, -601), "eye": (352, -613), "nose": (452, -595), "mouth": (440, -549), "hump": (0, -501), "humptop": (0, -601), "back": (0, -441),
                            "body": (0, -323), "feet": (0, 0), "legs": (10, -131), "all": (60, -330), "top": (345, -700)})

EP = {"id": "zc_ep09", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "What Do Camels Eat in the Desert?", "thumb_text": "THORNS? YUM!", "series": "Animal Facts with Milo",
      "description": ("What do camels eat in the desert, where so few plants grow? Milo the bluebird looks for lunch with Sandy the baby camel and her mama! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn that camels eat desert plants (grass, leaves and twigs), that a camel takes just a few leaves from each plant and walks on, "
                      "that camels can eat thorny plants with their big, tough lips, that a camel's top lip is split in two and each half moves on its own, "
                      "that hard little bumps inside the mouth push the food down, that camels can eat salty plants, and that camels chew their food again.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (camel; camel diet fact sheet); National Geographic (how camels eat; Arabian camel); "
                      "SeaWorld (dromedary camel)."),
      "tags": ["what do camels eat", "camel", "camels for kids", "baby camel", "camel lips", "desert animals for kids", "animal facts for kids",
               "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "zoo": [("milo", "milo", 960, 940, 1.1, False, False)],
    "dunes": [("sandy", "calf", 700, 935, .56), ("milo", "milo", 330, 560, .8, False, True)],
    "trail": [("mama", "camel", 1330, 900, .95), ("sandy", "calf", 590, 930, .54), ("milo", "milo", 300, 500, .75, False, True)],
    "oasis": [("mama", "camel", 1150, 880, .9), ("sandy", "calf", 400, 915, .52), ("milo", "milo", 1640, 520, .72, True, True)],
    "dune_eve": [("sandy", "calf", 900, 935, .56), ("milo", "milo", 400, 560, .72, False, True)],
    "night": [("mama", "camel", 1260, 905, .95), ("sandy", "calf", 680, 935, .54), ("milo", "milo", 290, 892, .8, False, False)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 1100, 0, -90))      # 9:16: Milo lower and smaller, room for the word between the title and his crest
BOARD = (960, 540, 1500); BOARDP = (960, 440, 1700)

# ------------------------------------------------------------------ eating
NECK = lambda who, deg: ("to", 0, "#{p}%s-neck" % who, {"rotation": deg, "svgOrigin": "190 -330", "duration": .01}, "")      # the head is down (eating) for the whole shot
def CHEW(at, who, d=2.0): return ("chew", at, who, d)
def BEND(at, who, d=2.4, deg=58): return ("drink", at, who, d, deg)                                                      # bends down to the plant and comes back up
GRASS = lambda name, x, y, s=.5, p=None: prop(name, A.grass, x, y, s, p=p)
BUSH = lambda name, x, y, s=.6, hidden=False, p=None: prop(name, A.leafy_bush, x, y, s, hidden, p)
THORNS = lambda name="th", x=1850, y=905, s=1.5: prop(name, lambda p: art._thorn(p, 0, 0), x, y, s)
SALT = lambda name, x, y, s=.6, p=None: prop(name, A.saltbush, x, y, s, p=p)
def EAT_LEAF(at, bush, k): return ("to", at, f"#{{p}}{bush}-l{k}", {"opacity": 0, "scale": .3, "transformOrigin": "50% 50%", "duration": .3}, "a leaf is eaten")

# dunes: Sandy's grass at her mouth when she bends down
DS = (700, 935, .56)
SANDY_D = C("dunes", "sandy", "all", 1100, 120, -40)
SANDY_DP = WV("dunes", ["sandy"], floor=.70, top=.44, pad=.12)
# trail: the leafy bush in front of Sandy, the thorny bush in front of Mama (zc_ep01's bush and cameras)
TB = (930, 932, .62)
TRS = (820, 720, 1100); TRSP = (700, 660, 1420)            # Sandy and her leafy bush
TRQ = (1000, 500, 2000); TRQP = WV("trail", ["sandy", "mama"], floor=.70, top=.46)            # the question view on the trail: heads under the answer signs
TRP = (1200, 300, 2600)
# oasis: the salty bush in front of Sandy
OS_ = (730, 918, .55)
OSC = (640, 700, 1100); OSCP = (590, 640, 1440)
OSQ = (860, 540, 1920); OSQP = WV("oasis", ["sandy", "mama", "milo"], floor=.70, top=.46)
# the lips board and the mouth board
MZ = (960, 720, .82); MZP = (960, 720, .72)
IM = (960, 600, .82); IMP = (960, 600, .74)
def LIPS(at, n=5):
    return [("to", at, "#{p}mz-lipL", {"rotation": -12, "svgOrigin": "-6 -140", "duration": .18, "yoyo": True, "repeat": n}, "the left half of the lip wiggles"),
            ("to", at, "#{p}mz-lipR", {"rotation": 12, "y": -10, "svgOrigin": "6 -140", "duration": .24, "yoyo": True, "repeat": n}, "the right half wiggles on its own")]
def CONES(at, n=3): return ("to", at, ".{p}im-cone", {"scale": 1.35, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": n, "stagger": .02}, "the little bumps light up")
ARROW_OFF = ("fromto", 0, "#{p}im-arrow", {"opacity": 0}, {"opacity": 0, "duration": .01}, "")
def ARROW_ON(at): return ("to", at, "#{p}im-arrow", {"opacity": 1, "duration": .3}, "the arrow shows the way down")
ICON = {"grass": A.food_icon(A.grass, .62, 80), "leaf": A.food_icon(A.leaf, .7), "twig": A.food_icon(A.twig, .62), "thorn": A.food_icon(lambda p: art._thorn(p, 0, 0), .6, 70),
        "salt": A.food_icon(A.saltbush, .38, 60), "hay": A.food_icon(A5.hay, .5, 80)}
def FOOD(name, kind, x, y, s=1.0, hidden=False, p=None): return prop(name, ICON[kind], x, y, s, hidden, p)
LUNCH = lambda new=(): [FOOD("f0", "grass", 560, 560, 1.0, "f0" in new, p=(660, 380, .62)), FOOD("f1", "leaf", 960, 560, 1.0, "f1" in new, p=(960, 380, .62)),
                        FOOD("f2", "twig", 1360, 560, 1.0, "f2" in new, p=(1260, 380, .62))]

SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("trail", (1650, 590, 1150), "What do camels eat in the desert?", q=True, tag="hook: what do camels eat", pcam=TRP, props=[THORNS(), BUSH("bu", *TB)], hide=["milo"],
      fx=[BEND(0.2, "mama", 2.2), CHEW(0.9, "mama", 1.4)], words=[("w:eat", "?", .2, .3, 2.6, "sun", (.22, .42), 1.4)]),
    S("paper_pink", BOARD, "Grass? Leaves? Or prickly thorns?", tag="hook: guesses", pcam=(960, 480, 1700),
      props=[FOOD("a", "grass", 560, 560, 1.3, True, p=(700, 360, 1.0)), FOOD("b", "leaf", 960, 560, 1.3, True, p=(1220, 560, 1.0)), FOOD("c", "thorn", 1360, 560, 1.3, True, p=(700, 760, 1.0))],
      fx=[("show", "w:Grass?", "a"), ("show", "w:Leaves?", "b"), ("show", "w:thorns?", "c")]),
    S("dunes", say="I'm Milo. Let's find out with Sandy!", tag="hook: Milo", hide=["sandy"], fx=[("hop", "w:find", "milo")], **MILO("dunes")),
    # ---------------------------------------------------------------- INTRO
    S("zoo", WIDE, "Welcome to The Animated Zoo, friends!", trans="iris", tag="gate wide", words=[("w:Animated", "HELLO!", .74, .6, 1.2, "pill")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, -40), "Today we fly to the sandy desert, for lunch!", tag="Milo close", words=[("w:desert,", "THE DESERT", .5, .16, 1.1, "sun")]),
    S("dunes", WIDE, "Here we are! It is hot and dry. Only a few plants grow here.", trans="iris", tag="dunes wide", cam2=(1000, 560, 1780), pcam=(760, 520, 1700), pcam2=(760, 520, 1780),
      props=[GRASS("g0", 1500, 930, .4), GRASS("g1", 260, 960, .35)],
      fx=[("fromto", 0, "#{p}milo_w", {"x": 1200, "y": 300}, {"x": 330, "y": 560, "duration": 1.6, "ease": "power2.out"}, "Milo flies in")],
      words=[("w:few", "A FEW PLANTS", .5, .14, 1.0, "sun", (.5, .33), .8)]),
    S("dunes", SANDY_D, "This is Sandy, the baby camel. Sandy is hungry!", tag="this is Sandy", hide=["milo"], pcam=SANDY_DP,
      words=[("w:Sandy,", "SANDY", .22, .2, 1.1, "pill", (.5, .33), .9)], fx=[("hop", "w:hungry!", "sandy"), ("lookat", "w:Sandy,", "sandy", -10)]),
    # ---------------------------------------------------------------- PART 1: what camels eat
    S("paper_blue", BOARD, "Camels eat plants that grow in the desert.", part=1, tag="board: desert plants", pcam=BOARDP,
      props=[prop("cm", lambda p: art.camel(p, 0, calf=True), 700, 880, .7, p=(780, 780, .55)), BUSH("bu", 1240, 880, 1.0, p=(1180, 780, .7)), GRASS("g0", 1500, 885, .7, p=(1330, 780, .5))],
      fx=[("to", "w:plants", "#{p}bu_w", {"y": "-=24", "duration": .2, "yoyo": True, "repeat": 1}, "the bush bobs")], words=[("w:plants", "PLANTS!", .5, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper_blue", BOARD, "Grass, leaves, and little twigs. Yum!", part=1, tag="board: grass leaves twigs", pcam=BOARDP, props=LUNCH(("f0", "f1", "f2")),
      fx=[("show", "w:Grass,", "f0"), ("show", "w:leaves,", "f1"), ("show", "w:twigs.", "f2")], words=[("w:Yum!", "YUM!", .5, .16, 1.2, "sun", (.5, .56), 1.0)]),
    S("paper_blue", BOARD, "Say it with me. Grass, leaves, and twigs!", part=1, q=True, tag="board: say it", pcam=BOARDP, props=LUNCH(),
      fx=[("to", "w:Grass,", "#{p}f0_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, ""), ("to", "w:leaves,", "#{p}f1_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, ""),
          ("to", "w:twigs!", "#{p}f2_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, "")],
      words=[("w:Say", "SAY IT!", .5, .16, 1.1, "sun", (.5, .56), .9)]),
    S("paper_blue", BOARD, "Let's count them. One, two, three!", part=1, q=True, tag="board: count three", pcam=BOARDP, props=LUNCH(),
      fx=[("to", "w:One,", "#{p}f0_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, ""), ("to", "w:two,", "#{p}f1_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, ""),
          ("to", "w:three!", "#{p}f2_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, "")],
      words=[("w:One,", "1", .25, .2, 1.2, "sun", (.19, .36), 1.0), ("w:two,", "2", .5, .2, 1.2, "sun", (.5, .36), 1.0), ("w:three!", "3", .75, .2, 1.2, "sun", (.81, .36), 1.0)]),
    S("dunes", (860, 620, 1500), "Sandy looks, and looks. Camels are very clever at finding food.", part=1, tag="Sandy looks", hide=["milo"], pcam=SANDY_DP, pcam2=W(SANDY_DP),
      props=[GRASS("gr", 1022, 942, .5)], fx=[("lookat", "w:looks,", "sandy", -14), ("lookat", "w:looks.", "sandy", 10), ("lookat", "w:clever", "sandy", 0)],
      words=[("w:clever", "CLEVER!", .78, .2, 1.1, "sun", (.5, .33), .9)]),
    S("dunes", SANDY_D, "Sandy finds some grass. Munch, munch!", part=1, tag="Sandy eats grass", hide=["milo"], pcam=SANDY_DP, props=[GRASS("gr", 1022, 942, .5)],
      fx=[BEND("w:finds", "sandy", 3.0, 62), CHEW("w:Munch,", "sandy", 1.8)], words=[("w:Munch,", "MUNCH!", .22, .2, 1.2, "sun", (.5, .33), 1.0)]),
    S("trail", WIDE, "Then Sandy and Mama walk to a little bush.", part=1, trans="iris", tag="trail wide", cam2=(1060, 560, 1740), pcam=TRP, pcam2=W(TRP), hide=["milo"],
      props=[BUSH("bu", *TB), THORNS()], move={"sandy": (330, 930, .54), "mama": (1030, 900, .95)},
      fx=[("walk", 0.1, "sandy", 260, 3.2), ("walk", 0.1, "mama", 300, 3.2)], words=[("w:little", "A LITTLE BUSH", .5, .14, .9, "sun", (.5, .33), .8)]),
    S("trail", TRS, "Sandy nibbles the green leaves. Nibble, nibble!", part=1, tag="Sandy nibbles leaves", hide=["milo", "mama"], pcam=TRSP, props=[BUSH("bu", *TB)],
      fx=[NECK("sandy", 34), CHEW("w:nibbles", "sandy", 2.6), EAT_LEAF("w:Nibble,", "bu", 2), EAT_LEAF("w:nibble!", "bu", 3)],
      words=[("w:Nibble,", "NIBBLE!", .22, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("trail", TRQ, "Does a camel eat leaves, or rocks?", part=1, q=True, tag="question 1", pause=3.2, hide=["milo"], pcam=TRQP, props=[BUSH("bu", *TB), THORNS()],
      fx=[("signs", "w:leaves,", ["LEAVES", "ROCKS"], 0, "wait:2.0"), ("hop", "wait:2.05", "sandy")]),
    S("trail", TRS, "Leaves! Camels eat leaves, and grass, and twigs.", part=1, tag="leaves!", hide=["milo", "mama"], pcam=TRSP, props=[BUSH("bu", *TB)],
      fx=[NECK("sandy", 34), CHEW(0.2, "sandy", 2.0), EAT_LEAF("w:Leaves!", "bu", 4)], words=[("w:Leaves!", "LEAVES!", .22, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("trail", say="Can you nibble like a camel? Nibble, nibble!", part=1, q=True, tag="nibble", hide=["mama", "sandy"], fx=[("hop", "w:Nibble,", "milo", 2)],
      words=[("w:Nibble,", "NIBBLE, NIBBLE!", .77, .1, 0.68, "sun", (.5, .33), .75)], **MILO("trail", 820)),
    S("trail", TRS, "Look! Sandy eats only a few leaves.", part=1, tag="only a few", hide=["milo", "mama"], pcam=TRSP, props=[BUSH("bu", *TB)],
      fx=[NECK("sandy", 34), CHEW(0.2, "sandy", 2.2), EAT_LEAF(0.1, "bu", 2), EAT_LEAF(0.1, "bu", 3), EAT_LEAF(0.1, "bu", 4)],
      words=[("w:few", "A FEW", .22, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("trail", TRS, "Count the leaves she eats. One, two, three!", part=1, q=True, tag="count leaves", hide=["milo", "mama"], pcam=TRSP, props=[BUSH("bu", *TB)],
      fx=[NECK("sandy", 34), CHEW("w:One,", "sandy", 2.6), EAT_LEAF(0, "bu", 2), EAT_LEAF(0, "bu", 3), EAT_LEAF(0, "bu", 4), EAT_LEAF("w:One,", "bu", 5), EAT_LEAF("w:two,", "bu", 6), EAT_LEAF("w:three!", "bu", 1)],
      words=[("w:One,", "1", .2, .2, 1.2, "sun", (.25, .3), 1.0), ("w:two,", "2", .35, .14, 1.2, "sun", (.5, .31), 1.0), ("w:three!", "3", .5, .2, 1.2, "sun", (.75, .3), 1.0)]),
    S("trail", (1000, 620, 1500), "Then she walks on, to the next plant.", part=1, tag="walks on", hide=["milo", "mama"], pcam=(960, 560, 2200), pcam2=(960, 560, 2300),
      props=[BUSH("b2", 1500, 932, .62)], move={"sandy": (590, 930, .54)},
      fx=[("walk", "w:walks", "sandy", 520, 2.6)],
      words=[("w:next", "NEXT PLANT!", .5, .14, 1.0, "sun", (.5, .3), .85)]),
    S("paper", BOARD, "Camels take just a few leaves from each plant.", part=1, tag="board: a few from each", pcam=BOARDP,
      props=[BUSH("b0", 560, 860, .9, p=(720, 560, .55)), BUSH("b1", 960, 860, .9, p=(1200, 560, .55)), BUSH("b2", 1360, 860, .9, p=(960, 820, .55))],
      fx=[EAT_LEAF("w:few", "b0", 1), EAT_LEAF("w:few", "b0", 5), EAT_LEAF("w:each", "b1", 2), EAT_LEAF("w:each", "b1", 4), EAT_LEAF("w:plant.", "b2", 0), EAT_LEAF("w:plant.", "b2", 3)],
      words=[("w:few", "A FEW FROM EACH", .5, .14, .95, "sun", (.5, .3), .75)]),
    S("trail", TRQ, "Does a camel eat all the leaves, or just a few?", part=1, q=True, tag="question 1b", pause=3.2, hide=["milo"], pcam=TRQP, props=[BUSH("bu", *TB), THORNS()],
      fx=[EAT_LEAF(0, "bu", 2), EAT_LEAF(0, "bu", 3), EAT_LEAF(0, "bu", 4), ("signs", "w:all", ["ALL", "A FEW"], 1, "wait:2.0"), ("hop", "wait:2.05", "sandy")]),
    S("dune_eve", WIDE, "Camels spend their days eating. Munch, munch, all day long!", part=1, trans="iris", tag="all day long", cam2=(980, 560, 1800), pcam=(900, 520, 1700), pcam2=(900, 520, 1780),
      hide=["milo"], props=[GRASS("gr", 1222, 942, .5), GRASS("g2", 1600, 950, .45)],
      fx=[("fromto", 0, "#{p}sun", {"y": -260}, {"y": 0, "duration": 5.0, "ease": "sine.inOut"}, "the sun goes down"), NECK("sandy", 62), CHEW("w:Munch,", "sandy", 2.4)],
      words=[("w:days", "ALL DAY!", .5, .14, 1.1, "sun", (.5, .33), .9)]),
    S("dune_eve", (1060, 640, 1300), "From the morning, until the sun goes down!", part=1, tag="until sundown", hide=["milo"], pcam=(1000, 560, 1500),
      props=[GRASS("gr", 1222, 942, .5)], fx=[("fromto", 0, "#{p}sun", {"y": 0}, {"y": 120, "duration": 3.0, "ease": "sine.inOut"}, "the sun goes lower"), NECK("sandy", 62), CHEW(0.1, "sandy", 2.6)],
      words=[("w:down!", "SUN DOWN!", .32, .2, .85, "sun", (.5, .33), .85)]),
    S("dune_eve", say="What do you like to eat for lunch?", part=1, q=True, tag="your lunch", hide=["sandy"], pause=1.0, fx=[("hop", "w:lunch?", "milo")],
      words=[("w:lunch?", "YOUR LUNCH?", .77, .1, 0.77, "sun", (.5, .33), .85)], **MILO("dune_eve")),
    S("dune_eve", say="Rub your tummy. Mmm, yum!", part=1, q=True, tag="rub tummy", hide=["sandy"], fx=[("hop", "w:yum!", "milo")],
      words=[("w:yum!", "MMM, YUM!", .77, .1, 0.81, "sun", (.5, .33), .85)], **MILO("dune_eve", 820)),
    S("paper_blue", BOARD, "Point to the leaf! Where is the leaf?", part=1, q=True, tag="board: point to the leaf", pause=1.4, pcam=BOARDP, props=LUNCH(),
      fx=[("to", "e:leaf?", "#{p}f1_w", {"scale": 1.25, "duration": .25, "yoyo": True, "repeat": 3}, "the leaf picture")],
      words=[("e:leaf?", "THE LEAF!", .5, .16, 1.1, "sun", (.5, .56), .9)]),
    S("paper_blue", BOARD, "Grass, leaves, and twigs. A camel's lunch!", part=1, tag="board: a camel's lunch", pcam=BOARDP, props=LUNCH(),
      fx=[("to", "w:Grass,", "#{p}f0_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, ""), ("to", "w:leaves,", "#{p}f1_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, ""),
          ("to", "w:twigs.", "#{p}f2_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, "")],
      words=[("w:lunch!", "LUNCH!", .5, .16, 1.2, "sun", (.5, .56), 1.0)]),
    # ---------------------------------------------------------------- PART 2: thorny plants, tough lips, little bumps
    S("trail", WIDE, "Look at this bush. It is covered in thorns!", part=2, trans="iris", tag="thorny bush wide", cam2=(1060, 560, 1740), pcam=TRP, pcam2=W(TRP), hide=["milo"],
      props=[THORNS()], words=[("w:thorns!", "THORNS!", .5, .14, 1.1, "sun", (.5, .33), .9)]),
    S("paper", BOARD, "Thorns are hard and pointy. Many animals cannot eat them.", part=2, tag="board: pointy thorns", pcam=BOARDP,
      props=[prop("tb", A.thorn_branch, 960, 600, 1.4, p=(960, 520, 1.0))],
      fx=[("to", "w:pointy.", "#{p}tb_w", {"rotation": 3, "transformOrigin": "50% 50%", "duration": .15, "yoyo": True, "repeat": 3}, "the branch wiggles")],
      words=[("w:pointy.", "POINTY!", .5, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("trail", TRQ, "Can a camel eat thorny plants? Yes, or no?", part=2, q=True, tag="question 2", pause=3.2, hide=["milo"], pcam=TRQP, props=[THORNS()],
      fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0"), ("hop", "wait:2.05", "mama")]),
    S("trail", (1650, 590, 1150), "Yes! Mama munches the thorny plant. Munch, munch!", part=2, tag="Mama eats thorns", hide=["milo", "sandy"], pcam=(1710, 480, 1300), props=[THORNS()],
      fx=[BEND("w:Mama", "mama", 3.0, 58), CHEW("w:munches", "mama", 2.4)]),
    S("paper", BOARD, "How? Camels have big, tough lips.", part=2, tag="board: tough lips", pcam=BOARDP, props=[prop("mz", A.muzzle, *MZ, p=MZP)],
      fx=LIPS("w:tough", 3), words=[("w:tough", "TOUGH LIPS", .16, .4, .75, "sun", (.5, .31), .8)]),
    S("paper", (960, 640, 1000), "Look closely. The top lip is split in two!", part=2, tag="board: split lip", pcam=BOARDP, pcam2=W(BOARDP, 1.15),
      props=[prop("mz", A.muzzle, *MZ, p=MZP), prop("ar", lambda p: art.arrow(p, 1300, 420, 985, 630), 0, 0, 1, True, p=(-30, 20, 1))],
      fx=[("show", "w:split", "ar")], words=[("w:two!", "2 HALVES", .15, .45, .75, "sun", (.5, .31), .8)]),
    S("paper", (960, 560, 1700), "One half, two halves. Count them with me!", part=2, q=True, tag="board: count halves", pcam=(960, 500, 1800), props=[prop("mz", A.muzzle, *MZ, p=MZP)],
      fx=[("to", "w:One", "#{p}mz-lipL", {"rotation": -12, "svgOrigin": "-6 -140", "duration": .2, "yoyo": True, "repeat": 1}, "the left half"),
          ("to", "w:two", "#{p}mz-lipR", {"rotation": 12, "svgOrigin": "6 -140", "duration": .2, "yoyo": True, "repeat": 1}, "the right half")],
      words=[("w:One", "1", .3, .7, 1.3, "sun", (.25, .6), 1.0), ("w:two", "2", .7, .7, 1.3, "sun", (.75, .6), 1.0)]),
    S("paper", (960, 620, 1150), "Each half can move on its own. Wiggle, wiggle!", part=2, tag="board: each half moves", pcam=BOARDP, pcam2=W(BOARDP, 1.15), props=[prop("mz", A.muzzle, *MZ, p=MZP)],
      fx=LIPS("w:Wiggle,", 7), words=[("w:Wiggle,", "WIGGLE!", .86, .2, 1.0, "sun", (.5, .31), .9)]),
    S("trail", say="Can you wiggle your lips? Wiggle, wiggle!", part=2, q=True, tag="wiggle", hide=["mama", "sandy"], fx=[("hop", "w:Wiggle,", "milo", 2)],
      words=[("w:Wiggle,", "WIGGLE, WIGGLE!", .77, .1, 0.68, "sun", (.5, .33), .75)], **MILO("trail", 820)),
    S("paper", BOARD, "The lips are tough, but bendy. They pick at the little leaves.", part=2, tag="board: bendy lips", pcam=BOARDP,
      props=[prop("mz", A.muzzle, 780, 720, .8, p=(900, 740, .64)), prop("lf", A.leaf, 1340, 760, .9, p=(1260, 720, .55))],
      fx=LIPS("w:bendy.", 3) + [("to", "w:pick", "#{p}lf_w", {"x": 900, "y": 740, "scale": .3, "opacity": 0, "duration": .6, "ease": "power2.in"}, "the lips pick up the leaf")],
      words=[("w:bendy.", "BENDY!", .82, .2, 1.0, "sun", (.5, .31), .9)]),
    S("paper_pink", BOARD, "Inside the mouth, there are lots of little bumps.", part=2, tag="board: little bumps", pcam=BOARDP, props=[prop("im", A.inside_mouth, *IM, p=IMP)],
      fx=[ARROW_OFF, CONES("w:bumps.", 3)], words=[("w:bumps.", "LITTLE BUMPS", .5, .1, .95, "sun", (.5, .31), .8)]),
    S("paper_pink", BOARD, "Count some bumps with me. One, two, three, four!", part=2, q=True, tag="board: count bumps", pcam=BOARDP, props=[prop("im", A.inside_mouth, *IM, p=IMP)],
      fx=[ARROW_OFF], words=[("w:One,", "1", .3, .1, 1.1, "sun", (.25, .31), .9), ("w:two,", "2", .43, .1, 1.1, "sun", (.42, .31), .9),
                             ("w:three,", "3", .57, .1, 1.1, "sun", (.58, .31), .9), ("w:four!", "4", .7, .1, 1.1, "sun", (.75, .31), .9)]),
    S("paper_pink", BOARD, "The bumps are hard, like your fingernails.", part=2, tag="board: like fingernails", pcam=BOARDP,
      props=[prop("im", A.inside_mouth, 760, 600, .7, p=(960, 500, .66)), prop("ft", A.fingertip, 1440, 860, 1.2, True, p=(1290, 830, .5))],
      fx=[ARROW_OFF, CONES("w:hard,", 2), ("show", "w:fingernails.", "ft")], words=[("w:hard,", "HARD!", .82, .14, 1.1, "sun", (.5, .31), .9)]),
    S("trail", say="Tap your fingernails. Tap, tap! So hard!", part=2, q=True, tag="tap", hide=["mama", "sandy"], fx=[("hop", "w:Tap,", "milo"), ("hop", "w:tap!", "milo")],
      words=[("w:Tap,", "TAP, TAP!", .77, .1, 0.81, "sun", (.5, .33), .85)], **MILO("trail", 820)),
    S("paper_pink", BOARD, "The bumps help push the food down, to the tummy.", part=2, tag="board: down to the tummy", pcam=BOARDP, props=[prop("im", A.inside_mouth, *IM, p=IMP)],
      fx=[ARROW_OFF, ARROW_ON("w:down,"), CONES("w:push", 2)], words=[("w:down,", "DOWN!", .5, .08, .9, "sun", (.5, .31), .9)]),
    S("paper_pink", BOARD, "Every little bump points the same way. Down, down, down!", part=2, tag="board: all point down", pcam=BOARDP, props=[prop("im", A.inside_mouth, *IM, p=IMP)],
      fx=[ARROW_OFF, CONES("w:points", 2), ARROW_ON("w:Down,")], words=[("w:Down,", "DOWN, DOWN!", .5, .08, .85, "sun", (.5, .31), .8)]),
    S("paper_pink", BOARD, "Where do the bumps push the food? Up to the nose, or down to the tummy?", part=2, q=True, tag="question 3", pause=3.2, pcam=BOARDP,
      props=[prop("im", A.inside_mouth, 960, 680, .7, p=(960, 640, .7))], fx=[ARROW_OFF, ("signs", "w:Up", ["NOSE", "TUMMY"], 1, "wait:2.0"), ARROW_ON("wait:2.05")]),
    S("trail", (1750, 640, 900), "Down to the tummy! So Mama can eat thorny plants.", part=2, tag="Mama munches", hide=["milo", "sandy"], pcam=(1750, 560, 1100), props=[THORNS()],
      fx=[NECK("mama", 58), CHEW(0.1, "mama", 3.6)], words=[("w:tummy!", "TUMMY!", .24, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("trail", TRS, "Sandy tries a little thorny twig, too. Crunch!", part=2, tag="Sandy tries thorns", hide=["milo", "mama"], pcam=TRSP, props=[THORNS("t2", 905, 935, .8)],
      fx=[NECK("sandy", 62), CHEW("w:twig,", "sandy", 2.2), ("snd", "w:Crunch!", "pop")], words=[("w:Crunch!", "CRUNCH!", .22, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper", BOARD, "Tough lips, and hard little bumps. Thorns, yum!", part=2, tag="board: lips and bumps", pcam=BOARDP,
      props=[prop("mz", A.muzzle, 620, 720, .6, p=(750, 600, .42)), prop("im", A.inside_mouth, 1330, 640, .55, p=(1170, 640, .42))],
      fx=[ARROW_OFF] + LIPS("w:lips,", 3) + [CONES("w:bumps.", 2)], words=[("w:yum!", "THORNS, YUM!", .5, .1, .95, "sun", (.5, .31), .8)]),
    # ---------------------------------------------------------------- PART 3: salty plants, chewing again, hay at the zoo
    S("oasis", WIDE, "At the oasis, Sandy finds a different plant.", part=3, trans="iris", tag="oasis wide", cam2=(980, 560, 1800), pcam=OSQP, pcam2=W(OSQP),
      props=[SALT("sb", *OS_)], fx=[("fromto", 0, "#{p}milo_w", {"x": 2200, "y": 200}, {"x": 1640, "y": 520, "duration": 1.4, "ease": "power2.out"}, "Milo flies in")],
      words=[("w:different", "A NEW PLANT", .5, .14, 1.0, "sun", (.5, .33), .85)]),
    S("oasis", OSC, "Sandy sniffs the leaves. They taste salty!", part=3, tag="salty leaves", hide=["milo", "mama"], pcam=OSCP, props=[SALT("sb", *OS_)],
      fx=[NECK("sandy", 30), ("to", "w:salty!", ".{p}sb-salt", {"scale": 1.6, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 3, "stagger": .03}, "the salt sparkles")],
      words=[("w:salty!", "SALTY!", .78, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper", BOARD, "It is a salty plant, called saltbush.", part=3, tag="board: saltbush", pcam=BOARDP, props=[SALT("sb", 960, 860, 1.4, p=(960, 800, 1.0))],
      fx=[("to", "w:salty", ".{p}sb-salt", {"scale": 1.6, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 3, "stagger": .03}, "the salt sparkles")],
      words=[("w:saltbush.", "SALTBUSH", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    S("paper", BOARD, "Is saltbush salty, or sweet?", part=3, q=True, tag="question 4a", pause=3.2, pcam=BOARDP, props=[SALT("sb", 960, 900, 1.2, p=(960, 860, .9))],
      fx=[("signs", "w:salty,", ["SALTY", "SWEET"], 0, "wait:2.0"), ("to", "wait:2.05", ".{p}sb-salt", {"scale": 1.6, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 3, "stagger": .03}, "the salt sparkles")]),
    S("oasis", OSQ, "Can camels eat salty plants? Yes, or no?", part=3, q=True, tag="question 4", pause=3.2, hide=["milo"], pcam=OSQP, props=[SALT("sb", *OS_)],
      fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0"), ("hop", "wait:2.05", "sandy")]),
    S("oasis", OSC, "Yes! Sandy nibbles the salty leaves. Munch!", part=3, tag="Sandy eats saltbush", hide=["milo", "mama"], pcam=OSCP, props=[SALT("sb", *OS_)],
      fx=[NECK("sandy", 40), CHEW("w:nibbles", "sandy", 2.6)], words=[("w:Yes!", "YES!", .78, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("oasis", OSC, "Munch, munch. A salty snack for Sandy!", part=3, tag="salty snack", hide=["milo", "mama"], pcam=OSCP, props=[SALT("sb", *OS_)],
      fx=[NECK("sandy", 40), CHEW("w:Munch,", "sandy", 2.4)], words=[("w:snack", "SNACK!", .78, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper", BOARD, "Salt is very important for camels.", part=3, tag="board: salt matters", pcam=BOARDP,
      props=[prop("cm", lambda p: art.camel(p, 0, calf=True), 700, 880, .7, p=(740, 780, .5)), SALT("sb", 1300, 880, 1.0, p=(1230, 780, .5))],
      fx=[("to", "w:important", ".{p}sb-salt", {"scale": 1.6, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 3, "stagger": .03}, "the salt sparkles")],
      words=[("w:important", "SALT!", .5, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("oasis", say="Can you say saltbush? Salt, bush!", part=3, q=True, tag="say saltbush", hide=["mama", "sandy"], fx=[("hop", "w:Salt,", "milo"), ("hop", "w:bush!", "milo")],
      words=[("w:Salt,", "SALT, BUSH!", .77, .16, 0.81, "sun", (.5, .33), .85)], **MILO("oasis")),
    S("oasis", C("oasis", "mama", "head", 900, -60, 40), "After lunch, Mama rests. But look, she is chewing again!", part=3, tag="Mama chews again", hide=["milo", "sandy"],
      pcam=V("oasis", "mama", "head", 1200, -60, 120), fx=[CHEW("w:chewing", "mama", 2.6)], words=[("w:again!", "CHEW AGAIN!", .34, .14, .8, "sun", (.5, .3), .8)]),
    S("paper_blue", BOARD, "Camels bring their food back up, and chew it again!", part=3, tag="board: chew it again", pcam=BOARDP,
      props=[prop("cm", lambda p: art.camel(p, 1), 860, 900, .85, p=(900, 900, .62)), prop("lp", A.loop_arrow, 1450, 520, .6, True, p=(1250, 680, .45))],
      fx=[("show", "w:back", "lp"), ("to", "w:back", "#{p}lp_w", {"rotation": 360, "transformOrigin": "50% 50%", "duration": 1.6, "ease": "power1.inOut"}, "the arrow goes round"),
          ("chew", "w:chew", "cm", 1.8)],
      words=[("w:again!", "AGAIN!", .2, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper_blue", BOARD, "Chew, chew, chew. Then chew some more!", part=3, tag="board: chew some more", pcam=BOARDP,
      props=[prop("cm", lambda p: art.camel(p, 1), 860, 900, .85, p=(900, 900, .62)), prop("lp", A.loop_arrow, 1450, 520, .6, p=(1250, 680, .45))],
      fx=[("chew", "w:Chew,", "cm", 3.2), ("to", "w:Then", "#{p}lp_w", {"rotation": 360, "transformOrigin": "50% 50%", "duration": 1.4, "ease": "power1.inOut"}, "the arrow goes round")],
      words=[("w:Chew,", "CHEW!", .2, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper_blue", BOARD, "Chew. Swallow. Then up it comes, to chew again!", part=3, tag="board: chew swallow again", pcam=BOARDP,
      props=[prop("cm", lambda p: art.camel(p, 1), 860, 900, .85, p=(900, 900, .62)), prop("lp", A.loop_arrow, 1450, 520, .6, p=(1250, 680, .45))],
      fx=[("chew", "w:Chew.", "cm", 1.0), ("to", "w:Swallow.", "#{p}lp_w", {"rotation": 180, "transformOrigin": "50% 50%", "duration": .8}, "down"),
          ("to", "w:up", "#{p}lp_w", {"rotation": 360, "transformOrigin": "50% 50%", "duration": .8}, "and up"), ("chew", "w:again!", "cm", 1.2)],
      words=[("w:Swallow.", "GULP!", .2, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("oasis", C("oasis", "mama", "head", 1100, -60, 60), "Let's say it together. Camels chew it again!", part=3, q=True, tag="say chew again", hide=["milo"],
      pcam=V("oasis", "mama", "head", 1400, -60, 160), fx=[CHEW("w:chew", "mama", 2.0), ("hop", "w:together.", "sandy")],
      words=[("w:chew", "CHEW IT AGAIN!", .38, .14, .72, "sun", (.5, .3), .8)]),
    S("oasis", OSQ, "Does a camel chew its food again? Yes, or no?", part=3, q=True, tag="question 5", pause=3.2, hide=["milo"], pcam=OSQP, props=[SALT("sb", *OS_)],
      fx=[("signs", "w:again?", ["YES", "NO"], 0, "wait:2.0"), CHEW("wait:2.05", "mama", 1.0)]),
    S("oasis", say="Let's chew like a camel. Chew, chew, chew!", part=3, q=True, tag="chew", hide=["mama", "sandy"], fx=[("hop", "w:Chew,", "milo", 2)],
      words=[("w:Chew,", "CHEW, CHEW!", .77, .16, 0.81, "sun", (.5, .33), .85)], **MILO("oasis")),
    S("zoo", (1060, 660, 1300), "And at the zoo, camels eat hay!", part=3, trans="iris", tag="hay at the zoo", pcam=(1100, 600, 1500),
      actors=[("mama", "camel", 1000, 960, .9)], props=[prop("hy", A5.hay, 1430, 975, .9, True)],
      fx=[("show", "w:hay!", "hy"), BEND("w:hay!", "mama", 2.0, 62)], words=[("w:hay!", "HAY!", .2, .2, 1.3, "sun", (.5, .3), 1.0)]),
    S("zoo", (1240, 720, 1000), "Mama munches the hay. Munch, munch!", part=3, tag="Mama eats hay", pcam=(1240, 660, 1200),
      actors=[("mama", "camel", 1000, 960, .9)], props=[prop("hy", A5.hay, 1430, 975, .9)],
      fx=[NECK("mama", 62), CHEW("w:munches", "mama", 2.6)], words=[("w:Munch,", "MUNCH!", .8, .2, 1.2, "sun", (.5, .35), 1.0)]),
    S("zoo", say="Pretend to munch some hay. Munch, munch!", part=3, q=True, tag="munch hay", fx=[("hop", "w:Munch,", "milo", 2)],
      words=[("w:Munch,", "MUNCH, MUNCH!", .77, .1, 0.72, "sun", (.5, .33), .8)], **MILO("zoo", 900)),
    S("paper_blue", BOARD, "Grass, leaves, twigs, thorns, and salty plants!", part=3, tag="board: everything", pcam=BOARDP,
      props=[FOOD("f0", "grass", 460, 480, .85, True, p=(740, 240, .7)), FOOD("f1", "leaf", 760, 480, .85, True, p=(1180, 240, .7)), FOOD("f2", "twig", 1060, 480, .85, True, p=(740, 500, .7)),
             FOOD("f3", "thorn", 1360, 480, .85, True, p=(1180, 500, .7)), FOOD("f4", "salt", 910, 760, .85, True, p=(960, 760, .7))],
      fx=[("show", "w:Grass,", "f0"), ("show", "w:leaves,", "f1"), ("show", "w:twigs,", "f2"), ("show", "w:thorns,", "f3"), ("show", "w:salty", "f4")]),
    S("dunes", say="Which camel lunch would you pick?", part=3, q=True, tag="your pick", hide=["sandy"], pause=1.6, fx=[("hop", "w:Which", "milo")], trans="iris",
      words=[("w:pick?", "WHICH ONE?", .77, .1, 0.77, "sun", (.5, .33), .85)], **MILO("dunes")),
    # ---------------------------------------------------------------- QUIZ + GOODBYE
    S("night", WIDE, "Time to remember what we learned!", part=4, trans="iris", tag="quiz time", cam2=(1000, 560, 1800), pcam=(900, 520, 1800),
      words=[("w:remember", "QUIZ TIME!", .5, .14, 1.3, "sun", (.5, .33))]),
    S("night", (960, 560, 1920), "What do camels eat? Plants, or candy?", part=4, q=True, tag="quiz 1", pause=3.2, hide=["milo"], pcam=(980, 470, 2000),
      fx=[("signs", "w:Plants,", ["PLANTS", "CANDY"], 0, "wait:2.0")]),
    S("paper_blue", BOARD, "Plants! Grass, leaves, and twigs.", part=4, tag="board: plants again", pcam=BOARDP, props=LUNCH(),
      fx=[("to", "w:Grass,", "#{p}f0_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, ""), ("to", "w:leaves,", "#{p}f1_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, ""),
          ("to", "w:twigs.", "#{p}f2_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, "")], words=[("w:Plants!", "PLANTS!", .5, .16, 1.2, "sun", (.5, .56), 1.0)]),
    S("night", (1040, 600, 1700), "Can camels eat thorny plants? Yes, or no?", part=4, q=True, tag="quiz 2", pause=3.2, hide=["milo"], pcam=(1000, 500, 1900),
      fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("paper", BOARD, "Yes! With their big, tough lips.", part=4, tag="board: lips again", pcam=BOARDP, props=[prop("mz", A.muzzle, *MZ, p=MZP)],
      fx=LIPS("w:tough", 3), words=[("w:Yes!", "YES!", .82, .2, 1.2, "sun", (.5, .31), 1.0)]),
    S("paper", BOARD, "How many halves does a camel's top lip have? One, or two?", part=4, q=True, tag="quiz 3", pause=3.2, pcam=BOARDP,
      props=[prop("mz", A.muzzle, 960, 800, .65, p=(960, 720, .66))], fx=[("signs", "w:One,", ["ONE", "TWO"], 1, "wait:2.0")] + LIPS("wait:2.05", 3)),
    S("paper", BOARD, "Two! And each half wiggles on its own.", part=4, tag="board: two halves", pcam=BOARDP, props=[prop("mz", A.muzzle, *MZ, p=MZP)],
      fx=LIPS("w:wiggles", 5), words=[("w:Two!", "TWO!", .82, .2, 1.2, "sun", (.5, .31), 1.0)]),
    S("night", WIDE, "Thank you for learning with me, friends. See you at the zoo!", part=4, tag="goodbye", cam2=(960, 560, 1860), pcam=(900, 520, 1800),
      words=[("w:See", "SEE YOU AT THE ZOO!", .45, .12, .82, "pill", (.5, .33), .62)], fx=[("hop", "w:zoo!", "milo", 2), ("hop", "w:See", "sandy")]),
]
for _s in SHOTS:        # a picture board never drifts closer: it only pulls out a little (16:9 and 9:16)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)

SHORTS = [
    {"id": "zc_ep09_short1", "title": "What Does a Baby Camel Eat?", "band": ("WHAT DOES", "IT EAT?"), "thumb_text": "MUNCH, MUNCH!", "part": 1,
     "extra_first": [S("dunes", SANDY_D, "What does a camel eat, in the dry desert?", part=1, q=True, tag="hook: what does a camel eat", hide=["milo"], pcam=SANDY_DP,
                       props=[GRASS("gr", 1022, 942, .5)], fx=[("lookat", 0.2, "sandy", -10)], words=[("w:What", "?", .22, .2, 2.2, "sun", (.5, .33), 1.3)])]},
    {"id": "zc_ep09_short2", "title": "How Can Camels Eat Thorny Plants?", "band": ("PRICKLY", "LUNCH?"), "thumb_text": "TOUGH LIPS!", "part": 2,
     "extra_first": [S("trail", (1650, 590, 1150), "How can a camel munch a prickly, thorny plant?", part=2, q=True, tag="hook: thorny lunch", hide=["milo", "sandy"], pcam=(1710, 480, 1300),
                       props=[THORNS()], fx=[NECK("mama", 58), CHEW(0.3, "mama", 2.0)], words=[("w:How", "?", .24, .14, 2.2, "sun", (.5, .3), 1.3)])]},
    {"id": "zc_ep09_short3", "title": "Why Do Camels Chew Their Food Again?", "band": ("CHEW IT", "AGAIN?"), "thumb_text": "SALTY SNACK!", "part": 3,
     "extra_first": [S("oasis", C("oasis", "mama", "head", 900, -60, 40), "Why is this camel chewing, and chewing, and chewing?", part=3, q=True, tag="hook: chewing again", hide=["milo", "sandy"],
                       pcam=V("oasis", "mama", "head", 1200, -60, 120), fx=[CHEW(0.2, "mama", 3.0)], words=[("w:Why", "?", .2, .2, 2.2, "sun", (.5, .3), 1.3)])]},
]

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
THUMBS = {
    "zc_ep09": {"place": "trail", "cam": (1620, 610, 1250), "actors": [("camel", 1330, 900, .95, False, 'gsap.set("#P-neck",{rotation:58,svgOrigin:"190 -330"});')],
                "props": [(lambda p: art._thorn(p, 0, 0), 1850, 905, 1.5)],
                "words": [("THORNS?", 560, 260, 150, ""), ("YUM!", 560, 430, 190, "sun")]},
    "zc_ep09_short1": {"place": "dunes", "cam": (900, 760, 900), "actors": [("calf", 700, 935, .56, False, 'gsap.set("#P-neck",{rotation:62,svgOrigin:"190 -330"});')],
                       "props": [(A.grass, 1022, 942, .5)],
                       "words": [("MUNCH,", 540, 420, 190, ""), ("MUNCH!", 540, 620, 210, "sun")]},
    "zc_ep09_short2": {"place": "paper", "cam": (960, 520, 1300), "actors": [], "props": [(A.muzzle, 960, 900, .6)],
                       "words": [("TOUGH", 540, 400, 200, ""), ("LIPS!", 540, 600, 210, "sun")]},
    "zc_ep09_short3": {"place": "oasis", "cam": (640, 700, 1000), "actors": [("calf", 400, 915, .52, False, 'gsap.set("#P-neck",{rotation:40,svgOrigin:"190 -330"});')],
                       "props": [(A.saltbush, 730, 918, .55)],
                       "words": [("SALTY", 540, 420, 200, ""), ("SNACK!", 540, 620, 210, "sun")]},
}
