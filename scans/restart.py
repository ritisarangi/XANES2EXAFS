#!/usr/bin/env python3
"""Restart scan branches that stopped before finishing (time limit or cancellation).

Usage (inside the project folder on S3DF):
    python3 <repo>/scans/restart.py .            # find stopped branches, write restart inputs
    python3 <repo>/scans/restart.py . --dry      # only list what it would do
    python3 <repo>/scans/restart.py . --stitch scans/REF/coord_branch   # used by restart_array.slurm

A branch counts as stopped when its last Slurm log says TIME LIMIT or CANCELLED and its
output did not terminate normally. For each one the converged steps so far are kept in
scan_acc.txt, the original input is saved once as scan_orig.inp, and a new scan.inp
continues from the last converged geometry over the remaining targets (a constrained
optimisation when one target is left). The continuation writes scan_cont.out; when it
terminates normally, --stitch writes scan.out = kept steps + new steps, numbered as one
scan, so validate.py reads the branch as if it had run in one piece.
Writes scans/jobs_restart.txt. Standard library only, Python 3.6+.
"""
import sys, os, re, glob, json

MARK = "RELAXED SURFACE SCAN STEP"


def chunks(text):
    return re.split(r"RELAXED SURFACE SCAN STEP\s+\d+[^\n]*\n", text)[1:]


def good(c):
    return ("THE OPTIMIZATION HAS CONVERGED" in c and "FINAL SINGLE POINT ENERGY" in c
            and "CARTESIAN COORDINATES (ANGSTROEM)" in c)


def leading_good(text):
    out = []
    for c in chunks(text):
        if not good(c):
            break
        out.append(c)
    return out


def last_geom(c, n):
    L = c.split("CARTESIAN COORDINATES (ANGSTROEM)")[-1].split("\n")[2:2 + n]
    return [l.split()[:4] for l in L]


def read(p):
    return open(p, errors="ignore").read() if os.path.exists(p) else ""


def acc_load(d):
    t = read(os.path.join(d, "scan_acc.txt"))
    return chunks(t) if t else []


def acc_save(d, cs):
    open(os.path.join(d, "scan_acc.txt"), "w").write("".join("%s %d\n%s" % (MARK, i + 1, c) for i, c in enumerate(cs)))


def stopped_dirs(dft):
    latest = {}
    for lg in glob.glob(os.path.join(dft, "logs", "scan_*.log")) + glob.glob(os.path.join(dft, "logs", "scanr_*.log")):
        t = read(lg)
        m = re.search(r"^(scans/\S+) start ", t, re.M)
        if not m:
            continue
        d = m.group(1)
        mt = os.path.getmtime(lg)
        if d not in latest or mt > latest[d][0]:
            latest[d] = (mt, bool(re.search(r"DUE TO TIME LIMIT|CANCELLED", t)))
    out = []
    for d, (_, stopped) in sorted(latest.items()):
        full = os.path.join(dft, d)
        prepared = (os.path.exists(os.path.join(full, "scan_orig.inp")) and not os.path.exists(os.path.join(full, "scan.out"))
                    and not os.path.exists(os.path.join(full, "scan_cont.out")))   # continuation written, not run yet
        if stopped and not prepared and "ORCA TERMINATED NORMALLY" not in read(os.path.join(full, "scan.out")):
            out.append(d)
    return out


