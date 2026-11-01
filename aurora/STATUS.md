# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-11-01 17:46 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 10149 done, 0 started (running/stopped/failed), 26 continuations ready, 0 not started, 10175 total
queue main: 22 of 45574 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 41,318.4 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 9013664 | zn_main | small | 256 | 04:00 | Q | -- |
| 9013865 | zn_main | small | 256 | 06:00 | Q | -- |
| 9024268 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 9027818 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 956 finished (956 copied back to Aurora), 4 running, 0 queued, 0 need review, 960 total
stops at the 48 h limit so far: 201; failed runs: 93
1455 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 30 / 30 |
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
| UYORAE | 26 / 30 |
| WEQZAT01 | 30 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-11-01 17:01:09] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-11-01 17:01:09] status: 5 jobs queued/running, 955 branches finished (955 back on Aurora), 0 need review
[2026-11-01 17:11:48] scans/UYORAE/angle_N7-Zn-N12_neg finished (job 60630032)
[2026-11-01 17:11:48] status: 4 jobs queued/running, 956 branches finished (955 back on Aurora), 0 need review
[2026-11-01 17:21:54] status: 4 jobs queued/running, 956 branches finished (955 back on Aurora), 0 need review
[2026-11-01 17:32:55] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-11-01 17:32:55] status: 4 jobs queued/running, 956 branches finished (956 back on Aurora), 0 need review
[2026-11-01 17:43:02] status: 4 jobs queued/running, 956 branches finished (956 back on Aurora), 0 need review
```

## Last autopilot actions

```
no stopped branches found
main farm jobs already queued or running (8939977 9013664 9013865 9024268): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (22 pending now)
NODES=0: queue updated, no farm submitted
[2026-11-01 17:41:43] submitting main capacity farm on ModCon, 6 h (queue 22 left, 22 with running)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 9013664 9013865 9024268): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (22 pending now)
2026-11-01 17:44:52 farm 9027818.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=22
prioritize main: 22 of 22 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
