import json, copy, re, sys
sys.path.insert(0, "/root/zoo/blender/zoo3d"); import timing_lib as TL
Z = "/root/zoo/blender/zoo3d"
B3 = lambda n: json.load(open(f"/root/zoo/specs/b5/{n}.song.json"))
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
L = lambda x: [-3.4, 0.3, 3.5] if x == "l" else [3.4, 0.3, 3.5] if x == "r" else [0, 0.6, 4.3]
specs = []

specs.append(dict(id="bl3d_ep08", base="bl3d_ep05", colors={"yellow": "#ffd21f"},
  lyrics="""[Chorus]
Bloop turns yellow, yellow, yellow!
Bright and happy, sunny fellow!
Yellow like the sun up high,
Yellow, yellow, wave hi!

[Verse 1]
A yellow banana, peel, peel, peel,
Yellow banana, what a meal!
A yellow duck goes quack, quack, quack,
Swimming out and swimming back!

[Chorus]
Bloop turns yellow, yellow, yellow!
Bright and happy, sunny fellow!
Yellow like the sun up high,
Yellow, yellow, wave hi!

[Verse 2]
A yellow school bus, beep, beep, beep,
A yellow chick goes cheep, cheep, cheep!
Yellow lemons, sour and bright,
Pucker up and take a bite!

[Bridge]
Find something yellow, look around!
Point to yellow, up and down!
Clap your hands and shout hooray,
Yellow is the color of the day!

[Verse 3]
Yellow flowers in the sun,
Yellow stars for everyone!
Yellow and blue make green, it's true,
Yellow is happy, just like you!

[Chorus]
Bloop turns yellow, yellow, yellow!
Bright and happy, sunny fellow!
Yellow like the sun up high,
Yellow, yellow, wave hi!

[Outro]
Yellow, yellow! Bye-bye, friends!""",
  props={"chorus1": [T("YELLOW!", "#ffd21f", size=0.9)], "verse1": [P("banana", "banana,", at=[-3.4, 0.9, 3.6]), T("QUACK!", "#ffd21f", "quack,", at=[3.4, 1.4, 3.6], size=0.6)],
         "chorus2": [P("sun", None, at=[0, 1.9, 3.4], delay=1)], "verse2": [T("BEEP BEEP!", "#ffd21f", "beep,", at=[-3.4, 1.4, 3.6], size=0.6), T("CHEEP!", "#ffb000", "cheep,", at=[3.4, 1.4, 3.6], size=0.6)],
         "bridge1": [T("FIND YELLOW!", "#ffd21f", "find", size=0.7), T("HOORAY!", "#ff8a1f", "hooray,", at=L("c"), size=0.7)],
         "verse3": [P("flower", "flowers", at=[-3.4, 0.9, 3.6], opts={"color": "#ffd21f"}), T("YELLOW + BLUE = GREEN", "#3cc45a", "blue", size=0.45)],
         "chorus3": [T("YELLOW!", "#ffd21f", size=0.9)], "outro1": [T("BYE-BYE!", "#ffd21f")]},
  meta={"title": "Bloop Turns Yellow! Yellow Color Song for Kids | Part 4", "card": "Bloop Turns Yellow!", "thumb_text": "BLOOP TURNS YELLOW!",
        "description": "Bloop turns yellow! Part 4 of Bloop's color song series: a yellow banana, a yellow duck, a school bus, a little chick, sour lemons and sunny flowers.\nKids find something yellow, point to yellow and learn that yellow and blue make green. Ages 2-5.",
        "tags": ["yellow color song", "learn colors", "color songs for kids", "colors for toddlers", "kids songs", "Bloop's Color Lab", "3D kids songs"]}))

