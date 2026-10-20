# Zn scan campaign on Aurora: status

Generated 2026-10-20 17:52 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1276 done, 571 started (running/stopped/failed), 5999 continuations ready, 2329 not started, 10175 total
queue main: 7948 of 23675 waiting, 0 ORCA runs active
queue big: 380 of 1175 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 20,363.7 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947389 | zn_main | capacity | 16 | 06:00 | R | 05:42 |
| 8947400 | zn_big | capacity | 16 | 06:00 | R | 05:42 |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |

## Last autopilot actions

```
prioritize big: 0 of 390 pending branches belong to complexes at least half done
prioritize main: 90 of 7963 pending branches belong to complexes at least half done
prioritize big: 0 of 390 pending branches belong to complexes at least half done
[2026-10-20 15:51:44] STATUS.md pushed
prioritize main: 86 of 7959 pending branches belong to complexes at least half done
prioritize big: 0 of 384 pending branches belong to complexes at least half done
prioritize main: 82 of 7955 pending branches belong to complexes at least half done
prioritize big: 0 of 383 pending branches belong to complexes at least half done
prioritize main: 78 of 7951 pending branches belong to complexes at least half done
prioritize big: 0 of 381 pending branches belong to complexes at least half done
prioritize main: 75 of 7948 pending branches belong to complexes at least half done
prioritize big: 0 of 380 pending branches belong to complexes at least half done
```
