# Make each motor port's JST connector its own label group, so every callout sits beside its port.
# The board is turned 90 degrees clockwise, which puts the ports in a column on the right, port 1 at the top.
PORTS = {"JST_S2B_PH_K002": "port1", "JST_S2B_PH_K": "port2",
         "JST_S2B_PH_K003": "port3", "JST_S2B_PH_K004": "port4",
         "JST_S2B_PH_K001": "port5"}  # ...005 is the battery port
for o in objs:
    if o.name in PORTS:
        o["grp"] = PORTS[o.name]
