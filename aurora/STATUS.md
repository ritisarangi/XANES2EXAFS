# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-25 20:33 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7158 done, 384 started (running/stopped/failed), 2341 continuations ready, 292 not started, 10175 total
queue main: 2169 of 39624 waiting, 384 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,850.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8962257 | zn_main | capacity | 16 | 06:00 | R | 02:26 |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 78 finished (76 copied back to Aurora), 461 running, 1 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 27
342 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 0 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 0 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 0 / 30 |
| ICAVAK | 0 / 30 |
| NAMSOJ | 2 / 30 |
| NECTOG | 3 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 24 / 30 |
| OJELOE | 3 / 30 |
| RAYBIC | 3 / 30 |
| REJBUD | 4 / 30 |
| SONROE | 4 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 0 / 30 |
| WUJZOS | 27 / 30 |

Last driver actions:

```
[2026-10-25 20:21:08] scans/OJEKUJ/angle_S1-Zn-S4_neg finished (job 60240444)
[2026-10-25 20:21:42] scans/WORMAR/angle_S2-Zn-N8_neg FAILED (job 60241201, state completed): ['scans/WORMAR/angle_S2-Zn-N8_neg end 2026-10-25 13:06:37']
[2026-10-25 20:22:14] scans/OJEKUJ/angle_S1-Zn-S3_neg finished (job 60240435)
[2026-10-25 20:22:18] submitted 1 jobs
[2026-10-25 20:22:18] status: 462 jobs queued/running, 78 branches finished (76 back on Aurora), 0 need review
[2026-10-25 20:34:47] scans/RAYBIC/angle_N2-Zn-S4_neg FAILED (job 60240615, state completed): ['scans/RAYBIC/angle_N2-Zn-S4_neg end 2026-10-25 13:25:20']
[2026-10-25 20:34:51] submitted 1 jobs
[2026-10-25 20:34:51] status: 462 jobs queued/running, 78 branches finished (76 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 18:04:10] STATUS.md pushed
prioritize main: 0 of 2209 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2197 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2178 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2169 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
