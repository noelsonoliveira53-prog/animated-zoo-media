"""Moonbeam Bedtime week 2: writes shorts_moon2.json, eps/mb_ep06..11, upload_plan_moon2.json, brand/moon/thumb_mb_ep06..11.html.
Calm, slow, cozy, no peril. Same formats as gen_moon.py / mkplan.py."""
import json, re, os
from art_moon2 import SCENES_MOON2 as S, NAMES_MOON2
from art_moon import LUNA as HOST
SRC = ["Bedtime routines for young children (AAP healthy sleep habits basics); simple nature facts (National Geographic Kids, Smithsonian's National Zoo animal fact pages)"]
SRC_TOY = ["Bedtime routines for young children (AAP healthy sleep habits basics); tidy-up and wind-down habits for preschoolers"]

# key: (name, clue, fact1, fact2, calm_action, q, a, extra, goodnight)
M = {
 # goodnight forest
 "mb2_deer": ("Deer", "she has long legs, big soft ears, and little white spots on her back.", "A baby deer is called a fawn, and she has soft white spots.", "Her spots help her rest quietly in the tall, shady grass.",
              "Can you make big deer ears with your hands, and listen very quietly?", "What do we call a baby deer?", "A fawn. A sweet, spotted little fawn.", "Fawn folds her long legs and lies down in the soft, cool grass.", "Goodnight, Deer. Sleep softly."),
 "mb2_fox": ("Fox", "he's orange, with pointy ears and a big, bushy tail.", "Foxes have big, fluffy tails, as soft as a scarf.", "When it's chilly, a fox curls up and wraps his tail around him like a warm blanket.",
             "Can you wrap your arms around yourself, like a cozy fox tail? Mmm, so warm.", "What does a fox use like a blanket?", "His big, bushy tail. Soft and warm.", "Fox tucks his nose under his tail and lets out a slow, sleepy sigh.", "Goodnight, Fox. Stay warm."),
 "mb2_hedgehog": ("Hedgehog", "she's small and round, and her back is covered in little spikes.", "The little spikes on a hedgehog's back are called spines.", "To feel cozy, a hedgehog can curl up into a round, spiky ball.",
                  "Can you curl up small like a hedgehog? Tuck in your chin, and breathe slowly.", "What are a hedgehog's spikes called?", "Spines. Lots and lots of little spines.", "Hedgehog snuggles into her soft nest of crunchy leaves.", "Goodnight, Hedgehog. Sleep tight."),
 "mb2_squirrel": ("Squirrel", "he has a big curly tail, and he loves to collect nuts.", "Squirrels hide nuts in the ground, so they have snacks for winter.", "They sleep in round, leafy nests high up in the trees.",
                  "Can you pretend to hold a little acorn, and hug it gently?", "Where does a squirrel sleep?", "In a leafy nest, high up in a tree.", "Squirrel curls his fluffy tail over his head like a cozy hat.", "Goodnight, Squirrel. Sweet dreams."),
 "mb2_raccoon": ("Raccoon", "she has a dark mask around her eyes and stripes on her tail.", "Raccoons have a mask of dark fur around their eyes.", "Their little front paws can feel things very, very well.",
                 "Can you wiggle your fingers softly, like little raccoon paws?", "Where is the raccoon's mask?", "Around her eyes. A soft, furry mask.", "Raccoon likes the quiet night, so she waves a gentle hello to the moon.", "Goodnight, Raccoon. Rest well."),
 # snowy dreams
 "mb2_penguin": ("Penguin", "he's black and white, and he waddles on the ice.", "Penguins live far, far away in the south, where it's icy and cold.", "To stay warm, penguins huddle close together, side by side.",
                 "Can you waddle your shoulders slowly, side to side, like a penguin?", "How do penguins stay warm?", "They huddle close together, like a big cozy hug.", "Penguin snuggles in close with all his penguin friends.", "Goodnight, Penguin. Stay snug."),
 "mb2_polarbear": ("Polar Bear", "she's big and white, and she lives where it snows.", "Polar bears live far up north, where there's lots of snow and ice.", "Baby polar bears are called cubs, and they're born in a cozy den of snow.",
                   "Can you give yourself a big, soft polar bear hug? Squeeze gently.", "What is a baby polar bear called?", "A cub. A fluffy little cub.", "Polar Bear Cub curls up close to Mama in their quiet, snowy den.", "Goodnight, Polar Bear. Sleep warm."),
 "mb2_seal": ("Seal", "he has flippers and whiskers, and he loves to swim.", "Seals have a thick layer of fat called blubber.", "Blubber keeps them warm, even in the icy cold water.",
              "Can you clap your hands softly, like little seal flippers? Clap, clap.", "What keeps a seal warm?", "A thick, cozy layer of blubber.", "Seal stretches out on the smooth ice and closes his eyes.", "Goodnight, Seal. Rest easy."),
 "mb2_snowyowl": ("Snowy Owl", "she's white like snow, with big yellow eyes.", "Snowy owls have white feathers that match the snow.", "They even have fluffy feathers on their feet, like warm slippers!",
                  "Can you wiggle your toes, like you're wearing fluffy owl slippers?", "What does a snowy owl have on her feet?", "Fluffy feathers, like cozy slippers.", "Snowy Owl fluffs up her feathers and blinks slowly, slowly.", "Goodnight, Snowy Owl. Hoo, hoo."),
 "mb2_beluga": ("Beluga Whale", "it's a white whale, with a round head and a gentle smile.", "Beluga whales are white, and they live in cold northern seas.", "Belugas make lots of soft sounds, like chirps, clicks, and whistles.",
                "Can you make a soft little whistle, like a beluga? Whoo, whoo.", "What color is a beluga whale?", "White. White like snow.", "Beluga floats under the shimmering ice, calm and slow.", "Goodnight, Beluga. Float softly."),
 # garden at night
 "mb2_snail": ("Snail", "she moves very slowly, and she carries a shell on her back.", "A snail carries her shell everywhere. It's her own little house.", "Snails like to come out at night, when the garden is cool and damp.",
               "Can you move your hand very, very slowly, like a snail? Slow, slow, slow.", "What does a snail carry on her back?", "Her shell. Her own little house.", "Snail leaves a shiny, silver trail as she glides through the garden.", "Goodnight, Snail. Slow and sleepy."),
 "mb2_moth": ("Moth", "it has soft, fuzzy wings, and it flutters at night.", "Most moths flutter around at night, while we're asleep.", "Moths have feathery antennae that help them smell sweet flowers.",
              "Can you flutter your hands softly, like little moth wings?", "When do most moths fly?", "At night, under the moon and stars.", "Moth flutters slowly past the glowing moon.", "Goodnight, Moth. Flutter softly."),
 "mb2_frog": ("Frog", "he's green, he hops, and he says ribbit.", "Many frogs sing at night, to say hello to each other.", "Frogs have long, sticky tongues for catching tiny bugs.",
              "Can you sing a very quiet ribbit? Ribbit, ribbit.", "When do many frogs sing?", "At night. Ribbit, ribbit, in the dark.", "Frog sits on his lily pad, and his song gets softer and softer.", "Goodnight, Frog. Ribbit."),
 "mb2_ladybug": ("Ladybug", "she's red, with little black spots.", "Ladybugs have wings hiding under their red, spotty shell.", "In winter, lots of ladybugs snuggle together to stay warm.",
                 "Can you count her spots with me? One, two, three, four, five, six.", "Where are a ladybug's wings?", "Hiding under her red, spotty shell.", "Ladybug tucks in her wings and rests on a soft green leaf.", "Goodnight, Ladybug. Sweet dreams."),
 "mb2_tulip": ("Tulip", "it's pink, it grows in the garden, and it has soft petals.", "Some flowers, like tulips, close their petals at night.", "In the morning, when the sun comes up, they open again.",
               "Can you close your hands slowly, like a flower closing its petals?", "What do tulips do at night?", "They close their petals, like they're going to sleep.", "Tulip folds her petals and sways softly in the breeze.", "Goodnight, Tulip. See you in the morning."),
 # toys go to sleep
 "mb2_blocks": ("Blocks", "they're square, colorful, and they stack up tall.", "Blocks stack up, one on top of another.", "A wide block at the bottom helps the tower stand up tall.",
                "Can you stack your fists, one on top of the other, slowly?", "What do blocks like to do?", "Stack up, one on top of another.", "Now the blocks go back in their box, all in a neat little pile.", "Goodnight, Blocks. Stack and sleep."),
 "mb2_doll": ("Rag Doll", "she's soft and floppy, with curly yarn hair.", "A rag doll is made of soft cloth, and she's very cuddly.", "Her floppy arms are just right for gentle hugs.",
              "Can you let your arms go soft and floppy, like a rag doll? So relaxed.", "What is a rag doll made of?", "Soft cloth. Soft and cuddly.", "Rag Doll lies down on her little pillow, all floppy and calm.", "Goodnight, Rag Doll. Rest your head."),
 "mb2_rockhorse": ("Rocking Horse", "it's a wooden horse that rocks back and forth.", "A rocking horse sits on two curved rockers.", "The curved rockers let it rock gently, back and forth.",
                   "Can you rock your body gently, back and forth, back and forth?", "How does a rocking horse move?", "Back and forth, back and forth, gently.", "Rocking Horse slows down, and down, until it's still and quiet.", "Goodnight, Rocking Horse. Rock softly."),
 "mb2_boat": ("Toy Boat", "it has a sail, and it floats on the water.", "Boats float on top of the water.", "The sail catches the wind to help the boat move along.",
              "Can you blow a slow, gentle breath, like a breeze for the little sail?", "What helps a sailboat move?", "The wind, blowing on its sail.", "Toy Boat drifts to the edge of the tub, ready to rest.", "Goodnight, Toy Boat. Float softly."),
 "mb2_toybox": ("Toy Box", "it's a big box where all the toys go at night.", "When we put our toys away, they're easy to find tomorrow.", "Ball, teddy, blocks, all tucked in, safe and sound.",
                "Can you pretend to put a toy away, gently, in the box?", "Where do the toys sleep at night?", "In the toy box, all tucked in.", "The lid closes softly. The playroom is tidy and quiet.", "Goodnight, Toy Box. Goodnight, toys."),
 # rainy night lullaby
 "mb2_raindrop": ("Raindrop", "it's a tiny drop of water that falls from the clouds.", "Raindrops fall from clouds when the clouds get full of water.", "Rain gives water to the trees, the grass, and the flowers.",
                  "Can you tap your fingers softly, like rain? Pitter, patter, pitter, patter.", "Who drinks up the rain?", "The trees, the grass, and the flowers.", "Raindrop lands softly in the garden, and a flower says thank you.", "Goodnight, Raindrop. Pitter, patter."),
 "mb2_window": ("Rainy Window", "it's where we can watch the rain, all warm and dry inside.", "Rain on the window makes a soft, tapping sound.", "Little drops slide down the glass, slowly, slowly.",
                "Can you trace a raindrop sliding down, with one finger, very slowly?", "What sound does rain make on the window?", "Tap, tap, tap. A soft, cozy sound.", "Kitty watches the drops from the windowsill, warm and dry.", "Goodnight, Rainy Window. Tap, tap."),
 "mb2_umbrella": ("Umbrella", "it opens up wide, and it keeps us dry in the rain.", "An umbrella opens up wide over our heads.", "The rain rolls off the top, and we stay nice and dry underneath.",
                  "Can you make a big umbrella with your arms, high over your head?", "What does an umbrella do?", "It keeps us dry when it rains.", "Umbrella closes up, and rests by the door for tomorrow.", "Goodnight, Umbrella. All done for today."),
 "mb2_worm": ("Earthworm", "it's long and wiggly, and it lives in the soil.", "Earthworms come up out of the soil on rainy nights, when the ground is wet.", "Worms help the soil stay soft, so plants can grow.",
              "Can you wiggle your fingers slowly, like a little worm? Wiggle, wiggle.", "How do worms help the garden?", "They keep the soil soft, so plants can grow.", "Earthworm wiggles back down into the soft, cool soil.", "Goodnight, Earthworm. Wiggle softly."),
 "mb2_moonbow": ("Moonbow", "it's like a rainbow, but it shines at night.", "Sometimes, after rain, the bright moon can make a rainbow at night.", "It's called a moonbow, and it looks soft and pale.",
                 "Can you draw a big, slow arch in the air with your hand?", "What do we call a rainbow at night?", "A moonbow. A soft, sleepy rainbow.", "The rain stops, and the moonbow glows softly over the hills.", "Goodnight, Moonbow. Glow gently."),
 # sleepy train to dreamland
 "mb2_engine": ("Dream Train", "it has big wheels, and it chugs along the tracks.", "Trains roll along on long metal tracks.", "The engine is at the front, and it pulls all the train cars behind it.",
                "Can you move your arms in slow circles, like train wheels? Round and round.", "What does the engine do?", "It pulls the train cars along the tracks.", "The Dream Train chugs slowly through the starry night.", "Goodnight, Dream Train. Chug softly."),
 "mb2_sleepcar": ("Sleeping Car", "it's a train car with little beds inside.", "Some real trains have sleeping cars with tiny beds.", "People can sleep in their beds while the train rolls through the night.",
                  "Can you rest your head on your hands, like a little pillow?", "What is inside a sleeping car?", "Little beds, for sleeping on the train.", "Bunny, Bear, and Lamb are tucked in, rocking gently with the train.", "Goodnight, Sleeping Car. Sleep tight."),
 "mb2_bridge": ("Bridge", "it goes up and over the river, so the train can cross.", "A bridge helps the train cross over the river.", "Under the bridge, the water flows slowly and shines in the moonlight.",
                "Can you make a bridge with your arms, and hold it, nice and still?", "How does the train cross the river?", "Over the bridge, nice and slow.", "The train glides softly over the bridge, under the moon.", "Goodnight, Bridge. Goodnight, river."),
 "mb2_caboose": ("Caboose", "it's the little car at the very end of the train.", "On many old trains, the last car was called the caboose.", "Railroad workers rode inside, and kept a lantern glowing at the back.",
                 "Can you wave a soft goodbye, like the caboose at the end of the train?", "Which car is the caboose?", "The little car at the very end.", "The caboose's little lantern glows warm and yellow in the dark.", "Goodnight, Caboose. Glow softly."),
 "mb2_station": ("Station", "it's the place where the train stops, so everyone can get off.", "A train station is where the train stops.", "People get on and off there, and wait on the platform.",
                 "Can you take one big, slow breath, as the train comes to a stop? Ahhh.", "What happens at the station?", "The train stops, and everyone can get off.", "We've arrived at Dreamland Station. Everything is quiet and calm.", "Goodnight, Station. We're home."),
}
LEAD = ["First, let's meet", "Next, here is", "Now, let's visit", "Look, it's", "And last, here is"]

