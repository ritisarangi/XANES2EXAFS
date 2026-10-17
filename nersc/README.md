# Zn scan production run on NERSC Perlmutter

Relaxed one-coordinate scans around the B3LYP-D3(BJ) minima of about 335 Zn model complexes, at the stage-2 level, 16 cores per ORCA job in the `shared` QOS. Everything runs through one script, `nersc/go.sh`.

## One-time setup

0. Get `scan_bundle.tar.gz` (0.7 MB) from Riti by email or Drive. It holds the stage-2 geometries and is not in this repo.
1. Download ORCA 6.0.1 for Linux x86-64 (`orca_6_0_1_linux_x86-64_shared_openmpi416.tar.xz`) from https://orcaforum.kofo.mpg.de under your own account, and copy it and `scan_bundle.tar.gz` to your Perlmutter home folder.
2. On Perlmutter:
   ```
   git clone https://github.com/ritisarangi/XANES2EXAFS.git
   bash XANES2EXAFS/nersc/install_orca.sh ~/orca_6_0_1_linux_x86-64_shared_openmpi416.tar.xz <NERSC project>
   source ~/.bashrc
   ```
   This unpacks ORCA, builds OpenMPI 4.1.6 under `$HOME/sw` (about 15 minutes), and adds `ACCOUNT`, `ORCA_DIR` and `MPI_DIR` to `~/.bashrc`.

## Commands

| Step | Command | What it does |
|---|---|---|
| 1 | `bash XANES2EXAFS/nersc/go.sh setup scan_bundle.tar.gz` | Unpacks into `$PSCRATCH/zn_scans`, checks ORCA and MPI, submits a 5-minute water test. Wait for `ORCA_TEST_OK` in the test log. |
| 2 | `bash XANES2EXAFS/nersc/go.sh submit` | Writes all scan inputs (first time) and submits the next 20 array chunks. Run again whenever the queue drains until it reports 0 chunks left. |
| 3 | `bash XANES2EXAFS/nersc/go.sh status` | Running and pending counts, finished jobs, validated points. |
| 4 | `bash XANES2EXAFS/nersc/go.sh restart` | Continues branches stopped by the 48 h limit from their last converged step. Safe to run any time. |
| 5 | `bash XANES2EXAFS/nersc/go.sh export` | Validates every point and packs the passing geometries into `scan_results.tar.gz` for Riti. |

`git -C XANES2EXAFS pull` picks up fixes; it does not touch running jobs.

## Size and cost

About 30 branch jobs and 273 geometries per four-coordinate complex. The S3DF pilot ran a median 31 minutes per geometry on 16 cores, so the full set is roughly 790,000 core-hours. Large complexes take up to about 7 hours per geometry, so some branches need one or two restarts.

## Notes for Claude

- Work only inside `$PSCRATCH/zn_scans` and the `XANES2EXAFS` clone. Do not edit or delete `scan.out`, `scan_acc.txt` or `scan_orig.inp` files: they are the results.
- Use `go.sh` for submitting, restarting and exporting. Do not write new submit scripts or change Slurm settings in `sites/nersc.sh` without asking.
- Do not cancel jobs unless asked. Report status with `go.sh status`.
- First failures listed by `validate.py` (jump, shell, energy_drop, new_contact) are expected at the ends of scans and need no action. An `energy_drop` more than 2 kJ/mol below a branch start means that complex has a lower minimum; list such complexes for Riti.
