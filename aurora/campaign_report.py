#!/usr/bin/env python3
"""Write the campaign report of the Zn relaxed scans (Markdown) for Riti and her agent.

Usage:
    python3 aurora/campaign_report.py <run_dir> [<results dir>] > aurora/CAMPAIGN_REPORT.md

<run_dir> is the Aurora run folder ($WORK); it is only read. <results dir> is a checkout of the
aurora-results branch (default: ../XANES2EXAFS-results next to this repository). The data-driven
parts come from autopilot/published.json, remote_refs.txt, scans/jobs_scan_full.txt,
scans/<REF>/coords.json, queue/main and the published validation_scan_full.csv; the hand-written
parts come from aurora/campaign_report_notes.md (sections marked <!-- name -->), included verbatim.
Branch progress of unfinished complexes is read from the tails of their scan.out files (about 30
small reads per complex). If the NERSC driver state (env NERSC_STATE, default
~/dev/iri/nersc_run/state.json) is readable, the branches run on Perlmutter are counted per complex.
Standard library only, Python 3.6+.
"""
import sys, os, re, csv, json, time, statistics, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "scans"))
import zncore as Z  # noqa: E402
OK = "ORCA TERMINATED NORMALLY"
FAILS = ("not_converged", "constraint", "bonds", "shell", "new_contact", "energy_cap", "energy_drop", "jump",
         "ref_mismatch")
LOW_PASS = 75.0     # % below which a complex is listed for attention
LOWER = -2.0        # kJ/mol below the branch start that counts as a lower minimum


def load_notes(path):
    """{section name: text} from the notes file, split at lines '<!-- name -->'."""
    notes, name, buf = {}, None, []
    for line in open(path):
        m = re.match(r"^<!--\s*([\w-]+)\s*-->\s*$", line)
        if m:
            if name:
                notes[name] = "".join(buf).strip("\n")
            name, buf = m.group(1), []
        elif name:
            buf.append(line)
    if name:
        notes[name] = "".join(buf).strip("\n")
    return notes


def tail_done(p):
    try:
        with open(p, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 4096))
            return OK in f.read().decode(errors="ignore")
    except OSError:
        return False


def remote_refs(run):
    """{REF: NERSC account} from remote_refs.txt (no account column means m5268, the driver default)."""
    out = {}
    p = os.path.join(run, "remote_refs.txt")
    if os.path.exists(p):
        for line in open(p):
            s = line.split("#")[0].split()
            if s:
                out[s[0]] = s[1] if len(s) > 1 else "m5268"
    return out


def nersc_branches(path):
    """{REF: branches that had at least one Perlmutter job} from the NERSC driver state, or None."""
    try:
        st = json.load(open(path))
    except (OSError, ValueError):
        return None
    c = collections.Counter()
    for d, v in st.items():
        if d.count("/") >= 2 and isinstance(v, dict) and "job" in v:
            c[d.split("/")[1]] += 1
    return c


def riti_notes(readme):
    """[(date, text)]: the Run-log (and setup) passages addressed to Riti, verbatim; operational sentences
    after a 'For Riti:' passage (NERSC/Aurora status) are cut."""
    stop = re.compile(r"^(NERSC|Aurora|New |Branches:|The \d+ whole-node|UDODOG stays|Autopilot|Farm|Progress)")
    out = []
    for line in open(readme):
        if not line.startswith("- ") or not re.search(r"\bRiti\b", line):
            continue
        m = re.match(r"^- (20\d\d-\d\d-\d\d(?: \d\d:\d\d(?:-\d\d:\d\d)?)?)[^:]*?:\s*(.*)$", line.rstrip("\n"))
        date, text = (m.group(1), m.group(2)) if m else ("setup note", line[2:].rstrip("\n"))
        sents = re.split(r"(?<=[.)])\s+(?=[A-Z(])", text)
        k = next((n for n, x in enumerate(sents) if re.search(r"\bfor Riti[:,]", x, re.I)), None)
        if k is not None:
            x = sents[k]
            keep = [x[re.search(r"\bfor Riti[:,]", x, re.I).start():]]
            for x in sents[k + 1:]:
                if stop.match(x):
                    break
                keep.append(x)
            out.append((date, " ".join(keep)))
            continue
        for n, x in enumerate(sents):
            if re.search(r"\bRiti\b", x) and "no new notes" not in x and "her agent" not in x:
                out.append((date, (sents[n - 1] + " " + x) if x.startswith("Riti:") and n else x))
    return out


