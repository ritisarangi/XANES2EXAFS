# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-27 10:57 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7620 done, 384 started (running/stopped/failed), 2120 continuations ready, 51 not started, 10175 total
queue main: 2002 of 40383 waiting, 384 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,632.5 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8970790 | zn_main | capacity | 16 | 06:00 | R | 04:50 |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 374 finished (372 copied back to Aurora), 144 running, 22 queued, 0 need review, 540 total
stops at the 48 h limit so far: 103; failed runs: 80
1122 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 27 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 25 / 30 |
| ICAVAK | 29 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 10 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 25 / 30 |
| RAYBIC | 18 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 20 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-27 09:54:31] status: 168 jobs queued/running, 372 branches finished (372 back on Aurora), 0 need review
[2026-10-27 10:05:21] status: 168 jobs queued/running, 372 branches finished (372 back on Aurora), 0 need review
[2026-10-27 10:16:07] status: 168 jobs queued/running, 372 branches finished (372 back on Aurora), 0 need review
[2026-10-27 10:26:53] status: 168 jobs queued/running, 372 branches finished (372 back on Aurora), 0 need review
[2026-10-27 10:37:43] status: 168 jobs queued/running, 372 branches finished (372 back on Aurora), 0 need review
[2026-10-27 10:49:07] scans/NONLEI/angle_N2-Zn-N3_neg finished (job 60358664)
[2026-10-27 10:49:39] scans/HOMQAC/angle_S2-Zn-N4_pos finished (job 60309216)
[2026-10-27 10:49:39] status: 166 jobs queued/running, 374 branches finished (372 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2019 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2015 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 09:02:17] STATUS.md pushed
prioritize main: 0 of 2008 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2008 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2003 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
