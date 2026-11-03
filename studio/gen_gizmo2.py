"""Gizmo Explains week 2 (Nov 9-17): eps gz_ep06..11, shorts_gizmo2.json (16 Shorts), upload_plan_gizmo_week2.json.
Scenes come from art_gizmo2.py (keys gz2_*). No custom thumbnails (channel not verified), so no "thumb" in the plan.
upload_plan_gizmo2.json already holds week-1 entries, so the week-2 plan goes to upload_plan_gizmo_week2.json."""
import json
from art_gizmo2 import SCENES_GIZMO2, NAMES_GIZMO2

SRC_BODY = ["KidsHealth (Nemours): How the Body Works", "Basic life science for ages 4-8"]
SRC_PHYS = ["NASA Climate Kids / NOAA SciJinks (water, energy)", "Basic physical science for ages 4-8"]
SRC_SPACE = ["NASA Space Place (Earth, Moon, Sun, seasons)", "Basic Earth & space science for ages 4-8"]
SRC_LIFE = ["National Wildlife Federation / USDA (animals, bees)", "Basic life science for ages 4-8"]
SRC_TECH = ["U.S. Department of Energy (fridges, electricity)", "Basic physical science for ages 4-8"]

# key: (name, clue, how1, how2, try_it, q, a, extra, wow)
G = {
 # ---- your body ----
 "gz2_heart": ("Heart", "it's in your chest, and it goes thump, thump!", "Your heart is a strong muscle, about the size of your fist.",
               "Every beat squeezes and pumps blood all around your body, from your head down to your toes!",
               "Can you put your hand on your chest and feel the thump, thump?", "What does your heart pump?", "Blood! It carries good things all through your body.",
               "When you run and play, your heart beats faster to keep up with you!", "PUMP, PUMP!"),
 "gz2_lungs": ("Lungs", "you have two of them, and they help you breathe!", "When you breathe in, air goes down a tube into your two lungs, like soft balloons.",
               "Your body takes the fresh air it needs, and then you breathe the old air back out.",
               "Can you take a big breath in, and slowly breathe out? Ahhh!", "What do your lungs fill up with?", "Air! In and out, all day and all night.",
               "You breathe even while you sleep, without thinking about it at all!", "BREATHE!"),
 "gz2_bones": ("Bones", "they're hard, and they hold you up!", "Bones are hard and strong, and they give your body its shape.",
               "Grown-ups have two hundred and six bones! Without bones, you'd be floppy like a noodle.",
               "Can you tap your knees, your elbows, and your head? Bones are inside!", "How many bones do grown-ups have?", "Two hundred and six bones!",
               "Milk, cheese, and green veggies help your bones grow big and strong.", "206 BONES!"),
 "gz2_muscles": ("Muscles", "they help you run, jump, and smile!", "Muscles are attached to your bones, and they move them by pulling.",
                 "When a muscle gets shorter, it pulls a bone, and your arm or leg moves!",
                 "Can you bend your arm and make a strong muscle? Flex!", "How do muscles move your bones?", "They pull! Muscles can only pull, not push.",
                 "You have more than six hundred muscles. Even smiling uses muscles in your face!", "FLEX!"),
 "gz2_teeth": ("Teeth", "they're white, and they help you chew!", "Your front teeth are sharp for biting, like when you bite an apple.",
               "Your back teeth are wide and bumpy for chewing and mashing your food.",
               "Can you show me your biggest smile? Look at those teeth!", "How many baby teeth do kids have?", "Twenty! Later, grown-up teeth grow in.",
               "Brush your teeth twice a day, in the morning and at night, to keep them clean!", "CHOMP!"),
 # ---- water ----
 "gz2_float": ("Floating", "a boat does it, and so does a rubber duck!", "When something sits in water, the water pushes up on it from below.",
               "If the push is strong enough to hold it up, it floats! Boats are shaped to let water push up a lot.",
               "Can you lie back and float, like a boat on the water?", "What pushes up on a floating boat?", "The water does!",
               "Big, heavy ships float too, because their wide shape spreads out on the water.", "IT FLOATS!"),
 "gz2_sink": ("Sinking", "a rock does it when you drop it in a pond!", "A rock is small, but it's very heavy for its size.",
              "The water can't push up hard enough to hold it, so down, down it goes to the bottom!",
              "Can you sink down slowly, down to the floor?", "Does a leaf sink or float?", "It floats! A leaf is very light for its size.",
              "Try it at bath time with a grown-up: which toys float, and which ones sink?", "SPLOOSH!"),
 "gz2_steam": ("Ice, Water and Steam", "it can be hard, wet, or floaty!", "Water can be three things: solid ice, runny water, or floaty steam.",
               "Warm up ice, and it melts into water. Heat water a lot, and it turns into steam!",
               "Can you be stiff like ice, then wiggly like water, then float like steam?", "What happens when water gets very hot?", "It turns into steam!",
               "Steam is very hot, so only grown-ups use the kettle. We just watch from far away.", "ICE, WATER, STEAM!"),
 "gz2_coldglass": ("Cold Glass", "it's a glass of ice water that gets wet on the outside!", "The air around us has tiny bits of water in it that we can't see.",
                   "When that air touches a cold glass, it cools down and turns into little drops!",
                   "Can you wiggle your fingers like tiny drops on a glass?", "Where do the drops come from?", "From the air! Not from inside the glass.",
                   "That's why grass is wet with dew on a cool morning. It's the same trick!", "DROPS!"),
 "gz2_puddle": ("Puddle", "it's on the ground after the rain, splash!", "When the sun shines on a puddle, it warms the water.",
                "The water turns into a gas we can't see, and floats up into the sky. Bye-bye, puddle!",
                "Can you float up, up, up like water going into the sky?", "Where does the puddle go?", "Up into the air! Then it helps make clouds.",
                "Wet clothes on a sunny day dry the same way. The water floats away!", "BYE, PUDDLE!"),
 # ---- simple machines ----
 "gz2_wheel": ("Wheel", "it's round, and it goes round and round!", "Dragging a heavy box is hard, because it rubs on the ground.",
               "Wheels roll instead of rubbing, so wagons, cars, and bikes move along easily!",
               "Can you roll your arms round and round like a wheel?", "Why are wheels so helpful?", "They roll, so things are easier to move!",
               "Wheels are on wagons, strollers, trains, and even shopping carts.", "ROLL!"),
 "gz2_lever": ("Lever", "a seesaw is one, up and down!", "A lever is a long bar that rests on a point, called a fulcrum.",
               "Push down on one end, and the other end goes up! It helps you lift heavy things.",
               "Can you be a seesaw? One arm up, one arm down!", "What happens when you push down on a lever?", "The other end goes up!",
               "A seesaw at the playground is a lever you can ride on!", "LIFT!"),
 "gz2_ramp": ("Ramp", "it's a slope that goes up, like a little hill!", "Lifting a heavy box straight up is really hard.",
              "A ramp is a longer path, but each push is smaller. So moving things up gets easier!",
              "Can you walk your fingers up a pretend ramp, step, step, step?", "Why do people use ramps?", "Ramps make it easier to move things up high!",
              "Ramps help wheelchairs, strollers, and delivery carts go up and down.", "EASY UP!"),
 "gz2_pulley": ("Pulley", "it's a wheel with a rope that helps lift things!", "A pulley is a wheel with a rope going over the top.",
                "When you pull the rope down, the thing on the other end goes up! Pulling down is easier than lifting up.",
                "Can you pull a pretend rope, hand over hand?", "Which way do you pull to lift with a pulley?", "Down! And the bucket goes up.",
                "Flagpoles use a pulley to raise the flag to the very top.", "PULL!"),
 "gz2_screw": ("Screw", "it twists, and it has a spiral around it!", "A screw is like a tiny ramp, wrapped around and around a pole.",
               "When you twist it, the spiral pulls the screw in, and it holds things together tight!",
               "Can you twist your body around and around, like a screw?", "What does a screw do?", "It twists in and holds things together!",
               "Jar lids twist on the same way. That's a screw too!", "TWIST!"),
 # ---- energy ----
 "gz2_battery": ("Battery", "it goes inside toys and flashlights!", "A battery stores energy inside it, ready to use.",
                 "When it's connected, it sends electricity through wires to make toys move and lights shine!",
                 "Can you light up like a flashlight? Click! Shine!", "What does a battery store?", "Energy! It turns into electricity.",
                 "Only grown-ups should change batteries. We keep them away from our mouths.", "POWER!"),
 "gz2_solar": ("Solar Panel", "it's a flat, shiny panel that loves the sun!", "A solar panel catches sunlight with special flat squares.",
               "It turns that sunlight into electricity, which can power lights in a home!",
               "Can you open your arms wide, like a panel catching sunshine?", "What does a solar panel need?", "Sunlight!",
               "Some calculators and garden lights have tiny solar panels on them.", "SUN POWER!"),
 "gz2_turbine": ("Wind Turbine", "it's very tall, with three long blades!", "Wind pushes on the long blades and makes them spin.",
                 "Inside, the spinning makes electricity that travels through wires to homes and schools!",
                 "Can you spin your arms slowly, like turbine blades in the wind?", "What makes a wind turbine spin?", "The wind!",
                 "Lots of wind turbines together are called a wind farm.", "SPIN!"),
 "gz2_waterwheel": ("Water Wheel", "it's a big wheel that turns in a river!", "Flowing water pushes on the paddles around the wheel.",
                    "The push makes the wheel spin, and the spinning can do work, like grinding grain into flour!",
                    "Can you make your hands go round and round, like a water wheel?", "What pushes a water wheel?", "Moving water!",
                    "Today, big dams use moving water to make electricity too.", "SPLASH, SPIN!"),
 "gz2_switch": ("Light Switch", "it's on the wall, and it goes click!", "Electricity needs a full loop of wire, like a circle, to flow.",
                "Click on, and the loop is joined, so the light shines. Click off, and there's a gap, so the light goes out!",
                "Can you click a pretend switch? On! Off! On!", "What does off do?", "It makes a gap, so electricity stops!",
                "Ask a grown-up to help with switches, and never touch plugs or outlets.", "CLICK!"),
 # ---- animals ----
 "gz2_fish": ("Fish", "it swims, and it has fins and a tail!", "Fish need air too, but they get it from water.",
              "Water goes in their mouth and over their gills, and the gills take out the air they need!",
              "Can you make a fish face and open and close your mouth?", "What do fish use to breathe?", "Their gills!",
              "That's why fish can stay underwater all day long.", "GILLS!"),
 "gz2_bird": ("Bird", "it has feathers and wings, tweet tweet!", "Birds flap their wings down to push on the air.",
              "Pushing the air down and back lifts them up and moves them forward!",
              "Can you flap your arms like wings? Flap, flap, flap!", "How do birds stay light enough to fly?", "Many birds have hollow bones and light feathers!",
              "Their feathers are shaped just right for catching air.", "FLAP!"),
 "gz2_bee": ("Honeybee", "it's fuzzy, it buzzes, and it loves flowers!", "Honeybees drink a sweet juice from flowers, called nectar.",
             "Back at the hive, they put it in little wax rooms and fan it with their wings until it turns into honey!",
             "Can you buzz and fan your wings like a busy bee? Bzzz!", "What do bees make honey from?", "Nectar from flowers!",
             "The little wax rooms have six sides. They're called a honeycomb.", "HONEY!"),
 "gz2_butterfly": ("Butterfly", "it has big, colorful wings!", "A butterfly starts as a tiny egg, and then a hungry caterpillar hatches out.",
                   "The caterpillar makes a cozy case called a chrysalis. Inside, it changes into a butterfly!",
                   "Can you curl up small like a caterpillar, then open your wings wide?", "What does a caterpillar turn into?", "A butterfly!",
                   "Egg, caterpillar, chrysalis, butterfly. What a change!", "NEW WINGS!"),
 "gz2_duck": ("Duck", "it swims on ponds and says quack, quack!", "Ducks have a special oil near their tail.",
              "They spread the oil on their feathers with their beak, so water rolls right off, and they stay dry!",
              "Can you waddle like a duck? Quack, quack!", "Why do ducks stay dry in the water?", "Their oily feathers keep the water out!",
              "Under their top feathers, ducks have soft fluffy feathers that keep them warm.", "STAYS DRY!"),
 # ---- space ----
 "gz2_daynight": ("Day and Night", "one is bright and sunny, and one is dark and sleepy!", "Our Earth is always spinning, like a slow spinning top.",
                  "The side facing the Sun has day, and the side facing away has night!",
                  "Can you spin around slowly, like the Earth? Day, night, day!", "How long does one spin take?", "One whole day!",
                  "When it's day for you, it's night for kids on the other side of the world.", "DAY AND NIGHT!"),
 "gz2_seasons": ("Seasons", "there are four of them: spring, summer, fall, and winter!", "Our Earth is tilted, like it's leaning a little to one side.",
                 "When your part of Earth leans toward the Sun, it gets more sunshine, and that's summer!",
                 "Can you lean to one side, like the tilted Earth?", "What makes the seasons?", "Earth's tilt as it goes around the Sun!",
                 "One trip all the way around the Sun takes one whole year.", "SEASONS!"),
 "gz2_moonphases": ("Moon Phases", "it can look round, or like a smile in the sky!", "The Moon doesn't make its own light. The Sun shines on it.",
                    "As the Moon goes around Earth, we see different parts of its sunny side!",
                    "Can you make a round full moon with your arms?", "Does the Moon really change shape?", "No! We just see more or less of its sunny side.",
                    "It takes about a month to go from new moon to full moon and back.", "MOON PHASES!"),
 "gz2_stars": ("Stars", "they twinkle in the night sky!", "Stars are giant suns, very, very far away.",
               "They're so far away that they look like tiny dots of light!",
               "Can you open and close your hands, like twinkling stars?", "Are stars still there in the daytime?", "Yes! The Sun is just too bright to see them.",
               "Our Sun is a star too, the closest star to Earth.", "TWINKLE!"),
 "gz2_sun": ("The Sun", "it's big, bright, and keeps us warm!", "The Sun is a giant ball of hot, glowing gas.",
             "It's so big that one hundred and nine Earths could fit across it, side by side!",
             "Can you stretch your arms out super wide, as big as the Sun?", "Why does the Sun look small?", "Because it's very, very far away!",
             "Never look right at the Sun, because it's too bright for your eyes.", "SO BIG!"),
}

