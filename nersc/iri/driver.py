#!/usr/bin/env python3
"""Runs the Zn big-pool branches on NERSC Perlmutter from an Aurora login node.

    python3 driver.py            # loop forever (run in `screen -S zn_nersc`)
    python3 driver.py --once     # one cycle
    touch ~/dev/iri/nersc_run/PAUSE   # stop submitting (running jobs continue)

Each branch of the complexes in $WORK/remote_refs.txt runs as one Slurm job in the shared QOS
(8 cores, 48 h; aurora/../nersc_run/pm_branch.sh). Every cycle the driver
  - reads the state of our jobs (IRI compute/status),
  - for each ended job reads its branch log: finished -> copied back; time limit -> resubmitted;
    a failure -> resubmitted at most MAX_FAIL times, then left for review,
  - submits branches that have no job,
  - every COPY_EVERY seconds copies the finished branches' scan.out and scan_acc.txt back into the
    Aurora run folder with Globus (the usual audit and publication pick them up there).
A branch never has two jobs: the state file records its job, and pm_branch.sh also takes the
folder's lock. State: state.json; log: driver.log.
"""
import os, sys, json, time, base64
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.expanduser("~/dev/iri/iri_team_bundle"))
import iridriver as I  # noqa: E402
import globus_sdk  # noqa: E402

_tok = {"t": None, "exp": 0}
_get_token = I.get_token


def _cached_token():
    """the IRI token from token_manager.py, kept until 10 min before it expires"""
    if not _tok["t"] or time.time() > _tok["exp"] - 600:
        _tok["t"] = _get_token()
        try:
            d = json.load(open(os.path.expanduser("~/.globus/auth_tokens.json")))
            exp = [o.get("expires_at_seconds") for o in d.get("other_tokens", []) if "iri_api" in o.get("scope", "")]
            _tok["exp"] = int(exp[0]) if exp and exp[0] else time.time() + 3600
        except Exception:
            _tok["exp"] = time.time() + 3600
    return _tok["t"]


I.get_token = _cached_token

WORK = "/lus/flare/projects/ModCon/dsokaras/zn_scans"
T = "/pscratch/sd/d/dsokaras/zn_nersc"
R = T + "/run"
ACCOUNT = os.environ.get("NERSC_ACCOUNT", "m5268")
ALCF, NERSC = "f39a7a0f-5bfc-46ce-9615-ba9f8592814f", "6bdc7956-fc0f-4ad2-989c-7aa5ee643a79"
WALL = 48 * 3600 - 60
LIMIT = WALL - 1800          # ORCA stops 30 min before the walltime (stitch and clean-up)
MAX_FAIL, COPY_EVERY, CYCLE = 2, 1800, 600
STATE, LOG = os.path.join(HERE, "state.json"), os.path.join(HERE, "driver.log")


def log(msg):
    with open(LOG, "a") as f:
        f.write("[%s] %s\n" % (time.strftime("%F %T"), msg))


def transfer_client():
    tok = json.load(open(os.path.expanduser("~/.globus/transfer_tokens.json")))
    c = globus_sdk.NativeAppAuthClient("fae5c579-490a-4d76-b6eb-d78f65caeb63")
    t = tok["transfer.api.globus.org"]
    return globus_sdk.TransferClient(authorizer=globus_sdk.RefreshTokenAuthorizer(
        t["refresh_token"], c, access_token=t["access_token"], expires_at=t["expires_at_seconds"]))


def text(path):
    s = I.download_text("scratch", path)
    try:
        return base64.b64decode(s, validate=True).decode("utf-8", "replace")
    except Exception:
        return s


def branches():
    refs = set(l.split()[0] for l in open(os.path.join(WORK, "remote_refs.txt")) if l.strip() and not l.startswith("#"))
    out = []
    for d in (l.strip() for l in open(os.path.join(WORK, "scans/jobs_scan_full.txt")) if l.strip()):
        if d.split("/")[1] in refs:
            out.append(d)
    return out


def submit(d):
    name = "zn_" + d.split("/", 1)[1].replace("/", "__")
    p = {"name": name[:120], "executable": "/bin/bash", "arguments": [T + "/code/pm_branch.sh", d, str(LIMIT)],
         "directory": R, "stdout_path": R + "/logs/slurm_%j.out", "stderr_path": R + "/logs/slurm_%j.out",
         "inherit_environment": True,
         "resources": {"node_count": 1, "process_count": 1, "processes_per_node": 1, "cpu_cores_per_process": 16,
                       "exclusive_node_use": False, "memory": 30 * 1024 ** 3},
         "attributes": {"duration": WALL, "queue_name": "shared", "account": ACCOUNT,
                        "custom_attributes": {"constraint": "cpu"}}}
    return I.submit_compute_job("compute", p)


def job_states(ids):
    """state of each of our job ids (the job-list endpoint returns every user's jobs, so ask per job)"""
    from concurrent.futures import ThreadPoolExecutor

    def one(jid):
        try:
            return jid, ((I._get("/compute/status/compute/%s" % jid).get("status") or {}).get("state") or "").lower()
        except Exception:
            return jid, "unknown"
    with ThreadPoolExecutor(10) as ex:
        return dict(ex.map(one, ids))


ENDED = {"completed", "failed", "canceled", "cancelled", "timeout", "timed_out", "node_fail", "out_of_memory"}


