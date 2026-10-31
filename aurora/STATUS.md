# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-31 05:03 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8869 done, 0 started (running/stopped/failed), 1306 continuations ready, 0 not started, 10175 total
queue main: 1120 of 45012 waiting, 0 ORCA runs active
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

The 27 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 632 finished (632 copied back to Aurora), 178 running, 0 queued, 0 need review, 810 total
stops at the 48 h limit so far: 173; failed runs: 91
1449 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 26 / 30 |
| CAWKIW | 8 / 30 |
| DOZVOF | 30 / 30 |
| FUXMAM | 15 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 17 / 30 |
| JUQXUO | 4 / 30 |
| LAJGIM | 10 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 4 / 30 |
| SONROE | 30 / 30 |
| TIFNUU | 4 / 30 |
| UYORAE | 4 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-31 04:46:06] status: 182 jobs queued/running, 628 branches finished (624 back on Aurora), 0 need review
[2026-10-31 04:57:51] scans/CAWKIW/twist_S6-N10-S8-N12_pos finished (job 60553084)
[2026-10-31 04:58:24] scans/FUXMAM/tilt_Zn-S1-C7-C8_neg finished (job 60553126)
[2026-10-31 04:58:24] status: 180 jobs queued/running, 630 branches finished (624 back on Aurora), 0 need review
[2026-10-31 05:09:56] scans/CATZUS10/angle_N22-Zn-N40_neg finished (job 60478583)
[2026-10-31 05:10:28] scans/CAWKIW/twist_S6-N10-S8-N12_neg finished (job 60553082)
[2026-10-31 05:15:26] copied 8 finished branches back to Aurora: SUCCEEDED
[2026-10-31 05:15:26] status: 178 jobs queued/running, 632 branches finished (632 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 03:13:58] STATUS.md pushed
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