LEAD = ["First up", "Next", "Here comes", "Now let's look at", "And last"]


def lines(k, lead):
    n, clue, h1, h2, tr, q, a, extra, wow = G[k]
    return [[f"Here's a clue: {clue} Can you guess?", "q"], [f"{lead}: {n}!", "enter"], ["How does it work? Let's find out!", "zoom"],
            [h1, "fx+bob"], [h2, "bob"], [tr, "wiggle"], [q, "fxoff+fx2off+q"], [a, f"fx2+badge:{wow}"],
            [f"Let's say it together: {n.upper()}!", "zoom"], [f"One more time, nice and loud: {n.upper()}!", "zoom"], [extra, "fxoff+fx2off+bob"], ["Now we know how it works. Great job!", "bob"]]


EPS = [
 ("gz_ep06_body", "How Does Your Body Work? Heart, Lungs and Bones", ["gz2_heart", "gz2_lungs", "gz2_bones", "gz2_muscles", "gz2_teeth"], "find out how your amazing body works",
  ["Your heart pumps, thump, thump.", "Your lungs breathe air in and out.", "Bones hold you up.", "Muscles pull to move you.", "And teeth bite and chew!"], "2026-11-12"),
 ("gz_ep07_water", "How Does Water Work? Floating, Sinking and Steam", ["gz2_float", "gz2_sink", "gz2_steam", "gz2_coldglass", "gz2_puddle"], "explore wonderful water",
  ["Water pushes up to make things float.", "Heavy rocks sink.", "Water can be ice, water, or steam.", "Cold glasses get drops from the air.", "And puddles float up into the sky!"], "2026-11-13"),
 ("gz_ep08_machines", "Simple Machines for Kids! Wheels, Levers and Ramps", ["gz2_wheel", "gz2_lever", "gz2_ramp", "gz2_pulley", "gz2_screw"], "find out how simple machines help us",
  ["Wheels roll.", "Levers lift.", "Ramps make going up easier.", "Pulleys lift when you pull down.", "And screws twist in tight!"], "2026-11-14"),
 ("gz_ep09_energy", "Where Does Electricity Come From? Gizmo Finds Out", ["gz2_battery", "gz2_solar", "gz2_turbine", "gz2_waterwheel", "gz2_switch"], "find out where energy comes from",
  ["Batteries store energy.", "Solar panels use sunlight.", "Wind turbines use wind.", "Water wheels use moving water.", "And switches open and close the loop!"], "2026-11-15"),
 ("gz_ep10_animals", "How Do Animals Do That? Fish, Birds and Bees", ["gz2_fish", "gz2_bird", "gz2_bee", "gz2_butterfly", "gz2_duck"], "find out how animals do amazing things",
  ["Fish breathe with gills.", "Birds flap to push the air.", "Bees turn nectar into honey.", "Caterpillars change into butterflies.", "And ducks stay dry with oily feathers!"], "2026-11-16"),
 ("gz_ep11_space", "Why Is It Night? Day, Seasons and the Moon for Kids", ["gz2_daynight", "gz2_seasons", "gz2_moonphases", "gz2_stars", "gz2_sun"], "find out how the sky works",
  ["Earth spins to make day and night.", "Earth's tilt makes the seasons.", "We see the Moon's sunny side.", "Stars are faraway suns.", "And our Sun is super big!"], "2026-11-17"),
]

