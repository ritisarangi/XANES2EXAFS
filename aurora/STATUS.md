# Zn scan campaign on Aurora: status

Generated 2026-10-24 23:33 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 6806 done, 385 started (running/stopped/failed), 2680 continuations ready, 304 not started, 10175 total
queue main: 2489 of 39254 waiting, 384 ORCA runs active
queue big: 495 of 693 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,945.5 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8957984 | zn_main | capacity | 16 | 06:00 | R | 01:18 |
| 8961548 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (495 pending now)
NODES=0: queue updated, no farm submitted
[2026-10-24 22:54:14] submitting big farm on ModCon (queue 495 left, 1 big farms)
logs tagged as cancelled: 0
scans/UDOCUL/twist_S1-N3-N4-N5_neg: running now; left alone
wrote scans/jobs_restart.txt (2 branches)
big farm jobs already queued or running (8940280): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/big (495 pending now)
2026-10-24 22:59:38 farm 8961548.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=big cores=8 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=495
prioritize main: 32 of 2504 pending branches belong to complexes at least half done
prioritize big: 18 of 495 pending branches belong to complexes at least half done
```
