#!/usr/bin/env python3
"""Build the PCBWay order files for one BlueBuzzah v3 board, not panelized.

    python3 make_pcbway.py

Needs KiCad 10. Writes pcbway/BlueBuzzah_v3_gerbers.zip, _BOM.csv and _centroid.csv,
and doesn't touch the JLCPCB package.

The JLCPCB files can't be reused: they come from the panel, and the CPL is corrected for
JLCPCB's parts library. Here the gerbers come from the bare board, and gerbers, drill and
centroid all measure from the board's lower-left corner, which PCBWay expects. That origin
is set on a temporary copy, so the KiCad project stays as it is.

Centroid Mid X/Y is the footprint origin. On this board that's the body center of every
SMT part; the pad center that make_jlcpcb.py uses is off on U20 (0.62 mm) and J10 (1.46 mm).
Rotation is KiCad's, with no JLCPCB offsets. Pad X/Y marks pin 1, as in PCBWay's sample.
"""
import csv, os, re, shutil, sys, tempfile, zipfile

from make_jlcpcb import (BOARD, GERBER_LAYERS, KICAD_CLI, KICAD_PYTHON, LCSC_BY_VALUE_FOOTPRINT,
                         ROOT, drc, run)

try:
    import pcbnew
except ImportError:
    if os.path.realpath(sys.executable) == os.path.realpath(KICAD_PYTHON):
        sys.exit(f'pcbnew not found in {KICAD_PYTHON}; set KICAD_PYTHON')
    os.execv(KICAD_PYTHON, [KICAD_PYTHON, os.path.abspath(__file__)])

OUT = os.path.join(ROOT, 'pcbway')
NAME = 'BlueBuzzah_v3'
LAYERS = GERBER_LAYERS.replace('B.Paste,', '')  # every part is on top
RES_NOTE = 'Any 1% 0402 equivalent is OK.'

