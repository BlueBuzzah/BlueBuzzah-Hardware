# BlueBuzzah v3 Hardware Wiki Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the public hardware wiki as a v3-only, end-to-end build guide for BlueBuzzah v3 (Seeed XIAO ESP32-S3, five motors), and copy the v3 design files into `BlueBuzzah-Hardware` so builders use one repo.

**Architecture:** Two repos, two branches, both already created. Content is written to `BlueBuzzah-Hardware.wiki` on branch `v3-docs`; design files and tooling land in `BlueBuzzah-Hardware` on branch `v3-docs`. A link-check script is built first so every later content task has a real test to run. All 17 pages ship in one merge to the wiki's `master` because GitHub wikis have no PR mechanism.

**Tech Stack:** Markdown (GitHub wiki flavor), Python 3 (link-check script, stdlib only), git.

**Spec:** `docs/superpowers/specs/2026-07-31-v3-hardware-wiki-design.md`

## Global Constraints

- **Naming:** "BlueBuzzah v3" throughout. "PentaBuzzer" / "Penta Buzzer mini V2.2" appears **only** where a builder needs it to locate design files (the PentaBuzzer repo link in Part-1 and `PCB/v3/kicad/README.md`).
- **No public v2 content.** Exactly one sanctioned exception: a link to `Instructions/Blue Buzzah Build Documentation.pdf`, on `Home` and `Parts-and-Tools-List`. No v2 build steps, parts, wiring, or pages anywhere.
- **No AI attribution** in any commit message, page, or file. No "Generated with", no `Co-Authored-By: Claude`.
- **Wiki links** use GitHub wiki double-bracket syntax: `[[Page Title]]`, matching the filename with dashes replaced by spaces.
- **Repo links** from the wiki are absolute GitHub URLs to `BlueBuzzah/BlueBuzzah-Hardware`, because wiki pages cannot use repo-relative paths.
- **Every ⚠️ claim** derived from schematic/firmware rather than observed hardware carries the callout defined in Task 3 and an entry on `Build-Status`.
- **Wiki branch:** `v3-docs`. Merge target: `master` (the wiki remote's only branch). Never merge to `main`.
- **Hardware repo branch:** `v3-docs`.
- **Firmware facts are cited from these exact sources** (do not re-derive):
  - `MAX_ACTUATORS 5`, `HW_VERSION_STRING "v3"` — `include/board_config.h:29-31`
  - `MOTOR_SILK_PORT(finger) = 5 - finger` — `include/board_config.h:47`
  - `FINGER_INDEX 0, FINGER_MIDDLE 1, FINGER_RING 2, FINGER_PINKY 3, FINGER_THUMB 4` — `include/config.h:214-218`
  - `ENABLE_PIN_OVERRIDE 1`, `POWER_SWITCH_PIN_OVERRIDE 3`, `USB_POW_DETECT_PIN_OVERRIDE 2`, `NEOPIXEL_PIN_OVERRIDE 4`, `SDA 5`, `SCL 6` — `include/board_config.h:32-40`
  - `TCA9548A_ADDRESS 0x70`, `DRV2605_ADDRESS 0x5A` — `include/board_config.h:53-54`
  - `DRV_REG_VBAT = 0x21` — `src/hardware.cpp:257`
  - LED battery states: orange slow-blink < 3.4V, rapid red < 3.3V, purple flashing = peer lost — `README.md:160-172`

---

## Canonical Finger-to-Port Table

This table is the single most consequential fact in the wiki. It is reproduced verbatim in
Part-6 and Part-8. Derived from `MOTOR_SILK_PORT(finger) = 5 - finger` with finger indices
from `config.h:214-218`.

| Finger | Firmware index | **Silk-screen port on PCB** |
| ------ | -------------- | --------------------------- |
| Index  | 0              | **5**                       |
| Middle | 1              | **4**                       |
| Ring   | 2              | **3**                       |
| Pinky  | 3              | **2**                       |
| Thumb  | 4              | **1**                       |

`MOTOR_DIAG` prints `[DIAG] silk port N (FN)` per channel (`src/hardware.cpp:498`), so the
device itself confirms this mapping on real hardware.

---

## File Structure

**`BlueBuzzah-Hardware`** (branch `v3-docs`)

| Path | Responsibility |
| ---- | -------------- |
| `PCB/v3/` | Gerbers, BOM, CPL — everything needed to order the board |
| `PCB/v3/README.md` | Source commit hash, what each file is for, how to order |
| `PCB/v3/kicad/` | Design source (schematics, PCB, project, lib tables) |
| `PCB/v3/kicad/README.md` | States footprints will not resolve without the PentaBuzzer `Libraries/` tree; points there for editing |
| `3D-Print-Models/Penta_Buzzer_mini_V2_2_single_side.step` | Board model for enclosure design |
| `tools/wiki_check.py` | Link + v2-leakage checker, run against a wiki checkout |

**`BlueBuzzah-Hardware.wiki`** (branch `v3-docs`) — 17 pages plus sidebar/footer

| Path | Responsibility |
| ---- | -------------- |
| `Home.md` | Landing, spec table, enclosure limitation, v2 PDF link |
| `Disclaimers.md`, `Acknowledgements.md` | Existing; reviewed |
| `Build-Status.md` | Every open item: 🚧, 📷, ⚠️ |
| `Introduction.md`, `Why-We-Use-Spring-Tactors.md` | Background |
| `Part-1-Ordering-the-PCB.md` … `Part-9-Using-the-Gloves.md` | The build |
| `Parts-and-Tools-List.md` | BOM-derived parts, tools, cost, v2 PDF link |
| `Troubleshooting.md` | Symptom-to-cause table |
| `_Sidebar.md`, `_Footer.md` | Navigation |
| ~~`archive/`~~ | Deleted (13 tracked files) |

---

## Task 1: Copy v3 design files into the hardware repo

**Files:**
- Create: `PCB/v3/` (gerbers, BOM, CPL), `PCB/v3/README.md`
- Create: `PCB/v3/kicad/` (schematics, PCB, project, lib tables), `PCB/v3/kicad/README.md`
- Create: `3D-Print-Models/Penta_Buzzer_mini_V2_2_single_side.step`

**Interfaces:**
- Produces: the GitHub URLs Part-1 and Parts-and-Tools-List link to. Later tasks depend on these exact paths existing.

- [ ] **Step 1: Record the source commit so staleness is detectable**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/PentaBuzzer
git rev-parse HEAD
```

Save the output — it goes into `PCB/v3/README.md` in Step 3.

- [ ] **Step 2: Copy the files (exclude `Libraries/`)**

```bash
cd /Users/rbonestell/Development/BlueBuzzah
mkdir -p BlueBuzzah-Hardware/PCB/v3/kicad

cp PentaBuzzer/jlc_manufacturing_files/* BlueBuzzah-Hardware/PCB/v3/

cp PentaBuzzer/*.kicad_sch \
   PentaBuzzer/*.kicad_pcb \
   PentaBuzzer/*.kicad_pro \
   PentaBuzzer/fp-lib-table \
   PentaBuzzer/sym-lib-table \
   BlueBuzzah-Hardware/PCB/v3/kicad/

cp PentaBuzzer/Penta_Buzzer_mini_V2_2_single_side.step \
   BlueBuzzah-Hardware/3D-Print-Models/
```

Do **not** copy `PentaBuzzer/Libraries/` — 18 MB of third-party content with its own
licenses (`OPL_Kicad_Library-master/LICENSE`, `113991054/License.txt`). Vendoring it into
this MIT repo creates an undisclosed mixed-license tree and no builder needs it to order a
board.

- [ ] **Step 3: Verify the copy is the expected size and shape**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware
du -sh PCB/v3 3D-Print-Models
ls PCB/v3 PCB/v3/kicad
```

Expected: `PCB/v3` ≈ 1.1 MB, `3D-Print-Models` ≈ 8 MB (7.5 MB STEP plus the existing v2
STL). `PCB/v3` contains a gerbers zip, a BOM csv, and a CPL csv. If `PCB/v3` is tens of
megabytes, `Libraries/` was copied by mistake — remove it and redo Step 2.

- [ ] **Step 4: Write `PCB/v3/README.md`**

Must contain: what each file is (gerbers zip = board fabrication, BOM = parts to
assemble, CPL = placement), the source commit hash from Step 1 with a line stating this is
a point-in-time snapshot of the PentaBuzzer repo that will not auto-update, and a one-line
pointer to `kicad/` for design source.

- [ ] **Step 5: Write `PCB/v3/kicad/README.md`**

Must state plainly: these files are here so the design is readable and archivable
alongside the board you order; the project will **not** open with all footprints and
symbols resolved because the third-party `Libraries/` tree is deliberately not vendored;
do actual schematic editing in the PentaBuzzer repo.

- [ ] **Step 6: Commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware
git add PCB/v3 3D-Print-Models
git commit -m "feat: add v3 PCB manufacturing files, KiCad source, and board model"
```

---

## Task 2: Build the wiki check script

Written before any page, so every content task has a real test to run.

**Files:**
- Create: `tools/wiki_check.py`

**Interfaces:**
- Produces: `python3 tools/wiki_check.py <wiki-path>` — exits 0 on pass, 1 on failure, printing one line per violation. Every later task runs this.

- [ ] **Step 1: Write the script**

```python
#!/usr/bin/env python3
"""Check the BlueBuzzah v3 wiki for broken links and v2 leakage.

Usage: python3 tools/wiki_check.py ../BlueBuzzah-Hardware.wiki
"""
import re
import sys
from pathlib import Path

# The single sanctioned v2 reference, allowlisted by exact path, not pattern.
V2_ALLOWED = "Instructions/Blue Buzzah Build Documentation.pdf"

# Anything else v2-ish is a failure.
V2_FORBIDDEN = re.compile(r"PCB/v2|archive/|BlueBuzzah 2\.0|Legacy[- ]v2", re.IGNORECASE)

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
# Image embeds: ![alt](path). Relative paths under images/ are correct here and
# resolve fine in GitHub wikis - check that the file exists rather than reject it.
IMGLINK = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
# Page links: [text](url), excluding image embeds via the negative lookbehind.
MDLINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def check(wiki: Path) -> list[str]:
    errors = []
    pages = sorted(wiki.glob("*.md"))
    names = {p.stem.replace("-", " ").lower() for p in pages}

    if (wiki / "archive").exists():
        errors.append("archive/ still exists - it is public surface and must be deleted")

    for page in pages:
        text = page.read_text(encoding="utf-8")

        for line_no, line in enumerate(text.splitlines(), 1):
            stripped = line.replace(V2_ALLOWED, "")
            if V2_FORBIDDEN.search(stripped):
                errors.append(f"{page.name}:{line_no}: forbidden v2 reference")

        for target in WIKILINK.findall(text):
            if target.strip().lower() not in names:
                errors.append(f"{page.name}: broken wikilink [[{target}]]")

        images = set(IMGLINK.findall(text))
        for src in images:
            if src.startswith(("http://", "https://")):
                continue
            if not (wiki / src).is_file():
                errors.append(f"{page.name}: missing image '{src}'")

        for url in MDLINK.findall(text):
            if url in images:
                continue
            if url.startswith(("http://", "https://", "#")):
                continue
            errors.append(f"{page.name}: non-absolute link '{url}' "
                          "- wiki pages cannot use repo-relative paths")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    wiki = Path(sys.argv[1])
    if not wiki.is_dir():
        print(f"not a directory: {wiki}")
        return 2

    errors = check(wiki)
    for e in errors:
        print(e)
    print(f"\n{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run it and verify it FAILS on the current wiki**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware
python3 tools/wiki_check.py ../BlueBuzzah-Hardware.wiki
```

Expected: **exit 1**, reporting `archive/ still exists` and a forbidden v2 reference in
`Home.md` (it is titled "BlueBuzzah 2.0 Hardware Wiki"). If it exits 0, the script is not
detecting anything and is broken — fix it before continuing.

- [ ] **Step 3: Commit**

```bash
git add tools/wiki_check.py
git commit -m "feat: add wiki link and v2-leakage checker"
```

---

## Task 3: Wiki scaffolding — delete archive, add navigation and status

**Files:**
- Delete: `archive/` (13 tracked files) in the wiki repo
- Create: `_Sidebar.md`, `Build-Status.md`
- Modify: `_Footer.md`

**Interfaces:**
- Consumes: `tools/wiki_check.py` from Task 2.
- Produces: the callout format every later page uses, and `Build-Status.md` which every later task appends to.

- [ ] **Step 1: Delete the archive**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware.wiki
git rm -r archive/
```

This removes 13 tracked `.md` files. The untracked
`archive/Blue Buzzah Build Documentation.pdf` is a local scratch copy — delete it from
disk too. The committed original stays at
`BlueBuzzah-Hardware/Instructions/Blue Buzzah Build Documentation.pdf` and is untouched.

- [ ] **Step 2: Write `_Sidebar.md`**

Lists all 17 pages in reading order under four headings — Getting Started, Understanding
the Project, Build, Reference — using `[[Page Title]]` links. The wiki currently has no
navigation at all, so this is the primary way readers move around.

- [ ] **Step 3: Define the callout format in `Build-Status.md`**

Three states, used verbatim on every page that needs one:

```markdown
> 🚧 **In design.** The v3 enclosure has not been designed yet. You can build,
> wire, flash, and bench-test a complete pair of gloves, but you cannot yet mount
> them on a glove for daily wear. No substitute enclosure is recommended.

> 📷 **Photos pending.** These steps are complete in text; illustrations are not
> yet available.

> ⚠️ **Needs hardware verification.** This is derived from the schematic and
> firmware source, not yet confirmed on an assembled board.
```

`Build-Status.md` then carries three tables (one per state) listing every page currently
flagged and what specifically is missing. Seed it with the enclosure (🚧, Part-7) and the
charging claim (⚠️, Part-8 — no charge IC in the v3 BOM; charging is presumed to run
through the XIAO's onboard LiPo charger over USB-C and must be confirmed on hardware).

- [ ] **Step 4: Review `_Footer.md`**

One line. Confirm it contains no v2 reference; leave it otherwise untouched.

- [ ] **Step 5: Run the check**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware
python3 tools/wiki_check.py ../BlueBuzzah-Hardware.wiki
```

Expected: the `archive/` error is gone. `Home.md` still fails on "BlueBuzzah 2.0" — that
is fixed in Task 4. Broken wikilinks from `_Sidebar.md` to pages not yet written are
expected at this stage.

- [ ] **Step 6: Commit**

Stage explicit paths — **never `git add -A` in the wiki repo.** It carries an uncommitted
edit to `Acknowledgements.md` made by the repository owner outside this plan; sweeping it
into an unrelated commit would publish unreviewed content. Leave that file alone; Task 4
handles it.

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware.wiki
git add _Sidebar.md Build-Status.md _Footer.md
git add -u archive/
git status --short   # confirm Acknowledgements.md is still unstaged
git commit -m "docs: remove v2 archive, add sidebar and build status"
```

---

## Task 4: Home, Disclaimers, Acknowledgements

**Files:**
- Modify: `Home.md` (currently titled "BlueBuzzah 2.0 Hardware Wiki" — full rewrite)
- Modify: `Disclaimers.md`, `Acknowledgements.md`

**Interfaces:**
- Consumes: callout format from Task 3.
- Produces: the spec table and framing every other page assumes.

- [ ] **Step 1: Rewrite `Home.md`**

Required content, in this order:

1. Title: "BlueBuzzah v3 Hardware Wiki".
2. One paragraph: what this is (DIY vibrotactile glove for Parkinson's therapy research,
   based on Dr. Peter Tass's vCR research), who it is for.
3. **The enclosure limitation, before anything else a reader might act on.** Use the 🚧
   callout from Task 3. A reader must learn this before spending money, not at Part-7.
4. Spec table — no v2 column: MCU Seeed XIAO ESP32-S3; 5 motors (index, middle, ring,
   pinky, thumb); BLE NimBLE; 5× DRV2605L haptic drivers; TCA9548A I2C mux; WS2812B status
   LED; SPDT slide switch with deep sleep; battery sensing via the DRV2605 VBAT register;
   LiPo required.
5. Build path overview: one line per Part-1 through Part-9 with `[[links]]`.
6. Link to `[[Disclaimers]]` — prominent, this is a medical-adjacent DIY device.
7. The single v2 reference. Exact framing: historical reference for owners of earlier
   hardware, not an alternative build path. Absolute URL to
   `https://github.com/BlueBuzzah/BlueBuzzah-Hardware/blob/main/Instructions/Blue%20Buzzah%20Build%20Documentation.pdf`.

- [ ] **Step 2: Review `Disclaimers.md`**

Keep all four sections (Medical, Liability, Electrical Safety, Research Context). The
Electrical Safety section already covers lithium batteries, shock, fire, and burns —
leave it. Change only "Blue Buzzah gloves" phrasing if it implies v2 specifically. Do not
add LiPo handling/charging guidance; that is explicitly out of scope.

- [ ] **Step 3: Review `Acknowledgements.md`**

Seven lines. Confirm no v2-specific claims; otherwise leave as-is.

- [ ] **Step 4: Run the check**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware
python3 tools/wiki_check.py ../BlueBuzzah-Hardware.wiki
```

Expected: no forbidden-v2 errors remain. The sanctioned PDF link must **not** be flagged —
if it is, the allowlist in `wiki_check.py` is wrong, and that is a script bug to fix, not a
reason to remove the link.

- [ ] **Step 5: Commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware.wiki
git add Home.md Disclaimers.md Acknowledgements.md
git commit -m "docs: rewrite Home for v3, review disclaimers and acknowledgements"
```

---

## Task 5: Introduction and Why We Use Spring Tactors

**Files:**
- Create: `Introduction.md`, `Why-We-Use-Spring-Tactors.md`

**Interfaces:**
- Consumes: nothing.
- Produces: background context Part-3 refers to when explaining the spring design.

Source material: the deleted `archive/Blue-Buzzah-Introduction.md` and
`archive/Why-We-Use-Spring-Tactors.md`. They were removed in Task 3, so recover them from
the commit before that deletion — find it and read the file with:

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware.wiki
DEL=$(git log --diff-filter=D --format=%H -1 -- archive/)
git show "$DEL^:archive/Why-We-Use-Spring-Tactors.md"
git show "$DEL^:archive/Blue-Buzzah-Introduction.md"
```

Both
are generation-neutral — the therapy rationale and the spring-mount argument do not depend
on which MCU drives the motors.

- [ ] **Step 1: Write `Introduction.md`**

Adapt the archived introduction. Cover: what vCR therapy is, the Tass research basis, what
the gloves do, what building one involves at a high level, and who should not attempt this
alone. Strip every v2 hardware reference (Feather, 4 motors, 4-pin connectors, CircuitPython).
State five fingers, not four.

- [ ] **Step 2: Write `Why-We-Use-Spring-Tactors.md`**

Adapt the archived page essentially intact — it argues that a spring-mounted LRA delivers a
stronger sensation at the skin than a rigidly mounted one, which is unchanged in v3. Remove
any "four tactors per glove" counts; v3 has five.

- [ ] **Step 3: Run the check and commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah
python3 BlueBuzzah-Hardware/tools/wiki_check.py BlueBuzzah-Hardware.wiki
cd BlueBuzzah-Hardware.wiki
git add Introduction.md Why-We-Use-Spring-Tactors.md
git commit -m "docs: add v3 introduction and spring tactor rationale"
```

---

## Task 6: Part-1 Ordering the PCB

**Files:**
- Create: `Part-1-Ordering-the-PCB.md`

**Interfaces:**
- Consumes: `PCB/v3/` URLs from Task 1.
- Produces: the ordered board Part-2 smoke-tests.

- [ ] **Step 1: Write the page**

Required content:

1. What you are ordering: one assembled PCB per glove, so **two** for a pair.
2. JLCPCB order walkthrough: upload the gerbers zip, then the BOM and CPL for assembly.
   Link all three by absolute URL into `PCB/v3/`.
3. What arrives already assembled — this is the big v3 simplification. The XIAO ESP32-S3,
   all five DRV2605L drivers, the TCA9548A mux, the WS2812B LED, the slide switch, and
   **all six 2-pin JST-PH sockets** (five motors plus battery) are placed by JLCPCB. The
   builder solders no connectors.
4. Soldering requirements, absorbed from the archived `Soldering-Requirements.md`: for v3
   this is limited to the tactor wiring in Part-3. Say so plainly rather than carrying over
   v2's board-level soldering section.
5. What is **not** included and must be sourced separately: LRAs, springs, gloves, battery,
   wire. Link `[[Parts and Tools List]]`.
6. Lead time and cost expectations, flagged as varying by supplier and quantity.

- [ ] **Step 2: Run the check and commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah
python3 BlueBuzzah-Hardware/tools/wiki_check.py BlueBuzzah-Hardware.wiki
cd BlueBuzzah-Hardware.wiki
git add Part-1-Ordering-the-PCB.md
git commit -m "docs: add Part 1 ordering the v3 PCB"
```

---

## Task 7: Part-2 Flashing and smoke-testing the bare board

The highest-value page in the build sequence: it is what stops a builder discovering a dead
board after five stages of irreversible assembly.

**Files:**
- Create: `Part-2-Flashing-and-Smoke-Testing-the-Bare-Board.md`
- Modify: `Build-Status.md`

**Interfaces:**
- Consumes: the assembled board from Part-1.
- Produces: a flashed, role-configured, verified-alive board for Part-3 onward.

- [ ] **Step 1: Write the flashing section**

Two routes, BlueBuzzah-Updater first as the supported path:

- **Updater (recommended):** connect over USB-C, the app labels v3 boards
  "BlueBuzzah v3 (port)", pick firmware, flash, then set role. Note that batch flashing
  cannot mix v2 and v3 boards in one run.
- **PlatformIO (advanced):** `pio run -e pentabuzzer_esp32s3 -t upload`, serial monitor at
  115200 baud.

Role assignment: one glove `SET_ROLE:PRIMARY`, the other `SET_ROLE:SECONDARY`. Both gloves
need firmware; they are not interchangeable once roles are set. Record which physical board
got which role — it determines hand assignment in Part-5.

**Do not duplicate the Updater's own documentation.** It has a wiki already; link to it
and keep this page focused on what a *builder* needs at this point in the build:

- https://github.com/BlueBuzzah/BlueBuzzah-Updater/wiki/Getting-Started — installing the Updater
- https://github.com/BlueBuzzah/BlueBuzzah-Updater/wiki/Understanding-Device-Roles — what PRIMARY/SECONDARY mean

Also state here that the Updater is the same tool and workflow used for **future firmware
updates**, not just this first flash — so nobody assumes it is a one-time build step.

- [ ] **Step 2: Write the smoke-test section**

State the power requirement first, as its own callout — it is the single most common
"my board is dead" false alarm:

```markdown
> **A battery is required.** The DRV2605 drivers run from VBat, so motors will not
> run on USB power alone. A board that flashes fine over USB and buzzes nothing is
> usually a board with no battery connected.
```

Then: connect a LiPo, set the slide switch on, and run `MOTOR_DIAG` over serial. It buzzes
every channel and prints `[DIAG] silk port N (FN)` per channel. Have the builder hold one
loose LRA against each port in turn to confirm all five drive. Also run `MOTOR_PRESENT`
(open-load probe across all ports) and `MOTOR_TEST:<n>` for a single channel.

Expected LED behavior: breathing blue at idle; purple flashing means the peer glove is not
connected, which is normal when testing one board alone.

State explicitly: **do not proceed to Part-3 until both boards pass.** Everything after
this point is difficult to undo.

- [ ] **Step 3: Add the ⚠️ charging entry to `Build-Status.md`**

No charge IC appears in the v3 BOM; charging presumably runs through the XIAO's onboard
LiPo charger over USB-C. Flag it ⚠️ against Part-8 until confirmed on hardware.

- [ ] **Step 4: Run the check and commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah
python3 BlueBuzzah-Hardware/tools/wiki_check.py BlueBuzzah-Hardware.wiki
cd BlueBuzzah-Hardware.wiki
git add Part-2-Flashing-and-Smoke-Testing-the-Bare-Board.md Build-Status.md
git commit -m "docs: add Part 2 flashing and bare-board smoke test"
```

---

## Task 8: Part-3 Building the Tactors, Part-4 LRA Housing Assembly

**Files:**
- Create: `Part-3-Building-the-Tactors.md`
- Rename: `LRA-Housing-Assembly.md` → `Part-4-LRA-Housing-Assembly.md`

**Interfaces:**
- Consumes: verified boards from Part-2.
- Produces: ten assembled tactors (five per glove) for Part-5.

**Boundary — do not duplicate.** Part-3 ends with a wired, tested, bare LRA. Part-4 begins
from that and covers only mechanical housing assembly. Wire tinning and soldering
instructions appear in Part-3 **only**.

- [ ] **Step 1: Write `Part-3-Building-the-Tactors.md`**

Adapt the archived tactor page, recovered the same way as in Task 5:

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware.wiki
DEL=$(git log --diff-filter=D --format=%H -1 -- archive/)
git show "$DEL^:archive/Part-3-Building-the-Tactors.md"
```

Keep: LRA terminal
tinning, the delicate wire-to-LRA soldering technique, heat-shrink strain relief, and the
per-tactor troubleshooting table — all unchanged for v3.

Change for v3:
- **Five tactors per glove, ten total** (v2 said four/eight).
- **2-pin JST-PH connectors**, not 4-pin. Delete the v2 4-pin pinout table entirely; there
  are no unused pins. Pin 1 = LRA +, pin 2 = LRA −.
- Test each tactor against a Part-2-verified board using `MOTOR_TEST:<n>` before moving on.

- [ ] **Step 2: Rename and update the housing page**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware.wiki
git mv LRA-Housing-Assembly.md Part-4-LRA-Housing-Assembly.md
```

The existing content is good and generation-neutral — keep it. Two edits: remove the
prerequisite line about tinning wire (that now lives in Part-3), and add a buzz-check step
before the housing is closed, since dovetail assembly is difficult to reverse.

- [ ] **Step 3: Confirm the images still resolve**

The page references 22 files under `images/lra-housing/` as relative paths, which is
correct for a GitHub wiki. The directory is untouched by the rename, so they should still
resolve — `wiki_check.py` verifies each one exists and will report `missing image` if not.

- [ ] **Step 4: Run the check and commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah
python3 BlueBuzzah-Hardware/tools/wiki_check.py BlueBuzzah-Hardware.wiki
cd BlueBuzzah-Hardware.wiki
git add Part-3-Building-the-Tactors.md
git add -u Part-4-LRA-Housing-Assembly.md LRA-Housing-Assembly.md
git commit -m "docs: add Part 3 tactor build, renumber housing assembly to Part 4"
```

---

## Task 9: Part-5 Mounting Tactors, Part-6 Wiring the Harness

Part-6 carries the canonical finger-to-port table. Get it wrong and every glove is miswired.

**Files:**
- Create: `Part-5-Mounting-Tactors-in-Glove-Fingertips.md`
- Create: `Part-6-Wiring-the-Glove-Harness.md`
- Modify: `Build-Status.md`

**Interfaces:**
- Consumes: ten tactors from Part-4, role-assigned boards from Part-2.
- Produces: two wired gloves for Part-8.

- [ ] **Step 1: Write `Part-5-Mounting-Tactors-in-Glove-Fingertips.md`**

Adapt the archived fingertip-mounting page, recovered the same way as in Task 5
(`git show "$DEL^:archive/Part-4-Mounting-Tactors-in-Glove-Fingertips.md"`). Extend from four fingers to
five — the thumb is new in v3 and its fingertip geometry differs, so call out that the
thumb tactor sits differently than the finger tactors.

Add two subjects the v2 docs never covered:
- **Glove selection and sizing** — stretchy nitrile-dipped work gloves; fit matters because
  a loose fingertip lets the tactor drift off the contact point.
- **Handedness** — you are building a mirrored pair. Label which glove is left and which is
  right now, and record which role-assigned board pairs with which glove. Getting this wrong
  is only discovered in Part-9 when therapy runs on the wrong hand.

- [ ] **Step 2: Write `Part-6-Wiring-the-Glove-Harness.md` with the reversed-port warning**

Lead with the warning, before any wiring step:

```markdown
> ⚠️ **The motor port labels on the PCB run backwards relative to firmware channels.**
> The silk-screened numbers 1–5 do **not** correspond to fingers in the order you
> would expect. Wire to the table below, not to intuition. Therapy patterns are
> per-finger, so a transposed harness produces a glove that runs the correct pattern
> on the wrong fingers — it will look like it works.
```

Then reproduce the canonical table from the top of this plan verbatim (Index→5, Middle→4,
Ring→3, Pinky→2, Thumb→1), cited to `board_config.h:47` and `config.h:214-218`.

Then: how to verify rather than trust. `MOTOR_DIAG` prints `[DIAG] silk port N (FN)` per
channel, so the board states its own mapping — have the builder run it and confirm each
buzz lands on the intended finger before dressing the wires down. Cover strain relief and
routing so flexing does not fatigue the joints.

- [ ] **Step 3: Add a 📷 entry to `Build-Status.md`**

Part-5 and Part-6 are the two pages most in need of photography. Flag both.

- [ ] **Step 4: Run the check and commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah
python3 BlueBuzzah-Hardware/tools/wiki_check.py BlueBuzzah-Hardware.wiki
cd BlueBuzzah-Hardware.wiki
git add Part-5-Mounting-Tactors-in-Glove-Fingertips.md Part-6-Wiring-the-Glove-Harness.md Build-Status.md
git commit -m "docs: add Part 5 fingertip mounting and Part 6 harness wiring"
```

---

## Task 10: Part-7 Enclosure stub, Part-8 Bench test

**Files:**
- Create: `Part-7-Enclosure-and-Mounting.md`, `Part-8-First-Power-On-and-Full-Bench-Test.md`

**Interfaces:**
- Consumes: wired gloves from Part-6.
- Produces: a verified pair ready for Part-9.

- [ ] **Step 1: Write `Part-7-Enclosure-and-Mounting.md` as an honest stub**

Open with the 🚧 callout. State what is known: the enclosure must house the PCB and a LiPo,
mount to the back of the glove, and route five tactor harnesses to the fingertips. State
plainly that the v2 ABS case is **not** a substitute — it is cut for a Feather footprint
with 4-pin connectors and will not fit a XIAO-based board with six 2-pin JSTs. Do not
suggest a workaround. Link the STEP file in `3D-Print-Models/` for anyone designing their
own, and point at `[[Build Status]]`.

- [ ] **Step 2: Write `Part-8-First-Power-On-and-Full-Bench-Test.md`**

Full-system test of the assembled glove, distinct from Part-2's bare-board check:

- `MOTOR_TEST:<n>` per channel, confirming each fires the intended **finger** — this is
  where a transposed harness from Part-6 gets caught.
- LED status reference: breathing blue idle; purple flashing = peer lost; orange slow-blink
  = battery low below 3.4V; rapid red = critical below 3.3V (`README.md:160-172`).
- Battery behavior and first charge, carrying the ⚠️ charging flag from Task 7 Step 3.
- Both gloves powered together — confirm they discover each other and the purple flashing
  stops.

- [ ] **Step 3: Run the check and commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah
python3 BlueBuzzah-Hardware/tools/wiki_check.py BlueBuzzah-Hardware.wiki
cd BlueBuzzah-Hardware.wiki
git add Part-7-Enclosure-and-Mounting.md Part-8-First-Power-On-and-Full-Bench-Test.md
git commit -m "docs: add Part 7 enclosure stub and Part 8 full bench test"
```

---

## Task 11: Part-9 Using the Gloves

**Files:**
- Create: `Part-9-Using-the-Gloves.md`

**Interfaces:**
- Consumes: bench-tested pair from Part-8.
- Produces: nothing downstream; this is the last build page.

Replaces the archived `Part-6-Adjusting-Buzzah-Settings.md`, which is obsolete — it
describes CircuitPython 9.2.4 and the Mu Editor. None of that applies. Do not carry any of
it forward.

- [ ] **Step 1: Write the page**

Must cover all of:
1. Installing BuzzahBuddy and pairing a glove to the app over BLE.
2. Pairing the two gloves to each other; confirming PRIMARY/SECONDARY map to the intended
   hands (set back in Part-2, physically assigned in Part-5).
3. Verifying bilateral sync, and what to do when it fails.
4. Adjusting intensity and therapy profile settings through the app.
5. Updating firmware after the initial build, via BlueBuzzah-Updater — link to
   https://github.com/BlueBuzzah/BlueBuzzah-Updater/wiki/User-Guide rather than restating
   it, and to
   https://github.com/BlueBuzzah/BlueBuzzah-Updater/wiki/Therapy-Profiles for profile
   details. The Updater wiki owns that content; this page owns the build context around it.

- [ ] **Step 2: Scope the page to bench and desk use**

Because there is no enclosure, this page describes running a session with the boards not
yet mounted on the gloves. It must **not** describe wearing the gloves for unsupervised
therapy. Reference `[[Disclaimers]]`. When the enclosure lands, this page extends.

- [ ] **Step 3: Run the check and commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah
python3 BlueBuzzah-Hardware/tools/wiki_check.py BlueBuzzah-Hardware.wiki
cd BlueBuzzah-Hardware.wiki
git add Part-9-Using-the-Gloves.md
git commit -m "docs: add Part 9 using the gloves with the app"
```

---

## Task 12: Parts and Tools List, Troubleshooting

**Files:**
- Create: `Parts-and-Tools-List.md`, `Troubleshooting.md`

**Interfaces:**
- Consumes: component quantities from every Part page.
- Produces: the list Task 13 reconciles against.

- [ ] **Step 1: Write `Parts-and-Tools-List.md` from the v3 BOM**

Build from `PCB/v3/` BOM, not from the archived v2 list. Per pair of gloves:
- 2× assembled v3 PCB (JLCPCB)
- 10× VLV101040A LRA
- 10× compression spring, 10× 3D-printed housing set
- 2× LiPo battery
- 2× stretchy gloves
- Wire, heat shrink, USB-C cable

Note what is **already on the board** so nobody orders it twice: XIAO ESP32-S3, 5×
DRV2605L, TCA9548A, WS2812B, slide switch, all six JST-PH sockets.

Tools: soldering iron with fine tip, solder, flux, wire strippers/cutters, heat gun,
fabric scissors, multimeter, helping hands.

Refresh the cost estimate — v2's ~$272 figure is invalid because both the BOM and the
JLCPCB assembly scope changed. Present it as an estimate that varies by supplier.

Include the second sanctioned v2 PDF link here, framed for readers who realize at this
point that they have the earlier board.

- [ ] **Step 2: Write `Troubleshooting.md`**

Symptom → cause → fix table, aggregating failure modes from across the build:

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Board flashes but no motor buzzes | No battery connected | DRV2605s run from VBat; connect a LiPo |
| Correct pattern, wrong fingers | Harness transposed | Rewire to the Part-6 table; confirm with `MOTOR_DIAG` |
| One channel dead | Cold joint at the LRA, or open harness | `MOTOR_PRESENT` to probe; reflow |
| Purple flashing forever | Peer glove not found | Confirm both roles set and both powered |
| Orange slow blink | Battery below 3.4V | Charge |
| Rapid red flash | Battery below 3.3V | Charge immediately |
| Weak vibration | Poor LRA solder joint | Reflow |

- [ ] **Step 3: Run the check and commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah
python3 BlueBuzzah-Hardware/tools/wiki_check.py BlueBuzzah-Hardware.wiki
cd BlueBuzzah-Hardware.wiki
git add Parts-and-Tools-List.md Troubleshooting.md
git commit -m "docs: add v3 parts and tools list and troubleshooting"
```

---

## Task 13: Verification passes

All five spec verification passes, run against the complete branch before merge.

**Files:**
- Create: `docs/superpowers/plans/2026-07-31-v3-wiki-claim-traceability.md` in the hardware repo
- Modify: whatever the passes turn up

- [ ] **Step 1: Link check must pass clean**

```bash
cd /Users/rbonestell/Development/BlueBuzzah
python3 BlueBuzzah-Hardware/tools/wiki_check.py BlueBuzzah-Hardware.wiki
```

Expected: **exit 0**, `0 problem(s)`. Every `[[wikilink]]` resolves, no forbidden v2
reference, and the sanctioned PDF link present and allowlisted. Fix anything it reports.

- [ ] **Step 2: Claim traceability table**

Write a table of every electrical and mechanical claim in the wiki against its source
(file:line, BOM row, or schematic net), so the user can spot-check rather than re-derive.
Every claim with no hardware-observed source gets ⚠️ and a `Build-Status` row.

- [ ] **Step 3: Procedural dry-run**

Read Part-1 → Part-9 sequentially as a builder would follow them. Check for: missing steps,
steps depending on something not yet done, tools or parts used but never introduced, and
forward references. The fact checks catch wrong claims; this catches a correct guide that
cannot be followed.

- [ ] **Step 4: Parts reconciliation**

Cross-check every quantity in `Parts-and-Tools-List` against actual consumption across the
Part pages. Ten LRAs listed, ten used. This is the error class that costs a reader real
money — they buy to the list, then run short mid-build.

- [ ] **Step 5: Confirm Build-Status is complete**

Every 🚧, 📷, and ⚠️ callout across all 17 pages has a matching `Build-Status` row. Grep
for the callout emoji and compare counts.

- [ ] **Step 6: Commit**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware
git add docs/
git commit -m "docs: add v3 wiki claim traceability and verification results"
```

---

## Task 14: Merge

Do not start until Task 13 passes clean and the user has reviewed.

- [ ] **Step 1: Delete the stray local `main` branch in the wiki repo**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware.wiki
git branch -D main
```

It was never pushed and is not a valid target. Deleting it removes the chance of publishing
to the wrong place.

- [ ] **Step 2: Merge the hardware repo first**

The wiki links to `PCB/v3/` URLs. If the wiki merges first, every ordering link 404s.

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware
git checkout main && git merge v3-docs && git push
```

- [ ] **Step 3: Verify the asset URLs resolve**

Open the `PCB/v3/` gerbers, BOM, and CPL URLs used in Part-1 and confirm each loads on
GitHub. Only then continue.

- [ ] **Step 4: Merge the wiki to `master`**

```bash
cd /Users/rbonestell/Development/BlueBuzzah/BlueBuzzah-Hardware.wiki
git checkout master && git merge v3-docs && git push
```

All 17 pages go live at once. There are no partial merges — a half-migrated wiki would
publish v3 pages alongside the v2 archive this work exists to remove.

- [ ] **Step 5: Verify live**

Load the wiki. Confirm: Home shows v3 and the enclosure callout, the sidebar navigates, no
`archive/` page is reachable, and the v2 PDF link works.
