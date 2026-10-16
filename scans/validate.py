#!/usr/bin/env python3
"""Check every scan point and decide which ones enter the dataset.

Usage (run inside the project folder):
    python3 <repo>/scans/validate.py . lists/pilot.txt [tag]

Per point, in order (first failure is recorded; later points of that branch become after_fail):
  not_converged  step optimisation or SCF did not converge
  constraint     scanned coordinate missed its target (0.002 A, 0.1 deg angle, 0.2 deg dihedral)
  bonds          covalent bond graph differs from the reference (bond broken/formed, H moved)
  shell          a reference donor left 2.8 A, or an unscanned Zn-L moved more than 0.15 A
  new_contact    a non-donor heavy atom came within 2.6 A of Zn
  energy_cap     more than 40 kJ/mol above the branch start
  energy_drop    energy fell by more than 2 kJ/mol from the previous point (new species)
  jump           a heavy-atom distance changed by more than 0.3 A from the previous point
  ref_mismatch   the branch start does not reproduce the stage-2 minimum (0.05 A, 0.5 kJ/mol)
Writes scans/validation_<tag>.csv and prints pass rates and cost. Standard library only.
"""
import sys, os, re, csv, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zncore as Z

HART = 2625.4996  # kJ/mol per hartree
TOL = {"B": 0.002, "A": 0.1, "D": 0.2}
CAP, DROP, JUMP, SHELL, NEWC, DONOR_MAX = 40.0, 2.0, 0.3, 0.15, 2.6, 2.8


def parse_steps(out, n_atoms):
    """[(converged, energy, geometry)] per relaxed-scan step, from the ORCA output."""
    parts = re.split(r"RELAXED SURFACE SCAN STEP\s+\d+", out)[1:]
    steps = []
    for p in parts:
        conv = "THE OPTIMIZATION HAS CONVERGED" in p
        E = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", p)
        blocks = p.split("CARTESIAN COORDINATES (ANGSTROEM)")
        geo = None
        if len(blocks) > 1:
            L = blocks[-1].split("\n")[2:2 + n_atoms]
            try:
                geo = [(s.split()[0], float(s.split()[1]), float(s.split()[2]), float(s.split()[3])) for s in L]
            except (IndexError, ValueError):
                geo = None
        steps.append((conv, float(E[-1]) if E else None, geo))
    return steps


def heavy_dmat(A, idx):
    return [[Z.dist(A[i], A[j]) for j in idx] for i in idx]


def max_ddiff(M1, M2):
    return max(abs(a - b) for r1, r2 in zip(M1, M2) for a, b in zip(r1, r2))


def angdiff(a, b):
    d = (a - b + 180.0) % 360.0 - 180.0
    return abs(d)


def ctype(name):
    return name.split("_")[0]


