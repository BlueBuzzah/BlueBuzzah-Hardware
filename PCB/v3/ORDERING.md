# Ordering assembled boards from JLCPCB

Use the three order files in this folder together, unchanged. Each panel holds one board, so the panel quantity is the board quantity.

1. Start a PCB order and upload `jlc_pcb_gerbers.zip`.
2. Turn on PCB Assembly, choose Standard, and assemble the top side.
3. Upload `BOM_JCLPCB_BlueBuzzah_v3.csv` and `CPL_JLCPCB_BlueBuzzah_v3-all-pos.csv`, and choose **Complete File, just proceed with my own files**.
4. On the Bill of Materials step, tick **D1**. JLCPCB requires this for the LED because it's moisture sensitive, and the order can't continue until it's ticked.
5. On the Component Placements step, check the 2D view. Each part's pin-1 dot should sit at the silkscreen mark. Don't rotate or move parts here: if something looks wrong, fix the files instead, so every order gets the same placement.
6. If the order page offers **Confirm Production file**, choose Yes.
7. After ordering, open the order in Order History and check the production files: the 2D file for SMD placement and polarity, and the 3D file for through-hole parts. An order can't be canceled once PCB production starts. Check D2 here in particular: the placement preview shows no polarity mark for it, and its cathode (pad 1) belongs at the closed end of the silkscreen outline, toward the bottom of the board.

If JLCPCB says a part is out of stock, don't substitute it on the order. Update the part in `make_jlcpcb.py`, run `python3 make_jlcpcb.py`, and check the new part in the placement preview.
