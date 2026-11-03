# The LRA sled face down (motor and wired plug in) with one uncompressed spring in each pocket. Built in the
# assembled frame, where each spring stands on its pocket roof (z 3.9) and its free 5 mm reaches z -1.1, then the
# whole scene is turned over (180 degrees about Y) so the sled's underside and the springs face up.
import os
exec(open(os.path.join(ENV["scripts"], "configs", "assembly", "tactor_wiring.py")).read())
wiring()

flip = Matrix.Rotation(math.pi, 4, "Y")
for o in objs:
    o.matrix_world = flip @ o.matrix_world
