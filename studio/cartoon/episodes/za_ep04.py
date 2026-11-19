"""za_ep04 - Milo's Zoo Adventures: "Mango and the Wobbly Vine Bridge" (cartoon adventure, the 3D music-and-sync process: "beat").
Picnic day. Mango fills a basket with fruit, and the picnic spot is on the other side of a little stream. The only way over is a low,
wobbly vine bridge. Tumble is not sure about the wobble; Mango runs on too fast and the basket tips; Tumble tries alone and the wobble is
too much. Mango works it out herself: she holds the rope with her tail, holds Tumble's trunk with her hand, and they cross slowly, side by side.
Nobody is hurt, lost, crying or trapped: the bridge is low and short, the fruit only rolls on the grass, and Tumble steps back by himself.

FACTS, read at the source on Nov 18 2026, 7:40 PM ET (each page fetched by the session's page reader, which quoted these sentences):
 [NGK] National Geographic Kids, kids.nationalgeographic.com/animals/mammals/facts/spider-monkey
   "has a prehensile tail, which means it can grasp" ... "can be used like a fifth limb to grab trees."
   "Spider monkeys have long, thin arms with hooklike hands that allow them to swing through the trees."
   "They do not have opposable thumbs."
 [NG] National Geographic, nationalgeographic.com/animals/mammals/facts/spider-monkeys
   "The spider monkey's tail is prehensile, which means 'capable of grasping.'"   "acts as a fifth limb"
   "It can support a spider monkey's full body weight" "and allows them to hang onto branches, freeing their hands so they can climb, forage, and eat."
   "(They also have thumbs but those are extremely short.)"
 Said as animal facts in the film (three fact shots and two closing questions), each from a quote above: a spider monkey's tail can hold up
 her whole body, so both hands are free to pick fruit [NG]; the tail can grab and hold, like an extra hand [NGK, NG]; long arms and hook-like
 hands to swing through the trees [NGK].
 Read but NOT said: thumbs (the build plan asked for "no thumbs"; Nat Geo Kids says "do not have opposable thumbs", Nat Geo says they have
 "extremely short" thumbs: the two pages word it differently, so the film says nothing about thumbs, as zc_ep04 did).
 Not animal facts, said as what happens in THIS story: the stream, the vine bridge and its wobble, the picnic, Mango carrying the basket.
 An elephant does not cross vine bridges; this is a cartoon story bridge, and nothing is said about what elephants do.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_zc_ep04 as A4          # Mango hanging with fruit in her hands, her big hand with four long fingers, a branch (read only)
import art_za_ep04 as A
import kit
from kit import Kit, S, prop

EP = {"id": "za_ep04", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "tumble": {"voice": "am_puck", "speed": .85, "pitch": 5, "formant": 1.16, "gain": .66},
               "mango": {"voice": "af_bella", "speed": .95, "pitch": 2, "formant": 1.08, "gain": .95}, "mama": {"voice": "bf_emma", "speed": .8, "gain": .8}},
      "title": "Mango and the Wobbly Vine Bridge", "thumb_text": "HOLD ON!",
      "series": "Milo's Zoo Adventures",
      "description": ("It is picnic day! Mango the spider monkey fills a basket with fruit, but the picnic spot is on the other side of a little stream. "
                      "The only way over is a low vine bridge that goes wiggle, wobble. Baby elephant Tumble is not sure, Mango runs too fast, and the basket tips. "
                      "How will the friends get across together? A gentle animal adventure for ages 2-6 about slowing down and helping a friend, "
                      "with questions to answer, steps to count and a tune to clap along to.\n"
                      "Kids see how a spider monkey's tail can hold up her whole body, how it can grab like an extra hand, and how her long arms and hook-like hands swing through the trees.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNational Geographic Kids (spider monkey); National Geographic (spider monkeys)."),
      "tags": ["spider monkey", "monkey story for kids", "baby elephant", "animal stories for kids", "friendship story for kids", "kids adventure cartoon", "monkey tail",
               "picnic story for kids", "counting steps", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

STAGES = {
    "jungle": [("tumble", "tumble", 520, 930, .62), ("mango", "monkey", 1260, 934, .58), ("milo", "milo", 260, 470, .78, False, True)],
    "canopy": [("mango", "monkey_hang", 900, 446, .6), ("milo", "milo", 1460, 290, .7, False, True)],
    "bigtree": [("tumble", "tumble", 560, 930, .62), ("mango", "monkey", 1160, 934, .55), ("milo", "milo", 280, 470, .75, False, True)],
    "stream": [("tumble", "tumble", 200, 930, .6), ("mango", "monkey", 560, 934, .55), ("milo", "milo", 420, 440, .7, False, True)],
    "meadow": [("tumble", "tumble", 380, 950, .6), ("mango", "monkey", 1400, 954, .56), ("milo", "milo", 960, 420, .72, False, True)],
    "zoo_eve": [("mango", "monkey", 300, 940, .55), ("tumble", "tumble", 660, 940, .6), ("mama", "elephant", 1540, 932, .9, True), ("milo", "milo", 330, 420, .68, False, True)],
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
SWIDE = (900, 560, 2000)                 # the stream: both banks, the bridge and the picnic spot
TP = "392 -430"                          # the pivot of an elephant's trunk
def only(place, *keep, stage=None): return [a[0] for a in (stage or STAGES[place]) if a[0] not in keep]

BR = lambda: prop("br", A.bridge, 970, 930, 1.0)                          # the bridge deck (the posts and the rope are in the place)
BK_BACK = (-40, -318, .46)                                               # the basket on Tumble's back: offset from his feet at scale .6, and its size
def BK(x, y, s=.46, n=3, hidden=False): return prop("bk", lambda p: A.basket(p, n), x, y, s, hidden)
def BK_ON(tx, ty=930, n=3): return BK(tx + BK_BACK[0], ty + BK_BACK[1], BK_BACK[2], n)
def WOB(at, n=5, k=1.0, who=()):
    """The bridge wobbles (and whoever stands on it goes with it): n swings."""
    out = [("to", at, "#{p}br-deck", {"y": round(12 * k), "rotation": round(.9 * k, 2), "svgOrigin": "0 0", "duration": .16, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, "the bridge wobbles")]
    for w in who: out.append(("to", at, "#{p}" + w, {"y": round(20 * k), "duration": .16, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, ""))
    return out
def WALKB(at, who, dx, d, extra=()):      # a walk that takes the basket on the back along
    return [("walk", at, who, dx, d)] + [("to", at, "#{p}" + e + "_w", {"x": f"+={dx}", "duration": d, "ease": "none"}, "") for e in extra]
TAIL = lambda at, who="mango", n=5: ("to", at, "#{p}" + who + "-tail", {"rotation": 12, "svgOrigin": "40 -80", "duration": .25, "yoyo": True, "repeat": n, "ease": "sine.inOut"}, f"{who} swishes her tail")
ARM = lambda at, side, deg, who="mango": ("arm", at, who, side, deg)
FR = lambda name, x, y, s=.42, hidden=True: prop(name, A.fruit, x, y, s, hidden)
CROSS = [("tumble", "tumble", 640, 930, .6), ("mango", "monkey_grip", 1040, 934, .55)]          # on the bridge, side by side: Mango a step ahead, her tail round the rope

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. Nobody sings: the rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}       # the show loop's key and the music bed's tempo
SING_STEP = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~ ~", "notes": "C4:1 D4:1 E4:1 G4:1 G4:1 A4:1 B4:1", "rest": 1},      # step by step, up the scale (C bar, G bar)
                                 {"text": "~ ~ ~ ~ ~ ~ ~", "notes": "A4:1 A4:1 G4:1 F4:1 E4:1 D4:1 C4:1", "rest": 1}])     # and down again (F bar, C bar)
SING_END_A = dict(REFRAIN, chords="C G", lines=[{"text": "~ ~ ~ ~ ~", "notes": "C4:1 E4:1 G4:1 G4:.5,A4:.5 G4:.5,E4:1.5", "rest": 2}])
SING_END_B = dict(REFRAIN, chords="F C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "A4:1 A4:.5 A4:.5,G4:.5 F4:.5,D4:.5 C4:2.5", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune

MCL = lambda place, dx=0, dy=-70, w=820: C(place, "milo", "body", w, dx, dy)          # Milo asks a question: low in the frame, under the signs

SHOTS = [
    # ------------------------------------------------------------ HOOK: the picnic and the problem in the first 5 seconds
    S("jungle", C("jungle", "mango", "all", 900, -60, -90), "It's picnic day! But the picnic spot is on the other side of the stream.", who="mango", beat="hook", tag="hook: picnic, the stream",
      hide=["tumble", "milo"], props=[prop("tb", lambda p: art2.bubble_thought(p, A.bridge_pic(p + "i"), -1), 1500, 420, 1.0, True)],
      fx=[("hop", "w:picnic", "mango"), ("show", "w:other", "tb"), ("face", "w:But", "mango", "wow")], words=[("w:picnic", "PICNIC DAY!", .3, .14, .85, "sun")]),
    S("jungle", C("jungle", "milo", "body", 760), "I'm Milo! Can you help my friends get to the picnic?", tag="hook: Milo", hide=["tumble", "mango"], fx=[("hop", "w:help", "milo")]),
    S("jungle", WIDE, "This is Mango, the spider monkey. And this is Tumble, the baby elephant.", tag="jungle wide", cam2=(980, 560, 1800),
      fx=[TAIL("w:Mango,"), ("hop", "w:Tumble,", "tumble")], words=[("w:Mango,", "MANGO", .66, .38, .85, "pill"), ("w:Tumble,", "TUMBLE", .3, .3, .85, "pill")]),
    # ------------------------------------------------------------ GOAL
    S("jungle", C("jungle", "mango", "head", 800, -40, 30), "Let's fill a basket with fruit, and have a picnic together!", who="mango", beat="goal", tag="goal: a picnic together", hide=["tumble", "milo"],
      props=[BK(1060, 930, .5, 0, True)], fx=[("show", "w:basket", "bk"), ARM("w:fruit,", "r", -60), ("hop", "w:together!", "mango")], words=[("w:together!", "A PICNIC!", .72, .2, .8, "sun")]),
    S("jungle", C("jungle", "tumble", "head", 900, -60, 20), "A picnic with my friends! Yummy! Let's go!", who="tumble", beat="goal", tag="goal: Tumble", hide=["mango", "milo"],
      fx=[("face", 0.1, "tumble", "happy"), ("hop", "w:Yummy!", "tumble"), ("trunk", "w:Let's", "tumble", -60, .4)], words=[("w:Yummy!", "YUMMY!", .25, .19, .9, "sun")]),
    S("jungle", MCL("jungle", 30), "What do we need for a picnic? A basket, or a bed?", q=True, beat="goal", tag="question: basket or bed", pause=3.2, hide=["tumble", "mango"],
      fx=[("signs", "w:basket,", ["BASKET", "BED"], 0, "wait:2.0")]),
    # ------------------------------------------------------------ the fruit: Mango hangs by her tail (fact: the tail holds her whole body, her hands are free)
    S("bigtree", WIDE, "The best fruit grows high up in the big tree. Up goes Mango!", trans="iris", tag="the big tree", cam2=(1000, 560, 1800), props=[BK(380, 930, .5, 0)],
      fx=[("to", "w:Up", "#{p}mango_w", {"y": 300, "x": 1300, "duration": 1.2, "ease": "power1.in"}, "Mango climbs up"), ("hop", "w:fruit", "tumble")],
      words=[("w:high", "UP HIGH!", .62, .18, .9, "sun")]),
    S("canopy", (900, 520, 1500), "Mango wraps her tail round the branch. And she hangs upside down!", trans="iris", tag="Mango hangs", hide=["milo"],
      fx=[("fromto", "w:Mango", "#{p}mango-swing", {"rotation": 0}, {"rotation": 0, "duration": .1}, "Mango holds on"), ("to", "w:hangs", "#{p}mango-swing", {"rotation": 10, "svgOrigin": "0 0", "duration": .5, "yoyo": True, "repeat": 3}, "Mango swings"),
          ("snd", "w:upside", "boing")], words=[("w:upside", "UPSIDE DOWN!", .5, .82, .9, "sun")]),
    S("canopy", (900, 560, 1300), "A spider monkey's tail can hold up her whole body. So both her hands are free to pick fruit!", beat="fact", tag="fact: the tail holds her, hands free",
      actors=[("mango", "monkey_hangfruit", 900, 446, .6)], props=[prop("ar", lambda p: art.arrow(p, 620, 380, 840, 440), 0, 0, 1, True)],
      fx=[("show", "w:tail", "ar"), ("to", "w:hands", "#{p}mango-al,#{p}mango-ar", {"rotation": 14, "svgOrigin": "0 -206", "duration": .3, "yoyo": True, "repeat": 3}, "Mango shows her hands")],
      words=[("w:tail", "TAIL HOLDS ON", .25, .2, .75, "pill"), ("w:hands", "HANDS FREE!", .76, .8, .85, "sun")]),
    S("canopy", C("canopy", "milo", "body", 760, -40, -60), "How many fruits is Mango holding? Count with me! One, two!", q=True, tag="question: count two fruits", hide=["mango"],
      fx=[("count", "w:One,", 2, .8, {"x": 1420, "y": 420}), ("hop", "w:two!", "milo")]),
    S("canopy", (900, 560, 1300), "One for Tumble. One for Milo. And one more for me!", who="mango", tag="Mango: one for each", actors=[("mango", "monkey_hangfruit", 900, 446, .6)],
      props=[FR("f3", 1120, 520)], fx=[("hop", "w:Tumble.", "mango"), ("hop", "w:Milo.", "mango"), ("show", "w:more", "f3"), ("to", "w:me!", "#{p}mango-swing", {"rotation": -8, "svgOrigin": "0 0", "duration": .4, "yoyo": True, "repeat": 1}, "")]),
    S("bigtree", (620, 760, 1200), "Plop, plop, plop! Three fruits drop into the basket.", tag="plop into the basket", hide=["mango", "milo"],
      props=[BK(380, 930, .5, 0), FR("f1", 330, -80, .42, False), FR("f2", 380, -260, .42, False), FR("f3", 430, -440, .42, False)],
      fx=[("to", "w:Plop,", "#{p}f1_w", {"y": 850, "duration": .5, "ease": "power2.in"}, "a fruit drops"), ("to", "w:plop,", "#{p}f2_w", {"y": 850, "duration": .6, "ease": "power2.in"}, "a fruit drops"),
          ("to", "w:plop!", "#{p}f3_w", {"y": 850, "duration": .7, "ease": "power2.in"}, "a fruit drops"), ("face", "w:Three", "tumble", "happy")],
      words=[("w:Three", "3 FRUITS!", .72, .22, .9, "sun")]),
    S("bigtree", C("bigtree", "tumble", "all", 1100, 120, -40), "I'll carry the basket on my back. Off to the stream!", who="tumble", tag="Tumble carries the basket", hide=["milo"],
      move={"mango": (1000, 934, .55)}, props=[BK_ON(560)], fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:stream!", "mango"), ("trunk", "w:back.", "tumble", -60, .4)]),
    S("jungle", (744, 600, 1400), "Off they go, through the green jungle.", trans="iris", tag="off they go", move={"tumble": (200, 930, .62), "mango": (600, 934, .58), "milo": (300, 520, .78)},
      props=[BK_ON(200)], fx=WALKB(0.1, "tumble", 300, 3.0, ["bk"]) + [("walk", 0.1, "mango", 360, 3.0), ("fly", 0.1, "milo", 640, 470, 3.0)]),
    S("jungle", (980, 600, 1500), "Tumble carries the basket. Mango swings ahead, from vine to vine.", tag="Mango swings ahead", move={"tumble": (500, 930, .62), "mango": (900, 700, .58), "milo": (640, 470, .78)},
      props=[BK_ON(500)], fx=WALKB(0.1, "tumble", 300, 3.4, ["bk"]) + [("to", "w:swings", "#{p}mango_w", {"x": 1500, "y": 640, "duration": 1.6, "ease": "sine.inOut"}, "Mango swings ahead"),
                               ARM(0.05, "r", -160), ("fly", "w:vine", "milo", 1000, 440, 1.6)], words=[("w:swings", "SWING!", .76, .2, .9, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: the only way over is the wobbly bridge
    S("stream", SWIDE, "Here is the stream. And there is the picnic spot, on the other side!", trans="iris", beat="obstacle1", tag="the stream", cam2=(920, 560, 1900),
      props=[BR(), BK_ON(200), prop("ar", lambda p: art.arrow(p, 1380, 820, 1620, 900), 0, 0, 1, True)],
      fx=[("show", "w:picnic", "ar"), ("snd", "w:spot,", "ding")], words=[("w:stream.", "THE STREAM", .45, .25, .8, "pill"), ("w:picnic", "PICNIC SPOT", .8, .3, .7, "sun")]),
    S("stream", MCL("stream", 20), "The water is too wide to jump. How can we get across?", tag="Milo: how to get across", hide=["tumble", "mango"], props=[BR()],
      fx=[("hop", "w:jump.", "milo")], words=[("w:across?", "HOW?", .74, .22, 1.0, "pill")]),
    S("stream", C("stream", "mango", "all", 800, 40, -80), "The vine bridge! I can swing across, easy peasy!", who="mango", beat="obstacle1", tag="Mango: I can swing", hide=["tumble", "milo"], props=[BR()],
      fx=[ARM("w:vine", "r", -110), ("hop", "w:swing", "mango"), ARM("w:easy", "r", 0)], words=[("w:vine", "VINE BRIDGE", .72, .2, .8, "pill")]),
    S("paper_blue", (960, 540, 1700), "Spider monkeys have long arms and hook-like hands. They swing through the trees!", beat="fact", tag="fact: long arms, hook-like hands",
      props=[prop("bh", A4.branch, 960, 300, 1.0), prop("hb", A4.hand_big, 960, 560, 1.0, True)],
      fx=[("show", "w:hook-like", "hb"), ("to", "w:hands.", "#{p}hb-f", {"scaleY": .55, "svgOrigin": "0 -60", "duration": .5, "ease": "back.out(2)"}, "the fingers hook"),
          ("to", "w:swing", "#{p}hb_w", {"rotation": 8, "svgOrigin": "0 -250", "duration": .4, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "the hand swings")],
      words=[("w:long", "LONG ARMS", .22, .7, .8, "pill"), ("w:hook-like", "HOOK HANDS", .78, .7, .8, "sun")]),
    S("stream", C("stream", "tumble", "head", 860, -40, 20), "But I can't swing, Mango. I'm an elephant!", who="tumble", beat="obstacle1", tag="Tumble: I can't swing", hide=["mango", "milo"], props=[BR(), BK_ON(200)],
      fx=[("face", 0.02, "tumble", "wow"), ("trunk", "w:elephant!", "tumble", -40, .4)], words=[("w:elephant!", "NO SWINGING!", .74, .2, .75, "pill")]),
    S("stream", (900, 860, 1100), "The bridge is low and short. But it goes wiggle, wobble!", beat="obstacle1", tag="wiggle wobble", hide=only("stream"), props=[BR(), prop("wl", A.wobble_lines, 970, 880, 1.0, True)],
      fx=WOB("w:wiggle,", 7) + [("show", "w:wiggle,", "wl")], words=[("w:wiggle,", "WIGGLE!", .3, .3, .9, "sun"), ("w:wobble!", "WOBBLE!", .7, .3, .9, "sun")]),
    S("stream", (560, 760, 1300), "Tumble puts one foot on the bridge. Wobble! He steps back.", beat="obstacle1", tag="one foot on", hide=["milo"], props=[BR(), BK_ON(200)], move={"mango": (180, 934, .55)},
      fx=WALKB(0.2, "tumble", 260, 1.2, ["bk"]) + WOB("w:Wobble!", 3) + WALKB("w:steps", "tumble", -260, 1.0, ["bk"]) + [("face", "w:Wobble!", "tumble", "wow")],
      words=[("w:Wobble!", "WOBBLE!", .7, .25, .9, "sun")]),
    S("stream", C("stream", "tumble", "head", 860, -40, 20), "Oh! It wiggles! I'm not sure about this, Mango.", who="tumble", beat="obstacle1", tag="Tumble: not sure", hide=["mango", "milo"], props=[BR(), BK_ON(200)],
      fx=[("face", 0.02, "tumble", "sad"), ("trunk", "w:wiggles!", "tumble", 20, .3), ("trunk", "e:Mango.", "tumble", 0, .4)], words=[("w:sure", "NOT SURE...", .74, .2, .75, "pill")]),
    S("stream", MCL("stream", 20), "Is the bridge still, or is it wobbly?", q=True, beat="obstacle1", tag="question: still or wobbly", pause=3.2, hide=["tumble", "mango"], props=[BR()],
      fx=[("signs", "w:still,", ["STILL", "WOBBLY"], 1, "wait:2.0")]),
    # ------------------------------------------------------------ OBSTACLE 2: Mango runs on too fast, and the basket tips
    S("stream", C("stream", "mango", "all", 800, 40, -80), "Watch me, Tumble! I'll take the basket over. Here I go!", who="mango", beat="obstacle2", tag="Mango: watch me", hide=["tumble", "milo"], props=[BR()],
      fx=[("hop", "w:Watch", "mango"), ("face", 0.02, "mango", "happy"), ("hop", "w:go!", "mango")], words=[("w:go!", "ZOOM!", .74, .25, 1.0, "sun")]),
    S("stream", (760, 760, 1300), "Mango runs onto the bridge, fast, fast, fast. Boing! The bridge bounces!", beat="obstacle2", tag="too fast", hide=["milo"],
      move={"mango": (500, 934, .55)}, props=[BR(), BK(560, 912, .36)],
      fx=WALKB("w:runs", "mango", 300, .9, ["bk"]) + WOB("w:Boing!", 5, 1.8, ("mango",)) + [("snd", "w:Boing!", "boing")], words=[("w:fast,", "TOO FAST!", .3, .22, .9, "pill"), ("w:Boing!", "BOING!", .7, .22, 1.0, "sun")]),
    S("stream", (620, 800, 1100), "Oh no! The basket tips over. The fruit rolls out on the grass.", beat="obstacle2", tag="the basket tips", hide=["milo", "tumble"], move={"mango": (800, 934, .55)},
      props=[BR(), BK(860, 912, .36, 0), FR("f1", 840, 860, .36, False), FR("f2", 860, 850, .36, False), FR("f3", 880, 860, .36, False)],
      fx=[("to", "w:tips", "#{p}bk_w", {"rotation": -100, "x": 700, "y": 950, "duration": .5, "ease": "power2.in"}, "the basket tips"),
          ("to", "w:fruit", "#{p}f1_w", {"x": 300, "y": 990, "rotation": -360, "duration": 1.4, "ease": "power1.out"}, "a fruit rolls"),
          ("to", "w:rolls", "#{p}f2_w", {"x": 440, "y": 1010, "rotation": -360, "duration": 1.3, "ease": "power1.out"}, "a fruit rolls"),
          ("to", "w:grass.", "#{p}f3_w", {"x": 560, "y": 980, "rotation": -360, "duration": 1.0, "ease": "power1.out"}, "a fruit rolls"), ("face", "w:Oh", "mango", "wow")],
      words=[("w:tips", "OOPS!", .7, .22, 1.0, "sun")]),
    S("stream", C("stream", "mango", "head", 760, 0, 20), "Oops! I went too fast. I'm sorry, Tumble.", who="mango", beat="obstacle2", tag="Mango: too fast", hide=["tumble", "milo"], move={"mango": (560, 934, .55)}, props=[BR()],
      fx=[("face", 0.02, "mango", "sad"), ("arm", "w:sorry,", "mango", "r", -30)], words=[("w:fast.", "TOO FAST", .74, .22, .8, "pill")]),
    S("stream", (440, 860, 1100), "Tumble helps. He picks up the fruit with his trunk. Count with me! One, two, three!", q=True, beat="obstacle2", tag="question: count the fruit",
      hide=["milo", "mango"], props=[BR(), BK(560, 930, .46, 0), FR("f1", 300, 990, .36, False), FR("f2", 440, 1010, .36, False), FR("f3", 560, 980, .36, False)],
      fx=[("trunk", "w:picks", "tumble", 30, .4), ("count", "w:One,", 3, 1.3, {"x": 1400, "y": 400}), ("hide", "w:One,", "f1"), ("hide", "w:two,", "f2"), ("hide", "w:three!", "f3")]),
    S("stream", C("stream", "tumble", "head", 860, -40, 20), "All three are back in the basket. Phew!", who="tumble", beat="obstacle2", tag="Tumble: phew", hide=["milo", "mango"], props=[BR(), BK_ON(200)],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:Phew!", "tumble", -40, .3)], words=[("w:Phew!", "PHEW!", .74, .22, 1.0, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 3: Tumble tries alone; the wobble is too much, and he goes back
    S("stream", C("stream", "tumble", "head", 860, -40, 20), "My turn. I'll try it all by myself.", who="tumble", beat="obstacle3", tag="Tumble: my turn", hide=["milo", "mango"], props=[BR(), BK_ON(200)],
      fx=[("face", 0.02, "tumble", "happy"), ("nod", "w:try", "tumble")], words=[("w:myself.", "BY MYSELF", .74, .22, .8, "pill")]),
    S("stream", (700, 740, 1400), "One step, two steps. Wobble, wobble, WOBBLE! Back he goes.", beat="obstacle3", tag="too wobbly alone", hide=["milo"], move={"mango": (130, 934, .55)}, props=[BR(), BK_ON(200)],
      fx=WALKB("w:One", "tumble", 340, 1.4, ["bk"]) + WOB("w:Wobble,", 9, 1.5, ("tumble",)) + [("face", "w:Wobble,", "tumble", "wow")] + WALKB("w:Back", "tumble", -340, 1.2, ["bk"]),
      words=[("w:WOBBLE!", "WOBBLE!", .62, .2, 1.1, "sun")]),
    S("stream", C("stream", "tumble", "head", 860, -40, 20), "It wobbles too much when I go alone.", who="tumble", beat="obstacle3", tag="Tumble: too much alone", hide=["milo", "mango"], props=[BR(), BK_ON(200)],
      fx=[("face", 0.02, "tumble", "sad"), ("trunk", "w:alone.", "tumble", 20, .5)]),
    S("stream", (980, 560, 1500), "Milo flies over. Easy for a bird! But elephants cannot fly.", beat="obstacle3", tag="Milo flies over", hide=["mango"], props=[BR(), BK_ON(200)],
      move={"milo": (500, 520, .7)}, fx=[("fly", "w:Milo", "milo", 1500, 500, 1.6), ("hop", "w:bird!", "milo"), ("face", "w:But", "tumble", "sad")], words=[("w:Easy", "EASY!", .78, .2, .9, "sun")]),
    S("stream", MCL("stream", 20), "Can an elephant fly? Yes, or no?", q=True, beat="obstacle3", tag="question: can an elephant fly", pause=3.2, hide=["tumble", "mango"], props=[BR()],
      fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    # ------------------------------------------------------------ LOW MOMENT: Tumble sits down; maybe no picnic (gentle: nobody cries)
    S("stream", (420, 800, 1200), "Tumble sits down by the stream. Maybe there will be no picnic today.", beat="low", tag="Tumble sits down", hide=["milo"], move={"mango": (680, 934, .55)}, props=[BR(), BK(560, 930, .46)],
      fx=[("to", "w:sits", "#{p}tumble", {"y": 30, "duration": .6}, "Tumble sits down"), ("face", "w:sits", "tumble", "sad"), ("face", "w:Maybe", "mango", "sad")], words=[("w:picnic", "NO PICNIC?", .5, .16, .9, "pill")]),
    S("stream", C("stream", "tumble", "head", 860, -40, 20), "You go without me, Mango. I can't do it.", who="tumble", beat="low", tag="Tumble: go without me", hide=["milo", "mango"], props=[BR()],
      fx=[("face", 0.02, "tumble", "sad"), ("blinkslow", "w:can't", "tumble-eye", 1)]),
    S("stream", (420, 800, 1200), "Mango sits down next to Tumble. Tumble's tail droops low.", beat="low", tag="Mango sits beside him", hide=["milo"], move={"mango": (640, 950, .55)}, props=[BR(), BK(560, 930, .46)],
      fx=[("to", 0.05, "#{p}tumble", {"y": 30, "duration": .01}, ""), ("face", 0.05, "tumble", "sad"), ("to", "w:sits", "#{p}mango_w", {"x": 520, "duration": .8}, "Mango sits down next to him"), ("face", "w:Tumble.", "mango", "sad"),
          ("to", "w:tail", "#{p}tumble-tail", {"rotation": 20, "svgOrigin": "-268 -390", "duration": .6}, "his tail droops")]),
    S("stream", C("stream", "mango", "head", 760, 0, 20), "No, Tumble. A picnic is no fun without you.", who="mango", beat="low", tag="Mango: no fun without you", hide=["tumble", "milo"], move={"mango": (560, 934, .55)}, props=[BR()],
      fx=[("face", 0.02, "mango", "sad"), ("face", "w:picnic", "mango", "happy")], words=[("w:fun", "NO FUN ALONE", .74, .22, .7, "pill")]),
    S("stream", MCL("stream", 20), "What can good friends do? Go alone, or help?", q=True, beat="low", tag="question: alone or help", pause=3.2, hide=["tumble", "mango"], props=[BR()],
      fx=[("signs", "w:alone,", ["ALONE", "HELP"], 1, "wait:2.0")]),
    # ------------------------------------------------------------ SOLUTION: Mango works it out herself
    S("stream", C("stream", "mango", "head", 760, 0, 20), "Hmm. I went too fast. And I did not hold on.", who="mango", beat="solution", tag="Mango thinks", hide=["tumble", "milo"], move={"mango": (560, 934, .55)}, props=[BR()],
      fx=[("face", 0.02, "mango", "sad"), ("arm", "w:Hmm.", "mango", "r", -150), ("arm", "w:did", "mango", "r", 0)], words=[("w:Hmm.", "HMM...", .74, .22, .9, "pill")]),
    S("stream", C("stream", "mango", "all", 800, 40, -80), "I know! My tail can hold the vine, like an extra hand!", who="mango", beat="solution", tag="Mango: my tail", hide=["tumble", "milo"], props=[BR()],
      fx=[("face", 0.02, "mango", "wow"), ("hop", "w:know!", "mango"), TAIL("w:tail")], words=[("w:tail", "MY TAIL!", .74, .22, 1.0, "sun")]),
    S("paper_pink", (960, 560, 1600), "A spider monkey's tail can grab and hold, like an extra hand.", beat="fact", tag="fact: the tail grabs like a hand",
      actors=[("m", "monkey_grip", 960, 900, .9)], props=[prop("bh", lambda p: A4.branch(p, 900), 1110, 621, 1.0), prop("ar", lambda p: art.arrow(p, 1420, 420, 1170, 600), 0, 0, 1, True)],
      fx=[("show", "w:grab", "ar"), ("to", "w:hold,", "#{p}m-tail", {"rotation": -4, "svgOrigin": "40 -80", "duration": .3, "yoyo": True, "repeat": 3}, "the tail holds"), ("arm", "w:extra", "m", "l", 60)],
      words=[("w:grab", "TAIL GRABS!", .76, .2, .85, "sun"), ("w:extra", "EXTRA HAND", .26, .2, .8, "pill")]),
    S("stream", C("stream", "mango", "all", 800, 40, -80), "I hold the vine with my tail. I hold your trunk with my hand. And we go slow, side by side.", who="mango", beat="solution", tag="Mango: the plan", hide=["tumble", "milo"], props=[BR()],
      fx=[TAIL("w:vine"), ARM("w:hand.", "l", 60), ARM("w:slow,", "l", 0), ("hop", "w:side", "mango")], words=[("w:slow,", "SLOW", .74, .2, 1.0, "sun"), ("w:side", "SIDE BY SIDE", .74, .36, .7, "pill")]),
    S("stream", C("stream", "tumble", "head", 860, -40, 20), "Slow, and together? Okay. Let's try!", who="tumble", beat="solution", tag="Tumble: let's try", hide=["milo", "mango"], props=[BR(), BK_ON(200)],
      fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:try!", "tumble")], words=[("w:try!", "LET'S TRY!", .74, .2, .85, "sun")]),
    # ------------------------------------------------------------ SONG MOMENT: the rhyme SAID, then the tune on instruments while they cross
    S("stream", (900, 640, 1500), "One step, two steps, slow and steady. Hold on tight, and here we go. Ready?", who="mango", beat="solution", tag="the stepping rhyme", actors=CROSS, move={"tumble": (340, 930, .6), "mango": (740, 934, .55)},
      props=[BR(), BK_ON(340)], fx=[ARM(0.05, "l", 60), ("hop", "w:steady.", "mango"), ("nod", "w:tight,", "tumble")], words=[("w:slow", "SLOW AND STEADY", .5, .14, .62, "pill"), ("w:Ready?", "READY?", .78, .32, .9, "sun")]),
    S("stream", (980, 620, 1560), who="", sing=SING_STEP, beat="song", tag="song: step by step", actors=CROSS, move={"tumble": (340, 930, .6), "mango": (740, 934, .55)}, props=[BR(), BK_ON(340)],
      fx=[ARM(0.05, "l", 60)] + WALKB(TB(0), "tumble", 300, 9.6, ["bk"]) + [("walk", TB(0), "mango", 300, 9.6)] + WOB(TB(4), 3, .5, ("tumble", "mango")) + WOB(TB(12), 3, .5, ("tumble", "mango")),
      words=[(TB(0), "STEP BY STEP", .5, .14, .7, "sun"), (TB(8), "SLOW AND STEADY", .5, .14, .62, "pill")]),
    S("stream", (980, 640, 1500), "Count the steps with me! Three, four, five, six!", q=True, beat="solution", tag="question: count the steps", actors=CROSS, move={"tumble": (640, 930, .6), "mango": (1040, 934, .55)},
      props=[BR(), BK_ON(640)], fx=[ARM(0.05, "l", 60), ("count", "w:Three,", 4, 1.8, {"x": 960, "y": 260})] + WALKB("w:Three,", "tumble", 160, 2.2, ["bk"]) + [("walk", "w:Three,", "mango", 160, 2.2)]),
    S("stream", (1040, 640, 1500), "The bridge gives a little wobble. But Mango holds on tight, and so does Tumble.", beat="solution", tag="holding on tight", actors=CROSS, move={"tumble": (800, 930, .6), "mango": (1200, 934, .55)},
      props=[BR(), BK_ON(800)], fx=[ARM(0.05, "l", 60)] + WOB("w:wobble.", 5, .9, ("tumble", "mango")) + [TAIL("w:holds"), ("face", "w:Tumble.", "tumble", "happy")], words=[("w:tight,", "HOLD ON!", .76, .2, 1.0, "sun")]),
    S("stream", (1200, 640, 1500), "Seven, eight, and hop! They made it across!", beat="solution", tag="across", actors=[("tumble", "tumble", 800, 930, .6), ("mango", "monkey", 1200, 934, .55)],
      props=[BR(), BK_ON(800)], fx=WALKB("w:Seven,", "tumble", 360, 1.6, ["bk"]) + [("walk", "w:Seven,", "mango", 380, 1.6), ("hop", "w:hop!", "tumble"), ("hop", "w:hop!", "mango"), ("snd", "w:across!", "ding")],
      words=[("w:across!", "WE DID IT!", .5, .18, 1.0, "sun")]),
    S("stream", C("stream", "tumble", "head", 860, -40, 20, stage=[("tumble", "tumble", 1160, 930, .6)]), "I did it! No, we did it, together!", who="tumble", beat="solution", tag="Tumble: we did it",
      actors=[("tumble", "tumble", 1160, 930, .6)], props=[BR(), BK_ON(1160)], fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:did", "tumble"), ("hop", "w:together!", "tumble")], words=[("w:together!", "TOGETHER!", .26, .2, .9, "sun")]),
    S("stream", C("stream", "mango", "head", 760, 0, 20, stage=[("mango", "monkey", 1580, 934, .55)]), "You tried again, Tumble. You were so brave!", who="mango", beat="solution", tag="Mango: so brave",
      actors=[("mango", "monkey", 1580, 934, .55)], props=[BR()], fx=[("face", 0.02, "mango", "happy"), ("hop", "w:brave!", "mango"), TAIL("w:tried")], words=[("w:brave!", "SO BRAVE!", .26, .22, .9, "sun")]),
    # ------------------------------------------------------------ WARM ENDING: the picnic, then home to Mama
    S("meadow", WIDE, "At last, the picnic! A blanket in the sun, and a basket of fruit.", trans="iris", beat="ending", tag="the picnic", cam2=(980, 560, 1800),
      props=[prop("bl", A.blanket, 900, 1010, 1.0), BK(900, 1000, .5), FR("f1", 720, 990, .4), FR("f2", 900, 1040, .4), FR("f3", 1080, 990, .4)],
      fx=[("show", "w:fruit.", "f1"), ("show", "w:fruit.", "f2"), ("show", "w:fruit.", "f3"), ("hop", "w:picnic!", "mango")], words=[("w:picnic!", "PICNIC!", .5, .16, 1.0, "sun")]),
    S("meadow", MCL("meadow", 0, -40), "How many fruits are on the blanket? Count with me! One, two, three!", q=True, beat="ending", tag="question: count the picnic fruit", hide=["tumble", "mango"],
      fx=[("count", "w:One,", 3, 1.3, {"x": 1420, "y": 420}), ("hop", "w:three!", "milo")]),
    S("meadow", C("meadow", "mango", "head", 800, 0, 30), "One for Tumble, one for Milo, and one for me. Yummy!", who="mango", beat="ending", tag="Mango shares", hide=["tumble", "milo"], props=[FR("f1", 1240, 900, .4, False)],
      fx=[ARM("w:Tumble,", "l", 50), ARM("w:Milo,", "l", 20), ARM("w:me.", "l", 0), ("hop", "w:Yummy!", "mango")], words=[("w:Yummy!", "YUM!", .76, .22, 1.0, "sun")]),
    S("meadow", C("meadow", "tumble", "head", 900, -40, 20), "Thank you for walking with me, Mango.", who="tumble", beat="ending", tag="Tumble: thank you", hide=["mango", "milo"],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:walking", "tumble", -50, .4), ("trunk", "e:Mango.", "tumble", 0, .4)]),
    S("meadow", C("meadow", "mango", "head", 800, 0, 30), "And thank you for trying again, Tumble.", who="mango", beat="ending", tag="Mango: thank you", hide=["tumble", "milo"],
      props=[prop("h1", lambda p: art2.heart(p), 1520, 640, .7, True)], fx=[("face", 0.02, "mango", "happy"), ("show", "w:trying", "h1"), TAIL("w:Tumble.")]),
    S("zoo_eve", WIDE, "Back at the zoo, the sun is low. And Mama is waiting.", trans="iris", beat="ending", tag="back at the zoo", cam2=(1000, 560, 1800),
      move={"tumble": (300, 940, .6), "mango": (80, 940, .55)}, fx=[("walk", 0.1, "tumble", 360, 3.2), ("walk", 0.1, "mango", 220, 3.2)], words=[("w:Mama", "HOME!", .5, .16, 1.0, "sun")]),
    S("zoo_eve", C("zoo_eve", "tumble", "all", 1000, 40, -60), "Mama! I crossed the wobbly bridge, with Mango!", who="tumble", beat="ending", tag="Tumble tells Mama", hide=["mama", "milo"],
      fx=[("face", 0.02, "tumble", "happy"), ("hop", "w:crossed", "tumble"), ("hop", "w:Mango!", "mango")], words=[("w:wobbly", "WOBBLY BRIDGE", .5, .16, .7, "pill")]),
    S("zoo_eve", C("zoo_eve", "mama", "head", 900, 60, 50), "You tried again, Tumble. And Mango slowed down to help. I am so proud of you both.", who="mama", beat="ending", tag="Mama: so proud", hide=["milo", "tumble", "mango"],
      fx=[("nod", "w:tried", "mama"), ("nod", "w:Mango", "mama"), ("blinkslow", "w:proud", "mama-eye", 1)], words=[("w:proud", "SO PROUD!", .2, .2, .8, "sun")]),
    S("zoo_eve", (1200, 660, 1400), "Mama wraps her trunk around Tumble. A big, warm trunk hug.", beat="ending", tag="trunk hug", hide=["milo", "mango"], move={"tumble": (900, 940, .6)},
      props=[prop("h1", lambda p: art2.heart(p), 1030, 470, .7, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 1105, 440, .5, True)],
      fx=[("trunk", "w:wraps", "mama", 34, .8), ("lookat", "w:wraps", "mama", 8), ("show", "w:big,", "h1"), ("show", "w:hug.", "h2"),
          ("to", "w:big,", "#{p}h1_w,#{p}h2_w", {"y": "-=60", "duration": 1.6, "ease": "sine.out"}, "")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 130, 0), "When a friend feels wobbly, we can slow down, and go together.", beat="ending", tag="the lesson", hide=["mama", "tumble", "mango"],
      fx=[("hop", "w:together.", "milo")], words=[("w:slow", "SLOW DOWN", .73, .16, .75, "pill"), ("w:together.", "TOGETHER", .73, .3, .75, "sun")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 40, 0), "Do you remember? What did Mango hold the vine with? Her tail, or her ear?", q=True, beat="ending", tag="question: tail or ear", pause=3.2,
      hide=["mama", "tumble", "mango"], cam2=C("zoo_eve", "milo", "body", 830, 40, -60), fx=[("signs", "w:tail,", ["TAIL", "EAR"], 0, "wait:2.0")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 40, 0), "And how did they cross the bridge? Fast, or slow?", q=True, beat="ending", tag="question: fast or slow", pause=3.2,
      hide=["mama", "tumble", "mango"], cam2=C("zoo_eve", "milo", "body", 830, 40, -60), fx=[("signs", "w:Fast,", ["FAST", "SLOW"], 1, "wait:2.0")]),
    S("zoo_eve", (980, 560, 1880), "One step, two steps, slow and steady. Hooray, hooray, the picnic was ready!", beat="ending", tag="the closing rhyme", cam2=(1000, 560, 1780),
      fx=[("hop", "w:Hooray,", "milo"), ("hop", "w:hooray,", "tumble"), ("hop", "w:picnic", "mango"), ("nod", "w:ready!", "mama")], words=[("w:slow", "SLOW AND STEADY", .5, .15, .6, "pill")]),
    S("zoo_eve", WIDE, who="", sing=SING_END_A, beat="song", tag="song: hooray", cam2=(980, 560, 1880),
      fx=[("hop", 1.0, "tumble"), ("hop", 1.0, "mango"), ("nod", 3.2, "mama"), TAIL(2.0)], words=[(TB(3), "HOORAY!", .5, .2, 1.05, "sun")]),
    S("zoo_eve", (1145, 620, 1500), who="", sing=SING_END_B, beat="song", tag="song: side by side", cam2=(1145, 620, 1420), hide=["milo", "mango"],
      props=[prop("h1", lambda p: art2.heart(p), 1010, 370, .9, True), prop("h2", lambda p: art2.heart(p, "#ff9ab8"), 930, 320, .6, True)],
      fx=[("nod", 1.6, "mama"), ("show", TB(1.5), "h1"), ("show", TB(3.5), "h2"), ("hop", 3.0, "tumble")]),
    S("zoo_eve", C("zoo_eve", "milo", "body", 900, 0, 0), "Next time: who took Mango's breakfast? See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure", hide=["mama", "tumble", "mango"],
      fx=[("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .78, .17, .8, "sun"), ("w:See", "SEE YOU SOON!", .78, .32, .72, "pill")]),
]

# thumbnail (thumb.py): the example in the picture (Mango holds the rope with her tail and Tumble's trunk with her hand), 3 words at most, none of the title's words, no watermark
THUMBS = {
    "za_ep04": {"place": "stream", "cam": (900, 700, 1200),
                "actors": [("tumble", 600, 930, .6, False, ''),
                           ("monkey_grip", 1000, 934, .55, False, 'gsap.set("#P-al",{rotation:60,svgOrigin:"-58 -206"});')],
                "props": [(A.bridge, 970, 930, 1.0)],
                "words": [("HOLD ON!", 1200, 330, 190, "sun")]},
}
