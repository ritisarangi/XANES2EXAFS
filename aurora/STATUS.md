# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-31 11:30 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8942 done, 0 started (running/stopped/failed), 1233 continuations ready, 0 not started, 10175 total
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
branches: 704 finished (704 copied back to Aurora), 106 running, 0 queued, 0 need review, 810 total
stops at the 48 h limit so far: 177; failed runs: 91
1450 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 26 / 30 |
| CAWKIW | 30 / 30 |
| DOZVOF | 30 / 30 |
| FUXMAM | 28 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 24 / 30 |
| JUQXUO | 17 / 30 |
| LAJGIM | 16 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 10 / 30 |
| SONROE | 30 / 30 |
| TIFNUU | 9 / 30 |
| UYORAE | 4 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-31 11:14:36] status: 111 jobs queued/running, 699 branches finished (697 back on Aurora), 0 need review
[2026-10-31 11:25:50] scans/LAJGIM/bond_Zn-S1_pos finished (job 60502607)
[2026-10-31 11:26:22] scans/FUXMAM/angle_S2-Zn-N3_neg finished (job 60553103)
[2026-10-31 11:26:54] scans/JUQXUO/angle_S1-Zn-N11_neg finished (job 60553144)
[2026-10-31 11:27:27] scans/JUQXUO/tilt_Zn-S2-C35-C44_pos finished (job 60553229)
[2026-10-31 11:27:59] scans/TIFNUU/tilt_Zn-S7-C23-N19_neg finished (job 60553377)
[2026-10-31 11:32:28] copied 7 finished branches back to Aurora: SUCCEEDED
[2026-10-31 11:32:28] status: 106 jobs queued/running, 704 branches finished (704 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 09:41:12] STATUS.md pushed
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