def prepare(dft, d, dry):
    full = os.path.join(dft, d)
    orig = os.path.join(full, "scan_orig.inp")
    if not os.path.exists(orig):
        if not dry:
            os.rename(os.path.join(full, "scan.inp"), orig)
        else:
            orig = os.path.join(full, "scan.inp")
    inp = read(orig)
    m = re.search(r"Scan\s*\n\s*([BAD])\s+([\d ]+?)\s*=\s*(-?[\d.]+),\s*(-?[\d.]+),\s*(\d+)", inp)
    kind, atoms, v1, v2, n = m.group(1), m.group(2).split(), float(m.group(3)), float(m.group(4)), int(m.group(5))
    natoms = len(inp.split("* xyz")[1].strip().split("\n")) - 2
    acc = acc_load(full)
    part = read(os.path.join(full, "scan_cont.out")) if acc else read(os.path.join(full, "scan.out"))
    good = leading_good(part)
    acc = acc + good
    k = len(acc)
    # RESUME_PARTIAL=1: start the interrupted step from its latest optimisation geometry instead of
    # the last converged step; same target, so the constrained optimisation ends at the same point
    # and the step's finished optimisation cycles are not repeated
    partial = None
    if os.environ.get("RESUME_PARTIAL") == "1" and k > 0:
        rest = chunks(part)[len(good):]
        if rest and "CARTESIAN COORDINATES (ANGSTROEM)" in rest[0]:
            G = last_geom(rest[0], natoms)
            try:
                if len(G) == natoms and all(len(g) == 4 and [float(x) for x in g[1:]] for g in G):
                    partial = rest[0]
            except ValueError:
                pass
    tgt = [v1 + (v2 - v1) * i / (n - 1) for i in range(n)]
    fmt = (lambda v: "%.4f" % v) if kind == "B" else (lambda v: "%.3f" % v)
    if dry:
        return "%s: %d of %d steps kept, %d to run" % (d, k, n, n - k)
    acc_save(full, acc)
    head, rest = inp.split("%geom", 1)
    tail = rest.split("* xyz", 1)[1]
    cm = tail.strip().split("\n")[0].split()            # charge mult
    old = [l for l in tail.strip().split("\n")[1:] if l.strip() != "*"]
    if k == 0:
        new = inp
    else:
        G = last_geom(partial or acc[-1], natoms)
        rows = []
        for g, o in zip(G, old):
            extra = ' newgto "def2-TZVP" end' if "newgto" in o else ""
            rows.append("  %-2s %12.6f %12.6f %12.6f%s" % (g[0], float(g[1]), float(g[2]), float(g[3]), extra))
        left = n - k
        if left >= 2:
            geom = "%%geom\n  MaxIter 100\n  Scan\n    %s %s = %s, %s, %d\n  end\nend\n" % (kind, " ".join(atoms), fmt(tgt[k]), fmt(v2), left)
        else:
            geom = "%%geom\n  MaxIter 100\n  Constraints\n    { %s %s %s C }\n  end\nend\n" % (kind, " ".join(atoms), fmt(tgt[k]))
        new = head + geom + "* xyz %s %s\n%s\n*\n" % (cm[0], cm[1], "\n".join(rows))
    # new input first (atomically), old outputs renamed last: a branch interrupted at any point is
    # either untouched or fully prepared, and a repeated run finishes the job
    open(os.path.join(full, "scan.inp.new"), "w").write(new)
    os.rename(os.path.join(full, "scan.inp.new"), os.path.join(full, "scan.inp"))
    for f in ("scan.out", "scan_cont.out"):
        p = os.path.join(full, f)
        if os.path.exists(p):
            i = 1
            while os.path.exists(os.path.join(full, "scan_try%d.out" % i)):
                i += 1
            os.rename(p, os.path.join(full, "scan_try%d.out" % i))
    return "%s: %d of %d steps kept, %d to run%s" % (d, k, n, n - k, " (interrupted step resumed from its last geometry)" if partial else "")


def stitch(dft, d):
    full = os.path.join(dft, d)
    cont = read(os.path.join(full, "scan_cont.out"))
    if "ORCA TERMINATED NORMALLY" not in cont:
        print(d, "continuation did not terminate normally; nothing stitched")
        return 1
    new = chunks(cont)
    if not new:                       # constrained optimisation for the last target
        new = [cont]
    allc = acc_load(full) + new
    text = "".join("%s %d\n%s" % (MARK, i + 1, c) for i, c in enumerate(allc))
    open(os.path.join(full, "scan.out"), "w").write(text + "\n                             ****ORCA TERMINATED NORMALLY****\n")
    print(d, "stitched: %d steps" % len(allc))
    return 0


def main():
    dft = os.path.abspath(sys.argv[1])
    if "--stitch" in sys.argv:
        sys.exit(stitch(dft, sys.argv[sys.argv.index("--stitch") + 1]))
    dry = "--dry" in sys.argv
    ds = stopped_dirs(dft)
    for d in ds:
        print(prepare(dft, d, dry))
    if not dry and ds:
        open(os.path.join(dft, "scans", "jobs_restart.txt"), "w").write("\n".join(ds) + "\n")
        print("wrote scans/jobs_restart.txt (%d branches)" % len(ds))
    if not ds:
        print("no stopped branches found")


if __name__ == "__main__":
    main()
