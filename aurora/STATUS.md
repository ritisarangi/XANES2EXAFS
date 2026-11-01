# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-11-01 08:04 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 10002 done, 144 started (running/stopped/failed), 29 continuations ready, 0 not started, 10175 total
queue main: 0 of 45434 waiting, 144 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 41,514.2 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8995873 | zn_main | capacity | 16 | 06:00 | R | 04:00 |
| 9013664 | zn_main | small | 256 | 04:00 | Q | -- |
| 9013865 | zn_main | small | 256 | 06:00 | Q | -- |
| 9019151 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 932 finished (932 copied back to Aurora), 28 running, 0 queued, 0 need review, 960 total
stops at the 48 h limit so far: 201; failed runs: 93
1454 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 28 / 30 |
| CAWKIW | 30 / 30 |
| DOZVOF | 30 / 30 |
| FAXYIP | 28 / 30 |
| FUXMAM | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 30 / 30 |
| JUQXUO | 30 / 30 |
| LAJGIM | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 28 / 30 |
| SONROE | 30 / 30 |
| TELRUZ | 29 / 30 |
| TEYSOG | 28 / 30 |
| TIFNUU | 30 / 30 |
| UWAVOF | 30 / 30 |
| UYORAE | 11 / 30 |
| WEQZAT01 | 30 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-11-01 07:29:46] status: 29 jobs queued/running, 931 branches finished (931 back on Aurora), 0 need review
[2026-11-01 07:39:59] status: 29 jobs queued/running, 931 branches finished (931 back on Aurora), 0 need review
[2026-11-01 07:50:14] status: 29 jobs queued/running, 931 branches finished (931 back on Aurora), 0 need review
[2026-11-01 08:00:32] status: 29 jobs queued/running, 931 branches finished (931 back on Aurora), 0 need review
[2026-11-01 08:11:19] scans/UWAVOF/angle_S3-Zn-N7_pos finished (job 60613457)
[2026-11-01 08:11:19] status: 28 jobs queued/running, 932 branches finished (931 back on Aurora), 0 need review
[2026-11-01 08:22:51] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-11-01 08:22:51] status: 28 jobs queued/running, 932 branches finished (932 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-11-01 05:48:01] submitting main capacity farm on ModCon, 6 h (queue 0 left, 176 with running)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8995873 9013664 9013865): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (0 pending now)
2026-11-01 06:26:17 farm 9019151.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=0
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-11-01 06:55:55] publish: publish: 22 complexes added (6150 passing points), 0 not exported; 285 complexes published in total pushed: 22aacfb Aurora results: 285 complexes published (2026-11-01 06:55) 
[2026-11-01 07:13:23] STATUS.md pushed
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
