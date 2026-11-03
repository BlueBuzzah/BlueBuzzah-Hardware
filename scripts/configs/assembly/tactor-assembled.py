# The finished tactor: shell, sled, springs, motor and wired plug inside, lid assembly latched, finger support in.
import os
exec(open(os.path.join(ENV["scripts"], "configs", "assembly", "tactor_wiring.py")).read())
wiring(tail=46.0)  # runs under the finger support's bridge and out its far end
