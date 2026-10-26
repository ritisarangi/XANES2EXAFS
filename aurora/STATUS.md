# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 18:00 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7407 done, 0 started (running/stopped/failed), 2613 continuations ready, 155 not started, 10175 total
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
branches: 245 finished (240 copied back to Aurora), 295 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 65
905 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 13 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 23 / 30 |
| ICAVAK | 28 / 30 |
| NAMSOJ | 16 / 30 |
| NECTOG | 25 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 13 / 30 |
| RAYBIC | 9 / 30 |
| REJBUD | 26 / 30 |
| SONROE | 12 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 9 / 30 |
| WUJZOS | 29 / 30 |

Last driver actions:

```
[2026-10-26 17:33:04] status: 300 jobs queued/running, 240 branches finished (240 back on Aurora), 0 need review
[2026-10-26 17:45:01] scans/OJELOE/tilt_Zn-S3-C25-N102_pos finished (job 60240564)
[2026-10-26 17:45:34] scans/REJBUD/angle_N3-Zn-S4_neg finished (job 60240742)
[2026-10-26 17:46:08] scans/RAYBIC/tilt_Zn-N1-C9-C14_neg finished (job 60240656)
[2026-10-26 17:46:41] scans/OJELOE/tilt_Zn-N100-C13-C14_neg finished (job 60240555)
[2026-10-26 17:46:41] status: 296 jobs queued/running, 244 branches finished (240 back on Aurora), 0 need review
[2026-10-26 17:58:33] scans/NAMSOJ/angle_N2-Zn-N3_pos finished (job 60240121)
[2026-10-26 17:58:33] status: 295 jobs queued/running, 245 branches finished (240 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 15:52:03] STATUS.md pushed
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 16:08:37] publish: publish: 1 complexes added (266 passing points), 0 not exported; 188 complexes published in total pushed: 93082ff Aurora results: 188 complexes published (2026-10-26 16:08) 
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
