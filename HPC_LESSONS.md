# Running ORCA campaigns on ALCF Aurora and NERSC Perlmutter

Instructions for an agent or person starting a large ORCA campaign on these machines. They distil
everything learned in the Zn relaxed-scan campaign (338 complexes, 10,175 scan branches, ~92,600
constrained optimisations, ORCA 6.0.1, Aurora and Perlmutter, from October 2026 on). This file is kept
current: when a rule changes, the rule is rewritten here, not appended as history. The chronological
record of the campaign is the Run log in `aurora/README.md`; the scripts are in `aurora/`,
`nersc/iri/` and `scans/`. The campaign was run by an AI agent within ISAAC (Integrated Scientific Agentic
AI for Catalysis), largely unattended, so these rules are written for an agent to follow as much as
for a person. The section *Running a campaign with an agent* describes how that operation is set up.

## When these instructions apply

They fit **many independent, restartable, single-node ORCA jobs**: geometry optimisations and relaxed
scans with hybrid DFT (here B3LYP-D3(BJ), def2-SVP/TZVP, RIJCOSX, CPCM, TightOpt) on 30-200-atom
molecules, 4-16 cores and 1.5-3 GB per rank, minutes to hours per optimisation, each job able to
continue from its last geometry. The goal is throughput.

Check them again for other work:
- **One large calculation** (DLPNO/CCSD(T) on big systems, large TDDFT or XAS/ROCIS, CASSCF/NEVPT2,
  analytic Hessians): memory per rank, scratch I/O and parallel scaling dominate. Benchmark one job at
  several core counts; packing many jobs per node may not pay.
- **Jobs that cannot be restarted** (numerical frequencies, long single points): the walltime must fit
  the whole job, so the short-walltime rule below needs care.
- **Very short jobs** (seconds each): start-up and file-system load dominate; run many inputs per task.

## Before the first production job

1. **Ask which allocations are cheap and which are precious, and plan around it.** Here the standing
   Aurora project (ModCon) could be spent freely, so speed beat efficiency there (idle nodes in a
   farm, extra farms queued, small farms released early), while isaac and the NERSC projects, shared
   by a group until the yearly reset, had to be protected with hard caps and the user's approval.
2. **Check every project's allocation end date and storage quota.** After an allocation ends, its
   storage quota can drop to almost nothing, and writes then fail silently: ORCA outputs are cut off
   with no error. Move to the next project and folder before the end date, and show quota and balance
   (`myquota`, `sbank-list-allocations`) on the status page.
3. **Estimate the total in node-hours, and measure progress in finished points (optimisations), not
   only finished branches.** A branch counts only when its whole scan is done, so branch counts lag
   far behind the real work early on.
4. **Benchmark the layout on one full node** with the median-cost molecule (`aurora/bench/`,
   `nersc/iri/pm_bench.sh`). For throughput, many narrow jobs beat few wide ones: on Aurora 24 jobs x
   4 cores per node did 21% more work than 6 x 16. Node-local scratch helped a little (+4%),
   hyperthreading barely (+2%), HBM not at all.
