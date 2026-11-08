import json, copy, re, sys
sys.path.insert(0, "/root/zoo/blender/zoo3d"); import timing_lib as TL
Z = "/root/zoo/blender/zoo3d"
B3 = lambda n: json.load(open(f"/root/zoo/specs/b5/{n}.song.json"))
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
L = lambda x: [-3.4, 0.3, 3.5] if x == "l" else [3.4, 0.3, 3.5] if x == "r" else [0, 0.6, 4.3]
specs = []

specs.append(dict(id="bl3d_ep10", base="bl3d_ep05", colors={"purple": "#8e3fd0"},
  lyrics="""[Chorus]
Bloop turns purple, purple, purple!
Purple, purple, round in a circle!
Red and blue, mix them, see?
Purple is magic, one, two, three!

[Verse 1]
Purple grapes in a bunch so sweet,
Purple grapes, a yummy treat!
A purple flower, a purple shoe,
Purple, purple, I see you!

[Chorus]
Bloop turns purple, purple, purple!
Purple, purple, round in a circle!
Red and blue, mix them, see?
Purple is magic, one, two, three!

[Verse 2]
A purple crayon, draw a line,
A purple balloon, isn't it fine?
A purple butterfly flutters by,
Purple wings up in the sky!

[Bridge]
Find something purple, point and say,
Purple, purple, hip hooray!
Spin around and touch your knees,
Purple is the color, if you please!

[Verse 3]
Red plus blue makes purple, true,
Mix it up, you can do it too!
Purple, purple, all day long,
Sing along with Bloop's purple song!

[Chorus]
Bloop turns purple, purple, purple!
Purple, purple, round in a circle!
Red and blue, mix them, see?
Purple is magic, one, two, three!

[Outro]
Purple, purple! Bye-bye, friends!""",
  props={"chorus1": [T("PURPLE!", "#8e3fd0", size=0.9)], "verse1": [P("grapes", "grapes", at=[-3.4, 0.9, 3.6]), P("flower", "flower,", at=[3.4, 0.9, 3.6], opts={"color": "#8e3fd0"})],
         "chorus2": [T("RED + BLUE = PURPLE", "#8e3fd0", "Red", size=0.45)], "verse2": [P("crayon", "crayon,", at=[-3.4, 0.9, 3.6], opts={"color": "#8e3fd0"}), P("balloon", "balloon,", at=[3.4, 1.4, 3.6], opts={"color": "#8e3fd0"})],
         "bridge1": [T("FIND PURPLE!", "#8e3fd0", "Find", size=0.7), T("HOORAY!", "#ffd21f", "hooray,", at=L("c"), size=0.7)],
         "verse3": [T("RED + BLUE = PURPLE", "#8e3fd0", "plus", size=0.45)],
         "chorus3": [T("PURPLE!", "#8e3fd0", size=0.9)], "outro1": [T("BYE-BYE!", "#8e3fd0")]},
  meta={"title": "Bloop Turns Purple! Purple Color Song for Kids | Part 5", "card": "Bloop Turns Purple!", "thumb_text": "BLOOP TURNS PURPLE!",
        "description": "Bloop turns purple! Part 5 of Bloop's color song series: purple grapes, a purple flower, a purple crayon and balloon, and a purple butterfly.\nKids find something purple and learn that red and blue mix to make purple. Ages 2-5.",
        "tags": ["purple color song", "learn colors", "color mixing for kids", "colors for toddlers", "kids songs", "Bloop's Color Lab", "3D kids songs"]}))

