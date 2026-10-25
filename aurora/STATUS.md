# Zn scan campaign on Aurora and NERSC Perlmutter: status

Generated 2026-10-25 15:51 UTC by `aurora/autopilot.sh`. Human-written notes are in the run log of `aurora/README.md`; validated results are on the `aurora-results` branch.

## Branches

```
branches: 7086 done, 0 started (running/stopped/failed), 2786 continuations ready, 303 not started, 10175 total
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
branches: 55 finished (48 copied back to Aurora), 485 running, 0 queued, 0 need review, 540 total
stops at the 48 h limit so far: 0; failed runs: 15
193 of your 3982 CPU node-hours on m5268 used
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
| NAMSOJ | 2 / 30 |
| NECTOG | 0 / 30 |
| NONLEI | 0 / 30 |
| OJEKUJ | 19 / 30 |
| OJELOE | 0 / 30 |
| RAYBIC | 3 / 30 |
| REJBUD | 1 / 30 |
| SONROE | 3 / 30 |
| WIGBIX | 1 / 30 |
| WORMAR | 0 / 30 |
| WUJZOS | 26 / 30 |

Last driver actions:

```
[2026-10-25 15:26:56] status: 489 jobs queued/running, 51 branches finished (48 back on Aurora), 0 need review
[2026-10-25 15:28:55] driver started (540 branches, account m5268)
[2026-10-25 15:31:35] scans/NAMSOJ/bond_Zn-N3_neg finished (job 60240153)
[2026-10-25 15:31:35] status: 488 jobs queued/running, 52 branches finished (48 back on Aurora), 0 need review
[2026-10-25 15:44:11] scans/OJEKUJ/angle_S1-Zn-S2_neg finished (job 60240428)
[2026-10-25 15:44:44] scans/REJBUD/bond_Zn-S4_neg finished (job 60240773)
[2026-10-25 15:45:16] scans/WIGBIX/bond_Zn-N45_neg finished (job 60241032)
[2026-10-25 15:45:16] status: 485 jobs queued/running, 55 branches finished (48 back on Aurora), 0 need review
```

## Last autopilot actions

```
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 13:45:52] STATUS.md pushed
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
[2026-10-25 15:28:40] publish: publish: no newly finished complexes 
prioritize main: 131 of 2600 pending branches belong to complexes at least half done
prioritize big: 0 of 0 pending branches belong to complexes at least half done
```
