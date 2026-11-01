# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-11-01 06:55 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 9986 done, 157 started (running/stopped/failed), 32 continuations ready, 0 not started, 10175 total
queue main: 0 of 45434 waiting, 155 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 41,514.2 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8995873 | zn_main | capacity | 16 | 06:00 | R | 02:50 |
| 9013664 | zn_main | small | 256 | 04:00 | Q | -- |
| 9013865 | zn_main | small | 256 | 06:00 | Q | -- |
| 9019151 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 930 finished (928 copied back to Aurora), 30 running, 0 queued, 0 need review, 960 total
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
| UWAVOF | 28 / 30 |
| UYORAE | 11 / 30 |
| WEQZAT01 | 30 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-11-01 06:32:23] scans/UWAVOF/angle_S1-Zn-N5_neg finished (job 60613427)
[2026-11-01 06:32:23] status: 32 jobs queued/running, 928 branches finished (924 back on Aurora), 0 need review
[2026-11-01 06:45:12] copied 4 finished branches back to Aurora: SUCCEEDED
[2026-11-01 06:45:12] status: 32 jobs queued/running, 928 branches finished (928 back on Aurora), 0 need review
[2026-11-01 06:55:59] scans/UWAVOF/angle_S3-Zn-N7_neg finished (job 60613448)
[2026-11-01 06:55:59] status: 31 jobs queued/running, 929 branches finished (928 back on Aurora), 0 need review
[2026-11-01 07:06:45] scans/UYORAE/tilt_Zn-N7-C31-C29_neg finished (job 60630747)
[2026-11-01 07:06:45] status: 30 jobs queued/running, 930 branches finished (928 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-11-01 05:06:02] autopilot started (pid 3555294, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at d208e7e, accounts: isaac ModCon)
[2026-11-01 05:31:02] autopilot started (pid 4046772, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 312a7ce, accounts: isaac ModCon)
[2026-11-01 05:47:41] new farms go to project ModCon (41514 node-hours left)
[2026-11-01 05:48:01] submitting main capacity farm on ModCon, 6 h (queue 0 left, 176 with running)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8995873 9013664 9013865): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (0 pending now)
2026-11-01 06:26:17 farm 9019151.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=0
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-11-01 06:55:55] publish: publish: 22 complexes added (6150 passing points), 0 not exported; 285 complexes published in total pushed: 22aacfb Aurora results: 285 complexes published (2026-11-01 06:55) 
```
