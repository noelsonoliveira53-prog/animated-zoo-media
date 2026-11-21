import json, copy
Z = "/root/zoo/blender/zoo3d"
B2 = lambda n: json.load(open(f"/root/zoo/specs/b2/{n}.song.json"))
J = lambda n: json.load(open(f"{Z}/jobs/{n}.json"))
NOINTRO = "vocals start immediately on the very first beat with the chorus, no instrumental intro, short outro"
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
def reuse(prev, name, props, **kw):
    d = copy.deepcopy({x["section"]: x for x in prev["job"]["direct"]}[name]); d["props"] = props; d.update(kw); return d
specs = []

# Bloop: Blue Color Song - Part 1 (series formula, ChuChu 7x)
p = B2("bl3d_ep02"); BL = "#3d8bff"
specs.append(dict(id="bl3d_ep03", base=p, color_words={"blue": BL, "bloop": BL},
  lyrics="""[Chorus]
Blue, blue, I'm turning blue!
Bloop is blue, and you can too!
Blue sky, blue sea, blue for me,
Blue, blue, find blue with me!

[Verse 1]
Look up high, the sky is blue,
Fluffy clouds are floating through!
Look down low, the ocean's blue,
Fishies swim and splash with you!

[Chorus]
Blue, blue, I'm turning blue!
Bloop is blue, and you can too!
Blue sky, blue sea, blue for me,
Blue, blue, find blue with me!

[Verse 2]
Blueberries, small and round,
Pick them up from the ground!
A big blue whale, the biggest one,
Sings and swims and has some fun!

[Bridge]
Point to something blue!
Touch your toes, one, two!
Clap your hands, clap, clap!
Jump up high, and back!

[Verse 3]
Blue and yellow make green, you see,
Blue and red make purple, whee!
Blue is cool and calm and bright,
Blue, blue, I love you, goodnight!

[Chorus]
Blue, blue, I'm turning blue!
Bloop is blue, and you can too!
Blue sky, blue sea, blue for me,
Blue, blue, find blue with me!

[Outro]
Blue, blue! See you next time!""",
  props={"chorus1": [T("BLUE!", BL, size=1.0)], "verse1": [T("SKY", BL, "sky", at=[-4.4, 0.6, 3.8]), T("OCEAN", BL, "ocean", at=[4.4, 0.6, 3.8]), P("drop", "ocean", at=[4.4, 0.4, 2.6])],
         "chorus2": [T("BLUE!", BL, size=1.0)], "verse2": [P("grapes", "blueberries", at=[-4.4, 0.4, 2.6], opts={"color": "blue"}), T("WHALE", BL, "whale", at=[4.4, 0.6, 3.8])],
         "bridge1": [T("POINT!", BL, "point", at=[-3.4, 0.3, 3.5], size=0.7), T("CLAP!", "#ff5c8a", "clap", at=[3.4, 0.3, 3.5], size=0.7), T("JUMP!", "#3ccf4e", "jump", at=[0, 0.6, 4.3], size=0.7)],
         "verse3": [T("GREEN", "#3ccf4e", "green", at=[-4.4, 0.6, 3.8]), T("PURPLE", "#9d6bff", "purple", at=[4.4, 0.6, 3.8])],
         "chorus3": [T("BLUE!", BL, size=1.0)], "outro1": [T("BYE-BYE!", BL)]},
  extra_colors={"green": "#3ccf4e", "purple": "#9d6bff", "yellow": "#ffd21f", "red": "#ff3b3b"},
  meta={"title": "Bloop Turns Blue! Blue Color Song for Kids | Part 1", "card": "Blue Color Song!", "thumb_text": "BLOOP TURNS BLUE!",
        "description": "The Blue Color Song for kids! Bloop the jelly blob turns blue and finds blue things everywhere: the sky, the ocean, blueberries and a big blue whale.\nKids learn the color blue and simple color mixing (blue + yellow = green, blue + red = purple). Part 1 of the Bloop color series. Ages 2-5.",
        "tags": ["blue color song", "learn colors", "color songs for kids", "colors for toddlers", "color mixing", "kids songs", "nursery rhymes", "Bloop's Color Lab", "3D kids songs"]}))

