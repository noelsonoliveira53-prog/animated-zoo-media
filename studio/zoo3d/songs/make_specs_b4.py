import json, copy, re, sys
sys.path.insert(0, "/root/zoo/blender/zoo3d"); import timing_lib as TL
Z = "/root/zoo/blender/zoo3d"
B3 = lambda n: json.load(open(f"/root/zoo/specs/b3/{n}.song.json"))
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
L = lambda x: [-3.4, 0.3, 3.5] if x == "l" else [3.4, 0.3, 3.5] if x == "r" else [0, 0.6, 4.3]
specs = []

specs.append(dict(id="bl3d_ep04", base="bl3d_ep03", colors={"red": "#ff3b3b", "yellow": "#ffd21f", "orange": "#ff8a1f", "blue": "#3d8bff", "green": "#3ccf4e", "purple": "#9d6bff"},
  lyrics="""[Chorus]
Mix, mix, mix the colors!
Swirl them round and see!
Two colors make a new one,
Mix the colors with me!

[Verse 1]
Red and yellow, swirl, swirl, swirl,
What do we get? Orange, hooray!
Orange like a pumpkin, orange like the sun,
Mixing colors is so much fun!

[Chorus]
Mix, mix, mix the colors!
Swirl them round and see!
Two colors make a new one,
Mix the colors with me!

[Verse 2]
Blue and yellow, swirl, swirl, swirl,
What do we get? Green, hooray!
Green like a froggy, green like a tree,
Green, green, green for me!

[Bridge]
Stir, stir, stir the paint!
Shake, shake, shake it up!
Splash, splash, splash, hooray!
Colors everywhere today!

[Verse 3]
Red and blue, swirl, swirl, swirl,
What do we get? Purple, hooray!
Purple like grapes, purple like a plum,
Bloop is purple, yum, yum, yum!

[Chorus]
Mix, mix, mix the colors!
Swirl them round and see!
Two colors make a new one,
Mix the colors with me!

[Outro]
Orange, green and purple! Bye-bye!""",
  props={"chorus1": [T("MIX COLORS!", "#ff5c8a", size=0.8)], "verse1": [T("RED", "#ff3b3b", "red", at=[-4.4, 0.6, 3.8]), T("YELLOW", "#ffd21f", "yellow", at=[4.4, 0.6, 3.8]), T("= ORANGE!", "#ff8a1f", "orange", size=0.8)],
         "chorus2": [T("MIX COLORS!", "#ff5c8a", size=0.8)], "verse2": [T("BLUE", "#3d8bff", "blue", at=[-4.4, 0.6, 3.8]), T("YELLOW", "#ffd21f", "yellow", at=[4.4, 0.6, 3.8]), T("= GREEN!", "#3ccf4e", "green", size=0.8)],
         "bridge1": [T("STIR!", "#ff5c8a", "stir", at=L("l"), size=0.7), T("SHAKE!", "#ffd21f", "shake", at=L("r"), size=0.7), T("SPLASH!", "#3d8bff", "splash", at=L("c"), size=0.7)],
         "verse3": [T("RED", "#ff3b3b", "red", at=[-4.4, 0.6, 3.8]), T("BLUE", "#3d8bff", "blue", at=[4.4, 0.6, 3.8]), T("= PURPLE!", "#9d6bff", "purple", size=0.8)],
         "chorus3": [T("MIX COLORS!", "#ff5c8a", size=0.8)], "outro1": [T("BYE-BYE!", "#ff5c8a")]},
  meta={"title": "Red + Yellow = Orange?! Bloop Mixes Colors | Kids Song", "card": "Mixing Colors!", "thumb_text": "RED + YELLOW = ?",
        "description": "Red + yellow = orange?! Bloop the jelly blob mixes colors and changes color every time. A color mixing song for kids.\nKids learn the secondary colors: red + yellow = orange, blue + yellow = green, red + blue = purple, then stir, shake and splash along. Ages 2-6.",
        "tags": ["color mixing song", "mixing colors for kids", "learn colors", "primary colors", "red yellow orange", "kids songs", "Bloop's Color Lab", "3D kids songs"]}))

