"""zc_ep07: "Who Looks After a Baby Elephant?" - cartoon fact lesson with Milo, Tumble the baby elephant and his family (3D music-and-sync process: "beat").
Three parts, each cut whole into one Short: 1. Mama (close to Mama, milk drunk with the mouth, a wobbly trunk), 2. the helpers (the herd is a family;
Auntie and big sister greet, watch and play; everyone helped the newborn stand), 3. Grandma leads (the oldest female leads to water and food, says when to rest).

FACTS, read at the source on Nov 18 2026, about 11:30 PM ET (each page fetched and its sentences quoted by the session's page reader):
 [SDZ] San Diego Zoo Wildlife Alliance, animals.sandiegozoo.org/animals/elephant
   "The little one uses its mouth to drink its mother's milk, so it doesn't need a long trunk yet to feed."
   "Calves are clumsy at first with their trunk, but they learn to use it as they grow older."
   "Calves stick close to Mom and nurse frequently"
   "Most elephants live in close social groups called herds, usually made up of related females and their offspring."
   "The leader of the herd is known as the matriarch; she is usually the oldest and most experienced female in the group."
   "Herd mates tend to naturally look out for calves."
   "rumbling and growling noises seems to signal to others that everything is "okay.""   "At birth, a baby elephant, called a calf, ..."
 [SW] SeaWorld, seaworld.org/animals/all-about/elephants/care-of-young/
   "Calves are able to stand on their own within minutes of birth."   "The newborn is helped to its feet by its mother and other females."
   "Mothers, aunts, sisters, and the matriarch are very important to calf development."
   "Mothers and aunts are in almost constant affectionate contact with the young, offering guidance and assistance."
 [NG] National Geographic, nationalgeographic.com/animals/article/elephant-nannies
   allomothers are "female elephants that help take care of calves that are not their own"; "elephant nannies spend a lot of time greeting and touching the baby";
   the relationship "includes a lot of play"; "moms get extra eyes on their young one" ... "while the moms can still go and forage".
 [MZ] Maryland Zoo, marylandzoo.org/animal/african-elephant
   the matriarch "leads the others to water and food, decides when to sleep and when to move."   "Baby and juvenile elephants in a herd have the benefit of multiple caregivers."
   allomothers (a babysitter) "keep watch over the youngest elephants, help them, comfort them, play with them."
 Read but NOT said: predators and the protective circle (not for this age), how long a calf nurses (the pages differ: six months, about 4 years), weights, the word "matriarch"
 (said as "the leader"). Adult elephants drinking with the trunk is zc_ep03's San Diego Zoo quote. Auntie, big sister and Grandma are characters of the story, drawn as
 Tumble's herd; "Auntie and big sister are like babysitters" rests on the National Geographic and Maryland Zoo pages.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_zc_ep07 as A
from kit import Kit, S, prop, W
from episodes.zc_ep02 import crossx, RV, DIP, TP

EP = {"id": "zc_ep07", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "Who Looks After a Baby Elephant?", "thumb_text": "WHOLE FAMILY!", "series": "Animal Facts with Milo",
      "description": ("Who looks after a baby elephant? Only Mama, or lots of elephants? Milo the bluebird visits baby elephant Tumble and his family to find out! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn that a baby elephant stays close to its mama and drinks her milk with its mouth, that a young elephant's trunk is wobbly at first, "
                      "that a herd is a family of mothers, aunts, sisters and their babies who help look after the little ones, that a newborn calf stands up within minutes, "
                      "and that the oldest female leads the herd to water and food.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (elephant); SeaWorld (elephant care of young); "
                      "National Geographic (elephant nannies); Maryland Zoo (African elephant)."),
      "tags": ["elephant", "elephants for kids", "baby elephant", "elephant family", "elephant herd", "savanna animals for kids", "animal facts for kids",
               "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "zoo": [("milo", "milo", 960, 940, 1.1, False, False)],
    "savanna": [("mama", "elephant", 1560, 930, .9, True), ("tumble", "tumble", 560, 936, .6), ("milo", "milo", 230, 490, .78, False, True)],
    "bigtree": [("auntie", "auntie", 1640, 930, .8, True), ("tumble", "tumble", 860, 936, .6), ("sister", "sister", 260, 934, .62), ("milo", "milo", 300, 400, .75, False, True)],
    "jungle": [("grandma", "grandma", 1340, 930, .62), ("mama", "elephant", 760, 930, .6), ("tumble", "tumble", 330, 936, .42), ("milo", "milo", 380, 470, .78, False, True)],
    "river": [("grandma", "grandma", 1500, 905, .8, True), ("tumble", "tumble", 560, 905, .55), ("milo", "milo", 300, 400, .7, False, True)],
    "zoo_eve": [("mama", "elephant", 1560, 944, .9, True), ("tumble", "tumble", 760, 940, .6), ("milo", "milo", 300, 420, .7, False, True)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920); INK = art.INK
CLOSE = {"tumble": (900, 936, .6)}                       # Tumble right next to Mama
TC = C("savanna", "tumble", "head", 880, 0, 20); TV = V("savanna", "tumble", "head", 1000, -30, 40)
MC = C("savanna", "mama", "head", 960, 100, 70); MV = V("savanna", "mama", "head", 1150, 80, 60)
_TS = [("tumble", "tumble", 900, 936, .6)]
TC2 = C("savanna", "tumble", "head", 880, 0, 20, stage=_TS); TV2 = V("savanna", "tumble", "head", 1000, -30, 40, stage=_TS)
SAV2 = (1110, 560, 1640); SAVQ = (1110, 520, 1700)
SAVP = WV("savanna", ["tumble", "mama"], stage=[("mama", "elephant", 1560, 930, .9, True), ("tumble", "tumble", 900, 936, .6)])
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 900))
WOB = lambda at, who="tumble", n=7: ("to", at, "#{p}" + who + "-trunk", {"rotation": 16, "svgOrigin": TP, "duration": .2, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, f"{who}'s trunk wobbles")
TRUNK_TO = lambda at, who, deg, d=.5: ("trunk", at, who, deg, d)

# the bigtree herd: Auntie, Tumble, big sister
BT = STAGES["bigtree"]
BTP = WV("bigtree", ["tumble", "auntie"], pad=.03); BSP = WV("bigtree", ["sister", "tumble"], pad=.03)
AC = C("bigtree", "auntie", "head", 900, 100, 60); AV = V("bigtree", "auntie", "head", 1150, 80, 60)
SC = C("bigtree", "sister", "head", 820, -40, 40); SV = V("bigtree", "sister", "head", 1050, -40, 60)
BTC = C("bigtree", "tumble", "head", 880, 0, 20); BTV = V("bigtree", "tumble", "head", 1000, -30, 40)
TWO = (1250, 600, 1300)                                   # Tumble and Auntie's trunks meeting
BQ = (960, 520, 2000)                                     # the three, low in the picture: room for the signs
# the jungle walk: Grandma in front, Mama, Tumble
JP = WV("jungle", ["tumble", "grandma"], pad=.02)
GC = C("jungle", "grandma", "head", 900, -60, 60); GV = V("jungle", "grandma", "head", 1100, -60, 70)
# the river
RGC = C("river", "grandma", "head", 900, 100, 60); RGV = V("river", "grandma", "head", 1150, 80, 60)
RP = WV("river", ["tumble", "grandma"], pad=.03)
HUG = [("mama", "elephant", 1560, 944, .9, True), ("tumble", "tumble", 760, 940, .6)]
HUGP = (1208, 400, 2600)


# ------------------------------------------------------------------ elephants as pictures on the boards (props: they have their own place in the 9:16 picture)
def ele(kind, flip=False):
    def f(pid):
        if kind == "mama": inner = art2.elephant(pid + "e")
        elif kind == "tumble": inner = art2.elephant(pid + "e", calf=True)
        else: inner = art2.elephant(pid + "e", c=A.SKIN[kind])
        return f'<g id="{pid}">' + (f'<g transform="scale(-1 1)">{inner}</g>' if flip else inner) + '</g>'
    return f


FAM = ["grandma", "mama", "auntie", "sister", "tumble"]
FX = [200, 590, 980, 1340, 1650]; FS = [.42, .42, .4, .34, .28]; FY = 800
FP = [(640, 640, .36), (1150, 640, .36), (560, 1150, .33), (930, 1150, .29), (1270, 1150, .24)]
FCAM = (925, 560, 2150); FPCAM = (930, 560, 2050)


def family(shown=(0, 1, 2, 3, 4), new=()):
    return [prop(f"f{k}", ele(FAM[k]), FX[k], FY, FS[k], k in new, p=FP[k]) for k in range(5) if k in shown or k in new]


# the milk board: a big Tumble, a drop of milk, an arrow to his mouth
MT = ("t", "tumble", 760, 1000, .95)
MOUTH = (760 + round(387 * .95), 1000 - round(327 * .95))          # (1128, 689)
MCAM = (1000, 560, 1700); MPCAM = (980, 640, 1900)
MILKP = lambda hidden=False: prop("mk", A.milk, 1500, 520, .9, hidden, p=(1240, 330, .7))
ARR = lambda hidden=True: prop("ar", lambda p: art.arrow(p, 1430, 610, MOUTH[0] + 50, MOUTH[1] - 10), 0, 0, 1, hidden)

# the newborn board: little Tumble wobbles, then stands; Mama and Auntie beside him
NB = [prop("nm", ele("mama", True), 1450, 860, .5, p=(1250, 900, .42)), prop("na", ele("auntie"), 470, 860, .5, p=(670, 900, .42))]
NT = lambda: prop("nt", ele("tumble"), 960, 880, .42, p=(960, 1350, .36))
NCAM = (960, 560, 1900); NPCAM = (960, 760, 1900)

SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("savanna", TC, "Who looks after baby Tumble?", q=True, tag="hook: who looks after", hide=["milo", "mama"], pcam=TV,
      words=[("w:Tumble?", "?", .2, .3, 3.0, "sun", (.75, .36), 1.6)], fx=[("face", 0.05, "tumble", "wow"), WOB("w:looks", n=5)]),
    S("savanna", SAV2, "Just his mama? Or lots of elephants?", tag="hook: guesses", hide=["milo"], pcam=SAVP, move=CLOSE,
      words=[("w:mama?", "MAMA?", .28, .22, 1.0, "", (.3, .29), .8), ("w:elephants?", "LOTS?", .7, .22, 1.0, "sun", (.7, .29), .8)], fx=[("nod", "w:mama?", "mama"), ("hop", "w:lots", "tumble")]),
    S("savanna", say="I'm Milo. Let's find out together!", tag="hook: Milo", hide=["tumble", "mama"], fx=[("hop", "w:find", "milo")], **MILO("savanna")),
    # ---------------------------------------------------------------- INTRO
    S("zoo", WIDE, "Welcome to The Animated Zoo, friends!", trans="iris", tag="gate wide", words=[("w:Animated", "HELLO!", .74, .6, 1.2, "pill")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, -40), "Today we fly to the sunny savanna.", tag="Milo close", words=[("w:savanna.", "THE SAVANNA", .5, .16, 1.1, "sun")]),
    S("savanna", WIDE, "Here we are! Look who is waiting for us.", trans="iris", tag="savanna wide", cam2=(960, 560, 1840), pcam=(700, 626, 1200), pcam2=WV("savanna", ["mama"]),
      fx=[("fromto", 0, "#{p}milo_w", {"x": -300, "y": 200}, {"x": 230, "y": 490, "duration": 1.3, "ease": "power2.out"}, "Milo flies in")]),
    S("savanna", (1110, 560, 1640), "This is Tumble. A baby elephant is called a calf.", tag="this is Tumble", hide=["milo"], pcam=(700, 626, 1200),
      words=[("w:Tumble.", "TUMBLE", .3, .26, 1.0, "pill", (.5, .31)), ("w:calf.", "A CALF", .3, .26, 1.0, "sun", (.5, .31))], fx=[("hop", "w:Tumble.", "tumble")]),
    # ---------------------------------------------------------------- PART 1: Mama
    S("savanna", MC, "Who looks after Tumble? Mama does, every day!", part=1, tag="Mama looks after him", hide=["milo", "tumble"], pcam=MV,
      fx=[("nod", "w:Mama", "mama")], words=[("w:Mama", "MAMA!", .8, .16, 1.2, "sun", (.5, .31))]),
    S("savanna", SAV2, "Tumble walks over and stays close to Mama.", part=1, tag="close to Mama", hide=["milo"], pcam=SAVP, pcam2=W(SAVP),
      fx=[("walk", 0.1, "tumble", 340, 2.4), ("face", "w:close", "tumble", "happy")], words=[("w:close", "CLOSE!", .3, .2, 1.1, "sun", (.5, .31))]),
    S("paper_pink", (960, 560, 1700), "Baby elephants stick close to their mamas.", part=1, tag="board: stick close",
      props=[prop("bm", ele("mama", True), 1240, 860, .62, p=(1120, 900, .55)), prop("bt", ele("tumble"), 640, 870, .44, p=(760, 900, .38))], pcam=(960, 640, 1900),
      fx=[("to", "w:close", "#{p}bt_w", {"x": "+=110", "duration": .8, "ease": "power2.out"}, "little Tumble moves close to Mama")],
      words=[("w:close", "CLOSE TO MAMA", .5, .16, 1.0, "pill", (.5, .36), .8)]),
    S("savanna", SAVQ, "Where is Tumble? Far away, or close to Mama?", part=1, q=True, tag="question 1", pause=3.2, hide=["milo"], move=CLOSE, pcam=SAVP,
      fx=[("signs", "w:Far", ["FAR", "CLOSE"], 1, "wait:2.0")]),
    S("savanna", SAV2, "Close to Mama! Close, close, close.", part=1, tag="answer 1", hide=["milo"], move=CLOSE, pcam=SAVP,
      fx=[("hop", "w:Close,", "tumble"), ("nod", "w:close.", "mama")], words=[("w:Close", "CLOSE!", .3, .2, 1.2, "sun", (.5, .31))]),
    S("savanna", (1180, 560, 1300), "Mama touches Tumble with her trunk, again and again.", part=1, tag="Mama's trunk", hide=["milo"], move=CLOSE, pcam=SAVP,
      fx=[TRUNK_TO("w:touches", "mama", -30, .5), TRUNK_TO("w:again", "mama", -10, .4), TRUNK_TO("w:again:2", "mama", -30, .4), ("face", "w:trunk,", "tumble", "happy")],
      words=[("w:again", "AGAIN!", .5, .16, 1.1, "sun", (.5, .31))]),
    S("savanna", say="Can you give yourself a big hug? Squeeze!", part=1, q=True, tag="hug along", hide=["tumble", "mama"], fx=[("hop", "w:Squeeze!", "milo")],
      words=[("w:hug?", "HUG!", .76, .22, 1.2, "sun", (.5, .31))], **MILO("savanna")),
    S("savanna", TC2, "Tumble is hungry. What does a baby elephant drink?", part=1, q=True, tag="hungry", hide=["milo", "mama"], move=CLOSE, pcam=TV2,
      fx=[("face", 0.05, "tumble", "wow")], words=[("w:drink?", "DRINK?", .2, .2, 1.2, "", (.5, .31))]),
    S("paper_blue", (960, 560, 1700), "Water, or milk? What do you think?", part=1, q=True, tag="question 2", pause=3.2, actors=[MT], pcam=MPCAM,
      fx=[("signs", "w:Water,", ["WATER", "MILK"], 1, "wait:2.0")]),
    S("paper_blue", MCAM, "Milk! Tumble drinks his mama's milk.", part=1, tag="board: milk", actors=[MT], props=[MILKP(True)], pcam=MPCAM,
      fx=[("show", "w:Milk!", "mk"), ("face", "w:drinks", "t", "happy")], words=[("w:Milk!", "MILK!", .22, .2, 1.3, "sun", (.5, .36), 1.0)]),
    S("paper_blue", (960, 560, 1700), "Does he drink it with his trunk, or with his mouth?", part=1, q=True, tag="question 3", pause=3.2, actors=[MT], pcam=MPCAM,
      fx=[("signs", "w:trunk,", ["TRUNK", "MOUTH"], 1, "wait:2.0"), WOB("w:trunk,", "t", 3)]),
    S("paper_blue", MCAM, "With his mouth! A baby elephant drinks milk with its mouth.", part=1, tag="board: mouth", actors=[MT], props=[MILKP(), ARR()], pcam=MPCAM,
      fx=[("show", "w:mouth!", "ar")], words=[("w:mouth!", "MOUTH!", .22, .2, 1.3, "sun", (.5, .36), 1.0)]),
    S("paper_blue", MCAM, "So he does not need a long trunk yet.", part=1, tag="board: not yet", actors=[MT], props=[MILKP(), ARR(False)], pcam=MPCAM,
      fx=[WOB("w:trunk", "t", 5)], words=[("w:yet.", "NOT YET!", .22, .2, 1.2, "pill", (.5, .36), 1.0)]),
    S("savanna", TC, "Tumble's trunk is short and wobbly. Wiggle, wobble!", part=1, tag="wobbly trunk", hide=["milo", "mama"], pcam=TV,
      fx=[WOB("w:wobbly.", n=11), ("face", "w:Wiggle,", "tumble", "happy")], words=[("w:Wiggle,", "WOBBLE!", .82, .2, 1.1, "sun", (.5, .31))]),
    S("savanna", (760, 600, 1200), "Is Tumble's trunk long, or short?", part=1, q=True, tag="question 3b", pause=3.2, hide=["milo", "mama"], pcam=(700, 626, 1200),
      fx=[("signs", "w:long,", ["LONG", "SHORT"], 1, "wait:2.0"), WOB("wait:2.05", n=3)]),
    S("savanna", TC, "Short! Short and wobbly, for now.", part=1, tag="answer 3b", hide=["milo", "mama"], pcam=TV,
      fx=[WOB("w:wobbly,", n=5), ("face", 0.05, "tumble", "happy")], words=[("w:Short!", "SHORT!", .82, .2, 1.2, "sun", (.5, .31))]),
    S("paper", (960, 560, 1500), "At first, a calf is clumsy with its trunk.", part=1, tag="board: clumsy", actors=[("t", "tumble", 800, 1000, .9)], pcam=(980, 640, 1800),
      fx=[WOB("w:clumsy", "t", 9)], words=[("w:clumsy", "CLUMSY!", .2, .2, 1.2, "", (.5, .36), 1.0)]),
    S("paper", (960, 560, 1500), "But it learns to use its trunk as it grows.", part=1, tag="board: learns",
      props=[prop("gt", ele("tumble"), 900, 960, .7, p=(960, 1000, .62))], pcam=(980, 640, 1800),
      fx=[("to", "w:grows.", "#{p}gt_w", {"scale": 1.15, "transformOrigin": "50% 100%", "duration": .8, "ease": "power1.out"}, "little Tumble grows")],
      words=[("w:learns", "LEARNS!", .2, .2, 1.2, "sun", (.5, .36), 1.0)]),
    S("savanna", say="Can you wiggle your arm like a wobbly trunk? Wiggle, wiggle!", part=1, q=True, tag="wiggle along", hide=["tumble", "mama"],
      fx=[("hop", "w:Wiggle,", "milo", 2)], words=[("w:Wiggle,", "WIGGLE!", .76, .22, 1.0, "sun", (.5, .31))], **MILO("savanna")),
    S("savanna", SAV2, "Tumble drinks Mama's milk many times a day.", part=1, tag="many times", hide=["milo"], move=CLOSE, pcam=SAVP,
      props=[prop("m1", A.milk, 1060, 420, .4, True), prop("m2", A.milk, 1160, 360, .4, True), prop("m3", A.milk, 1260, 420, .4, True)],
      fx=[("show", "w:many", "m1"), ("show", "w:times", "m2"), ("show", "w:day.", "m3")], words=[("w:many", "MANY TIMES", .3, .2, 1.0, "pill", (.5, .31), .8)]),
    S("savanna", SAVQ, "Mama looks after Tumble. But is Mama the only one?", part=1, q=True, tag="only Mama", hide=["milo"], move=CLOSE, pcam=SAVP,
      fx=[("nod", "w:after", "mama"), ("face", "w:only", "tumble", "wow")], words=[("w:only", "ONLY MAMA?", .5, .2, 1.0, "sun", (.5, .31), .8)]),
    # ---------------------------------------------------------------- PART 2: the helpers
    S("bigtree", WIDE, "Here comes Tumble's family. This is the herd!", part=2, trans="iris", tag="bigtree wide", cam2=(1000, 560, 1840), pcam=BTP, pcam2=W(BTP), hide=["milo"],
      move={"tumble": (700, 936, .6)}, fx=[("walk", 0.1, "tumble", 160, 2.0), ("hop", "w:herd!", "sister")], words=[("w:herd!", "THE HERD", .5, .16, 1.2, "sun", (.5, .31))]),
    S("paper_pink", FCAM, "A herd is a family: mamas, aunties, big sisters and babies.", part=2, tag="board: a family", pcam=FPCAM, props=family((), (1, 2, 3, 4)),
      fx=[("show", "w:mamas,", "f1"), ("show", "w:aunties,", "f2"), ("show", "w:sisters", "f3"), ("show", "w:babies.", "f4")],
      words=[("w:family", "FAMILY", .5, .14, 1.2, "sun", (.5, .27), 1.0)]),
    S("bigtree", AC, "This is Auntie. Hello, Auntie!", part=2, tag="Auntie", hide=["milo", "tumble", "sister"], pcam=AV,
      fx=[("nod", "w:Hello,", "auntie")], words=[("w:Auntie.", "AUNTIE", .8, .16, 1.1, "pill", (.5, .31))]),
    S("bigtree", SC, "And this is Tumble's big sister.", part=2, tag="big sister", hide=["milo", "tumble", "auntie"], pcam=SV,
      fx=[("hop", "w:sister.", "sister")], words=[("w:big", "BIG SISTER", .25, .2, 1.0, "pill", (.5, .31), .8)]),
    S("bigtree", BQ, "Who is the smallest elephant here? Tumble, or Auntie?", part=2, q=True, tag="question 4a", pause=3.2, hide=["milo"], pcam=W(BTP, 1.6),
      fx=[("signs", "w:Tumble,", ["TUMBLE", "AUNTIE"], 0, "wait:2.0")]),
    S("bigtree", BTC, "Tumble! He is the baby of the herd.", part=2, tag="answer 4a", hide=["milo", "auntie", "sister"], pcam=BTV,
      fx=[("hop", "w:Tumble!", "tumble"), ("face", 0.05, "tumble", "happy")], words=[("w:baby", "THE BABY", .82, .2, 1.1, "pill", (.5, .31))]),
    S("bigtree", BQ, "Let's count them. One, two, three!", part=2, q=True, tag="count the three", hide=["milo"], pcam=W(BTP, 1.6),
      fx=[("hop", "w:One,", "sister"), ("hop", "w:two,", "tumble"), ("nod", "w:three!", "auntie")],
      words=[("w:One,", "1", .2, .26, 1.4, "sun", (.25, .3), 1.0), ("w:two,", "2", .45, .26, 1.4, "sun", (.5, .3), 1.0), ("w:three!", "3", .8, .26, 1.4, "sun", (.75, .3), 1.0)]),
    S("bigtree", TWO, "Auntie says hello. She touches Tumble with her trunk.", part=2, tag="Auntie's trunk", hide=["milo", "sister"], pcam=BTP,
      fx=[TRUNK_TO("w:touches", "auntie", -40, .6), ("face", "w:trunk.", "tumble", "happy")], words=[("w:hello.", "HELLO!", .5, .16, 1.1, "sun", (.5, .31))]),
    S("bigtree", (1250, 560, 1500), "Does Auntie say hello with her trunk, or with her tail?", part=2, q=True, tag="question 4", pause=3.2, hide=["milo", "sister"], pcam=W(BTP, 1.08),
      fx=[("signs", "w:trunk,", ["TRUNK", "TAIL"], 0, "wait:2.0")]),
    S("bigtree", TWO, "With her trunk! Pat, pat. Hello, Tumble!", part=2, tag="answer 4", hide=["milo", "sister"], pcam=BTP,
      fx=[TRUNK_TO("w:Pat,", "auntie", -40, .3), TRUNK_TO("w:pat.", "auntie", -20, .3), ("hop", "w:Hello,", "tumble")], words=[("w:trunk!", "TRUNK!", .5, .16, 1.2, "sun", (.5, .31))]),
    S("bigtree", say="Can you wave hello like a trunk? Hello, hello!", part=2, q=True, tag="wave along", hide=["tumble", "auntie", "sister"],
      fx=[("hop", "w:Hello,", "milo", 2)], words=[("w:wave", "WAVE!", .76, .22, 1.1, "sun", (.5, .31))], **MILO("bigtree")),
    S("bigtree", (620, 600, 1300), "Big sister plays with Tumble. Push, push, play!", part=2, tag="sister plays", hide=["milo", "auntie"], pcam=BSP,
      move={"tumble": (760, 936, .6)}, fx=[("walk", 0.1, "sister", 60, 1.0), ("hop", "w:Push,", "tumble"), ("hop", "w:play!", "sister"), ("face", "w:play!", "tumble", "happy")],
      words=[("w:play!", "PLAY!", .5, .16, 1.2, "sun", (.5, .31))]),
    S("paper", (960, 560, 1800), "Helpers like Auntie and big sister are like babysitters.", part=2, tag="board: babysitters",
      props=[prop("ba", ele("auntie", True), 1350, 860, .55, p=(1180, 860, .45)), prop("bs", ele("sister"), 520, 870, .45, p=(700, 880, .38)), prop("bt", ele("tumble"), 920, 880, .32, p=(940, 1250, .3))],
      pcam=(960, 700, 2000), words=[("w:Helpers", "HELPERS!", .5, .16, 1.2, "sun", (.5, .27), 1.0)]),
    S("paper", (960, 560, 1800), "They watch Tumble, they help him, and they play with him.", part=2, tag="board: watch help play",
      props=[prop("ba", ele("auntie", True), 1350, 860, .55, p=(1180, 860, .45)), prop("bs", ele("sister"), 520, 870, .45, p=(700, 880, .38)), prop("bt", ele("tumble"), 920, 880, .32, p=(940, 1250, .3))],
      pcam=(960, 700, 2000), fx=[("to", "w:play", "#{p}bt_w", {"y": "-=50", "duration": .2, "yoyo": True, "repeat": 3}, "little Tumble hops")],
      words=[("w:watch", "WATCH", .2, .16, 1.0, "pill", (.5, .2), .8), ("w:help", "HELP", .5, .16, 1.0, "pill", (.5, .27), .8), ("w:play", "PLAY", .8, .16, 1.0, "sun", (.5, .34), .8)]),
    S("savanna", MC, "And Mama can eat her grass. Munch, munch!", part=2, trans="iris", tag="Mama eats", hide=["milo", "tumble"], pcam=MV,
      props=[prop("gr", A.grass, 1110, 830, .8)],
      fx=[TRUNK_TO(0.2, "mama", -30, .5), ("to", "w:eat", "#{p}gr_w", {"x": 1250, "y": 600, "scale": .3, "opacity": 0, "transformOrigin": "50% 50%", "duration": .6, "ease": "power2.in"}, "Mama eats the grass"),
          TRUNK_TO("w:Munch,", "mama", 0, .5)], words=[("w:Munch,", "MUNCH!", .8, .16, 1.2, "sun", (.5, .31))]),
    S("bigtree", BQ, "How many helpers are with Tumble? One, or two?", part=2, q=True, tag="question 5", pause=3.2, hide=["milo"], trans="iris", pcam=W(BTP, 1.6),
      fx=[("signs", "w:One,", ["ONE", "TWO"], 1, "wait:2.0")]),
    S("bigtree", (960, 560, 1920), "Two! Auntie and big sister.", part=2, tag="answer 5", hide=["milo"], pcam=W(BTP, 1.6),
      fx=[("nod", "w:Auntie", "auntie"), ("hop", "w:sister.", "sister")], words=[("w:Two!", "2 HELPERS", .5, .16, 1.1, "sun", (.5, .3), .8)]),
    S("paper_blue", NCAM, "When Tumble was born, he stood up in just minutes.", part=2, tag="board: stood up", props=NB + [NT()], pcam=NPCAM,
      fx=[("fromto", 0.1, "#{p}nt_w", {"rotation": -8, "transformOrigin": "50% 100%"}, {"rotation": 8, "duration": .3, "yoyo": True, "repeat": 5, "ease": "sine.inOut"}, "little Tumble wobbles"),
          ("to", "w:stood", "#{p}nt_w", {"rotation": 0, "duration": .3}, "Tumble stands")], words=[("w:minutes.", "UP!", .5, .16, 1.4, "sun", (.5, .27), 1.0)]),
    S("paper_blue", NCAM, "Mama and the other elephants helped him up.", part=2, tag="board: helped him up", props=NB + [NT()], pcam=NPCAM,
      fx=[("to", "w:Mama", "#{p}nm_w", {"x": "-=80", "duration": .6}, "Mama comes close"), ("to", "w:other", "#{p}na_w", {"x": "+=80", "duration": .6}, "Auntie comes close")],
      words=[("w:helped", "HELP!", .5, .16, 1.3, "sun", (.5, .27), 1.0)]),
    S("bigtree", say="Can you stand up tall like Tumble? Stand up, stand tall!", part=2, q=True, tag="stand along", hide=["tumble", "auntie", "sister"],
      fx=[("hop", "w:Stand:2", "milo", 2)], words=[("w:tall", "STAND UP!", .76, .22, 1.0, "sun", (.5, .31), .8)], **MILO("bigtree")),
    S("bigtree", (960, 560, 1920), "Lots of helpers! But who leads the whole herd?", part=2, q=True, tag="who leads", hide=["milo"], pcam=W(BTP, 1.6),
      fx=[("face", "w:leads", "tumble", "wow")], words=[("w:leads", "WHO LEADS?", .5, .16, 1.0, "sun", (.5, .3), .8)]),
    # ---------------------------------------------------------------- PART 3: Grandma leads
    S("jungle", WIDE, "Meet Grandma. She is the oldest elephant in the herd.", part=3, trans="iris", tag="jungle wide", cam2=(1000, 560, 1840), pcam=JP, pcam2=W(JP), hide=["milo"],
      fx=[("nod", "w:Grandma.", "grandma")], words=[("w:oldest", "OLDEST", .7, .16, 1.1, "pill", (.5, .3))]),
    S("jungle", GC, "Grandma is the leader of the herd.", part=3, tag="Grandma leads", hide=["milo", "mama", "tumble"], pcam=GV,
      props=[prop("st", A.star, *P("jungle", "grandma", "top", 0, -90), 1.0, True)], fx=[("show", "w:leader", "st")], words=[("w:leader", "LEADER", .2, .16, 1.2, "sun", (.5, .31))]),
    S("paper_pink", (960, 560, 1500), "The leader is the oldest female. She knows the most.", part=3, tag="board: oldest female",
      props=[prop("gg", ele("grandma"), 860, 900, .7, p=(900, 1000, .6)), prop("st", A.star, 1180, 330, 1.0, True, p=(1150, 420, .8))], pcam=(960, 700, 1900),
      fx=[("show", "w:knows", "st")], words=[("w:oldest", "OLDEST", .2, .18, 1.2, "pill", (.5, .27), 1.0)]),
    S("jungle", (960, 520, 2000), "Who leads the herd? Tumble, or Grandma?", part=3, q=True, tag="question 6", pause=3.2, hide=["milo"], pcam=W(JP, 1.1),
      fx=[("signs", "w:Tumble,", ["TUMBLE", "GRANDMA"], 1, "wait:2.0")]),
    S("jungle", GC, "Grandma! Everyone follows Grandma.", part=3, tag="answer 6", hide=["milo", "mama", "tumble"], pcam=GV,
      fx=[("nod", "w:Grandma!", "grandma")], words=[("w:Grandma!", "GRANDMA!", .2, .16, 1.2, "sun", (.5, .31))]),
    S("jungle", WIDE, "Grandma leads the herd to water and food.", part=3, tag="to water and food", cam2=(1160, 560, 1920), hide=["milo"], pcam=JP, pcam2=W(JP, 1.12),
      move={"grandma": (1140, 930, .62), "mama": (560, 930, .6), "tumble": (130, 936, .42)},
      fx=[("walk", 0.1, "grandma", 320, 3.2), ("walk", 0.1, "mama", 320, 3.2), ("walk", 0.1, "tumble", 320, 3.2)],
      words=[("w:water", "WATER", .3, .16, 1.0, "pill", (.3, .3), .8), ("w:food.", "FOOD", .7, .16, 1.0, "sun", (.7, .3), .8)]),
    S("jungle", (1100, 600, 1500), "Follow the leader! Step, step, step.", part=3, tag="follow the leader", hide=["milo", "grandma"], pcam=WV("jungle", ["tumble", "mama"], pad=.03),
      move={"mama": (900, 930, .6), "tumble": (470, 936, .42)},
      fx=[("walk", 0.1, "mama", 120, 2.6), ("walk", 0.1, "tumble", 120, 2.6), ("hop", "w:Step,", "tumble")], words=[("w:Follow", "FOLLOW!", .5, .16, 1.2, "sun", (.5, .31))]),
    S("jungle", GC, "Grandma decides when to walk, and when to stop.", part=3, tag="walk and stop", hide=["milo", "mama", "tumble"], pcam=GV,
      fx=[("nod", "w:walk,", "grandma"), ("blinkslow", "w:stop.", "grandma-eye", 1)], words=[("w:walk,", "WALK", .2, .16, 1.0, "pill", (.5, .27), .9), ("w:stop.", "STOP", .2, .3, 1.0, "sun", (.5, .35), .9)]),
    S("jungle", say="Can you march like an elephant? Stomp, stomp, stomp!", part=3, q=True, tag="march along", hide=["tumble", "mama", "grandma"],
      fx=[("hop", "w:Stomp,", "milo", 3)], words=[("w:Stomp,", "STOMP!", .76, .22, 1.1, "sun", (.5, .31))], **MILO("jungle")),
    S("river", WIDE, "Here is the river. Grandma knew the way!", part=3, trans="iris", tag="river wide", cam2=(1000, 560, 1780), pcam=RP, pcam2=W(RP), props=RV(), hide=["milo"],
      move={"tumble": (300, 905, .55), "grandma": (1760, 905, .8, True)}, fx=[("walk", 0, "tumble", 260, 3.0), ("walk", 0, "grandma", -260, 3.0)], words=[("w:river.", "RIVER", .5, .16, 1.3, "sun")]),
    S("river", (1180, 660, 1000), "Grandma has a long, cool drink. Slurp!", part=3, tag="Grandma drinks", hide=["milo", "tumble"], pcam=RGV, props=RV(),
      fx=[("to", 0.1, "#{p}grandma-trunk", DIP, "Grandma's trunk dips into the water")], words=[("w:Slurp!", "SLURP!", .22, .27, 1.3, "sun", (.5, .31))]),
    S("paper_pink", FCAM, "How many elephants are in Tumble's family? Let's count!", part=3, q=True, tag="count the family", pcam=FPCAM, props=family(),
      words=[("w:count!", "?", .5, .14, 1.8, "sun", (.5, .27), 1.2)]),
    S("paper_pink", FCAM, "One, two, three, four, five!", part=3, tag="board: five", pcam=FPCAM, props=family(),
      fx=[("to", f"w:{w}", f"#{{p}}f{k}_w", {"y": "-=60", "duration": .2, "yoyo": True, "repeat": 1}, f"elephant {k + 1} hops") for k, w in enumerate(["One,", "two,", "three,", "four,", "five!"])],
      words=[(f"w:{w}", str(k + 1), FX[k] / FCAM[2] + .5 - FCAM[0] / FCAM[2], .2, 1.3, "sun", (.5, .27), 1.0) for k, w in enumerate(["One,", "two,", "three,", "four,", "five!"])]),
    S("paper_pink", FCAM, "Five! Grandma, Mama, Auntie, big sister and Tumble.", part=3, tag="board: five names", pcam=FPCAM, props=family(),
      fx=[("to", f"w:{w}", f"#{{p}}f{k}_w", {"scale": 1.12, "transformOrigin": "50% 100%", "duration": .25, "yoyo": True, "repeat": 1}, "") for k, w in enumerate(["Grandma,", "Mama,", "Auntie,", "sister", "Tumble."])],
      words=[("w:Five!", "5!", .5, .14, 1.6, "sun", (.5, .27), 1.2)]),
    S("river", RGC, "Elephants can make a low rumble. It means: everything is okay.", part=3, tag="rumble", hide=["milo", "tumble"], pcam=RGV, props=RV(),
      fx=[("nod", "w:okay.", "grandma"), ("blinkslow", "w:rumble.", "grandma-eye", 1)], words=[("w:okay.", "OKAY!", .8, .16, 1.2, "sun", (.5, .31))]),
    S("river", say="Can you make a low rumble? Rumble, rumble!", part=3, q=True, tag="rumble along", hide=["tumble", "grandma"], props=RV(),
      fx=[("hop", "w:Rumble,", "milo")], words=[("w:Rumble,", "RUMBLE!", .76, .22, 1.0, "sun", (.5, .31))], **MILO("river")),
    S("zoo_eve", WIDE, "The sun goes down. Grandma says it is time to rest.", part=3, trans="iris", tag="evening wide", cam2=(1000, 560, 1780), pcam=WV("zoo_eve", ["tumble", "mama"], floor=.7),
      pcam2=W(WV("zoo_eve", ["tumble", "mama"], floor=.7)), hide=["milo"], move={"tumble": (440, 940, .6)}, fx=[("walk", 0, "tumble", 320, 3.0)], words=[("w:rest.", "REST", .5, .16, 1.2, "sun")]),
    S("zoo_eve", (1150, 620, 1100), "Tumble rests close to Mama. Cozy and happy!", part=3, tag="cozy", actors=HUG, pcam=HUGP, pcam2=HUGP,
      fx=[("face", "w:rests", "tumble", "sleepy"), ("trunk", "w:Mama.", "mama", -30, .6)], words=[("w:Cozy", "COZY!", .2, .2, 1.1, "sun", (.3, .31))]),
    S("zoo_eve", (960, 520, 1920), "Who looks after Tumble? Only Mama, or the whole family?", part=3, q=True, tag="question 7", pause=3.2, actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      fx=[("signs", "w:Only", ["MAMA", "FAMILY"], 1, "wait:2.0")]),
    S("paper_pink", FCAM, "The whole family! Mama, Auntie, big sister and Grandma.", part=3, tag="board: whole family", pcam=FPCAM, props=family(),
      fx=[("to", f"w:{w}", f"#{{p}}f{k}_w", {"y": "-=50", "duration": .2, "yoyo": True, "repeat": 1}, "") for k, w in ((1, "Mama,"), (2, "Auntie,"), (3, "sister"), (0, "Grandma."))],
      words=[("w:whole", "WHOLE FAMILY!", .5, .14, 1.0, "sun", (.5, .27), .8)]),
    S("zoo_eve", say="Big family, big love. Wow!", part=3, tag="wow", hide=["tumble", "mama"], fx=[("hop", "w:Wow!", "milo", 2)], words=[("w:Wow!", "WOW!", .76, .22, 1.3, "sun", (.5, .31))], **MILO("zoo_eve")),
    # ---------------------------------------------------------------- QUIZ + RECAP
    S("zoo_eve", WIDE, "Time to remember what we learned!", part=4, tag="quiz time", cam2=(1000, 560, 1760), actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      words=[("w:remember", "QUIZ TIME!", .62, .14, 1.3, "sun", (.5, .31))]),
    S("paper_blue", (960, 560, 1700), "How does Tumble drink his milk? With his trunk, or his mouth?", part=4, q=True, tag="quiz 1", pause=3.2, actors=[MT], pcam=MPCAM,
      fx=[("signs", "w:trunk,", ["TRUNK", "MOUTH"], 1, "wait:2.0")]),
    S("paper_blue", MCAM, "With his mouth!", part=4, tag="board: mouth again", actors=[MT], props=[MILKP(), ARR(False)], pcam=MPCAM,
      words=[("w:mouth!", "MOUTH!", .22, .2, 1.3, "sun", (.5, .36), 1.0)]),
    S("paper_pink", (960, 560, 1500), "Who leads the herd? Tumble, or Grandma?", part=4, q=True, tag="quiz 2", pause=3.2,
      props=[prop("gg", ele("grandma"), 1250, 940, .55, p=(1180, 1000, .45)), prop("tt", ele("tumble"), 600, 950, .42, p=(700, 1000, .34))], pcam=(960, 700, 1900),
      fx=[("signs", "w:Tumble,", ["TUMBLE", "GRANDMA"], 1, "wait:2.0")]),
    S("paper_pink", (960, 560, 1500), "Grandma, the oldest!", part=4, tag="board: Grandma again",
      props=[prop("gg", ele("grandma"), 860, 900, .7, p=(900, 1000, .6)), prop("st", A.star, 1180, 330, 1.0, p=(1150, 420, .8))], pcam=(960, 700, 1900),
      words=[("w:Grandma,", "GRANDMA!", .2, .18, 1.1, "sun", (.5, .27), 1.0)]),
    S("paper", (960, 560, 1800), "And who helps Mama look after Tumble?", part=4, q=True, tag="quiz 3", pause=1.6,
      props=[prop("bt", ele("tumble"), 920, 880, .32, p=(940, 1250, .3))], pcam=(960, 700, 2000), words=[("end+0.3", "?", .5, .2, 2.2, "sun", (.5, .3), 1.5)]),
    S("paper", (960, 560, 1800), "Auntie and big sister, the helpers!", part=4, tag="board: helpers again",
      props=[prop("ba", ele("auntie", True), 1350, 860, .55, p=(1180, 860, .45)), prop("bs", ele("sister"), 520, 870, .45, p=(700, 880, .38)), prop("bt", ele("tumble"), 920, 880, .32, p=(940, 1250, .3))],
      pcam=(960, 700, 2000), words=[("w:helpers!", "HELPERS!", .5, .16, 1.2, "sun", (.5, .27), 1.0)]),
    S("zoo_eve", (1150, 620, 1200), "Good night, Tumble. Good night, Mama.", part=4, tag="good night", actors=HUG, pcam=HUGP, pcam2=HUGP, props=[prop("h1", art2.heart, 1010, 440, 1.0, True)],
      fx=[("face", 0.02, "tumble", "sleepy"), ("show", "w:Mama.", "h1")]),
    S("zoo_eve", WIDE, "Thank you for learning with me, friends. See you at the zoo!", part=4, tag="goodbye", cam2=(960, 520, 2050), actors=HUG + [("milo", "milo", 300, 420, .7, False, True)], pcam=HUGP, pcam2=HUGP,
      words=[("w:See", "SEE YOU AT THE ZOO!", .6, .17, .95, "pill", (.5, .31), .62)], fx=[("hop", "w:zoo!", "milo", 2)]),
]
for _s in SHOTS:        # a picture board never drifts closer in 9:16: it only pulls out a little (zc_ep06)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)


def T(src, **kw):
    d = dict(next(x for x in SHOTS if x["tag"] == src)); d.update(kw); return d


SHORTS = [
    {"id": "zc_ep07_short1", "title": "What Does a Baby Elephant Drink?", "band": ("WHAT DOES", "HE DRINK?"), "thumb_text": "MOUTH OR TRUNK?", "part": 1,
     "extra_first": [S("savanna", TC, "What does a baby elephant drink?", part=1, q=True, tag="hook: what drink", hide=["milo", "mama"], pcam=TV,
                       fx=[("face", 0.05, "tumble", "wow"), WOB("w:drink?", n=5)], words=[("w:drink?", "?", .2, .3, 2.6, "sun", (.75, .36), 1.6)])]},
    {"id": "zc_ep07_short2", "title": "Who Helps Look After Tumble?", "band": ("WHO HELPS", "TUMBLE?"), "thumb_text": "BIG HELPERS!", "part": 2,
     "extra_first": [S("bigtree", TWO, "Who helps Mama look after Tumble?", part=2, q=True, tag="hook: who helps", hide=["milo", "sister"], pcam=BTP,
                       fx=[TRUNK_TO("w:helps", "auntie", -40, .6)], words=[("w:Tumble?", "?", .5, .2, 2.6, "sun", (.5, .33), 1.6)])]},
    {"id": "zc_ep07_short3", "title": "Who Leads an Elephant Herd?", "band": ("WHO LEADS", "THE HERD?"), "thumb_text": "FOLLOW GRANDMA!", "part": 3,
     "extra_first": [S("jungle", (960, 520, 2000), "Who leads an elephant herd?", part=3, q=True, tag="hook: who leads", hide=["milo"], pcam=W(JP, 1.1),
                       fx=[("nod", "w:leads", "grandma")], words=[("w:herd?", "?", .5, .2, 2.6, "sun", (.5, .33), 1.6)])]},
]
for _sh in SHORTS: _sh["band"] = tuple(_sh["band"])

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
THUMBS = {
    "zc_ep07": {"place": "savanna", "cam": (960, 540, 1920),
                "actors": [("elephant", 1100, 1000, .95, True, ""), ("tumble", 560, 1010, .6, False, ""), ("auntie", 1720, 1020, .72, True, ""), ("sister", 140, 1020, .6, False, "")],
                "props": [(art2.heart, 860, 330, 1.2)],
                "words": [("WHOLE FAMILY!", 960, 170, 170, "sun")]},
    "zc_ep07_short1": {"place": "paper_blue", "cam": MPCAM, "actors": [("tumble", 760, 1000, .95, False, "")],
                       "props": [(A.milk, 1240, 400, .7)],
                       "words": [("MOUTH", 540, 300, 170, "sun"), ("OR TRUNK?", 540, 470, 150, "")]},
    "zc_ep07_short2": {"place": "bigtree", "cam": BTP,
                       "actors": [("auntie", 1640, 930, .8, True, 'gsap.set("#P-trunk",{rotation:-40,svgOrigin:"392 -430"});'), ("tumble", 860, 936, .6, False, "")],
                       "props": [(art2.heart, 1240, 520, .9)],
                       "words": [("BIG", 540, 330, 170, ""), ("HELPERS!", 540, 500, 190, "sun")]},
    "zc_ep07_short3": {"place": "jungle", "cam": JP,
                       "actors": [("grandma", 1340, 930, .62, False, ""), ("elephant", 760, 930, .6, False, ""), ("tumble", 330, 936, .42, False, "")],
                       "props": [(A.star, 1530, 420, 1.0)],
                       "words": [("FOLLOW", 540, 320, 170, ""), ("GRANDMA!", 540, 490, 170, "sun")]},
}
