# Zn scan production run on ALCF Aurora

Same scans as `nersc/README.md` (relaxed one-coordinate scans at the stage-2 level, B3LYP-D3(BJ), mixed def2-TZVP/def2-SVP, RIJCOSX, CPCM(water), TightOpt, DefGrid3), run on Aurora's CPUs. Everything runs through `aurora/go.sh`; scan inputs, restart logic and validation are the shared ones in `scans/`. The method keywords are unchanged; only the parallel settings (`%pal nprocs`, `%maxcore`) follow the Aurora layout.

Workload from `scan_bundle.tar.gz`: 338 complexes, 10,175 branches, 92,589 constrained optimisations (the first point of each branch is the stage-2 minimum and is cheap).

## How it differs from Perlmutter

Aurora charges whole nodes (2 x Xeon Max 9470C, 104 cores, 1 TB DDR5, 128 GB HBM; cores 0 and 52 belong to the OS, so 102 are usable) and has no shared QOS or Slurm arrays. One PBS job (a "farm") runs many pinned ORCA jobs on every node and keeps them fed from a shared queue on Lustre (`$WORK/queue/<pool>`, locked with `flock`), largest complexes first.

- About 10 minutes before the walltime, ORCA runs still going are stopped and logged as `DUE TO TIME LIMIT`. The next `submit` continues them with `scans/restart.py`, exactly as on S3DF and NERSC.
- With `RESUME_PARTIAL=1` (on by default in `go.sh`, off by default in `restart.py`), the interrupted step restarts from its last optimisation geometry at the same target instead of from the last converged step, so its finished optimisation cycles are not repeated. Riti: please check you are happy with this; `RESUME_PARTIAL=0 go.sh submit` restores the original behaviour.
- ORCA works in node-local `/tmp` (a RAM disk); `scan.out` is written straight to `$WORK` so a stopped branch can always be continued, and the other outputs (minus `.gbw`/`.tmp`/densities, as before) are copied back when the run ends.
- When a queue is empty and fewer than a quarter of a farm's slots are still busy, the farm stops the stragglers instead of holding idle nodes; they continue in the next, smaller job.
- Jobs run from a frozen copy of the scripts in `$WORK/.repo/<time>`, so `git pull` never changes a queued or running farm.
- Continuations of stopped branches can be put at the front of a live queue (`go.sh submit` does this when farms of the pool are already queued or running; `NODES=0` only re-queues), so long `capacity` farms and short `prod` farms can share a pool.

## Layout (benchmarked 2026-10-17)

Whole node filled with copies of LUZTEF (81 atoms, the cost-weighted median complex), stage-2 keywords:

| ORCA jobs x cores per node | jobs per node-hour (1 opt cycle) | vs 6 x 16 |
|---|---|---|
| 6 x 16 (NERSC layout) | 72.0 | - |
| 6 x 17 | 70.8 | -2% |
| 10 x 10 | 80.2 | +11% |
| 12 x 8 | 78.1 | +8% |
| 24 x 4 | 87.4 | +21% |
| 34 x 3 | 86.8 | +21% |

Also measured with 12 x 8 (2 opt cycles): node-local `/tmp` scratch +4%, hyperthreading (16 ranks on 8 cores) +2%, HBM-preferred memory 0%. Peak memory was under 60 GB per node in every layout.

So the run uses two pools with separate queues and farms:

| Pool | Complexes | Branches | Cores per ORCA job | Jobs per node | Share of compute (~atoms^2.5) |
|---|---|---|---|---|---|
| `main` | 318 below 100 atoms | 9,575 | 4 | 24 | ~78% |
| `big` | 20 with 100 atoms or more | 600 | 8 | 12 | ~22% |

The large complexes get more cores so their points (several hours each at 16 cores on S3DF) do not trail the campaign for days.

## Queues

