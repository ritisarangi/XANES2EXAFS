# Zn scan campaign on Aurora: status

Generated 2026-10-21 19:22 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1487 done, 0 started (running/stopped/failed), 6378 continuations ready, 2310 not started, 10175 total
queue main: 8139 of 25193 waiting, 0 ORCA runs active
queue big: 549 of 1745 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 49,105.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8950108 | zn_big | capacity | 16 | 06:00 | Q | -- |
| 8950977 | zn_main | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
main farm jobs already queued or running (8939977 8947436): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (8139 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-21 18:44:10] submitting main capacity farm on ModCon, 6 h (queue 8139 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8947436): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (8139 pending now)
2026-10-21 18:44:48 farm 8950977.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=8139
[2026-10-21 19:11:33] publish: publish: 1 complexes added (204 passing points), 0 not exported; 20 complexes published in total pushed: b7ef162 Aurora results: 20 complexes published (2026-10-21 19:11) 
prioritize main: 31 of 8139 pending branches belong to complexes at least half done
prioritize big: 2 of 549 pending branches belong to complexes at least half done
```
