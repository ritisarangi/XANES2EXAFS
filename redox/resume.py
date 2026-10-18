#!/usr/bin/env python3
"""Continue a redox optimisation that Slurm stopped (preemption, requeue, time limit).

Usage (inside one redox/<primary|fallback>/<REF> folder):  python3 <repo>/redox/resume.py REF
When REF.out exists without a normal termination and ORCA left a current geometry in REF.xyz,
the original input is kept once as REF_orig.inp, REF.inp is rewritten to start from REF.xyz
(same method, charge, multiplicity and per-atom basis), and the partial output is renamed
REF_tryN.out. REF.gbw, when present, is picked up by ORCA as the starting guess.
Prints what it did. Standard library only, Python 3.6+.
"""
import sys, os


def main():
    ref = sys.argv[1]
    out, xyz, inp, orig = ref + ".out", ref + ".xyz", ref + ".inp", ref + "_orig.inp"
    if not os.path.exists(out):
        print(ref, "no partial output; starting fresh")
        return
    if "ORCA TERMINATED NORMALLY" in open(out, errors="ignore").read():
        return
    src = open(orig if os.path.exists(orig) else inp).read()
    head, rest = src.split("* xyz", 1)
    lines = rest.strip().split("\n")
    cm = lines[0].split()
    old = [l for l in lines[1:] if l.strip() != "*"]
    G = []
    if os.path.exists(xyz):
        L = open(xyz).read().strip().split("\n")
        if len(L) >= 2 and L[0].strip().isdigit() and int(L[0]) == len(old):
            G = [l.split()[:4] for l in L[2:2 + len(old)]]
    i = 1
    while os.path.exists("%s_try%d.out" % (ref, i)):
        i += 1
    os.rename(out, "%s_try%d.out" % (ref, i))
    if len(G) != len(old):
        print(ref, "partial output kept as %s_try%d.out; no usable geometry, restarting from the input" % (ref, i))
        return
    if not os.path.exists(orig):
        os.rename(inp, orig)
    rows = []
    for g, o in zip(G, old):
        extra = ' newgto "def2-TZVP" end' if "newgto" in o else ""
        rows.append("  %-2s %12.6f %12.6f %12.6f%s" % (g[0], float(g[1]), float(g[2]), float(g[3]), extra))
    open(inp, "w").write(head + "* xyz %s %s\n%s\n*\n" % (cm[0], cm[1], "\n".join(rows)))
    print(ref, "resuming from the last geometry in %s (partial output kept as %s_try%d.out)" % (xyz, ref, i))


if __name__ == "__main__":
    main()
