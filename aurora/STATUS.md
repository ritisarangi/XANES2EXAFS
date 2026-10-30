# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-30 01:03 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8292 done, 768 started (running/stopped/failed), 1114 continuations ready, 1 not started, 10175 total
queue main: 969 of 42898 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,916.7 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8985662 | zn_main | capacity | 16 | 06:00 | R | 04:56 |
| 8986279 | zn_main | capacity | 16 | 06:00 | R | 04:56 |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 22 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 515 finished (514 copied back to Aurora), 145 running, 0 queued, 0 need review, 660 total
stops at the 48 h limit so far: 173; failed runs: 91
1420 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 12 / 30 |
| CAPWIB | 4 / 30 |
| CATZUS10 | 16 / 30 |
| DOZVOF | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 3 / 30 |
| LAJGIM | 0 / 30 |
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
[2026-10-30 00:26:30] status: 148 jobs queued/running, 512 branches finished (510 back on Aurora), 0 need review
[2026-10-30 00:37:53] scans/BUNNII/angle_S130-Zn-S134_neg finished (job 60477933)
[2026-10-30 00:38:25] scans/JOCZEG/bond_Zn-S3_neg finished (job 60502517)
[2026-10-30 00:40:58] copied 4 finished branches back to Aurora: SUCCEEDED
[2026-10-30 00:40:58] status: 146 jobs queued/running, 514 branches finished (514 back on Aurora), 0 need review
[2026-10-30 00:51:48] status: 146 jobs queued/running, 514 branches finished (514 back on Aurora), 0 need review
[2026-10-30 01:03:12] scans/GUFHEU/angle_S2-Zn-S3_pos finished (job 60490604)
[2026-10-30 01:03:12] status: 145 jobs queued/running, 515 branches finished (514 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 0 of 1089 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 1048 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-29 22:57:21] STATUS.md pushed
prioritize main: 0 of 1017 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 988 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-30 00:26:40] publish: publish: 3 complexes added (865 passing points), 0 not exported; 218 complexes published in total pushed: 7e3efd8 Aurora results: 218 complexes published (2026-10-30 00:26) 
prioritize main: 0 of 975 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
