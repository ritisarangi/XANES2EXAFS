# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-30 17:18 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8575 done, 769 started (running/stopped/failed), 831 continuations ready, 0 not started, 10175 total
queue main: 598 of 44270 waiting, 768 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,522.4 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8987775 | zn_main | small | 256 | 04:00 | Q | -- |
| 8990248 | zn_main | capacity | 16 | 06:00 | R | 01:30 |
| 8990398 | zn_main | capacity | 16 | 06:00 | R | 01:28 |

## NERSC Perlmutter (big pool)

The 27 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 579 finished (577 copied back to Aurora), 208 running, 23 queued, 0 need review, 810 total
stops at the 48 h limit so far: 173; failed runs: 91
1441 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 25 / 30 |
| CAPWIB | 26 / 30 |
| CATZUS10 | 19 / 30 |
| CAWKIW | 4 / 30 |
| DOZVOF | 30 / 30 |
| FUXMAM | 4 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 7 / 30 |
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
| UYORAE | 0 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-30 16:54:07] scans/CAPWIB/angle_S10-Zn-N14_neg finished (job 60502402)
[2026-10-30 16:54:39] scans/CAPWIB/tilt_Zn-N12-C29-C31_neg finished (job 60502457)
[2026-10-30 16:56:06] copied 2 finished branches back to Aurora: SUCCEEDED
[2026-10-30 16:56:06] status: 233 jobs queued/running, 577 branches finished (577 back on Aurora), 0 need review
[2026-10-30 17:07:55] scans/CAPWIB/angle_S10-Zn-N12_pos finished (job 60502396)
[2026-10-30 17:07:55] status: 232 jobs queued/running, 578 branches finished (577 back on Aurora), 0 need review
[2026-10-30 17:19:53] scans/CAPWIB/angle_S8-Zn-N14_pos finished (job 60502412)
[2026-10-30 17:19:53] status: 231 jobs queued/running, 579 branches finished (577 back on Aurora), 0 need review
```

## Last autopilot actions

```
2026-10-30 14:43:17 farm 8990398.aurora-pbs-0001.hostmgmt.cm.aurora.alcf.anl.gov pool=main cores=4 queue=capacity nodes=16 hours=6 account=ModCon tasks_left=1379
prioritize main: 214 of 1379 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 214 of 1379 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-30 14:58:59] STATUS.md pushed
prioritize main: 214 of 1379 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 610 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 608 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
