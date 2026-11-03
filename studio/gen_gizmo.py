"""Gizmo Explains how-things-work scripts: eps gz_ep02..05 + Short gz_rainbow (appended to shorts_gizmo.json)."""
import json
SRC = ["NOAA SciJinks (rain, rainbows, lightning, snow, wind)", "NASA Kids Club (rockets, flight)", "Basic physical & life science for ages 4-8"]
# key: (name, clue, how1, how2, try_it, q, a, extra, wow)
G = {
 "gz_rain": ("Rain", "it falls from clouds, drip, drop!", "The sun warms water in lakes and oceans, and it floats up into the sky.", "Up high, it cools down and makes clouds out of tiny drops.",
             "Can you wiggle your fingers down like falling rain?", "Why does rain fall?", "When cloud drops get big and heavy, they fall down!", "Then the water goes back up again. It's called the water cycle!", "WATER CYCLE!"),
 "gz_rainbow": ("Rainbow", "it's a colorful arch in the sky!", "Sunlight looks white, but it's really made of many colors.", "When sunlight shines through raindrops, the colors spread out!",
                "Can you draw a big rainbow in the air with your finger?", "What do we need to see a rainbow?", "Sunshine and raindrops at the same time!", "Red, orange, yellow, green, blue, and purple!", "RAINBOW!"),
 "gz_lightning": ("Lightning", "it's a bright flash in a stormy sky!", "Lightning is a giant spark of electricity in the clouds.", "It's super hot, and it makes the air go BOOM. That's thunder!",
                  "Can you count with me after a flash? One, two, three!", "What comes after lightning?", "Thunder! Boom, rumble, rumble.", "When there's a storm, we stay safe inside.", "FLASH, BOOM!"),
 "gz_snow": ("Snow", "it's white, cold, and falls in winter!", "When it's really cold, water in the clouds freezes into ice crystals.", "The crystals stick together and make snowflakes!",
             "Can you float down slowly, like a snowflake?", "What is snow made of?", "Tiny frozen ice crystals!", "Every snowflake has six sides. So pretty!", "SNOWFLAKES!"),
 "gz_wind": ("Wind", "you can't see it, but you can feel it!", "Wind is air that's moving.", "When the sun warms the air, it moves around, whoosh!",
             "Can you blow like the wind? Whoooosh!", "What can wind push?", "Kites, sailboats, and windmills!", "Windmills use wind to make electricity.", "WHOOSH!"),
 "gz_rocket": ("Rocket", "it blasts off into space!", "A rocket burns fuel and pushes hot gas down, really hard.", "Pushing down makes the rocket go up, up, up!",
               "Can you count down with me? Three, two, one, blast off!", "Which way does the rocket push?", "Down! And that sends it up!", "Rockets carry astronauts and satellites to space.", "BLAST OFF!"),
 "gz_plane": ("Airplane", "it has big wings and flies above the clouds!", "Airplane wings are curved on top.", "When the plane zooms forward, the wings push air down and lift the plane up!",
              "Can you stretch your arms out like wings and zoom?", "What lifts an airplane up?", "Its wings, moving through the air!", "Engines push the plane forward fast.", "LIFT OFF!"),
 "gz_balloon": ("Hot Air Balloon", "it's a giant floating balloon with a basket!", "A burner heats the air inside the balloon.", "Hot air is lighter than cool air, so it floats up!",
                "Can you float up slowly, rising on your tiptoes?", "Why does a hot air balloon go up?", "Hot air rises!", "To come down, the pilot lets the air cool.", "UP, UP!"),
 "gz_heli": ("Helicopter", "it has spinning blades on top!", "A helicopter's blades spin really fast.", "The spinning blades push air down, so the helicopter goes straight up!",
             "Can you spin your arms like helicopter blades?", "Can helicopters fly straight up?", "Yes! And they can hover in one place!", "Helicopters can land in small spaces.", "HOVER!"),
 "gz_kite": ("Kite", "it flies on a string on a windy day!", "Wind pushes against the kite.", "The string holds it, so the kite climbs up high!",
             "Can you pretend to hold a kite string? Hold on tight!", "What does a kite need to fly?", "Wind!", "Running helps the kite catch the wind.", "WHEEE!"),
 "gz_magnet": ("Magnet", "it can stick to the fridge!", "Magnets have an invisible pull.", "They pull on some metals, like iron!",
               "Can you pretend your hands are magnets? Pull together, click!", "Will a magnet pull a paper clip?", "Yes! Paper clips have metal in them.", "Magnets won't stick to wood or plastic.", "CLICK!"),
 "gz_bulb": ("Light Bulb", "it lights up a dark room!", "Electricity flows through wires to the bulb.", "Inside, the electricity makes light!",
             "Can you flick a pretend light switch? On! Off!", "What makes a light bulb glow?", "Electricity!", "Always ask a grown-up for help with plugs.", "LIGHTS ON!"),
 "gz_ice": ("Melting Ice", "it's cold, hard, and slippery!", "Ice is frozen water.", "When ice gets warm, it melts back into water!",
            "Can you melt slowly, like an ice cube, down to the floor?", "What makes ice melt?", "Warmth! Like the sun.", "Put water in the freezer, and it turns back into ice!", "MELT!"),
 "gz_shadow": ("Shadow", "it follows you on a sunny day!", "Light travels in straight lines.", "When you block the light, you make a dark shape. That's your shadow!",
               "Can you make a shadow puppet with your hands?", "What do we need to make a shadow?", "Light, and something to block it!", "In the morning, shadows are long!", "SHADOW!"),
 "gz_sound": ("Sound", "you hear it with your ears!", "Sound happens when things shake, or vibrate.", "The shaking wiggles the air, and the wiggles reach your ears!",
              "Can you hum and touch your throat? Feel it buzz!", "How does sound travel?", "Through wiggly air waves!", "Loud sounds have big waves. Quiet sounds have small waves.", "BUZZ!"),
 "gz_seed": ("Seed", "it's tiny, and a plant grows from it!", "A seed has a baby plant inside.", "With water and warmth, it starts to grow!",
             "Can you curl up small like a seed, and then grow tall?", "What does a seed need to grow?", "Water, warmth, and soil!", "The first little sprout pokes up out of the dirt.", "SPROUT!"),
 "gz_roots": ("Roots", "they grow under the ground!", "Roots grow down into the soil.", "They drink up water, like straws!",
              "Can you stand strong, like roots holding a plant?", "What do roots do?", "Drink water, and hold the plant in place!", "Carrots are roots we can eat!", "SLURP!"),
 "gz_leaf": ("Leaves", "they're green, and they love sunshine!", "Leaves catch sunlight.", "They use sunlight, air, and water to make food for the plant!",
             "Can you open your hands wide, like leaves catching the sun?", "What do leaves use to make food?", "Sunlight, air, and water!", "Plants also give us fresh air to breathe.", "SUNSHINE FOOD!"),
 "gz_flower": ("Flower", "it's colorful, and bees love it!", "Flowers make a sweet juice called nectar.", "Bees visit, and help the flower make new seeds!",
               "Can you buzz like a busy bee? Bzzzz!", "Who helps flowers make seeds?", "Bees and butterflies!", "Then the seeds can grow into new plants.", "BZZZ!"),
 "gz_tree": ("Tree", "it's tall, with a trunk and branches!", "A tree starts as a tiny seed.", "It grows a little bit every year, for many, many years!",
             "Can you stretch up tall like a big tree?", "Where does a tree come from?", "A tiny seed!", "Some trees grow fruit, like apples!", "TALL TREE!"),
}

