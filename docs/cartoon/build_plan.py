"""Builds plan.html: the three pillars, the formats, the first content block (15 adventures, 15 fact lessons, 10 story songs, 20 Shorts),
playlists, packaging, the quality gate and how each upload is measured. Nov 16 2026.

Facts marked R were read at their source on Nov 16 2026 (the sentence is in the episode files). Facts marked V are ideas only:
they are read at the source on the day the script is written, and the line comes out if the source does not say it."""
import os, html as H
HERE = os.path.dirname(os.path.abspath(__file__))

THEMES = [
 dict(key="savanna", name="Savanna week", friend="Tumble the baby elephant", place="the sunny savanna",
  adv=[("Baby Elephant's Birthday Surprise for Mama", "Tumble has no present for Mama. He sets off with Milo for the golden fruit at the top of the tallest tree.|A river, a tall tree and a sandy hill are in the way. Mango and Sandy help. Then the fruit rolls away and goes splat.|The friends find the seed inside and plant a fruit tree for Mama. A trunk hug.",
        "R: a trunk works like a snorkel in deep water (WWF). R: a spider monkey's tail holds on like a fifth limb (Nat Geo Kids). R: a camel's wide feet do not sink in sand (San Diego Zoo).", "Tumble holds the golden fruit up to Mama, both smiling. Words: BEST GIFT EVER!", "built as the test episode"),
       ("Tumble and the Big Muddy Puddle", "Photo day at the zoo. Tumble wants to stay clean, but the sun is very hot.|He tries a leaf hat, a fan and the shade. Each one helps for a moment, then he is hot again.|Mama shows him the mud. Everybody ends up muddy, cool and laughing in the photo.",
        "V: elephants cover themselves in mud and dust, which shields their skin from the sun. R: ear flapping cools an elephant on warm days (San Diego Zoo).", "A muddy, grinning Tumble with one clean eye. Words: MUD DAY!", ""),
       ("Tumble Shares the Last Drink", "It has not rained and the water hole is low. Tumble finds one small pool.|Three little birds are thirsty too. The pool is too deep in a crack for their beaks.|Tumble sucks the water up with his trunk and squirts a drink for each friend. Then the rain comes.",
        "R: elephants suck water up their trunks, then blow it into their mouths (WWF). R: they can smell water far away (WWF).", "Tumble squirts an arc of water to three birds. Words: SQUIRT!", "")],
  les=[("Why Do Elephants Have Such Big Ears?", "Milo's mission: find out what the giant ears are for. Guess first: hearing, flying, or cooling?", "R: an elephant's ears work like a radiator; flapping cools the body (San Diego Zoo).", "One huge ear fills half the picture, a tiny Milo beside it. Words: LIKE A FAN?!"),
       ("What Can an Elephant's Trunk Do?", "Milo counts the jobs of one nose with Tumble: smell, grab, drink, spray, snorkel, hug.", "R: smelling, grabbing, snorkel, drinking (WWF). R: strong enough for a log, gentle enough for one straw; used in greeting and caressing (San Diego Zoo).", "A trunk holding one tiny straw. Words: ONE NOSE?!"),
       ("Who Looks After a Baby Elephant?", "Milo meets Tumble's family: Mama, and the herd around a calf.", "R: a calf drinks its mother's milk with its mouth (San Diego Zoo). V: other females in the herd help look after calves.", "Tumble under Mama, two more elephants close by. Words: WHOLE FAMILY!")],
  songs=[("Trunks Up! (Tumble's Song)", "Tumble", "proud to try", "Three tries with his trunk: a leaf, a splash, a hug.", "Trunks up, trunks up, I can try!"),
         ("Trunk Hug (I Love You, Mama)", "Tumble and Mama", "love at the end of the day", "From the water hole home to bed.", "Trunk hug, trunk hug, close to you.")],
  shorts=[("Can an Elephant Hide Under the Water?", "story moment + fact, from the birthday adventure", "First frame: only a trunk tip sticks out of a river. WHAT IS THAT?", "The trunk is a snorkel."),
          ("Why Did the Golden Fruit Go SPLAT?", "story moment, from the birthday adventure", "First frame: the fruit in mid-air over the hill.", "The seed inside becomes Mama's present."),
          ("Why Are Elephant Ears So Big?", "from the ears lesson", "First frame: an ear as big as the screen.", "They cool the elephant down."),
          ("One Nose, Six Jobs!", "from the trunk lesson", "First frame: a trunk holding one straw.", "Count the six jobs.")]),
 dict(key="jungle", name="Jungle week", friend="Mango the spider monkey", place="the green jungle",
  adv=[("Mango and the Wobbly Vine Bridge", "A picnic waits on the other side of a little stream. The only way is a low, wobbly vine bridge.|Tumble is too nervous to step on it. Mango runs across too fast and the picnic basket tips.|Mango slows down, holds on with her tail and walks beside Tumble, one step at a time.",
        "R: the tail grasps like a fifth limb (Nat Geo Kids). R: spider monkeys have no thumbs (Nat Geo Kids).", "Mango holds a vine with her tail and Tumble's trunk with her hand. Words: HOLD ON!", ""),
       ("Who Took Mango's Breakfast?", "Mango's fruit is gone from her branch. She is sure somebody took it.|The friends follow three clues: a peel, a trail of drips, a happy hum.|The fruit had rolled down to a baby tapir, who thought it was a gift. Mango shares the rest.",
        "R: fruit is the main part of a spider monkey's diet (Nat Geo Kids). V: one true fact about the animal who found the fruit.", "Mango with a magnifying glass over a banana peel. Words: A MYSTERY!", ""),
       ("The Rainy Day Umbrella", "Rain starts on the way to Mango's tree house. Milo's feathers are soaked.|A small leaf, a flower, a hat of moss: each one is too small.|Together they carry one giant leaf, and all four fit under it.",
        "V: how much rain a rainforest gets. V: one animal that shelters under leaves.", "Four friends under one giant leaf in the rain. Words: ROOM FOR ALL!", "")],
  les=[("Why Do Monkeys Have Long Tails?", "Milo's mission: is a tail a toy, a scarf or a hand?", "R: prehensile tail, a fifth limb; they hang upside down from it (Nat Geo Kids).", "Mango upside down, her tail in the middle of the picture. Words: EXTRA HAND?!"),
       ("What Does a Monkey Eat All Day?", "Milo follows Mango from breakfast to dinner.", "R: fruit is the main part of the diet (Nat Geo Kids). V: what else they eat.", "Mango behind a pile of fruit. Words: SO MUCH FRUIT!"),
       ("Who Lives at the Top of the Jungle?", "Milo flies up the tallest tree, floor by floor.", "V: the layers of a rainforest and one animal for each.", "A tree cut in four floors with an animal on each. Words: WAY UP HIGH!")],
  songs=[("Swing-a-Ding (Mango's Song)", "Mango", "joy of moving", "Branch to branch across the jungle to a friend.", "Swing-a-ding, swing-a-ding, here I go!"),
         ("Rain on the Leaves", "Mango and Milo", "calm and cosy", "The rain comes, they wait under a leaf, the sun returns.", "Drip, drop, drip, we are dry in here.")],
  shorts=[("How Many Hands Does This Monkey Have?", "fact, from the tail lesson", "First frame: Mango hangs with both hands full of fruit.", "Two hands and one tail."),
          ("Why Does This Monkey Hang Upside Down?", "fact, from the tail lesson", "First frame: an upside-down face, very close.", "Her tail holds her whole body."),
          ("Who Took the Breakfast?", "story moment, from the breakfast adventure", "First frame: an empty branch and one peel.", "A baby tapir thought it was a gift."),
          ("Can a Monkey Pick Fruit With No Thumbs?", "fact, from the tail lesson", "First frame: a monkey hand, four fingers.", "Hook hands, and a tail to hold on.")]),
 dict(key="desert", name="Desert week", friend="Sandy the baby camel", place="the sandy desert",
  adv=[("Sandy and the Flying Scarf", "The wind takes Milo's red scarf and carries it over the dunes.|Sand blows in everyone's eyes and noses. Only Sandy can keep walking.|Sandy leads the way with her nose shut and brings the scarf home.",
        "R: two rows of long eyelashes; camels can close their nostrils (San Diego Zoo).", "Sandy with the red scarf on her head, wind lines around her. Words: GOT IT!", ""),
       ("The Long Walk to the Oasis", "A little tree at the zoo is thirsty and the watering can is empty.|The oasis is far. Milo gets tired, Tumble gets hot, the sand is soft.|Sandy carries the water all the way, step by step. The tree drinks.",
        "R: a thirsty camel can drink 30 gallons in 13 minutes (National Geographic). R: a camel can go a week or more without water (San Diego Zoo).", "Sandy carries two water jugs up a dune. Words: SO FAR!", ""),
       ("Sandy's First Night Away", "Sandy is invited to a sleepover at the zoo, away from Mama for the first time.|The bed is too soft, the night is too quiet, and she misses Mama's hum.|Her friends hum with her until she sleeps. In the morning Mama is at the gate.",
        "R: mothers and their newborns hum to each other (San Diego Zoo).", "Sandy under a blanket with a little moon, friends around her. Words: SWEET DREAMS!", "")],
  les=[("What Is Inside a Camel's Hump?", "Milo and baby Sandy find out why Mama has a hump and Sandy has none.", "R: fat, not water; a hump droops when the fat is used; a calf has a tuft, no hump (San Diego Zoo). R: 80 pounds of fat (National Geographic).", "A hump cut open, full of round yellow fat. Words: NOT WATER?!"),
       ("What Do Camels Eat in the Desert?", "Milo and Sandy look for lunch in the desert: what can a camel eat where so little grows?", "R: what camels eat (thorny, dry desert plants) and how their mouths and lips manage it (San Diego Zoo, National Geographic); keep only what the pages say. Not the eyelashes, nose, feet, hump or drinking: those are in the live hump lesson (zc_ep01).", "Sandy munching a thorny branch. Words: THORNS? YUM!"),   # replaced Nov 19 (daily run): "Why Do Camels Have Long Eyelashes?" repeats the live zc_ep01 part 3 / zc_ep01_short3 (two rows of eyelashes, a nose that closes)
       ("One Hump or Two? Meet the Camels", "Milo visits Sandy's cousin in the snow.", "R: dromedary one hump, Bactrian two (San Diego Zoo). R: cold winters, snow (Nat Geo Kids).", "Two camels back to back, one hump and two. Words: COUSINS?!")],
  songs=[("Step, Step, Step (Sandy's Song)", "Sandy", "patience", "A long walk over three dunes to the water.", "Step, step, step, I will get there."),
         ("Close to Mama (Desert Lullaby)", "Sandy and Mama", "safe and sleepy", "The sun goes down, the stars come out, Mama hums.", "Hmm, hmm, close to Mama.")],
  shorts=[("Why Does This Baby Camel Have No Hump?", "fact, from the hump lesson", "First frame: Sandy's flat back and a big question mark.", "Fat, not water. Her hump will grow."),
          ("How Much Can a Camel Drink?", "fact, from the hump lesson", "First frame: Mama's nose in the water and a counter at 0.", "30 gallons in 13 minutes."),
          ("Can You Close Your Nose?", "fact, from the eyelashes lesson", "First frame: a camel nose, very close.", "A camel can. No sand gets in."),
          ("Catch Milo's Scarf!", "story moment, from the scarf adventure", "First frame: the red scarf flying away.", "Sandy walks through the wind and brings it back.")]),
 dict(key="guess", name="Guess With Milo (owner, Nov 20 2026: always 2D)", friend="Milo and the zoo friends", place="the zoo trail",
  adv=[],
  les=[("Whose Feet Are These? Guess With Milo", "GUESS WITH MILO format (docs/CARTOON_RUN.md 'Guess With Milo'): cold open on ONE giant footprint in the sand, first line 'Look! A giant footprint in the sand! Who made it?', Milo says his name after the hook. Three parts, each opening on its own print with two answer signs and 4 s thinking time BEFORE the animal walks in: elephant (tiptoes, soft cushion, toenails), giraffe (two hooves on each foot, walks both legs of one side together), zebra (one toe inside one hoof, hoof keeps growing). Quiz, then the footprint trail recap. Full draft script and shot plan: drafts/growth_test_2026-11/pilot/ (written for 3D; port the words and beats, not the 3D props).",
        "R (read Nov 19, read again on the build day): elephant walks 'on tiptoes', fat pads 'cushion bottoms of feet', savanna '4 to 5 nails on forefeet' (SDZWA Library, African Elephant). R: giraffe 'two weight-bearing hooves on each foot', feet '12 inches (30.5 cm) across' (Live Science); 'Alternate moving the two right limbs together and then the two left' (SDZWA Library, Giraffe behavior). R: zebra 'Single toe at terminus of each limb', 'Hooves enclose and protect the toe', hoof 'grows continually' (SDZWA Library, Plains Zebra).",
        "One giant footprint in the sand fills half the picture, Milo leaning over it with a wing at his beak, a big yellow question mark. Words: WHO?"),
       ("Whose Ears Are These? Guess With Milo", "GUESS WITH MILO format: cold open on two ears poking out of tall grass, each turning a different way; first line 'Look! Two ears in the grass, and they're turning different ways! Who is it?'. Three parts, each starting with an ear silhouette and two answer signs before the animal appears: rhino, fox, koala (or the three whose ear facts the build day's sources confirm). Listening action: cup your hands behind your ears. Quiz, recap.",
        "V: a rhino can turn each ear a different way (the channel's most re-watched Short; read again at the source). V: one true ear fact each for the fox and the koala, read on the build day; a line comes out if the source does not say it.",
        "Two big grey ears turning opposite ways above tall grass, the animal hidden, Milo cupping a wing to his ear. Words: LISTEN!"),
       ("Whose Egg Is This? Guess With Milo", "GUESS WITH MILO format: cold open on ONE big egg in a nest wobbling, a tiny crack on the first word; first line 'Look! An egg is wobbling! Who is inside?'. Three parts, each a different egg (size, colour, place) with two answer signs before it hatches and the mama comes: ostrich, sea turtle, penguin (or the three whose egg facts the build day's sources confirm). Gentle hatch, every baby safe with its family. Quiz, recap.",
        "V: one true egg fact each (size, where it is laid, who keeps it warm), read on the build day at a zoo or Nat Geo page; a line comes out if the source does not say it.",
        "One big cream egg with a tiny crack in a sandy nest, Milo peeking from behind it. Words: CRACK!")],
  songs=[], shorts=[]),
 dict(key="arctic", name="Arctic week", friend="Poppy the polar bear cub", place="the snowy Arctic",
  adv=[("Poppy's First Slide on the Ice", "All the friends slide down the snowy hill. Poppy watches from the top. She is too shy to try.|She tries sitting, then holding Milo's wing, and stops each time.|Her friends slide beside her, slowly. At the bottom she asks to go again.",
        "V: polar bear paws are very wide and help them walk on snow and ice. V: the bumps on their paw pads grip the ice.", "Poppy at the top of a snow hill, friends waving below. Words: YOU CAN!", ""),
       ("Too Cold for Milo!", "Milo visits the Arctic and cannot stop shivering.|A leaf blanket is too thin, hopping is too tiring, the sun is too low.|Poppy shows how she stays warm, and the friends build Milo a snug nest.",
        "V: a thick layer of fat and two layers of fur keep polar bears warm.", "Milo shivering in a tiny scarf next to a cosy Poppy. Words: BRRR!", ""),
       ("Poppy and the Dancing Sky", "The night sky is going to dance. Poppy wants to see it, but she always falls asleep first.|She tries counting stars, a song, a walk. Yawn.|Her friends take turns keeping watch and wake her gently when the lights come.",
        "V: the northern lights appear in the far north on dark, clear nights.", "Green lights in the sky over a sleepy cub. Words: WAKE UP!", "")],
  les=[("How Do Polar Bears Stay Warm?", "Milo's mission in the snow: what is under Poppy's coat?", "V: fat layer, two layers of fur.", "Poppy in the snow with a little thermometer. Words: NOT COLD?!"),
       ("Is a Polar Bear Really White?", "Milo looks very closely at one hair.", "V: the hairs are clear and hollow; the skin under them is black.", "One polar bear hair under a magnifying glass. Words: SEE-THROUGH?!"),
       ("Who Lives on the Ice?", "Milo meets Poppy's neighbours.", "V: seals, walruses and Arctic foxes live in the Arctic; penguins live in the far south.", "Poppy with a seal and a fox, and a crossed-out penguin shape. Words: NO PENGUINS?!")],
  songs=[("Brrr-illiant Day (Poppy's Song)", "Poppy", "brave enough to try", "From the top of the hill to the bottom, three tries.", "Brrr, brrr, brilliant day!"),
         ("Snowflakes Falling (Winter Lullaby)", "Poppy", "quiet wonder", "One snowflake falls on her nose, then many.", "Soft, soft, snowflakes fall.")],
  shorts=[("Is This Polar Bear Really White?", "fact, from the white-bear lesson", "First frame: one hair, clear like glass.", "The hair is clear, the skin is black."),
          ("Why Don't Polar Bears Slip?", "fact, from the slide adventure", "First frame: a giant paw on blue ice.", "Wide paws with bumpy pads."),
          ("Do Penguins Meet Polar Bears?", "fact, from the neighbours lesson", "First frame: a penguin and a polar bear nose to nose with a question mark.", "No. They live at opposite ends of the world."),
          ("Poppy's First Slide", "story moment, from the slide adventure", "First frame: Poppy's paws at the edge of the hill.", "She slides, and asks to go again.")]),
 dict(key="ocean", name="Ocean week", friend="Tula the sea turtle", place="the blue ocean",
  adv=[("Tula and the Slow, Slow Race", "The sea friends race to the big rock. Tula is the slowest and nobody wants her on their team.|The fast swimmers get tired, get tangled in seagrass and take a wrong turn.|Tula keeps her steady pace, shows the way and they all touch the rock together.",
        "V: sea turtles swim long distances at a steady pace. V: green turtles eat seagrass.", "Tula swims past two puffing fish. Words: LAST IS FIRST?", ""),
       ("A New House for Little Crab", "Little Crab has grown, and his shell pinches.|One shell is too big, one too heavy, one already has somebody in it.|Tula carries shells from the deep until one fits just right.",
        "V: a hermit crab moves into a bigger shell as it grows.", "A tiny crab between a huge shell and a tiny one. Words: TOO SMALL!", ""),
       ("Milo and the Deep Blue Sea", "Milo wants to see where Tula lives, but birds cannot breathe under the water.|A leaf boat tips, a reed is too short, a jump is too splashy.|Tula comes up for air right beside him, and tells him the whole sea from the top.",
        "V: sea turtles breathe air and come up to the surface for it.", "Milo on a leaf boat, Tula's head just out of the water. Words: UP FOR AIR!", "")],
  les=[("How Do Sea Turtles Breathe?", "Milo's mission at the beach: does Tula have gills like a fish?", "V: lungs, not gills; they surface for air and can hold their breath a long time.", "Tula's nose above the water, bubbles below. Words: NO GILLS?!"),
       ("Can a Turtle Leave Its Shell?", "Milo knocks on Tula's shell.", "V: the shell is part of the skeleton, joined to the backbone and ribs.", "A shell with a little door drawn on it and a question mark. Words: STUCK ON?!"),
       ("What Do Sea Turtles Eat?", "Lunch time under the sea with Tula.", "V: green turtles eat seagrass and algae.", "Tula with a mouthful of seagrass. Words: GREEN LUNCH!")],
  songs=[("Slow and Steady (Tula's Song)", "Tula", "calm confidence", "Across the sea to the big rock, never hurrying.", "Slow and steady, here I go."),
         ("Goodnight, Blue Ocean (Lullaby)", "Tula", "sleepy and safe", "The water turns dark blue, the fish go quiet, Tula rests.", "Goodnight, goodnight, blue ocean.")],
  shorts=[("Is a Turtle Stuck in Its Shell?", "fact, from the shell lesson", "First frame: a shell with a door and a question mark.", "No. The shell is part of her body."),
          ("Does a Sea Turtle Breathe Water?", "fact, from the breathing lesson", "First frame: Tula under the water holding her breath, cheeks full.", "She swims up for air."),
          ("Why Does This Crab Change Houses?", "story moment, from the crab adventure", "First frame: a crab half out of a tiny shell.", "He grew. He needs a bigger one."),
          ("Slow Wins the Race?", "story moment, from the race adventure", "First frame: Tula far behind three fast fish.", "They all finish together.")]),
 dict(key="farm", name="Farm week (written Nov 27 2026 by the afternoon adventure build: Clover had no theme)", friend="Clover the lamb", place="the sunny farm",
  adv=[("Clover Leads the Flock Home", "The sun is going down and it is supper time in the barn. Little Clover wants to bring the big sheep home from the meadow, but they keep munching.|She calls, and nobody hears. She pushes, and nobody moves. She runs round and round them, and gets dizzy.|Then she sees how one sheep walks and the others follow. Clover walks first, head high, and the flock follows her home, one by one.",
        "V: a group of sheep is a flock. V: sheep follow one another: when one sheep moves, the rest of the flock usually follows. V: sheep eat grass.", "Little Clover in front, three big sheep in a line behind her. Words: FOLLOW ME!", ""),
       ("Clover and the Woolly Haircut", "It is a warm day and the big sheep are getting their haircut. Clover is not sure she wants her soft coat cut.|She hides behind the hay, under a bucket and in the tall grass, and gets hotter and hotter.|She watches Mama feel cool and happy after her haircut, and tries it herself. The wool becomes a warm scarf for Milo.",
        "V: sheep are shorn about once a year and the wool grows back. V: wool is spun into yarn for warm clothes.", "Clover peeking from behind a big pile of wool. Words: SO FLUFFY!", ""),
       ("Clover's Big Jump Over the Puddle", "After the rain there is a big puddle between Clover and the sweetest patch of clover.|She tries to step round it, to tiptoe through it, and to wait for it to dry.|She practises little hops with her friends until she can jump it, and they all share the sweet clover.",
        "V: lambs play by running and jumping together. V: sheep eat grass and clover.", "Clover in mid-jump over a shiny puddle. Words: HOP, HOP!", "")],
  les=[], songs=[], shorts=[]),
 dict(key="nightforest", name="Night forest week (written Nov 27 2026: Hazel had no theme)", friend="Hazel the hedgehog", place="the night forest",
  adv=[("Hazel's Night-Time Snack Hunt", "When the moon comes up, Hazel wakes up hungry. Milo is sleepy, but he wants to see what a hedgehog does at night.|It is too dark for Milo to see the snacks, the leaves are too crunchy to be quiet, and the best snack is under a log.|Hazel follows her nose, snuffles under the log and shares the find. Milo learns that some friends are awake at night.",
        "V: hedgehogs are active at night. V: a hedgehog finds its food mostly by smell. V: hedgehogs eat beetles, worms and other small animals.", "Hazel's nose close to the ground under a big moon. Words: SNIFF, SNIFF!", ""),
       ("Hazel and the Crunchy Leaf Bed", "Morning is coming and Hazel needs a bed for the day.|One spot is too windy, one is too wet, one is too bright.|Hazel gathers dry leaves under a bush and makes her own cosy nest. She curls up small, and Milo says goodnight in the morning.",
        "V: hedgehogs sleep in the day in nests of leaves and grass. V: a hedgehog can curl up into a ball.", "Hazel curled up in a round nest of orange leaves. Words: COSY!", "")],
  les=[], songs=[], shorts=[]),
]


