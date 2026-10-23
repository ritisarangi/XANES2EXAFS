# Zn scan campaign on Aurora: status

Generated 2026-10-23 13:41 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 3087 done, 6347 started (running/stopped/failed), 0 continuations ready, 741 not started, 10175 total
queue main: 421 of 31980 waiting, 6144 ORCA runs active
queue big: 319 of 2127 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 47,175.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8954403 | zn_big | capacity | 16 | 06:00 | R | 03:50 |
| 8956596 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8956793 | zn_main | small | 256 | 06:00 | R | 01:06 |

## Last autopilot actions

```
2026-10-23 12:22:56 farm 8956768.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=prod nodes=256 hours=6 account=ModCon tasks_left=6756
[2026-10-23 12:23:19] autopilot started (pid 3931233, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 42f5c71, accounts: isaac ModCon)
[2026-10-23 12:38:51] new farms go to project ModCon (47175 node-hours left)
[2026-10-23 12:39:01] submitting main farm on ModCon (queue 6756 left, 1 main farms)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8956596): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (6756 pending now)
2026-10-23 12:42:44 farm 8956793.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=prod nodes=256 hours=6 account=ModCon tasks_left=6756
prioritize main: 292 of 6756 pending branches belong to complexes at least half done
prioritize big: 0 of 321 pending branches belong to complexes at least half done
[2026-10-23 13:41:08] publish:   queue    0 problems audit found problems: nothing published 
```
