import json, copy, re, sys
sys.path.insert(0, "/root/zoo/blender/zoo3d"); import timing_lib as TL
Z = "/root/zoo/blender/zoo3d"
B3 = lambda n: json.load(open(f"/root/zoo/specs/b5/{n}.song.json"))
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
L = lambda x: [-3.4, 0.3, 3.5] if x == "l" else [3.4, 0.3, 3.5] if x == "r" else [0, 0.6, 4.3]
specs = []

specs.append(dict(id="bl3d_ep13", base="bl3d_ep05", colors={"red": "#ff3b3b", "orange": "#ff8a1f", "yellow": "#ffd21f", "green": "#3cc45a", "blue": "#3b8be0", "purple": "#8e3fd0", "pink": "#ff6fb5"},
  lyrics="""[Chorus]
Rainbow Bloop, rainbow Bloop,
Changing colors, loop-de-loop!
Every color, one by one,
Rainbow Bloop is so much fun!

[Verse 1]
First he's red like a fire truck,
Then he's orange, what good luck!
Yellow like a sunny day,
Green like grass where we can play!

[Chorus]
Rainbow Bloop, rainbow Bloop,
Changing colors, loop-de-loop!
Every color, one by one,
Rainbow Bloop is so much fun!

[Verse 2]
Blue like the ocean, deep and wide,
Purple like grapes, he jumps with pride!
Pink like a flamingo, standing tall,
Bloop has turned into them all!

[Bridge]
Shout a color, red, red, red!
Touch something green, now touch your head!
Find something blue and wave hello,
Rainbow colors, here we go!

[Verse 3]
Red and orange, yellow and green,
Blue and purple, the best I've seen!
Pink at the end, now count with me,
Seven colors, one, two, three!

[Chorus]
Rainbow Bloop, rainbow Bloop,
Changing colors, loop-de-loop!
Every color, one by one,
Rainbow Bloop is so much fun!

[Outro]
Rainbow Bloop! Bye-bye, friends!""",
  props={"chorus1": [T("RAINBOW!", "#ff6fb5", size=0.8), P("rainbow", None, at=[0, 1.9, 3.4], delay=1)],
         "verse1": [T("RED!", "#ff3b3b", "red", at=[-3.4, 1.4, 3.6], size=0.6), T("GREEN!", "#3cc45a", "Green", at=[3.4, 1.4, 3.6], size=0.6)],
         "chorus2": [P("rainbow", None, at=[0, 1.9, 3.4], delay=1)], "verse2": [T("BLUE!", "#3b8be0", "Blue", at=[-3.4, 1.4, 3.6], size=0.6), T("PINK!", "#ff6fb5", "Pink", at=[3.4, 1.4, 3.6], size=0.6)],
         "bridge1": [T("SHOUT A COLOR!", "#ff8a1f", "Shout", size=0.55), T("HELLO!", "#3b8be0", "hello,", at=L("c"), size=0.7)],
         "verse3": [T("7 COLORS!", "#8e3fd0", "Seven", size=0.7)],
         "chorus3": [T("RAINBOW!", "#ff6fb5", size=0.8)], "outro1": [T("BYE-BYE!", "#3b8be0")]},
  meta={"title": "Rainbow Bloop! 7 Colors Song for Kids | Color Review", "card": "Rainbow Bloop!", "thumb_text": "7 COLORS!",
        "description": "Bloop turns every color of the rainbow! A review of the whole color series: red like a fire truck, orange, sunny yellow, green grass, blue ocean, purple grapes and a pink flamingo.\nKids shout colors, touch something green and find something blue. Ages 2-5.",
        "tags": ["rainbow colors song", "learn colors", "color songs for kids", "colors for toddlers", "kids songs", "Bloop's Color Lab", "3D kids songs"]}))

