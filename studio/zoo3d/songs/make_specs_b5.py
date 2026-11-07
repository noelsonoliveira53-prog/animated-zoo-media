import json, copy, re, sys
sys.path.insert(0, "/root/zoo/blender/zoo3d"); import timing_lib as TL
Z = "/root/zoo/blender/zoo3d"
B3 = lambda n: json.load(open(f"/root/zoo/specs/b4/{n}.song.json"))
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
L = lambda x: [-3.4, 0.3, 3.5] if x == "l" else [3.4, 0.3, 3.5] if x == "r" else [0, 0.6, 4.3]
specs = []
specs.append(dict(id="bl3d_ep05", base="bl3d_ep04", colors={"red": "#ff3b3b", "orange": "#ff8a1f", "yellow": "#ffd21f", "green": "#3ccf4e", "blue": "#3d8bff", "purple": "#9d6bff", "pink": "#ff7ac0"},
  lyrics="""[Chorus]
Where is Bloop? Where can he be?
Hiding in the rainbow, one, two, three!
Peekaboo, peekaboo, look and see,
Where is Bloop? Find him with me!

[Verse 1]
Is he hiding in the red? Red, red, red!
Peekaboo, there's Bloop's red head!
Is he hiding in the orange? Look, look, look!
Peekaboo, by the orange book!

[Chorus]
Where is Bloop? Where can he be?
Hiding in the rainbow, one, two, three!
Peekaboo, peekaboo, look and see,
Where is Bloop? Find him with me!

[Verse 2]
Is he hiding in the yellow sun?
Peekaboo, yellow, this is fun!
Is he hiding in the green, green grass?
Peekaboo, green, found him fast!

[Bridge]
Cover your eyes, one, two, three!
Open them wide, what do you see?
Peekaboo! Clap, clap, clap!
Peekaboo! Tap, tap, tap!

[Verse 3]
Is he hiding in the blue, blue sky?
Peekaboo, blue, way up high!
Is he hiding in the purple flower?
Peekaboo, purple, rainbow power!

[Chorus]
Where is Bloop? Where can he be?
Hiding in the rainbow, one, two, three!
Peekaboo, peekaboo, look and see,
Where is Bloop? Find him with me!

[Outro]
Peekaboo! Bye-bye, rainbow friends!""",
  props={"chorus1": [T("WHERE IS BLOOP?", "#ff5c8a", size=0.6)], "verse1": [T("RED", "#ff3b3b", "red", at=[-4.4, 0.6, 3.8]), T("ORANGE", "#ff8a1f", "orange", at=[4.4, 0.6, 3.8])],
         "chorus2": [T("WHERE IS BLOOP?", "#ff5c8a", size=0.6)], "verse2": [T("YELLOW", "#ffd21f", "yellow", at=[-4.4, 0.6, 3.8]), T("GREEN", "#3ccf4e", "green", at=[4.4, 0.6, 3.8])],
         "bridge1": [T("PEEKABOO!", "#ff5c8a", "peekaboo", size=0.8), T("CLAP!", "#ff8a1f", "clap", at=L("l"), size=0.6), T("TAP!", "#3d8bff", "tap", at=L("r"), size=0.6)],
         "verse3": [T("BLUE", "#3d8bff", "blue", at=[-4.4, 0.6, 3.8]), T("PURPLE", "#9d6bff", "purple", at=[4.4, 0.6, 3.8])],
         "chorus3": [T("FOUND YOU!", "#ff5c8a", size=0.7)], "outro1": [T("BYE-BYE!", "#ff5c8a")]},
  meta={"title": "Where Is Bloop? Rainbow Hide and Seek Song for Kids", "card": "Where Is Bloop?", "thumb_text": "WHERE IS BLOOP?",
        "description": "Where is Bloop? Play rainbow hide and seek with Bloop the jelly blob! He hides in red, orange, yellow, green, blue and purple, and changes color every time.\nA peekaboo color song for kids: cover your eyes, count to three and find Bloop. Ages 2-5.",
        "tags": ["where is bloop", "hide and seek song", "peekaboo song", "rainbow colors song", "learn colors", "kids songs", "Bloop's Color Lab", "3D kids songs"]}))

