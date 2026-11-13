"""Songs v3 (Nov 13, 2026): new-cast, multi-place Zoo songs that follow the VARIETY RULE.
Each song is written for its own animals and its own route of places (sets/zooworld.py).

  python3 make_specs_v3.py     -> songs/<id>.json + jobs/<id>.song.json, variety-checked and recorded in the ledger

The spec holds the coarse route; once the song is sung and jobs/<id>_timing.json exists, run
`python3 routes.py jobs/<id>.json` to turn it into the fine scene plan (each chorus, half-verse and bridge its own scene).
To add a song: append a dict to SONGS (cast = animal kinds from chars/animal.py, route = [(section, biome, tod)]).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import variety

STYLE = ("high-energy modern sing-along pop for families, {bpm} bpm, bright major key, punchy drums and big handclaps, "
         "bouncy synth bass, {flavor}, warm friendly male lead vocal with a cheerful group chorus on every chorus, "
         "call-and-response, verses light and bouncy, pre-chorus builds with a rising snare roll, chorus explodes with full "
         "band and group vocals, short claps-and-stomps breakdown, final chorus modulates up a whole step with the biggest "
         "energy, vocals start right away on the first beat with the chorus, no instrumental intro, short punchy ending")
BOILER = ("The Animated Zoo makes gentle, colorful videos for little learners. New videos every day! Made with care for ages 2-6. "
          "Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing.")
SPOTS = [("s1", 0.22), ("s2", -0.22), ("s3", 0.38), ("s4", -0.38), ("s5", -0.1), ("s6", 0.1)]
T = lambda text, color, size=0.7, **k: dict({"type": "text", "text": text, "color": color, "at": "top", "size": size}, **k)

SONGS = [
 dict(id="zoo3d_ep17", bpm=122, key="G Major", seed=917, flavor="ukulele, marimba and bamboo flute hooks",
      title="Panda Loves Bamboo! Forest Animals Song with Milo", card="Forest Friends!", thumb="PANDA!",
      cast=["panda", "tiger", "monkey", "koala", "fox"],
      route=[("chorus1", "bamboo", "morning"), ("verse1", "jungle", "noon"), ("chorus2", "bamboo", "noon"),
             ("verse2", "autumn_forest", "golden"), ("bridge1", "jungle", "morning"), ("chorus3", "bamboo", "sunset")],
      verses=[["panda", "tiger"], ["monkey", "koala"], ["fox", "host"]],
      words=["CRUNCH!", "STRIPES!", "MUNCH!", "SWING!", "CLAP!", "FLUFFY!", "FOREST FRIENDS!"],
      desc="Meet the forest friends with Milo the bluebird! The panda munches bamboo, the tiger shows its stripes, the monkey swings, "
           "the koala naps in a tree and the fox has a fluffy tail.\nA forest animals song for kids: munch, swing and clap along. Ages 2-6.",
      tags=["panda song for kids", "forest animals song", "animal song for kids", "bamboo song", "kids songs", "preschool learning song", "The Animated Zoo", "Milo"],
      lyrics="""[Chorus - full band, group vocals]
Panda, panda, munch, munch, munch!
Bamboo breakfast, bamboo lunch!
Forest friends, come sing with me,
Clap your hands, one, two, three!

[Verse 1 - light and bouncy]
The panda is black and white,
Eating bamboo, bite by bite!
The tiger has stripes, orange and black,
Stripes on its tail and stripes on its back!

[Pre-Chorus - build up, rising drums]
Who is next? Let's take a look,
Peek around the forest nook!

[Chorus - full band, group vocals]
Panda, panda, munch, munch, munch!
Bamboo breakfast, bamboo lunch!
Forest friends, come sing with me,
Clap your hands, one, two, three!

[Verse 2 - light and bouncy]
The monkey swings from tree to tree,
Swing your arms and swing with me!
The koala naps the day away,
Leaves for dinner, every day!

[Bridge - claps and stomps, call and response]
Munch like a panda! (Munch, munch, munch!)
Swing like a monkey! (Swing, swing, swing!)
Stretch like a tiger! (Stretch up high!)
Now wave your tail and say goodbye!

[Verse 3 - light and bouncy]
The fox has a tail so fluffy and red,
It curls up warm when it goes to bed!
Milo sings up in the tree,
Forest friends, sing along with me!

[Pre-Chorus - build up, rising drums]
Who is next? Let's take a look,
Peek around the forest nook!

[Final Chorus - key change up, biggest energy, everyone sings]
Panda, panda, munch, munch, munch!
Bamboo breakfast, bamboo lunch!
Forest friends, we sang with glee,
Clap your hands, one, two, three!

