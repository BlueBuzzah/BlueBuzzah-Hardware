# KiCad Source Files

The KiCad schematic and PCB design source for the BlueBuzzah v3 board, provided so the design is readable and archivable alongside the board you order.

## Contents

- `*.kicad_pro` - KiCad project file
- `*.kicad_sch` - top-level schematic, plus `Buzzer_Drivers.kicad_sch` (haptic driver sub-schematic)
- `*.kicad_pcb` - PCB layout
- `fp-lib-table`, `sym-lib-table` - KiCad library table references

## Important: This Project Will Not Open Cleanly

Opening this project in KiCad will **not** resolve all footprints and symbols. The design depends on a third-party component library tree that is deliberately not vendored into this repository (it carries its own license and is unrelated to this repository's MIT license).

To do actual schematic or PCB editing, work in the source project instead:

**[PentaBuzzer repository](https://github.com/BlueBuzzah/PentaBuzzer)**

These files exist here purely as a reference snapshot of the design that produced the manufacturing files in `PCB/v3/`.
