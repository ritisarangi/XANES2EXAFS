#!/usr/bin/env python3
"""One force-constant-distance slope for every Zn-L bond, with its source.

Usage (inside the project folder, after analyze_redox.py and analyze_eps.py):
    python3 <repo>/redox/combine_slopes.py .
Reads
    redox/redox_compare_all.csv          first redox run (RKS reference vs UKS doublet)
    redox/redox_compare_reverse_*.csv    reverse runs (UKS doublet)
    dielectric/eps_compare_*.csv         epsilon runs (RKS vs RKS, same charge)
and the stage-2 geometry of each complex (stage2_b3lyp/<REF>/<REF>.xyz) to type the donors.

A point (dr, dln k) for a bond is clean when
    0.01 <= |dr| <= 0.15 A, donor within 2.8 A of Zn ('use' status for redox runs),
    the donor stays closed-shell (|Mulliken spin| < 0.05; epsilon runs keep the charge and are RKS),
    k and r move in opposite directions,
    and the run does not rearrange the complex (in that run, more than half the usable bonds
    have k and r moving in the same direction; all bonds of such a complex are excluded).
Each bond keeps its clean point with the largest |dr| (least noise). The bond's slope is
    own point           slope = dln k / dr from that point
    donor-type slope    least-squares fit through the origin over all bonds of that donor type
                        (types with >= 8 bonds), for bonds without a clean point
    element slope       same fit over all Zn-N or all Zn-S bonds, for thin types
Writes redox/slopes_final.csv (one row per bond) and prints coverage, the donor-type table, the
RKS/UKS check (bonds with both a clean redox and a clean epsilon point) and a leave-one-out test
of the donor-type slopes. Standard library only, Python 3.6+.
"""
import sys, os, csv, glob, json, math
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dft", "analysis"))
sys.path.insert(0, os.path.join(HERE, "..", "scans"))
import zncore as Z  # noqa: E402
from ntype import classify  # noqa: E402

LO, HI, SPIN, MIN_TYPE = 0.01, 0.15, 0.05, 8


def dist(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in (1, 2, 3)))


def stype(A, nb, s):
    ns = [j for j in nb[s] if A[j][0] != "Zn"]
    els = [A[j][0] for j in ns]
    if len(ns) == 2 and all(e == "C" for e in els):
        return "thioether"
    if len(ns) != 1 or els[0] != "C":
        return "S other"
    c = ns[0]
    cn = [j for j in nb[c] if j != s]
    if any(A[j][0] == "S" and j != s and len([k for k in nb[j] if A[k][0] != "Zn"]) == 1 for j in cn):
        return "dithiocarbamate/carboxylate"
    if dist(A[s], A[c]) < 1.72 and len(cn) == 2 and any(A[j][0] == "N" for j in cn):
        return "thione (C=S)"
    for j in cn:
        if A[j][0] == "C" and dist(A[c], A[j]) < 1.40 and any(A[k][0] == "S" and k != s for k in nb[j]):
            return "dithiolene"
    return "alkyl thiolate" if len(cn) == 3 else "aryl/vinyl thiolate"


def donor_types(dft, ref, donors, zn):
    for p in (os.path.join(dft, "stage2_b3lyp", ref, ref + ".xyz"),
              os.path.join(HERE, "..", "structures", "dft_ready_xyz", ref + ".xyz")):
        if os.path.exists(p):
            A = Z.read_xyz(p)
            break
    else:
        return {}
    nb = {i: set() for i in range(len(A))}
    for i, j in Z.bonds(A):
        nb[i].add(j)
        nb[j].add(i)
    return {L: (classify(A, L, zn) if A[L][0] == "N" else stype(A, nb, L)) for L in donors}


def fit0(pts):
    sxx = sum(x * x for x, _ in pts)
    s = sum(x * y for x, y in pts) / sxx
    ss = sum((y - s * x) ** 2 for x, y in pts)
    syy = sum(y * y for _, y in pts)
    se = math.sqrt(ss / max(len(pts) - 1, 1) / sxx)
    return s, se, (1 - ss / syy) if syy > 0 else float("nan")


