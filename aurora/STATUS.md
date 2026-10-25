# Zn scan campaign on Aurora: status

Generated 2026-10-25 01:44 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 6969 done, 384 started (running/stopped/failed), 2518 continuations ready, 304 not started, 10175 total
queue main: 2327 of 39254 waiting, 384 ORCA runs active
queue big: 495 of 693 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,945.5 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8957984 | zn_main | capacity | 16 | 06:00 | R | 03:30 |
| 8961548 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
2026-10-24 22:59:38 farm 8961548.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=495
prioritize main: 32 of 2504 pending branches belong to complexes at least half done
prioritize big: 18 of 495 pending branches belong to complexes at least half done
[2026-10-24 23:34:59] STATUS.md pushed
prioritize main: 0 of 2470 pending branches belong to complexes at least half done
prioritize big: 18 of 495 pending branches belong to complexes at least half done
prioritize main: 0 of 2426 pending branches belong to complexes at least half done
prioritize big: 18 of 495 pending branches belong to complexes at least half done
prioritize main: 0 of 2379 pending branches belong to complexes at least half done
prioritize big: 18 of 495 pending branches belong to complexes at least half done
prioritize main: 0 of 2342 pending branches belong to complexes at least half done
prioritize big: 18 of 495 pending branches belong to complexes at least half done
```
