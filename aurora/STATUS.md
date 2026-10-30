# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-30 21:28 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8827 done, 751 started (running/stopped/failed), 597 continuations ready, 0 not started, 10175 total
queue main: 378 of 44270 waiting, 751 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,512.9 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |
| 8990248 | zn_main | capacity | 16 | 06:00 | R | 05:34 |
| 8990398 | zn_main | capacity | 16 | 06:00 | R | 05:32 |

## NERSC Perlmutter (big pool)

The 27 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 592 finished (591 copied back to Aurora), 218 running, 0 queued, 0 need review, 810 total
stops at the 48 h limit so far: 173; failed runs: 91
1445 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 27 / 30 |
| CAPWIB | 29 / 30 |
| CATZUS10 | 22 / 30 |
| CAWKIW | 4 / 30 |
| DOZVOF | 30 / 30 |
| FUXMAM | 4 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 9 / 30 |
| JUQXUO | 4 / 30 |
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
[2026-10-30 20:56:19] scans/CATZUS10/angle_N22-Zn-N40_pos finished (job 60478584)
[2026-10-30 20:56:51] scans/JOCZEG/tilt_Zn-N5-C37-H73_neg finished (job 60502520)
[2026-10-30 20:56:51] status: 220 jobs queued/running, 590 branches finished (587 back on Aurora), 0 need review
[2026-10-30 21:08:08] scans/BUNNII/angle_S132-Zn-S134_pos finished (job 60473097)
[2026-10-30 21:10:40] copied 4 finished branches back to Aurora: SUCCEEDED
[2026-10-30 21:10:40] status: 219 jobs queued/running, 591 branches finished (591 back on Aurora), 0 need review
[2026-10-30 21:22:24] scans/CAPWIB/angle_S8-Zn-S10_neg finished (job 60502413)
[2026-10-30 21:22:24] status: 218 jobs queued/running, 592 branches finished (591 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 0 of 553 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-30 18:47:22] publish: publish: no newly finished complexes 
prioritize main: 0 of 513 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-30 19:44:41] STATUS.md pushed
prioritize main: 0 of 455 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 412 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 378 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
