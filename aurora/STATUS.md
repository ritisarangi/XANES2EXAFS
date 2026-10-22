# Zn scan campaign on Aurora: status

Generated 2026-10-22 12:31 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1553 done, 384 started (running/stopped/failed), 5945 continuations ready, 2293 not started, 10175 total
queue main: 7704 of 25193 waiting, 384 ORCA runs active
queue big: 534 of 1935 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 48,996.8 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8950977 | zn_main | capacity | 16 | 06:00 | R | 04:46 |
| 8952802 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
prioritize big: 28 of 534 pending branches belong to complexes at least half done
prioritize main: 0 of 7729 pending branches belong to complexes at least half done
prioritize big: 28 of 534 pending branches belong to complexes at least half done
[2026-10-22 10:26:57] STATUS.md pushed
prioritize main: 0 of 7722 pending branches belong to complexes at least half done
prioritize big: 28 of 534 pending branches belong to complexes at least half done
prioritize main: 0 of 7716 pending branches belong to complexes at least half done
prioritize big: 28 of 534 pending branches belong to complexes at least half done
prioritize main: 0 of 7712 pending branches belong to complexes at least half done
prioritize big: 28 of 534 pending branches belong to complexes at least half done
prioritize main: 0 of 7708 pending branches belong to complexes at least half done
prioritize big: 28 of 534 pending branches belong to complexes at least half done
```
