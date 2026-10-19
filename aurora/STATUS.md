# Zn scan campaign on Aurora: status

Generated 2026-10-19 23:57 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 368 done, 0 started (running/stopped/failed), 6816 continuations ready, 2991 not started, 10175 total
queue main: 9223 of 17222 waiting, 0 ORCA runs active
queue big: 584 of 983 waiting, 0 ORCA runs active
failed ORCA runs not retried: 0
allocation: 22,090.0 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8940426 | zn_main | small | 256 | 06:00 | Q | -- |
| 8946258 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8946295 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (584 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-19 12:41:36] submitting big farm on isaac (queue 584 left, 1 big farms)
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (584 pending now)
2026-10-19 12:41:45 farm 8946295.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=isaac tasks_left=584
[2026-10-19 23:34:42] autopilot started (pid 187296, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 5777542, accounts: isaac ModCon)
[2026-10-19 23:38:52] new farms go to project isaac (22090 node-hours left)
[2026-10-19 23:57:47] publish: publish: no newly finished complexes nothing new to commit 
```