# Truck: Wheels on the Fire Truck (familiar song + twist)
p = B2("tt3d_ep02")
specs.append(dict(id="tt3d_ep03", base=p,
  lyrics="""[Chorus]
The wheels on the fire truck go round and round,
Round and round, round and round!
The wheels on the fire truck go round and round,
All through the town!

[Verse 1]
The siren on the fire truck goes wee-oo, wee-oo,
Wee-oo, wee-oo, wee-oo, wee-oo!
The lights on the fire truck go flash, flash, flash,
All through the town!

[Chorus]
The wheels on the fire truck go round and round,
Round and round, round and round!
The wheels on the fire truck go round and round,
All through the town!

[Verse 2]
The ladder on the fire truck goes up and down,
Up and down, up and down!
The hose on the fire truck goes whoosh, whoosh, whoosh,
All through the town!

[Bridge]
Roll your arms like wheels, round and round!
Reach up high like a ladder, up, up, up!
Spray like a hose, whoosh, whoosh, whoosh!
Honk like a horn, beep, beep, beep!

[Verse 3]
The firefighters on the truck say, we can help!
We can help, we can help!
The friends in the town say, thank you, thank you,
All through the town!

[Chorus]
The wheels on the fire truck go round and round,
Round and round, round and round!
The wheels on the fire truck go round and round,
All through the town!

[Outro]
Round and round! Bye-bye, fire truck!""",
  props={"chorus1": [T("ROUND & ROUND!", "#e8302a", size=0.6)], "verse1": [P("siren", "siren", at=[-2.8, 1.4, 3.6]), T("FLASH!", "#ffc107", "flash", at=[2.8, 1.6, 3.6])],
         "chorus2": [T("ROUND & ROUND!", "#e8302a", size=0.6)], "verse2": [P("ladder", "ladder", at=[-2.8, 0.6, 3.4]), P("water", "whoosh", at=[2.8, 0.8, 3.4])],
         "bridge1": [T("ROLL!", "#e8302a", "roll", at=[-3.4, 0.6, 3.5], size=0.7), T("REACH!", "#3b8be0", "reach", at=[3.4, 0.6, 3.5], size=0.7), T("SPRAY!", "#2fb5e0", "spray", at=[-1.2, 0.9, 4.2], size=0.7), T("HONK!", "#ffc107", "honk", at=[1.2, 0.9, 4.2], size=0.7)],
         "verse3": [P("helmet", "firefighters", at=[-2.8, 0.8, 3.4]), T("THANK YOU!", "#ff5c8a", "thank", at="top", size=0.6)],
         "chorus3": [T("ROUND & ROUND!", "#e8302a", size=0.6)], "outro1": [T("BYE-BYE!", "#e8302a")]},
  meta={"title": "Wheels on the Fire Truck! Kids Song | Tiny Truck Town", "card": "Wheels on the Fire Truck!", "thumb_text": "WHEELS ON THE FIRE TRUCK",
        "description": "The Wheels on the Fire Truck go round and round! A fire truck twist on the classic nursery rhyme, with Bolt and his truck friends.\nSing about the siren, flashing lights, ladder and hose, roll your arms like wheels and say thank you to firefighters. Ages 2-6.",
        "tags": ["wheels on the fire truck", "wheels on the bus", "fire truck song", "nursery rhymes", "trucks for kids", "kids songs", "vehicle songs", "Tiny Truck Town", "3D kids songs"]}))

