# Zn scan campaign on Aurora: status

Generated 2026-10-22 01:42 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1487 done, 192 started (running/stopped/failed), 6190 continuations ready, 2306 not started, 10175 total
queue main: 8139 of 25193 waiting, 0 ORCA runs active
queue big: 357 of 1745 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 49,094.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8950108 | zn_big | capacity | 16 | 06:00 | R | 01:10 |
| 8950977 | zn_main | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
prioritize main: 31 of 8139 pending branches belong to complexes at least half done
prioritize big: 2 of 549 pending branches belong to complexes at least half done
prioritize main: 31 of 8139 pending branches belong to complexes at least half done
prioritize big: 2 of 549 pending branches belong to complexes at least half done
[2026-10-21 23:37:26] STATUS.md pushed
prioritize main: 31 of 8139 pending branches belong to complexes at least half done
prioritize big: 2 of 549 pending branches belong to complexes at least half done
prioritize main: 31 of 8139 pending branches belong to complexes at least half done
prioritize big: 0 of 357 pending branches belong to complexes at least half done
[2026-10-22 01:31:52] publish: publish: no newly finished complexes nothing new to commit 
prioritize main: 31 of 8139 pending branches belong to complexes at least half done
prioritize big: 0 of 357 pending branches belong to complexes at least half done
```
