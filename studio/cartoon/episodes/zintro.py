"""zintro: The Animated Zoo main intro, rendered alone as a preview (owner, Nov 20 2026). The intro itself lives in studio/cartoon/intro.py and is
placed after the hook in every new 2D episode; this file only renders it so it can be watched and heard on its own."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import art, art2, kit
from kit import Kit
from intro import INTRO_STAGES, intro_shots

EP = {"id": "zintro", "nest": True, "beat": True, "voice": "af_heart", "speed": 0.8, "gap": 0.42, "music": 0.5, "lead_in": 0.3, "tail": 0.0, "intro": False,      # tail 0: the last shot holds one second by itself (intro.py pause=1.0); "intro": False: this IS the intro, the plan check does not ask for it twice
     
      "title": "The Animated Zoo (main intro)", "thumb_text": "", "series": "", "description": "", "tags": []}
STAGES = dict(INTRO_STAGES)
K = Kit(STAGES)
SHOTS = intro_shots()
SHORTS = []
