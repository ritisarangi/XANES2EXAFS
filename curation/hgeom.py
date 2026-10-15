"""Geometry-based H count prediction and placement for Zn complexes.

predict(el, X) -> list of (required_H, ambiguity_alternatives) per atom, using
neighbour count (Zn counts as a neighbour), bond lengths and angles.
place(el, X, i, k, hyb) -> positions for k new H on atom i.
"""
import numpy as np

RAD = dict(H=0.23, B=0.83, C=0.68, N=0.68, O=0.68, F=0.64, Si=1.20, P=1.05, S=1.02, Cl=0.99,
           Br=1.21, I=1.40, Se=1.22, Zn=1.45, As=1.21, Te=1.47, Ge=1.17, Sn=1.39)
XH = dict(C=1.09, N=1.01, O=0.97, B=1.19, S=1.34, Si=1.48, P=1.42, Se=1.47)


def bonds(el, X, tol=0.4):
    n = len(el)
    D = np.linalg.norm(X[:, None] - X[None], axis=2)
    nb = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if el[i] == "H" and el[j] == "H":
                continue
            if 0.5 < D[i, j] < RAD.get(el[i], 1.5) + RAD.get(el[j], 1.5) + tol:
                nb[i].append(j); nb[j].append(i)
    return nb, D


def ang(X, a, b, c):
    u = X[a] - X[b]; v = X[c] - X[b]
    return np.degrees(np.arccos(np.clip(u @ v / np.linalg.norm(u) / np.linalg.norm(v), -1, 1)))


def angle_sum(X, i, nbs):
    s = 0
    for p in range(len(nbs)):
        for q in range(p + 1, len(nbs)):
            s += ang(X, nbs[p], i, nbs[q])
    return s


def predict(el, X, nb, D):
    """Return per-atom (default_total_H, alternatives, hybridization) counting ALL H (existing+new)."""
    out = []
    for i, e in enumerate(el):
        heavy = [j for j in nb[i] if el[j] != "H"]
        n = len(heavy)
        zn = any(el[j] == "Zn" for j in heavy)
        hyb, h, alt = None, 0, []
        if e == "C":
            if n >= 4:
                h = 0
            elif n == 3:
                s = angle_sum(X, i, heavy)
                if s >= 345: h, hyb = 0, "sp2"
                else: h, hyb = 1, "sp3"
                if 335 <= s < 352: alt = [1 - h]
            elif n == 2:
                a = ang(X, heavy[0], i, heavy[1]); d = sorted(D[i, heavy])
                if a >= 165: h, hyb = 0, "sp"
                elif d[0] >= 1.46 or (a < 114 and d[0] >= 1.43): h, hyb = 2, "sp3"
                else: h, hyb = 1, "sp2"
                if 1.40 <= d[0] < 1.48 and 112 <= a < 118: alt = [3 - h]
            elif n == 1:
                d = D[i, heavy[0]]
                if d < 1.25: h, hyb = 1, "sp"
                elif d < 1.41: h, hyb = 2, "sp2"
                else: h, hyb = 3, "sp3"
                if 1.38 <= d < 1.45: alt = [5 - h]
        elif e == "N":
            if n >= 4:
                h = 0
            elif n == 3:
                h = 0
                s = angle_sum(X, i, heavy)
                other = [j for j in heavy if el[j] != "Zn"]
                if zn and s < 345 and min(D[i, other]) >= 1.44:
                    h, hyb = 1, "sp3"; alt = [0]          # Zn-NHR2 secondary amine donor
                elif not zn and s < 340: alt = [1]        # possible ammonium NH+
            elif n == 2:
                a = ang(X, heavy[0], i, heavy[1])
                other = [j for j in heavy if el[j] != "Zn"]
                if zn:
                    d = D[i, other[0]] if other else 9
                    if d < 1.20: h, hyb = 0, "sp"
                    elif d < 1.33: h, hyb = 0, "sp2"; alt = [1]
                    elif d >= 1.43: h, hyb = 2, "sp3"; alt = [1]
                    else: h, hyb = 0, "sp2"; alt = [1]
                else:
                    d = sorted(D[i, heavy])
                    if a >= 165: h = 0
                    elif d[0] >= 1.43: h, hyb = 1, "sp3"
                    else: h, hyb = 0, "sp2"; alt = [1]
            elif n == 1:
                d = D[i, heavy[0]]
                if zn: h, hyb = 3, "sp3"
                elif d < 1.20: h = 0
                elif d < 1.31: h, hyb = 1, "sp2"; alt = [0]
                elif d < 1.41: h, hyb = 2, "sp2"
                else: h, hyb = 2, "sp3"
        elif e == "O":
            if n >= 2:
                h = 0
                if zn and n == 2: alt = [1]                 # alcohol vs alkoxide donor
            elif n == 1:
                j = heavy[0]; d = D[i, j]
                if el[j] == "Zn": h, hyb = 2, "sp3"; alt = [1]
                elif el[j] == "C": h, hyb = (0, None) if d < 1.30 else (1, "sp3")
                elif el[j] in ("S", "P"): h, hyb = (0, None) if d < 1.53 else (1, "sp3")
                elif el[j] == "N": h, hyb = (0, None) if d < 1.33 else (1, "sp3")
                else: h = 0
                if el[j] == "C" and 1.27 <= d < 1.34: alt = [1 - h]
            else:
                h, hyb = 2, "sp3"
        elif e == "S":
            if n == 1 and not zn and el[heavy[0]] == "C":
                d = D[i, heavy[0]]
                h, hyb = (0, None) if d < 1.72 else (1, "sp3")
            else:
                h = 0
        elif e == "B":
            h = max(0, 4 - n); hyb = "sp3"
        elif e == "Si":
            h = max(0, 4 - n); hyb = "sp3"
        out.append([h, alt, hyb])
    return out


