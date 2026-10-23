# Zn scan campaign on Aurora: status

Generated 2026-10-23 08:09 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 2124 done, 6522 started (running/stopped/failed), 192 continuations ready, 1337 not started, 10175 total
queue main: 1000 of 25571 waiting, 6528 ORCA runs active
queue big: 515 of 2127 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 48,810.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | R | 03:08 |
| 8953480 | zn_main | capacity | 16 | 06:00 | R | 04:32 |
| 8954403 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
prioritize main: 0 of 7690 pending branches belong to complexes at least half done
prioritize big: 15 of 515 pending branches belong to complexes at least half done
[2026-10-23 05:13:56] STATUS.md pushed
prioritize main: 0 of 1528 pending branches belong to complexes at least half done
prioritize big: 15 of 515 pending branches belong to complexes at least half done
prioritize main: 0 of 1460 pending branches belong to complexes at least half done
prioritize big: 15 of 515 pending branches belong to complexes at least half done
prioritize main: 0 of 1373 pending branches belong to complexes at least half done
prioritize big: 15 of 515 pending branches belong to complexes at least half done
prioritize main: 0 of 1223 pending branches belong to complexes at least half done
prioritize big: 15 of 515 pending branches belong to complexes at least half done
[2026-10-23 08:09:51] publish: publish: no newly finished complexes nothing new to commit 
```
