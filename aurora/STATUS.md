# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-27 06:05 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7575 done, 0 started (running/stopped/failed), 2532 continuations ready, 68 not started, 10175 total
queue main: 2403 of 40383 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,632.5 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8970790 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 362 finished (362 copied back to Aurora), 160 running, 18 queued, 0 need review, 540 total
stops at the 48 h limit so far: 44; failed runs: 78
1086 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 27 / 30 |
| GUCSED | 26 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 24 / 30 |
| ICAVAK | 29 / 30 |
| NAMSOJ | 28 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 6 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 24 / 30 |
| RAYBIC | 18 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 18 / 30 |
| WIGBIX | 4 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-27 05:53:32] scans/CATZUS10/twist_N4-N22-N40-N58_pos stopped at the time limit (job 60244238); continues
[2026-10-27 05:54:08] scans/CATZUS10/bond_Zn-N58_neg finished (job 60244236)
[2026-10-27 05:54:40] scans/DOZVOF/angle_N3-Zn-N5_pos finished (job 60244238)
[2026-10-27 05:55:12] scans/CATZUS10/tilt_Zn-N22-C28-H87_neg stopped at the time limit (job 60244236); continues
[2026-10-27 05:55:44] scans/NONLEI/angle_N1-Zn-N2_pos finished (job 60240322)
[2026-10-27 05:57:10] submitted 18 jobs
[2026-10-27 06:08:11] copied 19 finished branches back to Aurora: SUCCEEDED
[2026-10-27 06:08:11] status: 178 jobs queued/running, 362 branches finished (362 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 0 of 2025 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-27 05:09:20] publish:     scans/UDODOG/bond_Zn-N5_pos: scanr_8947436_x4107c0s1b0n0_12_3.log and scanr_8947436_x4702c0s2b0n0_20_2.log ran at the same time   queue    0 problems 
[2026-10-27 05:19:30] farm 8965440 (zn_main) ended: =>> PBS: job killed: walltime 21606 exceeded limit 21600
logs tagged as cancelled: 0
scans/WEDVIK/angle_S3-Zn-N6_neg: 10 of 11 steps kept, 1 to run
wrote scans/jobs_restart.txt (380 branches)
main farm jobs already queued or running (8939977 8970790): continuations go to the front of the live queue
queue: 378 continuations added to the front of queue/main (2403 pending now)
NODES=0: queue updated, no farm submitted
prioritize main: 60 of 2403 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
