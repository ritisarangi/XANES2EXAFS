# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-26 09:26 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7290 done, 0 started (running/stopped/failed), 2629 continuations ready, 256 not started, 10175 total
queue main: 2468 of 40005 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,730.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8965440 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 127 finished (123 copied back to Aurora), 413 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 46
696 of your 3982 CPU node-hours on m5268 used
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
| NAMSOJ | 10 / 30 |
| NECTOG | 11 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 28 / 30 |
| OJELOE | 4 / 30 |
| RAYBIC | 4 / 30 |
| REJBUD | 13 / 30 |
| SONROE | 8 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 4 / 30 |
| WUJZOS | 28 / 30 |

Last driver actions:

```
[2026-10-26 09:08:45] copied 4 finished branches back to Aurora: SUCCEEDED
[2026-10-26 09:08:45] status: 417 jobs queued/running, 123 branches finished (123 back on Aurora), 0 need review
[2026-10-26 09:21:02] scans/NAMSOJ/angle_N1-Zn-N3_pos finished (job 60295094)
[2026-10-26 09:21:02] status: 416 jobs queued/running, 124 branches finished (123 back on Aurora), 0 need review
[2026-10-26 09:33:15] scans/NAMSOJ/twist_N1-N2-N3-S4_neg finished (job 60240189)
[2026-10-26 09:33:48] scans/SONROE/bond_Zn-N116_pos finished (job 60240892)
[2026-10-26 09:34:20] scans/NECTOG/angle_N4-Zn-N6_neg finished (job 60240207)
[2026-10-26 09:34:20] status: 413 jobs queued/running, 127 branches finished (123 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-26 07:24:24] STATUS.md pushed
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 79 of 2468 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
