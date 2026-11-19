"""Gizmo Explains 3D explainers, first two (Nov 19 2026, docs/GIZMO_RUN.md). Facts read at their sources on Nov 19 2026 (quotes in "facts").
python3 make_gizmo_x1.py -> lessons/gzx_ep01.json (How Do Rockets Fly?), lessons/gzx_ep02.json (Where Does Rain Come From?)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = {"show": ["pal"]}
UPA = {"up": True, "color": "#3cc45a", "s": 1.2}; DNA = {"color": "#ff7a00", "s": 1.2}


def teach(name, biome, tod, word, lines, choices, check, exhibits, short):
    return {"name": name, "kind": "teach", "biome": biome, "tod": tod, "word": word, "visits": [P], "lines": lines,
            "choices": choices, "checks": [check], "exhibits": exhibits, "short": short}


def quiz(biome, tod, qs):
    lines = ["Wow! We found out so much today. Now it is quiz time!", "Get ready. Think hard!"]; checks = []
    for k, (q, a, b, right, ans) in enumerate(qs):
        lines += [{"t": q, "pause": 3.2}, ans]
        checks.append({"a": a, "b": b, "right": right, "ask": [2 + 2 * k], "answer": [3 + 2 * k], "hold": 2.0})
    return {"name": "quiz", "kind": "teach", "biome": biome, "tod": tod, "word": "QUIZ TIME!", "visits": [P], "lines": lines, "checks": checks,
            "word_off": [2]}


def ins(spec, segname, i, line):
    """Insert a line at index i of a segment and move every line reference (signs, exhibits, Short thumbnail) that points at i or later."""
    seg = next(g for g in spec["segments"] if g["name"] == segname)
    sh = lambda r: ([r[0] + 1] + list(r[1:])) if isinstance(r, list) and r and isinstance(r[0], int) and r[0] >= i else r
    for c in ([seg["choices"]] if seg.get("choices") else []) + seg.get("checks", []):
        c["ask"] = sh(c["ask"]); c["answer"] = sh(c["answer"])
    for e in seg.get("exhibits", []):
        for k in ("on", "off", "leave"):
            if k in e: e[k] = sh(e[k])
        if "times" in e: e["times"] = [sh(t) for t in e["times"]]
    if seg.get("short", {}).get("thumb_line"): seg["short"]["thumb_line"] = sh(seg["short"]["thumb_line"])
    seg["lines"].insert(i, line)


ROCKET = {
 "id": "gzx_ep01", "channel": "gizmo", "version": 3, "seed": 91, "voice": "af_heart", "speed": 0.84,
 "title": "How Do Rockets Fly? Science for Kids with Gizmo", "card": "How Rockets Fly!", "thumb_text": "UP, UP, AWAY!",
 "thumb_at": ["push", 4, 0.6],
 "description": ("How do rockets fly? Find out with Gizmo the robot: a rocket engine turns its fuel into hot gas and pushes it out the back, "
                 "and the gas pushes the rocket the other way. A rocket carries its own oxygen, so it works in space, and big rockets drop empty stages to get lighter.\n"
                 "A science explainer for kids ages 4-8, with questions to answer, things to copy, quick checks and a quiz at the end.\n\n"
                 "Where the facts come from (read Nov 19, 2026): NASA, What Is a Rocket? (Grades K-4 and Grades 5-8); "
                 "NASA Glenn Research Center, Practical Rocketry."),
 "tags": ["how do rockets fly", "rockets for kids", "rocket science for kids", "space for kids", "science for kids", "how things work for kids",
          "STEM for kids", "science explainer", "Gizmo Explains", "Gizmo the robot"],
 "cast": ["pal"], "extras": [],
 "facts": [
  "NASA, 'What Is a Rocket? (Grades K-4)', nasa.gov/learning-resources/for-kids-and-students/what-is-a-rocket-grades-k-4 (read Nov 19 2026): "
  "'Most rocket engines turn the fuel into hot gas.' 'The engine pushes the gas out its back.' 'The gas makes the rocket move forward.' "
  "'for every action, there is an equal and opposite reaction.' 'The rocket pushes the exhaust backward.' 'The exhaust makes the rocket move forward.' "
  "'A rocket engine doesn't need air.' 'It carries with it everything it needs.' 'A rocket engine works in space, where there is no air.'",
  "NASA, 'What Is a Rocket? (Grades 5-8)', nasa.gov/learning-resources/for-kids-and-students/what-is-a-rocket-grades-5-8 (read Nov 19 2026): "
  "'A jet engine requires oxygen from the air to work.' 'A rocket engine carries everything it needs.'",
  "NASA Glenn Research Center, 'Practical Rocketry', grc.nasa.gov/www/K-12/rocket/TRCRocket/practical_rocketry.html (read Nov 19 2026): "
  "'for burning to take place, an oxidizer (oxygen) must be present.' 'they must carry oxygen with them into space, where there is no air.' "
  "'When the large rocket was exhausted, the rocket casing was dropped behind and the remaining rocket fired.' 'Much higher altitudes were achieved by this method.' "
  "'Today this technique of building a rocket is called staging.' 'Thanks to staging, it has become possible not only to reach outer space but the Moon and other planets too.' "
  "'the heavier the rocket, the more the thrust needed to get it off the ground.'"],
 "improves": [
  "first Gizmo explainer: Gizmo hosts in his own lab and outdoor places (gizmoworld set), the example is a science model on the board (rocket with gas puffs, fuel and oxygen tanks, three-stage rocket that drops a stage)",
  "the quiz is three answer-sign rounds with thinking dots and confetti (teach board), so no check mark has to stand beside a face (open Zoo defect: quiz close-ups cut the neighbour)",
  "every example cued on the word that names it; no close-up while an example is up",
  "no real people named (the push-back rule is 'a rule scientists use', not a name), no fire shown (soft gas puffs), nothing to copy but hand and breathing moves"],
 "segments": [
  {"name": "hello", "kind": "intro", "biome": "spring_meadow", "tod": "morning", "word": "ROCKETS!", "lines": [
     "Hello, friends! I am Gizmo the robot.",
     "Today we are finding out how rockets fly!",
     "My little helper bot is here too. Hello, little bot!",
     "We have three big questions. Count them with me. One, two, three!",
     "Ready? Let's find out!"],
   "exhibits": [{"prop": "count", "at": [-0.75, -1.7, 3.55], "on": [3, "one"], "times": [[3, "one"], [3, "two"], [3, "three"]], "opts": {"n": 3, "dx": 0.75, "s": 1.0}}]},
  teach("push", "spring_meadow", "noon", "PUSH!", [
     {"t": "What pushes a rocket up, up into the sky?", "pause": 0.4},
     {"t": "Is it hot gas? Or is it the wind?", "pause": 3.2},
     "It is hot gas!",
     "Here is how it works. A rocket engine turns its fuel into hot gas.",
     "The engine pushes the gas out of its back. Whoosh! And the gas pushes the rocket the other way.",
     {"t": "So which way does the rocket go? Hmm.", "pause": 2.4},
     "The gas goes down, so the rocket goes up!",
     ["Up, up, up it goes!", "close:host"],
     "Scientists have a rule about pushes.",
     "For every push, there is a push back, just as big, the other way!",
     "The rocket pushes the gas backward. The gas pushes the rocket forward.",
     "A push, and a push back. That is how a rocket moves!",
     ["Say it with me. The gas goes down, the rocket goes up!", "close:host"],
     "Can you press your hands together? Push! Can you feel them push back?",
     "Push, and push back. Now let your hands rest.",
     {"t": "Quick check! The gas goes down. Which way does the rocket go? Up? Or down?", "pause": 3.2},
     "Up! Great thinking!"],
   {"a": "HOT GAS", "b": "WIND", "right": "a", "ask": [1], "answer": [2], "hold": 2.4},
   {"a": "UP", "b": "DOWN", "right": "a", "ask": [15], "answer": [16], "hold": 2.0},
   [{"prop": "rocket", "at": [2.55, -0.5, 0.0], "on": [3, "rocket"], "off": [5], "opts": {"gas": True, "s": 0.72}},
    {"prop": "arrow", "at": [1.45, -1.0, 2.55], "on": [4, "pushes", 1], "off": [5], "opts": UPA},
    {"prop": "arrow", "at": [1.45, -1.0, 0.35], "on": [4, "gas"], "off": [5], "opts": DNA},
    {"prop": "dots", "at": "dots", "on": [5, "end"], "off": [6]},
    {"prop": "rocket", "at": [2.55, -0.5, 0.0], "on": [6, "gas"], "off": [7], "opts": {"gas": True, "s": 0.72}},
    {"prop": "sign", "at": [1.95, -1.3, 3.3], "on": [8, "rule"], "off": [10], "opts": {"text": "PUSH BACK!", "color": "#3561d9"}},
    {"prop": "rocket", "at": [2.55, -0.5, 0.0], "on": [10, "rocket"], "off": [12], "opts": {"gas": True, "s": 0.72}},
    {"prop": "arrow", "at": [1.45, -1.0, 0.35], "on": [10, "gas"], "off": [12], "opts": DNA},
    {"prop": "arrow", "at": [1.45, -1.0, 2.55], "on": [10, "forward"], "off": [12], "opts": UPA}],
   {"id": "gzs_rocket_push", "title": "What Pushes a Rocket Up? Science for Kids", "l1": "WHAT PUSHES", "l2": "A ROCKET UP?", "thumb_text": "WHOOSH!", "thumb_line": [4, 0.6],
    "fact": "A rocket engine turns its fuel into hot gas and pushes it out the back; the gas pushes the rocket the other way (NASA, What Is a Rocket?)."}),
  teach("space", "lab", "noon", "NO AIR!", [
     {"t": "Can a rocket work in space, where there is no air?", "pause": 0.4},
     {"t": "Is it yes? Or is it no?", "pause": 3.2},
     "Yes, it can!",
     "Here is the fun fact. A rocket engine does not need air.",
     "It carries everything it needs, right inside the rocket!",
     {"t": "What does a rocket carry? Hmm.", "pause": 2.4},
     "Its fuel, and its very own oxygen! The fuel needs oxygen to work.",
     ["Ready for the trip to space!", "close:host"],
     "An airplane's jet engine is different.",
     "A jet engine takes the oxygen it needs from the air around it.",
     "But up in space, there is no air at all.",
     "So a rocket brings its own oxygen along. Smart rocket!",
     ["Say it with me. A rocket carries its own oxygen!", "close:host"],
     "Can you take a big breath of air, like a jet engine? Breathe in!",
     "And breathe out, nice and slow. Ahh.",
     {"t": "Quick check! Does a rocket need air from outside to work? Yes? Or no?", "pause": 3.2},
     "No! It brings its own oxygen. You remembered!"],
   {"a": "YES", "b": "NO", "right": "a", "ask": [1], "answer": [2], "hold": 2.4},
   {"a": "YES", "b": "NO", "right": "b", "ask": [15], "answer": [16], "hold": 2.0},
   [{"prop": "rocket", "at": [2.55, -0.5, 0.0], "on": [3, "rocket"], "off": [4], "opts": {"s": 0.8}},
    {"prop": "tanks", "at": [2.45, -0.6, 0.0], "on": [4, "carries"], "off": [5], "opts": {"s": 0.9}},
    {"prop": "dots", "at": "dots", "on": [5, "end"], "off": [6]},
    {"prop": "tanks", "at": [2.45, -0.6, 0.0], "on": [6, "fuel"], "off": [7], "opts": {"s": 0.9}},
    {"prop": "jet", "at": [2.4, -0.6, 0.0], "on": [8, "airplane's"], "off": [10], "opts": {"s": 0.85}},
    {"prop": "sign", "at": [1.95, -1.3, 3.3], "on": [10, "space"], "off": [12], "opts": {"text": "NO AIR", "color": "#1d3a8a"}},
    {"prop": "tanks", "at": [2.45, -0.6, 0.0], "on": [11, "brings"], "off": [12], "opts": {"s": 0.75}}],
   {"id": "gzs_rocket_space", "title": "Can a Rocket Work in Space? Science for Kids", "l1": "CAN IT WORK", "l2": "IN SPACE?", "thumb_text": "NO AIR!", "thumb_line": [4, 0.6],
    "fact": "A rocket engine does not need air: it carries everything it needs, its fuel and its own oxygen (NASA, What Is a Rocket?; NASA Glenn, Practical Rocketry)."}),
  teach("stages", "mountain", "golden", "STAGES!", [
     {"t": "Why do some big rockets drop parts as they fly?", "pause": 0.4},
     {"t": "To get lighter? Or to get heavier?", "pause": 3.2},
     "To get lighter!",
     "Here is the fun fact. Big rockets are built in parts, called stages, stacked one on top of another.",
     "Let's count the stages. One, two, three!",
     {"t": "What happens when the bottom stage uses up its fuel? Hmm.", "pause": 2.4},
     "It drops away, and the next stage takes over!",
     ["Bye-bye, stage one! Now the rocket is lighter.", "close:host"],
     "A heavier rocket needs a bigger push to fly.",
     "So dropping the empty part helps the rocket go much higher.",
     "This idea is called staging. It helps rockets reach space, and even the Moon!",
     "Up, up, and away. All the way to space!",
     ["Say it with me. Rockets drop stages to get lighter!", "close:host"],
     "Can you stack your fists, one on top of the other, like rocket stages?",
     "Now take the bottom one away. Bye-bye, stage one!",
     {"t": "Quick check! After a stage drops away, is the rocket lighter? Or heavier?", "pause": 3.2},
     "Lighter! Super thinking!"],
   {"a": "LIGHTER", "b": "HEAVIER", "right": "a", "ask": [1], "answer": [2], "hold": 2.4},
   {"a": "LIGHTER", "b": "HEAVIER", "right": "a", "ask": [15], "answer": [16], "hold": 2.0},
   [{"prop": "rocket", "at": [2.55, -0.5, 0.0], "on": [3, "stages"], "off": [5], "opts": {"stages": 3, "s": 0.8}},
    {"prop": "dots", "at": "dots", "on": [5, "end"], "off": [6]},
    {"prop": "rocket", "at": [2.55, -0.5, 0.0], "on": [6, "drops"], "off": [8], "opts": {"stages": 3, "s": 0.8}, "leave": [6, "away"]},
    {"prop": "sign", "at": [1.95, -1.3, 3.3], "on": [8, "heavier"], "off": [10], "opts": {"text": "BIG PUSH", "color": "#ff7a00"}},
    {"prop": "sign", "at": [1.95, -1.3, 3.3], "on": [10, "staging"], "off": [12], "opts": {"text": "STAGING", "color": "#3561d9"}}],
   {"id": "gzs_rocket_stages", "title": "Why Do Big Rockets Drop Parts? Science for Kids", "l1": "WHY DROP", "l2": "PARTS?", "thumb_text": "BYE-BYE!", "thumb_line": [6, 0.7],
    "fact": "Big rockets are built in stages; an empty stage is dropped behind and the next one fires, and this staging helps rockets reach space (NASA Glenn, Practical Rocketry)."}),
  quiz("spring_meadow", "golden", [
     ("Question one. What does a rocket engine push out of its back? Hot gas? Or water?", "HOT GAS", "WATER", "a", "Hot gas! Yes!"),
     ("Question two. Does a rocket carry its own oxygen? Yes? Or no?", "YES", "NO", "a", "Yes! That's right!"),
     ("Question three. When a stage drops away, is the rocket lighter? Or heavier?", "LIGHTER", "HEAVIER", "a", "Lighter! You remembered!")]),
  {"name": "goodbye", "kind": "outro", "biome": "night_meadow", "tod": "sunset", "word": "BYE-BYE!", "lines": [
     "You found out so much today.",
     "The gas goes down, and the rocket goes up. It carries its own oxygen. And it drops stages to get lighter!",
     "What would you like to find out next?",
     "Thank you for exploring with me. Bye-bye, friends! See you next time!"]},
 ]}

RAIN = {
 "id": "gzx_ep02", "channel": "gizmo", "version": 3, "seed": 92, "voice": "af_heart", "speed": 0.84,
 "title": "Where Does Rain Come From? Science for Kids with Gizmo", "card": "Where Rain Comes From!", "thumb_text": "PITTER PATTER!",
 "thumb_at": ["rain", 4, 0.6],
 "description": ("Where does rain come from? Find out with Gizmo the robot: the sun warms water and turns some of it into invisible water vapor, "
                 "cold air high up turns the vapor back into tiny drops that gather on specks of dust and make clouds, and drops that grow too heavy fall as rain. "
                 "Small raindrops are round and bigger ones are shaped like a hamburger bun.\n"
                 "A science explainer for kids ages 4-8, with questions to answer, things to copy, quick checks and a quiz at the end.\n\n"
                 "Where the facts come from (read Nov 19, 2026): USGS Water Science School, The Water Cycle for Kids and Are Raindrops Shaped Like Teardrops?; "
                 "NOAA SciJinks, What Causes Rain?"),
 "tags": ["where does rain come from", "water cycle for kids", "rain for kids", "clouds for kids", "evaporation for kids", "science for kids",
          "how things work for kids", "STEM for kids", "Gizmo Explains", "Gizmo the robot"],
 "cast": ["pal"], "extras": [],
 "facts": [
  "USGS Water Science School, 'The Water Cycle for Kids', water.usgs.gov/edu/watercycle-kids-beg.html (read Nov 19 2026): "
  "'The sun causes liquid water to evaporate, or turn from a liquid to a gas (water vapor).' 'The invisible water vapor floats high into the atmosphere' "
  "'The colder temperatures high in the atmosphere cause the water vapor to turn back into tiny liquid water droplets' 'Condensation causes clouds to form.' "
  "'When they get heavy enough, they fall to Earth as precipitation, such as rain and snow.' 'When rain hits the land or snow melts, it flows downhill over the landscape.' "
  "'most of it ending up back in the oceans.' 'This process is always happening everywhere.'",
  "NOAA SciJinks, 'What Causes Rain?', scijinks.gov/rain (read Nov 19 2026): 'In order to condense, the water vapor must have a solid to glom onto.' "
  "'This solid \"seed\" may be a speck of dust or pollen' 'with more water condensing onto other water droplets, the droplets grow.' "
  "'When they get too heavy to stay suspended in the cloud ... they fall to Earth as rain.'",
  "USGS Water Science School, 'Raindrops are Different Shapes' (Are raindrops shaped like teardrops?), usgs.gov/water-science-school/science/are-raindrops-shaped-teardrops "
  "(read Nov 19 2026): 'Small raindrops (radius < 1 millimeter (mm)) are spherical; larger ones assume a shape more like that of a hamburger bun.' "
  "'The artistic representation of raindrop as presented by popular culture is that of a teardrop.'"],
 "improves": [
  "second Gizmo explainer: three new places (beach hello, mountain clouds, river rain) and three moving examples (a puddle that shrinks while vapor rises, a speck of dust a droplet grows on, a cloud that rains)",
  "invisible things are shown and said to be drawn ('we drew it with little dots'), so the picture does not teach that vapor can be seen",
  "the quiz is three answer-sign rounds on the teaching board (no check mark beside a face)"],
 "segments": [
  {"name": "hello", "kind": "intro", "biome": "beach", "tod": "morning", "word": "RAIN!", "lines": [
     "Hello, friends! I am Gizmo the robot.",
     "Today we are finding out where rain comes from!",
     "My little helper bot is here too. Hello, little bot!",
     "We have three big questions. Count them with me. One, two, three!",
     "Ready? Let's find out!"],
   "exhibits": [{"prop": "count", "at": [-0.75, -1.7, 3.55], "on": [3, "one"], "times": [[3, "one"], [3, "two"], [3, "three"]], "opts": {"n": 3, "dx": 0.75, "s": 1.0}}]},
  teach("vapor", "river", "noon", "VAPOR!", [
     {"t": "Where does the water for rain come from?", "pause": 0.4},
     {"t": "Does it come from the sea? Or from the Moon?", "pause": 3.2},
     "It comes from the sea, and from lakes, and even from puddles!",
     "Here is the fun fact. The sun warms the water, and some of it turns into a gas, called water vapor.",
     "This is called evaporation. Look! The puddle is getting smaller.",
     {"t": "Can we see water vapor? Hmm.", "pause": 2.4},
     "No! Water vapor is invisible. We drew it with little dots, so you can see where it goes.",
     ["Up, up, it floats!", "close:host"],
     "The water vapor floats high up into the air.",
     "The sun's warmth helps water change, from a liquid, into a gas.",
     "And this is happening everywhere, all the time!",
     "Over the sea, over the lakes, and over the puddles too.",
     ["Say it with me. The sun turns water into vapor!", "close:host"],
     "Can you wiggle your fingers up high, like rising water vapor?",
     "Up, up, up! Now float your hands down, nice and slow.",
     {"t": "Quick check! Can you see water vapor? Yes? Or no?", "pause": 3.2},
     "No! It is invisible. Great job!"],
   {"a": "THE SEA", "b": "THE MOON", "right": "a", "ask": [1], "answer": [2], "hold": 2.4},
   {"a": "YES", "b": "NO", "right": "b", "ask": [15], "answer": [16], "hold": 2.0},
   [{"prop": "puddle", "at": [2.45, -0.9, 0.0], "on": [3, "water"], "off": [5], "opts": {"s": 0.85, "shrink": 9.0}},
    {"prop": "sun", "at": [2.6, -1.1, 3.0], "on": [3, "sun"], "off": [5], "opts": {"s": 0.8}},
    {"prop": "vapor", "at": [2.45, -0.9, 0.2], "on": [3, "vapor"], "off": [5], "opts": {"s": 0.9}},
    {"prop": "dots", "at": "dots", "on": [5, "end"], "off": [6]},
    {"prop": "vapor", "at": [2.45, -0.9, 0.2], "on": [6, "dots"], "off": [7], "opts": {"s": 0.9}},
    {"prop": "puddle", "at": [2.45, -0.9, 0.0], "on": [6, "dots"], "off": [7], "opts": {"s": 0.6, "shrink": 60.0}},
    {"prop": "sign", "at": [1.95, -1.3, 3.3], "on": [8, "floats"], "off": [10], "opts": {"text": "WATER VAPOR", "color": "#3db8ff"}},
    {"prop": "vapor", "at": [2.45, -0.9, 0.0], "on": [10, "everywhere"], "off": [12], "opts": {"s": 1.0}},
    {"prop": "pool", "at": [2.45, -0.9, 0.0], "on": [11, "sea"], "off": [12], "opts": {"s": 0.75}}],
   {"id": "gzs_rain_vapor", "title": "Can You See Water Vapor? Science for Kids", "l1": "CAN YOU SEE", "l2": "WATER VAPOR?", "thumb_text": "INVISIBLE!", "thumb_line": [4, 0.6],
    "fact": "The sun warms water and turns some of it into invisible water vapor, which floats high into the air (USGS, The Water Cycle for Kids)."}),
  teach("clouds", "mountain", "noon", "CLOUDS!", [
     {"t": "How does a cloud form, high up in the sky?", "pause": 0.4},
     {"t": "Does the water vapor get colder? Or warmer?", "pause": 3.2},
     "It gets colder!",
     "Here is the fun fact. High up in the sky, the air is cold.",
     "The cold turns the water vapor back into tiny drops of liquid water.",
     {"t": "But tiny drops need something to hold on to. What is it? Hmm.", "pause": 2.4},
     "A speck of dust, or a bit of pollen! The water gathers on it.",
     ["The tiny drop grows, and grows!", "teach"],
     "Lots and lots of tiny drops together make a cloud.",
     "This change, from vapor back into water, is called condensation.",
     "Puff, puff! The cloud floats along, high in the sky.",
     "So a cloud is made of water. Who knew?",
     ["Say it with me. Cold air turns vapor into clouds!", "close:host"],
     "Can you make a cloud shape with your arms? Big and round!",
     "Now float like a cloud. Drift, drift, drift.",
     {"t": "Quick check! A cloud is made of tiny drops of what? Water? Or sand?", "pause": 3.2},
     "Tiny drops of water! You got it!"],
   {"a": "COLDER", "b": "WARMER", "right": "a", "ask": [1], "answer": [2], "hold": 2.4},
   {"a": "WATER", "b": "SAND", "right": "a", "ask": [15], "answer": [16], "hold": 2.0},
   [{"prop": "thermo", "at": [2.55, -0.6, 0.3], "on": [3, "cold"], "off": [5], "opts": {"hot": False}},
    {"prop": "dots", "at": "dots", "on": [5, "end"], "off": [6]},
    {"prop": "dust", "at": [2.45, -0.9, 2.1], "on": [6, "speck"], "off": [8], "opts": {"s": 1.1, "grow": 1.0}},
    {"prop": "cloud", "at": [2.45, -0.9, 2.4], "on": [8, "cloud"], "off": [10], "opts": {"s": 1.0}},
    {"prop": "sign", "at": [1.95, -1.3, 3.3], "on": [9, "condensation"], "off": [10], "opts": {"text": "CONDENSATION", "color": "#3561d9"}},
    {"prop": "cloud", "at": [2.45, -0.9, 2.4], "on": [10, "cloud"], "off": [12], "opts": {"s": 1.0}}],
   {"id": "gzs_rain_clouds", "title": "How Does a Cloud Form? Science for Kids", "l1": "HOW DOES A", "l2": "CLOUD FORM?", "thumb_text": "TINY DROPS!", "thumb_line": [6, 0.7],
    "fact": "Cold air high up turns water vapor back into tiny drops of water, which gather on specks of dust or pollen; condensation makes clouds (USGS, The Water Cycle for Kids; NOAA SciJinks, What Causes Rain?)."}),
  teach("rain", "river", "morning", "RAIN!", [
     {"t": "What makes the drops in a cloud fall down as rain?", "pause": 0.4},
     {"t": "Do they get too heavy? Or too sleepy?", "pause": 3.2},
     "They get too heavy!",
     "Here is the fun fact. More and more water gathers on the drops, and they grow bigger.",
     "When they get too heavy to float, they fall down as rain. Pitter, patter!",
     {"t": "What shape is a falling raindrop? Hmm.", "pause": 2.4},
     "Small raindrops are round, like a ball. Bigger ones look like a hamburger bun!",
     ["Not like a teardrop at all!", "teach"],
     "The rain lands on the ground, and flows downhill.",
     "Down into streams and rivers, and back to the sea.",
     "Then the sun warms the water again, and around and around it goes!",
     "This is called the water cycle. It is always happening, everywhere!",
     ["Say it with me. Heavy drops fall down as rain!", "close:host"],
     "Can you tap your fingers like falling rain? Pitter, patter!",
     "Faster, faster! Now slow, slow, and stop.",
     {"t": "Quick check! Is a big raindrop shaped like a teardrop? Or a hamburger bun?", "pause": 3.2},
     "A hamburger bun! Super thinking!"],
   {"a": "HEAVY", "b": "SLEEPY", "right": "a", "ask": [1], "answer": [2], "hold": 2.4},
   {"a": "TEARDROP", "b": "BUN", "right": "b", "ask": [15], "answer": [16], "hold": 2.0},
   [{"prop": "cloud", "at": [2.45, -0.9, 2.7], "on": [3, "water"], "off": [5], "opts": {"s": 1.0, "grey": True, "rain": True}},
    {"prop": "dots", "at": "dots", "on": [5, "end"], "off": [6]},
    {"prop": "drops", "at": [2.45, -0.9, 2.0], "on": [6, "small"], "off": [7], "opts": {"kinds": ["round", "bun"], "s": 1.0}, "times": [[6, "small"], [6, "bigger"]]},
    {"prop": "drops", "at": [2.45, -0.9, 2.0], "on": [7, "teardrop"], "off": [8], "opts": {"kinds": ["tear"], "s": 1.1}},
    {"prop": "river", "at": [2.3, -0.7, 0.0], "on": [8, "ground"], "off": [10], "opts": {"s": 0.85}},
    {"prop": "cycle", "at": [2.45, -0.9, 2.1], "on": [10, "around"], "off": [12], "opts": {"s": 1.05}}],
   {"id": "gzs_rain_drops", "title": "What Shape Is a Raindrop? Science for Kids", "l1": "WHAT SHAPE", "l2": "IS A RAINDROP?", "thumb_text": "LIKE A BUN!", "thumb_line": [6, 0.8],
    "fact": "Cloud drops grow until they are too heavy and fall as rain; small raindrops are round and bigger ones are shaped like a hamburger bun (NOAA SciJinks; USGS Water Science School)."}),
  quiz("beach", "golden", [
     ("Question one. What turns water into water vapor? The sun? Or the wind?", "THE SUN", "THE WIND", "a", "The sun! Yes!"),
     ("Question two. What is a cloud made of? Tiny drops of water? Or cotton?", "WATER", "COTTON", "a", "Tiny drops of water! That's right!"),
     ("Question three. When cloud drops get too heavy, what happens? They fall as rain? Or they fly away?", "RAIN", "FLY AWAY", "a", "They fall as rain! You remembered!")]),
  {"name": "goodbye", "kind": "outro", "biome": "autumn_forest", "tod": "sunset", "word": "BYE-BYE!", "lines": [
     "You found out so much today.",
     "The sun lifts water up as vapor. Cold air makes clouds. And heavy drops fall down as rain!",
     "What would you like to find out next?",
     "Thank you for exploring with me. Bye-bye, friends! See you next time!"]},
 ]}

# parts were 77-82 s in the first build: each gets one or two more lines so part + hook is a Short of 85-95 s
ins(ROCKET, "push", 10, "A big push down makes a big push up!")
ins(ROCKET, "push", 7, "Whoosh, the gas goes down. Zoom, the rocket goes up!")
ins(ROCKET, "space", 11, "In space, there is nothing for an engine to push against, either.")
ins(ROCKET, "space", 7, "Fuel and oxygen, packed in two big tanks.")
ins(ROCKET, "stages", 10, "Lighter means it can climb higher, and higher!")
ins(RAIN, "vapor", 10, "Liquid water is like the water in a puddle. A gas is like the air.")
ins(RAIN, "clouds", 7, "The water vapor holds on to the speck, and turns into a tiny drop.")
ins(RAIN, "rain", 5, "Down, down, down they fall, all the way to the ground.")
ins(ROCKET, "space", 3, "Even way up in space!")
ins(ROCKET, "stages", 5, "Three stages, stacked up tall!")
ins(RAIN, "rain", 13, "Around and around, again and again!")


def visit(spec, segname, line, biome, tod):
    """A second place inside a part (review.py wants 8+ places; a new place every minute or so keeps the picture changing)."""
    seg = next(g for g in spec["segments"] if g["name"] == segname)
    seg["visits"] = [dict(P), {"line": line, "show": ["pal"], "biome": biome, "tod": tod}]


visit(ROCKET, "push", 9, "lab", "noon")
visit(ROCKET, "space", 10, "beach", "noon")
visit(ROCKET, "stages", 12, "night_meadow", "night")
visit(RAIN, "vapor", 11, "beach", "noon")
visit(RAIN, "clouds", 9, "spring_meadow", "noon")
visit(RAIN, "rain", 9, "farm", "noon")

if __name__ == "__main__":
    for spec in (ROCKET, RAIN):
        json.dump(spec, open(os.path.join(HERE, "lessons", spec["id"] + ".json"), "w"), indent=1); print("wrote lessons/" + spec["id"] + ".json")
