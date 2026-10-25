# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-25 05:25 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7080 done, 0 started (running/stopped/failed), 2791 continuations ready, 304 not started, 10175 total
queue main: 2600 of 39624 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,851.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8962257 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 45 finished (45 copied back to Aurora), 60 running, 435 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 1
9 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 0 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 0 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 0 / 30 |
| ICAVAK | 0 / 30 |
| NAMSOJ | 0 / 30 |
| NECTOG | 0 / 30 |
| NONLEI | 0 / 30 |
| OJEKUJ | 16 / 30 |
| OJELOE | 0 / 30 |
| RAYBIC | 2 / 30 |
| REJBUD | 0 / 30 |
| SONROE | 1 / 30 |
| WIGBIX | 0 / 30 |
| WORMAR | 0 / 30 |
| WUJZOS | 26 / 30 |

Last driver actions:

```
[2026-10-25 04:50:29] pack: node job 60244258 runs 16 branches (scans/GUFHEU/bond_Zn-S3_neg ...)
[2026-10-25 04:50:35] pack: node job 60244261 runs 16 branches (scans/HOMQAC/angle_S1-Zn-N3_neg ...)
[2026-10-25 04:50:43] pack: node job 60244265 runs 16 branches (scans/HOMQAC/bond_Zn-S2_neg ...)
[2026-10-25 04:50:48] pack: node job 60244298 runs 16 branches (scans/ICAVAK/angle_N3-Zn-N4_neg ...)
[2026-10-25 04:50:48] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
[2026-10-25 05:03:23] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
[2026-10-25 05:15:32] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
[2026-10-25 05:27:37] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
```

## Last autopilot actions

```
queue: 0 continuations added to the front of queue/main (2600 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-25 04:24:40] submitting main capacity farm on ModCon, 6 h (queue 2600 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (2600 pending now)
2026-10-25 04:27:50 farm 8962257.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=2600
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
