# Tactor wire lead: JST PH 2-pin female connector lead (PHR-2 housing, 2.0 mm pitch) on 26 AWG wire; mm,
# tactor axes. Bare ends at y=0 (toward the wire plug), wires run +Y, housing mating face points +Y (away from the plug).
# The real lead is longer; bcfg["wire_len"] shortens it so the part reads at image scale. Runs inside brender.py.
import bmesh, math
def pmat(name, hexc, metal=0.0, rough=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    return m
NYLON, RED, BLACK = pmat("ph-nylon", "#F1EFE8", rough=0.55), pmat("wire-red", "#D22B22", rough=0.6), pmat("wire-black", "#1E1E20", rough=0.6)
COPPER, TIN = pmat("copper", "#C8794A", 1.0, 0.35), pmat("tin", "#C9CCD0", 1.0, 0.3)
PITCH, WIRE_OD, CU_D, STRIP = 2.0, 1.1, 0.4, 5.0  # 26 AWG: two wires side by side fill the wire plug's 2.2 mm notch
WIRE_LEN = bcfg.get("wire_len", 30.0)
HW, HH, HL = 6.0, 4.5, 6.0  # housing width (X), height (Z), length (Y)
Y0 = STRIP + WIRE_LEN        # housing rear face
def link(o, mat):
    o.data.materials.append(mat); objs.append(o); return o
def cyl(name, r, y0, y1, x, z, mat, verts=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=y1 - y0, vertices=verts,
                                        location=(x, (y0 + y1) / 2, z), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object; o.name = name; bpy.ops.object.shade_smooth(); return link(o, mat)
def box(name, x0, x1, y0, y1, z0, z1, mat, bevel=0.0):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 if v.co.x < 0 else x1; v.co.y = y0 if v.co.y < 0 else y1; v.co.z = z0 if v.co.z < 0 else z1
    if bevel: bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=2, affect="EDGES", profile=0.5)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); return link(o, mat)
zc = WIRE_OD / 2  # wires rest on z = 0
for i, (x, insul) in enumerate(((-PITCH / 2, RED), (PITCH / 2, BLACK))):
    cyl(f"wire{i}", WIRE_OD / 2, STRIP, Y0 + 0.5, x, zc, insul)
    cyl(f"bare{i}", CU_D / 2, 0.0, STRIP + 0.2, x, zc, COPPER, 16)
# housing: body + rear lip + latch ramp, centred on the wires
zb = zc - HH / 2
body = box("ph-housing", -HW / 2, HW / 2, Y0 + 0.6, Y0 + HL, zb, zb + HH, NYLON, bevel=0.15)
box("ph-lip", -HW / 2 - 0.2, HW / 2 + 0.2, Y0, Y0 + 0.9, zb - 0.2, zb + HH + 0.2, NYLON, bevel=0.15)
box("ph-latch", -1.2, 1.2, Y0 + 2.0, Y0 + 4.5, zb + HH, zb + HH + 0.5, NYLON, bevel=0.1)
for i, x in enumerate((-PITCH / 2, PITCH / 2)):  # contact openings in the mating face, with a tin contact inside
    cut = box(f"cut{i}", x - 0.6, x + 0.6, Y0 + HL - 3.0, Y0 + HL + 1.0, zc - 0.6, zc + 0.6, NYLON)
    mod = body.modifiers.new(f"hole{i}", "BOOLEAN"); mod.operation = "DIFFERENCE"; mod.object = cut; mod.solver = "EXACT"
    bpy.context.view_layer.objects.active = body; bpy.ops.object.modifier_apply(modifier=mod.name)
    objs.remove(cut); bpy.data.objects.remove(cut)
    box(f"contact{i}", x - 0.25, x + 0.25, Y0 + HL - 3.0, Y0 + HL - 1.2, zc - 0.25, zc + 0.25, TIN)