| Queue | Nodes | Walltime | Use here |
|---|---|---|---|
| `prod` (routes to `small` for 256-1024 nodes) | 256 or more | up to 12 h | `main` pool, 256-node farms |
| `capacity` | 1 to 16 (2 running jobs per user, 512 nodes for all users) | up to 168 h | one long `main` farm and the `big` pool |
| `debug`, `debug-scaling` | 1-2 / up to 256 | 1 h | tests and benchmarks only, never production |

Shorter `prod` jobs start sooner because they fit the backfill gaps before large reservations; with the stop/continue logic a 4 h job loses only a few percent to restarts. Several farms of the same pool share one queue, so it does not matter which one starts first.

## One-time setup

1. Download ORCA 6.0.1 for Linux x86-64 (`orca_6_0_1_linux_x86-64_shared_openmpi416.tar.xz`) from https://orcaforum.kofo.mpg.de under your own account, and copy it and `scan_bundle.tar.gz` to Aurora.
2. On an Aurora login node:
   ```
   git clone https://github.com/ritisarangi/XANES2EXAFS.git
   bash XANES2EXAFS/aurora/install_orca.sh ~/orca_6_0_1_linux_x86-64_shared_openmpi416.tar.xz <ALCF project> /lus/flare/projects/<project>/$USER/zn_scans
   source ~/.bashrc
   ```
   This unpacks ORCA, builds OpenMPI 4.1.6 (single-node only) and adds `ACCOUNT`, `ORCA_DIR`, `MPI_DIR` and `WORK` to `~/.bashrc`. Production jobs should read ORCA and OpenMPI from `/lus/flare`, not `$HOME` (copy them there and point `ORCA_DIR`/`MPI_DIR` at the copies).

## Commands

| Step | Command | What it does |
|---|---|---|
| 1 | `bash XANES2EXAFS/aurora/go.sh setup scan_bundle.tar.gz` | Unpacks into `$WORK` and checks ORCA and MPI. |
| 2 | `bash XANES2EXAFS/aurora/go.sh test` | One debug node runs 6 packed ORCA test jobs. |
| 3 | `POOL=main QUEUE=debug-scaling NODES=4 HOURS=1 bash XANES2EXAFS/aurora/go.sh submit REF1 REF2` | Pilot of some complexes for one hour; submit again when it ends to exercise the continuation. |
| 4 | `POOL=main QUEUE=prod NODES=256 HOURS=12 bash XANES2EXAFS/aurora/go.sh submit` | Production: continues stopped branches, queues everything not yet run, submits a farm. |
| 5 | `POOL=big QUEUE=capacity NODES=4 HOURS=96 bash XANES2EXAFS/aurora/go.sh submit` | Same for the large complexes. |
| 6 | `NODES=0 bash XANES2EXAFS/aurora/go.sh submit` | After a farm ends while others of the pool still run: re-queue its stopped branches without submitting a new job. |
| 7 | `bash XANES2EXAFS/aurora/go.sh status` / `watch`, or `bash XANES2EXAFS/aurora/monitor.sh` | Farm jobs, queues, branch states, validated points; `monitor.sh` prints a line a minute and ALERT lines on ORCA failures or a farm leaving the queue. |
| 8 | `bash XANES2EXAFS/aurora/go.sh export` | Validates every point and packs the passing geometries into `scan_results.tar.gz`. |

The layout benchmark is `aurora/bench/bench.pbs` (see its header); `aurora/bench/mkinp.py` writes the stage-2-level test input for any complex.

Other options: `CORES`, `HT`, `HBM`, `MAXCORE`, `SCRATCH` (see `sites/aurora.sh`), `TAIL_FRAC` (0 turns the tail cutoff off), `MIN_START_MIN` (no new branch with less time left, default 20), `BIG_ATOMS` (pool boundary, default 100). `POOL=<pool> go.sh drain` lets a pool's farms finish their current branches without starting new ones.

## Where things are (the 2026-10-17 run)