# Fruity: Five Little Grapes Jumping on the Bed
p = B2("fr3d_ep03")
num = lambda w, n, c: P("number", w, at=[-2.6 + (n - 1) * 1.3, 0.8, 4.4], opts={"text": str(n), "color": c})
C5 = ["#e8302a", "#ff9f1a", "#ffc107", "#2fb59a", "#3b8be0"]
specs.append(dict(id="fr3d_ep04", base=p,
  lyrics="""[Chorus]
Five little grapes jumping on the bed,
One fell off and bumped his head!
Mama called the doctor and the doctor said,
No more grapes jumping on the bed!

[Verse 1]
Four little grapes jumping on the bed,
One fell off and bumped his head!
Mama called the doctor and the doctor said,
No more grapes jumping on the bed!

[Verse 2]
Three little grapes jumping on the bed,
One fell off and bumped his head!
Two little grapes jumping on the bed,
One fell off and bumped his head!

[Bridge]
Jump, jump, jump with me!
Count down, five, four, three!
Two, one, sit down slow,
Rest and count, here we go!

[Verse 3]
One little grape jumping on the bed,
She fell off and bumped her head!
Mama gave a hug and the doctor said,
Grapes are safe now, sleepy in bed!

[Chorus]
Five little grapes jumping on the bed,
One fell off and bumped his head!
Mama called the doctor and the doctor said,
No more grapes jumping on the bed!

[Outro]
Five, four, three, two, one! Goodnight, grapes!""",
  props={"chorus1": [T("5 LITTLE GRAPES", "#8e5bd8", size=0.6), P("bigfruit", "grapes", at=[0, 1.1, 3.6], opts={"kind": "grape"})], "verse1": [T("4", "#2fb59a", "four", size=1.2)],
         "chorus2": [T("5 LITTLE GRAPES", "#8e5bd8", size=0.6)], "verse2": [T("3", "#ffc107", "three", at=[-3.4, 1.4, 3.6], size=1.2), T("2", "#ff9f1a", "two", at=[3.4, 1.4, 3.6], size=1.2)],
         "bridge1": [T("JUMP!", "#8e5bd8", "jump", at=[-3.4, 0.3, 3.5], size=0.7)] + [num(w, n, C5[n - 1]) for w, n in [("five", 5), ("four", 4), ("three", 3), ("two", 2), ("one", 1)]],
         "verse3": [T("1", "#e8302a", "one", size=1.2), P("heart", "hug", at="right")],
         "chorus3": [T("5 LITTLE GRAPES", "#8e5bd8", size=0.6)], "outro1": [T("GOODNIGHT!", "#8e5bd8", size=0.6)]},
  meta={"title": "Five Little Grapes Jumping on the Bed! | Fruity Friends", "card": "5 Little Grapes!", "thumb_text": "5 LITTLE GRAPES!",
        "description": "Five Little Grapes Jumping on the Bed! A fruity twist on the classic counting rhyme with Pipkiko and the Fruity Friends.\nKids count down from 5 to 1, jump along, and learn to be safe and gentle. Ages 2-5.",
        "tags": ["five little monkeys", "five little grapes", "counting song", "count down from 5", "nursery rhymes", "fruit song", "kids songs", "Fruity Friends", "3D kids songs"]}))

# Zoo: Animal Sounds Song (over-indexing topic)
p = B2("zoo3d_ep02")
specs.append(dict(id="zoo3d_ep03", base=p,
  lyrics="""[Chorus]
What does the animal say? Let's play!
Listen close and sing the sound today!
Roar and toot and neigh, hooray!
What does the animal say?

[Lion]
The lion says roar, roar, roar!
Roar so loud, the king of the savanna floor!
Roar, roar, roar,
Can you roar some more?

[Elephant]
The elephant says toot, toot, toot!
With a long gray trunk like a big flute!
Toot, toot, toot,
Elephants are cute!

[Chorus]
What does the animal say? Let's play!
Listen close and sing the sound today!
Roar and toot and neigh, hooray!
What does the animal say?

[Giraffe]
The giraffe is very quiet, shh, shh, shh,
She hums so soft, hmm, hmm, hmm!
Hum, hum, hum,
Giraffes hum, yum!

[Zebra]
The zebra says neigh, bray, bray!
Like a little horse that loves to play!
The hippo says honk, grunt, honk,
Splash in the river, plonk, plonk, plonk!

[Bridge]
Roar like a lion, roar!
Toot like an elephant, toot!
Neigh like a zebra, neigh!
Honk like a hippo, honk!

[Chorus]
What does the animal say? Let's play!
Listen close and sing the sound today!
Roar and toot and neigh, hooray!
What does the animal say?

[Outro]
Roar, toot, neigh, honk! Bye-bye, friends!""",
  props={"chorus1": [T("ANIMAL SOUNDS!", "#ffb627", size=0.6)], "lion1": [T("ROAR!", "#ff7a00", "roar", at=[-3.6, -0.3, 2.5], size=0.6)],
         "elephant1": [T("TOOT!", "#5d6b8f", "toot", at=[3.4, 0.4, 3.0], size=0.6)], "chorus2": [T("ANIMAL SOUNDS!", "#ffb627", size=0.6)],
         "giraffe1": [T("HMM...", "#b8692c", "hums", at=[3.2, 1.0, 3.0], size=0.5)], "zebra1": [T("NEIGH!", "#25232b", "neigh", at=[3.6, 0.3, 2.6], size=0.5), T("HONK!", "#6e5aa8", "honk", at=[-3.6, 0.3, 2.6], size=0.5)],
         "bridge1": [T("ROAR!", "#ff7a00", "roar", at=[-3.4, 0.3, 3.5], size=0.7), T("TOOT!", "#5d6b8f", "toot", at=[3.4, 0.3, 3.5], size=0.7), T("NEIGH!", "#25232b", "neigh", at=[-1.3, 0.6, 4.3], size=0.7), T("HONK!", "#6e5aa8", "honk", at=[1.3, 0.6, 4.3], size=0.7)],
         "chorus3": [T("ANIMAL SOUNDS!", "#ffb627", size=0.6)], "outro1": [T("BYE-BYE!", "#ffb627")]},
  meta={"title": "Animal Sounds Song for Kids! Roar, Toot, Neigh with Milo", "card": "Animal Sounds Song!", "thumb_text": "ANIMAL SOUNDS!",
        "description": "What does the animal say? Sing the Animal Sounds Song with Milo on the savanna: the lion roars, the elephant toots, the zebra brays and the hippo honks.\nFun fact: giraffes are very quiet, and scientists think they hum at night! Kids copy every sound. Ages 2-6.",
        "tags": ["animal sounds song", "animal sounds for kids", "what does the animal say", "safari animals", "zoo animals for kids", "kids songs", "nursery rhymes", "The Animated Zoo", "Milo"]}))

