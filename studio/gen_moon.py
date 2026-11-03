"""Moonbeam Bedtime scripts: calm, slow, cozy. Writes shorts_moon.json + eps/mb_ep0*.json."""
import json
SRC = ["Bedtime routines for young children (AAP healthy sleep habits basics); simple nature facts"]
# key: (name, clue, fact1, fact2, calm_action, q, a, extra, goodnight)
M = {
 "mb_bunny": ("Bunny", "she has long, soft ears and a fluffy tail.", "Bunnies sleep in cozy burrows under the ground.", "They curl up in a soft, round ball.",
              "Can you wiggle your nose like a bunny? Softly, softly.", "What do bunnies love to nibble?", "Crunchy carrots and green leaves.", "Bunny is warm and snug now.", "Goodnight, Bunny."),
 "mb_bear": ("Bear", "he's big and brown, and he loves honey.", "Bears take a very long sleep in winter.", "They sleep in a cozy cave called a den.",
             "Can you give yourself a big bear hug? Squeeze gently.", "What is a bear's bed called?", "A den. A warm, quiet den.", "Bear is yawning a big, slow yawn.", "Goodnight, Bear."),
 "mb_kitten": ("Kitten", "she says meow, and she purrs when she's happy.", "Kittens sleep for most of the day.", "They curl their tail around them like a blanket.",
               "Can you purr like a kitten? Prrr, prrr.", "What does a kitten do when she's happy?", "She purrs. A soft, happy sound.", "Kitten's eyes are getting heavy.", "Goodnight, Kitten."),
 "mb_duck": ("Duckling", "he's small and yellow, and he says quack.", "Ducklings sleep close to their mommy.", "Some ducks can even sleep while they float!",
             "Can you flap your arms slowly, like little wings?", "Where do ducklings like to sleep?", "Snuggled close to their family.", "Duckling tucks his head under his wing.", "Goodnight, Duckling."),
 "mb_lamb": ("Lamb", "she's white and woolly, and she says baa.", "Lambs have soft, curly wool.", "Their wool keeps them warm all night.",
             "Let's count sleepy sheep. One, two, three, four.", "What keeps a lamb warm?", "Her soft, woolly coat.", "Lamb rests in the quiet meadow.", "Goodnight, Lamb."),
 "mb_moon": ("Moon", "it glows in the night sky, round and bright.", "The moon shines when the sun goes to sleep.", "Sometimes it's round, and sometimes it's a thin smile.",
             "Can you make a big round moon with your arms? Slowly.", "What shapes can the moon be?", "A big round circle, or a thin crescent.", "The moon watches over us all night.", "Goodnight, Moon."),
 "mb_stars": ("Stars", "they twinkle, twinkle in the dark sky.", "Stars are very, very far away.", "They twinkle like tiny lights.",
              "Can you twinkle your fingers like little stars?", "When can we see the stars?", "At night, when the sky is dark.", "Stars make pictures in the sky.", "Goodnight, Stars."),
 "mb_cloud": ("Cloud", "it's soft and white, and it floats in the sky.", "Clouds are made of tiny drops of water.", "When they get heavy, they make gentle rain.",
              "Can you float like a cloud? Sway, slowly, side to side.", "What makes rain?", "Clouds full of tiny water drops.", "Cloud drifts by, quiet and slow.", "Goodnight, Cloud."),
 "mb_firefly": ("Firefly", "it's a little bug that glows in the dark.", "Fireflies glow with a soft yellow light.", "They blink on and off, on and off.",
                "Can you blink your eyes slowly, like a firefly? Blink, blink.", "What makes a firefly special?", "Its little glowing light.", "Fireflies dance softly in the night.", "Goodnight, Firefly."),
 "mb_sunset": ("Sunset", "the sun goes down, and the sky turns orange and pink.", "At sunset, the sun says goodbye for today.", "The sky turns orange, pink, and purple.",
               "Can you stretch up high, then slowly come down, like the sun?", "What colors are in a sunset?", "Orange, pink, and purple.", "Soon it will be night time.", "Goodnight, Sun."),
 "mb_bath": ("Bath Time", "there's warm water and lots of bubbles.", "A warm bath helps our body relax.", "Wash, wash, and rinse, rinse.",
             "Can you pretend to pop the bubbles? Pop, pop, gently.", "What helps us feel calm before bed?", "A warm, cozy bath.", "Now we're clean and sleepy.", "Bye-bye, bubbles."),
 "mb_pajamas": ("Pajamas", "they're soft and comfy, and we wear them to bed.", "Pajamas are soft and comfy.", "These ones have little stars on them!",
                "Can you pretend to put your arms in your pajama sleeves?", "When do we wear pajamas?", "At bedtime.", "Cozy pajamas, ready for sleep.", "All snug in pajamas."),
 "mb_book": ("Story Time", "it has pages, pictures, and words.", "A bedtime story helps us feel calm.", "We can read it with someone we love.",
             "Can you pretend to turn a page? Slowly.", "Who can read you a story?", "A grown-up who loves you.", "The story is almost done.", "The end, sweet dreams."),
 "mb_teddy": ("Teddy", "he's soft and cuddly, and he loves hugs.", "A teddy bear is a cozy bedtime friend.", "Teddy keeps you company all night.",
              "Can you give your teddy, or a pillow, a gentle hug?", "What does teddy love most?", "Soft, gentle hugs.", "Teddy is snuggled in tight.", "Goodnight, Teddy."),
 "mb_nightlight": ("Night Light", "it glows softly in the dark room.", "A night light glows soft and warm.", "It helps our room feel cozy.",
                   "Can you take a slow breath in, and a slow breath out?", "What does a night light do?", "It glows softly while we sleep.", "The room is calm and quiet.", "Glow softly, Night Light."),
 "mb_whale": ("Whale", "it's very big, it lives in the sea, and it sings.", "Whales are the biggest animals in the ocean.", "Some whales sing long, gentle songs.",
              "Can you hum a soft whale song? Mmmmm.", "Where do whales live?", "In the big, blue ocean.", "Whale floats in the calm, deep sea.", "Goodnight, Whale."),
 "mb_seahorse": ("Seahorse", "it has a curly tail and swims standing up.", "Seahorses hold onto seaweed with their tails.", "That way they don't float away while they rest.",
                 "Can you curl your hand like a seahorse tail?", "What does a seahorse hold on to?", "Seaweed, with its curly tail.", "Seahorse sways with the gentle waves.", "Goodnight, Seahorse."),
 "mb_fish": ("Fish", "it has fins and a tail, and it swims and swims.", "Fish rest in the water, very still.", "Some fish rest near rocks and plants.",
             "Can you swim your hands slowly, like a fish?", "How do fish move?", "With their fins and tails.", "Fish are resting in the quiet water.", "Goodnight, Fish."),
 "mb_turtle": ("Sea Turtle", "it has a shell on its back and swims in the sea.", "Sea turtles carry their shell everywhere.", "They glide slowly through the water.",
               "Can you move slowly, slowly, like a turtle?", "What does a turtle carry on its back?", "Its shell.", "Turtle rests on the soft, sandy bottom.", "Goodnight, Turtle."),
 "mb_jelly": ("Jellyfish", "it's soft and wiggly, with long, wavy tentacles.", "Jellyfish float gently in the sea.", "Some jellyfish even glow in the dark!",
              "Can you float your arms like wavy tentacles?", "How do jellyfish move?", "They float and drift with the water.", "Jellyfish glows softly in the deep.", "Goodnight, Jellyfish."),
 "mb_cow": ("Cow", "she says moo, and she lives on the farm.", "Cows can sleep lying down in the soft grass.", "They rest in the barn at night.",
            "Can you say a sleepy moo? Moooo.", "What does a cow say?", "Moo!", "Cow is lying down in the hay.", "Goodnight, Cow."),
 "mb_pig": ("Pig", "he's pink, and he says oink.", "Pigs like to sleep snuggled close together.", "They make soft, snorty sounds.",
            "Can you say a quiet oink? Oink, oink.", "How do pigs like to sleep?", "Snuggled close together.", "Pig is snoring softly.", "Goodnight, Pig."),
 "mb_horse": ("Horse", "he has a long mane, and he says neigh.", "Horses can sleep standing up!", "They also lie down for a deep sleep.",
              "Can you gently gallop your fingers on your lap?", "How can horses sleep?", "Standing up, or lying down.", "Horse rests in his cozy stall.", "Goodnight, Horse."),
 "mb_hen": ("Hen", "she says cluck, and she sits on eggs.", "Hens sleep up high on a perch.", "They keep their eggs warm and safe.",
            "Can you tuck your arms in like a hen on her nest?", "Where do hens sleep?", "Up high on a perch.", "Hen fluffs her feathers and settles in.", "Goodnight, Hen."),
 "mb_puppy": ("Puppy", "he wags his tail, and he says woof.", "Puppies need lots and lots of sleep.", "Sleep helps them grow big and strong.",
              "Can you wag your hand like a happy puppy tail?", "Why do puppies sleep so much?", "Sleep helps them grow.", "Puppy curls up in his little bed.", "Goodnight, Puppy."),
}

