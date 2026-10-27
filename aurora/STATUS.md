# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-27 03:00 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7542 done, 384 started (running/stopped/failed), 2173 continuations ready, 76 not started, 10175 total
queue main: 2039 of 40005 waiting, 384 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,728.8 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8965440 | zn_main | capacity | 16 | 06:00 | R | 04:10 |
| 8970790 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 333 finished (330 copied back to Aurora), 207 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 74
1051 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 17 / 30 |
| GUCSED | 26 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 23 / 30 |
| ICAVAK | 29 / 30 |
| NAMSOJ | 27 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 5 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 20 / 30 |
| RAYBIC | 17 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 14 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 27 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-27 02:31:27] scans/DOZVOF/twist_S1-N3-S2-N5_neg finished (job 60244244)
[2026-10-27 02:31:35] submitted 2 jobs
[2026-10-27 02:41:21] copied 16 finished branches back to Aurora: SUCCEEDED
[2026-10-27 02:41:21] status: 210 jobs queued/running, 330 branches finished (330 back on Aurora), 0 need review
[2026-10-27 02:52:47] scans/NAMSOJ/angle_N1-Zn-N2_pos finished (job 60240096)
[2026-10-27 02:53:19] scans/NONLEI/angle_N3-Zn-N4_pos finished (job 60240357)
[2026-10-27 02:53:51] scans/SONROE/angle_N115-Zn-N116_pos finished (job 60240851)
[2026-10-27 02:53:51] status: 207 jobs queued/running, 333 branches finished (330 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2078 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2073 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 00:50:53] STATUS.md pushed
prioritize main: 0 of 2064 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2052 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 2039 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
