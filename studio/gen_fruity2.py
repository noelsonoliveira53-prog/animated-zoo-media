"""Fruity Friends week 2: writes shorts_fruity2.json, eps/fr_ep06..11_*.json, upload_plan_fruity2.json and episode thumbnails.
Run: python3 gen_fruity2.py   (thumb PNGs are screenshotted separately with node + playwright)."""
import json, re, os
from art_fruity import SCENES8, PIPKIKO as HOST
from art_fruity2 import SCENES_FRUITY2, NAMES_FRUITY2

S = {**SCENES8, **SCENES_FRUITY2}
SRC = ["Kids nutrition & healthy habits basics (USDA MyPlate kids, CDC handwashing & cough/sneeze etiquette, AAP sun safety and sleep guidance, FDA produce-washing tips)"]

# key: name, say (word to repeat), clue, fact1, fact2, do-it, question, answer, badge, extra, this-line (optional)
F = {
 "fr2_grapes": ("Grapes", "grapes", "they're small and round, and they grow together in a big bunch!",
   "Grapes grow on long, twisty plants called vines. They hang down in big, heavy bunches.", "Grapes can be green, red or purple. And raisins are grapes that dried in the sun!",
   "Can you make a bunch of grapes? Hold up your fingers and wiggle them, one, two, three!", "How do grown-ups get grapes ready for little kids?",
   "They cut them into small pieces, so they're easy to eat!", "GRAPES!", "Grapes are sweet and juicy, and they make a cool, crunchy snack."),
 "fr2_pear": ("Pear", "pear", "it's skinny at the top, round at the bottom, and it grows on a tree!",
   "Pears grow on trees, just like apples do. They can be green, yellow, brown or red.", "A pear is ready when it feels a little soft near the top, by the stem.",
   "Can you make a pear shape? Hands up high and skinny, then make your tummy round!", "What's hiding in the middle of a pear?",
   "Little brown seeds! A new pear tree could grow from one.", "PEAR!", "Pears are soft and sweet, and so juicy you might need a napkin!"),
 "fr2_kiwi": ("Kiwi", "kiwi", "it's brown and fuzzy outside, but it's a big surprise inside!",
   "A kiwi has fuzzy brown skin, a little bit like a teddy bear.", "But inside, it's bright green, with a ring of tiny black seeds. And yes, you can eat the seeds!",
   "Can you pretend to scoop a kiwi with a spoon? Scoop, scoop, yum!", "What color is a kiwi on the inside?",
   "Bright green! With tiny black seeds all around.", "KIWI!", "Kiwis taste sweet and a little bit tangy, all at the same time."),
 "fr2_cherries": ("Cherries", "cherries", "they're little and red, and they often come in pairs with long stems!",
   "Cherries grow on trees. In spring, the trees are covered in pretty pink and white flowers.", "Later, the flowers turn into shiny red cherries, hanging by their long stems.",
   "Can you hold up two fingers, like a pair of cherries? Wiggle, wiggle!", "What's in the middle of a cherry?",
   "A hard pit! A grown-up takes it out for you first.", "CHERRIES!", "Cherries are sweet, shiny and red, like little jewels."),
 "fr2_peach": ("Peach", "peach", "it's round and fuzzy, and it can be orange, yellow and pink!",
   "Peaches grow on trees. Their skin is soft and fuzzy, like a cozy blanket.", "Inside, a peach is sweet and juicy, and it smells so yummy.",
   "Can you rub your cheek gently, like soft peach fuzz? So soft!", "What's in the middle of a peach?",
   "A big, bumpy pit! A grown-up cuts around it for you.", "PEACH!", "A ripe peach is so juicy, it can drip right down your chin!"),
 "fr2_pineapple": ("Pineapple", "pineapple", "it's spiky on top, bumpy outside, and sweet and yellow inside!",
   "Pineapples do not grow on trees! They grow on a spiky plant, close to the ground.", "Each pineapple grows for a long, long time. More than a whole year!",
   "Can you make spiky leaves on your head? Hands up, fingers out, like a pineapple crown!", "What are the spiky leaves on top called?",
   "The crown! Like a king or queen of fruits.", "PINEAPPLE!", "Pineapple is sweet and tangy, and so sunny yellow inside."),
 "fr2_mango": ("Mango", "mango", "it's shaped like a big bean, and it can be green, yellow, orange and red!",
   "Mangoes grow on big, tall trees where the weather is warm.", "Inside, a mango is soft, orange and very sweet.",
   "Can you pretend to pick a mango from a tall tree? Reach up, up, up!", "What's hiding in the middle of a mango?",
   "One big, flat seed! It's almost as big as your hand.", "MANGO!", "Mangoes are sweet and soft, and they smell like sunshine."),
 "fr2_lemon": ("Lemon", "lemon", "it's bright yellow, it grows on a tree, and it tastes very sour!",
   "Lemons grow on trees, and they are full of juice.", "Lemon juice is sour! It can make your face go squish, like this.",
   "Can you make a silly sour face? Squeeze your eyes and pucker up!", "How can we use a lemon?",
   "Squeeze a little juice into water, or on fish, or into a yummy sauce!", "LEMON!", "Lemons are sour all by themselves, but a little squeeze adds a bright, fresh taste."),
 "fr2_avocado": ("Avocado", "avocado", "it's bumpy and dark green outside, and soft and creamy inside!",
   "An avocado grows on a tree. And guess what? It's a fruit!", "Inside, it's soft, creamy and light green, so you can mash it with a fork.",
   "Can you pretend to mash an avocado? Squish, squish, squish!", "What's the big round ball in the middle?",
   "The seed! It's called a pit, and it's very big.", "AVOCADO!", "You can spread mashed avocado on toast, or dip veggies in it."),
 "fr2_tomato": ("Tomato", "tomato", "it's round and red, and it grows on a leafy green plant!",
   "Tomatoes grow on plants in the garden. They start out small and green.", "In the warm sun, they turn red. Some tomatoes turn yellow, orange or even purple!",
   "Can you grow tall like a tomato plant? Stretch your arms like leafy branches!", "Is a tomato a fruit or a veggie?",
   "It's a fruit, because it has seeds inside! But we often eat it like a veggie.", "TOMATO!", "Tomatoes are juicy in salads, and they make yummy sauce, too."),
 "fr2_cucumber": ("Cucumber", "cucumber", "it's long and green, cool and crunchy!",
   "Cucumbers grow on vines that love to climb up and up.", "Cucumbers are mostly water inside. That's why they feel so cool and fresh!",
   "Can you climb like a cucumber vine? Hand over hand, up, up, up!", "What can a cucumber turn into?",
   "A pickle! Pickles are cucumbers soaked in a special salty juice.", "CUCUMBER!", "Cucumber slices are cool and crunchy on a warm day."),
 "fr2_lettuce": ("Lettuce", "lettuce", "it's green and leafy, and it's crunchy in a salad!",
   "Lettuce grows in the garden, close to the ground.", "Lots of leaves grow together in a round bunch called a head.",
   "Can you crunch like lettuce? Make a big crunchy sound! Crunch, crunch!", "What can we make with lettuce?",
   "A salad! Or put it in a sandwich for a crunchy bite.", "LETTUCE!", "Lettuce can be green or even red, with leaves that are curly or flat."),
 "fr2_bellpepper": ("Bell Pepper", "bell pepper", "it's shiny and crunchy, and it comes in lots of colors!",
   "Bell peppers can be green, yellow, orange or red.", "Many peppers start out green. If they stay on the plant longer, they change color!",
   "Can you name a pepper color with me? Red! Yellow! Orange! Green!", "What's inside a bell pepper?",
   "It's almost empty, with lots of tiny seeds in the middle!", "BELL PEPPER!", "Bell peppers are crunchy and a little bit sweet. Not spicy at all!"),
 "fr2_harvest": ("Garden Harvest", "harvest", "it's when we pick food from the garden, because it's ready to eat!",
   "Plants need sunshine, water and good soil to grow.", "When the food is ready, we pick it. That's called a harvest!",
   "Can you pretend to dig, plant and water a seed? Dig, drop, sprinkle!", "What do plants need to grow?",
   "Sunshine, water and soil! And a little bit of time.", "HARVEST!", "After gardening, we wash our hands and the food we picked.",
   "This is a garden harvest! Can you say harvest?"),
 "fr2_potato": ("Potato", "potato", "it's brown and lumpy, and it grows hiding under the ground!",
   "Potatoes grow under the ground. Only the green leaves poke out on top.", "Potatoes can be brown, red, yellow or even purple!",
   "Can you dig for potatoes? Dig, dig, dig, and pull one up!", "Do we eat potatoes raw?",
   "No! We cook them first. They can be mashed, baked or roasted.", "POTATO!", "The little dots on a potato are called eyes. A new plant can grow from them!"),
 "fr2_sweetpotato": ("Sweet Potato", "sweet potato", "it's long and reddish outside, and bright orange inside!",
   "Sweet potatoes grow under the ground, like potatoes do.", "Most sweet potatoes are orange inside. Some are purple or white!",
   "Can you stretch out long, like a sweet potato? Long, long, long!", "Why is it called a sweet potato?",
   "Because it tastes a little sweet when it's cooked!", "SWEET POTATO!", "Sweet potatoes are cooked before we eat them, soft and warm."),
 "fr2_mushroom": ("Mushrooms", "mushroom", "it has a round cap on top, like a little umbrella!",
   "Mushrooms are not plants! They're a fungus. That's a fun word: fungus!", "Mushrooms grow in cool, shady places. They don't grow from seeds.",
   "Can you make a mushroom? Stand up tall, and hold your arms round like a cap!", "Where do we get mushrooms to eat?",
   "From the store, or from a grown-up! We never pick wild ones to eat.", "MUSHROOM!", "Mushrooms can be white, brown, big or tiny, and grown-ups cook them in yummy meals.",
   "These are mushrooms! Can you say mushroom?"),
 "orangefruit": ("Orange", "orange", "it's round and juicy, and it has the same name as its color!",
   "Oranges grow on trees, where the weather is warm and sunny.", "Peel off the skin, and inside are juicy pieces called segments.",
   "Can you pretend to peel an orange? Round and round and round!", "How many pieces are inside an orange?",
   "Often about ten! Let's count them next time.", "ORANGE!", "Oranges are sweet and juicy, and they smell so fresh."),
 "carrot": ("Carrot", "carrot", "it's orange and crunchy, and it grows under the ground!",
   "Carrots grow down in the dirt. The green leaves stay on top.", "A carrot is a root. It pulls up water from the ground for the plant.",
   "Can you pull a carrot out of the ground? Pull, pull, POP!", "Are carrots always orange?",
   "No! Some carrots are purple, yellow or white.", "CARROT!", "Carrots are crunchy raw, and soft and sweet when they're cooked."),
 "peas": ("Peas", "peas", "they're little green balls that live in a pod!",
   "Peas grow on climbing vines, inside a long green pod.", "Each pea is really a seed! Plant one, and a new pea plant can grow.",
   "Can you count peas in a pod with me? One, two, three, four, five!", "Where do peas live?",
   "Inside a pod! All in a row, like a cozy bed.", "PEAS!", "Peas are sweet and green, and fun to count on your plate."),
 "fr2_breakfast": ("Breakfast", "breakfast", "it's the very first meal of the day, in the morning!",
   "We sleep all night long. In the morning, breakfast gives us energy to play and learn.", "Breakfast can be oatmeal with berries, toast, eggs, yogurt or fruit.",
   "Can you stretch and say good morning? Arms up, big smile! Good morning!", "When do we eat breakfast?",
   "In the morning, after we wake up!", "BREAKFAST!", "Every family has its own favorite breakfast. What's yours?"),
 "fr2_washproduce": ("Wash Your Food", "wash", "we rinse fruits and veggies with water before we eat them!",
   "First, wash your hands. Then a grown-up helps rinse the fruits and veggies under running water.", "We rub them gently with our hands. Just water, no soap!",
   "Can you pretend to rinse an apple? Rub, rub, rub, under the water!", "Why do we wash fruits and veggies?",
   "To wash away dirt and germs, so they're clean and ready!", "WASH IT!", "Clean food and clean hands make snack time even better.",
   "This is washing our food! Can you say wash?"),
 "fr2_lunchbox": ("Pack a Lunch", "lunch", "we put yummy food in a box to take with us!",
   "A packed lunch can have a fruit, a veggie, a sandwich and water.", "A little cool pack helps keep the food fresh until lunchtime.",
   "Can you help pack a pretend lunch? Apple in, carrots in, sandwich in, close the lid!", "What's a good drink to pack?",
   "Water! In a bottle you can fill again.", "LUNCH!", "You can help choose what goes in your lunchbox. That's a fun job!",
   "This is packing a lunch! Can you say lunch?"),
 "fr2_trynew": ("Try New Foods", "try it", "it's when we taste something we never tasted before!",
   "Trying a new food is like a little adventure for your mouth.", "Start with a tiny taste. Is it crunchy? Soft? Sweet? Sour?",
   "Can you pretend to take a tiny taste? Nibble, nibble! Hmm!", "What if you don't like it the first time?",
   "That's okay! Sometimes we like a food after trying it a few times.", "TRY IT!", "Every tiny taste helps you learn about a new food.",
   "This is trying new foods! Can you say try it?"),
 "fr2_market": ("Farmers Market", "market", "it's a place outside where farmers sell the food they grew!",
   "At the farmers market, farmers bring fruits and veggies from their farms.", "You can see what's growing right now, like apples in fall or berries in summer.",
   "Can you carry a pretend basket? Pick a red one, a green one, an orange one!", "What do we say to the farmer?",
   "Hello, and thank you!", "MARKET!", "Bring a bag, and pick one new fruit or veggie to try.",
   "This is the farmers market! Can you say market?"),
 "fr2_play": ("Move and Play", "play", "we run, jump, dance and have fun with our bodies!",
   "Moving your body makes your heart pump and your muscles strong.", "You can run, jump, dance, climb, or play catch with a ball!",
   "Let's move! Jump, jump, jump! Now spin around! Now freeze!", "How often should we move and play?",
   "Every day! Little kids love to move a lot.", "PLAY!", "After playing, drink some water and take a rest.",
   "This is moving and playing! Can you say play?"),
 "fr2_sunscreen": ("Sunscreen", "sunscreen", "it's a cream we put on our skin before we play in the sun!",
   "Sunscreen helps protect your skin from the strong sunshine.", "A grown-up helps put it on before you go outside.",
   "Can you pretend to rub on sunscreen? Nose, cheeks, arms and legs!", "What else helps us in the sun?",
   "A hat, sunglasses, and playing in the shade!", "SUNSCREEN!", "After swimming, a grown-up puts on a little more sunscreen."),
 "fr2_sneeze": ("Cover Your Sneeze", "elbow", "ah, ah, ah-choo! Where should that sneeze go?",
   "When you sneeze or cough, cover it with your elbow or a tissue.", "That keeps germs from flying to your friends.",
   "Can you do a pretend sneeze into your elbow? Ah, ah, ah-choo!", "What do we do after we use a tissue?",
   "Throw it away, and wash your hands!", "ELBOW!", "Covering your sneeze is a kind way to help your friends stay well.",
   "This is covering your sneeze! Can you say elbow?"),
 "water": ("Drink Water", "water", "it's clear and cool, and it's the best drink when you're thirsty!",
   "Water helps your whole body work, from your head to your toes.", "When you run and play, you get thirsty. That's your body asking for water!",
   "Can you take a pretend sip? Glug, glug, glug! Ahh!", "When should we drink water?",
   "When we're thirsty, at mealtime, and after we play!", "DRINK WATER!", "A water bottle you can fill again is great to take along.",
   "This is drinking water! Can you say water?"),
 "sleep": ("Bedtime", "bedtime", "we put on pajamas, close our eyes, and dream!",
   "Sleep helps your body grow and rest.", "Little kids need lots of sleep, even more than grown-ups!",
   "Can you do a big pretend yawn and stretch? Yaaawn!", "What helps us get ready for bed?",
   "A bath, brushing teeth, a story, and a cozy, quiet room.", "BEDTIME!", "A good sleep helps you wake up ready to play."),
}
HABIT = {"fr2_harvest", "fr2_breakfast", "fr2_washproduce", "fr2_lunchbox", "fr2_trynew", "fr2_market", "fr2_play", "fr2_sunscreen", "fr2_sneeze", "water", "sleep"}


