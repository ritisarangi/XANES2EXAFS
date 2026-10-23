#!/usr/bin/env python3
"""Task queue for the Aurora node farm.

Usage (inside the run folder):
    python3 <repo>/aurora/queue.py build  . <jobs file> <queue dir> [REF ...]   (env NATOMS_MIN, NATOMS_MAX)
    python3 <repo>/aurora/queue.py add    . <jobs file> <queue dir>                (env NATOMS_MIN, NATOMS_MAX)
    python3 <repo>/aurora/queue.py prioritize . <jobs file> <queue dir> [<queue dir> ...]
    python3 <repo>/aurora/queue.py status . <jobs file>
    python3 <repo>/aurora/queue.py mark-lost . [running PBS job numbers ...]

build      writes <queue dir>/tasks.txt with every branch that can run now: continuations
           prepared by restart.py first, then fresh branches, largest complexes first so the
           long ones do not trail at the end. Only the given REFs when any are named, and only
           complexes with NATOMS_MIN <= atoms < NATOMS_MAX (the farms for normal and large
           complexes use different core counts).
add        puts continuations prepared by restart.py at the front of a live queue (farms of the
           pool keep running; same flock as the farm slots).
prioritize moves the pending branches of complexes that are at least half done to the front,
           most complete first (whole complexes are what gets published); the rest keep their order.
status     counts branches by state.
mark-lost  tags the logs of branches whose PBS job ended without the branch writing an end
           line (node failure, job killed) as CANCELLED, so restart.py continues them.
Standard library only, Python 3.6+.
"""
import sys, os, re, glob, json, collections

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


def in_pool(work, jobs):
    lo, hi = int(os.environ.get("NATOMS_MIN", 0)), int(os.environ.get("NATOMS_MAX", 10 ** 6))
    size = {}
    for d in jobs:
        r = d.split("/")[1]
        if r not in size:
            size[r] = json.load(open(os.path.join(work, "stage2_b3lyp", r, r + ".meta")))["natoms"]
    return [d for d in jobs if lo <= size[d.split("/")[1]] < hi]


def add_continuations(work, jobs, qdir):
    """Put continuations prepared by restart.py at the front of a live queue, under the same
    flock the farm slots use, so farms of the pool can keep running."""
    import fcntl
    # the states are read without the lock (minutes on a busy Lustre); a branch a farm claims
    # meanwhile still looks like a continuation, so everything past the position at the start
    # (claimed since, or still pending) counts as queued
    n0 = int(open(os.path.join(qdir, "next")).read())
    cont = [d for d in in_pool(work, jobs) if state(work, d) == "continuation"]
    with open(os.path.join(qdir, "lock"), "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        tasks = [l.strip() for l in open(os.path.join(qdir, "tasks.txt")) if l.strip()]
        n = int(open(os.path.join(qdir, "next")).read())
        pending = set(tasks[min(n0, n):])
        new = [d for _, d in sorted((-natoms(os.path.join(work, d, "scan.inp")), d) for d in cont if d not in pending)]
        tmp = os.path.join(qdir, "tasks.txt.new")
        open(tmp, "w").write("".join(d + "\n" for d in tasks[:n] + new + tasks[n:]))
        os.rename(tmp, os.path.join(qdir, "tasks.txt"))
        fcntl.flock(lk, fcntl.LOCK_UN)
    print("queue: %d continuations added to the front of %s (%d pending now)" % (len(new), os.path.relpath(qdir, work), len(tasks) - n + len(new)))


def prioritize(work, jobs, qdirs):
    import fcntl
    by = collections.defaultdict(list)
    for d in jobs:
        by[d.split("/")[1]].append(d)
    frac = {r: sum(state(work, d) == "done" for d in ds) / float(len(ds)) for r, ds in by.items()}
    key = lambda d: -frac[d.split("/")[1]] if frac[d.split("/")[1]] >= 0.5 else 0.0
    for qdir in qdirs:
        with open(os.path.join(qdir, "lock"), "a") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            tasks = [l.strip() for l in open(os.path.join(qdir, "tasks.txt")) if l.strip()]
            n = int(open(os.path.join(qdir, "next")).read())
            pend = sorted(tasks[n:], key=key)          # stable: equal keys keep their order
            tmp = os.path.join(qdir, "tasks.txt.new")
            open(tmp, "w").write("".join(d + "\n" for d in tasks[:n] + pend))
            os.rename(tmp, os.path.join(qdir, "tasks.txt"))
            fcntl.flock(lk, fcntl.LOCK_UN)
        print("prioritize %s: %d of %d pending branches belong to complexes at least half done"
              % (os.path.basename(qdir), sum(1 for d in pend if key(d) < 0), len(pend)))


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
    if cmd == "prioritize":
        prioritize(work, jobs, [os.path.join(work, q) for q in sys.argv[4:]])
        return
    if cmd == "add":
        add_continuations(work, jobs, os.path.join(work, sys.argv[4]))
        return
    qdir, refs = os.path.join(work, sys.argv[4]), set(sys.argv[5:])
    if refs:
        jobs = [d for d in jobs if d.split("/")[1] in refs]
    lo, hi = int(os.environ.get("NATOMS_MIN", 0)), int(os.environ.get("NATOMS_MAX", 10 ** 6))
    size = {}
    for d in jobs:
        r = d.split("/")[1]
        if r not in size:
            size[r] = json.load(open(os.path.join(work, "stage2_b3lyp", r, r + ".meta")))["natoms"]
    jobs = [d for d in jobs if lo <= size[d.split("/")[1]] < hi]
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
