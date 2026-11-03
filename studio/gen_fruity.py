"""Writes Fruity Friends Short + episode scripts (shorts_fruity.json, eps/fr_ep0*.json)."""
import json
SRC = ["Kids nutrition & healthy habits basics (USDA MyPlate kids, CDC handwashing, ADA toothbrushing guidance)"]
# key: (name, clue, fact1, fact2, doit, guessQ, guessA, badge, extra, warm, bye)
F = {
 "apple": ("Apple", "it's round and crunchy, and it can be red, green or yellow!", "Apples grow on trees.", "Crunch, crunch! Apples are fun to bite.",
           "Can you pretend to pick an apple from a tree? Reach up high!", "What's hiding inside an apple?", "Little seeds! They make a star shape.", "APPLE!", "Apples help keep your teeth and tummy happy.", "apple"),
 "banana": ("Banana", "it's long and yellow, and you peel it!", "Bananas grow in big bunches.", "Peel it down, down, down, and take a bite!",
            "Can you pretend to peel a banana? Peel, peel, peel!", "What color is a banana before it's ready?", "Green! It turns yellow when it's ready.", "BANANA!", "Bananas give you energy to run and play.", "banana"),
 "orangefruit": ("Orange", "it's round, it's juicy, and it has the same name as its color!", "Oranges are full of juicy pieces.", "Each little piece is called a segment.",
            "Can you make a big round orange with your arms?", "What's inside an orange?", "Juicy slices! Like a little wheel.", "ORANGE!", "Oranges help your body stay strong.", "orange"),
 "watermelon": ("Watermelon", "it's green outside and pink inside!", "Watermelons are big and heavy.", "They are full of water. That's why they're so juicy!",
                "Can you take a big pretend bite? Chomp!", "What are the little black dots?", "Seeds! Watermelons have lots of them.", "WATERMELON!", "Watermelon is a cool treat on a hot day.", "watermelon"),
 "blueberry": ("Blueberries", "they're tiny, round and blue!", "Blueberries grow on little bushes.", "They are small, so you can eat a handful!",
               "Can you count three blueberries on your fingers? One, two, three!", "What color are blueberries?", "Blue! Well, a little bit purple, too.", "BLUEBERRY!", "Blueberries are tiny but very good for you.", "blueberries"),
 "carrot": ("Carrot", "it's orange and crunchy, and it grows under the ground!", "Carrots grow down in the dirt.", "The green leaves stay on top, and the carrot hides below!",
            "Can you pull a carrot out of the ground? Pull, pull, POP!", "Are carrots always orange?", "No! Some are purple, yellow or white.", "CARROT!", "Carrots help your eyes stay healthy.", "carrot"),
 "broccoli": ("Broccoli", "it looks like a tiny green tree!", "Broccoli is a green vegetable.", "Each little bump is called a floret.",
              "Can you stand tall like a broccoli tree? Arms up!", "What does broccoli look like?", "Little trees! You can be a giant!", "BROCCOLI!", "Broccoli helps you grow big and strong.", "broccoli"),
 "peas": ("Peas", "they're little green balls that live in a pod!", "Peas grow inside a pod.", "Open the pod, and there they are, in a row!",
          "Can you count the peas with me? One, two, three, four!", "Where do peas live?", "Inside a pod! Like a cozy bed.", "PEAS!", "Peas are sweet and green and fun to count.", "peas"),
 "corn": ("Corn", "it's yellow, and it has lots of little bumps in rows!", "Corn grows on tall plants.", "Each yellow bump is a kernel.",
          "Can you grow tall like a corn plant? Stretch, stretch!", "What are the yellow bumps called?", "Kernels! Lots and lots of kernels.", "CORN!", "Corn is sweet and sunny yellow.", "corn"),
 "pumpkin": ("Pumpkin", "it's big, round and orange, and it grows on a vine!", "Pumpkins grow on long, curly vines.", "Some pumpkins get really, really big!",
             "Can you make yourself round like a pumpkin? Curl up!", "What's inside a pumpkin?", "Seeds and soft orange insides!", "PUMPKIN!", "Pumpkin can be soup, or even bread!", "pumpkin"),
 "handwash": ("Wash Hands", "we use soap and water, and we make bubbles!", "Wash your hands before you eat.", "And after you use the potty, too!",
              "Rub your hands together with me! Scrub, scrub, scrub!", "How long should we scrub?", "Twenty seconds! Like singing a song.", "WASH HANDS!", "Clean hands keep germs away.", "clean hands"),
 "toothbrush": ("Brush Teeth", "we use a toothbrush to make our smile sparkle!", "Brush your teeth in the morning and at night.", "Brush the top teeth and the bottom teeth.",
                "Can you pretend to brush? Round and round!", "How long should we brush?", "Two minutes! Ask a grown-up to help.", "BRUSH TEETH!", "Brushing keeps your smile bright.", "sparkly teeth"),
 "water": ("Drink Water", "it keeps us cool, and it's the best drink for our body!", "Water helps your body work.", "Drink water when you play and when you're thirsty.",
           "Can you take a pretend sip? Glug, glug, glug!", "When should we drink water?", "When we're thirsty, and when we play!", "DRINK WATER!", "Water is the best drink for kids.", "water"),
 "sleep": ("Bedtime", "we close our eyes, and we dream!", "Sleep helps your body grow.", "Your body rests, so you can play tomorrow!",
           "Can you pretend to yawn and stretch? Yaaawn!", "What helps us sleep well?", "A cozy bed, and a quiet room!", "BEDTIME!", "A good sleep makes a happy morning.", "sleep"),
 "share": ("Sharing", "it's when we give some to a friend!", "Sharing makes friends happy.", "You can share toys, and you can share snacks!",
           "Can you give a friend a big pretend high five?", "What do we say when someone shares?", "Thank you!", "SHARING!", "Sharing is caring!", "sharing"),
 "plate": ("Rainbow Plate", "it has lots of colors of food!", "A rainbow plate has many colors.", "Red, orange, yellow, green and blue!",
           "Can you name a color on your plate?", "Why do we eat many colors?", "Each color helps our body in a different way!", "RAINBOW!", "Try a new color today!", "a rainbow plate"),
}

