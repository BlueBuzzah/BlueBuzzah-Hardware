# M2x5 pan-head Phillips machine screw (ISO 7045: head 4.0 mm dia x 1.6 mm, 0.4 mm pitch), zinc-plated steel.
# mm; axis Z, underside of the head at z=0, shank down to z=-5. bcfg["at"]: [[x, y, z_head_underside], ...].
# Runs inside brender.py.
import math, bmesh
STEEL = bpy.data.materials.new("m2-steel"); STEEL.use_nodes = True
_b = STEEL.node_tree.nodes["Principled BSDF"]
_b.inputs["Base Color"].default_value = lin("#B4B7BB"); _b.inputs["Metallic"].default_value = 1.0
_b.inputs["Roughness"].default_value = 0.35
DK, K, D, LEN, P = 4.0, 1.6, 2.0, 5.0, 0.4
def mk(name):
    o = bpy.context.object; o.name = name; o.data.materials.append(STEEL); return o
def join(parts, name):
    for o in bpy.context.selected_objects: o.select_set(False)
    for o in parts: o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]; bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active; o.name = name; return o
for i, (x, y, z) in enumerate(bcfg.get("at", [[0, 0, 0]])):
    # pan head: short cylinder with a flattened dome on top
    bpy.ops.mesh.primitive_cylinder_add(radius=DK / 2, depth=0.7, vertices=64, location=(x, y, z + 0.35)); head = mk(f"m2-head{i}")
    bpy.ops.mesh.primitive_uv_sphere_add(radius=DK / 2, segments=64, ring_count=32, location=(x, y, z + 0.7)); dome = mk(f"m2-dome{i}")
    dome.scale = (1, 1, (K - 0.7) / (DK / 2)); bpy.ops.object.transform_apply(scale=True)
    me = dome.data; bm = bmesh.new(); bm.from_mesh(me)   # keep only the upper half of the dome
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < z + 0.7 - 1e-4], context="VERTS"); bm.to_mesh(me); bm.free()
    # shank (minor diameter) with a helical thread ridge
    bpy.ops.mesh.primitive_cylinder_add(radius=0.8, depth=LEN, vertices=48, location=(x, y, z - LEN / 2)); shank = mk(f"m2-shank{i}")
    cu = bpy.data.curves.new(f"m2-thread{i}", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.17; cu.bevel_resolution = 3
    sp = cu.splines.new("POLY"); turns = (LEN - 0.4) / P; n = int(turns * 32) + 1; sp.points.add(n - 1)
    for k in range(n):
        a = 2 * math.pi * k / 32
        sp.points[k].co = (x + 0.83 * math.cos(a), y + 0.83 * math.sin(a), z - 0.2 - k / 32 * P, 1)
    th = bpy.data.objects.new(f"m2-thread{i}", cu); sc.collection.objects.link(th)
    for o in bpy.context.selected_objects: o.select_set(False)
    th.select_set(True); bpy.context.view_layer.objects.active = th; bpy.ops.object.convert(target="MESH"); th = bpy.context.view_layer.objects.active
    screw = join([head, dome, shank, th], f"m2-screw{i}")
    # Phillips recess: two crossed slots cut into the dome
    for j, (sx, sy) in enumerate(((2.0, 0.5), (0.5, 2.0))):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z + K)); cut = bpy.context.object; cut.scale = (sx, sy, 1.6)
        m = screw.modifiers.new(f"ph{j}", "BOOLEAN"); m.operation = "DIFFERENCE"; m.object = cut; m.solver = "EXACT"
        bpy.context.view_layer.objects.active = screw; bpy.ops.object.modifier_apply(modifier=m.name); bpy.data.objects.remove(cut)
    for p in screw.data.polygons: p.use_smooth = True
    bpy.context.view_layer.objects.active = screw; screw.select_set(True); bpy.ops.object.shade_smooth_by_angle(angle=0.6); screw.select_set(False)
    if not screw.data.materials: screw.data.materials.append(STEEL)
    objs.append(screw)
