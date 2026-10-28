# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-28 10:10 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7807 done, 0 started (running/stopped/failed), 2356 continuations ready, 12 not started, 10175 total
queue main: 2285 of 41520 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,439.7 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8976721 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 462 finished (457 copied back to Aurora), 78 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 120; failed runs: 91
1279 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 28 / 30 |
| GUCSED | 28 / 30 |
| GUFHEU | 23 / 30 |
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
| WIGBIX | 15 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-28 09:22:47] status: 83 jobs queued/running, 457 branches finished (457 back on Aurora), 0 need review
[2026-10-28 09:33:55] scans/WIGBIX/tilt_Zn-N45-C46-C47_pos finished (job 60361681)
[2026-10-28 09:34:27] scans/SONROE/angle_N116-Zn-N117_pos finished (job 60403331)
[2026-10-28 09:34:27] status: 81 jobs queued/running, 459 branches finished (457 back on Aurora), 0 need review
[2026-10-28 09:45:29] scans/WIGBIX/tilt_Zn-S1-C2-C7_pos finished (job 60361683)
[2026-10-28 09:46:01] scans/WIGBIX/tilt_Zn-N45-C46-C47_neg finished (job 60361680)
[2026-10-28 09:46:33] scans/GUFHEU/tilt_Zn-S2-C33-C41_pos finished (job 60364814)
[2026-10-28 09:46:33] status: 78 jobs queued/running, 462 branches finished (457 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 09:02:23] farm 8972496 (zn_main) ended: =>> PBS: job killed: walltime 21606 exceeded limit 21600
logs tagged as cancelled: 0
scans/WEDVIK/angle_S3-Zn-N6_neg: 10 of 11 steps kept, 1 to run
wrote scans/jobs_restart.txt (381 branches)
main farm jobs already queued or running (8939977 8972593): continuations go to the front of the live queue
queue: 380 continuations added to the front of queue/main (1909 pending now)
NODES=0: queue updated, no farm submitted
prioritize main: 87 of 1908 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 125 of 2285 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
