# BlueBuzzah Hardware

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Hardware design files for BlueBuzzah, a medical device research platform implementing vibrotactile Coordinated Reset (vCR) therapy for Parkinson's disease treatment. This repository contains everything needed to manufacture the physical components: PCB fabrication files, 3D-printable enclosure models, and complete build documentation.

## Overview

BlueBuzzah consists of two synchronized haptic gloves that deliver precisely timed vibration patterns to fingers. Each glove requires:

- **Custom PCB** with Feather nRF52840 microcontroller, DRV2605 haptic drivers, and LRA motors
- **3D-printed enclosure** housing the electronics and tactors
- **Firmware** from the [BlueBuzzah-Firmware](https://github.com/BlueBuzzah/BlueBuzzah-Firmware) repository

## Repository Contents

| Folder                                   | Description                                                       |
| ---------------------------------------- | ----------------------------------------------------------------- |
| **[Instructions/](Instructions/)**       | Complete build documentation                                      |
| **[3D-Print-Models/](3D-Print-Models/)** | STL files for the enclosure and tactor housings                   |
| **[PCB/](PCB/)**                         | Gerber files, BOM, and pick-and-place positions for manufacturing |

## Getting Started

**[Download the Build Documentation (PDF)](Instructions/Blue%20Buzzah%20Build%20Documentation.pdf)** for complete step-by-step assembly instructions.

### Manufacturing the PCB

The `PCB/` folder contains all files needed for PCB fabrication:

- `Bluetooth_4-ch_Buzzah_v2.0_-_2-layer_v4.zip` - Gerber files for PCB manufacturing
- `bom.csv` - Bill of materials with component specifications
- `positions.csv` - Pick-and-place positions for SMT assembly
- `netlist.ipc` - IPC netlist for verification

Upload the Gerber zip to your preferred PCB manufacturer (JLCPCB, PCBWay, OSH Park, etc.).

### 3D Printing the Enclosure

The `3D-Print-Models/` folder contains STL files ready for slicing. Recommended print settings are detailed in the build documentation.

## Related Repositories

- **[BlueBuzzah-Updater](https://github.com/BlueBuzzah/BlueBuzzah-Updater)** - Desktop application for updating and configuring BlueBuzzah devices.

## License

MIT License - see [LICENSE](LICENSE) for details.
