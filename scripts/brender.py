# Headless Blender render / model export for one config.
#   blender -b -P brender.py -- configs/<folder>/<name>.json
# Config strings may use {scripts}, {work} and {out}, filled from the SCRIPTS, WORK and OUT environment
# variables that render_all.py sets. BB_SAMPLES overrides the sample count (quick previews);
# BB_MODE=model exports the scene to cfg["model"] as .glb instead of rendering.
import bpy, json, sys, os, math
from mathutils import Vector, Matrix

ENV = {"scripts": os.environ.get("SCRIPTS", os.path.dirname(os.path.abspath(__file__))),
       "work": os.environ.get("WORK", "/tmp"), "out": os.environ.get("OUT", ".")}

def fill(v):
    if isinstance(v, str): return v.format(**ENV)
    if isinstance(v, list): return [fill(x) for x in v]
    if isinstance(v, dict): return {k: fill(x) for k, x in v.items()}
    return v

cfg = fill(json.load(open(sys.argv[sys.argv.index("--") + 1])))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def lin(h):  # hex sRGB -> linear RGBA (Blender material inputs are linear)
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1]

mats = {}
def mat(h):
    if h not in mats:
        m = bpy.data.materials.new(h); m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = lin(h)
        b.inputs["Roughness"].default_value = cfg.get("rough", 0.55)
        b.inputs["Specular IOR Level"].default_value = cfg.get("spec", 0.25)
        mats[h] = m
    return mats[h]

objs = []

# 1. A colored model (.glb), optionally with some of its objects removed and the whole model moved
if "glb" in cfg:
    bpy.ops.import_scene.gltf(filepath=cfg["glb"])
    for name in cfg.get("remove", []):  # drop wrong models from the file
        bpy.data.objects.remove(bpy.data.objects[name])
    glb_meshes = [o for o in sc.objects if o.type == "MESH"]
    if "glb_loc" in cfg:  # move the whole model: unparent (keep world pose), then translate
        for o in glb_meshes:
            mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
            o.location = o.location + Vector(cfg["glb_loc"])
    for o in glb_meshes:
        o["grp"] = cfg.get("glb_group", "glb")
    objs += glb_meshes

# 1b. The finished models (models/GLB/*.glb, in metres), scaled to mm and placed as
#     Translate(loc) . RotateZ . RotateY . RotateX (rot, degrees) . Scale; "hide" drops objects by name prefix,
#     "color" recolours the whole part. Each part is one label group, named by "name" (default: the model name).
MODELS = os.environ.get("MODELS", os.path.join(os.path.dirname(ENV["scripts"]), "models", "GLB"))
for p in cfg.get("models", []):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(MODELS, p["model"] + ".glb"))
    new = [o for o in bpy.data.objects if o not in before]
    keep = [o for o in new if o.type == "MESH" and not any(o.name.startswith(h) for h in p.get("hide", []))]
    pose = {o: o.matrix_world.copy() for o in keep}
    for o in new:
        if o not in pose:
            bpy.data.objects.remove(o)
    rx, ry, rz = (math.radians(a) for a in p.get("rot", [0, 0, 0]))
    T = (Matrix.Translation(p.get("loc", [0, 0, 0])) @ Matrix.Rotation(rz, 4, "Z") @ Matrix.Rotation(ry, 4, "Y")
         @ Matrix.Rotation(rx, 4, "X") @ Matrix.Scale(p.get("scale", 1.0) * 1000, 4))
    for o, mw in pose.items():
        o.parent = None; o.matrix_world = T @ mw
        o["grp"] = p.get("name", p["model"])
        if "color" in p:
            o.data.materials.clear(); o.data.materials.append(mat(p["color"]))
    objs += list(pose)

# 2. Models built in code (builders/*.py); optional placement: scale, rotate about Z, then move
for bd in cfg.get("builds", []):
    n0 = len(objs)
    bcfg = bd.get("cfg", {})
    exec(open(bd["file"]).read())
    if bd.get("xform"):
        bx = bd["xform"]
        T = (Matrix.Translation(bx.get("loc", [0, 0, 0])) @ Matrix.Rotation(math.radians(bx.get("rot_z", 0)), 4, "Z")
             @ Matrix.Scale(bx.get("scale", 1.0), 4))
        for o in objs[n0:]:
            o.matrix_world = T @ o.matrix_world
    for o in objs[n0:]:
        o["grp"] = bd.get("group", os.path.basename(bd["file"])[:-3])

# 3. STL parts from a folder (one file per part, named after the part)
for f in (sorted(os.listdir(cfg["parts"])) if "parts" in cfg else []):
    name = f[:-4].replace("_", " ")
    if "only" in cfg and name not in cfg["only"]:
        continue
    bpy.ops.wm.stl_import(filepath=os.path.join(cfg["parts"], f))
    o = bpy.context.selected_objects[0]; o.name = name
    bpy.ops.object.shade_smooth_by_angle(angle=0.6)
    o.location = Vector(cfg.get("offsets", {}).get(name, [0, 0, 0]))
    o["grp"] = cfg.get("part_groups", {}).get(name, name)
    if "stl_scale" in cfg:  # e.g. mm STLs next to a metre-based GLB
        o.scale = (cfg["stl_scale"],) * 3
    if name in cfg.get("mats", {}):  # per-part [hex, metallic, roughness]
        h, metal, rough = cfg["mats"][name]
        m = bpy.data.materials.new(name); m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = lin(h)
        b.inputs["Metallic"].default_value = metal
        b.inputs["Roughness"].default_value = rough
        o.data.materials.append(m)
    else:
        o.data.materials.append(mat(cfg.get("colors", {}).get(name, cfg.get("default", "#4A5468"))))
    objs.append(o)
