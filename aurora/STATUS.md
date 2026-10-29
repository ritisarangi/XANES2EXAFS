# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-29 01:43 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7963 done, 0 started (running/stopped/failed), 2206 continuations ready, 6 not started, 10175 total
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
branches: 480 finished (480 copied back to Aurora), 60 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 123; failed runs: 91
1347 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 29 / 30 |
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
[2026-10-29 00:37:46] status: 60 jobs queued/running, 480 branches finished (480 back on Aurora), 0 need review
[2026-10-29 00:48:14] status: 60 jobs queued/running, 480 branches finished (480 back on Aurora), 0 need review
[2026-10-29 00:58:39] status: 60 jobs queued/running, 480 branches finished (480 back on Aurora), 0 need review
[2026-10-29 01:09:03] status: 60 jobs queued/running, 480 branches finished (480 back on Aurora), 0 need review
[2026-10-29 01:19:30] status: 60 jobs queued/running, 480 branches finished (480 back on Aurora), 0 need review
[2026-10-29 01:29:53] status: 60 jobs queued/running, 480 branches finished (480 back on Aurora), 0 need review
[2026-10-29 01:40:24] status: 60 jobs queued/running, 480 branches finished (480 back on Aurora), 0 need review
[2026-10-29 01:50:50] status: 60 jobs queued/running, 480 branches finished (480 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 23:13:04] publish: publish: no newly finished complexes 
[2026-10-28 23:26:48] STATUS.md pushed
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 156 of 2152 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
