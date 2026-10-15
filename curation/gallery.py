"""Render every DFT-ready structure as a small ball-and-stick PNG and build a scrollable HTML gallery."""
import glob, os, io, json, base64, re, collections, csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hgeom import bonds
from lewis_check import rd

COL = dict(H="#e8e8e8", C="#5d6670", N="#3a5bd9", O="#d6332a", S="#d9b310", Zn="#8a96a3", B="#f0a070",
           F="#6cc04a", Cl="#30b040", Br="#a0522d", I="#7a3fa0", Si="#c8a882", P="#f08000", Se="#e09030")
RAD = dict(H=0.14, C=0.26, N=0.26, O=0.26, S=0.33, Zn=0.42, B=0.26, F=0.24, Cl=0.32, Br=0.35, I=0.38, Si=0.33, P=0.32, Se=0.35)
AUD = {r["refcode"]: r for r in json.load(open("final/final_audit.json"))}
MAN = {r["refcode"]: r for r in csv.DictReader(open("final/dft_ready_manifest.csv"))}


def render(path, px=230):
    el, X = rd(path)
    nb, D = bonds(el, X)
    z = el.index("Zn")
    Y = X - X.mean(0)
    _, _, Vt = np.linalg.svd(Y, full_matrices=False)
    P = Y @ Vt.T                      # x,y = two largest spreads, z = depth toward viewer
    P -= P[z]
    fig = plt.figure(figsize=(px / 100, px / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off(); ax.set_aspect("equal")
    span = np.abs(P[:, :2]).max() + 0.6
    ax.set_xlim(-span, span); ax.set_ylim(-span, span)
    zmin, zmax = P[:, 2].min(), P[:, 2].max()
    shade = lambda d: 0.55 + 0.45 * (d - zmin) / (zmax - zmin + 1e-9)
    items = []
    for i in range(len(el)):
        for j in nb[i]:
            if j <= i:
                continue
            dz = (P[i, 2] + P[j, 2]) / 2
            items.append((dz - 0.01, "b", i, j))
        items.append((P[i, 2], "a", i, None))
    for dz, kind, i, j in sorted(items):
        a = shade(dz)
        if kind == "b":
            zn = z in (i, j)
            ax.plot([P[i, 0], P[j, 0]], [P[i, 1], P[j, 1]], color="#2b3138" if not zn else "#6a7480",
                    lw=1.1 if "H" in (el[i], el[j]) else 1.8, ls=(0, (2, 1.5)) if zn else "-", alpha=a, solid_capstyle="round", zorder=dz)
        else:
            e = el[i]
            ax.add_patch(plt.Circle((P[i, 0], P[i, 1]), RAD.get(e, 0.3), facecolor=COL.get(e, "#ff66cc"),
                                    edgecolor="#2b3138", lw=0.5, alpha=min(1, a + 0.15), zorder=dz + 0.005))
    buf = io.BytesIO(); fig.savefig(buf, format="png", transparent=True); plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


cards = []
for p in sorted(glob.glob("final/dft_ready_xyz/*.xyz")):
    ref = os.path.basename(p)[:-4]
    a = AUD[ref]; m = MAN.get(ref, {})
    src = m.get("H_source", "")
    tag = "deposited H" if src == "deposited" else "H completed" if src.startswith("completed") else "cleaned" if src.startswith("cleaned") else "edited" if src.startswith("edited") else ""
    flags = [f for f in a["fails"] if not f.startswith("contact H")]
    cards.append(dict(ref=ref, donors=a["donors"], cn=a["CN"], formula=a["formula"], n=a["natoms"], q=a["charge"], mult=a["mult"],
                      zl=a["zn_L"], tag=tag, flag="; ".join(flags), img=render(p)))
cards.sort(key=lambda c: (c["donors"], c["ref"]))
json.dump([{k: v for k, v in c.items() if k != "img"} for c in cards], open("final/gallery_index.json", "w"), indent=0)

groups = collections.OrderedDict()
for c in sorted(cards, key=lambda c: (-sum(1 for x in cards if x["donors"] == c["donors"]), c["donors"], c["ref"])):
    groups.setdefault(c["donors"], []).append(c)


def fmt(f):
    return re.sub(r"([A-Za-z])(\d+)", lambda mm: mm.group(1) + ("" if mm.group(2) == "1" else f"<sub>{mm.group(2)}</sub>"), f).replace(" ", "")


html = ["""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zn DFT Set Gallery</title><style>
:root{--bg:#f4f6f8;--card:#fff;--ink:#1c232a;--mute:#5f6b77;--line:#dfe4e9;--accent:#2f6f8f;--warn:#a35f00}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#13171b;--card:#1c2228;--ink:#e4e9ee;--mute:#98a3ae;--line:#2c343c;--accent:#7ab8d6;--warn:#e3a43c;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#13171b;--card:#1c2228;--ink:#e4e9ee;--mute:#98a3ae;--line:#2c343c;--accent:#7ab8d6;--warn:#e3a43c;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:13px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{max-width:1500px;margin:0 auto;padding:18px 16px 40px}h1{font-size:20px;margin:0 0 4px}.sub{color:var(--mute);margin:0 0 12px;max-width:95ch}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);padding:8px 0;display:flex;flex-wrap:wrap;gap:6px;align-items:center;border-bottom:1px solid var(--line)}
.bar button{font:inherit;font-size:12px;padding:3px 9px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink);cursor:pointer}
.bar button.on{border-color:var(--accent);color:var(--accent);font-weight:600}
.bar input{font:inherit;padding:4px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--ink);min-width:200px}
h2{font-size:15px;margin:22px 0 8px}h2 span{color:var(--mute);font-weight:400}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px}
.c{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 8px 8px;min-width:0}
.c img{width:100%;height:auto;display:block;background:#fbfcfd;border-radius:5px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .c img{background:#eef1f4}}
:root[data-theme="dark"] .c img{background:#eef1f4}
.r{font-weight:600;font-family:ui-monospace,Menlo,monospace;font-size:13px;margin-top:4px;display:flex;justify-content:space-between;gap:6px}
.r span{font-weight:400;color:var(--mute);font-family:inherit;font-size:11.5px}
.f{font-size:11.5px;overflow-wrap:anywhere}.m{color:var(--mute);font-size:11px;overflow-wrap:anywhere}.w{color:var(--warn);font-size:11px}
.leg{display:flex;flex-wrap:wrap;gap:12px;color:var(--mute);font-size:12px;margin-bottom:6px}.leg i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px;vertical-align:-1px;border:1px solid #0003}
</style></head><body><main>
<h1>Zn DFT set: all 347 structures</h1>
<p class="sub">Start geometries for ORCA, one card per complex, grouped by Zn donor set. Each image is projected along the molecule's two longest axes, with nearer atoms drawn darker; Zn–L bonds are dashed. Cards show charge, multiplicity, atom count and crystal Zn–L distances (Å). Amber notes are start-geometry bond lengths outside typical ranges, which the optimization will relax.</p>
<div class="leg"><span><i style="background:#8a96a3"></i>Zn</span><span><i style="background:#d9b310"></i>S</span><span><i style="background:#3a5bd9"></i>N</span><span><i style="background:#d6332a"></i>O</span><span><i style="background:#5d6670"></i>C</span><span><i style="background:#e8e8e8"></i>H</span><span><i style="background:#f0a070"></i>B</span><span><i style="background:#c8a882"></i>Si</span><span><i style="background:#6cc04a"></i>F</span></div>
<div class="bar"><input id="q" type="search" placeholder="Search refcode or formula" aria-label="Search"><button data-g="all" class="on">All</button>"""]
for g, cs in groups.items():
    html.append(f'<button data-g="{g}">{g} {len(cs)}</button>')
html.append("</div>")
for g, cs in groups.items():
    html.append(f'<section data-sec="{g}"><h2>{g} <span>{len(cs)} complexes</span></h2><div class="grid">')
    for c in cs:
        qs = f"{c['q']:+d}" if c["q"] else "0"
        html.append(f'<div class="c" data-k="{c["ref"]} {c["formula"]}"><img loading="lazy" alt="{c["ref"]}" src="data:image/png;base64,{c["img"]}">'
                    f'<div class="r">{c["ref"]}<span>q {qs} · m {c["mult"]} · {c["n"]} at.</span></div>'
                    f'<div class="f">{fmt(c["formula"])}</div><div class="m">{c["zl"]}{" · " + c["tag"] if c["tag"] else ""}</div>'
                    + (f'<div class="w">{c["flag"]}</div>' if c["flag"] else "") + "</div>")
    html.append("</div></section>")
html.append("""</main><script>
const secs=[...document.querySelectorAll('section')],cards=[...document.querySelectorAll('.c')];let g='all',q='';
function up(){secs.forEach(s=>{const show=g==='all'||s.dataset.sec===g;let n=0;s.querySelectorAll('.c').forEach(c=>{const v=show&&(!q||c.dataset.k.toLowerCase().includes(q));c.hidden=!v;if(v)n++;});s.hidden=!n;});}
document.querySelector('.bar').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;g=b.dataset.g;document.querySelectorAll('.bar button').forEach(x=>x.classList.toggle('on',x===b));up();});
document.getElementById('q').addEventListener('input',e=>{q=e.target.value.trim().toLowerCase();up();});
</script></body></html>""")
open("final/zn_dft_set_gallery.html", "w").write("\n".join(html))
print(len(cards), os.path.getsize("final/zn_dft_set_gallery.html") // 1024, "KB")