# LCSC number -> manufacturer, part number, description, package, note.
# Copied from LCSC's product pages: turnkey orders need the real manufacturer part number,
# and schematic values aren't always one (LSM6DS3 is the LSM6DS3TR-C here).
PARTS = {
    'C1525': ('Samsung Electro-Mechanics', 'CL05B104KO5NNNC', 'CAP CER 100nF 16V X7R 0402', '0402', ''),
    'C52923': ('Samsung Electro-Mechanics', 'CL05A105KA5NQNC', 'CAP CER 1uF 25V X5R 0402', '0402', ''),
    'C12891': ('Samsung Electro-Mechanics', 'CL31A226KAHNNNE', 'CAP CER 22uF 25V X5R 1206', '1206', 'Alternate: YAGEO CC1206KKX5R8BB226 (LCSC C2178233).'),
    'C19666': ('Samsung Electro-Mechanics', 'CL10A475KO8NNNC', 'CAP CER 4.7uF 16V X5R 0603', '0603', ''),
    'C15525': ('Samsung Electro-Mechanics', 'CL05A106MQ5NUNC', 'CAP CER 10uF 6.3V X5R 0402', '0402', ''),
    'C2874885': ('Worldsemi', 'WS2812B-V5/W', 'Addressable RGB LED', 'SMD5050-4P', 'Moisture sensitive. Alternate: Worldsemi WS2812B-B/W (LCSC C114586).'),
    'C3001948': ('UMW', 'PESD5V0L1UL', 'ESD diode 5V', 'SOD-882', 'Cathode is pad 1, at the closed end of the silkscreen outline.'),
    'C8598': ('JSCJ', 'B5819W SL', 'Schottky diode 40V', 'SOD-123', ''),
    'C5175239': ('HDGC', 'HDGC2001WR-2P', 'Header 2-pin 2 mm right angle', 'Through hole, right angle, 2 mm pitch', 'No substitutes: the battery polarity depends on this part.'),
    'C165948': ('Korean Hroparts Elec', 'TYPE-C-31-M-12', 'USB-C receptacle 16-pin', 'SMD', 'Four shell tabs are through-hole and must be soldered.'),
    'C15127': ('AOS', 'AO3401A', 'MOSFET P-channel 30V 4A', 'SOT-23', ''),
    'C8545': ('JSCJ', '2N7002', 'MOSFET N-channel 60V 115mA', 'SOT-23', ''),
    'C25900': ('UNI-ROYAL', '0402WGF4701TCE', 'RES 4.7k 1% 0402', '0402', RES_NOTE),
    'C26083': ('UNI-ROYAL', '0402WGF1004TCE', 'RES 1M 1% 0402', '0402', RES_NOTE),
    'C25092': ('UNI-ROYAL', '0402WGF220JTCE', 'RES 22R 1% 0402', '0402', f'{RES_NOTE} Example: YAGEO RC0402FR-0722RL (LCSC C114765).'),
    'C25905': ('UNI-ROYAL', '0402WGF5101TCE', 'RES 5.1k 1% 0402', '0402', RES_NOTE),
    'C25744': ('UNI-ROYAL', '0402WGF1002TCE', 'RES 10k 1% 0402', '0402', f'{RES_NOTE} Example: YAGEO RC0402FR-0710KL (LCSC C60490).'),
    'C25741': ('UNI-ROYAL', '0402WGF1003TCE', 'RES 100k 1% 0402', '0402', RES_NOTE),
    'C25770': ('UNI-ROYAL', '0402WGF2703TCE', 'RES 270k 1% 0402', '0402', RES_NOTE),
    'C92657': ('Korean Hroparts Elec', 'K3-1260D-L1', 'Slide switch SPDT right angle', 'Through hole', ''),
    'C720477': ('XUNPU', 'TS-1088-AR02016', 'Tactile switch SPST', 'SMD 4x3 mm', ''),
    'C967633': ('ST', 'LSM6DS3TR-C', 'Accelerometer and gyroscope', 'LGA-14 2.5x3 mm', ''),
    'C130026': ('TI', 'TCA9548APWR', '8-channel I2C switch', 'TSSOP-24', ''),
    'C527464': ('TI', 'DRV2605LDGSR', 'Haptic driver for LRA and ERM', 'VSSOP-10', ''),
    'C2980300': ('Espressif', 'ESP32-S3-WROOM-1U-N8R8', 'Wi-Fi and Bluetooth LE module, external antenna', 'SMD 19.2x18 mm', ''),
    'C7519': ('ST', 'USBLC6-2SC6', 'USB ESD protection', 'SOT-23-6', ''),
    'C424093': ('Microchip', 'MCP73831T-2ACI/OT', 'Li-Po charge controller', 'SOT-23-5', ''),
    'C841192': ('Richtek', 'RT9080-33GJ5', 'LDO regulator 3.3V 600mA', 'TSOT-23-5', ''),
}


def natural(ref):
    prefix, number = re.fullmatch(r'([A-Z]+)(\d+)', ref).groups()
    return prefix, int(number)


def write_gerbers(left, bottom):
    with tempfile.TemporaryDirectory() as tmp:
        for ext in ('.kicad_pcb', '.kicad_pro', '.kicad_dru'):
            shutil.copy(BOARD.replace('.kicad_pcb', ext), tmp)
        board = os.path.join(tmp, os.path.basename(BOARD))
        with open(board) as fh:
            text = fh.read()
        if 'aux_axis_origin' in text:  # a second one could leave the gerbers off the centroid's origin
            sys.exit('the board has a drill/place origin; clear it in KiCad or replace it here')
        with open(board, 'w') as fh:
            fh.write(text.replace('(setup', f'(setup\n\t\t(aux_axis_origin {left} {bottom})', 1))
        out = os.path.join(tmp, 'out')
        os.makedirs(out)
        run(KICAD_CLI, 'pcb', 'export', 'gerbers', '-o', out, '--layers', LAYERS, '--subtract-soldermask',
            '--check-zones', '--use-drill-file-origin', board)
        run(KICAD_CLI, 'pcb', 'export', 'drill', '-o', out + '/', '--format', 'excellon', '--drill-origin', 'plot',
            '--excellon-units', 'mm', '--excellon-separate-th', board)
        path = os.path.join(OUT, f'{NAME}_gerbers.zip')
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
            for name in sorted(os.listdir(out)):
                if not name.endswith('.gbrjob'):
                    z.write(os.path.join(out, name), name)
    print(f'wrote {os.path.relpath(path, ROOT)}')