def lines(k, nxt):
    v = F[k]
    n, say, clue, f1, f2, do, q, a, badge, extra = v[:10]
    this = v[10] if len(v) == 11 else f"This is {n}! Can you say {say}?"
    bye = "Hooray! Great job!" if k in HABIT else f"Bye-bye, {n}!"
    return [[f"Here's a clue: {clue} Can you guess?", "q"], [f"{nxt}: {n}!", "enter"], [this, "zoom"],
            [f1, "fx+bob"], [f2, "bob"], [do, "wiggle"], [q, "fxoff+fx2off+q"], [a, f"fx2+badge:{badge}"],
            [f"Let's say it together: {say.upper()}!", "zoom"], [f"One more time, nice and loud: {say.upper()}!", "zoom"],
            [extra, "fxoff+fx2off+bob"], [bye, "bob"]]


EPS = [
 ("fr_ep06_orchard", "More Fruits for Kids! Grapes, Pear, Kiwi and More with Pip", ["fr2_grapes", "fr2_pear", "fr2_kiwi", "fr2_cherries", "fr2_peach"], "five fruity friends that grow on trees and vines",
  ["Grapes, in a big bunch.", "Pear, skinny on top and round on the bottom.", "Kiwi, fuzzy outside and green inside.", "Cherries, with a pit in the middle.", "And peach, soft and fuzzy!"], ("MORE", "FRUITS!")),
 ("fr_ep07_sunny", "Sunny Fruits for Kids! Pineapple, Mango and More with Pip", ["fr2_pineapple", "fr2_mango", "fr2_lemon", "fr2_avocado", "orangefruit"], "five sunny fruits",
  ["Pineapple, with a spiky crown.", "Mango, with one big seed.", "Lemon, sour and bright.", "Avocado, soft and creamy.", "And orange, full of juicy pieces!"], ("SUNNY", "FRUITS!")),
 ("fr_ep08_garden", "Garden Veggies for Kids! Tomato, Lettuce and More with Kiko", ["fr2_tomato", "fr2_cucumber", "fr2_lettuce", "fr2_bellpepper", "fr2_harvest"], "five friends from the garden",
  ["Tomato, from green to red.", "Cucumber, cool and crunchy.", "Lettuce, in a leafy head.", "Bell pepper, in lots of colors.", "And a garden harvest!"], ("GARDEN", "VEGGIES!")),
 ("fr_ep09_surprise", "Veggie Surprises! Potato, Mushrooms and More with Kiko", ["fr2_potato", "fr2_sweetpotato", "fr2_mushroom", "carrot", "peas"], "five veggie surprises",
  ["Potato, hiding underground.", "Sweet potato, orange inside.", "Mushrooms, a fun fungus.", "Carrot, a crunchy root.", "And peas, little seeds in a pod!"], ("VEGGIE", "SURPRISE!")),
 ("fr_ep10_mealtime", "Mealtime Habits for Kids! Breakfast, Lunch and More with Pip", ["fr2_breakfast", "fr2_washproduce", "fr2_lunchbox", "fr2_trynew", "fr2_market"], "five fun mealtime habits",
  ["Breakfast, to start the day.", "Wash fruits and veggies with water.", "Pack a lunch to take along.", "Try a tiny taste of something new.", "And visit the farmers market!"], ("MEALTIME", "HABITS!")),
 ("fr_ep11_healthyday", "A Healthy Day for Kids! Play, Sunscreen and More with Kiko", ["fr2_play", "fr2_sunscreen", "fr2_sneeze", "water", "sleep"], "five habits for a happy, healthy day",
  ["Move and play every day.", "Sunscreen before the sunshine.", "Sneeze into your elbow.", "Drink water when you're thirsty.", "And a cozy bedtime!"], ("HEALTHY", "DAY!")),
]
WELCOME = {
 "fr_ep06_orchard": "Welcome to Fruity Friends! Today we're meeting five fruity friends that grow on trees and vines.",
 "fr_ep07_sunny": "Welcome to Fruity Friends! Today we're meeting five sunny fruits, bright and sweet and a little bit sour.",
 "fr_ep08_garden": "Welcome to Fruity Friends! Today we're visiting the garden to meet five green and growing friends.",
 "fr_ep09_surprise": "Welcome to Fruity Friends! Today we're meeting five veggie surprises, and some of them hide underground!",
 "fr_ep10_mealtime": "Welcome to Fruity Friends! Today we're learning five fun habits for mealtime and snack time.",
 "fr_ep11_healthyday": "Welcome to Fruity Friends! Today we're learning five habits for a happy, healthy day.",
}
ORD = ["First up", "Next", "Here comes", "Now meet", "And last"]
os.makedirs("eps", exist_ok=True)
for eid, title, keys, what, rec, _ in EPS:
    ep = {"id": eid, "title": title,
          "intro": [["Hi, friends! I'm Pip the strawberry, and this is my buddy Kiko the broccoli!", ""], [WELCOME[eid], ""],
                    ["Can you count with me? One, two, three, four, five!", ""], ["Yummy food and healthy habits help us grow, play and learn every day.", ""],
                    ["Ready? Let's go to the kitchen and find out!", ""]],
          "animals": [{"key": k, "lines": lines(k, ORD[i])} for i, k in enumerate(keys)],
          "recap": [["Yummy! Let's remember what we learned.", "@title"]] + [[r, "@" + k] for r, k in zip(rec, keys)],
          "outro": [["Which one was your favorite? Tell a grown-up, and try something new this week!", ""], ["Bye, friends! See you next time on Fruity Friends!", ""]]}
    json.dump(ep, open(f"eps/{eid}.json", "w"), indent=1, ensure_ascii=False)

