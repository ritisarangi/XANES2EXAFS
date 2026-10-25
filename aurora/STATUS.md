# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-25 09:37 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7080 done, 0 started (running/stopped/failed), 2791 continuations ready, 304 not started, 10175 total
queue main: 2600 of 39624 waiting, 0 ORCA runs active
queue big: 0 of 0 waiting, 0 ORCA runs active
failed ORCA runs not retried: 2
allocation: 43,851.1 Node Hours available on ModCon
```

## Farm jobs

| Job | Pool | Queue | Nodes | Walltime | State | Elapsed |
|---|---|---|---|---|---|---|
| 8939977 | zn_main | small | 256 | 12:00 | Q | -- |
| 8962257 | zn_main | capacity | 16 | 06:00 | Q | -- |

## NERSC Perlmutter (big pool)

The 18 unfinished big complexes (`remote_refs.txt`) run on Perlmutter: one shared-QOS job per branch (8 cores, 48 h), driven from Aurora through the NERSC IRI API; finished branches are copied back here and published like the others.

```
branches: 45 finished (45 copied back to Aurora), 364 running, 131 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 7
41 of your 3982 CPU node-hours on m5268 used
```

| Complex | Branches finished |
|---|---|
| BUNNII | 0 / 30 |
| CATZUS10 | 0 / 30 |
| DOZVOF | 0 / 30 |
| GUCSED | 0 / 30 |
| GUFHEU | 0 / 30 |
| HOMQAC | 0 / 30 |
| ICAVAK | 0 / 30 |
| NAMSOJ | 0 / 30 |
| NECTOG | 0 / 30 |
| NONLEI | 0 / 30 |
| OJEKUJ | 16 / 30 |
| OJELOE | 0 / 30 |
| RAYBIC | 2 / 30 |
| REJBUD | 0 / 30 |
| SONROE | 1 / 30 |
| WIGBIX | 0 / 30 |
| WORMAR | 0 / 30 |
| WUJZOS | 26 / 30 |

Last driver actions:

```
[2026-10-25 09:08:15] submitted 1 jobs
[2026-10-25 09:08:15] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
[2026-10-25 09:20:54] scans/NAMSOJ/tilt_Zn-S4-C5-O7_neg FAILED (job 60240182, state completed): ['scans/NAMSOJ/tilt_Zn-S4-C5-O7_neg end 2026-10-25 02:12:38']
[2026-10-25 09:21:00] submitted 1 jobs
[2026-10-25 09:21:00] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
[2026-10-25 09:33:44] scans/BUNNII/bond_Zn-S130_pos FAILED (job 60239255, state completed): ['scans/BUNNII/bond_Zn-S130_pos end 2026-10-25 02:31:10']
[2026-10-25 09:33:50] submitted 1 jobs
[2026-10-25 09:33:50] status: 495 jobs queued/running, 45 branches finished (45 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 07:34:42] STATUS.md pushed
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 09:26:11] publish: publish: 2 complexes added (486 passing points), 0 not exported; 167 complexes published in total pushed: d6b91b9 Aurora results: 167 complexes published (2026-10-25 09:26) 
```
