import json, copy, re, sys
sys.path.insert(0, "/root/zoo/blender/zoo3d"); import timing_lib as TL
Z = "/root/zoo/blender/zoo3d"
B3 = lambda n: json.load(open(f"/root/zoo/specs/b5/{n}.song.json"))
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
L = lambda x: [-3.4, 0.3, 3.5] if x == "l" else [3.4, 0.3, 3.5] if x == "r" else [0, 0.6, 4.3]
specs = []

specs.append(dict(id="bl3d_ep12", base="bl3d_ep05", colors={"orange": "#ff8a1f"},
  lyrics="""[Chorus]
Bloop turns orange, orange, orange!
Bright and bouncy, oh so gorgeous!
Orange like a pumpkin, orange like the sun,
Orange, orange, orange, fun, fun, fun!

[Verse 1]
A juicy orange, peel it round,
Orange carrots in the ground!
An orange goldfish swims so fast,
Swishing, swishing, swimming past!

[Chorus]
Bloop turns orange, orange, orange!
Bright and bouncy, oh so gorgeous!
Orange like a pumpkin, orange like the sun,
Orange, orange, orange, fun, fun, fun!

[Verse 2]
An orange pumpkin, big and round,
Orange leaves fall to the ground!
An orange tiger, stripes so bold,
Orange sunsets, warm and gold!

[Bridge]
Swim like a goldfish, swish, swish, swish!
Roll like a pumpkin, make a wish!
Fall like a leaf, down, down, down,
Orange, orange all around!

[Verse 3]
Red and yellow make orange, see?
Mix them up, one, two, three!
Orange is warm and orange is bright,
Orange makes me feel just right!

[Chorus]
Bloop turns orange, orange, orange!
Bright and bouncy, oh so gorgeous!
Orange like a pumpkin, orange like the sun,
Orange, orange, orange, fun, fun, fun!

[Outro]
Orange, orange! Bye-bye, friends!""",
  props={"chorus1": [T("ORANGE!", "#ff8a1f", size=0.9)], "verse1": [P("carrot", "carrots", at=[-3.4, 0.9, 3.6]), T("SWISH!", "#ff8a1f", "Swishing,", at=[3.4, 1.4, 3.6], size=0.6)],
         "chorus2": [P("sun", None, at=[0, 1.9, 3.4], delay=1)], "verse2": [P("leaf", "leaves", at=[3.4, 1.2, 3.6], opts={"color": "#ff8a1f"}), T("ROAR!", "#ff8a1f", "tiger,", at=[-3.4, 1.4, 3.6], size=0.6)],
         "bridge1": [T("SWISH!", "#ff8a1f", "Swim", at=L("l"), size=0.6), T("ROLL!", "#ffb000", "Roll", at=L("r"), size=0.6), T("DOWN!", "#e85d00", "Fall", at=L("c"), size=0.6)],
         "verse3": [T("RED + YELLOW = ORANGE", "#ff8a1f", "yellow", size=0.42)],
         "chorus3": [T("ORANGE!", "#ff8a1f", size=0.9)], "outro1": [T("BYE-BYE!", "#ff8a1f")]},
  meta={"title": "Bloop Turns Orange! Orange Color Song for Kids | Part 7", "card": "Bloop Turns Orange!", "thumb_text": "PUMPKIN TIME!",
        "description": "Bloop turns orange! Part 7 of Bloop's color song series: a juicy orange, carrots, a goldfish, a big pumpkin, falling leaves and a warm sunset.\nKids swim like a goldfish, roll like a pumpkin and learn that red and yellow make orange. Ages 2-5.",
        "tags": ["orange color song", "learn colors", "color songs for kids", "colors for toddlers", "kids songs", "Bloop's Color Lab", "3D kids songs"]}))