[Outro - quick and happy]
Munch, munch, munch! Bye-bye, friends!"""),

 dict(id="zoo3d_ep18", bpm=120, key="D Major", seed=918, flavor="sleigh bells, glockenspiel and pizzicato string hooks",
      title="Fluffy Coats! Snowy Animals Song for Kids with Milo", card="Snowy Friends!", thumb="BRRR!",
      cast=["polar_bear", "arctic_fox", "bear", "horse"],
      route=[("chorus1", "arctic", "noon"), ("verse1", "arctic", "morning"), ("chorus2", "mountain", "morning"),
             ("verse2", "autumn_forest", "golden"), ("bridge1", "arctic", "sunset"), ("chorus3", "arctic", "night")],
      verses=[["polar_bear", "arctic_fox"], ["bear", "horse"], ["host", "polar_bear"]],
      words=["BRRR!", "WHITE!", "FLUFFY!", "WARM!", "SHIVER!", "SNOW!", "FLUFFY COATS!"],
      desc="Brrr, it's snowy! Milo the bluebird meets animals with fluffy coats: the polar bear and the arctic fox have white fur for the snow, "
           "the brown bear has thick fur, and the horse grows a warm winter coat.\nA snowy animals song for kids: shiver, hug and stomp along. Ages 2-6.",
      tags=["winter animals song", "snow song for kids", "polar bear song", "arctic animals for kids", "kids songs", "preschool learning song", "The Animated Zoo", "Milo"],
      lyrics="""[Chorus - full band, group vocals]
Fluffy coats, fluffy coats,
Keep us warm in the snow, snow, snow!
Brrr, brrr, shake and spin,
Fluffy coats, let's begin!

[Verse 1 - light and bouncy]
The polar bear has fur so white,
It keeps him cozy day and night!
The arctic fox is white as snow,
Her fluffy tail is warm, you know!

[Pre-Chorus - build up, rising drums]
Rub your hands and stomp your feet,
Warm up, warm up, to the beat!

[Chorus - full band, group vocals]
Fluffy coats, fluffy coats,
Keep us warm in the snow, snow, snow!
Brrr, brrr, shake and spin,
Fluffy coats, let's begin!

[Verse 2 - light and bouncy]
The big brown bear has fur so thick,
It keeps her warm, that is the trick!
The horse grows a coat when the cold winds blow,
A winter coat, from head to toe!

[Bridge - claps and stomps, call and response]
Shiver, shiver! (Brrr, brrr, brrr!)
Give a hug! (Hug, hug, hug!)
Stomp the snow! (Stomp, stomp, stomp!)
Now spin around and off we go!

[Verse 3 - light and bouncy]
Milo fluffs his feathers blue,
Feathers keep him cozy too!
Put on your coat, your hat, your mitts,
Now we are warm, just like this!

[Pre-Chorus - build up, rising drums]
Rub your hands and stomp your feet,
Warm up, warm up, to the beat!

[Final Chorus - key change up, biggest energy, everyone sings]
Fluffy coats, fluffy coats,
Keep us warm in the snow, snow, snow!
Brrr, brrr, we shook and spun,
Fluffy coats, that was fun!

[Outro - quick and happy]
Stay warm! Bye-bye, friends!"""),

 dict(id="zoo3d_ep19", bpm=124, key="C Major", seed=919, flavor="banjo, fiddle and ukulele hooks",
      title="Good Morning, Farm! Animal Sounds Song with Milo", card="Good Morning, Farm!", thumb="MOO!",
      cast=["cow", "pig", "horse"],
      route=[("chorus1", "farm", "morning"), ("verse1", "farm", "noon"), ("chorus2", "spring_meadow", "noon"),
             ("verse2", "river", "golden"), ("bridge1", "spring_meadow", "morning"), ("chorus3", "farm", "sunset")],
      verses=[["cow", "pig"], ["horse", "host"], ["cow", "pig", "horse"]],
      words=["MOO!", "MOO!", "OINK!", "NEIGH!", "TWEET!", "HELLO!", "GOOD MORNING!"],
      desc="Good morning, farm! Sing the animal sounds with Milo the bluebird: the cow says moo, the pig says oink, the horse says neigh "
           "and Milo says tweet.\nA farm animal sounds song for kids: moo, oink and neigh along. Ages 2-6.",
      tags=["farm animal sounds song", "farm song for kids", "animal sounds for kids", "moo oink neigh", "kids songs", "preschool learning song", "The Animated Zoo", "Milo"],
      lyrics="""[Chorus - full band, group vocals]
Good morning, farm! The sun is up!
Moo and oink and clip, clip, clop!
Every friend has a sound to say,
Sing it loud to start the day!

[Verse 1 - light and bouncy]
The cow says moo, moo, moo,
She eats green grass, chew, chew, chew!
The pig says oink, oink, oink,
He rolls in mud, boink, boink, boink!

[Pre-Chorus - build up, rising drums]
What do you hear? What do you hear?
Cup your hands around your ear!

[Chorus - full band, group vocals]
Good morning, farm! The sun is up!
Moo and oink and clip, clip, clop!
Every friend has a sound to say,
Sing it loud to start the day!

[Verse 2 - light and bouncy]
The horse says neigh, neigh, neigh,
She trots around the field all day!
Milo says tweet, tweet, tweet,
He sings a song so soft and sweet!

