# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-30 10:11 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8460 done, 768 started (running/stopped/failed), 947 continuations ready, 0 not started, 10175 total
queue main: 820 of 43644 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,725.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |
| 8988070 | zn_main | capacity | 16 | 06:00 | R | 04:00 |
| 8988123 | zn_main | capacity | 16 | 06:00 | R | 03:46 |

## NERSC Perlmutter (big pool)

The 22 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 536 finished (536 copied back to Aurora), 124 running, 0 queued, 0 need review, 660 total
stops at the 48 h limit so far: 173; failed runs: 91
1434 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 23 / 30 |
| CAPWIB | 6 / 30 |
| CATZUS10 | 19 / 30 |
| DOZVOF | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 4 / 30 |
| LAJGIM | 4 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SONROE | 30 / 30 |
| UYORAE | 0 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-30 09:45:49] status: 127 jobs queued/running, 533 branches finished (533 back on Aurora), 0 need review
[2026-10-30 09:56:34] status: 127 jobs queued/running, 533 branches finished (533 back on Aurora), 0 need review
[2026-10-30 10:07:51] scans/BUNNII/angle_S128-Zn-S130_pos finished (job 60506100)
[2026-10-30 10:08:24] scans/CAPWIB/angle_N12-Zn-N14_neg finished (job 60502381)
[2026-10-30 10:08:56] scans/CAPWIB/angle_N12-Zn-N14_pos finished (job 60502386)
[2026-10-30 10:08:56] status: 124 jobs queued/running, 536 branches finished (533 back on Aurora), 0 need review
[2026-10-30 10:21:41] copied 3 finished branches back to Aurora: SUCCEEDED
[2026-10-30 10:21:41] status: 124 jobs queued/running, 536 branches finished (536 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-30 06:28:22] publish: publish: 1 complexes added (284 passing points), 0 not exported; 219 complexes published in total pushed: 65454a4 Aurora results: 219 complexes published (2026-10-30 06:28) 
prioritize main: 0 of 931 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 924 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-30 07:59:18] STATUS.md pushed
prioritize main: 0 of 911 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 881 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 838 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
