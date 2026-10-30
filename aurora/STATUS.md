# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-30 07:48 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8353 done, 768 started (running/stopped/failed), 1054 continuations ready, 0 not started, 10175 total
queue main: 923 of 43644 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,725.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |
| 8988070 | zn_main | capacity | 16 | 06:00 | R | 01:36 |
| 8988123 | zn_main | capacity | 16 | 06:00 | R | 01:20 |

## NERSC Perlmutter (big pool)

The 22 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 530 finished (529 copied back to Aurora), 130 running, 0 queued, 0 need review, 660 total
stops at the 48 h limit so far: 173; failed runs: 91
1430 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 20 / 30 |
| CAPWIB | 4 / 30 |
| CATZUS10 | 18 / 30 |
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
[2026-10-30 06:57:57] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-30 06:57:57] status: 131 jobs queued/running, 529 branches finished (529 back on Aurora), 0 need review
[2026-10-30 07:08:45] status: 131 jobs queued/running, 529 branches finished (529 back on Aurora), 0 need review
[2026-10-30 07:19:33] status: 131 jobs queued/running, 529 branches finished (529 back on Aurora), 0 need review
[2026-10-30 07:30:18] status: 131 jobs queued/running, 529 branches finished (529 back on Aurora), 0 need review
[2026-10-30 07:41:38] scans/CATZUS10/twist_N4-N22-N40-N58_neg finished (job 60483071)
[2026-10-30 07:41:38] status: 130 jobs queued/running, 530 branches finished (529 back on Aurora), 0 need review
[2026-10-30 07:52:24] status: 130 jobs queued/running, 530 branches finished (529 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 230 of 1705 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-30 05:26:03] STATUS.md pushed
prioritize main: 230 of 1705 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 230 of 1705 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-30 06:28:22] publish: publish: 1 complexes added (284 passing points), 0 not exported; 219 complexes published in total pushed: 65454a4 Aurora results: 219 complexes published (2026-10-30 06:28) 
prioritize main: 0 of 931 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 924 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
