# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-11-01 03:04 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 9900 done, 205 started (running/stopped/failed), 70 continuations ready, 0 not started, 10175 total
queue main: 0 of 45254 waiting, 204 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 41,609.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8994906 | zn_main | capacity | 16 | 06:00 | R | 05:04 |
| 8995873 | zn_main | capacity | 16 | 06:00 | H | -- |
| 9013664 | zn_main | small | 256 | 04:00 | Q | -- |
| 9013865 | zn_main | small | 256 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 894 finished (890 copied back to Aurora), 66 running, 0 queued, 0 need review, 960 total
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
| LAJGIM | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 26 / 30 |
| SONROE | 30 / 30 |
| TELRUZ | 28 / 30 |
| TEYSOG | 18 / 30 |
| TIFNUU | 30 / 30 |
| UWAVOF | 15 / 30 |
| UYORAE | 7 / 30 |
| WEQZAT01 | 29 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-11-01 02:54:00] copied 10 finished branches back to Aurora: SUCCEEDED
[2026-11-01 02:54:00] status: 70 jobs queued/running, 890 branches finished (890 back on Aurora), 0 need review
[2026-11-01 03:05:00] scans/LAJGIM/angle_S2-Zn-S3_neg finished (job 60628912)
[2026-11-01 03:05:32] scans/SEJZOW/angle_S1-Zn-S2_neg finished (job 60553238)
[2026-11-01 03:06:05] scans/WEQZAT01/angle_N3-Zn-N4_pos finished (job 60613507)
[2026-11-01 03:06:05] status: 67 jobs queued/running, 893 branches finished (890 back on Aurora), 0 need review
[2026-11-01 03:17:02] scans/TELRUZ/angle_S1-Zn-N5_neg finished (job 60613265)
[2026-11-01 03:17:02] status: 66 jobs queued/running, 894 branches finished (890 back on Aurora), 0 need review
```

## Last autopilot actions

```
2026-10-31 23:22:02 farm 9013865.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=prod nodes=256 hours=6 account=ModCon tasks_left=0
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-11-01 01:27:49] STATUS.md pushed
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
