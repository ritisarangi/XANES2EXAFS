# Zn scan campaign on Aurora: status

Generated 2026-10-23 19:52 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 5335 done, 192 started (running/stopped/failed), 4337 continuations ready, 311 not started, 10175 total
queue main: 4337 of 36317 waiting, 0 ORCA runs active
queue big: 311 of 2319 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 45,576.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8957252 | zn_big | capacity | 16 | 06:00 | R | 01:16 |
| 8957984 | zn_main | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
wrote scans/jobs_restart.txt (192 branches)
main farm jobs already queued or running (8939977 8956793): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (4337 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-23 19:17:32] submitting main capacity farm on ModCon, 6 h (queue 4337 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (4337 pending now)
2026-10-23 19:48:15 farm 8957984.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=4337
prioritize main: 654 of 4337 pending branches belong to complexes at least half done
prioritize big: 0 of 311 pending branches belong to complexes at least half done
```
