#!/usr/bin/env python3
"""Build the JLCPCB order files for the BlueBuzzah v3 board.

    python3 make_jlcpcb.py

Needs KiCad 10 (kicad-cli + its bundled Python). Quit KiCad first: it rewrites
the project file when it closes. On first run this sets up KiKit in .venv-kikit/
(git-ignored), using KiCad's Python so KiKit can load boards.

Steps:
  1. DRC the board (with schematic parity); stop on any error or unconnected item.
  2. Frame one board with KiKit into panel/, so an order of 2 assembled panels is 2
     boards. JLCPCB Standard assembly needs a panel of at least 70 x 70 mm, and V-cut
     can't work: the motor connectors overhang the top edge and USB-C/SW1 the bottom
     edge, so the frame stands clear of them and tabs only sit on the left/right edges.
  3. DRC the panel; stop on any error.
  4. Write the order files next to this script: gerbers + drill (zipped), BOM and CPL.
     Designators get the board number (R1_1) so they stay unique if the grid grows.
"""
import csv, os, re, shutil, subprocess, sys, json, zipfile, collections, tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
KICAD_DIR = os.path.join(ROOT, 'kicad')
BOARD = os.path.join(KICAD_DIR, 'BlueBuzzah_v3.kicad_pcb')
PANEL_DIR = os.path.join(ROOT, 'panel')
OUT = ROOT
VENV = os.path.join(ROOT, '.venv-kikit')
KIKIT_VERSION = '1.8.1'
KICAD_PYTHON = os.environ.get(
    'KICAD_PYTHON', '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3')
KICAD_CLI = shutil.which('kicad-cli') or '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'

ROWS, COLS, HSPACE, VSPACE, RAIL, RAIL_SPACE = 1, 1, 2.0, 4.5, 12.0, 3.0
KIKIT_ARGS = [
    '-l', f'grid; rows: {ROWS}; cols: {COLS}; hspace: {HSPACE}mm; vspace: {VSPACE}mm',
    '-t', 'fixed; hwidth: 5mm; hcount: 2; vcount: 0',
    '-c', 'mousebites; drill: 0.5mm; spacing: 0.8mm; offset: 0mm',
    '-r', f'frame; width: {RAIL}mm; space: {RAIL_SPACE}mm; cuts: none',
    '-o', '3hole; hoffset: 3.85mm; voffset: 3.85mm; size: 2mm',
    '-f', '3fid; hoffset: 3.85mm; voffset: 12mm; coppersize: 1mm; opening: 2mm',
    '-z', 'millradius: 1mm',
]
GERBER_LAYERS = 'F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts'

# JLCPCB's parts library has its own zero angle for many packages, and centers each part
# on its pads rather than on KiCad's footprint origin. The CPL uses the pad center, and
# adds these degrees to KiCad's rotation, by footprint. Check any new package in the preview.
CPL_ROTATIONS = {
    'SOT-23': 180,
    'SOT-23-5': 270,
    'SOT-23-6': 270,
    'TSOT-23-5': 270,
    'TSSOP-24_4.4x7.8mm_P0.65mm': 270,
    'VSSOP-10_3x3mm_P0.5mm': 270,
    'SW_K3_1260D_L1_SPDT_Angled': 90,
}

# Parts from the original (XIAO) design carry no LCSC field; these are the numbers
# from that board's JLCPCB BOM. New parts have an LCSC field in the schematic.
LCSC_BY_VALUE_FOOTPRINT = {
    ('Conn_01x02_Socket', 'JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal'): 'C5175239',
    ('1uF', 'C_0402_1005Metric'): 'C52923',
    ('100nF', 'C_0402_1005Metric'): 'C1525',
    ('22uF', 'C_1206_3216Metric'): 'C12891',
    ('4.7k', 'R_0402_1005Metric'): 'C25900',
    ('10k', 'R_0402_1005Metric'): 'C25744',
    ('100k', 'R_0402_1005Metric'): 'C25741',
    ('5.1k', 'R_0402_1005Metric'): 'C25905',
    ('DRV2605LDGS', 'VSSOP-10_3x3mm_P0.5mm'): 'C527464',
    ('TCA9548APWR', 'TSSOP-24_4.4x7.8mm_P0.65mm'): 'C130026',
    ('LSM6DS3', 'LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y'): 'C967633',
    ('WS2812B RGB LED', 'LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm'): 'C2874885',  # WS2812B-V5/W; the original C2761795 is out of stock, and C114586 isn't offered for assembly
    ('PESD5V0L1UL', 'D_SOD-882'): 'C3001948',
    ('SW_SPDT', 'SW_K3_1260D_L1_SPDT_Angled'): 'C92657',
}


