# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-29 03:44 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7964 done, 0 started (running/stopped/failed), 2206 continuations ready, 5 not started, 10175 total
queue main: 2152 of 42267 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,150.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8978689 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8978755 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 481 finished (481 copied back to Aurora), 43 running, 16 queued, 0 need review, 540 total
stops at the 48 h limit so far: 141; failed runs: 91
1354 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 25 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 30 / 30 |
| WIGBIX | 28 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-29 03:34:13] scans/CATZUS10/angle_N22-Zn-N40_pos stopped at the time limit (job 60349367); continues
[2026-10-29 03:34:45] scans/CATZUS10/angle_N22-Zn-N58_neg stopped at the time limit (job 60349369); continues
[2026-10-29 03:35:17] scans/BUNNII/twist_S128-S130-S132-S134_neg stopped at the time limit (job 60348821); continues
[2026-10-29 03:35:49] scans/CATZUS10/angle_N22-Zn-N40_neg stopped at the time limit (job 60348822); continues
[2026-10-29 03:36:21] scans/BUNNII/tilt_Zn-S134-C90-S135_neg stopped at the time limit (job 60348816); continues
[2026-10-29 03:36:53] scans/BUNNII/tilt_Zn-S134-C90-S135_pos stopped at the time limit (job 60348819); continues
[2026-10-29 03:37:16] submitted 6 jobs
[2026-10-29 03:37:16] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-29 01:57:41] STATUS.md pushed
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
