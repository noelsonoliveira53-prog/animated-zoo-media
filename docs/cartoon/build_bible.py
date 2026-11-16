"""Builds bible.html: the story world, the cast and the cartoon style bible (Nov 16 2026).
The character sheets and the places are drawn by studio/cartoon/bible.py from the same rigs the films use; the example frames are cut from the finished test files.

    python3 build_bible.py <dir with the sheet PNGs and frame JPGs>
"""
import os, sys, base64, io
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = sys.argv[1]; KEEP = os.path.join(HERE, "bible"); os.makedirs(KEEP, exist_ok=True)


def img(name, w, q=82):
    """Scale to width w, keep a copy in docs/cartoon/bible/, return a data URI."""
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    out = os.path.join(KEEP, os.path.splitext(name)[0] + ".jpg"); im.save(out, quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(open(out, "rb").read()).decode()


CAST = [
 ("Milo", "bluebird, the host", "Curious, kind, a little too quick to fly ahead.", "Warm storyteller. He tells every story and speaks his own lines.", "Let's find out together!", "To wait and listen before he flies off.", "in both test videos"),
 ("Tumble", "baby elephant, he", "Big-hearted and eager. Clumsy when he hurries.", "A small boy's voice, bright and a bit breathless.", "Trunks up!", "To keep trying when a plan goes wrong.", "in the test adventure"),
 ("Mango", "spider monkey, she", "Quick, funny, generous. Always moving.", "Fast and playful, a smile in every line.", "Swing-a-ding!", "To slow down and wait for her friends.", "in the test adventure"),
 ("Sandy", "baby camel, she", "Calm, patient, steady. Never in a rush.", "Soft and gentle.", "Step, step, step!", "To be brave when Mama is not beside her.", "in both test videos"),
 ("Poppy", "polar bear cub, she", "Shy and cuddly. Watches first, then joins in.", "Not chosen yet.", "Brrr-illiant!", "To try new things.", "drawn, not yet in a video"),
 ("Tula", "green sea turtle, she", "Gentle and thoughtful. The slowest and the surest.", "Not chosen yet.", "Slow and steady!", "To ask for help.", "drawn, not yet in a video"),
 ("Clover", "lamb, he", "Friendly, loves to share. Sometimes too quiet to be heard.", "Not chosen yet.", "Me too!", "To speak up.", "drawn, not yet in a video"),
 ("Hazel", "hedgehog, she", "A careful thinker who loves the night.", "Not chosen yet.", "Let me think!", "That small can be brave.", "drawn, not yet in a video"),
]
PAL = [("Ink", "#402010", "every word outline, pills, props"), ("Sun", "#ffd23f", "spoken word, pills, highlights"), ("Milo blue", "#2f80ed", "Milo, the gate, answer sign A"), ("Milo deep", "#1c5fc4", "Milo's wings and shade"),
       ("Scarf red", "#e63946", "Milo's scarf"), ("Beak", "#ff9f1c", "beak and feet"), ("Coral", "#ff7a59", "answer sign B"), ("Cheek", "#ff8fb1", "every cheek"),
       ("Camel", "#dba56a", "Sandy and Mama"), ("Camel line", "#7d4a22", "camel outline"), ("Elephant", "#a9bdd0", "Tumble and Mama"), ("Elephant line", "#3d5068", "elephant outline"),
       ("Monkey", "#9c6b45", "Mango"), ("Face cream", "#f7dcbc", "Mango's face, Hazel"), ("Paper", "#fff6e0", "picture board"), ("Paper blue", "#e6f4ff", "picture board"), ("Paper pink", "#ffeef2", "picture board"), ("Sky", "#7fd0ff", "day sky, top")]
cast_rows = "".join(f'<tr><td><b>{n}</b><br><span class="src">{a}</span></td><td>{p}</td><td>{v}</td><td>"{c}"</td><td>{l}</td><td>{s}</td></tr>' for n, a, p, v, c, l, s in CAST)
pal = "".join(f'<div class="sw"><span style="background:{h}"></span><b>{n}</b><code>{h}</code><small>{u}</small></div>' for n, h, u in PAL)
I = {k: img(f, w) for k, f, w in (("milo", "milo_sheet.png", 1500), ("tumble", "tumble_sheet.png", 1700), ("mama", "mama_elephant_sheet.png", 1700), ("mango", "mango_sheet.png", 1500), ("camel", "camel_sheet.png", 1700),
                                  ("friends", "friends_sheet.png", 1700), ("places", "places.png", 1900), ("f_words", "frame_words.jpg", 1280), ("f_signs", "frame_signs.jpg", 1280), ("f_board", "frame_board.jpg", 1280),
                                  ("f_story", "frame_story.jpg", 1280), ("f_short", "frame_short.jpg", 640), ("f_wm", "frame_wm.jpg", 900))}
CSS = open(os.path.join(HERE, "plan.css")).read() + """
figure { margin:0; display:flex; flex-direction:column; gap:6px; min-width:0 } figure img { display:block; width:100%; height:auto; border-radius:12px; border:1px solid var(--line) } figcaption { font-size:13.5px; color:var(--mut) }
.pal { display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:10px } .sw { display:flex; flex-direction:column; gap:1px; font-size:13px; min-width:0 }
.sw span { display:block; height:46px; border-radius:10px; border:1px solid var(--line) } .sw code { font-size:12.5px; color:var(--mut) } .sw small { color:var(--mut); line-height:1.3 }
.frames { display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:14px; align-items:start } .tallf { display:grid; grid-template-columns:minmax(0,260px) 1fr; gap:18px; align-items:start }
@media (max-width:640px) { .tallf { grid-template-columns:1fr } }
"""
page = f'''<title>Zoo Style Bible</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&family=Nunito:wght@400;600;800&display=swap">
<style>{CSS}</style>
<main>
<header>
  <p class="eyebrow">The Animated Zoo · written Nov 16, 2026</p>
  <h1>The story world and the cartoon style</h1>
  <p class="lead" style="margin-top:10px">Who lives in the zoo, where the adventures go, and how every cartoon video is drawn. Every picture on this page comes from the same drawing code the videos use, so a character cannot look different in a video than it does here.</p>
</header>

<section>
  <h2>The cast</h2>
  <div class="tw"><table>
    <thead><tr><th>Friend</th><th>Personality</th><th>Voice</th><th>Catchphrase</th><th>Is learning</th><th>Status</th></tr></thead>
    <tbody>{cast_rows}</tbody></table></div>
  <p class="src">Grown-ups: Mama Elephant (warm, slow, kind) and Sandy's Mama. The voices are made by the studio's own voice engine. I checked that every word can be placed from the audio; I cannot listen, so how the voices sound to the ear is for you to judge in the test adventure.</p>
</section>

<section>
  <h2>The world</h2>
  <p>The zoo gate is home. Every adventure starts and ends there. From the gate the friends go out to one place and come back before the sun goes down.</p>
  <figure><img src="{I["places"]}" alt="Twenty-one backgrounds: the zoo gate by day and at sunset, savanna, river, jungle, the tallest tree, the treetops, five desert places, the snowy Gobi, ocean, Arctic, farm, night forest and three picture boards."><figcaption>All places drawn so far. The jungle, savanna, river, treetops, desert and both zoo gates are used in the test videos. Ocean, Arctic, farm and night forest are drawn and not yet used.</figcaption></figure>
  <div class="grid">
    <div class="spec"><h4>Same every time</h4><ul><li>The hook, then Milo: "I'm Milo! Come on a big adventure with us!"</li><li>The refrain on the way out and on the way home: "Friends help friends, come along with me!"</li><li>The ending song line: "Friends help friends, hooray, hooray! What a big adventure day!"</li><li>Milo's goodbye: "See you on the next adventure, friends!"</li></ul></div>
    <div class="spec"><h4>New every time</h4><ul><li>One place and one friend who lives there.</li><li>One problem a small child knows: a present, a shy feeling, something too high, too far, too hot.</li><li>Two or three true things about the animals, each one used to solve the problem.</li></ul></div>
    <div class="spec"><h4>Always true of the world</h4><ul><li>Kindness, courage, friendship, curiosity.</li><li>No villains and no danger. Nobody is hurt, lost, crying or trapped.</li><li>The night forest is cosy and bright enough to see every face.</li><li>The friends solve the problem themselves.</li></ul></div>
  </div>
</section>

<section>
  <h2>Character sheets</h2>
  <figure><img src="{I["milo"]}" alt="Milo the bluebird in eight poses: rest, talking, asking, blink, flying with wings up and down, squash and stretch."><figcaption>Milo. Round body, a crest of three feathers, big brown eyes, orange beak, pale belly, red scarf.</figcaption></figure>
  <figure><img src="{I["tumble"]}" alt="Tumble the baby elephant in eight poses: rest, talking, worried, surprised, blink, trunks up, trunk as a snorkel, walking."><figcaption>Tumble. Big head, short trunk, a tuft of hair, no tusks. Worried is a tilted brow, a small frown, ears and head down. Nobody cries.</figcaption></figure>
  <figure><img src="{I["mama"]}" alt="Mama Elephant in four poses: rest, talking, trunk hug, with a birthday hat."><figcaption>Mama Elephant. Long trunk, small tusks, eyelashes.</figcaption></figure>
  <figure><img src="{I["mango"]}" alt="Mango the spider monkey in eight poses: rest, talking, worried, hooray, blink, hanging by her tail, reaching, talking upside down."><figcaption>Mango. Long thin arms and legs, and a tail that holds on like an extra hand.</figcaption></figure>
  <figure><img src="{I["camel"]}" alt="Sandy the camel calf, her Mama and a two-humped cousin in twelve poses."><figcaption>Sandy, her Mama and the Bactrian cousin. A calf has a tuft of curly hair where the hump will grow.</figcaption></figure>
  <figure><img src="{I["friends"]}" alt="Poppy the polar bear cub, Clover the lamb, Hazel the hedgehog and Tula the sea turtle, two poses each."><figcaption>Poppy, Clover, Hazel and Tula. First drawings: they can blink, talk, look worried and walk, and they have not been in a video yet.</figcaption></figure>
</section>

<section>
  <h2>Line, shape and shading</h2>
  <div class="grid">
    <div class="spec"><h4>Shape</h4><ul><li>Everything is built from round shapes. No sharp corners on a character.</li><li>Babies have a big head and big eyes for their body.</li><li>Eyes: a white circle, a brown iris, a dark pupil, two white sparkles. The same eye on every animal.</li><li>A pink cheek on every face.</li></ul></div>
    <div class="spec"><h4>Line</h4><ul><li>One outline round the whole silhouette, 9 units wide, in a dark shade of the animal's own colour. Never black.</li><li>Every part that moves carries its own outline, so a head that turns or a trunk that lifts takes its line with it.</li><li>No outlines on backgrounds: the characters stand out because only they have a line.</li></ul></div>
    <div class="spec"><h4>Shading</h4><ul><li>Flat colour. One soft highlight on top, one darker crescent under the belly, a soft shadow on the ground.</li><li>No gradients on characters. Skies are the only gradient.</li><li>Legs on the far side are one step darker.</li></ul></div>
  </div>
  <h3>Colours</h3>
  <div class="pal">{pal}</div>
</section>

<section>
  <h2>Words on screen</h2>
  <div class="frames">
    <figure><img src="{I["f_words"]}" alt="A frame of the camel lesson with a name on a yellow pill and the caption below."><figcaption>A name or a label sits on a yellow pill, tilted a little. The caption is at the bottom; each word turns yellow as it is spoken.</figcaption></figure>
    <figure><img src="{I["f_signs"]}" alt="A frame of the camel lesson with two answer signs and three thinking dots."><figcaption>A question: two answer signs, blue and coral, three dots that fill while the child thinks, then a green tick on the right answer.</figcaption></figure>
    <figure><img src="{I["f_board"]}" alt="A picture board frame from the camel lesson."><figcaption>A fact gets a picture board: paper with a soft grid, the example in the middle, the key word big and yellow.</figcaption></figure>
    <figure><img src="{I["f_story"]}" alt="A frame from the test adventure."><figcaption>In a story the same words are used more sparingly: a name, a sound, a feeling.</figcaption></figure>
  </div>
  <ul class="list">
    <li><b>One typeface:</b> Baloo 2, extra bold, for every word in the picture.</li>
    <li><b>Three word styles:</b> white with a dark outline; sun yellow with a dark outline for the key word; dark on a yellow pill for names and labels.</li>
    <li><b>Words never cover a face,</b> never touch the watermark, never sit on the caption, and are never cut by the frame.</li>
    <li><b>A word appears on the spoken word,</b> placed from the audio.</li>
  </ul>
</section>

<section>
  <h2>Camera and transitions</h2>
  <ul class="list">
    <li><b>Cut</b> between shots in the same place. Every shot drifts a little, in or out, so the picture is never frozen.</li>
    <li><b>Iris</b> (a yellow circle with a blue ring that opens and closes, with a soft whoosh) only when the place changes.</li>
    <li><b>Close-ups</b> show a face, a detail, or a part of the body the line is about. A second character is either whole in the picture or not in it.</li>
    <li><b>The tall version</b> of a shot has its own camera, its own word positions and, where needed, its own prop positions.</li>
  </ul>
</section>

<section>
  <h2>Watermark</h2>
  <div class="tallf">
    <figure><img src="{I["f_short"]}" alt="A frame of the camel Short: the watermark at the top centre, the title band below it, the picture, the caption."><figcaption>9:16: the mark sits top centre, above the title band.</figcaption></figure>
    <div style="display:flex;flex-direction:column;gap:12px;min-width:0">
      <figure><img src="{I["f_wm"]}" alt="The top left corner of a 16:9 frame with the watermark."><figcaption>16:9: Milo's channel picture and "The Animated Zoo", top left.</figcaption></figure>
      <ul class="list"><li>It is drawn into the video, because YouTube's own watermark button is not available on videos made for kids.</li><li>Nothing that matters sits under it: no face, no word, no answer sign.</li><li>Thumbnails carry no mark.</li></ul>
    </div>
  </div>
</section>
</main>
'''
open(os.path.join(HERE, "bible.html"), "w").write(page); print("bible.html", len(page) // 1024, "KB")
