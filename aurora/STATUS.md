# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 15:50 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7360 done, 0 started (running/stopped/failed), 2619 continuations ready, 196 not started, 10175 total
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
branches: 198 finished (193 copied back to Aurora), 342 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 59
845 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 2 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 0 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 23 / 30 |
| ICAVAK | 14 / 30 |
| NAMSOJ | 13 / 30 |
| NECTOG | 21 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 9 / 30 |
| RAYBIC | 5 / 30 |
| REJBUD | 23 / 30 |
| SONROE | 12 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 9 / 30 |
| WUJZOS | 29 / 30 |

Last driver actions:

```
[2026-10-26 15:16:43] scans/OJELOE/tilt_Zn-S5-C75-N108_neg finished (job 60299037)
[2026-10-26 15:17:16] scans/RAYBIC/angle_N1-Zn-S4_pos FAILED (job 60254744, state completed): ['scans/RAYBIC/angle_N1-Zn-S4_pos end 2026-10-26 08:01:37']
[2026-10-26 15:17:49] scans/WORMAR/tilt_Zn-N4-C12-C11_pos finished (job 60241246)
[2026-10-26 15:17:52] submitted 1 jobs
[2026-10-26 15:17:52] status: 344 jobs queued/running, 196 branches finished (193 back on Aurora), 0 need review
[2026-10-26 15:29:57] scans/WORMAR/tilt_Zn-N8-C34-C33_pos finished (job 60241254)
[2026-10-26 15:30:30] scans/RAYBIC/tilt_Zn-S4-C94-H96_neg finished (job 60240689)
[2026-10-26 15:30:30] status: 342 jobs queued/running, 198 branches finished (193 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 13:42:09] STATUS.md pushed
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