def median(v):
    v = sorted(v)
    n = len(v)
    return (v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])) if n else float("nan")


def main():
    dft = os.path.abspath(sys.argv[1])
    pts = defaultdict(list)          # (ref, bond) -> [point dicts]
    base = {}                        # (ref, bond) -> reference values
    # redox runs
    files = [("first", os.path.join(dft, "redox", "redox_compare_all.csv"))]
    files += [("reverse", p) for p in sorted(glob.glob(os.path.join(dft, "redox", "redox_compare_reverse_*.csv")))]
    for src, p in files:
        for r in csv.DictReader(open(p)):
            k = (r["ref"], r["bond"])
            if src == "first":
                base[k] = dict(el=r["el"], r0=float(r["r_ref"]), k0=float(r["k_ref"]), s2=float(r["s2_10K_ref"]),
                               line=r["slope_line"])
            dr = float(r["dr"])
            if float(r["k_redox"]) <= 0 or float(r["k_ref"]) <= 0:
                continue
            pts[k].append(dict(src=src, dr=dr, y=math.log(float(r["k_redox"]) / float(r["k_ref"])),
                               spin=abs(float(r["spin_L"])), ok=r["status"] == "use"))
    # epsilon runs
    for p in sorted(glob.glob(os.path.join(dft, "dielectric", "eps_compare_*.csv"))):
        for r in csv.DictReader(open(p)):
            k = (r["ref"], r["bond"])
            for e in ("1", "2", "4"):
                if r.get("r_" + e) and r.get("k_" + e) and r.get("r_80"):
                    dr = float(r["r_" + e]) - float(r["r_80"])
                    ke, k0 = float(r["k_" + e]), float(r["k_80"])
                    if ke > 0 and k0 > 0 and not any(q["src"] == "eps" + e for q in pts[k]):
                        pts[k].append(dict(src="eps" + e, dr=dr, y=math.log(ke / k0), spin=0.0,
                                           ok=LO <= abs(dr) <= HI))
    # rearranged runs: most usable bonds of a complex move the wrong way in that run
    by_run = defaultdict(list)
    for (ref, bond), P in pts.items():
        for q in P:
            if q["ok"]:
                by_run[(ref, q["src"])].append(q["dr"] * q["y"] > 0)
    rearranged = sorted({ref for (ref, src), v in by_run.items() if len(v) >= 2 and sum(v) / len(v) > 0.5})
    # donor types
    meta_cache, types = {}, {}
    for ref in sorted({k[0] for k in base}):
        M = json.load(open(os.path.join(dft, "stage2_b3lyp", ref, ref + ".meta")))
        meta_cache[ref] = M
        for L, g in donor_types(dft, ref, M["donors"], M["zn_index"]).items():
            types[(ref, "Zn-%s%d" % (M["donor_elems"][M["donors"].index(L)], L))] = g
    # one clean point per bond
    own = {}
    for k, P in pts.items():
        if k[0] in rearranged or k not in base:
            continue
        clean = [q for q in P if q["ok"] and q["spin"] < SPIN and q["dr"] * q["y"] < 0]
        if clean:
            own[k] = max(clean, key=lambda q: abs(q["dr"]))
    # type and element fits
    gp = defaultdict(list)
    for k, q in own.items():
        gp[(base[k]["el"], types.get(k, "unknown"))].append((q["dr"], q["y"]))
    el_fit = {el: fit0([p for (e, g), v in gp.items() if e == el for p in v]) for el in ("N", "S")}
    type_fit = {key: fit0(v) for key, v in gp.items() if len(v) >= MIN_TYPE}
    # rows
    rows = []
    for k in sorted(base):
        el, g = base[k]["el"], types.get(k, "unknown")
        q = own.get(k)
        if q:
            slope, source = q["y"] / q["dr"], "own_" + q["src"]
        elif (el, g) in type_fit:
            slope, source = type_fit[(el, g)][0], "donor_type"
        else:
            slope, source = el_fit[el][0], "element"
        red = [p for p in pts[k] if p["src"] in ("first", "reverse") and p["ok"] and p["spin"] < SPIN and p["dr"] * p["y"] < 0]
        eps = [p for p in pts[k] if p["src"].startswith("eps") and p["ok"] and p["dr"] * p["y"] < 0]
        rows.append(dict(ref=k[0], bond=k[1], el=el, donor_type=g, r0=base[k]["r0"], k0=base[k]["k0"],
                         s2_10K_0=base[k]["s2"], slope=round(slope, 3), source=source,
                         own_dr=round(q["dr"], 4) if q else "", rearranged_complex=int(k[0] in rearranged),
                         slope_redox=round(max(red, key=lambda p: abs(p["dr"]))["y"] / max(red, key=lambda p: abs(p["dr"]))["dr"], 3) if red else "",
                         slope_eps=round(max(eps, key=lambda p: abs(p["dr"]))["y"] / max(eps, key=lambda p: abs(p["dr"]))["dr"], 3) if eps else "",
                         slope_line=base[k]["line"]))
    out = os.path.join(dft, "redox", "slopes_final.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    # report
    print("bonds: %d in %d complexes" % (len(rows), len({r["ref"] for r in rows})))
    print("slope source:", dict(Counter(r["source"] for r in rows)))
    print("rearranged complexes (all bonds take type/element slopes):", " ".join(rearranged) or "none")
    print("\n%-2s %-30s %5s %16s %6s" % ("el", "donor type", "bonds", "slope +/- SE", "R2"))
    for (el, g), (s, se, R2) in sorted(type_fit.items(), key=lambda x: (x[0][0], -len(gp[x[0]]))):
        print("%-2s %-30s %5d %9.2f +/- %4.2f %6.2f" % (el, g, len(gp[(el, g)]), s, se, R2))
    for el, (s, se, R2) in el_fit.items():
        print("%-2s %-30s %5d %9.2f +/- %4.2f %6.2f" % (el, "ALL", sum(len(v) for (e, _), v in gp.items() if e == el), s, se, R2))
    both = [r for r in rows if r["slope_redox"] != "" and r["slope_eps"] != ""]
    if both:
        d = [r["slope_redox"] - r["slope_eps"] for r in both]
        print("\nRKS/UKS check: %d bonds with a clean redox (RKS/UKS) and a clean epsilon (RKS/RKS) slope" % len(both))
        print("  redox - eps: median %.2f, median |diff| %.2f 1/A" % (median(d), median([abs(x) for x in d])))
        for el in ("N", "S"):
            de = [r["slope_redox"] - r["slope_eps"] for r in both if r["el"] == el]
            if de:
                print("  Zn-%s: n=%d, median %.2f, median |diff| %.2f" % (el, len(de), median(de), median([abs(x) for x in de])))
    # leave-one-out on bonds with |dr| >= 0.02
    errs = defaultdict(list)
    for k, q in own.items():
        if abs(q["dr"]) < 0.02:
            continue
        el, g = base[k]["el"], types.get(k, "unknown")
        G = [p for p in gp[(el, g)] if p != (q["dr"], q["y"])]
        if len(G) < MIN_TYPE:
            G = [p for (e, _), v in gp.items() if e == el for p in v if p != (q["dr"], q["y"])]
        s = fit0(G)[0]
        errs[el].append(abs(math.exp(-(s - q["y"] / q["dr"]) * 0.20 / 2) - 1))
    for el, v in errs.items():
        v = sorted(v)
        print("leave-one-out Zn-%s (n=%d): sigma2 error at +0.20 A from a borrowed slope: median %.1f%%, 90th %.1f%%"
              % (el, len(v), 100 * median(v), 100 * v[int(0.9 * len(v))]))
    print("\nwrote", os.path.relpath(out, dft))


if __name__ == "__main__":
    main()
