# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-31 02:59 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8859 done, 0 started (running/stopped/failed), 1316 continuations ready, 0 not started, 10175 total
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
branches: 617 finished (614 copied back to Aurora), 193 running, 0 queued, 0 need review, 810 total
stops at the 48 h limit so far: 173; failed runs: 91
1448 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 25 / 30 |
| CAWKIW | 4 / 30 |
| DOZVOF | 30 / 30 |
| FUXMAM | 9 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 15 / 30 |
| JUQXUO | 4 / 30 |
| LAJGIM | 8 / 30 |
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
[2026-10-31 02:25:26] status: 196 jobs queued/running, 614 branches finished (607 back on Aurora), 0 need review
[2026-10-31 02:40:44] copied 7 finished branches back to Aurora: SUCCEEDED
[2026-10-31 02:40:44] status: 196 jobs queued/running, 614 branches finished (614 back on Aurora), 0 need review
[2026-10-31 02:52:23] scans/BUNNII/twist_S128-S130-S132-S134_neg finished (job 60478581)
[2026-10-31 02:52:23] status: 195 jobs queued/running, 615 branches finished (614 back on Aurora), 0 need review
[2026-10-31 03:04:00] scans/FUXMAM/angle_S2-Zn-N4_neg finished (job 60553106)
[2026-10-31 03:04:32] scans/FUXMAM/tilt_Zn-S1-C7-C8_pos finished (job 60553127)
[2026-10-31 03:04:32] status: 193 jobs queued/running, 617 branches finished (614 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 00:54:14] STATUS.md pushed
[2026-10-31 01:11:03] publish: publish: 10 complexes added (2853 passing points), 0 not exported; 237 complexes published in total pushed: 8aa56d8 Aurora results: 237 complexes published (2026-10-31 01:10) 
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
