# The finger support sliding into the finger cup's dovetails (open at the cup's +y end), thicker end toward the
# shell, 11 mm short of the lid. The lid assembly is still 3 mm short of latched. Seen from the back.
import os
exec(open(os.path.join(ENV["scripts"], "configs", "assembly", "tactor_wiring.py")).read())
wiring(tail=40.0)  # runs on through the support's centre channel (under its bridge, |x| < 3, z < 5.4)