def _perp(u):
    a = np.array([1.0, 0, 0]) if abs(u[0]) < 0.9 else np.array([0, 1.0, 0])
    v = np.cross(u, a); return v / np.linalg.norm(v)


def place(el, X, nb, i, k, hyb, existing_H):
    """Return k new H positions on atom i. Neighbours (incl. Zn and existing H) define directions."""
    L = XH.get(el[i], 1.0)
    nbs = nb[i]
    U = [(X[j] - X[i]) / np.linalg.norm(X[j] - X[i]) for j in nbs]
    tot = len(nbs) + k
    if not U:
        dirs = [np.array([0, 0, 1.0]), np.array([0.94, 0, -0.33])][:k]
        return [X[i] + L * d for d in dirs]
    if tot == 4 or hyb == "sp3":
        if len(U) == 3:
            d = -(U[0] + U[1] + U[2]); d /= np.linalg.norm(d); dirs = [d]
        elif len(U) == 2:
            b = -(U[0] + U[1]); b /= np.linalg.norm(b)
            p = np.cross(U[0], U[1]); p /= np.linalg.norm(p)
            t = np.radians(54.75)
            dirs = [b * np.cos(t) + p * np.sin(t), b * np.cos(t) - p * np.sin(t)]
            if k == 1:
                dirs = [b]
        else:
            u = U[0]
            j = nbs[0]
            ref = [m for m in nb[j] if m != i]
            v = (X[ref[0]] - X[j]) if ref else _perp(u)
            v = v - (v @ u) * u
            v = v / np.linalg.norm(v) if np.linalg.norm(v) > 1e-6 else _perp(u)
            w = np.cross(u, v)
            th = np.radians(109.47)
            dirs = [u * np.cos(th) + (v * np.cos(f) + w * np.sin(f)) * np.sin(th)
                    for f in np.radians([180, 300, 60])]
    elif hyb == "sp" or tot == 2:
        dirs = [-U[0]]
    else:  # sp2
        if len(U) == 2:
            d = -(U[0] + U[1]); d /= np.linalg.norm(d); dirs = [d]
        else:
            u = U[0]; j = nbs[0]
            ref = [m for m in nb[j] if m != i]
            v = (X[ref[0]] - X[j]) if ref else _perp(u)
            v = v - (v @ u) * u
            v = v / np.linalg.norm(v) if np.linalg.norm(v) > 1e-6 else _perp(u)
            th = np.radians(120)
            dirs = [u * np.cos(th) + v * np.sin(th), u * np.cos(th) - v * np.sin(th)]
    # drop directions already occupied by existing H
    free = []
    for d in dirs:
        if all(np.linalg.norm(X[i] + L * d - X[h]) > 0.9 for h in existing_H):
            free.append(d)
    return [X[i] + L * d for d in free[:k]]