specs.append(dict(id="tt3d_ep05", base="tt3d_ep04",
  lyrics="""[Chorus]
Big truck, little truck, here we go!
Fast truck, slow truck, high and low!
Opposites, opposites, sing with me,
Big and little, one, two, three!

[Verse 1]
The fire truck is big, big, big!
The police car is little, zig-zig-zig!
Big goes boom, and little goes beep,
Big and little, side by side we keep!

[Chorus]
Big truck, little truck, here we go!
Fast truck, slow truck, high and low!
Opposites, opposites, sing with me,
Big and little, one, two, three!

[Verse 2]
Zoom, zoom, fast truck, zooming by!
Slow, slow, slow truck, wave goodbye!
Up goes the ladder, high, high, high!
Down goes the ladder, low, bye-bye!

[Bridge]
Stretch up big, big, big!
Crouch down little, little, little!
Run in place so fast, fast, fast!
Now move slow, slow, slow at last!

[Verse 3]
Loud truck, honk, honk, honk!
Quiet truck, shh, tip-toe, tonk!
Opposites are fun to find,
Big and little, every kind!

[Chorus]
Big truck, little truck, here we go!
Fast truck, slow truck, high and low!
Opposites, opposites, sing with me,
Big and little, one, two, three!

[Outro]
Big and little! Bye-bye, trucks!""",
  props={"chorus1": [T("OPPOSITES!", "#e8302a", size=0.8)], "verse1": [T("BIG!", "#e8302a", "big", at=[-2.8, 1.6, 3.6], size=1.0), T("little", "#3b8be0", "little", at=[2.8, 1.6, 3.6], size=0.45)],
         "chorus2": [T("OPPOSITES!", "#e8302a", size=0.8)], "verse2": [T("FAST!", "#2fb54a", "fast", at=[-2.8, 1.6, 3.6], size=0.8), T("slow...", "#ffc107", "slow", at=[2.8, 1.6, 3.6], size=0.6), T("UP!", "#3b8be0", "up", size=0.8)],
         "bridge1": [T("BIG!", "#e8302a", "big", at=L("l"), size=0.9), T("little", "#3b8be0", "little", at=L("r"), size=0.45), T("FAST!", "#2fb54a", "fast", at=L("c"), size=0.7)],
         "verse3": [T("LOUD!", "#e8302a", "loud", at=[-2.8, 1.6, 3.6], size=0.9), T("shh...", "#8e5bd8", "quiet", at=[2.8, 1.6, 3.6], size=0.5)],
         "chorus3": [T("OPPOSITES!", "#e8302a", size=0.8)], "outro1": [T("BYE-BYE!", "#e8302a")]},
  meta={"title": "Big Truck vs Little Truck! Opposites Song for Kids", "card": "Big Truck vs Little Truck!", "thumb_text": "BIG vs LITTLE!",
        "description": "Big truck vs little truck! Learn opposites with Bolt the fire truck and his friends in Tiny Truck Town: big and little, fast and slow, up and down, loud and quiet.\nKids act out every opposite: stretch up big, crouch down little, run fast and move slow. Ages 2-6.",
        "tags": ["opposites song", "big and little", "opposites for kids", "fast and slow", "trucks for kids", "kids songs", "nursery rhymes", "Tiny Truck Town", "3D kids songs"]}))

