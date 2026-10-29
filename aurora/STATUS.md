# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-29 07:59 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7964 done, 0 started (running/stopped/failed), 2206 continuations ready, 5 not started, 10175 total
queue main: 2152 of 42267 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,150.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8978689 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8978755 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 481 finished (481 copied back to Aurora), 50 running, 9 queued, 0 need review, 540 total
stops at the 48 h limit so far: 165; failed runs: 91
1368 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 25 / 30 |
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
| WIGBIX | 28 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-29 06:50:53] driver started (540 branches, account m5268)
[2026-10-29 06:51:14] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 07:01:37] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 07:12:01] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 07:22:27] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 07:32:50] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 07:43:17] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
[2026-10-29 07:53:40] status: 59 jobs queued/running, 481 branches finished (481 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-29 05:27:53] publish: publish: 1 complexes added (294 passing points), 0 not exported; 214 complexes published in total pushed: 8d37ba8 Aurora results: 214 complexes published (2026-10-29 05:27) 
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-29 05:58:50] STATUS.md pushed
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