specs.append(dict(id="tt3d_ep04", base="tt3d_ep03",
  lyrics="""[Chorus]
Help! Help! The dump truck is stuck!
Stuck in the mud, oh, what bad luck!
Push and pull and heave, heave, ho,
Friends help friends, so here we go!

[Verse 1]
Dump truck drove into the mud,
Wheels went spin with a squishy thud!
Vroom, vroom, he cannot move,
Who can help him get unglued?

[Chorus]
Help! Help! The dump truck is stuck!
Stuck in the mud, oh, what bad luck!
Push and pull and heave, heave, ho,
Friends help friends, so here we go!

[Verse 2]
Here comes the tow truck with a hook,
Hook it on, now take a look!
Here comes Bolt to push, push, push,
One, two, three, and whoosh, whoosh, whoosh!

[Bridge]
Pull the rope, pull, pull, pull!
Push the truck, push, push, push!
Heave, heave, ho, and one more time,
Out of the mud, we're doing fine!

[Verse 3]
Pop! The dump truck rolls out free,
Thank you, friends, from you and me!
When a friend is stuck, we help,
Together we can do it well!

[Chorus]
Help! Help! The dump truck is stuck!
Stuck in the mud, oh, what bad luck!
Push and pull and heave, heave, ho,
Friends help friends, so here we go!

[Outro]
Heave, heave, ho! Bye-bye, friends!""",
  props={"chorus1": [T("HELP!", "#e8302a", size=1.0)], "verse1": [T("STUCK!", "#8a5a2b", "mud", size=0.9)], "chorus2": [T("HELP!", "#e8302a", size=1.0)],
         "verse2": [T("TOW TRUCK!", "#ffc107", "tow", at=[-2.8, 1.6, 3.6], size=0.6), T("PUSH!", "#e8302a", "push", at=[2.8, 1.6, 3.6], size=0.7)],
         "bridge1": [T("PULL!", "#3b8be0", "pull", at=L("l"), size=0.7), T("PUSH!", "#e8302a", "push", at=L("r"), size=0.7), T("HEAVE HO!", "#2fb54a", "heave", at=L("c"), size=0.6)],
         "verse3": [T("POP!", "#ff5c8a", "pop", size=1.0), T("THANK YOU!", "#ff5c8a", "thank", at=[0, 1.8, 3.6], size=0.6)],
         "chorus3": [T("HELP!", "#e8302a", size=1.0)], "outro1": [T("BYE-BYE!", "#e8302a")]},
  meta={"title": "Help! The Dump Truck Is Stuck! Kids Song | Tiny Truck Town", "card": "The Dump Truck Is Stuck!", "thumb_text": "HELP! TRUCK STUCK!",
        "description": "Help! The dump truck is stuck in the mud! Bolt the fire truck and the tow truck come to the rescue in Tiny Truck Town.\nA song about teamwork and helping friends: pull the rope, push the truck, heave, heave, ho! Ages 2-6.",
        "tags": ["dump truck song", "truck stuck in mud", "tow truck song", "trucks for kids", "teamwork song", "kids songs", "nursery rhymes", "Tiny Truck Town", "3D kids songs"]}))

