import json, copy, re, sys
sys.path.insert(0, "/root/zoo/blender/zoo3d"); import timing_lib as TL
Z = "/root/zoo/blender/zoo3d"
B3 = lambda n: json.load(open(f"/root/zoo/specs/b5/{n}.song.json"))
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
L = lambda x: [-3.4, 0.3, 3.5] if x == "l" else [3.4, 0.3, 3.5] if x == "r" else [0, 0.6, 4.3]
specs = []

specs.append(dict(id="bl3d_ep11", base="bl3d_ep05", colors={"pink": "#ff6fb5"},
  lyrics="""[Chorus]
Bloop turns pink, pink, pink!
Pinker than you'd ever think!
Pink like candy, pink like a rose,
Pink from his head down to his toes!

[Verse 1]
A pink flamingo stands on one leg,
A pink little piggy, wiggle and beg!
A pink balloon floats up so high,
Pink, pink, pink up in the sky!

[Chorus]
Bloop turns pink, pink, pink!
Pinker than you'd ever think!
Pink like candy, pink like a rose,
Pink from his head down to his toes!

[Verse 2]
Pink strawberry milk, slurp, slurp, slurp,
A pink bubblegum bubble goes burp!
Red and white make pink, it's true,
Mix them up and see it too!

[Bridge]
Stand on one leg like a flamingo, wobble!
Wiggle like a piggy, jiggle and bobble!
Blow a big bubble, puff, puff, pop,
Pink is the color, never stop!

[Verse 3]
Pink flowers blooming in the spring,
Pink is happy, let's all sing!
Pink and purple, pink and blue,
Pink is a color made for you!

[Chorus]
Bloop turns pink, pink, pink!
Pinker than you'd ever think!
Pink like candy, pink like a rose,
Pink from his head down to his toes!

[Outro]
Pink, pink, pink! Bye-bye, friends!""",
  props={"chorus1": [T("PINK!", "#ff6fb5", size=0.9)], "verse1": [P("balloon", "balloon", at=[3.4, 1.4, 3.6], opts={"color": "#ff6fb5"}), T("ONE LEG!", "#ff6fb5", "leg,", at=[-3.4, 1.4, 3.6], size=0.6)],
         "chorus2": [T("PINK!", "#ff6fb5", size=0.9)], "verse2": [T("RED + WHITE = PINK", "#ff6fb5", "white", size=0.45)],
         "bridge1": [T("WOBBLE!", "#ff6fb5", "wobble!", at=L("l"), size=0.6), T("WIGGLE!", "#ff8fc8", "Wiggle", at=L("r"), size=0.6), T("POP!", "#ff3b8b", "pop,", at=L("c"), size=0.8)],
         "verse3": [P("flower", "flowers", at=[-3.4, 0.9, 3.6], opts={"color": "#ff6fb5"}), P("heart", "happy,", at=[3.4, 1.2, 3.6], opts={"color": "#ff6fb5"})],
         "chorus3": [T("PINK!", "#ff6fb5", size=0.9)], "outro1": [T("BYE-BYE!", "#ff6fb5")]},
  meta={"title": "Bloop Turns Pink! Pink Color Song for Kids | Part 6", "card": "Bloop Turns Pink!", "thumb_text": "FLAMINGO TIME!",
        "description": "Bloop turns pink! Part 6 of Bloop's color song series: a pink flamingo, a little piggy, a pink balloon, strawberry milk and spring flowers.\nKids stand on one leg like a flamingo, wiggle like a piggy and learn that red and white make pink. Ages 2-5.",
        "tags": ["pink color song", "learn colors", "color songs for kids", "colors for toddlers", "kids songs", "Bloop's Color Lab", "3D kids songs"]}))