specs.append(dict(id="tt3d_ep08", base="tt3d_ep05",
  lyrics="""[Chorus]
Dig, lift, mix and build!
Construction trucks are very skilled!
Rumble, rumble, work all day,
Building trucks are on their way!

[Verse 1]
The digger digs a great big hole,
Scoop by scoop, that's the goal!
Down goes the bucket, up comes the dirt,
Digging, digging, hard at work!

[Chorus]
Dig, lift, mix and build!
Construction trucks are very skilled!
Rumble, rumble, work all day,
Building trucks are on their way!

[Verse 2]
The crane lifts beams up to the sky,
Higher, higher, way up high!
The cement mixer turns around,
Pour the cement on the ground!

[Bridge]
Dig like a digger, scoop, scoop, scoop!
Lift like a crane, up, up, up!
Spin like a mixer, round and round,
Stomp like a roller on the ground!

[Verse 3]
The roller rolls the road out flat,
Smooth and shiny, just like that!
Hard hats on and safety first,
Building trucks are the very best!

[Chorus]
Dig, lift, mix and build!
Construction trucks are very skilled!
Rumble, rumble, work all day,
Building trucks are on their way!

[Outro]
Dig, lift, build! Bye-bye, friends!""",
  props={"chorus1": [T("DIG! LIFT! MIX!", "#ffc107", size=0.7)], "verse1": [T("DIG!", "#ffc107", "digs", at=[-2.8, 1.6, 3.6], size=0.7), T("SCOOP!", "#8a5a32", "scoop", at=[2.8, 1.6, 3.6], size=0.6)],
         "chorus2": [T("RUMBLE!", "#ff8a1f", size=0.7)], "verse2": [T("UP HIGH!", "#3b8be0", "higher,", size=0.7), T("ROUND!", "#9e9e9e", "around,", at=L("c"), size=0.6)],
         "bridge1": [T("SCOOP!", "#ffc107", "scoop,", at=L("l"), size=0.6), T("UP!", "#3b8be0", "up,", at=L("r"), size=0.7), T("STOMP!", "#e8302a", "stomp", at=L("c"), size=0.6)],
         "verse3": [P("helmet", "hats", at=[-3.0, 1.0, 3.6]), P("cone", "safety", at=[3.0, 0.4, 3.6])],
         "chorus3": [T("BUILD!", "#ffc107", size=0.8)], "outro1": [T("BYE-BYE!", "#ffc107")]},
  meta={"title": "Construction Trucks Song! Dig, Lift, Mix | Tiny Truck Town", "card": "Construction Trucks!", "thumb_text": "DIG! LIFT! MIX!",
        "description": "Meet the construction trucks! The digger digs a hole, the crane lifts beams up high, the cement mixer spins and the roller makes the road flat.\nKids scoop like a digger, lift like a crane, spin like a mixer and stomp like a roller. Hard hats on, safety first! Ages 2-5.",
        "tags": ["construction trucks song", "digger song", "crane song", "cement mixer", "trucks for kids", "kids songs", "Tiny Truck Town", "3D kids songs"]}))

specs.append(dict(id="fr3d_ep09", base="fr3d_ep06",
  lyrics="""[Chorus]
Crunchy, crunchy veggies, crunch, crunch, crunch!
Veggies make a yummy lunch!
Carrots, peas and broccoli,
Veggies help me grow, you see!

[Verse 1]
Orange carrot, long and thin,
Crunch it up and give a grin!
Carrots help my eyes see bright,
Morning, noon and every night!

[Chorus]
Crunchy, crunchy veggies, crunch, crunch, crunch!
Veggies make a yummy lunch!
Carrots, peas and broccoli,
Veggies help me grow, you see!

[Verse 2]
Broccoli, like a little tree,
Green and strong, it's good for me!
Little peas, all round and green,
The tiniest veggies I have seen!

[Bridge]
Pull a carrot, pull, pull, pull!
Pick some peas, my basket's full!
Grow up tall like a broccoli tree,
Veggie power, one, two, three!

[Verse 3]
Red tomatoes, juicy too,
Corn so yellow, just for you!
Try a bite, it's fun to taste,
Veggies never go to waste!

[Chorus]
Crunchy, crunchy veggies, crunch, crunch, crunch!
Veggies make a yummy lunch!
Carrots, peas and broccoli,
Veggies help me grow, you see!

[Outro]
Crunch, crunch, crunch! Bye-bye, friends!""",
  props={"chorus1": [T("CRUNCH!", "#ff8418", size=0.8)], "verse1": [P("bigfruit", "carrot,", at=[-2.6, 0.9, 3.4], opts={"kind": "carrot"}), T("SEE BRIGHT!", "#ff8418", "eyes", at=[2.6, 1.5, 3.4], size=0.55)],
         "chorus2": [T("YUM YUM!", "#3cc45a", size=0.7)], "verse2": [P("bigfruit", "broccoli,", at=[-2.6, 0.9, 3.4], opts={"kind": "broccoli"}), T("STRONG!", "#2e9440", "strong,", at=[2.6, 1.5, 3.4], size=0.6)],
         "bridge1": [T("PULL!", "#ff8418", "pull", at=L("l"), size=0.7), P("basket", "basket's", at=[2.6, 0.8, 3.4]), T("VEGGIE POWER!", "#3cc45a", "power,", at=L("c"), size=0.55)],
         "verse3": [T("TRY A BITE!", "#ff5c8a", "try", size=0.6), P("plate", "taste,", at=[0, 0.8, 3.4])],
         "chorus3": [T("CRUNCH!", "#ff8418", size=0.8)], "outro1": [T("BYE-BYE!", "#ff8418")]},
  meta={"title": "Crunchy Veggies Song! Vegetables for Kids | Fruity Friends", "card": "Crunchy Veggies!", "thumb_text": "CRUNCH CRUNCH!",
        "description": "Crunch, crunch, crunch! The Fruity Friends sing about vegetables: crunchy orange carrots, broccoli that looks like a little tree, tiny green peas, juicy tomatoes and yellow corn.\nKids pull carrots, pick peas and learn that trying a new veggie is fun. Ages 2-5.",
        "tags": ["vegetables song", "veggies for kids", "healthy eating song", "carrot song", "broccoli song", "kids songs", "Fruity Friends", "3D kids songs"]}))

