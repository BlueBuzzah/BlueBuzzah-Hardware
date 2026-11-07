# KiCad Source Files

The KiCad schematic and PCB design source for the BlueBuzzah v3 board. Open `BlueBuzzah_v3.kicad_pro` in KiCad 10.

## Contents

- `BlueBuzzah_v3.kicad_pro` - KiCad project file
- `BlueBuzzah_v3.kicad_sch` - top-level schematic, plus `MCU_Power.kicad_sch` (module, USB and power) and `Buzzer_Drivers.kicad_sch` (haptic drivers)
- `BlueBuzzah_v3.kicad_pcb` - PCB layout
- `BlueBuzzah_v3.step` - 3D model of the assembled board
- `3dmodels/` - 3D model for the ESP32-S3-WROOM-1U-N8R8
- `Libraries/` - the slide switch footprint, and the DRV2605L symbol and footprint
- `fp-lib-table`, `sym-lib-table` - KiCad library tables
- `BlueBuzzah_v3.kicad_dru` - custom DRC rules for the six part pairs in tight gaps: R67 with C45 and U20; C45 with U20 and Q1; and SW2 with R43 and R45

Everything else comes from KiCad's standard libraries. KiCad has no 3D model for the USB-C connector (J10), so it's missing from the 3D view and the STEP file. J10's footprint keeps local shell-pad changes, and U1's pads are narrowed to 0.30 mm so PCBWay can keep a solder mask dam between them. KiCad reports both as different from their library copies.
