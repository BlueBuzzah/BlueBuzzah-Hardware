# PCB v3 Manufacturing Files

Fabrication-ready files for the BlueBuzzah v3 PCB, built around the JLCPCB-assembled ESP32-S3-WROOM-1U module.

## Contents

| File | Description |
| --- | --- |
| `jlc_pcb_gerbers.zip` | Gerber and drill files for one board in a production panel |
| `BOM_JCLPCB_BlueBuzzah_v3.csv` | Bill of materials with JLCPCB part numbers |
| `CPL_JLCPCB_BlueBuzzah_v3-all-pos.csv` | Pick-and-place positions, corrected for JLCPCB's parts library |
| `ORDERING.md` | Step-by-step JLCPCB ordering notes |
| `make_jlcpcb.py` | Rebuilds the order files and the panel from the KiCad sources |
| **[kicad/](kicad/)** | KiCad schematic, PCB and 3D sources |
| `panel/` | The KiKit panel the order files are built from |

## Ordering the Board

Follow [ORDERING.md](ORDERING.md) to order the board fully assembled from JLCPCB. The panel holds one board, so the panel quantity is the board quantity.

## Rebuilding the Order Files

Install KiCad 10, quit it, then run:

```bash
python3 make_jlcpcb.py
```

The script checks the board and panel with DRC, then rewrites the panel and all three order files. Check any new package in JLCPCB's placement preview before ordering.
