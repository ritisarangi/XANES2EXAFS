"""Build the two-stage ORCA workflow for the Zn DFT set.

Layout (mirrors S3DF REMOTE=/sdf/data/ssrl/smb/xas/users/ritis/Zn_small_molecule_dft):
  dft/s3df.env
  dft/lists/all.txt, pilot.txt          one refcode per line; array index = line number
  dft/stage1_r2scan/<REF>/<REF>.inp     r2SCAN-3c CPCM(water) Opt, crystal start geometry
  dft/stage2_b3lyp/<REF>/<REF>.meta     charge, multiplicity, 0-based donor-atom indices
  dft/scripts/stage1_array.slurm, stage2_array.slurm, make_stage2_inp.py, submit.sh, status.py
"""
import glob, os, re, json
import numpy as np
from hgeom import bonds
from lewis_check import rd

OUT = "dft"
for d in ("lists", "stage1_r2scan", "stage2_b3lyp", "scripts"):
    os.makedirs(f"{OUT}/{d}", exist_ok=True)
open(f"{OUT}/s3df.env", "w").write("REMOTE=/sdf/data/ssrl/smb/xas/users/ritis/Zn_small_molecule_dft\n")

refs, size = [], {}
for p in sorted(glob.glob("final/dft_ready_xyz/*.xyz")):
    ref = os.path.basename(p)[:-4]
    head = open(p).read().split("\n")[1]
    q = int(re.search(r"charge=(-?\d+)", head).group(1)); m = int(re.search(r"mult=(\d+)", head).group(1))
    el, X = rd(p)
    nb, D = bonds(el, X)
    z = el.index("Zn")
    donors = sorted(j for j in nb[z] if el[j] not in ("H", "Si") and D[z, j] <= 2.8)
    coords = "\n".join(f"  {e:2s} {x:12.6f} {y:12.6f} {zz:12.6f}" for e, (x, y, zz) in zip(el, X))
    d1 = f"{OUT}/stage1_r2scan/{ref}"; os.makedirs(d1, exist_ok=True)
    uks = " UKS" if m > 1 else ""
    open(f"{d1}/{ref}.inp", "w").write(
        f"# {ref} stage 1: r2SCAN-3c CPCM(water) optimization from crystal geometry\n"
        f"! r2SCAN-3c CPCM(water) Opt TightSCF{uks}\n"
        f"%pal nprocs 8 end\n%maxcore 3000\n"
        f"%geom MaxIter 300 end\n%scf MaxIter 500 end\n"
        f"* xyz {q} {m}\n{coords}\n*\n")
    d2 = f"{OUT}/stage2_b3lyp/{ref}"; os.makedirs(d2, exist_ok=True)
    json.dump(dict(ref=ref, charge=q, mult=m, natoms=len(el), donors=donors,
                   donor_elems=[el[j] for j in donors], zn_index=z), open(f"{d2}/{ref}.meta", "w"))
    refs.append(ref); size[ref] = len(el)

open(f"{OUT}/lists/all.txt", "w").write("\n".join(refs) + "\n")
# pilot: one per main donor class, spanning sizes
import json as _j
aud = {r["refcode"]: r for r in _j.load(open("final/final_audit.json"))}
pilot = []
for dset in ("S4", "N2S2", "N3S1", "N1S3", "N4"):
    c = sorted([r for r in refs if aud[r]["donors"] == dset], key=lambda r: size[r])
    if c:
        pilot.append(c[len(c) // 2])
big = max(refs, key=lambda r: size[r]); pilot.append(big)
open(f"{OUT}/lists/pilot.txt", "w").write("\n".join(pilot) + "\n")
print("jobs", len(refs), "pilot", [(r, size[r], aud[r]["donors"]) for r in pilot])