# ---------------- Shorts ----------------
SH = [  # id-topic, title, bg, hook, closing tip
 ("pineapple", "Does a Pineapple Grow on a Tree?", "#fff6d6", "Spiky, bumpy and sweet. But where does a pineapple grow? Not where you think!", "You can even grow a new pineapple plant from the crown."),
 ("sneeze", "Where Should You Sneeze?", "#f1ecff", "Ah, ah, ah-choo! Quick, where should that sneeze go?", "Elbow or tissue, then wash your hands. Great job!"),
 ("kiwi", "What Color Is a Kiwi Inside?", "#f3ffe0", "Brown, fuzzy, and a little bit like a teddy bear. What's inside?", "Kiwis grow on long, climbing vines."),
 ("washproduce", "Why Do We Wash Fruits and Veggies?", "#e6f6ff", "Splish, splash! Why do apples and carrots take a bath?", "Wash your hands first, then wash the food."),
 ("tomato", "Is a Tomato a Fruit or a Veggie?", "#ffe9e6", "Red, round and juicy. Is it a fruit or a veggie? Let's find out!", "Tomatoes can be big like a ball or tiny like a marble."),
 ("lemon", "Why Does a Lemon Taste So Sour?", "#fffbd6", "Yellow, bright, and it makes your face go squish! What is it?", "Lemon juice is sour because it's full of a special sour juice called citric acid."),
 ("trynew", "How Do You Try a New Food?", "#f4eeff", "A brand new food on your plate. What do you do? Let's be brave tasters!", "Maybe next time, it will be your new favorite."),
 ("mango", "What's Inside a Mango?", "#fff1e0", "Green, yellow, orange and red, all on one fruit! What's inside?", "Mango trees can grow taller than a house."),
 ("potato", "Where Do Potatoes Grow?", "#fbf1e4", "Brown, lumpy and hiding! Where do potatoes grow?", "One potato plant can grow lots of potatoes under the ground."),
 ("sunscreen", "Why Do We Wear Sunscreen?", "#fff8e1", "Sunny day, time to play! But first, what do we put on our skin?", "Hats and shade help too, on every sunny day."),
 ("grapes", "How Do Grapes Grow?", "#f3ecff", "Little, round, and they hang out in a big group. What are they?", "A bunch of grapes can have more than one hundred grapes!"),
 ("mushroom", "Is a Mushroom a Plant?", "#f7efe6", "It has a cap like a tiny umbrella. But is it a plant? Nope!", "Mushrooms make tiny specks called spores, instead of seeds."),
 ("breakfast", "Why Do We Eat Breakfast?", "#fff6d6", "Good morning, sunshine! What's the very first meal of the day?", "Some families eat rice, beans or soup for breakfast, too."),
 ("bellpepper", "What Colors Can a Bell Pepper Be?", "#ffeaea", "Red, yellow, orange, green. One veggie, so many colors!", "Green peppers that stay on the plant longer can turn red, yellow or orange."),
 ("avocado", "What's the Big Ball Inside an Avocado?", "#eefbe0", "Bumpy outside, creamy inside, and a giant ball in the middle! What is it?", "Avocado trees can grow from that big seed."),
 ("play", "Why Do We Move and Play Every Day?", "#ffeef6", "Jump, spin, dance and freeze! Why is moving so good for us?", "Find a fun way to move with your family today."),
]
DATES = [("2026-11-09", "8:20 AM"), ("2026-11-10", "8:20 AM")] + [(f"2026-11-{d}", t) for d in range(11, 18) for t in ("8:20 AM", "12:20 PM")]
out = []
for (t, title, bg, hook, tip) in SH:
    k = "fr2_" + t
    n, say, clue, f1, f2, do, q, a, badge, extra = F[k][:10]
    out.append({"id": k, "animal": k, "title": title, "thumb": badge, "top": NAMES_FRUITY2[k], "bg": [bg, "#fffdf4"], "floor": "#f6c992", "sources": SRC,
                "beats": [{"say": hook, "act": "hook"}, {"say": "Hi! I'm Pip the strawberry, and this is Kiko! Welcome to Fruity Friends!", "act": "milo_in"},
                          {"say": f"{n}! {f1} {f2}", "act": f"zoom+badge:{badge}"}, {"say": f"{q} {a}", "act": "fx+bob"},
                          {"say": do, "act": "wiggle"}, {"say": f"{extra} {tip} See you next time on Fruity Friends!", "act": "fxoff+outro"}]})
