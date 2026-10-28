# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-28 14:57 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7835 done, 768 started (running/stopped/failed), 1565 continuations ready, 7 not started, 10175 total
queue main: 1503 of 41520 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,343.5 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8976721 | zn_main | capacity | 16 | 06:00 | R | 01:50 |
| 8976814 | zn_main | capacity | 16 | 06:00 | R | 01:48 |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 472 finished (471 copied back to Aurora), 68 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 121; failed runs: 91
1303 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 29 / 30 |
| GUCSED | 29 / 30 |
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
| WIGBIX | 21 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-28 13:56:03] status: 69 jobs queued/running, 471 branches finished (470 back on Aurora), 0 need review
[2026-10-28 14:07:34] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-28 14:07:34] status: 69 jobs queued/running, 471 branches finished (471 back on Aurora), 0 need review
[2026-10-28 14:18:02] status: 69 jobs queued/running, 471 branches finished (471 back on Aurora), 0 need review
[2026-10-28 14:28:34] status: 69 jobs queued/running, 471 branches finished (471 back on Aurora), 0 need review
[2026-10-28 14:39:02] status: 69 jobs queued/running, 471 branches finished (471 back on Aurora), 0 need review
[2026-10-28 14:50:11] scans/WIGBIX/bond_Zn-S1_pos finished (job 60361665)
[2026-10-28 14:50:11] status: 68 jobs queued/running, 472 branches finished (471 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 125 of 2285 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 125 of 2285 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 12:46:55] STATUS.md pushed
prioritize main: 0 of 1517 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1513 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1509 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
