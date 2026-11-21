import json, copy, re, sys
sys.path.insert(0, "/root/zoo/blender/zoo3d"); import timing_lib as TL
Z = "/root/zoo/blender/zoo3d"
B3 = lambda n: json.load(open(f"/root/zoo/specs/b5/{n}.song.json"))
T = lambda text, color, word=None, at="top", size=0.8, **k: dict({"type": "text", "text": text, "color": color, "at": at, "size": size}, **({"word": word} if word else {}), **k)
P = lambda name, word=None, at="left", **k: dict({"type": "set_prop", "name": name, "at": at}, **({"word": word} if word else {}), **k)
L = lambda x: [-3.4, 0.3, 3.5] if x == "l" else [3.4, 0.3, 3.5] if x == "r" else [0, 0.6, 4.3]
specs = []

specs.append(dict(id="bl3d_ep09", base="bl3d_ep05",
  lyrics="""[Chorus]
Big or small, big or small,
Bloop can grow up really tall!
Then he shrinks down tiny, see?
Big and small, sing with me!

[Verse 1]
A big, big elephant, stomp, stomp, stomp,
A tiny mouse goes romp, romp, romp!
A big balloon, a little ball,
Which is big and which is small?

[Chorus]
Big or small, big or small,
Bloop can grow up really tall!
Then he shrinks down tiny, see?
Big and small, sing with me!

[Verse 2]
A tall, tall tree reaching for the sky,
A short little flower, waving hi!
A long, long snake goes wiggle, wiggle,
A short little worm makes Bloop giggle!

[Bridge]
Make yourself big, stretch your arms wide!
Make yourself small, curl up inside!
Stand up tall, then crouch down low,
Big and small, here we go!

[Verse 3]
Big blocks stacking up so high,
Little blocks, give them a try!
Big or little, short or tall,
Bloop loves every size of all!

[Chorus]
Big or small, big or small,
Bloop can grow up really tall!
Then he shrinks down tiny, see?
Big and small, sing with me!

[Outro]
Big and small! Bye-bye, friends!""",
  props={"chorus1": [T("BIG!", "#ff4b9b", "tall!", at=L("l"), size=1.0), T("small", "#3b8be0", "tiny,", at=L("r"), size=0.4)],
         "verse1": [P("balloon", "balloon,", at=[-3.4, 1.4, 3.6], opts={"color": "#ff4b9b"}), T("BIG or small?", "#ff8a1f", "Which", size=0.6)],
         "chorus2": [T("BIG!", "#ff4b9b", "tall!", at=L("l"), size=1.0), T("small", "#3b8be0", "tiny,", at=L("r"), size=0.4)],
         "verse2": [P("flower", "flower,", at=[3.4, 0.9, 3.6], opts={"color": "#ffd21f"}), T("LONG!", "#3cc45a", "long,", at=[-3.4, 1.4, 3.6], size=0.7)],
         "bridge1": [T("BIG!", "#ff4b9b", "big,", at=L("l"), size=1.0), T("small", "#3b8be0", "small,", at=L("r"), size=0.4), T("TALL!", "#ff8a1f", "tall,", at=L("c"), size=0.7)],
         "verse3": [P("block", "blocks", at=[-3.4, 0.9, 3.6], opts={"n": 3, "color": "#ff4b9b"}), P("block", "Little", at=[3.4, 0.6, 3.6], opts={"n": 1, "color": "#3b8be0"})],
         "chorus3": [T("BIG & SMALL!", "#ff4b9b", size=0.7)], "outro1": [T("BYE-BYE!", "#ff4b9b")]},
  meta={"title": "Big or Small? Bloop Grows and Shrinks! Opposites Song", "card": "Big or Small?", "thumb_text": "BIG OR SMALL?",
        "description": "Bloop the jelly blob grows big and shrinks small! A big elephant and a tiny mouse, a tall tree and a short flower, a long snake and a short worm.\nKids stretch big, curl up small, stand tall and crouch low while learning big, small, tall, short, long and little. Ages 2-5.",
        "tags": ["big and small song", "opposites song for kids", "sizes for toddlers", "tall and short", "kids songs", "Bloop's Color Lab", "3D kids songs"]}))

