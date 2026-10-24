# Zn scan campaign on Aurora: status

Generated 2026-10-24 10:25 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 6735 done, 0 started (running/stopped/failed), 3136 continuations ready, 304 not started, 10175 total
queue main: 2937 of 39254 waiting, 0 ORCA runs active
queue big: 503 of 503 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 44,037.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8940280 | zn_big | capacity | 16 | 24:00 | Q | -- |
| 8957984 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8959031 | zn_big | capacity | 16 | 06:00 | Q | -- |

## Last autopilot actions

```
[2026-10-24 08:19:30] autopilot started (pid 1301985, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 1d6ee32, accounts: isaac ModCon)
[2026-10-24 08:22:59] new farms go to project ModCon (44037 node-hours left)
prioritize main: 465 of 2937 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
[2026-10-24 08:37:39] publish: publish: 80 complexes added (22646 passing points), 1 not exported; 140 complexes published in total pushed: 3a4bca1 Aurora results: 140 complexes published (2026-10-24 08:37) 
[2026-10-24 08:39:51] STATUS.md pushed
prioritize main: 465 of 2937 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
prioritize main: 465 of 2937 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
prioritize main: 465 of 2937 pending branches belong to complexes at least half done
prioritize big: 24 of 503 pending branches belong to complexes at least half done
```
