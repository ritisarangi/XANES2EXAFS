# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-30 19:30 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8690 done, 767 started (running/stopped/failed), 718 continuations ready, 0 not started, 10175 total
queue main: 488 of 44270 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,522.4 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |
| 8990248 | zn_main | capacity | 16 | 06:00 | R | 03:48 |
| 8990398 | zn_main | capacity | 16 | 06:00 | R | 03:46 |

## NERSC Perlmutter (big pool)

The 27 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 586 finished (583 copied back to Aurora), 224 running, 0 queued, 0 need review, 810 total
stops at the 48 h limit so far: 173; failed runs: 91
1443 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 26 / 30 |
| CAPWIB | 28 / 30 |
| CATZUS10 | 20 / 30 |
| CAWKIW | 4 / 30 |
| DOZVOF | 30 / 30 |
| FUXMAM | 4 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 8 / 30 |
| JUQXUO | 3 / 30 |
| LAJGIM | 4 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 4 / 30 |
| SONROE | 30 / 30 |
| TIFNUU | 3 / 30 |
| UYORAE | 2 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-30 18:56:30] status: 227 jobs queued/running, 583 branches finished (583 back on Aurora), 0 need review
[2026-10-30 19:07:53] status: 227 jobs queued/running, 583 branches finished (583 back on Aurora), 0 need review
[2026-10-30 19:19:12] status: 227 jobs queued/running, 583 branches finished (583 back on Aurora), 0 need review
[2026-10-30 19:31:50] scans/UYORAE/bond_Zn-S1_neg finished (job 60502683)
[2026-10-30 19:31:50] status: 226 jobs queued/running, 584 branches finished (583 back on Aurora), 0 need review
[2026-10-30 19:43:38] scans/CATZUS10/angle_N4-Zn-N40_pos finished (job 60479141)
[2026-10-30 19:44:13] scans/CAPWIB/angle_S8-Zn-S10_pos finished (job 60502415)
[2026-10-30 19:44:13] status: 224 jobs queued/running, 586 branches finished (583 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 0 of 610 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 608 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-30 17:25:49] STATUS.md pushed
prioritize main: 0 of 591 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 553 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-30 18:47:22] publish: publish: no newly finished complexes 
prioritize main: 0 of 513 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
