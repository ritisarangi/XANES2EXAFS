# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-27 15:38 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7670 done, 0 started (running/stopped/failed), 2480 continuations ready, 25 not started, 10175 total
queue main: 2377 of 40761 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,536.0 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8972496 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8972593 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 415 finished (412 copied back to Aurora), 125 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 114; failed runs: 90
1166 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 27 / 30 |
| GUFHEU | 13 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 20 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 29 / 30 |
| RAYBIC | 23 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 23 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-27 15:02:04] status: 128 jobs queued/running, 412 branches finished (412 back on Aurora), 0 need review
[2026-10-27 15:12:54] status: 128 jobs queued/running, 412 branches finished (412 back on Aurora), 0 need review
[2026-10-27 15:23:43] status: 128 jobs queued/running, 412 branches finished (412 back on Aurora), 0 need review
[2026-10-27 15:34:34] status: 128 jobs queued/running, 412 branches finished (412 back on Aurora), 0 need review
[2026-10-27 15:45:59] scans/RAYBIC/twist_N1-N2-N3-S4_pos finished (job 60360740)
[2026-10-27 15:46:31] scans/SONROE/bond_Zn-N115_pos finished (job 60361246)
[2026-10-27 15:47:03] scans/RAYBIC/angle_N1-Zn-N2_neg finished (job 60360078)
[2026-10-27 15:47:03] status: 125 jobs queued/running, 415 branches finished (412 back on Aurora), 0 need review
```

## Last autopilot actions

```
NODES=0: queue updated, no farm submitted
[2026-10-27 13:32:57] submitting main capacity farm on ModCon, 6 h (queue 2377 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (2377 pending now)
2026-10-27 14:11:31 farm 8972496.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=2377
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 15:08:43] publish: publish: 4 complexes added (1277 passing points), 0 not exported; 206 complexes published in total pushed: 8aa87e0 Aurora results: 206 complexes published (2026-10-27 15:08) 
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
