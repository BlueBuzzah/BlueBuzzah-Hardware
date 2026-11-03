# Two straps, one through each pair of strap loops. Each loop is a tunnel from the side wall down to an opening in the
# underside (measured at y 10: it rises from x -27..-24 at z 0 to x -29.5, z 4.4-7.5), so a strap runs under the case,
# up through the loop on each side, and down around the hand. Ends cut short; there is no glove model.
import bmesh
T, W = 1.2, 12.0  # strap thickness and width, mm (loops are 15 mm long)
half = [(-25.5, 0.0), (-25.9, 2.0), (-27.0, 4.0), (-28.6, 5.6), (-30.6, 5.6), (-32.6, 4.2), (-33.8, 1.0), (-34.2, -12.0)]
path = [(x, z) for x, z in reversed(half)] + [(-24.0, -0.9), (24.0, -0.9)] + [(-x, z) for x, z in half]
def smooth(p, n=6):  # Catmull-Rom through the points
    out = []
    for i in range(len(p) - 1):
        p0, p1, p2, p3 = p[max(i - 1, 0)], p[i], p[i + 1], p[min(i + 2, len(p) - 1)]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t * t + (-a + 3 * b - 3 * c + d) * t ** 3)
                             for a, b, c, d in zip(p0, p1, p2, p3)))
    return out + [p[-1]]
strap = mat("#80838A")  # mid grey: reads on light and dark pages
for yc in (9.5, 36.5):  # loop centres (y 2-17 and 29-44)
    pts = smooth(path)
    me = bpy.data.meshes.new("strap"); bm = bmesh.new()
    rows = [(bm.verts.new((x, yc - W / 2, z)), bm.verts.new((x, yc + W / 2, z))) for x, z in pts]
    for (a, b), (c, d) in zip(rows, rows[1:]):
        bm.faces.new((a, b, d, c))
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("strap", me); bpy.context.scene.collection.objects.link(o)
    sol = o.modifiers.new("t", "SOLIDIFY"); sol.thickness = T; sol.offset = 0
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier="t")
    for f in o.data.polygons: f.use_smooth = True
    o.data.materials.append(strap); o["grp"] = "strap"; objs.append(o)
