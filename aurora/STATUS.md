# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-30 14:01 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8552 done, 0 started (running/stopped/failed), 1623 continuations ready, 0 not started, 10175 total
queue main: 1511 of 44402 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,534.7 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |
| 8990248 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 22 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 548 finished (548 copied back to Aurora), 112 running, 0 queued, 0 need review, 660 total
stops at the 48 h limit so far: 173; failed runs: 91
1438 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 25 / 30 |
| CAPWIB | 16 / 30 |
| CATZUS10 | 19 / 30 |
| DOZVOF | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 4 / 30 |
| LAJGIM | 4 / 30 |
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
[2026-10-30 13:26:06] scans/CAPWIB/twist_S8-N12-S10-N14_pos finished (job 60502471)
[2026-10-30 13:26:06] status: 113 jobs queued/running, 547 branches finished (546 back on Aurora), 0 need review
[2026-10-30 13:36:44] status: 113 jobs queued/running, 547 branches finished (546 back on Aurora), 0 need review
[2026-10-30 13:47:58] scans/CAPWIB/bond_Zn-S8_pos finished (job 60502455)
[2026-10-30 13:49:25] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-30 13:49:25] status: 112 jobs queued/running, 548 branches finished (548 back on Aurora), 0 need review
[2026-10-30 14:00:01] status: 112 jobs queued/running, 548 branches finished (548 back on Aurora), 0 need review
[2026-10-30 14:10:49] status: 112 jobs queued/running, 548 branches finished (548 back on Aurora), 0 need review
```

## Last autopilot actions

```
main farm jobs already queued or running (8939977 8987775 8988123): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (1511 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-30 13:13:03] submitting main capacity farm on ModCon, 6 h (queue 1511 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8987775): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (1511 pending now)
2026-10-30 13:41:38 farm 8990248.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=1511
prioritize main: 214 of 1511 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-30 14:01:49] publish: publish: 8 complexes added (2257 passing points), 0 not exported; 227 complexes published in total pushed: 4f0ff1c Aurora results: 227 complexes published (2026-10-30 14:01) 
```
