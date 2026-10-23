# Zn scan campaign on Aurora: status

Generated 2026-10-23 20:44 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 5336 done, 192 started (running/stopped/failed), 4337 continuations ready, 310 not started, 10175 total
queue main: 4337 of 36317 waiting, 0 ORCA runs active
queue big: 310 of 2319 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 45,576.7 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8957252 | zn_big | capacity | 16 | 06:00 | R | 01:58 |
| 8957984 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8958138 | zn_main | small | 256 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-23 20:07:18] STATUS.md pushed
[2026-10-23 20:07:35] autopilot started (pid 1087703, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 15c22b7, accounts: isaac ModCon)
[2026-10-23 20:15:42] new farms go to project ModCon (45576 node-hours left)
[2026-10-23 20:15:52] submitting main farm on ModCon (queue 4337 left, 1 main farms)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8957984): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (4337 pending now)
2026-10-23 20:37:20 farm 8958138.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=prod nodes=256 hours=6 account=ModCon tasks_left=4337
prioritize main: 654 of 4337 pending branches belong to complexes at least half done
prioritize big: 0 of 311 pending branches belong to complexes at least half done
[2026-10-23 20:44:41] publish: publish: 22 complexes added (6372 passing points), 0 not exported; 60 complexes published in total pushed: 85c13f8 Aurora results: 60 complexes published (2026-10-23 20:44) 
```
