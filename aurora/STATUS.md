# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-31 07:26 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8896 done, 0 started (running/stopped/failed), 1279 continuations ready, 0 not started, 10175 total
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
branches: 666 finished (660 copied back to Aurora), 144 running, 0 queued, 0 need review, 810 total
stops at the 48 h limit so far: 177; failed runs: 91
1449 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 26 / 30 |
| CAWKIW | 25 / 30 |
| DOZVOF | 30 / 30 |
| FUXMAM | 20 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 21 / 30 |
| JUQXUO | 8 / 30 |
| LAJGIM | 12 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 6 / 30 |
| SONROE | 30 / 30 |
| TIFNUU | 4 / 30 |
| UYORAE | 4 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-31 07:28:41] status: 150 jobs queued/running, 660 branches finished (660 back on Aurora), 0 need review
[2026-10-31 07:40:07] scans/CAWKIW/bond_Zn-S6_pos finished (job 60553063)
[2026-10-31 07:40:39] scans/CAWKIW/bond_Zn-S8_pos finished (job 60553064)
[2026-10-31 07:41:12] scans/CAWKIW/bond_Zn-N12_pos finished (job 60553062)
[2026-10-31 07:41:44] scans/CAWKIW/angle_S6-Zn-S8_neg finished (job 60553047)
[2026-10-31 07:42:16] scans/CAWKIW/tilt_Zn-N12-C54-C56_neg finished (job 60553068)
[2026-10-31 07:42:48] scans/SEJZOW/bond_Zn-N4_pos finished (job 60553276)
[2026-10-31 07:42:48] status: 144 jobs queued/running, 666 branches finished (660 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 05:17:05] STATUS.md pushed
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 07:26:24] publish: publish: 1 complexes added (182 passing points), 0 not exported; 238 complexes published in total pushed: 54974be Aurora results: 238 complexes published (2026-10-31 07:26) 
```
