# BlueBuzzah v3 board (ESP32-S3-WROOM-1U) render fixes, from PCB/v3/kicad/BlueBuzzah_v3.step. Runs inside brender.py.

# Blue solder mask: recolour the board body's material (KiCad exports it green).
for m in bpy.data.objects["BlueBuzzah_v3_PCB"].data.materials:
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = lin("#1F4FA0")

# USB-C J10: the KiCad library has no 3D model for HRO TYPE-C-31-M-12, so the board STEP has no connector there.
# models/USB_C_Receptacle_HRO_TYPE-C-31-M-12.step (KiCad RoyalBlue54L demo, CERN-OHL-P v2) is already in the
# footprint's frame; place it on the footprint (KiCad 142, 79.6, no rotation; board STEP = KiCad X, -Y; parts sit
# on z 1.6 mm; metres, like the board .glb). Skipped once the board STEP carries the connector itself.
if not any("TYPE-C-31" in o.name for o in bpy.data.objects):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(ENV["work"], "pcb", "usb-c.glb"))
    for o in [o for o in bpy.data.objects if o not in before and o.type == "MESH"]:
        mw = o.matrix_world.copy(); o.parent = None
        o.matrix_world = Matrix.Translation((0.142, -0.0796, 0.0016)) @ mw
        o["grp"] = "glb"; objs.append(o)

# ESP32-S3 module shield (and its U.FL socket): the model's near-white becomes metallic silver-grey.
silver = bpy.data.materials.new("wroom-shield"); silver.use_nodes = True
sb = silver.node_tree.nodes["Principled BSDF"]
sb.inputs["Base Color"].default_value = lin("#A4A8AE"); sb.inputs["Metallic"].default_value = 0.6
sb.inputs["Roughness"].default_value = 0.45
for o in bpy.data.objects:
    if o.type == "MESH" and "WROOM" in o.name:
        for i, m in enumerate(o.data.materials):
            if m and m.use_nodes and min(m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value[:3]) > 0.6:
                o.data.materials[i] = silver
