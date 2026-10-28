# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-28 05:55 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7721 done, 768 started (running/stopped/failed), 1672 continuations ready, 14 not started, 10175 total
queue main: 1596 of 40761 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,536.0 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8972496 | zn_main | capacity | 16 | 06:00 | R | 03:10 |
| 8972593 | zn_main | capacity | 16 | 06:00 | R | 01:48 |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 453 finished (451 copied back to Aurora), 87 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 119; failed runs: 90
1260 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 28 / 30 |
| GUFHEU | 22 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 29 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 29 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 29 / 30 |
| WIGBIX | 10 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-28 04:59:01] status: 89 jobs queued/running, 451 branches finished (451 back on Aurora), 0 need review
[2026-10-28 05:09:55] status: 89 jobs queued/running, 451 branches finished (451 back on Aurora), 0 need review
[2026-10-28 05:20:34] status: 89 jobs queued/running, 451 branches finished (451 back on Aurora), 0 need review
[2026-10-28 05:31:13] status: 89 jobs queued/running, 451 branches finished (451 back on Aurora), 0 need review
[2026-10-28 05:42:18] scans/WIGBIX/angle_N39-Zn-N45_pos finished (job 60361248)
[2026-10-28 05:42:51] scans/NONLEI/twist_N1-N3-N2-N4_neg finished (job 60359463)
[2026-10-28 05:42:51] status: 87 jobs queued/running, 453 branches finished (451 back on Aurora), 0 need review
[2026-10-28 05:53:28] status: 87 jobs queued/running, 453 branches finished (451 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 03:53:42] STATUS.md pushed
prioritize main: 0 of 1607 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1603 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1599 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
