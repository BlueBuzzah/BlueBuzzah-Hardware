# Website hero renders. The pair from bluebuzzah-pair.py, spread to make room for a phone
# showing BuzzahBuddy's Session screen (unless "no_phone"); perspective camera, studio light, shadow catcher; renders itself.
import os, bmesh
src = open(os.path.join(ENV["scripts"], "configs", "product", "bluebuzzah-pair.py")).read()
src = src.replace("DEVICES = (-66.0, 66.0)", f"DEVICES = {tuple(cfg.get('devices', [-104.0, 104.0]))}")
exec(src)

# ---- phone: rounded slab, bezel and screen, lying flat in front, centred between the cases (skipped with "no_phone")
if not cfg.get("no_phone"):
    PW, PH, PT, PR = 71.5, 147.0, 7.8, 10.0   # generic phone, mm
    PX, PY, PROT = cfg.get("phone", [0.0, 52.0, 0.0])
    def rrect(w, h, r, n=10):
        pts = []
        for cx, cy, a0 in ((w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90), (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)):
            for k in range(n + 1):
                a = math.radians(a0 + 90 * k / n); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        return pts
    def slab(name, pts, z0, z1, material, uv=None):
        bm = bmesh.new()
        bot = [bm.verts.new((x, y, z0)) for x, y in pts]; top = [bm.verts.new((x, y, z1)) for x, y in pts]
        ft = bm.faces.new(top); bm.faces.new(list(reversed(bot)))
        for i in range(len(pts)):
            j = (i + 1) % len(pts); bm.faces.new((bot[i], bot[j], top[j], top[i]))
        if uv:
            lay = bm.loops.layers.uv.new()
            for l in ft.loops: l[lay].uv = uv(l.vert.co)
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(material); o["grp"] = "phone"; objs.append(o)
        o.matrix_world = Matrix.Translation((PX, PY, 0)) @ Matrix.Rotation(math.radians(PROT), 4, "Z")
        return o

    def pbr(h, rough, metal=0.0, coat=0.0):
        m = bpy.data.materials.new(h + "x"); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = lin(h); b.inputs["Roughness"].default_value = rough
        b.inputs["Metallic"].default_value = metal; b.inputs["Coat Weight"].default_value = coat
        return m
    frame = slab("phone-body", rrect(PW, PH, PR), 0.0, PT, pbr("#2B3140", 0.35, 0.8))
    glass = slab("phone-glass", rrect(PW - 1.6, PH - 1.6, PR - 0.8), PT, PT + 0.25, pbr("#05070D", 0.08, 0.0, 1.0))
    SW, SH = 66.0, 66.0 * 2622 / 1206                 # screen keeps the screenshot's aspect
    scr = bpy.data.materials.new("screen"); scr.use_nodes = True; nt = scr.node_tree
    img = nt.nodes.new("ShaderNodeTexImage"); img.image = bpy.data.images.load(cfg["screen"]); img.interpolation = "Cubic"
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = cfg.get("screen_glow", 1.0)
    gl = nt.nodes.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.05
    mix = nt.nodes.new("ShaderNodeMixShader"); mix.inputs[0].default_value = 0.06
    nt.links.new(img.outputs["Color"], em.inputs["Color"]); nt.links.new(em.outputs[0], mix.inputs[1])
    nt.links.new(gl.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    slab("phone-screen", rrect(SW, SH, 7.5), PT + 0.25, PT + 0.26, scr,
         uv=lambda co: (co.x / SW + 0.5, co.y / SH + 0.5))

# ---- shadow catcher ground
bpy.ops.mesh.primitive_plane_add(size=2000, location=(0, 60, 0))
gnd = bpy.context.active_object; gnd.is_shadow_catcher = True

# --info and model export leave the scene to brender; only a plain run renders here
if not os.environ.get("BB_MODE"):
    # ---- perspective camera aimed at the scene centre, distance fitted to the bounds
    sc = bpy.context.scene
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    ctr = sum(pts, Vector()) / len(pts) + Vector(cfg.get("aim", [0, 0, 0]))
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.lens = cfg.get("lens", 85); cam.data.clip_end = 100000
    d = Vector(cfg.get("camdir", [0.22, -1.0, 0.95])).normalized()
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    R = sc.render; R.resolution_x = cfg["w"]; R.resolution_y = round(cfg["w"] / cfg.get("aspect", 1.6))
    from bpy_extras.object_utils import world_to_camera_view
    dist = 400.0
    for _ in range(30):  # grow/shrink until the content fills the frame with the margin
        cam.location = ctr + d * dist; bpy.context.view_layer.update()
        v = [world_to_camera_view(sc, cam, p) for p in pts]
        span = max(max(q.x for q in v) - min(q.x for q in v), max(q.y for q in v) - min(q.y for q in v))
        dist *= span / (1 - 2 * cfg.get("margin", 0.05))
    cam.location = ctr + d * dist; bpy.context.view_layer.update()
    v = [world_to_camera_view(sc, cam, p) for p in pts]
    cam.data.shift_x = ((max(q.x for q in v) + min(q.x for q in v)) / 2 - 0.5) * (1 if R.resolution_x >= R.resolution_y else R.resolution_x / R.resolution_y)
    cam.data.shift_y = ((max(q.y for q in v) + min(q.y for q in v)) / 2 - 0.5) * (R.resolution_y / R.resolution_x if R.resolution_x >= R.resolution_y else 1)

    # ---- studio light: big soft key (front-left, high), cool rim from behind, faint world fill
    world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = lin("#C9D6F2")
    world.node_tree.nodes["Background"].inputs[1].default_value = cfg.get("fill", 0.35)
    def area(name, loc, energy, size, color):
        L = bpy.data.lights.new(name, "AREA"); L.energy = energy; L.size = size; L.color = lin(color)[:3]
        o = bpy.data.objects.new(name, L); sc.collection.objects.link(o); o.location = loc
        o.rotation_euler = (ctr - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    k = cfg.get("key", 1.0)
    area("key", ctr + Vector((-260, -320, 420)), 9.0e7 * k, 380, "#FFF6EC")
    area("rim", ctr + Vector((120, 520, 160)), 6.0e7 * k, 300, "#8FB6FF")
    area("kick", ctr + Vector((420, -60, 140)), 2.0e7 * k, 200, "#DDE7FF")

    R.engine = "CYCLES"; sc.cycles.samples = int(os.environ.get("BB_SAMPLES", cfg.get("samples", 256)))
    sc.cycles.use_denoising = True; sc.cycles.device = "GPU"
    R.film_transparent = True
    sc.view_settings.view_transform = cfg.get("view", "AgX"); sc.view_settings.look = cfg.get("look", "None")
    R.image_settings.file_format = "PNG"; R.image_settings.color_mode = "RGBA"
    R.filepath = cfg["out"]; os.makedirs(os.path.dirname(cfg["out"]), exist_ok=True)
    bpy.ops.render.render(write_still=True)

    # The soft shadows spread past the parts, so the frame would cut them with a hard edge. Fade the alpha to 0 over the
    # outer "fade" fraction of the shorter side (smoothstep); "margin" keeps the parts themselves clear of that band.
    import numpy as np
    im = bpy.data.images.load(cfg["out"]); w, h = im.size
    px = np.array(im.pixels[:], dtype=np.float32).reshape(h, w, 4)
    band = cfg.get("fade", 0.12) * min(w, h)
    ramp = lambda n: (lambda t: t * t * (3 - 2 * t))(np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / band, 0, 1))
    px[:, :, 3] *= ramp(h)[:, None] * ramp(w)[None, :]
    im.pixels[:] = px.ravel(); im.filepath_raw = cfg["out"]; im.file_format = "PNG"; im.save()
    print("INFO rendered", cfg["out"])
    raise SystemExit