specs.append(dict(id="fr3d_ep05", base="fr3d_ep04",
  lyrics="""[Chorus]
Yes, yes, fruit salad, yes, yes, yum!
Chop, chop, mix, mix, here they come!
Apples, bananas, grapes so sweet,
Yes, yes, fruit salad, time to eat!

[Verse 1]
Wash your hands, scrub, scrub, scrub,
Now we're ready, rub-a-dub!
Banana, peel it, slice it thin,
Yes, yes, toss it in!

[Chorus]
Yes, yes, fruit salad, yes, yes, yum!
Chop, chop, mix, mix, here they come!
Apples, bananas, grapes so sweet,
Yes, yes, fruit salad, time to eat!

[Verse 2]
Strawberries, red, in they go,
Orange slices, in a row!
Purple grapes, one, two, three,
Yes, yes, fruit for me!

[Bridge]
Stir it round, round, round!
Stir it up and down!
Shake your hips and shake your hands,
Fruit salad dance, the best in the land!

[Verse 3]
Fruits have vitamins to help you grow,
Strong and happy, head to toe!
Share a bowl with all your friends,
Yes, yes, the yummy end!

[Chorus]
Yes, yes, fruit salad, yes, yes, yum!
Chop, chop, mix, mix, here they come!
Apples, bananas, grapes so sweet,
Yes, yes, fruit salad, time to eat!

[Outro]
Yes, yes, fruit salad! See you tomorrow!""",
  props={"chorus1": [T("YES YES FRUIT SALAD!", "#ff5c8a", size=0.5), P("basket", None, at="right", delay=1)], "verse1": [T("WASH HANDS!", "#3b8be0", "wash", size=0.6), P("bigfruit", "banana", at=[2.6, 0.9, 3.4], opts={"kind": "banana"})],
         "chorus2": [T("YES YES FRUIT SALAD!", "#ff5c8a", size=0.5)], "verse2": [P("bigfruit", "strawberries", at=[-2.6, 0.9, 3.4], opts={"kind": "strawberry"}), P("bigfruit", "orange", at=[0, 1.2, 3.6], opts={"kind": "orange"}), P("bigfruit", "grapes", at=[2.6, 0.9, 3.4], opts={"kind": "grape"})],
         "bridge1": [T("STIR!", "#ff5c8a", "stir", at=L("l"), size=0.7), T("SHAKE!", "#ffc107", "shake", at=L("r"), size=0.7), T("DANCE!", "#3cc45a", "dance", at=L("c"), size=0.7)],
         "verse3": [P("heart", "grow", at="left"), T("SHARE!", "#ff5c8a", "share", size=0.8)], "chorus3": [T("YES YES FRUIT SALAD!", "#ff5c8a", size=0.5)], "outro1": [T("SEE YOU TOMORROW!", "#ff5c8a", size=0.5)]},
  meta={"title": "Yes Yes Fruit Salad Song for Kids! | Fruity Friends", "card": "Yes Yes Fruit Salad!", "thumb_text": "YES YES FRUIT SALAD!",
        "description": "Yes, yes, fruit salad! Make a yummy fruit salad with Pipkiko and the Fruity Friends: wash your hands, peel the banana, add strawberries, oranges and grapes.\nA healthy eating song for kids: fruits have vitamins that help you grow. Stir, shake and dance along! Ages 2-5.",
        "tags": ["yes yes fruit salad", "fruit salad song", "healthy eating song", "fruit song for kids", "yes yes song", "kids songs", "nursery rhymes", "Fruity Friends", "3D kids songs"]}))