specs.append(dict(id="tt3d_ep10", base="tt3d_ep05",
  lyrics="""[Chorus]
Wash, wash, truck wash, splish, splash, splosh!
Bubbles and suds, it's time to wash!
Scrub, scrub, rinse and shine,
Clean trucks looking fine!

[Verse 1]
Muddy wheels from a muddy road,
Bolt the fire truck had a heavy load!
Into the truck wash, here we go,
Water spraying, to and fro!

[Chorus]
Wash, wash, truck wash, splish, splash, splosh!
Bubbles and suds, it's time to wash!
Scrub, scrub, rinse and shine,
Clean trucks looking fine!

[Verse 2]
Big round brushes spinning around,
Swish, swish, swish, what a sound!
Soap on the windows, soap on the door,
Bubbles on the roof and on the floor!

[Bridge]
Scrub your arms, scrub, scrub, scrub!
Rinse your hands, rub, rub, rub!
Shake it dry, shake, shake, shake,
Shiny and clean, no mistake!

[Verse 3]
Out comes Bolt, shiny and red,
Sparkly bright from wheels to head!
Honk, honk, thank you, truck wash crew,
Now my trucks look good as new!

[Chorus]
Wash, wash, truck wash, splish, splash, splosh!
Bubbles and suds, it's time to wash!
Scrub, scrub, rinse and shine,
Clean trucks looking fine!

[Outro]
Splish, splash! Bye-bye, trucks!""",
  props={"chorus1": [T("SPLISH SPLASH!", "#3b8be0", size=0.7), P("water", None, at=[0, 1.6, 3.4], delay=1)],
         "verse1": [T("MUDDY!", "#8a5a32", "Muddy", at=[-2.8, 1.6, 3.6], size=0.7), P("water", "spraying,", at=[2.8, 1.6, 3.6])],
         "chorus2": [T("SCRUB!", "#3b8be0", size=0.8)], "verse2": [T("SWISH!", "#3b8be0", "Swish,", size=0.7), T("BUBBLES!", "#7fd3ff", "Bubbles", at=L("c"), size=0.6)],
         "bridge1": [T("SCRUB!", "#3b8be0", "Scrub", at=L("l"), size=0.7), T("RINSE!", "#7fd3ff", "Rinse", at=L("r"), size=0.7), T("SHAKE!", "#ffc107", "Shake", at=L("c"), size=0.7)],
         "verse3": [T("SHINY!", "#ffc107", "shiny", size=0.7), T("THANK YOU!", "#e8302a", "thank", at=L("c"), size=0.6)],
         "chorus3": [T("SPLISH SPLASH!", "#3b8be0", size=0.7)], "outro1": [T("BYE-BYE!", "#3b8be0")]},
  meta={"title": "Truck Wash Song! Splish Splash Trucks | Tiny Truck Town", "card": "Truck Wash Song!", "thumb_text": "TRUCK WASH!",
        "description": "Splish, splash, splosh! After a muddy day, Bolt the fire truck and friends go through the truck wash: water sprays, big brushes spin and bubbles cover everything.\nKids scrub, rinse and shake dry along with the trucks. Ages 2-5.",
        "tags": ["truck wash song", "car wash song for kids", "fire truck song", "trucks for kids", "bath song", "kids songs", "Tiny Truck Town", "3D kids songs"]}))

