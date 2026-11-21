import json, copy, re, sys
sys.path.insert(0, "/root/zoo/blender/zoo3d"); import timing_lib as TL
Z = "/root/zoo/blender/zoo3d"
B3 = lambda n: json.load(open(f"/root/zoo/specs/b5/{n}.song.json"))
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
L = lambda x: [-3.4, 0.3, 3.5] if x == "l" else [3.4, 0.3, 3.5] if x == "r" else [0, 0.6, 4.3]
specs = []
specs.append(dict(id="bl3d_ep07", base="bl3d_ep05", colors={"red": "#ff3b3b"},
  lyrics="""[Chorus]
Bloop turns red, red, red!
Red from his toes up to his head!
Red like an apple, red like a heart,
Red, red, red, let's make a start!

[Verse 1]
A shiny red apple, crunch, crunch, crunch,
Red, red apple, munch, munch, munch!
A big red balloon floating so high,
Red, red balloon up in the sky!

[Chorus]
Bloop turns red, red, red!
Red from his toes up to his head!
Red like an apple, red like a heart,
Red, red, red, let's make a start!

[Verse 2]
A red fire truck goes zoom, zoom, zoom,
A red ladybug in my room!
A red crayon draws a happy face,
Red, red, red, all over the place!

[Bridge]
Touch something red, one, two, three!
Point to red, show it to me!
Jump up high and shout hooray,
Red is the color of the day!

[Verse 3]
Red strawberries, sweet and bright,
Red roses smell just right!
Red and yellow, red and blue,
Red is my favorite, how about you?

[Chorus]
Bloop turns red, red, red!
Red from his toes up to his head!
Red like an apple, red like a heart,
Red, red, red, let's make a start!

[Outro]
Red, red, red! Bye-bye, friends!""",
  props={"chorus1": [T("RED!", "#ff3b3b", size=0.9)], "verse1": [P("apple", "apple,", at=[-3.4, 0.9, 3.6]), P("balloon", "balloon", at=[3.4, 1.4, 3.6], opts={"color": "#ff3b3b"})],
         "chorus2": [T("RED!", "#ff3b3b", size=0.9)], "verse2": [P("crayon", "crayon", at=[3.4, 0.9, 3.6], opts={"color": "#ff3b3b"}), T("ZOOM!", "#ff3b3b", "zoom,", at=[-3.4, 1.4, 3.6], size=0.6)],
         "bridge1": [T("TOUCH RED!", "#ff3b3b", "touch", size=0.7), T("HOORAY!", "#ffd21f", "hooray,", at=L("c"), size=0.7)],
         "verse3": [P("heart", "roses", at=[3.4, 1.2, 3.6], opts={"color": "#ff3b3b"}), T("RED!", "#ff3b3b", "favorite,", size=0.7)],
         "chorus3": [T("RED!", "#ff3b3b", size=0.9)], "outro1": [T("BYE-BYE!", "#ff3b3b")]},
  meta={"title": "Bloop Turns Red! Red Color Song for Kids | Part 3", "card": "Bloop Turns Red!", "thumb_text": "BLOOP TURNS RED!",
        "description": "Bloop turns red! Part 3 of Bloop's color song series: a crunchy red apple, a red balloon, a red fire truck, a ladybug and red strawberries.\nKids touch something red, point to red and jump for the color of the day. Ages 2-5.",
        "tags": ["red color song", "learn colors", "color songs for kids", "colors for toddlers", "kids songs", "Bloop's Color Lab", "3D kids songs"]}))

