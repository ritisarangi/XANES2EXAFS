# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 03:15 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7266 done, 0 started (running/stopped/failed), 2634 continuations ready, 275 not started, 10175 total
queue main: 2468 of 40005 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,754.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8965440 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 100 finished (100 copied back to Aurora), 439 running, 1 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 38
540 of your 3982 CPU node-hours on m5268 used
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
| NAMSOJ | 3 / 30 |
| NECTOG | 6 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 26 / 30 |
| OJELOE | 4 / 30 |
| RAYBIC | 4 / 30 |
| REJBUD | 4 / 30 |
| SONROE | 4 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 4 / 30 |
| WUJZOS | 28 / 30 |

Last driver actions:

```
[2026-10-26 02:40:43] status: 441 jobs queued/running, 99 branches finished (99 back on Aurora), 0 need review
[2026-10-26 02:52:31] status: 441 jobs queued/running, 99 branches finished (99 back on Aurora), 0 need review
[2026-10-26 03:04:18] status: 441 jobs queued/running, 99 branches finished (99 back on Aurora), 0 need review
[2026-10-26 03:16:40] scans/NECTOG/bond_Zn-N5_pos finished (job 60240262)
[2026-10-26 03:17:13] scans/NECTOG/angle_N5-Zn-N6_pos FAILED (job 60240223, state completed): ['scans/NECTOG/angle_N5-Zn-N6_pos end 2026-10-25 20:06:43']
[2026-10-26 03:17:23] submitted 1 jobs
[2026-10-26 03:18:19] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-26 03:18:19] status: 440 jobs queued/running, 100 branches finished (100 back on Aurora), 0 need review
```

## Last autopilot actions

```
NODES=0: queue updated, no farm submitted
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 01:13:29] STATUS.md pushed
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
