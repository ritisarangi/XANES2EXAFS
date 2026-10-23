#!/usr/bin/env python3
"""Lists the complexes that need more runs to give every Zn-L bond a closed-shell slope point.

Usage (inside the project folder):
    python3 <repo>/redox/select_missing.py .          # after the first round: list N reverse runs
    python3 <repo>/redox/select_missing.py . --eps --next   # a later batch, skipping complexes already listed
    python3 <repo>/redox/select_missing.py . --eps    # list low-dielectric runs (complexes whose reverse run is still pending are left for later)
Reads redox/redox_compare_all.csv and every redox/redox_compare_reverse_*.csv present.
A bond is covered when some run gives status 'use' with donor |spin| < 0.05.
Writes
  lists/reverse_N.txt   complexes with an uncovered Zn-N bond whose N carried spin >= 0.05 in the
                        first run, and that have not had a reverse run yet
  lists/eps_small.txt   (--eps only) complexes with a Zn-L bond still uncovered after the first
                        and reverse runs because its donor carried spin or the bond dissociated,
                        for a low-dielectric run. Bonds that only moved < 0.01 A are left out: a
                        dielectric change moves them too little as well; they take the donor-type slope.
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
    def tiny(k):   # moved < 0.01 A with a closed-shell donor in some run: noise, not a missing state
        return any(r is not None and r["status"] == "small" and abs(float(r["spin_L"])) < 0.05
                   for r in (F.get(k), R.get(k)))
    planned = set()
    for p in glob.glob(os.path.join(dft, "lists", "reverse_*.txt")):
        planned |= {l.strip() for l in open(p) if l.strip()}
    pending = planned - {k[0] for k in R}          # reverse run planned but not analysed yet
    left = sorted({k[0] for k in F if k not in covered and not tiny(k) and k[0] not in pending})
    q = {k[0]: int(r["charge_ref"]) for k, r in F.items()}
    if "--next" in sys.argv:                       # a later batch: skip complexes already listed
        done_before = set()
        for p in glob.glob(os.path.join(dft, "lists", "eps1*.txt")) + glob.glob(os.path.join(dft, "lists", "eps2_anion*.txt")):
            done_before |= {l.strip() for l in open(p) if l.strip()}
        left = [r for r in left if r not in done_before]
    eps1 = [r for r in left if q[r] > -2]          # vacuum (epsilon = 1)
    eps2 = [r for r in left if q[r] <= -2]         # anions -2 and below: epsilon = 2, vacuum may not bind the electrons
    sfx = "_next" if "--next" in sys.argv else ""
    open(os.path.join(dft, "lists", "eps1%s.txt" % sfx), "w").write("\n".join(eps1) + "\n")
    open(os.path.join(dft, "lists", "eps2_anion%s.txt" % sfx), "w").write("\n".join(eps2) + "\n")
    print("waiting on a reverse run, not listed yet: %d complexes" % len({k[0] for k in F if k not in covered and k[0] in pending}))
    print("lists/eps1%s.txt: %d complexes (epsilon = 1)   lists/eps2_anion%s.txt: %d complexes (charge <= -2, epsilon = 2)" % (sfx, len(eps1), sfx, len(eps2)))
else:
    open(os.path.join(dft, "lists", "reverse_N.txt"), "w").write("\n".join(revN) + "\n")
    print("lists/reverse_N.txt: %d complexes (N spin, no reverse run yet)" % len(revN))
