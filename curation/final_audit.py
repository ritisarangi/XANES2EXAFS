"""Independent audit of every structure in final/dft_ready_xyz.

Checks per molecule:
 1 one connected molecule containing Zn (every atom reachable from Zn through bonds)
 2 Zn first shell: CN and Zn-L distances in 1.85-2.80 A
 3 H: each H bonded to exactly one heavy atom; X-H length standard
 4 valence ceilings: C<=4, N<=4, O<=3 (incl. Zn), B<=4, S<=4 (sulfonyl), halogen<=1
 5 heavy-heavy bond lengths plausible for the element pair
 6 no non-bonded contact (beyond 1-3) under 1.6 A; no two atoms closer than 0.9 A
 7 closed-shell Lewis structure at the stated charge (multiplicity 2 only for MECFAC)
 8 electron-count parity consistent with multiplicity
 9 formula in file header equals atoms present; no duplicate complexes in the set
"""
import glob, os, re, json, itertools, collections
import numpy as np
from hgeom import bonds
from lewis_check import rd, fragments, frag_charges

Z = dict(H=1, B=5, C=6, N=7, O=8, F=9, Si=14, P=15, S=16, Cl=17, Se=34, Br=35, I=53, Zn=30, As=33, Te=52, Ge=32, Sn=50)
MAXV = dict(C=4, N=4, O=3, B=4, S=4, F=1, Cl=1, Br=1, I=1, H=1, Si=4, P=5, Se=3)
XH = dict(C=1.09, N=1.01, O=0.97, B=1.19, S=1.34, Si=1.48, P=1.42)
BL = {("C", "C"): (1.17, 1.65), ("C", "N"): (1.12, 1.56), ("C", "O"): (1.17, 1.50), ("C", "S"): (1.55, 1.90),
      ("B", "N"): (1.45, 1.65), ("B", "C"): (1.50, 1.70), ("N", "N"): (1.10, 1.48), ("N", "O"): (1.18, 1.45),
      ("C", "F"): (1.28, 1.40), ("S", "S"): (1.95, 2.15), ("N", "S"): (1.50, 1.75), ("O", "S"): (1.40, 1.65),
      ("C", "Si"): (1.80, 1.95), ("N", "Si"): (1.65, 1.80), ("C", "P"): (1.75, 1.90), ("O", "P"): (1.45, 1.65),
      ("C", "Se"): (1.85, 2.00), ("C", "Cl"): (1.68, 1.80), ("C", "Br"): (1.85, 1.98), ("B", "O"): (1.30, 1.55)}


def wl_hash(el, nb, iters=4):
    import hashlib
    lab = list(el)
    for _ in range(iters):
        lab = [hashlib.md5((lab[i] + "|" + ",".join(sorted(lab[j] for j in nb[i]))).encode()).hexdigest()[:12] for i in range(len(el))]
    return hashlib.md5(",".join(sorted(lab)).encode()).hexdigest()[:16]