# Moon: Ten Sleepy Sheep counting lullaby
p = B2("mb3d_ep02")
star = lambda w, n, x: P("numstar", w, at=[x, 2.4, 3.2], opts={"n": n})
specs.append(dict(id="mb3d_ep03", base=p,
  lyrics="""[Chorus]
Count the sleepy sheep, one, two, three,
Jumping softly over the fence for me,
Close your eyes and count with me,
Sleepy sheep, sleepy sheep.

[Verse 1]
One little sheep jumps over the hill,
Two little sheep, so soft and still,
Three little sheep yawn and say,
Goodnight, goodnight, the end of day.

[Chorus]
Count the sleepy sheep, one, two, three,
Jumping softly over the fence for me,
Close your eyes and count with me,
Sleepy sheep, sleepy sheep.

[Verse 2]
Four little sheep in the silver light,
Five little sheep, cuddled up tight,
Luna the owl says hoo, hoo, hoo,
The sheep are sleepy, and so are you.

[Bridge]
Breathe in, one, and breathe out, two,
Wiggle your toes, and stretch them too,
Fluffy pillow, cozy bed,
Rest your sleepy little head.

[Verse 3]
Teddy's counting, lamb counts too,
Bunny's counting, just like you,
One, two, three, four, five, so deep,
Now it's time to fall asleep.

[Chorus]
Count the sleepy sheep, one, two, three,
Jumping softly over the fence for me,
Close your eyes and count with me,
Sleepy sheep, sleepy sheep.

[Outro]
Sleepy sheep, goodnight. Goodnight.""",
  props={"chorus1": [T("Sleepy Sheep", "#ffd88a", size=0.7), P("moon", None, at="top", delay=2)], "verse1": [star("one", 1, -3.0), star("two", 2, -1.5), star("three", 3, 0.0)],
         "chorus2": [T("Sleepy Sheep", "#ffd88a", size=0.7)], "verse2": [star("four", 4, 1.5), star("five", 5, 3.0), P("moon", "silver", at="top")],
         "bridge1": [T("Breathe...", "#bfa8ff", "breathe", size=0.6), P("zzz", "rest", at="right")], "verse3": [P("zzz", "asleep", at="left"), P("heart", "teddy", at="right")],
         "chorus3": [T("Goodnight", "#ffd88a", size=0.7)], "outro1": [P("zzz", None, at="right")]},
  meta={"title": "Count the Sleepy Sheep 🌙 Lullaby for Babies | Moonbeam", "card": "Sleepy Sheep", "thumb_text": "SLEEPY SHEEP",
        "description": "Count the Sleepy Sheep, a calm counting lullaby for babies and kids. Count 1 to 5 sleepy sheep with Luna the owl, Teddy, Lamb and Bunny.\nSoft music box and piano with slow breathing to help little ones fall asleep. Ages 0-6.",
        "tags": ["lullaby for babies", "counting sheep", "sleepy sheep song", "bedtime song", "sleep music for kids", "goodnight song", "baby sleep", "Moonbeam Bedtime", "3D kids songs"]}))

