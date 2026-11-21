import json, copy, os
Z = "/root/zoo/blender/zoo3d"
v2 = lambda n: {d["section"]: d for d in json.load(open(f"{Z}/jobs/{n}_v2.json"))["direct"]}
cast = lambda n: json.load(open(f"{Z}/jobs/{n}_v2.json"))["cast"]
def sec(name, src, **kw):
    d = copy.deepcopy(src); d["section"] = name; d.update(kw); return d
def num_props(words, cols, y=0.8, z=3.7, x0=-2.6, dx=1.3):
    return [{"type": "set_prop", "name": "number", "word": w, "at": [round(x0 + i * dx, 2), y, z], "opts": {"n": i + 1, "text": str(i + 1), "color": c}} for i, (w, c) in enumerate(zip(words, cols))]
COLS = ["#e8302a", "#ff9f1a", "#ffc107", "#2fb59a", "#3b8be0"]
NOINTRO = "vocals start right away on the first beat, no long intro, short outro"
specs = []

# ---------------- Tiny Truck Town
D = v2("tt3d_ep01")
truck_num = [{"type": "set_prop", "name": "number", "word": w, "at": [x, 1.6, 3.6], "opts": {"n": i + 1, "color": c}} for i, (w, x, c) in enumerate(zip(["one", "two", "three", "four"], [-2.7, -0.9, 0.9, 2.7], COLS))]
v1 = sec("verse1", D["verse1"]); v1["props"] = [p for p in v1["props"] if p.get("name") != "number"] + truck_num
specs.append(dict(id="tt3d_ep01", job_id="tt3d_ep01_v3", channel="truck",
  style="upbeat preschool kids pop rock sing-along, cheerful friendly young male vocal, clear diction, electric guitar, handclaps, siren synth, bouncy drums, major key, catchy repetitive chorus, " + NOINTRO,
  bpm=120, key="D Major", duration=165, seed=11,
  lyrics="""[Chorus]
Fire truck, fire truck, big and red!
Ladder up and hoses spray!
Wee-oo, wee-oo, clear the way!
Fire truck, fire truck, saves the day!

[Verse 1]
Up, up, up goes the ladder,
Up so high into the sky!
Count the steps: one, two, three, four!
Firefighters climb up high!

[Chorus]
Fire truck, fire truck, big and red!
Ladder up and hoses spray!
Wee-oo, wee-oo, clear the way!
Fire truck, fire truck, saves the day!

[Verse 2]
Here's the hose, it's long and strong,
Water from the hydrant comes along!
Spray, spray, spray it high and low,
Whoosh! The water starts to flow!

[Bridge]
Clap, clap! Clap your hands with me!
Stomp, stomp! Stomp like a big truck!
Jump, jump! Jump up, one, two, three!
Honk, honk! Beep, beep! Here we go!

[Verse 3]
See the lights go flash, flash, flash,
Hear the siren: wee-oo, wee-oo!
Cars move over, make some room,
Fire truck's coming, zoom, zoom, zoom!

[Verse 4]
Helmets, boots and big strong coats,
Firefighters stay safe and warm!
Thank you, thank you, brave and kind,
Firefighters help all the time!

[Chorus]
Fire truck, fire truck, big and red!
Ladder up and hoses spray!
Wee-oo, wee-oo, clear the way!
Fire truck, fire truck, saves the day!

[Outro]
Wee-oo, wee-oo! Bye-bye, fire truck!""",
  direct=[sec("chorus1", D["chorus1"]), v1, sec("chorus2", D["chorus2"]), sec("verse2", D["verse2"]), sec("bridge1", D["action"]),
          sec("verse3", D["verse3"]), sec("verse4", D["fact2"], shots=["close:host", "wide", "close:police", "close:host"], energy=0.6),
          sec("chorus3", D["chorus4"]), sec("outro1", D["outro"])],
  cast=cast("tt3d_ep01"), set="town", intro_shot="orbit", intro={"energy": 0.8, "jump": 0.3},
  meta={"title": "Fire Truck Song for Kids! Wee-oo with Bolt the Fire Truck", "card": "Fire Truck Song!", "thumb_text": "FIRE TRUCK SONG!",
        "description": "The Fire Truck Song for kids! Sing along with Bolt the fire truck and his truck friends in Tiny Truck Town.\nKids learn what fire trucks do: ladders, hoses, sirens and lights, and how firefighters stay safe. Count 1 to 4, then clap, stomp and jump along. Ages 2-6.",
        "tags": ["fire truck song", "fire truck for kids", "trucks for kids", "kids songs", "nursery rhymes", "vehicle songs", "wee-oo song", "Tiny Truck Town", "3D kids songs"]}))

