#!/usr/bin/env python3
"""Check that no two ORCA runs ever shared or crossed a branch folder.

Usage (inside the run folder):
    python3 <repo>/aurora/audit.py . scans/jobs_scan_full.txt [REF ...]

identity    every ORCA output in a branch folder (scan.out, scan_cont.out, scan_try*.out) echoes
            that folder's own input: same scanned or constrained coordinate (type and atoms),
            same charge and multiplicity
overlap     no branch folder was run by two ORCA processes at the same time (from the run logs)
queue       no branch is pending twice in a queue, and no branch is in both pools
With REFs, identity and overlap are checked for those complexes only. Prints the problems found
and a summary; with AUDIT_BAD set, also writes the complexes with problems to that file (ALL for
a queue problem). Folders listed in autopilot/audit_reviewed.txt (one per line, with the reason)
had an overlap that was examined and found harmless: it is reported, not counted.
Standard library only, Python 3.6+.
"""
import sys, os, re, glob, collections, time

ECHO_SCAN = re.compile(r"^\|\s*\d+>\s*([BAD])\s+([\d ]+?)\s*=\s*-?[\d.]+,\s*-?[\d.]+,\s*\d+", re.M)
ECHO_CONS = re.compile(r"^\|\s*\d+>\s*\{\s*([BAD])\s+([\d ]+?)\s+-?[\d.]+\s+C\s*\}", re.M)
ECHO_XYZ = re.compile(r"^\|\s*\d+>\s*\*\s*xyz\s+(-?\d+)\s+(\d+)", re.M)
INP_SCAN = re.compile(r"^\s*([BAD])\s+([\d ]+?)\s*=", re.M)
INP_XYZ = re.compile(r"^\*\s*xyz\s+(-?\d+)\s+(\d+)", re.M)


def head(p, n=80000):          # the input echo is near the top of an ORCA output
    with open(p, errors="ignore") as f:
        return f.read(n)


def main():
    work = os.path.abspath(sys.argv[1])
    jobs = [l.strip() for l in open(os.path.join(work, sys.argv[2])) if l.strip()]
    refs = set(sys.argv[3:])
    if refs:
        jobs = [d for d in jobs if d.split("/")[1] in refs]
    want_dirs = set(jobs)
    rp = os.path.join(work, "autopilot", "audit_reviewed.txt")
    reviewed = {l.split()[0]: l.strip() for l in open(rp) if l.strip() and not l.startswith("#")} if os.path.exists(rp) else {}
    problems = collections.defaultdict(list)
    bad = set()
    checked = 0
    for d in jobs:
        full = os.path.join(work, d)
        outs = [p for p in [os.path.join(full, "scan.out"), os.path.join(full, "scan_cont.out")]
                + glob.glob(os.path.join(full, "scan_try*.out")) if os.path.exists(p)]
        if not outs:
            continue
        inp = os.path.join(full, "scan_orig.inp")
        if not os.path.exists(inp):
            inp = os.path.join(full, "scan.inp")
        t = open(inp, errors="ignore").read()
        m, x = INP_SCAN.search(t), INP_XYZ.search(t)
        want = (m.group(1), m.group(2).split()) if m else None
        cm = (x.group(1), x.group(2)) if x else None
        for p in outs:
            h = head(p)
            if "INPUT FILE" not in h:
                continue          # stitched scan.out holds only steps; its parts are checked separately
            checked += 1
            e = ECHO_SCAN.search(h) or ECHO_CONS.search(h)
            ex = ECHO_XYZ.search(h)
            got = (e.group(1), e.group(2).split()) if e else None
            if got != want:
                bad.add(d.split("/")[1])
                problems["identity"].append("%s: coordinate %s in %s, folder input has %s" % (d, got, os.path.basename(p), want))
            if ex and (ex.group(1), ex.group(2)) != cm:
                bad.add(d.split("/")[1])
                problems["identity"].append("%s: charge/mult %s in %s, folder input has %s" % (d, ex.groups(), os.path.basename(p), cm))
    # overlapping runs of the same folder, from the start and end lines of the run logs
    runs = collections.defaultdict(list)
    for lg in glob.glob(os.path.join(work, "logs", "scan*_*.log")):
        t = open(lg, errors="ignore").read()
        s = re.search(r"^(scans/\S+) start (\S+ \S+)", t, re.M)
        if not s or s.group(1) not in want_dirs:
            continue
        e = re.search(r"^scans/\S+ end (\S+ \S+)", t, re.M)
        t0 = time.mktime(time.strptime(s.group(2), "%Y-%m-%d %H:%M:%S"))
        t1 = time.mktime(time.strptime(e.group(1), "%Y-%m-%d %H:%M:%S")) if e else float("inf")
        runs[s.group(1)].append((t0, t1, os.path.basename(lg)))
    for d, rs in runs.items():
        rs.sort()
        for a, b in zip(rs, rs[1:]):
            if b[0] < a[1]:
                if d in reviewed:
                    problems["reviewed"].append("%s: %s and %s ran at the same time (%s)" % (d, a[2], b[2], reviewed[d]))
                    continue
                bad.add(d.split("/")[1])
                problems["overlap"].append("%s: %s and %s ran at the same time" % (d, a[2], b[2]))
    # queues
    pend = {}
    for q in glob.glob(os.path.join(work, "queue", "*", "tasks.txt")):
        pool = os.path.basename(os.path.dirname(q))
        tasks = [l.strip() for l in open(q) if l.strip()]
        n = int(open(os.path.join(os.path.dirname(q), "next")).read())
        for d, c in collections.Counter(tasks[n:]).items():
            if c > 1:
                bad.add("ALL")
                problems["queue"].append("%s pending %d times in %s" % (d, c, pool))
        pend[pool] = set(tasks)
    if len(pend) > 1:
        a, b = list(pend.values())[:2]
        for d in sorted(a & b):
            bad.add("ALL")
            problems["queue"].append("%s is in both pools" % d)
    print("audit: %d ORCA outputs checked against their folder input, %d folders with run logs, %d runs logged"
          % (checked, len(runs), sum(len(r) for r in runs.values())))
    for k in ("identity", "overlap", "queue"):
        print("  %-8s %d problems" % (k, len(problems[k])))
        for line in problems[k][:20]:
            print("    " + line)
    if problems["reviewed"]:
        print("  reviewed %d overlaps examined earlier and found harmless (not counted)" % len(problems["reviewed"]))
    if os.environ.get("AUDIT_BAD"):
        open(os.environ["AUDIT_BAD"], "w").write("".join(r + "\n" for r in sorted(bad)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
