import json, copy, os
Z = "/root/zoo/blender/zoo3d"
J = lambda n: json.load(open(f"{Z}/jobs/{n}.json"))
NOINTRO = "vocals start right away on the first beat, no long intro, short outro"
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
specs = []

# ---- Bloop: Shapes Song (Bloop changes color on each shape word; shape friends)
bl_cast = J("bl3d_ep01_v3")["cast"]; bl_cast[0]["opts"].pop("color_schedule", None)
bl_cast.append({"id": "triangle", "char": "shape", "spot": "farright", "opts": {"shape": "triangle", "color": "#3ccf4e", "scale": 0.75}, "yaw": -0.35})
SC = {"circle": "#ff3b3b", "square": "#3d8bff", "triangle": "#3ccf4e", "star": "#ffd21f", "heart": "#ff4f7b"}
specs.append(dict(id="bl3d_ep02", job="bl3d_ep02", channel="bloop", set="colorlab", cast=bl_cast, color_words=SC, color_char="host",
  style="upbeat preschool kids pop sing-along, cheerful sweet female vocal, clear diction, bright ukulele, glockenspiel, handclaps, bouncy bass, major key, catchy repetitive chorus, " + NOINTRO,
  bpm=116, key="G Major", duration=150, seed=31,
  lyrics="""[Chorus]
Shapes, shapes, look around!
Shapes are everywhere I've found!
Circle, square, triangle, star,
Shapes, shapes, there you are!

[Verse 1]
A circle is round, round, round,
Like a ball that bounces up and down!
A square has four sides, one, two, three, four,
Like a window or a door!

[Chorus]
Shapes, shapes, look around!
Shapes are everywhere I've found!
Circle, square, triangle, star,
Shapes, shapes, there you are!

[Verse 2]
A triangle has three sides, three!
Like a slice of pizza, yum, for me!
A star has five points shining bright,
Twinkle, twinkle in the night!

[Bridge]
Draw a circle in the air!
Draw a square right over there!
Make a triangle, up and down!
Jump up high and spin around!

[Verse 3]
A heart is for love, hug, hug, hug!
Give your friends a great big hug!
Bloop can change from shape to shape,
Now you know them, isn't it great?

[Chorus]
Shapes, shapes, look around!
Shapes are everywhere I've found!
Circle, square, triangle, star,
Shapes, shapes, there you are!

[Outro]
Circle, square, triangle, star! Bye-bye!""",
  direct=[{"section": "chorus1", "shots": ["wide", "close:host", "orbit", "low"], "energy": 0.9, "group": True, "wave": 1, "props": [T("SHAPES!", "#ff5c8a", size=0.9)]},
          {"section": "verse1", "shots": ["close:host", "wide", "close:square", "close:host"], "energy": 0.75,
           "props": [T("CIRCLE", SC["circle"], "circle", at=[-4.4, 0.6, 3.8], size=0.9), P("balloon", "ball", at=[-4.4, 0.4, 2.6], opts={"color": "red"}),
                     T("SQUARE", SC["square"], "square", at=[4.4, 0.6, 3.8], size=0.9), P("block", "window", at=[4.4, 0.4, 2.6], opts={"color": "blue"})]},
          {"section": "chorus2", "shots": ["orbit", "close:host", "wide", "low"], "energy": 0.9, "group": True, "props": [T("SHAPES!", "#ff5c8a", size=0.9)]},
          {"section": "verse2", "shots": ["close:triangle", "wide", "close:star", "close:host"], "energy": 0.75,
           "props": [T("TRIANGLE", SC["triangle"], "triangle", at=[-4.2, 0.6, 3.8], size=0.75), T("STAR", SC["star"], "star", at=[4.4, 0.6, 3.8], size=0.9),
                     P("sun", "bright", at=[4.4, 0.4, 2.6])]},
          {"section": "bridge1", "shots": ["wide", "low", "orbit", "wide"], "energy": 1.0, "group": True, "wave": 1, "jump": 0.5,
           "props": [T("DRAW!", "#ff5c8a", "draw", at=[-3.4, 0.3, 3.5], size=0.7), T("JUMP!", "#3ccf4e", "jump", at=[3.4, 0.3, 3.5], size=0.7),
                     T("SPIN!", "#3d8bff", "spin", at=[0, 0.6, 4.3], size=0.7)]},
          {"section": "verse3", "shots": ["close:heart", "close:host", "wide", "close:host"], "energy": 0.8,
           "props": [T("HEART", SC["heart"], "heart", at=[-4.4, 0.6, 3.8], size=0.9), P("rainbow", "great", at="top")]},
          {"section": "chorus3", "shots": ["low", "close:host", "orbit", "wide"], "energy": 1.0, "group": True, "wave": 1, "props": [T("SHAPES!", "#ff5c8a", size=0.9)]},
          {"section": "outro1", "shots": ["wide"], "energy": 0.6, "group": True, "wave": 1, "props": [T("BYE-BYE!", "#ff5c8a", size=0.8)]}],
  meta={"title": "Shapes Song for Kids! Circle, Square, Triangle with Bloop", "card": "The Shapes Song!", "thumb_text": "SHAPES SONG!",
        "description": "The Shapes Song for kids! Sing along with Bloop the jelly blob and the shape friends: circle, square, triangle, star and heart.\nKids learn shape names and how many sides each one has, then draw shapes in the air, jump and spin. Ages 2-5.",
        "tags": ["shapes song", "shapes for kids", "learn shapes", "circle square triangle", "preschool songs", "kids songs", "nursery rhymes", "Bloop's Color Lab", "3D kids songs"]}))

