# Zn scan campaign on Aurora: status

Generated 2026-10-22 08:31 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1506 done, 384 started (running/stopped/failed), 5992 continuations ready, 2293 not started, 10175 total
queue main: 7751 of 25193 waiting, 384 ORCA runs active
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
| 8950977 | zn_main | capacity | 16 | 06:00 | R | 00:46 |
| 8952802 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
NODES=0: queue updated, no farm submitted
[2026-10-22 06:53:18] submitting big farm on ModCon (queue 534 left, 1 big farms)
logs tagged as cancelled: 0
no stopped branches found
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (534 pending now)
2026-10-22 06:54:47 farm 8952802.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=534
prioritize main: 31 of 8139 pending branches belong to complexes at least half done
prioritize big: 28 of 534 pending branches belong to complexes at least half done
[2026-10-22 07:57:03] publish: publish: 1 complexes added (302 passing points), 0 not exported; 21 complexes published in total pushed: 568905a Aurora results: 21 complexes published (2026-10-22 07:57) 
prioritize main: 0 of 7752 pending branches belong to complexes at least half done
prioritize big: 28 of 534 pending branches belong to complexes at least half done
```