specs.append(dict(id="tt3d_ep11", base="tt3d_ep05",
  lyrics="""[Chorus]
Tow truck, tow truck, here to help!
Hook it up and pull it out!
Beep, beep, beep, don't you worry,
Tow truck's coming in a hurry!

[Verse 1]
A little car got stuck in the mud,
Wheels went spinning, squish and thud!
Who can help? Let's call for one,
Here comes Tow, helping is fun!

[Chorus]
Tow truck, tow truck, here to help!
Hook it up and pull it out!
Beep, beep, beep, don't you worry,
Tow truck's coming in a hurry!

[Verse 2]
Down goes the hook, clank, clank, clank,
Wind up the chain with a crank, crank, crank!
Pull, pull, pull with all his might,
Out comes the car, safe and right!

[Bridge]
Pull the rope, heave, ho!
Pull it again, here we go!
Bend your knees and pull real strong,
Helping friends all day long!

[Verse 3]
The little car says, thank you, Tow!
Off to the garage we go!
When a friend needs help today,
Lend a hand and help them on their way!

[Chorus]
Tow truck, tow truck, here to help!
Hook it up and pull it out!
Beep, beep, beep, don't you worry,
Tow truck's coming in a hurry!

[Outro]
Beep, beep! Bye-bye, trucks!""",
  props={"chorus1": [T("TO THE RESCUE!", "#ffc107", size=0.6)], "verse1": [T("STUCK!", "#8a5a32", "stuck", at=[-2.8, 1.6, 3.6], size=0.7), T("HELP!", "#e8302a", "help?", at=[2.8, 1.6, 3.6], size=0.7)],
         "chorus2": [T("BEEP BEEP!", "#ffc107", size=0.7)], "verse2": [T("CLANK!", "#9e9e9e", "clank,", size=0.7), T("PULL!", "#ffc107", "Pull,", at=L("c"), size=0.8)],
         "bridge1": [T("HEAVE!", "#ffc107", "heave,", at=L("l"), size=0.7), T("HO!", "#e8302a", "ho!", at=L("r"), size=0.8), T("PULL STRONG!", "#3b8be0", "strong,", at=L("c"), size=0.6)],
         "verse3": [T("THANK YOU!", "#e8302a", "thank", size=0.7), T("HELP A FRIEND!", "#2fb54a", "friend", at=L("c"), size=0.55)],
         "chorus3": [T("TO THE RESCUE!", "#ffc107", size=0.6)], "outro1": [T("BYE-BYE!", "#ffc107")]},
  meta={"title": "Tow Truck to the Rescue! Helping Song | Tiny Truck Town", "card": "Tow Truck to the Rescue!", "thumb_text": "STUCK IN MUD!",
        "description": "Oh no, a little car is stuck in the mud! Tow the tow truck drops his hook, cranks the chain and pulls with all his might until the car is safe.\nKids heave-ho and pull along, and learn that helping a friend feels great. Ages 2-5.",
        "tags": ["tow truck song", "trucks for kids", "rescue song", "helping song for kids", "car song", "kids songs", "Tiny Truck Town", "3D kids songs"]}))