specs.append(dict(id="fr3d_ep06", base="fr3d_ep05",
  lyrics="""[Chorus]
Peekaboo, peekaboo, guess the fruit!
Who is hiding? Toot, toot, toot!
Look at the color, look at the shape,
Can you guess? Is it a grape?

[Verse 1]
I am yellow, long and bright,
Peel me down and take a bite!
Peekaboo, who can it be?
It's banana! Yes, it's me!

[Chorus]
Peekaboo, peekaboo, guess the fruit!
Who is hiding? Toot, toot, toot!
Look at the color, look at the shape,
Can you guess? Is it a grape?

[Verse 2]
I am red with seeds outside,
Juicy, sweet, I cannot hide!
Peekaboo, who can it be?
It's strawberry! Yes, it's me!

[Bridge]
Cover your eyes, peek, peek, peek!
Open them up, what do you seek?
Point to the fruit, one, two, three,
Peekaboo, it's fruity time with me!

[Verse 3]
I am round and orange too,
Squeeze me into juice for you!
Small and purple, round and sweet,
Orange and grapes, a yummy treat!

[Chorus]
Peekaboo, peekaboo, guess the fruit!
Who is hiding? Toot, toot, toot!
Look at the color, look at the shape,
Can you guess? Is it a grape?

[Outro]
Peekaboo, fruity friends! See you tomorrow!""",
  props={"chorus1": [T("GUESS THE FRUIT!", "#ff5c8a", size=0.6)], "verse1": [T("?", "#ffc107", size=1.4), P("bigfruit", "banana", at=[2.6, 0.9, 3.4], opts={"kind": "banana"})],
         "chorus2": [T("GUESS THE FRUIT!", "#ff5c8a", size=0.6)], "verse2": [T("?", "#e8302a", size=1.4), P("bigfruit", "strawberry", at=[-2.6, 0.9, 3.4], opts={"kind": "strawberry"})],
         "bridge1": [T("PEEK!", "#ff5c8a", "peek", at=L("l"), size=0.7), T("POINT!", "#3cc45a", "point", at=L("r"), size=0.7), T("PEEKABOO!", "#ffc107", "peekaboo", at=L("c"), size=0.6)],
         "verse3": [P("bigfruit", "orange", at=[-2.6, 0.9, 3.4], opts={"kind": "orange"}), P("bigfruit", "grapes", at=[2.6, 0.9, 3.4], opts={"kind": "grape"})],
         "chorus3": [T("GUESS THE FRUIT!", "#ff5c8a", size=0.6)], "outro1": [T("SEE YOU TOMORROW!", "#ff5c8a", size=0.5)]},
  meta={"title": "Can You Guess the Fruit? Peekaboo Song for Kids", "card": "Guess the Fruit!", "thumb_text": "GUESS THE FRUIT?",
        "description": "Can you guess the fruit? Play peekaboo with Pipkiko and the Fruity Friends: listen to the clues about color and shape, then guess banana, strawberry, orange or grapes.\nA guessing game song that builds vocabulary and listening skills. Ages 2-5.",
        "tags": ["guess the fruit", "peekaboo song", "fruit song for kids", "guessing game for kids", "learn fruits", "kids songs", "nursery rhymes", "Fruity Friends", "3D kids songs"]}))

specs.append(dict(id="zoo3d_ep05", base="zoo3d_ep04",
  lyrics="""[Chorus]
Milo had a zoo, E-I-E-I-O!
And at the zoo he had some friends, E-I-E-I-O!
With a roar, roar here, and a toot, toot there,
Milo had a zoo, E-I-E-I-O!

[Lion]
And at the zoo he had a lion, E-I-E-I-O!
With a roar, roar here, and a roar, roar there,
Here a roar, there a roar, everywhere a roar, roar,
Milo had a zoo, E-I-E-I-O!

[Elephant]
And at the zoo he had an elephant, E-I-E-I-O!
With a toot, toot here, and a toot, toot there,
Here a toot, there a toot, everywhere a toot, toot,
Milo had a zoo, E-I-E-I-O!

[Chorus]
Milo had a zoo, E-I-E-I-O!
And at the zoo he had some friends, E-I-E-I-O!
With a roar, roar here, and a toot, toot there,
Milo had a zoo, E-I-E-I-O!

[Giraffe]
And at the zoo he had a giraffe, E-I-E-I-O!
With a munch, munch here, and a munch, munch there,
Tall, tall neck, eating leaves up high,
Milo had a zoo, E-I-E-I-O!

[Zebra]
And at the zoo he had a zebra, E-I-E-I-O!
With a neigh, neigh here, and a stripe, stripe there,
And a hippo too, with a splash, splash, splash,
Milo had a zoo, E-I-E-I-O!

[Bridge]
Roar like a lion, E-I-E-I-O!
Toot like an elephant, E-I-E-I-O!
Munch like a giraffe, neigh like a zebra,
Splash like a hippo, here we go!

[Chorus]
Milo had a zoo, E-I-E-I-O!
And at the zoo he had some friends, E-I-E-I-O!
With a roar, roar here, and a toot, toot there,
Milo had a zoo, E-I-E-I-O!

[Outro]
E-I-E-I-O! Bye-bye, friends!""",
  props={"chorus1": [T("E-I-E-I-O!", "#ffb627", size=0.8)], "lion1": [T("ROAR!", "#ff7a00", "roar", at=[-3.6, -0.3, 2.5], size=0.6)],
         "elephant1": [T("TOOT!", "#5d6b8f", "toot", at=[3.4, 0.4, 3.0], size=0.6)], "chorus2": [T("E-I-E-I-O!", "#ffb627", size=0.8)],
         "giraffe1": [T("MUNCH!", "#b8692c", "munch", at=[3.2, 1.0, 3.0], size=0.5)], "zebra1": [T("NEIGH!", "#25232b", "neigh", at=[3.6, 0.3, 2.6], size=0.5), T("SPLASH!", "#3db8ff", "splash", at=[-3.6, 0.3, 2.6], size=0.5)],
         "bridge1": [T("ROAR!", "#ff7a00", "roar", at=L("l"), size=0.7), T("TOOT!", "#5d6b8f", "toot", at=L("r"), size=0.7), T("SPLASH!", "#3db8ff", "splash", at=L("c"), size=0.7)],
         "chorus3": [T("E-I-E-I-O!", "#ffb627", size=0.8)], "outro1": [T("BYE-BYE!", "#ffb627")]},
  meta={"title": "Milo Had a Zoo! E-I-E-I-O Animal Song for Kids", "card": "Milo Had a Zoo!", "thumb_text": "E-I-E-I-O!",
        "description": "Milo had a zoo, E-I-E-I-O! A safari twist on Old MacDonald with Milo and his animal friends: a lion, an elephant, a giraffe, a zebra and a hippo.\nKids sing the animal sounds and act them out: roar, toot, munch, neigh and splash! Ages 2-6.",
        "tags": ["old macdonald had a farm", "milo had a zoo", "e-i-e-i-o", "animal sounds song", "zoo animals for kids", "kids songs", "nursery rhymes", "The Animated Zoo", "Milo"]}))

