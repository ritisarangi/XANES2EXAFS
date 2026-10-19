# Zn scan campaign on Aurora: status

Generated 2026-10-19 07:40 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 335 done, 575 started (running/stopped/failed), 6269 continuations ready, 2996 not started, 10175 total
queue main: 8867 of 16461 waiting, 384 ORCA runs active
queue big: 397 of 791 waiting, 192 ORCA runs active
failed ORCA runs not retried: 0
allocation: 22,298.8 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8940426 | zn_main | small | 256 | 06:00 | Q | -- |
| 8944435 | zn_main | capacity | 16 | 06:00 | R | 03:40 |
| 8945717 | zn_big | capacity | 16 | 06:00 | R | 00:48 |

## Last autopilot actions

```
[2026-10-19 06:45:05] farm 8940421 (zn_big) ended: farm 8940421 done 2026-10-19 06:36:05; queue next 202 of 791
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (589 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-19 06:48:17] submitting big farm on isaac (queue 589 left, 1 big farms)
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (589 pending now)
2026-10-19 06:48:32 farm 8945717.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=isaac tasks_left=589
```