BOILER = ("Gizmo the little robot loves to ask \"How does that work?\" Simple, true science for curious kids ages 4-8. New videos every day! "
          "Characters and visuals are animated with the help of AI tools and every script is reviewed for kid safety.")
TAGS = "#ScienceForKids #HowThingsWork #KidsLearning #STEMforKids"

plan = []
for eid, title, keys, what, rec, date in EPS:
    ep = {"id": eid, "title": title,
          "intro": [["Hi, friends! I'm Gizmo the robot, and welcome to Gizmo Explains!", ""], [f"I love asking, how does that work? Today we're going to {what}.", ""],
                    ["We'll explore five cool things. Can you count them with me? One, two, three, four, five!", ""], ["When my antenna lights up, it means I have an idea!", ""], ["Ready? Let's go explore!", ""]],
          "animals": [{"key": k, "lines": lines(k, LEAD[i])} for i, k in enumerate(keys)],
          "recap": [["Wow, we learned so much! Let's remember.", "@title"]] + [[r, "@" + k] for r, k in zip(rec, keys)],
          "outro": [["Which one was your favorite? Keep asking, how does that work?", ""], ["Bye, friends! See you next time on Gizmo Explains!", ""]]}
    json.dump(ep, open(f"eps/{eid}.json", "w"), indent=1, ensure_ascii=False)
    learn = "\n".join("• " + r for r in rec)
    d = (f"Join Gizmo the robot for a 5-minute science adventure! {ep['intro'][1][0]} 🤖\nMade for curious kids ages 4–8: guess-what clues, move-along fun, and a recap at the end.\n\n"
         f"What we learn today:\n{learn}\n\n{BOILER}\n\n{TAGS}")
    plan.append({"file": f"gizmo/{eid}.mp4", "title": title, "description": d, "date": date, "time": "2:10 PM", "status": "to_upload"})

