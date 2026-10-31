# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-31 17:51 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8994 done, 0 started (running/stopped/failed), 1181 continuations ready, 0 not started, 10175 total
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
branches: 781 finished (781 copied back to Aurora), 179 running, 0 queued, 0 need review, 960 total
stops at the 48 h limit so far: 177; failed runs: 93
1452 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 27 / 30 |
| CAWKIW | 30 / 30 |
| DOZVOF | 30 / 30 |
| FAXYIP | 7 / 30 |
| FUXMAM | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 30 / 30 |
| JUQXUO | 27 / 30 |
| LAJGIM | 24 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 15 / 30 |
| SONROE | 30 / 30 |
| TELRUZ | 6 / 30 |
| TEYSOG | 8 / 30 |
| TIFNUU | 23 / 30 |
| UWAVOF | 4 / 30 |
| UYORAE | 4 / 30 |
| WEQZAT01 | 6 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-31 17:39:25] scans/TELRUZ/tilt_Zn-S1-C7-C8_pos finished (job 60613344)
[2026-10-31 17:39:57] scans/WEQZAT01/tilt_Zn-S1-C6-C11_pos finished (job 60613556)
[2026-10-31 17:39:57] status: 182 jobs queued/running, 778 branches finished (771 back on Aurora), 0 need review
[2026-10-31 17:51:31] scans/FAXYIP/tilt_Zn-N7-C27-C25_neg finished (job 60613246)
[2026-10-31 17:52:03] scans/TEYSOG/tilt_Zn-S2-C59-C60_neg finished (job 60613408)
[2026-10-31 17:52:08] scans/WEQZAT01/tilt_Zn-S1-C6-C11_neg finished (job 60613554)
[2026-10-31 17:58:12] copied 10 finished branches back to Aurora: SUCCEEDED
[2026-10-31 17:58:12] status: 179 jobs queued/running, 781 branches finished (781 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-31 14:00:09] STATUS.md pushed
prioritize main: 224 of 992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 16:08:53] STATUS.md pushed
prioritize main: 224 of 992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 992 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
