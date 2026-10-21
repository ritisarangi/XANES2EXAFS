# Zn scan campaign on Aurora: status

Generated 2026-10-21 04:35 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1351 done, 576 started (running/stopped/failed), 5921 continuations ready, 2327 not started, 10175 total
queue main: 7870 of 24054 waiting, 384 ORCA runs active
queue big: 378 of 1367 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 20,176.2 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8948275 | zn_main | capacity | 16 | 06:00 | R | 03:56 |
| 8948280 | zn_big | capacity | 16 | 06:00 | R | 03:12 |

## Last autopilot actions

```
prioritize big: 14 of 572 pending branches belong to complexes at least half done
prioritize main: 0 of 7915 pending branches belong to complexes at least half done
prioritize big: 0 of 380 pending branches belong to complexes at least half done
prioritize main: 0 of 7903 pending branches belong to complexes at least half done
prioritize big: 0 of 380 pending branches belong to complexes at least half done
[2026-10-21 02:30:35] STATUS.md pushed
prioritize main: 0 of 7893 pending branches belong to complexes at least half done
prioritize big: 0 of 380 pending branches belong to complexes at least half done
prioritize main: 0 of 7884 pending branches belong to complexes at least half done
prioritize big: 0 of 380 pending branches belong to complexes at least half done
prioritize main: 0 of 7877 pending branches belong to complexes at least half done
prioritize big: 0 of 379 pending branches belong to complexes at least half done
```
