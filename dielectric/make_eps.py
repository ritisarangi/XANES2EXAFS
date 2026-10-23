#!/usr/bin/env python3
"""Write optimisation + Hessian inputs for each complex at other CPCM dielectric constants.

Usage (inside the project folder on S3DF):
    python3 <repo>/dielectric/make_eps.py . lists/pilot.txt 4 2
Starts from the stage-2 B3LYP geometry (stage2_b3lyp/<REF>/<REF>.xyz) with the stage-2
method, basis, charge and multiplicity. Only the dielectric constant changes; the cavity
stays the stage-2 water cavity (Rsolv 1.30, Gaussian vdW surface, element radii).
Writes dielectric/eps<E>/<REF>/<REF>.inp and dielectric/jobs_<tag>.txt.
Standard library only, Python 3.6+.
"""
import sys, os, json

dft = os.path.abspath(sys.argv[1])
lst = sys.argv[2]
eps_list = sys.argv[3:] or ["4", "2"]
tag = os.path.splitext(os.path.basename(lst))[0]
refs = [l.strip() for l in open(os.path.join(dft, lst)) if l.strip() and not l.startswith("#")]
jobs, skipped = [], []
for e in eps_list:
    eps = float(e)
    for ref in refs:
        s2 = os.path.join(dft, "stage2_b3lyp", ref)
        xyz, meta = os.path.join(s2, ref + ".xyz"), os.path.join(s2, ref + ".meta")
        if not (os.path.exists(xyz) and os.path.exists(meta)):
            skipped.append(ref)
            continue
        M = json.load(open(meta))
        L = open(xyz).read().strip().split("\n")[2:]
        if len(L) != M["natoms"]:
            skipped.append(ref)
            continue
        tz = set(M["donors"]) | {M["zn_index"]}
        rows = []
        for i, l in enumerate(L):
            el, x, y, z = l.split()[:4]
            rows.append("  %-2s %12.6f %12.6f %12.6f" % (el, float(x), float(y), float(z))
                        + (' newgto "def2-TZVP" end' if i in tz else ""))
        uks = " UKS" if M["mult"] > 1 else ""
        d = os.path.join("dielectric", "eps%g" % eps, ref)
        os.makedirs(os.path.join(dft, d), exist_ok=True)
        # epsilon = 1 is vacuum: run without CPCM (CPCM at epsilon 1 has zero screening and ORCA's
        # property step fails on it with a diagonalization error)
        solv = "" if eps <= 1.0 else " CPCM"
        cpcm = "" if eps <= 1.0 else "%%cpcm\n  epsilon %g\n  refrac 1.3328\n  rsolv 1.30\nend\n" % eps
        inp = ("# %s: stage-2 level at %s, from the stage-2 geometry\n" % (ref, "gas phase (epsilon 1)" if eps <= 1.0 else "CPCM epsilon %g" % eps)
               + "! B3LYP D3BJ def2-SVP def2/J RIJCOSX%s TightOpt Freq DefGrid3 TightSCF%s\n" % (solv, uks)
               + "%pal nprocs 16 end\n%maxcore 3000\n%geom MaxIter 300 end\n%scf MaxIter 500 end\n"
               + cpcm
               + "* xyz %d %d\n" % (M["charge"], M["mult"]) + "\n".join(rows) + "\n*\n")
        open(os.path.join(dft, d, ref + ".inp"), "w").write(inp)
        jobs.append(d)
jf = os.path.join(dft, "dielectric", "jobs_%s.txt" % tag)
open(jf, "w").write("\n".join(jobs) + "\n")
print("inputs: %d (%s x %d complexes)  skipped: %s" % (len(jobs), ",".join(eps_list), len(refs), " ".join(sorted(set(skipped))) or "none"))
print("jobs file:", os.path.relpath(jf, dft))