specs.append(dict(id="tt3d_ep13", base="tt3d_ep05",
  lyrics="""[Chorus]
School bus, school bus, big and yellow,
Beep, beep, beep, say hi to every fellow!
Sit down tight and ride along,
School bus, school bus, sing this song!

[Verse 1]
Wait on the sidewalk, stand in line,
Here comes the bus, right on time!
Step up slowly, one, two, three,
Find a seat, there's room for me!

[Chorus]
School bus, school bus, big and yellow,
Beep, beep, beep, say hi to every fellow!
Sit down tight and ride along,
School bus, school bus, sing this song!

[Verse 2]
The stop sign swings out, red and bright,
Cars must stop, that's the rule, that's right!
Stay in your seat, keep your hands inside,
Safe and happy on the ride!

[Bridge]
Wave to the driver, hello, hello!
Bounce in your seat as the wheels go slow!
Look out the window, what do you see?
Friends and trees and the school for me!

[Verse 3]
Here's the school, the doors swing wide,
Walk down the steps, then go inside!
Thank you, driver, see you soon,
We'll ride back home this afternoon!

[Chorus]
School bus, school bus, big and yellow,
Beep, beep, beep, say hi to every fellow!
Sit down tight and ride along,
School bus, school bus, sing this song!

[Outro]
Beep, beep! Bye-bye, trucks!""",
  props={"chorus1": [T("SCHOOL BUS!", "#ffc107", size=0.7)], "verse1": [T("WAIT IN LINE!", "#3b8be0", "line,", size=0.55), T("1, 2, 3!", "#2fb54a", "slowly,", at=L("c"), size=0.6)],
         "chorus2": [T("BEEP BEEP!", "#ffc107", size=0.7)], "verse2": [T("STOP!", "#e8302a", "stop", size=0.8), T("STAY SEATED!", "#3b8be0", "Stay", at=L("c"), size=0.55)],
         "bridge1": [T("HELLO!", "#ffc107", "Wave", at=L("l"), size=0.6), T("BOUNCE!", "#ff8a1f", "Bounce", at=L("r"), size=0.6)],
         "verse3": [T("THANK YOU!", "#e8302a", "Thank", size=0.7)],
         "chorus3": [T("SCHOOL BUS!", "#ffc107", size=0.7)], "outro1": [T("BYE-BYE!", "#ffc107")]},
  meta={"title": "School Bus Song! Bus Safety for Kids | Tiny Truck Town", "card": "School Bus Song!", "thumb_text": "STAY SEATED!",
        "description": "Beep, beep! The big yellow school bus picks up the kids of Tiny Truck Town. Kids learn to wait in line on the sidewalk, step up slowly, stay in their seat, keep their hands inside and say thank you to the driver.\nWhen the red stop sign swings out, cars must stop. Ages 2-5.",
        "tags": ["school bus song", "bus safety for kids", "trucks for kids", "school song", "kids songs", "Tiny Truck Town", "3D kids songs"]}))

specs.append(dict(id="fr3d_ep14", base="fr3d_ep06",
  lyrics="""[Chorus]
Good morning, good morning, time to eat!
A healthy breakfast can't be beat!
Fruit and grains and a glass of milk,
Start the day as smooth as silk!

[Verse 1]
Rise and shine, the sun is up,
Pour some milk into my cup!
A bowl of oats, warm and sweet,
Sprinkle berries, what a treat!

[Chorus]
Good morning, good morning, time to eat!
A healthy breakfast can't be beat!
Fruit and grains and a glass of milk,
Start the day as smooth as silk!

[Verse 2]
Slice a banana, round and round,
Crunchy toast, a golden brown!
An apple slice, a yummy bite,
Breakfast makes me feel just right!

[Bridge]
Stretch your arms up, good morning sun!
Rub your tummy, breakfast is done!
Jump up high, you're full of power,
Ready to play for hour and hour!

[Verse 3]
Breakfast gives you energy,
To learn and play and run with glee!
Say thank you for the food today,
Now we're ready, hip hooray!

[Chorus]
Good morning, good morning, time to eat!
A healthy breakfast can't be beat!
Fruit and grains and a glass of milk,
Start the day as smooth as silk!

[Outro]
Good morning! Bye-bye, fruity friends!""",
  props={"chorus1": [T("GOOD MORNING!", "#ff8a1f", size=0.65), P("sun", None, at=[0, 1.9, 3.4], delay=1)],
         "verse1": [P("bigfruit", "berries,", at=[2.6, 0.9, 3.4], opts={"kind": "strawberry"}), T("RISE & SHINE!", "#ffc107", "Rise", at=[-2.6, 1.5, 3.4], size=0.55)],
         "chorus2": [T("YUM!", "#ff8a1f", size=0.8)], "verse2": [P("bigfruit", "banana,", at=[-2.6, 0.9, 3.4], opts={"kind": "banana"}), P("bigfruit", "apple", at=[2.6, 0.9, 3.4], opts={"kind": "apple"})],
         "bridge1": [T("STRETCH!", "#ffc107", "Stretch", at=L("l"), size=0.6), T("JUMP!", "#ff5c8a", "Jump", at=L("r"), size=0.7), T("POWER!", "#3cc45a", "power,", at=L("c"), size=0.6)],
         "verse3": [T("ENERGY!", "#ffc107", "energy,", size=0.7), P("plate", "food", at=[0, 0.8, 3.4])],
         "chorus3": [T("GOOD MORNING!", "#ff8a1f", size=0.65)], "outro1": [T("BYE-BYE!", "#ff8a1f")]},
  meta={"title": "Good Morning Breakfast Song! Healthy Food | Fruity Friends", "card": "Breakfast Song!", "thumb_text": "RISE & SHINE!",
        "description": "Good morning! The Fruity Friends make a healthy breakfast: warm oats with berries, banana slices, crunchy toast, apple slices and a cup of milk.\nKids stretch to the morning sun, rub their tummies and learn that breakfast gives energy to learn and play. Ages 2-5.",
        "tags": ["breakfast song for kids", "good morning song", "healthy eating song", "morning routine", "kids songs", "Fruity Friends", "3D kids songs"]}))

