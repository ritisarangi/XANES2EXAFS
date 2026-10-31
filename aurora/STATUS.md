# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-31 15:51 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8985 done, 0 started (running/stopped/failed), 1190 continuations ready, 0 not started, 10175 total
queue main: 992 of 44884 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,321.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |
| 8994906 | zn_main | capacity | 16 | 06:00 | Q | -- |
| 8995873 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 765 finished (765 copied back to Aurora), 168 running, 27 queued, 0 need review, 960 total
stops at the 48 h limit so far: 177; failed runs: 91
1452 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 26 / 30 |
| CAWKIW | 30 / 30 |
| DOZVOF | 30 / 30 |
| FAXYIP | 5 / 30 |
| FUXMAM | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 29 / 30 |
| JUQXUO | 25 / 30 |
| LAJGIM | 23 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 15 / 30 |
| SONROE | 30 / 30 |
| TELRUZ | 4 / 30 |
| TEYSOG | 5 / 30 |
| TIFNUU | 21 / 30 |
| UWAVOF | 4 / 30 |
| UYORAE | 4 / 30 |
| WEQZAT01 | 4 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-31 15:25:21] status: 198 jobs queued/running, 762 branches finished (762 back on Aurora), 0 need review
[2026-10-31 15:36:37] status: 198 jobs queued/running, 762 branches finished (762 back on Aurora), 0 need review
[2026-10-31 15:48:13] scans/JUQXUO/bond_Zn-N9_pos finished (job 60553203)
[2026-10-31 15:48:46] scans/JUQXUO/angle_S1-Zn-S2_neg finished (job 60553179)
[2026-10-31 15:48:46] status: 196 jobs queued/running, 764 branches finished (762 back on Aurora), 0 need review
[2026-10-31 16:00:21] scans/TIFNUU/twist_S5-S6-S7-S8_neg finished (job 60553389)
[2026-10-31 16:02:41] copied 3 finished branches back to Aurora: SUCCEEDED
[2026-10-31 16:02:41] status: 195 jobs queued/running, 765 branches finished (765 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 224 of 992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 13:22:26] publish: publish: 1 complexes added (293 passing points), 0 not exported; 239 complexes published in total pushed: 875bc80 Aurora results: 239 complexes published (2026-10-31 13:22) 
prioritize main: 224 of 992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 14:00:09] STATUS.md pushed
prioritize main: 224 of 992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
