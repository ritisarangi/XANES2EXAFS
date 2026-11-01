# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-11-01 15:08 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 10125 done, 38 started (running/stopped/failed), 12 continuations ready, 0 not started, 10175 total
queue main: 0 of 45552 waiting, 37 ORCA runs active
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
| 9019151 | zn_main | capacity | 16 | 06:00 | R | 04:20 |
| 9024268 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 950 finished (950 copied back to Aurora), 10 running, 0 queued, 0 need review, 960 total
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
| UYORAE | 20 / 30 |
| WEQZAT01 | 30 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-11-01 14:39:47] status: 12 jobs queued/running, 948 branches finished (948 back on Aurora), 0 need review
[2026-11-01 14:49:57] status: 12 jobs queued/running, 948 branches finished (948 back on Aurora), 0 need review
[2026-11-01 15:00:08] status: 12 jobs queued/running, 948 branches finished (948 back on Aurora), 0 need review
[2026-11-01 15:10:53] scans/UYORAE/bond_Zn-S1_pos finished (job 60630739)
[2026-11-01 15:11:25] scans/UYORAE/angle_S1-Zn-S2_neg finished (job 60630706)
[2026-11-01 15:11:25] status: 10 jobs queued/running, 950 branches finished (948 back on Aurora), 0 need review
[2026-11-01 15:23:28] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-11-01 15:23:28] status: 10 jobs queued/running, 950 branches finished (950 back on Aurora), 0 need review
```

## Last autopilot actions

```
queue: 0 continuations added to the front of queue/main (0 pending now)
2026-11-01 12:26:08 farm 9024268.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=0
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-11-01 13:17:50] publish: publish: 15 complexes added (3898 passing points), 1 not exported; 300 complexes published in total pushed: 082b75e Aurora results: 300 complexes published (2026-11-01 13:17) 
[2026-11-01 13:35:56] STATUS.md pushed
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
