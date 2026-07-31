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
| Scope | Complete and buildable from ordering through a fully assembled, wired, flashed, bench-tested pair of gloves driven by the app. **Wearable daily use is blocked pending the enclosure design** — see Enclosure Gap below. |
| Source of truth | Adapt the archived v2 prose as raw material; derive all electrical specifics from the KiCad schematic, JLCPCB BOM, and firmware source; flag anything unverified against real hardware. |
| Naming | "BlueBuzzah v3" throughout. "PentaBuzzer" / "Penta Buzzer mini V2.2" appears only where a builder needs it to locate design files. |
| Design files | Copied into `BlueBuzzah-Hardware` so builders use one repo. |
| Gaps | Explicit status callouts, aggregated on a `Build-Status` page. |
| v2 owners | Not addressed by the wiki. No references, banners, or redirects. |

## Constraints

**GitHub wikis publish only from the default branch and do not support pull requests.**
The `v3-docs` branch is a staging and review area. Nothing is public until it merges.

The wiki's remote has exactly one branch, `master` — that is the merge target. The local
checkout also carries a `main` branch that was never pushed and is not a real target;
delete it before merging so nobody publishes into the wrong place.

**GitHub wikis serve files in subdirectories as reachable pages.** Subfolders are
organizational only: any `.md` file is servable at `/wiki/PageName` regardless of folder,
and unlinked pages still appear in the wiki's Pages list. The existing `archive/` directory
is therefore public surface, not private storage. It must be deleted from the wiki repo,
not merely unlinked.

Deleting it stops those pages from being *served*, which is the goal. It does not make the
content private: the wiki repo is itself publicly clonable, so the history remains
fetchable by anyone. Nothing in the v2 pages is sensitive, so this is acceptable — but the
distinction should not be misremembered later as "the content is gone."

The `archive/` directory holds **13 tracked `.md` files**. A 14th entry on disk,
`Blue Buzzah Build Documentation.pdf`, is untracked — a local scratch copy that was never
committed and never served as a wiki page. The committed original lives at
`BlueBuzzah-Hardware/Instructions/Blue Buzzah Build Documentation.pdf` and is unaffected.

**Asset ordering.** The wiki links to `PCB/v3/...` paths in `BlueBuzzah-Hardware`. The
asset copy must land before the wiki merges, or every ordering link 404s.

**Merge granularity.** Because the wiki has no PR mechanism, the `v3-docs` branch is the
only review point and all 17 pages go live in one merge. Work therefore lands as
reviewable per-page commits on the branch, and the three verification passes run against
the complete branch before a single merge to `master`. No partial merges — a half-migrated
wiki would publish v3 pages alongside the v2 `archive/` pages this work exists to remove.

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

Ordering principle: **test before anything becomes irreversible.** Flashing moves to
Part-2 so the bare board can be smoke-tested while it is still just a board — before any
LRA is soldered, any housing is glued, and any glove fingertip is cut.

- `Part-1-Ordering-the-PCB` — JLCPCB order using v3 gerbers/BOM/CPL; absorbs the
  soldering-requirements material, which shrinks substantially for v3
- `Part-2-Flashing-and-Smoke-Testing-the-Bare-Board` — new; BlueBuzzah-Updater and
  PlatformIO, PRIMARY/SECONDARY role assignment, then `MOTOR_DIAG` and `MOTOR_PRESENT`
  on the bare board with a battery and one loose LRA. Establishes the board is alive
  before any irreversible assembly. States plainly that a battery is required and USB
  alone will not drive motors.
- `Part-3-Building-the-Tactors` — adapted. **Boundary:** covers wire preparation, tinning,
  and soldering leads to the LRA. Ends with a wired, untested LRA.
- `Part-4-LRA-Housing-Assembly` — existing page, renumbered. **Boundary:** begins from an
  already-wired LRA; does not repeat tinning or soldering instructions. Adds a
  per-tactor continuity/buzz check before the housing is closed, since dovetail assembly
  is difficult to reverse.
- `Part-5-Mounting-Tactors-in-Glove-Fingertips` — adapted, extended to five fingers.
  Covers glove selection and sizing, and left-versus-right glove handedness.
- `Part-6-Wiring-the-Glove-Harness` — new; carries the reversed silk-screen warning and
  the finger-to-port mapping table for both left and right gloves
- `Part-7-Enclosure-and-Mounting` — new, 🚧 stub; no interim enclosure is recommended
- `Part-8-First-Power-On-and-Full-Bench-Test` — new; full-system test of the assembled
  glove. `MOTOR_TEST:<n>` per channel to confirm the harness mapping, LED status codes,
  battery behavior, and first charge.
- `Part-9-Using-the-Gloves` — new; BuzzahBuddy app. Must cover, explicitly: pairing a
  glove to the app, pairing the two gloves to each other, confirming PRIMARY/SECONDARY
  maps to the intended hands, verifying bilateral sync, adjusting intensity and profile
  settings, and updating firmware after the initial build. Replaces the archived
  CircuitPython/Mu Editor page, which is obsolete.

