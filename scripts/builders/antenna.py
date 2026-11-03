# 2.4 GHz flexible PCB antenna (label: U4-WIFI-R-A0-HB): 30 x 12 x 1 mm black board, solder pad near the
# feed end, ~1.13 mm white coax leaving that end along -X to an IPEX1 (U.FL) plug. mm; board on z 0..1, long axis X.
# bcfg["cable_len"] shortens the cable so the part reads at image scale. Runs inside brender.py.
import bmesh, math
def pmat(name, hexc, metal=0.0, rough=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    return m
PCB, SILK = pmat("ant-board", "#1C1D1F", 0.0, 0.45), pmat("ant-silk", "#E9EAEC", 0.0, 0.6)
SOLDER, COAX, GOLD = pmat("ant-solder", "#C3C6CA", 1.0, 0.25), pmat("ant-coax", "#EEEDE8", 0.0, 0.5), pmat("ant-ufl", "#D6B56A", 1.0, 0.3)
L, W, T, OD = 30.0, 12.0, 1.0, 1.13
CABLE = bcfg.get("cable_len", 40.0)
def add(o, m):
    o.data.materials.append(m); objs.append(o); return o
def box(name, x0, x1, y0, y1, z0, z1, m, bevel=0.0):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 if v.co.x < 0 else x1; v.co.y = y0 if v.co.y < 0 else y1; v.co.z = z0 if v.co.z < 0 else z1
    if bevel: bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=2, affect="EDGES", profile=0.5)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); return add(o, m)
def cyl(name, r, depth, loc, rot, m, verts=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; bpy.ops.object.shade_smooth(); return add(o, m)
box("ant-board", 0, L, -W / 2, W / 2, 0, T, PCB, bevel=0.15)
FEED = 4.0  # solder pad centre, from the cable end
cyl("ant-pad", 1.1, 0.04, (FEED, 0, T + 0.02), (0, 0, 0), SOLDER)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.75, location=(FEED, 0, T + 0.2), segments=24, ring_count=12)
o = bpy.context.object; o.name = "ant-solder"; o.scale = (1.2, 1.0, 0.55); bpy.ops.object.shade_smooth(); add(o, SOLDER)
z = T + OD / 2
cyl("ant-coax", OD / 2, FEED + CABLE, ((FEED - CABLE) / 2, 0, z), (0, math.pi / 2, 0), COAX)
# IPEX1 / U.FL plug: square body with a round cap, cable entering from the side
x0 = -CABLE - 2.2
box("ant-ufl-body", x0, x0 + 2.2, -1.1, 1.1, z - 0.6, z, GOLD, bevel=0.08)
cyl("ant-ufl-cap", 0.95, 0.6, (x0 + 1.1, 0, z + 0.3), (0, 0, 0), GOLD)
# printed part number near the far end, reading along the long axis
cu = bpy.data.curves.new("ant-label", "FONT"); cu.body = "U4-WIFI-R-A0-HB"; cu.size = 1.6; cu.extrude = 0.01
cu.align_x = "RIGHT"; cu.align_y = "CENTER"
o = bpy.data.objects.new("ant-label", cu); sc.collection.objects.link(o); o.location = (L - 1.5, 3.0, T + 0.012)
bpy.context.view_layer.objects.active = o
for other in bpy.context.selected_objects: other.select_set(False)
o.select_set(True); bpy.ops.object.convert(target="MESH")
o = bpy.context.view_layer.objects.active; o.select_set(False); add(o, SILK)