specs.append(dict(id="fr3d_ep12", base="fr3d_ep06",
  lyrics="""[Chorus]
From a seed to an apple tree,
Grow, grow, grow with me!
Sun and rain and lots of time,
Apples growing, sweet and fine!

[Verse 1]
Plant a little seed in the ground,
Pat the dirt down, round and round!
Water drops and sunny rays,
Wait and wait for many days!

[Chorus]
From a seed to an apple tree,
Grow, grow, grow with me!
Sun and rain and lots of time,
Apples growing, sweet and fine!

[Verse 2]
Up pops a sprout, tiny and green,
The smallest plant you've ever seen!
It grows a trunk and branches wide,
With leaves and flowers on every side!

[Bridge]
Crouch down low like a little seed,
Stretch up tall like a tree indeed!
Wave your arms like branches, sway,
Grow, grow, grow every day!

[Verse 3]
Flowers turn to apples, red and round,
Pick them gently, don't drop them down!
Crunch, crunch, an apple a day,
Now plant the seeds and grow away!

[Chorus]
From a seed to an apple tree,
Grow, grow, grow with me!
Sun and rain and lots of time,
Apples growing, sweet and fine!

[Outro]
Grow, grow, grow! Bye-bye, fruity friends!""",
  props={"chorus1": [T("SEED TO TREE!", "#3cc45a", size=0.65), P("tree", None, at=[0, 1.6, 3.4], delay=1)],
         "verse1": [T("PLANT!", "#8a5a32", "Plant", at=[-2.6, 1.5, 3.4], size=0.7), P("water_drop", "Water", at=[2.6, 1.2, 3.4]), P("sun", "sunny", at=[0, 2.0, 3.4])],
         "chorus2": [T("GROW!", "#3cc45a", size=0.8)], "verse2": [T("SPROUT!", "#3cc45a", "sprout,", size=0.7), P("tree", "trunk", at=[2.6, 1.2, 3.4])],
         "bridge1": [T("CROUCH!", "#8a5a32", "Crouch", at=L("l"), size=0.6), T("STRETCH!", "#3cc45a", "Stretch", at=L("r"), size=0.6), T("SWAY!", "#ff8a1f", "sway,", at=L("c"), size=0.7)],
         "verse3": [P("bigfruit", "apples,", at=[-2.6, 0.9, 3.4], opts={"kind": "apple"}), T("CRUNCH!", "#e3262b", "Crunch,", at=[2.6, 1.5, 3.4], size=0.7)],
         "chorus3": [T("GROW!", "#3cc45a", size=0.8)], "outro1": [T("BYE-BYE!", "#3cc45a")]},
  meta={"title": "Seed to Apple Tree! Plant Life Cycle Song | Fruity Friends", "card": "Seed to Apple Tree!", "thumb_text": "TINY SEED!",
        "description": "How does an apple grow? The Fruity Friends plant a seed, give it water and sunshine, watch a sprout grow into a tree with flowers, and pick the apples.\nKids crouch like a seed, stretch like a tree and sway like branches. A gentle first look at the plant life cycle. Ages 2-5.",
        "tags": ["plant life cycle song", "how apples grow", "seed to tree", "science for toddlers", "fruit song", "kids songs", "Fruity Friends", "3D kids songs"]}))

specs.append(dict(id="zoo3d_ep11", base="zoo3d_ep05",
  lyrics="""[Chorus]
Where do animals live? Let's see!
Every friend has a home like me!
Big or small, high or low,
Animal homes, let's go, go, go!

[Verse 1]
The lion rests in the tall dry grass,
Watching the savanna friends walk past!
The giraffe stands where the tall trees grow,
Munching leaves from high to low!

[Chorus]
Where do animals live? Let's see!
Every friend has a home like me!
Big or small, high or low,
Animal homes, let's go, go, go!

[Verse 2]
The hippo lives in the river so wide,
Splashing and swimming from side to side!
The zebra runs with the herd all day,
Out on the plains where they love to play!

[Bridge]
Build a nest like a bird, tweet, tweet!
Dig a den with your paws and feet!
Splash in the river, splash, splash, splash,
Run with the herd, dash, dash, dash!

[Verse 3]
The elephant walks with her family near,
Finding water every day of the year!
Milo's nest is up in a tree,
Home, sweet home for you and me!

[Chorus]
Where do animals live? Let's see!
Every friend has a home like me!
Big or small, high or low,
Animal homes, let's go, go, go!

[Outro]
Home, sweet home! Bye-bye, friends!""",
  props={"chorus1": [T("ANIMAL HOMES!", "#ffb627", size=0.65)],
         "verse1": [P("sign", "lion", at=[-3.2, 1.6, 3.6], opts={"text": "GRASS"}), P("sign", "giraffe", at=[3.2, 1.6, 3.6], opts={"text": "TREES"})],
         "chorus2": [T("LET'S GO!", "#ff7a00", size=0.7)],
         "verse2": [P("sign", "hippo", at=[3.2, 1.6, 3.6], opts={"text": "RIVER"}), P("sign", "zebra", at=[-3.2, 1.6, 3.6], opts={"text": "PLAINS"})],
         "bridge1": [T("TWEET!", "#3b8be0", "tweet,", at=L("l"), size=0.6), T("SPLASH!", "#3db7ff", "Splash", at=L("r"), size=0.6), T("DASH!", "#ff7a00", "dash,", at=L("c"), size=0.6)],
         "verse3": [P("heart", "family", at=[0, 1.9, 3.4]), T("NEST!", "#8a5a32", "nest", size=0.7)],
         "chorus3": [T("HOME SWEET HOME!", "#ffb627", size=0.6)], "outro1": [T("BYE-BYE!", "#ffb627")]},
  meta={"title": "Where Do Animals Live? Animal Homes Song with Milo", "card": "Where Do Animals Live?", "thumb_text": "HOME SWEET HOME!",
        "description": "Where do animals live? Milo visits his zoo friends at home: the lion in the tall grass, the giraffe by the tall trees, the hippo in the river, the zebra with the herd on the plains and the elephant with her family.\nKids build a nest, dig a den, splash and run with the herd. Ages 2-5.",
        "tags": ["animal homes song", "where do animals live", "habitats for kids", "safari animals", "animal song for kids", "kids songs", "The Animated Zoo", "Milo", "3D kids songs"]}))

