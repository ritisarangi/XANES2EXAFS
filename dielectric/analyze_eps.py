#!/usr/bin/env python3
"""Compare Zn-L bonds across CPCM dielectric constants and against the relaxed scans.

Usage (inside the project folder, after the dielectric runs):
    python3 <repo>/dielectric/analyze_eps.py . lists/pilot.txt [4 2]
For every Zn-L bond and every dielectric (80 = stage 2, plus each eps<E> run) it reports
r, sigma2 at 10 K, nu_eff and the relaxed force constant k_hess from the Hessian,
    k_hess = [ sum_k q_k^2 / (4 pi^2 c^2 nu_k^2) ]^-1,   4 pi^2 c^2 = 5.8916e-7 mdyn A^-1 amu^-1 cm^2,
then two slopes of ln k against r:
    slope_eps   least-squares slope of ln k_hess against r over the dielectric points
    slope_scan  slope of ln k(r) from the relaxed bond scan between -0.02 and +0.04 A,
                k(r) from quadratic fits to the scan energy in 5-point windows
and the slope implied by the set-wide line nu_eff = a - b r:  2 b / nu_eff(r0).
Also checks that ORCA used the requested epsilon and lists imaginary modes.
Writes dielectric/eps_compare_<tag>.csv. Standard library only, Python 3.6+.
"""
import sys, os, re, json, math, csv
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dft", "analysis"))
sys.path.insert(0, os.path.join(HERE, "..", "scans"))
from report_extract import read_xyz, read_hess, dist, C  # noqa: E402
import validate as V  # noqa: E402

FAC = 5.8916e-7                     # 4 pi^2 c^2 in mdyn A^-1 amu^-1 cm^2
HA2MDYN = 2625.4996 / 602.214       # hartree/A^2 -> mdyn/A
HC_K = 1.438777
LINE = {"S": (1825.0, 653.0), "N": (2545.0, 985.0)}


def bond_props(masses, freqs, modes, zn, L, R):
    rv = [R[L][i] - R[zn][i] for i in (1, 2, 3)]
    nr = math.sqrt(sum(x * x for x in rv))
    rh = [x / nr for x in rv]
    s0 = s10 = comp = 0.0
    for k, nu in enumerate(freqs):
        if nu <= 1.0:
            continue
        mw = [modes[k][3 * a + j] * math.sqrt(masses[a]) for a in range(len(masses)) for j in range(3)]
        nrm = math.sqrt(sum(x * x for x in mw))
        if nrm == 0:
            continue
        q = sum((mw[3 * L + j] / math.sqrt(masses[L]) - mw[3 * zn + j] / math.sqrt(masses[zn])) * rh[j] for j in range(3)) / nrm
        s0 += C / nu * q * q
        s10 += C / nu * q * q / math.tanh(HC_K * nu / 20.0)
        comp += q * q / (FAC * nu * nu)
    mu = masses[zn] * masses[L] / (masses[zn] + masses[L])
    return nr, s10, C / (mu * s0), 1.0 / comp


def slope(x, y):
    n = len(x)
    if n < 2:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / sxx if sxx > 0 else None


def quad_k(pts):
    """k (hartree/A^2) from E = c0 + c1 x + c2 x^2 by least squares; k = 2 c2."""
    n = len(pts)
    S = [sum(x ** p for x, _ in pts) for p in range(5)]
    T = [sum(e * x ** p for x, e in pts) for p in range(3)]
    A = [[S[0], S[1], S[2]], [S[1], S[2], S[3]], [S[2], S[3], S[4]]]
    # Cramer's rule
    def det(M):
        return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    D = det(A)
    if n < 3 or abs(D) < 1e-30:
        return None
    A2 = [[A[i][0], A[i][1], T[i]] for i in range(3)]
    return 2.0 * det(A2) / D


def scan_slope(dft, ref, zn, L, n):
    cj = os.path.join(dft, "scans", ref, "coords.json")
    if not os.path.exists(cj):
        return None
    Cs = json.load(open(cj))
    E = {}
    for c in Cs["coords"]:
        if c["kind"] != "B" or sorted(c["atoms"]) != sorted([zn, L]):
            continue
        p = os.path.join(dft, c["dir"], "scan.out")
        if not os.path.exists(p):
            continue
        st = V.parse_steps(open(p, errors="ignore").read(), n)
        for k, (conv, e, A) in enumerate(st):
            if not conv or e is None:
                break
            off = round((c["start"] + (c["end"] - c["start"]) * k / (c["npoints"] - 1)) - c["v0"], 3)
            E[off] = e
    if 0.0 not in E:
        return None
    offs = sorted(E)
    xs, ys = [], []
    for o in offs:
        win = [(x, E[x]) for x in offs if abs(x - o) <= 0.0401]
        if len(win) < 5 or not (-0.0201 <= o <= 0.0401):
            continue
        k = quad_k([(x - o, e) for x, e in win])
        if k and k > 0:
            xs.append(o)
            ys.append(math.log(k * HA2MDYN))
    return slope(xs, ys) if len(xs) >= 3 else None


