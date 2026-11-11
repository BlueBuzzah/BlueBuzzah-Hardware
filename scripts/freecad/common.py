# Shared by the FreeCAD export scripts: input/output paths and closed-mesh export.
# Paths come from environment variables (render_all.py sets them); the STEP names can be overridden after renames.
import os, FreeCAD, Import, MeshPart
HW = os.environ["HW"]                      # BlueBuzzah-Hardware repo checkout
WORK = os.environ["WORK"]                  # scratch folder for intermediate meshes
MODELS = os.path.join(HW, "models")
TACTOR_STEP = os.environ.get("TACTOR_STEP", os.path.join(MODELS, "BlueBuzzah-v3-tactor.step"))
CASE_STEP = os.environ.get("CASE_STEP", os.path.join(MODELS, "BlueBuzzah-v3-shell.step"))

def load(step):
    doc = FreeCAD.newDocument("d"); Import.insert(step, doc.Name)
    return doc

def placed(o):
    s = o.Shape.copy(); s.Placement = o.getGlobalPlacement(); return s

def write_closed(shape, path):
    """Mesh finely, coarsening only until the mesh is closed: the tactor STEP's finger cup solid is invalid and
    leaves holes (a big false opening in renders) at 0.01 mm deflection."""
    for ld, ad in ((0.01, 0.05), (0.02, 0.1), (0.05, 0.2)):
        m = MeshPart.meshFromShape(Shape=shape, LinearDeflection=ld, AngularDeflection=ad, Relative=False)
        if m.isSolid(): break
    os.makedirs(os.path.dirname(path), exist_ok=True); m.write(path)
