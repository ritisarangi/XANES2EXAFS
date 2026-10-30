# Running ORCA campaigns on ALCF Aurora and NERSC Perlmutter

Instructions for an agent or person starting a large ORCA campaign on these machines. They distil
everything learned in the Zn relaxed-scan campaign (338 complexes, 10,175 scan branches, ~92,600
constrained optimisations, ORCA 6.0.1, Aurora and Perlmutter, from October 2026 on). This file is kept
current: when a rule changes, the rule is rewritten here, not appended as history. The chronological
record of the campaign is the Run log in `aurora/README.md`; the scripts are in `aurora/`,
`nersc/iri/` and `scans/`.

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

1. **Check every project's allocation end date and storage quota.** After an allocation ends, its
   storage quota can drop to almost nothing, and writes then fail silently: ORCA outputs are cut off
   with no error. Move to the next project and folder before the end date, and show quota and balance
   (`myquota`, `sbank-list-allocations`) on the status page.
2. **Estimate the total in node-hours, and measure progress in finished points (optimisations), not
   only finished branches.** A branch counts only when its whole scan is done, so branch counts lag
   far behind the real work early on.
3. **Benchmark the layout on one full node** with the median-cost molecule (`aurora/bench/`,
   `nersc/iri/pm_bench.sh`). For throughput, many narrow jobs beat few wide ones: on Aurora 24 jobs x
   4 cores per node did 21% more work than 6 x 16. Node-local scratch helped a little (+4%),
   hyperthreading barely (+2%), HBM not at all.
4. **Use the same ORCA build everywhere** (compare the archive's SHA-256) and **reproduce a few jobs at
   each new site** before moving work there. Agreement should be about 0.01 kJ/mol and 0.01 A.
5. **Run a short test farm in a debug queue before every new kind of production job**, including its
   end-of-run steps (stopping ORCA before the walltime, handing unfinished jobs back to the queue).
6. **Split the work by cost, and size the cores by the time one step takes.** Each scan step starts
   from the previous one, so a branch's wall time is (steps) x (time per step), and the largest
   molecules set the campaign's end date. Measure one constrained optimisation per complex first. Here
   ~140 atoms / ~1,400 basis functions (def2-SVP) took 9-15 h per step on 8 cores (30-50 optimisation
   cycles), so an 11-step branch needed 4-6 days. Give such molecules 16-32 cores per job from day one
   (fewer node-hours per step are lost to poor scaling than days are lost to the tail), keep 4 cores
   for the rest, start the largest first, or send them to a second site from day one.
7. **Check every optimised starting structure before scanning it.** Compare the donor list with the
   atoms actually near the metal (within about 2.8 A) at the reference minimum. In this campaign six of
   338 complexes had changed coordination during the reference optimisation (weak crystal contacts at
   2.5-3.1 A pulled in to bonds, one ligand switched binding atom). Every point of their 30 branches
   then failed validation, and that compute was wasted.
8. **Use every facility you have from the start.** Adding a second site late helps less than running
   both in parallel from day one.

## Aurora (PBS)

- **Project priority decides most of the wait.** PBS orders jobs by roughly
  eligible_time^2 / walltime^3 x project_priority x nodes, with walltime clamped to 6-12 h. Most queued
  work carries project_priority 25; discretionary projects (ModCon, isaac here) carry 2, so their
  256-node jobs start only when the machine is quiet. When the end date matters, ask ALCF support
  early for a temporary priority boost or a reservation (for example 256 nodes x 12 h), and ask the
  allocation program for an award with a higher priority; nothing in the job script matters as much.
- **Request 6 h for 256-node farms, never 12 h.** 12 h has 1/8 the priority of 6 h at equal wait, and
  a 12 h job never fits a backfill window: here 256-node farms of 6 h started after 5 min, 6 h and
  67 h, one of 4 h after 13 h, while the one 12 h farm waited more than 11 days. Below 6 h priority no
  longer rises (the clamp), but a 2-4 h job can backfill the hole PBS drains before a large job or a
  reservation (Aurora had a daily 335-node reservation, 14:00-05:00 Central). Stop-and-continue
  makes short farms cost only a few percent in restarts.
- **Throughput comes from 256-node farms.** `capacity` allows 2 running jobs of up to 16 nodes per
  user, so most of the node-hours come from `prod` (routed to `small`, 256 nodes and up). Their start is
  unpredictable (minutes to days), and priority only grows while a job waits, so **keep one or two
  256-node farms queued at all times while there is work to fill them**: submit the next one when the
  previous one starts, not when it ends. Never cancel a farm that has waited long: its eligible time
  is its priority. Resize what it does instead (`AUTO_CORES`, below).
  With two large farms queued for one pool, hold the second when the first starts (`aurora/bigpair.sh`)
  and release it when the first ends.
- **Keep both `capacity` slots busy** (2 running jobs per user, 16 nodes each): queue two 16-node farms,
  not one, so the second slot is not idle while the first farm hands back (autopilot `WANT_MAIN_CAP=2`).
- **Match a farm's slots to the queue when it starts, not when it is submitted.** A 256-node farm has
  6,144 slots at 4 cores; idle nodes in a running farm are charged. Farms take `AUTO_CORES=1`
  (`sites/aurora.sh`): at start they give each branch 4, 6, 8, 12 or 16 cores so the slots roughly
  match the branches waiting, which also makes each branch faster in the tail (12 cores: 2,048 slots;
  16 cores: 1,536). With even less work, use 16-node farms or another site.
- **A queued job runs the scripts of its own snapshot** (`$WORK/.repo/<time>`), however old. When a rule
  changes (a new list of complexes run elsewhere, a new layout), update the snapshots of queued jobs
  too, or they will start with the old behaviour.
- **Leave time for the end-of-run hand-back, and keep a backup for when it runs out.** Preparing stopped
  jobs for continuation takes 20-30 min for thousands of jobs, and on a slow Lustre even a few hundred
  can take longer than 25 min. Farms of 64 nodes or more stop ORCA 50 min before the walltime
  (`MARGIN_MIN`); smaller farms keep 25 min, and when one is killed mid-hand-back the autopilot's
  re-queue (`NODES=0 go.sh submit`) recovers its branches. Never rely on the margin alone.
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

## Running unattended

- **Run from a frozen copy of the scripts** (`$WORK/.repo/<time>`) so `git pull` never changes a running
  job. Replace files atomically; restart the autopilot only when it is idle.
- **One job per folder at a time:** a per-folder `flock`, a check that no output is still growing
  before a restart, and a snapshot of the queue length before adding continuations.
- **One list says which work runs where** (`remote_refs.txt`); every tool at the other site skips it.
- **Audit before publishing** (each output matches its folder's input, nothing ran twice), audit only
  what is about to be published, and publish a complex only when all its branches ended normally.
- **A problem in one item must not stop the rest.** Hold back the item with the problem and carry on
  with the others; check that a script running with `set -e` does not quit on a checker's non-zero
  exit (one complex with an audit finding once blocked every publication).
- **Keep a record people can follow:** a dated Run log, a status page regenerated every 2 h, and
  hourly checks (autopilot alive, alerts, farms, failures without a time-limit or cancel tag).
- **Watch for silence as well as errors.** A driver or farm that stops logging is as bad as one that
  fails; alert on a stale log, not only on error lines.
