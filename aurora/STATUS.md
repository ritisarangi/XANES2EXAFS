# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 13:40 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7344 done, 0 started (running/stopped/failed), 2622 continuations ready, 209 not started, 10175 total
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
branches: 177 finished (177 copied back to Aurora), 362 running, 1 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 55
801 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 0 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 0 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 23 / 30 |
| ICAVAK | 14 / 30 |
| NAMSOJ | 12 / 30 |
| NECTOG | 16 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 29 / 30 |
| OJELOE | 7 / 30 |
| RAYBIC | 4 / 30 |
| REJBUD | 18 / 30 |
| SONROE | 12 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 5 / 30 |
| WUJZOS | 29 / 30 |

Last driver actions:

```
[2026-10-26 13:06:09] status: 365 jobs queued/running, 175 branches finished (171 back on Aurora), 0 need review
[2026-10-26 13:18:12] scans/OJELOE/tilt_Zn-S3-C25-N102_neg finished (job 60240562)
[2026-10-26 13:18:12] status: 364 jobs queued/running, 176 branches finished (171 back on Aurora), 0 need review
[2026-10-26 13:30:11] scans/WIGBIX/angle_S1-Zn-S20_pos FAILED (job 60241000, state completed): ['scans/WIGBIX/angle_S1-Zn-S20_pos end 2026-10-26 06:28:59']
[2026-10-26 13:30:44] scans/REJBUD/angle_N1-Zn-S4_neg finished (job 60240718)
[2026-10-26 13:30:50] submitted 1 jobs
[2026-10-26 13:34:31] copied 6 finished branches back to Aurora: SUCCEEDED
[2026-10-26 13:34:31] status: 363 jobs queued/running, 177 branches finished (177 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 11:35:20] STATUS.md pushed
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
