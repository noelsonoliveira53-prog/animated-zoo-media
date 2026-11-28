"""gc_ep05: "Why Do Things Fall Down?" - Gizmo Explains cartoon explainer (catch-up run B, Nov 28 2026, session_014CFVfWNwXyYMYtjBTtMq95).
Gizmo hosts in his lab, at his bench, in the flower meadow by an apple tree, high in the sky, in space and in the park ("beat" process).
Three parts, each cut whole into one Short: 1. gravity is an invisible pull; the Earth pulls things toward its centre, so things fall down and we
stay on the ground, all around the Earth; 2. a heavy ball and a light ball dropped together land together; a feather is slowed down by the air, and
where there is no air a feather and a rock land at the same time; 3. everything that has mass has gravity, more mass more gravity, the big Earth's
pull is big, gravity keeps the Moon going around the Earth and the planets going around the Sun.

FACTS, read at the source on Nov 28 2026 (pages fetched in this session by the page reader; quotes copied from the page text, under 125 characters):
 [NASA] NASA Space Place, "What is gravity?" (spaceplace.nasa.gov/what-is-gravity):
   "The answer is gravity: an invisible force that pulls objects toward each other."
   "Gravity is the force by which a planet or other body draws objects toward its center."
   "Earth's gravity is what keeps you on the ground and what makes things fall."
   "Anything that has mass also has gravity. Objects with more mass have more gravity."
   "Gravity is what holds the planets in orbit around the sun and what keeps the moon in orbit around Earth."
 [UIUC] University of Illinois Physics Van, "Heavy and Light - Both Fall the Same" (van.physics.illinois.edu/qa/listing.php?id=164):
   "This is just the way gravity works - it accelerates everything at exactly the same rate."
   "In the absence of air friction both heavy and light objects will reach the ground at the same time."
   "the rock will land first since the feather is slowed down more by the air."
   "If you did the same thing somewhere where there is no air, the feather and the rock would land at exactly the same time."
 [APS] American Physical Society, PhysicsQuest "Falling Physics" teacher guide (aps.org/learning-resources/falling-physics):
   "objects with different masses will still hit the ground at the same time if they are dropped from the same height."
   "Air resistance: The force air exerts on something moving through it."
 [SB] Science Buddies, "Showing Science: Watch Objects in Freefall": "You should have found that both balls hit the ground at roughly the same time."
 Said as: gravity is an invisible pull that pulls things toward each other; the Earth pulls things toward its center (its middle); so things fall
 down, and Earth's gravity keeps you on the ground (people stand on the ground all around the Earth: the picture of "toward its center");
 drop a heavy ball and a light ball from the same height and they land at the same time (gravity speeds everything up the same way); a feather
 is slowed down by the air, so a ball lands first; where there is no air, a feather and a rock land at exactly the same time; anything that has
 mass has gravity ("everything made of stuff", "you too"), more mass means more gravity, so the big Earth has a big pull; gravity keeps the Moon
 going around the Earth and the planets going around the Sun.
 Taken out (not on the pages read today): crumpled paper against a flat sheet (APS names it as an activity but does not state the result),
 rain falling by gravity (read Nov 27, not today), "too small to feel". Pictures that are ours, not facts: the arrows that show the invisible pull,
 the tiny people standing on all sides of the Earth, the feather's sway.
 Safe: nothing is dropped from a height a child could copy (a ball drops from a hand to the floor on the board); the hop is "just a little".
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_gizmo as G
import art_gc_ep02 as R
import art_gc_ep03 as A3
import art_gc_ep05 as A
from kit import Kit, S, prop, W
from intro_gizmo import GZ_INTRO_STAGES, gz_intro_shots      # Gizmo's main intro (owner, Nov 21 2026 12:18 PM: "amazing emplement on every new video")
from episodes.gc_ep01 import WAVE, IDEA, ARMS, UP, DOWN, WIDEARMS, CURL, HOP, PULSE, OFF, ON

BOILER = ("Gizmo Explains makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 4-8. "
          "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.")
SRC = ("WHERE THE FACTS COME FROM\nNASA Space Place (What is gravity?), University of Illinois Physics Van (Heavy and Light - Both Fall the Same), "
       "American Physical Society PhysicsQuest (Falling Physics).")
EP = {"id": "gc_ep05", "nest": True, "beat": True, "voice": "am_michael", "speed": 0.85, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0, "wm": "brand/gizmo",      # Gizmo's OWN main intro (intro_gizmo.py): after the hook and as the last four shots
      "cast": {"gizmo": {"voice": "am_michael", "speed": 0.85}},
      "title": "Why Do Things Fall Down? Gizmo Explains", "thumb_text": "BIG PULL", "series": "Gizmo Explains",
      "description": ("Why do things fall down, and never up? Gizmo the robot watches an apple drop from a tree, races a heavy ball against a light ball, "
                      "lets a feather float down and looks out into space at the Moon. A gentle science lesson for ages 4-8 with questions to answer, things to try and a quiz at the end.\n"
                      "Kids learn that gravity is an invisible pull, that the Earth pulls things toward its center so things fall and we stay on the ground, "
                      "that a heavy ball and a light ball dropped together land together, that the air slows a feather down, that everything with mass has "
                      "gravity, and that gravity keeps the Moon going around the Earth and the planets going around the Sun.\n\n"
                      + BOILER + "\n\n" + SRC),
      "tags": ["why do things fall down", "gravity for kids", "what is gravity", "science for kids", "heavy and light", "feather and ball",
               "moon for kids", "space for kids", "Gizmo Explains", "Gizmo the robot", "preschool science", "kindergarten science"]}

GX, GY, GS = 700, 900, .7
STAGES = {"glab": [("gizmo", "gizmo", GX, GY, GS)],
          "gbench": [("gizmo", "gizmo", 520, 860, .66)],
          "gpark": [("gizmo", "gizmo", 470, 960, .6)],       # on the grass, left of the path
          "gmeadow": [("gizmo", "gizmo", 300, 900, .5)],     # never in the picture (hidden in every gmeadow shot)
          "gsky": [("gizmo", "gizmo", 300, 760, .5)],        # never in the picture (hidden in every gsky shot)
          "gspace": [("gizmo", "gizmo", 300, 760, .5)], **GZ_INTRO_STAGES}     # never in the picture (hidden in every gspace shot)
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
GP = lambda place: WV(place, ["gizmo"], floor=.72, top=.42)
GPL = lambda place: WV(place, ["gizmo"], floor=.62, top=.42)        # Gizmo smaller: room for a word under him
GCAM = lambda place, w=1000: C(place, "gizmo", "all", w)


# ------------------------------------------------------------------ moves
def FALL(at, sel, dy, d=.6, what="it falls down"): return ("fromto", at, sel, {"y": -dy}, {"y": 0, "duration": d, "ease": "power2.in"}, what)
def HELD(sel, dy): return ("fromto", 0, sel, {"y": -dy}, {"y": -dy, "duration": .01}, "")
def APPLE_DROP(at, what="the apple falls"): return ("to", at, "#{p}tr-apple", {"y": 275, "duration": .7, "ease": "power2.in"}, what)
def APPLE_DOWN(): return ("fromto", 0, "#{p}tr-apple", {"y": 275}, {"y": 275, "duration": .01}, "")
def DRIFT(at, sel, dy, d=3.4, what="the feather floats down slowly"):
    return [("fromto", at, sel, {"y": -dy}, {"y": 0, "duration": d, "ease": "sine.out"}, what),
            ("fromto", at, sel + "-f", {"x": -40, "rotation": -14}, {"x": 40, "rotation": 14, "duration": d / 4, "ease": "sine.inOut", "yoyo": True, "repeat": 3, "transformOrigin": "50% 50%"}, "")]
def SPIN(at, sel, d=9.0, what="it goes around"): return ("to", at, sel + "-spin", {"rotation": -360, "svgOrigin": "0 0", "duration": d, "ease": "none"}, what)


# ------------------------------------------------------------------ places, cameras, props
TX, TY, TS = 1250, 900, .9                                 # the apple tree in the meadow
TREE = (1250, 560, 1500); TREEP = (1300, 640, 1300)
APC = (1380, 720, 1000); APP = (1380, 740, 1000)           # close on the falling apple
def tree(): return prop("tr", A.apple_tree, TX, TY, TS, p=(TX, TY, TS))

BOARD = (960, 540, 1500); PBOARD = (960, 470, 1700)
FY, PFY = 760, 760                                          # the floor on the board (16:9 / 9:16)
def flr(): return prop("fl", A.floor, 960, FY, 1.0, p=(960, PFY, .9))
DROP = 220                                                  # how far a ball falls on the board
def hball(x=760): return prop("hb", A.heavy_ball, x, FY, 1.0, p=(x + 20, PFY, .9))
def lball(x=1160): return prop("lb", A.light_ball, x, FY, 1.0, p=(x - 20, PFY, .9))
def fea(x=1160): return prop("fe", A.feather, x, FY, 1.3, p=(x - 20, PFY, 1.1))
def rck(x=760): return prop("rk", A.rock, x, FY, 1.0, p=(x + 20, PFY, .9))
def arrow(): return prop("da", A.down_arrow, 960, 560, .8, p=(960, 560, .7))
def b_apple(): return prop("ba", A.apple, 960, 560, 1.6, p=(960, 560, 1.4))
def b_earth(): return prop("ea", A.earth, 960, 640, .72, p=(960, 600, .66))
def b_pulls(): return prop("pu", A.pulls, 960, 620, .82, p=(960, 600, .62))

SPACE = (960, 540, 1920); SPACEC = (960, 520, 1500); SPACEP = (960, 560, 1500)
def om(): return prop("om", A.orbit_moon, 960, 500, .75, p=(960, 600, .68))
def osun(): return prop("os", A.orbit_sun, 960, 500, .72, p=(960, 600, .64))

SKYC = (960, 520, 1300); SKYP = (960, 560, 1500)
def skyfea(): return prop("sf", A.feather, 960, 820, 1.8, p=(960, 820, 1.6))

BEN = (960, 540, 1800); BENP = (900, 560, 1500)
PARK = (960, 560, 1920); PARKP = (900, 600, 1700); PARKG = GCAM("gpark", 1150)
PBX = 1150
def pball(): return prop("pb", A.ball, PBX, 890, 1.0, p=(PBX - 100, 890, 1.0))


SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("gmeadow", TREE, "Why do things fall down? Why not up?", q=True, tag="hook: the apple falls", pcam=TREEP, hide=["gizmo"], props=[tree()], cam2=W(TREE, .96),
      fx=[APPLE_DROP("w:fall")], words=[("w:up?", "?", .2, .3, 2.0, "sun", (.3, .4), 1.3)]),
    S("paper_gz", BOARD, "Drop a ball, and down it goes. Every time!", tag="hook: the ball drops", pcam=PBOARD, cam2=(960, 555, 1390), props=[flr(), prop("rb", A.ball, 960, FY, 1.0, p=(960, PFY, .9))],
      fx=[FALL("w:Drop", "#{p}rb", DROP + 60, .6, "the ball falls")],
      words=[("w:Every", "EVERY TIME!", .5, .14, .95, "sun", (.5, .36), .8)]),
    S("glab", (GX, 640, 1000), "Hi! I'm Gizmo. Let's find out why things fall down!", tag="hook: Gizmo", pcam=GP("glab"), fx=[WAVE("w:Hi!"), HOP("w:find")],
      words=[("w:Gizmo.", "GIZMO", .78, .3, 1.1, "pill", (.5, .36), .9)]),
    # ---------------------------------------------------------------- MAIN INTRO (right after the hook; again as the last four shots)
    *gz_intro_shots(),
    S("glab", WIDE, "Welcome to my lab, science fans!", trans="iris", tag="lab wide", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=[WAVE("w:Welcome", 4)],
      words=[("w:lab,", "HELLO!", .74, .5, 1.2, "pill", (.5, .36), 1.0)]),
    S("gbench", BEN, "Today, we learn about a pull that you can not see!", tag="bench wide", pcam=BENP, props=[prop("mg", G.magnifier, 1250, 600, 1.0, p=(1180, 600, .8))],
      fx=[PULSE("w:pull", "#{p}mg", 3, 1.08)], words=[("w:see!", "A SECRET PULL!", .5, .14, .85, "sun", (.5, .36), .7)]),
    # ---------------------------------------------------------------- PART 1: gravity pulls things toward the Earth
    S("gmeadow", TREE, "Look at this apple tree in the meadow.", part=1, tag="the apple tree", pcam=TREEP, hide=["gizmo"], props=[tree()], cam2=W(TREE, .95),
      fx=[PULSE("w:apple", "#{p}tr-apple", 3, 1.1)], words=[("w:tree", "AN APPLE TREE!", .3, .3, .9, "sun", (.5, .36), .75)]),
    S("gmeadow", APC, "One apple lets go of its branch. Down it falls, onto the grass!", part=1, tag="the apple falls", pcam=APP, hide=["gizmo"], props=[tree()],
      fx=[APPLE_DROP("w:Down")], words=[("w:grass!", "PLOP!", .25, .3, 1.1, "sun", (.3, .4), .9)]),
    S("paper_gz", BOARD, "Which way does the apple fall? Up, or down?", part=1, q=True, tag="question 1", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_apple()],
      fx=[PULSE(0.3, "#{p}ba", 2, 1.06), ("signs", "w:Up,", ["UP", "DOWN"], 1, "wait:2.0")]),
    S("paper_gz", BOARD, "Down! Things always fall down, toward the ground.", part=1, tag="down", pcam=PBOARD, props=[flr(), arrow(), prop("ba", A.apple, 1240, FY, 1.4, p=(1200, PFY, 1.2))],
      fx=[ON("w:Down!", "#{p}da-a", "a big arrow points down"), FALL("w:fall", "#{p}ba", DROP, .6, "the apple falls")], words=[("w:Down!", "DOWN!", .24, .3, 1.1, "sun", (.3, .38), .9)]),
    S("gpark", PARKG, "But why? What pulls them down? Let's think!", part=1, q=True, tag="think", pause=.6, pcam=GPL("gpark"),
      fx=[("face", "w:why?", "gizmo", "wow")] + IDEA("w:think!"), words=[("w:down?", "WHY?", .8, .3, 1.0, "sun", (.5, .67), .9)]),
    S("paper_gz", BOARD, "It is a force called gravity!", part=1, tag="gravity", pcam=PBOARD, props=[b_earth()],
      fx=[PULSE("w:gravity!", "#{p}ea", 3, 1.05)], words=[("w:gravity!", "GRAVITY!", .5, .14, 1.0, "sun", (.5, .38), .85)]),
    S("paper_gz", BOARD, "Gravity is an invisible pull. It pulls things toward each other.", part=1, tag="invisible pull", pcam=PBOARD, props=[b_pulls()],
      fx=[ON("w:pulls", "#{p}pu-b", "arrows show the pull")], words=[("w:pull.", "A PULL!", .24, .3, 1.0, "sun", (.3, .38), .85)]),
    S("paper_gz", BOARD, "Can we see gravity? Yes, or no?", part=1, q=True, tag="question 2", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_earth()],
      fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("paper_gz", BOARD, "Gravity is invisible! We drew arrows, so you can see the pull.", part=1, tag="arrows", pcam=PBOARD, props=[b_earth()],
      fx=[ON("w:arrows,", "#{p}ea-arr", "arrows show the pull"), PULSE("w:pull.", "#{p}ea-arr", 2, 1.04)], words=[("w:invisible!", "INVISIBLE!", .3, .3, 1.0, "sun", (.5, .38), .85)]),
    S("paper_gz", BOARD, "The Earth pulls everything toward its middle, its center.", part=1, tag="toward the center", pcam=PBOARD, props=[b_earth()],
      fx=[ON(0, "#{p}ea-arr"), ON("w:middle,", "#{p}ea-dot", "the center lights up"), PULSE("w:center.", "#{p}ea-dot", 3, 1.3)], words=[("w:center.", "THE CENTER!", .76, .3, .9, "sun", (.72, .38), .75)]),
    S("paper_gz", BOARD, "So people all around the Earth stand on the ground!", part=1, tag="people all around", pcam=PBOARD, props=[b_earth()],
      fx=[ON("w:people", "#{p}ea-ppl", "little people stand all around the Earth"), ("to", "w:around", "#{p}ea", {"rotation": 40, "transformOrigin": "50% 50%", "duration": 3.0, "ease": "sine.inOut"}, "the Earth turns")],
      words=[("w:around", "ALL AROUND!", .24, .3, .9, "sun", (.3, .38), .75)]),
    S("gmeadow", APC, "Gravity pulled the apple down, toward the Earth's center.", part=1, tag="pulled the apple", pcam=APP, hide=["gizmo"], props=[tree(), prop("pa", A.down_arrow, 1385, 640, .6, p=(1385, 640, .6))],
      fx=[APPLE_DROP("w:pulled"), ON("w:down,", "#{p}pa-a", "an arrow points down")], words=[("w:pulled", "PULL!", .25, .3, 1.1, "sun", (.3, .4), .9)]),
    S("gmeadow", APC, "Plop! There it is, down on the grass.", part=1, tag="on the grass", pcam=APP, hide=["gizmo"], props=[tree()],
      fx=[APPLE_DOWN(), PULSE("w:Plop!", "#{p}tr-apple", 2, 1.12)], words=[("w:grass.", "ON THE GRASS!", .3, .3, .85, "sun", (.36, .4), .7)]),
    S("paper_gz", BOARD, "Which way does gravity pull? Toward the Earth's center, or up to the sky?", part=1, q=True, tag="question 2b", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_earth()],
      fx=[ON(0, "#{p}ea-dot"), PULSE(0.3, "#{p}ea-dot", 3, 1.3), ("signs", "w:center,", ["THE CENTER", "THE SKY"], 0, "wait:2.0")]),
    S("glab", GCAM("glab"), "Hop up, just a little! Gravity brings you back down.", part=1, q=True, tag="hop", pause=1.2, pcam=GPL("glab"), fx=[HOP("w:Hop", 2)],
      words=[("w:Hop", "HOP!", .8, .3, .7, "sun", (.5, .67), .9)]),
    S("glab", GCAM("glab"), "Point down to the ground, where gravity pulls!", part=1, q=True, tag="point down", pause=1.2, pcam=GPL("glab"), fx=DOWN("w:Point", 2.0),
      words=[("w:Point", "POINT DOWN!", .8, .3, .7, "sun", (.5, .67), .8)]),
    S("gbench", (900, 560, 1500), "Say it with me. Gravity pulls things down!", part=1, q=True, tag="say it", pcam=GPL("gbench"), fx=[HOP("w:down!")],
      words=[("w:Gravity", "GRAVITY PULLS!", .55, .2, .8, "sun", (.5, .36), .6)]),
    S("paper_gz", BOARD, "What keeps you on the ground? Gravity, or glue?", part=1, q=True, tag="question 3", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_earth()],
      fx=[ON(0, "#{p}ea-ppl"), ("signs", "w:Gravity,", ["GRAVITY", "GLUE"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Gravity! It keeps you on the ground, and makes things fall.", part=1, tag="part 1 recap", pcam=PBOARD, props=[flr(), prop("ba", A.apple, 960, FY, 1.4, p=(960, PFY, 1.2))],
      fx=[FALL("w:fall.", "#{p}ba", DROP, .6, "the apple falls")], words=[("w:Gravity!", "GRAVITY!", .5, .14, 1.0, "sun", (.5, .38), .85)]),
    # ---------------------------------------------------------------- PART 2: heavy and light, the feather and the air
    S("paper_gz", BOARD, "Here is a heavy ball, and a light ball.", part=2, trans="iris", tag="two balls", pcam=PBOARD, props=[flr(), hball(), lball()],
      fx=[HELD("#{p}hb", DROP), HELD("#{p}lb", DROP), PULSE("w:heavy", "#{p}hb", 2, 1.06), PULSE("w:light", "#{p}lb", 2, 1.06)],
      words=[("w:heavy", "HEAVY", .3, .3, .9, "sun", (.3, .38), .75), ("w:light", "LIGHT", .7, .3, .9, "sun", (.7, .38), .75)]),
    S("paper_gz", BOARD, "We drop them together. Which lands first? The heavy one, or do they land together?", part=2, q=True, tag="question 4", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[flr(), hball(), lball()], fx=[HELD("#{p}hb", DROP), HELD("#{p}lb", DROP), ("signs", "w:heavy", ["HEAVY", "TOGETHER"], 1, "wait:2.0")]),
    S("paper_gz", BOARD, "Together! Dropped from the same height, they land at the same time.", part=2, tag="together", pcam=PBOARD, props=[flr(), hball(), lball()],
      fx=[FALL("w:same", "#{p}hb", DROP, .6, "both balls fall"), FALL("w:same", "#{p}lb", DROP, .6, "")], words=[("w:Together!", "TOGETHER!", .5, .14, 1.0, "sun", (.5, .36), .85)]),
    S("glab", GCAM("glab"), "Wow! Gravity speeds up heavy things and light things the same way.", part=2, tag="the same way", pcam=GPL("glab"), fx=[("face", "w:Wow!", "gizmo", "wow")] + IDEA("w:same"),
      words=[("w:same", "THE SAME!", .8, .3, .7, "sun", (.5, .67), .85)]),
    S("paper_gz", BOARD, "Let's try it again. Ready? Drop!", part=2, q=True, tag="again", pcam=PBOARD, props=[flr(), hball(), lball()],
      fx=[FALL("w:Drop!", "#{p}hb", DROP, .6, "both balls fall"), FALL("w:Drop!", "#{p}lb", DROP, .6, "")], words=[("w:Drop!", "DROP!", .5, .14, 1.1, "sun", (.5, .36), .9)]),
    S("gsky", SKYC, "But look at this feather. It floats down, slowly.", part=2, tag="the feather floats", pcam=SKYP, hide=["gizmo"], props=[skyfea()], cam2=W(SKYC, .95),
      fx=DRIFT(0.1, "#{p}sf", 420, 4.4), words=[("w:slowly.", "SLOWLY...", .76, .3, 1.0, "sun", (.72, .4), .85)]),
    S("paper_gz", BOARD, "A ball and a feather. Which lands first?", part=2, q=True, tag="question 5", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[flr(), hball(), fea()],
      fx=[HELD("#{p}hb", DROP), HELD("#{p}fe", DROP), ("signs", "w:first?", ["BALL", "FEATHER"], 0, "wait:2.0")]),
    S("glab", GCAM("glab"), "Hmm, why is the feather so slow? Let's think!", part=2, q=True, tag="think 2", pause=.6, pcam=GPL("glab"), fx=[("face", "w:why", "gizmo", "wow")] + IDEA("w:think!"),
      words=[("w:slow?", "WHY?", .8, .3, .7, "sun", (.5, .67), .9)]),
    S("paper_gz", BOARD, "The ball! The air slows the feather down.", part=2, tag="the air slows it", pcam=PBOARD, props=[flr(), hball(), fea(), prop("ai", G.puff, 1160, 700, .6, p=(1140, 640, .5))],
      fx=[FALL("w:ball!", "#{p}hb", DROP, .6, "the ball falls fast")] + DRIFT("w:ball!", "#{p}fe", DROP, 3.6) + [PULSE("w:air", "#{p}ai", 3, 1.1)],
      words=[("w:air", "AIR!", .76, .3, 1.1, "sun", (.72, .38), .9)]),
    S("gsky", SKYC, "The air pushes on the feather, so it drifts down, side to side.", part=2, tag="the air pushes", pcam=SKYP, hide=["gizmo"], props=[skyfea(), prop("sp", G.puff, 960, 900, 1.2, p=(960, 900, 1.0))],
      fx=DRIFT(0.1, "#{p}sf", 380, 4.6), words=[("w:side", "SIDE TO SIDE!", .5, .14, .85, "sun", (.5, .36), .7)]),
    S("paper_gz", BOARD, "What slows the feather down? The air, or the ground?", part=2, q=True, tag="question 5b", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[flr(), fea(), prop("ai", G.puff, 1160, 700, .6, p=(1140, 640, .5))], fx=[HELD("#{p}fe", DROP), PULSE(0.3, "#{p}ai", 4, 1.08), ("signs", "w:air,", ["THE AIR", "GROUND"], 0, "wait:2.0")]),
    S("glab", GCAM("glab"), "Float your hands down slowly, like a feather!", part=2, q=True, tag="feather hands", pause=1.4, pcam=GPL("glab"), fx=DOWN("w:Float", 2.4),
      words=[("w:feather!", "SLOWLY!", .8, .3, .7, "sun", (.5, .67), .85)]),
    S("paper_gz", BOARD, "Now, think of a place with no air at all.", part=2, tag="no air", pcam=PBOARD, props=[flr(), rck(), fea()],
      fx=[HELD("#{p}rk", DROP), HELD("#{p}fe", DROP)], words=[("w:no", "NO AIR!", .5, .14, 1.1, "sun", (.5, .36), .9)]),
    S("paper_gz", BOARD, "With no air, we drop a rock and a feather. Which lands first?", part=2, q=True, tag="question 6", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[flr(), rck(), fea()],
      fx=[HELD("#{p}rk", DROP), HELD("#{p}fe", DROP), ("signs", "w:first?", ["THE ROCK", "SAME TIME"], 1, "wait:2.0")]),
    S("paper_gz", BOARD, "They land at exactly the same time! No air slows the feather.", part=2, tag="same time", pcam=PBOARD, props=[flr(), rck(), fea()],
      fx=[FALL("w:land", "#{p}rk", DROP, .6, "the rock and the feather fall together"), FALL("w:land", "#{p}fe", DROP, .6, "")], words=[("w:same", "SAME TIME!", .5, .14, 1.0, "sun", (.5, .36), .85)]),
    S("gbench", (900, 560, 1500), "Say it with me. The air slows the feather!", part=2, q=True, tag="say it 2", pcam=GPL("gbench"), fx=[HOP("w:feather!")],
      words=[("w:air", "AIR SLOWS IT!", .55, .2, .8, "sun", (.5, .36), .6)]),
    S("paper_gz", BOARD, "Heavy and light fall together. Only the air slows a feather down.", part=2, tag="part 2 recap", pcam=PBOARD, props=[flr(), hball(), lball()],
      fx=[FALL("w:together.", "#{p}hb", DROP, .6, "both balls fall"), FALL("w:together.", "#{p}lb", DROP, .6, "")], words=[("w:together.", "TOGETHER!", .5, .14, 1.0, "sun", (.5, .36), .85)]),
    # ---------------------------------------------------------------- PART 3: everything has gravity; the Moon and the Sun
    S("glab", WIDE, "Here is a big surprise. Everything that is made of stuff has gravity!", part=3, trans="iris", tag="everything has gravity", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=IDEA("w:surprise."),
      words=[("w:Everything", "EVERYTHING!", .74, .5, 1.1, "sun", (.5, .72), .8)]),
    S("paper_gz", BOARD, "A little ball has a little bit of gravity, just a tiny pull.", part=3, tag="a little pull", pcam=PBOARD, props=[b_pulls()],
      fx=[ON("w:little", "#{p}pu-a", "two tiny arrows by the little ball"), PULSE("w:bit", "#{p}pu-a", 3, 1.1)], words=[("w:little", "A LITTLE", .24, .3, .9, "sun", (.3, .38), .75)]),
    S("paper_gz", BOARD, "Does a little ball have gravity? Yes, or no?", part=3, q=True, tag="question 6b", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_pulls()],
      fx=[ON(0, "#{p}pu-a"), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Things with more stuff, more mass, have more gravity.", part=3, tag="more mass", pcam=PBOARD, props=[b_pulls()],
      fx=[ON(0, "#{p}pu-a"), ON("w:more", "#{p}pu-b", "big arrows by the big Earth"), PULSE("w:gravity.", "#{p}pu-e", 2, 1.05)], words=[("w:mass,", "MORE!", .76, .3, 1.1, "sun", (.72, .38), .9)]),
    S("glab", GCAM("glab"), "You have gravity too, and so do I!", part=3, tag="you too", pcam=GPL("glab"), fx=[HOP("w:too,"), ("face", "w:I!", "gizmo", "wow")],
      words=[("w:too,", "YOU TOO!", .8, .3, .7, "sun", (.5, .67), .85)]),
    S("paper_gz", BOARD, "Which has more gravity? A ball, or the big Earth?", part=3, q=True, tag="question 7", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_pulls()],
      fx=[("signs", "w:ball,", ["A BALL", "THE EARTH"], 1, "wait:2.0")]),
    S("paper_gz", BOARD, "The Earth! It is so big, its pull holds all of us down.", part=3, tag="the earth", pcam=PBOARD, props=[b_earth()],
      fx=[ON("w:pull", "#{p}ea-arr", "arrows show the pull"), ON("w:us", "#{p}ea-ppl", "people stand all around")], words=[("w:Earth!", "THE EARTH!", .5, .14, 1.0, "sun", (.5, .36), .85)]),
    S("glab", GCAM("glab"), "Make a big round Earth with your arms!", part=3, q=True, tag="earth arms", pause=1.2, pcam=GPL("glab"), fx=WIDEARMS("w:round", 2.2),
      words=[("w:Earth", "BIG EARTH!", .8, .3, .7, "sun", (.5, .67), .85)]),
    S("gspace", SPACE, "Now look up, into space. There is the Moon, way up high!", part=3, tag="the moon", pcam=SPACEP, hide=["gizmo"], props=[om()], cam2=W(SPACE, .94),
      fx=[PULSE("w:Moon,", "#{p}om-spin", 1, 1.0), SPIN(0.1, "#{p}om", 30.0)], words=[("w:Moon,", "THE MOON!", .76, .3, 1.0, "sun", (.72, .36), .85)]),
    S("gspace", SPACEC, "The Moon goes around, and around, the Earth.", part=3, tag="around the earth", pcam=SPACEP, hide=["gizmo"], props=[om()],
      fx=[SPIN(0.1, "#{p}om", 6.0)], words=[("w:around,", "AROUND!", .24, .3, 1.0, "sun", (.5, .36), .8)]),
    S("glab", GCAM("glab"), "Point up to the Moon in the sky!", part=3, q=True, tag="point up", pause=1.2, pcam=GPL("glab"), fx=UP("w:Point", 2.0),
      words=[("w:Point", "POINT UP!", .8, .3, .7, "sun", (.5, .67), .8)]),
    S("gspace", SPACEC, "Earth's gravity keeps the Moon going around the Earth.", part=3, tag="gravity keeps the moon", pcam=SPACEP, hide=["gizmo"], props=[om()],
      fx=[SPIN(0.1, "#{p}om", 8.0), ON("w:gravity", "#{p}om-pull", "an arrow pulls the Moon toward the Earth")], words=[("w:gravity", "GRAVITY!", .5, .12, 1.0, "sun", (.5, .36), .85)]),
    S("gspace", SPACEC, "What goes around the Earth? The Moon, or a cloud?", part=3, q=True, tag="question 8", pause=3.2, pcam=SPACEP, hide=["gizmo"], props=[om()], cam2=(960, 530, 1400),
      fx=[SPIN(0.1, "#{p}om", 12.0), ("signs", "w:Moon,", ["THE MOON", "A CLOUD"], 0, "wait:2.0")]),
    S("gspace", SPACEC, "And the Sun's gravity keeps the Earth, and all the planets, going around the Sun!", part=3, tag="around the sun", pcam=SPACEP, hide=["gizmo"], props=[osun()], cam2=W(SPACEC, .94),
      fx=[SPIN(0.1, "#{p}os", 9.0)], words=[("w:Sun!", "THE SUN!", .76, .3, 1.0, "sun", (.55, .36), .8)]),
    S("glab", GCAM("glab"), "Turn around slowly, like the Moon going around!", part=3, q=True, tag="turn", pause=1.2, pcam=GPL("glab"),
      fx=[("to", "w:Turn", "#{p}gizmo-body", {"scaleX": -1, "svgOrigin": "0 0", "duration": .6, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "Gizmo turns around")],
      words=[("w:Turn", "TURN!", .8, .3, .7, "sun", (.5, .67), .9)]),
    S("gbench", (900, 560, 1500), "Say it with me. Everything has gravity!", part=3, q=True, tag="say it 3", pcam=GPL("gbench"), fx=[HOP("w:gravity!")],
      words=[("w:Everything", "EVERYTHING!", .55, .2, .8, "sun", (.5, .36), .7)]),
    S("gpark", PARK, "So when a ball falls down in the park, now you know why!", part=3, tag="ball in the park", pcam=PARKP, cam2=W(PARK, 1.0), props=[pball()],
      fx=[FALL("w:falls", "#{p}pb", 360, .6, "the ball falls")], words=[("w:why!", "NOW YOU KNOW!", .7, .3, .85, "sun", (.5, .36), .7)]),
    S("paper_gz", BOARD, "It is gravity, pulling it toward the Earth!", part=3, tag="part 3 recap", pcam=PBOARD, props=[b_earth()],
      fx=[ON("w:pulling", "#{p}ea-arr", "arrows show the pull"), ON("w:Earth!", "#{p}ea-dot", "the center lights up")], words=[("w:gravity,", "GRAVITY!", .5, .14, 1.0, "sun", (.5, .36), .85)]),
    # ---------------------------------------------------------------- QUIZ + GOODBYE
    S("glab", WIDE, "Quiz time! Let's remember what we learned.", part=4, trans="iris", tag="quiz time", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=IDEA("w:Quiz"),
      words=[("w:Quiz", "QUIZ TIME!", .74, .5, 1.3, "sun", (.5, .36), 1.0)]),
    S("gmeadow", TREE, "Which way does an apple fall from a tree? Up, or down?", part=4, q=True, tag="quiz 1", pause=3.2, pcam=TREEP, hide=["gizmo"], props=[tree()], cam2=(1250, 580, 1400),
      fx=[("signs", "w:Up,", ["UP", "DOWN"], 1, "wait:2.0")]),
    S("gmeadow", APC, "Down! Gravity pulls it toward the ground.", part=4, tag="quiz 1 answer", pcam=APP, hide=["gizmo"], props=[tree()],
      fx=[APPLE_DROP("w:pulls")], words=[("w:Down!", "DOWN!", .25, .3, 1.1, "sun", (.3, .4), .9)]),
    S("paper_gz", BOARD, "Drop a heavy ball and a light ball. Which lands first? Heavy, or together?", part=4, q=True, tag="quiz 2", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), trans="iris",
      props=[flr(), hball(), lball()], fx=[HELD("#{p}hb", DROP), HELD("#{p}lb", DROP), ("signs", "w:Heavy,", ["HEAVY", "TOGETHER"], 1, "wait:2.0")]),
    S("paper_gz", BOARD, "Together! They land at the same time.", part=4, tag="quiz 2 answer", pcam=PBOARD, props=[flr(), hball(), lball()],
      fx=[FALL("w:land", "#{p}hb", DROP, .6, "both balls fall"), FALL("w:land", "#{p}lb", DROP, .6, "")], words=[("w:Together!", "TOGETHER!", .5, .14, 1.0, "sun", (.5, .36), .85)]),
    S("gspace", SPACEC, "What keeps the Moon going around the Earth? Gravity, or a rope?", part=4, q=True, tag="quiz 3", pause=3.2, pcam=SPACEP, hide=["gizmo"], props=[om()], trans="iris", cam2=(960, 530, 1400),
      fx=[SPIN(0.1, "#{p}om", 12.0), ("signs", "w:Gravity,", ["GRAVITY", "A ROPE"], 0, "wait:2.0")]),
    S("gspace", SPACEC, "Gravity! Round and round goes the Moon.", part=4, tag="quiz 3 answer", pcam=SPACEP, hide=["gizmo"], props=[om()],
      fx=[SPIN(0.1, "#{p}om", 5.0), ON("w:Gravity!", "#{p}om-pull", "an arrow pulls the Moon")], words=[("w:Round", "ROUND!", .24, .3, 1.0, "sun", (.4, .36), .85)]),
    S("gpark", PARKG, "Apples, balls, and the Moon. That is gravity! Thanks for exploring with me!", part=4, tag="goodbye", pcam=GP("gpark"),
      fx=[WAVE("w:Thanks", 5), HOP("w:exploring")], words=[("w:Thanks", "BYE-BYE!", .8, .3, 1.1, "pill", (.5, .36), .9)]),
    *gz_intro_shots(),      # the main intro again, as the last four shots
]
for _s in SHOTS:
    _s["who"] = "gizmo"        # Gizmo speaks every line, so his mouth moves
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)     # a picture board never drifts closer (zc_ep08)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)
    for _f in _s["fx"]:        # 9:16: a word never sits on the title band's second line
        if _f[0] == "word" and len(_f) > 3 and "p" in _f[3] and _s["pcam"]: _f[3]["p"]["y"] = max(_f[3]["p"]["y"], round(_s["pcam"][1] - .15 * _s["pcam"][2]))

SHORTS = [
    {"id": "gc_ep05_short1", "title": "Why Does an Apple Fall Down? Gizmo Explains", "band": ("WHY DOES IT", "FALL DOWN?"), "thumb_text": "WHOOSH!", "part": 1,
     "extra_first": [S("gmeadow", TREE, "Why does an apple fall down, and never up?", part=1, q=True, tag="hook: why does it fall", pcam=TREEP, hide=["gizmo"], who="gizmo",
                       props=[tree()], fx=[APPLE_DROP("w:down,")], pcam2=W(TREEP, .94), words=[("w:up?", "?", .2, .3, 2.0, "sun", (.3, .4), 1.3)])]},
    {"id": "gc_ep05_short2", "title": "Which Lands First? Gizmo Explains", "band": ("WHICH LANDS", "FIRST?"), "thumb_text": "RACE!", "part": 2,
     "extra_first": [S("paper_gz", BOARD, "A heavy ball and a light ball. Which one lands first?", part=2, q=True, tag="hook: which lands first", pcam=PBOARD, who="gizmo", pcam2=W(PBOARD, .94),
                       cam2=W(BOARD, 1.04), props=[flr(), hball(), lball()], fx=[HELD("#{p}hb", DROP), HELD("#{p}lb", DROP), PULSE("w:heavy", "#{p}hb", 2, 1.06), PULSE("w:light", "#{p}lb", 2, 1.06)],
                       words=[("w:first?", "?", .5, .3, 2.0, "sun", (.5, .4), 1.3)])]},
    {"id": "gc_ep05_short3", "title": "What Keeps the Moon Going Around? Gizmo Explains", "band": ("WHAT KEEPS", "THE MOON?"), "thumb_text": "SPACE PULL", "part": 3,
     "extra_first": [S("gspace", SPACEC, "What keeps the Moon going around and around the Earth?", part=3, q=True, tag="hook: what keeps the moon", pcam=SPACEP, hide=["gizmo"], who="gizmo", pcam2=W(SPACEP, .94),
                       props=[om()], fx=[SPIN(0.1, "#{p}om", 8.0)], words=[("w:Earth?", "?", .82, .3, 2.0, "sun", (.75, .4), 1.3)])]},
]
for _sp in SHORTS:
    for _s in _sp["extra_first"]:
        for _f in _s["fx"]:
            if _f[0] == "word" and len(_f) > 3 and "p" in _f[3] and _s["pcam"]: _f[3]["p"]["y"] = max(_f[3]["p"]["y"], round(_s["pcam"][1] - .15 * _s["pcam"][2]))


def _lit(fn, *parts):      # a prop drawn with some of its parts shown (for a thumbnail: no timeline there)
    def f(p):
        s = fn(p)
        for x in parts: s = s.replace(f'id="{p}-{x}" opacity="0"', f'id="{p}-{x}" opacity="1"')
        return s
    return f


# thumbnails (thumb.py): the example in the picture, 1-2 words, none of the title's words, no watermark
THUMBS = {
    "gc_ep05": {"place": "paper_gz", "cam": (960, 600, 1300), "actors": [],
                "props": [(_lit(A.earth, "arr", "ppl"), 960, 640, .85)],
                "words": [("BIG", 400, 330, 210, ""), ("PULL", 1520, 330, 210, "sun")]},
    "gc_ep05_short1": {"place": "gmeadow", "cam": (1300, 600, 1300), "actors": [],
                       "props": [(A.apple_tree, TX, TY, TS)],
                       "words": [("WHOOSH!", 540, 1560, 200, "sun")]},
    "gc_ep05_short2": {"place": "paper_gz", "cam": (960, 640, 1300), "actors": [],
                       "props": [(A.floor, 960, 900, 1.0), (A.heavy_ball, 760, 700, 1.3), (A.light_ball, 1160, 700, 1.3)],
                       "words": [("RACE!", 540, 330, 240, "sun")]},
    "gc_ep05_short3": {"place": "gspace", "cam": (960, 520, 1400), "actors": [],
                       "props": [(_lit(A.orbit_moon, "pull"), 960, 520, .9)],
                       "words": [("SPACE", 540, 1500, 200, ""), ("PULL", 540, 1720, 200, "sun")]},
}
