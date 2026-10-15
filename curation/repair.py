"""Repair H on complexes that failed the Lewis/charge test after protonation."""
import json, sys
import numpy as np
from hgeom import bonds, predict, place
from lewis_check import rd, fragments, frag_charges

U = {r["refcode"]: r for r in json.load(open("out/zn_unique.json"))}


def consistent(el, X, q):
    nb, D = bonds(el, X)
    frs = fragments(el, nb)
    opts = [frag_charges(el, X, nb, f) for f in frs]
    if any(not o for o in opts):
        return False
    import itertools
    return any(sum(c) + 2 == q for c in itertools.product(*[list(o) for o in opts]))


def write(ref, el, X, note):
    with open(f"out/molecules_H/{ref}.xyz", "w") as fh:
        fh.write(f"{len(el)}\n{ref} {note}\n")
        for e, p in zip(el, X):
            fh.write(f"{e:2s} {p[0]:12.6f} {p[1]:12.6f} {p[2]:12.6f}\n")


def reprotonate(el, X):
    keep = [i for i, e in enumerate(el) if e != "H"]
    el = [el[i] for i in keep]; X = X[keep]
    nb, D = bonds(el, X); pred = predict(el, X, nb, D)
    new = []
    for i in range(len(el)):
        if pred[i][0] > 0:
            new += place(el, X, nb, i, pred[i][0], pred[i][2], [])
    return el + ["H"] * len(new), np.vstack([X, np.array(new)]) if new else X


for ref, src, strip in [("PMTCZN10", "out/molecules", True), ("TBZZNP01", "out/molecules", True),
                        ("ICUCIT", "out/molecules", False)]:
    r = U[ref]; want = int(r["H_expected"]); q = r["charge_csd"]
    el, X = rd(f"{src}/{ref}.xyz")
    if strip:
        el, X = reprotonate(el, X)
    else:
        nb, D = bonds(el, X)
        orphan = [h for h, e in enumerate(el) if e == "H" and len([j for j in nb[h] if el[j] != "H"]) != 1]
        k = [i for i in range(len(el)) if i not in orphan]; el = [el[i] for i in k]; X = X[k]
    nH = el.count("H")
    print(ref, "start H", nH, "want", want, "consistent", consistent(el, X, q))
    done = consistent(el, X, q) and nH == want
    if not done:
        nb, D = bonds(el, X); heavy = [i for i, e in enumerate(el) if e in ("C", "N", "O") and not any(el[j] == "Zn" for j in nb[i])]
        trials = []
        if nH > want:
            for h in [h for h, e in enumerate(el) if e == "H"]:
                k = [i for i in range(len(el)) if i != h]
                trials.append((f"removed H on {el[nb[h][0]]}{nb[h][0]}", [el[i] for i in k], X[k]))
        if nH < want:
            for i in heavy:
                Hs = [j for j in nb[i] if el[j] == "H"]
                for hyb in ("sp3", "sp2"):
                    P = place(el, X, nb, i, 1, hyb, Hs)
                    if P:
                        Dm = np.linalg.norm(X - P[0], axis=1); Dm[i] = 9
                        if Dm.min() > 1.6:
                            trials.append((f"added H on {el[i]}{i} ({hyb})", el + ["H"], np.vstack([X, P])))
        for note, e2, X2 in trials:
            if e2.count("H") == want and consistent(e2, X2, q):
                el, X = e2, X2; print("  fix:", note); done = True; break
        if not done and want - nH == 2:
            for note, e2, X2 in trials:
                nb2, D2 = bonds(e2, X2)
                for i in heavy:
                    Hs = [j for j in nb2[i] if e2[j] == "H"]
                    for hyb in ("sp3", "sp2"):
                        P = place(e2, X2, nb2, i, 1, hyb, Hs)
                        if not P: continue
                        Dm = np.linalg.norm(X2 - P[0], axis=1); Dm[i] = 9
                        if Dm.min() > 1.6:
                            e3, X3 = e2 + ["H"], np.vstack([X2, P])
                            if consistent(e3, X3, q):
                                el, X = e3, X3; done = True; print("  fix:", note, f"+ H on {e2[i]}{i} ({hyb})"); break
                    if done: break
                if done: break
    print("  final H", el.count("H"), "ok", done)
    if done:
        write(ref, el, X, "H completed geometrically and checked for closed-shell Lewis structure")