specs.append(dict(id="tt3d_ep12", base="tt3d_ep05",
  lyrics="""[Chorus]
Ding-a-ling, ding-a-ling, here it comes!
The ice cream truck, yum, yum, yum!
Ring the bell and wave hello,
Ice cream truck, here we go!

[Verse 1]
Hear the music down the street,
Something cold and something sweet!
Line up nicely, one by one,
Waiting turns is lots of fun!

[Chorus]
Ding-a-ling, ding-a-ling, here it comes!
The ice cream truck, yum, yum, yum!
Ring the bell and wave hello,
Ice cream truck, here we go!

[Verse 2]
Chocolate, vanilla, strawberry too,
Which one is the one for you?
Say please and say thank you,
Good manners, that's what we do!

[Bridge]
Lick, lick, lick, before it drips!
Little bites and little sips!
Brr, brr, brr, it's cold, it's true,
Shiver like an ice cube, you!

[Verse 3]
Wave goodbye, the truck drives on,
Ding-a-ling, the truck is gone!
Wipe your hands and wipe your chin,
Tomorrow it will come again!

[Chorus]
Ding-a-ling, ding-a-ling, here it comes!
The ice cream truck, yum, yum, yum!
Ring the bell and wave hello,
Ice cream truck, here we go!

[Outro]
Ding-a-ling! Bye-bye, trucks!""",
  props={"chorus1": [T("DING-A-LING!", "#ff5c8a", size=0.7), P("bell", None, at=[-3.0, 1.4, 3.6], delay=1)],
         "verse1": [T("LINE UP!", "#3b8be0", "Line", size=0.7), T("TAKE TURNS!", "#2fb54a", "turns", at=L("c"), size=0.55)],
         "chorus2": [T("YUM YUM!", "#ff5c8a", size=0.7)], "verse2": [T("PLEASE!", "#ffc107", "please", at=L("l"), size=0.6), T("THANK YOU!", "#e8302a", "thank", at=L("r"), size=0.6)],
         "bridge1": [T("LICK!", "#ff5c8a", "Lick,", at=L("l"), size=0.7), T("SIP!", "#3b8be0", "sips!", at=L("r"), size=0.7), T("BRRR!", "#7fd3ff", "Brr,", at=L("c"), size=0.8)],
         "verse3": [T("BYE TRUCK!", "#ff5c8a", "goodbye,", size=0.6)],
         "chorus3": [T("DING-A-LING!", "#ff5c8a", size=0.7)], "outro1": [T("BYE-BYE!", "#ff5c8a")]},
  meta={"title": "Ice Cream Truck Song! Ding-a-Ling | Tiny Truck Town", "card": "Ice Cream Truck Song!", "thumb_text": "YUM YUM!",
        "description": "Ding-a-ling! The ice cream truck comes down the street in Tiny Truck Town. Kids line up nicely, take turns, choose chocolate, vanilla or strawberry, and remember to say please and thank you.\nLick, sip and shiver along. Ages 2-5.",
        "tags": ["ice cream truck song", "trucks for kids", "manners song for kids", "please and thank you", "kids songs", "Tiny Truck Town", "3D kids songs"]}))

