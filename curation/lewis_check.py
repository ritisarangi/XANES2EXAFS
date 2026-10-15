"""Validate structures: each ligand fragment (Zn removed) must admit a closed-shell Lewis
structure at some integer charge, and fragment charges + 2 (Zn2+) must equal the complex
charge. Gives a ligand-derived charge independent of the CSD moiety charge.
"""
import json, sys, itertools
import numpy as np
from rdkit import Chem, RDLogger
from rdkit.Chem import rdDetermineBonds
from hgeom import bonds

RDLogger.DisableLog("rdApp.*")


def rd(p):
    L = open(p).read().strip().split("\n")[2:]
    return [l.split()[0] for l in L], np.array([[float(v) for v in l.split()[1:4]] for l in L])


def fragments(el, nb):
    n = len(el); f = [-1] * n; k = 0
    for s in range(n):
        if el[s] == "Zn" or f[s] >= 0:
            continue
        st = [s]; f[s] = k
        while st:
            i = st.pop()
            for j in nb[i]:
                if el[j] != "Zn" and f[j] < 0:
                    f[j] = k; st.append(j)
        k += 1
    return [[i for i in range(n) if f[i] == c] for c in range(k)]


def frag_charges(el, X, nb, idx, trial=(-4, -3, -2, -1, 0, 1, 2)):
    """Charges at which the fragment has a closed-shell Lewis structure, and its SMILES."""
    ok = {}
    for q in trial:
        m = Chem.RWMol()
        mp = {}
        for i in idx:
            mp[i] = m.AddAtom(Chem.Atom(el[i]))
        for i in idx:
            for j in nb[i]:
                if j in mp and i < j:
                    m.AddBond(mp[i], mp[j], Chem.BondType.SINGLE)
        conf = Chem.Conformer(len(idx))
        for i in idx:
            conf.SetAtomPosition(mp[i], X[i].tolist())
        mol = m.GetMol(); mol.AddConformer(conf)
        nel = sum(a.GetAtomicNum() for a in mol.GetAtoms()) - q
        if nel % 2:
            continue
        try:
            rdDetermineBonds.DetermineBondOrders(mol, charge=q, allowChargedFragments=True, embedChiral=False)
            if sum(a.GetNumRadicalElectrons() for a in mol.GetAtoms()) == 0:
                fc = sum(abs(a.GetFormalCharge()) for a in mol.GetAtoms())
                ok[q] = (fc, Chem.MolToSmiles(Chem.RemoveHs(mol, sanitize=False)))
        except Exception:
            pass
    return ok


if __name__ == "__main__":
    U = json.load(open(sys.argv[1])); MOLS = sys.argv[2:]
    res = {}
    for r in U:
        if r["category"] not in ("A_ready", "B_add_H"):
            continue
        path = None
        for d in MOLS:
            try:
                open(f"{d}/{r['refcode']}.xyz").close(); path = f"{d}/{r['refcode']}.xyz"; break
            except FileNotFoundError:
                pass
        el, X = rd(path)
        nb, D = bonds(el, X)
        frs = fragments(el, nb)
        opts = [frag_charges(el, X, nb, f) for f in frs]
        q_csd = r["charge_csd"] if r["charge_csd"] != "" else None
        combos = []
        for c in itertools.product(*[list(o.keys()) for o in opts]):
            combos.append((sum(c) + 2, sum(opts[k][c[k]][0] for k in range(len(c))), c))
        status = "fail"; q_lig = None; chosen = None
        if any(not o for o in opts):
            status = "no_lewis_structure"
        elif q_csd is not None and any(cb[0] == q_csd for cb in combos):
            chosen = min([cb for cb in combos if cb[0] == q_csd], key=lambda x: x[1]); status = "consistent"; q_lig = q_csd
        elif combos:
            chosen = min(combos, key=lambda x: (x[1], abs(x[0]))); status = "charge_disagrees"; q_lig = chosen[0]
        smi = ".".join(opts[k][chosen[2][k]][1] for k in range(len(frs))) if chosen else ""
        res[r["refcode"]] = dict(status=status, q_csd=q_csd, q_lig=q_lig, n_frag=len(frs),
                                 frag_q=list(chosen[2]) if chosen else None, smiles=smi,
                                 nH=el.count("H"), natoms=len(el), path=path,
                                 options=[sorted(o) for o in opts])
    json.dump(res, open("out/lewis_check.json", "w"), indent=1)
    import collections
    print(collections.Counter(v["status"] for v in res.values()))
    for k, v in res.items():
        if v["status"] != "consistent":
            print(k, v["status"], "csd", v["q_csd"], "lig", v["q_lig"], v["options"], v["smiles"][:90])
