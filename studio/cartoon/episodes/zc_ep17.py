"""zc_ep17: "Can a Turtle Leave Its Shell?" - Ocean week, fact lesson (2D, docs/CARTOON_RUN.md "A fact lesson and its three Shorts", "VIRAL
PACKAGING", "MAIN INTRO", "GOODBYE: LIKE AND SUBSCRIBE"), with the 3D music-and-sync process ("beat"). Cold open on Milo knocking on Tula's shell,
a little door doodled on it with a question mark: "Knock, knock! Tula, can you come out of your shell?". Milo says his name after the hook; the
main intro right after the hook and again as the last shots; Milo's like-and-subscribe goodbye right before the closing intro. Three parts
("Tula's three shell secrets"), each cut whole into one Short, each opening on its own question with answer signs and thinking time:
1. a turtle cannot leave its shell: the shell is part of its body, made of bones, joined to its backbone and its ribs (you have ribs and a
   backbone too),
2. the shell grows as the turtle grows, like your bones; its plates are called scutes and are made of the same stuff as your fingernails,
3. a sea turtle cannot pull its head (or its flippers) into its shell, many land turtles can; and the shell can feel a gentle touch (nerves).
Quiz with the three secrets, recap, the closing names the next Ocean week lesson ("What Do Sea Turtles Eat?").
Same friend as zc_ep16 (Nov 29 5:30 PM); this one is on Nov 30 (upload_guard's day rule).

FACTS, read at the source on Nov 28 2026, about 2:05-2:15 AM ET (pages read by the session's page reader, which quoted the sentences verbatim):
 [SDZ] San Diego Zoo Wildlife Alliance, Turtle and Tortoise (animals.sandiegozoo.org/animals/turtle-and-tortoise)
   "The turtle cannot crawl out of it because the shell is permanently attached to the spine and the rib cage."   "made up of 59 to 61 bones
   covered by plates called scutes"   "which are made of keratin like our fingernails"   "Turtles can feel pressure and pain through their shells,
   just as you can feel pressure through your fingernails."   "Some turtles can pull their heads, legs, and feet inside their shells."
 [DRU] Ask Dr. Universe, Washington State University (askdruniverse.wsu.edu, 2025-07-23): hopping out of the shell "could never happen in real life".
   "It's part of the turtle's body."   "The shell is the turtle's backbone and rib cage with the collarbone, shoulder bones and pelvic bones tucked inside."
   "As the turtle grows, its shell grows along with it—just like our bones do."   "In many turtles, it's made of keratin plates called scutes."
   "A turtle's shell is sensitive. It houses the spinal cord and lots of nerves."   "So, turtles can feel anything that touches their shell."
 [PBS] PBS Nature, Photo Essay: Turtle Anatomy: "This portion of the shell is composed of bone and contains the fused, broadened ribs."
   "The spine is fused to the carapace in all species except the leatherback."   "The carapace is covered with large scale-like structures made of
   keratin called scutes."   "The head is retractable within the shell for most terrestrial turtles and tortoises but not for the sea turtle."
   "A sea turtle's head remains out at all times."
 [SI] Smithsonian Ocean, Sea Turtles: "the head and limbs of sea turtles are fixed outside the shell and cannot retract into the shell"
   "One layer is composed of flattened bone plates that grow between and fuse with the ribs as the turtle grows."   "The bony shell of a sea
   turtle can actually sense when something touches it."   "A series of thin nerves run along the shell and detect pressure changes associated with touch."
 [LS] Live Science, Turtle Facts: "A turtle's shell is a modified ribcage and part of its vertebral column,"   "Scutes are made of keratin, the same
   material that makes up humans' fingernails."   "Sea turtles have lost the ability to retract their heads."   "Many turtles are able to retract
   their heads and feet into their shells."
 [ORP] Olive Ridley Project, Facts about sea turtles: "Sea turtle shells consist of bones, which are covered by a layer of so-called scutes (plates)."
   "These scutes are made of keratin, the same material that human fingernails are made of."   "Yes, sea turtles can feel it when you touch their
   shell."   "No, sea turtles cannot retract their heads into their shells."   "there is simply not enough space in the shell to fully retract the head."
 [SR] The Spokesman-Review, Ask Dr. Universe "Why can't sea turtles pull back into their shell?": "a lot of turtles and tortoises on land have the
   ability to pull, or retract, their head into their body"   "sea turtles just don't have as much space inside their bodies to retract their limbs and heads."
 Said as: a turtle cannot leave its shell [SDZ, DRU]; the shell is part of its body [DRU]; it is made of bones [SDZ, ORP, PBS]; it is joined to its
 backbone [SDZ, PBS, LS] and its ribs [SDZ, PBS, SI]; the shell grows as the turtle grows, like your bones [DRU, SI]; its plates are called scutes [SDZ,
 PBS, DRU, ORP]; they are made of the same stuff as your fingernails (keratin, not named) [SDZ, LS, ORP]; a sea turtle's head always stays outside its
 shell [PBS, ORP, LS]; its flippers stay outside too [SI]; many turtles on land can pull their heads in [LS, SR, PBS]; a sea turtle has no room in its
 shell for its head [ORP, SR]; it can feel a touch on its shell [SI, ORP, DRU]; the shell has nerves [SI, DRU]; you can feel a touch on your fingernail
 too [SDZ]. Tula is a green sea turtle (the leatherback, the exception in PBS, is not named).
 Read but NOT said: the number of bones (the pages give 50, 59-61, about 60), keratin by name, collarbone and hips, "pain".
 Kid safety: the copy-me moves are feeling your ribs, touching your back, stretching tall, looking at and gently tapping your fingernails, pulling
 your head in and popping it out. Milo knocks and taps gently on his friend's shell, and Tula smiles; nobody is hurt, lost, crying or trapped, and
 the shell is shown as Tula's own cosy, strong body, never as something she is stuck in.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_za_ep12 as A12     # Tula's PT/BOX, the sea places
import art_za_ep13            # the "kelp" place
import art_zc_ep16 as A16     # bubbles
import art_zc_ep17 as A
from kit import Kit, S, prop, W
from intro import INTRO_STAGES, intro_shots, SUBSCRIBE_LINE

EP = {"id": "zc_ep17", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "Can a Turtle Leave Its Shell?", "thumb_text": "A DOOR?!", "series": "Animal Facts with Milo",
      "description": ("Can a turtle leave its shell? Milo the bluebird knocks on Tula the green sea turtle's shell and finds her three shell secrets! "
                      "A gentle animal lesson for ages 2-6 with questions to answer, things to feel, moves to copy and a quiz at the end.\n"
                      "Kids learn that a turtle cannot leave its shell, because the shell is part of its body: it is made of bones and joined to its backbone "
                      "and ribs; that the shell grows as the turtle grows, and its plates, called scutes, are made of the same stuff as your fingernails; and "
                      "that a sea turtle cannot pull its head into its shell, like many land turtles can, but it can feel a gentle touch on its shell.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (turtle and tortoise); Ask Dr. Universe, Washington State University (how turtles "
                      "get their shells); PBS Nature (turtle anatomy); Smithsonian Ocean (sea turtles); Live Science (turtle facts); Olive Ridley Project "
                      "(facts about sea turtles); The Spokesman-Review, Ask Dr. Universe (why sea turtles can not pull back into their shell)."),
      "tags": ["can a turtle leave its shell", "turtle shell facts for kids", "sea turtle", "ocean animals for kids", "green sea turtle", "turtle shell",
               "animal facts for kids", "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "reef": [("tur", "turtle", 900, 700, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
    "ocean": [("tur", "turtle", 900, 760, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
    "kelp": [("tur", "turtle", 900, 780, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
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
def HEADUP(at, deg=-16, who="tur"): return ("to", at, f"#{{p}}{who}-neck", {"rotation": deg, "svgOrigin": "180 -170", "duration": .35, "ease": "back.out(2)"}, "Tula lifts her head")
def SHOW(at, sel, what="it shows"): return ("to", at, sel, {"opacity": 1, "duration": .2}, what)
def HIDE(at, sel, what="it goes"): return ("to", at, sel, {"opacity": 0, "duration": .2}, what)
def BUBBLES(at, name): return ("fromto", at, f"#{{p}}{name}-b0,#{{p}}{name}-b1,#{{p}}{name}-b2,#{{p}}{name}-b3,#{{p}}{name}-b4,#{{p}}{name}-b5", {"y": 60, "opacity": 0},
                               {"y": -80, "opacity": 1, "duration": .9, "stagger": .15, "ease": "sine.out"}, "bubbles rise")


# ------------------------------------------------------------------ props and cameras
TX, TY = P("reef", "tur", "feet")                 # Tula's feet on the reef
DOOR = lambda hid=True: prop("dr", A.door, TX - 30, TY - 160, 1.0, hid, p=(TX - 30, TY - 160, 1.0))
BUB = lambda name="bu", x=None, y=None, s=1.0: prop(name, A16.bubble_col, x or P("reef", "tur", "head")[0] + 70, y or P("reef", "tur", "head")[1] - 40, s,
                                                    p=(x or P("reef", "tur", "head")[0] + 70, y or P("reef", "tur", "head")[1] - 40, s))
TAP = lambda hid=True: prop("tp", A.tap_lines, TX - 40, TY - 330, 1.0, hid, p=(TX - 40, TY - 330, 1.0))
RB = C("reef", "tur", "all", 1300, 40, -40); RBP = WV("reef", ["tur"], floor=.7, top=.46, pad=.3)
RH = C("reef", "tur", "head", 760, -60, 0); RHP = V("reef", "tur", "head", 1400, -160, 40)
RS = C("reef", "tur", "top", 1100, 60, 120); RSP = V("reef", "tur", "top", 1300, 0, 160)       # close on the shell
OB = C("ocean", "tur", "all", 1300, 40, -40); OBP = WV("ocean", ["tur"], floor=.7, top=.46, pad=.3)
KB = C("kelp", "tur", "all", 1500, 80, -100); KBP = WV("kelp", ["tur"], floor=.72, top=.46, pad=.3)
MK = {"milo": (TX - 250, TY - 300, .72, False, True)}                 # Milo flies close to Tula's shell (to knock or tap)
DUO = (TX - 60, TY - 240, 1400); DUOP = (TX - 60, TY - 200, 1900)
XR = lambda x=960, s=1.0, p=(960, 700, .8): prop("xr", A.xray_turtle, x, 640, s, p=p)
COAT = lambda x=1360, hid=False, p=(960, 560, .9): prop("co", A.coat, x, 560, 1.0, hid, p=p)
NS = lambda: prop("ns", A.nail_scute, 960, 600, 1.0, p=(960, 640, .78))
LT = lambda x=960, s=1.2, p=(920, 780, .95): prop("lt", A.land_turtle, x, 800, s, p=p)
GA = lambda: prop("ga", A.grow_arrow, 820, 430, 1.0, p=(820, 470, .9))
GROW_ACT = [("tb", "turtle", 560, 760, .5), ("tur", "turtle", 1160, 820, 1.0)]
def RIBS(at): return PULSE(at, "#{p}xr-ribs", 1.04, 2)
def SPINE(at): return PULSE(at, "#{p}xr-spine", 1.04, 2)
def HEADIN(at): return ("to", at, "#{p}lt-head", {"x": -170, "duration": .5, "ease": "power2.inOut"}, "the land turtle pulls its head into its shell")
def HEADOUT(at): return ("to", at, "#{p}lt-head", {"x": 0, "duration": .5, "ease": "back.out(1.6)"}, "its head pops out again")

SHOTS = [
    # ---------------------------------------------------------------- HOOK (cold open on the promise: Milo knocks on Tula's shell, a door doodled on it)
    S("reef", DUO, "Knock, knock! Tula, can you come out of your shell?", q=True, tag="hook: knock knock", pcam=DUOP, cam2=W(DUO, 1.05), move=MK,
      props=[DOOR(False)], fx=[("hop", "w:Knock,:1", "milo"), ("hop", "w:knock!", "milo"), PULSE("w:come", "#{p}dr-q", 1.2, 2), ("lookat", "w:Tula,", "tur", -6)],
      words=[("w:Knock,:1", "KNOCK, KNOCK!", .5, .12, 1.0, "sun", (.5, .3), .8)]),
    S("reef", RB, "Can a turtle ever leave its shell?", q=True, tag="hook: leave its shell?", hide=["milo"], pcam=RBP, cam2=W(RB, 1.06), props=[DOOR(False)],
      fx=[PULSE("w:leave", "#{p}dr", 1.1, 2, "50% 100%"), ("lookat", "e:shell?", "tur", 6)], words=[("e:shell?", "?", .82, .2, 2.0, "sun", (.8, .32), 1.3)]),
    S("reef", say="I'm Milo the bluebird. Let's find Tula's shell secrets!", q=True, tag="hook: Milo", hide=["tur"], fx=[("hop", "w:secrets!", "milo")],
      words=[("w:secrets!", "SECRETS!", .8, .45, 1.0, "sun", (.5, .33), .9)], **dict(cam=C("reef", "milo", "body", 900), pcam=V("reef", "milo", "body", 1100, 0, -90))),
    *intro_shots(),
    S("ocean", OB, "Tula has three shell secrets. Let's find them, one by one!", q=True, tag="three secrets", trans="iris", hide=["milo"], pcam=OBP, cam2=W(OB, 1.05),
      fx=PADDLE(0, 4) + [("nod", "w:three", "tur")],
      words=[("w:three", "1", .22, .2, 1.1, "sun", (.3, .3), 1.0), ("w:secrets.", "2", .5, .2, 1.1, "sun", (.5, .3), 1.0), ("w:one:1", "3", .78, .2, 1.1, "sun", (.7, .3), 1.0)]),
    # ---------------------------------------------------------------- PART 1: the shell is part of her body (bones, backbone, ribs)
    S("reef", RH, "Shell secret number one! Can Tula take off her shell, like a coat?", part=1, q=True, tag="secret 1", hide=["milo"], pcam=RHP, pcam2=W(RHP, .94), cam2=W(RH, 1.05),
      fx=[("lookat", "w:coat?", "tur", -6)], words=[("w:one!", "1", .62, .12, 1.4, "sun", (.3, .3), 1.2), ("e:coat?", "?", .88, .22, 2.0, "sun", (.75, .36), 1.1)]),
    S("reef", RB, "Yes, she can? Or no, she can't?", part=1, q=True, tag="question 1a", pause=3.2, hide=["milo"], pcam=RBP, pcam2=W(RBP, .9), cam2=W(RB, .92),
      fx=PADDLE("w:Yes,", 3) + [("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("reef", RH, "No! A turtle cannot leave its shell.", part=1, tag="no, it cannot", hide=["milo"], pcam=RHP, cam2=W(RH, .95),
      fx=[("nod", "w:cannot", "tur")], words=[("w:No!", "NO!", .2, .26, 1.4, "sun", (.5, .3), 1.1)]),
    S("reef", RB, "Not ever! A turtle and its shell always stay together.", part=1, tag="always together", hide=["milo"], pcam=RBP, cam2=W(RB, 1.05),
      fx=PADDLE("w:together.", 3) + [("nod", "w:always", "tur")], words=[("w:together.", "TOGETHER!", .26, .2, 1.0, "sun", (.5, .3), .85)]),
    S("paper", (1000, 560, 1700), "A coat comes off. But a shell is part of the turtle's body!", part=1, tag="board: not a coat", pcam=(1100, 600, 1900), props=[COAT(400, p=(1100, 470, .6)), XR(1150, .85, (1100, 870, .8))],
      fx=[PULSE("w:coat", "#{p}co-c", 1.06, 1), SHOW("w:shell", "#{p}co-x", "a red cross on the coat"), PULSE("w:body!", "#{p}xr-shell", 1.03, 1)],
      words=[("w:body!", "PART OF IT!", .62, .1, 1.0, "sun", (.5, .26), .8)]),
    S("paper_blue", (960, 560, 1500), "Look inside! A turtle's shell is made of bones.", part=1, tag="board: bones", pcam=(960, 660, 1700), cam2=(960, 540, 1300), props=[XR()],
      fx=[PULSE("w:inside!", "#{p}xr-shell", 1.03, 1), SPINE("w:bones."), RIBS("w:bones.")], words=[("w:bones.", "BONES!", .5, .14, 1.1, "sun", (.5, .3), 1.0)]),
    S("paper", (1060, 500, 1400), "This is her backbone. It is joined to her shell.", part=1, tag="board: backbone", pcam=(1000, 640, 1750), cam2=(1060, 480, 1300), props=[XR()],
      fx=[SPINE("w:backbone."), PULSE("w:joined", "#{p}xr-spine", 1.04, 1)], words=[("w:backbone.", "BACKBONE!", .5, .13, 1.0, "sun", (.5, .3), .85)]),
    S("paper_blue", (1000, 580, 1250), "And these are her ribs. They are joined to her shell, too!", part=1, tag="board: ribs", pcam=(1000, 660, 1750), cam2=(1000, 560, 1150), props=[XR()],
      fx=[RIBS("w:ribs."), PULSE("w:joined", "#{p}xr-ribs", 1.04, 1)], words=[("w:ribs.", "RIBS!", .5, .13, 1.1, "sun", (.5, .3), 1.0)]),
    S("paper", (960, 560, 1800), "Wow! Her shell is joined to her bones.", part=1, tag="board: wow joined", pcam=(960, 640, 1800), props=[XR()],
      fx=[PULSE("w:Wow!", "#{p}xr", 1.04, 1), SPINE("w:joined"), RIBS("w:bones.")], words=[("w:Wow!", "WOW!", .5, .1, 1.3, "sun", (.5, .3), 1.0)]),
    S("paper_pink", (960, 580, 1650), "Backbone, ribs, and shell. All joined together!", part=1, tag="board: all joined", pcam=(960, 660, 1750), props=[XR()],
      fx=[SPINE("w:Backbone,"), RIBS("w:ribs,"), PULSE("w:shell.", "#{p}xr-shell", 1.03, 1), PULSE("w:together!", "#{p}xr", 1.04, 1)],
      words=[("w:together!", "ALL JOINED!", .5, .1, 1.0, "sun", (.5, .26), .85)]),
    S("zoo", say="You have ribs, too! Put your hands on your sides, and feel your ribs.", part=1, q=True, tag="feel your ribs", pause=3.0, fx=[("hop", "w:ribs,", "milo"), ("hop", "w:feel", "milo")],
      words=[("w:feel", "RIBS!", .82, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("zoo", say="Now touch your back. Your backbone is in there!", part=1, q=True, tag="touch your back", pause=2.4, fx=[("hop", "w:back.", "milo"), ("hop", "w:there!", "milo")],
      words=[("w:backbone", "BACKBONE!", .8, .3, .85, "sun", (.5, .33), .75)], **MILO("zoo", 1300)),
    S("reef", RH, "So, can Tula come out of her shell?", part=1, q=True, tag="can she come out", pause=3.0, hide=["milo"], pcam=RHP, cam2=W(RH, 1.06),
      fx=[("lookat", "w:out", "tur", -6)], words=[("e:shell?", "?", .85, .2, 2.0, "sun", (.8, .3), 1.1)]),
    S("reef", RB, "No! Her shell is a part of her. It goes everywhere with her.", part=1, tag="part of her", hide=["milo"], pcam=RBP, cam2=W(RB, 1.05),
      fx=PADDLE("w:everywhere", 3) + [("nod", "w:part", "tur")], words=[("w:part", "PART OF HER!", .26, .2, 1.0, "sun", (.5, .3), .8)]),
    S("reef", DUO, "So, Milo, there is no door in Tula's shell. Her shell is Tula!", part=1, tag="no door", pcam=DUOP, cam2=W(DUO, 1.05), move=MK, props=[DOOR(False)],
      fx=[HIDE("w:door", "#{p}dr", "the doodled door goes away"), ("hop", "w:Milo,", "milo"), ("nod", "w:Tula!", "tur"), ("lookat", "w:Milo,", "tur", -8)],
      words=[("w:door", "NO DOOR!", .64, .12, 1.1, "sun", (.5, .3), .9)]),
    S("reef", RS, "Say it with me. A turtle's shell is part of its body!", part=1, q=True, tag="say it: part of its body", hide=["milo"], pcam=RSP, cam2=W(RS, 1.06),
      fx=[("nod", "w:body!", "tur")], words=[("w:Say", "SAY IT!", .5, .12, 1.1, "sun", (.5, .3), .9)]),
    S("ocean", OB, "Quick check! Is Tula's shell made of bones? Yes, or no?", part=1, q=True, tag="question 1b", pause=3.2, hide=["milo"], pcam=OBP, pcam2=W(OBP, .88), cam2=W(OB, .9),
      fx=PADDLE("w:bones?", 3) + [("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("reef", RH, "Yes, bones! Great job!", part=1, tag="great job 1", hide=["milo"], pcam=RHP, cam2=W(RH), fx=[("nod", "w:Great", "tur")],
      words=[("w:Great", "GREAT!", .2, .26, 1.3, "sun", (.5, .3), 1.0)]),
    # ---------------------------------------------------------------- PART 2: the shell grows with her; scutes, like your fingernails
    S("ocean", OB, "Shell secret number two! When a little turtle grows bigger, what happens to its shell?", part=2, q=True, tag="secret 2", trans="iris", hide=["milo"], pcam=OBP, pcam2=W(OBP, .94), cam2=W(OB, 1.05),
      move={"tur": (700, 760, 1.0)}, props=[BUB("b2", 1460, 600, 1.0)], fx=PADDLE(0, 8) + [("walk", "w:Shell", "tur", 260, 3.0), BUBBLES("w:grows", "b2"), ("lookat", "w:what", "tur", -8)],
      words=[("w:two!", "2", .2, .2, 1.4, "sun", (.3, .3), 1.2), ("e:shell?", "?", .8, .2, 2.0, "sun", (.7, .34), 1.3)]),
    S("kelp", KB, "Does it get a new shell? Or does its shell grow, too?", part=2, q=True, tag="question 2a", pause=3.2, hide=["milo"], pcam=KBP, pcam2=W(KBP, .92), cam2=W(KB, .86),
      fx=PADDLE("w:new", 3) + [("signs", "w:new", ["NEW ONE", "GROWS"], 1, "wait:2.0")]),
    S("paper_blue", (900, 560, 1700), "Its shell grows! As a turtle grows, its shell grows with it.", part=2, tag="board: it grows", pcam=(880, 640, 2400), cam2=(900, 540, 1550),
      actors=GROW_ACT, props=[GA()], fx=[PULSE("w:grows!", "#{p}ga", 1.15, 2), ("nod", "w:with", "tur"), ("nod", "w:As", "tb")],
      words=[("w:grows!", "IT GROWS!", .5, .1, 1.1, "sun", (.5, .26), .9)]),
    S("paper_blue", (1000, 600, 1500), "Just like your bones grow, when you grow!", part=2, tag="board: like your bones", pcam=(880, 640, 2400), cam2=(1000, 580, 1450),
      actors=GROW_ACT, props=[GA()], fx=[("nod", "w:bones", "tur"), ("nod", "w:grow!", "tur")], words=[("w:bones", "LIKE YOU!", .5, .1, 1.1, "sun", (.5, .26), .9)]),
    S("paper_blue", (900, 600, 1800), "A baby turtle has a little shell. A big turtle has a big shell!", part=2, tag="board: little and big", pcam=(880, 660, 2400),
      actors=GROW_ACT, props=[GA()], fx=[("nod", "w:little", "tb"), PULSE("w:little", "#{p}tb-shell", 1.1, 1, "50% 100%"), ("nod", "w:big:2", "tur"), PULSE("w:big:2", "#{p}tur-shell", 1.06, 1, "50% 100%")],
      words=[("w:little", "LITTLE", .22, .14, 1.0, "sun", (.3, .26), .8), ("w:big:2", "BIG!", .7, .14, 1.2, "sun", (.7, .26), 1.0)]),
    S("zoo", say="You are growing, too! Stretch up nice and tall. So tall!", part=2, q=True, tag="stretch up tall", pause=2.4, fx=[("hop", "w:tall.", "milo"), ("hop", "w:So", "milo"), ("hop", "wait:1.0", "milo")],
      words=[("w:tall.", "SO TALL!", .82, .3, .95, "sun", (.5, .33), .85)], **MILO("zoo", 1300)),
    S("reef", RS, "Look at the top of Tula's shell. Can you see the little plates?", part=2, q=True, tag="see the plates", pause=1.2, hide=["milo"], pcam=RSP, cam2=W(RS, .94),
      fx=[PULSE("w:plates?", "#{p}tur-shell", 1.04, 2, "50% 100%")], words=[("w:plates?", "PLATES!", .5, .12, 1.1, "sun", (.5, .3), 1.0)]),
    S("reef", W(RS, 1.1), "Let's count three plates. One, two, three!", part=2, q=True, tag="count the plates", hide=["milo"], pcam=W(RSP, 1.05), cam2=W(RS, 1.04),
      fx=[PULSE("w:One,", "#{p}tur-shell", 1.03, 1, "50% 100%"), PULSE("w:two,", "#{p}tur-shell", 1.03, 1, "50% 100%"), PULSE("w:three!", "#{p}tur-shell", 1.03, 1, "50% 100%")],
      words=[("w:One,", "1", .33, .34, 1.2, "sun", (.3, .5), 1.0), ("w:two,", "2", .5, .26, 1.2, "sun", (.5, .44), 1.0), ("w:three!", "3", .67, .34, 1.2, "sun", (.7, .5), 1.0)]),
    S("reef", RH, "These plates are called scutes. Say it: scutes!", part=2, q=True, tag="scutes", hide=["milo"], pcam=RHP, cam2=W(RH, 1.06),
      fx=[("nod", "w:scutes.", "tur"), ("nod", "w:scutes!", "tur")], words=[("w:scutes.", "SCUTES!", .2, .26, 1.2, "sun", (.5, .3), 1.0)]),
    S("reef", RB, "The scutes cover her shell, and help to protect her.", part=2, tag="scutes protect", hide=["milo"], pcam=RBP, cam2=W(RB, 1.05),
      fx=PADDLE("w:protect", 3) + [PULSE("w:cover", "#{p}tur-shell", 1.04, 1, "50% 100%")], words=[("w:protect", "STRONG!", .26, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper", (960, 560, 1600), "Scutes are made of the same stuff as your fingernails!", part=2, tag="board: like fingernails", pcam=(960, 640, 1700), cam2=(960, 540, 1450), props=[NS()],
      fx=[PULSE("w:Scutes", "#{p}ns-scute", 1.08, 1), PULSE("w:fingernails!", "#{p}ns-nail", 1.12, 2)], words=[("w:fingernails!", "FINGERNAILS!", .5, .1, .95, "sun", (.5, .26), .75)]),
    S("zoo", say="Look at your fingernails. Can you tap them? Tap, tap!", part=2, q=True, tag="tap your nails", pause=2.4, fx=[("hop", "w:Tap,", "milo"), ("hop", "w:tap!", "milo"), ("hop", "wait:1.0", "milo")],
      words=[("w:Tap,", "TAP, TAP!", .82, .3, .95, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("paper_blue", (960, 600, 1800), "Your fingernails, and Tula's scutes. The same stuff!", part=2, tag="board: the same", pcam=(960, 660, 1800), props=[NS()],
      fx=[PULSE("w:fingernails,", "#{p}ns-nail", 1.12, 1), PULSE("w:scutes.", "#{p}ns-scute", 1.08, 1)], words=[("w:same", "THE SAME!", .5, .12, 1.1, "sun", (.5, .26), .9)]),
    S("ocean", OB, "Tula swims, and grows, and grows. And her shell grows with her!", part=2, tag="shell grows with her", hide=["milo"], pcam=OBP, cam2=W(OB, 1.08),
      fx=PADDLE(0, 7) + [("nod", "w:shell", "tur")], words=[("w:grows,:2", "GROWS!", .26, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("kelp", KB, "Look how big Tula is now. And her shell is big, too!", part=2, tag="big tula", hide=["milo"], pcam=KBP, cam2=W(KB, 1.05),
      fx=PADDLE(0, 4) + [PULSE("w:big:2", "#{p}tur-shell", 1.05, 1, "50% 100%"), ("nod", "w:too!", "tur")], words=[("w:big:2", "BIG!", .26, .2, 1.3, "sun", (.5, .3), 1.0)]),
    S("reef", RB, "Say it with me. A turtle's shell grows with it!", part=2, q=True, tag="say it: grows with it", hide=["milo"], pcam=RBP, cam2=W(RB),
      fx=[("nod", "w:grows", "tur")], words=[("w:Say", "SAY IT!", .26, .2, 1.1, "sun", (.5, .3), .9)]),
    S("kelp", KB, "Quick check! When Tula grows, does her shell grow, too? Yes, or no?", part=2, q=True, tag="question 2b", pause=3.2, hide=["milo"], pcam=KBP, pcam2=W(KBP, .9), cam2=W(KB, .88),
      fx=PADDLE("w:grows,", 3) + [("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("reef", RH, "Yes! Super!", part=2, tag="super", hide=["milo"], pcam=RHP, cam2=W(RH), fx=[("nod", "w:Super!", "tur")],
      words=[("w:Super!", "SUPER!", .2, .26, 1.3, "sun", (.5, .3), 1.0)]),
    # ---------------------------------------------------------------- PART 3: a sea turtle's head stays out; the shell can feel a touch
    S("reef", RB, "Shell secret number three! Can a sea turtle hide its head inside its shell?", part=3, q=True, tag="secret 3", trans="iris", hide=["milo"], pcam=RBP, pcam2=W(RBP, .94), cam2=W(RB, 1.05),
      fx=[("lookat", "w:head", "tur", 6)], words=[("w:three!", "3", .2, .2, 1.4, "sun", (.3, .3), 1.2), ("e:shell?", "?", .8, .2, 2.0, "sun", (.7, .34), 1.3)]),
    S("ocean", OB, "Yes, it can? Or no, it can't?", part=3, q=True, tag="question 3a", pause=3.2, hide=["milo"], pcam=OBP, pcam2=W(OBP, .9), cam2=W(OB, .9),
      fx=PADDLE("w:Yes,", 3) + [("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("reef", RH, "No! A sea turtle's head always stays outside its shell.", part=3, tag="head stays out", hide=["milo"], pcam=RHP, cam2=W(RH, .95),
      fx=[HEADUP("w:head", -10), HEADUP("w:outside", 0)], words=[("w:outside", "STAYS OUT!", .45, .12, 1.1, "sun", (.5, .3), .85)]),
    S("reef", RS, "Hello, Tula! Your head is always out!", part=3, tag="hello tula", hide=["milo"], pcam=RSP, cam2=W(RS, 1.06),
      fx=[HEADUP("w:Hello,", -12), HEADUP("w:always", 0), ("nod", "w:out!", "tur")], words=[("w:Hello,", "HELLO!", .5, .12, 1.2, "sun", (.5, .3), 1.0)]),
    S("ocean", OB, "Her flippers stay outside, too. Paddle, paddle!", part=3, tag="flippers stay out", hide=["milo"], pcam=OBP, cam2=W(OB, 1.06),
      fx=PADDLE("w:flippers", 6), words=[("w:Paddle,", "FLIPPERS!", .26, .2, 1.0, "sun", (.5, .3), .85)]),
    S("paper_pink", (960, 600, 1500), "Many turtles that live on land can pull their heads in. Look! In it goes.", part=3, tag="board: land turtle head in", pcam=(960, 640, 1500), cam2=(960, 600, 1300), props=[LT()],
      fx=[HEADIN("w:In"), ("to", "w:Look!", "#{p}lt", {"y": -12, "duration": .2, "yoyo": True, "repeat": 1}, "the land turtle wiggles")], words=[("w:In", "IN!", .78, .16, 1.3, "sun", (.75, .3), 1.0)]),
    S("paper_pink", (960, 620, 1350), "And out it comes again! Hello!", part=3, tag="board: land turtle head out", pcam=(960, 660, 1350), cam2=(960, 620, 1250), props=[LT()],
      fx=[HEADIN(0.01), HEADOUT("w:out"), ("to", "w:Hello!", "#{p}lt", {"y": -14, "duration": .2, "yoyo": True, "repeat": 1}, "the land turtle wiggles")],
      words=[("w:out", "OUT!", .78, .16, 1.3, "sun", (.75, .3), 1.0)]),
    S("paper_pink", (1000, 560, 1800), "But a sea turtle has no room in its shell for its head.", part=3, tag="board: no room", pcam=(980, 640, 2500), props=[LT(620, 1.0, (620, 760, .8))],
      actors=[("tur", "turtle", 1330, 830, .9)], fx=[HEADOUT(0.2), ("nod", "w:sea", "tur"), PULSE("w:room", "#{p}tur-shell", 1.05, 2, "50% 100%")],
      words=[("w:room", "NO ROOM!", .72, .12, 1.1, "sun", (.5, .26), .9)]),
    S("zoo", say="Can you pull your head in, like a land turtle? Now pop it out!", part=3, q=True, tag="pull your head in", pause=2.4, fx=[("hop", "w:in,", "milo"), ("hop", "w:out!", "milo"), ("hop", "wait:1.0", "milo")],
      words=[("w:in,", "IN!", .82, .3, 1.0, "sun", (.5, .33), .9), ("w:out!", "OUT!", .82, .45, 1.0, "sun", (.5, .42), .9)], **MILO("zoo", 1300)),
    S("reef", RH, "And one more thing. Can Tula feel a gentle tap on her shell?", part=3, q=True, tag="can she feel a tap", pause=3.0, hide=["milo"], pcam=RHP, cam2=W(RH, 1.06),
      fx=[("lookat", "w:feel", "tur", -6)], words=[("e:shell?", "?", .85, .2, 2.0, "sun", (.8, .3), 1.1)]),
    S("reef", DUO, "Yes! Milo gives Tula a gentle tap. She can feel it!", part=3, tag="milo taps gently", pcam=DUOP, cam2=W(DUO, 1.05), move=MK, props=[TAP()],
      fx=[("hop", "w:tap.", "milo"), ("show", "w:tap.", "tp"), PULSE("w:feel", "#{p}tp", 1.2, 2), ("nod", "w:feel", "tur"), ("lookat", "w:Milo", "tur", -8)],
      words=[("w:feel", "SHE FEELS IT!", .7, .16, 1.0, "sun", (.5, .3), .8)]),
    S("paper", (960, 580, 1750), "Her shell has little nerves. So she can feel a touch.", part=3, tag="board: nerves", pcam=(960, 680, 1800), cam2=(960, 560, 1600), props=[XR()],
      fx=[SHOW("w:nerves.", "#{p}xr-nerves", "the nerves light up"), PULSE("w:touch.", "#{p}xr-nerves", 1.03, 2)], words=[("w:feel", "FEEL!", .5, .1, 1.2, "sun", (.5, .3), 1.0)]),
    S("paper", (960, 600, 1600), "You feel a tap on your fingernail. Tula feels a tap on her shell!", part=3, tag="board: feel a tap", pcam=(960, 640, 1700), props=[NS()],
      fx=[PULSE("w:fingernail.", "#{p}ns-nail", 1.12, 1), PULSE("w:shell!", "#{p}ns-scute", 1.08, 1)], words=[("w:feels", "TAP!", .5, .1, 1.3, "sun", (.5, .26), 1.0)]),
    S("zoo", say="Gently tap your fingernail. You can feel it, too!", part=3, q=True, tag="feel your nail", pause=2.4, fx=[("hop", "w:tap", "milo"), ("hop", "w:too!", "milo"), ("hop", "wait:1.0", "milo")],
      words=[("w:tap", "TAP!", .82, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("reef", RB, "Say it with me. A sea turtle's head stays out!", part=3, q=True, tag="say it: head stays out", hide=["milo"], pcam=RBP, cam2=W(RB),
      fx=[HEADUP("w:head", -10), ("nod", "w:out!", "tur")], words=[("w:Say", "SAY IT!", .26, .2, 1.1, "sun", (.5, .3), .9)]),
    S("ocean", OB, "Quick check! Can Tula feel a gentle tap on her shell? Yes, or no?", part=3, q=True, tag="question 3b", pause=3.2, hide=["milo"], pcam=OBP, pcam2=W(OBP, .88), cam2=W(OB, .88),
      fx=PADDLE("w:feel", 3) + [("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("reef", RB, "Yes! You remembered!", part=3, tag="you remembered", hide=["milo"], pcam=RBP, cam2=W(RB), fx=[("nod", "w:remembered!", "tur")],
      words=[("w:Yes!", "YES!", .26, .2, 1.3, "sun", (.5, .3), 1.0)]),
    # ---------------------------------------------------------------- QUIZ
    S("zoo_eve", WIDE, "Three shell secrets! Now it is quiz time!", part=4, trans="iris", tag="quiz time", cam2=(960, 560, 1860), pcam=(960, 560, 1800),
      words=[("w:quiz", "QUIZ TIME!", .5, .3, 1.3, "sun", (.5, .33))], fx=[("hop", "w:quiz", "milo", 2)]),
    S("reef", RB, "Can a turtle take off its shell? Yes, or no?", part=4, q=True, tag="quiz 1", pause=3.2, hide=["milo"], pcam=RBP, cam2=W(RB, .92),
      fx=PADDLE("w:shell?", 3) + [("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("paper_blue", (960, 560, 1600), "No! It is joined to her bones.", part=4, tag="quiz 1: joined", pcam=(960, 660, 1700), props=[XR()], fx=[SPINE("w:joined"), RIBS("w:bones.")],
      words=[("w:No!", "NO!", .5, .1, 1.3, "sun", (.5, .3), 1.0)]),
    S("kelp", KB, "When a turtle grows, does its shell grow, too? Yes, or no?", part=4, q=True, tag="quiz 2", pause=3.2, hide=["milo"], pcam=KBP, pcam2=W(KBP, .88), cam2=W(KB, .86),
      fx=PADDLE("w:grows,", 3) + [("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("paper", (900, 560, 1700), "Yes! It grows with her.", part=4, tag="quiz 2: grows", pcam=(880, 640, 2400), actors=GROW_ACT, props=[GA()],
      fx=[PULSE("w:grows", "#{p}ga", 1.15, 2), ("nod", "w:Yes!", "tur")], words=[("w:Yes!", "YES!", .5, .1, 1.3, "sun", (.5, .26), 1.0)]),
    S("ocean", OB, "Can a sea turtle pull its head into its shell? Yes, or no?", part=4, q=True, tag="quiz 3", pause=3.2, hide=["milo"], pcam=OBP, pcam2=W(OBP, .88), cam2=W(OB, .86),
      fx=PADDLE("w:pull", 3) + [("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("reef", RH, "No! Her head stays out.", part=4, tag="quiz 3: stays out", hide=["milo"], pcam=RHP, cam2=W(RH), fx=[HEADUP("w:head", -10)],
      words=[("w:No!", "NO!", .2, .26, 1.3, "sun", (.5, .3), 1.0)]),
    # ---------------------------------------------------------------- RECAP + GOODBYE + LIKE AND SUBSCRIBE
    S("reef", (960, 560, 1900), "Tula's shell is part of her, it grows with her, and her head stays out. You found all three secrets!", part=4, trans="iris",
      tag="recap", hide=[], pcam=(940, 560, 2300), cam2=(960, 560, 1960), move={"milo": (380, 360, .7, False, True)},
      fx=[("nod", "w:part", "tur"), ("hop", "w:grows", "milo"), HEADUP("w:head", -10), ("hop", "w:three", "milo")],
      words=[("w:part", "1", .3, .14, 1.1, "sun", (.3, .28), 1.0), ("w:grows", "2", .5, .14, 1.1, "sun", (.5, .28), 1.0), ("w:head", "3", .7, .14, 1.1, "sun", (.7, .28), 1.0)]),
    S("zoo_eve", say="Feel your ribs. Tap your fingernails. And pull your head in, then pop it out!", part=4, q=True, tag="all three moves", pause=1.6,
      fx=[("hop", "w:Feel", "milo"), ("hop", "w:Tap", "milo"), ("hop", "w:pop", "milo")],
      words=[("w:pop", "POP!", .84, .3, .9, "sun", (.5, .33), .8)], **MILO("zoo_eve", 940)),
    S("paper_blue", (960, 540, 1500), "Next time: what do sea turtles eat? Have a happy swim, Tula!", part=4, tag="next: what do they eat", pcam=(960, 440, 1700),
      actors=[("tur", "turtle", 900, 760, 1.1)], fx=[("nod", "w:eat?", "tur"), ("nod", "w:swim,", "tur")] + PADDLE("w:happy", 4),
      words=[("w:eat?", "NEXT TIME!", .5, .12, 1.1, "sun", (.5, .3), .9)]),
    S("zoo_eve", say=SUBSCRIBE_LINE, part=4, tag="goodbye: like and subscribe", fx=[("hop", "w:Thank", "milo"), ("hop", "w:subscribe,", "milo")],
      words=[("w:Thank", "THANK YOU!", .8, .18, .9, "sun", (.5, .33), .8)], **MILO("zoo_eve", 940)),
    *intro_shots(),      # the main intro again as the last shots (owner, Nov 20 4:50 PM: at the beginning and at the end of every new long video)
]
for _s in SHOTS:        # a picture board never drifts closer: it only pulls out a little (16:9 and 9:16)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)

SHORTS = [
    {"id": "zc_ep17_short1", "title": "Can a Turtle Come Out of Its Shell?", "band": ("COME OUT OF", "ITS SHELL?"), "thumb_text": "BONES!", "part": 1,
     "extra_first": [S("reef", RB, "Can a turtle come out of its shell?", part=1, q=True, tag="hook: come out?", hide=["milo"], pcam=(RBP[0], RBP[1], round(RBP[2] * .8)), pcam2=(RBP[0], RBP[1], round(RBP[2] * .86)), cam2=W(RB, 1.05),
                       props=[DOOR(False)], fx=[PULSE("w:come", "#{p}dr-q", 1.2, 2)], words=[("e:shell?", "?", .82, .2, 2.0, "sun", (.75, .36), 1.1)])]},
    {"id": "zc_ep17_short2", "title": "Does a Turtle's Shell Grow?", "band": ("DOES IT", "GROW?"), "thumb_text": "LIKE NAILS!", "part": 2,
     "extra_first": [S("reef", RS, "Does a turtle's shell grow?", part=2, q=True, tag="hook: does it grow?", hide=["milo"], pcam=(RSP[0], RSP[1], round(RSP[2] * .9)), pcam2=(RSP[0], RSP[1], RSP[2]), cam2=W(RS, 1.05),
                       fx=[PULSE("w:grow?", "#{p}tur-shell", 1.05, 2, "50% 100%")], words=[("w:grow?", "?", .8, .2, 2.0, "sun", (.75, .36), 1.1)])]},
    {"id": "zc_ep17_short3", "title": "Can a Sea Turtle Hide Its Head?", "band": ("HIDE ITS", "HEAD?"), "thumb_text": "STAYS OUT!", "part": 3,
     "extra_first": [S("reef", RH, "Can a sea turtle hide its head?", part=3, q=True, tag="hook: hide its head?", hide=["milo"], pcam=(RHP[0] - 60, RHP[1], 1000), pcam2=(RHP[0] - 60, RHP[1], 1080), cam2=W(RH, 1.05),
                       fx=[("lookat", "w:hide", "tur", -6)], words=[("e:head?", "?", .2, .3, 2.0, "sun", (.75, .36), 1.1)])]},
]

# thumbnails (thumb.py): one big object, 1-2 words, none of the title's words, no watermark
THUMBS = {
    "zc_ep17": {"place": "reef", "cam": (TX + 40, TY - 230, 1250), "actors": [("turtle", TX, TY, 1.0, False, "")],
                "props": [(A.door, TX - 30, TY - 160, 1.0)], "words": [("A DOOR?!", 470, 150, 150, "sun")]},
    "zc_ep17_short1": {"place": "paper_blue", "cam": (960, 600, 2300), "props": [(A.xray_turtle, 960, 640, 1.1)], "words": [("BONES!", 540, 1520, 210, "sun")]},
    "zc_ep17_short2": {"place": "paper", "cam": (960, 600, 2300), "props": [(A.nail_scute, 960, 640, .9)], "words": [("LIKE", 540, 1420, 200, "sun"), ("NAILS!", 540, 1640, 200, "sun")]},
    "zc_ep17_short3": {"place": "reef", "cam": (TX + 120, TY - 300, 1500), "actors": [("turtle", TX, TY, 1.2, False, "")],
                       "words": [("STAYS", 540, 1450, 190, "sun"), ("OUT!", 540, 1660, 190, "sun")]},
}