specs.append(dict(id="tt3d_ep07", base="tt3d_ep05",
  lyrics="""[Chorus]
Garbage truck, garbage truck, clean, clean, clean!
Keeping our town so neat and green!
Lift it up, dump it in, beep, beep, beep,
Garbage truck makes the street so neat!

[Verse 1]
Early in the morning, rumble, rumble, roar,
Here comes the garbage truck, past my door!
Big arms reach out and grab the bin,
Lift it up high and tip it in!

[Chorus]
Garbage truck, garbage truck, clean, clean, clean!
Keeping our town so neat and green!
Lift it up, dump it in, beep, beep, beep,
Garbage truck makes the street so neat!

[Verse 2]
Paper and bottles go in the blue,
Recycling helps the planet too!
Banana peels and apple cores,
Compost makes the garden grow more!

[Bridge]
Pick up a toy and put it away!
Clean up, clean up, every day!
Sweep, sweep, sweep and wipe, wipe, wipe,
Now our room looks clean and bright!

[Verse 3]
Thank you, driver, waving hi,
Honk, honk, honk as you drive by!
Every street is clean and neat,
Garbage truck, you can't be beat!

[Chorus]
Garbage truck, garbage truck, clean, clean, clean!
Keeping our town so neat and green!
Lift it up, dump it in, beep, beep, beep,
Garbage truck makes the street so neat!

[Outro]
Clean, clean, clean! Bye-bye, trucks!""",
  props={"chorus1": [T("CLEAN UP!", "#2fb54a", size=0.8)], "verse1": [T("RUMBLE!", "#ffc107", "rumble,", at=[-2.8, 1.6, 3.6], size=0.6), T("LIFT!", "#2fb54a", "lift", at=[2.8, 1.6, 3.6], size=0.7)],
         "chorus2": [T("BEEP BEEP!", "#ffc107", size=0.7)], "verse2": [T("RECYCLE!", "#3b8be0", "recycling", size=0.7), T("COMPOST!", "#8a5a32", "compost", at=L("c"), size=0.6)],
         "bridge1": [T("CLEAN UP!", "#2fb54a", "clean", at=L("l"), size=0.7), T("SWEEP!", "#ffc107", "sweep,", at=L("r"), size=0.7)],
         "verse3": [T("THANK YOU!", "#e8302a", "thank", size=0.7), P("cone", "street", at=[-3.0, 0.4, 3.6])],
         "chorus3": [T("CLEAN UP!", "#2fb54a", size=0.8)], "outro1": [T("BYE-BYE!", "#2fb54a")]},
  meta={"title": "Garbage Truck Song! Clean Up Song for Kids | Tiny Truck Town", "card": "Garbage Truck Song!", "thumb_text": "GARBAGE TRUCK!",
        "description": "The garbage truck is here! Sing along with the garbage truck as it lifts the bins, keeps Tiny Truck Town clean and helps with recycling and compost.\nKids clean up their toys, sweep and wipe, and say thank you to the driver. Ages 2-6.",
        "tags": ["garbage truck song", "clean up song", "recycling for kids", "trucks for kids", "garbage truck for kids", "kids songs", "Tiny Truck Town", "3D kids songs"]}))