specs.append(dict(id="fr3d_ep13", base="fr3d_ep06",
  lyrics="""[Chorus]
Sweet or sour, crunchy or soft,
Taste it, taste it, try a lot!
Your tongue can tell you every one,
Tasting fruit is so much fun!

[Verse 1]
A lemon is sour, pucker your face,
Sour, sour, what a taste!
A strawberry's sweet, mmm, so nice,
Sweet like candy, take a slice!

[Chorus]
Sweet or sour, crunchy or soft,
Taste it, taste it, try a lot!
Your tongue can tell you every one,
Tasting fruit is so much fun!

[Verse 2]
An apple goes crunch, crunch, crunch,
A crunchy apple for my lunch!
A banana is soft, squishy and smooth,
Soft and yummy, makes me groove!

[Bridge]
Pucker your lips for something sour!
Smile big for sweet, it's tasting hour!
Crunch your teeth and chomp, chomp, chomp,
Then a soft and squishy stomp!

[Verse 3]
Try a new fruit, take a bite,
Maybe you'll love it, that's alright!
Sweet, sour, crunchy, soft,
Fruity Friends will taste a lot!

[Chorus]
Sweet or sour, crunchy or soft,
Taste it, taste it, try a lot!
Your tongue can tell you every one,
Tasting fruit is so much fun!

[Outro]
Taste it, taste it! Bye-bye, fruity friends!""",
  props={"chorus1": [T("TASTE IT!", "#ff5c8a", size=0.8)],
         "verse1": [T("SOUR!", "#ffd83a", "sour,", at=[-2.6, 1.5, 3.4], size=0.7), P("bigfruit", "strawberry's", at=[2.6, 0.9, 3.4], opts={"kind": "strawberry"})],
         "chorus2": [T("YUM!", "#ff8a1f", size=0.8)], "verse2": [P("bigfruit", "apple", at=[-2.6, 0.9, 3.4], opts={"kind": "apple"}), P("bigfruit", "banana", at=[2.6, 0.9, 3.4], opts={"kind": "banana"})],
         "bridge1": [T("PUCKER!", "#ffd83a", "Pucker", at=L("l"), size=0.6), T("SMILE!", "#ff5c8a", "Smile", at=L("r"), size=0.6), T("CHOMP!", "#e3262b", "chomp,", at=L("c"), size=0.7)],
         "verse3": [T("TRY IT!", "#3cc45a", "Try", size=0.7)],
         "chorus3": [T("TASTE IT!", "#ff5c8a", size=0.8)], "outro1": [T("BYE-BYE!", "#ff5c8a")]},
  meta={"title": "Sweet or Sour? Fruit Tasting Song for Kids | Fruity Friends", "card": "Sweet or Sour?", "thumb_text": "PUCKER UP!",
        "description": "Sweet, sour, crunchy or soft? The Fruity Friends taste a sour lemon, a sweet strawberry, a crunchy apple and a soft banana.\nKids pucker for sour, smile for sweet, chomp for crunchy, and learn it's fun to try a new fruit. Ages 2-5.",
        "tags": ["taste song for kids", "sweet and sour", "fruit song for kids", "five senses", "picky eaters", "kids songs", "Fruity Friends", "3D kids songs"]}))

