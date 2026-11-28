"""zc_ep16: "How Do Sea Turtles Breathe?" - Ocean week, fact lesson (2D, docs/CARTOON_RUN.md "A fact lesson and its three Shorts", "VIRAL PACKAGING",
"MAIN INTRO"), a cartoon fact lesson with the 3D music-and-sync process ("beat"). Cold open on Tula the green sea turtle swimming under the
water with bubbles going up: "Tula lives in the sea. How does a sea turtle breathe?". Milo says his name after the hook; the main intro right
after the hook and again as the last shots. Three parts ("Tula's three breathing secrets"), each cut whole into one Short, each opening on its
own question with answer signs and thinking time:
1. a sea turtle cannot breathe under the water; it has no gills to take air from the water; it is a reptile and breathes air, like you; like
   other reptiles it has lungs, right under its shell,
2. it must come up to the top of the water to breathe; it pops its head out for a breath, then down it goes; green sea turtles eat seagrass
   and algae, then swim up for air,
3. a resting sea turtle can hold its breath for hours; when it swims and looks for food it comes up more often; sea turtles can even sleep
   under the water; while it holds its breath its heart beats very slowly, which saves its air.
Quiz with the three secrets, recap, the closing names the next Ocean week lesson ("Can a Turtle Leave Its Shell?").
za_ep15 (adventure, Nov 28) also has Tula coming up for air; this lesson teaches it as facts with questions, the day after.

FACTS, read at the source on Nov 27 2026, about 5:50-6:00 PM ET (pages read by the session's page reader, which quoted the sentences verbatim):
 [SI] Smithsonian Ocean, Sea Turtles (ocean.si.edu/ocean-life/reptiles/sea-turtles)
   "As reptiles, they require air to breathe and land to lay their eggs."   "Sea turtles cannot breathe underwater, but they can hold their breath
   for long periods of time"   "between 4 to 7 hours when resting."   "While holding their breath, their heart rate slows significantly to conserve
   oxygen"   "Sea turtles, including this Kemp's ridley, must come to the surface to breathe air."   "they feed mostly on plants, like seagrass and algae."
 [ORP] Olive Ridley Project, "Can sea turtles breathe underwater?" (oliveridleyproject.org/ufaqs/can-sea-turtles-breathe-underwater)
   "Sea turtles cannot breathe underwater, however they can hold their breath for long periods of time."   "a resting turtle can remain underwater
   for 4-7 hours whereas a foraging individual may need to surface more frequently."   "When turtles hold their breath, their heart rate slows
   significantly to conserve oxygen"   "A green turtle popping its head above water for a breath, Maldives."
 [ORP-B] Olive Ridley Project, "How do sea turtles breathe?" (oliveridleyproject.org/?p=13140)
   "Just like other reptiles, sea turtles have lungs."   "The lungs are located right under the carapace and the vertebral column."
 [SD] Scuba Diving, "How Do Sea Turtles Breathe?" (David Shiffman, Ask a Marine Biologist)
   "They need to breathe air as they do not have gills so they cannot extract oxygen directly from the water."
 [SWOT] State of the World's Sea Turtles, "How long can sea turtles hold their breath?" (seaturtlestatus.org, 2024-02-14)
   "they must hold their breath for at least several hours in order to forage for food, avoid predators, and sleep underwater."
   "sea turtles will dive for 20 to 40 minutes while foraging and up to several hours when sleeping."   "Sea turtles decrease their heart rate while diving."
 [FLMNH] Florida Museum, "Tell me about: sea turtle adaptations": "sea turtles are reptiles and breathe air, which means they cannot breathe
   underwater."   "Sea turtles must hold their breath for extended periods while swimming, feeding, and even sleeping below the waves!"
   "They have the remarkable ability to slow their heart rate and conserve oxygen,"
 [NOAA] NOAA Fisheries, "10 tremendous turtle facts": "Green sea turtles are unique among sea turtles in that they are primarily herbivores, eating
   mostly seagrasses and algae."  (the page's breathing item was returned only as a summary: not used)
 Said as: a sea turtle cannot breathe under the water [SI, ORP, FLMNH]; it has no gills, so it cannot take air from the water [SD]; a sea turtle is a
 reptile and breathes air, like you [SI, FLMNH]; like other reptiles it has lungs [ORP-B], right under its shell [ORP-B]; it must come up to the top
 of the water to breathe [SI]; it pops its head out of the water for a breath [ORP]; green sea turtles eat seagrass and algae [NOAA, SI]; a resting
 sea turtle can hold its breath for hours [SI, ORP]; when it swims and looks for food it comes up more often [ORP, SWOT]; sea turtles can even sleep
 under the water [SWOT, FLMNH]; while it holds its breath its heart beats very slowly, and that saves its air [SI, ORP, FLMNH, SWOT].
 "Air" is said for oxygen (ages 2-6). Read but NOT said: the minutes and hours in numbers, the seven-hour record, minutes between heartbeats,
 cold water, leatherbacks' lungs.
 Kid safety: the children are never asked to hold their breath; the copy-me moves are a hand on the chest with slow breaths, popping the head up,
 tapping slowly, resting the head on the hands. Nobody is hurt, lost, crying or trapped; Tula is happy and calm the whole time.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_za_ep12 as A12     # Tula's PT/BOX, the sea places, seagrass, bubbles
import art_za_ep14 as A15     # the zzz picture
import art_za_ep13            # the "kelp" place
import art_zc_ep16 as A
from kit import Kit, S, prop, W
from intro import INTRO_STAGES, intro_shots

EP = {"id": "zc_ep16", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "How Do Sea Turtles Breathe?", "thumb_text": "NO GILLS?!", "series": "Animal Facts with Milo",
      "description": ("How does a sea turtle breathe in the sea? Find Tula the green sea turtle's three breathing secrets with Milo the bluebird! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to count, moves to copy and a quiz at the end.\n"
                      "Kids learn that a sea turtle cannot breathe under the water because it has no gills: it is a reptile that breathes air with lungs right "
                      "under its shell; that it must swim up to the top of the water and pop its head out for a breath; and that a resting sea turtle can hold "
                      "its breath for hours and even sleep under the water, while its heart beats very slowly to save its air.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSmithsonian Ocean (sea turtles); Olive Ridley Project (sea turtle breathing); State of the World's Sea Turtles "
                      "(how long sea turtles hold their breath); Florida Museum of Natural History (sea turtle adaptations); NOAA Fisheries (turtle facts); "
                      "Scuba Diving, Ask a Marine Biologist (how sea turtles breathe)."),
      "tags": ["how do sea turtles breathe", "sea turtle facts for kids", "sea turtle", "ocean animals for kids", "green sea turtle", "do turtles have gills",
               "animal facts for kids", "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

WL = A.WL
STAGES = {
    "reef": [("tur", "turtle", 900, 700, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
    "ocean": [("tur", "turtle", 900, 760, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
    "kelp": [("tur", "turtle", 900, 780, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
    "surface": [("tur", "turtle", 900, WL + 110, 1.0), ("milo", "milo", 300, 280, .72, False, True)],
    "zoo": [("milo", "milo", 960, 940, 1.1)],
    "zoo_eve": [("milo", "milo", 960, 940, 1.0)],
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 1100, 0, -90))


def PULSE(at, sel, k=1.2, n=1, o="50% 50%"): return ("to", at, sel, {"scale": k, "transformOrigin": o, "duration": .2, "yoyo": True, "repeat": 2 * n - 1}, "a picture pulses")
def PADDLE(at, n=4, who="tur"):     # Tula swims: both flippers stroke
    return [("to", at, f"#{{p}}{who}-ff", {"rotation": -26, "svgOrigin": "100 -120", "duration": .3, "yoyo": True, "repeat": 2 * n - 1, "ease": "sine.inOut"}, "Tula paddles"),
            ("to", at, f"#{{p}}{who}-bf", {"rotation": 18, "svgOrigin": "-140 -120", "duration": .3, "yoyo": True, "repeat": 2 * n - 1, "ease": "sine.inOut"}, "")]
def RISE(at, dy=370, d=1.4, who="tur"): return ("to", at, f"#{{p}}{who}_w", {"y": f"-={dy}", "duration": d, "ease": "power1.inOut"}, "Tula swims up")
def SINK(at, dy=370, d=1.4, who="tur"): return ("to", at, f"#{{p}}{who}_w", {"y": f"+={dy}", "duration": d, "ease": "power1.inOut"}, "Tula swims down")
def HEADUP(at, deg=-16, who="tur"): return ("to", at, f"#{{p}}{who}-neck", {"rotation": deg, "svgOrigin": "180 -170", "duration": .35, "ease": "back.out(2)"}, "Tula lifts her head")
def SLEEPY(at, who="tur"): return ("to", at, f"#{{p}}{who}-eye-lid", {"opacity": 1, "duration": .05}, "Tula closes her eyes")
def BUBBLES(at, name): return ("fromto", at, f"#{{p}}{name}-b0,#{{p}}{name}-b1,#{{p}}{name}-b2,#{{p}}{name}-b3,#{{p}}{name}-b4,#{{p}}{name}-b5", {"y": 60, "opacity": 0},
                               {"y": -80, "opacity": 1, "duration": .9, "stagger": .15, "ease": "sine.out"}, "bubbles rise")


# ------------------------------------------------------------------ props and cameras
WATER = lambda: prop("wo", A.water_over, 960, WL, 1.0, p=(960, WL, 1.0))
BUB = lambda name="bu", x=None, y=None, s=1.0, hid=False: prop(name, A.bubble_col, x or P("reef", "tur", "head")[0] + 70, y or P("reef", "tur", "head")[1] - 40, s, hid,
                                                                p=(x or P("reef", "tur", "head")[0] + 70, y or P("reef", "tur", "head")[1] - 40, s))
GRASS = lambda: prop("sg", A12.seagrass_front, 1520, 880, 1.0, p=(1500, 880, 1.0))
RB = C("reef", "tur", "all", 1300, 40, -40); RBP = WV("reef", ["tur"], floor=.7, top=.46, pad=.3)
RH = C("reef", "tur", "head", 760, -60, 0); RHP = V("reef", "tur", "head", 1400, -160, 40)
OB = C("ocean", "tur", "all", 1300, 40, -40); OBP = WV("ocean", ["tur"], floor=.7, top=.46, pad=.3)
SU = (980, 520, 1500); SUP = (980, 560, 1700)                 # the surface: the water line across the middle
SUH = (1150, 470, 900); SUHP = (1150, 520, 1000)               # Tula's head at the water line
LUNG = lambda: prop("lu", A.lungs_cut, 860, 600, 1.0, p=(900, 700, .82))
HEART = lambda: prop("ht", A.slow_heart, 960, 560, 1.0, p=(960, 640, .7))
CLOCK = lambda x=1500, y=360, s=1.0, hid=True, p=(960, 560, .9): prop("ck", A.big_clock, x, y, s, hid, p=p)
def BREATHE(at, n=2): return ("to", at, "#{p}lu-lungs", {"scaleY": 1.16, "scaleX": 1.08, "transformOrigin": "50% 100%", "duration": .7, "yoyo": True, "repeat": 2 * n - 1, "ease": "sine.inOut"}, "the lungs fill with air and empty")
def BEAT(at, n=2): return ("to", at, "#{p}ht-h", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 1, "repeatDelay": 1.6}, "the heart beats, slowly")
def DOT(at, d=4.0): return ("fromto", at, "#{p}ht-dot", {"x": 0}, {"x": 1200, "duration": d, "ease": "none"}, "the dot travels along the slow heartbeat")
def SPIN(at): return ("to", at, "#{p}ck-min", {"rotation": 720, "svgOrigin": "0 0", "duration": 2.2, "ease": "power1.inOut"}, "the clock's hand goes round and round")
LEDGE = lambda: prop("lg", A.rest_ledge, 760, 870, 1.0, p=(760, 870, 1.0))

SHOTS = [
    # ---------------------------------------------------------------- HOOK (cold open on the promise: Tula under the water, bubbles going up)
    S("reef", RB, "Tula lives in the sea. How does a sea turtle breathe?", q=True, tag="hook: Tula under the sea", hide=["milo"], pcam=RBP, cam2=W(RB, 1.05),
      props=[BUB("bu", hid=False)], fx=PADDLE(0, 6) + [BUBBLES("w:sea.", "bu"), BUBBLES("w:breathe?", "bu")], words=[("w:breathe?", "BREATHE?", .78, .2, 1.1, "sun", (.5, .32), .9)]),
    S("reef", RH, "Does she breathe the water? Or something else?", q=True, tag="hook: breathe the water?", hide=["milo"], pcam=RHP, cam2=W(RH, 1.06),
      fx=[("lookat", "w:water?", "tur", -6), ("lookat", "e:else?", "tur", 4)], words=[("e:else?", "?", .2, .3, 2.0, "sun", (.5, .34), 1.3)]),
    S("surface", say="I'm Milo the bluebird. Let's find Tula's breathing secrets!", q=True, tag="hook: Milo", hide=["tur"], fx=[("hop", "w:secrets!", "milo")],
      words=[("w:secrets!", "SECRETS!", .8, .45, 1.0, "sun", (.5, .33), .9)], **dict(cam=C("surface", "milo", "body", 900), pcam=V("surface", "milo", "body", 1100, 0, -90))),
    *intro_shots(),
    S("ocean", OB, "Tula has three breathing secrets. Let's find them, one by one!", q=True, tag="three secrets", trans="iris", hide=["milo"], pcam=OBP, cam2=W(OB, 1.05),
      fx=PADDLE(0, 4) + [("nod", "w:three", "tur")],
      words=[("w:three", "1", .22, .2, 1.1, "sun", (.3, .3), 1.0), ("w:secrets.", "2", .5, .2, 1.1, "sun", (.5, .3), 1.0), ("w:one:1", "3", .78, .2, 1.1, "sun", (.7, .3), 1.0)]),
    # ---------------------------------------------------------------- PART 1: air and lungs
    S("reef", RH, "Breathing secret number one! Can a sea turtle breathe under the water?", part=1, q=True, tag="secret 1", hide=["milo"], pcam=RHP, pcam2=W(RHP, .94), cam2=W(RH, 1.05),
      props=[BUB("bu")], fx=[BUBBLES("w:breathe", "bu")], words=[("w:one!", "1", .62, .12, 1.4, "sun", (.3, .3), 1.2), ("e:water?", "?", .88, .22, 2.0, "sun", (.75, .36), 1.1)]),
    S("reef", RB, "Yes, it can? Or no, it can't?", part=1, q=True, tag="question 1a", pause=3.2, hide=["milo"], pcam=RBP,
      fx=PADDLE("w:Yes,", 3) + [("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("reef", RH, "No! A sea turtle cannot breathe under the water.", part=1, tag="no, it cannot", hide=["milo"], pcam=RHP, cam2=W(RH, .95),
      fx=[("nod", "w:cannot", "tur")], words=[("w:No!", "NO!", .2, .26, 1.4, "sun", (.5, .3), 1.1)]),
    S("reef", RB, "It has no gills, so it cannot take air from the water.", part=1, tag="no gills", hide=["milo"], pcam=RBP, cam2=W(RB, 1.05),
      fx=PADDLE(0, 4) + [("nod", "w:gills,", "tur")], words=[("w:gills,", "NO GILLS!", .28, .2, 1.0, "sun", (.5, .3), .9)]),
    S("reef", RH, "A sea turtle is not a fish. It is a reptile!", part=1, tag="not a fish", hide=["milo"], pcam=RHP, cam2=W(RH, 1.05),
      fx=[("nod", "w:reptile!", "tur")], words=[("w:reptile!", "REPTILE!", .2, .26, 1.1, "sun", (.5, .3), .9)]),
    S("surface", SU, "A sea turtle is a reptile. It breathes air, just like you!", part=1, tag="breathes air like you", hide=["milo"], pcam=SUP, cam2=W(SU, .95),
      props=[WATER()], fx=[HEADUP("w:air,"), ("nod", "w:you!", "tur")], words=[("w:air,", "AIR!", .78, .14, 1.3, "sun", (.5, .28), 1.0)]),
    S("paper", (1000, 560, 1600), "Just like other reptiles, a sea turtle has lungs.", part=1, tag="board: lungs", pcam=(1000, 640, 1700), props=[LUNG()],
      fx=[PULSE("w:lungs.", "#{p}lu-lungs", 1.1, 2, "50% 100%")], words=[("w:lungs.", "LUNGS!", .5, .1, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper_blue", (860, 500, 1150), "Its lungs are right under its shell. Look! In, and out.", part=1, tag="board: under the shell", pcam=(990, 620, 1750), pcam2=(970, 620, 1550), cam2=(900, 500, 1080), props=[LUNG()],
      fx=[PULSE("w:shell.", "#{p}lu-shell", 1.03, 1), ("to", "w:In,", "#{p}lu-air", {"opacity": 1, "duration": .2}, "air comes in"), BREATHE("w:In,", 2)],
      words=[("w:In,", "IN!", .22, .2, 1.0, "sun", (.25, .36), .9), ("w:out.", "OUT!", .78, .2, 1.0, "sun", (.75, .36), .9)]),
    S("paper", (1100, 580, 1700), "When Tula breathes in, her lungs fill up with air. When she breathes out, the air goes out.", part=1, tag="board: lungs fill", pcam=(1040, 660, 1800), pcam2=(1000, 640, 1500), cam2=(1000, 560, 1350), props=[LUNG()],
      fx=[("to", "w:in,", "#{p}lu-air", {"opacity": 1, "duration": .2}, "air comes in"), BREATHE("w:in,", 1), BREATHE("w:out,", 1)],
      words=[("w:fill", "FILL UP!", .5, .22, 1.0, "sun", (.5, .36), .9)]),
    S("paper_blue", (1000, 560, 1500), "Wow! Lungs, under a shell!", part=1, tag="board: wow lungs", pcam=(1000, 640, 1600), props=[LUNG()],
      fx=[PULSE("w:Lungs,", "#{p}lu-lungs", 1.1, 2, "50% 100%"), PULSE("w:shell!", "#{p}lu-shell", 1.03)], words=[("w:Wow!", "WOW!", .5, .1, 1.3, "sun", (.5, .3), 1.0)]),
    S("zoo", say="Put your hand on your chest. Breathe in, and out, nice and slow.", part=1, q=True, tag="hand on your chest", pause=3.0, fx=[("hop", "w:in,", "milo"), ("hop", "w:out,", "milo")],
      words=[("w:in,", "IN!", .82, .3, .9, "sun", (.5, .33), .8), ("w:out,", "OUT!", .82, .42, .9, "sun", (.5, .4), .8)], **MILO("zoo", 940)),
    S("zoo", say="Breathe in with me. One, two, three. And out!", part=1, q=True, tag="breathe in, count three", pause=1.6, fx=[("hop", "w:One,", "milo"), ("hop", "w:two,", "milo"), ("hop", "w:three.", "milo")],
      words=[("w:One,", "1", .2, .3, 1.2, "sun", (.15, .42), 1.0), ("w:two,", "2", .2, .5, 1.2, "sun", (.85, .42), 1.0), ("w:three.", "3", .8, .4, 1.2, "sun", (.15, .6), 1.0)], **MILO("zoo", 1300)),
    S("surface", SUH, "What does a sea turtle need, to breathe?", part=1, q=True, tag="what does it need", pause=3.0, hide=["milo"], pcam=SUHP, cam2=W(SUH, 1.06),
      props=[WATER()], fx=[HEADUP("w:need,", -8)], words=[("e:breathe?", "?", .85, .2, 2.0, "sun", (.8, .3), 1.1)]),
    S("surface", SU, "Air! Up here, above the water.", part=1, tag="air above the water", hide=["milo"], pcam=SUP, cam2=W(SU, 1.05),
      props=[WATER(), prop("np", A.nose_puff, P("surface", "tur", "head")[0] + 100, P("surface", "tur", "head")[1] - 30, 1.0, True, p=(P("surface", "tur", "head")[0] + 100, P("surface", "tur", "head")[1] - 30, 1.0))],
      fx=[HEADUP("w:Air!"), ("show", "w:Air!", "np"), PULSE("w:above", "#{p}np_w", 1.2, 2)], words=[("w:Air!", "AIR!", .22, .14, 1.3, "sun", (.5, .28), 1.0)]),
    S("surface", SU, "Say it with me. A sea turtle breathes air!", part=1, q=True, tag="say it: breathes air", hide=["milo"], pcam=SUP, cam2=W(SU),
      props=[WATER()], fx=[HEADUP("w:Say"), ("nod", "w:air!", "tur")], words=[("w:Say", "SAY IT!", .22, .14, 1.1, "sun", (.5, .28), .9)]),
    S("zoo", say="Now take a big, slow breath, like Tula. In, and out!", part=1, q=True, tag="big slow breath", pause=2.4, fx=[("hop", "w:In,", "milo"), ("hop", "w:out!", "milo")],
      words=[("w:In,", "BIG BREATH!", .8, .3, .85, "sun", (.5, .33), .8)], **MILO("zoo", 1300)),
    S("reef", RB, "Quick check! Does a sea turtle have gills? Yes, or no?", part=1, q=True, tag="question 1b", pause=3.2, hide=["milo"], pcam=RBP, cam2=W(RB, .95),
      fx=PADDLE("w:gills?", 3) + [("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("reef", RH, "No gills! Great job!", part=1, tag="great job 1", hide=["milo"], pcam=RHP, cam2=W(RH), fx=[("nod", "w:Great", "tur")],
      words=[("w:gills!", "GREAT!", .2, .26, 1.3, "sun", (.5, .3), 1.0)]),
    # ---------------------------------------------------------------- PART 2: up to the top for air
    S("ocean", OB, "Breathing secret number two! Where does a sea turtle go, to breathe air?", part=2, q=True, tag="secret 2", trans="iris", hide=["milo"], pcam=OBP, pcam2=W(OBP, .94), cam2=W(OB, 1.05),
      move={"tur": (700, 760, 1.0)}, props=[BUB("b2", 1460, 600, 1.0)], fx=PADDLE(0, 8) + [("walk", "w:Breathing", "tur", 260, 3.0), BUBBLES("w:Where", "b2"), ("lookat", "w:Where", "tur", -8)], words=[("w:two!", "2", .2, .2, 1.4, "sun", (.3, .3), 1.2), ("e:air?", "?", .8, .2, 2.0, "sun", (.7, .34), 1.3)]),
    S("kelp", C("kelp", "tur", "all", 1500, 80, -100), "Up to the top of the water? Or down to the sand?", part=2, q=True, tag="question 2a", pause=3.2, hide=["milo"], pcam=WV("kelp", ["tur"], floor=.72, top=.46, pad=.3), cam2=W(C("kelp", "tur", "all", 1500, 80, -100), .86),
      fx=PADDLE("w:Up", 3) + [("signs", "w:Up", ["UP", "DOWN"], 0, "wait:2.0")]),
    S("surface", SU, "Up to the top! Sea turtles must come up to the top, to breathe.", part=2, tag="up to the top", hide=["milo"], pcam=SUP, cam2=W(SU, 1.04), move={"tur": (900, WL + 530, 1.0)},
      props=[WATER()], fx=PADDLE("w:Up", 5) + [RISE("w:Up", 370, 1.6), HEADUP("w:breathe.")], words=[("w:Up", "UP!", .22, .14, 1.3, "sun", (.5, .28), 1.0)]),
    S("surface", (980, 360, 1400), "Look up! Can you see the sky? That is where the air is.", part=2, q=True, tag="look up at the sky", pause=1.0, hide=["milo"], pcam=(980, 420, 1700), cam2=(980, 330, 1460),
      props=[WATER()], fx=[HEADUP("w:Look", -22), HEADUP("w:air", -12)], words=[("w:sky?", "SKY!", .5, .12, 1.2, "sun", (.5, .28), .9)]),
    S("surface", SUH, "Look! Tula pops her head out of the water, and takes a breath.", part=2, tag="pops her head out", pause=0.8, hide=["milo"], pcam=SUHP, cam2=W(SUH, .94),
      props=[WATER(), prop("np", A.nose_puff, P("surface", "tur", "head")[0] + 100, P("surface", "tur", "head")[1] - 30, 1.0, True, p=(P("surface", "tur", "head")[0] + 100, P("surface", "tur", "head")[1] - 30, 1.0))],
      fx=[HEADUP("w:pops"), ("show", "w:breath.", "np")], words=[("w:pops", "POP!", .2, .14, 1.3, "sun", (.5, .28), 1.0)]),
    S("surface", SUH, "Breathe in! The air goes into her lungs.", part=2, tag="air into her lungs", pause=0.8, hide=["milo"], pcam=SUHP, cam2=W(SUH, 1.05),
      props=[WATER(), prop("np", A.nose_puff, P("surface", "tur", "head")[0] + 100, P("surface", "tur", "head")[1] - 30, 1.0, True, p=(P("surface", "tur", "head")[0] + 100, P("surface", "tur", "head")[1] - 30, 1.0))],
      fx=[HEADUP(0.1), ("show", "w:Breathe", "np"), ("to", "w:lungs.", "#{p}np_w", {"x": "-=60", "opacity": 0, "duration": .6}, "the air goes in")], words=[("w:Breathe", "BREATHE IN!", .22, .14, 1.0, "sun", (.5, .28), .85)]),
    S("surface", SU, "Then she swims back down again.", part=2, tag="down again", hide=["milo"], pcam=SUP, cam2=W(SU, 1.05),
      props=[WATER()], fx=[HEADUP(0.1, -16), HEADUP("w:down", 0), SINK("w:down", 330, 1.6)] + PADDLE("w:down", 5), words=[("w:down", "DOWN!", .22, .14, 1.2, "sun", (.5, .28), .9)]),
    S("surface", SU, "How many times does Tula pop up? Count with me! One, two, three!", part=2, q=True, tag="count the pops", hide=["milo"], pcam=(800, 560, 1700), cam2=W(SU, .96), move={"tur": (600, WL + 330, 1.0)},
      props=[WATER()], fx=[("to", f"w:{w}", "#{p}tur_w", {"y": "-=170", "duration": .3, "yoyo": True, "repeat": 1, "ease": "sine.inOut"}, "Tula pops up") for w in ("One,", "two,", "three!")],
      words=[("w:One,", "1", .62, .16, 1.3, "sun", (.86, .3), 1.0), ("w:two,", "2", .76, .16, 1.3, "sun", (.86, .4), 1.0), ("w:three!", "3", .9, .16, 1.3, "sun", (.86, .5), 1.0)]),
    S("kelp", C("kelp", "tur", "all", 1300, 80, -60), "Green sea turtles eat seagrass and algae. Munch, munch! Yummy!", part=2, tag="eats seagrass", hide=["milo"], pcam=WV("kelp", ["tur"], floor=.7, top=.46, pad=.3),
      props=[GRASS()], fx=[("lookat", "w:eat", "tur", 14), ("to", "w:Munch,", "#{p}tur-jaw", {"opacity": 1, "duration": .12, "yoyo": True, "repeat": 5}, "Tula munches"),
                         ("to", "w:Munch,", "#{p}sg-b0", {"scaleY": .8, "transformOrigin": "50% 100%", "duration": .3}, "a blade gets shorter")],
      words=[("w:seagrass", "SEAGRASS!", .26, .2, 1.0, "sun", (.5, .3), .85)]),
    S("kelp", C("kelp", "tur", "all", 1300, 80, -60), "Tula eats under the water. But she always comes back up, to breathe.", part=2, tag="always comes back up", hide=["milo"], pcam=WV("kelp", ["tur"], floor=.7, top=.46, pad=.3), cam2=W(C("kelp", "tur", "all", 1300, 80, -60), 1.05),
      props=[GRASS()], fx=[("lookat", "w:eats", "tur", 14), ("lookat", "w:up,", "tur", -16)] + PADDLE("w:back", 3), words=[("w:up,", "UP!", .26, .2, 1.3, "sun", (.5, .3), 1.0)]),
    S("surface", SU, "Then up she swims, for air!", part=2, tag="then up for air", hide=["milo"], pcam=SUP, cam2=W(SU, 1.04), move={"tur": (900, WL + 530, 1.0)},
      props=[WATER()], fx=PADDLE("w:up", 4) + [RISE("w:up", 370, 1.4), HEADUP("w:air!")], words=[("w:air!", "AIR!", .22, .14, 1.3, "sun", (.5, .28), 1.0)]),
    S("zoo", say="Look up, way up high, where the air is!", part=2, q=True, tag="look up high", pause=2.4, fx=[("hop", "w:high,", "milo"), ("hop", "wait:1.0", "milo")],
      words=[("w:high,", "UP HIGH!", .82, .3, .9, "sun", (.5, .33), .8)], **MILO("zoo", 1300)),
    S("zoo", say="Swim up like Tula, and pop your head up! Pop!", part=2, q=True, tag="pop your head up", pause=2.4, fx=[("hop", "w:Pop!", "milo"), ("hop", "wait:1.0", "milo")],
      words=[("w:Pop!", "POP!", .82, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("surface", SU, "Say it with me. A sea turtle swims up to breathe!", part=2, q=True, tag="say it: swims up", hide=["milo"], pcam=SUP, cam2=W(SU),
      props=[WATER()], fx=[HEADUP("w:Say"), ("nod", "w:breathe!", "tur")], words=[("w:Say", "SAY IT!", .22, .14, 1.1, "sun", (.5, .28), .9)]),
    S("zoo", say="Can you paddle your arms like flippers? Paddle, paddle!", part=2, q=True, tag="paddle like flippers", pause=2.4, fx=[("hop", "w:Paddle,", "milo"), ("hop", "w:paddle!", "milo"), ("hop", "wait:1.0", "milo")],
      words=[("w:Paddle,", "PADDLE!", .82, .3, .9, "sun", (.5, .33), .8)], **MILO("zoo", 1300)),
    S("ocean", OB, "Quick check! When Tula needs air, does she swim up? Or does she stay down?", part=2, q=True, tag="question 2b", pause=3.2, hide=["milo"], pcam=OBP, pcam2=W(OBP, .88), cam2=W(OB, .84),
      fx=PADDLE("w:needs", 3) + [("signs", "w:up?", ["UP", "DOWN"], 0, "wait:2.0")]),
    S("surface", SU, "Up! Super swimming!", part=2, tag="super swimming", hide=["milo"], pcam=SUP, cam2=W(SU), props=[WATER()], fx=[HEADUP("w:Up!"), ("nod", "w:Super", "tur")],
      words=[("w:Super", "SUPER!", .22, .14, 1.3, "sun", (.5, .28), 1.0)]),
    # ---------------------------------------------------------------- PART 3: holding the breath, sleeping, a slow heart
    S("reef", RB, "Breathing secret number three! How long can a resting sea turtle hold its breath?", part=3, q=True, tag="secret 3", trans="iris", hide=["milo"], pcam=RBP, pcam2=W(RBP, .94), cam2=W(RB, 1.05),
      fx=[("lookat", "w:long", "tur", 6)], words=[("w:three!", "3", .2, .2, 1.4, "sun", (.3, .3), 1.2), ("e:breath?", "?", .8, .2, 2.0, "sun", (.7, .34), 1.3)]),
    S("reef", RB, "Just a few seconds? Or for hours?", part=3, q=True, tag="question 3a", pause=3.2, hide=["milo"], pcam=RBP,
      props=[CLOCK(1500, 330, .7, False, p=(720, 320, .4))], fx=[("signs", "w:few", ["SECONDS", "HOURS"], 1, "wait:2.0"), PULSE("wait:1.0", "#{p}ck_w", 1.08, 2)]),
    S("reef", RB, "For hours! A resting sea turtle can hold its breath, for hours!", part=3, tag="for hours", hide=["milo"], pcam=RBP, cam2=W(RB, .95),
      props=[CLOCK(1500, 330, .7, False, p=(720, 320, .4))], fx=[SPIN("w:hours!:1"), SPIN("w:hours!:2")], words=[("w:hours!:1", "HOURS!", .26, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("reef", RH, "That is a long, long time!", part=3, tag="a long time", pause=1.0, hide=["milo"], pcam=RHP, cam2=W(RH, 1.06),
      fx=[("nod", "w:long,", "tur")], words=[("w:long,", "SO LONG!", .2, .26, 1.1, "sun", (.5, .3), .9)]),
    S("ocean", OB, "When it swims and looks for food, it comes up more often.", part=3, tag="comes up more often", hide=["milo"], pcam=OBP, cam2=W(OB, 1.05),
      fx=PADDLE(0, 6) + [("lookat", "w:food,", "tur", 10), ("lookat", "w:up", "tur", -12)], words=[("w:up", "UP MORE!", .26, .2, 1.0, "sun", (.5, .3), .85)]),
    S("reef", (760, 680, 1300), "And look! Sea turtles can even sleep, under the water!", part=3, tag="sleep under water", hide=["milo"], pcam=(820, 640, 1500), cam2=(760, 680, 1240),
      move={"tur": (820, 860, 1.0)}, props=[LEDGE()], fx=[SLEEPY("w:sleep,")], words=[("w:sleep,", "SLEEP!", .76, .18, 1.2, "sun", (.5, .3), 1.0)]),
    S("reef", (760, 680, 1300), "Tula is resting under a rock. Sleepy, sleepy turtle.", part=3, tag="resting under a rock", hide=["milo"], pcam=(820, 640, 1500), cam2=(760, 680, 1360),
      move={"tur": (820, 860, 1.0)}, props=[LEDGE(), prop("zz", A15.zzz, 1180, 560, .9, True, p=(1000, 560, .65))],
      fx=[SLEEPY(0.05), ("show", "w:resting", "zz"), PULSE("w:Sleepy,", "#{p}zz_w", 1.1, 2)], words=[("w:Sleepy,", "SLEEPY!", .78, .18, 1.0, "sun", (.5, .3), .9)]),
    S("reef", (760, 680, 1300), "Let's be very quiet, and let Tula rest.", part=3, q=True, tag="let Tula rest", hide=["milo"], pcam=(820, 640, 1500), cam2=(760, 680, 1240),
      move={"tur": (820, 860, 1.0)}, props=[LEDGE(), prop("zz", A15.zzz, 1180, 560, .9, False, p=(1000, 560, .65))], fx=[SLEEPY(0.05), PULSE("w:quiet,", "#{p}zz_w", 1.1, 2)],
      words=[("w:quiet,", "QUIET!", .78, .18, 1.1, "sun", (.5, .3), .9)]),
    S("reef", RH, "How does Tula save her air?", part=3, q=True, tag="how does she save air", pause=3.0, hide=["milo"], pcam=RHP, cam2=W(RH, 1.06),
      fx=[("lookat", "w:save", "tur", -6)], words=[("e:air?", "?", .85, .2, 2.0, "sun", (.8, .3), 1.1)]),
    S("paper_pink", (960, 560, 1700), "Her heart beats very, very slowly. That saves her air!", part=3, tag="board: slow heart", pcam=(960, 640, 1500), props=[HEART()],
      fx=[BEAT("w:heart"), DOT("w:heart", 4.2), PULSE("w:saves", "#{p}ht-h", 1.08)], words=[("w:slowly.", "SLOW!", .82, .14, 1.2, "sun", (.5, .26), .9)]),
    S("paper_pink", (960, 560, 1700), "Count the slow beats with me. One, and two.", part=3, q=True, tag="board: count slow beats", pcam=(960, 640, 1500), props=[HEART()],
      fx=[PULSE("w:One,", "#{p}ht-h", 1.14), PULSE("w:two.", "#{p}ht-h", 1.14), DOT("w:Count", 3.6)],
      words=[("w:One,", "1", .2, .14, 1.3, "sun", (.3, .26), 1.1), ("w:two.", "2", .8, .14, 1.3, "sun", (.7, .26), 1.1)]),
    S("reef", RB, "Her heart beats slowly, so her air lasts a long time.", part=3, tag="air lasts long", pause=0.8, hide=["milo"], pcam=RBP, cam2=W(RB, 1.05),
      fx=[("nod", "w:lasts", "tur")], words=[("w:lasts", "SLOW!", .26, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("zoo", say="Can you tap slowly, like Tula's heart? Tap, and tap, and tap.", part=3, q=True, tag="tap slowly", pause=2.4, fx=[("hop", "w:Tap,", "milo"), ("hop", "w:tap,:2", "milo"), ("hop", "w:tap.:3", "milo")],
      words=[("w:Tap,", "TAP!", .82, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("reef", RB, "Say it with me. A sea turtle can hold its breath, for a long time!", part=3, q=True, tag="say it: a long time", hide=["milo"], pcam=RBP, cam2=W(RB),
      fx=[("nod", "w:long", "tur")], words=[("w:Say", "SAY IT!", .26, .2, 1.1, "sun", (.5, .3), .9)]),
    S("zoo", say="Rest your head on your hands, like a sleepy sea turtle. Night, night!", part=3, q=True, tag="rest your head", pause=2.4, fx=[("hop", "w:Night,", "milo")],
      words=[("w:Night,", "NIGHT, NIGHT!", .8, .3, .85, "sun", (.5, .33), .75)], **MILO("zoo", 1300)),
    S("reef", (760, 680, 1300), "Quick check! Can a sea turtle sleep under the water? Yes, or no?", part=3, q=True, tag="question 3b", pause=3.2, hide=["milo"], pcam=(820, 640, 1500), cam2=(760, 680, 1240),
      move={"tur": (820, 860, 1.0)}, props=[LEDGE()], fx=[SLEEPY(0.05), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("reef", RB, "Yes! You remembered!", part=3, tag="you remembered", hide=["milo"], pcam=RBP, cam2=W(RB), fx=[("nod", "w:remembered!", "tur")],
      words=[("w:Yes!", "YES!", .26, .2, 1.3, "sun", (.5, .3), 1.0)]),
    # ---------------------------------------------------------------- QUIZ
    S("zoo_eve", WIDE, "Three breathing secrets! Now it is quiz time!", part=4, trans="iris", tag="quiz time", cam2=(960, 560, 1860), pcam=(960, 560, 1800),
      words=[("w:quiz", "QUIZ TIME!", .5, .3, 1.3, "sun", (.5, .33))], fx=[("hop", "w:quiz", "milo", 2)]),
    S("reef", RB, "What does a sea turtle breathe? Water, or air?", part=4, q=True, tag="quiz 1", pause=3.2, hide=["milo"], pcam=RBP,
      fx=PADDLE("w:breathe?", 3) + [("signs", "w:Water,", ["WATER", "AIR"], 1, "wait:2.0")]),
    S("surface", SU, "Air! With its lungs.", part=4, tag="quiz 1: air", hide=["milo"], pcam=SUP, cam2=W(SU), props=[WATER()], fx=[HEADUP("w:Air!")],
      words=[("w:Air!", "AIR!", .22, .14, 1.3, "sun", (.5, .28), 1.0)]),
    S("ocean", OB, "Where does Tula go for air? Up to the top, or down to the sand?", part=4, q=True, tag="quiz 2", pause=3.2, hide=["milo"], pcam=OBP, pcam2=W(OBP, .88), cam2=W(OB, .84),
      fx=PADDLE("w:Where", 3) + [("signs", "w:Up", ["UP", "DOWN"], 0, "wait:2.0")]),
    S("surface", SU, "Up to the top! Pop!", part=4, tag="quiz 2: up", hide=["milo"], pcam=SUP, cam2=W(SU), move={"tur": (900, WL + 530, 1.0)},
      props=[WATER()], fx=[RISE("w:Up", 370, 1.2), HEADUP("w:Pop!")] + PADDLE("w:Up", 3), words=[("w:Pop!", "POP!", .22, .14, 1.3, "sun", (.5, .28), 1.0)]),
    S("reef", (760, 680, 1300), "Can a resting sea turtle hold its breath for hours? Yes, or no?", part=4, q=True, tag="quiz 3", pause=3.2, hide=["milo"], pcam=(820, 640, 1500),
      move={"tur": (820, 860, 1.0)}, props=[LEDGE()], fx=[SLEEPY(0.05), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("reef", RB, "Yes! For hours and hours.", part=4, tag="quiz 3: hours", hide=["milo"], pcam=RBP, cam2=W(RB), fx=[("nod", "w:hours", "tur")],
      words=[("w:hours", "HOURS!", .26, .2, 1.2, "sun", (.5, .3), 1.0)]),
    # ---------------------------------------------------------------- RECAP + GOODBYE
    S("surface", (960, 470, 1900), "Tula breathes air, she swims up to the top, and she can hold her breath for a long time. You found all three secrets!", part=4, trans="iris",
      tag="recap", hide=[], pcam=(980, 560, 2300), cam2=(960, 470, 1960), move={"milo": (1560, 260, .7, True, True)},
      props=[WATER()], fx=[HEADUP("w:air,"), ("hop", "w:top,", "milo"), ("nod", "w:long", "tur"), ("hop", "w:three", "milo")],
      words=[("w:air,", "1", .2, .14, 1.1, "sun", (.3, .28), 1.0), ("w:top,", "2", .4, .14, 1.1, "sun", (.5, .28), 1.0), ("w:long", "3", .6, .14, 1.1, "sun", (.7, .28), 1.0)]),
    S("zoo_eve", say="Breathe in and out. Pop your head up. And tap slowly, like Tula's heart!", part=4, q=True, tag="all three moves", pause=1.6,
      fx=[("hop", "w:Breathe", "milo"), ("hop", "w:Pop", "milo"), ("hop", "w:tap", "milo")],
      words=[("w:Pop", "POP!", .84, .3, .9, "sun", (.5, .33), .8)], **MILO("zoo_eve", 940)),
    S("paper_blue", (960, 540, 1500), "Next time: can a turtle leave its shell? Bye-bye, friends!", part=4, tag="next: leave its shell", pcam=(960, 440, 1700),
      actors=[("tur", "turtle", 900, 760, 1.1)], fx=[("nod", "w:shell?", "tur")],
      words=[("w:shell?", "NEXT TIME!", .5, .12, 1.1, "sun", (.5, .3), .9), ("w:Bye-bye,", "BYE-BYE!", .5, .8, 1.0, "pill", (.5, .72), .8)]),
    *intro_shots(),      # the main intro again as the last shots (owner, Nov 20 4:50 PM: at the beginning and at the end of every new long video)
]
for _s in SHOTS:        # a picture board never drifts closer: it only pulls out a little (16:9 and 9:16)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)

SHORTS = [
    {"id": "zc_ep16_short1", "title": "Can a Sea Turtle Breathe Under Water?", "band": ("BREATHE UNDER", "WATER?"), "thumb_text": "LUNGS!", "part": 1,
     "extra_first": [S("reef", RH, "Can a sea turtle breathe under the water?", part=1, q=True, tag="hook: breathe under water", hide=["milo"], pcam=(RHP[0], RHP[1], 820), pcam2=(RHP[0], RHP[1], 900), cam2=W(RH, 1.05),
                       props=[BUB("bu")], fx=[BUBBLES("w:breathe", "bu")], words=[("w:water?", "?", .2, .3, 2.0, "sun", (.75, .36), 1.1)])]},
    {"id": "zc_ep16_short2", "title": "Where Do Sea Turtles Go for Air?", "band": ("WHERE FOR", "AIR?"), "thumb_text": "POP UP!", "part": 2,
     "extra_first": [S("surface", SUH, "Where does a sea turtle go for air?", part=2, q=True, tag="hook: where for air", hide=["milo"], pcam=(SUHP[0], SUHP[1], 860), pcam2=(SUHP[0], SUHP[1], 940), cam2=W(SUH, 1.05),
                       props=[WATER()], fx=[HEADUP("w:air?")], words=[("w:air?", "?", .2, .3, 2.0, "sun", (.75, .36), 1.1)])]},
    {"id": "zc_ep16_short3", "title": "How Long Can a Sea Turtle Hold Its Breath?", "band": ("HOW LONG?", "BREATH?"), "thumb_text": "HOURS!", "part": 3,
     "extra_first": [S("reef", RB, "How long can a sea turtle hold its breath?", part=3, q=True, tag="hook: how long", hide=["milo"], pcam=(RBP[0], RBP[1], round(RBP[2] * .8)), pcam2=(RBP[0], RBP[1], round(RBP[2] * .86)), cam2=W(RB, 1.05),
                       props=[CLOCK(1500, 330, .7, False, p=(720, 320, .4))], fx=[SPIN("w:long")], words=[("w:breath?", "?", .8, .2, 2.0, "sun", (.75, .36), 1.1)])]},
]

# thumbnails (thumb.py): one big object, 1-2 words, none of the title's words, no watermark
THUMBS = {
    "zc_ep16": {"place": "surface", "cam": (1060, 460, 1560), "actors": [("turtle", 1000, WL + 110, 1.25, False, 'gsap.set("#P-neck",{rotation:-16,svgOrigin:"180 -170"});')],
                "props": [(A.water_over, 960, WL, 1.0), (A.bubble_col, 720, WL + 420, 1.2)], "words": [("NO GILLS?!", 560, 140, 150, "sun")]},
    "zc_ep16_short1": {"place": "paper", "cam": (1040, 560, 2300), "props": [(A.lungs_cut, 900, 600, 1.1)], "words": [("LUNGS!", 540, 1500, 210, "sun")]},
    "zc_ep16_short2": {"place": "surface", "cam": (1060, 560, 1700), "actors": [("turtle", 1000, WL + 110, 1.3, False, 'gsap.set("#P-neck",{rotation:-16,svgOrigin:"180 -170"});')],
                       "props": [(A.water_over, 960, WL, 1.0)], "words": [("POP UP!", 540, 1520, 200, "sun")]},
    "zc_ep16_short3": {"place": "reef", "cam": (960, 600, 1700), "actors": [("turtle", 900, 860, 1.3, False, 'gsap.set("#P-eye-lid",{opacity:1});')],
                       "props": [(A.big_clock, 780, 260, .9)], "words": [("HOURS!", 540, 1640, 210, "sun")]},
}