# ---------------- Moonbeam Bedtime
D = v2("mb3d_ep01")
c1 = sec("chorus1", D["chorus1"]); c1["props"] = [{"type": "text", "text": "Time for Bed!", "color": "#ffd88a", "at": "top", "size": 0.8}] + [p for p in c1["props"] if p.get("type") != "text"]
specs.append(dict(id="mb3d_ep01", job_id="mb3d_ep01_v3", channel="moon",
  style="gentle bedtime lullaby for toddlers, soft warm female vocal, slow and calm, music box, soft piano, light strings, dreamy, sleepy, clear gentle diction, " + NOINTRO,
  bpm=76, key="F Major", duration=170, seed=5,
  lyrics="""[Chorus]
Time for bed, sleepyhead,
Moon is glowing, stars are bright,
Snuggle down in your cozy bed,
Time for bed, sleepyhead, goodnight.

[Verse 1]
Splash and splash in the warm bath,
Bubbles float up, pop, pop, pop!
Brush, brush, brush our little teeth,
Up and down and round and round.

[Chorus]
Time for bed, sleepyhead,
Moon is glowing, stars are bright,
Snuggle down in your cozy bed,
Time for bed, sleepyhead, goodnight.

[Verse 2]
One arm in, and two arms in,
Our pajamas, soft and warm.
Pick a book and snuggle close,
Turn the pages, one, two, three.

[Bridge]
Wave goodnight to the moon and stars,
Yawn so big and stretch up slow.
Sleep helps you grow big and strong,
Rest your head and hum along.

[Verse 3]
Big warm hug, a squeeze so tight,
Kiss goodnight and dim the light.
Teddy's here, the night light glows,
Close your eyes now, nice and slow.

[Chorus]
Time for bed, sleepyhead,
Moon is glowing, stars are bright,
Snuggle down in your cozy bed,
Time for bed, sleepyhead, goodnight.

[Outro]
Sweet dreams, sleepyhead, goodnight.""",
  direct=[c1, sec("verse1", D["verse1"]), sec("chorus2", D["chorus2"]), sec("verse2", D["verse2"]), sec("bridge1", D["wave"]),
          sec("verse3", D["verse3"]), sec("chorus3", D["chorus4"]), sec("outro1", D["outro"])],
  cast=cast("mb3d_ep01"), set="nightroom", intro_shot="wide", intro={"energy": 0.2},
  meta={"title": "Time for Bed Song for Kids! Bedtime Routine with Luna", "card": "Time for Bed, Sleepyhead!", "thumb_text": "TIME FOR BED!",
        "description": "Time for Bed, Sleepyhead! A calm bedtime routine song for kids, with Luna the sleepy owl and her friends.\nSing along: bath time, brushing teeth, pajamas, a story, a big hug and goodnight. A gentle lullaby to help little ones wind down. Ages 2-6.",
        "tags": ["bedtime song", "bedtime routine song", "lullaby for kids", "time for bed song", "goodnight song", "sleepy songs for toddlers", "nursery rhymes", "Moonbeam Bedtime", "3D kids songs"]}))

# ---------------- The Animated Zoo
D = v2("zoo3d_ep01")
def merge(name, a, b, **kw):
    d = sec(name, D[a], **kw); d["props"] = d.get("props", []) + [dict(p, delay=p.get("delay", 0) + 8.3) for p in D[b].get("props", [])]; return d
c1 = sec("chorus1", D["chorus1"]); c1["props"] = [{"type": "text", "text": "SAVANNA!", "color": "#ffb627", "at": "top", "size": 0.9}] + [p for p in c1.get("props", []) if p.get("type") != "text"]
br = sec("bridge1", D["action"])
for p, w in zip([p for p in br.get("props", []) if p.get("type") == "text"], ["stomp", "stretch", "swish", "clap"]):
    p["word"] = w; p["delay"] = 0