# Gizmo: Sink or Float?
g = json.load(open("/root/zoo/specs/out/gz3d_ep02.song.json"))
specs.append(dict(id="gz3d_ep03", base=g,
  lyrics="""[Chorus]
Sink or float? Sink or float?
Will it sink like a rock or float like a boat?
Drop it in and take a look,
Sink or float? Let's find out!

[Verse 1]
A rubber duck goes in, plop, plop,
It floats right up on the very top!
A heavy rock goes in, kerplunk,
Down, down, down, the rock has sunk!

[Verse 2]
A leaf is light, it floats away,
A coin goes down, it sinks today!
An apple bobs, it floats, hooray,
A spoon sinks down, it will not stay!

[Chorus]
Sink or float? Sink or float?
Will it sink like a rock or float like a boat?
Drop it in and take a look,
Sink or float? Let's find out!

[Verse 3]
Things that float push water away,
Air inside helps them stay!
Heavy, small and packed in tight,
Those things sink, that's right!

[Bridge]
Float like a boat, arms out wide!
Sink like a rock, squat down low!
Float back up, stand up tall!
Splash, splash, splash, that's all!

[Chorus]
Sink or float? Sink or float?
Will it sink like a rock or float like a boat?
Drop it in and take a look,
Sink or float? Let's find out!

[Outro]
Sink or float! Bye-bye, scientists!""",
  props={"chorus1": [T("SINK OR FLOAT?", "#3b8be0", size=0.6), P("beaker", None, at=[0, 1.2, 3.4], delay=1)], "verse1": [T("FLOATS!", "#2fb59a", "floats", at=[-3.2, 1.4, 3.6], size=0.7), T("SINKS!", "#e8302a", "sunk", at=[3.2, 1.4, 3.6], size=0.7)],
         "verse2": [T("FLOAT", "#2fb59a", "floats", at=[-3.2, 1.4, 3.6], size=0.7), T("SINK", "#e8302a", "sinks", at=[3.2, 1.4, 3.6], size=0.7)],
         "chorus2": [T("SINK OR FLOAT?", "#3b8be0", size=0.6)], "verse3": [P("beaker", "water", at=[-2.8, 1.0, 3.4]), T("AIR!", "#9fd8ff", "air", at=[2.8, 1.4, 3.6], size=0.7)],
         "bridge1": [T("FLOAT!", "#2fb59a", "float", at=[-3.4, 0.3, 3.5], size=0.7), T("SINK!", "#e8302a", "sink", at=[3.4, 0.3, 3.5], size=0.7), T("SPLASH!", "#3db8ff", "splash", at=[0, 0.6, 4.3], size=0.7)],
         "chorus3": [T("SINK OR FLOAT?", "#3b8be0", size=0.6)], "outro1": [T("BYE-BYE!", "#3b8be0")]},
  meta={"title": "Sink or Float? Science Song for Kids with Gizmo the Robot", "card": "Sink or Float?", "thumb_text": "SINK OR FLOAT?",
        "description": "Sink or float? Sing along with Gizmo the robot and test a rubber duck, a rock, a leaf, a coin, an apple and a spoon.\nA first science experiment song: kids learn that floating things push water away and have air inside. Act it out: float like a boat, sink like a rock! Ages 3-6.",
        "tags": ["sink or float", "science for kids", "science song", "experiments for kids", "preschool science", "kids songs", "Gizmo Explains", "3D kids songs"]}))

for s in specs:
    base = s["base"]; spec = copy.deepcopy(base)
    spec["lyrics"] = s["lyrics"]; spec["meta"] = s["meta"]; spec["seed"] = base["seed"] + 100
    spec["style"] = base["style"].replace("vocals start right away on the first beat, no long intro, short outro", NOINTRO)
    spec.pop("color_words", None); spec.pop("color_char", None)
    if s.get("color_words"): spec["color_words"] = dict(s["color_words"], **s.get("extra_colors", {})); spec["color_char"] = "host"
    job = spec["job"]; job["id"] = s["id"]; job["song"] = s["id"]; job["title"] = s["meta"]["card"]
    job["res"] = "1920x1080"; job["step"] = 1
    for c in job["cast"]: c.get("opts", {}).pop("color_schedule", None)
    if s["id"].startswith("bl"): job["cast"][0]["opts"]["color"] = "#9d6bff"
    names = [d["section"] for d in job["direct"]]
    job["direct"] = [dict(d, props=s["props"].get(d["section"], [])) for d in job["direct"]]
    assert set(s["props"]) <= set(names), (s["id"], set(s["props"]) - set(names))
    assert len(s["meta"]["title"]) <= 60, s["meta"]["title"]
    json.dump(spec, open(f"/root/zoo/specs/b3/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]), names)
