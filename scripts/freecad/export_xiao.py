# XIAO-ESP32S3 STEP -> one STL per material in {WORK}/xiao, already placed on the v3 board's footprint U2
# (board STEP mm coords). The STEP has almost no colors, so parts are grouped by material here.
import os, sys; sys.path.insert(0, os.path.join(os.environ["SCRIPTS"], "freecad")); from common import *
import Part
doc = load(XIAO_STEP)
# Model is Y-up with USB at +X. Footprint U2 (KiCad at 137.79, 71.9475, 180 deg) puts USB toward the board edge (-Y in
# STEP) and pin 1 / R button / U.FL on +X: (x, y, z) -> (-z, -x, y), then centre the 20.95 x 17.78 board on the
# footprint, bottom pads (y -0.25) resting on the board's copper (z 1.556).
M = FreeCAD.Matrix(0, 0, -1, 0,  -1, 0, 0, 0,  0, 1, 0, 0)
cx, cz = (-8.67 + 12.28) / 2, (-15.0 + 2.78) / 2
M.move(FreeCAD.Vector(137.795 + cz, -71.9475 + cx, 1.556 + 0.25))
groups = {k: [] for k in ("xiao-pcb", "xiao-gold", "xiao-shield", "xiao-metal", "xiao-black", "xiao-button", "xiao-ufl")}
for o in doc.Objects:
    if o.TypeId != "Part::Feature": continue
    s = placed(o)
    parent = " ".join(p.Label for p in o.InListRecursive)
    if o.Label == "SOLID":  # board: big faces/edges black; pads and plated half-holes gold
        for f in s.Faces:
            b = f.BoundBox; full = b.YMax - b.YMin > 1.0
            plated = isinstance(f.Surface, Part.Cylinder) and f.Surface.Radius < 0.8
            gold = (f.Area < 20 and not full) or (full and plated)
            groups["xiao-gold" if gold else "xiao-pcb"].append(f)
        continue
    if "USB" in parent:
        role = "xiao-gold" if o.Label.startswith("BOSS-EXTRUDE") else "xiao-black" if o.Label in ("CUT-EXTRUDE5", "MIRROR2") else "xiao-metal"
    elif o.Label == "Shield": role = "xiao-shield"
    elif o.Label.startswith("U.FL"): role = "xiao-ufl"
    elif o.Label.startswith("Body"): role = "xiao-button"
    else: role = "xiao-metal"  # button pins
    groups[role] += s.Faces
os.makedirs(os.path.join(WORK, "xiao"), exist_ok=True)
for k, faces in groups.items():
    c = Part.makeCompound(faces); c.transformShape(M)
    MeshPart.meshFromShape(Shape=c, LinearDeflection=0.01, AngularDeflection=0.1, Relative=False).write(os.path.join(WORK, "xiao", k + ".stl"))