def lines(k, lead):
    n, clue, f1, f2, do, q, a, extra, gn = M[k]
    return [[f"Here's a little clue: {clue} Who could it be?", "q"], [f"{lead}: {n}.", "enter"], [f"This is {n}. Can you whisper {n.lower()}?", "zoom"],
            [f1, "fx+bob"], [f2, "bob"], [do, "bob"], [q, "fxoff+fx2off+q"], [a, f"fx2+badge:{n.upper()}"],
            [f"Let's say it softly together: {n}.", "zoom"], [f"One more time, very quietly: {n}.", "zoom"], [extra, "fxoff+fx2off+bob"], [gn, "bob"]]

EPS = [
 ("mb_ep01_goodnight", "Goodnight Animals 🌙 Calm Bedtime Story for Kids with Luna the Owl", ["mb_bunny", "mb_bear", "mb_kitten", "mb_duck", "mb_lamb"], "five sleepy animal friends", "Goodnight, Bunny, Bear, Kitten, Duckling, and Lamb."),
 ("mb_ep02_nightsky", "Goodnight Moon and Stars 🌙 Calm Night Sky Bedtime Story with Luna", ["mb_sunset", "mb_moon", "mb_stars", "mb_cloud", "mb_firefly"], "the quiet night sky", "Goodnight, Sun, Moon, Stars, Cloud, and Firefly."),
 ("mb_ep03_routine", "My Bedtime Routine 🛁 Bath, Pajamas, Story and Sleep with Luna", ["mb_bath", "mb_pajamas", "mb_book", "mb_teddy", "mb_nightlight"], "our cozy bedtime routine", "Bath, pajamas, story, teddy, and a soft night light."),
 ("mb_ep04_ocean", "Ocean Dreams 🐋 Calm Bedtime Story with Sea Animals and Luna", ["mb_whale", "mb_seahorse", "mb_fish", "mb_turtle", "mb_jelly"], "sleepy friends under the sea", "Goodnight, Whale, Seahorse, Fish, Turtle, and Jellyfish."),
 ("mb_ep05_farm", "Goodnight Farm 🐄 Calm Bedtime Story with Farm Animals and Luna", ["mb_cow", "mb_pig", "mb_horse", "mb_hen", "mb_puppy"], "the sleepy farm friends", "Goodnight, Cow, Pig, Horse, Hen, and Puppy."),
]
LEAD = ["First, let's meet", "Next, here is", "Now, let's visit", "Look, it's", "And last, here is"]
for eid, title, keys, what, final in EPS:
    ep = {"id": eid, "title": title,
          "intro": [["Hello, little one. I'm Luna, the sleepy owl. Welcome to Moonbeam Bedtime.", ""], [f"Tonight, we'll say goodnight to {what}.", ""],
                    ["Let's take a slow, deep breath together. In, and out.", ""], ["Get cozy, snuggle in, and listen softly.", ""], ["Are you ready? Let's begin.", ""]],
          "animals": [{"key": k, "lines": lines(k, LEAD[i])} for i, k in enumerate(keys)],
          "recap": [["Let's remember all our friends.", "@title"]] + [[M[k][8], "@" + k] for k in keys],
          "outro": [[f"{final} Now close your eyes, and dream sweet dreams.", ""], ["Goodnight, little one. Luna loves you. Sleep tight.", ""]]}
    json.dump(ep, open(f"eps/{eid}.json", "w"), indent=1, ensure_ascii=False)

