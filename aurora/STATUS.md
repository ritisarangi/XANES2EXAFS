# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-31 20:34 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 9381 done, 637 started (running/stopped/failed), 157 continuations ready, 0 not started, 10175 total
queue main: 0 of 44884 waiting, 611 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 42,321.6 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | H | -- |
| 8987775 | zn_main | small | 256 | 04:00 | R | 01:42 |
| 8994906 | zn_main | capacity | 16 | 06:00 | H | -- |
| 8995873 | zn_main | capacity | 16 | 06:00 | H | -- |

## NERSC Perlmutter (big pool)

The 32 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 807 finished (803 copied back to Aurora), 153 running, 0 queued, 0 need review, 960 total
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
| FAXYIP | 13 / 30 |
| FUXMAM | 30 / 30 |
| GUCSED | 30 / 30 |
| GUFHEU | 30 / 30 |
| HOMQAC | 30 / 30 |
| ICAVAK | 30 / 30 |
| JOCZEG | 30 / 30 |
| JUQXUO | 28 / 30 |
| LAJGIM | 27 / 30 |
| NAMSOJ | 30 / 30 |
| NECTOG | 30 / 30 |
| NONLEI | 30 / 30 |
| OJEKUJ | 30 / 30 |
| OJELOE | 30 / 30 |
| RAYBIC | 30 / 30 |
| REJBUD | 30 / 30 |
| SEJZOW | 18 / 30 |
| SONROE | 30 / 30 |
| TELRUZ | 11 / 30 |
| TEYSOG | 11 / 30 |
| TIFNUU | 26 / 30 |
| UWAVOF | 4 / 30 |
| UYORAE | 4 / 30 |
| WEQZAT01 | 8 / 30 |
| WIGBIX | 30 / 30 |
| WORMAR | 30 / 30 |
| WUJZOS | 30 / 30 |

Last driver actions:

```
[2026-10-31 20:31:16] scans/FAXYIP/tilt_Zn-N10-C59-C57_neg finished (job 60613225)
[2026-10-31 20:34:52] copied 6 finished branches back to Aurora: SUCCEEDED
[2026-10-31 20:34:52] status: 157 jobs queued/running, 803 branches finished (803 back on Aurora), 0 need review
[2026-10-31 20:46:20] scans/LAJGIM/angle_S2-Zn-S4_pos finished (job 60502595)
[2026-10-31 20:46:52] scans/FAXYIP/tilt_Zn-S2-C64-N11_pos finished (job 60613255)
[2026-10-31 20:47:24] scans/TELRUZ/bond_Zn-N6_pos finished (job 60613311)
[2026-10-31 20:48:00] scans/TELRUZ/twist_S1-S2-N5-N6_pos finished (job 60613358)
[2026-10-31 20:48:00] status: 153 jobs queued/running, 807 branches finished (803 back on Aurora), 0 need review
```

## Last autopilot actions

```
[2026-10-31 19:12:17] new farms go to project ModCon (42321 node-hours left)
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 19:29:04] publish: publish: 2 complexes added (584 passing points), 0 not exported; 241 complexes published in total pushed: cdb9dee Aurora results: 241 complexes published (2026-10-31 19:29) 
[2026-10-31 19:42:59] STATUS.md pushed
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 20:15:12] autopilot started (pid 2174001, scripts frozen from /home/dsokaras/dev/xanes2exafs/XANES2EXAFS at fc7ba64, accounts: isaac ModCon)
[2026-10-31 20:20:12] new farms go to project ModCon (42321 node-hours left)
prioritize main: 0 of 0 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-31 20:34:31] publish: publish: 8 complexes added (2124 passing points), 0 not exported; 249 complexes published in total pushed: 8f11a60 Aurora results: 249 complexes published (2026-10-31 20:34) 
```
