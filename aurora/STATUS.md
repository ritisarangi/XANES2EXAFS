# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-31 23:05 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 9684 done, 367 started (running/stopped/failed), 124 continuations ready, 0 not started, 10175 total
queue main: 0 of 45254 waiting, 367 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 41,610.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8994906 | zn_main | capacity | 16 | 06:00 | R | 00:50 |
| 8995873 | zn_main | capacity | 16 | 06:00 | H | -- |
| 9013664 | zn_main | small | 256 | 04:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 836 finished (836 copied back to Aurora), 107 running, 17 queued, 0 need review, 960 total
stops at the 48 h limit so far: 198; failed runs: 93
1453 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 27 / 30 |
| CAWKIW | 30 / 30 |
| DOZVOF | 30 / 30 |
| FAXYIP | 14 / 30 |
| FUXMAM | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 30 / 30 |
| JUQXUO | 29 / 30 |
| LAJGIM | 27 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 21 / 30 |
| SONROE | 30 / 30 |
| TELRUZ | 18 / 30 |
| TEYSOG | 14 / 30 |
| TIFNUU | 28 / 30 |
| UWAVOF | 5 / 30 |
| UYORAE | 7 / 30 |
| WEQZAT01 | 16 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-31 22:53:26] scans/UYORAE/tilt_Zn-N7-C31-C29_pos stopped at the time limit (job 60502692); continues
[2026-10-31 22:53:58] scans/UYORAE/tilt_Zn-N12-C69-C67_pos stopped at the time limit (job 60502690); continues
[2026-10-31 22:54:30] scans/WEQZAT01/bond_Zn-S1_pos finished (job 60613541)
[2026-10-31 22:55:03] scans/WEQZAT01/bond_Zn-N3_pos finished (job 60613532)
[2026-10-31 22:55:35] scans/WEQZAT01/angle_S1-Zn-N3_neg finished (job 60613510)
[2026-10-31 22:56:43] submitted 14 jobs
[2026-10-31 23:02:30] copied 10 finished branches back to Aurora: SUCCEEDED
[2026-10-31 23:02:30] status: 124 jobs queued/running, 836 branches finished (836 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-31 22:33:05] publish: publish: 14 complexes added (3720 passing points), 0 not exported; 263 complexes published in total pushed: fded5ca Aurora results: 263 complexes published (2026-10-31 22:33) 
[2026-10-31 22:39:13] autopilot started (pid 3356561, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at b0cf721, accounts: isaac ModCon)
[2026-10-31 22:51:55] new farms go to project ModCon (41610 node-hours left)
[2026-10-31 22:53:48] submitting main farm on ModCon, 4 h (queue 0 left, 1 main farms)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8994906 8995873): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (0 pending now)
2026-10-31 23:03:19 farm 9013664.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=prod nodes=256 hours=4 account=ModCon tasks_left=0
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 23:05:09] publish: publish: no newly finished complexes 
```
