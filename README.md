# BlueBuzzah Hardware

[![License](https://img.shields.io/badge/license-MIT%20%7C%20CERN--OHL--S%20%7C%20CC%20BY--SA-blue.svg)](#license)

Hardware design files for BlueBuzzah v3, an open-source research platform for
vibrotactile Coordinated Reset (vCR) stimulation, inspired by published research
in Parkinson's disease. This repository contains the files needed to manufacture the
physical components: PCB fabrication files, the board 3D model, and links to the
full build documentation.

## Overview

BlueBuzzah consists of two synchronized haptic gloves that deliver precisely
timed vibration patterns to the fingertips. Each glove requires:

- **Custom PCB** built around the ESP32-S3-WROOM-1U-N8R8 module (MCU + BLE), with
  five DRV2605L haptic drivers, a TCA9548A I2C multiplexer, an LSM6DS3 IMU, a
  WS2812B status LED, and five LRA motors (index, middle, ring, pinky, thumb)
- **Firmware** from the [BlueBuzzah-Firmware](https://github.com/BlueBuzzah/BlueBuzzah-Firmware) repository
- **Enclosure** — the v3 wearable enclosure has not been designed yet; see the
  wiki's Build Status page for the current state of the build

The board arrives fully assembled from JLCPCB's SMT service, and the tactor's
wire-to-LRA connection is a friction fit made by a 3D-printed wire plug — there
is no soldering anywhere in the build.

## Important notices

BlueBuzzah devices are not FDA cleared or approved medical devices and not intended to diagnose, treat, cure, mitigate, or prevent any disease. The information provided through BlueBuzzah is for general wellness purposes only and not a substitute for professional medical advice, diagnosis, or treatment.

**Important:** People with implanted electrodes from deep brain stimulation (DBS), heart pacemakers, or other internal electronic devices should take special precautions around all electronic devices, including BlueBuzzah. Consult your physician before use.

Read the [safety page](https://bluebuzzah.com/docs/safety) and the [terms and safety](https://bluebuzzah.com/terms) page before you build or wear a pair.

## Repository Contents

| Folder | Description |
| --- | --- |
| **[PCB/v3/](PCB/v3/)** | KiCad sources and the scripts that build the Gerbers, BOM and pick-and-place (CPL) for the v3 board |
| **[models/](models/)** | CAD files for the board, tactor and case (`STEP/`), the `.3mf` print file, a `.stl` for each 3D-printed part (`STL/`), and the `.glb` models used for the build guide's images (`GLB/`) |
| **[scripts/](scripts/)** | Headless Blender scripts that render the build guide's images from those models; see its [README](scripts/README.md) |

## Getting Started

The complete, step-by-step build guide lives at
**[bluebuzzah.com/docs](https://bluebuzzah.com/docs/)** — start there before
ordering parts.

Each [release](https://github.com/BlueBuzzah/BlueBuzzah-Hardware/releases) includes
two zips: `BlueBuzzah-v3-PCB.zip` holds the built JLCPCB and PCBWay order files,
and `BlueBuzzah-v3-parts.zip` holds every 3D-printed part.

### Manufacturing the PCB

The [`PCB/v3/`](PCB/v3/) folder contains everything needed for fabrication and
assembly. The order files aren't kept in the repo; the scripts build them into
`PCB/v3/build/`:

- `make_jlcpcb.py` — builds the JLCPCB order files (Gerber zip, BOM, CPL) into `build/jlcpcb/`
- `ORDERING-JLCPCB.md` — step-by-step JLCPCB ordering notes
- `make_pcbway.py` — builds separate PCBWay order files for one board, not panelized, into `build/pcbway/`
- `ORDERING-PCBWay.md` — step-by-step PCBWay ordering notes
- `kicad/` — KiCad schematic and PCB source files
- `panel/` — the KiKit panel the order files are built from

Upload the Gerber zip, BOM, and CPL to JLCPCB's SMT assembly service to order the
board fully assembled. See the wiki's "Ordering the PCB" page for details.

## Related Repositories

- **[BlueBuzzah-Firmware](https://github.com/BlueBuzzah/BlueBuzzah-Firmware)** - Firmware for the BlueBuzzah gloves.
- **[BlueBuzzah-Updater](https://github.com/BlueBuzzah/BlueBuzzah-Updater)** - Desktop application for updating and configuring BlueBuzzah devices.
- **[BlueBuzzah-Gloves](https://github.com/PWPInnovator898/BlueBuzzah-Gloves)** - The original v2 design, for reference.

## License

Each part of this repository is under the license that fits it. Where two rows overlap, the more specific path wins.

| Path | License | File |
| --- | --- | --- |
| `PCB/v3/` (KiCad sources, panel, Gerbers, BOM, CPL, PCBWay package) | CERN-OHL-S v2 | [`LICENSE-CERN-OHL-S-2.0.txt`](LICENSE-CERN-OHL-S-2.0.txt) |
| `models/`, `README.md`, `PCB/v3/**/*.md`, `scripts/README.md` | CC BY-SA 4.0 | [`LICENSE-CC-BY-SA-4.0.txt`](LICENSE-CC-BY-SA-4.0.txt) |
| `scripts/`, `tools/`, `PCB/v3/make_*.py` | MIT | [`LICENSE`](LICENSE) |

These third-party files are not relicensed and keep their own licenses:

- `models/STEP/USB_C_Receptacle_HRO_TYPE-C-31-M-12.step`: CERN-OHL-P v2, from KiCad's RoyalBlue54L demo.
- `PCB/v3/kicad/3dmodels/ESP32-S3-WROOM-1U.step`: Espressif's vendor model.
- `PCB/v3/kicad/Libraries/` and the KiCad standard library parts the board uses: the KiCad library license (CC BY-SA 4.0 with KiCad's exception for designs made with them).
- `scripts/fonts/`: SIL Open Font License (OFL files alongside).
- The board exports (`PCB/v3/kicad/BlueBuzzah_v3.step`, `models/STEP/BlueBuzzah-v3-pcb-model.step`, `models/GLB/bluebuzzah-v3-pcb.glb`, `models/GLB/bluebuzzah-exploded.glb`) include the part models above, which keep their own licenses.

The BlueBuzzah and BuzzahBuddy names and logos are not covered by these licenses. See [Licenses and the BlueBuzzah name](https://bluebuzzah.com/terms#licenses).
