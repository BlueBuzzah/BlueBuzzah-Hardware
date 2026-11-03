# Writes labels.html: numbered callouts over an exploded render, styled with the BlueBuzzah design system's dark
# theme (brand-blue circle, on-brand number in Lexend, ink name in Atkinson Hyperlegible Next).
# usage: labels.py <work dir> <base.png> <fonts dir> <bounds.json from brender> <labels.json: [[n, name, group], ...]>
# Each callout sits a fixed GAP right of its part's silhouette, at the part's measured height.
import json, sys
S, IMG, FONTS, DATA, SPEC = sys.argv[1:6]
d = json.load(open(DATA)); P = d["parts"]
L = json.load(open(SPEC))
GAP = 100
tags = []
for n, name, part in L:
    xr, cy = P[part][4:6]
    tags.append(f'<div class="c" style="left:{(xr + GAP)/2}px;top:{cy/2}px;transform:translate(0,-50%)"><span class="n">{n}</span><span class="t">{name}</span></div>')
w, h = d["w"] / 2, d["h"] / 2
open(f"{S}/labels.html", "w").write(f"""<!doctype html><meta charset="utf-8">
<style>
@font-face {{ font-family: "Lexend"; src: url("file://{FONTS}/lexend-latin-wght-normal.woff2") format("woff2"); font-weight: 100 900; }}
@font-face {{ font-family: "Atkinson Hyperlegible Next"; src: url("file://{FONTS}/atkinson-hyperlegible-next-latin-wght-normal.woff2") format("woff2"); font-weight: 200 800; }}
:root {{ --brand: #4fb0ff; --on-brand: #03132f; --ink: #eef3ff; }}  /* design system tokens, dark theme */
html, body {{ margin: 0; background: transparent; overflow: hidden; }}
.wrap {{ position: absolute; left: 0; top: 0; width: {w}px; height: {h}px; }}
.wrap img {{ width: 100%; height: 100%; display: block; }}
.c {{ position: absolute; display: flex; align-items: center; gap: 26px; white-space: nowrap; }}
.n {{ width: 108px; height: 108px; border-radius: 50%; background: var(--brand); color: var(--on-brand);
     display: grid; place-items: center; font: 600 54px/1 Lexend, sans-serif; }}
.t {{ color: var(--ink); font: 700 64px/1.2 "Atkinson Hyperlegible Next", sans-serif; }}
</style>
<div class="wrap"><img src="file://{IMG}">{''.join(tags)}</div>
<script>
// grow the canvas to fit labels that run past the render: shift content, report the size in <title>
document.fonts.ready.then(() => {{
  const M = 24, r = [...document.querySelectorAll(".wrap img, .c")].map(e => e.getBoundingClientRect());
  const x0 = Math.min(...r.map(b => b.left)) - M, y0 = Math.min(...r.map(b => b.top)) - M;
  const x1 = Math.max(...r.map(b => b.right)) + M, y1 = Math.max(...r.map(b => b.bottom)) + M;
  const ox = Math.max(0, -x0), oy = Math.max(0, -y0);
  const wrap = document.querySelector(".wrap");
  wrap.style.left = ox + "px"; wrap.style.top = oy + "px";
  document.title = Math.ceil(Math.max(x1, {w}) + ox) + "x" + Math.ceil(Math.max(y1, {h}) + oy);
}});
</script>""")
