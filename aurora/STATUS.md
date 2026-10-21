# Zn scan campaign on Aurora: status

Generated 2026-10-21 00:54 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1280 done, 384 started (running/stopped/failed), 6182 continuations ready, 2329 not started, 10175 total
queue main: 7939 of 24054 waiting, 384 ORCA runs active
queue big: 572 of 1367 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 20,176.2 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8948275 | zn_main | capacity | 16 | 06:00 | R | 00:18 |
| 8948280 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
prioritize main: 85 of 8327 pending branches belong to complexes at least half done
prioritize big: 14 of 572 pending branches belong to complexes at least half done
prioritize main: 85 of 8327 pending branches belong to complexes at least half done
prioritize big: 14 of 572 pending branches belong to complexes at least half done
prioritize main: 85 of 8327 pending branches belong to complexes at least half done
prioritize big: 14 of 572 pending branches belong to complexes at least half done
[2026-10-21 00:20:15] STATUS.md pushed
[2026-10-21 00:26:30] autopilot started (pid 2106399, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 91029f4, accounts: isaac ModCon)
[2026-10-21 00:27:20] new farms go to project isaac (20176 node-hours left)
prioritize main: 85 of 8327 pending branches belong to complexes at least half done
prioritize big: 14 of 572 pending branches belong to complexes at least half done
[2026-10-21 00:54:09] publish: publish: no newly finished complexes nothing new to commit 
```
