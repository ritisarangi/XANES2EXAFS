# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-11-01 10:27 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 10037 done, 0 started (running/stopped/failed), 138 continuations ready, 0 not started, 10175 total
queue main: 118 of 45552 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 41,418.4 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 9013664 | zn_main | small | 256 | 04:00 | Q | -- |
| 9013865 | zn_main | small | 256 | 06:00 | Q | -- |
| 9019151 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 943 finished (943 copied back to Aurora), 17 running, 0 queued, 0 need review, 960 total
stops at the 48 h limit so far: 201; failed runs: 93
1454 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 29 / 30 |
| CAWKIW | 30 / 30 |
| DOZVOF | 30 / 30 |
| FAXYIP | 30 / 30 |
| FUXMAM | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 30 / 30 |
| JUQXUO | 30 / 30 |
| LAJGIM | 30 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 28 / 30 |
| SONROE | 30 / 30 |
| TELRUZ | 30 / 30 |
| TEYSOG | 29 / 30 |
| TIFNUU | 30 / 30 |
| UWAVOF | 30 / 30 |
| UYORAE | 17 / 30 |
| WEQZAT01 | 30 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-11-01 10:04:48] status: 20 jobs queued/running, 940 branches finished (940 back on Aurora), 0 need review
[2026-11-01 10:15:30] scans/CATZUS10/angle_N40-Zn-N58_neg finished (job 60604640)
[2026-11-01 10:15:30] status: 19 jobs queued/running, 941 branches finished (940 back on Aurora), 0 need review
[2026-11-01 10:25:41] status: 19 jobs queued/running, 941 branches finished (940 back on Aurora), 0 need review
[2026-11-01 10:36:28] scans/UYORAE/angle_S1-Zn-S2_pos finished (job 60630729)
[2026-11-01 10:37:00] scans/UYORAE/tilt_Zn-N12-C69-C67_pos finished (job 60630741)
[2026-11-01 10:38:59] copied 3 finished branches back to Aurora: SUCCEEDED
[2026-11-01 10:38:59] status: 17 jobs queued/running, 943 branches finished (943 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-11-01 06:55:55] publish: publish: 22 complexes added (6150 passing points), 0 not exported; 285 complexes published in total pushed: 22aacfb Aurora results: 285 complexes published (2026-11-01 06:55) 
[2026-11-01 07:13:23] STATUS.md pushed
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-11-01 08:23:32] STATUS.md pushed
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 80 of 118 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
