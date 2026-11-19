"""Gizmo Explains lessons (Nov 19 2026, docs/GIZMO_RUN.md "Engine"): one set module for a lesson job that visits Gizmo's science lab
and outdoor places. A location with "biome": "lab" is the space-station science lab (sets/sciencelab.py); every other biome is a
Zoo World place (sets/zooworld.py: river, spring_meadow, beach, mountain, night_meadow ...). Props: sciencelab.prop names.
"""
from sets import zooworld as ZW, sciencelab as SL


def build(L, rng, biome="spring_meadow", **o):
    if biome == "lab":
        st = SL.build(L, rng); st["_gz"] = "lab"; return st
    st = ZW.build(L, rng, biome=biome, **o); st["_gz"] = "out"; return st


def animate(L, SET, f, t, s):
    (SL if SET.get("_gz") == "lab" else ZW).animate(L, SET, f, t, s)


def prop(L, name, at, **o):
    return SL.prop(L, name, at, **o)