def lines(k, first, nxt):
    n, clue, f1, f2, do, q, a, badge, extra, warm = F[k]
    return [[f"Here's a clue: {clue} Can you guess?", "q"], [f"{nxt}: {n}!", "enter"], [f"This is {n}! Can you say {n.lower()}?", "zoom"],
            [f1, "fx+bob"], [f2, "bob"], [do, "wiggle"], [q, "fxoff+fx2off+q"], [a, f"fx2+badge:{badge}"],
            [f"Let's say it together: {n.upper()}!", "zoom"], [f"One more time, nice and loud: {n.upper()}!", "zoom"],
            [extra, "fxoff+fx2off+bob"], [f"Bye-bye, {n}!" if k not in ("handwash", "toothbrush", "water", "sleep", "share", "plate") else "Hooray! Great job!", "bob"]]

EPS = [
 ("fr_ep01_fruits", "Learn Fruits for Kids! Apple, Banana, Watermelon and More with Pip", ["apple", "banana", "orangefruit", "watermelon", "blueberry"], "five fruity friends",
  ["Apple, crunchy and sweet.", "Banana, peel it down.", "Orange, juicy slices.", "Watermelon, pink inside.", "And blueberries, tiny and blue!"]),
 ("fr_ep02_veggies", "Learn Vegetables for Kids! Carrot, Broccoli, Corn and More with Pip and Kiko", ["carrot", "broccoli", "peas", "corn", "pumpkin"], "five veggie friends",
  ["Carrot, from under the ground.", "Broccoli, like a little tree.", "Peas, in a pod.", "Corn, with yellow kernels.", "And pumpkin, big and round!"]),
 ("fr_ep03_habits", "Healthy Habits for Kids! Wash Hands, Brush Teeth and More with Pip", ["handwash", "toothbrush", "water", "sleep", "share"], "five healthy habits",
  ["Wash your hands with soap.", "Brush your teeth, morning and night.", "Drink water when you play.", "Get a good night's sleep.", "And share with your friends!"]),
 ("fr_ep04_rainbow", "Eat the Rainbow! Colorful Fruits and Veggies for Kids with Pip", ["apple", "carrot", "corn", "broccoli", "blueberry"], "a rainbow of foods",
  ["Red, like an apple.", "Orange, like a carrot.", "Yellow, like corn.", "Green, like broccoli.", "And blue, like blueberries!"]),
 ("fr_ep05_juicy", "Juicy and Crunchy Foods for Kids! Watermelon, Peas and More with Pip", ["watermelon", "peas", "banana", "pumpkin", "plate"], "five yummy surprises",
  ["Watermelon, cool and juicy.", "Peas, sweet and green.", "Banana, for energy.", "Pumpkin, on a curly vine.", "And a rainbow plate!"]),
]
ORD = ["First up", "Next", "Here comes", "Now meet", "And last"]
for eid, title, keys, what, rec in EPS:
    animals = [{"key": k, "lines": lines(k, i == 0, ORD[i])} for i, k in enumerate(keys)]
    ep = {"id": eid, "title": title,
          "intro": [["Hi, friends! I'm Pip the strawberry, and this is my buddy Kiko the broccoli!", ""], [f"Welcome to Fruity Friends! Today we're meeting {what}.", ""],
                    ["Can you count with me? One, two, three, four, five!", ""], ["Healthy food and healthy habits help us grow big and strong.", ""], ["Ready? Let's go to the kitchen!", ""]],
          "animals": animals,
          "recap": [["Yummy! Let's remember.", "@title"]] + [[r, "@" + k] for r, k in zip(rec, keys)],
          "outro": [["Which one was your favorite? Tell a grown-up, and try something new this week!", ""], ["Bye, friends! See you next time on Fruity Friends!", ""]]}
    json.dump(ep, open(f"eps/{eid}.json", "w"), indent=1, ensure_ascii=False)

