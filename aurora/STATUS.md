# Zn scan campaign on Aurora: status

Generated 2026-10-24 17:20 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 6735 done, 192 started (running/stopped/failed), 2944 continuations ready, 304 not started, 10175 total
queue main: 2937 of 39254 waiting, 0 ORCA runs active
queue big: 311 of 503 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 44,037.8 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8957984 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8959031 | zn_big | capacity | 16 | 06:00 | R | 00:56 |

## Last autopilot actions

```
prioritize main: 465 of 2937 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
prioritize main: 465 of 2937 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
[2026-10-24 14:47:44] publish: publish: no newly finished complexes 
[2026-10-24 15:19:20] STATUS.md pushed
prioritize main: 465 of 2937 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
prioritize main: 465 of 2937 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
prioritize main: 465 of 2937 pending branches belong to complexes at least half done
prioritize big: 0 of 311 pending branches belong to complexes at least half done
```
