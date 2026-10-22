# Zn scan campaign on Aurora: status

Generated 2026-10-22 14:31 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1564 done, 192 started (running/stopped/failed), 6129 continuations ready, 2290 not started, 10175 total
queue main: 8078 of 25571 waiting, 0 ORCA runs active
queue big: 341 of 1935 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 48,904.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8952802 | zn_big | capacity | 16 | 06:00 | R | 01:28 |
| 8953480 | zn_main | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
no stopped branches found
main farm jobs already queued or running (8939977 8947436): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (8078 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-22 14:18:40] submitting main capacity farm on ModCon, 6 h (queue 8078 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8947436): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (8078 pending now)
2026-10-22 14:19:38 farm 8953480.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=8078
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 0 of 342 pending branches belong to complexes at least half done
```
