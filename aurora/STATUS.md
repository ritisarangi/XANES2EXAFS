# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-11-01 13:17 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 10075 done, 86 started (running/stopped/failed), 14 continuations ready, 0 not started, 10175 total
queue main: 0 of 45552 waiting, 85 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 41,414.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 9013664 | zn_main | small | 256 | 04:00 | Q | -- |
| 9013865 | zn_main | small | 256 | 06:00 | Q | -- |
| 9019151 | zn_main | capacity | 16 | 06:00 | R | 02:30 |
| 9024268 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 946 finished (946 copied back to Aurora), 14 running, 0 queued, 0 need review, 960 total
stops at the 48 h limit so far: 201; failed runs: 93
1455 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 29 / 30 |
| CAWKIW | 30 / 30 |
| DOZVOF | 30 / 30 |
| FAXYIP | 30 / 30 |
| FUXMAM | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 30 / 30 |
| JUQXUO | 30 / 30 |
| LAJGIM | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 30 / 30 |
| SONROE | 30 / 30 |
| TELRUZ | 30 / 30 |
| TEYSOG | 30 / 30 |
| TIFNUU | 30 / 30 |
| UWAVOF | 30 / 30 |
| UYORAE | 17 / 30 |
| WEQZAT01 | 30 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-11-01 12:32:12] status: 15 jobs queued/running, 945 branches finished (943 back on Aurora), 0 need review
[2026-11-01 12:43:01] scans/SEJZOW/twist_S1-S2-S3-N4_neg finished (job 60553311)
[2026-11-01 12:45:22] copied 3 finished branches back to Aurora: SUCCEEDED
[2026-11-01 12:45:22] status: 14 jobs queued/running, 946 branches finished (946 back on Aurora), 0 need review
[2026-11-01 12:55:32] status: 14 jobs queued/running, 946 branches finished (946 back on Aurora), 0 need review
[2026-11-01 13:05:42] status: 14 jobs queued/running, 946 branches finished (946 back on Aurora), 0 need review
[2026-11-01 13:15:52] status: 14 jobs queued/running, 946 branches finished (946 back on Aurora), 0 need review
[2026-11-01 13:26:01] status: 14 jobs queued/running, 946 branches finished (946 back on Aurora), 0 need review
```

## Last autopilot actions

```
nothing left to run
[2026-11-01 11:48:19] submitting main capacity farm on ModCon, 6 h (queue 0 left, 114 with running)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 9013664 9013865 9019151): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (0 pending now)
2026-11-01 12:26:08 farm 9024268.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=0
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-11-01 13:17:50] publish: publish: 15 complexes added (3898 passing points), 1 not exported; 300 complexes published in total pushed: 082b75e Aurora results: 300 complexes published (2026-11-01 13:17) 
```
