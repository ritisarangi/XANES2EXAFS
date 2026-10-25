# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-25 22:40 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7218 done, 384 started (running/stopped/failed), 2288 continuations ready, 285 not started, 10175 total
queue main: 2119 of 39624 waiting, 384 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,850.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8962257 | zn_main | capacity | 16 | 06:00 | R | 04:42 |
| 8965440 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 86 finished (86 copied back to Aurora), 454 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 29
400 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 0 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 0 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 0 / 30 |
| ICAVAK | 2 / 30 |
| NAMSOJ | 2 / 30 |
| NECTOG | 4 / 30 |
| NONLEI | 4 / 30 |
| OJEKUJ | 25 / 30 |
| OJELOE | 3 / 30 |
| RAYBIC | 3 / 30 |
| REJBUD | 4 / 30 |
| SONROE | 4 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 4 / 30 |
| WUJZOS | 27 / 30 |

Last driver actions:

```
[2026-10-25 21:45:08] scans/ICAVAK/tilt_Zn-N4-C69-C74_pos finished (job 60257003)
[2026-10-25 21:45:08] status: 454 jobs queued/running, 86 branches finished (84 back on Aurora), 0 need review
[2026-10-25 21:56:58] status: 454 jobs queued/running, 86 branches finished (84 back on Aurora), 0 need review
[2026-10-25 22:10:19] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-25 22:10:19] status: 454 jobs queued/running, 86 branches finished (86 back on Aurora), 0 need review
[2026-10-25 22:22:10] status: 454 jobs queued/running, 86 branches finished (86 back on Aurora), 0 need review
[2026-10-25 22:34:04] status: 454 jobs queued/running, 86 branches finished (86 back on Aurora), 0 need review
[2026-10-25 22:45:56] status: 454 jobs queued/running, 86 branches finished (86 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 0 of 2178 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2169 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 20:35:56] STATUS.md pushed
prioritize main: 0 of 2154 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2144 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 22:04:43] publish: publish: 16 complexes added (4126 passing points), 2 not exported; 183 complexes published in total pushed: c56334e Aurora results: 183 complexes published (2026-10-25 22:04) 
prioritize main: 0 of 2123 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