SKY = dict(bg=["#7fd3ff", "#d6f1ff"], floor="#5fae5a")
LAB = dict(bg=["#c9d8fb", "#dfe9ff"], floor="#8a9bc7")
SPACE = dict(bg=["#0a0f2e", "#1b2366"], floor="transparent", root_bg="radial-gradient(ellipse at 50% 52%,#28328a 0%,#141a4f 45%,#090d2b 100%)")

# (key, title, thumb, look, sources, emoji, desc_lead, desc_body, beats[6 says], acts[6])
A1 = ["hook", "milo_in", "zoom+badge:{b}", "fx+bob", "fxoff+fx2+wiggle", "fx2off+outro"]
SH = [
 ("gz2_heart", "How Does Your Heart Work? ❤️", "PUMP, PUMP!", LAB, SRC_BODY, "❤️", "How does your heart work?",
  "Your heart is a strong muscle about the size of your fist. It pumps all day long, about one hundred thousand times a day, carrying good things all around your body!",
  ["Put your hand on your chest. Feel that thump, thump? Let's find out what it is!",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "It's your heart! Your heart is a strong muscle, about the size of your fist.",
   "Every beat squeezes and pumps blood all around your body, from your head to your toes. Thump, thump!",
   "Your heart beats about one hundred thousand times every day. When you run and play, it beats even faster!",
   "Your heart works hard all day, and even while you sleep. Now you know how it works! See you next time!"]),
 ("gz2_float", "Why Do Boats Float? 🚤", "IT FLOATS!", LAB, SRC_PHYS, "🚤", "Why do boats float?",
  "When a boat sits in water, the water pushes up on it. Boats are shaped wide, so the water can push up enough to hold them up!",
  ["A giant ship is super heavy, but it doesn't sink. How does it float?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "When something sits in water, the water pushes up on it from below. Push, push!",
   "Boats are wide, with lots of space inside, so the water can push up enough to hold them up. It floats!",
   "A small rock is heavy for its size, so the water can't hold it up. Down it sinks! But a wide boat stays on top.",
   "At bath time, ask a grown-up to help you test which toys float. See you next time!"]),
 ("gz2_eyes", "How Do Your Eyes See? 👀", "LIGHT IN!", LAB, SRC_BODY, "👀", "How do your eyes see?",
  "Light bounces off things and goes into your eyes. Your eyes send a message to your brain, and your brain tells you what you see!",
  ["You can see this apple right now. But how do your eyes do it?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "Light shines on the apple, and the light bounces off it, right into your eyes!",
   "The black dot in the middle of your eye is called the pupil. It's a little window that lets the light in.",
   "Then your eyes send a message to your brain, and your brain says, that's a red apple! Can you blink your eyes?",
   "Your eyes and brain work as a team. Now you know how it works! See you next time!"]),
 ("gz2_fridge", "How Does a Fridge Keep Food Cold?", "COLD INSIDE!", LAB, SRC_TECH, "🧊", "How does a fridge keep food cold?",
  "A fridge doesn't make cold. It moves heat from inside to outside! That's why it can feel warm near the back. Cold keeps food fresh longer.",
  ["Open the fridge, and brrr, it's cold inside! How does it stay so cold and chilly?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "Here's a big surprise: a fridge doesn't really make cold. It moves the heat out!",
   "Special tubes carry heat from inside the fridge to the outside. That's why it can feel warm near the back.",
   "With the heat gone, the inside stays cold, and cold food stays fresh longer. Can you shiver like you're in a fridge? Brrr!",
   "Remember to close the fridge door quickly, so the cold stays inside. See you next time!"]),
 ("gz2_guitar", "How Does a Guitar Make Music? 🎸", "STRINGS WIGGLE!", LAB, SRC_PHYS, "🎸", "How does a guitar make music?",
  "When you pluck a guitar string, it wiggles back and forth very fast. That wiggle makes sound! Thick strings sound low and thin strings sound high.",
  ["Strum, strum! A guitar can play happy songs and quiet songs. But how does it make music?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "When you pluck a string, it wiggles back and forth, super fast. That's called a vibration.",
   "The wiggling string shakes the air, and the hollow body makes the sound big and loud!",
   "Thick strings wiggle slowly and sound low. Thin strings wiggle fast and sound high. Can you sing low, then high?",
   "Every sound you hear comes from something wiggling, even your own voice. Touch your throat and hum to feel it! See you next time!"]),
 ("gz2_lever", "How Does a Seesaw Work? It's a Lever!", "LIFT!", SKY, SRC_PHYS, "", "How does a seesaw work?",
  "A seesaw is a simple machine called a lever. It's a long bar resting on a point called a fulcrum. Push down on one side, and the other side goes up!",
  ["Up and down, up and down! What kind of machine is a seesaw?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "A seesaw is a lever! It's a long bar that rests on a point called a fulcrum.",
   "Push down on one end, and the other end goes up. A lever helps you lift heavy things with a small push!",
   "If the heavy box is close to the fulcrum, it's even easier to lift. Can you be a seesaw? One arm up, one arm down!",
   "Next time you ride a seesaw, you're using a simple machine. See you next time!"]),
 ("gz2_ears", "How Do Your Ears Hear? 👂", "WIGGLE!", LAB, SRC_BODY, "👂", "How do your ears hear?",
  "Sound waves travel into your ear and make your eardrum wiggle. Tiny bones pass the wiggle along, and your brain hears the sound!",
  ["Ding, ding! You heard that bell. But how do your ears do it?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "Sounds make the air wiggle in little waves. The waves travel right into your ear!",
   "Inside, they make your eardrum wiggle, like a tiny drum. Then three tiny bones pass the wiggle along.",
   "Those are the smallest bones in your whole body! Then your brain says, that's a bell! Can you cup your hand by your ear and listen?",
   "Your ears are always listening, even in the dark and even with your eyes closed. See you next time!"]),
 ("gz2_solar", "How Do Solar Panels Work? ☀️", "SUN POWER!", SKY, SRC_PHYS, "☀️", "How do solar panels work?",
  "Solar panels catch sunlight and turn it into electricity. That electricity can light up homes, without burning anything!",
  ["The Sun can help turn on the lights in your home. Do you know how?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "With a solar panel! It's a flat panel with lots of special squares that catch sunlight.",
   "The squares turn sunlight into electricity, and wires carry it into a home to power lights and more!",
   "Solar panels work best on bright, sunny days. Can you open your arms wide and soak up the sunshine?",
   "Some garden lights have tiny solar panels too. They charge up all day and glow at night. Look for them! See you next time!"]),
 ("gz2_bee", "How Do Bees Make Honey? 🐝", "HONEY!", SKY, SRC_LIFE, "🐝", "How do bees make honey?",
  "Honeybees drink sweet nectar from flowers. At the hive, they store it in wax honeycomb and fan it with their wings until it turns into thick, sweet honey!",
  ["Honey is sweet, golden, and sticky. Do you know who makes it?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "Honeybees! They fly from flower to flower, all day long, and drink a sweet juice called nectar. They carry it home in their tummies.",
   "Back at the hive, they put the nectar into little wax rooms called a honeycomb.",
   "Then they fan it with their wings, buzz, buzz, until it gets thick and turns into honey! Can you buzz like a bee?",
   "Bees also help flowers make new seeds. Thank you, busy bees! See you next time!"]),
 ("gz2_bike", "How Do Bike Gears Work? 🚲", "SPIN FAST!", SKY, SRC_PHYS, "🚲", "How do bike gears work?",
  "Your pedals turn a big gear. A chain connects it to a small gear on the back wheel. The small gear spins faster, so one push of the pedals turns the wheel lots!",
  ["Pedal, pedal, zoom! How does pedaling make a bike go?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "Your pedals turn a big, round gear with teeth on it. A chain wraps around those teeth.",
   "The chain pulls a small gear on the back wheel. The small gear spins faster, so the wheel turns again and again!",
   "One turn of your pedals can spin the back wheel more than once. Can you pedal your legs in the air like a bike?",
   "That's how a bike goes so fast. And always wear a helmet when you ride! See you next time!"]),
 ("gz2_steam", "Ice, Water, Steam: What Changes Water?", "ICE, WATER, STEAM!", LAB, SRC_PHYS, "💧", "What changes ice into water, and water into steam?",
  "Water can be solid ice, runny water, or floaty steam. Warmth melts ice into water, and lots of heat turns water into steam!",
  ["Ice, water, and steam are all the same thing. Can you guess what it is?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "They're all water! Water can be hard ice, runny water, or floaty steam.",
   "Warm up ice, and it melts into water. Heat water a lot, and it turns into steam that floats up!",
   "Cool steam down, and it turns back into water. Freeze water, and it turns into ice again! Can you be stiff like ice, then wiggly like water?",
   "Steam is very hot, so we only watch it from far away. See you next time!"]),
 ("gz2_moonphases", "Why Does the Moon Change Shape? 🌙", "MOON PHASES!", SPACE, SRC_SPACE, "🌙", "Why does the Moon change shape?",
  "The Moon doesn't make its own light. The Sun shines on it. As the Moon goes around Earth, we see more or less of its sunny side. Those are the Moon's phases!",
  ["Sometimes the Moon is round, and sometimes it looks like a smile. Why?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "The Moon doesn't make its own light. The Sun shines on it, like a giant flashlight.",
   "As the Moon goes around Earth, we see different parts of its sunny side. Those are called phases!",
   "The Moon never really changes shape. We just see more or less of the light. Can you make a round full moon with your arms?",
   "Tonight, look up at the sky and see what shape the Moon is. See you next time!"]),
 ("gz2_screen", "How Does a Screen Show Pictures?", "TINY DOTS!", LAB, SRC_TECH, "📱", "How does a screen show pictures?",
  "A screen is made of tiny dots of light called pixels. Each dot mixes red, green, and blue light to make every color you see!",
  ["Every picture on a screen is made of something super, super tiny. Can you guess what it is?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "Tiny dots of light! A screen has millions of them, all lined up in rows. They're called pixels.",
   "Each pixel has little red, green, and blue lights. Mixing them makes every color, like yellow, pink, and purple!",
   "The dots are so small that your eyes see one big picture. Can you say it with me? Red, green, blue!",
   "Remember to take breaks from screens and go play, too. See you next time!"]),
 ("gz2_teeth", "Why Do We Have Different Teeth? 🦷", "CHOMP!", LAB, SRC_BODY, "🦷", "Why do we have different kinds of teeth?",
  "Front teeth are sharp for biting, and back teeth are wide and bumpy for chewing. Kids have twenty baby teeth, and grown-ups have thirty-two!",
  ["Smile big! Your teeth are not all the same. Did you know each kind of tooth has its own special job?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "Your front teeth are sharp, so they're great for biting, like biting an apple. Crunch!",
   "Your back teeth are wide and bumpy. They chew and mash your food into little bits.",
   "Kids have twenty baby teeth. Later, grown-up teeth grow in, thirty-two of them! Can you show me your biggest smile?",
   "Brush your teeth twice a day, morning and night, to keep them shiny. See you next time!"]),
 ("gz2_daynight", "Why Do We Have Day and Night? 🌍", "EARTH SPINS!", SPACE, SRC_SPACE, "🌍", "Why do we have day and night?",
  "Our Earth is always spinning. The side facing the Sun has day, and the side facing away has night. One whole spin takes one day!",
  ["Where does the Sun go at night? Let's find out!",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "The Sun doesn't go anywhere. Our Earth is spinning, like a slow spinning top!",
   "The side of Earth facing the Sun has day. The side facing away has night. One spin takes one whole day.",
   "When it's daytime for you, it's nighttime for kids on the other side of the world. Can you spin slowly, like the Earth?",
   "So when you go to sleep at night, Earth keeps on spinning, and the Sun comes back in the morning. See you next time!"]),
 ("gz2_turbine", "How Does a Wind Turbine Work? 💨", "WIND POWER!", SKY, SRC_PHYS, "💨", "How does a wind turbine work?",
  "Wind pushes on the long blades and makes them spin. Inside, the spinning makes electricity that travels through wires to homes and schools!",
  ["Whoosh! The wind can help make electricity. How?",
   "Hi! I'm Gizmo the robot. Let's find out how it works!",
   "With a wind turbine! It's a very tall tower, taller than a big tree, with three long blades on top.",
   "When the wind blows, it pushes on the blades and makes them spin around and around, nice and slow.",
   "Inside, the spinning makes electricity, and wires carry it to homes and schools. Can you spin your arms like turbine blades?",
   "Lots of turbines standing together are called a wind farm. Wind is clean energy that never runs out. See you next time!"]),
]

