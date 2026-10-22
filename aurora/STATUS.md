# Zn scan campaign on Aurora: status

Generated 2026-10-22 22:56 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1582 done, 0 started (running/stopped/failed), 6321 continuations ready, 2272 not started, 10175 total
queue main: 8078 of 25571 waiting, 0 ORCA runs active
queue big: 515 of 2127 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 48,810.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8953480 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8954403 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-22 19:50:33] publish: publish: no newly finished complexes nothing new to commit 
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 15 of 515 pending branches belong to complexes at least half done
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 15 of 515 pending branches belong to complexes at least half done
[2026-10-22 21:05:38] STATUS.md pushed
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 15 of 515 pending branches belong to complexes at least half done
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 15 of 515 pending branches belong to complexes at least half done
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 15 of 515 pending branches belong to complexes at least half done
```
