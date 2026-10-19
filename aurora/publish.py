#!/usr/bin/env python3
"""Publish the validated scan points of finished complexes into the results folder (a checkout
of the aurora-results branch).

Usage (inside the run folder, after aurora/audit.py reported no problems):
    python3 <repo>/aurora/publish.py . scans/jobs_scan_full.txt <results folder>

A complex is published once, when every one of its branches has terminated normally. Its points
go through scans/validate.py; only passing geometries are written:
  scan_points/<REF>.xyz   one frame per passing point (same comment line as scans/export_points.py)
  validation/<REF>.csv    the validate.py row of every point, passing or not, with the reason
  coords/<REF>.json       the scanned coordinates (scans/<REF>/coords.json)
  summary.csv             one line per published complex
  LOWER_MINIMA.md         complexes where a branch fell more than 2 kJ/mol below its start
                          (energy_drop): a lower minimum than stage 2, to be listed for Riti
A finished complex with no passing branch start is not published; it is listed in FLAGGED.md.
Standard library only, Python 3.6+.
"""
import sys, os, csv, json, shutil, subprocess, collections, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scans"))
import validate as V  # noqa: E402

OK = "ORCA TERMINATED NORMALLY"
SUMMARY = ["ref", "natoms", "branches", "points", "pass", "first_fail_reasons", "published"]


def done(p):
    try:
        with open(p, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 4096))
            return OK in f.read().decode(errors="ignore")
    except OSError:
        return False


def main():
    work, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[3])
    jobs = [l.strip() for l in open(os.path.join(work, sys.argv[2])) if l.strip()]
    by = collections.defaultdict(list)
    for d in jobs:
        by[d.split("/")[1]].append(d)
    for sub in ("scan_points", "validation", "coords"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    sp = os.path.join(out, "summary.csv")
    summary = list(csv.DictReader(open(sp))) if os.path.exists(sp) else []
    flagged_p = os.path.join(out, "FLAGGED.md")
    flagged = [l for l in open(flagged_p).read().split("\n") if l.startswith("- ")] if os.path.exists(flagged_p) else []
    lower_p = os.path.join(out, "LOWER_MINIMA.md")
    lower = [l for l in open(lower_p).read().split("\n") if l.startswith("- ")] if os.path.exists(lower_p) else []
    seen = {r["ref"] for r in summary} | {l.split()[1] for l in flagged}
    new = sorted(r for r, ds in by.items() if r not in seen and all(done(os.path.join(work, d, "scan.out")) for d in ds))
    if not new:
        print("publish: no newly finished complexes")
        return
    lst = os.path.join(work, "lists", "publish_batch.txt")
    open(lst, "w").write("\n".join(new) + "\n")
    subprocess.check_call([sys.executable, os.path.join(os.path.dirname(HERE), "scans", "validate.py"), work,
                           "lists/publish_batch.txt", "publish_batch"], stdout=subprocess.DEVNULL)
    rows = collections.defaultdict(list)
    for r in csv.DictReader(open(os.path.join(work, "scans", "validation_publish_batch.csv"))):
        rows[r["ref"]].append(r)
    stamp = time.strftime("%Y-%m-%d")
    n_new = n_pts = 0
    for ref in new:
        rs = rows[ref]
        drops = [r for r in rs if r["status"] == "energy_drop" and r["E_rel_kJ"] not in ("", None) and float(r["E_rel_kJ"]) < -2.0]
        if drops:
            lower.append("- %s: %s" % (ref, "; ".join("%s %s step %s at %s kJ/mol" % (r["coord"], r["branch"], r["step"], r["E_rel_kJ"]) for r in drops)))
        nat = int(open(os.path.join(work, "stage2_b3lyp", ref, ref + ".xyz")).readline())
        starts = [r for r in rs if float(r["offset"]) == 0.0]
        reasons = collections.Counter(r["status"] for r in rs if r["status"] not in ("pass", "after_fail"))
        if not any(r["status"] == "pass" for r in starts):
            flagged.append("- %s (%d atoms): all %d branches finished, but no branch start passes validation (%s); not published"
                           % (ref, nat, len(by[ref]), ", ".join("%s %d" % kv for kv in reasons.most_common())))
            continue
        C = json.load(open(os.path.join(work, "scans", ref, "coords.json")))
        dirs = {(c["name"], c["branch"]): c["dir"] for c in C["coords"]}
        cache, frames = {}, []
        for r in rs:
            if r["status"] != "pass":
                continue
            d = dirs[(r["coord"], r["branch"])]
            if d not in cache:
                cache[d] = V.parse_steps(open(os.path.join(work, d, "scan.out"), errors="ignore").read(), nat)
            conv, E, A = cache[d][int(r["step"])]
            frames.append("%d\n%s %s %s step=%s offset=%s value=%s E_rel_kJ=%s E_h=%.8f\n%s" % (
                nat, ref, r["coord"], r["branch"], r["step"], r["offset"], r["value"], r["E_rel_kJ"], E,
                "\n".join("%-2s %12.6f %12.6f %12.6f" % a for a in A)))
        open(os.path.join(out, "scan_points", ref + ".xyz"), "w").write("\n".join(frames) + "\n")
        with open(os.path.join(out, "validation", ref + ".csv"), "w") as f:
            w = csv.DictWriter(f, fieldnames=list(rs[0].keys()))
            w.writeheader()
            w.writerows(rs)
        shutil.copy(os.path.join(work, "scans", ref, "coords.json"), os.path.join(out, "coords", ref + ".json"))
        summary.append(dict(ref=ref, natoms=nat, branches=len(by[ref]), points=len(rs), **{"pass": len(frames)},
                            first_fail_reasons=";".join("%s:%d" % kv for kv in reasons.most_common()), published=stamp))
        n_new += 1
        n_pts += len(frames)
    summary.sort(key=lambda r: r["ref"])
    with open(sp, "w") as f:
        w = csv.DictWriter(f, fieldnames=SUMMARY)
        w.writeheader()
        w.writerows(summary)
    if lower:
        open(lower_p, "w").write("# Complexes with a lower minimum than stage 2\n\nA scan branch fell more than 2 kJ/mol below "
                                 "its start (`energy_drop` in validation), so the complex has a lower minimum than the "
                                 "stage-2 geometry. Points past the drop are not published.\n\n" + "\n".join(sorted(set(lower))) + "\n")
    if flagged:
        open(flagged_p, "w").write("# Finished complexes not published\n\nThese complexes finished every branch, but "
                                   "validation rejects their branch starts, so no point is usable as defined. They need a "
                                   "decision (for example a donor list that includes the extra Zn contact).\n\n"
                                   + "\n".join(sorted(set(flagged))) + "\n")
    print("publish: %d complexes added (%d passing points), %d flagged; %d complexes and %d points published in total"
          % (n_new, n_pts, len([f for f in flagged if f.split()[1] in new]), len(summary), sum(int(r["pass"]) for r in summary)))


if __name__ == "__main__":
    main()
