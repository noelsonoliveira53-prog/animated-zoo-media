"""zc_ep12: "Whose Ears Are These? Guess With Milo" - the second Guess With Milo episode (2D, docs/CARTOON_RUN.md "Guess With Milo",
"VIRAL PACKAGING", "MAIN INTRO"), a cartoon fact lesson with the 3D music-and-sync process ("beat"). Cold open on two grey ears poking out of
tall grass, each turning a different way; Milo says his name after the hook; the main intro right after the hook and again as the last shots.
Three parts, each cut whole into one Short, each opening on its own pair of ears above a hiding place with two answer signs and thinking time
BEFORE the animal is shown:
1. rhino (each ear moves on its own: one forward, one back; both perk straight up for an interesting sound; can't see very well, hears very well),
2. fennec fox (a little fox with giant ears; ears can be half as long as its body; ears listen for food under the sand, then it digs with all four
   feet; big ears let extra heat out in the hot desert),
3. polar bear (small, round ears and a short tail keep the warmth in, in the cold Arctic).
Quiz with the three pairs of ears, recap, the closing names the next Guess With Milo ("Whose Egg Is This?").
The build plan offered rhino, fox and koala "or the three whose ear facts the build day's sources confirm": the koala was replaced by the polar
bear (its small ears are the opposite of the fox's big ones, and the Poppy rig exists); the elephant was left out because zc_ep03 "Why Do
Elephants Have Such Big Ears?" is already on the channel.

FACTS, read at the source on Nov 21 2026, about 2:05-2:35 AM ET (pages read by the session's page reader, which quotes the sentences it finds;
every page below loaded):
 [SDZ-R] San Diego Zoo Wildlife Alliance, Animals and Plants, Rhinoceros (animals.sandiegozoo.org/animals/rhinoceros, also node/109)
   "Their ears can move independently of each other, and one may be cocked forward while the other is directed backward,"
   "or both may perk straight up when an interesting sound that requires total concentration is detected."
   "poor eyesight, excellent hearing, and a habit of rolling in the mud."
 [SDZ-WR] SDZWA Library, White rhino, Physical Characteristics (ielc.libguides.com/sdzg/factsheets/whiterhino/characteristics)
   "Hair fringes on the ears and tip of the tail"   "Good sense of hearing"
 [SDZ-BR] SDZWA Library, Black rhino, Behavior: "Ears straight up" - "Indicates interest or curious"
 [SDZ-F] SDZWA Library, Fennec fox, Physical Characteristics (ielc.libguides.com/sdzg/factsheets/fennec-fox/characteristics)
   "The fennec fox is the smallest canid but has the largest ears, relative to body size."
   "Largest ears of any canid (fox, dog, or wolf), relative to body size"   "Excellent hearing"   "Likely help to dissipate heat and locate prey"
 [SDZ-FA] SDZWA, Animals and Plants, Fennec fox (animals.sandiegozoo.org/animals/fennec-fox)
   "Fennec foxes' ears can be half as long as their body."
   "A fennec fox's large ears not only help it listen for prey underground, but also dissipate excess heat."
   "Those ears not only help them listen for prey underground, but also serve to dissipate excess heat of the desert."
   "They enjoy insects, rodents, snails, lizards, plants, fruits, roots, and eggs."   "They even have fur on their feet ..."
 [NZ-F] Smithsonian's National Zoo, Fennec fox (nationalzoo.si.edu/animals/fennec-fox)
   "fennec foxes use their abnormally large ears to listen for prey underneath the sand," "once located will dig with all four feet to expose their meal."
   "In the wild, fennec foxes eat insects—particularly grasshoppers and locusts—"
 [PBI] Polar Bears International, Adaptation (polarbearsinternational.org/polar-bears/adaptation)
   "Polar bear ears are small and round, and their tails short and compact," "to prevent heat loss and conserve the most warmth possible."
 [SW] SeaWorld, Polar bear characteristics: "The ears are small compared to those of other bears - an adaptation that enables them to conserve body heat."
   "The tail is small, about 7 to 12 cm (2.8-4.7 in.) long."
 [SDZ-PB] SDZWA Library, Polar bear, Physical Characteristics: "Ears relatively small"
 Said as: a rhino can move each ear on its own [SDZ-R]; one ear can point forward while the other points back [SDZ-R]; when it hears something
 interesting, both ears perk straight up [SDZ-R, SDZ-BR]; its ears have a little fringe of hair [SDZ-WR, white rhino; the drawn rhino is a white-rhino
 shape: wide square mouth not drawn, kept general]; a rhino can't see very well, but it hears very well [SDZ-R]; a fennec fox is a little fox with
 giant ears [SDZ-F]; its ears can be half as long as its body [SDZ-FA]; its ears listen for food hiding under the sand, like a little beetle
 [SDZ-FA, NZ-F; insects: SDZ-FA, NZ-F]; then it digs with all four feet [NZ-F]; big ears let extra heat out and help it stay cool in the hot desert
 [SDZ-FA "dissipate excess heat of the desert"]; a polar bear has small, round ears [PBI, SW, SDZ-PB]; small ears help keep the warmth in, in the
 cold Arctic [PBI, SW]; it has a short little tail that helps keep the warmth in too [PBI, SW].
 Read but NOT said: ear lengths in inches, the oxpecker bird in the rhino's ears, burrow lengths, panting, polar bear fur and fat (another lesson's topic).
 Nobody is hurt, lost, crying or trapped; the animals are only hiding for the game and come out happily; the food under the sand is a small
 beetle that is only heard, not caught on screen.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_zc_ep11 as A11
import art_zc_ep12 as A
from kit import Kit, S, prop, W
from intro import INTRO_STAGES, intro_shots

EP = {"id": "zc_ep12", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "Whose Ears Are These? Guess With Milo", "thumb_text": "LISTEN!", "series": "Guess With Milo",
      "description": ("Look! Two ears in the grass, and they are turning different ways! Who is it? Look at the ears with Milo the bluebird and guess the animal "
                      "before it comes out! A gentle guessing game for ages 2-6 with answer signs, thinking time, moves to copy and a quiz at the end.\n"
                      "Kids learn that a rhino can move each ear on its own, one forward and one back, and that both ears perk straight up when it hears "
                      "something interesting; that a fennec fox is a little fox with giant ears that listen for food under the sand and let extra heat out in "
                      "the hot desert; and that a polar bear's small, round ears and short tail help keep the warmth in.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (rhinoceros and fennec fox) and its Library fact sheets (white rhino, black rhino, "
                      "fennec fox, polar bear); Smithsonian's National Zoo (fennec fox); Polar Bears International (adaptations); SeaWorld (polar bear)."),
      "tags": ["whose ears are these", "guess with milo", "guess the animal", "animal ears for kids", "rhino ears", "fennec fox", "polar bear ears",
               "animal facts for kids", "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "savanna": [("rhi", "rhino", 1000, 930, .78), ("milo", "milo", 300, 520, .72, False, True)],
    "dunes": [("fox", "fennec", 1000, 930, 1.15), ("milo", "milo", 300, 520, .72, False, True)],
    "arctic": [("bear", "bear", 1000, 930, 1.0), ("milo", "milo", 300, 520, .72, False, True)],
    "zoo": [("milo", "milo", 960, 940, 1.1)],
    "zoo_eve": [("milo", "milo", 960, 940, 1.0)],
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
MILO = lambda place, w=760: dict(cam=C(place, "milo", "body", w), pcam=V(place, "milo", "body", 1100, 0, -90))
BOARD = (960, 540, 1500); BOARDP = (960, 440, 1700); BOARD2 = (960, 600, 1300)


def PULSE(at, sel, k=1.2, n=1, o="50% 50%"): return ("to", at, sel, {"scale": k, "transformOrigin": o, "duration": .2, "yoyo": True, "repeat": 2 * n - 1}, "")


# ears: (at, who, which, degrees, seconds) - the ear turns round its own base and HOLDS there (a later EAR moves it again)
EAR_O = {("rhino", "ear"): "262 -436", ("rhino", "ear2"): "214 -446", ("fennec", "ear"): "128 -256", ("fennec", "ear2"): "176 -262", ("bear", "ear"): "150 -402"}
def EAR(at, who, kind, which, deg, d=.35):
    return ("to", at, f"#{{p}}{who}-{which}", {"rotation": deg, "svgOrigin": EAR_O[(kind, which)], "duration": d, "ease": "back.out(2)"},
            f"the {kind}'s {'near' if which == 'ear' else 'far'} ear turns {'forward' if deg > 0 else 'back' if deg < 0 else 'up'}")
def PERK(at, who, kind):        # both ears straight up with a little stretch (an interesting sound)
    return [("to", at, f"#{{p}}{who}-{w}", {"rotation": 0, "scaleY": 1.18, "svgOrigin": EAR_O[(kind, w)], "duration": .25, "ease": "back.out(3)"}, "both ears perk straight up" if w == "ear" else "")
            for w in ("ear", "ear2")]
def NOFLICK(who): return ("face", 0.05, who, "happy")      # a "face" fx turns the engine's idle ear flick off for this actor in this shot
def WIGGLE(at, who, kind, n=2):  # both ears twitch together (a listening look)
    return [("to", at, f"#{{p}}{who}-{w}", {"rotation": 10, "svgOrigin": EAR_O[(kind, w)], "duration": .16, "yoyo": True, "repeat": 2 * n - 1, "ease": "sine.inOut"}, "the ears twitch" if w == "ear" else "")
            for w in ("ear", "ear2") if (kind, w) in EAR_O]


# ------------------------------------------------------------------ the hiding places: drawn IN FRONT of the actors, so only the ears show
GRASS = lambda s=1.0, hid=False: prop("gr", lambda q: A.grass_tall(q, 2600, 530), 1000, 985, s, hid, p=(1000, 985, s))
DUNE = lambda: prop("du", lambda q: A.dune_mound(q, 1500, 530), 1150, 995, 1.0, p=(1150, 995, 1.0))
SNOW = lambda: prop("sn", lambda q: A.snow_bank(q, 1600, 470), 1000, 990, 1.0, p=(1000, 990, 1.0))
def SINK(at, name, dy=1500): return ("to", at, f"#{{p}}{name}_w", {"y": f"+={dy}", "duration": .8, "ease": "power2.in"}, "the hiding place sinks away")
# cameras on the ears above the hiding places (16:9, 9:16)
RE = (1190, 545, 700); REP = (1190, 560, 900)                       # rhino ears above the grass
FE = (1170, 540, 900); FEP = (1170, 520, 1000)                      # fox ears above the dune
BE = (1200, 560, 900); BEP = (1200, 520, 1000)                       # bear ears above the snow
RQ = (1190, 520, 1000); RQP = (1190, 470, 1200)                      # the question: ears low, the signs above
FQ = (1170, 500, 1300); FQP = (1170, 430, 1400)
BQ = (1200, 520, 1200); BQP = (1200, 430, 1300)
QM = lambda x=1480, y=860, s=.8, hid=False: prop("qm", A11.qmark, x, y, s, hid, p=(1240, 640, .7))

# ------------------------------------------------------------------ cameras on the animals
RB = C("savanna", "rhi", "body", 1250, 40, -80); RBP = WV("savanna", ["rhi"], floor=.72, top=.44, pad=.08)
RH = C("savanna", "rhi", "head", 900, -40, -10); RHP = V("savanna", "rhi", "head", 1300, -60, -60)
FB = C("dunes", "fox", "all", 1150, 20, -40); FBP = WV("dunes", ["fox"], floor=.72, top=.42, pad=.1)
FH = C("dunes", "fox", "head", 900, -30, -80); FHP = V("dunes", "fox", "head", 1300, -40, -60)
BB = C("arctic", "bear", "all", 1150, 40, -40); BBP = WV("arctic", ["bear"], floor=.72, top=.44, pad=.1)
BH = C("arctic", "bear", "head", 800, -60, -30); BHP = V("arctic", "bear", "head", 1200, -60, -40)
BT = C("arctic", "bear", "tail", 1000, 150, -60); BTP = V("arctic", "bear", "tail", 1000, 120, 40)

# picture boards
FFACE = lambda name="ff", x=960, y=640, s=.85, p=(960, 700, 1.05): prop(name, A.fox_face, x, y, s, p=p)
SCUT = lambda name="sc", x=960, y=600, s=.95, p=(960, 640, .78): prop(name, A.sand_cut, x, y, s, p=p)
EPAIR = lambda name="ep", x=960, y=640, s=1.0, p=(960, 700, .82): prop(name, A.ear_pair, x, y, s, p=p)
RINGS = lambda name, x, y, s=1.0, flip=False, hid=True, p=None: prop(name, lambda q: A.sound_rings(q, flip=flip), x, y, s, hid, p=p or (x, y, s))
ARROW = lambda name, x, y, back=False, s=1.0, p=None: prop(name, lambda q: A.turn_arrow(q, back=back), x, y, s, True, p=p or (x, y, s))
def RINGPULSE(at, name): return ("to", at, f"#{{p}}{name}-a0,#{{p}}{name}-a1,#{{p}}{name}-a2", {"opacity": .25, "duration": .18, "yoyo": True, "repeat": 3, "stagger": .12}, "the sound rings pulse")

# the three hiding places side by side on the game board (hook and the start of the game)
TRIO_ACT = [("rhi", "rhino", 400, 1080, .8), ("fox", "fennec", 960, 1010, .85), ("bear", "bear", 1520, 1010, .7)]
def TRIO(hid=False):
    return [prop("g3", lambda q: A.grass_tall(q, 660, 420), 430, 1050, 1.0, hid), prop("d3", lambda q: A.dune_mound(q, 760, 380), 1010, 1055, 1.0, hid),
            prop("s3", lambda q: A.snow_bank(q, 560, 330), 1580, 1050, 1.0, hid)]
TRIO_P = {"g3": (420, 880, 1.0), "d3": (960, 885, 1.0), "s3": (1500, 885, 1.0)}

SHOTS = [
    # ---------------------------------------------------------------- HOOK (cold open on the promise: two ears in the grass, turning different ways)
    S("savanna", RE, "Look! Two ears in the grass, and they're turning different ways! Who is it?", q=True, tag="hook: two ears in the grass", hide=["milo"], pcam=REP, cam2=W(RE, 1.05),
      props=[GRASS()], fx=[NOFLICK("rhi"), EAR("w:turning", "rhi", "rhino", "ear", 34), EAR("w:different", "rhi", "rhino", "ear2", -34), EAR("w:Who", "rhi", "rhino", "ear", 14), EAR("w:Who", "rhi", "rhino", "ear2", -14)],
      words=[("w:Who", "WHO?", .78, .3, 1.4, "sun", (.5, .32), 1.2)]),
    S("paper_blue", (960, 640, 1920), "Three animals are hiding! We can only see their ears.", q=True, tag="hook: three hiding animals", pcam=(960, 640, 2700), cam2=(960, 640, 1980),
      actors=TRIO_ACT, props=TRIO(), fx=[NOFLICK("rhi"), NOFLICK("fox"), NOFLICK("bear")] + WIGGLE("w:hiding!", "fox", "fennec") + [EAR("w:ears.", "rhi", "rhino", "ear", 30), PULSE("w:ears.", "#{p}bear-ear", 1.3, 2)],
      words=[("w:Three", "1", .22, .3, 1.1, "sun", (.22, .3), 1.0), ("w:Three", "2", .5, .3, 1.1, "sun", (.5, .3), 1.0), ("w:Three", "3", .78, .3, 1.1, "sun", (.78, .3), 1.0)]),
    S("savanna", say="I'm Milo the bluebird. Let's play Guess With Milo!", q=True, tag="hook: Milo", hide=["rhi"], fx=[("hop", "w:Guess", "milo")],
      words=[("w:Guess", "GUESS!", .8, .45, 1.1, "sun", (.5, .33), .9)], **MILO("savanna", 900)),
    *intro_shots(),
    S("paper_blue", (960, 660, 1700), "Look closely at the ears, and say your guess. Ready? Let's play!", q=True, tag="look at the ears", trans="iris", pcam=(960, 660, 2500), cam2=(960, 660, 1760),
      actors=TRIO_ACT, props=TRIO(), fx=[NOFLICK("rhi"), NOFLICK("fox"), NOFLICK("bear")] + WIGGLE("w:ears,", "fox", "fennec") + [EAR("w:ears,", "rhi", "rhino", "ear2", -30), PULSE("w:Ready?", "#{p}bear-ear", 1.3, 2)],
      words=[("w:Ready?", "READY?", .5, .2, 1.1, "sun", (.5, .3), .9)]),
    # ---------------------------------------------------------------- PART 1: the rhino
    S("savanna", RE, "Here are two ears. They are gray, with a little fringe of hair. Whose ears are they?", part=1, q=True, tag="ears 1", hide=["milo"], pcam=REP, cam2=W(RE, 1.05),
      props=[GRASS()], fx=[NOFLICK("rhi"), PULSE("w:gray,", "#{p}rhi-ear,#{p}rhi-ear2", 1.12), PULSE("w:hair.", "#{p}rhi-ear,#{p}rhi-ear2", 1.12)],
      words=[("w:gray,", "GRAY!", .22, .32, 1.2, "sun", (.3, .3), 1.0), ("w:hair.", "HAIR!", .82, .32, 1.2, "sun", (.72, .3), 1.0)]),
    S("savanna", RQ, "Is it the rhino? Or is it the zebra?", part=1, q=True, tag="question 1a", pause=3.2, hide=["milo"], pcam=RQP,
      props=[GRASS()], fx=[NOFLICK("rhi"), ("signs", "w:rhino?", ["RHINO", "ZEBRA"], 0, "wait:2.0"), EAR("wait:1.0", "rhi", "rhino", "ear", 30), EAR("wait:1.8", "rhi", "rhino", "ear2", -30)]),
    S("savanna", (1000, 640, 1800), "It is the rhino!", part=1, tag="the rhino comes out", pause=1.4, hide=["milo"], pcam=(1000, 560, 1900), cam2=(1000, 640, 1860),
      props=[GRASS()], fx=[SINK("w:It", "gr"), ("nod", "e:rhino!", "rhi")], words=[("e:rhino!", "RHINO!", .26, .3, 1.1, "sun", (.5, .32), .9)]),
    S("savanna", RH, "Here is the fun fact. A rhino can move each ear, on its own!", part=1, tag="each ear on its own", hide=["milo"], pcam=RHP,
      fx=[NOFLICK("rhi"), EAR("w:each", "rhi", "rhino", "ear", 32), EAR("e:own!", "rhi", "rhino", "ear2", -32)],
      words=[("w:each", "EACH EAR!", .82, .32, 1.0, "sun", (.5, .3), .9)]),
    S("savanna", (P("savanna", "rhi", "ears")[0] + 40, P("savanna", "rhi", "ears")[1] + 40, 760), "One ear can point forward, while the other ear points back!", part=1, tag="forward and back", hide=["milo"],
      pcam=(P("savanna", "rhi", "ears")[0] + 40, P("savanna", "rhi", "ears")[1] + 60, 900),
      props=[ARROW("af", P("savanna", "rhi", "ears")[0] + 210, P("savanna", "rhi", "ears")[1] - 10, s=.9, p=(P("savanna", "rhi", "ears")[0] + 190, P("savanna", "rhi", "ears")[1] - 20, .65)), ARROW("ab", P("savanna", "rhi", "ears")[0] - 170, P("savanna", "rhi", "ears")[1] - 10, True, .9, p=(P("savanna", "rhi", "ears")[0] - 110, P("savanna", "rhi", "ears")[1] - 20, .65))],
      fx=[NOFLICK("rhi"), EAR("w:forward,", "rhi", "rhino", "ear", 36), ("show", "w:forward,", "af"), EAR("w:back!", "rhi", "rhino", "ear2", -36), ("show", "w:back!", "ab")],
      words=[("w:forward,", "FRONT!", .84, .17, .9, "sun", (.75, .27), .8), ("w:back!", "BACK!", .42, .17, .9, "sun", (.3, .27), .8)]),
    S("savanna", RB, "Watch the ears! Forward, and back. Forward, and back!", part=1, q=True, tag="watch the ears", hide=["milo"], pcam=RBP, cam2=W(RB),
      fx=[NOFLICK("rhi"), EAR("w:Forward,:1", "rhi", "rhino", "ear", 34), EAR("w:back.:1", "rhi", "rhino", "ear", -30), EAR("w:Forward,:2", "rhi", "rhino", "ear2", 30), EAR("w:back!:2", "rhi", "rhino", "ear2", -34)],
      words=[("w:Watch", "WATCH!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("savanna", RH, "What does a rhino do, when it hears something interesting?", part=1, q=True, tag="what does it do", pause=3.0, hide=["milo"], pcam=RHP, cam2=W(RH, 1.06),
      props=[RINGS("r1", P("savanna", "rhi", "ears")[0] - 190, P("savanna", "rhi", "ears")[1] + 10, .8, True, p=(P("savanna", "rhi", "ears")[0] - 90, P("savanna", "rhi", "ears")[1] + 10, .55))], fx=[NOFLICK("rhi"), ("show", "w:hears", "r1"), RINGPULSE("w:interesting?", "r1")],
      words=[("e:interesting?", "?", .8, .3, 2.0, "sun", (.5, .34), 1.3)]),
    S("savanna", RH, "Both ears perk straight up! Boing!", part=1, tag="ears perk up", hide=["milo"], pcam=RHP, cam2=(RH[0], RH[1], round(RH[2] * .92)),
      fx=[NOFLICK("rhi")] + PERK("w:perk", "rhi", "rhino") + [PULSE("w:Boing!", "#{p}rhi-ear,#{p}rhi-ear2", 1.1, 2)], words=[("w:perk", "PERK UP!", .76, .2, 1.0, "sun", (.5, .32), .85)]),
    S("savanna", RB, "Up go the ears, to listen very closely. Perk!", part=1, tag="listen closely", hide=["milo"], pcam=RBP, cam2=W(RB, 1.05),
      fx=[NOFLICK("rhi")] + PERK("w:Up", "rhi", "rhino") + [PULSE("w:Perk!", "#{p}rhi-ear,#{p}rhi-ear2", 1.12, 2)], words=[("w:Perk!", "PERK!", .26, .34, 1.2, "sun", (.5, .34), 1.0)]),
    S("zoo", say="Now point both hands straight up, like perky rhino ears. Perk!", part=1, q=True, tag="hands up like perky ears", pause=2.4, fx=[("hop", "w:Perk!", "milo")],
      words=[("w:Perk!", "PERK!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("savanna", RB, "A rhino can't see very well. But it hears very well!", part=1, tag="hears very well", hide=["milo"], pcam=RBP, cam2=W(RB, 1.06),
      props=[RINGS("r2", P("savanna", "rhi", "ears")[0] + 170, P("savanna", "rhi", "ears")[1] - 30, .9, False, p=(P("savanna", "rhi", "ears")[0] + 150, P("savanna", "rhi", "ears")[1] - 40, .8))],
      fx=[("blinkslow", "w:see", "rhi"), ("show", "w:hears", "r2"), RINGPULSE("w:hears", "r2")] + WIGGLE("e:well!:2", "rhi", "rhino"),
      words=[("w:hears", "HEARS WELL!", .24, .3, 1.0, "sun", (.5, .32), .8)]),
    S("zoo", say="Point one hand forward, and one hand back, like rhino ears!", part=1, q=True, tag="hands like rhino ears", pause=3.0, fx=[("hop", "w:forward,", "milo"), ("hop", "w:back,", "milo")],
      words=[("w:forward,", "FRONT!", .84, .3, .9, "sun", (.5, .26), .85), ("w:back,", "BACK!", .84, .42, .9, "sun", (.5, .34), .85)], **MILO("zoo", 940)),
    S("savanna", RB, "Say it with me. A rhino can move each ear, on its own!", part=1, q=True, tag="say it: each ear", hide=["milo"], pcam=RBP,
      fx=[NOFLICK("rhi"), EAR("w:each", "rhi", "rhino", "ear", 30), EAR("e:own!", "rhi", "rhino", "ear2", -30), ("nod", "w:rhino", "rhi")],
      words=[("w:Say", "SAY IT!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("zoo", say="Now be very quiet, like a listening rhino. What can you hear?", part=1, q=True, tag="be quiet and listen", pause=3.0, fx=[("hop", "w:hear?", "milo")],
      words=[("w:quiet,", "SHH!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("savanna", (RH[0], RH[1], 1050), "Quick check! Can a rhino turn its two ears different ways? Yes, or no?", part=1, q=True, tag="question 1b", cam2=(RH[0], RH[1], 900), pause=3.2, hide=["milo"], pcam=RHP,
      fx=[NOFLICK("rhi"), EAR("w:turn", "rhi", "rhino", "ear", 30), EAR("w:different", "rhi", "rhino", "ear2", -30), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0"),
          EAR("wait:1.0", "rhi", "rhino", "ear", -20), EAR("wait:1.0", "rhi", "rhino", "ear2", 20), ("word", "e:no?", "?", {"x": RH[0] + 380, "y": RH[1] + 160, "size": 180, "cls": "sun", "p": {"x": RH[0] + 180, "y": RH[1] + 260, "size": 160}})]),
    S("savanna", RB, "Yes! One ear forward, one ear back. Great job!", part=1, tag="great job 1", hide=["milo"], pcam=RBP, cam2=W(RB),
      fx=[NOFLICK("rhi"), EAR("w:forward,", "rhi", "rhino", "ear", 34), EAR("w:back.", "rhi", "rhino", "ear2", -34), ("nod", "w:Great", "rhi")],
      words=[("w:Yes!", "YES!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- PART 2: the fennec fox
    S("dunes", FE, "Here are two more ears. Look! They are so big, and pointy! Whose ears are they?", part=2, q=True, tag="ears 2", trans="iris", hide=["milo"], pcam=FEP, cam2=W(FE, 1.05),
      props=[DUNE()], fx=[NOFLICK("fox"), PULSE("w:big,", "#{p}fox-ear,#{p}fox-ear2", 1.1), PULSE("w:pointy!", "#{p}fox-ear,#{p}fox-ear2", 1.1)] + WIGGLE("w:Whose", "fox", "fennec"),
      words=[("w:big,", "BIG!", .2, .32, 1.3, "sun", (.25, .3), 1.0), ("w:pointy!", "POINTY!", .8, .32, 1.1, "sun", (.75, .3), .9)]),
    S("dunes", FQ, "Is it the fox? Or is it the rabbit?", part=2, q=True, tag="question 2a", pause=3.2, hide=["milo"], pcam=FQP,
      props=[DUNE()], fx=[NOFLICK("fox"), ("signs", "w:fox?", ["FOX", "RABBIT"], 0, "wait:2.0")] + WIGGLE("wait:1.2", "fox", "fennec")),
    S("dunes", (1000, 640, 1800), "It is the fennec fox!", part=2, tag="the fox comes out", pause=1.4, hide=["milo"], pcam=(1000, 580, 1900), cam2=(1000, 640, 1860),
      props=[DUNE()], fx=[SINK("w:It", "du"), ("nod", "e:fox!", "fox")], words=[("e:fox!", "FENNEC FOX!", .26, .3, 1.0, "sun", (.5, .32), .8)]),
    S("paper", (960, 520, 1500), "Here is the fun fact. A fennec fox is a little fox, with giant ears!", part=2, tag="board: giant ears", pcam=(960, 560, 1700), props=[FFACE()],
      fx=[PULSE("w:little", "#{p}ff_w", .94), PULSE("w:giant", "#{p}ff-eL,#{p}ff-eR", 1.12, 2)], words=[("w:giant", "GIANT EARS!", .8, .56, .9, "sun", (.5, .74), .8)]),
    S("paper", (960, 560, 1500), "Its ears can be half as long as its body!", part=2, tag="half as long as its body", pcam=(980, 480, 1700),
      actors=[("fox", "fennec", 980, 720, 1.3)],
      props=[prop("be", lambda q: f'<g id="{q}"><rect x="-16" y="-125" width="32" height="250" rx="16" fill="#ff7aa2" stroke="#402010" stroke-width="7"/></g>', 1375, 265, 1.0, True, p=(1375, 265, 1.0)),
             prop("bb", lambda q: f'<g id="{q}"><rect x="-265" y="-16" width="530" height="32" rx="16" fill="#ff9f43" stroke="#402010" stroke-width="7"/></g>', 1000, 770, 1.0, True, p=(1000, 770, 1.0)),
             prop("bh1", lambda q: f'<g id="{q}"><rect x="-125" y="-16" width="250" height="32" rx="16" fill="#ff7aa2" stroke="#402010" stroke-width="7"/></g>', 865, 818, 1.0, True, p=(865, 818, 1.0)),
             prop("bh2", lambda q: f'<g id="{q}"><rect x="-125" y="-16" width="250" height="32" rx="16" fill="#ff7aa2" stroke="#402010" stroke-width="7"/></g>', 1135, 818, 1.0, True, p=(1135, 818, 1.0))],
      fx=[NOFLICK("fox"), ("show", "w:ears", "be"), PULSE("w:ears", "#{p}fox-ear", 1.08), ("show", "w:half", "bb"), ("show", "w:half", "bh1"), ("show", "w:long", "bh2"), PULSE("w:body!", "#{p}bb_w", 1.06)],
      words=[("w:half", "HALF!", .2, .3, 1.2, "sun", (.3, .32), 1.0)]),
    S("dunes", FB, "Wow! That is a lot of ear, for a little fox!", part=2, tag="a lot of ear", hide=["milo"], pcam=FBP, cam2=W(FB, 1.05),
      fx=[NOFLICK("fox")] + WIGGLE("w:ear,", "fox", "fennec", 2) + [("hop", "w:Wow!", "fox")], words=[("w:Wow!", "WOW!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("dunes", (P("dunes", "fox", "ears")[0] + 20, 600, 1000), "Count the giant ears with me. One, two!", part=2, q=True, tag="count the fox's ears", hide=["milo"], pcam=V("dunes", "fox", "ears", 1300, 0, 60), cam2=(P("dunes", "fox", "ears")[0] + 20, 600, 940),
      fx=[NOFLICK("fox"), PULSE("w:One,", "#{p}fox-ear", 1.12), PULSE("w:two!", "#{p}fox-ear2", 1.12)],
      words=[("w:One,", "1", .22, .3, 1.3, "sun", (.3, .3), 1.1), ("w:two!", "2", .82, .3, 1.3, "sun", (.7, .3), 1.1)]),
    S("dunes", FH, "What do those giant ears do?", part=2, q=True, tag="what do the ears do", pause=3.0, hide=["milo"], pcam=FHP, cam2=W(FH, 1.06),
      fx=[NOFLICK("fox")] + WIGGLE("w:giant", "fox", "fennec"), words=[("e:do?:2", "?", .2, .34, 2.0, "sun", (.5, .34), 1.3)]),
    S("paper_blue", (960, 560, 1600), "They listen for food, hiding under the sand. Like a little beetle!", part=2, tag="board: food under the sand", pcam=(960, 600, 1500), props=[SCUT()],
      fx=[RINGPULSE("w:listen", "sc-r"), ("to", "w:beetle!", "#{p}sc-bug", {"x": 18, "duration": .15, "yoyo": True, "repeat": 5}, "the beetle wiggles"), RINGPULSE("w:hiding", "sc-r")],
      words=[("w:listen", "LISTEN!", .5, .12, 1.1, "sun", (.5, .32), .9)]),
    S("dunes", FB, "Then the fox digs with all four feet. Dig, dig, dig!", part=2, tag="digs with four feet", hide=["milo"], pcam=FBP, cam2=W(FB, 1.04),
      props=[prop("pf", lambda q: art.sand_puffs(q, 18, 4), 1160, 930, .7, True, p=(1160, 930, .7))],
      fx=[("show", "w:digs", "pf"), PULSE("w:Dig,:1", "#{p}pf_w", 1.3), PULSE("w:dig,:2", "#{p}pf_w", 1.3), PULSE("w:dig!:3", "#{p}pf_w", 1.3)]
      + [("to", f"w:{w}", f"#{{p}}fox-{lg}", {"rotation": 26, "svgOrigin": f"{x} -120", "duration": .14, "yoyo": True, "repeat": 3}, "the fox digs" if lg == "fl" else "")
         for w in ("Dig,:1", "dig,:2", "dig!:3") for lg, x in (("fl", 86), ("fl2", 60), ("bl", -74), ("bl2", -100))],
      words=[("w:Dig,:1", "DIG, DIG!", .26, .3, 1.0, "sun", (.5, .32), .85)]),
    S("paper", (960, 520, 1500), "And big ears let extra heat out. That helps the fox stay cool, in the hot desert!", part=2, tag="board: stay cool", pcam=(960, 560, 1700),
      props=[FFACE("ff", 960, 720, .75, p=(960, 760, .95)), prop("h1", A.heat_waves, 767, 375, .8, True, p=(716, 325, .8)), prop("h2", A.heat_waves, 1153, 375, .8, True, p=(1204, 325, .8))],
      fx=[("show", "w:heat", "h1"), ("show", "w:heat", "h2"), ("to", "w:out.", "#{p}h1_w,#{p}h2_w", {"y": "-=60", "duration": 1.4, "ease": "sine.out"}, "the heat rises away"),
          PULSE("w:cool,", "#{p}ff_w", 1.04)], words=[("w:cool,", "COOL!", .82, .56, 1.2, "sun", (.5, .26), .9)]),
    S("zoo", say="Cup your hands behind your ears, like big fox ears. Listen!", part=2, q=True, tag="cup your ears", pause=3.0, fx=[("hop", "w:Listen!", "milo")],
      words=[("w:Listen!", "LISTEN!", .84, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("dunes", FB, "Say it with me. A fennec fox has giant ears!", part=2, q=True, tag="say it: giant ears", hide=["milo"], pcam=FBP, cam2=W(FB),
      fx=[("nod", "w:giant", "fox")] + WIGGLE("w:ears!", "fox", "fennec"), words=[("w:Say", "SAY IT!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("zoo", say="Can you dig like a fennec fox? Dig, dig, dig!", part=2, q=True, tag="dig like a fox", pause=2.4, fx=[("hop", "w:Dig,:2", "milo"), ("hop", "w:dig,:3", "milo"), ("hop", "w:dig!:4", "milo"), ("hop", "wait:1.2", "milo")],
      words=[("w:Dig,:2", "DIG, DIG!", .84, .3, .9, "sun", (.5, .33), .85)], **MILO("zoo", 940)),
    S("paper_blue", (960, 560, 1700), "Quick check! What do the fox's big ears listen for? Food under the sand, or a drum?", part=2, q=True, tag="question 2b", cam2=(960, 560, 1500), pause=3.2, pcam=(960, 640, 1700),
      props=[SCUT("sc", 960, 680, .8, p=(960, 760, .7))], fx=[RINGPULSE("w:listen", "sc-r"), ("signs", "w:Food", ["FOOD", "DRUM"], 0, "wait:2.0"), RINGPULSE("wait:1.0", "sc-r"),
          ("word", "e:drum?", "?", {"x": 1600, "y": 470, "size": 200, "cls": "sun", "p": {"x": 1250, "y": 520, "size": 170}})]),
    S("dunes", FB, "Food under the sand! Super listening!", part=2, tag="super listening", hide=["milo"], pcam=FBP, cam2=W(FB),
      fx=[NOFLICK("fox")] + WIGGLE("w:Super", "fox", "fennec") + [("hop", "w:Food", "fox")], words=[("w:Super", "SUPER!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- PART 3: the polar bear
    S("arctic", BE, "Here are the last ears. They are small, and round. Whose ears are they?", part=3, q=True, tag="ears 3", trans="iris", hide=["milo"], pcam=BEP, cam2=W(BE, 1.05),
      props=[SNOW()], fx=[PULSE("w:small,", "#{p}bear-ear", 1.25), PULSE("w:round.", "#{p}bear-ear", 1.25)],
      words=[("w:small,", "SMALL!", .2, .32, 1.2, "sun", (.5, .27), 1.0), ("w:round.", "ROUND!", .42, .62, 1.2, "sun", (.5, .64), 1.0)]),
    S("arctic", BQ, "Is it the polar bear? Or is it the fennec fox?", part=3, q=True, tag="question 3a", pause=3.2, hide=["milo"], pcam=BQP,
      props=[SNOW()], fx=[("signs", "w:polar", ["POLAR BEAR", "FOX"], 0, "wait:2.0"), PULSE("wait:1.2", "#{p}bear-ear", 1.2, 2)]),
    S("arctic", (1000, 640, 1800), "It is the polar bear!", part=3, tag="the polar bear comes out", pause=1.4, hide=["milo"], pcam=(1000, 580, 1900), cam2=(1000, 640, 1860),
      props=[SNOW()], fx=[SINK("w:It", "sn"), ("nod", "e:bear!", "bear")], words=[("e:bear!", "POLAR BEAR!", .26, .3, 1.0, "sun", (.5, .32), .8)]),
    S("arctic", BH, "Here is the fun fact. A polar bear has small, round ears!", part=3, tag="small round ears", hide=["milo"], pcam=BHP,
      fx=[PULSE("w:small,", "#{p}bear-ear", 1.25), PULSE("w:round", "#{p}bear-ear", 1.25)], words=[("w:small,", "SMALL EARS!", .74, .2, 1.0, "sun", (.5, .3), .85)]),
    S("arctic", (P("arctic", "bear", "ears")[0] + 40, 590, 880), "Count the little ears with me. One, two!", part=3, q=True, tag="count the bear's ears", hide=["milo"], pcam=V("arctic", "bear", "ears", 1000, 30, 80), cam2=(P("arctic", "bear", "ears")[0] + 40, 590, 830),
      fx=[PULSE("w:One,", "#{p}bear-ear", 1.3), PULSE("w:two!", "#{p}bear-neck", 1.05)],
      words=[("w:One,", "1", .22, .3, 1.3, "sun", (.3, .3), 1.1), ("w:two!", "2", .82, .3, 1.3, "sun", (.7, .3), 1.1)]),
    S("arctic", BB, "Why are a polar bear's ears so small?", part=3, q=True, tag="why so small", pause=3.0, hide=["milo"], pcam=BBP, cam2=W(BB, 1.06),
      fx=[("lookat", "e:small?", "bear", -6)], words=[("e:small?", "?", .26, .34, 2.0, "sun", (.5, .34), 1.3)]),
    S("paper_pink", (960, 600, 1500), "Small ears help keep the warmth in, in the cold, snowy Arctic!", part=3, tag="board: warmth in", pcam=(960, 640, 1500),
      props=[prop("ear1", lambda q: f'<g id="{q}"><circle r="150" fill="#ffb347" opacity=".3"/><circle r="110" fill="#ffb347" opacity=".35"/><circle r="96" fill="#fdfaf2" stroke="#6a5a4c" stroke-width="12"/><circle r="52" fill="#f6c9d3"/></g>', 960, 620, 1.3, p=(960, 660, 1.2)),
             prop("snow1", lambda q: art.snow(q, 30, 5), 960, 540, 1.0, p=(960, 560, 1.0))],
      fx=[PULSE("w:warmth", "#{p}ear1_w", 1.12, 2), PULSE("w:snowy", "#{p}ear1_w", 1.06)], words=[("w:warmth", "WARM!", .5, .12, 1.2, "sun", (.5, .34), 1.0)]),
    S("paper_blue", (960, 620, 1600), "Big fox ears let heat out. Small bear ears keep the warmth in!", part=3, tag="board: big ears, small ears", pcam=(960, 680, 1700), props=[EPAIR("ep", 960, 720, 1.0, p=(960, 760, .82))],
      fx=[PULSE("w:Big", "#{p}ep-fox", 1.08), ("to", "w:out.", "#{p}ep-heat", {"y": "-=50", "duration": 1.2, "ease": "sine.out"}, "the heat rises away"),
          PULSE("w:Small", "#{p}ep-bear", 1.15), PULSE("w:warmth", "#{p}ep-glow", 1.15, 2)],
      words=[("w:Big", "OUT!", .14, .5, 1.1, "sun", (.22, .28), .9), ("w:Small", "IN!", .9, .5, 1.1, "sun", (.78, .28), .9)]),
    S("arctic", BT, "And look! A polar bear has a short little tail. It keeps the warmth in, too!", part=3, tag="short tail", hide=["milo"], pcam=BTP,
      fx=[("to", "w:tail.", "#{p}bear-tail", {"x": -10, "duration": .14, "yoyo": True, "repeat": 5}, "the tail wiggles"), PULSE("w:short", "#{p}bear-tail", 1.25)],
      words=[("w:short", "SHORT TAIL!", .62, .2, .9, "sun", (.5, .3), .85)]),
    S("zoo", say="Can you shiver, like you are in the snow? Brrr!", part=3, q=True, tag="shiver", pause=2.4,
      fx=[("to", "w:Brrr!", "#{p}milo", {"x": 8, "duration": .06, "yoyo": True, "repeat": 11}, "Milo shivers")],
      words=[("w:Brrr!", "BRRR!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("zoo", say="Make small ears! Cover your ears with your hands. So cozy!", part=3, q=True, tag="cover your ears", pause=3.2, fx=[("hop", "w:cozy!", "milo")],
      words=[("w:cozy!", "COZY!", .78, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 1300)),
    S("arctic", BB, "Say it with me. A polar bear has small, round ears!", part=3, q=True, tag="say it: small ears", hide=["milo"], pcam=BBP, cam2=W(BB),
      fx=[("nod", "w:small,", "bear"), PULSE("w:ears!", "#{p}bear-ear", 1.2)], words=[("w:Say", "SAY IT!", .26, .34, 1.1, "sun", (.5, .34), .9)]),
    S("zoo", say="Can you hug yourself, warm and cozy, like a polar bear? Squeeze!", part=3, q=True, tag="hug yourself", pause=3.0, fx=[("hop", "w:Squeeze!", "milo")],
      words=[("w:Squeeze!", "HUG!", .84, .3, 1.0, "sun", (.5, .33), .9)], **MILO("zoo", 940)),
    S("paper_pink", (960, 600, 1700), "Quick check! Which ears keep the warmth in? Big ears, or small ears?", part=3, q=True, tag="question 3b", cam2=(960, 600, 1500), pause=3.2, pcam=(960, 680, 1700),
      props=[EPAIR("ep", 960, 700, .85, p=(960, 900, .72))], fx=[PULSE("w:Big", "#{p}ep-fox", 1.08), PULSE("w:small", "#{p}ep-bear", 1.15), ("signs", "w:Big", ["BIG", "SMALL"], 1, "wait:2.0"),
          PULSE("wait:2.05", "#{p}ep-glow", 1.15, 2), ("word", "e:ears?:3", "?", {"x": 1600, "y": 470, "size": 200, "cls": "sun", "p": {"x": 1250, "y": 520, "size": 170}})]),
    S("arctic", BB, "Small ears! You remembered!", part=3, tag="you remembered", hide=["milo"], pcam=BBP, cam2=W(BB), fx=[("nod", "w:remembered!", "bear")],
      words=[("w:Small", "SMALL!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    # ---------------------------------------------------------------- QUIZ: the three pairs of ears again
    S("zoo_eve", WIDE, "Three pairs of ears, and three friends! Now it is quiz time!", part=4, trans="iris", tag="quiz time", cam2=(960, 560, 1860), pcam=(960, 560, 1800),
      words=[("w:quiz", "QUIZ TIME!", .5, .3, 1.3, "sun", (.5, .33))], fx=[("hop", "w:quiz", "milo", 2)]),
    S("savanna", RQ, "Whose ears can turn different ways? The rhino's, or the polar bear's?", part=4, q=True, tag="quiz 1", pause=3.2, hide=["milo"], pcam=RQP,
      props=[GRASS()], fx=[NOFLICK("rhi"), EAR("w:turn", "rhi", "rhino", "ear", 32), EAR("w:different", "rhi", "rhino", "ear2", -32), ("signs", "w:rhino's,", ["RHINO", "POLAR BEAR"], 0, "wait:2.0")]),
    S("savanna", RB, "The rhino! One ear forward, one ear back.", part=4, tag="quiz 1: rhino", hide=["milo"], pcam=RBP, cam2=W(RB),
      fx=[NOFLICK("rhi"), EAR("w:forward,", "rhi", "rhino", "ear", 34), EAR("w:back.", "rhi", "rhino", "ear2", -34)], words=[("w:rhino!", "RHINO!", .26, .34, 1.2, "sun", (.5, .34), 1.0)]),
    S("dunes", FQ, "Whose giant ears listen under the sand? The fox's, or the rhino's?", part=4, q=True, tag="quiz 2", pause=3.2, hide=["milo"], pcam=FQP,
      props=[DUNE()], fx=[NOFLICK("fox")] + WIGGLE("w:listen", "fox", "fennec") + [("signs", "w:fox's,", ["FOX", "RHINO"], 0, "wait:2.0")]),
    S("dunes", FB, "The fennec fox! Listen, listen!", part=4, tag="quiz 2: fox", hide=["milo"], pcam=FBP, cam2=W(FB),
      fx=[NOFLICK("fox")] + WIGGLE("w:Listen,:1", "fox", "fennec", 3), words=[("w:fox!", "FOX!", .26, .34, 1.3, "sun", (.5, .34), 1.0)]),
    S("arctic", BQ, "Whose ears are small and round? The fox's, or the polar bear's?", part=4, q=True, tag="quiz 3", pause=3.2, hide=["milo"], pcam=BQP,
      props=[SNOW()], fx=[PULSE("w:small", "#{p}bear-ear", 1.2), ("signs", "w:fox's,", ["FOX", "POLAR BEAR"], 1, "wait:2.0")]),
    S("arctic", BB, "The polar bear! Small ears keep it warm.", part=4, tag="quiz 3: polar bear", hide=["milo"], pcam=BBP, cam2=W(BB), fx=[("nod", "w:bear!", "bear")],
      words=[("w:bear!", "POLAR BEAR!", .27, .3, .85, "sun", (.5, .34), .8)]),
    # ---------------------------------------------------------------- RECAP + GOODBYE (the closing picture names the next Guess With Milo)
    S("paper_blue", (960, 640, 1900), "Look at all our ear friends! You guessed them all!", part=4, trans="iris", tag="all the ear friends", pcam=(980, 640, 2500), cam2=(960, 640, 1960),
      actors=[("rhi", "rhino", 360, 920, .7), ("fox", "fennec", 1010, 920, 1.05), ("bear", "bear", 1580, 920, .75), ("milo", "milo", 1740, 360, .62, True, True)],
      fx=[NOFLICK("rhi"), EAR("w:ear", "rhi", "rhino", "ear", 30), EAR("w:ear", "rhi", "rhino", "ear2", -30)] + WIGGLE("w:friends!", "fox", "fennec") + [PULSE("w:guessed", "#{p}bear-ear", 1.25), ("hop", "w:all!:2", "milo")],
      words=[("w:all!:2", "YOU DID IT!", .5, .15, 1.0, "sun", (.5, .3), .85)]),
    S("zoo_eve", say="Turn your ears like a rhino. Cup your ears like a fox. And cover them, so cozy, like a polar bear!", part=4, q=True, tag="all three moves", pause=1.6,
      fx=[("hop", "w:Turn", "milo"), ("hop", "w:Cup", "milo"), ("hop", "w:cover", "milo")],
      words=[("w:cozy,", "COZY!", .84, .3, .9, "sun", (.5, .33), .8)], **MILO("zoo_eve", 940)),
    S("paper_blue", BOARD, "Next time on Guess With Milo: whose egg is this? Bye-bye, friends!", part=4, tag="next: whose egg", pcam=BOARDP,
      props=[prop("qm", A11.qmark, 960, 520, 1.25, p=(960, 560, 1.5))], fx=[PULSE("w:egg", "#{p}qm_w", 1.15, 2)],
      words=[("w:egg", "WHOSE EGG?", .5, .14, 1.1, "sun", (.5, .3), .9), ("w:Bye-bye,", "BYE-BYE!", .5, .74, 1.0, "pill", (.5, .7), .8)]),
    *intro_shots(),      # the main intro again as the last shots (owner, Nov 20 4:50 PM: at the beginning and at the end of every new long video)
]
for _s in SHOTS:        # a picture board never drifts closer: it only pulls out a little (16:9 and 9:16)
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)

SHORTS = [
    {"id": "zc_ep12_short1", "title": "Whose Ears Turn Two Ways? Guess With Milo", "band": ("TWO WAYS?", "WHO?"), "thumb_text": "LISTEN!", "part": 1,
     "extra_first": [S("savanna", RE, "Two ears in the grass! Guess with Milo!", part=1, q=True, tag="hook: two ears", hide=["milo"], pcam=REP, cam2=W(RE, 1.05),
                       props=[GRASS()], fx=[NOFLICK("rhi"), EAR("w:ears", "rhi", "rhino", "ear", 34), EAR("w:grass!", "rhi", "rhino", "ear2", -34)],
                       words=[("w:Guess", "?", .8, .3, 2.0, "sun", (.5, .34), 1.3)])]},
    {"id": "zc_ep12_short2", "title": "Who Has Giant Ears? Guess With Milo", "band": ("GIANT EARS?", "WHO?"), "thumb_text": "DIG DIG!", "part": 2,
     "extra_first": [S("dunes", FE, "Two giant ears! Guess with Milo!", part=2, q=True, tag="hook: giant ears", hide=["milo"], pcam=FEP, cam2=W(FE, 1.05),
                       props=[DUNE()], fx=[NOFLICK("fox")] + WIGGLE("w:giant", "fox", "fennec"), words=[("w:Guess", "?", .8, .3, 2.0, "sun", (.5, .34), 1.3)])]},
    {"id": "zc_ep12_short3", "title": "Who Has Tiny Round Ears? Guess With Milo", "band": ("TINY EARS?", "WHO?"), "thumb_text": "COZY!", "part": 3,
     "extra_first": [S("arctic", BE, "Two small, round ears! Guess with Milo!", part=3, q=True, tag="hook: small ears", hide=["milo"], pcam=BEP, cam2=W(BE, 1.05),
                       props=[SNOW()], fx=[PULSE("w:small,", "#{p}bear-ear", 1.25)], words=[("w:Guess", "?", .8, .3, 2.0, "sun", (.5, .34), 1.3)])]},
]

# thumbnails (thumb.py): one big object, 1-2 words, none of the title's words, no watermark
_RP = 'gsap.set("#P-ear",{rotation:32,svgOrigin:"262 -436"});gsap.set("#P-ear2",{rotation:-32,svgOrigin:"214 -446"});'
_FP = 'gsap.set("#P-ear",{rotation:-8,svgOrigin:"128 -256"});gsap.set("#P-ear2",{rotation:8,svgOrigin:"176 -262"});'
THUMBS = {
    "zc_ep12": {"place": "savanna", "cam": (960, 540, 1920), "actors": [("rhino", 760, 1130, 1.55, False, _RP), ("milo", 1560, 980, 1.25, True, "")],
                "props": [(lambda q: A.grass_tall(q, 2600, 860), 900, 1160, 1.0)], "words": [("LISTEN!", 1440, 240, 230, "sun")]},
    "zc_ep12_short1": {"place": "savanna", "cam": (900, 560, 1000), "actors": [("rhino", 880, 1000, 1.0, False, _RP)],
                       "props": [(lambda q: A.grass_tall(q, 1400, 520), 900, 1010, 1.0)], "words": [("LISTEN!", 540, 1500, 190, "sun")]},
    "zc_ep12_short2": {"place": "dunes", "cam": (980, 560, 1000), "actors": [("fennec", 960, 960, 1.4, False, _FP)],
                       "props": [(lambda q: A.dune_mound(q, 1400, 600), 980, 1010, 1.0)], "words": [("DIG", 540, 1380, 200, ""), ("DIG!", 540, 1580, 220, "sun")]},
    "zc_ep12_short3": {"place": "arctic", "cam": (980, 600, 800), "actors": [("bear", 960, 960, 1.3, False, "")],
                       "props": [(lambda q: A.snow_bank(q, 1200, 640), 980, 1010, 1.0)], "words": [("COZY!", 540, 1500, 200, "sun")]},
}