def lcsc_of(f):
    fp = str(f.GetFPID().GetLibItemName())
    lcsc = (f.GetFieldText('LCSC') if f.HasField('LCSC') else '') or LCSC_BY_VALUE_FOOTPRINT.get((f.GetValue(), fp))
    if lcsc not in PARTS:
        sys.exit(f'no PCBWay part data for {f.GetReference()} ({lcsc}); add it to PARTS')
    return lcsc


def write_bom(footprints):
    lines = {}
    for f in footprints:
        kind = 'SMD' if f.GetAttributes() & pcbnew.FP_SMD else 'THT'
        lines.setdefault((lcsc_of(f), kind), []).append(f.GetReference())
    path = os.path.join(OUT, f'{NAME}_BOM.csv')
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['Item #', 'Designator', 'Qty', 'Manufacturer', 'Mfg Part #', 'Description / Value',
                    'Package/Footprint', 'Type', 'Your Instructions / Notes'])
        ordered = sorted(lines.items(), key=lambda kv: natural(min(kv[1], key=natural)))
        for item, ((lcsc, kind), refs) in enumerate(ordered, 1):
            maker, mpn, desc, package, note = PARTS[lcsc]
            w.writerow([item, ','.join(sorted(refs, key=natural)), len(refs), maker, mpn, desc, package, kind,
                        f'LCSC {lcsc}. {note}'.strip()])
    print(f'wrote {os.path.relpath(path, ROOT)} ({len(lines)} lines)')


def write_centroid(footprints, left, bottom):
    mm = lambda v: f'{v:.3f}mm'
    X = lambda p: pcbnew.ToMM(p.x) - left
    Y = lambda p: bottom - pcbnew.ToMM(p.y)
    path = os.path.join(OUT, f'{NAME}_centroid.csv')
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['Designator', 'Footprint', 'Mid X', 'Mid Y', 'Ref X', 'Ref Y', 'Pad X', 'Pad Y', 'TB', 'Rotation', 'Comment'])
        for f in sorted(footprints, key=lambda f: natural(f.GetReference())):
            pin1 = min((p for p in f.Pads() if p.GetNumber()), key=lambda p: p.GetNumber()).GetPosition()
            at = f.GetPosition()
            w.writerow([f.GetReference(), f.GetFPID().GetLibItemName(), mm(X(at)), mm(Y(at)), mm(X(at)), mm(Y(at)),
                        mm(X(pin1)), mm(Y(pin1)), 'T', f'{f.GetOrientationDegrees() % 360:.2f}', PARTS[lcsc_of(f)][1]])
    print(f'wrote {os.path.relpath(path, ROOT)} ({len(footprints)} placements)')


def main():
    drc(BOARD, parity=True)
    os.makedirs(OUT, exist_ok=True)
    board = pcbnew.LoadBoard(BOARD)
    # The outline's own points: GetBoardEdgesBoundingBox() adds half the 0.1 mm edge line on each side.
    edge = [p for d in board.GetDrawings() if d.GetLayer() == pcbnew.Edge_Cuts for p in (d.GetStart(), d.GetEnd())]
    left, bottom = pcbnew.ToMM(min(p.x for p in edge)), pcbnew.ToMM(max(p.y for p in edge))
    parts = [f for f in board.Footprints() if not f.IsExcludedFromBOM()]
    smt = [f for f in parts if f.GetAttributes() & pcbnew.FP_SMD]  # PCBWay's centroid lists SMT parts only
    assert all(f.GetLayer() == pcbnew.F_Cu for f in parts), 'bottom-side part: LAYERS and the centroid assume top only'
    write_gerbers(left, bottom)
    write_bom(parts)
    write_centroid(smt, left, bottom)


if __name__ == '__main__':
    main()
