#!/usr/bin/env python3
"""Build relaxed-scan ORCA inputs around the stage-2 B3LYP minimum of each complex.

Usage (run inside the project folder that holds stage2_b3lyp/):
    python3 <repo>/scans/make_scans.py . lists/pilot.txt [jobs_name]

For each complex it scans, one coordinate at a time with everything else relaxed:
  bonds   Zn-L, every first-shell donor      -0.06 .. +0.20 A in 0.02 A steps
  angles  L-Zn-L, every donor pair            -15 .. +15 deg in 1.5 deg steps
  twist   donor dihedral L1-L2-L3-L4 (CN 4)   -10 .. +10 deg in 1 deg steps
  tilt    Zn-L-C-X, one per donor             -10 .. +10 deg in 1 deg steps
Each coordinate runs as two branches that both start at the minimum (neg and pos), so a
failure at an extreme loses only the points beyond it.

Writes scans/<REF>/<COORD>_<branch>/scan.inp, scans/<REF>/coords.json, and the job list
scans/jobs_<name>.txt (one job folder per line, relative to the project folder).
Standard library only, Python 3.6+.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zncore as Z

BOND = (-0.06, 0.20, 0.02)
ANGLE = (-15.0, 15.0, 1.5)
DIHED = (-10.0, 10.0, 1.0)
LINEAR = 165.0          # skip a dihedral if any angle in it exceeds this (nitrile, NCS)
ANGLE_MAX = 178.0       # skip an angle branch that would pass this

KEYS = "! B3LYP D3BJ def2-SVP def2/J RIJCOSX CPCM(water) TightOpt DefGrid3 TightSCF"


def branches(v0, lo, hi, step):
    """Return [(name, start, end, npoints)] for the negative and positive branches."""
    out = []
    for name, lim in (("neg", lo), ("pos", hi)):
        n = int(round(abs(lim) / step)) + 1
        if n > 1:
            out.append((name, v0, v0 + lim, n))
    return out


def pick_tilt(A, nb, zn, L):
    """Zn-L-C-X dihedral. C: a heavy neighbour of L (carbon first). X: a neighbour of C, heavy atoms
    preferred so the constraint rotates the ligand rather than one H; values within 10 deg of 180
    are avoided because the +-10 deg scan would cross the -180/180 wrap."""
    heavy = [c for c in nb[L] if A[c][0] != "H"]
    heavy.sort(key=lambda c: (A[c][0] != "C", c))
    for C in heavy:
        if Z.angle(A[zn], A[L], A[C]) > LINEAR:
            continue
        cand = []
        for X in nb[C]:
            if X == L or Z.angle(A[L], A[C], A[X]) > LINEAR:
                continue
            d = Z.dihedral(A[zn], A[L], A[C], A[X])
            if abs(d) > 170.0:
                continue
            cand.append((A[X][0] == "H", abs(d), X, d))
        if cand:
            cand.sort()
            return (zn, L, C, cand[0][2]), cand[0][3]
    return None, None


def pick_twist(A, E, donors):
    """Donor dihedral L1-L2-L3-L4 with chelating pairs adjacent (L1,L2 one ligand, L3,L4 the other)."""
    if len(donors) != 4:
        return None, None
    comp = Z.components(E, len(A))
    d = sorted(donors, key=lambda i: (comp[i], i))
    v = Z.dihedral(*[A[i] for i in d])
    if abs(v) > 170.0:
        return None, None
    return tuple(d), v


def fmt_val(kind, v):
    return ("%.4f" if kind == "B" else "%.3f") % v


def main():
    dft = os.path.abspath(sys.argv[1])
    lst = sys.argv[2]
    tag = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(os.path.basename(lst))[0]
    refs = [l.strip() for l in open(os.path.join(dft, lst)) if l.strip()]
    jobs, summary = [], []
    for ref in refs:
        meta = Z.load_meta(dft, ref)
        xyz = os.path.join(dft, "stage2_b3lyp", ref, ref + ".xyz")
        if not os.path.exists(xyz):
            print(ref, "skipped: no stage-2 geometry")
            continue
        A = Z.read_xyz(xyz)
        if len(A) != meta["natoms"]:
            print(ref, "skipped: atom count differs from meta")
            continue
        zn, donors = meta["zn_index"], meta["donors"]
        E = Z.bonds(A)
        nb = Z.neighbors(E, len(A))
        lab = lambda i: "%s%d" % (A[i][0], i)
        coords = []
        for L in donors:
            coords.append(("B", (zn, L), "bond_Zn-" + lab(L), BOND))
        for a in range(len(donors)):
            for b in range(a + 1, len(donors)):
                i, j = donors[a], donors[b]
                coords.append(("A", (i, zn, j), "angle_%s-Zn-%s" % (lab(i), lab(j)), ANGLE))
        tw, _ = pick_twist(A, E, donors)
        if tw:
            coords.append(("D", tw, "twist_" + "-".join(lab(i) for i in tw), DIHED))
        for L in donors:
            t, _ = pick_tilt(A, nb, zn, L)
            if t:
                coords.append(("D", t, "tilt_Zn-" + "-".join(lab(i) for i in t[1:]), DIHED))
        tz = set(donors) | {zn}
        geo = "\n".join("  %-2s %12.6f %12.6f %12.6f%s" % (a[0], a[1], a[2], a[3],
                        ' newgto "def2-TZVP" end' if i in tz else "") for i, a in enumerate(A))
        uks = " UKS" if meta["mult"] > 1 else ""
        recs = []
        for kind, atoms, name, (lo, hi, step) in coords:
            v0 = Z.measure(A, kind, atoms)
            for br, start, end, n in branches(v0, lo, hi, step):
                if kind == "A" and max(start, end) > ANGLE_MAX:
                    print(ref, name, br, "skipped: angle would pass %.0f deg" % ANGLE_MAX)
                    continue
                d = os.path.join("scans", ref, "%s_%s" % (name, br))
                os.makedirs(os.path.join(dft, d), exist_ok=True)
                inp = ("# %s %s %s branch: %s %s -> %s in %d points; everything else relaxed\n"
                       "%s%s\n%%pal nprocs 16 end\n%%maxcore 3000\n%%scf MaxIter 500 end\n"
                       "%%geom\n  MaxIter 100\n  Scan\n    %s %s = %s, %s, %d\n  end\nend\n"
                       "* xyz %d %d\n%s\n*\n") % (
                    ref, name, br, kind, fmt_val(kind, start), fmt_val(kind, end), n,
                    KEYS, uks, kind, " ".join(str(i) for i in atoms),
                    fmt_val(kind, start), fmt_val(kind, end), n,
                    meta["charge"], meta["mult"], geo)
                open(os.path.join(dft, d, "scan.inp"), "w").write(inp)
                jobs.append(d)
                recs.append(dict(name=name, kind=kind, atoms=list(atoms), branch=br, v0=v0,
                                 start=start, end=end, npoints=n, dir=d))
        json.dump(dict(ref=ref, zn=zn, donors=donors, coords=recs), open(os.path.join(dft, "scans", ref, "coords.json"), "w"), indent=1)
        npts = sum(r["npoints"] - 1 for r in recs) + 1
        summary.append((ref, len(donors), len(recs), npts))
    jl = os.path.join(dft, "scans", "jobs_%s.txt" % tag)
    open(jl, "w").write("\n".join(jobs) + "\n")
    print("%-8s %3s %5s %7s" % ("ref", "CN", "jobs", "points"))
    for s in summary:
        print("%-8s %3d %5d %7d" % s)
    print("total jobs %d, points %d -> %s" % (len(jobs), sum(s[3] for s in summary), os.path.relpath(jl, dft)))


if __name__ == "__main__":
    main()
