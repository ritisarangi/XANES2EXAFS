# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 07:18 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7282 done, 0 started (running/stopped/failed), 2632 continuations ready, 261 not started, 10175 total
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
branches: 115 finished (115 copied back to Aurora), 424 running, 1 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 44
648 of your 3982 CPU node-hours on m5268 used
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
| NAMSOJ | 6 / 30 |
| NECTOG | 8 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 27 / 30 |
| OJELOE | 4 / 30 |
| RAYBIC | 4 / 30 |
| REJBUD | 12 / 30 |
| SONROE | 5 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 4 / 30 |
| WUJZOS | 28 / 30 |

Last driver actions:

```
[2026-10-26 06:46:25] scans/OJEKUJ/angle_S3-Zn-S4_pos finished (job 60240470)
[2026-10-26 06:46:25] status: 426 jobs queued/running, 114 branches finished (113 back on Aurora), 0 need review
[2026-10-26 06:58:53] scans/NAMSOJ/tilt_Zn-N3-C77-C82_neg finished (job 60240177)
[2026-10-26 06:58:53] status: 425 jobs queued/running, 115 branches finished (113 back on Aurora), 0 need review
[2026-10-26 07:11:10] scans/OJELOE/angle_S5-Zn-N100_pos FAILED (job 60240518, state completed): ['scans/OJELOE/angle_S5-Zn-N100_pos end 2026-10-25 23:57:28']
[2026-10-26 07:11:15] submitted 1 jobs
[2026-10-26 07:12:43] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-26 07:12:43] status: 425 jobs queued/running, 115 branches finished (115 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-26 04:04:58] publish: publish: 4 complexes added (1007 passing points), 0 not exported; 187 complexes published in total pushed: 35eccb6 Aurora results: 187 complexes published (2026-10-26 04:04) 
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 05:24:45] STATUS.md pushed
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