def main():
    dft = os.path.abspath(sys.argv[1])
    lst = sys.argv[2]
    tag = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(os.path.basename(lst))[0]
    refs = [l.strip() for l in open(os.path.join(dft, lst)) if l.strip()]
    rows, jobstate, cost = [], collections.Counter(), []
    for ref in refs:
        cj = os.path.join(dft, "scans", ref, "coords.json")
        if not os.path.exists(cj):
            continue
        C = json.load(open(cj))
        R = Z.read_xyz(os.path.join(dft, "stage2_b3lyp", ref, ref + ".xyz"))
        n = len(R)
        zn, donors = C["zn"], C["donors"]
        RB = Z.bonds(R)
        heavy = [i for i in range(n) if R[i][0] != "H"]
        RM = heavy_dmat(R, heavy)
        s2 = os.path.join(dft, "stage2_b3lyp", ref, ref + ".out")
        E2 = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", open(s2, errors="ignore").read()) if os.path.exists(s2) else []
        E2 = float(E2[-1]) if E2 else None
        ref_d = {L: Z.dist(R[zn], R[L]) for L in donors}
        for c in C["coords"]:
            path = os.path.join(dft, c["dir"], "scan.out")
            out = open(path, errors="ignore").read() if os.path.exists(path) else ""
            done = "ORCA TERMINATED NORMALLY" in out
            state = "done" if done else ("pending" if not out else ("failed" if "aborting" in out.lower() or "error termination" in out.lower() else "running"))
            jobstate[state] += 1
            steps = parse_steps(out, n) if out else []
            rt = re.findall(r"TOTAL RUN TIME: (\d+) days (\d+) hours (\d+) minutes", out)
            if rt and steps:
                d_, h_, m_ = map(int, rt[-1])
                cost.append(((d_ * 24 + h_) * 60 + m_) / len(steps))
            k_n = c["npoints"]
            failed, E0, prevE, prevM = False, None, None, None
            for k in range(k_n):
                target = c["start"] + (c["end"] - c["start"]) * k / (k_n - 1)
                row = dict(ref=ref, coord=c["name"], type=ctype(c["name"]), branch=c["branch"], step=k,
                           offset=round(target - c["v0"], 4), target=round(target, 4), value="", E_rel_kJ="", status="")
                if k >= len(steps):
                    row["status"] = "after_fail" if failed else ("missing" if done else "pending")
                    rows.append(row)
                    continue
                if not done and k == len(steps) - 1 and not failed:
                    # last step of a job that is still running: in progress, not a failure
                    row["status"] = "running"
                    rows.append(row)
                    continue
                conv, E, A = steps[k]
                why = ""
                if failed:
                    why = "after_fail"
                elif not conv or E is None or A is None:
                    why = "not_converged"
                else:
                    v = Z.measure(A, c["kind"], c["atoms"])
                    row["value"] = round(v, 4)
                    dv = abs(v - target) if c["kind"] != "D" else angdiff(v, target)
                    if E0 is None:
                        E0 = E
                    row["E_rel_kJ"] = round((E - E0) * HART, 3)
                    M = heavy_dmat(A, heavy)
                    scanned = c["atoms"][1] if c["kind"] == "B" else None
                    if dv > TOL[c["kind"]]:
                        why = "constraint"
                    elif Z.bonds(A) != RB:
                        why = "bonds"
                    elif any(Z.dist(A[zn], A[L]) > DONOR_MAX for L in donors) or any(
                            abs(Z.dist(A[zn], A[L]) - ref_d[L]) > SHELL for L in donors if L != scanned):
                        why = "shell"
                    elif any(A[i][0] != "H" and i != zn and i not in donors and Z.dist(A[zn], A[i]) < NEWC for i in range(n)):
                        why = "new_contact"
                    elif (E - E0) * HART > CAP:
                        why = "energy_cap"
                    elif prevE is not None and (prevE - E) * HART > DROP:
                        why = "energy_drop"
                    elif prevM is not None and max_ddiff(M, prevM) > JUMP:
                        why = "jump"
                    elif k == 0 and (max_ddiff(M, RM) > 0.05 or (E2 is not None and abs(E - E2) * HART > 0.5)):
                        why = "ref_mismatch"
                    prevE, prevM = E, M
                row["status"] = why or "pass"
                if why:
                    failed = True
                rows.append(row)
    if not rows:
        print("no scan folders found")
        return
    fn = os.path.join(dft, "scans", "validation_%s.csv" % tag)
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("jobs:", dict(jobstate))
    print("points:", dict(collections.Counter(r["status"] for r in rows)))
    print("unique passing geometries (branch starts counted once per coordinate):",
          sum(1 for r in rows if r["status"] == "pass" and r["step"] > 0) + len({(r["ref"], r["coord"]) for r in rows if r["status"] == "pass" and r["step"] == 0}))
    print("\npass rate by coordinate type and distance from the minimum (completed steps only)")
    agg = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        if r["status"] in ("pending", "running", "missing"):
            continue
        key = (r["type"], r["branch"], abs(r["offset"]))
        agg[key][1] += 1
        agg[key][0] += r["status"] == "pass"
    for key in sorted(agg):
        p, t = agg[key]
        print("  %-6s %-3s |offset| %7.3f  %4d/%-4d %5.1f%%" % (key[0], key[1], key[2], p, t, 100.0 * p / t))
    reasons = collections.Counter((r["type"], r["status"]) for r in rows if r["status"] not in ("pass", "after_fail", "pending", "running", "missing"))
    if reasons:
        print("\nfirst-failure reasons:", dict(reasons))
    if cost:
        cost.sort()
        print("\nminutes per scan point: median %.1f, max %.1f (%d finished jobs)" % (cost[len(cost) // 2], cost[-1], len(cost)))
    print("\nwrote", os.path.relpath(fn, dft))


if __name__ == "__main__":
    main()
