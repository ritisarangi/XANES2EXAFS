# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-28 19:57 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7959 done, 0 started (running/stopped/failed), 2210 continuations ready, 6 not started, 10175 total
queue main: 2152 of 42267 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,152.0 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8978689 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 476 finished (476 copied back to Aurora), 63 running, 1 queued, 0 need review, 540 total
stops at the 48 h limit so far: 122; failed runs: 91
1328 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 29 / 30 |
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
| WIGBIX | 24 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-28 19:11:00] status: 66 jobs queued/running, 474 branches finished (474 back on Aurora), 0 need review
[2026-10-28 19:22:04] scans/WIGBIX/angle_S1-Zn-S20_neg finished (job 60361256)
[2026-10-28 19:22:04] status: 65 jobs queued/running, 475 branches finished (474 back on Aurora), 0 need review
[2026-10-28 19:33:07] scans/WIGBIX/angle_S1-Zn-N39_neg finished (job 60361251)
[2026-10-28 19:34:34] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-28 19:34:34] status: 64 jobs queued/running, 476 branches finished (476 back on Aurora), 0 need review
[2026-10-28 19:45:00] status: 64 jobs queued/running, 476 branches finished (476 back on Aurora), 0 need review
[2026-10-28 19:55:31] status: 64 jobs queued/running, 476 branches finished (476 back on Aurora), 0 need review
```

## Last autopilot actions

```
no stopped branches found
main farm jobs already queued or running (8939977): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (2152 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-28 19:45:46] submitting main capacity farm on ModCon, 6 h (queue 2152 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (2152 pending now)
2026-10-28 19:56:16 farm 8978689.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=2152
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
