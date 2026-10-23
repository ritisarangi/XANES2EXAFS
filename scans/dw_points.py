#!/usr/bin/env python3
"""Debye-Waller factor of every Zn-L bond at every validated scan geometry.

Usage (inside the project folder, after combine_slopes.py and export_points.py):
    python3 <repo>/scans/dw_points.py . [tag] [T1 T2 ...]        default temperatures 10 300
Reads redox/slopes_final.csv (per bond: r0, k0, sigma2 at 10 K, nu0, slope, source) and
scan_results/<REF>.xyz (frames written by export_points.py). For each frame and each Zn-L bond:
    dr      = r - r0                                   change in the Zn-L distance (A)
    k       = k0 * exp(slope * dr)                     relaxed force constant (mdyn/A)
    nu      = nu0 * sqrt(k / k0)                       effective Zn-L frequency (cm^-1)
    s2(0)   = s2_0(0) * sqrt(k0 / k)                   zero-point sigma2, s2 ~ 1/(mu * nu) ~ k^-1/2
    s2(T)   = s2(0) * coth(h c nu / 2 kB T)            Einstein temperature factor
with s2_0(0) = s2_0(10 K) / coth(h c nu0 / 2 kB 10 K) from the stage-2 Hessian. Here r0, k0, nu0 and
s2_0 belong to the stage-2 minimum, slope = d ln k / d r of that bond (its own redox, reverse or
epsilon point, or its donor-type slope), and h c / kB = 1.438777 cm K.
Writes scan_results/dw_<tag>.csv with one row per frame and bond. Standard library only, Python 3.6+.
"""
import sys, os, csv, glob, json, math

HCK = 1.438777                      # h c / kB in cm K


def coth(x):
    return 1.0 / math.tanh(x)


def frames(path):
    L = open(path).read().split("\n")
    i = 0
    while i < len(L) and L[i].strip():
        n = int(L[i])
        head = L[i + 1].split()
        atoms = [(l.split()[0], float(l.split()[1]), float(l.split()[2]), float(l.split()[3])) for l in L[i + 2:i + 2 + n]]
        yield head, atoms
        i += 2 + n


def main():
    dft = os.path.abspath(sys.argv[1])
    tag = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].replace(".", "").isdigit() else "all"
    temps = [float(x) for x in sys.argv[2:] if x.replace(".", "").isdigit()] or [10.0, 300.0]
    S = {}
    for r in csv.DictReader(open(os.path.join(dft, "redox", "slopes_final.csv"))):
        S[(r["ref"], r["bond"])] = r
    out = os.path.join(dft, "scan_results", "dw_%s.csv" % tag)
    keys = ["ref", "coord", "branch", "step", "offset", "bond", "r", "dr", "k", "nu"] + ["s2_%gK" % T for T in temps] + ["s2_ratio_10K", "slope", "slope_source"]
    n_rows, refs = 0, 0
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for p in sorted(glob.glob(os.path.join(dft, "scan_results", "*.xyz"))):
            ref = os.path.basename(p)[:-4]
            M = json.load(open(os.path.join(dft, "stage2_b3lyp", ref, ref + ".meta")))
            zn = M["zn_index"]
            bonds = [("Zn-%s%d" % (M["donor_elems"][i], L), L) for i, L in enumerate(M["donors"])]
            if not all((ref, b) in S for b, _ in bonds):
                print("%s: missing slopes, skipped" % ref)
                continue
            refs += 1
            for head, A in frames(p):
                kv = dict(x.split("=", 1) for x in head[3:] if "=" in x)
                for b, L in bonds:
                    s = S[(ref, b)]
                    r0, k0, nu0, sl = float(s["r0"]), float(s["k0"]), float(s["nu0"]), float(s["slope"])
                    s2_0 = float(s["s2_10K_0"]) / coth(HCK * nu0 / (2 * 10.0))
                    r = math.sqrt(sum((A[L][j] - A[zn][j]) ** 2 for j in (1, 2, 3)))
                    dr = r - r0
                    k = k0 * math.exp(sl * dr)
                    nu = nu0 * math.sqrt(k / k0)
                    zp = s2_0 * math.sqrt(k0 / k)
                    row = dict(ref=ref, coord=head[1], branch=head[2], step=kv.get("step", ""), offset=kv.get("offset", ""),
                               bond=b, r=round(r, 4), dr=round(dr, 4), k=round(k, 4), nu=round(nu, 1),
                               slope=sl, slope_source=s["source"])
                    for T in temps:
                        row["s2_%gK" % T] = round(zp * coth(HCK * nu / (2 * T)), 6)
                    row["s2_ratio_10K"] = round(zp * coth(HCK * nu / 20.0) / float(s["s2_10K_0"]), 4)
                    w.writerow(row)
                    n_rows += 1
    print("complexes: %d, rows (frame x bond): %d; wrote %s" % (refs, n_rows, os.path.relpath(out, dft)))


if __name__ == "__main__":
    main()
