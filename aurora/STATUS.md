# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-27 17:28 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7678 done, 0 started (running/stopped/failed), 2472 continuations ready, 25 not started, 10175 total
queue main: 2377 of 40761 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,536.0 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8972496 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8972593 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 420 finished (420 copied back to Aurora), 120 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 115; failed runs: 90
1182 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 27 / 30 |
| GUFHEU | 13 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 22 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 29 / 30 |
| RAYBIC | 25 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 24 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-27 16:47:23] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-27 16:47:23] status: 122 jobs queued/running, 418 branches finished (418 back on Aurora), 0 need review
[2026-10-27 16:58:42] scans/NONLEI/angle_N2-Zn-N3_pos finished (job 60358668)
[2026-10-27 16:58:42] status: 121 jobs queued/running, 419 branches finished (418 back on Aurora), 0 need review
[2026-10-27 17:10:01] scans/NONLEI/tilt_Zn-N2-C14-C16_pos finished (job 60358978)
[2026-10-27 17:10:01] status: 120 jobs queued/running, 420 branches finished (418 back on Aurora), 0 need review
[2026-10-27 17:22:22] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-27 17:22:22] status: 120 jobs queued/running, 420 branches finished (420 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 15:08:43] publish: publish: 4 complexes added (1277 passing points), 0 not exported; 206 complexes published in total pushed: 8aa87e0 Aurora results: 206 complexes published (2026-10-27 15:08) 
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 15:50:33] STATUS.md pushed
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 60 of 2377 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
