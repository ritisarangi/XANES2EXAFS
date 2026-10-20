# Zn scan campaign on Aurora: status

Generated 2026-10-20 10:04 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1225 done, 6060 started (running/stopped/failed), 549 continuations ready, 2341 not started, 10175 total
queue main: 2306 of 17627 waiting, 0 ORCA runs active
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

## Last autopilot actions

```
main farm jobs already queued or running (8939977 8940426): continuations go to the front of the live queue
queue: 25 continuations added to the front of queue/main (2306 pending now)
2026-10-20 09:28:52 farm 8947389.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=isaac tasks_left=2306
[2026-10-20 09:39:04] submitting big farm on isaac (queue 584 left, 1 big farms)
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (584 pending now)
2026-10-20 09:39:33 farm 8947400.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=isaac tasks_left=584
[2026-10-20 09:41:53] autopilot started (pid 1996789, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 2f23758, accounts: isaac ModCon)
[2026-10-20 09:42:18] new farms go to project isaac (21905 node-hours left)
[2026-10-20 10:04:20] publish: publish: no newly finished complexes nothing new to commit 
```
