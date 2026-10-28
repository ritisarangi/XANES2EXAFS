# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-28 07:53 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7769 done, 768 started (running/stopped/failed), 1625 continuations ready, 13 not started, 10175 total
queue main: 1554 of 40761 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,536.0 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8972496 | zn_main | capacity | 16 | 06:00 | R | 05:04 |
| 8972593 | zn_main | capacity | 16 | 06:00 | R | 03:44 |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 456 finished (456 copied back to Aurora), 84 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 120; failed runs: 90
1269 of your 3982 CPU node-hours on m5268 used
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
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 29 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 29 / 30 |
| WIGBIX | 12 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-28 07:00:58] status: 85 jobs queued/running, 455 branches finished (454 back on Aurora), 0 need review
[2026-10-28 07:12:07] scans/WIGBIX/bond_Zn-N45_pos finished (job 60361263)
[2026-10-28 07:13:36] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-28 07:13:36] status: 84 jobs queued/running, 456 branches finished (456 back on Aurora), 0 need review
[2026-10-28 07:24:12] status: 84 jobs queued/running, 456 branches finished (456 back on Aurora), 0 need review
[2026-10-28 07:34:43] status: 84 jobs queued/running, 456 branches finished (456 back on Aurora), 0 need review
[2026-10-28 07:45:21] status: 84 jobs queued/running, 456 branches finished (456 back on Aurora), 0 need review
[2026-10-28 07:55:52] status: 84 jobs queued/running, 456 branches finished (456 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 0 of 1603 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1599 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 06:00:37] STATUS.md pushed
prioritize main: 0 of 1589 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1575 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 07:04:20] publish: publish: 3 complexes added (597 passing points), 0 not exported; 209 complexes published in total pushed: 5fc4836 Aurora results: 209 complexes published (2026-10-28 07:04) 
prioritize main: 0 of 1560 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