# ---- Truck: Stop and Go traffic light song
specs.append(dict(id="tt3d_ep02", job="tt3d_ep02", channel="truck", set="town", cast=J("tt3d_ep01_v3")["cast"],
  style="upbeat preschool kids pop rock sing-along, cheerful friendly young male vocal, clear diction, electric guitar, handclaps, car horn sounds, bouncy drums, major key, catchy repetitive chorus, " + NOINTRO,
  bpm=120, key="D Major", duration=150, seed=12,
  lyrics="""[Chorus]
Red means stop! Yellow, slow!
Green means go, go, go!
Traffic light, traffic light,
Keeps us safe, day and night!

[Verse 1]
Red light, red light, stop right here,
Wait, wait, wait until it's clear!
Brakes go squeak, and we stand still,
Stop, stop, stop, we always will!

[Chorus]
Red means stop! Yellow, slow!
Green means go, go, go!
Traffic light, traffic light,
Keeps us safe, day and night!

[Verse 2]
Yellow light, yellow light, slowing down,
Careful, careful, all around!
Green light, green light, off we zoom,
Beep, beep, beep, now make some room!

[Bridge]
When it's red, freeze like a statue!
When it's yellow, tiptoe slow!
When it's green, run in place, run, run!
Honk, honk, beep, beep, here we go!

[Verse 3]
Hold a grown-up's hand so tight,
Look left, look right, then left and right!
Cross the street when the walk light's on,
Safe and sound, we sing this song!

[Chorus]
Red means stop! Yellow, slow!
Green means go, go, go!
Traffic light, traffic light,
Keeps us safe, day and night!

[Outro]
Stop, slow, go! Bye-bye, friends!""",
  direct=[{"section": "chorus1", "shots": ["wide", "close:host", "orbit", "low"], "energy": 0.9, "group": True, "wave": 1,
           "props": [T("STOP!", "#e8302a", "stop", at=[-3.4, 1.6, 3.6]), T("SLOW", "#ffc107", "slow", at=[0, 2.0, 3.6]), T("GO!", "#2fb54a", "go", at=[3.4, 1.6, 3.6])]},
          {"section": "verse1", "shots": ["close:host", "wide", "close:police", "close:host"], "energy": 0.6,
           "props": [T("STOP!", "#e8302a", "stop", size=0.9), P("cone", "wait", at=[-2.8, 0, 3.4]), P("cone", "clear", at=[2.8, 0, 3.4])]},
          {"section": "chorus2", "shots": ["orbit", "close:host", "wide", "low"], "energy": 0.9, "group": True,
           "props": [T("STOP!", "#e8302a", "stop", at=[-3.4, 1.6, 3.6]), T("SLOW", "#ffc107", "slow", at=[0, 2.0, 3.6]), T("GO!", "#2fb54a", "go", at=[3.4, 1.6, 3.6])]},
          {"section": "verse2", "shots": ["close:dump", "wide", "close:host", "close:garbage"], "energy": 0.85,
           "props": [T("SLOW", "#ffc107", "yellow", size=0.9), T("GO!", "#2fb54a", "green", nth=0, at=[0, 1.8, 3.6], size=0.9, delay=2.0)]},
          {"section": "bridge1", "shots": ["wide", "low", "orbit", "wide"], "energy": 1.0, "group": True, "jump": 0.4,
           "props": [T("FREEZE!", "#e8302a", "freeze", at=[-3.4, 0.6, 3.5], size=0.7), T("TIPTOE!", "#ffc107", "tiptoe", at=[3.4, 0.6, 3.5], size=0.7),
                     T("RUN!", "#2fb54a", "run", at=[0, 0.9, 4.2], size=0.7)]},
          {"section": "verse3", "shots": ["close:host", "wide", "close:police", "close:host"], "energy": 0.6,
           "props": [T("LOOK LEFT", "#3b8be0", "left", at=[-3.2, 1.4, 3.6], size=0.55), T("LOOK RIGHT", "#3b8be0", "right", at=[3.2, 1.4, 3.6], size=0.55)]},
          {"section": "chorus3", "shots": ["low", "close:host", "orbit", "wide"], "energy": 1.0, "group": True, "wave": 1,
           "props": [T("STOP!", "#e8302a", "stop", at=[-3.4, 1.6, 3.6]), T("SLOW", "#ffc107", "slow", at=[0, 2.0, 3.6]), T("GO!", "#2fb54a", "go", at=[3.4, 1.6, 3.6])]},
          {"section": "outro1", "shots": ["wide"], "energy": 0.6, "group": True, "wave": 1, "props": [T("BYE-BYE!", "#e8302a")]}],
  meta={"title": "Traffic Light Song for Kids! Red Means Stop with Bolt", "card": "Stop and Go Song!", "thumb_text": "STOP & GO!",
        "description": "The Traffic Light Song for kids! Red means stop, yellow means slow, green means go. Sing along with Bolt the fire truck and friends in Tiny Truck Town.\nKids learn traffic light colors and road safety: hold a grown-up's hand and look left and right. Ages 2-6.",
        "tags": ["traffic light song", "red light green light", "stop and go song", "road safety for kids", "trucks for kids", "kids songs", "nursery rhymes", "Tiny Truck Town", "3D kids songs"]}))