SH = [("mb_s_bunny", "mb_bunny", "How Do Bunnies Sleep? 🌙", "Shh. Can you guess who's getting ready for bed?"),
      ("mb_s_moon", "mb_moon", "Why Does the Moon Change Shape? 🌙", "Look up! Something round and bright is glowing tonight."),
      ("mb_s_bath", "mb_bath", "Why Take a Bath Before Bed? 🛁", "Warm water, soft bubbles. It's almost bedtime."),
      ("mb_s_whale", "mb_whale", "Do Whales Really Sing? 🐋", "Listen. A gentle song is coming from the deep blue sea."),
      ("mb_s_lamb", "mb_lamb", "Let's Count Sleepy Sheep 🐑", "One, two, three. Let's count sleepy sheep together.")]
out = []
for sid, k, t, hook in SH:
    n, clue, f1, f2, do, q, a, extra, gn = M[k]
    out.append({"id": sid, "animal": k, "title": t, "thumb": n.upper(), "top": n.upper(), "bg": ["#1d2456", "#3a3f86"], "floor": "#232a5c", "sources": SRC,
                "beats": [{"say": hook, "act": "hook"}, {"say": "Hello, little one. I'm Luna, the sleepy owl.", "act": "milo_in"},
                          {"say": f"It's {n}. {f1}", "act": f"zoom+badge:{n.upper()}"}, {"say": f"{q} {a}", "act": "fx+bob"},
                          {"say": do, "act": "bob"}, {"say": f"{gn} Sweet dreams, from Moonbeam Bedtime.", "act": "fxoff+outro"}]})
json.dump(out, open("shorts_moon.json", "w"), indent=1, ensure_ascii=False)
print("ok")