specs.append(dict(id="mb3d_ep11", base="mb3d_ep05",
  lyrics="""[Chorus]
Pitter-patter, pitter-patter, rain is falling down,
Softly on the window, softly on the town,
Cozy in our blankets, warm inside our bed,
Listen to the raindrops, rest your sleepy head.

[Verse 1]
Raindrops on the rooftop, tap, tap, tap,
Bunny's getting sleepy, time to take a nap,
Lamb is snuggled close and Teddy's here too,
The rain is singing softly, just for you.

[Chorus]
Pitter-patter, pitter-patter, rain is falling down,
Softly on the window, softly on the town,
Cozy in our blankets, warm inside our bed,
Listen to the raindrops, rest your sleepy head.

[Verse 2]
Puddles in the garden, flowers drinking deep,
Trees are getting thirsty drinks before they sleep,
Clouds are slowly drifting, gray and soft and slow,
Tomorrow brings a rainbow, glowing as we go.

[Bridge]
Breathe in slowly, like the falling rain,
Breathe out softly, once and once again,
Tap your fingers gently, tap, tap, tap,
Close your eyes now, time to take a nap.

[Verse 3]
The rain is getting quiet, softer than before,
A gentle little whisper, tapping at the door,
Goodnight little raindrops, goodnight sky so gray,
We'll see you in the morning on a brand new day.

[Chorus]
Pitter-patter, pitter-patter, rain is falling down,
Softly on the window, softly on the town,
Cozy in our blankets, warm inside our bed,
Listen to the raindrops, rest your sleepy head.

[Outro]
Pitter-patter. Goodnight.""",
  props={"chorus1": [T("Pitter-Patter", "#bfd8ff", size=0.55)], "verse1": [P("zzz", "nap,", at="right"), P("heart", "Teddy's", at="left")],
         "chorus2": [P("zzz", "sleepy", at="right")], "verse2": [P("moon", "Clouds", at="top")],
         "bridge1": [T("Breathe...", "#bfa8ff", "Breathe", size=0.6)], "verse3": [P("heart", "Goodnight", at="right")],
         "outro1": [P("zzz", "Goodnight.", at="right")]},
  meta={"title": "Pitter-Patter Rain 🌙 Sleepy Lullaby for Babies | Moonbeam", "card": "Pitter-Patter Rain", "thumb_text": "COZY RAINY NIGHT",
        "description": "A soothing rainy-night lullaby. Luna, Bunny, Lamb and Teddy snuggle in their blankets and listen to the raindrops tapping on the window as the garden drinks and the clouds drift by.\nA slow breathing break helps little ones relax and fall asleep. For babies and toddlers.",
        "tags": ["rain lullaby", "rain sounds for sleep", "lullaby for babies", "bedtime song", "sleep music for kids", "Moonbeam Bedtime", "3D kids songs"]}))