| What | Where |
|---|---|
| Run folder (`$WORK`) | `/lus/flare/projects/isaac/dsokaras/zn_scans` (bundle unpacked here; `scans/<REF>/<coord>_<branch>/`) |
| Queues | `$WORK/queue/main`, `$WORK/queue/big` (`tasks.txt`, `next`, `active/`) |
| Logs | `$WORK/logs/scan[r]_<job>_<node>_<slot>_<n>.log` per branch run, `$WORK/logs/<job>.OU` per farm, `$WORK/logs/submissions.txt` |
| ORCA 6.0.1, OpenMPI 4.1.6 | `/lus/flare/projects/isaac/dsokaras/zn_sw/` |
| Allocation | ALCF project `isaac`; it ends 2026-10-22, so work left then needs another project (`ACCOUNT=<project> go.sh submit` continues it) |
| Benchmark runs | `$WORK/bench/run_<job>/summary.txt` |

## Run log

- 2026-10-17: ORCA 6.0.1 + OpenMPI 4.1.6 installed on Aurora; farm, packing, PALS/OpenMPI interplay, stop/continue/stitch tested with stand-ins; layout benchmarked (above).
- 2026-10-17 pilot (1 h; MAZBZN10 49 atoms, CAPWIB 65, LUZTEF 81 in `main` on 4 nodes; WIGBIX 121 in `big` on 2 nodes): 0 ORCA failures in 114 runs, all stopped cleanly at the walltime. First SCF at the stage-2 geometry reproduces the S3DF stage-2 energy to 1e-6 Eh (0.001 kJ/mol). `validate.py`: 52/52 completed points pass. About 7 min per optimisation cycle per 4-core slot. Branch-start points take 3-5+ TightOpt cycles even at the stage-2 minimum: gradient and energy are converged at once, but soft ligand modes keep the step criterion open (same input on S3DF, so not Aurora-specific; starting branches from the stage-2 point without re-optimising would save these cycles). Estimate for the full set: 4,500-5,500 node-hours.
- Fixed after the pilot: ORCA scratch files named `*.tmp.0` were copied back from `/tmp` (5 GB for 4 complexes, now about 4 MB per branch); now excluded. Continuations can go to the front of a live queue. `restart.py` re-prepared branches that were already prepared but not yet rerun, which replaced a partial-resume geometry with the last converged one; it now skips them. The 114 pilot continuations were re-prepared once from their saved `scan_try1.out` (52 resume their interrupted step, 62 start their branch again).
- 2026-10-17 22:25-22:45 production submitted on `isaac`. `main` queue: 90 pilot continuations first, then 9,485 fresh branches, largest first; farms 8939977 (256 nodes x 12 h, `prod`), 8940026 (256 x 4 h, `prod`, for backfill) and 8939979 (16 x 72 h, `capacity`). `big` queue: 24 continuations + 576 fresh; farm 8939981 (16 x 72 h, `capacity`). All queued at first (`capacity` near its 512-node limit, `small` with about 19,000 nodes requested ahead).

## Notes for Claude

- Work only inside `$WORK` and the `XANES2EXAFS` clone. Do not edit or delete `scan.out`, `scan_acc.txt` or `scan_orig.inp` files: they are the results.
- Use `go.sh` for submitting and exporting. A pool's queue is rebuilt only when none of that pool's farms is queued or running, so a branch is never handed out twice; the pools never share a branch.
- Do not cancel farm jobs unless asked; `go.sh drain` is the gentle stop. A farm killed outright is recovered by the next `submit` (its unfinished branches are tagged as cancelled and continued).
- When a farm ends: `POOL=<pool> go.sh submit` with the queue settings of the next farm (or `NODES=0` if other farms of the pool still run). Check `validate.py` pass rates and failed runs (`monitor.sh`) before adding more farms.
- Keep the Run log above current; it is how Riti and her agent follow the run.
