"""Shared geometry helpers for the scan workflow. Standard library only, Python 3.6+."""
import math, json, os

# Covalent radii (Angstrom), same table family as the curation step; bond if d < r1 + r2 + TOL.
RAD = {"H": 0.31, "B": 0.84, "C": 0.76, "N": 0.71, "O": 0.66, "F": 0.57, "Si": 1.11, "P": 1.07,
       "S": 1.05, "Cl": 1.02, "Br": 1.20, "Zn": 1.22}
TOL = 0.40


def read_xyz(path):
    L = open(path).read().split("\n")
    n = int(L[0])
    out = []
    for l in L[2:2 + n]:
        s = l.split()
        out.append((s[0], float(s[1]), float(s[2]), float(s[3])))
    return out


def dist(a, b):
    return math.sqrt((a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2 + (a[3] - b[3]) ** 2)


def _sub(a, b):
    return (a[1] - b[1], a[2] - b[2], a[3] - b[3])


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def _cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def angle(a, b, c):
    u, v = _sub(a, b), _sub(c, b)
    x = _dot(u, v) / math.sqrt(_dot(u, u) * _dot(v, v))
    return math.degrees(math.acos(max(-1.0, min(1.0, x))))


def dihedral(a, b, c, d):
    """IUPAC sign convention, degrees in (-180, 180]."""
    b0, b1, b2 = _sub(a, b), _sub(c, b), _sub(d, c)
    n1 = math.sqrt(_dot(b1, b1))
    b1n = (b1[0] / n1, b1[1] / n1, b1[2] / n1)
    v = tuple(b0[i] - _dot(b0, b1n) * b1n[i] for i in range(3))
    w = tuple(b2[i] - _dot(b2, b1n) * b1n[i] for i in range(3))
    x = _dot(v, w)
    y = _dot(_cross(b1n, v), w)
    return math.degrees(math.atan2(y, x))


def bonds(A, skip_zn=True):
    """Covalent bond set (i<j); Zn bonds excluded when skip_zn."""
    E = set()
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if skip_zn and (A[i][0] == "Zn" or A[j][0] == "Zn"):
                continue
            ri, rj = RAD.get(A[i][0], 1.2), RAD.get(A[j][0], 1.2)
            if dist(A[i], A[j]) < ri + rj + TOL:
                E.add((i, j))
    return E


def neighbors(E, n):
    nb = [[] for _ in range(n)]
    for i, j in E:
        nb[i].append(j)
        nb[j].append(i)
    return nb


def components(E, n):
    nb = neighbors(E, n)
    comp = [-1] * n
    c = 0
    for s in range(n):
        if comp[s] >= 0:
            continue
        stack = [s]
        comp[s] = c
        while stack:
            k = stack.pop()
            for m in nb[k]:
                if comp[m] < 0:
                    comp[m] = c
                    stack.append(m)
        c += 1
    return comp


def measure(A, kind, atoms):
    if kind == "B":
        return dist(A[atoms[0]], A[atoms[1]])
    if kind == "A":
        return angle(A[atoms[0]], A[atoms[1]], A[atoms[2]])
    return dihedral(*[A[i] for i in atoms])


def load_meta(dft, ref):
    return json.load(open(os.path.join(dft, "stage2_b3lyp", ref, ref + ".meta")))
