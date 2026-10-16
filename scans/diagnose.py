#!/usr/bin/env python3
"""Explain the not_converged points found by validate.py.

Usage (inside the project folder, after validate.py):
    python3 <repo>/scans/diagnose.py . [tag]

For every not_converged point it reads that step of scan.out and reports what happened:
cycles used, whether ORCA declared the step converged, hit the cycle limit, or lost SCF
convergence, and whether the geometry and energy were printed. Standard library only.
"""
import sys, os, re, csv, collections

dft = os.path.abspath(sys.argv[1])
tag = sys.argv[2] if len(sys.argv) > 2 else "pilot"
rows = list(csv.DictReader(open(os.path.join(dft, "scans", "validation_%s.csv" % tag))))
bad = [r for r in rows if r["status"] == "not_converged"]
cache, cat, per_ref, examples = {}, collections.Counter(), collections.Counter(), []
for r in bad:
    d = os.path.join(dft, "scans", r["ref"], "%s_%s" % (r["coord"], r["branch"]))
    if d not in cache:
        t = open(os.path.join(d, "scan.out"), errors="ignore").read()
        cache[d] = (t, re.split(r"RELAXED SURFACE SCAN STEP\s+\d+", t))
    t, parts = cache[d]
    k = int(r["step"]) + 1
    if k >= len(parts):
        why = "step never started (job ended after %d steps)" % (len(parts) - 1)
    else:
        p = parts[k]
        cyc = p.count("GEOMETRY OPTIMIZATION CYCLE")
        flags = []
        if "THE OPTIMIZATION HAS CONVERGED" in p:
            flags.append("ORCA says converged")
        if re.search(r"did not converge|maximum number of (optimization|geometry) cycles", p, re.I):
            flags.append("hit optimisation cycle limit")
        if re.search(r"SCF NOT CONVERGED|SCF not fully converged", p, re.I):
            flags.append("SCF not converged")
        if "FINAL SINGLE POINT ENERGY" not in p:
            flags.append("energy not printed")
        if "CARTESIAN COORDINATES (ANGSTROEM)" not in p:
            flags.append("geometry not printed")
        why = "%d cycles; %s" % (cyc, ", ".join(flags) or "unclassified")
    key = re.sub(r"^\d+ cycles; ", "", why)
    cat[key] += 1
    per_ref[r["ref"]] += 1
    if len(examples) < 12:
        examples.append("  %-7s %-34s %-3s step %2s  %s" % (r["ref"], r["coord"], r["branch"], r["step"], why))
print("not_converged points:", len(bad))
print("\nwhat happened:")
for k, v in cat.most_common():
    print("  %4d  %s" % (v, k))
print("\nby complex:", dict(per_ref))
print("\nexamples:")
print("\n".join(examples))
term = collections.Counter()
for d, (t, parts) in cache.items():
    tail = [l.strip() for l in t.strip().split("\n")[-40:] if l.strip()]
    msg = next((l for l in reversed(tail) if re.search(r"error|abort|TERMINATED|CANCELLED|TIME LIMIT", l, re.I)), tail[-1] if tail else "empty")
    term[msg[:90]] += 1
print("\nhow those jobs ended:")
for k, v in term.most_common(8):
    print("  %4d  %s" % (v, k))
