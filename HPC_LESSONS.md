# Running large ORCA campaigns on ALCF Aurora and NERSC Perlmutter: lessons learned

Written 2026-10-25, during the Zn relaxed-scan campaign (338 complexes, 10,175 scan branches, ~92,600
constrained optimisations, ORCA 6.0.1) that ran on Aurora from 2026-10-17 and on Perlmutter from
2026-10-25. The day-by-day record is the Run log in `aurora/README.md`; the scripts are in `aurora/`,
`nersc/iri/` and `scans/`. Read this before planning a new campaign, and add to it when you learn
something new.

## Scope: which calculations these lessons fit

They were learned on **many independent, restartable, single-node ORCA jobs**: relaxed surface scans
(B3LYP-D3(BJ), def2-SVP/TZVP, RIJCOSX, CPCM, TightOpt) of 30-200-atom complexes, 4-16 cores and
1.5-3 GB per rank, minutes to hours per optimisation, each branch able to continue from its last
geometry. Throughput mattered; no single job was large.

Other ORCA work needs its own checks:
- **One large calculation** (CCSD(T)/DLPNO on big systems, large TDDFT or XAS/ROCIS, CASSCF/NEVPT2,
  analytic Hessians): memory per rank, scratch I/O volume and whole-node or multi-node parallel scaling
  dominate. Benchmark one job at several core counts; packing many jobs per node may not help.
- **Jobs that cannot be restarted** (numerical frequencies, long single points): the walltime has to fit
  the job, so the short-walltime strategy below does not apply as is.
- **Very short jobs** (seconds each): process start-up and file-system load dominate; batch many
  inputs per ORCA task.
- Anything else: re-run the benchmark in `aurora/bench/` (or `nersc/iri/pm_bench.sh`) before choosing a layout.

## Planning (day 0)

1. **Check the allocation end date and the storage quota of every project you will use.** The `isaac`
   allocation ended on 2026-10-22; its file-system quota then dropped to 1 MB and **writes failed
   silently**: ORCA outputs were truncated with no error in the job. That cost a storage migration,
   quarantining one farm's output and rebuilding 373 branches. Move to the next project before the
   end date, and check the quota (`myquota`, `sbank-list-allocations`) in the status page.
2. **Estimate the work in node-hours and count it in points, not only branches.** A branch counts as
   finished only when its whole scan is done: on day 2 almost every branch had converged points while
   only 1.5% of branches were finished. A points count gives the true rate and shows a stall early.
3. **Plan the endgame from the start** (see "The last 30%" below), including which part goes to a
   second facility.
4. **Use both facilities from the start when you have them.** The 18 largest complexes were the
   long tail; moving them to Perlmutter on day 0 instead of at 70% would have run them alongside
   everything else.

## Validate before production

- **Benchmark the layout on one full node** with the median-cost molecule. On Aurora, 24 ORCA jobs x 4
  cores per node did 21% more work than 6 x 16; node-local `/tmp` scratch +4%; hyperthreading +2%;
  HBM 0% (`aurora/README.md`, "Layout"). For throughput, many small jobs beat few wide ones.
