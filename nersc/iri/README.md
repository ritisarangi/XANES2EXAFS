# Big pool on NERSC Perlmutter, driven from Aurora (IRI API + Globus)

Since 2026-10-25 the 18 unfinished big complexes (`$WORK/remote_refs.txt`) run on Perlmutter while
Aurora runs the main pool. Aurora never queues or prepares a complex listed in `remote_refs.txt`
(`aurora/queue.py`, `scans/restart.py`), so no branch runs at both sites.

| File | What it does |
|---|---|
| `pm_install.sh` | unpacks the user's own ORCA 6.0.1 archive (same file as on Aurora, SHA-256 checked) and builds OpenMPI 4.1.6 with the Aurora configure options, in `$PSCRATCH/zn_nersc_test/sw` |
| `pm_bench.sh` | node-throughput benchmark, as `aurora/bench/bench.sh` |
| `pm_branch.sh` | one branch as one shared-QOS job (8 cores, 48 h): prepares a continuation with `restart.py` if needed, runs ORCA, stitches `scan.out`; per-folder lock as on Aurora |
| `driver.py` | runs on an Aurora login node (`screen -S zn_nersc`): submits and watches the jobs through the NERSC IRI API, resubmits stopped branches, copies finished ones back to the Aurora run folder with Globus Transfer, writes the NERSC part of `aurora/STATUS.md` |

Credentials: the IRI token (`~/.globus/auth_tokens.json`) and the Globus Transfer token
(`~/.globus/transfer_tokens.json`) belong to the user and stay on Aurora; they refresh themselves.

Tests before the move (2026-10-24): a Perlmutter CPU node does 1.25-1.33x the work of an Aurora node
(109.4 vs 87.4 one-cycle LUZTEF jobs per node-hour at 4 cores per job); one branch runs at the same
speed on both. 103 scan steps of 24 CADKUO branches and the first cycles of 4 OJEKOD branches
reproduced the Aurora results to 0.003 and 0.009 kJ/mol and 0.007 A.
