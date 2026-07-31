# BlueBuzzah v3 Hardware Wiki — Design

**Date:** 2026-07-31
**Status:** Approved
**Branches:** `v3-docs` in `BlueBuzzah-Hardware.wiki` (content) and `BlueBuzzah-Hardware` (assets + this spec)

## Objective

Rebuild the public hardware wiki as a complete, end-to-end build guide for BlueBuzzah v3
(Seeed XIAO ESP32-S3, five motors). The wiki covers v3 only. No v2 content is published.

## Decisions

| Decision | Choice |
| --- | --- |
| v2 vs v3 | v3-forward. v2 content is removed from the wiki entirely, not archived in place. |
| Scope | Full end-to-end build guide, ordering through therapy use. |
| Source of truth | Adapt the archived v2 prose as raw material; derive all electrical specifics from the KiCad schematic, JLCPCB BOM, and firmware source; flag anything unverified against real hardware. |
| Naming | "BlueBuzzah v3" throughout. "PentaBuzzer" / "Penta Buzzer mini V2.2" appears only where a builder needs it to locate design files. |
| Design files | Copied into `BlueBuzzah-Hardware` so builders use one repo. |
| Gaps | Explicit status callouts, aggregated on a `Build-Status` page. |
| v2 owners | Not addressed by the wiki. No references, banners, or redirects. |

## Constraints

**GitHub wikis publish only from the default branch and do not support pull requests.**
The `v3-docs` branch is a staging and review area. Nothing is public until it merges.

**GitHub wikis serve files in subdirectories as reachable pages.** The existing `archive/`
directory is therefore public surface, not private storage. It must be deleted from the
wiki repo, not merely unlinked. The content survives in git history, and the original
source remains at `BlueBuzzah-Hardware/Instructions/Blue Buzzah Build Documentation.pdf`.

**Asset ordering.** The wiki links to `PCB/v3/...` paths in `BlueBuzzah-Hardware`. The
asset copy must land before the wiki merges, or every ordering link 404s.

## Page Structure

Seventeen live pages plus a sidebar. Numbered `Part-N-*` titles carry build order; the sidebar mirrors it.

**Getting started**
- `Home` — v3 landing, spec table, build-path overview
- `Disclaimers` — existing, reviewed for v3 accuracy
- `Acknowledgements` — existing, reviewed
- `Build-Status` — new; single tracker for every open item

**Understanding the project**
- `Introduction` — adapted from archived intro, v3-only
- `Why-We-Use-Spring-Tactors` — adapted, generation-neutral content

**Build**
- `Part-1-Ordering-the-PCB` — JLCPCB order using v3 gerbers/BOM/CPL; absorbs the
  soldering-requirements material, which shrinks substantially for v3
- `Part-2-Building-the-Tactors` — adapted
- `Part-3-LRA-Housing-Assembly` — existing page, renumbered only
- `Part-4-Mounting-Tactors-in-Glove-Fingertips` — adapted, extended to five fingers
- `Part-5-Wiring-the-Glove-Harness` — new; carries the reversed silk-screen warning
- `Part-6-Enclosure-and-Mounting` — new, 🚧 stub; no interim enclosure is recommended
- `Part-7-Flashing-the-Firmware` — new; BlueBuzzah-Updater and PlatformIO, role assignment
- `Part-8-First-Power-On-and-Bench-Test` — new; `MOTOR_DIAG`, `MOTOR_TEST:<n>`,
  `MOTOR_PRESENT`, LED status codes, battery behavior
- `Part-9-Using-the-Gloves` — new; BuzzahBuddy app. Replaces the archived
  CircuitPython/Mu Editor page, which is obsolete.

**Reference**
- `Parts-and-Tools-List` — rebuilt from the v3 BOM
- `Troubleshooting` — new
- `_Sidebar` — new; the wiki currently has no navigation

**Deleted:** `archive/` (13 files).

## v3-Specific Content

Facts a v2-derived guide would state incorrectly. Each is traced to its source; the two
marked critical get prominent callouts rather than inline mentions.

| Area | v3 behavior | Source |
| --- | --- | --- |
| Board | XIAO ESP32-S3, surface-mounted on the PCB | BOM `U2` |
| Motors | 5 (adds thumb) | `board_config.h:29` |
| Connectors | Six 2-pin JST-PH, placed by JLCPCB — builder solders none | BOM `J1`–`J6` |
| **Motor port labels** | **Silk 1–5 is reversed relative to firmware channels: firmware finger N drives the port labeled (5 − N)** | `board_config.h:44-47` |
| **USB-only operation** | **Motors will not run. DRV2605s are powered from VBat; a battery is required.** | firmware README |
| Power | SPDT slide switch, GPIO3, plus deep sleep | BOM `SW1`, `board_config.h:39` |
| Battery sense | DRV2605 VBAT register `0x21` over I2C; no divider | `board_config.h:42-43` |
| Status LED | WS2812B on GPIO4 | BOM `D1`, `board_config.h:32` |
| I2C | TCA9548A mux at `0x70`, DRV2605s at `0x5A` | `board_config.h:53-54` |
| IMU | LSM6DS3 populated but unused by current firmware | BOM `U1` |
| Software | PlatformIO firmware, BuzzahBuddy app, BlueBuzzah-Updater | firmware repo |

## Gap Handling

Three callout states, used consistently and aggregated on `Build-Status`:

- 🚧 **In design** — the enclosure. States that it is unavailable and that no substitute
  is recommended.
- 📷 **Photos pending** — steps are written completely in text; the image slot is marked.
- ⚠️ **Needs hardware verification** — any claim derived from schematic or firmware rather
  than observed on a built unit.

Each flag is a single-line deletion once resolved.

## Asset Work (`BlueBuzzah-Hardware`)

Copy from the `PentaBuzzer` repo:

- `PCB/v3/` — gerbers (`jlc_pcb_gerbers.zip`), BOM, CPL, and KiCad source
- `3D-Print-Models/` — the v3 STEP file

The existing v2 assets stay untouched. The wiki does not link to them.

## Verification

1. **Claim traceability** — every electrical and mechanical claim cites its source file,
   BOM row, or schematic net, delivered as a review table for spot-checking.
2. **Link check** — automated pass over all `[[wikilinks]]` and repo-relative paths,
   run before merge, to catch `PCB/v3/` breakage.
3. **Hardware pass** — the ⚠️ flags form a checklist to walk with a built v3 glove.

## Out of Scope

- Designing the enclosure.
- Producing build photography.
- Any v2 documentation, migration path, or owner communication.
- Fixing the stale v2 battery-monitoring row in the firmware README. It contradicts the
  section below it and should be corrected, but in the firmware repo, not here.
