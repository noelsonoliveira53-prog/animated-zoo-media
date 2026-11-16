"""Builds findings.html (Step 1 of the cartoon move, Nov 16 2026) from docs/analysis/*.json. Every number comes from those files."""
import json, base64, os
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis")
ch = json.load(open(os.path.join(A, "channel_2026-11-16.json"))); pace = json.load(open(os.path.join(A, "pace_2026-11-16.json")))
S = "/tmp/claude-0/-home-claude/ef203c51-db22-5edb-be31-9f6eb9bbdf6d/scratchpad/page/"
img = lambda n: "data:image/jpeg;base64," + base64.b64encode(open(S + n, "rb").read()).decode()
K = ch["by_kind"]; rows = ch["rows"]
KIND = [("cartoon_fact_short", "Cartoon fact Shorts", 1), ("song_3d", "3D songs", 2), ("cartoon_explainer", "Cartoon explainers (old)", 3), ("song_cut_short", "Shorts cut from songs", 4), ("explainer_3d", "3D explainers", 5)]
def rng(kind, key, fmt):
    v = [r[key] for r in rows if r["kind"] == kind and r[key] is not None and (r["views"] or 0) >= 20]
    return f"{fmt(min(v))} to {fmt(max(v))}" if v else "too few views"
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
kind_rows = ""
for k, name, slot in KIND:
    a = K[k]
    kind_rows += (f'<tr><td><span class="sw s{slot}"></span>{name}</td><td class="n">{a["videos"]}</td><td class="n">{a["views"]:,}</td><td class="n">{a["median_views"]:,}</td>'
                  f'<td class="n">{a["impressions"]:,}</td><td class="n">{a["ctr"] if a["ctr"] is not None else "-"}%</td><td class="n">{rng(k, "avg_view_s", mmss)}</td><td class="n">{rng(k, "pct_viewed", lambda x: f"{x:.0f}%")}</td></tr>')
views_data = [{"name": n, "v": K[k]["views"], "slot": s, "note": f'{K[k]["videos"]} videos, median {K[k]["median_views"]:,} views each'} for k, n, s in KIND]
P = [("zoo3d_ep04", "Where Is My Mama? (3D song, 2:50)", 2), ("s_camel", "Camel Humps (cartoon Short, 0:28)", 1), ("zool_ep08", "Who Am I? (3D explainer, 5:33)", 5), ("zool_ep09", "Animal Champions (3D explainer, 5:37)", 5),
     ("zs90_zebra_stripes", "Zebra stripes (Short cut from a 3D explainer, 1:28)", 5), ("ep02_ocean_ice", "Ocean & Ice (old cartoon explainer, 5:10)", 3), ("ep04_amazing_bodies", "Amazing Animal Bodies (old cartoon explainer, 4:58)", 3)]
pace_data = [{"name": n, "v": round(pace[k]["summary"]["share_in_long"] * 100), "slot": s,
              "note": f'{pace[k]["summary"]["over_max"]} stretches over 8 s, longest {pace[k]["summary"]["longest_gap"]:.0f} s; a change every {pace[k]["summary"]["mean_gap"]:.1f} s on average'} for k, n, s in P]
pace_rows = "".join(f'<tr><td><span class="sw s{s}"></span>{n}</td><td class="n">{pace[k]["summary"]["mean_gap"]:.1f} s</td><td class="n">{pace[k]["summary"]["over_max"]}</td>'
                    f'<td class="n">{pace[k]["summary"]["share_in_long"] * 100:.0f}%</td><td class="n">{pace[k]["summary"]["longest_gap"]:.0f} s</td><td class="n">{pace[k]["summary"]["shot_longest"]:.0f} s</td></tr>' for k, n, s in P)
