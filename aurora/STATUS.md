# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-27 19:39 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7688 done, 0 started (running/stopped/failed), 2468 continuations ready, 19 not started, 10175 total
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
branches: 434 finished (430 copied back to Aurora), 105 running, 1 queued, 0 need review, 540 total
stops at the 48 h limit so far: 117; failed runs: 90
1197 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 27 / 30 |
| GUFHEU | 20 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 25 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 29 / 30 |
| RAYBIC | 26 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 27 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-27 19:23:12] scans/RAYBIC/angle_N2-Zn-N3_neg finished (job 60360085)
[2026-10-27 19:23:44] scans/GUFHEU/angle_S1-Zn-S2_pos finished (job 60367949)
[2026-10-27 19:24:18] scans/SONROE/bond_Zn-N117_pos finished (job 60367999)
[2026-10-27 19:24:50] scans/NONLEI/bond_Zn-N4_pos finished (job 60326006)
[2026-10-27 19:24:50] status: 106 jobs queued/running, 434 branches finished (430 back on Aurora), 0 need review
[2026-10-27 19:36:07] scans/WIGBIX/tilt_Zn-S1-C2-C7_neg stopped at the time limit (job 60276446); continues
[2026-10-27 19:36:12] submitted 1 jobs
[2026-10-27 19:36:12] status: 106 jobs queued/running, 434 branches finished (430 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 17:30:26] STATUS.md pushed
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 18:42:26] publish: publish: no newly finished complexes 
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
