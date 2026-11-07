# Ordering assembled boards from PCBWay

Use the three order files in this folder together, unchanged. They describe one bare board with no panel. The JLCPCB files in the parent folder are a separate package, so don't mix the two.

| File | Description |
| --- | --- |
| `BlueBuzzah_v3_gerbers.zip` | Gerber and drill files for one board |
| `BlueBuzzah_v3_BOM.csv` | Bill of materials in PCBWay's template, with manufacturer part numbers and LCSC numbers |
| `BlueBuzzah_v3_centroid.csv` | Placement of the 76 SMT parts, in mm from the board's lower-left corner |

## Placing the Order

1. Start a PCB order, upload `BlueBuzzah_v3_gerbers.zip`, and enter these values:

   | Option | Value |
   | --- | --- |
   | Board type | Single pieces |
   | Layers | 2 |
   | Size | 42 × 42 mm |
   | Material | FR-4 |
   | Thickness | 1.6 mm |
   | Finished copper | 1 oz |
   | Minimum track and spacing | 4 mil (0.1 mm) |
   | Minimum hole | 0.2 mm |
   | Solder mask | Blue |
   | Silkscreen | White |
   | Surface finish | Immersion gold(ENIG) |

   The Gerbers don't carry color or finish, so these values have to be set on the order.

2. Turn on assembly, choose turnkey, and assemble the top side. The board has 76 SMT parts and 7 through-hole parts (J1 to J6 and SW1).
3. Upload `BlueBuzzah_v3_BOM.csv` and `BlueBuzzah_v3_centroid.csv`.
4. Add the panel note below to the order.
5. Review the production files PCBWay sends before approving them. The centroid uses KiCad's rotations, and `Pad X` and `Pad Y` give each part's pin 1. Check D1, D2, D11, U1 and the SOT-23 parts in particular. D2's cathode (pad 1) belongs at the closed end of the silkscreen outline, toward the bottom of the board.

U1's pads are 0.15 mm apart, under PCBWay's 0.19 mm minimum for a solder mask dam in blue or green, so expect them to propose one open mask area across those pads. The motor drivers and USB-C connector, at 0.2 mm, are within the limit.

U21 pad 2 and U23 pad 2 each have a 0.2 mm via in the pad, because neither has room to move it. They're unfilled, like the board's other vias, so tell PCBWay they're intentional if it asks.

The BOM's notes list checked alternates for D1, C17, R60, R61, R64, R67 and R68, and allow any 1% 0402 equivalent for every resistor. For any other part PCBWay can't source, change it in `make_pcbway.py` and rebuild, so the files stay correct for the next order.

## Panel Note

PCBWay adds two break-away rails to SMT orders by default. This board needs them on the left and right edges, because the connectors overhang the top and bottom. It's also smaller than PCBWay's published 50 × 50 mm assembly minimum and has no fiducials of its own, so confirm the rails with PCBWay before ordering, and include this note in the remarks:

> The connectors overhang the board's top edge by about 2 mm and its bottom edge by about 1.5 mm, so please don't V-cut, and don't put rails on those edges. Put the rails on the left and right edges, joined by mouse-bite tabs. U20 sits 0.3 mm from the left edge and the pads of C43 and C44 sit 0.43 mm from it, so put the left tabs in the top 14 mm of that edge, viewed from the top side. The board has no fiducials, so please put them on the rails.

## Rebuilding the Files

Install KiCad 10, then run `python3 make_pcbway.py` from `PCB/v3`.
