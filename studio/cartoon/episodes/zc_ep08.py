"""zc_ep08: "Who Lives at the Top of the Jungle?" - cartoon fact lesson with Milo and Mango the spider monkey (3D music-and-sync process: "beat").
Milo flies up the rainforest floor by floor. Three parts, each cut whole into one Short:
1. four layers, and the forest floor (the darkest layer; the anteater), 2. the understory (big leaves; the tree frog) and the canopy (the roof of leaves;
Mango and the macaw pick fruit), 3. the emergent layer (taller than all the rest, the sunniest; the harpy eagle, fliers and butterflies).
Mango's own food lesson is zc_ep06 and her tail lesson zc_ep04: neither is repeated (here she only shows us her floor and picks one fruit).

FACTS, read at the source on Nov 19 2026 (each page fetched by the session's page reader, which quotes the sentences it finds; nothing is said as an animal fact without one):
 [STRI] Smithsonian Tropical Research Institute, striresearch.si.edu/rainforest/home/rainforest-layers/
   "We will be referring to four layers."   "From top to bottom, they are: the emergent layer, the canopy, the understory, and the forest floor."
   "the main layer of treetops forms a barrier that cuts off most of the light and wind"   "a few trees considerably taller than all the rest stick up out of the greenery"
   "The tropical sun beats down on them"   "many of the creatures that live up here move around by flying or gliding"   "One of the top predators up here is a flier: the harpy eagle"
   "Male Morpho butterflies gather up here"
 [NGE] National Geographic Education, education.nationalgeographic.org/resource/rain-forest/
   "The top layer of the rainforest is the emergent layer."   "The animals living in the emergent layer of the Amazon rainforest include birds, bats, gliders and butterflies."
   "Large raptors, such as harpy eagles (Harpia harpyja), are its top predators."   "...spreads wide as the trees reach the sunny upper layer"
   "The canopy blocks winds, rainfall and sunlight, creating a humid, still and dark environment below."
   "canopy fruit is snatched up in the large beaks of screeching scarlet macaws (Ara macao)"   "...and picked by barking spider monkeys (Ateles)"
   "the understory is an even darker, stiller and more humid environment."   "The large leaves of understory plants are able to catch the minimal sunlight reaching beyond the dense canopy."
   "Amphibians, such as dazzlingly colored tree frogs, thrive in the humidity because it keeps their skin moist."
   "The forest floor is the darkest of all rainforest layers"   "Animals such as collared peccaries (Pecari tajacu), armadillos and anteaters forage in the decomposing brush"
 [TFK] TIME for Kids, timeforkids.com/g2/jungle-layers/ (the reader gave a summary, not quotes): the emergent layer is "the sunniest level"; the forest floor is "the darkest, dampest level".
 [SW] SeaWorld, seaworld.org/animals/facts/mammals/giant-anteater/
   "Giant anteaters prey almost exclusively on social insects (i.e. ants and termites)."   "Anteaters are able to detect insects with their powerful sense of smell"
   "Tapered head with a long, tubular mouth opening."   "Giant anteaters are terrestrial."
 Said as: four layers like the floors of a house (the floors picture is ours); the leaves up high block the sunlight; the forest floor is the darkest layer; anteaters look
 for food on the ground and find ants with their nose (smell); the understory is shady and its plants have big leaves to catch the little light; the air is wet and keeps a
 tree frog's skin wet (moist); the canopy is a thick roof of leaves where spider monkeys pick fruit and macaws grab fruit with big beaks; in the emergent layer a few trees are
 taller than all the rest and it is the sunniest layer; animals up there fly or glide; harpy eagles live there (a big bird: "large raptors"); butterflies flutter there.
 Read but NOT said: predators and prey (the eagle is only "a very big bird"), the green mamba, leopards, heights in metres or feet, bats and gliders (not drawn), the macaw's screech.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_zc_ep08 as A
from kit import Kit, S, prop, W

EP = {"id": "zc_ep08", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "Who Lives at the Top of the Jungle?", "thumb_text": "WAY UP HIGH!", "series": "Animal Facts with Milo",
      "description": ("Who lives at the top of the jungle? Milo the bluebird flies up the rainforest, floor by floor, with Mango the spider monkey: from the dark forest floor "
                      "to the sunny treetops! A gentle animal lesson for ages 2-6 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn that a rainforest has four layers (the forest floor, the understory, the canopy and the emergent layer), that the forest floor is the darkest "
                      "layer, where anteaters sniff out ants, that understory plants have big leaves and tree frogs like the wet air, that spider monkeys and macaws pick fruit "
                      "in the canopy, and that the emergent layer is the sunniest, where harpy eagles and butterflies fly.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSmithsonian Tropical Research Institute (rainforest layers); National Geographic Education (rain forest); "
                      "TIME for Kids (jungle layers); SeaWorld (giant anteater)."),
      "tags": ["rainforest layers", "rainforest animals for kids", "layers of the rainforest", "jungle animals", "harpy eagle", "tree frog", "anteater", "animal facts for kids",
               "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

MX = 1100; MY = 432; MS = .62          # Mango / the eagle on the high branch (canopy and emergent: the branch is at y = 430 in both)
AX = 1000; AY = 905; AS = .8           # the anteater on the forest floor
FX = 1060; FY = 645; FS = .6           # the tree frog on its big leaf
STAGES = {"zoo": [("milo", "milo", 960, 940, 1.1, False, False)],
          "bigtree": [("mango", "monkey", 900, -536, .7), ("milo", "milo", 640, 640, .7, False, True)],
          "floor": [("ant", "anteater", AX, AY, AS), ("milo", "milo", 420, 905, .72)],
          "understory": [("frog", "frog", FX, FY, FS), ("milo", "milo", 420, 470, .7, False, True)],
          "canopy": [("mango", "monkey", MX, MY, MS), ("milo", "milo", 420, 300, .62, False, True)],
          "emergent": [("eagle", "eagle", MX, MY, MS), ("milo", "milo", 420, 300, .62, False, True)]}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920); INK = art.INK
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 900))

# the high branch (canopy: Mango; emergent: the eagle)
MW = (960, 380, 1800); MC = (MX, 290, 1000); MH = (MX, 262, 720); QC = (MX, 170, 1300)
MP = WV("canopy", ["mango"], floor=.68, top=.42); MPW = WV("canopy", ["mango"], hmin=1040, floor=.68, top=.42); MPQ = WV("canopy", ["mango"], floor=.70, top=.46); MPH = (MX, 270, 900)
EC = (MX, 250, 1100); EH = (MX, 210, 800); EQ = (MX, 130, 1400)
EP_ = WV("emergent", ["eagle"], floor=.68, top=.42); EPW = WV("emergent", ["eagle"], hmin=1200, floor=.68, top=.42); EPQ = WV("emergent", ["eagle"], floor=.70, top=.46)
# the forest floor
AW = (960, 640, 1700); AC = (1080, 700, 1200); AH = (1230, 720, 1000); AQ = (1040, 600, 1600)
AP = WV("floor", ["ant"], floor=.70, top=.42, pad=.09); APW = WV("floor", ["ant"], floor=.70, top=.42, pad=.25); APQ = WV("floor", ["ant"], floor=.72, top=.47)
# the understory
UW = (960, 460, 1800); UC = (FX, 540, 760); UH = (FX, 560, 560); UQ = (FX, 460, 980)
UP = WV("understory", ["frog"], hmin=700, floor=.68, top=.42); UPQ = WV("understory", ["frog"], hmin=760, floor=.70, top=.46)

# ------------------------------------------------------------------ the layer tree board
LT = (880, 500, .8); LTP = (1010, 520, .62)
LCAM = (940, 520, 1560); LPCAM = (960, 480, 1700)
BY = lambda k, s=LT: s[1] + A.band_y(k) * s[2]          # the middle of band k (0 = top) on the board
ICX = LT[0] + round(770 * LT[2])                                       # where the animal pictures sit, right of the bands
ICP = (1010 + 330, .4)                                 # the same in 9:16 (x, scale): on the band itself, at its right end


def tree(hidden_bands=(), lit=None):
    """The layer tree; `hidden_bands` start invisible (shown by ("to", at, "#{p}lt-bK", {"opacity": 1})), `lit` pulses."""
    out = [prop("lt", A.layer_tree, *LT, p=LTP)]
    return out


def bands_off(ks): return ("fromto", 0, ",".join(f"#{{p}}lt-b{k}" for k in ks), {"opacity": .2}, {"opacity": .2, "duration": .01}, "")      # faint, not empty: a board shows its picture from the start
def band_on(at, k, what="a layer appears"): return ("to", at, f"#{{p}}lt-b{k}", {"opacity": 1, "duration": .3}, what)
def pulse(at, k, n=3): return ("to", at, f"#{{p}}lt-b{k}", {"scale": 1.04, "transformOrigin": "50% 50%", "duration": .22, "yoyo": True, "repeat": n}, "the layer lights up")


ICONS = {0: A.eagle_icon, 1: A.macaw_icon, 2: A.frog_icon, 3: A.anteater_icon}


def icons(shown, new=()):
    return [prop(f"i{k}", A.icon(ICONS[k]), ICX, BY(k), .78, k in new, p=(ICP[0], BY(k, LTP), ICP[1])) for k in range(4) if k in shown or k in new]


# ------------------------------------------------------------------ actions
def SNIFF(at, n=7, who="ant"): return ("to", at, "#{p}" + who + "-snout", {"rotation": -7, "svgOrigin": "240 -230", "duration": .14, "yoyo": True, "repeat": n}, "the anteater sniffs")
def LICK(at, n=5, who="ant"): return ("to", at, "#{p}" + who + "-jaw", {"opacity": 1, "duration": .12, "yoyo": True, "repeat": n}, "its long tongue flicks")
def FLAP(at, who="eagle", n=5):
    return [("to", at, f"#{{p}}{who}-wl", {"rotation": -34, "svgOrigin": "-70 -300", "duration": .2, "yoyo": True, "repeat": n}, f"the {who} flaps"),
            ("to", at, f"#{{p}}{who}-wr", {"rotation": 34, "svgOrigin": "70 -300", "duration": .2, "yoyo": True, "repeat": n}, "")]
def PUFF(at, n=3): return ("to", at, "#{p}frog-throat", {"opacity": 1, "scale": 1.3, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": n}, "the frog puffs its throat")
def BFLY(name, x, y, s=.8, hidden=False, p=None): return prop(name, A.butterfly, x, y, s, hidden, p)
def FLUT(at, name, dx, dy, d=3.0):
    return [("to", at, f"#{{p}}{name}-wings", {"scaleX": .25, "transformOrigin": "50% 50%", "duration": .12, "yoyo": True, "repeat": int(d / .12) | 1}, ""),
            ("to", at, f"#{{p}}{name}_w", {"x": f"+={dx}", "y": f"+={dy}", "duration": d, "ease": "sine.inOut"}, "a butterfly flutters")]


SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("paper_blue", LCAM, "Who lives at the top of the jungle?", q=True, tag="hook: who lives at the top", pcam=LPCAM, props=tree(),
      fx=[pulse("w:top", 0)], words=[("w:top", "?", .9, .3, 2.4, "sun", (.82, .3), 1.4)]),
    S("paper_pink", (960, 540, 1500), "A bird? A frog? Or an anteater?", tag="hook: guesses", pcam=(960, 480, 1700),
      props=[prop("a", A.icon(A.eagle_icon), 600, 560, 1.3, True, p=(700, 400, 1.0)), prop("b", A.icon(A.frog_icon), 960, 560, 1.3, True, p=(1220, 560, 1.0)),
             prop("c", A.icon(A.anteater_icon), 1320, 560, 1.3, True, p=(700, 720, 1.0))],
      fx=[("show", "w:bird?", "a"), ("show", "w:frog?", "b"), ("show", "w:anteater?", "c")]),
    S("canopy", say="I'm Milo. Let's fly up and find out!", tag="hook: Milo", hide=["mango"], fx=[("hop", "w:fly", "milo")], **MILO("canopy")),
    # ---------------------------------------------------------------- INTRO
    S("zoo", WIDE, "Welcome to The Animated Zoo, friends!", trans="iris", tag="gate wide", words=[("w:Animated", "HELLO!", .74, .6, 1.2, "pill")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, -40), "Today we visit the rainforest, floor by floor.", tag="Milo close", words=[("w:floor", "FLOOR BY FLOOR", .5, .16, .95, "sun")]),
    S("bigtree", (960, -100, 2700), "Look at this tall, tall tree! Who is way up there?", q=True, trans="iris", tag="tall tree", cam2=(960, -180, 2500), pcam=(900, -520, 1900), pcam2=(900, -560, 1700),
      fx=[("fly", "w:tall,", "milo", 760, -200, 2.4), ("hop", "w:up", "mango")], words=[("w:tall,", "SO TALL!", .26, .7, .9, "sun", (.5, .33), .9)]),
    S("canopy", MC, "It's Mango! Mango is a spider monkey. She will show us around.", tag="this is Mango", hide=["milo"], pcam=MP, words=[("w:Mango!", "MANGO", .2, .3, 1.1, "pill", (.5, .33))],
      fx=[("hop", "w:Mango!", "mango"), ("arm", "w:show", "mango", "r", -60)]),
    # ---------------------------------------------------------------- PART 1: four layers, and the forest floor
    S("paper_blue", LCAM, "A rainforest has layers, like the floors of a house.", part=1, tag="board: layers", pcam=LPCAM, props=tree(),
      fx=[pulse("w:layers,", 3), pulse("w:floors", 1)], words=[("w:layers,", "LAYERS", .9, .5, .85, "sun", (.5, .33), .9)]),
    S("paper_blue", LCAM, "Let's count them from the bottom. One, two, three, four!", part=1, q=True, tag="board: count four", pcam=LPCAM, props=tree(),
      fx=[bands_off((0, 1, 2, 3)), band_on("w:One,", 3), band_on("w:two,", 2), band_on("w:three,", 1), band_on("w:four!", 0)],
      words=[("e:four!", "4", .9, .3, 1.6, "sun", (.82, .3), 1.3)]),
    S("paper_blue", LCAM, "Four layers! Four floors, from the ground to the sky.", part=1, tag="board: four layers", pcam=LPCAM, props=tree(),
      fx=[pulse("w:ground", 3), pulse("w:sky.", 0)], words=[("w:Four", "4 LAYERS", .9, .5, .62, "sun", (.5, .33), .95)]),
    S("canopy", say="How many floors does your house have?", part=1, q=True, tag="your house", hide=["mango"], pause=1.0, fx=[("hop", "w:How", "milo")],
      words=[("w:floors", "HOW MANY?", .74, .2, .9, "sun", (.5, .33), .85)], **MILO("canopy")),
    S("floor", AW, "Floor number one is the forest floor. Down, down, down!", part=1, trans="iris", tag="floor wide", hide=["ant"], pcam=(700, 600, 1500), pcam2=(700, 640, 1600),
      move={"milo": (760, 560, .72, False)}, fly=["milo"], fx=[("fly", "w:Down,", "milo", 600, 860, 2.2)], words=[("w:forest", "THE FOREST FLOOR", .5, .14, .9, "sun", (.5, .33), .75)]),
    S("floor", C("floor", "milo", "body", 900), "It is dark down here. Can you see?", part=1, q=True, tag="dark here", hide=["ant"], pcam=V("floor", "milo", "body", 1000),
      fx=[("face", "w:dark", "milo", "wow")], words=[("w:dark", "DARK!", .74, .24, 1.1, "", (.5, .33), .9)]),
    S("floor", (700, 860, 1100), "Fallen leaves cover the ground. Crunch, crunch!", part=1, tag="crunch", hide=["ant"], pcam=(560, 760, 1100), move={"milo": (560, 905, .72)},
      fx=[("hop", "w:Crunch,", "milo"), ("hop", "w:crunch!", "milo"), ("snd", "w:Crunch,", "pop"), ("snd", "w:crunch!", "pop")], words=[("w:Crunch,", "CRUNCH!", .7, .3, 1.0, "sun", (.5, .33), .9)]),
    S("paper", (960, 540, 1500), "The leaves up high block the sunlight.", part=1, tag="board: leaf roof", pcam=(960, 420, 1700),
      props=[prop("lr", A.leaf_roof, 960, 620, .82, p=(960, 560, .7))],
      fx=[("to", "w:block", "#{p}lr-r0,#{p}lr-r1,#{p}lr-r2", {"opacity": .25, "duration": .5}, "the light gets thin"),
          ("to", "w:leaves", "#{p}lr-roof", {"y": -14, "duration": .2, "yoyo": True, "repeat": 3}, "the leaf roof wiggles")],
      words=[("w:block", "NO SUN!", .82, .2, 1.0, "", (.5, .3), .8)]),
    S("paper", (960, 540, 1500), "So the forest floor is the darkest layer of all.", part=1, tag="board: darkest", pcam=LPCAM, props=tree(),
      fx=[pulse("w:darkest", 3, 5)], words=[("w:darkest", "DARKEST!", .9, .5, .7, "sun", (.5, .33), .8)]),
    S("floor", say="Let's squint, to see in the dark. Squint!", part=1, q=True, tag="squint", hide=["ant"],
      fx=[("to", "w:Squint!", "#{p}milo-eyeL,#{p}milo-eyeR", {"scaleY": .35, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 3}, "Milo squints")],
      words=[("w:Squint!", "SQUINT!", .74, .22, 1.0, "sun", (.5, .33))], **MILO("floor", 900)),
    S("floor", AW, "Sniff, sniff! Who is that?", part=1, q=True, tag="who is that", pcam=AP, pcam2=AP, move={"ant": (AX - 420, AY, AS)},
      fx=[("walk", 0.1, "ant", 420, 2.6), SNIFF("w:Sniff,")], words=[("w:Who", "WHO?", .82, .2, 1.1, "sun", (.5, .33), 1.0)]),
    S("floor", AC, "It's an anteater! Look at its long, long nose.", part=1, tag="an anteater", hide=["milo"], pcam=AP, pcam2=AP,
      props=[prop("ar", lambda p: art.arrow(p, 1530, 560, 1400, 700), 0, 0, 1, True, p=(-120, 20, 1))], fx=[("show", "w:long,", "ar"), SNIFF("w:nose.", 5)],
      words=[("w:anteater!", "ANTEATER", .24, .2, 1.0, "pill", (.5, .33), .85)]),
    S("floor", AQ, "Where does the anteater look for food? Up in the trees, or down on the ground?", part=1, q=True, tag="question 1", pause=3.2, hide=["milo"], pcam=APQ, pcam2=APQ,
      fx=[("signs", "w:Up", ["TREES", "GROUND"], 1, "wait:2.0"), SNIFF("wait:2.05", 5)]),
    S("floor", AC, "On the ground! It sniffs through the fallen leaves.", part=1, tag="on the ground", hide=["milo"], pcam=APW, pcam2=APW, move={"ant": (AX - 160, AY, AS)},
      fx=[("walk", 0.1, "ant", 160, 1.6), SNIFF("w:sniffs", 9)], words=[("w:ground!", "GROUND!", .24, .2, 1.1, "sun", (.5, .33), .9)]),
    S("floor", AH, "It has a long, long tongue, too. Flick, flick!", part=1, tag="tongue", hide=["milo"], pcam=AP, pcam2=AP, fx=[LICK("w:Flick,", 7)],
      words=[("w:tongue,", "LONG TONGUE", .28, .22, .9, "sun", (.5, .33), .8)]),
    S("paper", (960, 540, 1500), "Anteaters live on the ground. They do not climb up high.", part=1, tag="board: on the ground", pcam=(960, 440, 1700),
      props=[prop("an", A.anteater, 860, 820, .9, p=(900, 820, .62)), prop("x", lambda p: f'<g id="{p}">{art.cross(p + "x")}</g>', 1320, 300, 1.2, True, p=(1200, 330, 1.0)),
             prop("tr", lambda p: A.tree_icon(p, 760), 1320, 900, .8, p=(1250, 900, .7))],
      fx=[("show", "w:climb", "x"), SNIFF("w:ground.", 5, "an")], words=[("w:ground.", "ON THE GROUND", .3, .14, .9, "sun", (.5, .3), .75)]),
    S("paper_pink", (960, 540, 1500), "Anteaters find food with their super nose.", part=1, tag="board: super nose", pcam=(960, 440, 1700),
      props=[prop("an", A.anteater, 760, 760, .9, p=(860, 760, .62)), prop("nw", A.nose_waves, 1250, 520, 1.2, True, p=(1150, 500, 1.0))],
      fx=[("show", "w:super", "nw"), SNIFF("w:nose.", 5, "an")], words=[("w:super", "SUPER NOSE!", .5, .14, 1.1, "sun", (.5, .3), .85)]),
    S("paper_pink", (960, 540, 1500), "Sniff! They smell ants, and gobble them up.", part=1, tag="board: ants", pcam=(960, 440, 1700),
      props=[prop("an", A.anteater, 760, 760, .9, p=(860, 760, .62)), prop("a0", A.ant, 1200, 790, 1.6, True, p=(1120, 840, 1.1)), prop("a1", A.ant, 1360, 760, 1.6, True, p=(1230, 820, 1.1)),
             prop("a2", A.ant, 1520, 800, 1.6, True, p=(1340, 840, 1.1))],
      fx=[SNIFF("w:Sniff!", 7, "an"), ("show", "w:ants,", "a0"), ("show", "w:ants,", "a1", None, False), ("show", "w:ants,", "a2", None, False), LICK("w:gobble", 5, "an")],
      words=[("w:ants,", "ANTS!", .5, .14, 1.2, "sun", (.5, .3), 1.0)]),
    S("floor", AQ, "Can an anteater smell ants with its nose? Yes, or no?", part=1, q=True, tag="question 1b", pause=3.2, hide=["milo"], pcam=APQ, pcam2=APQ,
      fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0"), SNIFF("wait:2.05", 5)]),
    S("floor", say="Can you sniff like an anteater? Sniff, sniff!", part=1, q=True, tag="sniff", hide=["ant"], fx=[("hop", "w:Sniff,", "milo", 2)],
      words=[("w:Sniff,", "SNIFF, SNIFF!", .74, .22, .85, "sun", (.5, .33), .8)], **MILO("floor", 900)),
    S("paper_blue", LCAM, "That is floor number one. The forest floor!", part=1, tag="board: floor one", pcam=LPCAM, props=tree() + icons((), (3,)),
      fx=[pulse("w:one.", 3), ("show", "w:forest", "i3")]),
    # ---------------------------------------------------------------- PART 2: the understory and the canopy
    S("understory", UW, "Up we go, to floor number two: the understory.", part=2, trans="iris", tag="understory wide", hide=["frog"], cam2=W(UW), pcam=(700, 420, 1500), pcam2=(700, 420, 1600),
      move={"milo": (420, 1000, .7, False, True)}, fx=[("fly", 0.1, "milo", 420, 470, 2.0)], words=[("w:understory.", "THE UNDERSTORY", .5, .14, .9, "sun", (.5, .33), .75)]),
    S("understory", C("understory", "milo", "body", 900), "It is still shady here, under the tall trees.", part=2, tag="shady", hide=["frog"], pcam=V("understory", "milo", "body", 1000),
      words=[("w:shady", "SHADY", .76, .24, 1.1, "", (.5, .33), .9)]),
    S("paper", (960, 540, 1500), "Plants here grow big leaves, to catch the little bits of sunlight.", part=2, tag="board: big leaves", pcam=(960, 440, 1700),
      props=[prop("lf", A.big_leaf, 800, 640, 1.0, p=(960, 700, .9)), prop("r0", lambda p: f'<g id="{p}"><path d="M-10 60 L-250 330" stroke="#f5a623" stroke-width="12" stroke-dasharray="26 22" stroke-linecap="round"/><circle r="70" fill="#ffe066" stroke="#f5a623" stroke-width="10"/></g>', 1380, 420, 1.0, True, p=(1200, 330, .9))],
      fx=[("fromto", "w:big", "#{p}lf_w", {"scale": .6}, {"scale": 1.0, "duration": .6, "ease": "back.out(2)"}, "the leaf grows big"), ("show", "w:sunlight.", "r0")],
      words=[("w:big", "BIG LEAVES", .5, .14, 1.1, "sun", (.5, .3), .9)]),
    S("understory", say="Can you make a big leaf with your hands? Open wide!", part=2, q=True, tag="big hands", hide=["frog"], fx=[("hop", "w:Open", "milo")],
      words=[("w:Open", "OPEN WIDE!", .74, .22, .9, "sun", (.5, .33), .85)], **MILO("understory", 900)),
    S("understory", UQ, "Look, on that big leaf! Who is that?", part=2, q=True, tag="who on the leaf", hide=["milo"], pcam=UPQ, pcam2=UPQ,
      fx=[("fromto", "w:Who", "#{p}frog_w", {"y": FY + 40, "opacity": 0}, {"y": FY, "opacity": 1, "duration": .4, "ease": "back.out(2)"}, "the frog pops up")],
      words=[("w:Who", "?", .8, .3, 2.0, "sun", (.8, .36), 1.3)]),
    S("understory", UC, "A little green tree frog! Ribbit!", part=2, tag="a tree frog", hide=["milo"], pcam=UP, pcam2=UP,
      fx=[PUFF("w:Ribbit!"), ("hop", "w:tree", "frog")], words=[("w:tree", "TREE FROG", .24, .2, 1.0, "pill", (.5, .33), .85)]),
    S("paper_blue", (960, 540, 1500), "The air down here is wet and still.", part=2, tag="board: wet air", pcam=(960, 440, 1700),
      props=[prop(f"d{k}", A.drop, x, y, 1.1, True, p=(px, py, 1.0)) for k, (x, y, px, py) in enumerate(((620, 500, 760, 520), (960, 420, 960, 440), (1300, 520, 1160, 540), (800, 720, 860, 760), (1140, 700, 1060, 780)))],
      fx=[("show", "w:air", "d0"), ("show", "w:down", "d1"), ("show", "w:wet", "d2"), ("show", "w:wet", "d3", None, False), ("show", "w:still.", "d4")],
      words=[("w:wet", "WET AIR", .5, .14, 1.1, "sun", (.5, .3), .95)]),
    S("understory", UQ, "Does a tree frog like wet air, or dry air?", part=2, q=True, tag="question 2", pause=3.2, hide=["milo"], pcam=UPQ, pcam2=UPQ,
      fx=[("signs", "w:wet", ["WET", "DRY"], 0, "wait:2.0"), ("hop", "wait:2.05", "frog")]),
    S("understory", UH, "Wet air! It keeps the frog's skin nice and wet.", part=2, tag="wet skin", hide=["milo"], pcam=UP, pcam2=UP,
      props=[prop("d0", A.drop, FX - 100, 470, .5, True), prop("d1", A.drop, FX + 110, 490, .45, True)],
      fx=[("show", "w:skin", "d0"), ("show", "w:skin", "d1", None, False), ("face", 0.05, "frog", "happy"), PUFF("w:Wet")],
      words=[("w:Wet", "WET!", .2, .26, 1.1, "sun", (.5, .33), .9)]),
    S("understory", UH, "Count the drops with me. One, two, three!", part=2, q=True, tag="count drops", hide=["milo"], pcam=UP, pcam2=UP,
      props=[prop("d0", A.drop, FX - 120, 480, .45, True), prop("d1", A.drop, FX, 420, .45, True), prop("d2", A.drop, FX + 120, 480, .45, True)],
      fx=[("show", "w:One,", "d0"), ("show", "w:two,", "d1"), ("show", "w:three!", "d2")],
      words=[("w:One,", "1", .2, .3, 1.2, "sun", (.25, .36), 1.0), ("w:two,", "2", .5, .14, 1.2, "sun", (.5, .3), 1.0), ("w:three!", "3", .8, .3, 1.2, "sun", (.75, .36), 1.0)]),
    S("understory", say="Can you hop like a tree frog? Hop, hop!", part=2, q=True, tag="hop", hide=["frog"], fx=[("hop", "w:Hop,", "milo", 2)],
      words=[("w:Hop,", "HOP, HOP!", .74, .22, .95, "sun", (.5, .33), .85)], **MILO("understory", 900)),
    S("canopy", MW, "Up, up, to floor number three: the canopy!", part=2, trans="iris", tag="canopy wide", cam2=(980, 370, 1700), pcam=MPW, pcam2=MPW,
      fx=[("fromto", 0, "#{p}milo_w", {"x": -300, "y": 760}, {"x": 420, "y": 300, "duration": 1.4, "ease": "power2.out"}, "Milo flies in")],
      words=[("w:canopy!", "THE CANOPY", .5, .62, 1.0, "sun", (.5, .33), .85)]),
    S("canopy", MC, "Mango lives up here! Hello again, Mango!", part=2, tag="Mango's floor", hide=["milo"], pcam=MP, fx=[("hop", "w:Hello", "mango"), ("arm", "w:Hello", "mango", "r", -70), ("face", 0.05, "mango", "happy")],
      words=[("w:here!", "HELLO!", .2, .3, 1.1, "sun", (.5, .33), .9)]),
    S("paper", (960, 540, 1500), "The canopy is a thick roof of leaves, high in the trees.", part=2, tag="board: roof of leaves", pcam=(960, 420, 1700),
      props=[prop("lr", A.leaf_roof, 960, 620, .82, p=(960, 560, .7))],
      fx=[("fromto", "w:roof", "#{p}lr-roof", {"y": -120, "opacity": 0}, {"y": 0, "opacity": 1, "duration": .5, "ease": "back.out(2)"}, "the roof of leaves drops in")],
      words=[("w:roof", "A LEAF ROOF", .82, .14, .9, "sun", (.5, .3), .8)]),
    S("paper", (960, 540, 1500), "Above the roof, it is sunny. Under it, shady.", part=2, tag="board: above and under", pcam=(960, 420, 1700),
      props=[prop("lr", A.leaf_roof, 960, 620, .82, p=(960, 560, .7))],
      fx=[("to", "w:sunny.", "#{p}lr-sun", {"scale": 1.15, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 3}, "the sun shines"),
          ("to", "w:shady.", "#{p}lr-r0,#{p}lr-r1,#{p}lr-r2", {"opacity": .2, "duration": .4}, "the light gets thin")],
      words=[("w:sunny.", "SUNNY", .2, .16, 1.0, "sun", (.3, .3), .8), ("w:shady.", "SHADY", .8, .7, 1.0, "", (.7, .72), .8)]),
    S("canopy", MH, "Spider monkeys pick fruit up here. Munch, munch!", part=2, tag="Mango picks fruit", hide=["milo"], pcam=MPH,
      props=[prop("fr", art2.fruit, MX + 130, 283, .34)],
      fx=[("arm", 0, "mango", "r", -80), ("to", "w:Munch,", "#{p}fr_w", {"x": MX, "y": 286, "scale": .3, "opacity": 0, "duration": .45, "ease": "power2.in"}, "Mango eats the fruit"),
          ("arm", "w:munch!", "mango", "r", 0), ("to", "w:Munch,", "#{p}mango-jaw", {"opacity": 1, "y": 12, "duration": .16, "yoyo": True, "repeat": 9}, "Mango munches")],
      words=[("w:fruit", "FRUIT!", .82, .3, 1.0, "sun", (.5, .33), .9)]),
    S("canopy", (1240, 300, 1300), "And look! A macaw, with a big, strong beak.", part=2, tag="a macaw", hide=["milo"], pcam=(1310, 230, 1200), actors=[("mango", "monkey", MX, MY, MS), ("mac", "macaw", 1500, MY, .7)],
      fx=[("fromto", 0.05, "#{p}mac_w", {"x": 2300, "y": 100}, {"x": 1500, "y": MY, "duration": 1.2, "ease": "power2.out"}, "the macaw flies in"),
          ("to", 0.05, "#{p}mac-wing", {"rotation": -40, "svgOrigin": "-40 -200", "duration": .15, "yoyo": True, "repeat": 7}, "")],
      words=[("w:beak.", "BIG BEAK!", .3, .2, 1.0, "sun", (.5, .33), .9)]),
    S("canopy", (1300, 170, 1500), "What does the macaw grab with its big beak? Fruit, or rocks?", part=2, q=True, tag="question 3", pause=3.2, hide=["milo"],
      pcam=(1300, 160, 1500), actors=[("mango", "monkey", MX, MY, MS), ("mac", "macaw", 1500, MY, .7)],
      props=[prop("fr", art2.fruit, 1650, 300, .3, True)], fx=[("signs", "w:Fruit,", ["FRUIT", "ROCKS"], 0, "wait:2.0"), ("show", "wait:2.0", "fr")]),
    S("canopy", (1480, 280, 900), "Fruit! The macaw grabs fruit in the canopy.", part=2, tag="macaw fruit", hide=["milo"], pcam=(1480, 260, 900), actors=[("mac", "macaw", 1500, MY, .7)],
      props=[prop("fr", art2.fruit, 1600, 268, .26)], fx=[("to", "w:grabs", "#{p}mac-jaw", {"rotation": 16, "svgOrigin": "92 -232", "duration": .15, "yoyo": True, "repeat": 5}, "the macaw bites")],
      words=[("w:Fruit!", "FRUIT!", .25, .24, 1.1, "sun", (.5, .33), .9)]),
    S("canopy", say="Flap your wings like a macaw! Flap, flap!", part=2, q=True, tag="flap", hide=["mango"], fx=[("hop", "w:Flap,", "milo", 2)],
      words=[("w:Flap,", "FLAP, FLAP!", .74, .22, .9, "sun", (.5, .33), .85)], **MILO("canopy")),
    S("paper_blue", LCAM, "Floor two, the understory. Floor three, the canopy.", part=2, tag="board: floors two and three", pcam=LPCAM, props=tree() + icons((3,), (2, 1)),
      fx=[pulse("w:two,", 2), ("show", "w:understory.", "i2"), pulse("w:three,", 1), ("show", "w:canopy.", "i1")]),
    # ---------------------------------------------------------------- PART 3: the emergent layer
    S("emergent", MW, "Now, the very top! Floor number four: the emergent layer.", part=3, trans="iris", tag="emergent wide", hide=["eagle"], cam2=(980, 370, 1700), pcam=(600, 180, 1300), pcam2=(600, 170, 1360),
      fx=[("fromto", 0, "#{p}milo_w", {"x": -300, "y": 760}, {"x": 420, "y": 300, "duration": 1.4, "ease": "power2.out"}, "Milo flies up out of the treetops")],
      words=[("w:emergent", "THE EMERGENT LAYER", .5, .62, .85, "sun", (.5, .33), .65)]),
    S("emergent", (960, 300, 1900), "Look! A few trees grow taller than all the rest.", part=3, tag="taller trees", hide=["eagle"], cam2=(960, 260, 2000), pcam=(1450, 40, 1300), pcam2=(1450, 30, 1360),
      props=[prop("a0", lambda p: art.arrow(p, 260, -130, 260, 0), 0, 0, 1, True), prop("a1", lambda p: art.arrow(p, 1560, -60, 1560, 70), 0, 0, 1, True)],
      fx=[("show", "w:few", "a0"), ("show", "w:taller", "a1")], words=[("w:taller", "TALLER!", .5, .14, 1.0, "sun", (.5, .33), .9)]),
    S("paper", (960, 520, 1500), "Short, short, short, and one tall tree sticks up!", part=3, tag="board: one tall tree", pcam=(960, 420, 1700),
      props=[prop("t0", lambda p: A.tree_icon(p, 500), 560, 900, 1.0, p=(660, 820, .75)), prop("t1", lambda p: A.tree_icon(p, 520, "#57c078"), 800, 900, 1.0, p=(860, 820, .75)),
             prop("t2", lambda p: A.tree_icon(p, 500), 1040, 900, 1.0, p=(1060, 820, .75)), prop("t3", lambda p: A.tree_icon(p, 740, "#3f9e5c"), 1300, 900, 1.0, p=(1260, 820, .75))],
      fx=[("to", "w:Short,", "#{p}t0_w", {"y": "-=20", "duration": .15, "yoyo": True, "repeat": 1}, "a tree bobs"), ("to", "w:short,", "#{p}t1_w", {"y": "-=20", "duration": .15, "yoyo": True, "repeat": 1}, "a tree bobs"),
          ("to", "w:short,:2", "#{p}t2_w", {"y": "-=20", "duration": .15, "yoyo": True, "repeat": 1}, "a tree bobs"),
          ("fromto", "w:tall", "#{p}t3_w", {"scaleY": 0, "transformOrigin": "50% 100%"}, {"scaleY": 1, "duration": .6, "ease": "back.out(1.6)"}, "the tall tree grows up")],
      words=[("w:tall", "SO TALL!", .76, .14, 1.0, "sun", (.5, .3), .9)]),
    S("paper", (960, 520, 1500), "Count the short trees with me. One, two, three!", part=3, q=True, tag="board: count trees", pcam=(960, 420, 1700),
      props=[prop("t0", lambda p: A.tree_icon(p, 500), 560, 900, 1.0, p=(660, 820, .75)), prop("t1", lambda p: A.tree_icon(p, 520, "#57c078"), 800, 900, 1.0, p=(860, 820, .75)),
             prop("t2", lambda p: A.tree_icon(p, 500), 1040, 900, 1.0, p=(1060, 820, .75)), prop("t3", lambda p: A.tree_icon(p, 740, "#3f9e5c"), 1300, 900, 1.0, p=(1260, 820, .75))],
      words=[("w:One,", "1", .233, .2, 1.3, "sun", (.27, .36), 1.0), ("w:two,", "2", .393, .2, 1.3, "sun", (.43, .36), 1.0), ("w:three!", "3", .553, .2, 1.3, "sun", (.59, .36), 1.0)]),
    S("emergent", EQ, "Is it dark up here, or sunny?", part=3, q=True, tag="question 4", pause=3.2, hide=["eagle"], pcam=(MX, 60, 1400), pcam2=(MX, 60, 1400),
      actors=[("milo", "milo", MX, MY, .62)], fx=[("signs", "w:dark", ["DARK", "SUNNY"], 1, "wait:2.0"), ("hop", "wait:2.05", "milo")]),
    S("emergent", (1400, 120, 1300), "Sunny! It is the sunniest layer of all.", part=3, tag="sunniest", hide=["eagle"], pcam=(1500, 60, 1300),
      fx=[("to", "w:sunniest", "#{p}sun", {"scale": 1.15, "transformOrigin": "1640px -60px", "duration": .3, "yoyo": True, "repeat": 5}, "the sun shines")],
      words=[("w:sunniest", "THE SUNNIEST!", .3, .3, .9, "sun", (.5, .33), .8)]),
    S("emergent", say="Shade your eyes from the sun, like this!", part=3, q=True, tag="shade your eyes", hide=["eagle"],
      fx=[("to", "w:Shade", "#{p}milo-wr", {"rotation": -70, "svgOrigin": "96 -182", "duration": .3}, "Milo shades his eyes"), ("hop", "w:this!", "milo")],
      words=[("w:Shade", "SHADE YOUR EYES!", .74, .22, .75, "sun", (.5, .33), .65)], **MILO("emergent")),
    S("emergent", MW, "Who lives up here, at the very top? Look who is coming!", part=3, q=True, tag="who is coming", hide=["milo"], cam2=(980, 370, 1700), pcam=EPW, pcam2=EPW,
      fx=[("fromto", "w:Look", "#{p}eagle_w", {"x": 2400, "y": -300}, {"x": MX, "y": MY, "duration": 1.6, "ease": "power2.out"}, "a big bird flies in")] + FLAP("w:Look", n=9),
      words=[("w:top?", "?", .82, .3, 2.0, "sun", (.8, .36), 1.3)]),
    S("emergent", EC, "A harpy eagle! It is a very big bird.", part=3, tag="a harpy eagle", hide=["milo"], pcam=EP_, pcam2=EP_,
      fx=FLAP("w:big", n=3) + [("face", 0.05, "eagle", "happy")], words=[("w:harpy", "HARPY EAGLE", .24, .2, .9, "pill", (.5, .33), .8)]),
    S("emergent", EH, "Flap, flap, flap! Look at its big, wide wings.", part=3, tag="big wings", hide=["milo"], pcam=EP_, pcam2=EP_, fx=FLAP("w:Flap,", n=9),
      words=[("w:wide", "BIG WINGS!", .24, .2, 1.0, "sun", (.5, .33), .9)]),
    S("emergent", (960, 700, 1500), "Look down! The forest floor is far, far below.", part=3, tag="look down", hide=["eagle"], move={"milo": (720, 600, .62, False, True)}, pcam=(960, 640, 1500),
      props=[prop("ar", lambda p: art.arrow(p, 1300, 500, 1300, 900), 0, 0, 1, True)], fx=[("show", "w:down!", "ar")],
      words=[("w:far,", "FAR BELOW!", .3, .74, 1.0, "sun", (.5, .74), .9)]),
    S("paper_blue", (960, 540, 1500), "Many animals up here fly, or glide, from tree to tree.", part=3, tag="board: fly or glide", pcam=(960, 440, 1700),
      props=[prop("t0", lambda p: A.tree_icon(p, 480), 560, 940, 1.0, p=(660, 860, .8)), prop("t1", lambda p: A.tree_icon(p, 480, "#57c078"), 1160, 940, 1.0, p=(1260, 860, .8)),
             prop("ea", A.eagle, 560, 462, .4, p=(660, 470, .34)), prop("ar", lambda p: art.arrow(p, 700, 300, 1020, 300), 0, 0, 1, True, p=(0, 0, 1))],
      fx=[("show", "w:fly,", "ar"), ("to", "w:fly,", "#{p}ea_w", {"x": "+=600", "duration": 2.4, "ease": "power1.inOut"}, "the eagle flies to the other tree")],
      words=[("w:fly,", "FLY!", .4, .62, 1.2, "sun", (.36, .62), 1.0), ("w:glide,", "GLIDE!", .62, .74, 1.2, "", (.64, .7), 1.0)]),
    S("emergent", (900, 240, 1300), "And butterflies flutter up here, too.", part=3, tag="butterflies", hide=["milo", "eagle"], pcam=(800, 140, 1300),
      props=[BFLY("b0", 560, 120, .8), BFLY("b1", 760, 300, .6), BFLY("b2", 520, 330, .55)],
      fx=FLUT(0.05, "b0", 260, -40) + FLUT(0.05, "b1", 200, -90) + FLUT(0.05, "b2", 300, 30), words=[("w:butterflies", "BUTTERFLIES", .5, .14, .9, "sun", (.5, .33), .8)]),
    S("emergent", (900, 240, 1300), "Count the butterflies. One, two, three!", part=3, q=True, tag="count butterflies", hide=["milo", "eagle"], pcam=(800, 140, 1300),
      props=[BFLY("b0", 760, 80, .8, True), BFLY("b1", 960, 260, .6, True), BFLY("b2", 680, 360, .55, True)],
      fx=[("show", "w:One,", "b0"), ("show", "w:two,", "b1"), ("show", "w:three!", "b2")] + FLUT("w:One,", "b0", 160, -20, 2.4) + FLUT("w:two,", "b1", 140, -40, 2.0) + FLUT("w:three!", "b2", 160, 20, 1.6),
      words=[("w:three!", "3", .8, .3, 1.4, "sun", (.75, .5), 1.1)]),
    S("emergent", say="Can you flutter like a butterfly? Flutter, flutter!", part=3, q=True, tag="flutter", hide=["eagle"], pause=.8,
      props=[BFLY("b0", 640, 200, .5)], fx=FLUT(0.05, "b0", 120, -30) + [("hop", "w:Flutter,", "milo", 2)],
      words=[("w:Flutter,", "FLUTTER!", .74, .22, 1.0, "sun", (.5, .33), .9)], **MILO("emergent")),
    S("emergent", EQ, "Who lives at the very top? The anteater, or the eagle?", part=3, q=True, tag="question 5", pause=3.2, hide=["milo"], pcam=EPQ, pcam2=EPQ,
      fx=[("signs", "w:anteater,", ["ANTEATER", "EAGLE"], 1, "wait:2.0")] + FLAP("wait:2.05", n=3)),
    S("emergent", EC, "The eagle! The anteater stays down on the forest floor.", part=3, tag="the eagle", hide=["milo"], pcam=EP_, pcam2=EP_,
      fx=FLAP("w:eagle!", n=3), words=[("w:eagle!", "EAGLE!", .24, .2, 1.1, "sun", (.5, .33), .9)]),
    S("paper_blue", LCAM, "Let's fly back down. Four, three, two, one!", part=3, q=True, tag="board: count down", pcam=LPCAM, props=tree() + icons((0, 1, 2, 3)),
      fx=[pulse("w:Four,", 0, 1), pulse("w:three,", 1, 1), pulse("w:two,", 2, 1), pulse("w:one!", 3, 1)]),
    S("paper_blue", LCAM, "Eagle, macaw, frog and anteater. Everyone has a home!", part=3, tag="board: everyone has a home", pcam=LPCAM, props=tree() + icons((0, 1, 2, 3)),
      fx=[("to", "w:Eagle,", "#{p}i0_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, "the eagle picture"), ("to", "w:macaw,", "#{p}i1_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, "the macaw picture"),
          ("to", "w:frog", "#{p}i2_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, "the frog picture"), ("to", "w:anteater.", "#{p}i3_w", {"scale": 1.2, "duration": .2, "yoyo": True, "repeat": 1}, "the anteater picture")],
      words=[("w:Everyone", "A HOME FOR ALL!", .5, .05, .7, "pill", (.5, .3), .7)]),
    S("emergent", say="Which floor would you like to live on?", part=3, q=True, tag="your floor", hide=["eagle"], pause=2.0, fx=[("hop", "w:Which", "milo")],
      words=[("w:floor", "WHICH FLOOR?", .74, .22, .85, "sun", (.5, .33), .8)], **MILO("emergent")),
    # ---------------------------------------------------------------- QUIZ + RECAP
    S("canopy", MW, "Time to remember what we learned!", part=4, trans="iris", tag="quiz time", cam2=(980, 370, 1700), pcam=MPW, words=[("w:remember", "QUIZ TIME!", .5, .62, 1.3, "sun", (.5, .33))]),
    S("canopy", QC, "How many layers does a rainforest have? Two, or four?", part=4, q=True, tag="quiz 1", pause=3.2, hide=["milo"], pcam=MPQ, fx=[("signs", "w:Two,", ["TWO", "FOUR"], 1, "wait:2.0")]),
    S("paper_blue", LCAM, "Four! Floor, understory, canopy, and the emergent layer.", part=4, tag="board: four again", pcam=LPCAM, props=tree() + icons((0, 1, 2, 3)),
      fx=[pulse("w:Floor,", 3, 1), pulse("w:understory,", 2, 1), pulse("w:canopy,", 1, 1), pulse("w:emergent", 0, 1)]),
    S("floor", AQ, "Which layer is the darkest? The forest floor, or the top?", part=4, q=True, tag="quiz 2", pause=3.2, hide=["milo"], pcam=APQ, trans="iris",
      fx=[("signs", "w:forest", ["FLOOR", "TOP"], 0, "wait:2.0")]),
    S("paper", (960, 540, 1500), "The forest floor! The leaves up high block the sun.", part=4, tag="board: leaf roof again", pcam=(960, 420, 1700),
      props=[prop("lr", A.leaf_roof, 960, 620, .82, p=(960, 560, .7))], fx=[("to", 0.1, "#{p}lr-r0,#{p}lr-r1,#{p}lr-r2", {"opacity": .25, "duration": .5}, "the light gets thin")],
      words=[("w:forest", "THE FLOOR!", .82, .2, .95, "sun", (.5, .3), .85)]),
    S("emergent", EC, "Who lives way up at the top?", part=4, q=True, tag="quiz 3", pause=1.6, hide=["milo", "eagle"], pcam=EP_, trans="iris",
      words=[("end+0.3", "?", .5, .3, 2.4, "sun", (.5, .36), 1.5)]),
    S("emergent", EC, "The harpy eagle, in the sunny emergent layer!", part=4, tag="the eagle again", hide=["milo"], pcam=EP_,
      fx=FLAP("w:harpy", n=3), words=[("w:harpy", "HARPY EAGLE!", .24, .2, .85, "sun", (.5, .33), .75)]),
    S("emergent", MW, "Thank you for learning with me, friends. See you at the zoo!", part=4, tag="goodbye", cam2=(960, 380, 1900), pcam=EPW,
      words=[("w:See", "SEE YOU AT THE ZOO!", .5, .62, .95, "pill", (.5, .33), .62)], fx=[("hop", "w:zoo!", "milo", 2)] + FLAP("w:See", n=3)),
]
for _s in SHOTS:        # a picture board never drifts closer in 9:16: it only pulls out a little
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)      # and in 16:9 (the layer tree's numbers were cut by a push-in in the first stills)

SHORTS = [
    {"id": "zc_ep08_short1", "title": "Who Lives on the Rainforest Floor?", "band": ("WHO LIVES", "DOWN HERE?"), "thumb_text": "SNIFF, SNIFF!", "part": 1,
     "extra_first": [S("floor", AC, "Who lives way down, on the dark forest floor?", part=1, q=True, tag="hook: who lives down here", hide=["milo"], pcam=AP, pcam2=AP,
                       fx=[SNIFF(0.3, 9)], words=[("w:Who", "?", .24, .2, 2.2, "sun", (.5, .33), 1.3)])]},
    {"id": "zc_ep08_short2", "title": "Who Lives in the Middle of the Rainforest?", "band": ("FLOORS TWO", "AND THREE!"), "thumb_text": "BIG LEAVES!", "part": 2,
     "extra_first": [S("understory", UC, "Who lives in the middle of the rainforest?", part=2, q=True, tag="hook: the middle floors", hide=["milo"], pcam=UP, pcam2=UP,
                       fx=[PUFF(0.4)], words=[("w:middle", "?", .24, .2, 2.2, "sun", (.5, .33), 1.3)])]},
    {"id": "zc_ep08_short3", "title": "What Lives Above the Rainforest Treetops?", "band": ("WHO LIVES", "UP HIGH?"), "thumb_text": "SO SUNNY!", "part": 3,
     "extra_first": [S("emergent", EC, "What lives up above the treetops?", part=3, q=True, tag="hook: above the treetops", hide=["milo"], pcam=EP_, pcam2=EP_,
                       fx=FLAP(0.3, n=5), words=[("w:above", "?", .24, .2, 2.2, "sun", (.5, .33), 1.3)])]},
]

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
THUMBS = {
    "zc_ep08": {"place": "paper_blue", "cam": (1150, 560, 2300), "actors": [],
                "props": [(A.layer_tree, 820, 560, .9), (A.icon(A.eagle_icon), 1460, 560 - 315 * .9, .8), (A.icon(A.anteater_icon), 1460, 560 + 315 * .9, .8)],
                "words": [("WAY UP", 1600, 450, 140, ""), ("HIGH!", 1600, 640, 190, "sun")]},
    "zc_ep08_short1": {"place": "floor", "cam": (1080, 640, 1100), "actors": [("anteater", AX, AY, AS, False, 'gsap.set("#P-jaw",{opacity:1});')],
                       "props": [(A.nose_waves, 1330, 640, .8)],
                       "words": [("SNIFF,", 540, 420, 190, ""), ("SNIFF!", 540, 620, 210, "sun")]},
    "zc_ep08_short2": {"place": "understory", "cam": (FX, 520, 760), "actors": [("frog", FX, FY, FS, False, "")],
                       "props": [], "words": [("BIG", 540, 400, 200, ""), ("LEAVES!", 540, 600, 200, "sun")]},
    "zc_ep08_short3": {"place": "emergent", "cam": (1200, 160, 1200), "actors": [("eagle", MX, MY, MS, False, "")],
                       "props": [], "words": [("SO", 540, 420, 200, ""), ("SUNNY!", 540, 620, 210, "sun")]},
}
