# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-31 00:52 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8846 done, 0 started (running/stopped/failed), 1329 continuations ready, 0 not started, 10175 total
queue main: 1120 of 45012 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,321.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |
| 8994906 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8995873 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 27 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 601 finished (601 copied back to Aurora), 209 running, 0 queued, 0 need review, 810 total
stops at the 48 h limit so far: 173; failed runs: 91
1447 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 29 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 23 / 30 |
| CAWKIW | 4 / 30 |
| DOZVOF | 30 / 30 |
| FUXMAM | 5 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 10 / 30 |
| JUQXUO | 4 / 30 |
| LAJGIM | 4 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 4 / 30 |
| SONROE | 30 / 30 |
| TIFNUU | 4 / 30 |
| UYORAE | 4 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-31 00:09:03] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-31 00:09:03] status: 211 jobs queued/running, 599 branches finished (599 back on Aurora), 0 need review
[2026-10-31 00:20:16] status: 211 jobs queued/running, 599 branches finished (599 back on Aurora), 0 need review
[2026-10-31 00:31:27] status: 211 jobs queued/running, 599 branches finished (599 back on Aurora), 0 need review
[2026-10-31 00:43:07] scans/CATZUS10/angle_N22-Zn-N58_neg finished (job 60478586)
[2026-10-31 00:43:39] scans/FUXMAM/tilt_Zn-S2-C17-C18_pos finished (job 60553130)
[2026-10-31 00:45:06] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-31 00:45:06] status: 209 jobs queued/running, 601 branches finished (601 back on Aurora), 0 need review
```

## Last autopilot actions

```
queue: 0 continuations added to the front of queue/main (1120 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-30 23:52:22] submitting main capacity farm on ModCon, 6 h (queue 1120 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8987775 8994906): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (1120 pending now)
2026-10-31 00:23:13 farm 8995873.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=1120
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
