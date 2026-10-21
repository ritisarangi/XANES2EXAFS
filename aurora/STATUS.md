# Zn scan campaign on Aurora: status

Generated 2026-10-21 10:53 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1427 done, 576 started (running/stopped/failed), 5856 continuations ready, 2316 not started, 10175 total
queue main: 7805 of 24433 waiting, 384 ORCA runs active
queue big: 367 of 1557 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 19,990.8 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8949575 | zn_main | capacity | 16 | 06:00 | R | 04:14 |
| 8949671 | zn_big | capacity | 16 | 06:00 | R | 02:52 |

## Last autopilot actions

```
prioritize big: 7 of 563 pending branches belong to complexes at least half done
prioritize main: 0 of 7832 pending branches belong to complexes at least half done
prioritize big: 0 of 371 pending branches belong to complexes at least half done
[2026-10-21 08:47:18] STATUS.md pushed
prioritize main: 0 of 7830 pending branches belong to complexes at least half done
prioritize big: 0 of 370 pending branches belong to complexes at least half done
prioritize main: 4 of 7820 pending branches belong to complexes at least half done
prioritize big: 0 of 368 pending branches belong to complexes at least half done
prioritize main: 0 of 7816 pending branches belong to complexes at least half done
prioritize big: 0 of 367 pending branches belong to complexes at least half done
prioritize main: 0 of 7808 pending branches belong to complexes at least half done
prioritize big: 0 of 367 pending branches belong to complexes at least half done
```
