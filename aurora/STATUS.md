# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-11-01 01:07 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 9783 done, 297 started (running/stopped/failed), 95 continuations ready, 0 not started, 10175 total
queue main: 0 of 45254 waiting, 295 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 41,609.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8994906 | zn_main | capacity | 16 | 06:00 | R | 03:10 |
| 8995873 | zn_main | capacity | 16 | 06:00 | H | -- |
| 9013664 | zn_main | small | 256 | 04:00 | Q | -- |
| 9013865 | zn_main | small | 256 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 872 finished (865 copied back to Aurora), 88 running, 0 queued, 0 need review, 960 total
stops at the 48 h limit so far: 201; failed runs: 93
1453 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 28 / 30 |
| CAWKIW | 30 / 30 |
| DOZVOF | 30 / 30 |
| FAXYIP | 23 / 30 |
| FUXMAM | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 30 / 30 |
| JUQXUO | 30 / 30 |
| LAJGIM | 27 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 24 / 30 |
| SONROE | 30 / 30 |
| TELRUZ | 24 / 30 |
| TEYSOG | 17 / 30 |
| TIFNUU | 29 / 30 |
| UWAVOF | 9 / 30 |
| UYORAE | 7 / 30 |
| WEQZAT01 | 24 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-11-01 01:02:52] scans/TELRUZ/angle_S2-Zn-N6_pos finished (job 60613305)
[2026-11-01 01:03:24] scans/TEYSOG/bond_Zn-S1_pos finished (job 60613393)
[2026-11-01 01:03:56] scans/WEQZAT01/twist_S1-S2-N3-N4_neg finished (job 60613562)
[2026-11-01 01:03:56] status: 91 jobs queued/running, 869 branches finished (865 back on Aurora), 0 need review
[2026-11-01 01:15:03] scans/JUQXUO/angle_S2-Zn-N11_pos finished (job 60553191)
[2026-11-01 01:15:36] scans/FAXYIP/angle_N7-Zn-N10_neg finished (job 60612988)
[2026-11-01 01:16:08] scans/UWAVOF/tilt_Zn-N7-C40-C45_pos finished (job 60613489)
[2026-11-01 01:16:08] status: 88 jobs queued/running, 872 branches finished (865 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-31 23:18:53] submitting main farm on ModCon, 6 h (queue 0 left, 2 main farms)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8994906 8995873 9013664): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (0 pending now)
2026-10-31 23:22:02 farm 9013865.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=prod nodes=256 hours=6 account=ModCon tasks_left=0
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