specs.append(dict(id="gz3d_ep11", base="gz3d_ep05",
  lyrics="""[Chorus]
Spring, summer, fall and winter too,
Four seasons, each one new!
The Earth goes round the sun all year,
That's why the seasons change right here!

[Verse 1]
The Earth is tilted, leaning a bit,
As it travels round, the sun shines on it!
When our side leans toward the sun so bright,
It's summer, with long days of light!

[Chorus]
Spring, summer, fall and winter too,
Four seasons, each one new!
The Earth goes round the sun all year,
That's why the seasons change right here!

[Verse 2]
When our side leans away, it's cold,
Winter comes with snow, I'm told!
Spring brings flowers, warm and new,
Fall brings leaves in orange too!

[Bridge]
Lean to the left, lean to the right,
Tilt like the Earth in the warm sunlight!
Spin around and round you go,
One trip round the sun, now you know!

[Verse 3]
One trip round the sun takes a year,
Every season comes back, never fear!
Snow and flowers, sun and leaves,
The tilted Earth gives all of these!

[Chorus]
Spring, summer, fall and winter too,
Four seasons, each one new!
The Earth goes round the sun all year,
That's why the seasons change right here!

[Outro]
Four seasons! Bye-bye, friends!""",
  props={"chorus1": [T("4 SEASONS!", "#3b8be0", size=0.8), P("sun", None, at=[-3.2, 1.3, 3.6], opts={"size": 0.7}, delay=1)],
         "verse1": [T("TILTED!", "#ff8a1f", "tilted,", size=0.7), P("sun", "sun", at=[-3.0, 1.3, 3.6], opts={"size": 0.8})],
         "chorus2": [T("SPRING SUMMER FALL WINTER", "#3b8be0", size=0.4)], "verse2": [T("WINTER!", "#7fd3ff", "Winter", at=L("l"), size=0.6), T("SPRING!", "#3cc45a", "Spring", at=L("r"), size=0.6)],
         "bridge1": [T("LEAN!", "#ff8a1f", "Lean", at=L("l"), size=0.7), T("TILT!", "#3b8be0", "Tilt", at=L("r"), size=0.7), T("SPIN!", "#8e5bd8", "Spin", at=L("c"), size=0.7)],
         "verse3": [T("1 YEAR!", "#ffc107", "year,", size=0.7)],
         "chorus3": [T("4 SEASONS!", "#3b8be0", size=0.8)], "outro1": [T("BYE-BYE!", "#3b8be0")]},
  meta={"title": "Why Do We Have Seasons? Science Song for Kids with Gizmo", "card": "Why Seasons?", "thumb_text": "EARTH TILTS!",
        "description": "Why do we have seasons? Gizmo the robot explains that the Earth is tilted. As it travels around the sun over a year, our side leans toward the sun for summer and away from it for winter, with spring and fall in between.\nKids lean, tilt and spin like the Earth. Ages 3-6.",
        "tags": ["seasons song for kids", "why do we have seasons", "four seasons", "earth tilt", "science song for kids", "kids songs", "Gizmo Explains", "3D kids songs"]}))
for s in specs:
    base = B3(s["base"]); spec = copy.deepcopy(base)
    spec["lyrics"] = s["lyrics"]; spec["meta"] = s["meta"]; spec["seed"] = base["seed"] + 600
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
    json.dump(spec, open(f"/root/zoo/specs/b11/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]), secs)
