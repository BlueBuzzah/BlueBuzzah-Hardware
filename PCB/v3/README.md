# PCB v3 Manufacturing Files

Sources and build scripts for the BlueBuzzah v3 PCB, built around the JLCPCB-assembled ESP32-S3-WROOM-1U-N8R8 module. The order files aren't kept in the repo: the scripts build them into `build/`, which git ignores.

## Contents

| File | Description |
| --- | --- |
| `make_jlcpcb.py` | Builds the panel and the JLCPCB order files (one board in a production panel) into `build/jlcpcb/` |
| [`ORDERING-JLCPCB.md`](ORDERING-JLCPCB.md) | Step-by-step JLCPCB ordering notes |
| `make_pcbway.py` | Builds the separate PCBWay order files (one board, not panelized) into `build/pcbway/` |
| [`ORDERING-PCBWay.md`](ORDERING-PCBWay.md) | Step-by-step PCBWay ordering notes |
| **[kicad/](kicad/)** | KiCad schematic, PCB and 3D sources |
| `panel/` | The KiKit panel the order files are built from |

## Ordering the Board

Download `BlueBuzzah-v3-PCB.zip` from the latest [release](https://github.com/BlueBuzzah/BlueBuzzah-Hardware/releases). It holds the built order files and these ordering notes.

Follow [ORDERING-JLCPCB.md](ORDERING-JLCPCB.md), in the zip's `JLCPCB` folder, to order the board fully assembled from JLCPCB. The panel holds one board, so the panel quantity is the board quantity.

To order from PCBWay instead, follow [ORDERING-PCBWay.md](ORDERING-PCBWay.md), in the zip's `PCBWay` folder. Those files describe the bare board, with no panel. Don't mix them with the JLCPCB files.

## Recovering a Board

If the BlueBuzzah Updater can't reach a board over USB, put it in the bootloader by hand:

1. Open the case and plug in USB.
2. Hold the BOOT button (SW2) and slide the power switch off.
3. Wait 5 seconds, then slide the switch on and release BOOT.
4. Flash the board with the Updater.

Sliding the switch off signals the firmware at once and cuts the 3.3 V supply in hardware about 2 seconds later, even if the firmware has stopped running. The delay gives the firmware time to stop the motors and save the session; once the supply is cut, the motor drivers shut down on their own.

## Building the Order Files

Each release includes these files already built, in `BlueBuzzah-v3-PCB.zip`. To build them yourself:

Install KiCad 10, quit it, then run:

```bash
python3 make_jlcpcb.py
```

The script checks the board and panel with DRC, then rewrites the panel and writes the three order files to `build/jlcpcb/`. Check any new package in JLCPCB's placement preview before ordering.

The PCBWay files are separate. Run `python3 make_pcbway.py` to build them into `build/pcbway/`.

If a part goes out of stock, don't substitute it on the order. Update it in `make_jlcpcb.py` or `make_pcbway.py`, rebuild, and check the new part in the placement preview.