# ---- Fruity: Banana Dance
fr_cast = J("fr3d_ep02")["cast"]
specs.append(dict(id="fr3d_ep03", job="fr3d_ep03", channel="fruity", set="kitchen", cast=fr_cast,
  style="upbeat preschool kids dance pop, cheerful sweet female vocal, clear diction, funky bass, ukulele, handclaps, fun silly energy, major key, catchy repetitive chant chorus, " + NOINTRO,
  bpm=124, key="F Major", duration=150, seed=22,
  lyrics="""[Chorus]
Peel banana, peel, peel, peel!
Wiggle banana, wiggle like an eel!
Go bananas, jump up high,
Banana dance, wave hi, hi, hi!

[Verse 1]
Bananas are yellow, long and bright,
Peel it down and take a bite!
Bananas grow in a bunch, you see,
High up on a banana tree!

[Chorus]
Peel banana, peel, peel, peel!
Wiggle banana, wiggle like an eel!
Go bananas, jump up high,
Banana dance, wave hi, hi, hi!

[Verse 2]
Apple, apple, crunch and spin!
Orange, orange, roll right in!
Grape, grape, bounce so small,
Fruity friends dance, one and all!

[Bridge]
Peel to the left, peel, peel!
Peel to the right, peel, peel!
Shake your arms and shake your feet,
Wiggle, wiggle to the beat!

[Verse 3]
Fruit gives energy to play,
Have some fruit every day!
Pipkiko says, one more time,
Dance with me and feel so fine!

[Chorus]
Peel banana, peel, peel, peel!
Wiggle banana, wiggle like an eel!
Go bananas, jump up high,
Banana dance, wave hi, hi, hi!

[Outro]
Go bananas! See you tomorrow!""",
  direct=[{"section": "chorus1", "shots": ["wide", "close:banana", "close:host", "low"], "energy": 1.0, "group": True, "wave": 1, "jump": 0.4,
           "props": [T("BANANA DANCE!", "#ffc107", size=0.6), P("banana_hand", "peel", at="right")]},
          {"section": "verse1", "shots": ["close:banana", "wide", "close:host", "close:banana"], "energy": 0.8,
           "props": [P("bigfruit", "bananas", at=[-2.6, 0.9, 3.4], opts={"kind": "banana"}), P("tree", "tree", at="left")]},
          {"section": "chorus2", "shots": ["orbit", "close:host", "wide", "low"], "energy": 1.0, "group": True, "wave": 1, "jump": 0.4,
           "props": [T("BANANA DANCE!", "#ffc107", size=0.6), P("banana_hand", "peel", at="right")]},
          {"section": "verse2", "shots": ["close:apple", "close:orange", "close:grape", "wide"], "energy": 0.9, "group": True,
           "props": [P("bigfruit", "apple", at=[-2.6, 0.9, 3.4], opts={"kind": "apple"}), P("bigfruit", "orange", at=[0, 1.2, 3.6], opts={"kind": "orange"}),
                     P("bigfruit", "grape", at=[2.6, 0.9, 3.4], opts={"kind": "grape"})]},
          {"section": "bridge1", "shots": ["wide", "low", "orbit", "wide"], "energy": 1.0, "group": True, "wave": 1, "jump": 0.5,
           "props": [T("PEEL!", "#ffc107", "peel", at=[-3.4, 0.3, 3.5], size=0.7), T("SHAKE!", "#ff5c8a", "shake", at=[3.4, 0.3, 3.5], size=0.7),
                     T("WIGGLE!", "#3cc45a", "wiggle", at=[0, 0.6, 4.3], size=0.7)]},
          {"section": "verse3", "shots": ["close:host", "wide", "close:host", "low"], "energy": 0.85,
           "props": [P("heart", "fruit", at="left"), P("basket", "day", at="right")]},
          {"section": "chorus3", "shots": ["low", "close:host", "orbit", "wide"], "energy": 1.0, "group": True, "wave": 1, "jump": 0.5,
           "props": [T("BANANA DANCE!", "#ffc107", size=0.6), P("banana_hand", "peel", at="right")]},
          {"section": "outro1", "shots": ["wide"], "energy": 0.7, "group": True, "wave": 1, "props": [T("SEE YOU TOMORROW!", "#ff5c8a", size=0.5)]}],
  meta={"title": "Banana Dance Song for Kids! Peel and Wiggle with Pipkiko", "card": "Banana Dance!", "thumb_text": "BANANA DANCE!",
        "description": "The Banana Dance Song for kids! Peel, wiggle and go bananas with Pipkiko and the Fruity Friends.\nA silly fruit dance song: kids learn that bananas grow in bunches on banana trees, meet apple, orange and grape, and dance along. Ages 2-6.",
        "tags": ["banana dance", "banana song", "dance song for kids", "fruit song", "action songs for kids", "kids songs", "nursery rhymes", "Fruity Friends", "3D kids songs"]}))