**Reference**
- `Parts-and-Tools-List` — rebuilt from the v3 BOM; includes a refreshed cost estimate
  (v2's figure is invalid — the v3 BOM and JLCPCB assembly scope both changed) and
  per-step quantities that reconcile against each `Part-N` page
- `Troubleshooting` — new
- `_Sidebar` — new; the wiki currently has no navigation
- `_Footer` — existing, one line; reviewed for v3 accuracy, otherwise untouched

**Deleted:** `archive/` (13 tracked files).

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
| Battery sense | DRV2605 VBAT register `0x21` over I2C; no divider | `hardware.cpp:257` (`DRV_REG_VBAT`), `board_config.h:42-43` |
| Status LED | WS2812B on GPIO4 | BOM `D1`, `board_config.h:32` |
| I2C | TCA9548A mux at `0x70`, DRV2605s at `0x5A` | `board_config.h:53-54` |
| IMU | LSM6DS3 populated but unused by current firmware | BOM `U1` |
| Charging | ⚠️ No charge IC appears in the v3 BOM; charging is presumably via the XIAO ESP32-S3's onboard LiPo charger over USB-C. Must be confirmed on hardware before it is documented. | BOM (absence) |
| Software | PlatformIO firmware, BuzzahBuddy app, BlueBuzzah-Updater | firmware repo |

## Enclosure Gap

The enclosure is the one thing standing between a working pair of gloves and a wearable
pair. There is no v3 case design yet, and the v2 ABS case is not a substitute — it is cut
for a Feather footprint with 4-pin connectors and will not fit a XIAO-based board with six
2-pin JSTs.

This must be stated **at the top of `Home`, before a reader spends money**, not discovered
at Part-7. The wiki says plainly: you can build, wire, flash, and bench-test a complete
pair by following this guide; you cannot yet mount them on a glove for daily wear.

`Part-9-Using-the-Gloves` is therefore scoped to bench and desk use — app pairing, sync
verification, settings, running a session with the boards not yet enclosed. It does not
describe wearing the gloves for unsupervised therapy. When the enclosure lands, Part-7
gains real content and Part-9 extends; nothing else in the structure changes.

## Gap Handling

Three callout states, used consistently and aggregated on `Build-Status`:

- 🚧 **In design** — the enclosure. States that it is unavailable and that no substitute
  is recommended.
- 📷 **Photos pending** — steps are written completely in text; the image slot is marked.
- ⚠️ **Needs hardware verification** — any claim derived from schematic or firmware rather
  than observed on a built unit.

Each flag is a single-line deletion once resolved.

## Asset Work (`BlueBuzzah-Hardware`)

Copy from the `PentaBuzzer` repo. The scope is deliberately narrow — "KiCad source" means
the project's own design files, **not** its vendored third-party library tree.

**Copy (~8.7 MB total):**

| Destination | Files | Size |
| --- | --- | --- |
| `PCB/v3/` | `jlc_pcb_gerbers.zip`, `BOM_JCLPCB_*.csv`, `CPL_JLCPCB_*.csv` | 132 KB |
| `PCB/v3/kicad/` | `*.kicad_sch` (both), `*.kicad_pcb`, `*.kicad_pro`, `fp-lib-table`, `sym-lib-table` | ~1 MB |
| `3D-Print-Models/` | `Penta_Buzzer_mini_V2_2_single_side.step` | 7.5 MB |

**Do not copy:** `PentaBuzzer/Libraries/` (18 MB). It is third-party content carrying its
own licenses — `OPL_Kicad_Library-master/LICENSE` and `113991054/License.txt` — and
vendoring it into an MIT-licensed repo creates an undisclosed mixed-license tree for no
builder benefit. Ordering a board needs only the gerbers, BOM, and CPL, none of which
depend on the libraries.

**Consequence to document, not hide:** without `Libraries/`, the copied KiCad project will
not open with all footprints and symbols resolved. `PCB/v3/kicad/README.md` must state
this plainly and point at the `PentaBuzzer` repo as the place to do actual schematic
editing. The copy exists so the design is readable and archivable alongside the board a
builder orders — not as an editing environment.

**Drift.** `PentaBuzzer` remains a live, independently-versioned repo. This copy is a
point-in-time snapshot and will go stale silently. `PCB/v3/README.md` records the source
commit hash so staleness is at least detectable. There is no automatic re-sync; refreshing
the copy is a manual step whenever the board is revised. This is the accepted cost of the
one-repo-for-builders decision.

The existing v2 assets stay in place and untouched. The wiki links to neither them nor any
`PCB/v2` path.

## Verification

1. **Claim traceability** — every electrical and mechanical claim cites its source file,
   BOM row, or schematic net, delivered as a review table for spot-checking.
2. **Link check** — automated pass over all `[[wikilinks]]` and repo-relative paths, run
   before merge. It must do two things, not one: resolve every new `PCB/v3/` link, **and
   fail on any `PCB/v2` path, `archive/` reference, or v2-named page link** appearing in
   wiki content. The second half is what keeps "no public v2 content" true over time
   rather than only on merge day.
3. **Procedural dry-run** — a sequential read of Part-1 through Part-9 as a builder would
   follow them, checking for missing steps, steps that depend on something not yet done,
   and tools or parts used but never introduced. The fact checks above catch wrong claims;
   this catches a correct guide that cannot actually be followed.
4. **Parts reconciliation** — every quantity in `Parts-and-Tools-List` cross-checked
   against actual consumption across the Part pages. This is the error class that costs a
   reader real money: they buy to the list, then run short mid-build.
5. **Hardware pass** — the ⚠️ flags form a checklist to walk with a built v3 glove.

## Out of Scope

- Designing the enclosure.
- Producing build photography.
- Any v2 documentation, migration path, or owner communication.
- Fixing the stale v2 battery-monitoring row in the firmware README. It contradicts the
  section below it and should be corrected, but in the firmware repo, not here.
