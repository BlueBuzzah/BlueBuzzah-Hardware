# Ordering assembled boards from JLCPCB

Use the three order files in this folder together, unchanged. They describe one board inside a 72 × 72 mm production panel, so the panel quantity is the board quantity. The files in the `PCBWay` folder are a separate package for PCBWay, described in `PCBWay/ORDERING-PCBWAY.md`, so don't mix the two.

| File | Description |
| --- | --- |
| `BlueBuzzah_v3_JLCPCB_gerbers.zip` | Gerber and drill files for the panel: one board in a frame with mouse-bite tabs, tooling holes and fiducials |
| `BlueBuzzah_v3_JLCPCB_BOM.csv` | Bill of materials with JLCPCB (LCSC) part numbers |
| `BlueBuzzah_v3_JLCPCB_CPL.csv` | Placement of the 83 parts, corrected for JLCPCB's parts library |

## Placing the Order

1. Start a Standard PCB/PCBA quote, upload `BlueBuzzah_v3_JLCPCB_gerbers.zip`, and enter these values:

   | Option | Value |
   | --- | --- |
   | Base material | FR-4 |
   | Layers | 2 |
   | Dimensions | 72 × 72 mm (read from the Gerbers) |
   | Delivery format | Panel by Customer, 1 column and 1 row |
   | PCB thickness | 1.6 mm |
   | PCB color | Blue |
   | Silkscreen | White |
   | Surface finish | ENIG |
   | Outer copper weight | 1 oz |
   | Min via hole size/diameter | 0.3mm/(0.4/0.45mm), the default |

   The Gerbers don't carry color or finish, so these values have to be set on the order. The board's smallest vias are 0.2 mm and 0.25 mm holes in 0.55 mm pads, which JLCPCB makes at no extra charge on the default via option. Don't pick a smaller one: it adds plugged vias and a 4-wire Kelvin test to the price.

2. Turn on PCB Assembly, choose Standard, and assemble the top side. The board has 28 unique parts, 76 SMT parts and 7 through-hole parts (J1 to J6 and SW1).
3. Upload `BlueBuzzah_v3_JLCPCB_BOM.csv` and `BlueBuzzah_v3_JLCPCB_CPL.csv`, and choose **Complete File, just proceed with my own files**.
4. On the Bill of Materials step, tick **D1**. JLCPCB requires this for the LED because it's moisture sensitive, and the order can't continue until it's ticked.
5. On the Component Placements step, check the 2D view. Each part's pin-1 dot should sit at the silkscreen mark. Don't rotate or move parts here: if something looks wrong, [open an issue](https://github.com/BlueBuzzah/BlueBuzzah-Hardware/issues) so the files get fixed for every order.
6. If the order page offers **Confirm Production file**, choose Yes.
7. After ordering, open the order in Order History and check the production files: the 2D file for SMD placement and polarity, and the 3D file for through-hole parts. An order can't be canceled once PCB production starts. Check these in particular, because their placement uses JLCPCB's default orientation:
   - D2: the placement preview shows no polarity mark for it. Its cathode (pad 1) belongs at the closed end of the silkscreen outline, toward the bottom of the board.
   - U1 (LGA-14): pin 1 at the dot in the preview. The part itself has no mark.
   - D1: the LED's notched corner.
   - D11: cathode bar toward the board's left edge.

U21 pad 2 and U23 pad 2 each have a 0.2 mm via in the pad, because neither has room to move it. They're unfilled, like the board's other vias, so tell JLCPCB they're intentional if it asks.

If JLCPCB says a part is out of stock, don't substitute it on the order. Check for a newer release of these files, or [open an issue](https://github.com/BlueBuzzah/BlueBuzzah-Hardware/issues).
