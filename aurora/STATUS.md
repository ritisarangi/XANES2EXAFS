# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-28 17:16 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7901 done, 768 started (running/stopped/failed), 1500 continuations ready, 6 not started, 10175 total
queue main: 1440 of 41520 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,343.5 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8976721 | zn_main | capacity | 16 | 06:00 | R | 04:12 |
| 8976814 | zn_main | capacity | 16 | 06:00 | R | 04:10 |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 474 finished (474 copied back to Aurora), 66 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 121; failed runs: 91
1316 of your 3982 CPU node-hours on m5268 used
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
| WIGBIX | 22 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-28 16:17:34] scans/WIGBIX/tilt_Zn-S1-C2-C7_neg finished (job 60398075)
[2026-10-28 16:18:35] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-28 16:18:35] status: 66 jobs queued/running, 474 branches finished (474 back on Aurora), 0 need review
[2026-10-28 16:29:02] status: 66 jobs queued/running, 474 branches finished (474 back on Aurora), 0 need review
[2026-10-28 16:39:36] status: 66 jobs queued/running, 474 branches finished (474 back on Aurora), 0 need review
[2026-10-28 16:50:01] status: 66 jobs queued/running, 474 branches finished (474 back on Aurora), 0 need review
[2026-10-28 17:01:06] status: 66 jobs queued/running, 474 branches finished (474 back on Aurora), 0 need review
[2026-10-28 17:11:40] status: 66 jobs queued/running, 474 branches finished (474 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 0 of 1513 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1509 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 14:59:47] STATUS.md pushed
prioritize main: 0 of 1492 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1473 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1452 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 17:16:09] publish: publish: 1 complexes added (288 passing points), 0 not exported; 213 complexes published in total pushed: 9b86f73 Aurora results: 213 complexes published (2026-10-28 17:16) 
```
