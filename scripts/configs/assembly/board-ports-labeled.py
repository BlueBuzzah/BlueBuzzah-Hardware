# Make each motor port's JST connector its own label group, so every callout sits beside its port.
# The board is turned 90 degrees clockwise, which puts the ports in a column on the right, port 1 at the top.
PORTS = {"JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal002": "port1", "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal": "port2",
         "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal003": "port3", "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal004": "port4",
         "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal001": "port5"}  # ...005 is the battery port
for o in objs:
    if o.name in PORTS:
        o["grp"] = PORTS[o.name]