def run_info(out):
    t = open(out, errors="ignore").read() if os.path.exists(out) else ""
    ok = "ORCA TERMINATED NORMALLY" in t and "VIBRATIONAL FREQUENCIES" in t
    m = re.findall(r"Epsilon\s+\.\.\.\s+([\d.]+)", t)
    return ok, (float(m[-1]) if m else None)


def main():
    dft = os.path.abspath(sys.argv[1])
    lst = sys.argv[2]
    eps_list = sys.argv[3:] or ["4", "2"]
    tag = os.path.splitext(os.path.basename(lst))[0]
    refs = [l.strip() for l in open(os.path.join(dft, lst)) if l.strip() and not l.startswith("#")]
    rows, notes = [], []
    for ref in refs:
        meta = json.load(open(os.path.join(dft, "stage2_b3lyp", ref, ref + ".meta")))
        zn, donors = meta["zn_index"], meta["donors"]
        runs = [("80", os.path.join(dft, "stage2_b3lyp", ref))] + [(e, os.path.join(dft, "dielectric", "eps%g" % float(e), ref)) for e in eps_list]
        res = {}
        for e, d in runs:
            ok, eps_used = run_info(os.path.join(d, ref + ".out"))
            if not ok:
                notes.append("%s eps %s: not finished" % (ref, e))
                continue
            if e != "80" and (eps_used is None or abs(eps_used - float(e)) > 0.01):
                notes.append("%s eps %s: ORCA printed epsilon %s, result not used" % (ref, e, eps_used))
                continue
            masses, freqs, modes = read_hess(os.path.join(d, ref + ".hess"))
            imag = [round(f, 1) for f in freqs if f < -1.0]
            if imag:
                notes.append("%s eps %s: imaginary %s" % (ref, e, imag))
            R = read_xyz(os.path.join(d, ref + ".xyz"))
            res[e] = {L: bond_props(masses, freqs, modes, zn, L, R) for L in donors}
        if "80" not in res:
            continue
        for i, L in enumerate(donors):
            el = meta["donor_elems"][i]
            pts = [(e, res[e][L]) for e, _ in runs if e in res]
            r0, _, nu0, _ = res["80"][L]
            row = {"ref": ref, "bond": "Zn-%s%d" % (el, L), "el": el}
            for e, (r, s10, nu, k) in pts:
                row.update({"r_%s" % e: round(r, 4), "k_%s" % e: round(k, 4), "nu_%s" % e: round(nu, 1), "s2_10K_%s" % e: round(s10, 6)})
            row["dr_max"] = round(max(p[1][0] for p in pts) - min(p[1][0] for p in pts), 4)
            se = slope([p[1][0] for p in pts], [math.log(p[1][3]) for p in pts]) if len(pts) >= 2 else None
            row["slope_eps"] = round(se, 2) if se is not None else ""
            ss = scan_slope(dft, ref, zn, L, meta["natoms"])
            row["slope_scan"] = round(ss, 2) if ss is not None else ""
            row["slope_line"] = round(-2 * LINE[el][1] / nu0, 2) if el in LINE else ""
            rows.append(row)
    if not rows:
        print("nothing to compare yet")
    else:
        keys = []
        for r in rows:
            keys += [k for k in r if k not in keys]
        fn = os.path.join(dft, "dielectric", "eps_compare_%s.csv" % tag)
        with open(fn, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys, restval="")
            w.writeheader()
            w.writerows(rows)
        print("%-7s %-9s %8s %8s %9s %9s %9s" % ("ref", "bond", "dr_max", "dk/k %", "slope_eps", "slope_scn", "slope_lin"))
        for r in rows:
            ks = [r[k] for k in r if k.startswith("k_")]
            dk = 100 * (max(ks) - min(ks)) / r["k_80"] if ks else 0
            print("%-7s %-9s %8.4f %8.1f %9s %9s %9s" % (r["ref"], r["bond"], r["dr_max"], dk, r["slope_eps"], r["slope_scan"], r["slope_line"]))
        print("\nslopes are d ln k / d r in 1/A; wrote", os.path.relpath(fn, dft))
    if notes:
        print("\nnotes:\n  " + "\n  ".join(notes))


if __name__ == "__main__":
    main()