- **Use the same ORCA build at every site** (we checked the archive's SHA-256) and **check that a few
  branches reproduce across sites** before moving work: Perlmutter reproduced Aurora to 0.009 kJ/mol
  and 0.007 A.
- **Run a debug-queue test farm before every new kind of farm**, including its end-of-run steps
  (stopping ORCA at the deadline, handing stopped branches back to the queue). Several bugs only
  appeared at full scale (see "Things that went wrong"); a 16-node dress rehearsal of the
  end-of-run steps would have caught some of them.

## Aurora (PBS)

- **Request 6 h, not 12 h.** Priority grows with eligible time squared and falls with requested
  walltime cubed, so a 12 h request has about 1/8 the priority of a 6 h one. With stop-and-continue,
  a 6 h farm loses only a few percent to restarts. The only 12 h farm of this campaign was the slowest
  to start.
- **Big farms set the pace.** `capacity` allows 2 running jobs of up to 16 nodes per user (32 nodes),
  so most of the throughput comes from 256-node farms in `prod`/`small`: 6,490 of the 8,621 Aurora
  node-hours to 2026-10-25, and +900 to +3,750 finished branches on days with a 256-node farm against
  +100 to +200 on days with only 16-node farms. Their start time is unpredictable (5 minutes to 2.8
  days here), and eligible time only accrues while a job waits, so **keep one or two big farms
  queued without gaps from day 0** while there is work to fill them; submit the next one when the
  previous one starts, not when it ends.
- `qhold`/`qrls` keep a job's eligible time; use a hold to stop a queued farm from starting into an
  empty queue. `qalter -A <project>` moves a queued job to another project and kept its eligible time.
  `qalter -v` is not supported.
- **Leave a margin for the hand-back.** At the end of a 256-node farm, preparing ~6,000 stopped
  branches for continuation took 24-26 min on a busy Lustre; one farm was killed at its walltime in the
  middle of it. Farms of 64 nodes or more now stop ORCA 50 min before the walltime (`MARGIN_MIN`).
- **A big farm needs enough work.** A 256-node farm has 6,144 slots of 4 cores. With fewer pending
  branches, nodes sit idle but are charged (115 and ~250 idle node-hours in two farms). Mixed farms
  (`node.sh`) give the spare nodes to another pool; the autopilot submits a 256-node farm only while
  more than 3,000 branches are pending.

## Perlmutter (Slurm, driven through the NERSC IRI API)

- **Charging:** use `shared` (charged by cores used), `regular` or `debug` (normal charge). Never use
  `premium` (charged at a multiple) for a campaign. A pending reason of `Priority` is Slurm's reason
  code, not a QOS.
- **Speed:** a Perlmutter CPU node (2 x EPYC 7763, 128 cores) does 1.25-1.33x the work of an Aurora node;
  one branch runs at the same speed on both.
- **`shared` QOS:** one job per branch (8 physical cores = 16 CPUs, 30 GB, 48 h). About 40 of 495 jobs
  started at once at first; whole-node `regular` jobs with 16 branches each are an alternative, but a
  node is charged until its slowest branch ends.
- **Crashes in `shared`:** about 2% of branch jobs died with a segmentation fault in
  `orca_startup_mpi`, minutes to hours into a run; none in whole-node jobs and none on Aurora. Moving
  ORCA scratch from `/tmp` (memory, counted against the job) to `$PSCRATCH` and lowering `%maxcore`
  did not stop them. Each crash costs one step plus a new wait, because the branch continues from its
  last geometry, so we resubmit (up to 3 failures) rather than pay for whole nodes. Root cause not found.
- **OpenMPI 4.1.6** for ORCA 6.0.1 builds on Perlmutter only with its internal hwloc, PMIx and libevent
  (`nersc/iri/pm_install.sh`).
- **IRI API** (`api.iri.nersc.gov`), from an Aurora login node:
  - login is a two-step PKCE flow, and the tokens need an `expires_at` stamp or refreshes race;
  - uploads are limited to 5 MB; scratch downloads come back base64-encoded;
  - the job list returns every user's jobs, so poll your own jobs one by one;
  - log times are Pacific;
  - deploy a script by uploading `name.new` and renaming it (atomic), never by overwriting it in place.
- **Globus Transfer** for results (ALCF `dtn_flare` and the NERSC Perlmutter collection, with linked
  identities). A missing source file makes a transfer retry until its deadline and blocks anything
  waiting on it: add only files that exist (a branch finished in one run has no `scan_acc.txt`).

## The last 30%

- When the pending work falls below one big farm's slots, every big farm leaves nodes idle, and
  Aurora's `small` queue has nothing under 256 nodes. Plan for this point: shift to 16-node farms,
  give spare nodes to another pool (mixed farms), or move the remaining work to another site.
- The largest molecules finish last. Give them more cores per job (we used 8 instead of 4) and start
  them first, or run them at a second site from the beginning.
- Sites with per-core charging (`shared` on Perlmutter) suit a thinning tail: nothing is charged for
  idle cores while the last branches finish.

## Running it unattended

- **Run from a frozen copy of the scripts** (`$WORK/.repo/<time>`), so a `git pull` never changes a
  running farm. Replace files atomically, and restart the autopilot only when it is idle.
- **One branch, one runner:** a per-folder `flock`, a check that no output is still growing before a
  restart, and a snapshot of the queue length before adding continuations. Without them one branch
  (UDODOG) ran twice at once.
- **One place that knows what runs where:** `remote_refs.txt` lists the complexes on the other site,
  and every Aurora tool skips them, so no branch runs at both sites.
- **Audit before publishing**, and publish a complex only when all its branches ended normally.
  Audit only what is about to be published (a full audit took 57 min while holding the queue lock).
- **Keep a human-readable record:** the Run log in `aurora/README.md` (dated, one line per event),
  `aurora/STATUS.md` regenerated every 2 h, and hourly check-ins (autopilot alive, alerts, farms,
  failures without a time-limit or cancel tag).
- **Watch for silence as well as errors:** a driver that stops logging is as bad as one that fails
  (a blocked Globus transfer froze the NERSC driver for 15 min).

## Things that went wrong, and the fix

| What happened | Fix |
|---|---|
| Allocation ended; quota cut to 1 MB; writes failed silently | moved to the new project and storage; quarantined and rebuilt affected branches; check end dates and quotas on day 0 |
| `rsync --exclude scans/` also skipped nested `scans/` folders | recopied; anchor exclude patterns (`--exclude /scans/`) |
| A branch ran twice at once | per-folder lock, busy check, queue-length snapshot |
| 256-node farm killed at walltime while handing back branches | 50 min margin for farms of 64+ nodes |
| Full audit held the publish lock for 57 min | audit only the complexes about to be published |
| 12 h farm request waited longest | 6 h requests |
| Perlmutter `shared` jobs segfault (~2%) | resubmit from the last geometry; whole-node jobs as fallback |
| Globus transfer stuck on a missing file | copy `scan_acc.txt` only if it exists |
