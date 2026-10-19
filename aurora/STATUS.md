# Zn scan campaign on Aurora: status

Generated 2026-10-19 11:51 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 367 done, 573 started (running/stopped/failed), 6244 continuations ready, 2991 not started, 10175 total
queue main: 8843 of 16842 waiting, 381 ORCA runs active
queue big: 392 of 791 waiting, 192 ORCA runs active
failed ORCA runs not retried: 0
allocation: 22,206.8 Node Hours available on isaac
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8940426 | zn_main | small | 256 | 06:00 | Q | -- |
| 8945717 | zn_big | capacity | 16 | 06:00 | R | 05:00 |
| 8946081 | zn_main | capacity | 16 | 02:00 | R | 01:34 |

## Last autopilot actions

```
[2026-10-19 07:41:49] STATUS.md pushed
[2026-10-19 09:41:27] publish: publish: 2 complexes added (590 passing points), 0 not exported; 3 complexes published in total pushed: 8f0cf96 Aurora results: 3 complexes published (2026-10-19 09:41) 
[2026-10-19 09:41:36] autopilot started (pid 317237, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at ce4718c, accounts: isaac ModCon)
[2026-10-19 09:42:33] new farms go to project isaac (22298 node-hours left)
[2026-10-19 09:57:08] publish: publish: no newly finished complexes nothing new to commit 
[2026-10-19 09:57:46] STATUS.md pushed
[2026-10-19 10:10:13] submitting main capacity farm on isaac, 2 h (queue 9230 left)
logs tagged as cancelled: 0
no stopped branches found
main farm jobs already queued or running (8939977 8940426): continuations go to the front of the live queue
queue: 0 continuations added to the front of queue/main (9230 pending now)
2026-10-19 10:11:25 farm 8946081.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=2 account=isaac tasks_left=9230
```
