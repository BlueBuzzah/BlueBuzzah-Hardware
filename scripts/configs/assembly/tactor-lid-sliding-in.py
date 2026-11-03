# The lid assembly mostly seated but not latched: 3 mm short, so the latching tab hasn't reached the shell's
# front lip yet.
import os
exec(open(os.path.join(ENV["scripts"], "configs", "assembly", "tactor_wiring.py")).read())
wiring()