specs.append(dict(id="zoo3d_ep12", base="zoo3d_ep05",
  lyrics="""[Chorus]
How do animals sleep at night?
Some lie down and some stand upright!
Close your eyes and count to three,
Sleepy zoo friends, just like me!

[Verse 1]
The lion sleeps most of the day,
Napping lots, then up to play!
The giraffe takes tiny naps,
Standing up, just short ones, perhaps!

[Chorus]
How do animals sleep at night?
Some lie down and some stand upright!
Close your eyes and count to three,
Sleepy zoo friends, just like me!

[Verse 2]
The zebra can sleep standing tall,
Ready to run if friends should call!
The hippo naps in water deep,
Floating up to breathe in sleep!

[Bridge]
Stand up tall and close your eyes,
Like a zebra, what a surprise!
Curl up small like a cozy cat,
Yawn, yawn, yawn, imagine that!

[Verse 3]
The elephant can stand or lie,
Under the big savanna sky!
Milo sleeps up in his tree,
Tucked in his nest, sleepy as can be!

[Chorus]
How do animals sleep at night?
Some lie down and some stand upright!
Close your eyes and count to three,
Sleepy zoo friends, just like me!

[Outro]
Goodnight, zoo friends! Bye-bye, friends!""",
  props={"chorus1": [T("SLEEPY ZOO!", "#8e5bd8", size=0.7)],
         "verse1": [P("sign", "lion", at=[-3.2, 1.6, 3.6], opts={"text": "LION"}), P("sign", "giraffe", at=[3.2, 1.6, 3.6], opts={"text": "GIRAFFE"})],
         "chorus2": [T("1, 2, 3...", "#8e5bd8", "count", size=0.6)],
         "verse2": [P("sign", "zebra", at=[-3.2, 1.6, 3.6], opts={"text": "ZEBRA"}), P("sign", "hippo", at=[3.2, 1.6, 3.6], opts={"text": "HIPPO"})],
         "bridge1": [T("STAND TALL!", "#ffb627", "Stand", at=L("l"), size=0.55), T("CURL UP!", "#8e5bd8", "Curl", at=L("r"), size=0.55), T("YAWN!", "#3b8be0", "Yawn,", at=L("c"), size=0.7)],
         "verse3": [P("sign", "elephant", at=[-3.2, 1.6, 3.6], opts={"text": "ELEPHANT"}), T("NEST!", "#8a5a32", "nest,", at=[3.2, 1.6, 3.6], size=0.6)],
         "chorus3": [T("SLEEPY ZOO!", "#8e5bd8", size=0.7)], "outro1": [T("GOODNIGHT!", "#8e5bd8")]},
  meta={"title": "How Do Animals Sleep? Sleepy Animal Song for Kids with Milo", "card": "How Do Animals Sleep?", "thumb_text": "STANDING UP?!",
        "description": "How do animals sleep? Milo finds out: lions nap for most of the day, giraffes take tiny naps standing up, zebras can sleep standing, hippos nap in the water and float up to breathe, and elephants can sleep standing or lying down.\nKids stand tall like a zebra, curl up small and yawn along. Ages 2-5.",
        "tags": ["how do animals sleep", "animal facts for kids", "sleepy song", "safari animals", "animal song for kids", "kids songs", "The Animated Zoo", "Milo", "3D kids songs"]}))

specs.append(dict(id="mb3d_ep12", base="mb3d_ep05",
  lyrics="""[Chorus]
Waves are rolling, soft and slow,
Back and forth they come and go,
Hush now, hush now, close your eyes,
Sleep beneath the starry skies.

[Verse 1]
The ocean whispers, shh, shh, shh,
Little boats are resting, hush,
Seashells sleeping in the sand,
Moonlight shining on the land.

[Chorus]
Waves are rolling, soft and slow,
Back and forth they come and go,
Hush now, hush now, close your eyes,
Sleep beneath the starry skies.

[Verse 2]
Little fishes, swimming deep,
Snuggle down and fall asleep,
Gentle turtles, slow and calm,
Rocking in the ocean's arms.

[Bridge]
Breathe in slowly, like a wave comes in,
Breathe out softly, let the rest begin,
Rock, rock, rocking, side to side,
Floating on the sleepy tide.

[Verse 3]
Bunny, Lamb and Teddy too,
The ocean sings a song for you,
Waves are quiet, stars are bright,
Goodnight ocean, sleep tight.

[Chorus]
Waves are rolling, soft and slow,
Back and forth they come and go,
Hush now, hush now, close your eyes,
Sleep beneath the starry skies.

[Outro]
Shh, shh, shh. Goodnight.""",
  props={"chorus1": [T("Sleepy Waves", "#9fd3ff", size=0.55), P("moon", None, at="top", delay=2)], "verse1": [P("moon", "Moonlight", at="top")],
         "chorus2": [P("numstar", "starry", at="left", opts={"size": 0.4})], "verse2": [P("zzz", "asleep,", at="right")],
         "bridge1": [T("Breathe...", "#bfa8ff", "Breathe", size=0.6)], "verse3": [P("heart", "Teddy", at="right")],
         "outro1": [P("zzz", "Goodnight.", at="right")]},
  meta={"title": "Sleepy Ocean Waves 🌙 Calm Lullaby for Babies | Moonbeam", "card": "Sleepy Ocean Waves", "thumb_text": "SHH... WAVES",
        "description": "A calm ocean lullaby. Soft waves roll in and out, little boats rest, seashells sleep in the sand and turtles rock gently as Luna, Bunny, Lamb and Teddy drift off.\nA slow breathing break, in like a wave and out like the tide, helps little ones fall asleep. For babies and toddlers.",
        "tags": ["ocean lullaby", "waves for sleep", "lullaby for babies", "calming bedtime song", "sleep music for kids", "Moonbeam Bedtime", "3D kids songs"]}))

