# Tactor housing STEP -> one closed STL per printed part in {WORK}/tactor (named after the part, spaces as _).
# Run: freecadcmd -c "exec(open('export_tactor.py').read())"
import os, sys; sys.path.insert(0, os.path.join(os.environ["SCRIPTS"], "freecad")); from common import *
OMIT = {"Pin-.5mm", "Pin-1mm", "Supports", "Supports001"}  # alternate pin lengths and print supports
doc = load(TACTOR_STEP)
for o in doc.Objects:
    if o.TypeId == "Part::Feature" and o.Label not in OMIT:
        write_closed(placed(o), os.path.join(WORK, "tactor", o.Label.replace(" ", "_") + ".stl"))
