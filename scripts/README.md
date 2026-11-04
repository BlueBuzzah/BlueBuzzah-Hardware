# Render scripts

These scripts rebuild the v3 renders in `images/v3/` and the `.glb` models in `models/` from the CAD files in `models/`. Everything runs headless; no app windows open.

Rendered images in `images/` aren't committed. The published copies are WebP files on BlueBuzzah.com, in `src/public/docs/img/` of the [BlueBuzzah.com](https://github.com/BlueBuzzah/BlueBuzzah.com) repository; convert new renders as its `CLAUDE.md` describes.

## Requirements

- macOS (image resizing uses `sips`)
- [FreeCAD](https://www.freecad.org) 1.1 in `/Applications` (or set `FREECAD_BIN`)
- [Blender](https://www.blender.org) 5.2 on the `PATH` (or set `BLENDER`)
- Google Chrome in `/Applications` (or set `CHROME`), for the numbered labels

## Running

```sh
python3 scripts/render_all.py                    # rebuild everything into this checkout
python3 scripts/render_all.py battery pin        # only images whose name contains one of these words
OUT=/tmp/preview BB_SAMPLES=16 python3 scripts/render_all.py   # quick, low-quality preview elsewhere
```

Each run:

1. Exports meshes from the STEP files with FreeCAD (`freecad/`).
2. Renders each image in `configs/` with Blender (`brender.py`), building the parts that have no CAD model in code (`builders/`).
3. Adds the numbered labels to the two exploded views (`label.sh`, `labels.py`, `labels/`).
4. Resizes images for the web: part images to 900 px wide, the exploded views and board render to 1800 px.
5. Exports each scene as a `.glb` model.

The unlabeled exploded renders (`tactor-exploded.png`, `bluebuzzah-exploded.png`) are only inputs for the labeled versions. Don't publish them.

## Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `OUT` | this checkout | Where `images/v3/` and `models/` are written |
| `HW` | this checkout | Where the CAD files in `models/` are read from |
| `WORK` | a new temporary folder | Intermediate meshes; reuse one to skip the FreeCAD step |
| `BB_SAMPLES` | each config's value | Render samples; lower for quick previews |
| `TACTOR_STEP`, `CASE_STEP` | files in `$HW/models/` | Override a STEP file's path |
| `BOARD_STEP` | `$HW/PCB/v3/kicad/BlueBuzzah_v3.step` | Override the board STEP's path |

## Layout

| Path | What it is |
| --- | --- |
| `render_all.py` | Runs every step above |
| `brender.py` | Renders one config, or exports it as `.glb` (`BB_MODE=model`) |
| `configs/<folder>/<image>.json` | One file per published image: parts, colors, camera, layout offsets, output paths |
| `builders/` | Models built in code: LRA motor, compression spring, wire lead, battery, antenna, M2 screw, and a stand-in for the board's power switch |
| `freecad/` | STEP-to-mesh exports, and the board STEP-to-colored-`.glb` conversion |
| `labels/` | Number and name for each part in the two exploded views |
| `fonts/` | Lexend and Atkinson Hyperlegible Next for the labels (SIL Open Font License) |

## Modelling notes

- **LRA motor, battery, antenna and wire lead** are modelled from datasheet dimensions and photos. Their wires and cables are shortened so the parts read at image scale.
- **Compression spring:** the supplier lists 5 mm compressed and 3 mm free length, which can't be right; the model uses 5 mm free length, which fits the housing's 5.2 mm spring space. The coil count (7 turns) is assumed.
- **Board power switch:** the KiCad board assigns the wrong 3D model (a two-row DPDT switch) to the K3-1260D-L1 footprint, so its second pin row hangs off the board edge. Renders remove it and use `builders/switch.py`, sized from the footprint outline (body height assumed).
- **Tactor finger cup:** its STEP solid is invalid and meshes with holes at fine detail; the export coarsens it until the mesh is closed.
- **BlueBuzzah v3 board (`bluebuzzah-v3-pcb`):** rendered from `PCB/v3/kicad/BlueBuzzah_v3.step` (ESP32-S3-WROOM-1U-N8R8) with a blue solder mask and a silver-grey module shield. KiCad's library has no model for the USB-C connector (J10), so the render adds `models/USB_C_Receptacle_HRO_TYPE-C-31-M-12.step`, taken from KiCad's RoyalBlue54L demo (CERN Open Hardware Licence v2, Permissive). The case exploded view uses the same board and fixes.