def shell_check(run, refs, coords):
    """[(REF, findings)] for complexes whose stage-2 Zn shell disagrees with the donor list (validate.py
    limits: non-donor heavy atom < 2.6 A fails every branch start, 2.6-2.8 A is at risk; donor > 2.8 A fails
    every start), plus crystal contacts between the curation cut-off (2.53 A for N/O) and 2.6 A."""
    cdir = os.path.join(REPO, "structures", "dft_ready_xyz")
    out = []
    for ref in refs:
        S = Z.read_xyz(os.path.join(run, "stage2_b3lyp", ref, ref + ".xyz"))
        zn, don = coords[ref]["zn"], coords[ref]["donors"]
        f = []
        for i in range(len(S)):
            if i == zn or S[i][0] == "H":
                continue
            d = Z.dist(S[zn], S[i])
            if i in don and d > 2.6:
                f.append("donor %s%d at %.3f%s" % (S[i][0], i, d, " (> 2.8: fails every start)" if d > 2.8 else ""))
            elif i not in don and d < 2.8:
                f.append("non-donor %s%d at %.3f%s" % (S[i][0], i, d, " (< 2.6: fails every start)" if d < 2.6 else ""))
        cx = os.path.join(cdir, ref + ".xyz")
        if os.path.exists(cx):
            X = Z.read_xyz(cx)
            if len(X) == len(S) and all(a[0] == b[0] for a, b in zip(X, S)):
                for i in range(len(X)):
                    if i != zn and i not in don and X[i][0] != "H" and 2.53 <= Z.dist(X[zn], X[i]) < 2.6:
                        f.append("crystal: non-donor %s%d at %.3f" % (X[i][0], i, Z.dist(X[zn], X[i])))
        if f:
            out.append((ref, f))
    return out


def fmt_counter(c, n=3):
    return ", ".join("%s %d" % kv for kv in c.most_common(n)) or "-"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(x) for x in r) + " |" for r in rows]
    return "\n".join(out)


