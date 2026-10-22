# Zn scan campaign on Aurora: status

Generated 2026-10-22 18:46 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1582 done, 192 started (running/stopped/failed), 6129 continuations ready, 2272 not started, 10175 total
queue main: 8078 of 25571 waiting, 0 ORCA runs active
queue big: 323 of 1935 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 48,902.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8952802 | zn_big | capacity | 16 | 06:00 | R | 05:44 |
| 8953480 | zn_main | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
prioritize big: 0 of 339 pending branches belong to complexes at least half done
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 0 of 332 pending branches belong to complexes at least half done
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 0 of 328 pending branches belong to complexes at least half done
[2026-10-22 16:38:32] STATUS.md pushed
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 0 of 328 pending branches belong to complexes at least half done
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 0 of 325 pending branches belong to complexes at least half done
prioritize main: 41 of 8078 pending branches belong to complexes at least half done
prioritize big: 0 of 323 pending branches belong to complexes at least half done
```