specs.append(dict(id="fr3d_ep08", base="fr3d_ep06",
  lyrics="""[Chorus]
Eat a rainbow, yum, yum, yum!
Every color, here they come!
Red and orange, yellow, green,
The yummiest rainbow you've ever seen!

[Verse 1]
Red strawberries, sweet and bright,
Orange carrots, crunchy bite!
Yellow bananas, peel and munch,
Colors for breakfast, colors for lunch!

[Chorus]
Eat a rainbow, yum, yum, yum!
Every color, here they come!
Red and orange, yellow, green,
The yummiest rainbow you've ever seen!

[Verse 2]
Green broccoli, little trees,
Blueberries, blue as the seas!
Purple grapes, round and sweet,
A rainbow plate is fun to eat!

[Bridge]
Pick a color, one, two, three!
Take a bite and smile with me!
Rub your tummy, round and round,
Healthy food makes us strong and sound!

[Verse 3]
Every color helps you grow,
Strong and healthy, head to toe!
Fill your plate with every hue,
A rainbow lunch for me and you!

[Chorus]
Eat a rainbow, yum, yum, yum!
Every color, here they come!
Red and orange, yellow, green,
The yummiest rainbow you've ever seen!

[Outro]
Eat a rainbow! Bye-bye, fruity friends!""",
  props={"chorus1": [T("EAT A RAINBOW!", "#ff5c8a", size=0.6), P("rainbow", None, at=[0, 1.8, 3.4], delay=1)],
         "verse1": [P("bigfruit", "strawberries,", at=[-2.6, 0.9, 3.4], opts={"kind": "strawberry"}), P("bigfruit", "bananas,", at=[2.6, 0.9, 3.4], opts={"kind": "banana"})],
         "chorus2": [T("YUM YUM!", "#ff8a1f", size=0.7)], "verse2": [P("bigfruit", "broccoli,", at=[-2.6, 0.9, 3.4], opts={"kind": "broccoli"}), P("bigfruit", "grapes,", at=[2.6, 0.9, 3.4], opts={"kind": "grape"})],
         "bridge1": [T("1, 2, 3!", "#3cc45a", "one,", size=0.7), T("YUM!", "#ff5c8a", "tummy,", at=L("c"), size=0.7)],
         "verse3": [P("plate", "plate", at=[0, 0.8, 3.4]), T("GROW!", "#3cc45a", "grow,", size=0.7)],
         "chorus3": [T("EAT A RAINBOW!", "#ff5c8a", size=0.6)], "outro1": [T("BYE-BYE!", "#ff5c8a")]},
  meta={"title": "Eat a Rainbow! Healthy Food Song for Kids | Fruity Friends", "card": "Eat a Rainbow!", "thumb_text": "EAT A RAINBOW!",
        "description": "Eat a rainbow! Pipkiko and the Fruity Friends sing about red strawberries, orange carrots, yellow bananas, green broccoli, blueberries and purple grapes.\nA healthy eating song that teaches colors and good food habits. Ages 2-5.",
        "tags": ["eat a rainbow", "healthy food song", "fruit and vegetable song", "healthy eating for kids", "learn colors", "kids songs", "Fruity Friends", "3D kids songs"]}))

specs.append(dict(id="zoo3d_ep07", base="zoo3d_ep05",
  lyrics="""[Chorus]
Head, shoulders, knees and paws, knees and paws!
Head, shoulders, knees and paws, knees and paws!
Ears and eyes and a nose and jaws,
Head, shoulders, knees and paws!

[Lion]
The lion shakes his fluffy mane,
Shake your head, now do it again!
Roar, roar, touch your nose,
Head, shoulders, knees and toes!

[Elephant]
The elephant has great big ears,
Flap, flap, flap, give a cheer!
Toot, toot, swing your arm,
Elephant trunk, safe from harm!

[Chorus]
Head, shoulders, knees and paws, knees and paws!
Head, shoulders, knees and paws, knees and paws!
Ears and eyes and a nose and jaws,
Head, shoulders, knees and paws!

[Giraffe]
The giraffe has a long, long neck,
Stretch up tall, now let's check!
Munch, munch, touch the sky,
Giraffe neck reaches high!

[Zebra]
The zebra stomps with stripy legs,
The hippo opens wide and begs!
Stomp your feet and open wide,
Splash, splash, splash, side to side!

[Bridge]
Faster now, head, shoulders, go!
Knees and paws, now nice and slow!
Touch your nose and touch your ears,
Give yourself a round of cheers!

[Chorus]
Head, shoulders, knees and paws, knees and paws!
Head, shoulders, knees and paws, knees and paws!
Ears and eyes and a nose and jaws,
Head, shoulders, knees and paws!

[Outro]
Knees and paws! Bye-bye, friends!""",
  props={"chorus1": [T("HEAD!", "#ffb627", "head,", at=L("l"), size=0.6), T("PAWS!", "#ff7a00", "paws,", at=L("r"), size=0.6)],
         "lion1": [T("SHAKE!", "#ff7a00", "shake", at=[-3.6, -0.3, 2.5], size=0.6)], "elephant1": [T("FLAP!", "#5d6b8f", "flap,", at=[3.4, 0.4, 3.0], size=0.6)],
         "chorus2": [T("KNEES!", "#3db8ff", "knees", at=L("c"), size=0.6)], "giraffe1": [T("STRETCH!", "#b8692c", "stretch", at=[3.2, 1.0, 3.0], size=0.5)],
         "zebra1": [T("STOMP!", "#25232b", "stomp", at=[3.6, 0.3, 2.6], size=0.5), T("SPLASH!", "#3db8ff", "splash,", at=[-3.6, 0.3, 2.6], size=0.5)],
         "bridge1": [T("FASTER!", "#ff7a00", "faster", at=L("l"), size=0.7), T("SLOW...", "#3db8ff", "slow", at=L("r"), size=0.6)],
         "chorus3": [T("HEAD!", "#ffb627", "head,", at=L("l"), size=0.6), T("PAWS!", "#ff7a00", "paws,", at=L("r"), size=0.6)], "outro1": [T("BYE-BYE!", "#ffb627")]},
  meta={"title": "Head, Shoulders, Knees and Paws! Animal Song with Milo", "card": "Head, Shoulders, Knees and Paws!", "thumb_text": "KNEES AND PAWS!",
        "description": "Head, shoulders, knees and paws! An animal twist on the classic body parts song with Milo, the lion, the elephant, the giraffe, the zebra and the hippo.\nKids touch their head, shoulders, knees and toes, shake like a lion, flap like an elephant and stretch like a giraffe. Ages 2-6.",
        "tags": ["head shoulders knees and toes", "body parts song", "animal song for kids", "action song", "zoo animals for kids", "kids songs", "nursery rhymes", "The Animated Zoo", "Milo"]}))