# ---- Zoo: What do animals eat?
zc = J("zoo3d_ep01_v3"); zd = {d["section"]: d for d in zc["direct"]}
def zsec(name, src, word_props):
    d = copy.deepcopy(zd[src]); d["section"] = name
    d["props"] = [p for p in d["props"] if p.get("name") in ("sign", "num")] + word_props; return d
specs.append(dict(id="zoo3d_ep02", job="zoo3d_ep02", channel="zoo", set="savanna", cast=zc["cast"],
  who_map={"lion1": "lion", "elephant1": "elephant", "giraffe1": "giraffe", "zebra1": "zebra", "hippo1": "hippo", "bridge1": "all"},
  style="upbeat preschool kids pop sing-along, cheerful friendly male vocal, clear diction, african percussion, marimba, ukulele, handclaps, bouncy bass, major key, catchy repetitive chorus, " + NOINTRO,
  bpm=116, key="A Major", duration=170, seed=4,
  lyrics="""[Chorus]
What do animals eat? Let's see!
Munch, munch, crunch, crunch, yummy!
Big and small, they eat it all,
What do animals eat? Let's see!

[Lion]
Lions eat meat, it makes them strong,
They nap in the sun all day long!
Roar, roar, I'm the king,
Hear the lion family sing!

[Elephant]
Elephants munch on grass and leaves,
Bark and fruit from tall green trees!
My trunk picks up my lunch, you see,
Toot, toot, it's yummy for me!

[Chorus]
What do animals eat? Let's see!
Munch, munch, crunch, crunch, yummy!
Big and small, they eat it all,
What do animals eat? Let's see!

[Giraffe]
Giraffes eat leaves up high, high, high,
Acacia leaves up in the sky!
My long tongue grabs them, one, two, three,
Stretch up tall and munch with me!

[Zebra]
Zebras graze on grass all day,
Munch, munch, munch, then run and play!
Hippos come out when it's night,
To eat green grass by the moonlight!

[Bridge]
Munch like a zebra, munch, munch, munch!
Stretch like a giraffe for lunch!
Stomp like an elephant, stomp, stomp, stomp!
Roar like a lion, chomp, chomp, chomp!

[Chorus]
What do animals eat? Let's see!
Munch, munch, crunch, crunch, yummy!
Big and small, they eat it all,
What do animals eat? Let's see!

[Outro]
Yummy, yummy! Bye-bye, friends!""",
  direct=[{**copy.deepcopy(zd["chorus1"]), "props": [T("YUMMY!", "#ffb627", size=0.9)]},
          zsec("lion1", "lion1", [P("sun", "sun", at=[3.4, 1.2, 3.0])]),
          zsec("elephant1", "elephant1", [P("leaves", "leaves", at=[3.4, 0.4, 3.0])]),
          {**copy.deepcopy(zd["chorus2"]), "props": [T("YUMMY!", "#ffb627", size=0.9)]},
          zsec("giraffe1", "giraffe1", [P("leaves", "leaves", at=[3.2, 1.0, 3.0])]),
          {**zsec("zebra1", "zebra1", [T("NIGHT", "#6e5aa8", "night", at=[3.6, 0.3, 2.6], size=0.5)]), "shots": ["close:zebra", "wide", "close:hippo", "wide"]},
          {**copy.deepcopy(zd["bridge1"]), "props": [T("MUNCH!", "#2fb59a", "munch", at=[-3.4, 0.3, 3.5], size=0.7), T("STRETCH!", "#ffb627", "stretch", at=[3.4, 0.3, 3.5], size=0.7),
                                                     T("STOMP!", "#ff7a00", "stomp", at=[-1.3, 0.6, 4.3], size=0.7), T("ROAR!", "#e8302a", "roar", at=[1.3, 0.6, 4.3], size=0.7)]},
          {**copy.deepcopy(zd["chorus3"]), "props": [T("YUMMY!", "#ffb627", size=0.9)]},
          copy.deepcopy(zd["outro1"])],
  meta={"title": "What Do Animals Eat? Safari Song for Kids with Milo", "card": "What Do Animals Eat?", "thumb_text": "WHAT DO THEY EAT?",
        "description": "What do animals eat? Sing along with Milo on the savanna and find out what lions, elephants, giraffes, zebras and hippos eat.\nReal animal facts for kids: giraffes eat acacia leaves up high and hippos graze on grass at night. Munch, stretch, stomp and roar along! Ages 2-6.",
        "tags": ["what do animals eat", "animal song for kids", "safari animals", "zoo animals for kids", "animal facts for kids", "kids songs", "nursery rhymes", "The Animated Zoo", "Milo"]}))

