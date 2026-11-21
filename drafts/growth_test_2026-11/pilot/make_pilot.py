"""Pilot draft "Whose Feet Are These? Guess With Milo" (zool_g01).

Writes, next to this file:
  zool_g01.json   lesson spec in the studio/zoo3d/teach.py format (same schema as lessons/zool_ep16.json)
  script.md       timed script (narration, answer pauses, music and sound cues), times ESTIMATED from the pace
                  measured on zool_ep12/13/16 (speech 3.09 words/s, 0.75 s between lines, the pauses teach.py adds)
  shotlist.md     shot list for the existing Blender lesson workflow (zooworld set, current Milo and animal rigs)

DRAFT ONLY. Nothing here is built, scheduled or uploaded. To build it later: copy zool_g01.json into
studio/zoo3d/lessons/ and run `python3 teach.py lessons/zool_g01.json` (that re-times every line exactly; the
times below are estimates). The new prop "footprint" must be added to teachprops.py first (see shotlist.md).
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
WPS, GAP, SEG_GAP = 3.09, 0.75, 1.3          # measured on zool_ep12/13/16 timings (median), teach.py SEG_GAP
ASK_WAIT, THINK_WAIT, DO_WAIT = 4.0, 3.1, 3.3   # gaps measured after an answer-sign question, a "Hmm." line, an action line

FACTS = [
    "Elephant: 'on tiptoes,' with bone digits angled toward ground; wedge-shaped fat pads 'cushion bottoms of feet', "
    "'absorb shock from impact with ground'; savanna elephants '4 to 5 nails on forefeet, 3 to 5 on hind feet'; 'may detect "
    "vibrations through their feet, bones, and inner ear structures' (SDZWA Library fact sheet 'African Elephant', "
    "Physical Characteristics, ielc.libguides.com/sdzg/factsheets/african_elephant/characteristics, read Nov 19 2026).",
    "Giraffe: 'their feet are 12 inches (30.5 cm) across'; 'two weight-bearing hooves on each foot'; 'The animal's legs "
    "are also 6 feet long'; 'At just an hour after birth, they can stand up and walk around' (Live Science 'Giraffes: "
    "Facts about the tallest animals', livescience.com/27336-giraffes.html, read Nov 19 2026). 'About an hour after birth, "
    "the calf can already start to stand up and walk' (PBS Nature 'Giraffe Fact Sheet', read Nov 19 2026).",
    "Giraffe walk: 'Alternate moving the two right limbs together and then the two left'; this 'keeps front legs from "
    "tangling with hind legs' (SDZWA Library fact sheet 'Giraffe', Behavior & Ecology, "
    "ielc.libguides.com/sdzg/factsheets/giraffes/behavior, read Nov 19 2026).",
    "Zebra: 'Single toe at terminus of each limb'; 'Hooves enclose and protect the toe'; hoof is 'Modified skin, grows "
    "continually'; 'Unique pattern on each individual' (SDZWA Library fact sheet 'Plains Zebra', Physical "
    "Characteristics, ielc.libguides.com/sdzg/factsheets/plains_zebra/characteristics, read Nov 19 2026).",
]

def say(t, pause=None, shot=None):
    if shot: return [t, shot]
    if pause is not None: return {"t": t, "pause": pause}
    return t

SEGMENTS = [
  {"name": "mystery", "kind": "intro", "biome": "savanna", "tod": "morning", "word": "WHOSE FEET?",
   "show": [],
   "exhibits": [
     {"prop": "footprint", "at": [0.6, -1.6, 0.05], "on": [0, "Look"], "off": [2], "opts": {"kind": "elephant", "s": 1.4, "ground": "sand"}},
     {"prop": "footprint", "at": [-0.4, -1.9, 0.05], "on": [1, "one"], "off": [3], "times": [[1, "one"], [1, "two"], [1, "three"]],
      "opts": {"trail": ["elephant", "giraffe", "zebra"], "dx": 0.9, "s": 0.8, "ground": "sand"}},
   ],
   "lines": [
     say("Look! A giant footprint in the sand! Who made it?", pause=1.6),
     "And there are more! One, two, three mystery footprints!",
     "I'm Milo the bluebird. Let's play Guess With Milo!",
     say("Look closely, and shout out your guess. Ready? Follow the footprints!", pause=0.6),
   ]},

  {"name": "elephant", "kind": "teach", "biome": "savanna", "tod": "morning", "word": "TIPTOES!", "word_on": [3], "word_off": [5],
   "visits": [{"show": ["none"]}, {"line": 2, "show": ["elephant"]}],
   "choices": {"a": "ELEPHANT", "b": "LION", "right": "a", "ask": [1], "answer": [2], "hold": 2.4},
   "checks": [{"a": "CUSHION", "b": "WHEEL", "right": "a", "ask": [15], "answer": [16], "hold": 2.0}],
   "exhibits": [
     {"prop": "footprint", "at": [1.95, -1.3, 0.6], "on": [0, "footprint"], "off": [2], "opts": {"kind": "elephant", "s": 1.0, "ground": "sand"}},
     {"prop": "sign", "at": [1.95, -1.3, 3.3], "on": [3, "tiptoes"], "off": [4], "opts": {"text": "TIPTOES!", "color": "#3db8ff"}},
     {"prop": "magnifier", "at": [2.3, -1.1, 2.3], "on": [4, "cushion"], "off": [6], "opts": {"s": 1.0, "fill": "#c9a27a", "label": "CUSHION"}},
     {"prop": "dots", "at": "dots", "on": [5, "end"], "off": [6]},
     {"prop": "count", "at": [1.05, -1.3, 2.2], "on": [8, "One"], "off": [9], "times": [[8, "One"], [8, "two"], [8, "three"], [8, "four"], [8, "five"]],
      "opts": {"n": 5, "dx": 0.45, "s": 0.8}},
     {"prop": "rings", "at": [2.3, -1.1, 0.4], "on": [10, "rumbles"], "off": [11], "opts": {"s": 0.9}},
   ],
   "lines": [
     say("Here is the first footprint. It is big and round. Whose foot made it?", pause=0.4),
     say("Is it the elephant? Or is it the lion?", pause=3.2),
     "It is the elephant!",
     "Here is the fun fact. An elephant walks on its tiptoes!",
     "Under its toes is a soft cushion, like a squishy pillow!",
     say("Why does an elephant need a cushion? Hmm.", pause=2.4),
     "The cushion soaks up the bump when a heavy elephant steps down. Squish!",
     say("Look at those big, round feet. Step, step!", shot="close:elephant"),
     "Elephants have toenails, too! Let's count five toenails. One, two, three, four, five!",
     "Some elephants have four nails on a front foot, and some have five.",
     "Scientists think elephants may even feel tiny rumbles in the ground, with their feet!",
     "Shh. Put your hand flat on the floor. What can you feel?",
     say("Say it with me. An elephant walks on its tiptoes!", shot="close:host"),
     "Can you walk on your tiptoes, like an elephant? Tip, tip, tiptoe!",
     "Now step softly, with big cushion feet. Squish, squish!",
     say("Quick check! What is under an elephant's toes? A soft cushion? Or a wheel?", pause=3.2),
     "A soft cushion! Squish, squish. Great job!",
   ],
   "short": {"id": "zs90_elephant_tiptoes", "title": "Does an Elephant Walk on Tiptoes? Elephant Feet", "l1": "WHOSE", "l2": "FOOT?",
             "thumb_text": "SQUISHY!", "thumb_line": [4, 0.6]}},

  {"name": "giraffe", "kind": "teach", "biome": "savanna", "tod": "golden", "word": "TWO HOOVES!", "word_on": [3], "word_off": [5],
   "visits": [{"show": ["none"]}, {"line": 2, "show": ["giraffe"]}],
   "choices": {"a": "GIRAFFE", "b": "LION", "right": "a", "ask": [1], "answer": [2], "hold": 2.4},
   "checks": [{"a": "TWO", "b": "TEN", "right": "a", "ask": [15], "answer": [16], "hold": 2.0, "colors": {"a": "#22a84a", "b": "#e23b34"}}],
   "exhibits": [
     {"prop": "footprint", "at": [1.95, -1.3, 0.6], "on": [0, "footprint"], "off": [2], "opts": {"kind": "giraffe", "s": 1.0, "ground": "sand"}},
     {"prop": "count", "at": [1.05, -1.3, 2.2], "on": [3, "two"], "off": [4], "times": [[3, "two"], [3, "hooves"]], "opts": {"n": 2, "dx": 0.5, "s": 0.9}},
     {"prop": "ruler", "at": [2.3, -1.2, 1.2], "on": [4, "ruler"], "off": [5], "opts": {"s": 1.0, "label": "12 INCHES"}},
     {"prop": "dots", "at": "dots", "on": [5, "end"], "off": [6]},
     {"prop": "sign", "at": [1.95, -1.3, 3.3], "on": [6, "together"], "off": [8], "opts": {"text": "SIDE, SIDE!", "color": "#ffb627"}},
     {"prop": "sign", "at": [1.95, -1.3, 3.3], "on": [10, "hour"], "off": [11], "opts": {"text": "1 HOUR!", "color": "#3cc45a"}},
   ],
   "lines": [
     say("Here is the next footprint. It has two halves, side by side! Whose foot made it?", pause=0.4),
     say("Is it the giraffe? Or is it the lion?", pause=3.2),
     "It is the giraffe!",
     "Here is the fun fact. A giraffe has two hooves on each foot!",
     "And its feet are big! About as wide as a ruler is long.",
     say("How does a giraffe walk on such long legs? Hmm.", pause=2.4),
     "It moves the two legs on one side together. Then the two legs on the other side!",
     say("Look! This side, this side. That side, that side!", shot="close:giraffe"),
     "That keeps its front and back legs from bumping!",
     "A giraffe's legs are very long. Each leg is about as tall as a grown-up!",
     "And a baby giraffe can stand up and walk, about an hour after it is born!",
     "Wobble, wobble, up it goes!",
     say("Say it with me. A giraffe has two hooves on each foot!", shot="close:host"),
     "Can you walk like a giraffe? This side, this side. That side, that side!",
     "Now stand up tall. Stretch!",
     say("Quick check! How many hooves are on each giraffe foot? Two? Or ten?", pause=3.2),
     "Two! Two hooves on every foot. Super thinking!",
   ],
   "short": {"id": "zs90_giraffe_hooves", "title": "How Many Hooves Does a Giraffe Have? Giraffe Feet", "l1": "WHOSE", "l2": "FOOT?",
             "thumb_text": "SIDE, SIDE!", "thumb_line": [6, 0.6]}},

  {"name": "zebra", "kind": "teach", "biome": "spring_meadow", "tod": "noon", "word": "ONE TOE!", "word_on": [3], "word_off": [5],
   "visits": [{"show": ["none"]}, {"line": 2, "show": ["zebra"]}],
   "choices": {"a": "ZEBRA", "b": "ELEPHANT", "right": "a", "ask": [1], "answer": [2], "hold": 2.4},
   "checks": [{"a": "ONE", "b": "FIVE", "right": "a", "ask": [15], "answer": [16], "hold": 2.0, "colors": {"a": "#22a84a", "b": "#e23b34"}}],
   "exhibits": [
     {"prop": "footprint", "at": [1.95, -1.3, 0.6], "on": [0, "footprint"], "off": [2], "opts": {"kind": "zebra", "s": 1.0, "ground": "mud"}},
     {"prop": "count", "at": [1.05, -1.3, 2.2], "on": [4, "One"], "off": [5], "times": [[4, "One"]], "opts": {"n": 1, "s": 1.0}},
     {"prop": "dots", "at": "dots", "on": [5, "end"], "off": [6]},
     {"prop": "sign", "at": [1.95, -1.3, 3.3], "on": [6, "hoof"], "off": [8], "opts": {"text": "HOOF!", "color": "#8e5bd8"}},
     {"prop": "count", "at": [1.05, -1.3, 2.2], "on": [9, "One"], "off": [10], "times": [[9, "One"], [9, "two"], [9, "three"], [9, "four"]],
      "opts": {"n": 4, "dx": 0.5, "s": 0.8}},
     {"prop": "fingerprint", "at": [2.3, -1.1, 2.3], "on": [11, "fingerprints"], "off": [12], "opts": {"s": 0.9}},
   ],
   "lines": [
     say("Here is the last footprint. It is one smooth print. Whose foot made it?", pause=0.4),
     say("Is it the zebra? Or is it the elephant?", pause=3.2),
     "It is the zebra!",
     "Here is the fun fact. A zebra walks on just one toe, on each foot!",
     "Let's count the toes on one zebra foot. One! Just one!",
     say("So what is that hard part on the bottom? Hmm.", pause=2.4),
     "It is a hoof! The hoof covers the toe, and keeps it safe.",
     say("Look at those strong hooves. Clip, clop, clip, clop!", shot="close:zebra"),
     "A hoof keeps on growing, all the time, a little like your fingernails!",
     "Four legs, four hooves! Count with me. One, two, three, four!",
     "And every zebra has its very own stripes. No two zebras are the same!",
     "Just like your fingerprints are only yours.",
     say("Say it with me. A zebra walks on one toe!", shot="close:host"),
     "Can you trot like a zebra? Clip, clop, clip, clop!",
     "Now hold up one finger, for one zebra toe. One!",
     say("Quick check! How many toes are on each zebra foot? One? Or five?", pause=3.2),
     "One! One toe, inside one hoof. You remembered!",
   ],
   "short": {"id": "zs90_zebra_one_toe", "title": "How Many Toes Does a Zebra Have? Zebra Feet", "l1": "WHOSE", "l2": "FOOT?",
             "thumb_text": "JUST ONE!", "thumb_line": [4, 0.6]}},

  {"name": "quiz", "kind": "quiz", "biome": "beach", "tod": "noon", "word": "QUIZ TIME!",
   "lines": ["Wow! Three footprints, and three friends. Now it is quiz time!", "Get ready. Think hard!"],
   "quiz": [["Who walks on its tiptoes, on a soft cushion?", "The elephant! Yes!", "elephant"],
            ["Who has two hooves on each foot?", "The giraffe! That's right!", "giraffe"],
            ["Who walks on just one toe, on each foot?", "The zebra! You remembered!", "zebra"]]},

  {"name": "goodbye", "kind": "outro", "biome": "savanna", "tod": "sunset", "word": "BYE-BYE!",
   "exhibits": [{"prop": "footprint", "at": [-0.4, -1.9, 0.05], "on": [0], "off": [3],
                 "opts": {"trail": ["elephant", "giraffe", "zebra"], "dx": 0.9, "s": 0.8, "ground": "sand"}}],
   "lines": ["Look at our footprint trail! You guessed them all!",
             "Tiptoe like an elephant. Walk this side, that side, like a giraffe. And trot like a zebra!",
             "Look at your own feet. How many toes do you have?",
             "Thank you for guessing with me. See you at the next Guess With Milo. Bye-bye, friends!"]},
]

SPEC = {
  "id": "zool_g01", "thumb_at": ["elephant", 0, 0.5], "seed": 101,
  "title": "Whose Feet Are These? Guess With Milo",
  "card": "Whose Feet?", "thumb_text": "WHO?",
  "description": ("Whose feet are these? A giant footprint in the sand starts the mystery. Guess with Milo the bluebird, then meet "
                  "the animal: an elephant walks on its tiptoes on a soft cushion, a giraffe has two hooves on each foot and walks "
                  "this side, that side, and a zebra walks on just one toe inside each hoof.\n"
                  "An interactive guessing game for kids ages 2-6, with answer signs, thinking time, counting, actions to copy "
                  "and a quiz at the end.\n\n"
                  "WHERE THE FACTS COME FROM\nSan Diego Zoo Wildlife Alliance Library (African elephant, plains zebra, giraffe "
                  "behavior); Live Science (giraffes); PBS Nature (giraffe)."),
  "tags": ["whose feet are these", "guess the animal", "animal feet for kids", "elephant facts for kids", "giraffe facts for kids",
           "zebra facts for kids", "animal guessing game", "preschool learning", "animals for toddlers", "The Animated Zoo", "Milo"],
  "cast": ["elephant", "giraffe", "zebra"],
  "extras": [],
  "facts": FACTS,
  "segments": SEGMENTS,
  "voice": "af_heart", "speed": 0.84,
  "improves": [
    "cold open: the first shot is the mystery footprint and the first line asks the title's question; Milo's name comes after the hook (every Zoo lesson so far opened with a greeting, and every lesson retention curve loses 55-60% of viewers by 10 s)",
    "one recurring format name said in the video (Guess With Milo) so parents can find it again",
    "a guess before every animal appears: the footprint is on the board before the animal walks in",
  ],
  "version": 3,
  "draft": "growth test pilot, NOT built; see drafts/growth_test_2026-11/README.md",
}

def words(t): return len(re.findall(r"[A-Za-z0-9']+", t))
def text(l): return l if isinstance(l, str) else (l["t"] if isinstance(l, dict) else l[0])

def timeline():
    """Estimated start/end of every line (seconds) with the same pause rules teach.py applies."""
    t, out = 0.5, []
    for si, s in enumerate(SEGMENTS):
        if si: t += SEG_GAP
        lines = list(s["lines"])
        for i, l in enumerate(lines):
            tx = text(l); d = max(1.2, words(tx) / WPS)
            out.append((s["name"], i, round(t, 1), round(t + d, 1), tx, l))
            t += d
            if isinstance(l, dict) and l.get("pause", 0) >= 3: t += ASK_WAIT          # answer signs + thinking time
            elif tx.endswith("Hmm."): t += THINK_WAIT
            elif re.match(r"(Can you|Now |Shh)", tx): t += DO_WAIT                   # time to do the action
            else: t += GAP
        if s["kind"] == "quiz":
            for q, a, _ in s["quiz"]:
                d = words(q) / WPS; out.append((s["name"], "Q", round(t, 1), round(t + d, 1), q, None)); t += d + ASK_WAIT
                d = words(a) / WPS; out.append((s["name"], "A", round(t, 1), round(t + d, 1), a, None)); t += d + GAP
    return out, t

def mmss(x): return f"{int(x // 60)}:{int(x % 60):02d}"

CUES = {  # music and sound cues per line (music: the 3D lessons' bed at 96 BPM, lowered under the voice as today)
  ("mystery", 0): "MUSIC: lesson bed starts on the downbeat at 0:00, already ducked under the voice (no music-only intro). "
                  "SFX: one soft sand 'pff' as the print appears, BEFORE Milo speaks (never on top of a word).",
  ("mystery", 1): "SFX none. Three prints pop in on 'one', 'two', 'three' (sparkle pop already used by count props).",
  ("mystery", 2): "MUSIC: small lift (bells) on 'Guess With Milo' as the WHOSE FEET? word appears.",
  ("quiz", 0): "MUSIC: quiz bed (as in zool_ep16).",
  ("goodbye", 3): "MUSIC: bed resolves on the tonic and fades over 2 s after the last word; closing picture holds 3 s.",
}

def write_script(rows, total):
    L = ["# Whose Feet Are These? Guess With Milo (zool_g01), timed script DRAFT", "",
         f"Estimated length **{mmss(total)}** ({total:.0f} s). The Zoo's 3D lessons run 5:34-5:47 (zool_ep12/13/16), so this fits the current format.",
         "Times are ESTIMATES from the measured pace of zool_ep12/13/16 (3.09 words/s, 0.75 s between lines, 4.0 s of thinking time after an "
         "answer-sign question, 3.1 s after a 'Hmm.' line, 3.3 s to do an action). teach.py sets the exact times when the lesson is built.", "",
         "Voice: Milo (af_heart, speed 0.84, the current lesson voice), speaking only. Music: the existing 96 BPM lesson bed under the voice. "
         "No sound effect is ever laid over a spoken word. PAUSE = the child answers out loud.", "",
         "| Time | Part | Line (Milo) | Pause / cue |", "|---|---|---|---|"]
    seg_start = {}
    for name, i, a, b, tx, l in rows:
        seg_start.setdefault(name, a)
        cue = []
        if isinstance(l, dict) and l.get("pause", 0) >= 3: cue.append("PAUSE ~4 s: answer signs on screen, child shouts a guess; correct sign lights up on the next line")
        elif tx.endswith("Hmm."): cue.append("PAUSE ~3 s thinking time (dots on the board)")
        elif re.match(r"(Can you|Now |Shh)", tx): cue.append("PAUSE ~3 s: child does the action with Milo")
        if i == "Q": cue.append("PAUSE ~4 s: quiz answer signs")
        if (name, i) in CUES: cue.append(CUES[(name, i)])
        L.append(f"| {mmss(a)} | {name} | {tx} | {'; '.join(cue)} |")
    L += ["", "## Part lengths (estimated)", ""]
    names = [s["name"] for s in SEGMENTS]
    for k, n in enumerate(names):
        end = seg_start[names[k + 1]] if k + 1 < len(names) else total
        L.append(f"- {n}: {mmss(seg_start[n])} to {mmss(end)} ({end - seg_start[n]:.0f} s)")
    L += ["", "The three animal parts are each cut whole into one 9:16 Short (part + 3 s hook = 85-95 s target); teach.py's measured parts "
          "run 86-93 s, so check the real part lengths after the build and trim or add one line if a part falls outside 83-90 s."]
    open(os.path.join(HERE, "script.md"), "w").write("\n".join(L) + "\n")

if __name__ == "__main__":
    json.dump(SPEC, open(os.path.join(HERE, "zool_g01.json"), "w"), indent=1, ensure_ascii=False)
    rows, total = timeline()
    write_script(rows, total)
    print(f"zool_g01.json + script.md written; estimated {mmss(total)} ({total:.0f} s), {sum(len(s['lines']) for s in SEGMENTS)} lines")