specs.append(dict(id="zoo3d_ep01", job_id="zoo3d_ep01_v3", channel="zoo",
  style="upbeat preschool kids pop sing-along, cheerful friendly male vocal, clear diction, african percussion, marimba, ukulele, handclaps, bouncy bass, major key, catchy repetitive chorus, " + NOINTRO,
  bpm=116, key="G Major", duration=180, seed=3,
  who_map={"lion1": "lion", "elephant1": "elephant", "giraffe1": "giraffe", "zebra1": "zebra", "hippo1": "hippo", "bridge1": "all"},
  lyrics="""[Chorus]
Savanna, savanna, who lives there?
Big and small, let's meet them all!
Savanna, savanna, sunny and warm,
Savanna, savanna, who lives there?

[Lion]
I'm a lion, look at my mane!
I live with my family, a pride!
Lions say roar, roar, roar!
Roar like a lion, everybody, roar!

[Elephant]
I'm an elephant, big and gray,
My trunk can smell and drink all day!
Elephants go toot, toot, toot!
Toot like an elephant, toot, toot, toot!

[Chorus]
Savanna, savanna, who lives there?
Big and small, let's meet them all!
Savanna, savanna, sunny and warm,
Savanna, savanna, who lives there?

[Giraffe]
I'm a giraffe, so very tall,
I munch the leaves above it all!
Stretch your neck up to the sky,
Stretch up tall, way up high!

[Zebra]
I'm a zebra, black and white,
My stripes are such a lovely sight!
Gallop, gallop, swish my tail,
Gallop, gallop, down the trail!

[Bridge]
Stomp like an elephant, stomp, stomp, stomp!
Stretch like a giraffe, up so high!
Swish like a zebra, swish, swish, swish!
Clap for the lion and roar so loud!

[Hippo]
I'm a hippo, I love to swim,
Splash all day, come jump right in!
Mud and water keep me cool,
The river is my swimming pool!

[Chorus]
Savanna, savanna, who lives there?
Big and small, let's meet them all!
Savanna, savanna, sunny and warm,
Savanna, savanna, who lives there?

[Outro]
Bye-bye, savanna! Bye-bye, friends!""",
  direct=[c1, merge("lion1", "verse_lion", "fact_lion"), merge("elephant1", "verse_elephant", "fact_elephant"), sec("chorus2", D["chorus2"]),
          merge("giraffe1", "verse_giraffe", "fact_giraffe"), merge("zebra1", "verse_zebra", "fact_zebra"), br,
          merge("hippo1", "verse_hippo", "fact_hippo"), sec("chorus3", D["chorus5"]), sec("outro1", D["outro"])],
  cast=cast("zoo3d_ep01"), set="savanna", intro_shot="orbit", intro={"energy": 0.8, "wave": 1},
  meta={"title": "Safari Animals Song for Kids! Roar and Stomp with Milo", "card": "Safari Animals Song!", "thumb_text": "SAFARI ANIMALS!",
        "description": "The Safari Animals Song for kids! Sing along with Milo on the sunny savanna and meet a lion, an elephant, a giraffe, a zebra and a hippo.\nKids learn real animal facts and copy the animals: roar, stomp, stretch and swish. Ages 2-6.",
        "tags": ["animal song for kids", "safari animals song", "savanna animals", "zoo animals for kids", "lion song", "elephant song", "kids songs", "nursery rhymes", "The Animated Zoo", "Milo"]}))

# ---------------- Fruity Friends (new episode 2)
fr_cast = [{"id": "host", "char": "fruit", "spot": "center", "opts": {"kind": "pipkiko"}},
           {"id": "apple", "char": "fruit", "spot": "left", "opts": {"kind": "apple"}, "yaw": 0.22},
           {"id": "banana", "char": "fruit", "spot": "right", "opts": {"kind": "banana"}, "yaw": -0.22},
           {"id": "orange", "char": "fruit", "spot": "farleft", "opts": {"kind": "orange"}, "yaw": 0.35},
           {"id": "grape", "char": "fruit", "spot": "farright", "opts": {"kind": "grape"}, "yaw": -0.35}]
FIVE = ["one", "two", "three", "four", "five"]
chorus = lambda n, shots: {"section": n, "shots": shots, "energy": 0.9, "group": True, "wave": 1,
    "props": [{"type": "text", "text": "COUNT TO 5!", "color": "#ff5c8a", "at": "top", "size": 0.6}] + num_props(FIVE, COLS, y=0.6, z=4.2)}