def run(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'failed: {" ".join(cmd)}\n{r.stdout}{r.stderr}')
    return r.stdout


def ensure_venv():
    """Re-run this script inside .venv-kikit (KiCad's Python + KiKit)."""
    py = os.path.join(VENV, 'bin', 'python')
    if os.path.realpath(sys.prefix) == os.path.realpath(VENV):
        return
    if not os.path.exists(py):
        if not os.path.exists(KICAD_PYTHON):
            sys.exit(f"KiCad's Python not found at {KICAD_PYTHON}; set KICAD_PYTHON")
        print('Setting up KiKit (first run)...', flush=True)
        run(KICAD_PYTHON, '-m', 'venv', '--system-site-packages', VENV)
        run(py, '-m', 'pip', 'install', '-q', f'kikit=={KIKIT_VERSION}')
    os.execv(py, [py, os.path.abspath(__file__)] + sys.argv[1:])


def drc(board, parity):
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, 'drc.json')
        args = [KICAD_CLI, 'pcb', 'drc', '--severity-all', '--format', 'json', '-o', out]
        if parity: args.append('--schematic-parity')
        run(*args, board)
        d = json.load(open(out))
    errors = [v for v in d['violations'] if v['severity'] == 'error']
    if errors or d['unconnected_items']:
        for v in errors[:10]:
            print('  ', v['type'], [i['description'] for i in v['items']])
        sys.exit(f'DRC failed on {os.path.basename(board)}: {len(errors)} errors, '
                 f'{len(d["unconnected_items"])} unconnected')
    print(f'DRC ok: {os.path.basename(board)}')


def gerbers(board, zip_path):
    with tempfile.TemporaryDirectory() as tmp:
        g = os.path.join(tmp, 'manufacturing')
        os.makedirs(g)
        run(KICAD_CLI, 'pcb', 'export', 'gerbers', '-o', g, '--layers', GERBER_LAYERS,
            '--subtract-soldermask', '--check-zones', board)
        run(KICAD_CLI, 'pcb', 'export', 'drill', '-o', g + '/', '--format', 'excellon',
            '--drill-origin', 'absolute', '--excellon-units', 'mm', board)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for name in sorted(os.listdir(g)):
                if not name.endswith('.gbrjob'):
                    z.write(os.path.join(g, name), f'manufacturing/{name}')
    print(f'wrote {os.path.relpath(zip_path, ROOT)}')


