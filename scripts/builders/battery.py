# PKCELL LP552035 LiPo (350 mAh, 3.7 V): 36 x 19.6 x 5.2 mm pouch, long edges rounded, Kapton-taped terminal end,
# red/black lead to a 2-pin JST-PH plug. mm; long axis +Y, wires leave the taped end along +Y, plug faces +Y.
# bcfg["wire_len"] shortens the lead for the image. Runs inside brender.py.
import bmesh, math
def pmat(name, hexc, metal=0.0, rough=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    return m
FOIL, TAPE = pmat("pouch-foil", "#C9CBCE", 0.6, 0.35), pmat("kapton", "#D99A1C", 0.0, 0.3)
INK = pmat("print", "#3A3D42", 0.0, 0.6)
NYL, RED, BLK, TIN = pmat("bat-ph", "#F1EFE8", rough=0.55), pmat("bat-red", "#D22B22", rough=0.6), pmat("bat-black", "#1E1E20", rough=0.6), pmat("bat-tin", "#C9CCD0", 1.0, 0.3)
L, W, T = 36.0, 19.6, 5.2
def add(o, m):
    o.data.materials.append(m); objs.append(o); return o
def rbox(name, x0, x1, y0, y1, z0, z1, m, r_long=0.0, r=0.0):
    """Box; r_long rounds the four edges running along Y, r softens the rest."""
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 if v.co.x < 0 else x1; v.co.y = y0 if v.co.y < 0 else y1; v.co.z = z0 if v.co.z < 0 else z1
    if r_long:
        along = [e for e in bm.edges if abs(e.verts[0].co.y - e.verts[1].co.y) > 1e-6]
        bmesh.ops.bevel(bm, geom=along, offset=r_long, segments=10, affect="EDGES", profile=0.5)
    if r:
        rest = [e for e in bm.edges if abs(e.verts[0].co.y - e.verts[1].co.y) < 1e-6 and e.calc_length() > r * 3]
        bmesh.ops.bevel(bm, geom=rest, offset=r, segments=2, affect="EDGES", profile=0.5)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    for p in me.polygons: p.use_smooth = True
    return add(o, m)
rbox("pouch", -W / 2, W / 2, 0, L - 4.0, 0, T, FOIL, r_long=2.2, r=0.3)
rbox("kapton", -W / 2 - 0.05, W / 2 + 0.05, L - 4.2, L, -0.05, T + 0.05, TAPE, r_long=2.25, r=0.3)
# printing on the top face, reading along the long axis
for i, (txt, dx) in enumerate((("PKCELL LP552035", -2.2), ("3.7V 350mAh", 2.2))):
    cu = bpy.data.curves.new(f"label{i}", "FONT"); cu.body = txt; cu.size = 2.6; cu.extrude = 0.01
    cu.align_x = "CENTER"; cu.align_y = "CENTER"
    o = bpy.data.objects.new(f"label{i}", cu); sc.collection.objects.link(o)
    o.location = (dx, (L - 4.0) / 2, T + 0.012); o.rotation_euler = (0, 0, math.pi / 2)
    bpy.context.view_layer.objects.active = o
    for other in bpy.context.selected_objects: other.select_set(False)
    o.select_set(True); bpy.ops.object.convert(target="MESH")
    o = bpy.context.view_layer.objects.active; o.select_set(False); add(o, INK)
# lead: two silicone wires out of the taped end, then a PH housing (same as the tactor wire lead's)
WIRE_LEN, OD, PITCH, z = bcfg.get("wire_len", 30.0), 1.4, 2.0, T / 2
for i, (x, m) in enumerate(((-PITCH / 2, RED), (PITCH / 2, BLK))):
    bpy.ops.mesh.primitive_cylinder_add(radius=OD / 2, depth=WIRE_LEN + 1.5, vertices=32,
                                        location=(x, L + (WIRE_LEN + 1.5) / 2 - 1.0, z), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object; o.name = f"bat-wire{i}"; bpy.ops.object.shade_smooth(); add(o, m)
Y0 = L + WIRE_LEN - 0.5
rbox("bat-ph-lip", -3.2, 3.2, Y0, Y0 + 0.9, z - 2.45, z + 2.45, NYL, r=0.15)
rbox("bat-ph-body", -3.0, 3.0, Y0 + 0.6, Y0 + 6.0, z - 2.25, z + 2.25, NYL, r=0.15)
rbox("bat-ph-latch", -1.2, 1.2, Y0 + 2.0, Y0 + 4.5, z + 2.25, z + 2.75, NYL, r=0.1)
