# Zn scan campaign on Aurora: status

Generated 2026-10-19 09:57 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 357 done, 192 started (running/stopped/failed), 6631 continuations ready, 2995 not started, 10175 total
queue main: 9230 of 16842 waiting, 0 ORCA runs active
queue big: 396 of 791 waiting, 192 ORCA runs active
failed ORCA runs not retried: 0
allocation: 22,206.8 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8940426 | zn_main | small | 256 | 06:00 | Q | -- |
| 8945717 | zn_big | capacity | 16 | 06:00 | R | 03:04 |

## Last autopilot actions

```
NODES=0: queue updated, no farm submitted
[2026-10-19 06:48:17] submitting big farm on isaac (queue 589 left, 1 big farms)
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (589 pending now)
2026-10-19 06:48:32 farm 8945717.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=isaac tasks_left=589
[2026-10-19 07:41:49] STATUS.md pushed
[2026-10-19 09:41:27] publish: publish: 2 complexes added (590 passing points), 0 not exported; 3 complexes published in total pushed: 8f0cf96 Aurora results: 3 complexes published (2026-10-19 09:41) 
[2026-10-19 09:41:36] autopilot started (pid 317237, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at ce4718c, accounts: isaac ModCon)
[2026-10-19 09:42:33] new farms go to project isaac (22298 node-hours left)
[2026-10-19 09:57:08] publish: publish: no newly finished complexes nothing new to commit 
```
