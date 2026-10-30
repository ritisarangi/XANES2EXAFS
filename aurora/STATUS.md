# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-30 14:57 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8552 done, 0 started (running/stopped/failed), 1623 continuations ready, 0 not started, 10175 total
queue main: 1379 of 44270 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,531.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |
| 8990248 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8990398 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 27 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 568 finished (566 copied back to Aurora), 97 running, 145 queued, 0 need review, 810 total
stops at the 48 h limit so far: 173; failed runs: 91
1438 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 25 / 30 |
| CAPWIB | 17 / 30 |
| CATZUS10 | 19 / 30 |
| CAWKIW | 4 / 30 |
| DOZVOF | 30 / 30 |
| FUXMAM | 4 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 5 / 30 |
| JUQXUO | 3 / 30 |
| LAJGIM | 4 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 4 / 30 |
| SONROE | 30 / 30 |
| TIFNUU | 3 / 30 |
| UYORAE | 0 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-30 14:10:49] status: 112 jobs queued/running, 548 branches finished (548 back on Aurora), 0 need review
[2026-10-30 14:21:32] status: 112 jobs queued/running, 548 branches finished (548 back on Aurora), 0 need review
[2026-10-30 14:32:45] scans/JOCZEG/tilt_Zn-N5-C37-H73_pos finished (job 60502522)
[2026-10-30 14:32:45] status: 111 jobs queued/running, 549 branches finished (548 back on Aurora), 0 need review
[2026-10-30 14:40:06] driver started (810 branches, account m5268)
[2026-10-30 14:41:15] scans/CAPWIB/bond_Zn-S10_pos finished (job 60502449)
[2026-10-30 14:50:34] submitted 132 jobs
[2026-10-30 14:50:34] status: 242 jobs queued/running, 568 branches finished (566 back on Aurora), 0 need review
```

## Last autopilot actions

```
queue: 0 continuations added to the front of queue/main (1511 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-30 14:39:51] submitting main capacity farm on ModCon, 6 h (queue 1379 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8987775 8990248): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (1379 pending now)
2026-10-30 14:43:17 farm 8990398.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=1379
prioritize main: 214 of 1379 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 214 of 1379 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
