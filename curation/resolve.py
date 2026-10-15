"""Resolve disorder in the review set and report status per complex.

Input molecules come from parse_cifs with minor ('?') components dropped. Remaining
symmetry-generated overlaps (pairs closer than 1.2 A) are resolved by removing one
partner of each pair (with its H), choosing the combination whose formula matches the
CSD moiety and which has a closed-shell Lewis structure.
"""
import json, re, itertools, sys, os
import numpy as np
from hgeom import bonds
from lewis_check import rd, fragments, frag_charges
sys.path.insert(0, ".")
from moiety import parse_moiety  # noqa

RAW = {r["refcode"]: r for r in json.load(open("out_rev/zn_inventory_raw.json"))}
OLD = {r["refcode"]: r for r in json.load(open("out/zn_unique.json"))}
os.makedirs("out_rev/resolved", exist_ok=True)


def counts(el):
    c = {}
    for e in el:
        c[e] = c.get(e, 0) + 1
    return c


def target(moiety):
    best = []
    for mult, comp, ch in parse_moiety(moiety):
        if abs(comp.get("Zn", 0) - 1) < 0.01:
            best.append(({k: int(round(v)) for k, v in comp.items()}, ch))
    return best


def lewis(el, X):
    nb, D = bonds(el, X)
    frs = fragments(el, nb)
    opts = [frag_charges(el, X, nb, f) for f in frs]
    if any(not o for o in opts):
        return None
    qs = sorted({sum(c) + 2 for c in itertools.product(*[list(o) for o in opts])})
    return qs


def close_pairs(el, X, cut=1.2):
    D = np.linalg.norm(X[:, None] - X[None], axis=2)
    P = []
    for i in range(len(el)):
        for j in range(i + 1, len(el)):
            if el[i] != "H" and el[j] != "H" and D[i, j] < cut and el[i] == el[j]:
                P.append((i, j))
    return P


def drop(el, X, rm):
    nb, D = bonds(el, X)
    gone = set(rm)
    for i in rm:
        gone |= {j for j in nb[i] if el[j] == "H"}
    keep = [k for k in range(len(el)) if k not in gone]
    return [el[k] for k in keep], X[keep]


if __name__ == "__main__":
    out = {}
    for ref, r in RAW.items():
        el, X = rd(f"out_rev/molecules/{ref}.xyz")
        tg = target(OLD[ref]["moiety"])
        P = close_pairs(el, X)
        cands = [(el, X, "as parsed")]
        if P:
            for choice in itertools.product(*[(a, b) for a, b in P[:8]]):
                e2, X2 = drop(el, X, list(choice))
                if not close_pairs(e2, X2):
                    cands.append((e2, X2, f"removed overlap partners {sorted(choice)}"))
        best = None
        for e2, X2, note in cands:
            c = counts(e2)
            fm = [q for comp, q in tg if comp == c]
            if close_pairs(e2, X2):
                continue
            qs = lewis(e2, X2)
            score = (0 if fm else 1, 0 if qs else 1)
            if best is None or score < best[0]:
                best = (score, e2, X2, note, fm, qs)
            if score == (0, 0):
                break
        score, e2, X2, note, fm, qs = best
        nb, D = bonds(e2, X2)
        zi = e2.index("Zn")
        shell = sorted((round(float(D[zi, j]), 3), e2[j]) for j in nb[zi])
        q_csd = OLD[ref]["charge_csd"]
        out[ref] = dict(formula=" ".join(f"{k}{v}" for k, v in sorted(counts(e2).items())), natoms=len(e2),
                        formula_match=bool(fm), lewis_charges=qs, q_csd=q_csd, note=note,
                        CN=len(shell), shell=" ".join(f"{e}{d}" for d, e in shell),
                        moiety=[f"{' '.join(f'{k}{v}' for k, v in sorted(c.items()))} q={q}" for c, q in tg])
        with open(f"out_rev/resolved/{ref}.xyz", "w") as fh:
            fh.write(f"{len(e2)}\n{ref} disorder resolved: {note}\n")
            for e, p in zip(e2, X2):
                fh.write(f"{e:2s} {p[0]:12.6f} {p[1]:12.6f} {p[2]:12.6f}\n")
    json.dump(out, open("out_rev/resolve_report.json", "w"), indent=1)
    for k, v in sorted(out.items(), key=lambda kv: (kv[1]["formula_match"], bool(kv[1]["lewis_charges"]))):
        print(k, "match" if v["formula_match"] else "MISMATCH", "lewis", v["lewis_charges"], "csd", v["q_csd"],
              "CN", v["CN"], "|", v["formula"], "| moiety", v["moiety"][:2], "|", v["note"][:50])
