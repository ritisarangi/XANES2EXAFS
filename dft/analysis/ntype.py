#!/usr/bin/env python3
"""Classify each N donor of a Zn complex by its chemical type, from connectivity.

    from ntype import classify;  classify(atoms, n_index, zn_index) -> type string
    python3 ntype.py <xyz> <meta>          prints the type of every N donor

Types: imidazole (5-ring N whose ring neighbours are both C, another N in the ring: imidazole N3,
benzimidazole), pyrazole (5-ring N bonded to a ring N: pyrazole, triazole, tetrazole, thiadiazole),
thiazole (5-ring N with S or O as the other heteroatom), pyrrolide (5-ring N, all other ring atoms C:
dipyrrins, porphyrins), pyridine (N in a 6-membered ring), imine (C=N-C outside a ring, Schiff base),
hydrazone (C=N-N outside a ring, incl. thiosemicarbazones), nitrile,
amido (deprotonated N on a C=O, S=O or in a sulfonamide/carboxamide), amine (sp3 N with H or
three single bonds), other. Standard library only, Python 3.6+.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scans"))
import zncore as Z  # noqa: E402


def _graph(A):
    nb = {i: set() for i in range(len(A))}
    for i, j in Z.bonds(A):
        nb[i].add(j)
        nb[j].add(i)
    return nb


def _rings(nb, start, maxlen=6):
    """Sizes of simple rings through `start` up to maxlen, with their atoms."""
    out, stack = [], [(start, [start])]
    while stack:
        v, path = stack.pop()
        for w in nb[v]:
            if w == start and len(path) >= 3:
                out.append(list(path))
            elif w not in path and len(path) < maxlen:
                stack.append((w, path + [w]))
    return out


def classify(A, n, zn):
    nb = _graph(A)
    el = [a[0] for a in A]
    heavy = [j for j in nb[n] if el[j] != "H" and j != zn]
    nH = sum(1 for j in nb[n] if el[j] == "H")
    rings = _rings(nb, n)
    r5 = [r for r in rings if len(r) == 5]
    r6 = [r for r in rings if len(r) == 6]
    hetero5 = [sorted(el[k] for k in r if k != n and el[k] != "C") for r in r5]
    if r5 and nH == 0 and len(heavy) == 2:
        if any("N" in h for h in hetero5):
            # imidazole N3 (both ring neighbours C) vs pyrazole/triazole/tetrazole N (an N neighbour)
            return "pyrazole" if any(el[j] == "N" for j in heavy) else "imidazole"
        if any(h for h in hetero5):
            return "thiazole"              # thiazole / oxazole N
        return "pyrrolide"
    if r6 and nH == 0 and len(heavy) == 2:
        return "pyridine"
    if nH == 0 and len(heavy) == 2:
        for c in heavy:
            if el[c] == "Si":
                return "amido"
            if el[c] in ("C", "S") and any(el[o] == "O" and Z.dist(A[c], A[o]) < (1.30 if el[c] == "C" else 1.50) for o in nb[c]):
                return "amido"
        if any(el[c] == "C" and Z.dist(A[n], A[c]) < 1.345 for c in heavy):
            return "hydrazone" if any(el[j] == "N" for j in heavy) else "imine"
        return "other"
    if nH == 0 and len(heavy) == 1 and el[heavy[0]] == "C" and Z.dist(A[n], A[heavy[0]]) < 1.20:
        return "nitrile"
    if nH >= 1 or len(heavy) == 3:
        return "amine"
    return "other"


if __name__ == "__main__":
    A = Z.read_xyz(sys.argv[1])
    M = json.load(open(sys.argv[2]))
    for i, d in enumerate(M["donors"]):
        if M["donor_elems"][i] == "N":
            print(d, classify(A, d, M["zn_index"]))
