"""gc_ep02: "How Do Rockets Fly?" - Gizmo Explains cartoon explainer (daily run Nov 21 2026, session_014CFVfX9xTrYXRL7oziQw2A).
Gizmo hosts in his lab, at his bench, at the window, at a launch field far away, high in the sky and in space ("beat" music-and-sync process).
Three parts, each cut whole into one Short: 1. what pushes a rocket up (fuel -> hot gas -> pushed out the back -> the gas pushes the rocket the other way),
2. a rocket works in space where there is no air (a jet needs air from outside; a rocket carries everything it needs), 3. stages: a heavy rocket needs a
big push, empty parts drop away and the rocket goes much higher, to space and even the Moon; rockets launch satellites and take astronauts to space.

FACTS, read at the source on Nov 21 2026 (pages fetched in this session; quotes copied from the page text):
 [K4] NASA, "What Is a Rocket? (Grades K-4)" (nasa.gov/learning-resources/for-kids-and-students/what-is-a-rocket-grades-k-4/):
   "Most rocket engines turn the fuel into hot gas."   "The engine pushes the gas out its back."   "The gas makes the rocket move forward."
   "His third law says that for every action, there is an equal and opposite reaction."   "A rocket engine doesn't need air."
   "It carries with it everything it needs."   "A rocket engine works in space, where there is no air."
   "NASA uses rockets to launch satellites."   "These rockets will take astronauts into space."
 [58] NASA, "What Is a Rocket? (Grades 5-8)" (nasa.gov/learning-resources/for-kids-and-students/what-is-a-rocket-grades-5-8/):
   "A jet engine requires oxygen from the air to work."   "A rocket engine carries everything it needs."
 [GRC] NASA Glenn Research Center, "Practical Rocketry" (grc.nasa.gov/www/K-12/rocket/TRCRocket/practical_rocketry.html):
   "When the large rocket was exhausted, the rocket casing was dropped behind and the remaining rocket fired."   "Much higher altitudes were achieved by this method."
   "Today this technique of building a rocket is called staging."   "Thanks to staging, it has become possible not only to reach outer space but the Moon and other planets too."
   "In general, the heavier the rocket, the more the thrust needed to get it off the ground."
 Said as: a rocket engine turns its fuel into hot gas; it pushes the gas out of its back; the gas pushes the rocket the other way (gas down, rocket up);
 every push has a push back (the third law, said simply, no name); a jet needs air from outside to work; a rocket engine does not need air, it carries
 everything it needs, so it works in space where there is no air; a heavy rocket needs a big push to get off the ground; big rockets are built in parts
 (stages); an empty part drops away and the next part starts its engine; the rocket is lighter and goes much higher; this is called staging; it helps rockets
 reach space and even the Moon; rockets launch satellites; some rockets take astronauts into space.
 Taken out (not on the pages read today): "a rocket carries its own oxygen" (the Nov 19 3D script said it; the K-4 page read today says "everything it
 needs", not oxygen), the name Newton, the balloon example, "fuel and oxidizer".
 Pictures that are ours, not facts: "like packing a backpack for a trip". The exhaust is drawn as puffy hot gas, never as fire; nothing a child could copy.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_gizmo as G
import art_gc_ep02 as A
from kit import Kit, S, prop, W
from intro_gizmo import GZ_INTRO_STAGES, gz_intro_shots      # Gizmo's main intro (owner, Nov 21 2026 12:18 PM: "amazing emplement on every new video")
from episodes.gc_ep01 import WAVE, IDEA, ARMS, UP, DOWN, WIDEARMS, CURL, HOP, PULSE, OFF, ON

BOILER = ("Gizmo Explains makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 4-8. "
          "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.")
SRC = "WHERE THE FACTS COME FROM\nNASA, What Is a Rocket? (Grades K-4 and Grades 5-8); NASA Glenn Research Center, Practical Rocketry."
EP = {"id": "gc_ep02", "nest": True, "beat": True, "voice": "am_michael", "speed": 0.85, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0, "wm": "brand/gizmo",      # Gizmo's OWN main intro since Nov 21 2026 (intro_gizmo.py): after the hook and as the last four shots
      "cast": {"gizmo": {"voice": "am_michael", "speed": 0.85}},
      "title": "How Do Rockets Fly? Gizmo Explains", "thumb_text": "BLAST OFF!", "series": "Gizmo Explains",
      "description": ("How do rockets fly with no wings? Gizmo the robot opens up his model rocket, watches a launch, flies up through the clouds and out into space "
                      "to find out. A gentle science lesson for ages 4-8 with questions to answer, things to try and a quiz at the end.\n"
                      "Kids learn that a rocket engine turns its fuel into hot gas and pushes it out the back, that the gas pushes the rocket the other way "
                      "(gas down, rocket up), that a rocket engine does not need air because it carries everything it needs, so it works in space, "
                      "and that big rockets drop their empty parts (stages) to go much higher, all the way to space and even the Moon.\n\n" + BOILER + "\n\n" + SRC),
      "tags": ["how do rockets fly", "rockets for kids", "how rockets work", "rocket science for kids", "space for kids", "science for kids",
               "rocket stages", "Gizmo Explains", "Gizmo the robot", "preschool science", "kindergarten science", "STEM for kids"]}

GX, GY, GS = 700, 900, .7
STAGES = {"glab": [("gizmo", "gizmo", GX, GY, GS)],
          "gbench": [("gizmo", "gizmo", 520, 860, .66)],
          "gwindow": [("gizmo", "gizmo", 560, 900, .66)],
          "gpad": [("gizmo", "gizmo", 400, 960, .56)],      # watching from the grass, far from the pad
          "gsky": [("gizmo", "gizmo", 300, 760, .5)],       # never in the picture (hidden in every gsky shot)
          "gspace": [("gizmo", "gizmo", 300, 760, .5)], **GZ_INTRO_STAGES}     # gspace: Gizmo never in the picture (hidden in every gspace shot)
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
GQ = lambda place: WV(place, ["gizmo"], floor=.70, top=.46)
GP = lambda place: WV(place, ["gizmo"], floor=.72, top=.42)
GPL = lambda place: WV(place, ["gizmo"], floor=.62, top=.42)        # Gizmo smaller: room for a word under him (gc_ep01 Short 2 stills)
GCAM = lambda place, w=1000: C(place, "gizmo", "all", w)


def LIFT(at, sel, dy=-520, d=2.6, ease="power2.in", what="the rocket lifts off"): return ("to", at, sel, {"y": f"{'+' if dy > 0 else '-'}={abs(dy)}", "duration": d, "ease": ease}, what)
def GAS(at, sel, what="hot gas rushes out"): return [ON(at, sel, what), ("to", at, sel + "-p", {"scale": 1.08, "transformOrigin": "50% 0%", "duration": .25, "yoyo": True, "repeat": 9}, "")]
def DROP3(at, p="rk"): return [("to", at, "#{p}" + p + "-s3", {"y": 420, "rotation": 8, "opacity": 0, "duration": 1.8, "ease": "power1.in", "svgOrigin": "0 -100"}, "the bottom part drops away"),
                               ("to", at, "#{p}" + p + "-g3", {"opacity": 0, "duration": .3}, "")]


# ------------------------------------------------------------------ places and cameras
RX, RY, RS = 1300, 800, .8                 # the rocket on the launch pad
PAD = (960, 540, 1920); PADC = (RX, 560, 950); PADP = (RX, 400, 1500); PADG = GCAM("gpad", 900); PADQ = (RX - 60, 560, 1250)      # question shots on the pad: the signs clear the rocket
def rk_pad(name="rk", hidden=False): return prop(name, A.rocket, RX, RY, RS, hidden, p=(RX, RY, RS))
BX, BY, BS = 960, 760, .6                  # low and small: the answer signs at the top never touch the nose (stills r1)                 # the rocket on the board
BOARD = (960, 540, 1500); PBOARD = (960, 470, 1700)
def rk_board(name="rk"): return prop(name, A.rocket, BX, BY, BS, p=(BX, BY + 120, BS))
SX, SY = 1230, 740                         # the model rocket on the bench
BEN = (960, 540, 1800); BENC = (SX - 40, 520, 1050); BENP = (900, 560, 1500); BENCP = (SX - 40, 520, 1000)
def rk_bench(): return prop("mr", A.rocket, SX, SY, .55, p=(SX, SY, .55))
KX, KY = 960, 900                          # the rocket high in the sky
SKY = (960, 540, 1920); SKYC = (KX, 560, 1300); SKYP = (KX, 560, 1500)
SPACE = (960, 540, 1920); SPACEP = (960, 560, 1500)
WIN = (960, 520, 1700); WINP = (1000, 430, 1150)
JETY = 230


SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("gpad", PADC, "How does a big rocket fly up, up into the sky?", q=True, tag="hook: rocket on the pad", pcam=PADP, hide=["gizmo"],
      props=[rk_pad()], fx=GAS("w:fly", "#{p}rk-g3") + [LIFT("w:up,:2", "#{p}rk_w", -560, 2.2)], words=[("w:sky?", "?", .2, .28, 2.0, "sun", (.3, .4), 1.3)]),
    S("gsky", SKY, "No wings to flap! Whoosh, through the clouds!", tag="hook: through the clouds", pcam=SKYP, hide=["gizmo"],
      props=[prop("rs", A.rocket_small, KX, 1300, .9, p=(KX, 1300, .9))], fx=GAS(0.05, "#{p}rs-g") + [LIFT(0.1, "#{p}rs_w", -900, 3.4, "sine.inOut", "the rocket zooms up")],
      words=[("w:Whoosh,", "WHOOSH!", .76, .3, 1.1, "sun", (.5, .4), .95)]),
    S("glab", (GX, 640, 1000), "Hi! I'm Gizmo. Let's find out how rockets fly!", tag="hook: Gizmo", pcam=GP("glab"), fx=[WAVE("w:Hi!"), HOP("w:find")],
      words=[("w:Gizmo.", "GIZMO", .78, .3, 1.1, "pill", (.5, .36), .9)]),
    # ---------------------------------------------------------------- MAIN INTRO (right after the hook; again as the last four shots)
    *gz_intro_shots(),
    S("glab", WIDE, "Welcome to my lab, rocket fans!", trans="iris", tag="lab wide", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=[WAVE("w:Welcome", 4)],
      words=[("w:lab,", "HELLO!", .74, .5, 1.2, "pill", (.5, .36), 1.0)]),
    S("gbench", BEN, "Today we look inside a rocket, step by step.", tag="bench wide", pcam=BENP, props=[rk_bench()],
      fx=[PULSE("w:rocket,", "#{p}mr_w", 3, 1.06)], words=[("w:step", "STEP BY STEP", .5, .14, .95, "sun", (.5, .36), .8)]),
    # ---------------------------------------------------------------- PART 1: what pushes a rocket up
    S("gbench", BENC, "Here is my model rocket. A pointy nose, and fins.", part=1, tag="the model close", pcam=BENCP, hide=["gizmo"], props=[rk_bench()],
      fx=[PULSE("w:nose,", "#{p}mr-top", 3, 1.05), PULSE("w:fins.", "#{p}mr-s3", 3, 1.04)],
      words=[("w:nose,", "NOSE", .3, .2, 1.0, "sun", (.24, .44), .8), ("w:fins.", "FINS", .3, .8, 1.0, "", (.22, .62), .8)]),
    S("paper_gz", BOARD, "Inside, a rocket carries fuel. The engine uses the fuel.", part=1, tag="fuel", pcam=PBOARD, props=[rk_board()],
      fx=[ON("w:fuel.:1", "#{p}rk-fuel", "the fuel tank lights up"), PULSE("w:engine", "#{p}rk-fuel", 3, 1.08)],
      words=[("w:fuel.:1", "FUEL", .24, .5, 1.1, "sun", (.25, .62), .9)]),
    S("paper_gz", BOARD, "What does the engine turn the fuel into? Hot gas, or ice cream?", part=1, q=True, tag="question 1", pause=3.2, pcam=PBOARD, props=[rk_board()],
      fx=[ON(0, "#{p}rk-fuel"), ("signs", "w:Hot", ["HOT GAS", "ICE CREAM"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Hot gas! The engine turns its fuel into hot gas.", part=1, tag="hot gas", pcam=PBOARD, props=[rk_board()],
      fx=[ON(0, "#{p}rk-fuel")] + GAS("w:gas.", "#{p}rk-g3"), words=[("w:Hot", "HOT GAS!", .76, .3, 1.0, "sun", (.5, .36), .9)]),
    S("paper_gz", (BX, 760, 1300), "Then it pushes the gas out of its back. Whoosh!", part=1, tag="out the back", pcam=PBOARD, props=[rk_board(), prop("ad", A.updown, 1260, 880, 1.0, p=(1250, 880, .8))],
      fx=GAS(0, "#{p}rk-g3") + [ON("w:out", "#{p}ad-dn", "an arrow points down")], words=[("w:Whoosh!", "WHOOSH!", .24, .3, 1.1, "sun", (.3, .4), .9)]),
    S("glab", GCAM("glab"), "Out the back? Hmm. What happens next?", part=1, q=True, tag="hmm", pcam=GPL("glab"), pause=.6, fx=[("face", "w:Hmm.", "gizmo", "wow")] + IDEA("w:next?"),
      words=[("w:Hmm.", "HMM...", .8, .3, 1.0, "sun", (.5, .72), .9)]),
    S("paper_gz", BOARD, "The gas goes down. Which way does the rocket go? Up, or down?", part=1, q=True, tag="question 2", pause=3.2, pcam=PBOARD,
      props=[rk_board(), prop("ad", A.updown, 1260, 880, 1.0, p=(1250, 880, .8))], fx=GAS(0, "#{p}rk-g3") + [ON(0, "#{p}ad-dn"), ("signs", "w:Up,", ["UP", "DOWN"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Up! The gas goes down, so the rocket goes up!", part=1, tag="rocket goes up", pcam=PBOARD,
      props=[rk_board(), prop("ad", A.updown, 1260, 880, 1.0, p=(1250, 880, .8)), prop("au", A.updown, 1260, 330, 1.0, p=(1250, 300, .9))],
      fx=GAS(0, "#{p}rk-g3") + [ON(0, "#{p}ad-dn"), ON("w:up!", "#{p}au-upa", "an arrow points up"), LIFT("w:up!", "#{p}rk_w", -90, 1.4, "power1.out")],
      words=[("w:down,", "DOWN", .86, .86, .9, "", (.78, .6), .8), ("w:up!", "UP!", .86, .14, 1.1, "sun", (.78, .4), .9)]),
    S("gpad", PADG, "Let's watch a real rocket, on its launch pad.", part=1, tag="watch the pad", pcam=GP("gpad"), props=[rk_pad()], fx=[("face", "w:real", "gizmo", "wow"), PULSE("w:pad.", "#{p}rk_w", 3, 1.04)],
      words=[("w:pad.", "LAUNCH PAD", .7, .2, .9, "sun", (.5, .36), .75)]),
    S("gpad", PAD, "The gas pushes the rocket the other way. Up it goes!", part=1, tag="pad lift-off", pcam=PADP, cam2=W(PAD, 1.0), props=[rk_pad()],
      fx=GAS("w:gas", "#{p}rk-g3") + [LIFT("w:Up", "#{p}rk_w", -620, 2.4), HOP("w:goes!")], words=[("w:Up", "UP IT GOES!", .7, .14, .9, "sun", (.5, .38), .8)]),
    S("paper_gz", BOARD, "It is a push, and a push back. Push, and push back!", part=1, tag="push and push back", pcam=PBOARD, props=[prop("hd", A.hands, 960, 560, 1.4, p=(960, 600, 1.0))],
      fx=[("to", "w:push,", "#{p}hd-l", {"x": 40, "duration": .3, "yoyo": True, "repeat": 3}, "the hands push"), ("to", "w:push,", "#{p}hd-r", {"x": -40, "duration": .3, "yoyo": True, "repeat": 3}, "")],
      words=[("w:push,", "PUSH", .3, .25, 1.1, "sun", (.5, .38), .9), ("w:back.", "PUSH BACK", .7, .78, 1.0, "", (.5, .7), .8)]),
    S("glab", GCAM("glab"), "Press your hands together, like this. Do they push back?", part=1, q=True, tag="press hands", pause=1.2, pcam=GPL("glab"), fx=ARMS("w:Press", 55, -55, 2.4, "Gizmo presses his hands together"),
      words=[("w:Press", "PRESS!", .8, .3, 1.0, "sun", (.5, .72), .9)]),
    S("paper_gz", BOARD, "Scientists say it simply. Every push has a push back!", part=1, tag="every push", pcam=PBOARD, props=[rk_board(), prop("ad", A.updown, 1260, 880, 1.0, p=(1250, 880, .8)), prop("au", A.updown, 1260, 330, 1.0, p=(1250, 300, .9))],
      fx=GAS(0, "#{p}rk-g3") + [ON("w:push:1", "#{p}ad-dn"), ON("w:back!", "#{p}au-upa")], words=[("w:Every", "EVERY PUSH...", .3, .2, .9, "sun", (.5, .38), .75), ("w:back!", "...A PUSH BACK!", .3, .68, .9, "", (.5, .6), .75)]),
    S("gbench", (900, 560, 1500), "Say it with me. Gas goes down! Rocket goes up!", part=1, q=True, tag="say it", pcam=GPL("gbench"), props=[rk_bench()], fx=DOWN("w:Gas", .9) + UP("w:Rocket", 1.0),
      words=[("w:Gas", "GAS, DOWN!", .48, .8, .9, "", (.5, .72), .75), ("w:Rocket", "ROCKET, UP!", .6, .2, .9, "sun", (.5, .36), .75)]),
    S("glab", GCAM("glab"), "Crouch down low, like a rocket. Ready? Blast off!", part=1, q=True, tag="crouch and jump", pause=.6, pcam=GPL("glab"), fx=[CURL("w:Crouch", 2.0), HOP("w:Blast", 2)],
      words=[("w:Crouch", "CROUCH!", .8, .7, .9, "", (.5, .72), .85), ("w:Blast", "BLAST OFF!", .8, .22, 1.0, "sun", (.5, .36), .85)]),
    S("gpad", PADQ, "What comes out of a rocket's engine? Hot gas, or water?", part=1, q=True, tag="question 3", pause=3.2, pcam=PADP, hide=["gizmo"], props=[rk_pad()],
      fx=GAS(0, "#{p}rk-g3") + [("signs", "w:Hot", ["HOT GAS", "WATER"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Hot gas! Fuel, hot gas, and a big push. Up, up, up!", part=1, tag="part 1 recap", pcam=PBOARD, props=[rk_board()],
      fx=[ON("w:Fuel,", "#{p}rk-fuel")] + GAS("w:gas,:2", "#{p}rk-g3") + [LIFT("w:Up,", "#{p}rk_w", -120, 1.6, "power1.out")],
      words=[("w:Fuel,", "FUEL", .2, .3, .9, "sun", (.25, .4), .75), ("w:gas,:2", "GAS", .2, .5, .9, "sun", (.25, .5), .75), ("w:push.", "PUSH!", .8, .3, 1.0, "sun", (.75, .4), .8)]),
    # ---------------------------------------------------------------- PART 2: no air in space
    S("gspace", SPACE, "Way up high, a rocket flies into space.", part=2, trans="iris", tag="space wide", pcam=SPACEP, hide=["gizmo"], cam2=W(SPACE, 1.0),
      props=[prop("rs", A.rocket_small, 760, 1000, .8, p=(900, 1050, .8))], fx=GAS(0.05, "#{p}rs-g") + [LIFT(0.1, "#{p}rs_w", -380, 3.2, "sine.out", "the rocket flies up")],
      words=[("w:space.", "SPACE!", .7, .3, 1.1, "sun", (.74, .44), .9)]),
    S("gspace", SPACE, "But wait! In space, there is no air at all.", part=2, tag="no air", pcam=SPACEP, hide=["gizmo"],
      props=[prop("rs", A.rocket_small, 760, 620, .8, p=(900, 900, .8))], fx=GAS(0, "#{p}rs-g") + [("to", 0.1, "#{p}rs_w", {"y": "-=40", "duration": 1.6, "yoyo": True, "repeat": 1, "ease": "sine.inOut"}, "the rocket floats")],
      words=[("w:air", "NO AIR!", .7, .3, 1.2, "sun", (.5, .4), 1.0)]),
    S("glab", GCAM("glab"), "No air? Then how can a rocket work up there? Hmm.", part=2, q=True, tag="hmm 2", pause=.6, pcam=GPL("glab"), fx=[("face", "w:air?", "gizmo", "wow")] + IDEA("w:Hmm."),
      words=[("w:air?", "NO AIR?", .8, .3, 1.0, "sun", (.5, .72), .9)]),
    S("gwindow", WIN, "Look, a jet plane! A jet needs air from outside to work.", part=2, tag="jet needs air", pcam=(730, 520, 1450), props=[prop("jt", A.jet, 520, JETY, .55, p=(520, 260, .45))],
      fx=[("to", 0.1, "#{p}jt_w", {"x": "+=420", "duration": 4.0, "ease": "none"}, "the jet flies by"), ON("w:air", "#{p}jt-air", "air goes into the jet")],
      words=[("w:air", "AIR", .78, .62, 1.1, "sun", (.72, .5), .9)]),
    S("gwindow", (1000, 360, 1000), "Its engines take in air, as it flies along.", part=2, tag="jet close", pcam=(1000, 330, 900), hide=["gizmo"], props=[prop("jt", A.jet, 820, JETY + 80, .8, p=(940, 340, .45))],
      fx=[ON(0.2, "#{p}jt-air", "air goes into the jet"), ("to", 0.1, "#{p}jt_w", {"x": "+=110", "duration": 4.0, "ease": "none"}, "the jet flies")],
      words=[("w:air,", "AIR IN!", .74, .74, 1.0, "sun", (.5, .64), .85)]),
    S("paper_gz", BOARD, "Can a rocket work in space, where there is no air? Yes, or no?", part=2, q=True, tag="question 4", pause=3.2, pcam=PBOARD, props=[rk_board()],
      fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("gspace", (900, 520, 1300), "Yes! A rocket engine does not need air.", part=2, tag="yes it works", pcam=SPACEP, hide=["gizmo"],
      props=[prop("rs", A.rocket_small, 900, 760, .9, p=(1060, 900, .8))], fx=GAS(0, "#{p}rs-g") + [LIFT("w:Yes!", "#{p}rs_w", -160, 3.0, "sine.out")],
      words=[("w:Yes!", "YES!", .24, .3, 1.2, "sun", (.28, .4), 1.0)]),
    S("paper_gz", BOARD, "It carries everything it needs, right inside the rocket!", part=2, tag="carries everything", pcam=PBOARD, props=[rk_board()],
      fx=[ON("w:carries", "#{p}rk-fuel"), PULSE("w:inside", "#{p}rk-fuel", 3, 1.1)], words=[("w:everything", "EVERYTHING!", .24, .3, .9, "sun", (.5, .38), .75)]),
    S("glab", GCAM("glab"), "Like packing a backpack for a trip. All inside!", part=2, tag="backpack", pcam=GPL("glab"), fx=[HOP("w:All"), ("face", "w:backpack", "gizmo", "wow")],
      words=[("w:backpack", "A BACKPACK!", .8, .3, .85, "sun", (.5, .72), .75)]),
    S("paper_gz", BOARD, "Which one needs air from outside? The jet, or the rocket?", part=2, q=True, tag="question 5", pause=3.2, pcam=PBOARD,
      props=[prop("jt", A.jet, 560, 560, .75, p=(960, 440, .7)), prop("rs", A.rocket_small, 1400, 760, 1.0, p=(1230, 1100, .7))],
      fx=[("signs", "w:jet,", ["JET", "ROCKET"], 0, "wait:2.0"), ON("wait:2.05", "#{p}jt-air", "air goes into the jet")]),
    S("paper_gz", BOARD, "The jet! A rocket brings what it needs along.", part=2, tag="the jet", pcam=PBOARD,
      props=[prop("jt", A.jet, 560, 560, .75, p=(960, 440, .7)), prop("rs", A.rocket_small, 1400, 760, 1.0, p=(1230, 1100, .7))],
      fx=[ON("w:jet!", "#{p}jt-air", "air goes into the jet"), PULSE("w:rocket", "#{p}rs_w", 3, 1.06)], words=[("w:jet!", "THE JET!", .3, .2, 1.0, "sun", (.5, .38), .85)]),
    S("paper_gz", BOARD, "Air from outside? The jet needs it. The rocket does not!", part=2, tag="jet yes rocket no", pcam=PBOARD,
      props=[prop("jt", A.jet, 560, 560, .75, p=(960, 440, .7)), prop("rs", A.rocket_small, 1400, 760, 1.0, p=(1230, 1100, .7))],
      fx=[ON("w:jet", "#{p}jt-air", "air goes into the jet"), PULSE("w:rocket", "#{p}rs_w", 3, 1.06)],
      words=[("w:jet", "JET: YES", .3, .2, .9, "sun", (.5, .38), .75), ("w:not!", "ROCKET: NO", .74, .82, .9, "", (.36, .62), .7)]),
    S("gspace", SPACE, "So a rocket engine works in space, where there is no air.", part=2, tag="works in space", pcam=SPACEP, hide=["gizmo"],
      props=[prop("rs", A.rocket_small, 600, 800, .8, p=(800, 900, .8))], fx=GAS(0, "#{p}rs-g") + [("to", 0.1, "#{p}rs_w", {"x": "+=380", "y": "-=200", "rotation": 20, "duration": 4.0, "ease": "sine.inOut"}, "the rocket flies on")],
      words=[("w:works", "IT WORKS!", .7, .2, 1.0, "sun", (.5, .38), .85)]),
    S("gpad", PADG, "Now let's watch one more launch, from far away.", part=2, tag="one more launch", pcam=GP("gpad"), props=[rk_pad()], fx=[HOP("w:launch,"), PULSE("w:away.", "#{p}rk_w", 3, 1.04)],
      words=[("w:launch,", "ONE MORE!", .7, .2, .9, "sun", (.5, .36), .8)]),
    S("glab", GCAM("glab"), "Let's count down for a launch! Ready? Three, two, one...", part=2, q=True, tag="count down", pcam=GPL("glab"), fx=IDEA("w:launch!"),
      words=[("w:Three,", "3", .82, .2, 1.4, "sun", (.25, .74), 1.0), ("w:two,", "2", .82, .45, 1.4, "sun", (.5, .74), 1.0), ("w:one...", "1", .82, .7, 1.4, "sun", (.75, .74), 1.0)]),
    S("gpad", PAD, "Blast off! Up it goes, higher and higher!", part=2, tag="blast off", pcam=PADP, cam2=W(PAD, 1.0), props=[rk_pad()],
      fx=GAS("w:Blast", "#{p}rk-g3") + [LIFT("w:Up", "#{p}rk_w", -700, 2.6), HOP("w:higher")], words=[("w:Blast", "BLAST OFF!", .7, .14, 1.0, "sun", (.5, .38), .85)]),
    S("gsky", SKYC, "Up through the clouds, and out into space!", part=2, tag="up through the clouds", pcam=SKYP, hide=["gizmo"],
      props=[prop("rs", A.rocket_small, KX, 1250, .9, p=(KX, 1300, .9))], fx=GAS(0.05, "#{p}rs-g") + [LIFT(0.1, "#{p}rs_w", -900, 3.2, "sine.inOut", "the rocket zooms up")],
      words=[("w:space!", "SPACE!", .3, .25, 1.1, "sun", (.5, .4), .9)]),
    S("glab", GCAM("glab"), "Say it with me. A rocket does not need air!", part=2, q=True, tag="say it 2", pcam=GPL("glab"), fx=[HOP("w:air!")],
      words=[("w:air!", "NO AIR NEEDED!", .8, .3, .8, "sun", (.5, .64), .7)]),
    S("gspace", (1150, 480, 1200), "Rockets carry satellites like this one up into space.", part=2, tag="satellite", pcam=(1150, 520, 1300), hide=["gizmo"],
      props=[prop("st", A.satellite, 1150, 480, .9, True, p=(1150, 520, .8))], fx=[("show", "w:satellites", "st"), ("to", "w:space.", "#{p}st_w", {"rotation": 8, "duration": 1.4, "yoyo": True, "repeat": 1, "ease": "sine.inOut"}, "the satellite turns")],
      words=[("w:satellites", "A SATELLITE!", .5, .14, .9, "sun", (.5, .38), .8)]),
    S("gspace", (1150, 480, 1200), "Can you point to the satellite? Point!", part=2, q=True, tag="point satellite", pause=1.0, pcam=(1150, 520, 1300), hide=["gizmo"],
      props=[prop("st", A.satellite, 1150, 480, .9, p=(1150, 520, .8))], fx=[PULSE("w:satellite?", "#{p}st_w", 5, 1.08)],
      words=[("w:Point!", "POINT!", .5, .82, 1.1, "sun", (.5, .72), .9)]),
    # ---------------------------------------------------------------- PART 3: stages
    S("gbench", BENC, "Big rockets have a trick. They are built in parts.", part=3, trans="iris", tag="built in parts", pcam=BENCP, hide=["gizmo"], props=[rk_bench()],
      fx=[PULSE("w:trick.", "#{p}mr_w", 1, 1.05), PULSE("w:parts.", "#{p}mr-s3", 1, 1.05)], words=[("w:trick.", "A TRICK!", .3, .2, 1.0, "sun", (.26, .44), .8)]),
    S("paper_gz", BOARD, "Let's count the parts. One, two, three!", part=3, q=True, tag="count parts", pcam=PBOARD, props=[rk_board()],
      fx=[PULSE("w:One,", "#{p}rk-s3", 1, 1.05), PULSE("w:two,", "#{p}rk-s2", 1, 1.05), PULSE("w:three!", "#{p}rk-top", 1, 1.05)],
      words=[("w:One,", "1", .72, .62, 1.3, "sun", (.75, .62), 1.0), ("w:two,", "2", .72, .42, 1.3, "sun", (.75, .5), 1.0), ("w:three!", "3", .72, .22, 1.3, "sun", (.75, .38), 1.0)]),
    S("paper_gz", BOARD, "A heavy rocket needs a big push, to get off the ground.", part=3, tag="heavy needs a big push", pcam=PBOARD, props=[rk_board()],
      fx=GAS("w:push,", "#{p}rk-g3") + [("to", "w:push,", "#{p}rk-g3", {"scale": 1.25, "transformOrigin": "50% 0%", "duration": .6}, "a big push")],
      words=[("w:heavy", "HEAVY!", .24, .3, 1.0, "sun", (.5, .36), .8), ("w:push,", "BIG PUSH!", .76, .8, 1.0, "", (.5, .43), .8)]),
    S("gsky", SKYC, "When the bottom part runs out of fuel, it drops away.", part=3, tag="bottom part drops", pcam=SKYP, hide=["gizmo"],
      props=[prop("rk", A.rocket, KX, KY, .8, p=(KX, KY + 150, .8))], fx=GAS(0, "#{p}rk-g3") + DROP3("w:drops"), words=[("w:drops", "DROP!", .78, .7, 1.1, "sun", (.75, .62), .9)]),
    S("gsky", SKYC, "Bye-bye, bottom part! Now the next part starts its engine.", part=3, tag="next part", pcam=SKYP, hide=["gizmo"],
      props=[prop("rk", A.rocket, KX, KY, .8, p=(KX, KY + 150, .8))], fx=[OFF("#{p}rk-s3", "#{p}rk-g3")] + GAS("w:engine.", "#{p}rk-g2") + [LIFT("w:engine.", "#{p}rk_w", -260, 2.0, "power1.in")],
      words=[("w:Bye-bye,", "BYE-BYE!", .76, .3, 1.0, "sun", (.5, .38), .85)]),
    S("glab", (900, 470, 1700), "Is it easier to run with a heavy bag, or with no bag?", part=3, q=True, tag="question bag", pause=3.2, pcam=GQ("glab"),
      fx=[("signs", "w:heavy", ["HEAVY BAG", "NO BAG"], 1, "wait:2.0"), HOP("wait:2.05")]),
    S("paper_gz", BOARD, "Is the rocket lighter now, or heavier?", part=3, q=True, tag="question 6", pause=3.2, pcam=PBOARD, props=[rk_board()],
      fx=[OFF("#{p}rk-s3"), ("signs", "w:lighter", ["LIGHTER", "HEAVIER"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Lighter! A lighter rocket can go much higher.", part=3, tag="lighter goes higher", pcam=PBOARD, props=[rk_board()],
      fx=[OFF("#{p}rk-s3")] + GAS(0, "#{p}rk-g2") + [LIFT("w:higher.", "#{p}rk_w", -150, 1.6, "power1.out")], words=[("w:higher.", "HIGHER!", .76, .2, 1.1, "sun", (.75, .4), .9)]),
    S("gsky", SKYC, "Up, and up, and up it goes!", part=3, tag="up and up", pcam=SKYP, hide=["gizmo"],
      props=[prop("rk", A.rocket, KX, KY, .8, p=(KX, KY + 150, .8))], fx=[OFF("#{p}rk-s3", "#{p}rk-g3")] + GAS(0, "#{p}rk-g2") + [LIFT(0.1, "#{p}rk_w", -420, 2.6, "power1.in")],
      words=[("w:goes!", "UP!", .76, .3, 1.2, "sun", (.75, .4), .95)]),
    S("glab", GCAM("glab"), "Stack your fists, one on top of the other, like rocket parts!", part=3, q=True, tag="stack fists", pause=1.2, pcam=GPL("glab"), fx=ARMS("w:Stack", 60, -70, 2.6, "Gizmo stacks his hands"),
      words=[("w:Stack", "STACK!", .8, .3, 1.0, "sun", (.5, .72), .9)]),
    S("gspace", SPACE, "This trick is called staging. It helps rockets reach space.", part=3, trans="iris", tag="staging", pcam=SPACEP, hide=["gizmo"],
      props=[prop("rs", A.rocket_small, 700, 820, .8, p=(900, 900, .8))], fx=GAS(0, "#{p}rs-g") + [LIFT("w:helps", "#{p}rs_w", -300, 2.6, "sine.inOut")],
      words=[("w:staging.", "STAGING", .7, .2, 1.0, "sun", (.72, .5), .8)]),
    S("gspace", (1500, 360, 1100), "And even all the way to the Moon! Wow!", part=3, tag="the Moon", pcam=(1500, 420, 1100), hide=["gizmo"],
      props=[prop("mn", A.moon, 1500, 330, 1.0, p=(1500, 400, .9)), prop("rs", A.rocket_small, 1250, 600, .45, p=(1380, 680, .45))],
      fx=[PULSE("w:Moon!", "#{p}mn_w", 3, 1.06), GAS(0, "#{p}rs-g")[0], ("to", 0.1, "#{p}rs_w", {"x": "+=70", "y": "-=90", "rotation": 25, "duration": 2.4, "ease": "sine.inOut"}, "the rocket flies to the Moon")],
      words=[("w:Moon!", "THE MOON!", .5, .82, 1.0, "sun", (.5, .7), .85)]),
    S("paper_gz", BOARD, "What does a big rocket drop as it flies? An empty part, or its nose?", part=3, q=True, tag="question 7", pause=3.2, pcam=PBOARD, props=[rk_board()],
      fx=[("signs", "w:empty", ["EMPTY PART", "ITS NOSE"], 0, "wait:2.0")]),
    S("gsky", SKYC, "An empty part! Drop it, and go higher.", part=3, tag="drop and go higher", pcam=SKYP, hide=["gizmo"],
      props=[prop("rk", A.rocket, KX, KY, .8, p=(KX, KY + 150, .8))], fx=GAS(0, "#{p}rk-g3") + DROP3("w:Drop") + GAS("w:higher.", "#{p}rk-g2") + [LIFT("w:higher.", "#{p}rk_w", -200, 1.6, "power1.in")],
      words=[("w:empty", "EMPTY!", .76, .3, 1.0, "sun", (.75, .4), .85)]),
    S("gspace", (960, 700, 1500), "Look how high we are! There is the Earth, way down below.", part=3, tag="the Earth below", pcam=(960, 720, 1300), hide=["gizmo"],
      props=[prop("rs", A.rocket_small, 1300, 600, .5, p=(1150, 620, .5))], fx=[GAS(0, "#{p}rs-g")[0], ("to", "w:Earth,", "#{p}rs_w", {"y": "-=60", "duration": 2.0, "ease": "sine.inOut"}, "the rocket flies on")],
      words=[("w:Earth,", "THE EARTH!", .3, .3, 1.0, "sun", (.38, .55), .8)]),
    S("glab", GCAM("glab", 1250), "Say it together. Drop a part, go higher!", part=3, q=True, tag="say it 3", pcam=GPL("glab"), fx=DOWN("w:Drop", .9) + UP("w:higher!", 1.0),
      words=[("w:Drop", "DROP A PART!", .82, .7, .7, "", (.5, .72), .7), ("w:higher!", "GO HIGHER!", .82, .22, .8, "sun", (.5, .36), .75)]),
    S("gpad", PADG, "And some rockets take astronauts into space!", part=3, tag="astronauts", pcam=GP("gpad"), props=[rk_pad()],
      fx=[("face", "w:astronauts", "gizmo", "wow"), HOP("w:space!")], words=[("w:astronauts", "ASTRONAUTS!", .7, .2, .9, "sun", (.5, .36), .75)]),
    S("glab", GCAM("glab"), "Wave to the rocket! Bye-bye, rocket! Have a good trip!", part=3, q=True, tag="wave", pause=1.0, pcam=GPL("glab"), fx=[WAVE("w:Wave", 5)],
      words=[("w:Wave", "WAVE!", .8, .3, 1.1, "sun", (.5, .72), .9)]),
    # ---------------------------------------------------------------- QUIZ + GOODBYE
    S("glab", WIDE, "Quiz time! Let's remember what we learned.", part=4, trans="iris", tag="quiz time", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=IDEA("w:Quiz"),
      words=[("w:Quiz", "QUIZ TIME!", .74, .5, 1.3, "sun", (.5, .36), 1.0)]),
    S("gbench", (900, 470, 1700), "What comes out of a rocket's engine? Hot gas, or bubbles?", part=4, q=True, tag="quiz 1", pause=3.2, pcam=GQ("gbench"), props=[rk_bench()],
      fx=[("signs", "w:Hot", ["HOT GAS", "BUBBLES"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Hot gas! The gas goes down, and the rocket goes up.", part=4, tag="quiz 1 answer", pcam=PBOARD, props=[rk_board()],
      fx=GAS("w:Hot", "#{p}rk-g3") + [LIFT("w:up.", "#{p}rk_w", -120, 1.4, "power1.out")]),
    S("gspace", SPACE, "Does a rocket engine need air? Yes, or no?", part=4, q=True, tag="quiz 2", pause=3.2, pcam=SPACEP, hide=["gizmo"], trans="iris",
      props=[prop("rs", A.rocket_small, 760, 700, .8, p=(900, 820, .8))], fx=GAS(0, "#{p}rs-g") + [("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("gspace", SPACE, "No! It carries everything it needs.", part=4, tag="quiz 2 answer", pcam=SPACEP, hide=["gizmo"],
      props=[prop("rs", A.rocket_small, 760, 700, .8, p=(900, 820, .8))], fx=GAS(0, "#{p}rs-g") + [LIFT("w:carries", "#{p}rs_w", -220, 2.4, "sine.inOut")],
      words=[("w:No!", "NO!", .7, .3, 1.2, "sun", (.5, .4), 1.0)]),
    S("gsky", SKYC, "When the bottom part drops away, is the rocket lighter, or heavier?", part=4, q=True, tag="quiz 3", pause=3.2, pcam=SKYP, hide=["gizmo"], trans="iris",
      props=[prop("rk", A.rocket, KX, KY, .8, p=(KX, KY + 150, .8))], fx=[OFF("#{p}rk-s3", "#{p}rk-g3")] + GAS(0, "#{p}rk-g2") + [("signs", "w:lighter,", ["LIGHTER", "HEAVIER"], 0, "wait:2.0")]),
    S("gsky", SKYC, "Lighter! So it can go much higher.", part=4, tag="quiz 3 answer", pcam=SKYP, hide=["gizmo"],
      props=[prop("rk", A.rocket, KX, KY, .8, p=(KX, KY + 150, .8))], fx=[OFF("#{p}rk-s3", "#{p}rk-g3")] + GAS(0, "#{p}rk-g2") + [LIFT("w:higher.", "#{p}rk_w", -300, 1.8, "power1.in")],
      words=[("w:Lighter!", "LIGHTER!", .76, .3, 1.0, "sun", (.75, .4), .85)]),
    S("gpad", PAD, "Gas goes down, rocket goes up! Thanks for exploring with me!", part=4, tag="goodbye", pcam=GP("gpad"), cam2=W(PAD, 1.0), props=[rk_pad()],
      fx=GAS("w:Gas", "#{p}rk-g3") + [LIFT("w:up!", "#{p}rk_w", -700, 2.6), WAVE("w:Thanks", 5), HOP("w:exploring")],
      words=[("w:Thanks", "BYE-BYE!", .3, .2, 1.1, "pill", (.5, .36), .9)]),
    *gz_intro_shots(),      # the main intro again, as the last four shots
]
for _s in SHOTS:
    _s["who"] = "gizmo"        # Gizmo speaks every line, so his mouth moves (gc_ep01 kept the default who="milo": no mouth, found Nov 21)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)     # a picture board never drifts closer (zc_ep08)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)
    for _f in _s["fx"]:        # 9:16: a word never sits on the title band's second line
        if _f[0] == "word" and len(_f) > 3 and "p" in _f[3] and _s["pcam"]: _f[3]["p"]["y"] = max(_f[3]["p"]["y"], round(_s["pcam"][1] - .15 * _s["pcam"][2]))

SHORTS = [
    {"id": "gc_ep02_short1", "title": "What Pushes a Rocket Up? Gizmo Explains", "band": ("WHAT PUSHES", "IT UP?"), "thumb_text": "WHOOSH!", "part": 1,
     "extra_first": [S("gpad", PADC, "What pushes a rocket up into the sky?", part=1, q=True, tag="hook: what pushes it up", pcam=PADP, hide=["gizmo"], who="gizmo",
                       props=[rk_pad()], fx=GAS("w:pushes", "#{p}rk-g3") + [LIFT("w:sky?", "#{p}rk_w", -200, 1.6, "power1.in")], words=[("w:sky?", "?", .2, .28, 2.0, "sun", (.3, .4), 1.3)])]},
    {"id": "gc_ep02_short2", "title": "Can a Rocket Fly in Space? Gizmo Explains", "band": ("CAN IT FLY", "IN SPACE?"), "thumb_text": "NO AIR!", "part": 2,
     "extra_first": [S("gspace", SPACE, "Can a rocket fly in space, with no air?", part=2, q=True, tag="hook: no air", pcam=SPACEP, hide=["gizmo"], who="gizmo",
                       props=[prop("rs", A.rocket_small, 760, 700, .8, p=(900, 820, .8))], fx=GAS(0, "#{p}rs-g") + [("to", 0.1, "#{p}rs_w", {"y": "-=60", "duration": 1.5, "yoyo": True, "repeat": 1, "ease": "sine.inOut"}, "the rocket floats")],
                       words=[("w:air?", "?", .7, .3, 2.0, "sun", (.5, .4), 1.3)])]},
    {"id": "gc_ep02_short3", "title": "Why Do Big Rockets Drop Parts? Gizmo Explains", "band": ("WHY DROP", "PARTS?"), "thumb_text": "BYE-BYE!", "part": 3,
     "extra_first": [S("gsky", SKYC, "Why do big rockets drop parts as they fly?", part=3, q=True, tag="hook: why drop parts", pcam=SKYP, hide=["gizmo"], who="gizmo",
                       props=[prop("rk", A.rocket, KX, KY, .8, p=(KX, KY + 150, .8))], fx=GAS(0, "#{p}rk-g3") + DROP3("w:drop"), words=[("w:drop", "?", .76, .3, 2.0, "sun", (.75, .4), 1.3)])]},
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
    "gc_ep02": {"place": "gsky", "cam": (1060, 520, 1500), "actors": [],
                "props": [(_lit(A.rocket, "g3"), 1180, 700, .78)],
                "words": [("BLAST", 560, 400, 200, ""), ("OFF!", 560, 640, 230, "sun")]},
    "gc_ep02_short1": {"place": "paper_gz", "cam": (960, 600, 1500), "actors": [],
                       "props": [(_lit(A.rocket, "g3"), 960, 870, 1.0)],
                       "words": [("WHOOSH!", 540, 360, 200, "sun")]},
    "gc_ep02_short2": {"place": "gspace", "cam": (900, 560, 1300), "actors": [],
                       "props": [(_lit(A.rocket_small, "g"), 900, 760, 1.1)],
                       "words": [("NO", 540, 380, 230, ""), ("AIR!", 540, 1600, 250, "sun")]},
    "gc_ep02_short3": {"place": "gsky", "cam": (960, 640, 1400), "actors": [],
                       "props": [(lambda p: _lit(A.rocket, "g2")(p).replace(f'id="{p}-s3"', f'opacity="0" id="{p}-s3"'), 960, 980, .85),
                                 (lambda p: A.rocket(p).replace(f'id="{p}-s2"', f'opacity="0" id="{p}-s2"').replace(f'id="{p}-top"', f'opacity="0" id="{p}-top"'), 1010, 1230, .7)],
                       "words": [("BYE-BYE!", 540, 300, 190, "sun")]},

}