specs.append(dict(id="mb3d_ep07", base="mb3d_ep05",
  lyrics="""[Chorus]
Rock-a-bye baby, on the treetop,
When the wind blows, the cradle will rock,
Hush now, little one, snuggle in tight,
Rock-a-bye baby, sleep through the night.

[Verse 1]
The moon is rising, silver and round,
The stars are twinkling without a sound,
Bunny is yawning, lamb is too,
Teddy is sleepy, and so are you.

[Chorus]
Rock-a-bye baby, on the treetop,
When the wind blows, the cradle will rock,
Hush now, little one, snuggle in tight,
Rock-a-bye baby, sleep through the night.

[Verse 2]
Gentle breezes whisper low,
Swaying branches, soft and slow,
Owl says hoo from the tall oak tree,
Close your eyes and dream with me.

[Bridge]
Breathe in slowly, one, two, three,
Breathe out softly, calm and free,
Wiggle your toes and let them rest,
Snuggle down, you're the very best.

[Verse 3]
Luna is watching from up above,
Wrapping the world in a blanket of love,
Morning will come with the shining sun,
Sleep now, sleep now, little one.

[Chorus]
Rock-a-bye baby, on the treetop,
When the wind blows, the cradle will rock,
Hush now, little one, snuggle in tight,
Rock-a-bye baby, sleep through the night.

[Outro]
Rock-a-bye baby. Goodnight.""",
  props={"chorus1": [T("Rock-a-bye Baby", "#ffd88a", size=0.55), P("moon", None, at="top", delay=2)], "verse1": [P("star", "stars", at=[2.6, 2.0, 3.2], opts={"size": 0.4}), P("zzz", "yawning,", at="right")],
         "chorus2": [P("heart", "snuggle", at="right")], "verse2": [P("zzz", "eyes", at="left")],
         "bridge1": [T("Breathe...", "#bfa8ff", "breathe", size=0.6)], "verse3": [P("heart", "love,", at="right")],
         "chorus3": [T("Rock-a-bye Baby", "#ffd88a", size=0.55)], "outro1": [P("zzz", None, at="right")]},
  meta={"title": "Rock-a-bye Baby 🌙 Lullaby for Babies & Kids | Moonbeam", "card": "Rock-a-bye Baby", "thumb_text": "ROCK-A-BYE BABY",
        "description": "Rock-a-bye Baby, the classic lullaby with gentle new verses. Luna, Bunny, Lamb and Teddy get sleepy as the moon rises and the stars twinkle.\nSoft music box, harp and slow breathing to help little ones fall asleep. Ages 0-6.",
        "tags": ["rock a bye baby", "lullaby for babies", "nursery rhymes", "bedtime song", "sleep music for kids", "baby sleep", "lullabies", "Moonbeam Bedtime", "3D kids songs"]}))

