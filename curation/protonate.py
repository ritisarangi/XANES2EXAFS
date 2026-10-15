"""Add missing H to the B_add_H complexes and validate H on every candidate.

For each complex: predict total H per heavy atom from geometry; existing H are kept.
If the predicted total differs from the CSD moiety H count, flip ambiguous atoms
(listed alternatives) until it matches, choosing the flips nearest to the default.
"""
import json, sys, os, itertools, collections
import numpy as np
from hgeom import bonds, predict, place

U = json.load(open(sys.argv[1])); MOL = sys.argv[2]; OUT = sys.argv[3]
os.makedirs(OUT, exist_ok=True)


def rd(p):
    L = open(p).read().strip().split("\n")[2:]
    return [l.split()[0] for l in L], np.array([[float(v) for v in l.split()[1:4]] for l in L])


def attached_H(el, nb, i):
    return [j for j in nb[i] if el[j] == "H"]


report = {}
for r in U:
    if r["category"] not in ("A_ready", "B_add_H"):
        continue
    el, X = rd(f"{MOL}/{r['refcode']}.xyz")
    nb, D = bonds(el, X)
    pred = predict(el, X, nb, D)
    want = int(r["H_expected"]) if r["H_expected"] != "" else el.count("H")
    heavy = [i for i, e in enumerate(el) if e != "H"]
    have = {i: len(attached_H(el, nb, i)) for i in heavy}
    # H bonded to more than one heavy atom, or to none
    hbad = [h for h, e in enumerate(el) if e == "H" and len([j for j in nb[h] if el[j] != "H"]) != 1]
    target = {i: max(pred[i][0], have[i]) if r["category"] == "B_add_H" else pred[i][0] for i in heavy}
    tot = sum(target.values())
    flips = []
    if tot != want:
        cand = [(i, a) for i in heavy for a in pred[i][1] if (a - target[i]) * (want - tot) > 0 and a >= have[i]]
        best = None
        for k in range(1, 5):
            for combo in itertools.combinations(cand, k):
                if len({c[0] for c in combo}) < k:
                    continue
                if tot + sum(a - target[i] for i, a in combo) == want:
                    best = combo; break
            if best:
                break
        if best:
            for i, a in best:
                flips.append((i, el[i], target[i], a)); target[i] = a
            tot = want
    rep = dict(want=want, pred_total=sum(target.values()), have=el.count("H"), hbad=len(hbad),
               flips=[f"{e}{i}:{a}->{b}" for i, e, a, b in flips])
    # per-atom disagreement between existing H and geometry prediction (for ready set)
    if r["category"] == "A_ready":
        dis = [(i, el[i], have[i], target[i]) for i in heavy if have[i] != target[i]]
        rep["atom_mismatch"] = [f"{e}{i}:has{a}/pred{b}" for i, e, a, b in dis]
    else:
        newpos = []
        newel = []
        for i in heavy:
            k = target[i] - have[i]
            if k > 0:
                P = place(el, X, nb, i, k, pred[i][2], attached_H(el, nb, i))
                newpos += P; newel += ["H"] * len(P)
        el2 = el + newel
        X2 = np.vstack([X] + [np.array(newpos)]) if newpos else X
        rep["added"] = len(newel)
        rep["final_H"] = el2.count("H")
        # clash check on new H
        nb2, D2 = bonds(el2, X2, tol=0.0)
        Dn = np.linalg.norm(X2[:, None] - X2[None], axis=2); np.fill_diagonal(Dn, 9)
        rep["min_newH_contact"] = round(float(min(Dn[len(el):].min(), 9)), 2) if newel else None
        with open(f"{OUT}/{r['refcode']}.xyz", "w") as fh:
            fh.write(f"{len(el2)}\n{r['refcode']} H completed geometrically ({len(newel)} added)\n")
            for e, p in zip(el2, X2):
                fh.write(f"{e:2s} {p[0]:12.6f} {p[1]:12.6f} {p[2]:12.6f}\n")
    report[r["refcode"]] = rep
json.dump(report, open(f"{OUT}/protonation_report.json", "w"), indent=1)
B = {k: v for k, v in report.items() if "added" in v}
for k, v in B.items():
    print(k, v)
A = {k: v for k, v in report.items() if "atom_mismatch" in v}
print("ready set:", len(A), "with any per-atom H disagreement:", sum(bool(v["atom_mismatch"]) for v in A.values()),
      "H-bond-topology problems:", sum(v["hbad"] > 0 for v in A.values()))
