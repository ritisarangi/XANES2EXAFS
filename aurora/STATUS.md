# Zn scan campaign on Aurora: status

Generated 2026-10-19 00:12 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 208 done, 576 started (running/stopped/failed), 6384 continuations ready, 3007 not started, 10175 total
queue main: 8983 of 16084 waiting, 384 ORCA runs active
queue big: 408 of 600 waiting, 192 ORCA runs active
failed ORCA runs not retried: 0
allocation: 23,832.2 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8940420 | zn_main | capacity | 16 | 12:00 | R | 09:06 |
| 8940421 | zn_big | capacity | 16 | 12:00 | R | 05:30 |
| 8940426 | zn_main | small | 256 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-18 17:17:47] publish: publish: no newly finished complexes nothing new to commit 
[2026-10-18 17:22:05] STATUS.md pushed
[2026-10-18 17:31:39] autopilot started (pid 472182, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 8b2763b)
[2026-10-18 17:53:01] publish: publish: no newly finished complexes nothing new to commit 
[2026-10-18 17:56:18] STATUS.md pushed
[2026-10-18 19:36:54] STATUS.md pushed
[2026-10-18 21:38:09] STATUS.md pushed
[2026-10-18 23:49:30] publish: publish: no newly finished complexes nothing new to commit 
[2026-10-19 00:00:50] STATUS.md pushed
[2026-10-19 00:10:02] autopilot started (pid 3427404, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at c7f03b9, accounts: isaac ModCon)
[2026-10-19 00:10:42] new farms go to project isaac (23832 node-hours left)
[2026-10-19 00:12:48] publish: publish: no newly finished complexes nothing new to commit 
```
