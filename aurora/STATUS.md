# Zn scan campaign on Aurora: status

Generated 2026-10-20 15:51 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1250 done, 576 started (running/stopped/failed), 6012 continuations ready, 2337 not started, 10175 total
queue main: 7961 of 23675 waiting, 384 ORCA runs active
queue big: 388 of 1175 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 20,363.7 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947389 | zn_main | capacity | 16 | 06:00 | R | 03:40 |
| 8947400 | zn_big | capacity | 16 | 06:00 | R | 03:40 |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-20 13:45:13] autopilot started (pid 2772834, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 8be0a42, accounts: isaac ModCon)
[2026-10-20 13:45:26] new farms go to project isaac (20363 node-hours left)
prioritize main: 94 of 7967 pending branches belong to complexes at least half done
prioritize big: 0 of 392 pending branches belong to complexes at least half done
[2026-10-20 14:02:35] publish: publish: no newly finished complexes nothing new to commit 
[2026-10-20 14:02:56] STATUS.md pushed
prioritize main: 93 of 7966 pending branches belong to complexes at least half done
prioritize big: 0 of 391 pending branches belong to complexes at least half done
prioritize main: 92 of 7965 pending branches belong to complexes at least half done
prioritize big: 0 of 390 pending branches belong to complexes at least half done
prioritize main: 90 of 7963 pending branches belong to complexes at least half done
prioritize big: 0 of 390 pending branches belong to complexes at least half done
```
