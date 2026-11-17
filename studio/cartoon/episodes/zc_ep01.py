"""zc_ep01: "What Is Inside a Camel's Hump? Baby Camel Story with Milo" - the first cartoon explainer (TEST, not for upload
until Noelson approves the cartoon format).
Built on the two winners: a baby and her mama (Where Is My Mama?) + one myth turned over (Camel Humps Are Full of Fat, Not Water!).

FACTS, read at the source on Nov 16 2026:
 [SDZ] San Diego Zoo, animals.sandiegozoo.org/animals/camel
   "They store fat, not water. The fat becomes an energy source for the camel."
   "When food is scarce, the camel's body uses the fat stored in the hump, causing the hump to lean over and droop."
   "The calf has no humps but small peaks of hide, each topped with a tassel of curly hair to indicate where the humps will form."
   "a newborn camel is able to walk beside the mother within half an hour."   "Mothers and their newborns hum to each other."
   "The dromedary camel has one hump and the Bactrian camel has two."   "A camel can go a week or more without water"
   "Double rows of extra-long eyelashes also help keep sand out of the eyes."   "camels can close their nostrils to keep sand out of their nose"
   "Their large, broad feet ... expand when stepped on and contract when lifted to simplify walking in sand or snow."
   "These tough but flexible lips can break off and eat vegetation such as thorns or salty plants"
 [NG] National Geographic, Arabian camel: "The hump stores up to 80 pounds of fat"; "A very thirsty animal can drink 30 gallons of water in only 13 minutes."
 [NGK] National Geographic Kids, Bactrian camel: "rocky deserts where it gets very cold in the winter"; "mountain areas where snow and springs provide water";
   "two rows of long eyelashes protect their eyes from blowing sand and ice."
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art
from toon import shot

EP = {"id": "zc_ep01", "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0,
      "title": "What Is Inside a Camel's Hump? Baby Camel Story with Milo", "thumb_text": "NOT WATER?!",
      "description": ("What is inside a camel's hump? Is it water? Baby camel Sandy has no hump at all, so she and Milo the bluebird go to find out! "
                      "A gentle animal story for ages 2-6 with questions to answer, things to count and a quiz at the end.\n"
                      "Kids learn that a camel's hump is full of fat, why a hump can stand tall or flop over, how much a camel can drink, "
                      "how long eyelashes and closing noses keep sand out, and why some camels have two humps.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (camel); National Geographic (Arabian camel); National Geographic Kids (Bactrian camel)."),
      "tags": ["camel", "camels for kids", "camel hump", "baby camel", "desert animals for kids", "animal facts for kids", "learning videos for toddlers", "preschool", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "dunes": [("mama", "camel", 1390, 905, 1.0), ("calf", "calf", 700, 935, .56), ("milo", "milo", 330, 560, .8, False, True)],
    "trail": [("mama", "camel", 1180, 900, .95), ("calf", "calf", 590, 930, .54), ("milo", "milo", 300, 500, .75, False, True)],
    "oasis": [("mama", "camel", 1000, 880, .9), ("calf", "calf", 400, 915, .52), ("milo", "milo", 1640, 520, .72, True, True)],
    "wind": [("mama", "camel", 1370, 905, 1.0), ("calf", "calf", 690, 935, .56), ("milo", "milo", 320, 540, .78, False, True)],
    "gobi": [("bac", "bactrian", 1180, 920, .95), ("milo", "milo", 400, 560, .8, False, True)],
    "night": [("mama", "camel", 1260, 905, .95), ("calf", "calf", 680, 935, .54), ("milo", "milo", 290, 892, .8, False, False)],
    "zoo": [("milo", "milo", 960, 940, 1.1, False, False)],
}
CAMEL_PT = {"head": (345, -600), "eye": (352, -612), "nose": (452, -594), "mouth": (440, -548), "hump": (0, -500), "humptop": (0, -600), "back": (0, -440), "body": (0, -322), "feet": (0, 0), "legs": (10, -130)}
MILO_PT = {"head": (0, -185), "body": (0, -150), "top": (0, -360), "feet": (0, 0)}


def P(place, who, part="head", dx=0, dy=0):
    """Where a part of a character is on the stage (so cameras and labels follow the cast, not guessed numbers)."""
    a = next(a for a in STAGES[place] if a[0] == who); kind, x, y, s = a[1], a[2], a[3], a[4]; flip = len(a) > 5 and a[5]
    if kind == "milo": lx, ly = MILO_PT[part]
    else:
        calf = kind == "calf"; lx, ly = CAMEL_PT[part]
        if calf and part in ("head", "eye", "nose", "mouth"): lx, ly = 190 + (lx - 190) * 1.22, -330 + (ly + 330) * 1.22
        if part != "feet": ly += -31 if calf else -1
    return round(x + (-lx if flip else lx) * s + dx), round(y + ly * s + dy)


def C(place, who, part, w, dx=0, dy=0): return (*P(place, who, part, dx, dy), w)             # a 16:9 camera on a part
def V(place, who, part, h, dx=0, dy=0): x, y = P(place, who, part, dx, dy); return (x, round(y - h * .05), h)   # a 9:16 camera: the subject sits a little below the middle, under the title


WIDE = (960, 540, 1920)
PAPER = (960, 540, 1920)


def S(place, cam, say="", words=(), fx=(), pcam=None, **kw):
    """shot() plus words=[(at, text, fx, fy, k, cls)]: a word at a place in the PICTURE (fx, fy = 0..1 across the camera's view),
    sized to the camera so it reads the same in a close-up and in a wide shot. In the 9:16 version it sits at (pfx, pfy) of that view."""
    out = list(fx)
    for w in words:
        at, text, fx_, fy_ = w[:4]; k = w[4] if len(w) > 4 else 1.0; cls = w[5] if len(w) > 5 else ""; pf = w[6] if len(w) > 6 else (.5, .34); pk = w[7] if len(w) > 7 else k
        cx, cy, cw = cam; o = {"x": round(cx + (fx_ - .5) * cw), "y": round(cy + (fy_ - .5) * cw * 9 / 16), "size": round(cw * .068 * k), "cls": cls}
        pc = pcam or (cam[0], cam[1], cam[2] * 9 / 16 * 1.5); pw = pc[2] * 9 / 16
        o["p"] = {"x": round(pc[0] + (pf[0] - .5) * pw), "y": round(pc[1] + (pf[1] - .5) * pc[2]), "size": round(pw * .125 * pk)}
        out.append(("word", at, text, o))
    return shot(place, cam, say, fx=out, pcam=pcam, **kw)


def W(c, k=1.05): return (c[0], c[1], round(c[2] * k))      # the end of a slow pull-out: a wide 9:16 view only gets wider, so nobody slides out of the frame


def prop(name, fn, x, y, s=1.0, hidden=False, p=None): return (name, fn, x, y, s, "hidden" if hidden else "", p)   # p=(x, y, s): where it sits in the 9:16 picture


TWO = (1215, 570, 1460); TWOP = (1230, 480, 2560)
# The camels' hums: "mmm" sung on notes by the voice itself (sing.hum_word) with a soft music box, in C like the show's loop, at the loop's speed.
# Mama low (sol do mi), Sandy high, ending on Mama's last note (do' sol mi); the lullaby is Mama's tune and its way home (mi re do), slower.
SCL = C("dunes", "calf", "head", 600, -150, -65); SCLP = (725, 636, 1300)      # Sandy's close-up while she hums: Mama's tail stays outside
HUM = {"hum": True, "bpm": 96, "chords": "C C", "style": "lullaby", "outro_bars": 0, "group": False, "level": 0.3}
HUM_MAMA = dict(HUM, voice="bf_emma", formant=1.0, lines=[{"text": "Mmm, mmm, mmm.", "notes": "G3:1 C4:1 E4:2"}])
HUM_SANDY = dict(HUM, voice="af_sarah", formant=1.15, level=0.27, lines=[{"text": "Mmm, mmm, mmm.", "notes": "C5:1 G4:1 E4:2"}])
HUM_ALL = dict(HUM, voice="af_sarah", formant=1.15, group=True, level=0.3, lines=[{"text": "Mmm, mmm, mmm!", "notes": "C5:1 G4:1 E4:2"}])
HUM_LULLABY = dict(HUM, bpm=72, voice="bf_emma", formant=1.0, level=0.26, lines=[{"text": "Mmm, mmm, mmm.", "notes": "G3:1 C4:1 E4:2"}, {"text": "Mmm, mmm, mmm.", "notes": "E4:1 D4:1 C4:2"}])
DRK = (1180, 500, 1700); OAS = (800, 310, 2400); WND = (1205, 380, 2400); GOB = (1251, 461, 1700); EYE = (960, 560, 2300)      # 9:16 at the oasis: Mama drinking with sky above for the count and the jug; Mama and Sandy whole
SHOTS = [
    # ---------------------------------------------------------------- HOOK (the question, the animal, in the first 5 seconds)
    S("dunes", C("dunes", "mama", "hump", 1000, 60, 10), "What is inside a camel's hump?", q=True, tag="hook: the hump", pcam=V("dunes", "mama", "hump", 1400, 120),
      words=[("w:inside", "?", .2, .3, 3.2, "sun", (.22, .42))], fx=[("hop", "w:hump?", "mama")], cam2=C("dunes", "mama", "hump", 860, 40, 0)),
    S("dunes", C("dunes", "calf", "back", 720, 30, -20), "And why does baby Sandy have no hump at all?", tag="hook: no hump", hide=["milo"], pcam=V("dunes", "calf", "back", 1000, 60, -150),
      words=[("w:no", "NO HUMP?", .27, .2, 1.2, "", (.42, .31))], fx=[("lookat", "w:no", "calf", -12)]),
    S("dunes", C("dunes", "milo", "body", 760), "I'm Milo. Let's find out together!", tag="hook: Milo", pcam=V("dunes", "milo", "body", 900),
      fx=[("hop", "w:find", "milo")]),
    # ---------------------------------------------------------------- INTRO
    S("zoo", WIDE, "Welcome to The Animated Zoo, friends!", trans="iris", tag="gate wide", words=[("w:Animated", "HELLO!", .74, .6, 1.2, "pill")]),
    S("zoo", C("zoo", "milo", "body", 900, 0, -40), "Today we fly far away, to the hot, sunny desert.", tag="Milo close", words=[("w:desert", "THE DESERT", .5, .16, 1.1, "sun")]),
    S("dunes", WIDE, "Here we are! Look at all that sand.", trans="iris", tag="dunes wide", cam2=(1000, 560, 1780), fx=[("fromto", 0, "#{p}milo_w", {"x": -300, "y": 200}, {"x": 330, "y": 560, "duration": 1.3, "ease": "power2.out"}, "Milo flies in")]),
    S("dunes", (1430, 330, 1150), "The desert is hot in the day. Phew!", tag="the sun", hide=["calf", "milo"], words=[("w:hot", "HOT!", .2, .46, 1.5, "sun")],
      fx=[("to", "w:hot", "#{p}sun", {"scale": 1.18, "transformOrigin": "50% 50%", "duration": .4, "yoyo": True, "repeat": 5}, "the sun glows")]),
    # ---------------------------------------------------------------- PART 1: what is inside the hump?
    S("dunes", TWO, "This is Sandy. Sandy is a baby camel.", part=1, tag="two camels", hide=["milo"], pcam=TWOP, words=[("w:Sandy.", "SANDY", .2, .24, 1.0, "pill", (.32, .42))], fx=[("hop", "w:Sandy.", "calf")]),
    S("dunes", C("dunes", "calf", "head", 760, -30, 30), "A baby camel is called a calf. Can you say calf?", part=1, q=True, tag="Sandy close", hide=["mama"], pcam=V("dunes", "calf", "head", 940, -30, 60),
      words=[("w:calf.", "CALF", .22, .26, 1.5, "sun", (.5, .34))], fx=[("nod", "w:say", "calf")]),
    S("dunes", C("dunes", "mama", "head", 900, -120, 90), "And this is Sandy's mama. Hello, Mama!", part=1, tag="Mama close", pcam=V("dunes", "mama", "head", 1100, -100, 60),
      words=[("w:mama.", "MAMA", .24, .2, 1.3, "pill", (.36, .305), 1.1)], fx=[("nod", "w:Hello,", "mama")]),
    S("dunes", TWO, "Mama is tall. Sandy is small.", part=1, tag="tall and small", hide=["milo"], pcam=TWOP, words=[("w:tall.", "TALL", .6, .13, 1.1, "", (.72, .3)), ("w:small.", "SMALL", .16, .3, 1.0, "sun", (.26, .46))]),
    S("paper_blue", PAPER, "When Sandy was born, she stood up fast.", part=1, tag="board: newborn", actors=[("calf", "calf", 720, 900, .8)], pcam=(900, 560, 1500),
      props=[prop("clock", art.clock, 1420, 430, 1.2)], fx=[("fromto", 0, "#{p}calf", {"y": 60, "scaleY": .8, "svgOrigin": "0 0"}, {"y": 0, "scaleY": 1, "duration": 1.0, "ease": "back.out(2)"}, "Sandy stands up")]),
    S("paper_blue", (1180, 480, 1400), "In just half an hour, she could walk beside her mama!", part=1, tag="board: the clock", actors=[("calf", "calf", 720, 900, .8)], pcam=(1260, 500, 1300),
      props=[prop("clock", art.clock, 1420, 400, 1.05)], words=[("w:half", "30 MINUTES", .7, .79, .95, "pill", (.52, .7))],
      fx=[("to", "w:half", "#{p}clock-min", {"rotation": 180, "svgOrigin": "0 0", "duration": 1.6, "ease": "power1.inOut"}, "the clock hand goes round half way")]),
    S("dunes", WIDE, "Step, step, step! Off they go.", part=1, tag="they walk", pcam=(1150, 520, 1900), cam2=(1080, 560, 1840),
      fx=[("walk", 0.1, "mama", 110, 3.0), ("walk", 0.1, "calf", 110, 3.0)]),
    S("dunes", C("dunes", "calf", "body", 900, 120, -40), "Sandy stays close to her mama.", part=1, tag="close to Mama", pcam=V("dunes", "calf", "body", 1200, 150, -60), fx=[("hop", "w:close", "calf")]),
    S("dunes", TWO, "Mama and Sandy hum to each other.", part=1, tag="they hum", hide=["milo"], pcam=TWOP, pcam2=W(TWOP),
      fx=[("lookat", "w:hum", "mama", 14), ("lookat", "w:hum", "calf", -14)]),
    # the hums are music now (Noelson, Nov 16: the parts where the animals sing had issues - it was a two-note beep). Mama hums low, Sandy answers high, then everybody hums.
    S("dunes", C("dunes", "mama", "head", 900, -70, 10), part=1, tag="Mama hums", who="", sing=HUM_MAMA, pcam=V("dunes", "mama", "head", 1100, -60, 40),
      props=[prop("n1", lambda p: art.note(p), 1900, 300, 1.1, True, p=(1790, 180, 1.0)), prop("n2", lambda p: art.note(p, "#58b9e8"), 1990, 330, .9, True, p=(1890, 250, .9))],
      fx=[("lookat", 0, "mama", 14), ("show", 0.15, "n1", None, False), ("show", 1.4, "n2", None, False), ("to", 0.15, "#{p}n1_w", {"y": "-=60", "x": "+=30", "rotation": 10, "duration": 2.3, "ease": "sine.out"}),
          ("to", 1.4, "#{p}n2_w", {"y": "-=50", "x": "+=20", "rotation": -12, "duration": 1.2, "ease": "sine.out"})]),
    S("dunes", SCL, part=1, tag="Sandy hums", who="", sing=HUM_SANDY, hide=["milo"], cam2=SCL, pcam=SCLP, pcam2=SCLP,      # held still: with the slow drift Mama's tail swings into the close-up
      props=[prop("n1", lambda p: art.note(p, "#58b9e8"), 770, 450, .7, True), prop("n2", lambda p: art.note(p, "#ff9ab8"), 945, 430, .55, True)],
      fx=[("lookat", 0, "calf", -14), ("show", 0.15, "n1", None, False), ("show", 1.4, "n2", None, False), ("to", 0.15, "#{p}n1_w", {"y": "-=25", "x": "-=10", "rotation": -10, "duration": 2.3, "ease": "sine.out"}),
          ("to", 1.4, "#{p}n2_w", {"y": "-=20", "x": "+=8", "rotation": 10, "duration": 1.2, "ease": "sine.out"})]),
    S("dunes", C("dunes", "milo", "body", 820, 60, -20), "Can you hum like a camel?", part=1, q=True, tag="hum along", pcam=V("dunes", "milo", "body", 860, -60, 70)),
    S("dunes", TWO, part=1, tag="everybody hums", who="", sing=HUM_ALL, pause=0.3, hide=["milo"], pcam=TWOP, pcam2=W(TWOP), words=[(0.1, "YOUR TURN!", .4, .1, .8, "pill", (.5, .33))],
      props=[prop("n1", lambda p: art.note(p), 1620, 340, 1.3, True, p=(1640, 250, 2.0)), prop("n2", lambda p: art.note(p, "#58b9e8"), 1030, 480, 1.0, True, p=(1040, 420, 1.7)),
             prop("n3", lambda p: art.note(p, "#59c36a"), 1180, 420, .9, True, p=(1230, 250, 1.6))],
      fx=[("lookat", 0, "mama", 14), ("lookat", 0, "calf", -14), ("show", 0.15, "n1", None, False), ("show", 0.75, "n2", None, False), ("show", 1.4, "n3", None, False),
          ("to", 0.15, "#{p}n1_w,#{p}n2_w,#{p}n3_w", {"y": "-=50", "duration": 2.4, "ease": "sine.out"})]),
    S("dunes", C("dunes", "mama", "hump", 1000, 60, 20), "Now look at Mama's back. She has a big, tall hump!", part=1, tag="the hump", hide=["calf"], pcam=V("dunes", "mama", "hump", 1500, 110),
      words=[("w:hump!", "HUMP", .2, .2, 1.6, "sun", (.3, .33))], props=[prop("ar", lambda p: art.arrow(p, 1310, 170, 1380, 285), 0, 0, 1, True)], fx=[("show", "w:big,", "ar")]),
    S("dunes", C("dunes", "calf", "back", 700, 20, -30), "But Sandy has no hump. Just a little tuft of curly hair.", part=1, tag="the tuft", hide=["milo"], pcam=V("dunes", "calf", "back", 880, 30, -40),
      words=[("w:no", "NO HUMP", .5, .14, 1.2, "", (.5, .34)), ("w:tuft", "CURLY TUFT", .26, .76, 1.0, "pill", (.5, .66))],
      props=[prop("ar", lambda p: art.arrow(p, 620, 520, 760, 640), 0, 0, 1, True)], fx=[("show", "w:little", "ar")]),
    S("dunes", C("dunes", "calf", "head", 900, 60, -40), "Sandy looks up at Mama's hump. What is in there?", part=1, q=True, tag="Sandy wonders", pcam=V("dunes", "calf", "head", 1100, 60, -20),
      words=[("w:What", "?", .7, .2, 2.4, "sun", (.72, .36))], fx=[("lookat", 0.2, "calf", -16)]),
    S("dunes", (1000, 590, 1840), "What do you think? Is it water? Or is it fat?", part=1, q=True, tag="question 1", pause=3.4, pcam=TWOP,
      fx=[("signs", "w:water?", ["WATER", "FAT"], 1, "wait:3.0"), ("hop", "wait:3.05", "calf")]),
    S("paper", (960, 520, 1500), "It is fat! A camel's hump is full of fat.", part=1, tag="board: inside the hump", pcam=(960, 430, 1700),
      props=[prop("cut", art.hump_cutaway, 960, 880, 1.45)], words=[("w:fat!", "FAT!", .2, .24, 1.9, "sun", (.5, .3))],
      fx=[("fromto", 0, "#{p}cut_w", {"scale": .5, "transformOrigin": "50% 100%"}, {"scale": 1.45, "duration": .6, "ease": "back.out(1.6)"}, "the hump opens"),
          ("to", "w:full", ".{p}cut-fat", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .3, "yoyo": True, "repeat": 5, "stagger": .05}, "the fat wobbles")]),
    S("paper", (1000, 520, 1640), "Not water. No, no, no!", part=1, tag="board: not water", pcam=(1130, 560, 1500),
      props=[prop("cut", art.hump_cutaway, 760, 880, 1.2), prop("drop", art.water_drop, 1420, 520, 1.7, True), prop("x", art.cross, 1420, 540, 1.5, True)],
      words=[("w:no,", "NOT WATER!", .72, .78, 1.1, "pill", (.5, .66))], fx=[("show", 0.1, "drop"), ("show", "w:No,", "x"), ("to", "w:no,", "#{p}drop_w", {"rotation": 10, "transformOrigin": "50% 50%", "duration": .12, "yoyo": True, "repeat": 5})]),
    S("paper_pink", (960, 520, 1100), "The fat is like a lunch box.", part=1, tag="board: lunch box", pcam=(960, 560, 1150),
      props=[prop("lb", art.lunchbox, 960, 760, 2.6, True)], fx=[("show", "w:lunch", "lb")], words=[("e:box.", "LUNCH BOX", .5, .12, 1.2, "sun", (.5, .32))]),
    S("paper_pink", (960, 520, 1500), "It gives the camel energy when there is no food around.", part=1, tag="board: energy", pcam=(960, 667, 1900),
      props=[prop("lb", art.lunchbox, 960, 800, 1.7), prop("b1", art.bolt, 520, 480, 1.3, True), prop("b2", art.bolt, 1400, 480, 1.3, True), prop("b3", art.bolt, 1500, 690, .9, True, p=(960, 942, .8))],
      fx=[("show", "w:energy", "b1"), ("show", "e:energy", "b2"), ("show", "w:no", "b3")], words=[("w:energy", "ENERGY!", .5, .16, 1.2, "pill", (.5, .3), 1.0)]),
    S("paper", (960, 520, 1500), "One big hump can hold eighty pounds of fat!", part=1, tag="board: 80 pounds", pcam=(960, 440, 2500),
      props=[prop("sc", art.scale_prop, 1300, 825, 1.5), prop("cut", art.hump_cutaway, 620, 835, 1.0)], words=[("w:eighty", "80 POUNDS", .5, .12, 1.25, "sun", (.5, .36))],
      fx=[("to", "w:eighty", "#{p}sc-hand", {"rotation": 250, "svgOrigin": "0 -210", "duration": 1.2, "ease": "back.out(1.4)"}, "the scale swings")]),
    S("dunes", (1070, 565, 1800), "Let's say it together. Fat, not water!", part=1, q=True, tag="say it", pcam=TWOP, words=[("w:Fat,", "FAT, NOT WATER!", .46, .2, 1.0, "sun", (.5, .32), .8)],
      fx=[("hop", "w:Fat,", "calf"), ("hop", "w:not", "mama")]),
    # ---------------------------------------------------------------- PART 2: food, the hump and water
    S("trail", WIDE, "Mama and Sandy walk down the rocky trail.", part=2, trans="iris", tag="trail wide", cam2=(1060, 560, 1740), pcam=(1195, 282, 2400), pcam2=(1195, 282, 2400),
      props=[prop("bush", lambda p: art._thorn(p, 0, 0), 1700, 905, 1.5)], fx=[("fromto", 0, "#{p}mama_w", {"x": 880}, {"x": 1180, "duration": 3.2, "ease": "none"}), ("fromto", 0, "#{p}calf_w", {"x": 330}, {"x": 590, "duration": 3.2, "ease": "none"}),
                                                           ("walk", 0, "mama", 0, 3.2), ("walk", 0, "calf", 0, 3.2)]),
    S("trail", (1660, 760, 760), "Look! A thorny bush. Those thorns are sharp.", part=2, tag="the bush", props=[prop("bush", lambda p: art._thorn(p, 0, 0), 1700, 905, 1.5)],
      words=[("w:thorny", "THORNS", .26, .2, 1.3, "sun")], fx=[("to", "w:sharp.", "#{p}bush_w", {"rotation": 4, "transformOrigin": "50% 100%", "duration": .15, "yoyo": True, "repeat": 5}, "the bush shakes")]),
    S("trail", (1500, 590, 1150), "But camels have tough lips. Mama can eat thorny plants!", part=2, tag="Mama eats", props=[prop("bush", lambda p: art._thorn(p, 0, 0), 1700, 905, 1.5)],
      words=[("w:tough", "TOUGH LIPS", .27, .14, 1.0, "pill")], fx=[("drink", "w:Mama", "mama", 2.4, 58), ("chew", "w:eat", "mama", 2.0)]),
    S("trail", (1600, 640, 900), "Munch, munch, munch. Can you munch like Mama?", part=2, q=True, tag="munch", props=[prop("bush", lambda p: art._thorn(p, 0, 0), 1700, 905, 1.5)],
      words=[("w:Munch,", "MUNCH!", .24, .2, 1.3, "sun")], fx=[("to", 0, "#{p}mama-neck", {"rotation": 58, "svgOrigin": "190 -330", "duration": .01}), ("chew", 0.1, "mama", 4.2)]),
    S("trail", C("trail", "calf", "head", 780, 40, 30), "Sandy has a little snack too. Nibble, nibble.", part=2, tag="Sandy nibbles", props=[prop("b2", lambda p: art._thorn(p, 0, 0), 905, 945, .8)],
      fx=[("drink", 0.2, "calf", 3.0, 40), ("chew", "w:Nibble,", "calf", 1.8)], words=[("w:Nibble,", "NIBBLE!", .24, .24, 1.2, "sun")]),
    S("paper", (960, 520, 1560), "When a camel eats a lot, her hump stands up tall.", part=2, tag="board: tall hump", actors=[("cam", "camel", 880, 930, 1.05)], pcam=(1000, 535, 1900),
      words=[("w:tall.", "TALL", .2, .2, 1.6, "sun", (.3, .297), 1.0)], props=[prop("ar", lambda p: art.arrow(p, 620, 560, 620, 330), 0, 0, 1, True)],
      fx=[("fromto", 0, "#{p}cam-hump", {"scaleY": .7, "scaleX": .94, "rotation": 22, "svgOrigin": "0 -372"}, {"scaleY": 1, "scaleX": 1, "rotation": 0, "duration": 1.6, "ease": "back.out(2)"}, "the hump stands up"), ("show", "w:tall.", "ar")]),
    S("paper", (960, 520, 1560), "When there is no food for a long time, she uses the fat.", part=2, tag="board: using the fat", actors=[("cam", "camel", 880, 930, 1.05)], pcam=(1040, 610, 1750),
      props=[prop("lb", art.lunchbox, 1410, 800, .8)], words=[("w:no", "NO FOOD", .2, .2, 1.0, "pill", (.3, .3))],
      fx=[("to", "w:uses", "#{p}lb_w", {"scale": .35, "opacity": .3, "transformOrigin": "50% 100%", "duration": 1.4}, "the lunch box empties"), ("droop", "w:uses", "cam", 10)]),
    S("paper", (900, 480, 1300), "Then the hump gets soft, and leans over. Flop!", part=2, tag="board: flop", actors=[("cam", "camel", 880, 930, 1.05)], pcam=(960, 535, 1900),
      words=[("w:Flop!", "FLOP!", .24, .2, 1.7, "sun", (.3, .3), 1.0)], fx=[("to", 0, "#{p}cam-hump", {"rotation": 10, "scaleY": .9, "svgOrigin": "0 -372", "duration": .01}), ("droop", "w:leans", "cam", 30), ("snd", "w:Flop!", "boing")]),
    S("paper_blue", PAPER, "A tall hump is full. A floppy hump is empty.", part=2, tag="board: full or empty", actors=[("a", "camel", 520, 900, .78), ("b", "camel", 1300, 900, .78)], pcam=(640, 583, 1300), pcam2=(1420, 583, 1300),
      words=[("w:full.", "FULL", .25, .13, 1.3, "sun", (.36, .3), 1.1), ("w:empty.", "EMPTY", .68, .13, 1.3, "", (1.42, .3), 1.1)], fx=[("to", 0, "#{p}b-hump", {"rotation": 30, "scaleY": .72, "scaleX": .94, "svgOrigin": "0 -372", "duration": .01})]),
    S("trail", (960, 470, 1920), "Mama just had a big lunch. Is her hump tall, or floppy?", part=2, q=True, tag="question 2", pause=3.4, pcam=(1170, 255, 2500), pcam2=W((1170, 255, 2500)),
      fx=[("signs", "w:tall,", ["TALL", "FLOPPY"], 0, "wait:3.0"), ("hop", "wait:3.05", "mama")]),
    S("trail", C("trail", "mama", "hump", 1000, 60, 20), "Tall! Mama's hump is full of fat.", part=2, tag="tall!", pcam=(1340, 470, 1560), pcam2=W((1340, 470, 1560)), words=[("w:Tall!", "TALL!", .2, .26, 1.6, "sun")], fx=[("hop", "w:Tall!", "mama")]),
    S("oasis", WIDE, "Now they find a pool of cool water. Splash!", part=2, trans="iris", tag="oasis wide", cam2=(1000, 580, 1700), pcam=OAS, pcam2=OAS, words=[("w:Splash!", "SPLASH!", .5, .2, 1.3, "sun")],
      fx=[("to", "w:Splash!", "#{p}rip", {"scale": 1.3, "transformOrigin": "50% 50%", "duration": .5, "yoyo": True, "repeat": 3}, "the water ripples")]),
    S("oasis", (1130, 640, 1100), "Camels do not keep water in the hump. They drink it!", part=2, tag="Mama drinks", hide=["milo", "calf"], pcam=DRK, pcam2=W(DRK), words=[("w:drink", "DRINK!", .22, .16, 1.3, "sun")],
      fx=[("drink", "w:They", "mama", 3.0, 100)]),
    S("oasis", (1150, 640, 1000), "A thirsty camel can drink thirty gallons of water,", part=2, tag="30 gallons", hide=["milo"], pcam=DRK, pcam2=W(DRK), props=[prop("jug", art.jug, 1575, 524, 1.3, True, p=(1500, 470, 2.0))],
      fx=[("to", 0, "#{p}mama-neck", {"rotation": 100, "svgOrigin": "190 -330", "duration": .01}), ("show", "w:thirty", "jug"), ("count", "w:thirty", 30, 1.5, {"x": 1300, "y": 112})],
      words=[("e:gallons", "GALLONS", .72, .4, 1.0, "pill", (.5, .31), .8)]),
    S("oasis", (1200, 660, 900), "in only thirteen minutes! Gulp, gulp, gulp.", part=2, tag="13 minutes", hide=["milo"], pcam=DRK, pcam2=W(DRK), props=[prop("clock", art.clock, 1500, 560, .75, p=(1520, 470, .75))],
      fx=[("to", 0, "#{p}mama-neck", {"rotation": 100, "svgOrigin": "190 -330", "duration": .01}), ("to", "w:thirteen", "#{p}clock-min", {"rotation": 78, "svgOrigin": "0 0", "duration": 1.2}, "the clock hand moves 13 minutes"),
          ("to", "w:Gulp,", "#{p}mama", {"y": "+=10", "duration": .2, "yoyo": True, "repeat": 5}, "gulp")], words=[("w:thirteen", "13 MINUTES", .3, .16, 1.0, "sun")]),
    S("paper_blue", PAPER, "After that, a camel can go a week or more without a drink.", part=2, tag="board: a week", pcam=(960, 440, 2700), props=[prop("wk", art.week, 960, 640, 1.5, p=(960, 640, 1.3))],
      fx=[("fromto", "w:week", ".{p}wk-d", {"opacity": .25}, {"opacity": 1, "duration": .2, "stagger": .22}, "seven days light up"), ("count", "w:week", 7, 1.4, {"x": 960, "y": 300})],
      words=[("e:week", "DAYS", .5, .74, 1.2, "pill", (.5, .68))]),
    S("oasis", C("oasis", "calf", "head", 900, 40, 150), "Drink up, little Sandy!", part=2, tag="Sandy drinks", pcam=(480, 742, 900), fx=[("drink", 0.2, "calf", 2.4, 96)]),
    S("oasis", (640, 700, 1000), "Let's count Sandy's sips. One, two, three!", part=2, q=True, tag="count the sips", pcam=(480, 742, 900),
      fx=[("to", 0, "#{p}calf-neck", {"rotation": 96, "svgOrigin": "190 -330", "duration": .01}), ("to", "w:One,", "#{p}calf", {"y": "+=8", "duration": .15, "yoyo": True, "repeat": 1}, "sip"),
          ("to", "w:two,", "#{p}calf", {"y": "+=8", "duration": .15, "yoyo": True, "repeat": 1}, "sip"), ("to", "w:three!", "#{p}calf", {"y": "+=8", "duration": .15, "yoyo": True, "repeat": 1}, "sip")],
      words=[("w:One,", "1", .2, .22, 2.0, "sun", (.28, .34), 1.5), ("w:two,", "2", .36, .22, 2.0, "sun", (.5, .34), 1.5), ("w:three!", "3", .52, .22, 2.0, "sun", (.72, .34), 1.5)]),
    S("oasis", (820, 600, 1500), "Ahh! That feels good.", part=2, tag="after the drink", hide=["milo"], pcam=OAS, pcam2=OAS, fx=[("hop", "w:good.", "calf"), ("nod", "w:Ahh!", "mama")], words=[("w:Ahh!", "AHH!", .42, .16, 1.3, "sun")]),
    # ---------------------------------------------------------------- PART 3: sand, snow and cousins
    S("wind", WIDE, "Whoosh! The wind is blowing the sand around.", part=3, trans="iris", tag="windy wide", pcam=WND, pcam2=W(WND), props=[prop("puff", art.sand_puffs, 960, 520, 1.0)], words=[("w:Whoosh!", "WHOOSH!", .5, .2, 1.4, "")],
      fx=[("fromto", 0, "#{p}gust", {"x": -260}, {"x": 320, "duration": 4.0, "ease": "none"}, ""), ("fromto", 0, "#{p}puff_w", {"x": 700}, {"x": 1300, "duration": 4.0, "ease": "none"}, ""), ("snd", 0.1, "whoosh")]),
    S("wind", C("wind", "milo", "body", 820), "Sand in the air tickles my eyes!", part=3, tag="Milo blinks", pcam=V("wind", "milo", "body", 1100), props=[prop("puff", art.sand_puffs, 400, 400, .6)],
      fx=[("fromto", 0, "#{p}puff_w", {"x": 200}, {"x": 560, "duration": 3.4, "ease": "none"}, ""), ("fromto", "w:tickles", "#{p}milo-eyeL-lid,#{p}milo-eyeR-lid", {"opacity": 1}, {"opacity": 0, "duration": .01, "delay": .5}, "Milo shuts his eyes")]),
    S("wind", C("wind", "mama", "head", 900, -80, 60), "But camels are ready for a sandy day.", part=3, tag="Mama calm", props=[prop("puff", art.sand_puffs, 1500, 300, .7)],
      fx=[("fromto", 0, "#{p}puff_w", {"x": 1300}, {"x": 1700, "duration": 3.4, "ease": "none"}, ""), ("nod", "w:ready", "mama")]),
    S("paper", (960, 520, 1500), "They have two rows of long eyelashes.", part=3, tag="board: the eye", pcam=EYE, props=[prop("eye", art.big_eye, 960, 600, 1.15)],
      words=[("w:two", "1", .12, .22, 1.8, "sun", (.14, .37), 1.2), ("w:rows", "2", .12, .46, 1.8, "sun", (.14, .45), 1.2), ("w:long", "EYELASHES", .78, .14, 1.0, "pill", (.56, .315), .8)],
      fx=[("to", "w:two", ".{p}eye-row0", {"stroke": "#e63946", "duration": .2, "yoyo": True, "repeat": 3}, "the first row lights up"), ("to", "w:rows", ".{p}eye-row1", {"stroke": "#e63946", "duration": .2, "yoyo": True, "repeat": 3}, "the second row lights up")]),
    S("paper", (960, 560, 1280), "The eyelashes keep sand out of their eyes. Blink, blink!", part=3, tag="board: blink", pcam=EYE, props=[prop("eye", art.big_eye, 960, 600, 1.15), prop("puff", art.sand_puffs, 500, 300, .5)],
      fx=[("fromto", 0, "#{p}puff_w", {"x": 300}, {"x": 700, "duration": 3.0, "ease": "none"}, ""), ("blinkslow", "w:Blink,", "eye", 2)], words=[("w:Blink,", "BLINK!", .2, .19, 1.2, "sun")]),
    S("wind", C("wind", "calf", "head", 760, -20, 20), "Can you blink like a camel? Blink, blink, blink!", part=3, q=True, tag="blink along", fx=[("blinkslow", "w:Blink,", "calf-eye", 3)],
      words=[("w:Blink,", "BLINK", .22, .2, 1.3, "sun")]),
    S("paper_pink", (960, 540, 1500), "And look at this nose. A camel can close its nose!", part=3, tag="board: the nose", pcam=(960, 560, 1700), props=[prop("nose", art.big_nose, 960, 620, 1.05)],
      words=[("w:close", "CLOSE!", .5, .15, 1.3, "sun")], fx=[("to", "w:close", "#{p}nose-nl,#{p}nose-nr", {"scaleY": .08, "transformOrigin": "50% 50%", "duration": .35}, "the nostrils shut")]),
    S("paper_pink", (960, 560, 1280), "Open. Closed. Open. Closed! No sand gets in.", part=3, tag="board: open, closed", pcam=(960, 560, 1900), props=[prop("nose", art.big_nose, 960, 600, 1.2)],
      fx=[("to", "w:Closed.", "#{p}nose-nl,#{p}nose-nr", {"scaleY": .08, "transformOrigin": "50% 50%", "duration": .2}, "shut"), ("to", "w:Open.:2", "#{p}nose-nl,#{p}nose-nr", {"scaleY": 1, "duration": .2}, "open"),
          ("to", "w:Closed!:2", "#{p}nose-nl,#{p}nose-nr", {"scaleY": .08, "duration": .2}, "shut")],
      words=[("w:Open.", "OPEN", .2, .14, 1.2, "", (.27, .31), .85), ("w:Closed.", "CLOSED", .78, .14, 1.2, "sun", (.7, .31), .85)]),
    S("paper_blue", (960, 540, 1500), "Camels have big, wide feet too.", part=3, tag="board: the foot", props=[prop("foot", lambda p: art.footprint(p), 960, 620, 3.0)], words=[("w:wide", "WIDE FEET", .5, .16, 1.2, "sun")],
      fx=[("fromto", 0, "#{p}foot_w", {"scale": 1.2, "transformOrigin": "50% 50%"}, {"scale": 3.0, "duration": .5, "ease": "back.out(2)"}, "the foot appears")]),
    S("paper_blue", (960, 560, 1300), "Each foot spreads out when it steps down.", part=3, tag="board: the foot spreads", pcam=(960, 600, 1900), props=[prop("foot", lambda p: art.footprint(p), 960, 620, 3.0)],
      words=[("w:spreads", "SPREAD!", .5, .14, 1.3, "pill")],
      fx=[("fromto", "w:spreads", "#{p}foot", {"scaleX": .62, "transformOrigin": "50% 50%"}, {"scaleX": 1.12, "duration": .5, "ease": "back.out(3)"}, "the foot spreads"), ("snd", "w:steps", "boing")]),
    S("wind", (1100, 640, 1500), "That helps them walk on soft sand. Step, step, step!", part=3, tag="walking on sand", hide=["milo"], pcam=(1290, 480, 2600), pcam2=(1290, 480, 2600), fx=[("walk", 0.1, "mama", 140, 3.6), ("walk", 0.1, "calf", 140, 3.6)],
      words=[("w:Step,", "STEP!", .2, .2, 1.2, "sun")]),
    S("wind", C("wind", "calf", "body", 1000, 40, 10), "No sinking for Sandy!", part=3, tag="Sandy's feet", hide=["milo"], pcam=(720, 693, 1250), words=[("w:No", "NO SINKING!", .26, .14, 1.0, "pill", (.5, .29), .85)], fx=[("hop", "w:Sandy!", "calf")]),
    S("gobi", WIDE, "Far, far away, it is cold and snowy.", part=3, trans="iris", tag="Gobi wide", pcam=GOB, pcam2=W(GOB), props=[prop("snow", art.snow, 0, 0, 1.0)], words=[("w:cold", "BRRR!", .52, .13, 1.4, "")],
      fx=[("fromto", 0, "#{p}snow_w", {"y": -200}, {"y": 160, "duration": 4.0, "ease": "none"}, "")]),
    S("gobi", C("gobi", "bac", "body", 1300, 40, -120), "Sandy's cousins live here. Look closely at this camel's back!", part=3, tag="the cousin", pcam=GOB, pcam2=W(GOB), props=[prop("snow", art.snow, 0, 0, 1.0)],
      fx=[("fromto", 0, "#{p}snow_w", {"y": -200}, {"y": 220, "duration": 5.0, "ease": "none"}, ""), ("nod", "w:Look", "bac")]),
    S("gobi", C("gobi", "bac", "hump", 1000, 0, 20), "One hump, two humps! This camel has two.", part=3, q=True, tag="count the humps", pcam=GOB, pcam2=W(GOB), props=[prop("snow", art.snow, 0, 0, 1.0)],
      words=[("w:One", "1", .41, .2, 1.8, "sun", (.3, .36), 1.3), ("w:two", "2", .59, .2, 1.8, "sun", (.54, .36), 1.3)], fx=[("fromto", 0, "#{p}snow_w", {"y": -200}, {"y": 220, "duration": 5.0, "ease": "none"}, "")]),
    S("paper_blue", PAPER, "Some camels have one hump. Some camels have two.", part=3, tag="board: one or two", actors=[("a", "camel", 520, 900, .78), ("b", "bactrian", 1320, 900, .78)], pcam=(640, 583, 1300), pcam2=(1440, 583, 1300),
      words=[("w:one", "1 HUMP", .25, .12, 1.3, "sun", (.36, .3), 1.0), ("w:two.", "2 HUMPS", .7, .12, 1.3, "", (1.45, .3), 1.0)]),
    S("gobi", C("gobi", "bac", "head", 900, -100, 60), "Long eyelashes keep out the snow and ice, too.", part=3, tag="cousin close", props=[prop("snow", art.snow, 0, 0, 1.0)],
      fx=[("fromto", 0, "#{p}snow_w", {"y": -200}, {"y": 220, "duration": 5.0, "ease": "none"}, ""), ("blinkslow", "w:eyelashes", "bac-eye", 2)], words=[("w:snow", "SNOW", .22, .2, 1.3, "", (.3, .29))]),
    S("gobi", (960, 480, 1920), "How many humps does Sandy's mama have? One, or two?", part=3, q=True, tag="question 3", pause=3.4, pcam=GOB, pcam2=W(GOB), props=[prop("snow", art.snow, 0, 0, 1.0)],
      fx=[("fromto", 0, "#{p}snow_w", {"y": -200}, {"y": 320, "duration": 9.0, "ease": "none"}, ""), ("signs", "w:One,", ["ONE", "TWO"], 0, "wait:3.0")]),
    S("dunes", C("dunes", "mama", "hump", 1100, 60, 20), "One! Mama has one big hump.", part=3, tag="one hump", hide=["calf"], pcam=(1465, 473, 1600), pcam2=W((1465, 473, 1600)), words=[("w:One!", "1", .2, .28, 2.4, "sun", (.2, .42), 1.4)], fx=[("hop", "w:One!", "mama")]),
    # ---------------------------------------------------------------- QUIZ + RECAP
    S("night", WIDE, "The sun goes down. Time to remember what we learned!", part=4, trans="iris", tag="night wide", cam2=(1000, 560, 1760),
      fx=[("to", 0, ".{p}star", {"opacity": .2, "duration": .5, "yoyo": True, "repeat": 9, "stagger": {"each": .05, "from": "random"}}, "the stars twinkle")], words=[("w:remember", "QUIZ TIME!", .5, .2, 1.3, "sun")]),
    S("night", (960, 520, 1920), "What is inside a camel's hump? Water, or fat?", part=4, q=True, tag="quiz 1", pause=3.2, pcam=(963, 179, 2800), fx=[("signs", "w:Water,", ["WATER", "FAT"], 1, "wait:2.8")]),
    S("paper", (960, 520, 1500), "Fat! It is the camel's lunch box.", part=4, tag="board: fat again", pcam=(960, 560, 2100), props=[prop("cut", art.hump_cutaway, 700, 880, 1.25, p=(760, 880, 1.25)), prop("lb", art.lunchbox, 1400, 780, 1.4, True, p=(1330, 860, 1.2))],
      words=[("w:Fat!", "FAT!", .5, .12, 1.6, "sun")], fx=[("show", "w:lunch", "lb")]),
    S("night", (960, 520, 1920), "Was baby Sandy born with a hump? Yes, or no?", part=4, q=True, tag="quiz 2", pause=3.2, fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.8")]),
    S("night", C("night", "calf", "back", 760, 30, -30), "No! Just a little curly tuft.", part=4, tag="the tuft again", hide=["milo"], words=[("w:No!", "NO!", .22, .22, 1.6, "sun")],
      props=[prop("ar", lambda p: art.arrow(p, 540, 520, 660, 630), 0, 0, 1, True)], fx=[("show", "w:curly", "ar")]),
    S("paper_blue", (960, 520, 1560), "How do camels keep sand out of their eyes?", part=4, q=True, tag="quiz 3", pause=1.6, pcam=EYE, props=[prop("eye", art.big_eye, 960, 620, 1.05)],
      words=[("end+0.3", "?", .86, .2, 2.4, "sun", (.8, .33), 1.4)]),
    S("paper_blue", (960, 560, 1300), "With two rows of long eyelashes!", part=4, tag="board: lashes again", pcam=EYE, props=[prop("eye", art.big_eye, 960, 620, 1.05)],
      fx=[("blinkslow", "w:two", "eye", 2)], words=[("w:two", "2 ROWS", .5, .1, 1.3, "sun")]),
    S("paper_pink", (960, 520, 1560), "As Sandy grows up, her hump will grow too.", part=4, tag="board: the hump grows", actors=[("c", "camel", 900, 930, 1.0)], pcam=(1020, 520, 1700),
      fx=[("grow", 0.2, "c", .8)], words=[("w:grow", "GROW!", .24, .2, 1.3, "sun", (.3, .3))]),
    S("night", C("night", "calf", "head", 860, 0, 20), "One day, Sandy will have a hump just like Mama's.", part=4, tag="Sandy happy", hide=["milo"], fx=[("hop", "w:hump", "calf", 2)]),
    S("night", (900, 560, 1760), "And it will be full of... fat! You remembered!", part=4, q=True, tag="you remembered", words=[("w:fat!", "FAT!", .5, .14, 1.7, "sun")], fx=[("hop", "w:fat!", "milo"), ("snd", "w:fat!", "ding")],
      speak="And it will be full of, fat! You remembered!"),
    S("night", C("night", "milo", "body", 900, 40, -30), "Today we learned three big things.", part=4, tag="recap", hide=["calf", "mama"], words=[("w:three", "3", .78, .3, 2.6, "sun")]),
    S("paper", (960, 520, 1500), "One. A hump is full of fat, not water.", part=4, tag="recap 1", props=[prop("cut", art.hump_cutaway, 1180, 880, 1.2)], words=[("w:One.", "1", .14, .26, 2.4, "sun"), ("w:fat,", "FAT", .2, .62, 1.6, "pill")]),
    S("paper_blue", (960, 520, 1500), "Two. A baby camel has no hump yet.", part=4, tag="recap 2", actors=[("c", "calf", 1150, 900, .8)], words=[("w:Two.", "2", .14, .26, 2.4, "sun"), ("w:no", "NO HUMP YET", .26, .64, .95, "pill")]),
    S("paper_pink", (960, 520, 1500), "Three. A camel can close its nose!", part=4, tag="recap 3", props=[prop("nose", art.big_nose, 1220, 600, 1.0)], words=[("w:Three.", "3", .14, .26, 2.4, "sun")],
      fx=[("to", "w:close", "#{p}nose-nl,#{p}nose-nr", {"scaleY": .08, "transformOrigin": "50% 50%", "duration": .3}, "the nostrils shut")]),
    S("night", (1180, 540, 1480), "Mama hums a sleepy song for Sandy.", part=4, tag="lullaby", hide=["milo"], fx=[("lookat", 0.3, "mama", 16)]),
    S("night", (1180, 540, 1480), part=4, tag="lullaby song", who="", sing=HUM_LULLABY, pause=0.4, hide=["milo"], cam2=(1160, 570, 1300),
      props=[prop("n1", lambda p: art.note(p, "#ffd97a"), 1330, 310, 1.2, True), prop("n2", lambda p: art.note(p, "#ff9ab8"), 1180, 360, 1.0, True), prop("n3", lambda p: art.note(p, "#bfe3ff"), 1040, 400, .9, True)],
      fx=[("lookat", 0, "mama", 16), ("show", 0.2, "n1", None, False), ("show", 1.9, "n2", None, False), ("sleep", 3.5, "calf"), ("show", 4.4, "n3", None, False),
          ("to", 0.2, "#{p}n1_w", {"y": "-=110", "duration": 3.0, "ease": "sine.out"}), ("to", 1.9, "#{p}n2_w", {"y": "-=100", "duration": 3.0, "ease": "sine.out"}),
          ("to", 4.4, "#{p}n3_w", {"y": "-=90", "duration": 2.4, "ease": "sine.out"})]),
    S("night", C("night", "milo", "body", 820, 20, -20), "Good night, Sandy. Good night, Mama.", part=4, tag="good night", hide=["mama", "calf"]),
    S("night", WIDE, "Thank you for learning with me, friends. See you at the zoo!", part=4, tag="goodbye", cam2=(960, 520, 2050), words=[("w:See", "SEE YOU AT THE ZOO!", .5, .2, 1.05, "pill")],
      fx=[("to", 0, ".{p}star", {"opacity": .2, "duration": .5, "yoyo": True, "repeat": 9, "stagger": {"each": .05, "from": "random"}}, ""), ("hop", "w:zoo!", "milo", 2)]),
]

SHORT1_TAGS = ["hook: the hump", "hook: no hump", "two camels", "Sandy close", "Mama close", "tall and small", "they hum", "Mama hums", "Sandy hums", "hum along", "everybody hums", "the hump", "the tuft", "Sandy wonders", "question 1",
               "board: inside the hump", "board: not water", "board: lunch box", "board: energy", "board: 80 pounds", "board: tall hump", "board: using the fat", "board: flop", "board: full or empty",
               "say it", "board: the hump grows"]
SHORTS = [{"id": "zc_ep01_short1", "title": "Why Does This Baby Camel Have No Hump?", "band": ("WHAT IS INSIDE", "THE HUMP?"), "thumb_text": "NO HUMP?!",
           "shots": [next(i for i, s in enumerate(SHOTS) if s["tag"] == t) for t in SHORT1_TAGS]}]



def T(src, **kw):
    """A copy of a shot of the lesson (by its tag), with changes, for a Short's first or last shots."""
    d = dict(next(x for x in SHOTS if x["tag"] == src)); d.update(kw); return d


# Short 2: part 2 whole (food, the hump, water) + its own hook + the lesson's quiz on the hump
SHORTS.append({"id": "zc_ep01_short2", "title": "How Much Can a Thirsty Camel Drink?", "band": ("HOW MUCH CAN", "IT DRINK?"), "thumb_text": "30 GALLONS?!", "part": 2,
               "extra_first": [S("oasis", (1130, 640, 1100), "How much water can a thirsty camel drink?", part=2, q=True, tag="hook: how much", hide=["milo", "calf"], pcam=DRK, pcam2=W(DRK),
                                 words=[("w:much", "?", .2, .3, 3.2, "sun", (.24, .36))], fx=[("drink", "w:thirsty", "mama", 2.0, 100)])],
               "extra_last": [T("quiz 1", trans="iris", hide=["milo"], pcam=(1136, 400, 2400), pcam2=(1136, 400, 2400)), T("board: fat again")]})
# Short 3: part 3 whole (sand, eyelashes, nose, feet, two humps) + the question first and the answer again at the end
SHORTS.append({"id": "zc_ep01_short3", "title": "How Do Camels Keep Sand Out of Their Eyes?", "band": ("HOW DO CAMELS", "STOP SAND?"), "thumb_text": "BLINK, BLINK!", "part": 3,
               "extra_first": [T("quiz 3", pause=0.5, part=3, tag="hook: sand in the eyes")],
               "extra_last": [S("wind", C("wind", "milo", "body", 820), "So, how do camels keep the sand out?", part=3, q=True, tag="ask again", pause=1.2, trans="iris", pcam=V("wind", "milo", "body", 900),
                                words=[("end+0.2", "?", .76, .3, 2.6, "sun", (.74, .4))]),
                              T("board: lashes again", part=3),
                              S("paper_pink", (960, 560, 1280), "And a nose that can close!", part=3, tag="board: nose again", pcam=(960, 560, 1900), props=[prop("nose", art.big_nose, 960, 600, 1.2)],
                                words=[("w:close!", "CLOSE!", .5, .14, 1.3, "sun")], fx=[("to", "w:close!", "#{p}nose-nl,#{p}nose-nr", {"scaleY": .08, "transformOrigin": "50% 50%", "duration": .3}, "the nostrils shut")]),
                              S("wind", C("wind", "calf", "head", 760, -20, 20), "Blink, blink! Bye-bye, sand!", part=3, tag="bye sand", pcam=V("wind", "calf", "head", 940, -20, 60),
                                fx=[("blinkslow", "w:Blink,", "calf-eye", 2), ("hop", "w:Bye-bye,", "calf")], words=[("w:Bye-bye,", "BYE, SAND!", .24, .2, 1.1, "sun", (.5, .3))])]})

# thumbnails (thumb.py): the example in the picture, 3 words at most, none of the title's words, no watermark
THUMBS = {
    "zc_ep01": {"place": "dunes", "cam": (960, 540, 1920),
                "actors": [("calf", 350, 1010, .88, False, 'gsap.set("#P-neck",{rotation:-12,svgOrigin:"190 -330"});')],
                "props": [(art.hump_cutaway, 1330, 965, 1.7), (art.water_drop, 1700, 250, 1.5), (art.cross, 1700, 250, 1.5)],
                "words": [("NOT WATER?!", 600, 125, 168, "sun")]},
    "zc_ep01_short1": {"place": "dunes", "cam": (1050, 480, 1450),
                       "actors": [("calf", 960, 900, 1.0, False, 'gsap.set("#P-neck",{rotation:-10,svgOrigin:"190 -330"});')],
                       "props": [(lambda p: art.arrow(p, 870, 250, 945, 395), 0, 0, 1)],
                       "words": [("WHERE IS IT?", 540, 330, 165, "sun"), ("?", 330, 600, 330, "")]},
    "zc_ep01_short2": {"place": "oasis", "cam": (1180, 500, 1700),
                       "actors": [("camel", 1000, 880, .9, False, 'gsap.set("#P-neck",{rotation:100,svgOrigin:"190 -330"});')],
                       "props": [(art.jug, 1540, 600, 2.2)],
                       "words": [("30", 540, 380, 330, "sun"), ("GALLONS?!", 540, 600, 140, "")]},
    "zc_ep01_short3": {"place": "paper_blue", "cam": (960, 540, 1900),
                       "props": [(art.big_eye, 960, 740, 1.3), (art.sand_puffs, 620, 420, .9)],
                       "words": [("BLINK,", 470, 420, 190, "sun"), ("BLINK!", 620, 620, 190, "")]},
}
SHORTS[0]["thumb_text"] = "WHERE IS IT?"; EP["thumb_text"] = "NOT WATER?!"
