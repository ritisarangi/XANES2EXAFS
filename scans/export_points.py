#!/usr/bin/env python3
"""Collect every passing scan geometry into small per-complex files for transfer.

Usage (inside the project folder, after validate.py):
    python3 <repo>/scans/export_points.py . lists/scan_full.txt [tag]
Writes scan_results/<REF>.xyz (one frame per passing point; the comment line holds
ref, coordinate, branch, step, offset, value, E_rel in kJ/mol and the absolute energy),
copies the validation CSV and coords.json files, and packs them into scan_results.tar.gz.
Standard library only.
"""
import sys, os, csv, json, tarfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate as V  # noqa: E402

dft = os.path.abspath(sys.argv[1])
lst = sys.argv[2]
tag = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(os.path.basename(lst))[0]
rows = list(csv.DictReader(open(os.path.join(dft, "scans", "validation_%s.csv" % tag))))
outd = os.path.join(dft, "scan_results")
os.makedirs(outd, exist_ok=True)
by = {}
for r in rows:
    if r["status"] == "pass":
        by.setdefault(r["ref"], []).append(r)
n_pts = 0
for ref, rs in sorted(by.items()):
    C = json.load(open(os.path.join(dft, "scans", ref, "coords.json")))
    dirs = {(c["name"], c["branch"]): c["dir"] for c in C["coords"]}
    nat = int(open(os.path.join(dft, "stage2_b3lyp", ref, ref + ".xyz")).readline())
    cache, frames = {}, []
    for r in rs:
        d = dirs[(r["coord"], r["branch"])]
        if d not in cache:
            cache[d] = V.parse_steps(open(os.path.join(dft, d, "scan.out"), errors="ignore").read(), nat)
        conv, E, A = cache[d][int(r["step"])]
        frames.append("%d\n%s %s %s step=%s offset=%s value=%s E_rel_kJ=%s E_h=%.8f\n%s" % (
            nat, ref, r["coord"], r["branch"], r["step"], r["offset"], r["value"], r["E_rel_kJ"], E,
            "\n".join("%-2s %12.6f %12.6f %12.6f" % a for a in A)))
    open(os.path.join(outd, ref + ".xyz"), "w").write("\n".join(frames) + "\n")
    n_pts += len(frames)
tb = os.path.join(dft, "scan_results.tar.gz")
with tarfile.open(tb, "w:gz") as tar:
    tar.add(outd, "scan_results")
    tar.add(os.path.join(dft, "scans", "validation_%s.csv" % tag), "scan_results/validation_%s.csv" % tag)
    for ref in by:
        tar.add(os.path.join(dft, "scans", ref, "coords.json"), "scan_results/coords/%s.json" % ref)
print("passing points exported: %d from %d complexes" % (n_pts, len(by)))
print("wrote %s (%.1f MB)" % (os.path.relpath(tb, dft), os.path.getsize(tb) / 1e6))
