"""Thumbnails + upload plan for a channel. Usage: python3 mkplan.py <channel>"""
import json, re, os, sys
CH = sys.argv[1]
font = "@font-face{font-family:Baloo;src:url(/root/zoo/vendor/f/package/files/baloo-2-latin-800-normal.woff2)}"
if CH == "bloop":
    from art_bloop import SCENES7 as S, BLOOP as HOST
    cfg = dict(name="Bloop's Color Lab", host_desc="Bloop the jelly blob", aud="1-5", aud2="1–5", emoji="🌈", tag="#ColorsForKids #ShapesForKids #KidsLearning",
               bg="#e9f6ff", stroke="#3d2a7a", accent="#9d6bff", ground="#f3edff", short_time="7:50 AM", ep_time="1:50 PM", prefix="bloop", shorts="shorts_bloop.json", eps="bl_ep",
               short_kind="A fun learning Short", ep_kind="learning adventure",
               T={"bl_ep01_colors": ("LEARN", "COLORS!"), "bl_ep02_shapes": ("LEARN", "SHAPES!"), "bl_ep03_counting": ("COUNT", "TO 5!"),
                  "bl_ep04_morecolors": ("MORE", "COLORS!"), "bl_ep05_moreshapes": ("MORE", "SHAPES!")})
exec(open(f"mkplan_{CH}.py").read()) if os.path.exists(f"mkplan_{CH}.py") else None
def animal(s):
    i = s.index('<g id="animal"'); depth = 0; j = i
    for m in re.finditer(r'<g[\s>]|</g>', s[i:]):
        depth += 1 if m.group().startswith('<g') else -1
        if depth == 0: j = i + m.end(); break
    return "".join(re.findall(r'<defs>.*?</defs>', s, re.S)) + s[i:j]
def pet(k, x, y, h):
    w = h * 1080 / 1100; return f'<svg viewBox="0 0 1080 1100" width="{w:.0f}" height="{h}" style="position:absolute;left:{x}px;top:{y}px">{animal(S[k])}</svg>'
os.makedirs(f"brand/{cfg['prefix']}", exist_ok=True)
pos = [(-40, 300, 400), (160, 350, 360), (360, 310, 390), (560, 350, 360), (760, 320, 380)]
dates = ["2026-11-04", "2026-11-06", "2026-11-08", "2026-11-10", "2026-11-11"]
B = f"{cfg['name']} makes gentle, colorful videos for little learners. New videos every day! Made with care for ages {cfg['aud']}. Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing."
plan = []
for i, s in enumerate(json.load(open(cfg["shorts"]))):
    b = [x["say"] for x in s["beats"]]
    d = f"{b[0]} {cfg['host_desc']} finds out! {cfg['emoji']}\n{cfg['short_kind']} for kids ages {cfg['aud2']} from {cfg['name']}.\n\n{' '.join(b[2:5])}\n\n{B}\n\n#Shorts {cfg['tag']}"
    plan.append({"file": f"{cfg['prefix']}/{s['id']}.mp4", "title": s["title"], "description": d, "date": f"2026-11-0{4+i}", "time": cfg["short_time"], "status": "to_upload"})
for (k, (a, b2)), dt in zip(cfg["T"].items(), dates):
    e = json.load(open(f"eps/{k}.json")); keys = [x["key"] for x in e["animals"]]
    p = "".join(pet(v, x, y, h) for v, (x, y, h) in zip(keys, pos))
    html = f"""<html><head><style>{font}*{{margin:0}}body{{width:1280px;height:720px;overflow:hidden;position:relative;font-family:Baloo;background:radial-gradient(circle at 70% 30%,#fff7d6 0,{cfg['bg']} 62%)}}
.t{{position:absolute;left:40px;font-size:{110 if len(a)<12 else 92}px;line-height:1;color:#fff;-webkit-text-stroke:14px {cfg['stroke']};paint-order:stroke fill;text-shadow:0 8px 0 rgba(0,0,0,.18)}}
#n{{position:absolute;right:40px;top:30px;width:180px;height:180px;border-radius:50%;background:{cfg['accent']};color:#fff;font-size:140px;line-height:205px;text-align:center;box-shadow:0 8px 0 rgba(0,0,0,.18)}}
#m{{position:absolute;left:930px;top:250px;transform:scale(1.05);transform-origin:0 0}}#g{{position:absolute;left:0;right:0;bottom:0;height:110px;background:{cfg['ground']}}}</style></head>
<body><div id="g"></div>{p}<div class="t" style="top:28px">{a}</div><div class="t" style="top:140px;color:#ffe066">{b2}</div><div id="n">5</div><div id="m">{HOST}</div></body></html>"""
    open(f"brand/{cfg['prefix']}/thumb_{k}.html", "w").write(html)
    learn = "\n".join("• " + r[0] for r in e["recap"][1:])
    d = f"Join {cfg['host_desc']} for a 5-minute {cfg['ep_kind']}! {e['intro'][1][0]} {cfg['emoji']}\nMade for little learners ages {cfg['aud2']}: guess-what clues, move-along fun, and a recap at the end.\n\nWhat we learn today:\n{learn}\n\n{B}\n\n{cfg['tag']}"
    plan.append({"file": f"{cfg['prefix']}/{k}.mp4", "title": e["title"], "description": d, "date": dt, "time": cfg["ep_time"], "status": "to_upload", "thumb": f"brand/{cfg['prefix']}/thumb_{k}.png"})
json.dump(plan, open(f"upload_plan_{cfg['prefix']}.json", "w"), indent=1, ensure_ascii=False)
print(len(plan), plan[5]["description"][:300])
