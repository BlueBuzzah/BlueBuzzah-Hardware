# Two tactors from the back: the wire plug half inserted (front left, 3.6 mm out) and fully inserted (back right, flush with
# the sled's back at y 11). The plug slides in along -y through the sled's back opening. Each plug carries the
# finished wiring from tactor-wire-plug-complete, mapped from that image's upside-down frame into the assembled
# frame (z -> 4 - z): copper in the underside pockets and side slots, insulation in the top notch, out the back.
import os
exec(open(os.path.join(ENV["scripts"], "configs", "assembly", "tactor_wiring.py")).read())
for grp, ox, oy in (("plug-half", 9, 3.6), ("plug-full", -9, 0)):
    wiring(ox, oy, grp)
