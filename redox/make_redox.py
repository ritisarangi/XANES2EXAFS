#!/usr/bin/env python3
"""Write optimisation + Hessian inputs for each complex with its charge moved one unit toward neutral.

Usage (inside the project folder on S3DF):
    python3 <repo>/redox/make_redox.py . lists/pilot.txt
Charge rule: q > 0 -> q - 1, q < 0 -> q + 1, q = 0 -> +1 (primary) with -1 as the fallback,
which redox_array.slurm runs only when the +1 run does not finish.
Multiplicity: doublet for an odd electron count, singlet for an even one (UKS for doublets).
Start geometry, method, basis and CPCM(water) are those of stage 2.
Writes redox/primary/<REF>/<REF>.inp, redox/fallback/<REF>/<REF>.inp (neutral complexes only)
and redox/jobs_<tag>.txt (one REF per line).
With --reverse: writes only redox/reverse/<REF>/<REF>.inp, one electron in the direction opposite
to the primary run (q > 0 -> q + 1, q < 0 -> q - 1, q = 0 -> -1), and redox/jobs_reverse_<tag>.txt.
Standard library only, Python 3.6+.
"""
import sys, os, json

Z = {"H": 1, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Si": 14, "P": 15, "S": 16, "Cl": 17,
     "Se": 34, "Br": 35, "I": 53, "Zn": 30, "Na": 11, "K": 19, "Li": 3, "As": 33, "Te": 52, "Sn": 50}


def write(dft, sub, ref, L, tz, q, note):
    nel = sum(Z[l.split()[0]] for l in L) - q
    mult = 2 if nel % 2 else 1
    rows = []
    for i, l in enumerate(L):
        el, x, y, z = l.split()[:4]
        rows.append("  %-2s %12.6f %12.6f %12.6f" % (el, float(x), float(y), float(z))
                    + (' newgto "def2-TZVP" end' if i in tz else ""))
    d = os.path.join(dft, "redox", sub, ref)
    os.makedirs(d, exist_ok=True)
    uks = " UKS" if mult > 1 else ""
    inp = ("# %s: %s, charge %d mult %d, stage-2 level from the stage-2 geometry\n" % (ref, note, q, mult)
           + "! B3LYP D3BJ def2-SVP def2/J RIJCOSX CPCM(water) TightOpt Freq DefGrid3 TightSCF%s\n" % uks
           + "%pal nprocs 16 end\n%maxcore 3000\n%geom MaxIter 300 end\n%scf MaxIter 500 end\n"
           + "* xyz %d %d\n" % (q, mult) + "\n".join(rows) + "\n*\n")
    open(os.path.join(d, ref + ".inp"), "w").write(inp)
    return mult


def main():
    dft = os.path.abspath(sys.argv[1])
    lst = sys.argv[2]
    reverse = "--reverse" in sys.argv
    tag = os.path.splitext(os.path.basename(lst))[0]
    refs = [l.strip() for l in open(os.path.join(dft, lst)) if l.strip() and not l.startswith("#")]
    jobs, skipped, summary = [], [], {}
    for ref in refs:
        s2 = os.path.join(dft, "stage2_b3lyp", ref)
        try:
            M = json.load(open(os.path.join(s2, ref + ".meta")))
            L = open(os.path.join(s2, ref + ".xyz")).read().strip().split("\n")[2:]
            assert len(L) == M["natoms"]
        except Exception:
            skipped.append(ref)
            continue
        tz = set(M["donors"]) | {M["zn_index"]}
        q0 = M["charge"]
        if reverse:
            qr = q0 + 1 if q0 > 0 else q0 - 1
            mr = write(dft, "reverse", ref, L, tz, qr, "charge %+d -> %+d, reverse of primary" % (q0, qr))
            key = "%+d -> %+d (mult %d)" % (q0, qr, mr)
            summary[key] = summary.get(key, 0) + 1
            jobs.append(ref)
            continue
        q1 = q0 - 1 if q0 > 0 else (q0 + 1 if q0 < 0 else 1)
        m1 = write(dft, "primary", ref, L, tz, q1, "charge %+d -> %+d" % (q0, q1))
        key = "%+d -> %+d (mult %d)" % (q0, q1, m1)
        if q0 == 0:
            m2 = write(dft, "fallback", ref, L, tz, -1, "charge 0 -> -1, fallback")
            key += ", fallback -1 (mult %d)" % m2
        summary[key] = summary.get(key, 0) + 1
        jobs.append(ref)
    jf = os.path.join(dft, "redox", ("jobs_reverse_%s.txt" if reverse else "jobs_%s.txt") % tag)
    open(jf, "w").write("\n".join(jobs) + "\n")
    for k in sorted(summary):
        print("  %-45s %d" % (k, summary[k]))
    print("complexes: %d  skipped: %s" % (len(jobs), " ".join(skipped) or "none"))
    print("jobs file:", os.path.relpath(jf, dft))


if __name__ == "__main__":
    main()