specs.append(dict(id="tt3d_ep09", base="tt3d_ep05",
  lyrics="""[Chorus]
Police car, police car, wee-oo, wee-oo!
Officer Blue is here for you!
Lights go flash and siren sings,
Keeping us safe is a helpful thing!

[Verse 1]
Red light, blue light, flashing bright,
Police car zooming day and night!
When you're lost and need a hand,
Find a helper, they understand!

[Chorus]
Police car, police car, wee-oo, wee-oo!
Officer Blue is here for you!
Lights go flash and siren sings,
Keeping us safe is a helpful thing!

[Verse 2]
Stop at the corner, look both ways,
Hold a grown-up's hand, that's what Blue says!
Cross with the green light, walk, don't run,
Safety rules can be lots of fun!

[Bridge]
Look to the left, look to the right!
Look to the left, all clear? Alright!
Hold a hand and walk across,
Officer Blue gives a big thumbs-up!

[Verse 3]
Fire trucks, ambulances, police cars too,
Community helpers, they help you!
Wave hello when they drive by,
Thank you, helpers, wave up high!

[Chorus]
Police car, police car, wee-oo, wee-oo!
Officer Blue is here for you!
Lights go flash and siren sings,
Keeping us safe is a helpful thing!

[Outro]
Wee-oo, wee-oo! Bye-bye, trucks!""",
  props={"chorus1": [T("WEE-OO!", "#3b8be0", size=0.8), P("siren", None, at=[-3.0, 1.4, 3.6], delay=1)],
         "verse1": [P("siren", "light,", at=[-3.0, 1.4, 3.6]), T("FIND A HELPER!", "#3b8be0", "helper,", size=0.55)],
         "chorus2": [T("WEE-OO!", "#3b8be0", size=0.8)], "verse2": [T("LOOK BOTH WAYS!", "#ffc107", "look", size=0.55), T("WALK!", "#2fb54a", "walk,", at=L("c"), size=0.7)],
         "bridge1": [T("LEFT!", "#3b8be0", "left,", at=L("l"), size=0.7), T("RIGHT!", "#e8302a", "right!", at=L("r"), size=0.7), T("THUMBS UP!", "#ffc107", "thumbs-up!", at=L("c"), size=0.6)],
         "verse3": [T("THANK YOU!", "#e8302a", "Thank", size=0.7), P("helmet", "helpers,", at=[3.0, 1.0, 3.6])],
         "chorus3": [T("WEE-OO!", "#3b8be0", size=0.8)], "outro1": [T("BYE-BYE!", "#3b8be0")]},
  meta={"title": "Police Car Song! Road Safety for Kids | Tiny Truck Town", "card": "Police Car Song!", "thumb_text": "WEE-OO!",
        "description": "Wee-oo, wee-oo! Officer Blue the police car keeps Tiny Truck Town safe. Kids learn to find a helper when they're lost, look both ways, hold a grown-up's hand and cross with the green light.\nA fun road safety song about community helpers. Ages 2-5.",
        "tags": ["police car song", "road safety song", "community helpers", "look both ways song", "trucks for kids", "kids songs", "Tiny Truck Town", "3D kids songs"]}))

