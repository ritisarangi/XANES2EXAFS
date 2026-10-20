# Zn scan campaign on Aurora: status

Generated 2026-10-20 08:51 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1055 done, 6717 started (running/stopped/failed), 0 continuations ready, 2403 not started, 10175 total
queue main: 2011 of 17229 waiting, 6521 ORCA runs active
queue big: 392 of 983 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 22,090.0 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8940426 | zn_main | small | 256 | 06:00 | R | 04:56 |
| 8946258 | zn_main | capacity | 16 | 06:00 | R | 05:26 |
| 8946295 | zn_big | capacity | 16 | 06:00 | R | 05:10 |

## Last autopilot actions

```
[2026-10-20 00:09:49] publish: publish: no newly finished complexes nothing new to commit 
[2026-10-20 00:10:04] STATUS.md pushed
[2026-10-20 02:16:32] STATUS.md pushed
[2026-10-20 04:25:48] STATUS.md pushed
[2026-10-20 05:32:06] autopilot started (pid 493530, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at d2bc482, accounts: isaac ModCon)
[2026-10-20 05:32:21] new farms go to project isaac (22090 node-hours left)
[2026-10-20 05:52:26] publish: publish: no newly finished complexes nothing new to commit 
[2026-10-20 05:54:19] STATUS.md pushed
[2026-10-20 07:46:25] STATUS.md pushed
[2026-10-20 08:29:15] autopilot started (pid 1672127, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at b90db72, accounts: isaac ModCon)
[2026-10-20 08:29:33] new farms go to project isaac (22090 node-hours left)
[2026-10-20 08:51:49] publish: publish: 2 complexes added (551 passing points), 0 not exported; 7 complexes published in total pushed: db65066 Aurora results: 7 complexes published (2026-10-20 08:51) 
```