specs.append(dict(id="zoo3d_ep04", base="zoo3d_ep03",
  lyrics="""[Chorus]
Where is my mama? Where can she be?
Milo will help you, come with me!
Look high, look low, look all around,
Where is my mama? Mama is found!

[Lion]
Little lion cub says roar,
Where's my mama? I want more!
There she is, the lioness,
Big warm hug, she loves me best!

[Elephant]
Little elephant, toot, toot, toot,
Where's my mama? Look, there's her foot!
Mama's trunk gives a gentle hug,
Snuggle close, so warm and snug!

[Chorus]
Where is my mama? Where can she be?
Milo will help you, come with me!
Look high, look low, look all around,
Where is my mama? Mama is found!

[Giraffe]
Little giraffe, so new and small,
Where's my mama, very tall?
Look up high, there's mama's face,
Baby giraffes can stand up in an hour, what a race!

[Zebra]
Little zebra knows her mama's stripes,
Every pattern is just right!
Little hippo swims to mama, splash,
Baby hippos stay close, dash, dash!

[Bridge]
Look high, look low, look left, look right!
Clap your hands, hug someone tight!
Mamas and babies, two by two,
Mama loves me, I love you!

[Chorus]
Where is my mama? Where can she be?
Milo will help you, come with me!
Look high, look low, look all around,
Where is my mama? Mama is found!

[Outro]
Mama is found! Bye-bye, friends!""",
  props={"chorus1": [T("WHERE IS MY MAMA?", "#ffb627", size=0.55)], "lion1": [P("heart", "hug", at=[-3.6, 0.6, 2.6])], "elephant1": [P("heart", "hug", at=[3.4, 0.6, 3.0])],
         "chorus2": [T("WHERE IS MY MAMA?", "#ffb627", size=0.55)], "giraffe1": [T("LOOK UP!", "#b8692c", "up", at=[3.2, 1.0, 3.0], size=0.5)],
         "zebra1": [T("STRIPES!", "#25232b", "stripes", at=[3.6, 0.3, 2.6], size=0.5), T("SPLASH!", "#3db8ff", "splash", at=[-3.6, 0.3, 2.6], size=0.5)],
         "bridge1": [T("LOOK!", "#ffb627", "look", at=L("l"), size=0.7), T("CLAP!", "#ff5c8a", "clap", at=L("r"), size=0.7), T("HUG!", "#e8302a", "hug", at=L("c"), size=0.7)],
         "chorus3": [T("MAMA IS FOUND!", "#ffb627", size=0.55)], "outro1": [T("BYE-BYE!", "#ffb627")]},
  meta={"title": "Where Is My Mama? Baby Animals Song for Kids with Milo", "card": "Where Is My Mama?", "thumb_text": "WHERE IS MY MAMA?",
        "description": "Where is my mama? Milo helps baby animals on the savanna find their mamas: a lion cub, a baby elephant, a baby giraffe, a zebra foal and a baby hippo.\nReal facts for kids: baby giraffes can stand up within about an hour of being born, zebra foals learn their mama's stripe pattern, and baby hippos stay close to mama in the water. Ages 2-6.",
        "tags": ["where is my mama", "baby animals song", "mama and baby animals", "safari animals", "animal song for kids", "kids songs", "nursery rhymes", "The Animated Zoo", "Milo"]}))

specs.append(dict(id="mb3d_ep04", base="mb3d_ep03",
  lyrics="""[Chorus]
Hush, little bunny, close your eyes,
Moon is rising in the skies,
Soft and cozy, safe and warm,
Hush, little bunny, sleep till morn.

[Verse 1]
Little bunny hops to bed,
Fluffy pillow for her head,
Ears fold down and paws tuck in,
Sleepy dreams are soon to begin.

[Chorus]
Hush, little bunny, close your eyes,
Moon is rising in the skies,
Soft and cozy, safe and warm,
Hush, little bunny, sleep till morn.

[Verse 2]
Owl says hoo from the tall oak tree,
Teddy yawns so sleepily,
Little lamb curls up in a ball,
Goodnight, goodnight, to one and all.

[Bridge]
Breathe in slow, like a gentle breeze,
Breathe out slow, through the sleepy trees,
Wiggle your toes and let them rest,
Snuggle in, you're loved the best.

[Verse 3]
Stars are blinking, one, two, three,
Night light glowing, soft for me,
Mama sings a lullaby,
Hush now, hush now, close your eyes.

[Chorus]
Hush, little bunny, close your eyes,
Moon is rising in the skies,
Soft and cozy, safe and warm,
Hush, little bunny, sleep till morn.

[Outro]
Hush, little bunny. Goodnight.""",
  props={"chorus1": [T("Hush, Little Bunny", "#ffd88a", size=0.6), P("moon", None, at="top", delay=2)], "verse1": [P("zzz", "dreams", at="right")],
         "chorus2": [T("Hush, Little Bunny", "#ffd88a", size=0.6)], "verse2": [P("zzz", "yawns", at="left")],
         "bridge1": [T("Breathe...", "#bfa8ff", "breathe", size=0.6), P("heart", "loved", at="right")], "verse3": [P("numstar", "one", at=[-3.0, 2.4, 3.2], opts={"n": 1}), P("numstar", "two", at=[0, 2.4, 3.2], opts={"n": 2}), P("numstar", "three", at=[3.0, 2.4, 3.2], opts={"n": 3})],
         "chorus3": [T("Goodnight", "#ffd88a", size=0.7)], "outro1": [P("zzz", None, at="right")]},
  meta={"title": "Hush Little Bunny 🌙 Lullaby for Babies & Kids | Moonbeam", "card": "Hush, Little Bunny", "thumb_text": "HUSH LITTLE BUNNY",
        "description": "Hush, Little Bunny, a soft bedtime lullaby for babies and kids. Little bunny hops to bed while the owl hoots, Teddy yawns and the stars blink.\nGentle music box and piano with slow breathing to help little ones relax and fall asleep. Ages 0-6.",
        "tags": ["lullaby for babies", "hush little bunny", "bedtime song", "sleep music for kids", "baby sleep", "goodnight song", "lullabies", "Moonbeam Bedtime", "3D kids songs"]}))

