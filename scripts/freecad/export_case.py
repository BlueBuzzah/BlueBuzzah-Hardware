# v3 case STEP -> lower-shell.stl, upper-shell.stl, switch.stl in {WORK}/case (the case uses the board's axes).
import os, sys; sys.path.insert(0, os.path.join(os.environ["SCRIPTS"], "freecad")); from common import *
NAMES = {"Lower shell": "lower-shell", "Upper shell": "upper-shell", "Switch": "switch"}
doc = load(CASE_STEP)
for o in doc.Objects:
    if o.TypeId == "Part::Feature" and o.Label in NAMES:
        write_closed(placed(o), os.path.join(WORK, "case", NAMES[o.Label] + ".stl"))
