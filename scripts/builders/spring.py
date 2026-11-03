# Compression spring: 304 stainless, 3 mm OD, 0.3 mm wire, 5 mm free length, closed ends
# (7 turns: 5 active + 1 closed each end; the coil count is an assumption, the supplier gives none).
# bcfg["at"]: list of [x, y, z_base] in mm. Runs inside brender.py.
import math
OD, WIRE, FREE, ACTIVE = 3.0, 0.3, 5.0, 5
R = (OD - WIRE) / 2
STEEL304 = bpy.data.materials.new("steel304"); STEEL304.use_nodes = True
_b = STEEL304.node_tree.nodes["Principled BSDF"]
_b.inputs["Base Color"].default_value = lin("#B6B9BD"); _b.inputs["Metallic"].default_value = 1.0
_b.inputs["Roughness"].default_value = 0.3
p_act = (FREE - WIRE - 2 * WIRE) / ACTIVE  # closed turns use pitch = wire
def z_at(t):  # t in turns, 0..ACTIVE+2
    if t <= 1: return WIRE / 2 + t * WIRE
    if t <= 1 + ACTIVE: return WIRE / 2 + WIRE + (t - 1) * p_act
    return WIRE / 2 + WIRE + ACTIVE * p_act + (t - 1 - ACTIVE) * WIRE
N, STEPS = ACTIVE + 2, 64
for i, (x, y, z0) in enumerate(bcfg.get("at", [[0, 0, 0]])):
    cu = bpy.data.curves.new(f"spring{i}", "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = WIRE / 2; cu.bevel_resolution = 6; cu.use_fill_caps = True
    sp = cu.splines.new("POLY"); pts = N * STEPS + 1; sp.points.add(pts - 1)
    for k in range(pts):
        t = k / STEPS; a = 2 * math.pi * t
        sp.points[k].co = (x + R * math.cos(a), y + R * math.sin(a), z0 + z_at(t), 1)
    o = bpy.data.objects.new(f"spring{i}", cu); sc.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    for other in bpy.context.selected_objects: other.select_set(False)
    o.select_set(True); bpy.ops.object.convert(target="MESH")  # mesh so it can be measured for labels
    o = bpy.context.view_layer.objects.active; o.data.materials.append(STEEL304)
    bpy.ops.object.shade_smooth(); o.select_set(False); objs.append(o)