specs.append(dict(id="gz3d_ep07", base="gz3d_ep05",
  lyrics="""[Chorus]
Day and night, day and night,
The Earth spins round from dark to light!
Sun comes up and sun goes down,
Our big Earth keeps spinning round!

[Verse 1]
In the morning, the sun says hi,
Rising up into the sky!
The Earth is spinning, slow and steady,
Wake up, wake up, the day is ready!

[Verse 2]
When our side turns away from the sun,
Night time comes and the day is done!
The moon and stars come out to play,
Goodnight sun, see you next day!

[Chorus]
Day and night, day and night,
The Earth spins round from dark to light!
Sun comes up and sun goes down,
Our big Earth keeps spinning round!

[Verse 3]
One whole spin takes a day,
Twenty-four hours, hip hooray!
Somewhere it's morning, somewhere it's night,
Our spinning Earth is just right!

[Bridge]
Spin around like the Earth, whee!
Stretch up high like the sun, see!
Curl up small like the night,
Then wake up with the morning light!

[Chorus]
Day and night, day and night,
The Earth spins round from dark to light!
Sun comes up and sun goes down,
Our big Earth keeps spinning round!

[Outro]
Day and night! Bye-bye, friends!""",
  props={"chorus1": [T("DAY & NIGHT!", "#3b8be0", size=0.7), P("sun", None, at=[-3.2, 1.2, 3.6], opts={"size": 0.7}, delay=1)],
         "verse1": [P("sun", "sun", at=[-3.0, 1.2, 3.6], opts={"size": 0.8}), T("SPIN!", "#3b8be0", "spinning,", size=0.7)],
         "verse2": [P("moon", "moon", at=[3.0, 1.4, 3.6]), P("star", "stars", at=[-3.0, 1.6, 3.6])],
         "chorus2": [T("DAY & NIGHT!", "#3b8be0", size=0.7)], "verse3": [T("24 HOURS!", "#ff8a1f", "twenty-four", size=0.6)],
         "bridge1": [T("SPIN!", "#3b8be0", "spin", at=L("l"), size=0.7), T("STRETCH!", "#ffc107", "stretch", at=L("r"), size=0.7), T("CURL UP!", "#8e5bd8", "curl", at=L("c"), size=0.6)],
         "chorus3": [T("DAY & NIGHT!", "#3b8be0", size=0.7)], "outro1": [T("BYE-BYE!", "#3b8be0")]},
  meta={"title": "Why Is There Day and Night? Science Song for Kids with Gizmo", "card": "Day and Night!", "thumb_text": "DAY & NIGHT?",
        "description": "Why is there day and night? Gizmo the robot explains that the Earth spins: when our side faces the sun it's day, and when it turns away it's night. One spin takes 24 hours.\nKids spin like the Earth, stretch like the sun and curl up like the night. Ages 3-6.",
        "tags": ["day and night song", "why is there day and night", "earth spins", "science song for kids", "space for kids", "kids songs", "Gizmo Explains", "3D kids songs"]}))
for s in specs:
    base = B3(s["base"]); spec = copy.deepcopy(base)
    spec["lyrics"] = s["lyrics"]; spec["meta"] = s["meta"]; spec["seed"] = base["seed"] + 200
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
    json.dump(spec, open(f"/root/zoo/specs/b7/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]), secs)
