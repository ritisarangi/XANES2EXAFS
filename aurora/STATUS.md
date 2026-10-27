# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-27 21:48 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7695 done, 0 started (running/stopped/failed), 2462 continuations ready, 18 not started, 10175 total
queue main: 2377 of 40761 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,536.0 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8972496 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8972593 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 438 finished (437 copied back to Aurora), 102 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 118; failed runs: 90
1210 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 28 / 30 |
| GUFHEU | 20 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 26 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 29 / 30 |
| RAYBIC | 27 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 28 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-27 20:57:46] status: 103 jobs queued/running, 437 branches finished (437 back on Aurora), 0 need review
[2026-10-27 21:09:28] scans/SONROE/angle_N116-Zn-N117_pos stopped at the time limit (job 60280637); continues
[2026-10-27 21:09:39] submitted 1 jobs
[2026-10-27 21:09:39] status: 103 jobs queued/running, 437 branches finished (437 back on Aurora), 0 need review
[2026-10-27 21:20:22] status: 103 jobs queued/running, 437 branches finished (437 back on Aurora), 0 need review
[2026-10-27 21:30:57] status: 103 jobs queued/running, 437 branches finished (437 back on Aurora), 0 need review
[2026-10-27 21:42:10] scans/GUCSED/tilt_Zn-N1-C5-C7_neg finished (job 60343875)
[2026-10-27 21:42:10] status: 102 jobs queued/running, 438 branches finished (437 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-27 18:42:26] publish: publish: no newly finished complexes 
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 19:40:44] STATUS.md pushed
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
