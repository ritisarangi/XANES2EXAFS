#!/usr/bin/env python3
"""Summarize both stages: python3 scripts/status.py [lists/all.txt]  -> status.csv + printed summary.

Per complex: stage-1 state and cycles; stage-2 state, cycles, final energy, lowest
frequency and number of imaginary modes (frequencies < 0 cm-1 in ORCA output).
States: pending (no .out), running, converged, failed.
"""
import os, re, sys, csv, collections

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lst = sys.argv[1] if len(sys.argv) > 1 else "lists/all.txt"
refs = [l.strip() for l in open(os.path.join(root, lst)) if l.strip()]


def state(path, need):
    if not os.path.exists(path):
        return "pending", 0, ""
    t = open(path, errors="ignore").read()
    cyc = t.count("GEOMETRY OPTIMIZATION CYCLE")
    E = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", t)
    if "ORCA TERMINATED NORMALLY" in t:
        return ("converged" if all(k in t for k in need) else "failed"), cyc, (E[-1] if E else "")
    if "ERROR" in t or "aborting" in t.lower():
        return "failed", cyc, ""
    return "running", cyc, (E[-1] if E else "")


rows = []
for r in refs:
    s1, c1, e1 = state(f"{root}/stage1_r2scan/{r}/{r}.out", ["OPTIMIZATION RUN DONE"])
    s2, c2, e2 = state(f"{root}/stage2_b3lyp/{r}/{r}.out", ["OPTIMIZATION RUN DONE", "VIBRATIONAL FREQUENCIES"])
    low, nimag = "", ""
    if s2 == "converged":
        t = open(f"{root}/stage2_b3lyp/{r}/{r}.out", errors="ignore").read()
        blk = t.split("VIBRATIONAL FREQUENCIES")[-1].split("NORMAL MODES")[0]
        fr = [float(x) for x in re.findall(r"^\s*\d+:\s+(-?\d+\.\d+) cm\*\*-1", blk, re.M)]
        nz = [f for f in fr if abs(f) > 0.01]
        low = f"{min(nz):.1f}" if nz else ""; nimag = sum(f < 0 for f in nz)
    rows.append(dict(refcode=r, stage1=s1, s1_cycles=c1, s1_E=e1, stage2=s2, s2_cycles=c2, s2_E=e2,
                     lowest_freq=low, n_imag=nimag))
with open(os.path.join(root, "status.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("stage 1:", dict(collections.Counter(x["stage1"] for x in rows)))
print("stage 2:", dict(collections.Counter(x["stage2"] for x in rows)))
im = [x["refcode"] + f"({x['lowest_freq']})" for x in rows if x["n_imag"] not in ("", 0)]
print("imaginary modes:", ", ".join(im) if im else "none so far")
