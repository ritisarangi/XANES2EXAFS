# Zn scan campaign on Aurora: status

Generated 2026-10-24 00:45 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 5338 done, 58 started (running/stopped/failed), 4475 continuations ready, 304 not started, 10175 total
queue main: 4337 of 36317 waiting, 0 ORCA runs active
queue big: -2015 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 4
allocation: 45,483.0 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8957984 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8958138 | zn_main | small | 256 | 06:00 | Q | -- |

## Last autopilot actions

```
main farm jobs already queued or running (8939977 8957984): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (4337 pending now)
2026-10-23 20:37:20 farm 8958138.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=prod nodes=256 hours=6 account=ModCon tasks_left=4337
prioritize main: 654 of 4337 pending branches belong to complexes at least half done
prioritize big: 0 of 311 pending branches belong to complexes at least half done
[2026-10-23 20:44:41] publish: publish: 22 complexes added (6372 passing points), 0 not exported; 60 complexes published in total pushed: 85c13f8 Aurora results: 60 complexes published (2026-10-23 20:44) 
[2026-10-23 20:48:49] STATUS.md pushed
prioritize main: 654 of 4337 pending branches belong to complexes at least half done
prioritize big: 0 of 309 pending branches belong to complexes at least half done
prioritize main: 654 of 4337 pending branches belong to complexes at least half done
prioritize big: 0 of 308 pending branches belong to complexes at least half done
[2026-10-23 22:38:57] STATUS.md pushed
```
