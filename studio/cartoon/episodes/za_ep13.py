"""za_ep13 - Milo's Zoo Adventures: "Can Little Crab Find a Shell That Fits?" (theme title "A New House for Little Crab"; cartoon adventure, the 3D
music-and-sync process: "beat"). Ocean week, adventure 2.
Little Crab, a hermit crab, has grown: his old blue shell is much too small (it feels tight; nobody is hurt). With Tula the sea turtle he looks for a
new house. The first shell is huge (he slides all around inside), the second is shiny but much too heavy to carry, the third looks just right but a
snail lives in it (Little Crab says sorry and leaves it: he needs an EMPTY shell). Low moment: three shells and not one is right; Little Crab sits on
the sand, a little sad (nobody cries, nobody is lost or stuck; he keeps his old shell on the whole time). His own idea: now he knows what he needs
(not too big, not too heavy, and empty), and Tula can dive deep, so she brings shells and he tries them one by one. The white one is too small, the
red one too big, the golden one fits just right. Evening: thank-yous, and a tiny crab moves into the old blue shell. Milo is the storyteller on a
rock above the water (a bird stays in the air: he is never under the water).

FACTS, read at the source on Nov 21 2026, about 3:30 PM ET (each page fetched by the session's page reader, which quoted these sentences verbatim;
it trims a quote at 125 characters, so some are the first part of their sentence):
 [SEA] Seattle Aquarium, "Hermit crab", seattleaquarium.org/animal/hermit-crab/
   "Unlike free-living crabs, their abdomens aren't covered in a hard exoskeleton but rather a thin, soft one"
   "their abdomens are also twisted to fit the spiral cavity of the snail shells in which they make their homes."
   "And, as they grow, they must seek out new shells in which to live."   "As they grow, these creatures look for another empty shell to move into."
 [BRI] Encyclopaedia Britannica, "hermit crab", britannica.com/animal/hermit-crab
   "These crabs use empty snail shells (e.g., whelk or periwinkle) or other hollow objects as a shelter"
   "As the crab grows and becomes too large for its shell, it must find and move into a larger one."   "The soft abdomen is asymmetrical, usually curling to the right."
 [DW] Discover Wildlife (BBC Wildlife), "Hermit crabs: all you need to know...", discoverwildlife.com/animal-facts/hermit-crab-facts
   "but must find a series of bigger homes as it grows."   "These soft-bodied crustaceans are so dependent on their shells for protection"
 Said as animal facts in the film (three fact shots, questions, recap): hermit crabs live in empty snail shells [SEA, BRI]; as a hermit crab grows,
 it must find a bigger shell and move in [BRI, SEA, DW]; the back part of a hermit crab's body is soft, and it fits inside the shell [SEA, BRI].
 NOT said as facts: that a hermit crab cannot grow a shell of its own (no page read today says it in so many words), how it tests a shell (Little
 Crab's "tap, tap, tap" with his claws is THIS story), that a smaller crab takes the old shell (the ending's tiny neighbour is this story), anything
 about snails or sea turtles. The theme's "his shell pinches" became "too small / too tight" (nobody is hurt).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep13 as A
import kit
from kit import Kit, S, prop
from intro import INTRO_STAGES, intro_shots      # the main intro, right after the hook and as the last shots (owner, Nov 20 4:50 PM)

EP = {"id": "za_ep13", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "tula": {"voice": "bf_emma", "speed": .8, "gain": .8},
               "crab": {"voice": "af_nova", "speed": .95, "pitch": 5, "formant": 1.22, "gain": 1.1}},
      "title": "Can Little Crab Find a Shell That Fits?", "thumb_text": "TOO SMALL!",
      "series": "Milo's Zoo Adventures",
      "description": ("Can Little Crab find a shell that fits? He has grown, and his old shell is much too small. One shell is huge, one is too heavy, "
                      "and one already has a snail inside! With his friend Tula the sea turtle, Little Crab keeps trying until one fits just right. "
                      "A gentle ocean adventure for ages 2-6 about trying again and knowing what you need, with questions to answer, a count-along and a little tune.\n"
                      "Kids see how hermit crabs live in empty snail shells, how a growing hermit crab must find a bigger shell and move in, "
                      "and how the soft back part of a hermit crab's body fits inside the shell.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSeattle Aquarium (hermit crab); Encyclopaedia Britannica (hermit crab); Discover Wildlife (hermit crabs)."),
      "tags": ["hermit crab for kids", "hermit crab", "why do hermit crabs change shells", "ocean animals for kids", "under the sea", "sea turtle", "crab story for kids",
               "animal stories for kids", "friendship story for kids", "kids adventure cartoon", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

CS = .55
MILO_S = ("milo", "milo", A.ISLE_TOP[0], A.ISLE_TOP[1], .5)
CR = lambda x, y=900, s=CS, f=False, kind="hermit_small": ("crab", kind, x, y, s, f)
CF = lambda x, y=900, s=CS, f=False: ("crab", "hermit_fit", x, y, s, f)
T = lambda x, y, s=.55, f=False: ("tula", "turtle", x, y, s, f)
STAGES = {
    "shore": [MILO_S, CR(700), T(1120, 700)],
    "shellbed": [CR(1130, f=True), T(1480, 620, .55, True)],
    "rocks": [CR(1130, f=True), T(500, 600)],
    "kelp": [CR(540), T(1480, 640, .55, True)],
    "deep": [T(700, 560)],
    "shore_eve": [MILO_S, CF(820), T(1160, 700)],
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
CCL = lambda place, w=820, dx=0, dy=-40, stage=None: C(place, "crab", "all", w, dx, dy, stage=stage)      # Little Crab whole, close
TCL = lambda place, w=1000, dx=0, dy=-20, stage=None: C(place, "tula", "all", w, dx, dy, stage=stage)     # Tula whole, close
MCLS = (A.ISLE_TOP[0], 170, 800)                                                                           # Milo on his rock, low in the frame

SWIM = lambda at, who, dx, d, ease="sine.inOut": ("to", at, "#{p}%s_w" % who, {"x": "+=%d" % dx, "duration": d, "ease": ease}, who + " moves")
DIVE = lambda at, who, dx, dy, d: ("to", at, "#{p}%s_w" % who, {"x": "+=%d" % dx, "y": "+=%d" % dy, "duration": d, "ease": "sine.inOut"}, who + " swims")
FLAP = lambda at, n=7, d=.45: ("to", at, "#{p}tula-ff", {"rotation": 24, "svgOrigin": "95 -122", "duration": d, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "Tula paddles")
WIG = lambda at, who="crab", n=9, d=.14, a=6: ("to", at, "#{p}%s" % who, {"rotation": a, "transformOrigin": "50% 80%", "duration": d, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, who + " wiggles")
CLAW = lambda at, n=5, who="crab": ("to", at, "#{p}%s-cl" % who, {"rotation": -26, "svgOrigin": "150 -74", "duration": .18, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "Little Crab waves his claw")
TAP = lambda at, n=5: ("to", at, "#{p}crab-cl", {"rotation": 16, "svgOrigin": "150 -74", "duration": .12, "yoyo": True, "repeat": n, "ease": "power1.in"}, "tap, tap")
ROCK = lambda at, name, n=7, a=4, d=.3: ("to", at, "#{p}%s" % name, {"rotation": a, "transformOrigin": "50% 100%", "duration": d, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "the shell wobbles")
BLINK = lambda at, sel, what, n=5: ("to", at, sel, {"opacity": .35, "duration": .2, "yoyo": True, "repeat": n}, what)
FADEIN = lambda at, sel, what: ("fromto", at, sel, {"opacity": 0}, {"opacity": 1, "duration": .3}, what)

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. The rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_HOUSE = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "G4:1 E4:1 C5:2 D5:1 B4:1 G4:1", "rest": 1},      # not too big, and not too small (C bar, G bar)
                                  {"text": "~ ~ ~ ~ ~ ~", "notes": "F4:1 A4:1 C5:2 G4:1 E4:1 C5:1", "rest": 1}])     # my new house is best of all (F bar, C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "D5:1 B4:1 G4:1 B4:1 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune
CNT3 = 0.62                                      # seconds from "One" to "three" (set from the timing file)

BIG = (760, 905, 1.6)                            # the huge green shell (its opening looks right, at about x 790)
SHINY = (900, 905, .62)                          # the shiny purple shell
SNAIL = (1000, 905, 1.0)                         # the pink shell with the snail
TRY = {"white": (300, 905, .28), "coral": (560, 905, .72), "gold": (1106, 897, CS)}      # the three shells Tula brings
TRY_PROPS = lambda: [prop("sw", A.shell_white, *TRY["white"]), prop("sc", A.shell_coral, *TRY["coral"]), prop("sg", A.shell_gold, *TRY["gold"])]
TRY_ST = [CR(790), T(-120, 540)]
OLD = lambda x=800, hidden=False: prop("old", A.shell_blue, x, 902, CS * .56, hidden)      # the old blue shell, empty now
TINY = ("tiny", "hermit_blue", 440, 900, .3)
OLDE = lambda hidden=False: OLD(430, hidden)
EVE_ALL = [MILO_S, CF(820), T(1160, 700), TINY]

SHOTS = [
    # ------------------------------------------------------------ HOOK: Little Crab in a shell that is much too small (first 5 seconds)
    S("shore", CCL("shore", 900, 30, -50, stage=[CR(760)]), "Can Little Crab find a shell that fits? Look! His shell is much too small!", beat="hook", tag="hook: the shell is too small",
      cam2=CCL("shore", 780, 30, -50, stage=[CR(760)]), actors=[CR(760)], props=[prop("ar", A.arrow, 550, 790, .55, True)],
      fx=[("face", 0.02, "crab", "wow"), WIG(0.3, "crab", 13), CLAW("w:find"), ("show", "w:Look!", "ar"), BLINK("w:shell:2", "#{p}crab-shell", "the little shell blinks", 7), ("face", "w:much", "crab", "sad"), WIG("w:much", "crab", 9)],
      words=[("w:too", "TOO SMALL!", .5, .14, 1.0, "sun")]),
    *intro_shots(),      # the main intro, right after the hook
    # ------------------------------------------------------------ GOAL: a new house that fits just right
    S("shore", WIDE, "Hello, I'm Milo! Down in the shallow water lives my friend, Little Crab.", trans="iris", beat="goal", tag="shore wide: Milo on his rock",
      cam2=(940, 540, 1800), hide=["tula"], fx=[("hop", "w:Hello,", "milo"), CLAW("w:Little", 7), ("hop", "w:friend,", "milo")],
      words=[("w:Little", "LITTLE CRAB", .36, .58, .7, "sun")]),
    S("shore", CCL("shore"), "I grew, and I grew! Now my shell is too tight. I can hardly wiggle!", who="crab", beat="goal", tag="Little Crab: my shell is too tight",
      hide=["tula"], fx=[("face", 0.02, "crab", "sad"), ("hop", "w:grew!", "crab"), BLINK("w:shell", "#{p}crab-shell", "the little shell blinks"), WIG("w:wiggle!", "crab", 7, .16, 4)],
      words=[("w:tight.", "TOO TIGHT!", .5, .14, .85, "pill")]),
    S("paper", (960, 560, 1500), "Hermit crabs live in empty snail shells. The shell is their house!", beat="fact", tag="fact: hermit crabs live in empty snail shells",
      actors=[CF(1230, 760, .95)], props=[prop("es", A.shell_gold, 560, 756, .95), prop("ar", A.arrow, 880, 620, .8, True)],
      fx=[FADEIN("w:house!", "#{p}crab_w", "a hermit crab in its shell"), BLINK("w:empty", "#{p}es", "the empty shell blinks"), ("show", "w:The", "ar"), CLAW("e:house!", 5)],
      words=[("w:empty", "EMPTY SHELL", .28, .2, .6, "pill"), ("w:house!", "A HOUSE!", .72, .2, .75, "sun")]),
    S("paper", (980, 580, 1500), "Where does a hermit crab live? In a shell, or in a nest?", q=True, beat="fact", tag="question: shell or nest", pause=3.2, cam2=(990, 600, 1420),
      actors=[CF(880, 800, .95)], fx=[CLAW(0.4, 7), ("signs", "w:shell,", ["SHELL", "NEST"], 0, "wait:1.8")]),
    S("paper_blue", (960, 560, 1500), "As a hermit crab grows, it must find a bigger shell, and move in.", beat="fact", tag="fact: a growing hermit crab needs a bigger shell",
      actors=[CR(480, 760, .95)], props=[prop("ar", A.arrow, 980, 620, .7, True), prop("bs", A.shell_gold, 1400, 756, .95, True)],
      fx=[("face", 0.02, "crab", "sad"), WIG("w:grows,", "crab", 7, .16, 4), ("show", "w:find", "ar"), ("show", "w:bigger", "bs"), ("face", "w:bigger", "crab", "happy"), CLAW("w:move", 5)],
      words=[("w:grows,", "IT GROWS", .3, .2, .7, "sun"), ("w:bigger", "A BIGGER SHELL", .72, .2, .6, "pill")]),
    S("paper_blue", (980, 580, 1500), "What does a growing hermit crab need? A bigger shell, or a hat?", q=True, beat="fact", tag="question: bigger shell or hat", pause=3.2, cam2=(990, 600, 1420),
      actors=[CR(700, 800, .95)], props=[prop("bs", A.shell_gold, 1260, 796, .95)], fx=[WIG(0.4, "crab", 7, .16, 4), ("signs", "w:bigger", ["BIGGER SHELL", "HAT"], 0, "wait:1.8")]),
    S("shore", (920, 720, 1300), "Good morning, Little Crab! Why do you wiggle so?", who="tula", beat="goal", tag="Tula arrives",
      cam2=(940, 720, 1240), actors=[CR(700), T(1500, 640, .55, True)],
      fx=[("face", 0.02, "crab", "sad"), FLAP(0.1, 9), SWIM(0.1, "tula", -330, 2.6), WIG("w:wiggle", "crab", 9, .16, 4)],
      words=[("w:Good", "GOOD MORNING!", .36, .16, .7, "sun")]),
    S("shore", CCL("shore"), "I need a new house, Tula. A shell that fits just right!", who="crab", beat="goal", tag="Little Crab: I need a new house",
      hide=["tula"], fx=[("face", 0.02, "crab", "happy"), ("hop", "w:new", "crab"), CLAW("w:fits", 5), ("hop", "w:right!", "crab")],
      words=[("w:new", "A NEW HOUSE!", .5, .14, .8, "sun")]),
    S("shore", TCL("shore", 1000, 0, -20, stage=[T(1170, 640, .55, True)]), "Then let's go and look for one. I will come with you!", who="tula", beat="goal", tag="Tula: I will come with you",
      actors=[T(1170, 640, .55, True)], fx=[("face", 0.02, "tula", "happy"), ("nod", "w:look", "tula"), FLAP("w:come", 5)],
      words=[("w:look", "LET'S LOOK!", .5, .13, .8, "sun")]),
    S("shore", MCLS, "Find a shell that is not too big, and not too small. A shell that fits just right!", beat="goal", tag="Milo: just right",
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:Find", "milo"), ("hop", "w:small.", "milo"), ("hop", "w:right!", "milo")],
      words=[("w:just", "JUST RIGHT!", .5, .12, .85, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: the huge shell (much too big)
    S("shellbed", WIDE, "First, they find a great big shell. Wow! It is huge!", trans="iris", beat="obstacle1", tag="the huge shell",
      cam2=(940, 560, 1800), actors=[CR(1500, f=True), T(1750, 620, .55, True)], props=[prop("bs", A.shell_green, *BIG)],
      fx=[("walk", 0.1, "crab", -370, 2.4), FLAP(0.1, 7), SWIM(0.1, "tula", -270, 2.6), ("face", "w:Wow!", "crab", "wow"), ROCK("w:huge!", "bs", 3, 2)],
      words=[("w:Wow!", "WOW!", .68, .2, .9, "sun"), ("w:huge!", "HUGE!", .4, .3, 1.0, "pill")]),
    S("shellbed", CCL("shellbed", 860, -60), "So much room! I will try it on.", who="crab", beat="obstacle1", tag="Little Crab: so much room",
      hide=["tula"], props=[prop("bs", A.shell_green, *BIG)], fx=[("face", 0.02, "crab", "happy"), ("hop", "w:room!", "crab"), CLAW("w:try", 5)],
      words=[("w:room!", "SO MUCH ROOM!", .6, .14, .7, "sun")]),
    S("shellbed", (900, 660, 1300), "Little Crab climbs in. But where did he go? The shell is much too big!", beat="obstacle1", tag="he climbs in: too big",
      cam2=(860, 660, 1200), hide=["tula"], props=[prop("bs", A.shell_green, *BIG), prop("bp", A.big_shell_peek, BIG[0], BIG[1], BIG[2], True)],
      fx=[("walk", 0.1, "crab", -150, 1.2), ("to", 1.2, "#{p}crab_w", {"opacity": 0, "duration": .3}, "Little Crab climbs into the shell"), ("show", "w:where", "bp", None, False),
          ("to", "w:where", "#{p}bs_w", {"opacity": 0, "duration": .1}, ""), ROCK("w:go?", "bp", 9, 3),
          ("to", "w:go?", "#{p}bp-eyes", {"x": -22, "y": 16, "duration": .5, "yoyo": True, "repeat": 9, "ease": "sine.inOut"}, "two eyes look out")],
      words=[("w:where", "WHERE IS HE?", .62, .16, .75, "sun"), ("w:too", "TOO BIG!", .62, .32, .8, "pill")]),
    S("shellbed", (800, 700, 1000), "Hello? It is wobbly in here. I slide all around!", who="crab", beat="obstacle1", tag="Little Crab: I slide all around",
      cam2=(790, 700, 940), actors=[], props=[prop("bp", A.big_shell_peek, *BIG)],
      fx=[ROCK(0.2, "bp", 17, 4), ("to", 0.2, "#{p}bp-eyes", {"x": -26, "y": 22, "duration": .45, "yoyo": True, "repeat": 13, "ease": "sine.inOut"}, "he slides around inside")],
      words=[("w:wobbly", "WOBBLY!", .7, .16, .85, "sun"), ("w:slide", "WHEEE!", .72, .34, .7, "pill")]),
    S("shellbed", (900, 640, 1400), "Is the huge shell just right? Yes, or no?", q=True, beat="obstacle1", tag="question: huge shell yes or no", pause=3.2, cam2=(900, 660, 1320),
      actors=[], props=[prop("bp", A.big_shell_peek, *BIG)], fx=[ROCK(0.3, "bp", 21, 3), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 2: the shiny shell (much too heavy)
    S("rocks", WIDE, "Next, a shiny shell sits by the big rocks. It is thick, and very pretty.", trans="iris", beat="obstacle2", tag="the shiny shell by the rocks",
      cam2=(960, 560, 1800), actors=[CR(1520, f=True), T(200, 600)], props=[prop("ss", A.shell_purple, *SHINY), prop("sp", A.sparkle, 830, 720, .8, True)],
      fx=[("walk", 0.1, "crab", -390, 2.6), FLAP(0.1, 7), SWIM(0.1, "tula", 300, 3.0), ("show", "w:shiny", "sp"),
          ("to", "w:shiny", "#{p}sp", {"rotation": 40, "transformOrigin": "50% 50%", "duration": .5, "yoyo": True, "repeat": 7}, "the shell sparkles")],
      words=[("w:shiny", "SHINY!", .62, .2, .9, "sun"), ("w:pretty.", "SO PRETTY", .62, .36, .65, "pill")]),
    S("rocks", CCL("rocks", 900, -80), "Ooh, shiny! And this one is just my size.", who="crab", beat="obstacle2", tag="Little Crab: just my size",
      hide=["tula"], props=[prop("ss", A.shell_purple, *SHINY)], fx=[("face", 0.02, "crab", "wow"), ("hop", "w:shiny!", "crab"), ("face", "w:And", "crab", "happy"), CLAW("w:my", 5)],
      words=[("w:my", "MY SIZE!", .56, .14, .85, "sun")]),
    S("rocks", (1000, 700, 1200), "Little Crab pulls, and pulls. But the shell will not move. It is much too heavy!", beat="obstacle2", tag="he pulls: too heavy",
      cam2=(1010, 700, 1120), hide=["tula"], actors=[CR(1100, f=True)], props=[prop("ss", A.shell_purple, *SHINY), prop("pl", A.pull_lines, 1290, 720, .9, True)],
      fx=[("face", 0.02, "crab", "sad"), ("to", "w:pulls,", "#{p}crab_w", {"x": "+=26", "duration": .35, "yoyo": True, "repeat": 9, "ease": "power2.out"}, "Little Crab pulls"), ("show", "w:pulls,", "pl", None, False),
          BLINK("w:pulls.", "#{p}pl", "he pulls hard", 9), ("hide", "w:will", "pl"), ("face", "w:heavy!", "crab", "wow")],
      words=[("w:pulls,", "PULL!", .7, .16, .85, "sun"), ("w:heavy!", "TOO HEAVY!", .4, .34, .85, "pill")]),
    S("rocks", CCL("rocks", 860, -40, stage=[CR(1100, f=True)]), "Phew! I cannot carry this house.", who="crab", beat="obstacle2", tag="Little Crab: I cannot carry it",
      actors=[CR(1100, f=True)], props=[prop("ss", A.shell_purple, *SHINY)], fx=[("face", 0.02, "crab", "sad"), CLAW("w:Phew!", 3), ("nod", "w:carry", "crab")],
      words=[("w:Phew!", "PHEW!", .58, .14, .9, "sun")]),
    S("rocks", (980, 660, 1400), "Why can't Little Crab take the shiny shell? Too heavy, or too small?", q=True, beat="obstacle2", tag="question: too heavy or too small", pause=3.2,
      cam2=(990, 680, 1320), hide=["tula"], actors=[CR(1130, f=True)], props=[prop("ss", A.shell_purple, *SHINY)],
      fx=[("face", 0.02, "crab", "sad"), CLAW(0.4, 7), ("signs", "w:heavy,", ["TOO HEAVY", "TOO SMALL"], 0, "wait:1.8")]),
    S("rocks", CCL("rocks", 900, -60, -50, stage=[CR(1100, f=True)]), "Can you pull, like Little Crab? Pull, pull, pull!", q=True, beat="obstacle2", tag="copy me: pull", pause=3.0,
      actors=[CR(1100, f=True)], props=[prop("ss", A.shell_purple, *SHINY)],
      fx=[("to", "w:Pull,", "#{p}crab_w", {"x": "+=26", "duration": .3, "yoyo": True, "repeat": 7, "ease": "power2.out"}, "Little Crab pulls"),
          ("to", "wait:0.3", "#{p}crab_w", {"x": "+=26", "duration": .3, "yoyo": True, "repeat": 7, "ease": "power2.out"}, "pull again"), ("nod", "wait:1.9", "crab")],
      words=[("w:Pull,", "PULL!", .5, .14, .9, "sun"), ("wait:0.3", "YOUR TURN!", .5, .28, .7, "pill")]),
    # ------------------------------------------------------------ OBSTACLE 3: the shell under the kelp (somebody lives in it)
    S("kelp", WIDE, "Then, under the green kelp, they see a shell that looks just right.", trans="iris", beat="obstacle3", tag="the shell under the kelp",
      cam2=(960, 560, 1800), actors=[CR(160), T(1760, 640, .55, True)], props=[prop("sn", A.snail_shell, *SNAIL)],
      fx=[("walk", 0.1, "crab", 380, 2.6), FLAP(0.1, 7), SWIM(0.1, "tula", -280, 2.8), ("face", "w:looks", "crab", "happy"), ROCK("w:just", "sn", 3, 2)],
      words=[("w:kelp,", "THE KELP", .5, .2, .7, "sun"), ("w:just", "JUST RIGHT?", .5, .36, .7, "pill")]),
    S("kelp", (760, 730, 1000), "Knock, knock! Is anybody home?", who="crab", beat="obstacle3", tag="Little Crab: knock, knock",
      cam2=(770, 730, 940), hide=["tula"], actors=[CR(600)], props=[prop("sn", A.snail_shell, *SNAIL)],
      fx=[("face", 0.02, "crab", "happy"), TAP("w:Knock,", 5), ("snd", "w:Knock,", "tick"), ("snd", "w:knock!", "tick"), ("lookat", "w:anybody", "crab", -6)],
      words=[("w:Knock,", "KNOCK, KNOCK!", .5, .14, .75, "sun")]),
    S("kelp", (1000, 740, 900), "Two little eyes peek out. A snail lives in this shell!", beat="obstacle3", tag="a snail peeks out",
      cam2=(1020, 740, 840), hide=["tula", "crab"], props=[prop("sn", A.snail_shell, *SNAIL)],
      fx=[("fromto", "w:eyes", "#{p}sn-sn", {"opacity": 0, "x": -60}, {"opacity": 1, "x": 0, "duration": .6, "ease": "back.out(1.6)"}, "a snail peeks out"),
          ("to", "w:snail", "#{p}sn-sn", {"y": -8, "duration": .3, "yoyo": True, "repeat": 7}, "the snail nods")],
      words=[("w:eyes", "PEEK!", .68, .16, .9, "sun"), ("w:snail", "A SNAIL!", .5, .32, .8, "pill")]),
    S("kelp", (860, 740, 1160), "Oh! Sorry, Snail. This house is yours.", who="crab", beat="obstacle3", tag="Little Crab: this house is yours",
      hide=["tula"], actors=[CR(600)], props=[prop("sn", A.snail_shell, *SNAIL)],
      fx=[("to", 0.01, "#{p}sn-sn", {"opacity": 1, "duration": .01}, ""), ("face", 0.02, "crab", "wow"), ("nod", "w:Sorry,", "crab"), ("walk", "w:This", "crab", -70, 1.4), ("face", "w:This", "crab", "happy")],
      words=[("w:Sorry,", "SORRY, SNAIL!", .4, .14, .75, "sun")]),
    S("kelp", (900, 680, 1400), "Can Little Crab take the snail's shell? Yes, or no?", q=True, beat="obstacle3", tag="question: the snail's shell yes or no", pause=3.2, cam2=(910, 700, 1320),
      hide=["tula"], actors=[CR(520)], props=[prop("sn", A.snail_shell, *SNAIL)],
      fx=[("to", 0.01, "#{p}sn-sn", {"opacity": 1, "duration": .01}, ""), ("to", 0.4, "#{p}sn-sn", {"y": -8, "duration": .4, "yoyo": True, "repeat": 15}, "the snail nods"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ LOW MOMENT: three shells, and not one is right (gentle: nobody cries)
    S("kelp", (700, 680, 1500), "Three shells, and not one is right. Little Crab sits down on the sand.", beat="low", tag="Little Crab sits down",
      cam2=(700, 700, 1400), actors=[CR(520), T(1080, 620, .55, True)],
      fx=[("face", 0.02, "crab", "sad"), ("face", 0.02, "tula", "sad"), ("to", "w:sits", "#{p}crab_w", {"y": "+=14", "duration": .8, "ease": "sine.inOut"}, "Little Crab sits down"), FLAP("w:not", 3)],
      words=[("w:Three", "THREE SHELLS", .36, .16, .7, "pill"), ("w:not", "NOT ONE!", .36, .32, .8, "sun")]),
    S("kelp", CCL("kelp", 820, 0, -40, stage=[CR(520)]), "Too big. Too heavy. And somebody is home. Maybe there is no shell for me.", who="crab", beat="low", tag="Little Crab: maybe there is no shell for me",
      actors=[CR(520)], fx=[("face", 0.02, "crab", "sad"), ("nod", "w:Maybe", "crab")],
      words=[("w:Too", "TOO BIG", .3, .14, .6, "pill"), ("w:heavy.", "TOO HEAVY", .7, .14, .6, "pill"), ("w:Maybe", "NO SHELL?", .5, .3, .75, "sun")]),
    S("kelp", (580, 700, 1100), "How does Little Crab feel now? Sad, or happy?", q=True, beat="low", tag="question: sad or happy", pause=3.2, cam2=(580, 720, 1040),
      actors=[CR(520)], fx=[("face", 0.02, "crab", "sad"), ("nod", 0.5, "crab"), ("signs", "w:Sad,", ["SAD", "HAPPY"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: Little Crab's own idea; Tula dives; he tries the shells one by one
    S("kelp", CCL("kelp", 900, 0, -70, stage=[CR(520)]), "Then Little Crab looks at his two claws. And he has an idea!", beat="solution", tag="Little Crab has an idea",
      actors=[CR(520)], props=[prop("tb", A.think_bulb, 330, 640, .7, True)],
      fx=[("face", 0.02, "crab", "sad"), ("lookat", "w:looks", "crab", 8), CLAW("w:claws.", 5), ("face", "w:idea!", "crab", "happy"), ("show", "w:idea!", "tb"), ("hop", "e:idea!", "crab")],
      words=[("w:idea!", "AN IDEA!", .68, .2, .85, "sun")]),
    S("kelp", CCL("kelp", 820, 0, -40, stage=[CR(520)]), "Now I know what I need! Not too big, not too heavy, and empty.", who="crab", beat="solution", tag="Little Crab: I know what I need",
      actors=[CR(520)], fx=[("face", 0.02, "crab", "happy"), ("hop", "w:need!", "crab"), CLAW("w:Not", 7), ("nod", "w:empty.", "crab")],
      words=[("w:know", "I KNOW!", .5, .14, .85, "sun"), ("w:empty.", "AND EMPTY", .5, .29, .65, "pill")]),
    S("kelp", (700, 680, 1300), "Tula, you can dive deep! Will you bring me shells? I will try them, one by one.", who="crab", beat="solution", tag="Little Crab asks Tula",
      cam2=(720, 680, 1240), actors=[CR(520), T(1080, 620, .55, True)],
      fx=[("face", 0.02, "crab", "happy"), ("face", 0.02, "tula", "happy"), CLAW("w:dive", 5), ("nod", "w:bring", "tula"), ("hop", "w:try", "crab"), FLAP("w:one", 5)],
      words=[("w:dive", "DIVE DEEP!", .34, .14, .75, "sun"), ("w:one", "ONE BY ONE", .34, .3, .65, "pill")]),
    S("deep", WIDE, "Down, down, down goes Tula, into the deep blue water. So many empty shells!", trans="iris", beat="solution", tag="Tula dives into the deep",
      cam2=(1000, 600, 1760), actors=[T(520, 340)],
      fx=[("face", 0.02, "tula", "happy"), FLAP(0.1, 15), DIVE(0.1, "tula", 520, 280, 5.0), ("lookat", "w:So", "tula", 8)],
      words=[("w:Down,", "DOWN, DOWN, DOWN", .66, .15, .65, "sun"), ("w:deep", "THE DEEP", .26, .42, .7, "pill"), ("w:empty", "EMPTY SHELLS!", .3, .6, .7, "sun")]),
    S("deep", TCL("deep", 1240, 40, 90, stage=[T(940, 600)]), "This one, and this one, and this one. Little Crab can try them all!", who="tula", beat="solution", tag="Tula picks three shells",
      actors=[T(940, 600)], props=[prop("sw", A.shell_white, 700, 816, .28), prop("sc", A.shell_coral, 1010, 824, .72), prop("sg", A.shell_gold, 1290, 820, CS)],
      fx=[("face", 0.02, "tula", "happy"), ("lookat", 0.02, "tula", 8), ROCK("w:This", "sw", 1, 8, .12), ROCK("w:this:2", "sc", 1, 6, .12), ROCK("w:this:3", "sg", 1, 6, .12), FLAP("w:Little", 5), ("nod", "w:try", "tula")],
      words=[("w:This", "THIS ONE!", .42, .12, .7, "sun"), ("w:try", "TRY THEM ALL!", .75, .12, .7, "pill")]),
    S("paper_pink", (960, 560, 1500), "The back part of a hermit crab's body is soft. It fits inside the shell.", beat="fact", tag="fact: the soft back part fits inside the shell",
      actors=[("crab", "hermit_none", 900, 780, .95)], props=[prop("gs", A.shell_gold_on, 900 + 30 * .95, 780 - 6 * .95, .95, True)],
      fx=[BLINK("w:back", "#{p}crab-soft", "the soft back part blinks", 7), ("show", "w:fits", "gs"), ("to", "e:fits", "#{p}crab-soft", {"opacity": 0, "duration": .15}, ""), CLAW("w:shell.", 5)],
      words=[("w:soft.", "SOFT", .3, .2, .9, "sun"), ("w:inside", "INSIDE THE SHELL", .68, .2, .6, "pill")]),
    S("paper_pink", (980, 580, 1500), "Which part of a hermit crab is soft? The back part, or the claws?", q=True, beat="fact", tag="question: back part or claws", pause=3.2, cam2=(990, 600, 1420),
      actors=[("crab", "hermit_none", 900, 820, .95)], fx=[BLINK(0.4, "#{p}crab-soft", "the soft back part blinks", 5), CLAW("w:claws?", 5), ("signs", "w:back", ["BACK PART", "CLAWS"], 0, "wait:1.8")]),
    S("shore", (760, 640, 1500), "Tula comes back with shells for Little Crab. Let's count them! One, two, three!", q=True, trans="iris", beat="solution", tag="count the three shells", pause=1.0,
      cam2=(760, 660, 1440), actors=TRY_ST, props=TRY_PROPS(),
      fx=[("face", 0.02, "crab", "happy"), FLAP(0.1, 9), SWIM(0.1, "tula", 520, 3.2), ("count", "w:One,", 3, CNT3, {"x": 960, "y": 330}),
          ROCK("w:One,", "sw", 1, 8, .12), ROCK("w:two,", "sc", 1, 6, .12), ROCK("w:three!", "sg", 1, 6, .12)],
      words=[("w:shells", "SHELLS!", .72, .16, .8, "sun")]),
    S("shore", (640, 740, 1100), "Let me check with my claws. Tap, tap, tap.", who="crab", beat="solution", tag="Little Crab: tap, tap, tap",
      cam2=(640, 740, 1040), actors=[CR(790, f=True)], props=TRY_PROPS(),
      fx=[("face", 0.02, "crab", "happy"), TAP("w:Tap,", 7), ("snd", "w:Tap,", "tick"), ("snd", "w:tap,", "tick"), ("snd", "w:tap.", "tick"), ROCK("w:Tap,", "sc", 5, 3, .12)],
      words=[("w:Tap,", "TAP, TAP, TAP", .5, .14, .75, "sun")]),
    S("shore", (640, 720, 1200), "The white shell? Too small. The red shell? Too big.", beat="solution", tag="too small, too big",
      cam2=(660, 720, 1140), actors=[CR(790, f=True)], props=TRY_PROPS(),
      fx=[("face", 0.02, "crab", "sad"), BLINK("w:white", "#{p}sw", "the white shell blinks"), ROCK("w:white", "sw", 3, 8, .12), ("nod", "w:small.", "crab"), BLINK("w:red", "#{p}sc", "the red shell blinks"), ROCK("w:red", "sc", 3, 4, .12), ("nod", "w:big.", "crab")],
      words=[("w:small.", "TOO SMALL", .26, .3, .7, "pill"), ("w:big.", "TOO BIG", .42, .16, .75, "pill")]),
    S("shore", (980, 740, 1000), "And the golden shell? Little Crab slips inside.", beat="solution", tag="he slips into the golden shell",
      cam2=(1020, 740, 920), actors=[CR(790), ("crab2", "hermit_fit", 1090, 900, CS)], props=[prop("sg", A.shell_gold, *TRY["gold"]), OLD(800, True)],
      fx=[("to", 0.0, "#{p}crab2_w", {"opacity": 0, "duration": .01}, ""), ("walk", 0.1, "crab", 26, .8), BLINK("w:golden", "#{p}sg", "the golden shell blinks", 3),
          ("to", "w:slips", "#{p}crab_w", {"opacity": 0, "duration": .3}, "Little Crab slips out of the old shell"), ("show", "w:slips", "old", None, False),
          ("to", "w:inside.", "#{p}sg_w", {"opacity": 0, "duration": .2}, ""), ("to", "w:inside.", "#{p}crab2_w", {"opacity": 1, "duration": .2}, "Little Crab is in the golden shell"),
          ("to", "e:inside.", "#{p}crab2", {"y": "-=40", "duration": .2, "yoyo": True, "repeat": 1, "ease": "power2.out"}, "he hops")],
      words=[("w:golden", "THE GOLDEN SHELL", .56, .14, .65, "sun")]),
    S("shore", CCL("shore", 860, 0, -40, stage=[CF(1090)]), "It fits! It fits just right!", who="crab", beat="solution", tag="Little Crab: it fits",
      actors=[CF(1090)], props=[OLD(), prop("sp", A.sparkle, 960, 720, .8, True)],
      fx=[("face", 0.02, "crab", "happy"), ("hop", "w:fits!", "crab"), CLAW("w:It:2", 7), ("show", "w:just", "sp"), ("hop", "w:right!", "crab", 2)],
      words=[("w:fits!", "IT FITS!", .5, .14, 1.0, "sun")]),
    S("shore", (900, 700, 1300), "Hooray! The golden shell is not too big, not too heavy, and it is empty.", beat="solution", tag="the golden shell is just right",
      cam2=(910, 700, 1240), actors=[CF(1090), T(520, 640)], props=[OLD()],
      fx=[("face", 0.02, "crab", "happy"), ("face", 0.02, "tula", "happy"), ("hop", "w:Hooray!", "crab"), FLAP("w:golden", 5), CLAW("w:not", 5), ("hop", "w:empty.", "crab")],
      words=[("w:Hooray!", "HOORAY!", .64, .14, .9, "sun"), ("w:empty.", "JUST RIGHT!", .64, .3, .75, "pill")]),
    S("shore", (740, 700, 1500), "Which shell fits just right? The golden shell, or the white shell?", q=True, beat="solution", tag="question: golden or white", pause=3.2, cam2=(740, 720, 1440),
      actors=[CF(1090)], props=[prop("sw", A.shell_white, *TRY["white"]), prop("sc", A.shell_coral, *TRY["coral"]), OLD()],
      fx=[("face", 0.02, "crab", "happy"), CLAW(0.4, 9), ("signs", "w:golden", ["GOLDEN", "WHITE"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ the song moment: Little Crab SAYS the rhyme, then the tune on instruments
    S("shore", (860, 680, 1400), "Not too big, and not too small. My new house is best of all!", who="crab", beat="solution", tag="the new house rhyme", cam2=(880, 680, 1340),
      actors=[CF(1090), T(520, 700)], props=[OLD()],
      fx=[("face", 0.02, "crab", "happy"), ("face", 0.02, "tula", "happy"), CLAW("w:Not", 5), ("hop", "w:small.", "crab"), FLAP("w:My", 7), ("hop", "w:all!", "crab")],
      words=[("w:Not", "NOT TOO BIG, NOT TOO SMALL", .5, .11, .5, "sun"), ("w:My", "BEST OF ALL!", .7, .24, .6, "pill")]),
    S("shore", (860, 640, 1700), who="", sing=SING_HOUSE, beat="song", tag="song: my new house", cam2=(880, 650, 1600),
      actors=[CF(1090), T(520, 700)], props=[OLD(), prop("b1", A.A12.bubbles, 250, 620, 1.0), prop("b2", A.A12.bubbles, 1320, 600, 1.0)],
      fx=[("face", 0.02, "crab", "happy"), ("face", 0.02, "tula", "happy"),
          ("to", TB(0), "#{p}tula-ff", {"rotation": 24, "svgOrigin": "95 -122", "duration": 60 / 96, "yoyo": True, "repeat": 15, "ease": "sine.inOut"}, "Tula paddles to the beat"),
          ("to", TB(0), "#{p}crab-cl", {"rotation": -26, "svgOrigin": "150 -74", "duration": 60 / 96, "yoyo": True, "repeat": 15, "ease": "sine.inOut"}, "Little Crab waves to the beat"),
          ("hop", TB(2), "crab"), ("nod", TB(4), "tula"), ("hop", TB(6), "crab"), ("nod", TB(8), "tula"), ("hop", TB(10), "crab"), ("nod", TB(12), "tula"), ("hop", TB(14), "crab"),
          ("to", TB(0), "#{p}b1_w,#{p}b2_w", {"y": "-=260", "duration": 9.6, "ease": "none"}, "bubbles float up"),
          ("word", TB(0), "NOT TOO BIG, NOT TOO SMALL", {"x": 860, "y": 300, "size": 70, "cls": "sun", "hold": 4.4})],
      words=[(TB(8), "BEST OF ALL!", .5, .17, .7, "pill")]),
    S("shore", (860, 660, 1340), "Did Little Crab find a shell that fits? Yes, or no?", q=True, beat="solution", tag="question: did he find a shell yes or no", pause=3.2, cam2=(860, 680, 1280),
      actors=[CF(1090), T(480, 770)], props=[OLD()], fx=[CLAW(0.4, 9), FLAP(0.3, 13), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ WARM ENDING: evening, thank-yous, a new neighbour in the old shell
    S("shore_eve", WIDE, "The sun goes down, and the water turns gold. Little Crab is cozy in his new house.", trans="iris", beat="ending", tag="evening in the shallow water",
      cam2=(940, 550, 1820), props=[OLDE()],
      fx=[("face", 0.02, "crab", "happy"), ("face", 0.02, "tula", "happy"), ("hop", "w:sun", "milo"), FLAP("w:water", 5), CLAW("w:cozy", 7)],
      words=[("w:gold.", "GOLDEN WATER", .3, .46, .7, "sun"), ("w:cozy", "COZY!", .2, .62, .8, "pill")]),
    S("shore_eve", CCL("shore_eve"), "Thank you, Tula! You carried every shell.", who="crab", beat="ending", tag="Little Crab: thank you",
      hide=["tula"], fx=[("face", 0.02, "crab", "happy"), ("hop", "w:Thank", "crab"), CLAW("w:carried", 5)], words=[("w:Thank", "THANK YOU!", .5, .14, .85, "sun")]),
    S("shore_eve", TCL("shore_eve"), "And you knew just what you needed. Clever Little Crab!", who="tula", beat="ending", tag="Tula: clever Little Crab",
      hide=["crab"], fx=[("face", 0.02, "tula", "happy"), ("nod", "w:needed.", "tula"), FLAP("w:Clever", 5)], words=[("w:Clever", "CLEVER CRAB!", .5, .13, .8, "pill")]),
    S("shore_eve", CCL("shore_eve"), "I love my new house. I can wiggle, and wiggle, and wiggle!", who="crab", beat="ending", tag="Little Crab: I can wiggle",
      hide=["tula"], fx=[("face", 0.02, "crab", "happy"), ("hop", "w:love", "crab"), WIG("w:wiggle,", "crab", 15, .14, 6)], words=[("w:wiggle,", "WIGGLE, WIGGLE!", .5, .14, .75, "sun")]),
    S("shore_eve", (480, 800, 760), "And look at the old blue shell. A tiny crab moves in. Now it is her house!", beat="ending", tag="a tiny crab moves into the old shell",
      cam2=(470, 800, 700), actors=[TINY], props=[OLDE()],
      fx=[("to", 0.0, "#{p}tiny_w", {"opacity": 0, "duration": .01}, ""), BLINK("w:old", "#{p}old", "the old shell blinks", 3),
          ("to", "w:tiny", "#{p}old_w", {"opacity": 0, "duration": .25}, ""), ("to", "w:tiny", "#{p}tiny_w", {"opacity": 1, "duration": .25}, "a tiny crab is in the old blue shell"),
          ("hop", "w:moves", "tiny"), ("to", "w:Now", "#{p}tiny-cl", {"rotation": -26, "svgOrigin": "150 -74", "duration": .18, "yoyo": True, "repeat": 7}, "the tiny crab waves"), ("hop", "w:her", "tiny")],
      words=[("w:tiny", "A TINY CRAB!", .42, .16, .75, "sun"), ("w:her", "HER HOUSE", .42, .32, .65, "pill")]),
    S("shore_eve", MCLS, "When something does not fit, try again. One by one, you will find what is just right.", beat="ending", tag="the lesson",
      fx=[("hop", "w:try", "milo"), ("hop", "w:One", "milo"), ("hop", "w:right.", "milo")], words=[("w:try", "TRY AGAIN!", .5, .12, .85, "sun")]),
    S("shore_eve", (760, 700, 1300), "Do you remember? Where do hermit crabs live? In empty shells, or in trees?", q=True, beat="ending", tag="question: empty shells or trees", pause=3.2,
      cam2=(770, 720, 1220), hide=["milo", "tula"], actors=EVE_ALL, fx=[CLAW("w:Where", 9), ("signs", "w:empty", ["EMPTY SHELLS", "TREES"], 0, "wait:1.8")]),
    S("shore_eve", (900, 680, 1400), "And when a hermit crab grows, what does it find? A bigger shell, or a smaller shell?", q=True, beat="ending", tag="question: bigger or smaller shell", pause=3.2,
      cam2=(910, 700, 1320), hide=["milo"], actors=EVE_ALL, fx=[FLAP("w:grows,", 9), CLAW("w:find?", 5), ("signs", "w:bigger", ["BIGGER", "SMALLER"], 0, "wait:1.8")]),
    S("shore_eve", WIDE, "Not too big, and not too small. A cozy house is best of all!", beat="ending", tag="the closing rhyme", cam2=(980, 560, 1860), actors=EVE_ALL,
      fx=[("hop", "w:Not", "milo"), CLAW("w:not:2", 5), ("hop", "w:cozy", "milo"), FLAP("w:best", 5), ("hop", "w:all!", "tiny")],
      words=[("w:Not", "NOT TOO BIG, NOT TOO SMALL", .32, .46, .5, "sun"), ("w:cozy", "BEST OF ALL!", .3, .58, .6, "pill")]),
    S("shore_eve", (800, 700, 1400), who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(790, 700, 1320), actors=EVE_ALL,
      props=[prop("b1", A.A12.bubbles, 300, 640, 1.0), prop("b2", A.A12.bubbles, 1240, 560, 1.0)],
      fx=[("hop", 1.0, "crab"), ("nod", 1.6, "tula"), ("hop", 2.2, "tiny"), FLAP(0.2, 9),
          ("to", 0.1, "#{p}b1_w,#{p}b2_w", {"y": "-=200", "duration": 4.6, "ease": "none"}, "bubbles float up")],
      words=[(TB(3), "HOORAY!", .5, .15, .9, "sun")]),
    S("shore_eve", MCLS, "Next time: Poppy and the Dancing Sky! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure",
      fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .5, .1, .62, "sun"), ("w:See", "SEE YOU SOON!", .5, .22, .5, "pill")]),
    *intro_shots(),      # and again as the last shots: the video ends on the logo with the whole cast
]

# thumbnail (thumb.py): the promise of the first shot: Little Crab, big, squeezed into his tiny blue shell; 2 words, none of the title's words, no watermark
THUMBS = {
    "za_ep13": {"place": "shore", "cam": (900, 700, 1300),
                "actors": [("hermit_small", 980, 960, 1.5, False, '')],
                "props": [(A.arrow, 640, 720, 1.0)],
                "words": [("TOO SMALL!", 660, 420, 170, "sun", -5)]},
}