def bom_cpl(panel_board, board_w, board_h):
    import pcbnew
    MM = pcbnew.ToMM
    b = pcbnew.LoadBoard(panel_board)
    bb = b.GetBoardEdgesBoundingBox()
    x0 = MM(bb.GetLeft()) + RAIL + RAIL_SPACE           # left edge of the first board column
    y0 = MM(bb.GetTop()) + RAIL + RAIL_SPACE

    def board_no(x, y):
        col = min(COLS - 1, int((x - x0) // (board_w + HSPACE)))
        row = min(ROWS - 1, int((y - y0) // (board_h + VSPACE)))
        return row * COLS + col + 1

    rows, cpl, missing = collections.OrderedDict(), [], set()
    for f in b.Footprints():
        ref = f.GetReference()
        # skip test pads, mounting holes, KiKit fiducials/tooling, nameless pads
        if not re.fullmatch(r'[A-Z]+\d+', ref) or ref.startswith(('H', 'TP')) or f.IsExcludedFromBOM():
            continue
        fp = str(f.GetFPID().GetLibItemName())
        lcsc = (f.GetFieldText('LCSC') if f.HasField('LCSC') else '') or LCSC_BY_VALUE_FOOTPRINT.get((f.GetValue(), fp))
        if not lcsc:
            missing.add(f'{ref} ({f.GetValue()}, {fp})'); continue
        x, y = MM(f.GetPosition().x), MM(f.GetPosition().y)
        des = f'{ref}_{board_no(x, y)}'
        rows.setdefault((f.GetValue(), fp, lcsc), []).append(des)
        pads = [p.GetBoundingBox() for p in f.Pads()]
        mid_x = MM(min(p.GetLeft() for p in pads) + max(p.GetRight() for p in pads)) / 2
        mid_y = MM(min(p.GetTop() for p in pads) + max(p.GetBottom() for p in pads)) / 2
        rot = (f.GetOrientationDegrees() + CPL_ROTATIONS.get(fp, 0)) % 360
        cpl.append((des, mid_x, -mid_y, rot, 'top' if f.GetLayer() == pcbnew.F_Cu else 'bottom'))
    if missing:
        sys.exit('no LCSC number for: ' + ', '.join(sorted(missing)) +
                 '\nadd an LCSC field to the symbol, or extend LCSC_BY_VALUE_FOOTPRINT')
    dups = [d for d, n in collections.Counter(c[0] for c in cpl).items() if n > 1]
    if dups:
        sys.exit(f'duplicate designators: {dups}')

    def key(des):
        ref, n = des.split('_')
        return re.sub(r'\d', '', ref), int(re.sub(r'\D', '', ref)), int(n)
    fmt = lambda v: f'{v:.4f}'.rstrip('0').rstrip('.')
    with open(os.path.join(OUT, 'BOM_JCLPCB_BlueBuzzah_v3.csv'), 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['Comment', 'Designator', 'Footprint', 'JLCPCB Part #'])
        for (val, fp, lcsc), refs in sorted(rows.items(), key=lambda kv: key(sorted(kv[1], key=key)[0])):
            w.writerow([val, ','.join(sorted(refs, key=key)), fp, lcsc])
    with open(os.path.join(OUT, 'CPL_JLCPCB_BlueBuzzah_v3-all-pos.csv'), 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['Designator', 'Mid X', 'Mid Y', 'Rotation', 'Layer'])
        for des, x, y, rot, side in sorted(cpl, key=lambda c: key(c[0])):
            w.writerow([des, fmt(x), fmt(y), f'{rot:g}', side])
    per_board = collections.Counter(c[0].split('_')[1] for c in cpl)
    print(f'wrote BOM ({len(rows)} lines) and CPL ({len(cpl)} placements, per board {dict(sorted(per_board.items()))})')


def main():
    ensure_venv()
    if any(n.startswith('~') and n.endswith('.lck') for n in os.listdir(KICAD_DIR)):
        sys.exit('KiCad seems to have this project open (lock files present); quit it first')
    import pcbnew
    src = pcbnew.LoadBoard(BOARD)
    sb = src.GetBoardEdgesBoundingBox()
    board_w, board_h = pcbnew.ToMM(sb.GetWidth()), pcbnew.ToMM(sb.GetHeight())

    drc(BOARD, parity=True)
    os.makedirs(PANEL_DIR, exist_ok=True)
    panel = os.path.join(PANEL_DIR, 'panel.kicad_pcb')
    run(os.path.join(VENV, 'bin', 'kikit'), 'panelize', *KIKIT_ARGS, BOARD, panel)
    for n in os.listdir(PANEL_DIR):                      # KiKit leaves a lock and local settings behind
        if n.endswith(('.lck', '.kicad_prl')):
            os.remove(os.path.join(PANEL_DIR, n))
    pb = pcbnew.LoadBoard(panel)
    pcbnew.ZONE_FILLER(pb).Fill(pb.Zones())
    pb.Save(panel)
    pbb = pb.GetBoardEdgesBoundingBox()
    print(f'panel {pcbnew.ToMM(pbb.GetWidth()):.1f} x {pcbnew.ToMM(pbb.GetHeight()):.1f} mm')
    drc(panel, parity=False)

    os.makedirs(OUT, exist_ok=True)
    gerbers(panel, os.path.join(OUT, 'jlc_pcb_gerbers.zip'))
    bom_cpl(panel, board_w, board_h)


if __name__ == '__main__':
    main()
