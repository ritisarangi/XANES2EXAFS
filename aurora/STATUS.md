# Zn scan campaign on Aurora: status

Generated 2026-10-21 08:46 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1398 done, 576 started (running/stopped/failed), 5882 continuations ready, 2319 not started, 10175 total
queue main: 7831 of 24433 waiting, 384 ORCA runs active
queue big: 370 of 1557 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 19,990.8 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8949575 | zn_main | capacity | 16 | 06:00 | R | 02:08 |
| 8949671 | zn_big | capacity | 16 | 06:00 | R | 00:44 |

## Last autopilot actions

```
[2026-10-21 07:17:47] submitting big farm on isaac (queue 563 left, 1 big farms)
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (563 pending now)
2026-10-21 07:18:22 farm 8949671.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=isaac tasks_left=563
prioritize main: 0 of 7839 pending branches belong to complexes at least half done
prioritize big: 7 of 563 pending branches belong to complexes at least half done
prioritize main: 0 of 7835 pending branches belong to complexes at least half done
prioritize big: 7 of 563 pending branches belong to complexes at least half done
prioritize main: 0 of 7832 pending branches belong to complexes at least half done
prioritize big: 0 of 371 pending branches belong to complexes at least half done
```