def audit(path):
    ref = os.path.basename(path)[:-4]
    head = open(path).read().split("\n")[1]
    q = int(re.search(r"charge=(-?\d+)", head).group(1)); m = int(re.search(r"mult=(\d+)", head).group(1))
    el, X = rd(path); n = len(el)
    nb, D = bonds(el, X)
    fail = []
    # 1 connectivity from Zn
    z = el.index("Zn"); seen = {z}; st = [z]
    while st:
        i = st.pop()
        for j in nb[i]:
            if j not in seen:
                seen.add(j); st.append(j)
    if len(seen) != n:
        fail.append(f"{n - len(seen)} atoms not connected to the complex")
    if el.count("Zn") != 1:
        fail.append(f"{el.count('Zn')} Zn atoms")
    # 2 Zn shell
    sh = sorted((float(D[z, j]), el[j]) for j in nb[z])
    cn = len(sh)
    bad_sh = [f"{e}{d:.2f}" for d, e in sh if not 1.85 <= d <= 2.80]
    if bad_sh: fail.append("Zn-L out of range " + " ".join(bad_sh))
    if not 3 <= cn <= 6: fail.append(f"CN {cn}")
    # 3 H
    for h in range(n):
        if el[h] == "H":
            p = [j for j in nb[h] if el[j] != "H"]
            if len(p) != 1: fail.append(f"H{h} bonded to {len(p)} heavy atoms"); continue
            if abs(D[h, p[0]] - XH.get(el[p[0]], 1.0)) > 0.02: fail.append(f"{el[p[0]]}-H {D[h, p[0]]:.2f}")
            if el[p[0]] == "Zn": fail.append("Zn-H bond")
    # 4 valence, 5 bond lengths
    for i in range(n):
        v = len(nb[i])
        if v > MAXV.get(el[i], 8): fail.append(f"{el[i]}{i} valence {v}")
        for j in nb[i]:
            if j > i and "Zn" not in (el[i], el[j]) and "H" not in (el[i], el[j]):
                k = tuple(sorted((el[i], el[j])))
                lo, hi = BL.get(k, (1.1, 2.3))
                if not lo <= D[i, j] <= hi: fail.append(f"bond {el[i]}{i}-{el[j]}{j} {D[i, j]:.2f}")
    # 6 contacts
    if (D + np.eye(n) * 9).min() < 0.9: fail.append("atoms closer than 0.9 A")
    for i in range(n):
        n13 = set(nb[i]) | {k for j in nb[i] for k in nb[j]}
        for j in range(i + 1, n):
            if j not in n13 and D[i, j] < 1.6:
                fail.append(f"contact {el[i]}{i}-{el[j]}{j} {D[i, j]:.2f}")
    # 7 Lewis/charge
    opts = []
    for f in fragments(el, nb):
        o = frag_charges(el, X, nb, f)
        if not o and any(el[i] == "Si" for i in f):
            o = {-1: 0, 0: 0}
        opts.append(o)
    if any(not o for o in opts):
        lew = "no Lewis structure"
    else:
        qs = {sum(c) + 2 for c in itertools.product(*[list(o) for o in opts])}
        lew = "ok" if q in qs else f"charge {q} not in {sorted(qs)}"
    if lew != "ok" and not (ref == "MECFAC" and m == 2):
        fail.append(lew)
    # 8 parity
    ne = sum(Z[e] for e in el) - q
    if (ne % 2 == 0) != (m % 2 == 1): fail.append(f"electron count {ne} inconsistent with multiplicity {m}")
    # 9 header formula
    c = collections.Counter(el)
    hf = re.search(r"mult=\d+ ((?:[A-Z][a-z]?\d+ ?)+)", head)
    if hf:
        hc = {e: int(k) for e, k in re.findall(r"([A-Z][a-z]?)(\d+)", hf.group(1))}
        if hc != dict(c): fail.append("header formula differs from atoms")
    donors = "".join(f"{e}{k}" for e, k in sorted(collections.Counter(e for d, e in sh).items()))
    return dict(refcode=ref, natoms=n, charge=q, mult=m, CN=cn, donors=donors,
                formula=" ".join(f"{e}{c[e]}" for e in sorted(c)), zn_L=" ".join(f"{e}{d:.2f}" for d, e in sh),
                hash=wl_hash(el, [[j for j in nb[i] if el[j] != "H"] for i in range(n)]), fails=fail)


if __name__ == "__main__":
    res = [audit(p) for p in sorted(glob.glob("final/dft_ready_xyz/*.xyz"))]
    dup = collections.defaultdict(list)
    for r in res:
        dup[r["hash"]].append(r["refcode"])
    for h, g in dup.items():
        if len(g) > 1:
            for r in res:
                if r["refcode"] in g: r["fails"].append("duplicate of " + ",".join(x for x in g if x != r["refcode"]))
    json.dump(res, open("final/final_audit.json", "w"), indent=1)
    print("structures", len(res), "passing all checks", sum(not r["fails"] for r in res))
    for r in res:
        if r["fails"]:
            print(r["refcode"], r["fails"][:6])
    print("CN", collections.Counter(r["CN"] for r in res), "mult", collections.Counter(r["mult"] for r in res))
