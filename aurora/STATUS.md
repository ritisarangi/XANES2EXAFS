# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-25 07:33 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7080 done, 0 started (running/stopped/failed), 2791 continuations ready, 304 not started, 10175 total
queue main: 2600 of 39624 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,851.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8962257 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 45 finished (45 copied back to Aurora), 152 running, 343 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 2
20 of your 3982 CPU node-hours on m5268 used
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
| NAMSOJ | 0 / 30 |
| NECTOG | 0 / 30 |
| NONLEI | 0 / 30 |
| OJEKUJ | 16 / 30 |
| OJELOE | 0 / 30 |
| RAYBIC | 2 / 30 |
| REJBUD | 0 / 30 |
| SONROE | 1 / 30 |
| WIGBIX | 0 / 30 |
| WORMAR | 0 / 30 |
| WUJZOS | 26 / 30 |

Last driver actions:

```
[2026-10-25 06:28:14] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
[2026-10-25 06:40:21] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
[2026-10-25 06:52:25] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
[2026-10-25 07:05:11] scans/NAMSOJ/angle_N1-Zn-S4_pos FAILED (job 60240111, state completed): ['scans/NAMSOJ/angle_N1-Zn-S4_pos end 2026-10-25 00:02:33']
[2026-10-25 07:05:14] submitted 1 jobs
[2026-10-25 07:05:14] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
[2026-10-25 07:17:19] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
[2026-10-25 07:29:25] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 05:28:16] STATUS.md pushed
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