def cycle(st, tc):
    paused = os.path.exists(os.path.join(HERE, "PAUSE"))
    active = {b: s["job"] for b, s in st.items() if s.get("job") and not s.get("ended")}
    states = job_states(list(active.values())) if active else {}
    for b, jid in active.items():
        if states.get(jid) not in ENDED:
            continue
        s = st[b]
        s["ended"] = True
        try:
            lg = text("%s/logs/%s_%s.log" % (R, b.replace("/", "_"), jid))
        except Exception as e:
            lg = "no log (%s)" % str(e)[:80]
        if "finished" in lg:
            s["done"] = True
            log("%s finished (job %s)" % (b, jid))
        elif "DUE TO TIME LIMIT" in lg:
            s["stops"] = s.get("stops", 0) + 1
            log("%s stopped at the time limit (job %s); continues" % (b, jid))
        else:
            s["fails"] = s.get("fails", 0) + 1
            log("%s FAILED (job %s, state %s): %s" % (b, jid, states.get(jid), lg.strip().splitlines()[-1:] if lg.strip() else ""))
    n = 0
    for b, s in sorted(st.items()):
        if paused or s.get("done") or s.get("fails", 0) > MAX_FAIL or (s.get("job") and not s.get("ended")):
            continue
        try:
            jid = str(submit(b))
        except Exception as e:
            log("submit %s failed: %s" % (b, str(e)[:200]))
            break
        s.update(job=jid, ended=False, submits=s.get("submits", 0) + 1)
        n += 1
    if n:
        log("submitted %d jobs" % n)
    # copy finished branches back to Aurora
    if time.time() - st.get("_last_copy", {}).get("t", 0) >= COPY_EVERY:
        todo = [b for b, s in st.items() if not b.startswith("_") and s.get("done") and not s.get("back")]
        if todo:
            td = globus_sdk.TransferData(source_endpoint=NERSC, destination_endpoint=ALCF, label="zn big results back",
                                         sync_level="checksum", verify_checksum=True)
            for b in todo:
                for f in ("scan.out", "scan_acc.txt"):
                    td.add_item("%s/%s/%s" % (R, b, f), "/ModCon/dsokaras/zn_scans/%s/%s" % (b, f))
            tid = tc.submit_transfer(td)["task_id"]
            tc.task_wait(tid, timeout=3000, polling_interval=20)
            res = tc.get_task(tid)
            if res["status"] == "SUCCEEDED":
                for b in todo:
                    st[b]["back"] = True
            log("copied %d finished branches back to Aurora: %s" % (len(todo), res["status"]))
        st["_last_copy"] = {"t": time.time()}
    run = sum(1 for b, s in st.items() if not b.startswith("_") and s.get("job") and not s.get("ended"))
    done = sum(1 for b, s in st.items() if not b.startswith("_") and s.get("done"))
    bad = [b for b, s in st.items() if not b.startswith("_") and s.get("fails", 0) > MAX_FAIL]
    back = sum(1 for b, s in st.items() if not b.startswith("_") and s.get("back"))
    log("status: %d jobs queued/running, %d branches finished (%d back on Aurora), %d need review"
        % (run, done, back, len(bad)))
    write_status(st, states, run, done, back, bad)


def write_status(st, states, run, done, back, bad):
    """the NERSC part of aurora/STATUS.md (status.sh includes $WORK/nersc_status.md)"""
    bs = [b for b in st if not b.startswith("_")]
    running = sum(1 for b in bs if st[b].get("job") and not st[b].get("ended") and states.get(st[b]["job"]) in ("active", "running"))
    queued = run - running
    by = {}
    for b in bs:
        r = b.split("/")[1]
        by.setdefault(r, [0, 0])
        by[r][1] += 1
        by[r][0] += 1 if st[b].get("done") else 0
    try:
        used = None
        for p in I._get("/account/projects"):
            if p["name"] == ACCOUNT:
                for a in I._get("/account/projects/%s/project_allocations" % p["id"]):
                    if a["entries"][0]["unit"] == "node_hours" and "cpu" in (a.get("capability_uri") or ""):
                        ua = I._get("/account/projects/%s/project_allocations/%s/user_allocations" % (p["id"], a["id"]))
                        e = ua[0]["entries"][0]
                        used = "%.0f of your %.0f CPU node-hours on %s used" % (e["usage"], e["allocation"], ACCOUNT)
    except Exception:
        used = None
    L = ["## NERSC Perlmutter (big pool)", "",
         "The %d unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), "
         "driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others." % len(by), "",
         "```",
         "branches: %d finished (%d copied back to Aurora), %d running, %d queued, %d need review, %d total" % (done, back, running, queued, len(bad), len(bs)),
         "stops at the 48 h limit so far: %d; failed runs: %d" % (sum(st[b].get("stops", 0) for b in bs), sum(st[b].get("fails", 0) for b in bs))]
    if used:
        L.append(used)
    L += ["```", "", "| Complex | Branches finished |", "|---|---|"]
    L += ["| %s | %d / %d |" % (r, d, n) for r, (d, n) in sorted(by.items())]
    L += ["", "Last driver actions:", "", "```"] + open(LOG).read().splitlines()[-8:] + ["```"]
    tmp = os.path.join(WORK, "nersc_status.md.new")
    open(tmp, "w").write("\n".join(L) + "\n")
    os.replace(tmp, os.path.join(WORK, "nersc_status.md"))


def main():
    st = json.load(open(STATE)) if os.path.exists(STATE) else {}
    for b in branches():
        st.setdefault(b, {})
    tc = transfer_client()
    log("driver started (%d branches, account %s)" % (sum(1 for k in st if not k.startswith("_")), ACCOUNT))
    while True:
        try:
            cycle(st, tc)
        except Exception as e:
            log("cycle error: %s" % str(e)[:300])
        tmp = STATE + ".new"
        json.dump(st, open(tmp, "w"), indent=0)
        os.replace(tmp, STATE)
        if "--once" in sys.argv:
            break
        time.sleep(CYCLE)


if __name__ == "__main__":
    main()
