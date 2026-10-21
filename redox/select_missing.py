#!/usr/bin/env python3
"""Lists the complexes that need more runs to give every Zn-L bond a closed-shell slope point.

Usage (inside the project folder):  python3 <repo>/redox/select_missing.py .
Reads redox/redox_compare_all.csv and redox/redox_compare_reverse_reverse_S.csv (if present).
A bond is covered when some run gives status 'use' with donor |spin| < 0.05.
Writes
  lists/reverse_N.txt   complexes with an uncovered Zn-N bond whose N carried spin >= 0.05 in the
                        first run, and that have not had a reverse run yet
  lists/eps_small.txt   complexes with an uncovered bond that moved < 0.01 A in the first run
                        (status 'small'), for a CPCM epsilon = 2 run
Standard library only, Python 3.6+.
"""
import sys, os, csv
dft = os.path.abspath(sys.argv[1])
F, R = {}, {}
for fn, T in (("redox_compare_all.csv", F), ("redox_compare_reverse_reverse_S.csv", R)):
    p = os.path.join(dft, "redox", fn)
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            T[(r["ref"], r["bond"])] = r
clean = lambda r: r is not None and r["status"] == "use" and abs(float(r["spin_L"])) < 0.05
covered = {k for k in set(F) | set(R) if clean(F.get(k)) or clean(R.get(k))}
had_reverse = {k[0] for k in R}
revN = sorted({k[0] for k, r in F.items() if k not in covered and r["el"] == "N" and r["status"] == "use"
               and abs(float(r["spin_L"])) >= 0.05 and k[0] not in had_reverse})
small = sorted({k[0] for k, r in F.items() if k not in covered and r["status"] == "small"})
open(os.path.join(dft, "lists", "reverse_N.txt"), "w").write("\n".join(revN) + "\n")
open(os.path.join(dft, "lists", "eps_small.txt"), "w").write("\n".join(small) + "\n")
print("bonds covered: %d of %d" % (len(covered), len(F)))
print("lists/reverse_N.txt: %d complexes (N spin, no reverse run yet)" % len(revN))
print("lists/eps_small.txt: %d complexes (bond moved < 0.01 A)" % len(small))
