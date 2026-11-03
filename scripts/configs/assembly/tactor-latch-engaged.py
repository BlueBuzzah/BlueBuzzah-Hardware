# Everything seated: the lid's latching tab snapped over the front edge of the shell. Framed on the tab with a
# hidden box around it; the rest of the tactor runs off the edges.
import os
exec(open(os.path.join(ENV["scripts"], "configs", "assembly", "tactor_wiring.py")).read())
wiring()
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -10.5, 4.0)); box = bpy.context.object
box.scale = (22, 9, 9); box.hide_render = True; box["grp"] = "frame"
objs[:] = [box]
