from brand import pet, font, MILO
T = {"ep01_savanna": ("SAVANNA", "FRIENDS!", ["giraffe","elephant","lion","zebra","hippo"], "#ffd166"),
     "ep02_ocean_ice": ("OCEAN &amp; ICE", "ANIMALS!", ["penguin","octopus","turtle","polarbear","flamingo"], "#8ecae6"),
     "ep03_treetops": ("TREETOP", "FRIENDS!", ["monkey","owl","panda","koala","sloth"], "#b5e48c"),
     "ep04_amazing_bodies": ("AMAZING", "BODIES!", ["giraffe","elephant","kangaroo","polarbear","flamingo"], "#ffc8dd"),
     "ep05_baby_animals": ("BABY", "ANIMALS!", ["gorilla","rhino","seal","elephant","sloth"], "#ffd6a5"),
     "ep06_desert": ("SUNNY DESERT", "FRIENDS!", ["camel","meerkat","ostrich","kangaroo","lion"], "#ffd59e")}
MILO_POS = {"ep06_desert": "left:960px;top:150px", "ep04_amazing_bodies": "left:600px;top:40px", "ep05_baby_animals": "left:640px;top:20px"}
POS = {"ep06_desert": [(-60, 300, 420), (230, 400, 330), (380, 230, 500), (600, 330, 400), (800, 330, 400)], "ep05_baby_animals": [(-60, 250, 470), (200, 330, 400), (470, 360, 380), (760, 320, 400), (840, 170, 400)]}
EXTRA = {"ep05_baby_animals": '<div style="position:absolute;left:880px;top:282px;width:420px;height:16px;border-radius:8px;background:#8d5a2b"></div>'}  # keep Milo off tall animals
for k, (a, b, an, bg) in T.items():
    pos = [(-60, 250, 470), (150, 330, 400), (340, 300, 430), (560, 330, 400), (770, 300, 430)]
    pos = POS.get(k, pos)
    pets = EXTRA.get(k, "") + "".join(pet(x, px, py, h) for x, (px, py, h) in zip(an, pos))
    html = f"""<html><head><style>{font}*{{margin:0}}body{{width:1280px;height:720px;overflow:hidden;position:relative;font-family:Baloo;
background:radial-gradient(circle at 70% 30%,#fff7d6 0,{bg} 60%)}}
.t{{position:absolute;left:40px;font-size:118px;line-height:1;color:#fff;-webkit-text-stroke:14px #1c5fc4;paint-order:stroke fill;text-shadow:0 8px 0 rgba(0,0,0,.18)}}
#n{{position:absolute;right:40px;top:30px;width:190px;height:190px;border-radius:50%;background:#ff5c8a;color:#fff;font-size:150px;line-height:215px;text-align:center;box-shadow:0 8px 0 rgba(0,0,0,.18)}}
#m{{position:absolute;left:860px;top:200px;transform:scale(1.05);transform-origin:0 0}}
#g{{position:absolute;left:0;right:0;bottom:0;height:120px;background:#5fb043}}</style></head>
<body><div id="g"></div>{pets}<div class="t" style="top:28px">{a}</div><div class="t" style="top:140px;color:#ffe066">{b}</div><div id="n">5</div><div id="m">{MILO}</div></body></html>"""
    if k in MILO_POS: html = html.replace("left:860px;top:200px", MILO_POS[k])
    open(f"brand/thumb_{k}.html", "w").write(html)
