"""Clean the 51 review complexes: disorder removed, overlaps resolved, H completed,
charge validated, X-H normalized. Writes out_rev/clean/<REF>.xyz and clean_report.json."""
import json, re, itertools, os
import numpy as np
from hgeom import bonds, predict, place, ang
from lewis_check import rd, fragments, frag_charges
from moiety import parse_moiety

OLD = {r["refcode"]: r for r in json.load(open("out/zn_unique.json"))}
REV = json.load(open("final/review_list.json"))["review"]
os.makedirs("out_rev/clean", exist_ok=True)
XH = dict(C=1.09, N=1.01, O=0.97, B=1.19, S=1.34, Si=1.48, P=1.42)
ALK = ("Li", "Na", "K", "Rb", "Cs")


def cnt(el):
    c = {}
    for e in el:
        c[e] = c.get(e, 0) + 1
    return c


def fstr(c):
    return " ".join(f"{k}{v}" for k, v in sorted(c.items()))


def zn_target(moiety):
    for mult, comp, ch in parse_moiety(moiety):
        if abs(comp.get("Zn", 0) - 1) < 0.01:
            return {k: int(round(v)) for k, v in comp.items()}, ch
    return None, None


def overlaps(el, X, cut=1.35):
    D = np.linalg.norm(X[:, None] - X[None], axis=2)
    return [(i, j) for i in range(len(el)) for j in range(i + 1, len(el))
            if el[i] == el[j] and el[i] not in ("H", "Zn") and D[i, j] < cut]


def drop(el, X, rm):
    nb, D = bonds(el, X)
    gone = set(rm)
    for i in rm:
        gone |= {j for j in nb[i] if el[j] == "H"}
    k = [i for i in range(len(el)) if i not in gone]
    return [el[i] for i in k], X[k]


def lewis_qs(el, X):
    nb, D = bonds(el, X)
    opts = []
    for f in fragments(el, nb):
        o = frag_charges(el, X, nb, f)
        if not o and any(el[i] == "Si" for i in f):     # RDKit cannot type silylamides
            o = {-1: (1, "silylamide"), 0: (0, "silyl")}
        if not o:
            return None
        opts.append(o)
    return sorted({sum(c) + 2 for c in itertools.product(*[list(o) for o in opts])})


def fill_H(el, X, want_H, q):
    """Keep existing H; add H to reach geometric prediction; flip ambiguous atoms toward want_H;
    accept only if Lewis-consistent at charge q."""
    nb, D = bonds(el, X)
    pred = predict(el, X, nb, D)
    heavy = [i for i, e in enumerate(el) if e != "H"]
    have = {i: sum(el[j] == "H" for j in nb[i]) for i in heavy}
    tgt = {i: max(pred[i][0], have[i]) for i in heavy}
    tot = sum(tgt.values())
    if want_H is not None and tot != want_H:
        cand = [(i, a) for i in heavy for a in pred[i][1] if (a - tgt[i]) * (want_H - tot) > 0 and a >= have[i]]
        for k in range(1, 5):
            hit = next((c for c in itertools.combinations(cand, k) if len({x[0] for x in c}) == k and
                        tot + sum(a - tgt[i] for i, a in c) == want_H), None)
            if hit:
                for i, a in hit:
                    tgt[i] = a
                break
    new = []
    for i in heavy:
        if tgt[i] > have[i]:
            new += place(el, X, nb, i, tgt[i] - have[i], pred[i][2], [j for j in nb[i] if el[j] == "H"])
    if new:
        el = el + ["H"] * len(new); X = np.vstack([X, np.array(new)])
    return el, X


def normalize_H(el, X):
    nb, D = bonds(el, X)
    for h, e in enumerate(el):
        if e == "H":
            p = [j for j in nb[h] if el[j] != "H"]
            if len(p) == 1:
                v = X[h] - X[p[0]]; X[h] = X[p[0]] + v / np.linalg.norm(v) * XH.get(el[p[0]], 1.0)
    return X


def audit(el, X):
    nb, D = bonds(el, X); iss = []
    for h, e in enumerate(el):
        if e == "H" and len([j for j in nb[h] if el[j] != "H"]) != 1:
            iss.append(f"H{h} not singly bonded")
    for i in range(len(el)):
        n13 = set(nb[i]) | {k for j in nb[i] for k in nb[j]}
        for j in range(i + 1, len(el)):
            if j not in n13 and D[i, j] < 1.6:
                iss.append(f"contact {el[i]}{i}-{el[j]}{j} {D[i, j]:.2f}")
            if j in nb[i] and el[i] != "H" and el[j] != "H" and "Zn" not in (el[i], el[j]) and D[i, j] < 1.15:
                iss.append(f"short bond {el[i]}{i}-{el[j]}{j} {D[i, j]:.2f}")
    return iss