specs.append(dict(id="gz3d_ep04", base="gz3d_ep03",
  lyrics="""[Chorus]
Why is the sky blue? Do you know?
Sunlight hides a rainbow glow!
Blue light bounces all around,
That's why the sky is blue, wow, wow!

[Verse 1]
Sunlight looks white, but guess what's true,
It's red and orange, yellow, green and blue!
All the colors hide inside,
Sunlight takes them for a ride!

[Verse 2]
When sunlight zooms into the air,
Blue light bounces everywhere!
Bounce, bounce, bounce across the sky,
Blue, blue, blue way up high!

[Chorus]
Why is the sky blue? Do you know?
Sunlight hides a rainbow glow!
Blue light bounces all around,
That's why the sky is blue, wow, wow!

[Verse 3]
At sunset, light goes a long, long way,
Red and orange come out to play!
Pink and orange in the evening sky,
Then the stars say, goodnight, bye-bye!

[Bridge]
Bounce like blue light, bounce, bounce, bounce!
Zoom like sunlight, zoom, zoom, zoom!
Stretch up high and touch the sky!
Wave to the sun, bye-bye!

[Chorus]
Why is the sky blue? Do you know?
Sunlight hides a rainbow glow!
Blue light bounces all around,
That's why the sky is blue, wow, wow!

[Outro]
Why is the sky blue? Now you know! Bye-bye!""",
  props={"chorus1": [T("WHY IS THE SKY BLUE?", "#3b8be0", size=0.5), P("sun", None, at=[-3.2, 1.2, 3.6], opts={"size": 0.7}, delay=1)],
         "verse1": [P("sun", "sunlight", at=[0, 1.2, 3.4], opts={"size": 0.9}), T("RAINBOW!", "#ff5c8a", "rainbow", size=0.7)],
         "verse2": [T("BOUNCE!", "#3b8be0", "bounce", size=0.8), T("BLUE!", "#3b8be0", "blue", at=[3.2, 1.6, 3.6], size=0.7)],
         "chorus2": [T("WHY IS THE SKY BLUE?", "#3b8be0", size=0.5)], "verse3": [T("SUNSET!", "#ff8a1f", "sunset", size=0.8), P("star", "stars", at=[2.6, 1.6, 3.6], opts={"size": 0.5})],
         "bridge1": [T("BOUNCE!", "#3b8be0", "bounce", at=L("l"), size=0.7), T("ZOOM!", "#ffb627", "zoom", at=L("r"), size=0.7), T("STRETCH!", "#2fb59a", "stretch", at=L("c"), size=0.7)],
         "chorus3": [T("WHY IS THE SKY BLUE?", "#3b8be0", size=0.5)], "outro1": [T("BYE-BYE!", "#3b8be0")]},
  meta={"title": "Why Is the Sky Blue? Science Song for Kids with Gizmo", "card": "Why Is the Sky Blue?", "thumb_text": "WHY IS THE SKY BLUE?",
        "description": "Why is the sky blue? Gizmo the robot explains it with a song: sunlight is made of all the rainbow colors, and blue light bounces around the sky the most.\nKids also learn why sunsets look red and orange. Bounce like blue light and zoom like sunlight! Ages 3-6.",
        "tags": ["why is the sky blue", "science for kids", "science song", "sky facts for kids", "preschool science", "kids songs", "Gizmo Explains", "3D kids songs"]}))

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
    json.dump(spec, open(f"/root/zoo/specs/b4/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]), secs)
