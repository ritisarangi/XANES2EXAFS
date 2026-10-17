# Zn scan production run on ALCF Aurora

Same scans as `nersc/README.md` (relaxed one-coordinate scans at the stage-2 level, 16 cores per ORCA job), run on Aurora's CPUs. Everything runs through `aurora/go.sh`; the scan inputs, restart logic and validation are the shared ones in `scans/`.

## How it differs from Perlmutter

Aurora charges whole nodes and has no shared QOS or Slurm arrays, so one PBS job (a "farm") runs 6 ORCA jobs of 16 cores on each node, each pinned to its own cores (1-16, 17-32, 33-48, 53-68, 69-84, 85-100; cores 0 and 52 belong to the OS). The slots pull branches from one shared queue (`$WORK/queue`, locked with `flock`), largest complexes first. About 10 minutes before the walltime, ORCA runs still going are stopped and logged as `DUE TO TIME LIMIT`, so the next `submit` continues them from their last converged step with `scans/restart.py`, exactly as on S3DF and NERSC. When the queue is empty and fewer than a quarter of the slots are still busy, the farm stops the stragglers instead of holding idle nodes; they continue in the next, smaller job.

Queues: `capacity` (1 to 16 nodes, up to 168 h, 2 running jobs per user) is the production queue. `prod` starts at 256 nodes (up to 12 h). `debug` (1 to 2 nodes, 1 h) and `debug-scaling` (up to 256 nodes, 1 h) are for tests.

## One-time setup

1. Download ORCA 6.0.1 for Linux x86-64 (`orca_6_0_1_linux_x86-64_shared_openmpi416.tar.xz`) from https://orcaforum.kofo.mpg.de under your own account, and copy it and `scan_bundle.tar.gz` to Aurora.
2. On an Aurora login node:
   ```
   git clone https://github.com/ritisarangi/XANES2EXAFS.git
   bash XANES2EXAFS/aurora/install_orca.sh ~/orca_6_0_1_linux_x86-64_shared_openmpi416.tar.xz <ALCF project> /lus/flare/projects/<project>/$USER/zn_scans
   source ~/.bashrc
   ```
   This unpacks ORCA, builds OpenMPI 4.1.6 under `$HOME/sw` (about 15 minutes, single-node only), and adds `ACCOUNT`, `ORCA_DIR`, `MPI_DIR` and `WORK` to `~/.bashrc`.

## Commands

| Step | Command | What it does |
|---|---|---|
| 1 | `bash XANES2EXAFS/aurora/go.sh setup scan_bundle.tar.gz` | Unpacks into `$WORK` and checks ORCA and MPI. |
| 2 | `bash XANES2EXAFS/aurora/go.sh test` | One debug node runs 6 packed ORCA test jobs. Expect 6 normal terminations and 6 disjoint core groups in `logs/test_placement_<job>.txt`. |
| 3 | `QUEUE=debug-scaling NODES=8 HOURS=1 bash XANES2EXAFS/aurora/go.sh submit REF1 REF2` | Pilot: all branches of two complexes for one hour, which also exercises the time-limit stop. Submit again when it ends to run the continuations, then `go.sh status`. |
| 4 | `bash XANES2EXAFS/aurora/go.sh submit` | Production: continues stopped branches, queues everything not yet run, submits a 16-node, 48 h capacity farm. Run it a second time to have two farms on the same queue. |
| 5 | `bash XANES2EXAFS/aurora/go.sh status` | Farm jobs, branch states, validated points. |
| 6 | `bash XANES2EXAFS/aurora/go.sh export` | Validates every point and packs the passing geometries into `scan_results.tar.gz` for Riti. |

`submit` options: `QUEUE`, `NODES`, `HOURS`, `TAIL_FRAC` (0 turns the tail cutoff off), `MIN_START_MIN` (no new branch with less time left, default 45). `go.sh drain` lets running farms finish their current branches without starting new ones.

## Cost

S3DF pilot: median 31 minutes per geometry on 16 cores, about 790,000 core-hours for the full set. At 96 busy cores per node that is about 8,200 Aurora node-hours if an Aurora core matches a Milan core; the pilot's `validate.py` timing gives the real figure. Two 16-node capacity farms (192 ORCA jobs at once) take about 11 days.

## Notes for Claude

- Work only inside `$WORK` and the `XANES2EXAFS` clone. Do not edit or delete `scan.out`, `scan_acc.txt` or `scan_orig.inp` files: they are the results.
- Use `go.sh` for submitting and exporting. The queue is rebuilt only when no farm job is queued or running, so a branch is never handed out twice.
- Do not cancel farm jobs unless asked; `go.sh drain` is the gentle stop. A farm killed outright is recovered by the next `submit` (its unfinished branches are tagged as cancelled and continued).
