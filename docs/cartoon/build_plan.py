"""Builds plan.html: the three pillars, the formats, the first content block (15 adventures, 15 fact lessons, 10 story songs, 20 Shorts),
playlists, packaging, the quality gate and how each upload is measured. Nov 16 2026.

Facts marked R were read at their source on Nov 16 2026 (the sentence is in the episode files). Facts marked V are ideas only:
they are read at the source on the day the script is written, and the line comes out if the source does not say it."""
import os, html as H
HERE = os.path.dirname(os.path.abspath(__file__))

THEMES = [
 dict(key="savanna", name="Savanna week", friend="Tumble the baby elephant", place="the sunny savanna",
  adv=[("Baby Elephant's Birthday Surprise for Mama", "Tumble has no present for Mama. He sets off with Milo for the golden fruit at the top of the tallest tree.|A river, a tall tree and a sandy hill are in the way. Mango and Sandy help. Then the fruit rolls away and goes splat.|The friends find the seed inside and plant a fruit tree for Mama. A trunk hug.",
        "R: a trunk works like a snorkel in deep water (WWF). R: a spider monkey's tail holds on like a fifth limb (Nat Geo Kids). R: a camel's wide feet do not sink in sand (San Diego Zoo).", "Tumble holds the golden fruit up to Mama, both smiling. Words: FOR MAMA!", "built as the test episode"),
       ("Tumble and the Big Muddy Puddle", "Photo day at the zoo. Tumble wants to stay clean, but the sun is very hot.|He tries a leaf hat, a fan and the shade. Each one helps for a moment, then he is hot again.|Mama shows him the mud. Everybody ends up muddy, cool and laughing in the photo.",
        "V: elephants cover themselves in mud and dust, which shields their skin from the sun. R: ear flapping cools an elephant on warm days (San Diego Zoo).", "A muddy, grinning Tumble with one clean eye. Words: MUD DAY!", ""),
       ("Tumble Shares the Last Drink", "It has not rained and the water hole is low. Tumble finds one small pool.|Three little birds are thirsty too. The pool is too deep in a crack for their beaks.|Tumble sucks the water up with his trunk and squirts a drink for each friend. Then the rain comes.",
        "R: elephants suck water up their trunks, then blow it into their mouths (WWF). R: they can smell water far away (WWF).", "Tumble squirts an arc of water to three birds. Words: SQUIRT!", "")],
  les=[("Why Do Elephants Have Such Big Ears?", "Milo's mission: find out what the giant ears are for. Guess first: hearing, flying, or cooling?", "R: an elephant's ears work like a radiator; flapping cools the body (San Diego Zoo).", "One huge ear fills half the picture, a tiny Milo beside it. Words: SO BIG?!"),
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
        "R: fruit is the main part of a spider monkey's diet (Nat Geo Kids). V: one true fact about the animal who found the fruit.", "Mango with a magnifying glass over a banana peel. Words: WHO DID IT?", ""),
       ("The Rainy Day Umbrella", "Rain starts on the way to Mango's tree house. Milo's feathers are soaked.|A small leaf, a flower, a hat of moss: each one is too small.|Together they carry one giant leaf, and all four fit under it.",
        "V: how much rain a rainforest gets. V: one animal that shelters under leaves.", "Four friends under one giant leaf in the rain. Words: ROOM FOR ALL!", "")],
  les=[("Why Do Monkeys Have Long Tails?", "Milo's mission: is a tail a toy, a scarf or a hand?", "R: prehensile tail, a fifth limb; they hang upside down from it (Nat Geo Kids).", "Mango upside down, her tail in the middle of the picture. Words: EXTRA HAND?!"),
       ("What Does a Monkey Eat All Day?", "Milo follows Mango from breakfast to dinner.", "R: fruit is the main part of the diet (Nat Geo Kids). V: what else they eat.", "Mango behind a pile of fruit. Words: ALL DAY?!"),
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
        "R: mothers and their newborns hum to each other (San Diego Zoo).", "Sandy under a blanket with a little moon, friends around her. Words: GOOD NIGHT!", "")],
  les=[("What Is Inside a Camel's Hump?", "Milo and baby Sandy find out why Mama has a hump and Sandy has none.", "R: fat, not water; a hump droops when the fat is used; a calf has a tuft, no hump (San Diego Zoo). R: 80 pounds of fat (National Geographic).", "A hump cut open, full of round yellow fat. Words: NOT WATER?!"),
       ("Why Do Camels Have Long Eyelashes?", "Milo's mission on a windy day: how does Sandy keep the sand out?", "R: double rows of extra-long eyelashes; nostrils close (San Diego Zoo).", "One giant camel eye with two rows of lashes. Words: TWO ROWS?!"),
       ("One Hump or Two? Meet the Camels", "Milo visits Sandy's cousin in the snow.", "R: dromedary one hump, Bactrian two (San Diego Zoo). R: cold winters, snow (Nat Geo Kids).", "Two camels back to back, one hump and two. Words: 1 OR 2?")],
  songs=[("Step, Step, Step (Sandy's Song)", "Sandy", "patience", "A long walk over three dunes to the water.", "Step, step, step, I will get there."),
         ("Close to Mama (Desert Lullaby)", "Sandy and Mama", "safe and sleepy", "The sun goes down, the stars come out, Mama hums.", "Hmm, hmm, close to Mama.")],
  shorts=[("Why Does This Baby Camel Have No Hump?", "fact, from the hump lesson", "First frame: Sandy's flat back and a big question mark.", "Fat, not water. Her hump will grow."),
          ("How Much Can a Camel Drink?", "fact, from the hump lesson", "First frame: Mama's nose in the water and a counter at 0.", "30 gallons in 13 minutes."),
          ("Can You Close Your Nose?", "fact, from the eyelashes lesson", "First frame: a camel nose, very close.", "A camel can. No sand gets in."),
          ("Catch Milo's Scarf!", "story moment, from the scarf adventure", "First frame: the red scarf flying away.", "Sandy walks through the wind and brings it back.")]),
 dict(key="arctic", name="Arctic week", friend="Poppy the polar bear cub", place="the snowy Arctic",
  adv=[("Poppy's First Slide on the Ice", "All the friends slide down the snowy hill. Poppy watches from the top. She is too shy to try.|She tries sitting, then holding Milo's wing, and stops each time.|Her friends slide beside her, slowly. At the bottom she asks to go again.",
        "V: polar bear paws are very wide and help them walk on snow and ice. V: the bumps on their paw pads grip the ice.", "Poppy at the top of a snow hill, friends waving below. Words: YOU CAN!", ""),
       ("Too Cold for Milo!", "Milo visits the Arctic and cannot stop shivering.|A leaf blanket is too thin, hopping is too tiring, the sun is too low.|Poppy shows how she stays warm, and the friends build Milo a snug nest.",
        "V: a thick layer of fat and two layers of fur keep polar bears warm.", "Milo shivering in a tiny scarf next to a cosy Poppy. Words: BRRR!", ""),
       ("Poppy and the Dancing Sky", "The night sky is going to dance. Poppy wants to see it, but she always falls asleep first.|She tries counting stars, a song, a walk. Yawn.|Her friends take turns keeping watch and wake her gently when the lights come.",
        "V: the northern lights appear in the far north on dark, clear nights.", "Green lights in the sky over a sleepy cub. Words: WAKE UP!", "")],
  les=[("How Do Polar Bears Stay Warm?", "Milo's mission in the snow: what is under Poppy's coat?", "V: fat layer, two layers of fur.", "Poppy in the snow with a little thermometer. Words: NOT COLD?!"),
       ("Is a Polar Bear Really White?", "Milo looks very closely at one hair.", "V: the hairs are clear and hollow; the skin under them is black.", "One polar bear hair under a magnifying glass. Words: NOT WHITE?!"),
       ("Who Lives on the Ice?", "Milo meets Poppy's neighbours.", "V: seals, walruses and Arctic foxes live in the Arctic; penguins live in the far south.", "Poppy with a seal and a fox, and a crossed-out penguin shape. Words: NO PENGUINS?!")],
  songs=[("Brrr-illiant Day (Poppy's Song)", "Poppy", "brave enough to try", "From the top of the hill to the bottom, three tries.", "Brrr, brrr, brilliant day!"),
         ("Snowflakes Falling (Winter Lullaby)", "Poppy", "quiet wonder", "One snowflake falls on her nose, then many.", "Soft, soft, snowflakes fall.")],
  shorts=[("Is This Polar Bear Really White?", "fact, from the white-bear lesson", "First frame: one hair, clear like glass.", "The hair is clear, the skin is black."),
          ("Why Don't Polar Bears Slip?", "fact, from the slide adventure", "First frame: a giant paw on blue ice.", "Wide paws with bumpy pads."),
          ("Do Penguins Meet Polar Bears?", "fact, from the neighbours lesson", "First frame: a penguin and a polar bear nose to nose with a question mark.", "No. They live at opposite ends of the world."),
          ("Poppy's First Slide", "story moment, from the slide adventure", "First frame: Poppy's paws at the edge of the hill.", "She slides, and asks to go again.")]),
 dict(key="ocean", name="Ocean week", friend="Tula the sea turtle", place="the blue ocean",
  adv=[("Tula and the Slow, Slow Race", "The sea friends race to the big rock. Tula is the slowest and nobody wants her on their team.|The fast swimmers get tired, get tangled in seagrass and take a wrong turn.|Tula keeps her steady pace, shows the way and they all touch the rock together.",
        "V: sea turtles swim long distances at a steady pace. V: green turtles eat seagrass.", "Tula swims past two puffing fish. Words: SLOW WINS?", ""),
       ("A New House for Little Crab", "Little Crab has grown, and his shell pinches.|One shell is too big, one too heavy, one already has somebody in it.|Tula carries shells from the deep until one fits just right.",
        "V: a hermit crab moves into a bigger shell as it grows.", "A tiny crab between a huge shell and a tiny one. Words: TOO SMALL!", ""),
       ("Milo and the Deep Blue Sea", "Milo wants to see where Tula lives, but birds cannot breathe under the water.|A leaf boat tips, a reed is too short, a jump is too splashy.|Tula comes up for air right beside him, and tells him the whole sea from the top.",
        "V: sea turtles breathe air and come up to the surface for it.", "Milo on a leaf boat, Tula's head just out of the water. Words: UP FOR AIR!", "")],
  les=[("How Do Sea Turtles Breathe?", "Milo's mission at the beach: does Tula have gills like a fish?", "V: lungs, not gills; they surface for air and can hold their breath a long time.", "Tula's nose above the water, bubbles below. Words: NO GILLS?!"),
       ("Can a Turtle Leave Its Shell?", "Milo knocks on Tula's shell.", "V: the shell is part of the skeleton, joined to the backbone and ribs.", "A shell with a little door drawn on it and a question mark. Words: STUCK ON?!"),
       ("What Do Sea Turtles Eat?", "Lunch time under the sea with Tula.", "V: green turtles eat seagrass and algae.", "Tula with a mouthful of seagrass. Words: SEA SALAD!")],
  songs=[("Slow and Steady (Tula's Song)", "Tula", "calm confidence", "Across the sea to the big rock, never hurrying.", "Slow and steady, here I go."),
         ("Goodnight, Blue Ocean (Lullaby)", "Tula", "sleepy and safe", "The water turns dark blue, the fish go quiet, Tula rests.", "Goodnight, goodnight, blue ocean.")],
  shorts=[("Can a Turtle Leave Its Shell?", "fact, from the shell lesson", "First frame: a shell with a door and a question mark.", "No. The shell is part of her body."),
          ("Does a Sea Turtle Breathe Water?", "fact, from the breathing lesson", "First frame: Tula under the water holding her breath, cheeks full.", "She swims up for air."),
          ("Why Does This Crab Change Houses?", "story moment, from the crab adventure", "First frame: a crab half out of a tiny shell.", "He grew. He needs a bigger one."),
          ("Slow Wins the Race?", "story moment, from the race adventure", "First frame: Tula far behind three fast fish.", "They all finish together.")]),
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
assert (n_adv, n_les, n_song, n_sh) == (15, 15, 10, 20), (n_adv, n_les, n_song, n_sh)
for t in THEMES:
    for a in t["adv"] + t["les"] + t["songs"] + t["shorts"]: assert len(a[0]) <= 60, (len(a[0]), a[0])

CSS = open(os.path.join(HERE, "plan.css")).read()
body = open(os.path.join(HERE, "plan_body.html")).read()
page = body.replace("{{CSS}}", CSS).replace("{{THEMES}}", "".join(theme_html(t, k + 1) for k, t in enumerate(THEMES))).replace(
    "{{TOC}}", "".join(f'<a href="#{t["key"]}">{e(t["name"])}</a>' for t in THEMES))
open(os.path.join(HERE, "plan.html"), "w").write(page); print("plan.html", len(page), "bytes;", n_adv, "adventures,", n_les, "lessons,", n_song, "songs,", n_sh, "Shorts")
