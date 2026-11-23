"""za_ep14 - Milo's Zoo Adventures: "Can Poppy Stay Awake to See the Dancing Sky?" (theme title "Poppy and the Dancing Sky"; cartoon adventure, the
3D music-and-sync process: "beat"). Arctic week, adventure 3.
Milo and Tumble visit Poppy the polar bear cub. Tonight the sky is going to dance (the northern lights), and Poppy wants to see it, but she always
falls asleep first. She counts the stars (and falls asleep), does a bouncy dance in the snow (gets tired, lies down, falls asleep), walks up the
snowy hill (sits down at the top, falls asleep). Each time a friend wakes her gently, and the sky is still dark. Low moment: "maybe I will never see
the dancing sky" (a little sad, never crying; her friends stay with her). Poppy's own idea: take turns. She sleeps first in a snow nest, Tumble
watches, then Milo watches; when the green lights come, Milo wakes her gently. The rhyme is said, the tune is played on instruments, and the three
friends watch the dancing sky together. Nobody is hurt, lost, crying or trapped; nobody is in danger: being sleepy is a small, funny problem
that friends solve together. (No song is sung: the premise's "a song" became "a bouncy dance", owner's rule of Nov 17 8:25 PM.)

FACTS, read at the source on Nov 23 2026, about 9:20 AM ET (each page fetched by the session's page reader, which quoted these sentences verbatim;
it trims a quote at 125 characters, so some are a clause of a longer sentence):
 [NSP] NASA Space Place, "What Is an Aurora?", spaceplace.nasa.gov/aurora/
   "If you're near the North Pole, it is called an aurora borealis or northern lights."
   "Even though auroras are best seen at night, they happen because of activity from the Sun and Earth's magnetic field."
   "Oxygen gives off green and red light."   "Nitrogen glows blue and purple."
 [NES] NOAA NESDIS, "What is an Aurora?", nesdis.noaa.gov/about/k-12-education/optical-phenomena/what-aurora
   "Auroras are often seen in areas near the North Pole or South Pole."   "Even though auroras are best seen at night, they are actually caused by the sun."
 [NCEI] NOAA NCEI, "The Science, Beauty, and Mystery of Auroras", ncei.noaa.gov/news/science-beauty-and-mystery-auroras
   "Cloudy or overcast skies decrease visibility" (clause)   "These sheets ripple and move across the sky as the aurora evolves," (clause)
   "Although auroral lights appear most frequently in the night sky near the poles" (clause)
 [SWPC] NOAA Space Weather Prediction Center, "Aurora Tutorial", swpc.noaa.gov/content/aurora-tutorial
   "The most common auroral color is a pale green color at a wavelength of 557.7 nm."
   "This can be seen as waves or ripples in the auroral arcs much like someone running their hand along a curtain."
 [NAS] NASA Science, "Auroras", science.nasa.gov/sun/auroras
   "The most common color is green, which is produced when oxygen is excited by electrons" (clause)
   "An aurora can appear in a variety of colors, from an eerie green to blue and purple to pink and red."
 Said as facts in the film (three fact boards, questions, recap): the northern lights are often seen near the North Pole [NES, NSP, NCEI]; they are
 best seen at night, when the sky is dark, and clouds can hide them [NSP, NES, NCEI]; most northern lights are green, they can also be pink or
 purple, and they ripple and move across the sky like a waving curtain [SWPC, NAS, NCEI].
 NOT said as facts: what makes the lights (the sun, particles: too much for ages 2-6), when in the year they come, anything about how polar bear cubs
 sleep (no page read today says it). The lights coming "tonight", Poppy falling asleep, taking turns, the rhyme and the tune are THIS story.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, art3
import art_za_ep09 as A9
import art_za_ep10 as A10
import art_za_ep13 as A13
import art_za_ep14 as A
import kit
from kit import Kit, S, prop
from intro import INTRO_STAGES, intro_shots      # the main intro, right after the hook and as the last shots (owner, Nov 20 4:50 PM)

EP = {"id": "za_ep14", "kind": "story", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.4, "music": 0.5, "lead_in": 0.3, "tail": 1.2,
      "cast": {"milo": {"voice": "af_heart", "speed": .8}, "poppy": {"voice": "af_jessica", "speed": .88, "pitch": 4, "formant": 1.2, "gain": .9},
               "tumble": {"voice": "am_puck", "speed": .85, "pitch": 5, "formant": 1.16, "gain": .66}},
      "title": "Can Poppy Stay Awake to See the Dancing Sky?", "thumb_text": "WAKE UP!",
      "series": "Milo's Zoo Adventures",
      "description": ("Can Poppy stay awake to see the dancing sky? Tonight the green northern lights will shine over the Arctic, but Poppy the polar bear cub "
                      "always falls asleep first! She counts the stars, she dances in the snow, she walks up the hill... and every time, she falls asleep. "
                      "Then Poppy has an idea: her friends Milo the bluebird and Tumble the baby elephant can take turns keeping watch. "
                      "A gentle Arctic adventure for ages 2-6 about teamwork and taking turns, with questions to answer, a count-along and a little tune.\n"
                      "Kids see how the northern lights are often seen near the North Pole, how they are best seen on dark nights when clouds do not hide them, "
                      "and how most northern lights are green and ripple across the sky like a waving curtain.\n\n"
                      "The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
                      "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.\n\n"
                      "WHERE THE FACTS COME FROM\nNASA Space Place (What Is an Aurora?); NOAA NESDIS (What is an Aurora?); NOAA National Centers for Environmental "
                      "Information (auroras); NOAA Space Weather Prediction Center (Aurora Tutorial); NASA Science (Auroras)."),
      "tags": ["northern lights for kids", "aurora for kids", "polar bear cub", "polar bear for kids", "arctic animals for kids", "bedtime story for kids", "taking turns",
               "baby elephant", "animal stories for kids", "friendship story for kids", "kids adventure cartoon", "preschool", "toddlers", "Milo the bluebird", "The Animated Zoo"]}

PO = lambda x, y, s=.6, f=False, kind="bear": ("poppy", kind, x, y, s, f)
PB = lambda x, y, s=.6, f=False: ("poppy", "bear_belly", x, y, s, f)
TU = lambda x, y, s=.55, f=False: ("tumble", "tumble", x, y, s, f)
MI = lambda x, y, s=.6: ("milo", "milo", x, y, s, False, True)
STAGES = {
    "arctic_eve": [TU(330, 900), PO(1120, 900, f=True), MI(730, 560)],
    "arctic_night": [TU(330, 900), PO(1180, 900, f=True), MI(770, 560)],
    "snow_night": [PO(900, 935), TU(1640, 935, f=True), MI(1280, 600)],
    "hilltop_night": [TU(280, 880), PO(800, 880, .62), MI(1180, 620)],
    "hilltop_lights": [PB(820, 880, .62)],
    "nest_night": [TU(290, 920), PB(820, 920), MI(1380, 680)],
    "nest_lights": [TU(290, 920), PB(820, 920), MI(1380, 680)],
    **INTRO_STAGES,
}
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
PH = lambda place, w=820, dx=-40, dy=40, stage=None: C(place, "poppy", "head", w, dx, dy, stage=stage)       # Poppy's face, close
TH = lambda place, w=860, dx=40, dy=40, stage=None: C(place, "tumble", "head", w, dx, dy, stage=stage)       # Tumble's face, close
MB = lambda place, w=820, dx=0, dy=-40, stage=None: C(place, "milo", "body", w, dx, dy, stage=stage)         # Milo asks: low in the frame, under the signs

# ---- sleepy Poppy (the bear's eye has a lid: "#<poppy>-eye-lid"; toon's "sleep" shuts it and stops the idle blink)
YAWN = lambda at: ("to", at, "#{p}poppy-jaw", {"opacity": 1, "y": 14, "scale": 1.5, "transformOrigin": "50% 0%", "duration": .45, "yoyo": True, "repeat": 1, "repeatDelay": .7}, "Poppy yawns")
DROOP = lambda at, n=2: ("blinkslow", at, "poppy", n)
SLEEP = lambda at: ("sleep", at, "poppy")
ASLEEP = [("sleep", 0.3, "poppy"), ("to", 0.0, "#{p}poppy-eye-lid", {"opacity": 1, "duration": 0})]   # asleep from frame 1 (the sleep blink falls before the shot; no idle blink)
WAKE = lambda at: [("to", at, "#{p}poppy-eye-lid", {"opacity": 0, "duration": .01}, "Poppy opens her eyes"), ("to", at, "#{p}poppy-neck", {"rotation": 0, "duration": .4}, "")]
Z = lambda x, y, s=.8, hidden=False: prop("zz", A.zzz, x, y, s, hidden)
ZFLOAT = lambda at: ("to", at, "#{p}zz", {"y": -30, "opacity": .6, "duration": .9, "yoyo": True, "repeat": 11, "ease": "sine.inOut"}, "the Z's float")
FADEIN = lambda at, sel, what: ("fromto", at, sel, {"opacity": 0}, {"opacity": 1, "duration": .4}, what)
BLINK = lambda at, sel, what, n=5: ("to", at, sel, {"opacity": .35, "duration": .2, "yoyo": True, "repeat": n}, what)

# ---- the dancing sky: three curtains of light that sway, stretch and drift (art_za_ep14.lights)
def DANCE(at, fast=1.0):
    return [("to", at, "#{p}aur1", {"skewX": 10, "x": "+=70", "scaleY": 1.12, "transformOrigin": "50% 100%", "duration": 1.25 / fast, "yoyo": True, "repeat": 21, "ease": "sine.inOut"}, "the green lights dance"),
            ("to", at, "#{p}aur2", {"skewX": -9, "x": "-=60", "opacity": .6, "transformOrigin": "50% 100%", "duration": 1.0 / fast, "yoyo": True, "repeat": 25, "ease": "sine.inOut"}, ""),
            ("to", at, "#{p}aur3", {"skewX": 7, "scaleY": 1.22, "transformOrigin": "50% 100%", "duration": 1.5 / fast, "yoyo": True, "repeat": 17, "ease": "sine.inOut"}, "")]
LIGHTS_ON = lambda at: ("to", at, "#{p}aur", {"opacity": 1, "duration": 1.6, "ease": "sine.inOut"}, "the green lights appear")
RIB = lambda at, name: ("to", at, "#{p}%s-rib" % name, {"skewX": 8, "x": "+=24", "transformOrigin": "50% 100%", "duration": .9, "yoyo": True, "repeat": 13, "ease": "sine.inOut"}, "the little lights ripple")

STARS = [(560, 430), (800, 360), (1060, 330), (1320, 360), (1580, 430)]
STAR_PROPS = lambda: [prop("st%d" % k, A9.big_star, x, y, .9) for k, (x, y) in enumerate(STARS)]
POP = lambda at, k: ("fromto", at, "#{p}st%d_w" % k, {"scale": .4}, {"scale": 1.25, "duration": .25, "yoyo": True, "repeat": 1, "ease": "back.out(2)"}, "a star twinkles")

# Owner, Nov 17 8:25 PM: no voice is synthesized onto notes. The rhyme is SAID in a spoken shot, then the tune is played by the bells and the soft band.
REFRAIN = {"bpm": 96, "chords": "C G F C", "outro_bars": 0, "style": "lullaby"}
SING_SKY = dict(REFRAIN, lines=[{"text": "~ ~ ~ ~ ~ ~", "notes": "G4:1 C5:1 E5:2 D5:1 B4:1 G4:1", "rest": 1},      # green lights dancing, way up high (C bar, G bar)
                                {"text": "~ ~ ~ ~ ~ ~", "notes": "A4:1 C5:1 F5:2 E5:1 C5:1 G4:1", "rest": 1}])     # take turns, friends, and watch the sky (F bar, C bar)
SING_END = dict(REFRAIN, chords="G C", lines=[{"text": "~ ~ ~ ~ ~", "notes": "B4:1 G4:1 D5:1 B4:1 C5:2", "rest": 2}])
TB = lambda b: round(0.12 + b * 60 / 96, 2)      # seconds into a tune shot of beat b of its tune
CNT5 = 1.22                                      # seconds from "One" to "five" (set from the timing file)

NEST = [TU(290, 920), PB(820, 920), MI(1380, 680)]
NCAM = (860, 660, 1560)                          # a nest view: everybody whole, the lights above them
ZA, ZS, ZH, ZN = (990, 650), (1110, 680), (1010, 630), (1000, 670)      # the Z's over sleeping Poppy's head: shore, snow, hilltop, nest

SHOTS = [
    # ------------------------------------------------------------ HOOK: the green lights dance over a very sleepy cub (first 5 seconds)
    S("hilltop_lights", (1000, 560, 1760), "Can Poppy stay awake to see the dancing sky? Look! Green lights! But her eyes are so sleepy.", beat="hook", tag="hook: the lights and a sleepy Poppy",
      cam2=(980, 600, 1560), fx=[*DANCE(0.0), ("face", 0.02, "poppy", "sleepy"), ("lookat", 0.02, "poppy", -10), ("face", "w:Look!", "poppy", "wow"), DROOP("w:sleepy.", 2), YAWN("w:eyes")],
      words=[("w:dancing", "DANCING SKY!", .76, .56, .7, "sun"), ("w:sleepy.", "SO SLEEPY!", .76, .7, .75, "pill")]),
    *intro_shots(),      # the main intro, right after the hook
    # ------------------------------------------------------------ GOAL: tonight the sky will dance; Poppy always falls asleep first
    S("arctic_eve", WIDE, "Hello, I'm Milo! Tumble and I are visiting Poppy the polar bear cub, far up north in the snowy Arctic.", trans="iris", beat="goal", tag="arctic at sunset: Milo, Tumble, Poppy",
      cam2=(980, 560, 1820), fx=[("hop", "w:Hello,", "milo"), ("trunk", "w:Tumble", "tumble", -60, .4), ("nod", "w:Poppy", "poppy")],
      words=[("w:Poppy", "POPPY", .6, .3, .7, "pill"), ("w:north", "FAR UP NORTH", .5, .14, .7, "sun")]),
    S("arctic_eve", PH("arctic_eve"), "Tonight, the sky is going to dance! Green lights, way up high!", who="poppy", beat="goal", tag="Poppy: the sky will dance",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "happy"), ("lookat", "w:sky", "poppy", -14), ("nod", "w:Green", "poppy"), ("lookat", "w:high!", "poppy", -18)],
      words=[("w:Green", "GREEN LIGHTS!", .74, .14, .8, "sun")]),
    S("arctic_eve", TH("arctic_eve"), "A dancing sky? Wow! I want to see it too!", who="tumble", beat="goal", tag="Tumble: I want to see it",
      hide=["poppy", "milo"], fx=[("face", 0.02, "tumble", "wow"), ("trunk", "w:Wow!", "tumble", -100, .4), ("face", "w:want", "tumble", "happy"), ("trunk", "w:too!", "tumble", -40, .4)],
      words=[("w:Wow!", "WOW!", .62, .12, .95, "sun")]),
    S("arctic_eve", PH("arctic_eve", 860), "But there is one little problem. I always fall asleep first!", who="poppy", beat="goal", tag="Poppy: I always fall asleep first",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "sad"), ("nod", "w:problem.", "poppy"), ("face", "w:asleep", "poppy", "sleepy"), DROOP("w:first!", 1)],
      words=[("w:asleep", "ASLEEP FIRST!", .74, .14, .8, "pill")]),
    S("arctic_eve", (760, 640, 1500), "Who always falls asleep first? Poppy, or Tumble?", q=True, beat="goal", tag="question: Poppy or Tumble", pause=3.2,
      hide=["milo"], cam2=(760, 660, 1420), fx=[("face", 0.02, "poppy", "sleepy"), DROOP(0.6, 3), ("trunk", 0.4, "tumble", -60, .5), ("signs", "w:Poppy,", ["POPPY", "TUMBLE"], 0, "wait:1.8")]),
    S("paper", (960, 560, 1500), "The northern lights are often seen near the North Pole, far up in the north.", beat="fact", tag="fact: northern lights near the North Pole",
      actors=[PO(560, 880, .62)], props=[prop("gl", A.globe, 1280, 600, .85)],
      fx=[("face", 0.02, "poppy", "happy"), ("lookat", 0.02, "poppy", -8), ("to", "w:northern", "#{p}gl-ring", {"opacity": .4, "duration": .3, "yoyo": True, "repeat": 7}, "the green ring glows"),
          ("to", "w:North", "#{p}gl-arr", {"y": 26, "duration": .3, "yoyo": True, "repeat": 5}, "the arrow points at the North Pole"), ("nod", "w:far", "poppy")],
      words=[("w:northern", "NORTHERN LIGHTS", .4, .3, .6, "sun"), ("w:Pole,", "NORTH POLE", .76, .1, .6, "pill")]),
    S("paper", (980, 580, 1500), "Where are the northern lights often seen? Near the North Pole, or in the jungle?", q=True, beat="fact", tag="question: North Pole or jungle", pause=3.2, cam2=(990, 600, 1420),
      actors=[PO(560, 900, .62)], props=[prop("gl", A.globe, 1280, 640, .8)],
      fx=[("to", 0.4, "#{p}gl-ring", {"opacity": .4, "duration": .3, "yoyo": True, "repeat": 11}, "the green ring glows"), ("signs", "w:North", ["NORTH POLE", "JUNGLE"], 0, "wait:1.8")]),
    S("arctic_eve", (900, 600, 1600), "The sun goes down, and the pink sky turns dark blue. Now the friends wait, and watch.", beat="goal", tag="sunset: they wait and watch",
      cam2=(900, 620, 1500), fx=[("lookat", "w:sun", "poppy", -14), ("trunk", "w:pink", "tumble", -80, .5), ("fly", "w:dark", "milo", 760, 470, 1.6), ("hop", "w:watch.", "milo")],
      words=[("w:wait,", "WAIT AND WATCH", .5, .14, .7, "sun")]),
    S("arctic_eve", MB("arctic_eve", 820, 0, -20), "Let's stay awake together, Poppy. We can do it!", beat="goal", tag="Milo: let's stay awake together",
      hide=["tumble", "poppy"], fx=[("face", 0.02, "milo", "happy"), ("hop", "w:awake", "milo"), ("hop", "w:it!", "milo")], words=[("w:awake", "STAY AWAKE!", .5, .12, .8, "sun")]),
    # ------------------------------------------------------------ OBSTACLE 1: counting the stars (she falls asleep)
    S("arctic_night", WIDE, "Night comes. The stars twinkle in the dark sky. But no lights are dancing yet.", trans="iris", beat="obstacle1", tag="night on the shore: no lights yet",
      cam2=(980, 580, 1780), fx=[("lookat", 0.3, "poppy", -14), ("fly", "w:stars", "milo", 900, 500, 1.6), ("trunk", "w:dark", "tumble", -90, .5), ("face", "w:no", "poppy", "sad")],
      words=[("w:stars", "STARS!", .36, .3, .8, "sun"), ("w:no", "NO LIGHTS YET", .64, .14, .7, "pill")]),
    S("arctic_night", PH("arctic_night"), "I know! I will count the stars. Counting will keep me awake!", who="poppy", beat="obstacle1", tag="Poppy: I will count the stars",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:know!", "poppy"), ("lookat", "w:stars.", "poppy", -18), ("nod", "w:awake!", "poppy")],
      words=[("w:count", "COUNT THE STARS", .26, .62, .6, "sun")]),
    S("arctic_night", (1100, 520, 1500), "Count the stars with Poppy! One, two, three, four, five!", q=True, beat="obstacle1", tag="count five stars", pause=1.0,
      cam2=(1100, 540, 1420), hide=["tumble", "milo"], props=STAR_PROPS(),
      fx=[("face", 0.02, "poppy", "happy"), ("lookat", 0.02, "poppy", -20), ("count", "w:One,", 5, CNT5, {"x": 400, "y": 560}),
          POP("w:One,", 0), POP("w:two,", 1), POP("w:three,", 2), POP("w:four,", 3), POP("w:five!", 4)],
      words=[("w:Count", "COUNT!", .78, .7, .8, "sun")]),
    S("arctic_night", (1060, 680, 1300), "Poppy counts, and counts. Her eyes get heavy. She lies down, and she falls asleep!", beat="obstacle1", tag="Poppy falls asleep counting",
      cam2=(1080, 700, 1200), actors=[PB(1180, 900, f=True)], props=[Z(*ZA, .8, True)],
      fx=[("face", 0.02, "poppy", "sleepy"), ("lookat", 0.02, "poppy", -14), DROOP("w:heavy.", 2), YAWN("w:eyes"), SLEEP("w:asleep!"), FADEIN("w:asleep!", "#{p}zz_w", "Z's float up"), ZFLOAT("w:asleep!")],
      words=[("w:heavy.", "HEAVY EYES", .44, .16, .75, "pill"), ("w:asleep!", "ASLEEP!", .8, .32, .85, "sun")]),
    S("arctic_night", (1000, 700, 1600), "Is Poppy awake, or asleep?", q=True, beat="obstacle1", tag="question: awake or asleep", pause=3.2, cam2=(1000, 700, 1500),
      actors=[TU(460, 900), PB(1180, 900, f=True)], props=[Z(*ZA)], fx=[*ASLEEP, ZFLOAT(0.1), ("lookat", 0.4, "tumble", 6), ("signs", "w:awake,", ["AWAKE", "ASLEEP"], 1, "wait:1.8")]),
    S("arctic_night", (800, 660, 1400), "Poppy? Wake up, Poppy. The lights are not here yet.", who="tumble", beat="obstacle1", tag="Tumble wakes her gently",
      cam2=(820, 660, 1320), actors=[TU(520, 900), PB(1180, 900, f=True)], props=[Z(*ZA)],
      fx=[*ASLEEP, ZFLOAT(0.1), ("face", 0.02, "tumble", "happy"), ("trunk", "w:Wake", "tumble", -30, .4), ("hide", "w:up,", "zz"), *WAKE("w:up,"), ("face", "w:lights", "poppy", "wow")],
      words=[("w:Wake", "WAKE UP!", .5, .14, .8, "sun")]),
    S("arctic_night", PH("arctic_night", 820, -40, 60, stage=[PB(1180, 900, f=True)]), "Oh! I fell asleep. Counting stars is too sleepy for me.", who="poppy", beat="obstacle1", tag="Poppy: counting is too sleepy",
      actors=[PB(1180, 900, f=True)], fx=[("face", 0.02, "poppy", "wow"), ("face", "w:Counting", "poppy", "sad"), ("nod", "w:sleepy", "poppy")],
      words=[("w:sleepy", "TOO SLEEPY!", .27, .62, .7, "pill")]),
    # ------------------------------------------------------------ OBSTACLE 2: a bouncy dance in the snow (she gets tired and falls asleep)
    S("snow_night", WIDE, "Then Poppy has a new idea. A bouncy dance in the snow!", trans="iris", beat="obstacle2", tag="the snow at night: a bouncy dance",
      cam2=(980, 580, 1780), fx=[("hop", "w:idea.", "poppy"), ("hop", "w:bouncy", "poppy", 2), ("trunk", "w:dance", "tumble", -100, .4), ("hop", "w:snow!", "milo")],
      words=[("w:bouncy", "A BOUNCY DANCE!", .5, .14, .75, "sun")]),
    S("snow_night", (1110, 660, 1540), "Can you hop, like Poppy? Hop, hop, hop!", q=True, beat="obstacle2", tag="copy me: hop", pause=3.0, cam2=(1110, 680, 1480),
      fx=[("face", 0.02, "poppy", "happy"), ("hop", "w:Hop,", "poppy", 3), ("hop", "w:hop,:2", "tumble"), ("hop", "w:hop!", "milo"), ("hop", "wait:0.4", "poppy", 3), ("hop", "wait:1.4", "tumble", 2)],
      words=[("w:Hop,", "HOP, HOP, HOP!", .42, .14, .8, "sun"), ("wait:0.4", "YOUR TURN!", .42, .28, .7, "pill")]),
    S("snow_night", (920, 680, 1300), "Poppy hops, and hops, and hops. Now she is tired. She lies down to rest, and she falls asleep!", beat="obstacle2", tag="Poppy is tired and falls asleep",
      cam2=(920, 700, 1220), actors=[PO(900, 935), ("poppy2", "bear_belly", 900, 935, .6, False)], props=[Z(*ZS, .8, True)],
      fx=[("to", 0.0, "#{p}poppy2_w", {"opacity": 0, "duration": .01}, ""), ("hop", "w:Poppy", "poppy", 3), ("face", "w:tired.", "poppy", "sleepy"), YAWN("w:tired."),
          ("to", "w:lies", "#{p}poppy_w", {"opacity": 0, "duration": .3}, "Poppy lies down"), ("to", "w:lies", "#{p}poppy2_w", {"opacity": 1, "duration": .3}, ""),
          ("face", "w:lies", "poppy2", "sleepy"), ("sleep", "w:asleep!", "poppy2"), FADEIN("w:asleep!", "#{p}zz_w", "Z's float up"), ZFLOAT("w:asleep!")],
      words=[("w:tired.", "TIRED!", .7, .16, .85, "pill"), ("w:asleep!", "ASLEEP AGAIN!", .5, .3, .7, "sun")]),
    S("snow_night", (940, 680, 1500), "Did the bouncy dance keep Poppy awake? Yes, or no?", q=True, beat="obstacle2", tag="question: did the dance keep her awake", pause=3.2, cam2=(960, 700, 1400),
      actors=[PB(900, 935), MI(1380, 700)], props=[Z(*ZS)], fx=[*ASLEEP, ZFLOAT(0.1), ("signs", "w:Yes,", ["YES", "NO"], 1, "wait:1.8")]),
    S("snow_night", (1040, 660, 1300), "Milo flies down, and taps her nose. Poppy, wake up, sleepy bear!", beat="obstacle2", tag="Milo wakes her gently",
      cam2=(1040, 680, 1220), actors=[PB(900, 935), MI(1400, 520)], props=[Z(*ZS)],
      fx=[*ASLEEP, ZFLOAT(0.1), ("fly", "w:flies", "milo", 1330, 780, 1.4), ("hop", "w:taps", "milo"), ("hide", "w:wake", "zz"), *WAKE("w:wake"), ("face", "w:sleepy", "poppy", "happy")],
      words=[("w:taps", "TAP, TAP!", .76, .16, .8, "sun"), ("w:wake", "WAKE UP!", .4, .3, .8, "pill")]),
    S("snow_night", PH("snow_night", 820, 40, 60, stage=[PB(900, 935)]), "Oh no! Dancing made me tired. I fell asleep again!", who="poppy", beat="obstacle2", tag="Poppy: dancing made me tired",
      actors=[PB(900, 935)], fx=[("face", 0.02, "poppy", "wow"), ("face", "w:Dancing", "poppy", "sad"), ("nod", "w:again!", "poppy")],
      words=[("w:again!", "AGAIN!", .74, .14, .9, "pill")]),
    # ------------------------------------------------------------ OBSTACLE 3: a walk up the snowy hill (she sits down at the top and falls asleep)
    S("hilltop_night", WIDE, "Next, the friends walk up the snowy hill, to see the sky up close.", trans="iris", beat="obstacle3", tag="the hilltop at night: a walk",
      cam2=(980, 580, 1780), actors=[TU(80, 880), PO(560, 880, .62), MI(900, 560)],
      fx=[("walk", 0.1, "poppy", 260, 3.6), ("walk", 0.3, "tumble", 220, 3.4), ("fly", 0.6, "milo", 1180, 600, 3.0), ("lookat", "w:sky", "poppy", -16)],
      words=[("w:hill,", "UP THE HILL", .66, .16, .75, "sun")]),
    S("hilltop_night", PH("hilltop_night", 820, 40, 40), "A walk will keep me awake! Step, step, step.", who="poppy", beat="obstacle3", tag="Poppy: a walk will keep me awake",
      hide=["tumble", "milo"], fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:walk", "poppy"), ("nod", "w:Step,", "poppy"), ("nod", "w:step.", "poppy")],
      words=[("w:Step,", "STEP, STEP!", .74, .14, .8, "sun")]),
    S("hilltop_night", (900, 640, 1500), "But the hill is long, and Poppy is slow. At the top, she sits down, and falls asleep!", beat="obstacle3", tag="at the top Poppy falls asleep",
      cam2=(900, 660, 1420), actors=[PO(560, 880, .62), ("poppy2", "bear_belly", 820, 880, .62, False)], hide=["tumble", "milo"], props=[Z(*ZH, .8, True)],
      fx=[("to", 0.0, "#{p}poppy2_w", {"opacity": 0, "duration": .01}, ""), ("walk", 0.2, "poppy", 260, 3.4), ("face", "w:slow.", "poppy", "sleepy"), YAWN("w:slow."),
          ("to", "w:sits", "#{p}poppy_w", {"opacity": 0, "duration": .3}, "Poppy lies down"), ("to", "w:sits", "#{p}poppy2_w", {"opacity": 1, "duration": .3}, ""),
          ("face", "w:sits", "poppy2", "sleepy"), ("sleep", "w:asleep!", "poppy2"), FADEIN("w:asleep!", "#{p}zz_w", "Z's float up"), ZFLOAT("w:asleep!")],
      words=[("w:long,", "SO LONG!", .4, .16, .8, "pill"), ("w:asleep!", "ASLEEP!", .4, .3, .85, "sun")]),
    S("hilltop_night", (860, 620, 1500), "What did Poppy do at the top of the hill? Sleep, or fly?", q=True, beat="obstacle3", tag="question: sleep or fly", pause=3.2, cam2=(880, 640, 1400),
      actors=[PB(820, 880, .62)], props=[Z(*ZH)], fx=[*ASLEEP, ZFLOAT(0.1), ("signs", "w:Sleep,", ["SLEEP", "FLY"], 0, "wait:1.8")]),
    S("hilltop_night", (700, 640, 1400), "Wake up, Poppy! There are no lights yet. But we are here.", who="tumble", beat="obstacle3", tag="Tumble wakes her again",
      cam2=(720, 660, 1320), actors=[TU(280, 880), PB(820, 880, .62)], props=[Z(*ZH)],
      fx=[*ASLEEP, ZFLOAT(0.1), ("face", 0.02, "tumble", "happy"), ("trunk", "w:Wake", "tumble", -30, .4), ("hide", "w:Poppy!", "zz"), *WAKE("w:Poppy!"), ("trunk", "w:here.", "tumble", -80, .4)],
      words=[("w:no", "NO LIGHTS YET", .5, .14, .75, "pill")]),
    # ------------------------------------------------------------ LOW MOMENT: maybe I will never see it (gentle: nobody cries)
    S("hilltop_night", (860, 600, 1600), "Poppy looks up at the dark, quiet sky. She feels a little sad.", beat="low", tag="Poppy looks at the dark sky, a little sad",
      cam2=(860, 620, 1500), actors=[TU(280, 880), PB(820, 880, .62), MI(1180, 620)],
      fx=[("face", 0.02, "poppy", "sad"), ("lookat", "w:looks", "poppy", -16), ("face", "w:sad.", "tumble", "sad"), ("lookat", "w:sad.", "poppy", 6)],
      words=[("w:quiet", "DARK AND QUIET", .5, .14, .7, "sun"), ("w:sad.", "A LITTLE SAD", .66, .3, .7, "pill")]),
    S("hilltop_night", PH("hilltop_night", 760, 40, 60, stage=[PB(820, 880, .62)]), "I always fall asleep first. Maybe I will never see the dancing sky.", who="poppy", beat="low", tag="Poppy: maybe I will never see it",
      actors=[PB(820, 880, .62)], fx=[("face", 0.02, "poppy", "sad"), ("lookat", "w:Maybe", "poppy", 10), ("nod", "w:never", "poppy")],
      words=[("w:never", "NEVER?", .76, .14, .9, "pill")]),
    S("hilltop_night", (700, 600, 1500), "It's okay, Poppy. We are right here with you.", who="tumble", beat="low", tag="Tumble: we are right here",
      cam2=(720, 620, 1420), actors=[TU(280, 880), PB(820, 880, .62), MI(1180, 620)],
      fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:okay,", "tumble", -40, .5), ("fly", "w:right", "milo", 1100, 640, 1.0), ("face", "w:here", "poppy", "happy")],
      words=[("w:right", "RIGHT HERE", .5, .14, .8, "sun")]),
    S("hilltop_night", (900, 640, 1300), "How does Poppy feel now? Sad, or happy?", q=True, beat="low", tag="question: sad or happy", pause=3.2, cam2=(900, 660, 1220),
      actors=[PB(820, 880, .62)], fx=[("face", 0.02, "poppy", "sad"), ("lookat", 0.4, "poppy", 8), ("signs", "w:Sad,", ["SAD", "HAPPY"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ SOLUTION: Poppy's own idea: take turns
    S("hilltop_night", (820, 620, 1300), "Then Poppy looks at her two good friends. And she has an idea!", beat="solution", tag="Poppy has an idea",
      cam2=(820, 640, 1220), actors=[TU(430, 880), PB(820, 880, .62), MI(1180, 620)], props=[prop("tb", A13.think_bulb, 990, 520, .6, True)],
      fx=[("face", 0.02, "poppy", "sad"), ("lookat", "w:looks", "poppy", 4), ("face", "w:idea!", "poppy", "happy"), ("show", "w:idea!", "tb"), ("hop", "e:idea!", "milo")],
      words=[("w:idea!", "AN IDEA!", .46, .2, .85, "sun")]),
    S("hilltop_night", PH("hilltop_night", 860, 40, 60, stage=[PB(820, 880, .62)]), "We can take turns! I sleep first. You watch the sky. When the lights come, wake me up!", who="poppy", beat="solution",
      tag="Poppy: we can take turns", actors=[PB(820, 880, .62)],
      fx=[("face", 0.02, "poppy", "happy"), ("nod", "w:turns!", "poppy"), ("lookat", "w:watch", "poppy", -14), ("lookat", "w:wake", "poppy", 0), ("nod", "w:up!", "poppy")],
      words=[("w:turns!", "TAKE TURNS!", .74, .12, .85, "sun"), ("w:wake", "WAKE ME UP", .74, .26, .7, "pill")]),
    S("hilltop_night", C("hilltop_night", "tumble", "all", 1200, 0, -60, stage=[TU(280, 880)]), "Yes! I will watch first. Then Milo will watch. And we will wake you up, gently.", who="tumble", beat="solution", tag="Tumble: I will watch first",
      actors=[TU(280, 880)], fx=[("face", 0.02, "tumble", "happy"), ("trunk", "w:Yes!", "tumble", -100, .4), ("trunk", "w:Milo", "tumble", -40, .4), ("trunk", "w:gently.", "tumble", -70, .5)],
      words=[("w:first.", "TUMBLE FIRST", .5, .1, .7, "sun"), ("w:Milo", "THEN MILO", .5, .22, .7, "pill")]),
    S("hilltop_night", (820, 640, 1560), "What is Poppy's idea? Take turns, or go home?", q=True, beat="solution", tag="question: take turns or go home", pause=3.2, cam2=(830, 660, 1480),
      actors=[TU(360, 880), PB(820, 880, .62), MI(1180, 620)], fx=[("face", 0.02, "poppy", "happy"), ("hop", 0.4, "milo"), ("signs", "w:Take", ["TAKE TURNS", "GO HOME"], 0, "wait:1.8")]),
    S("nest_night", WIDE, "So Poppy curls up in a cozy snow nest, and closes her eyes. Tumble watches the sky.", trans="iris", beat="solution", tag="the snow nest: Poppy sleeps, Tumble watches",
      cam2=(960, 580, 1780), props=[Z(*ZN, .8, True)],
      fx=[("face", 0.02, "poppy", "sleepy"), YAWN("w:curls"), ("sleep", "w:closes", "poppy"), FADEIN("e:eyes,", "#{p}zz_w", "Z's float up"), ZFLOAT("e:eyes,"),
          ("lookat", "w:watches", "tumble", -12), ("trunk", "w:sky.", "tumble", -90, .5)],
      words=[("w:cozy", "A COZY NEST", .5, .14, .75, "sun"), ("w:watches", "TUMBLE WATCHES", .24, .3, .6, "pill")]),
    S("paper_blue", (960, 560, 1500), "Northern lights are best seen at night, when the sky is dark. Big clouds can hide them.", beat="fact", tag="fact: best seen at night, clouds hide them",
      props=[prop("nc", A.night_card, 560, 540, 1.0), prop("sc", A.sun_card, 1380, 540, .7, True), prop("cc", A.cloud_card, 1380, 540, 1.0, True)],
      fx=[RIB(0.1, "nc"), ("show", "w:night,", "sc"), ("to", "w:dark.", "#{p}sc_w", {"opacity": 0, "duration": .3}, "the day picture goes"), ("show", "w:clouds", "cc"),
          ("fromto", "w:clouds", "#{p}cc-cl", {"x": -320}, {"x": 0, "duration": 1.0, "ease": "sine.out"}, "a cloud slides over the lights")],
      words=[("w:night,", "AT NIGHT", .3, .8, .7, "sun"), ("w:clouds", "CLOUDS HIDE THEM", .72, .8, .55, "pill")]),
    S("paper_blue", (980, 580, 1500), "When are northern lights best seen? In the day, or at night?", q=True, beat="fact", tag="question: day or night", pause=3.2, cam2=(990, 600, 1420),
      props=[prop("sc", A.sun_card, 600, 600, .8), prop("nc", A.night_card, 1340, 600, .8)], fx=[RIB(0.4, "nc"), ("signs", "w:day,", ["DAY", "NIGHT"], 1, "wait:1.8")]),
    S("nest_night", (800, 660, 1500), "Tumble watches, and watches. Then it is Milo's turn. Milo watches the sky.", beat="solution", tag="Tumble's turn, then Milo's",
      cam2=NCAM, props=[Z(*ZN)],
      fx=[*ASLEEP, ZFLOAT(0.1), ("lookat", 0.3, "tumble", -12), ("face", "w:turn.", "tumble", "sleepy"), ("fly", "w:Milo's", "milo", 1240, 520, 1.6), ("hop", "e:sky.", "milo")],
      words=[("w:Milo's", "MILO'S TURN", .5, .14, .75, "sun")]),
    S("nest_night", (880, 600, 1700), "And then, look! Green lights! The sky begins to dance!", beat="solution", tag="the lights come", cam2=(880, 620, 1660),
      actors=[TU(290, 920), PB(820, 920), MI(1240, 520)], props=[Z(*ZN)],
      fx=[*ASLEEP, ZFLOAT(0.1), LIGHTS_ON("w:look!"), *DANCE("w:look!"), ("face", "w:Green", "milo", "wow"), ("hop", "w:dance!", "milo"), ("face", "w:dance!", "tumble", "wow")],
      words=[("w:Green", "GREEN LIGHTS!", .5, .14, .8, "sun")]),
    S("nest_lights", NCAM, "What is in the sky? Green lights, or a rainbow?", q=True, beat="solution", tag="question: lights or rainbow", pause=3.2, cam2=(870, 650, 1620),
      actors=NEST, props=[Z(*ZN)], fx=[*ASLEEP, ZFLOAT(0.1), *DANCE(0.0), ("face", 0.02, "milo", "wow"), ("signs", "w:Green", ["GREEN LIGHTS", "RAINBOW"], 0, "wait:1.8")]),
    S("nest_lights", (960, 700, 1200), "Poppy, wake up! Gently, gently. The sky is dancing!", beat="solution", tag="Milo wakes Poppy gently",
      cam2=(960, 700, 1120), actors=[PB(820, 920), MI(1300, 560)], props=[Z(*ZN)],
      fx=[*ASLEEP, ZFLOAT(0.1), *DANCE(0.0), ("fly", 0.2, "milo", 1220, 680, 1.2), ("hop", "w:Gently,", "milo"), ("hide", "w:gently.", "zz"), *WAKE("w:gently."), ("face", "w:dancing!", "poppy", "wow")],
      words=[("w:wake", "WAKE UP!", .4, .2, .85, "sun")]),
    S("nest_lights", (960, 620, 1500), "Oh! The dancing sky! It is so beautiful!", who="poppy", beat="solution", tag="Poppy: the dancing sky!",
      cam2=(960, 590, 1420), actors=[PB(820, 920)], fx=[*DANCE(0.0), ("face", 0.02, "poppy", "wow"), ("lookat", 0.3, "poppy", -18), ("face", "w:beautiful!", "poppy", "happy")],
      words=[("w:beautiful!", "SO BEAUTIFUL!", .74, .5, .75, "sun")]),
    S("paper_pink", (960, 560, 1500), "Most northern lights are green. Some are pink, or purple. They ripple and move across the sky, like a waving curtain.", beat="fact",
      tag="fact: mostly green, they ripple like a curtain", props=[prop("nc", A.night_card, 620, 560, 1.0), prop("co", A.colors, 1360, 400, .9)],
      fx=[RIB(0.1, "nc"), ("to", "w:green.", "#{p}co_w", {"scale": 1.1, "duration": .25, "yoyo": True, "repeat": 1}, "the green dot pulses"),
          ("to", "w:ripple", "#{p}nc-rib", {"skewX": -14, "x": "-=30", "duration": .5, "yoyo": True, "repeat": 9, "ease": "sine.inOut"}, "the lights ripple")],
      words=[("w:green.", "GREEN!", .7, .58, .9, "sun"), ("w:ripple", "RIPPLE AND MOVE", .7, .76, .6, "pill")]),
    S("paper_pink", (980, 580, 1500), "What color are most northern lights? Green, or orange?", q=True, beat="fact", tag="question: green or orange", pause=3.2, cam2=(990, 600, 1420),
      props=[prop("nc", A.night_card, 960, 640, 1.1)], fx=[RIB(0.3, "nc"), ("signs", "w:Green,", ["GREEN", "ORANGE"], 0, "wait:1.8")]),
    S("nest_lights", NCAM, "Can you sway, like the dancing sky? Sway, sway, sway!", q=True, beat="solution", tag="copy me: sway", pause=3.0, cam2=(870, 650, 1620), actors=NEST,
      fx=[*DANCE(0.0, 1.3), ("face", 0.02, "poppy", "happy"),
          ("to", "w:Sway,", "#{p}poppy", {"rotation": 5, "transformOrigin": "50% 100%", "duration": .5, "yoyo": True, "repeat": 9, "ease": "sine.inOut"}, "Poppy sways"),
          ("to", "w:sway,:2", "#{p}tumble", {"rotation": -4, "transformOrigin": "50% 100%", "duration": .5, "yoyo": True, "repeat": 9, "ease": "sine.inOut"}, "Tumble sways"), ("hop", "w:sway!", "milo")],
      words=[("w:Sway,", "SWAY, SWAY!", .5, .14, .8, "sun"), ("wait:0.4", "YOUR TURN!", .5, .28, .65, "pill")]),
    # ------------------------------------------------------------ the song moment: Poppy SAYS the rhyme, then the tune on instruments
    S("nest_lights", (860, 660, 1520), "Green lights dancing, way up high. Take turns, friends, and watch the sky!", who="poppy", beat="solution", tag="the dancing sky rhyme", cam2=(880, 650, 1640),
      actors=NEST, fx=[*DANCE(0.0), ("face", 0.02, "poppy", "happy"), ("nod", "w:Green", "poppy"), ("trunk", "w:Take", "tumble", -90, .4), ("hop", "w:friends,", "milo"), ("nod", "w:sky!", "poppy")],
      words=[("w:Green", "GREEN LIGHTS DANCING", .5, .14, .6, "sun"), ("w:Take", "TAKE TURNS!", .5, .27, .65, "pill")]),
    S("nest_lights", (840, 600, 1720), who="", sing=SING_SKY, beat="song", tag="song: the dancing sky", cam2=(840, 620, 1600), actors=NEST,
      fx=[*DANCE(0.0, 96 / 60 * 1.25 / 2), ("face", 0.02, "poppy", "happy"), ("face", 0.02, "tumble", "happy"),
          ("to", TB(0), "#{p}poppy", {"rotation": 4, "transformOrigin": "50% 100%", "duration": 60 / 96, "yoyo": True, "repeat": 15, "ease": "sine.inOut"}, "Poppy sways to the beat"),
          ("trunk", TB(2), "tumble", -100, .4), ("hop", TB(4), "milo"), ("trunk", TB(6), "tumble", -40, .4), ("hop", TB(8), "milo"), ("trunk", TB(10), "tumble", -100, .4), ("hop", TB(12), "milo"),
          ("word", TB(0), "GREEN LIGHTS DANCING", {"x": 840, "y": 300, "size": 76, "cls": "sun", "hold": 4.4})],
      words=[(TB(8), "WATCH THE SKY!", .5, .2, .7, "pill")]),
    S("nest_lights", (900, 680, 1300), "Did Poppy see the dancing sky? Yes, or no?", q=True, beat="solution", tag="question: did she see it yes or no", pause=3.2, cam2=(900, 660, 1240),
      actors=[PB(820, 920), MI(1320, 760)], fx=[*DANCE(0.0), ("face", 0.02, "poppy", "happy"), ("hop", 0.4, "milo"), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:1.8")]),
    # ------------------------------------------------------------ WARM ENDING: watching together, thank-yous
    S("hilltop_lights", (900, 560, 1800), "The lights dance, and dance, over the snowy hill. The three friends watch together, snuggled up close.", trans="iris", beat="ending", tag="the three friends watch together",
      cam2=(880, 600, 1600), actors=[TU(330, 880), PB(820, 880, .62), MI(1180, 640)],
      fx=[*DANCE(0.0), ("face", 0.02, "poppy", "happy"), ("face", 0.02, "tumble", "happy"), ("lookat", 0.3, "poppy", -16), ("trunk", "w:friends", "tumble", -90, .5), ("hop", "w:together,", "milo")],
      words=[("w:together,", "TOGETHER!", .5, .24, .85, "sun")]),
    S("hilltop_lights", PH("hilltop_lights", 860, 40, 60, stage=[PB(820, 880, .62)]), "Thank you, Tumble! Thank you, Milo! You watched the sky for me.", who="poppy", beat="ending", tag="Poppy: thank you",
      actors=[PB(820, 880, .62)], fx=[*DANCE(0.0), ("face", 0.02, "poppy", "happy"), ("nod", "w:Tumble!", "poppy"), ("nod", "w:Milo!", "poppy")],
      words=[("w:Thank", "THANK YOU!", .74, .14, .85, "sun")]),
    S("hilltop_lights", C("hilltop_lights", "tumble", "all", 1200, 0, -60, stage=[TU(330, 880)]), "And you had the best idea, Poppy. Taking turns!", who="tumble", beat="ending", tag="Tumble: the best idea",
      actors=[TU(330, 880)], fx=[*DANCE(0.0), ("face", 0.02, "tumble", "happy"), ("trunk", "w:best", "tumble", -100, .4), ("trunk", "w:turns!", "tumble", -40, .4)],
      words=[("w:turns!", "TAKING TURNS!", .5, .14, .75, "pill")]),
    S("hilltop_lights", MB("hilltop_lights", 820, 0, -40, stage=[MI(1180, 640)]), "When something is hard to do alone, good friends can take turns, and help.", beat="ending", tag="the lesson",
      actors=[MI(1180, 640)], fx=[*DANCE(0.0), ("hop", "w:hard", "milo"), ("hop", "w:turns,", "milo"), ("hop", "w:help.", "milo")],
      words=[("w:turns,", "TAKE TURNS!", .5, .14, .85, "sun")]),
    S("hilltop_lights", (840, 620, 1600), "Do you remember? Where are northern lights often seen? Near the North Pole, or at the beach?", q=True, beat="ending", tag="question: North Pole or beach", pause=3.2,
      cam2=(850, 640, 1500), actors=[TU(330, 880), PB(820, 880, .62), MI(1180, 680)], fx=[*DANCE(0.0), ("hop", "w:remember?", "milo"), ("signs", "w:North", ["NORTH POLE", "BEACH"], 0, "wait:1.8")]),
    S("hilltop_lights", (800, 660, 1460), "And when are they best seen? On a sunny day, or on a dark night?", q=True, beat="ending", tag="question: sunny day or dark night", pause=3.2,
      cam2=(810, 670, 1380), actors=[TU(330, 880), PB(820, 880, .62), MI(1200, 770)], fx=[*DANCE(0.0), ("nod", "w:best", "poppy"), ("signs", "w:sunny", ["SUNNY DAY", "DARK NIGHT"], 1, "wait:1.8")]),
    S("hilltop_lights", (880, 560, 1840), "Green lights dancing, way up high. Take turns, friends, and watch the sky!", beat="ending", tag="the closing rhyme", cam2=(880, 590, 1680),
      actors=[TU(330, 880), PB(820, 880, .62), MI(1180, 640)], fx=[*DANCE(0.0), ("hop", "w:Green", "milo"), ("trunk", "w:Take", "tumble", -90, .4), ("nod", "w:sky!", "poppy")],
      words=[("w:Green", "GREEN LIGHTS DANCING", .5, .14, .5, "sun"), ("w:Take", "TAKE TURNS!", .5, .25, .55, "pill")]),
    S("nest_lights", (860, 660, 1540), who="", sing=SING_END, beat="song", tag="song: hooray", cam2=(880, 650, 1640), actors=NEST,
      fx=[*DANCE(0.0), ("hop", 1.0, "milo"), ("trunk", 1.6, "tumble", -100, .4), ("nod", 2.2, "poppy"), ("face", 0.02, "poppy", "happy")],
      words=[(TB(3), "HOORAY!", .5, .16, .9, "sun")]),
    S("nest_lights", MB("nest_lights", 820, 0, -40, stage=[MI(1380, 680)]), "Next time: Milo and the Deep Blue Sea! See you on the next adventure, friends!", beat="ending", tag="goodbye: next adventure",
      actors=[MI(1380, 680)], fx=[*DANCE(0.0), ("hop", "w:next", "milo")], words=[("w:Next", "NEXT TIME!", .5, .1, .62, "sun"), ("w:See", "SEE YOU SOON!", .5, .22, .5, "pill")]),
    *intro_shots(),      # and again as the last shots: the video ends on the logo with the whole cast
]

# thumbnail (thumb.py): the promise of the first shot: green lights over a very sleepy cub; 2 words, none of the title's words, no watermark
THUMBS = {
    "za_ep14": {"place": "hilltop_lights", "cam": (1000, 560, 1400),
                "actors": [("bear_belly", 900, 880, 1.0, False, "gsap.set('#P-eye-lid',{opacity:1});gsap.set('#P-neck',{rotation:7,svgOrigin:'190 -330'});")],
                "props": [(A.zzz, 1240, 440, 1.2)],
                "words": [("WAKE UP!", 640, 300, 170, "sun", -5)]},
}