def main():
    run = os.path.abspath(sys.argv[1])
    res = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(os.path.dirname(REPO), "XANES2EXAFS-results")
    notes = load_notes(os.path.join(HERE, "campaign_report_notes.md"))
    N = lambda k: notes.get(k, "*(notes section `%s` missing)*" % k)

    jobs = [l.strip() for l in open(os.path.join(run, "scans", "jobs_scan_full.txt")) if l.strip()]
    by = collections.defaultdict(list)
    for d in jobs:
        by[d.split("/")[1]].append(d)
    state = json.load(open(os.path.join(run, "autopilot", "published.json")))
    remote = remote_refs(run)
    nb = nersc_branches(os.environ.get("NERSC_STATE", os.path.expanduser("~/dev/iri/nersc_run/state.json")))

    coords, planned = {}, {}
    for ref in by:
        coords[ref] = json.load(open(os.path.join(run, "scans", ref, "coords.json")))
        planned[ref] = sum(c["npoints"] for c in coords[ref]["coords"])
    natoms = {}
    for ref in by:
        natoms[ref] = state[ref]["natoms"] if ref in state else int(
            open(os.path.join(run, "stage2_b3lyp", ref, ref + ".xyz")).readline())
    done = {}
    for ref in by:
        done[ref] = len(by[ref]) if ref in state else sum(tail_done(os.path.join(run, d, "scan.out")) for d in by[ref])

    qd = os.path.join(run, "queue", "main")
    try:
        ntask = sum(1 for _ in open(os.path.join(qd, "tasks.txt")))
        nxt = int(open(os.path.join(qd, "next")).read().split()[0])
        qpend, qact = max(0, ntask - nxt), len(os.listdir(os.path.join(qd, "active")))
    except (OSError, ValueError, IndexError):
        qpend = qact = None

    rows = collections.defaultdict(list)
    vcsv = os.path.join(res, "scan_results", "validation_scan_full.csv")
    for r in csv.DictReader(open(vcsv)):
        rows[r["ref"]].append(r)

    pub = sorted(r for r in by if state.get(r, {}).get("status") == "published")
    nex = sorted(r for r in by if state.get(r, {}).get("status") == "not_exported")
    inp = sorted(r for r in by if r not in state)
    allrows = [r for ref in pub for r in rows[ref]]
    npts, npass = len(allrows), sum(r["status"] == "pass" for r in allrows)
    first = collections.Counter(r["status"] for r in allrows if r["status"] in FAILS)
    n_after = sum(r["status"] == "after_fail" for r in allrows)

    # per complex: first-failure reasons, lower minima (any first failure below the branch start)
    reason, lowmin, stepinfo = {}, {}, {}
    for ref in pub:
        rs = rows[ref]
        reason[ref] = collections.Counter(r["status"] for r in rs if r["status"] in FAILS)
        lowmin[ref] = sorted([r for r in rs if r["status"] in FAILS and r["E_rel_kJ"] not in ("", None)
                              and float(r["E_rel_kJ"]) < LOWER], key=lambda r: float(r["E_rel_kJ"]))
        ff = [r for r in rs if r["status"] in FAILS]
        stepinfo[ref] = (statistics.median(int(r["step"]) for r in ff) if ff else None,
                         statistics.median(float(r["E_rel_kJ"]) for r in ff if r["E_rel_kJ"] != "") if ff else None)

    def site(ref):
        if ref not in remote:
            return "Aurora"
        s = "Aurora + NERSC %s" % remote[ref]
        if nb is not None:
            s += " (%d/%d br.)" % (nb[ref], len(by[ref]))
        return s

    now = time.strftime("%Y-%m-%d %H:%M %Z")
    total_planned = sum(planned.values())
    br_done = sum(done.values())
    out = []
    P = out.append
    P("# Zn relaxed-scan campaign: report for Riti Sarangi (SSRL)")
    P("")
    P("Generated %s by `aurora/campaign_report.py` from the run folder `%s` and the results checkout `%s` "
      "(branch `aurora-results`). Rebuild with `python3 aurora/campaign_report.py %s > aurora/CAMPAIGN_REPORT.md`. "
      "Hand-written sections come from `aurora/campaign_report_notes.md`. Numbers in tables are computed; "
      "statements marked *(inference)* are interpretation." % (now, run, res, run))
    P("")
    P("## Summary")
    P("")
    P("Relaxed one-coordinate scans (B3LYP-D3(BJ), def2-TZVP on Zn and donors, def2-SVP elsewhere, RIJCOSX, "
      "CPCM(water), ORCA 6.0.1) around the stage-2 minima of **%d Zn complexes**: %s scan branches, %s planned points "
      "(constrained optimisations, two branch starts per coordinate included). %s of %s branches have terminated "
      "normally (%.1f%%). **%d complexes are published** on `aurora-results` (%s points validated, **%s pass**, "
      "**%.1f%%**); **%d finished complexes are not exported** (every branch start fails validation: the stage-2 "
      "minimum has a different Zn first shell than the donor list); **%d complexes are still running** "
      "(%s of their %s branches done%s). %d published complexes fall below their stage-2 energy by more than 2 kJ/mol "
      "in some branch, and %d pass fewer than %.0f%% of their points; both lists are below."
      % (len(by), "{:,}".format(len(jobs)), "{:,}".format(total_planned), "{:,}".format(br_done),
         "{:,}".format(len(jobs)), 100.0 * br_done / len(jobs), len(pub), "{:,}".format(npts), "{:,}".format(npass),
         100.0 * npass / max(npts, 1), len(nex), len(inp), "{:,}".format(sum(done[r] for r in inp)),
         "{:,}".format(sum(len(by[r]) for r in inp)),
         "" if qpend is None else "; Aurora `main` queue: %d pending, %d running" % (qpend, qact),
         sum(1 for r in pub if lowmin[r]),
         sum(1 for r in pub if 100.0 * sum(x["status"] == "pass" for x in rows[r]) / len(rows[r]) < LOW_PASS),
         LOW_PASS))
    P("")
    P(table(["", "Complexes", "Branches", "Points", "Passing"], [
        ["Published", len(pub), "{:,}".format(sum(len(by[r]) for r in pub)), "{:,}".format(npts), "{:,}".format(npass)],
        ["Not exported", len(nex), sum(len(by[r]) for r in nex), "{:,}".format(sum(planned[r] for r in nex)), 0],
        ["In progress", len(inp), "%s (%s done)" % ("{:,}".format(sum(len(by[r]) for r in inp)),
                                                     "{:,}".format(sum(done[r] for r in inp))),
         "{:,}".format(sum(planned[r] for r in inp)), "-"],
        ["Total", len(by), "{:,}".format(len(jobs)), "{:,}".format(total_planned), "{:,}".format(npass)]]))
    P("")
    P(N("summary"))
    P("")
    P(N("method"))
    P("")
    P("### Complexes run (fully or partly) on NERSC Perlmutter")
    P("")
    P("From `remote_refs.txt`; branch counts from the NERSC driver state%s. Every complex listed started on Aurora; "
      "branches that had already finished there before the move are not counted, and the moved branches continued "
      "from their Aurora files." % ("" if nb is not None else " (not readable here)"))
    P("")
    P(table(["Complex", "Atoms", "Account", "Branches with a Perlmutter job", "Status"],
            [[r, natoms[r], remote[r], ("%d / %d" % (nb[r], len(by[r]))) if nb is not None else "-",
              state[r]["status"] + " " + state[r]["date"] if r in state else "in progress (%d/%d done)" % (done[r], len(by[r]))]
             for r in sorted(remote, key=lambda x: (remote[x], x))]))
    P("")
    P(N("validation"))
    P("")
    P("### First failures over all published points")
    P("")
    P("Each branch has at most one first failure; every later point of that branch is `after_fail`.")
    P("")
    P(table(["Status", "Points", "Share of published points"],
            [["pass", "{:,}".format(npass), "%.1f%%" % (100.0 * npass / npts)]] +
            [[k, v, "%.2f%%" % (100.0 * v / npts)] for k, v in first.most_common()] +
            [["after_fail", "{:,}".format(n_after), "%.1f%%" % (100.0 * n_after / npts)]] +
            [[k, 0, "-"] for k in FAILS if k not in first]))
    P("")
    P("### Pass rate by coordinate type and branch (published complexes)")
    P("")
    agg = collections.defaultdict(lambda: [0, 0, collections.Counter()])
    for r in allrows:
        a = agg[(r["type"], r["branch"])]
        a[0] += r["status"] == "pass"
        a[1] += 1
        if r["status"] in FAILS:
            a[2][r["status"]] += 1
    P(table(["Coordinate", "Branch", "Points", "Pass", "Pass %", "First failures"],
            [[k[0], k[1], "{:,}".format(v[1]), "{:,}".format(v[0]), "%.1f" % (100.0 * v[0] / v[1]), fmt_counter(v[2], 4)]
             for k, v in sorted(agg.items())]))
    P("")
    jl = collections.Counter()
    for ref in pub:
        brs = collections.defaultdict(list)
        for r in rows[ref]:
            brs[(r["coord"], r["branch"])].append(r)
        for rs in brs.values():
            f = [r["status"] for r in rs if r["status"] in FAILS]
            if f:
                jl[f[0]] += sum(r["status"] in (f[0], "after_fail") for r in rs)
    P("Points lost per first-failure type (the failing point plus the `after_fail` points behind it): %s."
      % ", ".join("%s %s" % (k, "{:,}".format(v)) for k, v in jl.most_common()))
    P("")
    P("## Per-complex table")
    P("")
    P("All %d complexes, by name. *Points*: validated points (published) or planned points (otherwise). *First failures*: "
      "counts of the first failing point per branch (`after_fail` points not counted). *Below start*: branches whose "
      "first failure lies more than 2 kJ/mol below the branch start (any reason; `energy_drop` ones are the README "
      "list), with the lowest E_rel in kJ/mol. *Site*: NERSC account and number of branches that had a Perlmutter job. "
      "*Date*: publication date (`published.json`)." % len(by))
    P("")
    trows = []
    for ref in sorted(by):
        s = state.get(ref)
        if s and s["status"] == "published":
            rs = rows[ref]
            p = sum(r["status"] == "pass" for r in rs)
            lm = lowmin[ref]
            trows.append([ref, "published", natoms[ref], len(by[ref]), len(rs), p, "%.1f" % (100.0 * p / len(rs)),
                          fmt_counter(reason[ref]), sum(r["status"] == "after_fail" for r in rs),
                          ("%d (%s)" % (len(lm), lm[0]["E_rel_kJ"])) if lm else "-", site(ref), s["date"]])
        elif s:
            m = re.search(r"\((.*)\)", s.get("reason", ""))
            trows.append([ref, "**not exported**", natoms[ref], len(by[ref]), planned[ref], 0, "0.0",
                          "branch starts: " + (m.group(1) if m else "-"), "-", "-", site(ref), s["date"]])
        else:
            trows.append([ref, "in progress (%d/%d br.)" % (done[ref], len(by[ref])), natoms[ref], len(by[ref]),
                          planned[ref], "-", "-", "-", "-", "-", site(ref), "-"])
    P(table(["Complex", "Status", "Atoms", "Branches", "Points", "Pass", "Pass %", "First failures", "after_fail",
             "Below start", "Site", "Date"], trows))
    P("")
    P("## Complexes that need Riti's attention")
    P("")
    P(N("attention"))
    P("")
    P("### (a) Finished but not exported")
    P("")
    P(table(["Complex", "Atoms", "Branches", "Planned points", "Reason recorded by publish.py", "Finished", "Site"],
            [[r, natoms[r], len(by[r]), planned[r], state[r]["reason"], state[r]["date"], site(r)] for r in nex]))
    P("")
    P(N("not_exported"))
    P("")
    P("### (b) Lower minimum than the stage-2 geometry")
    P("")
    P("Every published complex with at least one branch whose first failing point lies more than 2 kJ/mol below the "
      "branch start. *energy_drop* = flagged as such (the results README list); *structural* = the drop came with a "
      "`shell`, `new_contact` or `jump` failure, so it is not in the README list. E_rel is relative to the branch start, "
      "which reproduces the stage-2 minimum (within 0.5 kJ/mol and 0.05 A, else `ref_mismatch`).")
    P("")
    lrows = []
    for ref in sorted(pub, key=lambda r: float(lowmin[r][0]["E_rel_kJ"]) if lowmin[r] else 0):
        lm = lowmin[ref]
        if not lm:
            continue
        p = sum(r["status"] == "pass" for r in rows[ref])
        lrows.append([ref, len(lm), lm[0]["E_rel_kJ"], "%s %s step %s (%s)" % (lm[0]["coord"], lm[0]["branch"],
                                                                                lm[0]["step"], lm[0]["status"]),
                      fmt_counter(collections.Counter("energy_drop" if r["status"] == "energy_drop" else "structural"
                                                      for r in lm), 2), "%d/%d" % (p, len(rows[ref]))])
    P(table(["Complex", "Branches below start", "Lowest E_rel (kJ/mol)", "Where", "Kind", "Pass"], lrows))
    P("")
    P("All branches below start (coordinate, branch, step of the first failure, E_rel kJ/mol, status):")
    P("")
    for ref in sorted(pub):
        if lowmin[ref]:
            P("- **%s**: %s" % (ref, "; ".join("%s %s %s %s (%s)" % (r["coord"], r["branch"], r["step"], r["E_rel_kJ"],
                                                                     r["status"]) for r in
                                                 sorted(lowmin[ref], key=lambda r: (r["coord"], r["branch"])))))
    P("")
    P(N("lower_minima"))
    P("")
    P("### (c) Pass rate below %.0f%%" % LOW_PASS)
    P("")
    P("*Median first-failure step* and *median E_rel at first failure* help tell soft modes (early, near 0 kJ/mol) "
      "from lower minima (negative) and from the ends of stiff scans (late, positive).")
    P("")
    crows = []
    for ref in pub:
        rs = rows[ref]
        p = sum(r["status"] == "pass" for r in rs)
        if 100.0 * p / len(rs) < LOW_PASS:
            st, e = stepinfo[ref]
            crows.append((100.0 * p / len(rs), [ref, natoms[ref], "%d/%d" % (p, len(rs)), "%.1f" % (100.0 * p / len(rs)),
                                                 fmt_counter(reason[ref], 4), "-" if st is None else "%g" % st,
                                                 "-" if e is None else "%.1f" % e, site(ref)]))
    P(table(["Complex", "Atoms", "Pass", "Pass %", "First failures", "Median first-failure step",
             "Median E_rel at first failure", "Site"], [x[1] for x in sorted(crows)]))
    P("")
    P(N("low_pass"))
    P("")
    P("### (d) Non-converged optimisation steps")
    P("")
    nc = [(r["ref"], r["coord"], r["branch"], r["step"]) for r in allrows if r["status"] == "not_converged"]
    P("`not_converged` first failures among the published points: **%d**%s." %
      (len(nc), "" if not nc else " (" + "; ".join("%s %s %s step %s" % x for x in nc) + ")"))
    P("")
    P(N("nonconverged"))
    P("")
    P("### (e) Branch starts that miss the stage-2 minimum (`ref_mismatch`)")
    P("")
    rm = [r for r in allrows if r["status"] == "ref_mismatch"]
    P(table(["Complex", "Coordinate", "Branch", "Points lost (incl. after_fail)"],
            [[r["ref"], r["coord"], r["branch"], sum(1 for x in rows[r["ref"]] if x["coord"] == r["coord"] and
                                                      x["branch"] == r["branch"])] for r in rm]) if rm else "None.")
    P("")
    P(N("ref_mismatch"))
    P("")
    P("### (f) Stage-2 Zn shell versus the donor list, all complexes")
    P("")
    P("Computed from `stage2_b3lyp/<REF>/<REF>.xyz` and the donors in `scans/<REF>/coords.json` (= the `.meta` "
      "donors), with the `validate.py` limits; the crystal column uses `structures/dft_ready_xyz/` from this repository. "
      "Listed: any non-donor heavy atom within 2.8 A of Zn, any donor beyond 2.6 A, and any crystal non-donor contact "
      "between the curation cut-off for N/O (2.53 A) and the 2.6 A validation limit. Carbon contacts of 2.6-2.8 A are "
      "usually the ipso/ring carbons of the donor's own ring (*inference*); O, N, S, F, Cl and Br contacts are the ones "
      "to look at.")
    P("")
    sc = shell_check(run, sorted(by), coords)
    P(table(["Complex", "Status", "Findings (atom index 0-based, distance to Zn in A)"],
            [[r, state[r]["status"] if r in state else "in progress (%d/%d br.)" % (done[r], len(by[r])), "; ".join(f)]
             for r, f in sc]))
    P("")
    P(N("shell_check"))
    P("")
    P("### (g) Every Run-log note addressed to Riti")
    P("")
    P("Verbatim from `aurora/README.md` (Run log and setup notes), oldest first.")
    P("")
    for d, t in riti_notes(os.path.join(HERE, "README.md")):
        P("- %s: %s" % (d, t))
    P("")
    P(N("decisions"))
    P("")
    P(N("where"))
    P("")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