5. **Use the same ORCA build everywhere** (compare the archive's SHA-256) and **reproduce a few jobs at
   each new site** before moving work there. Agreement should be about 0.01 kJ/mol and 0.01 A.
6. **Run a short test farm in a debug queue before every new kind of production job**, including its
   end-of-run steps (stopping ORCA before the walltime, handing unfinished jobs back to the queue).
7. **Split the work by cost, and size the cores by the time one step takes.** Each scan step starts
   from the previous one, so a branch's wall time is (steps) x (time per step), and the largest
   molecules set the campaign's end date. Measure one constrained optimisation per complex first. Here
   ~140 atoms / ~1,400 basis functions (def2-SVP) took 9-15 h per step on 8 cores (30-50 optimisation
   cycles), so an 11-step branch needed 4-6 days. Give such molecules 16-32 cores per job from day one
   (fewer node-hours per step are lost to poor scaling than days are lost to the tail), keep 4 cores
   for the rest, start the largest first, or send them to a second site from day one.
8. **Check every optimised starting structure before scanning it.** Compare the donor list with the
   atoms actually near the metal (within about 2.8 A) at the reference minimum. In this campaign six of
   338 complexes had changed coordination during the reference optimisation (weak crystal contacts at
   2.5-3.1 A pulled in to bonds, one ligand switched binding atom). Every point of their 30 branches
   then failed validation, and that compute was wasted.
9. **Use every facility you have from the start, and judge a site by how soon jobs start, not by its
   size.** For many small restartable jobs, a site where each job starts within minutes (Perlmutter
   `shared` here) finishes sooner than a much larger machine where the project's priority is low and
   large jobs wait for days (Aurora with a discretionary award here: about 85% of the work, but in
   bursts with days of idle queue between). Adding a second site late helps less than running both
   in parallel from day one. Know each project's priority class and balance before planning, and ask
   for a priority boost, a reservation or more hours in the first days, not after two weeks.

## Aurora (PBS)

- **Project priority decides most of the wait.** PBS orders jobs by roughly
  eligible_time^2 / walltime^3 x project_priority x nodes, with walltime clamped to 6-12 h. Most queued
  work carries project_priority 25; discretionary projects (ModCon, isaac here) carry 2, so their
  256-node jobs start only when the machine is quiet. When the end date matters, ask ALCF support
  early for a temporary priority boost or a reservation (for example 256 nodes x 12 h), and ask the
  allocation program for an award with a higher priority; nothing in the job script matters as much.
- **A large job starts when the nodes are free for its whole walltime, so keep short ones queued.**
  On a busy machine PBS plans the top-priority jobs ahead and starts any other job only if enough
  nodes are free from now until its walltime ends. Priority decides the order; the walltime decides
  whether a job fits at all. Here a 256-node farm of 4 h started after 42 h in the queue while the
  12 h farm, with 326 h of eligible time and about 8 times its priority score, still had "Not enough
  free nodes available" after two weeks. Earlier 6 h farms started after 5 min to 67 h, a 4 h farm
  after 13 h. Rules: never queue only long farms; keep a 4 h and a 6 h 256-node farm queued at all
  times (the autopilot keeps one of at most `SHORT_HOURS` = 4 h); a 12 h farm is at most an extra.
  Below about 3 h a farm is not worth it: the end-of-run hand-back takes 25-50 min on 256 nodes, and
  every restart loses the optimiser's history.
- **Never cancel a farm that has waited long, and never let the queue of large farms lapse.** Eligible
  time counts squared in the priority and is lost on cancel; `qhold` keeps it. From Oct 24 to Oct 30
  the only 256-node farm queued was a 12 h one, because the autopilot submitted new ones only when the
  queue could fill all 6,144 slots; that week was mostly lost on Aurora. Farms now size their slots at
  start (`AUTO_CORES`), so a small queue is no reason to stop submitting.
- **Read the PBS comment before guessing.** `qstat -f <job> | grep comment`: "Not enough free nodes
  available" means waiting for a fitting gap (shorter walltime helps); "Job would conflict with
  reservation or top job" means it would overlap a reservation or a planned job (shorter helps, or wait);
  "would exceed overall limit on resource nodect in queue" or "Insufficient amount of resource:
  at_queue" mean the queue itself is full or limited by the admins (often before a maintenance): only
  waiting helps. `pbs_rstat` lists reservations; a job must end before a full-machine one starts.
- **Throughput comes from 256-node farms.** `capacity` allows 2 running jobs of up to 16 nodes per
  user, so most of the node-hours come from `prod` (routed to `small`, 256 nodes and up). Their start is
  unpredictable (minutes to days), and priority only grows while a job waits, so **keep one or two
  256-node farms queued at all times while there is work to fill them**: submit the next one when the
  previous one starts, not when it ends. With several large farms queued for one pool,
  `aurora/bigpair.sh` holds the others while one runs and releases them when it ends.
- **Keep both `capacity` slots busy** (2 running jobs per user, 16 nodes each): queue two 16-node farms,
  not one, so the second slot is not idle while the first farm hands back (autopilot `WANT_MAIN_CAP=2`).
- **Hold the small farms while a large one has taken the whole queue.** When a 256-node farm starts on
  fewer branches than it has slots, a 16-node farm starting next would find nothing to run: `qhold` it
  until the large farm hands its branches back, then `qrls`.
- **Match a farm's slots to the queue when it starts, not when it is submitted.** A 256-node farm has
  6,144 slots at 4 cores; idle nodes in a running farm are charged. Farms take `AUTO_CORES=1`
  (`sites/aurora.sh`): at start they give each branch 4, 6, 8, 12 or 16 cores so the slots roughly
  match the branches waiting, which also makes each branch faster in the tail (12 cores: 2,048 slots;
  16 cores: 1,536). With even less work, use 16-node farms or another site.
- **Send the last few dozen slow branches to a site that runs one long job per branch.** The end of a
  campaign is a tail of the hardest branches (largest molecules, many attempts), each needing several
  more hours of compute. On Aurora every 6 h farm run then costs a 4-6 h queue wait and a restart, and
  a maintenance can add days; on Perlmutter one shared-QOS job per branch (48 h) runs straight
  through for a few node-hours in total. Check how many points each branch still needs (`scan_acc.txt`
  against the scan's step count) and move them once the work left needs more than one farm run.
- **A queued job runs the scripts of its own snapshot** (`$WORK/.repo/<time>`), however old. When a rule
  changes (a new list of complexes run elsewhere, a new layout), update the snapshots of queued jobs
  too, or they will start with the old behaviour.
- **Leave time for the end-of-run hand-back, and keep a backup for when it runs out.** Preparing stopped
  jobs for continuation takes 20-30 min for thousands of jobs, and on a slow Lustre even a few hundred
  can take longer than 25 min. Farms of 64 nodes or more stop ORCA 50 min before the walltime
  (`MARGIN_MIN`); smaller farms keep 25 min, and when one is killed mid-hand-back the autopilot's
  re-queue (`NODES=0 go.sh submit`) recovers its branches. Never rely on the margin alone.
- **Never re-read every log on each check.** Late in a campaign the log directory holds ~50,000 files and
  a full `grep` over them takes 10+ min on a busy Lustre (it made the autopilot's cycle about an hour).
  Keep a cache of each log's verdict and read only logs newer than the last check (`find -newer
  <stamp>`, about a minute).
- `qhold`/`qrls` and `qalter -A <project>` keep a queued job's eligible time. Hold queued farms rather
  than letting them start into an empty queue. `qalter -v` is not supported.
- Production reads ORCA and OpenMPI from `/lus/flare`, not `$HOME`; set `OPAL_PREFIX`.

## Perlmutter (Slurm, through the NERSC IRI API)

- **Charging:** use `shared` (charged per core used), `regular` or `debug`. Never use `premium` (a
  charge multiple) for a campaign. A pending reason `Priority` is Slurm's reason code, not a QOS.
- **Check the project's balance before moving work, and cap what the driver may spend.** NERSC
  projects are shared by their members: here m2464 had 1,900 of 29,500 CPU node-hours left and m5268
  1,600 of 39,800. The IRI API reports them (`/account/projects/<id>/project_allocations`). A job
  still running when its project hits zero is killed. `driver.py` takes the account per complex from
  the second column of `remote_refs.txt` and caps each account (`BUDGET`: no new jobs; `CUTOFF`:
  running jobs cancelled), counting each shared job as 1/16 node from submission.
  Size a batch by its worst case, not by steps: N branches submitted together can each run their
  full walltime, so a batch can cost N x walltime x 1/16 node-hours before any finishes (128 branches
  x 48 h = 384 node-hours), however few steps they have left. Decide up front whether reaching the cap
  should cancel running jobs (they lose the step in progress) or only stop new submissions.
- **Speed:** a CPU node (2 x EPYC 7763, 128 cores) does 1.25-1.33x the work of an Aurora node; a
  single job runs at the same speed on both.
- **Layout:** one `shared` job per branch (8 physical cores = 16 CPUs, 30 GB, 48 h). `shared` charges
  nothing for idle cores, which suits a thinning tail. Avoid packing branches into whole-node
  `regular` jobs (16 branches x 8 cores): the node is charged until its slowest branch ends, a slot
  whose branch finishes or crashes stays idle, and a crash is seen and resubmitted only when the whole
  job ends (here up to 25 h later). If you must pack, have the node job refill its own slots.
- **OpenMPI 4.1.6** for ORCA 6.0.1 builds only with its internal hwloc, PMIx and libevent
  (`nersc/iri/pm_install.sh`). It also detects Cray XPMEM and uses it for single copies between ranks
  by default, and with XPMEM about 2% of runs die at random with a segmentation fault in
  `vader_return_registration`. **Always set `OMPI_MCA_btl_vader_single_copy_mechanism=cma`** (Linux CMA;
  results unchanged). Check with `ompi_info --param btl vader --level 9 | grep single_copy`.
- Keep ORCA scratch on `$PSCRATCH` in `shared` jobs (`/tmp` is memory and counts against the job).
- Resubmit a crashed branch automatically from its last geometry (up to 3 tries), but **read the
  backtrace of the first crashes before calling them random**: the frames name the library at fault.
- **IRI API** (`api.iri.nersc.gov`), driven from an Aurora login node (`nersc/iri/driver.py`):
  - login is a two-step PKCE flow; stamp tokens with `expires_at`, or refreshes race;
  - uploads are limited to 5 MB, and scratch downloads come back base64-encoded;
  - the job list returns every user's jobs: poll your own jobs one by one;
  - times in NERSC logs are Pacific;
  - deploy a script by uploading `name.new` and renaming it, never by overwriting it in place.
  - file reads fail now and then: when a job's log cannot be read, read it again next cycle (up to
    3 times) rather than counting the run as a failure.
- **Globus Transfer** moves results (ALCF `dtn_flare`, NERSC Perlmutter collection; link the identities
  first). A missing source file makes a transfer retry until its deadline and blocks whatever waits on
  it, so add only files that exist (a branch finished in one run has no `scan_acc.txt`).
- **The ALCF Globus collection needs a recent login with an ALCF identity.** When that session lapses
  (here after about a week), transfers fail with "None of your authenticated identities are from
  domains allowed by resource policies" (403, LOGIN_DENIED). Only a person can renew it (browser, ALCF
  MFA): `nersc/iri/globus_login.py url`, then `code <CODE>`, then restart the driver. Watch for this
  error and ask the user at once; results wait safely at NERSC meanwhile.

## Running unattended

- **Run from a frozen copy of the scripts** (`$WORK/.repo/<time>`) so `git pull` never changes a running
  job. Replace files atomically; restart the autopilot only when it is idle.
- **One job per folder at a time:** a per-folder `flock`, a check that no output is still growing
  before a restart, and a snapshot of the queue length before adding continuations.
- **One list says which work runs where** (`remote_refs.txt`); every tool at the other site skips it.
  Move work between sites by whole complex, under the same locks the farms and the autopilot use,
  and only while no farm is running it.
- **Audit before publishing** (each output matches its folder's input, nothing ran twice), audit only
  what is about to be published, and publish a complex only when all its branches ended normally.
- **A problem in one item must not stop the rest.** Hold back the item with the problem and carry on
  with the others; check that a script running with `set -e` does not quit on a checker's non-zero
  exit (one complex with an audit finding once blocked every publication).
- **Watch for silence as well as errors.** A driver or farm that stops logging is as bad as one that
  fails; alert on a stale log, not only on error lines.

## Running a campaign with an agent

This campaign ran for more than two weeks with an AI coding agent (Claude Code) in charge day and
night, with the user away for most of it. What made that work:

**Layers.** Routine work is done by plain scripts that need no agent; the agent watches them, handles
what they cannot, and talks to the user.

| Layer | Runs | Does |
|---|---|---|
| Farms (`aurora/farm.pbs`, `node.sh`) | PBS jobs | run branches, stop before the walltime, hand stopped branches back |
| Autopilot (`aurora/autopilot.sh`) | `screen -S zn_autopilot`, 10-min cycle | re-queue after farm ends (backup), keep farms queued, publish finished complexes, push `STATUS.md` |
| NERSC driver (`nersc/iri/driver.py`) | `screen -S zn_nersc`, 10-min cycle | one Slurm job per branch, resubmit at the time limit, copy results back, per-account budget caps |
| Pair watcher (`aurora/bigpair.sh`) | `screen -S zn_bigpair` | never let two 256-node farms run at once |
| Watchdog (`aurora/watchdog.sh`) | `screen -S zn_watchdog`, 5-min cycle | restart the agent and any of the scripts above if its screen is gone |
| Agent (Claude Code) | `screen` on a login node: `claude --continue --remote-control <name>` | events, hourly check-ins, diagnosis, fixes, decisions, records |

**The agent's session.**
- Start it inside `screen` on a login node, so it outlives the user's connection. `--continue` resumes
  the conversation after a restart. `--remote-control` lets the user follow and steer it from a phone
  or browser.
- The agent works from three sources: the repo (this file, `CLAUDE.md`, the READMEs and Run log),
  its memory files, and the conversation. When the conversation is compacted, the repo must hold
  everything needed to carry on.

**How the agent keeps watch.**
- **Event watches** (the Monitor tool): one watch tails the autopilot log, the NERSC driver log and
  the pair-watcher log, filtered to alerts, farm ends, submissions, publications, failures, budget
  lines and log-read retries. It also prints the farm list from `qstat` whenever it changes. A watch
  expires after 30 min: re-arm it at once, and print the state at start so nothing is missed between
  watches. Keep exactly one watch; stop duplicates.
- **Hourly check-ins** (a scheduled prompt, cron `17 * * * *`): check that the screens are alive, read
  the logs, check that ended farms were re-queued and both capacity slots are covered, count failures
  that have no time-limit or cancel tag, check budgets, re-arm the watch, refresh the progress page
  every few hours, log what was notable. The autopilot and the watches cover the routine; the
  check-in catches what makes no noise (a dead or hung process, a slow drift).
- **Keep the check-in alive for weeks.** Scheduled prompts live only in the agent's session and
  expire after 7 days (in this campaign they once expired silently). So the check-in renews itself:
  its first step re-creates it when it is 6 days old and records the date in a memory file. A
  one-shot backup reminder re-creates it if it is missing, then reschedules itself.
- **Keep the agent itself alive.** `aurora/watchdog.sh` (its own `screen`, 5-min cycle) restarts the
  agent with `claude --continue` and an instruction to re-create its check-in and watches if the
  session dies, and restarts the autopilot, the NERSC driver and the pair watcher if their screens
  are gone. There is no `crontab` on Aurora login nodes. A login-node reboot ends everything,
  watchdog included: after a maintenance, start the watchdog again and it brings back the rest.
- **To restart a watched script, quit its screen and let the watchdog bring it back** (within 5
  min); never quit and re-launch it yourself, or the two launches race and two copies run (two
  autopilots submit duplicate farms). Every long-running script also takes a `flock` at start and
  exits if another copy holds it.
- **Never edit a running bash script in place.** bash reads it while it runs; replace the file
  (`sed -i`, `git checkout`, or write-and-`mv` all make a new file) and restart the script.
- Long waits (a queued job, a transfer) go in a background command that exits when the condition is
  met, not in a sleep loop.

**How the agent acts.**
- Act on the obvious next step without asking: re-queue, resubmit, fill an empty capacity slot,
  re-arm a watch, fix a script bug, correct a false failure. Ask the user before anything that spends
  a large share of an allocation, moves work to another project, cancels a job that has waited long,
  or changes the science (inputs, methods, what counts as a valid point). Give a recommendation with
  each question.
- **Read the evidence before naming a cause**: the backtrace, the job comment (`qstat -f`), the
  project balance, the actual step counts. Several first explanations in this campaign were wrong
  until the logs were read.
- Put limits in code, not in good intentions: budget caps in the driver, the pair watcher, locks,
  atomic file replacement, frozen script copies. Restart a daemon only between cycles, and check
  afterwards that exactly one copy runs.
- Before moving or deleting anything, look at it. Before submitting with a script, check which
  account and settings it will use (a submission once went to an expired project).
- A false alarm still gets an explanation and, if it can recur, a fix (log reads that fail now and
  then are retried instead of counted as failures).

**How the agent keeps people informed.**
- Run log (`aurora/README.md`): one dated entry per notable event or decision, with the user's
  decisions marked as such. This file: rules only, rewritten in place when they change.
- `STATUS.md` (pushed every 2 h) and a progress page (an artifact with the finished-branch curve,
  farms and NERSC runs, republished on request and every few hours). If a page cannot be updated,
  publish a new one and give the link.
- In chat: one or two lines per routine event, a short summary when something changes, and the
  open decisions repeated until answered.
- Memory files hold facts that must survive a new session: where things live, the user's standing
  rules (frugal NERSC charging, the Aurora job comes first), links.
