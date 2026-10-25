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
6. **Split the work by cost.** Give the largest molecules more cores per job (8 instead of 4 here) and
   start them first, or send them to a second site from day one: they finish last and set the end
   date.
7. **Use every facility you have from the start.** Adding a second site late helps less than running
   both in parallel from day one.

## Aurora (PBS)

- **Request 6 h walltimes.** Priority grows with eligible time squared and falls with requested
  walltime cubed: 12 h has about 1/8 the priority of 6 h. With stop-and-continue, short farms lose only
  a few percent to restarts.
- **Throughput comes from 256-node farms.** `capacity` allows 2 running jobs of up to 16 nodes per
  user, so most of the node-hours come from `prod` (routed to `small`, 256 nodes and up). Their start is
  unpredictable (minutes to days), and priority only grows while a job waits, so **keep one or two
  256-node farms queued at all times while there is work to fill them**: submit the next one when the
  previous one starts, not when it ends.
- **Only submit a 256-node farm when the queue can fill it** (6,144 slots at 24 per node). Idle nodes
  in a running farm are charged. With less work, use 16-node farms, mixed farms that give spare nodes
  to another pool (`node.sh`), or another site.
- **Leave time for the end-of-run hand-back.** Preparing thousands of stopped jobs for continuation
  takes 20-30 min on a busy Lustre. Farms of 64 nodes or more stop ORCA 50 min before the walltime
  (`MARGIN_MIN`).
- `qhold`/`qrls` and `qalter -A <project>` keep a queued job's eligible time. Hold queued farms rather
  than letting them start into an empty queue. `qalter -v` is not supported.
- Production reads ORCA and OpenMPI from `/lus/flare`, not `$HOME`; set `OPAL_PREFIX`.

## Perlmutter (Slurm, through the NERSC IRI API)

- **Charging:** use `shared` (charged per core used), `regular` or `debug`. Never use `premium` (a
  charge multiple) for a campaign. A pending reason `Priority` is Slurm's reason code, not a QOS.
- **Speed:** a CPU node (2 x EPYC 7763, 128 cores) does 1.25-1.33x the work of an Aurora node; a
  single job runs at the same speed on both.
- **Layout:** one `shared` job per branch (8 physical cores = 16 CPUs, 30 GB, 48 h). `shared` charges
  nothing for idle cores, which suits a thinning tail; whole-node `regular` jobs (16 branches x 8
  cores) are charged until their slowest branch ends.
- **Expect about 2% of `shared` jobs to die with a segmentation fault in `orca_startup_mpi`.** Scratch
  location and `%maxcore` do not change it, and it has not been seen in whole-node jobs or on Aurora.
  Resubmit automatically from the last geometry, up to 3 tries; move a branch that keeps failing to a
  whole-node job.
- **OpenMPI 4.1.6** for ORCA 6.0.1 builds only with its internal hwloc, PMIx and libevent
  (`nersc/iri/pm_install.sh`). Keep ORCA scratch on `$PSCRATCH` in `shared` jobs (`/tmp` is memory and
  counts against the job).
- **IRI API** (`api.iri.nersc.gov`), driven from an Aurora login node (`nersc/iri/driver.py`):
  - login is a two-step PKCE flow; stamp tokens with `expires_at`, or refreshes race;
  - uploads are limited to 5 MB, and scratch downloads come back base64-encoded;
  - the job list returns every user's jobs: poll your own jobs one by one;
  - times in NERSC logs are Pacific;
  - deploy a script by uploading `name.new` and renaming it, never by overwriting it in place.
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
- **Keep a record people can follow:** a dated Run log, a status page regenerated every 2 h, and
  hourly checks (autopilot alive, alerts, farms, failures without a time-limit or cancel tag).
- **Watch for silence as well as errors.** A driver or farm that stops logging is as bad as one that
  fails; alert on a stale log, not only on error lines.