specs.append(dict(id="fr3d_ep10", base="fr3d_ep06",
  lyrics="""[Chorus]
Let's go shopping, fruit market fun!
Count the fruit, every one!
One, two, three, into the cart,
Fruit market shopping, let's start!

[Verse 1]
One red apple, shiny and round,
Two yellow bananas, the best in town!
Three orange oranges, juicy and sweet,
Count them up, what a treat!

[Chorus]
Let's go shopping, fruit market fun!
Count the fruit, every one!
One, two, three, into the cart,
Fruit market shopping, let's start!

[Verse 2]
Four purple grapes, a bunch to share,
Five strawberries, red with care!
Count them all, one to five,
Fruity Friends come alive!

[Bridge]
Hold up one finger, one!
Two fingers, two, this is fun!
Three, four, five, wiggle them high,
Count with me, wave goodbye!

[Verse 3]
Put them in the basket, say thank you,
Share with friends, they want some too!
Fruit for snack and fruit for lunch,
Fruity Friends love fruit a bunch!

[Chorus]
Let's go shopping, fruit market fun!
Count the fruit, every one!
One, two, three, into the cart,
Fruit market shopping, let's start!

[Outro]
One, two, three! Bye-bye, fruity friends!""",
  props={"chorus1": [T("1, 2, 3!", "#ff5c8a", size=0.8), P("basket", None, at=[0, 0.8, 3.4], delay=1)],
         "verse1": [P("number", "One", at=[-2.6, 1.6, 3.4], opts={"n": 1}), P("bigfruit", "apple,", at=[-2.6, 0.7, 3.4], opts={"kind": "apple"}), P("bigfruit", "bananas,", at=[2.6, 0.9, 3.4], opts={"kind": "banana"}), P("bigfruit", "oranges,", at=[0, 1.6, 3.4], opts={"kind": "orange"})],
         "chorus2": [T("COUNT!", "#ff8a1f", size=0.8)], "verse2": [P("bigfruit", "grapes,", at=[-2.6, 0.9, 3.4], opts={"kind": "grape"}), P("bigfruit", "strawberries,", at=[2.6, 0.9, 3.4], opts={"kind": "strawberry"}), T("1 to 5!", "#ff5c8a", "five,", at=L("c"), size=0.7)],
         "bridge1": [P("number", "one!", at=[-2.6, 1.6, 3.4], opts={"n": 1}), P("number", "two,", at=[2.6, 1.6, 3.4], opts={"n": 2}), T("3, 4, 5!", "#ff8a1f", "Three,", at=L("c"), size=0.7)],
         "verse3": [P("basket", "basket,", at=[0, 0.8, 3.4]), T("SHARE!", "#3cc45a", "Share", size=0.7)],
         "chorus3": [T("1, 2, 3!", "#ff5c8a", size=0.8)], "outro1": [T("BYE-BYE!", "#ff5c8a")]},
  meta={"title": "Fruit Market Counting Song! Count to 5 | Fruity Friends", "card": "Fruit Market Counting!", "thumb_text": "COUNT THE FRUIT!",
        "description": "Let's go fruit shopping! The Fruity Friends count one apple, two bananas, three oranges, four grapes and five strawberries into the basket.\nKids count on their fingers from one to five and learn to share snacks with friends. Ages 2-5.",
        "tags": ["counting song for kids", "count to 5", "fruit song", "numbers for toddlers", "shopping song", "kids songs", "Fruity Friends", "3D kids songs"]}))

