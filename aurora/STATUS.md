# Zn scan campaign on Aurora: status

Generated 2026-10-21 17:25 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1478 done, 384 started (running/stopped/failed), 6003 continuations ready, 2310 not started, 10175 total
queue main: 7763 of 24814 waiting, 384 ORCA runs active
queue big: 549 of 1745 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 49,110.5 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8950006 | zn_main | capacity | 16 | 06:00 | R | 04:42 |
| 8950108 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
prioritize big: 2 of 549 pending branches belong to complexes at least half done
[2026-10-21 16:04:36] new farms go to project ModCon (49112 node-hours left)
[2026-10-21 16:04:36] moved queued farm 8939977 from isaac to ModCon (allocation not usable)
[2026-10-21 16:04:36] moved queued farm 8940280 from isaac to ModCon (allocation not usable)
[2026-10-21 16:04:37] moved queued farm 8947436 from isaac to ModCon (allocation not usable)
[2026-10-21 16:04:37] moved queued farm 8950108 from isaac to ModCon (allocation not usable)
prioritize main: 0 of 7773 pending branches belong to complexes at least half done
prioritize big: 2 of 549 pending branches belong to complexes at least half done
prioritize main: 0 of 7769 pending branches belong to complexes at least half done
prioritize big: 2 of 549 pending branches belong to complexes at least half done
prioritize main: 0 of 7765 pending branches belong to complexes at least half done
prioritize big: 2 of 549 pending branches belong to complexes at least half done
```
