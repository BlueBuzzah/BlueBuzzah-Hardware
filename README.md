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

- **Custom PCB** built around the Seeed XIAO ESP32-S3 (MCU + BLE), with five
  DRV2605L haptic drivers, a TCA9548A I2C multiplexer, an LSM6DS3 IMU, a
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
| **[PCB/v3/](PCB/v3/)** | Gerbers, BOM, pick-and-place (CPL), and KiCad sources for the v3 board |
| **[models/](models/)** | CAD files for the board, tactor and case (`.step`, `.3mf`), and the `.glb` models used for the build guide's images |
| **[scripts/](scripts/)** | Headless Blender scripts that render the build guide's images from those models; see its [README](scripts/README.md) |

## Getting Started

The complete, step-by-step build guide lives at
**[bluebuzzah.com/docs](https://bluebuzzah.com/docs/)** — start there before
ordering parts.

### Manufacturing the PCB

The [`PCB/v3/`](PCB/v3/) folder contains everything needed for fabrication and
assembly:

- `jlc_pcb_gerbers.zip` — Gerber files for PCB manufacturing
- `BOM_JCLPCB_BlueBuzzah_v3.csv` — bill of materials
- `CPL_JLCPCB_BlueBuzzah_v3-all-pos.csv` — pick-and-place positions
- `kicad/` — KiCad schematic and PCB source files

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
| `PCB/v3/` (KiCad sources, Gerbers, BOM, CPL) | CERN-OHL-S v2 | [`LICENSE-CERN-OHL-S-2.0.txt`](LICENSE-CERN-OHL-S-2.0.txt) |
| `models/`, `README.md`, `PCB/v3/**/*.md`, `scripts/README.md` | CC BY-SA 4.0 | [`LICENSE-CC-BY-SA-4.0.txt`](LICENSE-CC-BY-SA-4.0.txt) |
| `scripts/`, `tools/` | MIT | [`LICENSE`](LICENSE) |

These third-party files are not relicensed and keep their own licenses:

- The KiCad standard library parts and Seeed Studio's XIAO parts the board uses (the KiCad library license, and Seeed's OPL KiCad library license).
- `scripts/fonts/`: SIL Open Font License (OFL files alongside).
- The board exports (`models/BlueBuzzah-v3-pcb-model.step`, `models/bluebuzzah-v3-pcb.glb`, `models/bluebuzzah-exploded.glb`) include the part models above, which keep their own licenses.

The BlueBuzzah and BuzzahBuddy names and logos are not covered by these licenses. See [Licenses and the BlueBuzzah name](https://bluebuzzah.com/terms#licenses).
