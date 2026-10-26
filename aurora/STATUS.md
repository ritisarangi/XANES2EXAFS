# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 22:35 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7445 done, 0 started (running/stopped/failed), 2604 continuations ready, 126 not started, 10175 total
queue main: 2468 of 40005 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,728.8 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8965440 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 278 finished (278 copied back to Aurora), 262 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 68
975 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 14 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 23 / 30 |
| ICAVAK | 29 / 30 |
| NAMSOJ | 23 / 30 |
| NECTOG | 28 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 17 / 30 |
| RAYBIC | 15 / 30 |
| REJBUD | 28 / 30 |
| SONROE | 13 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 16 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-26 22:24:52] scans/NECTOG/angle_N4-Zn-N7_pos finished (job 60266730)
[2026-10-26 22:25:26] scans/WORMAR/twist_S1-N4-S2-N8_pos finished (job 60241272)
[2026-10-26 22:26:01] scans/SONROE/angle_N115-Zn-N117_neg FAILED (job 60240853, state completed): ['scans/SONROE/angle_N115-Zn-N117_neg end 2026-10-26 15:23:37']
[2026-10-26 22:26:33] scans/SONROE/twist_N114-N115-N116-N117_neg finished (job 60240956)
[2026-10-26 22:26:38] submitted 1 jobs
[2026-10-26 22:30:18] copied 6 finished branches back to Aurora: SUCCEEDED
[2026-10-26 22:30:18] status: 262 jobs queued/running, 278 branches finished (278 back on Aurora), 0 need review
[2026-10-26 22:41:26] status: 262 jobs queued/running, 278 branches finished (278 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 20:48:17] STATUS.md pushed
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 22:19:12] publish: publish: 1 complexes added (154 passing points), 0 not exported; 189 complexes published in total pushed: 61de745 Aurora results: 189 complexes published (2026-10-26 22:19) 
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
