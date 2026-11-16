#!/bin/bash
# TAGS="tag a|tag b" limits the stills to those shots.
# stills.sh <episode> <short index or L> <sheet.jpg> [cols] [width] [extra times]: one still near the end of every shot, tiled
cd "$(dirname "$0")"
ep=$1; n=$2; out=$3; cols=${4:-8}; w=${5:-300}
if [ "$n" = L ]; then tj=out/$ep/${ep}_timing.json; flag="--plan"; proj=proj_l; python3 toon.py $ep --plan >/dev/null 2>&1; sf="";
else python3 toon.py $ep --short $n --plan >/dev/null 2>&1; sid=$(python3 -c "import sys;sys.path.insert(0,'.');import importlib;print(importlib.import_module('episodes.$ep').SHORTS[$n]['id'])"); tj=out/$ep/${sid}_timing.json; proj=proj_p; sf="--short $n"; fi
T=$(python3 -c "
import json
t=json.load(open('$tj'))
import os; tags=[x for x in os.environ.get('TAGS','').split('|') if x]
print(','.join(f\"{s['t1']-0.3:.2f}\" for s in t['shots'] if not tags or s['tag'] in tags))")
[ -n "$6" ] && T="$T,$6"
python3 toon.py $ep $sf --stills $T >/dev/null 2>&1
python3 sheet.py out/$ep/$proj $out $cols $w