def lines(k, lead):
    n, clue, h1, h2, tr, q, a, extra, wow = G[k]
    return [[f"Here's a clue: {clue} Can you guess?", "q"], [f"{lead}: {n}!", "enter"], [f"How does it work? Let's find out!", "zoom"],
            [h1, "fx+bob"], [h2, "bob"], [tr, "wiggle"], [q, "fxoff+fx2off+q"], [a, f"fx2+badge:{wow}"],
            [f"Let's say it together: {n.upper()}!", "zoom"], [f"One more time, nice and loud: {n.upper()}!", "zoom"], [extra, "fxoff+fx2off+bob"], [f"Now we know how it works. Great job!", "bob"]]

EPS = [
 ("gz_ep02_weather", "How Does Weather Work? Rain, Rainbows, Snow and More with Gizmo", ["gz_rain", "gz_rainbow", "gz_lightning", "gz_snow", "gz_wind"], "find out how weather works",
  ["Rain falls from heavy clouds.", "Rainbows need sun and rain.", "Lightning flashes, then thunder booms.", "Snow is frozen ice crystals.", "And wind is moving air!"]),
 ("gz_ep03_flying", "How Do Things Fly? Rockets, Airplanes, Helicopters for Kids with Gizmo", ["gz_rocket", "gz_plane", "gz_balloon", "gz_heli", "gz_kite"], "find out how things fly",
  ["Rockets push down to go up.", "Airplane wings make lift.", "Hot air balloons rise with hot air.", "Helicopters spin their blades.", "And kites ride the wind!"]),
 ("gz_ep04_science", "Everyday Science for Kids! Magnets, Light, Shadows and Sound with Gizmo", ["gz_magnet", "gz_bulb", "gz_ice", "gz_shadow", "gz_sound"], "explore everyday science",
  ["Magnets pull on metal.", "Electricity lights the bulb.", "Warmth melts ice.", "Blocking light makes a shadow.", "And sound is wiggly air!"]),
 ("gz_ep05_plants", "How Do Plants Grow? From Seed to Tree for Kids with Gizmo", ["gz_seed", "gz_roots", "gz_leaf", "gz_flower", "gz_tree"], "find out how plants grow",
  ["A seed needs water and warmth.", "Roots drink water.", "Leaves make food from sunlight.", "Flowers make new seeds.", "And a tiny seed can grow into a tree!"]),
]
LEAD = ["First up", "Next", "Here comes", "Now let's look at", "And last"]
for eid, title, keys, what, rec in EPS:
    ep = {"id": eid, "title": title,
          "intro": [["Hi, friends! I'm Gizmo the robot, and welcome to Gizmo Explains!", ""], [f"I love asking, how does that work? Today we're going to {what}.", ""],
                    ["We'll explore five cool things. Can you count them with me? One, two, three, four, five!", ""], ["When my antenna lights up, it means I have an idea!", ""], ["Ready? Let's go explore!", ""]],
          "animals": [{"key": k, "lines": lines(k, LEAD[i])} for i, k in enumerate(keys)],
          "recap": [["Wow, we learned so much! Let's remember.", "@title"]] + [[r, "@" + k] for r, k in zip(rec, keys)],
          "outro": [["Which one was your favorite? Keep asking, how does that work?", ""], ["Bye, friends! See you next time on Gizmo Explains!", ""]]}
    json.dump(ep, open(f"eps/{eid}.json", "w"), indent=1, ensure_ascii=False)

sh = [s for s in json.load(open("shorts_gizmo.json")) if s["id"] != "gz_rainbow"]
n, clue, h1, h2, tr, q, a, extra, wow = G["gz_rainbow"]
sh.append({"id": "gz_rainbow", "animal": "gz_rainbow", "title": "How Is a Rainbow Made? 🌈", "thumb": "RAINBOW!", "top": "RAINBOW", "bg": ["#7fd3ff", "#d6f1ff"], "floor": "#7cc576", "sources": SRC,
           "beats": [{"say": "Sunshine plus rain equals something magical. Do you know what?", "act": "hook"}, {"say": "Hi! I'm Gizmo the robot. Let's find out how it works!", "act": "milo_in"},
                     {"say": f"A rainbow! {h1}", "act": "zoom+badge:RAINBOW!"}, {"say": f"{h2} {a}", "act": "fx+bob"},
                     {"say": "Red, orange, yellow, green, blue, and purple! Can you say them with me?", "act": "wiggle"}, {"say": "Next time it's sunny and rainy, look for a rainbow! See you next time!", "act": "fxoff+outro"}]})
json.dump(sh, open("shorts_gizmo.json", "w"), indent=1, ensure_ascii=False)
print("ok")
