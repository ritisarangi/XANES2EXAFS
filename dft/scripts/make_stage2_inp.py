#!/usr/bin/env python3
"""Write stage2_b3lyp/<REF>/<REF>.inp from the converged stage-1 geometry.

Zn and its first-shell donor atoms (indices in <REF>.meta, same atom order as stage 1)
get def2-TZVP through per-atom newgto; all other atoms use the def2-SVP default.
Standard library only, so it runs on S3DF nodes without extra modules.
"""
import json, sys, os

root, ref = sys.argv[1], sys.argv[2]
s1 = os.path.join(root, "stage1_r2scan", ref)
s2 = os.path.join(root, "stage2_b3lyp", ref)
out = open(os.path.join(s1, ref + ".out"), errors="ignore").read() if os.path.exists(os.path.join(s1, ref + ".out")) else ""
if "ORCA TERMINATED NORMALLY" not in out or "OPTIMIZATION RUN DONE" not in out:
    sys.exit(f"{ref}: stage 1 not converged")
meta = json.load(open(os.path.join(s2, ref + ".meta")))
L = open(os.path.join(s1, ref + ".xyz")).read().strip().split("\n")[2:]
if len(L) != meta["natoms"]:
    sys.exit(f"{ref}: atom count changed ({len(L)} vs {meta['natoms']})")
tz = set(meta["donors"]) | {meta["zn_index"]}
rows = []
for i, l in enumerate(L):
    e, x, y, z = l.split()[:4]
    rows.append(f"  {e:2s} {float(x):12.6f} {float(y):12.6f} {float(z):12.6f}" + (' newgto "def2-TZVP" end' if i in tz else ""))
uks = " UKS" if meta["mult"] > 1 else ""
inp = (f"# {ref} stage 2: B3LYP-D3(BJ) CPCM(water) TightOpt + Freq; def2-TZVP on Zn + donors {sorted(tz)}, def2-SVP elsewhere\n"
       f"! B3LYP D3BJ def2-SVP def2/J RIJCOSX CPCM(water) TightOpt Freq DefGrid3 TightSCF{uks}\n"
       f"%pal nprocs 16 end\n%maxcore 3000\n%geom MaxIter 300 end\n%scf MaxIter 500 end\n"
       f"* xyz {meta['charge']} {meta['mult']}\n" + "\n".join(rows) + "\n*\n")
open(os.path.join(s2, ref + ".inp"), "w").write(inp)
print(f"{ref}: stage 2 input written ({len(tz)} atoms def2-TZVP)")