big = lambda kind, word, x: {"type": "set_prop", "name": "bigfruit", "word": word, "at": [x, 0.9, 3.4], "opts": {"kind": kind}}
specs.append(dict(id="fr3d_ep02", job_id="fr3d_ep02", channel="fruity",
  style="upbeat preschool kids pop sing-along, cheerful sweet female vocal, clear diction, bright ukulele, xylophone, handclaps, bouncy bass, major key, catchy repetitive counting chorus, " + NOINTRO,
  bpm=118, key="C Major", duration=160, seed=21,
  lyrics="""[Chorus]
One, two, three, four, five,
Count the fruits and come alive!
Yummy, yummy, in my tummy,
Count with me, one to five!

[Verse 1]
One red apple, round and sweet,
Crunch, crunch, crunch, a healthy treat!
Two yellow bananas, peel them slow,
One, two bananas, here we go!

[Chorus]
One, two, three, four, five,
Count the fruits and come alive!
Yummy, yummy, in my tummy,
Count with me, one to five!

[Verse 2]
Three orange oranges, juicy and bright,
Squeeze them up and take a bite!
Four purple grapes, so small and round,
One, two, three, four, all found!

[Bridge]
Clap one time, clap!
Stomp two times, stomp, stomp!
Jump three times, jump, jump, jump!
Spin around and count again!

[Verse 3]
Five red strawberries in a bowl,
Seeds on the outside, count them all!
One, two, three, four, five,
Fruits and colors, high five!

[Chorus]
One, two, three, four, five,
Count the fruits and come alive!
Yummy, yummy, in my tummy,
Count with me, one to five!

[Outro]
Five yummy fruits! See you tomorrow!""",
  direct=[chorus("chorus1", ["wide", "close:host", "low", "close:host"]),
          {"section": "verse1", "shots": ["close:apple", "wide", "close:banana", "close:host"], "energy": 0.75,
           "props": [big("apple", "apple", -2.6), {"type": "set_prop", "name": "number", "word": "one", "at": [-2.6, 0.8, 4.6], "opts": {"text": "1", "color": "#e8302a"}},
                     {"type": "set_prop", "name": "banana_hand", "word": "bananas", "at": "right"}, {"type": "set_prop", "name": "number", "word": "two", "at": [2.6, 0.8, 4.6], "opts": {"text": "2", "color": "#ffc107"}}]},
          chorus("chorus2", ["orbit", "close:host", "wide", "close:host"]),
          {"section": "verse2", "shots": ["close:orange", "wide", "close:grape", "close:host"], "energy": 0.75,
           "props": [big("orange", "oranges", -2.6), {"type": "set_prop", "name": "number", "word": "three", "at": [-2.6, 0.8, 4.6], "opts": {"text": "3", "color": "#ff9f1a"}},
                     big("grape", "grapes", 2.6), {"type": "set_prop", "name": "number", "word": "four", "nth": 0, "at": [2.6, 0.8, 4.6], "opts": {"text": "4", "color": "#8e5bd8"}}]},
          {"section": "bridge1", "shots": ["wide", "low", "orbit", "wide"], "energy": 1.0, "group": True, "wave": 1, "jump": 0.5,
           "props": [{"type": "text", "text": "CLAP!", "color": "#ff5c8a", "word": "clap", "at": [-3.4, 0.3, 3.5], "size": 0.7},
                     {"type": "text", "text": "STOMP!", "color": "#ff9416", "word": "stomp", "at": [3.4, 0.3, 3.5], "size": 0.7},
                     {"type": "text", "text": "JUMP!", "color": "#3cc45a", "word": "jump", "at": [-1.3, 0.6, 4.3], "size": 0.7},
                     {"type": "text", "text": "SPIN!", "color": "#3f8cff", "word": "spin", "at": [1.3, 0.6, 4.3], "size": 0.7}]},
          {"section": "verse3", "shots": ["close:host", "wide", "close:host", "low"], "energy": 0.8,
           "props": [big("strawberry", "strawberries", 0.0), {"type": "set_prop", "name": "basket", "at": "left", "delay": 2}] + num_props(FIVE, COLS, y=0.6, z=4.2)},
          chorus("chorus3", ["low", "close:host", "orbit", "wide"]),
          {"section": "outro1", "shots": ["wide"], "energy": 0.6, "group": True, "wave": 1,
           "props": [{"type": "text", "text": "SEE YOU TOMORROW!", "color": "#ff5c8a", "at": "top", "size": 0.5}, {"type": "set_prop", "name": "heart", "at": "right"}]}],
  cast=fr_cast, set="kitchen", intro_shot="orbit", intro={"energy": 0.6, "wave": 1},
  meta={"title": "Fruit Counting Song for Kids! Count 1 to 5 with Pipkiko", "card": "Count the Fruits!", "thumb_text": "COUNT 1 TO 5!",
        "description": "The Fruit Counting Song for kids! Count from 1 to 5 with Pipkiko and the Fruity Friends: apples, bananas, oranges, grapes and strawberries.\nKids practice counting, fruit names and colors, then clap, stomp, jump and spin along. Ages 2-5.",
        "tags": ["counting song", "count to 5", "fruit song for kids", "numbers song", "learn to count", "kids songs", "nursery rhymes", "Fruity Friends", "3D kids songs"]}))

