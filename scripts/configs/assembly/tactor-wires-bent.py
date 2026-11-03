# Same scene as tactor-wires-inserted (plug held upside down, insulation flush underneath), with each bare end
# bent over: up the through slot, out into its pocket on the plug's face, along it, then down the side slot.
# Plug features in this flipped frame: face z 2.8, pockets |x| 1.3-1.9 y 5.2-7.3 (floor z 2.2-2.4),
# side slots y 7.6-8.4 |x| 0.7-2.1 (full height). The insulation ends at z 0.26, wires at x +-1.0, y 5.65.
STUB = 6.0  # mm of insulation to keep
lead = [o for o in objs if o["grp"] == "lead"]
for o in lead:
    if not o.name.startswith("wire"):
        continue
    zs = [(o.matrix_world @ Vector(c)).z for c in o.bound_box]
    pivot = max(zs)
    k = STUB / (max(zs) - min(zs))
    o.matrix_world = (Matrix.Translation((0, 0, pivot)) @ Matrix.Diagonal((1, 1, k, 1))
                      @ Matrix.Translation((0, 0, -pivot)) @ o.matrix_world)

copper = bpy.data.objects["bare0"].data.materials[0]
for n in ("bare0", "bare1"):
    objs.remove(bpy.data.objects[n]); bpy.data.objects.remove(bpy.data.objects[n])

R = 0.2  # copper radius (26 AWG)
for s in (-1, 1):
    pts = [(1.0, 5.65, 0.26), (1.0, 5.65, 2.2), (1.15, 5.65, 2.45), (1.6, 5.95, 2.5), (1.6, 7.1, 2.5),
           (1.6, 7.75, 2.35), (1.6, 8.0, 2.0), (1.6, 8.0, 0.9)]
    cu = bpy.data.curves.new("bent", "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = R; cu.bevel_resolution = 6; cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for bp, (x, y, z) in zip(sp.bezier_points, pts):
        bp.co = (s * x, y, z); bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new("bent", cu); bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    for x in bpy.context.view_layer.objects: x.select_set(x is o)
    bpy.ops.object.convert(target="MESH")
    o = bpy.context.view_layer.objects.active
    o.data.materials.clear(); o.data.materials.append(copper)
    o["grp"] = "lead"; objs.append(o)