def fix_xubbax(el, X):
    nb, D = bonds(el, X)
    o, c1, c2 = 4, 22, 23
    c0 = [j for j in nb[o] if j != c1][0]
    u = (X[c1] - X[o]) / np.linalg.norm(X[c1] - X[o]); X[c1] = X[o] + 1.43 * u
    a = X[o] - X[c1]; a /= np.linalg.norm(a)
    ref = X[c0] - X[o]; ref -= (ref @ a) * a; ref /= np.linalg.norm(ref)
    th = np.radians(109.5)
    X[c2] = X[c1] + 1.52 * (a * np.cos(th) - ref * np.sin(th))      # anti to C(ring)-O
    return X


report = {}
for ref in REV:
    r = OLD[ref]
    el, X = rd(f"out_rev/molecules/{ref}.xyz")
    steps = ["minor ('?') disorder components removed"] if open(f"out_rev/molecules/{ref}.xyz") else []
    comp, qm = zn_target(r["moiety"])
    if ref == "QADDEF":
        comp, qm = None, 0
    nalk = sum(int(round(v)) for k, v in (comp or {}).items() if k in ALK)
    if ref == "QADDEF":
        nalk = 2                                   # K6Zn3 network: two K+ per Zn
    q = (qm if qm not in (None, "") else 0) - nalk
    def heavy_ok(e2):
        c = cnt(e2)
        return comp is not None and all(c.get(k, 0) == v for k, v in comp.items() if k not in ("H",) + ALK) \
            and all(comp.get(k, 0) == v for k, v in c.items() if k != "H")
    if not heavy_ok(el) and not nalk:
        P = overlaps(el, X)
        hit = None
        for choice in itertools.product(*[(a, b) for a, b in P[:12]]):
            for sub in range(len(choice), 0, -1):
                for cc in itertools.combinations(choice, sub):
                    e2, X2 = drop(el, X, list(cc))
                    if heavy_ok(e2):
                        hit = (e2, X2, cc); break
                if hit: break
            if hit: break
        if hit:
            el, X = hit[0], hit[1]; steps.append(f"{len(hit[2])} overlapping disorder atoms removed")
        else:
            steps.append("UNRESOLVED: heavy-atom formula does not match CSD")
    elif nalk:
        P = [p for p in overlaps(el, X, 1.2)]
        if P:
            best = None
            for choice in itertools.product(*[(a, b) for a, b in P[:10]]):
                e2, X2 = drop(el, X, list(choice))
                if not overlaps(e2, X2, 1.2):
                    best = (e2, X2, choice); break
            if best:
                el, X = best[0], best[1]; steps.append(f"{len(P)} overlapping disorder atoms removed")
    if ref == "XUBBAX":
        X = fix_xubbax(el, X); steps.append("ethoxy group rebuilt (O-C 1.43, C-C 1.52 A)")
    want_H = None
    if comp and nalk == 0:
        want_H = comp.get("H", 0)
    elif ref in ("BUNTOW",):
        want_H = 8
    h0 = el.count("H")
    if want_H is None or h0 < want_H:
        el, X = fill_H(el, X, want_H, q)
        if el.count("H") > h0:
            steps.append(f"{el.count('H') - h0} H added")
    if nalk:
        steps.append(f"{nalk} bonded alkali cation(s) and their solvent removed; complex charge {q:+d}")
    X = normalize_H(el, X)
    qs = lewis_qs(el, X)
    mult = 1
    if ref == "MECFAC":
        mult = 2; steps.append("ligand radical: charge -1 run as doublet")
    c = cnt(el)
    heavy_match = comp is not None and all(c.get(k, 0) == v for k, v in comp.items() if k not in ALK and k != "H") \
        and all(comp.get(k, 0) == v for k, v in c.items() if k != "H")
    H_match = want_H is None or c.get("H", 0) == want_H
    lew = (qs is not None and q in qs) or ref == "MECFAC"
    iss = audit(el, X)
    nb, D = bonds(el, X); zi = el.index("Zn")
    shell = sorted((float(D[zi, j]), el[j]) for j in nb[zi] if D[zi, j] < 2.8)
    ok = (heavy_match or nalk or ref == "QADDEF") and H_match and lew and not [i for i in iss if not i.startswith("contact H")]
    report[ref] = dict(category=r["category"], formula=fstr(c), natoms=len(el), charge=q, mult=mult,
                       csd_complex=fstr(comp) if comp else r["moiety"][:60], heavy_match=bool(heavy_match),
                       H=c.get("H", 0), H_target=want_H, lewis_charges=qs, steps="; ".join(steps),
                       issues="; ".join(iss[:4]), CN=len(shell), donors="".join(f"{e}{n}" for e, n in sorted(cnt([s[1] for s in shell]).items())),
                       zn_L=" ".join(f"{e}{d:.3f}" for d, e in shell), ok=bool(ok))
    with open(f"out_rev/clean/{ref}.xyz", "w") as fh:
        fh.write(f"{len(el)}\n{ref} charge={q} mult={mult} {fstr(c)} cleaned: {'; '.join(steps)}\n")
        for e, p in zip(el, X):
            fh.write(f"{e:2s} {p[0]:12.6f} {p[1]:12.6f} {p[2]:12.6f}\n")
json.dump(report, open("out_rev/clean_report.json", "w"), indent=1)
print("ok", sum(v["ok"] for v in report.values()), "of", len(report))
for k, v in report.items():
    if not v["ok"]:
        print(k, v)
