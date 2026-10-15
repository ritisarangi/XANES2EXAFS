"""Re-protonate complexes whose deposited coordinates lack some or all H.

Strategy: strip every H, rebuild connectivity, perceive bond orders with Open Babel
from 3D geometry, add H, and compare the H count with the CSD moiety formula.
Two variants are tried: Zn-donor bonds kept (donor valence counted) and removed.
"""
import json, sys, os
from openbabel import openbabel as ob, pybel

ob.obErrorLog.SetOutputLevel(0)
U = json.load(open(sys.argv[1]))
MOL = sys.argv[2]
OUT = sys.argv[3]
os.makedirs(OUT, exist_ok=True)


def read_xyz(p):
    L = open(p).read().strip().split("\n")[2:]
    return [(l.split()[0], tuple(map(float, l.split()[1:4]))) for l in L]


def build(atoms, keep_zn_bonds):
    m = ob.OBMol()
    for e, (x, y, z) in atoms:
        a = m.NewAtom()
        a.SetAtomicNum(ob.GetAtomicNum(e))
        a.SetVector(x, y, z)
    m.ConnectTheDots()
    zn = [a for a in ob.OBMolAtomIter(m) if a.GetAtomicNum() == 30]
    for z in zn:
        for b in list(ob.OBAtomBondIter(z)):
            if not keep_zn_bonds:
                m.DeleteBond(b)
    m.PerceiveBondOrders()
    m.AddHydrogens(False, False)
    return m


def to_atoms(m):
    return [(ob.GetSymbol(a.GetAtomicNum()), (a.GetX(), a.GetY(), a.GetZ())) for a in ob.OBMolAtomIter(m)]


res = {}
for r in U:
    if r["category"] != "B_add_H":
        continue
    atoms = [a for a in read_xyz(f"{MOL}/{r['refcode']}.xyz") if a[0] != "H"]
    want = int(r["H_expected"])
    out = {}
    for keep in (True, False):
        m = build(atoms, keep)
        nh = sum(1 for a in ob.OBMolAtomIter(m) if a.GetAtomicNum() == 1)
        out[keep] = (nh, m)
    res[r["refcode"]] = dict(want=want, keep=out[True][0], drop=out[False][0], had=r["n_H"])
    best = None
    for keep in (True, False):
        if out[keep][0] == want:
            best = keep; break
    res[r["refcode"]]["chosen"] = best
    if best is not None:
        A = to_atoms(out[best][1])
        with open(f"{OUT}/{r['refcode']}.xyz", "w") as fh:
            fh.write(f"{len(A)}\n{r['refcode']} H added (Open Babel, zn_bonds={'kept' if best else 'removed'})\n")
            for e, (x, y, z) in A:
                fh.write(f"{e:2s} {x:12.6f} {y:12.6f} {z:12.6f}\n")
for k, v in res.items():
    print(k, v)
