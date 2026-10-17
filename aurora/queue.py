#!/usr/bin/env python3
"""Task queue for the Aurora node farm.

Usage (inside the run folder):
    python3 <repo>/aurora/queue.py build  . <jobs file> <queue dir> [REF ...]
    python3 <repo>/aurora/queue.py status . <jobs file>
    python3 <repo>/aurora/queue.py mark-lost . [running PBS job numbers ...]

build      writes <queue dir>/tasks.txt with every branch that can run now: continuations
           prepared by restart.py first, then fresh branches, largest complexes first so the
           long ones do not trail at the end. Only the given REFs when any are named.
status     counts branches by state.
mark-lost  tags the logs of branches whose PBS job ended without the branch writing an end
           line (node failure, job killed) as CANCELLED, so restart.py continues them.
Standard library only, Python 3.6+.
"""
import sys, os, re, glob, collections

OK = "ORCA TERMINATED NORMALLY"


def tail(p, n=4096):
    try:
        with open(p, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - n))
            return f.read().decode(errors="ignore")
    except OSError:
        return None


def natoms(p):
    try:
        t = open(p, errors="ignore").read()
    except OSError:
        return 0
    g = t.split("* xyz", 1)
    return len([l for l in g[1].split("\n")[1:] if l.strip() and l.strip() != "*"]) if len(g) > 1 else 0


def state(work, d):
    full = os.path.join(work, d)
    out, cont = tail(os.path.join(full, "scan.out")), tail(os.path.join(full, "scan_cont.out"))
    if out is not None and OK in out:
        return "done"
    if out is not None or cont is not None:
        return "started"            # running now, stopped (restart.py prepares it) or failed
    if os.path.exists(os.path.join(full, "scan_orig.inp")):
        return "continuation"
    return "fresh"


def main():
    cmd, work = sys.argv[1], os.path.abspath(sys.argv[2])
    if cmd == "mark-lost":
        running = set(sys.argv[3:])
        n = 0
        for lg in glob.glob(os.path.join(work, "logs", "scan*_*.log")):
            m = re.match(r"scanr?_(\d+)_", os.path.basename(lg))
            if not m or m.group(1) in running:
                continue
            t = open(lg, errors="ignore").read()
            if re.search(r"^scans/\S+ start ", t, re.M) and not re.search(r"^scans/\S+ end ", t, re.M) \
                    and not re.search(r"DUE TO TIME LIMIT|CANCELLED", t):
                open(lg, "a").write("CANCELLED (PBS job %s ended before this branch finished)\n" % m.group(1))
                n += 1
        print("logs tagged as cancelled: %d" % n)
        return
    jobs = [l.strip() for l in open(os.path.join(work, sys.argv[3])) if l.strip()]
    if cmd == "status":
        c = collections.Counter(state(work, d) for d in jobs)
        print("branches: %d done, %d started (running/stopped/failed), %d continuations ready, %d not started, %d total"
              % (c["done"], c["started"], c["continuation"], c["fresh"], len(jobs)))
        return
    qdir, refs = os.path.join(work, sys.argv[4]), set(sys.argv[5:])
    if refs:
        jobs = [d for d in jobs if d.split("/")[1] in refs]
    cont, fresh = [], []
    for d in jobs:
        s = state(work, d)
        if s in ("continuation", "fresh"):
            (cont if s == "continuation" else fresh).append((-natoms(os.path.join(work, d, "scan.inp")), d))
    tasks = [d for _, d in sorted(cont)] + [d for _, d in sorted(fresh)]
    os.makedirs(qdir, exist_ok=True)
    open(os.path.join(qdir, "tasks.txt"), "w").write("".join(d + "\n" for d in tasks))
    open(os.path.join(qdir, "next"), "w").write("0\n")
    print("queue: %d continuations + %d fresh branches -> %s" % (len(cont), len(fresh), os.path.relpath(qdir, work)))


if __name__ == "__main__":
    main()