def lines(k, lead):
    n, clue, f1, f2, do, q, a, extra, gn = M[k]
    return [[f"Here's a little clue: {clue} Who could it be?", "q"], [f"{lead}: {n}.", "enter"], [f"This is {n}. Can you whisper {n.lower()}? Nice and soft.", "zoom"],
            [f1, "fx+bob"], [f2, "bob"], [do, "bob"], [q, "fxoff+fx2off+q"], [a, f"fx2+badge:{n.upper()}"],
            [f"Let's say it softly together: {n}.", "zoom"], [f"One more time, very quietly, like a little whisper: {n}.", "zoom"], [extra, "fxoff+fx2off+bob"], [gn, "bob"]]

# (id, title, keys, tonight-what, final line, thumb words, date)
EPS = [
 ("mb_ep06_forest", "Goodnight Forest 🦔 Calm Bedtime Story with Luna the Owl", ["mb2_deer", "mb2_fox", "mb2_hedgehog", "mb2_squirrel", "mb2_raccoon"],
  "the sleepy friends of the forest", "Goodnight, Deer, Fox, Hedgehog, Squirrel, and Raccoon.", ("GOODNIGHT", "FOREST"), "2026-11-12"),
 ("mb_ep07_snowy", "Snowy Dreams 🐧 Calm Bedtime Story with Polar Animals", ["mb2_penguin", "mb2_polarbear", "mb2_seal", "mb2_snowyowl", "mb2_beluga"],
  "snowy friends from the coldest places on Earth", "Goodnight, Penguin, Polar Bear, Seal, Snowy Owl, and Beluga.", ("SNOWY", "DREAMS"), "2026-11-13"),
 ("mb_ep08_garden", "The Garden at Night 🐌 Calm Bedtime Story with Luna", ["mb2_snail", "mb2_moth", "mb2_frog", "mb2_ladybug", "mb2_tulip"],
  "the quiet garden at night", "Goodnight, Snail, Moth, Frog, Ladybug, and Tulip.", ("GARDEN", "AT NIGHT"), "2026-11-14"),
 ("mb_ep09_toys", "Toys Go to Sleep 🧸 Cozy Tidy-Up Bedtime Story with Luna", ["mb2_blocks", "mb2_doll", "mb2_rockhorse", "mb2_boat", "mb2_toybox"],
  "the toys in our playroom", "Goodnight, Blocks, Rag Doll, Rocking Horse, Toy Boat, and Toy Box.", ("TOYS GO", "TO SLEEP"), "2026-11-15"),
 ("mb_ep10_rainy", "Rainy Night Lullaby 🌧️ Calm Bedtime Story with Luna", ["mb2_raindrop", "mb2_window", "mb2_umbrella", "mb2_worm", "mb2_moonbow"],
  "a soft and gentle rainy night", "Goodnight, Raindrop, Window, Umbrella, Earthworm, and Moonbow.", ("RAINY", "NIGHT"), "2026-11-16"),
 ("mb_ep11_train", "The Sleepy Train to Dreamland 🚂 Calm Bedtime Story", ["mb2_engine", "mb2_sleepcar", "mb2_bridge", "mb2_caboose", "mb2_station"],
  "the sleepy train, all the way to Dreamland", "Goodnight, Dream Train, Sleeping Car, Bridge, Caboose, and Station.", ("DREAM", "TRAIN"), "2026-11-17"),
]
for eid, title, keys, what, final, _, _ in EPS:
    ep = {"id": eid, "title": title,
          "intro": [["Hello, little one. I'm Luna, the sleepy owl. Welcome back to Moonbeam Bedtime.", ""], [f"Tonight, we'll say goodnight to {what}.", ""],
                    ["First, let's take a slow, deep breath together. Breathe in, and breathe out.", ""], ["Get cozy, snuggle in under your blanket, and listen softly.", ""], ["Are you ready? Let's begin our story.", ""]],
          "animals": [{"key": k, "lines": lines(k, LEAD[i])} for i, k in enumerate(keys)],
          "recap": [["Let's remember all of our sleepy friends.", "@title"]] + [[M[k][8], "@" + k] for k in keys],
          "outro": [[f"{final} Now close your eyes, and dream sweet, gentle dreams.", ""], ["Goodnight, little one. Luna loves you. Sleep tight.", ""]]}
    json.dump(ep, open(f"eps/{eid}.json", "w"), indent=1, ensure_ascii=False)