def e(s): return H.escape(s, quote=False)


def facts(s):
    out = []
    for part in [p.strip() for p in s.replace(". V:", ".|V:").replace(". R:", ".|R:").split("|") if p.strip()]:
        k = part[0]; out.append(f'<span class="f {"r" if k == "R" else "v"}"><b>{"read" if k == "R" else "to read"}</b>{e(part[2:].strip())}</span>')
    return "".join(out)


def theme_html(t, n):
    adv = "".join(f'<article class="ep"><h4>{e(a[0])}</h4><ol class="plot">{"".join(f"<li>{e(x)}</li>" for x in a[1].split("|"))}</ol><div class="fs">{facts(a[2])}</div>'
                  f'<p class="th"><b>Thumbnail</b> {e(a[3])}</p>{f"<p class=st>{e(a[4])}</p>" if a[4] else ""}</article>' for a in t["adv"])
    les = "".join(f'<article class="ep"><h4>{e(a[0])}</h4><p>{e(a[1])}</p><div class="fs">{facts(a[2])}</div><p class="th"><b>Thumbnail</b> {e(a[3])}</p></article>' for a in t["les"])
    songs = "".join(f'<article class="ep"><h4>{e(a[0])}</h4><p><b>Who</b> {e(a[1])} · <b>Feeling</b> {e(a[2])}</p><p><b>Journey</b> {e(a[3])}</p><p class="th"><b>Chorus</b> {e(a[4])}</p></article>' for a in t["songs"])
    sh = "".join(f'<tr><td>{e(a[0])}</td><td>{e(a[1])}</td><td>{e(a[2])}</td><td>{e(a[3])}</td></tr>' for a in t["shorts"])
    return (f'<section class="theme" id="{t["key"]}"><p class="eyebrow">Theme {n} · {e(t["place"])}</p><h2>{e(t["name"])}: {e(t["friend"])}</h2>'
            f'<h3>Adventures</h3><div class="grid">{adv}</div><h3>Fact lessons</h3><div class="grid">{les}</div><h3>Story songs (3D)</h3><div class="grid two">{songs}</div>'
            f'<h3>Shorts</h3><div class="tw"><table><thead><tr><th>Title</th><th>Cut from</th><th>First frame</th><th>Payoff at the end</th></tr></thead><tbody>{sh}</tbody></table></div></section>')


