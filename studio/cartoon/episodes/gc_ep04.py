"""gc_ep04: "How Does Your Heart Work?" - Gizmo Explains cartoon explainer (catch-up run A, Nov 28 2026, session_014CFVfXs8xfsEZKF885Z161).
Gizmo hosts in his lab, at his bench, at the window at night, in the sunny park, in the flower meadow and over the green hills ("beat" process).
Gizmo is a robot: he has no heart, the viewer does. Three parts, each cut whole into one Short:
1. your heart is a muscle, about the size of your fist, in your chest a little to the left of the middle; it pumps blood all day and all night,
2. blood gives your body oxygen and nutrients; the heart sends blood to the lungs to pick up oxygen, then all around the body; blood vessels take
   blood away from the heart and bring it back, over and over again,
3. the heartbeat sound (lub, dub) is little doors inside the heart (valves) closing; the heart has four rooms (chambers), two on top and two on the
   bottom; when you exercise the heart pumps faster so your muscles get more oxygen; running and swimming help keep the heart healthy.

FACTS, read at the source on Nov 28 2026 (pages fetched in this session by the page reader; quotes copied from the page text, under 125 characters):
 [KIDS] KidsHealth (Nemours) for kids, "Your Heart & Circulatory System" (akronchildrens.org/kidshealth/en/kids/heart.html; the kids article, verbatim part):
   "Your heart is really a muscle."
   "It's located a little to the left of the middle of your chest, and it's about the size of your fist."
   "It pumps blood around your body."   "Blood provides your body with the oxygen and nutrients it needs."
   "Blood delivers oxygen to all the body's cells."   "Your heart does this all day and all night, all the time."
   "The heart is made up of four different blood-filled areas, and each of these areas is called a chamber."
   "...a fresh breath of oxygen that can enter the blood to start the process again."
 [PAR] KidsHealth (Nemours) for parents, "Heart & Circulatory System" (kidshealth.org/en/parents/circulatory-system.html, reviewed Nov 2025):
   "With each heartbeat, the heart sends blood throughout your body, carrying oxygen to every cell."
   "At the lungs, the blood picks up oxygen and drops off carbon dioxide."   "The heart then sends the blood to the lungs to pick up more oxygen."
   "Arteries carry blood away from the heart, and veins carry blood back to the heart."   "This cycle repeats over and over again."
   "when you're sleeping, it pumps just enough to provide for the lower amounts of oxygen your body needs when resting."
   "During systole, the atrioventricular valves close, creating the first sound — the lub — of a heartbeat."
   "These valves closing is what creates the second sound — the dub — of a heartbeat."
   "The heart has four chambers — two on the top and two on the bottom:"
   "But when you're exercising, the heart pumps faster so that your muscles get more oxygen and can work harder."
   "To keep your heart healthy, it's important to follow healthy habits, such as:" / "getting plenty of intense physical activity (like running or swimming)"
 Said as: your heart is a muscle; it is about the size of your fist; it is in your chest, a little to the left of the middle; it pumps blood around
 your body, all day and all night, all the time, even when you sleep; blood gives your body oxygen and good things from food (nutrients); the
 oxygen comes in with the air you breathe; the heart sends blood to the lungs, where it picks up oxygen; then it sends it all around the body;
 blood vessels take blood away from the heart and bring it back, over and over again; the heartbeat sound, lub, dub, is little doors inside the
 heart (valves) closing; the heart has four rooms (chambers), two on top and two on the bottom; when you run and play the heart pumps faster, so
 your muscles get more oxygen; running and swimming help keep your heart healthy.
 Taken out (not read verbatim today: that part of the kids page came back only as a summary): where to feel your pulse (neck, wrist), beats per
 minute. Pictures that are ours, not facts: the heart's face, squeezing a fist "like" the heart pumps, the arrows of the blood's way, the doors
 drawn as flaps, the heartbeat line. Nothing a child could copy unsafely: the only actions are a hand on the chest, a fist, breathing, hopping in place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_gizmo as G
import art_gc_ep03 as R
import art_gc_ep04 as A
from kit import Kit, S, prop, W
from intro_gizmo import GZ_INTRO_STAGES, gz_intro_shots      # Gizmo's main intro (owner, Nov 21 2026 12:18 PM: "amazing emplement on every new video")
from episodes.gc_ep01 import WAVE, IDEA, ARMS, UP, DOWN, WIDEARMS, CURL, HOP, PULSE, OFF, ON

BOILER = ("Gizmo Explains makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 4-8. "
          "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.")
SRC = ("WHERE THE FACTS COME FROM\nKidsHealth from Nemours: Your Heart and Circulatory System (for kids) and Heart and Circulatory System (for parents).")
EP = {"id": "gc_ep04", "nest": True, "beat": True, "voice": "am_michael", "speed": 0.85, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0, "wm": "brand/gizmo",      # Gizmo's OWN main intro (intro_gizmo.py): after the hook and as the last four shots
      "cast": {"gizmo": {"voice": "am_michael", "speed": 0.85}},
      "title": "How Does Your Heart Work? Gizmo Explains", "thumb_text": "THUMP!", "series": "Gizmo Explains",
      "description": ("How does your heart work? Gizmo the robot has no heart, but you do! He shows where your heart is, how big it is, where it sends your "
                      "blood, what makes the heartbeat sound and why it beats faster when you run and play. A gentle science lesson for ages 4-8 with "
                      "questions to answer, things to try and a quiz at the end.\n"
                      "Kids learn that the heart is a muscle about the size of their fist, in the chest a little to the left of the middle; that it pumps "
                      "blood all day and all night; that blood picks up oxygen in the lungs and carries it all around the body, then comes back to the heart; "
                      "that the lub-dub sound is little doors inside the heart (valves) closing; that the heart has four rooms (chambers); and that the "
                      "heart pumps faster when we exercise, so our muscles get more oxygen.\n\n"
                      + BOILER + "\n\n" + SRC),
      "tags": ["how does your heart work", "heart for kids", "human body for kids", "heartbeat for kids", "blood for kids", "lungs for kids",
               "science for kids", "body science for kids", "Gizmo Explains", "Gizmo the robot", "preschool science", "kindergarten science"]}

GX, GY, GS = 700, 900, .7
STAGES = {"glab": [("gizmo", "gizmo", GX, GY, GS)],
          "gbench": [("gizmo", "gizmo", 520, 860, .66)],
          "gwindow": [("gizmo", "gizmo", 560, 900, .66)],    # never in the picture (hidden in every gwindow shot: the night prop is drawn in front)
          "gpark": [("gizmo", "gizmo", 560, 960, .6)],
          "gmeadow": [("gizmo", "gizmo", 760, 980, .62)],
          "ghills": [("gizmo", "gizmo", 300, 760, .5)], **GZ_INTRO_STAGES}     # never in the picture (hidden in every ghills shot)
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
GQ = lambda place: WV(place, ["gizmo"], floor=.70, top=.46)
GP = lambda place: WV(place, ["gizmo"], floor=.72, top=.42)
GPL = lambda place: WV(place, ["gizmo"], floor=.62, top=.42)        # Gizmo smaller: room for a word under him
GCAM = lambda place, w=1000: C(place, "gizmo", "all", w)


# ------------------------------------------------------------------ moves of the heart and the blood (one beat = 0.625 s at 96 bpm)
def BEAT(at, sel, n=3, fast=False, what="the heart squeezes and relaxes"):
    d = .156 if fast else .3125
    return ("to", at, sel + "-sq", {"scale": .86, "transformOrigin": "50% 50%", "duration": d, "yoyo": True, "repeat": 2 * n - 1, "ease": "sine.inOut"}, what)
def GLOW(at, sel, what="a soft light around the heart"): return ("to", at, sel + "-glow", {"opacity": 1, "duration": .4}, what)
def WAY(at, sel, tag, n, step=.35, what="the blood goes along"): return [("to", at, f"{sel}-{tag}{k}", {"opacity": 1, "duration": .25, "delay": k * step}, what if k == 0 else "") for k in range(n)]
def OUTWAY(at, sel): return [ON(at, sel + "-out", "red lines: the way away from the heart")] + WAY(at, sel, "o", 5)
def BACKWAY(at, sel): return [ON(at, sel + "-back", "blue lines: the way back to the heart")] + WAY(at, sel, "b", 4)
def SHOWWAYS(sel): return [("fromto", 0, f"{sel}-out,{sel}-back", {"opacity": 1}, {"opacity": 1, "duration": .01}, "")]
def OXY(at, sel, what="the blood in the lungs picks up oxygen"):
    return [("to", at, sel + "-o2", {"opacity": 1, "duration": .5}, what), ("to", at, sel + "-red", {"opacity": 1, "duration": .8, "delay": .6}, ""),
            ("to", at, sel + "-blue", {"opacity": 0, "duration": .8, "delay": .6}, "")]
def DOORS(at, sel, what="the little doors close"):
    return [("to", at, f"{sel}-d0,{sel}-d1", {"keyframes": [{"rotation": 34, "svgOrigin": "0 0", "duration": .2}, {"rotation": 0, "svgOrigin": "0 0", "duration": .4}]}, what)]
def DOORS2(at, sel, n=2, what="the little doors swing shut, lub, dub"):
    k = []
    for _ in range(n): k += [{"scaleX": .2, "duration": .16}, {"scaleX": 1, "duration": .47}]
    return [("to", at, f"{sel}-d0,{sel}-d1,{sel}-e0,{sel}-e1", {"keyframes": k, "transformOrigin": "50% 0%"}, what)]
def ROOM(at, sel, k, what=""): return ("to", at, f"{sel}-c{k}", {"keyframes": [{"opacity": 1, "duration": .2}, {"opacity": 1, "duration": .6}, {"opacity": .25, "duration": .3}]}, what)
def RUN(at, sel, d=2.4, what="the dot runs along the heartbeat line"): return ("fromto", at, sel + "-dot", {"x": 0}, {"x": 800, "duration": d, "ease": "none"}, what)
def BOUNCE(at, sel, n=3, what="the ball bounces"): return ("to", at, sel, {"y": "-=160", "duration": .3125, "yoyo": True, "repeat": 2 * n - 1, "ease": "power1.out"}, what)


# ------------------------------------------------------------------ props and cameras
BOARD = (960, 540, 1500); PBOARD = (960, 470, 1700)
BODY = (960, 560, 1700); PBODY = (960, 560, 1700)
def b_heart(x=960, y=720, s=1.0, px=960, py=700, ps=.9): return prop("ht", A.heart, x, y, s, p=(px, py, ps))
def b_body(s=.72, y=540, ps=.56, py=640): return prop("bd", A.body, 960, y, s, p=(960, py, ps))
def b_bodyq(): return prop("bd", A.body, 960, 680, .44, p=(960, 690, .42))       # a question: the body small, under the answer signs
def b_fist(): return prop("fs", A.fist, 1220, 660, .9, p=(1210, 680, .7))
def b_lungs(y=700, s=.9, py=660, ps=.7): return prop("lg", A.lungs, 960, y, s, p=(960, py, ps))
def b_rooms(y=730, s=.9, py=650, ps=.75): return prop("rm", A.rooms, 960, y, s, p=(960, py, ps))
def b_beat(fast=False): return prop("bt", lambda p: A.beat_line(p, fast), 960, 720, 1.0, p=(960, 660, .9))
def b_bed(): return prop("bed", A.bed, 960, 760, 1.0, p=(960, 690, .95))
def b_sun(): return prop("bs", G.warm_sun, 650, 620, .6, p=(720, 560, .45))
def b_moon(): return prop("bm", A.moon, 1250, 640, .7, p=(1190, 560, .5))
def b_smallheart(): return prop("sh", A.heart, 960, 780, .55, p=(960, 760, .5))
WIN = (960, 520, 1700); WINP = (1000, 430, 1150)
def night(): return prop("nt", A.night, 960, 350, 1.0, p=(960, 350, 1.0))
PARK = (960, 560, 1920); PARKP = (900, 600, 1700)
PARKG = GCAM("gpark", 1150)
def pball(): return prop("bl", A.ball, 1250, 900, .9, p=(1200, 900, .8))
MEAD = (960, 600, 1700); MEADG = GCAM("gmeadow", 1150)
HILL = (960, 540, 1920); HILLP = (700, 560, 1500)


SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("paper_gz", BOARD, "How does your heart work? What makes that thump, thump?", q=True, tag="hook: the heart beats", pcam=PBOARD, cam2=(960, 600, 1300),
      props=[b_heart()], fx=[BEAT(0.1, "#{p}ht", 6)], words=[("w:thump,:2", "?", .8, .3, 2.0, "sun", (.75, .38), 1.3)]),
    S("paper_gz", BODY, "Thump, thump! Your heart beats inside your chest.", tag="hook: the heart in the chest", pcam=PBODY, cam2=W(BODY, 1.0),
      props=[b_body()], fx=[BEAT(0.05, "#{p}bd-h", 6)], words=[("w:Thump,", "THUMP, THUMP!", .24, .3, .9, "sun", (.5, .3), .7)]),
    S("glab", (GX, 640, 1000), "Hi! I'm Gizmo. Let's find out how your heart works!", tag="hook: Gizmo", pcam=GP("glab"), fx=[WAVE("w:Hi!"), HOP("w:find")],
      words=[("w:Gizmo.", "GIZMO", .78, .3, 1.1, "pill", (.5, .36), .9)]),
    # ---------------------------------------------------------------- MAIN INTRO (right after the hook; again as the last four shots)
    *gz_intro_shots(),
    S("glab", WIDE, "Welcome to my lab, body explorers!", trans="iris", tag="lab wide", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=[WAVE("w:Welcome", 4)],
      words=[("w:lab,", "HELLO!", .74, .5, 1.2, "pill", (.5, .36), 1.0)]),
    S("gbench", (900, 560, 1500), "I am a robot, so I have no heart. But you do!", tag="no heart", pcam=GPL("gbench"), props=[prop("bh", A.heart, 1260, 640, .6, p=(1180, 1010, .4))],
      fx=[("face", "w:no", "gizmo", "wow"), BEAT("w:you", "#{p}bh", 3)], words=[("w:you", "YOU DO!", .8, .2, 1.0, "sun", (.5, .67), .85)]),
    # ---------------------------------------------------------------- PART 1: a muscle, the size of your fist, in your chest, pumping all the time
    S("paper_gz", BODY, "Your heart is in your chest, a little to the left of the middle.", part=1, tag="where it is", pcam=PBODY, cam2=W(BODY, 1.0), props=[b_body()],
      fx=[BEAT("w:chest,", "#{p}bd-h", 4)], words=[("w:chest,", "IN YOUR CHEST!", .76, .3, .85, "sun", (.5, .3), .65)]),
    S("glab", GCAM("glab"), "Put your hand on your chest. Can you feel a beat?", part=1, q=True, tag="hand on chest", pause=1.6, pcam=GPL("glab"),
      props=[prop("lh", A.heart, 1080, 600, .45, p=(1000, 1000, .35))], fx=[BEAT("w:hand", "#{p}lh", 5), ("face", "w:feel", "gizmo", "wow")],
      words=[("w:hand", "HAND ON CHEST", .3, .2, .8, "sun", (.5, .67), .6)]),
    S("paper_gz", BODY, "Where is your heart? In your chest, or in your foot?", part=1, q=True, tag="question 1", pause=3.2, pcam=PBODY, cam2=(960, 575, 1600),
      props=[b_bodyq()], fx=[BEAT(0.2, "#{p}bd-h", 8), ("signs", "w:chest,", ["CHEST", "FOOT"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "In your chest! Your heart is really a muscle.", part=1, tag="a muscle", pcam=PBOARD, props=[b_heart()],
      fx=[BEAT("w:chest!", "#{p}ht", 2), GLOW("w:muscle.", "#{p}ht")], words=[("w:muscle.", "A MUSCLE!", .24, .3, 1.0, "sun", (.3, .38), .85)]),
    S("paper_gz", BOARD, "Is your heart a muscle, or a balloon?", part=1, q=True, tag="question 2", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_heart()],
      fx=[BEAT(0.2, "#{p}ht", 7), ("signs", "w:muscle,", ["MUSCLE", "BALLOON"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "A muscle! It squeezes, and pumps blood around your body.", part=1, tag="it pumps", pcam=PBOARD, props=[b_heart()],
      fx=[BEAT("w:squeezes,", "#{p}ht", 4)], words=[("w:pumps", "PUMP!", .76, .3, 1.1, "sun", (.72, .38), .9)]),
    S("glab", GCAM("glab"), "Make a fist. Squeeze it, and open it, like a heart pumping!", part=1, q=True, tag="squeeze a fist", pause=1.8, pcam=GPL("glab"),
      fx=[CURL("w:Squeeze", 1.0), ("hop", "w:open", "gizmo", 1)], words=[("w:Squeeze", "SQUEEZE!", .8, .3, 1.0, "sun", (.5, .67), .85)]),
    S("paper_gz", BOARD, "Look at your fist. Your heart is about the size of your fist!", part=1, tag="fist size", pcam=PBOARD,
      props=[b_heart(720, 720, .85, 740, 700, .66), b_fist()], fx=[PULSE("w:fist.", "#{p}fs", 1, 1.06), BEAT("w:heart", "#{p}ht", 3)],
      words=[("w:size", "SAME SIZE!", .5, .2, .9, "sun", (.5, .36), .7)]),
    S("glab", GCAM("glab"), "Hold up your fist, and look. That is about how big your heart is!", part=1, q=True, tag="hold up a fist", pause=1.4, pcam=GPL("glab"),
      props=[prop("fh", A.fist, 1100, 560, .55, p=(1000, 1000, .4))], fx=UP("w:Hold", 1.4) + [PULSE("w:big", "#{p}fh", 1, 1.08)],
      words=[("w:fist,", "FIST UP!", .3, .2, 1.0, "sun", (.5, .67), .85)]),
    S("paper_gz", BOARD, "How big is your heart? As big as your fist, or as big as a car?", part=1, q=True, tag="question 3", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[b_heart(720, 720, .85, 740, 700, .66), b_fist()], fx=[BEAT(0.2, "#{p}ht", 8), ("signs", "w:fist,", ["A FIST", "A CAR"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Your heart pumps all day, and all night, all the time!", part=1, tag="day and night", pcam=PBOARD, props=[b_sun(), b_moon(), b_smallheart()],
      fx=[PULSE("w:day,", "#{p}bs", 1, 1.08), PULSE("w:night,", "#{p}bm", 1, 1.08), BEAT("w:time!", "#{p}sh", 3)],
      words=[("w:time!", "ALL THE TIME!", .5, .14, .9, "sun", (.5, .36), .7)]),
    S("gwindow", WIN, "Even when you sleep at night, your heart keeps pumping.", part=1, tag="night window", pcam=WINP, hide=["gizmo"], cam2=W(WIN, 1.0), props=[night()],
      fx=[PULSE("w:night,", "#{p}nt", 1, 1.01)], words=[("w:sleep", "SLEEP TIGHT!", .78, .14, .9, "sun", (.5, .36), .75)]),
    S("paper_gz", BOARD, "Your heart keeps on going, nice and calm.", part=1, tag="asleep", pcam=PBOARD, props=[b_bed()],
      fx=[BEAT(0.3, "#{p}bed-h", 5)], words=[("w:calm.", "NICE AND CALM", .5, .14, .85, "sun", (.5, .36), .65)]),
    S("gpark", PARKG, "Sitting, walking, or playing, your heart is always working!", part=1, tag="always working", pcam=GP("gpark"), props=[pball()],
      fx=[HOP("w:playing,"), BOUNCE("w:playing,", "#{p}bl", 2)], words=[("w:always", "ALWAYS!", .8, .3, 1.1, "sun", (.5, .36), .9)]),
    S("paper_gz", BOARD, "When does your heart pump? Only in the day, or all the time?", part=1, q=True, tag="question 4", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[b_sun(), b_moon(), b_smallheart()], fx=[BEAT(0.2, "#{p}sh", 8), ("signs", "w:day,", ["DAY ONLY", "ALL THE TIME"], 1, "wait:2.0")]),
    S("gbench", (900, 560, 1500), "Say it with me. My heart is a muscle!", part=1, q=True, tag="say it", pcam=GPL("gbench"), fx=[HOP("w:muscle!")],
      words=[("w:heart", "HEART = MUSCLE!", .55, .2, .8, "sun", (.5, .36), .6)]),
    S("paper_gz", BOARD, "A muscle, as big as your fist, pumping all the time!", part=1, tag="part 1 recap", pcam=PBOARD,
      props=[b_heart(720, 720, .85, 740, 700, .66), b_fist()], fx=[BEAT("w:muscle,", "#{p}ht", 4), PULSE("w:fist,", "#{p}fs", 1, 1.06)],
      words=[("w:pumping", "PUMP, PUMP!", .5, .14, .9, "sun", (.5, .36), .7)]),
    # ---------------------------------------------------------------- PART 2: blood, oxygen, the lungs, out and back
    S("paper_gz", BODY, "What does your heart pump around your body? Blood!", part=2, trans="iris", tag="blood", pcam=PBODY, cam2=W(BODY, 1.0), props=[b_body()],
      fx=[BEAT(0.2, "#{p}bd-h", 3)] + OUTWAY("w:Blood!", "#{p}bd"), words=[("w:Blood!", "BLOOD!", .78, .3, 1.1, "sun", (.75, .3), .9)]),
    S("paper_gz", BODY, "Blood gives your body oxygen, and good things from your food.", part=2, tag="oxygen and food", pcam=PBODY, props=[b_body()],
      fx=SHOWWAYS("#{p}bd") + [BEAT(0.1, "#{p}bd-h", 4)] + WAY("w:oxygen,", "#{p}bd", "o", 5, .3, "the blood carries oxygen to every part"),
      words=[("w:oxygen,", "OXYGEN!", .22, .3, 1.0, "sun", (.25, .3), .8)]),
    S("paper_gz", BODY, "It carries oxygen to every part of you, from your head to your toes!", part=2, tag="head to toes", pcam=PBODY, props=[b_body()],
      fx=SHOWWAYS("#{p}bd") + WAY("w:head", "#{p}bd", "o", 2, .3, "up to the head") + WAY("w:toes!", "#{p}bd", "o", 5, .2, "down to the toes"),
      words=[("w:head", "HEAD", .76, .14, 1.0, "sun", (.75, .3), .8), ("w:toes!", "TOES!", .76, .82, 1.0, "", (.75, .68), .8)]),
    S("glab", GCAM("glab"), "Touch your head, and then touch your toes!", part=2, q=True, tag="head and toes", pause=1.6, pcam=GPL("glab"),
      fx=UP("w:head,", .8) + DOWN("w:toes!", 1.0), words=[("w:toes!", "HEAD, TOES!", .3, .2, 1.0, "sun", (.5, .67), .8)]),
    S("paper_gz", BOARD, "What does blood carry? Oxygen, or sand?", part=2, q=True, tag="question 5", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_heart()],
      fx=[BEAT(0.2, "#{p}ht", 7), ("signs", "w:Oxygen,", ["OXYGEN", "SAND"], 0, "wait:2.0")]),
    S("glab", GCAM("glab"), "Oxygen is in the air. Breathe in slowly, and breathe out.", part=2, q=True, tag="breathe", pause=2.0, pcam=GPL("glab"),
      props=[prop("pf", G.puff, 1100, 520, .6, p=(1000, 980, .45))], fx=WIDEARMS("w:Breathe", 1.8) + [("to", "w:in", "#{p}pf", {"x": -80, "duration": 1.6, "ease": "sine.inOut", "yoyo": True, "repeat": 1}, "air goes in and out")],
      words=[("w:Breathe", "BREATHE IN!", .3, .2, .9, "sun", (.5, .67), .75)]),
    S("paper_gz", BOARD, "Your heart sends blood to your lungs.", part=2, tag="to the lungs", pcam=PBOARD, props=[b_lungs()],
      fx=[BEAT("w:sends", "#{p}lgh", 3), PULSE("w:lungs.", "#{p}lg", 1, 1.04)], words=[("w:lungs.", "LUNGS!", .2, .3, 1.1, "sun", (.25, .3), .9)]),
    S("paper_gz", BOARD, "There, the blood picks up oxygen!", part=2, tag="picks up oxygen", pcam=PBOARD, props=[b_lungs()],
      fx=OXY("w:picks", "#{p}lg"), words=[("w:oxygen!", "OXYGEN!", .8, .3, 1.0, "sun", (.75, .3), .85)]),
    S("paper_gz", BOARD, "Where does blood pick up oxygen? In your lungs, or in your toes?", part=2, q=True, tag="question 6", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[b_lungs(740, .8, 660, .7)], fx=[BEAT(0.2, "#{p}lgh", 7), ("signs", "w:lungs,", ["LUNGS", "TOES"], 0, "wait:2.0")]),
    S("paper_gz", BODY, "The lungs! Then your heart pumps the blood all around your body.", part=2, tag="all around", pcam=PBODY, cam2=W(BODY, 1.0), props=[b_body()],
      fx=[BEAT("w:heart", "#{p}bd-h", 4)] + OUTWAY("w:pumps", "#{p}bd"), words=[("w:around", "ALL AROUND!", .22, .3, .9, "sun", (.5, .3), .75)]),
    S("paper_gz", BODY, "Tubes called blood vessels carry it away, and bring it back!", part=2, tag="out and back", pcam=PBODY, props=[b_body()],
      fx=OUTWAY("w:away,", "#{p}bd") + BACKWAY("w:back!", "#{p}bd"), words=[("w:away,", "AWAY", .22, .3, 1.0, "sun", (.25, .3), .8), ("w:back!", "BACK!", .78, .3, 1.0, "sun", (.75, .3), .8)]),
    S("paper_gz", BODY, "Does the blood come back to your heart? Yes, or no?", part=2, q=True, tag="question 7", pause=3.2, pcam=PBODY, cam2=(960, 575, 1600),
      props=[b_bodyq()], fx=SHOWWAYS("#{p}bd") + [BEAT(0.2, "#{p}bd-h", 8), ("signs", "w:Yes,", ["YES", "NO"], 0, "wait:2.0")]),
    S("paper_gz", BODY, "Yes! Away and back, over and over again.", part=2, tag="over and over", pcam=PBODY, props=[b_body()],
      fx=SHOWWAYS("#{p}bd") + WAY("w:Away", "#{p}bd", "o", 5, .25) + WAY("w:back,", "#{p}bd", "b", 4, .25, "the blood comes back"),
      words=[("w:over", "AGAIN AND AGAIN!", .5, .14, .8, "sun", (.5, .3), .6)]),
    S("gmeadow", MEADG, "Draw a big circle in the air with your finger!", part=2, q=True, tag="draw a circle", pause=1.6, pcam=GPL("gmeadow"),
      fx=WIDEARMS("w:circle", 1.6) + [("to", "w:circle", "#{p}gizmo-body", {"rotation": 8, "svgOrigin": "0 -200", "duration": .31, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "Gizmo sways")],
      words=[("w:circle", "ROUND!", .8, .3, 1.1, "sun", (.5, .67), .9)]),
    S("gbench", (900, 560, 1500), "Say it with me. My heart pumps blood!", part=2, q=True, tag="say it 2", pcam=GPL("gbench"), fx=[HOP("w:blood!")],
      words=[("w:pumps", "PUMP THE BLOOD!", .55, .2, .8, "sun", (.5, .36), .6)]),
    S("paper_gz", BOARD, "Where does blood get oxygen? In your lungs, or in your hair?", part=2, q=True, tag="question 7b", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[b_lungs(740, .8, 660, .7)], fx=OXY(0.3, "#{p}lg") + [("signs", "w:lungs,", ["LUNGS", "HAIR"], 0, "wait:2.0")]),
    S("paper_gz", BODY, "The lungs! Then the heart sends it all around, and back again.", part=2, tag="part 2 recap", pcam=PBODY, props=[b_body()],
      fx=OUTWAY("w:sends", "#{p}bd") + BACKWAY("w:back", "#{p}bd"), words=[("w:around,", "ROUND AND BACK!", .5, .14, .8, "sun", (.5, .3), .6)]),
    # ---------------------------------------------------------------- PART 3: the sound, four rooms, faster when you play
    S("paper_gz", BOARD, "Listen to a heartbeat. It sounds like lub, dub!", part=3, trans="iris", tag="lub dub", pcam=PBOARD, props=[b_beat()],
      fx=[RUN("w:Listen", "#{p}bt", 3.0)], words=[("w:lub,", "LUB, DUB!", .5, .14, 1.1, "sun", (.5, .36), .9)]),
    S("glab", GCAM("glab"), "Clap with me, like a heartbeat. Lub, dub! Lub, dub!", part=3, q=True, tag="clap lub dub", pause=1.4, pcam=GPL("glab"),
      props=[prop("lh", A.heart, 1080, 600, .45, p=(1000, 1000, .35))], fx=[BEAT("w:Clap", "#{p}lh", 5)] + ARMS("w:Lub,", 40, -40, .3) + ARMS("w:Lub,:2", 40, -40, .3),
      words=[("w:Clap", "CLAP, CLAP!", .3, .2, 1.0, "sun", (.5, .67), .85)]),
    S("paper_gz", BOARD, "Inside your heart are little doors, called valves.", part=3, tag="valves", pcam=PBOARD, props=[b_rooms()],
      fx=[PULSE("w:doors,", "#{p}rm-d0", 2, 1.2), PULSE("w:doors,", "#{p}rm-d1", 2, 1.2)], words=[("w:valves.", "VALVES", .2, .3, 1.0, "sun", (.25, .3), .8)]),
    S("paper_gz", BOARD, "When the doors close, they make the sound. Lub, dub!", part=3, tag="doors close", pcam=PBOARD, props=[b_rooms()],
      fx=DOORS2("w:close,", "#{p}rm", 3), words=[("w:Lub,", "LUB, DUB!", .8, .3, 1.0, "sun", (.75, .3), .8)]),
    S("paper_gz", BOARD, "What makes the heartbeat sound? Little doors closing, or a tiny drum?", part=3, q=True, tag="question 8", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[b_rooms(760, .8, 660, .7)], fx=DOORS2(0.2, "#{p}rm", 6) + [("signs", "w:doors", ["DOORS", "A DRUM"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Your heart has four rooms. Two on top, and two on the bottom!", part=3, tag="four rooms", pcam=PBOARD, props=[b_rooms()],
      fx=[ROOM("w:top,", "#{p}rm", 0, "the top rooms light up"), ROOM("w:top,", "#{p}rm", 1), ROOM("w:bottom!", "#{p}rm", 2, "the bottom rooms light up"), ROOM("w:bottom!", "#{p}rm", 3)],
      words=[("w:four", "4 ROOMS!", .2, .3, 1.0, "sun", (.25, .3), .8)]),
    S("paper_gz", BOARD, "How many rooms are in your heart? Two, or four?", part=3, q=True, tag="question 9", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[b_rooms(760, .8, 660, .7)], fx=[("signs", "w:Two,", ["TWO", "FOUR"], 1, "wait:2.0")]),
    S("paper_gz", BOARD, "Four! Let's count them. One, two, three, four!", part=3, q=True, tag="count rooms", pcam=PBOARD, props=[b_rooms()],
      fx=[ROOM("w:One,", "#{p}rm", 0, "room 1"), ROOM("w:two,", "#{p}rm", 1, "room 2"), ROOM("w:three,", "#{p}rm", 2, "room 3"), ROOM("w:four!:2", "#{p}rm", 3, "room 4")],
      words=[("w:One,", "1", .38, .3, 1.1, "sun", (.38, .36), .8), ("w:two,", "2", .62, .3, 1.1, "sun", (.62, .36), .8),
             ("w:three,", "3", .38, .8, 1.1, "", (.38, .66), .8), ("w:four!:2", "4", .62, .8, 1.1, "", (.62, .66), .8)]),
    S("paper_gz", BOARD, "Listen again. Lub, dub, lub, dub. Your heart never stops!", part=3, tag="listen again", pcam=PBOARD, props=[b_beat()],
      fx=[RUN("w:Listen", "#{p}bt", 3.4)], words=[("w:never", "NEVER STOPS!", .5, .14, .9, "sun", (.5, .36), .7)]),
    S("gpark", PARK, "When you run and play, your heart pumps faster!", part=3, tag="run and play", pcam=PARKP, cam2=W(PARK, 1.0), props=[pball()],
      fx=[BOUNCE("w:run", "#{p}bl", 4), HOP("w:play,", 2)], words=[("w:faster!", "FASTER!", .78, .3, 1.1, "sun", (.75, .36), .9)]),
    S("paper_gz", BOARD, "Why? So your muscles get more oxygen, and can work harder.", part=3, tag="why faster", pcam=PBOARD, props=[b_beat(True)],
      fx=[RUN("w:Why?", "#{p}bt", 2.4), RUN("w:oxygen,", "#{p}bt", 2.4, "")], words=[("w:oxygen,", "MORE OXYGEN!", .5, .14, .9, "sun", (.5, .36), .7)]),
    S("gpark", PARKG, "Can you march in place? Left, right, left, right!", part=3, q=True, tag="march", pause=1.0, pcam=GP("gpark"), props=[pball()],
      fx=[HOP("w:Left,"), HOP("w:right,"), HOP("w:left,:2"), HOP("w:right!")], words=[("w:march", "MARCH!", .8, .3, 1.1, "sun", (.5, .36), .9)]),
    S("gmeadow", MEADG, "Let's hop five times! One, two, three, four, five!", part=3, q=True, tag="hop five", pause=.6, pcam=GPL("gmeadow"),
      fx=[HOP("w:One,", 1), HOP("w:two,", 1), HOP("w:three,", 1), HOP("w:four,", 1), HOP("w:five!", 1)], words=[("w:hop", "HOP, HOP!", .8, .3, 1.0, "sun", (.5, .67), .85)]),
    S("glab", GCAM("glab"), "Now, hand on your chest. Is your heart beating faster?", part=3, q=True, tag="feel it faster", pause=2.0, pcam=GPL("glab"),
      props=[prop("lh", A.heart, 1080, 600, .45, p=(1000, 1000, .35))], fx=[BEAT("w:hand", "#{p}lh", 10, True)] + IDEA("w:faster?"),
      words=[("w:faster?", "FASTER?", .3, .2, 1.0, "sun", (.5, .67), .85)]),
    S("paper_gz", BOARD, "When you run and play, does your heart beat faster, or slower?", part=3, q=True, tag="question 10", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[b_heart()], fx=[BEAT(0.2, "#{p}ht", 14, True), ("signs", "w:faster,", ["FASTER", "SLOWER"], 0, "wait:2.0")]),
    S("ghills", HILL, "Running and swimming help keep your heart healthy!", part=3, tag="keep it healthy", pcam=HILLP, hide=["gizmo"], cam2=W(HILL, 1.0),
      props=[prop("hh", A.heart, 1500, 360, .6, p=(900, 420, .5))], fx=[BEAT(0.2, "#{p}hh", 5), GLOW("w:healthy!", "#{p}hh")],
      words=[("w:healthy!", "STRONG HEART!", .3, .3, .9, "sun", (.36, .3), .7)]),
    S("gbench", (900, 560, 1500), "Say it with me. Lub, dub! My heart works hard!", part=3, q=True, tag="say it 3", pcam=GPL("gbench"), fx=[HOP("w:hard!")],
      words=[("w:Lub,", "LUB, DUB!", .55, .2, .9, "sun", (.5, .36), .75)]),
    # ---------------------------------------------------------------- QUIZ + GOODBYE
    S("glab", WIDE, "Quiz time! Let's remember what we learned.", part=4, trans="iris", tag="quiz time", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=IDEA("w:Quiz"),
      words=[("w:Quiz", "QUIZ TIME!", .74, .5, 1.3, "sun", (.5, .36), 1.0)]),
    S("paper_gz", BOARD, "How big is your heart? As big as your fist, or as big as a bus?", part=4, q=True, tag="quiz 1", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[b_heart(720, 720, .85, 740, 700, .66), b_fist()], fx=[BEAT(0.2, "#{p}ht", 8), ("signs", "w:fist,", ["A FIST", "A BUS"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Your fist! A strong muscle, pumping all the time.", part=4, tag="quiz 1 answer", pcam=PBOARD, props=[b_heart(720, 720, .85, 740, 700, .66), b_fist()],
      fx=[BEAT("w:fist!", "#{p}ht", 4), PULSE("w:fist!", "#{p}fs", 1, 1.06)], words=[("w:fist!", "YOUR FIST!", .5, .14, 1.0, "sun", (.5, .36), .8)]),
    S("paper_gz", BOARD, "Where does blood pick up oxygen? In your lungs, or in your ears?", part=4, q=True, tag="quiz 2", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), trans="iris",
      props=[b_lungs(740, .8, 660, .7)], fx=[BEAT(0.2, "#{p}lgh", 7), ("signs", "w:lungs,", ["LUNGS", "EARS"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "In your lungs! Fresh oxygen for your blood.", part=4, tag="quiz 2 answer", pcam=PBOARD, props=[b_lungs()],
      fx=OXY("w:lungs!", "#{p}lg"), words=[("w:lungs!", "LUNGS!", .2, .3, 1.1, "sun", (.25, .3), .9)]),
    S("paper_gz", BOARD, "What makes the lub, dub sound? Little doors, or little bells?", part=4, q=True, tag="quiz 3", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), trans="iris",
      props=[b_rooms(760, .8, 660, .7)], fx=DOORS2(0.2, "#{p}rm", 6) + [("signs", "w:doors,", ["DOORS", "BELLS"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Little doors inside your heart, closing. Lub, dub!", part=4, tag="quiz 3 answer", pcam=PBOARD, props=[b_rooms()],
      fx=DOORS2("w:closing.", "#{p}rm", 3), words=[("w:Lub,", "LUB, DUB!", .8, .3, 1.0, "sun", (.75, .3), .8)]),
    S("gpark", PARKG, "Muscle, blood, oxygen, lub, dub! Thanks for exploring with me!", part=4, tag="goodbye", pcam=GP("gpark"), props=[pball()],
      fx=[WAVE("w:Thanks", 5), HOP("w:exploring")], words=[("w:Thanks", "BYE-BYE!", .8, .3, 1.1, "pill", (.5, .36), .9)]),
    *gz_intro_shots(),      # the main intro again, as the last four shots
]
for _s in SHOTS:
    _s["who"] = "gizmo"        # Gizmo speaks every line, so his mouth moves
    if _s["place"].startswith("paper") and _s["pcam"] and not _s["pcam2"]: _s["pcam2"] = W(_s["pcam"], 1.04)     # a picture board never drifts closer (zc_ep08)
    if _s["place"].startswith("paper") and not _s["cam2"]: _s["cam2"] = W(_s["cam"], 1.04)
    for _f in _s["fx"]:        # 9:16: a word never sits on the title band's second line
        if _f[0] == "word" and len(_f) > 3 and "p" in _f[3] and _s["pcam"]: _f[3]["p"]["y"] = max(_f[3]["p"]["y"], round(_s["pcam"][1] - .15 * _s["pcam"][2]))

SHORTS = [
    {"id": "gc_ep04_short1", "title": "How Big Is Your Heart? Gizmo Explains", "band": ("HOW BIG IS", "IT?"), "thumb_text": "FIST SIZE", "part": 1,
     "extra_first": [S("paper_gz", BOARD, "How big is the heart inside your chest?", part=1, q=True, tag="hook: how big", pcam=PBOARD, who="gizmo", pcam2=W(PBOARD, .94),
                       props=[b_heart(720, 720, .85, 740, 700, .66), b_fist()], fx=[BEAT(0.1, "#{p}ht", 5)], words=[("w:chest?", "?", .5, .2, 2.0, "sun", (.5, .36), 1.3)])]},
    {"id": "gc_ep04_short2", "title": "Where Does Your Blood Go? Gizmo Explains", "band": ("WHERE DOES", "IT GO?"), "thumb_text": "OUT, BACK!", "part": 2,
     "extra_first": [S("paper_gz", BODY, "Where does your blood go, all day long?", part=2, q=True, tag="hook: where does blood go", pcam=PBODY, who="gizmo", pcam2=W(PBODY, .94),
                       props=[b_body()], fx=[BEAT(0.1, "#{p}bd-h", 4)] + OUTWAY(0.4, "#{p}bd"), words=[("w:long?", "?", .78, .3, 2.0, "sun", (.75, .3), 1.3)])]},
    {"id": "gc_ep04_short3", "title": "What Makes the Heartbeat Sound? Gizmo Explains", "band": ("WHAT MAKES", "THE SOUND?"), "thumb_text": "LUB DUB", "part": 3,
     "extra_first": [S("paper_gz", BOARD, "What makes that sound inside you? Lub, dub!", part=3, q=True, tag="hook: the sound", pcam=PBOARD, who="gizmo", pcam2=W(PBOARD, .94),
                       props=[b_beat()], fx=[RUN(0.1, "#{p}bt", 3.0)], words=[("w:you?", "?", .8, .3, 2.0, "sun", (.75, .36), 1.3)])]},
]
for _sp in SHORTS:
    for _s in _sp["extra_first"]:
        for _f in _s["fx"]:
            if _f[0] == "word" and len(_f) > 3 and "p" in _f[3] and _s["pcam"]: _f[3]["p"]["y"] = max(_f[3]["p"]["y"], round(_s["pcam"][1] - .15 * _s["pcam"][2]))


# thumbnails (thumb.py): the example in the picture, 1-2 words, none of the title's words, no watermark
THUMBS = {
    "gc_ep04": {"place": "paper_gz", "cam": (900, 560, 1300), "actors": [],
                "props": [(A.heart, 640, 640, 1.35)],
                "words": [("THUMP", 1380, 400, 190, ""), ("THUMP!", 1380, 660, 200, "sun")]},
    "gc_ep04_short1": {"place": "paper_gz", "cam": (960, 640, 1400), "actors": [],
                       "props": [(A.heart, 720, 700, .95), (A.fist, 1200, 650, 1.0)],
                       "words": [("FIST", 540, 330, 220, ""), ("SIZE", 540, 1560, 220, "sun")]},
    "gc_ep04_short2": {"place": "paper_gz", "cam": (960, 560, 1500), "actors": [],
                       "props": [(lambda p: A.body(p).replace('opacity="0"', 'opacity="1"'), 960, 560, .78)],
                       "words": [("OUT,", 540, 300, 220, ""), ("BACK!", 540, 1580, 220, "sun")]},
    "gc_ep04_short3": {"place": "paper_gz", "cam": (960, 640, 1400), "actors": [],
                       "props": [(A.rooms, 960, 700, 1.0)],
                       "words": [("LUB", 540, 330, 230, ""), ("DUB!", 540, 1560, 240, "sun")]},
}