specs.append(dict(id="mb3d_ep05", base="mb3d_ep04",
  lyrics="""[Chorus]
Goodnight, little animals, goodnight,
The moon is glowing, soft and bright,
Close your eyes and snuggle tight,
Goodnight, little animals, goodnight.

[Verse 1]
Goodnight, little bunny, in your burrow deep,
Fold your ears and go to sleep,
Goodnight, little lamb, on the soft green hill,
The night is quiet, calm and still.

[Chorus]
Goodnight, little animals, goodnight,
The moon is glowing, soft and bright,
Close your eyes and snuggle tight,
Goodnight, little animals, goodnight.

[Verse 2]
Owls stay up when the stars come out,
Luna says hoo, then flies about,
Teddy bear yawns, a great big yawn,
Sleep until the morning dawn.

[Bridge]
Breathe in slow, like the evening breeze,
Breathe out slow, through the sleepy trees,
Rest your arms and rest your toes,
Close your eyes, and off it goes.

[Verse 3]
All the friends are tucked in bed,
Pillows soft for every head,
Stars are watching, twinkle, twink,
Sweet dreams now, I think, I think.

[Chorus]
Goodnight, little animals, goodnight,
The moon is glowing, soft and bright,
Close your eyes and snuggle tight,
Goodnight, little animals, goodnight.

[Outro]
Goodnight, little animals. Goodnight.""",
  props={"chorus1": [T("Goodnight, Little Animals", "#ffd88a", size=0.5), P("moon", None, at="top", delay=2)], "verse1": [P("zzz", "sleep", at="right")],
         "chorus2": [T("Goodnight", "#ffd88a", size=0.7)], "verse2": [P("star", "stars", at=[2.6, 2.0, 3.2], opts={"size": 0.4}), P("zzz", "yawns", at="left")],
         "bridge1": [T("Breathe...", "#bfa8ff", "breathe", size=0.6)], "verse3": [P("heart", "dreams", at="right")],
         "chorus3": [T("Goodnight", "#ffd88a", size=0.7)], "outro1": [P("zzz", None, at="right")]},
  meta={"title": "Goodnight Little Animals 🌙 Lullaby for Babies | Moonbeam", "card": "Goodnight, Little Animals", "thumb_text": "GOODNIGHT ANIMALS",
        "description": "Goodnight, Little Animals, a calm lullaby for babies and kids. Say goodnight to the bunny, the lamb, Luna the owl and Teddy as the moon glows and the stars twinkle.\nFun fact: owls stay awake at night! Soft music box and piano with slow breathing to help little ones fall asleep. Ages 0-6.",
        "tags": ["lullaby for babies", "goodnight song", "goodnight little animals", "bedtime song", "sleep music for kids", "baby sleep", "lullabies", "Moonbeam Bedtime", "3D kids songs"]}))

