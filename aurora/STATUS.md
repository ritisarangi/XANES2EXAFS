# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-28 12:45 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7819 done, 0 started (running/stopped/failed), 2349 continuations ready, 7 not started, 10175 total
queue main: 2285 of 41520 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,343.7 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8976721 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8976814 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 469 finished (469 copied back to Aurora), 71 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 120; failed runs: 91
1294 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 4 / 30 |
| CATZUS10 | 4 / 30 |
| DOZVOF | 29 / 30 |
| GUCSED | 29 / 30 |
| GUFHEU | 25 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 30 / 30 |
| WIGBIX | 18 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-28 11:55:51] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-28 11:55:51] status: 72 jobs queued/running, 468 branches finished (468 back on Aurora), 0 need review
[2026-10-28 12:06:56] scans/WIGBIX/tilt_Zn-N39-C40-H100_neg finished (job 60361672)
[2026-10-28 12:06:56] status: 71 jobs queued/running, 469 branches finished (468 back on Aurora), 0 need review
[2026-10-28 12:17:29] status: 71 jobs queued/running, 469 branches finished (468 back on Aurora), 0 need review
[2026-10-28 12:28:54] copied 1 finished branches back to Aurora: SUCCEEDED
[2026-10-28 12:28:54] status: 71 jobs queued/running, 469 branches finished (469 back on Aurora), 0 need review
[2026-10-28 12:39:29] status: 71 jobs queued/running, 469 branches finished (469 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-28 10:36:42] autopilot started (pid 3343153, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at 3f10a92, accounts: isaac ModCon)
[2026-10-28 10:40:14] new farms go to project ModCon (43343 node-hours left)
prioritize main: 125 of 2285 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-28 10:43:53] publish: publish: 3 complexes added (809 passing points), 0 not exported; 212 complexes published in total pushed: 7695bd0 Aurora results: 212 complexes published (2026-10-28 10:43) 
[2026-10-28 10:45:50] STATUS.md pushed
prioritize main: 125 of 2285 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 125 of 2285 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 125 of 2285 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