def stretches(k): return ", ".join(f"{mmss(a)}–{mmss(b)}" for a, b, d in pace[k]["summary"]["long"])
top = sorted(rows, key=lambda r: -(r["views"] or 0))[:10]
top_rows = "".join(f'<tr><td>{r["title"]}</td><td class="n">{r["views"]:,}</td><td class="n">{r["pct_viewed"]:.0f}%</td></tr>' for r in top)
html = f'''<title>Zoo Channel Findings</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&family=Nunito:wght@400;600;800&display=swap">
<style>
/* layout: one reading column (max 980px); numbers in tables, two bar charts, three evidence frames; rules as a numbered list because their order is the order of a video */
:root {{ --bg:#f6f9fd; --card:#ffffff; --fg:#14213d; --mut:#55617a; --line:#d9e2ef; --accent:#1f6fd6; --sun:#ffd23f; --ink:#402010;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --s5:#e87ba4; --disp:"Baloo 2","Nunito",system-ui,sans-serif; --body:"Nunito",system-ui,-apple-system,"Segoe UI",sans-serif }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#0f1626; --card:#172036; --fg:#eef3fb; --mut:#aab6cc; --line:#2a3653; --accent:#6aa8ff; --sun:#ffd23f; --ink:#f3e7dc;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --bg:#0f1626; --card:#172036; --fg:#eef3fb; --mut:#aab6cc; --line:#2a3653; --accent:#6aa8ff; --sun:#ffd23f; --ink:#f3e7dc;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181; color-scheme: dark }}
body {{ background:var(--bg); color:var(--fg); font:16px/1.55 var(--body); padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); padding-block:28px 56px }}
main {{ max-width:980px; margin:0 auto; display:flex; flex-direction:column; gap:34px }}
h1 {{ font:800 clamp(30px,5vw,44px)/1.05 var(--disp); margin:0; text-wrap:balance }}
h2 {{ font:800 26px/1.15 var(--disp); margin:0 0 10px; text-wrap:balance }}
h3 {{ font:800 18px/1.2 var(--disp); margin:0 0 6px }}
p {{ margin:0 0 10px; max-width:68ch }} .lead {{ font-size:18px; color:var(--mut) }}
.src {{ font-size:13px; color:var(--mut) }}
section {{ display:flex; flex-direction:column; gap:12px; min-width:0 }}
.tw {{ overflow-x:auto; border:1px solid var(--line); border-radius:10px; background:var(--card) }}
table {{ border-collapse:collapse; width:100%; font-size:14.5px; font-variant-numeric:tabular-nums }}
th,td {{ padding:8px 12px; text-align:left; border-bottom:1px solid var(--line); vertical-align:top }} tr:last-child td {{ border-bottom:0 }}
th {{ font-weight:800; font-size:12.5px; letter-spacing:.04em; text-transform:uppercase; color:var(--mut) }} .n {{ text-align:right; white-space:nowrap }}
.sw {{ display:inline-block; width:11px; height:11px; border-radius:3px; margin-right:8px; vertical-align:-1px }}
.s1{{background:var(--s1)}} .s2{{background:var(--s2)}} .s3{{background:var(--s3)}} .s4{{background:var(--s4)}} .s5{{background:var(--s5)}}
.chart {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:16px 16px 10px; position:relative }}
.chart h3 {{ margin-bottom:10px }} .bar-row {{ display:grid; grid-template-columns:minmax(120px,300px) 1fr; gap:10px; align-items:center; padding:4px 0; border-radius:6px }}
.bar-row:hover, .bar-row:focus {{ background:color-mix(in srgb, var(--accent) 9%, transparent); outline:none }}
.bar-name {{ font-size:14px; line-height:1.25 }} .bar-track {{ display:flex; align-items:center; gap:8px; min-width:0 }}
.bar {{ height:16px; border-radius:0 4px 4px 0; min-width:2px }} .bar-val {{ font-weight:800; font-size:14px; font-variant-numeric:tabular-nums; white-space:nowrap }}
.tip {{ position:absolute; pointer-events:none; background:var(--fg); color:var(--bg); font-size:13px; padding:6px 9px; border-radius:6px; max-width:300px; z-index:5 }}
.two {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(290px,1fr)); gap:18px }}
.win {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:16px; display:flex; flex-direction:column; gap:8px; min-width:0 }}
.win img {{ border-radius:8px; align-self:flex-start; max-height:230px }}
ul {{ margin:0; padding-left:20px; max-width:68ch }} li {{ margin-bottom:5px }}
.rules {{ counter-reset:r; list-style:none; padding:0; display:flex; flex-direction:column; gap:12px; max-width:none }}
.rules li {{ counter-increment:r; background:var(--card); border:1px solid var(--line); border-radius:12px; padding:14px 16px 14px 62px; position:relative; margin:0 }}
.rules li::before {{ content:counter(r); position:absolute; left:14px; top:12px; width:34px; height:34px; border-radius:50%; background:var(--sun); color:#402010; font:800 20px/34px var(--disp); text-align:center }}
.rules b {{ font:800 18px/1.25 var(--disp); display:block }} .rules span {{ color:var(--mut); font-size:14.5px }}
.note {{ border-left:4px solid var(--sun); padding:8px 14px; background:var(--card); border-radius:0 8px 8px 0; max-width:72ch }}
figure {{ margin:0; display:flex; flex-direction:column; gap:6px }} figcaption {{ font-size:13px; color:var(--mut); max-width:60ch }}
</style>
<main>
<header><h1>What won on The Animated Zoo, and the five rules for the cartoon videos</h1>
<p class="lead">Read from YouTube Studio on Nov 16, 2026 at 12:15 PM ET (lifetime numbers) and from the video files themselves. The channel has 32,766 views; 72% of them came from Shorts.</p></header>

<section><h2>Views by kind of video</h2>
<div class="chart" id="c1"><h3>Lifetime views</h3><div class="bars"></div></div>
<div class="tw"><table><thead><tr><th>Kind</th><th class="n">Videos</th><th class="n">Views</th><th class="n">Median views</th><th class="n">Thumbnail impressions</th><th class="n">Click rate</th><th class="n">Average view</th><th class="n">Share watched</th></tr></thead><tbody>{kind_rows}</tbody></table></div>
<p class="src">Average view and share watched are the lowest and highest video of each kind (videos with 20 views or more). Four older uploads from before the Milo format (82 views) are left out.</p>
<div class="note"><b>The 3D explainers cannot be judged from data yet.</b> Two are public, both since Nov 15, with 8 views and 26 impressions between them. What the data does show: the old cartoon explainers have a median of {K["cartoon_explainer"]["median_views"]} views each, the 3D songs a median of {K["song_3d"]["median_views"]}.</div>
<div class="tw"><table><thead><tr><th>Top 10 videos</th><th class="n">Views</th><th class="n">Share watched</th></tr></thead><tbody>{top_rows}</tbody></table></div>
<p class="src">Eight of the top ten are cartoon Shorts built on one surprising fact. The other two are 3D songs.</p></section>

<section><h2>The two winners</h2><div class="two">
<div class="win"><h3>Where Is My Mama? (3D song)</h3><img src="{img("mama.jpg")}" alt="Thumbnail: Milo with the lion, giraffe and zebra, the words WHERE IS MY MAMA?">
<p>3,882 views. It won on reach: YouTube showed its thumbnail 120,313 times, and 93% of its views came from Suggested videos. No other video on the channel has more than 34,632 impressions.</p>
<ul><li><b>Hook:</b> the title is a child's question, and the first sung line repeats it.</li><li><b>Story:</b> baby animals look for their mamas with Milo; each verse ends with a find ("There she is!"), the song ends on "Mama is found!".</li>
<li><b>Emotion:</b> a baby, a mama, a happy reunion. Nobody is lost or sad on screen.</li><li><b>Pacing:</b> the picture changes every 1.1 seconds on average; the longest it holds still is 7 seconds.</li>
<li><b>Thumbnail:</b> Milo's face fills the middle, three friends around him, the question in big yellow letters.</li></ul>
<p class="src">Its watch time is ordinary: 0:28 average, 16.6% watched, the same as the other 3D songs (12–22%). Click rate 2.9%. 46% of its views came from India. Why YouTube suggested this one so widely is not something Studio shows; the title and topic are what set it apart from the other songs.</p></div>
<div class="win"><h3>Camel Humps Are Full of Fat, Not Water! (cartoon Short)</h3><img src="{img("camel.jpg")}" alt="First frame of the camel Short: the camel, its name, the question caption">
<p>4,913 views, the most on the channel. 94% came from the Shorts feed. 64.6% of the people who saw it stayed to watch, and it was watched 72.6% through.</p>
<ul><li><b>Hook:</b> the animal is on screen in the first frame and Milo asks "What do you think is inside a camel's hump? Is it water?" in the first 3 seconds.</li>
<li><b>Payoff:</b> the answer lands at 0:09 with a label on the hump ("FAT, NOT WATER!").</li><li><b>Story:</b> one animal, one myth turned over, two small extra facts, then "Can you blink your eyes like a camel?"</li>
<li><b>Pacing:</b> one location, but something new appears every 3.5 seconds (a question mark, Milo, the label, a zoom).</li><li><b>Title:</b> the surprising fact itself, 39 characters.</li></ul>
<p class="src">Published Nov 7. Almost all of its views came after Nov 9 (3,206 by Nov 13, 4,538 by Nov 14). 33% of its views came from the Philippines, 14% India, 13% United States.</p></div></div></section>

<section><h2>Where the picture stands still</h2>
<p>I measured each video four times a second: a visual change is a cut, a camera move, or something new that appears and stays (a sign, a word, a diagram). A character bobbing or waving in place does not count.</p>
<div class="chart" id="c2"><h3>Share of the video spent in stretches longer than 8 seconds with no visual change</h3><div class="bars"></div></div>
<div class="tw"><table><thead><tr><th>Video</th><th class="n">A change every</th><th class="n">Stretches over 8 s</th><th class="n">Share of the video</th><th class="n">Longest stretch</th><th class="n">Longest single shot</th></tr></thead><tbody>{pace_rows}</tbody></table></div>
<div class="two"><div><h3>Who Am I? (Nov 15)</h3><p class="src">Stretches over 8 seconds with no visual change: {stretches("zool_ep08")}.</p></div>
<div><h3>Animal Champions (Nov 16)</h3><p class="src">Stretches over 8 seconds with no visual change: {stretches("zool_ep09")}.</p></div></div>
<div class="two"><figure><img src="{img("spots.jpg")}" alt="Animal Champions at 4:03: Milo and the lion, caption about lion cubs born with spots, no spots shown"><figcaption>Animal Champions at 4:03. The voice says "Lion cubs are born with spots!" The picture is the same two characters it has been since 3:56; no cub and no spots are shown.</figcaption></figure>
<figure><img src="{img("old.jpg")}" alt="Old cartoon explainer: one animal in the middle of one background"><figcaption>The old cartoon explainers hold one shot per animal for up to 56 seconds. They hold a single shot longer than any other video measured. They also have the longest average views among the long videos with 20 views or more (0:44 for Ocean & Ice).</figcaption></figure></div>
<div class="note"><b>Going back to cartoon does not fix the stillness by itself.</b> The old cartoon explainers sit in long still stretches for about half of their length, the same as the 3D explainers. The fix is the shot plan: the winning song changes its picture three times as often as the 3D explainers and five times as often as the old cartoon ones.</div></section>

<section><h2>The five rules for every new cartoon video</h2>
<ol class="rules">
<li><b>Start with a question a child wants answered, with the animal already on screen.</b><span>Explainers ask it in the first 5 seconds; Shorts answer it by 0:10. Ask the viewer something again about every 45 seconds, and end with a recap. (Camel: question at 0:00, answer at 0:09.)</span></li>
<li><b>One true, surprising fact carries the video, and the title says it.</b><span>Eight of the top ten videos are one surprising fact ("Camel Humps Are Full of Fat, Not Water!", "An Octopus Has 3 Hearts!"). Every fact is read at its source the day the script is written.</span></li>
<li><b>Tell it as a small story with a baby and its mama.</b><span>A want, a search with Milo, a happy find. Nobody lost, hurt, scared or crying. (Where Is My Mama? is the only long video YouTube suggested widely.)</span></li>
<li><b>Change the picture every 4 to 6 seconds, never longer than 8.</b><span>A new place, a camera move, a close-up, a cutaway, a diagram, a comparison or an on-screen word. At least 6 places per explainer; a change every 2 to 3 seconds in a Short. The pace check rejects any stretch over 8 seconds.</span></li>
<li><b>Show the fact, not the speaker.</b><span>Every fact line gets its own picture of exactly that thing, in sync with the words. (At 4:03 of Animal Champions the spots are spoken and never shown.)</span></li>
</ol></section>

<section><h2>How the five rules read in each pillar</h2>
<p>Added the same day, after the channel grew to three pillars: music, stories and adventures, animal facts.</p>
<div class="tw"><table><thead><tr><th>Rule</th><th>Music (3D)</th><th>Stories and adventures (cartoon)</th><th>Animal facts (cartoon)</th></tr></thead><tbody>
<tr><td>1. Open on what the child wants to know</td><td>The first line of the song is the character's wish.</td><td>The problem and the feeling in the first 5 seconds ("Tumble has no present!").</td><td>The question in the first 5 seconds, the animal on screen.</td></tr>
<tr><td>2. One true surprise</td><td>One fact in the chorus is enough.</td><td>2 or 3 true facts, and each one solves a problem in the plot.</td><td>One fact carries the lesson and the title says it.</td></tr>
<tr><td>3. A baby, a mama or a friend, and a feeling</td><td>One character, one feeling, a small journey.</td><td>A goal, three obstacles, a low moment, an answer the friends find, a warm ending.</td><td>A baby animal goes to find out with Milo.</td></tr>
<tr><td>4. Keep the picture changing</td><td>Already does: a change every 1.1 s in the winner.</td><td>Something new every 4 to 6 seconds, at least 6 places.</td><td>Something new every 4 to 6 seconds, at least 6 places; every 2 to 3 seconds in a Short.</td></tr>
<tr><td>5. Show it</td><td>The pictures follow the words of the song.</td><td>Faces act the feeling; each fact gets a picture board.</td><td>Every fact line has its own picture.</td></tr>
</tbody></table></div></section>
<p class="src">Not measured: per-second retention curves (Studio shows them as a chart only), and anything about viewers' ages. Data files: docs/analysis in the repo. Pace check: studio/cartoon/pace_check.py.</p>
</main>
<script>
const D1 = {json.dumps(views_data)}, D2 = {json.dumps(pace_data)};
function bars(id, data, unit, max) {{
  const root = document.querySelector('#' + id), box = root.querySelector('.bars'); const m = max || Math.max(...data.map(d => d.v));
  const tip = document.createElement('div'); tip.className = 'tip'; tip.hidden = true; root.appendChild(tip);
  data.forEach(d => {{
    const row = document.createElement('div'); row.className = 'bar-row'; row.tabIndex = 0;
    row.innerHTML = `<div class="bar-name">${{d.name}}</div><div class="bar-track"><div class="bar s${{d.slot}}" style="width:${{Math.max(0.4, d.v / m * 82)}}%"></div><div class="bar-val">${{d.v.toLocaleString()}}${{unit}}</div></div>`;
    const show = e => {{ tip.textContent = d.name + ': ' + d.v.toLocaleString() + unit + '. ' + d.note; tip.hidden = false; const r = root.getBoundingClientRect(), b = row.getBoundingClientRect(); tip.style.left = Math.min(r.width - 310, Math.max(8, (e.clientX || b.left + 140) - r.left)) + 'px'; tip.style.top = (b.bottom - r.top + 4) + 'px'; }};
    row.addEventListener('mousemove', show); row.addEventListener('focus', show); row.addEventListener('mouseleave', () => tip.hidden = true); row.addEventListener('blur', () => tip.hidden = true);
    box.appendChild(row);
  }});
}}
bars('c1', D1, '', null); bars('c2', D2, '%', 100);
</script>
'''
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "findings.html"), "w").write(html); print("findings.html", len(html) // 1024, "KB")
