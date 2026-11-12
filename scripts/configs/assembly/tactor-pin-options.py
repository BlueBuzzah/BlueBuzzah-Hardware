# The three pin options, left to right: short (Pin-1mm, 3.74 mm), standard (Pin-.5mm, 4.24 mm), long (Pin, 4.74 mm).
# Only the long pin is in the tactor STEP file, so the meshes come from print files in the BlueBuzzah-Hardware
# repo ($HW, default: this checkout): BlueBuzzah-v3-parts.3mf, which has only the standard pin, then the short and
# long pins from the last committed BlueBuzzah-v3.3mf (read with git). Bottoms level at z 0.
import io, os, re, subprocess, zipfile
hw = os.environ.get("HW", os.path.dirname(ENV["scripts"]))
OLD_3MF = "69789d48de5698d5d098616ca1d1300a91644105:models/BlueBuzzah-v3.3mf"

def source(z):
    cfgx = z.read("Metadata/model_settings.config").decode()
    ids = dict((n, i) for i, n in re.findall(r'<part id="(\d+)"[^>]*>\s*<metadata key="name" value="(Pin[^"]*)"', cfgx))
    return ids, [z.read(n).decode() for n in z.namelist() if n.startswith("3D/Objects/")]

old = subprocess.run(["git", "-C", hw, "show", OLD_3MF], check=True, capture_output=True).stdout
sources = [source(zipfile.ZipFile(os.path.join(hw, "models", "BlueBuzzah-v3-parts.3mf"))),
           source(zipfile.ZipFile(io.BytesIO(old)))]

def pin_mesh(name):
    ids, models = next(s for s in sources if name in s[0])
    pid = ids[name]
    for s in models:
        m = re.search(r'<object id="%s"[^>]*>(.*?)</object>' % pid, s, re.S)
        if m and "<vertex" in m.group(1):
            vs = [tuple(map(float, v)) for v in re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"', m.group(1))]
            ts = [tuple(map(int, t)) for t in re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', m.group(1))]
            return vs, ts

for i, name in enumerate(("Pin-1mm", "Pin-.5mm", "Pin")):
    vs, ts = pin_mesh(name)
    z0 = min(v[2] for v in vs)
    me = bpy.data.meshes.new(name); me.from_pydata([(x + (i - 1) * 10.0, y, zz - z0) for x, y, zz in vs], [], ts)
    me.update()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat(cfg["default"])); o["grp"] = name; objs.append(o)
    for p in me.polygons: p.use_smooth = False