specs.append(dict(id="zoo3d_ep13", base="zoo3d_ep05",
  lyrics="""[Chorus]
What do we call the baby, baby?
Every animal baby has a name, maybe!
Cub and calf and foal, it's true,
Baby animals, just like you!

[Verse 1]
A baby lion is called a cub,
Roaring small with a playful rub!
A baby elephant is called a calf,
Swinging its trunk, it makes us laugh!

[Chorus]
What do we call the baby, baby?
Every animal baby has a name, maybe!
Cub and calf and foal, it's true,
Baby animals, just like you!

[Verse 2]
A baby zebra is called a foal,
Wobbly legs out on a stroll!
A baby giraffe is a calf too,
Already taller than me and you!

[Bridge]
Roar like a cub, roar, roar, roar!
Wobble like a foal across the floor!
Swing your arm like a calf's small trunk,
Stomp, stomp, stomp, ka-plunk!

[Verse 3]
A baby hippo is a calf as well,
Swimming close to Mom, she knows it well!
Milo was once a chick so small,
Now he's singing with you all!

[Chorus]
What do we call the baby, baby?
Every animal baby has a name, maybe!
Cub and calf and foal, it's true,
Baby animals, just like you!

[Outro]
Cub, calf, foal! Bye-bye, friends!""",
  props={"chorus1": [T("BABY NAMES!", "#ffb627", size=0.7)],
         "verse1": [P("sign", "cub,", at=[-3.2, 1.6, 3.6], opts={"text": "CUB"}), P("sign", "calf,", at=[3.2, 1.6, 3.6], opts={"text": "CALF"})],
         "chorus2": [T("CUB! CALF! FOAL!", "#ff7a00", size=0.6)],
         "verse2": [P("sign", "foal,", at=[-3.2, 1.6, 3.6], opts={"text": "FOAL"}), P("sign", "calf", at=[3.2, 1.6, 3.6], opts={"text": "CALF"})],
         "bridge1": [T("ROAR!", "#ffb627", "Roar", at=L("l"), size=0.7), T("WOBBLE!", "#333333", "Wobble", at=L("r"), size=0.6), T("STOMP!", "#8a5a32", "Stomp,", at=L("c"), size=0.6)],
         "verse3": [P("sign", "hippo", at=[3.2, 1.6, 3.6], opts={"text": "CALF"}), P("sign", "chick", at=[-3.2, 1.6, 3.6], opts={"text": "CHICK"})],
         "chorus3": [T("BABY NAMES!", "#ffb627", size=0.7)], "outro1": [T("BYE-BYE!", "#ffb627")]},
  meta={"title": "Baby Animal Names! Cub, Calf, Foal Song for Kids with Milo", "card": "Baby Animal Names!", "thumb_text": "WHAT'S MY NAME?",
        "description": "What do we call baby animals? Milo and friends learn the names: a baby lion is a cub, a baby elephant, giraffe or hippo is a calf, a baby zebra is a foal, and a baby bird like Milo is a chick.\nKids roar like a cub, wobble like a foal and stomp like a calf. Ages 2-5.",
        "tags": ["baby animal names", "cub calf foal", "baby animals song", "animal song for kids", "safari animals", "kids songs", "The Animated Zoo", "Milo", "3D kids songs"]}))

