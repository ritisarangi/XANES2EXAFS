#!/usr/bin/env python3
"""List complexes that need the reverse charge step: any Zn-S donor with Mulliken spin >= CUT
in the primary redox run (the S stopped being a closed-shell thiolate).

Usage (inside the project folder):  python3 <repo>/redox/select_reverse.py . [0.05]
Reads redox/redox_compare_all.csv, writes lists/reverse_S.txt. Standard library only.
"""
import sys, os, csv
dft = os.path.abspath(sys.argv[1])
cut = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
rows = list(csv.DictReader(open(os.path.join(dft, "redox", "redox_compare_all.csv"))))
refs = sorted({r["ref"] for r in rows if r["el"] == "S" and abs(float(r["spin_L"])) >= cut})
open(os.path.join(dft, "lists", "reverse_S.txt"), "w").write("\n".join(refs) + "\n")
from collections import Counter
print("complexes with S spin >= %.2f: %d" % (cut, len(refs)))
print("by reference charge:", dict(Counter(next(r["charge_ref"] for r in rows if r["ref"] == x) for x in refs)))
print("wrote lists/reverse_S.txt")
