# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-25 03:25 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7059 done, 385 started (running/stopped/failed), 2427 continuations ready, 304 not started, 10175 total
queue main: 2236 of 39254 waiting, 384 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,945.5 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8957984 | zn_main | capacity | 16 | 06:00 | R | 05:10 |

## Last autopilot actions

```
[2026-10-25 02:23:39] new farms go to project ModCon (43945 node-hours left)
prioritize main: 0 of 2284 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 02:46:31] publish: publish: 20 complexes added (5177 passing points), 1 not exported; 160 complexes published in total pushed: d03d594 Aurora results: 160 complexes published (2026-10-25 02:46) 
[2026-10-25 02:57:50] STATUS.md pushed
prioritize main: 0 of 2240 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 03:20:22] autopilot started (pid 2055893, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 9a4e7b6, accounts: isaac ModCon)
[2026-10-25 03:22:31] new farms go to project ModCon (43945 node-hours left)
prioritize main: 0 of 2238 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 03:25:13] publish: publish: 5 complexes added (1371 passing points), 0 not exported; 165 complexes published in total pushed: 70a22ed Aurora results: 165 complexes published (2026-10-25 03:25) 
```
