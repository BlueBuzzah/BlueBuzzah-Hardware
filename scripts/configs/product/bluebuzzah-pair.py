# Product shot: two finished gloves' electronics, each a closed case with 4 tactor leads (ports 2-5) running out of
# the back-wall wire opening to a finished tactor. Builds one tactor at the origin, then copies the case and tactor
# into place. The JST plugs, battery, antenna and screws sit under the closed upper shell, so they're left out.
import os
exec(open(os.path.join(ENV["scripts"], "configs", "assembly", "tactor_wiring.py")).read())
wiring(tail=27.0)  # stub to the finger support's far end; the long lead below continues it

CASE = ("lower-shell", "upper-shell", "switch", "pcb")
case = [o for o in objs if o["grp"] in CASE]
tactor = [o for o in objs if o["grp"] not in CASE]
tz = -min((o.matrix_world @ Vector(c)).z for o in tactor for c in o.bound_box)  # stand the tactor on z = 0

PORTS = (-8.8, 0.0, 8.8, 17.5)               # motor ports 2-5, case-frame x
SPREAD = ((-39, 102, 8), (-13, 113, 2.5), (13, 113, -2.5), (39, 102, -8))  # tactor x (from case centre), y, splay deg
CX = 4.35                                    # centre of ports 2-5
DEVICES = (-66.0, 66.0)                      # case x offsets
EXIT = Vector((1.0, 27.0, 3.29))             # tactor-frame insulation end (x = +-1)

def place(src, M, grp):
    for o in src:
        c = o.copy(); bpy.context.scene.collection.objects.link(c)
        c.matrix_world = M @ o.matrix_world; c["grp"] = grp; objs.append(c)

def lead(pts, grp):  # red/black pair side by side along a centre path
    for s, m in ((1, _m["wire0"]), (-1, _m["wire1"])):
        out = []
        for i, p in enumerate(pts):
            a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
            t = (b - a); t.z = 0; t.normalize()
            out.append(p + Vector((-t.y, t.x, 0)) * 0.55 * s)
        _tube(out, 0.55, m, grp)

for d, dx in enumerate(DEVICES):
    place(case, Matrix.Translation((dx, 0, 0)), f"case{d}")
    for i, (px, (sx, sy, splay)) in enumerate(zip(PORTS, SPREAD)):
        g = f"tactor{d}{i}"
        R = Matrix.Rotation(math.radians(180 + splay), 4, "Z")
        M = Matrix.Translation((dx + CX + sx, sy, tz)) @ R
        place(tactor, M, g)
        ax = (R @ Vector((0, 1, 0))).to_3d()  # tactor's +y (wire exit direction) in world
        tip = M @ Vector((0, 26.0, 3.29))
        x = dx + px
        pts = [Vector((x, 46.0, 10.0)), Vector((x, 50.5, 4.0)), Vector((x, 54.0, 1.8)), Vector((x, 64.0, 0.6)),
               (tip + ax * 14) * 0.5 + Vector((x, 64.0, 0.6)) * 0.5 + Vector((0, 0, 0.6 - ((tip + ax * 14).z + 0.6) / 2)),
               tip + ax * 9 - Vector((0, 0, tip.z - 0.8)), tip + ax * 3, tip]
        lead(pts, g)

for o in case + tactor:
    objs.remove(o); bpy.data.objects.remove(o)
