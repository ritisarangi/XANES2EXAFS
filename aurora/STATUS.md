# Zn scan campaign on Aurora: status

Generated 2026-10-24 02:26 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 5336 done, 4336 started (running/stopped/failed), 199 continuations ready, 304 not started, 10175 total
queue main: 0 of 36317 waiting, 4334 ORCA runs active
queue big: 503 of 503 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 45,482.8 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8957984 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8958138 | zn_main | small | 256 | 06:00 | R | 00:04 |
| 8959031 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-23 22:38:57] STATUS.md pushed
[2026-10-24 02:12:01] autopilot started (pid 1626349, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 6eacada, accounts: isaac ModCon)
[2026-10-24 02:19:04] new farms go to project ModCon (45482 node-hours left)
[2026-10-24 02:19:37] submitting big farm on ModCon (queue 503 left, 1 big farms)
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (503 pending now)
2026-10-24 02:21:57 farm 8959031.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=503
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
[2026-10-24 02:26:42] publish: publish: no newly finished complexes 
```
