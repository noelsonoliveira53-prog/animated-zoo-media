# ZooBlender 3D engine: how the pieces fit

```
sing.py (container)  song.json -> song.wav + timing.json (words, lines, sections, beats, mouth@24fps)
engine.py (Blender)  job.json + timing + song.wav -> out/<id>/frames/*.png -> out/<id>/<id>_raw.mp4
finish.py (container) raw.mp4 -> karaoke lyrics captions + end card -> final MP4 + thumbnail -> repo + upload plan
worker.bat (Noelson's PC, RTX 4060 Ti, EEVEE) renders every job in Documents\ZooBlender\jobs
```

Test in the container (no GPU, Cycles on CPU, keep it small):
```
cd /root/zoo/blender/zoo3d
/root/bpyenv/bin/python bpyrun.py engine.py -- --job jobs/<id>.json --test --engine CYCLES --res 640x360 --samples 12 --frames 30,300,900
```
Stills land in `out/<id>/test_*.png`. Look at them with the Read tool.

## Character module: `chars/<name>.py`
```python
def build(L, prefix, loc=(0,0,0), scale=1.0, **opts) -> Char   # opts from job cast[].opts (color, variant, ...)
class Char:
    height: float   # top of head above the ground at scale 1
    face_z: float   # height of the face (camera aims here for close-ups)
    root            # empty placed at loc; engine sets root.rotation_euler z (yaw)
    def pose(self, f, t, s): ...   # set values with L.key(obj, "location"/"rotation_euler"/"scale", f, value)
```
`s` (state) keys: `talk` 0..1 (mouth open, from the vocal), `energy` 0..1 (dance size), `beat` 0..1 (phase in the beat),
`bar` 0..1 (phase in a 4-beat bar), `look` (yaw radians toward whoever sings), `wave` 0/1 (arm wave / celebrate),
`jump` 0..1 (hop on beats), `blink` bool, `singing` bool.
Rules: the character faces **-Y** (toward the camera). Z is up. The ground is z = 0. Build everything procedurally
with `lib.py` helpers (sphere, cube with bevel, cylinder, cone, torus, text3d, eye_pair, mat). Big glossy eyes
(`L.eye_pair`) with blinking lids, a mouth or jaw that opens with `talk`, squash and stretch on the beat, and limbs or
parts that dance. Keep it to about 150 objects or fewer and segs at 48 or less, because it has to render fast in EEVEE.
Look: premium preschool 3D (Cocomelon, Pinkfong, Pixar shorts). Rounded, soft, saturated colors, clearcoat or sheen,
expressive faces. Never creepy: eyes need white catchlights, and mouths stay simple shapes.

## Set module: `sets/<name>.py`
```python
def build(L, rng, **opts) -> dict(
    spots={"center":(x,y,z), "left":..., "right":..., ...},      # where cast members stand
    cams={"wide": ((camx,camy,camz), (aimx,aimy,aimz)), "center": (x,y,z), "orbit_r": 9, ...},  # extra named shots allowed
    prop_spots={"top":(...), "left":(...), "right":(...), "front":(...)},  # where teaching props pop in
    exposure=-0.2, look="AgX - Punchy" or "AgX - High Contrast")
def prop(L, name, at, **opts) -> obj      # optional: set-specific teaching props a job can pop in ({"type":"set_prop","name":...})
def animate(L, SET, f, t, s)              # optional: animated set pieces (lights pulsing on the beat, clouds, wheels)
```
The set adds its own world/sky and lights (use `L.sky`, `L.light`). Keep the camera's wide view full of color and depth,
with foreground, midground and background.

## Job: `jobs/<id>.json`
```json
{"id": "tt3d_ep01_firetruck", "channel": "truck", "set": "town", "timing_file": "<id>_timing.json", "audio": "<id>_song.wav",
 "cast": [{"id": "host", "char": "truck", "spot": "center", "opts": {"color": "#e53935"}},
          {"id": "pal", "char": "truck", "spot": "left", "opts": {"variant": "police"}, "yaw": 0.3}],
 "intro_shot": "orbit", "thumb_frame": 400,
 "direct": [{"section": "chorus1", "shots": ["wide", "close:host", "orbit", "low"], "energy": 1.0, "wave": 1, "jump": 0.4, "group": true,
             "props": [{"type": "text", "text": "RED", "color": "#e53935", "at": "top"},
                       {"type": "set_prop", "name": "ladder", "at": "left", "delay": 1.0}]}]}
```
Each section's shots cycle once per sung line, so the camera cuts land on line starts. Shot names: `wide`, any named cam from
the set, `close:<castid>`, `orbit`, `low`, `top`. Section names must match the `section` names in the song JSON.
