# Shared by the assembly hooks: the finished wire-plug wiring (copper in the plug's underside pockets and side
# slots, insulation in the top notch running out the back), in the assembled tactor frame, built as tubes.
# Load the "wire-lead" model in the scene for its materials; this removes it. Use it from a hook with
#   exec(open(os.path.join(ENV["scripts"], "configs", "assembly", "tactor_wiring.py")).read())
#   wiring(dy=0.0, grp="lead", tail=20.0)
# The points are tactor-wire-plug-complete's (that image is upside down, so z -> 4 - z here).
_m = {n: bpy.data.objects[n].data.materials[0] for n in ("bare0", "wire0", "wire1")}
for _o in [o for o in objs if o.name in ("bare0", "bare1", "wire0", "wire1") or o.name.startswith(("ph-", "contact"))]:
    objs.remove(_o); bpy.data.objects.remove(_o)

def _tube(pts, r, material, grp):
    cu = bpy.data.curves.new("wire", "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = r; cu.bevel_resolution = 6; cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new("wire", cu); bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    for x in bpy.context.view_layer.objects: x.select_set(x is o)
    bpy.ops.object.convert(target="MESH")
    o = bpy.context.view_layer.objects.active
    o.data.materials.clear(); o.data.materials.append(material)
    o["grp"] = grp; objs.append(o)

def wiring(dx=0.0, dy=0.0, grp="lead", tail=20.0):
    insul = [(1.0, 5.65, 1.0), (0.9, 5.75, 0.75), (0.7, 6.3, 0.71), (0.55, 7.0, 0.71), (0.55, 11.0, 0.71),
             (0.8, 14.0, 0.71), (1.0, tail, 0.71)]
    copper = [(1.0, 5.65, 0.9), (1.0, 5.65, 2.2), (1.15, 5.65, 2.45), (1.6, 5.95, 2.5), (1.6, 7.1, 2.5),
              (1.6, 7.75, 2.35), (1.6, 8.0, 2.0), (1.6, 8.0, 0.9)]
    for s, insul_mat in ((1, _m["wire0"]), (-1, _m["wire1"])):
        f = lambda p: (dx + s * p[0], dy + p[1], 4.0 - p[2])
        _tube([f(p) for p in insul], 0.55, insul_mat, grp)
        _tube([f(p) for p in copper], 0.2, _m["bare0"], grp)