specs.append(dict(id="fr3d_ep11", base="fr3d_ep06",
  lyrics="""[Chorus]
Make a smoothie, whirr, whirr, whirr!
Fruit goes in and round they stir!
Blend it up, pour it out,
Smoothie time, let's sing and shout!

[Verse 1]
In goes banana, peel it first,
In go berries, ready to burst!
A splash of milk, a spoon of yogurt,
Smoothie, smoothie, here's the best part!

[Chorus]
Make a smoothie, whirr, whirr, whirr!
Fruit goes in and round they stir!
Blend it up, pour it out,
Smoothie time, let's sing and shout!

[Verse 2]
Strawberry pink and mango gold,
Blend it smooth and nice and cold!
Ask a grown-up to press the button,
Safety first, now watch it spin!

[Bridge]
Spin around like a blender, whirr!
Shake your hips, give it a stir!
Pour it slowly, glug, glug, glug,
Take a sip from your smoothie mug!

[Verse 3]
Fruit gives energy to run and play,
A healthy snack for any day!
Share your smoothie with a friend,
Yummy, yummy, to the end!

[Chorus]
Make a smoothie, whirr, whirr, whirr!
Fruit goes in and round they stir!
Blend it up, pour it out,
Smoothie time, let's sing and shout!

[Outro]
Whirr, whirr, whirr! Bye-bye, fruity friends!""",
  props={"chorus1": [T("WHIRR!", "#ff5c8a", size=0.8)],
         "verse1": [P("bigfruit", "banana,", at=[-2.6, 0.9, 3.4], opts={"kind": "banana"}), P("bigfruit", "berries,", at=[2.6, 0.9, 3.4], opts={"kind": "strawberry"})],
         "chorus2": [T("BLEND IT!", "#ff8a1f", size=0.7)], "verse2": [P("bigfruit", "Strawberry", at=[-2.6, 0.9, 3.4], opts={"kind": "strawberry"}), T("ASK A GROWN-UP!", "#3b8be0", "grown-up", at=L("c"), size=0.5)],
         "bridge1": [T("SPIN!", "#ff5c8a", "Spin", at=L("l"), size=0.7), T("SHAKE!", "#ff8a1f", "Shake", at=L("r"), size=0.7), T("GLUG GLUG!", "#3cc45a", "glug,", at=L("c"), size=0.6)],
         "verse3": [T("ENERGY!", "#ffc107", "energy", size=0.7), P("heart", "Share", at=[0, 1.8, 3.4])],
         "chorus3": [T("WHIRR!", "#ff5c8a", size=0.8)], "outro1": [T("BYE-BYE!", "#ff5c8a")]},
  meta={"title": "Make a Smoothie Song! Healthy Snack | Fruity Friends", "card": "Make a Smoothie!", "thumb_text": "SMOOTHIE TIME!",
        "description": "Whirr, whirr, whirr! The Fruity Friends make a smoothie: in go bananas, berries, mango, milk and yogurt, then a grown-up presses the blender button.\nKids spin like a blender, pour it slowly and learn that fruit gives energy to play. Ages 2-5.",
        "tags": ["smoothie song", "healthy snack song", "fruit song for kids", "healthy eating", "kids songs", "Fruity Friends", "3D kids songs"]}))

specs.append(dict(id="zoo3d_ep10", base="zoo3d_ep05",
  lyrics="""[Chorus]
Who's hiding in the savanna? Peekaboo!
Who's hiding in the grass? Is it you?
Look, look, look around,
A zoo friend will be found!

[Verse 1]
I see a mane, big and gold,
A mighty roar, brave and bold!
Peekaboo, who could it be?
It's the lion, smiling at me!

[Chorus]
Who's hiding in the savanna? Peekaboo!
Who's hiding in the grass? Is it you?
Look, look, look around,
A zoo friend will be found!

[Verse 2]
I see a neck, so long and tall,
Munching leaves, the tallest of all!
Peekaboo, who could it be?
It's the giraffe up by the tree!

[Bridge]
Cover your eyes, one, two, three,
Open them up, what do you see?
Hide behind your hands so small,
Peekaboo! We found them all!

[Verse 3]
I see stripes, black and white,
And a hippo, splashing bright!
Big gray ears go flap, flap, flap,
The elephant joins the clap, clap, clap!

[Chorus]
Who's hiding in the savanna? Peekaboo!
Who's hiding in the grass? Is it you?
Look, look, look around,
A zoo friend will be found!

[Outro]
Peekaboo! Bye-bye, friends!""",
  props={"chorus1": [T("PEEKABOO!", "#ffb627", size=0.8)],
         "verse1": [P("sign", "lion,", at=[-3.2, 1.6, 3.6], opts={"text": "LION"})],
         "chorus2": [T("PEEKABOO!", "#ff7a00", size=0.8)],
         "verse2": [P("sign", "giraffe", at=[3.2, 1.6, 3.6], opts={"text": "GIRAFFE"})],
         "bridge1": [T("1, 2, 3...", "#ffb627", "Cover", size=0.6), T("PEEKABOO!", "#ff7a00", "Peekaboo!", at=L("c"), size=0.8)],
         "verse3": [P("sign", "stripes,", at=[-3.2, 1.6, 3.6], opts={"text": "ZEBRA"}), P("sign", "hippo,", at=[3.2, 1.6, 3.6], opts={"text": "HIPPO"})],
         "chorus3": [T("PEEKABOO!", "#ffb627", size=0.8)], "outro1": [T("BYE-BYE!", "#ffb627")]},
  meta={"title": "Peekaboo Animals! Hide and Seek Song for Kids with Milo", "card": "Peekaboo Animals!", "thumb_text": "PEEKABOO!",
        "description": "Peekaboo! Milo plays hide and seek in the savanna. Kids guess each hidden friend from clues: a golden mane, a long tall neck, black and white stripes, a splashing hippo and big flapping ears.\nKids cover their eyes, count to three and shout peekaboo. Ages 1-4.",
        "tags": ["peekaboo song", "hide and seek song", "animal guessing game", "safari animals", "baby songs", "kids songs", "The Animated Zoo", "Milo", "3D kids songs"]}))

