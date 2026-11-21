"""gzintro: the Gizmo Explains main intro, rendered alone as a preview (owner, Nov 21 2026 12:01 PM: "create an intro for the gizmo explain as well").
The intro itself lives in studio/cartoon/intro_gizmo.py; this file only renders it so it can be watched and heard on its own."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
import art_gizmo as G
from kit import Kit
from intro_gizmo import GZ_INTRO_STAGES, gz_intro_shots

EP = {"id": "gzintro", "nest": True, "beat": True, "voice": "am_michael", "speed": 0.85, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 0.0, "intro": False, "wm": "brand/gizmo",
      "cast": {"gizmo": {"voice": "am_michael", "speed": 0.85}},
      "title": "Gizmo Explains (main intro)", "thumb_text": "", "series": "", "description": "", "tags": []}
STAGES = dict(GZ_INTRO_STAGES)
K = Kit(STAGES)
SHOTS = gz_intro_shots()
SHORTS = []
