# VLV101040A LRA motor, modelled from the datasheet drawing (mm). Can centred at the origin, flex tail along +X.
# Runs inside brender.py (uses bpy, sc, objs, lin).
import bmesh

def pmat(name, hexc, metal=0.0, rough=0.5, trans=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    b.inputs["Transmission Weight"].default_value = trans
    return m

STEEL = pmat("steel", "#9C9E9C", metal=1.0, rough=0.5)
PORON = pmat("poron", "#202022", rough=0.95)
FLEX  = pmat("flex", "#C07A22", rough=0.35)
GOLD  = pmat("gold", "#D8C083", metal=0.85, rough=0.45)
GLUE  = pmat("glue", "#B98A45", rough=0.2)

def box(name, x0, x1, y0, y1, z0, z1, mat, corner=0.0, top=0.0, seg=6):
    """Box with rounded vertical corners (corner) and rounded top edges (top)."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 if v.co.x < 0 else x1
        v.co.y = y0 if v.co.y < 0 else y1
        v.co.z = z0 if v.co.z < 0 else z1
    if corner:
        vert = [e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) > 1e-6]
        bmesh.ops.bevel(bm, geom=vert, offset=corner, segments=seg, affect="EDGES", profile=0.5)
    if top:
        tops = [e for e in bm.edges if all(abs(v.co.z - z1) < 1e-6 for v in e.verts)
                and len(e.link_faces) == 2 and not all(abs(v.co.z - z1) < 1e-6 for f in e.link_faces for v in f.verts)]
        bmesh.ops.bevel(bm, geom=tops, offset=top, segments=seg, affect="EDGES", profile=0.5)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    o.data.materials.append(mat)
    for p in me.polygons: p.use_smooth = True
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=0.6); o.select_set(False)
    objs.append(o); return o

H = 3.8  # can height; the Poron pad adds 0.25 for the 4.05 overall
box("can",   -5, 5, -5, 5, 0, H, STEEL, corner=1.0, top=0.22)
box("poron", -4.5, 4.5, -4.5, 4.5, H, H + 0.25, PORON, corner=0.7)
# base-plate tab on the side opposite the tail
bpy.ops.mesh.primitive_cylinder_add(radius=2.2, depth=0.3, location=(-5, 0, 0.15), vertices=64)
t = bpy.context.object; t.data.materials.append(STEEL); objs.append(t)
# flex tail: steel stiffener, amber polyimide, two gold pads (13.9 overall, 5.7 wide)
box("stiffener", 4.6, 8.9, -2.85, 2.85, 0, 0.2, STEEL, corner=0.25)
box("flex",      4.6, 8.75, -2.6, 2.6, 0.2, 0.33, FLEX, corner=0.3)
box("pad_a", 6.0, 8.5,  0.2, 2.35, 0.33, 0.35, GOLD, corner=0.2)
box("pad_b", 6.0, 8.5, -2.35, -0.2, 0.33, 0.35, GOLD, corner=0.2)
# glue bead where the flex leaves the can
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.75, location=(5.0, 0, 0.33), segments=48, ring_count=24)
g = bpy.context.object; g.scale = (1.0, 1.6, 1.0); bpy.ops.object.shade_smooth()
g.data.materials.append(GLUE); objs.append(g)
