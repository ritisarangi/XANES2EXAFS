# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-31 09:29 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 8923 done, 0 started (running/stopped/failed), 1252 continuations ready, 0 not started, 10175 total
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
branches: 681 finished (678 copied back to Aurora), 129 running, 0 queued, 0 need review, 810 total
stops at the 48 h limit so far: 177; failed runs: 91
1450 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 30 / 30 |
| CAPWIB | 30 / 30 |
| CATZUS10 | 26 / 30 |
| CAWKIW | 29 / 30 |
| DOZVOF | 30 / 30 |
| FUXMAM | 25 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 22 / 30 |
| JUQXUO | 11 / 30 |
| LAJGIM | 14 / 30 |
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
[2026-10-31 09:21:48] scans/LAJGIM/tilt_Zn-S2-C6-C26_pos finished (job 60502630)
[2026-10-31 09:22:21] scans/CAWKIW/angle_S6-Zn-S8_pos finished (job 60553049)
[2026-10-31 09:26:31] copied 7 finished branches back to Aurora: SUCCEEDED
[2026-10-31 09:26:31] status: 132 jobs queued/running, 678 branches finished (678 back on Aurora), 0 need review
[2026-10-31 09:37:45] scans/LAJGIM/tilt_Zn-S4-C8-C28_neg finished (job 60502635)
[2026-10-31 09:38:17] scans/CAWKIW/angle_S8-Zn-N12_neg finished (job 60553057)
[2026-10-31 09:38:50] scans/JUQXUO/angle_N9-Zn-N11_neg finished (job 60553134)
[2026-10-31 09:38:50] status: 129 jobs queued/running, 681 branches finished (678 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 07:26:24] publish: publish: 1 complexes added (182 passing points), 0 not exported; 238 complexes published in total pushed: 54974be Aurora results: 238 complexes published (2026-10-31 07:26) 
[2026-10-31 07:45:19] STATUS.md pushed
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 224 of 1120 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
