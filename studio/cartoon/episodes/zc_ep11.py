"""zc_ep11: "Whose Feet Are These? Guess With Milo" - the first Guess With Milo episode (2D, docs/CARTOON_RUN.md "Guess With Milo" and
"VIRAL PACKAGING"), a cartoon fact lesson with the 3D music-and-sync process ("beat"). Cold open on ONE giant footprint in the sand; Milo says his
name after the hook; the main intro (intro.py) right after the hook. Three parts, each cut whole into one Short, each opening on its own print with
two answer signs and thinking time BEFORE the animal walks in:
1. elephant (walks on tiptoes, a soft cushion under its toes that soaks up the bump, toenails: some have four on a front foot, some five; may feel rumbles with its feet),
2. giraffe (two hooves on each foot, feet as big as a dinner plate, walks moving the two legs of one side together, then the other side, so its legs do not bump),
3. zebra (one toe on each foot, inside one hoof that wraps round it and keeps it safe, a hoof keeps growing, every zebra has its own stripes).
Quiz with the three prints, the footprint trail recap, the closing names the next Guess With Milo ("Whose Ears Are These?").

FACTS, read at the source on Nov 20 2026, about 1:35-1:45 PM ET (pages read by the session's page reader, which quotes the sentences it finds; every page below was read):
 [SDZ-E] San Diego Zoo Wildlife Alliance Library, African elephant fact sheet, Physical Characteristics, ielc.libguides.com/sdzg/factsheets/african_elephant/characteristics
   "Elephants walk "on tiptoes," with bone digits angled toward ground"   "Large, wedge-shaped" "fat pads" cushion bottoms of feet   "Absorb shock from impact with ground"
   "4 to 5 nails on forefeet, 3 to 5 on hind feet" (savanna elephant)   "May detect vibrations through their feet, bones, and inner ear structures"
 [SDZ-EB] same library, African elephant, Behavior: "Fatty pad beneath bones in foot might help elephants sense ground vibrations"
 [LS] Live Science, "Giraffe Facts & Photos", livescience.com/27336-giraffes.html
   "Giraffes are even-toed ungulates, which means they have two weight-bearing hooves on each foot"   "their feet are 12 inches (30.5 cm) across"
 [SDZ] San Diego Zoo Wildlife Alliance, Animals and Plants, Giraffe (animals.sandiegozoo.org/node/66)
   "A giraffe's feet are the size of a dinner plate—12 inches across (30.5 centimeters)."
   "Giraffes have a way of moving, or gait, in which both the front and back legs on one side move forward together, then the other two legs on the other side move forward."
 [SDZ-G] SDZWA Library, Giraffe, Behavior, ielc.libguides.com/sdzg/factsheets/giraffes/behavior
   "Alternate moving the two right limbs together and then the two left."   "Advantage: keeps front legs from tangling with hind legs."
 [SDZ-Z] SDZWA Library, Plains zebra, Physical Characteristics, ielc.libguides.com/sdzg/factsheets/plains_zebra/characteristics
   "Single toe at terminus of each limb"   "Hooves enclose and protect the toe"   "Modified skin, grows continually"
   "All zebras have a unique arrangement of stripes which can be used to identify individuals."
 Said as: an elephant walks on its tiptoes [SDZ-E]; under its toes is a big, soft cushion [SDZ-E "fat pads cushion bottoms of feet"]; the cushion soaks up the bump
 when the heavy elephant steps down [SDZ-E "Absorb shock from impact with ground"]; elephants have toenails, some have four on a front foot and some have five [SDZ-E];
 elephants may feel tiny rumbles in the ground with their feet [SDZ-E, SDZ-EB, both say "may"/"might"]; a giraffe has two hooves on each foot [LS]; its feet are
 as big as a dinner plate [SDZ, LS]; it moves the two legs on one side together, then the two legs on the other side [SDZ, SDZ-G]; so its front and back legs do not
 bump [SDZ-G "keeps front legs from tangling with hind legs"]; a zebra walks on one toe on each foot [SDZ-Z]; the hoof wraps round the toe and keeps it safe [SDZ-Z];
 a hoof keeps growing, all the time [SDZ-Z "grows continually"], "a little like your fingernails" (a comparison for children, not a source claim);
 every zebra has its very own stripes, no two zebras are the same [SDZ-Z].
 Read but NOT said: nails on hind feet, speeds, leg length in feet, the calf that stands an hour after birth (no calf drawn), heights and weights.
 Footprint drawings: the elephant's big and round with nail marks, the giraffe's two halves (two hooves), the zebra's one smooth hoof (one toe) - drawn from the facts above.
 Nobody is hurt, lost, crying or trapped; the animals walk in happily and leave their prints; the "lion" is only a word on a sign.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_zc_ep11 as A
from kit import Kit, S, prop, W
from intro import INTRO_STAGES, intro_shots

EP = {"id": "zc_ep11", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "Whose Feet Are These? Guess With Milo", "thumb_text": "WHO?", "series": "Guess With Milo",
      "description": ("Look! A giant footprint in the sand. Who made it? Follow the footprints with Milo the bluebird and guess the animal before it walks in! "
                      "A gentle guessing game for ages 2-6 with answer signs, thinking time, things to count, moves to copy and a quiz at the end.\n"
                      "Kids learn that an elephant walks on its tiptoes, on a big, soft cushion that soaks up the bump of each step, and that some elephants have four "
                      "toenails on a front foot and some have five; that a giraffe has two hooves on each foot, feet as big as a dinner plate, and walks by moving the two "
                      "legs on one side together; and that a zebra walks on one toe on each foot, inside one hoof that keeps growing, and that every zebra has its own stripes.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance Library (African elephant, giraffe and plains zebra fact sheets); "
                      "San Diego Zoo Wildlife Alliance (giraffe); Live Science (giraffe facts)."),
      "tags": ["whose feet are these", "guess with milo", "guess the animal", "animal footprints for kids", "elephant feet", "giraffe hooves", "zebra hooves",
               "animal facts for kids", "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "sandtrail": [("milo", "milo", 300, 560, .75, False, True)],
    "river": [("ele", "elephant", 1150, 905, .82), ("milo", "milo", 300, 520, .72, False, True)],
    "savanna": [("gir", "giraffe", 1020, 935, .62), ("milo", "milo", 300, 520, .72, False, True)],
    "zoo": [("milo", "milo", 960, 940, 1.1)],
    "zoo_eve": [("milo", "milo", 960, 940, 1.0)],
    **INTRO_STAGES,
}
ZEB = [("zeb", "zebra", 1080, 930, .95), ("milo", "milo", 300, 520, .72, False, True)]       # the zebra by the river (actors= of the zebra shots)
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 1100, 0, -90))
BOARD = (960, 540, 1500); BOARDP = (960, 440, 1700); BOARD2 = (960, 600, 1300)


def PULSE(at, sel, k=1.2, n=1, o="50% 50%"): return ("to", at, sel, {"scale": k, "transformOrigin": o, "duration": .2, "yoyo": True, "repeat": 2 * n - 1}, "")


def SQUISH(at, sel, n=1): return ("to", at, sel, {"scaleY": .8, "scaleX": 1.08, "transformOrigin": "50% 100%", "duration": .18, "yoyo": True, "repeat": 2 * n - 1}, "the cushion squishes")


# the giraffe walks: both legs of ONE side together (SDZWA). near side = fl + bl, far side = fl2 + bl2. forward = a negative turn (it faces right)
_GL = art2.RIGS["giraffe"]["legs"]; _GH = art2.RIGS["giraffe"]["hip"]
def SIDE(at, who, side, deg=-18):
    legs = ("fl", "bl") if side == "near" else ("fl2", "bl2")
    return [("to", at, f"#{{p}}{who}-{lg}", {"rotation": deg, "svgOrigin": f"{_GL[lg]} {_GH}", "duration": .26, "yoyo": True, "repeat": 1, "ease": "sine.inOut"},
             f"the giraffe's {side} legs step together" if lg in ("fl", "fl2") else "") for lg in legs]


def STEP(at, who, dx=60): return ("to", at, f"#{{p}}{who}_w", {"x": f"+={dx}", "duration": .5, "ease": "sine.inOut"}, "")


# ------------------------------------------------------------------ the prints in the sand (sandtrail): elephant, giraffe, zebra, left to right
PX = {"pe": (560, 1090), "pg": (960, 1080), "pz": (1360, 1090)}
def PRINTS(hid=(), s=1.0, only=None):
    fns = {"pe": A.print_elephant, "pg": A.print_giraffe, "pz": A.print_zebra}
    return [prop(n, fns[n], PX[n][0], PX[n][1], s, n in hid) for n in (only or fns)]
def BIG(name, fn, s=1.7): return [prop(name, fn, 960, 1090, s, p=(960, 1080, s * .95))]       # one print alone, big, in the middle of the path
PCLOSE = (960, 1075, 1150); PCLOSEP = (960, 960, 1300)                                          # close on one print (16:9, 9:16)
PQ = (960, 1010, 1500); PQP = (960, 920, 1500)                                                    # the print question: the print low, the signs above it
TRAIL = (970, 990, 1500); TRAILP = (970, 900, 1700)
QM = lambda x=1480, y=860, s=.8, hid=False: prop("qm", A.qmark, x, y, s, hid, p=(1240, 640, .7))

# ------------------------------------------------------------------ cameras on the animals
EB = C("river", "ele", "body", 1300, 40, -100); EBP = WV("river", ["ele"], floor=.72, top=.44, pad=.08)
EH = C("river", "ele", "head", 1050, -60, 60); EHP = V("river", "ele", "head", 1300, -60, 120)
EF = C("river", "ele", "feet", 1150, 20, -150); EFP = V("river", "ele", "legs" if "legs" in kit.PT["elephant"] else "feet", 1300, 20, -260)
GB = C("savanna", "gir", "all", 1500, 0, -80); GBP = WV("savanna", ["gir"], floor=.76, top=.40, pad=.06)
GL = C("savanna", "gir", "legs", 1150, 20, -40); GLP = WV("savanna", ["gir"], floor=.76, top=.48, pad=.06)
GHD = C("savanna", "gir", "head", 1000, -80, 120); GHDP = V("savanna", "gir", "head", 1200, -60, 200)
ZB = C("river", "zeb", "body", 1250, 60, -60, stage=ZEB); ZBP = WV("river", ["zeb"], stage=ZEB, floor=.72, top=.44, pad=.08)
ZL = C("river", "zeb", "legs", 1050, 20, -10, stage=ZEB); ZLP = V("river", "zeb", "legs", 1150, 20, -100, stage=ZEB)
ZH = C("river", "zeb", "head", 950, -60, 80, stage=ZEB); ZHP = V("river", "zeb", "head", 1150, -40, 160, stage=ZEB)

# walk-ins: the animal starts off-screen left and walks onto the path
def WALKIN(who, kind, y, s, x0, dx, d=2.2): return dict(actors=[(who, kind, x0, y, s)], fx=[("walk", "w:It", who, dx, d)])

# picture boards: the foot close-ups
EFC = lambda name="fc", x=960, y=840, s=1.15, p=(960, 800, 1.4): prop(name, A.ele_foot_cut, x, y, s, p=p)
EFF = lambda name="ff", x=960, y=820, s=1.15, p=(960, 800, 1.4): prop(name, A.ele_foot_front, x, y, s, p=p)
GFT = lambda name="gf", x=960, y=840, s=1.25, p=(960, 800, 1.5): prop(name, A.gir_foot, x, y, s, p=p)
ZFC = lambda name="zf", x=960, y=840, s=1.25, p=(960, 800, 1.5): prop(name, A.zeb_foot_cut, x, y, s, p=p)

SHOTS = [
    # ---------------------------------------------------------------- HOOK (cold open on the promise: one giant print, the title's question)
    S("sandtrail", PCLOSE, "Look! A giant footprint in the sand! Who made it?", q=True, tag="hook: the giant print", hide=["milo"], pcam=PCLOSEP, cam2=W(PCLOSE, 1.06),
      props=BIG("pe", A.print_elephant) + [QM(1380, 960, .7)], fx=[PULSE("w:footprint", "#{p}pe_w", 1.08), PULSE("w:Who", "#{p}qm_w", 1.25, 2)],
      words=[("w:Who", "WHO?", .3, .34, 1.4, "sun", (.5, .34), 1.2)]),
    S("sandtrail", TRAIL, "And there are more! One, two, three mystery footprints!", q=True, tag="hook: three prints", hide=["milo"], pcam=TRAILP, cam2=W(TRAIL),
      props=PRINTS(("pe", "pg", "pz"), 1.2), fx=[("show", "w:One,", "pe"), ("show", "w:two,", "pg"), ("show", "w:three", "pz")],
      words=[("w:One,", "1", .27, .42, 1.2, "sun", (.22, .66), 1.0), ("w:two,", "2", .5, .42, 1.2, "sun", (.5, .66), 1.0), ("w:three", "3", .73, .42, 1.2, "sun", (.78, .66), 1.0)]),
    S("sandtrail", say="I'm Milo the bluebird. Let's play Guess With Milo!", q=True, tag="hook: Milo", props=PRINTS(), fx=[("hop", "w:Guess", "milo")],
      words=[("w:Guess", "GUESS!", .8, .45, 1.1, "sun", (.5, .33), .9)], **MILO("sandtrail", 900)),
    *intro_shots(),
    S("sandtrail", TRAIL, "Look closely at each footprint, and say your guess. Ready? Let's follow the footprints!", q=True, tag="follow the prints", trans="iris", pcam=TRAILP, cam2=W(TRAIL),
      props=PRINTS(), fx=[("fly", "w:follow", "milo", 1150, 800, 1.6), PULSE("w:footprint,", "#{p}pe_w,#{p}pg_w,#{p}pz_w", 1.12)],
      words=[("w:Ready?", "READY?", .3, .36, 1.1, "sun", (.5, .34), .9)]),
    # ---------------------------------------------------------------- PART 1: the elephant
    S("sandtrail", PCLOSE, "Here is a footprint. It is big, and round. Whose foot made it?", part=1, q=True, tag="print 1", hide=["milo"], pcam=PCLOSEP, cam2=W(PCLOSE, 1.06),
      props=BIG("pe", A.print_elephant), fx=[PULSE("w:big,", "#{p}pe_w", 1.1), PULSE("w:round.", "#{p}pe_w", 1.1)],
      words=[("w:big,", "BIG!", .3, .3, 1.2, "sun", (.3, .36), 1.0), ("w:round.", "ROUND!", .72, .3, 1.2, "sun", (.7, .36), 1.0)]),
    S("sandtrail", PQ, "Is it the elephant? Or is it the lion?", part=1, q=True, tag="question 1a", pause=3.2, hide=["milo"], pcam=PQP,
      props=BIG("pe", A.print_elephant, 1.5), fx=[("signs", "w:elephant?", ["ELEPHANT", "LION"], 0, "wait:2.0")]),
    S("sandtrail", (960, 680, 1900), "It is the elephant!", part=1, tag="the elephant walks in", pause=1.2, hide=["milo"], pcam=(1000, 560, 1900), props=PRINTS(only=("pe",)),
      **WALKIN("ele", "elephant", 1000, .72, -420, 1500, 2.4), words=[("e:elephant!", "ELEPHANT!", .3, .32, 1.1, "sun", (.5, .33), .9)]),
    S("paper", BOARD, "Here is the fun fact. An elephant walks on its tiptoes!", part=1, tag="board: tiptoes", pcam=BOARDP, props=[EFC()],
      fx=[PULSE("w:tiptoes!", "#{p}fc-bones", 1.08)], words=[("w:tiptoes!", "TIPTOES!", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    S("paper", BOARD2, "Under its toes is a big, soft cushion. Like a squishy pillow!", part=1, tag="board: cushion", pcam=(960, 560, 1500), props=[EFC()],
      fx=[SQUISH("w:cushion.", "#{p}fc-pad"), SQUISH("w:squishy", "#{p}fc-pad")], words=[("w:cushion.", "CUSHION", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    S("river", EH, "Why does an elephant need a cushion?", part=1, q=True, tag="why a cushion", pause=3.0, hide=["milo"], pcam=EBP,
      fx=[("lookat", "e:cushion?", "ele", -6)], words=[("e:cushion?", "?", .27, .36, 2.0, "sun", (.5, .34), 1.3)]),
    S("paper_blue", (960, 600, 1500), "The cushion soaks up the bump, when a big, heavy elephant steps down. Squish!", part=1, tag="board: soaks up the bump", pcam=BOARDP,
      props=[EFC(), prop("bp", A.bump, 700, 800, 1.0, p=(700, 760, 1.0)), prop("bp2", A.bump, 1230, 800, 1.0, p=(1220, 760, 1.0))], fx=[PULSE("w:bump,", "#{p}bp_w,#{p}bp2_w", 1.3), SQUISH("w:down.", "#{p}fc-pad"), SQUISH("w:Squish!", "#{p}fc-pad", 2)],
      words=[("w:Squish!", "SQUISH!", .5, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("sandtrail", (1000, 700, 1800), "Look at those big, round feet. Step, step!", part=1, tag="step step", hide=["milo"], pcam=(760, 600, 2100),
      actors=[("ele", "elephant", 520, 1000, .72)], fx=[("walk", "w:Step,:1", "ele", 380, 1.6)], words=[("w:Step,:1", "STEP, STEP!", .7, .26, 1.0, "sun", (.5, .33), .85)]),
    S("paper_pink", BOARD, "Elephants have toenails, too! Let's count them. One, two, three, four, five!", part=1, q=True, tag="board: count nails", pcam=BOARDP, props=[EFF()],
      fx=[PULSE(f"w:{w}", f"#{{p}}ff-n{k}", 1.35) for k, w in enumerate(("One,", "two,", "three,", "four,", "five!"))],
      words=[(f"w:{w}", str(k + 1), .26 + k * .12, .26, 1.0, "sun", (.14 + k * .18, .34), .9) for k, w in enumerate(("One,", "two,", "three,", "four,", "five!"))]),
    S("paper_pink", BOARD2, "Some elephants have four nails on a front foot. Some have five!", part=1, tag="board: four or five", pcam=(960, 560, 1500), props=[EFF()],
      fx=[PULSE("w:four", "#{p}ff-n0,#{p}ff-n1,#{p}ff-n2,#{p}ff-n3", 1.2), PULSE("w:five!", "#{p}ff-n0,#{p}ff-n1,#{p}ff-n2,#{p}ff-n3,#{p}ff-n4", 1.2)],
      words=[("w:four", "4", .24, .42, 1.4, "sun", (.3, .36), 1.1), ("w:five!", "5", .76, .42, 1.4, "sun", (.7, .36), 1.1)]),
    S("sandtrail", (1000, 760, 1400), "Elephants may even feel tiny rumbles in the ground, with their feet!", part=1, tag="rumbles", cam2=(1000, 760, 1470), hide=["milo"], pcam=(1000, 680, 1550), pcam2=(1000, 680, 1610), actors=[("ele", "elephant", 900, 955, .8)],
      props=[prop("rb", A.rumble, 1000, 975, 1.6, True, p=(1000, 990, 1.4))], fx=[("show", "w:rumbles", "rb"), PULSE("w:feet!", "#{p}rb_w", 1.15, 2)],
      words=[("w:rumbles", "RUMBLE!", .2, .45, .9, "sun", (.5, .3), .9)]),
    S("zoo", say="Put your hand flat on the floor. What can you feel?", part=1, q=True, tag="hand on the floor", pause=3.0, fx=[("hop", "w:feel?", "milo")],
      words=[("w:floor.", "HAND DOWN!", .72, .3, .8, "sun", (.5, .33), .8)], **MILO("zoo", 940)),
    S("river", EB, "Say it with me. An elephant walks on its tiptoes!", part=1, q=True, tag="say it: tiptoes", hide=["milo"], pcam=EBP, fx=[("nod", "w:tiptoes!", "ele")],
      words=[("w:Say", "SAY IT!", .27, .34, 1.1, "sun", (.5, .34), .9)]),
    S("zoo", say="Can you walk on your tiptoes, like an elephant? Tip, tip, tiptoe!", part=1, q=True, tag="tiptoe", pause=2.4, fx=[("hop", "w:Tip,:1", "milo"), ("hop", "w:tiptoe!", "milo")],
      words=[("w:Tip,:1", "TIP, TIP!", .72, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("paper_blue", BOARD, "Quick check! What is under an elephant's toes? A soft cushion, or a wheel?", part=1, q=True, tag="question 1b", cam2=(960, 560, 1280), pause=3.2, pcam=BOARDP,
      props=[EFC("fc", 960, 800, 1.0, p=(960, 800, 1.3))], fx=[PULSE("w:toes?", "#{p}fc_w", 1.08), SQUISH("wait:0.6", "#{p}fc-pad"), ("signs", "w:cushion,", ["CUSHION", "WHEEL"], 0, "wait:2.0"), SQUISH("wait:2.05", "#{p}fc-pad", 2), ("word", "e:wheel?", "?", {"x": 1380, "y": 600, "size": 200, "cls": "sun", "p": {"x": 1250, "y": 560, "size": 170}})]),
    S("river", EB, "A soft cushion! Squish, squish. Great job!", part=1, tag="great job 1", hide=["milo"], pcam=EBP, fx=[("walk", "w:Squish,:1", "ele", 140, 1.4)],
      words=[("w:Squish,:1", "SQUISH!", .27, .34, 1.2, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- PART 2: the giraffe
    S("sandtrail", PCLOSE, "Here is another footprint. Look! It has two halves, side by side. Whose foot made it?", part=2, q=True, tag="print 2", trans="iris", hide=["milo"],
      pcam=PCLOSEP, cam2=W(PCLOSE, 1.06), props=BIG("pg", A.print_giraffe),
      fx=[PULSE("w:two", "#{p}pg-a", 1.15), PULSE("w:halves,", "#{p}pg-b", 1.15)], words=[("w:two", "2", .72, .3, 1.6, "sun", (.72, .38), 1.2)]),
    S("sandtrail", PQ, "Is it the zebra? Or is it the giraffe?", part=2, q=True, tag="question 2a", pause=3.2, hide=["milo"], pcam=PQP,
      props=BIG("pg", A.print_giraffe, 1.5), fx=[("signs", "w:zebra?", ["ZEBRA", "GIRAFFE"], 1, "wait:2.0")]),
    S("savanna", (960, 540, 1920), "It is the giraffe!", part=2, tag="the giraffe walks in", pause=1.2, hide=["milo"], pcam=(1000, 470, 2100),
      **WALKIN("gir", "giraffe", 935, .58, -420, 1380, 2.4), words=[("e:giraffe!", "GIRAFFE!", .81, .64, 1.1, "sun", (.5, .33), .9)]),
    S("paper", BOARD, "Here is the fun fact. A giraffe has two hooves on each foot!", part=2, tag="board: two hooves", pcam=BOARDP, props=[GFT()],
      fx=[PULSE("w:two", "#{p}gf-h0,#{p}gf-h1", 1.12)], words=[("w:hooves", "2 HOOVES", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    S("paper", BOARD2, "Count the hooves with me. One, two!", part=2, q=True, tag="board: count hooves", pcam=(960, 560, 1500), props=[GFT()],
      fx=[PULSE("w:One,", "#{p}gf-h0", 1.3), PULSE("w:two!", "#{p}gf-h1", 1.3)],
      words=[("w:One,", "1", .36, .4, 1.4, "sun", (.3, .4), 1.1), ("w:two!", "2", .64, .4, 1.4, "sun", (.7, .4), 1.1)]),
    S("paper_blue", (960, 620, 1600), "And its feet are big! As big as a dinner plate.", part=2, tag="board: dinner plate", pcam=(960, 640, 1700),
      props=[prop("pl", A.plate_top, 960, 640, 1.1, p=(960, 640, 1.1)), prop("gp", A.print_giraffe, 960, 640, 1.9, p=(960, 640, 1.9))], fx=[PULSE("w:big!:1", "#{p}gp_w", 1.1), PULSE("w:plate.", "#{p}pl_w", 1.08)],
      words=[("w:big!:1", "BIG!", .26, .4, 1.2, "sun", (.5, .32), 1.0)]),
    S("savanna", GHD, "How does a giraffe walk, on such long legs?", part=2, q=True, tag="how does it walk", pause=3.0, hide=["milo"], pcam=GHDP,
      fx=[("lookat", "e:legs?", "gir", 6)], words=[("e:legs?", "?", .32, .32, 2.0, "sun", (.5, .34), 1.3)]),
    S("savanna", GL, "It moves the two legs on one side together. Then the two legs on the other side!", part=2, tag="legs: one side, then the other", hide=["milo"], pcam=GLP,
      props=[prop("a1", A.side_arrow, 1300, 760, 1.2, True, p=(1240, 760, 1.0))],
      fx=SIDE("w:together.", "gir", "near") + SIDE("w:other", "gir", "far") + [("show", "w:together.", "a1")],
      words=[("w:together.", "THIS SIDE!", .22, .4, .9, "sun", (.5, .32), .8), ("w:other", "THAT SIDE!", .22, .55, .9, "", (.5, .4), .8)]),
    S("savanna", GB, "Look! This side, this side. That side, that side!", part=2, q=True, tag="pace walk", hide=["milo"], pcam=GBP,
      fx=SIDE("w:This:1", "gir", "near") + SIDE("w:this:2", "gir", "near") + SIDE("w:That:1", "gir", "far") + SIDE("w:that:2", "gir", "far")
      + [STEP("w:This:1", "gir"), STEP("w:this:2", "gir"), STEP("w:That:1", "gir"), STEP("w:that:2", "gir")],
      words=[("w:This:1", "THIS SIDE!", .26, .4, .9, "sun", (.5, .34), .8), ("w:That:1", "THAT SIDE!", .26, .56, .9, "", (.5, .44), .8)]),
    S("savanna", GL, "That way, its front legs and its back legs do not bump!", part=2, tag="legs do not bump", hide=["milo"], pcam=GLP,
      fx=SIDE("w:front", "gir", "near") + SIDE("w:back", "gir", "far"), words=[("w:bump!", "NO BUMP!", .22, .4, 1.0, "sun", (.5, .34), .9)]),
    S("savanna", (900, 640, 1700), "And a baby giraffe can stand up and walk, about an hour after it is born!", part=2, tag="baby giraffe stands", hide=["milo"], pcam=(950, 560, 2000),
      actors=[("gir", "giraffe", 1200, 935, .58), ("calf", "giraffe", 640, 935, .3)],
      fx=[("fromto", "w:stand", "#{p}calf", {"scaleY": .55, "svgOrigin": "0 0"}, {"scaleY": 1, "duration": .9, "ease": "back.out(1.6)"}, "the baby giraffe stands up"),
          ("walk", "w:walk,", "calf", 160, 1.5), ("nod", "w:born!", "gir")],
      words=[("w:baby", "BABY!", .3, .36, 1.2, "sun", (.5, .34), 1.0)]),
    S("savanna", (760, 760, 1100), "Wobble, wobble, up it goes!", part=2, tag="wobble wobble", hide=["milo"], pcam=(760, 700, 1200),
      actors=[("calf", "giraffe", 760, 935, .3)],
      fx=[("to", "w:Wobble,:1", "#{p}calf", {"rotation": 4, "svgOrigin": "0 0", "duration": .2, "yoyo": True, "repeat": 5, "ease": "sine.inOut"}, "the baby giraffe wobbles")],
      words=[("w:Wobble,:1", "WOBBLE!", .27, .34, 1.1, "sun", (.5, .34), .9)]),
    S("zoo", say="Stand up tall, like a giraffe. Stretch!", part=2, q=True, tag="stand tall", pause=2.4, fx=[("hop", "w:Stretch!", "milo")],
      words=[("w:Stretch!", "STRETCH!", .72, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("savanna", GB, "Say it with me. A giraffe has two hooves on each foot!", part=2, q=True, tag="say it: two hooves", hide=["milo"], pcam=GBP, cam2=W(GB),
      fx=[("nod", "w:hooves", "gir")], words=[("w:Say", "SAY IT!", .26, .36, 1.1, "sun", (.5, .34), .9)]),
    S("zoo", say="Can you walk like a giraffe? This side, this side. That side, that side!", part=2, q=True, tag="walk like a giraffe", pause=2.4,
      fx=[("hop", "w:This:1", "milo"), ("hop", "w:this:2", "milo"), ("hop", "w:That:1", "milo"), ("hop", "w:that:2", "milo")],
      words=[("w:This:1", "THIS SIDE!", .72, .3, .8, "sun", (.5, .33), .8)], **MILO("zoo", 940)),
    S("paper_pink", BOARD, "Quick check! How many hooves are on each giraffe foot? Two, or ten?", part=2, q=True, tag="question 2b", cam2=(960, 560, 1280), pause=3.2, pcam=BOARDP,
      props=[GFT("gf", 960, 810, 1.05, p=(960, 800, 1.4))], fx=[PULSE("w:hooves", "#{p}gf_w", 1.08), PULSE("wait:0.6", "#{p}gf-h0,#{p}gf-h1", 1.1), ("signs", "w:Two,", ["TWO", "TEN"], 0, "wait:2.0"), PULSE("wait:2.05", "#{p}gf-h0,#{p}gf-h1", 1.15, 2), ("word", "e:ten?", "?", {"x": 1380, "y": 600, "size": 200, "cls": "sun", "p": {"x": 1250, "y": 560, "size": 170}})]),
    S("savanna", GB, "Two! Two hooves on every foot. Super thinking!", part=2, tag="super thinking", hide=["milo"], pcam=GBP, cam2=W(GB), fx=SIDE("w:Super", "gir", "near"),
      words=[("w:Two!:1", "TWO!", .26, .36, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- PART 3: the zebra
    S("sandtrail", PCLOSE, "Here is the last footprint. It is one smooth, round print. Whose foot made it?", part=3, q=True, tag="print 3", trans="iris", hide=["milo"],
      pcam=PCLOSEP, cam2=W(PCLOSE, 1.06), props=BIG("pz", A.print_zebra), fx=[PULSE("w:one", "#{p}pz_w", 1.12)],
      words=[("w:one", "1", .72, .3, 1.6, "sun", (.72, .38), 1.2)]),
    S("sandtrail", PQ, "Is it the elephant? Or is it the zebra?", part=3, q=True, tag="question 3a", pause=3.2, hide=["milo"], pcam=PQP,
      props=BIG("pz", A.print_zebra, 1.5), fx=[("signs", "w:elephant?", ["ELEPHANT", "ZEBRA"], 1, "wait:2.0")]),
    S("river", (960, 600, 1900), "It is the zebra!", part=3, tag="the zebra walks in", pause=1.2, pcam=(1000, 560, 1900), hide=["milo"],
      actors=[("zeb", "zebra", -400, 930, .9)], fx=[("walk", "w:It", "zeb", 1400, 2.2)], words=[("e:zebra!", "ZEBRA!", .28, .34, 1.2, "sun", (.5, .33), 1.0)]),
    S("paper", BOARD, "Here is the fun fact. A zebra walks on just one toe, on each foot!", part=3, tag="board: one toe", pcam=BOARDP, props=[ZFC()],
      fx=[PULSE("w:toe,", "#{p}zf-toe", 1.12, 2)], words=[("w:toe,", "1 TOE", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    S("paper", BOARD2, "Let's count the toes on one zebra foot. One! Just one!", part=3, q=True, tag="board: count one toe", pcam=(960, 560, 1500), props=[ZFC()],
      fx=[PULSE("w:One!:1", "#{p}zf-toe", 1.25), PULSE("w:one!:2", "#{p}zf-toe", 1.25)], words=[("w:One!:1", "1", .72, .36, 1.6, "sun", (.72, .4), 1.2)]),
    S("zoo", say="Hold up one finger, for one zebra toe. One!", part=3, q=True, tag="one finger", pause=2.4, fx=[("hop", "w:One!:3", "milo")],
      words=[("w:One!:3", "ONE!", .72, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("river", ZL, "So what is that hard part, at the bottom?", part=3, q=True, tag="the hard part", pause=3.0, hide=["milo"], actors=ZEB, pcam=ZBP,
      words=[("e:bottom?", "?", .15, .55, 2.0, "sun", (.5, .34), 1.3)]),
    S("paper_blue", BOARD, "It is a hoof! The hoof wraps around the toe, and keeps it safe.", part=3, tag="board: the hoof", pcam=BOARDP, props=[ZFC()],
      fx=[PULSE("w:hoof!:1", "#{p}zf-hoof", 1.08), PULSE("w:safe.", "#{p}zf-toe", 1.1)], words=[("w:hoof!:1", "HOOF!", .5, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("river", ZB, "Look at those strong hooves. Clip, clop, clip, clop!", part=3, tag="clip clop", hide=["milo"], actors=ZEB, pcam=ZBP, cam2=W(ZB),
      fx=[("walk", "w:Clip,:1", "zeb", 200, 1.8)], words=[("w:Clip,:1", "CLIP, CLOP!", .27, .34, 1.0, "sun", (.5, .34), .85)]),
    S("paper_blue", BOARD2, "A hoof keeps on growing, all the time. A little like your fingernails!", part=3, tag="board: hoof grows", pcam=(960, 560, 1500), props=[ZFC()],
      fx=[("to", "w:growing,", "#{p}zf-hoof", {"scaleY": 1.1, "transformOrigin": "50% 100%", "duration": 1.4, "ease": "power1.inOut", "yoyo": True, "repeat": 1}, "the hoof grows")],
      words=[("w:growing,", "IT GROWS!", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    S("river", ZL, "Four legs, four hooves! Count with me. One, two, three, four!", part=3, q=True, tag="count four hooves", hide=["milo"], actors=ZEB, pcam=ZBP,
      fx=[PULSE(f"w:{w}", f"#{{p}}zeb-{lg}", 1.08, 1, "50% 0%") for w, lg in (("One,", "bl"), ("two,", "bl2"), ("three,", "fl2"), ("four!:3", "fl"))],
      words=[("w:One,", "1", .3, .3, 1.2, "sun", (.2, .36), 1.0), ("w:two,", "2", .43, .3, 1.2, "sun", (.4, .36), 1.0), ("w:three,", "3", .57, .3, 1.2, "sun", (.6, .36), 1.0),
             ("w:four!:3", "4", .7, .3, 1.2, "sun", (.8, .36), 1.0)]),
    S("paper_pink", BOARD, "And every zebra has its very own stripes. No two zebras are the same!", part=3, tag="board: own stripes", pcam=(960, 560, 2100),
      actors=[("z1", "zebra", 560, 900, .62), ("z2", "zebra2", 1340, 900, .62, True)], fx=[("nod", "w:own", "z1"), ("nod", "w:same!", "z2")],
      words=[("w:own", "ALL DIFFERENT!", .5, .14, .9, "sun", (.5, .3), .7)]),
    S("river", ZH, "Say it with me. A zebra walks on one toe!", part=3, q=True, tag="say it: one toe", hide=["milo"], actors=ZEB, pcam=ZBP, fx=[("nod", "w:toe!", "zeb")],
      words=[("w:Say", "SAY IT!", .3, .32, 1.1, "sun", (.5, .34), .9)]),
    S("zoo", say="Can you trot like a zebra? Clip, clop, clip, clop!", part=3, q=True, tag="trot like a zebra", pause=2.4,
      fx=[("hop", "w:Clip,:1", "milo"), ("hop", "w:clip,:2", "milo")], words=[("w:Clip,:1", "CLIP, CLOP!", .72, .3, .8, "sun", (.5, .33), .8)], **MILO("zoo", 940)),
    S("paper", BOARD, "Quick check! How many toes are on each zebra foot? One, or five?", part=3, q=True, tag="question 3b", cam2=(960, 560, 1280), pause=3.2, pcam=BOARDP,
      props=[ZFC("zf", 960, 810, 1.05, p=(960, 800, 1.4))], fx=[PULSE("w:toes", "#{p}zf_w", 1.08), PULSE("w:foot?", "#{p}zf-hoof", 1.1), PULSE("wait:0.6", "#{p}zf-toe", 1.15), ("signs", "w:One,", ["ONE", "FIVE"], 0, "wait:2.0"), PULSE("wait:2.05", "#{p}zf-toe", 1.2, 2), ("word", "e:five?", "?", {"x": 1380, "y": 600, "size": 200, "cls": "sun", "p": {"x": 1250, "y": 560, "size": 170}})]),
    S("river", ZB, "One! One toe, inside one hoof. You remembered!", part=3, tag="you remembered", hide=["milo"], actors=ZEB, pcam=ZBP, cam2=W(ZB), fx=[("nod", "w:remembered!", "zeb")],
      words=[("w:One!:1", "ONE!", .27, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- QUIZ: the three prints again
    S("zoo_eve", WIDE, "Three footprints, and three friends! Now it is quiz time!", part=4, trans="iris", tag="quiz time", cam2=(960, 560, 1860), pcam=(960, 560, 1800),
      words=[("w:quiz", "QUIZ TIME!", .5, .3, 1.3, "sun", (.5, .33))], fx=[("hop", "w:quiz", "milo", 2)]),
    S("sandtrail", PQ, "Whose footprint has two halves? The giraffe's, or the elephant's?", part=4, q=True, tag="quiz 1", pause=3.2, hide=["milo"], pcam=PQP,
      props=BIG("pg", A.print_giraffe, 1.5), fx=[("signs", "w:giraffe's,", ["GIRAFFE", "ELEPHANT"], 0, "wait:2.0")]),
    S("savanna", GB, "The giraffe! Two hooves on each foot.", part=4, tag="quiz 1: giraffe", hide=["milo"], pcam=GBP, cam2=W(GB), fx=SIDE("w:giraffe!", "gir", "near"),
      words=[("w:giraffe!", "GIRAFFE!", .27, .36, 1.1, "sun", (.5, .34), .9)]),
    S("sandtrail", (960, 1000, 1600), "Whose footprint is one smooth hoof? The elephant's, or the zebra's?", part=4, q=True, tag="quiz 2", pause=3.2, hide=["milo"], pcam=(960, 900, 1600),
      props=BIG("pz", A.print_zebra, 1.5), fx=[("signs", "w:elephant's,", ["ELEPHANT", "ZEBRA"], 1, "wait:2.0")]),
    S("river", ZB, "The zebra! One toe, one hoof.", part=4, tag="quiz 2: zebra", hide=["milo"], actors=ZEB, pcam=ZBP, cam2=W(ZB), fx=[("nod", "w:zebra!", "zeb")],
      words=[("w:zebra!", "ZEBRA!", .27, .34, 1.2, "sun", (.5, .34), 1.0)]),
    S("sandtrail", (960, 1030, 1450), "Whose footprint is big and round? The lion's, or the elephant's?", part=4, q=True, tag="quiz 3", pause=3.2, hide=["milo"], pcam=(960, 940, 1450),
      props=BIG("pe", A.print_elephant, 1.5), fx=[("signs", "w:lion's,", ["LION", "ELEPHANT"], 1, "wait:2.0")]),
    S("river", EB, "The elephant! On its soft, squishy tiptoes.", part=4, tag="quiz 3: elephant", hide=["milo"], pcam=EBP, fx=[("nod", "w:elephant!", "ele")],
      words=[("w:elephant!", "ELEPHANT!", .28, .34, 1.1, "sun", (.5, .34), .9)]),
    # ---------------------------------------------------------------- RECAP + GOODBYE (the closing picture names the next Guess With Milo)
    S("sandtrail", (960, 640, 2000), "Look at our footprint trail! You guessed them all!", part=4, trans="iris", tag="the footprint trail", pcam=(980, 640, 2300),
      actors=[("ele", "elephant", 380, 860, .5), ("gir", "giraffe", 960, 850, .42), ("zeb", "zebra", 1500, 860, .6), ("milo", "milo", 1720, 420, .6, True, True)],
      props=[prop(n, fn, x, 985, .7) for n, fn, x in (("pe", A.print_elephant, 520), ("pg", A.print_giraffe, 960), ("pz", A.print_zebra, 1400))], fx=[PULSE("w:footprint", "#{p}pe_w,#{p}pg_w,#{p}pz_w", 1.15), ("hop", "w:all!", "milo")],
      words=[("w:all!", "YOU DID IT!", .5, .15, 1.0, "sun", (.5, .32), .85)]),
    S("zoo_eve", say="Tiptoe like an elephant. Walk this side, that side, like a giraffe. And trot like a zebra!", part=4, q=True, tag="all three moves", pause=1.6,
      fx=[("hop", "w:Tiptoe", "milo"), ("hop", "w:this", "milo"), ("hop", "w:that", "milo"), ("hop", "w:trot", "milo")],
      words=[("w:trot", "CLIP, CLOP!", .72, .3, .8, "sun", (.5, .33), .8)], **MILO("zoo_eve", 940)),
    S("paper_blue", BOARD, "Next time on Guess With Milo: whose ears are these? Bye-bye, friends!", part=4, tag="next: whose ears", pcam=BOARDP,
      props=[prop("qm", A.qmark, 960, 520, 1.25, p=(960, 560, 1.5))], fx=[PULSE("w:ears", "#{p}qm_w", 1.15, 2)],
      words=[("w:ears", "WHOSE EARS?", .5, .14, 1.1, "sun", (.5, .3), .9), ("w:Bye-bye,", "BYE-BYE!", .5, .74, 1.0, "pill", (.5, .7), .8)]),
]
for _s in SHOTS:        # a picture board never drifts closer: it only pulls out a little (16:9 and 9:16)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)

SHORTS = [
    {"id": "zc_ep11_short1", "title": "Who Walks on Tiptoes? Guess With Milo", "band": ("WHOSE BIG", "FOOT?"), "thumb_text": "SQUISH!", "part": 1,
     "extra_first": [S("sandtrail", PCLOSE, "A giant footprint! Guess with Milo!", part=1, q=True, tag="hook: giant print", hide=["milo"], pcam=PCLOSEP, cam2=W(PCLOSE, 1.06),
                       props=BIG("pe", A.print_elephant), fx=[PULSE("w:footprint!", "#{p}pe_w", 1.1)], words=[("w:Guess", "?", .7, .3, 2.0, "sun", (.5, .34), 1.3)])]},
    {"id": "zc_ep11_short2", "title": "Whose Feet Have Two Hooves? Guess With Milo", "band": ("TWO HALVES?", "WHO?"), "thumb_text": "HALVES?", "part": 2,
     "extra_first": [S("sandtrail", PCLOSE, "A footprint with two halves! Guess with Milo!", part=2, q=True, tag="hook: two halves", hide=["milo"], pcam=PCLOSEP, cam2=W(PCLOSE, 1.06),
                       props=BIG("pg", A.print_giraffe), fx=[PULSE("w:two", "#{p}pg_w", 1.1)], words=[("w:Guess", "?", .7, .3, 2.0, "sun", (.5, .34), 1.3)])]},
    {"id": "zc_ep11_short3", "title": "Who Walks on Just One Toe? Guess With Milo", "band": ("ONE TOE?", "WHO?"), "thumb_text": "CLIP CLOP!", "part": 3,
     "extra_first": [S("sandtrail", PCLOSE, "One smooth, round footprint! Guess with Milo!", part=3, q=True, tag="hook: one smooth print", hide=["milo"], pcam=PCLOSEP, cam2=W(PCLOSE, 1.06),
                       props=BIG("pz", A.print_zebra), fx=[PULSE("w:One", "#{p}pz_w", 1.1)], words=[("w:Guess", "?", .7, .3, 2.0, "sun", (.5, .34), 1.3)])]},
]

# thumbnails (thumb.py): one big object, 1-2 words, none of the title's words, no watermark
THUMBS = {
    "zc_ep11": {"place": "sandtrail", "cam": (960, 860, 1500), "actors": [("milo", 1480, 1080, 1.05, True, "")],
                "props": [(A.print_elephant, 720, 1050, 2.3)], "words": [("WHO?", 1400, 250, 250, "sun")]},
    "zc_ep11_short1": {"place": "sandtrail", "cam": (960, 900, 1500), "props": [(A.print_elephant, 960, 1120, 2.7)],
                       "words": [("SQUISH!", 540, 520, 200, "sun")]},
    "zc_ep11_short2": {"place": "sandtrail", "cam": (960, 900, 1500), "props": [(A.print_giraffe, 960, 1120, 3.0)],
                       "words": [("HALVES?", 540, 520, 200, "sun")]},
    "zc_ep11_short3": {"place": "sandtrail", "cam": (960, 900, 1500), "props": [(A.print_zebra, 960, 1120, 3.0)],
                       "words": [("CLIP", 540, 440, 200, ""), ("CLOP!", 540, 640, 220, "sun")]},
}
