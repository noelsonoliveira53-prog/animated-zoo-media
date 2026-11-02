import re, json
from art import MILO, SCENES
from art2 import SCENES2
S = {**SCENES, **SCENES2}
def animal(key):
    s = S[key]; i = s.index('<g id="animal"'); depth = 0; j = i
    for m in re.finditer(r'<g[\s>]|</g>', s[i:]):
        depth += 1 if m.group().startswith('<g') else -1
        if depth == 0: j = i + m.end(); break
    defs = re.search(r'<defs>.*?</defs>', s, re.S)
    d = defs.group() if defs and 'clipPath' in defs.group() else ''
    return d + s[i:j]
def pet(key, x, y, h, flip=False, vb="0 0 1080 1100"):
    w = h * 1080 / 1100
    tr = f' style="transform:scaleX(-1)"' if flip else ''
    return f'<svg viewBox="{vb}" width="{w:.0f}" height="{h}" style="position:absolute;left:{x}px;top:{y}px"{tr.replace("style=","")and ""}><g{" transform=\"translate(1080 0) scale(-1 1)\"" if flip else ""}>{animal(key)}</g></svg>'
font = "@font-face{font-family:Baloo;src:url(/root/zoo/vendor/f/package/files/baloo-2-latin-800-normal.woff2)}"
hills = '<svg width="2560" height="1440" style="position:absolute;left:0;top:0"><path d="M0 1020 Q400 900 800 1000 T1600 990 T2560 960 L2560 1440 L0 1440Z" fill="#7ccf5a"/><path d="M0 1120 Q500 1040 1000 1110 T2000 1100 T2560 1080 L2560 1440 L0 1440Z" fill="#5fb043"/><circle cx="2300" cy="230" r="120" fill="#ffe066"/><g fill="#fff"><ellipse cx="420" cy="260" rx="140" ry="50"/><ellipse cx="350" cy="240" rx="70" ry="55"/><ellipse cx="1900" cy="330" rx="120" ry="44"/><ellipse cx="1960" cy="310" rx="60" ry="46"/></g></svg>'
pets = (pet("giraffe", -40, 330, 760) + pet("elephant", 150, 640, 470) + pet("panda", 2080, 640, 440) + pet("lion", 2220, 600, 480, flip=True)
        + pet("penguin", 1840, 760, 300) + pet("zebra", 330, 760, 330))
banner = f"""<html><head><style>{font}*{{margin:0}}body{{width:2560px;height:1440px;position:relative;overflow:hidden;background:linear-gradient(#7fd0ff,#e3f6ff);font-family:Baloo}}
#t{{position:absolute;left:800px;width:1250px;top:585px;text-align:center;font-size:138px;line-height:1;color:#fff;-webkit-text-stroke:18px #1c5fc4;paint-order:stroke fill;text-shadow:0 12px 0 rgba(0,0,0,.12)}}
#s{{position:absolute;left:800px;width:1250px;top:770px;text-align:center;font-size:56px;color:#1c5fc4}}
#s span{{background:#fff;border-radius:50px;padding:10px 46px 0;box-shadow:0 8px 0 rgba(0,0,0,.1)}}
#m{{position:absolute;left:540px;top:545px;transform:scale(1.3);transform-origin:0 0}}
</style></head><body>{hills}{pets}<div id="t">THE ANIMATED ZOO</div><div id="s"><span>Fun animal facts with Milo! 🦒🐧🐘</span></div><div id="m">{MILO}</div></body></html>"""
open("brand/banner.html","w").write(banner)
avatar = f"""<html><head><style>*{{margin:0}}body{{width:800px;height:800px;background:radial-gradient(circle at 50% 40%,#ffe066 0,#ffd23f 45%,#ffb703 100%);display:flex;align-items:center;justify-content:center}}svg{{transform:scale(2.3) translate(6px,6px)}}</style></head><body>{MILO}</body></html>"""
open("brand/avatar.html","w").write(avatar)
