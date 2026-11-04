#!/usr/bin/env python3
"""Rebuild the v3 renders (images/v3/) and models (models/) from the CAD files. See README.md.

    python3 scripts/render_all.py                 # everything, written into this checkout
    python3 scripts/render_all.py battery pin     # only configs whose name contains one of these words
    OUT=/tmp/check BB_SAMPLES=16 python3 scripts/render_all.py   # quick preview somewhere else
"""
import glob, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
env = dict(os.environ)
env.setdefault("HW", REPO)
env.setdefault("OUT", REPO)
env.setdefault("WORK", tempfile.mkdtemp(prefix="bb-render-"))
env["SCRIPTS"] = HERE
FC = env.get("FREECAD_BIN", "/Applications/FreeCAD.app/Contents/Resources/bin")
BLENDER = env.get("BLENDER", "blender")
WORK = env["WORK"]

def run(cmd, quiet=False, **extra):
    """Run a tool with the shared environment (plus any extra variables); quiet hides its output."""
    subprocess.run(cmd, check=True, env=dict(env, **extra), stdout=subprocess.DEVNULL if quiet else None)

def fill(s):
    return s.format(scripts=HERE, work=WORK, out=env["OUT"])

# 1. Meshes from the STEP files (skipped when WORK already holds them from an earlier run)
XIAO = env.get("XIAO_STEP", os.path.join(env["HW"], "models", "XIAO-ESP32S3-v2.step"))
HAVE_XIAO = os.path.exists(XIAO)
if not HAVE_XIAO:
    print(f"note: {XIAO} not found (set XIAO_STEP); skipping the BlueBuzzah exploded view")
if not os.path.isdir(os.path.join(WORK, "tactor")):
    for script in ("export_tactor", "export_case") + (("export_xiao",) if HAVE_XIAO else ()):
        run([f"{FC}/freecadcmd", "-c", f"exec(open({os.path.join(HERE, 'freecad', script + '.py')!r}).read())"])
    run([f"{FC}/freecad", os.path.join(HERE, "freecad", "pcb2glb.py")], QT_QPA_PLATFORM="offscreen")
    for step, name in ((("PCB", "v3", "kicad", "BlueBuzzah_v3.step"), "bluebuzzah-v3-pcb"),  # WROOM board + its USB-C
                       (("models", "USB_C_Receptacle_HRO_TYPE-C-31-M-12.step"), "usb-c")):
        run([f"{FC}/freecad", os.path.join(HERE, "freecad", "pcb2glb.py")], QT_QPA_PLATFORM="offscreen",
            BOARD_STEP=os.path.join(env["HW"], *step), GLB_NAME=name)
    bbx = os.path.join(WORK, "bbx")  # parts for the BlueBuzzah exploded view: XIAO materials + case parts
    os.makedirs(bbx, exist_ok=True)
    for d in ("xiao", "case"):
        for f in glob.glob(os.path.join(WORK, d, "*.stl")):
            shutil.copy(f, bbx)

# 2. Each config: render, label, resize for the web, export the .glb model
words = sys.argv[1:]
for path in sorted(glob.glob(os.path.join(HERE, "configs", "*", "*.json"))):
    name = os.path.basename(path)[:-5]
    if words and not any(w in name for w in words):
        continue
    cfg = json.load(open(path))
    if not HAVE_XIAO and cfg.get("parts") in ("{work}/xiao", "{work}/bbx"):  # these need the XIAO meshes
        continue
    print(f"== {name}", flush=True)
    run([BLENDER, "-b", "-P", os.path.join(HERE, "brender.py"), "--", path], quiet=True)
    out = fill(cfg["out"])
    images = [out]
    if "labels" in cfg:  # the unlabeled render is only an input for the labeled one
        labeled = fill(cfg["labels"]["out"])
        bounds = os.path.join(WORK, "bounds", os.path.basename(out) + ".json")
        run(["sh", os.path.join(HERE, "label.sh"), bounds, out, fill(cfg["labels"]["spec"]), labeled])
        images.append(labeled)
    for img in images:  # web delivery: about 2x the size the old wiki displayed them at
        subprocess.run(["sips", "--resampleWidth", str(cfg["web_width"]), img], check=True, stdout=subprocess.DEVNULL)
    if "model" in cfg:
        run([BLENDER, "-b", "-P", os.path.join(HERE, "brender.py"), "--", path], quiet=True, BB_MODE="model")
print(f"done; intermediate files in {WORK}")
