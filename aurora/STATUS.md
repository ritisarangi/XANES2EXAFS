# Zn scan campaign on Aurora: status

Generated 2026-10-21 13:19 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 1449 done, 576 started (running/stopped/failed), 5840 continuations ready, 2310 not started, 10175 total
queue main: 7789 of 24814 waiting, 384 ORCA runs active
queue big: 361 of 1557 waiting, 191 ORCA runs active
failed ORCA runs not retried: 2
allocation: 19,514.4 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | Q | -- |
| 8949671 | zn_big | capacity | 16 | 06:00 | R | 05:18 |
| 8950006 | zn_main | capacity | 16 | 06:00 | R | 00:34 |

## Last autopilot actions

```
NODES=0: queue updated, no farm submitted
[2026-10-21 12:30:29] submitting main capacity farm on isaac, 6 h (queue 8174 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8947436): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (8174 pending now)
2026-10-21 12:30:59 farm 8950006.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=isaac tasks_left=8174
prioritize main: 18 of 8174 pending branches belong to complexes at least half done
prioritize big: 0 of 364 pending branches belong to complexes at least half done
[2026-10-21 13:08:45] publish: publish: 5 complexes added (1093 passing points), 0 not exported; 19 complexes published in total pushed: 63dcda4 Aurora results: 19 complexes published (2026-10-21 13:08) 
prioritize main: 0 of 7789 pending branches belong to complexes at least half done
prioritize big: 0 of 361 pending branches belong to complexes at least half done
```
