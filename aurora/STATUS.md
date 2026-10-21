# Zn scan campaign on Aurora: status

Generated 2026-10-21 07:06 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1388 done, 574 started (running/stopped/failed), 5891 continuations ready, 2322 not started, 10175 total
queue main: 7840 of 24433 waiting, 384 ORCA runs active
queue big: 373 of 1367 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 20,084.1 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8948280 | zn_big | capacity | 16 | 06:00 | R | 05:42 |
| 8949575 | zn_main | capacity | 16 | 06:00 | R | 00:28 |

## Last autopilot actions

```
main farm jobs already queued or running (8939977 8947436): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (8225 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-21 06:27:22] submitting main capacity farm on isaac, 6 h (queue 8225 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8947436): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (8225 pending now)
2026-10-21 06:28:00 farm 8949575.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=isaac tasks_left=8225
prioritize main: 11 of 8225 pending branches belong to complexes at least half done
prioritize big: 0 of 374 pending branches belong to complexes at least half done
[2026-10-21 07:06:14] publish: publish: 4 complexes added (1189 passing points), 0 not exported; 14 complexes published in total pushed: 4c117fa Aurora results: 14 complexes published (2026-10-21 07:06) 
```
