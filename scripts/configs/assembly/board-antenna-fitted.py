# The antenna model has its U.FL plug cap-up. Mated, the round cap faces down over the socket and the flat back
# faces up, so flip the plug 180 degrees about the cable's axis (the cable stays joined).
c = bpy.data.objects["ant-coax"]
pts = [c.matrix_world @ Vector(v) for v in c.bound_box]
pivot = Vector((0, sum(p.y for p in pts) / 8, sum(p.z for p in pts) / 8))
flip = Matrix.Translation(pivot) @ Matrix.Rotation(math.pi, 4, "X") @ Matrix.Translation(-pivot)
for n in ("ant-ufl-body", "ant-ufl-cap"):
    o = bpy.data.objects[n]; o.matrix_world = flip @ o.matrix_world

# Frame on the ESP32-S3 module and the antenna plug, so the plug reads at step-image size.
# Everything else still renders; the rest of the board and the antenna run off the edges.
objs[:] = [o for o in objs if "WROOM" in o.name or o.name.startswith(("I-IPEX", "ant-ufl"))]