specs.append(dict(id="mb3d_ep13", base="mb3d_ep05",
  lyrics="""[Chorus]
All aboard the starlight train,
Chugging softly down the lane,
Choo-choo, choo-choo, slow and deep,
Starlight train will bring you sleep.

[Verse 1]
Bunny has a ticket, Lamb has one too,
Teddy has a pillow, soft and blue,
The moon is the light at the front of the train,
Rolling past the fields of grain.

[Chorus]
All aboard the starlight train,
Chugging softly down the lane,
Choo-choo, choo-choo, slow and deep,
Starlight train will bring you sleep.

[Verse 2]
Past the sleepy mountains, past the quiet sea,
Past the sleepy owl in the tall pine tree,
Every little star is a station light,
Waving to the train goodnight.

[Bridge]
Breathe in slowly, the train goes slow,
Breathe out softly, steady, low,
Rock, rock, rocking on the track,
Close your eyes and settle back.

[Verse 3]
The train is getting quiet as it rolls along,
Humming you a soft and gentle song,
Last stop is your cozy bed,
Rest now, sleepy little head.

[Chorus]
All aboard the starlight train,
Chugging softly down the lane,
Choo-choo, choo-choo, slow and deep,
Starlight train will bring you sleep.

[Outro]
Choo-choo. Goodnight.""",
  props={"chorus1": [T("Starlight Train", "#ffd88a", size=0.55), P("moon", None, at="top", delay=2)], "verse1": [P("heart", "Teddy", at="right"), P("moon", "moon", at="top")],
         "chorus2": [P("zzz", "sleep.", at="right")], "verse2": [P("numstar", "star", at="left", opts={"size": 0.4})],
         "bridge1": [T("Breathe...", "#bfa8ff", "Breathe", size=0.6)], "verse3": [P("zzz", "bed,", at="right")],
         "outro1": [P("zzz", "Goodnight.", at="right")]},
  meta={"title": "The Starlight Train 🌙 Sleepy Lullaby for Babies | Moonbeam", "card": "The Starlight Train", "thumb_text": "ALL ABOARD...",
        "description": "All aboard the starlight train! Luna, Bunny, Lamb and Teddy ride a gentle night train past sleepy mountains, the quiet sea and twinkling star stations, with the moon lighting the way to bed.\nA slow breathing break helps little ones settle down for sleep. For babies and toddlers.",
        "tags": ["train lullaby", "lullaby for babies", "bedtime song", "sleep music for kids", "calming lullaby", "Moonbeam Bedtime", "3D kids songs"]}))

specs.append(dict(id="gz3d_ep13", base="gz3d_ep05",
  lyrics="""[Chorus]
Why do leaves change color in the fall?
Red and orange, yellow, and all!
The green goes away and the colors show,
That's how autumn leaves glow!

[Verse 1]
All summer long the leaves are green,
Making food, the best you've seen!
They use the sunlight, water, and air,
Green, green leaves everywhere!

[Chorus]
Why do leaves change color in the fall?
Red and orange, yellow, and all!
The green goes away and the colors show,
That's how autumn leaves glow!

[Verse 2]
When fall comes, the days get short,
Less sunlight of every sort!
The green fades out, and then, surprise,
Yellow and orange meet our eyes!

[Bridge]
Fall like a leaf, twirl, twirl, twirl!
Float down softly, give a swirl!
Crunch, crunch, crunch on the ground,
Jump in a leaf pile, all around!

[Verse 3]
Then leaves let go and fall below,
The tree rests through the winter snow!
In spring new green leaves grow again,
The cycle starts, now count to ten!

[Chorus]
Why do leaves change color in the fall?
Red and orange, yellow, and all!
The green goes away and the colors show,
That's how autumn leaves glow!

[Outro]
Autumn leaves! Bye-bye, friends!""",
  props={"chorus1": [T("AUTUMN LEAVES!", "#ff8a1f", size=0.6)],
         "verse1": [T("GREEN!", "#3cc45a", "green,", size=0.7), P("sun", "sunlight,", at=[-3.0, 1.3, 3.6], opts={"size": 0.7})],
         "chorus2": [T("RED! ORANGE! YELLOW!", "#ff8a1f", size=0.5)], "verse2": [T("SHORT DAYS!", "#3b8be0", "short,", size=0.6), T("SURPRISE!", "#ffc107", "surprise,", at=L("c"), size=0.6)],
         "bridge1": [T("TWIRL!", "#ff8a1f", "twirl,", at=L("l"), size=0.6), T("CRUNCH!", "#8a5a32", "Crunch,", at=L("r"), size=0.6), T("JUMP!", "#e53935", "Jump", at=L("c"), size=0.7)],
         "verse3": [T("SPRING!", "#3cc45a", "spring", size=0.7)],
         "chorus3": [T("AUTUMN LEAVES!", "#ff8a1f", size=0.6)], "outro1": [T("BYE-BYE!", "#ff8a1f")]},
  meta={"title": "Why Do Leaves Change Color? Science Song for Kids with Gizmo", "card": "Why Leaves Change!", "thumb_text": "GREEN GOES AWAY!",
        "description": "Why do leaves change color in the fall? Gizmo the robot explains that green leaves use sunlight to make food all summer. When fall brings shorter days, the green fades and the yellow and orange show through. Then leaves drop, the tree rests in winter and new leaves grow in spring.\nKids twirl like falling leaves and jump in a leaf pile. Ages 3-6.",
        "tags": ["why do leaves change color", "autumn leaves song", "fall song for kids", "seasons", "science song for kids", "kids songs", "Gizmo Explains", "3D kids songs"]}))
for s in specs:
    base = B3(s["base"]); spec = copy.deepcopy(base)
    spec["lyrics"] = s["lyrics"]; spec["meta"] = s["meta"]; spec["seed"] = base["seed"] + 800
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
    json.dump(spec, open(f"/root/zoo/specs/b13/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]), secs)
