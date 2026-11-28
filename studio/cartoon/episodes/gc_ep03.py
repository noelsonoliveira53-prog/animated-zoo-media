"""gc_ep03: "Where Does Rain Come From?" - Gizmo Explains cartoon explainer (daily run Nov 27 2026, session_014CFVfVoMCFiR6Tndgu9wxQ).
Gizmo hosts in his lab, at his bench, at the window, in a sunny park with a puddle, high in the sky and over the hills with a river ("beat" process).
Three parts, each cut whole into one Short: 1. the sun warms water and it turns into invisible water vapor that floats up (evaporation),
2. high up the cold air turns the vapor back into tiny drops on specks of dust, and the drops make clouds (condensation; drops on a window in winter),
3. the tiny drops join into bigger drops, heavy drops fall as rain or snow, the water flows downhill to rivers, lakes and the ocean, and the sun warms
it again: the water cycle, always happening, everywhere.

FACTS, read at the source on Nov 27 2026 (pages fetched in this session by the page reader; quotes copied from the page text, at most 125 characters each):
 [KIDS] USGS Water Science School, "Interactive Water Cycle Diagram for Kids (Beginner)" (water.usgs.gov/edu/watercycle-kids-beg.html):
   "The sun provides heat, or energy, which is what makes the water cycle work."
   "The sun causes liquid water to evaporate, or turn from a liquid to a gas (water vapor)."
   "The invisible water vapor floats high into the atmosphere (the air that surrounds the earth)."
   "The colder temperatures high in the atmosphere cause the water vapor to turn back into tiny liquid water droplets" (-- the clouds)
   "Condensation causes clouds to form."   "This is condensation, the opposite of evaporation."
   "The tiny cloud droplets combine with each other and grow into bigger water drops."
   "When they get heavy enough, they fall to Earth as precipitation, such as rain and snow."
   "When rain hits the land or snow melts, it flows downhill over the landscape."   "This is called runoff, which provides water to rivers, lakes, and the oceans."
   "This process is always happening everywhere."
 [COND] USGS Water Science School, "The Water Cycle for Kids: Condensation create clouds" (water.usgs.gov/edu/gallery/watercyclekids/condensation-beg.html):
   "Condensation is the term for water that is a gas (water vapor) turning into liquid water."
   "That liquid can become clouds in the sky or be drops of water on the inside of your home windows on a cold winter day."
   "Condensation is the opposite of evaporation."
 [DRIP] USGS Water Science School, "Follow a Drip Through the Water Cycle" (usgs.gov/water-science-school/science/follow-a-drip-through-water-cycle):
   "The heat from the sun found the drop, warmed it, and evaporated it into water vapor."
   "The vapor condenses on tiny particles of dust, smoke, and salt crystals to become part of a cloud." (quoted in part)
   "After a while our drop combined with other drops to form a bigger drop and fell to the earth as precipitation."
   "Earth's gravity helped to pull it down to the surface."
 Said as: the sun's heat makes the water cycle work; the sun warms water and it turns into a gas called water vapor (evaporation); water vapor is
 invisible (drawn as little dots, and the episode says so); it floats high into the sky; high up it is cold, and the cold turns the vapor back into tiny
 drops of water; each tiny drop forms on a tiny speck of dust, smoke or salt; lots of tiny drops make a cloud (condensation); condensation is the opposite
 of evaporation; you can see it at home: drops of water on the inside of a window on a cold winter day; tiny drops join and grow into bigger drops; when
 they are heavy enough they fall as rain, or snow; gravity pulls them down; rain flows downhill into rivers, lakes and the ocean; the sun warms the water
 again; the water cycle is always happening, everywhere.
 Taken out (not on the pages read today): raindrop shapes (the "hamburger bun" page could not be read today), "most of it ends up in the oceans",
 cold-glass drops, kettles and steam (also: nothing hot a child could copy). Pictures that are ours, not facts: "round and round", the shrinking puddle
 drawn in a few seconds (it takes longer), the dots that show the invisible vapor.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_gizmo as G
import art_gc_ep02 as R
import art_gc_ep03 as A
from kit import Kit, S, prop, W
from intro_gizmo import GZ_INTRO_STAGES, gz_intro_shots      # Gizmo's main intro (owner, Nov 21 2026 12:18 PM: "amazing emplement on every new video")
from episodes.gc_ep01 import WAVE, IDEA, ARMS, UP, DOWN, WIDEARMS, CURL, HOP, PULSE, OFF, ON

BOILER = ("Gizmo Explains makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 4-8. "
          "Every fact is checked against trusted sources and every script is reviewed for kid safety before publishing.")
SRC = ("WHERE THE FACTS COME FROM\nUSGS Water Science School: The Water Cycle for Kids, Condensation, and Follow a Drip Through the Water Cycle.")
EP = {"id": "gc_ep03", "nest": True, "beat": True, "voice": "am_michael", "speed": 0.85, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 1.0, "wm": "brand/gizmo",      # Gizmo's OWN main intro (intro_gizmo.py): after the hook and as the last four shots
      "cast": {"gizmo": {"voice": "am_michael", "speed": 0.85}},
      "title": "Where Does Rain Come From? Gizmo Explains", "thumb_text": "DRIP DROP!", "series": "Gizmo Explains",
      "description": ("Where does rain come from? Gizmo the robot watches a puddle shrink in the sun, floats up into the cold sky, looks inside a cloud and "
                      "follows the rain down the hills to the sea. A gentle science lesson for ages 4-8 with questions to answer, things to try and a quiz at the end.\n"
                      "Kids learn that the sun warms water and turns it into invisible water vapor that floats up (evaporation), that cold air high up turns the "
                      "vapor back into tiny drops that form on specks of dust and make clouds (condensation), that tiny drops join into bigger drops and fall as "
                      "rain or snow, and that the water flows downhill to rivers, lakes and the ocean: the water cycle, always happening, everywhere.\n\n"
                      + BOILER + "\n\n" + SRC),
      "tags": ["where does rain come from", "water cycle for kids", "rain for kids", "clouds for kids", "evaporation for kids", "condensation for kids",
               "science for kids", "weather for kids", "Gizmo Explains", "Gizmo the robot", "preschool science", "kindergarten science"]}

GX, GY, GS = 700, 900, .7
STAGES = {"glab": [("gizmo", "gizmo", GX, GY, GS)],
          "gbench": [("gizmo", "gizmo", 520, 860, .66)],
          "gwindow": [("gizmo", "gizmo", 560, 900, .66)],
          "gpark": [("gizmo", "gizmo", 470, 960, .6)],       # on the grass, left of the path
          "gsky": [("gizmo", "gizmo", 300, 760, .5)],        # never in the picture (hidden in every gsky shot)
          "ghills": [("gizmo", "gizmo", 300, 760, .5)], **GZ_INTRO_STAGES}     # never in the picture (hidden in every ghills shot)
K = Kit(STAGES); P, C, V, WV = K.P, K.C, K.V, K.WV
WIDE = (960, 540, 1920)
GQ = lambda place: WV(place, ["gizmo"], floor=.70, top=.46)
GP = lambda place: WV(place, ["gizmo"], floor=.72, top=.42)
GPL = lambda place: WV(place, ["gizmo"], floor=.62, top=.42)        # Gizmo smaller: room for a word under him
GCAM = lambda place, w=1000: C(place, "gizmo", "all", w)


# ------------------------------------------------------------------ moves of the water
def RISE(at, sel, dy=150, d=3.0, what="the vapor floats up"): return [("to", at, sel + "-v", {"opacity": 1, "duration": .6}, what), ("to", at, sel + "-v", {"y": f"-={dy}", "duration": d, "ease": "sine.out"}, "")]
def RAIN(at, sel, what="the rain falls", n=9): return [("to", at, sel + "-rain", {"opacity": 1, "duration": .3}, what), ("fromto", at, sel + "-rain", {"y": 0}, {"y": 70, "duration": .5, "ease": "none", "repeat": n}, "")]
def SNOW(at, sel, what="snow falls", n=5): return [("to", at, sel + "-snow", {"opacity": 1, "duration": .4}, what), ("fromto", at, sel + "-snow", {"y": 0, "x": 0}, {"y": 60, "x": 14, "duration": .9, "ease": "sine.inOut", "repeat": n, "yoyo": False}, "")]
def GREY(at, sel, what="the cloud turns grey and heavy"): return ("to", at, sel + "-grey", {"opacity": 1, "duration": .8}, what)
def SHRINK(at, sel, s=.4, d=3.6, what="the puddle gets smaller"): return ("to", at, sel, {"scale": s, "transformOrigin": "50% 50%", "duration": d, "ease": "sine.inOut"}, what)
def MAKE_CLOUD(at, sel, what="the tiny drops make a cloud"): return [("to", at, sel + "-cl", {"opacity": 1, "duration": 1.0}, what), ("to", at, sel + "-dots", {"opacity": 0, "duration": 1.0}, "")]
def JOIN(at, sel, what="the tiny drops join into one big drop"):
    return [("to", at, sel + "-a", {"x": 170, "duration": 1.0, "ease": "power1.in"}, what), ("to", at, sel + "-b", {"x": -170, "duration": 1.0, "ease": "power1.in"}, ""),
            ("to", at, sel + "-c", {"y": 150, "duration": 1.0, "ease": "power1.in"}, ""),
            ("to", at, sel + "-big", {"opacity": 1, "duration": .25, "delay": 1.0}, ""),
            ("to", at, f"{sel}-a,{sel}-b,{sel}-c", {"opacity": 0, "duration": .2, "delay": 1.0}, "")]
def BIGDROP(sel): return [("fromto", 0, f"{sel}-a,{sel}-b,{sel}-c", {"opacity": 0}, {"opacity": 0, "duration": .01}, ""), ("fromto", 0, sel + "-big", {"opacity": 1}, {"opacity": 1, "duration": .01}, "")]
def FLOW(at, sel, n, step=.5, what="the water flows downhill"): return [("to", at, f"{sel}-a{k}", {"opacity": 1, "duration": .3, "delay": k * step}, what if k == 0 else "") for k in range(n)]


# ------------------------------------------------------------------ places and cameras
PARK = (960, 560, 1920); PARKP = (900, 600, 1700)
PX, PY = 1250, 900                         # the puddle on the path
SUNX, SUNY = 1560, 330                     # the sun over the park (a prop)
PUDC = (1300, 620, 1700); PUDP = (1300, 720, 1350)      # the whole puddle above the caption, the sun inside the top (stills r1)
def pud(s=1.0): return prop("pd", A.puddle, PX, PY, s, p=(PX, PY, s))
def psun(): return prop("sn", G.warm_sun, SUNX, SUNY, .8, p=(SUNX - 120, SUNY + 130, .7))
def pvap(): return prop("vp", A.vapor, PX, PY - 40, 1.0, p=(PX, PY - 40, 1.0))
PARKG = GCAM("gpark", 1150)      # 1000 cut the antenna (stills r1)

BOARD = (960, 540, 1500); PBOARD = (960, 470, 1700)
SKY = (960, 540, 1920); SKYC = (960, 520, 1300); SKYP = (960, 560, 1500)
HILL = (960, 540, 1920); HILLP = (700, 560, 1500); RAINC = (520, 420, 1300); RAINP = (520, 520, 1400)
CX, CY = 520, 220                          # the rain cloud over the tall hill
def rcloud(s=1.0, y=CY): return prop("cl", A.cloud, CX, y, s, p=(CX, y + 60, .9))
WIN = (960, 520, 1700); WINP = (1000, 430, 1150)
BEN = (960, 540, 1800); BENP = (900, 560, 1500)

# on the board (props low: the answer signs at the top never touch them)
def b_sun(): return prop("bs", G.warm_sun, 760, 560, .72, p=(800, 560, .6))      # low: the answer signs at the top never touch the rays (stills r1)
def b_sea(): return prop("bw", A.sea, 960, 760, 1.0, p=(960, 700, .8))
def b_vap(): return prop("bv", A.vapor, 1160, 800, 1.1, p=(1100, 720, .9))
def b_heat(): return prop("bh", A.heat, 960, 720, 1.0, p=(960, 680, .8))
def b_speck(): return prop("sp", A.speck, 960, 680, 1.6, p=(960, 660, 1.4))      # 9:16: board props between the signs and the caption (0.45-0.70 of the view)
def b_dots(): return prop("dc", A.dots_cloud, 960, 680, 1.4, p=(960, 660, 1.1))
def b_join(): return prop("jn", A.join, 960, 660, 1.3, p=(960, 640, 1.1))
def b_cycle(): return prop("cy", A.wcycle, 960, 530, .72, p=(960, 640, .55))


SHOTS = [
    # ---------------------------------------------------------------- HOOK
    S("ghills", RAINC, "Where does rain come from? Who fills up the clouds?", q=True, tag="hook: rain from the cloud", pcam=RAINP, hide=["gizmo"],
      props=[rcloud()], fx=[GREY(0.1, "#{p}cl")] + RAIN("w:rain", "#{p}cl", n=12), words=[("w:clouds?", "?", .82, .3, 2.0, "sun", (.75, .4), 1.3)]),
    S("ghills", HILL, "Drip, drop! The rain falls on the hills.", tag="hook: rain on the hills", pcam=HILLP, hide=["gizmo"], cam2=W(HILL, 1.0),
      props=[rcloud()], fx=[GREY(0, "#{p}cl")] + RAIN(0.05, "#{p}cl", n=8), words=[("w:Drip,", "DRIP, DROP!", .7, .3, 1.0, "sun", (.5, .4), .9)]),
    S("glab", (GX, 640, 1000), "Hi! I'm Gizmo. Let's find out where rain comes from!", tag="hook: Gizmo", pcam=GP("glab"), fx=[WAVE("w:Hi!"), HOP("w:find")],
      words=[("w:Gizmo.", "GIZMO", .78, .3, 1.1, "pill", (.5, .36), .9)]),
    # ---------------------------------------------------------------- MAIN INTRO (right after the hook; again as the last four shots)
    *gz_intro_shots(),
    S("glab", WIDE, "Welcome to my lab, weather fans!", trans="iris", tag="lab wide", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=[WAVE("w:Welcome", 4)],
      words=[("w:lab,", "HELLO!", .74, .5, 1.2, "pill", (.5, .36), 1.0)]),
    S("gbench", BEN, "Today we follow some water, all the way around!", tag="bench wide", pcam=BENP, props=[prop("bd", G.drop, 1240, 640, 1.4, p=(1180, 620, 1.2))],
      fx=[PULSE("w:water,", "#{p}bd", 3, 1.08)], words=[("w:around!", "ALL THE WAY!", .5, .14, .95, "sun", (.5, .36), .8)]),
    # ---------------------------------------------------------------- PART 1: the sun warms the water, the vapor floats up
    S("gpark", PARK, "After the rain, there is a puddle in the park.", part=1, tag="the puddle", pcam=PARKP, cam2=W(PARK, 1.0), props=[pud(), psun()],
      fx=[PULSE("w:puddle", "#{p}pd", 3, 1.04)], words=[("w:puddle", "A PUDDLE!", .7, .3, 1.0, "sun", (.5, .36), .9)]),
    S("gpark", PUDC, "Out comes the sun. It warms the water in the puddle.", part=1, tag="the sun warms it", pcam=PUDP, hide=["gizmo"], props=[pud(), psun(), prop("ph", A.heat, PX, PY - 60, 1.0, p=(PX, PY - 60, 1.0))],
      fx=[("to", "w:sun.", "#{p}sn-rays", {"rotation": 30, "transformOrigin": "50% 50%", "duration": 3.0, "ease": "none"}, "the sun's rays turn"), ON("w:warms", "#{p}ph-h", "warm lines rise from the puddle")],
      words=[("w:warms", "WARM!", .2, .3, 1.1, "sun", (.3, .4), .9)]),
    S("ghills", (1700, 560, 1100), "The sun warms lakes, and the ocean too. Vapor rises from them!", part=1, tag="the ocean too", pcam=(1750, 560, 1100), hide=["gizmo"],
      props=[prop("ov", A.vapor, 1900, 680, 1.0, p=(1800, 680, 1.0)), prop("os", G.warm_sun, 2050, 330, .6, p=(1900, 260, .5))],
      fx=RISE("w:Vapor", "#{p}ov", 140, 3.0), words=[("w:ocean", "THE OCEAN!", .3, .3, 1.0, "sun", (.36, .4), .8)]),
    S("paper_gz", BOARD, "What does the sun give the water? Heat, or snow?", part=1, q=True, tag="question 1", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_sun(), b_sea()],
      fx=[("to", 0.2, "#{p}bs-rays", {"rotation": 30, "transformOrigin": "50% 50%", "duration": 6.0, "ease": "none"}, "the sun's rays turn"), ("signs", "w:Heat,", ["HEAT", "SNOW"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Heat! The sun's heat makes the water cycle work.", part=1, tag="heat", pcam=PBOARD, props=[b_sun(), b_sea(), b_heat()],
      fx=[ON("w:Heat!", "#{p}bh-h", "warm lines rise from the water"), PULSE("w:sun's", "#{p}bs", 3, 1.06)], words=[("w:Heat!", "HEAT!", .78, .3, 1.1, "sun", (.75, .38), .9)]),
    S("gpark", PUDC, "Look! The puddle gets smaller, and smaller.", part=1, tag="the puddle shrinks", pcam=PUDP, hide=["gizmo"], props=[pud(), psun()],
      fx=[SHRINK("w:Look!", "#{p}pd", .45, 3.6)], words=[("w:smaller,", "SMALLER!", .24, .3, 1.0, "sun", (.3, .4), .85)]),
    S("gpark", PARKG, "Where did the water go? Let's think!", part=1, q=True, tag="think", pause=.6, pcam=GPL("gpark"), props=[pud(.45), psun()],
      fx=[("face", "w:Where", "gizmo", "wow")] + IDEA("w:think!"), words=[("w:go?", "WHERE?", .8, .3, 1.0, "sun", (.5, .67), .9)]),
    S("gpark", PUDC, "The warm water turns into a gas. It is called water vapor.", part=1, tag="water vapor", pcam=PUDP, hide=["gizmo"], props=[pud(.45), psun(), pvap()],
      fx=RISE("w:gas.", "#{p}vp", 160, 3.4), words=[("w:vapor.", "WATER VAPOR", .26, .2, .9, "sun", (.36, .4), .7)]),
    S("paper_gz", BOARD, "Can we see water vapor? Yes, or no?", part=1, q=True, tag="question 2", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_sea()],
      fx=[("signs", "w:Yes,", ["YES", "NO"], 1, "wait:2.0")]),
    S("paper_gz", BOARD, "Water vapor is invisible! We drew it as little dots, so you can see it.", part=1, tag="invisible", pcam=PBOARD, props=[b_sea(), b_vap()],
      fx=RISE("w:dots,", "#{p}bv", 120, 3.0, "little dots show the vapor"), words=[("w:invisible!", "INVISIBLE!", .3, .3, 1.0, "sun", (.5, .38), .85)]),
    S("gsky", SKYC, "The vapor floats high into the sky.", part=1, tag="vapor floats high", pcam=SKYP, hide=["gizmo"], props=[prop("sv", A.vapor, 960, 1000, 1.4, p=(960, 1050, 1.3))],
      fx=RISE(0.1, "#{p}sv", 300, 4.0), words=[("w:high", "HIGH!", .76, .3, 1.1, "sun", (.75, .4), .9)]),
    S("glab", GCAM("glab"), "Point up to the sky, where the vapor goes!", part=1, q=True, tag="point up", pause=1.2, pcam=GPL("glab"), fx=UP("w:Point", 2.0),
      words=[("w:Point", "POINT UP!", .8, .3, 1.0, "sun", (.5, .67), .85)]),
    S("gsky", SKYC, "Where does the vapor go? Up to the sky, or under the ground?", part=1, q=True, tag="question 2b", pause=3.2, pcam=SKYP, hide=["gizmo"], cam2=(960, 540, 1200),
      props=[prop("sv", A.vapor, 960, 1000, 1.4, p=(960, 1050, 1.3))], fx=RISE(0.1, "#{p}sv", 200, 5.0) + [("signs", "w:Up", ["THE SKY", "GROUND"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Water turns into vapor. This is called evaporation!", part=1, tag="evaporation", pcam=PBOARD, props=[b_sun(), b_sea(), b_vap()],
      fx=RISE("w:vapor.", "#{p}bv", 120, 3.0), words=[("w:evaporation!", "EVAPORATION", .5, .14, .85, "sun", (.5, .38), .6)]),
    S("glab", GCAM("glab"), "Wiggle your fingers and float them up, like vapor!", part=1, q=True, tag="wiggle up", pause=1.2, pcam=GPL("glab"), fx=UP("w:float", 2.0),
      words=[("w:Wiggle", "WIGGLE UP!", .8, .3, .9, "sun", (.5, .67), .8)]),
    S("gbench", (900, 560, 1500), "Say it with me. The sun warms the water!", part=1, q=True, tag="say it", pcam=GPL("gbench"), fx=[HOP("w:warms")],
      words=[("w:sun", "SUN WARMS WATER!", .55, .2, .8, "sun", (.5, .36), .6)]),
    S("paper_gz", BOARD, "What does warm water turn into? Vapor, or sand?", part=1, q=True, tag="question 3", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_sun(), b_sea()],
      fx=[("signs", "w:Vapor,", ["VAPOR", "SAND"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Vapor! The sun warms the water, and the vapor floats up.", part=1, tag="part 1 recap", pcam=PBOARD, props=[b_sun(), b_sea(), b_heat(), b_vap()],
      fx=[ON("w:warms", "#{p}bh-h")] + RISE("w:floats", "#{p}bv", 120, 2.6), words=[("w:up.", "UP!", .8, .3, 1.1, "sun", (.75, .38), .9)]),
    # ---------------------------------------------------------------- PART 2: cold up high, tiny drops, clouds
    S("gsky", SKY, "High up in the sky, the air is very cold.", part=2, trans="iris", tag="cold up high", pcam=SKYP, hide=["gizmo"], cam2=W(SKY, 1.0),
      props=[prop("sf", A.snowflake, 1500, 260, .6, p=(1150, 320, .5))], fx=[("to", "w:cold.", "#{p}sf", {"rotation": 60, "transformOrigin": "50% 50%", "duration": 2.4}, "a snowflake turns")],
      words=[("w:cold.", "COLD!", .3, .3, 1.2, "sun", (.36, .4), 1.0)]),
    S("gsky", SKYC, "The cold turns the vapor back into tiny drops of water.", part=2, tag="back into drops", pcam=SKYP, hide=["gizmo"], props=[prop("dc", A.dots_cloud, 960, 520, 1.2, p=(960, 560, 1.1))],
      fx=[("fromto", "w:tiny", "#{p}dc-dots", {"opacity": 0}, {"opacity": 1, "duration": 1.2}, "tiny drops appear")], words=[("w:drops", "TINY DROPS", .5, .2, .9, "sun", (.5, .62), .75)]),
    S("glab", GCAM("glab"), "Back into water? Let's look closer!", part=2, q=True, tag="look closer", pause=.4, pcam=GPL("glab"), fx=[("face", "w:Back", "gizmo", "wow")] + IDEA("w:closer!"),
      words=[("w:closer!", "CLOSER!", .8, .3, 1.0, "sun", (.5, .67), .9)]),
    S("paper_gz", BOARD, "Each tiny drop forms on a tiny speck of dust, smoke, or salt.", part=2, tag="speck of dust", pcam=PBOARD, props=[b_speck(), prop("mg", G.magnifier, 1350, 420, .8, p=(1240, 480, .5))],
      fx=[("to", "w:forms", "#{p}sp-drop", {"opacity": 1, "duration": 1.0}, "a drop forms around the speck")], words=[("w:speck", "A SPECK!", .24, .3, 1.0, "sun", (.3, .38), .85)]),
    S("paper_gz", BOARD, "What does a tiny drop form on? A speck of dust, or a shoe?", part=2, q=True, tag="question 4", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_speck()],
      fx=[("signs", "w:speck", ["DUST", "A SHOE"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "A speck of dust! So tiny, you can not see it.", part=2, tag="dust", pcam=PBOARD, props=[b_speck()],
      fx=[ON("w:dust!", "#{p}sp-drop", "a drop forms around the speck"), PULSE("w:tiny,", "#{p}sp", 3, 1.06)], words=[("w:dust!", "DUST!", .76, .3, 1.1, "sun", (.75, .38), .9)]),
    S("paper_gz", BOARD, "Lots and lots of tiny drops make a cloud!", part=2, tag="drops make a cloud", pcam=PBOARD, props=[b_dots()],
      fx=MAKE_CLOUD("w:make", "#{p}dc"), words=[("w:Lots", "LOTS!", .24, .3, 1.0, "sun", (.3, .38), .85), ("w:cloud!", "A CLOUD!", .76, .3, 1.0, "sun", (.72, .38), .85)]),
    S("gsky", SKYC, "Vapor turns back into water. This is called condensation!", part=2, tag="condensation", pcam=SKYP, hide=["gizmo"], props=[prop("dc", A.dots_cloud, 960, 520, 1.2, p=(960, 560, 1.1))],
      fx=MAKE_CLOUD("w:water.", "#{p}dc"), words=[("w:condensation!", "CONDENSATION", .5, .2, .8, "sun", (.5, .64), .55)]),
    S("gwindow", WIN, "You can see this at home! On a cold winter day, look at a window.", part=2, tag="winter window", pcam=(960, 430, 1150), hide=["gizmo"], props=[prop("ww", A.winter_window, 960, 350, 1.0, p=(960, 350, 1.0))],
      fx=[PULSE("w:window.", "#{p}ww", 1, 1.01)], words=[("w:winter", "WINTER", .78, .14, 1.0, "sun", (.5, .36), .85)]),
    S("gwindow", (960, 450, 1100), "Drops of water form on the inside of the glass!", part=2, tag="drops on the glass", pcam=(960, 430, 1000), hide=["gizmo"], props=[prop("ww", A.winter_window, 960, 350, 1.0, p=(960, 350, 1.0))],
      fx=[("to", "w:Drops", "#{p}ww-drops", {"opacity": 1, "duration": 1.6}, "drops form on the glass")], words=[("w:inside", "INSIDE!", .5, .14, 1.0, "sun", (.5, .38), .85)]),
    S("gwindow", (960, 450, 1100), "Where do drops form at home on a cold day? On a window, or on a pillow?", part=2, q=True, tag="question 5b", pause=3.2, pcam=(960, 430, 1000), hide=["gizmo"],
      cam2=(960, 440, 1000), props=[prop("ww", A.winter_window, 960, 350, 1.0, p=(960, 350, 1.0))],
      fx=[("fromto", 0, "#{p}ww-drops", {"opacity": 1}, {"opacity": 1, "duration": .01}, ""), ("signs", "w:window,", ["WINDOW", "PILLOW"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Is condensation the same as evaporation, or the opposite?", part=2, q=True, tag="question 5", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_dots()],
      fx=[("signs", "w:same", ["SAME", "OPPOSITE"], 1, "wait:2.0")]),
    S("paper_gz", BOARD, "The opposite! Water goes up as vapor, and comes back as drops.", part=2, tag="the opposite", pcam=PBOARD,
      props=[prop("uu", R.updown, 760, 640, 1.0, p=(800, 660, .8)), prop("dd", R.updown, 1160, 640, 1.0, p=(1120, 660, .8))], fx=[ON("w:up", "#{p}uu-upa", "an arrow points up"), ON("w:back", "#{p}dd-dn", "an arrow points down")],
      words=[("w:up", "UP!", .3, .3, 1.1, "sun", (.3, .44), .9), ("w:drops.", "DROPS!", .74, .72, 1.0, "", (.72, .66), .85)]),
    S("glab", GCAM("glab"), "Make a big round cloud with your arms!", part=2, q=True, tag="cloud arms", pause=1.2, pcam=GPL("glab"), fx=WIDEARMS("w:round", 2.2),
      words=[("w:cloud", "BIG CLOUD!", .8, .3, 1.0, "sun", (.5, .67), .85)]),
    S("gbench", (900, 560, 1500), "Say it with me. Cold air makes clouds!", part=2, q=True, tag="say it 2", pcam=GPL("gbench"), fx=[HOP("w:clouds!")],
      words=[("w:Cold", "COLD AIR, CLOUDS!", .55, .2, .8, "sun", (.5, .36), .6)]),
    S("gsky", SKYC, "What is a cloud made of? Tiny drops of water, or cotton candy?", part=2, q=True, tag="question 6", pause=3.2, pcam=SKYP, hide=["gizmo"], cam2=(960, 540, 1200),
      props=[prop("cc", A.cloud, 960, 720, 1.1, p=(960, 800, 1.0))], fx=[("signs", "w:Tiny", ["TINY DROPS", "CANDY"], 0, "wait:2.0")]),
    S("gsky", SKYC, "Tiny drops of water, high up in the cold sky!", part=2, tag="part 2 recap", pcam=SKYP, hide=["gizmo"], props=[prop("dc", A.dots_cloud, 960, 560, 1.2, p=(960, 600, 1.1))],
      fx=MAKE_CLOUD("w:high", "#{p}dc"), words=[("w:Tiny", "TINY DROPS!", .5, .14, 1.0, "sun", (.5, .38), .85)]),
    # ---------------------------------------------------------------- PART 3: drops join, fall as rain, flow to the sea
    S("paper_gz", BOARD, "Inside a cloud, the tiny drops bump together.", part=3, trans="iris", tag="drops bump", pcam=PBOARD, props=[b_join()],
      fx=[("to", "w:bump", "#{p}jn-a", {"x": 40, "duration": .3, "yoyo": True, "repeat": 3}, "the drops bump"), ("to", "w:bump", "#{p}jn-b", {"x": -40, "duration": .3, "yoyo": True, "repeat": 3}, "")],
      words=[("w:bump", "BUMP!", .24, .3, 1.1, "sun", (.3, .38), .9)]),
    S("paper_gz", BOARD, "They join, and grow into bigger drops!", part=3, tag="they join", pcam=PBOARD, props=[b_join()], fx=JOIN("w:join,", "#{p}jn"),
      words=[("w:bigger", "BIGGER!", .76, .3, 1.1, "sun", (.72, .38), .9)]),
    S("paper_gz", BOARD, "Big drops are heavy. What happens next? They fall, or float away?", part=3, q=True, tag="question 7", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390), props=[b_join()],
      fx=BIGDROP("#{p}jn") + [("signs", "w:fall,", ["FALL", "FLOAT AWAY"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "They fall! Gravity pulls them down to the ground.", part=3, tag="they fall", pcam=PBOARD, props=[b_join()],
      fx=BIGDROP("#{p}jn") + [("to", "w:pulls", "#{p}jn-big", {"y": 160, "duration": 1.2, "ease": "power2.in"}, "the big drop falls")], words=[("w:fall!", "FALL!", .24, .3, 1.1, "sun", (.3, .38), .9)]),
    S("ghills", RAINC, "Down comes the rain! Pitter, patter!", part=3, tag="down comes the rain", pcam=RAINP, hide=["gizmo"], props=[rcloud()],
      fx=[GREY(0, "#{p}cl")] + RAIN("w:Down", "#{p}cl", n=9), words=[("w:Pitter,", "PITTER, PATTER!", .64, .3, .9, "sun", (.55, .44), .62)]),
    S("ghills", RAINC, "When it is very cold, the drops can fall as snow.", part=3, tag="snow", pcam=RAINP, hide=["gizmo"], props=[rcloud()],
      fx=[GREY(0, "#{p}cl")] + SNOW("w:cold,", "#{p}cl"), words=[("w:snow.", "SNOW!", .8, .3, 1.1, "sun", (.75, .4), .9)]),
    S("paper_gz", BOARD, "What can fall from a very cold cloud? Snow, or leaves?", part=3, q=True, tag="question 7b", pause=3.2, pcam=PBOARD, cam2=(960, 555, 1390),
      props=[prop("bf", A.snowflake, 960, 700, 1.3, p=(960, 680, 1.1))], fx=[("to", 0.2, "#{p}bf", {"rotation": 60, "transformOrigin": "50% 50%", "duration": 6.0, "ease": "none"}, "the snowflake turns"),
      ("signs", "w:Snow,", ["SNOW", "LEAVES"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Snow! Soft, white snow comes from clouds too.", part=3, tag="snow answer", pcam=PBOARD, props=[prop("bf", A.snowflake, 960, 700, 1.3, p=(960, 680, 1.1))],
      fx=[PULSE("w:Snow!", "#{p}bf", 3, 1.08)], words=[("w:Snow!", "SNOW!", .24, .3, 1.1, "sun", (.3, .38), .9)]),
    S("glab", GCAM("glab"), "Tap your fingers on your legs, like falling rain!", part=3, q=True, tag="tap like rain", pause=1.4, pcam=GPL("glab"), fx=DOWN("w:Tap", 2.4),
      words=[("w:Tap", "TAP, TAP!", .8, .3, 1.0, "sun", (.5, .67), .9)]),
    S("ghills", HILL, "The rain flows downhill, into a river.", part=3, tag="downhill", pcam=HILLP, hide=["gizmo"], cam2=W(HILL, 1.0),
      props=[prop("fl", lambda p: A.flow(p, [(170, 300, 330, 520), (520, 640, 860, 720), (1000, 800, 1400, 740)]), 0, 0, 1.0, p=(0, 0, 1.0))],
      fx=FLOW("w:flows", "#{p}fl", 3, .6), words=[("w:downhill,", "DOWNHILL!", .7, .3, 1.0, "sun", (.5, .4), .85)]),
    S("ghills", (1350, 640, 1300), "Rivers carry the water to lakes, and to the ocean.", part=3, tag="to the ocean", pcam=(1500, 640, 1300), hide=["gizmo"],
      props=[prop("fl", lambda p: A.flow(p, [(1000, 800, 1400, 740), (1700, 690, 2100, 690)]), 0, 0, 1.0, p=(0, 0, 1.0))],
      fx=FLOW("w:Rivers", "#{p}fl", 2, 1.0), words=[("w:ocean.", "THE OCEAN!", .7, .25, 1.0, "sun", (.5, .4), .8)]),
    S("gpark", PUDC, "And look! The rain fills up the puddle in the park again.", part=3, tag="the puddle fills", pcam=PUDP, hide=["gizmo"],
      props=[pud(.45), prop("pc", A.cloud, 1250, 320, .9, p=(1300, 480, .8))], fx=[GREY(0, "#{p}pc")] + RAIN(0.05, "#{p}pc", n=9) + [("to", "w:fills", "#{p}pd", {"scale": 2.2, "transformOrigin": "50% 50%", "duration": 3.0, "ease": "sine.inOut"}, "the puddle fills up")],
      words=[("w:again.", "AGAIN!", .2, .3, 1.0, "sun", (.3, .4), .85)]),
    S("ghills", HILL, "Which way does rain water flow? Downhill, or uphill?", part=3, q=True, tag="question 8", pause=3.2, pcam=HILLP, hide=["gizmo"], cam2=(900, 560, 1700),
      fx=[("signs", "w:Downhill,", ["DOWNHILL", "UPHILL"], 0, "wait:2.0")]),
    S("paper_gz", BOARD, "Then the sun warms the water again. Round and round it goes!", part=3, tag="round and round", pcam=PBOARD, props=[b_cycle()],
      fx=[PULSE("w:sun", "#{p}cy-k0", 1, 1.08), ("to", "w:Round", "#{p}cy-k1", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 1}, "the circle lights up step by step"),
          ("to", "w:Round", "#{p}cy-k2", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 1, "delay": .5}, ""), ("to", "w:Round", "#{p}cy-k3", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 1, "delay": 1.0}, ""),
          ("to", "w:Round", "#{p}cy-k0", {"scale": 1.12, "transformOrigin": "50% 50%", "duration": .25, "yoyo": True, "repeat": 1, "delay": 1.5}, "")],
      words=[("w:Round", "ROUND!", .2, .3, 1.0, "sun", (.25, .36), .8)]),
    S("paper_gz", BOARD, "This is the water cycle. It is always happening, everywhere!", part=3, tag="the water cycle", pcam=PBOARD, props=[b_cycle()],
      fx=[PULSE("w:cycle.", "#{p}cy", 1, 1.04)], words=[("w:cycle.", "WATER CYCLE", .2, .2, .8, "sun", (.5, .36), .62)]),
    S("paper_gz", BOARD, "Let's count the steps. Warm, rise, cloud, rain!", part=3, q=True, tag="count steps", pcam=PBOARD, props=[b_cycle()],
      fx=[PULSE("w:Warm,", "#{p}cy-k0", 1, 1.1), PULSE("w:rise,", "#{p}cy-k1", 1, 1.1), PULSE("w:cloud,", "#{p}cy-k2", 1, 1.1), PULSE("w:rain!", "#{p}cy-k3", 1, 1.1)],
      words=[("w:Warm,", "1", .63, .88, 1.1, "sun", (.34, .68), .8), ("w:rise,", "2", .3, .5, 1.1, "sun", (.12, .58), .8), ("w:cloud,", "3", .63, .14, 1.1, "sun", (.66, .46), .8), ("w:rain!", "4", .78, .5, 1.1, "sun", (.88, .58), .8)]),
    S("glab", GCAM("glab"), "Spin around slowly, like the water cycle!", part=3, q=True, tag="spin", pause=1.2, pcam=GPL("glab"),
      fx=[("to", "w:Spin", "#{p}gizmo-body", {"scaleX": -1, "svgOrigin": "0 0", "duration": .6, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, "Gizmo turns around")],
      words=[("w:Spin", "SPIN!", .8, .3, 1.1, "sun", (.5, .67), .9)]),
    S("gbench", (900, 560, 1500), "Say it with me. Round and round goes the water!", part=3, q=True, tag="say it 3", pcam=GPL("gbench"), fx=[HOP("w:water!")],
      words=[("w:Round", "ROUND AND ROUND!", .55, .2, .8, "sun", (.5, .36), .6)]),
    # ---------------------------------------------------------------- QUIZ + GOODBYE
    S("glab", WIDE, "Quiz time! Let's remember what we learned.", part=4, trans="iris", tag="quiz time", cam2=W(WIDE, 1.0), pcam=(GX + 60, 640, 1500), fx=IDEA("w:Quiz"),
      words=[("w:Quiz", "QUIZ TIME!", .74, .5, 1.3, "sun", (.5, .36), 1.0)]),
    S("gpark", PUDC, "What warms the water in the puddle? The sun, or the moon?", part=4, q=True, tag="quiz 1", pause=3.2, pcam=PUDP, hide=["gizmo"], cam2=(1300, 610, 1400), props=[pud(), psun()],
      fx=[("signs", "w:sun,", ["THE SUN", "THE MOON"], 0, "wait:2.0")]),
    S("gpark", PUDC, "The sun! The water floats up as vapor.", part=4, tag="quiz 1 answer", pcam=PUDP, hide=["gizmo"], props=[pud(), psun(), pvap()],
      fx=RISE("w:floats", "#{p}vp", 160, 3.0) + [SHRINK("w:floats", "#{p}pd", .5, 3.0)], words=[("w:sun!", "THE SUN!", .24, .3, 1.0, "sun", (.3, .4), .85)]),
    S("gsky", SKYC, "What makes a cloud? Tiny drops of water, or tiny rocks?", part=4, q=True, tag="quiz 2", pause=3.2, pcam=SKYP, hide=["gizmo"], trans="iris", cam2=(960, 540, 1200),
      props=[prop("cc", A.cloud, 960, 720, 1.1, p=(960, 800, 1.0))], fx=[("signs", "w:Tiny", ["WATER DROPS", "ROCKS"], 0, "wait:2.0")]),
    S("gsky", SKYC, "Tiny drops of water, in the cold air!", part=4, tag="quiz 2 answer", pcam=SKYP, hide=["gizmo"], props=[prop("dc", A.dots_cloud, 960, 560, 1.2, p=(960, 600, 1.1))],
      fx=MAKE_CLOUD("w:water,", "#{p}dc"), words=[("w:cold", "COLD AIR!", .5, .2, 1.0, "sun", (.5, .64), .8)]),
    S("ghills", RAINC, "Why do drops fall as rain? They get heavy, or they get sleepy?", part=4, q=True, tag="quiz 3", pause=3.2, pcam=RAINP, hide=["gizmo"], trans="iris", cam2=(520, 430, 1200),
      props=[rcloud(.9, 470)], fx=[GREY(0, "#{p}cl"), ("signs", "w:heavy,", ["HEAVY", "SLEEPY"], 0, "wait:2.0")]),
    S("ghills", RAINC, "They get heavy! Down comes the rain.", part=4, tag="quiz 3 answer", pcam=RAINP, hide=["gizmo"], props=[rcloud(.9, 470)],
      fx=[GREY(0, "#{p}cl")] + RAIN("w:Down", "#{p}cl", n=6), words=[("w:heavy!", "HEAVY!", .8, .3, 1.1, "sun", (.75, .4), .9)]),
    S("gpark", PARKG, "Sun, vapor, cloud, rain! Thanks for exploring with me!", part=4, tag="goodbye", pcam=GP("gpark"), props=[pud(), psun()],
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
    {"id": "gc_ep03_short1", "title": "Where Does a Puddle Go? Gizmo Explains", "band": ("WHERE DOES", "IT GO?"), "thumb_text": "POOF!", "part": 1,
     "extra_first": [S("gpark", PUDC, "Where does a puddle go when the sun comes out?", part=1, q=True, tag="hook: where does it go", pcam=PUDP, hide=["gizmo"], who="gizmo",
                       props=[pud(), psun()], fx=[SHRINK("w:puddle", "#{p}pd", .6, 3.0)], pcam2=W(PUDP, .94), words=[("w:out?", "?", .24, .3, 2.0, "sun", (.3, .4), 1.3)])]},
    {"id": "gc_ep03_short2", "title": "How Is a Cloud Made? Gizmo Explains", "band": ("HOW IS A CLOUD", "MADE?"), "thumb_text": "TINY DROPS", "part": 2,
     "extra_first": [S("gsky", SKYC, "How is a fluffy cloud made, up in the sky?", part=2, q=True, tag="hook: how is a cloud made", pcam=SKYP, hide=["gizmo"], who="gizmo", pcam2=W(SKYP, .94),
                       props=[prop("dc", A.dots_cloud, 960, 520, 1.2, p=(960, 560, 1.1))], fx=MAKE_CLOUD("w:made,", "#{p}dc"), words=[("w:sky?", "?", .76, .3, 2.0, "sun", (.75, .4), 1.3)])]},
    {"id": "gc_ep03_short3", "title": "Why Does Rain Fall Down? Gizmo Explains", "band": ("WHY DOES", "RAIN FALL?"), "thumb_text": "PLOP!", "part": 3,
     "extra_first": [S("ghills", RAINC, "Why does rain fall down from the clouds?", part=3, q=True, tag="hook: why does rain fall", pcam=RAINP, hide=["gizmo"], who="gizmo", pcam2=W(RAINP, .94),
                       props=[rcloud()], fx=[GREY(0, "#{p}cl")] + RAIN(0.1, "#{p}cl", n=8), words=[("w:clouds?", "?", .82, .3, 2.0, "sun", (.75, .4), 1.3)])]},
]
for _sp in SHORTS:
    for _s in _sp["extra_first"]:
        for _f in _s["fx"]:
            if _f[0] == "word" and len(_f) > 3 and "p" in _f[3] and _s["pcam"]: _f[3]["p"]["y"] = max(_f[3]["p"]["y"], round(_s["pcam"][1] - .15 * _s["pcam"][2]))


def _lit(fn, *parts):      # a prop drawn with some of its parts shown (for a thumbnail: no timeline there)
    def f(p):
        s = fn(p)
        for x in parts: s = s.replace(f'id="{p}-{x}" opacity="0"', f'id="{p}-{x}" opacity="1"')
        return s
    return f


# thumbnails (thumb.py): the example in the picture, 1-2 words, none of the title's words, no watermark
THUMBS = {
    "gc_ep03": {"place": "ghills", "cam": (620, 420, 1300), "actors": [],
                "props": [(_lit(A.cloud, "grey", "rain"), 760, 330, 1.25)],
                "words": [("DRIP", 1450, 300, 200, ""), ("DROP!", 1450, 560, 220, "sun")]},
    "gc_ep03_short1": {"place": "gpark", "cam": (1300, 640, 1400), "actors": [],
                       "props": [(A.puddle, PX, PY, 1.0), (G.warm_sun, 1400, 330, .9), (_lit(A.vapor, "v"), PX, PY - 40, 1.2)],
                       "words": [("POOF!", 540, 1500, 230, "sun")]},
    "gc_ep03_short2": {"place": "gsky", "cam": (960, 600, 1300), "actors": [],
                       "props": [(_lit(A.dots_cloud, "cl"), 960, 640, 1.4)],
                       "words": [("TINY", 540, 330, 220, ""), ("DROPS", 540, 1560, 220, "sun")]},
    "gc_ep03_short3": {"place": "ghills", "cam": (560, 560, 1300), "actors": [],
                       "props": [(_lit(A.cloud, "grey", "rain"), 560, 420, 1.3)],
                       "words": [("PLOP!", 540, 1520, 240, "sun")]},
}
