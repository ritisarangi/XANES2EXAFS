# Zn scan campaign on Aurora: status

Generated 2026-10-19 01:45 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 234 done, 576 started (running/stopped/failed), 6358 continuations ready, 3007 not started, 10175 total
queue main: 8957 of 16084 waiting, 384 ORCA runs active
queue big: 408 of 600 waiting, 192 ORCA runs active
failed ORCA runs not retried: 0
allocation: 23,832.2 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8940420 | zn_main | capacity | 16 | 12:00 | R | 10:38 |
| 8940421 | zn_big | capacity | 16 | 12:00 | R | 07:02 |
| 8940426 | zn_main | small | 256 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-19 00:00:50] STATUS.md pushed
[2026-10-19 00:10:02] autopilot started (pid 3427404, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at c7f03b9, accounts: isaac ModCon)
[2026-10-19 00:10:42] new farms go to project isaac (23832 node-hours left)
[2026-10-19 00:12:48] publish: publish: no newly finished complexes nothing new to commit 
[2026-10-19 00:13:11] STATUS.md pushed
[2026-10-19 01:36:31] autopilot started (pid 393477, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 06ea93b, accounts: isaac ModCon)
[2026-10-19 01:37:38] new farms go to project isaac (23832 node-hours left)
[2026-10-19 01:39:37] publish: publish: no newly finished complexes nothing new to commit 
[2026-10-19 01:40:01] STATUS.md pushed
[2026-10-19 01:41:51] autopilot started (pid 466599, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 16bdcda, accounts: isaac ModCon)
[2026-10-19 01:42:50] new farms go to project isaac (23832 node-hours left)
[2026-10-19 01:45:10] publish: publish: no newly finished complexes nothing new to commit 
```
