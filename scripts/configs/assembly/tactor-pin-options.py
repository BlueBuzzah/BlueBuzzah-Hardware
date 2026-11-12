# The three pin options, left to right: short (3.74 mm), standard (4.24 mm), long (4.74 mm).
# Only the long pin is in the tactor STEP file, so the meshes come from the pin STLs in the BlueBuzzah-Hardware
# repo's models/ ($HW, default: this checkout). Each STL is upright, centred on x/y, with its bottom at z 0.
import os, struct
hw = os.environ.get("HW", os.path.dirname(ENV["scripts"]))

def stl_mesh(path):
    d = open(path, "rb").read()
    vs, ts, index = [], [], {}
    for i in range(struct.unpack_from("<I", d, 80)[0]):
        tri = []
        for k in range(3):
            v = struct.unpack_from("<3f", d, 84 + i * 50 + 12 + k * 12)
            tri.append(index.setdefault(v, len(vs)))
            if tri[-1] == len(vs): vs.append(v)
        ts.append(tuple(tri))
    return vs, ts

for i, name in enumerate(("tactor-pin-1mm", "tactor-pin-0.5mm", "tactor-pin")):
    vs, ts = stl_mesh(os.path.join(hw, "models", name + ".stl"))
    me = bpy.data.meshes.new(name); me.from_pydata([(x + (i - 1) * 10.0, y, z) for x, y, z in vs], [], ts)
    me.update()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat(cfg["default"])); o["grp"] = name; objs.append(o)
    for p in me.polygons: p.use_smooth = False
