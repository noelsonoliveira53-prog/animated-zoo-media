"""gc_ep01: "How Does a Seed Grow Into a Plant?" - Gizmo Explains, CARTOON TEST (Noelson, Nov 19 2026 12:37 AM: "create a cartoon version of that
and let's test it"). A new format for that channel: never uploaded until Noelson has watched it and said yes (plan status hold_review).
Gizmo the robot hosts, in his lab and his garden (3D music-and-sync process: "beat"). Three parts, each cut whole into one Short (only Short 1 is built for the test):
1. what is inside a seed (a baby plant, its food, the seed coat), 2. what a seed needs to start growing (water, air, the right warmth; most do not need light),
the root comes out first and grows down, the shoot grows up, 3. leaves make the plant's food with sunlight, air and water; roots take in water;
flowers help plants make new seeds, and new seeds grow into new plants.

FACTS, read at the source on Nov 19 2026 (each page fetched in this session; the page reader quotes the sentences it finds):
 [SNE] Science News Explores, "Explainer: How a seed grows into a plant" (snexplores.org/?p=201195):
   "The seeds of flowering plants are made up of three parts." (the embryo, the young plant; the endosperm, food; the seed coat that protects both)
   the endosperm is "a packet of food the embryo will use as energy to grow until it has leaves and can make its own food."
   "A tiny root called a radicle grows down into the soil."   "The first shoot or stem — called a plumule — grows up toward the sunlight."
   chloroplasts "absorb energy from the sun" and the plant makes sugar from carbon dioxide and water (photosynthesis)   the xylem "carries water absorbed by roots throughout the plant."
   (The same page says a seed needs "enough water and sunlight" to sprout; the Academy page below says most seeds do not need light: the light line is NOT said.)
 [AAS] Australian Academy of Science, Curious, "Just add water? Weird ways plants germinate" (science.org.au/curious/node/406):
   "All seeds need water, oxygen and the right temperature to germinate."   "Most seeds need to take up water to germinate"   "Seeds need oxygen so that they can produce energy"
   "Most seeds don't need light to set off germination"   "the seed coat—which is a protective layer surrounding the whole package"   "the embryonic root (radicle) pushes through."
   "'True' leaves form—the plant is now able to get energy from the sun."
 [BRIT] Britannica, "germination" (britannica.com/science/germination): water, oxygen and a suitable temperature (the reader paraphrased this part);
   "The radicle, which normally grows downward into the soil, is said to be positively geotropic."; the shoot grows upward (paraphrased by the reader).
 [USBG] United States Botanic Garden, "Flower to Seed" lesson plan K-2 (usbg.gov ... flower_to_seed_lesson_plan_k-2nd_usbotanicgarden.pdf):
   "Flowers help most plants make seeds."   "which can then grow into a new plant"   "its first leaves (cotyledons) begin making food for the young plant"
 Said as: a seed has three parts: a tiny baby plant, food for it, and a seed coat that keeps it safe; a seed needs water, air and the right warmth to start
 growing; it takes up (soaks up) water; most seeds do not need light to start; the root comes out first and grows down; the shoot grows up toward the light;
 the first two leaves (seed leaves) start making food; leaves make the plant's food with sunlight, air and water; roots take in water and it goes up through
 the plant; flowers help plants make new seeds; a seed can grow into a new plant. "Air" stands for oxygen and carbon dioxide (the words are not said).
 Read but NOT said: "radicle", "plumule", "endosperm", "embryo", "photosynthesis", "chlorophyll", seeds that need cold or fire, the coconut, "the seed swells".
 Pictures that are ours, not facts: the seed coat "like a jacket", food "like a packed lunch", a leaf "like a little kitchen".
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_gizmo as G
from kit import Kit, S, prop, W

EP = {"id": "gc_ep01", "nest": True, "beat": True, "voice": "am_michael", "speed": 0.85, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0, "wm": "brand/gizmo",
      "cast": {"gizmo": {"voice": "am_michael", "speed": 0.85}},
      "title": "How Does a Seed Grow Into a Plant?", "thumb_text": "ROOT FIRST!", "series": "Gizmo Explains (cartoon test)",
      "description": ("How does a tiny seed grow into a big plant? Gizmo the robot opens a seed in his lab, watches it wake up under the ground and follows it all "
                      "the way to a flower. A gentle science lesson for ages 4-8 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn the three parts of a seed (a tiny baby plant, its food and the seed coat), that a seed needs water, air and the right warmth to "
                      "start growing, that the root comes out first and grows down while the shoot grows up, that leaves make the plant's food with sunlight, "
                      "air and water, that roots take in water, and that flowers help plants make new seeds.\n\n"
                      "Gizmo Explains makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 4-8. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nScience News Explores (how a seed grows into a plant); Australian Academy of Science, Curious (how plants germinate); "
                      "Britannica (germination); United States Botanic Garden (flower to seed)."),
      "tags": ["how does a seed grow", "seed to plant for kids", "parts of a seed", "plant life cycle for kids", "germination for kids", "science for kids",
               "how plants grow", "roots and shoots", "Gizmo Explains", "Gizmo the robot", "preschool science", "kindergarten science"]}

GX, GY, GS = 700, 900, .7              # Gizmo in the lab
STAGES = {"glab": [("gizmo", "gizmo", GX, GY, GS)],
          "gbench": [("gizmo", "gizmo", 520, 860, .66)],
          "gwindow": [("gizmo", "gizmo", 560, 900, .66)],
          "gsoil": [("gizmo", "gizmo", 640, 380, .45)],      # hovering low over the grass, right of the watermark corner
          "ggarden": [("gizmo", "gizmo", 520, 900, .66)],
          "gmeadow": [("gizmo", "gizmo", 560, 920, .62)]}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
GIZ = lambda place, w=1000, dy=0: dict(cam=C(place, "gizmo", "all", w, 0, dy), pcam=V(place, "gizmo", "body", 1000))      # "all": the whole robot, antenna to jets (stills: "body" cut the antenna)
GQ = lambda place: WV(place, ["gizmo"], floor=.70, top=.46)                 # 9:16 question view: signs and thinking dots above his antenna
GP = lambda place: WV(place, ["gizmo"], floor=.72, top=.40)


# ------------------------------------------------------------------ Gizmo's moves
def WAVE(at, n=3):
    # the arms are drawn behind the head and body: a hand raised higher than about -90 degrees disappears behind the head (first stills, Nov 19)
    k = [{"rotation": -70, "svgOrigin": "120 120", "duration": .25}] + [{"rotation": r, "svgOrigin": "120 120", "duration": .2} for _ in range(n) for r in (-50, -84)] + [{"rotation": 0, "svgOrigin": "120 120", "duration": .3}]
    return ("to", at, "#{p}gizmo-ar", {"keyframes": k}, "Gizmo waves")


def IDEA(at):
    k = [{"opacity": 1, "duration": .12}] + [{"opacity": o, "duration": .18} for o in (.55, 1, .55, 1)]
    return [("to", at, "#{p}gizmo-glow", {"keyframes": k}, "the antenna lights up"),
            ("to", at, "#{p}gizmo-ar", {"keyframes": [{"rotation": -82, "svgOrigin": "120 120", "duration": .25}, {"rotation": -82, "svgOrigin": "120 120", "duration": 1.2}, {"rotation": 0, "svgOrigin": "120 120", "duration": .3}]}, "")]


def ARMS(at, l, r, hold=1.4, what="Gizmo moves his arms"):
    kl = [{"rotation": l, "svgOrigin": "-120 120", "duration": .3}, {"rotation": l, "svgOrigin": "-120 120", "duration": hold}, {"rotation": 0, "svgOrigin": "-120 120", "duration": .3}]
    kr = [{"rotation": r, "svgOrigin": "120 120", "duration": .3}, {"rotation": r, "svgOrigin": "120 120", "duration": hold}, {"rotation": 0, "svgOrigin": "120 120", "duration": .3}]
    return [("to", at, "#{p}gizmo-al", {"keyframes": kl}, what), ("to", at, "#{p}gizmo-ar", {"keyframes": kr}, "")]


def UP(at, hold=1.4): return ARMS(at, 84, -84, hold, "Gizmo reaches up")
def DOWN(at, hold=1.4): return ARMS(at, -30, 30, hold, "Gizmo points down")
def WIDEARMS(at, hold=1.4): return ARMS(at, 40, -40, hold, "Gizmo opens his arms wide")
def CURL(at, d=1.2): return ("to", at, "#{p}gizmo-body", {"keyframes": [{"scaleY": .78, "scaleX": 1.06, "svgOrigin": "0 0", "duration": .3}, {"scaleY": .78, "scaleX": 1.06, "svgOrigin": "0 0", "duration": d}, {"scaleY": 1, "scaleX": 1, "svgOrigin": "0 0", "duration": .25, "ease": "back.out(3)"}]}, "Gizmo curls up small")
def HOP(at, n=1): return ("hop", at, "gizmo", n)
def PULSE(at, sel, n=3, s=1.12): return ("to", at, sel, {"scale": s, "transformOrigin": "50% 50%", "duration": .22, "yoyo": True, "repeat": n}, "a part lights up")
def GROW(at, sel, origin="50% 100%", d=1.0, what="it grows"): return ("fromto", at, sel, {"scaleY": 0, "transformOrigin": origin}, {"scaleY": 1, "transformOrigin": origin, "duration": d, "ease": "power1.out"}, what)
def OFF(*sels): return ("fromto", 0, ",".join(sels), {"opacity": 0}, {"opacity": 0, "duration": .01}, "")
def ON(at, sel, what="it appears"): return ("to", at, sel, {"opacity": 1, "duration": .3}, what)


# ------------------------------------------------------------------ the boards
BOARD = (960, 540, 1500); PBOARD = (960, 470, 1700)
SO = (960, 620, 1.6); SOP = (960, 600, 1.4)              # the open seed on the board
def sopen(hidden=False): return [prop("so", G.seed_open, *SO, hidden, p=SOP)]
SOW = (960, 560, 1500)                                   # board camera for the open seed

# under the ground: the seed and its growth
RX, RY = 1150, 640
SOIL = (960, 515, 1700); SOILP = (890, 520, 1400); SOILC = (RX, 560, 1000); SOILCP = (RX, 520, 1100); SOILQ = (1020, 430, 1700); SOILQP = (RX, 420, 1500)
def gr(name="gr", sc=1.0, root=True): return prop(name, lambda p: G.growth(p, root=root), RX, RY, sc, p=(RX, RY, sc))
BELOW = lambda *k: OFF(*[f"#{{p}}gr-{x}" for x in k])

# the garden
HX, HY, HS = 1260, 940, .62
def hg(name="hg"): return prop(name, lambda p: G.growth(p, root=False), HX, HY, HS)
GARD = (1060, 640, 1500); GARDC = (HX, 760, 900); GARDP = (1150, 600, 1500); GARDCP = (HX, 700, 1050)
# the meadow
FX, FY = 1260, 940
MEAD = (1000, 560, 1700); MEADC = (FX, 460, 900); MEADP = (1060, 560, 1600); MEADCP = (FX, 520, 1100)
# the window
PX, PY = 1150, 740
WIN = (960, 520, 1700); WINC = (1000, 500, 1200); WINP = (900, 560, 1500); WINCP = (1000, 520, 1100)
WG = {"gizmo": (800, 560, .55)}          # close window shots: Gizmo hovers over the sill, his right hand at (934, 480)
# the bench
SX, SY = 1230, 740
BEN = (960, 540, 1800); BENC = (SX - 60, 600, 1000); BENP = (900, 560, 1500); BENCP = (SX - 60, 560, 1000)


SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("ggarden", GARDC, "How does a tiny seed grow into a big plant?", q=True, tag="hook: how does a seed grow", pcam=GARDCP,
      props=[hg()], fx=[OFF("#{p}hg-leaves", "#{p}hg-sl"), GROW("w:grow", "#{p}hg-shoot", d=1.4, what="a shoot grows up"), ON("w:big", "#{p}hg-sl", "two leaves open"), ON("w:plant?", "#{p}hg-leaves", "more leaves")],
      words=[("w:plant?", "?", .82, .3, 2.2, "sun", (.82, .3), 1.4)]),
    S("paper_gz", BOARD, "From this little seed, to this tall sunflower!", tag="hook: seed to sunflower", pcam=PBOARD,
      props=[prop("sd", G.seed, 560, 700, .8, p=(760, 1040, .6)), prop("ar", lambda p: G.arrow(p, 740, 620, 1060, 560), 0, 0, 1, True, p=(-40, 120, 1)),
             prop("sf", lambda p: G.sunflower(p, 560), 1300, 940, .9, True, p=(1200, 800, .75))],
      fx=[PULSE("w:little", "#{p}sd_w", 1), ("show", "w:to", "ar"), ("show", "w:tall", "sf")], words=[("w:tall", "WOW!", .82, .14, 1.0, "sun", (.5, .3), .9)]),
    S("glab", (GX, 640, 1000), "Hi! I'm Gizmo. Let's find out how it works!", tag="hook: Gizmo", pcam=GP("glab"), fx=[WAVE("w:Hi!"), HOP("w:find")],
      words=[("w:Gizmo.", "GIZMO", .78, .3, 1.1, "pill", (.5, .3), .9)]),
    # ---------------------------------------------------------------- INTRO
    S("glab", WIDE, "Welcome to my lab, curious friends!", trans="iris", tag="lab wide", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=[WAVE("w:Welcome", 4)],
      words=[("w:lab,", "HELLO!", .74, .5, 1.2, "pill", (.5, .3), 1.0)]),
    S("gbench", BEN, "Today we watch a seed grow, step by step.", tag="bench wide", pcam=BENP, props=[prop("sd", G.seed, SX, SY - 70, .8)],
      fx=[PULSE("w:seed", "#{p}sd_w", 3)], words=[("w:step", "STEP BY STEP", .5, .14, .95, "sun", (.5, .3), .8)]),
    # ---------------------------------------------------------------- PART 1: inside a seed
    S("gbench", BENC, "Here is a seed. It looks small and quiet.", part=1, tag="the seed close", pcam=BENCP, hide=["gizmo"],
      props=[prop("sd", G.seed, SX, SY - 70, .8), prop("mg", G.magnifier, SX + 230, SY - 240, .8, True, p=(SX + 170, SY - 260, .7))],
      fx=[("show", "w:seed.", "mg")], words=[("w:small", "SO SMALL", .3, .18, 1.0, "sun", (.5, .3), .85)]),
    S("gbench", (SX - 30, 560, 760), "Let's look closer, with my magnifier. Zoom!", part=1, tag="zoom", pcam=(SX - 30, 540, 820), hide=["gizmo"],
      props=[prop("sd", G.seed, SX, SY - 70, .8), prop("mg", G.magnifier, SX + 230, SY - 240, .8, p=(SX + 170, SY - 260, .7))],
      fx=[("to", "w:Zoom!", "#{p}mg_w", {"x": SX + 40, "y": SY - 90, "duration": .6, "ease": "power2.inOut"}, "the magnifier moves over the seed")],
      words=[("w:Zoom!", "ZOOM!", .26, .2, 1.1, "sun", (.5, .3), .9)]),
    S("gbench", C("gbench", "gizmo", "body", 900, 160), "But a seed is alive! Something is waiting inside.", part=1, tag="alive", pcam=V("gbench", "gizmo", "body", 1000, 100),
      fx=[("face", "w:alive!", "gizmo", "wow"), HOP("w:alive!")],
      words=[("w:alive!", "ALIVE!", .76, .18, 1.1, "sun", (.76, .4), .8)]),
    S("paper_gz", BOARD, "What do you think is inside a seed? A baby plant, or a little stone?", part=1, q=True, tag="question 1", pause=3.2, pcam=PBOARD,
      props=[prop("sd", G.seed, 960, 640, 1.6, p=(960, 600, 1.3))], fx=[("signs", "w:baby", ["PLANT", "STONE"], 0, "wait:2.0"), PULSE("wait:2.05", "#{p}sd_w", 3)]),
    S("paper_gz", SOW, "A tiny baby plant! Let's open the seed and look.", part=1, tag="open the seed", pcam=PBOARD, props=[prop("sd", G.seed, *SO, p=SOP)] + sopen(True),
      fx=[("hide", "w:open", "sd"), ("show", "w:open", "so"), PULSE("w:look.", "#{p}so-baby", 3, 1.25)], words=[("w:baby", "A BABY PLANT!", .5, .12, .9, "sun", (.5, .26), .8)]),
    S("paper_gz", (990, 600, 1050), "See the baby plant? It has a tiny root, and a tiny shoot.", part=1, tag="root and shoot", pcam=PBOARD, props=sopen(),
      fx=[PULSE("w:root,", "#{p}so-broot", 3, 1.3), PULSE("w:shoot.", "#{p}so-bshoot", 3, 1.3)],
      words=[("w:root,", "ROOT", .76, .76, 1.0, "", (.72, .74), .9), ("w:shoot.", "SHOOT", .76, .22, 1.0, "sun", (.72, .3), .9)]),
    S("paper_gz", (1000, 650, 1000), "Can you see the tiny root? Point at the root!", part=1, q=True, tag="find the root", pcam=PBOARD, props=sopen(), pause=.8,
      fx=[PULSE("w:root?:1", "#{p}so-broot", 5, 1.3)], words=[("w:Point", "POINT!", .8, .74, 1.1, "sun", (.72, .76), .9)]),
    S("paper_gz", (880, 620, 1200), "All around it is food, for the baby plant to use.", part=1, tag="food", pcam=PBOARD, props=sopen(),
      fx=[PULSE("w:food,", "#{p}so-food", 3, 1.06)], words=[("w:food,", "FOOD", .2, .2, 1.1, "sun", (.28, .3), .95)]),
    S("paper_gz", SOW, "What is the food for? To help it grow, or to play?", part=1, q=True, tag="question 1b", pause=3.2, pcam=PBOARD, props=sopen(),
      fx=[("signs", "w:grow,", ["GROW", "PLAY"], 0, "wait:2.0"), PULSE("wait:2.05", "#{p}so-food", 3, 1.06)]),
    S("paper_gz", (1000, 600, 1250), "To grow! It uses the food until it has leaves.", part=1, tag="food to grow", pcam=PBOARD, props=sopen(),
      fx=[PULSE("w:food", "#{p}so-food", 3, 1.06), PULSE("w:leaves.", "#{p}so-bshoot", 3, 1.3)], words=[("w:grow!", "TO GROW!", .5, .12, 1.0, "sun", (.5, .26), .9)]),
    S("glab", (GX + 80, 640, 1000), "It's like a packed lunch, inside the seed!", part=1, tag="lunch", pcam=GP("glab"), fx=[HOP("w:lunch,"), ("face", "w:packed", "gizmo", "wow")],
      words=[("w:lunch,", "A PACKED LUNCH!", .76, .4, .75, "sun", (.5, .3), .7)]),
    S("paper_gz", (960, 600, 1350), "And the outside is the seed coat. It keeps the seed safe.", part=1, tag="seed coat", pcam=PBOARD, props=sopen(),
      fx=[PULSE("w:coat.", "#{p}so-coat", 3, 1.05)], words=[("w:coat.", "SEED COAT", .5, .12, 1.0, "sun", (.5, .26), .9)]),
    S("gbench", BENC, "A seed coat is like a little jacket. Snug and safe!", part=1, tag="jacket", pcam=BENCP, hide=["gizmo"], props=[prop("sd", G.seed, SX, SY - 70, .8)],
      fx=[PULSE("w:jacket.", "#{p}sd-coat", 3, 1.08)], words=[("w:jacket.", "A JACKET!", .3, .2, 1.0, "sun", (.5, .3), .9)]),
    S("paper_gz", SOW, "Let's count the parts. One, two, three!", part=1, q=True, tag="count parts", pcam=PBOARD, props=sopen(),
      fx=[PULSE("w:One,", "#{p}so-coat", 1, 1.05), PULSE("w:two,", "#{p}so-food", 1, 1.06), PULSE("w:three!", "#{p}so-baby", 1, 1.3)],
      words=[("w:One,", "1", .2, .3, 1.3, "sun", (.25, .3), 1.0), ("w:two,", "2", .5, .12, 1.3, "sun", (.5, .26), 1.0), ("w:three!", "3", .8, .3, 1.3, "sun", (.75, .3), 1.0)]),
    S("gbench", (900, 470, 1700), "What keeps the seed safe? The coat, or the food?", part=1, q=True, tag="question 2", pause=3.2, pcam=GQ("gbench"),
      props=[prop("sd", G.seed, SX, SY - 70, .8)], fx=[("signs", "w:coat,", ["COAT", "FOOD"], 0, "wait:2.0"), HOP("wait:2.05")]),
    S("paper_gz", SOW, "The seed coat! Baby plant, food, and coat. Three parts!", part=1, tag="three parts", pcam=PBOARD, props=sopen(),
      fx=[PULSE("w:coat!", "#{p}so-coat", 3, 1.05)], words=[("w:Three", "3 PARTS!", .5, .12, 1.0, "sun", (.5, .26), .9)]),
    S("glab", GIZ("glab")["cam"], "Can you curl up small, like a seed? Now pop up!", part=1, q=True, tag="curl up", pcam=GP("glab"), fx=[CURL("w:curl", 1.3), HOP("w:pop")],
      words=[("w:curl", "CURL UP!", .82, .3, .9, "sun", (.5, .3), .9), ("w:pop", "POP!", .82, .55, 1.2, "", (.8, .5), .9)]),
    S("paper_gz", SOW, "Inside every seed, a baby plant is waiting to grow.", part=1, tag="waiting to grow", pcam=PBOARD, props=sopen(),
      fx=[PULSE("w:baby", "#{p}so-baby", 5, 1.3)]),
    # ---------------------------------------------------------------- PART 2: wake up, root first
    S("gwindow", WIN, "Now let's help our seed wake up. What does it need?", part=2, q=True, trans="iris", tag="window wide", pcam=WINP, cam2=W(WIN, 1.0),
      props=[prop("pt", G.pot, PX, PY)], words=[("w:need?", "?", .7, .22, 2.0, "sun", (.75, .26), 1.3)]),
    S("gwindow", WINC, "First, water! Drip, drop, drip.", part=2, tag="water", pcam=WINCP,
      move=WG, props=[prop("pt", G.pot, PX, PY), prop("cn", G.can, 946, 616, .8)],
      fx=[("to", "w:water!", "#{p}cn", {"rotation": 16, "svgOrigin": "-12 -190", "duration": .4}, "Gizmo tips the can"), ON("w:Drip,", "#{p}cn-water", "water pours")],
      words=[("w:water!", "WATER", .74, .18, 1.1, "sun", (.5, .26), .95)]),
    S("paper_gz", BOARD, "Which seed will grow? The dry seed, or the seed with water?", part=2, q=True, tag="question 2b", pause=3.2, pcam=PBOARD,
      props=[prop("s1", G.seed, 600, 700, .9, p=(760, 1000, .6)), prop("s2", G.seed, 1320, 700, .9, p=(1160, 1000, .6))] + [prop(f"d{k}", G.drop, 1320 + dx, 520, .6, p=(1160 + dx * .6, 880, .45)) for k, dx in enumerate((-90, 0, 90))],
      fx=[("signs", "w:dry", ["DRY", "WATER"], 1, "wait:2.0"), PULSE("wait:2.05", "#{p}s2_w", 3)]),
    S("paper_gz", BOARD, "The seed with water! Seeds need water to grow.", part=2, tag="water wins", pcam=PBOARD,
      props=[prop("s2", G.seed, 960, 680, 1.2, p=(960, 700, 1.0))] + [prop(f"d{k}", G.drop, 960 + dx, 420, .8, p=(960 + dx * .8, 450, .7)) for k, dx in enumerate((-150, 0, 150))],
      fx=[PULSE("w:water!", "#{p}s2_w", 3)], words=[("w:water!", "WATER!", .5, .12, 1.1, "sun", (.5, .26), .95)]),
    S("paper_gz", BOARD, "The seed soaks up the water. Slurp!", part=2, tag="soaks up", pcam=PBOARD,
      props=[prop("sd", G.seed, 960, 640, 1.4, p=(960, 640, 1.2))] + [prop(f"d{k}", G.drop, x, y, .9, True, p=(px, py, .8)) for k, (x, y, px, py) in enumerate(((620, 420, 760, 420), (1300, 420, 1160, 420), (960, 300, 960, 330)))],
      fx=[("show", "w:soaks", "d0"), ("show", "w:water.", "d1"), ("show", "w:Slurp!", "d2"), ("to", "w:Slurp!", "#{p}sd_w", {"scale": 1.18, "duration": .5, "ease": "back.out(2)"}, "the seed drinks")],
      words=[("w:Slurp!", "SLURP!", .78, .2, 1.1, "sun", (.5, .26), .95)]),
    S("paper_gz", BOARD, "Second, air! A seed needs air to grow.", part=2, tag="air", pcam=PBOARD,
      props=[prop("sd", G.seed, 960, 680, 1.2, p=(960, 700, 1.0)), prop("pf", G.puff, 900, 380, 1.2, True, p=(940, 420, 1.0))],
      fx=[("show", "w:air!", "pf"), ("to", "w:air!", "#{p}pf_w", {"x": "+=80", "duration": 2.0, "ease": "sine.inOut"}, "the air drifts")], words=[("w:air!", "AIR", .78, .2, 1.2, "sun", (.5, .26), 1.0)]),
    S("paper_gz", BOARD, "Third, just the right warmth. Not too cold!", part=2, tag="warmth", pcam=PBOARD,
      props=[prop("sd", G.seed, 760, 700, 1.2, p=(960, 760, 1.0)), prop("sun", G.warm_sun, 1260, 440, 1.0, True, p=(960, 380, .8))],
      fx=[("show", "w:warmth.", "sun"), ("to", "w:warmth.", "#{p}sun-rays", {"rotation": 30, "transformOrigin": "50% 50%", "duration": 3, "ease": "none"}, "the sun shines")],
      words=[("w:warmth.", "WARM", .2, .2, 1.2, "sun", (.28, .2), 1.0)]),
    S("gwindow", WINC, "Water, air, and warmth. Count them! One, two, three!", part=2, q=True, tag="count needs", pcam=WINCP, move=WG, props=[prop("pt", G.pot, PX, PY)], fx=[HOP("w:three!")],
      words=[("w:One,", "WATER", .8, .14, .85, "sun", (.72, .22), .75), ("w:two,", "AIR", .8, .29, .85, "sun", (.72, .32), .75), ("w:three!", "WARM", .8, .44, .85, "sun", (.72, .42), .75)]),
    S("paper_gz", BOARD, "Water, air, and warmth. That is what a seed needs to wake up!", part=2, tag="needs recap", pcam=PBOARD,
      props=[prop("dr", G.drop, 520, 500, 1.1, p=(960, 340, .8)), prop("pf", G.puff, 960, 500, .9, p=(960, 560, .7)), prop("sun", G.warm_sun, 1400, 500, .8, p=(960, 800, .6))],
      fx=[PULSE("w:Water,", "#{p}dr_w", 1), PULSE("w:air,", "#{p}pf_w", 1), PULSE("w:warmth.", "#{p}sun_w", 1)], words=[("w:wake", "WAKE UP!", .5, .12, 1.0, "sun", (.5, .14), .9)]),
    S("gsoil", SOILQ, "Does a seed need light to start growing? Yes, or no?", part=2, q=True, trans="iris", tag="question 3", pause=3.2, pcam=SOILQP, hide=["gizmo"],
      props=[gr()], fx=[BELOW("root", "shoot", "sl", "leaves"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("gsoil", SOILC, "No! Most seeds start to grow in the dark, under the ground.", part=2, tag="in the dark", pcam=SOILCP, hide=["gizmo"],
      props=[gr()], fx=[BELOW("root", "shoot", "sl", "leaves"), PULSE("w:dark,", "#{p}gr-seed", 3, 1.15)],
      words=[("w:dark,", "IN THE DARK", .3, .22, .95, "sun", (.5, .26), .8)]),
    S("gsoil", SOIL, "I have an idea! Let's watch our seed under the ground.", part=2, tag="idea", pcam=SOILP,
      props=[gr()], fx=[BELOW("root", "shoot", "sl", "leaves")] + IDEA("w:idea!"), words=[("w:idea!", "AN IDEA!", .62, .3, 1.1, "sun", (.5, .26), .95)]),
    S("gsoil", SOILC, "Pop! The seed coat opens. Something is coming out.", part=2, tag="coat opens", pcam=SOILCP, hide=["gizmo"],
      props=[gr()], fx=[BELOW("root", "shoot", "sl", "leaves"), ON("w:Pop!", "#{p}gr-crack", "the coat cracks"), ("snd", "w:Pop!", "pop"), PULSE("w:coming", "#{p}gr-seed", 3, 1.1)],
      words=[("w:Pop!", "POP!", .3, .22, 1.3, "sun", (.5, .26), 1.0)]),
    S("gsoil", SOILQ, "Which comes out first? The root, or the leaves?", part=2, q=True, tag="question 4", pause=3.2, pcam=SOILQP, hide=["gizmo"],
      props=[gr()], fx=[BELOW("root", "shoot", "sl", "leaves"), ON(0, "#{p}gr-crack"), ("signs", "w:root,", ["ROOT", "LEAVES"], 0, "wait:2.0")]),
    S("gsoil", SOILC, "The root! The root grows down, down, down.", part=2, tag="root grows down", pcam=SOILCP, hide=["gizmo"], cam2=(RX, 640, 1100),
      props=[gr()], fx=[BELOW("shoot", "sl", "leaves"), ON(0, "#{p}gr-crack"), GROW("w:grows", "#{p}gr-root", "50% 0%", 2.0, "the root grows down")],
      words=[("w:down,", "DOWN!", .76, .74, 1.2, "sun", (.72, .76), 1.0)]),
    S("gsoil", SOILC, "Then the shoot grows up, up, up, toward the light.", part=2, tag="shoot grows up", pcam=SOILCP, hide=["gizmo"], cam2=(RX, 470, 1100),
      props=[gr()], fx=[BELOW("sl", "leaves"), ON(0, "#{p}gr-crack"), GROW("w:shoot", "#{p}gr-shoot", "50% 100%", 2.0, "the shoot grows up"), ON("w:light.", "#{p}gr-sl", "two little leaves")],
      words=[("w:up,", "UP!", .76, .2, 1.3, "sun", (.72, .26), 1.0)]),
    S("glab", GIZ("glab")["cam"], "Point down, like a root! Now reach up, like a shoot!", part=2, q=True, tag="down and up", pcam=GP("glab"), fx=DOWN("w:Point", 1.0) + UP("w:reach", 1.2),
      words=[("w:Point", "DOWN!", .84, .62, 1.0, "", (.5, .55), .95), ("w:reach", "UP!", .78, .2, 1.2, "sun", (.5, .3), 1.0)]),
    S("glab", (GX + 80, 640, 1000), "Let's say it together. Root, down! Shoot, up!", part=2, q=True, tag="say it", pcam=GP("glab"), fx=DOWN("w:Root,", .8) + UP("w:Shoot,", .8),
      words=[("w:Root,", "ROOT, DOWN!", .76, .62, .9, "", (.5, .55), .8), ("w:Shoot,", "SHOOT, UP!", .76, .2, .9, "sun", (.5, .3), .8)]),
    S("gsoil", SOIL, "Root goes down. Shoot goes up. Our seed is growing!", part=2, tag="growing", pcam=SOILP,
      props=[gr()], fx=[BELOW("leaves"), ON(0, "#{p}gr-crack"), PULSE("w:Root", "#{p}gr-root", 1, 1.05), PULSE("w:Shoot", "#{p}gr-shoot", 1, 1.05), HOP("w:growing!")],
      words=[("w:growing!", "IT GROWS!", .84, .58, .9, "sun", (.5, .3), .9)]),
    # ---------------------------------------------------------------- PART 3: leaves make food, roots drink, flowers make seeds
    S("ggarden", GARD, "Look! Our shoot pokes out of the soil, into the sun.", part=3, trans="iris", tag="garden wide", pcam=GARDP,
      props=[hg()], fx=[OFF("#{p}hg-leaves", "#{p}hg-sl"), GROW("w:pokes", "#{p}hg-shoot", d=1.2, what="the shoot pokes out"), ON("w:sun.", "#{p}hg-sl")],
      words=[("w:sun.", "HELLO, SUN!", .78, .16, .9, "sun", (.5, .26), .8)]),
    S("ggarden", GARDC, "Two little seed leaves open, and they start making food.", part=3, tag="seed leaves", pcam=GARDCP, hide=["gizmo"],
      props=[hg()], fx=[OFF("#{p}hg-leaves"), ("fromto", "w:open,", "#{p}hg-sl", {"scale": .2, "transformOrigin": "50% 100%"}, {"scale": 1, "duration": .6, "ease": "back.out(2)"}, "the seed leaves open")],
      words=[("w:leaves", "SEED LEAVES", .3, .16, .9, "sun", (.5, .26), .8)]),
    S("paper_gz", BOARD, "A leaf is like a little kitchen. It makes food for the plant!", part=3, tag="leaf kitchen", pcam=PBOARD,
      props=[prop("lf", G.kitchen_leaf, 960, 600, 1.4, p=(960, 600, 1.1))], fx=[ON("w:food", "#{p}lf-food", "food appears on the leaf")],
      words=[("w:kitchen.", "A KITCHEN!", .5, .12, 1.0, "sun", (.5, .26), .9)]),
    S("paper_gz", BOARD, "It uses sunlight, air, and water to make it.", part=3, tag="sun air water", pcam=PBOARD,
      props=[prop("lf", G.kitchen_leaf, 960, 700, 1.1, p=(960, 760, .9)), prop("sun", G.warm_sun, 420, 330, .7, True, p=(700, 420, .5)),
             prop("pf", G.puff, 960, 260, .8, True, p=(960, 500, .6)), prop("dr", G.drop, 1500, 330, 1.0, True, p=(1220, 420, .8))],
      fx=[("show", "w:sunlight,", "sun"), ("show", "w:air,", "pf"), ("show", "w:water", "dr"), ON("w:make", "#{p}lf-food", "food appears")],
      words=[("w:make", "FOOD!", .5, .5, 1.1, "sun", (.5, .6), .9)]),
    S("ggarden", (900, 500, 1700), "Where does a plant get its food? It makes it, or from a shop?", part=3, q=True, tag="question 5", pause=3.2, pcam=GQ("ggarden"),
      props=[hg()], fx=[("signs", "w:makes", ["MAKES IT", "A SHOP"], 0, "wait:2.0"), HOP("wait:2.05")]),
    S("ggarden", GARDC, "It makes it, with its leaves and sunlight. Clever plant!", part=3, tag="clever plant", pcam=GARDCP, hide=["gizmo"],
      props=[hg()], fx=[PULSE("w:leaves", "#{p}hg-leaves", 3, 1.08)], words=[("w:Clever", "CLEVER!", .3, .16, 1.1, "sun", (.5, .26), .9)]),
    S("gsoil", say="And the roots? They take in water from the soil.", part=3, tag="roots drink", pcam=(RX, 700, 1100), hide=["gizmo"], trans="iris", cam=(RX, 690, 1100),
      props=[gr()] + [prop(f"w{k}", G.drop, RX + dx, RY + 170, .35, True) for k, dx in enumerate((-110, 110))],
      fx=[ON(0, "#{p}gr-crack"), ("show", "w:water", "w0"), ("show", "w:soil.", "w1"), PULSE("w:roots?", "#{p}gr-root", 3, 1.05)],
      words=[("w:water", "WATER IN!", .3, .78, 1.0, "sun", (.5, .8), .9)]),
    S("gsoil", (RX, 460, 1200), "The water goes up, all through the plant.", part=3, tag="water goes up", pcam=(RX, 470, 1300), hide=["gizmo"],
      props=[gr(), prop("wd", G.drop, RX, RY + 100, .3)],
      fx=[ON(0, "#{p}gr-crack"), ("to", "w:goes", "#{p}wd_w", {"y": RY - 300, "duration": 2.4, "ease": "power1.inOut"}, "a drop travels up the plant")],
      words=[("w:up,", "UP IT GOES!", .3, .2, 1.0, "sun", (.5, .26), .85)]),
    S("gsoil", (RX, 600, 1300), "Let's name the parts. Root! Stem! Leaves!", part=3, q=True, tag="name the parts", pcam=(RX, 600, 1300), hide=["gizmo"],
      props=[gr()], fx=[ON(0, "#{p}gr-crack"), PULSE("w:Root!", "#{p}gr-root", 3, 1.05), PULSE("w:Stem!", "#{p}gr-shoot", 3, 1.05), PULSE("w:Leaves!", "#{p}gr-leaves", 3, 1.1)],
      words=[("w:Root!", "ROOT", .7, .82, .9, "", (.75, .78), .8), ("w:Stem!", "STEM", .7, .45, .9, "sun", (.75, .5), .8), ("w:Leaves!", "LEAVES", .22, .16, .9, "sun", (.3, .3), .8)]),
    S("ggarden", GIZ("ggarden")["cam"], "Can you slurp like a thirsty root? Slurp, slurp!", part=3, q=True, tag="slurp", pause=1.0, pcam=GP("ggarden"), fx=[HOP("w:Slurp,", 2), ("face", "w:slurp", "gizmo", "wow")],
      words=[("w:Slurp,", "SLURP!", .76, .2, 1.1, "sun", (.5, .3), .9)]),
    S("gmeadow", MEAD, "Days go by. The plant grows taller, with more leaves.", part=3, trans="iris", tag="meadow taller", pcam=MEADP, cam2=W(MEAD, 1.0),
      props=[prop("pl", lambda p: G.growth(p, root=False), FX, FY, .62)], fx=[GROW("w:taller,", "#{p}pl-stem2", d=1.6, what="the plant grows taller"), ON("w:taller,", "#{p}pl-stem2")],
      words=[("w:taller,", "TALLER!", .78, .16, 1.1, "sun", (.5, .26), .9)]),
    S("gmeadow", MEADC, "Then, a flower opens! Hello, flower!", part=3, tag="flower opens", pcam=MEADCP, hide=["gizmo"],
      props=[prop("pl", lambda p: G.growth(p, root=False), FX, FY, .62)], fx=[ON(0, "#{p}pl-stem2"),
      ("fromto", "w:flower", "#{p}pl-flower", {"opacity": 0, "scale": .2, "transformOrigin": "50% 50%"}, {"opacity": 1, "scale": 1, "duration": .6, "ease": "back.out(2)"}, "the flower opens")],
      words=[("w:Hello,", "HELLO!", .26, .2, 1.1, "sun", (.5, .26), .9)]),
    S("gmeadow", (FX, 500, 1100), "Flowers help plants make new seeds.", part=3, tag="flowers make seeds", pcam=MEADCP, hide=["gizmo"],
      props=[prop("pl", lambda p: G.growth(p, root=False), FX, FY, .62)], fx=[ON(0, "#{p}pl-stem2"), ON(0, "#{p}pl-flower"), PULSE("w:seeds.", "#{p}pl-flower", 3, 1.08)],
      words=[("w:seeds.", "NEW SEEDS!", .28, .2, 1.0, "sun", (.5, .26), .85)]),
    S("gmeadow", (FX - 40, 560, 1200), "Count the new seeds with me. One, two, three!", part=3, q=True, tag="count seeds", pcam=(FX - 20, 560, 1300), hide=["gizmo"],
      props=[prop("pl", lambda p: G.growth(p, root=False), FX, FY, .62)] + [prop(f"s{k}", G.seed_small, FX + dx, 640, .9, True, p=(FX + dx * .8, 640, .8)) for k, dx in enumerate((-180, 0, 180))],
      fx=[ON(0, "#{p}pl-stem2"), ON(0, "#{p}pl-flower"), ("show", "w:One,", "s0"), ("show", "w:two,", "s1"), ("show", "w:three!", "s2")],
      words=[("w:three!", "3", .8, .3, 1.4, "sun", (.75, .3), 1.1)]),
    S("paper_gz", (960, 540, 1500), "New seeds can grow into new plants. Round and round!", part=3, tag="cycle", pcam=(960, 520, 1500),
      props=[prop("cy", G.cycle, 960, 520, .8, p=(960, 600, .8))],
      fx=[PULSE("w:New", "#{p}cy-k0", 1), PULSE("w:grow", "#{p}cy-k1", 1), PULSE("w:plants.", "#{p}cy-k2", 1), PULSE("w:Round", "#{p}cy-k3", 1), PULSE("w:round!", "#{p}cy-k0", 1)],
      words=[("w:Round", "ROUND!", .5, .47, .6, "sun", (.5, .58), .6)]),
    S("gmeadow", MEADC, "What helps a plant make new seeds? A flower, or a rock?", part=3, q=True, tag="question 6", pause=3.2, pcam=MEADCP, hide=["gizmo"],
      props=[prop("pl", lambda p: G.growth(p, root=False), FX, FY, .62)], fx=[ON(0, "#{p}pl-stem2"), ON(0, "#{p}pl-flower"), ("signs", "w:flower,", ["FLOWER", "ROCK"], 0, "wait:2.0")]),
    S("gmeadow", (FX, 500, 1100), "A flower! It helps the plant make new seeds.", part=3, tag="flower answer", pcam=MEADCP, hide=["gizmo"],
      props=[prop("pl", lambda p: G.growth(p, root=False), FX, FY, .62)], fx=[ON(0, "#{p}pl-stem2"), ON(0, "#{p}pl-flower"), PULSE("w:flower!", "#{p}pl-flower", 3, 1.08)],
      words=[("w:flower!", "A FLOWER!", .28, .2, 1.0, "sun", (.5, .26), .85)]),
    S("gmeadow", GIZ("gmeadow")["cam"], "Stretch your arms wide, like big green leaves!", part=3, q=True, tag="stretch", pause=1.0, pcam=GP("gmeadow"), fx=WIDEARMS("w:Stretch", 1.6),
      words=[("w:wide,", "STRETCH!", .76, .2, 1.0, "sun", (.5, .3), .9)]),
    # ---------------------------------------------------------------- QUIZ + GOODBYE
    S("gmeadow", GIZ("gmeadow", 900)["cam"], "Wiggle your fingers, like warm sunshine. Shine, shine!", part=3, q=True, tag="shine", pause=1.0, pcam=GP("gmeadow"), fx=UP("w:Wiggle", 1.8) + [HOP("w:Shine,", 2)],
      words=[("w:Shine,", "SHINE!", .76, .2, 1.1, "sun", (.5, .3), .9)]),
    S("glab", WIDE, "Quiz time! Let's remember what we learned.", part=4, trans="iris", tag="quiz time", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=IDEA("w:Quiz"),
      words=[("w:Quiz", "QUIZ TIME!", .74, .5, 1.3, "sun", (.5, .3), 1.0)]),
    S("gbench", (900, 470, 1700), "What is inside a seed? A baby plant, or a toy car?", part=4, q=True, tag="quiz 1", pause=3.2, pcam=GQ("gbench"),
      props=[prop("sd", G.seed, SX, SY - 70, .8)], fx=[("signs", "w:baby", ["PLANT", "TOY CAR"], 0, "wait:2.0")]),
    S("paper_gz", SOW, "A baby plant, with its food and its coat!", part=4, tag="quiz 1 answer", pcam=PBOARD, props=sopen(),
      fx=[PULSE("w:baby", "#{p}so-baby", 1, 1.3), PULSE("w:food", "#{p}so-food", 1, 1.06), PULSE("w:coat!", "#{p}so-coat", 1, 1.05)]),
    S("gsoil", SOILQ, "What grows first, the root, or the shoot?", part=4, q=True, tag="quiz 2", pause=3.2, pcam=SOILQP, hide=["gizmo"], trans="iris",
      props=[gr()], fx=[BELOW("root", "shoot", "sl", "leaves"), ON(0, "#{p}gr-crack"), ("signs", "w:root,", ["ROOT", "SHOOT"], 0, "wait:2.0")]),
    S("gsoil", SOILC, "The root! It grows down into the soil.", part=4, tag="quiz 2 answer", pcam=SOILCP, hide=["gizmo"],
      props=[gr()], fx=[BELOW("shoot", "sl", "leaves"), ON(0, "#{p}gr-crack"), GROW("w:root!", "#{p}gr-root", "50% 0%", 1.6, "the root grows down")],
      words=[("w:down", "DOWN!", .76, .74, 1.2, "sun", (.72, .76), 1.0)]),
    S("ggarden", (900, 500, 1700), "What do leaves make for the plant? Food, or rain?", part=4, q=True, tag="quiz 3", pause=3.2, pcam=GQ("ggarden"), trans="iris",
      props=[hg()], fx=[("signs", "w:Food,", ["FOOD", "RAIN"], 0, "wait:2.0")]),
    S("ggarden", GARDC, "Food! Leaves use sunlight to make food.", part=4, tag="quiz 3 answer", pcam=GARDCP, hide=["gizmo"],
      props=[hg()], fx=[PULSE("w:Leaves", "#{p}hg-leaves", 3, 1.08)], words=[("w:Food!", "FOOD!", .3, .16, 1.2, "sun", (.5, .26), 1.0)]),
    S("gmeadow", MEAD, "From a tiny seed, to a big plant. Thanks for exploring with me!", part=4, tag="goodbye", pcam=MEADP, cam2=W(MEAD, 1.0),
      props=[prop("pl", lambda p: G.growth(p, root=False), FX, FY, .62)], fx=[ON(0, "#{p}pl-stem2"), ON(0, "#{p}pl-flower"), WAVE("w:Thanks", 5), HOP("w:exploring")],
      words=[("w:Thanks", "BYE-BYE!", .78, .2, 1.1, "pill", (.5, .3), .9)]),
]
for _s in SHOTS:        # a picture board never drifts closer: it only pulls out a little (zc_ep08)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)
    for _f in _s["fx"]:        # 9:16: a word never sits on the title band's second line (stills: TO GROW!, SEED COAT, ZOOM! touched INSIDE?)
        if _f[0] == "word" and len(_f) > 3 and "p" in _f[3] and _s["pcam"]: _f[3]["p"]["y"] = max(_f[3]["p"]["y"], round(_s["pcam"][1] - .15 * _s["pcam"][2]))

SHORTS = [
    {"id": "gc_ep01_short1", "title": "What Is Inside a Seed?", "band": ("WHAT IS", "INSIDE?"), "thumb_text": "BABY PLANT!", "part": 1,
     "extra_first": [S("gbench", BENC, "What is hiding inside a tiny seed?", part=1, q=True, tag="hook: inside a seed", pcam=BENCP, hide=["gizmo"],
                       props=[prop("sd", G.seed, SX, SY - 70, .8)], fx=[PULSE(0.3, "#{p}sd_w", 5)], words=[("w:hiding", "?", .3, .2, 2.2, "sun", (.5, .3), 1.3)])]},
]

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
THUMBS = {
    "gc_ep01": {"place": "gsoil", "cam": (1080, 470, 1300), "actors": [("gizmo", 560, 360, .55, False, 'gsap.set("#P-glow",{opacity:1});gsap.set("#P-jaw",{opacity:1});')],
                "props": [(lambda p: G.growth(p), RX, RY, 1.0)],
                "words": [("ROOT", 1560, 300, 170, ""), ("FIRST!", 1560, 480, 190, "sun")]},
    "gc_ep01_short1": {"place": "paper_gz", "cam": (960, 560, 1500), "actors": [],
                       "props": [(G.seed_open, 960, 640, 1.6)],
                       "words": [("BABY", 540, 380, 200, ""), ("PLANT!", 540, 1260, 200, "sun")]},
}
