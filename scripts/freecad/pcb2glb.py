# Board STEP -> colored {WORK}/pcb/BlueBuzzah_v3.glb. Colors only load with the GUI's view providers, so run the full
# FreeCAD app offscreen (no window): QT_QPA_PLATFORM=offscreen freecad pcb2glb.py
import os, FreeCAD, FreeCADGui, ImportGui
step = os.environ.get("BOARD_STEP", os.path.join(os.environ["HW"], "models", "BlueBuzzah-v3-pcb-model.step"))
out = os.path.join(os.environ["WORK"], "pcb", "BlueBuzzah_v3.glb")
try:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc = FreeCAD.newDocument("p"); ImportGui.insert(step, "p")
    ImportGui.export([o for o in doc.RootObjects if o.TypeId in ("App::Part", "Part::Feature")], out)
except Exception:
    import traceback; traceback.print_exc()
os._exit(0)
