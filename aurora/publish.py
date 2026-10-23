#!/usr/bin/env python3
"""Publish the validated scan points of finished complexes into the results folder (a checkout of
the aurora-results branch), in exactly the layout of scans/export_points.py (scan_results/).

Usage (inside the run folder, after aurora/audit.py reported no problems):
    python3 <repo>/aurora/publish.py . scans/jobs_scan_full.txt <results folder>

A complex is published once, when every one of its branches has terminated normally. Its points
go through scans/validate.py; only passing geometries are written:
  scan_results/<REF>.xyz                 one frame per passing point (export_points.py format)
  scan_results/validation_scan_full.csv  the validate.py rows of the published complexes
  scan_results/coords/<REF>.json         the scanned coordinates (scans/<REF>/coords.json)
and README.md lists the published complexes, the complexes with a lower minimum than stage 2
(an energy_drop more than 2 kJ/mol below a branch start, the list nersc/README.md asks for), and
finished complexes not exported because no branch start passes. What has been handled is kept in
<run folder>/autopilot/published.json, outside git. Standard library only, Python 3.6+.
"""
import sys, os, csv, json, shutil, subprocess, collections, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scans"))
import validate as V  # noqa: E402

OK = "ORCA TERMINATED NORMALLY"
TAG = "scan_full"


def done(p):
    try:
        with open(p, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 4096))
            return OK in f.read().decode(errors="ignore")
    except OSError:
        return False


def readme(state):
    pub = sorted(r for r, s in state.items() if s["status"] == "published")
    lines = [
        "# Zn relaxed-scan results from ALCF Aurora", "",
        "`scan_results/` is the export of `scans/export_points.py` (the `scan_results.tar.gz` of `nersc/README.md`), "
        "added complex by complex as each finishes on Aurora. Code and run log: branch `aurora`, `aurora/README.md`.", "",
        "- `scan_results/<REF>.xyz`: one frame per point that passes `scans/validate.py`; comment line "
        "`REF coordinate branch step= offset= value= E_rel_kJ= E_h=`",
        "- `scan_results/validation_%s.csv`: the `validate.py` row of every point of the published complexes" % TAG,
        "- `scan_results/coords/<REF>.json`: the scanned coordinates", "",
        "A complex is added when all its branches have terminated normally and `aurora/audit.py` finds no problem "
        "(every ORCA output matches its own folder's input; no folder run twice at once).", "",
        "## Published (%d complexes, %d points)" % (len(pub), sum(state[r]["pass"] for r in pub)), "",
        "| Complex | Atoms | Branches | Points | Passing | Published |", "|---|---|---|---|---|---|"]
    lines += ["| %s | %d | %d | %d | %d | %s |" % (r, state[r]["natoms"], state[r]["branches"], state[r]["points"],
                                                   state[r]["pass"], state[r]["date"]) for r in pub]
    low = sorted(r for r, s in state.items() if s.get("drops"))
    lines += ["", "## Lower minimum than stage 2", "",
              "A branch fell more than 2 kJ/mol below its start (`energy_drop`), so the complex has a lower minimum "
              "than the stage-2 geometry; points past the drop are not exported.", ""]
    lines += ["- %s: %s" % (r, "; ".join(state[r]["drops"])) for r in low] or ["None so far."]
    bad = sorted(r for r, s in state.items() if s["status"] == "not_exported")
    lines += ["", "## Finished but not exported", "",
              "No branch start passes validation, so no point is usable as defined (for example a non-donor atom "
              "within 2.6 A of Zn at the stage-2 minimum).", ""]
    lines += ["- %s: %s" % (r, state[r]["reason"]) for r in bad] or ["None so far."]
    return "\n".join(lines) + "\n"


def main():
    work, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[3])
    jobs = [l.strip() for l in open(os.path.join(work, sys.argv[2])) if l.strip()]
    by = collections.defaultdict(list)
    for d in jobs:
        by[d.split("/")[1]].append(d)
    sr = os.path.join(out, "scan_results")
    os.makedirs(os.path.join(sr, "coords"), exist_ok=True)
    sp = os.path.join(work, "autopilot", "published.json")
    state = json.load(open(sp)) if os.path.exists(sp) else {}
    new = sorted(r for r, ds in by.items() if r not in state and all(done(os.path.join(work, d, "scan.out")) for d in ds))
    if "--pending" in sys.argv:          # print the complexes ready to publish (go.sh audits those); exit 3 if none
        print(" ".join(new))
        sys.exit(0 if new else 3)
    if os.environ.get("PUBLISH_REFS") is not None:   # only the complexes the audit passed
        ok = set(os.environ["PUBLISH_REFS"].split())
        new = [r for r in new if r in ok]
    if not new:
        print("publish: no newly finished complexes")
        return
    open(os.path.join(work, "lists", "publish_batch.txt"), "w").write("\n".join(new) + "\n")
    subprocess.check_call([sys.executable, os.path.join(os.path.dirname(HERE), "scans", "validate.py"), work,
                           "lists/publish_batch.txt", "publish_batch"], stdout=subprocess.DEVNULL)
    rows = collections.defaultdict(list)
    for r in csv.DictReader(open(os.path.join(work, "scans", "validation_publish_batch.csv"))):
        rows[r["ref"]].append(r)
    vp = os.path.join(sr, "validation_%s.csv" % TAG)
    stamp, n_pts, added = time.strftime("%Y-%m-%d"), 0, []
    for ref in new:
        rs = rows[ref]
        nat = int(open(os.path.join(work, "stage2_b3lyp", ref, ref + ".xyz")).readline())
        reasons = collections.Counter(r["status"] for r in rs if r["status"] not in ("pass", "after_fail"))
        drops = ["%s %s step %s at %s kJ/mol" % (r["coord"], r["branch"], r["step"], r["E_rel_kJ"]) for r in rs
                 if r["status"] == "energy_drop" and r["E_rel_kJ"] not in ("", None) and float(r["E_rel_kJ"]) < -2.0]
        if not any(r["status"] == "pass" for r in rs if float(r["offset"]) == 0.0):
            state[ref] = dict(status="not_exported", natoms=nat, branches=len(by[ref]), date=stamp, drops=drops,
                              reason="all %d branches finished; branch starts fail validation (%s)"
                                     % (len(by[ref]), ", ".join("%s %d" % kv for kv in reasons.most_common())))
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
        open(os.path.join(sr, ref + ".xyz"), "w").write("\n".join(frames) + "\n")
        shutil.copy(os.path.join(work, "scans", ref, "coords.json"), os.path.join(sr, "coords", ref + ".json"))
        first = not os.path.exists(vp)
        with open(vp, "a") as f:
            w = csv.DictWriter(f, fieldnames=list(rs[0].keys()))
            if first:
                w.writeheader()
            w.writerows(rs)
        state[ref] = dict(status="published", natoms=nat, branches=len(by[ref]), points=len(rs), date=stamp,
                          drops=drops, **{"pass": len(frames)})
        added.append(ref)
        n_pts += len(frames)
    json.dump(state, open(sp, "w"), indent=1)
    open(os.path.join(out, "README.md"), "w").write(readme(state))
    print("publish: %d complexes added (%d passing points), %d not exported; %d complexes published in total"
          % (len(added), n_pts, len(new) - len(added), sum(1 for s in state.values() if s["status"] == "published")))


if __name__ == "__main__":
    main()
