# Zn scan campaign on Aurora: status

Generated 2026-10-21 15:20 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1463 done, 384 started (running/stopped/failed), 6018 continuations ready, 2310 not started, 10175 total
queue main: 7777 of 24814 waiting, 384 ORCA runs active
queue big: 549 of 1745 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 19,422.7 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8950006 | zn_main | capacity | 16 | 06:00 | R | 02:36 |
| 8950108 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-21 13:54:49] submitting big farm on isaac (queue 549 left, 1 big farms)
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (549 pending now)
2026-10-21 13:55:24 farm 8950108.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=isaac tasks_left=549
prioritize main: 0 of 7788 pending branches belong to complexes at least half done
prioritize big: 2 of 549 pending branches belong to complexes at least half done
prioritize main: 0 of 7787 pending branches belong to complexes at least half done
prioritize big: 2 of 549 pending branches belong to complexes at least half done
prioritize main: 0 of 7784 pending branches belong to complexes at least half done
prioritize big: 2 of 549 pending branches belong to complexes at least half done
```