SH = [("fr_apple", "apple", "What's Hiding Inside an Apple?", "#ffe9e6"), ("fr_carrot", "carrot", "Why Do Carrots Grow Underground?", "#fff1e0"),
      ("fr_handwash", "handwash", "How Long Should You Wash Your Hands?", "#e6f6ff"), ("fr_toothbrush", "toothbrush", "How Long Should You Brush Your Teeth?", "#eef7ff"),
      ("fr_watermelon", "watermelon", "Why Is Watermelon So Juicy?", "#ffeef2")]
HOOK = {"apple": "Crunchy, round, and it grows on a tree. Do you know what's inside?", "carrot": "This orange veggie plays hide and seek under the ground!",
        "handwash": "Soap, water, and lots of bubbles. How long should we scrub?", "toothbrush": "Morning and night, round and round. How long do we brush?",
        "watermelon": "Green outside, pink inside, and super juicy. Why?"}
out = []
for sid, k, t, bg in SH:
    n, clue, f1, f2, do, q, a, badge, extra, warm = F[k]
    out.append({"id": sid, "animal": k, "title": t, "thumb": badge, "top": n.upper(), "bg": [bg, "#fffdf4"], "floor": "#f6c992", "sources": SRC,
                "beats": [{"say": HOOK[k], "act": "hook"}, {"say": "Hi! I'm Pip the strawberry, and this is Kiko! Welcome to Fruity Friends!", "act": "milo_in"},
                          {"say": f"{n}! {f1}", "act": f"zoom+badge:{badge}"}, {"say": f"{q} {a}", "act": "fx+bob"},
                          {"say": do, "act": "wiggle"}, {"say": f"{extra} See you next time on Fruity Friends!", "act": "fxoff+outro"}]})
json.dump(out, open("shorts_fruity.json", "w"), indent=1, ensure_ascii=False)
print("ok")
