"""Quick look: draws given SVG content on a 1920x1080 stage and saves a PNG (for checking art before a render)."""
import sys, asyncio, os
from playwright.sync_api import sync_playwright
FONT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "vendor/f/package/files/baloo-2-latin-800-normal.woff2"))
def shot(svg_inner, out, w=1920, h=1080, extra_html="", scale=1):
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:"Baloo";src:url(file://{FONT}) format("woff2");font-weight:800}}
*{{margin:0}}body{{width:{w}px;height:{h}px;overflow:hidden;font-family:Baloo}}</style></head><body><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;inset:0">{svg_inner}</svg>{extra_html}</body></html>'''
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale); pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path=out); b.close()
