# BlueBuzzah Hardware

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Hardware design files for BlueBuzzah v3, a medical device research platform
implementing vibrotactile Coordinated Reset (vCR) therapy for Parkinson's
disease research. This repository contains the files needed to manufacture the
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

## Repository Contents

| Folder | Description |
| --- | --- |
| **[PCB/v3/](PCB/v3/)** | Gerbers, BOM, pick-and-place (CPL), and KiCad sources for the v3 board |
| **[3D-Print-Models/](3D-Print-Models/)** | 3D model of the v3 board (`.step`) |
| **[archive/](archive/)** | Deprecated v2 hardware files, kept for historical reference only |

## Getting Started

The complete, step-by-step build guide lives in the
**[BlueBuzzah-Hardware wiki](https://github.com/BlueBuzzah/BlueBuzzah-Hardware/wiki)** —
start there before ordering parts.

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

## License

MIT License - see [LICENSE](LICENSE) for details.
