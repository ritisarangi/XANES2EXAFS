# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-29 14:24 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8070 done, 769 started (running/stopped/failed), 1333 continuations ready, 3 not started, 10175 total
queue main: 1283 of 42267 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,149.2 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8978689 | zn_main | capacity | 16 | 06:00 | R | 04:26 |
| 8978755 | zn_main | capacity | 16 | 06:00 | R | 03:50 |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 487 finished (487 copied back to Aurora), 53 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 171; failed runs: 91
1389 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 6 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 27 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 30 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-29 13:36:30] status: 55 jobs queued/running, 485 branches finished (485 back on Aurora), 0 need review
[2026-10-29 13:46:54] status: 55 jobs queued/running, 485 branches finished (485 back on Aurora), 0 need review
[2026-10-29 13:57:54] scans/BUNNII/bond_Zn-S128_pos finished (job 60410259)
[2026-10-29 13:57:54] status: 54 jobs queued/running, 486 branches finished (485 back on Aurora), 0 need review
[2026-10-29 14:08:53] scans/BUNNII/tilt_Zn-S134-C90-S135_neg finished (job 60478576)
[2026-10-29 14:10:19] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-29 14:10:19] status: 53 jobs queued/running, 487 branches finished (487 back on Aurora), 0 need review
[2026-10-29 14:20:42] status: 53 jobs queued/running, 487 branches finished (487 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 0 of 1371 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-29 11:38:15] publish: publish: 1 complexes added (216 passing points), 0 not exported; 215 complexes published in total pushed: 5b43b8e Aurora results: 215 complexes published (2026-10-29 11:38) 
prioritize main: 0 of 1357 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-29 12:19:09] STATUS.md pushed
prioritize main: 0 of 1335 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1314 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1291 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
