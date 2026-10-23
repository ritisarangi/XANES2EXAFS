# Zn scan campaign on Aurora: status

Generated 2026-10-23 10:32 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 2841 done, 6254 started (running/stopped/failed), 97 continuations ready, 983 not started, 10175 total
queue main: 757 of 25981 waiting, 6073 ORCA runs active
queue big: 323 of 2127 waiting, 192 ORCA runs active
failed ORCA runs not retried: 2
allocation: 48,717.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8947436 | zn_main | small | 256 | 06:00 | R | 05:30 |
| 8954403 | zn_big | capacity | 16 | 06:00 | R | 00:30 |
| 8956596 | zn_main | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
wrote scans/jobs_restart.txt (17 branches)
main farm jobs already queued or running (8939977 8947436): continuations go to the front of the live queue
queue: 21 continuations added to the front of queue/main (806 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-23 10:14:52] submitting main capacity farm on ModCon, 6 h (queue 801 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8947436): continuations go to the front of the live queue
queue: 7 continuations added to the front of queue/main (783 pending now)
2026-10-23 10:18:31 farm 8956596.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=783
prioritize main: 0 of 757 pending branches belong to complexes at least half done
prioritize big: 0 of 323 pending branches belong to complexes at least half done
```
