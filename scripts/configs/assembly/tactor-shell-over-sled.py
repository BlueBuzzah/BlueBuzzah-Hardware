# Before the flip: the LRA sled face down with its springs (as in tactor-springs-on-sled), and the shell upside
# down, held 14 mm above it with its spring pins over the springs and its wire notch on the wire side.
# Built in the assembled frame (shell lowered 14 mm, springs uncompressed), then turned over about Y.
import os
exec(open(os.path.join(ENV["scripts"], "configs", "assembly", "tactor_wiring.py")).read())
wiring()
flip = Matrix.Rotation(math.pi, 4, "Y")
for o in objs:
    o.matrix_world = flip @ o.matrix_world
