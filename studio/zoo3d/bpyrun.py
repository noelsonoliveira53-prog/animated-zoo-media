# Container stand-in for `blender -b -P script -- args`:  python bpyrun.py script.py -- args
import sys, runpy
script = sys.argv[1]; sys.argv = ["blender"] + sys.argv[2:]
runpy.run_path(script, run_name="__main__")