specs.append(dict(id="mb3d_ep10", base="mb3d_ep05",
  lyrics="""[Chorus]
Goodnight moon and goodnight stars,
Goodnight sky, near and far,
Goodnight room, so warm and still,
Goodnight trees upon the hill.

[Verse 1]
Goodnight lamp, it's time to rest,
Goodnight teddy, you're the best,
Goodnight window, goodnight door,
Goodnight toys upon the floor.

[Chorus]
Goodnight moon and goodnight stars,
Goodnight sky, near and far,
Goodnight room, so warm and still,
Goodnight trees upon the hill.

[Verse 2]
Goodnight Bunny, snuggled tight,
Goodnight Lamb, sleep well tonight,
Goodnight Owl up in the tree,
Goodnight, goodnight, from you and me.

[Bridge]
Breathe in slow, the day is done,
Breathe out soft, goodnight sun,
Close your eyes and rest your head,
Cozy, cozy in your bed.

[Verse 3]
Goodnight Mommy, goodnight Dad,
Thank you for the day we had,
Tomorrow brings a brand new day,
But now it's time to drift away.

[Chorus]
Goodnight moon and goodnight stars,
Goodnight sky, near and far,
Goodnight room, so warm and still,
Goodnight trees upon the hill.

[Outro]
Goodnight, goodnight. Sweet dreams.""",
  props={"chorus1": [T("Goodnight", "#ffd88a", size=0.55), P("moon", None, at="top", delay=2)], "verse1": [P("heart", "teddy,", at="right"), P("zzz", "rest,", at="left")],
         "chorus2": [P("numstar", "stars,", at="left", opts={"size": 0.4})], "verse2": [P("heart", "Bunny,", at="right"), P("zzz", "Owl", at="left")],
         "bridge1": [T("Breathe...", "#bfa8ff", "Breathe", size=0.6)], "verse3": [P("heart", "Thank", at="right")],
         "outro1": [P("zzz", "dreams.", at="right")]},
  meta={"title": "Goodnight Everything 🌙 Calm Bedtime Lullaby | Moonbeam", "card": "Goodnight Everything", "thumb_text": "GOODNIGHT",
        "description": "A calm bedtime lullaby where Luna, Bunny and Lamb say goodnight to the moon, the stars, the lamp, the toys and everyone they love.\nA slow breathing break helps little ones settle down and drift off to sleep. For babies and toddlers.",
        "tags": ["goodnight song", "bedtime lullaby", "lullaby for babies", "sleep music for kids", "calming bedtime song", "Moonbeam Bedtime", "3D kids songs"]}))

