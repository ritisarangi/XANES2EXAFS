# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-29 22:55 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8205 done, 767 started (running/stopped/failed), 1201 continuations ready, 2 not started, 10175 total
queue main: 1045 of 42898 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,916.7 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8985662 | zn_main | capacity | 16 | 06:00 | R | 02:48 |
| 8986279 | zn_main | capacity | 16 | 06:00 | R | 02:48 |

## NERSC Perlmutter (big pool)

The 22 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 505 finished (505 copied back to Aurora), 125 running, 30 queued, 0 need review, 660 total
stops at the 48 h limit so far: 173; failed runs: 91
1415 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 10 / 30 |
| CAPWIB | 3 / 30 |
| CATZUS10 | 14 / 30 |
| DOZVOF | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 28 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 0 / 30 |
| LAJGIM | 0 / 30 |
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
[2026-10-29 22:03:34] status: 156 jobs queued/running, 504 branches finished (503 back on Aurora), 0 need review
[2026-10-29 22:18:05] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-29 22:18:05] status: 156 jobs queued/running, 504 branches finished (504 back on Aurora), 0 need review
[2026-10-29 22:29:29] scans/BUNNII/twist_S128-S130-S132-S134_pos finished (job 60447329)
[2026-10-29 22:29:29] status: 155 jobs queued/running, 505 branches finished (504 back on Aurora), 0 need review
[2026-10-29 22:40:24] status: 155 jobs queued/running, 505 branches finished (504 back on Aurora), 0 need review
[2026-10-29 22:52:15] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-29 22:52:15] status: 155 jobs queued/running, 505 branches finished (505 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1107 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1106 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-29 20:54:20] STATUS.md pushed
prioritize main: 0 of 1102 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1089 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1048 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