specs.append(dict(id="gz3d_ep12", base="gz3d_ep05",
  lyrics="""[Chorus]
Shadow, shadow, follow me!
Where I go, my shadow will be!
Light shines bright, I block the way,
That's how shadows come to play!

[Verse 1]
When light shines on me, guess what I see?
A dark shape on the ground, it's me!
Light can't go through me, so it's true,
A shadow forms behind me too!

[Chorus]
Shadow, shadow, follow me!
Where I go, my shadow will be!
Light shines bright, I block the way,
That's how shadows come to play!

[Verse 2]
In the morning, shadows are long,
At noon they're short, now sing along!
In the evening, long again,
Stretching out from you and friends!

[Bridge]
Wave your arms, your shadow waves too!
Jump up high, it jumps with you!
Make a bunny with your hands,
Shadow puppets, shadow bands!

[Verse 3]
Move the light and watch it change,
Big and small, it rearranges!
No light at all? No shadow there,
Light makes shadows everywhere!

[Chorus]
Shadow, shadow, follow me!
Where I go, my shadow will be!
Light shines bright, I block the way,
That's how shadows come to play!

[Outro]
Shadow, shadow! Bye-bye, friends!""",
  props={"chorus1": [T("SHADOWS!", "#3b3b5c", size=0.8), P("lightbulb", None, at=[-3.0, 1.4, 3.6], delay=1)],
         "verse1": [P("lightbulb", "light", at=[-3.0, 1.4, 3.6]), T("BLOCK THE LIGHT!", "#3b3b5c", "through", size=0.5)],
         "chorus2": [T("FOLLOW ME!", "#3b8be0", size=0.7)], "verse2": [T("LONG!", "#ff8a1f", "long,", at=L("l"), size=0.7), T("SHORT!", "#3b8be0", "short,", at=L("r"), size=0.7), P("sun", "noon", at=[0, 1.9, 3.6], opts={"size": 0.6})],
         "bridge1": [T("WAVE!", "#ffc107", "Wave", at=L("l"), size=0.7), T("JUMP!", "#e53935", "Jump", at=L("r"), size=0.7), T("BUNNY!", "#8e5bd8", "bunny", at=L("c"), size=0.7)],
         "verse3": [T("NO LIGHT = NO SHADOW", "#3b3b5c", "No", size=0.42)],
         "chorus3": [T("SHADOWS!", "#3b3b5c", size=0.8)], "outro1": [T("BYE-BYE!", "#3b8be0")]},
  meta={"title": "What Is a Shadow? Science Song for Kids with Gizmo", "card": "What Is a Shadow?", "thumb_text": "FOLLOW ME!",
        "description": "What is a shadow? Gizmo the robot explains that light can't pass through us, so a dark shape forms behind us. Shadows are long in the morning and evening and short at noon, and with no light there's no shadow.\nKids wave and jump with their shadows and make a shadow bunny. Ages 3-6.",
        "tags": ["shadow song for kids", "what is a shadow", "light and shadow", "science song for kids", "STEM for kids", "kids songs", "Gizmo Explains", "3D kids songs"]}))
for s in specs:
    base = B3(s["base"]); spec = copy.deepcopy(base)
    spec["lyrics"] = s["lyrics"]; spec["meta"] = s["meta"]; spec["seed"] = base["seed"] + 700
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
    json.dump(spec, open(f"/root/zoo/specs/b12/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]), secs)
