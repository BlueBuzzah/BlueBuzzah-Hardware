# Shorten the lead's insulation to a short stub so the wire plug fills the frame.
# The lead runs along Z here; scale each wire along Z about its stripped end (the end nearest the copper).
STUB = 6.0  # mm of insulation to keep
lead = [o for o in objs if o["grp"] == "lead"]
bare_z = sum((o.matrix_world @ Vector(c)).z for o in lead if o.name.startswith("bare") for c in o.bound_box) / 16
for o in lead:
    if not o.name.startswith("wire"):
        continue
    zs = [(o.matrix_world @ Vector(c)).z for c in o.bound_box]
    pivot = min(zs, key=lambda z: abs(z - bare_z))
    k = STUB / (max(zs) - min(zs))
    o.matrix_world = (Matrix.Translation((0, 0, pivot)) @ Matrix.Diagonal((1, 1, k, 1))
                      @ Matrix.Translation((0, 0, -pivot)) @ o.matrix_world)