json.dump(out, open("shorts_fruity2.json", "w"), indent=1, ensure_ascii=False)

# ---------------- thumbnails + upload plan ----------------
font = "@font-face{font-family:Baloo;src:url(/root/zoo/vendor/f/package/files/baloo-2-latin-800-normal.woff2)}"
cfg = dict(name="Fruity Friends", host_desc="Pip the strawberry and Kiko the broccoli", aud="2-6", aud2="2–6", emoji="🍓🥦",
           tag="#HealthyHabits #FruitsForKids #VegetablesForKids #KidsLearning", bg="#ffe9c7", stroke="#b91c1c", accent="#3aa856", ground="#f6c992",
           ep_time="2:20 PM", prefix="fruity", short_kind="A fun healthy-habits Short", ep_kind="healthy food adventure")


def animal(s):
    i = s.index('<g id="animal"'); j = i; depth = 0
    for m in re.finditer(r'<g[\s>]|</g>', s[i:]):
        depth += 1 if m.group().startswith('<g') else -1
        if depth == 0: j = i + m.end(); break
    return "".join(re.findall(r'<defs>.*?</defs>', s, re.S)) + s[i:j]


def pet(k, x, y, h):
    w = h * 1080 / 1100
    return f'<svg viewBox="0 0 1080 1100" width="{w:.0f}" height="{h}" style="position:absolute;left:{x}px;top:{y}px">{animal(S[k])}</svg>'


