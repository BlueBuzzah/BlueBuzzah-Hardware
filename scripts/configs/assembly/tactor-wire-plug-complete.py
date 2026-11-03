# Finished wire plug, held upside down as in tactor-wires-inserted/-bent. The insulation bends 90 degrees inside the
# through slot and lies in the notch (here on the underside: |x| < 1.1, y 6.6-11, recessed to z 1.26), the two wires
# side by side; it runs out the back. The copper runs up the slot, along its pocket on the top face (z 2.8) and down
# the side slot, at or below the face. Copper and insulation are rebuilt as tubes; the model's straight wires go.
def tube(name, pts, r, material, s):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = r; cu.bevel_resolution = 6; cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for bp, (x, y, z) in zip(sp.bezier_points, pts):
        bp.co = (s * x, y, z); bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu); bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    for x in bpy.context.view_layer.objects: x.select_set(x is o)
    bpy.ops.object.convert(target="MESH")
    o = bpy.context.view_layer.objects.active
    o.data.materials.clear(); o.data.materials.append(material)
    o["grp"] = "lead"; objs.append(o)

mats = {n: bpy.data.objects[n].data.materials[0] for n in ("bare0", "wire0", "wire1")}
for o in [o for o in objs if o["grp"] == "lead"]:
    objs.remove(o); bpy.data.objects.remove(o)

for s, insul in ((-1, mats["wire0"]), (1, mats["wire1"])):
    tube("insulation", [(1.0, 5.65, 1.0), (0.9, 5.75, 0.75), (0.7, 6.3, 0.71), (0.55, 7.0, 0.71),
                        (0.55, 11.0, 0.71), (0.8, 14.0, 0.71), (1.0, 17.0, 0.71)], 0.55, insul, s)
    tube("copper", [(1.0, 5.65, 0.9), (1.0, 5.65, 2.2), (1.15, 5.65, 2.45), (1.6, 5.95, 2.5), (1.6, 7.1, 2.5),
                    (1.6, 7.75, 2.35), (1.6, 8.0, 2.0), (1.6, 8.0, 0.9)], 0.2, mats["bare0"], s)