# ---------------- Gizmo Explains (new episode 2)
gz_cast = cast("gz3d_ep01")
specs.append(dict(id="gz3d_ep02", job_id="gz3d_ep02", channel="gizmo",
  style="upbeat preschool kids electro pop sing-along, cheerful playful male vocal, clear diction, bright synths, bleepy robot sounds, handclaps, bouncy drums, major key, catchy repetitive chorus, " + NOINTRO,
  bpm=118, key="E Major", duration=165, seed=9,
  lyrics="""[Chorus]
What's the weather, weather today?
Look outside and you can say!
Sunny, rainy, windy, snow,
What's the weather? Here we go!

[Verse 1]
Sunny, sunny, the sun is out,
Warm and bright, we run about!
Wear your hat and drink water too,
The sun gives light to me and you!

[Verse 2]
Rainy, rainy, drip, drop, drip,
Clouds are full, the raindrops slip!
Boots and umbrella, splash, hooray,
Rain helps flowers grow each day!

[Chorus]
What's the weather, weather today?
Look outside and you can say!
Sunny, rainy, windy, snow,
What's the weather? Here we go!

[Verse 3]
Windy, windy, whoosh, whoosh, whoosh,
Leaves are dancing, see them go!
Wind is air that moves, you know,
Kites fly high when the wind blows!

[Verse 4]
Snowy, snowy, cold and white,
Snowflakes falling, soft and light!
Every snowflake, tiny and new,
Is made of ice, it's really true!

[Bridge]
Sunny, stretch your arms up high!
Rainy, wiggle fingers, drip, drop, drip!
Windy, sway from side to side!
Snowy, shiver, brrr, and freeze!

[Chorus]
What's the weather, weather today?
Look outside and you can say!
Sunny, rainy, windy, snow,
What's the weather? Here we go!

[Outro]
Sunny, rainy, windy, snow! Bye-bye, friends!""",
  direct=[{"section": "chorus1", "shots": ["close:host", "wide", "orbit", "low"], "energy": 0.9, "group": True, "wave": 1,
           "props": [{"type": "text", "text": "WEATHER SONG", "color": "#3b8be0", "at": "top", "size": 0.7},
                     {"type": "set_prop", "name": "sun", "word": "sunny", "at": [-3.2, 1.0, 3.6], "opts": {"size": 0.7}},
                     {"type": "set_prop", "name": "raincloud", "word": "rainy", "at": [3.2, 1.0, 3.6], "opts": {"size": 0.8}}]},
          {"section": "verse1", "shots": ["wide", "close:host", "wide", "close:host"], "energy": 0.8,
           "props": [{"type": "set_prop", "name": "sun", "word": "sunny", "at": [0.0, 1.2, 3.4], "opts": {"size": 1.0}},
                     {"type": "text", "text": "SUNNY!", "color": "#ffb627", "word": "sunny", "nth": 1, "at": "top", "size": 0.8}]},
          {"section": "verse2", "shots": ["wide", "close:host", "close:pal", "close:host"], "energy": 0.75,
           "props": [{"type": "set_prop", "name": "raincloud", "word": "rainy", "at": [0.0, 1.2, 3.4], "opts": {"size": 1.1}},
                     {"type": "text", "text": "RAINY!", "color": "#3db8ff", "word": "rainy", "nth": 1, "at": "top", "size": 0.8}]},
          {"section": "chorus2", "shots": ["orbit", "close:host", "wide", "low"], "energy": 0.9, "group": True,
           "props": [{"type": "set_prop", "name": "sun", "word": "sunny", "at": [-3.2, 1.0, 3.6], "opts": {"size": 0.7}},
                     {"type": "set_prop", "name": "raincloud", "word": "rainy", "at": [3.2, 1.0, 3.6], "opts": {"size": 0.8}}]},
          {"section": "verse3", "shots": ["wide", "close:host", "wide", "close:pal"], "energy": 0.9, "jump": 0.2,
           "props": [{"type": "text", "text": "WINDY!", "color": "#2fb59a", "word": "windy", "nth": 1, "at": "top", "size": 0.8},
                     {"type": "set_prop", "name": "rocket", "word": "kites", "at": [2.8, 1.2, 3.6], "opts": {"size": 0.6}}]},
          {"section": "verse4", "shots": ["close:host", "wide", "close:host", "wide"], "energy": 0.7,
           "props": [{"type": "text", "text": "SNOWY!", "color": "#9fd8ff", "word": "snowy", "nth": 1, "at": "top", "size": 0.8},
                     {"type": "set_prop", "name": "star", "word": "snowflakes", "at": [-2.6, 1.6, 3.6], "opts": {"size": 0.5}},
                     {"type": "set_prop", "name": "star", "word": "snowflake", "at": [2.6, 1.6, 3.6], "opts": {"size": 0.5}}]},
          {"section": "bridge1", "shots": ["wide", "low", "orbit", "wide"], "energy": 1.0, "group": True, "wave": 1, "jump": 0.4,
           "props": [{"type": "text", "text": "STRETCH!", "color": "#ffb627", "word": "stretch", "at": [-3.4, 0.3, 3.5], "size": 0.7},
                     {"type": "text", "text": "WIGGLE!", "color": "#3db8ff", "word": "wiggle", "at": [3.4, 0.3, 3.5], "size": 0.7},
                     {"type": "text", "text": "SWAY!", "color": "#2fb59a", "word": "sway", "at": [-1.3, 0.6, 4.3], "size": 0.7},
                     {"type": "text", "text": "BRRR!", "color": "#9fd8ff", "word": "brrr", "at": [1.3, 0.6, 4.3], "size": 0.7}]},
          {"section": "chorus3", "shots": ["wide", "close:host", "orbit", "low"], "energy": 1.0, "group": True, "wave": 1,
           "props": [{"type": "text", "text": "WEATHER SONG", "color": "#3b8be0", "at": "top", "size": 0.7},
                     {"type": "set_prop", "name": "sun", "word": "sunny", "at": [-3.2, 1.0, 3.6], "opts": {"size": 0.7}},
                     {"type": "set_prop", "name": "raincloud", "word": "rainy", "at": [3.2, 1.0, 3.6], "opts": {"size": 0.8}}]},
          {"section": "outro1", "shots": ["wide"], "energy": 0.6, "group": True, "wave": 1,
           "props": [{"type": "text", "text": "BYE BYE!", "color": "#3b8be0", "at": "top", "size": 0.7}, {"type": "set_prop", "name": "sun", "at": [3.0, 1.2, 3.6], "opts": {"size": 0.6}}]}],
  cast=gz_cast, set="sciencelab", intro_shot="orbit", intro={"energy": 0.6},
  meta={"title": "Weather Song for Kids! Sunny, Rainy, Windy with Gizmo", "card": "The Weather Song!", "thumb_text": "WEATHER SONG!",
        "description": "The Weather Song for kids! Sing along with Gizmo the robot and learn sunny, rainy, windy and snowy weather.\nKids learn simple weather facts (rain helps plants grow, wind is moving air, snowflakes are made of ice) and act out each kind of weather. Ages 2-6.",
        "tags": ["weather song", "weather for kids", "sunny rainy song", "learn weather", "science for kids", "kids songs", "nursery rhymes", "Gizmo Explains", "3D kids songs"]}))

out = "/root/zoo/specs/out"; os.makedirs(out, exist_ok=True)
for s in specs:
    job = {"id": s["job_id"], "title": s["meta"]["card"], "channel": s["channel"], "set": s["set"], "seed": 7, "cast": s["cast"],
           "intro_shot": s["intro_shot"], "intro": s["intro"], "thumb_frame": 96, "direct": s["direct"], "song": s["id"],
           "res": "1280x720", "step": 2}
    spec = {"style": s["style"], "lyrics": s["lyrics"], "duration": s["duration"], "bpm": s["bpm"], "key": s["key"], "seed": s["seed"],
            "who_map": s.get("who_map", {}), "meta": s["meta"], "job": job}
    assert len(s["meta"]["title"]) <= 60, s["meta"]["title"]
    json.dump(spec, open(f"{out}/{s['id']}.song.json", "w"), indent=1)
    json.dump(spec, open(f"{Z}/songs/{s['id']}.json", "w"), indent=1)
    secs = [d["section"] for d in s["direct"]]
    print(s["id"], s["job_id"], len(s["meta"]["title"]), secs)
