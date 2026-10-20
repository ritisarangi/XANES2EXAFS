# Zn scan campaign on Aurora: status

Generated 2026-10-20 20:23 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1276 done, 0 started (running/stopped/failed), 6570 continuations ready, 2329 not started, 10175 total
queue main: 8327 of 24054 waiting, 0 ORCA runs active
queue big: 572 of 1367 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 20,176.2 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8948275 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8948280 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (572 pending now)
2026-10-20 18:12:36 farm 8948280.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=isaac tasks_left=572
prioritize main: 85 of 8327 pending branches belong to complexes at least half done
prioritize big: 14 of 572 pending branches belong to complexes at least half done
prioritize main: 85 of 8327 pending branches belong to complexes at least half done
prioritize big: 14 of 572 pending branches belong to complexes at least half done
prioritize main: 85 of 8327 pending branches belong to complexes at least half done
prioritize big: 14 of 572 pending branches belong to complexes at least half done
[2026-10-20 20:23:39] publish: publish: 3 complexes added (901 passing points), 0 not exported; 10 complexes published in total pushed: c3ee6c5 Aurora results: 10 complexes published (2026-10-20 20:23) 
```
