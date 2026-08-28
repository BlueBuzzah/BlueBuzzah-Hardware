# PCB v3 Manufacturing Files

Fabrication-ready files for the BlueBuzzah v3 PCB.

## Contents

| File                                                             | Description                                     |
| ------------------------------------------------------------------ | ------------------------------------------------ |
| `jlc_pcb_gerbers.zip`                                             | Gerber files for PCB manufacturing              |
| `BOM_JCLPCB_BlueBuzzah_v3.csv`                                    | Bill of materials with component specifications |
| `CPL_JLCPCB_BlueBuzzah_v3-all-pos.csv`                            | Pick-and-place positions for SMT assembly       |
| **[kicad/](kicad/)**                                              | KiCad schematic and PCB source files            |

## Ordering the Board

Upload `jlc_pcb_gerbers.zip`, the BOM CSV, and the CPL CSV to your preferred PCB manufacturer's assembly service (e.g. JLCPCB) to order the board fully assembled. The files are already formatted for JLCPCB's SMT assembly workflow.

If you only need bare boards (no assembly), the gerber zip alone is sufficient — order components separately using the BOM.