specs.append(dict(id="gz3d_ep10", base="gz3d_ep05",
  lyrics="""[Chorus]
Boom, boom, my heart goes boom!
Pumping blood in every room!
Thump, thump, all day long,
My heart is beating, big and strong!

[Verse 1]
Put your hand upon your chest,
Feel the beat, it never rests!
Your heart's about the size of your fist,
A super pump that can't be missed!

[Chorus]
Boom, boom, my heart goes boom!
Pumping blood in every room!
Thump, thump, all day long,
My heart is beating, big and strong!

[Verse 2]
Blood goes round from head to toes,
Up and down your body it flows!
It carries air your body needs,
That's how your heart helps you succeed!

[Bridge]
Jump, jump, jump up high!
Feel your heart beat fast, oh my!
Now sit down and breathe so slow,
Your heartbeat slows down, now you know!

[Verse 3]
Healthy food and lots of play,
Keep your heart strong every day!
Running, dancing, jumping too,
A happy heart is good for you!

[Chorus]
Boom, boom, my heart goes boom!
Pumping blood in every room!
Thump, thump, all day long,
My heart is beating, big and strong!

[Outro]
Boom, boom! Bye-bye, friends!""",
  props={"chorus1": [T("BOOM BOOM!", "#e53935", size=0.8), P("heart", None, at=[-3.0, 1.4, 3.6], delay=1)],
         "verse1": [T("FEEL THE BEAT!", "#e53935", "Feel", size=0.6), T("FIST SIZE!", "#ff8a1f", "fist,", at=L("c"), size=0.6)],
         "chorus2": [T("THUMP THUMP!", "#e53935", size=0.7)], "verse2": [T("HEAD TO TOES!", "#3b8be0", "toes,", size=0.6)],
         "bridge1": [T("JUMP!", "#ffc107", "Jump,", at=L("l"), size=0.8), T("FAST!", "#e53935", "fast,", at=L("r"), size=0.7), T("SLOW...", "#3b8be0", "slow,", at=L("c"), size=0.6)],
         "verse3": [T("PLAY!", "#3cc45a", "play,", size=0.7), P("heart", "happy", at=[3.0, 1.4, 3.6])],
         "chorus3": [T("BOOM BOOM!", "#e53935", size=0.8)], "outro1": [T("BYE-BYE!", "#e53935")]},
  meta={"title": "How Does Your Heart Work? Body Song for Kids with Gizmo", "card": "Your Heart!", "thumb_text": "BOOM BOOM HEART!",
        "description": "Boom, boom! Gizmo the robot explains the heart: it's about the size of your fist and pumps blood from your head to your toes, carrying the air your body needs.\nKids feel their heartbeat, jump to make it go fast, sit to slow it down and learn that play and healthy food keep the heart strong. Ages 3-6.",
        "tags": ["heart song for kids", "human body song", "how the heart works", "science song for kids", "body parts", "kids songs", "Gizmo Explains", "3D kids songs"]}))
for s in specs:
    base = B3(s["base"]); spec = copy.deepcopy(base)
    spec["lyrics"] = s["lyrics"]; spec["meta"] = s["meta"]; spec["seed"] = base["seed"] + 500
    spec.pop("color_words", None); spec.pop("color_char", None)
    if s.get("colors"): spec["color_words"] = s["colors"]; spec["color_char"] = "host"
    job = spec["job"]; job["id"] = s["id"]; job["song"] = s["id"]; job["title"] = s["meta"]["card"]
    for c in job["cast"]: c.get("opts", {}).pop("color_schedule", None)
    secs = [x["name"] for x in TL.lyric_sections(s["lyrics"])]
    d = {x["section"]: x for x in job["direct"]}; out = []
    for n in secs:
        m = [k for k in d if k.startswith(re.sub(r"\d+$", "", n))] or [k for k in d if k.startswith("verse")] or [k for k in d if not re.match(r"(chorus|bridge|outro|intro)", k)][:1]
        src = d.get(n) or d[m[-1]]
        x = copy.deepcopy(src); x["section"] = n; x["props"] = s["props"].get(n, []); out.append(x)
    job["direct"] = out
    assert set(s["props"]) <= set(secs), (s["id"], set(s["props"]) - set(secs))
    assert len(s["meta"]["title"]) <= 60, (s["meta"]["title"], len(s["meta"]["title"]))
    json.dump(spec, open(f"/root/zoo/specs/b10/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]), secs)
