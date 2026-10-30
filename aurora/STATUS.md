# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-30 03:13 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8326 done, 0 started (running/stopped/failed), 1849 continuations ready, 0 not started, 10175 total
queue main: 1705 of 43644 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,725.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |
| 8988070 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8988123 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 22 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 517 finished (516 copied back to Aurora), 143 running, 0 queued, 0 need review, 660 total
stops at the 48 h limit so far: 173; failed runs: 91
1424 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 14 / 30 |
| CAPWIB | 4 / 30 |
| CATZUS10 | 16 / 30 |
| DOZVOF | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 3 / 30 |
| LAJGIM | 0 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 30 / 30 |
| UYORAE | 0 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-30 02:20:21] status: 145 jobs queued/running, 515 branches finished (515 back on Aurora), 0 need review
[2026-10-30 02:31:45] scans/BUNNII/tilt_Zn-S130-C30-S131_neg finished (job 60478318)
[2026-10-30 02:31:45] status: 144 jobs queued/running, 516 branches finished (515 back on Aurora), 0 need review
[2026-10-30 02:42:34] status: 144 jobs queued/running, 516 branches finished (515 back on Aurora), 0 need review
[2026-10-30 02:54:18] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-30 02:54:18] status: 144 jobs queued/running, 516 branches finished (516 back on Aurora), 0 need review
[2026-10-30 03:05:40] scans/BUNNII/angle_S130-Zn-S132_neg finished (job 60477649)
[2026-10-30 03:05:40] status: 143 jobs queued/running, 517 branches finished (516 back on Aurora), 0 need review
```

## Last autopilot actions

```
no stopped branches found
main farm jobs already queued or running (8939977 8987775 8988070): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (1705 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-30 02:34:21] submitting main capacity farm on ModCon, 6 h (queue 1705 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8987775 8988070): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (1705 pending now)
2026-10-30 02:37:46 farm 8988123.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=1705
prioritize main: 230 of 1705 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
