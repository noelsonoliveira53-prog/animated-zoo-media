"""Turn a channel scene into a printable coloring page (black outlines on white). Usage: python3 books/lineart.py <scene_key> <out.html>"""
import re, sys
sys.path.insert(0, "/root/zoo")
import build
def subject(svg):
    i = svg.index('<g id="animal"'); depth = 0
    for m in re.finditer(r'<g[\s>]|</g>', svg[i:]):
        depth += 1 if m.group().startswith('<g') else -1
        if depth == 0: return "".join(re.findall(r'<defs>.*?</defs>', svg, re.S)) + svg[i:i + m.end()]
def outline(g):
    g = re.sub(r'fill="(?!none)[^"]*"', 'fill="#fff"', g)
    g = re.sub(r'stroke="[^"]*"', 'stroke="#111"', g)
    g = re.sub(r'stroke-width="[^"]*"', 'stroke-width="7"', g)
    g = re.sub(r'opacity="[^"]*"', '', g)
    g = re.sub(r'<(circle|ellipse|rect|path|polygon)\b(?![^>]*stroke=)', r'<\1 stroke="#111" stroke-width="7"', g)
    return g
def page(key, label):
    s = build.SCENES[key]
    return f'''<div class="pg"><div class="lbl">{label}</div><svg viewBox="0 120 1080 980">{outline(subject(s))}</svg><div class="foot">Color me!</div></div>'''
if __name__ == "__main__":
    key, out = sys.argv[1], sys.argv[2]
    css = "@font-face{font-family:Baloo;src:url(/root/zoo/vendor/f/package/files/baloo-2-latin-800-normal.woff2)}*{margin:0}body{background:#fff}.pg{width:2550px;height:3300px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:60px;font-family:Baloo}.lbl{font-size:220px;letter-spacing:6px;-webkit-text-stroke:8px #111;color:#fff}.pg svg{width:2200px;height:2000px}.foot{font-size:90px;color:#111}"
    open(out, "w").write(f"<html><head><style>{css}</style></head><body>{page(key, sys.argv[3] if len(sys.argv) > 3 else key.upper())}</body></html>")
