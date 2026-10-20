#!/usr/bin/env python3
"""Pair each Zn-L bond in the stage-2 complex with the same bond after the one-electron change.

Usage (inside the project folder, after the redox runs):
    python3 <repo>/redox/analyze_redox.py . lists/pilot.txt
For each bond in both states: r, relaxed force constant k_hess, nu_eff and sigma2 at 10 K
from the Hessian (same formulas as dielectric/analyze_eps.py), then
    dr = r_redox - r_ref,  dk/k,  slope = (ln k_redox - ln k_ref) / dr   (1/A)
and a status: use if 0.01 <= |dr| <= 0.15 A with the Zn-L set unchanged, small if |dr| < 0.01,
dissociated if |dr| > 0.15 A or the donor leaves 2.8 A. Mulliken spin on Zn and on each donor,
and <S**2>, are kept for reference. Writes redox/redox_compare_<tag>.csv. With --reverse it reads redox/reverse/ instead and
writes redox/redox_compare_reverse_<tag>.csv.
Standard library only, Python 3.6+.
"""
import sys, os, re, json, math, csv
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dft", "analysis"))
sys.path.insert(0, os.path.join(HERE, "..", "dielectric"))
from report_extract import read_xyz, read_hess  # noqa: E402
from analyze_eps import bond_props, LINE  # noqa: E402

LO, HI, DONOR_MAX = 0.01, 0.15, 2.8


def out_info(p):
    t = open(p, errors="ignore").read() if os.path.exists(p) else ""
    ok = "ORCA TERMINATED NORMALLY" in t and "VIBRATIONAL FREQUENCIES" in t
    q = re.findall(r"Total Charge\s+Charge\s+\.\.\.\.\s+(-?\d+)", t)
    s2 = re.findall(r"Expectation value of <S\*\*2>\s*:\s*([\d.]+)", t)
    spin = {}
    blk = t.split("MULLIKEN ATOMIC CHARGES AND SPIN POPULATIONS")
    if len(blk) > 1:
        for l in blk[-1].split("\n")[2:]:
            m = re.match(r"\s*(\d+)\s+\w+\s*:\s+(-?[\d.]+)\s+(-?[\d.]+)", l)
            if not m:
                break
            spin[int(m.group(1))] = float(m.group(3))
    return ok, (int(q[-1]) if q else None), (float(s2[-1]) if s2 else None), spin


def main():
    dft = os.path.abspath(sys.argv[1])
    lst = sys.argv[2]
    tag = os.path.splitext(os.path.basename(lst))[0]
    subs = ("reverse",) if "--reverse" in sys.argv else ("primary", "fallback")
    if "--reverse" in sys.argv:
        tag = "reverse_" + tag
    refs = [l.strip() for l in open(os.path.join(dft, lst)) if l.strip() and not l.startswith("#")]
    rows, notes = [], []
    for ref in refs:
        meta = json.load(open(os.path.join(dft, "stage2_b3lyp", ref, ref + ".meta")))
        zn, donors = meta["zn_index"], meta["donors"]
        state = None
        for sub in subs:
            d = os.path.join(dft, "redox", sub, ref)
            ok, q, s2, spin = out_info(os.path.join(d, ref + ".out"))
            if ok:
                state = (sub, d, q, s2, spin)
                break
        if not state:
            notes.append("%s: no finished redox run" % ref)
            continue
        sub, d, q, s2, spin = state
        res = {}
        for name, dd in (("ref", os.path.join(dft, "stage2_b3lyp", ref)), ("redox", d)):
            masses, freqs, modes = read_hess(os.path.join(dd, ref + ".hess"))
            imag = [round(f, 1) for f in freqs if f < -1.0]
            if imag and name == "redox":
                notes.append("%s %s: imaginary %s" % (ref, sub, imag))
            R = read_xyz(os.path.join(dd, ref + ".xyz"))
            res[name] = {L: bond_props(masses, freqs, modes, zn, L, R) for L in donors}
        for i, L in enumerate(donors):
            el = meta["donor_elems"][i]
            r0, s0, nu0, k0 = res["ref"][L]
            r1, s1, nu1, k1 = res["redox"][L]
            dr = r1 - r0
            if r1 > DONOR_MAX or abs(dr) > HI:
                st = "dissociated"
            elif abs(dr) < LO:
                st = "small"
            else:
                st = "use"
            rows.append(dict(ref=ref, run=sub, charge_ref=meta["charge"], charge_redox=q,
                             S2=s2 if s2 is not None else "", bond="Zn-%s%d" % (el, L), el=el,
                             r_ref=round(r0, 4), r_redox=round(r1, 4), dr=round(dr, 4),
                             k_ref=round(k0, 4), k_redox=round(k1, 4), dk_pct=round(100 * (k1 - k0) / k0, 1),
                             s2_10K_ref=round(s0, 6), s2_10K_redox=round(s1, 6),
                             nu_ref=round(nu0, 1), nu_redox=round(nu1, 1),
                             slope=round((math.log(k1) - math.log(k0)) / dr, 2) if abs(dr) > 1e-4 else "",
                             slope_line=round(-2 * LINE[el][1] / nu0, 2) if el in LINE else "",
                             spin_Zn=round(spin.get(zn, 0.0), 3), spin_L=round(spin.get(L, 0.0), 3), status=st))
    if rows:
        fn = os.path.join(dft, "redox", "redox_compare_%s.csv" % tag)
        with open(fn, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print("%-7s %-8s %-4s %-9s %8s %7s %7s %7s %6s %6s %-11s" % ("ref", "run", "q", "bond", "dr", "dk/k%", "slope", "line", "spinL", "S2", "status"))
        for r in rows:
            print("%-7s %-8s %+d>%+d %-9s %8.4f %7.1f %7s %7s %6.2f %6s %-11s" % (
                r["ref"], r["run"], r["charge_ref"], r["charge_redox"] if r["charge_redox"] is not None else 0, r["bond"], r["dr"], r["dk_pct"],
                r["slope"], r["slope_line"], r["spin_L"], r["S2"], r["status"]))
        from collections import Counter
        print("\nbonds by status:", dict(Counter(r["status"] for r in rows)))
        print("wrote", os.path.relpath(fn, dft))
    if notes:
        print("\nnotes:\n  " + "\n  ".join(notes))


if __name__ == "__main__":
    main()