specs.append(dict(id="gz3d_ep05", base="gz3d_ep04",
  lyrics="""[Chorus]
Gizmo makes a rainbow, look, look, look!
Sunlight and water, that's all it took!
Red, orange, yellow, green and blue,
Rainbow, rainbow, I made you!

[Verse 1]
Fill a glass with water, clear and bright,
Put it in the sunny light!
Look at the wall, what do we see?
A little rainbow, wow, whee!

[Verse 2]
Sunlight looks white, but it's hiding a show,
All the colors in a row!
Water bends the light, and then,
The colors spread out, count them again!

[Chorus]
Gizmo makes a rainbow, look, look, look!
Sunlight and water, that's all it took!
Red, orange, yellow, green and blue,
Rainbow, rainbow, I made you!

[Verse 3]
After the rain, when the sun comes out,
Look for a rainbow, round about!
Raindrops bend the light up high,
Painting a rainbow across the sky!

[Bridge]
Arms up high, make a rainbow arch!
Sway to the left, then side to side!
Clap for red and stomp for blue,
Wiggle for purple, rainbow you!

[Chorus]
Gizmo makes a rainbow, look, look, look!
Sunlight and water, that's all it took!
Red, orange, yellow, green and blue,
Rainbow, rainbow, I made you!

[Outro]
Rainbow science! Bye-bye, friends!""",
  props={"chorus1": [T("MAKE A RAINBOW!", "#ff5c8a", size=0.6), P("sun", None, at=[-3.2, 1.2, 3.6], opts={"size": 0.7}, delay=1)],
         "verse1": [P("beaker", "glass", at=[0, 1.0, 3.4]), T("RAINBOW!", "#ff5c8a", "rainbow", size=0.7)],
         "verse2": [P("sun", "sunlight", at=[-3.0, 1.2, 3.6], opts={"size": 0.8}), T("BEND!", "#3b8be0", "bends", size=0.7)],
         "chorus2": [T("MAKE A RAINBOW!", "#ff5c8a", size=0.6)], "verse3": [P("raincloud", "rain", at=[-3.0, 1.2, 3.6], opts={"size": 0.8}), P("sun", "sun", at=[3.0, 1.2, 3.6], opts={"size": 0.7})],
         "bridge1": [T("ARCH!", "#ff5c8a", "arch", at=L("l"), size=0.7), T("SWAY!", "#2fb59a", "sway", at=L("r"), size=0.7), T("WIGGLE!", "#8e5bd8", "wiggle", at=L("c"), size=0.7)],
         "chorus3": [T("MAKE A RAINBOW!", "#ff5c8a", size=0.6)], "outro1": [T("BYE-BYE!", "#3b8be0")]},
  meta={"title": "Gizmo Makes a Rainbow! Science Song for Kids", "card": "Gizmo Makes a Rainbow!", "thumb_text": "MAKE A RAINBOW!",
        "description": "Gizmo makes a rainbow! A science experiment song for kids: put a glass of water in the sunlight and a little rainbow appears.\nKids learn that sunlight holds all the colors and water bends the light to spread them out, just like raindrops do in the sky. Ages 3-6.",
        "tags": ["make a rainbow", "rainbow science for kids", "science song", "experiments for kids", "how rainbows form", "kids songs", "Gizmo Explains", "3D kids songs"]}))

for s in specs:
    base = B3(s["base"]); spec = copy.deepcopy(base)
    spec["lyrics"] = s["lyrics"]; spec["meta"] = s["meta"]; spec["seed"] = base["seed"] + 100
    spec.pop("color_words", None); spec.pop("color_char", None)
    if s.get("colors"): spec["color_words"] = s["colors"]; spec["color_char"] = "host"
    job = spec["job"]; job["id"] = s["id"]; job["song"] = s["id"]; job["title"] = s["meta"]["card"]
    for c in job["cast"]: c.get("opts", {}).pop("color_schedule", None)
    secs = [x["name"] for x in TL.lyric_sections(s["lyrics"])]
    d = {x["section"]: x for x in job["direct"]}; out = []
    for n in secs:
        src = d.get(n) or d[[k for k in d if k.startswith(re.sub(r"\d+$", "", n))][-1]]
        x = copy.deepcopy(src); x["section"] = n; x["props"] = s["props"].get(n, []); out.append(x)
    job["direct"] = out
    assert set(s["props"]) <= set(secs), (s["id"], set(s["props"]) - set(secs))
    assert len(s["meta"]["title"]) <= 60, (s["meta"]["title"], len(s["meta"]["title"]))
    json.dump(spec, open(f"/root/zoo/specs/b5/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]), secs)
