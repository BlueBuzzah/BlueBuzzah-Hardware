#!/usr/bin/env python3
"""Copy renders from images/v3/ into the two websites as WebP. Run render_all.py first. See README.md.

    python3 scripts/publish_images.py upper-shell pair hero   # only images whose name contains one of these words
    python3 scripts/publish_images.py                         # every site image that has a render

It only replaces images the sites already have; it commits nothing. Renders differ slightly from run to run, so
name the images that really changed, or unchanged ones show up as modified too.
"""
import glob, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = os.environ.get("SITES", os.path.dirname(REPO))  # the folder holding the BlueBuzzah.com and BuzzahBuddy.com checkouts
RENDERS = {os.path.basename(p)[:-4]: p for p in glob.glob(os.path.join(REPO, "images", "v3", "*", "*.png"))}
DOCS = os.path.join(SITES, "BlueBuzzah.com", "src", "public", "docs", "img")
HEROES = {  # render name -> site file without extension; published at 1600 and 800 px wide
    "bluebuzzah-hero": os.path.join(SITES, "BlueBuzzah.com", "src", "public", "assets", "bluebuzzah-hero"),
    "buzzahbuddy-hero": os.path.join(SITES, "BuzzahBuddy.com", "src", "public", "assets", "hero-pair"),
}

def cwebp(src, dst, quality, width=None):
    size = ["-resize", str(width), "0"] if width else []
    subprocess.run(["cwebp", "-quiet", "-q", str(quality), *size, src, "-o", dst], check=True)

def width(png):
    out = subprocess.run(["sips", "-g", "pixelWidth", png], check=True, capture_output=True, text=True).stdout
    return int(out.split()[-1])

words = sys.argv[1:]
wanted = lambda name: not words or any(w in name for w in words)
done = 0
for page in sorted(glob.glob(os.path.join(DOCS, "*.webp"))):  # docs images: up to 1600 px wide plus a 640 px thumb
    name = os.path.basename(page)[:-5]
    if name.endswith("-thumb") or not wanted(name):
        continue
    if name not in RENDERS:
        print(f"no render for {name}")
        continue
    src = RENDERS[name]
    cwebp(src, page, 85, 1600 if width(src) > 1600 else None)  # never upscaled
    cwebp(src, page[:-5] + "-thumb.webp", 82, 640)
    print(f"docs  {name}"); done += 1
for name, dst in HEROES.items():
    if wanted(name) and name in RENDERS and os.path.exists(dst + ".webp"):
        cwebp(RENDERS[name], dst + ".webp", 85, 1600)
        cwebp(RENDERS[name], dst + "-800.webp", 85, 800)
        print(f"hero  {name} -> {os.path.relpath(dst, SITES)}"); done += 1
print(f"{done} images updated under {SITES}")