pos = [(-40, 300, 400), (160, 350, 360), (360, 310, 390), (560, 350, 360), (760, 320, 380)]
B = f"{cfg['name']} makes gentle, colorful videos for little learners. New videos every day! Made with care for ages {cfg['aud']}. Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing."
plan = []
for s, (d, tm) in zip(out, DATES):
    b = [x["say"] for x in s["beats"]]
    desc = f"{b[0]} {cfg['host_desc']} find out! {cfg['emoji']}\n{cfg['short_kind']} for kids ages {cfg['aud2']} from {cfg['name']}.\n\n{' '.join(b[2:5])}\n\n{B}\n\n#Shorts {cfg['tag']}"
    plan.append({"file": f"{cfg['prefix']}/{s['id']}.mp4", "title": s["title"], "description": desc, "date": d, "time": tm, "status": "to_upload"})
for (eid, title, keys, what, rec, (a, b2)), d in zip(EPS, [f"2026-11-{x}" for x in range(12, 18)]):
    e = json.load(open(f"eps/{eid}.json"))
    p = "".join(pet(v, x, y, h) for v, (x, y, h) in zip(keys, pos))
    html = f"""<html><head><style>{font}*{{margin:0}}body{{width:1280px;height:720px;overflow:hidden;position:relative;font-family:Baloo;background:radial-gradient(circle at 70% 30%,#fff7d6 0,{cfg['bg']} 62%)}}
.t{{position:absolute;left:40px;font-size:{110 if len(a)<12 else 92}px;line-height:1;color:#fff;-webkit-text-stroke:14px {cfg['stroke']};paint-order:stroke fill;text-shadow:0 8px 0 rgba(0,0,0,.18)}}
#n{{position:absolute;right:40px;top:30px;width:180px;height:180px;border-radius:50%;background:{cfg['accent']};color:#fff;font-size:140px;line-height:205px;text-align:center;box-shadow:0 8px 0 rgba(0,0,0,.18)}}
#m{{position:absolute;left:930px;top:250px;transform:scale(1.05);transform-origin:0 0}}#g{{position:absolute;left:0;right:0;bottom:0;height:110px;background:{cfg['ground']}}}</style></head>
<body><div id="g"></div>{p}<div class="t" style="top:28px">{a}</div><div class="t" style="top:140px;color:#ffe066">{b2}</div><div id="n">5</div><div id="m">{HOST}</div></body></html>"""
    open(f"brand/{cfg['prefix']}/thumb_{eid}.html", "w").write(html)
    learn = "\n".join("• " + r[0] for r in e["recap"][1:])
    desc = f"Join {cfg['host_desc']} for a 5-minute {cfg['ep_kind']}! {e['intro'][1][0]} {cfg['emoji']}\nMade for little learners ages {cfg['aud2']}: guess-what clues, move-along fun, and a recap at the end.\n\nWhat we learn today:\n{learn}\n\n{B}\n\n{cfg['tag']}"
    plan.append({"file": f"{cfg['prefix']}/{eid}.mp4", "title": e["title"], "description": desc, "date": d, "time": cfg["ep_time"], "status": "to_upload", "thumb": f"brand/{cfg['prefix']}/thumb_{eid}.png"})
json.dump(plan, open("upload_plan_fruity2.json", "w"), indent=1, ensure_ascii=False)
print("ok", len(out), "shorts,", len(EPS), "episodes,", len(plan), "plan rows")
