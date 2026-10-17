#!/usr/bin/env python3
"""mkinp.py <repo> <REF> <nprocs> <maxcore> <geom maxiter>  -> stage-2-level opt input on stdout (scan KEYS, same basis layout)"""
import sys, os, json
repo, ref, npr, mc, it = sys.argv[1:6]
meta = json.load(open(os.path.join(repo, "dft/stage2_b3lyp", ref, ref + ".meta")))
L = open(os.path.join(repo, "structures/dft_ready_xyz", ref + ".xyz")).read().strip().split("\n")[2:]
tz = set(meta["donors"]) | {meta["zn_index"]}
rows = ["  %-2s %12.6f %12.6f %12.6f%s" % (l.split()[0], float(l.split()[1]), float(l.split()[2]), float(l.split()[3]),
        ' newgto "def2-TZVP" end' if i in tz else "") for i, l in enumerate(L)]
uks = " UKS" if meta["mult"] > 1 else ""
print("! B3LYP D3BJ def2-SVP def2/J RIJCOSX CPCM(water) TightOpt DefGrid3 TightSCF%s\n%%pal nprocs %s end\n%%maxcore %s\n"
      "%%scf MaxIter 500 end\n%%geom MaxIter %s end\n* xyz %d %d\n%s\n*" % (uks, npr, mc, it, meta["charge"], meta["mult"], "\n".join(rows)))
