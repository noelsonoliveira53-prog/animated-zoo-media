"""za_ep03 - Milo's Zoo Adventures: "Baby Elephant Tumble Shares the Last Drink" (cartoon adventure, the 3D music-and-sync process: "beat").
It has not rained and the water hole is dry. Tumble follows his nose to one small pool, deep in a crack in the rocks. Three little birds
are thirsty too, and their beaks cannot reach. Tumble sucks the water up and squirts a drink for each friend. Then the rain comes.
Nobody is hurt, lost, crying or trapped: the birds are thirsty in a mild way and get their drink.

FACTS, read at the source on Nov 17 2026, 8:35 PM ET:
 [WWF] wwf.org.uk/gowild/amazing-facts/awesome-animals/unforgettable-elephant-facts ("Unforgettable elephant facts")
   "They also use their trunks to smell water up to 5km away."
   "They suck water up their trunks then blow it into their mouths."
   "Since African elephants live in very hot countries, they keep cool by squirting a trunkful of cool water over their bodies."
 [SDZ] San Diego Zoo Wildlife Alliance, animals.sandiegozoo.org/animals/elephant
   "the elephant sucks water only part way up the trunk, curls it toward its mouth," "tilts its head up, and lets the water from the trunk pour in."
   "They often choose to live near rivers during dry months."
 Said as animal facts in the film (the three "fact" shots and the two closing questions), each from a quote above: an elephant can smell water
 from far away with its trunk; it sucks water up its trunk, then blows it into its mouth; elephants squirt water over their bodies to keep cool.
 Not animal facts, said as what happens in THIS story: the water hole dries without rain, the birds ride on Tumble, a pool lies in a crack,
 Tumble squirts a drink into each beak, the birds see the clouds first. The three birds are story birds of no named kind; nothing is claimed about them.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep03 as A
import kit
from kit import Kit, S, prop
kit.PT.update(A.BIRD_PT); kit.BOX.update(A.BIRD_BOX)

EP = {"id": "za_ep03", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "tumble": {"voice": "am_puck", "speed": .85, "pitch": 5, "formant": 1.16, "gain": .66},
               "mama": {"voice": "bf_emma", "speed": .8, "gain": .8},
               "pip": {"voice": "af_nova", "speed": .9, "pitch": 5, "formant": 1.22, "gain": 1.1}, "kiki": {"voice": "af_sky", "speed": .9, "pitch": 6, "formant": 1.25, "gain": .95},
               "bo": {"voice": "af_jessica", "speed": .88, "pitch": 4, "formant": 1.2, "gain": .9}},
      "title": "Baby Elephant Tumble Shares the Last Drink", "thumb_text": "SQUIRT!",
      "series": "Milo's Zoo Adventures",
      "description": ("It has not rained for days, and the water hole is dry. Baby elephant Tumble follows his nose to one small pool, deep in a crack in the rocks. "
                      "Three little birds are thirsty too, but their beaks cannot reach the water. What will Tumble do with the very last drink? "
                      "A gentle animal adventure for ages 2-6 about sharing and helping friends, with questions to answer and a song to sing along.\n"
                      "Kids see how an elephant smells water from far away, how it sucks water up its trunk and blows it into its mouth, and how it squirts water to keep cool.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nWWF (Unforgettable elephant facts); San Diego Zoo Wildlife Alliance (elephant)."),
      "tags": ["baby elephant", "elephant story for kids", "animal stories for kids", "sharing story for kids", "kids adventure cartoon", "how elephants drink water", "elephant trunk",
               "little birds", "rain story for kids", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

# the birds on Tumble's back: (dx, dy) from Tumble's feet in his own units, at scale s of Tumble's scale
BACK = {"bo": (-236, -420, .5), "kiki": (-36, -440, .5), "pip": (300, -592, .5)}      # Bo and Kiki on his back, Pip on top of his head
BK = {"pip": "bird_pip", "kiki": "bird_kiki", "bo": "bird_bo"}


def riders(x, y, s): return [(w, BK[w], round(x + BACK[w][0] * s), round(y + BACK[w][1] * s), round(s * BACK[w][2], 3)) for w in ("bo", "kiki", "pip")]
def ride_move(x, y, s): return {a[0]: a[2:5] for a in riders(x, y, s)}


STAGES = {
    "zoo": [("mama", "elephant", 1480, 930, .92, True), ("tumble", "tumble", 560, 936, .6), ("milo", "milo", 260, 500, .78, False, True)],
    "savanna": [("tumble", "tumble", 620, 930, .62), ("milo", "milo", 430, 500, .8, False, True)],
    "dryhole": [("tumble", "tumble", 430, 930, .6), ("milo", "milo", 1320, 470, .75, False, True)],
    "bigtree": [("tumble", "tumble", 860, 930, .62), ("pip", "bird_pip", 1340, 950, .5, True), ("kiki", "bird_kiki", 1530, 962, .5, True), ("bo", "bird_bo", 1750, 950, .5, True),
                ("milo", "milo", 450, 500, .75, False, True)],
    "rocks": [("tumble", "tumble", 520, 960, .62), ("pip", "bird_pip", 1180, 930, .5, True), ("kiki", "bird_kiki", 1380, 940, .5, True), ("bo", "bird_bo", 1600, 934, .5, True),
              ("milo", "milo", 300, 430, .7, False, True)],
    "zoo_eve": [("tumble", "tumble", 660, 940, .6), ("mama", "elephant", 1540, 932, .9, True), ("milo", "milo", 300, 400, .68, False, True)] + riders(660, 940, .6),
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
EAR = "250 -590"; TP = "392 -430"       # the pivots of an elephant's ear and trunk
BIRDS = ["pip", "kiki", "bo"]
JAW = {w: art2.RIGS[BK[w]]["jaw"][2] for w in BIRDS}
def only(place, *keep, stage=None): return [a[0] for a in (stage or STAGES[place]) if a[0] not in keep]
TREE_RIDE = [a for a in STAGES["bigtree"] if a[0] in ("tumble", "milo")] + riders(860, 930, .62)       # the birds sit on Tumble's back
ROCKS_RIDE = [("tumble", "tumble", 520, 960, .62), ("milo", "milo", 300, 430, .7, False, True)] + riders(520, 960, .62)
POOL = lambda lv=58: prop("pl", lambda p: A.pool(p, lv), 866, 1056, 1.0)       # the water in the crack: 0 full, 58 the small pool, 170 empty
SUN_S = lambda: prop("hs", art3.hot_sun, 1500, 220, .8)                        # over the savanna's own sun
SPIN = ("to", 0.05, "#{p}hs-rays", {"rotation": 60, "transformOrigin": "50% 50%", "duration": 6, "ease": "none"}, "")
FLAP = lambda at, who="tumble", n=7: ("to", at, "#{p}" + who + "-ear", {"rotation": 14, "svgOrigin": EAR, "duration": .18, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, f"{who} flaps its ears")
TRUNK = lambda deg: ("to", 0, "#{p}tumble-trunk", {"rotation": deg, "svgOrigin": TP, "duration": .01}, "")       # the trunk already in a pose when the shot starts
DIP = lambda at, k=1.55, d=.6: ("to", at, "#{p}tumble-trunk", {"scaleY": k, "svgOrigin": TP, "duration": d, "ease": "power2.inOut"}, "Tumble's trunk reaches down")
BEAK = lambda at, who, deg=20, d=.2: ("to", at, "#{p}" + who + "-jaw", {"rotation": deg, "svgOrigin": JAW[who], "duration": d}, f"{who} opens its beak")
WING = lambda at, who, n=9: ("to", at, "#{p}" + who + "-wing", {"rotation": -50, "svgOrigin": "20 -150", "duration": .12, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, f"{who} flaps its wings")
RAIN = [prop("tn", A.tint, 0, 0, 1.0), prop("rn", A.rain, -500, -700, 1.0)]
RAINFX = ("to", 0, "#{p}rn_w", {"x": "-=60", "y": "+=220", "duration": .3, "repeat": 40, "ease": "none"}, "")
CLOUDS = lambda: [prop("c1", A.cloud, 520, 190, 1.3), prop("c2", A.cloud, 1180, 140, 1.5), prop("c3", A.cloud, 1760, 230, 1.2)]
SQ_FROM = (955, 769)       # the tip of Tumble's trunk on the "rocks" stage when it is lifted by 40 degrees


def SQ(name, who, h, hidden=True):
    bx, by = P("rocks", who, "beak"); return prop(name, lambda p: A.squirt(p, bx - SQ_FROM[0] + 6, by - SQ_FROM[1] + 8, h), SQ_FROM[0], SQ_FROM[1], 1.0, hidden)


# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. Nobody sings: the rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}       # the show loop's key and the music bed's tempo
SING_GO = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~ ~", "notes": "C4:1 E4:1 G4:1 G4:.5 A4:.5,G4:.5 E4:.5 D4:2", "rest": 1},
                               {"text": "~ ~ ~ ~ ~ ~ ~", "notes": "F4:1 F4:1 E4:1 D4:.5 D4:.5 E4:1 C4:2", "rest": 1}])
SING_TY = dict(REFRAIN, chords="C G", lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "E4:.5 G4:.5 C5:1 A4:1 G4:1 E4:.5,C4:1.5", "rest": 2}])       # the birds' thank-you tune
SING_END_A = dict(REFRAIN, chords="C G", lines=[{"text": "~ ~ ~ ~ ~", "notes": "C4:1 E4:1 G4:1 G4:.5,A4:.5 G4:.5,E4:1.5", "rest": 2}])
SING_END_B = dict(REFRAIN, chords="F C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "F4:1 F4:.5 F4:.5,E4:.5 D4:.5,E4:.5 C4:2.5", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune

SHOTS = [
    # ------------------------------------------------------------ HOOK: the feeling and the problem in the first 5 seconds
    S("zoo", C("zoo", "tumble", "all", 1000, 20, -50), "No rain for days and days! And Tumble is so, so thirsty.", beat="hook", tag="hook: no rain, so thirsty", hide=["mama", "milo"],
      words=[("w:rain", "NO RAIN!", .43, .13, .85, "sun"), ("w:thirsty.", "SO THIRSTY!", .8, .16, .8, "")], fx=[("face", "w:And", "tumble", "sad")]),
    S("zoo", C("zoo", "milo", "body", 760), "I'm Milo! Can you help Tumble find a drink of water?", tag="hook: Milo", hide=["mama", "tumble"], fx=[("hop", "w:help", "milo")],
      props=[prop("wd", A.drop, 760, 430, .5, True)], ),
    S("zoo", WIDE, "This is Tumble, the baby elephant. And this is his mama.", tag="zoo wide", cam2=(980, 560, 1800),
      words=[("w:Tumble,", "TUMBLE", .41, .4, .85, "pill"), ("w:mama.", "MAMA", .66, .3, .85, "pill")]),
    S("zoo", C("zoo", "mama", "head", 900, 40, 40), "The water hole is dry, little one. We need the rain.", who="mama", tag="Mama: we need the rain", hide=["tumble", "milo"],
      fx=[("nod", "w:We", "mama")], words=[("w:rain.", "WE NEED RAIN", .26, .2, .75, "pill")]),
    # ------------------------------------------------------------ GOAL
    S("zoo", C("zoo", "tumble", "head", 920, -60, 20), "I will find water, Mama. One big, cool drink!", who="tumble", beat="goal", tag="goal: find water", hide=["mama", "milo"],
      fx=[("face", 0.1, "tumble", "happy"), ("hop", "w:One", "tumble")], words=[("w:big,", "A BIG DRINK!", .25, .19, .75, "sun")]),
    S("zoo", C("zoo", "milo", "body", 820, 30, 0), "But where is the water, when there is no rain?", tag="Milo: where is the water", hide=["mama", "tumble"],
      props=[prop("wd", A.drop, 540, 420, .5, True)], fx=[("show", "w:water,", "wd")], words=[("w:where", "WHERE?", .74, .22, 1.0, "pill")]),
    S("zoo", C("zoo", "mama", "head", 900, 40, 40), "Follow your nose, Tumble. And stay close to Milo.", who="mama", tag="Mama: follow your nose", hide=["tumble", "milo"],
      fx=[("nod", "w:Follow", "mama"), ("trunk", "w:nose,", "mama", -30, .4), ("trunk", "e:Tumble.", "mama", 0, .4)], words=[("w:nose,", "FOLLOW YOUR NOSE", .3, .18, .62, "pill")]),
    S("zoo", (744, 600, 1400), "Off they go, to look for water.", tag="off they go", hide=["mama"], move={"milo": (260, 570, .78)},
      fx=[("walk", 0.1, "tumble", 260, 3.0), ("fly", 0.1, "milo", 480, 610, 3.0)]),
    S("savanna", (560, 640, 1300), "Friends help friends, come along with me! Step by step, what will we see?", trans="iris", tag="the walking rhyme", cam2=(600, 640, 1240), props=[SUN_S()],
      move={"tumble": (240, 930, .62), "milo": (860, 640, .8)}, fx=[SPIN, ("hop", "w:come", "milo"), ("trunk", "w:Step", "tumble", -50, .4), ("trunk", "w:what", "tumble", 0, .4)],
      words=[("w:Friends", "FRIENDS HELP FRIENDS", .4, .15, .62, "pill")]),
    S("savanna", WIDE, who="", sing=SING_GO, beat="song", tag="song: off we go", props=[SUN_S()],
      fx=[SPIN, ("walk", 0.2, "tumble", 360, 8.6), ("fly", 0.2, "milo", 400, 500, 8.6), ("trunk", TB(3), "tumble", -60, .4), ("trunk", TB(5), "tumble", 0, .4), ("trunk", TB(11), "tumble", -60, .4), ("trunk", TB(13), "tumble", 0, .4)],
      move={"tumble": (240, 930, .62), "milo": (150, 480, .8)}, words=[(TB(0), "FRIENDS HELP FRIENDS", .52, .1, .6, "pill"), (TB(8), "STEP BY STEP", .5, .32, .8, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: the water hole is dry (Tumble's own nose finds the way)
    S("dryhole", WIDE, "Here is the water hole. But, oh! Where is the water?", trans="iris", beat="obstacle1", tag="the water hole", cam2=(1000, 560, 1800),
      move={"tumble": (220, 930, .6)}, fx=[("walk", 0.1, "tumble", 210, 2.6), ("face", "w:But,", "tumble", "wow")], words=[("w:water", "WATER HOLE", .36, .2, .9, "pill")]),
    S("dryhole", (1180, 960, 1200), "No water. Only dry, cracked mud.", beat="obstacle1", tag="dry mud", hide=["tumble", "milo"], cam2=(1180, 960, 1050),
      props=[prop("x", art.cross, 1180, 880, 1.0, True)], fx=[("show", "w:No", "x"), ("snd", "w:dry,", "pop")], words=[("w:dry,", "ALL DRY!", .5, .2, 1.1, "sun")]),
    S("dryhole", C("dryhole", "tumble", "head", 800, -40, 10), "Oh no. The water is all gone.", who="tumble", beat="obstacle1", tag="all gone", hide=["milo"],
      fx=[("face", 0.02, "tumble", "sad")]),
    S("dryhole", C("dryhole", "milo", "body", 820, 20, -70), "Is there any water in the water hole? Yes, or no?", q=True, beat="obstacle1", tag="question: yes or no", pause=3.2, hide=["tumble"],
      fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("dryhole", C("dryhole", "tumble", "all", 1000, 60, -40), "My mouth is so dry, Milo. What can I do?", who="tumble", beat="obstacle1", tag="what can I do", hide=["milo"],
      fx=[("face", 0.02, "tumble", "sad"), ("trunk", "w:What", "tumble", -20, .4), ("trunk", "e:do?", "tumble", 0, .4)]),
    S("dryhole", C("dryhole", "milo", "body", 780, 70, 0), "Tumble, you have a super nose. Your trunk!", beat="obstacle1", tag="Milo: your trunk", hide=["tumble"],
      fx=[("hop", "w:super", "milo")], words=[("w:super", "SUPER NOSE!", .77, .24, .8, "sun")]),
    S("paper_pink", (960, 540, 1600), "An elephant can smell water with its trunk, from far, far away.", beat="fact", tag="fact: smells water far away",
      actors=[("t", "tumble", 420, 930, .62)], props=[prop("wd", A.drop, 1560, 500, 1.1), prop("s1", A.smell, 1230, 470, .9, True), prop("s2", A.smell, 960, 500, .9, True), prop("s3", A.smell, 720, 540, .8, True)],
      fx=[("trunk", 0.1, "t", -62, .5), ("show", "w:smell", "s1"), ("show", "w:with", "s2"), ("show", "w:trunk,", "s3"),
          ("to", "w:smell", "#{p}s1_w,#{p}s2_w,#{p}s3_w", {"x": "-=40", "duration": .7, "yoyo": True, "repeat": 7, "ease": "sine.inOut"}, "")],
      words=[("w:smell", "SMELLS WATER", .5, .16, .9, "sun"), ("w:far,", "FAR AWAY", .76, .68, .9, "pill")]),
    S("dryhole", C("dryhole", "tumble", "head", 900, 40, -40), "Sniff, sniff, sniff. I smell water! This way!", who="tumble", beat="obstacle1", tag="I smell water", hide=["milo"],
      props=[prop("s1", A.smell, 900, 560, .7, True)],
      fx=[("face", 0.02, "tumble", "wow"), ("trunk", 0.1, "tumble", -50, .4), ("show", "w:I", "s1"), ("trunk", "w:This", "tumble", -80, .3), ("hop", "w:This", "tumble")],
      words=[("w:Sniff,", "SNIFF!", .2, .2, 1.0, "sun")]),
    S("dryhole", C("dryhole", "milo", "body", 820, 20, 0), "Can you sniff like Tumble? Sniff, sniff, sniff!", q=True, beat="obstacle1", tag="question: sniff", hide=["tumble"],
      fx=[("hop", "w:Sniff,", "milo", 2)], words=[("w:Sniff,", "SNIFF, SNIFF!", .79, .2, .85, "sun")]),
    S("savanna", (900, 620, 1700), "Tumble follows his nose. Over the hill, and past the tall, dry grass.", beat="obstacle1", tag="follows his nose", cam2=(1040, 620, 1600),
      move={"tumble": (300, 930, .62), "milo": (360, 540, .8)}, props=[prop("s1", A.smell, 1320, 640, .8)],
      fx=[TRUNK(-50), ("walk", 0.1, "tumble", 420, 4.6), ("fly", 0.1, "milo", 640, 520, 4.6), ("to", 0.1, "#{p}s1_w", {"x": 1640, "duration": 4.6, "ease": "none"}, ""),],
      words=[("w:nose.", "THIS WAY!", .66, .15, .9, "pill")]),
    # ------------------------------------------------------------ OBSTACLE 2: three thirsty little birds, too tired and too slow to come along
    S("bigtree", WIDE, "Under the big tree, somebody calls. Cheep, cheep, cheep!", trans="iris", beat="obstacle2", tag="cheep", cam2=(1040, 560, 1780),
      move={"tumble": (520, 930, .62)}, fx=[("walk", 0.1, "tumble", 340, 3.0), ("hop", "w:Cheep,", "pip"), ("hop", "w:cheep,", "kiki"), ("hop", "w:cheep!", "bo")],
      words=[("w:Cheep,", "CHEEP!", .78, .5, .9, "sun")]),
    S("bigtree", (1545, 800, 960), "Three little birds! Pip, Kiki and Bo.", beat="obstacle2", tag="Pip, Kiki and Bo", hide=["tumble", "milo"],
      fx=[("hop", "w:Pip,", "pip"), ("hop", "w:Kiki", "kiki"), ("hop", "w:Bo.", "bo")],
      words=[("w:Pip,", "PIP", .29, .3, .8, "pill"), ("w:Kiki", "KIKI", .5, .26, .8, "pill"), ("w:Bo.", "BO", .72, .3, .8, "pill")]),
    S("bigtree", C("bigtree", "pip", "head", 700, -60, 20), "We are thirsty, too. Our puddle is all dry.", who="pip", beat="obstacle2", tag="Pip: thirsty too", hide=["tumble", "milo", "kiki", "bo"],
      fx=[("face", 0.02, "pip", "sad")], words=[("w:thirsty,", "THIRSTY, TOO", .7, .2, .8, "pill")]),
    S("bigtree", C("bigtree", "kiki", "head", 700, -40, 20), "And our wings are too tired to fly far.", who="kiki", beat="obstacle2", tag="Kiki: tired wings", hide=["tumble", "milo", "pip", "bo"],
      fx=[("face", 0.02, "kiki", "sad"), ("to", "w:wings", "#{p}kiki-wing", {"rotation": -30, "svgOrigin": "20 -150", "duration": .3, "yoyo": True, "repeat": 3}, "Kiki lifts a wing")]),
    S("bigtree", C("bigtree", "tumble", "head", 800, -40, 10), "Come with me! My nose can find water.", who="tumble", beat="obstacle2", tag="come with me", hide=["milo"] + BIRDS,
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:nose", "tumble", -50, .3), ("trunk", "e:water.", "tumble", 0, .4)]),
    S("bigtree", (1150, 660, 1500), "Tumble walks on. The birds hop after him. Hop, hop, hop. Too slow!", beat="obstacle2", tag="too slow", hide=["milo"],
      move={"tumble": (560, 930, .62)}, fx=[("walk", 0.1, "tumble", 300, 3.4), ("hop", "w:Hop,", "pip"), ("hop", "w:hop,", "kiki"), ("hop", "w:hop.", "bo"), ("face", "w:Too", "pip", "sad")],
      words=[("w:Too", "TOO SLOW!", .76, .3, .9, "pill")]),
    S("bigtree", C("bigtree", "milo", "body", 820, 20, -70), "How can three little birds come along? Ride on Tumble, or stay here?", q=True, beat="obstacle2", tag="question: ride or stay", pause=3.2, hide=["tumble"] + BIRDS,
      fx=[("signs", "w:Ride", ["RIDE", "STAY"], 0, "wait:2.0")]),
    S("bigtree", C("bigtree", "tumble", "head", 800, -40, 10), "I know! Hop on my back, little birds!", who="tumble", beat="obstacle2", tag="hop on my back", hide=["milo"] + BIRDS,
      fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:Hop", "tumble")], words=[("w:Hop", "HOP ON!", .26, .2, 1.0, "sun")]),
    S("bigtree", C("bigtree", "tumble", "all", 1300, 160, -60), "Hop, hop, hop! Three birds on one elephant.", beat="obstacle2", tag="three birds on one elephant", actors=TREE_RIDE, hide=["milo"],
      fx=[("fromto", "w:Hop,", "#{p}pip_w", {"x": 1300, "y": 950}, {"x": riders(860, 930, .62)[2][2], "y": riders(860, 930, .62)[2][3], "duration": .45, "ease": "power1.out"}, "Pip hops on"),
          ("fromto", "w:hop,", "#{p}kiki_w", {"x": 1440, "y": 962}, {"x": riders(860, 930, .62)[1][2], "y": riders(860, 930, .62)[1][3], "duration": .45, "ease": "power1.out"}, "Kiki hops on"),
          ("fromto", "w:hop!", "#{p}bo_w", {"x": 1580, "y": 950}, {"x": riders(860, 930, .62)[0][2], "y": riders(860, 930, .62)[0][3], "duration": .45, "ease": "power1.out"}, "Bo hops on"),
          ("snd", "w:Hop,", "boing"), ("snd", "w:hop,", "boing"), ("snd", "w:hop!", "boing")],
      words=[("w:Three", "3 BIRDS!", .74, .2, 1.0, "sun")]),
    S("bigtree", (880, 600, 760), "Thank you, Tumble! This is a very good seat.", who="bo", beat="obstacle2", tag="Bo: a good seat", actors=TREE_RIDE, hide=["milo"],
      fx=[("hop", "w:Thank", "bo"), ("face", 0.02, "tumble", "happy")]),
    S("bigtree", (1060, 640, 1500), "And off they go. Sniff, sniff, sniff.", beat="obstacle2", tag="off they go again", actors=TREE_RIDE, hide=["milo"],
      fx=[TRUNK(-50), ("walk", 0.1, "tumble", 360, 3.6)] + [("walk", 0.1, w, 360, 3.6) for w in BIRDS], words=[("w:Sniff,", "SNIFF!", .3, .2, 1.0, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 3: one small pool, too deep in a crack for a little beak
    S("rocks", WIDE, "The smell stops at a pile of big rocks. Is the water here?", trans="iris", beat="obstacle3", tag="the rocks", actors=ROCKS_RIDE, cam2=(940, 560, 1800), props=[POOL()],
      move=dict({"tumble": (200, 960, .62)}, **ride_move(200, 960, .62)), fx=[TRUNK(-30), ("walk", 0.1, "tumble", 320, 3.0)] + [("walk", 0.1, w, 320, 3.0) for w in BIRDS],
      words=[("w:rocks.", "BIG ROCKS", .7, .3, .9, "pill")]),
    S("rocks", (866, 960, 760), "Look! Down in a crack, one small pool of water.", beat="obstacle3", tag="one small pool", hide=only("rocks"), props=[POOL(), prop("ar", lambda p: art.arrow(p, 1080, 860, 930, 990), 0, 0, 1, True)],
      fx=[("show", "w:crack,", "ar"), ("snd", "w:pool", "ding")], words=[("w:one", "ONE SMALL POOL", .5, .13, .8, "sun")]),
    S("rocks", (960, 850, 780), "Water! Me first, me first!", who="pip", beat="obstacle3", tag="Pip: me first", hide=["tumble", "milo", "kiki", "bo"], props=[POOL()], move={"pip": (1050, 902, .5)},
      fx=[("hop", "w:Water!", "pip"), ("hop", "w:first,", "pip")]),
    S("rocks", (930, 900, 800), "Pip leans down. But the pool is too deep for a little beak.", beat="obstacle3", tag="too deep", hide=["tumble", "milo", "kiki", "bo"], move={"pip": (1050, 902, .5)},
      props=[POOL(), prop("ar", lambda p: art.arrow(p, 846, 908, 846, 972), 0, 0, 1, True)],
      fx=[("to", "w:leans", "#{p}pip", {"rotation": 42, "svgOrigin": "0 0", "duration": .6, "ease": "power2.inOut"}, "Pip leans down"), BEAK("w:down.", "pip"), ("show", "w:too", "ar"), ("face", "w:But", "pip", "sad")],
      words=[("w:too", "TOO DEEP!", .3, .2, .9, "pill")]),
    S("rocks", C("rocks", "kiki", "head", 700, -40, 20), "I cannot reach it. Not even on my tiptoes!", who="kiki", beat="obstacle3", tag="Kiki: cannot reach", hide=["tumble", "milo", "pip", "bo"],
      fx=[("face", 0.02, "kiki", "sad"), ("to", "w:tiptoes!", "#{p}kiki", {"y": "-=16", "duration": .25, "yoyo": True, "repeat": 3}, "Kiki stands on tiptoes")]),
    S("rocks", C("rocks", "bo", "head", 700, -40, 20), "So close. But we cannot get a drink.", who="bo", beat="obstacle3", tag="Bo: so close", hide=["tumble", "milo", "pip", "kiki"],
      fx=[("face", 0.02, "bo", "sad")], words=[("w:So", "SO CLOSE...", .7, .2, .8, "pill")]),
    S("rocks", C("rocks", "milo", "body", 820, 20, -70), "Who has a long, long nose to reach the water? Tumble, or Pip?", q=True, beat="obstacle3", tag="question: Tumble or Pip", pause=3.2, hide=["tumble"] + BIRDS,
      fx=[("signs", "w:Tumble,", ["TUMBLE", "PIP"], 0, "wait:2.0")]),
    S("rocks", C("rocks", "tumble", "head", 860, -20, 30), "My trunk is long. I can reach!", who="tumble", beat="obstacle3", tag="my trunk is long", hide=["milo"] + BIRDS, props=[POOL()],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:trunk", "tumble", -40, .3), ("trunk", "w:I", "tumble", 0, .3)], words=[("w:long.", "LONG TRUNK!", .27, .16, .85, "sun")]),
    S("rocks", (840, 860, 900), "Tumble dips his trunk in. Slurp! He sucks the water up.", beat="obstacle3", tag="slurp", hide=["milo"] + BIRDS, props=[POOL()],
      fx=[DIP("w:dips"), ("lookat", "w:dips", "tumble", 5), ("snd", "w:Slurp!", "whoosh"), ("to", "w:Slurp!", "#{p}pl-lv", {"y": 170, "duration": 1.8, "ease": "power1.inOut"}, "the water goes up the trunk")],
      words=[("w:Slurp!", "SLURP!", .76, .22, 1.1, "sun")]),
    S("paper_blue", (930, 620, 1300), "An elephant sucks water up its trunk. Then it blows the water into its mouth.", beat="fact", tag="fact: sucks up, blows in",
      actors=[("t", "tumble", 560, 900, .7)], props=[prop("pd", A.pond, 960, 902, 1.0), prop("n1", lambda p: A.num(p, 1), 1150, 760, 1.0, True), prop("n2", lambda p: A.num(p, 2), 1150, 480, 1.0, True),
                                                      prop("ar", lambda p: art.arrow(p, 1040, 640, 890, 668), 0, 0, 1, True), prop("dr", lambda p: A.drops3(p, 40, .2), 945, 800, 1.0, True)],
      fx=[("to", 0.1, "#{p}t-trunk", {"scaleY": 1.42, "svgOrigin": TP, "duration": .5, "ease": "power2.inOut"}, "the trunk dips into the water"), ("show", "w:sucks", "n1"),
          ("to", "w:Then", "#{p}t-trunk", {"scaleY": 1.0, "svgOrigin": TP, "duration": .4, "ease": "power2.inOut"}, "the trunk comes up"), ("show", "w:Then", "n2"), ("show", "w:blows", "ar"),
          ("fromto", "w:blows", "#{p}dr_w", {"x": 945, "y": 800, "opacity": 1}, {"x": 834, "y": 684, "opacity": 0, "duration": .55, "repeat": 3, "ease": "power1.in"}, "the water goes into the mouth")],
      words=[("w:sucks", "SUCK UP", .82, .69, .8, "sun"), ("w:blows", "BLOW IN", .82, .31, .8, "sun")]),
    # ------------------------------------------------------------ LOW MOMENT: one trunkful is all there is, and everybody is thirsty (gentle: nobody cries)
    S("rocks", (866, 960, 760), "But now the little pool is empty. That was the last drink.", beat="low", tag="the pool is empty", hide=only("rocks"), props=[POOL(170)],
      words=[("w:empty.", "EMPTY!", .5, .14, 1.0, "pill"), ("w:last", "THE LAST DRINK", .5, .3, .7, "sun")]),
    S("rocks", C("rocks", "tumble", "head", 860, 0, 20), "The water is in Tumble's trunk. And Tumble is so, so thirsty.", beat="low", tag="one trunkful", hide=["milo"] + BIRDS, props=[POOL(170), prop("wd", A.drop, 930, 720, .5, True)],
      fx=[("show", "w:trunk.", "wd"), ("face", "w:And", "tumble", "sad")], words=[("w:trunk.", "ONE TRUNKFUL", .3, .15, .75, "pill")]),
    S("rocks", (1390, 780, 960), "Three little birds look up at him. They are thirsty, too.", beat="low", tag="the birds look up", hide=["tumble", "milo"], props=[POOL(170)],
      fx=[("face", 0.02, "pip", "sad"), ("face", 0.02, "kiki", "sad"), ("face", 0.02, "bo", "sad"), ("to", "w:look", "#{p}pip,#{p}kiki,#{p}bo", {"rotation": 10, "svgOrigin": "0 0", "duration": .4}, "the birds look up")]),
    S("rocks", C("rocks", "tumble", "all", 1000, 60, -40), "If I drink it all, my friends get nothing.", who="tumble", beat="low", tag="if I drink it all", hide=["milo"] + BIRDS, props=[POOL(170)],
      fx=[("face", 0.02, "tumble", "sad"), ("lookat", "w:my", "tumble", 6)]),
    S("rocks", C("rocks", "tumble", "head", 780, -40, 10), "Oh, Milo. I do not know what to do.", who="tumble", beat="low", tag="I do not know", hide=["milo"] + BIRDS, props=[POOL(170)],
      fx=[("face", 0.02, "tumble", "sad"), ("blinkslow", "w:know", "tumble-eye", 1)]),
    S("rocks", C("rocks", "milo", "body", 820, 20, -70), "What should Tumble do? Drink it all, or share?", q=True, beat="low", tag="question: drink or share", pause=3.2, hide=["tumble"] + BIRDS,
      fx=[("signs", "w:Drink", ["DRINK", "SHARE"], 1, "wait:2.0")]),
    # ------------------------------------------------------------ SOLUTION: Tumble chooses to share, and the birds see the rain coming
    S("rocks", C("rocks", "tumble", "head", 800, -40, 10), "I know. Friends help friends. I will share!", who="tumble", beat="solution", tag="I will share", hide=["milo"] + BIRDS, props=[POOL(170)],
      fx=[("face", 0.02, "tumble", "sad"), ("face", "w:Friends", "tumble", "happy"), ("hop", "w:share!", "tumble")], words=[("w:share!", "SHARE!", .26, .2, 1.1, "sun")]),
    S("rocks", (970, 720, 1400), "Tumble lifts his trunk. Open your beaks, little birds!", beat="solution", tag="open your beaks", hide=["milo"], props=[POOL(170)],
      fx=[("trunk", "w:lifts", "tumble", -40, .5), BEAK("w:Open", "pip"), BEAK("w:Open", "kiki"), BEAK("w:Open", "bo")], words=[("w:Open", "OPEN WIDE!", .72, .25, .9, "pill")]),
    S("rocks", (990, 720, 1480), cam2=(990, 720, 1440), say="Squirt! A drink for Pip.", beat="solution", tag="a drink for Pip", hide=["milo"], props=[POOL(170), SQ("sq", "pip", 110)],
      fx=[TRUNK(-40), BEAK(0, "pip", 20, .01), ("show", "w:Squirt!", "sq"), ("snd", "w:Squirt!", "whoosh"), ("hop", "w:Pip.", "pip")],
      words=[("w:Squirt!", "SQUIRT!", .5, .14, 1.0, "sun"), ("w:Pip.", "1", .62, .37, 1.3, "sun")]),
    S("rocks", (990, 720, 1480), cam2=(990, 720, 1440), say="Squirt! A drink for Kiki.", beat="solution", tag="a drink for Kiki", hide=["milo"], props=[POOL(170), SQ("sq", "kiki", 150)],
      fx=[TRUNK(-40), BEAK(0, "kiki", 20, .01), ("show", "w:Squirt!", "sq"), ("snd", "w:Squirt!", "whoosh"), ("hop", "w:Kiki.", "kiki")],
      words=[("w:Squirt!", "SQUIRT!", .5, .14, 1.0, "sun"), ("w:Kiki.", "2", .76, .37, 1.3, "sun")]),
    S("rocks", (990, 720, 1480), cam2=(990, 720, 1440), say="Squirt! And a drink for Bo.", beat="solution", tag="a drink for Bo", hide=["milo"], props=[POOL(170), SQ("sq", "bo", 190)],
      fx=[TRUNK(-40), BEAK(0, "bo", 20, .01), ("show", "w:Squirt!", "sq"), ("snd", "w:Squirt!", "whoosh"), ("hop", "w:Bo.", "bo")],
      words=[("w:Squirt!", "SQUIRT!", .5, .14, 1.0, "sun"), ("w:Bo.", "3", .915, .37, 1.3, "sun")]),
    S("rocks", C("rocks", "tumble", "head", 860, 0, 10), "And the last three drops? Drip, drip, drip. Those are for Tumble.", beat="solution", tag="three drops for Tumble", hide=["milo"] + BIRDS,
      props=[POOL(170), prop("dr", lambda p: A.drops3(p, 60, .22), 880, 640, 1.0, True)],
      fx=[("show", "w:three", "dr"), ("to", "w:Drip,", "#{p}dr_w", {"x": P("rocks", "tumble", "mouth")[0], "y": P("rocks", "tumble", "mouth")[1], "scale": .4, "opacity": 0, "transformOrigin": "50% 50%", "duration": 1.3, "ease": "power1.in"}, "three drops go into his mouth"),
          ("face", "w:Those", "tumble", "happy")], words=[("w:Drip,", "DRIP!", .26, .2, 1.0, "sun")]),
    S("rocks", C("rocks", "milo", "body", 820, 20, 0), "How many birds got a drink? Count with me! One, two, three!", q=True, beat="solution", tag="question: count the birds", hide=["tumble"] + BIRDS,
      fx=[("count", "w:One,", 3, 1.3, {"x": 1420, "y": 420}), ("hop", "w:three!", "milo")]),
    S("rocks", C("rocks", "tumble", "head", 800, -40, 10), "It was only a tiny sip. But I feel so happy inside.", who="tumble", beat="solution", tag="happy inside", hide=["milo"] + BIRDS,
      props=[POOL(170), prop("h1", lambda p: art2.heart(p), 560, 560, .9, True)], fx=[("face", 0.02, "tumble", "happy"), ("show", "w:happy", "h1"), ("blinkslow", "w:happy", "tumble-eye", 1)]),
    S("rocks", C("rocks", "pip", "head", 760, -60, 20), "Tweet, tweet, tweet! Thank you, Tumble!", who="pip", beat="solution", tag="Pip: thank you", hide=["tumble", "milo", "kiki", "bo"],
      fx=[("hop", "w:Thank", "pip")], words=[("w:Thank", "THANK YOU!", .72, .2, .85, "pill")]),
    S("rocks", (1390, 760, 1040), who="", sing=SING_TY, beat="song", tag="song: the birds' thank-you tune", hide=["tumble", "milo"], props=[POOL(170)],
      fx=[("hop", TB(0), "pip"), ("hop", TB(.5), "kiki"), ("hop", TB(1), "bo"), WING(TB(2), "pip", 11), WING(TB(2), "kiki", 11), WING(TB(2), "bo", 11)],
      words=[(TB(0), "TWEET!", .2, .3, .9, "sun"), (TB(2), "THANK YOU!", .76, .24, .9, "pill")]),
    S("rocks", C("rocks", "kiki", "all", 900, -40, -120), "Now we can fly again. And look what I see!", who="kiki", beat="solution", tag="Kiki flies up", hide=["tumble", "milo", "pip", "bo"],
      fx=[WING(0.1, "kiki", 31), ("to", "w:fly", "#{p}kiki_w", {"y": "-=170", "duration": 1.0, "ease": "power1.out"}, "Kiki flies up"), ("face", "w:look", "kiki", "wow")]),
    S("rocks", (1100, 380, 1700), "Up in the sky, big gray clouds are coming.", beat="solution", tag="clouds", hide=only("rocks"), cam2=(1040, 400, 1800), props=CLOUDS(),
      fx=[("fromto", 0, "#{p}c1_w,#{p}c2_w,#{p}c3_w", {"x": "+=900"}, {"x": "-=900", "duration": 3.4, "ease": "power1.out"}, "the clouds come")], words=[("w:clouds", "RAIN CLOUDS!", .5, .62, .9, "pill")]),
    S("rocks", C("rocks", "bo", "head", 760, -40, -20), "Rain is coming, Tumble! Rain!", who="bo", beat="solution", tag="Bo: rain is coming", hide=["tumble", "milo", "pip", "kiki"], props=CLOUDS(),
      fx=[("hop", "w:Rain", "bo"), ("hop", "w:Rain!", "bo"), ("face", 0.02, "bo", "wow")]),
    S("rocks", WIDE, "Drip. Drop. Splash! Down comes the rain.", beat="solution", tag="the rain", cam2=(960, 560, 1800), hide=["milo"], props=[POOL(140)] + CLOUDS() + RAIN,
      fx=[RAINFX, ("face", 0.02, "tumble", "happy"), ("hop", "w:Splash!", "tumble"), ("hop", "w:Down", "pip"), ("hop", "w:comes", "kiki"), ("hop", "w:rain.", "bo"),
          ("to", 0.2, "#{p}pl-lv", {"y": 100, "duration": 4.0, "ease": "none"}, "")], words=[("w:Splash!", "RAIN!", .5, .34, 1.3, "sun")]),
    S("rocks", (866, 960, 760), "The little pool fills up. Up, up, up, to the very top.", beat="solution", tag="the pool fills up", hide=only("rocks"), props=[POOL(100)] + RAIN,
      fx=[RAINFX, ("to", "w:fills", "#{p}pl-lv", {"y": 0, "duration": 2.6, "ease": "power1.inOut"}, "the pool fills up")], words=[("w:top.", "FULL!", .5, .14, 1.1, "sun")]),
    S("rocks", (840, 860, 900), "Now I can have my big, cool drink. Slurp!", who="tumble", beat="solution", tag="the big drink", hide=["milo"] + BIRDS, props=[POOL(0)] + RAIN,
      fx=[RAINFX, ("face", 0.02, "tumble", "happy"), DIP("w:big,", 1.36), ("lookat", "w:big,", "tumble", 5), ("snd", "w:Slurp!", "whoosh")], words=[("w:Slurp!", "SLURP!", .76, .22, 1.1, "sun")]),
    S("rocks", C("rocks", "tumble", "head", 860, 0, 10), "Tumble drinks and drinks. Glug, glug, glug.", beat="solution", tag="glug", hide=["milo"] + BIRDS,
      props=[POOL(0), prop("dr", lambda p: A.drops3(p, 40, .2), 880, 760, 1.0, True)],
      fx=[("fromto", "w:Glug,", "#{p}dr_w", {"x": 880, "y": 770, "opacity": 1}, {"x": P("rocks", "tumble", "mouth")[0], "y": P("rocks", "tumble", "mouth")[1], "opacity": 0, "duration": .45, "repeat": 3, "ease": "power1.in"}, "the water goes into his mouth"),
          ("face", 0.02, "tumble", "happy"), ("blinkslow", "w:Glug,", "tumble-eye", 2)], words=[("w:Glug,", "GLUG!", .27, .2, 1.1, "sun")]),
    S("rocks", (700, 640, 1500), "Elephants squirt water over their bodies to keep cool.", beat="fact", tag="fact: squirt to keep cool", hide=["milo"] + BIRDS,
      props=[POOL(20), prop("sp", lambda p: f'<g transform="scale(-1.25 1.75)">{art2.spray(p)}</g>', 846, 536, 1.0, True)],
      fx=[("trunk", 0.1, "tumble", -150, .6), ("show", "w:squirt", "sp"), ("snd", "w:squirt", "whoosh"), FLAP("w:cool.", n=5), ("face", 0.02, "tumble", "happy")],
      words=[("w:squirt", "SQUIRT!", .74, .2, 1.0, "sun"), ("w:cool.", "= COOL!", .76, .38, 1.0, "")]),
    S("rocks", (1390, 800, 1040), "The birds splash in the puddles. Splish, splash, splosh!", beat="solution", tag="the birds splash", hide=["tumble", "milo"],
      props=[prop("p1", A.puddle, 1180, 936, .9), prop("p2", A.puddle, 1380, 950, .9), prop("p3", A.puddle, 1600, 940, .9), prop("r1", A.ripple, 1180, 930, 1.0, True), prop("r2", A.ripple, 1380, 942, 1.0, True), prop("r3", A.ripple, 1600, 934, 1.0, True)],
      fx=[("hop", "w:Splish,", "pip"), ("hop", "w:splash,", "kiki"), ("hop", "w:splosh!", "bo"), ("show", "w:Splish,", "r1", .5), ("show", "w:splash,", "r2", .5), ("show", "w:splosh!", "r3", .5), WING("w:birds", "pip", 7)],
      words=[("w:Splish,", "SPLASH!", .5, .2, 1.1, "sun")]),
    # ------------------------------------------------------------ WARM ENDING: home to Mama
    S("zoo_eve", WIDE, "Back at the zoo, the rain has stopped. And Mama is waiting.", trans="iris", beat="ending", tag="back at the zoo", cam2=(1000, 560, 1800),
      move=dict({"tumble": (300, 940, .6)}, **ride_move(300, 940, .6)), fx=[("walk", 0.1, "tumble", 360, 3.2)] + [("walk", 0.1, w, 360, 3.2) for w in BIRDS], words=[("w:Mama", "HOME!", .5, .16, 1.0, "sun")]),
    S("zoo_eve", C("zoo_eve", "tumble", "all", 1000, 40, -60), "Mama! I found water. And I found three new friends!", who="tumble", beat="ending", tag="three new friends", hide=["mama", "milo"],
      fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:three", "pip"), ("hop", "w:new", "kiki"), ("hop", "w:friends!", "bo")]),
    S("zoo_eve", C("zoo_eve", "pip", "head", 760, -60, 40), "Tumble gave us his last drink!", who="pip", beat="ending", tag="Pip: his last drink", hide=["mama", "milo"],
      fx=[("hop", "w:last", "pip")]),
    S("zoo_eve", C("zoo_eve", "mama", "head", 900, 60, 50), "You shared, even when you were thirsty. I am so proud of you.", who="mama", beat="ending", tag="Mama: so proud", hide=["milo", "tumble"] + BIRDS,
      fx=[("nod", "w:shared,", "mama"), ("blinkslow", "w:proud", "mama-eye", 1)], words=[("w:proud", "SO PROUD!", .2, .2, .8, "sun")]),
    S("zoo_eve", (1200, 660, 1400), "Mama wraps her trunk around Tumble. A big, warm trunk hug.", beat="ending", tag="trunk hug", hide=["milo"], move=dict({"tumble": (900, 940, .6)}, **ride_move(900, 940, .6)),
      props=[prop("h1", lambda p: art2.heart(p), 1030, 470, .7, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 1105, 440, .5, True)],
      fx=[("trunk", "w:wraps", "mama", 34, .8), ("lookat", "w:wraps", "mama", 8), ("show", "w:big,", "h1"), ("show", "w:hug.", "h2"),
          ("to", "w:big,", "#{p}h1_w,#{p}h2_w", {"y": "-=60", "duration": 1.6, "ease": "sine.out"}, "")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 130, 0), "When we share, everybody feels good inside.", beat="ending", tag="the lesson", hide=["mama", "tumble"] + BIRDS,
      words=[("w:share,", "SHARING IS KIND", .73, .22, .72, "pill")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 40, 0), "Do you remember? What does an elephant use to smell water? Its trunk, or its tail?", q=True, beat="ending", tag="question: trunk or tail", pause=3.2,
      hide=["mama", "tumble"] + BIRDS, cam2=C("zoo_eve", "milo", "body", 830, 40, -60), fx=[("signs", "w:trunk,", ["TRUNK", "TAIL"], 0, "wait:2.0")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 40, 0), "And where does an elephant blow the water? Into its mouth, or into its ear?", q=True, beat="ending", tag="question: mouth or ear", pause=3.2,
      hide=["mama", "tumble"] + BIRDS, cam2=C("zoo_eve", "milo", "body", 830, 40, -60), fx=[("signs", "w:mouth,", ["MOUTH", "EAR"], 0, "wait:2.0")]),
    S("zoo_eve", (980, 560, 1880), "Friends help friends. Hooray, hooray! What a rainy, happy day!", beat="ending", tag="the rhyme", cam2=(1000, 560, 1780),
      fx=[("hop", "w:Hooray,", "milo"), ("hop", "w:hooray!", "tumble"), ("nod", "w:rainy,", "mama")], words=[("w:Friends", "FRIENDS HELP FRIENDS", .5, .15, .6, "pill")]),
    S("zoo_eve", WIDE, who="", sing=SING_END_A, beat="song", tag="song: hooray", cam2=(980, 560, 1880),
      fx=[("hop", 1.0, "tumble"), ("hop", 1.0, "pip"), ("hop", 1.0, "kiki"), ("hop", 1.0, "bo"), ("nod", 3.2, "mama")], words=[(TB(3), "HOORAY!", .5, .2, 1.05, "sun")]),
    S("zoo_eve", (1145, 620, 1500), who="", sing=SING_END_B, beat="song", tag="song: rainy happy day", cam2=(1145, 620, 1420), hide=["milo"],
      props=[prop("h1", lambda p: art2.heart(p), 1010, 370, .9, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 930, 320, .6, True)],
      fx=[("nod", 1.6, "mama"), ("show", TB(1.5), "h1"), ("show", TB(3.5), "h2"), WING(3.0, "pip", 9), WING(3.0, "kiki", 9), WING(3.0, "bo", 9)]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 0, 0), "See you on the next adventure, friends!", beat="ending", tag="goodbye", hide=["mama", "tumble"] + BIRDS, fx=[("hop", "w:next", "milo")],
      words=[("w:next", "SEE YOU SOON!", .78, .17, .72, "pill")]),
]

# thumbnail (thumb.py): the example in the picture (Tumble squirts a drink to three little birds), 3 words at most, none of the title's words, no watermark
THUMBS = {
    "za_ep03": {"place": "rocks", "cam": (960, 640, 1500),
                "actors": [("tumble", 520, 960, .62, False, 'gsap.set("#P-trunk",{rotation:-40,svgOrigin:"392 -430"});'),
                           ("bird_pip", 1200, 930, .5, True, f'gsap.set("#P-jaw",{{rotation:20,svgOrigin:"{JAW["pip"]}"}});'),
                           ("bird_kiki", 1370, 940, .5, True, f'gsap.set("#P-jaw",{{rotation:20,svgOrigin:"{JAW["kiki"]}"}});'),
                           ("bird_bo", 1540, 930, .5, True, f'gsap.set("#P-jaw",{{rotation:20,svgOrigin:"{JAW["bo"]}"}});')],
                "props": [(lambda p: A.pool(p, 58), 866, 1056, 1.0), (SQ("sq", "bo", 190)[1], SQ_FROM[0], SQ_FROM[1], 1.0)],
                "words": [("SQUIRT!", 1180, 330, 190, "sun")]},
}
