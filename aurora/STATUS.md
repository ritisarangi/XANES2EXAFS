# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 20:37 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7431 done, 0 started (running/stopped/failed), 2608 continuations ready, 136 not started, 10175 total
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
branches: 266 finished (264 copied back to Aurora), 274 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 67
941 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 14 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 23 / 30 |
| ICAVAK | 28 / 30 |
| NAMSOJ | 21 / 30 |
| NECTOG | 27 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 16 / 30 |
| RAYBIC | 12 / 30 |
| REJBUD | 28 / 30 |
| SONROE | 12 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 13 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-26 20:25:49] scans/WORMAR/bond_Zn-N8_pos finished (job 60241224)
[2026-10-26 20:26:21] scans/REJBUD/angle_N1-Zn-N3_neg finished (job 60240711)
[2026-10-26 20:26:53] scans/OJELOE/angle_S5-Zn-N100_neg finished (job 60240516)
[2026-10-26 20:32:07] copied 9 finished branches back to Aurora: SUCCEEDED
[2026-10-26 20:32:07] status: 276 jobs queued/running, 264 branches finished (264 back on Aurora), 0 need review
[2026-10-26 20:43:56] scans/WORMAR/tilt_Zn-S2-C49-C39_pos finished (job 60241267)
[2026-10-26 20:44:28] scans/NAMSOJ/tilt_Zn-S4-C5-O7_neg finished (job 60255138)
[2026-10-26 20:44:28] status: 274 jobs queued/running, 266 branches finished (264 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 18:01:53] STATUS.md pushed
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