specs.append(dict(id="zoo3d_ep08", base="zoo3d_ep05",
  lyrics="""[Chorus]
Stripes and spots and fluffy manes,
Every animal looks different, not the same!
Look so close, what do you see?
Animal patterns, one, two, three!

[Verse 1]
Zebra has stripes, black and white,
Stripes on the left, stripes on the right!
Giraffe has spots, brown and tan,
Count the spots if you can!

[Chorus]
Stripes and spots and fluffy manes,
Every animal looks different, not the same!
Look so close, what do you see?
Animal patterns, one, two, three!

[Verse 2]
Lion has a mane, big and round,
Shake it, shake it, all around!
Elephant has wrinkly skin,
Big gray ears and a happy grin!

[Bridge]
Wiggle like a zebra, stripe, stripe, stripe!
Stretch like a giraffe, way up high!
Shake like a lion, shake your mane,
Flap your ears and do it again!

[Verse 3]
Hippo is smooth and purple too,
Milo has feathers, bright and blue!
Every friend is special, it's true,
Just like me and just like you!

[Chorus]
Stripes and spots and fluffy manes,
Every animal looks different, not the same!
Look so close, what do you see?
Animal patterns, one, two, three!

[Outro]
Stripes and spots! Bye-bye, friends!""",
  props={"chorus1": [T("STRIPES & SPOTS!", "#ffb627", size=0.6)], "verse1": [P("sign", "Zebra", at=[3.2, 1.6, 3.6], opts={"text": "ZEBRA"}), P("sign", "Giraffe", at=[-3.2, 1.6, 3.6], opts={"text": "GIRAFFE"})],
         "chorus2": [T("LOOK CLOSE!", "#ff7a00", size=0.7)], "verse2": [P("sign", "Lion", at=[-3.2, 1.6, 3.6], opts={"text": "LION"}), P("sign", "Elephant", at=[3.2, 1.6, 3.6], opts={"text": "ELEPHANT"})],
         "bridge1": [T("WIGGLE!", "#333333", "wiggle", at=L("l"), size=0.6), T("STRETCH!", "#ffb627", "stretch", at=L("r"), size=0.6), T("SHAKE!", "#ff7a00", "shake", at=L("c"), size=0.6)],
         "verse3": [P("heart", "special,", at=[0, 1.9, 3.4]), T("SPECIAL!", "#ff5c8a", "true,", size=0.6)],
         "chorus3": [T("STRIPES & SPOTS!", "#ffb627", size=0.6)], "outro1": [T("BYE-BYE!", "#ffb627")]},
  meta={"title": "Stripes and Spots! Animal Patterns Song for Kids with Milo", "card": "Stripes and Spots!", "thumb_text": "STRIPES & SPOTS!",
        "description": "Stripes, spots and fluffy manes! Milo and the zoo friends look closely at animal patterns: the zebra's black and white stripes, the giraffe's spots, the lion's mane and the elephant's wrinkly skin.\nKids wiggle like a zebra, stretch like a giraffe and shake like a lion, and learn that every friend is special. Ages 2-5.",
        "tags": ["animal patterns song", "zebra stripes", "giraffe spots", "animal song for kids", "safari animals", "kids songs", "The Animated Zoo", "Milo", "3D kids songs"]}))