n_adv = sum(len(t["adv"]) for t in THEMES); n_les = sum(len(t["les"]) for t in THEMES); n_song = sum(len(t["songs"]) for t in THEMES); n_sh = sum(len(t["shorts"]) for t in THEMES)
assert (n_adv, n_les, n_song, n_sh) == (20, 18, 10, 20), (n_adv, n_les, n_song, n_sh)
import re
titles = []
for t in THEMES:
    for a in t["adv"] + t["les"] + t["songs"] + t["shorts"]:
        assert len(a[0]) <= 60, (len(a[0]), a[0]); titles.append(a[0].lower())
    for a in t["adv"] + t["les"]:          # the thumbnail's words: 3 at most, none of the title's
        w = re.findall(r"[a-z']+", a[3].split("Words:")[1].lower()); tw = set(re.findall(r"[a-z']+", a[0].lower().replace("'s", "")))
        assert len(w) <= 3 and not [x for x in w if x in tw], (a[0], w)
assert len(titles) == len(set(titles)), [x for x in titles if titles.count(x) > 1]

CSS = open(os.path.join(HERE, "plan.css")).read()
body = open(os.path.join(HERE, "plan_body.html")).read()
import json
ST = json.load(open(os.path.join(HERE, "status.json")))          # what exists today, written after the checks ran
for k, v in ST.items(): body = body.replace("{{" + k + "}}", v)
page = body.replace("{{CSS}}", CSS).replace("{{THEMES}}", "".join(theme_html(t, k + 1) for k, t in enumerate(THEMES))).replace(
    "{{TOC}}", "".join(f'<a href="#{t["key"]}">{e(t["name"])}</a>' for t in THEMES))
open(os.path.join(HERE, "plan.html"), "w").write(page); print("plan.html", len(page), "bytes;", n_adv, "adventures,", n_les, "lessons,", n_song, "songs,", n_sh, "Shorts")
