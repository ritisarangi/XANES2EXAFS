#!/usr/bin/env python3
"""Lists the complexes that need more runs to give every Zn-L bond a closed-shell slope point.

Usage (inside the project folder):
    python3 <repo>/redox/select_missing.py .          # after the first round: list N reverse runs
    python3 <repo>/redox/select_missing.py . --eps    # after all reverse runs: list epsilon = 2 runs
Reads redox/redox_compare_all.csv and every redox/redox_compare_reverse_*.csv present.
A bond is covered when some run gives status 'use' with donor |spin| < 0.05.
Writes
  lists/reverse_N.txt   complexes with an uncovered Zn-N bond whose N carried spin >= 0.05 in the
                        first run, and that have not had a reverse run yet
  lists/eps_small.txt   (--eps only) complexes with any Zn-L bond still uncovered after the
                        first and reverse runs, for a CPCM epsilon = 2 run
Standard library only, Python 3.6+.
"""
import sys, os, csv, glob
dft = os.path.abspath(sys.argv[1])
F, R = {}, {}
for r in csv.DictReader(open(os.path.join(dft, "redox", "redox_compare_all.csv"))):
    F[(r["ref"], r["bond"])] = r
for p in sorted(glob.glob(os.path.join(dft, "redox", "redox_compare_reverse_*.csv"))):
    for r in csv.DictReader(open(p)):
        k = (r["ref"], r["bond"])
        if k not in R or (r["status"] == "use" and abs(float(r["spin_L"])) < abs(float(R[k]["spin_L"]))):
            R[k] = r
clean = lambda r: r is not None and r["status"] == "use" and abs(float(r["spin_L"])) < 0.05
covered = {k for k in set(F) | set(R) if clean(F.get(k)) or clean(R.get(k))}
had_reverse = {k[0] for k in R}
revN = sorted({k[0] for k, r in F.items() if k not in covered and r["el"] == "N" and r["status"] == "use"
               and abs(float(r["spin_L"])) >= 0.05 and k[0] not in had_reverse})
print("bonds covered: %d of %d" % (len(covered), len(F)))
if "--eps" in sys.argv:
    left = sorted({k[0] for k in F if k not in covered})
    open(os.path.join(dft, "lists", "eps_small.txt"), "w").write("\n".join(left) + "\n")
    print("lists/eps_small.txt: %d complexes with a bond still uncovered after the reverse runs" % len(left))
else:
    open(os.path.join(dft, "lists", "reverse_N.txt"), "w").write("\n".join(revN) + "\n")
    print("lists/reverse_N.txt: %d complexes (N spin, no reverse run yet)" % len(revN))