specs.append(dict(id="mb3d_ep08", base="mb3d_ep05",
  lyrics="""[Chorus]
Sleepy little ducky, splash, splash, splash,
Bath time bubbles, a gentle wash,
Warm and cozy, dry and clean,
Off to bed to sweetly dream.

[Verse 1]
Bubbles floating, round and light,
Ducky paddles left and right,
Wash your toes and wash your nose,
Soft and slow the water flows.

[Chorus]
Sleepy little ducky, splash, splash, splash,
Bath time bubbles, a gentle wash,
Warm and cozy, dry and clean,
Off to bed to sweetly dream.

[Verse 2]
Fluffy towel, wrap you tight,
Brush your teeth, so clean and bright,
Pajamas on, so soft and new,
Bunny and lamb are sleepy too.

[Bridge]
Breathe in slowly, like a bubble grows,
Breathe out softly, gently goes,
One more yawn and one more sigh,
Close your eyes, the moon is high.

[Verse 3]
A little story, a goodnight kiss,
Snuggle deep in sleepy bliss,
Ducky's dreaming on the shelf,
Time to dream now, like yourself.

[Chorus]
Sleepy little ducky, splash, splash, splash,
Bath time bubbles, a gentle wash,
Warm and cozy, dry and clean,
Off to bed to sweetly dream.

[Outro]
Goodnight, little ducky. Goodnight.""",
  props={"chorus1": [T("Sleepy Little Ducky", "#ffd88a", size=0.5), P("duck", None, at="right", delay=2)], "verse1": [P("bubbles", "Bubbles", at="left")],
         "chorus2": [P("duck", "ducky,", at="right")], "verse2": [P("toothbrush", "teeth,", at="left"), P("heart", "sleepy", at="right")],
         "bridge1": [T("Breathe...", "#bfa8ff", "breathe", size=0.6), P("moon", "moon", at="top")], "verse3": [P("book", "story,", at="left"), P("zzz", "dreaming", at="right")],
         "outro1": [P("zzz", "Goodnight,", at="right")]},
  meta={"title": "Sleepy Little Ducky 🌙 Bath and Bedtime Lullaby | Moonbeam", "card": "Sleepy Little Ducky", "thumb_text": "SLEEPY LITTLE DUCKY",
        "description": "A gentle bath and bedtime lullaby. Luna, Bunny and Lamb float bubbles with a sleepy rubber ducky, wrap up in a fluffy towel, brush their teeth, put on pajamas and hear a little story.\nA slow breathing break helps little ones wind down for sleep. For babies and toddlers.",
        "tags": ["bedtime lullaby", "bath time song", "lullaby for babies", "bedtime routine song", "sleep music for kids", "Moonbeam Bedtime", "3D kids songs"]}))

specs.append(dict(id="gz3d_ep08", base="gz3d_ep05",
  lyrics="""[Chorus]
Magnets, magnets, pull and push!
Some things stick with a whoosh!
Metal paper clips go click,
Magnets make the metal stick!

[Verse 1]
A magnet has an invisible pull,
It grabs the metal, that's magical!
A spoon, a key, a paper clip,
They jump right up and stick, stick, stick!

[Chorus]
Magnets, magnets, pull and push!
Some things stick with a whoosh!
Metal paper clips go click,
Magnets make the metal stick!

[Verse 2]
But wood and plastic, paper too,
Magnets can't pull those, it's true!
Only metal like iron will do,
Try it out and see for you!

[Bridge]
North and south, they come together, click!
North and north, they push apart, quick!
Pull your arms in, push them out,
Magnet power, give a shout!

[Verse 3]
Magnets hold your art up high,
On the fridge where it won't fly!
A compass needle points the way,
Magnets help us every day!

[Chorus]
Magnets, magnets, pull and push!
Some things stick with a whoosh!
Metal paper clips go click,
Magnets make the metal stick!

[Outro]
Magnets! Bye-bye, friends!""",
  props={"chorus1": [T("MAGNETS!", "#e53935", size=0.8), P("magnet", None, at=[-3.0, 1.3, 3.6], delay=1)],
         "verse1": [P("magnet", "magnet", at=[-3.0, 1.3, 3.6]), T("STICK!", "#e53935", "stick,", at=[3.0, 1.5, 3.6], size=0.7)],
         "chorus2": [T("PULL & PUSH!", "#3b8be0", size=0.7)], "verse2": [T("METAL ONLY!", "#9e9e9e", "metal", size=0.6)],
         "bridge1": [T("CLICK!", "#3b8be0", "together,", at=L("l"), size=0.7), T("PUSH!", "#e53935", "apart,", at=L("r"), size=0.7), T("MAGNET POWER!", "#ffc107", "power,", at=L("c"), size=0.55)],
         "verse3": [T("COMPASS!", "#3b8be0", "compass", size=0.6), P("star", "way,", at=[3.0, 1.6, 3.6])],
         "chorus3": [T("MAGNETS!", "#e53935", size=0.8)], "outro1": [T("BYE-BYE!", "#e53935")]},
  meta={"title": "How Do Magnets Work? Science Song for Kids with Gizmo", "card": "Magnets!", "thumb_text": "HOW MAGNETS WORK!",
        "description": "How do magnets work? Gizmo the robot shows that magnets pull metal things like spoons, keys and paper clips, but not wood, plastic or paper. North and south stick together; north and north push apart.\nKids pull and push like magnets and learn how magnets hold art on the fridge and help a compass point the way. Ages 3-6.",
        "tags": ["magnets song", "how magnets work", "science song for kids", "magnets for kids", "STEM for kids", "kids songs", "Gizmo Explains", "3D kids songs"]}))
for s in specs:
    base = B3(s["base"]); spec = copy.deepcopy(base)
    spec["lyrics"] = s["lyrics"]; spec["meta"] = s["meta"]; spec["seed"] = base["seed"] + 300
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
    json.dump(spec, open(f"/root/zoo/specs/b8/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]), secs)
