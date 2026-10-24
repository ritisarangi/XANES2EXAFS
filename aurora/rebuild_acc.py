#!/usr/bin/env python3
"""Rebuild a branch's scan_acc.txt from its ORCA outputs, and check the existing one.

Usage (inside the run folder):
    python3 <repo>/aurora/rebuild_acc.py . <list of branch folders> [--write]

restart.py keeps the converged steps of every stopped run in scan_acc.txt: each time it prepares a
continuation it appends the leading converged steps of the run that just stopped, then renames
that run's output to scan_tryN.out. The tries are numbered in the order the runs happened, so
replaying them gives scan_acc.txt again. For every folder this prints whether the replay matches
the existing scan_acc.txt (same steps, byte for byte) and, with --write, rewrites scan_acc.txt
and scan.inp (the continuation input, as restart.py writes it) where the existing one is empty or
shorter than the replay. Folders with a current scan.out or scan_cont.out are left alone.
Standard library only, Python 3.6+.
"""
import sys, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scans"))
import restart as R  # noqa: E402


def tries(full):
    ts = glob.glob(os.path.join(full, "scan_try*.out"))
    return sorted(ts, key=lambda p: int(re.search(r"scan_try(\d+)\.out$", p).group(1)))


ECHO_SCAN = re.compile(r"^\|\s*\d+>\s*[BAD]\s+[\d ]+?\s*=\s*(-?[\d.]+),\s*-?[\d.]+,\s*\d+", re.M)
ECHO_CONS = re.compile(r"^\|\s*\d+>\s*\{\s*[BAD]\s+[\d ]+?\s+(-?[\d.]+)\s+C\s*\}", re.M)


def start_target(text):
    h = text[:80000]
    m = ECHO_SCAN.search(h) or ECHO_CONS.search(h)
    return float(m.group(1)) if m else None


def targets(full):
    inp = R.read(os.path.join(full, "scan_orig.inp"))
    m = re.search(r"Scan\s*\n\s*([BAD])\s+([\d ]+?)\s*=\s*(-?[\d.]+),\s*(-?[\d.]+),\s*(\d+)", inp)
    v1, v2, n = float(m.group(3)), float(m.group(4)), int(m.group(5))
    return [v1 + (v2 - v1) * i / (n - 1) for i in range(n)]


def inp_matches(full, k):
    """scan.inp is the continuation of k kept steps: it starts at target k (or is the original
    input when k is 0)."""
    t = R.read(os.path.join(full, "scan.inp"))
    if not t.strip():
        return False
    tgt = targets(full)
    if k >= len(tgt):
        return True
    m = re.search(r"Scan\s*\n\s*[BAD]\s+[\d ]+?\s*=\s*(-?[\d.]+),", t) or re.search(r"\{\s*[BAD]\s+[\d ]+?\s+(-?[\d.]+)\s+C\s*\}", t)
    return bool(m) and abs(float(m.group(1)) - tgt[k]) <= 1e-3


def clean(chunk, elems):
    """The step's final geometry has one row per atom, in input order, with three numbers."""
    try:
        G = R.last_geom(chunk, len(elems))
        return len(G) == len(elems) and all(g[0] == e and len(g) == 4 and [float(x) for x in g[1:]] for g, e in zip(G, elems)) \
            and re.search(r"FINAL SINGLE POINT ENERGY\s+-?\d+\.\d+\s*\n", chunk) is not None
    except ValueError:
        return False


def replay(full):
    """The tries in order; a try continues the chain only if it started at the chain's next
    target (a run restarted from an earlier point, e.g. from the original input, is skipped)."""
    acc, tgt = [], targets(full)
    inp = R.read(os.path.join(full, "scan_orig.inp"))
    elems = [l.split()[0] for l in inp.split("* xyz", 1)[1].strip().split("\n")[1:] if l.strip() and l.strip() != "*"]
    for p in tries(full):
        t = R.read(p)
        s = start_target(t)
        if s is None or len(acc) >= len(tgt) or abs(s - tgt[len(acc)]) > 1e-3:
            continue
        for c in R.leading_good(t):
            if not clean(c, elems):          # a damaged step (e.g. output lost to a failed write): the chain stops here
                return acc
            acc.append(c)
    return acc


def main():
    work = os.path.abspath(sys.argv[1])
    dirs = [l.strip() for l in open(sys.argv[2]) if l.strip()]
    write = "--write" in sys.argv
    stats = {}
    for d in dirs:
        full = os.path.join(work, d)
        if os.path.exists(os.path.join(full, "scan.out")) or os.path.exists(os.path.join(full, "scan_cont.out")):
            why = "has a current output; left alone"
        elif not os.path.exists(os.path.join(full, "scan_orig.inp")):
            why = "never prepared; nothing to rebuild"
        else:
            new = replay(full)
            old = R.acc_load(full)
            inp_ok = inp_matches(full, len(new))
            if old == new and inp_ok:
                why = "matches (%d steps)" % len(new)
            elif old == new:
                why = "scan.inp does not continue the %d kept steps" % len(new)
                if write:
                    rebuild(work, d, new)
                    why += "; rebuilt"
            elif len(old) < len(new) and new[:len(old)] == old:
                why = "existing is short: %d of %d steps" % (len(old), len(new))
                if write:
                    rebuild(work, d, new)
                    why += "; rebuilt"
            else:
                why = "DIFFERS: existing %d steps, replay %d" % (len(old), len(new))
        stats[why.split(":")[0].split(" (")[0]] = stats.get(why.split(":")[0].split(" (")[0], 0) + 1
        print("%s: %s" % (d, why))
    print("summary:", ", ".join("%s %d" % kv for kv in sorted(stats.items())))


def rebuild(work, d, acc):
    """Write scan_acc.txt and the continuation input exactly as restart.prepare does."""
    full = os.path.join(work, d)
    inp = R.read(os.path.join(full, "scan_orig.inp"))
    m = re.search(r"Scan\s*\n\s*([BAD])\s+([\d ]+?)\s*=\s*(-?[\d.]+),\s*(-?[\d.]+),\s*(\d+)", inp)
    kind, atoms, v1, v2, n = m.group(1), m.group(2).split(), float(m.group(3)), float(m.group(4)), int(m.group(5))
    natoms = len(inp.split("* xyz")[1].strip().split("\n")) - 2
    k = len(acc)
    tgt = [v1 + (v2 - v1) * i / (n - 1) for i in range(n)]
    fmt = (lambda v: "%.4f" % v) if kind == "B" else (lambda v: "%.3f" % v)
    R.acc_save(full, acc[:n])
    if k >= n:
        text = "".join("%s %d\n%s" % (R.MARK, i + 1, c) for i, c in enumerate(acc[:n]))
        open(os.path.join(full, "scan.out.new"), "w").write(text + "\n                             ****ORCA TERMINATED NORMALLY****\n")
        os.rename(os.path.join(full, "scan.out.new"), os.path.join(full, "scan.out"))
        return
    if k == 0:
        new = inp
    else:
        head, rest = inp.split("%geom", 1)
        tail = rest.split("* xyz", 1)[1]
        cm = tail.strip().split("\n")[0].split()
        old = [l for l in tail.strip().split("\n")[1:] if l.strip() != "*"]
        G = R.last_geom(acc[-1], natoms)
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
    open(os.path.join(full, "scan.inp.new"), "w").write(new)
    os.rename(os.path.join(full, "scan.inp.new"), os.path.join(full, "scan.inp"))


if __name__ == "__main__":
    main()
