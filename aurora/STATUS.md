# Zn scan campaign on Aurora: status

Generated 2026-10-20 14:02 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1240 done, 576 started (running/stopped/failed), 6018 continuations ready, 2341 not started, 10175 total
queue main: 7967 of 23675 waiting, 384 ORCA runs active
queue big: 392 of 1175 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 20,363.7 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947389 | zn_main | capacity | 16 | 06:00 | R | 01:52 |
| 8947400 | zn_big | capacity | 16 | 06:00 | R | 01:52 |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-20 10:25:58] submitting main farm on isaac (queue 8354 left, 1 main farms)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8947389): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (8354 pending now)
2026-10-20 10:26:47 farm 8947436.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=prod nodes=256 hours=6 account=isaac tasks_left=8354
[2026-10-20 11:52:48] STATUS.md pushed
[2026-10-20 13:45:13] autopilot started (pid 2772834, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 8be0a42, accounts: isaac ModCon)
[2026-10-20 13:45:26] new farms go to project isaac (20363 node-hours left)
prioritize main: 94 of 7967 pending branches belong to complexes at least half done
prioritize big: 0 of 392 pending branches belong to complexes at least half done
[2026-10-20 14:02:35] publish: publish: no newly finished complexes nothing new to commit 
```