bpy.context.view_layer.update()

# 4. Optional hook: Python run with this script's names in scope (bpy, objs, lin, mat, Vector, Matrix, math, cfg).
#    It can move, delete or add geometry; tag new objects with o["grp"] and append them to objs.
if cfg.get("hook"):
    exec(open(cfg["hook"]).read())
    objs = [o for o in objs if o.name in bpy.data.objects]
    bpy.context.view_layer.update()

if os.environ.get("BB_MODE") == "info":  # print each group's objects and world bounds (scene units), no render
    def bb(group):
        pts = [o.matrix_world @ Vector(c) for o in group for c in o.bound_box]
        return tuple(round(min(p[i] for p in pts), 2) for i in range(3)), tuple(round(max(p[i] for p in pts), 2) for i in range(3))
    for tag in dict.fromkeys(o.get("grp") for o in objs):
        group = [o for o in objs if o.get("grp") == tag]
        print("INFO group", repr(tag), *bb(group))
        for o in group:
            print("INFO   obj", repr(o.name), *bb([o]))
    raise SystemExit

if os.environ.get("BB_MODE") == "model":  # save the scene as .glb (scene units are mm unless model_scale says otherwise)
    k = cfg.get("model_scale", 0.001)
    if k != 1:
        for o in objs:
            o.matrix_world = Matrix.Scale(k, 4) @ o.matrix_world
    for o in sc.objects: o.select_set(o in objs)
    os.makedirs(os.path.dirname(cfg["model"]), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=cfg["model"], export_format="GLB", use_selection=True, export_apply=True)
    raise SystemExit

# Orthographic camera along cfg["dir"], framed to the parts' bounds; image height follows the content
d = Vector(cfg["dir"]).normalized()
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam)
cam.data.type = "ORTHO"; sc.camera = cam
pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
ctr = sum(pts, Vector()) / len(pts)
cam.location = ctr + d * 500; cam.data.clip_end = 2000
cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
bpy.context.view_layer.update()
inv = cam.matrix_world.inverted()
loc = [inv @ p for p in pts]
xs, ys = [p.x for p in loc], [p.y for p in loc]
w, h = max(xs) - min(xs), max(ys) - min(ys)
R = sc.render; R.resolution_x = cfg["w"]
R.resolution_y = round(cfg["w"] * h / w)
cam.data.ortho_scale = max(w, h) * (1 + 2 * cfg.get("margin", 0.06))  # spans the larger image side
cam.data.shift_x = ((max(xs) + min(xs)) / 2) / cam.data.ortho_scale
cam.data.shift_y = ((max(ys) + min(ys)) / 2) / cam.data.ortho_scale

# Lighting: soft uniform world fill + one soft key light
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes["Background"]; bg.inputs[0].default_value = (1, 1, 1, 1)
bg.inputs[1].default_value = cfg.get("fill", 0.8)
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sc.collection.objects.link(sun)
sun.data.energy = cfg.get("key", 1.2); sun.data.angle = 0.5
sun.rotation_euler = Vector(cfg.get("keydir", [-0.4, -0.6, 1])).normalized().to_track_quat("Z", "Y").to_euler()

R.engine = "CYCLES"; sc.cycles.samples = int(os.environ.get("BB_SAMPLES", cfg.get("samples", 96)))
sc.cycles.use_denoising = True
sc.cycles.device = "GPU" if cfg.get("gpu", True) else "CPU"
R.film_transparent = True
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
R.image_settings.file_format = "PNG"; R.image_settings.color_mode = "RGBA"
R.filepath = cfg["out"]
os.makedirs(os.path.dirname(cfg["out"]), exist_ok=True)
bpy.ops.render.render(write_still=True)

# Pixel bounds of each part and group, for placing labels over the image (written to {work}/bounds/)
from bpy_extras.object_utils import world_to_camera_view
def measure(group, frac=0.5):
    """Pixel bounds, plus the silhouette's right edge across the label strip (frac of the height ± band px)."""
    p, edges = [], []
    for o in group:
        n = len(p)
        p += [world_to_camera_view(sc, cam, o.matrix_world @ v.co) for v in o.data.vertices]
        edges += [(n + e.vertices[0], n + e.vertices[1]) for e in o.data.edges]
    y0, y1 = min(q.y for q in p), max(q.y for q in p); cy = y1 - (y1 - y0) * frac  # frac: 0 = top, 1 = bottom
    hb = cfg.get("band", 0) / R.resolution_y; ya, yb = cy - hb, cy + hb
    xr = max([q.x for q in p if ya <= q.y <= yb] + [0.0])
    for i, j in edges:
        a, b = p[i], p[j]
        for yl in (ya, yb, cy):
            if (a.y - yl) * (b.y - yl) <= 0 and a.y != b.y:
                xr = max(xr, a.x + (yl - a.y) / (b.y - a.y) * (b.x - a.x))
    return [min(q.x for q in p) * R.resolution_x, (1 - y1) * R.resolution_y,
            max(q.x for q in p) * R.resolution_x, (1 - y0) * R.resolution_y,
            xr * R.resolution_x, (1 - cy) * R.resolution_y]

if "labels" in cfg:
    boxes = {}
    for tag in {o.get("grp") for o in objs if o.get("grp")}:
        boxes[tag] = measure([o for o in objs if o.get("grp") == tag], cfg.get("anchor", {}).get(tag, 0.5))
    bounds = os.path.join(ENV["work"], "bounds", os.path.basename(cfg["out"]) + ".json")
    os.makedirs(os.path.dirname(bounds), exist_ok=True)
    json.dump({"w": R.resolution_x, "h": R.resolution_y, "parts": boxes}, open(bounds, "w"), indent=1)
