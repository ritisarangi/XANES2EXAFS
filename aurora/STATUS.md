# Zn scan campaign on Aurora: status

Generated 2026-10-19 05:32 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 294 done, 576 started (running/stopped/failed), 6306 continuations ready, 2999 not started, 10175 total
queue main: 8905 of 16461 waiting, 384 ORCA runs active
queue big: 400 of 600 waiting, 192 ORCA runs active
failed ORCA runs not retried: 0
allocation: 22,489.6 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8940421 | zn_big | capacity | 16 | 12:00 | R | 10:50 |
| 8940426 | zn_main | small | 256 | 06:00 | Q | -- |
| 8944435 | zn_main | capacity | 16 | 06:00 | R | 01:32 |

## Last autopilot actions

```
[2026-10-19 01:45:30] STATUS.md pushed
[2026-10-19 03:04:59] farm 8940420 (zn_main) ended: farm 8940420 done 2026-10-19 02:56:35; queue next 7146 of 16084
logs tagged as cancelled: 0
scans/ZEFGAS/twist_S1-N3-S2-N4_neg: 10 of 11 steps kept, 1 to run (interrupted step resumed from its last geometry)
wrote scans/jobs_restart.txt (379 branches)
main farm jobs already queued or running (8939977 8940426): continuations go to the front of the live queue
queue: 377 continuations added to the front of queue/main (9315 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-19 03:21:09] autopilot started (pid 1561311, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 0a50767, accounts: isaac ModCon)
[2026-10-19 03:22:32] new farms go to project isaac (23642 node-hours left)
[2026-10-19 03:34:17] publish: publish: no newly finished complexes nothing new to commit 
[2026-10-19 03:34:31] STATUS.md pushed
```
