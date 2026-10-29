# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-29 10:08 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7964 done, 384 started (running/stopped/failed), 1822 continuations ready, 5 not started, 10175 total
queue main: 1768 of 42267 waiting, 384 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,150.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8978689 | zn_main | capacity | 16 | 06:00 | R | 00:07 |
| 8978755 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 483 finished (481 copied back to Aurora), 57 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 165; failed runs: 91
1375 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 26 / 30 |
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
| WIGBIX | 29 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-29 09:06:37] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 09:17:38] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 09:28:02] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 09:38:29] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 09:48:54] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 09:59:53] scans/GUFHEU/tilt_Zn-S1-C9-C17_pos finished (job 60364808)
[2026-10-29 10:00:25] scans/WIGBIX/angle_S20-Zn-N45_pos finished (job 60361261)
[2026-10-29 10:00:25] status: 57 jobs queued/running, 483 branches finished (481 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-29 08:00:54] STATUS.md pushed
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
