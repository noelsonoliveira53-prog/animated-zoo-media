"""za_ep07 - Milo's Zoo Adventures: "Sandy and the Flying Scarf" (cartoon adventure, the 3D music-and-sync process: "beat").
At the oasis a gust of wind takes Milo's red scarf and carries it over the dunes. Sandy the baby camel and Milo set off to bring it home.
Milo tries to fly after it, but the wind is too strong for a little bird and he floats down softly. Then the blowing sand tickles his eyes,
then his beak. Resting beside a big rock, Milo thinks his scarf is gone. Sandy works it out herself: her long eyelashes keep the sand out of
her eyes, her nose closes and her wide feet do not sink, so she can walk in the wind for both of them. Milo rides on her back with his eyes
shut; she finds the scarf caught on a thorny bush at the top of the big sandy hill, picks it up and puts it back on him. Home by bedtime, Mama.
Nobody is hurt, lost, crying or trapped: the wind is a warm, gentle desert wind, Milo floats down "soft as a feather", the sand only tickles,
and Mama knows where they are going and when they will be back. Mama camel has no voice in this film (no new voice).

FACTS, read at the source on Nov 19 2026, about 9:05 AM ET (each page fetched by the session's page reader, which quoted these sentences):
 [SDZ] San Diego Zoo Wildlife Alliance, "Camel", animals.sandiegozoo.org/node/173 (the camel page)
   "Double rows of extra-long eyelashes also help keep sand out of the eyes."
   "And camels can close their nostrils to keep sand out of their nose, too!"
   "Their large, broad feet are heavily callused; they expand when stepped on and contract when lifted to simplify walking in sand or snow."
   "small peaks of hide, each topped with a tassel of curly hair to indicate where the humps will form."   (Sandy's look: a calf, no hump)
   "These tough but flexible lips can break off and eat vegetation such as thorns or salty plants"     (read; Sandy's lips pick up the scarf as story)
 [NGK] National Geographic Kids, "Bactrian camel", kids.nationalgeographic.com/animals/mammals/facts/bactrian-camel
   "Their nostrils close to block sand, and their bushy eyebrows and two rows of long eyelashes" ... "protect their eyes from blowing sand and ice."
 Said as animal facts in the film (three fact boards and closing questions), each from a quote above: camels have two rows of long eyelashes
 that help keep sand out of their eyes [SDZ, NGK]; a camel can close its nostrils to keep sand out of its nose [SDZ, NGK]; a camel's big, wide
 feet spread out when they step down, and that helps camels walk on sand [SDZ].
 Not animal facts, said as what happens in THIS story: the wind taking the scarf, the bush, Sandy picking the scarf up with her lips, Milo
 riding on her back. Nothing is said about how strong a wind a bird can fly in.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2
import art_za_ep07 as A
import kit
from kit import Kit, S, prop

EP = {"id": "za_ep07", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "sandy": {"voice": "af_sarah", "speed": .82, "pitch": 3, "formant": 1.1, "gain": .88}},
      "title": "Sandy and the Flying Scarf", "thumb_text": "GOT IT!",
      "series": "Milo's Zoo Adventures",
      "description": ("Whoosh! The desert wind takes Milo's red scarf and carries it over the dunes. Milo can't fly in the wind, and the blowing sand tickles his eyes "
                      "and his beak. But Sandy the baby camel can keep on walking. How? A gentle animal adventure for ages 2-6 about helping a friend in your own "
                      "special way, with questions to answer, a blink-along and a tune to clap along to.\n"
                      "Kids see how camels have two rows of long eyelashes that help keep sand out of their eyes, how a camel can close its nose, "
                      "and how a camel's wide feet spread out to walk on sand.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance (camel); National Geographic Kids (Bactrian camel)."),
      "tags": ["baby camel", "camel for kids", "desert animals for kids", "camel eyelashes", "windy day story", "animal stories for kids", "friendship story for kids",
               "kids adventure cartoon", "desert for kids", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "oasis": [("mama", "camel", 1330, 880, .9, True), ("sandy", "calf", 560, 915, .52), ("milo", "milo", 820, 330, .72, False, True)],
    "wind": [("sandy", "calf", 960, 935, .56), ("milo", "milo", 480, 560, .72, False, True)],
    "dunes": [("sandy", "calf", 760, 935, .56), ("milo", "milo", 400, 560, .72, False, True)],
    "trail": [("sandy", "calf", 1040, 930, .54), ("milo", "milo", 700, 930, .7)],
    "dune_eve": [("sandy", "calf", 900, 935, .56), ("milo", "milo", 870, 672, .4)],
    "night": [("mama", "camel", 1180, 905, .95, True), ("sandy", "calf", 400, 935, .54), ("milo", "milo", 1720, 760, .7, True, True)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
def only(place, *keep, stage=None): return [a[0] for a in (stage or STAGES[place]) if a[0] not in keep]

# ------------------------------------------------------------------ Milo without his scarf (until Sandy puts it back on him): the scarf parts of art.milo, picked by their colour
NOSCARF = ("#{p}milo-body>path[fill='%s'],#{p}milo-body>path[fill='%s'],#{p}milo-body>circle[fill='%s'],#{p}milo-scarf" % (art.SCARF, art.SCARF_D, art.SCARF))
BARE = ("fromto", 0, NOSCARF, {"opacity": 0}, {"opacity": 0, "duration": .01}, "")
def NS(place, cam, say="", fx=(), **kw):
    """A shot where Milo has no scarf (only when he is in the picture)."""
    acts = kw.get("actors") or STAGES[place]
    bare = any(a[0] == "milo" for a in acts) and "milo" not in kw.get("hide", ())
    return S(place, cam, say, fx=([BARE] if bare else []) + list(fx), **kw)

# Milo on Sandy's back (feet on her back, a little behind the middle), and the lids he keeps shut against the sand
def BACK(sx, sy=935, s=.56, ms=.4): return ("milo", "milo", round(sx - 40 * s), round(sy - 470 * s + 2), ms)
def RIDE(sx, sy=935, s=.56): return [("sandy", "calf", sx, sy, s), BACK(sx, sy, s)]
def LIDS(x, y, s, hidden=False): return prop("ey", A.shut_eyes, x, y, s, hidden)
CLOSE_NOSE = lambda at, who="sandy": ("to", at, "#{p}%s-nose" % who, {"scaleY": .12, "scaleX": 1.2, "transformOrigin": "50% 50%", "duration": .25}, "Sandy closes her nose")
NOSE_SHUT = lambda who="sandy": ("fromto", 0, "#{p}%s-nose" % who, {"scaleY": .12, "scaleX": 1.2, "transformOrigin": "50% 50%"}, {"scaleY": .12, "duration": .01}, "")
PUFF = lambda name, x, y, s, dx=420, d=5.0: ([prop(name, art.sand_puffs, x, y, s)], [("fromto", 0, "#{p}%s_w" % name, {"x": x - dx / 2}, {"x": x + dx / 2, "duration": d, "ease": "none"}, "")])
FLY_SCARF = lambda name, x, y, s, dx, dy, d, at=0.1: ("to", at, "#{p}%s_w" % name, {"x": x + dx, "y": y + dy, "rotation": 25, "duration": d, "ease": "power1.inOut"}, "the scarf flies away")
FLUTTER = lambda name, at=0.05, n=21: ("to", at, "#{p}%s-endL,#{p}%s-endR" % (name, name), {"rotation": 10, "transformOrigin": "50% 50%", "duration": .18, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "")

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. Nobody sings: the rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_BLINK = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~ ~", "notes": "G4:1 G4:1 E4:1 E4:1 D4:1 G4:1 B4:1", "rest": 1},     # blink, blink (C bar), close my nose (G bar)
                                  {"text": "~ ~ ~ ~ ~ ~ ~", "notes": "A4:1 A4:1 F4:1 F4:1 E4:1 G4:1 C4:1", "rest": 1}])    # step, step (F bar), here Sandy goes (C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "D4:1 B4:1 G4:1 A4:.5,B4:.5 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune

CNT_BUSH = .64                                    # seconds from "One" to the last number, read from the timing file
MCL = lambda place, dx=0, dy=-70, w=820, stage=None: C(place, "milo", "body", w, dx, dy, stage=stage)     # Milo asks a question: low in the frame, under the signs
GND_W = [("sandy", "calf", 1060, 935, .56), ("milo", "milo", 560, 935, .72)]            # Milo on the ground beside Sandy in the wind
BUSH_X = 1560
BUSH = lambda hidden=False, with_scarf=True: prop("bs", A.bush_scarf if with_scarf else (lambda p: art._thorn(p, 0, 0, 1.4)), BUSH_X, 905, .9, hidden)
MOUTH = P("dune_eve", "sandy", "head", 60, 75, stage=RIDE(1130))                                 # the scarf held in Sandy's lips
OASIS_SCARF = P("oasis", "milo", "feet", 0, -82)          # a flying Milo is drawn about 40 px above his feet point (seen in stills)                                         # where Milo's scarf sits on him at the oasis

SHOTS = [
    # ------------------------------------------------------------ HOOK: the wind takes the scarf in the first 5 seconds
    NS("oasis", C("oasis", "milo", "body", 820, 120, -40), "Whoosh! Oh! The wind took my red scarf!", beat="hook", tag="hook: the scarf flies off", hide=["mama", "sandy"],
       props=[prop("sf", A.scarf, OASIS_SCARF[0], OASIS_SCARF[1], .45), prop("wl", A.wind_lines, 640, 360, .7, True)],
       fx=[FLY_SCARF("sf", *OASIS_SCARF, .45, 520, -330, 1.6, "w:Whoosh!"), FLUTTER("sf"), ("show", "w:Whoosh!", "wl"), ("face", "w:Oh!", "milo", "wow"),
           ("fromto", "w:Whoosh!", "#{p}wl_w", {"x": 440}, {"x": 900, "duration": 2.4, "ease": "none"}, "")],
       words=[("w:Whoosh!", "WHOOSH!", .26, .22, 1.0, "sun")]),
    NS("oasis", WIDE, "Hello, I'm Milo! I'm at the oasis with my friend Sandy, the baby camel, and her mama.", tag="oasis wide: Milo, Sandy, Mama", cam2=(980, 560, 1800),
       props=[prop("sf", A.scarf, 1500, 160, .4)], fx=[FLY_SCARF("sf", 1500, 160, .4, 700, -60, 4.5, 0.05), FLUTTER("sf"), ("hop", "w:Hello,", "milo"), ("hop", "w:Sandy,", "sandy"), ("nod", "w:mama.", "mama")],
       words=[("w:Sandy,", "SANDY", .3, .45, .85, "pill")]),
    NS("oasis", C("oasis", "sandy", "head", 820, -60, 30), "Look, Milo! Your scarf is flying over the dunes!", who="sandy", tag="Sandy: over the dunes", hide=["mama", "milo"],
       fx=[("face", 0.02, "sandy", "wow"), ("lookat", "w:Look,", "sandy", -14)], words=[("w:dunes!", "OVER THE DUNES", .7, .2, .7, "pill")]),
    NS("oasis", C("oasis", "milo", "body", 760, 0, -10), "My scarf! I wear it every day. It keeps my neck cozy.", tag="Milo: my scarf", hide=["mama", "sandy"],
       fx=[("face", 0.02, "milo", "sad"), ("hop", "w:cozy.", "milo")], words=[("w:cozy.", "COZY", .74, .24, .9, "pill")]),
    # ------------------------------------------------------------ GOAL
    NS("oasis", C("oasis", "sandy", "all", 980, 60, -60), "Let's go and bring it home, Milo! I know the way over the dunes.", who="sandy", beat="goal", tag="goal: bring it home", hide=["mama", "milo"],
       fx=[("face", 0.02, "sandy", "happy"), ("hop", "w:home,", "sandy"), ("nod", "w:way", "sandy")], words=[("w:home,", "BRING IT HOME!", .3, .2, .75, "sun")]),
    NS("oasis", C("oasis", "mama", "head", 900, 60, 60), "Mama camel nods. Stay together, and be home by bedtime.", beat="goal", tag="Mama nods", hide=["sandy", "milo"],
       fx=[("nod", "w:nods.", "mama"), ("nod", "w:together,", "mama")], words=[("w:together,", "STAY TOGETHER", .3, .2, .7, "pill")]),
    NS("oasis", MCL("oasis", 40), "What color is Milo's scarf? Red, or blue?", q=True, beat="goal", tag="question: red or blue", pause=3.2, hide=["mama", "sandy"],
       fx=[("signs", "w:Red,", ["RED", "BLUE"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ off over the first dune
    NS("dunes", WIDE, "Sandy and Milo set off over the first dune. Far ahead, the scarf flutters like a little red bird.", trans="iris", beat="goal", tag="over the first dune", cam2=(980, 560, 1800),
       move={"sandy": (300, 935, .56), "milo": (-200, 560, .72)}, props=[prop("sf", A.scarf, 1420, 200, .3)],
       fx=[("walk", 0.1, "sandy", 420, 4.0), ("fly", 0.1, "milo", 380, 520, 4.0), FLUTTER("sf", 0.05, 31), ("to", "w:flutters", "#{p}sf_w", {"x": 1800, "y": 150, "duration": 3.0, "ease": "sine.inOut"}, "the scarf flutters on")],
       words=[("w:dune.", "OFF WE GO!", .3, .2, .85, "sun"), ("w:flutters", "FLUTTER!", .74, .3, .8, "pill")]),
    NS("dunes", C("dunes", "sandy", "head", 800, -40, 30), "Up and down, up and down. I love walking on the dunes!", who="sandy", tag="Sandy: up and down", hide=["milo"],
       fx=[("face", 0.02, "sandy", "happy"), ("nod", "w:Up", "sandy"), ("nod", "w:down.:2", "sandy"), ("hop", "w:love", "sandy")], words=[("w:Up", "UP AND DOWN", .26, .2, .75, "sun")]),
    NS("dunes", MCL("dunes", 40), "Where is the scarf now? Up in the sky, or under the sand?", q=True, beat="goal", tag="question: sky or sand", pause=3.2, hide=["sandy"],
       props=[prop("sf", A.scarf, 1500, 220, .3)], fx=[FLUTTER("sf", 0.05, 41), ("signs", "w:sky,", ["SKY", "SAND"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 1: the wind is too strong for a little bird
    NS("wind", WIDE, "Out on the dunes, the wind blows, and blows. Whoosh!", trans="iris", beat="obstacle1", tag="windy dunes wide", cam2=(980, 560, 1800),
       props=PUFF("pf", 960, 480, 1.0)[0] + [prop("sf", A.scarf, 1700, 220, .3)],
       fx=PUFF("pf", 960, 480, 1.0)[1] + [("fromto", 0, "#{p}gust", {"x": -260}, {"x": 320, "duration": 4.0, "ease": "none"}, ""), FLY_SCARF("sf", 1700, 220, .3, 400, -40, 3.5, 0.3), FLUTTER("sf")],
       words=[("w:Whoosh!", "WHOOSH!", .5, .2, 1.0, "sun")]),
    NS("wind", C("wind", "milo", "body", 860, 60, -20), "I'll fly after my scarf! Flap, flap!", tag="Milo: I'll fly", hide=["sandy"],
       fx=[("face", 0.02, "milo", "happy"), ("fly", "w:Flap,", "milo", 600, 500, 1.0)], words=[("w:Flap,", "FLAP, FLAP!", .24, .22, .85, "sun")]),
    NS("wind", (900, 620, 1500), "But the wind is too strong. It pushes Milo back, and he floats down, soft as a feather, next to Sandy.", beat="obstacle1", tag="the wind pushes Milo back",
       props=PUFF("pf", 900, 500, .8)[0], fx=PUFF("pf", 900, 500, .8)[1] + [("fly", "w:pushes", "milo", 300, 470, 1.0), ("fly", "w:floats", "milo", 560, 935, 2.4), ("face", "w:strong.", "milo", "wow")],
       words=[("w:strong.", "TOO WINDY!", .28, .2, .8, "pill"), ("w:feather,", "SOFT LANDING", .7, .2, .65, "sun")]),
    NS("wind", C("wind", "milo", "body", 700, 0, -20, stage=GND_W), "Phew! The wind is too strong for a little bird. I'll walk with you, Sandy.", tag="Milo: I'll walk", actors=GND_W, fly=[], hide=["sandy"],
       fx=[("face", 0.02, "milo", "happy"), ("hop", "w:walk", "milo")], words=[("w:walk", "WALK!", .74, .24, .9, "sun")]),
    NS("wind", MCL("wind", 40, stage=GND_W), "Is the wind strong, or gentle?", q=True, beat="obstacle1", tag="question: strong or gentle", pause=3.2, actors=GND_W, fly=[], hide=["sandy"],
       props=PUFF("pf", 600, 600, .6)[0], fx=PUFF("pf", 600, 600, .6)[1] + [("signs", "w:strong,", ["STRONG", "GENTLE"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ OBSTACLE 2: sand in the eyes (Sandy's long eyelashes, fact 1)
    NS("wind", (820, 700, 1300), "They walk on. But the sand blows into their faces.", beat="obstacle2", tag="walking into the sand", actors=[("sandy", "calf", 700, 935, .56), ("milo", "milo", 360, 935, .72)], fly=[],
       props=PUFF("pf", 900, 600, .8)[0], fx=PUFF("pf", 900, 600, .8)[1] + [("walk", 0.1, "sandy", 240, 3.0), ("to", 0.1, "#{p}milo_w", {"x": "+=240", "duration": 3.0, "ease": "none"}, "Milo hops along"),
                                                                     ("hop", 0.4, "milo", 3)], words=[("w:sand", "SAND!", .3, .22, .9, "sun")]),
    NS("wind", C("wind", "milo", "body", 700, 0, -20, stage=GND_W), "Oh! The sand tickles my eyes. I have to shut them tight!", beat="obstacle2", tag="Milo shuts his eyes", actors=GND_W, fly=[], hide=["sandy"],
       props=[LIDS(*P("wind", "milo", "feet", stage=GND_W), .72, True)] + PUFF("pf", 560, 620, .6)[0],
       fx=PUFF("pf", 560, 620, .6)[1] + [("face", "w:Oh!", "milo", "wow"), ("show", "w:shut", "ey", None, False)], words=[("w:tickles", "TICKLY!", .74, .24, .9, "pill")]),
    NS("wind", C("wind", "sandy", "head", 760, -40, 30, stage=GND_W), "Not me! The sand stays out of my eyes. Blink, blink!", who="sandy", beat="obstacle2", tag="Sandy: blink blink", actors=GND_W, hide=["milo"],
       props=PUFF("pf", 1300, 380, .6)[0], fx=PUFF("pf", 1300, 380, .6)[1] + [("face", 0.02, "sandy", "happy"), ("blinkslow", "w:Blink,", "sandy-eye", 2)], words=[("w:Blink,", "BLINK!", .26, .2, .9, "sun")]),
    S("paper", (960, 520, 1500), "Camels have two rows of long eyelashes. They help keep sand out of their eyes!", beat="fact", tag="fact: two rows of eyelashes",
      props=[prop("eye", art.big_eye, 960, 600, 1.15), prop("pf", art.sand_puffs, 500, 300, .5, True)],
      fx=[("to", "w:two", ".{p}eye-row0", {"stroke": "#e63946", "duration": .2, "yoyo": True, "repeat": 3}, "the first row lights up"),
          ("to", "w:rows", ".{p}eye-row1", {"stroke": "#e63946", "duration": .2, "yoyo": True, "repeat": 3}, "the second row lights up"),
          ("show", "w:sand", "pf"), ("fromto", "w:sand", "#{p}pf_w", {"x": 300}, {"x": 600, "duration": 2.4, "ease": "none"}, ""), ("blinkslow", "w:eyes!", "eye", 2)],
      words=[("w:two", "2 ROWS", .17, .3, .8, "sun"), ("w:sand", "NO SAND IN!", .8, .15, .8, "pill")]),
    NS("wind", MCL("wind", 40, stage=GND_W), "How many rows of eyelashes does a camel have? One, or two?", q=True, beat="obstacle2", tag="question: one or two rows", pause=3.2, actors=GND_W, fly=[], hide=["sandy"],
       props=[LIDS(*P("wind", "milo", "feet", stage=GND_W), .72)], fx=[("signs", "w:One,", ["ONE", "TWO"], 1, "wait:1.8")]),
    NS("wind", C("wind", "sandy", "head", 700, -40, 30, stage=GND_W), "Can you blink like Sandy? Blink, blink, blink!", q=True, beat="obstacle2", tag="blink along", actors=GND_W, hide=["milo"],
       fx=[("face", 0.02, "sandy", "happy"), ("blinkslow", "w:Blink,", "sandy-eye", 3)], words=[("w:Blink,", "BLINK!", .26, .2, .9, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 3: sand on the beak (Sandy closes her nose, fact 2)
    NS("trail", WIDE, "On the rocky trail, the wind blows the sand up, up, onto everyone's noses.", trans="iris", beat="obstacle3", tag="the rocky trail", cam2=(980, 560, 1800),
       props=[prop("rk", A.rock, 330, 935, .9)] + PUFF("pf", 960, 520, .9)[0], fx=PUFF("pf", 960, 520, .9)[1] + [("hop", "w:up,", "milo")], words=[("w:noses.", "NOSES!", .5, .2, .9, "sun")]),
    NS("trail", C("trail", "milo", "body", 700, 0, -20), "Oh, sand on my beak! Tickly, tickly!", beat="obstacle3", tag="Milo: sand on my beak", hide=["sandy"],
       props=[prop("rk", A.rock, 330, 935, .9)] + PUFF("pf", 700, 640, .5)[0], fx=PUFF("pf", 700, 640, .5)[1] + [("face", 0.02, "milo", "wow"), ("to", "w:Tickly,", "#{p}milo", {"rotation": 6, "svgOrigin": "0 -150", "duration": .1, "yoyo": True, "repeat": 7}, "Milo wiggles")],
       words=[("w:beak!", "TICKLY!", .74, .24, .9, "pill")]),
    NS("trail", C("trail", "sandy", "head", 700, -40, 30), "Watch my nose, Milo! I can close it. Closed! No sand gets in.", who="sandy", beat="obstacle3", tag="Sandy closes her nose", hide=["milo"],
       fx=[("face", 0.02, "sandy", "happy"), CLOSE_NOSE("w:Closed!"), ("nod", "e:in.", "sandy")], words=[("w:Closed!", "CLOSED!", .26, .2, .9, "sun")]),
    S("paper_pink", (960, 560, 1500), "A camel can close its nostrils, to keep sand out of its nose. Open. Closed!", beat="fact", tag="fact: a camel can close its nose",
      props=[prop("nose", art.big_nose, 960, 620, 1.05), prop("pf", art.sand_puffs, 560, 320, .5, True)],
      fx=[("to", "w:close", "#{p}nose-nl,#{p}nose-nr", {"scaleY": .08, "transformOrigin": "50% 50%", "duration": .3}, "the nostrils shut"),
          ("to", "w:keep", "#{p}nose-nl,#{p}nose-nr", {"scaleY": 1, "duration": .3}, "the nostrils open"), ("show", "w:sand", "pf"),
          ("fromto", "w:sand", "#{p}pf_w", {"x": 360}, {"x": 700, "duration": 2.0, "ease": "none"}, ""),
          ("to", "w:Closed!", "#{p}nose-nl,#{p}nose-nr", {"scaleY": .08, "duration": .2}, "shut")],
      words=[("w:Open.", "OPEN", .26, .2, 1.0, ""), ("w:Closed!", "CLOSED", .8, .16, 1.0, "sun")]),
    NS("trail", MCL("trail", 40), "Can a camel close its nose? Yes, or no?", q=True, beat="obstacle3", tag="question: yes or no nose", pause=3.2, hide=["sandy"],
       props=[prop("rk", A.rock, 330, 935, .9)], fx=[("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ LOW MOMENT: beside the rock, the scarf is far away (gentle: nobody cries)
    NS("trail", (800, 640, 1500), "Milo and Sandy rest beside a big rock. The wind blows, and the scarf is far, far away.", beat="low", tag="resting by the rock",
       actors=[("sandy", "calf", 1060, 930, .54), ("milo", "milo", 720, 930, .7)], props=[prop("rk", A.rock, 330, 935, .9), prop("sf", A.scarf, 1400, 260, .2)],
       fx=[("face", "w:rest", "milo", "sad"), ("to", "w:rest", "#{p}sandy", {"y": 10, "duration": .5}, "Sandy settles"), FLUTTER("sf"),
           ("to", "w:far,", "#{p}sf_w", {"x": 1700, "y": 200, "duration": 2.4, "ease": "sine.inOut"}, "the scarf flutters far away")],
       words=[("w:far,", "SO FAR...", .3, .2, .9, "pill")]),
    NS("trail", C("trail", "milo", "body", 700, 0, -20), "My eyes are shut tight. I can't fly in the wind, and I can't walk in the sand.", beat="low", tag="Milo: I can't", hide=["sandy"],
       props=[prop("rk", A.rock, 330, 935, .9), LIDS(*P("trail", "milo", "feet"), .7)], fx=[("face", 0.02, "milo", "sad"), ("face", "w:fly", "milo", "sad")],
       words=[("w:fly", "NO FLYING", .22, .2, .65, "pill"), ("w:walk", "NO WALKING", .22, .32, .62, "pill")]),
    NS("trail", C("trail", "milo", "body", 640, 0, -20), "Maybe my scarf is gone.", beat="low", tag="Milo: maybe it's gone", hide=["sandy"],
       props=[LIDS(*P("trail", "milo", "feet"), .7)], fx=[("face", 0.02, "milo", "sad")]),
    NS("trail", C("trail", "sandy", "head", 760, -40, 40), "Don't worry, Milo. We are together. Let me think.", who="sandy", beat="low", tag="Sandy: let me think", hide=["milo"],
       fx=[("face", 0.02, "sandy", "sad"), ("lookat", "w:think.", "sandy", -12)], words=[("w:think.", "HMM...", .26, .2, 1.0, "pill")]),
    NS("trail", MCL("trail", 40), "Who can walk in the windy sand? Milo, or Sandy?", q=True, beat="low", tag="question: Milo or Sandy", pause=3.2, hide=["sandy"],
       props=[LIDS(*P("trail", "milo", "feet"), .7)], fx=[("signs", "w:Milo,", ["MILO", "SANDY"], 1, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: Sandy works it out herself, and walks in the wind for both of them
    NS("trail", C("trail", "sandy", "all", 900, 60, -60), "I know! My eyelashes keep the sand out. My nose can close. I can walk in the wind!", who="sandy", beat="solution", tag="Sandy: I know!", hide=["milo"],
       fx=[("face", 0.02, "sandy", "happy"), ("hop", "w:know!", "sandy"), ("blinkslow", "w:eyelashes", "sandy-eye", 1), CLOSE_NOSE("w:nose"), ("to", "w:walk", "#{p}sandy-nose", {"scaleY": 1, "scaleX": 1, "duration": .2}, "")],
       words=[("w:know!", "I KNOW!", .3, .2, .9, "sun")]),
    NS("trail", (900, 640, 1400), "Hop on my back, Milo! Keep your eyes shut. I will walk for both of us.", who="sandy", beat="solution", tag="Milo hops on Sandy's back",
       actors=[("sandy", "calf", 1060, 930, .54), ("milo", "milo", 720, 930, .7)], fly=[],
       fx=[("to", "w:Hop", "#{p}milo_w", {"x": BACK(1060, 930, .54)[2], "y": BACK(1060, 930, .54)[3], "duration": .8, "ease": "power2.inOut"}, "Milo hops onto her back"),
           ("to", "w:Hop", "#{p}milo", {"scale": .4 / .7, "svgOrigin": "0 0", "duration": .8}, ""), ("face", "w:both", "sandy", "happy")],
       words=[("w:both", "BOTH OF US!", .26, .2, .8, "sun")]),
    NS("wind", (900, 660, 1400), "Milo snuggles in. Sandy closes her nose, and off they go!", beat="solution", tag="off they go", trans="iris", actors=RIDE(700),
       props=[LIDS(BACK(700)[2], BACK(700)[3], .4)] + PUFF("pf", 1100, 520, .8)[0],
       fx=PUFF("pf", 1100, 520, .8)[1] + [CLOSE_NOSE("w:closes"), ("walk", "w:off", "sandy", 260, 2.4), ("to", "w:off", "#{p}milo_w,#{p}ey_w", {"x": "+=260", "duration": 2.4, "ease": "none"}, "")],
       words=[("w:off", "OFF WE GO!", .3, .2, .85, "sun")]),
    NS("wind", (1000, 640, 1500), "Step, step, step. Sandy's wide feet do not sink in the soft sand.", beat="solution", tag="step step step", actors=RIDE(620),
       props=[LIDS(BACK(620)[2], BACK(620)[3], .4)] + PUFF("pf", 1100, 460, .8)[0],
       fx=PUFF("pf", 1100, 460, .8)[1] + [NOSE_SHUT(), ("walk", 0.1, "sandy", 520, 5.0), ("to", 0.1, "#{p}milo_w,#{p}ey_w", {"x": "+=520", "duration": 5.0, "ease": "none"}, "")],
       words=[("w:Step,", "STEP, STEP!", .24, .2, .85, "sun"), ("w:sink", "NO SINKING!", .76, .2, .75, "pill")]),
    S("paper_blue", (960, 540, 1500), "A camel's big, wide feet spread out when they step down. That helps camels walk on sand!", beat="fact", tag="fact: wide feet spread out",
      props=[prop("foot", lambda p: art.footprint(p), 960, 620, 3.0)],
      fx=[("fromto", "w:spread", "#{p}foot", {"scaleX": .62, "transformOrigin": "50% 50%"}, {"scaleX": 1.12, "duration": .5, "ease": "back.out(3)"}, "the foot spreads"),
          ("to", "w:helps", "#{p}foot", {"scaleX": .7, "duration": .3, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "step, step")],
      words=[("w:wide", "WIDE FEET", .5, .16, 1.1, "sun"), ("w:spread", "SPREAD!", .82, .28, .9, "pill")]),
    # ------------------------------------------------------------ the big sandy hill: the scarf on a thorny bush
    NS("dune_eve", WIDE, "Up the big sandy hill they go. And look, on a thorny bush! The red scarf!", trans="iris", beat="solution", tag="the hill: the scarf on a bush", cam2=(1000, 560, 1800),
       actors=RIDE(500), props=[LIDS(BACK(500)[2], BACK(500)[3], .4), BUSH()],
       fx=[NOSE_SHUT(), ("walk", 0.1, "sandy", 300, 3.0), ("to", 0.1, "#{p}milo_w,#{p}ey_w", {"x": "+=300", "duration": 3.0, "ease": "none"}, ""), ("to", "w:bush!", "#{p}bs-s", {"rotation": 6, "transformOrigin": "50% 50%", "duration": .2, "yoyo": True, "repeat": 5}, "the scarf flutters on the bush")],
       words=[("w:scarf!", "THE SCARF!", .78, .2, .85, "sun")]),
    NS("dune_eve", C("dune_eve", "sandy", "head", 1100, 0, 120, stage=RIDE(1130)), "Sandy picks up the scarf, gently, with her soft lips. Got it!", beat="solution", tag="Sandy picks up the scarf", actors=RIDE(1130),
       props=[LIDS(BACK(1130)[2], BACK(1130)[3], .4), BUSH(with_scarf=False), prop("sf", A.scarf, BUSH_X + 10, 905 - 236 * .9, .4)],
       fx=[("lookat", "w:picks", "sandy", 24), ("lookat", "w:lips.", "sandy", 0), ("to", "w:lips.", "#{p}sf_w", {"x": MOUTH[0], "y": MOUTH[1], "duration": .5}, "the scarf comes away"),
           ("face", "w:Got", "sandy", "happy")],
       words=[("w:Got", "GOT IT!", .75, .18, 1.0, "sun")]),
    NS("dune_eve", (1000, 660, 1300), "How many thorny bushes are on the hill? Count with me! One. Two. Three!", q=True, beat="solution", tag="question: count the bushes", actors=RIDE(1130),
       props=[LIDS(BACK(1130)[2], BACK(1130)[3], .4), prop("b1", lambda p: art._thorn(p, 0, 0, 1.4), 480, 905, .9), prop("b2", lambda p: art._thorn(p, 0, 0, 1.4), 760, 925, .7), BUSH(with_scarf=False), prop("sf", A.scarf, *MOUTH, .4)],
       fx=[("count", "w:One.", 3, CNT_BUSH, {"x": 420, "y": 300}), ("to", "w:One.", "#{p}b1_w", {"scale": 1.1, "duration": .15, "yoyo": True, "repeat": 1}, ""),
           ("to", "w:Two.", "#{p}b2_w", {"scale": 1.1, "duration": .15, "yoyo": True, "repeat": 1}, ""), ("to", "w:Three!", "#{p}bs_w", {"scale": 1.0, "duration": .15, "yoyo": True, "repeat": 1}, "")]),
    NS("dune_eve", C("dune_eve", "milo", "body", 520, -10, -10, stage=RIDE(1130)), "The wind is calm now. Milo opens his eyes. My scarf! Thank you, Sandy!", beat="solution", tag="Milo opens his eyes", actors=RIDE(1130),
       props=[LIDS(BACK(1130)[2], BACK(1130)[3], .4)], fx=[("hide", "w:opens", "ey"), ("face", "w:scarf!", "milo", "wow"), ("face", "w:Thank", "milo", "happy"), ("hop", "w:Sandy!", "milo")],
       words=[("w:calm", "NO MORE WIND", .26, .2, .7, "pill")]),
    S("dune_eve", C("dune_eve", "sandy", "all", 1000, 40, -120, stage=RIDE(1130)), "Sandy puts the scarf around Milo's neck. Nice and snug.", beat="solution", tag="the scarf back on Milo", actors=RIDE(1130),
      fx=[("fromto", 0, NOSCARF, {"opacity": 0}, {"opacity": 0, "duration": .01}, ""), ("lookat", "w:puts", "sandy", -20), ("to", "w:neck.", NOSCARF, {"opacity": 1, "duration": .4}, "the scarf is on Milo again"),
          ("lookat", "w:snug.", "sandy", 0), ("hop", "w:snug.", "milo")], words=[("w:snug.", "SNUG!", .78, .2, 1.0, "sun")]),
    S("dune_eve", MCL("dune_eve", 0, -40, 700, stage=RIDE(1130)), "What helped Sandy walk in the windy sand? Long eyelashes, or a big hat?", q=True, beat="solution", tag="question: eyelashes or hat", pause=3.2, actors=RIDE(1130),
      fx=[("signs", "w:Long", ["EYELASHES", "A HAT"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ SONG MOMENT: the rhyme SAID by Sandy, then the tune on instruments while they walk home down the hill
    S("dune_eve", C("dune_eve", "sandy", "all", 1100, 0, -80, stage=RIDE(1130)), "Blink, blink, close my nose. Step, step, here Sandy goes!", who="sandy", beat="solution", tag="the blink rhyme", actors=RIDE(1130),
      fx=[("face", 0.02, "sandy", "happy"), ("blinkslow", "w:Blink,", "sandy-eye", 2), CLOSE_NOSE("w:close"), ("to", "w:Step,", "#{p}sandy-nose", {"scaleY": 1, "scaleX": 1, "duration": .2}, ""), ("hop", "w:goes!", "milo")],
      words=[("w:Blink,", "BLINK, BLINK!", .26, .2, .75, "sun"), ("w:Step,", "STEP, STEP!", .74, .2, .75, "pill")]),
    S("dune_eve", (760, 620, 1500), who="", sing=SING_BLINK, beat="song", tag="song: blink, step", actors=RIDE(420), cam2=(1240, 620, 1500),
      fx=[("walk", TB(0), "sandy", 800, 9.6), ("to", TB(0), "#{p}milo_w", {"x": "+=800", "duration": 9.6, "ease": "none"}, "they walk home"), ("hop", TB(4), "milo"), ("hop", TB(12), "milo"),
          ("word", TB(0), "BLINK, BLINK!", {"x": 760, "y": 300, "size": 80, "cls": "sun", "hold": 4.4})],
      words=[(TB(8), "STEP, STEP!", .8, .14, .8, "pill")]),
    # ------------------------------------------------------------ WARM ENDING: home at night, Mama, thank-yous
    S("night", WIDE, "Back home, the stars come out. And Mama is waiting by the lamp.", trans="iris", beat="ending", tag="home at night", cam2=(980, 560, 1800),
      move={"sandy": (-300, 935, .54), "milo": (2160, 760, .7, True)}, fx=[("walk", 0.1, "sandy", 700, 3.0), ("fly", 0.1, "milo", 1720, 760, 3.0), ("nod", "w:Mama", "mama")],
      words=[("w:stars", "GOOD NIGHT, STARS", .45, .16, .7, "sun")]),
    S("night", C("night", "sandy", "all", 940, 40, -60), "Mama! I walked in the wind, and we found Milo's scarf!", who="sandy", beat="ending", tag="Sandy tells Mama", hide=["mama", "milo"],
      fx=[("face", 0.02, "sandy", "happy"), ("hop", "w:Mama!", "sandy"), ("nod", "w:scarf!", "sandy")], words=[("w:scarf!", "WE FOUND IT!", .3, .2, .8, "sun")]),
    S("night", (900, 560, 1500), "Mama camel nuzzles Sandy. She is so proud of her.", beat="ending", tag="Mama nuzzles Sandy", hide=["milo"], move={"sandy": (520, 935, .54)},
      props=[prop("h1", lambda p: art2.heart(p), 640, 360, .7, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 720, 330, .5, True)],
      fx=[("lookat", "w:nuzzles", "mama", 20), ("lookat", "w:nuzzles", "sandy", -8), ("show", "w:nuzzles", "h1"), ("show", "w:proud", "h2"),
          ("to", "w:proud", "#{p}h1_w,#{p}h2_w", {"y": "-=60", "duration": 1.6, "ease": "sine.out"}, "")],
      words=[("w:proud", "SO PROUD!", .3, .2, .8, "sun")]),
    S("night", C("night", "milo", "body", 760, 0, -10), "Thank you, Sandy. You are a great friend on a windy day!", beat="ending", tag="Milo: thank you", hide=["mama", "sandy"],
      fx=[("face", 0.02, "milo", "happy"), ("hop", "w:friend", "milo")], words=[("w:friend", "GREAT FRIEND!", .28, .22, .8, "sun")]),
    S("night", C("night", "sandy", "head", 800, -40, 30), "And you are a great friend to ride with, Milo!", who="sandy", beat="ending", tag="Sandy: great friend", hide=["mama", "milo"],
      fx=[("face", 0.02, "sandy", "happy"), ("nod", "w:ride", "sandy")]),
    S("night", (1000, 600, 1760), "Everyone can help in their own way. Sandy's eyelashes, her nose and her feet were just right for a windy day.", beat="ending", tag="the lesson",
      cam2=(1040, 600, 1700), fx=[("hop", "w:help", "milo"), ("blinkslow", "w:eyelashes,", "sandy-eye", 2), CLOSE_NOSE("w:nose"), ("to", "w:feet", "#{p}sandy-nose", {"scaleY": 1, "scaleX": 1, "duration": .2}, ""),
                                  ("hop", "w:feet", "sandy"), ("nod", "w:right", "mama"), ("hop", "w:windy", "milo")],
      words=[("w:own", "YOUR OWN WAY", .19, .2, .5, "sun")]),
    S("night", C("night", "milo", "body", 900, 40, 0), "Do you remember? What can a camel close, to keep the sand out? Its nose, or its ears?", q=True, beat="ending", tag="question: nose or ears", pause=3.2,
      hide=["mama", "sandy"], cam2=C("night", "milo", "body", 830, 40, -60), fx=[("hop", "w:remember?", "milo"), ("signs", "w:nose,", ["NOSE", "EARS"], 0, "wait:1.8")]),
    S("night", C("night", "milo", "body", 1000, 140, 0), "Where was Milo's scarf? On a bush, or in a tree?", q=True, beat="ending", tag="question: bush or tree", pause=3.2,
      hide=["mama", "sandy"], cam2=C("night", "milo", "body", 940, 140, -20), fx=[("hop", "w:scarf?", "milo"), ("signs", "w:bush,", ["BUSH", "TREE"], 0, "wait:1.8")]),
    S("night", (1560, 720, 1120), "And do a camel's wide feet sink in the sand? Yes, or no?", q=True, beat="ending", tag="question: sink yes or no", pause=3.2,
      hide=["mama", "sandy"], move={"milo": (1720, 860, .7)}, cam2=(1580, 720, 1060), fx=[("hop", "w:feet", "milo"), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    S("night", (960, 540, 1920), "Blink, blink, close my nose. Step, step, here Sandy goes!", beat="ending", tag="the closing rhyme", cam2=(980, 560, 1880),
      fx=[("hop", "w:Blink,", "milo"), ("blinkslow", "w:Blink,", "sandy-eye", 2), CLOSE_NOSE("w:close"), ("hop", "w:Step,", "sandy"), ("nod", "w:goes!", "mama")],
      words=[("w:Blink,", "BLINK, BLINK!", .5, .15, .7, "sun")]),
    S("night", WIDE, who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(980, 560, 1880),
      fx=[("hop", 1.0, "sandy"), ("nod", 3.2, "mama"), ("hop", 2.2, "milo")], words=[(TB(3), "HOORAY!", .5, .2, 1.05, "sun")]),
    S("night", C("night", "milo", "body", 900, 0, 0), "Next time: the long walk to the oasis! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure", hide=["mama", "sandy"],
      fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .24, .2, .72, "sun"), ("w:See", "SEE YOU SOON!", .24, .33, .62, "pill")]),
]

# thumbnail (thumb.py): the example in the picture (Sandy on the windy dunes with the red scarf she found, Milo on her back), 3 words at most, none of the title's words, no watermark
THUMBS = {
    "za_ep07": {"place": "wind", "cam": (1080, 600, 1300),
                "actors": [("calf", 1000, 935, .62, False, ''), ("milo", 950, 935 - round(470 * .62) + 2, .44, False, 'gsap.set("' + NOSCARF.replace("#{p}milo", "#P") + '",{opacity:0});')],
                "props": [(A.wind_lines, 520, 330, .8), (A.wind_lines, 1520, 420, .6), (art.sand_puffs, 1000, 500, .9),
                          (A.scarf, 1000 + round(379 * .62) + 95, 935 - round(690 * .62) + 35, .5)],
                "words": [("GOT IT!", 1420, 160, 180, "sun", -4)]},
}
