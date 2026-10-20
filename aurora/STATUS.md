# Zn scan campaign on Aurora: status

Generated 2026-10-20 11:51 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1237 done, 0 started (running/stopped/failed), 6597 continuations ready, 2341 not started, 10175 total
queue main: 8354 of 23675 waiting, 0 ORCA runs active
queue big: 584 of 1175 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 20,363.7 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947389 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8947400 | zn_big | capacity | 16 | 06:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |

## Last autopilot actions

```
logs tagged as cancelled: 0
scans/ZUKRII/twist_N21-S24-N58-S61_pos: 3 of 11 steps kept, 8 to run (interrupted step resumed from its last geometry)
wrote scans/jobs_restart.txt (6060 branches)
main farm jobs already queued or running (8939977 8947389): continuations go to the front of the live queue
queue: 6048 continuations added to the front of queue/main (8354 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-20 10:25:58] submitting main farm on isaac (queue 8354 left, 1 main farms)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8947389): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (8354 pending now)
2026-10-20 10:26:47 farm 8947436.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=prod nodes=256 hours=6 account=isaac tasks_left=8354
```