specs.append(dict(id="zoo3d_ep09", base="zoo3d_ep05",
  lyrics="""[Chorus]
One little, two little, three little animals,
Four little, five little, six little animals,
Seven little, eight little, nine little animals,
Ten little zoo friends dancing!

[Verse 1]
One big lion with a roar, roar, roar,
Two little monkeys swinging more, more, more!
Three tall giraffes munching on a tree,
Count with Milo, one, two, three!

[Chorus]
One little, two little, three little animals,
Four little, five little, six little animals,
Seven little, eight little, nine little animals,
Ten little zoo friends dancing!

[Verse 2]
Four gray elephants, stomp, stomp, stomp,
Five stripy zebras, romp, romp, romp!
Six happy hippos splashing in the sun,
Counting animals is so much fun!

[Bridge]
Hold up your fingers, let's count to ten,
One, two, three, four, five, and then,
Six, seven, eight, nine, ten,
Let's count the zoo friends once again!

[Verse 3]
Seven parrots flying way up high,
Eight penguins waddling by!
Nine pandas munching, ten owls say hoo,
Ten little friends at the animal zoo!

[Chorus]
One little, two little, three little animals,
Four little, five little, six little animals,
Seven little, eight little, nine little animals,
Ten little zoo friends dancing!

[Outro]
Ten little zoo friends! Bye-bye, friends!""",
  props={"chorus1": [T("1 to 10!", "#ffb627", size=0.8)],
         "verse1": [P("num", "One", at=[-3.2, 1.8, 3.6], opts={"n": 1}), P("num", "Two", at=[0, 2.2, 3.6], opts={"n": 2}), P("num", "Three", at=[3.2, 1.8, 3.6], opts={"n": 3})],
         "chorus2": [T("COUNT!", "#ff7a00", size=0.8)],
         "verse2": [P("num", "Four", at=[-3.2, 1.8, 3.6], opts={"n": 4}), P("num", "Five", at=[0, 2.2, 3.6], opts={"n": 5}), P("num", "Six", at=[3.2, 1.8, 3.6], opts={"n": 6})],
         "bridge1": [T("1, 2, 3, 4, 5", "#ffb627", "One,", size=0.55), T("6, 7, 8, 9, 10!", "#ff7a00", "Six,", at=L("c"), size=0.55)],
         "verse3": [P("num", "Seven", at=[-3.2, 1.8, 3.6], opts={"n": 7}), P("num", "Nine", at=[0, 2.2, 3.6], opts={"n": 9}), P("num", "Ten", at=[3.2, 1.8, 3.6], opts={"n": 10})],
         "chorus3": [T("10 ZOO FRIENDS!", "#ffb627", size=0.6)], "outro1": [T("BYE-BYE!", "#ffb627")]},
  meta={"title": "Ten Little Animals! Counting Song for Kids with Milo", "card": "Ten Little Animals!", "thumb_text": "COUNT TO 10!",
        "description": "Count to ten with Milo and the zoo friends! One big lion, two swinging monkeys, three tall giraffes, four elephants, five zebras, six hippos, seven parrots, eight penguins, nine pandas and ten owls.\nKids count on their fingers from one to ten and roar, stomp and splash along. Ages 2-5.",
        "tags": ["counting song for kids", "count to 10", "ten little animals", "numbers song", "animal song for kids", "kids songs", "The Animated Zoo", "Milo", "3D kids songs"]}))

specs.append(dict(id="mb3d_ep09", base="mb3d_ep05",
  lyrics="""[Chorus]
Close your eyes and float away,
On a soft and fluffy cloud we'll stay,
Drifting, drifting, slow and deep,
Floating gently into sleep.

[Verse 1]
The cloud is soft, as soft can be,
It carries Bunny, Lamb and me,
Over hills all dark and blue,
The moon is smiling down at you.

[Chorus]
Close your eyes and float away,
On a soft and fluffy cloud we'll stay,
Drifting, drifting, slow and deep,
Floating gently into sleep.

[Verse 2]
Past the stars that twinkle bright,
Past the owls who say goodnight,
Gentle breezes hum a tune,
Underneath the silver moon.

[Bridge]
Breathe in slow, the cloud goes high,
Breathe out soft, we float on by,
Heavy arms and heavy feet,
Sleepy dreams are oh so sweet.

[Verse 3]
When the morning sun comes round,
The cloud will bring you safely down,
But for now, just rest your head,
Snuggled warm in your cozy bed.

[Chorus]
Close your eyes and float away,
On a soft and fluffy cloud we'll stay,
Drifting, drifting, slow and deep,
Floating gently into sleep.

[Outro]
Float away, little one. Goodnight.""",
  props={"chorus1": [T("Float Away", "#ffd88a", size=0.55), P("moon", None, at="top", delay=2)], "verse1": [P("moon", "moon", at="top"), P("heart", "Bunny,", at="right")],
         "chorus2": [P("zzz", "sleep.", at="right")], "verse2": [P("numstar", "stars", at="left", opts={"size": 0.4}), P("star", "twinkle", at="right", opts={"size": 0.35})],
         "bridge1": [T("Breathe...", "#bfa8ff", "Breathe", size=0.6)], "verse3": [P("heart", "warm", at="right"), P("zzz", "rest", at="left")],
         "outro1": [P("zzz", "Goodnight.", at="right")]},
  meta={"title": "Float Away on a Cloud 🌙 Sleepy Lullaby for Babies | Moonbeam", "card": "Float Away on a Cloud", "thumb_text": "FLOAT AWAY",
        "description": "A dreamy lullaby about floating on a soft, fluffy cloud past twinkling stars and sleepy owls under the silver moon. Luna, Bunny and Lamb drift gently toward sleep.\nA slow breathing break with heavy arms and heavy feet helps little ones relax. For babies and toddlers.",
        "tags": ["lullaby for babies", "sleep music for babies", "bedtime song", "calming lullaby", "baby sleep", "Moonbeam Bedtime", "3D kids songs"]}))