SLOTS = [("2026-11-09", "8:10 AM"), ("2026-11-10", "8:10 AM")] + [(f"2026-11-{d}", t) for d in range(11, 18) for t in ("8:10 AM", "12:10 PM")]
assert len(SH) == len(SLOTS) == 16
shorts = []
for (key, title, badge, look, src, emo, lead, body, says), (date, time) in zip(SH, SLOTS):
    sid = key  # ids are gz2_<topic>
    s = {"id": sid, "animal": key, "title": title, "thumb": badge, "top": NAMES_GIZMO2[key], "bg": look["bg"], "floor": look["floor"], "sources": src,
         "beats": [{"say": t, "act": a.format(b=badge)} for t, a in zip(says, A1)]}
    if "root_bg" in look:
        s["root_bg"] = look["root_bg"]
    shorts.append(s)
    d = (f"{lead} Gizmo the robot finds out! {emo}🤖\nA fun science Short for kids ages 4–8 from Gizmo Explains.\n\n{body}\n\n{BOILER}\n\n#Shorts {TAGS}")
    plan.append({"file": f"gizmo/{sid}.mp4", "title": title, "description": d, "date": date, "time": time, "status": "to_upload"})

json.dump(shorts, open("shorts_gizmo2.json", "w"), indent=1, ensure_ascii=False)
order = {"8:10 AM": 0, "12:10 PM": 1, "2:10 PM": 2}
plan.sort(key=lambda p: (p["date"], order[p["time"]]))
json.dump(plan, open("upload_plan_gizmo_week2.json", "w"), indent=1, ensure_ascii=False)

# ---- checks ----
import art_gizmo
CHECK = []
known = set(SCENES_GIZMO2) | set(art_gizmo.SCENES10)
for s in shorts:
    assert s["animal"] in known, s["animal"]
    w = sum(len(b["say"].split()) for b in s["beats"])
    print(f"short {s['id']:16s} {w:4d} words  {len(s['title']):2d}ch  {s['title']}")
    CHECK.append((len(s["title"]) <= 60 and 100 <= w <= 125, s["id"], w))
for eid, title, keys, *_ in EPS:
    e = json.load(open(f"eps/{eid}.json"))
    assert all(a["key"] in known for a in e["animals"])
    t = [l[0] for l in e["intro"] + e["recap"] + e["outro"]] + [l[0] for a in e["animals"] for l in a["lines"]]
    w = sum(len(x.split()) for x in t)
    print(f"ep {eid:18s} {w:4d} words  {len(title):2d}ch  {title}")
    CHECK.append((len(title) <= 60 and 600 <= w <= 720, eid, w))
print(len(plan), "plan entries")
bad = [c for c in CHECK if not c[0]]
print("FAILED:", bad) if bad else print("all checks ok")
assert not bad