# ---------- Shorts: (id, scene, title, thumb word, date, time, [hook, luna, fact, q+a, calm action, goodnight]) ----------
A, B = "9:00 AM", "5:00 PM"
SH = [
 ("mb2_s_hedgehog", "mb2_hedgehog", "Why Do Hedgehogs Curl Up? 🦔", "HEDGEHOG", "2026-11-09", A,
  ["Shh. Someone small and spiky is getting ready for bed. Who could it be?",
   "Hello, little one. I'm Luna, the sleepy owl. Let's say goodnight to a gentle forest friend. Get cozy, and listen softly.",
   "It's Hedgehog. Her back is covered in little spikes called spines. To feel snug and cozy, she curls up into a round, spiky ball.",
   "Where does a hedgehog sleep? In a soft nest of leaves and grass, all tucked in and warm.",
   "Can you curl up small like a hedgehog? Tuck in your chin, hug your knees, and breathe in slowly, and out.",
   "Goodnight, Hedgehog. Sleep tight in your leafy nest. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_penguin", "mb2_penguin", "How Do Penguins Stay Warm? 🐧", "PENGUIN", "2026-11-10", A,
  ["Brr. It's icy and snowy tonight. Who's waddling off to bed?",
   "Hello, little one. I'm Luna, the sleepy owl. Let's visit a snowy friend far, far away. Get cozy, and listen softly.",
   "It's Penguin. Penguins live way down south, where it's very icy and cold. Their thick feathers keep them warm and dry. They waddle slowly along on the ice.",
   "How do penguins stay warm at night? They huddle close together, side by side, like one big cozy hug.",
   "Can you give yourself a gentle penguin hug? Squeeze softly, and sway slowly, side to side.",
   "Goodnight, Penguin. Snuggle close with your friends. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_countstars", "mb2_countstars", "Let's Count the Stars Together ⭐", "STARS", "2026-11-11", A,
  ["Look up, little one. The sky is full of twinkling stars tonight.",
   "Hello, little one. I'm Luna, the sleepy owl. Shall we count some sleepy stars together? Get cozy, and listen softly.",
   "Stars are giant, glowing suns, very, very far away. They're so far, they look like tiny twinkling lights. They shine all night long, even while we sleep.",
   "Let's count them slowly. One star. Two stars. Three stars. Four stars. And five little stars.",
   "Now twinkle your fingers softly, like the stars. Twinkle, twinkle, slower, and slower, and slower.",
   "Goodnight, stars. Thank you for shining. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_snail", "mb2_snail", "Where Does a Snail Sleep? 🐌", "SNAIL", "2026-11-11", B,
  ["Slowly, slowly, someone is gliding through the garden. Can you guess who?",
   "Hello, little one. I'm Luna, the sleepy owl. Let's peek into the quiet garden tonight. Get cozy, and listen softly.",
   "It's Snail. A snail carries her shell everywhere she goes. It's her very own little house, right on her back.",
   "Where does a snail sleep? She tucks herself inside her shell, all cozy and snug.",
   "Can you move your hand very, very slowly, like a snail? Slow, slow, slow. Now rest your hand, nice and still.",
   "Goodnight, Snail. Rest in your little shell house. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_balloon", "mb2_balloon", "Balloon Breathing Before Bed 🎈", "BREATHE", "2026-11-12", A,
  ["Let's get our bodies calm and sleepy with a gentle breathing game.",
   "Hello, little one. I'm Luna, the sleepy owl. Tonight, let's breathe like a soft balloon. Get cozy, and listen softly.",
   "Put your hands on your tummy. Slow breathing helps our bodies feel calm and ready for sleep.",
   "Breathe in slowly through your nose, and fill your tummy up like a big round balloon. Hold it, one, two.",
   "Now let the air out slowly, slowly, like a balloon floating gently down. Let's do it once more. In, and out.",
   "Your body is calm and cozy now. Goodnight, little balloon. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_snowyowl", "mb2_snowyowl", "Why Is the Snowy Owl White? 🦉", "SNOWY OWL", "2026-11-12", B,
  ["Hoo, hoo. A white, fluffy friend is perched in the snow tonight. Who is it?",
   "Hello, little one. I'm Luna, the sleepy owl. Let's meet one of my owl cousins. Get cozy, and listen softly.",
   "It's Snowy Owl. She has soft white feathers that match the snow all around her. She lives far up north, where it's cold. Her round yellow eyes blink slowly, slowly.",
   "What does Snowy Owl have on her feet? Fluffy feathers, like warm, cozy slippers.",
   "Can you wiggle your toes, like you're wearing fluffy owl slippers? Wiggle, wiggle, and then rest.",
   "Goodnight, Snowy Owl. Hoo, hoo. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_fox", "mb2_fox", "How Does a Fox Stay Cozy? 🦊", "FOX", "2026-11-13", A,
  ["Shh. Someone with a big, bushy tail is getting sleepy in the forest.",
   "Hello, little one. I'm Luna, the sleepy owl. Let's tiptoe into the quiet forest. Get cozy, and listen softly.",
   "It's Fox. Foxes have big, fluffy tails, as soft as a scarf. On chilly nights, a fox curls up and wraps his tail around him.",
   "What does a fox use like a blanket? His bushy tail. Soft, fluffy, and warm.",
   "Can you wrap your arms around yourself, like a cozy fox tail? Mmm. Now take a slow, sleepy breath.",
   "Goodnight, Fox. Stay warm and snug. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_rain", "mb2_window", "A Cozy Rainy Night Lullaby 🌧️", "RAIN", "2026-11-13", B,
  ["Listen. Tap, tap, tap. Can you hear the rain on the window?",
   "Hello, little one. I'm Luna, the sleepy owl. Let's watch the rain, all warm and dry inside. Get cozy, and listen softly.",
   "Rain falls from clouds when they get full of tiny drops of water. The rain gives a drink to the trees, the grass, and the flowers.",
   "What sound does rain make on the window? Pitter, patter, tap, tap. A soft and cozy sound.",
   "Can you tap your fingers softly, like rain? Pitter, patter, slower and slower, until it's quiet.",
   "Goodnight, rain. Goodnight, cozy window. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_frog", "mb2_frog", "Why Do Frogs Sing at Night? 🐸", "FROG", "2026-11-14", A,
  ["Ribbit, ribbit. Who's singing a soft song in the garden tonight?",
   "Hello, little one. I'm Luna, the sleepy owl. Let's listen by the little pond. Get cozy, and listen softly.",
   "It's Frog. Many frogs sing at night. Their songs are how they say hello to each other in the dark. Frogs have long, sticky tongues, too.",
   "Where does Frog like to sit? On a big, round lily pad, floating on the quiet pond. The water is calm and still.",
   "Can you sing a very quiet ribbit with me? Ribbit. Ribbit. Now even softer, like a whisper. Ribbit.",
   "Goodnight, Frog. Sing softly. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_train", "mb2_engine", "All Aboard the Sleepy Dream Train 🚂", "TRAIN", "2026-11-14", B,
  ["All aboard, little one. The sleepy Dream Train is ready to go.",
   "Hello, little one. I'm Luna, the sleepy owl. Let's take a gentle ride to Dreamland. Get cozy, and listen softly.",
   "This is the Dream Train. Trains roll along on long metal tracks. The engine at the front pulls all the cars behind it.",
   "Some real trains even have sleeping cars, with tiny beds, so people can sleep while the train rolls through the night.",
   "Can you move your arms in slow circles, like train wheels? Round and round, slower, and slower.",
   "Next stop, Dreamland. Goodnight, Dream Train. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_starfish", "mb2_starfish", "Starfish Stretch Before Bed ⭐", "STRETCH", "2026-11-15", A,
  ["Let's do a slow, sleepy stretch, just like a starfish on the sand.",
   "Hello, little one. I'm Luna, the sleepy owl. Let's stretch our bodies before bed. Get cozy, and listen softly.",
   "This is Starfish. Most starfish have five arms, and they move very slowly on tiny tube feet. Let's be starfish together.",
   "Lie down or stand tall, and stretch out your arms and legs, wide like a star. Hold it, and breathe in.",
   "Now let everything go soft and floppy. Breathe out slowly. Let's stretch wide once more, and relax.",
   "Your body feels calm and sleepy. Goodnight, Starfish. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_moth", "mb2_moth", "Who Flutters at Night? The Moth 🌙", "MOTH", "2026-11-15", B,
  ["Flutter, flutter. Someone soft and fuzzy is flying under the moon.",
   "Hello, little one. I'm Luna, the sleepy owl. Let's meet a gentle night flier. Get cozy, and listen softly.",
   "It's Moth. Most moths flutter around at night, while we're asleep. Their wings are soft and a little bit fuzzy. In the daytime, many moths rest quietly on tree bark.",
   "What helps a moth find flowers? Its feathery antennae help it smell sweet flowers in the dark.",
   "Can you flutter your hands softly, like little moth wings? Flutter, flutter, then rest them on your lap.",
   "Goodnight, Moth. Flutter softly. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_fort", "mb2_fort", "A Cozy Weekend Blanket Fort 🧸", "COZY", "2026-11-16", A,
  ["Shh. Something soft and cozy is waiting in the living room. Let's take a peek.",
   "Hello, little one. I'm Luna, the sleepy owl. It's the weekend, and we have time to slow down. Get cozy, and listen softly.",
   "It's a blanket fort. With a grown-up's help, we can drape a big blanket over chairs to make a cozy little hideaway.",
   "What goes inside a blanket fort? Soft pillows, a favorite teddy, and a quiet story with someone you love.",
   "Can you pretend to fluff a pillow, and snuggle in? Breathe in slowly, and breathe out. So cozy.",
   "Goodnight, cozy fort. Happy, slow weekend. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_polarbear", "mb2_polarbear", "Where Do Polar Bear Cubs Sleep? ❄️", "POLAR BEAR", "2026-11-16", B,
  ["Shh. Something fluffy and white is getting sleepy in the snow.",
   "Hello, little one. I'm Luna, the sleepy owl. Let's visit the snowy north tonight. Get cozy, and listen softly.",
   "It's a Polar Bear Cub. Polar bears live far up north, where there's lots of snow and ice. Their thick fur keeps them warm.",
   "Where are polar bear cubs born? In a cozy den, dug into the snow, snuggled close to Mama Bear.",
   "Can you give yourself a big, soft polar bear hug? Squeeze gently, and take a slow, sleepy breath.",
   "Goodnight, Polar Bear Cub. Sleep warm. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_toys", "mb2_toybox", "Time for Toys to Go to Sleep 🧸", "TOYS", "2026-11-17", A,
  ["Shh. The playroom is getting sleepy. Who needs to be tucked in tonight?",
   "Hello, little one. I'm Luna, the sleepy owl. Let's help the toys get ready for bed. Get cozy, and listen softly.",
   "It's the Toy Box. When we put our toys away at night, the room feels calm, and our toys are easy to find tomorrow.",
   "Who goes in the toy box? The ball, the blocks, and teddy too. All tucked in, safe and sound.",
   "Can you pretend to put a toy away, gently? One toy, two toys, three toys. All done. What a helper.",
   "Goodnight, toys. Goodnight, Toy Box. Sweet dreams, from Moonbeam Bedtime."]),
 ("mb2_s_tulip", "mb2_tulip", "Why Do Some Flowers Close at Night? 🌷", "TULIP", "2026-11-17", B,
  ["Look. A pretty pink flower is slowly folding up its petals. Why?",
   "Hello, little one. I'm Luna, the sleepy owl. Let's visit the garden as the moon comes up. Get cozy, and listen softly.",
   "It's Tulip. Some flowers, like tulips, close their petals at night. In the morning, when the sun comes back, they open again.",
   "What does Tulip do at night? She closes her petals, like she's going to sleep, just like you.",
   "Can you close your hands slowly, like a flower closing its petals? Slowly, slowly, all the way closed.",
   "Goodnight, Tulip. See you in the morning. Sweet dreams, from Moonbeam Bedtime."]),
]
ACTS = ["hook", "milo_in", None, "fx+bob", "bob", "fxoff+outro"]
shorts = []
for sid, k, t, word, d, tm, says in SH:
    acts = [a if a else f"zoom+badge:{NAMES_MOON2[k]}" for a in ACTS]
    shorts.append({"id": sid, "animal": k, "title": t, "thumb": word, "top": word, "bg": ["#1d2456", "#3a3f86"], "floor": "#232a5c",
                   "sources": SRC_TOY if k in ("mb2_toybox", "mb2_fort") else SRC, "beats": [{"say": s, "act": a} for s, a in zip(says, acts)]})
json.dump(shorts, open("shorts_moon2.json", "w"), indent=1, ensure_ascii=False)

# ---------- thumbnails + upload plan (same style as mkplan.py / existing brand/moon thumbs) ----------
font = "@font-face{font-family:Baloo;src:url(/root/zoo/vendor/f/package/files/baloo-2-latin-800-normal.woff2)}"
cfg = dict(name="Moonbeam Bedtime", host_desc="Luna the sleepy owl", aud="2-7", aud2="2–7", emoji="🌙", tag="#BedtimeStories #SleepyTime #KidsBedtime #CalmForKids",
           bg="#2a3175", glow="#5c64b8", stroke="#1a237e", accent="#7e6bb8", ground="#232a5c", short_kind="A calm bedtime Short", ep_kind="calm bedtime story")
def animal(s):
    i = s.index('<g id="animal"'); depth = 0; j = i
    for m in re.finditer(r'<g[\s>]|</g>', s[i:]):
        depth += 1 if m.group().startswith('<g') else -1
        if depth == 0: j = i + m.end(); break
    return "".join(re.findall(r'<defs>.*?</defs>', s, re.S)) + s[i:j]
def pet(k, x, y, h):
    w = h * 1080 / 1100; return f'<svg viewBox="0 0 1080 1100" width="{w:.0f}" height="{h}" style="position:absolute;left:{x}px;top:{y}px">{animal(S[k])}</svg>'
THUMB_KEYS = {"mb_ep11_train": ["mb2_engine", "mb2_sleepcar", "mb2_caboose", "mb2_station"]}  # the bridge scene is a wide panorama, skip it on the thumb
pos4 = [(-60, 300, 420), (190, 330, 400), (440, 330, 400), (680, 300, 420)]
pos = [(-40, 300, 400), (160, 350, 360), (360, 310, 390), (560, 350, 360), (760, 320, 380)]
Bp = f"{cfg['name']} makes gentle, colorful videos for little learners. New videos every day! Made with care for ages {cfg['aud']}. Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing."
plan = []
for s in shorts:
    b = [x["say"] for x in s["beats"]]
    dsc = f"{b[0]} {cfg['host_desc']} finds out! {cfg['emoji']}\n{cfg['short_kind']} for kids ages {cfg['aud2']} from {cfg['name']}.\n\n{' '.join(b[2:5])}\n\n{Bp}\n\n#Shorts {cfg['tag']}"
    sh = next(x for x in SH if x[0] == s["id"])
    plan.append({"file": f"moon/{s['id']}.mp4", "title": s["title"], "description": dsc, "date": sh[4], "time": sh[5], "status": "to_upload"})
os.makedirs("brand/moon", exist_ok=True)
for eid, title, keys, what, final, (a, b2), dt in EPS:
    e = json.load(open(f"eps/{eid}.json"))
    tk = THUMB_KEYS.get(eid, keys)
    p = "".join(pet(v, x, y, h) for v, (x, y, h) in zip(tk, pos if len(tk) == 5 else pos4))
    html = f"""<html><head><meta charset="utf-8"><style>{font}*{{margin:0}}body{{width:1280px;height:720px;overflow:hidden;position:relative;font-family:Baloo;background:radial-gradient(circle at 70% 30%,{cfg['glow']} 0,{cfg['bg']} 62%)}}
.t{{position:absolute;left:40px;font-size:{110 if len(a)<12 else 92}px;line-height:1;color:#fff;-webkit-text-stroke:14px {cfg['stroke']};paint-order:stroke fill;text-shadow:0 8px 0 rgba(0,0,0,.18)}}
#n{{position:absolute;right:40px;top:30px;width:180px;height:180px;border-radius:50%;background:{cfg['accent']};color:#fff;font-size:140px;line-height:205px;text-align:center;box-shadow:0 8px 0 rgba(0,0,0,.18)}}
#m{{position:absolute;left:930px;top:250px;transform:scale(1.05);transform-origin:0 0}}#g{{position:absolute;left:0;right:0;bottom:0;height:110px;background:{cfg['ground']}}}</style></head>
<body><div id="g"></div>{p}<div class="t" style="top:28px">{a}</div><div class="t" style="top:140px;color:#ffe066">{b2}</div><div id="n">🌙</div><div id="m">{HOST}</div></body></html>"""
    open(f"brand/moon/thumb_{eid}.html", "w").write(html)
    learn = "\n".join("• " + r[0] for r in e["recap"][1:])
    dsc = f"Join {cfg['host_desc']} for a 5-minute {cfg['ep_kind']}! {e['intro'][1][0]} {cfg['emoji']}\nMade for little learners ages {cfg['aud2']}: guess-what clues, move-along fun, and a recap at the end.\n\nWhat we learn today:\n{learn}\n\n{Bp}\n\n{cfg['tag']}"
    plan.append({"file": f"moon/{eid}.mp4", "title": title, "description": dsc, "date": dt, "time": "7:00 PM", "status": "to_upload", "thumb": f"brand/moon/thumb_{eid}.png"})
plan.sort(key=lambda x: (x["date"], {"9:00 AM": 0, "5:00 PM": 1, "7:00 PM": 2}[x["time"]]))
json.dump(plan, open("upload_plan_moon2.json", "w"), indent=1, ensure_ascii=False)
print(len(shorts), "shorts,", len(EPS), "episodes,", len(plan), "plan rows")
