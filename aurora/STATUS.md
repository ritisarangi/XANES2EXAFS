# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-27 23:48 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7698 done, 0 started (running/stopped/failed), 2461 continuations ready, 16 not started, 10175 total
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
branches: 440 finished (440 copied back to Aurora), 100 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 119; failed runs: 90
1223 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 28 / 30 |
| GUFHEU | 21 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 26 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 29 / 30 |
| RAYBIC | 27 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 29 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-27 22:58:46] status: 100 jobs queued/running, 440 branches finished (438 back on Aurora), 0 need review
[2026-10-27 23:09:59] scans/BUNNII/bond_Zn-S128_pos stopped at the time limit (job 60286033); continues
[2026-10-27 23:10:03] submitted 1 jobs
[2026-10-27 23:11:32] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-27 23:11:32] status: 100 jobs queued/running, 440 branches finished (440 back on Aurora), 0 need review
[2026-10-27 23:22:13] status: 100 jobs queued/running, 440 branches finished (440 back on Aurora), 0 need review
[2026-10-27 23:32:48] status: 100 jobs queued/running, 440 branches finished (440 back on Aurora), 0 need review
[2026-10-27 23:43:28] status: 100 jobs queued/running, 440 branches finished (440 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 21:50:09] STATUS.md pushed
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
