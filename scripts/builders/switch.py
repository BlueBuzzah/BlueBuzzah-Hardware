# Stand-in for the board's power switch SW1, a Korean Hroparts K3-1260D-L1 right-angle SPDT slide switch.
# The KiCad board assigns the C&K JS202011AQN (DPDT) 3D model to this footprint, so its second pin row hangs off the
# board edge; configs remove that model and build this one from the footprint's fab outline instead
# (footprint at KiCad 150.5, 79.55, no rotation; board STEP coords = KiCad (X, -Y); metres, like the board .glb).
# Body height 3.6 mm is approximate (no datasheet drawing available). Runs inside brender.py.
import bmesh
def pm(name, hexc, metal, rough):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    return m
SHELL, HANDLE, PIN = pm("sw-shell", "#B9BCC0", 1.0, 0.35), pm("sw-handle", "#1A1A1C", 0.0, 0.5), pm("sw-pin", "#C9CCD0", 1.0, 0.3)
FX, FY, TOP = 150.5, 79.55, 1.556
def sbox(name, lx0, lx1, ly0, ly1, z0, z1, mat, bevel=0.0):
    """Box in footprint-local KiCad mm (x right, y down), z in mm; placed in metres."""
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = (FX + (lx0 if v.co.x < 0 else lx1)) / 1000
        v.co.y = -(FY + (ly0 if v.co.y < 0 else ly1)) / 1000
        v.co.z = (z0 if v.co.z < 0 else z1) / 1000
    if bevel:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel / 1000, segments=3, affect="EDGES", profile=0.5)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.data.materials.append(mat); objs.append(o)
sbox("sw-body", -2.0, 7.0, -0.35, 2.39, TOP, TOP + 3.6, SHELL, bevel=0.12)
sbox("sw-handle", 0.74, 2.24, 2.39, 4.39, TOP + 1.05, TOP + 2.55, HANDLE, bevel=0.1)
for i, px in enumerate((0.0, 2.5, 5.0)):  # pins through the three plated holes
    sbox(f"sw-pin{i}", px - 0.25, px + 0.25, -0.4, 0.4, -1.4, TOP + 0.4, PIN)