[Bridge - claps and stomps, call and response]
Moo like a cow! (Moo, moo, moo!)
Oink like a pig! (Oink, oink, oink!)
Neigh like a horse! (Neigh, neigh, neigh!)
Now tweet like Milo and shout hooray!

[Verse 3 - light and bouncy]
Moo and oink and neigh and tweet,
Clap your hands and stomp your feet!
Every sound is fun to do,
The farm friends sing along with you!

[Pre-Chorus - build up, rising drums]
What do you hear? What do you hear?
Cup your hands around your ear!

[Final Chorus - key change up, biggest energy, everyone sings]
Good morning, farm! The sun is up!
Moo and oink and clip, clip, clop!
Every friend had a sound to say,
We sang it loud to start the day!

[Outro - quick and happy]
Moo! Oink! Neigh! Bye-bye, friends!"""),
]

COLORS = ["#ffb627", "#3db8ff", "#ff7a00", "#8e5bd8", "#3cc45a", "#ff6fb5", "#ffb627"]


def build(s):
    assert len(s["title"]) <= 60, s["title"]
    cast = [{"id": "host", "char": "milo", "spot": "center"}]
    for k, kind in enumerate(s["cast"]):
        cast.append({"id": kind, "char": "animal", "spot": SPOTS[k][0], "opts": {"kind": kind}, "yaw": SPOTS[k][1]})
    closes = lambda who: [x for w in who for x in ("close:" + w, "wide" if w == who[-1] else "close:host")]
    all_close = [f"close:{k}" for k in s["cast"]]
    W = s["words"]
    chorus = lambda i, shots: {"section": f"chorus{i}", "shots": shots, "energy": 1.0, "wave": 1, "jump": 0.4, "group": True}
    verse = lambda i: {"section": f"verse{i}", "shots": closes(s["verses"][i - 1]) + ["side"], "energy": 0.75, "wave": 0, "jump": 0.15, "group": False}
    pre = lambda i: {"section": f"prechorus{i}", "shots": ["close:host", "low"], "energy": 0.9, "wave": 1, "jump": 0.2, "group": True, "props": []}
    direct = [dict(chorus(1, ["wide", "close:host", "orbit", all_close[0], "low"]), props=[T(W[0], COLORS[0])]),
              dict(verse(1), props=[T(W[1], COLORS[1])]), pre(1),
              dict(chorus(2, ["vista", "close:host", "orbit", all_close[-1], "low"]), props=[T(W[2], COLORS[2])]),
              dict(verse(2), props=[T(W[3], COLORS[3])]),
              {"section": "bridge1", "shots": ["wide", "low"] + all_close + ["orbit"], "energy": 1.0, "wave": 1, "jump": 0.5, "group": True, "props": [T(W[4], COLORS[4])]},
              dict(verse(3), props=[T(W[5], COLORS[5])]), pre(2),
              dict(chorus(3, ["orbit", "hero", "wide", "close:host", "high"]), props=[T(W[6], COLORS[6], 0.6)]),
              {"section": "outro1", "shots": ["close:host", "wide"], "energy": 0.7, "wave": 1, "jump": 0.2, "group": True, "props": [T("BYE-BYE!", "#ffb627", 0.8)]}]
    job = {"id": s["id"], "title": s["card"], "channel": "zoo", "set": "zooworld", "set_opts": {}, "seed": s["seed"] % 50, "new_song": True,
           "cast": cast, "verses": s["verses"], "locations": [{"from": a, "biome": b, "tod": t, **({"seed": i} if i else {})} for i, (a, b, t) in enumerate(s["route"])],
           "intro_shot": "orbit", "intro": {"energy": 0.6, "wave": 1}, "thumb_frame": 96, "direct": direct, "song": s["id"],
           "res": "1920x1080", "step": 1, "cut_mode": "beat", "cut_beats": {"chorus": 4, "bridge": 4, "prechorus": 2}, "follow_singer": True, "punch": True}
    spec = {"style": STYLE.format(bpm=s["bpm"], flavor=s["flavor"]), "lyrics": s["lyrics"], "duration": 160, "bpm": s["bpm"], "key": s["key"],
            "seed": s["seed"], "who_map": {},
            "meta": {"title": s["title"], "card": s["card"], "thumb_text": s["thumb"], "description": s["desc"] + "\n\n" + BOILER,
                     "tags": s["tags"], "song_v": "v3 new cast + places (Nov 13)"}, "job": job}
    return spec


if __name__ == "__main__":
    for s in SONGS:
        spec = build(s)
        why = variety.check(spec["job"])
        if why: sys.exit(f"{s['id']} repeats: {why}")
        for p in (f"songs/{s['id']}.json", f"jobs/{s['id']}.song.json"):
            json.dump(spec, open(os.path.join(HERE, p), "w"), indent=1)
        variety.record(spec["job"]); print("OK", s["id"], s["title"], [l["biome"] for l in spec["job"]["locations"]])
