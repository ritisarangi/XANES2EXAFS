# Zn scan campaign on Aurora: status

Generated 2026-10-18 17:17 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 95 done, 2723 started (running/stopped/failed), 4182 continuations ready, 3175 not started, 10175 total
queue main: 5009 of 12001 waiting, 384 ORCA runs active
queue big: 600 of 600 waiting, 0 ORCA runs active
failed ORCA runs not retried: 0
allocation: 23,832.2 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8940420 | zn_main | capacity | 16 | 12:00 | R | 02:16 |
| 8940421 | zn_big | capacity | 16 | 12:00 | Q | -- |
| 8940426 | zn_main | small | 256 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-18 15:40:23] autopilot started (pid 3452899, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at f79adec)
[2026-10-18 15:44:47] no new farms: balance 0 node-hours below 1500
[2026-10-18 15:44:47] publish: DRY go.sh publish 
[2026-10-18 15:52:04] autopilot started (pid 3576422, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at ce150ee)
[2026-10-18 16:02:39] autopilot started (pid 3615890, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 68920cf)
[2026-10-18 16:28:22] publish: fatal: not a git repository (or any parent up to mount point /lus) Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set). 
[2026-10-18 16:31:42] STATUS.md pushed
[2026-10-18 16:41:40] autopilot started (pid 128224, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 51b76a8)
[2026-10-18 17:17:47] publish: publish: no newly finished complexes nothing new to commit 
```