# ---- Moon: Count the Stars lullaby
mc = J("mb3d_ep01_v3"); md = {d["section"]: d for d in mc["direct"]}
star = lambda w, n, x: P("numstar", w, at=[x, 2.4, 3.2], opts={"n": n})
specs.append(dict(id="mb3d_ep02", job="mb3d_ep02", channel="moon", set="nightroom", cast=mc["cast"],
  style="gentle bedtime lullaby for toddlers, soft warm female vocal, slow and calm, music box, soft piano, harp, light strings, dreamy, sleepy, clear gentle diction, " + NOINTRO,
  bpm=72, key="D Major", duration=170, seed=6,
  lyrics="""[Chorus]
Count the stars and close your eyes,
One by one across the skies,
Twinkle softly, shining bright,
Count the stars and say goodnight.

[Verse 1]
One little star says hello,
Two little stars in a sleepy glow,
Three little stars, yawn so wide,
Snuggle up, warm inside.

[Chorus]
Count the stars and close your eyes,
One by one across the skies,
Twinkle softly, shining bright,
Count the stars and say goodnight.

[Verse 2]
Four little stars, sparkle and blink,
Five little stars, softly I think,
Moon is smiling, round and wide,
Owls and bunnies sleep inside.

[Bridge]
Breathe in slow, and breathe out slow,
Rest your arms and wiggle your toes,
Stars are suns so far away,
They'll shine again another day.

[Verse 3]
Teddy's sleepy, lamb is too,
Bunny's dreaming, so are you,
Hush now, hush now, close your eyes,
Stars will twinkle in the skies.

[Chorus]
Count the stars and close your eyes,
One by one across the skies,
Twinkle softly, shining bright,
Count the stars and say goodnight.

[Outro]
Goodnight, little stars. Goodnight.""",
  direct=[{**copy.deepcopy(md["chorus1"]), "props": [T("Count the Stars", "#ffd88a", size=0.7), P("moon", None, at="top", delay=2)]},
          {**copy.deepcopy(md["verse1"]), "props": [star("one", 1, -3.0), star("two", 2, -1.5), star("three", 3, 0.0)]},
          {**copy.deepcopy(md["chorus2"]), "props": [T("Count the Stars", "#ffd88a", size=0.7)]},
          {**copy.deepcopy(md["verse2"]), "props": [star("one", 1, -3.0), star("two", 2, -1.5), star("three", 3, 0.0), star("four", 4, 1.5), star("five", 5, 3.0)]},
          {**copy.deepcopy(md["bridge1"]), "props": [T("Breathe...", "#bfa8ff", "breathe", size=0.6), P("zzz", "rest", at="right")]},
          {**copy.deepcopy(md["verse3"]), "props": [P("zzz", "dreaming", at="left"), P("heart", "hush", at="right")]},
          {**copy.deepcopy(md["chorus3"]), "props": [T("Goodnight", "#ffd88a", size=0.7)]},
          copy.deepcopy(md["outro1"])],
  meta={"title": "Count the Stars Lullaby for Babies and Kids | Moonbeam", "card": "Count the Stars", "thumb_text": "COUNT THE STARS",
        "description": "Count the Stars, a gentle lullaby for babies and kids. Count from 1 to 5 with Luna the sleepy owl as the stars twinkle and the moon smiles.\nSoft music box and piano, slow breathing, and a calm goodnight to help little ones fall asleep. Ages 0-6.",
        "tags": ["lullaby for babies", "count the stars", "bedtime song", "sleep music for kids", "goodnight song", "lullabies", "baby sleep", "Moonbeam Bedtime", "3D kids songs"]}))

out = "/root/zoo/specs/b2"
for s in specs:
    job = {"id": s["job"], "title": s["meta"]["card"], "channel": s["channel"], "set": s["set"], "seed": 7, "cast": s["cast"],
           "intro_shot": "orbit", "intro": {"energy": 0.6, "wave": 1}, "thumb_frame": 96, "direct": s["direct"], "song": s["id"],
           "res": "1920x1080", "step": 1}
    spec = {"style": s["style"], "lyrics": s["lyrics"], "duration": s["duration"], "bpm": s["bpm"], "key": s["key"], "seed": s["seed"],
            "who_map": s.get("who_map", {}), "meta": s["meta"], "job": job}
    if s.get("color_words"): spec["color_words"] = s["color_words"]; spec["color_char"] = s["color_char"]
    assert len(s["meta"]["title"]) <= 60, s["meta"]["title"]
    json.dump(spec, open(f"{out}/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]))
