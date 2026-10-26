# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 01:11 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7261 done, 0 started (running/stopped/failed), 2636 continuations ready, 278 not started, 10175 total
queue main: 2468 of 40005 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,755.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8965440 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 94 finished (94 copied back to Aurora), 444 running, 2 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 35
484 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 0 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 0 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 0 / 30 |
| ICAVAK | 7 / 30 |
| NAMSOJ | 3 / 30 |
| NECTOG | 4 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 25 / 30 |
| OJELOE | 4 / 30 |
| RAYBIC | 4 / 30 |
| REJBUD | 4 / 30 |
| SONROE | 4 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 4 / 30 |
| WUJZOS | 27 / 30 |

Last driver actions:

```
[2026-10-26 00:32:20] status: 446 jobs queued/running, 94 branches finished (93 back on Aurora), 0 need review
[2026-10-26 00:45:05] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-26 00:45:05] status: 446 jobs queued/running, 94 branches finished (94 back on Aurora), 0 need review
[2026-10-26 00:56:56] status: 446 jobs queued/running, 94 branches finished (94 back on Aurora), 0 need review
[2026-10-26 01:09:23] scans/NAMSOJ/angle_N2-Zn-S4_neg FAILED (job 60240124, state completed): ['scans/NAMSOJ/angle_N2-Zn-S4_neg end 2026-10-25 17:58:02']
[2026-10-26 01:09:55] scans/SONROE/angle_N115-Zn-N117_pos FAILED (job 60240860, state completed): ['scans/SONROE/angle_N115-Zn-N117_pos end 2026-10-25 17:56:29']
[2026-10-26 01:10:03] submitted 2 jobs
[2026-10-26 01:10:03] status: 446 jobs queued/running, 94 branches finished (94 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 00:17:54] farm 8962257 (zn_main) ended: farm 8962257 done 2026-10-26 00:03:22; queue next 37537 of 40005
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8965440): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (2468 pending now)
NODES=0: queue updated, no farm submitted
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
