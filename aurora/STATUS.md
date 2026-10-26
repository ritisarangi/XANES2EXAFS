# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 05:18 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7274 done, 0 started (running/stopped/failed), 2634 continuations ready, 267 not started, 10175 total
queue main: 2468 of 40005 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,742.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8965440 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 107 finished (107 copied back to Aurora), 433 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 41
594 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 0 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 0 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 0 / 30 |
| ICAVAK | 9 / 30 |
| NAMSOJ | 5 / 30 |
| NECTOG | 8 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 26 / 30 |
| OJELOE | 4 / 30 |
| RAYBIC | 4 / 30 |
| REJBUD | 7 / 30 |
| SONROE | 4 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 4 / 30 |
| WUJZOS | 28 / 30 |

Last driver actions:

```
[2026-10-26 04:37:04] status: 434 jobs queued/running, 106 branches finished (106 back on Aurora), 0 need review
[2026-10-26 04:49:25] scans/OJELOE/bond_Zn-S4_pos FAILED (job 60240546, state completed): ['scans/OJELOE/bond_Zn-S4_pos end 2026-10-25 21:34:35']
[2026-10-26 04:49:57] scans/NAMSOJ/tilt_Zn-S4-C5-O7_pos finished (job 60275033)
[2026-10-26 04:50:02] submitted 1 jobs
[2026-10-26 04:50:02] status: 433 jobs queued/running, 107 branches finished (106 back on Aurora), 0 need review
[2026-10-26 05:02:19] status: 433 jobs queued/running, 107 branches finished (106 back on Aurora), 0 need review
[2026-10-26 05:14:56] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-26 05:14:56] status: 433 jobs queued/running, 107 branches finished (107 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 03:25:37] STATUS.md pushed
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 04:04:58] publish: publish: 4 complexes added (1007 passing points), 0 not exported; 187 complexes published in total pushed: 35eccb6 Aurora results: 187 complexes published (2026-10-26 04:04) 
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
