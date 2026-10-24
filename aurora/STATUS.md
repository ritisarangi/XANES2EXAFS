# Zn scan campaign on Aurora: status

Generated 2026-10-24 04:33 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 6010 done, 3662 started (running/stopped/failed), 199 continuations ready, 304 not started, 10175 total
queue main: 0 of 36317 waiting, 3644 ORCA runs active
queue big: 503 of 503 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 45,482.8 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | H | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8957984 | zn_main | capacity | 16 | 06:00 | H | -- |
| 8958138 | zn_main | small | 256 | 06:00 | R | 02:20 |
| 8959031 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
queue: 0 continuations added to the front of queue/big (503 pending now)
2026-10-24 02:21:57 farm 8959031.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=503
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
[2026-10-24 02:26:42] publish: publish: no newly finished complexes 
[2026-10-24 02:29:25] STATUS.md pushed
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
```
