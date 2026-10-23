# Zn scan campaign on Aurora: status

Generated 2026-10-23 16:44 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 4611 done, 5061 started (running/stopped/failed), 192 continuations ready, 311 not started, 10175 total
queue main: 0 of 31980 waiting, 5022 ORCA runs active
queue big: 503 of 2319 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 47,080.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8956596 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8956793 | zn_main | small | 256 | 06:00 | R | 04:14 |
| 8957252 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-23 15:30:21] STATUS.md pushed
[2026-10-23 15:30:41] autopilot started (pid 2827919, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 01a2158, accounts: isaac ModCon)
[2026-10-23 15:54:42] new farms go to project ModCon (47174 node-hours left)
[2026-10-23 15:54:47] submitting big farm on ModCon (queue 503 left, 1 big farms)
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (503 pending now)
2026-10-23 16:18:51 farm 8957252.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=503
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
[2026-10-23 16:44:39] publish: publish: 16 complexes added (4632 passing points), 1 not exported; 38 complexes published in total pushed: 55f67d7 Aurora results: 38 complexes published (2026-10-23 16:44) 
```
