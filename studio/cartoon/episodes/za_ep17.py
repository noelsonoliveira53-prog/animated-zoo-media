"""za_ep17 - Milo's Zoo Adventures: "How Does Hazel Find Snacks at Night?" (theme title "Hazel's Night-Time Snack Hunt"; cartoon adventure, the
3D music-and-sync process: "beat"). Night forest week, adventure 1: the first story with Hazel the hedgehog.
The moon comes up. Hazel wakes up hungry; Milo is sleepy, but he wants to see what a hedgehog does at night, so he comes along on her snack hunt.
Obstacle 1: under the tall trees it is too dark for Milo to see any snacks. Obstacle 2: on the leafy path the leaves go crunch, crunch, and a beetle
scuttles away from the noise. Obstacle 3: the best smell comes from under a big log: Milo tries to lift it (much too heavy) and to peek under it (too
dark). Low moment: "The log is too big. Maybe we can not get the snack." (a little sad, never crying; they sit together). Then Hazel has her own idea:
she does not need to lift it or see it: she follows her nose and snuffles under the log with her little pointed snout, and pulls out a cluster of
blackberries, enough for two. She SAYS the rhyme, the tune is played on instruments, the sun comes up, and Hazel goes to bed in her leaf nest just as
Milo wakes up. Nobody is hurt, lost, crying or trapped; nobody is in danger: the wood is cosy and moonlit, with fireflies.

FACTS, read at the source on Nov 27 2026, about 7:30 PM ET by the session's clock (each page fetched by the session's page reader, which quoted these sentences verbatim):
 [NG] National Geographic, "Hedgehog", nationalgeographic.com/animals/mammals/facts/hedgehog
   "They usually sleep in this position during the day and awaken to search for food at night."
   "While on the hunt, they rely upon their senses of hearing and smell because their eyesight is weak."
   "As a hedgehog picks its way through the hedges it emits piglike grunts"
 [LS] Live Science, "Hedgehog Facts", livescience.com/51221-hedgehog.html
   "They are also nocturnal, which means they sleep during the day."
   "Hedgehogs have poor eyesight and rely on hearing and smell to help them find food."
   "they find meals of fruit, fungi, centipedes, insects, snails, worms, mice" (fragment of a list)
 [WWT] Warwickshire Wildlife Trust, "About hedgehogs", warwickshirewildlifetrust.org.uk/hedgehogs/about-hedgehogs
   "Hedgehogs eat predominantly beetles, caterpillars and earthworms."
 [EB] Encyclopaedia Britannica, "Hedgehog (subfamily Erinaceinae)", britannica.com/animal/hedgehog-mammal
   "Hedgehogs are primarily nocturnal ..."   "Although the eyes are large, vision is poor."   "They snuffle and snort while foraging" (fragment)
 Said as facts in the film (three fact boards, questions, recap): hedgehogs sleep in the day and look for food at night [NG, LS, EB]; hedgehogs can not
 see very well, they use their nose (and ears) to find food [NG, LS, EB]; hedgehogs eat beetles, caterpillars and worms [WWT]. Hazel snuffling and
 grunting while she hunts follows [EB, NG]; the berries she finds are fruit [LS].
 NOT said as facts: that hedgehogs look under logs (no page read today says so: the log is THIS story), anything about spines, rolling into a ball,
 hibernation, milk or pets. Nobody eats a beetle on screen: the beetle scuttles away, the snack shown is blackberries.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep07 as A7
import art_za_ep13 as A13
import art_zc_ep12 as A12
import art_za_ep17 as A
import kit
from kit import Kit, S, prop
from intro import INTRO_STAGES, intro_shots, SUBSCRIBE_LINE      # the main intro, right after the hook and as the last shots (owner, Nov 20 4:50 PM)

EP = {"id": "za_ep17", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "hazel": {"voice": "af_sky", "speed": .88, "pitch": 4, "formant": 1.2, "gain": .95}},
      "title": "How Does Hazel Find Snacks at Night?", "thumb_text": "SNIFF, SNIFF!",
      "series": "Milo's Zoo Adventures",
      "description": ("How does Hazel find snacks at night? The moon is up, and Hazel the hedgehog is awake and hungry! Sleepy Milo comes along on her "
                      "night-time snack hunt. It is too dark to see, the leaves go crunch, crunch, and the best snack is under a big log... Then Hazel "
                      "has her very own idea. A gentle night forest adventure for ages 2-6 about using what you are good at, with questions to answer, "
                      "a count-along, moves to copy and a little tune.\n"
                      "Kids see that hedgehogs sleep in the day and look for food at night, that hedgehogs can not see very well and use their nose to find "
                      "food, and that hedgehogs eat beetles, caterpillars and worms.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNational Geographic (Hedgehog); Live Science (Hedgehog Facts); Warwickshire Wildlife Trust (About hedgehogs); "
                      "Encyclopaedia Britannica (Hedgehog)."),
      "tags": ["hedgehog for kids", "hedgehog cartoon", "night animals for kids", "nocturnal animals for kids", "forest animals for kids", "animal stories for kids",
               "bedtime story for kids", "friendship story for kids", "kids adventure cartoon", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

HZ = lambda x, y, s=.72, f=False: ("hazel", "hedgehog", x, y, s, f)
MI = lambda x, y, s=.6: ("milo", "milo", x, y, s, False, True)
# boxes (rig units): hedgehog -250..310 wide, 285 tall; at .72 Hazel reaches 180 left and 223 right of her feet, 205 up
LOG = (1240, 965, .9)                     # the big log in the clearing (a prop, in front of the actors): 1240 +- 390 wide, top at about 650
STAGES = {
    "dusk_wood": [HZ(620, 940), MI(1120, 600)],
    "darkwood": [HZ(760, 945), MI(1080, 640)],
    "leafwood": [HZ(560, 950), MI(1000, 640)],
    "logglade": [HZ(420, 945), MI(250, 560)],
    "nightforest": [HZ(520, 945), MI(980, 620)],
    "dawn_wood": [HZ(620, 940), MI(1120, 560)],
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
CH = lambda place, w=760, dx=120, dy=0, stage=None: C(place, "hazel", "head", w, dx, dy, stage=stage)        # Hazel's face on the left, room for words on the right
MB = lambda place, w=820, dx=0, dy=-40, stage=None: C(place, "milo", "body", w, dx, dy, stage=stage)           # Milo: low in the frame, under the signs

# ---- Hazel sniffs: her snout goes down to the ground, the smell lines wave up to her nose
DOWN = lambda at, deg=16: ("lookat", at, "hazel", deg)
UP = lambda at: ("lookat", at, "hazel", 0)
WAVE = lambda at, pid="sn", n=10: ("to", at, "#{p}%s-l2" % pid, {"y": -24, "duration": .3, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "the smell lines wave")
SNIFFS = lambda at, n=6: ("to", at, "#{p}hazel-neck", {"y": -8, "duration": .16, "yoyo": True, "repeat": 2 * n - 1, "ease": "sine.inOut"}, "Hazel sniffs")
SN = lambda x, y, s=.8, hidden=True: prop("sn", A.sniff, x, y, s, hidden)
SCURRY = lambda at, dx, d: ("walk", at, "hazel", dx, d)
YAWN = lambda at: ("to", at, "#{p}milo", {"scaleY": 1.06, "transformOrigin": "50% 100%", "duration": .5, "yoyo": True, "repeat": 1, "ease": "sine.inOut"}, "Milo yawns")
GLOW = lambda at, pid, n=7: ("to", at, "#{p}%s_w" % pid, {"scale": 1.12, "transformOrigin": "50% 100%", "duration": .3, "yoyo": True, "repeat": n}, "%s pulses" % pid)

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. The rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_SNIFF = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~ ~", "notes": "G4:1 E4:1 G4:1 C5:1 B4:1 D5:1 G4:1", "rest": 1},     # sniff and snuffle, through the night (C bar, G bar)
                                  {"text": "~ ~ ~ ~ ~ ~ ~", "notes": "A4:1 F4:1 A4:1 C5:1 G4:1 E4:1 C5:1", "rest": 1}])    # my little nose can find a bite (F bar, C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "D5:1 B4:1 G4:1 B4:1 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune
CNT3 = 0.53                                      # seconds from "One" to "three" (checked against the timing file)

# the board pictures
DAYCARD = lambda x, y, s=1.0: prop("dc", lambda p: A.skycard(p, False), x, y, s)
NIGHTCARD = lambda x, y, s=1.0: prop("nc", lambda p: A.skycard(p, True), x, y, s)
FOODS = lambda y=700, s=1.5: [prop("f1", A12.beetle, 520, y, s * 1.6), prop("f2", A.caterpillar, 960, y + 20, s), prop("f3", A.worm, 1420, y + 20, s)]
CLEAR = [HZ(420, 945), MI(250, 560)]
BYLOG = [HZ(660, 948), MI(420, 640)]

SHOTS = [
    # ------------------------------------------------------------ HOOK: the promise (first 5 seconds): the moonlit wood, Hazel's nose sniffing the ground
    S("nightforest", (760, 700, 1300), "How does Hazel find snacks at night? Look! It is very dark. But Hazel's nose goes sniff, sniff!", beat="hook",
      tag="hook: Hazel sniffs in the moonlit wood", cam2=(780, 710, 1220), hide=["milo"], props=[SN(890, 950, .8, False)],
      fx=[DOWN(0.02), SNIFFS(0.1, 4), WAVE(0.1), ("face", 0.02, "hazel", "happy"), SCURRY("w:Look!", 60, .9), ("face", "w:nose", "hazel", "wow"), SNIFFS("w:sniff,", 6)],
      words=[("w:snacks", "SNACKS AT NIGHT?", .56, .16, .7, "sun"), ("w:sniff,", "SNIFF, SNIFF!", .7, .34, .75, "pill")]),
    *intro_shots(),      # the main intro, right after the hook
    # ------------------------------------------------------------ GOAL: the moon is up; Hazel wakes up hungry, sleepy Milo comes along
    S("dusk_wood", WIDE, "Hello, I'm Milo! The moon is coming up. And I am visiting Hazel the hedgehog.", trans="iris", beat="goal", tag="dusk: Milo and Hazel by her nest",
      cam2=(960, 570, 1800), actors=[HZ(330, 948, .5), MI(1120, 600)],
      fx=[("hop", "w:Hello,", "milo"), ("face", 0.02, "hazel", "sleepy"), SCURRY("w:Hazel", 280, 1.6), ("face", "w:hedgehog.", "hazel", "happy")],
      words=[("w:moon", "THE MOON!", .62, .14, .7, "sun"), ("w:Hazel", "HAZEL", .34, .6, .62, "pill")]),
    S("dusk_wood", CH("dusk_wood"), "Good evening, Milo! I just woke up. And I am hungry! Time for my night-time snack hunt!", who="hazel", beat="goal",
      tag="Hazel: time for my snack hunt", hide=["milo"], fx=[("face", 0.02, "hazel", "sleepy"), ("face", "w:woke", "hazel", "happy"), ("nod", "w:hungry!", "hazel"), ("hop", "w:snack", "hazel")],
      words=[("w:hungry!", "HUNGRY!", .74, .22, .85, "pill"), ("w:snack", "SNACK HUNT!", .74, .4, .75, "sun")]),
    S("dusk_wood", MB("dusk_wood"), "But Milo is sleepy. Birds like me sleep at night! Can I come too, Hazel?", beat="goal", tag="Milo: sleepy, can I come too",
      hide=["hazel"], props=[prop("se", A7.shut_eyes, 1120, 600, .6, True)],
      fx=[("face", 0.02, "milo", "sleepy"), YAWN("w:sleepy."), ("show", "w:sleepy.", "se", 1.2), ("face", "w:come", "milo", "happy"), ("hop", "w:come", "milo")],
      words=[("w:sleepy.", "SLEEPY MILO", .5, .12, .7, "pill"), ("w:come", "ME TOO?", .74, .32, .8, "sun")]),
    S("dusk_wood", (800, 700, 1240), "Yes! Come and see what a hedgehog does at night!", who="hazel", beat="goal", tag="Hazel: yes, come and see",
      cam2=(810, 710, 1180), actors=[HZ(620, 940), MI(1000, 800)], fx=[("face", 0.02, "hazel", "happy"), ("hop", "w:Yes!", "hazel"), ("hop", "w:see", "milo")],
      words=[("w:Yes!", "YES!", .5, .14, .9, "sun")]),
    S("dusk_wood", (700, 640, 1560), "When does Hazel look for her snacks? In the day, or at night?", q=True, beat="goal", tag="question: day or night", pause=3.2,
      cam2=(780, 700, 1320), actors=[HZ(620, 940), MI(1000, 800)], fx=[("face", 0.02, "hazel", "happy"), SNIFFS(0.4, 3), ("signs", "w:day,", ["DAY", "NIGHT"], 1, "wait:1.8")]),
    S("paper", (960, 520, 1560), "Hedgehogs sleep in the day. At night, they wake up, and look for food.", beat="fact", tag="fact: hedgehogs sleep in the day, hunt at night",
      cam2=(960, 530, 1480), actors=[("hz1", "hedgehog", 600, 800, .62, False), ("hz2", "hedgehog", 1320, 800, .62, False)],
      props=[DAYCARD(560, 430, .9), NIGHTCARD(1340, 430, .9), prop("lid", A.hog_lids, 600, 800, .62), prop("zz", A.zzz, 760, 590, .7)],
      fx=[GLOW("w:day.", "dc", 3), ("to", "w:day.", "#{p}zz", {"y": -30, "duration": .5, "yoyo": True, "repeat": 5}, "the z's float"), GLOW("w:night,", "nc", 3),
          ("hop", "w:wake", "hz2"), ("to", "w:look", "#{p}hz2-neck", {"rotation": 16, "svgOrigin": "90 -110", "duration": .4, "yoyo": True, "repeat": 3}, "the hedgehog sniffs")],
      words=[("w:sleep", "SLEEP IN THE DAY", .3, .14, .5, "pill"), ("w:night,", "AWAKE AT NIGHT!", .7, .14, .5, "sun")]),
    S("paper", (960, 560, 1560), "When do hedgehogs look for food? At night, or in the day?", q=True, beat="fact", tag="question: night or day", pause=3.2, cam2=(960, 570, 1500),
      actors=[("hz2", "hedgehog", 960, 850, .7, False)], props=[NIGHTCARD(960, 520, 1.0)],
      fx=[GLOW(0.3, "nc", 9), ("signs", "w:night,", ["NIGHT", "DAY"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 1: under the tall trees it is too dark for Milo's eyes
    S("darkwood", WIDE, "Off they go, deep into the wood, under the tall, tall trees.", trans="iris", beat="obstacle1", tag="the dark wood under tall trees",
      cam2=(990, 560, 1800), actors=[HZ(260, 945), MI(80, 560)], fx=[SCURRY(0.1, 500, 3.2), ("fly", 0.2, "milo", 1080, 640, 3.0), ("face", 0.02, "hazel", "happy")],
      words=[("w:wood,", "THE DEEP WOOD", .62, .12, .66, "sun"), ("w:tall,", "TALL TREES!", .62, .27, .7, "pill")]),
    S("darkwood", MB("darkwood"), "Where are the snacks? I can not see a thing! It is too dark for my eyes.", beat="obstacle1", tag="Milo: I can not see a thing",
      hide=["hazel"], fx=[("face", 0.02, "milo", "wow"), ("to", "w:Where", "#{p}milo", {"x": "-=30", "duration": .5, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "Milo looks left and right"),
                          ("face", "w:dark", "milo", "sad")],
      words=[("w:see", "WHERE?", .74, .2, .9, "sun"), ("w:dark", "TOO DARK!", .26, .34, .8, "pill")]),
    S("darkwood", (920, 720, 1300), actors=[HZ(700, 945), MI(1150, 870)], say="Can you look around, like Milo? Look this way. Look that way!", q=True, beat="obstacle1", tag="copy me: look around", pause=3.0, cam2=(920, 730, 1220),
      fx=[("face", 0.02, "milo", "wow"), ("to", "w:this", "#{p}milo", {"x": "-=60", "duration": .6, "ease": "sine.inOut"}, "Milo looks this way"),
          ("to", "w:that", "#{p}milo", {"x": "+=120", "duration": .8, "ease": "sine.inOut"}, "Milo looks that way"),
          ("to", "wait:0.6", "#{p}milo", {"x": "-=120", "duration": .8, "yoyo": True, "repeat": 1, "ease": "sine.inOut"}, "Milo looks again"), SNIFFS(0.3, 4)],
      words=[("w:this", "THIS WAY!", .3, .14, .7, "sun"), ("w:that", "THAT WAY!", .7, .14, .7, "pill"), ("wait:0.4", "YOUR TURN!", .5, .3, .7, "sun")]),
    S("darkwood", (920, 700, 1360), actors=[HZ(700, 945), MI(1150, 870)], say="Can Milo see any snacks in the dark? Yes, or no?", q=True, beat="obstacle1", tag="question: can Milo see", pause=3.2, cam2=(930, 710, 1300),
      fx=[("face", 0.02, "milo", "sad"), ("hop", 0.4, "milo"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    S("darkwood", CH("darkwood"), "That's okay, Milo! I do not need my eyes. I have my nose! Sniff, sniff!", who="hazel", beat="obstacle1", tag="Hazel: I have my nose",
      hide=["milo"], props=[SN(1070, 955, .7)], fx=[("face", 0.02, "hazel", "happy"), ("nod", "w:okay,", "hazel"), ("face", "w:nose!", "hazel", "wow"), DOWN("w:Sniff,"), ("show", "w:Sniff,", "sn"), WAVE("w:Sniff,"), SNIFFS("w:Sniff,", 5)],
      words=[("w:nose!", "MY NOSE!", .74, .2, .85, "sun")]),
    S("paper_blue", (960, 520, 1560), "Hedgehogs can not see very well. They use their nose, and their ears, to find food.", beat="fact", tag="fact: hedgehogs use their nose to find food",
      cam2=(960, 530, 1480), actors=[("hz2", "hedgehog", 600, 770, 1.0, False)], props=[prop("sn2", A.sniff, 1000, 790, 1.0), prop("f3", A.worm, 1360, 770, 1.2)],
      fx=[("to", "w:nose,", "#{p}hz2-neck", {"rotation": 14, "svgOrigin": "90 -110", "duration": .3, "yoyo": True, "repeat": 5}, "the hedgehog sniffs"), WAVE("w:nose,", "sn2", 12),
          ("to", "w:ears,", "#{p}hz2-ear", {"scale": 1.25, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 3}, "the ear pulses"), GLOW("w:food.", "f3", 3)],
      words=[("w:nose,", "NOSE!", .6, .14, .95, "sun"), ("w:ears,", "AND EARS", .36, .3, .6, "pill")]),
    S("paper_blue", (960, 560, 1560), "What helps Hazel find her food? Her nose, or her tail?", q=True, beat="fact", tag="question: nose or tail", pause=3.2, cam2=(960, 570, 1500),
      actors=[("hz2", "hedgehog", 800, 880, .9, False)], props=[prop("sn2", A.sniff, 1170, 890, .9)],
      fx=[("to", 0.3, "#{p}hz2-neck", {"rotation": 14, "svgOrigin": "90 -110", "duration": .3, "yoyo": True, "repeat": 17}, "the hedgehog sniffs"), WAVE(0.2, "sn2", 22),
          ("signs", "w:nose,", ["NOSE", "TAIL"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 2: the leafy path: crunch, crunch! the beetle scuttles away
    S("leafwood", WIDE, "Hazel's nose leads the way, to a path full of leaves. And Hazel smells a beetle!", trans="iris", beat="obstacle2", tag="the leafy path: a beetle",
      cam2=(990, 560, 1800), actors=[HZ(200, 950), MI(80, 600)], props=[prop("bt", A12.beetle, 1450, 930, 1.4), SN(1300, 930, .8)],
      fx=[SCURRY(0.1, 450, 3.0), ("fly", 0.2, "milo", 760, 620, 3.0), DOWN("w:smells"), ("show", "w:smells", "sn"), WAVE("w:smells"), SNIFFS("w:smells", 5),
          ("to", 0.5, "#{p}bt_w", {"x": "+=20", "duration": .3, "yoyo": True, "repeat": 9}, "the beetle wiggles")],
      words=[("w:leaves.", "LEAVES!", .3, .14, .8, "sun"), ("w:beetle!", "A BEETLE!", .66, .3, .75, "pill")]),
    S("leafwood", (900, 720, 1300), "Milo hops closer. But the dry leaves go crunch! Crunch, crunch!", beat="obstacle2", tag="Milo hops: crunch, crunch",
      cam2=(910, 730, 1240), actors=[HZ(560, 950), MI(820, 880)], props=[prop("cr", A.crunch, 900, 950, .9, True), prop("cr2", A.crunch, 1020, 950, .7, True)],
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:hops", "milo"), ("walk", "w:hops", "milo", 80, .8), ("show", "w:crunch!", "cr", 1.6), ("hop", "w:Crunch,", "milo"),
          ("show", "w:Crunch,", "cr2", 1.4), ("face", "w:crunch!", "hazel", "wow"), ("show", "e:crunch!:2", "cr", .8)],
      words=[("w:crunch!", "CRUNCH!", .7, .16, .95, "sun"), ("w:Crunch,", "CRUNCH, CRUNCH!", .4, .34, .7, "pill")]),
    S("leafwood", (1150, 760, 1300), "The beetle hears the noise. And it scuttles away, under the leaves.", beat="obstacle2", tag="the beetle scuttles away",
      cam2=(1160, 770, 1240), actors=[HZ(800, 950), MI(1150, 880)], props=[prop("bt", A12.beetle, 1430, 960, 1.4), prop("lp", A.leafpile, 1720, 990, .9)],
      fx=[("face", 0.02, "hazel", "wow"), ("to", "w:hears", "#{p}bt_w", {"y": -20, "duration": .15, "yoyo": True, "repeat": 3}, "the beetle jumps"),
          ("to", "w:scuttles", "#{p}bt_w", {"x": "+=330", "duration": 1.4, "ease": "power1.in"}, "the beetle scuttles into the leaves"), ("face", "w:under", "milo", "sad")],
      words=[("w:scuttles", "BYE, BEETLE!", .4, .14, .75, "sun")]),
    S("leafwood", (760, 720, 1300), "Can you tiptoe, like Milo? Tip, tip, tiptoe!", q=True, beat="obstacle2", tag="copy me: tiptoe", pause=3.0, cam2=(770, 730, 1240),
      actors=[HZ(480, 950), MI(900, 880)],
      fx=[("face", 0.02, "milo", "happy"), *[("to", f"w:{w}", "#{p}milo", {"y": "-=24", "duration": .14, "yoyo": True, "repeat": 1}, "Milo tiptoes") for w in ("Tip,", "tip,", "tiptoe!")],
          ("to", "wait:0.3", "#{p}milo", {"y": "-=24", "duration": .14, "yoyo": True, "repeat": 9, "repeatDelay": .14}, "Milo tiptoes on"), ("walk", "w:tiptoe", "milo", 70, 2.0)],
      words=[("w:Tip,", "TIP, TIP!", .5, .14, .85, "sun"), ("wait:0.4", "YOUR TURN!", .5, .3, .7, "pill")]),
    S("leafwood", (760, 700, 1360), "Are the dry leaves quiet, or crunchy?", q=True, beat="obstacle2", tag="question: quiet or crunchy", pause=3.2, cam2=(770, 710, 1300),
      actors=[HZ(480, 950), MI(900, 880)], props=[prop("cr", A.crunch, 1250, 960, .8)],
      fx=[("to", 0.2, "#{p}cr-b", {"scale": 1.2, "transformOrigin": "50% 50%", "duration": .3, "yoyo": True, "repeat": 13}, "the crunch marks pulse"), ("signs", "w:quiet,", ["QUIET", "CRUNCHY"], 1, "wait:1.8")]),
    S("leafwood", CH("leafwood", stage=[HZ(480, 950)]), "Never mind the beetle. My nose can smell something even better!", who="hazel", beat="obstacle2", tag="Hazel: something even better",
      actors=[HZ(480, 950)], props=[SN(830, 965, .7)], fx=[("face", 0.02, "hazel", "happy"), DOWN("w:nose"), ("show", "w:nose", "sn"), WAVE("w:nose"), SNIFFS("w:smell", 5), ("face", "w:better!", "hazel", "wow")],
      words=[("w:better!", "EVEN BETTER!", .74, .22, .75, "sun")]),
    S("paper_pink", (960, 520, 1560), "Hedgehogs eat beetles, caterpillars, and worms. Those are hedgehog snacks!", beat="fact", tag="fact: hedgehogs eat beetles, caterpillars and worms",
      cam2=(960, 530, 1480), props=FOODS(), fx=[GLOW("w:beetles,", "f1", 3), GLOW("w:caterpillars,", "f2", 3), GLOW("w:worms.", "f3", 3)],
      words=[("w:beetles,", "BEETLES", .27, .3, .55, "pill"), ("w:caterpillars,", "CATERPILLARS", .5, .2, .55, "sun"), ("w:worms.", "WORMS", .74, .3, .55, "pill")]),
    S("paper_pink", (960, 560, 1560), "Count the hedgehog snacks with Milo! One, two, three!", q=True, beat="fact", tag="count three snacks", pause=1.2, cam2=(960, 570, 1500),
      props=FOODS(740), fx=[("count", "w:One,", 3, CNT3, {"x": 960, "y": 300}), GLOW("w:One,", "f1", 1), GLOW("w:two,", "f2", 1), GLOW("w:three!", "f3", 1)],
      words=[("w:Count", "COUNT!", .2, .36, .8, "sun")]),
    S("paper_pink", (960, 560, 1560), "What do hedgehogs eat? Beetles, or pizza?", q=True, beat="fact", tag="question: beetles or pizza", pause=3.2, cam2=(960, 570, 1500),
      props=[prop("f1", A12.beetle, 960, 760, 2.4)], fx=[("to", 0.3, "#{p}f1_w", {"x": "+=30", "duration": .3, "yoyo": True, "repeat": 17}, "the beetle wiggles"),
                                                          ("signs", "w:Beetles,", ["BEETLES", "PIZZA"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 3: the best smell is under the big log
    S("logglade", WIDE, "Sniff, sniff! Hazel follows the smell, to a clearing. The best smell of all comes from under a big log.", trans="iris", beat="obstacle3",
      tag="the clearing: the big log", cam2=(990, 560, 1800), actors=[HZ(120, 945), MI(60, 560)], props=[prop("log", A.biglog, *LOG), SN(830, 960, .8)],
      fx=[SCURRY(0.1, 380, 2.6), ("fly", 0.2, "milo", 380, 600, 2.8), ("show", "w:best", "sn"), WAVE("w:best"), DOWN("w:best"), SNIFFS("w:log.", 4)],
      words=[("w:log.", "UNDER THE LOG!", .62, .14, .7, "sun")]),
    S("logglade", CH("logglade", stage=BYLOG), "It smells so yummy! But it is under the log.", who="hazel", beat="obstacle3", tag="Hazel: it smells yummy, under the log",
      actors=BYLOG, props=[prop("log", A.biglog, *LOG)], hide=["milo"], fx=[("face", 0.02, "hazel", "wow"), SNIFFS(0.1, 5), ("nod", "w:yummy!", "hazel"), ("face", "w:under", "hazel", "sad")],
      words=[("w:yummy!", "YUMMY!", .74, .2, .9, "sun")]),
    S("logglade", (1050, 640, 1600), "I will lift it! Push, push, push! But the log is much too big, and much too heavy.", beat="obstacle3", tag="Milo tries to lift the log",
      cam2=(1040, 645, 1560), actors=[HZ(500, 948), MI(800, 880)], props=[prop("log", A.biglog, *LOG)],
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:lift", "milo"), ("to", "w:Push,", "#{p}milo", {"x": "+=16", "duration": .2, "yoyo": True, "repeat": 11}, "Milo pushes"),
          ("to", "w:Push,", "#{p}log_w", {"rotation": .6, "transformOrigin": "50% 100%", "duration": .2, "yoyo": True, "repeat": 3}, "the log does not move"), ("face", "w:heavy.", "milo", "sad")],
      words=[("w:Push,", "PUSH, PUSH!", .4, .14, .8, "sun"), ("w:heavy.", "TOO HEAVY!", .7, .3, .7, "pill")]),
    S("logglade", (900, 720, 1300), "Can you push, like Milo? Push, push, push!", q=True, beat="obstacle3", tag="copy me: push", pause=3.0, cam2=(900, 725, 1260),
      actors=[HZ(500, 948), MI(800, 880)], props=[prop("log", A.biglog, *LOG)],
      fx=[("face", 0.02, "milo", "wow"), ("to", "w:Push,", "#{p}milo", {"x": "+=16", "duration": .2, "yoyo": True, "repeat": 23}, "Milo pushes"), ("hop", "wait:1.0", "hazel")],
      words=[("w:Push,", "PUSH, PUSH!", .5, .12, .8, "sun"), ("wait:0.4", "YOUR TURN!", .5, .27, .7, "pill")]),
    S("logglade", (920, 740, 1340), "Then Milo peeks under the log. But it is too dark under there.", beat="obstacle3", tag="Milo peeks under the log: too dark",
      cam2=(930, 745, 1300), actors=[HZ(500, 948), MI(800, 880)], props=[prop("log", A.biglog, *LOG)],
      fx=[("face", 0.02, "milo", "wow"), ("to", "w:peeks", "#{p}milo", {"rotation": 22, "transformOrigin": "50% 100%", "duration": .5, "ease": "power2.out"}, "Milo leans to peek"),
          ("to", "w:dark", "#{p}milo", {"rotation": 0, "duration": .5}, "Milo stands up"), ("face", "w:dark", "milo", "sad")],
      words=[("w:peeks", "PEEK!", .3, .14, .85, "sun"), ("w:dark", "TOO DARK!", .64, .3, .75, "pill")]),
    S("logglade", (900, 700, 1360), "Can Milo lift the big log? Yes, or no?", q=True, beat="obstacle3", tag="question: can Milo lift the log", pause=3.2, cam2=(910, 710, 1300),
      actors=[HZ(500, 948), MI(800, 880)], props=[prop("log", A.biglog, *LOG)], fx=[("face", 0.02, "milo", "sad"), ("hop", 0.4, "milo"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ LOW MOMENT: the log is too big (gentle: nobody cries, they sit together)
    S("logglade", (760, 720, 1300), "Milo sits down next to Hazel. The moon shines. The log is still there.", beat="low", tag="they sit together by the log",
      cam2=(780, 730, 1240), actors=[HZ(520, 948), MI(820, 900)], props=[prop("log", A.biglog, *LOG)],
      fx=[("face", 0.02, "milo", "sad"), ("face", 0.02, "hazel", "sad"), ("walk", "w:sits", "milo", -60, .8), ("lookat", "w:moon", "hazel", -8)],
      words=[("w:moon", "THE MOON SHINES", .62, .14, .62, "sun")]),
    S("logglade", MB("logglade", 760, 0, -40, stage=[MI(820, 900)]), "The log is too big, and it is too dark. Maybe we can not get the snack.", beat="low", tag="Milo: maybe we can not get the snack",
      actors=[MI(820, 900)], fx=[("face", 0.02, "milo", "sad"), ("to", "w:Maybe", "#{p}milo", {"scaleY": .95, "transformOrigin": "50% 100%", "duration": .6}, "Milo droops")],
      words=[("w:big,", "TOO BIG", .26, .2, .8, "pill"), ("w:snack.", "NO SNACK?", .74, .3, .8, "sun")]),
    S("logglade", (720, 740, 1200), "How do Milo and Hazel feel now? Sad, or happy?", q=True, beat="low", tag="question: sad or happy", pause=3.2, cam2=(730, 750, 1140),
      actors=[HZ(520, 948), MI(820, 900)], fx=[("face", 0.02, "milo", "sad"), ("face", 0.02, "hazel", "sad"), ("lookat", 0.4, "hazel", 8), ("signs", "w:Sad,", ["SAD", "HAPPY"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: Hazel's own idea: no lifting, no seeing: her nose and her little snout
    S("logglade", CH("logglade", stage=CLEAR), "Wait! I do not need to lift it. I do not need to see. I can follow my nose, and snuffle under!", who="hazel", beat="solution",
      tag="Hazel's idea: follow my nose, snuffle under", actors=CLEAR, hide=["milo"], props=[prop("bulb", A13.think_bulb, 590, 705, .4, True)],
      fx=[("face", 0.02, "hazel", "sad"), ("face", "w:Wait!", "hazel", "wow"), ("show", "w:Wait!", "bulb"), ("face", "w:follow", "hazel", "happy"), ("nod", "w:nose,", "hazel"), ("hop", "w:snuffle", "hazel")],
      words=[("w:nose,", "MY NOSE!", .74, .2, .8, "sun"), ("w:snuffle", "SNUFFLE UNDER!", .74, .38, .66, "pill")]),
    S("logglade", (1050, 720, 1400), "So Hazel puts her little nose down, and snuffles in, under the log. Snuffle, snuffle! Grunt, grunt!", beat="solution",
      tag="Hazel snuffles under the log", cam2=(1060, 730, 1340), actors=[HZ(600, 948), MI(1560, 625)], props=[prop("log", A.biglog, *LOG), SN(840, 965, .7)],
      fx=[("face", 0.02, "hazel", "happy"), DOWN("w:nose"), ("show", "w:nose", "sn", 1.6), WAVE("w:nose"), SCURRY("w:snuffles", 250, 1.6), SNIFFS("w:Snuffle,", 8),
          ("to", "w:Grunt,", "#{p}hazel", {"x": "+=10", "duration": .12, "yoyo": True, "repeat": 7}, "Hazel wriggles"), ("face", "w:Grunt,", "milo", "wow")],
      words=[("w:Snuffle,", "SNUFFLE!", .3, .3, .8, "sun"), ("w:Grunt,", "GRUNT, GRUNT!", .55, .14, .7, "pill")]),
    S("logglade", (1000, 720, 1440), "Out comes Hazel, with a big bunch of juicy blackberries! Enough for two!", beat="solution", tag="Hazel comes out with blackberries",
      cam2=(1010, 730, 1400), actors=[HZ(850, 948), MI(1560, 625)], props=[prop("log", A.biglog, *LOG), prop("bb", A.berries, 905, 960, .8, True)],
      fx=[("face", 0.02, "hazel", "happy"), DOWN(0.0, 10), SCURRY("w:Out", -250, 1.2), UP("e:Hazel,"), ("show", "w:blackberries!", "bb"), ("face", "w:blackberries!", "milo", "wow"),
          ("hop", "w:Enough", "milo"), ("hop", "w:two!", "hazel")],
      words=[("w:blackberries!", "BLACKBERRIES!", .44, .14, .7, "sun"), ("w:two!", "FOR TWO!", .64, .3, .75, "pill")]),
    S("logglade", (720, 740, 1200), "Who found the snack? Hazel, or Milo?", q=True, beat="solution", tag="question: who found the snack", pause=3.2, cam2=(730, 750, 1140),
      actors=[HZ(520, 948), MI(1040, 880)], props=[prop("bb", A.berries, 820, 960, .8)],
      fx=[("face", 0.02, "hazel", "happy"), ("hop", 0.4, "hazel"), GLOW(0.6, "bb", 9), ("signs", "w:Hazel,", ["HAZEL", "MILO"], 0, "wait:1.8")]),
    S("logglade", MB("logglade", 760, 0, -40, stage=[MI(900, 880)]), "Hazel, you did it! You found the snack with your nose!", beat="solution", tag="Milo: you did it",
      actors=[MI(900, 880)], fx=[("face", 0.02, "milo", "wow"), ("hop", "w:did", "milo"), ("face", "w:nose!", "milo", "happy"), ("hop", "w:nose!", "milo")],
      words=[("w:did", "YOU DID IT!", .74, .2, .8, "sun")]),
    S("logglade", (720, 720, 1300), "Can you sniff, like Hazel? Sniff, sniff, sniff!", q=True, beat="solution", tag="copy me: sniff", pause=3.0, cam2=(730, 730, 1240),
      actors=[HZ(520, 948), MI(1060, 880)], props=[prop("bb", A.berries, 900, 960, .8), SN(775, 900, .6, False)],
      fx=[("face", 0.02, "hazel", "happy"), DOWN(0.0, 10), SNIFFS("w:Sniff,", 14), WAVE("w:Sniff,", "sn", 16), ("hop", "wait:1.2", "milo")],
      words=[("w:Sniff,", "SNIFF, SNIFF!", .5, .12, .8, "sun"), ("wait:0.4", "YOUR TURN!", .5, .27, .7, "pill")]),
    # ------------------------------------------------------------ the song moment: Hazel SAYS the rhyme, then the tune on instruments
    S("logglade", (720, 760, 1100), "Sniff and snuffle, through the night. My little nose can find a bite!", who="hazel", beat="solution", tag="the sniff rhyme", cam2=(730, 762, 1060),
      actors=[HZ(520, 948), MI(1020, 760)], hide=["milo"], props=[prop("bb", A.berries, 850, 960, .8)],
      fx=[("face", 0.02, "hazel", "happy"), ("nod", "w:Sniff", "hazel"), SNIFFS("w:snuffle,", 3), ("nod", "w:My", "hazel"), ("hop", "w:bite!", "hazel")],
      words=[("w:Sniff", "SNIFF AND SNUFFLE", .5, .14, .62, "sun"), ("w:My", "MY LITTLE NOSE!", .5, .28, .62, "pill")]),
    S("logglade", (960, 600, 1840), who="", sing=SING_SNIFF, beat="song", tag="song: sniff and snuffle", cam2=(980, 610, 1760),
      actors=[HZ(380, 948), MI(720, 760)], props=[prop("log", A.biglog, *LOG), prop("bb", A.berries, 660, 960, .8)],
      fx=[("face", 0.02, "hazel", "happy"), ("face", 0.02, "milo", "happy"), ("hop", TB(0), "hazel"), ("hop", TB(4), "milo"), ("hop", TB(8), "hazel"), ("hop", TB(12), "milo"),
          SNIFFS(TB(2), 3), SNIFFS(TB(10), 3),
          ("word", TB(0), "SNIFF AND SNUFFLE!", {"x": 900, "y": 240, "size": 70, "cls": "sun", "hold": 4.4})],
      words=[(TB(8), "THROUGH THE NIGHT!", .5, .16, .66, "pill")]),
    # ------------------------------------------------------------ WARM ENDING: the sun comes up: Hazel's bedtime, Milo's wake-up time
    S("dawn_wood", WIDE, "Munch, munch, yum! Then, the sky turns pink. The sun is coming up!", trans="iris", beat="ending", tag="dawn at Hazel's nest",
      cam2=(960, 570, 1800), actors=[HZ(700, 940), MI(1120, 600)], props=[prop("bb", A.berries, 900, 950, .6)],
      fx=[("face", 0.02, "hazel", "happy"), ("nod", "w:Munch,", "hazel"), ("hop", "w:yum!", "milo"), ("face", "w:pink.", "hazel", "sleepy"), ("fly", "w:sun", "milo", 1220, 520, 1.6)],
      words=[("w:pink.", "A PINK SKY", .44, .14, .7, "pill"), ("w:sun", "GOOD MORNING!", .4, .3, .66, "sun")]),
    S("dawn_wood", CH("dawn_wood"), "Now it is my bedtime. Hedgehogs sleep in the day! Good night, Milo.", who="hazel", beat="ending", tag="Hazel: now it is my bedtime",
      hide=["milo"], fx=[("face", 0.02, "hazel", "sleepy"), ("nod", "w:bedtime.", "hazel"), ("nod", "w:night,", "hazel")],
      words=[("w:bedtime.", "BEDTIME!", .74, .2, .85, "pill")]),
    S("dawn_wood", (560, 760, 1200), "Hazel curls up, in her cosy leaf nest. And Milo is wide awake!", beat="ending", tag="Hazel in her leaf nest, Milo awake",
      cam2=(570, 770, 1140), actors=[HZ(560, 940, .62), MI(860, 760)], props=[prop("lid", A.hog_lids, 380, 940, .62, True), prop("zz", A.zzz, 540, 760, .6, True)],
      fx=[("face", 0.02, "hazel", "sleepy"), SCURRY("w:curls", -180, 1.0), ("show", "e:nest.", "lid"), ("show", "e:nest.", "zz"),
          ("to", "e:nest.", "#{p}zz", {"y": -30, "duration": .5, "yoyo": True, "repeat": 5}, "the z's float"), ("face", "w:awake!", "milo", "wow"), ("hop", "w:awake!", "milo")],
      words=[("w:awake!", "WIDE AWAKE!", .7, .16, .8, "sun")]),
    S("dawn_wood", MB("dawn_wood"), "Some friends sleep in the day, and look for food at night. Thank you, Hazel!", beat="ending", tag="Milo: some friends sleep in the day",
      hide=["hazel"], fx=[("face", 0.02, "milo", "happy"), ("hop", "w:night.", "milo"), ("nod", "w:Thank", "milo")],
      words=[("w:night.", "AWAKE AT NIGHT", .5, .16, .66, "pill"), ("w:Thank", "THANK YOU!", .76, .34, .7, "sun")]),
    S("dawn_wood", (860, 680, 1700), "Do you remember? When do hedgehogs look for food? At night, or in the day?", q=True, beat="ending", tag="question: night or day again", pause=3.2,
      cam2=(700, 780, 1200), actors=[HZ(380, 940, .62), MI(1100, 760)], props=[prop("lid", A.hog_lids, 380, 940, .62), prop("zz", A.zzz, 540, 760, .6)],
      fx=[("to", 0.3, "#{p}zz", {"y": -30, "duration": .5, "yoyo": True, "repeat": 13}, "the z's float"),
          ("hop", "w:remember?", "milo"), ("signs", "w:night,", ["NIGHT", "DAY"], 0, "wait:1.8")]),
    S("dawn_wood", (960, 540, 1920), "And what helps Hazel find her food? Her eyes, or her nose?", q=True, beat="ending", tag="question: eyes or nose", pause=3.2,
      cam2=(900, 600, 1720), actors=[HZ(380, 940, .62), MI(1100, 760)], props=[prop("lid", A.hog_lids, 380, 940, .62), prop("zz", A.zzz, 540, 760, .6)],
      fx=[("to", 0.3, "#{p}zz", {"y": -30, "duration": .5, "yoyo": True, "repeat": 13}, "the z's float"),
          ("fly", 0.5, "milo", 1180, 700, 1.2), ("signs", "w:eyes,", ["EYES", "NOSE"], 1, "wait:1.8")]),
    S("dawn_wood", (900, 580, 1800), "Sniff and snuffle, through the night. My little nose can find a bite!", beat="ending", tag="the closing rhyme", cam2=(900, 600, 1720),
      actors=[HZ(380, 940, .62), MI(1100, 600)], props=[prop("lid", A.hog_lids, 380, 940, .62), prop("zz", A.zzz, 540, 760, .6)],
      fx=[("to", 0.3, "#{p}zz", {"y": -30, "duration": .5, "yoyo": True, "repeat": 9}, "the z's float"),
          ("hop", "w:Sniff", "milo"), ("fly", "w:My", "milo", 1260, 640, 1.4), ("hop", "w:bite!", "milo")],
      words=[("w:Sniff", "SNIFF AND SNUFFLE", .66, .13, .58, "sun"), ("w:My", "MY LITTLE NOSE!", .66, .25, .58, "pill")]),
    S("dawn_wood", (800, 680, 1400), who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(800, 670, 1500), actors=[HZ(380, 940, .62), MI(1000, 680)], props=[prop("lid", A.hog_lids, 380, 940, .62), prop("zz", A.zzz, 540, 760, .6)],
      fx=[("face", 0.02, "milo", "happy"), ("hop", 1.0, "milo"), ("fly", 1.6, "milo", 940, 640, 1.2), ("hop", 3.0, "milo")], words=[(TB(3), "HOORAY!", .44, .16, .9, "sun")]),
    S("dawn_wood", MB("dawn_wood"), "Next time: Hazel and the Crunchy Leaf Bed! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure",
      hide=["hazel"], fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .5, .1, .62, "sun"), ("w:See", "SEE YOU SOON!", .5, .22, .5, "pill")]),
    # the goodbye asks to like and subscribe (owner, Nov 27 2026 7:29 PM; added Nov 28 by the 8:43 AM adventure build): Milo alone, the last shot before the closing intro
    S("dawn_wood", MB("dawn_wood", w=760), SUBSCRIBE_LINE, beat="ending", tag="goodbye: like and subscribe", hide=["hazel"], cam2=MB("dawn_wood", w=1150),
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:Thank", "milo"), ("hop", "w:subscribe,", "milo")],
      words=[("w:Thank", "THANK YOU!", .74, .2, .8, "sun")]),      # the camera pulls out (a push in carried the words off the frame: stills r7)
    *intro_shots(),      # and again as the last shots: the video ends on the logo with the whole cast
]

# thumbnail (thumb.py): the promise: Hazel's nose down to the ground under a big moon, smell lines rising; 2 words, none of the title's words, no watermark
THUMBS = {
    "za_ep17": {"place": "logglade", "cam": (1120, 600, 1340),
                "actors": [("hedgehog", 1000, 940, 1.35, False, "gsap.set('#P-neck',{rotation:16,svgOrigin:'90 -110'});")],
                "props": [(A.sniff, 1490, 945, 1.25)],
                "words": [("SNIFF, SNIFF!", 820, 260, 170, "sun", -5)]},
}