specs.append(dict(id="gz3d_ep09", base="gz3d_ep05",
  lyrics="""[Chorus]
Solid, liquid, gas, hooray!
Water changes every day!
Freeze it, melt it, watch it go,
Water's magic, now you know!

[Verse 1]
Ice is solid, cold and hard,
Ice cubes and snow in the yard!
Put it in the sun and see,
Ice melts into water, whee!

[Chorus]
Solid, liquid, gas, hooray!
Water changes every day!
Freeze it, melt it, watch it go,
Water's magic, now you know!

[Verse 2]
Water is liquid, splash and pour,
In a cup or on the floor!
Heat it up and steam will rise,
Steam is gas up to the skies!

[Bridge]
Freeze like ice, stand very still!
Melt like water, down the hill!
Float like steam up in the air,
Water changes everywhere!

[Verse 3]
Steam goes up and makes a cloud,
Rain comes down, pitter-patter loud!
Round and round the water goes,
That's the water cycle, now Gizmo knows!

[Chorus]
Solid, liquid, gas, hooray!
Water changes every day!
Freeze it, melt it, watch it go,
Water's magic, now you know!

[Outro]
Solid, liquid, gas! Bye-bye, friends!""",
  props={"chorus1": [T("SOLID! LIQUID! GAS!", "#3b8be0", size=0.55)],
         "verse1": [T("ICE = SOLID", "#7fd3ff", "solid,", size=0.6), P("sun", "sun", at=[-3.0, 1.3, 3.6], opts={"size": 0.7})],
         "chorus2": [T("FREEZE! MELT!", "#3b8be0", size=0.65)], "verse2": [T("WATER = LIQUID", "#3b8be0", "liquid,", size=0.55), P("beaker", "cup", at=[3.0, 1.0, 3.6])],
         "bridge1": [T("FREEZE!", "#7fd3ff", "Freeze", at=L("l"), size=0.7), T("MELT!", "#3b8be0", "Melt", at=L("r"), size=0.7), T("FLOAT!", "#bdbdbd", "Float", at=L("c"), size=0.7)],
         "verse3": [P("raincloud", "cloud,", at=[3.0, 1.6, 3.6]), T("WATER CYCLE!", "#3b8be0", "cycle,", size=0.6)],
         "chorus3": [T("SOLID! LIQUID! GAS!", "#3b8be0", size=0.55)], "outro1": [T("BYE-BYE!", "#3b8be0")]},
  meta={"title": "Ice, Water and Steam! States of Matter Song with Gizmo", "card": "Ice, Water and Steam!", "thumb_text": "ICE, WATER, STEAM!",
        "description": "Solid, liquid, gas! Gizmo the robot shows how water changes: ice is solid, it melts into liquid water, and heated water rises as steam, a gas. Steam makes clouds and rain falls back down in the water cycle.\nKids freeze like ice, melt like water and float like steam. Ages 3-6.",
        "tags": ["states of matter song", "solid liquid gas", "water cycle song", "science song for kids", "STEM for kids", "kids songs", "Gizmo Explains", "3D kids songs"]}))
for s in specs:
    base = B3(s["base"]); spec = copy.deepcopy(base)
    spec["lyrics"] = s["lyrics"]; spec["meta"] = s["meta"]; spec["seed"] = base["seed"] + 400
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
    json.dump(spec, open(f"/root/zoo/specs/b9/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    print(s["id"], len(s["meta"]["title"]), secs)
