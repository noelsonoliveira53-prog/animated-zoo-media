"""za_ep16 - Milo's Zoo Adventures: "Can Little Clover Lead the Sheep Home?" (theme title "Clover Leads the Flock Home"; cartoon adventure, the
3D music-and-sync process: "beat"). Farm week, adventure 1: the first story with Clover the lamb.
Milo visits Clover on the farm. It is almost supper time and Clover wants to lead the flock (three big sheep: Woolly, Daisy, Bramble) home from the
meadow all by herself. She calls (her voice is too little, the sheep keep munching), she pushes Woolly (he is much too big), she runs round and round
the flock (she gets dizzy, sits and takes a big breath). Low moment: "I am too little. Maybe I can not lead the flock home." (a little sad, never
crying; Milo stays with her). Then Clover SEES Daisy walk to new grass and the others follow her, and has her own idea: not to push, but to walk
first. She walks, the flock follows her down the lane, the rhyme is said, the tune is played on instruments, Mama is proud, supper in the barn.
Nobody is hurt, lost, crying or trapped; nobody is in danger: the sheep are never far from home and the sun going down only means supper time.

FACTS, read at the source on Nov 27 2026, about 3:20 PM ET by the session's clock (each page fetched by the session's page reader, which quoted these sentences verbatim):
 [BK] Britannica Kids (Students), "sheep", kids.britannica.com/students/article/sheep/277023
   "Sheep live in flocks."   "They follow a leader, usually an old ram (male sheep)."
   "They eat grasses and other plants."   "They like to graze over wide areas of pasture."
 [S101] Sheep 101, "Sheep behavior" (Susan Schoenian, updated 19-Apr-2021), sheep101.info/201/behavior.html
   "Sheep are best known for their strong flocking (herding) and following instinct."
   "When one sheep moves, the rest will follow, even if it does not seem to be a good idea."
   "Even from birth, lambs learn to follow the older members of the flock."   "Sheep are very social animals."
 Said as facts in the film (three fact boards, questions, recap): sheep live together in a flock [BK, S101]; sheep eat grass and other plants and
 like to graze over a wide meadow [BK]; sheep like to follow each other: when one sheep moves, the rest will follow [S101, BK].
 NOT said as facts: who usually leads a flock (the sources say an old ram or the dominant sheep: a lamb leading is THIS story), anything about wool,
 hay, sheepdogs or what lambs drink. Supper in the barn is "sweet, dry grass" (grass: [BK]); the rhyme and the tune are this story.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep13 as A13
import art_za_ep16 as A
import kit
from kit import Kit, S, prop
from intro import INTRO_STAGES, intro_shots      # the main intro, right after the hook and as the last shots (owner, Nov 20 4:50 PM)

EP = {"id": "za_ep16", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "clover": {"voice": "af_bella", "speed": .88, "pitch": 4, "formant": 1.2, "gain": .9},
               "mama": {"voice": "af_sarah", "speed": .85, "gain": .95}},
      "title": "Can Little Clover Lead the Sheep Home?", "thumb_text": "FOLLOW ME!",
      "series": "Milo's Zoo Adventures",
      "description": ("Can little Clover lead the big sheep home? It is almost supper time on the farm, and Clover the lamb wants to bring the flock home from the "
                      "meadow all by herself. She calls, she pushes, she runs round and round... but the big sheep just munch, munch, munch! Then Clover sees "
                      "something, and has her very own idea. A gentle farm adventure for ages 2-6 about trying again and going first, with questions to answer, "
                      "a count-along, moves to copy and a little tune.\n"
                      "Kids see how sheep live together in a flock, how sheep eat grass and other plants in a wide meadow, and how sheep like to follow each "
                      "other: when one sheep moves, the rest will follow.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nBritannica Kids (sheep); Sheep 101, Sheep behavior (Susan Schoenian)."),
      "tags": ["sheep for kids", "lamb for kids", "farm animals for kids", "farm story for kids", "baby lamb", "flock of sheep", "animal stories for kids",
               "trying again", "friendship story for kids", "kids adventure cartoon", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

CL = lambda x, y, s=.52, f=False: ("clover", "lamb", x, y, s, f)
MA = lambda x, y, s=.74, f=False: ("mama", "sheep_mama", x, y, s, f)
WO = lambda x, y, s=.6, f=False: ("woolly", "sheep_woolly", x, y, s, f)
DA = lambda x, y, s=.6, f=False: ("daisy", "sheep_daisy", x, y, s, f)
BR = lambda x, y, s=.6, f=False: ("bramble", "sheep_bramble", x, y, s, f)
MI = lambda x, y, s=.6: ("milo", "milo", x, y, s, False, True)
# boxes (rig units): lamb and sheep -260..330 wide, 470 tall; at .6 a sheep is 156 left and 198 right of its feet, at .52 Clover is 135 and 172
FLOCK = [WO(760, 925), DA(1290, 940, f=True), BR(1710, 925, f=True)]                  # the flock grazing in the meadow: nobody inside another
MEADOW = [CL(300, 940), *FLOCK, MI(470, 520)]
LINE = [BR(330, 950), WO(720, 940), DA(1110, 950), CL(1540, 945), MI(1800, 620)]      # the line on the lane: Clover first
BARN = [WO(300, 935, .62), CL(850, 940), MA(1330, 935, f=True), MI(1040, 580)]
STAGES = {
    "farm": [CL(520, 935), MA(1200, 935, f=True), MI(300, 500)],
    "meadow": MEADOW, "meadow_gold": MEADOW,
    "lane": LINE,
    "farm_gold": [WO(230, 945, .56), CL(600, 940), MA(1240, 935, f=True), MI(900, 500)],
    "barn": BARN,
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
CH = lambda place, w=880, dx=120, dy=10, stage=None: C(place, "clover", "head", w, dx, dy, stage=stage)       # Clover's face on the left, room for words in front of her
MH = lambda place, w=980, dx=-110, dy=20, stage=None: C(place, "mama", "head", w, dx, dy, stage=stage)        # Mama (she faces left): her face on the right, words on the left
MB = lambda place, w=820, dx=0, dy=-40, stage=None: C(place, "milo", "body", w, dx, dy, stage=stage)          # Milo: low in the frame, under the signs
SOLO = ["milo", "woolly", "daisy", "bramble", "mama"]                                                           # hidden in Clover's close-ups (nobody half in the frame)

# ---- sheep that munch: the head goes down to the grass and the jaw works
DOWN = lambda at, who, deg=52: ("lookat", at, who, deg)
UP = lambda at, who: ("lookat", at, who, 0)
MUNCH = lambda at, who, n=6: ("to", at, "#{p}%s-jaw" % who, {"opacity": 1, "y": 9, "duration": .19, "yoyo": True, "repeat": 2 * n - 1, "ease": "sine.inOut"}, "%s munches" % who)
def GRAZE(at=0.0, n=14, who=("woolly", "daisy", "bramble")):
    return [x for k, w in enumerate(who) for x in (DOWN(at, w, 52 - 4 * k), MUNCH(at + .1 + .23 * k, w, n))]
TUFTS = lambda: [prop("tw", A.tuft, 1025, 942, .85), prop("tb", A.tuft, 1490, 936, .85)]      # grass at the mouths (Woolly and Daisy share one)
TW = lambda: [prop("tw", A.tuft, 1090, 935, .9)]                                              # the tuft big Woolly munches while Clover pushes
SPIN = lambda at, n=8: ("to", at, "#{p}dz-spin", {"rotation": 360, "transformOrigin": "50% 50%", "duration": 1.1, "repeat": n, "ease": "none"}, "the dizzy stars turn")
WOBBLE = lambda at, who="clover", n=7: ("to", at, "#{p}%s" % who, {"rotation": 5, "transformOrigin": "50% 100%", "duration": .45, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "%s wobbles" % who)
PUSH = lambda at, n=13: ("to", at, "#{p}clover", {"x": "+=14", "duration": .2, "yoyo": True, "repeat": n}, "Clover pushes")

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. The rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_HOME = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~ ~", "notes": "E4:1 G4:1 C5:1 G4:1 D5:1 B4:1 G4:1", "rest": 1},      # follow, follow, one by one (C bar, G bar)
                                 {"text": "~ ~ ~ ~ ~ ~ ~", "notes": "A4:1 C5:1 F5:1 C5:1 E5:1 G4:1 C5:1", "rest": 1}])     # home together, day is done (F bar, C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "D5:1 B4:1 G4:1 B4:1 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune
CNT3 = 0.53                                      # seconds from "One" to "three" (set from the timing file)

PUSHERS = [CL(470, 940), WO(830, 925, .7)]                                                    # Clover right behind big Woolly
RUNFLOCK = [WO(700, 765, .5), DA(1160, 772, .5, f=True), BR(1580, 765, .5, f=True)]           # the flock further back while Clover runs along the front
# the solution: everybody faces right. Daisy walks to new grass, the others follow; then Clover walks first.
SEE = [BR(330, 930), WO(740, 940), DA(1150, 930), CL(1840, 945, f=True), MI(300, 430)]
SEEN = [BR(580, 930), WO(990, 940), DA(1410, 930), CL(1840, 945, f=True)]
GO = [BR(240, 935, .56), WO(620, 945, .56), DA(1000, 935, .56), CL(1400, 945), MI(1560, 420)]
SEECAM = (1040, 600, 1900)

SHOTS = [
    # ------------------------------------------------------------ HOOK: the promise (first 5 seconds): the sun is low, a little lamb, three big munching sheep
    S("meadow_gold", (960, 600, 1840), "Can little Clover lead the big sheep home? Look! The sun is going down. But the sheep just munch, and munch!", beat="hook",
      tag="hook: Clover and the munching flock", cam2=(990, 610, 1770), hide=["milo"], props=TUFTS(),
      fx=[*GRAZE(), ("face", 0.02, "clover", "wow"), ("hop", "w:Look!", "clover"), ("face", "w:But", "clover", "sad")],
      words=[("w:lead", "LEAD THE SHEEP?", .6, .14, .7, "sun"), ("w:munch,", "MUNCH, MUNCH!", .66, .3, .7, "pill")]),
    *intro_shots(),      # the main intro, right after the hook
    # ------------------------------------------------------------ GOAL: supper time; Clover wants to lead the flock home all by herself
    S("farm", WIDE, "Hello, I'm Milo! Today I am visiting Clover the lamb, on the sunny farm.", trans="iris", beat="goal", tag="the farm: Milo, Clover, Mama",
      cam2=(960, 570, 1800), fx=[("hop", "w:Hello,", "milo"), ("hop", "w:Clover", "clover"), ("nod", "w:farm.", "mama")],
      words=[("w:Clover", "CLOVER", .3, .57, .62, "pill"), ("w:sunny", "THE SUNNY FARM", .62, .12, .7, "sun")]),
    S("farm", CH("farm"), "It is almost supper time! Today, I want to lead the flock home. All by myself!", who="clover", beat="goal", tag="Clover: I want to lead the flock home",
      hide=SOLO, fx=[("face", 0.02, "clover", "happy"), ("nod", "w:supper", "clover"), ("lookat", "w:lead", "clover", -10), ("nod", "w:myself!", "clover")],
      words=[("w:supper", "SUPPER TIME!", .72, .22, .7, "pill"), ("w:lead", "LEAD THE FLOCK!", .72, .4, .66, "sun")]),
    S("farm", MH("farm"), "The flock is up in the meadow, little one. Walk them home, before the sun goes down.", who="mama", beat="goal", tag="Mama: walk them home before sunset",
      hide=["clover", "milo"], fx=[("face", 0.02, "mama", "happy"), ("lookat", "w:meadow,", "mama", -10), ("nod", "w:little", "mama"), ("nod", "w:home,", "mama")],
      words=[("w:meadow,", "UP IN THE MEADOW", .3, .26, .6, "pill"), ("w:home,", "WALK THEM HOME", .3, .42, .6, "sun")]),
    S("farm", (860, 660, 1300), "I can do it, Mama! I am a big lamb now!", who="clover", beat="goal", tag="Clover: I can do it",
      cam2=(860, 670, 1240), hide=["milo"], fx=[("face", 0.02, "clover", "happy"), ("hop", "w:can", "clover"), ("nod", "w:big", "clover"), ("face", "w:Mama!", "mama", "happy")],
      words=[("w:can", "I CAN DO IT!", .5, .14, .8, "sun")]),
    S("farm", (800, 700, 1500), "Who wants to lead the flock home? Clover, or Milo?", q=True, beat="goal", tag="question: Clover or Milo", pause=3.2,
      cam2=(800, 710, 1420), actors=[CL(520, 935), MI(1100, 800)], fx=[("face", 0.02, "clover", "happy"), ("hop", 0.5, "clover"), ("signs", "w:Clover,", ["CLOVER", "MILO"], 0, "wait:1.8")]),
    S("paper", (960, 520, 1560), "Sheep live together, in a big group. It is called a flock.", beat="fact", tag="fact: sheep live in a flock",
      cam2=(960, 530, 1480), actors=[WO(430, 820, .62), DA(900, 820, .62), BR(1370, 820, .62)],
      fx=[("nod", "w:together,", "woolly"), ("nod", "w:big", "daisy"), ("nod", "w:group.", "bramble"), ("hop", "w:flock.", "woolly"), ("hop", "w:flock.", "daisy"), ("hop", "w:flock.", "bramble")],
      words=[("w:together,", "TOGETHER", .5, .12, .7, "pill"), ("w:flock.", "A FLOCK!", .5, .27, .95, "sun")]),
    S("paper", (960, 560, 1560), "What is a group of sheep called? A flock, or a sock?", q=True, beat="fact", tag="question: flock or sock", pause=3.2, cam2=(960, 570, 1500),
      actors=[WO(380, 860, .5), DA(720, 860, .5), BR(1060, 860, .5)], props=[prop("sk", A.sock, 1480, 700, .9)],
      fx=[("to", 0.4, "#{p}sk_w", {"rotation": 8, "transformOrigin": "50% 50%", "duration": .5, "yoyo": True, "repeat": 13, "ease": "sine.inOut"}, "the sock wiggles"),
          ("signs", "w:flock,", ["FLOCK", "SOCK"], 0, "wait:1.8")]),
    S("meadow", WIDE, "Clover and Milo skip up the hill, to the green meadow. And there is the flock!", trans="iris", beat="goal", tag="the meadow: there is the flock",
      cam2=(990, 560, 1800), actors=[CL(40, 940), *FLOCK, MI(250, 480)], props=TUFTS(),
      fx=[*GRAZE(), ("walk", 0.1, "clover", 260, 3.0), ("fly", 0.2, "milo", 470, 520, 2.8), ("hop", "w:there", "clover")],
      words=[("w:meadow.", "THE GREEN MEADOW", .62, .12, .66, "sun"), ("w:flock!", "THE FLOCK!", .66, .28, .75, "pill")]),
    S("meadow", (1250, 640, 1440), "Count the big sheep with Milo! One, two, three!", q=True, beat="goal", tag="count three sheep", pause=1.2,
      cam2=(1250, 650, 1400), hide=["clover", "milo"], props=TUFTS(),
      fx=[*GRAZE(), ("count", "w:One,", 3, CNT3, {"x": 960, "y": 230}), ("hop", "w:One,", "woolly"), ("hop", "w:two,", "daisy"), ("hop", "w:three!", "bramble")],
      words=[("w:Count", "COUNT!", .2, .3, .8, "sun")]),
    S("meadow", (1250, 650, 1440), "Here are Woolly, Daisy, and Bramble. They are very busy. Munch, munch, munch!", beat="goal", tag="Woolly, Daisy and Bramble munch",
      cam2=(1250, 660, 1400), hide=["clover", "milo"], props=TUFTS(),
      fx=[*GRAZE(), ("word", "w:Woolly,", "WOOLLY", {"x": 780, "y": 560, "size": 56, "cls": "pill"}), ("word", "w:Daisy,", "DAISY", {"x": 1270, "y": 575, "size": 56, "cls": "pill"}),
          ("word", "w:Bramble.", "BRAMBLE", {"x": 1700, "y": 560, "size": 56, "cls": "pill"})],
      words=[("w:Munch,", "MUNCH, MUNCH!", .5, .14, .7, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: Clover calls (her voice is too little)
    S("meadow", CH("meadow"), "Time to go home, everyone! Baa! Baa!", who="clover", beat="obstacle1", tag="Clover calls: time to go home",
      hide=SOLO, fx=[("face", 0.02, "clover", "happy"), ("nod", "w:home,", "clover"), ("hop", "w:Baa!", "clover"), ("hop", "w:Baa!:2", "clover")],
      words=[("w:Baa!", "BAA! BAA!", .74, .26, .9, "sun")]),
    S("meadow", (960, 600, 1840), "But Clover's voice is very little. The big sheep do not look up. Munch, munch, munch.", beat="obstacle1", tag="the sheep do not look up",
      cam2=(1000, 610, 1760), hide=["milo"], props=TUFTS(), fx=[*GRAZE(), ("face", 0.02, "clover", "happy"), ("face", "w:do", "clover", "sad")],
      words=[("w:little.", "A LITTLE VOICE", .3, .36, .6, "pill"), ("w:Munch,", "MUNCH, MUNCH!", .66, .14, .7, "sun")]),
    S("meadow", (540, 700, 1300), "Can you call, like Clover? Baa! Baa!", q=True, beat="obstacle1", tag="copy me: call baa", pause=3.0, cam2=(540, 710, 1220),
      actors=[CL(330, 940), MI(820, 780)], fx=[("face", 0.02, "clover", "happy"), ("hop", "w:Baa!", "clover"), ("hop", "w:Baa!:2", "clover"), ("hop", "wait:0.5", "clover", 2), ("hop", "wait:1.6", "milo")],
      words=[("w:Baa!", "BAA! BAA!", .56, .14, .9, "sun"), ("wait:0.4", "YOUR TURN!", .56, .3, .7, "pill")]),
    S("paper_blue", (960, 520, 1560), "Sheep eat grass, and other plants. They like to munch all over a wide, green meadow.", beat="fact", tag="fact: sheep eat grass and other plants",
      cam2=(960, 530, 1480), actors=[DA(520, 790, .8)], props=[prop("g1", A.tuft, 900, 790, 1.4), prop("g2", A.tuft, 1220, 790, 1.8), prop("g3", A.tuft, 1540, 790, 1.4)],
      fx=[DOWN(0.0, "daisy", 46), MUNCH(0.2, "daisy", 16), ("to", "w:grass,", "#{p}g1_w", {"scale": 1.12, "transformOrigin": "50% 100%", "duration": .25, "yoyo": True, "repeat": 3}, "the grass pulses"),
          ("to", "w:plants.", "#{p}g2_w", {"scale": 1.12, "transformOrigin": "50% 100%", "duration": .25, "yoyo": True, "repeat": 3}, "the plants pulse"),
          ("to", "w:wide,", "#{p}g3_w", {"scale": 1.12, "transformOrigin": "50% 100%", "duration": .25, "yoyo": True, "repeat": 3}, "more grass pulses")],
      words=[("w:grass,", "GRASS!", .6, .14, .95, "sun"), ("w:plants.", "AND OTHER PLANTS", .66, .3, .6, "pill")]),
    S("paper_blue", (960, 560, 1560), "What do sheep eat? Grass, or cake?", q=True, beat="fact", tag="question: grass or cake", pause=3.2, cam2=(960, 570, 1500),
      actors=[DA(900, 860, .7)], props=[prop("g1", A.tuft, 1230, 860, 1.3)], fx=[DOWN(0.0, "daisy", 46), MUNCH(0.2, "daisy", 18), ("signs", "w:Grass,", ["GRASS", "CAKE"], 0, "wait:1.8")]),
    S("meadow", (1000, 660, 1780), "Did the sheep come when Clover called? Yes, or no?", q=True, beat="obstacle1", tag="question: did the sheep come", pause=3.2, cam2=(1010, 670, 1740),
      hide=["milo"], props=TUFTS(), fx=[*GRAZE(n=18), ("face", 0.02, "clover", "sad"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    S("meadow", CH("meadow"), "Oh. They did not hear me. I need a new idea.", who="clover", beat="obstacle1", tag="Clover: I need a new idea",
      hide=SOLO, fx=[("face", 0.02, "clover", "sad"), ("nod", "w:hear", "clover"), ("face", "w:new", "clover", "happy")],
      words=[("w:new", "A NEW IDEA", .74, .26, .8, "pill")]),
    # ------------------------------------------------------------ OBSTACLE 2: Clover pushes Woolly (he is much too big)
    S("meadow", (760, 640, 1340), "So Clover walks behind big Woolly. And she pushes!", beat="obstacle2", tag="Clover walks behind Woolly and pushes", trans="iris",
      cam2=(780, 650, 1280), actors=[CL(240, 940), WO(830, 925, .7), MI(1260, 540)], props=TW(),
      fx=[*GRAZE(who=("woolly",)), ("walk", 0.2, "clover", 230, 2.2), PUSH("w:pushes!", 5)],
      words=[("w:pushes!", "PUSH!", .5, .14, .95, "sun")]),
    S("meadow", C("meadow", "clover", "head", 900, 60, 20, stage=PUSHERS), "Push, push, push! Please move, Woolly!", who="clover", beat="obstacle2", tag="Clover: push, push, push",
      actors=PUSHERS, props=TW(), fx=[*GRAZE(who=("woolly",)), ("face", 0.02, "clover", "wow"), PUSH(0.2)],
      words=[("w:Push,", "PUSH, PUSH!", .36, .14, .8, "sun")]),
    S("meadow", (760, 620, 1360), "But Woolly is big, and Clover is small. Woolly does not move one bit.", beat="obstacle2", tag="Woolly does not move",
      cam2=(780, 630, 1300), actors=[*PUSHERS, MI(1260, 540)], props=TW(),
      fx=[*GRAZE(who=("woolly",)), ("face", 0.02, "clover", "sad"), ("fly", "w:Woolly:2", "milo", 1220, 580, 1.0)],
      words=[("w:big,", "SO BIG!", .6, .14, .85, "sun"), ("w:small.", "SO SMALL!", .3, .4, .7, "pill")]),
    S("meadow", (660, 700, 1300), "Can you push, like Clover? Push, push, push!", q=True, beat="obstacle2", tag="copy me: push", pause=3.0, cam2=(670, 710, 1240),
      actors=PUSHERS, props=TW(), fx=[*GRAZE(who=("woolly",), n=20), ("face", 0.02, "clover", "wow"), PUSH("w:Push,", 23)],
      words=[("w:Push,", "PUSH, PUSH, PUSH!", .5, .12, .78, "sun"), ("wait:0.4", "YOUR TURN!", .5, .27, .7, "pill")]),
    S("meadow", (700, 700, 1400), "Did Woolly move? Yes, or no?", q=True, beat="obstacle2", tag="question: did Woolly move", pause=3.2, cam2=(720, 710, 1340),
      actors=[CL(400, 940), WO(830, 925, .7)], props=TW(), fx=[*GRAZE(who=("woolly",), n=18), ("face", 0.02, "clover", "sad"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    S("meadow", CH("meadow", stage=[CL(400, 940)]), "Oh my! Pushing is too hard for me.", who="clover", beat="obstacle2", tag="Clover: pushing is too hard",
      actors=[CL(400, 940)], fx=[("face", 0.02, "clover", "sad"), ("nod", "w:hard", "clover")], words=[("w:hard", "TOO HARD!", .74, .26, .85, "pill")]),
    # ------------------------------------------------------------ OBSTACLE 3: round and round the flock (she gets dizzy)
    S("meadow_gold", WIDE, "The sun slides lower. Clover has one more idea. She will run around the flock!", trans="iris", beat="obstacle3", tag="the sun is lower: one more idea",
      cam2=(990, 560, 1800), props=TUFTS(), fx=[*GRAZE(), ("face", 0.02, "clover", "happy"), ("hop", "w:idea.", "clover"), ("fly", "w:run", "milo", 560, 480, 1.4)],
      words=[("w:lower.", "THE SUN IS LOW", .62, .12, .68, "sun"), ("w:run", "RUN AROUND!", .66, .28, .7, "pill")]),
    S("meadow_gold", (960, 630, 1840), "Round and round I go! Come on, everyone!", who="clover", beat="obstacle3", tag="Clover runs round the flock",
      cam2=(980, 635, 1800), actors=[*RUNFLOCK, CL(170, 1015)], props=[prop("tw", A.tuft, 930, 776, .7), prop("tb", A.tuft, 1390, 770, .7)],
      fx=[*GRAZE(), ("face", 0.02, "clover", "happy"), ("walk", 0.1, "clover", 1500, 3.3)], words=[("w:Round", "ROUND AND ROUND!", .6, .12, .7, "sun")]),
    S("meadow_gold", (700, 640, 1400), "Round, and round, and round. But the sheep only watch. And now Clover is dizzy!", beat="obstacle3", tag="the sheep watch, Clover is dizzy",
      cam2=(690, 655, 1300), actors=[CL(420, 945), WO(1060, 925, .66, f=True)], props=[prop("dz", A.dizzy, 535, 655, .9, True)],
      fx=[("face", 0.02, "clover", "happy"), ("to", 0.1, "#{p}clover", {"rotation": 6, "transformOrigin": "50% 100%", "duration": .3, "yoyo": True, "repeat": 9}, "Clover turns and turns"),
          ("lookat", 0.3, "woolly", -6), MUNCH("w:sheep", "woolly", 5), ("face", "w:dizzy!", "clover", "wow"), ("show", "w:dizzy!", "dz"), SPIN("w:dizzy!"), WOBBLE("w:dizzy!")],
      words=[("w:watch.", "THEY ONLY WATCH", .68, .16, .6, "pill"), ("w:dizzy!", "DIZZY!", .36, .22, .9, "sun")]),
    S("meadow_gold", (640, 700, 1300), "How does Clover feel? Dizzy, or sleepy?", q=True, beat="obstacle3", tag="question: dizzy or sleepy", pause=3.2, cam2=(640, 710, 1220),
      actors=[CL(520, 945), MI(980, 800)], props=[prop("dz", A.dizzy, 635, 655, .9)], fx=[("face", 0.02, "clover", "wow"), SPIN(0.0, 9), WOBBLE(0.1, n=17), ("signs", "w:Dizzy,", ["DIZZY", "SLEEPY"], 0, "wait:1.8")]),
    S("meadow_gold", (700, 700, 1300), "Take a big breath with Clover. In, and out.", q=True, beat="obstacle3", tag="copy me: a big breath", pause=3.0, cam2=(700, 710, 1220),
      actors=[CL(520, 945), MI(960, 790)],
      fx=[("face", 0.02, "clover", "happy"), ("to", "w:In,", "#{p}clover", {"scale": 1.08, "transformOrigin": "50% 100%", "duration": .9, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "Clover breathes in and out"),
          ("to", "w:In,", "#{p}milo", {"scale": 1.08, "transformOrigin": "50% 100%", "duration": .9, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "Milo breathes in and out")],
      words=[("w:In,", "IN...", .4, .14, .9, "sun"), ("w:out.", "AND OUT...", .68, .14, .9, "pill"), ("wait:0.6", "YOUR TURN!", .54, .3, .7, "sun")]),
    # ------------------------------------------------------------ LOW MOMENT: I am too little (gentle: nobody cries, Milo stays)
    S("meadow_gold", (960, 600, 1840), "The sky turns gold. The big sheep are still munching. Clover feels a little sad.", beat="low", tag="gold sky, Clover a little sad",
      cam2=(980, 610, 1780), hide=["milo"], props=TUFTS(), fx=[*GRAZE(), ("face", 0.02, "clover", "sad"), ("lookat", "w:sad.", "clover", 12)],
      words=[("w:gold.", "A GOLD SKY", .62, .12, .7, "sun"), ("w:sad.", "A LITTLE SAD", .3, .44, .6, "pill")]),
    S("meadow_gold", CH("meadow_gold"), "I am too little. Maybe I can not lead the flock home.", who="clover", beat="low", tag="Clover: maybe I can not lead the flock",
      hide=SOLO, fx=[("face", 0.02, "clover", "sad"), ("nod", "w:little.", "clover"), ("lookat", "w:Maybe", "clover", 10)],
      words=[("w:little.", "TOO LITTLE?", .74, .26, .85, "pill")]),
    S("meadow_gold", (500, 680, 1200), "It's okay, Clover. I am right here with you.", beat="low", tag="Milo: I am right here",
      cam2=(500, 690, 1140), actors=[CL(300, 940), MI(720, 590)], fx=[("face", 0.02, "clover", "sad"), ("fly", 0.2, "milo", 660, 780, 1.2), ("hop", "w:right", "milo"), ("face", "w:here", "clover", "happy")],
      words=[("w:right", "RIGHT HERE", .6, .14, .85, "sun")]),
    S("meadow_gold", (460, 720, 1200), "How does Clover feel now? Sad, or happy?", q=True, beat="low", tag="question: sad or happy", pause=3.2, cam2=(460, 730, 1140),
      actors=[CL(300, 940), MI(700, 860)], fx=[("face", 0.02, "clover", "sad"), ("lookat", 0.4, "clover", 8), ("signs", "w:Sad,", ["SAD", "HAPPY"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: Clover sees how sheep follow, and has her own idea: walk first
    S("meadow_gold", SEECAM, "Then Clover sees something. Daisy walks to a new patch of grass.", beat="solution", tag="Daisy walks to new grass", trans="iris",
      cam2=(1060, 610, 1840), actors=SEE, props=[prop("g1", A.tuft, 1610, 940, .9)],
      fx=[("face", 0.02, "clover", "sad"), DOWN(0.0, "woolly"), DOWN(0.0, "bramble", 48), MUNCH(0.1, "woolly", 12), MUNCH(0.3, "bramble", 12), ("face", "w:sees", "clover", "wow"),
          ("walk", "w:Daisy", "daisy", 260, 2.2), DOWN("e:grass.", "daisy", 46)],
      words=[("w:sees", "LOOK!", .8, .3, .85, "sun"), ("w:new", "NEW GRASS", .62, .14, .7, "pill")]),
    S("meadow_gold", SEECAM, "And look! Woolly follows Daisy. And Bramble follows Woolly!", beat="solution", tag="Woolly and Bramble follow",
      cam2=(1060, 610, 1840), actors=[BR(330, 930), WO(740, 940), DA(1410, 930), CL(1840, 945, f=True), MI(300, 430)], props=[prop("g1", A.tuft, 1610, 940, .9)],
      fx=[("face", 0.02, "clover", "wow"), DOWN(0.0, "daisy", 46), MUNCH(0.1, "daisy", 16), ("walk", "w:Woolly", "woolly", 250, 1.8), ("walk", "w:Bramble", "bramble", 250, 1.8), ("hop", "e:Woolly!", "clover")],
      words=[("w:follows", "FOLLOW!", .54, .14, .85, "sun"), ("w:follows:2", "FOLLOW!", .38, .32, .75, "pill")]),
    S("meadow_gold", (1100, 680, 1840), "What did the other sheep do? Follow, or fly?", q=True, beat="solution", tag="question: follow or fly", pause=3.2, cam2=(1110, 690, 1780),
      actors=SEEN, props=[prop("g1", A.tuft, 1610, 940, .9)],
      fx=[*GRAZE(n=18), ("face", 0.02, "clover", "wow"), ("signs", "w:Follow,", ["FOLLOW", "FLY"], 0, "wait:1.8")]),
    S("meadow_gold", (1095, 778, 800), "I know! Sheep like to follow! I will not push. I will walk first!", who="clover", beat="solution", tag="Clover's idea: I will walk first",
      actors=[CL(1300, 945, f=True)], props=[prop("bulb", A13.think_bulb, 1100, 655, .6, True)],
      fx=[("face", 0.02, "clover", "wow"), ("show", "w:know!", "bulb"), ("face", "w:Sheep", "clover", "happy"), ("nod", "w:follow!", "clover"), ("hop", "w:walk", "clover")],
      words=[("w:follow!", "SHEEP FOLLOW!", .26, .32, .66, "sun"), ("w:walk", "WALK FIRST!", .26, .48, .66, "pill")]),
    S("paper_pink", (960, 520, 1600), "Sheep like to follow each other. When one sheep moves, the rest will follow.", beat="fact", tag="fact: when one sheep moves the rest follow",
      cam2=(980, 530, 1540), actors=[BR(330, 820, .56), WO(720, 820, .56), DA(1110, 820, .56)], props=[prop("ar", A.arrow, 1570, 430, 1.0)],
      fx=[("walk", "w:When", "daisy", 240, 1.6), ("walk", "w:rest", "woolly", 240, 1.6), ("walk", "w:rest", "bramble", 240, 1.6),
          ("to", "w:follow", "#{p}ar_w", {"x": "+=40", "duration": .35, "yoyo": True, "repeat": 9, "ease": "sine.inOut"}, "the arrow points the way")],
      words=[("w:follow", "FOLLOW!", .5, .12, .95, "sun"), ("w:rest", "THE REST FOLLOW", .44, .28, .62, "pill")]),
    S("paper_pink", (960, 560, 1600), "When one sheep moves, what do the others do? Follow, or hide?", q=True, beat="fact", tag="question: follow or hide", pause=3.2, cam2=(960, 570, 1560),
      actors=[BR(420, 860, .56), WO(820, 860, .56), DA(1220, 860, .56)], props=[prop("ar", A.arrow, 1570, 640, .75)],
      fx=[("to", 0.3, "#{p}ar_w", {"x": "+=40", "duration": .35, "yoyo": True, "repeat": 17, "ease": "sine.inOut"}, "the arrow points the way"), ("signs", "w:Follow,", ["FOLLOW", "HIDE"], 0, "wait:1.8")]),
    S("meadow_gold", (1000, 600, 1880), "So Clover lifts her head up high. And she walks. Step, step, step.", beat="solution", tag="Clover walks first",
      cam2=(1010, 605, 1860), actors=GO, props=[prop("tb", A.tuft, 440, 940, .75), prop("tw", A.tuft, 820, 950, .75), prop("td", A.tuft, 1200, 942, .7)],
      fx=[DOWN(0.0, "bramble", 48), DOWN(0.0, "woolly"), DOWN(0.0, "daisy", 46), MUNCH(0.1, "bramble", 14), MUNCH(0.3, "woolly", 14), MUNCH(0.5, "daisy", 14),
          ("face", 0.02, "clover", "happy"), ("lookat", "w:lifts", "clover", -14), ("walk", "w:walks.", "clover", 160, 2.8)],
      words=[("w:high.", "HEAD UP HIGH!", .36, .14, .72, "sun"), ("w:Step,", "STEP, STEP, STEP!", .4, .3, .66, "pill")]),
    S("meadow_gold", (1000, 600, 1880), "Daisy looks up. And she follows Clover! Then Woolly. Then Bramble!", beat="solution", tag="the flock follows Clover",
      cam2=(1010, 605, 1860), actors=[BR(240, 935, .56), WO(620, 945, .56), DA(1000, 935, .56), CL(1560, 945), MI(1560, 420)],
      fx=[("face", 0.02, "clover", "happy"), ("lookat", 0.0, "clover", -14), DOWN(0.0, "woolly"), DOWN(0.0, "bramble", 48), DOWN(0.0, "daisy", 46), ("walk", 0.1, "clover", 180, 5.0), ("fly", 0.1, "milo", 1700, 400, 4.0),
          UP("w:looks", "daisy"), ("walk", "w:follows", "daisy", 240, 3.2), UP("w:Then", "woolly"), ("walk", "w:Then", "woolly", 240, 2.2), UP("w:Then:2", "bramble"), ("walk", "w:Then:2", "bramble", 240, 1.3)],
      words=[("w:follows", "DAISY FOLLOWS!", .5, .12, .66, "sun"), ("w:Woolly.", "WOOLLY!", .42, .27, .62, "pill"), ("w:Bramble!", "BRAMBLE!", .34, .4, .62, "pill")]),
    S("lane", WIDE, "Down the lane they go, in a line. Clover first, and the flock behind her.", trans="iris", beat="solution", tag="the lane: Clover first, the flock behind",
      cam2=(1000, 560, 1840), fx=[("face", 0.02, "clover", "happy"), ("lookat", 0.0, "clover", -12), *[("walk", 0.1, w, 100, 4.6) for w in ("clover", "daisy", "woolly", "bramble")], ("hop", "w:first,", "milo")],
      words=[("w:line.", "IN A LINE", .44, .12, .75, "sun"), ("w:first,", "CLOVER FIRST!", .7, .26, .64, "pill")]),
    S("lane", (960, 620, 1840), "Count the sheep behind Clover! One, two, three!", q=True, beat="solution", tag="count the sheep behind Clover", pause=1.2, cam2=(960, 630, 1780),
      hide=["milo"], fx=[("face", 0.02, "clover", "happy"), ("count", "w:One,", 3, CNT3, {"x": 960, "y": 240}), ("hop", "w:One,", "daisy"), ("hop", "w:two,", "woolly"), ("hop", "w:three!", "bramble")],
      words=[("w:Count", "COUNT!", .2, .32, .8, "sun")]),
    S("lane", (980, 640, 1800), "Can you march, like Clover? March, march, march!", q=True, beat="solution", tag="copy me: march", pause=3.0, cam2=(1000, 650, 1760),
      hide=["milo"], fx=[("face", 0.02, "clover", "happy"), *[("walk", "w:March,", w, 60, 5.0) for w in ("clover", "daisy", "woolly", "bramble")]],
      words=[("w:March,", "MARCH, MARCH!", .5, .12, .8, "sun"), ("wait:0.4", "YOUR TURN!", .5, .27, .7, "pill")]),
    # ------------------------------------------------------------ the song moment: Clover SAYS the rhyme, then the tune on instruments
    S("lane", (1400, 725, 1100), "Follow, follow, one by one. Home together, day is done!", who="clover", beat="solution", tag="the follow rhyme", cam2=(1410, 722, 1080),
      hide=["milo", "woolly", "bramble"], fx=[("face", 0.02, "clover", "happy"), ("nod", "w:Follow,", "clover"), ("nod", "w:Home", "clover"), ("hop", "w:done!", "daisy")],
      words=[("w:Follow,", "FOLLOW, FOLLOW", .4, .14, .7, "sun"), ("w:Home", "HOME TOGETHER!", .4, .28, .62, "pill")]),
    S("lane", (960, 580, 1880), who="", sing=SING_HOME, beat="song", tag="song: follow, follow", cam2=(1000, 590, 1800),
      fx=[("face", 0.02, "clover", "happy"), *[("walk", TB(0), w, 120, 9.6) for w in ("clover", "daisy", "woolly", "bramble")],
          ("hop", TB(4), "milo"), ("hop", TB(8), "milo"), ("hop", TB(12), "milo"),
          ("word", TB(0), "FOLLOW, FOLLOW, ONE BY ONE", {"x": 900, "y": 240, "size": 66, "cls": "sun", "hold": 4.4})],
      words=[(TB(8), "HOME TOGETHER!", .48, .16, .7, "pill")]),
    S("lane", (980, 680, 1800), "Who is leading the flock? Clover, or Woolly?", q=True, beat="solution", tag="question: who is leading", pause=3.2, cam2=(1000, 690, 1740),
      hide=["milo"], fx=[("face", 0.02, "clover", "happy"), ("hop", 0.5, "clover"), ("signs", "w:Clover,", ["CLOVER", "WOOLLY"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ WARM ENDING: home, Mama is proud, supper in the barn
    S("farm_gold", WIDE, "Past the fence, and all the way home, to the big red barn. And there is Mama!", trans="iris", beat="ending", tag="home at the red barn",
      cam2=(960, 570, 1800), actors=[WO(-20, 945, .56), CL(300, 940), MA(1240, 935, f=True), MI(700, 480)],
      fx=[("face", 0.02, "clover", "happy"), ("walk", 0.1, "clover", 300, 3.6), ("walk", 0.1, "woolly", 250, 3.6), ("fly", 0.2, "milo", 900, 500, 3.0), ("nod", "w:Mama!", "mama")],
      words=[("w:home,", "HOME!", .4, .15, .85, "sun"), ("w:Mama!", "MAMA!", .7, .3, .75, "pill")]),
    S("farm_gold", MH("farm_gold"), "Clover! You led the flock home! I am so proud of you.", who="mama", beat="ending", tag="Mama: I am so proud",
      hide=["clover", "milo", "woolly"], fx=[("face", 0.02, "mama", "wow"), ("face", "w:proud", "mama", "happy"), ("nod", "w:led", "mama"), ("nod", "w:proud", "mama")],
      words=[("w:proud", "SO PROUD!", .3, .28, .85, "sun")]),
    S("barn", WIDE, "Inside the cosy barn, supper is ready. Sweet, dry grass for everyone!", trans="iris", beat="ending", tag="the barn: supper for everyone",
      cam2=(960, 570, 1800), props=[prop("hy", A.hay, 545, 950, .68)],
      fx=[("face", 0.02, "clover", "happy"), DOWN("w:Sweet,", "woolly", 44), MUNCH("w:Sweet,", "woolly", 8), ("hop", "w:supper", "clover"), ("hop", "w:everyone!", "milo")],
      words=[("w:cosy", "THE COSY BARN", .64, .1, .66, "sun"), ("w:supper", "SUPPER TIME!", .64, .23, .66, "pill")]),
    S("barn", CH("barn"), "Thank you, Milo! You stayed with me the whole time.", who="clover", beat="ending", tag="Clover: thank you, Milo",
      hide=SOLO, fx=[("face", 0.02, "clover", "happy"), ("nod", "w:Milo!", "clover"), ("nod", "w:whole", "clover")],
      words=[("w:Thank", "THANK YOU!", .74, .26, .85, "sun")]),
    S("barn", MB("barn", 820, 0, -40), "You do not have to be big to lead, Clover. You just have to go first.", beat="ending", tag="the lesson: go first",
      hide=["mama", "woolly", "clover"], fx=[("hop", "w:big", "milo"), ("hop", "w:first.", "milo")], words=[("w:first.", "GO FIRST!", .5, .12, .9, "sun")]),
    S("barn", (960, 700, 1700), "Do you remember? What is a group of sheep called? A flock, or a sock?", q=True, beat="ending", tag="question: flock or sock again", pause=3.2,
      cam2=(960, 710, 1660), hide=["milo"], props=[prop("hy", A.hay, 545, 950, .68)],
      fx=[("face", 0.02, "clover", "happy"), ("hop", "w:remember?", "clover"), ("signs", "w:flock,", ["FLOCK", "SOCK"], 0, "wait:1.8")]),
    S("barn", (900, 710, 1560), "And what do sheep eat? Grass, or rocks?", q=True, beat="ending", tag="question: grass or rocks", pause=3.2,
      cam2=(905, 718, 1540), hide=["milo"], props=[prop("hy", A.hay, 545, 950, .68)],
      fx=[DOWN(0.0, "woolly", 44), MUNCH(0.2, "woolly", 18), ("nod", "w:eat?", "clover"), ("signs", "w:Grass,", ["GRASS", "ROCKS"], 0, "wait:1.8")]),
    S("barn", (960, 560, 1840), "Follow, follow, one by one. Home together, day is done!", beat="ending", tag="the closing rhyme", cam2=(960, 590, 1700),
      props=[prop("hy", A.hay, 545, 950, .68)], fx=[("face", 0.02, "clover", "happy"), ("hop", "w:Follow,", "milo"), ("nod", "w:Home", "mama"), ("hop", "w:done!", "clover")],
      words=[("w:Follow,", "FOLLOW, FOLLOW", .6, .13, .6, "sun"), ("w:Home", "HOME TOGETHER!", .6, .25, .58, "pill")]),
    S("barn", (1060, 660, 1400), who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(1060, 650, 1500), hide=["woolly"],
      fx=[("face", 0.02, "clover", "happy"), ("hop", 1.0, "milo"), ("hop", 1.6, "clover"), ("nod", 2.2, "mama")], words=[(TB(3), "HOORAY!", .26, .16, .9, "sun")]),
    S("barn", MB("barn", 820, 0, -40), "Next time: Clover and the Woolly Haircut! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure",
      hide=["mama", "woolly", "clover"], fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .5, .1, .62, "sun"), ("w:See", "SEE YOU SOON!", .5, .22, .5, "pill")]),
    *intro_shots(),      # and again as the last shots: the video ends on the logo with the whole cast
]

# thumbnail (thumb.py): the promise: little Clover in front, the big sheep in a line behind her; 2 words, none of the title's words, no watermark
THUMBS = {
    "za_ep16": {"place": "meadow_gold", "cam": (1095, 600, 1500),
                "actors": [("sheep_woolly", 700, 965, 1.0), ("lamb", 1300, 970, .8, False, "gsap.set('#P-neck',{rotation:-10,svgOrigin:'150 -290'});")],
                "words": [("FOLLOW ME!", 900, 250, 180, "sun", -5)]},
}
